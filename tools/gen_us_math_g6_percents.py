# -*- coding: utf-8 -*-
"""
US Grade 6 Math: Percents (6.RP.A.3c)
  python3 tools/gen_us_math_g6_percents.py
Percent of a quantity as a rate per 100, and finding the whole from a part and a percent.
All arithmetic uses fractions.Fraction, so every answer is exact; every right answer is checked in code.
Every 10 x 10 grid and double number line is drawn from the numbers in the question.
HTML attributes use single quotes (no backslashes in the JSON).
Grade 6 style: numbers 1,000 and above are written with commas; minus sign is U+2212.
"""
import json, os, random, re
from fractions import Fraction as F
from math import gcd

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "us", "math", "grade-6")
UPDATED = "2026-11-02"
FILL = "#4fae74"
LINE = "#2b2b2b"
THIN = "#8a8a8a"
RED = "#c0392b"
FONT = "Arial, Helvetica, sans-serif"
MINUS = "−"
GIRLS = ["Maya", "Ava", "Mia", "Zoe", "Lily", "Emma", "Nora", "Ruby", "Sofia", "Grace"]
BOYS = ["Leo", "Noah", "Eli", "Sam", "Ben", "Omar", "Kai", "Jack", "Luis", "Owen"]


# ------------------------------------------------------------ numbers
def num(x):
    """Exact decimal text, commas from 1,000: F(9, 2) -> '4.5', 2500 -> '2,500'."""
    x = F(x)
    assert x >= 0, x
    d, k = x.denominator, 0
    while (10 ** k) % d:
        k += 1
        assert k < 8, x
    v = x.numerator * (10 ** k // d)
    i, r = divmod(v, 10 ** k)
    s = "{:,}".format(i)
    if r:
        s += "." + str(r).zfill(k).rstrip("0")
    return s


def pct(x):
    return num(x) + "%"


def money(x, cents=False):
    x = F(x)
    if cents or x.denominator != 1:
        c = x * 100
        assert c.denominator == 1, x
        c = int(c)
        return "$%s.%02d" % ("{:,}".format(c // 100), c % 100)
    return "$" + num(x)


def fr(a, b):
    return "<span class='fr'><span class='fn'>%s</span><span class='fd'>%s</span></span>" % (a, b)


def frs(x):
    """A Fraction in simplest form as a fraction picture."""
    x = F(x)
    return fr(x.numerator, x.denominator)


def plain(s):
    return re.sub(r"<[^>]+>", " ", s)


def mcq(q, right, wrongs, e):
    """right first; balance() moves it. All 4 choices must differ."""
    ch = [right] + list(wrongs)
    assert len(ch) == 4, (q, ch)
    assert len({re.sub(r"\s+", " ", plain(c)).strip() for c in ch}) == 4, ch
    return {"q": q, "c": ch, "a": 0, "e": e}


def nmcq(q, right, wrongs, e, unit="", kind="num"):
    """Number choices: all values must be different and positive. kind: num, pct or money."""
    vals = [F(right)] + [F(w) for w in wrongs]
    assert len(set(vals)) == 4 and all(v > 0 for v in vals), (q, vals)
    if kind == "money":
        cents = any(v.denominator != 1 for v in vals)
        ch = [money(v, cents) for v in vals]
    elif kind == "pct":
        ch = [pct(v) for v in vals]
    else:
        ch = [num(v) + unit for v in vals]
    return mcq(q, ch[0], ch[1:], e)


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


def cap(s):
    return s[0].upper() + s[1:]


def fig(svg):
    return "<div class='qfig'>" + svg + "</div>"


def svg_wrap(w, h, body, label):
    return ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 %d %d' width='%d' height='%d' "
            "role='img' aria-label='%s'><g font-family='%s'>%s</g></svg>" % (w, h, w, h, label, FONT, body))


def table(head, rows):
    h = "".join("<th>%s</th>" % x for x in head)
    b = "".join("<tr>" + "".join("<td>%s</td>" % c for c in r) + "</tr>" for r in rows)
    return "<div class='sn-tw'><table class='sn-table'><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>" % (h, b)


def ex(title, q, s, a):
    return ("<div class='sn-ex'><span class='sn-ex-t'>%s</span><p class='sn-ex-q'>%s</p>"
            "<p class='sn-ex-s'>%s</p><p class='sn-ex-a'>Answer: %s</p></div>" % (title, q, s, a))


def mark_large(u, pattern):
    """Tag pictures that must print larger (grids, double number lines) so squares and labels stay readable."""
    rx = re.compile(r"<svg (?=[^>]*aria-label='" + pattern + ")")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u


# ------------------------------------------------------------ pictures
def text(x, y, t, fs=16, col=LINE, anchor="middle", weight="700"):
    return ("<text x='%.1f' y='%.1f' font-size='%d' font-weight='%s' fill='%s' text-anchor='%s'>%s</text>"
            % (x, y, fs, weight, col, anchor, t))


def grid_body(k, ox, oy, cell):
    """10 x 10 grid with k squares shaded: full columns first, then from the top of the next column."""
    assert 0 <= k <= 100
    s = []
    for c in range(10):
        for r in range(10):
            if c * 10 + r < k:
                s.append("<rect x='%d' y='%d' width='%d' height='%d' fill='%s'/>" % (ox + c * cell, oy + r * cell, cell, cell, FILL))
    for i in range(1, 10):
        s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='1.2'/>"
                 % (ox + i * cell, oy, ox + i * cell, oy + 10 * cell, THIN))
        s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='1.2'/>"
                 % (ox, oy + i * cell, ox + 10 * cell, oy + i * cell, THIN))
    s.append("<rect x='%d' y='%d' width='%d' height='%d' fill='none' stroke='%s' stroke-width='2.5'/>"
             % (ox, oy, 10 * cell, 10 * cell, LINE))
    return "".join(s)


def grid_svg(k, cell=18):
    pad = 4
    w = 10 * cell + 2 * pad
    return svg_wrap(w, w, grid_body(k, pad, pad, cell), "10 by 10 grid with %d of 100 squares shaded" % k)


def dnl_svg(parts, top, bot, W=440):
    """Double number line: percents on top, amounts below, `parts` equal spaces.
    top / bot: {tick index: label}. A label '?' is drawn in red."""
    L, R, Y1, Y2 = 34, W - 34, 44, 100
    H = Y2 + 40

    def X(i):
        return L + (R - L) * i / float(parts)
    s = []
    for y in (Y1, Y2):
        s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='2.5'/>" % (L, y, R, y, LINE))
    for i in range(parts + 1):
        big = i in top or i in bot
        h = 10 if big else 6
        for y in (Y1, Y2):
            s.append("<line x1='%.1f' y1='%d' x2='%.1f' y2='%d' stroke='%s' stroke-width='%s'/>"
                     % (X(i), y - h, X(i), y + h, LINE, "2.5" if big else "1.8"))
        if i in top and i in bot:
            s.append("<line x1='%.1f' y1='%d' x2='%.1f' y2='%d' stroke='%s' stroke-width='1.2' stroke-dasharray='4 4'/>"
                     % (X(i), Y1 + 12, X(i), Y2 - 12, THIN))
    for i, t in top.items():
        q = t == "?"
        s.append(text(X(i), Y1 - 17, t, 20 if q else 16, RED if q else LINE, weight="800" if q else "700"))
    for i, t in bot.items():
        q = t == "?"
        s.append(text(X(i), Y2 + 32, t, 20 if q else 16, RED if q else LINE, weight="800" if q else "700"))
    lab = "double number line with %d equal parts: %s on top, %s below" % (
        parts, ", ".join(top[i] for i in sorted(top)), ", ".join(bot[i] for i in sorted(bot)))
    return svg_wrap(W, H, "".join(s), lab.replace("?", "unknown"))


# ============================================================ set 1: percent means per 100
def set_per100(rnd):
    its = []
    grids = [(37, [F("0.37"), 63, F("3.7")]),
             (8, [F("0.08"), 92, 80]),
             (60, [6, 40, F("0.6")]),
             (45, [55, F("4.5"), F("0.45")]),
             (92, [8, F("9.2"), F("0.92")]),
             (3, [30, 97, F("0.03")])]
    for k, wr in grids:
        e = ("The grid has <b>100 equal squares</b>, and %d of them are shaded. %d out of 100 = %s = <b>%d%%</b>. "
             "Percent means “per 100.”" % (k, k, fr(k, 100), k))
        if k % 10 == 0:
            e += " %d full columns are %d squares, not %d%%." % (k // 10, k, k // 10)
        if k < 10:
            e += " There is no full column, so it is less than 10%."
        e += " (%d%% is the white part.)" % (100 - k)
        its.append(nmcq(fig(grid_svg(k)) + "What percent of the grid is shaded?", k, wr, e, kind="pct"))

    for k, right, wrong, note in [(25, (1, 4), [(1, 25), (3, 4), (1, 5)], "It is not " + fr(1, 25) + ": 25% means 25 out of 100, not 1 out of 25."),
                                  (40, (2, 5), [(1, 40), (4, 100), (3, 5)], fr(4, 100) + " would be only 4 squares.")]:
        g = gcd(k, 100)
        e = ("%d out of 100 squares are shaded: %s. Divide the top and bottom by %d: %s = <b>%s</b>. %s"
             % (k, fr(k, 100), g, fr(k, 100), fr(*right), note))
        its.append(mcq(fig(grid_svg(k)) + "Which fraction in simplest form names the shaded part?",
                       fr(*right), [fr(*w) for w in wrong], e))

    p2d = [(25, ["0.025", "2.5", "25.0"], "0.025 would be 2.5%."),
           (7, ["0.7", "7.0", "0.007"], "0.7 would be 70%. Write a 0 in the tenths place: 7 hundredths."),
           (60, ["0.06", "6.0", "60.0"], "0.06 would be only 6%."),
           (125, ["0.125", "12.5", "0.25"], "More than 100% is more than 1 whole, so the decimal is more than 1.")]
    for p, wr, note in p2d:
        d = num(F(p, 100))
        e = ("Percent means “per 100,” so divide by 100: %d%% = %s = <b>%s</b>. Move the decimal point 2 places left. %s"
             % (p, fr(p, 100), d, note))
        its.append(mcq("Write <b>%d%%</b> as a decimal." % p, d, wr, e))

    d2p = [(F("0.4"), [4, F("0.4"), 400], "4% would be 0.04."),
           (F("0.05"), [50, F("0.05"), 500], "50% would be 0.5."),
           (F("0.5"), [F("0.5"), 5, 500], "0.5% is less than 1%, so it is much smaller than 0.5.")]
    for d, wr, note in d2p:
        p = d * 100
        e = ("Multiply by 100 (move the point 2 places right): %s = %s = <b>%s</b>. %s" % (num(d), fr(num(p), 100), pct(p), note))
        its.append(nmcq("Write <b>%s</b> as a percent." % num(d), p, wr, e, kind="pct"))

    f2p = [((3, 4), [34, F("0.75"), 25], "Do not just write the digits 3 and 4 together."),
           ((1, 5), [15, 5, F("0.2")], "Do not write the digits 1 and 5 together. 5% would be 1/20."),
           ((3, 25), [3, 75, F("0.12")], "3% would be 3/100, not 3/25.")]
    for (a, b), wr, note in f2p:
        m = 100 // b
        p = F(a, b) * 100
        note = note.replace("1/20", fr(1, 20)).replace("3/100", fr(3, 100)).replace("3/25", fr(3, 25))
        e = ("Make the bottom 100. Multiply the top and bottom by %d: %s = %s = <b>%s</b>. %s"
             % (m, fr(a, b), fr(a * m, 100), pct(p), note))
        its.append(nmcq("Write %s as a percent." % fr(a, b), p, wr, e, kind="pct"))

    p2f = [(50, (1, 2), [(1, 50), (1, 5), (5, 100)], "It is not " + fr(1, 50) + ": that is 2%."),
           (20, (1, 5), [(1, 20), (2, 100), (4, 5)], "It is not " + fr(1, 20) + ": that is 5%. And " + fr(4, 5) + " is 80%.")]
    for p, right, wr, note in p2f:
        g = gcd(p, 100)
        e = ("%d%% = %s. Divide the top and bottom by %d: <b>%s</b>. %s" % (p, fr(p, 100), g, fr(*right), note))
        its.append(mcq("Which fraction in simplest form is equal to <b>%d%%</b>?" % p, fr(*right), [fr(*w) for w in wr], e))
    assert len(its) == 20, len(its)
    return {"title": "Percent means per 100: grids, fractions and decimals", "items": its}


# ============================================================ set 2: benchmark percents
def bench_e(p, n):
    r = F(p * n, 100)
    if p == 10:
        return "10%% = %s, so divide by 10: %s ÷ 10 = <b>%s</b>." % (fr(1, 10), num(n), num(r))
    if p == 50:
        return "50%% = %s, so divide by 2: %s ÷ 2 = <b>%s</b>. Half of the number." % (fr(1, 2), num(n), num(r))
    if p == 25:
        return "25%% = %s, so divide by 4: %s ÷ 4 = <b>%s</b>." % (fr(1, 4), num(n), num(r))
    if p == 75:
        q = F(n, 4)
        return ("75%% = %s. First find 25%%: %s ÷ 4 = %s. Then 75%% is 3 times that: 3 × %s = <b>%s</b>."
                % (fr(3, 4), num(n), num(q), num(q), num(r)))
    if p == 1:
        return "1%% = %s, so divide by 100: %s ÷ 100 = <b>%s</b>." % (fr(1, 100), num(n), num(r))
    if p == 20:
        return "20%% = %s, so divide by 5: %s ÷ 5 = <b>%s</b>. (Or: 10%% is %s, and 20%% is 2 × %s.)" % (
            fr(1, 5), num(n), num(r), num(F(n, 10)), num(F(n, 10)))
    if p == 5:
        t = F(n, 10)
        return "10%% of %s is %s. 5%% is half of 10%%: %s ÷ 2 = <b>%s</b>." % (num(n), num(t), num(t), num(r))
    if p == 200:
        return "100%% is the whole number, so 200%% is 2 times it: 2 × %s = <b>%s</b>." % (num(n), num(r))
    if p == 150:
        h = F(n, 2)
        return ("150%% = 100%% + 50%%. 100%% of %s is %s, and 50%% is %s. %s + %s = <b>%s</b>."
                % (num(n), num(n), num(h), num(n), num(h), num(r)))
    raise ValueError(p)


def set_bench(rnd):
    its = []
    items = [(10, 80, [800, 72, 90], "Not 10 × 80: percent means per 100."),
             (10, 350, [F("3.5"), 315, 3500], "3.5 would be 1%."),
             (50, 64, [3200, 114, 14], "Do not add or subtract 50."),
             (50, 90, [180, 140, 40], "180 doubles the number; 50% halves it."),
             (25, 80, [F("3.2"), 60, 40], "Not 80 ÷ 25: 25% is one fourth. 60 is the other 75%."),
             (25, 36, [27, 18, 61], "27 is the other 75%, and 18 is 50%."),
             (75, 80, [20, 5, 155], "20 is only 25%. Remember to multiply by 3."),
             (75, 40, [10, 115, 3000], "10 is only 25%."),
             (1, 600, [60, F("0.6"), 599], "60 would be 10%."),
             (1, 2500, [250, F("2.5"), 2525], "250 would be 10%."),
             (20, 45, [F("2.25"), 36, F("4.5")], "Not 45 ÷ 20: 20% is one fifth. 4.5 is only 10%."),
             (20, 150, [F("7.5"), 120, 15], "15 is only 10%. 120 is the other 80%."),
             (5, 60, [12, 6, 57], "12 would be 20% (60 ÷ 5). 6 is 10%."),
             (5, 240, [48, 24, 228], "48 would be 20% (240 ÷ 5). 24 is 10%."),
             (200, 15, [F("7.5"), 3000, 215], "200% is more than the whole, so the answer is more than 15."),
             (150, 40, [20, 6000, 190], "150% is more than 100%, so the answer is more than 40.")]
    for p, n, wr, note in items:
        r = F(p * n, 100)
        its.append(nmcq("What is <b>%d%%</b> of %s?" % (p, num(n)), r, wr, bench_e(p, n) + " " + note))

    figs = [(10, 120, 3, [30, 12, 84]),
            (4, 60, 3, [15, 75, 30]),
            (5, 200, 2, [40, 120, 160]),
            (10, 50, 7, [70, 15, 5])]
    for parts, n, k, wr in figs:
        step = 100 // parts
        p = k * step
        r = F(n * k, parts)
        u = F(n, parts)
        top = {0: "0%", k: "%d%%" % p, parts: "100%"}
        bot = {0: "0", k: "?", parts: num(n)}
        e = ("100%% matches %s. The lines have %d equal parts, so each part is %d%% and %s ÷ %d = %s. "
             "%d%% is %d parts: %d × %s = <b>%s</b>." % (num(n), parts, step, num(n), parts, num(u), p, k, k, num(u), num(r)))
        if num(p) in [num(w) for w in wr]:
            e += " The answer is an amount, not the percent %d." % p
        its.append(nmcq(fig(dnl_svg(parts, top, bot)) + "The double number line shows that 100%% is %s. What is %d%% of %s?"
                        % (num(n), p, num(n)), r, wr, e))
    assert len(its) == 20, len(its)
    return {"title": "Benchmark percents: 10%, 25%, 50%, 75% and more", "items": its}


# ============================================================ set 3: percent of a quantity
def pof_e(p, n):
    p = F(p)
    r = p * n / 100
    d = num(p / 100)
    top = fr(num(p), 100)
    e = "%s%% = %s = %s. Multiply: %s × %s = <b>%s</b>." % (num(p), top, d, d, num(n), num(r))
    if p.denominator == 1 and p % 10 == 0 and p <= 100 and F(n, 10).denominator == 1:
        t = F(n, 10)
        e += " Check: 10%% of %s is %s, and %s × %s = %s." % (num(n), num(t), num(p / 10), num(t), num(r))
    elif p.denominator == 1 and p % 5 == 0 and p < 100 and F(n, 20).denominator == 1:
        t = F(n, 10)
        e += " Check: 10%% of %s is %s and 5%% is %s, so %s%% is %s." % (num(n), num(t), num(t / 2), num(p), num(r))
    return e


def set_pof(rnd):
    its = []
    items = [(30, 70, [2100, 49, 100], "Not 30 × 70: percent means per 100."),
             (15, 60, [4, 900, 51], "Not 60 ÷ 15 = 4. 51 is the other 85%."),
             (40, 85, [51, 3400, F("8.5")], "8.5 is only 10%."),
             (35, 80, [52, 2800, 115], "Do not add the percent to the number."),
             (12, 50, [44, 600, 62], "44 is the other 88%."),
             (8, 25, [200, 23, 20], "8% = 0.08, not 0.8."),
             (65, 40, [14, 2600, 105], "14 is the other 35%."),
             (45, 120, [66, 5400, 165], "66 is the other 55%."),
             (90, 30, [3, 2700, 120], "3 is only 10%. 90% is almost all of 30."),
             (6, 150, [90, 25, 141], "6% = 0.06, not 0.6. And not 150 ÷ 6."),
             (18, 200, [164, 3600, F("3.6")], "18% of 200 is 2 × 18, because 1% of 200 is 2."),
             (2, 450, [90, 225, 441], "2% = 0.02, not 0.2. And not 450 ÷ 2."),
             (30, 15, [45, F("0.5"), F("10.5")], "Check the decimal point: 3 × 1.5 = 4.5."),
             (120, 35, [7, 155, 4200], "120% is more than 100%, so the answer is more than 35."),
             (F("0.5"), 400, [200, 20, 800], "0.5% is half of 1%, not 50%. 1% of 400 is 4, so 0.5% is 2."),
             (125, 48, [12, 173, 6000], "125% = 100% + 25% = 48 + 12."),
             (3, 1200, [360, 400, 1164], "3% = 0.03, not 0.3. And not 1,200 ÷ 3."),
             (24, 75, [57, 1800, 99], "57 is the other 76%.")]
    for p, n, wr, note in items:
        r = F(p) * n / 100
        its.append(nmcq("What is <b>%s%%</b> of %s?" % (num(p), num(n)), r, wr, pof_e(p, n) + " " + note))

    its.append(mcq("Which expression finds <b>30% of 70</b>?", fr(30, 100) + " × 70",
                   ["30 × 70", "70 ÷ 30", "70 %s 30" % MINUS],
                   "30%% means 30 per 100, so 30%% of 70 is %s × 70 = 21. 30 × 70 forgets to divide by 100." % fr(30, 100)))
    its.append(mcq("Which expression finds <b>15% of 60</b>?", "0.15 × 60", ["15 × 60", "0.015 × 60", "60 ÷ 15"],
                   "15%% = %s = 0.15, so 15%% of 60 is 0.15 × 60 = 9. 0.015 would be 1.5%%." % fr(15, 100)))
    assert len(its) == 20, len(its)
    return {"title": "Find the percent of a quantity", "items": its}


# ============================================================ set 4: find the whole
def whole_e(part, p):
    """part is p% of the whole. Use g% chunks with g = gcd(p, 100)."""
    g = gcd(p, 100)
    k = p // g
    unit = F(part, k)
    assert unit.denominator == 1, (part, p)
    whole = F(part * 100, p)
    m = 100 // g
    if k == 1:
        e = ("%s is %d%% of the whole. 100%% is %d times %d%%, so the whole is %d × %s = <b>%s</b>."
             % (num(part), p, m, p, m, num(part), num(whole)))
    else:
        e = ("%d%% is %d groups of %d%%. So %d%% is %s ÷ %d = %s. 100%% is %d groups of %d%%: %d × %s = <b>%s</b>."
             % (p, k, g, g, num(part), k, num(unit), m, g, m, num(unit), num(whole)))
    e += " Check: %d%% of %s is %s." % (p, num(whole), num(part))
    return e, whole


def set_whole(rnd):
    its = []
    figs = [(12, 25, 4, [3, 36, 300]),
            (30, 75, 4, [F("22.5"), 10, 105]),
            (18, 30, 10, [F("5.4"), 42, 48]),
            (24, 80, 5, [F("19.2"), 6, 104])]
    for part, p, parts, wr in figs:
        e, whole = whole_e(part, p)
        k = p * parts // 100
        top = {0: "0%", k: "%d%%" % p, parts: "100%"}
        bot = {0: "0", k: num(part), parts: "?"}
        e += " Do not multiply %s by %d%%: that finds a part of %s, not the whole." % (num(part), p, num(part))
        its.append(nmcq(fig(dnl_svg(parts, top, bot)) + "%s is %d%% of a number. What is the number?" % (num(part), p),
                        whole, wr, e))

    items = [(9, 10, [F("0.9"), 81, 19], "The whole is bigger than the part."),
             (15, 50, [F("7.5"), 65, 750], "50% is half, so the whole is double."),
             (7, 20, [F("1.4"), 28, 27], "28 is the other 80%."),
             (6, 5, [F("0.3"), 30, 11], "30 would be 6 × 5. The whole is 20 times 5%."),
             (4, 1, [F("0.04"), 40, 396], "1% is a very small part, so the whole is much bigger than 4."),
             (21, 35, [F("7.35"), 39, 56], "39 is the other 65%."),
             (45, 90, [F("40.5"), 5, 135], "90% is almost all, so the whole is a little more than 45."),
             (16, 40, [F("6.4"), 24, 56], "24 is the other 60%."),
             (27, 45, [F("12.15"), 33, 72], "33 is the other 55%."),
             (36, 120, [F("43.2"), 6, 156], "120% is more than the whole, so the whole is less than 36."),
             (3, 12, [F("0.36"), 22, 15], "22 is the other 88%."),
             (13, 65, [F("8.45"), 7, 78], "7 is the other 35%.")]
    for part, p, wr, note in items:
        e, whole = whole_e(part, p)
        its.append(nmcq("<b>%s</b> is <b>%d%%</b> of what number?" % (num(part), p), whole, wr, e + " " + note))

    wp = [(9, 20, [9, F("0.45"), 55]),
          (6, 24, [6, 400, F("0.25")]),
          (14, 40, [14, F("0.35"), 65]),
          (33, 300, [33, F("0.11"), 89])]
    for part, n, wr in wp:
        p = F(part * 100, n)
        f = F(part, n)
        steps = [fr(part, n)]
        if (f.numerator, f.denominator) != (part, n):
            steps.append(frs(f))
        if f.denominator != 100:
            steps.append(fr(num(f * 100), 100))
        e = ("Write the part over the whole and make the bottom 100: %s = <b>%s</b>. "
             "The part is %s, but the percent is out of 100." % (" = ".join(steps), pct(p), num(part)))
        its.append(nmcq("What percent of <b>%s</b> is <b>%s</b>?" % (num(n), num(part)), p, wr, e, kind="pct"))
    assert len(its) == 20, len(its)
    return {"title": "Find the whole from a part and a percent", "items": its}


# ============================================================ set 5: word problems
def set_words(rnd):
    its = []
    P = People(rnd)
    # right answers of the stories below, checked here
    for got, want in [(F(18, 20) * 100, 90), (F(85, 100) * 40, 34), (F(100, 25), 4), (F(25, 100) * 60, 15),
                      (F(15, 100) * 80, 12), (F(20, 100) * 45, 9), (6 / F(10, 100), 60), (F(40, 100) * 25, 10),
                      (12 / F(30, 100), 40), (F(8, 100) * 500, 40), (F(60, 100) * 15, 9), (18 / F(75, 100), 24),
                      (F(4, 16) * 100, 25), (F(35, 100) * 2000, 700), (45 / F(30, 100), 150), (120 / F(40, 100), 300),
                      (36 / F(75, 100), 48), (F(30, 100) * 50, F(50, 100) * 30), (F(17, 20) * 100, 85),
                      (F(42, 50) * 100, 84), (F(45, 100) * 220, 99)]:
        assert got == want, (got, want)

    n, he, his = P.next()
    its.append(nmcq("%s got 18 out of 20 questions right on a quiz. What percent did %s get right?" % (n, he),
                    90, [18, 10, F("0.9")],
                    "%s = %s = <b>90%%</b>. Multiply the top and bottom by 5 to get a bottom of 100. "
                    "(10%% is the part %s got wrong.)" % (fr(18, 20), fr(90, 100), he), kind="pct"))

    n, he, his = P.next()
    its.append(nmcq("A test has 40 questions. %s scored 85%%. How many questions did %s get right?" % (n, he),
                    34, [6, 85, 45],
                    "85%% of 40 = 0.85 × 40 = <b>34</b>. Check: 10%% of 40 is 4, so 5%% is 2 and 85%% is 8 × 4 + 2 = 34. "
                    "(6 is the number %s got wrong.)" % he))

    its.append(nmcq("A spelling test has 25 words. Each word is worth the same. What percent is each word worth?",
                    4, [25, 1, F("0.04")],
                    "The whole test is 100%%. Share 100%% among 25 words: 100 ÷ 25 = <b>4%%</b>. "
                    "So %s = %s." % (fr(1, 25), fr(4, 100)), kind="pct"))

    n, he, his = P.next()
    its.append(nmcq("%s buys a $60 jacket that is 25%% off. How much money does %s save?" % (n, he),
                    15, [45, 35, F("2.4")],
                    "25%% = %s, so the discount is $60 ÷ 4 = <b>$15</b>. $45 is the sale price, not the amount saved. "
                    "Do not subtract 25 from 60." % fr(1, 4), kind="money"))

    its.append(nmcq("Shoes cost $80. They are 15% off. How many dollars off is that?",
                    12, [68, 65, F("1.2")],
                    "15%% of $80 = 0.15 × 80 = <b>$12</b>. Check: 10%% is $8 and 5%% is $4, so 15%% is $12. "
                    "($68 is the new price.)", kind="money"))

    its.append(nmcq("A video game costs $45. It is on sale for 20% off. How much is the discount?",
                    9, [36, 25, F("2.25")],
                    "20%% = %s, so the discount is $45 ÷ 5 = <b>$9</b>. Not $45 ÷ 20: 20%% means 20 per 100." % fr(1, 5),
                    kind="money"))

    its.append(nmcq("A store takes $6 off the price of a lamp. That is 10% off. What was the price of the lamp?",
                    60, [F("0.6"), 54, 16],
                    "$6 is 10%% of the price. 100%% is 10 times 10%%: 10 × $6 = <b>$60</b>. "
                    "Check: 10%% of $60 is $6.", kind="money"))

    its.append(nmcq("In a class of 25 students, 40% walk to school. How many students walk?",
                    10, [15, 65, F("6.25")],
                    "40%% of 25 = 0.4 × 25 = <b>10</b>. Check: 20%% of 25 is 5, so 40%% is 10. "
                    "(15 students do not walk.)"))

    its.append(nmcq("In a class survey, 12 students chose pizza. That is 30% of the class. How many students are in the class?",
                    40, [F("3.6"), 28, 42],
                    "30%% is 3 groups of 10%%, so 10%% is 12 ÷ 3 = 4. 100%% is 10 × 4 = <b>40</b> students. "
                    "Check: 30%% of 40 is 12. 3.6 is 30%% of 12, which finds a part, not the whole."))

    its.append(nmcq("A school has 500 students. 8% of them are left-handed. How many students are left-handed?",
                    40, [400, 460, F("62.5")],
                    "8%% = 0.08. 0.08 × 500 = <b>40</b>. Check: 1%% of 500 is 5, so 8%% is 8 × 5 = 40. "
                    "8%% is 0.08, not 0.8."))

    n, he, his = P.next()
    its.append(nmcq("%s took 15 free throws in a basketball game and made 60%% of them. How many free throws did %s make?" % (n, he),
                    9, [6, 75, 90],
                    "60%% of 15 = 0.6 × 15 = <b>9</b>. Check: 10%% of 15 is 1.5, and 6 × 1.5 = 9. "
                    "(6 is the number %s missed.)" % he))

    its.append(nmcq("A soccer team won 75% of its games this season. It won 18 games. How many games did the team play?",
                    24, [F("13.5"), 6, 93],
                    "75%% is 3 groups of 25%%, so 25%% is 18 ÷ 3 = 6. 100%% is 4 × 6 = <b>24</b> games. "
                    "Check: 75%% of 24 is 18."))

    n, he, his = P.next()
    its.append(nmcq("%s took 16 shots in a hockey game and scored on 4 of them. What percent of %s shots scored?" % (n, his),
                    25, [4, 75, 400],
                    "%s = %s = %s = <b>25%%</b>. (75%% of the shots did not score.)" % (fr(4, 16), fr(1, 4), fr(25, 100)),
                    kind="pct"))

    its.append(nmcq("A 2-liter water bottle holds 2,000 mL. It is 35% full. How many milliliters of water are in it?",
                    700, [1300, 70, 2035],
                    "35%% of 2,000 = 0.35 × 2,000 = <b>700 mL</b>. Check: 10%% is 200 mL and 5%% is 100 mL, "
                    "so 35%% is 600 + 100 = 700 mL.", unit=" mL"))

    n, he, his = P.next()
    its.append(nmcq("%s has saved $45 for a bike. That is 30%% of the price. What is the price of the bike?" % n,
                    150, [F("13.5"), 105, 75],
                    "30%% is 3 groups of 10%%, so 10%% is $45 ÷ 3 = $15. 100%% is 10 × $15 = <b>$150</b>. "
                    "Check: 30%% of $150 is $45. ($105 is the money %s still needs.)" % he, kind="money"))

    its.append(nmcq("A file is 40% downloaded. So far, 120 MB have downloaded. How big is the whole file?",
                    300, [48, 180, 160],
                    "40%% is 2 groups of 20%%, so 20%% is 120 ÷ 2 = 60 MB. 100%% is 5 × 60 = <b>300 MB</b>. "
                    "Check: 40%% of 300 is 120.", unit=" MB"))

    its.append(nmcq("A school bus is 75% full. There are 36 students on it. How many seats does the bus have?",
                    48, [27, 12, 111],
                    "75%% is 3 groups of 25%%, so 25%% is 36 ÷ 3 = 12 seats. 100%% is 4 × 12 = <b>48</b> seats. "
                    "(12 seats are empty.)"))

    its.append(mcq("Which is more: 30% of 50 or 50% of 30?", "They are equal",
                   ["30% of 50", "50% of 30", "You can’t tell"],
                   "30%% of 50 = 0.3 × 50 = 15. 50%% of 30 = half of 30 = 15. They are <b>equal</b>. "
                   "(Both are 30 × 50 ÷ 100.)"))

    a, ah, _ = P.next()
    b, bh, _ = P.next()
    its.append(mcq("%s got 17 out of 20 on a math test. %s got 42 out of 50 on another test. Who got the higher percent?" % (a, b),
                   a, [b, "They are equal", "You can’t tell"],
                   "%s: %s = %s = 85%%. %s: %s = %s = 84%%. 85%% &gt; 84%%, so <b>%s</b> got the higher percent, "
                   "even though %s got more points." % (a, fr(17, 20), fr(85, 100), b, fr(42, 50), fr(84, 100), a, b)))

    n, he, his = P.next()
    its.append(nmcq("A book has 220 pages. %s has read 45%% of it. How many pages has %s read?" % (n, he),
                    99, [121, F("9.9"), 265],
                    "45%% of 220 = 0.45 × 220 = <b>99</b> pages. Check: 10%% is 22 and 5%% is 11, so 45%% is 4 × 22 + 11 = 99. "
                    "(121 pages are left to read.)"))
    for it in its:
        it["e"] = it["e"].replace("%%", "%")
    assert len(its) == 20, len(its)
    return {"title": "Percent word problems: tests, discounts, surveys and sports", "items": its}


# ============================================================ lesson
def body_html():
    f_grid = grid_svg(30, cell=20)
    f_of = dnl_svg(10, {0: "0%", 1: "10%", 3: "30%", 10: "100%"}, {0: "0", 1: "7", 3: "21", 10: "70"}, W=520)
    f_whole = dnl_svg(4, {0: "0%", 1: "25%", 2: "50%", 3: "75%", 4: "100%"}, {0: "0", 1: "12", 2: "24", 3: "36", 4: "48"})
    return (
        "<h2>Percent means “per 100”</h2>"
        "<p><b>Percent</b> means “out of 100.” 30% is 30 out of 100, or " + fr(30, 100) + ". "
        "100% is the whole. 50% is half.</p>"
        "<figure class='sn-fig'>" + f_grid +
        "<figcaption>30 of the 100 squares are shaded: 30% = " + fr(30, 100) + " = 0.3.</figcaption></figure>"
        "<h2>Percents, fractions and decimals</h2>"
        "<p>To change a percent to a decimal, divide by 100: move the point 2 places left.</p>"
        + table(["Percent", "Fraction", "Decimal"], [
            ["1%", fr(1, 100), "0.01"],
            ["10%", fr(1, 10), "0.1"],
            ["20%", fr(1, 5), "0.2"],
            ["25%", fr(1, 4), "0.25"],
            ["50%", fr(1, 2), "0.5"],
            ["75%", fr(3, 4), "0.75"],
            ["100%", "1", "1"],
        ]) +
        "<h2>Find a percent of a number</h2>"
        "<p>Change the percent to a fraction or decimal, then multiply. Benchmark percents make it quick: "
        "10% means divide by 10, 50% means divide by 2, 25% means divide by 4.</p>"
        + ex("Example", "What is 30% of 70?",
             "30% = " + fr(30, 100) + " = 0.3. 0.3 × 70 = 21. Or: 10% of 70 is 7, so 30% is 3 × 7 = 21.", "21")
        + "<figure class='sn-fig'>" + f_of +
        "<figcaption>100% matches 70. Each 10% is 7, so 30% is 21.</figcaption></figure>"
        "<h2>Find the whole</h2>"
        "<p>When you know a part and its percent, work up to 100%.</p>"
        + ex("Example", "12 is 25% of what number?",
             "100% is 4 times 25%. So the whole is 4 × 12 = 48. Check: 25% of 48 = 12.", "48")
        + "<figure class='sn-fig'>" + f_whole +
        "<figcaption>25% matches 12. Count up by 12 for each 25%: 24, 36, 48.</figcaption></figure>"
        + ex("Example", "18 is 30% of what number?",
             "30% is 3 groups of 10%, so 10% is 18 ÷ 3 = 6. 100% is 10 × 6 = 60.", "60")
        + "<h2>Common mistakes</h2>"
        + table(["Mistake", "What to do instead"], [
            ["30% of 70 = 30 × 70 = 2,100", "Percent means per 100: 0.3 × 70 = 21"],
            ["25% = 0.025", "Move the point 2 places: 25% = 0.25"],
            ["0.5% = 50%", "0.5% is half of 1%. 50% is half of the whole"],
            ["12 is 25% of ? → 12 × 0.25 = 3", "The whole is bigger than the part: 12 × 4 = 48"],
            ["$60 at 25% off saves $60 " + MINUS + " 25 = $35", "Find 25% of $60 first: $15"],
        ])
    )


FAQ = [
    {"q": "How do you find the percent of a number in 6th grade?",
     "a": "Write the percent as a fraction over 100 or as a decimal, then multiply. For example, 30% of 70 = 30/100 × 70 = 0.3 × 70 = 21."},
    {"q": "Why does percent mean per 100?",
     "a": "The word comes from “per centum,” Latin for “for each hundred.” So 45% is 45 out of every 100, or 45/100 = 0.45."},
    {"q": "How do you find the whole when you know the part and the percent?",
     "a": "Work up to 100%. If 12 is 25% of a number, then 100% is 4 times 25%, so the whole is 4 × 12 = 48."},
    {"q": "What is a double number line for percents?",
     "a": "It is two number lines that line up: percents on top and amounts below, with 100% matching the whole. It helps students see that 10% of 70 is 7, 30% is 21 and 100% is 70."},
]


def gen():
    rnd = random.Random(604)
    sets = [set_per100(rnd), set_bench(rnd), set_pof(rnd), set_whole(rnd), set_words(rnd)]
    balance(sets, rnd)
    for s in sets:
        assert len(s["items"]) == 20
        for it in s["items"]:
            assert len(set(it["c"])) == 4, it
    return {
        "country": "us", "subject": "math", "grade": "grade-6", "slug": "percents", "sort": 4,
        "updated": UPDATED, "pdf_url": "",
        "title": "Percents: Percent of a Number and Finding the Whole",
        "seo_title": "Grade 6 Percent Worksheets: Percent of a Number, Percent as a Rate per 100 and Finding the Whole",
        "short_title": "Percents",
        "domain": "Ratios and Proportional Relationships",
        "standard_code": "6.RP.A.3c",
        "standard_url": "https://www.thecorestandards.org/Math/Content/6/RP/A/3/",
        "standard_text": "Find a percent of a quantity as a rate per 100 (e.g., 30% of a quantity means 30/100 times the quantity); solve problems involving finding the whole, given a part and the percent.",
        "meta_desc": "Free Grade 6 percent worksheets: read percents on 10 × 10 grids, change percents to fractions and decimals, find 10%, 25%, 50% and 75% of a number, find 30% of 70, and find the whole from a part and a percent with double number lines. 100 practice questions with answers.",
        "key_big": "Percent means “per 100.” 30% of 70 = 30/100 × 70 = 21.",
        "key_sub": "To find the whole, work up to 100%: if 12 is 25% of a number, 100% is 4 times 25%, so the number is 4 × 12 = 48.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    mark_large(u, "(10 by 10 grid|double number line)")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
