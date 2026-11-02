# -*- coding: utf-8 -*-
"""
UK Year 2 Maths: Multiplication and division (National Curriculum in England)
The meaning of × and ÷: equal groups and repeated addition, arrays (multiplication can be done in any order),
sharing and grouping, writing statements with ×, ÷ and = (division cannot be swapped), and word problems.
  python3 tools/gen_uk_maths_y2_mult_div.py
Every drawn picture is counted in code. HTML attributes use single quotes (no backslashes in the JSON).
Year 2 style: numbers up to 100, very short sentences, mostly the 2, 5 and 10 times tables.
"""
import json, math, os, random, re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "uk", "maths", "year-2")
UPDATED = "2026-11-02"
GREEN = "#006633"
FILL = "#cfe6d6"
FILL2 = "#eef6f0"
RED = "#c0392b"
ORANGE = "#d9822b"
BLUE = "#2e6da4"
GREY = "#9a9a9a"
INK = "#2b2b2b"
FONT = "Arial, Helvetica, sans-serif"
GIRLS = ["Amelia", "Isla", "Freya", "Poppy", "Ava", "Aisha", "Lily", "Zara", "Grace", "Ruby", "Maya", "Evie"]
BOYS = ["Oliver", "Harry", "Mohammed", "Jack", "Arjun", "Noah", "George", "Leo", "Alfie", "Kai", "Ethan", "Charlie"]
WORD = {"dot": "counters", "star": "stars", "square": "blocks"}
COL = {"dot": GREEN, "star": ORANGE, "square": BLUE}


# ------------------------------------------------------------ helpers
def mcq(q, correct, cands, e):
    """4 choices: correct + the first 3 unique distractors (no 0 or negatives). Positions are set by balance()."""
    correct = str(correct)
    seen = {correct}
    pick = []
    for c in cands:
        c = str(c)
        if c in seen or not c or re.match(r"^[-−]\d", c) or re.match(r"^0(p)?$", c):
            continue
        seen.add(c)
        pick.append(c)
        if len(pick) == 3:
            break
    assert len(pick) == 3, (q, correct, cands)
    return {"q": q, "c": [correct] + pick, "a": 0, "e": e}


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


def rep(n, times):
    """n + n + n (times addends)."""
    return " + ".join([str(n)] * times)


def count_on(n, times):
    return ", ".join(str(n * (i + 1)) for i in range(times))


# ------------------------------------------------------------ figures
def shape(kind, cx, cy, r, col=None):
    col = col or COL[kind]
    if kind == "dot":
        return "<circle cx='%.1f' cy='%.1f' r='%.1f' fill='%s'/>" % (cx, cy, r, col)
    if kind == "square":
        return ("<rect x='%.1f' y='%.1f' width='%.1f' height='%.1f' rx='2' fill='%s'/>"
                % (cx - r * 0.9, cy - r * 0.9, r * 1.8, r * 1.8, col))
    pts = []
    for k in range(10):
        rr = r * 1.15 if k % 2 == 0 else r * 0.48
        a = -math.pi / 2 + k * math.pi / 5
        pts.append("%.1f,%.1f" % (cx + rr * math.cos(a), cy + rr * math.sin(a)))
    return "<polygon points='%s' fill='%s'/>" % (" ".join(pts), col)


def n_objects(svg):
    """How many objects (counters, stars, blocks) a picture draws."""
    return sum(svg.count("fill='%s'/>" % c) for c in COL.values())


def layout(n):
    """Rows and columns inside one group: up to 3 in a line, then 2 rows."""
    if n <= 3:
        return 1, max(n, 1)
    return 2, (n + 1) // 2


def groups_body(sizes, x0, y0, kind, style, S, r, per_row, G):
    """Boxes (rings or plates) in rows of per_row. Every box has the size of the largest group."""
    rows_in, cols_in = layout(max(sizes))
    P = 6
    bw, bh = cols_in * S + 2 * P, rows_in * S + 2 * P
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
            rr, cc = divmod(i, cols_in)
            el.append(shape(kind, bx + P + cc * S + S / 2.0, by + P + rr * S + S / 2.0, r))
    nrow = (len(sizes) + per_row - 1) // per_row
    ncol = min(len(sizes), per_row)
    return "".join(el), ncol * bw + (ncol - 1) * G, nrow * bh + (nrow - 1) * G


def groups_svg(sizes, kind="dot", style="ring", label=None):
    """Equal groups (ring) or plates after sharing (plate)."""
    M = 5
    body, w, h = groups_body(sizes, M, M, kind, style, 26, 9, 5, 12)
    svg = svg_wrap(int(w + 2 * M), int(h + 2 * M), body, label or (
        "%d %s of %d %s" % (len(sizes), "plates" if style == "plate" else "groups", sizes[0], WORD[kind])))
    assert n_objects(svg) == sum(sizes)
    return svg


def counters_svg(n, kind="dot"):
    """n objects in rows of 10 (a small gap after 5), not yet shared."""
    assert 1 <= n <= 50
    S, r, M = 24, 8.5, 5
    el = []
    for i in range(n):
        rr, cc = divmod(i, 10)
        el.append(shape(kind, M + cc * S + (8 if cc >= 5 else 0) + S / 2.0, M + rr * S + S / 2.0, r))
    cols = min(n, 10)
    W = M * 2 + cols * S + (8 if cols > 5 else 0)
    H = M * 2 + ((n + 9) // 10) * S
    svg = svg_wrap(W, H, "".join(el), "%d %s in rows of 10" % (n, WORD[kind]))
    assert n_objects(svg) == n
    return svg


def array_svg(rows, cols, kind="dot"):
    assert 1 <= rows <= 5 and 1 <= cols <= 10
    S, o = 28, 6
    body = "".join(shape(kind, o + c * S + S / 2.0, o + i * S + S / 2.0, 9.5)
                   for i in range(rows) for c in range(cols))
    svg = svg_wrap(cols * S + 2 * o, rows * S + 2 * o, body,
                   "array of %d rows and %d columns of %s" % (rows, cols, WORD[kind]))
    assert n_objects(svg) == rows * cols
    return svg


def abcd_svg(panels, kind="dot", style="ring"):
    """Four group pictures side by side, labelled A to D. panels: lists of group sizes."""
    S, r, G, PAD = 18, 6.5, 7, 10
    built = []
    for p in panels:
        assert len(p) <= 5 and max(p) <= 10
        built.append(groups_body(p, 0, 0, kind, style, S, r, {4: 2, 5: 3}.get(len(p), len(p)), G))
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
    assert n_objects(svg) == sum(sum(p) for p in panels)
    return svg


def lesson_array_svg(rows, cols):
    """Array with the rows counted on the right and the columns counted below."""
    S, R, x0, y0 = 36, 11, 12, 12
    el = ["".join(shape("dot", x0 + c * S + S / 2.0, y0 + i * S + S / 2.0, R) for i in range(rows) for c in range(cols))]
    for i in range(rows):
        el.append(text(x0 + cols * S + 22, y0 + i * S + S / 2 + 6, str(cols), 17, "middle", RED))
    for c in range(cols):
        el.append(text(x0 + c * S + S / 2, y0 + rows * S + 22, str(rows), 17, "middle", BLUE))
    return svg_wrap(x0 + cols * S + 40, y0 + rows * S + 32, "".join(el),
                    "array of %d rows of %d, with each row and column counted" % (rows, cols))


# ============================================================ set 1: equal groups and repeated addition
def set_groups(P):
    its = []
    kinds = ["dot", "star", "square"]
    k = [0]

    def kind():
        k[0] += 1
        return kinds[(k[0] - 1) % 3]

    for g, n in [(3, 2), (4, 5), (5, 3)]:
        kd = kind()
        e = "Count the rings: there are <b>%d</b> groups. %d is how many %s are in each group." % (g, n, WORD[kd])
        its.append(mcq(fig(groups_svg([n] * g, kd)) + "How many groups are there?", g, [n, g * n, g + 1, g - 1], e))

    for g, n in [(2, 5), (3, 4), (4, 2)]:
        kd = kind()
        e = "Look inside one ring. It has <b>%d</b> %s. Every group is the same." % (n, WORD[kd])
        its.append(mcq(fig(groups_svg([n] * g, kd)) + "How many %s are in each group?" % WORD[kd], n,
                       [g, g * n, n + 1, n - 1], e))

    for g, n in [(2, 3), (5, 2), (3, 5), (2, 10)]:
        kd = kind()
        t = g * n
        e = ("%d groups of %d. Count in %ds: %s. There are <b>%d</b>. (Not %d + %d = %d: that adds the number of groups to the number in one group.)"
             % (g, n, n, count_on(n, g), t, g, n, g + n))
        its.append(mcq(fig(groups_svg([n] * g, kd)) + "How many %s are there altogether?" % WORD[kd], t,
                       [g + n, (g + 1) * n, (g - 1) * n, t + 1, g], e))

    for g, n in [(3, 4), (4, 5), (5, 2)]:
        kd = kind()
        right = rep(n, g)
        e = "There are %d groups. Each group has %d. Add %d, %d times: <b>%s</b> = %d." % (g, n, n, g, right, g * n)
        its.append(mcq(fig(groups_svg([n] * g, kd)) + "Which addition matches the picture?", right,
                       ["%d + %d" % (g, n), rep(n, g + 1), rep(n, g - 1) if g > 2 else rep(n + 1, g), rep(n + 1, g)], e))

    for g, n in [(2, 4), (3, 10), (4, 3)]:
        kd = kind()
        right = "%d × %d" % (g, n)
        e = "%d groups of %d is written <b>%d × %d</b>. It means %s = %d." % (g, n, g, n, rep(n, g), g * n)
        its.append(mcq(fig(groups_svg([n] * g, kd)) + "Which number sentence matches the picture?", right,
                       ["%d + %d" % (g, n), "%d × %d" % (g, g), "%d × %d" % (g + 1, n), "%d × %d" % (n, n)], e))

    for g, n, wrong, kd in [(3, 4, [[3, 3, 3, 3], [4, 4, 3], [4, 4]], "dot"),
                            (2, 5, [[5, 5, 4], [2, 2, 2, 2, 2], [5, 4]], "star"),
                            (4, 2, [[2, 2, 2], [4, 4], [2, 3, 2, 2]], "square")]:
        assert len({tuple(w) for w in wrong}) == 3 and [n] * g not in wrong
        e = ("<b>{L}</b> has %d rings with %d %s in each. Check both numbers: count the groups, "
             "then count inside one group. All the groups must be equal." % (g, n, WORD[kd]))
        its.append({"q": "", "c": ["A", "B", "C", "D"], "a": 0, "e": e,
                    "_abcd": ("Which picture shows %d groups of %d?" % (g, n), [n] * g, wrong, kd, "ring")})

    its.append(mcq("Which is the same as 3 groups of 5?", "5 + 5 + 5",
                   ["3 + 5", "3 + 3 + 3", "5 + 5 + 5 + 5"],
                   "3 groups of 5 means 5, three times: <b>5 + 5 + 5</b> = 15. It is also 3 × 5."))
    assert len(its) == 20, len(its)
    return {"title": "Equal groups and repeated addition", "items": its}


# ============================================================ set 2: arrays (order does not matter)
def set_arrays(P):
    its = []
    its.append(mcq(fig(array_svg(3, 5, "dot")) + "How many rows are in this array?", 3, [5, 15, 4],
                   "Rows go across. Count from top to bottom: <b>3</b> rows. Each row has 5."))
    its.append(mcq(fig(array_svg(2, 4, "star")) + "How many columns are in this array?", 4, [2, 8, 6],
                   "Columns go up and down. Count from left to right: <b>4</b> columns. Each column has 2."))

    for r, c, kd in [(2, 5, "square"), (4, 2, "dot"), (3, 10, "star"), (5, 5, "square")]:
        t = r * c
        e = "%d rows of %d. Count in %ds: %s. That is <b>%d</b>. It is %d × %d = %d." % (
            r, c, c, count_on(c, r), t, r, c, t)
        its.append(mcq(fig(array_svg(r, c, kd)) + "How many %s are in the array?" % WORD[kd], t,
                       [r + c, (r + 1) * c, (r - 1) * c, t - 1], e))

    for r, c, kd in [(2, 5, "dot"), (3, 2, "star"), (5, 10, "dot")]:
        right = "%d × %d and %d × %d" % (r, c, c, r)
        wrong = ["%d × %d and %d + %d" % (r, c, r, c), "%d × %d and %d × %d" % (c, r, c, c),
                 "%d × %d and %d × %d" % (r, r, c, c)]
        e = ("Rows: %d rows of %d is %d × %d. Columns: %d columns of %d is %d × %d. "
             "Both are %d, so <b>both</b> match." % (r, c, r, c, c, r, c, r, r * c))
        its.append(mcq(fig(array_svg(r, c, kd)) + "Which two number sentences match this array?", right, wrong, e))

    for a, b in [(5, 2), (10, 3), (2, 7), (5, 4)]:
        t = a * b
        e = ("You can multiply in any order. %d × %d and %d × %d are the same array turned round. "
             "So %d × %d = <b>%d</b> too." % (a, b, b, a, b, a, t))
        its.append(mcq("%d × %d = %d. What is %d × %d?" % (a, b, t, b, a), t, [a + b, t + b, t - a, a * a], e))

    for a, b in [(4, 5), (2, 9), (10, 6)]:
        e = ("Multiplication can be done in any order. %d × %d = %d × %d, so the missing number is <b>%d</b>. "
             "Both sides are %d." % (a, b, b, a, a, a * b))
        its.append(mcq("%d × %d = %d × <b>?</b>" % (a, b, b), a, [b, a * b, a + b], e))

    its.append(mcq("Which is true?", "3 × 10 = 10 × 3", ["3 × 10 = 3 + 10", "3 × 10 = 13", "10 × 3 = 103"],
                   "3 × 10 = 30 and 10 × 3 = 30. You can swap the numbers in a multiplication: "
                   "<b>3 × 10 = 10 × 3</b>."))
    its.append(mcq("Ruby says 2 × 10 and 10 × 2 have different answers. Is she right?",
                   "No. Both are 20.", ["Yes. 10 × 2 is bigger.", "No. Both are 12.", "Yes. 2 × 10 is 12."],
                   "2 tens make 20, and 10 twos make 20. <b>No. Both are 20.</b> The order does not matter in ×."))
    its.append(mcq("An array has 5 rows of 2. You turn it round. Now it has 2 rows. How many are in each row?",
                   5, [2, 10, 7, 3],
                   "Turning it round does not change the total: 5 × 2 = 10. 2 rows that make 10 have <b>5</b> in each row. "
                   "5 × 2 = 2 × 5."))
    its.append(mcq("Which one is <b>not</b> true?", "5 × 3 = 5 + 3",
                   ["5 × 2 = 2 × 5", "10 × 4 = 4 × 10", "3 × 2 = 2 × 3"],
                   "5 × 3 = 15, but 5 + 3 = 8. So <b>5 × 3 = 5 + 3</b> is not true. The others just swap the order, "
                   "and that is fine in ×."))
    assert len(its) == 20, len(its)
    return {"title": "Arrays: order does not matter", "items": its}


# ============================================================ set 3: sharing and grouping
def set_share_group(P):
    its = []
    # share counters that are not yet shared
    for t, k, kd, what in [(10, 2, "dot", "plates"), (12, 3, "star", "plates"), (15, 5, "dot", "plates"),
                           (20, 2, "square", "boxes")]:
        a = t // k
        e = ("Give out one at a time, round and round, until none are left. Each of the %d %s gets <b>%d</b>. "
             "%d ÷ %d = %d." % (k, what, a, t, k, a))
        its.append(mcq(fig(counters_svg(t, kd)) + "Share these %d %s equally between %d %s. How many %s each %s?"
                       % (t, WORD[kd], k, what, "in" if what == "boxes" else "on", what[:-2] if what == "boxes" else what[:-1]), a, [k, t - k, a + 1, a - 1], e))

    # pictures after sharing
    for t, k in [(12, 3), (10, 5), (20, 4), (16, 2)]:
        a = t // k
        right = "%d ÷ %d = %d" % (t, k, a)
        wrong = ["%d ÷ %d = %d" % (k, t, a), "%d − %d = %d" % (t, k, t - k), "%d ÷ %d = %d" % (t, k, a + 1)]
        e = "%d counters are shared between %d plates. Each plate has %d. That is <b>%s</b>." % (t, k, a, right)
        its.append(mcq(fig(groups_svg([a] * k, "dot", "plate")) +
                       "%d counters are shared between %d plates. Which division does the picture show?" % (t, k),
                       right, wrong, e))

    # grouping with rings
    for t, k, kd in [(15, 5, "star"), (8, 2, "dot"), (30, 10, "square"), (12, 4, "dot")]:
        g = t // k
        e = ("Count the rings: %d groups. %d in groups of %d makes <b>%d</b> groups, so %d ÷ %d = %d."
             % (g, t, k, g, t, k, g))
        its.append(mcq(fig(groups_svg([k] * g, kd)) + "%d %s are put into groups of %d. How many groups are there?"
                       % (t, WORD[kd], k), g, [k, t - k, t, g + 1], e))

    # grouping, no picture
    for t, k in [(20, 2), (35, 5), (50, 10)]:
        g = t // k
        e = "Count in %ds until you reach %d: %s. That is <b>%d</b> groups. %d ÷ %d = %d." % (
            k, t, count_on(k, g), g, t, k, g)
        its.append(mcq("There are %d counters. Put them in groups of %d. How many groups?" % (t, k), g,
                       [k, t - k, g + 1, g - 1], e))

    # sharing or grouping picture (A to D)
    its.append({"q": "", "c": ["A", "B", "C", "D"], "a": 0,
                "e": ("Isla puts 2 sweets in each bag, so every bag has 2. <b>{L}</b> has 5 bags of 2. "
                      "2 bags of 5 is sharing between 2, not groups of 2."),
                "_abcd": ("Isla has 10 sweets. She puts 2 sweets in each bag. Which picture shows this?",
                          [2] * 5, [[5, 5], [2, 2, 2, 2], [3, 3, 3]], "dot", "plate")})
    its.append({"q": "", "c": ["A", "B", "C", "D"], "a": 0,
                "e": ("Sharing between 4 plates means 4 plates, all the same. <b>{L}</b> has 4 plates of 3. "
                      "3 plates of 4 is groups of 4. 3, 3, 3 and 2 is not equal."),
                "_abcd": ("Share 12 counters equally between 4 plates. Which picture shows this?",
                          [3] * 4, [[4, 4, 4], [3, 3, 3, 2], [2, 2, 2, 2]], "dot", "plate")})

    its.append(mcq("Which one is grouping?", "Put 10 eggs in boxes of 2.",
                   ["Share 10 eggs between 2 boxes.", "Add 10 eggs and 2 eggs.", "Take 2 eggs away from 10."],
                   "Grouping means you know how many go in each group. “Boxes of 2” tells you 2 in each box: "
                   "<b>Put 10 eggs in boxes of 2.</b> That makes 5 boxes. Sharing between 2 boxes gives 5 in each box."))
    nm, he, his = P.next()
    its.append(mcq(fig(groups_svg([6, 4], "dot", "plate", "2 plates with 6 and 4 counters")) +
                   "%s wants to share 10 counters equally between 2 plates. How many counters must move?" % nm,
                   1, [2, 4, 5],
                   "10 ÷ 2 = 5, so each plate needs 5. Move <b>1</b> counter from the 6 to the 4: 5 and 5. "
                   "(Moving 2 would make 4 and 6.)"))
    nm, he, his = P.next()
    its.append(mcq("%s shares 15 counters between 5 friends. %s friend puts 15 counters in groups of 5. "
                   "What do they both get?" % (nm, cap(his)), 3, [5, 10, 20],
                   "Sharing: 15 shared between 5 is 3 each. Grouping: 15 in groups of 5 is 3 groups. "
                   "Both are 15 ÷ 5 = <b>3</b>."))
    assert len(its) == 20, len(its)
    return {"title": "Sharing and grouping", "items": its}


# ============================================================ set 4: ×, ÷ and = statements
def set_statements(P):
    its = []
    for a, b, t, s in [(4, 5, 20, "×"), (20, 5, 4, "÷"), (10, 2, 12, "+"), (6, 2, 3, "÷")]:
        val = {"×": a * b, "÷": a // b, "+": a + b}[s]
        assert val == t and (s != "÷" or a % b == 0)
        e = "Try each sign. %d %s %d = %d, so the sign is <b>%s</b>." % (a, s, b, t, s)
        if s == "÷":
            e += " %d shared between %d is %d." % (a, b, t)
        its.append(mcq("Which sign goes in the box? %d □ %d = %d" % (a, b, t), s, ["×", "÷", "+", "−"], e))

    for a, b in [(5, 4), (2, 8), (10, 3), (3, 5)]:
        t = a * b
        right = "%d ÷ %d = %d" % (t, a, b)
        wrong = ["%d ÷ %d = %d" % (a, t, b), "%d ÷ %d = %d" % (t, b, b + 1), "%d ÷ %d = %d" % (b, a, t)]
        e = ("%d groups of %d make %d. So %d shared into %d groups is %d: <b>%s</b>. "
             "Division starts with the whole amount, %d." % (a, b, t, t, a, b, right, t))
        its.append(mcq("%d × %d = %d. Which division fact is also true?" % (a, b, t), right, wrong, e))

    for t, d in [(10, 2), (20, 5), (30, 10)]:
        a = t // d
        right = "%d ÷ %d = %d" % (t, d, a)
        wrong = ["%d ÷ %d = %d" % (d, t, a), "%d ÷ %d = %d" % (t, a, t), "%d ÷ %d = %d" % (a, t, d)]
        e = ("%d shared between %d is %d, so <b>%s</b> is true. You cannot swap the numbers in a division: "
             "%d ÷ %d is not the same as %d ÷ %d." % (t, d, a, right, t, d, d, t))
        its.append(mcq("Which is true?", right, wrong, e))

    its.append(mcq("Which pair gives the same answer?", "3 × 5 and 5 × 3",
                   ["15 ÷ 3 and 3 ÷ 15", "10 ÷ 2 and 2 ÷ 10", "20 ÷ 5 and 5 ÷ 20"],
                   "3 × 5 = 15 and 5 × 3 = 15. <b>Multiplication</b> can be done in any order. "
                   "Division cannot: 10 ÷ 2 = 5, but 2 ÷ 10 is not 5."))
    its.append(mcq("Which can you swap round and still get the same answer?", "2 × 10",
                   ["10 ÷ 2", "20 ÷ 10", "10 − 2"],
                   "2 × 10 = 10 × 2 = 20, so you can swap <b>2 × 10</b>. 10 ÷ 2 = 5, but 2 ÷ 10 is not 5. "
                   "Division and subtraction cannot be swapped."))

    miss = [
        ("<b>?</b> × 5 = 30", 6, [25, 35, 5], "Count in 5s to 30: 5, 10, 15, 20, 25, 30. That is 6 fives, so <b>6</b> × 5 = 30."),
        ("20 = <b>?</b> × 2", 10, [18, 22, 40], "Count in 2s to 20: that takes 10 twos. 20 = <b>10</b> × 2. The = sign can be at the start."),
        ("<b>?</b> ÷ 2 = 6", 12, [3, 4, 8], "Use the inverse: 6 × 2 = 12. So <b>12</b> ÷ 2 = 6. (3 is 6 ÷ 2, the wrong way round.)"),
        ("35 ÷ <b>?</b> = 7", 5, [28, 42, 7], "How many 7s? Think 7 × 5 = 35. So 35 ÷ <b>5</b> = 7."),
        ("<b>?</b> = 40 ÷ 10", 4, [30, 50, 400], "Count in 10s to 40: 10, 20, 30, 40. That is 4 tens. <b>4</b> = 40 ÷ 10."),
    ]
    for q, a, w, e in miss:
        its.append(mcq("What is the missing number? " + q, a, w, e))

    its.append(mcq("Which number sentence shows 5 groups of 2?", "5 × 2 = 10",
                   ["5 + 2 = 7", "5 × 2 = 7", "5 × 5 = 25"],
                   "5 groups of 2 is 2 + 2 + 2 + 2 + 2 = 10. We write it <b>5 × 2 = 10</b>."))
    its.append(mcq("Which number sentence shows 15 shared between 5?", "15 ÷ 5 = 3",
                   ["5 ÷ 15 = 3", "15 − 5 = 10", "15 ÷ 5 = 10"],
                   "Sharing is division. Start with the amount you share: <b>15 ÷ 5 = 3</b>. Each gets 3."))
    assert len(its) == 20, len(its)
    return {"title": "Writing ×, ÷ and = statements", "items": its}


# ============================================================ set 5: word problems
def set_story(P):
    its = []

    def add(q, a, w, e, unit=""):
        u = lambda x: (str(x) + unit) if unit in ("p",) else ("%d %s" % (x, unit) if unit else str(x))
        its.append(mcq(q, u(a), [u(x) for x in w], e))

    # multiplication
    add("A box holds 5 cakes. How many cakes are in 4 boxes?", 20, [9, 4, 25, 15],
        "4 boxes of 5: 5 + 5 + 5 + 5 = 20. 4 × 5 = <b>20</b> cakes.", "cakes")
    add("There are 6 birds on a fence. Each bird has 2 legs. How many legs is that?", 12, [8, 6, 14],
        "6 lots of 2: 2, 4, 6, 8, 10, 12. 6 × 2 = <b>12</b> legs.", "legs")
    add("There are 3 dogs in the park. Each dog has 4 legs. How many legs is that?", 12, [7, 3, 16],
        "4 + 4 + 4 = 12. 3 × 4 = <b>12</b> legs. (3 + 4 = 7 adds the dogs to the legs.)", "legs")
    nm, he, his = P.next()
    add("%s has 7 pairs of socks. A pair is 2 socks. How many socks does %s have?" % (nm, he), 14, [9, 7, 12],
        "7 pairs of 2: count in 2s seven times. 7 × 2 = <b>14</b> socks.", "socks")
    nm, he, his = P.next()
    add("A pack has 10 stickers. %s buys 3 packs. How many stickers does %s have?" % (nm, he), 30, [13, 3, 20],
        "10, 20, 30. 3 × 10 = <b>30</b> stickers.", "stickers")
    add("There are 8 hands. Each hand has 5 fingers. How many fingers is that?", 40, [13, 8, 35],
        "Count in 5s eight times: 5, 10, 15, 20, 25, 30, 35, 40. 8 × 5 = <b>40</b> fingers.", "fingers")
    nm, he, his = P.next()
    add("A sweet costs 5p. %s buys 4 sweets. How much does %s pay?" % (nm, he), 20, [9, 4, 25],
        "5p + 5p + 5p + 5p = 20p. 4 × 5 = <b>20p</b>.", "p")
    nm, he, his = P.next()
    add("%s has six 10p coins. How much money is that?" % nm, 60, [16, 6, 50],
        "Count in 10s: 10, 20, 30, 40, 50, 60. 6 × 10 = <b>60p</b>.", "p")

    # division
    nm, he, his = P.next()
    add("%s shares 20 stickers equally between 5 friends. How many does each friend get?" % nm, 4, [15, 5, 25],
        "20 ÷ 5 = <b>4</b>. Check: 4 × 5 = 20.", "stickers")
    add("There are 30 children in PE. They make teams of 5. How many teams are there?", 6, [25, 5, 35],
        "Count in 5s to 30: 5, 10, 15, 20, 25, 30. That is 6 fives. 30 ÷ 5 = <b>6</b> teams.", "teams")
    add("A baker has 18 cakes. She puts 2 cakes in each box. How many boxes does she fill?", 9, [16, 2, 20],
        "18 in groups of 2: count in 2s to 18 and you say 9 numbers. 18 ÷ 2 = <b>9</b> boxes.", "boxes")
    add("A teacher has 40 pencils. She puts 10 in each pot. How many pots does she need?", 4, [30, 10, 50],
        "10, 20, 30, 40. That is 4 tens. 40 ÷ 10 = <b>4</b> pots.", "pots")
    add("Share 14 biscuits equally between 2 plates. How many biscuits go on each plate?", 7, [12, 2, 16],
        "Half of 14 is 7. 14 ÷ 2 = <b>7</b> biscuits. Check: 7 + 7 = 14.", "biscuits")
    nm, he, his = P.next()
    add("%s has 50p in 10p coins. How many coins does %s have?" % (nm, he), 5, [40, 10, 60],
        "10p, 20p, 30p, 40p, 50p. That is 5 coins. 50 ÷ 10 = <b>5</b> coins.", "coins")
    add("Some ducks are on a pond. They have 12 legs altogether. Each duck has 2 legs. How many ducks are there?",
        6, [10, 24, 14], "12 legs in pairs of 2: 12 ÷ 2 = <b>6</b> ducks. (24 is 12 × 2, the wrong way.)", "ducks")
    add("There are 35 crayons. 5 crayons fit in each box. How many boxes are needed?", 7, [30, 5, 40],
        "35 ÷ 5: count in 5s to 35. That is 7 fives. <b>7</b> boxes.", "boxes")

    # two steps and reasoning
    nm, he, his = P.next()
    add("%s has 3 bags of 10 marbles. %s gives away 5 marbles. How many marbles are left?" % (nm, cap(he)),
        25, [30, 18, 35],
        "Step 1: 3 × 10 = 30. Step 2: 30 − 5 = <b>25</b> marbles.", "marbles")
    nm, he, his = P.next()
    add("%s has 2 boxes of 5 eggs. %s uses 3 eggs. How many eggs are left?" % (nm, cap(he)), 7, [10, 13, 4],
        "Step 1: 2 × 5 = 10 eggs. Step 2: 10 − 3 = <b>7</b> eggs. (4 comes from 2 + 5 − 3.)", "eggs")
    its.append(mcq("There are 15 apples. They are put into bags of 5. Which calculation tells you how many bags?",
                   "15 ÷ 5 = 3", ["15 × 5 = 75", "15 − 5 = 10", "15 + 5 = 20"],
                   "Putting into bags of 5 is grouping, so divide: <b>15 ÷ 5 = 3</b> bags."))
    nm, he, his = P.next()
    its.append(mcq("%s says, “I have 4 bags of 5 marbles. That is 9 marbles.” What went wrong?" % nm,
                   "%s added. It is 4 × 5 = 20." % cap(he),
                   ["%s should take away: 5 − 4 = 1." % cap(he), "Nothing. 9 is right.",
                    "%s counted the bags. It is 4." % cap(he)],
                   "4 + 5 = 9 adds the bags to one bag. 4 bags of 5 is 5 + 5 + 5 + 5. "
                   "<b>%s added. It is 4 × 5 = 20.</b>" % cap(he)))
    assert len(its) == 20, len(its)
    return {"title": "Multiplication and division word problems", "items": its}


# ============================================================ balance (and build A-D pictures)
def balance(sets, rnd):
    """Spread the correct answers evenly over the 4 positions in every set."""
    for s in sets:
        targets = [0, 1, 2, 3] * 5
        rnd.shuffle(targets)
        for it, t in zip(s["items"], targets):
            if "_abcd" in it:
                prompt, right, wrong, kind, style = it.pop("_abcd")
                wrong = list(wrong)
                rnd.shuffle(wrong)
                panels = wrong[:t] + [right] + wrong[t:]
                it["q"] = fig(abcd_svg(panels, kind, style)) + prompt
                it["a"] = t
                it["e"] = it["e"].replace("{L}", "ABCD"[t])
                continue
            c = it["c"]
            right = c[it["a"]]
            wrong = [x for i, x in enumerate(c) if i != it["a"]]
            rnd.shuffle(wrong)
            it["c"] = wrong[:t] + [right] + wrong[t:]
            it["a"] = t


def mark_large(u, pattern):
    """Tag wide pictures so they print larger and the objects stay easy to count."""
    rx = re.compile(r"<svg (?=[^>]*aria-label='" + pattern + ")")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u


# ============================================================ lesson
def body_html():
    return (
        "<h2>Equal groups</h2>"
        "<p>Multiplication is about <b>equal groups</b>. Count the groups. Count how many are in one group. "
        "Then add the same number again and again. This is <b>repeated addition</b>.</p>"
        "<figure class='sn-fig'>" + groups_svg([4, 4, 4], "dot", "ring", "3 groups of 4 counters") +
        "<figcaption>3 groups of 4: 4 + 4 + 4 = 12. We write 3 × 4 = 12.</figcaption></figure>"
        + ex("Example", "There are 5 bags. Each bag has 2 apples. How many apples?",
             "5 groups of 2. Count in 2s: 2, 4, 6, 8, 10. So 5 × 2 = 10.", "10 apples")
        + "<h2>Arrays: any order</h2>"
        "<p>An <b>array</b> is objects in rows and columns. <b>Rows</b> go across. <b>Columns</b> go up and down. "
        "Count the rows or count the columns. You get the same total.</p>"
        "<figure class='sn-fig'>" + lesson_array_svg(2, 5) +
        "<figcaption>2 rows of 5 is 2 × 5 = 10. 5 columns of 2 is 5 × 2 = 10. Same dots, same total.</figcaption></figure>"
        "<p>So you can multiply in <b>any order</b>: 2 × 5 = 5 × 2. This is a handy trick. "
        "If you know 2 × 10 = 20, you know 10 × 2 = 20 too.</p>"
        "<h2>Sharing and grouping</h2>"
        "<p>Division (÷) has two meanings. <b>Sharing</b>: you know how many plates. Give out one at a time. "
        "<b>Grouping</b>: you know how many go in each group. Make groups until none are left.</p>"
        "<figure class='sn-fig'>" + groups_svg([4, 4, 4], "dot", "plate", "12 counters shared between 3 plates") +
        "<figcaption>Sharing: 12 shared between 3 plates is 4 on each plate. 12 ÷ 3 = 4.</figcaption></figure>"
        "<figure class='sn-fig'>" + groups_svg([3, 3, 3, 3], "dot", "ring", "12 counters in groups of 3") +
        "<figcaption>Grouping: 12 in groups of 3 makes 4 groups. 12 ÷ 3 = 4.</figcaption></figure>"
        + ex("Example", "30 children make teams of 5. How many teams?",
             "This is grouping. Count in 5s to 30: 5, 10, 15, 20, 25, 30. That is 6 fives. 30 ÷ 5 = 6.", "6 teams")
        + "<h2>×, ÷ and =</h2>"
        "<p>One picture gives you four facts. Multiplication can be swapped. <b>Division cannot be swapped</b>: "
        "10 ÷ 2 = 5, but 2 ÷ 10 is not 5. A division starts with the whole amount.</p>"
        + table(["Picture", "× facts", "÷ facts"], [
            ["2 rows of 5", "2 × 5 = 10 and 5 × 2 = 10", "10 ÷ 2 = 5 and 10 ÷ 5 = 2"],
            ["3 groups of 10", "3 × 10 = 30 and 10 × 3 = 30", "30 ÷ 3 = 10 and 30 ÷ 10 = 3"],
            ["4 groups of 5", "4 × 5 = 20 and 5 × 4 = 20", "20 ÷ 4 = 5 and 20 ÷ 5 = 4"],
        ])
        + "<p>The = sign means “is the same as”. It can go at the start too: 20 = 4 × 5.</p>"
        "<h2>Common mistakes</h2>"
        + table(["Mistake", "What to do instead"], [
            ["Adding the two numbers: 3 groups of 4 = 7", "Add 4 once for each group: 4 + 4 + 4 = 12"],
            ["Counting the groups, not the objects: 3 groups of 4 = 3", "Count everything inside the rings: 12"],
            ["Mixing up sharing and grouping: 10 in groups of 2 drawn as 2 groups of 5",
             "Groups of 2 means 2 in every group. That makes 5 groups"],
            ["Swapping a division: 2 ÷ 10 = 5", "Start with the whole amount: 10 ÷ 2 = 5"],
        ])
    )


FAQ = [
    {"q": "What times tables do Year 2 children learn?",
     "a": "Year 2 children learn the 2, 5 and 10 times tables, with the matching division facts. They also learn what × and ÷ mean, using equal groups, arrays, sharing and grouping."},
    {"q": "What is the difference between sharing and grouping?",
     "a": "In sharing, you know how many groups there are and find how many go in each (12 shared between 3 is 4 each). In grouping, you know the size of each group and find how many groups (12 in groups of 3 is 4 groups). Both are 12 ÷ 3 = 4."},
    {"q": "Why can you swap the numbers in multiplication but not in division?",
     "a": "An array of 2 rows of 5 turned round is 5 rows of 2, so 2 × 5 = 5 × 2. Division is not like this: 10 ÷ 2 = 5, but 2 ÷ 10 is not 5."},
    {"q": "How do you explain multiplication to a Year 2 child?",
     "a": "Start with equal groups of real objects, such as 3 plates of 4 biscuits. Add the groups (4 + 4 + 4 = 12), then show that 3 × 4 = 12 is a short way to write it."},
]


def gen():
    rnd = random.Random(2206)
    P = People(rnd)
    sets = [set_groups(P), set_arrays(P), set_share_group(P), set_statements(P), set_story(P)]
    balance(sets, rnd)
    keys = set()
    for s in sets:
        assert len(s["items"]) == 20, (s["title"], len(s["items"]))
        assert sorted(it["a"] for it in s["items"]) == sorted([0, 1, 2, 3] * 5), s["title"]
        for it in s["items"]:
            assert len(set(it["c"])) == 4, it
            assert it["q"].count("<svg") <= 1, it["q"]
            assert "{" not in it["e"] and "_abcd" not in it
            k = it["q"] + "|" + "|".join(sorted(it["c"]))
            assert k not in keys, it["q"]
            keys.add(k)
            # every array has as many objects as its label says
            m = re.search(r"aria-label='array of (\d+) rows and (\d+) columns", it["q"])
            if m:
                assert n_objects(it["q"]) == int(m.group(1)) * int(m.group(2)), it["q"]
    u = {
        "country": "uk", "subject": "maths", "grade": "year-2", "slug": "multiplication-and-division", "sort": 6,
        "updated": UPDATED, "pdf_url": "",
        "title": "Multiplication and Division",
        "seo_title": "Year 2 Multiplication and Division Worksheets: Equal Groups, Arrays, Sharing and Grouping",
        "short_title": "Multiplication and division",
        "domain": "Multiplication and division",
        "standard_code": "Year 2: Multiplication and division",
        "standard_url": "https://www.gov.uk/government/publications/national-curriculum-in-england-mathematics-programmes-of-study",
        "standard_text": "Calculate mathematical statements for multiplication and division within the multiplication tables and write them using the multiplication (×), division (÷) and equals (=) signs; show that multiplication of two numbers can be done in any order (commutative) and division of one number by another cannot; solve problems involving multiplication and division, using materials, arrays, repeated addition, mental methods, and multiplication and division facts, including problems in contexts.",
        "meta_desc": "Free Year 2 maths worksheets on multiplication and division, following the National Curriculum: equal groups and repeated addition, arrays, sharing and grouping, writing ×, ÷ and = statements, and word problems. 100 questions with pictures and an answer key.",
        "key_big": "Multiplication is equal groups. Division is sharing or grouping.",
        "key_sub": "3 groups of 4 = 4 + 4 + 4 = 3 × 4 = 12. You can swap a multiplication (2 × 5 = 5 × 2), but not a division (10 ÷ 2 is not 2 ÷ 10).",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }
    return mark_large(u, "(four pictures|\\d+ (groups|plates) of|\\d+ \\w+ in rows of 10|array of \\d+ rows and 10 )")


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
