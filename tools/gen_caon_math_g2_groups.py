# -*- coding: utf-8 -*-
"""
CA Grade 2 Math: Equal groups and sharing (Ontario Mathematics Curriculum 2020, B2.5 and B2.6)
Equal groups and repeated addition, arrays, groups of one half and one fourth (4 halves make 2 wholes),
sharing up to 12 items equally, and word problems.
  python3 tools/gen_caon_math_g2_groups.py
Every drawn picture is counted in code. HTML attributes use single quotes (no backslashes in the JSON).
Grade 2 style: very short sentences, a picture in most questions, repeated addition (no × or ÷ signs in the
questions), sharing only up to 12 items. Canadian English.
"""
import json, math, os, random, re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "ca-on", "math", "grade-2")
UPDATED = "2026-11-02"
GREEN = "#006633"
FILL2 = "#eef6f0"
RED = "#c0392b"
ORANGE = "#d9822b"
BLUE = "#2e6da4"
GREY = "#9a9a9a"
INK = "#2b2b2b"
PIECE = "#f2b36b"
PIECE_LINE = "#a85d12"
FONT = "Arial, Helvetica, sans-serif"
GIRLS = ["Olivia", "Emma", "Maya", "Zoe", "Amira", "Mei", "Chloe", "Priya", "Leah", "Hana", "Ava", "Sofia"]
BOYS = ["Liam", "Noah", "Aiden", "Lucas", "Owen", "Arjun", "Ethan", "Jayden", "Benjamin", "Mateo", "Nathan", "Kai"]
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
        if c in seen or not c or re.match(r"^[-−]\d", c) or re.match(r"^0( |¢|$)", c):
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


def wholes(w):
    return "%d whole%s" % (w, "" if w == 1 else "s")


def amount(halves=0, fourths=0):
    """A count of halves or fourths in words: '2 wholes', '1 and a half', '1 and 3 fourths'."""
    if halves:
        w, r = divmod(halves, 2)
        return wholes(w) if not r else ("a half" if not w else "%d and a half" % w)
    w, r = divmod(fourths, 4)
    if not r:
        return wholes(w)
    assert r != 2  # 2 fourths: say “a half” instead (never two equal choices)
    part = "1 fourth" if r == 1 else "3 fourths"
    return part if not w else "%d and %s" % (w, part)


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
        built.append(groups_body(p, 0, 0, kind, style, S, r, {3: 2, 4: 2, 5: 3}.get(len(p), len(p)), G))
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


# ---- halves and fourths
def piece(d, cx, cy, r, sw=2):
    """One half (a half circle, flat side down) or one fourth (a quarter circle) of a round orange or pizza.
    (cx, cy) is the middle of the piece's box."""
    st = "fill='%s' stroke='%s' stroke-width='%s' stroke-linejoin='round'" % (PIECE, PIECE_LINE, sw)
    if d == 2:
        y = cy + r / 2.0
        return "<path class='pc' d='M%.1f %.1f A%.1f %.1f 0 0 1 %.1f %.1f Z' %s/>" % (cx - r, y, r, r, cx + r, y, st)
    x, y = cx - r / 2.0, cy + r / 2.0
    return ("<path class='pc' d='M%.1f %.1f L%.1f %.1f A%.1f %.1f 0 0 1 %.1f %.1f Z' %s/>"
            % (x, y, x, y - r, r, r, x + r, y, st))


def n_pieces(svg):
    return svg.count("class='pc'")


def pieces_svg(n, d, plates=False, label=None):
    """n separate halves (d=2) or fourths (d=4), up to 5 in a row. plates=True puts each piece on its own plate."""
    r = 20 if d == 2 else 26
    cw, ch = (2 * r + 18, r + 22) if d == 2 else (r + 22, r + 22)
    if plates:
        cw, ch = cw + 8, ch + 8
    per = 5
    el = []
    for i in range(n):
        rr, cc = divmod(i, per)
        x0, y0 = 5 + cc * cw, 5 + rr * ch
        cx, cy = x0 + cw / 2.0, y0 + ch / 2.0
        if plates:
            el.append("<rect x='%.1f' y='%.1f' width='%.1f' height='%.1f' rx='%.1f' fill='%s' stroke='%s' stroke-width='2'/>"
                      % (x0 + 3, y0 + 3, cw - 6, ch - 6, (ch - 6) / 2.0, FILL2, GREEN))
        el.append(piece(d, cx, cy, r))
    cols = min(n, per)
    rows = (n + per - 1) // per
    name = "halves" if d == 2 else "fourths"
    svg = svg_wrap(int(10 + cols * cw), int(10 + rows * ch), "".join(el),
                   label or "%d %s%s" % (n, name, ", each on its own plate" if plates else ""))
    assert n_pieces(svg) == n
    return svg


def cut_svg(w, d, label=None):
    """w whole circles (oranges or pizzas), each cut into d equal pieces."""
    R, G, M = 30, 14, 6
    el = []
    for k in range(w):
        cx, cy = M + R + k * (2 * R + G), M + R
        for i in range(d):
            a0 = math.radians(-90 + 360.0 * i / d)
            a1 = math.radians(-90 + 360.0 * (i + 1) / d)
            el.append("<path class='pc' d='M%.1f %.1f L%.1f %.1f A%d %d 0 0 1 %.1f %.1f Z' fill='%s' stroke='%s' "
                      "stroke-width='2.5' stroke-linejoin='round'/>"
                      % (cx, cy, cx + R * math.cos(a0), cy + R * math.sin(a0), R, R,
                         cx + R * math.cos(a1), cy + R * math.sin(a1), PIECE, PIECE_LINE))
    svg = svg_wrap(int(2 * M + w * 2 * R + (w - 1) * G), 2 * M + 2 * R, "".join(el),
                   label or "%d wholes, each cut into %s" % (w, "halves" if d == 2 else "fourths"))
    assert n_pieces(svg) == w * d
    return svg


def lesson_halves_svg():
    """4 halves on the left, then the same 4 halves pushed together into 2 wholes."""
    r = 22
    el = []
    for i in range(4):
        el.append(piece(2, 30 + i * 52, 40, r))
    el.append(text(240, 46, "=", 26))
    for k in range(2):
        cx = 290 + k * 58
        el.append(piece(2, cx, 29, r))
        el.append(piece(2, cx, 29, r).replace("A%.1f %.1f 0 0 1" % (r, r), "A%.1f %.1f 0 0 0" % (r, r)))
    svg = svg_wrap(372, 68, "".join(el), "4 halves make 2 whole circles")
    assert n_pieces(svg) == 8
    return svg


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

    for g, n in [(2, 3), (5, 2), (3, 5), (2, 10), (3, 4)]:
        kd = kind()
        t = g * n
        e = ("%d groups of %d: %s = <b>%d</b>. (Not %d: that is just the number of groups. "
             "Not %d + %d = %d: that adds the groups to one group.)" % (g, n, rep(n, g), t, g, g, n, g + n))
        its.append(mcq(fig(groups_svg([n] * g, kd)) + "How many %s are there in all?" % WORD[kd], t,
                       [g + n, g, (g + 1) * n, (g - 1) * n, t + 1], e))

    for g, n in [(3, 5), (4, 2), (3, 10), (4, 3)]:
        kd = kind()
        right = rep(n, g)
        e = "There are %d groups. Each group has %d. Add %d, %d times: <b>%s</b> = %d." % (g, n, n, g, right, g * n)
        its.append(mcq(fig(groups_svg([n] * g, kd)) + "Which addition matches the picture?", right,
                       ["%d + %d" % (g, n), rep(n, g + 1), rep(n, g - 1), rep(n + 1, g)], e))

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
                   "3 groups of 5 means 5, three times: <b>5 + 5 + 5</b> = 15."))
    its.append(mcq("Count by 5s. How many are in 4 groups of 5?", 20, [9, 15, 25, 4],
                   "Say one 5 for each group: 5, 10, 15, 20. 4 groups of 5 is <b>20</b>. "
                   "(9 comes from 4 + 5.)"))
    assert len(its) == 20, len(its)
    return {"title": "Equal groups and repeated addition", "items": its}


# ============================================================ set 2: arrays
def set_arrays(P):
    its = []
    for r, c, kd in [(3, 5, "dot"), (4, 3, "square")]:
        its.append(mcq(fig(array_svg(r, c, kd)) + "How many rows are in this array?", r, [c, r * c, r + 1],
                       "Rows go across. Count from top to bottom: <b>%d</b> rows. Each row has %d." % (r, c)))
    for r, c, kd in [(2, 4, "star"), (5, 2, "dot")]:
        its.append(mcq(fig(array_svg(r, c, kd)) + "How many columns are in this array?", c, [r, r * c, c + 2],
                       "Columns go up and down. Count from left to right: <b>%d</b> columns. Each column has %d."
                       % (c, r)))

    for r, c, kd in [(2, 5, "square"), (4, 2, "dot"), (3, 10, "star"), (5, 5, "square"), (3, 4, "dot")]:
        t = r * c
        e = "%d rows of %d: %s = <b>%d</b>. (Not %d + %d = %d: that adds the rows to one row.)" % (
            r, c, rep(c, r), t, r, c, r + c)
        its.append(mcq(fig(array_svg(r, c, kd)) + "How many %s are in the array?" % WORD[kd], t,
                       [r + c, (r + 1) * c, (r - 1) * c, t - 1, t + 1], e))

    for r, c, kd in [(2, 3, "dot"), (4, 5, "star"), (3, 10, "square")]:
        right = rep(c, r)
        e = "Each row has %d. There are %d rows. So add %d, %d times: <b>%s</b> = %d." % (c, r, c, r, right, r * c)
        its.append(mcq(fig(array_svg(r, c, kd)) + "Add the rows. Which addition matches?", right,
                       ["%d + %d" % (r, c), rep(c, r + 1), rep(c + 1, r), rep(c, r - 1)], e))

    for r, c, kd in [(5, 3, "dot"), (3, 4, "star"), (2, 5, "square")]:
        right = rep(r, c)
        e = ("Each column has %d. There are %d columns. So add %d, %d times: <b>%s</b> = %d. "
             "Adding the rows gives %d too." % (r, c, r, c, right, r * c, r * c))
        its.append(mcq(fig(array_svg(r, c, kd)) + "Add the columns. Which addition matches?", right,
                       ["%d + %d" % (r, c), rep(r, c + 1), rep(r + 1, c), rep(r, c - 1)], e))

    for r, c, s, wrong in [(4, 5, 2, [10, 9, 25]), (5, 3, 2, [6, 9, 8])]:
        a1, a2 = s * c, (r - s) * c
        t = a1 + a2
        assert t == r * c
        e = ("Top part: %s = %d. Bottom part: %s = %d. Add the parts: %d + %d = <b>%d</b>."
             % (rep(c, s), a1, rep(c, r - s), a2, a1, a2, t))
        its.append(mcq(fig(array_svg(r, c, "dot", s)) + "The array is split into two parts. How many counters are there in all?",
                       t, wrong, e))

    nm, he, his = P.next()
    its.append(mcq("%s says 2 rows of 5 and 5 rows of 2 have different totals. Is %s right?" % (nm, he),
                   "No. Both are 10.", ["Yes. 5 rows is more.", "No. Both are 7.", "Yes. 2 rows is less."],
                   "5 + 5 = 10 and 2 + 2 + 2 + 2 + 2 = 10. <b>No. Both are 10.</b> It is the same array, turned."))
    its.append(mcq("Which array has the same number of dots as 3 rows of 4?", "4 rows of 3",
                   ["3 rows of 3", "4 rows of 4", "3 rows of 5"],
                   "3 rows of 4 is 4 + 4 + 4 = 12. <b>4 rows of 3</b> is 3 + 3 + 3 + 3 = 12. Turning an array keeps the total."))
    its.append(mcq("An array has 5 rows of 10. Count by 10s. How many dots?", 50, [15, 40, 60],
                   "Say one 10 for each row: 10, 20, 30, 40, 50. That is <b>50</b> dots. (15 comes from 5 + 10.)"))
    assert len(its) == 20, len(its)
    return {"title": "Arrays: rows and columns", "items": its}


# ============================================================ set 3: groups of halves and fourths
def set_parts(P):
    its = []
    for n in [4, 6, 8, 10]:
        w = n // 2
        e = ("2 halves make 1 whole. Put the halves in pairs: %d halves make <b>%s</b>. "
             "(%d counts the pieces, not the whole oranges.)" % (n, wholes(w), n))
        its.append(mcq(fig(pieces_svg(n, 2, label="%d orange halves" % n)) +
                       "Here are %d orange halves. How many whole oranges do they make?" % n,
                       wholes(w), [wholes(n), wholes(n * 2), wholes(w + 1), wholes(w - 1)], e))

    for n in [3, 5, 7]:
        w = n // 2
        e = ("Make pairs: %d pair%s of halves make%s %s. One half is left over. That is <b>%s</b>."
             % (w, "" if w == 1 else "s", "s" if w == 1 else "", wholes(w), amount(halves=n)))
        its.append(mcq(fig(pieces_svg(n, 2, label="%d orange halves" % n)) +
                       "Here are %d orange halves. How many whole oranges do they make?" % n,
                       amount(halves=n), [wholes(n), wholes(w), wholes(w + 1)], e))

    for n in [4, 8, 12]:
        w = n // 4
        e = ("4 fourths make 1 whole pizza. Make groups of 4: %d fourths make <b>%s</b>. "
             "(Not %d: it takes 4 fourths, not 2, to make a whole.)" % (n, wholes(w), n // 2))
        its.append(mcq(fig(pieces_svg(n, 4, label="%d pizza pieces, each one fourth" % n)) +
                       "Each piece is one fourth of a pizza. How many whole pizzas do these %d pieces make?" % n,
                       wholes(w), [wholes(n), wholes(n // 2), wholes(w + 1), wholes(w + 2)], e))

    for n, wrong in [(5, ["5 wholes", "2 and a half", "1 whole"]), (7, ["7 wholes", "3 and a half", "2 wholes"])]:
        e = ("4 fourths make 1 whole. %d fourths is 4 fourths and %d more: <b>%s</b>. "
             "(%s would be right for halves, not fourths.)" % (n, n - 4, amount(fourths=n), wrong[1]))
        its.append(mcq(fig(pieces_svg(n, 4, label="%d pizza pieces, each one fourth" % n)) +
                       "Each piece is one fourth of a pizza. How much pizza is this?", amount(fourths=n), wrong, e))

    for w, cands in [(2, [2, 6, 3]), (4, [4, 6, 10])]:
        e = "Each orange is cut into 2 halves. Count by 2s: %s. That is <b>%d</b> halves." % (count_on(2, w), 2 * w)
        its.append(mcq(fig(cut_svg(w, 2, "%d oranges, each cut into halves" % w)) +
                       "These %d oranges are cut in half. How many halves are there?" % w, 2 * w, cands, e))

    for w, cands in [(2, [2, 4, 6]), (3, [3, 6, 7])]:
        e = "Each pizza is cut into 4 fourths. %s = <b>%d</b> fourths." % (rep(4, w), 4 * w)
        its.append(mcq(fig(cut_svg(w, 4, "%d pizzas, each cut into fourths" % w)) +
                       "These %d pizzas are cut into fourths. How many fourths are there?" % w, 4 * w, cands, e))

    its.append(mcq(fig(pieces_svg(3, 2, True, "3 plates with half a sandwich on each")) +
                   "There is half a sandwich on each plate. How many whole sandwiches is that?",
                   "1 and a half", ["3 wholes", "1 whole", "2 wholes"],
                   "3 groups of one half. 2 halves make 1 whole, and 1 half is left: <b>1 and a half</b> sandwiches."))
    its.append(mcq(fig(pieces_svg(6, 2, True, "6 plates with half a sandwich on each")) +
                   "There is half a sandwich on each plate. How many whole sandwiches is that?",
                   "3 wholes", ["6 wholes", "12 wholes", "2 wholes"],
                   "6 groups of one half. Every 2 halves make 1 whole: 6 halves make <b>3 wholes</b>."))
    its.append(mcq("What do 4 groups of one half make?", "2 wholes", ["4 wholes", "8 wholes", "1 whole"],
                   "One half + one half = 1 whole. Do it twice: 4 halves make <b>2 wholes</b>."))
    its.append(mcq("How many fourths make 2 wholes?", 8, [4, 2, 6],
                   "4 fourths make 1 whole. 2 wholes need 4 + 4 = <b>8</b> fourths. (4 fourths make only 1 whole.)"))
    assert len(its) == 20, len(its)
    return {"title": "Groups of halves and fourths", "items": its}


# ============================================================ set 4: sharing equally (up to 12)
def set_sharing(P):
    its = []
    for t, k, kd, what in [(6, 2, "dot", "plates"), (8, 2, "star", "plates"), (9, 3, "square", "plates"),
                           (12, 3, "dot", "plates"), (10, 5, "star", "bags"), (12, 4, "square", "bags"),
                           (8, 4, "dot", "bags"), (12, 2, "star", "bags")]:
        a = t // k
        e = ("Give out one at a time, round and round, until none are left. Each %s gets <b>%d</b>. "
             "Check: %s = %d." % (what[:-1], a, rep(a, k), t))
        its.append(mcq(fig(counters_svg(t, kd)) + "Share these %d %s equally between %d %s. How many does each %s get?"
                       % (t, WORD[kd], k, what, what[:-1]), a, [k, t - k, a + 1, a - 1, t], e))

    its.append({"q": "", "c": ["A", "B", "C", "D"], "a": 0,
                "e": ("Sharing between 4 plates means 4 plates, all the same. <b>{L}</b> has 4 plates of 3. "
                      "3 plates of 4 is the wrong number of plates. 4, 3, 3 and 2 is not equal. "
                      "4 plates of 2 shares only 8."),
                "_abcd": ("Share 12 counters equally between 4 plates. Which picture shows this?",
                          [3] * 4, [[4, 4, 4], [4, 3, 3, 2], [2, 2, 2, 2]], "dot", "plate")})
    its.append({"q": "", "c": ["A", "B", "C", "D"], "a": 0,
                "e": ("Sharing between 2 plates means 2 plates with the same amount. <b>{L}</b> has 5 and 5. "
                      "6 and 4 is not fair. 5 plates of 2 is the wrong number of plates. 4 and 4 shares only 8."),
                "_abcd": ("Share 10 stars equally between 2 plates. Which picture shows this?",
                          [5, 5], [[6, 4], [2, 2, 2, 2, 2], [4, 4]], "star", "plate")})
    its.append({"q": "", "c": ["A", "B", "C", "D"], "a": 0,
                "e": ("Sharing between 3 plates means 3 plates with the same amount. <b>{L}</b> has 2, 2 and 2. "
                      "2 plates of 3 is the wrong number of plates. 3, 2 and 1 is not equal. 1, 1 and 1 shares only 3."),
                "_abcd": ("Share 6 blocks equally between 3 plates. Which picture shows this?",
                          [2, 2, 2], [[3, 3], [3, 2, 1], [1, 1, 1]], "square", "plate")})

    for sizes, move, wrong in [([6, 4], 1, [2, 4, 5]), ([7, 3], 2, [4, 5, 3]), ([5, 1], 2, [4, 3, 1])]:
        t = sum(sizes)
        h = t // 2
        nm, he, his = P.next()
        e = ("%d shared between 2 is %d each. Move <b>%d</b> from the %d to the %d: %d and %d. "
             "(Moving %d would just swap the two amounts.)"
             % (t, h, move, sizes[0], sizes[1], h, h, sizes[0] - sizes[1]))
        its.append(mcq(fig(groups_svg(sizes, "dot", "plate", "2 plates with %d and %d counters" % tuple(sizes))) +
                       "%s wants %d counters shared equally on 2 plates. How many counters must move?" % (nm, t),
                       move, wrong, e))

    nm, he, his = P.next()
    its.append(mcq(fig(groups_svg([5, 4, 3], "dot", "plate", "3 plates with 5, 4 and 3 counters")) +
                   "%s shared 12 counters on 3 plates. What went wrong?" % nm,
                   "Not equal. Each gets 4.",
                   ["Nothing. It is 12.", "Each should get 3.", "Use 4 plates."],
                   "5 + 4 + 3 = 12, but equal shares must be the same. 4 + 4 + 4 = 12, so <b>each plate should get 4</b>."))
    nm, he, his = P.next()
    its.append(mcq(fig(groups_svg([6, 6], "dot", "plate", "2 plates with 6 and 6 counters")) +
                   "%s had to share 12 counters equally on 3 plates. What went wrong?" % nm,
                   "Use 3 plates of 4.",
                   ["Nothing. It is 12.", "Each should get 6.", "Use 4 plates of 3."],
                   "The shares are equal, but there should be 3 plates, not 2. 4 + 4 + 4 = 12, so <b>use 3 plates of 4</b>."))

    its.append(mcq("Which shows 12 shared equally between 3?", "4, 4 and 4", ["5, 4 and 3", "6 and 6", "3, 3, 3 and 3"],
                   "Between 3 means 3 shares, all the same size. 4 + 4 + 4 = 12, so <b>4, 4 and 4</b>. "
                   "5, 4 and 3 also makes 12, but it is not equal."))
    its.append(mcq("Which shows 10 shared equally between 2?", "5 and 5", ["6 and 4", "7 and 3", "4 and 4"],
                   "Equal shares are the same size. 5 + 5 = 10, so <b>5 and 5</b>. "
                   "6 and 4 also make 10, but they are not equal."))
    its.append(mcq("Counters are shared on 4 plates. Each plate gets 3. How many counters were shared?", 12,
                   [7, 3, 4, 9],
                   "4 plates of 3: 3 + 3 + 3 + 3 = <b>12</b>. (7 comes from 4 + 3.)"))
    its.append(mcq("Stars are shared between 3 bags. Each bag gets 2. How many stars were shared?", 6,
                   [5, 2, 3, 8],
                   "3 bags of 2: 2 + 2 + 2 = <b>6</b>. (5 comes from 3 + 2.)"))
    assert len(its) == 20, len(its)
    return {"title": "Sharing up to 12 equally", "items": its}


# ============================================================ set 5: word problems
def set_story(P):
    its = []

    def add(q, a, w, e, unit="", pic=""):
        if unit == "¢":
            u = lambda x: "%d¢" % x
        elif unit:
            u = lambda x: x if isinstance(x, str) else "%d %s" % (x, unit[:-1] if x == 1 and unit.endswith("s") else unit)
        else:
            u = str
        its.append(mcq((fig(pic) if pic else "") + q, u(a), [u(x) for x in w], e))

    # equal groups
    nm, he, his = P.next()
    add("A pair of mitts is 2 mitts. %s has 4 pairs. How many mitts is that?" % nm, 8, [6, 4, 10],
        "4 groups of 2: 2 + 2 + 2 + 2 = <b>8</b> mitts. (6 comes from 4 + 2.)", "mitts",
        groups_svg([2] * 4, "square", "ring", "4 groups of 2 mitts"))
    add("A canoe holds 2 people. 5 canoes go out on the lake. How many people is that?", 10, [7, 5, 12],
        "5 groups of 2. Count by 2s: 2, 4, 6, 8, 10. That is <b>10</b> people.", "people")
    add("A Canada goose has 2 legs. There are 7 geese on the pond. How many legs is that?", 14, [9, 7, 16],
        "7 groups of 2. Count by 2s: %s. That is <b>14</b> legs." % count_on(2, 7), "legs")
    add("A moose has 4 legs. There are 3 moose in the field. How many legs is that?", 12, [7, 3, 16],
        "3 groups of 4: 4 + 4 + 4 = <b>12</b> legs. (7 comes from 3 + 4.)", "legs",
        groups_svg([4] * 3, "dot", "ring", "3 groups of 4 legs"))
    add("A box holds 5 muffins. There are 4 boxes. How many muffins is that?", 20, [9, 4, 25],
        "4 groups of 5. Count by 5s: 5, 10, 15, 20. That is <b>20</b> muffins.", "muffins",
        groups_svg([5] * 4, "dot", "plate", "4 boxes of 5 muffins"))
    nm, he, his = P.next()
    add("A dime is 10¢. %s has 6 dimes. How much money is that?" % nm, 60, [16, 6, 50], "Count by 10s: "
        "10, 20, 30, 40, 50, 60. 6 dimes is <b>60¢</b>.", "¢")
    nm, he, his = P.next()
    add("A nickel is 5¢. %s has 5 nickels. How much money is that?" % nm, 25, [10, 5, 20],
        "Count by 5s: 5, 10, 15, 20, 25. 5 nickels is <b>25¢</b>.", "¢")
    add("Chairs for the class show are set out in 3 rows of 5. How many chairs is that?", 15, [8, 10, 20],
        "3 rows of 5: 5 + 5 + 5 = <b>15</b> chairs.", "chairs", array_svg(3, 5, "square"))

    # sharing up to 12
    add("In gym class, 12 students make 2 equal soccer teams. How many students are on each team?", 6,
        [10, 2, 14], "12 shared between 2 teams: 6 + 6 = 12. Each team has <b>6</b> students.", "students")
    nm, he, his = P.next()
    add("%s shares 8 stickers equally with a friend. How many stickers does each of them get?" % nm, 4,
        [6, 2, 10], "There are 2 people. 8 shared between 2: 4 + 4 = 8. Each gets <b>4</b> stickers.", "stickers")
    add("Share 12 maple cookies equally among 4 friends. How many cookies does each friend get?", 3, [8, 4, 16],
        "Give out one at a time until none are left. 3 + 3 + 3 + 3 = 12. Each friend gets <b>3</b> cookies.",
        "cookies", counters_svg(12, "dot").replace("12 counters in rows of 10", "12 cookies in rows of 10"))
    add("A teacher shares 10 markers equally between 5 tables. How many markers go on each table?", 2,
        [5, 15, 3], "10 shared between 5: 2 + 2 + 2 + 2 + 2 = 10. Each table gets <b>2</b> markers.", "markers")
    nm, he, his = P.next()
    add("%s has 6 crackers. %s shares them equally with 2 friends. How many crackers does each person get?"
        % (nm, cap(he)), 2, [3, 4, 12],
        "%s and 2 friends are <b>3 people</b>. 6 shared between 3: 2 + 2 + 2 = 6. Each gets <b>2</b> crackers. "
        "(3 each would be for only 2 people.)" % nm, "crackers")

    # halves and fourths
    add("At lunch, 5 children each eat half a sandwich. How many whole sandwiches do they eat?",
        "2 and a half", ["5 sandwiches", "2 sandwiches", "3 sandwiches"],
        "5 halves. 2 halves make 1 whole, so 4 halves make 2 wholes. 1 half is left: <b>2 and a half</b> sandwiches.",
        "sandwiches", pieces_svg(5, 2, True, "5 plates with half a sandwich on each"))
    add("A pizza is cut into fourths. 8 children each get one fourth. How many pizzas is that?",
        2, [8, 4, 1], "4 fourths make 1 pizza. 8 fourths make 4 + 4, so <b>2</b> pizzas. "
        "(4 pizzas would mean 2 fourths make a whole.)", "pizzas")
    nm, he, his = P.next()
    add("%s eats half an apple each day for 6 days. How many whole apples is that?" % nm, 3, [6, 12, 2],
        "6 halves. Every 2 halves make 1 whole: 6 halves make <b>3</b> apples.", "apples")
    add("A pancake recipe uses half a cup of milk. Ava makes it 4 times. How many cups of milk does she use?",
        2, [4, 8, 1], "4 groups of one half. 2 halves make 1 cup, so 4 halves make <b>2</b> cups.", "cups")

    # two steps and reasoning
    nm, he, his = P.next()
    add("%s has 2 bags of 5 marbles. %s gives away 3 marbles. How many marbles are left?" % (nm, cap(he)), 7,
        [10, 13, 4], "Step 1: 5 + 5 = 10 marbles. Step 2: 10 − 3 = <b>7</b> marbles. (4 comes from 2 + 5 − 3.)",
        "marbles")
    nm, he, his = P.next()
    its.append(mcq("%s says, “3 bags of 4 apples is 7 apples.” What went wrong?" % nm,
                   "%s added 3 + 4. It is 12." % cap(he),
                   ["Nothing. 7 is right.", "%s should take away." % cap(he), "%s counted the bags." % cap(he)],
                   "3 + 4 = 7 adds the bags to one bag. 3 bags of 4 is 4 + 4 + 4. "
                   "<b>%s added 3 + 4. It is 12.</b>" % cap(he)))
    nm, he, his = P.next()
    add("%s has 3 bags with 4 granola bars in each. %s shares all the bars equally with a friend. "
        "How many bars does each of them get?" % (nm, cap(he)), 6, [7, 12, 4, 3],
        "Step 1: 4 + 4 + 4 = 12 bars. Step 2: 12 shared between 2 people is 6 + 6. Each gets <b>6</b> bars.", "bars")
    assert len(its) == 20, len(its)
    return {"title": "Equal groups and sharing word problems", "items": its}


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
        "<p>Look for <b>equal groups</b>. Count the groups. Count how many are in one group. "
        "Then add the same number again and again. This is <b>repeated addition</b>.</p>"
        "<figure class='sn-fig'>" + groups_svg([4, 4, 4], "dot", "ring", "3 groups of 4 counters") +
        "<figcaption>3 groups of 4: 4 + 4 + 4 = 12.</figcaption></figure>"
        + ex("Example", "There are 5 bags. Each bag has 2 apples. How many apples?",
             "5 groups of 2. Count by 2s: 2, 4, 6, 8, 10.", "10 apples")
        + "<h2>Arrays</h2>"
        "<p>An <b>array</b> is objects in rows and columns. <b>Rows</b> go across. <b>Columns</b> go up and down. "
        "Add the rows or add the columns. You get the same total.</p>"
        "<figure class='sn-fig'>" + lesson_array_svg(2, 5) +
        "<figcaption>2 rows of 5: 5 + 5 = 10. 5 columns of 2: 2 + 2 + 2 + 2 + 2 = 10.</figcaption></figure>"
        "<h2>Groups of halves and fourths</h2>"
        "<p>You can make groups of parts, too. <b>2 halves make 1 whole.</b> <b>4 fourths make 1 whole.</b> "
        "Put the parts together to find how many wholes.</p>"
        "<figure class='sn-fig'>" + lesson_halves_svg() +
        "<figcaption>4 groups of one half make 2 wholes.</figcaption></figure>"
        + ex("Example", "3 children each eat half an orange. How many oranges do they eat?",
             "3 halves. 2 halves make 1 whole, and 1 half is left over.", "1 and a half oranges")
        + "<h2>Sharing equally</h2>"
        "<p>To <b>share equally</b>, give out one at a time, round and round, until none are left. "
        "Every share must be the same.</p>"
        "<figure class='sn-fig'>" + groups_svg([4, 4, 4], "dot", "plate", "12 counters shared on 3 plates") +
        "<figcaption>12 counters shared on 3 plates: 4 on each plate. Check: 4 + 4 + 4 = 12.</figcaption></figure>"
        + ex("Example", "Share 8 crackers equally between 2 friends.",
             "Give 1 to each friend, again and again. Each friend gets 4. Check: 4 + 4 = 8.", "4 crackers each")
        + "<h2>Common mistakes</h2>"
        + table(["Mistake", "What to do instead"], [
            ["Counting the groups, not the objects: 3 groups of 4 = 3", "Count everything inside the rings: 4 + 4 + 4 = 12"],
            ["Adding the two numbers: 3 groups of 4 = 7", "Add 4 once for each group: 4 + 4 + 4 = 12"],
            ["Unequal sharing: 12 shared as 5, 4 and 3", "Every share must be the same: 4, 4 and 4"],
            ["Counting halves as wholes: 6 halves = 6 oranges", "Put 2 halves together for each whole: 3 oranges"],
        ])
    )


FAQ = [
    {"q": "What multiplication do Grade 2 students learn in Ontario?",
     "a": "Grade 2 students show multiplication as repeated equal groups, such as 3 groups of 4 = 4 + 4 + 4 = 12, using objects, arrays and drawings. They also make groups of one half and one fourth, like 4 halves make 2 wholes."},
    {"q": "Do Grade 2 students learn division in Ontario?",
     "a": "Yes. Grade 2 students show division as sharing up to 12 items equally, using objects and drawings. The × and ÷ signs and the multiplication facts come in Grade 3."},
    {"q": "How do arrays help Grade 2 students with equal groups?",
     "a": "An array puts equal groups in neat rows, so students can count by 2s, 5s or 10s instead of counting one by one. Adding the rows or the columns gives the same total."},
    {"q": "How can I help my child understand sharing equally?",
     "a": "Use real things like crackers or blocks. Have your child give out one at a time to each plate until none are left, then check that every plate has the same number."},
]


def gen():
    rnd = random.Random(42806)
    P = People(rnd)
    sets = [set_groups(P), set_arrays(P), set_parts(P), set_sharing(P), set_story(P)]
    balance(sets, rnd)
    keys = set()
    for s in sets:
        assert len(s["items"]) == 20, (s["title"], len(s["items"]))
        assert sorted(it["a"] for it in s["items"]) == sorted([0, 1, 2, 3] * 5), s["title"]
        for it in s["items"]:
            assert len(set(it["c"])) == 4, it
            assert it["q"].count("<svg") <= 1, it["q"]
            assert "{" not in it["e"] and "_abcd" not in it
            assert "×" not in it["q"] + "".join(it["c"]) and "÷" not in it["q"] + "".join(it["c"])
            k = it["q"] + "|" + "|".join(sorted(it["c"]))
            assert k not in keys, it["q"]
            keys.add(k)
            m = re.search(r"aria-label='array of (\d+) rows and (\d+) columns", it["q"])
            if m:
                assert n_objects(it["q"]) == int(m.group(1)) * int(m.group(2)), it["q"]
            m = re.search(r"aria-label='(\d+) (orange halves|pizza pieces)", it["q"])
            if m:
                assert n_pieces(it["q"]) == int(m.group(1)), it["q"]
            for x in it["c"]:
                for n in re.findall(r"\d+", x):
                    assert int(n) <= 100, x
    u = {
        "country": "ca-on", "subject": "math", "grade": "grade-2", "slug": "equal-groups-and-sharing",
        "sort": 6, "updated": UPDATED, "pdf_url": "",
        "title": "Equal Groups and Sharing",
        "seo_title": "Grade 2 Equal Groups and Sharing Worksheets: Repeated Addition, Arrays, Halves (Free, Ontario)",
        "short_title": "Equal groups and sharing",
        "domain": "Number",
        "standard_code": "Grade 2: B2.5",
        "standard_url": "https://www.dcp.edu.gov.on.ca/en/curriculum/elementary-mathematics",
        "standard_text": "Represent multiplication as repeated equal groups, including groups of one half and one fourth, and solve related problems, using various tools and drawings",
        "meta_desc": "Free Grade 2 math worksheets on equal groups and sharing for the Ontario curriculum: repeated addition, arrays, groups of halves and fourths, sharing up to 12 equally and word problems. 100 questions with pictures and an answer key.",
        "key_big": "Equal groups are added again and again. Equal shares are all the same size.",
        "key_sub": "3 groups of 4 = 4 + 4 + 4 = 12. 4 halves make 2 wholes. 12 shared equally on 3 plates is 4 on each plate.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }
    return mark_large(u, "(four pictures|\\d+ (groups|plates|boxes) of|\\d+ \\w+ in rows of 10|"
                         "array of \\d+ rows and 10 |\\d+ (orange halves|pizza pieces)|\\d+ plates with half|"
                         "\\d+ (oranges|pizzas), each)")


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
