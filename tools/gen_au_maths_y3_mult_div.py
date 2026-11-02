# -*- coding: utf-8 -*-
"""
AU Year 3 Maths: Multiplying and dividing (Australian Curriculum v9.0, AC9M3N04)
Arrays and number sentences, multiplying a 2-digit number by a 1-digit number by partitioning (area model),
dividing by sharing, grouping and partitioning, remainders, choosing the number sentence, word problems.
  python3 tools/gen_au_maths_y3_mult_div.py
HTML attributes use single quotes (no backslashes in the JSON). Every drawn picture is counted in code.
Australian style: Australian English, $ and c, numbers under 1000 (no separators needed).
"""
import json, os, random, re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "au", "maths", "year-3")
UPDATED = "2026-11-02"
GREEN = "#006633"
FILL = "#cfe6d6"
FILL2 = "#eef6f0"
RED = "#c0392b"
GREY = "#9a9a9a"
INK = "#2b2b2b"
FONT = "Arial, Helvetica, sans-serif"


# ------------------------------------------------------------ helpers
def mcq(q, correct, cands, e, rnd=None):
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


def cap(s):
    return s[0].upper() + s[1:]


def fig(svg):
    return "<div class='qfig'>" + svg + "</div>"


def svg_wrap(w, h, body, label):
    return ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 %d %d' width='%d' height='%d' "
            "role='img' aria-label='%s'><g font-family='%s'>%s</g></svg>" % (w, h, w, h, label, FONT, body))


def tw(t, fs):
    return len(str(t)) * fs * 0.6


def text(x, y, t, fs=18, anchor="middle", col=INK):
    return ("<text x='%.1f' y='%.1f' font-size='%d' font-weight='700' fill='%s' text-anchor='%s'>%s</text>"
            % (x, y, fs, col, anchor, t))


def dot(cx, cy, r=9, col=GREEN):
    return "<circle cx='%.1f' cy='%.1f' r='%.1f' fill='%s'/>" % (cx, cy, r, col)


def n_dots(svg):
    return svg.count("<circle ")


def parts(n):
    """23 -> [20, 3]."""
    return [n // 10 * 10, n % 10]


def tens(k):
    return "%d ten%s" % (k, "" if k == 1 else "s")


def rep(n, times):
    return " + ".join([str(n)] * times)


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
    return svg_wrap(x0 + cols * S + 36, y0 + rows * S + 10, "".join(el),
                    "array of %d rows of %d dots, with each row counted" % (rows, cols))


def area_svg(a, d, cells=None, label=None):
    """Area model: a rectangle d tall, split into tens and ones. Labels above and to the left."""
    t, o = parts(a)
    cells = cells or ["", ""]
    FS = 18
    wt = max(118, tw(cells[0], FS) + 30)
    wo = max(66, tw(cells[1], FS) + 26)
    x0, y0, h = 34, 30, 60
    s = []
    for x, w, top, c in ((x0, wt, t, cells[0]), (x0 + wt, wo, o, cells[1])):
        s.append("<rect x='%.1f' y='%d' width='%.1f' height='%d' fill='%s' stroke='%s' stroke-width='2.5'/>"
                 % (x, y0, w, h, FILL2 if c != "?" else "#ffffff", GREEN))
        s.append(text(x + w / 2, y0 - 9, str(top), FS, col=GREEN))
        if c:
            s.append(text(x + w / 2, y0 + h / 2 + 6, c, FS, col=RED if c == "?" else INK))
    s.append(text(x0 - 14, y0 + h / 2 + 6, str(d), FS, col=GREEN))
    W = int(x0 + wt + wo + 6)
    return svg_wrap(W, y0 + h + 6, "".join(s), label or "area model: %d × %d split into %d and %d" % (a, d, t, o))


def split_svg(whole, a, b, d=None, label=None):
    """Part-whole diagram: the whole on top, two parts below. With d: '÷ d = …' under each part."""
    FS = 18
    bw = max(64, tw(whole, FS) + 26)
    pw = max(64, tw(max(a, b), FS) + 26)
    gap = 40 if d is None else 70
    W = int(max(bw, 2 * pw + gap) + 8)
    cx = W / 2
    s = ["<rect x='%.1f' y='4' width='%.1f' height='38' rx='6' fill='%s' stroke='%s' stroke-width='2.5'/>"
         % (cx - bw / 2, bw, FILL, GREEN), text(cx, 29, whole, FS)]
    xs = [cx - gap / 2 - pw / 2, cx + gap / 2 + pw / 2]
    for x, v in zip(xs, (a, b)):
        s.append("<line x1='%.1f' y1='42' x2='%.1f' y2='72' stroke='%s' stroke-width='2.5'/>" % (cx, x, GREEN))
        s.append("<rect x='%.1f' y='72' width='%.1f' height='38' rx='6' fill='#ffffff' stroke='%s' stroke-width='2.5'/>"
                 % (x - pw / 2, pw, GREEN))
        s.append(text(x, 97, v, FS))
        if d is not None:
            s.append(text(x, 134, "÷ %d = %d" % (d, v // d), 17, col=GREEN))
    H = 116 if d is None else 142
    if d is not None:
        W = int(max(W, xs[1] + tw("÷ %d = %d" % (d, b // d), 17) / 2 + 6))
    return svg_wrap(W, H, "".join(s), label or ("%d partitioned into %d and %d" % (whole, a, b)))


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


def rem_svg(n, group):
    """n counters: full groups of `group` in rings, the leftovers on their own (outside any ring)."""
    R, STEP = 8, 21
    g, rem = divmod(n, group)
    gw = group * STEP + 10
    x, y0 = 4, 4
    s = []
    for _ in range(g):
        s.append("<rect x='%.1f' y='%.1f' width='%.1f' height='%.1f' rx='10' fill='%s' stroke='%s' stroke-width='2'/>"
                 % (x, y0, gw, STEP + 12, FILL2, GREEN))
        for k in range(group):
            s.append(dot(x + 5 + STEP / 2 + k * STEP, y0 + 6 + STEP / 2, R))
        x += gw + 10
    for k in range(rem):
        s.append(dot(x + 5 + STEP / 2 + k * STEP, y0 + 6 + STEP / 2, R, RED))
    x += rem * STEP + 10
    svg = svg_wrap(int(x + 4), int(y0 + STEP + 16), "".join(s),
                   "%d counters: %d groups of %d and %d left over" % (n, g, group, rem))
    assert n_dots(svg) == n
    return svg


# ------------------------------------------------------------ typical mistakes for a × d
def concat(a, d):
    """Each part's answer written side by side: 23 × 4 -> 8 | 12 -> 812."""
    t, o = a // 10, a % 10
    return int(str(t * d) + str(o * d))


def no_regroup(a, d):
    """Adding 80 + 12 as 82: the ten in 12 is lost."""
    t, o = parts(a)
    return t * d + (o * d) % 10


def tens_as_ones(a, d):
    """20 × 4 = 8, so 23 × 4 = 8 + 12 = 20."""
    return (a // 10) * d + (a % 10) * d


def cands_mult(a, d):
    t, o = parts(a)
    out = []
    if o * d >= 10:
        out.append(no_regroup(a, d))
    if concat(a, d) < 1000:
        out.append(concat(a, d))
    out += [tens_as_ones(a, d), t * d + o, a + d, a * (d + 1)]
    return [v for v in out if v != a * d]


def area_steps(a, d):
    t, o = parts(a)
    return ("Partition %d = %d + %d. %d × %d = %d and %d × %d = %d. Add: %d + %d = %d."
            % (a, t, o, t, d, t * d, o, d, o * d, t * d, o * d, a * d))


# ------------------------------------------------------------ set 1: arrays and number sentences
def set_arrays():
    its = []
    # A: which number sentence matches the array?
    for r, c in [(3, 5), (2, 8), (4, 10), (5, 4), (2, 6)]:
        right = "%d × %d = %d" % (r, c, r * c)
        wrong = ["%d + %d = %d" % (r, c, r + c), "%d × %d = %d" % (r, c + 1, r * (c + 1)),
                 "%d × %d = %d" % (r + 1, c, (r + 1) * c)]
        e = ("There are %d rows with %d dots in each row: %s = %d. So the array shows <b>%s</b>. "
             "(Adding %d + %d mixes up the number of rows with the number in a row.)"
             % (r, c, rep(c, r), r * c, right, r, c))
        its.append(mcq(fig(array_svg(r, c)) + "Which number sentence matches this array?", right, wrong, e))
    # B: how many dots altogether?
    for r, c in [(5, 5), (3, 10), (4, 6), (2, 9)]:
        e = ("%d rows of %d. Count in %ds: %s. That is %d × %d = <b>%d</b>."
             % (r, c, c, ", ".join(str(c * (i + 1)) for i in range(r)), r, c, r * c))
        its.append(mcq(fig(array_svg(r, c)) + "There are %d rows of %d dots. How many dots are there altogether?" % (r, c),
                       r * c, [r + c, (r + 1) * c, (r - 1) * c, r * c + 1], e))
    # C: repeated addition
    for n, k, wrong in [(5, 4, ["5 × 5", "4 + 5", "4 × 4"]), (10, 3, ["10 × 10", "3 + 10", "3 × 3"]),
                        (3, 5, ["3 × 3", "5 + 3", "5 × 5"])]:
        e = "There are %d lots of %d, so %s = <b>%d × %d</b> = %d." % (k, n, rep(n, k), k, n, k * n)
        its.append(mcq("Which is the same as <b>%s</b>?" % rep(n, k), "%d × %d" % (k, n), wrong, e))
    # D: turn the array around
    for r, c in [(3, 4), (2, 5), (4, 10)]:
        right = "%d × %d = %d" % (c, r, r * c)
        wrong = ["%d × %d = %d" % (r, r, r * r), "%d × %d = %d" % (c, c, c * c), "%d + %d = %d" % (c, r, c + r)]
        e = ("Turn the array a quarter turn. The %d rows of %d become %d rows of %d. The number of dots does not change: "
             "<b>%s</b>. This is the turnaround fact." % (r, c, c, r, right))
        its.append(mcq(fig(array_svg(r, c)) + "This array shows %d × %d = %d. Turn it around. Which number sentence does it show now?"
                       % (r, c, r * c), right, wrong, e))
    # E: division from an array
    for r, c in [(3, 6), (2, 10), (4, 4)]:
        n = r * c
        right = "%d ÷ %d = %d" % (n, r, c)
        wrong = ["%d − %d = %d" % (n, r, n - r), "%d ÷ %d = %d" % (n, r, c + 1), "%d × %d = %d" % (n, r, n * r)]
        e = ("%d dots are split into %d equal rows. Each row has %d dots, so <b>%s</b>. Check: %d × %d = %d."
             % (n, r, c, right, r, c, n))
        its.append(mcq(fig(array_svg(r, c)) + "These %d dots are in %d equal rows. Which division does the array show?" % (n, r),
                       right, wrong, e))
    its.append(mcq(fig(array_svg(4, 5)) + "Use the array. What number goes in the box?  <b>☐ × 5 = 20</b>", 4,
                   [5, 20, 15],
                   "Count the rows of 5: there are 4. 4 × 5 = 20, so the missing number is <b>4</b>."))
    its.append(mcq(fig(array_svg(2, 7)) + "Use the array. What number goes in the box?  <b>2 × ☐ = 14</b>", 7,
                   [12, 16, 28],
                   "There are 2 rows. Each row has 7 dots. 2 × 7 = 14, so the missing number is <b>7</b>. "
                   "(12 is 14 − 2 and 28 is 14 × 2.)"))
    assert len(its) == 20, len(its)
    return {"title": "Arrays and number sentences", "items": its}


# ------------------------------------------------------------ set 2: multiply by partitioning
def set_partition(rnd):
    its = []
    seen = set()

    def pick(ones_regroup=True):
        while True:
            a, d = rnd.randint(12, 49), rnd.choice([2, 3, 4, 5])
            t, o = parts(a)
            if o == 0 or a // 10 == o or (a, d) in seen or (a, d) == (23, 4) or (a, d) == (14, 3):
                continue
            if ones_regroup != (o * d >= 10):
                continue
            seen.add((a, d))
            return a, d

    # A: tens × 1-digit (the 20 × 4 = 8 mistake)
    for tt, d in [(20, 4), (30, 5), (40, 3), (50, 2)]:
        k = tt // 10
        e = ("%d is %s. %s × %d = %s = <b>%d</b>. Not %d: that would be ones, not tens."
             % (tt, tens(k), tens(k), d, tens(k * d), tt * d, k * d))
        its.append(mcq("What is %d × %d?  <i>Think: %d × %d = %d.</i>" % (tt, d, k, d, k * d), tt * d,
                       [k * d, tt * d * 10, tt + d], e))
    # B: use the area model
    for i in range(6):
        a, d = pick(ones_regroup=i < 4)
        t, o = parts(a)
        e = area_steps(a, d) + " Remember: %d × %d = %d, not %d." % (t, d, t * d, t // 10 * d)
        if o * d >= 10:
            e += " And %d + %d = %d, not %d." % (t * d, o * d, a * d, no_regroup(a, d))
        q = fig(area_svg(a, d)) + "Use the area model. What is %d × %d?" % (a, d)
        its.append(mcq(q, a * d, cands_mult(a, d), e))
    # C: one part of the area model is missing
    for k in range(4):
        a, d = pick(ones_regroup=k < 2)
        t, o = parts(a)
        if k % 2 == 0:
            cells, ans = ["?", str(o * d)], t * d
            wrong = [t // 10 * d, t * d * 10, t + d]
            e = "The ? part is %d × %d. %s × %d = %s = %d." % (t, d, tens(t // 10), d, tens(t // 10 * d), t * d)
        else:
            cells, ans = [str(t * d), "?"], o * d
            wrong = [o + d, (o + 1) * d, (o - 1) * d if o > 2 else (o + 2) * d, (o + 2) * d, o * d * 10]
            e = "The ? part is %d × %d = %d." % (o, d, o * d)
        e += " Altogether: %d × %d = %d + %d = %d." % (a, d, t * d, o * d, a * d)
        its.append(mcq(fig(area_svg(a, d, cells)) + "What number goes in the part marked ?", ans, wrong, e))
    # D: which partitioning is right?
    for _ in range(3):
        a, d = pick()
        t, o = parts(a)
        right = "%d × %d + %d × %d" % (t, d, o, d)
        wrong = ["%d × %d + %d × %d" % (t // 10, d, o, d), "%d × %d + %d" % (t, d, o), "%d + %d × %d" % (t, o, d)]
        e = ("Partition %d into %d + %d. Multiply <b>both</b> parts by %d, then add: %s = %d + %d = %d."
             % (a, t, o, d, right, t * d, o * d, a * d))
        its.append(mcq("Which is the same as %d × %d?" % (a, d), right, wrong, e))
    # E: missing number in the number sentence
    for k in range(3):
        a, d = pick()
        t, o = parts(a)
        if k == 0:
            q = "%d × %d = %d × %d + ☐ × %d" % (a, d, t, d, d)
            ans, wrong = o, [t // 10, a, o * d]
            e = "%d = %d + %d, so %d × %d = %d × %d + %d × %d. The missing number is <b>%d</b>." % (a, t, o, a, d, t, d, o, d, o)
        elif k == 1:
            q = "%d × %d = ☐ × %d + %d × %d" % (a, d, d, o, d)
            ans, wrong = t, [t // 10, a, t * d]
            e = ("%d = %d + %d, so %d × %d = %d × %d + %d × %d. The missing number is <b>%d</b> (%s, not %d)."
                 % (a, t, o, a, d, t, d, o, d, t, tens(t // 10), t // 10))
        else:
            q = "%d × %d = %d + ☐" % (a, d, t * d)
            ans, wrong = o * d, [o, o + d, (o + 1) * d]
            e = ("%d × %d = %d × %d + %d × %d = %d + %d. The missing number is %d × %d = <b>%d</b>."
                 % (a, d, t, d, o, d, t * d, o * d, o, d, o * d))
        its.append(mcq("What number goes in the box?  <b>%s</b>" % q, ans, wrong, e))
    assert len(its) == 20, len(its)
    return {"title": "Multiplying by partitioning", "items": its}


# ------------------------------------------------------------ set 3: sharing, grouping and partitioning
def rev(n):
    return int(str(n)[::-1])


def set_divide():
    its = []
    # A: share counters that are not yet shared
    for n, k, where in [(12, 3, "plates"), (20, 4, "plates"), (15, 5, "bags"), (18, 2, "boxes")]:
        a = n // k
        one = {"plates": "plate", "bags": "bag", "boxes": "box"}[where]
        prep = "on" if where == "plates" else "in"
        e = ("Sharing: give the counters out one at a time, round and round, until none are left. "
             "Each of the %d %s gets <b>%d</b>. %d ÷ %d = %d." % (k, where, a, n, k, a))
        its.append(mcq(fig(counters_svg(n)) + "Share these %d counters equally between %d %s. How many go %s each %s?"
                       % (n, k, where, prep, one), a, [k, n - k, a + 1, a - 1], e))
    # B1: grouping pictures, count the groups
    for n, k in [(20, 5), (24, 4)]:
        g = n // k
        e = ("Grouping: you know there are %d in each group. Count the rings: %d groups. So %d ÷ %d = <b>%d</b>."
             % (k, g, n, k, g))
        its.append(mcq(fig(groups_svg([k] * g, "ring")) + "%d counters are put into groups of %d. How many groups are there?"
                       % (n, k), g, [k, n - k, g + 1, n], e))
    # B2: sharing pictures, which division?
    for n, k in [(24, 4), (15, 3)]:
        a = n // k
        right = "%d ÷ %d = %d" % (n, k, a)
        wrong = ["%d ÷ %d = %d" % (k, n, a), "%d − %d = %d" % (n, k, n - k), "%d ÷ %d = %d" % (n, k, a + 1)]
        e = "%d counters are shared between %d plates. Each plate has %d. That is <b>%s</b>." % (n, k, a, right)
        its.append(mcq(fig(groups_svg([a] * k, "plate")) +
                       "%d counters are shared equally between %d plates. Which division does the picture show?" % (n, k),
                       right, wrong, e))
    # C: sharing or grouping?
    its.append(mcq("Which one is <b>grouping</b>?", "Put 20 oranges in bags of 5.",
                   ["Share 20 oranges between 5 bags.", "Add 5 more oranges to 20.", "Eat 5 of the 20 oranges."],
                   "Grouping means you know how many go in each group. “Bags of 5” tells you there are 5 in each bag. "
                   "That makes 20 ÷ 5 = 4 bags. Sharing between 5 bags gives 4 in each bag."))
    its.append({"q": "", "c": ["A", "B", "C", "D"], "a": 3,
                "e": ("Sharing between 3 plates means exactly 3 plates, all the same. <b>{L}</b> has 3 plates of 4. "
                      "4 plates of 3 is groups of 3. 4, 4 and 3 is not equal, and 3 plates of 3 is only 9."),
                "_abcd": ("Share 12 counters equally between 3 plates. Which picture shows this?",
                          [4, 4, 4], [[3, 3, 3, 3], [4, 4, 3], [3, 3, 3]], "plate")})
    # D: tens ÷ 1-digit with a known fact
    for a, d in [(80, 4), (60, 3), (40, 2), (50, 5)]:
        k = a // 10
        e = ("%d is %s. %s ÷ %d = %s = <b>%d</b>. Not %d: the answer is tens, not ones."
             % (a, tens(k), tens(k), d, tens(k // d), a // d, k // d))
        its.append(mcq("What is %d ÷ %d?  <i>Think: %d ÷ %d = %d.</i>" % (a, d, k, d, k // d), a // d,
                       [k // d, a * d, a - d], e))
    # E: divide by partitioning
    for a, d, big, fg in [(48, 4, 40, True), (69, 3, 60, True), (84, 4, 80, False),
                          (72, 3, 60, True), (56, 4, 40, False), (75, 5, 50, False)]:
        rest = a - big
        ans = a // d
        easy = big == a // 10 * 10
        e = ("Partition %d = %d + %d. %d ÷ %d = %d and %d ÷ %d = %d. Add: %d + %d = <b>%d</b>. Check: %d × %d = %d."
             % (a, big, rest, big, d, big // d, rest, d, rest // d, big // d, rest // d, ans, ans, d, a))
        if not easy:
            e = ("%d tens do not share equally into %d, so use %d = %d + %d. " % (a // 10, d, a, big, rest)) + e[e.index(".") + 2:]
        wrong = [big // d + rest, big // 10 // d + rest // d, rev(ans), a - d, ans + 10]
        q = "What is %d ÷ %d?" % (a, d)
        if fg:
            q = fig(split_svg(a, big, rest)) + "%d is partitioned like this. What is %d ÷ %d?" % (a, a, d)
        its.append(mcq(q, ans, wrong, e))
    assert len(its) == 20, len(its)
    return {"title": "Dividing by sharing and grouping", "items": its}


# ------------------------------------------------------------ set 4: remainders and choosing the number sentence
def set_choose():
    its = []
    # A: remainders
    for i, (a, d) in enumerate([(17, 5), (23, 4), (14, 3), (22, 5), (19, 2)]):
        q_, r = divmod(a, d)
        right = "%d r %d" % (q_, r)
        wrong = ["%d r %d" % (q_ - 1, r + d), "%d r %d" % (q_, d - r), str(q_), "%d r %d" % (q_ + 1, (q_ + 1) * d - a)]
        e = ("%d × %d = %d and %d × %d = %d, which is too many. So %d groups of %d, and %d − %d = %d left over. "
             "The remainder is always less than %d." % (q_, d, q_ * d, q_ + 1, d, (q_ + 1) * d, q_, d, a, q_ * d, r, d))
        q = "What is %d ÷ %d?" % (a, d)
        if i < 2:
            q = fig(rem_svg(a, d)) + "%d counters are put into groups of %d. What is %d ÷ %d?" % (a, d, a, d)
        its.append(mcq(q, right, wrong, e))
    # B: what to do with the remainder
    its.append(mcq("26 students have lunch at tables. 4 students sit at each table. How many tables are needed so every student has a seat?",
                   "7 tables", ["6 tables", "8 tables", "22 tables"],
                   "26 ÷ 4 = 6 r 2. 6 tables seat 24 students. The 2 students left over need one more table, so <b>7 tables</b>."))
    its.append(mcq("Chloe has $23. Books cost $5 each. How many books can she buy?",
                   "4 books", ["5 books", "3 books", "18 books"],
                   "23 ÷ 5 = 4 r 3. 4 books cost $20. The $3 left over is not enough for another book, so <b>4 books</b>."))
    its.append(mcq("Cooper puts 29 cards into 3 equal piles. How many cards are left over?",
                   "2", ["9", "3", "1"],
                   "9 × 3 = 27 and 10 × 3 = 30, which is too many. So each pile has 9 cards, and 29 − 27 = <b>2</b> are left over."))
    # C: choose the number sentence
    stories = [
        ("There are 4 rows of chairs. Each row has 6 chairs. How many chairs are there?", "4 × 6 = ☐",
         ["4 + 6 = ☐", "6 + 6 + 6 = ☐", "6 − 4 = ☐"],
         "4 equal rows of 6 is multiplication: <b>4 × 6 = ☐</b>. 6 + 6 + 6 only counts 3 rows."),
        ("Ruby shares 24 stickers equally among 4 friends. How many stickers does each friend get?", "24 ÷ 4 = ☐",
         ["24 × 4 = ☐", "24 − 4 = ☐", "24 + 4 = ☐"],
         "Sharing equally is division: <b>24 ÷ 4 = ☐</b>. Each friend gets 6."),
        ("Noah puts 35 cards in piles of 5. How many piles does he make?", "35 ÷ 5 = ☐",
         ["35 × 5 = ☐", "35 − 5 = ☐", "5 ÷ 35 = ☐"],
         "Making groups of 5 is division (grouping): <b>35 ÷ 5 = ☐</b>. Start with the total, 35. He makes 7 piles."),
        ("A koala toy costs $7. How much do 3 koala toys cost?", "3 × 7 = ☐",
         ["3 + 7 = ☐", "7 − 3 = ☐", "7 + 7 = ☐"],
         "3 lots of $7 is multiplication: <b>3 × 7 = ☐</b>. They cost $21. 7 + 7 is only 2 toys."),
        ("Mia had 18 shells. She found 6 more. How many shells does she have now?", "18 + 6 = ☐",
         ["18 × 6 = ☐", "18 ÷ 6 = ☐", "18 − 6 = ☐"],
         "Finding more is adding. There are no equal groups here, so it is <b>18 + 6 = ☐</b>. She has 24 shells."),
        ("Leo has some bags of 4 oranges. He has 20 oranges. Which number sentence finds the number of bags?",
         "☐ × 4 = 20", ["20 × 4 = ☐", "20 + 4 = ☐", "20 − 4 = ☐"],
         "Some bags of 4 make 20: <b>☐ × 4 = 20</b>. 5 × 4 = 20, so he has 5 bags. (20 ÷ 4 = ☐ would also work.)"),
        ("Kai has 5 marbles. Zara has 3 times as many. How many marbles does Zara have?", "5 × 3 = ☐",
         ["5 + 3 = ☐", "5 + 5 = ☐", "5 − 3 = ☐"],
         "“3 times as many” means multiply: <b>5 × 3 = ☐</b>. Zara has 15 marbles. 5 + 5 is only 2 times as many."),
        ("Grace had 30 stickers. She gave 6 to her brother. How many stickers does she have left?", "30 − 6 = ☐",
         ["30 ÷ 6 = ☐", "30 × 6 = ☐", "30 + 6 = ☐"],
         "Giving some away is taking away. Nothing is shared equally, so it is <b>30 − 6 = ☐</b>. She has 24 left."),
    ]
    for q, right, wrong, e in stories:
        its.append(mcq(q + " Which number sentence matches the story?" if not q.startswith("Leo") else q, right, wrong, e))
    # D: missing numbers using the inverse
    its.append(mcq("What number goes in the box?  <b>☐ ÷ 4 = 12</b>", 48, [3, 16, 8],
                   "Use the inverse: ☐ = 12 × 4 = 48 (10 × 4 = 40 and 2 × 4 = 8). Check: 48 ÷ 4 = 12."))
    its.append(mcq("What number goes in the box?  <b>☐ ÷ 3 = 21</b>", 63, [7, 24, 18],
                   "Use the inverse: ☐ = 21 × 3 = 63 (20 × 3 = 60 and 1 × 3 = 3). Check: 63 ÷ 3 = 21."))
    its.append(mcq("What number goes in the box?  <b>☐ × 5 = 45</b>", 9, [40, 50, 225],
                   "Think: how many 5s make 45? 9 × 5 = 45, so ☐ = 9. Or use the inverse: 45 ÷ 5 = 9."))
    its.append(mcq("What number goes in the box?  <b>40 ÷ ☐ = 8</b>", 5, [32, 48, 320],
                   "How many groups of 8 make 40? 5 × 8 = 40, so ☐ = 5. Check: 40 ÷ 5 = 8."))
    assert len(its) == 20, len(its)
    return {"title": "Remainders and choosing the number sentence", "items": its}


# ------------------------------------------------------------ set 5: word problems
def set_story():
    its = []
    mult = [
        ("There are 4 rows of chairs at assembly. Each row has 23 chairs. How many chairs are there?", 23, 4, "{} chairs"),
        ("A relay team at the swimming carnival has 4 swimmers. There are 16 teams. How many swimmers is that?", 16, 4, "{} swimmers"),
        ("Two buses take Year 3 on a school excursion. Each bus has 45 seats. How many seats is that altogether?", 45, 2, "{} seats"),
        ("A packet has 12 sausages. The school buys 5 packets for the sausage sizzle. How many sausages is that?", 12, 5, "{} sausages"),
        ("A netball team has 7 players on the court. There are 5 teams at training. How many players is that?", 7, 5, "{} players"),
        ("An AFL team has 18 players on the field. How many players are on the field when 2 teams play?", 18, 2, "{} players"),
        ("A cricket team has 11 players. 4 teams play at a school cricket day. How many players is that?", 11, 4, "{} players"),
        ("A child’s ticket to the aquarium costs $25. Oliver’s mum buys 3 child tickets. How much does she pay?", 25, 3, "${}"),
    ]
    for q, a, d, fm in mult:
        e = "Equal groups, so multiply: %d × %d. " % (a, d)
        if a >= 10:
            e += area_steps(a, d) + " "
        e += "The answer is <b>%s</b>." % fm.format(a * d)
        cands = cands_mult(a, d) if a >= 10 else [a + d, a * (d + 1), a * (d - 1)]
        its.append(mcq(q, fm.format(a * d), [fm.format(v) for v in cands], e))
    div = [
        ("Matilda shares $24 equally between 3 children. How much does each child get?", "$8",
         ["$21", "$27", "$72"], "Sharing equally: $24 ÷ 3. 3 × 8 = 24, so each child gets <b>$8</b>."),
        ("The school chooks laid 30 eggs. The eggs are packed in boxes of 6. How many boxes are filled?", "5",
         ["6", "24", "36"], "Grouping in 6s: 30 ÷ 6. 5 × 6 = 30, so <b>5</b> boxes are filled."),
        ("96 students are split equally into 4 sport houses. How many students are in each house?", "24",
         ["21", "92", "100"],
         "96 ÷ 4. Partition 96 = 80 + 16. 80 ÷ 4 = 20 and 16 ÷ 4 = 4. Add: 20 + 4 = <b>24</b>. Check: 24 × 4 = 96."),
        ("64 chairs are set out in 4 equal rows for assembly. How many chairs are in each row?", "16",
         ["61", "60", "26"],
         "64 ÷ 4. Partition 64 = 40 + 24. 40 ÷ 4 = 10 and 24 ÷ 4 = 6. Add: 10 + 6 = <b>16</b>. Check: 16 × 4 = 64."),
        ("There are 55 players at a cricket day. Each team has 11 players. How many teams are there?", "5",
         ["44", "66", "6"],
         "Grouping in 11s: count 11, 22, 33, 44, 55. That is 5 elevens, so 55 ÷ 11 = <b>5</b> teams."),
        ("84 coloured pencils are shared equally between 4 tables. How many pencils does each table get?", "21",
         ["24", "12", "80"],
         "84 ÷ 4. Partition 84 = 80 + 4. 80 ÷ 4 = 20 and 4 ÷ 4 = 1. Add: 20 + 1 = <b>21</b>. Check: 21 × 4 = 84."),
        ("Ethan shares 39 kookaburra stickers equally among 3 friends. How many stickers does each friend get?", "13",
         ["31", "36", "12"],
         "39 ÷ 3. Partition 39 = 30 + 9. 30 ÷ 3 = 10 and 9 ÷ 3 = 3. Add: 10 + 3 = <b>13</b>. Check: 13 × 3 = 39."),
        ("Charlotte reads 5 pages each night. How many nights does it take her to read a 60-page book?", "12",
         ["55", "65", "300"],
         "How many 5s make 60? 60 ÷ 5. Partition 60 = 50 + 10. 50 ÷ 5 = 10 and 10 ÷ 5 = 2. Add: 10 + 2 = <b>12</b> nights."),
    ]
    for q, right, wrong, e in div:
        its.append(mcq(q, right, wrong, e))
    its.append(mcq("Jack buys 3 drinks at the school canteen. Each drink costs $2. He pays with a $10 note. How much change does he get?",
                   "$4", ["$6", "$7", "$16"],
                   "Step 1: cost: 3 × $2 = $6. Step 2: change: $10 − $6 = <b>$4</b>. ($6 is the cost, not the change.)"))
    its.append(mcq("The teacher buys 4 packs of 23 markers. The class uses 40 markers. How many markers are left?",
                   "52", ["92", "42", "132"],
                   "Step 1: 4 × 23 = 80 + 12 = 92 markers. Step 2: 92 − 40 = <b>52</b> markers are left."))
    its.append(mcq("Isla has 3 bags with 12 marbles in each bag. She shares all the marbles equally among 4 friends. How many marbles does each friend get?",
                   "9", ["36", "4", "12"],
                   "Step 1: 3 × 12 = 36 marbles. Step 2: 36 ÷ 4 = <b>9</b>, because 9 × 4 = 36."))
    its.append(mcq("At assembly there are 3 rows of 8 chairs and 2 rows of 10 chairs. How many chairs are there?",
                   "44", ["23", "48", "40"],
                   "Step 1: 3 × 8 = 24 and 2 × 10 = 20. Step 2: 24 + 20 = <b>44</b> chairs."))
    assert len(its) == 20, len(its)
    return {"title": "Multiplying and dividing word problems", "items": its}


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
        "<h2>Arrays and number sentences</h2>"
        "<p>An <b>array</b> is objects in equal rows. Count the rows, then count one row. Write a number sentence.</p>"
        "<figure class='sn-fig'>" + lesson_array_svg(3, 5) +
        "<figcaption>3 rows of 5: 5 + 5 + 5 = 15, so 3 × 5 = 15. Turn it around and it shows 5 × 3 = 15.</figcaption></figure>"
        "<p>The same array shows division too: 15 dots in 3 equal rows is 15 ÷ 3 = 5.</p>"
        "<h2>Multiply by partitioning</h2>"
        "<p>Use the facts you know to multiply bigger numbers. <b>Partition</b> the 2-digit number into tens and ones. "
        "Multiply each part. Then add the parts.</p>"
        "<figure class='sn-fig'>" + area_svg(23, 4, ["80", "12"], "area model: 23 × 4 split into 20 × 4 and 3 × 4") +
        "<figcaption>23 × 4 = 20 × 4 + 3 × 4 = 80 + 12 = 92.</figcaption></figure>"
        "<p>20 × 4 is 2 tens × 4 = 8 tens = 80. It is not 8.</p>" +
        ex("Partitioning", "34 × 5 = ?", "34 = 30 + 4. 30 × 5 = 150 and 4 × 5 = 20. Add: 150 + 20 = 170.", "170") +
        "<h2>Divide by sharing and grouping</h2>"
        "<p><b>Sharing:</b> you know how many groups. Give out one at a time. 12 shared between 3 plates is 4 on each plate.</p>"
        "<figure class='sn-fig'>" + groups_svg([4, 4, 4], "plate", "12 counters shared between 3 plates") +
        "<figcaption>Sharing: 12 ÷ 3 = 4 on each plate.</figcaption></figure>"
        "<p><b>Grouping:</b> you know how many in each group. 12 in groups of 3 makes 4 groups. Both are 12 ÷ 3 = 4.</p>"
        "<p>For bigger numbers, partition into parts you can divide. Divide each part, then add.</p>"
        "<figure class='sn-fig'>" + split_svg(48, 40, 8, 4, "48 partitioned into 40 and 8, each divided by 4") +
        "<figcaption>48 ÷ 4: 40 ÷ 4 = 10 and 8 ÷ 4 = 2. 10 + 2 = 12.</figcaption></figure>"
        "<p>Sometimes the tens do not divide equally. For 72 ÷ 3, use 72 = 60 + 12. 60 ÷ 3 = 20 and 12 ÷ 3 = 4, so 72 ÷ 3 = 24.</p>"
        "<h2>Remainders</h2>"
        "<p>Some numbers do not divide equally. The amount left over is the <b>remainder</b>.</p>"
        "<figure class='sn-fig'>" + rem_svg(17, 5) +
        "<figcaption>17 ÷ 5 = 3 r 2: 3 groups of 5, with 2 left over.</figcaption></figure>"
        "<p>In a story, think about the remainder. 26 students at tables of 4 need 7 tables, not 6, so nobody misses out.</p>"
        "<h2>Choose the number sentence</h2>"
        "<p>Equal groups or “times as many”: multiply. Sharing equally or making equal groups from a total: divide. "
        "Joining or taking away with no equal groups: add or subtract.</p>"
        "<h2>Common mistakes</h2>" +
        table(["Mistake", "What to do instead"], [
            ["Treating 20 as 2 (20 × 4 = 8)", "20 × 4 = 2 tens × 4 = 8 tens = 80"],
            ["Writing the parts side by side (23 × 4 = 812)", "Add the parts: 80 + 12 = 92"],
            ["Losing the ten when adding the parts (80 + 12 = 82)", "12 is 1 ten and 2 ones, so 80 + 12 = 92"],
            ["Adding instead of multiplying (4 rows of 23 = 27)", "Equal rows mean multiply: 4 × 23 = 92"],
            ["Dividing only the tens (48 ÷ 4 = 18)", "Divide both parts: 40 ÷ 4 = 10 and 8 ÷ 4 = 2, so 12"],
            ["Mixing up sharing and grouping", "“Between 4” means 4 groups. “Groups of 4” means 4 in each group"],
        ])
    )


FAQ = [
    {"q": "What multiplication should a Year 3 student know in Australia?",
     "a": "Year 3 students learn the multiplication facts for 3, 4, 5 and 10 and the related division facts. They use these facts to multiply and divide one- and two-digit numbers, such as 23 × 4 or 48 ÷ 4, with arrays, diagrams and partitioning."},
    {"q": "What is the difference between sharing and grouping in division?",
     "a": "In sharing you know the number of groups and find how many go in each, like 12 shared between 3 plates. In grouping you know how many go in each group and find the number of groups, like 12 in groups of 3. Both give 12 ÷ 3 = 4."},
    {"q": "How do you teach 2-digit by 1-digit multiplication in Year 3?",
     "a": "Partition the 2-digit number into tens and ones, multiply each part, then add. For 23 × 4: 20 × 4 = 80 and 3 × 4 = 12, so 80 + 12 = 92. An area model or array helps students see why it works."},
    {"q": "Is multiplication and division on the Year 3 NAPLAN numeracy test?",
     "a": "Yes. NAPLAN numeracy in Year 3 tests the number skills of the Australian Curriculum, which include multiplying and dividing with equal groups, arrays and simple word problems. Practising mixed word problems like the ones on this page is good preparation."},
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
    rnd = random.Random(3805)
    sets = [set_arrays(), set_partition(rnd), set_divide(), set_choose(), set_story()]
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
        "country": "au", "subject": "maths", "grade": "year-3", "slug": "multiplying-and-dividing", "sort": 5,
        "updated": UPDATED, "pdf_url": "",
        "title": "Multiplying and Dividing",
        "seo_title": "Year 3 Multiplying and Dividing Worksheets: Arrays, Partitioning, Sharing and Grouping (Free)",
        "short_title": "Multiplying and dividing",
        "domain": "Number",
        "standard_code": "AC9M3N04",
        "standard_url": "https://v9.australiancurriculum.edu.au/f-10-curriculum/learning-areas/mathematics",
        "standard_text": "Multiply and divide one- and two-digit numbers, representing problems using number sentences, diagrams and arrays, and using a variety of calculation strategies",
        "meta_desc": "Free Year 3 maths worksheets on multiplying and dividing, following the Australian Curriculum (AC9M3N04): arrays and number sentences, 2-digit × 1-digit by partitioning, sharing and grouping, remainders and word problems. 100 questions with an answer key, great for NAPLAN practice.",
        "key_big": "Partition the 2-digit number. Multiply or divide each part, then add the answers.",
        "key_sub": "23 × 4 = 20 × 4 + 3 × 4 = 80 + 12 = 92. 48 ÷ 4 = 40 ÷ 4 + 8 ÷ 4 = 10 + 2 = 12. Sharing: you know the number of groups. Grouping: you know how many in each group.",
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
