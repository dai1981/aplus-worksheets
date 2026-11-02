# -*- coding: utf-8 -*-
"""
Canada (British Columbia) Grade 8 Math: Percents less than 1 and greater than 100
(BC Mathematics Curriculum, Grade 8, Content — Number:
 "percents less than 1 and greater than 100 (decimal and fractional percents)")
  python3 tools/gen_cabc_math_g8_percents.py
Percents over 100% (150% of 60), under 1% (0.5% of 4000), fractional percents (12½%, 33⅓%),
converting among fractions, decimals and percents, and BC word problems with GST 5% + PST 7% and growth.
Wrong answers come from real mistakes: 150% of 60 = 60 + 150, 0.5% = 0.5 (one half), 0.5% = 0.05,
12½% read as 12%, 33⅓% read as 0.33, percent "as many" read as "more", change divided by the new value.
Every answer is checked with fractions.Fraction (never float).
Canadian English, dollars and cents, metric units, SI number spacing. HTML attributes use single quotes.
"""
import json, os, random, re
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "ca-bc", "math", "grade-8")
UPDATED = "2026-11-02"
NBSP = " "
FILL = "#4fae74"
LINE = "#2b2b2b"
RED = "#d6453b"
BLUE = "#2f6fc0"
FONT = "Arial, Helvetica, sans-serif"
GIRLS = ["Olivia", "Ava", "Chloe", "Simran", "Jasleen", "Mei", "Ji-woo", "Hana", "Sofia", "Emma", "Leah", "Zara", "Nadia"]
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


def D(s):
    """Exact value of a decimal string."""
    return F(str(s))


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


def mixed(w, n, d):
    """2¼ -> '2' + fraction; w = 0 gives the fraction alone."""
    return (str(w) if w else "") + fr(n, d)


def fp(w, n, d):
    """Fractional percent: 12½%."""
    return mixed(w, n, d) + "%"


def plain(s):
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", s)).strip()


MIX = re.compile(r"^(\d*)<span class='fr'><span class='fn'>(\d+)</span><span class='fd'>(\d+)</span></span>(%)?$")
NUM = re.compile(r"^(\$)?(\d[\d" + NBSP + r"]*(?:\.\d+)?)(¢|%)?( .+)?$")


def val(c):
    """Value of a choice with its unit, or None when it is not a single number."""
    m = MIX.match(c)
    if m:
        return (int(m.group(1) or 0) + F(int(m.group(2)), int(m.group(3))), "%" if m.group(4) else "")
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
def percent_line_svg(pcts, amts, label):
    """Double number line: percents above, amounts below, at positions proportional to the percent.
    '?' is drawn in red. The 100% tick is drawn taller."""
    fs = 16
    nw = max(tw("Percent", fs), tw("Amount", fs)) + 8
    top = max(pcts)
    sp_min = max([58] + [tw(t, fs) + 14 for t in amts] + [tw(num(p) + "%", fs) + 14 for p in pcts])
    steps = sorted(set(pcts))
    gaps = [b - a for a, b in zip(steps, steps[1:])]
    unit = sp_min / float(min(gaps))          # pixels per 1%
    x0 = 8 + nw + 18
    x1 = x0 + top * unit
    W = int(x1 + sp_min / 2 + 6)
    yt, yb = 36, 70
    s = [text(8 + nw / 2, yt + 5, "Percent", fs, col=BLUE), text(8 + nw / 2, yb + 5, "Amount", fs, col=BLUE)]
    for y in (yt, yb):
        s.append("<line x1='%.1f' y1='%d' x2='%.1f' y2='%d' stroke='%s' stroke-width='2.5'/>" % (x0 - 6, y, x1 + 16, y, LINE))
    for p, a in zip(pcts, amts):
        x = x0 + p * unit
        h = 11 if p == 100 else 8
        for y in (yt, yb):
            s.append("<line x1='%.1f' y1='%d' x2='%.1f' y2='%d' stroke='%s' stroke-width='2'/>" % (x, y - h, x, y + h, LINE))
        s.append(text(x, yt - 15, num(p) + "%", fs))
        s.append(text(x, yb + 29, a, fs, col=RED if a == "?" else LINE))
    return svg_wrap(W, yb + 37, "".join(s), label)


def hundred_grid_svg(halves, label):
    """10 × 10 grid = 100 squares. halves: number of half squares shaded, filled row by row
    (whole squares first; an odd count ends with the left half of the next square)."""
    c, m = 20, 6
    W = m * 2 + 10 * c
    s = []
    whole, half = divmod(halves, 2)
    for i in range(whole):
        r, k = divmod(i, 10)
        s.append("<rect x='%d' y='%d' width='%d' height='%d' fill='%s'/>" % (m + k * c, m + r * c, c, c, FILL))
    if half:
        r, k = divmod(whole, 10)
        s.append("<rect x='%d' y='%d' width='%d' height='%d' fill='%s'/>" % (m + k * c, m + r * c, c // 2, c, FILL))
    for i in range(11):
        w = 2.5 if i in (0, 10) else 1.2
        s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='%s'/>" % (m + i * c, m, m + i * c, m + 10 * c, LINE, w))
        s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='%s'/>" % (m, m + i * c, m + 10 * c, m + i * c, LINE, w))
    return svg_wrap(W, W, "".join(s), label)


# ============================================================ set 1: percents over 100%
def set_over_100():
    its = []

    def pq(p, n, wrong, e, q=None, fg=""):
        r = pc(p, n)
        its.append(mcq(fg + (q or "What is %s%% of %s?" % (num(p), num(n))), num(r), [num(w) for w in wrong], e, value=r))

    pq(200, 45, [245, D("22.5"), 9],                                                     # 0
       "200% = 2, so 200% of 45 = 2 × 45 = <b>90</b>. 245 adds 200 to 45, 22.5 halves 45 instead of doubling it, "
       "and 9 uses 0.2 instead of 2.")
    pq(150, 60, [210, 30, 900],                                                          # 1
       "150% = 1.5. 1.5 × 60 = <b>90</b>. Or: 100% of 60 is 60 and 50% is 30, so 60 + 30 = 90. "
       "210 adds 150 to 60, 30 is only the extra 50%, and 900 uses 15 instead of 1.5.")
    pq(300, 15, [315, 5, 60],                                                            # 2
       "300% = 3. 3 × 15 = <b>45</b>. 315 adds 300 to 15, 5 divides by 3, and 60 is 400%.")
    pq(125, 48, [173, 12, 600],                                                          # 3
       "125% = 1.25. 100% of 48 is 48 and 25% is 12, so 48 + 12 = <b>60</b>. "
       "173 adds 125 to 48, 12 is only the extra 25%, and 600 uses 12.5 instead of 1.25.")
    pq(110, 70, [180, 7, 770],                                                           # 4
       "110% = 100% + 10%. 70 + 7 = <b>77</b>. 180 adds 110 to 70, 7 is only 10%, and 770 uses 11 instead of 1.1.")
    pq(250, 22, [272, 44, 11],                                                           # 5
       "250% = 2.5. 2 × 22 = 44 and 0.5 × 22 = 11, so 44 + 11 = <b>55</b>. 272 adds 250 to 22, "
       "44 is only 200%, and 11 is only 50%.")
    pq(120, 35, [155, 7, 420],                                                           # 6
       "120% = 1.2. 100% of 35 is 35 and 20% is 7, so 35 + 7 = <b>42</b>. 155 adds 120 to 35, "
       "7 is only the extra 20%, and 420 uses 12 instead of 1.2.")
    pq(175, 36, [211, 27, 630],                                                          # 7
       "175% = 1.75. 100% of 36 is 36 and 75% is 27, so 36 + 27 = <b>63</b>. 211 adds 175 to 36, "
       "27 is only 75%, and 630 uses 17.5 instead of 1.75.")
    pq(450, 6, [456, 24, D("2.7")],                                                      # 8
       "450% = 4.5. 4 × 6 = 24 and 0.5 × 6 = 3, so 24 + 3 = <b>27</b>. 456 adds 450 to 6, 24 is only 400%, "
       "and 2.7 uses 0.45 instead of 4.5.")
    pq(105, 400, [505, 20, 4200],                                                        # 9
       "105% = 100% + 5%. 5% of 400 is 20, so 400 + 20 = <b>420</b>. 505 adds 105 to 400, "
       "20 is only 5%, and 4200 uses 10.5 instead of 1.05.")
    pq(150, 56, [206, 28, 112],                                                          # 10
       "On the line, 100% matches 56, so 50% matches 28. 150% = 100% + 50%: 56 + 28 = <b>84</b>. "
       "206 adds 150 to 56, 28 is only 50%, and 112 is 200%.",
       q="The double number line shows that 100% is 56. What amount matches 150%?",
       fg=fig(percent_line_svg([0, 50, 100, 150], ["0", "28", "56", "?"], "percent line: 100% is 56, 150% is unknown")))
    its.append(mcq("Which calculation finds 175% of 32?", "1.75 × 32", ["17.5 × 32", "0.175 × 32", "32 + 175"],   # 11
                   "Percent means out of 100, so 175% = 175 ÷ 100 = 1.75. The calculation is <b>1.75 × 32</b> (= 56). "
                   "17.5 and 0.175 move the decimal point the wrong number of places, and 32 + 175 adds the percent."))
    its.append(mcq("Without calculating, which amount is greater than 90?", "110% of 90",                       # 12
                   ["90% of 90", "99% of 90", "100% of 90"],
                   "100% of 90 is 90 itself. A percent <b>greater than</b> 100% gives more than the number, so "
                   "<b>110% of 90</b> is greater than 90. 90% and 99% give less than 90, and 100% gives exactly 90."))
    its.append(mcq("21 is what percent of 14?", "150%", ["50%", "1.5%", "7%"],                                   # 13
                   fr(21, 14) + " = 1.5 = <b>150%</b>. 21 is more than 14, so the answer must be more than 100%. "
                   "50% is only the extra 7, 1.5% forgets to multiply by 100, and 7% uses the difference.", value=150))
    its.append(mcq("52 is what percent of 16?", "325%", ["225%", "3.25%", "36%"],                               # 14
                   fr(52, 16) + " = 3.25 = <b>325%</b>. Check: 3.25 × 16 = 52. 225% is only the extra 36 compared "
                   "with 16, 3.25% forgets to multiply by 100, and 36% uses the difference 52 − 16.", value=325))
    its.append(mcq("Which is greater: 250% of 12 or 12% of 250?", "They are equal",                             # 15
                   ["250% of 12", "12% of 250", "You can’t tell"],
                   "250% of 12 = 2.5 × 12 = 30. 12% of 250 = 0.12 × 250 = 30. <b>They are equal</b>: "
                   "a% of b is always the same as b% of a."))
    its.append(mcq("125% of a number is 50. What is the number?", "40", ["62.5", "37.5", "400"],                 # 16
                   "1.25 × ? = 50, so ? = 50 ÷ 1.25 = <b>40</b>. Check: 125% of 40 = 40 + 10 = 50. "
                   "62.5 is 125% of 50 (the wrong way round), 37.5 takes 25% of 50 away, and 400 divides by 0.125.",
                   value=40))
    its.append(mcq("300% of a number is 84. What is the number?", "28", ["252", "280", "0.28"],                  # 17
                   "300% = 3, so 3 × ? = 84 and ? = 84 ÷ 3 = <b>28</b>. "
                   "252 is 300% of 84 (the wrong way round), 280 divides by 0.3, and 0.28 divides by 300 "
                   "without changing the percent to a decimal.", value=28))
    its.append(mcq("Which statement is true?", "140% of 50 = 70",                                               # 18
                   ["140% of 50 = 190", "140% of 50 = 7", "140% of 50 = 700"],
                   "140% = 1.4, and 1.4 × 50 = 70, so <b>140% of 50 = 70</b>. 190 adds 140 + 50, "
                   "7 is only 14%, and 700 uses 14 instead of 1.4."))
    its.append(mcq("What percent of 80 is 200?", "250%", ["120%", "40%", "2.5%"],                                # 19
                   fr(200, 80) + " = 2.5 = <b>250%</b>. 200 is more than 80, so the percent is more than 100%. "
                   "120% uses the difference 200 − 80, 40% divides the wrong way (80 ÷ 200), and 2.5% forgets "
                   "to multiply by 100.", value=250))
    assert pc(140, 50) == 70 and pc(250, 12) == pc(12, 250) == 30 and pc(175, 32) == 56
    assert F(50) / D("1.25") == 40 and pc(125, 50) == D("62.5") and F(50) / D("0.125") == 400
    assert len(its) == 20, len(its)
    order = [0, 1, 2, 12, 11, 4, 3, 6, 5, 7, 9, 8, 10, 13, 14, 18, 15, 19, 16, 17]
    assert sorted(order) == list(range(20))
    its = [its[i] for i in order]
    return {"title": "Percents greater than 100%: 150%, 250% and 450% of a number", "items": its}


# ============================================================ set 2: percents under 1%
def set_under_1():
    its = []

    def pq(p, n, wrong, e, q=None):
        r = pc(D(p), n)
        its.append(mcq(q or "What is %s%% of %s?" % (num(D(p)), num(n)), num(r), [num(w) for w in wrong], e, value=r))

    pq(1, 3000, [300, 3, D("0.3")],                                                       # 0
       "1% means divide by 100: 3000 ÷ 100 = <b>30</b>. 300 is 10%, 3 is 0.1%, and 0.3 is 0.01%.")
    pq("0.5", 4000, [2000, 200, 2],                                                       # 1
       "1% of 4000 is 40. 0.5% is <b>half of 1%</b>: 40 ÷ 2 = <b>20</b>. "
       "2000 treats 0.5% as one half (50%), 200 is 5%, and 2 is 0.05%.")
    pq("0.1", 6000, [600, 60, D("0.6")],                                                  # 2
       "1% of 6000 is 60. 0.1% is one tenth of 1%: 60 ÷ 10 = <b>6</b>. 600 is 10%, 60 is 1%, and 0.6 is 0.01%.")
    pq("0.5", 600, [300, 30, D("0.3")],                                                   # 3
       "1% of 600 is 6, so 0.5% is half of 6 = <b>3</b>. 300 treats 0.5% as one half, 30 is 5%, and 0.3 is 0.05%.")
    pq("0.25", 800, [200, 20, D("0.2")],                                                  # 4
       "1% of 800 is 8. 0.25% is a quarter of 1%: 8 ÷ 4 = <b>2</b>. 200 is 25%, 20 is 2.5%, and 0.2 is 0.025%.")
    pq("0.2", 2500, [500, 50, D("0.5")],                                                  # 5
       "1% of 2500 is 25. 0.2% = 0.2 × 25 = <b>5</b>. 500 is 20%, 50 is 2%, and 0.5 is 0.02%.")
    pq("0.75", 2400, [1800, 180, D("1.8")],                                               # 6
       "1% of 2400 is 24. 0.75% is three quarters of 1%: 24 ÷ 4 × 3 = <b>18</b>. 1800 is 75%, 180 is 7.5%, "
       "and 1.8 is 0.075%.")
    pq("0.1", 35000, [3500, 350, D("3.5")],                                               # 7
       "0.1% = 0.001, so divide by 1000: 35" + NBSP + "000 ÷ 1000 = <b>35</b>. 3500 is 10%, 350 is 1%, "
       "and 3.5 is 0.01%.")
    pq("0.6", 1500, [900, 90, D("0.9")],                                                  # 8
       "1% of 1500 is 15. 0.6% = 0.6 × 15 = <b>9</b>. 900 is 60%, 90 is 6%, and 0.9 is 0.06%.")
    pq("0.3", 7000, [2100, 210, D("2.1")],                                                # 9
       "1% of 7000 is 70. 0.3% = 0.3 × 70 = <b>21</b>. 2100 is 30%, 210 is 3%, and 2.1 is 0.03%.")
    pq("0.05", 40000, [2000, 200, 2],                                                     # 10
       "1% of 40" + NBSP + "000 is 400. 0.05% is one twentieth of 1%: 400 ÷ 20 = <b>20</b>. "
       "2000 is 5%, 200 is 0.5%, and 2 is 0.005%.")
    pq("0.8", 250, [200, 20, D("0.2")],                                                   # 11
       "1% of 250 is 2.5. 0.8% = 0.8 × 2.5 = <b>2</b>. 200 is 80%, 20 is 8%, and 0.2 is 0.08%.")
    pq("0.5", 48, [24, D("2.4"), D("0.024")],                                             # 12
       "1% of 48 is 0.48. 0.5% is half of that: <b>0.24</b>. 24 treats 0.5% as one half, 2.4 is 5%, "
       "and 0.024 is 0.05%.")
    its.append(mcq(fig(hundred_grid_svg(1, "hundred grid: half of one square shaded")) +                       # 13
                   "The grid has 100 equal squares. What percent of the grid is shaded?",
                   "0.5%", ["5%", "50%", "0.05%"],
                   "One whole square is 1% of the grid. Only half of one square is shaded, so the shaded part is "
                   "<b>0.5%</b>: less than 1%. 50% would be half of the <b>whole grid</b>.", value=D("0.5")))
    its.append(mcq("4 is what percent of 1000?", "0.4%", ["4%", "40%", "0.04%"],                              # 14
                   fr(4, 1000) + " = 0.004. Multiply by 100: <b>0.4%</b>. 4% would be 40 out of 1000.", value=D("0.4")))
    its.append(mcq("1 is what percent of 200?", "0.5%", ["50%", "5%", "0.005%"],                                   # 15
                   fr(1, 200) + " = 0.005 = <b>0.5%</b>. Check: 1% of 200 is 2, so 1 is half of 1%. "
                   "50% mixes up " + fr(1, 200) + " with " + fr(1, 2) + ", 5% moves the decimal point 3 places, "
                   "and 0.005% forgets to multiply by 100.",
                   value=D("0.5")))
    its.append(mcq("0.5% of a number is 9. What is the number?", "1800", ["18", "4.5", "180"],                 # 16
                   "0.5% = 0.005, so ? = 9 ÷ 0.005 = <b>1800</b>. Or: 0.5% is 9, so 1% is 18 and 100% is 1800. "
                   "18 divides by 0.5 (treats 0.5% as 0.5), 4.5 takes half of 9, and 180 divides by 0.05.", value=1800))
    its.append(mcq("Which amount is <b>less</b> than 1% of 600?", "0.9% of 600",                              # 17
                   ["1.1% of 600", "10% of 60", "2% of 300"],
                   "1% of 600 = 6. 0.9% of 600 = 5.4, which is less, so <b>0.9% of 600</b>. "
                   "1.1% of 600 = 6.6, and 10% of 60 and 2% of 300 are both exactly 6."))
    its.append(mcq("Which list is in order from least to greatest?", "0.07%, 0.6%, 1%",                       # 18
                   ["0.6%, 1%, 0.07%", "1%, 0.6%, 0.07%", "0.6%, 0.07%, 1%"],
                   "Compare the decimals: 0.07 &lt; 0.60 &lt; 1. So <b>0.07%, 0.6%, 1%</b>. "
                   "0.07% has the digit 7, but it is less than one tenth of 1%."))
    its.append(mcq("Which is equal to 0.5% of 600?", "1% of 300", ["5% of 600", "50% of 600", "0.5% of 60"],  # 19
                   "0.5% of 600 = 3. 1% of 300 = 3 too, so <b>1% of 300</b>. "
                   "5% of 600 = 30, 50% of 600 = 300, and 0.5% of 60 = 0.3."))
    assert pc(D("0.5"), 600) == pc(1, 300) == 3 and pc(D("0.9"), 600) == D("5.4") and pc(D("1.1"), 600) == D("6.6")
    assert F(9) / D("0.005") == 1800
    assert len(its) == 20, len(its)
    order = [0, 1, 2, 3, 13, 4, 5, 7, 8, 9, 14, 15, 11, 10, 6, 12, 17, 18, 19, 16]
    assert sorted(order) == list(range(20))
    its = [its[i] for i in order]
    return {"title": "Percents less than 1%: 0.5%, 0.25% and 0.1% of a number", "items": its}


# ============================================================ set 3: fractional percents
def set_fractional():
    its = []
    h = fp(12, 1, 2)          # 12½%
    t = fp(33, 1, 3)          # 33⅓%

    def pq(w, n, d, base, wrong, e):
        p = w + F(n, d)
        r = pc(p, base)
        its.append(mcq("What is %s of %s?" % (fp(w, n, d), num(base)), num(r), [num(x) for x in wrong], e, value=r))

    its.append(mcq("Write %s as a decimal." % h, "0.125", ["0.12", "1.25", "12.5"],                           # 0
                   h + " = 12.5%. Divide by 100: move the decimal point 2 places left. 12.5% = <b>0.125</b>. "
                   "0.12 drops the half, 1.25 moves only one place, and 12.5 forgets to divide.", value=D("0.125")))
    its.append(mcq("Write %s as a fraction in simplest form." % h, fr(1, 8), [fr(3, 25), fr(1, 80), fr(25, 2)],  # 1
                   h + " = " + fr("12.5", 100) + " = " + fr(125, 1000) + " = <b>" + fr(1, 8) + "</b>. "
                   + fr(3, 25) + " is 12% (the half is dropped), " + fr(1, 80) + " is 1.25%, and " + fr(25, 2)
                   + " is 12" + fr(1, 2) + " itself, not divided by 100.", value=F(1, 8)))
    its.append(mcq("Write %s as a decimal." % fp(0, 1, 4), "0.0025", ["0.25", "0.025", "25"],                 # 2
                   fp(0, 1, 4) + " = 0.25%. Divide by 100: <b>0.0025</b>. 0.25 forgets to divide (that is 25%), "
                   "0.025 moves only one place, and 25 multiplies by 100 instead of dividing.", value=D("0.0025")))
    its.append(mcq("Which fraction is equal to %s?" % t, fr(1, 3), [fr(33, 100), fr(1, 33), fr(3, 10)],       # 3
                   t + " means 33" + fr(1, 3) + " out of 100. Since 3 × 33" + fr(1, 3) + " = 100, this is <b>"
                   + fr(1, 3) + "</b>. " + fr(33, 100) + " drops the " + fr(1, 3) + ", " + fr(1, 33)
                   + " uses 33 as the denominator, and " + fr(3, 10) + " is 30%.", value=F(1, 3)))
    its.append(mcq("Write %s as a percent." % fr(1, 8), h, ["8%", "18%", fp(0, 1, 8)],                       # 4
                   "1 ÷ 8 = 0.125. Multiply by 100: 12.5% = <b>" + h + "</b>. 8% uses the denominator, 18% joins "
                   "the digits, and " + fp(0, 1, 8) + " forgets to multiply by 100.", value=D("12.5")))
    its.append(mcq("Write %s as a percent." % fr(1, 200), fp(0, 1, 2), ["50%", "200%", "0.005%"],            # 5
                   "1 ÷ 200 = 0.005. Multiply by 100: <b>" + fp(0, 1, 2) + "</b> (0.5%). 50% mixes up "
                   + fr(1, 200) + " with " + fr(1, 2) + ", 200% uses the denominator, and 0.005% forgets "
                   "to multiply by 100.", value=F(1, 2)))
    its.append(mcq(fig(hundred_grid_svg(25, "hundred grid: 12 and a half squares shaded")) +                  # 6
                   "The grid has 100 equal squares. What percent of the grid is shaded?",
                   h, ["25%", "12%", "13%"],
                   "12 whole squares are shaded (12%) and then half of one more square (" + fp(0, 1, 2) + "). "
                   "12% + " + fp(0, 1, 2) + " = <b>" + h + "</b>. 25% doubles the count, 12% leaves out the half square, "
                   "and 13% counts the half square as a whole one.", value=D("12.5")))
    pq(12, 1, 2, 64, [D("7.68"), 80, D("0.8")],                                                               # 7
       h + " = " + fr(1, 8) + ", so " + h + " of 64 = 64 ÷ 8 = <b>8</b>. 7.68 is only 12% (the half is dropped), "
       "80 uses 1.25, and 0.8 uses 0.0125.")
    pq(2, 1, 2, 400, [8, 100, 1],                                                                             # 8
       "1% of 400 is 4. " + fp(2, 1, 2) + " = 2.5 × 4 = <b>10</b>. 8 is only 2% (the half is dropped), "
       "100 is 25%, and 1 is 0.25%.")
    pq(0, 1, 2, 1200, [600, 60, D("0.6")],                                                                    # 9
       fp(0, 1, 2) + " means half of 1%, not half. 1% of 1200 is 12, so " + fp(0, 1, 2) + " is <b>6</b>. "
       "600 treats " + fp(0, 1, 2) + " as one half (50%), 60 is 5%, and 0.6 is 0.05%.")
    pq(0, 1, 4, 2000, [500, 50, D("0.5")],                                                                    # 10
       "1% of 2000 is 20. " + fp(0, 1, 4) + " is a quarter of 1%: 20 ÷ 4 = <b>5</b>. 500 is 25%, 50 is 2.5%, "
       "and 0.5 is 0.025%.")
    pq(1, 1, 2, 600, [6, 90, D("0.9")],                                                                       # 11
       "1% of 600 is 6, and " + fp(0, 1, 2) + " of 600 is 3. " + fp(1, 1, 2) + ": 6 + 3 = <b>9</b>. "
       "6 is only 1% (the half is dropped), 90 is 15%, and 0.9 is 0.15%.")
    pq(33, 1, 3, 27, [D("8.91"), 81, D("0.9")],                                                               # 12
       t + " = " + fr(1, 3) + ", so " + t + " of 27 = 27 ÷ 3 = <b>9</b>. 8.91 uses 0.33 × 27, which is a little "
       "too small, 81 multiplies by 3, and 0.9 is " + fp(3, 1, 3) + ".")
    pq(6, 1, 4, 160, [D("9.6"), 100, 1],                                                                      # 13
       fp(6, 1, 4) + " = 6.25% = " + fr(1, 16) + ", so 160 ÷ 16 = <b>10</b>. 9.6 is only 6% (the quarter is "
       "dropped), 100 uses 0.625, and 1 uses 0.00625.")
    pq(37, 1, 2, 48, [30, D("17.76"), 180],                                                                   # 14
       fp(37, 1, 2) + " = " + fr(3, 8) + ". 48 ÷ 8 = 6, and 3 × 6 = <b>18</b>. 30 is " + fr(5, 8)
       + " of 48, 17.76 is only 37% (the half is dropped), and 180 uses 3.75.")
    pq(66, 2, 3, 45, [15, D("29.7"), 300],                                                                    # 15
       fp(66, 2, 3) + " = " + fr(2, 3) + ". 45 ÷ 3 = 15, and 2 × 15 = <b>30</b>. 15 is only " + fr(1, 3)
       + ", 29.7 uses 0.66 × 45, and 300 uses 6" + fr(2, 3) + " instead of " + fr(2, 3) + ".")
    pq(87, 1, 2, 40, [5, D("34.8"), 350],                                                                     # 16
       fp(87, 1, 2) + " = " + fr(7, 8) + ". 40 ÷ 8 = 5, and 7 × 5 = <b>35</b>. 5 is only " + h
       + " (the part left out), 34.8 is only 87%, and 350 uses 8.75.")
    its.append(mcq("Write %s as a percent." % fr(5, 8), fp(62, 1, 2), ["58%", fp(6, 1, 4), "160%"],           # 17
                   "5 ÷ 8 = 0.625. Multiply by 100: 62.5% = <b>" + fp(62, 1, 2) + "</b>. 58% joins the digits, "
                   + fp(6, 1, 4) + " multiplies by 10 instead of 100, and 160% is " + fr(8, 5) + " (the fraction flipped).",
                   value=D("62.5")))
    its.append(mcq("Which is equal to %s of 80?" % h, "25% of 40", ["12% of 80", h + " of 8", "25% of 80"],   # 18
                   h + " of 80 = 80 ÷ 8 = 10. 25% of 40 = 40 ÷ 4 = 10 too, so <b>25% of 40</b>. "
                   "12% of 80 = 9.6, " + h + " of 8 = 1, and 25% of 80 = 20."))
    its.append(mcq("%s of a number is 9. What is the number?" % h, "72", ["112.5", "0.72", "1.125"],          # 19
                   h + " = " + fr(1, 8) + ", so 9 is one eighth of the number: 9 × 8 = <b>72</b>. "
                   "Check: 72 ÷ 8 = 9. 112.5 multiplies 9 by 12.5, 0.72 divides 9 by 12.5, and 1.125 is "
                   + h + " of 9 (the wrong way round).", value=72))
    assert pc(D("12.5"), 80) == pc(25, 40) == 10 and pc(12, 80) == D("9.6") and pc(D("12.5"), 8) == 1
    assert F(9) / D("0.125") == 72 and F(9) * D("12.5") == D("112.5") and pc(D("12.5"), 9) == D("1.125")
    assert pc(12, 64) == D("7.68") and pc(37, 48) == D("17.76") and pc(66, 45) == D("29.7") and pc(87, 40) == D("34.8")
    assert pc(F(10, 3), 27) == D("0.9") and pc(6, 160) == D("9.6")
    assert len(its) == 20, len(its)
    order = [0, 1, 2, 4, 3, 5, 6, 9, 8, 10, 7, 11, 12, 13, 14, 15, 16, 17, 18, 19]
    assert sorted(order) == list(range(20))
    its = [its[i] for i in order]
    return {"title": "Fractional percents: 12½%, 33⅓% and ½% of a number", "items": its}


# ============================================================ set 4: converting among forms
def set_convert():
    its = []

    def conv(q, right, wrong, e, value, same_ok=False):
        its.append(mcq(q, right, wrong, e, value=value, same_ok=same_ok))

    conv("Write 0.5% as a decimal.", "0.005", ["0.5", "0.05", "5"],                                           # 0
         "Percent means out of 100, so divide by 100: move the decimal point 2 places left. "
         "0.5% = <b>0.005</b>. 0.5 forgets to divide (0.5 is 50%), 0.05 moves only one place, and 5 multiplies by 10.",
         D("0.005"))
    conv("Write 175% as a decimal.", "1.75", ["0.175", "17.5", "175"],                                         # 1
         "Divide by 100: 175% = 175 ÷ 100 = <b>1.75</b>. 175% is more than 100%, so the decimal is more than 1.",
         D("1.75"))
    conv("Write 0.09 as a percent.", "9%", ["0.09%", "90%", "0.9%"],                                           # 2
         "Multiply by 100: move the decimal point 2 places right. 0.09 = <b>9%</b>. 90% would be 0.9.", 9)
    conv("Write 3.2 as a percent.", "320%", ["32%", "3.2%", "0.32%"],                                          # 3
         "Multiply by 100: 3.2 × 100 = <b>320%</b>. 3.2 is more than 1, so the percent is more than 100%. "
         "32% moves the decimal point only one place.", 320)
    conv("Write 0.006 as a percent.", "0.6%", ["6%", "60%", "0.06%"],                                          # 4
         "Multiply by 100: 0.006 × 100 = <b>0.6%</b>. The number is less than 0.01, so the percent is less than 1%.",
         D("0.6"))
    conv("Write " + fr(7, 8) + " as a percent.", "87.5%", ["7.8%", "0.875%", "12.5%"],                         # 5
         "7 ÷ 8 = 0.875. Multiply by 100: <b>87.5%</b>. 7.8% reads " + fr(7, 8) + " as 7.8, 0.875% forgets to "
         "multiply by 100, and 12.5% is " + fr(1, 8) + ".", D("87.5"))
    conv("Write " + fr(7, 4) + " as a percent.", "175%", ["1.75%", "17.5%", "74%"],                            # 6
         "7 ÷ 4 = 1.75 = <b>175%</b>. The fraction is more than 1, so the percent is more than 100%. "
         "1.75% forgets to multiply by 100, and 74% joins the digits.", 175)
    conv("Write " + fr(1, 250) + " as a percent.", "0.4%", ["4%", "250%", "0.004%"],                           # 7
         "1 ÷ 250 = 0.004. Multiply by 100: <b>0.4%</b>. 4% would be " + fr(1, 25) + ", 250% uses the "
         "denominator, and 0.004% forgets to multiply by 100.", D("0.4"))
    conv("Write 0.3% as a fraction.", fr(3, 1000), [fr(3, 10), fr(3, 100), fr(3, 10000)],                      # 8
         "0.3% = " + fr("0.3", 100) + ". Multiply top and bottom by 10: <b>" + fr(3, 1000) + "</b>. "
         + fr(3, 10) + " is 30%, and " + fr(3, 100) + " is 3%.", F(3, 1000))
    conv("Write 225% as a mixed number.", mixed(2, 1, 4), [mixed(22, 1, 2), mixed(2, 2, 5), fr(1, 4)],         # 9
         "225% = " + fr(225, 100) + " = 2.25 = <b>" + mixed(2, 1, 4) + "</b>. " + mixed(22, 1, 2)
         + " divides by 10 instead of 100, " + mixed(2, 2, 5) + " reads .25 as “2 over 5”, and " + fr(1, 4)
         + " forgets the 2 wholes.", F(9, 4))
    conv("Write " + mixed(1, 3, 5) + " as a percent.", "160%", ["1.6%", "16%", "60%"],                          # 10
         mixed(1, 3, 5) + " = 1.6. Multiply by 100: <b>160%</b>. 60% forgets the whole, and 1.6% forgets to "
         "multiply by 100.", 160)
    conv("Write 0.45% as a decimal.", "0.0045", ["0.45", "0.045", "4.5"],                                      # 11
         "Divide by 100: move the decimal point 2 places left. 0.45% = <b>0.0045</b>. "
         "0.45 forgets to divide, and 0.045 moves only one place.", D("0.0045"))
    conv("Write 1.08 as a percent.", "108%", ["10.8%", "1.08%", "18%"],                                        # 12
         "1.08 × 100 = <b>108%</b>. 10.8% moves the decimal point only one place, and 18% drops the zero.", 108)
    its.append(mcq("Which is equal to 0.8%?", fr(1, 125), ["0.08", "0.8", "8"],                                # 13
                   "0.8% = 0.8 ÷ 100 = 0.008 = " + fr(8, 1000) + " = <b>" + fr(1, 125) + "</b>. "
                   "0.08 is 8%, 0.8 is 80%, and 8 is 800%."))
    assert D("0.008") == F(1, 125)
    its.append(mcq("Which is equal to " + fr(1, 500) + "?", "0.2%", ["2%", "20%", "0.02%"],                   # 14
                   fr(1, 500) + " = 0.002. Multiply by 100: <b>0.2%</b>. 2% is " + fr(1, 50) + ".", value=D("0.2")))
    its.append(mcq("Which is greater: 0.6% or 0.06?", "0.06", ["0.6%", "They are equal", "You can’t tell"],    # 15
                   "Write both as decimals. 0.6% = 0.006. 0.06 &gt; 0.006, so <b>0.06</b> is greater "
                   "(0.06 = 6%)."))
    its.append(mcq("Which number is greatest?", "1.4", ["135%", fr(11, 8), "0.9%"],                            # 16
                   "Write all as decimals: 1.4, 135% = 1.35, " + fr(11, 8) + " = 1.375, 0.9% = 0.009. "
                   "The greatest is <b>1.4</b>. 135 looks big, but 135% is only 1.35."))
    assert D("1.4") > F(11, 8) > D("1.35")
    its.append(mcq("Which is <b>not</b> equal to 2.5?", "25%", ["250%", fr(5, 2), mixed(2, 1, 2)],             # 17
                   "250% = 2.5, " + fr(5, 2) + " = 2.5 and " + mixed(2, 1, 2) + " = 2.5. <b>25%</b> = 0.25, so it "
                   "is not equal to 2.5.", same_ok=True))
    its.append(mcq("Which list is in order from least to greatest?",                                           # 18
                   "99%, 1.05, " + mixed(1, 1, 8),
                   [mixed(1, 1, 8) + ", 1.05, 99%", "1.05, 99%, " + mixed(1, 1, 8), "99%, " + mixed(1, 1, 8) + ", 1.05"],
                   "Write all as decimals: 99% = 0.99, 1.05, " + mixed(1, 1, 8) + " = 1.125. So the order is <b>99%, 1.05, "
                   + mixed(1, 1, 8) + "</b>. 99% is just under 1."))
    its.append(mcq("Which shows " + fr(3, 400) + " as a decimal and as a percent?", "0.0075 and 0.75%",        # 19
                   ["0.075 and 7.5%", "0.75 and 75%", "0.0075 and 0.0075%"],
                   "3 ÷ 400 = 0.0075. Multiply by 100: 0.75%. So <b>0.0075 and 0.75%</b>. "
                   "0.0075% forgets to multiply by 100, and the others put the decimal point in the wrong place."))
    assert F(3, 400) == D("0.0075")
    assert len(its) == 20, len(its)
    order = [0, 1, 2, 3, 4, 11, 12, 5, 6, 7, 14, 13, 8, 9, 10, 15, 16, 17, 18, 19]
    assert sorted(order) == list(range(20))
    its = [its[i] for i in order]
    return {"title": "Converting fractions, decimals and percents", "items": its}


# ============================================================ set 5: word problems
def set_problems(P):
    its = []
    tax = "BC charges 5% GST and 7% PST"
    n, he, his = P.next()
    its.append(mcq("%s buys headphones for $60. %s. What is the total with tax?" % (n, tax), "$67.20",       # 0
                   ["$72", "$7.20", "$60.12"],
                   "GST + PST = 5% + 7% = 12%. 12% of $60 = 0.12 × 60 = $7.20. $60 + $7.20 = <b>$67.20</b>. "
                   "$72 adds 12 dollars, $7.20 is only the tax, and $60.12 adds 12 cents.", value=D("67.20")))
    assert 60 + pc(12, 60) == D("67.2")
    its.append(mcq("A snowboard costs $250. How much PST (7%) is charged on it?", "$17.50",                     # 1
                   ["$175", "$1.75", "$30"],
                   "7% of $250 = 0.07 × 250 = <b>$17.50</b>. $175 uses 0.7 (70%), $1.75 uses 0.007, and $30 is "
                   "GST and PST together (12%).", value=D("17.50")))
    assert pc(7, 250) == D("17.5") and pc(12, 250) == 30
    its.append(mcq("A board game costs $45. %s. What is the total with tax?" % tax, "$50.40",                   # 2
                   ["$57", "$47.25", "$48.15"],
                   "12% of $45 = $5.40, so the total is $45 + $5.40 = <b>$50.40</b>. Or 1.12 × $45 = $50.40. "
                   "$57 adds 12 dollars, $47.25 adds only the GST, and $48.15 adds only the PST.", value=D("50.40")))
    assert F(45) * D("1.12") == D("50.40") and F(45) * D("1.05") == D("47.25") and F(45) * D("1.07") == D("48.15")
    its.append(mcq("A town in the Okanagan has 15%s000 people. The population grows by 4%%. What is the new "
                   "population?" % NBSP, num(15600), [num(15004), "600", num(21000)],                          # 3
                   "4% of 15" + NBSP + "000 = 600. 15" + NBSP + "000 + 600 = <b>15" + NBSP + "600</b>. 15" + NBSP
                   + "004 adds 4 people, 600 is only the growth, and 21" + NBSP + "000 grows by 40%.", value=15600))
    a, ah, _ = P.next()
    its.append(mcq("%s has $2400 in a savings account that pays 0.5%% interest a month. How much interest does %s "
                   "earn in one month?" % (a, ah), "$12", ["$1200", "$120", "$1.20"],                            # 4
                   "1% of $2400 = $24, so 0.5% is half of that: <b>$12</b>. $1200 treats 0.5% as one half, "
                   "$120 is 5%, and $1.20 is 0.05%.", value=12))
    assert pc(D("0.5"), 2400) == 12
    its.append(mcq("Last year, 85 students ran in their school’s Terry Fox Run. This year, 160% as many students "
                   "ran. How many students ran this year?", "136", ["245", "221", "51"],                         # 5
                   "“160% as many” means 160% <b>of</b> 85: 1.6 × 85 = <b>136</b>. 245 adds 160 to 85, "
                   "221 increases 85 <b>by</b> 160%, and 51 is only the extra 60%.", value=136))
    assert pc(160, 85) == 136 and 85 + pc(160, 85) == 221 and pc(60, 85) == 51
    its.append(mcq("A hockey stick costs $96. A Kamloops sports store takes " + fp(12, 1, 2) + " off. What is the "
                   "sale price?", "$84", ["$12", "$83.50", "$108"],                                              # 6
                   fp(12, 1, 2) + " = " + fr(1, 8) + ", so the discount is $96 ÷ 8 = $12. $96 − $12 = <b>$84</b>. "
                   "$12 is only the discount, $83.50 takes 12.5 dollars off, and $108 adds the discount.", value=84))
    its.append(mcq("Last year, 4000 salmon returned to a creek on Vancouver Island. This year, 250% as many "
                   "returned. How many salmon returned this year?", num(10000),
                   ["4250", num(14000), "6000"],                                                                 # 7
                   "250% of 4000 = 2.5 × 4000 = <b>10" + NBSP + "000</b>. 4250 adds 250, 14" + NBSP + "000 increases "
                   "4000 <b>by</b> 250%, and 6000 is only the extra 150%.", value=10000))
    assert pc(250, 4000) == 10000 and 4000 + pc(250, 4000) == 14000 and pc(150, 4000) == 6000
    its.append(mcq("A Burnaby factory makes 25%s000 light bulbs in a week. 0.4%% of them are faulty. How many bulbs "
                   "are faulty?" % NBSP, "100", [num(10000), "1000", "10"],                                      # 8
                   "1% of 25" + NBSP + "000 = 250. 0.4% = 0.4 × 250 = <b>100</b>. 10" + NBSP + "000 is 40%, "
                   "1000 is 4%, and 10 is 0.04%.", value=100))
    assert pc(D("0.4"), 25000) == 100
    b, bh, bp = P.next()
    its.append(mcq("%s’s phone plan includes 8 GB of data a month. This month %s used 10 GB. What percent of "
                   "%s plan did %s use?" % (b, bh, bp, bh), "125%", ["25%", "1.25%", "80%"],                     # 9
                   fr(10, 8) + " = 1.25 = <b>125%</b>. " + b + " used more than the plan, so the answer is more "
                   "than 100%. 25% is only the extra, 1.25% forgets to multiply by 100, and 80% divides the wrong way.",
                   value=125))
    its.append(mcq("In November, 200 mm of rain fell in Vancouver. In December, 170 mm fell. What is the percent "
                   "decrease?", "15%", ["30%", "85%", "1.5%"],                                                   # 10
                   "Decrease = 200 − 170 = 30 mm. Divide by the <b>starting</b> amount: " + fr(30, 200)
                   + " = 0.15 = <b>15%</b>. 30% uses the 30 mm as a percent, 85% is December as a percent of "
                   "November, and 1.5% moves the decimal point only one place.", value=15))
    its.append(mcq("The number of daily riders at a SkyTrain station grew from 20%s000 to 25%s000. What is the "
                   "percent increase?" % (NBSP, NBSP), "25%", ["20%", "125%", "2.5%"],                           # 11
                   "Increase = 5000. Divide by the <b>starting</b> number: " + fr(5000, "20" + NBSP + "000")
                   + " = 0.25 = <b>25%</b>. 20% divides by the new number (" + fr(5000, "25" + NBSP + "000")
                   + "), 125% is the new number as a percent of the old one, and 2.5% multiplies by 10 instead of 100.", value=25))
    its.append(mcq("In ski season, a Whistler hotel charges 140% of its usual price. The usual price is $200 a "
                   "night. What is the ski-season price?", "$280", ["$340", "$80", "$480"],                       # 12
                   "140% of $200 = 1.4 × 200 = <b>$280</b>. $340 adds 140 dollars, $80 is only the extra 40%, "
                   "and $480 increases $200 <b>by</b> 140%.", value=280))
    its.append(mcq("A condo in Vancouver is worth $650%s000. Its value rises by 0.5%%. By how much does the value "
                   "rise?" % NBSP, money(3250), [money(325000), money(32500), money(325)],                       # 13
                   "1% of $650" + NBSP + "000 = $6500, so 0.5% is half of that: <b>$3250</b>. $325" + NBSP
                   + "000 treats 0.5% as one half, $32" + NBSP + "500 is 5%, and $325 is 0.05%.", value=3250))
    assert pc(D("0.5"), 650000) == 3250
    its.append(mcq("At an eagle count near Squamish, volunteers counted 1200 bald eagles one year. The next year "
                   "the count was " + fp(33, 1, 3) + " higher. How many eagles were counted the next year?", "1600",
                   ["400", "1596", "800"],                                                                       # 14
                   fp(33, 1, 3) + " = " + fr(1, 3) + ". 1200 ÷ 3 = 400, so the count is 1200 + 400 = <b>1600</b>. "
                   "400 is only the increase, 1596 uses 33% instead of " + fp(33, 1, 3) + ", and 800 is a decrease.",
                   value=1600))
    assert 1200 + pc(F(100, 3), 1200) == 1600 and 1200 + pc(33, 1200) == 1596
    c, ch, _ = P.next()
    its.append(mcq("%s buys a $35 lacrosse stick. %s. How much more is the PST than the GST?" % (c, tax),       # 15
                   "70¢", ["$2", "$4.20", "$1.75"],
                   "PST: 7% of $35 = $2.45. GST: 5% of $35 = $1.75. $2.45 − $1.75 = <b>70¢</b> "
                   "(that is 2% of $35). $2 subtracts the rates as dollars, $4.20 is both taxes together, "
                   "and $1.75 is only the GST.", value=D("0.70")))
    assert pc(7, 35) - pc(5, 35) == D("0.7") and pc(12, 35) == D("4.2")
    its.append(mcq("A town of 20%s000 people grows by 5%% each year for 2 years. What is the population after "
                   "2 years?" % NBSP, num(22050), [num(22000), num(21000), num(20010)],                          # 16
                   "After 1 year: 5% of 20" + NBSP + "000 = 1000, so 21" + NBSP + "000. After 2 years: 5% of 21"
                   + NBSP + "000 = 1050, so 21" + NBSP + "000 + 1050 = <b>22" + NBSP + "050</b>. 22" + NBSP
                   + "000 adds 5% of 20" + NBSP + "000 twice, but the second 5% is of the bigger number. 21" + NBSP
                   + "000 is only one year, and 20" + NBSP + "010 adds just 5 people a year.", value=22050))
    assert F(20000) * D("1.05") * D("1.05") == 22050
    its.append(mcq("Snowboard boots cost $120. They are 25% off, and then 5% GST and 7% PST are added to the sale "
                   "price. What is the total?", "$100.80", ["$134.40", "$90", "$104.40"],                         # 17
                   "25% of $120 = $30, so the sale price is $90. 12% of $90 = $10.80. $90 + $10.80 = <b>$100.80</b>. "
                   "$134.40 forgets the discount, $90 forgets the tax, and $104.40 takes off 25% − 12% = 13%.",
                   value=D("100.80")))
    assert (120 - pc(25, 120)) * D("1.12") == D("100.8") and F(120) * D("1.12") == D("134.4") and F(120) * D("0.87") == D("104.4")
    its.append(mcq("A hiking club grew by " + fp(12, 1, 2) + " and now has 72 members. How many members did it have "
                   "before?", "64", ["63", "81", "60"],                                                          # 18
                   "After the growth the club has 112.5% of the old number. " + fp(12, 1, 2) + " = " + fr(1, 8)
                   + ", so the old number plus one eighth of it is 72: " + fr(9, 8) + " × ? = 72, and ? = 72 ÷ 9 × 8 = "
                   "<b>64</b>. Check: 64 ÷ 8 = 8, and 64 + 8 = 72. 63 takes " + fp(12, 1, 2) + " of 72 away, but the "
                   + fp(12, 1, 2) + " is of the <b>old</b> number. 81 adds it on, and 60 takes away 12.", value=64))
    assert F(72) / D("1.125") == 64 and 72 - pc(D("12.5"), 72) == 63 and 72 + pc(D("12.5"), 72) == 81
    its.append(mcq("Ski goggles cost $84 including 5% GST and 7% PST. What was the price before tax?", "$75",
                   ["$73.92", "$72", "$9"],                                                                      # 19
                   "The total is 112% of the price: 1.12 × ? = $84, so ? = $84 ÷ 1.12 = <b>$75</b>. "
                   "Check: 12% of $75 = $9, and $75 + $9 = $84. $73.92 takes 12% of $84 away, but the tax is 12% "
                   "of the price <b>before</b> tax. $72 takes away 12 dollars, and $9 is only the tax.", value=75))
    assert F(84) / D("1.12") == 75 and F(84) * D("0.88") == D("73.92")
    assert len(its) == 20, len(its)
    order = [0, 1, 4, 5, 2, 6, 9, 3, 7, 8, 10, 11, 12, 13, 15, 14, 16, 17, 18, 19]
    assert sorted(order) == list(range(20))
    its = [its[i] for i in order]
    return {"title": "Word problems: GST and PST, discounts and growth", "items": its}


# ============================================================ lesson
def body_html():
    f_line = percent_line_svg([0, 50, 100, 150], ["0", "30", "60", "90"], "percent line: 150% of 60 is 90")
    f_grid = hundred_grid_svg(1, "hundred grid: half of one square shaded")
    f_grid2 = hundred_grid_svg(25, "hundred grid: 12 and a half squares shaded")
    h = fp(12, 1, 2)
    return (
        "<h2>Percent means “out of 100”</h2>"
        "<p>To use any percent in a calculation, divide it by 100 to get a decimal. Then multiply. "
        "This works for 25%, for 150% and for 0.5%.</p>"
        + table(["Percent", "Decimal", "Fraction", "Size compared with the whole"], [
            ["150%", "1.5", mixed(1, 1, 2), "more than the whole"],
            ["100%", "1", "1", "the whole"],
            [h, "0.125", fr(1, 8), "less than the whole"],
            ["1%", "0.01", fr(1, 100), "one hundredth"],
            ["0.5% = " + fp(0, 1, 2), "0.005", fr(1, 200), "half of one hundredth"],
        ])
        + "<h2>Percents greater than 100%</h2>"
        "<p>100% is the whole amount. A percent greater than 100% gives <b>more</b> than the amount you started with.</p>"
        "<figure class='sn-fig'>" + f_line +
        "<figcaption>100% of 60 is 60. 50% is 30 more, so 150% of 60 is 60 + 30 = 90.</figcaption></figure>"
        + ex("Example", "What is 150% of 60?", "150% = 1.5. 1.5 × 60 = 90.", "90")
        + "<h2>Percents less than 1%</h2>"
        "<p>A percent less than 1% is a very small part. Find 1% first (divide by 100), then take part of it.</p>"
        "<figure class='sn-fig'>" + f_grid +
        "<figcaption>Each square is 1% of the grid. Half of one square is 0.5%.</figcaption></figure>"
        + ex("Example", "What is 0.5% of 4000?", "1% of 4000 = 40. 0.5% is half of 1%: 40 ÷ 2 = 20.", "20")
        + "<h2>Fractional percents</h2>"
        "<p>A percent can include a fraction, such as " + h + " or 33" + fr(1, 3) + "%. Change the fraction "
        "to a decimal (" + h + " = 12.5%), or use the matching fraction of the whole.</p>"
        "<figure class='sn-fig'>" + f_grid2 +
        "<figcaption>12 whole squares and half of one more: " + h + " of the grid, which is " + fr(1, 8)
        + ".</figcaption></figure>"
        + table(["Percent", "Fraction"], [
            [h, fr(1, 8)], ["33" + fr(1, 3) + "%", fr(1, 3)], ["37" + fr(1, 2) + "%", fr(3, 8)],
            ["66" + fr(2, 3) + "%", fr(2, 3)],
        ])
        + ex("Example", "What is " + h + " of 64?", h + " = " + fr(1, 8) + ". 64 ÷ 8 = 8.", "8")
        + "<h2>GST and PST in BC</h2>"
        "<p>In BC, most items are charged 5% GST and 7% PST. Together that is 12%, so multiply the price by 1.12.</p>"
        + ex("Sales tax", "Headphones cost $60. What is the total with 5% GST and 7% PST?",
             "12% of $60 = 0.12 × 60 = $7.20. $60 + $7.20 = $67.20. Or 1.12 × $60 = $67.20.", "$67.20")
        + "<h2>Common mistakes</h2>"
        + table(["Mistake", "What to do instead"], [
            ["150% of 60 = 60 + 150 = 210", "150% = 1.5, so 1.5 × 60 = 90"],
            ["0.5% = 0.5 (one half)", "0.5% = 0.5 ÷ 100 = 0.005"],
            ["0.5% of 4000 = 2000", "1% of 4000 is 40, so 0.5% is 20"],
            [h + " of 64 = 12% of 64 = 7.68", "Keep the half: " + h + " = 0.125, so the answer is 8"],
            ["160% as many as 85 = 85 + 136 = 221", "“As many” means 160% <b>of</b> 85, so 1.6 × 85 = 136"],
        ])
    )


FAQ = [
    {"q": "What do Grade 8 students learn about percents in BC?",
     "a": "The BC Grade 8 math curriculum includes percents less than 1 and greater than 100, written as decimal percents (0.5%) and fractional percents (12½%). Students use them to solve problems such as sales tax, discounts and population growth."},
    {"q": "How do you find a percent of a number when the percent is greater than 100%?",
     "a": "Write the percent as a decimal and multiply. For 150% of 60, 150% = 1.5 and 1.5 × 60 = 90, which is more than 60 because 150% is more than the whole."},
    {"q": "How do you find a percent that is less than 1%?",
     "a": "Find 1% first by dividing by 100, then take part of it. For 0.5% of 4000, 1% is 40 and 0.5% is half of that, so the answer is 20. Remember that 0.5% is 0.005, not 0.5."},
    {"q": "How do you calculate GST and PST in BC?",
     "a": "BC charges 5% GST and 7% PST on most items, which is 12% in total. Multiply the price by 1.12: a $45 item costs 1.12 × $45 = $50.40 with tax."},
]


def mark_large(u, pattern):
    """Tag pictures that must print larger (percent lines, hundred grids)."""
    rx = re.compile(r"<svg (?=[^>]*aria-label='" + pattern + ")")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u


def gen():
    rnd = random.Random(58802)
    P = People(rnd)
    sets = [set_over_100(), set_under_1(), set_fractional(), set_convert(), set_problems(P)]
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
        "country": "ca-bc", "subject": "math", "grade": "grade-8",
        "slug": "percents-less-than-1-and-greater-than-100", "sort": 2,
        "updated": UPDATED, "pdf_url": "",
        "title": "Grade 8 Percents Less Than 1% and Greater Than 100%",
        "seo_title": "Grade 8 Percents Less Than 1% and Greater Than 100% Worksheets: Free Math with Answer Key (BC Curriculum)",
        "short_title": "Percents under 1% and over 100%",
        "domain": "Number",
        "standard_code": "Grade 8: Number",
        "standard_url": "https://curriculum.gov.bc.ca/curriculum/mathematics/8/core",
        "standard_text": "Percents less than 1 and greater than 100 (decimal and fractional percents)",
        "meta_desc": "Free Grade 8 math worksheets for the BC curriculum on percents less than 1% and greater than 100%: decimal percents like 0.5%, fractional percents like 12½% and 33⅓%, converting fractions, decimals and percents, and GST and PST, discount and growth problems. 100 questions with an answer key.",
        "key_big": "Change the percent to a decimal, then multiply: 150% = 1.5, 0.5% = 0.005 and 12½% = 0.125.",
        "key_sub": "150% of 60 is 1.5 × 60 = 90, not 60 + 150. 0.5% is half of 1%, not one half, so 0.5% of 4000 is 20. In BC, 5% GST + 7% PST = 12%, so multiply a price by 1.12.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }
    return mark_large(u, "(percent line|hundred grid)")


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
