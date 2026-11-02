# -*- coding: utf-8 -*-
"""
Singapore Primary 2 Maths: Multiplication and Division (MOE 2021 Primary Mathematics Syllabus, Standard,
Number and Algebra, Whole Numbers: "Use of ÷; relationship between multiplication and division;
multiplying and dividing within the multiplication tables")
  python3 tools/gen_sg_maths_p2_mult_div.py
Sharing equally (pictures), grouping, the ÷ sign and fact families, missing numbers, and word problems
with bar models. Multiplication tables of 2, 3, 4, 5 and 10 only.
Wrong answers come from real mistakes: taking away instead of sharing (12 ÷ 3 = 9), dividing the wrong way
(3 ÷ 12), giving the number of groups instead of the number in each group, adding instead of multiplying,
and counting one group too many or too few.
Helpers adapted from gen_uk_maths_y2_mult_div.py (pictures) and gen_sg_maths_p3_mult_div.py (bar models).
Singapore English. Every drawn picture is counted in code and every answer is computed in code.
HTML attributes use single quotes (no backslashes in the JSON).
"""
import json, math, os, random, re
from fractions import Fraction

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "sg", "maths", "primary-2")
UPDATED = "2026-11-03"
GREEN = "#006633"
FILL = "#cfe6d6"
FILL2 = "#eef6f0"
RED = "#c0392b"
ORANGE = "#d9822b"
BLUE = "#2e6da4"
GREY = "#9a9a9a"
INK = "#2b2b2b"
FONT = "Arial, Helvetica, sans-serif"
GIRLS = ["Siti", "Nurul", "Farah", "Mei Ling", "Hui Min", "Xin Yi", "Priya", "Devi", "Kavya", "Chloe", "Sarah"]
BOYS = ["Ali", "Ahmad", "Hafiz", "Wei Ming", "Jun Jie", "Zhi Hao", "Raju", "Kumar", "Arjun", "Ethan", "Ryan"]
WORD = {"dot": "counters", "star": "stars", "square": "cubes"}
COL = {"dot": GREEN, "star": ORANGE, "square": BLUE}
TABLES = (2, 3, 4, 5, 10)


# ------------------------------------------------------------ helpers
def mcq(q, correct, cands, e):
    """4 choices: correct + the first 3 unique distractors (no 0 or negatives). Positions are set by balance()."""
    correct = str(correct)
    seen = {correct}
    pick = []
    for c in cands:
        c = str(c)
        if c in seen or not c or re.match(r"^\$?[-−]\d", c) or re.match(r"^\$?0(¢)?( |$)", c):
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


def among(k):
    return "between" if k == 2 else "among"


def fig(svg):
    return "<div class='qfig'>" + svg + "</div>"


def svg_wrap(w, h, body, label):
    w, h = int(round(w + 0.49)), int(round(h + 0.49))
    return ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 %d %d' width='%d' height='%d' "
            "role='img' aria-label='%s'><g font-family='%s'>%s</g></svg>" % (w, h, w, h, label, FONT, body))


def T(x, y, t, fs=16, col=INK, anchor="middle"):
    return ("<text x='%.1f' y='%.1f' font-size='%d' font-weight='700' fill='%s' text-anchor='%s'>%s</text>"
            % (x, y, fs, col, anchor, t))


def tw(s, size=15):
    return len(s) * size * 0.58


def table(head, rows):
    h = "".join("<th>%s</th>" % x for x in head)
    b = "".join("<tr>" + "".join("<td>%s</td>" % c for c in r) + "</tr>" for r in rows)
    return "<div class='sn-tw'><table class='sn-table'><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>" % (h, b)


def ex(title, q, s, a):
    return ("<div class='sn-ex'><span class='sn-ex-t'>%s</span><p class='sn-ex-q'>%s</p>"
            "<p class='sn-ex-s'>%s</p><p class='sn-ex-a'>Answer: %s</p></div>" % (title, q, s, a))


def count_on(n, times):
    return ", ".join(str(n * (i + 1)) for i in range(times))


def in_tables(a, b):
    """a × b is inside the P2 tables (2, 3, 4, 5, 10) and at most 10 × 10."""
    return (a in TABLES or b in TABLES) and 1 <= a <= 10 and 1 <= b <= 10


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
    """How many objects (counters, stars, cubes) a picture draws."""
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
    svg = svg_wrap(w + 2 * M, h + 2 * M, body, label or (
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
        assert len(p) <= 6 and max(p) <= 10
        built.append(groups_body(p, 0, 0, kind, style, S, r, {4: 2, 5: 3, 6: 3}.get(len(p), len(p)), G))
    PW = max(b[1] for b in built) + 2 * PAD
    H = 30 + max(b[2] for b in built) + 8
    el = []
    for k, (body, w, h) in enumerate(built):
        x0 = k * PW
        if k:
            el.append("<line x1='%.1f' y1='4' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='1'/>" % (x0, x0, H - 4, GREY))
        el.append(T(x0 + 8, 20, "ABCD"[k], 18, INK, "start"))
        el.append("<g transform='translate(%.1f,30)'>%s</g>" % (x0 + (PW - w) / 2.0, body))
    svg = svg_wrap(4 * PW, H, "".join(el), "four pictures labelled A to D")
    assert n_objects(svg) == sum(sum(p) for p in panels)
    return svg


def jumps_svg(step, total):
    """Number line from 0 to total with equal jumps of `step` drawn above it."""
    assert total % step == 0
    s = min(18.0, 340.0 / total)
    x0, y = 14, 62
    el = ["<line x1='%.1f' y1='%d' x2='%.1f' y2='%d' stroke='%s' stroke-width='2'/>" % (x0 - 6, y, x0 + total * s + 6, y, INK)]
    for i in range(total + 1):
        big = i % step == 0
        el.append("<line x1='%.1f' y1='%d' x2='%.1f' y2='%d' stroke='%s' stroke-width='%s'/>"
                  % (x0 + i * s, y - (7 if big else 4), x0 + i * s, y + (7 if big else 4), INK, "2" if big else "1"))
        if big:
            el.append(T(x0 + i * s, y + 24, str(i), 14))
    n = total // step
    for k in range(n):
        a, b = x0 + k * step * s, x0 + (k + 1) * step * s
        h = min(34.0, (b - a) * 0.9)
        el.append("<path d='M%.1f %d Q%.1f %.1f %.1f %d' fill='none' stroke='%s' stroke-width='2.2'/>"
                  % (a, y - 3, (a + b) / 2, y - 3 - 2 * h, b, y - 3, RED))
    svg = svg_wrap(x0 + total * s + 14, y + 30, "".join(el), "number line from 0 to %d with jumps of %d" % (total, step))
    assert svg.count("<path") == n
    return svg


SEGFILL = {"u": FILL, "o": "#e3e3e3", "w": "#ffffff"}


def model_svg(rows, top=None, under=(), right=None, BW=320, label="bar model"):
    """Bar model drawn to scale.
    rows: [(name, [(value, text, style)])]; top: (v0, v1, text) bracket over row 0;
    under: [(row, v0, v1, text)] brackets under a row. Text '?' is drawn in red."""
    names = [n for n, _ in rows]
    nw = max([tw(n, 15) for n in names] + [0])
    x0 = 8 + (nw + 10 if nw else 0)
    maxv = max(sum(v for v, _, _ in segs) for _, segs in rows)
    sc = BW / float(maxv)
    bh = 34
    out = []
    y = 38 if top else 8
    ys = []
    for i, (n, segs) in enumerate(rows):
        ys.append(y)
        y += bh + (38 if any(u[0] == i for u in under) else 16)
    Hh = y - 16 + 8 if not any(u[0] == len(rows) - 1 for u in under) else y - 38 + 44

    def col(t):
        return RED if t == "?" else INK

    for i, (n, segs) in enumerate(rows):
        ry = ys[i]
        if n:
            out.append(T(8, ry + 23, n, 15, INK, "start"))
        x = x0
        for v, t, st in segs:
            w = v * sc
            out.append("<rect x='%.1f' y='%d' width='%.1f' height='%d' fill='%s' stroke='%s' stroke-width='2'/>"
                       % (x, ry, w, bh, SEGFILL[st], GREEN))
            if t:
                assert tw(t, 15) + 4 <= w, (t, w)
                out.append(T(x + w / 2, ry + 23, t, 15, col(t)))
            x += w
    if top:
        v0, v1, t = top
        a, b = x0 + v0 * sc, x0 + v1 * sc
        ry = ys[0]
        out.append("<path d='M%.1f %d V%d H%.1f V%d' fill='none' stroke='%s' stroke-width='2'/>" % (a, ry - 4, ry - 11, b, ry - 4, INK))
        out.append(T((a + b) / 2, ry - 16, t, 16, col(t)))
    for r, v0, v1, t in under:
        a, b = x0 + v0 * sc, x0 + v1 * sc
        yb = ys[r] + bh
        out.append("<path d='M%.1f %d V%d H%.1f V%d' fill='none' stroke='%s' stroke-width='2'/>" % (a, yb + 4, yb + 11, b, yb + 4, RED if t == "?" else INK))
        out.append(T((a + b) / 2, yb + 30, t, 16, col(t)))
    W = x0 + BW + 8
    return svg_wrap(W, Hh, "".join(out), label)


def share_model(total, d):
    """Total shared into d equal units; '?' under one unit."""
    return model_svg([("", [(1, "", "u")] * d)], top=(0, d, total), under=[(0, 0, 1, "?")],
                     label="bar model: %s shared into %d equal units" % (total, d))


def groups_model(each, k):
    """k equal units of `each`; '?' for the total over the top."""
    return model_svg([("", [(1, each, "u")] * k)], top=(0, k, "?"),
                     label="bar model: %d units of %s" % (k, each))


def lesson_array_svg(rows, cols):
    """Array with each row counted on the right and each column counted below."""
    S, R, x0, y0 = 36, 11, 12, 12
    el = ["".join(shape("dot", x0 + c * S + S / 2.0, y0 + i * S + S / 2.0, R) for i in range(rows) for c in range(cols))]
    for i in range(rows):
        el.append(T(x0 + cols * S + 22, y0 + i * S + S / 2 + 6, str(cols), 17, RED))
    for c in range(cols):
        el.append(T(x0 + c * S + S / 2, y0 + rows * S + 22, str(rows), 17, BLUE))
    return svg_wrap(x0 + cols * S + 40, y0 + rows * S + 32, "".join(el),
                    "array of %d rows of %d, with each row and column counted" % (rows, cols))


# ------------------------------------------------------------ checking number sentences
def ev(s):
    s = s.replace("×", "*").replace("÷", "/").replace("−", "-")
    assert re.match(r"^[\d\s*/+\-()]+$", s), s
    return Fraction(eval(re.sub(r"(\d+)", r"Fraction(\1)", s)))


def true_fact(s):
    """'12 ÷ 3 = 4' -> True. Every side must be a whole-number expression."""
    s = re.sub(r"<[^>]+>", "", s)
    parts = [p.strip() for p in s.split("=")]
    vals = [ev(p) for p in parts]
    return all(v == vals[0] for v in vals)


# ============================================================ set 1: sharing equally (pictures)
def set_sharing(P):
    its = []
    # share objects that are not shared yet
    for t, k, kd in [(10, 2, "dot"), (12, 3, "star"), (15, 5, "square"), (20, 4, "dot"), (14, 2, "star"), (18, 3, "square")]:
        a = t // k
        assert a * k == t and in_tables(a, k) and a != k
        e = ("Give out one at a time, round and round, until none are left. Each plate gets <b>%d</b>. "
             "%d ÷ %d = %d. Check: %d × %d = %d." % (a, t, k, a, k, a, t))
        if t - k not in (a,):
            e += " (%d − %d = %d takes away instead of sharing.)" % (t, k, t - k)
        its.append(mcq(fig(counters_svg(t, kd)) + "Share these %d %s equally %s %d plates. How many %s go on each plate?"
                       % (t, WORD[kd], among(k), k, WORD[kd]), a, [t - k, k, a + 1, a - 1, t + k], e))

    # pictures after sharing: which division?
    for t, k in [(12, 3), (10, 5), (20, 4), (18, 2)]:
        a = t // k
        right = "%d ÷ %d = %d" % (t, k, a)
        wrong = ["%d ÷ %d = %d" % (k, t, a), "%d ÷ %d = %d" % (t, k, t - k), "%d ÷ %d = %d" % (t, k, k),
                 "%d ÷ %d = %d" % (t, k, a + 1)]
        assert true_fact(right) and not any(true_fact(w) for w in wrong)
        e = ("%d counters are shared equally %s %d plates. Each plate has %d. That is <b>%s</b>. "
             "Start with the whole amount, %d." % (t, among(k), k, a, right, t))
        its.append(mcq(fig(groups_svg([a] * k, "dot", "plate")) +
                       "%d counters are shared equally %s %d plates. Which division does the picture show?"
                       % (t, among(k), k), right, wrong, e))

    # use the picture to find the value
    for t, k, kd in [(15, 3, "star"), (8, 2, "square"), (30, 5, "dot")]:
        a = t // k
        e = "Look at one plate. It has %d. So %d ÷ %d = <b>%d</b>. (%d is the number of plates, not the number on each plate.)" % (a, t, k, a, k)
        its.append(mcq(fig(groups_svg([a] * k, kd, "plate")) + "%d %s are shared equally. Find the value of %d ÷ %d."
                       % (t, WORD[kd], t, k), a, [k, t - k, a + 1, t + k], e))

    # how many were shared altogether
    for k, a in [(3, 5), (4, 2)]:
        t = a * k
        e = ("There are %d plates with %d on each. %s. So <b>%d</b> counters were shared. (%d + %d = %d adds the plates to one plate.)"
             % (k, a, " + ".join([str(a)] * k) + " = %d" % t, t, k, a, k + a))
        its.append(mcq(fig(groups_svg([a] * k, "dot", "plate")) + "Some counters were shared equally. How many counters were there altogether?",
                       t, [k + a, a, t + a, t - a], e))

    # move to make it equal
    nm, he, his = P.next()
    its.append(mcq(fig(groups_svg([6, 4], "dot", "plate", "2 plates with 6 and 4 counters")) +
                   "%s wants to share 10 counters equally between 2 plates. How many counters must %s move?" % (nm, he),
                   1, [2, 4, 5],
                   "10 ÷ 2 = 5, so each plate needs 5. Move <b>1</b> counter from the 6 to the 4: 5 and 5. "
                   "(Moving 2 would make 4 and 6.)"))

    # A-D pictures
    for t, k, wrong, kd in [(12, 3, [[3, 3, 3, 3], [5, 4, 3], [6, 6]], "dot"),
                            (10, 2, [[2, 2, 2, 2, 2], [6, 4], [4, 4]], "star"),
                            (20, 5, [[5, 5, 5, 5], [4, 4, 4, 4], [5, 4, 4, 4, 3]], "square")]:
        a = t // k
        assert [a] * k not in wrong and len({tuple(w) for w in wrong}) == 3
        e = ("Sharing equally %s %d plates means <b>%d</b> plates with the same number on each. <b>{L}</b> has %d plates of %d. "
             "Check: %d × %d = %d." % (among(k), k, k, k, a, k, a, t))
        its.append({"q": "", "c": ["A", "B", "C", "D"], "a": 0, "e": e,
                    "_abcd": ("Which picture shows %d %s shared equally %s %d plates?" % (t, WORD[kd], among(k), k),
                              [a] * k, wrong, kd, "plate")})

    # the 12 ÷ 3 = 9 mistake
    nm, he, his = P.next()
    its.append(mcq("%s says, “12 sweets shared equally among 3 friends is 9 each.” What went wrong?" % nm,
                   "%s took away 3. It is 4." % cap(he),
                   ["Nothing. 9 is right.", "%s added 3. It is 15." % cap(he), "%s should multiply. It is 36." % cap(he)],
                   "12 − 3 = 9 takes away. Sharing is dividing: 12 ÷ 3 = 4, because 3 × 4 = 12. "
                   "<b>%s took away 3. It is 4.</b>" % cap(he)))
    assert len(its) == 20, len(its)
    return {"title": "Sharing equally", "items": its}


# ============================================================ set 2: grouping
def set_grouping(P):
    its = []
    for t, k, kd in [(15, 5, "star"), (8, 2, "dot"), (30, 10, "square"), (12, 4, "dot")]:
        g = t // k
        e = ("Count the rings: %d groups. %d in groups of %d makes <b>%d</b> groups, so %d ÷ %d = %d."
             % (g, t, k, g, t, k, g))
        its.append(mcq(fig(groups_svg([k] * g, kd)) + "%d %s are put into groups of %d. How many groups are there?"
                       % (t, WORD[kd], k), g, [k, t - k, t, g + 1], e))

    # groups vs number in each group
    for g, n, ask, kd in [(5, 2, "groups", "star"), (3, 4, "each", "square"), (2, 5, "groups", "dot"), (4, 3, "each", "star")]:
        if ask == "groups":
            e = "Count the rings: there are <b>%d</b> groups. %d is how many %s are in each group." % (g, n, WORD[kd])
            its.append(mcq(fig(groups_svg([n] * g, kd)) + "How many groups are there?", g, [n, g * n, g + 1, g - 1], e))
        else:
            e = "Look inside one ring. It has <b>%d</b> %s. %d is the number of groups." % (n, WORD[kd], g)
            its.append(mcq(fig(groups_svg([n] * g, kd)) + "How many %s are in each group?" % WORD[kd], n,
                           [g, g * n, n + 1, n - 1], e))

    # number line jumps
    for step, total in [(4, 20), (3, 18), (2, 16)]:
        n = total // step
        e = ("Count the jumps: %s. There are <b>%d</b> jumps of %d. So %d ÷ %d = %d."
             % (count_on(step, n), n, step, total, step, n))
        its.append(mcq(fig(jumps_svg(step, total)) + "How many jumps of %d are there from 0 to %d?" % (step, total),
                       n, [step, total, n + 1, total - step], e))

    # grouping without a picture
    for t, k in [(20, 2), (35, 5), (24, 3)]:
        g = t // k
        e = "Count in %ds until you reach %d: %s. That is <b>%d</b> groups. %d ÷ %d = %d." % (
            k, t, count_on(k, g), g, t, k, g)
        its.append(mcq("There are %d counters. Put them in groups of %d. How many groups are there?" % (t, k), g,
                       [k, t - k, g + 1, g - 1], e))

    # A-D pictures
    for t, k, wrong, kd in [(12, 3, [[4, 4, 4], [3, 3, 3], [2, 2, 2, 2, 2, 2]], "dot"),
                            (10, 2, [[5, 5], [2, 2, 2, 2], [3, 3, 3]], "star"),
                            (20, 5, [[4, 4, 4, 4, 4], [5, 5, 5], [10, 10]], "square")]:
        g = t // k
        assert [k] * g not in wrong and len({tuple(w) for w in wrong}) == 3
        e = ("Groups of %d means %d in every group. %d in groups of %d makes %d groups. <b>{L}</b> shows this. "
             "(%d groups of %d is sharing %s %d, not groups of %d.)" % (k, k, t, k, g, k, g, among(k), k, k))
        its.append({"q": "", "c": ["A", "B", "C", "D"], "a": 0, "e": e,
                    "_abcd": ("Which picture shows %d %s put into groups of %d?" % (t, WORD[kd], k),
                              [k] * g, wrong, kd, "ring")})

    its.append(mcq("Which one is grouping?", "Put 10 eggs in trays of 2.",
                   ["Share 10 eggs between 2 trays.", "Add 2 eggs to 10 eggs.", "Take 2 eggs away from 10."],
                   "Grouping means you know how many go in each group. “Trays of 2” tells you 2 in each tray: "
                   "<b>Put 10 eggs in trays of 2.</b> That makes 5 trays."))
    its.append(mcq("Which one is sharing?", "Share 12 buns among 4 plates.",
                   ["Put 12 buns in bags of 4.", "Add 4 buns to 12 buns.", "Take 4 buns away from 12."],
                   "Sharing means you know how many groups there are. “Among 4 plates” tells you there are 4 plates: "
                   "<b>Share 12 buns among 4 plates.</b> Each plate gets 3."))
    nm, he, his = P.next()
    its.append(mcq("%s shares 15 cubes equally among 5 friends. %s puts 15 cubes into groups of 5. "
                   "What number do they both get?" % (nm, cap(his) + " brother"), 3, [5, 10, 20],
                   "Sharing: 15 shared among 5 is 3 each. Grouping: 15 in groups of 5 makes 3 groups. "
                   "Both are 15 ÷ 5 = <b>3</b>."))
    assert len(its) == 20, len(its)
    return {"title": "Grouping", "items": its}


# ============================================================ set 3: the ÷ sign and fact families
def set_facts(P):
    its = []
    for a, b, t, s in [(3, 4, 12, "×"), (20, 4, 5, "÷"), (15, 3, 12, "−"), (18, 2, 9, "÷")]:
        assert true_fact("%d %s %d = %d" % (a, s, b, t))
        for o in "×÷+−":
            if o != s and (o != "÷" or a % b == 0):
                assert not true_fact("%d %s %d = %d" % (a, o, b, t))
        e = "Try each sign. %d %s %d = %d, so the sign is <b>%s</b>." % (a, s, b, t, s)
        if s == "÷":
            e += " %d shared equally into %d groups is %d." % (a, b, t)
        its.append(mcq("Which sign goes in the box? %d □ %d = %d" % (a, b, t), s, ["×", "÷", "+", "−"], e))

    # arrays: which division fact?
    for r, c, kd in [(2, 5, "dot"), (3, 4, "star"), (4, 10, "square"), (5, 3, "dot")]:
        t = r * c
        right = "%d ÷ %d = %d" % (t, c, r)
        wrong = ["%d ÷ %d = %d" % (c, t, r), "%d ÷ %d = %d" % (t, c, r + 1), "%d ÷ %d = %d" % (t, c, t - c)]
        assert true_fact(right) and not any(true_fact(w) for w in wrong)
        e = ("%d rows of %d make %d: %d × %d = %d. Put %d into rows of %d and you get %d rows: <b>%s</b>. "
             "A division starts with the whole amount." % (r, c, t, r, c, t, t, c, r, right))
        its.append(mcq(fig(array_svg(r, c, kd)) + "This array shows %d × %d = %d. Which division fact does it also show?"
                       % (r, c, t), right, wrong, e))

    # not in the family
    for a, b in [(3, 4), (5, 2)]:
        t = a * b
        right = "%d ÷ %d = %d" % (a, t, b)
        others = ["%d × %d = %d" % (a, b, t), "%d ÷ %d = %d" % (t, b, a), "%d × %d = %d" % (b, a, t)]
        assert not true_fact(right) and all(true_fact(o) for o in others)
        e = ("The fact family of %d, %d and %d is %d × %d = %d, %d × %d = %d, %d ÷ %d = %d and %d ÷ %d = %d. "
             "<b>%s</b> divides the wrong way: the biggest number, %d, comes first."
             % (a, b, t, a, b, t, b, a, t, t, a, b, t, b, a, right, t))
        its.append(mcq("Which fact is <b>not</b> in the fact family of %d, %d and %d?" % (a, b, t), right, others, e))

    # finish the family
    for a, b in [(2, 10), (4, 5)]:
        t = a * b
        right = "%d ÷ %d = %d" % (t, b, a)
        wrong = ["%d ÷ %d = %d" % (b, t, a), "%d − %d = %d" % (t, b, a), "%d × %d = %d" % (t, b, a)]
        assert true_fact(right) and not any(true_fact(w) for w in wrong)
        e = ("Each fact uses %d, %d and %d. The family has two × facts and two ÷ facts. "
             "The missing one is <b>%s</b>." % (a, b, t, right))
        its.append(mcq("%d × %d = %d, %d × %d = %d, %d ÷ %d = %d. Which fact completes the family?"
                       % (a, b, t, b, a, t, t, a, b), right, wrong, e))

    # use × to divide
    for a, b in [(5, 4), (3, 6), (4, 7), (10, 8)]:
        t = a * b
        assert in_tables(a, b)
        e = ("%d × %d = %d, so %d groups of %d make %d. That means %d ÷ %d = <b>%d</b>." % (a, b, t, a, b, t, t, a, b))
        its.append(mcq("%d × %d = %d. Find the value of %d ÷ %d." % (a, b, t, t, a), b, [t - a, a, b + 1, t + a], e))

    its.append(mcq("Which pair gives the same answer?", "4 × 5 and 5 × 4",
                   ["20 ÷ 4 and 4 ÷ 20", "10 ÷ 2 and 2 ÷ 10", "5 − 4 and 4 − 5"],
                   "4 × 5 = 20 and 5 × 4 = 20. You can swap the numbers in <b>multiplication</b>. "
                   "You cannot swap them in division: 10 ÷ 2 = 5, but 2 ÷ 10 is not 5."))
    its.append(mcq("What does 12 ÷ 4 mean?", "12 shared equally into 4 groups",
                   ["4 shared equally into 12 groups", "12 take away 4", "4 groups of 12"],
                   "Read ÷ as “shared equally into” or “divided by”. 12 ÷ 4 means <b>12 shared equally into 4 groups</b>. "
                   "Each group gets 3."))
    its.append(mcq("Which number sentence shows 15 shared equally among 5?", "15 ÷ 5 = 3",
                   ["5 ÷ 15 = 3", "15 − 5 = 10", "15 × 5 = 75"],
                   "Sharing equally is division. Start with the amount you share: <b>15 ÷ 5 = 3</b>. Each gets 3."))
    its.append(mcq("Which can you swap round and still get the same answer?", "2 × 10",
                   ["10 ÷ 2", "20 ÷ 10", "10 − 2"],
                   "2 × 10 = 10 × 2 = 20, so you can swap <b>2 × 10</b>. 10 ÷ 2 = 5, but 2 ÷ 10 is not 5. "
                   "Division and subtraction cannot be swapped."))
    assert len(its) == 20, len(its)
    return {"title": "The ÷ sign and fact families", "items": its}


# ============================================================ set 4: missing numbers
def set_missing(P):
    its = []
    # (sentence with ?, answer, distractors, explanation)
    rows = [
        ("<b>?</b> × 5 = 15", 3, [10, 20, 5],
         "Count in 5s to 15: 5, 10, 15. That is 3 fives, so <b>3</b> × 5 = 15."),
        ("2 × <b>?</b> = 14", 7, [12, 16, 28],
         "Count in 2s to 14: 2, 4, 6, 8, 10, 12, 14. That is 7 twos, so 2 × <b>7</b> = 14."),
        ("<b>?</b> × 10 = 60", 6, [50, 70, 600],
         "Count in 10s to 60: 10, 20, 30, 40, 50, 60. That is 6 tens, so <b>6</b> × 10 = 60."),
        ("4 × <b>?</b> = 32", 8, [28, 36, 7],
         "Count in 4s to 32: 4, 8, 12, 16, 20, 24, 28, 32. That is 8 fours, so 4 × <b>8</b> = 32."),
        ("3 × <b>?</b> = 27", 9, [24, 30, 8],
         "Count in 3s to 27: 3, 6, 9, 12, 15, 18, 21, 24, 27. That is 9 threes, so 3 × <b>9</b> = 27."),
        ("16 ÷ <b>?</b> = 4", 4, [12, 20, 64],
         "Think: 4 × ? = 16. 4 × 4 = 16, so 16 ÷ <b>4</b> = 4."),
        ("25 ÷ <b>?</b> = 5", 5, [20, 30, 125],
         "Think: 5 × ? = 25. 5 × 5 = 25, so 25 ÷ <b>5</b> = 5."),
        ("30 ÷ <b>?</b> = 10", 3, [20, 40, 300],
         "Think: 10 × ? = 30. 10 × 3 = 30, so 30 ÷ <b>3</b> = 10. (20 is 30 − 10, a take-away mistake.)"),
        ("<b>?</b> ÷ 2 = 6", 12, [3, 4, 8],
         "Use the related fact: 6 × 2 = 12. So <b>12</b> ÷ 2 = 6. (3 is 6 ÷ 2, the wrong way round.)"),
        ("<b>?</b> ÷ 5 = 8", 40, [13, 3, 35],
         "Use the related fact: 8 × 5 = 40. So <b>40</b> ÷ 5 = 8. (13 is 8 + 5, an adding mistake.)"),
        ("<b>?</b> ÷ 4 = 3", 12, [7, 16, 8],
         "Use the related fact: 3 × 4 = 12. So <b>12</b> ÷ 4 = 3. (7 is 3 + 4, an adding mistake.)"),
        ("<b>?</b> ÷ 10 = 9", 90, [19, 80, 100],
         "Use the related fact: 9 × 10 = 90. So <b>90</b> ÷ 10 = 9."),
        ("21 = <b>?</b> × 3", 7, [18, 24, 63],
         "The = sign can be at the start. Count in 3s to 21: that takes 7 threes. 21 = <b>7</b> × 3."),
        ("8 = 40 ÷ <b>?</b>", 5, [32, 48, 4],
         "Think: 8 × ? = 40. 8 × 5 = 40, so 8 = 40 ÷ <b>5</b>. (32 is 40 − 8, a take-away mistake.)"),
        ("<b>?</b> = 18 ÷ 2", 9, [16, 20, 36],
         "Half of 18 is 9, because 9 × 2 = 18. So <b>9</b> = 18 ÷ 2."),
        ("5 × 4 = <b>?</b> × 5", 4, [5, 20, 9],
         "You can swap the numbers in multiplication: 5 × 4 = 4 × 5. Both are 20. The missing number is <b>4</b>."),
        ("2 × 10 = 4 × <b>?</b>", 5, [8, 20, 10],
         "2 × 10 = 20. Which number times 4 makes 20? 4 × 5 = 20. The missing number is <b>5</b>."),
        ("<b>?</b> × 2 = 40 ÷ 5", 4, [8, 20, 6],
         "Work out the right side first: 40 ÷ 5 = 8. Then 4 × 2 = 8. The missing number is <b>4</b>. (8 is only the right side.)"),
    ]
    for q, a, w, e in rows:
        assert true_fact(q.replace("<b>?</b>", str(a))), q
        for x in w:
            assert not true_fact(q.replace("<b>?</b>", str(x))), (q, x)
        its.append(mcq("What is the missing number? " + q, a, w, e))

    its.append(mcq("Which number makes both true? 4 × <b>?</b> = 20 and 20 ÷ <b>?</b> = 4", 5, [16, 24, 80],
                   "4 × 5 = 20 and 20 ÷ 5 = 4. They are in the same fact family, so the number is <b>5</b>."))
    assert true_fact("4 × 5 = 20") and true_fact("20 ÷ 5 = 4")
    svg = share_model("20", 4)
    its.append(mcq(fig(svg) + "The bar model shows 20 in 4 equal units. What is the missing number? 20 ÷ 4 = <b>?</b>", 5,
                   [16, 4, 80],
                   "4 units = 20. 1 unit = 20 ÷ 4 = <b>5</b>, because 4 × 5 = 20. (16 is 20 − 4.)"))
    assert len(its) == 20, len(its)
    return {"title": "Missing numbers", "items": its}


# ============================================================ set 5: word problems with bar models
def set_story(P):
    its = []

    def add(q, a, w, e, unit, svg=None):
        if unit == "$":
            u = lambda x: "$%d" % x
        elif unit == "¢":
            u = lambda x: "%d¢" % x
        else:
            u = lambda x: "%d %s" % (x, unit)
        its.append(mcq((fig(svg) if svg else "") + q, u(a), [u(x) for x in w], e))

    # multiplication with bar models
    nm, he, his = P.next()
    add("Mrs Lim buys 4 boxes of curry puffs. Each box has 5 curry puffs. How many curry puffs does she buy?",
        20, [9, 25, 15], "4 units of 5. 4 × 5 = <b>20</b> curry puffs. (4 + 5 = 9 adds instead of multiplying.)",
        "curry puffs", groups_model("5", 4))
    nm, he, his = P.next()
    add("%s has 6 bowls. Each bowl has 3 fish balls. How many fish balls are there?" % nm,
        18, [9, 21, 15], "6 units of 3. 6 × 3 = <b>18</b> fish balls. Count in 3s: %s." % count_on(3, 6),
        "fish balls", groups_model("3", 6))
    add("A bottle of water costs $2. Mr Tan buys 7 bottles. How much does he pay?",
        14, [9, 16, 12], "7 units of $2. 7 × $2 = <b>$14</b>. (7 + 2 = 9 adds instead of multiplying.)",
        "$", groups_model("$2", 7))
    add("Each bag of rice has a mass of 5 kg. What is the mass of 6 bags?",
        30, [11, 35, 25], "6 units of 5 kg. 6 × 5 = <b>30 kg</b>.", "kg", groups_model("5 kg", 6))

    # sharing with bar models
    add("Mdm Wong has 20 rambutans. She shares them equally among 4 children. How many rambutans does each child get?",
        5, [16, 24, 4], "4 units = 20. 1 unit = 20 ÷ 4 = <b>5</b>. Check: 4 × 5 = 20. (16 is 20 − 4, a take-away mistake.)",
        "rambutans", share_model("20", 4))
    nm, he, his = P.next()
    add("%s and %s sister share 18 stickers equally. How many stickers does each of them get?" % (nm, his),
        9, [16, 36, 8], "2 units = 18. 1 unit = 18 ÷ 2 = <b>9</b>. Check: 9 + 9 = 18.", "stickers", share_model("18", 2))
    add("Mr Kumar shares $30 equally among his 3 sons. How much money does each son get?",
        10, [27, 90, 3], "3 units = $30. 1 unit = $30 ÷ 3 = <b>$10</b>. Check: 3 × $10 = $30.", "$", share_model("$30", 3))
    add("Mr Rahman puts 24 pupils into 3 equal teams for Sports Day. How many pupils are in each team?",
        8, [21, 72, 9], "3 units = 24. 1 unit = 24 ÷ 3 = <b>8</b>. Check: 3 × 8 = 24.", "pupils", share_model("24", 3))

    # grouping
    add("There are 35 durian puffs. Mdm Wong puts 5 durian puffs in each box. How many boxes does she fill?",
        7, [30, 40, 5], "35 in groups of 5: count in 5s to 35. That is 7 fives. 35 ÷ 5 = <b>7</b> boxes.", "boxes")
    nm, he, his = P.next()
    add("A pair of socks is 2 socks. %s has 16 socks. How many pairs of socks does %s have?" % (nm, he),
        8, [14, 18, 32], "16 in groups of 2: 16 ÷ 2 = <b>8</b> pairs. Check: 8 × 2 = 16.", "pairs")
    nm, he, his = P.next()
    add("%s has $50 in $10 notes. How many $10 notes does %s have?" % (nm, he),
        5, [40, 60, 10], "Count in 10s: 10, 20, 30, 40, 50. That is 5 tens. 50 ÷ 10 = <b>5</b> notes.", "notes")
    add("Each table at the hawker centre has 4 stools. There are 32 stools. How many tables are there?",
        8, [28, 36, 7], "32 in groups of 4: 32 ÷ 4 = <b>8</b> tables. Check: 8 × 4 = 32.", "tables")
    nm, he, his = P.next()
    add("%s has 40¢ in 5¢ coins. How many 5¢ coins does %s have?" % (nm, he),
        8, [35, 45, 9], "Count in 5s to 40: %s. That is 8 fives. 40 ÷ 5 = <b>8</b> coins." % count_on(5, 8), "coins")
    add("Mr Tan cuts a 20 m rope into pieces of 5 m each. How many pieces does he get?",
        4, [15, 25, 5], "20 in groups of 5: 5, 10, 15, 20. That is 4 fives. 20 ÷ 5 = <b>4</b> pieces.", "pieces")

    # multiplication without a model
    add("Each child gets 2 red packets from Grandma at Chinese New Year. There are 9 children. How many red packets does Grandma give?",
        18, [11, 16, 20], "9 groups of 2. 9 × 2 = <b>18</b> red packets.", "red packets")
    nm, he, his = P.next()
    add("%s reads 4 pages of %s library book every day. How many pages does %s read in 7 days?" % (nm, his, he),
        28, [11, 24, 32], "7 groups of 4. 7 × 4 = <b>28</b> pages. Count in 4s: %s." % count_on(4, 7), "pages")
    nm, he, his = P.next()
    add("A sweet costs 10¢. %s buys 8 sweets. How much does %s pay?" % (nm, he),
        80, [18, 70, 90], "8 groups of 10¢. 8 × 10 = <b>80¢</b>.", "¢")

    # choose the number sentence and spot the mistake
    its.append(mcq("There are 30 eggs. They are put into trays of 10. Which number sentence tells you how many trays there are?",
                   "30 ÷ 10 = 3", ["30 × 10 = 300", "30 − 10 = 20", "10 ÷ 30 = 3"],
                   "Putting into trays of 10 is grouping, so divide. Start with the total: <b>30 ÷ 10 = 3</b> trays."))
    nm, he, his = P.next()
    its.append(mcq("%s says, “I have 4 bags of 5 marbles. That is 9 marbles.” What went wrong?" % nm,
                   "%s added. It is 4 × 5 = 20." % cap(he),
                   ["%s should take away: 5 − 4 = 1." % cap(he), "Nothing. 9 is right.",
                    "%s counted the bags. It is 4." % cap(he)],
                   "4 + 5 = 9 adds the bags to one bag. 4 bags of 5 is 5 + 5 + 5 + 5. "
                   "<b>%s added. It is 4 × 5 = 20.</b>" % cap(he)))
    nm, he, his = P.next()
    its.append(mcq("%s puts 20 stickers into groups of 5. %s says the answer is 5. What is the right answer?" % (nm, cap(he)),
                   "4 groups", ["5 groups", "15 groups", "25 groups"],
                   "5 is the number in each group. 20 ÷ 5 = 4, so there are <b>4 groups</b>. Check: 4 × 5 = 20."))
    assert len(its) == 20, len(its)
    return {"title": "Word problems with bar models", "items": its}


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
    rx = re.compile(r"<svg (?=[^>]*aria-label='(?:" + pattern + "))")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u


def verify(sets):
    """Recompute answers that can be read from the question text."""
    for s in sets:
        for it in s["items"]:
            ans = it["c"][it["a"]]
            q = re.sub(r"<[^>]+>", "", it["q"])
            m = re.search(r"Find the value of (\d+) ÷ (\d+)\.", q)
            if m:
                n, d = int(m.group(1)), int(m.group(2))
                assert n % d == 0 and ans == str(n // d), (q, ans)
            m = re.search(r"Share these (\d+) \w+ equally \w+ (\d+) plates", q)
            if m:
                assert ans == str(int(m.group(1)) // int(m.group(2))), (q, ans)
            m = re.search(r"(\d+) \w+ are put into groups of (\d+)\. How many groups", q)
            if m:
                assert ans == str(int(m.group(1)) // int(m.group(2))), (q, ans)
            m = re.search(r"How many jumps of (\d+) are there from 0 to (\d+)", q)
            if m:
                assert ans == str(int(m.group(2)) // int(m.group(1))), (q, ans)
            # number-sentence choices marked as the answer are true facts
            if re.match(r"^\d+ [×÷−+] \d+ = \d+$", ans) and " not " not in q:
                assert true_fact(ans), ans
            # a choice set of number sentences has exactly one true sentence, unless it is a "not" question
            # (questions about which operation matches a story may use true sentences as wrong choices)
            if all(re.match(r"^\d+ [×÷−+] \d+ = \d+$", c) for c in it["c"]) and re.search(r"fact|picture show", q):
                tv = [true_fact(c) for c in it["c"]]
                if "not" in q:
                    assert tv.count(False) == 1 and not tv[it["a"]], (q, it["c"])
                else:
                    assert tv.count(True) == 1 and tv[it["a"]], (q, it["c"])


# ============================================================ lesson
def body_html():
    return (
        "<h2>Sharing equally</h2>"
        "<p>Division (÷) is <b>sharing equally</b>. You know how many groups there are. "
        "Give out one at a time until none are left. Every group must have the same number.</p>"
        "<figure class='sn-fig'>" + groups_svg([4, 4, 4], "dot", "plate", "12 counters shared equally among 3 plates") +
        "<figcaption>12 counters shared equally among 3 plates: 4 on each plate. 12 ÷ 3 = 4.</figcaption></figure>"
        + ex("Example", "Share 10 sweets equally between 2 friends. How many sweets does each friend get?",
             "Give out one at a time: 5 each. 10 ÷ 2 = 5. Check: 2 × 5 = 10.", "5 sweets")
        + "<h2>Grouping</h2>"
        "<p>Division is also <b>making equal groups</b>. You know how many go in each group. "
        "Make groups until none are left, then count the groups.</p>"
        "<figure class='sn-fig'>" + groups_svg([3, 3, 3, 3], "dot", "ring", "12 counters in groups of 3") +
        "<figcaption>12 counters in groups of 3: 4 groups. 12 ÷ 3 = 4.</figcaption></figure>"
        + ex("Example", "30 pupils make teams of 5. How many teams are there?",
             "Count in 5s to 30: 5, 10, 15, 20, 25, 30. That is 6 fives. 30 ÷ 5 = 6.", "6 teams")
        + "<h2>The ÷ sign and fact families</h2>"
        "<p>Multiplication and division go together. One array gives a <b>fact family</b> of four facts. "
        "You can swap the numbers in ×, but <b>not in ÷</b>. A division starts with the whole amount.</p>"
        "<figure class='sn-fig'>" + lesson_array_svg(2, 5) +
        "<figcaption>2 rows of 5 = 10 and 5 columns of 2 = 10.</figcaption></figure>"
        + table(["Numbers", "× facts", "÷ facts"], [
            ["2, 5, 10", "2 × 5 = 10, 5 × 2 = 10", "10 ÷ 2 = 5, 10 ÷ 5 = 2"],
            ["3, 4, 12", "3 × 4 = 12, 4 × 3 = 12", "12 ÷ 3 = 4, 12 ÷ 4 = 3"],
            ["4, 10, 40", "4 × 10 = 40, 10 × 4 = 40", "40 ÷ 4 = 10, 40 ÷ 10 = 4"],
        ])
        + "<h2>Missing numbers</h2>"
        "<p>Use a related fact. To find 35 ÷ 5, think “5 times what is 35?” 5 × 7 = 35, so 35 ÷ 5 = 7.</p>"
        + ex("Example", "Find the missing number: <b>?</b> ÷ 4 = 3.",
             "Use the related fact: 3 × 4 = 12. So 12 ÷ 4 = 3.", "12")
        + "<h2>Word problems with a bar model</h2>"
        "<p>Draw a bar for the whole. Cut it into equal <b>units</b>. Then write what you know and what you must find.</p>"
        "<figure class='sn-fig'>" + share_model("20", 4) +
        "<figcaption>20 rambutans shared equally among 4 children. 4 units = 20, so 1 unit = 20 ÷ 4 = 5.</figcaption></figure>"
        "<figure class='sn-fig'>" + groups_model("5", 4) +
        "<figcaption>4 boxes of 5 curry puffs. 4 units of 5: 4 × 5 = 20.</figcaption></figure>"
        "<h2>Common mistakes</h2>"
        + table(["Mistake", "What to do instead"], [
            ["Taking away: 12 ÷ 3 = 9", "Share 12 into 3 equal groups: 12 ÷ 3 = 4, because 3 × 4 = 12"],
            ["Dividing the wrong way: 3 ÷ 12 = 4", "Start with the whole amount: 12 ÷ 3 = 4"],
            ["Mixing up groups and number in each group: 20 in groups of 5 is 5", "5 is in each group. Count the groups: 20 ÷ 5 = 4"],
            ["Adding: 4 bags of 5 is 9", "Add 5 once for each bag: 5 + 5 + 5 + 5 = 4 × 5 = 20"],
        ])
    )


FAQ = [
    {"q": "What multiplication and division is taught in Primary 2 maths?",
     "a": "In the MOE syllabus, Primary 2 pupils learn the multiplication tables of 2, 3, 4, 5 and 10, the ÷ sign, and how multiplication and division are related. They solve 1-step word problems, often with a bar model."},
    {"q": "How do I explain division to my P2 child?",
     "a": "Use real objects: share 12 sweets equally among 3 plates, then put 12 sweets into groups of 3. Both give 12 ÷ 3 = 4, and 3 × 4 = 12 checks the answer."},
    {"q": "What is the most common mistake in P2 division?",
     "a": "Taking away instead of sharing, such as writing 12 ÷ 3 = 9, is the most common. Mixing up the number of groups with the number in each group comes next."},
    {"q": "What is a fact family in P2 maths?",
     "a": "A fact family is the four facts made from three numbers, such as 3 × 4 = 12, 4 × 3 = 12, 12 ÷ 3 = 4 and 12 ÷ 4 = 3. Knowing one fact helps pupils find the others."},
]


def gen():
    rnd = random.Random(62805)
    P = People(rnd)
    sets = [set_sharing(P), set_grouping(P), set_facts(P), set_missing(P), set_story(P)]
    balance(sets, rnd)
    verify(sets)
    keys = set()
    for s in sets:
        assert len(s["items"]) == 20, (s["title"], len(s["items"]))
        assert sorted(it["a"] for it in s["items"]) == sorted([0, 1, 2, 3] * 5), s["title"]
        for it in s["items"]:
            assert len(set(it["c"])) == 4, it
            assert it["q"].count("<svg") <= 1, it["q"]
            assert "{" not in it["e"] and "_abcd" not in it
            k = re.sub(r"<[^>]+>", "", it["q"]) + "|" + "|".join(sorted(it["c"]))
            assert k not in keys, it["q"]
            keys.add(k)
            m = re.search(r"aria-label='array of (\d+) rows and (\d+) columns", it["q"])
            if m:
                assert n_objects(it["q"]) == int(m.group(1)) * int(m.group(2)), it["q"]
    u = {
        "country": "sg", "subject": "maths", "grade": "primary-2", "slug": "multiplication-and-division", "sort": 5,
        "updated": UPDATED, "pdf_url": "",
        "title": "Primary 2 Multiplication and Division",
        "seo_title": "P2 Multiplication and Division Worksheets: Free Primary 2 Maths with Answers (MOE Syllabus)",
        "short_title": "Multiplication and Division",
        "domain": "Number and Algebra",
        "standard_code": "Primary 2: Whole Numbers",
        "standard_url": "https://www.moe.gov.sg/primary/curriculum/syllabus",
        "standard_text": "Use of ÷; relationship between multiplication and division; multiplying and dividing within the multiplication tables",
        "meta_desc": "Free P2 practice: sharing equally, grouping, the ÷ sign, fact families, missing numbers and bar model word problems. 100 questions with answers.",
        "key_big": "Division is sharing equally or making equal groups, and every ÷ fact comes from a × fact.",
        "key_sub": "3 × 4 = 12, so 12 ÷ 3 = 4 and 12 ÷ 4 = 3.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }
    assert len(u["meta_desc"]) <= 160, len(u["meta_desc"])
    return mark_large(u, "four pictures|\\d+ (groups|plates) of|\\d+ \\w+ in rows of 10|array of \\d+ rows and 10 |number line|bar model")


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
