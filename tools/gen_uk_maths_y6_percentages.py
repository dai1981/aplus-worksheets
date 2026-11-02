# -*- coding: utf-8 -*-
"""
UK Year 6 Maths: Percentages of amounts (National Curriculum in England, Year 6: Ratio and proportion)
  python3 tools/gen_uk_maths_y6_percentages.py
Percentages of amounts and measures, building percentages from 10%, 5% and 1%,
"what percentage is it?" and comparing with percentages.
All arithmetic uses fractions.Fraction, so every answer is exact; every right answer is checked in code.
Every bar model and grid is drawn from the numbers in the question.
HTML attributes use single quotes (no backslashes in the JSON).
UK style: numbers 1,000 and above with commas; money as £45, £40.50 or 80p; metric units.
"""
import json, os, random, re
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "uk", "maths", "year-6")
UPDATED = "2026-11-02"
FILL = "#9fd3b4"
DARK = "#006633"
LINE = "#2b2b2b"
THIN = "#8a8a8a"
RED = "#c0392b"
FONT = "Arial, Helvetica, sans-serif"
MINUS = "−"
GIRLS = ["Amelia", "Isla", "Freya", "Poppy", "Ava", "Aisha", "Lily", "Zara", "Grace", "Ruby", "Maya", "Evie"]
BOYS = ["Oliver", "Harry", "Mohammed", "Jack", "Arjun", "Noah", "George", "Leo", "Alfie", "Kai", "Ethan", "Charlie"]


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


def money(x, pence=False):
    """£45, £40.50 (pence=True: always two digits), 80p under £1"""
    x = F(x)
    c = x * 100
    assert c.denominator == 1 and c > 0, x
    c = int(c)
    if c < 100:
        return "%dp" % c
    if pence or c % 100:
        return "£{:,}.{:02d}".format(c // 100, c % 100)
    return "£{:,}".format(c // 100)


def fr(a, b):
    return "<span class='fr'><span class='fn'>%s</span><span class='fd'>%s</span></span>" % (a, b)


def plain(s):
    return re.sub(r"<[^>]+>", " ", s)


def mcq(q, right, wrongs, e):
    """right first; balance() moves it. All 4 choices must differ."""
    ch = [right] + list(wrongs)
    assert len(ch) == 4, (q, ch)
    assert len({re.sub(r"\s+", " ", plain(c)).strip() for c in ch}) == 4, ch
    return {"q": q, "c": ch, "a": 0, "e": e}


def nmcq(q, right, wrongs, e, unit="", kind="num"):
    """Number choices: all values different and positive. kind: num, pct or money."""
    vals = [F(right)] + [F(w) for w in wrongs]
    assert len(set(vals)) == 4 and all(v > 0 for v in vals), (q, vals)
    if kind == "money":
        pence = any((v * 100) % 100 for v in vals if v >= 1)
        ch = [money(v, pence) for v in vals]
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


def fig(svg):
    return "<div class='qfig'>" + svg + "</div>"


def svg_wrap(w, h, body, label):
    return ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 %d %d' width='%d' height='%d' "
            "role='img' aria-label='%s'><g font-family='%s'>%s</g></svg>" % (w, h, w, h, label, FONT, body))


def text(x, y, t, fs=16, col=LINE, anchor="middle", weight="700"):
    return ("<text x='%.1f' y='%.1f' font-size='%d' font-weight='%s' fill='%s' text-anchor='%s'>%s</text>"
            % (x, y, fs, weight, col, anchor, t))


def table(head, rows):
    h = "".join("<th>%s</th>" % x for x in head)
    b = "".join("<tr>" + "".join("<td>%s</td>" % c for c in r) + "</tr>" for r in rows)
    return "<div class='sn-tw'><table class='sn-table'><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>" % (h, b)


def ex(title, q, s, a):
    return ("<div class='sn-ex'><span class='sn-ex-t'>%s</span><p class='sn-ex-q'>%s</p>"
            "<p class='sn-ex-s'>%s</p><p class='sn-ex-a'>Answer: %s</p></div>" % (title, q, s, a))


def mark_large(u, pattern):
    """Tag pictures that must print larger (bar models, grids) so the parts and labels stay readable."""
    rx = re.compile(r"<svg (?=[^>]*aria-label='" + pattern + ")")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u


# ------------------------------------------------------------ pictures
def bar_svg(parts, shade, whole_txt, labels, ask="?", halves=(), W=460):
    """Bar model: a bar of `parts` equal parts, the first `shade` parts shaded.
    whole_txt is written over the whole bar (None: no label); labels: [(centre in part units, text)] inside the bar;
    halves: part indexes where a dashed line splits the part in two; ask: text under the shaded part (red)."""
    L, R = 14, W - 14
    pw = (R - L) / float(parts)
    top = 42 if whole_txt else 6
    Y0, Y1 = top, top + 44
    H = Y1 + (42 if ask else 6)
    s = []
    if whole_txt:
        s.append("<line x1='%d' y1='30' x2='%d' y2='30' stroke='%s' stroke-width='2'/>" % (L, R, LINE))
        for x in (L, R):
            s.append("<line x1='%d' y1='24' x2='%d' y2='36' stroke='%s' stroke-width='2'/>" % (x, x, LINE))
        tw = len(plain(whole_txt)) * 9 + 14
        s.append("<rect x='%.1f' y='12' width='%d' height='24' fill='#ffffff'/>" % ((L + R) / 2.0 - tw / 2.0, tw))
        s.append(text((L + R) / 2.0, 30, whole_txt, 17))
    if shade:
        s.append("<rect x='%d' y='%d' width='%.1f' height='%d' fill='%s'/>" % (L, Y0, pw * float(shade), Y1 - Y0, FILL))
    for i in range(1, parts):
        s.append("<line x1='%.1f' y1='%d' x2='%.1f' y2='%d' stroke='%s' stroke-width='1.6'/>" % (L + i * pw, Y0, L + i * pw, Y1, LINE))
    for i in halves:
        x = L + (i + 0.5) * pw
        s.append("<line x1='%.1f' y1='%d' x2='%.1f' y2='%d' stroke='%s' stroke-width='1.6' stroke-dasharray='4 3'/>" % (x, Y0, x, Y1, LINE))
    s.append("<rect x='%d' y='%d' width='%d' height='%d' fill='none' stroke='%s' stroke-width='2.5'/>" % (L, Y0, R - L, Y1 - Y0, LINE))
    for c, t in labels:
        s.append(text(L + c * pw, (Y0 + Y1) / 2.0 + 5, t, 14))
    if ask:
        xe = L + pw * float(shade)
        s.append("<path d='M%d %d L%d %d L%.1f %d L%.1f %d' fill='none' stroke='%s' stroke-width='2'/>"
                 % (L, Y1 + 6, L, Y1 + 13, xe, Y1 + 13, xe, Y1 + 6, RED))
        tw = len(plain(ask)) * 11
        cx = max((L + xe) / 2.0, L + tw / 2.0)
        s.append(text(cx, Y1 + 36, ask, 18, RED, weight="800"))
    lab = "bar model: %s in %d equal parts, %s parts shaded" % (plain(whole_txt) if whole_txt else "a bar", parts, num(shade))
    return svg_wrap(W, H, "".join(s), lab)


def grid_svg(rows, cols, k, cell=26):
    """rows x cols grid with the first k squares (row by row) shaded"""
    pad = 4
    W, H = cols * cell + 2 * pad, rows * cell + 2 * pad
    s = []
    for i in range(k):
        r, c = divmod(i, cols)
        s.append("<rect x='%d' y='%d' width='%d' height='%d' fill='%s'/>" % (pad + c * cell, pad + r * cell, cell, cell, FILL))
    for c in range(1, cols):
        s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='1.4'/>" % (pad + c * cell, pad, pad + c * cell, pad + rows * cell, THIN))
    for r in range(1, rows):
        s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='1.4'/>" % (pad, pad + r * cell, pad + cols * cell, pad + r * cell, THIN))
    s.append("<rect x='%d' y='%d' width='%d' height='%d' fill='none' stroke='%s' stroke-width='2.5'/>" % (pad, pad, cols * cell, rows * cell, LINE))
    return svg_wrap(W, H, "".join(s), "grid of %d squares with %d shaded" % (rows * cols, k))


def simple_bar(p, n, unit=""):
    """bar for 50%, 25% or 10% of n: each part labelled with its percentage"""
    parts = 100 // p
    return bar_svg(parts, 1, num(n) + unit, [(i + 0.5, "%d%%" % p) for i in range(parts)])


# ------------------------------------------------------------ explanations
def build_e(p, n, u=""):
    """Steps to find p% of n from 10%, 5% and 1% (or 50% and 25%). u: unit text after numbers."""
    p, n = F(p), F(n)
    r = p * n / 100
    t = n / 10
    o = n / 100
    N = lambda x: num(x) + u
    if p == 50:
        return "50%% is a half, so divide by 2: %s ÷ 2 = <b>%s</b>." % (N(n), N(r))
    if p == 25:
        return "25%% is a quarter, so divide by 4: %s ÷ 4 = <b>%s</b>." % (N(n), N(r))
    if p == 75:
        h = n / 2
        return ("50%% is %s ÷ 2 = %s. 25%% is half of that: %s. 75%% = 50%% + 25%% = %s + %s = <b>%s</b>."
                % (N(n), N(h), N(h / 2), N(h), N(h / 2), N(r)))
    if p == 10:
        return "10%% is a tenth, so divide by 10: %s ÷ 10 = <b>%s</b>." % (N(n), N(r))
    if p == 1:
        return "1%% is a hundredth, so divide by 100: %s ÷ 100 = <b>%s</b>." % (N(n), N(r))
    if p == 5:
        return "10%% of %s is %s. 5%% is half of 10%%: <b>%s</b>." % (N(n), N(t), N(r))
    if p in (90, 95, 99):
        d = 100 - p
        dd = n * d / 100
        how = {10: "10%% is %s ÷ 10 = %s" % (N(n), N(dd)),
               5: "10%% is %s, so 5%% is %s" % (N(t), N(dd)),
               1: "1%% is %s ÷ 100 = %s" % (N(n), N(dd))}[d]
        return ("%s%% = 100%% %s %d%%. %s. %s %s %s = <b>%s</b>."
                % (num(p), MINUS, d, how, N(n), MINUS, N(dd), N(r)))
    tens, rest = divmod(int(p), 10)
    steps, terms, names = ["10%% of %s is %s ÷ 10 = %s." % (N(n), N(n), N(t))], [], []
    if tens:
        if tens > 1:
            steps.append("%d0%% = %d × %s = %s." % (tens, tens, N(t), N(tens * t)))
        terms.append(tens * t)
        names.append("%d0%%" % tens)
    if rest == 5:
        steps.append("5%% is half of 10%%: %s." % N(t / 2))
        terms.append(t / 2)
        names.append("5%")
    elif rest:
        steps.append("1%% is %s ÷ 100 = %s%s." % (N(n), N(o), "" if rest == 1 else ", so %d%% = %d × %s = %s" % (rest, rest, N(o), N(rest * o))))
        terms.append(rest * o)
        names.append("%d%%" % rest)
    assert terms and sum(terms) == r, (p, n)
    if len(terms) == 1:
        last = steps[-1]
        k = last.rfind("= " + N(r) + ".")
        assert k >= 0, (p, n, last)
        steps[-1] = last[:k] + "= <b>%s</b>." % N(r)
        return " ".join(steps)
    steps.append("%s%% = %s = %s = <b>%s</b>." % (num(p), " + ".join(names), " + ".join(N(x) for x in terms), N(r)))
    return " ".join(steps)


# ============================================================ set 1: 50%, 25%, 10%, 1%
def set_simple(rnd):
    its = []
    for p, n, wr, note in [
            (50, 84, [168, 34, F("8.4")], "Do not double, and do not take away 50."),
            (25, 60, [45, F("2.4"), 30], "Not 60 ÷ 25: 25% is one quarter. 45 is the other 75%."),
            (10, 70, [F("0.7"), 60, 700], "10% means divide by 10, not by 100, and not take away 10."),
            (25, 120, [90, F("4.8"), 60], "60 is 50%. 25% is half of that."),
            (10, 450, [F("4.5"), 440, 405], "4.5 is 1%. 405 is the other 90%.")]:
        r = F(p * n, 100)
        q = fig(simple_bar(p, n)) + "The bar shows %s split into equal parts. What is <b>%d%%</b> of %s?" % (num(n), p, num(n))
        its.append(nmcq(q, r, wr, build_e(p, n) + " " + note))

    for p, n, wr, note in [
            (10, 90, [F("0.9"), 80, 81], "0.9 would be 1%. Do not take away 10."),
            (10, 3200, [32, 3190, 2880], "32 would be 1%. 2,880 is the other 90%."),
            (10, 46, [F("0.46"), 36, F("41.4")], "Move each digit one place to the right: 46 becomes 4.6."),
            (1, 500, [50, F("0.5"), 499], "1% means divide by 100, not by 10. Do not take away 1."),
            (1, 1200, [120, F("1.2"), 1199], "120 would be 10%."),
            (1, 350, [35, F("0.35"), 349], "35 would be 10%. Move each digit two places to the right."),
            (50, 2500, [5000, 2450, 250], "250 would be 10%. 5,000 is double, not half."),
            (50, 9, [18, F("0.9"), F("0.18")], "The answer does not have to be a whole number. Not 9 ÷ 50."),
            (25, 48, [36, 24, F("1.92")], "24 is 50%. A quarter is half of a half: 24 ÷ 2 = 12."),
            (25, 200, [8, 150, 175], "Not 200 ÷ 25 = 8, and not 200 " + MINUS + " 25."),
            (25, 10, [F("0.4"), F("7.5"), 5], "5 is 50%. Half of 5 is 2.5."),
            (1, 80, [8, F("0.08"), 79], "8 would be 10%."),
            (10, 5, [F("0.05"), 50, F("4.5")], "0.05 would be 1%. 10% is less than the number, not more.")]:
        r = F(p * n, 100)
        its.append(nmcq("What is <b>%d%%</b> of %s?" % (p, num(n)), r, wr, build_e(p, n) + " " + note))

    its.append(mcq("Which calculation finds <b>25% of 64</b>?", "64 ÷ 4", ["64 ÷ 25", "64 × 25", "64 %s 25" % MINUS],
                   "25%% is one quarter, so divide by 4: 64 ÷ 4 = 16. 64 ÷ 25 mixes up the 25 with the number of parts."))
    its.append(mcq("Which calculation finds <b>1% of 700</b>?", "700 ÷ 100", ["700 ÷ 10", "700 × 100", "700 %s 1" % MINUS],
                   "1%% is one hundredth, so divide by 100: 700 ÷ 100 = 7. 700 ÷ 10 = 70 is 10%%."))
    assert len(its) == 20, len(its)
    return {"title": "50%, 25%, 10% and 1% of an amount", "items": its}


# ============================================================ set 2: build from 10%, 5% and 1%
def set_build(rnd, P):
    its = []
    f15 = bar_svg(10, F(3, 2), "360", [(0.5, "36"), (1.25, "18"), (1.75, "18")] + [(i + 0.5, "36") for i in range(2, 10)],
                  ask="15% = ?", halves=(1,), W=540)
    its.append(nmcq(fig(f15) + "The bar shows 360 split into ten parts of 10%. What is <b>15%</b> of 360?",
                    54, [24, 5400, 345],
                    build_e(15, 360) + " Not 360 ÷ 15 = 24: that would split 360 into 15 parts. Not 15 × 360 either."))
    for p, n, wr, note in [
            (30, 250, [25, 220, 7500], "25 is only 10%. Do not take away 30."),
            (40, 65, [F("6.5"), 25, 39], "39 is the other 60%. Do not take away 40."),
            (5, 240, [48, 24, 235], "Not 240 ÷ 5 = 48: that is 20%. 24 is 10%."),
            (35, 80, [52, 115, 24], "24 is only 30%: add the 5% too. 52 is the other 65%."),
            (45, 120, [48, 66, 75], "48 is only 40%. 66 is the other 55%."),
            (60, 45, [18, F("0.75"), F("4.5")], "18 is the other 40%. 4.5 is only 10%."),
            (75, 36, [9, 18, F("0.48")], "9 is 25% and 18 is 50%. Add them to get 75%."),
            (75, 840, [210, 765, 420], "210 is only 25%. Do not take away 75."),
            (12, 300, [25, 288, 30], "Not 300 ÷ 12 = 25. 30 is only 10%: add 2% as well."),
            (3, 400, [120, F("1.2"), 397], "120 would be 30%. 1% is 4, not 0.4."),
            (99, 300, [3, 299, 270], "3 is the 1% you take away. Take away 1%, not 1."),
            (95, 60, [3, 55, 54], "3 is the 5% you take away. 54 is 90%."),
            (90, 70, [7, 60, 77], "7 is the 10% you take away. Do not take away 10."),
            (21, 600, [120, 6, 579], "120 is only 20%. Remember to add 1% (6)."),
            (15, 18, [F("1.2"), F("1.8"), F("0.9")], "Not 18 ÷ 15 = 1.2. 1.8 is only 10% and 0.9 is only 5%."),
            (65, 140, [49, 75, 84], "49 is the other 35%. 84 is only 60%."),
            (35, 260, [78, 169, 225], "78 is only 30%. 169 is the other 65%. Do not take away 35.")]:
        r = F(p * n, 100)
        its.append(nmcq("What is <b>%d%%</b> of %s?" % (p, num(n)), r, wr, build_e(p, n) + " " + note))

    n, he, his = P.next()
    its.append(nmcq("%s works out 15%% of 80 like this: 10%% of 80 is 8, so 15%% is 8 + 5 = 13. What is the correct answer?" % n,
                    12, [13, 15, 16],
                    "%s added 5, not 5%%. 10%% of 80 = 8. 5%% is half of 10%%: 4. 15%% = 8 + 4 = <b>12</b>." % n))
    its.append(mcq("Which is <b>not</b> a correct way to find 15% of 360?", "360 ÷ 15",
                   ["36 + 18", "3 × 18", "15 × 3.6"],
                   "10%% of 360 is 36 and 5%% is 18, so 15%% = 36 + 18 = 54. Also 3 × 5%% = 3 × 18 = 54, and 15 × 1%% = 15 × 3.6 = 54. "
                   "<b>360 ÷ 15</b> = 24 is wrong: it splits 360 into 15 equal parts."))
    assert len(its) == 20, len(its)
    return {"title": "Build percentages from 10%, 5% and 1%", "items": its}


# ============================================================ set 3: percentages of measures
def set_measures(rnd):
    its = []
    # (percent, amount, from-unit text, factor to small unit, small unit, wrongs, note)
    rows = [
        (20, 4, "kg", 1000, "g", [200, 80, 3200], "200 g is 4 kg ÷ 20. 80 g has the wrong place value: 0.8 kg = 800 g."),
        (30, F("2.5"), "m", 100, "cm", [F("7.5"), 750, 175], "0.75 m = 75 cm (1 m = 100 cm). 175 cm is the other 70%."),
        (10, 3, "litres", 1000, "ml", [30, 3000, 2700], "30 ml would be 1%. 1 litre = 1,000 ml, so 3 litres = 3,000 ml."),
        (50, F("1.5"), "km", 1000, "m", [75, 3000, 7500], "0.75 km = 750 m, because 1 km = 1,000 m. Half, not double."),
        (75, 1, "litre", 1000, "ml", [250, 75, 925], "250 ml is only 25%. Do not take away 75."),
        (15, 2, "m", 100, "cm", [20, 185, 300], "20 cm is only 10%. 1 m = 100 cm, not 1,000 cm."),
        (1, 5, "km", 1000, "m", [500, 5, F("0.05")], "500 m would be 10%. 0.05 is in km: 0.05 km = 50 m."),
        (35, 3, "kg", 1000, "g", [105, 1950, 900], "900 g is only 30%. 1,950 g is the other 65%."),
        (45, F("1.2"), "m", 100, "cm", [66, 48, F("5.4")], "48 cm is only 40%. 66 cm is the other 55%."),
        (65, 2, "litres", 1000, "ml", [700, 130, 1935], "700 ml is the other 35%. 1 litre = 1,000 ml."),
        (40, F("2.5"), "kg", 1000, "g", [100, 1500, 400], "1,500 g is the other 60%. 1 kg = 1,000 g."),
    ]
    for k, (p, a, fu, fac, su, wr, note) in enumerate(rows):
        small = a * fac
        r = F(p) * small / 100
        base = "%s %s = %s %s. " % (num(a), fu, num(small), su)
        q = "What is <b>%d%%</b> of %s %s? Give your answer in %s." % (p, num(a), fu,
                                                                    {"g": "grams", "cm": "centimetres", "m": "metres", "ml": "millilitres"}[su])
        if k in (0, 4):
            if p == 20:
                q = fig(bar_svg(5, 1, "4 kg = 4,000 g", [(i + 0.5, "20%") for i in range(5)])) + q
            else:
                q = fig(bar_svg(4, 3, "1 litre = 1,000 ml", [(i + 0.5, "25%") for i in range(4)], ask="75% = ?")) + q
        its.append(nmcq(q, r, wr, base + build_e(p, small, " " + su) + " " + note, unit=" " + su))

    for p, n, u, wr, note in [
            (5, 600, "g", [120, 60, 595], "120 g would be 20% (600 ÷ 5). 60 g is 10%."),
            (40, 80, "cm", [2, 48, 40], "Not 80 ÷ 40, and not 80 " + MINUS + " 40. 48 cm is the other 60%."),
            (60, 250, "ml", [100, 190, 25], "100 ml is the other 40%. 25 ml is only 10%."),
            (12, 50, "kg", [5, 38, F("0.6")], "5 kg is only 10%: add 2% (1 kg) as well."),
            (8, 750, "ml", [600, 75, 742], "600 ml would be 80%. 75 ml is 10%.")]:
        r = F(p * n, 100)
        its.append(nmcq("What is <b>%d%%</b> of %s %s?" % (p, num(n), u), r, wr, build_e(p, n, " " + u) + " " + note, unit=" " + u))

    its.append(nmcq("What is <b>25%</b> of 1 hour? Give your answer in minutes.", 15, [25, 45, F("2.4")],
                    "1 hour = 60 minutes. 25%% is a quarter: 60 ÷ 4 = <b>15 minutes</b>. An hour has 60 minutes, not 100, "
                    "so 25%% is not 25 minutes. 45 minutes is 75%%.", unit=" minutes"))
    its.append(nmcq("What is <b>90%</b> of 2 hours? Give your answer in minutes.", 108, [12, 90, 180],
                    "2 hours = 120 minutes. 10%% is 12 minutes, so 90%% = 120 %s 12 = <b>108 minutes</b>. "
                    "12 minutes is the 10%% you take away." % MINUS, unit=" minutes"))
    its.append(mcq("Which is more: 20% of 3 kg or 70% of 800 g?", "20% of 3 kg",
                   ["70% of 800 g", "They are equal", "You can’t tell"],
                   "20%% of 3 kg: 3 kg = 3,000 g, 10%% is 300 g, so 20%% is 600 g. "
                   "70%% of 800 g: 10%% is 80 g, so 70%% is 560 g. 600 g &gt; 560 g, so <b>20%% of 3 kg</b> is more."))
    its.append(mcq("Which is the same as <b>30% of 2 m</b>?", "60 cm", ["6 cm", "30 cm", "140 cm"],
                   "2 m = 200 cm. 10%% of 200 cm is 20 cm, so 30%% is 3 × 20 = <b>60 cm</b>. "
                   "6 cm uses 1 m = 10 cm. 140 cm is the other 70%%."))
    for it in its:
        it["e"] = it["e"].replace("%%", "%")
    # spot checks of the hand-written answers
    assert F(20, 100) * 3000 == 600 and F(70, 100) * 800 == 560 and F(30, 100) * 200 == 60
    assert F(25, 100) * 60 == 15 and F(90, 100) * 120 == 108
    assert len(its) == 20, len(its)
    return {"title": "Percentages of measures: kg, m, litres and time", "items": its}


# ============================================================ set 4: what percentage is it?
def out_of_e(part, n):
    p = F(part * 100, n)
    assert p.denominator == 1, (part, n)
    m = F(100, n)
    if m.denominator == 1:
        return ("Make the total 100. Multiply the top and bottom by %s: %s = %s = <b>%s%%</b>."
                % (num(m), fr(part, n), fr(num(p), 100), num(p)))
    g = n // 100 if n % 100 == 0 else None
    if g:
        return ("Divide the top and bottom by %d to make the total 100: %s = %s = <b>%s%%</b>."
                % (g, fr(part, n), fr(num(p), 100), num(p)))
    # e.g. 60/240 = 1/4 = 25/100
    from math import gcd
    k = gcd(part, n)
    a, b = part // k, n // k
    assert 100 % b == 0
    return ("Simplify, then make the total 100: %s = %s = %s = <b>%s%%</b>."
            % (fr(part, n), fr(a, b), fr(num(p), 100), num(p)))


def set_what(rnd, P):
    its = []
    for part, n, wr, note in [
            (12, 50, [12, 38, 76], "12% would be 12 out of 100. 76% is the part that is not 12 out of 50."),
            (7, 10, [7, 30, F("0.7")], "7 out of 10 is 7 tenths, and each tenth is 10%."),
            (9, 20, [9, 11, 55], "9% would be 9 out of 100. 55% is the other part."),
            (3, 4, [34, 3, 25], "Do not write the 3 and the 4 together. 25% is the other quarter."),
            (18, 25, [18, 7, 28], "18% would be 18 out of 100. 28% is the other part."),
            (1, 5, [15, 5, 80], "Do not write the 1 and the 5 together. 5% would be 1 out of 20."),
            (45, 300, [45, 85, F("4.5")], "45% would be 45 out of 100. 85% is the other part."),
            (6, 200, [6, 30, 97], "6% would be 6 out of 100. The total here is 200, so halve: 3 out of 100."),
            (27, 30, [27, 10, 3], "10% is the part that is not 27 out of 30."),
            (13, 20, [13, 35, 33], "Do not add 13 and 20. 35% is the other part."),
            (14, 40, [14, 26, 65], "26 is 40 " + MINUS + " 14, not a percentage. 65% is the other part."),
            (60, 240, [60, 75, 4], "60% would be 60 out of 100. 240 ÷ 60 = 4 tells you it is a quarter, not 4%.")]:
        p = F(part * 100, n)
        its.append(nmcq("What percentage is <b>%d out of %s</b>?" % (part, num(n)), p, wr, out_of_e(part, n) + " " + note, kind="pct"))

    its.append(nmcq(fig(bar_svg(10, 3, None, [], ask="")) + "What percentage of the bar is shaded?", 30, [3, 70, F("0.3")],
                    "The bar has 10 equal parts and 3 are shaded: %s = %s = <b>30%%</b>. Each part is 10%%, not 1%%. "
                    "70%% is the part that is not shaded." % (fr(3, 10), fr(30, 100)), kind="pct"))
    its.append(nmcq(fig(grid_svg(4, 5, 7)) + "What percentage of the grid is shaded?", 35, [7, 65, 70],
                    "7 of the 20 squares are shaded. Multiply the top and bottom by 5: %s = %s = <b>35%%</b>. "
                    "There are 20 squares, not 100, so it is not 7%%. 65%% is not shaded." % (fr(7, 20), fr(35, 100)), kind="pct"))

    its.append(mcq("Which is greater: %s or 65%%?" % fr(3, 5), "65%", [fr(3, 5), "They are equal", "You can’t tell"],
                   "%s = %s = 60%%. 65%% &gt; 60%%, so <b>65%%</b> is greater." % (fr(3, 5), fr(60, 100))))
    its.append(mcq("Which is the largest?", fr(3, 4), ["0.7", "72%", "69%"],
                   "Change them all to percentages: 0.7 = 70%%, %s = 75%%. 75%% is the largest, so <b>%s</b>." % (fr(3, 4), fr(3, 4))))

    its.append(mcq("Which is the smallest?", "38%", [fr(2, 5), "0.45", fr(1, 2)],
                   "Change them all to percentages: %s = 40%%, 0.45 = 45%%, %s = 50%%. The smallest is <b>38%%</b>."
                   % (fr(2, 5), fr(1, 2))))
    assert F(12, 20) == F(60, 100) and F(14, 25) == F(56, 100)
    its.append(mcq("Team A won 12 out of 20 matches. Team B won 14 out of 25 matches. Which team won the higher percentage of its matches?",
                   "Team A", ["Team B", "They are equal", "You can’t tell"],
                   "Team A: %s = %s = 60%%. Team B: %s = %s = 56%%. 60%% &gt; 56%%, so <b>Team A</b>, "
                   "even though Team B won more matches." % (fr(12, 20), fr(60, 100), fr(14, 25), fr(56, 100))))

    n, he, his = P.next()
    assert F(17, 20) == F(85, 100) and F(22, 25) == F(88, 100) and F(43, 50) == F(86, 100)
    its.append(mcq("%s scored 17 out of 20 in maths, 22 out of 25 in science and 43 out of 50 in English. "
                   "In which test did %s get the highest percentage?" % (n, he),
                   "Science", ["Maths", "English", "They are all equal"],
                   "Maths: %s = %s = 85%%. Science: %s = %s = 88%%. English: %s = %s = 86%%. "
                   "<b>Science</b> is highest, even though English has the most marks."
                   % (fr(17, 20), fr(85, 100), fr(22, 25), fr(88, 100), fr(43, 50), fr(86, 100))))
    a, _, _ = P.next()
    b, _, _ = P.next()
    assert F(18, 20) == F(45, 50)
    its.append(mcq("%s got 18 out of 20 in a quiz. %s got 45 out of 50 in a different quiz. Who got the higher percentage?" % (a, b),
                   "They are equal", [a, b, "You can’t tell"],
                   "%s: %s = %s = 90%%. %s: %s = %s = 90%%. The percentages are <b>equal</b>, "
                   "even though %s has more marks." % (a, fr(18, 20), fr(90, 100), b, fr(45, 50), fr(90, 100), b)))
    for it in its:
        it["e"] = it["e"].replace("%%", "%")
    assert len(its) == 20, len(its)
    return {"title": "What percentage is it? Compare with percentages", "items": its}


# ============================================================ set 5: word problems
def set_words(rnd, P):
    its = []
    M = "money"

    assert 60 - F(25, 100) * 60 == 45
    its.append(nmcq("A coat costs £60. In the sale it is 25% off. What is the sale price?", 45, [15, 35, 75],
                    "25%% is a quarter: £60 ÷ 4 = £15 off. Sale price: £60 %s £15 = <b>£45</b>. "
                    "£15 is the discount, not the price. Do not take away 25." % MINUS, kind=M))

    assert F(15, 100) * 80 == 12
    its.append(nmcq("Trainers cost £80. They are 15% off. How much money is taken off?", 12, [68, 65, 8],
                    "10%% of £80 is £8 and 5%% is £4, so 15%% is <b>£12</b>. £68 is the sale price, not the money taken off.", kind=M))

    assert 45 - F(20, 100) * 45 == 36
    its.append(nmcq("A video game costs £45. It is reduced by 20%. What is the new price?", 36, [9, 25, F("40.5")],
                    "10%% of £45 is £4.50, so 20%% is £9. New price: £45 %s £9 = <b>£36</b>. "
                    "£40.50 only takes off 10%%. Do not take away 20." % MINUS, kind=M))

    n, he, his = P.next()
    assert F(20, 100) * 45 == 9
    its.append(mcq("%s wants a £45 game. One shop offers 20%% off. Another shop offers £10 off. Which is the better offer?" % n,
                   "£10 off", ["20% off", "They are the same", "You can’t tell"],
                   "20%% of £45 = £9 off. £10 off saves more than £9, so <b>£10 off</b> is the better offer. "
                   "20%% is not the same as £20 or £10."))

    assert F(25, 100) * 36 == 9 and 36 - 9 == 27 and 36 - 8 == 28
    its.append(mcq("Jeans cost £36 in two shops. Shop A takes 25% off. Shop B takes £8 off. Which shop is cheaper now?",
                   "Shop A", ["Shop B", "They cost the same", "You can’t tell"],
                   "Shop A: 25%% of £36 = £9 off, so £27. Shop B: £36 %s £8 = £28. £27 &lt; £28, so <b>Shop A</b> is cheaper." % MINUS))

    assert 240 - F(30, 100) * 240 == 168
    its.append(nmcq("A bike was £240. The price is reduced by 30%. What is the new price?", 168, [72, 210, 216],
                    "10%% of £240 is £24, so 30%% is £72 off. New price: £240 %s £72 = <b>£168</b>. "
                    "£72 is the discount. £216 only takes off 10%%." % MINUS, kind=M))

    assert F(10, 50) * 100 == 20
    its.append(nmcq("A jumper cost £50. In the sale it costs £40. What percentage has been taken off?", 20, [10, 80, 25],
                    "£10 has been taken off. %s = %s = <b>20%%</b>. The £10 is not 10%%. "
                    "Compare with the old price (£50), not the new price (£40)." % (fr(10, 50), fr(20, 100)), kind="pct"))

    assert 300 + F(5, 100) * 300 == 315
    its.append(nmcq("A tablet costs £300. The price goes up by 5%. What is the new price?", 315, [15, 305, 285],
                    "10%% of £300 is £30, so 5%% is £15. The price goes <b>up</b>: £300 + £15 = <b>£315</b>. "
                    "Do not add £5, and do not take the £15 away.", kind=M))

    n, he, his = P.next()
    assert F(10, 100) * 8 * 4 == F(32, 10)
    its.append(mcq("%s saves 10%% of %s £8 pocket money each week. How much does %s save in 4 weeks?" % (n, his, he),
                   "£3.20", ["80p", "£32", "32p"],
                   "10%% of £8 is 80p each week. In 4 weeks: 4 × 80p = 320p = <b>£3.20</b>. "
                   "80p is only one week."))

    assert F(75, 100) * 24 == 18
    its.append(nmcq("A school trip costs £24. Parents pay 75% and the school pays the rest. How much do parents pay?", 18, [6, 12, 51],
                    "50%% of £24 is £12 and 25%% is £6, so 75%% is £12 + £6 = <b>£18</b>. £6 is what the school pays.", kind=M))

    assert F(35, 100) * 200 == 70
    its.append(nmcq("In a survey, 200 pupils chose their favourite sport. 35% chose football. How many pupils chose football?",
                    70, [35, 130, 165],
                    "10%% of 200 is 20, so 30%% is 60, and 5%% is 10. 35%% = 60 + 10 = <b>70</b> pupils. "
                    "35 would be 35 out of 100, but there are 200 pupils."))

    assert F(45, 100) * 80 == 36
    its.append(nmcq("80 children were asked about their favourite fruit. 45% chose apples. How many children chose apples?",
                    36, [44, 35, 45],
                    "10%% of 80 is 8, so 40%% is 32, and 5%% is 4. 45%% = 32 + 4 = <b>36</b> children. "
                    "44 is the other 55%%."))

    assert 60 - F(45, 100) * 60 == 33
    its.append(nmcq("There are 60 pupils in Year 6. 45% of them are girls. How many boys are there?", 33, [27, 15, 55],
                    "45%% of 60: 10%% is 6, 40%% is 24, 5%% is 3, so 27 girls. Boys: 60 %s 27 = <b>33</b>. "
                    "(Or 55%% of 60 = 33.) 27 is the number of girls." % MINUS))

    n, he, his = P.next()
    assert F(34, 40) * 100 == 85
    its.append(nmcq("%s scored 34 out of 40 in a spelling test. What percentage did %s score?" % (n, he), 85, [34, 15, 74],
                    "%s: divide the top and bottom by 4 to get %s, then multiply the top and bottom by 5: %s = <b>85%%</b>. "
                    "15%% is the part %s got wrong." % (fr(34, 40), fr(17, 20), fr(85, 100), he), kind="pct"))

    n, he, his = P.next()
    assert F(18, 25) * 100 == 72 and F(34, 50) * 100 == 68
    its.append(mcq("%s scored 18 out of 25 in maths and 34 out of 50 in science. In which test did %s get the higher percentage?" % (n, he),
                   "Maths", ["Science", "They are equal", "You can’t tell"],
                   "Maths: %s = %s = 72%%. Science: %s = %s = 68%%. 72%% &gt; 68%%, so <b>maths</b>, "
                   "even though science has more marks." % (fr(18, 25), fr(72, 100), fr(34, 50), fr(68, 100))))

    n, he, his = P.next()
    assert 250 - F(40, 100) * 250 == 150
    its.append(nmcq("A cake recipe uses 250 g of sugar. %s uses 40%% less sugar. How much sugar does %s use?" % (n, he),
                    150, [100, 210, 350],
                    "10%% of 250 g is 25 g, so 40%% is 100 g. %s uses 250 g %s 100 g = <b>150 g</b>. "
                    "100 g is the sugar left out, not the sugar used." % (n, MINUS), unit=" g"))

    assert F(60, 100) * 750 == 450
    its.append(nmcq("A smoothie is 60% milk. How much milk is in 750 ml of smoothie?", 450, [300, 690, 75],
                    "10%% of 750 ml is 75 ml, so 60%% is 6 × 75 = <b>450 ml</b>. 300 ml is the other 40%%. "
                    "Do not take away 60.", unit=" ml"))

    n, he, his = P.next()
    assert F(30, 100) * 1500 == 450
    its.append(nmcq("%s has a 1.5 litre bottle of water. %s drinks 30%% of it. How much water does %s drink?" % (n, he.capitalize(), he),
                    450, [45, 1050, 1470],
                    "1.5 litres = 1,500 ml. 10%% is 150 ml, so 30%% is <b>450 ml</b>. 1,050 ml is what is left.",
                    unit=" ml"))

    assert F(85, 100) * 40000 == 34000
    its.append(nmcq("A football stadium holds 40,000 people. It is 85% full. How many people are in the stadium?",
                    34000, [6000, 39915, 3400],
                    "10%% of 40,000 is 4,000, so 80%% is 32,000, and 5%% is 2,000. 85%% = 32,000 + 2,000 = <b>34,000</b>. "
                    "6,000 is the number of empty seats."))

    n, he, his = P.next()
    assert F(1, 100) * 3000 * 4 == 120
    its.append(nmcq("A charity needs £3,000. %s raises 4%% of it. How much does %s raise?" % (n, he), 120, [12, 1200, 750],
                    "1%% of £3,000 is £30, so 4%% is 4 × £30 = <b>£120</b>. £1,200 would be 40%%. "
                    "Not £3,000 ÷ 4 = £750.", kind=M))
    for it in its:
        it["e"] = it["e"].replace("%%", "%")
    assert len(its) == 20, len(its)
    return {"title": "Percentage word problems: sales, surveys, tests and recipes", "items": its}


# ============================================================ lesson
def body_html():
    f_whole = bar_svg(10, 0, "360", [(i + 0.5, "36") for i in range(10)], ask="", W=540)
    f15 = bar_svg(10, F(3, 2), "360", [(0.5, "36"), (1.25, "18"), (1.75, "18")] + [(i + 0.5, "36") for i in range(2, 10)],
                  ask="15% = 36 + 18 = 54", halves=(1,), W=540)
    f_out = grid_svg(5, 10, 12, cell=24)
    return (
        "<h2>Per cent means “out of 100”</h2>"
        "<p>A <b>percentage</b> is a number out of 100. 100% is the whole amount. 50% is a half, 25% is a quarter, "
        "10% is a tenth and 1% is a hundredth.</p>"
        + table(["Percentage", "Fraction", "How to find it"], [
            ["50%", fr(1, 2), "÷ 2"],
            ["25%", fr(1, 4), "÷ 4"],
            ["10%", fr(1, 10), "÷ 10"],
            ["5%", fr(1, 20), "half of 10%"],
            ["1%", fr(1, 100), "÷ 100"],
        ]) +
        "<h2>Build any percentage from 10%, 5% and 1%</h2>"
        "<p>Find 10% first. Then put the pieces together.</p>"
        "<figure class='sn-fig'>" + f_whole +
        "<figcaption>360 in ten equal parts: each part is 10% = 36.</figcaption></figure>"
        + ex("Example", "Find 15% of 360.",
             "10% of 360 = 36. 5% is half of 10% = 18. 15% = 10% + 5% = 36 + 18.", "54")
        + "<figure class='sn-fig'>" + f15 +
        "<figcaption>15% is one part of 10% and half a part (5%).</figcaption></figure>"
        + ex("Example", "Find 35% of 80.", "10% = 8, so 30% = 24. 5% = 4. 35% = 24 + 4.", "28")
        + ex("Example", "Find 99% of 300.", "1% of 300 = 3. 99% = 100% " + MINUS + " 1% = 300 " + MINUS + " 3.", "297")
        + "<h2>Percentages of measures and money</h2>"
        "<p>Change to a smaller unit first if it helps: 20% of 4 kg = 20% of 4,000 g = 800 g.</p>"
        + ex("Example", "A coat costs £60. It is 25% off. What is the sale price?",
             "25% of £60 = £60 ÷ 4 = £15 off. £60 " + MINUS + " £15.", "£45")
        + "<h2>What percentage is it?</h2>"
        "<p>Write a fraction, then make the total 100.</p>"
        "<figure class='sn-fig'>" + f_out +
        "<figcaption>12 out of 50 squares: " + fr(12, 50) + " = " + fr(24, 100) + " = 24%.</figcaption></figure>"
        "<p>To compare test results, change each score to a percentage: 17 out of 20 = 85% is better than 42 out of 50 = 84%.</p>"
        + "<h2>Common mistakes</h2>"
        + table(["Mistake", "What to do instead"], [
            ["15% of 360 = 360 ÷ 15 = 24", "10% = 36, 5% = 18, so 15% = 54"],
            ["10% of 70 = 70 ÷ 100 = 0.7", "10% means ÷ 10: 7. 1% means ÷ 100"],
            ["15% of 80 = 8 + 5 = 13", "5% is half of 10%: 8 + 4 = 12"],
            ["25% off £60 = £15, so it costs £15", "£15 is the discount. The sale price is £60 " + MINUS + " £15 = £45"],
            ["12 out of 50 = 12%", "Make the total 100: " + fr(12, 50) + " = " + fr(24, 100) + " = 24%"],
        ])
    )


FAQ = [
    {"q": "How do you find a percentage of an amount in Year 6?",
     "a": "Find 10% by dividing by 10 and 1% by dividing by 100, then build the percentage you need. For example, 30% of 250 is 3 × 25 = 75."},
    {"q": "How do you work out 15% of 360?",
     "a": "10% of 360 is 36 and 5% is half of that, 18. So 15% = 36 + 18 = 54. Do not divide 360 by 15."},
    {"q": "Are percentages in the Year 6 SATs?",
     "a": "Yes. Percentages of amounts appear on the arithmetic paper (for example 35% of 260) and in reasoning questions about sales, surveys and test scores."},
    {"q": "How do you work out what percentage one number is of another?",
     "a": "Write it as a fraction and make the total 100. 12 out of 50 = 12/50 = 24/100 = 24%."},
]


def gen():
    rnd = random.Random(6611)
    P = People(rnd)
    sets = [set_simple(rnd), set_build(rnd, P), set_measures(rnd), set_what(rnd, P), set_words(rnd, P)]
    for s in sets:
        for it in s["items"]:
            it["e"] = it["e"].replace("%%", "%")
    balance(sets, rnd)
    seen = set()
    for s in sets:
        assert len(s["items"]) == 20, (s["title"], len(s["items"]))
        assert sorted(it["a"] for it in s["items"]) == sorted([0, 1, 2, 3] * 5)
        for it in s["items"]:
            assert len(set(it["c"])) == 4, it
            assert it["q"] not in seen, it["q"]
            assert "%%" not in it["e"] and "%%" not in it["q"], it
            assert len(re.findall("<svg", it["q"])) <= 1
            seen.add(it["q"])
    u = {
        "country": "uk", "subject": "maths", "grade": "year-6", "slug": "percentages-of-amounts", "sort": 11,
        "updated": UPDATED, "pdf_url": "",
        "title": "Percentages of Amounts: 10%, 15% of 360 and Percentage Problems",
        "seo_title": "Year 6 Percentages of Amounts Worksheets: Find 10%, 25%, 15% of 360, Measures and Sale Prices",
        "short_title": "Percentages of amounts",
        "domain": "Ratio and proportion",
        "standard_code": "Year 6: Ratio and proportion",
        "standard_url": "https://www.gov.uk/government/publications/national-curriculum-in-england-mathematics-programmes-of-study",
        "standard_text": "Solve problems involving the calculation of percentages [for example, of measures, and such as 15% of 360] and the use of percentages for comparison.",
        "meta_desc": "Free Year 6 maths worksheets on percentages of amounts: find 50%, 25%, 10% and 1%, build 15% of 360 from 10% and 5%, find percentages of measures, work out 12 out of 50 as a percentage and solve sale price problems. 100 questions with an answer key, following the National Curriculum.",
        "key_big": "Find 10% (÷ 10) and 1% (÷ 100), then build: 15% of 360 = 36 + 18 = 54.",
        "key_sub": "5% is half of 10%, and 99% is 100% − 1%. To find what percentage a part is, make the total 100: 12 out of 50 = 24/100 = 24%.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }
    return mark_large(u, "(bar model|grid of)")


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
