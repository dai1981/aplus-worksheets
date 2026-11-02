# -*- coding: utf-8 -*-
"""
CA Grade 1 Math: Counting and estimating to 50 (Ontario Mathematics Curriculum 2020, Grade 1: B1.5, also B1.4)
  python3 tools/gen_caon_math_g1_counting.py
HTML attributes use single quotes (no backslashes in the JSON).
Grade 1: whole numbers to 50, very short sentences for 6-7 year olds, a picture in almost every question
(number tracks, apples, mitts, hands, nickels, ten frames, tally marks, number lines, jars of marbles).
Wrong answers come from real mistakes: skipping a number, saying a number twice, going the wrong way,
changing the step partway (2, 4, 6, 7), writing "twenty-ten" as 210 after 29, writing digits backwards
(14 as 41), counting the pairs or groups instead of the things, counting the start as a jump,
missing or adding one group, and wild estimates.
"""
import json, os, random, re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "ca-on", "math", "grade-1")
UPDATED = "2026-11-02"
GREEN = "#006633"
FILL = "#cfe6d6"
LIGHT = "#e8f3ec"
RED = "#c0392b"
BLUE = "#2e6da4"
GREY = "#9a9a9a"
INK = "#2b2b2b"
SKIN = "#f3d9bd"
FONT = "Arial, Helvetica, sans-serif"
GIRLS = ["Olivia", "Emma", "Maya", "Zoe", "Amira", "Mei", "Chloe", "Priya", "Leah", "Hana", "Ava", "Sofia"]
BOYS = ["Liam", "Noah", "Aiden", "Lucas", "Owen", "Arjun", "Ethan", "Jayden", "Benjamin", "Mateo", "Nathan", "Kai"]
# wrong answers above 60 that show a real mistake ("twenty-ten" written as 210, digits written backwards)
BIG_OK = {210, 310, 410, 62, 63, 64, 71, 72, 100}


# ------------------------------------------------------------ helpers
def mcq(q, correct, wrong, e):
    correct = str(correct)
    wrong = [str(w) for w in wrong]
    assert len(wrong) == 3 and len(set(wrong + [correct])) == 4, (q, correct, wrong)
    for c in [correct] + wrong:
        for tok in re.findall(r"\d+", c):
            v = int(tok)
            assert 0 <= v <= 60 or v in BIG_OK, (q, c)
    return {"q": q, "c": [correct] + wrong, "a": 0, "e": e}


def balance(sets, rnd):
    """Move the correct choice so each position (A to D) is the answer 5 times in every set."""
    for st in sets:
        pos = [0, 1, 2, 3] * 5
        rnd.shuffle(pos)
        for it, t in zip(st["items"], pos):
            ch = it["c"]
            wrong = [x for i, x in enumerate(ch) if i != it["a"]]
            rnd.shuffle(wrong)
            it["c"] = wrong[:t] + [ch[it["a"]]] + wrong[t:]
            it["a"] = t
        assert [sum(1 for it in st["items"] if it["a"] == i) for i in range(4)] == [5, 5, 5, 5]


class People:
    def __init__(self, rnd):
        self.pool = [(n, "she", "her") for n in GIRLS] + [(n, "he", "his") for n in BOYS]
        rnd.shuffle(self.pool)
        self.i = 0

    def next(self):
        nm, he, his = self.pool[self.i % len(self.pool)]
        self.i += 1
        return dict(n=nm, he=he, He=he.capitalize(), his=his)


def fig(svg):
    return "<div class='qfig'>" + svg + "</div>"


def svg_wrap(w, h, body, label, large=False):
    return ("<svg %sxmlns='http://www.w3.org/2000/svg' viewBox='0 0 %d %d' width='%d' height='%d' "
            "role='img' aria-label='%s'><g font-family='%s'>%s</g></svg>"
            % ("data-pf='lg' " if large else "", w, h, w, h, label, FONT, body))


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


def lst(xs):
    return ", ".join(str(x) for x in xs)


def counts(start, step, n):
    return [start + step * k for k in range(n)]


def rows_of(n, per):
    """Split n things into rows of at most `per`, as even as possible (7 -> 4 + 3)."""
    r = (n + per - 1) // per
    base, extra = divmod(n, r)
    return [base + (1 if i < extra else 0) for i in range(r)]


def grid(n, per, w, h, gx, gy, m, draw, fixed=False):
    """Lay out n tiles of w x h in rows of `per` (fixed=True: full rows of `per`, last row shorter)."""
    rows = [per] * (n // per) + ([n % per] if n % per else []) if fixed else rows_of(n, per)
    W = 2 * m + max(rows) * w + (max(rows) - 1) * gx
    H = 2 * m + len(rows) * h + (len(rows) - 1) * gy
    s, i = [], 0
    for r, k in enumerate(rows):
        for c in range(k):
            s.append(draw(i, m + c * (w + gx), m + r * (h + gy)))
            i += 1
    assert i == n
    return "".join(s), W, H


# ------------------------------------------------------------ pictures
def track_svg(cells, label="number track"):
    """Number track. cells: numbers or '?'."""
    w, h, m = 48, 42, 3
    s = []
    for i, v in enumerate(cells):
        q = v == "?"
        x = m + i * w
        s.append("<rect x='%d' y='%d' width='%d' height='%d' fill='%s' stroke='%s' stroke-width='2'/>"
                 % (x, m, w, h, FILL if q else "#ffffff", GREEN))
        s.append(text(x + w / 2.0, m + 28, str(v), 20, col=RED if q else INK))
    return svg_wrap(2 * m + len(cells) * w, 2 * m + h, "".join(s), label, large=len(cells) > 5)


def apple(cx, cy):
    return ("<circle cx='%.1f' cy='%.1f' r='9.5' fill='%s'/>"
            "<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='2.2'/>"
            "<ellipse cx='%.1f' cy='%.1f' rx='4' ry='2.2' fill='%s'/>"
            % (cx, cy + 2, RED, cx, cy - 6, cx + 2, cy - 12, GREEN, cx + 6, cy - 10, GREEN))


def apples_svg(n):
    body, W, H = grid(n, 5, 26, 28, 4, 4, 5, lambda i, x, y: apple(x + 13, y + 15), fixed=True)
    return svg_wrap(W, H, body, "%d apples in rows of 5" % n)


def mitt(x, y, left):
    """One winter mitt in a 26 x 40 box. left=True puts the thumb on the left."""
    bx = x + (6 if left else 2)
    tx = x + 1 if left else x + 19
    return ("<rect x='%.1f' y='%.1f' width='7' height='15' rx='3.5' fill='%s' stroke='%s' stroke-width='1.5' "
            "transform='rotate(%d %.1f %.1f)'/>" % (tx, y + 10, FILL, GREEN, -25 if left else 25, tx + 3.5, y + 24)
            + "<rect x='%.1f' y='%.1f' width='18' height='30' rx='9' fill='%s' stroke='%s' stroke-width='1.5'/>"
            % (bx, y, FILL, GREEN)
            + "<rect x='%.1f' y='%.1f' width='18' height='8' rx='2' fill='%s' stroke='%s' stroke-width='1.5'/>"
            % (bx, y + 31, GREEN, GREEN))


def mitts_svg(pairs):
    def draw(i, x, y):
        return ("<rect x='%d' y='%d' width='62' height='50' rx='9' fill='none' stroke='%s' stroke-width='1.5' "
                "stroke-dasharray='4 3'/>" % (x, y, GREY) + mitt(x + 4, y + 5, True) + mitt(x + 32, y + 5, False))
    body, W, H = grid(pairs, 4, 62, 50, 8, 8, 4, draw)
    return svg_wrap(W, H, body, "%d pairs of mitts" % pairs, large=pairs > 4)


def hand(x, y):
    """One hand, 4 fingers and a thumb, in a 40 x 58 box."""
    s = []
    for k, top in enumerate([10, 3, 5, 12]):
        s.append("<rect x='%.1f' y='%.1f' width='6.5' height='%d' rx='3.2' fill='%s' stroke='%s' stroke-width='1.5'/>"
                 % (x + 11 + k * 7, y + top, 36 - top, SKIN, "#9a6a3a"))
    s.append("<rect x='%.1f' y='%.1f' width='7' height='20' rx='3.5' fill='%s' stroke='%s' stroke-width='1.5' "
             "transform='rotate(-38 %.1f %.1f)'/>" % (x + 6, y + 22, SKIN, "#9a6a3a", x + 9.5, y + 42))
    s.append("<rect x='%.1f' y='%.1f' width='30' height='26' rx='8' fill='%s' stroke='%s' stroke-width='1.5'/>"
             % (x + 9, y + 30, SKIN, "#9a6a3a"))
    return "".join(s)


def hands_svg(n):
    body, W, H = grid(n, 5, 40, 58, 10, 8, 6, lambda i, x, y: hand(x, y))
    return svg_wrap(W, H, body, "%d hands" % n, large=n > 4)


def nickel(cx, cy):
    r = 21
    return ("<circle cx='%.1f' cy='%.1f' r='%d' fill='#dfe3e7' stroke='#7a828a' stroke-width='2'/>"
            "<circle cx='%.1f' cy='%.1f' r='%d' fill='none' stroke='#9aa2aa' stroke-width='1'/>"
            % (cx, cy, r, cx, cy, r - 4) + text(cx, cy + 6, "5¢", 16))


def nickels_svg(n):
    body, W, H = grid(n, 5, 42, 42, 8, 8, 4, lambda i, x, y: nickel(x + 21, y + 21))
    return svg_wrap(W, H, body, "%d nickels" % n, large=n > 5)


def ten_frame(x, y, k=10):
    s = ["<rect x='%d' y='%d' width='110' height='44' fill='#ffffff' stroke='%s' stroke-width='2'/>" % (x, y, GREEN)]
    for c in range(1, 5):
        s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='1.2'/>"
                 % (x + 22 * c, y, x + 22 * c, y + 44, GREEN))
    s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='1.2'/>" % (x, y + 22, x + 110, y + 22, GREEN))
    for j in range(k):
        r, c = divmod(j, 5)
        s.append("<circle cx='%d' cy='%d' r='8' fill='%s'/>" % (x + 11 + 22 * c, y + 11 + 22 * r, RED))
    return "".join(s)


def frames_svg(full, last=0):
    """`full` full ten frames, then one more frame with `last` counters (if last > 0)."""
    n = full + (1 if last else 0)
    body, W, H = grid(n, 3, 110, 44, 12, 10, 4, lambda i, x, y: ten_frame(x, y, last if i == full else 10))
    label = ("%d full ten frame" if full == 1 else "%d full ten frames") % full + (" and a ten frame with %d" % last if last else "")
    return svg_wrap(W, H, body, label, large=n > 2)


def tally_svg(groups):
    """Tally marks: groups of 5 (4 sticks and a slash)."""
    s, gx = [], 10
    for g in range(groups):
        for k in range(4):
            s.append("<line x1='%d' y1='8' x2='%d' y2='42' stroke='%s' stroke-width='3' stroke-linecap='round'/>"
                     % (gx + 4 + k * 9, gx + 4 + k * 9, INK))
        s.append("<line x1='%d' y1='36' x2='%d' y2='14' stroke='%s' stroke-width='3' stroke-linecap='round'/>"
                 % (gx - 2, gx + 37, RED))
        gx += 50
    return svg_wrap(gx - 50 + 39 + 10, 50, "".join(s), "tally marks, %d groups of 5" % groups, large=groups > 4)


def counter_groups_svg(sizes, label):
    """Groups of counters, each group in a box (5 in a row inside a box)."""
    S = 22
    bh = max((k + 4) // 5 for k in sizes) * S + 12
    per = 5 if max(sizes) <= 2 else (4 if max(sizes) <= 5 else 2)
    rows = [sizes[i:i + per] for i in range(0, len(sizes), per)]
    s, W = [], 0
    for r, row in enumerate(rows):
        x = 4
        for k in row:
            cols = min(k, 5)
            bw = cols * S + 12
            y = 4 + r * (bh + 10)
            s.append("<rect x='%d' y='%d' width='%d' height='%d' rx='10' fill='%s' stroke='%s' stroke-width='2'/>"
                     % (x, y, bw, bh, LIGHT, GREEN))
            for j in range(k):
                rr, c = divmod(j, cols)
                s.append("<circle cx='%.1f' cy='%.1f' r='8' fill='%s'/>" % (x + 6 + c * S + S / 2.0, y + 6 + rr * S + S / 2.0, GREEN))
            x += bw + 10
        W = max(W, x - 10 + 4)
    H = 4 + len(rows) * (bh + 10) - 10 + 4
    return svg_wrap(W, H, "".join(s), label, large=W > 260)


def chart_svg(tl, nrows, ncols, target, hide=()):
    """A piece of the number chart (1 to 50, 10 in a row). target (r, c) shows a red ?, hide = blank cells."""
    assert (tl - 1) % 10 + ncols <= 10, "piece must stay inside one row of the chart"
    assert tl + 10 * (nrows - 1) + ncols - 1 <= 50
    m, CW, CH = 4, 46, 36
    W, H = 2 * m + ncols * CW, 2 * m + nrows * CH
    s = []
    for r in range(nrows):
        for c in range(ncols):
            x, y = m + c * CW, m + r * CH
            isT = (r, c) == target
            s.append("<rect x='%d' y='%d' width='%d' height='%d' fill='%s' stroke='%s' stroke-width='1.5'/>"
                     % (x, y, CW, CH, FILL if isT else "#ffffff", GREEN))
            if isT:
                s.append(text(x + CW / 2, y + 25, "?", 18, col=RED))
            elif (r, c) not in hide:
                s.append(text(x + CW / 2, y + 25, str(tl + 10 * r + c), 17))
    return svg_wrap(W, H, "".join(s), "number chart piece")


def shade_chart_svg(lo, hi, shaded):
    """Rows of the number chart from lo to hi (10 a row); `shaded` numbers are coloured."""
    w, h, m = 32, 30, 3
    s = []
    for v in range(lo, hi + 1):
        r, c = divmod(v - lo, 10)
        x, y = m + c * w, m + r * h
        s.append("<rect x='%d' y='%d' width='%d' height='%d' fill='%s' stroke='%s' stroke-width='1.2'/>"
                 % (x, y, w, h, "#f6d7a6" if v in shaded else "#ffffff", GREEN))
        s.append(text(x + w / 2.0, y + 20, str(v), 15))
    rows = (hi - lo) // 10 + 1
    return svg_wrap(2 * m + 10 * w, 2 * m + rows * h, "".join(s),
                    "number chart from %d to %d with some numbers coloured" % (lo, hi), large=True)


def jw(j):
    j = abs(j)
    return 74 if j >= 10 else 64 if j >= 5 else 52


def nline_svg(start, jumps, ticks=None):
    """Open number line. Jumps go right for +, left for −. ticks: one label per point (None = no label)."""
    if ticks is None:
        ticks = [str(start)] + [None] * (len(jumps) - 1) + ["?"]
    jlabels = [("+%d" % j) if j > 0 else ("−%d" % -j) for j in jumps]
    m, ry, ly = 30, 22, 48
    W = 2 * m + sum(jw(j) for j in jumps)
    H = ly + 32
    xs = [m] if jumps[0] > 0 else [W - m]
    for j in jumps:
        xs.append(xs[-1] + (jw(j) if j > 0 else -jw(j)))
    s = ["<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='2.5'/>" % (m - 18, ly, W - m + 18, ly, INK)]
    for k, j in enumerate(jumps):
        x1, x2 = xs[k], xs[k + 1]
        rx = abs(x2 - x1) / 2
        s.append("<path d='M %d %d A %.1f %d 0 0 %d %d %d' fill='none' stroke='%s' stroke-width='2.5'/>"
                 % (x1, ly, rx, ry, 1 if x2 > x1 else 0, x2, ly, GREEN))
        s.append("<polyline points='%d,%d %d,%d %d,%d' fill='none' stroke='%s' stroke-width='2.5' "
                 "stroke-linejoin='round'/>" % (x2 - 5, ly - 10, x2, ly - 2, x2 + 5, ly - 10, GREEN))
        s.append(text((x1 + x2) / 2, ly - ry - 6, jlabels[k], 15, col=GREEN))
    for x, t in zip(xs, ticks):
        s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='2'/>" % (x, ly - 6, x, ly + 6, INK))
        if t is not None:
            s.append(text(x, ly + 24, t, 16, col=RED if t == "?" else INK))
    return svg_wrap(W, H, "".join(s), "open number line starting at %d with jumps of %s" % (
        start, ", ".join(jlabels).replace("−", "minus ")), large=True)


def step_line_svg(start, step, n, labels):
    """Number line with n evenly spaced ticks, `step` apart. labels: {index: text}. Checks every number label."""
    for k, t in labels.items():
        assert t == "?" or int(t) == start + step * k, (start, step, k, t)
    m, sp, ly = 30, 50, 14
    W = 2 * m + (n - 1) * sp
    H = ly + 34
    s = ["<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='2.5'/>" % (6, ly, W - 6, ly, INK),
         "<polyline points='%d,%d %d,%d %d,%d' fill='none' stroke='%s' stroke-width='2.5'/>"
         % (14, ly - 6, 6, ly, 14, ly + 6, INK),
         "<polyline points='%d,%d %d,%d %d,%d' fill='none' stroke='%s' stroke-width='2.5'/>"
         % (W - 14, ly - 6, W - 6, ly, W - 14, ly + 6, INK)]
    for k in range(n):
        x = m + k * sp
        s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='2'/>" % (x, ly - 7, x, ly + 7, INK))
        if k in labels:
            t = labels[k]
            s.append(text(x, ly + 27, t, 16, col=RED if t == "?" else INK))
    return svg_wrap(W, H, "".join(s), "number line counting by %ds" % step, large=True)


def scatter_body(n, cols, rows, rnd, x0, y0, col=BLUE, cell=24):
    """n marbles in random cells of a cols x rows grid (one per cell, small wobble), so none overlap."""
    assert n <= cols * rows
    cells = rnd.sample(range(cols * rows), n)
    s = []
    for k in sorted(cells):
        r, c = divmod(k, cols)
        cx = x0 + c * cell + cell / 2.0 + rnd.uniform(-3, 3)
        cy = y0 + r * cell + cell / 2.0 + rnd.uniform(-3, 3)
        s.append("<circle cx='%.1f' cy='%.1f' r='8' fill='%s'/>" % (cx, cy, col))
    return "".join(s)


def scatter_svg(n, rnd):
    cols, rows = (12, 6) if n > 20 else (8, 4)
    body = scatter_body(n, cols, rows, rnd, 6, 6)
    W, H = 12 + cols * 24, 12 + rows * 24
    frame = "<rect x='2' y='2' width='%d' height='%d' rx='10' fill='%s' stroke='%s' stroke-width='1.5'/>" % (
        W - 4, H - 4, LIGHT, GREEN)
    return svg_wrap(W, H, frame + body, "%d marbles spread out" % n, large=n > 20)


def jars_svg(ref, n, rnd):
    """Two same-size jars: the left one has `ref` marbles and a label, the right one has n marbles and ?."""
    cols, rows, cell = 6, 6, 22
    jw_, jh = cols * cell + 12, rows * cell + 12
    s = []
    for k, (cnt, lab) in enumerate([(ref, str(ref)), (n, "?")]):
        x = 6 + k * (jw_ + 40)
        y = 16
        s.append("<rect x='%d' y='%d' width='%d' height='12' rx='3' fill='%s' stroke='%s' stroke-width='1.5'/>"
                 % (x + 20, y - 12, jw_ - 40, GREY, INK))
        s.append("<rect x='%d' y='%d' width='%d' height='%d' rx='16' fill='#ffffff' stroke='%s' stroke-width='2.5'/>"
                 % (x, y, jw_, jh, INK))
        # fill from the bottom up, so the jar looks like a real jar
        for c in range(cnt):
            r, cc = divmod(c, cols)
            cx = x + 6 + cc * cell + cell / 2.0
            cy = y + jh - 6 - r * cell - cell / 2.0
            s.append("<circle cx='%.1f' cy='%.1f' r='8.5' fill='%s'/>" % (cx, cy, BLUE))
        s.append(text(x + jw_ / 2.0, y + jh + 24, lab, 20, col=RED if lab == "?" else INK))
    W = 12 + 2 * jw_ + 40
    H = 16 + jh + 32
    return svg_wrap(W, H, "".join(s), "a jar with %d marbles and a jar with more marbles" % ref, large=True)


# ------------------------------------------------------------ question makers
def track_q(cells, prompt, ans, wrong, e):
    assert cells.count("?") == 1
    return mcq(fig(track_svg(cells)) + prompt, ans, wrong, e)


def next_q(xs, step, wrong, e):
    """xs = numbers shown; the next one is the answer. step < 0 counts back."""
    assert all(b - a == step for a, b in zip(xs, xs[1:]))
    ans = xs[-1] + step
    if abs(step) == 1:
        word = "Count back." if step < 0 else "Count on."
    else:
        word = ("Count back by %ds." if step < 0 else "Count by %ds.") % abs(step)
    return track_q(xs + ["?"], word + " What comes next?", ans, wrong, e)


def gap_q(xs, blank, step, wrong, e):
    assert all(b - a == step for a, b in zip(xs, xs[1:]))
    cells = [("?" if i == blank else x) for i, x in enumerate(xs)]
    if abs(step) == 1:
        word = "Count back." if step < 0 else "Count on."
    else:
        word = ("Count back by %ds." if step < 0 else "Count by %ds.") % abs(step)
    return track_q(cells, word + " What number is missing?", xs[blank], wrong, e)


def line_q(start, step, n, labels, wrong, e):
    k = [i for i, t in labels.items() if t == "?"][0]
    ans = start + step * k
    word = "The marks go up by 1." if step == 1 else "The marks go up by %d." % step
    q = fig(step_line_svg(start, step, n, labels)) + word + " What number goes at the ?"
    return mcq(q, ans, wrong, e)


def jumps_q(start, step, n, wrong):
    end = start + step * n
    pts = counts(start, step, n + 1)
    if step > 0:
        q = "Start at %d. Make the jumps. Where do you land?" % start
        e = "Each jump is +%d. Say a number for each jump: %s. You land on <b>%d</b>." % (step, lst(pts[1:]), end)
    else:
        q = "Start at %d. Jump back. Where do you land?" % start
        e = "Each jump is back %d. Say a number for each jump: %s. You land on <b>%d</b>." % (-step, lst(pts[1:]), end)
    assert 0 <= end <= 50
    return mcq(fig(nline_svg(start, [step] * n)) + q, end, wrong, e)


def chart_q(tl, rows, cols, tgt, hide, wrong, how):
    ans = tl + 10 * tgt[0] + tgt[1]
    q = fig(chart_svg(tl, rows, cols, tgt, hide)) + "This is part of a number chart. What number goes at the ?"
    return mcq(q, ans, wrong, how.replace("ANS", "<b>%d</b>" % ans))


# ============================================================ set 1: count on and back by 1s
def set_ones():
    S = {}
    S["a"] = next_q([3, 4, 5, 6], 1, [8, 6, 5], "Each number is 1 more. After 6 comes <b>7</b>. 8 skips a number.")
    S["b"] = next_q([11, 12, 13], 1, [15, 13, 41], "After 13 comes <b>14</b>. Write 1 ten and 4 ones: 14, not 41.")
    S["c"] = mcq(fig(apples_svg(12)) + "How many apples?", 12, [11, 13, 21],
                 "Touch each apple once. The rows have 5, 5 and 2: 5, 10, 11, 12. There are <b>12</b> apples.")
    S["d"] = next_q([10, 9, 8], -1, [9, 6, 8], "Count back: each number is 1 less. After 8 comes <b>7</b>.")
    S["e"] = line_q(40, 1, 7, {0: "40", 3: "?", 6: "46"}, [42, 44, 34],
                    "Count on by 1s from 40: 41, 42, <b>43</b>.")
    S["f"] = next_q([17, 18, 19], 1, [21, 19, 18], "After 19 comes <b>20</b>. 9 ones and 1 more make a new ten.")
    S["g"] = mcq(fig(apples_svg(17)) + "How many apples?", 17, [16, 18, 71],
                 "Count each row by 5s, then by 1s: 5, 10, 15, 16, 17. There are <b>17</b> apples.")
    S["h"] = jumps_q(15, 1, 3, [17, 19, 12])
    S["i"] = next_q([25, 24, 23], -1, [21, 23, 24], "Count back: 1 less each time. After 23 comes <b>22</b>.")
    S["j"] = mcq(fig(frames_svg(1, 3)) + "How many counters? Count on from 10.", 13, [3, 12, 14],
                 "The full ten frame is 10. Count on: 11, 12, <b>13</b>.")
    S["k"] = chart_q(33, 1, 5, (0, 3), (), [35, 37, 63],
                     "Count on by 1s: 33, 34, 35, ANS, 37.")
    S["l"] = next_q([27, 28, 29], 1, [31, 29, 210],
                    "After 29 comes <b>30</b>. We say “thirty”, not “twenty-ten”. Do not write 210.")
    S["m"] = next_q([32, 31, 30], -1, [20, 39, 31],
                    "Just before 30 is <b>29</b>. 20 is 10 less, not 1 less.")
    S["n"] = next_q([37, 38, 39], 1, [41, 30, 310],
                    "After 39 comes <b>40</b>. 9 ones and 1 more make a new ten. Do not write 310.")
    S["o"] = track_q(["?", 20, 21, 22], "What number comes just before 20?", 19, [21, 10, 18],
                     "Count back 1 from 20: <b>19</b>. 21 comes just after 20.")
    S["p"] = jumps_q(34, -1, 4, [31, 38, 29])
    S["q"] = line_q(20, 1, 7, {0: "20", 4: "?", 6: "26"}, [23, 25, 42],
                    "Count on by 1s from 20: 21, 22, 23, <b>24</b>.")
    S["r"] = mcq(fig(apples_svg(23)) + "How many apples?", 23, [22, 24, 32],
                 "Each row has 5. Count by 5s: 5, 10, 15, 20. Then 21, 22, 23. There are <b>23</b> apples.")
    S["s"] = next_q([46, 47, 48, 49], 1, [51, 49, 410],
                    "After 49 comes <b>50</b>. We say “fifty”, not “forty-ten”.")
    S["t"] = chart_q(44, 1, 5, (0, 0), (), [43, 45, 54],
                     "The number after it is 45. Count back 1: ANS.")
    order = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j",
             "k", "l", "m", "n", "o", "p", "q", "r", "s", "t"]
    assert len(order) == 20 and set(order) == set(S)
    return {"title": "Count on and back by 1s", "items": [S[k] for k in order]}


# ============================================================ set 2: count by 2s
def set_twos():
    S = {}

    def mitts(key, n, wrong):
        S[key] = mcq(fig(mitts_svg(n)) + "Count by 2s. How many mitts?", 2 * n, wrong,
                     "A pair is 2 mitts. Count by 2s, one pair at a time: %s. There are <b>%d</b> mitts."
                     % (lst(counts(2, 2, n)), 2 * n))
    mitts("M1", 3, [3, 4, 8])
    mitts("M2", 5, [5, 8, 12])
    mitts("M3", 7, [7, 12, 16])
    mitts("M4", 9, [9, 16, 20])
    mitts("M5", 12, [12, 22, 26])
    S["P"] = mcq(fig(mitts_svg(6)) + "Each box holds a pair. How many pairs?", 6, [12, 3, 7],
                 "Count the boxes: 1, 2, 3, 4, 5, 6. There are <b>6</b> pairs. 12 is the number of mitts.")
    S["s1"] = next_q([2, 4, 6], 2, [7, 10, 5], "Each number is 2 more. 6 and 2 more is <b>8</b>. 7 is counting by 1s.")
    S["s2"] = next_q([10, 12, 14], 2, [15, 18, 41], "Each number is 2 more. 14 and 2 more is <b>16</b>.")
    S["s3"] = next_q([20, 22, 24], 2, [25, 28, 62], "Each number is 2 more. 24 and 2 more is <b>26</b>.")
    S["s4"] = next_q([20, 18, 16], -2, [15, 12, 18], "Count back by 2s: 2 less each time. 16, then <b>14</b>.")
    S["s5"] = next_q([36, 38, 40], 2, [41, 44, 50], "Each number is 2 more. 40 and 2 more is <b>42</b>. 41 is counting by 1s.")
    S["s6"] = next_q([44, 46, 48], 2, [49, 52, 410], "48 and 2 more is <b>50</b>. 8 ones and 2 more make a new ten.")
    S["s7"] = next_q([50, 48, 46], -2, [45, 42, 40], "Count back by 2s: 2 less each time. 46, then <b>44</b>.")
    S["s8"] = next_q([1, 3, 5], 2, [6, 8, 9], "Each number is 2 more. 5 and 2 more is <b>7</b>. 6 is counting by 1s.")
    S["L1"] = line_q(0, 2, 7, {0: "0", 1: "2", 4: "?"}, [5, 6, 10],
                     "Count by 2s: 0, 2, 4, 6, <b>8</b>.")
    S["L2"] = line_q(30, 2, 7, {0: "30", 1: "32", 5: "?"}, [35, 38, 42],
                     "Count by 2s: 30, 32, 34, 36, 38, <b>40</b>.")
    S["J1"] = jumps_q(10, 2, 3, [13, 14, 18])
    S["J2"] = jumps_q(30, 2, 4, [34, 36, 40])
    S["C"] = mcq(fig(shade_chart_svg(21, 40, {22, 24, 26, 28, 30})) +
                 "The coloured numbers count by 2s. What is the next coloured number after 30?", 32, [31, 33, 40],
                 "Count by 2s: 22, 24, 26, 28, 30, <b>32</b>. Skip 31.")
    S["W"] = mcq("Which list counts by 2s?", "2, 4, 6, 8", ["2, 4, 6, 7", "2, 4, 5, 6", "1, 2, 3, 4"],
                 "Each number must be 2 more: <b>2, 4, 6, 8</b>. In 2, 4, 6, 7 the last jump is only 1.")
    order = ["M1", "s1", "M2", "L1", "s2", "J1", "M3", "s8", "P", "s3",
             "s4", "C", "M4", "L2", "s5", "W", "J2", "s7", "s6", "M5"]
    assert len(order) == 20 and set(order) == set(S)
    return {"title": "Count by 2s (pairs of mitts)", "items": [S[k] for k in order]}


# ============================================================ set 3: count by 5s and 10s
def set_fives_tens():
    S = {}

    def hands(key, n, wrong):
        S[key] = mcq(fig(hands_svg(n)) + "Count by 5s. How many fingers?", 5 * n, wrong,
                     "Each hand has 5 fingers. Count by 5s: %s. There are <b>%d</b> fingers." % (lst(counts(5, 5, n)), 5 * n))

    def nickels(key, n, wrong):
        S[key] = mcq(fig(nickels_svg(n)) + "A nickel is 5¢. How much money is this?", "%d¢" % (5 * n),
                     ["%d¢" % w for w in wrong],
                     "Count by 5s, one nickel at a time: %s. That is <b>%d¢</b>." % (lst(counts(5, 5, n)), 5 * n))

    def frames(key, n, wrong):
        S[key] = mcq(fig(frames_svg(n)) + "Each ten frame holds 10. How many counters?", 10 * n, wrong,
                     "Count by 10s, one frame at a time: %s. There are <b>%d</b> counters." % (lst(counts(10, 10, n)), 10 * n))
    hands("H1", 2, [2, 5, 15])
    hands("H2", 4, [4, 15, 25])
    hands("H3", 6, [6, 25, 35])
    nickels("N1", 3, [3, 10, 20])
    nickels("N2", 5, [5, 20, 30])
    nickels("N3", 7, [7, 30, 40])
    frames("F1", 2, [2, 12, 30])
    frames("F2", 4, [4, 30, 50])
    S["F3"] = mcq(fig(frames_svg(3, 4)) + "How many counters? Count by 10s, then by 1s.", 34, [7, 33, 43],
                  "Count the full frames by 10s: 10, 20, 30. Then count on 4: 31, 32, 33, 34. There are <b>34</b>.")
    S["T"] = mcq(fig(tally_svg(4)) + "Each group is 5. How many tally marks?", 20, [4, 16, 25],
                 "Count by 5s, one group at a time: 5, 10, 15, 20. There are <b>20</b> marks. "
                 "Do not forget the line across: it is the 5th mark.")
    S["s1"] = next_q([5, 10, 15], 5, [16, 25, 30], "Each number is 5 more. 15 and 5 more is <b>20</b>. 16 is counting by 1s.")
    S["s2"] = next_q([10, 20, 30], 10, [31, 35, 50], "Each number is 10 more. 30 and 10 more is <b>40</b>.")
    S["s3"] = next_q([50, 45, 40], -5, [39, 30, 45], "Count back by 5s: 5 less each time. 40, then <b>35</b>.")
    S["s4"] = next_q([25, 30, 35], 5, [36, 45, 30], "Each number is 5 more. 35 and 5 more is <b>40</b>.")
    S["s5"] = next_q([50, 40, 30], -10, [29, 10, 25], "Count back by 10s: 10 less each time. 30, then <b>20</b>.")
    S["L5"] = line_q(0, 5, 7, {0: "0", 1: "5", 4: "?"}, [8, 15, 25],
                     "Count by 5s: 0, 5, 10, 15, <b>20</b>. Keep jumping by 5.")
    S["L10"] = line_q(0, 10, 6, {0: "0", 1: "10", 3: "?"}, [12, 20, 40],
                      "Count by 10s: 0, 10, 20, <b>30</b>.")
    S["J5"] = jumps_q(15, 5, 3, [18, 25, 35])
    S["J10"] = jumps_q(10, 10, 3, [13, 30, 50])
    S["W"] = mcq("Which list counts by 5s?", "5, 10, 15, 20", ["5, 10, 15, 16", "5, 10, 20, 30", "5, 6, 7, 8"],
                 "Each number must be 5 more: <b>5, 10, 15, 20</b>. In 5, 10, 20, 30 the step changes to 10.")
    order = ["H1", "s1", "F1", "N1", "s2", "H2", "F2", "L5", "s3", "N2",
             "T", "s4", "L10", "s5", "J5", "F3", "H3", "W", "N3", "J10"]
    assert len(order) == 20 and set(order) == set(S)
    return {"title": "Count by 5s and 10s (fingers, nickels, ten frames)", "items": [S[k] for k in order]}


# ============================================================ set 4: missing numbers and counting mistakes
def set_missing(P):
    S = {}
    S["g1"] = gap_q([12, 13, 14, 15], 2, 1, [16, 41, 13], "Count on: 12, 13, <b>14</b>, 15.")
    S["g2"] = gap_q([26, 27, 28, 29], 1, 1, [30, 72, 26], "Count on: 26, <b>27</b>, 28, 29.")
    S["g3"] = gap_q([22, 21, 20, 19], 2, -1, [18, 23, 10], "Count back: 22, 21, <b>20</b>, 19.")
    S["g4"] = gap_q([30, 32, 34, 36], 2, 2, [33, 35, 38], "Each number is 2 more: 30, 32, <b>34</b>, 36.")
    S["g5"] = gap_q([18, 20, 22, 24], 1, 2, [19, 21, 23], "Each number is 2 more: 18, <b>20</b>, 22, 24.")
    S["g6"] = gap_q([15, 20, 25, 30], 2, 5, [21, 35, 40], "Each number is 5 more: 15, 20, <b>25</b>, 30.")
    S["g7"] = gap_q([10, 20, 30, 40], 1, 10, [11, 25, 50], "Each number is 10 more: 10, <b>20</b>, 30, 40.")
    S["g8"] = gap_q([48, 47, 46, 45], 2, -1, [44, 49, 64], "Count back: 48, 47, <b>46</b>, 45.")
    S["g9"] = gap_q([40, 35, 30, 25], 2, -5, [34, 20, 45], "Count back by 5s: 40, 35, <b>30</b>, 25.")

    def told(key, xs, ask, ans, wrong, e):
        d = P.next()
        cells = [str(x) for x in xs]
        svg = track_svg(cells, "%s counts: %s" % (d["n"], ", ".join(cells)))
        S[key] = mcq(fig(svg) + ask.format(**d), ans, wrong, e.format(**d))
    told("k1", [21, 22, 24, 25], "{n} counts by 1s. Which number did {he} skip?", 23, [24, 26, 20],
         "After 22 comes 23, then 24. {He} skipped <b>23</b>.")
    told("k2", [4, 6, 8, 12], "{n} counts by 2s. Which number did {he} skip?", 10, [9, 11, 14],
         "8 and 2 more is 10, then 12. {He} skipped <b>10</b>.")
    told("k3", [5, 10, 20, 25], "{n} counts by 5s. Which number did {he} skip?", 15, [11, 30, 16],
         "10 and 5 more is 15, then 20. {He} skipped <b>15</b>.")
    told("k4", [31, 32, 33, 33, 34], "{n} counts by 1s. Which number did {he} say twice?", 33, [32, 34, 35],
         "{He} said <b>33</b> two times. Say each number only once: 31, 32, 33, 34.")
    told("k5", [5, 10, 15, 16], "{n} counts by 5s. What should {he} say after 15, not 16?", 20, [17, 25, 15],
         "{He} changed to 1s. Keep the step: 15 and 5 more is <b>20</b>.")
    told("k6", [10, 20, 30, 31], "{n} counts by 10s. What should {he} say after 30, not 31?", 40, [32, 50, 35],
         "{He} changed to 1s. Keep the step: 30 and 10 more is <b>40</b>.")
    rules = ["Count by 1s", "Count by 2s", "Count by 5s", "Count by 10s", "Count back by 1s"]
    for key, xs, right, e in [
        ("r1", [10, 20, 30, 40], "Count by 10s", "Each number is 10 more. The rule is <b>count by 10s</b>."),
        ("r2", [35, 40, 45, 50], "Count by 5s", "Each number is 5 more. The rule is <b>count by 5s</b>."),
        ("r3", [14, 16, 18, 20], "Count by 2s", "Each number is 2 more. The rule is <b>count by 2s</b>."),
        ("r4", [40, 39, 38, 37], "Count back by 1s", "Each number is 1 less. The rule is <b>count back by 1s</b>."),
    ]:
        step = xs[1] - xs[0]
        assert all(b - a == step for a, b in zip(xs, xs[1:]))
        assert right == ("Count back by %ds" % -step if step < 0 else "Count by %ds" % step)
        others = {"r1": ["Count by 1s", "Count by 5s", "Count by 2s"],
                  "r2": ["Count by 1s", "Count by 10s", "Count by 2s"],
                  "r3": ["Count by 1s", "Count by 5s", "Count by 10s"],
                  "r4": ["Count by 1s", "Count by 2s", "Count by 10s"]}[key]
        assert right in rules and all(o in rules for o in others)
        S[key] = mcq(fig(track_svg(xs, "number track: %s" % lst(xs))) + "What is the rule?", right, others, e)
    S["ch"] = chart_q(21, 2, 5, (1, 4), {(1, 1), (1, 2)}, [26, 34, 36],
                      "Count on along the row: 31, 32, 33, 34, ANS. Or look up: 25 and 10 more is 35.")
    order = ["g1", "g2", "r1", "g3", "k1", "g4", "g5", "r3", "k4", "g6",
             "g7", "r2", "k2", "g8", "k5", "ch", "g9", "k3", "r4", "k6"]
    assert len(order) == 20 and set(order) == set(S)
    return {"title": "Missing numbers and counting mistakes", "items": [S[k] for k in order]}


# ============================================================ set 5: estimate, then count, and word problems
def set_estimate(P, rnd):
    S = {}
    tens = ["about 10", "about 20", "about 30", "about 40", "about 50"]

    def est(key, n, wrong_tens):
        right = "about %d" % (10 * round(n / 10.0))
        assert abs(n - 10 * round(n / 10.0)) <= 2
        wrong = ["about %d" % w for w in wrong_tens]
        assert right in tens and all(w in tens for w in wrong)
        S[key] = mcq(fig(scatter_svg(n, rnd)) + "Do not count. Estimate. About how many marbles?", right, wrong,
                     "Look at how much space they fill. There are %d marbles, so <b>%s</b> is the best estimate." % (n, right))
    est("E1", 11, [20, 30, 40])
    est("E2", 19, [10, 30, 50])
    est("E3", 29, [10, 20, 50])
    est("E4", 41, [10, 20, 30])
    S["E5"] = mcq(fig(scatter_svg(48, rnd)) + "Which is the best estimate?", "50", ["5", "20", "100"],
                  "There are 48 marbles. <b>50</b> is close. 5 and 20 are too few. 100 is too many.")
    S["J"] = mcq(fig(jars_svg(10, 30, rnd)) + "The first jar has 10 marbles. About how many are in the other jar?",
                 "about 30", ["about 10", "about 50", "about 100"],
                 "The other jar looks like 3 jars of 10: 10, 20, 30. So <b>about 30</b>. "
                 "Then count to check. There are 30.")
    S["C1"] = mcq(fig(counter_groups_svg([2] * 11, "11 pairs of shells")) +
                  "Leah has some shells. She estimates 20. She counts by 2s to check. How many shells?", 22, [20, 11, 24],
                  "Count each pair by 2s: 2, 4, 6 … 20, 22. There are <b>22</b>. Her estimate was close.")
    S["C2"] = mcq(fig(frames_svg(3, 2)) + "Estimate first. Then count by 10s and 1s. How many counters?", 32,
                  [5, 23, 30],
                  "Count the full frames by 10s: 10, 20, 30. Then count on 2: 31, 32. There are <b>32</b>.")
    S["C3"] = mcq(fig(tally_svg(7)) + "Count by 5s to check. How many tally marks?", 35, [7, 30, 40],
                  "Count by 5s, one group at a time: %s. There are <b>35</b> marks." % lst(counts(5, 5, 7)))

    def story(key, t, ans, unit, wrong, e, pic=None):
        d = P.next()
        u = (lambda v: "%d%s" % (v, unit)) if unit == "¢" else (lambda v: "%d %s" % (v, unit))
        q = (fig(pic) if pic else "") + t.format(**d)
        S[key] = mcq(q, u(ans), [u(v) for v in wrong], e.format(**d))
    story("w1", "{n} sees 6 pairs of skates at the rink. How many skates are there?", 12, "skates", [6, 10, 14],
          "A pair is 2 skates. Count by 2s 6 times: 2, 4, 6, 8, 10, 12. There are <b>12</b> skates.")
    story("w2", "8 children hang up their mitts at recess. Each child has 2 mitts. How many mitts?", 16, "mitts",
          [8, 14, 18], "Count by 2s 8 times: 2, 4, 6, 8, 10, 12, 14, 16. There are <b>16</b> mitts.",
          pic=mitts_svg(8))
    story("w3", "{n} has 9 nickels. A nickel is 5¢. How much money does {he} have?", 45, "¢", [9, 40, 50],
          "Count by 5s 9 times: 5, 10, 15, 20, 25, 30, 35, 40, 45. That is <b>45¢</b>.")
    story("w4", "A box holds 10 crayons. {n} has 4 boxes. How many crayons?", 40, "crayons", [14, 30, 50],
          "Count by 10s, one box at a time: 10, 20, 30, 40. There are <b>40</b> crayons.",
          pic=counter_groups_svg([10] * 4, "4 groups of 10 crayons"))
    story("w5", "Canada geese fly by in groups of 5. {n} sees 6 groups. How many geese?", 30, "geese", [11, 25, 35],
          "Count by 5s, one group at a time: 5, 10, 15, 20, 25, 30. There are <b>30</b> geese.",
          pic=counter_groups_svg([5] * 6, "6 groups of 5 geese"))
    story("w6", "{n} has 50 stickers. {He} gives away 10 each day. How many are left after 2 days?", 30, "stickers",
          [48, 40, 20], "Count back by 10s 2 times: 50, 40, 30. {He} has <b>30</b> stickers left.")
    story("w7", "3 basketball teams practise in the gym. Each team has 5 players. How many players?", 15, "players",
          [8, 10, 20], "Count by 5s, one team at a time: 5, 10, 15. There are <b>15</b> players.",
          pic=counter_groups_svg([5] * 3, "3 groups of 5 players"))
    story("w8", "{n} picks apples. {He} fills 3 bags of 10. {He} has 4 more apples. How many apples?", 34, "apples",
          [7, 43, 30], "Count the bags by 10s: 10, 20, 30. Then count on 4: 31, 32, 33, 34. There are <b>34</b> apples.",
          pic=counter_groups_svg([10, 10, 10, 4], "3 groups of 10 apples and 4 more"))
    story("w9", "On a snow day, {n} makes 5 rows of snowballs. Each row has 10. How many snowballs?", 50, "snowballs",
          [15, 40, 60], "Count by 10s, one row at a time: 10, 20, 30, 40, 50. There are <b>50</b> snowballs.")
    story("w10", "There are 9 loons on the lake. Each loon has 2 wings. How many wings?", 18, "wings", [9, 11, 20],
          "Count by 2s 9 times: 2, 4, 6, 8, 10, 12, 14, 16, 18. There are <b>18</b> wings.")
    story("w11", "{n} counts back by 5s from 30 to blast off: 30, 25, 20. What does {he} say next?", 15, "", [19, 10, 25],
          "Count back by 5s: 30, 25, 20, then <b>15</b>. 19 is counting back by 1s.")
    # w11 has no unit word: tidy the choices
    for i, c in enumerate(S["w11"]["c"]):
        S["w11"]["c"][i] = c.strip()
    order = ["E1", "E2", "w1", "E3", "C1", "w2", "E4", "w3", "J", "w4",
             "C2", "w5", "E5", "w6", "C3", "w7", "w8", "w9", "w10", "w11"]
    assert len(order) == 20 and set(order) == set(S)
    return {"title": "Estimate, then count, and word problems", "items": [S[k] for k in order]}


# ============================================================ lesson
def body_html():
    return (
        "<h2>Count on and count back</h2>"
        "<p>To count on, say the next number. It is 1 more. To count back, say the number before. It is 1 less.</p>"
        "<figure class='sn-fig'>" + track_svg([27, 28, 29, 30, 31]) +
        "<figcaption>After 29 comes 30. We say “thirty”, not “twenty-ten”.</figcaption></figure>"
        "<h2>Skip counting by 2s, 5s and 10s</h2>"
        "<p>Skip counting is jumping by the same number each time. It is faster than counting by 1s.</p>"
        + table(["Count by", "Say", "Use"], [
            ["2s", "2, 4, 6, 8, 10", "pairs of mitts or boots"],
            ["5s", "5, 10, 15, 20, 25", "fingers on a hand, nickels, tally marks"],
            ["10s", "10, 20, 30, 40, 50", "full ten frames, both hands"],
        ]) +
        "<figure class='sn-fig'>" + mitts_svg(4) +
        "<figcaption>4 pairs of mitts: 2, 4, 6, 8. There are 8 mitts.</figcaption></figure>"
        "<figure class='sn-fig'>" + nickels_svg(5) +
        "<figcaption>A nickel is 5¢. 5, 10, 15, 20, 25. That is 25¢.</figcaption></figure>"
        + ex("Count by 10s", "How many counters? 3 full ten frames.",
             "Count one frame at a time: 10, 20, 30.", "30") +
        "<figure class='sn-fig'>" + frames_svg(3) +
        "<figcaption>3 full ten frames: 10, 20, 30.</figcaption></figure>"
        "<h2>Find the missing number</h2>"
        "<p>Find the jump first. Then use it to fill the gap.</p>"
        "<figure class='sn-fig'>" + track_svg([15, 20, "?", 30]) +
        "<figcaption>Each number is 5 more. 20 and 5 more is 25.</figcaption></figure>"
        "<h2>Estimate, then count</h2>"
        "<p>An estimate is a good guess. Do not count yet. Ask: is it closer to 10 or to 30? "
        "Then count to check.</p>"
        + ex("Estimate", "About how many marbles? Is it closer to 10 or to 30?",
             "They fill a lot of space. Then count by 2s to check: there are 28.", "about 30") +
        "<figure class='sn-fig'>" + scatter_svg(28, random.Random(7)) +
        "<figcaption>28 marbles. 28 is closer to 30 than to 10.</figcaption></figure>"
        "<h2>Common mistakes</h2>"
        + table(["Mistake", "What to do instead"], [
            ["Skipping a number: 21, 22, 24", "Say every number: 21, 22, 23, 24"],
            ["Saying a number twice: 33, 33", "Touch each thing only once"],
            ["Changing the step: 5, 10, 15, 16", "Keep the same jump: 5, 10, 15, 20"],
            ["Writing 210 after 29", "After 29 comes 30"],
            ["Counting pairs, not mitts: 4 pairs = 4", "Count by 2s: 4 pairs = 8 mitts"],
        ])
    )


FAQ = [
    {"q": "How high should a Grade 1 student count in Ontario?",
     "a": "In the Ontario Mathematics Curriculum (2020), Grade 1 students count to 50 by 1s, 2s, 5s and 10s (B1.5). They also count on and count back from any number up to 50."},
    {"q": "What is estimating in Grade 1 math?",
     "a": "Estimating is making a good guess about how many things there are without counting them all. Grade 1 students estimate collections up to 50 and then count to check (B1.4)."},
    {"q": "Why does my child say “twenty-ten” after 29?",
     "a": "They keep the ten and go on counting ones. Use a number chart or ten frames to show that 9 ones and 1 more make a new ten, so 29 is followed by 30."},
    {"q": "How can I practise counting to 50 at home?",
     "a": "Count real things in groups: pairs of mitts by 2s, nickels by 5s and egg cartons or ten frames by 10s. Before you count a pile, ask your child to estimate first, then count to check."},
]


def gen_unit():
    rnd = random.Random(41802)
    P = People(random.Random(418021))
    sets = [set_ones(), set_twos(), set_fives_tens(), set_missing(P), set_estimate(P, random.Random(418022))]
    balance(sets, rnd)
    seen = set()
    for s in sets:
        assert len(s["items"]) == 20, (s["title"], len(s["items"]))
        for it in s["items"]:
            assert len(set(it["c"])) == 4, it
            assert it["q"].count("<svg") <= 1
            key = it["q"] + "|" + "|".join(sorted(it["c"]))
            assert key not in seen, key
            seen.add(key)
            m = re.search(r"aria-label='(\d+) apples in rows", it["q"])
            if m:
                assert it["q"].count("r='9.5'") == int(m.group(1))
            m = re.search(r"aria-label='(\d+) marbles spread out", it["q"])
            if m:
                assert it["q"].count("r='8' fill='%s'" % BLUE) == int(m.group(1))
            m = re.search(r"aria-label='(\d+) pairs of mitts", it["q"])
            if m:
                assert it["q"].count("height='30' rx='9'") == 2 * int(m.group(1))
            m = re.search(r"aria-label='(\d+) hands", it["q"])
            if m:
                assert it["q"].count("width='30' height='26'") == int(m.group(1))
            m = re.search(r"aria-label='(\d+) nickels", it["q"])
            if m:
                assert it["q"].count(">5¢<") == int(m.group(1))
    u = {
        "country": "ca-on", "subject": "math", "grade": "grade-1", "slug": "counting-and-estimating-to-50", "sort": 2,
        "updated": UPDATED, "pdf_url": "",
        "title": "Counting and Estimating to 50: Count by 1s, 2s, 5s and 10s",
        "seo_title": "Grade 1 Counting to 50 Math Worksheets: Skip Counting and Estimating, Free with Answer Key (Ontario)",
        "short_title": "Counting and estimating to 50",
        "domain": "Number",
        "standard_code": "Grade 1: B1.5",
        "standard_url": "https://www.dcp.edu.gov.on.ca/en/curriculum/elementary-mathematics",
        "standard_text": "Count to 50 by 1s, 2s, 5s, and 10s, using a variety of tools and strategies",
        "meta_desc": "Free Grade 1 math worksheets on counting to 50 for the Ontario curriculum: count on and back by 1s, skip count by 2s, 5s and 10s with mitts, nickels and ten frames, find missing numbers and estimate, then count to check. 100 picture questions with an answer key.",
        "key_big": "Count on, count back, and skip count by 2s, 5s and 10s to 50.",
        "key_sub": "Keep the same jump all the way, say each number once, and after 29 comes 30. Estimate first, then count to check.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }
    return u


if __name__ == "__main__":
    u = gen_unit()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(u, f, ensure_ascii=False, indent=1)
    print("wrote", path)
