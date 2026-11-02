# -*- coding: utf-8 -*-
"""
UK Year 6 Maths: The mean (National Curriculum: Year 6 Statistics)
  python3 tools/gen_uk_maths_y6_mean.py
Every answer is computed with fractions.Fraction. Exact answers are whole numbers or end in at most 2 decimal
places; "to 1 decimal place" answers are rounded half up. Wrong choices come from real mistakes and never have
the same value as the right answer. HTML attributes use single quotes (no backslashes in the JSON).
"""
import json, math, os, random, re
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "uk", "maths", "year-6")
UPDATED = "2026-11-02"
GREEN = "#006633"
BAR = "#2e8b57"
FILL = "#cfe6d6"
FILL2 = "#e6f2ea"
RED = "#c0392b"
INK = "#2b2b2b"
GRID = "#c9d3cc"
FONT = "Arial, Helvetica, sans-serif"
MINUS = "−"
GIRLS = ["Amelia", "Isla", "Freya", "Poppy", "Ava", "Aisha", "Lily", "Zara", "Grace", "Ruby", "Maya", "Evie"]
BOYS = ["Oliver", "Harry", "Mohammed", "Jack", "Arjun", "Noah", "George", "Leo", "Alfie", "Kai", "Ethan", "Charlie"]
DAYS5 = ["Mon", "Tue", "Wed", "Thu", "Fri"]
DAYS7 = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
FULLDAY = {"Mon": "Monday", "Tue": "Tuesday", "Wed": "Wednesday", "Thu": "Thursday", "Fri": "Friday",
           "Sat": "Saturday", "Sun": "Sunday"}


# ------------------------------------------------------------ numbers
def clean(x, dp=2):
    return (10 ** dp) % F(x).denominator == 0


def fmt(x):
    """Fraction -> '1,245', '7.5', '−2', '3.25'. Must be exact to 2 dp."""
    x = F(x)
    neg = x < 0
    x = abs(x)
    assert clean(x), x
    w, r = divmod(x.numerator, x.denominator)
    s = "{:,}".format(w)
    if r:
        s += ("%.2f" % float(F(r, x.denominator)))[1:].rstrip("0")
    return (MINUS if neg else "") + s


def fmt_dp(x, dp):
    """Fixed number of decimal places (x must already be exact to dp)."""
    x = F(x)
    assert clean(x, dp), x
    neg = x < 0
    x = abs(x)
    n = x * 10 ** dp
    assert n.denominator == 1
    n = n.numerator
    w, r = divmod(n, 10 ** dp)
    s = "{:,}".format(w) + ("." + str(r).zfill(dp) if dp else "")
    return (MINUS if neg else "") + s


def r1(x):
    """Round to 1 dp, half up (x > 0)."""
    return F(math.floor(F(x) * 10 + F(1, 2)), 10)


def t1(x):
    return F(math.floor(F(x) * 10), 10)


def money(x):
    """x in pounds (Fraction). 75p or £3.50."""
    p = F(x) * 100
    assert p.denominator == 1 and p > 0, x
    p = p.numerator
    if p < 100:
        return "%dp" % p
    if p % 100 == 0:
        return "£" + fmt(F(p, 100))
    return "£" + fmt_dp(F(p, 100), 2)


def money2(x):
    """Money always with pence (for lists of prices): 70p, £7.00, £1.25."""
    x = F(x)
    if x < 1:
        return money(x)
    return "£" + fmt_dp(x, 2)


def mean(v):
    return F(sum(v), len(v))


def median(v):
    s = sorted(v)
    n = len(s)
    return F(s[n // 2]) if n % 2 else F(s[n // 2 - 1] + s[n // 2], 2)


def lst(v, f=fmt):
    v = [f(x) for x in v]
    return ", ".join(v[:-1]) + " and " + v[-1]


def plus(v, f=fmt):
    out = f(v[0])
    for x in v[1:]:
        out += (" − " + f(-x)) if x < 0 else (" + " + f(x))
    return out


# ------------------------------------------------------------ choices
def mcq(q, correct, cands, e):
    correct = str(correct)
    seen, pick = {correct}, []
    for c in cands:
        if c is None:
            continue
        c = str(c)
        if c in seen:
            continue
        seen.add(c)
        pick.append(c)
        if len(pick) == 3:
            break
    assert len(pick) == 3, (q, correct, cands)
    return {"q": q, "c": pick + [correct], "a": 3, "e": e}


def mcq_n(q, ans, cands, e, show=fmt, dp=2, allow_neg=False):
    """Numbers (Fractions). Distractors: different value, exact to dp, positive unless allow_neg."""
    ans = F(ans)
    vals, cc = {ans}, []
    for c in cands:
        if c is None:
            continue
        c = F(c)
        if c in vals or not clean(c, dp) or (c <= 0 and not allow_neg):
            continue
        vals.add(c)
        cc.append(show(c))
    return mcq(q, show(ans), cc, e)


def fills(ans, step=1):
    a = F(ans)
    return [a + step, a - step, a + 2 * step, a - 2 * step, a + 3 * step, a - 3 * step]


def unit_show(u):
    return lambda x: fmt(x) + u


class People:
    def __init__(self, rnd):
        self.pool = [(n, "she", "her") for n in GIRLS] + [(n, "he", "his") for n in BOYS]
        rnd.shuffle(self.pool)
        self.i = 0

    def next(self):
        p = self.pool[self.i % len(self.pool)]
        self.i += 1
        return p

    def two(self):
        a = self.next()
        b = self.next()
        return a, b


# ------------------------------------------------------------ explanations
def e_mean(v, f=fmt, unit="", count_word="values", res=None):
    S, n = sum(v), len(v)
    m = mean(v)
    zero = " (count the 0 too)" if 0 in v else ""
    r = res if res is not None else f(m) + unit
    return ("Total: %s = %s. There are %d %s%s, so divide by %d: %s ÷ %d = <b>%s</b>."
            % (plus(v, f), f(S), n, count_word, zero, n, f(S), n, r))


def mean_cands(v):
    """Real mistakes when finding a mean."""
    S, n = sum(v), len(v)
    c = [F(S, n - 1), F(S, n + 1), median(v), F(max(v) + min(v), 2)]
    if n % 2:
        c.append(F(v[n // 2]))
    nz = sum(1 for x in v if x != 0)
    if nz < n:
        c.insert(0, F(S, nz))
    c.append(F(S))
    return c


# ------------------------------------------------------------ SVG
def svg_wrap(w, h, body, label):
    return ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 %d %d' width='%d' height='%d' "
            "role='img' aria-label='%s'><g font-family='%s'>%s</g></svg>" % (w, h, w, h, label, FONT, body))


def fig(svg):
    return "<div class='qfig'>" + svg + "</div>"


def tw(t, fs, bold=False):
    return len(str(t)) * fs * (0.62 if bold else 0.58)


def text(x, y, t, fs=14, anchor="middle", bold=False, col=INK, extra=""):
    return ("<text x='%.1f' y='%.1f' font-size='%d'%s fill='%s' text-anchor='%s'%s>%s</text>"
            % (x, y, fs, " font-weight='700'" if bold else "", col, anchor, extra, t))


def towers_body(hs, x0, top, maxh, cube=18, gap=16, after=None):
    """Towers of cubes standing on one base line. Returns (svg parts, width)."""
    s = []
    yb = top + maxh * cube
    for i, h in enumerate(hs):
        x = x0 + i * (cube + gap)
        for k in range(h):
            moved = after is not None and k >= after[i]
            s.append("<rect x='%d' y='%d' width='%d' height='%d' fill='%s' stroke='%s' stroke-width='1.5'/>"
                     % (x, yb - (k + 1) * cube, cube, cube, FILL if not moved else "#f6d6d2", GREEN))
        s.append(text(x + cube / 2, yb + 18, h, 15, bold=True))
    w = len(hs) * (cube + gap) - gap
    s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='2'/>" % (x0 - 6, yb, x0 + w + 6, yb, INK))
    return s, w


def towers_svg(hs):
    maxh = max(hs)
    parts, w = towers_body(hs, 10, 8, maxh)
    W = w + 20
    H = 8 + maxh * 18 + 26
    return svg_wrap(W, H, "".join(parts), "towers of cubes: " + ", ".join(str(h) for h in hs))


def level_svg(before, m):
    """Lesson picture: towers before and after levelling."""
    maxh = max(before)
    cube, gap = 18, 16
    top = 30
    p1, w1 = towers_body(before, 14, top, maxh)
    x2 = 14 + w1 + 70
    p2, w2 = towers_body([m] * len(before), x2, top, maxh)
    W = x2 + w2 + 14
    H = top + maxh * cube + 26
    yb = top + maxh * cube
    s = [text(14 + w1 / 2, 18, "Before", 15, bold=True), text(x2 + w2 / 2, 18, "After: all the same", 15, bold=True)]
    s += p1 + p2
    ay = yb - maxh * cube / 2
    s.append("<path d='M%d %d H%d M%d %d L%d %d L%d %d' fill='none' stroke='%s' stroke-width='2.5'/>"
             % (14 + w1 + 14, ay, x2 - 14, x2 - 22, ay - 7, x2 - 14, ay, x2 - 22, ay + 7, GREEN))
    s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='2' stroke-dasharray='5 4'/>"
             % (8, yb - m * cube, x2 + w2 + 8, yb - m * cube, RED))
    return svg_wrap(int(W), int(H), "".join(s), "towers levelled to the mean")


def bar_svg(title, cat_axis, val_axis, cats, vals, scale, missing=None, label="bar chart", mean_line=None):
    """Vertical bar chart with a grid line at every step of the scale. `missing` = index drawn as a red ?."""
    fs = 14
    top_v = int(math.ceil(max(vals) / scale) * scale)
    nt = top_v // scale
    assert 2 <= nt <= 10, (title, vals, scale)
    s = []
    gy = 18 if nt > 5 else 20
    ph = nt * gy
    lw = tw(top_v, fs)
    x0 = 22 + lw + 6
    slot = max(44, max(tw(c, fs) for c in cats) + 10)
    pw = slot * len(cats)
    y0 = 32
    yb = y0 + ph
    W = x0 + pw + 8
    W = max(W, tw(title, 16, True) + 16)
    s.append(text(W / 2, 18, title, 16, bold=True))
    for k in range(nt + 1):
        y = yb - k * gy
        s.append("<line x1='%d' y1='%.1f' x2='%d' y2='%.1f' stroke='%s' stroke-width='1'/>" % (x0, y, x0 + pw, y, GRID))
        s.append(text(x0 - 5, y + 5, k * scale, fs, anchor="end"))
    for i, (c, v) in enumerate(zip(cats, vals)):
        cx = x0 + slot * i + slot / 2
        bw = min(28, slot * 0.6)
        if i == missing:
            s.append(text(cx, yb - 6, "?", 18, bold=True, col=RED))
        elif v:
            h = v / scale * gy
            s.append("<rect x='%.1f' y='%.1f' width='%.1f' height='%.1f' fill='%s'/>" % (cx - bw / 2, yb - h, bw, h, BAR))
        s.append(text(cx, yb + 17, c, fs))
    if mean_line is not None:
        y = yb - float(mean_line) / scale * gy
        s.append("<line x1='%d' y1='%.1f' x2='%d' y2='%.1f' stroke='%s' stroke-width='2' stroke-dasharray='6 4'/>"
                 % (x0, y, x0 + pw, y, RED))
    s.append("<path d='M%d %d V%d H%d' fill='none' stroke='%s' stroke-width='2'/>" % (x0, y0 - 6, yb, x0 + pw, INK))
    s.append(text(x0 + pw / 2, yb + 36, cat_axis, fs, bold=True))
    mid = y0 + ph / 2
    s.append(text(13, mid, val_axis, fs, bold=True, extra=" transform='rotate(-90 13 %.1f)'" % mid))
    H = yb + 42
    assert tw(val_axis, fs, True) < ph + 30, (val_axis, ph)
    return svg_wrap(int(math.ceil(W)), int(H), "".join(s), label)


def table_svg(title, head, rows, label="table"):
    """head = column headings; rows = lists of cells (first cell = row name)."""
    fs, rh = 15, 28
    ncol = len(head)
    cw = []
    for k in range(ncol):
        cells = [head[k]] + [str(r[k]) for r in rows]
        cw.append(int(max(tw(x, fs, True) for x in cells) + 18))
    tot = sum(cw)
    W = int(max(tot + 8, tw(title, 16, True) + 16))
    x0 = (W - tot) / 2
    top = 28
    s = [text(W / 2, 19, title, 16, bold=True)]
    for r, row in enumerate([head] + rows):
        y = top + r * rh
        x = x0
        for k, cell in enumerate(row):
            hd = r == 0 or k == 0
            s.append("<rect x='%.1f' y='%d' width='%d' height='%d' fill='%s' stroke='%s' stroke-width='1.5'/>"
                     % (x, y, cw[k], rh, FILL2 if hd else "#ffffff", GREEN))
            s.append(text(x + cw[k] / 2, y + 19, cell, fs, bold=hd))
            x += cw[k]
    H = top + (len(rows) + 1) * rh + 4
    return svg_wrap(W, H, "".join(s), label)


# ============================================================ set 1: mean of small sets
SMALL_CTX = [
    ("The numbers of goals a football team scored in {n} matches were", 0, 5, True),
    ("{name} got these marks in {n} spelling tests, out of 10:", 3, 10, False),
    ("The numbers of pupils absent from Year 6 on {n} days were", 0, 6, True),
    ("{name} read these numbers of pages on {n} nights:", 6, 30, False),
    ("The ages, in years, of {n} children at a party are", 5, 11, False),
    ("The numbers of sweets in {n} party bags are", 6, 15, False),
    ("{name} counted the birds in the garden on {n} mornings:", 0, 12, True),
    ("The heights, in cm, of {n} sunflower seedlings are", 4, 15, False),
    ("{name} did these numbers of keepy-uppies in {n} tries:", 2, 25, False),
    ("The numbers of packets of crisps sold at the tuck shop on {n} days were", 8, 30, False),
    ("The numbers of children at after-school club on {n} days were", 9, 24, False),
    ("{name}’s house team scored these points in {n} quizzes:", 4, 20, False),
    ("The numbers of lorries that passed the school in {n} lessons were", 0, 9, True),
    ("{name} scored these numbers of runs in {n} games of cricket:", 0, 18, True),
]


def set_small(rnd, P):
    its = []
    ctx = list(SMALL_CTX)
    rnd.shuffle(ctx)
    # first 6: towers of cubes (share equally)
    seen_t = set()
    for k in range(6):
        for _ in range(5000):
            n = [3, 4, 3, 4, 5, 4][k]
            hs = [rnd.randint(1, 9) for _ in range(n)]
            m = mean(hs)
            if (m.denominator == 1 and len(set(hs)) >= n - 1 and max(hs) - min(hs) >= 4 and tuple(hs) not in seen_t
                    and m != median(hs)):
                break
        seen_t.add(tuple(hs))
        S = sum(hs)
        q = (fig(towers_svg(hs)) + "Cubes are moved between these %d towers until all the towers are the same height. "
             "How many cubes are in each tower now? (This is the mean.)" % n)
        e = ("Total cubes: %s = %d. Share them equally between %d towers: %d ÷ %d = <b>%s</b> cubes each."
             % (plus(hs), S, n, S, n, fmt(m)))
        its.append(mcq_n(q, m, [S, F(S, n - 1), median(hs), F(max(hs) - min(hs)), F(S, n + 1)] + fills(m), e))
    # then 14 lists (4 of them with a zero)
    zero_left = 4
    for i in range(14):
        t, lo, hi, zok = ctx[i % len(ctx)]
        need_zero = zok and zero_left > 0
        for _ in range(20000):
            n = rnd.choice([4, 5, 5, 6, 6])
            v = [rnd.randint(lo, hi) for _ in range(n)]
            if need_zero:
                v[rnd.randrange(n)] = 0
            m = mean(v)
            if m.denominator != 1 or m == median(v) or m <= 0:
                continue
            if (0 in v) != need_zero:
                continue
            if v.count(0) > 1:
                continue
            break
        if need_zero:
            zero_left -= 1
        name, pro, pos = P.next()
        q = "%s <b>%s</b>. What is the mean?" % (t.format(n=n, name=name), lst(v))
        its.append(mcq_n(q, m, mean_cands(v) + fills(m), e_mean(v)))
    assert zero_left == 0
    return {"title": "Find the mean: share equally", "items": its}


# ============================================================ set 2: larger numbers and decimal answers
def set_decimals(rnd, P):
    its = []
    # a) whole-number data, exact decimal mean (4)
    EXACT = [("The heights of {n} children in Year 6 are <b>{v}</b> cm. What is their mean height?", 128, 156, 4, " cm"),
             ("{name} scored <b>{v}</b> in {n} games of darts. What was {pos} mean score?", 20, 60, 4, ""),
             ("A farmer’s {n} hens laid <b>{v}</b> eggs in a month. What is the mean number of eggs per hen?", 14, 28, 5, ""),
             ("The masses of {n} pumpkins are <b>{v}</b> kg. What is their mean mass?", 3, 12, 8, " kg")]
    for t, lo, hi, n, u in EXACT:
        for _ in range(20000):
            v = [rnd.randint(lo, hi) for _ in range(n)]
            m = mean(v)
            if m.denominator > 1 and clean(m) and m != median(v):
                break
        name, pro, pos = P.next()
        q = t.format(n=n, v=lst(v), name=name, pos=pos)
        its.append(mcq_n(q, m, mean_cands(v) + [F(S, n) * 10 for S in [sum(v)]] + fills(m), e_mean(v, unit=u),
                         show=unit_show(u)))
    # b) large numbers with commas (3)
    BIG = [("The numbers of visitors to a museum on {n} days were <b>{v}</b>. What was the mean number of visitors per day?", 1050, 2400, 4),
           ("A school counted the steps pupils walked in {n} lunchtimes: <b>{v}</b>. What is the mean?", 1200, 3200, 5),
           ("The crowds at {n} rugby matches were <b>{v}</b>. What was the mean crowd?", 2100, 6800, 3)]
    for t, lo, hi, n in BIG:
        for _ in range(20000):
            v = [rnd.randint(lo, hi) for _ in range(n)]
            m = mean(v)
            if m.denominator == 1 and m != median(v):
                break
        q = t.format(n=n, v=lst(v))
        its.append(mcq_n(q, m, mean_cands(v) + fills(m, 10), e_mean(v)))
    # c) decimal data (4)
    DEC = [("{name} ran 60 m four times. {Pro} took <b>{v}</b> seconds. What was {pos} mean time?", 92, 126, 4, 10, " s"),
           ("{name}’s long jumps were <b>{v}</b> m. What was {pos} mean jump?", 205, 340, 4, 100, " m"),
           ("A rain gauge collected <b>{v}</b> mm of rain on 5 days. What was the mean daily rainfall?", 2, 96, 5, 10, " mm"),
           ("Five parcels have masses of <b>{v}</b> kg. What is their mean mass?", 8, 45, 5, 10, " kg")]
    for t, lo, hi, n, d, u in DEC:
        for _ in range(20000):
            v = [F(rnd.randint(lo, hi), d) for _ in range(n)]
            m = mean(v)
            if clean(m) and m != median(v) and len(set(v)) == n and m.denominator != 1:
                break
        name, pro, pos = P.next()
        f = (lambda x: fmt_dp(x, 2)) if d == 100 else (lambda x: fmt_dp(x, 1))
        q = t.format(v=lst(v, f), name=name, Pro=pro.capitalize(), pos=pos)
        cands = mean_cands(v) + [m * 10, m / 10]
        show = (lambda x: fmt_dp(x, 2) + u) if d == 100 else unit_show(u)
        e = e_mean(v, f=f, unit=u, res=show(m))
        its.append(mcq_n(q, m, cands + fills(m, F(1, 10)), e, show=show))
    # d) round to 1 decimal place (4)
    ROUND = [("The numbers of pupils in {n} classes are <b>{v}</b>.", 24, 32, 3),
             ("{name} scored <b>{v}</b> on {n} times-tables tests.", 15, 25, 6),
             ("The numbers of cars in the car park on {n} days were <b>{v}</b>.", 30, 70, 7),
             ("The numbers of books borrowed from the library on {n} days were <b>{v}</b>.", 12, 40, 6)]
    for t, lo, hi, n in ROUND:
        for _ in range(20000):
            v = [rnd.randint(lo, hi) for _ in range(n)]
            m = mean(v)
            a = r1(m)
            if not clean(m, 1) and a != t1(m) and r1(F(sum(v), n - 1)) != a and median(v) != a:
                break
        name, pro, pos = P.next()
        q = t.format(n=n, v=lst(v), name=name) + " What is the mean, to 1 decimal place?"
        S = sum(v)
        e = ("Total: %s = %d. Divide by %d: %d ÷ %d = %s… Round to 1 decimal place: <b>%s</b>."
             % (plus(v), S, n, S, n, "%.3f" % float(m), fmt_dp(a, 1)))
        cands = [t1(m), r1(F(S, n - 1)), r1(F(S, n + 1)), median(v), a + F(1, 10), a - F(1, 10)]
        its.append(mcq_n(q, a, cands, e, show=lambda x: fmt_dp(x, 1), dp=1))
    # e) money (5)
    MONEY = [("{name} bought {n} drinks costing <b>{v}</b>. What was the mean cost of a drink?", 65, 180, 4),
             ("The prices of {n} paperback books are <b>{v}</b>. What is the mean price?", 399, 899, 5),
             ("{name} spent <b>{v}</b> on lunch on {n} school days. What was the mean amount per day?", 210, 395, 5),
             ("Four pupils raised <b>{v}</b> for charity. What was the mean amount raised?", 450, 1800, 4),
             ("The costs of {n} cinema tickets were <b>{v}</b>. What was the mean cost?", 650, 1150, 3)]
    for t, lo, hi, n in MONEY:
        for _ in range(20000):
            step = 5
            v = [F(step * rnd.randint(lo // step, hi // step), 100) for _ in range(n)]
            m = mean(v)
            if clean(m) and m != median(v) and len(set(v)) == n and m.denominator != 1:
                break
        name, pro, pos = P.next()
        q = t.format(n=n, v=lst(v, money2), name=name)
        q = q[0].upper() + q[1:]
        S = sum(v)
        e = "Total: %s = %s. Divide by %d: %s ÷ %d = <b>%s</b>." % (" + ".join(money2(x) for x in v), money2(S), n,
                                                                  money2(S), n, money2(m))
        its.append(mcq_n(q, m, mean_cands(v) + fills(m, F(1, 100)), e, show=money2))
    order = [0, 4, 8, 1, 5, 11, 2, 9, 15, 6, 12, 3, 16, 10, 7, 13, 17, 14, 18, 19]
    assert sorted(order) == list(range(20))
    return {"title": "Larger numbers, decimals and money", "items": [its[i] for i in order]}


# ============================================================ set 3: mean from a bar chart or table
BARC = [
    dict(title="Goals in each match", cat="Match", val="Goals", cats=["1", "2", "3", "4", "5", "6"],
         lo=0, hi=6, scale=1, unit="goals", per="match", ask="What was the mean number of goals per match?", zero=True),
    dict(title="Rainfall this week", cat="Day", val="Rainfall (mm)", cats=DAYS5, lo=0, hi=18, scale=2,
         unit="mm", per="day", ask="What was the mean daily rainfall?", zero=True),
    dict(title="Hours of sunshine", cat="Day", val="Hours", cats=DAYS7, lo=0, hi=9, scale=1, unit="hours",
         per="day", ask="What was the mean number of hours of sunshine per day?", zero=True),
    dict(title="Cakes sold at the bake sale", cat="Day", val="Cakes", cats=DAYS5, lo=10, hi=45, scale=5,
         unit="cakes", per="day", ask="What was the mean number of cakes sold per day?", zero=False),
    dict(title="House points this week", cat="House", val="Points", cats=["Red", "Blue", "Green", "Yellow"],
         lo=20, hi=90, scale=10, unit="points", per="house", ask="What was the mean number of points per house?", zero=False),
    dict(title="Books read this term", cat="Pupil", val="Books", cats=["Ava", "Kai", "Lily", "Noah", "Zara"],
         lo=2, hi=16, scale=2, unit="books", per="pupil", ask="What was the mean number of books read per pupil?", zero=False),
    dict(title="Pupils in the library", cat="Day", val="Pupils", cats=DAYS5, lo=10, hi=40, scale=5,
         unit="pupils", per="day", ask="What was the mean number of pupils in the library per day?", zero=False),
    dict(title="Runs in each over", cat="Over", val="Runs", cats=["1", "2", "3", "4", "5", "6"], lo=0, hi=9,
         scale=1, unit="runs", per="over", ask="What was the mean number of runs per over?", zero=True),
]

TABC = [
    dict(title="Highest temperature", row="°C", head="Day", cats=DAYS5, lo=12, hi=24, d=1, unit=" °C",
         per="day", what="the mean highest temperature"),
    dict(title="Distance run", row="km", head="Pupil", cats=["Leo", "Isla", "Jack", "Ruby"], lo=15, hi=48, d=10,
         unit=" km", per="pupil", what="the mean distance"),
    dict(title="Money raised", row="Amount", head="Class", cats=["6A", "6B", "6C", "6D"], lo=40, hi=160, d=1,
         unit="", per="class", what="the mean amount raised", money=True),
    dict(title="Time to run 100 m", row="Seconds", head="Pupil", cats=["Amelia", "Ethan", "Grace", "Alfie"],
         lo=140, hi=199, d=10, unit=" s", per="pupil", what="the mean time"),
    dict(title="Rainfall each month", row="mm", head="Month", cats=["Jan", "Feb", "Mar", "Apr", "May", "Jun"],
         lo=30, hi=90, d=1, unit=" mm", per="month", what="the mean monthly rainfall"),
    dict(title="Pupils absent", row="Pupils", head="Day", cats=DAYS5, lo=0, hi=6, d=1, unit="", per="day",
         what="the mean number of pupils absent per day", zero=True),
    dict(title="Bottles collected", row="Bottles", head="Class", cats=["6A", "6B", "6C", "6D", "6E"], lo=35,
         hi=95, d=1, unit="", per="class", what="the mean number of bottles per class"),
    dict(title="Mass of each bag", row="kg", head="Bag", cats=["A", "B", "C", "D", "E"], lo=12, hi=49, d=10,
         unit=" kg", per="bag", what="the mean mass"),
]


def bar_vals(rnd, c, ok, zero=False):
    n = len(c["cats"])
    for _ in range(50000):
        v = [c["scale"] * rnd.randint(c["lo"] // c["scale"], c["hi"] // c["scale"]) for _ in range(n)]
        if zero and v.count(0) != 1:
            continue
        if not zero and 0 in v:
            continue
        top = int(math.ceil(max(v) / c["scale"]))
        if not 2 <= top <= 10:
            continue
        if ok(v):
            return v
    raise RuntimeError(c["title"])


def bar_of(c, v, missing=None):
    return bar_svg(c["title"], c["cat"], c["val"], c["cats"], v, c["scale"], missing,
                   label="bar chart: " + c["title"].lower())


def set_charts(rnd, P):
    its = []
    # mean from a bar chart (8), 3 with a zero
    zero_plan = [True, False, True, False, False, True, False, True]
    bc = list(BARC)
    rnd.shuffle(bc)
    zc = [c for c in bc if c["zero"]]
    nzc = [c for c in bc if not c["zero"]]
    for z in zero_plan:
        c = zc.pop(0) if z else nzc.pop(0)
        v = bar_vals(rnd, c, lambda v: mean(v).denominator in (1, 2, 4, 5) and mean(v) != median(v)
                     and (len(v) < 7 or mean(v).denominator == 1), zero=z)
        m = mean(v)
        q = fig(bar_of(c, v)) + c["ask"]
        u = " mm" if c["unit"] == "mm" else ""
        its.append(mcq_n(q, m, mean_cands(v) + fills(m), e_mean(v, unit=u, count_word=c["per"] + ("es" if c["per"] == "match" else "s")),
                         show=unit_show(u)))
    # mean from a table (8), 1 with a zero
    tc = list(TABC)
    rnd.shuffle(tc)
    for c in tc:
        n = len(c["cats"])
        for _ in range(50000):
            v = [F(rnd.randint(c["lo"], c["hi"]), c["d"]) for _ in range(n)]
            if c.get("zero"):
                v[rnd.randrange(n)] = F(0)
                if v.count(0) != 1:
                    continue
            m = mean(v)
            if clean(m) and m != median(v) and len(set(v)) >= n - 1 and (c["d"] == 1 or m.denominator > 1):
                if c.get("money") and m.denominator != 1 and not clean(m):
                    continue
                break
        if c.get("money"):
            f = lambda x: fmt(x)
            show = money2
            vs = ["£" + fmt(x) for x in v]
        else:
            f = (lambda x: fmt_dp(x, 1)) if c["d"] == 10 else fmt
            show = unit_show(c["unit"])
            vs = [f(x) for x in v]
        svg = table_svg(c["title"], [c["head"]] + c["cats"], [[c["row"]] + vs], label="table: " + c["title"].lower())
        q = fig(svg) + "What is %s?" % c["what"]
        if c.get("money"):
            e = "Total: %s = %s. There are %d classes, so divide by %d: %s ÷ %d = <b>%s</b>." % (
                " + ".join(money(x) for x in v), money(sum(v)), n, n, money(sum(v)), n, money2(m))
        else:
            e = e_mean(v, f=f, unit=c["unit"], res=show(m), count_word=c["per"] + ("es" if c["per"] in ("class",) else "s"))
        its.append(mcq_n(q, m, mean_cands(v) + fills(m, F(1, c["d"]) if c["d"] > 1 else 1), e, show=show))
    # how many above the mean (2)
    for c in [BARC[3], BARC[6]]:
        c = dict(c)
        v = bar_vals(rnd, c, lambda v: mean(v).denominator == 1 and mean(v) not in v and
                     1 <= sum(1 for x in v if x > mean(v)) <= len(v) - 1 and
                     sum(1 for x in v if x > mean(v)) != sum(1 for x in v if x < mean(v)))
        m = mean(v)
        above = [d for d, x in zip(c["cats"], v) if x > m]
        k = len(above)
        q = fig(bar_of(c, v)) + "On how many days was the number of %s greater than the mean?" % c["unit"]
        e = ("Mean: %s ÷ %d = %s. Bars above %s: %s. So the answer is <b>%d</b>."
             % (fmt(sum(v)), len(v), fmt(m), fmt(m), ", ".join(FULLDAY[d] for d in above), k))
        its.append(mcq_n(q, k, [len(v) - k, len(v), m, k + 1, k - 1, 1], e))
    # missing bar from the mean (2)
    for c in [BARC[4], BARC[5]]:
        n = len(c["cats"])
        for _ in range(50000):
            v = bar_vals(rnd, c, lambda v: True)
            mi = rnd.randrange(1, n)
            m = mean(v)
            if m.denominator == 1 and m != v[mi] and m not in v:
                break
        others = [x for i, x in enumerate(v) if i != mi]
        ans = v[mi]
        q = (fig(bar_of(c, v, missing=mi)) + "The bar for %s is missing. The mean is %s %s per %s. What should the "
             "missing bar show?" % (c["cats"][mi], fmt(m), c["unit"], c["per"]))
        e = ("Total = mean × number of bars = %s × %d = %s. The other bars add to %s = %s. Missing bar: %s − %s = <b>%s</b>."
             % (fmt(m), n, fmt(n * m), plus(others), fmt(sum(others)), fmt(n * m), fmt(sum(others)), fmt(ans)))
        its.append(mcq_n(q, ans, [(n - 1) * m - sum(others), m, n * m, F(sum(others), n - 1)] + fills(ans, c["scale"]), e))
    assert len(its) == 20
    order = [0, 8, 1, 9, 2, 10, 16, 3, 11, 4, 12, 18, 5, 13, 6, 14, 17, 7, 15, 19]
    assert sorted(order) == list(range(20))
    return {"title": "Mean from a bar chart or table", "items": [its[i] for i in order]}


# ============================================================ set 4: total and missing values
TOT_CTX = [
    ("The mean of {n} numbers is {m}. What is the total of the {n} numbers?", "", 1),
    ("The mean mass of {n} parcels is {m} kg. What is their total mass?", " kg", 10),
    ("{name} scored a mean of {m} marks in {n} tests. How many marks did {pro} score altogether?", "", 1),
    ("The mean length of {n} ribbons is {m} cm. What is their total length?", " cm", 10),
    ("The mean of {n} numbers is {m}. What is the sum of the numbers?", "", 1),
]


def set_missing(rnd, P):
    its = []
    for t, u, d in TOT_CTX:
        for _ in range(5000):
            n = rnd.choice([4, 5, 6, 8])
            m = F(rnd.randint(30, 95), 10) if d == 10 else F(rnd.randint(6, 25))
            if d == 10 and m.denominator == 1:
                continue
            break
        name, pro, pos = P.next()
        q = t.format(n=n, m=fmt(m), name=name, pro=pro)
        ans = n * m
        e = "Mean = total ÷ number of values, so total = mean × number of values: %s × %d = <b>%s</b>." % (fmt(m), n, fmt(ans) + u)
        its.append(mcq_n(q, ans, [m + n, m / n if clean(m / n) else None, (n - 1) * m, (n + 1) * m, m]
                         + fills(ans, F(1, d)), e, show=unit_show(u)))
    # missing number (7)
    for k in range(7):
        for _ in range(5000):
            n = [4, 5, 5, 6, 4, 5, 6][k]
            m = rnd.randint(8, 30) if k < 5 else rnd.randint(30, 80)
            known = [rnd.randint(max(1, m - 9), m + 9) for _ in range(n - 1)]
            ans = n * m - sum(known)
            if 1 <= ans and ans not in known and abs(ans - m) >= 3 and (n - 1) * m - sum(known) > 0:
                break
        q = "The mean of %d numbers is %d. %s of the numbers are <b>%s</b>. What is the other number?" % (
            n, m, ["", "", "", "Three", "Four", "Five"][n - 1], lst(known))
        e = ("Total of all %d numbers: %d × %d = %d. Known numbers: %s = %d. Missing number: %d − %d = <b>%d</b>."
             % (n, n, m, n * m, plus(known), sum(known), n * m, sum(known), ans))
        its.append(mcq_n(q, ans, [(n - 1) * m - sum(known), m, n * m, F(sum(known), n - 1)] + fills(ans), e))
    # add a value: new mean (4)
    for k in range(4):
        for _ in range(5000):
            n = rnd.choice([3, 4, 5])
            m = rnd.randint(6, 20)
            x = rnd.randint(1, 40)
            nm = F(n * m + x, n + 1)
            if nm.denominator == 1 and abs(x - m) >= 4 and F(m + x, 2) != nm and nm != m:
                break
        q = "The mean of %d numbers is %d. The number %d is added. What is the mean of all %d numbers now?" % (n, m, x, n + 1)
        e = ("Old total: %d × %d = %d. New total: %d + %d = %d. New mean: %d ÷ %d = <b>%s</b>."
             % (m, n, n * m, n * m, x, n * m + x, n * m + x, n + 1, fmt(nm)))
        its.append(mcq_n(q, nm, [F(m + x, 2), F(n * m + x, n), m + x, n * m + x] + fills(nm), e))
    # remove a value (2)
    for k in range(2):
        for _ in range(5000):
            n = rnd.choice([5, 6])
            m = rnd.randint(8, 20)
            x = rnd.randint(2, 35)
            nm = F(n * m - x, n - 1)
            if nm.denominator == 1 and abs(x - m) >= 4 and nm > 0 and F(n * m - x, n) != nm:
                break
        q = "The mean of %d numbers is %d. One of the numbers, %d, is removed. What is the mean of the other %d numbers?" % (
            n, m, x, n - 1)
        e = ("Old total: %d × %d = %d. Take away %d: %d − %d = %d. New mean: %d ÷ %d = <b>%s</b>."
             % (m, n, n * m, x, n * m, x, n * m - x, n * m - x, n - 1, fmt(nm)))
        its.append(mcq_n(q, nm, [F(n * m - x, n), m - x if m > x else x - m, m, n * m - x] + fills(nm), e))
    # a value is corrected (2)
    for k in range(2):
        name, pro, pos = P.next()
        for _ in range(5000):
            n = rnd.choice([4, 5])
            m = rnd.randint(9, 15)
            wrong = rnd.randint(3, 12)
            right = wrong + n * rnd.randint(2, 3)
            nm = m + F(right - wrong, n)
            if nm.denominator == 1 and right <= 20 and nm <= 18 and wrong <= n * m - wrong <= 20 * (n - 1):
                break
        q = ("%s’s mean score in %d spelling tests (out of 20) was %d. Then %s teacher found a mistake: one score of %d "
             "should have been %d. What is the correct mean?" % (name, n, m, pos, wrong, right))
        e = ("The total goes up by %d − %d = %d. Shared between %d tests, the mean goes up by %d ÷ %d = %d. "
             "Correct mean: %d + %d = <b>%s</b>." % (right, wrong, right - wrong, n, right - wrong, n,
                                                   (right - wrong) // n, m, (right - wrong) // n, fmt(nm)))
        its.append(mcq_n(q, nm, [m + right - wrong, F(m + right, 2), m + 1, right] + fills(nm), e))
    order = [0, 5, 1, 6, 2, 7, 12, 3, 8, 13, 4, 9, 14, 16, 10, 15, 18, 11, 17, 19]
    assert sorted(order) == list(range(20))
    return {"title": "Find the total or a missing value", "items": [its[i] for i in order]}


# ============================================================ set 5: word problems
def set_words(rnd, P):
    its = []
    # goals per match with goalless games (2)
    for n in (6, 8):
        for _ in range(20000):
            v = [rnd.randint(0, 4) for _ in range(n)]
            m = mean(v)
            if v.count(0) in (1, 2) and m.denominator in (1, 2) and m != median(v) and clean(F(sum(v), n - v.count(0))):
                break
        q = ("The school football team scored <b>%s</b> goals in its last %d matches. What was the mean number of goals "
             "per match?" % (lst(v), n))
        its.append(mcq_n(q, m, mean_cands(v) + fills(m, F(1, 2)), e_mean(v, count_word="matches")))
    # temperature (2): one with negative values
    for neg in (True, False):
        for _ in range(20000):
            if neg:
                v = [rnd.randint(-5, 6) for _ in range(5)]
                ok = sum(1 for x in v if x < 0) >= 2 and mean(v).denominator == 1 and mean(v) != 0
            else:
                v = [rnd.randint(14, 27) for _ in range(7)]
                ok = mean(v).denominator == 1
            if ok and mean(v) != median(v) and len(set(v)) >= len(v) - 1:
                break
        m = mean(v)
        if neg:
            q = ("The temperatures at 8 am on 5 winter mornings were <b>%s</b> °C. What was the mean temperature?" % lst(v))
            # mistake: ignore the minus signs
            ab = [abs(x) for x in v]
            cands = [mean(ab), F(sum(v), 4), F(sum(v), 6), median(v), -m]
        else:
            q = ("The highest temperatures in Brighton during one week in July were <b>%s</b> °C. What was the mean "
                 "highest temperature?" % lst(v))
            cands = mean_cands(v)
        e = e_mean(v, unit=" °C", count_word="mornings" if neg else "days")
        if neg:
            e += " (Remember: adding a negative number is the same as subtracting.)"
        its.append(mcq_n(q, m, [c for c in cands if clean(c)] + fills(m), e, show=unit_show(" °C"), allow_neg=True))
    # score needed in the last test (3)
    NEED = [("arithmetic practice papers (out of 40)", 40, 4, 26, 39),
            ("reasoning practice papers (out of 35)", 35, 2, 20, 34),
            ("spelling tests (out of 20)", 20, 3, 11, 19)]
    for what, top, k, lo, hi in NEED:
        name, pro, pos = P.next()
        for _ in range(20000):
            v = [rnd.randint(lo, hi) for _ in range(k)]
            T = rnd.randint(lo + 2, hi - 1)
            ans = (k + 1) * T - sum(v)
            if lo <= ans <= top and abs(ans - T) >= 2 and 2 * T - mean(v) != ans and clean(2 * T - mean(v)):
                break
        q = ("%s’s scores on %d %s were <b>%s</b>. What does %s need to score on the next one to have a mean of %d?"
             % (name, k, what, lst(v), pro, T))
        e = ("For a mean of %d over %d papers, the total must be %d × %d = %d. So far: %s = %d. %s needs %d − %d = <b>%d</b>."
             % (T, k + 1, k + 1, T, (k + 1) * T, plus(v), sum(v), name, (k + 1) * T, sum(v), ans))
        if "spelling" in what:
            e = e.replace("papers", "tests")
        its.append(mcq_n(q, ans, [2 * T - mean(v), T, k * T - sum(v) if k * T > sum(v) else None, (k + 1) * T]
                         + fills(ans), e))
    # compare two teams of different sizes (2)
    for tA, tB, lo, hi in [("Hawks", "Falcons", 3, 15), ("Robins", "Owls", 8, 25)]:
        for _ in range(50000):
            na, nb = 4, 6
            va = [rnd.randint(lo, hi) for _ in range(na)]
            vb = [rnd.randint(lo, hi) for _ in range(nb)]
            ma, mb = mean(va), mean(vb)
            if (ma.denominator == 1 and mb.denominator == 1 and ma - mb >= 2 and sum(vb) > sum(va)
                    and sum(vb) - sum(va) != ma - mb):
                break
        q = ("In a quiz, the %d %s scored <b>%s</b> points and the %d %s scored <b>%s</b> points. "
             "How much greater is the %s’ mean score than the %s’?" % (na, tA, lst(va), nb, tB, lst(vb), tA, tB))
        e = ("%s: %d ÷ %d = %s. %s: %d ÷ %d = %s. Difference: %s − %s = <b>%s</b>. (The %s have the greater total, "
             "but they have more players, so compare the means.)" % (tA, sum(va), na, fmt(ma), tB, sum(vb), nb, fmt(mb),
                                                                   fmt(ma), fmt(mb), fmt(ma - mb), tB))
        its.append(mcq_n(q, ma - mb, [sum(vb) - sum(va), ma, mb, ma + mb] + fills(ma - mb), e))
    # who scored more in total (1)
    (a, ap, _), (b, bp, _) = P.two()
    for _ in range(5000):
        ma, na, mb, nb = rnd.randint(12, 20), 3, rnd.randint(8, 15), 4
        if ma > mb and nb * mb > na * ma:
            break
    d = nb * mb - na * ma
    q = ("%s’s mean score in %d games was %d. %s’s mean score in %d games was %d. Who scored more points in total, "
         "and how many more?" % (a, na, ma, b, nb, mb))
    e = ("%s: %d × %d = %d points. %s: %d × %d = %d points. %s scored %d − %d = <b>%d more</b>. A higher mean does not "
         "always mean a higher total." % (a, ma, na, na * ma, b, mb, nb, nb * mb, b, nb * mb, na * ma, d))
    its.append(mcq(q, "%s, %d more" % (b, d), ["%s, %d more" % (a, ma - mb), "%s, %d more" % (a, d),
                                                "%s, %d more" % (b, ma - mb)], e))
    # combined groups (1)
    for _ in range(5000):
        n1, n2 = rnd.randint(3, 6), rnd.randint(7, 10)
        m1, m2 = rnd.randint(4, 12), rnd.randint(4, 12)
        M = F(n1 * m1 + n2 * m2, n1 + n2)
        if abs(m1 - m2) >= 3 and M.denominator == 1 and F(m1 + m2, 2) != M:
            break
    q = ("In a reading challenge, %d pupils in Year 5 read a mean of %d books each and %d pupils in Year 6 read a mean of "
         "%d books each. What was the mean for all %d pupils?" % (n1, m1, n2, m2, n1 + n2))
    e = ("Totals: %d × %d = %d and %d × %d = %d. All together: %d books for %d pupils. Mean: %d ÷ %d = <b>%s</b>. "
         "(Do not just find the mean of %d and %d: the groups are different sizes.)"
         % (n1, m1, n1 * m1, n2, m2, n2 * m2, n1 * m1 + n2 * m2, n1 + n2, n1 * m1 + n2 * m2, n1 + n2, fmt(M), m1, m2))
    its.append(mcq_n(q, M, [F(m1 + m2, 2), m1 + m2, n1 * m1 + n2 * m2] + fills(M), e))
    # teacher's age (1)
    for _ in range(5000):
        n, m1, m2 = 4, rnd.randint(9, 11), rnd.randint(14, 18)
        age = (n + 1) * m2 - n * m1
        if 25 <= age <= 60:
            break
    q = ("The mean age of %d children is %d years. When their teacher joins them, the mean age of all %d people is %d "
         "years. How old is the teacher?" % (n, m1, n + 1, m2))
    e = ("Children’s total: %d × %d = %d. Total with the teacher: %d × %d = %d. Teacher: %d − %d = <b>%d</b> years."
         % (n, m1, n * m1, n + 1, m2, (n + 1) * m2, (n + 1) * m2, n * m1, age))
    its.append(mcq_n(q, age, [m2 - m1, n * m2 - n * m1, (n + 1) * m2, F(m1 + m2, 2) * 2, m1 + m2] + fills(age), e,
                     show=unit_show(" years")))
    # single contexts (8)
    name, pro, pos = P.next()
    for _ in range(5000):
        v = [F(5 * rnd.randint(13, 36), 100) for _ in range(4)]
        if clean(mean(v)) and mean(v) != median(v) and len(set(v)) == 4:
            break
    q = ("At the tuck shop, %s bought 4 snacks costing <b>%s</b>. What was the mean cost of a snack?" % (name, lst(v, money2)))
    e = "Total: %s = %s. Divide by 4: %s ÷ 4 = <b>%s</b>." % (" + ".join(money2(x) for x in v), money2(sum(v)),
                                                            money2(sum(v)), money2(mean(v)))
    its.append(mcq_n(q, mean(v), mean_cands(v) + fills(mean(v), F(1, 100)), e, show=money2))
    for _ in range(5000):
        v = [F(rnd.randint(85, 160), 10) for _ in range(5)]
        if clean(mean(v)) and mean(v) != median(v) and mean(v).denominator != 1 and len(set(v)) == 5:
            break
    f1 = lambda x: fmt_dp(x, 1)
    q = ("Year 6 grew 5 bean plants. After 3 weeks their heights were <b>%s</b> cm. What was the mean height?" % lst(v, f1))
    its.append(mcq_n(q, mean(v), mean_cands(v) + fills(mean(v), F(1, 10)), e_mean(v, f=f1, unit=" cm", count_word="plants", res=fmt(mean(v)) + " cm"),
                     show=unit_show(" cm")))
    for _ in range(5000):
        v = [rnd.randint(31, 69) * 10 for _ in range(4)]
        if mean(v).denominator == 1 and mean(v) % 5 != 0 and mean(v) != median(v):
            break
    q = ("Four Year 6 classes held a cake sale. They raised <b>%s</b>. What was the mean amount raised per class?"
         % lst(v, money))
    e = "Total: %s = %s. Divide by 4: %s ÷ 4 = <b>%s</b>." % (" + ".join(money(x) for x in v), money(sum(v)),
                                                            money(sum(v)), money2(mean(v)))
    its.append(mcq_n(q, mean(v), mean_cands(v) + fills(mean(v), 5), e, show=money2))
    for _ in range(5000):
        n, m = 4, rnd.randint(26, 31)
        x = rnd.randint(18, 34)
        nm = F(n * m + x, n + 1)
        if nm.denominator == 1 and abs(x - m) >= 4 and F(m + x, 2) != nm:
            break
    q = ("A school has 4 classes with a mean of %d pupils per class. A new class of %d pupils joins the school. "
         "What is the new mean number of pupils per class?" % (m, x))
    e = ("Pupils before: 4 × %d = %d. Now: %d + %d = %d pupils in 5 classes. New mean: %d ÷ 5 = <b>%s</b>."
         % (m, 4 * m, 4 * m, x, 4 * m + x, 4 * m + x, fmt(nm)))
    its.append(mcq_n(q, nm, [F(m + x, 2), F(4 * m + x, 4), m + 1, m - 1] + fills(nm), e))
    m = F(rnd.randint(12, 19), 10)
    q = "The mean mass of 3 bags of flour is %s kg. What is the total mass of the 3 bags?" % fmt(m)
    its.append(mcq_n(q, 3 * m, [m + 3, 2 * m, 4 * m, m / 3 if clean(m / 3) else None] + fills(3 * m, F(1, 10)),
                     "Total = mean × number of bags = %s × 3 = <b>%s kg</b>." % (fmt(m), fmt(3 * m)), show=unit_show(" kg")))
    name, pro, pos = P.next()
    m = F(rnd.choice([35, 45, 55, 65]), 10)
    q = ("%s cycled a mean distance of %s km a day for 6 days. How far did %s cycle altogether?" % (name, fmt(m), pro))
    its.append(mcq_n(q, 6 * m, [m + 6, 5 * m, 7 * m, m * 60] + fills(6 * m, F(1, 2)),
                     "Total = mean × number of days = %s × 6 = <b>%s km</b>." % (fmt(m), fmt(6 * m)), show=unit_show(" km")))
    for _ in range(20000):
        v = [rnd.choice([0, 0, rnd.randint(1, 14)]) for _ in range(7)]
        m = mean(v)
        if 2 <= v.count(0) <= 3 and m.denominator == 1 and m != median(v) and clean(F(sum(v), 7 - v.count(0))):
            break
    q = ("The rainfall in Manchester each day for a week was <b>%s</b> mm. What was the mean daily rainfall?" % lst(v))
    its.append(mcq_n(q, m, mean_cands(v) + fills(m), e_mean(v, unit=" mm", count_word="days"), show=unit_show(" mm")))
    name, pro, pos = P.next()
    for _ in range(5000):
        v = [F(rnd.randint(150, 230), 10) for _ in range(4)]
        if clean(mean(v)) and mean(v) != median(v) and len(set(v)) == 4 and mean(v).denominator != 1:
            break
    q = ("%s swam a length of the pool 4 times. %s times were <b>%s</b> seconds. What was %s mean time?"
         % (name, pos.capitalize(), lst(v, f1), pos))
    its.append(mcq_n(q, mean(v), mean_cands(v) + fills(mean(v), F(1, 10)), e_mean(v, f=f1, unit=" s", count_word="lengths", res=fmt(mean(v)) + " s"),
                     show=unit_show(" s")))
    assert len(its) == 20, len(its)
    rnd.shuffle(its)
    return {"title": "Word problems", "items": its}


# ============================================================ lesson
def ex(title, q, s, a):
    return ("<div class='sn-ex'><span class='sn-ex-t'>%s</span><p class='sn-ex-q'>%s</p>"
            "<p class='sn-ex-s'>%s</p><p class='sn-ex-a'>Answer: %s</p></div>" % (title, q, s, a))


def table(head, rows):
    h = "".join("<th>%s</th>" % x for x in head)
    b = "".join("<tr>" + "".join("<td>%s</td>" % c for c in r) + "</tr>" for r in rows)
    return "<div class='sn-tw'><table class='sn-table'><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>" % (h, b)


LV = [7, 3, 6, 4]
BV = [3, 0, 2, 4, 1]


def body_html():
    assert mean(LV) == 5 and mean(BV) == 2
    lev = level_svg(LV, 5).replace("<svg ", "<svg data-pf='lg' ", 1)
    bar = bar_svg("Goals in each match", "Match", "Goals", ["1", "2", "3", "4", "5"], BV, 1,
                  label="bar chart: goals in each match", mean_line=2).replace("<svg ", "<svg data-pf='lg' ", 1)
    return (
        "<h2>What is the mean?</h2>"
        "<p>The <b>mean</b> is a kind of average. It tells you what each value would be if the total were "
        "<b>shared out equally</b>.</p>"
        "<p><b>Mean = total ÷ number of values</b></p>"
        "<figure class='sn-fig'>" + lev +
        "<figcaption>Towers of 7, 3, 6 and 4 cubes: 20 cubes in total. Share them between 4 towers: 20 ÷ 4 = 5. "
        "The mean is 5.</figcaption></figure>" +
        ex("Example 1", "Find the mean of 12, 8, 15, 9 and 11.",
           "Total: 12 + 8 + 15 + 9 + 11 = 55. There are 5 numbers. 55 ÷ 5 = 11.", "11") +
        "<h2>When the mean is a decimal</h2>"
        "<p>The mean does not have to be a whole number, and it does not have to be one of the values.</p>" +
        ex("Example 2", "Four children are 136 cm, 142 cm, 139 cm and 145 cm tall. What is their mean height?",
           "Total: 136 + 142 + 139 + 145 = 562. 562 ÷ 4 = 140.5.", "140.5 cm") +
        ex("Example 3", "Four drinks cost £2.40, £1.85, £3.20 and £1.75. What is the mean cost?",
           "Total: £2.40 + £1.85 + £3.20 + £1.75 = £9.20. £9.20 ÷ 4 = £2.30.", "£2.30") +
        "<h2>The mean from a bar chart</h2>"
        "<p>Read every bar, add them, then divide by the number of bars. A bar of 0 still counts.</p>"
        "<figure class='sn-fig'>" + bar +
        "<figcaption>3 + 0 + 2 + 4 + 1 = 10 goals in 5 matches. 10 ÷ 5 = 2 goals per match (the dashed line).</figcaption></figure>"
        "<h2>Work backwards from the mean</h2>"
        "<p>If you know the mean, you can find the total: <b>total = mean × number of values</b>. "
        "This helps you find a missing value.</p>" +
        ex("Example 4", "The mean of 5 numbers is 12. Four of the numbers are 10, 15, 9 and 14. What is the fifth number?",
           "Total of all 5: 5 × 12 = 60. The four numbers add to 10 + 15 + 9 + 14 = 48. 60 − 48 = 12.", "12") +
        ex("Example 5", "Isla’s first 3 test scores are 16, 13 and 17. What must she score in the 4th test to have a mean of 16?",
           "Total needed: 4 × 16 = 64. So far: 16 + 13 + 17 = 46. 64 − 46 = 18.", "18") +
        "<h2>Common mistakes</h2>" +
        table(["Mistake", "What to do instead"], [
            ["Forgetting to count a 0 (a match with no goals)", "A 0 is a value: count it when you divide"],
            ["Dividing by the wrong number", "Divide by how many values there are"],
            ["Leaving out a value when adding", "Tick each value as you add it"],
            ["Choosing the middle value of the list", "The mean is total ÷ number of values"],
            ["Giving the total as the answer", "Remember to divide"],
            ["Dividing the mean by the count to find the total", "Total = mean × number of values"],
            ["Averaging two means for groups of different sizes", "Find each total, add them, then divide by everyone"],
        ])
    )


FAQ = [
    {"q": "How do you find the mean in Year 6?",
     "a": "Add all the values to find the total, then divide by how many values there are. For 4, 7, 6 and 3 the total is 20, and 20 ÷ 4 = 5, so the mean is 5."},
    {"q": "Is the mean in the Year 6 maths SATs?",
     "a": "Yes. Calculating and interpreting the mean is part of the Year 6 statistics curriculum, so it can come up in the reasoning papers, often with a table or bar chart or as a missing-value problem."},
    {"q": "How do you find a missing number when you know the mean?",
     "a": "Multiply the mean by the number of values to get the total. Then subtract the numbers you know. If the mean of 4 numbers is 10 and three are 8, 12 and 9, the missing number is 40 − 29 = 11."},
    {"q": "What is the difference between the mean, median and mode?",
     "a": "The mean shares the total out equally. The median is the middle value and the mode is the most common value; in England these are taught from Year 7, while Year 6 focuses on the mean."},
]


def balance(sets, rnd):
    for s in sets:
        items = s["items"]
        targets = [i for i in range(4) for _ in range(5)]
        rnd.shuffle(targets)
        for it, t in zip(items, targets):
            corr = it["c"][it["a"]]
            wrong = [c for k, c in enumerate(it["c"]) if k != it["a"]]
            rnd.shuffle(wrong)
            wrong.insert(t, corr)
            it["c"] = wrong
            it["a"] = t
        assert [sum(1 for it in items if it["a"] == i) for i in range(4)] == [5, 5, 5, 5]


def mark_large(u, pattern):
    rx = re.compile(r"<svg (?=[^>]*aria-label='" + pattern + ")")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u


def gen_unit():
    rnd = random.Random(6620)
    P = People(rnd)
    sets = [set_small(rnd, P), set_decimals(rnd, P), set_charts(rnd, P), set_missing(rnd, P), set_words(rnd, P)]
    balance(sets, rnd)
    seen = set()
    for s in sets:
        assert len(s["items"]) == 20, (s["title"], len(s["items"]))
        for it in s["items"]:
            assert len(set(it["c"])) == 4, it
            assert it["e"], it
            assert it["q"].count("<svg") <= 1, it["q"]
            assert it["q"] not in seen, it["q"]
            seen.add(it["q"])
    return {
        "country": "uk", "subject": "maths", "grade": "year-6", "slug": "mean", "sort": 20,
        "updated": UPDATED, "pdf_url": "",
        "title": "The Mean",
        "seo_title": "Year 6 Mean Worksheets: Find the Mean, Missing Values and Bar Charts (Free, with Answers)",
        "short_title": "Mean",
        "domain": "Statistics",
        "standard_code": "Year 6: Statistics",
        "standard_url": "https://www.gov.uk/government/publications/national-curriculum-in-england-mathematics-programmes-of-study",
        "standard_text": "Calculate and interpret the mean as an average.",
        "meta_desc": "Free Year 6 maths worksheets on the mean: share equally, find the mean of whole numbers, decimals and money, read it from bar charts and tables, work out a missing value, and solve SATs-style word problems. 100 questions with an answer key, following the National Curriculum.",
        "key_big": "Mean = total ÷ number of values",
        "key_sub": "The mean is what each value would be if the total were shared out equally. Count every value, including 0. To work backwards, total = mean × number of values.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }


if __name__ == "__main__":
    u = gen_unit()
    mark_large(u, "(bar chart|table|towers)")
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
