# -*- coding: utf-8 -*-
"""
UK Year 2 Maths (National Curriculum in England): the 2, 5 and 10 times tables, odd and even numbers.
  python3 tools/gen_uk_maths_y2_times_tables.py
Every product, quotient, count and odd/even label is checked in code.
HTML attributes use single quotes (no backslashes in the JSON).
Year 2: short sentences for 6-7 year olds, numbers to 100, lots of pictures.
"""
import json, math, os, random, re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "uk", "maths", "year-2")
UPDATED = "2026-11-02"
GREEN = "#006633"
FILL = "#e8f3ec"
RED = "#c0392b"
GOLD = "#e3a81b"
INK = "#2b2b2b"
GREY = "#9a948c"
SKIN = ("#f3c9a4", "#9a6b4a")
FONT = "Arial, Helvetica, sans-serif"
GIRLS = ["Amelia", "Isla", "Freya", "Poppy", "Ava", "Aisha", "Lily", "Zara", "Grace", "Ruby", "Maya", "Evie"]
BOYS = ["Oliver", "Harry", "Mohammed", "Jack", "Arjun", "Noah", "George", "Leo", "Alfie", "Kai", "Ethan", "Charlie"]
X = "×"


# ------------------------------------------------------------ helpers
def mcq(q, correct, cands, e):
    """4 choices: correct + the first 3 unique distractors. Positions are set later by balance()."""
    correct = str(correct)
    seen = {correct}
    pick = []
    for c in cands:
        c = str(c)
        if c in seen or not c or c.startswith("-") or c.startswith("0"):
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
            wrong = [x for i, x in enumerate(c) if i != it["a"]]
            rnd.shuffle(wrong)
            right = c[it["a"]]
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


def par(n):
    return "even" if n % 2 == 0 else "odd"


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


def calc(expr):
    """Evaluate a short expression written with × and ÷ (only digits, spaces and + − × ÷)."""
    assert re.fullmatch(r"[0-9 +×÷−]+", expr), expr
    return eval(expr.replace(X, "*").replace("÷", "/").replace("−", "-"))


def count_list(step, k):
    return ", ".join(str(step * i) for i in range(1, k + 1))


# ------------------------------------------------------------ figures
def dots(x0, y0, rows, cols, cell, col=GREEN):
    return "".join("<circle cx='%d' cy='%d' r='%d' fill='%s'/>"
                   % (x0 + c * cell + cell // 2, y0 + r * cell + cell // 2, cell // 3, col)
                   for r in range(rows) for c in range(cols))


GROUP_SHAPE = {2: (1, 2), 5: (1, 5), 10: (2, 5)}
GROUP_ROW = {2: 5, 5: 3, 10: 3}


def groups_svg(g, n, cell=20, label_sizes=False):
    """g equal groups of n counters, each group in a rounded box."""
    gr, gc = GROUP_SHAPE[n]
    pad, gap = 5, 10
    bw, bh = gc * cell + 2 * pad, gr * cell + 2 * pad
    per_row = min(GROUP_ROW[n], g)
    nrows = (g + per_row - 1) // per_row
    lab = 22 if label_sizes else 0
    W = per_row * bw + (per_row - 1) * gap + 4
    H = nrows * (bh + lab) + (nrows - 1) * gap + 4
    s = []
    for i in range(g):
        r, c = divmod(i, per_row)
        x = 2 + c * (bw + gap)
        y = 2 + r * (bh + lab + gap)
        s.append("<rect x='%d' y='%d' width='%d' height='%d' rx='8' fill='%s' stroke='%s' stroke-width='2'/>"
                 % (x, y, bw, bh, FILL, GREEN))
        s.append(dots(x + pad, y + pad, gr, gc, cell))
        if label_sizes:
            s.append(text(x + bw / 2, y + bh + 17, str(n), 15))
    return svg_wrap(W, H, "".join(s), "%d equal groups with %d counters in each group" % (g, n), large=W > 2.2 * H)


COPPER = ("#d9915a", "#8a5428")
SILVER = ("#dfe3e7", "#7a828a")
COIN = {2: (22, COPPER, 15), 5: (17, SILVER, 14), 10: (21, SILVER, 14)}


def coin(v, cx, cy):
    r, (fill, edge), fs = COIN[v]
    return ("<circle cx='%.1f' cy='%.1f' r='%d' fill='%s' stroke='%s' stroke-width='2'/>" % (cx, cy, r, fill, edge)
            + "<circle cx='%.1f' cy='%.1f' r='%d' fill='none' stroke='%s' stroke-width='1'/>" % (cx, cy, r - 4, edge)
            + text(cx, cy + fs * 0.36, "%dp" % v, fs))


def coins_svg(vals, per_row=5, gap=8, pad=6):
    """coins in rows of per_row, biggest first"""
    vals = sorted(vals, reverse=True)
    rows = [vals[i:i + per_row] for i in range(0, len(vals), per_row)]
    widths = [sum(2 * COIN[v][0] for v in r) + gap * (len(r) - 1) for r in rows]
    heights = [max(2 * COIN[v][0] for v in r) for r in rows]
    W = max(widths) + 2 * pad
    H = sum(heights) + gap * (len(rows) - 1) + 2 * pad
    s, y = [], pad
    for r, rh in zip(rows, heights):
        x = pad
        for v in r:
            d = 2 * COIN[v][0]
            s.append(coin(v, x + d / 2, y + rh / 2))
            x += d + gap
        y += rh + gap
    lab = ", ".join("%d %dp coin%s" % (vals.count(v), v, "" if vals.count(v) == 1 else "s")
                    for v in sorted(set(vals), reverse=True))
    return svg_wrap(W, H, "".join(s), lab)


def hand(x, y):
    """one open hand with 5 fingers, top-left corner at x, y (44 x 56)."""
    f, e = SKIN
    s = []
    for fx, fy, fh in [(10, 4, 26), (17, 0, 30), (24, 2, 28), (31, 8, 22)]:
        s.append("<rect x='%d' y='%d' width='6' height='%d' rx='3' fill='%s' stroke='%s' stroke-width='1.5'/>"
                 % (x + fx, y + fy, fh, f, e))
    s.append("<rect x='%d' y='%d' width='7' height='20' rx='3.5' fill='%s' stroke='%s' stroke-width='1.5' "
             "transform='rotate(-40 %d %d)'/>" % (x + 3, y + 26, f, e, x + 9, y + 40))
    s.append("<rect x='%d' y='%d' width='30' height='28' rx='9' fill='%s' stroke='%s' stroke-width='1.5'/>"
             % (x + 8, y + 26, f, e))
    return "".join(s)


def hands_svg(n):
    o, w, gap = 4, 44, 8
    W = n * w + (n - 1) * gap + 2 * o
    body = "".join(hand(o + i * (w + gap), o) for i in range(n))
    return svg_wrap(W, 56 + 2 * o, body, "%d hands" % n)


def clock_svg(h, m):
    """analogue clock at h:m (m a multiple of 5)"""
    R, c = 48, 54
    s = ["<circle cx='%d' cy='%d' r='%d' fill='#fff' stroke='%s' stroke-width='3'/>" % (c, c, R, INK)]
    for k in range(60):
        a = math.radians(k * 6)
        r1 = R - (6 if k % 5 == 0 else 3)
        s.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='%s'/>"
                 % (c + r1 * math.sin(a), c - r1 * math.cos(a), c + (R - 1) * math.sin(a), c - (R - 1) * math.cos(a),
                    INK, "2" if k % 5 == 0 else "1"))
    for k in range(1, 13):
        a = math.radians(k * 30)
        s.append(text(c + 34 * math.sin(a), c - 34 * math.cos(a) + 5, str(k), 14))
    am = math.radians(m * 6)
    ah = math.radians((h % 12) * 30 + m * 0.5)
    s.append("<line x1='%d' y1='%d' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='4' stroke-linecap='round'/>"
             % (c, c, c + 18 * math.sin(ah), c - 18 * math.cos(ah), INK))
    s.append("<line x1='%d' y1='%d' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='3' stroke-linecap='round'/>"
             % (c, c, c + 27 * math.sin(am), c - 27 * math.cos(am), RED))
    s.append("<circle cx='%d' cy='%d' r='3.5' fill='%s'/>" % (c, c, INK))
    return svg_wrap(2 * c, 2 * c, "".join(s), "analogue clock showing %d:%02d" % (h, m))


def tens_svg(n, ones=0):
    """n tens rods (10 cubes each) and some ones cubes"""
    C, rw, gap, o = 11, 13, 7, 4
    s = []
    for i in range(n):
        x = o + i * (rw + gap)
        for k in range(10):
            s.append("<rect x='%d' y='%d' width='%d' height='%d' fill='%s' stroke='%s' stroke-width='1'/>"
                     % (x, o + k * C, rw, C, FILL, GREEN))
    W = o + n * (rw + gap) - gap + o
    return svg_wrap(W, 10 * C + 2 * o, "".join(s), "%d tens rods of 10 cubes" % n)


PITCH = 28
KINDS = {"counters": ("counter", "counters", RED), "stars": ("star", "stars", GOLD), "blocks": ("block", "blocks", GREEN)}


def obj(kind, cx, cy, col=None):
    col = col or KINDS[kind][2]
    if kind == "counters":
        return "<circle cx='%.1f' cy='%.1f' r='10' fill='%s' stroke='%s' stroke-width='1.5'/>" % (cx, cy, col, INK)
    if kind == "blocks":
        return ("<rect x='%.1f' y='%.1f' width='19' height='19' rx='3' fill='%s' stroke='%s' stroke-width='1.5'/>"
                % (cx - 9.5, cy - 9.5, col, INK))
    pts = []
    for k in range(10):
        r = 11 if k % 2 == 0 else 4.6
        a = math.pi / 2 + k * math.pi / 5
        pts.append("%.1f,%.1f" % (cx + r * math.cos(a), cy - r * math.sin(a) + 1))
    return "<polygon points='%s' fill='%s' stroke='%s' stroke-width='1.2'/>" % (" ".join(pts), col, INK)


def pairs_body(x0, y0, n, kind, outline=False, gx=0):
    """n objects in columns of 2 (pairs). A left-over object sits alone in the top row of the last column."""
    s = []
    cols = (n + 1) // 2
    CP = PITCH + gx
    if outline:
        for c in range(n // 2):
            s.append("<rect x='%d' y='%d' width='%d' height='%d' rx='8' fill='none' stroke='%s' stroke-width='1.5' "
                     "stroke-dasharray='4 3'/>" % (x0 + c * CP + gx / 2 - 1, y0 - 2, PITCH + 2, 2 * PITCH + 4, GREEN))
        if n % 2:
            s.append("<circle cx='%d' cy='%d' r='13' fill='none' stroke='%s' stroke-width='2'/>"
                     % (x0 + (cols - 1) * CP + gx / 2 + PITCH // 2, y0 + PITCH // 2, RED))
    for i in range(n):
        c, r = divmod(i, 2)
        s.append(obj(kind, x0 + c * CP + gx / 2 + PITCH / 2, y0 + r * PITCH + PITCH / 2))
    return "".join(s), cols * CP, 2 * PITCH


def pairs_svg(n, kind):
    o = 6
    body, w, h = pairs_body(o, o, n, kind)
    W, H = w + 2 * o, h + 2 * o
    return svg_wrap(W, H, body, "%d %s in pairs" % (n, KINDS[kind][1]), large=W > 2.2 * H)


def lesson_odd_even_svg(a, b, kind="counters"):
    o, gap, lab = 10, 60, 26
    ba, wa, h = pairs_body(o, o, a, kind, outline=True, gx=10)
    bb, wb, _ = pairs_body(o + wa + gap, o, b, kind, outline=True, gx=10)
    W = wa + wb + gap + 2 * o
    t1 = text(o + wa / 2, o + h + 20, "%d: %s" % (a, par(a)), 16, col=GREEN if a % 2 == 0 else RED)
    t2 = text(o + wa + gap + wb / 2, o + h + 20, "%d: %s" % (b, par(b)), 16, col=GREEN if b % 2 == 0 else RED)
    return svg_wrap(W, h + 2 * o + lab - 6, ba + bb + t1 + t2,
                    "%d counters in pairs, none left over, and %d counters in pairs with 1 left over" % (a, b))


# ------------------------------------------------------------ strategies and mistakes
def tip(a, b):
    """Strategy for a × b, where b is the times table being practised."""
    p = a * b
    if b == 2:
        return "Times 2 means double. Double %d: %d + %d = <b>%d</b>." % (a, a, a, p)
    if b == 5:
        return "Count in 5s, %d times: %s. So the answer is <b>%d</b>." % (a, count_list(5, a), p)
    if b == 10:
        return "%d tens make %d. Count in 10s: %s. So the answer is <b>%d</b>." % (a, p, count_list(10, a), p)
    raise ValueError(b)


def fact_cands(a, b, rnd):
    """Real mistakes: neighbouring fact (one group too many or too few), adding instead of multiplying."""
    p = a * b
    pool = [(a + 1) * b, (a - 1) * b, a + b]
    if b == 2:
        pool.append(3 * a)          # used the 3 times table
    if b == 5:
        pool.append(10 * a)         # used the 10 times table
    if b == 10:
        pool.append(5 * a)          # used the 5 times table
    pool = [v for v in pool if v > 0 and v != p]
    rnd.shuffle(pool)
    return pool + [p + 1, p - 1]


def fact_q(a, b, rnd):
    x, y = (a, b) if rnd.random() < 0.5 else (b, a)
    return mcq("%d %s %d = ?" % (x, X, y), a * b, fact_cands(a, b, rnd), tip(a, b))


def facts(b, mults, rnd):
    mults = list(mults)
    rnd.shuffle(mults)
    return [fact_q(a, b, rnd) for a in mults]


def seq_q(seq, step, wrong, extra=""):
    nxt = seq[-1] + step
    assert all(seq[i + 1] - seq[i] == step for i in range(len(seq) - 1))
    assert nxt not in wrong
    e = "Each number is %d more than the one before: %d + %d = <b>%d</b>. %s" % (step, seq[-1], step, nxt, extra)
    return mcq("Count in %ds. What comes next?<br>%s, ?" % (step, ", ".join(map(str, seq))), nxt, wrong, e.strip())


def count_q(g, n, wrong):
    p = g * n
    assert p not in wrong
    e = "There are %d groups of %d. Count in %ds: %s. %d %s %d = <b>%d</b>." % (
        g, n, n, count_list(n, g), g, X, n, p)
    return mcq(fig(groups_svg(g, n)) + "How many counters are there?", p, wrong, e)


RULE = {2: "Numbers in the 2 times table are even. They end in 0, 2, 4, 6 or 8.",
        5: "Numbers in the 5 times table end in 0 or 5.",
        10: "Numbers in the 10 times table end in 0."}


def multiple_q(ask, right, wrong, n, inside):
    assert (right % n == 0) == inside and all((w % n == 0) != inside for w in wrong)
    e = "%s <b>%d</b> %s." % (RULE[n], right, "is in the %d times table" % n if inside else "is not in the %d times table" % n)
    return mcq(ask, right, wrong, e)


def choice_calc_q(ask, target, right, wrong, e):
    assert calc(right) == target and all(calc(w) != target for w in wrong), (ask, right, wrong)
    return mcq(ask, right, wrong, e)


# ============================================================ set 1: the 2 times table
def set_two(rnd):
    its = [
        count_q(4, 2, [6, 10, 4]),
        count_q(6, 2, [8, 14, 10]),
        count_q(9, 2, [11, 16, 20]),
        count_q(3, 2, [5, 8, 4]),
    ]
    for g in (5, 7):
        p = g * 2
        wrong = ["%d + 2" % g, "%d %s 2" % (g + 1, X), "%d %s 2" % (g - 1, X)]
        e = ("There are %d groups with 2 counters in each group: %d %s 2 = %d. "
             "%d + 2 adds the numbers. It does not count the groups." % (g, g, X, p, g))
        its.append(choice_calc_q(fig(groups_svg(g, 2)) + "Which matches the picture?", p,
                                 "%d %s 2" % (g, X), wrong, e))
    its.append(seq_q([6, 8, 10], 2, [11, 13, 20], "So 2 %s 6 = 12." % X))
    its.append(seq_q([14, 16, 18], 2, [19, 22, 28], "So 2 %s 10 = 20." % X))
    its.append(mcq("Socks come in pairs. How many socks are in 8 pairs?", 16, [10, 14, 18],
                   "A pair is 2. 8 pairs is 8 %s 2. Double 8: 8 + 8 = <b>16</b>. "
                   "10 is 8 + 2, which adds instead of multiplies." % X))
    assert 8 * 2 == 16
    its += facts(2, [3, 4, 5, 6, 7, 8, 9, 11, 12], rnd)
    its.append(multiple_q("Which number is in the 2 times table?", 16, [13, 17, 21], 2, True))
    its.append(multiple_q("Which number is <b>not</b> in the 2 times table?", 15, [12, 18, 20], 2, False))
    assert len(its) == 20, len(its)
    return {"title": "The 2 times table", "items": its}


# ============================================================ set 2: the 5 times table
def set_five(rnd):
    its = [count_q(3, 5, [8, 10, 20]), count_q(6, 5, [11, 25, 35])]
    for k in (4, 7, 9):
        p = 5 * k
        e = "Count in 5s: %s. %d coins of 5p: %d %s 5p = <b>%dp</b>. %dp counts the coins, not the money." % (
            count_list(5, k), k, k, X, p, k)
        its.append(mcq(fig(coins_svg([5] * k)) + "How much money is this?", "%dp" % p,
                       ["%dp" % k, "%dp" % (p - 5), "%dp" % (p + 5), "%dp" % (k + 5)], e))
    its.append(mcq(fig(hands_svg(4)) + "Each hand has 5 fingers. How many fingers are there?", 20, [9, 15, 25],
                   "4 hands of 5 fingers: 5, 10, 15, 20. 4 %s 5 = <b>20</b>. 9 is 4 + 5, which adds instead." % X))
    for h, k in [(3, 4), (2, 9)]:
        m = 5 * k
        e = ("The minute hand points to %d. Each number on the clock is 5 minutes. "
             "Count in 5s: %s. So it is <b>%d minutes</b> past %d." % (k, count_list(5, k), m, h))
        its.append(mcq(fig(clock_svg(h, m)) + "The red hand is the minute hand. How many minutes past %d is it?" % h,
                       "%d minutes" % m, ["%d minutes" % k, "%d minutes" % (10 * k), "%d minutes" % (m - 5)], e))
    its.append(seq_q([15, 20, 25], 5, [26, 35, 50], "So 5 %s 6 = 30." % X))
    its.append(seq_q([40, 45, 50], 5, [51, 60, 100], "So 5 %s 11 = 55." % X))
    its += facts(5, [4, 5, 7, 8, 9, 10, 11, 12], rnd)
    its.append(multiple_q("Which number is in the 5 times table?", 45, [42, 54, 48], 5, True))
    its.append(multiple_q("Which number is <b>not</b> in the 5 times table?", 52, [25, 50, 35], 5, False))
    assert len(its) == 20, len(its)
    return {"title": "The 5 times table", "items": its}


# ============================================================ set 3: the 10 times table
def set_ten(rnd):
    its = []
    for k in (4, 7, 9):
        p = 10 * k
        e = "Each rod is 10 cubes. Count in 10s: %s. %d tens = <b>%d</b>." % (count_list(10, k), k, p)
        its.append(mcq(fig(tens_svg(k)) + "How many cubes are there?", p, [k, k + 10, p - 10, p + 10], e))
    for k in (3, 6, 8):
        p = 10 * k
        e = "Count in 10s: %s. %d %s 10p = <b>%dp</b>. %dp counts the coins, not the money." % (
            count_list(10, k), k, X, p, k)
        its.append(mcq(fig(coins_svg([10] * k)) + "How much money is this?", "%dp" % p,
                       ["%dp" % k, "%dp" % (k + 10), "%dp" % (p - 10), "%dp" % (p + 10)], e))
    its.append(seq_q([30, 40, 50], 10, [51, 55, 70], "So 10 %s 6 = 60." % X))
    its.append(seq_q([60, 70, 80], 10, [81, 85, 100], "So 10 %s 9 = 90." % X))
    its += facts(10, [3, 4, 6, 7, 8, 9, 10], rnd)
    its.append(mcq("? %s 10 = 50" % X, 5, [50, 40, 6],
                   "Ask: what times 10 makes 50? 5 tens make 50, so ? = <b>5</b>. Check: 5 %s 10 = 50." % X))
    assert 5 * 10 == 50
    its.append(mcq("10 %s 4 = 4 %s ?" % (X, X), 10, [4, 40, 14],
                   "You can swap the numbers in a multiplication. 10 %s 4 = 40 and 4 %s 10 = 40. "
                   "So ? = <b>10</b>." % (X, X)))
    assert 10 * 4 == 4 * 10
    its.append(multiple_q("Which number is in the 10 times table?", 70, [17, 75, 61], 10, True))
    its.append(multiple_q("Which number is <b>not</b> in the 10 times table?", 55, [50, 30, 90], 10, False))
    v, wrong = 30, [25, 12, 15]
    assert v % 2 == 0 and v % 5 == 0 and v % 10 == 0
    assert all(not (w % 2 == 0 and w % 5 == 0 and w % 10 == 0) for w in wrong)
    its.append(mcq("Which number is in the 2, the 5 <b>and</b> the 10 times tables?", v, wrong,
                   "<b>30</b> ends in 0, so it is in all three: 2 %s 15, 5 %s 6 and 10 %s 3. "
                   "25 and 15 are only in the 5 times table. 12 is only in the 2 times table." % (X, X, X)))
    assert len(its) == 20, len(its)
    return {"title": "The 10 times table", "items": its}


# ============================================================ set 4: odd and even numbers
def set_odd_even(P):
    its = []
    for n, kind in [(7, "counters"), (10, "stars"), (13, "blocks"), (6, "counters"), (11, "stars"), (14, "blocks")]:
        one, many, _ = KINDS[kind]
        h = n // 2
        q = fig(pairs_svg(n, kind)) + "Make pairs. How many %s? Odd or even?" % many
        if n % 2:
            e = "%d pairs and 1 %s left over. One left over means odd. So %d is <b>odd</b>." % (h, one, n)
        else:
            e = "%d pairs and none left over. Every %s has a partner, so %d is <b>even</b>." % (h, one, n)
        alt = "even" if n % 2 else "odd"
        its.append(mcq(q, "%d: %s" % (n, par(n)),
                       ["%d: %s" % (n, alt), "%d: %s" % (n + 1, par(n + 1)), "%d: %s" % (n - 1, par(n - 1))], e))

    def pick(ask, right, wrong, want):
        assert par(right) == want and all(par(w) != want for w in wrong)
        e = ("Look at the ones digit. Even numbers end in 0, 2, 4, 6 or 8. Odd numbers end in 1, 3, 5, 7 or 9. "
             "<b>%d</b> ends in %d, so it is %s. The tens digit does not matter." % (right, right % 10, want))
        its.append(mcq(ask, right, wrong, e))

    pick("Which number is even?", 34, [43, 27, 61], "even")
    pick("Which number is even?", 58, [85, 41, 69], "even")
    pick("Which number is odd?", 79, [86, 64, 92], "odd")
    pick("Which number is odd?", 23, [32, 50, 74], "odd")
    pick("Which number is odd?", 95, [40, 66, 88], "odd")
    pick("Which number is even?", 70, [17, 75, 93], "even")
    its.append(mcq("Which digit tells you if a number is odd or even?", "the ones digit",
                   ["the tens digit", "the biggest digit", "the smallest digit"],
                   "Only <b>the ones digit</b> matters. 41 has 4 tens, but it ends in 1, so 41 is odd."))
    its.append(mcq("What is the next even number after 36?", 38, [37, 39, 46],
                   "Even numbers go up in 2s: 36, <b>38</b>. 37 is the next number, but it is odd."))
    its.append(mcq("What is the next odd number after 47?", 49, [48, 50, 57],
                   "Odd numbers go up in 2s: 47, <b>49</b>. 48 is the next number, but it is even."))
    its.append(mcq("Count on in 2s. What comes next?<br>1, 3, 5, 7, ?", 9, [8, 10, 11],
                   "Each number is 2 more: 7 + 2 = <b>9</b>. These are the odd numbers."))
    lists = ["12, 14, 16", "12, 15, 18", "21, 41, 61", "13, 23, 33"]
    assert all(int(x) % 2 == 0 for x in lists[0].split(", "))
    assert all(any(int(x) % 2 for x in l.split(", ")) for l in lists[1:])
    its.append(mcq("Which list has <b>only</b> even numbers?", lists[0], lists[1:],
                   "<b>12, 14, 16</b> all end in 2, 4 or 6. 21, 41, 61 have even tens digits, but they end in 1, so they are odd."))
    nm, he, his = P.next()
    its.append(mcq("%s has 9 pairs of gloves. How many gloves? Odd or even?" % nm, "18: even",
                   ["18: odd", "11: odd", "9: odd"],
                   "A pair is 2. 9 %s 2 = 18. Every glove has a partner, so 18 is <b>even</b>. "
                   "11 is 9 + 2, which adds instead of multiplies." % X))
    assert 9 * 2 == 18
    its.append(mcq("There are 17 children in a class. They work in pairs. Is anyone left without a partner?",
                   "Yes, 1 child", ["No", "Yes, 2 children", "Yes, 7 children"],
                   "17 is odd, because it ends in 7. 8 pairs make 16, so <b>1 child</b> is left over."))
    assert 17 - 2 * (17 // 2) == 1
    its.append(mcq("There are 28 pupils in a class. They work in pairs. Is anyone left without a partner?",
                   "No, 28 is even", ["Yes, 28 is odd", "Yes, 1 child", "Yes, 8 children"],
                   "28 ends in 8, so it is even. 14 pairs make 28. <b>Nobody</b> is left over."))
    assert 28 % 2 == 0
    assert len(its) == 20, len(its)
    return {"title": "Odd and even numbers", "items": its}


# ============================================================ set 5: division and word problems
def set_words(P):
    its = []
    for p, d in [(18, 2), (35, 5), (60, 10), (14, 2)]:
        q = p // d
        assert q * d == p
        e = "Think: %d %s ? = %d. %d %s %d = %d, so %d ÷ %d = <b>%d</b>." % (d, X, p, d, X, q, p, p, d, q)
        its.append(mcq("%d ÷ %d = ?" % (p, d), q, [p, q + 1, q - 1, p - d], e))
    for a, b in [(5, 8), (10, 9)]:
        p = a * b
        e = "Ask: %d times what makes %d? %d %s %d = %d, so ? = <b>%d</b>." % (a, p, a, X, b, p, b)
        its.append(mcq("%d %s ? = %d" % (a, X, p), b, [p, p - a, b + 1, b - 1], e))
    its.append(mcq(fig(groups_svg(3, 5)) + "15 counters are put into groups of 5. How many groups?", 3, [15, 5, 10],
                   "Count the groups: there are <b>3</b>. 15 ÷ 5 = 3. Check: 3 %s 5 = 15." % X))

    def w(q, ans, unit, wrong, e, check):
        assert check == ans, (q, check, ans)
        assert ans not in wrong
        u = (lambda v: "%dp" % v) if unit == "p" else (lambda v: "%d %s" % (v, unit))
        its.append(mcq(q, u(ans), [u(v) for v in wrong], e))

    nm, he, his = P.next()
    w("%s shares 12 strawberries equally between 2 bowls. How many go in each bowl?" % nm, 6, "strawberries",
      [12, 10, 5], "12 ÷ 2 = ? Half of 12 is 6. Check: 2 %s 6 = 12. So <b>6 strawberries</b>." % X, 12 // 2)
    w("30 children get into teams of 5 for PE. How many teams are there?", 6, "teams",
      [30, 25, 5], "30 ÷ 5 = ? Count in 5s: 5, 10, 15, 20, 25, 30. That is 6 fives, so <b>6 teams</b>.", 30 // 5)
    nm, he, his = P.next()
    w("%s wants to make 70p with 10p coins. How many 10p coins does %s need?" % (nm, he), 7, "coins",
      [70, 10, 8], "70 ÷ 10 = ? 7 tens make 70. So <b>7 coins</b>.", 70 // 10)
    nm, he, his = P.next()
    w("%s pays 40p with 5p coins. How many 5p coins is that?" % nm, 8, "coins",
      [40, 35, 9], "40 ÷ 5 = ? Count in 5s: 5, 10, 15, 20, 25, 30, 35, 40. That is <b>8 coins</b>.", 40 // 5)
    w("A bike has 2 wheels. There are 6 bikes in the playground. How many wheels?", 12, "wheels",
      [8, 10, 14], "6 bikes with 2 wheels each: 6 %s 2 = <b>12</b>. 8 is 6 + 2, which adds instead of multiplies." % X,
      6 * 2)
    nm, he, his = P.next()
    w("Pencils come in boxes of 10. %s’s teacher buys 4 boxes. How many pencils?" % nm, 40, "pencils",
      [14, 30, 50], "4 boxes of 10: 4 %s 10 = <b>40</b>. 14 is 4 + 10, which adds instead of multiplies." % X, 4 * 10)
    w("5 children hold up one hand each. How many fingers is that?", 25, "fingers",
      [10, 20, 30], "5 hands with 5 fingers: 5, 10, 15, 20, 25. 5 %s 5 = <b>25</b>." % X, 5 * 5)
    nm, he, his = P.next()
    w("Sweets cost 5p each. %s buys 6 sweets. How much does %s spend?" % (nm, he), 30, "p",
      [11, 25, 35], "6 %s 5p = <b>30p</b>. 11p is 6 + 5, which adds instead of multiplies." % X, 6 * 5)
    w("A duck has 2 legs. How many legs do 9 ducks have?", 18, "legs",
      [11, 16, 20], "9 %s 2 is double 9: 9 + 9 = <b>18</b>." % X, 9 * 2)
    w("50 cubes are made into towers of 10. How many towers are there?", 5, "towers",
      [50, 10, 6], "50 ÷ 10 = ? 5 tens make 50. So there are <b>5 towers</b>.", 50 // 10)
    nm, he, his = P.next()
    w("%s puts 40 biscuits on plates, 5 on each plate. How many plates does %s need?" % (nm, he), 8, "plates",
      [40, 35, 9], "40 ÷ 5 = ? 5 %s 8 = 40, so %s needs <b>8 plates</b>." % (X, he), 40 // 5)
    nm, he, his = P.next()
    w("%s has three 10p coins and four 5p coins. How much money does %s have?" % (nm, he), 50, "p",
      [7, 35, 70], "Three 10p coins: 10, 20, 30. Four 5p coins: 5, 10, 15, 20. 30p + 20p = <b>50p</b>. "
      "7p counts the coins, not the money.", 3 * 10 + 4 * 5)
    nm, he, his = P.next()
    w("%s shares 20 stickers equally with a friend. How many does each child get?" % nm, 10, "stickers",
      [20, 18, 5], "Sharing between 2 children: 20 ÷ 2 = 10. Check: 2 %s 10 = 20. Each child gets <b>10 stickers</b>." % X,
      20 // 2)
    assert len(its) == 20, len(its)
    return {"title": "Division facts and word problems", "items": its}


# ============================================================ lesson
def body_html():
    rows = [[str(k), "%d %s 2 = %d" % (k, X, 2 * k), "%d %s 5 = %d" % (k, X, 5 * k), "%d %s 10 = %d" % (k, X, 10 * k)]
            for k in range(1, 13)]
    return (
        "<h2>Multiplication is equal groups</h2>"
        "<p><b>3 %s 5</b> means 3 groups of 5. Count in 5s: 5, 10, 15. So 3 %s 5 = 15. "
        "You can swap the numbers: 5 %s 3 = 15 too.</p>" % (X, X, X)
        + "<figure class='sn-fig'>" + groups_svg(3, 5, 20, True)
        + "<figcaption>3 groups of 5: 5, 10, 15. 3 %s 5 = 15.</figcaption></figure>" % X
        + "<h2>Count in 2s, 5s and 10s</h2>"
        "<p>The 2 times table is <b>doubles</b>: 2 %s 7 = 7 + 7 = 14. "
        "The 5 times table ends in 0 or 5, like 5p coins and the minutes on a clock. "
        "The 10 times table ends in 0, like 10p coins.</p>" % X
        + "<figure class='sn-fig'>" + coins_svg([10] * 4 + [5] * 3, per_row=7)
        + "<figcaption>Four 10p coins: 10, 20, 30, 40. Three 5p coins: 45, 50, 55. That is 55p.</figcaption></figure>"
        + table(["", "2 times table", "5 times table", "10 times table"], rows)
        + "<h2>Odd and even numbers</h2>"
        "<p>Put the objects in pairs. If none are left over, the number is <b>even</b>. "
        "If 1 is left over, it is <b>odd</b>. For a big number, look at the ones digit only: "
        "even numbers end in 0, 2, 4, 6 or 8.</p>"
        + "<figure class='sn-fig'>" + lesson_odd_even_svg(8, 7)
        + "<figcaption>8 makes 4 pairs. 7 makes 3 pairs and 1 left over.</figcaption></figure>"
        + ex("Example", "5 %s 7 = ?" % X, "Count in 5s, 7 times: 5, 10, 15, 20, 25, 30, 35.", "35")
        + ex("Division", "20 ÷ 2 = ?", "Division is the inverse of multiplication. Think: 2 %s ? = 20. 2 %s 10 = 20." % (X, X), "10")
        + ex("Word problem", "How many 10p coins make 60p?", "Count in 10s: 10, 20, 30, 40, 50, 60. That is 6 tens.", "6 coins")
        + "<h2>Common mistakes</h2>"
        + table(["Mistake", "What to do instead"], [
            ["Adding instead: 5 %s 3 = 8" % X, "%s means groups of: 3 groups of 5 = 15" % X],
            ["One group too many: 5 %s 6 = 35" % X, "Count in 5s carefully: 5, 10, 15, 20, 25, 30"],
            ["Saying 43 is even because 4 is even", "Look at the ones digit: 43 ends in 3, so it is odd"],
            ["Giving the big number in division: 20 ÷ 2 = 20", "Ask: 2 times what makes 20? The answer is 10"],
        ])
    )


FAQ = [
    {"q": "What times tables do Year 2 children learn?",
     "a": "The 2, 5 and 10 times tables. The National Curriculum says Year 2 pupils should recall and use the multiplication and division facts for these tables, and recognise odd and even numbers."},
    {"q": "How do you know if a number is odd or even?",
     "a": "Look at the ones digit. If it is 0, 2, 4, 6 or 8 the number is even; if it is 1, 3, 5, 7 or 9 it is odd. So 41 is odd, even though it has 4 tens."},
    {"q": "How can I help my child learn the 2, 5 and 10 times tables?",
     "a": "Count in 2s, 5s and 10s out loud, then use real things: pairs of socks, 5p and 10p coins, and the minutes on a clock. A few minutes of practice each day works better than one long session."},
    {"q": "Which times tables come after Year 2?",
     "a": "In Year 3 children learn the 3, 4 and 8 times tables. By the end of Year 4 they should know every table up to 12 × 12 for the Multiplication Tables Check."},
]


def gen():
    rnd = random.Random(2205)
    P = People(rnd)
    sets = [set_two(rnd), set_five(rnd), set_ten(rnd), set_odd_even(P), set_words(P)]
    balance(sets, rnd)
    seen = set()
    for s in sets:
        assert len(s["items"]) == 20, (s["title"], len(s["items"]))
        assert sorted(it["a"] for it in s["items"]) == sorted([0, 1, 2, 3] * 5)
        for it in s["items"]:
            assert len(set(it["c"])) == 4, it
            assert it["q"].count("<svg") <= 1
            k = it["q"] + "|" + "|".join(sorted(it["c"]))
            assert k not in seen, it["q"]
            seen.add(k)
    return {
        "country": "uk", "subject": "maths", "grade": "year-2", "slug": "2-5-and-10-times-tables", "sort": 5,
        "updated": UPDATED, "pdf_url": "",
        "title": "The 2, 5 and 10 Times Tables",
        "seo_title": "Year 2 Times Tables Worksheets: 2, 5 and 10 Times Tables, Odd and Even",
        "short_title": "2, 5 and 10 times tables",
        "domain": "Multiplication and division",
        "standard_code": "Year 2: Multiplication and division",
        "standard_url": "https://www.gov.uk/government/publications/national-curriculum-in-england-mathematics-programmes-of-study",
        "standard_text": "Recall and use multiplication and division facts for the 2, 5 and 10 multiplication tables, including recognising odd and even numbers.",
        "meta_desc": "Free Year 2 maths worksheets on the 2, 5 and 10 times tables: equal groups, counting in 2s, 5s and 10s with coins and clocks, odd and even numbers, division facts and word problems. 100 questions with an answer key, following the National Curriculum.",
        "key_big": "Count in 2s, 5s and 10s. Every answer in the 2 times table is even.",
        "key_sub": "3 × 5 means 3 groups of 5: 5, 10, 15. Odd or even? Look at the ones digit only. Each fact gives a division fact too: 15 ÷ 5 = 3.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
