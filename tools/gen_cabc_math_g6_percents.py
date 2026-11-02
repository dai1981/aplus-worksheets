# -*- coding: utf-8 -*-
"""
British Columbia Grade 6 Math: Percents and discounts
(BC Mathematics Curriculum, Grade 6, Number — whole-number percents and percentage discounts)
  python3 tools/gen_cabc_math_g6_percents.py
Percent as "out of 100" on hundred grids; changing between percents, fractions and decimals;
percent of a number with benchmarks (1%, 5%, 10%, 25%, 50%); discounts and sale prices;
word problems in BC contexts (no taxes in Grade 6).
Wrong answers come from real mistakes: 25% off $40 = $15 (taking away dollars, not percent),
giving the discount instead of the sale price, 0.6 = 6%, 3/4 = 34%, using the unshaded part,
17 out of 50 = 17%.
Every answer is checked with fractions.Fraction (never float).
Canadian English, dollars and cents (¢), metric units, SI number spacing. HTML attributes use single quotes.
"""
import json, os, random, re
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "ca-bc", "math", "grade-6")
UPDATED = "2026-11-02"
NBSP = " "
FILL = "#4fae74"
LINE = "#2b2b2b"
THIN = "#8a8a8a"
RED = "#d6453b"
BLUE = "#2f6fb5"
FONT = "Arial, Helvetica, sans-serif"
GIRLS = ["Olivia", "Ava", "Chloe", "Simran", "Jasleen", "Mei", "Hana", "Sofia", "Emma", "Leah", "Zara", "Nadia"]
BOYS = ["Liam", "Ethan", "Noah", "Arjun", "Harjot", "Wei", "Mateo", "Lucas", "Kai", "Owen", "Ryan"]


# ------------------------------------------------------------ numbers
def num(x):
    """Exact decimal text: F(9, 2) -> '4.5', 2500 -> '2500', 18000 -> '18 000' (no-break space)."""
    x = F(x)
    assert x >= 0, x
    d, k = x.denominator, 0
    while (10 ** k) % d:
        k += 1
        assert k < 8, x
    v = x.numerator * (10 ** k // d)
    i, r = divmod(v, 10 ** k)
    s = str(i) if i < 10000 else "{:,}".format(i).replace(",", NBSP)
    if r:
        s += "." + str(r).zfill(k).rstrip("0")
    return s


def dec(x):
    """Decimal with a leading 0 for values under 1: '0.35'."""
    return num(x)


def pct(x):
    return num(x) + "%"


def money(x):
    """$45, $25.50, 75¢ under $1."""
    x = F(x)
    c = x * 100
    assert c.denominator == 1 and c > 0, x
    c = int(c)
    if c < 100:
        return "%d¢" % c
    if c % 100:
        return "$%s.%02d" % (num(c // 100), c % 100)
    return "$" + num(c // 100)


def pc(p, n):
    """p% of n, exactly."""
    return F(p) * F(n) / 100


def fr(a, b):
    return "<span class='fr'><span class='fn'>%s</span><span class='fd'>%s</span></span>" % (a, b)


def frf(x):
    x = F(x)
    return fr(x.numerator, x.denominator)


def plain(s):
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", s)).strip()


FRX = re.compile(r"^<span class='fr'><span class='fn'>(\d+)</span><span class='fd'>(\d+)</span></span>$")
NUM = re.compile(r"^(\$)?(\d[\d" + NBSP + r"]*(?:\.\d+)?)(¢|%)?( .+)?$")


def val(c):
    """Value of a choice with its unit, or None when it is not a single number."""
    m = FRX.match(c)
    if m:
        return (F(int(m.group(1)), int(m.group(2))), "")
    m = NUM.match(c)
    if not m:
        return None
    v = F(m.group(2).replace(NBSP, ""))
    if (m.group(1) or m.group(3) == "¢") and m.group(4):
        return None
    if m.group(1):
        return (v, "$")
    if m.group(3) == "¢":
        return (v / 100, "$")
    if m.group(3) == "%":
        if m.group(4):
            return None
        return (v, "%")
    return (v, (m.group(4) or "").strip())


def mcq(q, right, wrong, e, value=None, same_ok=False):
    """Correct answer first + 3 wrong; balance() moves it. No two choices equal in value (unless same_ok).
    value: the exact answer, checked against the correct choice."""
    right = str(right)
    wrong = [str(x) for x in wrong]
    assert len(wrong) == 3, (q, wrong)
    ch = [right] + wrong
    assert len(set(plain(x) for x in ch)) == 4, (q, ch)
    if value is not None:
        assert val(right) is not None and val(right)[0] == F(value), (q, right, value)
    if not same_ok:
        vs = [val(x) for x in ch]
        known = [v for v in vs if v is not None]
        assert len(set(known)) == len(known), (q, ch)
    return {"q": q, "c": ch, "a": 0, "e": e}


def balance(sets, rnd):
    """Spread the correct answers evenly over the 4 positions in every set (5 each)."""
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


def text(x, y, t, fs=16, anchor="middle", col=LINE, weight=700):
    return ("<text x='%.1f' y='%.1f' font-size='%d' font-weight='%d' fill='%s' text-anchor='%s'>%s</text>"
            % (x, y, fs, weight, col, anchor, t))


def tw(t, fs):
    """Rough width of bold Arial text."""
    return len(plain(t)) * fs * 0.62


def table(head, rows):
    h = "".join("<th>%s</th>" % x for x in head)
    b = "".join("<tr>" + "".join("<td>%s</td>" % c for c in r) + "</tr>" for r in rows)
    return "<div class='sn-tw'><table class='sn-table'><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>" % (h, b)


def ex(title, q, s, a):
    return ("<div class='sn-ex'><span class='sn-ex-t'>%s</span><p class='sn-ex-q'>%s</p>"
            "<p class='sn-ex-s'>%s</p><p class='sn-ex-a'>Answer: %s</p></div>" % (title, q, s, a))


# ------------------------------------------------------------ pictures
def grid_svg(k, cell=18):
    """10 x 10 hundred grid with k squares shaded: full columns first, then from the top of the next column."""
    pad = 4
    s = []
    for c in range(10):
        for r in range(10):
            if c * 10 + r < k:
                s.append("<rect x='%d' y='%d' width='%d' height='%d' fill='%s'/>" % (pad + c * cell, pad + r * cell, cell, cell, FILL))
    for i in range(1, 10):
        s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='1.2'/>"
                 % (pad + i * cell, pad, pad + i * cell, pad + 10 * cell, THIN))
        s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='1.2'/>"
                 % (pad, pad + i * cell, pad + 10 * cell, pad + i * cell, THIN))
    s.append("<rect x='%d' y='%d' width='%d' height='%d' fill='none' stroke='%s' stroke-width='2.5'/>"
             % (pad, pad, 10 * cell, 10 * cell, LINE))
    w = 10 * cell + 2 * pad
    return svg_wrap(w, w, "".join(s), "hundred grid with %d of 100 squares shaded" % k)


def percent_bar_svg(total_txt, parts, shade, part_txt, W=420):
    """A bar for the whole amount (100%) in `parts` equal parts, the first `shade` parts shaded,
    each part labelled with part_txt; 0% and 100% under the ends."""
    L, Rr = 14, W - 14
    pw = (Rr - L) / float(parts)
    Y0, Y1 = 40, 80
    s = ["<line x1='%d' y1='22' x2='%d' y2='22' stroke='%s' stroke-width='2'/>" % (L, Rr, LINE)]
    for x in (L, Rr):
        s.append("<line x1='%d' y1='16' x2='%d' y2='28' stroke='%s' stroke-width='2'/>" % (x, x, LINE))
    bw = tw(total_txt, 16) + 16
    s.append("<rect x='%.1f' y='8' width='%.1f' height='24' fill='#ffffff'/>" % ((L + Rr) / 2.0 - bw / 2, bw))
    s.append(text((L + Rr) / 2.0, 27, total_txt, 16))
    if shade:
        s.append("<rect x='%d' y='%d' width='%.1f' height='%d' fill='%s'/>" % (L, Y0, pw * shade, Y1 - Y0, FILL))
    for i in range(1, parts):
        s.append("<line x1='%.1f' y1='%d' x2='%.1f' y2='%d' stroke='%s' stroke-width='1.6'/>" % (L + i * pw, Y0, L + i * pw, Y1, LINE))
    s.append("<rect x='%d' y='%d' width='%d' height='%d' fill='none' stroke='%s' stroke-width='2.5'/>" % (L, Y0, Rr - L, Y1 - Y0, LINE))
    for i in range(parts):
        s.append(text(L + (i + 0.5) * pw, (Y0 + Y1) / 2.0 + 5.5, part_txt, 14))
    s.append(text(L, Y1 + 22, "0%", 14, "start"))
    s.append(text(Rr, Y1 + 22, "100%", 14, "end"))
    return svg_wrap(W, Y1 + 28, "".join(s),
                    "percent bar: %s split into %d equal parts, %d shaded" % (plain(total_txt), parts, shade))


# ============================================================ set 1: percent as out of 100
def set_out_of_100():
    its = []

    def grid_q(k, q, right, wrong, e, value):
        its.append(mcq(fig(grid_svg(k)) + q, right, wrong, e, value=value))

    grid_q(37, "What percent of the hundred grid is shaded?", "37%", ["63%", "3.7%", "0.37%"],
           "37 of the 100 squares are shaded. 37 out of 100 = <b>37%</b>. 63% is the part that is <b>not</b> shaded.", 37)
    grid_q(60, "What percent of the hundred grid is shaded?", "60%", ["40%", "6%", "600%"],
           "6 full columns of 10 = 60 squares out of 100 = <b>60%</b>. 6% counts the columns, not the squares.", 60)
    grid_q(8, "What percent of the hundred grid is shaded?", "8%", ["80%", "92%", "0.8%"],
           "Only 8 squares out of 100 are shaded: <b>8%</b>. 80% would be 8 full columns.", 8)
    grid_q(45, "What percent of the hundred grid is <b>not</b> shaded?", "55%", ["45%", "145%", "5.5%"],
           "45 squares are shaded, so 100 − 45 = 55 are not: <b>55%</b>. 45% is the shaded part, "
           "and 145% adds 100 + 45 instead of subtracting.", 55)
    its.append(mcq("What does percent mean?", "out of 100", ["out of 10", "times 100", "out of 1000"],
                   "<i>Per cent</i> means “for each hundred”. 45% means 45 <b>out of 100</b>."))
    its.append(mcq("On a hundred grid, each small square is what percent of the whole grid?", "1%",
                   ["10%", "100%", "0.1%"],
                   "There are 100 squares, so each one is 1 out of 100 = <b>1%</b>. 10% is one full column of 10.", value=1))
    grid_q(100, "What percent of the hundred grid is shaded?", "100%", ["10%", "1%", "0%"],
           "All 100 squares are shaded. The whole is <b>100%</b>.", 100)
    its.append(mcq("Write 73 out of 100 as a percent.", "73%", ["7.3%", "27%", "0.73%"],
                   "Out of 100 is the same as percent: <b>73%</b>. 27% is the other part, 100 − 73.", value=73))
    its.append(mcq("Which means the same as 9%?", "9 out of 100", ["9 out of 10", "90 out of 100", "1 out of 9"],
                   "9% = <b>9 out of 100</b>. 9 out of 10 is 90%, ten times as much.", same_ok=True))
    its.append(mcq("On a hundred grid, 25% of the squares are shaded. How many squares are shaded?", "25",
                   ["4", "75", "250"],
                   "25% means 25 out of 100, so <b>25</b> squares. 75 squares are not shaded, "
                   "and 4 comes from 100 ÷ 25.", value=25))
    grid_q(12, "How many more squares must be shaded so that 50% of the grid is shaded?", "38",
           ["12", "50", "62"],
           "50% is 50 squares. 12 are shaded now, so 50 − 12 = <b>38</b> more. 62 adds 50 + 12, and 50 forgets the 12 already shaded.", 38)
    its.append(mcq("On a hundred grid, 30 squares are red and 45 squares are blue. The rest are white. "
                   "What percent of the grid is white?", "25%", ["75%", "15%", "70%"],
                   "30 + 45 = 75 squares are coloured. 100 − 75 = 25 are white: <b>25%</b>. "
                   "75% is the coloured part, and 15% is 45 − 30.", value=25))
    grid_q(64, "The shaded squares show the cedar seedlings that grew in a school garden. "
           "What percent of the seedlings grew?", "64%", ["36%", "6.4%", "46%"],
           "64 of the 100 squares are shaded: <b>64%</b>. 36% is the part that did not grow, "
           "and 46% swaps the digits.", 64)
    its.append(mcq("A school has 100 Grade 6 students. 46 of them walk to school. What percent do <b>not</b> walk?",
                   "54%", ["46%", "146%", "0.54%"],
                   "100 − 46 = 54 students out of 100 do not walk: <b>54%</b>. 46% is the walkers, "
                   "and 146% adds 100 + 46 instead of subtracting.", value=54))
    its.append(mcq("Write 7 out of 10 as a percent.", "70%", ["7%", "30%", "17%"],
                   "Make the whole 100: 7 out of 10 = 70 out of 100 = <b>70%</b>. 7% is only 7 out of 100.", value=70))
    its.append(mcq("Write 17 out of 50 as a percent.", "34%", ["17%", "67%", "33%"],
                   "50 × 2 = 100, so multiply 17 by 2 too: 34 out of 100 = <b>34%</b>. "
                   "17% forgets that the whole is 50, not 100.", value=34))
    its.append(mcq("Write 9 out of 20 as a percent.", "45%", ["9%", "11%", "29%"],
                   "20 × 5 = 100, so 9 × 5 = 45: 45 out of 100 = <b>45%</b>. 11 is 20 − 9, and 29 is 9 + 20.", value=45))
    its.append(mcq("Write 12 out of 25 as a percent.", "48%", ["12%", "13%", "37%"],
                   "25 × 4 = 100, so 12 × 4 = 48: <b>48%</b>. 12% forgets that the whole is 25. "
                   "13 is 25 − 12, and 37 is 12 + 25.", value=48))
    its.append(mcq("Write 3 out of 4 as a percent.", "75%", ["34%", "25%", "3.4%"],
                   "4 × 25 = 100, so 3 × 25 = 75: <b>75%</b>. 34% just writes the digits 3 and 4 together, "
                   "and 25% is the 1 part left over.", value=75))
    its.append(mcq("Which is greater than 50%?", "13 out of 25", ["24 out of 50", "4 out of 10", "49 out of 100"],
                   "Change each to out of 100. 13 out of 25 = 52 out of 100 = 52%. 24 out of 50 = 48%, "
                   "4 out of 10 = 40%, and 49 out of 100 = 49%. Only <b>13 out of 25</b> is more than 50%.",
                   same_ok=True))
    assert len(its) == 20, len(its)
    return {"title": "Percent means out of 100: hundred grids", "items": its}


# ============================================================ set 2: percents, fractions, decimals
def set_fdp():
    its = []

    def chk(right, value):
        v = val(right)
        assert v is not None and v[0] == F(value), (right, value)

    its.append(mcq("Write 35% as a decimal.", "0.35", ["3.5", "0.035", "35.0"],
                   "35% = 35 hundredths = <b>0.35</b>. Divide by 100: move the decimal point 2 places left.",
                   value=F(35, 100)))
    its.append(mcq("Write 7% as a decimal.", "0.07", ["0.7", "7.0", "0.007"],
                   "7% = 7 hundredths = <b>0.07</b>. 0.7 is 7 tenths, which is 70%.", value=F(7, 100)))
    its.append(mcq("Write 0.6 as a percent.", "60%", ["6%", "0.6%", "600%"],
                   "0.6 = 6 tenths = 60 hundredths = <b>60%</b>. Multiply by 100. 6% would be 0.06.", value=60))
    its.append(mcq("Write 0.08 as a percent.", "8%", ["80%", "0.08%", "800%"],
                   "0.08 = 8 hundredths = <b>8%</b>. 80% would be 0.8.", value=8))
    its.append(mcq("Write 1 as a percent.", "100%", ["1%", "10%", "0.01%"],
                   "1 is one whole, and the whole is <b>100%</b>. 1% is only 0.01.", value=100))
    grid = grid_svg(5)
    its.append(mcq(fig(grid) + "Write the shaded part of the hundred grid as a decimal.", "0.05",
                   ["0.5", "5.0", "0.95"],
                   "5 out of 100 squares = 5 hundredths = <b>0.05</b>. 0.5 would be 50 squares, and 0.95 is the "
                   "part that is not shaded.", value=F(5, 100)))
    its.append(mcq("Write %s as a percent." % fr(1, 2), "50%", ["12%", "2%", "20%"],
                   "%s = %s = <b>50%%</b>. 12%% just writes the digits 1 and 2 together." % (fr(1, 2), fr(50, 100)),
                   value=50))
    its.append(mcq("Write %s as a percent." % fr(7, 10), "70%", ["7%", "17%", "30%"],
                   "%s = %s = <b>70%%</b>. Multiply the top and bottom by 10. 30%% is the part left over." % (fr(7, 10), fr(70, 100)),
                   value=70))
    its.append(mcq("Write %s as a percent." % fr(1, 4), "25%", ["14%", "4%", "40%"],
                   "%s = %s = <b>25%%</b>, because 4 × 25 = 100. 14%% just writes the digits together." % (fr(1, 4), fr(25, 100)),
                   value=25))
    its.append(mcq("Write %s as a percent." % fr(3, 5), "60%", ["35%", "6%", "30%"],
                   "5 × 20 = 100, so %s = %s = <b>60%%</b>. 35%% writes the digits together, "
                   "and 30%% multiplies only by 10." % (fr(3, 5), fr(60, 100)), value=60))
    its.append(mcq("Write %s as a percent." % fr(3, 20), "15%", ["3%", "32%", "23%"],
                   "20 × 5 = 100, so %s = %s = <b>15%%</b>. 23 is 3 + 20, and 3%% forgets that the whole is 20."
                   % (fr(3, 20), fr(15, 100)), value=15))
    its.append(mcq("Write 20% as a fraction in simplest form.", fr(1, 5), [fr(1, 20), fr(20, 1), fr(1, 2)],
                   "20%% = %s. Divide the top and bottom by 20: <b>%s</b>. %s would be 5%%." % (fr(20, 100), fr(1, 5), fr(1, 20)),
                   value=F(1, 5)))
    its.append(mcq("Write 75% as a fraction in simplest form.", fr(3, 4), [fr(7, 5), fr(1, 4), fr(1, 75)],
                   "75%% = %s. Divide the top and bottom by 25: <b>%s</b>. %s is 25%%, the part left over."
                   % (fr(75, 100), fr(3, 4), fr(1, 4)), value=F(3, 4)))
    its.append(mcq("Write 45% as a fraction in simplest form.", fr(9, 20), [fr(4, 5), fr(9, 2), fr(45, 1000)],
                   "45%% = %s. Divide the top and bottom by 5: <b>%s</b>. %s just uses the digits 4 and 5."
                   % (fr(45, 100), fr(9, 20), fr(4, 5)), value=F(9, 20)))
    its.append(mcq("Write 0.25 as a fraction in simplest form.", fr(1, 4), [fr(1, 25), fr(2, 5), fr(25, 10)],
                   "0.25 = %s = <b>%s</b>. %s uses the digits 2 and 5 as a fraction." % (fr(25, 100), fr(1, 4), fr(2, 5)),
                   value=F(1, 4)))
    its.append(mcq("Write 4% as a fraction in simplest form.", fr(1, 25), [fr(1, 4), fr(2, 5), fr(1, 40)],
                   "4%% = %s. Divide the top and bottom by 4: <b>%s</b>. %s is 25%%, not 4%%."
                   % (fr(4, 100), fr(1, 25), fr(1, 4)), value=F(1, 25)))
    its.append(mcq("Which number is the same as 40%?", "0.4", ["0.04", "4.0", fr(1, 40)],
                   "40%% = %s = <b>0.4</b>. 0.04 is 4%%, and %s is 2.5%%." % (fr(40, 100), fr(1, 40)), value=F(2, 5)))
    its.append(mcq(fig(grid_svg(40)) + "Which does <b>not</b> describe the shaded part of the hundred grid?",
                   "0.04", ["40%", "0.4", fr(2, 5)],
                   "40 of 100 squares are shaded: 40%% = 0.4 = %s. <b>0.04</b> is only 4 squares." % fr(2, 5),
                   same_ok=True))
    its.append(mcq("Which is the greatest?", "0.45", [fr(2, 5), "38%", "0.405"],
                   "Change all to percents: %s = 40%%, 0.45 = 45%%, 38%%, 0.405 = 40.5%%. "
                   "The greatest is <b>0.45</b>. 0.405 has more digits, but it is less than 0.45." % fr(2, 5),
                   same_ok=True))
    its.append(mcq("Which list is in order from least to greatest?",
                   "%s, 0.3, 35%%" % fr(1, 4), ["0.3, %s, 35%%" % fr(1, 4), "35%%, 0.3, %s" % fr(1, 4),
                                                "0.3, 35%%, %s" % fr(1, 4)],
                   "Change all to percents: %s = 25%%, 0.3 = 30%%, 35%%. Least to greatest: <b>%s, 0.3, 35%%</b>."
                   % (fr(1, 4), fr(1, 4))))
    for v, r in [(F(35, 100), "0.35"), (F(7, 100), "0.07")]:
        chk(r, v)
    assert len(its) == 20, len(its)
    return {"title": "Percents, fractions and decimals", "items": its}


# ============================================================ set 3: percent of a number
def set_percent_of():
    its = []

    def pq(p, n, right, wrong, e, q=None, fg="", unit=""):
        assert F(right) == pc(p, n), (p, n, right)
        f = (lambda x: money(x)) if unit == "$" else (lambda x: num(x) + unit)
        its.append(mcq(fg + (q or "What is %s%% of %s?" % (num(p), num(n))), f(right), [f(w) for w in wrong], e,
                       value=right))

    pq(10, 90, 9, [F(9, 10), 80, 900],
       "10%% = %s. Divide by 10: 90 ÷ 10 = <b>9</b>. 0.9 is 1%%, and 80 subtracts 10 from 90." % fr(1, 10))
    pq(50, 64, 32, [14, 128, F(32, 10)],
       "50% is half. 64 ÷ 2 = <b>32</b>. 14 subtracts 50 from 64, and 128 doubles instead of halving.")
    pq(1, 700, 7, [70, F(7, 10), 699],
       "1%% = %s. Divide by 100: 700 ÷ 100 = <b>7</b>. 70 is 10%%, and 699 subtracts 1." % fr(1, 100))
    pq(25, 36, 9, [18, 11, 144],
       "25%% = %s. Divide by 4: 36 ÷ 4 = <b>9</b>. 18 is 50%%, and 11 subtracts 25 from 36." % fr(1, 4))
    pq(20, 35, 7, [15, F(7, 2), 70],
       "10% of 35 = 3.5. 20% is double: 2 × 3.5 = <b>7</b>. 15 subtracts 20 from 35, and 3.5 is only 10%.")
    pq(5, 80, 4, [8, 16, 75],
       "10% of 80 = 8. 5% is half of 10%: <b>4</b>. 16 divides 80 by 5, which gives 20%.")
    pq(75, 60, 45, [15, 30, 50],
       "25% of 60 = 15. 75% = 3 × 25%, so 3 × 15 = <b>45</b>. 15 is only 25%, and 30 is 50%.")
    pq(30, 70, 21, [7, 40, F(21, 10)],
       "10% of 70 = 7. 30% = 3 × 7 = <b>21</b>. 7 is only 10%, and 40 subtracts 30 from 70.")
    pq(15, 60, 9, [6, 3, 45],
       "15% = 10% + 5%. 10% of 60 = 6, and 5% = 3. 6 + 3 = <b>9</b>. 6 and 3 are only the two steps.")
    pq(40, 45, 18, [5, F(9, 2), 27],
       "10% of 45 = 4.5. 40% = 4 × 4.5 = <b>18</b>. 5 subtracts 40 from 45, and 27 is 60%.")
    pq(2, 350, 7, [70, F(7, 2), 348],
       "1% of 350 = 3.5. 2% = 2 × 3.5 = <b>7</b>. 3.5 is only 1%, and 70 is 20%.")
    pq(60, 80, 48, [20, 32, F(48, 10)],
       "10% of 80 = 8. 60% = 6 × 8 = <b>48</b>. 20 subtracts 60 from 80, and 32 is 40%.")
    pq(90, 40, 36, [4, F(36, 10), 50],
       "10% of 40 = 4. 90% = 100% − 10%, so 40 − 4 = <b>36</b>. 4 is the 10% that is left out, "
       "and 50 adds 10 to 40.")
    pq(10, F(64, 10), F(64, 100), [64, F(64, 1000), F(54, 10)],
       "10% means divide by 10: 6.4 ÷ 10 = <b>0.64</b>. 64 multiplies by 10, and 5.4 subtracts 1.")
    pq(1, 12000, 120, [1200, 12, 11999],
       "1%% means divide by 100: 12%s000 ÷ 100 = <b>120</b>. 1200 is 10%%, and 12 divides by 1000." % NBSP)
    pq(12, 50, 6, [38, F(6, 10), 60],
       "1% of 50 = 0.5. 12% = 12 × 0.5 = <b>6</b>. Or: 50 is half of 100, so 12% of 50 is half of 12. "
       "38 subtracts 12 from 50.")
    pq(40, 50, 20, [5, 10, 25],
       "The bar shows $50 in 10 equal parts, so each part is 10% = $5. 4 parts: 4 × $5 = <b>$20</b>. "
       "$5 is one part, and $10 subtracts 40 from 50.",
       q="The whole bar is $50. What is 40% of $50?", fg=fig(percent_bar_svg("$50", 10, 4, "$5")), unit="$")
    pq(75, 80, 60, [20, 5, 75],
       "The bar shows 80 km in 4 equal parts. Each part is 25% = 80 ÷ 4 = 20 km. 3 parts: 3 × 20 = <b>60 km</b>. "
       "20 km is one part (25%), and 5 km subtracts 75 from 80.",
       q="The whole bar is 80 km. What is 75% of 80 km?", fg=fig(percent_bar_svg("80 km", 4, 3, "20 km")), unit=" km")
    its.append(mcq("Which is greater: 20% of 50 or 50% of 20?", "They are equal",
                   ["20% of 50", "50% of 20", "You can’t tell"],
                   "20% of 50 = 2 × 5 = 10. 50% of 20 = 20 ÷ 2 = 10. <b>They are equal</b>: a% of b is always b% of a."))
    its.append(mcq("Which has the same value as 25% of 80?", "50% of 40", ["25% of 40", "50% of 160", "80 ÷ 25"],
                   "25% of 80 = 80 ÷ 4 = 20. 50% of 40 = 40 ÷ 2 = 20, so <b>50% of 40</b>. "
                   "25% of 40 = 10, 50% of 160 = 80, and 80 ÷ 25 = 3.2."))
    assert len(its) == 20, len(its)
    return {"title": "Percent of a number", "items": its}


# ============================================================ set 4: discounts and sale prices
def set_discounts():
    its = []

    def sale(price, p, q, wrong, e, ask="sale"):
        d = pc(p, price)
        right = price - d if ask == "sale" else d
        its.append(mcq(q, money(right), [money(w) for w in wrong], e, value=right))

    sale(40, 25, "A $40 sweater is 25% off. What is the sale price?", [15, 10, 36],
         "25%% = %s. $40 ÷ 4 = $10 off. Sale price: $40 − $10 = <b>$30</b>. $15 takes away 25 dollars "
         "instead of 25 percent, and $10 is the discount, not the price." % fr(1, 4))
    sale(60, 10, "A $60 soccer ball is 10% off. How much money do you save?", [54, 50, 6 * F(1, 10)],
         "10% of $60 = $60 ÷ 10 = <b>$6</b> saved. $54 is the sale price, and $50 takes away 10 dollars.",
         ask="discount")
    sale(80, 20, "Hiking boots that cost $80 are 20% off. What is the sale price?", [60, 16, 72],
         "10% of $80 = $8, so 20% = $16. $80 − $16 = <b>$64</b>. $60 takes away 20 dollars, "
         "and $72 takes off only 10%.")
    sale(70, 50, "A $70 rain jacket is 50% off. What is the sale price?", [20, 63, 105],
         "50% off means you pay half: $70 ÷ 2 = <b>$35</b>. $20 takes away 50 dollars, "
         "and $105 adds the discount.")
    sale(120, 25, "A $120 lacrosse stick is 25% off. What is the sale price?", [95, 30, 108],
         "25%% of $120 = $120 ÷ 4 = $30. $120 − $30 = <b>$90</b>. $95 takes away 25 dollars, and $30 is the discount."
         % ())
    sale(45, 40, "A $45 backpack is 40% off. What is the sale price?", [5, 18, 41],
         "10% of $45 = $4.50, so 40% = $18. $45 − $18 = <b>$27</b>. $5 takes away 40 dollars, "
         "$18 is the discount, and $41 takes off only 4 dollars.")
    sale(32, 25, "A $32 board game is 25% off. What is the sale price?", [7, 8, F(288, 10)],
         "25% of $32 = $32 ÷ 4 = $8. $32 − $8 = <b>$24</b>. $7 takes away 25 dollars, $8 is the discount, "
         "and $28.80 takes off only 10%.")
    sale(200, 15, "A $200 snowboard is 15% off. What is the sale price?", [185, 30, 180],
         "10% of $200 = $20 and 5% = $10, so 15% = $30. $200 − $30 = <b>$170</b>. $185 takes away 15 dollars, "
         "and $180 takes off only 10%.")
    sale(18, 50, "An $18 puzzle is 50% off. What is the sale price?", [F(35, 2), F(162, 10), 27],
         "50% is half: $18 ÷ 2 = <b>$9</b>. $17.50 takes away only 50¢, $16.20 takes off 10%, "
         "and $27 adds the discount.")
    sale(65, 20, "A $65 helmet is 20% off. What is the sale price?", [45, 13, F(585, 10)],
         "10% of $65 = $6.50, so 20% = $13. $65 − $13 = <b>$52</b>. $45 takes away 20 dollars, "
         "and $58.50 takes off only 10%.")
    sale(12, 5, "A $12 book is 5% off. What is the sale price?", [7, F(60, 100), F(108, 10)],
         "10% of $12 = $1.20, so 5% = 60¢. $12.00 − $0.60 = <b>$11.40</b>. $7 takes away 5 dollars, "
         "60¢ is the discount, and $10.80 takes off 10%.")
    sale(85, 30, "An $85 hockey jersey is 30% off. What is the sale price?", [55, F(255, 10), F(765, 10)],
         "10% of $85 = $8.50, so 30% = $25.50. $85 − $25.50 = <b>$59.50</b>. $55 takes away 30 dollars, "
         "and $76.50 takes off only 10%.")
    its.append(mcq("A $40 item is 25% off. Which calculation gives the sale price?", "75% of $40",
                   ["25% of $40", "$40 − 25", "$40 ÷ 25"],
                   "You pay what is left: 100% − 25% = 75%. So the sale price is <b>75% of $40</b> = $30. "
                   "25% of $40 = $10 is the discount."))
    its.append(mcq("A sign says “Pay only 70% of the price.” What percent is the discount?", "30%",
                   ["70%", "7%", "170%"],
                   "You pay 70%, so you save 100% − 70% = <b>30%</b>. 70% is the part you pay.", value=30))
    its.append(mcq("You save $9 on a $36 item. What percent is the discount?", "25%", ["9%", "4%", "75%"],
                   "$9 out of $36 = %s = %s = <b>25%%</b>. 9%% uses the dollars as a percent, 4%% is 36 ÷ 9, "
                   "and 75%% is the part you pay." % (fr(9, 36), fr(1, 4)), value=25))
    its.append(mcq("Skates were $50. Now they are on sale for $40. What percent is the discount?", "20%",
                   ["10%", "80%", "25%"],
                   "The discount is $50 − $40 = $10. $10 out of $50 = %s = <b>20%%</b>. 10%% uses the $10 as a percent, "
                   "and 25%% compares $10 to the sale price ($40), not the old price." % fr(1, 5), value=20))
    its.append(mcq(fig(percent_bar_svg("$60", 5, 1, "$12")) +
                   "The bar shows a $60 price in 5 equal parts. The shaded part is the discount. What is the sale price?",
                   "$48", ["$12", "$40", "$54"],
                   "Each part is $60 ÷ 5 = $12, and 1 part is shaded, so the discount is $12 (20%). "
                   "Sale price: $60 − $12 = <b>$48</b>. $12 is the discount, and $40 takes away 20 dollars.", value=48))
    assert 60 - pc(20, 60) == 48
    its.append(mcq("Store A takes $20 off a $120 coat. Store B takes 25% off the same coat. Which store saves you more?",
                   "Store B", ["Store A", "They save the same", "You can’t tell"],
                   "25%% of $120 = $120 ÷ 4 = $30. $30 &gt; $20, so <b>Store B</b> saves more. "
                   "($20 out of $120 is only %s, about 17%%.)" % fr(1, 6)))
    assert pc(25, 120) == 30
    its.append(mcq("A $48 tent is 25% off. You pay with a $50 bill. How much change do you get?",
                   "$14", ["$27", "$12", "$2"],
                   "25% of $48 = $12, so the sale price is $48 − $12 = $36. Change: $50 − $36 = <b>$14</b>. "
                   "$27 comes from taking 25 dollars off ($23), $12 is the discount, and $2 forgets the sale.", value=14))
    assert 50 - (48 - pc(25, 48)) == 14
    its.append(mcq("Leah paid $24 for a scarf that was 25% off. What was the price before the sale?",
                   "$32", ["$30", "$49", "$18"],
                   "She paid 100% − 25% = 75% of the price. 75% = $24, so 25% = $8 and 100% = 4 × $8 = <b>$32</b>. "
                   "Check: 25% of $32 = $8, and $32 − $8 = $24. $30 adds 25% of $24, but the 25% is of the "
                   "<b>original</b> price.", value=32))
    assert 32 - pc(25, 32) == 24
    assert len(its) == 20, len(its)
    return {"title": "Discounts and sale prices", "items": its}


# ============================================================ set 5: word problems
def set_problems(P):
    its = []
    its.append(mcq("Our school’s goal for the Terry Fox Run is $2000. So far we have raised $1500. "
                   "What percent of the goal is that?", "75%", ["25%", "15%", "50%"],
                   "%s = %s = <b>75%%</b>. 25%% is the part still to raise, and 15%% is 1500 ÷ 100."
                   % (fr(1500, 2000), fr(3, 4)), value=75))
    n, he, his = P.next()
    its.append(mcq("Ski rentals at Whistler cost $60 a day. During Spring Break, %s’s family gets 15%% off. "
                   "What is the sale price for one day?" % n, "$51", ["$45", "$9", "$54"],
                   "10% of $60 = $6 and 5% = $3, so 15% = $9. $60 − $9 = <b>$51</b>. $45 takes away 15 dollars, "
                   "$9 is the discount, and $54 takes off only 10%.", value=51))
    assert 60 - pc(15, 60) == 51
    its.append(mcq("In November, it rained in Vancouver on 24 of the 30 days. On what percent of the days did it rain?",
                   "80%", ["24%", "20%", "6%"],
                   "%s = %s = %s = <b>80%%</b>. 24%% forgets that the whole is 30, and 20%% is the dry days."
                   % (fr(24, 30), fr(4, 5), fr(80, 100)), value=80))
    its.append(mcq("A class of 25 students goes on a field trip to Stanley Park. 60% of them have been there before. "
                   "How many students have been there before?", "15", ["10", "6", "35"],
                   "10% of 25 = 2.5. 60% = 6 × 2.5 = <b>15</b> students. 10 is the other 40%, 6 is 60 ÷ 10, "
                   "and 35 subtracts 25 from 60.", value=15))
    assert pc(60, 25) == 15
    its.append(mcq("A soccer team won 9 of its 12 games. What percent of its games did it win?", "75%",
                   ["9%", "25%", "3%"],
                   "%s = %s = <b>75%%</b>. 25%% is the games it did not win, and 3%% is 12 − 9." % (fr(9, 12), fr(3, 4)),
                   value=75))
    its.append(mcq("A math test has 40 questions. Arjun gets 85% of them right. How many questions does he get right?",
                   "34", ["6", "8.5", "85"],
                   "10% of 40 = 4 and 5% = 2, so 85% = 8 × 4 + 2 = <b>34</b>. 6 is the questions he got wrong (15%), "
                   "8.5 is 10% of 85, and 85 uses the percent as the answer.", value=34))
    assert pc(85, 40) == 34
    its.append(mcq("A salmon hatchery on the Fraser River has 2000 eggs. 85% of them hatch. How many eggs hatch?",
                   "1700", ["300", "1915", "170"],
                   "10% of 2000 = 200 and 5% = 100, so 15% = 300 do <b>not</b> hatch. 2000 − 300 = <b>1700</b>. "
                   "300 is the eggs that do not hatch, and 1915 subtracts 85.", value=1700))
    assert pc(85, 2000) == 1700
    its.append(mcq("A survey asks a class for its favourite sport. 35% choose hockey, 40% choose soccer and the rest "
                   "choose lacrosse. What percent choose lacrosse?", "25%", ["75%", "65%", "60%"],
                   "All the students together are 100%. 35% + 40% = 75%, so 100% − 75% = <b>25%</b>. "
                   "75% is hockey and soccer together.", value=25))
    n, he, his = P.next()
    its.append(mcq("An $80 hockey jersey is 25%% off. %s pays with a $100 bill. How much change does %s get?" % (n, he),
                   "$40", ["$45", "$20", "$60"],
                   "25% of $80 = $20, so the sale price is $60. Change: $100 − $60 = <b>$40</b>. "
                   "$45 takes 25 dollars off ($55), $20 is the discount, and $60 is the sale price.", value=40))
    assert 100 - (80 - pc(25, 80)) == 40
    its.append(mcq("A fruit stand in the Okanagan sells a $20 box of cherries for 30% off. What is the sale price?",
                   "$14", ["$6", "$18", "$26"],
                   "10% of $20 = $2, so 30% = $6. $20 − $6 = <b>$14</b>. $6 is the discount, $18 takes off only 10%, "
                   "and $26 adds the discount.", value=14))
    assert 20 - pc(30, 20) == 14
    its.append(mcq("There are 30 students in a class. 40% of them bike to school. How many students do <b>not</b> bike?",
                   "18", ["12", "60", "3"],
                   "10% of 30 = 3, so 40% = 12 students bike. 30 − 12 = <b>18</b> do not. 12 is the bikers, "
                   "and 60 is the percent who do not bike (60%), not the number of students.", value=18))
    assert 30 - pc(40, 30) == 18
    its.append(mcq("A Grade 6 class of 120 students goes on a field trip. 5% forget their permission form. "
                   "How many students forget it?", "6", ["24", "115", "60"],
                   "10% of 120 = 12. 5% is half: <b>6</b>. 24 divides 120 by 5, which gives 20%, "
                   "and 115 subtracts 5.", value=6))
    assert pc(5, 120) == 6
    n, he, his = P.next()
    its.append(mcq("A hiking trail near Grouse Mountain is 3 km long. %s has hiked 60%% of it. How far does %s have left?"
                   % (n, he), "1.2 km", ["1.8 km", "2.4 km", "0.6 km"],
                   "%s has 100%% − 60%% = 40%% left. 10%% of 3 km = 0.3 km, so 40%% = <b>1.2 km</b>. "
                   "1.8 km is the part already hiked, and 2.4 km is 80%%." % n, value=F(6, 5)))
    assert 3 - pc(60, 3) == F(6, 5)
    its.append(mcq("A whale-watching boat in Victoria has 50 seats. 42 seats are full. What percent of the seats are full?",
                   "84%", ["42%", "16%", "8%"],
                   "50 × 2 = 100, so 42 × 2 = 84: <b>84%</b>. 42% forgets that the whole is 50, "
                   "and 16% is the empty seats.", value=84))
    n, he, his = P.next()
    its.append(mcq("%s sells 54 of the 60 tickets for the school raffle. What percent of the tickets has %s sold?"
                   % (n, he), "90%", ["54%", "10%", "6%"],
                   "%s = %s = <b>90%%</b>. 54%% forgets that the whole is 60, and 10%% is the tickets still to sell."
                   % (fr(54, 60), fr(9, 10)), value=90))
    its.append(mcq("A cedar seedling is 40 cm tall. By next year it grows 25% taller. How tall is it then?",
                   "50 cm", ["65 cm", "10 cm", "30 cm"],
                   "25% of 40 cm = 40 ÷ 4 = 10 cm. It grows 10 cm: 40 + 10 = <b>50 cm</b>. 65 cm adds 25 cm, "
                   "10 cm is only the growth, and 30 cm takes 25% away.", value=50))
    assert 40 + pc(25, 40) == 50
    its.append(mcq("A store in Burnaby sells a $90 skateboard for 20% off. A store in Surrey sells the same skateboard "
                   "for $80 with 10% off. Which sale price is lower?", "They cost the same",
                   ["The Burnaby store", "The Surrey store", "You can’t tell"],
                   "Burnaby: 20% of $90 = $18, so $90 − $18 = $72. Surrey: 10% of $80 = $8, so $80 − $8 = $72. "
                   "<b>They cost the same</b>, even though the Burnaby store gives the bigger percent off."))
    assert 90 - pc(20, 90) == 80 - pc(10, 80) == 72
    its.append(mcq("A pack of lacrosse balls costs $40. You can use a $5-off coupon or get 10% off. Which saves more?",
                   "The $5-off coupon", ["10% off", "They save the same", "You can’t tell"],
                   "10% of $40 = $4. $5 &gt; $4, so <b>the $5-off coupon</b> saves more on this price."))
    n, he, his = P.next()
    its.append(mcq("%s has saved $72. A $90 bike is 25%% off. After buying the bike, how much money will %s have left?"
                   % (n, he), "$4.50", ["$7", "$22.50", "$18"],
                   "25% of $90 = $22.50, so the sale price is $90 − $22.50 = $67.50. "
                   "$72 − $67.50 = <b>$4.50</b>. $7 comes from taking 25 dollars off ($65), "
                   "$22.50 is the discount, and $18 forgets the sale.", value=F(9, 2)))
    assert 72 - (90 - pc(25, 90)) == F(9, 2)
    n, he, his = P.next()
    its.append(mcq("%s pays $42 for a jacket that is 30%% off. What was the price before the sale?" % n,
                   "$60", ["$54.60", "$72", "$12.60"],
                   "%s paid 100%% − 30%% = 70%% of the price. 70%% = $42, so 10%% = $6 and 100%% = <b>$60</b>. "
                   "Check: 30%% of $60 = $18, and $60 − $18 = $42. $54.60 adds 30%% of $42, but the 30%% is of the "
                   "<b>original</b> price." % (he.capitalize()), value=60))
    assert 60 - pc(30, 60) == 42
    assert len(its) == 20, len(its)
    return {"title": "Word problems: sales, sports and trips around BC", "items": its}


# ============================================================ lesson
def body_html():
    f_grid = grid_svg(35)
    f_bar = percent_bar_svg("$40", 4, 1, "$10", W=480)
    return (
        "<h2>Percent means out of 100</h2>"
        "<p>A <b>percent</b> is a number out of 100. The sign % means “out of 100”. "
        "On a hundred grid, each square is 1%, and the whole grid is 100%.</p>"
        "<figure class='sn-fig'>" + f_grid +
        "<figcaption>35 of the 100 squares are shaded: 35%. The other 65 squares are 65%. Together they make 100%.</figcaption></figure>"
        + ex("Out of another whole", "Write 17 out of 50 as a percent.",
             "Make the whole 100: 50 × 2 = 100, so 17 × 2 = 34.", "34%")
        + "<h2>Percents, fractions and decimals</h2>"
        "<p>A percent is a fraction with a denominator of 100. It is also a decimal in hundredths. "
        "To change a percent to a decimal, divide by 100. To change a decimal to a percent, multiply by 100.</p>"
        + table(["Percent", "Fraction", "Decimal"], [
            ["50%", fr(1, 2), "0.5"],
            ["25%", fr(1, 4), "0.25"],
            ["75%", fr(3, 4), "0.75"],
            ["20%", fr(1, 5), "0.2"],
            ["10%", fr(1, 10), "0.1"],
            ["5%", fr(1, 20), "0.05"],
            ["1%", fr(1, 100), "0.01"],
        ])
        + "<h2>Percent of a number</h2>"
        "<p>Start from easy benchmarks. 10% means divide by 10. 1% means divide by 100. "
        "25% means divide by 4, and 50% means divide by 2. Then build the percent you need.</p>"
        + table(["Percent", "How to find it", "Of 60"], [
            ["10%", "divide by 10", "6"],
            ["5%", "half of 10%", "3"],
            ["15%", "10% + 5%", "9"],
            ["30%", "3 × 10%", "18"],
            ["25%", "divide by 4", "15"],
            ["75%", "3 × 25%", "45"],
        ])
        + "<h2>Discounts and sale prices</h2>"
        "<p>The <b>discount</b> is the money you save. The <b>sale price</b> is the price minus the discount. "
        "Find the discount first, then subtract.</p>"
        "<figure class='sn-fig'>" + f_bar +
        "<figcaption>$40 in 4 equal parts: each part is 25% = $10. 25% off takes away 1 part. You pay the other 3 parts: $30.</figcaption></figure>"
        + ex("Example", "An $80 pair of hiking boots is 20% off. What is the sale price?",
             "10% of $80 = $8, so 20% = $16. $80 − $16 = $64.", "$64")
        + "<h2>Common mistakes</h2>"
        + table(["Mistake", "What to do instead"], [
            ["25% off $40 = $40 − $25 = $15", "Find 25% of $40 first: $10. $40 − $10 = $30"],
            ["0.6 = 6%", "Multiply by 100: 0.6 = 60%"],
            [fr(3, 4) + " = 34%", "Make the denominator 100: " + fr(3, 4) + " = " + fr(75, 100) + " = 75%"],
            ["17 out of 50 = 17%", "Percent is out of 100: 17 out of 50 = 34 out of 100 = 34%"],
            ["Giving the discount as the answer", "Read the question: discount or sale price?"],
        ])
    )


FAQ = [
    {"q": "What do Grade 6 students learn about percents in BC?",
     "a": "The BC Grade 6 math curriculum includes whole-number percents and percentage discounts. Students see a percent as a number out of 100, change between percents, fractions and decimals, find a percent of a number and work out sale prices."},
    {"q": "How do you find a percent of a number without a calculator?",
     "a": "Use benchmarks: 10% means divide by 10, 5% is half of 10%, 25% means divide by 4 and 50% means divide by 2. Then combine them, so 15% of 60 is 6 + 3 = 9."},
    {"q": "How do you calculate a sale price with a percent discount?",
     "a": "Find the discount first, then subtract it from the price. For 25% off $40, the discount is $10 and the sale price is $30, not $40 − $25 = $15."},
    {"q": "How do you change a fraction to a percent?",
     "a": "Make the denominator 100. For example, 3/5 = 60/100 = 60%. If that is hard, divide the numerator by the denominator and multiply by 100: 3 ÷ 5 = 0.6, and 0.6 × 100 = 60%."},
]


def mark_large(u, pattern):
    """Tag pictures that must print larger (hundred grids, percent bars)."""
    rx = re.compile(r"<svg (?=[^>]*aria-label='" + pattern + ")")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u


def gen():
    rnd = random.Random(56805)
    P = People(rnd)
    sets = [set_out_of_100(), set_fdp(), set_percent_of(), set_discounts(), set_problems(P)]
    balance(sets, rnd)
    seen = set()
    for s in sets:
        assert len(s["items"]) == 20, (s["title"], len(s["items"]))
        assert sorted(it["a"] for it in s["items"]) == sorted([0, 1, 2, 3] * 5)
        for it in s["items"]:
            assert len(set(it["c"])) == 4, it
            assert it["q"].count("<svg") <= 1
            k = plain(it["q"]) + "|" + "|".join(sorted(it["c"]))
            assert k not in seen, it["q"]
            seen.add(k)
    u = {
        "country": "ca-bc", "subject": "math", "grade": "grade-6", "slug": "percents-and-discounts", "sort": 5,
        "updated": UPDATED, "pdf_url": "",
        "title": "Grade 6 Percents and Discounts",
        "seo_title": "Grade 6 Percents and Discounts Worksheets: Free Math Practice with Answer Key (BC Curriculum)",
        "short_title": "Percents and discounts",
        "domain": "Number",
        "standard_code": "Grade 6: Number",
        "standard_url": "https://curriculum.gov.bc.ca/curriculum/mathematics/6/core",
        "standard_text": "Whole-number percents and percentage discounts",
        "meta_desc": "Free Grade 6 math worksheets on percents and discounts for the BC curriculum: percent as out of 100 on hundred grids, changing between percents, fractions and decimals, percent of a number, and discounts and sale prices. 100 questions with an answer key.",
        "key_big": "Percent means out of 100: 35% = 35/100 = 0.35. For a sale price, find the discount first, then subtract it.",
        "key_sub": "25% off $40 is not $15: 25% of $40 is $40 ÷ 4 = $10, so the sale price is $40 − $10 = $30.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }
    return mark_large(u, "(hundred grid|percent bar)")


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
