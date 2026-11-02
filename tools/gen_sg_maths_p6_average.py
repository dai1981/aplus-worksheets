# -*- coding: utf-8 -*-
"""
Singapore Primary 6 Maths: Average (MOE 2021 Primary Mathematics Syllabus, Standard: Statistics)
  python3 tools/gen_sg_maths_p6_average.py
Average = total value ÷ number of data, and total value = average × number of data.
Helpers adapted from gen_uk_maths_y6_mean.py; all wording, names, money and units rewritten for Singapore.
Every answer is computed with fractions.Fraction. Wrong answers come from real mistakes: dividing by the wrong
number of data, forgetting a 0, giving the total or the middle value, adding a new value to the average,
dividing the average to get the total, and forgetting to multiply back to the total.
Singapore number style: 4536, 12 360 (no-break space), $4.50, 85¢, 1 kg 250 g, 1 ℓ 200 ml.
HTML attributes use single quotes (no backslashes in the JSON).
"""
import json, math, os, random, re
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "sg", "maths", "primary-6")
UPDATED = "2026-11-03"
GREEN = "#006633"
BAR = "#2e8b57"
FILL = "#cfe6d6"
FILL2 = "#fbe3c4"
HEAD = "#e6f2ea"
RED = "#c0392b"
INK = "#2b2b2b"
GRID = "#c9d3cc"
FONT = "Arial, Helvetica, sans-serif"
MINUS = "−"
NBSP = " "
GIRLS = ["Siti", "Nurul", "Farah", "Mei Ling", "Hui Min", "Xin Yi", "Priya", "Devi", "Kavya", "Chloe", "Sarah"]
BOYS = ["Ali", "Ahmad", "Hafiz", "Wei Ming", "Jun Jie", "Zhi Hao", "Raju", "Kumar", "Arjun", "Ethan", "Ryan"]
DAYS5 = ["Mon", "Tue", "Wed", "Thu", "Fri"]


# ------------------------------------------------------------ numbers
def clean(x, dp=2):
    return (10 ** dp) % F(x).denominator == 0


def grp(w):
    return str(w) if w < 10000 else "{:,}".format(w).replace(",", NBSP)


def fmt(x):
    """Fraction -> '4536', '12 360', '7.5', '3.25'. Must be exact to 2 dp."""
    x = F(x)
    neg = x < 0
    x = abs(x)
    assert clean(x), x
    w, r = divmod(x.numerator, x.denominator)
    s = grp(w)
    if r:
        s += ("%.2f" % float(F(r, x.denominator)))[1:].rstrip("0")
    return (MINUS if neg else "") + s


def fmt_dp(x, dp):
    x = F(x)
    assert clean(x, dp) and x >= 0, x
    n = x * 10 ** dp
    assert n.denominator == 1
    w, r = divmod(n.numerator, 10 ** dp)
    return grp(w) + ("." + str(r).zfill(dp) if dp else "")


def money(x):
    """x in dollars: 85¢, $4.50, $12.00."""
    c = F(x) * 100
    assert c.denominator == 1 and c > 0, x
    if c < 100:
        return "%d¢" % c.numerator
    return "$" + fmt_dp(x, 2)


def dollars(x):
    """Whole dollars without cents ($8), else $4.50."""
    x = F(x)
    return "$" + fmt(x) if x.denominator == 1 else money(x)


def comp(x, big, small, k=1000):
    """Compound unit from the small unit: 1250 g -> 1 kg 250 g."""
    x = F(x)
    assert x.denominator == 1 and x > 0, x
    x = x.numerator
    a, b = divmod(x, k)
    if a == 0:
        return "%d %s" % (b, small)
    if b == 0:
        return "%d %s" % (a, big)
    return "%d %s %d %s" % (a, big, b, small)


def kg(x):
    return comp(x, "kg", "g")


def litre(x):
    return comp(x, "ℓ", "ml")


def hmin(x):
    return comp(x, "h", "min", 60)


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
    return " + ".join(f(x) for x in v)


WORDN = {2: "two", 3: "three", 4: "four", 5: "five", 6: "six", 7: "seven", 8: "eight", 9: "nine", 10: "ten"}


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


def mcq_n(q, ans, cands, e, show=fmt, dp=2):
    ans = F(ans)
    vals, cc = {ans}, []
    for c in cands:
        if c is None:
            continue
        c = F(c)
        if c in vals or not clean(c, dp) or c <= 0:
            continue
        vals.add(c)
        cc.append(show(c))
    return mcq(q, show(ans), cc, e)


def fills(ans, step=1):
    a = F(ans)
    return [a + step, a - step, a + 2 * step, a - 2 * step, a + 3 * step, a - 3 * step]


def us(u):
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


def poss(name):
    return name + "’s"


# ------------------------------------------------------------ explanations
def e_avg(v, f=fmt, res=None, word="numbers"):
    S, n = sum(v), len(v)
    zero = " (the 0 counts too)" if 0 in v else ""
    r = res if res is not None else f(mean(v))
    return ("Total: %s = %s. There are %d %s%s. Average = %s ÷ %d = <b>%s</b>."
            % (plus(v, f), f(S), n, word, zero, f(S), n, r))


def avg_cands(v):
    """Real mistakes when finding an average."""
    S, n = sum(v), len(v)
    c = []
    nz = sum(1 for x in v if x != 0)
    if nz < n:
        c.append(F(S, nz))
    c += [F(S, n - 1), F(S, n + 1), median(v), F(max(v) + min(v), 2), F(S)]
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


def towers_body(hs, x0, top, maxh, cube=18, gap=16):
    s = []
    yb = top + maxh * cube
    for i, h in enumerate(hs):
        x = x0 + i * (cube + gap)
        for k in range(h):
            s.append("<rect x='%d' y='%d' width='%d' height='%d' fill='%s' stroke='%s' stroke-width='1.5'/>"
                     % (x, yb - (k + 1) * cube, cube, cube, FILL, GREEN))
        s.append(text(x + cube / 2, yb + 18, h, 15, bold=True))
    w = len(hs) * (cube + gap) - gap
    s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='2'/>" % (x0 - 6, yb, x0 + w + 6, yb, INK))
    return s, w


def level_svg(before, m):
    """Lesson picture: towers before and after levelling."""
    maxh = max(before)
    cube = 18
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
    return svg_wrap(int(W), int(H), "".join(s), "towers levelled to the average")


def bar_svg(title, cat_axis, val_axis, cats, vals, scale, missing=None, label="bar graph", avg_line=None):
    """Vertical bar graph with a grid line at every step of the scale. `missing` = index drawn as a red ?."""
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
    if avg_line is not None:
        y = yb - float(avg_line) / scale * gy
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
                     % (x, y, cw[k], rh, HEAD if hd else "#ffffff", GREEN))
            s.append(text(x + cw[k] / 2, y + 19, cell, fs, bold=hd))
            x += cw[k]
    H = top + (len(rows) + 1) * rh + 4
    return svg_wrap(W, H, "".join(s), label)


def model_svg(rows, px, total=None, label="bar model"):
    """Bar model. rows = [(name, [(length, inside_label, kind)], right_label)], kind 'u' (unit) or 'x' (extra).
    Lengths are drawn exactly to scale (px per unit of length). total = label of a brace around all rows."""
    fs, rh, gap = 14, 26, 14
    nw = max(tw(r[0], fs, True) for r in rows)
    x0 = 8 + nw + 8
    s = []
    y = 8
    ends = []
    for name, segs, rl in rows:
        x = x0
        s.append(text(x0 - 8, y + rh / 2 + 5, name, fs, anchor="end", bold=True))
        for ln, lab, kind in segs:
            w = float(ln) * px
            s.append("<rect x='%.1f' y='%d' width='%.1f' height='%d' fill='%s' stroke='%s' stroke-width='1.5'/>"
                     % (x, y, w, rh, FILL if kind == "u" else FILL2, GREEN))
            if lab:
                assert tw(lab, fs) + 4 <= w, (lab, w)
                s.append(text(x + w / 2, y + rh / 2 + 5, lab, fs))
            x += w
        end = x
        if rl:
            s.append(text(x + 6, y + rh / 2 + 5, rl, fs, anchor="start", bold=True, col=RED if rl == "?" else INK))
            end = x + 6 + tw(rl, fs, True)
        ends.append(end)
        y += rh + gap
    bottom = y - gap
    W = max(ends) + 8
    if total:
        xb = max(ends) + 10
        top = 8
        mid = (top + bottom) / 2
        d = ("M%.1f %.1f Q%.1f %.1f %.1f %.1f V%.1f Q%.1f %.1f %.1f %.1f Q%.1f %.1f %.1f %.1f V%.1f Q%.1f %.1f %.1f %.1f"
             % (xb, top, xb + 6, top, xb + 6, top + 6, mid - 6, xb + 6, mid, xb + 12, mid, xb + 6, mid, xb + 6, mid + 6,
                bottom - 6, xb + 6, bottom, xb, bottom))
        s.append("<path d='%s' fill='none' stroke='%s' stroke-width='2'/>" % (d, INK))
        s.append(text(xb + 16, mid + 5, total, fs, anchor="start", bold=True, col=RED if total == "?" else INK))
        W = xb + 16 + tw(total, fs, True) + 8
    H = bottom + 8
    return svg_wrap(int(math.ceil(W)), int(H), "".join(s), label)


# ============================================================ set 1: find the average
WHOLE = [
    ("{name} scored <b>{v}</b> marks in {n} spelling tests. Each test was out of 20. What was {pos} average mark?", 9, 20, "tests"),
    ("{name} read <b>{v}</b> pages of a storybook on {n} nights. What was the average number of pages per night?", 12, 45, "nights"),
    ("A hawker sold <b>{v}</b> plates of chicken rice in the first hour on {n} days. What was the average number of "
     "plates sold per day?", 18, 46, "days"),
    ("The numbers of pupils who went to the library during recess on {n} days were <b>{v}</b>. What was the average "
     "number of pupils per day?", 15, 40, "days"),
]
ZERO = [
    ("The numbers of pupils absent from Class 6A on {n} days were <b>{v}</b>. What was the average number of pupils "
     "absent per day?", 0, 5, "days"),
    ("The school football team scored <b>{v}</b> goals in {n} matches. What was the average number of goals per match?",
     0, 5, "matches"),
]


def set_find(rnd, P):
    its = []
    # whole numbers (4)
    for k, (t, lo, hi, word) in enumerate(WHOLE):
        n = [4, 5, 5, 6][k]
        for _ in range(20000):
            v = [rnd.randint(lo, hi) for _ in range(n)]
            m = mean(v)
            if m.denominator == 1 and m != median(v) and len(set(v)) == n:
                break
        name, pro, pos = P.next()
        q = t.format(n=n, v=lst(v), name=name, pos=pos)
        its.append(mcq_n(q, m, avg_cands(v) + fills(m), e_avg(v, word=word)))
    # with a zero (2)
    for t, lo, hi, word in ZERO:
        for _ in range(20000):
            n = rnd.choice([5, 6])
            v = [rnd.randint(1, hi) for _ in range(n)]
            v[rnd.randrange(n)] = 0
            m = mean(v)
            if m.denominator == 1 and m != median(v) and F(sum(v), n - 1).denominator <= 4:
                break
        q = t.format(n=n, v=lst(v))
        its.append(mcq_n(q, m, avg_cands(v) + fills(m), e_avg(v, word=word)))
    # decimals (3)
    f1 = lambda x: fmt_dp(x, 1)
    f2 = lambda x: fmt_dp(x, 2)
    for _ in range(20000):
        v = [F(rnd.randint(12, 26), 10) for _ in range(4)]
        m = mean(v)
        if clean(m) and m.denominator != 1 and m != median(v) and len(set(v)) == 4:
            break
    q = "The masses of 4 durians are <b>%s</b> kg. What is the average mass of a durian?" % lst(v, f1)
    its.append(mcq_n(q, m, avg_cands(v) + [m * 10] + fills(m, F(1, 10)), e_avg(v, f1, fmt(m) + " kg", "durians"),
                     show=us(" kg")))
    for _ in range(20000):
        v = [F(rnd.randint(138, 162), 100) for _ in range(4)]
        m = mean(v)
        if clean(m) and m != median(v) and len(set(v)) == 4 and (m * 10).denominator != 1:
            break
    q = "The heights of 4 pupils are <b>%s</b> m. What is their average height?" % lst(v, f2)
    its.append(mcq_n(q, m, avg_cands(v) + fills(m, F(1, 100)), e_avg(v, f2, f2(m) + " m", "pupils"),
                     show=lambda x: f2(x) + " m"))
    for _ in range(20000):
        v = [F(rnd.randint(25, 380), 10) for _ in range(5)]
        m = mean(v)
        if clean(m) and m.denominator != 1 and m != median(v) and len(set(v)) == 5:
            break
    q = "A school weather station recorded <b>%s</b> mm of rain on 5 days. What was the average daily rainfall?" % lst(v, f1)
    its.append(mcq_n(q, m, avg_cands(v) + fills(m, F(1, 10)), e_avg(v, f1, fmt(m) + " mm", "days"), show=us(" mm")))
    # money (3)
    name, pro, pos = P.next()
    for _ in range(20000):
        v = [F(10 * rnd.randint(18, 35), 100) for _ in range(5)]
        m = mean(v)
        if clean(m) and m != median(v) and len(set(v)) == 5 and m.denominator != 1:
            break
    q = ("%s spent <b>%s</b> at the school canteen on 5 school days. What was the average amount %s spent per day?"
         % (name, lst(v, money), pro))
    its.append(mcq_n(q, m, avg_cands(v) + fills(m, F(1, 10)), e_avg(v, money, money(m), "days"), show=money))
    for _ in range(20000):
        v = [F(10 * rnd.randint(89, 165), 100) for _ in range(4)]
        m = mean(v)
        if clean(m) and m != median(v) and len(set(v)) == 4:
            break
    q = "At a book fair, 4 storybooks cost <b>%s</b>. What was the average price of a storybook?" % lst(v, money)
    its.append(mcq_n(q, m, avg_cands(v) + fills(m, F(1, 10)), e_avg(v, money, money(m), "books"), show=money))
    name, pro, pos = P.next()
    for _ in range(20000):
        v = [rnd.choice([2, 4, 6, 8, 10, 12, 20]) for _ in range(5)]
        m = mean(v)
        if m.denominator != 1 and clean(m) and m != median(v) and len(set(v)) >= 4:
            break
    q = ("During Chinese New Year, %s received 5 red packets with <b>%s</b>. What was the average amount in a red packet?"
         % (name, lst(v, dollars)))
    its.append(mcq_n(q, m, avg_cands(v) + fills(m, F(1, 10)), e_avg(v, dollars, money(m), "red packets"), show=money))
    # large numbers (2)
    for _ in range(20000):
        v = [rnd.randint(7800, 13600) for _ in range(4)]
        m = mean(v)
        if m.denominator == 1 and m != median(v) and sum(1 for x in v if x >= 10000) == 2:
            break
    q = "Mr Tan walked <b>%s</b> steps on 4 days. What was the average number of steps he walked per day?" % lst(v)
    its.append(mcq_n(q, m, avg_cands(v) + fills(m, 10), e_avg(v, word="days")))
    for _ in range(20000):
        v = [rnd.randint(1150, 1480) for _ in range(3)]
        m = mean(v)
        if m.denominator == 1 and m != median(v):
            break
    q = ("A school concert was held on 3 nights. The audience on the 3 nights was <b>%s</b> people. What was the "
         "average audience per night?" % lst(v))
    its.append(mcq_n(q, m, avg_cands(v) + fills(m, 10), e_avg(v, word="nights")))
    # compound units (2)
    for _ in range(20000):
        v = [5 * rnd.randint(150, 340) for _ in range(3)]
        m = mean(v)
        if m.denominator == 1 and m % 5 == 0 and m != median(v) and sum(1 for x in v if x < 1000) == 1:
            break
    q = "Three parcels have masses of <b>%s</b>. What is the average mass of a parcel?" % lst(v, kg)
    e = ("Change to grams: %s = %s g. Average = %s g ÷ 3 = %s g = <b>%s</b>."
         % (" + ".join("%d" % x for x in v), fmt(sum(v)), fmt(sum(v)), fmt(m), kg(m)))
    its.append(mcq_n(q, m, [x for x in avg_cands(v) if F(x).denominator == 1] + fills(m, 50), e, show=kg, dp=0))
    for _ in range(20000):
        v = [50 * rnd.randint(14, 34) for _ in range(4)]
        m = mean(v)
        if m.denominator == 1 and m % 50 == 0 and m != median(v) and len(set(v)) == 4 and m % 1000 and \
                sum(1 for x in v if x < 1000) in (1, 2):
            break
    q = "Four bottles hold <b>%s</b> of water. What is the average volume of water in a bottle?" % lst(v, litre)
    e = ("Change to millilitres: %s = %s ml. Average = %s ml ÷ 4 = %s ml = <b>%s</b>."
         % (" + ".join("%d" % x for x in v), fmt(sum(v)), fmt(sum(v)), fmt(m), litre(m)))
    its.append(mcq_n(q, m, [x for x in avg_cands(v) if F(x).denominator == 1] + fills(m, 50), e, show=litre, dp=0))
    # bar graph (2)
    for _ in range(20000):
        v = [rnd.randint(0, 6) for _ in range(5)]
        m = mean(v)
        if v.count(0) == 1 and m.denominator == 1 and m != median(v) and max(v) >= 4:
            break
    svg = bar_svg("Pupils absent from Class 6B", "Day", "Pupils", DAYS5, v, 1, label="bar graph: pupils absent")
    q = fig(svg) + "The bar graph shows the number of pupils absent from Class 6B each day. What was the average number of pupils absent per day?"
    its.append(mcq_n(q, m, avg_cands(v) + fills(m), e_avg(v, word="days")))
    for _ in range(20000):
        v = [10 * rnd.randint(3, 9) for _ in range(5)]
        m = mean(v)
        if m.denominator == 1 and m % 10 and m != median(v) and len(set(v)) >= 4:
            break
    svg = bar_svg("Cups of bubble tea sold", "Day", "Cups", DAYS5, v, 10, label="bar graph: cups of bubble tea sold")
    q = fig(svg) + "The bar graph shows the number of cups of bubble tea a shop sold from Monday to Friday. What was the average number of cups sold per day?"
    its.append(mcq_n(q, m, avg_cands(v) + fills(m), e_avg(v, word="days")))
    # tables (2)
    for _ in range(20000):
        v = [F(rnd.randint(380, 560), 10) for _ in range(4)]
        m = mean(v)
        if clean(m) and m.denominator != 1 and m != median(v) and len(set(v)) == 4:
            break
    cats = ["Ali", "Mei Ling", "Raju", "Siti"]
    svg = table_svg("Time to swim 50 m", ["Pupil"] + cats, [["Time (s)"] + [f1(x) for x in v]], label="table: time to swim 50 m")
    q = fig(svg) + "What was the average time taken by the 4 pupils?"
    its.append(mcq_n(q, m, avg_cands(v) + fills(m, F(1, 10)), e_avg(v, f1, fmt(m) + " s", "pupils"), show=us(" s")))
    for _ in range(20000):
        v = [F(5 * rnd.randint(16, 60), 1) for _ in range(4)]
        m = mean(v)
        if clean(m) and m.denominator != 1 and m != median(v) and len(set(v)) == 4:
            break
    svg = table_svg("Money raised for charity", ["Class"] + ["6A", "6B", "6C", "6D"], [["Amount"] + [dollars(x) for x in v]],
                    label="table: money raised for charity")
    q = fig(svg) + "What was the average amount of money raised by a class?"
    its.append(mcq_n(q, m, avg_cands(v) + fills(m, F(1, 4)), e_avg(v, dollars, money(m), "classes"), show=money))
    assert len(its) == 20
    order = [0, 1, 4, 2, 14, 5, 3, 6, 15, 9, 7, 10, 16, 12, 8, 11, 17, 13, 18, 19]
    assert sorted(order) == list(range(20))
    return {"title": "Find the average", "items": [its[i] for i in order]}


# ============================================================ set 2: find the total from the average
def e_tot(m, n, ans, word="data"):
    return ("Total value = average × number of %s = %s × %d = <b>%s</b>." % (word, m, n, ans))


def set_total(rnd, P):
    its = []
    # numbers (6)
    plans = [(3, 1), (4, 1), (5, 1), (6, 1), (4, 10), (8, 10)]
    used = set()
    for n, d in plans:
        for _ in range(5000):
            m = F(rnd.randint(120, 480), 10) if d == 10 else F(rnd.randint(14, 96))
            if (d == 10 and m.denominator == 1) or m in used:
                continue
            break
        used.add(m)
        q = "The average of %s numbers is %s. What is the total of the %s numbers?" % (WORDN[n], fmt(m), WORDN[n])
        ans = n * m
        its.append(mcq_n(q, ans, [m / n if clean(m / n) else None, m + n, (n - 1) * m, (n + 1) * m]
                         + fills(ans, F(1, d)), e_tot(fmt(m), n, fmt(ans), "numbers")))
    # measures (4)
    MEAS = [("The average mass of {n} bags of rice is {m} kg. What is the total mass of the bags?", " kg", 8, 245, 520, 100, "bags"),
            ("The average length of {n} ribbons is {m} cm. What is the total length of the ribbons?", " cm", 6, 125, 480, 10, "ribbons"),
            ("The average height of {n} pupils in a relay team is {m} m. What is their total height?", " m", 4, 138, 159, 100, "pupils"),
            ("The average distance {name} jogged each day for {n} days at East Coast Park was {m} km. How far did {pro} jog altogether?", " km", 7, 24, 58, 10, "days")]
    for t, u, n, lo, hi, d, word in MEAS:
        for _ in range(5000):
            m = F(rnd.randint(lo, hi), d)
            if m.denominator == d:
                break
        name, pro, pos = P.next()
        shw = (lambda x: fmt_dp(x, 2)) if d == 100 else fmt
        q = t.format(n=n, m=shw(m), name=name, pro=pro)
        ans = n * m
        its.append(mcq_n(q, ans, [m / n if clean(m / n) else None, m + n, (n - 1) * m, (n + 1) * m] + fills(ans, F(1, d)),
                         e_tot(shw(m) + u, n, fmt(ans) + u, word), show=us(u)))
    # money (3)
    MON = [("{name} saved an average of {m} a week for {n} weeks. How much did {pro} save altogether?", 12, (250, 650), 5, "weeks"),
           ("The average price of {n} T-shirts is {m}. What is the total price of the T-shirts?", 4, (1290, 2490), 10, "T-shirts"),
           ("A stall sold {n} bowls of laksa. The average amount collected per bowl was {m}. How much money did the stall collect?", 25, (450, 650), 10, "bowls")]
    for t, n, (lo, hi), step, word in MON:
        for _ in range(5000):
            m = F(step * rnd.randint(lo // step, hi // step), 100)
            if m.denominator != 1:
                break
        name, pro, pos = P.next()
        q = t.format(n=n, m=money(m), name=name, pro=pro)
        ans = n * m
        its.append(mcq_n(q, ans, [m / n if clean(m / n) else None, m + n, (n - 1) * m, (n + 1) * m] + fills(ans, F(1, 10)),
                         e_tot(money(m), n, money(ans), word), show=money))
    # time in h and min (2)
    for n, lo, hi, what in [(7, 35, 55, "practising the piano"), (5, 50, 75, "reading")]:
        for _ in range(5000):
            m = 5 * rnd.randint(lo // 5, hi // 5)
            T = n * m
            if T % 60 and (T // 60) * 100 + T % 60 != T and T % 60 >= 10:
                break
        name, pro, pos = P.next()
        days = "a week" if n == 7 else "5 days"
        q = ("%s spent an average of %d min a day %s for %s. How much time did %s spend altogether? Give your answer in "
             "hours and minutes." % (name, m, what, days, pro))
        h, mi = divmod(T, 60)
        e = "Total = %d min × %d = %d min. %d min = %d × 60 min + %d min = <b>%s</b>." % (m, n, T, T, h, mi, hmin(T))
        wrong100 = T // 100 * 60 + T % 100  # 315 min read as 3 h 15 min
        its.append(mcq_n(q, T, [wrong100 if T % 100 < 60 else None, (n - 1) * m, (n + 1) * m, T + 60, T - 60], e,
                         show=hmin, dp=0))
    # volume (1)
    name, pro, pos = P.next()
    m = 25 * rnd.randint(11, 15)
    n = 6
    T = n * m
    q = "The average amount of water in %d cups is %d ml. How much water is there altogether?" % (n, m)
    e = "Total = %d ml × %d = %d ml = <b>%s</b>." % (m, n, T, litre(T))
    its.append(mcq_n(q, T, [(n - 1) * m, (n + 1) * m, T + 100, T - 100]
                     + fills(T, 50), e, show=litre, dp=0))
    # number of data (4)
    NUM = [("{name}’s total score in some tests was {T} marks. {Pos} average score was {m} marks. How many tests did {pro} take?", "tests"),
           ("A group of friends saved $ {T} altogether. The average amount each friend saved was $ {m}. How many friends were there?", "friends"),
           ("Some boxes have a total mass of {T} kg. The average mass of a box is {m} kg. How many boxes are there?", "boxes"),
           ("A class collected {T} cans for recycling. On average, each pupil collected {m} cans. How many pupils are in the class?", "pupils")]
    for k, (t, word) in enumerate(NUM):
        for _ in range(5000):
            n = [5, 6, 8, 32][k]
            m = [rnd.randint(62, 92), rnd.randint(14, 48), F(rnd.randint(25, 95), 10), rnd.randint(4, 9)][k]
            T = n * m
            if F(T).denominator == 1 or k == 2:
                if clean(T):
                    break
        name, pro, pos = P.next()
        q = t.format(T=fmt(T), m=fmt(m), name=name, pro=pro, Pos=pos.capitalize()).replace("$ ", "$")
        e = "Number of %s = total ÷ average = %s ÷ %s = <b>%d</b>." % (word, fmt(T), fmt(m), n)
        its.append(mcq_n(q, n, [n - 1, n + 1, n + 2, n - 2, F(T) - m if F(T) - m < 1000 else None], e))
    assert len(its) == 20
    order = [0, 1, 2, 3, 6, 4, 10, 7, 14, 5, 11, 15, 8, 12, 16, 18, 9, 13, 17, 19]
    assert sorted(order) == list(range(20))
    return {"title": "Find the total from the average", "items": [its[i] for i in order]}


# ============================================================ set 3: find a missing value
def set_missing(rnd, P):
    its = []
    # missing number (6)
    for k in range(6):
        n = [3, 4, 4, 5, 5, 6][k]
        for _ in range(5000):
            m = rnd.randint(12, 40) if k < 4 else rnd.randint(40, 90)
            known = [rnd.randint(max(1, m - 12), m + 12) for _ in range(n - 1)]
            ans = n * m - sum(known)
            if ans >= 1 and ans not in known and abs(ans - m) >= 3 and (n - 1) * m - sum(known) > 0 \
                    and len(set(known)) == n - 1:
                break
        q = ("The average of %s numbers is %d. %s of the numbers are <b>%s</b>. What is the missing number?"
             % (WORDN[n], m, WORDN[n - 1].capitalize(), lst(known)))
        e = ("Total of all %d numbers = %d × %d = %d. The %d numbers given add up to %s = %d. Missing number = %d − %d = <b>%d</b>."
             % (n, m, n, n * m, n - 1, plus(known), sum(known), n * m, sum(known), ans))
        its.append(mcq_n(q, ans, [(n - 1) * m - sum(known), m, n * m, F(sum(known), n - 1)]
                         + fills(ans), e))
    # missing test mark (3)
    for k in range(3):
        name, pro, pos = P.next()
        n = [3, 4, 5][k]
        for _ in range(5000):
            m = rnd.randint(68, 86)
            known = [rnd.randint(60, 98) for _ in range(n - 1)]
            ans = n * m - sum(known)
            if 55 <= ans <= 100 and ans not in known and abs(ans - m) >= 4 and len(set(known)) == n - 1:
                break
        q = ("%s average mark for %d tests was %d. %s marks for %d of the tests were <b>%s</b>. What was %s mark for the "
             "other test?" % (poss(name), n, m, pos.capitalize(), n - 1, lst(known), pos))
        e = ("Total for %d tests = %d × %d = %d. Known marks: %s = %d. Other test = %d − %d = <b>%d</b>."
             % (n, m, n, n * m, plus(known), sum(known), n * m, sum(known), ans))
        its.append(mcq_n(q, ans, [(n - 1) * m - sum(known) if (n - 1) * m > sum(known) else None, m,
                                  2 * m - mean(known) if clean(2 * m - mean(known)) and (2 * m - mean(known)).denominator == 1 else None,
                                  n * m] + fills(ans), e))
    # mark needed in the next test (3)
    for k in range(3):
        name, pro, pos = P.next()
        n = [3, 4, 4][k]
        for _ in range(5000):
            known = [rnd.randint(64, 92) for _ in range(n)]
            T = rnd.randint(int(mean(known)) + 2, int(mean(known)) + 6)
            ans = (n + 1) * T - sum(known)
            if ans <= 100 and len(set(known)) == n and (2 * T - mean(known)).denominator == 1 and 2 * T - mean(known) != ans:
                break
        q = ("%s marks for %d Science tests were <b>%s</b>. What mark must %s get in the next test so that %s average "
             "mark for all %d tests is %d?" % (poss(name), n, lst(known), pro, pos, n + 1, T))
        e = ("Total needed for %d tests = %d × %d = %d. Total so far = %s = %d. Mark needed = %d − %d = <b>%d</b>."
             % (n + 1, n + 1, T, (n + 1) * T, plus(known), sum(known), (n + 1) * T, sum(known), ans))
        its.append(mcq_n(q, ans, [2 * T - mean(known), T, n * T - sum(known) if n * T > sum(known) else None,
                                  (n + 1) * T] + fills(ans), e))
    # missing bar (2)
    for title, axis, cats, sc, lo, hi, unit, per in [
            ("Books borrowed", "Books", DAYS5, 5, 4, 9, "books", "day"),
            ("Rainfall in 5 months", "Rainfall (mm)", ["Jan", "Feb", "Mar", "Apr", "May"], 50, 2, 6, "mm", "month")]:
        n = len(cats)
        for _ in range(50000):
            v = [sc * rnd.randint(lo, hi) for _ in range(n)]
            mi = rnd.randrange(1, n)
            m = mean(v)
            if m.denominator == 1 and m not in v and len(set(v)) >= 4:
                break
        others = [x for i, x in enumerate(v) if i != mi]
        ans = v[mi]
        full = {"Jan": "January", "Feb": "February", "Mar": "March", "Apr": "April", "May": "May", "Jul": "July", "Aug": "August", "Sep": "September", "Oct": "October", "Nov": "November",
                "Mon": "Monday", "Tue": "Tuesday", "Wed": "Wednesday", "Thu": "Thursday", "Fri": "Friday"}[cats[mi]]
        svg = bar_svg(title, "Day" if per == "day" else "Month", axis, cats, v, sc, missing=mi, label="bar graph: " + title.lower())
        uu = " mm" if unit == "mm" else ""
        if unit == "mm":
            q = fig(svg) + "The bar for %s is missing. The average rainfall for the 5 months was %s mm. What was the rainfall in %s?" % (full, fmt(m), full)
        else:
            q = fig(svg) + "The bar for %s is missing. The average number of books borrowed per day was %s. How many books were borrowed on %s?" % (full, fmt(m), full)
        e = ("Total = %s × %d = %s. The other bars add up to %s = %s. %s: %s − %s = <b>%s</b>."
             % (fmt(m), n, fmt(n * m), plus(others), fmt(sum(others)), full, fmt(n * m), fmt(sum(others)), fmt(ans) + uu))
        its.append(mcq_n(q, ans, [(n - 1) * m - sum(others) if (n - 1) * m > sum(others) else None, m, n * m,
                                  F(sum(others), n - 1)] + fills(ans, sc), e, show=us(uu)))
    # average of 3 and average of 2 (3)
    for k in range(3):
        for _ in range(5000):
            m3 = rnd.randint(20, 70)
            m2 = rnd.randint(m3 - 10, m3 + 10)
            C = 3 * m3 - 2 * m2
            if C > 0 and m2 != m3 and abs(C - m3) >= 4 and C != m3 - m2:
                break
        q = ("The average of three numbers A, B and C is %d. The average of A and B is %d. What is C?" % (m3, m2))
        e = ("A + B + C = 3 × %d = %d. A + B = 2 × %d = %d. C = %d − %d = <b>%d</b>."
             % (m3, 3 * m3, m2, 2 * m2, 3 * m3, 2 * m2, C))
        its.append(mcq_n(q, C, [abs(m3 - m2), m3 + m2, 3 * m3 - m2, 2 * m3 - m2, m3] + fills(C), e))
    # average of two numbers (2)
    for k in range(2):
        for _ in range(5000):
            m = rnd.randint(25, 80) if k == 0 else F(rnd.randint(105, 395), 10)
            a = rnd.randint(10, 60) if k == 0 else F(rnd.randint(40, 300), 10)
            b = 2 * m - a
            if b > 0 and b != a and abs(b - m) >= 3 and clean(b, 1):
                break
        q = "The average of two numbers is %s. One of the numbers is %s. What is the other number?" % (fmt(m), fmt(a))
        e = "Total = 2 × %s = %s. Other number = %s − %s = <b>%s</b>." % (fmt(m), fmt(2 * m), fmt(2 * m), fmt(a), fmt(b))
        its.append(mcq_n(q, b, [abs(m - a), m, 2 * m, m + a] + fills(b, 1 if k == 0 else F(1, 10)), e, dp=1))
    # average of the other numbers (1)
    for _ in range(5000):
        m5, m3 = rnd.randint(30, 60), rnd.randint(25, 65)
        r = F(5 * m5 - 3 * m3, 2)
        if r.denominator == 1 and r > 0 and abs(r - m5) >= 3 and m3 != m5:
            break
    q = ("The average of 5 numbers is %d. The average of the first 3 numbers is %d. What is the average of the last 2 "
         "numbers?" % (m5, m3))
    e = ("Total of 5 numbers = 5 × %d = %d. Total of first 3 = 3 × %d = %d. Last 2 add up to %d − %d = %d. Average = "
         "%d ÷ 2 = <b>%s</b>." % (m5, 5 * m5, m3, 3 * m3, 5 * m5, 3 * m3, 2 * r, 2 * r, fmt(r)))
    its.append(mcq_n(q, r, [2 * r, abs(m5 - m3), m5 + m3, F(m5 + m3, 2) if F(m5 + m3, 2) != r else None, 2 * m5 - m3] + fills(r), e))
    assert len(its) == 20
    order = [0, 1, 17, 2, 6, 3, 9, 12, 4, 18, 7, 14, 10, 5, 13, 8, 15, 11, 16, 19]
    assert sorted(order) == list(range(20))
    return {"title": "Find a missing value", "items": [its[i] for i in order]}


# ============================================================ set 4: a value is added or removed
def set_change(rnd, P):
    its = []
    # add a value: new average (5)
    for k in range(5):
        for _ in range(5000):
            n = [3, 4, 4, 5, 6][k]
            m = rnd.randint(10, 40)
            x = rnd.randint(5, 70)
            nm = F(n * m + x, n + 1)
            if nm.denominator == 1 and abs(x - m) >= 5 and F(m + x, 2) != nm and nm != m and clean(F(n * m + x, n)):
                break
        q = ("The average of %s numbers is %d. The number %d is added to the group. What is the average of the %s "
             "numbers now?" % (WORDN[n], m, x, WORDN[n + 1]))
        e = ("Old total = %d × %d = %d. New total = %d + %d = %d. New average = %d ÷ %d = <b>%s</b>."
             % (m, n, n * m, n * m, x, n * m + x, n * m + x, n + 1, fmt(nm)))
        its.append(mcq_n(q, nm, [m + x, F(m + x, 2), F(n * m + x, n), n * m + x] + fills(nm), e))
    # remove a value (4)
    for k in range(4):
        for _ in range(5000):
            n = [4, 5, 5, 6][k]
            m = rnd.randint(15, 45)
            x = rnd.randint(4, 80)
            nm = F(n * m - x, n - 1)
            if nm.denominator == 1 and nm > 0 and abs(x - m) >= 5 and F(n * m - x, n) != nm and clean(F(n * m - x, n)):
                break
        q = ("The average of %s numbers is %d. The number %d is removed. What is the average of the remaining %s numbers?"
             % (WORDN[n], m, x, WORDN[n - 1]))
        e = ("Old total = %d × %d = %d. New total = %d − %d = %d. New average = %d ÷ %d = <b>%s</b>."
             % (m, n, n * m, n * m, x, n * m - x, n * m - x, n - 1, fmt(nm)))
        its.append(mcq_n(q, nm, [abs(m - x), F(n * m - x, n), m, n * m - x, F(m + x, 2)] + fills(nm), e))
    # find the value added (4)
    for k in range(4):
        for _ in range(5000):
            n = [4, 5, 6, 7][k]
            m1 = rnd.randint(15, 50)
            m2 = m1 + rnd.choice([-4, -3, -2, 2, 3, 4, 5])
            x = (n + 1) * m2 - n * m1
            if x > 0 and x != m2 and abs(x - m2) >= 4:
                break
        q = ("The average of %s numbers is %d. When one more number is added, the average becomes %d. What is the "
             "number that was added?" % (WORDN[n], m1, m2))
        e = ("Old total = %d × %d = %d. New total = %d × %d = %d. Number added = %d − %d = <b>%d</b>."
             % (n, m1, n * m1, n + 1, m2, (n + 1) * m2, (n + 1) * m2, n * m1, x))
        its.append(mcq_n(q, x, [abs(m2 - m1), m2, n * (m2 - m1) if m2 > m1 else None, m1 + m2, (n + 1) * m2]
                         + fills(x), e))
    # find the value removed (3)
    for k in range(3):
        for _ in range(5000):
            n = [5, 6, 8][k]
            m1 = rnd.randint(20, 60)
            m2 = m1 + rnd.choice([-3, -2, 2, 3, 4])
            x = n * m1 - (n - 1) * m2
            if x > 0 and x != m1 and abs(x - m1) >= 4:
                break
        q = ("The average of %s numbers is %d. When one number is removed, the average of the remaining numbers is %d. "
             "What number was removed?" % (WORDN[n], m1, m2))
        e = ("Old total = %d × %d = %d. New total = %d × %d = %d. Number removed = %d − %d = <b>%d</b>."
             % (n, m1, n * m1, n - 1, m2, (n - 1) * m2, n * m1, (n - 1) * m2, x))
        its.append(mcq_n(q, x, [abs(m1 - m2), m1, n * m1 - n * m2 if n * m1 > n * m2 else None, m1 + m2] + fills(x), e))
    # average increases by k when a value is added (2)
    for k in range(2):
        for _ in range(5000):
            n = [4, 5][k]
            m = rnd.randint(12, 30)
            inc = rnd.choice([2, 3, 4])
            x = (n + 1) * (m + inc) - n * m
            if x <= 99:
                break
        q = ("The average of %s numbers is %d. When one more number is added, the average increases by %d. What is the "
             "number that was added?" % (WORDN[n], m, inc))
        e = ("New average = %d + %d = %d. New total = %d × %d = %d. Old total = %d × %d = %d. Number added = %d − %d = "
             "<b>%d</b>." % (m, inc, m + inc, n + 1, m + inc, (n + 1) * (m + inc), n, m, n * m, (n + 1) * (m + inc), n * m, x))
        its.append(mcq_n(q, x, [m + inc, m + n * inc, inc * (n + 1), m + inc * 2] + fills(x), e))
    # a value is corrected (2)
    for k in range(2):
        name, pro, pos = P.next()
        for _ in range(5000):
            n = [4, 5][k]
            m = rnd.randint(13, 16)
            wrong = rnd.randint(6, 12)
            right = wrong + n * rnd.randint(1, 2)
            nm = m + F(right - wrong, n)
            if right <= 20 and nm <= 18:
                break
        q = ("%s average score for %d spelling tests was %d. Each test was out of 20. Later, %s teacher found that one "
             "score of %d should be %d. What is the correct average score?" % (poss(name), n, m, pos, wrong, right))
        e = ("The total increases by %d − %d = %d. Shared among %d tests, the average increases by %d ÷ %d = %d. "
             "Correct average = %d + %d = <b>%s</b>." % (right, wrong, right - wrong, n, right - wrong, n,
                                                      (right - wrong) // n, m, (right - wrong) // n, fmt(nm)))
        its.append(mcq_n(q, nm, [m + right - wrong, F(m + right, 2), m + 1 if nm != m + 1 else m + 3, right] + fills(nm), e))
    assert len(its) == 20
    order = [0, 5, 1, 6, 2, 9, 7, 3, 10, 13, 8, 4, 11, 14, 12, 15, 18, 16, 17, 19]
    assert sorted(order) == list(range(20))
    return {"title": "When a value is added or removed", "items": [its[i] for i in order]}


# ============================================================ set 5: PSLE-style word problems
def set_words(rnd, P):
    its = []
    nm = P.next

    # 1. four subjects
    name, pro, pos = nm()
    a3, mt = 82, 90
    ans = F(3 * a3 + mt, 4)
    assert ans.denominator == 1
    q = ("%s average mark for English, Maths and Science was %d. %s mark for Mother Tongue was %d. What was %s average "
         "mark for the 4 subjects?" % (poss(name), a3, pos.capitalize(), mt, pos))
    e = ("Total for 3 subjects = 3 × %d = %d. Total for 4 subjects = %d + %d = %d. Average = %d ÷ 4 = <b>%s</b>."
         % (a3, 3 * a3, 3 * a3, mt, 3 * a3 + mt, 3 * a3 + mt, fmt(ans)))
    its.append(mcq_n(q, ans, [F(a3 + mt, 2), F(3 * a3 + mt, 3), a3 + 1, F(a3 + mt, 4)], e))

    # 2. hawker week
    wk, we = 85, 120
    ans = F(5 * wk + 2 * we, 7)
    assert ans.denominator == 1
    q = ("A hawker sold an average of %d plates of chicken rice a day from Monday to Friday. On Saturday and Sunday, "
         "he sold an average of %d plates a day. What was the average number of plates he sold per day for the whole week?"
         % (wk, we))
    e = ("Monday to Friday: 5 × %d = %d. Weekend: 2 × %d = %d. Week total = %d. Average = %d ÷ 7 = <b>%s</b>."
         % (wk, 5 * wk, we, 2 * we, 5 * wk + 2 * we, 5 * wk + 2 * we, fmt(ans)))
    its.append(mcq_n(q, ans, [F(wk + we, 2), F(5 * wk + 2 * we, 5), F(5 * wk + 2 * we, 2) if clean(F(5 * wk + 2 * we, 2)) else None,
                              wk + 10], e))

    # 3. rainfall first 4 days / last 3 days
    r4, r3 = F(126, 10), F(42, 10)
    ans = (4 * r4 + 3 * r3) / 7
    assert clean(ans)
    q = ("During one week in December, the average daily rainfall for the first 4 days was %s mm. The average daily "
         "rainfall for the last 3 days was %s mm. What was the average daily rainfall for the whole week?" % (fmt(r4), fmt(r3)))
    e = ("First 4 days: 4 × %s = %s mm. Last 3 days: 3 × %s = %s mm. Total = %s mm. Average = %s ÷ 7 = <b>%s mm</b>."
         % (fmt(r4), fmt(4 * r4), fmt(r3), fmt(3 * r3), fmt(4 * r4 + 3 * r3), fmt(4 * r4 + 3 * r3), fmt(ans)))
    its.append(mcq_n(q, ans, [(r4 + r3) / 2, r4 + r3, (4 * r4 + 3 * r3) / 2] + fills(ans, F(1, 10)), e, show=us(" mm")))

    # 4. grandmother joins, average age increases by 10
    n, m, inc = 4, 22, 10
    g = (n + 1) * (m + inc) - n * m
    q = ("The average age of a family of 4 is %d years. When their grandmother joins them, the average age of the 5 "
         "people increases by %d years. How old is their grandmother?" % (m, inc))
    e = ("Before: 4 × %d = %d years. After: the average is %d + %d = %d, so the total is 5 × %d = %d years. "
         "Grandmother = %d − %d = <b>%d years</b>." % (m, n * m, m, inc, m + inc, m + inc, 5 * (m + inc), 5 * (m + inc), n * m, g))
    its.append(mcq_n(q, g, [m + inc, m + n * inc, 5 * (m + inc), (m + inc) * 2] + fills(g), e, show=us(" years")))

    # 5. coach joins, average age increases by 2
    n, m, inc = 5, 11, 2
    c = (n + 1) * (m + inc) - n * m
    q = ("The average age of 5 pupils in a CCA group is %d years. A coach joins the group, and the average age "
         "increases by %d years. How old is the coach?" % (m, inc))
    e = ("Total age of 5 pupils = 5 × %d = %d. New total = 6 × %d = %d. Coach = %d − %d = <b>%d years</b>. "
         "(The coach is %d years older than the new average, enough to add %d years to each of the 5 pupils.)"
         % (m, n * m, m + inc, 6 * (m + inc), 6 * (m + inc), n * m, c, n * inc, inc))
    its.append(mcq_n(q, c, [m + inc, m + n * inc, inc * 6, 6 * (m + inc)] + fills(c), e, show=us(" years")))

    # 6. ages in 4 years
    n, m, yrs = 3, 9, 4
    q = ("The average age of 3 brothers is %d years now. What will their average age be in %d years’ time?" % (m, yrs))
    e = ("Each brother will be %d years older, so the average also goes up by %d: %d + %d = <b>%d years</b>. "
         "(Total now = 27; total then = 27 + 3 × %d = %d; %d ÷ 3 = %d.)" % (yrs, yrs, m, yrs, m + yrs, yrs, 27 + 3 * yrs, 27 + 3 * yrs, m + yrs))
    its.append(mcq_n(q, m + yrs, [m + 3 * yrs, F(3 * m + yrs, 3) if clean(F(3 * m + yrs, 3)) else None, m, 3 * m + 3 * yrs,
                                  m + yrs + 1], e, show=us(" years")))

    # 7. combined class average mass
    nb, mb, ng, mg = 12, 42, 18, 38
    ans = F(nb * mb + ng * mg, nb + ng)
    assert clean(ans, 1)
    q = ("In a class, the average mass of the %d boys is %d kg and the average mass of the %d girls is %d kg. "
         "What is the average mass of all the pupils in the class?" % (nb, mb, ng, mg))
    e = ("Boys: %d × %d = %d kg. Girls: %d × %d = %d kg. Total = %d kg for %d pupils. Average = %d ÷ %d = <b>%s kg</b>. "
         "(Not (42 + 38) ÷ 2, because the groups are different sizes.)"
         % (nb, mb, nb * mb, ng, mg, ng * mg, nb * mb + ng * mg, nb + ng, nb * mb + ng * mg, nb + ng, fmt(ans)))
    its.append(mcq_n(q, ans, [F(mb + mg, 2), F(nb * mg + ng * mb, nb + ng), mb + mg, F(39)] + fills(ans, F(1, 10)), e,
                     show=us(" kg")))

    # 8. average of the girls
    N, M, nb, mb = 20, 40, 8, 43
    ng = N - nb
    ans = F(N * M - nb * mb, ng)
    assert ans.denominator == 1
    q = ("The average mass of %d pupils is %d kg. The average mass of the %d boys among them is %d kg. What is the "
         "average mass of the girls?" % (N, M, nb, mb))
    e = ("All: %d × %d = %d kg. Boys: %d × %d = %d kg. Girls: %d − %d = %d kg for %d girls. Average = %d ÷ %d = <b>%s kg</b>."
         % (N, M, N * M, nb, mb, nb * mb, N * M, nb * mb, N * M - nb * mb, ng, N * M - nb * mb, ng, fmt(ans)))
    its.append(mcq_n(q, ans, [2 * M - mb, F(N * M - nb * mb, N), M - (mb - M) * 2, F(M + mb, 2)] + fills(ans), e,
                     show=us(" kg")))

    # 9. player leaves (before and after)
    h5, h4 = F(162, 100), F(160, 100)
    ans = 5 * h5 - 4 * h4
    f2 = lambda x: fmt_dp(x, 2) + " m"
    q = ("The average height of 5 basketball players is %s m. One player leaves the team. The average height of the "
         "other 4 players is %s m. What is the height of the player who left?" % (fmt_dp(h5, 2), fmt_dp(h4, 2)))
    e = ("Before: 5 × %s = %s m. After: 4 × %s = %s m. Player who left = %s − %s = <b>%s</b>."
         % (fmt_dp(h5, 2), fmt_dp(5 * h5, 2), fmt_dp(h4, 2), fmt_dp(4 * h4, 2), fmt_dp(5 * h5, 2), fmt_dp(4 * h4, 2), f2(ans)))
    its.append(mcq_n(q, ans, [h5 + (h5 - h4), (h5 + h4) / 2, h5, h5 + 5 * (h5 - h4)], e, show=f2))

    # 10. units: A twice B, C three times B (model)
    avg, n = 60, 3
    T = avg * n
    u = F(T, 6)
    assert u.denominator == 1
    px = 7
    rows = [("A", [(u, "1 u", "u")] * 2, ""), ("B", [(u, "1 u", "u")], ""), ("C", [(u, "1 u", "u")] * 3, "?")]
    svg = model_svg(rows, F(50, u), total=fmt(T), label="bar model: A, B and C")
    q = (fig(svg) + "The average of three numbers A, B and C is %d. A is twice as big as B. C is 3 times as big as B. "
         "What is C?" % avg)
    e = ("Total = 3 × %d = %d. A + B + C = 2 units + 1 unit + 3 units = 6 units. 6 units = %d, so 1 unit = %d. "
         "C = 3 units = <b>%d</b>." % (avg, T, T, u, 3 * u))
    its.append(mcq_n(q, 3 * u, [u, 2 * u, T, avg] + fills(3 * u, 10), e))

    # 11. average of two numbers, one is 18 more (model)
    avg, d = 45, 18
    small = F(2 * avg - d, 2)
    big = small + d
    rows = [("Smaller", [(small, "1 u", "u")], ""), ("Bigger", [(small, "1 u", "u"), (d, str(d), "x")], "?")]
    svg = model_svg(rows, F(3), total=str(2 * avg), label="bar model: two numbers")
    q = (fig(svg) + "The average of two numbers is %d. One number is %d more than the other. What is the bigger number?"
         % (avg, d))
    e = ("Total = 2 × %d = %d. 2 units = %d − %d = %d, so 1 unit = %s. Bigger number = %s + %d = <b>%s</b>."
         % (avg, 2 * avg, 2 * avg, d, 2 * avg - d, fmt(small), fmt(small), d, fmt(big)))
    its.append(mcq_n(q, big, [small, avg + d, 2 * avg - d] + fills(big), e))

    # 12. Mr Tan 3 times as old as his son (model)
    avg = 26
    T = 2 * avg
    u = F(T, 4)
    rows = [("Son", [(u, "1 u", "u")], ""), ("Mr Tan", [(u, "1 u", "u")] * 3, "?")]
    svg = model_svg(rows, F(3), total="%d years" % T, label="bar model: Mr Tan and his son")
    q = (fig(svg) + "Mr Tan is 3 times as old as his son. Their average age is %d years. How old is Mr Tan?" % avg)
    e = ("Total age = 2 × %d = %d years. 4 units = %d, so 1 unit = %s. Mr Tan = 3 units = <b>%s years</b>."
         % (avg, T, T, fmt(u), fmt(3 * u)))
    its.append(mcq_n(q, 3 * u, [u, 3 * avg, T] + fills(3 * u), e,
                     show=us(" years")))

    # 13. savings with units and parts (model)
    name1, _, _ = nm()
    name2, _, _ = nm()
    name3, _, _ = nm()
    avg = 51
    T = 3 * avg
    extra = 13
    # name2: u, name1: u + 13, name3: 2u -> 4u + 13 = 153 -> u = 35
    u = F(T - extra, 4)
    assert u.denominator == 1
    rows = [(name1, [(u, "1 u", "u"), (extra, "$%d" % extra, "x")], ""), (name2, [(u, "1 u", "u")], "?"),
            (name3, [(u, "1 u", "u"), (u, "1 u", "u")], "")]
    svg = model_svg(rows, F(5, 2), total="$%d" % T, label="bar model: money saved")
    q = (fig(svg) + "%s, %s and %s saved an average of $%d. %s saved $%d more than %s. %s saved twice as much as %s. "
         "How much did %s save?" % (name1, name2, name3, avg, name1, extra, name2, name3, name2, name2))
    e = ("Total = 3 × $%d = $%d. 4 units + $%d = $%d, so 4 units = $%d and 1 unit = $%s. %s saved <b>$%s</b>."
         % (avg, T, extra, T, T - extra, fmt(u), name2, fmt(u)))
    its.append(mcq_n(q, u, [F(T, 4), u + extra, 2 * u, avg - extra, F(T + extra, 4)], e, show=dollars))

    # 14. class mark corrected
    N, M, wrong, right = 40, 68, 54, 94
    ans = M + F(right - wrong, N)
    q = ("The average Maths mark of a class of %d pupils was %d. Later, the teacher found that one pupil’s mark of %d "
         "should have been %d. What is the correct average mark of the class?" % (N, M, wrong, right))
    e = ("The total increases by %d − %d = %d. Shared among %d pupils, the average increases by %d ÷ %d = %s. "
         "Correct average = %d + %s = <b>%s</b>." % (right, wrong, right - wrong, N, right - wrong, N, fmt(F(right - wrong, N)),
                                                  M, fmt(F(right - wrong, N)), fmt(ans)))
    its.append(mcq_n(q, ans, [M + right - wrong, F(M + right, 2), F(M + wrong, 2), M + F(right - wrong, N - 1) if clean(M + F(right - wrong, N - 1)) else M + 2], e))

    # 15. two numbers removed
    n, m1, k, m2 = 8, 25, 2, 22
    r = F(n * m1 - (n - k) * m2, k)
    q = ("The average of %d numbers is %d. When 2 of the numbers are removed, the average of the remaining numbers is "
         "%d. What is the average of the 2 numbers that were removed?" % (n, m1, m2))
    e = ("Total of %d numbers = %d × %d = %d. Total of the other 6 = 6 × %d = %d. The 2 numbers add up to %d − %d = %d. "
         "Average = %d ÷ 2 = <b>%s</b>." % (n, n, m1, n * m1, m2, 6 * m2, n * m1, 6 * m2, n * m1 - 6 * m2, n * m1 - 6 * m2, fmt(r)))
    its.append(mcq_n(q, r, [n * m1 - (n - k) * m2, m1 - m2, m1 + m2, F(n * (m1 - m2), 2), m1] + fills(r), e))

    # 16. savings to reach a new average
    name, pro, pos = nm()
    a1, w, a2 = F(9, 2), 8, F(5)
    need = (w + 1) * a2 - w * a1
    q = ("%s saved an average of %s a week for %d weeks. How much must %s save in the 9th week so that %s average "
         "savings for the 9 weeks is %s?" % (name, money(a1), w, pro, pos, money(a2)))
    e = ("Total needed = 9 × %s = %s. Saved so far = %d × %s = %s. Week 9 = %s − %s = <b>%s</b>."
         % (money(a2), money(9 * a2), w, money(a1), money(w * a1), money(9 * a2), money(w * a1), money(need)))
    its.append(mcq_n(q, need, [a2 - a1, a2, 2 * a2 - a1, a2 + (a2 - a1) * 9] + fills(need, F(1, 2)), e, show=money))

    # 17. bar graph rainfall, 6th month missing
    v = [150, 250, 200, 300, 100]
    cats = ["Jul", "Aug", "Sep", "Oct", "Nov"]
    avg6 = 210
    dec = 6 * avg6 - sum(v)
    svg = bar_svg("Rainfall from July to November", "Month", "Rainfall (mm)", cats, v, 50,
                  label="bar graph: rainfall from July to November")
    q = (fig(svg) + "The bar graph shows the rainfall at a weather station from July to November. The average monthly "
         "rainfall from July to December was %d mm. What was the rainfall in December?" % avg6)
    e = ("Total for 6 months = 6 × %d = %d mm. July to November = %s = %d mm. December = %d − %d = <b>%d mm</b>."
         % (avg6, 6 * avg6, plus(v), sum(v), 6 * avg6, sum(v), dec))
    its.append(mcq_n(q, dec, [5 * avg6 - sum(v) if 5 * avg6 > sum(v) else None, avg6, mean(v), 6 * avg6 - sum(v) + 50,
                              6 * avg6] + fills(dec, 50), e, show=us(" mm")))

    # 18. consecutive even numbers
    avg = 36
    big = avg + 4
    q = "The average of 5 consecutive even numbers is %d. What is the largest of the 5 numbers?" % avg
    e = ("For numbers that go up in equal steps, the average is the middle number. The numbers are 32, 34, 36, 38 and 40. "
         "The largest is <b>%d</b>. (Check: 180 ÷ 5 = 36.)" % big)
    its.append(mcq_n(q, big, [avg + 2, avg + 5, avg + 8, avg + 3], e))

    # 19. money spent and received
    p1, p2, p3 = nm(), nm(), nm()
    avg, spent, got = 56, 18, 6
    ans = F(3 * avg - spent + got, 3)
    assert ans.denominator == 1
    q = ("%s, %s and %s had an average of $%d each. %s spent $%d and %s was given $%d. What is their new average "
         "amount of money?" % (p1[0], p2[0], p3[0], avg, p1[0], spent, p2[0], got))
    e = ("Total before = 3 × $%d = $%d. Total after = $%d − $%d + $%d = $%d. New average = $%d ÷ 3 = <b>$%s</b>."
         % (avg, 3 * avg, 3 * avg, spent, got, 3 * avg - spent + got, 3 * avg - spent + got, fmt(ans)))
    its.append(mcq_n(q, ans, [avg - spent + got, avg - spent, avg + F(got - spent, 2), avg - 1], e, show=dollars))

    # 20. new member scored more than the new average
    n, m, x = 6, 15, 22
    nmn = F(n * m + x, n + 1)
    assert nmn.denominator == 1
    q = ("In a quiz, the average score of a team of %d pupils was %d points. A 7th pupil joined the team and scored %d "
         "points. How many more points did the 7th pupil score than the new average of the team?" % (n, m, x))
    e = ("Old total = 6 × %d = %d. New total = %d + %d = %d. New average = %d ÷ 7 = %s. Difference = %d − %s = <b>%s</b>."
         % (m, n * m, n * m, x, n * m + x, n * m + x, fmt(nmn), x, fmt(nmn), fmt(x - nmn)))
    its.append(mcq_n(q, x - nmn, [x - m, nmn - m, F(x - m, 2) if clean(F(x - m, 2)) else None, x - m - 2], e))

    assert len(its) == 20
    order = [0, 1, 5, 2, 3, 10, 6, 11, 4, 8, 12, 13, 16, 9, 7, 15, 14, 17, 18, 19]
    assert sorted(order) == list(range(20))
    return {"title": "PSLE-style word problems", "items": [its[i] for i in order]}


# ============================================================ lesson
def ex(title, q, s, a):
    return ("<div class='sn-ex'><span class='sn-ex-t'>%s</span><p class='sn-ex-q'>%s</p>"
            "<p class='sn-ex-s'>%s</p><p class='sn-ex-a'>Answer: %s</p></div>" % (title, q, s, a))


def table(head, rows):
    h = "".join("<th>%s</th>" % x for x in head)
    b = "".join("<tr>" + "".join("<td>%s</td>" % c for c in r) + "</tr>" for r in rows)
    return "<div class='sn-tw'><table class='sn-table'><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>" % (h, b)


LV = [7, 3, 6, 4]


def lg(svg):
    return svg.replace("<svg ", "<svg data-pf='lg' ", 1)


def body_html():
    assert mean(LV) == 5
    lev = lg(level_svg(LV, 5))
    model = lg(model_svg([("Smaller", [(36, "1 u", "u")], ""), ("Bigger", [(36, "1 u", "u"), (18, "18", "x")], "?")],
                         F(3), total="90", label="bar model: two numbers with an average of 45"))
    return (
        "<h2>What is an average?</h2>"
        "<p>An <b>average</b> tells you how much each item would have if the total were <b>shared equally</b>.</p>"
        "<p><b>Average = total value ÷ number of data</b></p>"
        "<figure class='sn-fig'>" + lev +
        "<figcaption>Towers of 7, 3, 6 and 4 cubes: 20 cubes in all. Share them equally among 4 towers: 20 ÷ 4 = 5. "
        "The average is 5.</figcaption></figure>" +
        ex("Example 1", "Find the average of 48, 52, 39, 45 and 61.",
           "Total = 48 + 52 + 39 + 45 + 61 = 245. There are 5 numbers. 245 ÷ 5 = 49.", "49") +
        ex("Example 2", "Siti spent $2.40, $1.80, $3.10 and $2.30 at the canteen on 4 days. What was the average amount she spent per day?",
           "Total = $9.60. $9.60 ÷ 4 = $2.40.", "$2.40") +
        "<h2>Total value = average × number of data</h2>"
        "<p>If you know the average, multiply to get the total. Most PSLE average questions start here.</p>" +
        ex("Example 3", "The average of 4 numbers is 27. Three of the numbers are 18, 35 and 24. What is the fourth number?",
           "Total of 4 numbers = 4 × 27 = 108. The three numbers add up to 18 + 35 + 24 = 77. 108 − 77 = 31.", "31") +
        "<h2>When a value is added or removed</h2>"
        "<p>Find the old total and the new total. The difference is the value that was added or removed.</p>" +
        ex("Example 4", "The average age of 4 children is 10 years. When their aunt joins them, the average age increases by 6 years. How old is the aunt?",
           "Old total = 4 × 10 = 40. New average = 10 + 6 = 16, so new total = 5 × 16 = 80. Aunt = 80 − 40 = 40.",
           "40 years") +
        "<h2>Average with the model method</h2>"
        "<p>When the numbers are compared, change the average into a total first. Then draw a model and use units.</p>"
        "<figure class='sn-fig'>" + model +
        "<figcaption>The average of two numbers is 45, so their total is 2 × 45 = 90. One number is 18 more than the "
        "other. 2 units = 90 − 18 = 72, so 1 unit = 36. The bigger number is 36 + 18 = 54.</figcaption></figure>"
        "<h2>Common mistakes</h2>" +
        table(["Mistake", "What to do instead"], [
            ["Dividing by the wrong number of data", "Count the data. A 0 (a day with no rain) is still a piece of data"],
            ["Giving the total or the middle value as the average", "Average = total ÷ number of data"],
            ["Dividing the average to find the total", "Total = average × number of data"],
            ["Adding a new value straight onto the average", "Find the old total, add the value, then divide by the new number of data"],
            ["Using the average in a missing-value question", "Multiply back to the total first, then subtract what you know"],
            ["Finding the average of two averages for groups of different sizes", "Find each total, add them, then divide by everyone"],
        ])
    )


FAQ = [
    {"q": "How do you find the average in P6 maths?",
     "a": "Add all the values to get the total, then divide by the number of data. For 7, 3, 6 and 4 the total is 20, and 20 ÷ 4 = 5, so the average is 5."},
    {"q": "Is average tested in the PSLE?",
     "a": "Yes. Average is part of the Primary 6 Statistics topic in the MOE syllabus, and PSLE questions often combine it with the model method, before-and-after changes or a bar graph."},
    {"q": "How do I solve a question where the average increases after someone joins?",
     "a": "Find the old total (old average × old number) and the new total (new average × new number), then subtract. If 4 children have an average age of 10 and the average becomes 16 when an adult joins, the adult is 80 − 40 = 40 years old."},
    {"q": "What is the most common mistake with averages?",
     "a": "Forgetting to multiply back to the total. Questions about a missing value, a new value or two groups must be worked with totals, not with the averages themselves."},
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
    rnd = random.Random(66810)
    P = People(rnd)
    sets = [set_find(rnd, P), set_total(rnd, P), set_missing(rnd, P), set_change(rnd, P), set_words(rnd, P)]
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
        "country": "sg", "subject": "maths", "grade": "primary-6", "slug": "average", "sort": 10,
        "updated": UPDATED, "pdf_url": "",
        "title": "Primary 6 Average",
        "seo_title": "P6 Average Worksheets: Free Primary 6 Maths with Answers (MOE Syllabus, PSLE Practice)",
        "short_title": "Average",
        "domain": "Statistics",
        "standard_code": "Primary 6: Statistics",
        "standard_url": "https://www.moe.gov.sg/primary/curriculum/syllabus",
        "standard_text": "Average as total value ÷ number of data; relationship between average, total value and number of data",
        "meta_desc": "Free P6 average worksheets: find the average, the total and a missing value, and solve PSLE-style word problems. 100 questions with answers.",
        "key_big": "Average = total value ÷ number of data",
        "key_sub": "The average of 7, 3, 6 and 4 is 20 ÷ 4 = 5. To work backwards, total value = average × number of data.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }


if __name__ == "__main__":
    u = gen_unit()
    mark_large(u, "(bar graph|table|bar model)")
    assert len(u["meta_desc"]) <= 160, len(u["meta_desc"])
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
