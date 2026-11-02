# -*- coding: utf-8 -*-
"""
US Grade 2 Math: Skip Counting by 5s, 10s and 100s (2.NBT.A.2)
  python tools/gen_us_math_g2_skip_counting.py
Count by 5s with hands, nickels and tally marks; by 10s and 100s from any number;
count on and back across a hundred; mixed patterns and stories.
Every answer and every picture is computed and checked in code.
HTML attributes use single quotes (no backslashes in the JSON).
"""
import json, os, random, re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "us", "math", "grade-2")
UPDATED = "2026-11-02"
GREEN = "#006633"
FILL = "#cfe6d6"
RED = "#c0392b"
INK = "#2b2b2b"
FONT = "Arial, Helvetica, sans-serif"
GIRLS = ["Maya", "Ava", "Mia", "Zoe", "Lily", "Emma", "Nora", "Ruby", "Sofia", "Grace"]
BOYS = ["Leo", "Noah", "Eli", "Sam", "Ben", "Omar", "Kai", "Jack", "Luis", "Owen"]
# wrong answers above 1000 that show a real mistake (199 -> 1100, 392 -> 3102 …)
BIG_OK = {1100, 2100, 1101, 1001, 3102, 5100, 6100, 9100, 9910, 3410, 2910}


# ------------------------------------------------------------ helpers
def mcq(q, correct, cands, e):
    """4 choices: correct + the first 3 unique distractors. Positions are set later by balance()."""
    correct = str(correct)
    seen = {correct}
    pick = []
    for c in cands:
        c = str(c)
        lead = c.split(" ")[0]
        if c in seen or not c or lead.startswith("-") or lead in ("0", "0¢"):
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


def mark_large(u, pattern):
    """Tag pictures that must print larger so they stay readable."""
    rx = re.compile(r"<svg (?=[^>]*aria-label='" + pattern + ")")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u


def lst(xs):
    return ", ".join(str(x) for x in xs)


def counts(start, step, n):
    return [start + step * k for k in range(n)]


# ------------------------------------------------------------ pictures
def rows_of(n, per):
    """Split n things into rows of at most `per`, as even as possible (7 -> 4 + 3)."""
    r = (n + per - 1) // per
    base, extra = divmod(n, r)
    return [base + (1 if i < extra else 0) for i in range(r)]


HW, HH, HGAP = 40, 58, 10


def hand(x, y):
    """One hand, 4 fingers and a thumb, in a 40 × 58 box."""
    s = []
    for k, top in enumerate([10, 3, 5, 12]):
        s.append("<rect x='%.1f' y='%.1f' width='6.5' height='%d' rx='3.2' fill='%s' stroke='%s' stroke-width='1.5'/>"
                 % (x + 11 + k * 7, y + top, 36 - top, FILL, GREEN))
    s.append("<rect x='%.1f' y='%.1f' width='7' height='20' rx='3.5' fill='%s' stroke='%s' stroke-width='1.5' "
             "transform='rotate(-38 %.1f %.1f)'/>" % (x + 6, y + 22, FILL, GREEN, x + 9.5, y + 42))
    s.append("<rect x='%.1f' y='%.1f' width='30' height='26' rx='8' fill='%s' stroke='%s' stroke-width='1.5'/>"
             % (x + 9, y + 30, FILL, GREEN))
    return "".join(s)


def hands_svg(n):
    m = 6
    rows = rows_of(n, 5)
    W = 2 * m + max(rows) * HW + (max(rows) - 1) * HGAP
    H = 2 * m + len(rows) * HH + (len(rows) - 1) * 8
    s = []
    for r, k in enumerate(rows):
        for i in range(k):
            s.append(hand(m + i * (HW + HGAP), m + r * (HH + 8)))
    return svg_wrap(W, H, "".join(s), "%d hands" % n)


NR = 21


def nickels_svg(n):
    m = 4
    rows = rows_of(n, 5)
    d = 2 * NR + 8
    W = 2 * m + max(rows) * d - 8
    H = 2 * m + len(rows) * d - 8
    s = []
    for r, k in enumerate(rows):
        for i in range(k):
            cx, cy = m + NR + i * d, m + NR + r * d
            s.append("<circle cx='%d' cy='%d' r='%d' fill='#dfe3e7' stroke='#7a828a' stroke-width='2'/>" % (cx, cy, NR))
            s.append("<circle cx='%d' cy='%d' r='%d' fill='none' stroke='#9aa2aa' stroke-width='1'/>" % (cx, cy, NR - 4))
            s.append(text(cx, cy + 6, "5¢", 16))
    return svg_wrap(W, H, "".join(s), "%d nickels" % n)


TG, TH = 8, 38


def tally_svg(groups, extra=0):
    """Tally marks: groups of 5 (4 sticks and a slash), then `extra` single sticks."""
    m = 8
    units = [4] * groups + ([extra] if extra else [])
    full = [True] * groups + ([False] if extra else [])
    rows = rows_of(len(units), 4)
    uw = 3 * TG + 12            # width of one group with the slash overhang
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
    """A piece of the hundred chart. tl = top-left number. target (r, c) shows a red ?, hide = blank cells."""
    assert (tl - 1) % 10 + ncols <= 10, "piece must stay inside one row of the hundred chart"
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
    return svg_wrap(W, H, "".join(s), "hundred chart piece")


def jw(j):
    j = abs(j)
    return 96 if j >= 100 else 74 if j >= 10 else 56


def nline_svg(start, jumps, ticks=None, jlabels=None):
    """Open number line. Jumps go right for +, left for −. ticks: one label per point (None = no label)."""
    if ticks is None:
        ticks = [str(start)] + [None] * (len(jumps) - 1) + ["?"]
    if jlabels is None:
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


# ============================================================ set 1: count by 5s
def set_fives(rnd, P):
    its = []
    hands = []
    for n in [3, 4, 6, 8]:
        e = "Each hand has 5 fingers. Count by 5s, one hand at a time: %s. There are <b>%d</b> fingers." % (
            lst(counts(5, 5, n)), 5 * n)
        hands.append(mcq(fig(hands_svg(n)) + "Count by 5s. How many fingers are there in all?", 5 * n,
                         [n, 10 * n, 5 * (n - 1), 5 * (n + 1)], e))
    nick = []
    for n in [4, 5, 7, 9]:
        e = "A nickel is worth 5¢. Count by 5s: %s. That is <b>%d¢</b>." % (lst(counts(5, 5, n)), 5 * n)
        nick.append(mcq(fig(nickels_svg(n)) + "Each nickel is worth 5¢. How much money is this?", "%d¢" % (5 * n),
                        ["%d¢" % v for v in (n, 10 * n, 5 * (n - 1), 5 * (n + 1))], e))
    tal = []
    for g in [4, 5, 7]:
        e = ("Each group has 4 sticks and 1 slash. That is 5 marks. Count by 5s: %s. There are <b>%d</b> marks."
             % (lst(counts(5, 5, g)), 5 * g))
        tal.append(mcq(fig(tally_svg(g)) + "How many tally marks are there?", 5 * g, [4 * g, g, 5 * (g - 1), 5 * (g + 1)], e))
    tal.append(mcq(fig(tally_svg(3, 2)) + "How many tally marks are there?", 17, [14, 20, 16],
                   "Count the groups by 5s: 5, 10, 15. Then count on by 1s for the 2 single sticks: 16, 17. "
                   "There are <b>17</b> marks."))

    seq = []
    seq.append(mcq("Count by 5s: 5, 10, 15, ☐. What comes next?", 20, [16, 25, 30],
                   "Each number is 5 more. 15 + 5 = <b>20</b>."))
    seq.append(mcq("Count by 5s: 35, 40, 45, ☐. What comes next?", 50, [46, 55, 60],
                   "Each number is 5 more. 45 + 5 = <b>50</b>. 46 is counting by 1s."))
    seq.append(mcq("Count by 5s: 85, 90, 95, ☐. What comes next?", 100, [910, 96, 105],
                   "95 + 5 = <b>100</b>. After 95 comes 100, not 910. 9 tens and 1 more ten make 1 hundred."))
    seq.append(mcq("Count by 5s: 20, 25, ☐, 35. What number is missing?", 30, [26, 40, 36],
                   "The missing number comes after 25 and before 35. 25 + 5 = <b>30</b>, and 30 + 5 = 35."))
    seq.append(mcq("Count back by 5s: 60, 55, 50, ☐. What comes next?", 45, [49, 40, 55],
                   "Counting back, each number is 5 less. 50 − 5 = <b>45</b>. 49 is counting back by 1s."))
    seq.append(mcq("Count by 5s: 110, 115, 120, ☐. What comes next?", 125, [121, 130, 220],
                   "Each number is 5 more. 120 + 5 = <b>125</b>. The hundreds digit stays 1."))
    idea = [
        mcq("When you count by 5s from 0, what is the last digit of each number?", "0 or 5",
            ["only 5", "only 0", "any digit"],
            "0, 5, 10, 15, 20, 25 … The last digit goes 0, 5, 0, 5. So it is always <b>0 or 5</b>."),
        mcq("Count by 5s from 0. Which number do you say?", 45, [42, 54, 48],
            "When you count by 5s from 0, every number ends in 0 or 5. <b>45</b> ends in 5. "
            "42, 54 and 48 do not."),
    ]
    its = [hands[0], seq[0], nick[0], tal[0], hands[1], seq[1], nick[1], idea[0], tal[1], seq[3],
           hands[2], nick[2], seq[4], tal[2], idea[1], seq[2], hands[3], nick[3], tal[3], seq[5]]
    assert len(its) == 20, len(its)
    return {"title": "Count by 5s", "items": its}


# ============================================================ set 2: count by 10s from any number
def set_tens(rnd, P):
    fwd, back, line, chart = [], [], [], []
    for a in [37, 14, 52, 125, 263, 418]:
        s = counts(a, 10, 3)
        ans = a + 30
        last = s[-1]
        e = ("Each number is 10 more. Only the tens digit goes up by 1. The ones digit stays %d. %d + 10 = <b>%d</b>."
             % (a % 10, last, ans))
        fwd.append(mcq("Count by 10s: %s, ☐. What comes next?" % lst(s), ans, [last + 1, last + 11, last + 100, last + 20], e))
    for a in [93, 486, 271]:
        s = counts(a, -10, 3)
        last = s[-1]
        e = "Counting back by 10s, each number is 10 less. The ones digit stays %d. %d − 10 = <b>%d</b>." % (
            a % 10, last, last - 10)
        back.append(mcq("Count back by 10s: %s, ☐. What comes next?" % lst(s), last - 10, [last - 1, last - 11, last - 20], e))
    mid = []
    for a in [46, 305]:
        q = "Count by 10s: %d, ☐, %d, %d. What number is missing?" % (a, a + 20, a + 30)
        e = "The missing number is 10 more than %d. %d + 10 = <b>%d</b>. Then %d + 10 = %d." % (a, a, a + 10, a + 10, a + 20)
        mid.append(mcq(q, a + 10, [a + 1, a + 19, a + 40], e))
    for tl, rows, cols, tgt, hide in [(23, 3, 4, (2, 1), {(1, 2), (2, 3)}), (45, 3, 4, (1, 3), {(2, 0), (0, 1)}),
                                      (162, 3, 4, (2, 2), {(0, 3), (1, 0)}), (516, 3, 4, (2, 0), {(1, 3), (2, 2)})]:
        ans = tl + 10 * tgt[0] + tgt[1]
        above = ans - 10
        assert tgt[0] > 0 and (tgt[0] - 1, tgt[1]) not in hide
        e = ("In a hundred chart, each row is 10 more than the row above. The number above the ? is %d. "
             "%d + 10 = <b>%d</b>." % (above, above, ans))
        chart.append(mcq(fig(chart_svg(tl, rows, cols, tgt, hide)) + "This is part of a hundred chart. "
                         "What number goes in the box with the ?", ans, [above + 1, ans + 10, ans + 1, ans - 1], e))
    for start, n in [(26, 3), (148, 4), (365, 3)]:
        end = start + 10 * n
        pts = counts(start, 10, n + 1)
        e = "Each jump is +10. Count by 10s from %d: %s. You land on <b>%d</b>." % (start, lst(pts[1:]), end)
        line.append(mcq(fig(nline_svg(start, [10] * n)) + "Start at %d. Make the jumps. Where do you land?" % start,
                        end, [start + n, end - 10, end + 10], e))
    pts = counts(84, -10, 4)
    line.append(mcq(fig(nline_svg(84, [-10] * 3)) + "Start at 84. Jump back. Where do you land?", 54, [81, 64, 114],
                    "Each jump is back 10. Count back by 10s: %s. You land on <b>54</b>." % lst(pts[1:])))
    idea = mcq("Count by 10s: 37, 47, 57. Which digit changes each time?", "the tens digit",
               ["the ones digit", "the hundreds digit", "both digits"],
               "37, 47, 57: the 7 stays the same. The 3, 4, 5 go up by 1. That is <b>the tens digit</b>.")
    its = [fwd[0], chart[0], fwd[1], line[0], idea, back[0], fwd[2], mid[0], chart[1], line[1],
           fwd[3], back[1], chart[2], line[3], fwd[4], mid[1], line[2], back[2], chart[3], fwd[5]]
    assert len(its) == 20, len(its)
    return {"title": "Count by 10s from any number", "items": its}


# ============================================================ set 3: count by 100s from any number
def set_hundreds(rnd, P):
    fwd, back, line = [], [], []
    for a in [240, 108, 315, 52, 436, 199]:
        s = counts(a, 100, 3)
        last = s[-1]
        e = ("Each number is 100 more. Only the hundreds digit goes up by 1. %d + 100 = <b>%d</b>." % (last, last + 100))
        fwd.append(mcq("Count by 100s: %s, ☐. What comes next?" % lst(s), last + 100, [last + 10, last + 1, last + 200], e))
    for a in [975, 610, 999]:
        s = counts(a, -100, 3)
        last = s[-1]
        e = "Counting back by 100s, the hundreds digit goes down by 1. %d − 100 = <b>%d</b>." % (last, last - 100)
        back.append(mcq("Count back by 100s: %s, ☐. What comes next?" % lst(s), last - 100, [last - 10, last - 1, last - 200], e))
    top = mcq("Count by 100s: 700, 800, 900, ☐. What comes next?", 1000, [9100, 910, 901],
              "900 + 100 = <b>1000</b>. 9 hundreds and 1 more hundred make 10 hundreds. 10 hundreds is one thousand.")
    mid = []
    for a in [163, 507]:
        q = "Count by 100s: %d, ☐, %d, %d. What number is missing?" % (a, a + 200, a + 300)
        e = "The missing number is 100 more than %d. %d + 100 = <b>%d</b>." % (a, a, a + 100)
        mid.append(mcq(q, a + 100, [a + 10, a + 1, a + 110], e))
    for start, n in [(150, 3), (230, 4)]:
        end = start + 100 * n
        e = "Each jump is +100. Count by 100s from %d: %s. You land on <b>%d</b>." % (
            start, lst(counts(start + 100, 100, n)), end)
        line.append(mcq(fig(nline_svg(start, [100] * n)) + "Start at %d. Make the jumps. Where do you land?" % start,
                        end, [start + n, start + 10 * n, end + 100], e))
    line.append(mcq(fig(nline_svg(920, [-100] * 3)) + "Start at 920. Jump back. Where do you land?", 620, [917, 890, 520],
                    "Each jump is back 100. Count back by 100s: 820, 720, 620. You land on <b>620</b>."))
    idea = [
        mcq("Count by 100s: 264, 364, 464. Which digit changes each time?", "the hundreds digit",
            ["the tens digit", "the ones digit", "all the digits"],
            "The 64 stays the same. The 2, 3, 4 go up by 1. That is <b>the hundreds digit</b>."),
        mcq("Which list counts by 100s?", "312, 412, 512", ["312, 322, 332", "312, 313, 314", "312, 413, 514"],
            "Counting by 100s, only the hundreds digit goes up by 1: <b>312, 412, 512</b>. "
            "312, 322, 332 counts by 10s."),
    ]
    nm, he, his = P.next()
    on = [mcq("Start at 425. Count on by 100s three times. Where do you stop?", 725, [455, 428, 825],
              "Count by 100s three times: 525, 625, <b>725</b>. Do not count 425 as one of the three."),
          mcq("Start at 680. Count back by 100s two times. Where do you stop?", 480, [660, 678, 380],
              "Count back by 100s two times: 580, <b>480</b>.")]
    jumps = mcq("%s starts at 300 and counts by 100s to 800. How many jumps does %s make?" % (nm, he), 5, [500, 6, 8],
                "Count the jumps: 400, 500, 600, 700, 800. That is <b>5</b> jumps. Do not count 300, because that is "
                "where %s starts." % he)
    its = [fwd[0], line[0], fwd[1], idea[0], back[0], fwd[2], mid[0], idea[1], fwd[3], line[1],
           back[1], on[0], fwd[4], mid[1], top, line[2], back[2], on[1], fwd[5], jumps]
    assert len(its) == 20, len(its)
    return {"title": "Count by 100s from any number", "items": its}


# ============================================================ set 4: count on and back across a hundred
def set_across(rnd, P):
    lines = []
    for start, n, labels, ans, wrong, e in [
        (196, 7, {0: "196", 4: "?"}, 200, [1100, 1000, 201],
         "Count on by 1s from 196: 197, 198, 199, <b>200</b>. After 199 comes 200."),
        (397, 7, {0: "397", 5: "?"}, 402, [401, 403, 392],
         "Count on by 1s from 397: 398, 399, 400, 401, <b>402</b>. Count each jump, not the first tick."),
        (595, 7, {0: "595", 6: "?"}, 601, [600, 602, 691],
         "Count on by 1s from 595: 596, 597, 598, 599, 600, <b>601</b>."),
        (797, 7, {1: "?", 6: "803"}, 798, [799, 797, 808],
         "Count back by 1s from 803: 802, 801, 800, 799, <b>798</b>."),
    ]:
        nums = {k: start + k for k in range(n)}
        assert nums[[k for k, v in labels.items() if v == "?"][0]] == ans
        assert all(v == "?" or int(v) == nums[k] for k, v in labels.items())
        lines.append(mcq(fig(ones_line_svg(start, n, labels)) + "Each tick is 1 more. What number goes at the ?",
                         ans, wrong, e))
    nxt = [
        mcq("Count on: 197, 198, 199, ☐. What comes next?", 200, [1100, 1000, 201],
            "199 + 1 = <b>200</b>. 9 ones and 1 more make a ten. 9 tens and 1 more ten make a hundred. "
            "So 199 becomes 200, not 1100."),
        mcq("Count on: 597, 598, 599, ☐. What comes next?", 600, [5100, 590, 700],
            "599 + 1 = <b>600</b>. The ones and tens become 0, and the hundreds go up by 1."),
        mcq("What number comes just after 999?", 1000, [9910, 9100, 998],
            "999 + 1 = <b>1000</b>. 9 hundreds and 1 more hundred make 10 hundreds, which is one thousand."),
        mcq("Count on: 348, 349, ☐, 351. What number is missing?", 350, [3410, 340, 352],
            "349 + 1 = <b>350</b>. 9 ones and 1 more make a new ten. Then 350 + 1 = 351."),
        mcq("Count by 10s: 670, 680, 690, ☐. What comes next?", 700, [6100, 691, 790],
            "690 + 10 = <b>700</b>. 9 tens and 1 more ten make a new hundred. So 6 hundreds become 7 hundreds."),
        mcq("Count by 10s: 372, 382, 392, ☐. What comes next?", 402, [3102, 393, 492],
            "392 + 10 = <b>402</b>. 9 tens and 1 more ten make a new hundred, and the ones stay 2."),
    ]
    back = [
        mcq("Count back: 402, 401, 400, ☐. What comes next?", 399, [300, 390, 499],
            "400 − 1 = <b>399</b>. Just before 400 is 399. The hundreds go down to 3, and the tens and ones become 9."),
        mcq("Count back: 703, 702, 701, 700, ☐. What comes next?", 699, [600, 690, 799],
            "700 − 1 = <b>699</b>. Just before a hundred, the tens and ones are 9."),
        mcq("Count back by 10s: 520, 510, 500, ☐. What comes next?", 490, [590, 400, 499],
            "500 − 10 = <b>490</b>. Going back past 500, the hundreds go down to 4, and the tens become 9."),
        mcq("Count back by 5s: 315, 310, 305, ☐. What comes next?", 300, [304, 295, 310],
            "305 − 5 = <b>300</b>. Each number is 5 less."),
        mcq("What number comes just before 600?", 599, [500, 590, 601],
            "Count back 1 from 600: <b>599</b>. 601 comes just after 600."),
        mcq("Count back by 100s: 350, 250, 150, ☐. What comes next?", 50, [140, 149, 250],
            "150 − 100 = <b>50</b>. Take away 1 hundred, and there are no hundreds left. 5 tens are still there."),
    ]
    nm, he, his = P.next()
    other = [
        mcq("%s starts at 597 and counts on 6 more. Where does %s stop?" % (nm, he), 603, [602, 604, 593],
            "Count 6 numbers after 597: 598, 599, 600, 601, 602, <b>603</b>. Do not count 597."),
        mcq("Count on: 298, 299, ☐, 301. What number is missing?", 300, [2910, 2100, 290],
            "299 + 1 = <b>300</b>. 9 tens and 1 more ten make a new hundred. Then 300 + 1 = 301."),
        mcq("Which list counts on by 1s?", "198, 199, 200, 201",
            ["198, 199, 1100, 1101", "198, 199, 190, 191", "198, 199, 1000, 1001"],
            "After 199 comes 200, then 201. The right list is <b>198, 199, 200, 201</b>."),
        mcq("Count back: 1000, 999, 998, ☐. What comes next?", 997, [990, 996, 999],
            "Each number is 1 less. 998 − 1 = <b>997</b>."),
    ]
    its = [nxt[0], lines[0], back[0], nxt[3], other[1], back[4], lines[1], nxt[1], back[1], other[2],
           nxt[4], back[2], lines[2], other[0], nxt[5], back[3], lines[3], nxt[2], back[5], other[3]]
    assert len(its) == 20, len(its)
    return {"title": "Count on and back across a hundred", "items": its}


# ============================================================ set 5: patterns and word problems
def set_stories(rnd, P):
    def who():
        nm, he, his = P.next()
        return dict(n=nm, he=he, He=cap(he), his=his)

    its = []

    def story(t, ans, unit, wrong, e, d=None):
        d = d or who()
        q = t.format(**d)
        u = (lambda v: "%d%s" % (v, unit)) if unit in ("¢", "") else (lambda v: "%d %s" % (v, unit))
        its.append(mcq(q, u(ans), [u(v) for v in wrong], e.format(**d)))

    story("{n} counts the fingers on 7 hands. Each hand has 5 fingers. How many fingers are there?", 35, "fingers",
          [7, 70, 30, 40], "Count by 5s 7 times: 5, 10, 15, 20, 25, 30, 35. There are <b>35</b> fingers.")
    story("{n} has 6 nickels. A nickel is worth 5¢. How much money does {he} have?", 30, "¢",
          [6, 60, 35, 25], "Count by 5s 6 times: 5, 10, 15, 20, 25, 30. That is <b>30¢</b>.")
    story("{n} reads 10 pages each day. How many pages does {he} read in 8 days?", 80, "pages",
          [18, 8, 90, 70], "Count by 10s 8 times: 10, 20, 30, 40, 50, 60, 70, 80. That is <b>80</b> pages.")
    story("A store has 6 boxes. Each box has 100 pencils. How many pencils are there?", 600, "pencils",
          [106, 60, 700, 500], "Count by 100s 6 times: 100, 200, 300, 400, 500, 600. There are <b>600</b> pencils.")
    story("{n} has 120 stamps. {He} gets 10 more stamps each week. How many stamps does {he} have after 4 weeks?",
          160, "stamps", [124, 520, 150, 170],
          "Start at 120 and count by 10s 4 times: 130, 140, 150, 160. {He} has <b>160</b> stamps.")
    story("{n} has 900 points in a game. {He} loses 100 points each turn. How many points does {he} have after 3 turns?",
          600, "points", [870, 897, 500],
          "Start at 900 and count back by 100s 3 times: 800, 700, 600. {He} has <b>600</b> points.")
    d = who()
    its.append(mcq("{n} counts {his} nickels: 5, 10, 15, 20, 25, 30, 35. How many nickels does {he} have?".format(**d),
                   7, [35, 6, 8],
                   "{He} says one number for each nickel. There are 7 numbers, so {he} has <b>7</b> nickels. "
                   "35¢ is how much they are worth.".format(**d)))
    story("{n} has 3 dimes and 2 nickels. How much money is that?", 40, "¢", [50, 25, 5, 35],
          "Count the dimes by 10s: 10, 20, 30. Then count the nickels by 5s: 35, 40. That is <b>40¢</b>.")
    its.append(mcq(fig(tally_svg(6, 3)) + "The class voted with tally marks. How many votes are there?", 33, [27, 30, 9, 38],
                   "Count the 6 groups by 5s: 5, 10, 15, 20, 25, 30. Then count on 3 single sticks: 31, 32, 33. "
                   "There are <b>33</b> votes."))
    rules = ["Count by 1s", "Count by 5s", "Count by 10s", "Count by 100s",
             "Count back by 5s", "Count back by 10s", "Count back by 100s"]
    for xs, right, e in [
        ([345, 355, 365, 375], "Count by 10s", "Only the tens digit goes up by 1 each time: 345, 355, 365, 375. The rule is <b>count by 10s</b>."),
        ([520, 515, 510, 505], "Count back by 5s", "The numbers get smaller by 5 each time: 520, 515, 510, 505. The rule is <b>count back by 5s</b>."),
        ([128, 228, 328, 428], "Count by 100s", "Only the hundreds digit goes up by 1 each time. The rule is <b>count by 100s</b>."),
    ]:
        wrong = {"Count by 10s": ["Count by 5s", "Count by 1s", "Count by 100s"],
                 "Count back by 5s": ["Count by 5s", "Count back by 10s", "Count back by 1s"],
                 "Count by 100s": ["Count by 10s", "Count by 1s", "Count back by 100s"]}[right]
        its.append(mcq("What is the rule? %s" % lst(xs), right, wrong, e))
    its.append(mcq("You count by 5s from 5. Which number do you NOT say?", 62, [40, 55, 70],
                   "Counting by 5s from 5, every number ends in 0 or 5. 40, 55 and 70 do. <b>62</b> ends in 2, so you do not say it."))
    d = who()
    its.append(mcq("{n} counts by 10s from 7: 7, 17, 27 … Which number will {he} say?".format(**d), 57, [50, 75, 68],
                   "Counting by 10s from 7, the ones digit is always 7: 7, 17, 27, 37, 47, <b>57</b>.".format(**d)))
    d = who()
    its.append(mcq("{n} counts down for a rocket by 10s: 100, 90, 80 … What does {he} say after 40?".format(**d), 30,
                   [39, 50, 20], "Counting back by 10s, each number is 10 less. 40 − 10 = <b>30</b>.".format(**d)))
    story("{n} has 250 points. {He} gets 100 points for each level. How many points does {he} have after 3 more levels?",
          550, "points", [280, 253, 650],
          "Start at 250 and count by 100s 3 times: 350, 450, 550. {He} has <b>550</b> points.")
    story("A box has 10 crayons. {n} has 9 boxes. How many crayons does {he} have?", 90, "crayons", [19, 9, 100],
          "Count by 10s 9 times: 10, 20, 30, 40, 50, 60, 70, 80, 90. {He} has <b>90</b> crayons.")
    story("A pack has 10 stickers. {n} has 4 packs and 5 more stickers. How many stickers does {he} have?",
          45, "stickers", [9, 405, 54],
          "Count the packs by 10s: 10, 20, 30, 40. Then count on 5 by 1s: 41, 42, 43, 44, 45. {He} has <b>45</b> stickers.")
    story("A bag has 100 beads. {n} has 3 bags and 2 strings of 10 beads. How many beads does {he} have?",
          320, "beads", [5, 302, 230],
          "Count the bags by 100s: 100, 200, 300. Then count the strings by 10s: 310, 320. {He} has <b>320</b> beads.")
    story("{n} jumps by 5s on a number path. {He} starts at 0. Where is {he} after 9 jumps?", 45, "",
          [9, 14, 50], "Count by 5s 9 times: 5, 10, 15, 20, 25, 30, 35, 40, 45. {He} is on <b>45</b>.")
    its_order = its
    assert len(its_order) == 20, len(its_order)
    # easy stories first, puzzles and mixed counting last
    k = its_order
    its = [k[0], k[1], k[2], k[16], k[19], k[9], k[14], k[3], k[12], k[6],
           k[4], k[10], k[13], k[5], k[15], k[11], k[7], k[8], k[17], k[18]]
    assert len({id(x) for x in its}) == 20
    return {"title": "Patterns and word problems", "items": its}


# ============================================================ lesson
def body_html():
    return (
        "<h2>Skip counting means jumping by the same number</h2>"
        "<p>When you skip count, you do not say every number. You jump by the same amount each time: "
        "by <b>5s</b>, by <b>10s</b> or by <b>100s</b>. It is a fast way to count many things.</p>"
        + table(["Count by", "Example", "What changes"], [
            ["5s", "5, 10, 15, 20, 25", "The last digit goes 5, 0, 5, 0"],
            ["10s", "37, 47, 57, 67", "Only the tens digit"],
            ["100s", "240, 340, 440, 540", "Only the hundreds digit"],
        ]) +
        "<h2>Count by 5s</h2>"
        "<p>Use hands, nickels or tally marks. Each one is a group of 5.</p>"
        "<figure class='sn-fig'>" + hands_svg(4) +
        "<figcaption>4 hands: 5, 10, 15, 20. There are 20 fingers.</figcaption></figure>"
        "<h2>Count by 10s from any number</h2>"
        "<p>You can start at any number, not only at 10. The ones digit stays the same.</p>"
        "<figure class='sn-fig'>" + nline_svg(37, [10, 10, 10], ticks=["37", "47", "57", "67"]) +
        "<figcaption>Start at 37 and jump +10 three times: 47, 57, 67.</figcaption></figure>"
        "<p>On a hundred chart, the number just below is 10 more.</p>"
        "<figure class='sn-fig'>" + chart_svg(34, 3, 4, (2, 1)) +
        "<figcaption>Below 45 is 55. The ? is 55.</figcaption></figure>"
        + ex("Count by 100s", "Count by 100s: 108, 208, 308, ☐",
             "Only the hundreds digit goes up by 1. The 08 stays the same.", "408") +
        "<h2>Crossing a hundred</h2>"
        "<p>10 ones make a ten, and <b>10 tens make a hundred</b>. So after 199 comes 200, "
        "and after 390 (counting by 10s) comes 400.</p>"
        + table(["Count by", "Across a hundred"], [
            ["1s", "197, 198, 199, <b>200</b>, 201"],
            ["10s", "372, 382, 392, <b>402</b>, 412"],
            ["1s, back", "402, 401, 400, <b>399</b>, 398"],
        ]) +
        "<h2>Common mistakes</h2>"
        + table(["Mistake", "What to do instead"], [
            ["Changing the ones digit when counting by 10s: 37, 47, 58", "Keep the ones digit: 37, 47, 57"],
            ["Changing the tens digit when counting by 100s: 240, 340, 450", "Only the hundreds change: 440"],
            ["Writing 1100 or 1000 after 199", "199 + 1 = 200"],
            ["Writing 3102 after 392 when counting by 10s", "10 tens make a hundred: 402"],
            ["Counting tally groups as 4", "Each group has 5 marks: 4 sticks and a slash"],
        ])
    )


FAQ = [
    {"q": "What is skip counting in 2nd grade?",
     "a": "Skip counting is counting by the same number each time instead of by 1s. Grade 2 students skip count by 5s, 10s and 100s within 1000, for example 240, 340, 440, 540."},
    {"q": "How do you teach skip counting by 5s?",
     "a": "Use things that come in fives: fingers on a hand, nickels and tally marks. Count each group by 5s (5, 10, 15, 20) and point out that the last digit always goes 5, 0, 5, 0."},
    {"q": "How do you skip count by 10s from a number that does not end in 0?",
     "a": "Keep the ones digit the same and add 1 to the tens digit each time: 37, 47, 57, 67. A hundred chart helps, because each number directly below is 10 more."},
    {"q": "Why does my child write 1100 after 199?",
     "a": "They add 1 to the 99 and write 100 after the 1. Show that 9 ones and 1 more make a ten, and 9 tens and 1 more ten make a hundred, so 199 + 1 = 200."},
]


def gen():
    rnd = random.Random(209)
    P = People(rnd)
    sets = [set_fives(rnd, P), set_tens(rnd, P), set_hundreds(rnd, P), set_across(rnd, P), set_stories(rnd, P)]
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
                    assert 0 <= v <= 1000 or v in BIG_OK, c
            k = re.sub(r"<[^>]+>", "", it["q"])
            assert k not in seen or "<svg" in it["q"], it["q"]
            seen.add(it["q"] + "|".join(sorted(it["c"])))
    u = {
        "country": "us", "subject": "math", "grade": "grade-2", "slug": "skip-counting", "sort": 9,
        "updated": UPDATED, "pdf_url": "",
        "title": "Skip Counting by 5s, 10s and 100s",
        "seo_title": "Grade 2 Skip Counting Worksheets: Count by 5s, 10s and 100s Within 1000",
        "short_title": "Skip counting",
        "domain": "Number and Operations in Base Ten",
        "standard_code": "2.NBT.A.2",
        "standard_url": "https://www.thecorestandards.org/Math/Content/2/NBT/A/2/",
        "standard_text": "Count within 1000; skip-count by 5s, 10s, and 100s.",
        "meta_desc": "Free Grade 2 skip counting worksheets: count by 5s with hands, nickels and tally marks, count by 10s and 100s from any number, count on and back across a hundred, and solve simple stories. 100 practice questions with simple answers explained.",
        "key_big": "Skip counting is jumping by the same number each time.",
        "key_sub": "Count by 10s and only the tens digit changes: 37, 47, 57. Count by 100s and only the hundreds digit changes: 240, 340, 440. After 199 comes 200.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }
    mark_large(u, "(\\d+ hands|open number line|number line counting|tally marks)")
    return u


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
