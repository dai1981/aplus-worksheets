# -*- coding: utf-8 -*-
"""
AU Year 5 Maths: Percentages
(Australian Curriculum v9.0, AC9M5N04)
  python3 tools/gen_au_maths_y5_percentages.py
Percent as parts of 100 (hundred squares); 100% is the complete whole; familiar equivalences
(50%, 25%, 75%, 10%, 20%, 1% and their fractions and decimals); comparing relative size; real contexts.
Percent of a quantity is Year 6, so only very simple ones appear (50% of 40, 10% of 50).
Every answer is checked with fractions.Fraction (never float).
Australian English, dollars and cents, metric units. HTML attributes use single quotes (no backslashes in the JSON).
"""
import json, os, random, re
from decimal import Decimal as Dm
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "au", "maths", "year-5")
UPDATED = "2026-11-02"
FILL = "#4fae74"
FILL2 = "#4a7fd4"
LINE = "#2b2b2b"
THIN = "#8a8a8a"
RED = "#d6453b"
WATER = "#6aaee0"
FONT = "Arial, Helvetica, sans-serif"
GIRLS = ["Charlotte", "Isla", "Mia", "Amelia", "Ava", "Harper", "Chloe", "Ruby", "Mei", "Zara", "Matilda", "Sienna", "Grace"]
BOYS = ["Oliver", "Jack", "Noah", "William", "Leo", "Lachlan", "Liam", "Aarav", "Kai", "Cooper", "Ethan"]


# ------------------------------------------------------------ helpers
def fr(a, b):
    return "<span class='fr'><span class='fn'>%s</span><span class='fd'>%s</span></span>" % (a, b)


FRX = re.compile(r"^<span class='fr'><span class='fn'>(\d+)</span><span class='fd'>(\d+)</span></span>( .+)?$")
NUM = re.compile(r"^(\$)?(\d*\.?\d+)(%|c)?( .+)?$")


def val(c):
    """Value of a choice (Fraction, unit). 20% is 1/5 with unit '' so 20% and 0.2 count as equal.
    None for choices that are not a single number."""
    m = FRX.match(c)
    if m:
        return (F(int(m.group(1)), int(m.group(2))), (m.group(3) or "").strip())
    m = NUM.match(c)
    if not m:
        return None
    v = F(m.group(2))
    if m.group(1):
        return (v, "$")
    if m.group(3) == "c":
        return (v / 100, "$")
    if m.group(3) == "%":
        v = v / 100
    return (v, (m.group(4) or "").strip())


def v(c):
    """Plain value of a number choice (fraction, decimal or percentage)."""
    r = val(c)
    assert r is not None and r[1] == "", c
    return r[0]


def mcq(q, correct, wrong, e, same_ok=False, fixed=False):
    """4 choices: correct first + 3 wrong, positions set by balance(). fixed=True keeps the order given
    (A, B, C, D picture labels); then `correct` is the index of the answer and `wrong` is the full list."""
    if fixed:
        ch = [str(x) for x in wrong]
        assert len(ch) == 4
        it = {"q": q, "c": ch, "a": correct, "e": e, "fixed": True}
        return it
    correct = str(correct)
    wrong = [str(x) for x in wrong]
    assert len(wrong) == 3, (q, wrong)
    ch = [correct] + wrong
    assert len(set(re.sub(r"<[^>]+>", "", x) for x in ch)) == 4, (q, ch)
    if not same_ok:
        vs = [val(x) for x in ch]
        known = [x for x in vs if x is not None]
        assert len(set(known)) == len(known), (q, ch)
    return {"q": q, "c": ch, "a": 0, "e": e}


def balance(sets, rnd):
    """Spread the correct answers evenly over the 4 positions in every set (5 each). Fixed items keep their order."""
    for s in sets:
        targets = [0, 1, 2, 3] * 5
        for it in s["items"]:
            if it.get("fixed"):
                targets.remove(it["a"])
        rnd.shuffle(targets)
        k = 0
        for it in s["items"]:
            if it.pop("fixed", False):
                continue
            t = targets[k]
            k += 1
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


def text(x, y, t, fs=16, anchor="middle", col=LINE, weight=700):
    return ("<text x='%.1f' y='%.1f' font-size='%d' font-weight='%d' fill='%s' text-anchor='%s'>%s</text>"
            % (x, y, fs, weight, col, anchor, t))


def table(head, rows):
    h = "".join("<th>%s</th>" % x for x in head)
    b = "".join("<tr>" + "".join("<td>%s</td>" % c for c in r) + "</tr>" for r in rows)
    return "<div class='sn-tw'><table class='sn-table'><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>" % (h, b)


def ex(title, q, s, a):
    return ("<div class='sn-ex'><span class='sn-ex-t'>%s</span><p class='sn-ex-q'>%s</p>"
            "<p class='sn-ex-s'>%s</p><p class='sn-ex-a'>Answer: %s</p></div>" % (title, q, s, a))


def reorder(its, order):
    assert sorted(order) == list(range(len(its))), order
    return [its[i] for i in order]


# ------------------------------------------------------------ pictures
def grid_body(k, ox, oy, cell, k2=0):
    """10 x 10 hundred square at (ox, oy): k squares green, then k2 squares blue (full columns first, top to bottom)."""
    assert 0 <= k + k2 <= 100
    s = []
    for c in range(10):
        for r in range(10):
            i = c * 10 + r
            if i < k + k2:
                s.append("<rect x='%d' y='%d' width='%d' height='%d' fill='%s'/>"
                         % (ox + c * cell, oy + r * cell, cell, cell, FILL if i < k else FILL2))
    for i in range(1, 10):
        s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='1.2'/>"
                 % (ox + i * cell, oy, ox + i * cell, oy + 10 * cell, THIN))
        s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='1.2'/>"
                 % (ox, oy + i * cell, ox + 10 * cell, oy + i * cell, THIN))
    s.append("<rect x='%d' y='%d' width='%d' height='%d' fill='none' stroke='%s' stroke-width='2.5'/>"
             % (ox, oy, 10 * cell, 10 * cell, LINE))
    return "".join(s)


def grid_svg(k, cell=18, k2=0):
    pad = 4
    w = 10 * cell + 2 * pad
    lab = "hundred square with %d of 100 squares shaded green" % k
    if k2:
        lab += " and %d shaded blue" % k2
    return svg_wrap(w, w, grid_body(k, pad, pad, cell, k2), lab)


def grids4_svg(ks):
    """Four small hundred squares labelled A, B, C, D in one picture."""
    cell, gap, pad = 9, 22, 4
    side = 10 * cell
    W = 2 * pad + 4 * side + 3 * gap
    H = pad + side + 28
    o = []
    for i, k in enumerate(ks):
        x = pad + i * (side + gap)
        o.append(grid_body(k, x, pad, cell))
        o.append(text(x + side / 2.0, pad + side + 22, "ABCD"[i], 18))
    return svg_wrap(W, H, "".join(o), "four hundred squares labelled A to D")


def strip_svg(parts, shaded, W=400):
    """A bar from 0% to 100% split into equal parts, the first `shaded` parts filled."""
    L, R, T, Hh = 24, W - 24, 6, 40
    pw = (R - L) / float(parts)
    o = []
    for i in range(shaded):
        o.append("<rect x='%.1f' y='%d' width='%.1f' height='%d' fill='%s'/>" % (L + i * pw, T, pw, Hh, FILL))
    for i in range(1, parts):
        o.append("<line x1='%.1f' y1='%d' x2='%.1f' y2='%d' stroke='%s' stroke-width='1.8'/>"
                 % (L + i * pw, T, L + i * pw, T + Hh, LINE))
    o.append("<rect x='%d' y='%d' width='%d' height='%d' fill='none' stroke='%s' stroke-width='2.5'/>" % (L, T, R - L, Hh, LINE))
    o.append(text(L, T + Hh + 22, "0%", 16))
    o.append(text(R, T + Hh + 22, "100%", 16))
    return svg_wrap(W, T + Hh + 30, "".join(o), "percentage bar in %d equal parts with %d part%s shaded" % (parts, shaded, "" if shaded == 1 else "s"))


def battery_svg(lit, bars):
    """Battery with `bars` equal bars, `lit` of them green."""
    x0, y0, bw, gap, h = 6, 6, 44, 6, 56
    W_in = bars * bw + (bars + 1) * gap
    o = ["<rect x='%d' y='%d' width='%d' height='%d' rx='8' fill='#fff' stroke='%s' stroke-width='3'/>" % (x0, y0, W_in, h, LINE),
         "<rect x='%d' y='%d' width='10' height='22' rx='3' fill='%s'/>" % (x0 + W_in, y0 + h / 2 - 11, LINE)]
    for i in range(bars):
        o.append("<rect x='%d' y='%d' width='%d' height='%d' rx='3' fill='%s' stroke='%s' stroke-width='1.2'/>"
                 % (x0 + gap + i * (bw + gap), y0 + gap, bw, h - 2 * gap, FILL if i < lit else "#eeeeee", THIN))
    return svg_wrap(x0 + W_in + 16, h + 12, "".join(o), "battery with %d of %d bars green" % (lit, bars))


def tank_svg(quarters):
    """Water tank with marks at quarters, filled to `quarters` quarters."""
    x0, y0, w, h = 66, 14, 90, 120
    lvl = y0 + h - h * quarters / 4.0
    o = ["<rect x='%d' y='%.1f' width='%d' height='%.1f' fill='%s'/>" % (x0, lvl, w, y0 + h - lvl, WATER),
         "<rect x='%d' y='%d' width='%d' height='%d' fill='none' stroke='%s' stroke-width='3'/>" % (x0, y0, w, h, LINE),
         "<ellipse cx='%d' cy='%d' rx='%d' ry='6' fill='#fff' stroke='%s' stroke-width='2.5'/>" % (x0 + w / 2, y0, w / 2, LINE)]
    for q in range(1, 4):
        y = y0 + h - h * q / 4.0
        o.append("<line x1='%d' y1='%.1f' x2='%d' y2='%.1f' stroke='%s' stroke-width='2'/>" % (x0 - 10, y, x0, y, LINE))
    o.append(text(x0 - 14, y0 + 6, "Full", 14, anchor="end"))
    o.append(text(x0 - 14, y0 + h + 5, "Empty", 14, anchor="end"))
    return svg_wrap(x0 + w + 10, y0 + h + 10, "".join(o), "water tank with marks at each quarter, filled to %d quarter%s"
                    % (quarters, "" if quarters == 1 else "s"))


def P(n):
    """Text of a percentage choice."""
    return "%s%%" % n


# ============================================================ set 1: parts of 100
def set_parts():
    its = []
    its.append(mcq("What does <b>per cent</b> mean?", "out of 100", ["out of 10", "out of 1000", "out of 50"],
                   "“Per cent” means <b>out of 100</b>. 23% means 23 parts out of 100 equal parts."))
    for k, wrong, e in [
        (37, ["63%", "3.7%", "0.37%"], "37 of the 100 squares are shaded, so it is <b>37%</b>. 63% is the white part."),
        (60, ["6%", "40%", "0.6%"], "6 full columns of 10 are shaded: 60 of the 100 squares = <b>60%</b>. "
                                    "6% would be only 6 small squares."),
        (8, ["80%", "92%", "0.8%"], "8 of the 100 squares are shaded: <b>8%</b>. 80% would be 8 full columns."),
        (1, ["10%", "100%", "99%"], "Only 1 of the 100 squares is shaded: <b>1%</b>. 10% would be a full column."),
    ]:
        its.append(mcq(fig(grid_svg(k)) + "What percentage of the hundred square is shaded?", P(k), wrong, e))
    its.append(mcq(fig(grid_svg(52)) + "What percentage of the hundred square is <b>not</b> shaded?", "48%",
                   ["52%", "58%", "4.8%"],
                   "52 squares are shaded, so 100 − 52 = 48 squares are white: <b>48%</b>. "
                   "58% is a common slip: check 52 + 58 = 110, not 100."))
    its.append(mcq("Write <b>23%</b> as a fraction.", fr(23, 100), [fr(23, 10), fr(23, 1000), fr(1, 23)],
                   "Per cent means out of 100: 23%% = <b>%s</b>." % fr(23, 100)))
    its.append(mcq("Write <b>9%</b> as a fraction.", fr(9, 100), [fr(9, 10), fr(9, 1000), fr(1, 9)],
                   "9%% = 9 out of 100 = <b>%s</b>. %s would be 90%%." % (fr(9, 100), fr(9, 10))))
    its.append(mcq("Write %s as a percentage." % fr(71, 100), "71%", ["7.1%", "0.71%", "29%"],
                   "%s means 71 out of 100, so it is <b>71%%</b>." % fr(71, 100)))
    its.append(mcq("Write <b>45%</b> as a decimal.", "0.45", ["4.5", "0.045", "45"],
                   "45%% = %s = 45 hundredths = <b>0.45</b>." % fr(45, 100)))
    its.append(mcq("Write <b>7%</b> as a decimal.", "0.07", ["0.7", "7", "0.007"],
                   "7%% = %s = 7 hundredths. Hundredths are the second place after the point: <b>0.07</b>. "
                   "0.7 is 70%%." % fr(7, 100)))
    its.append(mcq("Write <b>0.29</b> as a percentage.", "29%", ["2.9%", "0.29%", "290%"],
                   "0.29 = 29 hundredths = %s = <b>29%%</b>." % fr(29, 100)))
    its.append(mcq("A box has 100 tiles. 13 of them are blue. What percentage of the tiles are blue?", "13%",
                   ["87%", "1.3%", "0.13%"],
                   "13 out of 100 = %s = <b>13%%</b>. 87%% are not blue." % fr(13, 100)))
    ks = [3, 30, 70, 33]
    its.append(mcq(fig(grids4_svg(ks)) + "Which hundred square shows <b>30%</b> shaded?", 1, ["A", "B", "C", "D"],
                   "30% = 30 out of 100 = 3 full columns of 10. That is <b>B</b>. A shows only 3%, C shows 70% "
                   "and D shows 33%.", fixed=True))
    its.append(mcq(fig(grid_svg(25)) + "Which shows the shaded part in three ways?",
                   "%s = 0.25 = 25%%" % fr(25, 100),
                   ["%s = 2.5 = 25%%" % fr(25, 100), "%s = 0.25 = 25%%" % fr(25, 10), "%s = 0.025 = 25%%" % fr(25, 100)],
                   "25 of 100 squares: %s = 25 hundredths = 0.25 = <b>25%%</b>." % fr(25, 100), same_ok=True))
    its.append(mcq("In a survey of 100 students, 64 like footy. What percentage like footy?", "64%",
                   ["36%", "6.4%", "0.64%"],
                   "64 out of 100 = %s = <b>64%%</b>. 36%% is the students who do not." % fr(64, 100)))
    its.append(mcq("1% of a hundred square is how many small squares?", "1", ["10", "100", "0.1"],
                   "The square has 100 small squares. 1% = 1 out of 100 = <b>1</b> small square."))
    n = "Mia"
    its.append(mcq(fig(grid_svg(70)) + "%s has shaded 70 squares. How many more squares must she shade to show <b>75%%</b>?" % n,
                   "5", ["75", "25", "30"],
                   "75% = 75 squares. 75 − 70 = <b>5</b> more squares. 30 is the number of white squares, not the squares to add."))
    its.append(mcq("Write %s as a percentage." % fr(6, 100), "6%", ["60%", "0.6%", "94%"],
                   "%s = 6 out of 100 = <b>6%%</b>. 60%% would be %s." % (fr(6, 100), fr(60, 100))))
    its.append(mcq("Which decimal is the same as <b>99%</b>?", "0.99", ["9.9", "0.099", "99"],
                   "99%% = %s = 99 hundredths = <b>0.99</b>. It is just less than 1 whole." % fr(99, 100)))
    order = [0, 1, 2, 3, 4, 16, 13, 12, 15, 6, 7, 8, 18, 9, 10, 11, 19, 14, 5, 17]
    return {"title": "Percent as parts of 100", "items": reorder(its, order)}


# ============================================================ set 2: 100% is the whole
def set_whole():
    its = []
    its.append(mcq(fig(grid_svg(100)) + "What percentage of the hundred square is shaded?", "100%",
                   ["10%", "1%", "0%"],
                   "All 100 squares are shaded: 100 out of 100 = <b>100%</b>. 100% is the whole."))
    its.append(mcq("<b>100%</b> of something means …", "the whole amount",
                   ["100 things", "half of it", "one hundredth of it"],
                   "100%% = %s = 1 whole. So 100%% is <b>the whole amount</b>, however many things there are."
                   % fr(100, 100)))
    its.append(mcq("Write <b>100%</b> as a decimal.", "1", ["0.1", "0.01", "100"],
                   "100%% = %s = <b>1</b> whole. 0.01 is only 1%%." % fr(100, 100)))
    for a, right, wrong, e in [
        (35, 65, [75, 55, "0.65"], "35% + 65% = 100%. Count on from 35 to 100: 5 to 40, then 60 to 100. "
                                   "So <b>65%</b>. 75% is a common slip: 35 + 75 = 110."),
        (80, 20, [30, 2, "0.2"], "80% + <b>20%</b> = 100%. Count on from 80 by tens: 90, 100. That is 2 tens = 20."),
        (42, 58, [68, 42, 142], "42 + 58 = 100, so the missing part is <b>58%</b>. Check: 42 + 68 = 110, not 100."),
        (7, 93, [3, 97, 107], "7 + 93 = 100, so the missing part is <b>93%</b>. 3% only makes 10%."),
    ]:
        assert a + right == 100
        its.append(mcq("%d%% + ? = 100%%" % a, P(right), [P(w) for w in wrong], e))
    its.append(mcq(fig(grid_svg(45, k2=30)) + "45% is green and 30% is blue. What percentage is <b>white</b>?",
                   "25%", ["75%", "55%", "70%"],
                   "Green and blue: 45% + 30% = 75%. The whole is 100%, so white is 100% − 75% = <b>25%</b>. "
                   "75% is the shaded part."))
    its.append(mcq(fig(grid_svg(36, k2=24)) + "What percentage of the hundred square is <b>not</b> shaded?",
                   "40%", ["60%", "36%", "24%"],
                   "Shaded: 36 + 24 = 60 squares. Not shaded: 100 − 60 = 40 squares = <b>40%</b>."))
    its.append(mcq("A class has 25 students. <b>100%</b> of the class go on the school excursion. How many students go?",
                   "25", ["100", "1", "75"],
                   "100% means the whole class, all <b>25</b> students. 100% does not mean 100 people."))
    its.append(mcq("Liam has read 100% of his 60-page book. How many pages has he read?", "60", ["100", "40", "6"],
                   "100% is the whole book: all <b>60</b> pages. 100% does not always mean 100 things."))
    its.append(mcq(fig(strip_svg(10, 7)) + "What percentage of the bar is shaded?", "70%", ["7%", "30%", "0.7%"],
                   "The whole bar is 100%, split into 10 equal parts. Each part is 10%. 7 parts = <b>70%</b>."))
    its.append(mcq(fig(strip_svg(4, 1)) + "What percentage of the bar is shaded?", "25%", ["14%", "4%", "75%"],
                   "The whole bar is 100%%, split into 4 equal parts. Each part is 100%% ÷ 4 = <b>25%%</b>. "
                   "%s = 25%%, not 14%%." % fr(1, 4)))
    its.append(mcq(fig(strip_svg(5, 2)) + "What percentage of the bar is shaded?", "40%", ["20%", "2%", "60%"],
                   "100% ÷ 5 = 20% for each part. 2 parts = 20% + 20% = <b>40%</b>. 60% is the white part."))
    its.append(mcq("Which pair makes <b>100%</b>?", "63% and 37%", ["63% and 47%", "60% and 30%", "37% and 73%"],
                   "63 + 37 = 100, so <b>63% and 37%</b> make the whole. 63 + 47 = 110 and 37 + 73 = 110.", same_ok=True))
    for x in ["63% and 37%", "63% and 47%", "60% and 30%", "37% and 73%"]:
        a, b = [int(t.strip(" %")) for t in x.split("and")]
        assert (a + b == 100) == (x == "63% and 37%")
    its.append(mcq("Which is <b>not</b> the same as the whole?", "10%", ["100%", "1", fr(100, 100)],
                   "The whole is 100%% = %s = 1. <b>10%%</b> is only one tenth of the whole." % fr(100, 100), same_ok=True))
    its.append(mcq("25% + 25% + 25% + 25% = ?", "100%", ["25%", "1%", "75%"],
                   "4 × 25% = <b>100%</b>. Four quarters make the whole."))
    its.append(mcq("Ruby has coloured 65% of her poster. What percentage is still to be coloured?", "35%",
                   ["45%", "65%", "165%"],
                   "The whole poster is 100%. 100% − 65% = <b>35%</b>. Check: 65 + 35 = 100."))
    its.append(mcq("Ava, Leo and Mei share a garden bed. Ava has 50%, Leo has 30% and Mei has the rest. "
                   "What percentage does Mei have?", "20%", ["30%", "80%", "10%"],
                   "Ava and Leo: 50% + 30% = 80%. The whole bed is 100%, so Mei has 100% − 80% = <b>20%</b>."))
    its.append(mcq("A cake is cut into 10 equal pieces. 4 pieces are eaten. What percentage of the cake is left?",
                   "60%", ["40%", "4%", "6%"],
                   "The whole cake is 100%. Each piece is 100% ÷ 10 = 10%. 6 pieces are left: <b>60%</b>. 40% was eaten."))
    order = [1, 0, 2, 15, 16, 4, 11, 3, 12, 5, 13, 6, 14, 7, 8, 9, 10, 17, 19, 18]
    return {"title": "100% is the whole", "items": reorder(its, order)}


# ============================================================ set 3: familiar equivalences
def set_equiv():
    its = []
    for (n, d), right, wrong, e in [
        ((1, 2), 50, [12, 2, 20], "%s = %s = <b>50%%</b>. Half of 100 is 50. Do not just write the digits 1 and 2."
         % (fr(1, 2), fr(50, 100))),
        ((1, 4), 25, [14, 4, 40], "4 × 25 = 100, so %s = %s = <b>25%%</b>." % (fr(1, 4), fr(25, 100))),
        ((3, 4), 75, [34, 25, 70], "%s = 25%%, so %s = 3 × 25%% = <b>75%%</b>. 25%% is the part that is left."
         % (fr(1, 4), fr(3, 4))),
        ((1, 10), 10, [1, 100, "0.1"], "10 × 10 = 100, so %s = %s = <b>10%%</b>." % (fr(1, 10), fr(10, 100))),
        ((1, 5), 20, [15, 5, 50], "5 × 20 = 100, so %s = %s = <b>20%%</b>. 15%% just writes the digits 1 and 5."
         % (fr(1, 5), fr(20, 100))),
        ((1, 100), 1, [100, 10, "0.01"], "%s means 1 out of 100 = <b>1%%</b>." % fr(1, 100)),
        ((3, 10), 30, [3, 70, 13], "%s = %s = <b>30%%</b>. 3%% would be %s." % (fr(3, 10), fr(30, 100), fr(3, 100))),
    ]:
        assert F(right) / 100 == F(n, d)
        its.append(mcq("Write %s as a percentage." % fr(n, d), P(right), [P(w) for w in wrong], e))
    for d_, right, wrong, e in [
        ("0.5", 50, [5, "0.5", 500], "0.5 = 5 tenths = 50 hundredths = <b>50%</b>. 5% would be 0.05."),
        ("0.4", 40, [4, "0.4", 400], "0.4 = 4 tenths = 40 hundredths = <b>40%</b>. 4% would be 0.04."),
        ("0.25", 25, ["2.5", 250, "0.25"], "0.25 = 25 hundredths = <b>25%</b>."),
    ]:
        assert F(Dm(d_)) == F(right) / 100
        its.append(mcq("Write <b>%s</b> as a percentage." % d_, P(right), [P(w) for w in wrong], e))
    for p_, right, wrong, e in [
        (75, "0.75", ["7.5", "0.075", "75"], "75%% = %s = <b>0.75</b>." % fr(75, 100)),
        (20, "0.2", ["0.02", "2", "0.5"], "20%% = %s = %s = <b>0.2</b>. 0.02 is only 2%%." % (fr(20, 100), fr(2, 10))),
        (1, "0.01", ["0.1", "1", "0.001"], "1%% = %s = 1 hundredth = <b>0.01</b>. 0.1 is 10%%." % fr(1, 100)),
    ]:
        assert F(Dm(right)) == F(p_, 100)
        its.append(mcq("Write <b>%d%%</b> as a decimal." % p_, right, wrong, e))
    for p_, (n, d), wrong, e in [
        (25, (1, 4), [fr(1, 25), fr(2, 5), fr(1, 2)], "25%% = %s. 4 × 25 = 100, so it is <b>%s</b>." % (fr(25, 100), fr(1, 4))),
        (10, (1, 10), [fr(1, 100), fr(1, 5), fr(1, 1000)], "10%% = %s = <b>%s</b>. %s is 1%%." % (fr(10, 100), fr(1, 10), fr(1, 100))),
        (20, (1, 5), [fr(1, 20), fr(1, 2), fr(1, 4)], "20%% = %s. 5 × 20 = 100, so it is <b>%s</b>." % (fr(20, 100), fr(1, 5))),
    ]:
        assert F(p_, 100) == F(n, d)
        its.append(mcq("Write <b>%d%%</b> as a fraction in simplest form." % p_, fr(n, d), wrong, e))
    its.append(mcq("Which is <b>not</b> equal to 50%?", "0.05", [fr(1, 2), "0.5", fr(50, 100)],
                   "50%% = %s = %s = 0.5. <b>0.05</b> is only 5%%." % (fr(50, 100), fr(1, 2)), same_ok=True))
    its.append(mcq("Which is <b>correct</b>?", "%s = 0.75 = 75%%" % fr(3, 4),
                   ["%s = 0.34 = 34%%" % fr(3, 4), "%s = 0.75 = 7.5%%" % fr(3, 4), "%s = 0.7 = 70%%" % fr(3, 4)],
                   "%s = %s = 0.75 = 75%%. So <b>%s = 0.75 = 75%%</b> is correct." % (fr(3, 4), fr(75, 100), fr(3, 4)),
                   same_ok=True))
    assert F(50, 100) * 40 == 20 and F(10, 100) * 50 == 5
    its.append(mcq("What is <b>50% of 40</b>?", "20", ["80", "10", "50"],
                   "50%% = %s. Half of 40 is <b>20</b>. 10 is 25%% of 40." % fr(1, 2)))
    its.append(mcq("What is <b>10% of 50</b>?", "5", ["10", "40", "500"],
                   "10%% = %s. 50 ÷ 10 = <b>5</b>. 40 is what is left after taking away 10, not 10%%." % fr(1, 10)))
    order = [0, 7, 1, 9, 3, 10, 2, 4, 8, 12, 5, 11, 6, 13, 14, 15, 16, 17, 18, 19]
    return {"title": "Familiar percentages, fractions and decimals", "items": reorder(its, order)}


# ============================================================ set 4: compare relative size
def which_bigger(x, y, e):
    a, b = v(x), v(y)
    right = x if a > b else y if b > a else "They are equal"
    ch = [x, y, "They are equal", "You can’t tell"]
    wrong = [c for c in ch if c != right]
    return mcq("Which is greater: <b>%s</b> or <b>%s</b>?" % (x, y), right, wrong, e, same_ok=True)


def set_compare():
    its = []
    its.append(which_bigger("0.5", "45%", "0.5 = 50%. 50% &gt; 45%, so <b>0.5</b> is greater. Do not compare 5 and 45."))
    its.append(which_bigger("0.4", "45%", "0.4 = 40%. 45% &gt; 40%, so <b>45%</b> is greater. 0.4 is not 4%."))
    its.append(which_bigger(fr(3, 10), "25%", "%s = 30%%. 30%% &gt; 25%%, so <b>%s</b> is greater." % (fr(3, 10), fr(3, 10))))
    its.append(which_bigger(fr(1, 4), "0.25", "%s = %s = 0.25. <b>They are equal</b>." % (fr(1, 4), fr(25, 100))))
    its.append(which_bigger("0.6", "58%", "0.6 = 60%. 60% &gt; 58%, so <b>0.6</b> is greater."))
    its.append(which_bigger(fr(1, 5), "15%", "%s = 20%%. 20%% &gt; 15%%, so <b>%s</b> is greater." % (fr(1, 5), fr(1, 5))))
    its.append(which_bigger("0.07", "10%", "0.07 = 7%. 10% &gt; 7%, so <b>10%</b> is greater."))
    its.append(which_bigger(fr(3, 4), "0.8", "%s = 0.75. 0.8 = 0.80. 0.80 &gt; 0.75, so <b>0.8</b> is greater." % fr(3, 4)))
    its.append(mcq("Which is the <b>greatest</b>?", "45%", ["0.4", fr(3, 10), fr(1, 4)],
                   "Write them all as percentages: 0.4 = 40%%, %s = 30%%, %s = 25%%. The greatest is <b>45%%</b>."
                   % (fr(3, 10), fr(1, 4))))
    its.append(mcq("Which is the <b>smallest</b>?", fr(1, 4), ["0.5", "48%", "0.3"],
                   "As percentages: 0.5 = 50%%, 48%%, %s = 25%%, 0.3 = 30%%. The smallest is <b>%s</b>." % (fr(1, 4), fr(1, 4))))

    def order_q(nums, asc, wrongs, e):
        right = sorted(nums, key=v, reverse=not asc)
        ws = [", ".join(w) for w in wrongs]
        for w in wrongs:
            assert sorted(w) == sorted(nums) and w != right
        assert len(set(ws)) == 3
        return mcq("Order from <b>%s</b>:<br><b>%s</b>" % ("smallest to greatest" if asc else "greatest to smallest", ", ".join(nums)),
                   ", ".join(right), ws, e, same_ok=True)
    its.append(order_q(["0.4", "45%", fr(3, 10)], True,
                       [["0.4", fr(3, 10), "45%"], [fr(3, 10), "45%", "0.4"], ["45%", "0.4", fr(3, 10)]],
                       "As percentages: 0.4 = 40%%, 45%%, %s = 30%%. Smallest first: <b>%s, 0.4, 45%%</b>." % (fr(3, 10), fr(3, 10))))
    its.append(order_q([fr(1, 2), "0.45", "60%", fr(1, 5)], False,
                       [["0.45", "60%", fr(1, 2), fr(1, 5)], ["60%", "0.45", fr(1, 2), fr(1, 5)], [fr(1, 2), fr(1, 5), "60%", "0.45"]],
                       "As percentages: %s = 50%%, 0.45 = 45%%, 60%%, %s = 20%%. Greatest first: <b>60%%, %s, 0.45, %s</b>."
                       % (fr(1, 2), fr(1, 5), fr(1, 2), fr(1, 5))))
    its.append(order_q(["9%", "0.2", fr(1, 10), "15%"], True,
                       [["0.2", "9%", fr(1, 10), "15%"], [fr(1, 10), "9%", "15%", "0.2"], ["9%", "15%", fr(1, 10), "0.2"]],
                       "As percentages: 9%%, 0.2 = 20%%, %s = 10%%, 15%%. Smallest first: <b>9%%, %s, 15%%, 0.2</b>."
                       % (fr(1, 10), fr(1, 10))))
    its.append(mcq("Which is between <b>25%</b> and <b>50%</b>?", "0.3", ["0.03", "0.6", fr(1, 5)],
                   "0.3 = 30%%, which is between 25%% and 50%%: <b>0.3</b>. 0.03 = 3%%, 0.6 = 60%% and %s = 20%%." % fr(1, 5)))
    assert F(1, 4) < v("0.3") < F(1, 2)
    its.append(mcq("Which is <b>closest</b> to 50%?", "0.48", ["0.4", "0.05", fr(3, 4)],
                   "0.48 = 48%%, only 2%% away from 50%%. 0.4 = 40%%, 0.05 = 5%% and %s = 75%%. So <b>0.48</b>." % fr(3, 4)))
    its.append(mcq("Which is <b>greater than</b> %s?" % fr(1, 2), "55%", ["0.45", fr(2, 5), "0.05"],
                   "%s = 50%%. Only <b>55%%</b> is more. 0.45 = 45%%, %s = 40%% and 0.05 = 5%%." % (fr(1, 2), fr(2, 5))))
    its.append(mcq("Which is <b>less than</b> 10%?", "0.08", ["0.8", fr(1, 5), "0.12"],
                   "0.08 = 8 hundredths = 8%%. 8%% &lt; 10%%, so <b>0.08</b>. 0.8 = 80%%, %s = 20%% and 0.12 = 12%%." % fr(1, 5)))
    its.append(mcq("Harper says, “45% is greater than 0.5, because 45 is greater than 5.” Is she right?",
                   "No, because 0.5 = 50%", ["Yes, because 45 &gt; 5", "Yes, because 45% has more digits",
                                             "No, because 0.5 = 5%"],
                   "Change them to the same kind of number: 0.5 = 50 hundredths = 50%. 45% &lt; 50%. "
                   "So <b>no, because 0.5 = 50%</b>.", same_ok=True))
    nums = ["0.6", fr(2, 5), "55%", "0.45"]
    assert sum(1 for x in nums if v(x) > F(1, 2)) == 2
    its.append(mcq("How many of these are <b>greater than 50%%</b>?<br><b>%s</b>" % ", ".join(nums), "2", ["1", "3", "4"],
                   "As percentages: 60%%, %s = 40%%, 55%%, 45%%. Only 60%% and 55%% are greater, so <b>2</b>." % fr(2, 5)))
    its.append(mcq("Compare <b>0.7</b> and <b>7%</b>.", "0.7 &gt; 7%", ["0.7 &lt; 7%", "0.7 = 7%", "You can’t tell"],
                   "0.7 = 70 hundredths = 70%. 70% &gt; 7%, so <b>0.7 &gt; 7%</b>.", same_ok=True))
    order = [0, 19, 1, 3, 6, 2, 4, 5, 7, 16, 15, 8, 9, 13, 14, 17, 18, 10, 11, 12]
    return {"title": "Compare percentages, fractions and decimals", "items": reorder(its, order)}


# ============================================================ set 5: real contexts
def set_problems(Pp):
    its = []
    n, he, his = Pp.next()
    its.append(mcq(fig(battery_svg(3, 4)) + "%s’s tablet battery has 4 equal bars. 3 bars are green. "
                   "What percentage is charged?" % n, "75%", ["3%", "34%", "25%"],
                   "3 of 4 bars = %s. %s = 25%%, so %s = <b>75%%</b>. 25%% is the empty part." % (fr(3, 4), fr(1, 4), fr(3, 4))))
    n, he, his = Pp.next()
    its.append(mcq("%s’s phone shows <b>40%%</b> battery left. What percentage of the charge has been used?" % n,
                   "60%", ["40%", "4%", "140%"],
                   "A full charge is 100%. 100% − 40% = <b>60%</b> has been used."))
    n, he, his = Pp.next()
    assert F(18, 20) == F(90, 100)
    its.append(mcq("%s scores <b>18 out of 20</b> in a spelling test. What percentage is that?" % n, "90%",
                   ["18%", "2%", "80%"],
                   "20 × 5 = 100, so multiply the score by 5 too: %s = %s = <b>90%%</b>. 2 is the number of marks %s missed."
                   % (fr(18, 20), fr(90, 100), he)))
    n, he, his = Pp.next()
    its.append(mcq("%s gets <b>7 out of 10</b> in a times tables quiz. What percentage is that?" % n, "70%",
                   ["7%", "30%", "0.7%"],
                   "%s = %s = <b>70%%</b>. 30%% is the part %s got wrong." % (fr(7, 10), fr(70, 100), he)))
    its.append(mcq("A T-shirt costs $40. A sign says <b>50% off</b>. How much do you pay now?", "$20",
                   ["$10", "$30", "$80"],
                   "50% off means half the price is taken off. Half of $40 is $20, so you pay $40 − $20 = <b>$20</b>. "
                   "$30 takes off only $10."))
    its.append(mcq(fig(tank_svg(1)) + "The marks split the rainwater tank into 4 equal parts. "
                   "What percentage of the tank is full?", "25%", ["75%", "4%", "14%"],
                   "The water is up to the first of 4 equal parts: %s = <b>25%%</b>. 75%% is the empty part." % fr(1, 4)))
    its.append(mcq("A rainwater tank is 25% full. What fraction of the tank is <b>empty</b>?", fr(3, 4),
                   [fr(1, 4), fr(1, 25), fr(1, 3)],
                   "25%% is full, so 100%% − 25%% = 75%% is empty. 75%% = <b>%s</b>." % fr(3, 4)))
    its.append(mcq("Shop A has <b>25%% off</b>. Shop B has <b>%s off</b>. Which shop takes off more?" % fr(1, 5),
                   "Shop A", ["Shop B", "They take off the same", "You can’t tell"],
                   "%s = 20%%. 25%% &gt; 20%%, so <b>Shop A</b> takes off more." % fr(1, 5), same_ok=True))
    its.append(mcq("A netball team won 60% of its games this season. What percentage of its games did it <b>not</b> win?",
                   "40%", ["60%", "50%", "6%"],
                   "All the games are 100%. 100% − 60% = <b>40%</b>."))
    a, ah, _ = Pp.next()
    b, bh, _ = Pp.next()
    its.append(mcq("In a quiz, %s gets 45%% of the questions right. %s gets 0.5 of the questions right. "
                   "Who gets more right?" % (a, b), b, [a, "They are the same", "You can’t tell"],
                   "0.5 = 50%%. 50%% &gt; 45%%, so <b>%s</b> gets more right." % b, same_ok=True))
    its.append(mcq("At the school sausage sizzle, 50% of the 60 sausages have been sold. How many have been sold?",
                   "30", ["120", "10", "50"],
                   "50%% = %s. Half of 60 is <b>30</b>. 10 is 60 − 50." % fr(1, 2)))
    assert F(1, 2) * 60 == 30
    its.append(mcq(fig(strip_svg(10, 3)) + "This bar shows how much of a game has downloaded. What percentage has downloaded?",
                   "30%", ["3%", "70%", "0.3%"],
                   "The bar has 10 equal parts, so each part is 10%. 3 parts = <b>30%</b>. 70% is still to download."))
    its.append(mcq("A 2 L bottle of water is 50% full. How much water is in it?", "1 L", ["50 L", "2 L", "0.5 L"],
                   "50%% = %s. Half of 2 L is <b>1 L</b>. 2 L would be 100%%." % fr(1, 2)))
    its.append(mcq("Which sign means <b>half price</b>?", "50% off", ["25% off", "5% off", "12% off"],
                   "Half = %s = 50%%. So <b>50%% off</b> takes off half the price." % fr(1, 2)))
    n, he, his = Pp.next()
    assert 100 - 30 - 45 == 25
    its.append(mcq("In %s’s garden, 0.3 of the flowers are red, 45%% are yellow and the rest are white. "
                   "What percentage are white?" % n, "25%", ["75%", "52%", "55%"],
                   "0.3 = 30%. Red and yellow: 30% + 45% = 75%. White: 100% − 75% = <b>25%</b>. "
                   "52% comes from reading 0.3 as 3%."))
    its.append(mcq("In a class survey, %s of the students like cricket and 70%% like swimming. Which is liked by more students?"
                   % fr(3, 4), "cricket", ["swimming", "They are the same", "You can’t tell"],
                   "%s = 75%%. 75%% &gt; 70%%, so <b>cricket</b> is liked by more students." % fr(3, 4), same_ok=True))
    its.append(mcq("A bus for the athletics carnival is 100% full. There are 48 students on it. How many seats are there?",
                   "48", ["100", "52", "148"],
                   "100% full means every seat is taken. So there are <b>48</b> seats. 100% does not mean 100 seats."))
    a, ah, _ = Pp.next()
    b, bh, _ = Pp.next()
    its.append(mcq("%s’s water bottle is 0.6 full. %s’s is 65%% full. Both bottles are the same size. "
                   "Whose bottle has more water?" % (a, b), b, [a, "They are the same", "You can’t tell"],
                   "0.6 = 60%%. 65%% &gt; 60%%, so <b>%s’s</b> bottle has more water." % b, same_ok=True))
    n, he, his = Pp.next()
    assert F(16, 20) == F(80, 100)
    its.append(mcq("%s scores <b>16 out of 20</b> in a maths test. What percentage is that?" % n, "80%",
                   ["16%", "4%", "20%"],
                   "20 × 5 = 100, so %s = %s = <b>80%%</b>. 4 is the number of marks %s missed." % (fr(16, 20), fr(80, 100), he)))
    its.append(mcq("A film is 50% downloaded after 10 minutes. At the same speed, how long will it take to download 100%?",
                   "20 minutes", ["10 minutes", "50 minutes", "100 minutes"],
                   "50% is half. Half took 10 minutes, so the whole takes 10 + 10 = <b>20 minutes</b>."))
    order = [13, 11, 0, 1, 5, 8, 3, 16, 6, 7, 9, 12, 2, 10, 4, 17, 15, 18, 14, 19]
    return {"title": "Percentages in real life", "items": reorder(its, order)}


# ============================================================ lesson
def body_html():
    g = grid_svg(37, cell=22)
    w = grid_svg(45, cell=22, k2=30)
    return (
        "<h2>Per cent means out of 100</h2>"
        "<p>Per cent (%) means <b>out of 100</b>. Split a whole into 100 equal parts. Each part is 1%.</p>"
        "<figure class='sn-fig'>" + g +
        "<figcaption>37 of 100 squares are shaded: " + fr(37, 100) + " = 0.37 = 37%.</figcaption></figure>"
        "<h2>100% is the whole</h2>"
        "<p>All 100 parts make the whole, so <b>100% = 1 whole</b>. The parts always add up to 100%.</p>"
        "<figure class='sn-fig'>" + w +
        "<figcaption>45% green + 30% blue = 75% shaded. 100% − 75% = 25% white.</figcaption></figure>"
        "<p>100% means <b>all</b> of something, not 100 things. If a class of 25 students all go on an excursion, "
        "100% of the class is 25 students.</p>"
        "<h2>Percentages to know</h2>"
        "<p>To change a fraction into a percentage, make the denominator 100.</p>"
        + table(["Percentage", "Fraction", "Decimal"], [
            ["50%", fr(1, 2), "0.5"],
            ["25%", fr(1, 4), "0.25"],
            ["75%", fr(3, 4), "0.75"],
            ["20%", fr(1, 5), "0.2"],
            ["10%", fr(1, 10), "0.1"],
            ["1%", fr(1, 100), "0.01"],
        ])
        + ex("Example", "Write " + fr(1, 5) + " as a percentage.",
             "5 × 20 = 100, so multiply the top by 20 too: " + fr(1, 5) + " = " + fr(20, 100) + ".", "20%")
        + "<h2>Comparing</h2>"
        "<p>Change every number into a percentage, then compare.</p>"
        + ex("Example", "Order 0.4, 45% and " + fr(3, 10) + " from smallest to greatest.",
             "0.4 = 40%, 45% and " + fr(3, 10) + " = 30%.", fr(3, 10) + ", 0.4, 45%")
        + ex("Test score", "Isla scores 18 out of 20. What percentage is that?",
             "20 × 5 = 100, so multiply the score by 5 too: " + fr(18, 20) + " = " + fr(90, 100) + ".", "90%")
        + "<h2>Common mistakes</h2>"
        + table(["Mistake", "What to do instead"], [
            ["0.4 = 4%", "0.4 = 0.40 = 40%"],
            [fr(1, 5) + " = 15%", fr(1, 5) + " = " + fr(20, 100) + " = 20%"],
            ["45% &gt; 0.5 because 45 &gt; 5", "0.5 = 50%, so 45% &lt; 0.5"],
            ["100% means 100 things", "100% means the whole, however many there are"],
        ])
    )


FAQ = [
    {"q": "What do Year 5 students learn about percentages in the Australian Curriculum?",
     "a": "In Year 5 (AC9M5N04) students learn that 100% is the complete whole, use percentages to describe and compare amounts, and connect familiar percentages such as 50%, 25%, 10% and 1% to their fractions and decimals."},
    {"q": "How do you explain percentages to a Year 5 child?",
     "a": "Show a hundred square: the whole is 100 small squares, and each square is 1%. If 37 squares are shaded, 37% is shaded, which is also 37/100 or 0.37."},
    {"q": "Which percentage, fraction and decimal facts should Year 5 know?",
     "a": "50% = 1/2 = 0.5, 25% = 1/4 = 0.25, 75% = 3/4 = 0.75, 20% = 1/5 = 0.2, 10% = 1/10 = 0.1 and 1% = 1/100 = 0.01."},
    {"q": "How do you compare a percentage, a fraction and a decimal?",
     "a": "Change them all into percentages first. For 0.4, 45% and 3/10, write 40%, 45% and 30%, so the order from smallest is 3/10, 0.4, 45%. This kind of question also appears in NAPLAN numeracy."},
]


def mark_large(u, pattern):
    """Tag pictures that must print larger (hundred squares, bars)."""
    rx = re.compile(r"<svg (?=[^>]*aria-label='" + pattern + ")")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u


def gen():
    rnd = random.Random(5804)
    Pp = People(rnd)
    sets = [set_parts(), set_whole(), set_equiv(), set_compare(), set_problems(Pp)]
    balance(sets, rnd)
    seen = set()
    for s in sets:
        assert len(s["items"]) == 20, (s["title"], len(s["items"]))
        assert sorted(it["a"] for it in s["items"]) == sorted([0, 1, 2, 3] * 5)
        for it in s["items"]:
            assert len(set(it["c"])) == 4, it
            assert it["q"].count("<svg") <= 1
            k = re.sub(r"<[^>]+>", "", it["q"]) + "|" + "|".join(sorted(it["c"]))
            assert k not in seen, it["q"]
            seen.add(k)
    u = {
        "country": "au", "subject": "maths", "grade": "year-5", "slug": "percentages", "sort": 4,
        "updated": UPDATED, "pdf_url": "",
        "title": "Percentages",
        "seo_title": "Year 5 Percentages Worksheets: 100% as the Whole, Fractions and Decimals",
        "short_title": "Percentages",
        "domain": "Number",
        "standard_code": "AC9M5N04",
        "standard_url": "https://v9.australiancurriculum.edu.au/f-10-curriculum/learning-areas/mathematics",
        "standard_text": "Recognise that 100% represents the complete whole and use percentages to describe, represent and compare relative size; connect familiar percentages to their decimal and fraction equivalents",
        "meta_desc": "Free Year 5 percentages worksheets for the Australian Curriculum: per cent as parts of 100, 100% as the whole, 50%, 25%, 10% and 1% as fractions and decimals, comparing sizes and real-life problems. 100 maths questions with an answer key, great for NAPLAN practice.",
        "key_big": "Per cent means out of 100, and 100% is the whole: 37% = 37/100 = 0.37.",
        "key_sub": "Know 50% = 1/2 = 0.5, 25% = 1/4 = 0.25, 10% = 1/10 = 0.1 and 1% = 1/100 = 0.01. To compare, change everything into percentages: 0.5 = 50% > 45%.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }
    return mark_large(u, "(hundred square|four hundred squares|percentage bar)")


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
