# -*- coding: utf-8 -*-
"""
US Grade 1 Math: 10 More and 10 Less (1.NBT.C.5)
  python tools/gen_us_math_g1_ten_more_less.py
Add one ten and take away one ten with base-ten blocks, find 10 more / 10 less on a
hundred chart (and 1 more / 1 less to compare), mixed practice and patterns, short stories.
Every answer and every picture is computed and checked in code.
HTML attributes use single quotes (no backslashes in the JSON).
Grade 1: numbers up to 120, no commas. Very short sentences for 6-7 year olds.
"""
import json, os, random, re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "us", "math", "grade-1")
UPDATED = "2026-11-02"
GREEN = "#006633"
FILL = "#cfe6d6"
CUBE = "#8fc7a0"
NEWF = "#f6c35b"
NEWS = "#9a5b00"
RED = "#c0392b"
INK = "#2b2b2b"
FONT = "Arial, Helvetica, sans-serif"
MINUS = "−"
GIRLS = ["Maya", "Ava", "Mia", "Zoe", "Lily", "Emma", "Nora", "Ruby", "Sofia", "Grace"]
BOYS = ["Leo", "Noah", "Eli", "Sam", "Ben", "Omar", "Kai", "Jack", "Luis", "Owen"]


# ------------------------------------------------------------ helpers
def mcq(q, correct, cands, e):
    """4 choices: correct + the first 3 unique distractors. Positions are set later by balance()."""
    correct = str(correct)
    seen = {correct}
    pick = []
    for c in cands:
        if c is None:
            continue
        c = str(c)
        lead = c.split(" ")[0]
        if c in seen or not c or lead.startswith("-") or lead == "0":
            continue
        seen.add(c)
        pick.append(c)
        if len(pick) == 3:
            break
    assert len(pick) == 3, (q, correct, cands)
    return {"q": q, "c": [correct] + pick, "a": 0, "e": e}


def mcq_n(q, correct, cands, e):
    """Number choices. Wrong numbers that are 0 or less, or above 120, are dropped."""
    return mcq(q, correct, [v for v in cands if v is not None and 0 < v <= 120 and v != correct], e)


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

    def named(self, name):
        return (name, "she", "her") if name in GIRLS else (name, "he", "his")


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
    """Tag pictures that must print larger so the small cubes stay easy to count."""
    rx = re.compile(r"<svg (?=[^>]*aria-label='" + pattern + ")")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u


def unit(k, one, many):
    return "%d %s" % (k, one if k == 1 else many)


def T(k):
    return unit(k, "ten", "tens")


def O(k):
    return unit(k, "one", "ones")


def to(t, o):
    return "%s, %s" % (T(t), O(o))


def rev(n):
    """Digits turned around: 56 -> 65 (only for 2-digit numbers with two different digits)."""
    t, o = divmod(n, 10)
    return o * 10 + t if 10 <= n <= 99 and o and o != t else None


# typical wrong answers
def more_c(n):
    """10 more than n: changed the ones (n+1), went the wrong way (n-10), changed both (n+11),
    counted on by ones from n itself (n+9), turned the digits around."""
    return [n + 1, n - 10, n + 11, n + 9, rev(n + 10), n + 20]


def less_c(n):
    return [n - 1, n + 10, n - 11, n - 9, rev(n - 10), n - 20]


def one_more_c(n):
    return [n + 10, n - 1, n + 11, n + 2]


def one_less_c(n):
    return [n - 10, n + 1, n - 11, n - 2]


def e_more(n):
    t, o = divmod(n, 10)
    return ("%d is %s. 10 more is 1 more ten: %s. That is %d. The ones digit stays %d."
            % (n, to(t, o), to(t + 1, o), n + 10, o))


def e_less(n):
    t, o = divmod(n, 10)
    return ("%d is %s. 10 less is 1 ten fewer: %s. That is %d. The ones digit stays %d."
            % (n, to(t, o), to(t - 1, o), n - 10, o))


# ------------------------------------------------------------ figures
U = 8                          # small cube U x U, a ten rod U x 10U (exact 1 : 10)
RG, CG, GG, M = 6, 6, 18, 6    # gaps between rods, cubes, groups; margin
TOP = 22                       # room for the +10 / −10 label


def rod(x, y, fill, stroke, dash=False):
    s = ["<rect x='%d' y='%d' width='%d' height='%d' fill='%s' stroke='%s' stroke-width='1.5'%s/>"
         % (x, y, U, 10 * U, fill, stroke, " stroke-dasharray='3 2'" if dash else "")]
    for i in range(1, 10):
        s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='0.7'/>"
                 % (x, y + i * U, x + U, y + i * U, stroke))
    return "".join(s)


def blocks_svg(t, o, extra=None):
    """t ten rods and o ones cubes. extra='add': one more new rod (+10), 'take': the last rod crossed out (−10)."""
    F = 10 * U
    top = TOP if extra else 0
    nrods = t + (1 if extra == "add" else 0)
    s = []
    x = M + (10 if extra else 0)     # room for the label centred over the first rod
    y = M + top
    lastc = 0
    for k in range(nrods):
        if extra == "add" and k == nrods - 1:
            x += 4
            s.append(rod(x, y, NEWF, NEWS))
            s.append(text(x + U / 2, M + 15, "+10", 15, col=NEWS))
            lastc = x + U / 2
        elif extra == "take" and k == nrods - 1:
            s.append(rod(x, y, "#ffffff", GREEN, dash=True))
            s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='2.5'/>"
                     % (x - 3, y - 3, x + U + 3, y + F + 3, RED))
            s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='2.5'/>"
                     % (x + U + 3, y - 3, x - 3, y + F + 3, RED))
            s.append(text(x + U / 2, M + 15, MINUS + "10", 15, col=RED))
            lastc = x + U / 2
        else:
            s.append(rod(x, y, FILL, GREEN))
        x += U + RG
    x -= RG
    if o:
        x += GG
        for k in range(o):
            cx = x + (k // 5) * (U + CG)
            cy = y + (k % 5) * (U + 8)
            s.append("<rect x='%d' y='%d' width='%d' height='%d' fill='%s' stroke='%s' stroke-width='1.5'/>"
                     % (cx, cy, U, U, CUBE, GREEN))
        x += ((o + 4) // 5) * (U + CG) - CG
    W = x + M + (6 if extra == "take" else 0)
    if extra:
        W = max(W, int(lastc + 20))
    H = 2 * M + top + F + (3 if extra == "take" else 0)
    lab = "base-ten blocks %s" % to(t, o)
    if extra:
        lab += ", %s" % ("one ten added" if extra == "add" else "one ten taken away")
    return svg_wrap(W, H, "".join(s), lab)


CWID, CHT = 48, 34


def chart_svg(n, target=None, show=None, hl=()):
    """A 3 x 3 piece of the hundred chart (1-100) with n in the middle.
    target = (dr, dc) shows a red ?; show = cells (dr, dc) whose numbers are written (None = all); hl = filled cells."""
    assert 12 <= n <= 89 and 2 <= n % 10 <= 9, n   # the whole piece stays inside the chart and in its rows
    m = 4
    W, H = 2 * m + 3 * CWID, 2 * m + 3 * CHT
    s = []
    for dr in (-1, 0, 1):
        for dc in (-1, 0, 1):
            x, y = m + (dc + 1) * CWID, m + (dr + 1) * CHT
            v = n + 10 * dr + dc
            isT = (dr, dc) == target
            fill = FILL if isT or (dr, dc) in hl else "#ffffff"
            s.append("<rect x='%d' y='%d' width='%d' height='%d' fill='%s' stroke='%s' stroke-width='1.5'/>"
                     % (x, y, CWID, CHT, fill, GREEN))
            if isT:
                s.append(text(x + CWID / 2, y + 23, "?", 18, col=RED))
            elif show is None or (dr, dc) in show:
                s.append(text(x + CWID / 2, y + 23, str(v), 16, col=INK))
    # thick border around the middle number
    s.append("<rect x='%d' y='%d' width='%d' height='%d' fill='none' stroke='%s' stroke-width='3'/>"
             % (m + CWID, m + CHT, CWID, CHT, GREEN))
    return svg_wrap(W, H, "".join(s), "hundred chart piece")


def jw(j):
    return 74


def nline_svg(start, jumps, ticks=None):
    """Open number line. Jumps go right for +, left for −."""
    if ticks is None:
        ticks = [str(start)] + [None] * (len(jumps) - 1) + ["?"]
    jlabels = [("+%d" % j) if j > 0 else (MINUS + "%d" % -j) for j in jumps]
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
        start, ", ".join(jlabels).replace(MINUS, "minus ")))


# ------------------------------------------------------------ number picking
def pick(rnd, used, lo, hi, ok=lambda n: True):
    while True:
        n = rnd.randint(lo, hi)
        if n not in used and ok(n):
            used.add(n)
            return n


def mix_order(groups, pattern):
    """Interleave groups: pattern is a list of group indexes."""
    its = [list(g) for g in groups]
    out = [its[k].pop(0) for k in pattern]
    assert all(not g for g in its), [len(g) for g in its]
    return out


# ============================================================ set 1: 10 more with blocks
def set_more_blocks(rnd):
    used = set()
    a, b, c = [], [], []
    # one new ten is added (10): includes a teen and a number with 0 ones
    specials = [16, 40]
    for k in range(10):
        n = specials[k // 5] if k in (2, 7) else pick(rnd, used, 21, 79, lambda v: v % 10 != 0)
        used.add(n)
        t, o = divmod(n, 10)
        e = "%d is %s. Add 1 ten. Now you have %s. That is %d." % (n, to(t, o), to(t + 1, o), n + 10)
        if o == 0:
            e += " There are still 0 ones."
        a.append(mcq_n(fig(blocks_svg(t, o, "add")) +
                       "The blocks show %d. 1 more ten is added. What number is it now?" % n,
                       n + 10, more_c(n), e))
    # count the blocks, then find 10 more (6)
    for k in range(6):
        n = pick(rnd, used, 12, 68, lambda v: v % 10 != 0 and v // 10 != v % 10)
        t, o = divmod(n, 10)
        e = ("Count: %s is %d. 10 more is 1 more ten: %s. That is %d. The ones digit stays %d."
             % (to(t, o), n, to(t + 1, o), n + 10, o))
        b.append(mcq_n(fig(blocks_svg(t, o)) + "What number is 10 more than the blocks show?",
                       n + 10, more_c(n) + [n], e))
    # which shows 10 more, in tens and ones (4)
    for k in range(4):
        n = pick(rnd, used, 23, 77, lambda v: 2 <= v % 10 <= 8 and v // 10 != v % 10)
        t, o = divmod(n, 10)
        wrong = [to(t, o + 1), to(t - 1, o), to(t + 2, o), to(o, t + 1)]
        c.append(mcq(fig(blocks_svg(t, o)) + "The blocks show %d. Which is 10 more?" % n, to(t + 1, o), wrong,
                     "Add 1 rod. %d has %s. 10 more has %s. That is %d." % (n, to(t, o), to(t + 1, o), n + 10)))
    order = mix_order([a, b, c], [0, 0, 0, 0, 1, 0, 0, 1, 0, 2, 1, 0, 1, 0, 2, 1, 0, 2, 1, 2])
    return {"title": "10 more with base-ten blocks", "items": order}


# ============================================================ set 2: 10 less with blocks
def set_less_blocks(rnd):
    used = set()
    a, b, c = [], [], []
    specials = {2: 19, 7: 60}
    for k in range(10):
        n = specials.get(k) or pick(rnd, used, 31, 89, lambda v: v % 10 != 0)
        used.add(n)
        t, o = divmod(n, 10)
        e = "%d is %s. Take away 1 ten. Now you have %s. That is %d." % (n, to(t, o), to(t - 1, o), n - 10)
        if t == 1:
            e = "%d is %s. Take away 1 ten. Now you have only %s. That is %d." % (n, to(t, o), O(o), n - 10)
        a.append(mcq_n(fig(blocks_svg(t, o, "take")) +
                       "The blocks show %d. 1 ten is taken away. What number is left?" % n,
                       n - 10, less_c(n), e))
    for k in range(6):
        n = pick(rnd, used, 22, 79, lambda v: v % 10 != 0 and v // 10 != v % 10)
        t, o = divmod(n, 10)
        e = ("Count: %s is %d. 10 less is 1 ten fewer: %s. That is %d. The ones digit stays %d."
             % (to(t, o), n, to(t - 1, o), n - 10, o))
        b.append(mcq_n(fig(blocks_svg(t, o)) + "What number is 10 less than the blocks show?",
                       n - 10, less_c(n) + [n], e))
    for k in range(4):
        n = pick(rnd, used, 32, 88, lambda v: 2 <= v % 10 <= 8 and v // 10 != v % 10)
        t, o = divmod(n, 10)
        wrong = [to(t, o - 1), to(t + 1, o), to(t - 2, o), to(o, t - 1)]
        c.append(mcq(fig(blocks_svg(t, o)) + "The blocks show %d. Which is 10 less?" % n, to(t - 1, o), wrong,
                     "Take away 1 rod. %d has %s. 10 less has %s. That is %d." % (n, to(t, o), to(t - 1, o), n - 10)))
    order = mix_order([a, b, c], [0, 0, 0, 0, 1, 0, 0, 1, 0, 2, 1, 0, 1, 0, 2, 1, 0, 2, 1, 2])
    return {"title": "10 less with base-ten blocks", "items": order}


# ============================================================ set 3: hundred chart
def set_chart(rnd):
    used = set()
    its = []
    kinds = [(1, 0), (-1, 0), (1, 0), (0, 1), (-1, 0), (0, -1), (1, 0), (-1, 0),
             (0, 1), (1, 0), (0, -1), (-1, 0), (0, 1), (0, -1)]
    for dr, dc in kinds:
        n = pick(rnd, used, 12, 89, lambda v: 2 <= v % 10 <= 9)
        ans = n + 10 * dr + dc
        if dr:      # show the middle row, so the ? row gives nothing away
            show = {(0, -1), (0, 0), (0, 1)}
        else:       # show the middle column
            show = {(-1, 0), (0, 0), (1, 0)}
        cands = {(1, 0): more_c, (-1, 0): less_c, (0, 1): one_more_c, (0, -1): one_less_c}[(dr, dc)](n)
        if dr == 1:
            e = "The ? is just below %d. One row down is 10 more. %d + 10 = %d." % (n, n, ans)
        elif dr == -1:
            e = "The ? is just above %d. One row up is 10 less. %d %s 10 = %d." % (n, n, MINUS, ans)
        elif dc == 1:
            e = "The ? is just to the right of %d. One box right is 1 more. %d + 1 = %d." % (n, n, ans)
        else:
            e = "The ? is just to the left of %d. One box left is 1 less. %d %s 1 = %d." % (n, n, MINUS, ans)
        its.append(mcq_n(fig(chart_svg(n, (dr, dc), show)) + "This is part of a hundred chart. What number is the ?",
                         ans, cands, e))
    # how to move (2)
    moves = ["Move down 1 row", "Move up 1 row", "Move right 1 box", "Move left 1 box"]
    its.append(mcq("On a hundred chart, how do you find 10 more?", moves[0], moves[1:],
                   "Each row has 10 numbers. The number just below is 10 more. 33 is just below 23."))
    its.append(mcq("On a hundred chart, how do you find 10 less?", moves[1], [moves[0], moves[3], moves[2]],
                   "The number just above is 10 less. 33 is below 23, so 10 less than 33 is 23."))
    # words only (4)
    n = pick(rnd, used, 12, 89, lambda v: 2 <= v % 10 <= 9)
    its.append(mcq_n("On a hundred chart, you start at %d. You move down 1 row. Where are you now?" % n,
                     n + 10, more_c(n), "Down 1 row is 10 more. " + e_more(n)))
    n = pick(rnd, used, 12, 89, lambda v: 2 <= v % 10 <= 9)
    its.append(mcq_n("On a hundred chart, you start at %d. You move up 1 row. Where are you now?" % n,
                     n - 10, less_c(n), "Up 1 row is 10 less. " + e_less(n)))
    its.append(mcq_n("On a hundred chart, which number is just below 40?", 50, [41, 30, 51, 49],
                     "40 is at the end of its row. The number just below it is 10 more: 50."))
    its.append(mcq_n("On a hundred chart, which number is just above 70?", 60, [69, 80, 71, 59],
                     "The number just above is 10 less. 7 tens take away 1 ten is 6 tens: 60."))
    order = [its[k] for k in [0, 1, 14, 2, 3, 4, 15, 5, 6, 16, 7, 8, 9, 17, 10, 11, 18, 12, 13, 19]]
    assert len({id(x) for x in order}) == 20
    return {"title": "Use a hundred chart", "items": order}


# ============================================================ set 4: mixed practice and patterns
def set_mixed(rnd):
    used = set()
    its = []
    plan = [("10 more", 10), ("1 more", 1), ("10 less", -10), ("1 less", -1),
            ("10 more", 10), ("10 less", -10), ("1 more", 1), ("1 less", -1)]
    for word, d in plan:
        n = pick(rnd, used, 21, 88, lambda v: 1 <= v % 10 <= 8 and v // 10 != v % 10)
        ans = n + d
        c = {10: more_c, -10: less_c, 1: one_more_c, -1: one_less_c}[d](n)
        if d == 10:
            e = e_more(n)
        elif d == -10:
            e = e_less(n)
        elif d == 1:
            e = "1 more changes the ones digit. %d + 1 = %d. The tens digit stays %d." % (n, ans, n // 10)
        else:
            e = "1 less changes the ones digit. %d %s 1 = %d. The tens digit stays %d." % (n, MINUS, ans, n // 10)
        its.append(mcq_n("What is %s than %d?" % (word, n), ans, c, e))
    # equations (2)
    n = pick(rnd, used, 21, 88, lambda v: v % 10 and v // 10 != v % 10)
    its.append(mcq_n("%d + 10 = ☐" % n, n + 10, more_c(n), "Add 1 ten. The tens digit goes up by 1. %d + 10 = %d." % (n, n + 10)))
    n = pick(rnd, used, 21, 98, lambda v: v % 10 and v // 10 != v % 10)
    its.append(mcq_n("%d %s 10 = ☐" % (n, MINUS), n - 10, less_c(n),
                     "Take away 1 ten. The tens digit goes down by 1. %d %s 10 = %d." % (n, MINUS, n - 10)))
    # patterns (4)
    pats = [([14, 24, 34], None), ([78, 68, 58], None), ([25, 35, None, 55], 45), ([93, 83, None, 63], 73)]
    for seq, mid in pats:
        if mid is None:
            step = seq[1] - seq[0]
            ans = seq[-1] + step
            last = seq[-1]
            c = [last + (1 if step > 0 else -1), last + step + (1 if step > 0 else -1), last - step, rev(ans)]
            shown = ", ".join(str(v) for v in seq) + ", ☐"
        else:
            step = seq[1] - seq[0]
            ans = mid
            prev = seq[1]
            sg = 1 if step > 0 else -1
            c = [prev + sg, ans + sg, rev(ans), ans - sg]
            shown = ", ".join("☐" if v is None else str(v) for v in seq)
        word = "up" if step > 0 else "down"
        e = "Each number is 10 %s than the one before. The tens digit goes %s by 1. The ones digit stays %d. ☐ = %d." % (
            "more" if step > 0 else "less", word, ans % 10, ans)
        its.append(mcq_n("What number goes in the box? " + shown, ans, c, e))
    # number lines (2)
    its.append(mcq_n(fig(nline_svg(23, [10, 10])) + "Start at 23. Jump +10, then +10 again. Where do you land?",
                     43, [33, 25, 42, 53], "23 + 10 = 33. 33 + 10 = 43. Two jumps of 10 add 2 tens."))
    its.append(mcq_n(fig(nline_svg(86, [-10, -10])) + "Start at 86. Jump %s10, then %s10 again. Where do you land?" % (MINUS, MINUS),
                     66, [76, 84, 67, 56], "86 %s 10 = 76. 76 %s 10 = 66. Two jumps back take away 2 tens." % (MINUS, MINUS)))
    # which digit changes / pairs (2)
    its.append(mcq("When you add 10 to 52, which digit changes?", "the tens digit",
                   ["the ones digit", "both digits", "no digit"],
                   "52 + 10 = 62. The 5 tens become 6 tens. The ones digit stays 2."))
    its.append(mcq("Which pair shows a number and 10 more?", "36 and 46", ["36 and 37", "36 and 26", "36 and 63"],
                   "10 more than 36 is 46. Only the tens digit goes up by 1."))
    # missing start (2)
    its.append(mcq_n("10 more than ☐ is 65. What number goes in the box?", 55, [75, 64, 66, 56],
                     "Go back 1 ten from 65. 65 %s 10 = 55. Check: 10 more than 55 is 65." % MINUS))
    its.append(mcq_n("10 less than ☐ is 30. What number goes in the box?", 40, [20, 31, 29, 3],
                     "Go up 1 ten from 30. 30 + 10 = 40. Check: 10 less than 40 is 30."))
    k = its
    order = [k[0], k[1], k[2], k[3], k[8], k[9], k[16], k[10], k[4], k[5], k[11], k[14],
             k[6], k[7], k[12], k[15], k[13], k[17], k[18], k[19]]
    assert len({id(x) for x in order}) == 20
    return {"title": "10 more, 10 less, 1 more, 1 less", "items": order}


# ============================================================ set 5: word problems
def set_stories(rnd, P):
    its = []

    def nxt():
        p = P.next()
        while p[0] == "Leo":
            p = P.next()
        return p

    def st(q, ans, wrong, e):
        its.append(mcq_n(q, ans, wrong, e))

    leo = P.named("Leo")
    n, s, h = leo
    st("%s has 46 stickers. %s gets a pack of 10 more. How many stickers does %s have now?" % (n, cap(s), s),
       56, [47, 36, 55], "46 + 10 = 56. 4 tens and 6 ones plus 1 ten is 5 tens and 6 ones.")
    st("A book has 72 pages. A thin book has 10 fewer pages. How many pages does the thin book have?",
       62, [71, 82, 63], "10 fewer means 10 less. 72 %s 10 = 62." % MINUS)
    st("There are 35 kids in the gym. 10 more kids come in. How many kids are in the gym now?",
       45, [36, 25, 44], "35 + 10 = 45. The tens digit goes from 3 to 4.")
    n, s, h = nxt()
    st("%s has 58 beads. %s uses 10 beads to make a ring. How many beads are left?" % (n, cap(s)),
       48, [57, 68, 49], "58 %s 10 = 48. The ones digit stays 8." % MINUS)
    st("A box has 64 crayons. A big box has 10 more crayons. How many crayons are in the big box?",
       74, [65, 54, 73], "64 + 10 = 74.")
    n, s, h = nxt()
    st("%s is on page 23 of a book. %s reads 10 more pages. What page is %s on now?" % (n, cap(s), s),
       33, [24, 13, 32], "23 + 10 = 33. 2 tens become 3 tens.")
    st("A tree has 81 apples. 10 apples fall off. How many apples are on the tree now?",
       71, [80, 91, 72], "81 %s 10 = 71. 8 tens become 7 tens. The 1 one stays." % MINUS)
    n, s, h = nxt()
    st("%s has 39 cents. %s finds a dime. A dime is 10 cents. How many cents does %s have now?" % (n, cap(s), s),
       49, [40, 29, 48], "39 + 10 = 49. Do not add just 1 cent: a dime is worth 10.")
    st("A bus has 27 people on it. 10 people get off. How many people are still on the bus?",
       17, [26, 37, 18], "27 %s 10 = 17. 2 tens become 1 ten. The 7 ones stay." % MINUS)
    n, s, h = nxt()
    st("There are 90 marbles in a jar. %s takes out 10 marbles. How many marbles are in the jar now?" % n,
       80, [89, 100, 81], "90 %s 10 = 80. 9 tens take away 1 ten is 8 tens." % MINUS)
    st("A farm has 53 cows. It has 10 more sheep than cows. How many sheep are there?",
       63, [54, 43, 64], "10 more than 53 is 63.")
    g = nxt()
    while g[1] != "she":
        g = nxt()
    b = nxt()
    while b[1] != "he":
        b = nxt()
    st("%s has 44 shells. %s has 10 fewer shells than %s. How many shells does %s have?" % (g[0], b[0], g[0], b[0]),
       34, [43, 54, 35], "10 fewer than 44 is 44 %s 10 = 34." % MINUS)
    n, s, h = nxt()
    st("%s jumps rope 66 times. Then %s jumps 10 more times. How many jumps is that in all?" % (n, s),
       76, [67, 56, 75], "66 + 10 = 76.")
    st("I am 10 less than 75. What number am I?", 65, [74, 85, 64], "75 is 7 tens, 5 ones. Take away 1 ten: 6 tens, 5 ones. I am 65.")
    st("I am 10 more than 49. What number am I?", 59, [50, 39, 58], "49 is 4 tens, 9 ones. Add 1 ten: 5 tens, 9 ones. I am 59.")
    n, s, h = nxt()
    st("Pencils come in boxes of 10. %s has 61 pencils. %s buys 1 more box. How many pencils does %s have now?"
       % (n, cap(s), s), 71, [62, 51, 70], "1 box is 10 pencils. 61 + 10 = 71.")
    st("A store has 7 packs of 10 eggs. It sells 1 pack. How many eggs are left?",
       60, [69, 80, 6], "7 packs of 10 is 70 eggs. 1 pack is 10 eggs. 70 %s 10 = 60." % MINUS)
    n, s, h = nxt()
    st("%s makes 35 with 3 tens and 5 ones. %s adds 1 ten. What number does %s have now?" % (n, cap(s), s),
       45, [36, 25, 44], "3 tens and 1 more ten is 4 tens. 4 tens and 5 ones is 45.")
    n, s, h = nxt()
    st("%s had some cards. %s got 10 more cards. Now %s has 52 cards. How many cards did %s have before?"
       % (n, cap(s), s, s), 42, [62, 51, 53], "Before means 10 less than now. 52 %s 10 = 42. Check: 42 + 10 = 52." % MINUS)
    n, s, h = nxt()
    st("%s counts 28 birds in a tree. 10 birds fly away. How many birds are still in the tree?" % n,
       18, [27, 38, 19], "28 %s 10 = 18. 2 tens become 1 ten." % MINUS)
    k = its
    order = [k[0], k[2], k[1], k[3], k[4], k[6], k[5], k[8], k[12], k[9], k[15], k[7],
             k[13], k[14], k[10], k[11], k[17], k[16], k[19], k[18]]
    assert len({id(x) for x in order}) == 20
    return {"title": "Word problems: 10 more and 10 less", "items": order}


# ============================================================ lesson
def body_html():
    return (
        "<h2>10 more and 10 less: change the tens</h2>"
        "<p>A number like 34 has <b>3 tens</b> and <b>4 ones</b>. "
        "To find <b>10 more</b>, add 1 ten. To find <b>10 less</b>, take away 1 ten. "
        "Only the <b>tens digit</b> changes. The ones digit stays the same. You do not need to count by 1s.</p>"
        "<figure class='sn-fig'>" + blocks_svg(3, 4, "add") +
        "<figcaption>34 is 3 tens and 4 ones. Add 1 ten. Now there are 4 tens and 4 ones: 44.</figcaption></figure>"
        "<figure class='sn-fig'>" + blocks_svg(5, 6, "take") +
        "<figcaption>56 is 5 tens and 6 ones. Take away 1 ten. Now there are 4 tens and 6 ones: 46.</figcaption></figure>"
        + ex("10 more", "What is 10 more than 27?",
             "27 is 2 tens and 7 ones. Add 1 ten: 3 tens and 7 ones.", "37")
        + ex("10 less", "What is 10 less than 81?",
             "81 is 8 tens and 1 one. Take away 1 ten: 7 tens and 1 one.", "71") +
        "<h2>Use a hundred chart</h2>"
        "<p>Each row of a hundred chart has 10 numbers. So the number <b>just below</b> is 10 more. "
        "The number <b>just above</b> is 10 less. The number to the right is 1 more, and to the left is 1 less.</p>"
        "<figure class='sn-fig'>" + chart_svg(45, hl={(-1, 0), (1, 0)}) +
        "<figcaption>Above 45 is 35 (10 less). Below 45 is 55 (10 more). Next to 45 are 44 and 46 (1 less, 1 more).</figcaption></figure>"
        + table(["Start", "1 less", "1 more", "10 less", "10 more"], [
            ["45", "44", "46", "35", "55"],
            ["62", "61", "63", "52", "72"],
            ["30", "29", "31", "20", "40"],
        ]) +
        "<h2>Count by 10s from any number</h2>"
        "<p>Keep adding 10 and you get a pattern: 14, 24, 34, 44. The ones digit is always 4.</p>"
        "<figure class='sn-fig'>" + nline_svg(14, [10, 10, 10], ticks=["14", "24", "34", "44"]) +
        "<figcaption>Start at 14 and jump +10 three times: 24, 34, 44.</figcaption></figure>"
        "<h2>Common mistakes</h2>"
        + table(["Mistake", "What to do instead"], [
            ["10 more than 46 is 47 (the ones digit changed)", "Change the tens digit: 56"],
            ["10 less than 56 is 55", "Take away 1 ten: 46"],
            ["10 more than 35 is 44 (counting on from 35)", "Start counting after 35, or just add 1 ten: 45"],
            ["10 more than 46 is 65 (digits turned around)", "Tens first: 5 tens, 6 ones is 56"],
            ["Going up a row on a hundred chart for 10 more", "Down 1 row is 10 more. Up 1 row is 10 less."],
        ])
    )


FAQ = [
    {"q": "How do you find 10 more or 10 less in 1st grade?",
     "a": "Change only the tens digit. For 10 more, add 1 ten (34 becomes 44). For 10 less, take away 1 ten (34 becomes 24). The ones digit stays the same."},
    {"q": "Why does the ones digit stay the same when you add 10?",
     "a": "Adding 10 adds one whole ten and no ones. So the number of ones does not change, and only the tens digit goes up by 1."},
    {"q": "How do you use a hundred chart to find 10 more and 10 less?",
     "a": "Find the number on the chart. The number just below it is 10 more, and the number just above it is 10 less, because each row has 10 numbers."},
    {"q": "Why does my child say 10 more than 46 is 47?",
     "a": "They are changing the ones digit, as if adding 1. Build 46 with 4 ten rods and 6 cubes, add one more rod, and count the tens: 5 tens and 6 ones is 56."},
]


def gen():
    rnd = random.Random(108)
    P = People(rnd)
    sets = [set_more_blocks(rnd), set_less_blocks(rnd), set_chart(rnd), set_mixed(rnd), set_stories(rnd, P)]
    balance(sets, rnd)
    seen = set()
    for s in sets:
        assert len(s["items"]) == 20, (s["title"], len(s["items"]))
        assert sorted(it["a"] for it in s["items"]) == sorted([0, 1, 2, 3] * 5)
        for it in s["items"]:
            assert len(set(it["c"])) == 4, it
            for c in it["c"]:
                for tok in re.findall(r"\d+", c):
                    assert 0 <= int(tok) <= 120, c
            key = it["q"] + "|".join(sorted(it["c"]))
            assert key not in seen, it["q"]
            seen.add(key)
    u = {
        "country": "us", "subject": "math", "grade": "grade-1", "slug": "ten-more-ten-less", "sort": 8,
        "updated": UPDATED, "pdf_url": "",
        "title": "10 More and 10 Less Than a Number",
        "seo_title": "Grade 1 10 More and 10 Less Worksheets: Base-Ten Blocks and Hundred Chart",
        "short_title": "10 more, 10 less",
        "domain": "Number and Operations in Base Ten",
        "standard_code": "1.NBT.C.5",
        "standard_url": "https://www.thecorestandards.org/Math/Content/1/NBT/C/5/",
        "standard_text": "Given a two-digit number, mentally find 10 more or 10 less than the number, without having to count; explain the reasoning used.",
        "meta_desc": "Free Grade 1 worksheets on 10 more and 10 less: add or take away a ten with base-ten blocks, use a hundred chart, compare with 1 more and 1 less, number patterns and short word problems. 100 questions with an answer key.",
        "key_big": "10 more or 10 less changes only the tens digit.",
        "key_sub": "10 more than 46 is 56. 10 less than 46 is 36. The ones digit stays 6. On a hundred chart, go down 1 row for 10 more and up 1 row for 10 less.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }
    return mark_large(u, "(base-ten blocks|open number line)")


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
