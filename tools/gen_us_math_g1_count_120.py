# -*- coding: utf-8 -*-
"""
US Grade 1 Math: Count to 120 (1.NBT.A.1)
  python tools/gen_us_math_g1_count_120.py
Count objects in rows of 10, ten-frames and ten rods; say what comes next or before
(also across a new ten and past 100); fill in a 120 chart; read and write number words;
count past 100 in short stories.
Every answer and every picture is computed and checked in code.
HTML attributes use single quotes (no backslashes in the JSON).
"""
import json, os, random, re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "us", "math", "grade-1")
UPDATED = "2026-11-02"
GREEN = "#006633"
FILL = "#cfe6d6"
CUBE = "#f2c94c"
RED = "#c0392b"
INK = "#2b2b2b"
FONT = "Arial, Helvetica, sans-serif"
GIRLS = ["Maya", "Ava", "Mia", "Zoe", "Lily", "Emma", "Nora", "Ruby", "Sofia", "Grace"]
BOYS = ["Leo", "Noah", "Eli", "Sam", "Ben", "Omar", "Kai", "Jack", "Luis", "Owen"]
# wrong answers above 120 that show a real mistake (writing "one hundred five" as 1005 …)
BIG_OK = {1005, 10010, 1010, 1000, 910, 1009, 1015, 10017, 10020, 1020, 1104, 1006, 1003, 1101, 1001, 1110,
          1007, 1018, 150, 160, 170, 130, 151, 141, 402, 508, 703, 909, 990, 300, 510, 310, 810, 610, 710, 1102}


# ------------------------------------------------------------ helpers
def mcq(q, correct, cands, e):
    """4 choices: correct + the first 3 unique distractors. Positions are set later by balance()."""
    correct = str(correct)
    seen = {correct}
    pick = []
    for c in cands:
        c = str(c)
        if c in seen or not c or c.startswith("-") or c == "0":
            continue
        seen.add(c)
        pick.append(c)
        if len(pick) == 3:
            break
    assert len(pick) == 3, (q, correct, cands)
    return {"q": q, "c": [correct] + pick, "a": 0, "e": e}


def balance(sets, rnd):
    """Spread the correct answers evenly over the 4 positions in every set."""
    for s in sets:
        targets = [0, 1, 2, 3] * 5
        rnd.shuffle(targets)
        for it, t in zip(s["items"], targets):
            c = it["c"]
            right = c[it["a"]]
            wrong = [x for i, x in enumerate(c) if i != it["a"]]
            rnd.shuffle(wrong)
            it["c"] = wrong[:t] + [right] + wrong[t:]
            it["a"] = t


class People:
    def __init__(self, rnd):
        self.pool = [(n, "she", "her") for n in GIRLS] + [(n, "he", "his") for n in BOYS]
        rnd.shuffle(self.pool)
        self.i = 0

    def next(self):
        nm, he, his = self.pool[self.i % len(self.pool)]
        self.i += 1
        return dict(n=nm, he=he, He=cap(he), his=his)


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


def mark_large(u, pattern):
    """Tag pictures that must print larger so they stay readable."""
    rx = re.compile(r"<svg (?=[^>]*aria-label='" + pattern + ")")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u


def lst(xs):
    return ", ".join(str(x) for x in xs)


def rev(n):
    """Digits written backwards (16 -> 61). None when that gives the same number or a lone digit."""
    s = str(n)
    r = s[::-1]
    if len(s) != 2 or r == s or r.startswith("0"):
        return None
    return int(r)


ONES = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten",
        "eleven", "twelve", "thirteen", "fourteen", "fifteen", "sixteen", "seventeen", "eighteen", "nineteen"]
TENS = ["", "", "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety"]


def words(n):
    out = []
    if n >= 100:
        out.append("one hundred")
        n -= 100
    if n >= 20:
        out.append(TENS[n // 10] + ("-" + ONES[n % 10] if n % 10 else ""))
    elif n > 0:
        out.append(ONES[n])
    return " ".join(out)


def plural(n, one, many):
    return "%d %s" % (n, one if n == 1 else many)


# ------------------------------------------------------------ pictures
OS, OGAP, M = 26, 12, 6          # object cell, extra gap after 5 in a row, margin


def obj(kind, cx, cy):
    if kind == "apples":
        return ("<circle cx='%.1f' cy='%.1f' r='9' fill='#e05a4f' stroke='#9b2d24' stroke-width='1.2'/>"
                "<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='#6b4423' stroke-width='2' stroke-linecap='round'/>"
                "<ellipse cx='%.1f' cy='%.1f' rx='3.6' ry='2' fill='%s' transform='rotate(-30 %.1f %.1f)'/>"
                % (cx, cy + 2, cx, cy - 6, cx + 1, cy - 10, cx + 4.5, cy - 9, GREEN, cx + 4.5, cy - 9))
    if kind == "stars":
        pts = []
        import math
        for k in range(10):
            r = 10.5 if k % 2 == 0 else 4.6
            a = -math.pi / 2 + k * math.pi / 5
            pts.append("%.1f,%.1f" % (cx + r * math.cos(a), cy + 1 + r * math.sin(a)))
        return "<polygon points='%s' fill='#f4c430' stroke='#a57c00' stroke-width='1.2'/>" % " ".join(pts)
    if kind == "balls":
        return ("<circle cx='%.1f' cy='%.1f' r='9.5' fill='#5b9bd5' stroke='#2e5f8a' stroke-width='1.2'/>"
                "<path d='M %.1f %.1f Q %.1f %.1f %.1f %.1f' fill='none' stroke='#ffffff' stroke-width='1.6'/>"
                % (cx, cy, cx - 9, cy, cx, cy - 6, cx + 9, cy))
    if kind == "buttons":
        s = ["<circle cx='%.1f' cy='%.1f' r='9.5' fill='%s' stroke='%s' stroke-width='1.4'/>" % (cx, cy, FILL, GREEN)]
        for dx, dy in [(-2.6, -2.6), (2.6, -2.6), (-2.6, 2.6), (2.6, 2.6)]:
            s.append("<circle cx='%.1f' cy='%.1f' r='1.4' fill='%s'/>" % (cx + dx, cy + dy, GREEN))
        return "".join(s)
    raise ValueError(kind)


def objects_svg(n, kind):
    """n objects in rows of 10. Each row has a small gap after 5, like a ten-frame."""
    rows = [10] * (n // 10) + ([n % 10] if n % 10 else [])
    W = 2 * M + 10 * OS + OGAP
    H = 2 * M + len(rows) * OS
    s = []
    for r, k in enumerate(rows):
        for i in range(k):
            cx = M + OS / 2 + i * OS + (OGAP if i >= 5 else 0)
            cy = M + OS / 2 + r * OS
            s.append(obj(kind, cx, cy))
    assert sum(rows) == n
    return svg_wrap(W, H, "".join(s), "%s in rows of 10" % kind)


TC = 24


def tenframes_svg(n):
    """Two ten-frames side by side; the first one fills up before the second."""
    assert 0 < n <= 20
    m, gap = 4, 16
    W = 2 * m + 2 * 5 * TC + gap
    H = 2 * m + 2 * TC
    s = []
    for f in range(2):
        x0 = m + f * (5 * TC + gap)
        s.append("<rect x='%d' y='%d' width='%d' height='%d' fill='#ffffff' stroke='%s' stroke-width='2'/>"
                 % (x0, m, 5 * TC, 2 * TC, GREEN))
        for i in range(1, 5):
            s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='1.2'/>"
                     % (x0 + i * TC, m, x0 + i * TC, m + 2 * TC, GREEN))
        s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='1.2'/>"
                 % (x0, m + TC, x0 + 5 * TC, m + TC, GREEN))
        for k in range(10):
            if f * 10 + k < n:
                s.append("<circle cx='%.1f' cy='%.1f' r='8' fill='%s'/>"
                         % (x0 + (k % 5) * TC + TC / 2, m + (k // 5) * TC + TC / 2, RED))
    return svg_wrap(W, H, "".join(s), "two ten-frames with dots")


U, RG, CG = 8, 6, 4


def rods_svg(t, o):
    """t ten rods (each 10 cubes tall) and o single cubes. A wider gap after every 5 rods."""
    m, gg = 6, 22
    F = 10 * U
    rx = []
    x = m
    for k in range(t):
        rx.append(x)
        x += U + RG + (6 if k % 5 == 4 else 0)
    s = []
    for x0 in rx:
        s.append("<rect x='%d' y='%d' width='%d' height='%d' fill='%s' stroke='%s' stroke-width='1.5'/>"
                 % (x0, m, U, F, FILL, GREEN))
        for i in range(1, 10):
            s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='0.7'/>"
                     % (x0, m + i * U, x0 + U, m + i * U, GREEN))
    xe = (rx[-1] + U) if rx else m - gg
    cx0 = xe + gg
    for k in range(o):
        cx = cx0 + (k // 5) * (U + CG + 2)
        cy = m + F - U - (k % 5) * (U + CG + 4)
        s.append("<rect x='%d' y='%d' width='%d' height='%d' fill='%s' stroke='%s' stroke-width='1.5'/>"
                 % (cx, cy, U, U, CUBE, GREEN))
    right = (cx0 + ((o - 1) // 5) * (U + CG + 2) + U) if o else xe
    W = right + m
    H = 2 * m + F
    return svg_wrap(W, H, "".join(s), "ten rods and single cubes")


CWID, CHT = 48, 34


def chart_svg(tl, nrows, ncols, target=None, hide=()):
    """A piece of the 120 chart. tl = top-left number. target (r, c) shows a red ?, hide = blank cells."""
    assert (tl - 1) % 10 + ncols <= 10, "piece must stay inside one row of the chart"
    assert tl + 10 * (nrows - 1) + ncols - 1 <= 120
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
    return svg_wrap(W, H, "".join(s), "piece of a 120 chart")


def ones_line_svg(start, n, labels):
    """Number line with n ticks, 1 apart. labels: {index: text}."""
    m, sp, ly = 34, 46, 14
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
    return svg_wrap(W, H, "".join(s), "number line counting by 1s from %d" % start)


def line_q(start, n, labels):
    """Number line question; the answer is computed from the tick that shows ?."""
    nums = {k: start + k for k in range(n)}
    assert all(v == "?" or int(v) == nums[k] for k, v in labels.items())
    k = [k for k, v in labels.items() if v == "?"][0]
    return fig(ones_line_svg(start, n, labels)) + "Each tick is 1 more. What number goes at the ?", nums[k]


def count_e(n, what):
    t, o = divmod(n, 10)
    if n < 10:
        return "Point and count each one: %s. There are <b>%d</b> %s." % (lst(range(1, n + 1)), n, what)
    tens = lst(range(10, 10 * t + 1, 10))
    if o == 0:
        return "Each full row has 10. Count the rows by 10s: %s. There are <b>%d</b> %s." % (tens, n, what)
    return ("Each full row has 10. Count the rows by 10s: %s. Then count on by 1s: %s. There are <b>%d</b> %s."
            % (tens, lst(range(10 * t + 1, n + 1)), n, what))


# ============================================================ set 1: count objects
def set_objects(rnd, P):
    kinds = ["apples", "stars", "balls", "buttons"]
    obs = []
    for i, n in enumerate([8, 10, 13, 15, 17, 20, 22, 24, 26, 28, 30, 19]):
        kind = kinds[i % 4]
        t, o = divmod(n, 10)
        if n < 10:
            cands = [n - 1, n + 1, n + 2]
        elif o == 0:
            cands = [t, n - 1, n + 1, n + 10]
        else:
            cands = [rev(n), n + 1, n - 1, n + 10, t + o]
        cands = [c for c in cands if c]
        obs.append(mcq(fig(objects_svg(n, kind)) + "How many %s are there?" % kind, n, cands, count_e(n, kind)))
    tfs = []
    for n in [11, 14, 16, 18]:
        e = ("The first ten-frame is full. That is 10. Then count on: %s. There are <b>%d</b> dots."
             % (lst(range(11, n + 1)), n))
        tfs.append(mcq(fig(tenframes_svg(n)) + "How many dots are there?", n, [c for c in (rev(n), n - 1, n + 1, n - 10) if c], e))
    rods = []
    for n in [34, 47, 63, 80]:
        t, o = divmod(n, 10)
        if o:
            e = ("Each rod is 10 cubes. Count the rods by 10s: %s. Then count on the cubes: %s. That is <b>%d</b>."
                 % (lst(range(10, 10 * t + 1, 10)), lst(range(10 * t + 1, n + 1)), n))
            cands = [rev(n), t + o, int("%d0%d" % (t, o)), n + 1]
        else:
            e = "Each rod is 10 cubes. Count the rods by 10s: %s. That is <b>%d</b>." % (
                lst(range(10, 10 * t + 1, 10)), n)
            cands = [t, n - 10, n + 10]
        rods.append(mcq(fig(rods_svg(t, o)) + "Each rod has 10 cubes. How many cubes are there in all?", n, cands, e))
    its = [obs[0], obs[1], tfs[0], obs[2], obs[3], tfs[1], obs[11], obs[4], tfs[2], obs[5],
           rods[0], obs[6], tfs[3], obs[7], obs[8], rods[1], obs[9], obs[10], rods[2], rods[3]]
    assert len(its) == 20 and len({id(x) for x in its}) == 20
    return {"title": "Count objects", "items": its}


# ============================================================ set 2: what comes next or before
def set_next(rnd, P):
    its = []

    def add(q, ans, wrong, e):
        its.append(mcq(q, ans, wrong, e))

    def nxt(xs, wrong, e):
        ans = xs[-1] + 1
        add("Count on: %s, ☐. What comes next?" % lst(xs), ans, wrong, e.format(a=ans, l=xs[-1]))

    nxt([14, 15, 16], [18, 71, 15], "Count on by 1s. After {l} comes <b>{a}</b>. 71 has the digits the wrong way.")
    nxt([23, 24, 25], [27, 62, 36], "Count on by 1s. After {l} comes <b>{a}</b>. 27 skips a number.")
    nxt([38, 39], [310, 30, 41],
        "After 39 comes <b>{a}</b>. 9 ones and 1 more make a new ten. So 3 tens become 4 tens. Do not write 310.")
    nxt([46, 47, 48], [50, 94, 59], "After {l} comes <b>{a}</b>. Only the ones digit goes up by 1.")
    nxt([57, 58, 59], [510, 50, 61],
        "After 59 comes <b>{a}</b>. 9 ones and 1 more make a new ten. Do not go back to 50, and do not write 510.")
    nxt([77, 78, 79], [710, 70, 90],
        "After 79 comes <b>{a}</b>. The 9 ones make a new ten with 1 more, so 7 tens become 8 tens.")
    nxt([97, 98, 99], [910, 1000, 90],
        "After 99 comes <b>{a}</b>. 9 tens and 1 more ten make 10 tens. 10 tens is one hundred. Do not write 910.")
    nxt([107, 108, 109], [1010, 100, 111],
        "After 109 comes <b>{a}</b>. 100 and 9 ones, plus 1 more, is 100 and 1 ten. Do not write 1010.")
    nxt([112, 113, 114], [116, 1015, 105], "Count on by 1s. After {l} comes <b>{a}</b>.")
    add("Count on: 28, ☐, 30. What number is missing?", 29, [27, 31, 92],
        "The missing number comes after 28 and before 30. After 28 comes <b>29</b>.")
    add("Count on: 68, 69, ☐, 71. What number is missing?", 70, [610, 60, 72],
        "After 69 comes <b>70</b>, then 71. 9 ones and 1 more make a new ten.")

    def before(n, wrong, e):
        add("What number comes just before %d?" % n, n - 1, wrong, e)

    before(40, [41, 30, 38], "Count back 1 from 40: <b>39</b>. 41 comes just after 40.")
    before(100, [101, 90, 98], "Count back 1 from 100: <b>99</b>. 101 comes just after 100.")
    before(110, [111, 100, 1009], "Count back 1 from 110: <b>109</b>. Write 109, not 1009.")
    add("Count back: 63, 62, 61, ☐. What comes next?", 60, [59, 50, 70],
        "Counting back, each number is 1 less. 61 − 1 = <b>60</b>. 59 skips a number.")
    add("Count back: 86, 85, 84, ☐. What comes next?", 83, [85, 82, 38],
        "Counting back, each number is 1 less. 84 − 1 = <b>83</b>.")
    for start, n, labels, wrong, e in [
        (43, 6, {0: "43", 3: "?"}, [45, 47, 64], "Count on from 43: 44, 45, <b>46</b>. Do not count the first tick."),
        (64, 7, {2: "?", 6: "70"}, [67, 65, 60], "Count back from 70: 69, 68, 67, <b>66</b>. Or count on from 64: 65, 66."),
        (97, 6, {0: "97", 4: "?"}, [100, 102, 1001], "Count on from 97: 98, 99, 100, <b>101</b>."),
        (106, 7, {0: "106", 5: "?"}, [110, 1011, 112], "Count on from 106: 107, 108, 109, 110, <b>111</b>."),
    ]:
        q, ans = line_q(start, n, labels)
        add(q, ans, wrong, e)
    o = its
    # easy to hard: no new ten, then a new ten, then past 100
    order = [o[0], o[1], o[9], o[15], o[3], o[16], o[11], o[2], o[14], o[17],
             o[4], o[10], o[5], o[12], o[6], o[18], o[7], o[13], o[8], o[19]]
    assert len(order) == 20 and len({id(x) for x in order}) == 20
    return {"title": "What comes next or before", "items": order}


# ============================================================ set 3: missing numbers on a 120 chart
def chart_e(tl, tgt, hide, ncols, nrows):
    r, c = tgt
    ans = tl + 10 * r + c
    vis = lambda rr, cc: 0 <= rr < nrows and 0 <= cc < ncols and (rr, cc) not in hide
    if vis(r, c - 1):
        return "The number just left of the ? is %d. Count on 1. The ? is <b>%d</b>." % (ans - 1, ans)
    if vis(r - 1, c):
        return ("The number just above the ? is %d. Going down one row is 10 more. The ? is <b>%d</b>."
                % (ans - 10, ans))
    if vis(r, c + 1):
        return "The number just right of the ? is %d. Count back 1. The ? is <b>%d</b>." % (ans + 1, ans)
    if vis(r + 1, c):
        return ("The number just below the ? is %d. Going up one row is 10 less. The ? is <b>%d</b>."
                % (ans + 10, ans))
    raise ValueError("no helper cell")


def set_chart(rnd, P):
    Q = "This is part of a 120 chart. What number goes in the box with the ?"
    pieces = [
        # tl, rows, cols, target, hide, wrong, e (None = automatic)
        (12, 2, 4, (0, 2), set(), [41, 16, 40], None),
        (23, 2, 4, (1, 1), set(), [43, 44, 32], None),
        (36, 3, 3, (2, 0), set(), [65, 55, 66], None),
        (57, 2, 4, (0, 3), set(), [510, 50, 61], "The row goes 57, 58, 59. After 59 comes <b>60</b>. A row of the chart ends with a ten."),
        (65, 3, 4, (1, 2), {(1, 1)}, [76, 79, 707], None),
        (81, 2, 4, (1, 0), set(), [19, 90, 71], None),
        (97, 2, 4, (0, 3), set(), [910, 1000, 90], "The row goes 97, 98, 99. After 99 comes <b>100</b>."),
        (97, 3, 4, (1, 3), set(), [10010, 1010, 101],
         "The row goes 107, 108, 109. After 109 comes <b>110</b>. You can also look up: 100 + 10 = 110."),
        (93, 3, 4, (1, 2), set(), [1005, 150, 15], "The number just left of the ? is 104. Count on 1. The ? is <b>105</b>. Write 105, not 1005."),
        (101, 2, 5, (1, 4), set(), [1015, 151, 116], None),
        (44, 3, 4, (2, 3), {(2, 2), (1, 3)}, [76, 68, 57], "Count across the bottom row: 64, 65, 66, <b>67</b>."),
        (18, 3, 3, (0, 0), set(), [17, 81, 8], None),
        (106, 2, 5, (0, 0), set(), [1006, 105, 160], None),
        (72, 3, 3, (2, 1), {(2, 0), (1, 1)}, [39, 103, 95], None),
        (88, 2, 3, (0, 2), set(), [810, 80, 91], "The row goes 88, 89. After 89 comes <b>90</b>. 9 ones and 1 more make a new ten."),
        (114, 1, 7, (0, 4), {(0, 3), (0, 5)}, [117, 119, 1018], "Count on from 116: 117, <b>118</b>. The blank box is 117."),
    ]
    pics = []
    for tl, rows, cols, tgt, hide, wrong, e in pieces:
        ans = tl + 10 * tgt[0] + tgt[1]
        e = e or chart_e(tl, tgt, hide, cols, rows)
        assert ("<b>%d</b>" % ans) in e, (ans, e)
        shown = {tl + 10 * r + c for r in range(rows) for c in range(cols) if (r, c) not in hide and (r, c) != tgt}
        assert not shown & set(wrong), (tl, wrong)
        pics.append(mcq(fig(chart_svg(tl, rows, cols, tgt, hide)) + Q, ans, wrong, e))
    txt = [
        mcq("On a 120 chart, which number is just below 57?", 67, [58, 47, 76],
            "Going down one row on the chart is 10 more. 57 + 10 = <b>67</b>. 58 is just to the right."),
        mcq("On a 120 chart, which number is just above 104?", 94, [103, 114, 49],
            "Going up one row on the chart is 10 less. 104 − 10 = <b>94</b>."),
        mcq("A row on a 120 chart starts with 71. Which number ends that row?", 80, [79, 710, 81],
            "Each row has 10 numbers: 71, 72, 73, 74, 75, 76, 77, 78, 79, <b>80</b>."),
        mcq("On a 120 chart, which number starts the row after 110?", 111, [1011, 120, 101],
            "The row after 110 starts with the next number. After 110 comes <b>111</b>."),
    ]
    p = pics
    order = [p[0], p[1], p[3], p[2], p[5], txt[0], p[11], p[14], p[4], p[6],
             txt[2], txt[1], p[8], p[7], p[13], p[12], p[9], p[10], p[15], txt[3]]
    assert len(order) == 20 and len({id(x) for x in order}) == 20
    return {"title": "Missing numbers on a 120 chart", "items": order}


# ============================================================ set 4: read and write numbers
def set_words(rnd, P):
    its = []
    for n, wrong, e in [
        (12, [21, 2, 102], "Twelve is 1 ten and 2 ones. Write <b>12</b>."),
        (16, [61, 60, 106], "Sixteen is 1 ten and 6 ones. The 1 comes first: <b>16</b>. 61 is sixty-one."),
        (19, [91, 90, 109], "Nineteen is 1 ten and 9 ones. Write <b>19</b>. 91 is ninety-one."),
        (30, [13, 3, 300], "Thirty is 3 tens and 0 ones. Write <b>30</b>. 13 is thirteen."),
        (42, [24, 402, 40], "Forty-two is 4 tens and 2 ones. Write <b>42</b>, not 402."),
        (58, [85, 508, 50], "Fifty-eight is 5 tens and 8 ones. Write <b>58</b>, not 508."),
        (73, [37, 703, 70], "Seventy-three is 7 tens and 3 ones. Write <b>73</b>."),
        (99, [909, 90, 19], "Ninety-nine is 9 tens and 9 ones. Write <b>99</b>, not 909."),
        (100, [1000, 10, 101], "One hundred is 10 tens. Write <b>100</b>: a 1 and two zeros."),
        (105, [1005, 150, 15], "One hundred five is 100 and 5 more. Write <b>105</b>. The 0 shows there are no tens. Do not write 1005."),
        (110, [10010, 1010, 101], "One hundred ten is 100 and 1 ten. Write <b>110</b>. Do not write 100 and then 10."),
        (117, [10017, 170, 107], "One hundred seventeen is 100 and 17 more. Write <b>117</b>, not 10017."),
        (120, [10020, 1020, 102], "One hundred twenty is 100 and 2 tens. Write <b>120</b>, not 10020."),
    ]:
        assert ("<b>%d</b>" % n) in e
        its.append(mcq("Which number is “%s”?" % words(n), n, wrong, e))
    for n, wrong, e in [
        (14, ["forty", "forty-one", "four"], "14 is 1 ten and 4 ones. Say <b>fourteen</b>. Forty is 40."),
        (50, ["fifteen", "five", "fifty-one"], "50 is 5 tens and 0 ones. Say <b>fifty</b>. Fifteen is 15."),
        (61, ["sixteen", "sixty", "six one"], "61 is 6 tens and 1 one. Say <b>sixty-one</b>. Sixteen is 16."),
        (103, ["one hundred thirty", "thirteen", "one zero three"],
         "103 is 100 and 3 more. Say <b>one hundred three</b>. One hundred thirty is 130."),
        (115, ["one hundred fifty", "fifteen", "one hundred five"],
         "115 is 100 and 15 more. Say <b>one hundred fifteen</b>. One hundred fifty is 150."),
    ]:
        w = words(n)
        assert ("<b>%s</b>" % w) in e, (w, e)
        its.append(mcq("How do you say %d?" % n, w, wrong, e))
    its.append(mcq("Which number is the same as 10 tens?", 100, [10, 1010, 110],
                   "Count 10 tens by 10s: 10, 20, 30, 40, 50, 60, 70, 80, 90, <b>100</b>."))
    its.append(mcq("Which number is the same as 10 tens and 8 ones?", 108, [1008, 18, 180],
                   "10 tens is 100. 100 and 8 ones is <b>108</b>. Write 108, not 1008."))
    o = its
    # 0-12 numerals from words, 13-17 words from numerals, 18-19 tens
    order = [o[0], o[13], o[1], o[3], o[14], o[2], o[4], o[15], o[5], o[6],
             o[7], o[8], o[18], o[16], o[9], o[19], o[10], o[17], o[11], o[12]]
    assert len(order) == 20 and len({id(x) for x in order}) == 20
    return {"title": "Read and write numbers", "items": order}


BIG_OK.update({1008, 304, 407, 603, 707, 911, 1011, 180, 121})


# ============================================================ set 5: count past 100 and stories
def set_stories(rnd, P):
    its = {}

    def story(key, t, ans, wrong, e, unit=None):
        d = P.next()
        u = (lambda v: plural(v, unit[0], unit[1])) if unit else str
        its[key] = mcq(t.format(**d), u(ans), [u(v) for v in wrong], e.format(**d))

    q, a = line_q(98, 7, {0: "98", 5: "?"})
    its["nl98"] = mcq(q, a, [102, 104, 1003], "Count on from 98: 99, 100, 101, 102, <b>103</b>.")
    q, a = line_q(113, 7, {0: "113", 5: "?"})
    its["nl113"] = mcq(q, a, [117, 119, 1018], "Count on from 113: 114, 115, 116, 117, <b>118</b>.")
    for key, t, o, wrong in [("b106", 10, 6, [1006, 16, 160]), ("b114", 11, 4, [1104, 15, 104]),
                             ("b120", 12, 0, [12, 110, 1020])]:
        n = 10 * t + o
        e = "Count the rods by 10s: %s." % lst(range(10, 10 * t + 1, 10))
        e += (" Then count on the cubes: %s. That is <b>%d</b>." % (lst(range(10 * t + 1, n + 1)), n)) if o else \
            " That is <b>%d</b>." % n
        its[key] = mcq(fig(rods_svg(t, o)) + "Each rod has 10 cubes. How many cubes are there in all?", n, wrong, e)

    story("mia", "{n} counted 97, 98, 99. What number comes next?", 100, [910, 1000, 90],
          "After 99 comes <b>100</b>. 10 tens make one hundred.")
    story("leo", "{n} is reading a book. {He} is on page 108. What page comes next?", 109, [110, 107, 1009],
          "Count on 1 from 108. The next page is <b>109</b>.")
    story("car", "Parking spots are in order. A red car is in spot 59. A blue car is in the next spot. What is the blue car’s spot?",
          60, [510, 50, 61], "After 59 comes <b>60</b>. 9 ones and 1 more make a new ten.")
    story("omar", "{n} counts the steps as {he} walks up: 104, 105, 106. What step comes next?", 107,
          [108, 1007, 117], "Count on 1 from 106. The next step is <b>107</b>.")
    story("ruby", "{n} counts back: 102, 101, 100. What does {he} say next?", 99, [90, 98, 101],
          "Counting back, each number is 1 less. Just before 100 is <b>99</b>.")
    story("kai", "{n} has 110 stickers. {He} gets 1 more sticker. How many stickers does {he} have now?",
          111, [120, 112, 1101], "Count on 1 from 110. {He} has <b>111</b> stickers.", ("sticker", "stickers"))
    story("grace", "{n} is on page 99. {He} reads 2 more pages. What page is {he} on now?", 101, [100, 102, 1001],
          "Count on 2 from 99: 100, <b>101</b>. Do not count page 99.")
    story("day", "The class counts the days of school. Today is day 119. What day is tomorrow?", 120,
          [110, 121, 1110], "Count on 1 from 119. Tomorrow is day <b>120</b>. 9 ones and 1 more make a new ten.")
    its["list1"] = mcq("Which list counts on by 1s?", "98, 99, 100, 101",
                       ["98, 99, 910, 911", "98, 99, 1000, 1001", "98, 99, 90, 91"],
                       "After 99 comes 100, then 101. The right list is <b>98, 99, 100, 101</b>.")
    its["list2"] = mcq("Which list counts on by 1s?", "108, 109, 110, 111",
                       ["108, 109, 1010, 1011", "108, 109, 100, 101", "108, 109, 110, 112"],
                       "After 109 comes 110, then 111. The right list is <b>108, 109, 110, 111</b>.")
    story("noah", "{n} has 10 strings of beads. Each string has 10 beads. {He} has 3 more beads. "
                  "How many beads does {he} have?", 103, [1003, 13, 130],
          "Count the strings by 10s: 10, 20, 30, 40, 50, 60, 70, 80, 90, 100. Then count on 3: 101, 102, <b>103</b>.",
          ("bead", "beads"))
    story("eli", "{n} starts at 112 and counts on 5 more. Where does {he} stop?", 117, [116, 118, 107],
          "Count 5 numbers after 112: 113, 114, 115, 116, <b>117</b>. Do not count 112.")
    story("jack", "Tickets at the fair go 100, 101, 102 … {n} gets the ticket after 104. What is {his} number?",
          105, [1005, 106, 115], "Count on 1 from 104. The number is <b>105</b>. Write 105, not 1005.")
    its["between"] = mcq("Which number comes between 109 and 111?", 110, [1010, 10010, 100],
                         "Count on: 109, <b>110</b>, 111. Write 110, not 1010 or 10010.")
    story("ben", "{n}’s book has 120 pages. Which page comes just before the last page?", 119, [118, 120, 110],
          "The last page is 120. Count back 1 from 120. The page before it is <b>119</b>.")
    k = its
    order = [k["nl98"], k["mia"], k["b106"], k["leo"], k["list1"], k["car"], k["nl113"], k["b114"], k["omar"],
             k["between"], k["kai"], k["ruby"], k["b120"], k["jack"], k["list2"], k["noah"], k["grace"], k["eli"],
             k["day"], k["ben"]]
    assert len(order) == 20 and len({id(x) for x in order}) == 20 and len(its) == 20
    return {"title": "Count past 100 and stories", "items": order}


# ============================================================ lesson
def body_html():
    return (
        "<h2>Counting to 120 means saying the numbers in order</h2>"
        "<p>You can start at any number and count on by 1s. Only the ones digit changes, "
        "until you get to 9 ones. Then 1 more makes a <b>new ten</b>.</p>"
        + table(["Count on", "What happens"], [
            ["37, 38, 39, <b>40</b>", "9 ones and 1 more make a new ten"],
            ["97, 98, 99, <b>100</b>", "10 tens make one hundred"],
            ["107, 108, 109, <b>110</b>", "100 and 1 ten"],
        ]) +
        "<h2>Count objects in rows of 10</h2>"
        "<p>Put things in rows of 10. Count the full rows by 10s. Then count on the rest by 1s.</p>"
        "<figure class='sn-fig'>" + objects_svg(23, "apples") +
        "<figcaption>Count by 10s: 10, 20. Then count on: 21, 22, 23. There are 23 apples.</figcaption></figure>"
        "<p>A rod is 10 cubes. 10 rods are 100 cubes.</p>"
        "<figure class='sn-fig'>" + rods_svg(10, 5) +
        "<figcaption>10 rods and 5 cubes: 100 and 5 more is 105.</figcaption></figure>"
        "<h2>The 120 chart</h2>"
        "<p>Each row has 10 numbers. Go right to count on 1. Go down to get 10 more.</p>"
        "<figure class='sn-fig'>" + chart_svg(97, 3, 4) +
        "<figcaption>After 99 comes 100. After 109 comes 110. Below 100 is 110.</figcaption></figure>"
        + ex("What comes next?", "58, 59, ☐",
             "59 has 9 ones. 1 more makes a new ten, so 5 tens become 6 tens.", "60") +
        "<h2>Read and write numbers</h2>"
        + table(["Word", "Number"], [
            ["sixteen", "16"], ["forty-two", "42"], ["one hundred five", "105"], ["one hundred ten", "110"],
        ]) +
        "<h2>Common mistakes</h2>"
        + table(["Mistake", "What to do instead"], [
            ["Writing 510 after 59", "9 ones and 1 more make a new ten: 60"],
            ["Going back to 50 after 59", "Count on to the next ten: 59, 60"],
            ["Writing 1005 for one hundred five", "Write 105. The 0 means no tens"],
            ["Writing 10010 for one hundred ten", "Write 110"],
            ["Writing 61 for sixteen", "Teen numbers start with 1: 16"],
        ])
    )


FAQ = [
    {"q": "How high should a 1st grader count?",
     "a": "By the end of Grade 1, children should count to 120. They should also start at any number, like 87, and count on from there."},
    {"q": "How do you teach counting past 100?",
     "a": "Use a 120 chart and count 98, 99, 100, 101 out loud. Show that 101 to 120 work just like 1 to 20, with a 1 hundred in front."},
    {"q": "Why does my child write 1005 for 105?",
     "a": "They write 100 and then 5, just as they hear it. Show that 105 is 1 hundred, 0 tens and 5 ones, so it has only three digits."},
    {"q": "What is a 120 chart?",
     "a": "It is a grid with the numbers 1 to 120 in rows of 10. Moving right is 1 more and moving down is 10 more, so it helps children find missing numbers."},
]


def gen():
    rnd = random.Random(105)
    P = People(rnd)
    sets = [set_objects(rnd, P), set_next(rnd, P), set_chart(rnd, P), set_words(rnd, P), set_stories(rnd, P)]
    balance(sets, rnd)
    seen = set()
    for s in sets:
        assert len(s["items"]) == 20, (s["title"], len(s["items"]))
        assert sorted(it["a"] for it in s["items"]) == sorted([0, 1, 2, 3] * 5)
        for it in s["items"]:
            assert len(set(it["c"])) == 4, it
            for c in it["c"]:
                for tok in re.findall(r"\d+", c):
                    v = int(tok)
                    assert 1 <= v <= 120 or v in BIG_OK, c
            key = it["q"] + "|".join(sorted(it["c"]))
            assert key not in seen, it["q"]
            seen.add(key)
    u = {
        "country": "us", "subject": "math", "grade": "grade-1", "slug": "count-to-120", "sort": 5,
        "updated": UPDATED, "pdf_url": "",
        "title": "Count to 120: Count On, Read and Write Numbers",
        "seo_title": "Grade 1 Counting to 120 Worksheets: Count On, 120 Chart, Read and Write Numbers",
        "short_title": "Count to 120",
        "domain": "Number and Operations in Base Ten",
        "standard_code": "1.NBT.A.1",
        "standard_url": "https://www.thecorestandards.org/Math/Content/1/NBT/A/1/",
        "standard_text": "Count to 120, starting at any number less than 120. In this range, read and write numerals "
                         "and represent a number of objects with a written numeral.",
        "meta_desc": "Free Grade 1 counting to 120 worksheets: count objects in rows of 10, say what comes next "
                     "(59, 60 and 109, 110), fill in a 120 chart, read and write number words, and count past 100. "
                     "100 practice questions with an answer key and simple explanations.",
        "key_big": "Count on by 1s. After 9 ones comes a new ten: 59, 60 and 109, 110.",
        "key_sub": "10 tens make 100. Then keep going: 101, 102 … 120. Write one hundred five as 105, not 1005.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }
    mark_large(u, "(\\w+ in rows of 10|number line counting|ten rods)")
    return u


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
