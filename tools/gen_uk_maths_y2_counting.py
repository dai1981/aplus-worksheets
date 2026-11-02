# -*- coding: utf-8 -*-
"""
UK Year 2 Maths: Counting in 2s, 3s, 5s and 10s (National Curriculum in England, Year 2: Number and place value)
  python tools/gen_uk_maths_y2_counting.py
Count in steps of 2, 3 and 5 from 0 (socks, hands, tricycles, cube towers, number tracks), count in tens
from any number forwards and backwards (hundred square, number lines), missing numbers and counting back,
and word problems with 2p, 5p and 10p coins.
Wrong answers come from real mistakes: counting on 1 at the end, adding 2 instead of 3, counting the groups
instead of the things (7 pairs -> 7 socks), one group too many or too few, changing the ones digit when
counting in tens (23 -> 34), going the wrong way when counting back, and slipping across a ten (30 - 2 = 29).
Every answer and every picture is computed and checked in code.
HTML attributes use single quotes (no backslashes in the JSON).
"""
import json, os, random, re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "uk", "maths", "year-2")
UPDATED = "2026-11-02"
GREEN = "#006633"
FILL = "#cfe6d6"
CUBE = "#8fc7a0"
RED = "#c0392b"
INK = "#2b2b2b"
FONT = "Arial, Helvetica, sans-serif"
GIRLS = ["Amelia", "Isla", "Freya", "Poppy", "Ava", "Aisha", "Lily", "Zara", "Grace", "Ruby", "Maya", "Evie"]
BOYS = ["Oliver", "Harry", "Mohammed", "Jack", "Arjun", "Noah", "George", "Leo", "Alfie", "Kai", "Ethan", "Charlie"]
COPPER = ("#d9915a", "#8a5428")
SILVER = ("#dfe3e7", "#7a828a")
COIN = {2: (22, COPPER, 15), 5: (17, SILVER, 14), 10: (21, SILVER, 14)}


# ------------------------------------------------------------ helpers
def mcq(q, correct, cands, e, unit=""):
    """4 choices: correct + the first 3 unique wrong numbers (above 0). Positions are set later by balance()."""
    fmt = (lambda v: "%d%s" % (v, unit)) if unit in ("", "p") else (lambda v: "%d %s" % (v, unit))
    if isinstance(correct, int):
        right = fmt(correct)
        pick, seen = [], {correct}
        for v in cands:
            if v is None or v <= 0 or v in seen:
                continue
            seen.add(v)
            pick.append(fmt(v))
            if len(pick) == 3:
                break
    else:
        right = correct
        pick = []
        for v in cands:
            if v != right and v not in pick:
                pick.append(v)
            if len(pick) == 3:
                break
    assert len(pick) == 3, (q, correct, cands)
    return {"q": q, "c": [right] + pick, "a": 0, "e": e}


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
        return dict(n=p[0], he=p[1], He=p[1].capitalize(), his=p[2])


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


def grid(n, per, w, h, gx, gy, m, draw):
    rows = rows_of(n, per)
    W = 2 * m + max(rows) * w + (max(rows) - 1) * gx
    H = 2 * m + len(rows) * h + (len(rows) - 1) * gy
    s = []
    for r, k in enumerate(rows):
        for i in range(k):
            s.append(draw(m + i * (w + gx), m + r * (h + gy)))
    return W, H, "".join(s)


# ------------------------------------------------------------ pictures
def sock(x, y):
    """One sock in a 22 x 40 box: a leg going down and a foot pointing right."""
    return ("<path d='M %.1f %.1f L %.1f %.1f L %.1f %.1f L %.1f %.1f Q %.1f %.1f %.1f %.1f L %.1f %.1f "
            "Q %.1f %.1f %.1f %.1f Z' fill='%s' stroke='%s' stroke-width='1.5' stroke-linejoin='round'/>"
            % (x, y, x + 12, y, x + 12, y + 24, x + 19, y + 28, x + 24, y + 33, x + 18, y + 40, x + 6, y + 40,
               x, y + 40, x, y + 32, FILL, GREEN)
            + "<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='3'/>"
            % (x + 1, y + 5, x + 11, y + 5, GREEN))


def pair(x, y):
    return ("<rect x='%.1f' y='%.1f' width='60' height='50' rx='8' fill='none' stroke='#9ab' stroke-width='1.2' "
            "stroke-dasharray='4 3'/>" % (x, y) + sock(x + 5, y + 5) + sock(x + 31, y + 5))


def socks_svg(n):
    W, H, body = grid(n, 5, 60, 50, 8, 8, 4, pair)
    return svg_wrap(W, H, body, "%d pairs of socks" % n)


def hand(x, y):
    """One hand, 4 fingers and a thumb, in a 40 x 58 box."""
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
    W, H, body = grid(n, 5, 40, 58, 10, 8, 6, hand)
    return svg_wrap(W, H, body, "%d hands" % n)


def trike(x, y):
    """A tricycle in a 70 x 50 box: 1 big front wheel and 2 small back wheels, all visible."""
    w = []
    w.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='3' stroke-linecap='round'/>"
             % (x + 14, y + 37, x + 18, y + 8, INK))                       # fork
    w.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='3' stroke-linecap='round'/>"
             % (x + 11, y + 7, x + 24, y + 7, INK))                         # handlebar
    w.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='3' stroke-linecap='round'/>"
             % (x + 17, y + 20, x + 46, y + 22, INK))                       # frame
    w.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='3' stroke-linecap='round'/>"
             % (x + 46, y + 18, x + 48, y + 39, INK))                       # seat post
    w.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='3' stroke-linecap='round'/>"
             % (x + 38, y + 40, x + 60, y + 37, INK))                       # back axle
    w.append("<rect x='%.1f' y='%.1f' width='16' height='5' rx='2.5' fill='%s'/>" % (x + 38, y + 14, GREEN))
    for cx, cy, r in [(x + 14, y + 37, 12), (x + 38, y + 40, 9), (x + 60, y + 37, 9)]:
        w.append("<circle cx='%.1f' cy='%.1f' r='%d' fill='%s' stroke='%s' stroke-width='2.5'/>" % (cx, cy, r, FILL, GREEN))
        w.append("<circle cx='%.1f' cy='%.1f' r='2.5' fill='%s'/>" % (cx, cy, GREEN))
    return "".join(w)


def trikes_svg(n):
    W, H, body = grid(n, 4, 70, 50, 12, 10, 4, trike)
    return svg_wrap(W, H, body, "%d tricycles" % n)


CS = 16


def tower(x, y, k=3):
    return "".join("<rect x='%.1f' y='%.1f' width='%d' height='%d' fill='%s' stroke='%s' stroke-width='1.5'/>"
                   % (x, y + j * CS, CS, CS, CUBE, GREEN) for j in range(k))


def towers_svg(n):
    W, H, body = grid(n, 8, CS, 3 * CS, 12, 12, 4, tower)
    return svg_wrap(W, H, body, "%d towers of 3 cubes" % n)


def coins_svg(n, v):
    r, (fill, edge), fs = COIN[v]
    d = 2 * r

    def coin(x, y):
        cx, cy = x + r, y + r
        return ("<circle cx='%.1f' cy='%.1f' r='%d' fill='%s' stroke='%s' stroke-width='2'/>" % (cx, cy, r, fill, edge)
                + "<circle cx='%.1f' cy='%.1f' r='%d' fill='none' stroke='%s' stroke-width='1'/>" % (cx, cy, r - 4, edge)
                + text(cx, cy + fs * 0.36, "%dp" % v, fs))
    W, H, body = grid(n, 5, d, d, 8, 8, 4, coin)
    return svg_wrap(W, H, body, "%d coins of %dp" % (n, v))


TW, TH = 46, 36


def track_svg(nums):
    """Number track: a row of boxes. None shows a red ? in a shaded box."""
    m = 4
    W, H = 2 * m + len(nums) * TW, 2 * m + TH
    s = []
    for i, v in enumerate(nums):
        x = m + i * TW
        s.append("<rect x='%d' y='%d' width='%d' height='%d' fill='%s' stroke='%s' stroke-width='1.5'/>"
                 % (x, m, TW, TH, FILL if v is None else "#ffffff", GREEN))
        s.append(text(x + TW / 2, m + 24, "?" if v is None else str(v), 17, col=RED if v is None else INK))
    return svg_wrap(W, H, "".join(s), "number track")


CW, CH = 46, 34


def square_svg(tl, nrows, ncols, target, hide=()):
    """A piece of the hundred square. tl = top-left number. target (r, c) shows a red ?, hide = blank cells."""
    assert (tl - 1) % 10 + ncols <= 10, "piece must stay inside one row of the hundred square"
    assert tl + 10 * (nrows - 1) + ncols - 1 <= 100
    m = 4
    W, H = 2 * m + ncols * CW, 2 * m + nrows * CH
    s = []
    for r in range(nrows):
        for c in range(ncols):
            x, y = m + c * CW, m + r * CH
            isT = (r, c) == target
            s.append("<rect x='%d' y='%d' width='%d' height='%d' fill='%s' stroke='%s' stroke-width='1.5'/>"
                     % (x, y, CW, CH, FILL if isT else "#ffffff", GREEN))
            if isT:
                s.append(text(x + CW / 2, y + 23, "?", 18, col=RED))
            elif (r, c) not in hide:
                s.append(text(x + CW / 2, y + 23, str(tl + 10 * r + c), 16))
    return svg_wrap(W, H, "".join(s), "hundred square piece")


def jw(j):
    return 74 if abs(j) >= 10 else 56


def nline_svg(start, jumps, ticks=None):
    """Open number line. Jumps go right for +, left for −. ticks: one label per point (None = no label)."""
    if ticks is None:
        ticks = [str(start)] + [None] * (len(jumps) - 1) + ["?"]
    jl = [("+%d" % j) if j > 0 else ("−%d" % -j) for j in jumps]
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
        s.append(text((x1 + x2) / 2, ly - ry - 6, jl[k], 15, col=GREEN))
    for x, t in zip(xs, ticks):
        s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='2'/>" % (x, ly - 6, x, ly + 6, INK))
        if t is not None:
            s.append(text(x, ly + 24, t, 16, col=RED if t == "?" else INK))
    return svg_wrap(W, H, "".join(s), "number line starting at %d with jumps of %s" % (
        start, ", ".join(jl).replace("−", "minus ")))


# ============================================================ set 1: count in 2s and 5s
def set_twos_fives():
    socks, hands, track, seq = [], [], [], []
    for n in [3, 4, 6, 8]:
        a = 2 * n
        socks.append(mcq(fig(socks_svg(n)) + "Count in 2s. How many socks are there?", a,
                         [n, a + 1, a - 2, a + 2],
                         "A pair is 2 socks. Count in 2s, one pair at a time: %s. There are <b>%d</b> socks." % (
                             lst(counts(2, 2, n)), a)))
    for n in [2, 3, 5, 7]:
        a = 5 * n
        hands.append(mcq(fig(hands_svg(n)) + "Count in 5s. How many fingers are there?", a,
                         [4 * n, n, a - 5, a + 5, a + 1],
                         "Each hand has 5 fingers (count the thumb too). Count in 5s: %s. There are <b>%d</b> fingers." % (
                             lst(counts(5, 5, n)), a)))
    for nums, step in [([0, 2, 4, 6], 2), ([10, 12, 14, 16], 2), ([5, 10, 15, 20], 5), ([40, 45, 50, 55], 5)]:
        last = nums[-1]
        a = last + step
        track.append(mcq(fig(track_svg(nums + [None])) + "Count in %ds. What number goes in the box with the ?" % step,
                         a, [last + 1, last + 2 * step, last + 3 if step == 2 else last + 2],
                         "Each number is %d more. %d + %d = <b>%d</b>." % (step, last, step, a)))
    for nums, step, cands in [([0, 2, 4, 6, 8], 2, [9, 12, 11]), ([14, 16, 18], 2, [19, 22, 21]),
                              ([22, 24, 26], 2, [27, 30, 29]),
                              ([0, 5, 10, 15], 5, [16, 25, 30]), ([30, 35, 40], 5, [41, 50, 42]),
                              ([85, 90, 95], 5, [96, 97, 90])]:
        last = nums[-1]
        a = last + step
        e = "Each number is %d more. %d + %d = <b>%d</b>." % (step, last, step, a)
        if cands[0] == last + 1:
            e += " %d is counting on 1, not %d." % (last + 1, step)
        seq.append(mcq("Count in %ds: %s, ☐. What comes next?" % (step, lst(nums)), a, cands, e))
    idea = [
        mcq("You count in 2s from 0. Which number do you say?", 14, [7, 9, 15],
            "Counting in 2s from 0: 0, 2, 4, 6, 8, 10, 12, <b>14</b>. These are even numbers. "
            "7, 9 and 15 are odd, so you do not say them."),
        mcq("You count in 5s from 0. What does every number end in?", "0 or 5", ["only 5", "only 0", "any digit"],
            "0, 5, 10, 15, 20, 25 … The last digit goes 0, 5, 0, 5. Every number ends in <b>0 or 5</b>."),
    ]
    its = [socks[0], seq[0], hands[0], track[0], socks[1], seq[3], hands[1], track[2], idea[0], seq[1],
           socks[2], hands[2], track[1], seq[4], idea[1], socks[3], hands[3], track[3], seq[2], seq[5]]
    assert len(its) == 20
    return {"title": "Count in 2s and 5s", "items": its}


# ============================================================ set 2: count in 3s
def set_threes():
    trikes, towers, track, line = [], [], [], []
    for n in [2, 4, 5, 7]:
        a = 3 * n
        trikes.append(mcq(fig(trikes_svg(n)) + "A tricycle has 3 wheels. How many wheels are there?", a,
                          [2 * n, n, a + 3, a - 3],
                          "Count in 3s, one tricycle at a time: %s. There are <b>%d</b> wheels." % (
                              lst(counts(3, 3, n)), a)))
    for n in [3, 6, 8, 10]:
        a = 3 * n
        towers.append(mcq(fig(towers_svg(n)) + "Each tower has 3 cubes. How many cubes are there?", a,
                          [n, a - 3, a + 3, 2 * n, a + 1],
                          "Count in 3s, one tower at a time: %s. There are <b>%d</b> cubes." % (
                              lst(counts(3, 3, n)), a)))
    for nums, i in [([0, 3, 6, 9], 3), ([9, 12, 15, 18], 3), ([18, 21, 24, 27], 3), ([3, 6, 9, 12], 2)]:
        a = nums[i]
        prev = nums[i - 1]
        shown = [None if k == i else v for k, v in enumerate(nums)]
        e = "Each number is 3 more. %d + 3 = <b>%d</b>." % (prev, a)
        if i < len(nums) - 1:
            e += " Check: %d + 3 = %d." % (a, nums[i + 1])
        track.append(mcq(fig(track_svg(shown)) + "Count in 3s. What number goes in the box with the ?", a,
                         [prev + 1, prev + 2, a + 3 if i == len(nums) - 1 else prev + 4], e))
    for n in [4, 6]:
        a = 3 * n
        line.append(mcq(fig(nline_svg(0, [3] * n)) + "Start at 0. Make the jumps. Where do you land?", a,
                        [n, a - 3, a + 3, 2 * n],
                        "Each jump is +3. Count in 3s: %s. You land on <b>%d</b>." % (lst(counts(3, 3, n)), a)))
    seq = []
    for nums, cands in [([0, 3, 6, 9, 12], [13, 14, 18]), ([15, 18, 21], [22, 23, 27]),
                        ([21, 24, 27], [28, 29, 33]), ([30, 33, 36], [37, 38, 42])]:
        last = nums[-1]
        a = last + 3
        seq.append(mcq("Count in 3s: %s, ☐. What comes next?" % lst(nums), a, cands,
                       "Each number is 3 more. %d + 3 = <b>%d</b>. %d is only 2 more." % (last, a, last + 2)))
    idea = [
        mcq("You count in 3s from 0. Which number do you say?", 18, [16, 20, 14],
            "Counting in 3s from 0: 0, 3, 6, 9, 12, 15, <b>18</b>. 16, 20 and 14 are in the 2s count, not the 3s count."),
        mcq("Which list counts in 3s?", "3, 6, 9, 12", ["3, 5, 7, 9", "3, 6, 8, 10", "3, 4, 5, 6"],
            "Each number must be 3 more: 3, 6, 9, 12. <b>3, 6, 9, 12</b> is right. "
            "3, 5, 7, 9 counts in 2s."),
    ]
    its = [trikes[0], seq[0], towers[0], track[0], line[0], trikes[1], idea[0], towers[1], seq[1], track[1],
           trikes[2], towers[2], track[3], seq[2], idea[1], line[1], trikes[3], track[2], towers[3], seq[3]]
    assert len(its) == 20
    return {"title": "Count in 3s", "items": its}


# ============================================================ set 3: count in 10s from any number
def set_tens():
    fwd, back, sq, line = [], [], [], []
    for a in [23, 14, 41, 36, 52]:
        s = counts(a, 10, 3)
        last = s[-1]
        fwd.append(mcq("Count in 10s: %s, ☐. What comes next?" % lst(s), last + 10,
                       [last + 1, last + 11, last + 20],
                       "Each number is 10 more. The tens digit goes up by 1. The ones digit stays %d. "
                       "%d + 10 = <b>%d</b>." % (a % 10, last, last + 10)))
    for a in [87, 95, 68, 74]:
        s = counts(a, -10, 3)
        last = s[-1]
        back.append(mcq("Count back in 10s: %s, ☐. What comes next?" % lst(s), last - 10,
                        [last - 1, last - 11, last - 20],
                        "Counting back, each number is 10 less. The tens digit goes down by 1. The ones digit stays %d. "
                        "%d − 10 = <b>%d</b>." % (a % 10, last, last - 10)))
    for tl, rows, cols, tgt, hide in [(12, 3, 4, (2, 1), {(1, 3)}), (35, 3, 4, (0, 2), {(2, 0)}),
                                      (54, 3, 3, (2, 2), {(0, 0)}), (61, 3, 4, (1, 3), {(2, 1), (0, 0)})]:
        a = tl + 10 * tgt[0] + tgt[1]
        if tgt[0] > 0:
            assert (tgt[0] - 1, tgt[1]) not in hide
            ref = a - 10
            e = ("In a hundred square, the number below is 10 more. The number above the ? is %d. "
                 "%d + 10 = <b>%d</b>." % (ref, ref, a))
            cands = [ref + 1, a + 1, a - 1, a + 10]
        else:
            assert (1, tgt[1]) not in hide
            ref = a + 10
            e = ("In a hundred square, the number above is 10 less. The number below the ? is %d. "
                 "%d − 10 = <b>%d</b>." % (ref, ref, a))
            cands = [ref - 1, a + 1, a - 1, ref]
        sq.append(mcq(fig(square_svg(tl, rows, cols, tgt, hide)) + "This is part of a hundred square. "
                      "What number goes in the box with the ?", a, cands, e))
    for start, n in [(16, 3), (47, 4)]:
        a = start + 10 * n
        line.append(mcq(fig(nline_svg(start, [10] * n)) + "Start at %d. Make the jumps. Where do you land?" % start,
                        a, [start + n, a - 10, a + 10, a + 1],
                        "Each jump is +10. Count in 10s from %d: %s. You land on <b>%d</b>." % (
                            start, lst(counts(start + 10, 10, n)), a)))
    for start, n in [(92, 3), (58, 2)]:
        a = start - 10 * n
        line.append(mcq(fig(nline_svg(start, [-10] * n)) + "Start at %d. Jump back. Where do you land?" % start,
                        a, [start - n, a + 10, a - 10, start + 10 * n],
                        "Each jump is back 10. Count back in 10s from %d: %s. You land on <b>%d</b>." % (
                            start, lst(counts(start - 10, -10, n)), a)))
    idea = mcq("Count in 10s: 23, 33, 43. Which digit changes?", "the tens digit",
               ["the ones digit", "both digits", "no digits"],
               "23, 33, 43: the 3 ones stay the same. The 2, 3, 4 go up by 1. That is <b>the tens digit</b>.")
    more = [mcq("What is 10 more than 68?", 78, [69, 79, 88],
                "10 more: the tens digit goes up by 1. 6 tens become 7 tens. The 8 ones stay. 68 + 10 = <b>78</b>."),
            mcq("What is 10 less than 40?", 30, [39, 41, 20],
                "10 less: the tens digit goes down by 1. 4 tens become 3 tens. 40 − 10 = <b>30</b>. "
                "39 is 1 less.")]
    its = [fwd[0], sq[0], back[0], line[0], idea, more[0], fwd[1], sq[1], back[1], line[2],
           fwd[2], more[1], sq[2], line[1], back[2], fwd[3], sq[3], line[3], back[3], fwd[4]]
    assert len(its) == 20
    return {"title": "Count in 10s from any number", "items": its}


# ============================================================ set 4: missing numbers and counting back
def set_missing():
    its = []
    for nums, step, i, cands in [([8, 10, 12, 14], 2, 2, [11, 13, 16]), ([45, 50, 55, 60], 5, 1, [46, 65, 40]),
                                 ([12, 15, 18, 21], 3, 2, [16, 17, 19]), ([34, 44, 54, 64], 10, 1, [35, 45, 74]),
                                 ([6, 9, 12, 15], 3, 0, [8, 7, 3])]:
        a = nums[i]
        shown = ["☐" if k == i else str(v) for k, v in enumerate(nums)]
        if i == 0:
            e = "Count back 3 from %d: %d − 3 = <b>%d</b>. Check: %d, %d, %d, %d go up in 3s." % (
                nums[1], nums[1], a, *nums)
        else:
            e = "Each number is %d more. %d + %d = <b>%d</b>. Check: %d + %d = %d." % (
                step, nums[i - 1], step, a, a, step, nums[i + 1])
        its.append(mcq("Count in %ds: %s. What number is missing?" % (step, ", ".join(shown)), a, cands, e))
    for nums, step, cands, extra in [
            ([20, 18, 16], 2, [15, 12, 13], " 15 is only 1 less."),
            ([50, 45, 40], 5, [39, 36, 30], " 39 is only 1 less."),
            ([30, 27, 24], 3, [23, 22, 18], " 22 is only 2 less."),
            ([61, 51, 41], 10, [40, 30, 21], " The ones digit stays 1, so it is not 40."),
            ([34, 32, 30], 2, [29, 38, 20], " Going back past 30, the tens go down to 2: 28, not 29 or 38."),
            ([75, 70, 65], 5, [64, 61, 55], " Take away 5, not 1 or 10."),
            ([18, 15, 12], 3, [11, 10, 6], " 10 is only 2 less.")]:
        last = nums[-1]
        a = last - step
        its.append(mcq("Count back in %ds: %s, ☐. What comes next?" % (step, lst(nums)), a, cands,
                       "Counting back, each number is %d less. %d − %d = <b>%d</b>.%s" % (step, last, step, a, extra)))
    its.append(mcq(fig(nline_svg(21, [-3] * 3)) + "Start at 21. Jump back. Where do you land?", 12, [15, 9, 18],
                   "Each jump is back 3. Count back in 3s: 18, 15, <b>12</b>. That is 3 jumps."))
    its.append(mcq(fig(track_svg([90, 80, None, 60])) + "Count back in 10s. What number goes in the box with the ?",
                   70, [79, 75, 50],
                   "Each number is 10 less. 80 − 10 = <b>70</b>. Check: 70 − 10 = 60."))
    rules = [
        mcq("What is the rule? 6, 9, 12, 15", "count in 3s", ["count in 2s", "count in 5s", "count in 1s"],
            "6 + 3 = 9, 9 + 3 = 12, 12 + 3 = 15. The rule is <b>count in 3s</b>."),
        mcq("What is the rule? 40, 35, 30, 25", "count back in 5s",
            ["count in 5s", "count back in 10s", "count back in 1s"],
            "The numbers get smaller by 5 each time. The rule is <b>count back in 5s</b>."),
    ]
    nots = [
        mcq("You count in 2s from 0. Which number do you NOT say?", 15, [16, 20, 12],
            "Counting in 2s from 0 gives even numbers: 0, 2, 4, 6 … 16, 20 and 12 are even. "
            "<b>15</b> is odd, so you do not say it."),
        mcq("You count in 5s from 0. Which number do you NOT say?", 32, [35, 40, 25],
            "Counting in 5s from 0, every number ends in 0 or 5. <b>32</b> ends in 2, so you do not say it."),
    ]
    from6 = mcq("Count in 10s from 6: 6, 16, 26 … Which number do you say?", 56, [50, 65, 57],
                "Counting in 10s from 6, the ones digit is always 6: 6, 16, 26, 36, 46, <b>56</b>.")
    rocket = mcq("Count back in 10s from 100: 100, 90, 80 … What comes after 30?", 20, [29, 40, 10],
                 "Each number is 10 less. 30 − 10 = <b>20</b>. 29 is counting back 1.")
    m, b = its[:5], its[5:12]
    nl, tr = its[12], its[13]
    out = [m[0], b[0], m[1], rules[0], b[1], nots[0], tr, m[2], b[2], rocket,
           m[3], b[3], nots[1], from6, nl, b[5], m[4], rules[1], b[6], b[4]]
    assert len({id(x) for x in out}) == 20
    return {"title": "Missing numbers and counting back", "items": out}


# ============================================================ set 5: word problems
def set_stories(P):
    its = []

    def story(t, ans, unit, wrong, e, pic=""):
        d = P.next()
        its.append(mcq(pic + t.format(**d), ans, wrong, e.format(**d), unit))

    story("{n} has 7 pairs of socks. How many socks is that?", 14, "socks", [7, 15, 12, 16],
          "A pair is 2 socks. Count in 2s 7 times: 2, 4, 6, 8, 10, 12, 14. That is <b>14</b> socks.")       # 0
    story("The PE cupboard has 10 pairs of football boots. How many boots is that?", 20, "boots", [10, 12, 21],
          "Count in 2s 10 times: 2, 4, 6, 8, 10, 12, 14, 16, 18, 20. That is <b>20</b> boots.")             # 1
    story("{n} has these 10p coins. How much money is that?", 60, "p", [6, 16, 50, 70],
          "Count in 10s: 10, 20, 30, 40, 50, 60. That is <b>60p</b>.", fig(coins_svg(6, 10)))              # 2
    story("{n} has these 5p coins. How much money is that?", 40, "p", [8, 13, 35, 45],
          "Count in 5s: 5, 10, 15, 20, 25, 30, 35, 40. That is <b>40p</b>.", fig(coins_svg(8, 5)))           # 3
    story("{n} has these 2p coins. How much money is that?", 18, "p", [9, 11, 16, 20],
          "Count in 2s: 2, 4, 6, 8, 10, 12, 14, 16, 18. That is <b>18p</b>.", fig(coins_svg(9, 2)))           # 4
    story("There are 4 tricycles in the playground. Each one has 3 wheels. How many wheels are there?", 12,
          "wheels", [8, 7, 15],
          "Count in 3s 4 times: 3, 6, 9, 12. There are <b>12</b> wheels. 8 is counting in 2s.")              # 5
    story("{n} jumps in 5s from 0. Where does {he} land?", 30, "", [6, 25, 35],
          "Count the jumps in 5s: 5, 10, 15, 20, 25, 30. {He} lands on <b>30</b>.",
          fig(nline_svg(0, [5] * 6)))                                                                       # 6
    story("A frog is on 95. It jumps back 10 each time. Where is it after 3 jumps?", 65, "", [92, 75, 55],
          "Count back in 10s 3 times: 85, 75, 65. It is on <b>65</b>.")                                      # 7
    story("9 children each have 2 gloves. How many gloves are there?", 18, "gloves", [9, 11, 20],
          "Count in 2s 9 times: 2, 4, 6, 8, 10, 12, 14, 16, 18. There are <b>18</b> gloves.")               # 8
    story("{n} puts 3 biscuits on each plate. There are 6 plates. How many biscuits are there?", 18,
          "biscuits", [12, 9, 21],
          "Count in 3s 6 times: 3, 6, 9, 12, 15, 18. There are <b>18</b> biscuits.")                         # 9
    story("6 children each hold up one hand. How many fingers are there?", 30, "fingers", [24, 6, 35],
          "Each hand has 5 fingers. Count in 5s 6 times: 5, 10, 15, 20, 25, 30. There are <b>30</b> fingers.")  # 10
    story("{n} has 23 stickers. {He} gets 10 more each week. How many does {he} have after 3 weeks?", 53,
          "stickers", [26, 43, 63, 54],
          "Start at 23. Count on in 10s 3 times: 33, 43, 53. {He} has <b>53</b> stickers.")                 # 11
    story("{n} has 80p. {He} spends 10p each day. How much is left after 3 days?", 50, "p", [77, 60, 40],
          "Start at 80p. Count back in 10s 3 times: 70p, 60p, 50p. <b>50p</b> is left.")                   # 12
    story("{n} counts {his} 10p coins: 10, 20, 30, 40, 50. How many coins does {he} have?", 5, "coins",
          [50, 4, 6],
          "{He} says one number for each coin. There are 5 numbers, so there are <b>5</b> coins. "
          "50p is how much they are worth.")                                                               # 13
    story("{n} counts socks in 2s: 2, 4, 6 … 16. How many pairs are there?", 8, "pairs", [16, 7, 9],
          "Each number is one more pair: 2, 4, 6, 8, 10, 12, 14, 16. That is 8 numbers, so <b>8</b> pairs.")  # 14
    story("Pencils come in packs of 10. The class has 7 packs. How many pencils are there?", 70, "pencils",
          [17, 60, 80],
          "Count in 10s 7 times: 10, 20, 30, 40, 50, 60, 70. There are <b>70</b> pencils.")                 # 15
    story("{n} puts 5 strawberries in each bowl. There are 7 bowls. How many strawberries are there?", 35,
          "strawberries", [12, 30, 40],
          "Count in 5s 7 times: 5, 10, 15, 20, 25, 30, 35. There are <b>35</b> strawberries.")               # 16
    story("{n} counts back in 2s: 20, 18, 16 … What does {he} say after 10?", 8, "", [9, 12, 6],
          "Each number is 2 less. 10 − 2 = <b>8</b>. 9 is only 1 less.")                                   # 17
    story("Each pot has 3 sunflowers. There are 5 pots. How many sunflowers are there?", 15, "sunflowers",
          [10, 8, 18],
          "Count in 3s 5 times: 3, 6, 9, 12, 15. There are <b>15</b> sunflowers. 8 is 5 + 3.")               # 17
    story("{n} is on 12 on a number track. {He} counts back in 3s two times. Where does {he} stop?", 6, "",
          [10, 9, 3],
          "Count back in 3s two times: 9, <b>6</b>. Do not count 12, because that is where {he} starts.")   # 19
    k = its
    out = [k[0], k[2], k[8], k[1], k[4], k[10], k[5], k[3], k[15], k[6],
           k[9], k[13], k[18], k[17], k[11], k[16], k[7], k[14], k[12], k[19]]
    assert len({id(x) for x in out}) == 20
    return {"title": "Word problems", "items": out}


# ============================================================ lesson
def body_html():
    return (
        "<h2>Counting in steps</h2>"
        "<p>When you count in steps, you do not say every number. You jump by the same amount each time. "
        "In Year 2 you count in <b>2s</b>, <b>3s</b> and <b>5s</b> from 0, and in <b>10s</b> from any number. "
        "You count forwards and backwards.</p>"
        + table(["Count in", "Numbers", "Look for"], [
            ["2s", "0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20", "Even numbers"],
            ["3s", "0, 3, 6, 9, 12, 15, 18, 21, 24, 27, 30", "3 more each time"],
            ["5s", "0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50", "Ends in 0 or 5"],
            ["10s", "0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100", "Ends in 0"],
        ]) +
        "<h2>Count in groups</h2>"
        "<p>Count things that come in groups. Say one number for each group.</p>"
        "<figure class='sn-fig'>" + socks_svg(4) +
        "<figcaption>4 pairs of socks: 2, 4, 6, 8. There are 8 socks.</figcaption></figure>"
        "<figure class='sn-fig'>" + trikes_svg(3) +
        "<figcaption>3 tricycles: 3, 6, 9. There are 9 wheels.</figcaption></figure>"
        "<figure class='sn-fig'>" + hands_svg(4) +
        "<figcaption>4 hands: 5, 10, 15, 20. There are 20 fingers.</figcaption></figure>"
        "<h2>Count in 10s from any number</h2>"
        "<p>You can start at any number. The <b>tens digit</b> changes. The <b>ones digit</b> stays the same.</p>"
        "<figure class='sn-fig'>" + nline_svg(23, [10, 10, 10], ticks=["23", "33", "43", "53"]) +
        "<figcaption>Start at 23 and jump +10 three times: 33, 43, 53.</figcaption></figure>"
        "<p>On a hundred square, the number below is 10 more. The number above is 10 less.</p>"
        "<figure class='sn-fig'>" + square_svg(34, 3, 4, (2, 1)) +
        "<figcaption>Below 45 is 55. The ? is 55.</figcaption></figure>"
        + ex("Count back in 10s", "87, 77, 67, ☐",
             "Each number is 10 less. The tens go 8, 7, 6, 5. The 7 ones stay.", "57") +
        ex("Missing number", "Count in 3s: 12, 15, ☐, 21",
           "15 + 3 = 18. Check: 18 + 3 = 21.", "18") +
        "<h2>Common mistakes</h2>"
        + table(["Mistake", "What to do instead"], [
            ["Counting on 1 at the end: 0, 3, 6, 7", "Add 3 every time: 0, 3, 6, 9"],
            ["Adding 2 instead of 3: 9, 12, 14", "Count in 3s: 9, 12, 15"],
            ["Changing the ones digit in 10s: 23, 24, 34", "Keep the ones digit: 23, 33, 43"],
            ["Counting back across a ten: 34, 32, 30, 29", "30 − 2 = 28"],
            ["Counting the pairs, not the socks: 7 pairs = 7 socks", "Count in 2s: 7 pairs = 14 socks"],
        ])
    )


FAQ = [
    {"q": "What should a Year 2 child be able to count in?",
     "a": "In Year 2 children count in steps of 2, 3 and 5 from 0, and in tens from any number, forwards and backwards. For example 0, 3, 6, 9 and 47, 37, 27."},
    {"q": "How do you help a child count in 3s?",
     "a": "Use things that come in threes, such as tricycle wheels or towers of 3 cubes, and count one group at a time: 3, 6, 9, 12. Jumps of 3 on a number line help too."},
    {"q": "How do you count in tens from a number like 23?",
     "a": "Keep the ones digit the same and add 1 to the tens digit each time: 23, 33, 43, 53. On a hundred square, just move down one row."},
    {"q": "Why does counting in 2s, 5s and 10s matter in Year 2?",
     "a": "These counts are the start of the 2, 5 and 10 times tables, which Year 2 children learn. Counting in 5s and 10s also helps with telling the time and counting 5p and 10p coins."},
]


def gen():
    rnd = random.Random(2202)
    P = People(rnd)
    sets = [set_twos_fives(), set_threes(), set_tens(), set_missing(), set_stories(P)]
    balance(sets, rnd)
    seen = set()
    for s in sets:
        assert len(s["items"]) == 20, (s["title"], len(s["items"]))
        assert sorted(it["a"] for it in s["items"]) == sorted([0, 1, 2, 3] * 5)
        for it in s["items"]:
            assert len(set(it["c"])) == 4, it
            assert it["q"].count("<svg") <= 1
            for c in it["c"]:
                for tok in re.findall(r"\d+", c):
                    assert 0 <= int(tok) <= 100, c
            k = it["q"] + "|".join(sorted(it["c"]))
            assert k not in seen, it["q"]
            seen.add(k)
    u = {
        "country": "uk", "subject": "maths", "grade": "year-2", "slug": "counting-in-2s-3s-5s-and-10s", "sort": 2,
        "updated": UPDATED, "pdf_url": "",
        "title": "Counting in 2s, 3s, 5s and 10s: Forwards and Backwards",
        "seo_title": "Year 2 Counting in 2s, 3s, 5s and 10s Worksheets: Count Forwards and Backwards",
        "short_title": "Counting in 2s, 3s, 5s and 10s",
        "domain": "Number and place value",
        "standard_code": "Year 2: Number and place value",
        "standard_url": "https://www.gov.uk/government/publications/national-curriculum-in-england-mathematics-programmes-of-study",
        "standard_text": "Count in steps of 2, 3, and 5 from 0, and in tens from any number, forward and backward.",
        "meta_desc": "Free Year 2 maths worksheets for counting in 2s, 3s, 5s and 10s: count socks, fingers, tricycle wheels and coins, count in tens from any number on a hundred square, find missing numbers and count backwards. 100 questions with an answer key, following the National Curriculum.",
        "key_big": "Counting in steps means adding the same number each time.",
        "key_sub": "Count in 2s, 3s and 5s from 0: 0, 3, 6, 9. Count in 10s from any number and only the tens digit changes: 23, 33, 43. Counting back, take the same step away: 50, 45, 40.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }
    return mark_large(u, "(\\d+ hands|\\d+ pairs|\\d+ tricycles|\\d+ towers|\\d+ coins|number track|number line|hundred square)")


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
