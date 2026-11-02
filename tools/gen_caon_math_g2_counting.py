# -*- coding: utf-8 -*-
"""
CA Grade 2 Math: Counting to 200 (Ontario Mathematics Curriculum 2020, Grade 2: B1.4)
  python3 tools/gen_caon_math_g2_counting.py
HTML attributes use single quotes (no backslashes in the JSON).
Grade 2: whole numbers to 200, short sentences for 7-8 year olds, many pictures
(mitts, nickels, quarters, tally marks, number lines, number chart pieces).
Wrong answers come from real mistakes: 25, 50, 75, 90 (switching to 10s), writing each spoken
part across 100 (95, 100, 1005 / 109, 1010), counting by 1s instead of the step, counting pairs
instead of mitts, counting coins instead of their value, counting the start as a jump.
"""
import json, os, random, re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "ca-on", "math", "grade-2")
UPDATED = "2026-11-02"
GREEN = "#006633"
FILL = "#cfe6d6"
RED = "#c0392b"
INK = "#2b2b2b"
FONT = "Arial, Helvetica, sans-serif"
GIRLS = ["Olivia", "Emma", "Maya", "Zoe", "Amira", "Mei", "Chloe", "Priya", "Leah", "Hana", "Ava", "Sofia"]
BOYS = ["Liam", "Noah", "Aiden", "Lucas", "Owen", "Arjun", "Ethan", "Jayden", "Benjamin", "Mateo", "Nathan", "Kai"]
# wrong answers above 250 that show a real mistake (writing each part you say)
BIG_OK = {1010, 1110, 1100, 910, 1006, 1002, 1810, 1005, 1910, 1020, 1050, 1003}


# ------------------------------------------------------------ helpers
def mcq(q, correct, wrong, e):
    correct = str(correct)
    wrong = [str(w) for w in wrong]
    assert len(wrong) == 3 and len(set(wrong + [correct])) == 4, (q, correct, wrong)
    for c in [correct] + wrong:
        for tok in re.findall(r"\d+", c):
            v = int(tok)
            assert 0 <= v <= 250 or v in BIG_OK, (q, c)
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
        p = self.pool[self.i % len(self.pool)]
        self.i += 1
        nm, he, his = p
        return dict(n=nm, he=he, He=he.capitalize(), his=his)


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
    rx = re.compile(r"<svg (?=[^>]*aria-label='" + pattern + ")")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u


def lst(xs):
    return ", ".join(str(x) for x in xs)


def counts(start, step, n):
    return [start + step * k for k in range(n)]


def rows_of(n, per):
    """Split n things into rows of at most `per`, as even as possible (7 -> 4 + 3)."""
    r = (n + per - 1) // per
    base, extra = divmod(n, r)
    return [base + (1 if i < extra else 0) for i in range(r)]


# ------------------------------------------------------------ pictures
def mitt(x, y, left):
    """One winter mitt in a 26 x 40 box. left=True puts the thumb on the left."""
    s = []
    bx = x + (6 if left else 2)
    tx = x + 1 if left else x + 19
    s.append("<rect x='%.1f' y='%.1f' width='7' height='15' rx='3.5' fill='%s' stroke='%s' stroke-width='1.5' "
             "transform='rotate(%d %.1f %.1f)'/>" % (tx, y + 10, FILL, GREEN, -25 if left else 25, tx + 3.5, y + 24))
    s.append("<rect x='%.1f' y='%.1f' width='18' height='30' rx='9' fill='%s' stroke='%s' stroke-width='1.5'/>"
             % (bx, y, FILL, GREEN))
    s.append("<rect x='%.1f' y='%.1f' width='18' height='8' rx='2' fill='%s' stroke='%s' stroke-width='1.5'/>"
             % (bx, y + 31, GREEN, GREEN))
    return "".join(s)


def mitts_svg(pairs):
    m, pw, ph, gap = 6, 56, 40, 14
    rows = rows_of(pairs, 4)
    W = 2 * m + max(rows) * pw + (max(rows) - 1) * gap
    H = 2 * m + len(rows) * ph + (len(rows) - 1) * 10
    s = []
    for r, k in enumerate(rows):
        for i in range(k):
            x, y = m + i * (pw + gap), m + r * (ph + 10)
            s.append(mitt(x, y, True))
            s.append(mitt(x + 28, y, False))
    return svg_wrap(W, H, "".join(s), "%d pairs of mitts" % pairs)


def coins_svg(n, val, r):
    m, gap = 4, 8
    rows = rows_of(n, 5)
    d = 2 * r + gap
    W = 2 * m + max(rows) * d - gap
    H = 2 * m + len(rows) * d - gap
    s = []
    for row, k in enumerate(rows):
        for i in range(k):
            cx, cy = m + r + i * d, m + r + row * d
            s.append("<circle cx='%d' cy='%d' r='%d' fill='#dfe3e7' stroke='#7a828a' stroke-width='2'/>" % (cx, cy, r))
            s.append("<circle cx='%d' cy='%d' r='%d' fill='none' stroke='#9aa2aa' stroke-width='1'/>" % (cx, cy, r - 4))
            s.append(text(cx, cy + 6, "%d¢" % val, 16))
    name = "nickels" if val == 5 else "quarters"
    return svg_wrap(W, H, "".join(s), "%d %s" % (n, name))


def nickels_svg(n):
    return coins_svg(n, 5, 21)


def quarters_svg(n):
    return coins_svg(n, 25, 25)


TG, TH = 8, 38


def tally_svg(groups, extra=0):
    """Tally marks: groups of 5 (4 sticks and a slash), then `extra` single sticks."""
    m = 8
    units = [4] * groups + ([extra] if extra else [])
    full = [True] * groups + ([False] if extra else [])
    rows = rows_of(len(units), 4)
    uw = 3 * TG + 12
    gap = 20
    W = 2 * m + max(rows) * uw + (max(rows) - 1) * gap
    H = 2 * m + len(rows) * TH + (len(rows) - 1) * 14
    s, k = [], 0
    for r, cnt in enumerate(rows):
        for i in range(cnt):
            x0 = m + i * (uw + gap) + 6
            y0 = m + r * (TH + 14)
            for j in range(units[k]):
                s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='2.5' stroke-linecap='round'/>"
                         % (x0 + j * TG, y0, x0 + j * TG, y0 + TH, INK))
            if full[k]:
                s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='2.5' stroke-linecap='round'/>"
                         % (x0 - 5, y0 + TH - 6, x0 + 3 * TG + 5, y0 + 6, INK))
            k += 1
    label = "tally marks, %d groups of 5" % groups + (" and %d more" % extra if extra else "")
    return svg_wrap(W, H, "".join(s), label)


CWID, CHT = 48, 34


def chart_svg(tl, nrows, ncols, target, hide=()):
    """A piece of the number chart (1 to 200, 10 in a row). target (r, c) shows a red ?, hide = blank cells."""
    assert (tl - 1) % 10 + ncols <= 10, "piece must stay inside one row of the chart"
    assert tl + 10 * (nrows - 1) + ncols - 1 <= 200
    m = 4
    W, H = 2 * m + ncols * CWID, 2 * m + nrows * CHT
    s = []
    for r in range(nrows):
        for c in range(ncols):
            x, y = m + c * CWID, m + r * CHT
            isT = (r, c) == target
            s.append("<rect x='%d' y='%d' width='%d' height='%d' fill='%s' stroke='%s' stroke-width='1.5'/>"
                     % (x, y, CWID, CHT, FILL if isT else "#ffffff", GREEN))
            if isT:
                s.append(text(x + CWID / 2, y + 23, "?", 18, col=RED))
            elif (r, c) not in hide:
                s.append(text(x + CWID / 2, y + 23, str(tl + 10 * r + c), 16))
    return svg_wrap(W, H, "".join(s), "number chart piece")


def jw(j):
    j = abs(j)
    return 84 if j >= 20 else 74 if j >= 10 else 56


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
        start, ", ".join(jlabels).replace("−", "minus ")))


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
    return svg_wrap(W, H, "".join(s), "number line counting by %ds" % step)


def line_q(start, step, n, labels, wrong, e):
    k = [i for i, t in labels.items() if t == "?"][0]
    ans = start + step * k
    q = fig(step_line_svg(start, step, n, labels)) + "The marks go up by %d each time. What number goes at the ?" % step
    return mcq(q, ans, wrong, e)


def chart_q(tl, rows, cols, tgt, hide, wrong, how):
    ans = tl + 10 * tgt[0] + tgt[1]
    q = fig(chart_svg(tl, rows, cols, tgt, hide)) + "This is part of a number chart. What number goes at the ?"
    return mcq(q, ans, wrong, how.replace("ANS", "<b>%d</b>" % ans)), ans


def jumps_q(start, step, n, wrong):
    end = start + step * n
    pts = counts(start, step, n + 1)
    if step > 0:
        q = "Start at %d. Make the jumps. Where do you land?" % start
        e = "Each jump is +%d. Count by %ds from %d: %s. You land on <b>%d</b>." % (step, step, start, lst(pts[1:]), end)
    else:
        q = "Start at %d. Jump back. Where do you land?" % start
        e = "Each jump is back %d. Count back by %ds: %s. You land on <b>%d</b>." % (-step, -step, lst(pts[1:]), end)
    assert 0 <= end <= 200
    return mcq(fig(nline_svg(start, [step] * n)) + q, end, wrong, e)


def seq_q(xs, blank, step, wrong, e, back=False):
    """xs: the counting list; blank = index shown as ☐ (last = 'What comes next?')."""
    for a, b in zip(xs, xs[1:]):
        assert b - a == step
    ans = xs[blank]
    shown = [("☐" if i == blank else str(x)) for i, x in enumerate(xs)]
    word = ("Count back by %ds" if back else "Count by %ds") % abs(step)
    if abs(step) == 1:
        word = "Count back" if back else "Count on"
    if blank == len(xs) - 1:
        q = "%s: %s. What comes next?" % (word, ", ".join(shown))
    else:
        q = "%s: %s. What number is missing?" % (word, ", ".join(shown))
    return mcq(q, ans, wrong, e)


# ============================================================ set 1: count on and back by 1s and 10s
def set_ones_tens():
    S = {}
    S["a"] = seq_q([46, 47, 48, 49], 3, 1, [58, 47, 94],
                   "Each number is 1 more. 48 + 1 = <b>49</b>.")
    S["h"] = seq_q([30, 40, 50, 60], 3, 10, [51, 70, 65],
                   "Each number is 10 more. 50 + 10 = <b>60</b>. 51 is only 1 more.")
    S["g"] = mcq("What number comes just before 160?", 159, [150, 161, 169],
                 "Count back 1 from 160: <b>159</b>. 161 comes just after 160.")
    S["j"] = seq_q([23, 33, 43, 53], 3, 10, [44, 63, 54],
                   "Each number is 10 more. The ones digit stays 3. Only the tens digit goes up. 43 + 10 = <b>53</b>.")
    S["f"] = seq_q([142, 141, 140, 139], 3, -1, [130, 149, 138],
                   "Each number is 1 less. 140 − 1 = <b>139</b>. Just before 140 is 139, not 130.", back=True)
    S["m"] = seq_q([90, 80, 70, 60], 3, -10, [69, 50, 80],
                   "Each number is 10 less. 70 − 10 = <b>60</b>. 69 is only 1 less.", back=True)
    S["b"] = seq_q([107, 108, 109, 110], 3, 1, [1010, 100, 111],
                   "109 + 1 = <b>110</b>. 9 ones and 1 more make a new ten. Write 110, not 1010.")
    S["i"] = seq_q([80, 90, 100, 110], 3, 10, [1010, 101, 200],
                   "100 + 10 = <b>110</b>. 1 hundred and 1 ten is 110, not 1010.")
    S["c"] = seq_q([117, 118, 119, 120], 3, 1, [1110, 130, 121],
                   "119 + 1 = <b>120</b>. 9 ones and 1 more make a new ten. So 11 tens become 12 tens.")
    S["e"] = seq_q([103, 102, 101, 100], 3, -1, [99, 110, 102],
                   "Each number is 1 less. 101 − 1 = <b>100</b>. Do not skip 100. 99 comes after it.", back=True)
    S["k"] = seq_q([76, 86, 96, 106], 3, 10, [97, 1006, 116],
                   "96 + 10 = <b>106</b>. 9 tens and 1 more ten make 1 hundred. The ones digit stays 6.")
    S["l"] = seq_q([145, 155, 165, 175], 3, 10, [166, 185, 176],
                   "Each number is 10 more. Only the tens digit goes up. 165 + 10 = <b>175</b>.")
    S["n"] = seq_q([132, 122, 112, 102], 3, -10, [111, 92, 12],
                   "Each number is 10 less. The ones digit stays 2. 112 − 10 = <b>102</b>. Keep the 0 in the tens place.",
                   back=True)
    S["d"] = mcq("What number comes just after 199?", 200, [1100, 1910, 190],
                 "199 + 1 = <b>200</b>. 9 ones and 1 more make a ten. 9 tens and 1 more ten make a hundred. "
                 "So 1 hundred becomes 2 hundreds.")
    S["L1"] = line_q(115, 1, 7, {0: "115", 3: "?", 6: "121"}, [117, 119, 128],
                     "Count on by 1s from 115: 116, 117, <b>118</b>.")
    S["L2"] = line_q(96, 1, 7, {0: "96", 4: "?", 6: "102"}, [910, 99, 101],
                     "Count on by 1s from 96: 97, 98, 99, <b>100</b>. After 99 comes 100, not 910.")
    S["C1"], _ = chart_q(63, 3, 4, (2, 1), {(1, 3), (2, 3)}, [75, 85, 74],
                         "Each row is 10 more than the row above. The number above the ? is 74. 74 + 10 = ANS.")
    S["C2"], _ = chart_q(176, 3, 4, (2, 2), {(0, 1), (1, 0)}, [189, 199, 188],
                         "Each row is 10 more than the row above. The number above the ? is 188. 188 + 10 = ANS. "
                         "Or count on 1 from 197.")
    S["J1"] = jumps_q(58, 10, 3, [61, 78, 98])
    S["J2"] = jumps_q(175, -10, 3, [172, 155, 135])
    order = ["a", "h", "L1", "g", "j", "f", "m", "C1", "J1", "b",
             "i", "L2", "c", "e", "k", "l", "n", "J2", "C2", "d"]
    assert len(order) == 20 and set(order) == set(S)
    return {"title": "Count on and back by 1s and 10s", "items": [S[k] for k in order]}


# ============================================================ set 2: count by 2s and 5s
def set_twos_fives():
    S = {}
    for key, n, wrong in [("M1", 4, [4, 6, 10]), ("M2", 9, [9, 16, 20])]:
        S[key] = mcq(fig(mitts_svg(n)) + "Count by 2s. How many mitts are there?", 2 * n, wrong,
                     "A pair is 2 mitts. Count by 2s, one pair at a time: %s. There are <b>%d</b> mitts."
                     % (lst(counts(2, 2, n)), 2 * n))
    for key, n, wrong in [("N1", 6, ["6¢", "25¢", "35¢"]), ("N2", 12, ["12¢", "55¢", "65¢"])]:
        S[key] = mcq(fig(nickels_svg(n)) + "A nickel is 5¢. How much money is this?", "%d¢" % (5 * n), wrong,
                     "Count by 5s, one nickel at a time: %s. That is <b>%d¢</b>." % (lst(counts(5, 5, n)), 5 * n))
    S["T1"] = mcq(fig(tally_svg(7)) + "How many tally marks are there?", 35, [28, 7, 40],
                  "Each group has 5 marks. Count by 5s: %s. There are <b>35</b> marks." % lst(counts(5, 5, 7)))
    S["T2"] = mcq(fig(tally_svg(4, 3)) + "How many tally marks are there?", 23, [19, 20, 7],
                  "Count the groups by 5s: 5, 10, 15, 20. Then count on 3 by 1s: 21, 22, 23. "
                  "There are <b>23</b> marks.")
    S["s1"] = seq_q([2, 4, 6, 8, 10], 4, 2, [9, 12, 7], "Each number is 2 more. 8 + 2 = <b>10</b>.")
    S["s2"] = seq_q([31, 33, 35, 37], 3, 2, [36, 38, 45],
                    "Each number is 2 more. 35 + 2 = <b>37</b>. 36 is counting by 1s.")
    S["s3"] = seq_q([96, 98, 100, 102], 3, 2, [1002, 101, 120],
                    "100 + 2 = <b>102</b>. 1 hundred and 2 ones is 102, not 1002.")
    S["s4"] = seq_q([150, 148, 146, 144], 3, -2, [145, 142, 136],
                    "Each number is 2 less. 146 − 2 = <b>144</b>.", back=True)
    S["s5"] = seq_q([186, 188, 190, 192], 2, 2, [189, 194, 1810],
                    "The missing number is 2 more than 188. 188 + 2 = <b>190</b>. Then 190 + 2 = 192.")
    S["f1"] = seq_q([15, 20, 25, 30], 3, 5, [26, 35, 50], "Each number is 5 more. 25 + 5 = <b>30</b>.")
    S["f2"] = seq_q([90, 95, 100, 105], 3, 5, [1005, 101, 110],
                    "100 + 5 = <b>105</b>. 1 hundred and 5 ones is 105. Do not write 1005.")
    S["f3"] = seq_q([135, 140, 145, 150], 2, 5, [141, 146, 155],
                    "The missing number is 5 more than 140. 140 + 5 = <b>145</b>. Then 145 + 5 = 150.")
    S["f4"] = seq_q([70, 65, 60, 55], 3, -5, [59, 50, 65],
                    "Each number is 5 less. 60 − 5 = <b>55</b>. 59 is counting back by 1s.", back=True)
    S["f5"] = seq_q([110, 105, 100, 95], 3, -5, [99, 90, 105],
                    "Each number is 5 less. 100 − 5 = <b>95</b>. 99 is only 1 less.", back=True)
    S["f6"] = seq_q([185, 190, 195, 200], 3, 5, [196, 190, 1910],
                    "195 + 5 = <b>200</b>. 5 ones and 5 more ones make a ten. 9 tens and 1 more ten make a hundred. So 195 becomes 200.")
    S["i1"] = mcq("Count by 5s from 0. Which number do you say?", 85, [82, 58, 93],
                  "Counting by 5s from 0, every number ends in 0 or 5: 75, 80, <b>85</b>. 82, 58 and 93 do not.")
    S["J1"] = jumps_q(46, 2, 4, [50, 52, 56])
    S["J2"] = jumps_q(120, 5, 4, [124, 135, 145])
    order = ["s1", "M1", "f1", "N1", "s2", "T1", "f4", "J1", "M2", "i1",
             "s4", "N2", "f3", "T2", "s3", "f2", "J2", "f5", "s5", "f6"]
    assert len(order) == 20 and set(order) == set(S)
    return {"title": "Count by 2s and 5s", "items": [S[k] for k in order]}


# ============================================================ set 3: count by 20s and 25s
def set_twenties():
    S = {}
    S["a"] = seq_q([20, 40, 60, 80], 3, 20, [61, 70, 100],
                   "Each number is 20 more. 60 + 20 = <b>80</b>. 70 is counting by 10s.")
    S["b"] = seq_q([60, 80, 100, 120], 3, 20, [1020, 110, 140],
                   "100 + 20 = <b>120</b>. 1 hundred and 2 tens is 120, not 1020.")
    S["c"] = seq_q([100, 120, 140, 160], 3, 20, [150, 141, 180],
                   "Each number is 20 more. 140 + 20 = <b>160</b>. 150 is counting by 10s.")
    S["d"] = seq_q([120, 140, 160, 180], 1, 20, [130, 121, 150],
                   "The missing number is 20 more than 120. 120 + 20 = <b>140</b>. Then 140 + 20 = 160.")
    S["e"] = seq_q([200, 180, 160, 140], 3, -20, [150, 159, 120],
                   "Each number is 20 less. 160 − 20 = <b>140</b>.", back=True)
    S["f"] = seq_q([10, 30, 50, 70], 3, 20, [60, 51, 90],
                   "Each number is 20 more. The tens digit goes up by 2. 50 + 20 = <b>70</b>.")
    S["g"] = mcq("Count by 20s from 0. Which number do you say?", 160, [150, 170, 90],
                 "Counting by 20s from 0: 20, 40, 60, 80, 100, 120, 140, <b>160</b>. 150, 170 and 90 are not in the list.")
    S["h"] = seq_q([25, 50, 75, 100], 3, 25, [90, 80, 76],
                   "Each number is 25 more. 75 + 25 = <b>100</b>. After 75 do not switch to 10s (90).")
    S["i"] = seq_q([100, 125, 150, 175], 3, 25, [165, 200, 151],
                   "Each number is 25 more. 150 + 25 = <b>175</b>. 200 is counting by 50s.")
    S["j"] = seq_q([50, 75, 100, 125], 2, 25, [90, 85, 105],
                   "The missing number is 25 more than 75. 75 + 25 = <b>100</b>. Then 100 + 25 = 125.")
    S["k"] = seq_q([200, 175, 150, 125], 3, -25, [140, 100, 130],
                   "Each number is 25 less. 150 − 25 = <b>125</b>.", back=True)
    S["l"] = mcq("Count by 25s from 0. Which number do you say?", 75, [70, 85, 95],
                 "Counting by 25s from 0: 25, 50, <b>75</b>, 100. The numbers end in 25, 50, 75 or 00.")
    S["Q1"] = mcq(fig(quarters_svg(3)) + "A quarter is 25¢. How much money is this?", "75¢", ["3¢", "90¢", "50¢"],
                  "Count by 25s, one quarter at a time: 25, 50, 75. That is <b>75¢</b>.")
    S["Q2"] = mcq(fig(quarters_svg(4)) + "A quarter is 25¢. How much money is this?", "100¢", ["4¢", "90¢", "125¢"],
                  "Count by 25s: 25, 50, 75, 100. That is <b>100¢</b>. 100¢ is $1, the same as a loonie.")
    S["Q3"] = mcq(fig(quarters_svg(6)) + "A quarter is 25¢. How much money is this?", "150¢", ["6¢", "125¢", "175¢"],
                  "Count by 25s: 25, 50, 75, 100, 125, 150. That is <b>150¢</b>.")
    S["Q4"] = mcq("How many quarters make $1 (100¢)?", 4, [5, 10, 25],
                  "Count by 25s until you reach 100: 25, 50, 75, 100. That is <b>4</b> quarters.")
    S["Q5"] = mcq("How many quarters make $2 (200¢), the same as a toonie?", 8, [4, 10, 20],
                  "Count by 25s to 200: 25, 50, 75, 100, 125, 150, 175, 200. That is <b>8</b> quarters.")
    S["J1"] = jumps_q(40, 20, 3, [43, 80, 120])
    S["J2"] = jumps_q(50, 25, 4, [54, 125, 175])
    S["L"] = mcq("Which list counts by 25s?", "25, 50, 75, 100",
                 ["25, 50, 75, 90", "25, 30, 35, 40", "20, 40, 60, 80"],
                 "Each number must be 25 more: <b>25, 50, 75, 100</b>. In 25, 50, 75, 90 the last jump is only 15.")
    order = ["a", "h", "Q1", "f", "g", "Q2", "J1", "l", "c", "Q4",
             "b", "j", "d", "Q3", "L", "e", "i", "J2", "k", "Q5"]
    assert len(order) == 20 and set(order) == set(S)
    return {"title": "Count by 20s and 25s", "items": [S[k] for k in order]}


# ============================================================ set 4: count by 50s and find the rule
def set_fifties():
    S = {}
    S["a"] = seq_q([0, 50, 100, 150], 3, 50, [1050, 101, 200],
                   "Each number is 50 more. 100 + 50 = <b>150</b>. 1 hundred and 5 tens is 150, not 1050.")
    S["b"] = seq_q([50, 100, 150, 200], 3, 50, [160, 250, 151],
                   "150 + 50 = <b>200</b>. Two 50s make 100, so 100 + 100 = 200.")
    S["c"] = seq_q([200, 150, 100, 50], 3, -50, [90, 99, 150],
                   "Each number is 50 less. 100 − 50 = <b>50</b>. 90 is counting back by 10s.", back=True)
    S["d"] = seq_q([10, 60, 110, 160], 3, 50, [111, 120, 210],
                   "Each number is 50 more. 110 + 50 = <b>160</b>. The ones digit stays 0.")
    S["e"] = seq_q([25, 75, 125, 175], 3, 50, [130, 126, 225],
                   "Each number is 50 more. 125 + 50 = <b>175</b>.")
    S["f"] = seq_q([30, 80, 130, 180], 2, 50, [90, 131, 150],
                   "The missing number is 50 more than 80. 80 + 50 = <b>130</b>. Then 130 + 50 = 180.")
    S["g"] = seq_q([190, 140, 90, 40], 3, -50, [80, 89, 50],
                   "Each number is 50 less. 90 − 50 = <b>40</b>.", back=True)
    S["h"] = mcq("How many 50s make 100?", 2, [50, 5, 10],
                 "Count by 50s: 50, 100. That is <b>2</b> fifties.")
    S["i"] = mcq("How many 50s make 200?", 4, [2, 5, 20],
                 "Count by 50s: 50, 100, 150, 200. That is <b>4</b> fifties.")
    S["k"] = mcq("Count by 50s from 0. Which number do you say?", 150, [105, 125, 140],
                 "Counting by 50s from 0: 50, 100, <b>150</b>, 200. 125 is counting by 25s.")
    S["l"] = mcq("Which list counts by 50s?", "20, 70, 120, 170",
                 ["20, 25, 30, 35", "20, 70, 100, 150", "20, 50, 80, 110"],
                 "Each number must be 50 more: <b>20, 70, 120, 170</b>. 20, 25, 30, 35 counts by 5s.")
    S["J1"] = jumps_q(0, 50, 3, [3, 100, 200])
    S["J2"] = jumps_q(70, 50, 2, [72, 120, 220])
    S["J3"] = jumps_q(200, -50, 3, [197, 100, 0])
    rule_wrong = {
        "Count by 50s": ["Count by 5s", "Count by 25s", "Count by 10s"],
        "Count by 25s": ["Count by 5s", "Count by 20s", "Count by 50s"],
        "Count by 20s": ["Count by 2s", "Count by 10s", "Count by 25s"],
        "Count back by 10s": ["Count by 10s", "Count back by 1s", "Count back by 20s"],
    }
    for key, xs, right, e in [
        ("r1", [35, 85, 135, 185], "Count by 50s", "Each number is 50 more: 35 + 50 = 85. The rule is <b>count by 50s</b>."),
        ("r2", [100, 125, 150, 175], "Count by 25s", "Each number is 25 more: 100 + 25 = 125. The rule is <b>count by 25s</b>."),
        ("r3", [40, 60, 80, 100], "Count by 20s", "Each number is 20 more: 40 + 20 = 60. The rule is <b>count by 20s</b>."),
        ("r4", [160, 150, 140, 130], "Count back by 10s",
         "The numbers get smaller by 10 each time. The rule is <b>count back by 10s</b>."),
    ]:
        step = xs[1] - xs[0]
        assert all(b - a == step for a, b in zip(xs, xs[1:]))
        assert right == ("Count back by %ds" % -step if step < 0 else "Count by %ds" % step)
        S[key] = mcq("What is the rule? %s" % lst(xs), right, rule_wrong[right], e)
    S["both"] = mcq("You count by 50s from 0. Your friend counts by 25s from 0. Which number do you both say?", 100,
                    [75, 125, 25],
                    "By 50s: 50, <b>100</b>, 150, 200. By 25s: 25, 50, 75, <b>100</b>, 125. "
                    "75, 125 and 25 are only in the 25s list.")
    S["more"] = mcq("What number is 50 more than 135?", 185, [140, 186, 235],
                    "Count on 50 from 135. 135 + 50 = <b>185</b>. Only the tens digit changes: 3 tens + 5 tens = 8 tens.")
    order = ["a", "J1", "b", "h", "k", "c", "i", "d", "J2", "r1",
             "e", "l", "f", "r2", "J3", "g", "r3", "more", "r4", "both"]
    assert len(order) == 20 and set(order) == set(S)
    return {"title": "Count by 50s and find the rule", "items": [S[k] for k in order]}


# ============================================================ set 5: number lines, charts and word problems
def set_stories(P):
    S = {}
    S["L2"] = line_q(94, 2, 7, {0: "94", 1: "96", 4: "?"}, [101, 1002, 100],
                     "Count by 2s from 94: 96, 98, 100, <b>102</b>.")
    S["L5"] = line_q(80, 5, 7, {0: "80", 1: "85", 3: "?"}, [90, 100, 98],
                     "Count by 5s from 80: 85, 90, <b>95</b>.")
    S["L10"] = line_q(60, 10, 7, {0: "60", 1: "70", 4: "?"}, [910, 90, 110],
                      "Count by 10s from 60: 70, 80, 90, <b>100</b>. After 90 comes 100, not 910.")
    S["L20"] = line_q(100, 20, 6, {0: "100", 1: "120", 3: "?", 5: "200"}, [130, 140, 180],
                      "Count by 20s from 100: 120, 140, <b>160</b>.")
    S["L25"] = line_q(0, 25, 7, {0: "0", 1: "25", 4: "?"}, [90, 75, 125],
                      "Count by 25s from 0: 25, 50, 75, <b>100</b>. Not 90: keep jumping by 25.")
    S["L50"] = line_q(0, 50, 5, {0: "0", 1: "50", 3: "?"}, [1050, 100, 200],
                      "Count by 50s from 0: 50, 100, <b>150</b>. Write 150, not 1050.")
    S["C1"], a = chart_q(112, 3, 4, (2, 3), {(2, 2), (2, 1)}, [126, 134, 145],
                         "Each row is 10 more than the row above. The number above the ? is 125. 125 + 10 = ANS.")
    S["C2"], a = chart_q(165, 3, 4, (2, 0), {(2, 1), (1, 1)}, [176, 195, 184],
                         "Each row is 10 more than the row above. The number above the ? is 175. 175 + 10 = ANS.")
    S["C3"], a = chart_q(142, 3, 4, (0, 3), {(0, 2), (0, 1)}, [146, 155, 135],
                         "The number below the ? is 155. The row above is 10 less. 155 − 10 = ANS.")

    def story(key, t, ans, unit, wrong, e):
        d = P.next()
        u = (lambda v: "%d%s" % (v, unit)) if unit == "¢" else (lambda v: "%d %s" % (v, unit))
        S[key] = mcq(t.format(**d), u(ans), [u(v) for v in wrong], e.format(**d))

    story("boots", "{n} sees 8 pairs of winter boots by the classroom door. How many boots are there?", 16, "boots",
          [8, 14, 18], "A pair is 2 boots. Count by 2s 8 times: 2, 4, 6, 8, 10, 12, 14, 16. There are <b>16</b> boots.")
    story("geese", "{n} sees Canada geese fly by in groups of 5. {He} counts 8 groups. How many geese are there?",
          40, "geese", [13, 35, 45],
          "Count by 5s 8 times: 5, 10, 15, 20, 25, 30, 35, 40. There are <b>40</b> geese.")
    story("nickels", "{n} has 9 nickels. A nickel is 5¢. How much money does {he} have?", 45, "¢",
          [9, 40, 90], "Count by 5s 9 times: 5, 10, 15, 20, 25, 30, 35, 40, 45. That is <b>45¢</b>.")
    story("pages", "{n} reads 20 pages each night. How many pages does {he} read in 5 nights?", 100, "pages",
          [25, 80, 120], "Count by 20s 5 times: 20, 40, 60, 80, 100. That is <b>100</b> pages.")
    story("stickers", "{n} has 150 stickers. {He} gives away 10 stickers each day. How many stickers are left after 3 days?",
          120, "stickers", [147, 130, 180],
          "Start at 150 and count back by 10s 3 times: 140, 130, 120. {He} has <b>120</b> stickers left.")
    story("syrup", "A sugar bush has 120 bottles of maple syrup. Each hour, the workers fill 10 more. "
                   "How many bottles are there after 4 hours?", 160, "bottles", [124, 150, 170],
          "Start at 120 and count by 10s 4 times: 130, 140, 150, 160. There are <b>160</b> bottles.")
    story("quarters", "{n} has 5 quarters. A quarter is 25¢. How much money does {he} have?", 125, "¢",
          [5, 100, 150], "Count by 25s 5 times: 25, 50, 75, 100, 125. That is <b>125¢</b>, or $1.25.")
    story("pucks", "A box holds 25 hockey pucks. The rink has 6 boxes. How many pucks are there?", 150, "pucks",
          [31, 125, 175], "Count by 25s 6 times: 25, 50, 75, 100, 125, 150. There are <b>150</b> pucks.")
    story("terry", "At the Terry Fox Run, {n} runs 4 laps around the gym. Each lap is 50 m. How far does {he} run?",
          200, "m", [54, 150, 250], "Count by 50s 4 times: 50, 100, 150, 200. {He} runs <b>200 m</b>.")
    story("crayons", "{n} has 5 boxes of 20 crayons and 3 more crayons. How many crayons does {he} have?", 103,
          "crayons", [28, 1003, 100],
          "Count the boxes by 20s: 20, 40, 60, 80, 100. Then count on 3 by 1s: 101, 102, 103. "
          "{He} has <b>103</b> crayons.")
    story("bank", "{n} puts 1 quarter in {his} piggy bank each day. How many days until {he} has $2 (200¢)?", 8, "days",
          [2, 4, 25], "Count by 25s to 200: 25, 50, 75, 100, 125, 150, 175, 200. That is 8 quarters, so <b>8</b> days.")
    order = ["L2", "L5", "L10", "C1", "C2", "C3", "L20", "L25", "L50", "boots",
             "geese", "nickels", "pages", "stickers", "syrup", "quarters", "pucks", "terry", "crayons", "bank"]
    assert len(order) == 20 and set(order) == set(S)
    return {"title": "Number lines, charts and word problems", "items": [S[k] for k in order]}


# ============================================================ lesson
def body_html():
    return (
        "<h2>Skip counting: jump by the same number</h2>"
        "<p>When you skip count, you jump by the same amount each time. "
        "In Grade 2 you count to 200 by 1s, 2s, 5s, 10s, 20s, 25s and 50s.</p>"
        + table(["Count by", "Example", "Look for"], [
            ["2s", "36, 38, 40, 42", "Skip every other number"],
            ["5s", "85, 90, 95, 100", "The ones digit is 0 or 5"],
            ["10s", "23, 33, 43, 53", "Only the tens digit changes"],
            ["20s", "100, 120, 140, 160", "Five 20s make 100"],
            ["25s", "25, 50, 75, 100", "The numbers end in 25, 50, 75, 00"],
            ["50s", "50, 100, 150, 200", "Two 50s make 100"],
        ]) +
        "<h2>Count by 10s from any number</h2>"
        "<p>You can start at any number. When you count by 10s, the ones digit stays the same.</p>"
        "<figure class='sn-fig'>" + nline_svg(86, [10, 10, 10], ticks=["86", "96", "106", "116"]) +
        "<figcaption>Start at 86 and jump +10 three times: 96, 106, 116.</figcaption></figure>"
        "<p>On a number chart, the number just below is 10 more. The number just right is 1 more.</p>"
        "<figure class='sn-fig'>" + chart_svg(154, 3, 4, (2, 1)) +
        "<figcaption>Below 165 is 175. The ? is 175.</figcaption></figure>"
        "<h2>Count by 25s with quarters</h2>"
        "<p>A quarter is 25¢. Count quarters by 25s. 4 quarters make 100¢, or $1. That is a loonie.</p>"
        "<figure class='sn-fig'>" + quarters_svg(4) +
        "<figcaption>25, 50, 75, 100. Four quarters are 100¢.</figcaption></figure>"
        + ex("Count by 25s", "Count by 25s: 100, 125, 150, ☐",
             "Each number is 25 more. 150 + 25 = 175.", "175") +
        "<figure class='sn-fig'>" + step_line_svg(0, 50, 5, {0: "0", 1: "50", 2: "100", 3: "150", 4: "200"}) +
        "<figcaption>Counting by 50s: 0, 50, 100, 150, 200.</figcaption></figure>"
        "<h2>Going past 100</h2>"
        "<p>After 100, the numbers start again with a 1 in front: 101, 102, 103 … 110, 120. "
        "100 and 5 more is <b>105</b>. It has 3 digits, not 4.</p>"
        + table(["Count by", "Past 100"], [
            ["1s", "98, 99, <b>100</b>, 101, 102"],
            ["5s", "90, 95, 100, <b>105</b>, 110"],
            ["10s", "80, 90, 100, <b>110</b>, 120"],
            ["1s", "197, 198, 199, <b>200</b>"],
        ]) +
        "<h2>Common mistakes</h2>"
        + table(["Mistake", "What to do instead"], [
            ["Counting 25, 50, 75, 90", "Keep jumping by 25: 75 + 25 = 100"],
            ["Writing 1005 after 100 when counting by 5s", "100 and 5 more is 105"],
            ["Writing 1010 after 109", "109 + 1 = 110"],
            ["Changing the ones digit when counting by 10s: 23, 33, 44", "Keep the ones digit: 23, 33, 43"],
            ["Counting pairs, not things (8 pairs = 8 boots)", "Count by 2s: 8 pairs = 16 boots"],
            ["Counting the start as a jump", "Count only the numbers you land on"],
        ])
    )


FAQ = [
    {"q": "What counting is in the Grade 2 Ontario math curriculum?",
     "a": "Expectation B1.4 asks Grade 2 students to count to 200, including by 20s, 25s and 50s, using tools like number lines, number charts and coins. They also count on and back by 1s, 2s, 5s and 10s from any number."},
    {"q": "Why do Grade 2 students count by 25s?",
     "a": "Counting by 25s is counting quarters. Four quarters make $1 (a loonie) and eight quarters make $2 (a toonie), so it builds money sense too."},
    {"q": "Why does my child write 1005 after 100 when counting by 5s?",
     "a": "They write “100” and then “5”, the way the number sounds. Show that 100 and 5 more is 105, which has only 3 digits, on a number chart or a number line."},
    {"q": "How can I practise counting to 200 at home?",
     "a": "Count real things in groups: pairs of mitts by 2s, nickels by 5s, dimes by 10s and quarters by 25s. Ask your child to count on and back from a number like 96 or 185, past 100 and up to 200."},
]


def gen_unit():
    rnd = random.Random(42802)
    P = People(random.Random(428021))
    sets = [set_ones_tens(), set_twos_fives(), set_twenties(), set_fifties(), set_stories(P)]
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
    u = {
        "country": "ca-on", "subject": "math", "grade": "grade-2", "slug": "counting-to-200", "sort": 2,
        "updated": UPDATED, "pdf_url": "",
        "title": "Counting to 200: Skip Counting by 2s, 5s, 10s, 20s, 25s and 50s",
        "seo_title": "Grade 2 Counting to 200 Math Worksheets: Skip Counting, Free with Answer Key (Ontario)",
        "short_title": "Counting to 200",
        "domain": "Number",
        "standard_code": "Grade 2: B1.4",
        "standard_url": "https://www.dcp.edu.gov.on.ca/en/curriculum/elementary-mathematics",
        "standard_text": "Count to 200, including by 20s, 25s, and 50s, using a variety of tools and strategies",
        "meta_desc": "Free Grade 2 math worksheets on counting to 200 for the Ontario curriculum: count on and back by 1s and 10s, skip count by 2s, 5s, 20s, 25s and 50s with mitts, nickels and quarters, and fill in number lines and number charts. 100 questions with an answer key.",
        "key_big": "Skip counting means jumping by the same number each time.",
        "key_sub": "Count by 25s like quarters: 25, 50, 75, 100, not 90. Past 100, 100 and 5 more is 105, not 1005.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }
    return mark_large(u, "(open number line|number line counting|tally marks|\\d+ pairs of mitts|\\d+ nickels|\\d+ quarters)")


if __name__ == "__main__":
    u = gen_unit()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(u, f, ensure_ascii=False, indent=1)
    print("wrote", path)
