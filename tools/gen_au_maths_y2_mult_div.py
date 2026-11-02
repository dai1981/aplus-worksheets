# -*- coding: utf-8 -*-
"""
AU Year 2 Maths: Multiplying and dividing with groups (Australian Curriculum v9.0, AC9M2N05)
Equal groups and repeated addition, arrays (both number sentences, partitioning an array), sharing equally,
grouping (how many groups of 5 in 20, jumps on a number line), and simple word problems.
  python3 tools/gen_au_maths_y2_mult_div.py
Every drawn picture is counted in code. HTML attributes use single quotes (no backslashes in the JSON).
Year 2 style: numbers well under 1000, very short sentences, mostly groups of 2, 3, 5 and 10, a picture in most questions.
"""
import json, math, os, random, re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "au", "maths", "year-2")
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
GIRLS = ["Charlotte", "Isla", "Mia", "Amelia", "Ava", "Harper", "Chloe", "Ruby", "Mei", "Zara", "Matilda", "Grace"]
BOYS = ["Oliver", "Jack", "Noah", "William", "Leo", "Lachlan", "Liam", "Aarav", "Kai", "Cooper", "Ethan"]
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
        if c in seen or not c or re.match(r"^[-−]\d", c) or re.match(r"^\$?0(c)?( |$)", c):
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
    """n objects in rows of 10 (a small gap after 5), not yet shared or grouped."""
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


def array_svg(rows, cols, kind="dot", split=0):
    """rows x cols array. split=s draws a dashed cut (and a gap) after row s."""
    assert 1 <= rows <= 5 and 1 <= cols <= 10 and 0 <= split < rows
    S, o, GAP = 28, 6, (14 if split else 0)
    el = [shape(kind, o + c * S + S / 2.0, o + i * S + S / 2.0 + (GAP if split and i >= split else 0), 9.5)
          for i in range(rows) for c in range(cols)]
    W, H = cols * S + 2 * o, rows * S + 2 * o + GAP
    label = "array of %d rows and %d columns of %s" % (rows, cols, WORD[kind])
    if split:
        y = o + split * S + GAP / 2.0
        el.append("<line x1='2' y1='%.1f' x2='%d' y2='%.1f' stroke='%s' stroke-width='2.5' stroke-dasharray='6 4'/>"
                  % (y, W - 2, y, RED))
        label += ", split after row %d" % split
    svg = svg_wrap(W, H, "".join(el), label)
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


def jumps_svg(total, k):
    """Number line from 0 to total with equal jumps of k drawn as arcs."""
    assert total % k == 0
    L, R = 16, 16
    u = 360.0 / total
    W = int(L + total * u + R)
    y = 62
    el = ["<line x1='%d' y1='%d' x2='%.1f' y2='%d' stroke='%s' stroke-width='2'/>" % (L - 6, y, L + total * u + 6, y, INK)]
    for i in range(total + 1):
        x = L + i * u
        big = i % k == 0
        el.append("<line x1='%.1f' y1='%d' x2='%.1f' y2='%d' stroke='%s' stroke-width='%s'/>"
                  % (x, y - (8 if big else 4), x, y + (8 if big else 4), INK, "2" if big else "1"))
        if big:
            el.append(text(x, y + 26, str(i), 14))
    njump = 0
    for j in range(total // k):
        x1, x2 = L + j * k * u, L + (j + 1) * k * u
        h = min(34, 10 + k * u * 0.35)
        el.append("<path d='M%.1f,%d Q%.1f,%.1f %.1f,%d' fill='none' stroke='%s' stroke-width='2.5'/>"
                  % (x1, y - 2, (x1 + x2) / 2, y - 2 - 2 * h, x2, y - 2, RED))
        el.append("<polygon points='%.1f,%d %.1f,%d %.1f,%d' fill='%s'></polygon>"
                  % (x2, y - 2, x2 - 7, y - 10, x2 + 1, y - 12, RED))
        njump += 1
    svg = svg_wrap(W, y + 34, "".join(el), "number line from 0 to %d with jumps of %d" % (total, k))
    assert svg.count("<path ") == total // k == njump
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

    for g, n in [(2, 5), (5, 2), (4, 3)]:
        kd = kind()
        e = "Look inside one ring. It has <b>%d</b> %s. Every group is the same." % (n, WORD[kd])
        its.append(mcq(fig(groups_svg([n] * g, kd)) + "How many %s are in each group?" % WORD[kd], n,
                       [g, g * n, n + 1, n - 1], e))

    for g, n in [(2, 3), (5, 2), (3, 5), (2, 10)]:
        kd = kind()
        t = g * n
        e = ("%d groups of %d. Count by %ds: %s. There are <b>%d</b>. (Not %d + %d = %d: that adds the number of groups "
             "to the number in one group.)" % (g, n, n, count_on(n, g), t, g, n, g + n))
        its.append(mcq(fig(groups_svg([n] * g, kd)) + "How many %s are there altogether?" % WORD[kd], t,
                       [g + n, (g + 1) * n, (g - 1) * n, t + 1, g], e))

    for g, n in [(3, 5), (4, 2), (3, 10)]:
        kd = kind()
        right = rep(n, g)
        e = "There are %d groups. Each group has %d. Add %d, %d times: <b>%s</b> = %d." % (g, n, n, g, right, g * n)
        its.append(mcq(fig(groups_svg([n] * g, kd)) + "Which addition matches the picture?", right,
                       ["%d + %d" % (g, n), rep(n, g + 1), rep(g, n) if n <= 5 else rep(n, g - 1), rep(n + 1, g)], e))

    for g, n in [(4, 5), (3, 2), (5, 5)]:
        kd = kind()
        right = "%d × %d = %d" % (g, n, g * n)
        e = "%d groups of %d is written <b>%d × %d</b>. It means %s = %d." % (g, n, g, n, rep(n, g), g * n)
        its.append(mcq(fig(groups_svg([n] * g, kd)) + "Which number sentence matches the picture?", right,
                       ["%d + %d = %d" % (g, n, g + n), "%d × %d = %d" % (g, n, g + n),
                        "%d × %d = %d" % (g + 1, n, (g + 1) * n), "%d × %d = %d" % (g, g, g * g)], e))

    for g, n, wrong, kd in [(3, 4, [[3, 3, 3, 3], [4, 4, 3], [4, 4]], "dot"),
                            (2, 5, [[5, 4], [2, 2, 2, 2, 2], [5, 5, 5]], "star"),
                            (5, 2, [[2, 2, 2, 2], [5, 5], [2, 3, 2, 2, 2]], "square")]:
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


# ============================================================ set 2: arrays
def set_arrays(P):
    its = []
    its.append(mcq(fig(array_svg(3, 5, "dot")) + "How many rows are in this array?", 3, [5, 15, 4],
                   "Rows go across. Count from top to bottom: <b>3</b> rows. Each row has 5."))
    its.append(mcq(fig(array_svg(2, 4, "star")) + "How many columns are in this array?", 4, [2, 8, 6],
                   "Columns go up and down. Count from left to right: <b>4</b> columns. Each column has 2."))

    for r, c, kd in [(2, 5, "square"), (4, 2, "dot"), (3, 10, "star"), (5, 5, "square")]:
        t = r * c
        e = "%d rows of %d. Count by %ds: %s. That is <b>%d</b>. It is %d × %d = %d." % (
            r, c, c, count_on(c, r), t, r, c, t)
        its.append(mcq(fig(array_svg(r, c, kd)) + "How many %s are in the array?" % WORD[kd], t,
                       [r + c, (r + 1) * c, (r - 1) * c, t - 1], e))

    for r, c, kd in [(2, 3, "dot"), (4, 5, "star"), (5, 10, "dot")]:
        right = "%d × %d and %d × %d" % (r, c, c, r)
        wrong = ["%d × %d and %d + %d" % (r, c, r, c), "%d × %d and %d × %d" % (c, r, c, c),
                 "%d × %d and %d × %d" % (r, r, c, c)]
        e = ("Rows: %d rows of %d is %d × %d. Columns: %d columns of %d is %d × %d. "
             "Both make %d, so <b>both</b> match." % (r, c, r, c, c, r, c, r, r * c))
        its.append(mcq(fig(array_svg(r, c, kd)) + "Which two number sentences match this array?", right, wrong, e))

    for r, c, kd in [(2, 10, "square"), (5, 3, "dot"), (3, 4, "star")]:
        t = r * c
        right = "%d × %d = %d" % (c, r, t)
        wrong = ["%d + %d = %d" % (r, c, r + c), "%d × %d = %d" % (c, c, c * c), "%d × %d = %d" % (r, r, r * r)]
        e = ("Count the columns: %d columns of %d. That is <b>%s</b>. "
             "The rows give %d × %d = %d. Same array, same total." % (c, r, right, r, c, t))
        its.append(mcq(fig(array_svg(r, c, kd)) + "This array shows %d × %d = %d. Which other number sentence does it show?"
                       % (r, c, t), right, wrong, e))

    for r, c, s, wrong in [(4, 5, 2, [10, 9, 25]), (5, 3, 2, [6, 9, 8]), (4, 10, 2, [20, 14, 30])]:
        a1, a2 = s * c, (r - s) * c
        t = a1 + a2
        assert t == r * c
        e = ("Top part: %d × %d = %d. Bottom part: %d × %d = %d. Add the parts: %d + %d = <b>%d</b>. "
             "That is %d × %d = %d." % (s, c, a1, r - s, c, a2, a1, a2, t, r, c, t))
        its.append(mcq(fig(array_svg(r, c, "dot", s)) + "The array is split into two parts. How many counters are there in all?",
                       t, wrong, e))

    for a, b in [(5, 2), (10, 3)]:
        t = a * b
        e = ("You can multiply in any order. %d × %d and %d × %d are the same array turned around. "
             "So %d × %d = <b>%d</b> too." % (a, b, b, a, b, a, t))
        its.append(mcq("%d × %d = %d. What is %d × %d?" % (a, b, t, b, a), t, [a + b, t + b, t - a, a * a], e))

    its.append(mcq("Which is true?", "3 × 10 = 10 × 3", ["3 × 10 = 3 + 10", "3 × 10 = 13", "10 × 3 = 103"],
                   "3 × 10 = 30 and 10 × 3 = 30. You can swap the numbers in a multiplication: "
                   "<b>3 × 10 = 10 × 3</b>."))
    its.append(mcq("Ruby says 2 × 5 and 5 × 2 have different answers. Is she right?",
                   "No. Both are 10.", ["Yes. 5 × 2 is bigger.", "No. Both are 7.", "Yes. 2 × 5 is 7."],
                   "2 fives make 10, and 5 twos make 10. <b>No. Both are 10.</b> The order does not matter in ×."))
    its.append(mcq("Which one is <b>not</b> true?", "5 × 3 = 5 + 3",
                   ["5 × 2 = 2 × 5", "10 × 4 = 4 × 10", "3 × 2 = 2 × 3"],
                   "5 × 3 = 15, but 5 + 3 = 8. So <b>5 × 3 = 5 + 3</b> is not true. The others just swap the order, "
                   "and that is fine in ×."))
    assert len(its) == 20, len(its)
    return {"title": "Arrays: rows and columns", "items": its}


# ============================================================ set 3: sharing equally
def set_sharing(P):
    its = []
    for t, k, kd, what in [(10, 2, "dot", "plates"), (6, 3, "star", "plates"), (15, 5, "dot", "plates"),
                           (20, 2, "square", "bags"), (30, 3, "dot", "bags")]:
        a = t // k
        e = ("Give out one at a time, round and round, until none are left. Each %s gets <b>%d</b>. "
             "%d ÷ %d = %d." % (what[:-1], a, t, k, a))
        its.append(mcq(fig(counters_svg(t, kd)) + "Share these %d %s equally between %d %s. How many does each %s get?"
                       % (t, WORD[kd], k, what, what[:-1]), a, [k, t - k, a + 1, a - 1, t], e))

    for t, k in [(12, 3), (10, 5), (20, 2), (15, 3)]:
        a = t // k
        right = "%d ÷ %d = %d" % (t, k, a)
        wrong = ["%d ÷ %d = %d" % (k, t, a), "%d − %d = %d" % (t, k, t - k), "%d ÷ %d = %d" % (t, k, a + 1)]
        e = "%d counters are shared between %d plates. Each plate has %d. That is <b>%s</b>." % (t, k, a, right)
        its.append(mcq(fig(groups_svg([a] * k, "dot", "plate")) +
                       "%d counters are shared between %d plates. Which number sentence matches?" % (t, k),
                       right, wrong, e))

    its.append({"q": "", "c": ["A", "B", "C", "D"], "a": 0,
                "e": ("Sharing between 4 plates means 4 plates, all the same. <b>{L}</b> has 4 plates of 3. "
                      "3 plates of 4 is the wrong number of plates. 3, 3, 3 and 2 is not equal."),
                "_abcd": ("Share 12 counters equally between 4 plates. Which picture shows this?",
                          [3] * 4, [[4, 4, 4], [3, 3, 3, 2], [2, 2, 2, 2]], "dot", "plate")})
    its.append({"q": "", "c": ["A", "B", "C", "D"], "a": 0,
                "e": ("Sharing between 2 plates means 2 plates with the same amount. <b>{L}</b> has 5 and 5. "
                      "6 and 4 is not fair. 5 plates of 2 is the wrong number of plates."),
                "_abcd": ("Share 10 counters equally between 2 plates. Which picture shows this?",
                          [5, 5], [[6, 4], [2, 2, 2, 2, 2], [5, 4]], "star", "plate")})

    for sizes, move, wrong in [([6, 4], 1, [2, 4, 5]), ([7, 3], 2, [4, 5, 3])]:
        t = sum(sizes)
        nm, he, his = P.next()
        e = ("%d ÷ 2 = %d, so each plate needs %d. Move <b>%d</b> from the %d to the %d: %d and %d. "
             "(Moving %d would just swap the plates around.)"
             % (t, t // 2, t // 2, move, sizes[0], sizes[1], t // 2, t // 2, sizes[0] - sizes[1]))
        its.append(mcq(fig(groups_svg(sizes, "dot", "plate", "2 plates with %d and %d counters" % tuple(sizes))) +
                       "%s wants to share %d counters equally between 2 plates. How many counters must move?" % (nm, t),
                       move, wrong, e))

    for t, k in [(16, 2), (25, 5), (40, 10)]:
        a = t // k
        e = ("Share out %d at a time, or count by %ds to %d: %s. That is %d %ss, so each gets <b>%d</b>. "
             "%d ÷ %d = %d." % (k, k, t, count_on(k, a), a, {2: "two", 5: "five", 10: "ten"}[k], a, t, k, a))
        its.append(mcq("Share %d counters equally between %d friends. How many does each friend get?" % (t, k), a,
                       [k, t - k, a + 1, t + k], e))

    its.append(mcq("Which shows 10 shared equally between 2?", "5 and 5", ["6 and 4", "2 and 8", "8 and 2"],
                   "Equal shares are the same size. 5 + 5 = 10 and both are 5, so <b>5 and 5</b>. "
                   "6 and 4 also make 10, but they are not equal."))
    its.append(mcq("Which number sentence shows 15 shared between 5?", "15 ÷ 5 = 3",
                   ["5 ÷ 15 = 3", "15 − 5 = 10", "15 ÷ 5 = 10"],
                   "Sharing is division. Start with the amount you share: <b>15 ÷ 5 = 3</b>. Each gets 3."))
    nm, he, his = P.next()
    its.append(mcq(fig(groups_svg([5, 4, 3], "dot", "plate", "3 plates with 5, 4 and 3 counters")) +
                   "%s shared 12 counters between 3 plates. What went wrong?" % nm,
                   "The plates are not equal. Each should have 4.",
                   ["Nothing. 5 + 4 + 3 = 12.", "%s needs 4 plates." % cap(he), "Each plate should have 3."],
                   "The total is right, but equal shares must be the same. 12 ÷ 3 = 4, so <b>each plate should have 4</b>."))
    its.append(mcq("20 shared between 5 is 4 each. Which number sentence checks this?", "4 × 5 = 20",
                   ["4 + 5 = 9", "20 − 5 = 15", "20 × 5 = 100"],
                   "5 friends with 4 each: 4 + 4 + 4 + 4 + 4 = 20. So <b>4 × 5 = 20</b> checks the sharing."))
    assert len(its) == 20, len(its)
    return {"title": "Sharing equally", "items": its}


# ============================================================ set 4: grouping
def set_grouping(P):
    its = []
    for t, k, kd in [(15, 5, "star"), (8, 2, "dot"), (30, 10, "square"), (9, 3, "dot")]:
        g = t // k
        e = ("Count the rings: %d groups. %d in groups of %d makes <b>%d</b> groups, so %d ÷ %d = %d."
             % (g, t, k, g, t, k, g))
        its.append(mcq(fig(groups_svg([k] * g, kd)) + "%d %s are put into groups of %d. How many groups are there?"
                       % (t, WORD[kd], k), g, [k, t - k, t, g + 1], e))

    for t, k, kd in [(20, 5, "dot"), (12, 2, "star"), (40, 10, "square")]:
        g = t // k
        e = ("Circle %d at a time until none are left. Or count by %ds to %d: %s. That is <b>%d</b> groups. "
             "%d ÷ %d = %d." % (k, k, t, count_on(k, g), g, t, k, g))
        its.append(mcq(fig(counters_svg(t, kd)) + "How many groups of %d can you make with these %d %s?" % (k, t, WORD[kd]),
                       g, [k, t - k, g + 1, g - 1], e))

    for t, k in [(10, 2), (25, 5), (18, 3)]:
        g = t // k
        e = ("Count the jumps: %s. There are <b>%d</b> jumps of %d. So %d ÷ %d = %d."
             % (count_on(k, g), g, k, t, k, g))
        its.append(mcq(fig(jumps_svg(t, k)) + "How many jumps of %d does it take to get from 0 to %d?" % (k, t), g,
                       [k, t, g + 1, t - k], e))

    for t, k in [(40, 10), (35, 5), (14, 2)]:
        g = t // k
        e = "Count by %ds until you reach %d: %s. That is <b>%d</b> groups. %d ÷ %d = %d." % (
            k, t, count_on(k, g), g, t, k, g)
        its.append(mcq("There are %d counters. Put them in groups of %d. How many groups?" % (t, k), g,
                       [k, t - k, g + 1, g - 1], e))

    nm, he, his = P.next()
    its.append({"q": "", "c": ["A", "B", "C", "D"], "a": 0,
                "e": ("%s puts 2 lollies in each bag, so every bag has 2. <b>{L}</b> has 5 bags of 2. "
                      "2 bags of 5 is sharing between 2, not groups of 2." % cap(he)),
                "_abcd": ("%s has 10 lollies. %s puts 2 lollies in each bag. Which picture shows this?" % (nm, cap(he)),
                          [2] * 5, [[5, 5], [2, 2, 2, 2], [3, 3, 4]], "dot", "plate")})
    its.append({"q": "", "c": ["A", "B", "C", "D"], "a": 0,
                "e": ("Groups of 3 means 3 in every ring. <b>{L}</b> has 5 rings of 3, which is 15. "
                      "3 rings of 5 is groups of 5. 4 rings of 3 is only 12."),
                "_abcd": ("Put 15 blocks into groups of 3. Which picture shows this?",
                          [3] * 5, [[5, 5, 5], [3, 3, 3, 3], [3, 3, 4, 5]], "square", "ring")})

    its.append(mcq("Which one is grouping?", "Put 10 eggs in boxes of 2.",
                   ["Share 10 eggs between 2 boxes.", "Add 10 eggs and 2 eggs.", "Take 2 eggs away from 10."],
                   "Grouping means you know how many go in each group. “Boxes of 2” tells you 2 in each box: "
                   "<b>Put 10 eggs in boxes of 2.</b> That makes 5 boxes. Sharing between 2 boxes gives 5 in each box."))

    for t, k in [(12, 3), (10, 5)]:
        g = t // k
        right = "%d ÷ %d = %d" % (t, k, g)
        wrong = ["%d ÷ %d = %d" % (k, t, g), "%d − %d = %d" % (t, k, t - k), "%d + %d = %d" % (t, k, t + k)]
        e = "%d counters in groups of %d make %d groups. Start with the whole amount: <b>%s</b>." % (t, k, g, right)
        its.append(mcq(fig(groups_svg([k] * g, "dot")) + "%d counters are put into groups of %d. Which number sentence matches?"
                       % (t, k), right, wrong, e))

    nm, he, his = P.next()
    its.append(mcq("%s shares 15 counters between 5 friends. %s friend puts 15 counters in groups of 5. "
                   "What number do they both get?" % (nm, cap(his)), 3, [5, 10, 20],
                   "Sharing: 15 shared between 5 is 3 each. Grouping: 15 in groups of 5 is 3 groups. "
                   "Both are 15 ÷ 5 = <b>3</b>."))
    its.append(mcq("How many groups of 10 are in 60?", 6, [10, 50, 70],
                   "Count by 10s: 10, 20, 30, 40, 50, 60. That is <b>6</b> tens. 60 ÷ 10 = 6."))
    assert len(its) == 20, len(its)
    return {"title": "Grouping: how many groups?", "items": its}


# ============================================================ set 5: word problems
def set_story(P):
    its = []

    def add(q, a, w, e, unit="", pic=""):
        if unit == "$":
            u = lambda x: "$%d" % x
        elif unit == "c":
            u = lambda x: "%dc" % x
        elif unit:
            u = lambda x: "%d %s" % (x, unit)
        else:
            u = str
        its.append(mcq((fig(pic) if pic else "") + q, u(a), [u(x) for x in w], e))

    # multiplication
    add("A punnet has 10 strawberries. Mum buys 3 punnets. How many strawberries is that?", 30, [13, 3, 20],
        "3 groups of 10: 10, 20, 30. 3 × 10 = <b>30</b> strawberries.", "strawberries",
        groups_svg([10] * 3, "dot", "plate", "3 punnets of 10 strawberries"))
    add("A kookaburra has 2 legs. There are 6 kookaburras on a branch. How many legs is that?", 12, [8, 6, 14],
        "6 lots of 2: 2, 4, 6, 8, 10, 12. 6 × 2 = <b>12</b> legs.", "legs")
    add("A wombat has 4 legs. There are 3 wombats. How many legs is that?", 12, [7, 3, 16],
        "4 + 4 + 4 = 12. 3 × 4 = <b>12</b> legs. (3 + 4 = 7 adds the wombats to the legs.)", "legs",
        groups_svg([4] * 3, "dot", "ring", "3 groups of 4 legs"))
    add("At the sausage sizzle, each tray has 5 sausages. There are 4 trays. How many sausages is that?", 20,
        [9, 4, 25], "5 + 5 + 5 + 5 = 20. 4 × 5 = <b>20</b> sausages.", "sausages",
        groups_svg([5] * 4, "square", "plate", "4 trays of 5 sausages"))
    nm, he, his = P.next()
    add("An ice block costs $2 at the canteen. %s buys 5 ice blocks. How much does %s pay?" % (nm, he), 10,
        [7, 5, 12], "$2 five times: 2, 4, 6, 8, 10. 5 × $2 = <b>$10</b>.", "$")
    nm, he, his = P.next()
    add("%s has seven 10c coins. How much money is that?" % nm, 70, [17, 7, 60],
        "Count by 10s: 10, 20, 30, 40, 50, 60, 70. 7 × 10c = <b>70c</b>.", "c")
    add("Chairs are set out in 3 rows of 5 for assembly. How many chairs is that?", 15, [8, 10, 20],
        "3 rows of 5: 5, 10, 15. 3 × 5 = <b>15</b> chairs.", "chairs", array_svg(3, 5, "square"))

    # division
    add("20 students make 2 equal teams for footy. How many students are in each team?", 10, [18, 2, 22],
        "20 shared between 2 teams: 20 ÷ 2 = <b>10</b>. Check: 10 + 10 = 20.", "students")
    nm, he, his = P.next()
    add("%s shares 20 stickers equally between 5 friends. How many does each friend get?" % nm, 4, [15, 5, 25],
        "20 ÷ 5 = <b>4</b>. Check: 4 × 5 = 20.", "stickers", counters_svg(20, "star"))
    add("30 students make groups of 5 for sport. How many groups are there?", 6, [25, 5, 35],
        "Count by 5s to 30: 5, 10, 15, 20, 25, 30. That is 6 fives. 30 ÷ 5 = <b>6</b> groups.", "groups")
    add("A baker has 18 muffins. She puts 2 muffins in each box. How many boxes does she fill?", 9, [16, 2, 20],
        "18 in groups of 2: count by 2s to 18 and you say 9 numbers. 18 ÷ 2 = <b>9</b> boxes.", "boxes")
    add("A teacher has 40 pencils. She puts 10 in each tub. How many tubs does she need?", 4, [30, 10, 50],
        "10, 20, 30, 40. That is 4 tens. 40 ÷ 10 = <b>4</b> tubs.", "tubs",
        groups_svg([10] * 4, "square", "ring", "4 groups of 10 pencils"))
    add("Share 14 crackers equally between 2 plates. How many crackers go on each plate?", 7, [12, 2, 16],
        "Half of 14 is 7. 14 ÷ 2 = <b>7</b> crackers. Check: 7 + 7 = 14.", "crackers")
    nm, he, his = P.next()
    add("%s has 50c in 10c coins. How many coins does %s have?" % (nm, he), 5, [40, 10, 60],
        "10c, 20c, 30c, 40c, 50c. That is 5 coins. 50 ÷ 10 = <b>5</b> coins.", "coins")
    add("Some kookaburras sit on a fence. They have 10 legs altogether. Each one has 2 legs. "
        "How many kookaburras are there?", 5, [8, 20, 12],
        "10 legs in groups of 2: 2, 4, 6, 8, 10. 10 ÷ 2 = <b>5</b> kookaburras. (20 is 10 × 2, the wrong way.)",
        "kookaburras")
    add("There are 35 crayons. 5 crayons fit in each box. How many boxes are needed?", 7, [30, 5, 40],
        "35 ÷ 5: count by 5s to 35. That is 7 fives. <b>7</b> boxes.", "boxes")

    # two steps and reasoning
    nm, he, his = P.next()
    add("%s has 3 bags of 10 marbles. %s gives away 5 marbles. How many marbles are left?" % (nm, cap(he)),
        25, [30, 18, 35],
        "Step 1: 3 × 10 = 30. Step 2: 30 − 5 = <b>25</b> marbles.", "marbles")
    nm, he, his = P.next()
    add("%s has 2 cartons of 5 eggs. %s uses 3 eggs. How many eggs are left?" % (nm, cap(he)), 7, [10, 13, 4],
        "Step 1: 2 × 5 = 10 eggs. Step 2: 10 − 3 = <b>7</b> eggs. (4 comes from 2 + 5 − 3.)", "eggs")
    its.append(mcq("There are 15 apples. They are put into bags of 5. Which number sentence tells you how many bags?",
                   "15 ÷ 5 = 3", ["15 × 5 = 75", "15 − 5 = 10", "15 + 5 = 20"],
                   "Putting into bags of 5 is grouping, so divide: <b>15 ÷ 5 = 3</b> bags."))
    nm, he, his = P.next()
    its.append(mcq("%s says, “I have 3 bags of 4 marbles. That is 7 marbles.” What went wrong?" % nm,
                   "%s added. It is 3 × 4 = 12." % cap(he),
                   ["%s should take away: 4 − 3 = 1." % cap(he), "Nothing. 7 is right.",
                    "%s counted the bags. It is 3." % cap(he)],
                   "3 + 4 = 7 adds the bags to one bag. 3 bags of 4 is 4 + 4 + 4. "
                   "<b>%s added. It is 3 × 4 = 12.</b>" % cap(he)))
    assert len(its) == 20, len(its)
    return {"title": "Multiplying and dividing word problems", "items": its}


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
        "<p>Multiplying is about <b>equal groups</b>. Count the groups. Count how many are in one group. "
        "Then add the same number again and again. This is <b>repeated addition</b>.</p>"
        "<figure class='sn-fig'>" + groups_svg([4, 4, 4], "dot", "ring", "3 groups of 4 counters") +
        "<figcaption>3 groups of 4: 4 + 4 + 4 = 12. We write 3 × 4 = 12.</figcaption></figure>"
        + ex("Example", "There are 5 bags. Each bag has 2 apples. How many apples?",
             "5 groups of 2. Count by 2s: 2, 4, 6, 8, 10. So 5 × 2 = 10.", "10 apples")
        + "<h2>Arrays</h2>"
        "<p>An <b>array</b> is objects in rows and columns. <b>Rows</b> go across. <b>Columns</b> go up and down. "
        "Count the rows or count the columns. You get the same total, so one array gives two number sentences.</p>"
        "<figure class='sn-fig'>" + lesson_array_svg(2, 5) +
        "<figcaption>2 rows of 5 is 2 × 5 = 10. 5 columns of 2 is 5 × 2 = 10. Same dots, same total.</figcaption></figure>"
        "<p>You can also <b>split</b> an array into parts you know. 4 rows of 5 is 2 rows of 5 and 2 more rows of 5: "
        "10 + 10 = 20.</p>"
        "<figure class='sn-fig'>" + array_svg(4, 5, "dot", 2) +
        "<figcaption>4 × 5: split it into 2 × 5 = 10 and 2 × 5 = 10. Then 10 + 10 = 20.</figcaption></figure>"
        "<h2>Sharing equally</h2>"
        "<p>Dividing (÷) can mean <b>sharing</b>. You know how many plates. Give out one at a time until none are left. "
        "Every plate must get the same.</p>"
        "<figure class='sn-fig'>" + groups_svg([4, 4, 4], "dot", "plate", "12 counters shared between 3 plates") +
        "<figcaption>12 shared between 3 plates is 4 on each plate. 12 ÷ 3 = 4.</figcaption></figure>"
        "<h2>Grouping</h2>"
        "<p>Dividing can also mean <b>grouping</b>. You know how many go in each group. Make groups until none are left. "
        "Count the groups. Jumps on a number line work the same way.</p>"
        "<figure class='sn-fig'>" + groups_svg([5, 5, 5, 5], "dot", "ring", "20 counters in groups of 5") +
        "<figcaption>20 in groups of 5 makes 4 groups. 20 ÷ 5 = 4.</figcaption></figure>"
        "<figure class='sn-fig'>" + jumps_svg(20, 5) +
        "<figcaption>4 jumps of 5 get from 0 to 20. So there are 4 fives in 20.</figcaption></figure>"
        + ex("Example", "30 students make teams of 5. How many teams?",
             "This is grouping. Count by 5s to 30: 5, 10, 15, 20, 25, 30. That is 6 fives. 30 ÷ 5 = 6.", "6 teams")
        + "<h2>Common mistakes</h2>"
        + table(["Mistake", "What to do instead"], [
            ["Adding the two numbers: 3 × 4 = 7", "Add 4 once for each group: 4 + 4 + 4 = 12"],
            ["Counting the groups, not the objects: 3 groups of 4 = 3", "Count everything inside the rings: 12"],
            ["Unequal groups: 12 shared as 5, 4 and 3", "Every share must be the same: 4, 4 and 4"],
            ["Mixing up sharing and grouping: 10 in groups of 2 drawn as 2 groups of 5",
             "Groups of 2 means 2 in every group. That makes 5 groups"],
        ])
    )


FAQ = [
    {"q": "What multiplication and division do Year 2 students learn in Australia?",
     "a": "Year 2 students learn what multiplying and dividing mean. They use equal groups, repeated addition, arrays, sharing and grouping, mostly with groups of 2, 3, 5 and 10. Quick recall of multiplication facts for 3, 4, 5 and 10 comes in Year 3."},
    {"q": "What is the difference between sharing and grouping?",
     "a": "In sharing, you know how many groups there are and find how many go in each (12 shared between 3 is 4 each). In grouping, you know how many go in each group and find how many groups (12 in groups of 3 is 4 groups). Both are 12 ÷ 3 = 4."},
    {"q": "How do arrays help Year 2 students with multiplication?",
     "a": "An array shows equal rows, so students can count by 2s, 5s or 10s instead of counting one by one. It also shows that 2 × 5 and 5 × 2 give the same total, and a big array can be split into smaller parts."},
    {"q": "How do you explain multiplication to a Year 2 child?",
     "a": "Start with equal groups of real objects, such as 3 plates of 4 biscuits. Add the groups (4 + 4 + 4 = 12), then show that 3 × 4 = 12 is a short way to write it."},
]


def gen():
    rnd = random.Random(2806)
    P = People(rnd)
    sets = [set_groups(P), set_arrays(P), set_sharing(P), set_grouping(P), set_story(P)]
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
            m = re.search(r"aria-label='array of (\d+) rows and (\d+) columns", it["q"])
            if m:
                assert n_objects(it["q"]) == int(m.group(1)) * int(m.group(2)), it["q"]
            for x in it["c"]:
                for n in re.findall(r"\d+", x):
                    assert int(n) < 1000, x
    u = {
        "country": "au", "subject": "maths", "grade": "year-2", "slug": "multiplying-and-dividing-with-groups",
        "sort": 6, "updated": UPDATED, "pdf_url": "",
        "title": "Multiplying and Dividing with Groups",
        "seo_title": "Year 2 Multiplying and Dividing Worksheets: Equal Groups, Arrays, Sharing and Grouping (Free)",
        "short_title": "Multiplying and dividing with groups",
        "domain": "Number",
        "standard_code": "AC9M2N05",
        "standard_url": "https://v9.australiancurriculum.edu.au/f-10-curriculum/learning-areas/mathematics",
        "standard_text": "Multiply and divide by one-digit numbers using repeated addition, equal grouping, arrays, and partitioning to support a variety of calculation strategies",
        "meta_desc": "Free Year 2 maths worksheets on multiplying and dividing, following the Australian Curriculum (AC9M2N05): equal groups and repeated addition, arrays, sharing equally, grouping and word problems. 100 questions with pictures and an answer key.",
        "key_big": "Multiplying is adding equal groups. Dividing is sharing equally or making equal groups.",
        "key_sub": "3 groups of 4 = 4 + 4 + 4 = 3 × 4 = 12. 12 shared between 3 is 4 each, and 12 in groups of 3 is 4 groups: 12 ÷ 3 = 4.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }
    return mark_large(u, "(four pictures|\\d+ (groups|plates|punnets|trays) of|\\d+ \\w+ in rows of 10|"
                         "array of \\d+ rows and 10 |number line)")


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
