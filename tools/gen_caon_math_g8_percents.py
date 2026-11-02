# -*- coding: utf-8 -*-
"""
Canada (Ontario) Grade 8 Math: Percents
(Ontario Curriculum, Grades 1-8: Mathematics, 2020 — Grade 8, Number, B1.4)
  python3 tools/gen_caon_math_g8_percents.py
Percents of more than 100% (150% of 40) and less than 1% (0.5% of 2000); converting among fractions,
decimals and percents; percent increase and decrease; word problems with HST 13%, discounts and population growth.
Wrong answers come from real mistakes: 150% of 40 = 40 + 150, 0.5% = 0.5 (half), 0.5% = 0.05,
increase by 150% read as 150% of, percent change divided by the new value, giving only the change.
Every answer is checked with fractions.Fraction (never float).
Canadian English, dollars and cents, metric units, SI number spacing. HTML attributes use single quotes.
"""
import json, os, random, re
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "ca-on", "math", "grade-8")
UPDATED = "2026-11-02"
NBSP = " "
FILL = "#4fae74"
LINE = "#2b2b2b"
THIN = "#8a8a8a"
RED = "#d6453b"
BLUE = "#2f6fc0"
FONT = "Arial, Helvetica, sans-serif"
GIRLS = ["Olivia", "Emma", "Maya", "Zoe", "Amira", "Mei", "Chloe", "Priya", "Leah", "Hana", "Ava", "Sofia"]
BOYS = ["Liam", "Noah", "Aiden", "Lucas", "Owen", "Arjun", "Ethan", "Jayden", "Benjamin", "Mateo", "Nathan", "Kai"]


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
    return D(p) * F(n) / 100


def fr(a, b):
    return "<span class='fr'><span class='fn'>%s</span><span class='fd'>%s</span></span>" % (a, b)


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


def hundred_grid_svg(shaded_halves=1):
    """10 × 10 grid = 100 squares. shaded_halves: number of half squares shaded (left halves, first row)."""
    c, m = 20, 6
    W = m * 2 + 10 * c
    s = []
    for k in range(shaded_halves):
        i, half = divmod(k, 2)
        s.append("<rect x='%.1f' y='%d' width='%.1f' height='%d' fill='%s'/>" % (m + i * c + half * c / 2.0, m, c / 2.0, c, FILL))
    for i in range(11):
        w = 2.5 if i in (0, 10) else 1.2
        s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='%s'/>" % (m + i * c, m, m + i * c, m + 10 * c, LINE, w))
        s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='%s'/>" % (m, m + i * c, m + 10 * c, m + i * c, LINE, w))
    return svg_wrap(W, W, "".join(s), "hundred grid: %d half square shaded" % shaded_halves)


# ============================================================ set 1: percents over 100%
def set_over_100():
    its = []

    def pq(p, n, wrong, e, q=None, fg=""):
        r = pc(p, n)
        its.append(mcq(fg + (q or "What is %s%% of %s?" % (num(p), num(n))), num(r), [num(w) for w in wrong], e, value=r))

    pq(200, 35, [235, D("17.5"), 7],
       "200% = 2, so 200% of 35 = 2 × 35 = <b>70</b>. 235 adds 200 to 35, and 17.5 halves 35 instead of doubling it.")
    pq(150, 40, [190, 20, 600],
       "150% = 1.5. 1.5 × 40 = <b>60</b>. Or: 100% of 40 is 40 and 50% is 20, so 40 + 20 = 60. "
       "190 adds 150 to 40, and 20 is only the extra 50%.")
    pq(300, 12, [312, 4, 48],
       "300% = 3. 3 × 12 = <b>36</b>. 312 adds 300 to 12, 4 divides by 3, and 48 is 400%.")
    pq(125, 80, [205, 20, 1000],
       "125% = 1.25. 100% of 80 is 80 and 25% is 20, so 80 + 20 = <b>100</b>. "
       "205 adds 125 to 80, 20 is only the extra 25%, and 1000 uses 12.5 instead of 1.25.")
    pq(110, 60, [170, 6, 660],
       "110% = 100% + 10%. 60 + 6 = <b>66</b>. 170 adds 110 to 60, 6 is only 10%, and 660 uses 11 instead of 1.1.")
    pq(250, 18, [268, 36, 9],
       "250% = 2.5. 2 × 18 = 36 and 0.5 × 18 = 9, so 36 + 9 = <b>45</b>. 268 adds 250 to 18, 36 is only 200%, "
       "and 9 is only 50%.")
    pq(120, 45, [165, 9, 540],
       "120% = 1.2. 100% of 45 is 45 and 20% is 9, so 45 + 9 = <b>54</b>. 165 adds 120 to 45, "
       "and 540 uses 12 instead of 1.2.")
    pq(175, 24, [199, 18, 420],
       "175% = 1.75. 100% of 24 is 24 and 75% is 18, so 24 + 18 = <b>42</b>. 199 adds 175 to 24, "
       "18 is only 75%, and 420 uses 17.5 instead of 1.75.")
    pq(350, 8, [358, 24, D("2.8")],
       "350% = 3.5. 3.5 × 8 = 24 + 4 = <b>28</b>. 358 adds 350 to 8, 24 is only 300%, "
       "and 2.8 uses 0.35 instead of 3.5.")
    pq(105, 300, [405, 15, 3150],
       "105% = 100% + 5%. 5% of 300 is 15, so 300 + 15 = <b>315</b>. 405 adds 105 to 300, "
       "15 is only 5%, and 3150 uses 10.5 instead of 1.05.")
    pq(400, D("2.5"), [D("402.5"), 1, D("7.5")],
       "400% = 4. 4 × 2.5 = <b>10</b>. 402.5 adds 400 to 2.5, 1 uses 0.4 instead of 4, and 7.5 is 300%.")
    pq(150, 64, [214, 32, 128],
       "On the line, 100% matches 64, so 50% matches 32. 150% = 100% + 50%: 64 + 32 = <b>96</b>. "
       "214 adds 150 to 64, 32 is only 50%, and 128 is 200%.",
       q="The double number line shows that 100% is 64. What amount matches 150%?",
       fg=fig(percent_line_svg([0, 50, 100, 150], ["0", "32", "64", "?"], "percent line: 100% is 64, 150% is unknown")))
    its.append(mcq("Which calculation finds 125% of 64?", "1.25 × 64", ["12.5 × 64", "0.125 × 64", "64 + 125"],
                   "Percent means out of 100, so 125% = 125 ÷ 100 = 1.25. The calculation is <b>1.25 × 64</b> (= 80). "
                   "12.5 and 0.125 move the decimal point the wrong number of places, and 64 + 125 adds the percent."))
    its.append(mcq("Without calculating, which amount is greater than 72?", "125% of 72",
                   ["75% of 72", "99% of 72", "100% of 72"],
                   "100% of 72 is 72 itself. A percent <b>over</b> 100% gives more than the number, so <b>125% of 72</b> is "
                   "greater than 72. 75% and 99% give less than 72, and 100% gives exactly 72."))
    its.append(mcq("18 is what percent of 12?", "150%", ["50%", "1.5%", "6%"],
                   "%s = 1.5 = <b>150%%</b>. 18 is more than 12, so the answer must be more than 100%%. "
                   "50%% is only the extra 6, 1.5%% forgets to multiply by 100, and 6%% uses the difference." % fr(18, 12)))
    its.append(mcq("45 is what percent of 20?", "225%", ["125%", "2.25%", "25%"],
                   "%s = 2.25 = <b>225%%</b>. Check: 225%% of 20 = 2.25 × 20 = 45. "
                   "125%% is only the extra 25, 2.25%% forgets to multiply by 100, and 25%% uses the difference 45 − 20."
                   % fr(45, 20)))
    its.append(mcq("Which is greater: 150% of 30 or 30% of 150?", "They are equal",
                   ["150% of 30", "30% of 150", "You can’t tell"],
                   "150% of 30 = 1.5 × 30 = 45. 30% of 150 = 0.3 × 150 = 45. <b>They are equal</b>: "
                   "a% of b is always the same as b% of a."))
    its.append(mcq("150% of a number is 60. What is the number?", "40", ["90", "30", "400"],
                   "1.5 × ? = 60, so ? = 60 ÷ 1.5 = <b>40</b>. Check: 150% of 40 = 60. "
                   "90 is 150% of 60 (the wrong way round), 30 halves 60, and 400 divides by 0.15.", value=40))
    its.append(mcq("200% of a number is 52. What is the number?", "26", ["104", "13", "260"],
                   "200% = 2, so 2 × ? = 52 and ? = 52 ÷ 2 = <b>26</b>. "
                   "104 is 200% of 52 (the wrong way round), 13 divides by 4, and 260 divides by 0.2.", value=26))
    its.append(mcq("Which statement is true?", "120% of 50 = 60",
                   ["120% of 50 = 170", "120% of 50 = 6", "120% of 50 = 600"],
                   "120% = 1.2, and 1.2 × 50 = 60, so <b>120% of 50 = 60</b>. 170 adds 120 + 50, "
                   "6 is only 12%, and 600 uses 12 instead of 1.2."))
    assert pc(120, 50) == 60 and pc(150, 30) == pc(30, 150) == 45 and pc(125, 64) == 80
    assert len(its) == 20, len(its)
    order = [0, 1, 2, 3, 4, 12, 13, 5, 6, 11, 7, 8, 9, 10, 19, 14, 15, 16, 17, 18]
    its = [its[i] for i in order]
    return {"title": "Percents over 100%: 150%, 200% and 350% of a number", "items": its}


# ============================================================ set 2: percents under 1%
def set_under_1():
    its = []

    def pq(p, n, wrong, e, q=None):
        r = pc(p, n)
        its.append(mcq(q or "What is %s%% of %s?" % (num(D(p)), num(n)), num(r), [num(w) for w in wrong], e, value=r))

    pq(1, 2000, [200, 2, D("0.2")],
       "1% means divide by 100: 2000 ÷ 100 = <b>20</b>. 200 is 10%, and 2 is 0.1%.")
    pq("0.5", 2000, [1000, 100, 1],
       "1% of 2000 is 20. 0.5% is <b>half of 1%</b>: 20 ÷ 2 = <b>10</b>. "
       "1000 treats 0.5% as one half (50%), 100 is 5%, and 1 is 0.05%.")
    pq("0.1", 3000, [300, 30, D("0.3")],
       "1% of 3000 is 30. 0.1% is one tenth of 1%: 30 ÷ 10 = <b>3</b>. 300 is 10%, and 30 is 1%.")
    pq("0.5", 800, [400, 40, D("0.4")],
       "1% of 800 is 8, so 0.5% is half of 8 = <b>4</b>. 400 treats 0.5% as one half, and 40 is 5%.")
    pq("0.25", 400, [100, 10, D("0.1")],
       "1% of 400 is 4. 0.25% is a quarter of 1%: 4 ÷ 4 = <b>1</b>. 100 is 25%, and 10 is 2.5%.")
    pq("0.2", 1500, [300, 30, D("0.3")],
       "1% of 1500 is 15. 0.2% = 2 × 0.1%, and 0.1% is 1.5, so 0.2% is <b>3</b>. 300 is 20%, and 30 is 2%.")
    pq("0.75", 1200, [900, 90, D("0.9")],
       "1% of 1200 is 12. 0.75% is three quarters of 1%: 12 ÷ 4 × 3 = <b>9</b>. 900 is 75%, and 90 is 7.5%.")
    pq("0.1", 45000, [4500, 450, D("4.5")],
       "0.1%% = 0.001, so divide by 1000: 45%s000 ÷ 1000 = <b>45</b>. 4500 is 10%%, and 450 is 1%%." % NBSP)
    pq("0.4", 250, [100, 10, D("0.1")],
       "1% of 250 is 2.5. 0.4% = 0.4 × 2.5 = <b>1</b>. 100 is 40%, and 10 is 4%.")
    pq("0.6", 5000, [3000, 300, 3],
       "1% of 5000 is 50. 0.6% = 0.6 × 50 = <b>30</b>. 3000 is 60%, and 300 is 6%.")
    pq("0.05", 20000, [1000, 100, 1],
       "1%% of 20%s000 is 200. 0.05%% is one twentieth of 1%%: 200 ÷ 20 = <b>10</b>. "
       "1000 is 5%%, and 100 is 0.5%%." % NBSP)
    pq("0.8", 750, [600, 60, D("0.6")],
       "1% of 750 is 7.5. 0.8% = 0.8 × 7.5 = <b>6</b>. 600 is 80%, and 60 is 8%.")
    pq("0.5", 36, [18, D("1.8"), D("0.018")],
       "1% of 36 is 0.36. 0.5% is half of that: <b>0.18</b>. 18 treats 0.5% as one half, 1.8 is 5%, "
       "and 0.018 is 0.05%.")
    its.append(mcq(fig(hundred_grid_svg(1)) + "The grid has 100 equal squares. What percent of the grid is shaded?",
                   "0.5%", ["5%", "50%", "0.05%"],
                   "One whole square is 1% of the grid. Only half of one square is shaded, so the shaded part is "
                   "<b>0.5%</b>: less than 1%. 50% would be half of the <b>whole grid</b>."))
    its.append(mcq("3 is what percent of 1000?", "0.3%", ["3%", "30%", "0.03%"],
                   "%s = 0.003. Multiply by 100: <b>0.3%%</b>. 3%% would be 30 out of 1000." % fr(3, 1000)))
    its.append(mcq("1 is what percent of 400?", "0.25%", ["25%", "2.5%", "4%"],
                   "%s = 0.0025 = <b>0.25%%</b>. Check: 1%% of 400 is 4, so 1 is a quarter of 1%%. "
                   "25%% of 400 would be 100." % fr(1, 400)))
    its.append(mcq("0.5% of a number is 6. What is the number?", "1200", ["12", "3", "120"],
                   "0.5% = 0.005, so ? = 6 ÷ 0.005 = <b>1200</b>. Or: 0.5% is 6, so 1% is 12 and 100% is 1200. "
                   "12 divides by 0.5, and 3 takes half of 6.", value=1200))
    its.append(mcq("Which amount is <b>less</b> than 1% of 500?", "0.8% of 500",
                   ["1.2% of 500", "10% of 50", "5% of 100"],
                   "1% of 500 = 5. 0.8% of 500 = 4, which is less, so <b>0.8% of 500</b>. "
                   "1.2% of 500 = 6, and 10% of 50 and 5% of 100 are both exactly 5."))
    its.append(mcq("Which list is in order from least to greatest?", "0.09%, 0.5%, 1%",
                   ["0.5%, 1%, 0.09%", "1%, 0.5%, 0.09%", "0.5%, 0.09%, 1%"],
                   "Compare the decimals: 0.09 &lt; 0.50 &lt; 1. So <b>0.09%, 0.5%, 1%</b>. "
                   "0.09% has the digit 9, but it is less than one tenth of 1%."))
    its.append(mcq("Which is equal to 0.5% of 400?", "1% of 200", ["5% of 400", "50% of 400", "0.5% of 40"],
                   "0.5% of 400 = 2. 1% of 200 = 2 too, so <b>1% of 200</b>. "
                   "5% of 400 = 20, 50% of 400 = 200, and 0.5% of 40 = 0.2."))
    assert pc("0.5", 400) == pc(1, 200) == 2 and pc("0.8", 500) == 4 and F(1, 400) * 100 == D("0.25")
    assert len(its) == 20, len(its)
    order = [0, 1, 2, 3, 13, 4, 5, 6, 8, 14, 7, 9, 15, 10, 11, 17, 18, 12, 19, 16]
    its = [its[i] for i in order]
    return {"title": "Percents under 1%: 0.5%, 0.25% and 0.1% of a number", "items": its}


# ============================================================ set 3: converting among forms
def set_convert():
    its = []

    def conv(q, right, wrong, e, value, same_ok=False):
        its.append(mcq(q, right, wrong, e, value=value, same_ok=same_ok))

    conv("Write 0.5% as a decimal.", "0.005", ["0.5", "0.05", "5"],
         "Percent means out of 100, so divide by 100: move the decimal point 2 places left. "
         "0.5% = <b>0.005</b>. 0.5 forgets to divide, and 0.05 moves only one place.", D("0.005"))
    conv("Write 150% as a decimal.", "1.5", ["0.15", "15", "150"],
         "Divide by 100: 150% = 150 ÷ 100 = <b>1.5</b>. 150% is more than 100%, so the decimal is more than 1.",
         D("1.5"))
    conv("Write 0.07 as a percent.", "7%", ["0.07%", "70%", "0.7%"],
         "Multiply by 100: move the decimal point 2 places right. 0.07 = <b>7%</b>. 70% would be 0.7.", 7)
    conv("Write 2.4 as a percent.", "240%", ["24%", "2.4%", "0.24%"],
         "Multiply by 100: 2.4 × 100 = <b>240%</b>. 2.4 is more than 1, so the percent is more than 100%. "
         "24% moves the decimal point only one place.", 240)
    conv("Write 0.003 as a percent.", "0.3%", ["3%", "30%", "0.03%"],
         "Multiply by 100: 0.003 × 100 = <b>0.3%</b>. The number is less than 0.01, so the percent is less than 1%.",
         D("0.3"))
    conv("Write %s as a percent." % fr(3, 8), "37.5%", ["3.8%", "0.375%", "62.5%"],
         "3 ÷ 8 = 0.375. Multiply by 100: <b>37.5%%</b>. 3.8%% reads %s as 3.8, 0.375%% forgets to multiply by 100, "
         "and 62.5%% is %s." % (fr(3, 8), fr(5, 8)), D("37.5"))
    conv("Write %s as a percent." % fr(5, 4), "125%", ["80%", "1.25%", "12.5%"],
         "5 ÷ 4 = 1.25 = <b>125%%</b>. The fraction is more than 1, so the percent is more than 100%%. "
         "80%% is %s (the fraction flipped)." % fr(4, 5), 125)
    conv("Write %s as a percent." % fr(1, 200), "0.5%", ["5%", "200%", "0.005%"],
         "1 ÷ 200 = 0.005. Multiply by 100: <b>0.5%%</b>. Check: 1%% is %s, and %s is half of that. "
         "0.005%% forgets to multiply by 100." % (fr(1, 100), fr(1, 200)), D("0.5"))
    conv("Write %s as a percent." % fr(1, 8), "12.5%", ["8%", "0.125%", "18%"],
         "1 ÷ 8 = 0.125 = <b>12.5%%</b>. 8%% uses the denominator, and 18%% just joins the digits of %s." % fr(1, 8),
         D("12.5"))
    conv("Write 0.2% as a fraction in simplest form.", fr(1, 500), [fr(1, 5), fr(1, 50), fr(1, 5000)],
         "0.2%% = %s = %s = <b>%s</b>. %s is 20%%, and %s is 2%%."
         % (fr("0.2", 100), fr(2, 1000), fr(1, 500), fr(1, 5), fr(1, 50)), F(1, 500))
    conv("Write 250% as a mixed number.", "2" + fr(1, 2), ["25", fr(2, 5), "2" + fr(1, 5)],
         "250%% = %s = 2.5 = <b>2%s</b>. %s reads 2.5 as “2 over 5”, 2%s reads 0.5 as one fifth, and 25 divides by 10 "
         "instead of 100." % (fr(250, 100), fr(1, 2), fr(2, 5), fr(1, 5)), None)
    conv("Write 2" + fr(3, 4) + " as a percent.", "275%", ["2.75%", "27.5%", "75%"],
         "2%s = 2.75. Multiply by 100: <b>275%%</b>. 75%% forgets the 2 wholes, and 2.75%% forgets to multiply by 100."
         % fr(3, 4), 275)
    conv("Write 0.65% as a decimal.", "0.0065", ["0.65", "0.065", "6.5"],
         "Divide by 100: move the decimal point 2 places left. 0.65% = <b>0.0065</b>. "
         "0.65 forgets to divide, and 0.065 moves only one place.", D("0.0065"))
    conv("Write 1.05 as a percent.", "105%", ["10.5%", "1.05%", "15%"],
         "1.05 × 100 = <b>105%</b>. 10.5% moves the decimal point only one place, and 15% drops the zero.", 105)
    its.append(mcq("Which is equal to 0.4%?", fr(1, 250), ["0.04", "0.4", "4"],
                   "0.4%% = 0.4 ÷ 100 = 0.004 = %s = <b>%s</b>. 0.04 is 4%%, 0.4 is 40%%, and 4 is 400%%." % (fr(4, 1000), fr(1, 250))))
    its.append(mcq("Which is equal to %s?" % fr(1, 1000), "0.1%", ["1%", "10%", "0.01%"],
                   "%s = 0.001. Multiply by 100: <b>0.1%%</b>. 1%% is %s." % (fr(1, 1000), fr(1, 100)), value=D("0.1")))
    its.append(mcq("Which is greater: 0.8% or 0.08?", "0.08", ["0.8%", "They are equal", "You can’t tell"],
                   "Write both as decimals. 0.8% = 0.008. 0.08 &gt; 0.008, so <b>0.08</b> is greater "
                   "(0.08 = 8%)."))
    its.append(mcq("Which number is greatest?", "1.3", ["125%", fr(6, 5), "0.9%"],
                   "Write all as decimals: 1.3, 125%% = 1.25, %s = 1.2, 0.9%% = 0.009. The greatest is <b>1.3</b>. "
                   "125 looks big, but 125%% is only 1.25." % fr(6, 5)))
    its.append(mcq("Which is <b>not</b> equal to 1.5?", "15%", ["150%", fr(3, 2), "1" + fr(1, 2)],
                   "150%% = 1.5, %s = 1.5 and 1%s = 1.5. <b>15%%</b> = 0.15, so it is not equal to 1.5."
                   % (fr(3, 2), fr(1, 2)), same_ok=True))
    its.append(mcq("Which list is in order from least to greatest?",
                   "98%, " + fr(9, 8) + ", 1.2", ["1.2, 98%, " + fr(9, 8), fr(9, 8) + ", 1.2, 98%", "98%, 1.2, " + fr(9, 8)],
                   "Write all as decimals: 98%% = 0.98, %s = 1.125, 1.2. So the order is <b>98%%, %s, 1.2</b>."
                   % (fr(9, 8), fr(9, 8))))
    assert D("0.004") == F(1, 250) and F(9, 8) == D("1.125") and F(11, 4) * 100 == 275
    assert len(its) == 20, len(its)
    order = [0, 1, 2, 3, 4, 13, 12, 14, 8, 5, 6, 7, 15, 9, 10, 11, 16, 18, 17, 19]
    its = [its[i] for i in order]
    return {"title": "Converting fractions, decimals and percents", "items": its}


# ============================================================ set 4: percent increase and decrease
def set_change():
    its = []

    def new_val(n, p, up, wrong, e, q):
        r = F(n) + pc(p, n) if up else F(n) - pc(p, n)
        its.append(mcq(q, num(r), [num(w) for w in wrong], e, value=r))

    def change(a, b, wrong, e, q=None):
        r = abs(F(b) - F(a)) / F(a) * 100
        word = "increase" if b > a else "decrease"
        its.append(mcq(q or "A value changes from %s to %s. What is the percent %s?" % (num(a), num(b), word),
                       pct(r), [pct(w) for w in wrong], e, value=r))

    new_val(40, 25, True, [65, 10, 30],
            "25% of 40 = 10. Increase: 40 + 10 = <b>50</b>. Or 125% of 40 = 1.25 × 40 = 50. "
            "65 adds 25, 10 is only the increase, and 30 is a decrease.", "Increase 40 by 25%.")
    new_val(80, 15, False, [65, 12, 92],
            "15% of 80 = 8 + 4 = 12. Decrease: 80 − 12 = <b>68</b>. Or 85% of 80 = 68. "
            "65 subtracts 15, 12 is only the decrease, and 92 is an increase.", "Decrease 80 by 15%.")
    new_val(45, 40, False, [5, 18, 63],
            "40% of 45 = 18. 45 − 18 = <b>27</b>. Or 60% of 45 = 27. 5 subtracts 40, and 18 is only the decrease.",
            "Decrease 45 by 40%.")
    new_val(64, D("12.5"), True, [D("76.5"), 8, 56],
            "12.5%% = %s, so 12.5%% of 64 = 8. 64 + 8 = <b>72</b>. 76.5 adds 12.5, and 56 is a decrease." % fr(1, 8),
            "Increase 64 by 12.5%.")
    change(20, 25, [5, 20, 125],
           "Change = 25 − 20 = 5. Divide by the <b>starting</b> value: %s = 0.25 = <b>25%%</b>. "
           "5%% uses the change as a percent, 20%% divides by the new value (%s), and 125%% is 25 as a percent of 20."
           % (fr(5, 20), fr(5, 25)))
    change(50, 40, [10, 25, 80],
           "Change = 50 − 40 = 10. Divide by the starting value: %s = <b>20%%</b>. "
           "25%% divides by the new value (%s), and 80%% is 40 as a percent of 50." % (fr(10, 50), fr(10, 40)))
    change(16, 4, [12, 300, 25],
           "Change = 16 − 4 = 12. %s = 0.75 = <b>75%%</b>. 300%% divides by the new value (%s), "
           "and 25%% is 4 as a percent of 16." % (fr(12, 16), fr(12, 4)))
    its.append(mcq("Multiplying a number by 1.2 is the same as which change?", "a 20% increase",
                   ["a 120% increase", "a 2% increase", "a 12% increase"],
                   "1.2 = 120% = 100% + 20%. You keep the whole number and add 20%: <b>a 20% increase</b>. "
                   "A 120% increase would multiply by 2.2."))
    its.append(mcq("Multiplying a number by 0.85 is the same as which change?", "a 15% decrease",
                   ["an 85% decrease", "a 0.85% decrease", "a 15% increase"],
                   "0.85 = 85% = 100% − 15%. You keep 85% and lose 15%: <b>a 15% decrease</b>. "
                   "An 85% decrease would leave only 15%."))
    new_val(60, 150, True, [90, 210, 69],
            "Increase by 150%: add 150% of 60 = 90 to 60. 60 + 90 = <b>150</b>. Or 250% of 60 = 2.5 × 60 = 150. "
            "90 is only 150% <b>of</b> 60, 210 adds 150, and 69 adds only 15%.", "Increase 60 by 150%.")
    change(30, 75, [250, 45, 60],
           "Change = 75 − 30 = 45. %s = 1.5 = <b>150%%</b>. 250%% is 75 as a percent of 30 (the new value is 250%% "
           "<b>of</b> the old one), 45%% uses the change, and 60%% divides by the new value (%s)."
           % (fr(45, 30), fr(45, 75)))
    new_val(200, D("0.5"), False, [100, 190, D("199.5")],
            "0.5% of 200 = 1. 200 − 1 = <b>199</b>. 100 treats 0.5% as one half, 190 takes off 5%, "
            "and 199.5 subtracts 0.5.", "Decrease 200 by 0.5%.")
    new_val(500, D("0.4"), True, [700, 520, D("500.4")],
            "1% of 500 is 5, so 0.4% = 2. 500 + 2 = <b>502</b>. 700 adds 40%, 520 adds 4%, and 500.4 adds 0.4.",
            "Increase 500 by 0.4%.")
    change(2000, 2010, [10, 5, D("0.05")],
           "Change = 10. %s = 0.005 = <b>0.5%%</b>. 10%% uses the change as a percent, and 5%% and 0.05%% "
           "move the decimal point the wrong number of places." % fr(10, 2000))
    change(250, 300, [50, 120, D("0.2")],
           "Change = 50. %s = 0.2 = <b>20%%</b>. 50%% uses the change, 120%% is 300 as a percent of 250, "
           "and 0.2%% forgets to multiply by 100." % fr(50, 250))
    its.append(mcq("A price doubles. What is the percent increase?", "100%", ["200%", "2%", "50%"],
                   "The new price is 200% of the old price. The increase is 200% − 100% = <b>100%</b>. "
                   "200% is the new price as a percent of the old one."))
    change(8, 24, [300, 16, 3],
           "Change = 24 − 8 = 16. %s = 2 = <b>200%%</b>. 24 is three times 8 (300%% <b>of</b> 8), "
           "but the increase is 2 times 8." % fr(16, 8))
    its.append(mcq("Increase 100 by 10%. Then decrease the result by 10%. What is the final value?", "99",
                   ["100", "90", "101"],
                   "100 + 10 = 110. 10% of 110 = 11, so 110 − 11 = <b>99</b>. The second 10% is of 110, not 100, "
                   "so the changes do not cancel out.", value=99))
    assert (100 + pc(10, 100)) * F(9, 10) == 99
    its.append(mcq("After a 20% increase, a number is 60. What was the number before the increase?", "50",
                   ["48", "72", "40"],
                   "After the increase the number is 120% of the start: 1.2 × ? = 60, so ? = 60 ÷ 1.2 = <b>50</b>. "
                   "Check: 20% of 50 = 10, and 50 + 10 = 60. 48 takes 20% of 60 away, but the 20% is of the "
                   "<b>starting</b> number.", value=50))
    its.append(mcq("After a 25% decrease, a number is 60. What was the number before the decrease?", "80",
                   ["75", "85", "45"],
                   "After the decrease the number is 75% of the start: 0.75 × ? = 60, so ? = 60 ÷ 0.75 = <b>80</b>. "
                   "Check: 25% of 80 = 20, and 80 − 20 = 60. 75 adds 25% of 60, and 85 adds 25.", value=80))
    assert F(60) / D("1.2") == 50 and F(60) / D("0.75") == 80
    assert len(its) == 20, len(its)
    order = [0, 1, 2, 4, 5, 3, 6, 7, 8, 15, 9, 10, 16, 11, 12, 13, 14, 17, 18, 19]
    its = [its[i] for i in order]
    return {"title": "Percent increase and decrease", "items": its}


# ============================================================ set 5: word problems
def set_problems(P):
    its = []
    n, he, his = P.next()
    its.append(mcq("%s buys a $40 hoodie. Ontario HST is 13%%. What is the total with tax?" % n, "$45.20",
                   ["$53", "$5.20", "$40.13"],
                   "13% of $40 = 0.13 × 40 = $5.20. $40 + $5.20 = <b>$45.20</b>. $53 adds 13 dollars, "
                   "$5.20 is only the tax, and $40.13 adds 13 cents.", value=D("45.20")))
    assert 40 + pc(13, 40) == D("45.2")
    its.append(mcq("Skates that cost $120 are 30% off. What is the sale price?", "$84", ["$90", "$36", "$156"],
                   "30% of $120 = $36. $120 − $36 = <b>$84</b>. $90 takes away 30 dollars, $36 is the discount, "
                   "and $156 adds the discount.", value=84))
    its.append(mcq("A savings account pays 0.5% interest a month. Leah has $1600 in it. How much interest does she earn "
                   "in one month?", "$8", ["$800", "$80", "80¢"],
                   "1% of $1600 = $16, so 0.5% is half: <b>$8</b>. $800 treats 0.5% as one half, $80 is 5%, "
                   "and 80¢ is 0.05%.", value=8))
    assert pc("0.5", 1600) == 8
    its.append(mcq("A hockey league has 150% as many players this year as last year. Last year it had 240 players. "
                   "How many players does it have this year?", "360", ["390", "600", "120"],
                   "“150% as many” means 150% <b>of</b> 240: 1.5 × 240 = <b>360</b>. 390 adds 150, "
                   "600 is an increase <b>by</b> 150%, and 120 is only 50%.", value=360))
    assert pc(150, 240) == 360
    its.append(mcq("A town has 12%s000 people. The population grows by 5%%. What is the new population?" % NBSP,
                   num(12600), [num(12005), "600", num(13200)],
                   "5%% of 12%s000 = 600. 12%s000 + 600 = <b>12%s600</b>. 12%s005 adds 5 people, 600 is only the growth, "
                   "and 13%s200 grows by 10%%." % ((NBSP,) * 5), value=12600))
    its.append(mcq("A school has 750 students. On one day, 0.4% of them are absent. How many students are absent?",
                   "3", ["300", "30", "0.3"],
                   "1% of 750 = 7.5. 0.4% = 0.4 × 7.5 = <b>3</b> students. 300 is 40%, and 30 is 4%.", value=3))
    assert pc("0.4", 750) == 3
    its.append(mcq("A town grew from 8000 to 10%s000 people. What is the percent increase?" % NBSP, "25%",
                   ["20%", "2000%", "125%"],
                   "Increase = 2000. Divide by the starting population: %s = <b>25%%</b>. "
                   "20%% divides by the new population, 2000%% uses the increase, and 125%% is the new population "
                   "as a percent of the old one." % fr(2000, 8000), value=25))
    its.append(mcq("The CN Tower is 553 m tall. A model of it is 0.1% of the real height. How tall is the model?",
                   "55.3 cm", ["5.53 m", "55.3 m", "5.53 cm"],
                   "0.1% = 0.001. 0.001 × 553 m = 0.553 m = <b>55.3 cm</b>. 5.53 m is 1%, 55.3 m is 10%, "
                   "and 5.53 cm is 0.01%."))
    assert pc("0.1", 553) * 100 == D("55.3")
    its.append(mcq("Last winter, 120 cm of snow fell in a town. This winter, 90 cm fell. What is the percent decrease?",
                   "25%", ["30%", "75%", "0.25%"],
                   "Decrease = 120 − 90 = 30 cm. %s = 0.25 = <b>25%%</b>. 30%% uses the 30 cm as a percent, "
                   "75%% is this winter as a percent of last winter, and 0.25%% forgets to multiply by 100." % fr(30, 120), value=25))
    its.append(mcq("Winter boots that cost $80 are on sale for $68. What percent is the discount?", "15%",
                   ["12%", "85%", "1.5%"],
                   "Discount = $80 − $68 = $12. %s = 0.15 = <b>15%%</b>. 12%% uses the $12 as a percent, "
                   "85%% is the part you pay, and 1.5%% moves the decimal point only one place." % fr(12, 80), value=15))
    its.append(mcq("In a survey, 0.6 of the students chose hockey and %s chose soccer. The rest chose basketball. "
                   "What percent chose basketball?" % fr(1, 4), "15%", ["85%", "40%", "75%"],
                   "0.6 = 60%% and %s = 25%%. 100%% − 60%% − 25%% = <b>15%%</b>. 85%% is hockey and soccer together, "
                   "and 40%% forgets to take away soccer. 75%% takes away only soccer." % fr(1, 4), value=15))
    its.append(mcq("A town of 40%s000 people holds a Terry Fox Run. 0.25%% of the people volunteer. How many volunteers "
                   "is that?" % NBSP, "100", [num(10000), num(1000), "10"],
                   "1%% of 40%s000 = 400. 0.25%% is a quarter of 1%%: 400 ÷ 4 = <b>100</b>. 10%s000 is 25%%, and 1000 "
                   "is 2.5%%." % (NBSP, NBSP), value=100))
    assert pc("0.25", 40000) == 100
    its.append(mcq("A phone plan includes 5 GB of data. Ethan uses 6.5 GB. What percent of the plan did he use?", "130%",
                   ["30%", "1.3%", "65%"],
                   "%s = 1.3 = <b>130%%</b>. He used more than the plan, so the answer is more than 100%%. "
                   "30%% is only the extra, and 65%% divides by 10." % fr("6.5", 5), value=130))
    its.append(mcq("Kai buys a used bike for $150 and sells it for $180. What is the percent increase in price?", "20%",
                   ["30%", "120%", "0.2%"],
                   "Increase = $30. %s = 0.2 = <b>20%%</b>. 30%% uses the $30 as a percent, and 120%% is $180 as a "
                   "percent of $150." % fr(30, 150), value=20))
    its.append(mcq("A town’s population fell from 25%s000 to 24%s500. What is the percent decrease?" % (NBSP, NBSP), "2%",
                   ["5%", "20%", "0.2%"],
                   "Decrease = 500. %s = 0.02 = <b>2%%</b>. 5%%, 20%% and 0.2%% put the decimal point in the "
                   "wrong place." % fr(500, "25" + NBSP + "000"), value=2))
    its.append(mcq("A town of 10%s000 people grows by 10%% each year for 2 years. What is the population after 2 years?"
                   % NBSP, num(12100), [num(12000), num(11000), num(10020)],
                   "After 1 year: 10%% of 10%s000 = 1000, so 11%s000. After 2 years: 10%% of 11%s000 = 1100, so 11%s000 + 1100 = "
                   "<b>12%s100</b>. 12%s000 adds 10%% of 10%s000 twice, but the second 10%% is of the bigger number. 11%s000 is only one year, and 10%s020 adds just 10 people a year."
                   % ((NBSP,) * 9), value=12100))
    assert F(10000) * D("1.1") * D("1.1") == 12100
    its.append(mcq("A jacket costs $60. It is 25% off, and then 13% HST is added to the sale price. What is the total?",
                   "$50.85", ["$67.80", "$45", "$52.80"],
                   "25% of $60 = $15, so the sale price is $45. 13% of $45 = $5.85. $45 + $5.85 = <b>$50.85</b>. "
                   "$67.80 forgets the discount, $45 forgets the tax, and $52.80 takes off 25% − 13% = 12%.",
                   value=D("50.85")))
    assert (60 - pc(25, 60)) * D("1.13") == D("50.85")
    a, ah, _ = P.next()
    its.append(mcq("%s pays $34 for a sweater that is 15%% off. What was the price before the sale?" % a, "$40",
                   ["$39.10", "$49", "$28.90"],
                   "%s pays 100%% − 15%% = 85%% of the price. 0.85 × ? = $34, so ? = $34 ÷ 0.85 = <b>$40</b>. "
                   "Check: 15%% of $40 = $6, and $40 − $6 = $34. $39.10 adds 15%% of $34, but the 15%% is of the "
                   "<b>original</b> price. $49 adds 15 dollars, and $28.90 takes 15%% off again." % ah.capitalize(), value=40))
    assert F(34) / D("0.85") == 40 and 34 + pc(15, 34) == D("39.10")
    its.append(mcq("A meal costs $50 before tax. HST is 13%, and the family leaves a 15% tip on the price before tax. "
                   "What is the total?", "$64", ["$78", "$57.50", "$56.50"],
                   "HST: 13% of $50 = $6.50. Tip: 15% of $50 = $7.50. $50 + $6.50 + $7.50 = <b>$64</b>. "
                   "$78 adds 13 and 15 dollars, and $57.50 and $56.50 each forget one of the two parts.", value=64))
    its.append(mcq("A board game costs $56.50 including 13% HST. What was the price before tax?", "$50",
                   ["$43.50", "$63", "$6.50"],
                   "The total is 113% of the price: 1.13 × ? = $56.50, so ? = $56.50 ÷ 1.13 = <b>$50</b>. "
                   "Check: 13% of $50 = $6.50. $43.50 subtracts 13 dollars, $63 adds the $6.50 tax a second time, "
                   "and $6.50 is only the tax.", value=50))
    assert D("56.50") / D("1.13") == 50 and D("56.50") + pc(13, 50) == 63
    assert len(its) == 20, len(its)
    order = [0, 1, 2, 5, 3, 4, 7, 9, 8, 6, 10, 11, 12, 13, 14, 15, 16, 18, 17, 19]
    its = [its[i] for i in order]
    return {"title": "Word problems: HST, discounts and population growth", "items": its}


# ============================================================ lesson
def body_html():
    f_line = percent_line_svg([0, 50, 100, 150], ["0", "20", "40", "60"], "percent line: 150% of 40 is 60")
    f_grid = hundred_grid_svg(1)
    return (
        "<h2>Percent means “out of 100”</h2>"
        "<p>To use a percent in a calculation, divide it by 100 to get a decimal. Then multiply. "
        "This works for every percent: 25%, 150% or 0.5%.</p>"
        + table(["Percent", "Decimal", "Fraction", "Size compared with the whole"], [
            ["150%", "1.5", "1" + fr(1, 2), "more than the whole"],
            ["100%", "1", "1", "the whole"],
            ["12.5%", "0.125", fr(1, 8), "less than the whole"],
            ["1%", "0.01", fr(1, 100), "one hundredth"],
            ["0.5%", "0.005", fr(1, 200), "half of one hundredth"],
        ])
        + "<h2>Percents over 100%</h2>"
        "<p>100% is the whole amount. A percent over 100% gives <b>more</b> than the amount you started with.</p>"
        "<figure class='sn-fig'>" + f_line +
        "<figcaption>100% of 40 is 40. 50% is 20 more, so 150% of 40 is 40 + 20 = 60.</figcaption></figure>"
        + ex("Example", "What is 150% of 40?", "150% = 1.5. 1.5 × 40 = 60.", "60")
        + "<h2>Percents under 1%</h2>"
        "<p>A percent under 1% is a very small part. Find 1% first (divide by 100), then take part of it.</p>"
        "<figure class='sn-fig'>" + f_grid +
        "<figcaption>Each square is 1% of the grid. Half of one square is 0.5%.</figcaption></figure>"
        + ex("Example", "What is 0.5% of 2000?", "1% of 2000 = 20. 0.5% is half of 1%: 20 ÷ 2 = 10.", "10")
        + "<h2>Percent increase and decrease</h2>"
        "<p>Percent change = change ÷ <b>starting</b> value × 100. To increase by 20%, multiply by 1.2. "
        "To decrease by 15%, multiply by 0.85.</p>"
        + ex("Percent change", "A price rises from $20 to $25. What is the percent increase?",
             "Change = $5. Divide by the starting price: 5 ÷ 20 = 0.25.", "25%")
        + ex("HST", "A $40 hoodie plus 13% HST. What is the total?",
             "13% of $40 = 0.13 × 40 = $5.20. $40 + $5.20 = $45.20. Or 1.13 × $40 = $45.20.", "$45.20")
        + "<h2>Common mistakes</h2>"
        + table(["Mistake", "What to do instead"], [
            ["150% of 40 = 40 + 150 = 190", "150% = 1.5, so 1.5 × 40 = 60"],
            ["0.5% = 0.5 (one half)", "0.5% = 0.5 ÷ 100 = 0.005"],
            ["0.5% of 2000 = 1000", "1% of 2000 is 20, so 0.5% is 10"],
            ["$20 to $25 is a 5% increase", "Divide the change by the start: 5 ÷ 20 = 25%"],
            ["Increase 60 by 150% = 90", "90 is 150% of 60. Add it on: 60 + 90 = 150"],
        ])
    )


FAQ = [
    {"q": "What do Grade 8 students learn about percents in Ontario?",
     "a": "In the Ontario Grade 8 math curriculum, students use fractions, decimals and percents interchangeably, including percents of more than 100% and less than 1%, to solve problems such as percent increase and decrease, sales tax and discounts."},
    {"q": "How do you find a percent of a number that is more than 100%?",
     "a": "Write the percent as a decimal and multiply. For 150% of 40, 150% = 1.5 and 1.5 × 40 = 60, which is more than 40 because 150% is more than the whole."},
    {"q": "How do you find a percent that is less than 1%?",
     "a": "Find 1% first by dividing by 100, then take part of it. For 0.5% of 2000, 1% is 20 and 0.5% is half of that, so the answer is 10."},
    {"q": "How do you calculate percent increase or decrease?",
     "a": "Subtract to find the change, divide it by the starting value, then multiply by 100. From $20 to $25 the change is $5, and 5 ÷ 20 = 0.25, so the increase is 25%."},
]


def mark_large(u, pattern):
    """Tag pictures that must print larger (percent lines, hundred grids)."""
    rx = re.compile(r"<svg (?=[^>]*aria-label='" + pattern + ")")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u


def gen():
    rnd = random.Random(48803)
    P = People(rnd)
    sets = [set_over_100(), set_under_1(), set_convert(), set_change(), set_problems(P)]
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
        "country": "ca-on", "subject": "math", "grade": "grade-8", "slug": "percents", "sort": 3,
        "updated": UPDATED, "pdf_url": "",
        "title": "Grade 8 Percents: Over 100%, Under 1%, Percent Change and HST",
        "seo_title": "Grade 8 Percents Worksheets: Over 100%, Under 1% and Percent Change, Free Math with Answer Key (Ontario Curriculum)",
        "short_title": "Percents",
        "domain": "Number",
        "standard_code": "Grade 8: B1.4",
        "standard_url": "https://www.dcp.edu.gov.on.ca/en/curriculum/elementary-mathematics",
        "standard_text": "Use fractions, decimal numbers, and percents, including percents of more than 100% or less than 1%, interchangeably and flexibly to solve a variety of problems",
        "meta_desc": "Free Grade 8 math worksheets on percents for the Ontario curriculum: percents over 100% and under 1%, converting fractions, decimals and percents, percent increase and decrease, and HST, discount and population growth problems. 100 questions with an answer key.",
        "key_big": "Change the percent to a decimal, then multiply: 150% = 1.5 and 0.5% = 0.005.",
        "key_sub": "150% of 40 is 1.5 × 40 = 60, not 40 + 150. 0.5% is half of 1%, so 0.5% of 2000 is 10, not 1000.",
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
