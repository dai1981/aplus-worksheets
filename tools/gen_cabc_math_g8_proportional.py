# -*- coding: utf-8 -*-
"""
BC Grade 8 Math: Proportional reasoning (BC Mathematics Curriculum, Grade 8 Number:
"Numerical proportional reasoning (rates, ratio, proportions, and percent)")
  python3 tools/gen_cabc_math_g8_proportional.py
Unit rates and comparing rates, equivalent ratios and ratio tables, solving proportions,
percent problems (percent of, percent change, finding the whole), then word problems with
recipes, map scales and fuel use in BC contexts.
Wrong answers come from real mistakes: additive thinking (adding the same amount instead of
multiplying), inverting a ratio, multiplying without dividing, part-to-part vs part-to-whole,
subtracting a percent as if it were dollars, dividing by the new value, and decimal slips.
Every numeric answer is checked with fractions.Fraction (never float).
Canadian English, dollars and cents, metric units, SI number spacing. HTML attributes use single quotes.
"""
import json, math, os, random, re
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "ca-bc", "math", "grade-8")
SLUG = "proportional-reasoning"
UPDATED = "2026-11-02"
NBSP = " "
GREEN = "#006633"
FILL = "#cfe6d6"
LINE = "#2b2b2b"
RED = "#c0392b"
BLUE = "#2f6fc0"
FONT = "Arial, Helvetica, sans-serif"
CANT = "You can’t tell"
SAME = "They are the same"


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


def pc(x):
    return num(x) + "%"


def fr(a, b):
    return "<span class='fr'><span class='fn'>%s</span><span class='fd'>%s</span></span>" % (a, b)


XV = "<i>x</i>"


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
        return None if m.group(4) else (v, "%")
    return (v, (m.group(4) or "").strip())


def ratio_val(c):
    m = re.match(r"^(\d+(?:\.\d+)?):(\d+(?:\.\d+)?)$", c)
    return F(m.group(1)) / F(m.group(2)) if m else None


def mcq(q, right, wrong, e, value=None):
    """Correct answer first + 3 wrong; balance() moves it. No two choices equal in value.
    value: the exact answer, checked against the correct choice."""
    right = str(right)
    wrong = [str(x) for x in wrong]
    assert len(wrong) == 3, (q, wrong)
    ch = [right] + wrong
    assert len(set(plain(x) for x in ch)) == 4, (q, ch)
    if value is not None:
        v = val(right)
        assert v is not None and v[0] == F(value), (q, right, value)
    vs = [val(x) for x in ch]
    known = [v for v in vs if v is not None]
    assert len(set(known)) == len(known), (q, ch)
    rs = [ratio_val(x) for x in ch]
    rk = [r for r in rs if r is not None]
    assert len(set(rk)) == len(rk), (q, ch)
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


# ------------------------------------------------------------ pictures
def fig(svg):
    return "<div class='qfig'>" + svg + "</div>"


def svg_wrap(w, h, body, label):
    w, h = int(math.ceil(w)), int(math.ceil(h))
    return ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 %d %d' width='%d' height='%d' "
            "role='img' aria-label='%s'><g font-family='%s'>%s</g></svg>" % (w, h, w, h, label, FONT, body))


def text(x, y, t, fs=16, anchor="middle", col=LINE, bold=True):
    return ("<text x='%.1f' y='%.1f' font-size='%d'%s fill='%s' text-anchor='%s'>%s</text>"
            % (x, y, fs, " font-weight='700'" if bold else "", col, anchor, t))


def tw(t, fs):
    """Rough width of bold Arial text."""
    return sum(0.36 if ch in " .,()" else 0.62 for ch in plain(t)) * fs


def cell(c):
    return c if isinstance(c, str) else num(c)


def table_svg(names, rows, label="ratio table"):
    """Two-row ratio table. names: row headings; rows: two lists of numbers or '?' (red)."""
    rows = [[cell(c) for c in r] for r in rows]
    fs = 16
    hw = max(tw(n, 15) for n in names) + 22
    cw = max([50] + [tw(c, fs) + 20 for r in rows for c in r])
    rh = 32
    n = len(rows[0])
    W = 4 + hw + n * cw + 4
    H = 2 * rh + 8
    s = []
    for j, nm in enumerate(names):
        y = 4 + j * rh
        s.append("<rect x='4' y='%d' width='%.1f' height='%d' fill='%s' stroke='%s' stroke-width='2'/>"
                 % (y, hw, rh, FILL, GREEN))
        s.append(text(4 + hw / 2, y + rh / 2 + 6, nm, 15))
        for i, c in enumerate(rows[j]):
            x = 4 + hw + i * cw
            s.append("<rect x='%.1f' y='%d' width='%.1f' height='%d' fill='#ffffff' stroke='%s' stroke-width='2'/>"
                     % (x, y, cw, rh, GREEN))
            s.append(text(x + cw / 2, y + rh / 2 + 6, c, fs, col=RED if c == "?" else LINE))
    return svg_wrap(W, H, "".join(s), label)


def dnl_svg(top_name, bottom_name, pos, top, bottom, label="double number line"):
    """Double number line. pos: exact positions (top-row values) of each tick, used for spacing.
    top / bottom: the labels at each tick (numbers or '?', drawn red)."""
    fs = 16
    nw = max(tw(top_name, 15), tw(bottom_name, 15)) + 14
    L = 6 + nw
    PW = 300.0
    pmax = F(max(pos))
    R = 26
    W = L + PW + R
    yt, yb = 40, 84
    s = []
    for y in (yt, yb):
        s.append("<line x1='%.1f' y1='%d' x2='%.1f' y2='%d' stroke='%s' stroke-width='2'/>"
                 % (L, y, L + PW + 14, y, LINE))
        s.append("<polygon points='%.1f,%d %.1f,%d %.1f,%d' fill='%s'/>"
                 % (L + PW + 20, y, L + PW + 11, y - 5, L + PW + 11, y + 5, LINE))
    s.append(text(6, yt + 5, top_name, 15, "start"))
    s.append(text(6, yb + 5, bottom_name, 15, "start"))
    for p, a, b in zip(pos, top, bottom):
        x = L + float(F(p) / pmax) * PW
        s.append("<line x1='%.1f' y1='%d' x2='%.1f' y2='%d' stroke='%s' stroke-width='2'/>" % (x, yt - 8, x, yt + 8, GREEN))
        s.append("<line x1='%.1f' y1='%d' x2='%.1f' y2='%d' stroke='%s' stroke-width='2'/>" % (x, yb - 8, x, yb + 8, GREEN))
        a, b = cell(a), cell(b)
        s.append(text(x, yt - 14, a, fs, col=RED if a == "?" else LINE))
        s.append(text(x, yb + 26, b, fs, col=RED if b == "?" else LINE))
    return svg_wrap(W, 118, "".join(s), label)


def scale_bar_svg(cm_unit, km):
    """Map scale bar: 2 cm drawn as alternating blocks, labelled 0 and the distance."""
    U = 60.0  # 1 cm on the map drawn as 60 units
    L, y = 20, 34
    s = []
    for i in range(4):
        s.append("<rect x='%.1f' y='%d' width='%.1f' height='12' fill='%s' stroke='%s' stroke-width='2'/>"
                 % (L + i * U / 2, y, U / 2, GREEN if i % 2 == 0 else "#ffffff", GREEN))
    s.append(text(L, y - 8, "0", 15, bold=False))
    s.append(text(L + 2 * U, y - 8, num(km) + " km", 15))
    s.append(text(L + U, y + 34, "2 cm on the map", 15, bold=False))
    return svg_wrap(L + 2 * U + 40, y + 42, "".join(s), "map scale bar")


# ============================================================ set 1: rates and unit rates
def set_rates():
    its = []
    x = F(48, 10) / 6
    its.append(mcq("A pack of 6 granola bars costs $4.80. What is the price of 1 bar?", money(x),
                   ["$1.25", "$28.80", "8¢"],
                   "Unit price = cost ÷ number: $4.80 ÷ 6 = <b>80¢</b>. $1.25 is 6 ÷ 4.80 (the inverted rate), "
                   "$28.80 multiplies, and 8¢ is a decimal slip.", value=x))
    x = F(36, 3)
    its.append(mcq("Kai bikes 36 km in 3 hours on a trail in the Okanagan. What is his speed?", "12 km/h",
                   ["108 km/h", "33 km/h", "39 km/h"],
                   "Speed = distance ÷ time: 36 ÷ 3 = <b>12 km/h</b>. 108 multiplies, 33 subtracts, and 39 adds.",
                   value=x))
    x = F(260, 5)
    its.append(mcq("Simran types 260 words in 5 minutes. How many words does she type per minute?", "52",
                   ["1300", "255", "265"],
                   "Words per minute: 260 ÷ 5 = <b>52</b>. 1300 multiplies, 255 subtracts 5, and 265 adds 5.",
                   value=x))
    x = F(1890, 100) / 10
    its.append(mcq(fig(table_svg(["Litres", "Cost ($)"], [[10, 20, 30], ["18.90", "37.80", "56.70"]],
                                 label="ratio table of litres and cost")) +
                   "The table shows the cost of gas. What is the price per litre?", money(x),
                   ["$18.90", "$189", "$8.90"],
                   "Divide one cost by its litres: $18.90 ÷ 10 = <b>$1.89</b> per litre. Check: $37.80 ÷ 20 = $1.89. "
                   "$18.90 is the cost of 10 L, $189 multiplies by 10, and $8.90 subtracts 10.", value=x))
    its.append(mcq("Which of these is a <b>unit rate</b>?", "80 km per hour",
                   ["160 km in 2 hours", "12 apples for $6", "3 goals in 2 games"],
                   "A unit rate compares an amount to <b>1</b> of something: <b>80 km per hour</b> means 80 km in 1 hour. "
                   "The others compare to 2 hours, 6 dollars or 2 games."))
    a, b = F(455, 100) / F(65, 10), F(650, 100) / 10
    assert b < a
    its.append(mcq("Which is the better buy for yogurt: 650 g for $4.55 or 1 kg for $6.50?",
                   "1 kg for $6.50", ["650 g for $4.55", SAME, CANT],
                   "Price per 100 g: $4.55 ÷ 6.5 = %s and $6.50 ÷ 10 = %s. <b>1 kg for $6.50</b> costs less per 100 g."
                   % (money(a), money(b))))
    rice = [(1, F(34, 10)), (2, F(64, 10)), (5, F(155, 10)), (10, F(32))]
    u = [c / q for q, c in rice]
    assert min(u) == u[2] and u.count(min(u)) == 1
    its.append(mcq("Which bag of rice is the best buy?",
                   "5 kg for $15.50", ["1 kg for $3.40", "2 kg for $6.40", "10 kg for $32"],
                   "Price per kilogram: %s, %s, %s and %s. The lowest is <b>5 kg for $15.50</b>. "
                   "The biggest bag is not always the best buy." % tuple(money(v) for v in u)))
    assert F(300, 57) > F(400, 80)
    its.append(mcq("Liam runs 400 m in 80 seconds. Ava runs 300 m in 57 seconds. Who runs faster?",
                   "Ava", ["Liam", SAME, CANT],
                   "Metres per second: Liam 400 ÷ 80 = 5 m/s. Ava 300 ÷ 57 ≈ 5.26 m/s. <b>Ava</b> is faster, "
                   "even though Liam runs farther."))
    x = F(45, 3) * 5
    its.append(mcq("Noah earns $45 for 3 hours of babysitting. At the same rate, what does he earn for 5 hours?",
                   money(x), ["$47", "$225", "$15"],
                   "Unit rate: $45 ÷ 3 = $15 an hour. 5 × $15 = <b>$75</b>. $47 adds $2 for 2 more hours "
                   "(additive thinking), $225 is 5 × $45, and $15 is the pay for only 1 hour.", value=x))
    x = F(24) / F(3, 2)
    its.append(mcq("A garden hose fills a 24 L bucket in 1.5 minutes. How many litres per minute is that?", "16 L",
                   ["36 L", "22.5 L", "0.0625 L"],
                   "24 ÷ 1.5 = <b>16 L</b> per minute. Check: 16 × 1.5 = 24. 36 multiplies, 22.5 subtracts 1.5, "
                   "and 0.0625 is 1.5 ÷ 24 (minutes per litre).", value=x))
    x = F(18) * 4
    its.append(mcq("Ji-woo counts 18 heartbeats in 15 seconds. What is her heart rate in beats per minute?", "72",
                   ["63", "1.2", "270"],
                   "1 minute is 60 s, which is 4 × 15 s. 4 × 18 = <b>72</b> beats per minute. 63 adds 45 because "
                   "15 + 45 = 60 (additive thinking), 1.2 is beats per second, and 270 is 18 × 15.", value=x))
    x = F(15) * 120
    its.append(mcq("A leaky tap drips 15 mL of water per minute. How much water drips in 2 hours?",
                   num(x) + " mL", ["30 mL", "900 mL", "18" + NBSP + "000 mL"],
                   "2 hours = 120 minutes. 15 × 120 = <b>1800 mL</b> (1.8 L). 30 mL treats 2 hours as 2 minutes, "
                   "900 mL is only 1 hour, and 18\u00a0000 mL is a decimal slip.", value=x))
    x = F(6, 8) * 20
    its.append(mcq(fig(dnl_svg("Distance (km)", "Time (min)", [0, 6, 15], [0, 6, "?"], [0, 8, 20],
                               label="double number line of distance and time")) +
                   "A cyclist rides at a steady speed. How far does she ride in 20 minutes?", "15 km",
                   ["18 km", "120 km", "7.5 km"],
                   "6 km in 8 min is 0.75 km per minute. 0.75 × 20 = <b>15 km</b>. Or: 20 ÷ 8 = 2.5, and 6 × 2.5 = 15. "
                   "18 adds 12 because 8 + 12 = 20 (additive thinking), 120 is 6 × 20, and 7.5 is a decimal slip.",
                   value=x))
    its.append(mcq("Which rate is the same as 90 km/h?", "1.5 km per minute",
                   ["9 km per minute", "0.9 km per minute", "5400 km per minute"],
                   "1 hour is 60 minutes, so 90 ÷ 60 = <b>1.5 km per minute</b>. 9 divides by 10, 0.9 divides by 100, "
                   "and 5400 multiplies by 60 instead of dividing."))
    x = F(20) / F(5, 2)
    its.append(mcq("Snow falls at Whistler at a steady 2.5 cm per hour. How long does it take for 20 cm of snow to fall?",
                   "8 h", ["50 h", "17.5 h", "22.5 h"],
                   "Time = amount ÷ rate: 20 ÷ 2.5 = <b>8 h</b>. Check: 8 × 2.5 = 20 cm. 50 multiplies, "
                   "17.5 subtracts, and 22.5 adds.", value=x))
    assert F(234, 12) > F(133, 7)
    its.append(mcq("Harjot earns $133 for 7 hours of work. Zara earns $234 for 12 hours. Who earns more per hour?",
                   "Zara", ["Harjot", SAME, CANT],
                   "Harjot: $133 ÷ 7 = $19 an hour. Zara: $234 ÷ 12 = $19.50 an hour. <b>Zara</b> earns more per hour."))
    assert F(33, 9) > F(42, 12)
    its.append(mcq("A hockey team scored 42 goals in 12 games. Another team scored 33 goals in 9 games. "
                   "Which team scored more goals per game?",
                   "The team with 33 goals", ["The team with 42 goals", SAME, CANT],
                   "Goals per game: 42 ÷ 12 = 3.5 and 33 ÷ 9 ≈ 3.67. <b>The team with 33 goals</b> scored more per game, "
                   "even though its total is smaller."))
    x = F(75, 100) * 4
    its.append(mcq("Mateo walks 0.75 km in 15 minutes. What is his speed in kilometres per hour?", "3 km/h",
                   ["11.25 km/h", "0.05 km/h", "20 km/h"],
                   "1 hour is 4 × 15 minutes, so 4 × 0.75 = <b>3 km/h</b>. 11.25 is 0.75 × 15, 0.05 is the distance "
                   "in 1 minute, and 20 is 15 ÷ 0.75.", value=x))
    x = F(185, 100) * 42
    its.append(mcq("Gas costs $1.85 per litre in Vancouver. What do 42 L cost?", money(x),
                   ["$43.85", "$7.77", "$40.15"],
                   "Cost = rate × litres: 42 × $1.85 = <b>$77.70</b>. $43.85 adds, $7.77 is a decimal slip, "
                   "and $40.15 subtracts.", value=x))
    x = F(255, 30)
    its.append(mcq("A sockeye salmon swims about 30 km a day up the Fraser River. At this rate, how many days does it "
                   "take to swim 255 km?", "8.5", ["7650", "225", "85"],
                   "Days = distance ÷ rate: 255 ÷ 30 = <b>8.5</b> days. 7650 multiplies, 225 subtracts, "
                   "and 85 is a decimal slip.", value=x))
    assert len(its) == 20
    return {"title": "Rates and unit rates", "items": its}


# ============================================================ set 2: ratios and proportions
def set_ratios():
    its = []
    its.append(mcq("Which ratio is equivalent to 3:5?", "12:20", ["5:7", "5:3", "6:8"],
                   "Multiply both terms by the same number: 3 × 4 = 12 and 5 × 4 = 20, so <b>12:20</b>. "
                   "5:7 and 6:8 add the same number to both terms, which changes the ratio, and 5:3 is upside down."))
    its.append(mcq("Which ratio is equivalent to 18:24?", "3:4", ["9:15", "4:3", "6:12"],
                   "Divide both terms by 6: 18 ÷ 6 = 3 and 24 ÷ 6 = 4, so <b>3:4</b>. 9:15 and 6:12 subtract the same "
                   "number from both terms, and 4:3 is upside down."))
    assert F(4, 6) == F(10, 15)
    its.append(mcq("Is %s = %s a true proportion?" % (fr(4, 6), fr(10, 15)),
                   "Yes. 4 × 15 = 6 × 10", ["No. 15 is not a multiple of 6", "No. 10 − 4 = 6, but 15 − 6 = 9",
                                            "Yes. 4 + 6 = 10"],
                   "Cross-multiply: 4 × 15 = 60 and 6 × 10 = 60. The products match, so it is <b>true</b>. "
                   "Both fractions equal %s. Differences do not matter in a proportion." % fr(2, 3)))
    assert F(6, 9) == F(10, 15)
    its.append(mcq("Which pair of ratios forms a proportion?", "6:9 and 10:15",
                   ["6:9 and 9:12", "6:9 and 8:11", "6:9 and 9:6"],
                   "6:9 = 2:3 and 10:15 = 2:3, so <b>6:9 and 10:15</b> are equal. 9:12 and 8:11 add the same number "
                   "to both terms, and 9:6 is the inverted ratio."))
    x = F(2, 3) * 15
    its.append(mcq(fig(table_svg(["Flour (cups)", "Eggs"], [[2, 4, 6, "?"], [3, 6, 9, 15]],
                                 label="ratio table of flour and eggs")) +
                   "The ratio table is for a pancake recipe. How many cups of flour go with 15 eggs?", "10",
                   ["8", "12", "22.5"],
                   "Each 3 eggs need 2 cups of flour. 15 = 3 × 5, so flour = 2 × 5 = <b>10</b>. "
                   "8 just continues the top row 2, 4, 6, 12 adds 6 like 9 + 6 = 15, and 22.5 inverts the ratio (15 × 3 ÷ 2).",
                   value=x))
    x = F(4, 6) * 27
    its.append(mcq(fig(table_svg(["Distance (km)", "Time (min)"], [[4, 10, "?"], [6, 15, 27]],
                                 label="ratio table of distance and time")) +
                   "Olivia runs at a steady pace. How far does she run in 27 minutes?", "18",
                   ["22", "40.5", "16"],
                   "4 km in 6 min is %s km per minute. %s × 27 = <b>18</b> km. 22 adds 12 like 15 + 12 = 27, "
                   "40.5 inverts the ratio (27 × 6 ÷ 4), and 16 adds 6 like 4 + 6 = 10." % (fr(2, 3), fr(2, 3)), value=x))
    its.append(mcq("A class has 12 girls and 16 boys. What is the ratio of girls to <b>all</b> students?", "3:7",
                   ["3:4", "4:7", "7:3"],
                   "There are 12 + 16 = 28 students. 12:28 = <b>3:7</b> (divide both by 4). 3:4 is girls to boys "
                   "(part to part), 4:7 is boys to all students, and 7:3 is upside down."))
    its.append(mcq("A drink is made with juice and water in the ratio 2:7. What fraction of the drink is juice?",
                   fr(2, 9), [fr(2, 7), fr(7, 9), fr(7, 2)],
                   "There are 2 + 7 = 9 parts in all, and 2 are juice: <b>%s</b>. %s compares juice to water "
                   "(part to part), %s is the water, and %s is upside down." % (fr(2, 9), fr(2, 7), fr(7, 9), fr(7, 2))))
    its.append(mcq("Write 36:90 in simplest form.", "2:5", ["5:2", "3:9", "18:72"],
                   "The greatest common factor is 18: 36 ÷ 18 = 2 and 90 ÷ 18 = 5, so <b>2:5</b>. 5:2 is upside down, "
                   "3:9 divides the two terms by different numbers (12 and 10), and 18:72 subtracts 18 from both."))
    its.append(mcq("Mei says 2:3 and 5:6 are equivalent because she added 3 to each term. Is she right?",
                   "No. 2:3 = 4:6, not 5:6",
                   ["Yes. Adding the same number keeps the ratio", "Yes. Both terms went up by 3",
                    "No. She should add 2 to each term"],
                   "Equivalent ratios come from <b>multiplying</b> both terms by the same number. 2 × 2 = 4 and 3 × 2 = 6, "
                   "so 2:3 = 4:6. 5:6 is not equal: %s ≠ %s. Adding is additive thinking." % (fr(2, 3), fr(5, 6))))
    x = F(3, 2) * 5
    its.append(mcq(fig(dnl_svg("Blue (L)", "White (L)", [0, 2, 5], [0, 2, 5], [0, 3, "?"],
                               label="double number line of blue and white paint")) +
                   "Paint is mixed in the same ratio. How many litres of white go with 5 L of blue?", "7.5",
                   ["6", "15", "10"],
                   "White is 3 ÷ 2 = 1.5 times the blue. 1.5 × 5 = <b>7.5</b> L. 6 adds 3 because 2 + 3 = 5 "
                   "(additive thinking), 15 is 3 × 5, and 10 is 2 × 5.", value=x))
    x = F(36, 4) * 5
    its.append(mcq("The ratio of cats to dogs at an animal shelter in Surrey is 4:5. There are 36 cats. How many dogs are there?",
                   "45", ["37", "28.8", "81"],
                   "36 = 4 × 9, so dogs = 5 × 9 = <b>45</b>. 37 adds 1 because 5 is 1 more than 4, "
                   "28.8 inverts the ratio (36 × 4 ÷ 5), and 81 is cats and dogs together.", value=x))
    x = F(88, 11) * 3
    its.append(mcq("A jar has red and green marbles in the ratio 3:8. There are 88 marbles in all. How many are red?",
                   "24", ["64", "33", "8"],
                   "3 + 8 = 11 parts, and 88 ÷ 11 = 8 marbles in each part. Red = 3 × 8 = <b>24</b>. "
                   "64 is the green marbles, 33 uses %s of 88 (part to part instead of part to whole), "
                   "and 8 is only one part." % fr(3, 8), value=x))
    assert F(15, 12) == F(5, 4)
    its.append(mcq("The ratio of boys to girls on a soccer team is 5:4. Which could be the numbers of boys and girls?",
                   "15 boys and 12 girls", ["6 boys and 5 girls", "4 boys and 5 girls", "10 boys and 9 girls"],
                   "15:12 = 5:4 (divide both by 3), so <b>15 boys and 12 girls</b>. 6:5 and 10:9 add the same number "
                   "to both terms, and 4 boys and 5 girls is the ratio the wrong way round."))
    a, b = F(2, 5), F(3, 7)
    assert b > a
    its.append(mcq("Which orange drink is stronger: 2 cups of concentrate with 5 cups of water, or 3 cups of concentrate "
                   "with 7 cups of water?",
                   "3 cups with 7 cups of water", ["2 cups with 5 cups of water", SAME, CANT],
                   "Concentrate per cup of water: 2 ÷ 5 = 0.4 and 3 ÷ 7 ≈ 0.43. <b>3 cups with 7 cups of water</b> is "
                   "stronger. The second drink has more water, but it also has more concentrate, so compare ratios, not amounts."))
    x = F(60, 8)
    its.append(mcq("A school field trip needs at least 1 adult for every 8 students. 60 students are going. "
                   "What is the smallest number of adults needed?", "8", ["7", "7.5", "480"],
                   "60 ÷ 8 = 7.5. Half an adult is not possible, and 7 adults could take only 56 students, "
                   "so round up to <b>8</b>. 480 is 60 × 8.", value=8))
    assert F(3, 4) == F(15, 10) / 2
    its.append(mcq("Which ratio is equivalent to 1.5:2?", "3:4", ["2.5:3", "15:2", "4:3"],
                   "Multiply both terms by 2 to clear the decimal: 1.5 × 2 = 3 and 2 × 2 = 4, so <b>3:4</b>. "
                   "2.5:3 adds 1 to each term, 15:2 multiplies only the first term by 10, and 4:3 is upside down."))
    x = F(6, 3) * 4
    its.append(mcq("A granola recipe uses oats, flour and maple syrup in the ratio 4:3:1. Ava uses 6 cups of flour. "
                   "How many cups of oats does she need?", "8", ["7", "4.5", "2"],
                   "Flour is 3 parts, so 1 part is 6 ÷ 3 = 2 cups. Oats = 4 × 2 = <b>8</b>. 7 adds 1 like 3 + 1 = 4, "
                   "4.5 inverts the ratio (6 × 3 ÷ 4), and 2 cups is the maple syrup.", value=x))
    xs, ys = [2, 4, 6], [9, 15, 21]
    assert len({F(b, a) for a, b in zip(xs, ys)}) > 1
    its.append(mcq(fig(table_svg(["Tickets", "Cost ($)"], [xs, ys], label="table of tickets and cost")) +
                   "Is this a ratio table (are all the ratios equivalent)?",
                   "No. 2:9 and 4:15 are not equivalent",
                   ["Yes. The cost goes up by $6 each time", "Yes. The tickets go up by 2 each time",
                    "Yes. Each ticket costs $4.50"],
                   "2 tickets cost $9 ($4.50 each), but 4 tickets cost $15 ($3.75 each). The unit price changes, "
                   "so it is <b>not</b> a ratio table. Going up by the same amount is adding, not multiplying."))
    x = F(15) * F(25, 10)
    its.append(mcq("A photo 10 cm wide and 15 cm tall is enlarged to 25 cm wide. How tall is the enlargement?",
                   "37.5 cm", ["30 cm", "22.5 cm", "375 cm"],
                   "The width is multiplied by 25 ÷ 10 = 2.5, so the height is 15 × 2.5 = <b>37.5 cm</b>. "
                   "30 cm adds 15 cm like 10 + 15 = 25 (additive thinking: the photo would look stretched), "
                   "22.5 cm uses 15 ÷ 10 = 1.5 as the multiplier, and 375 cm forgets to divide by 10.", value=x))
    assert len(its) == 20
    return {"title": "Equivalent ratios and proportions", "items": its}


# ============================================================ set 3: solving proportions
def set_solve():
    its = []
    xv = XV

    def check(a, b, c, d):
        assert F(a) / F(b) == F(c) / F(d), (a, b, c, d)

    def sq(lhs, rhs, x, wrong, e):
        return mcq("Solve: %s = %s" % (lhs, rhs), num(x), [num(w) for w in wrong], e, value=x)

    x = F(6); check(x, 8, 3, 4)
    its.append(sq(fr(xv, 8), fr(3, 4), x, [7, 24, 2],
                  "8 = 4 × 2, so %s = 3 × 2 = <b>6</b>. 7 adds 4 because 4 + 4 = 8 (additive thinking), "
                  "24 is 8 × 3, and 2 is only the multiplier." % xv))
    x = F(14); check(2, 5, x, 35)
    its.append(sq(fr(2, 5), fr(xv, 35), x, [32, F(175, 2), 70],
                  "35 = 5 × 7, so %s = 2 × 7 = <b>14</b>. 32 adds 30 like 5 + 30 = 35, 87.5 inverts the ratio "
                  "(35 × 5 ÷ 2), and 70 is 2 × 35." % xv))
    x = F(21); check(9, x, 3, 7)
    its.append(sq(fr(9, xv), fr(3, 7), x, [13, 63, 3],
                  "9 = 3 × 3, so %s = 7 × 3 = <b>21</b>. 13 adds 6 like 3 + 6 = 9, 63 is 9 × 7, "
                  "and 3 is only the multiplier." % xv))
    x = F(16 * 9, 12); check(12, 16, 9, x)
    its.append(sq(fr(12, 16), fr(9, xv), x, [13, F(27, 4), 144],
                  "%s = %s, and 9 = 3 × 3, so %s = 4 × 3 = <b>12</b>. 13 subtracts 3 like 12 − 3 = 9, "
                  "6.75 is 9 × 12 ÷ 16 (inverted), and 144 is 9 × 16." % (fr(12, 16), fr(3, 4), xv)))
    x = F(9, 2) * 6 / 9; check(x, F(9, 2), 6, 9)
    its.append(sq(fr(xv, "4.5"), fr(6, 9), x, [F(3, 2), F(27, 4), 27],
                  "%s = %s, so %s = %s × 4.5 = <b>3</b>. 1.5 subtracts 3 like 9 − 3 = 6, 6.75 inverts the ratio, "
                  "and 27 is 4.5 × 6." % (fr(6, 9), fr(2, 3), xv, fr(2, 3))))
    x = F(7 * 30, 21); check(7, x, 21, 30)
    its.append(mcq("Solve: 7:%s = 21:30" % xv, num(x), ["16", "90", "210"],
                   "21 = 7 × 3, so %s = 30 ÷ 3 = <b>10</b>. 16 subtracts 14 like 21 − 14 = 7, 90 is 21 × 30 ÷ 7, "
                   "and 210 is 7 × 30." % xv, value=x))
    x = F(24, 10) * 5 / 3; check(F(24, 10), x, 3, 5)
    its.append(mcq("Solve: 2.4:%s = 3:5" % xv, num(x), ["4.4", "1.44", "12"],
                   "2.4 = 3 × 0.8, so %s = 5 × 0.8 = <b>4</b>. 4.4 subtracts 0.6 like 3 − 0.6 = 2.4, "
                   "1.44 is 2.4 × 3 ÷ 5, and 12 is 2.4 × 5." % xv, value=x))
    x = F(15) / F(3, 5)
    its.append(mcq("Solve: %s = 0.6" % fr(15, xv), num(x), ["9", "15.6", "14.4"],
                   "0.6%s = 15, so %s = 15 ÷ 0.6 = <b>25</b>. Check: 15 ÷ 25 = 0.6. 9 is 15 × 0.6, "
                   "15.6 adds 0.6, and 14.4 subtracts 0.6." % (xv, xv), value=x))
    x = F(12 * 5, 8); check(x, 12, 5, 8)
    its.append(sq(fr(xv, 12), fr(5, 8), x, [9, F(96, 5), 60],
                  "12 ÷ 8 = 1.5, so %s = 5 × 1.5 = <b>7.5</b>. 9 adds 4 like 8 + 4 = 12, 19.2 is 12 × 8 ÷ 5, "
                  "and 60 is 12 × 5." % xv))
    x = F(9, 2) * 8 / 3; check(3, 8, F(9, 2), x)
    its.append(sq(fr(3, 8), fr("4.5", xv), x, [F(19, 2), 36, F(3, 2)],
                  "4.5 = 3 × 1.5, so %s = 8 × 1.5 = <b>12</b>. 9.5 adds 1.5 like 3 + 1.5 = 4.5, 36 is 4.5 × 8, "
                  "and 1.5 is only the multiplier." % xv))
    assert F(5, 6) == F(8) / (F(48, 5))
    its.append(mcq("5 kg of potatoes cost $6. Which proportion finds the cost %s of 8 kg?" % xv,
                   "%s = %s" % (fr(5, 6), fr(8, xv)),
                   ["%s = %s" % (fr(5, 6), fr(xv, 8)), "%s = %s" % (fr(6, 5), fr(8, xv)),
                    "%s = %s" % (fr(5, xv), fr(8, 6))],
                   "Keep the same order in both ratios: kilograms over dollars on each side, so <b>%s = %s</b>. "
                   "The other choices flip one ratio, so kilograms and dollars no longer match."
                   % (fr(5, 6), fr(8, xv))))
    x = F(6, 5) * 8
    its.append(mcq("5 kg of potatoes cost $6. What do 8 kg cost?", money(x), ["$9", "$48", "$3.75"],
                   "1 kg costs $6 ÷ 5 = $1.20. 8 × $1.20 = <b>$9.60</b>. $9 adds $3 for 3 more kilograms "
                   "(additive thinking), $48 is 8 × $6, and $3.75 is 5 × 6 ÷ 8 (inverted).", value=x))
    x = F(6) * F(3, 2) / 2; check(x, 6, F(3, 2), 2)
    its.append(sq(fr(xv, 6), fr("1.5", 2), x, [F(11, 2), 8, 9],
                  "6 = 2 × 3, so %s = 1.5 × 3 = <b>4.5</b>. 5.5 adds 4 like 2 + 4 = 6, 8 is 6 × 2 ÷ 1.5, "
                  "and 9 is 6 × 1.5." % xv))
    x = F(6, 10) * 25; check(6, 10, x, 25)
    its.append(mcq("Jasleen solves %s = %s and gets 21, because 10 + 15 = 25 and 6 + 15 = 21. What is the correct answer?"
                   % (fr(6, 10), fr(xv, 25)),
                   num(x), ["21", "150", "2.5"],
                   "Ratios grow by multiplying, not adding. 25 = 10 × 2.5, so %s = 6 × 2.5 = <b>15</b>. "
                   "Check: %s = %s = %s. 150 is 6 × 25, and 2.5 is only the multiplier." % (xv, fr(6, 10), fr(15, 25), fr(3, 5)),
                   value=x))
    x = F(18) * 7 / 4; check(4, 7, 18, x)
    its.append(mcq("Which value of %s makes 4:7 = 18:%s true?" % (xv, xv), num(x), ["21", "126", "4.5"],
                   "18 = 4 × 4.5, so %s = 7 × 4.5 = <b>31.5</b>. 21 adds 14 like 4 + 14 = 18, 126 is 18 × 7, "
                   "and 4.5 is only the multiplier." % xv, value=x))
    x = F(8, 10) * 15 / 2; check(F(8, 10), 2, x, 15)
    its.append(sq(fr("0.8", 2), fr(xv, 15), x, [F(138, 10), F(75, 2), 12],
                  "0.8 ÷ 2 = 0.4, so %s = 0.4 × 15 = <b>6</b>. 13.8 subtracts 1.2 like 2 − 1.2 = 0.8, "
                  "37.5 inverts the ratio (15 × 2 ÷ 0.8), and 12 is 0.8 × 15." % xv))
    x = F(250) * 3 / 4; check(x, 250, 3, 4)
    its.append(sq(fr(xv, 250), fr(3, 4), x, [249, 750, F(125, 2)],
                  "%s = 0.75, so %s = 0.75 × 250 = <b>187.5</b>. 249 subtracts 1 like 4 − 1 = 3, 750 is 250 × 3, "
                  "and 62.5 is only %s of 250." % (fr(3, 4), xv, fr(1, 4))))
    x = F(45 * 4, 15); check(45, x, 15, 4)
    its.append(sq(fr(45, xv), fr(15, 4), x, [34, F(675, 4), 180],
                  "45 = 15 × 3, so %s = 4 × 3 = <b>12</b>. 34 subtracts 11 like 15 − 11 = 4, "
                  "168.75 is 45 × 15 ÷ 4, and 180 is 45 × 4." % xv))
    check(F(5, 2), 4, 10, 16)
    assert F(7, 2) / 5 != F(5, 8) and F(5) / F(13, 2) != F(5, 8)
    its.append(mcq("Which proportion is true?", "%s = %s" % (fr("2.5", 4), fr(10, 16)),
                   ["%s = %s" % (fr("2.5", 4), fr("3.5", 5)), "%s = %s" % (fr("2.5", 4), fr(4, "2.5")),
                    "%s = %s" % (fr("2.5", 4), fr(5, "6.5"))],
                   "Cross-multiply: 2.5 × 16 = 40 and 4 × 10 = 40, so <b>%s = %s</b> is true (both are 0.625). "
                   "%s and %s add the same number to the top and bottom, and %s is upside down."
                   % (fr("2.5", 4), fr(10, 16), fr("3.5", 5), fr(5, "6.5"), fr(4, "2.5"))))
    x = F(5) * 18 / 12; check(x, 5, 18, 12)
    its.append(sq(fr(xv, 5), fr(18, 12), x, [11, 90, F(216, 5)],
                  "%s = 1.5, so %s = 1.5 × 5 = <b>7.5</b>. 11 adds 6 like 12 + 6 = 18, 90 is 5 × 18, "
                  "and 43.2 is 18 × 12 ÷ 5 (the wrong pair)." % (fr(18, 12), xv)))
    assert len(its) == 20
    return {"title": "Solving proportions", "items": its}


# ============================================================ set 4: percent problems
def set_percent():
    its = []
    x = F(25, 100) * 80
    its.append(mcq("What is 25% of 80?", num(x), ["3.2", "55", "2000"],
                   "25%% = 0.25, and 0.25 × 80 = <b>20</b>. Or: 25%% is %s, and 80 ÷ 4 = 20. 3.2 is 80 ÷ 25, "
                   "55 is 80 − 25, and 2000 is 80 × 25." % fr(1, 4), value=x))
    x = F(15, 100) * 60
    its.append(mcq("What is 15% of 60?", num(x), ["4", "45", "900"],
                   "10% of 60 is 6 and 5% is 3, so 15% is 6 + 3 = <b>9</b>. 4 is 60 ÷ 15, 45 is 60 − 15, "
                   "and 900 is 60 × 15.", value=x))
    x = F(120, 100) * 45
    its.append(mcq("What is 120% of 45?", num(x), ["165", "5.4", "37.5"],
                   "120% = 1.2, and 1.2 × 45 = <b>54</b>. More than 100% gives more than 45. 165 adds 120, "
                   "5.4 is a decimal slip, and 37.5 is 45 ÷ 1.2.", value=x))
    x = F(5, 1000) * 400
    its.append(mcq("What is 0.5% of 400?", num(x), ["200", "20", "0.2"],
                   "1% of 400 is 4, so 0.5% is half of 4 = <b>2</b>. 200 is 50%, 20 is 5%, and 0.2 is 0.05%.",
                   value=x))
    x = F(18, 24) * 100
    its.append(mcq("18 is what percent of 24?", pc(x), ["6%", "18%", "25%"],
                   "Part ÷ whole = 18 ÷ 24 = 0.75 = <b>75%</b>. 6% is 24 − 18, 18% uses the part as the percent, "
                   "and 25% is the part that is left.", value=x))
    x = F(12) / F(30, 100)
    its.append(mcq("12 is 30% of what number?", num(x), ["3.6", "42", "360"],
                   "Write a proportion: %s = %s. 12 ÷ 0.3 = <b>40</b>. Check: 30%% of 40 = 12. "
                   "3.6 is 30%% of 12, 42 is 12 + 30, and 360 is 12 × 30." % (fr(12, XV), fr(30, 100)), value=x))
    x = F(50 - 40, 40) * 100
    its.append(mcq("A price goes up from $40 to $50. What is the percent increase?", pc(x), ["20%", "10%", "125%"],
                   "Increase ÷ original = 10 ÷ 40 = 0.25 = <b>25%</b>. 20% divides by the new price ($50), 10% is the "
                   "dollar change, and 125% is the new price as a percent of the old one.", value=x))
    x = F(80 - 60, 80) * 100
    its.append(mcq("A number drops from 80 to 60. What is the percent decrease?", pc(x),
                   ["20%", "75%", "about 33%"],
                   "Decrease ÷ original = 20 ÷ 80 = 0.25 = <b>25%</b>. 20% is the change itself, 75% is the new value "
                   "as a percent of the original, and about 33% divides by 60, the new value.", value=x))
    x = F(90) * F(70, 100)
    its.append(mcq("A rain jacket costs $90. It is on sale for 30% off. What is the sale price?", money(x),
                   ["$60", "$27", "$117"],
                   "30% of $90 is $27. $90 − $27 = <b>$63</b>. Or: pay 70%, and 0.7 × $90 = $63. "
                   "$60 subtracts $30 instead of 30%, $27 is only the discount, and $117 adds 30%.", value=x))
    x = F(45) * F(120, 100)
    its.append(mcq("Increase 45 by 20%.", num(x), ["65", "9", "36"],
                   "20% of 45 is 9. 45 + 9 = <b>54</b>. Or: 1.2 × 45 = 54. 65 adds 20, 9 is only the increase, "
                   "and 36 decreases by 20%.", value=x))
    x = F(36) / F(75, 100)
    its.append(mcq("After a 25% discount, a pair of skates costs $36. What was the original price?", money(x),
                   ["$45", "$27", "$61"],
                   "$36 is 75% of the original price. $36 ÷ 0.75 = <b>$48</b>. Check: 25% of $48 is $12, and "
                   "$48 − $12 = $36. $45 adds 25% of $36 (the wrong whole), $27 takes 25% off again, and $61 adds $25.",
                   value=x))
    x = F(125, 1000) * 64
    its.append(mcq("What is 12.5% of 64?", num(x), ["80", "0.8", "51.5"],
                   "12.5%% = 0.125 = %s, and 64 ÷ 8 = <b>8</b>. 80 uses 1.25, 0.8 uses 0.0125, and 51.5 is 64 − 12.5."
                   % fr(1, 8), value=x))
    x = F(250, 100) * 18
    its.append(mcq("What is 250% of 18?", num(x), ["268", "4.5", "7.2"],
                   "250% = 2.5, and 2.5 × 18 = <b>45</b>. 268 adds 250, 4.5 is a decimal slip, and 7.2 is 18 ÷ 2.5.",
                   value=x))
    x = F(34) / F(85, 100)
    its.append(mcq("Sofia got 34 questions right on a math test. That is 85% of the questions. How many questions were on the test?",
                   num(x), ["28.9", "119", "49"],
                   "34 is 85% of the total: 34 ÷ 0.85 = <b>40</b>. Check: 85% of 40 = 34. 28.9 is 85% of 34, "
                   "119 is 34 + 85, and 49 adds the missing 15 as if it were 15 questions.", value=x))
    a, b = F(6, 20), F(6, 50)
    assert a > b
    its.append(mcq("Two bean plants each grow 6 cm. One grew from 20 cm to 26 cm. The other grew from 50 cm to 56 cm. "
                   "Which grew more <b>relative to its height</b>?",
                   "The 20 cm plant", ["The 50 cm plant", SAME, CANT],
                   "Percent increase: 6 ÷ 20 = 30% and 6 ÷ 50 = 12%. <b>The 20 cm plant</b> grew more relative to its height. "
                   "The same 6 cm is the additive view, not the proportional one."))
    assert F(110, 100) * F(90, 100) == F(99, 100)
    its.append(mcq("A price goes up 10%, then the new price goes down 10%. How does the final price compare with the start?",
                   "1% lower", ["The same", "1% higher", "10% lower"],
                   "Use $100: up 10% gives $110, and 10% of $110 is $11, so $110 − $11 = $99. That is <b>1% lower</b>. "
                   "The two 10% are of different amounts, so they do not cancel."))
    x = F(24) * F(115, 100)
    its.append(mcq("A family lunch costs $24. They add a 15% tip. What is the total?", money(x),
                   ["$39", "$3.60", "$20.40"],
                   "15% of $24 = 0.15 × 24 = $3.60. $24 + $3.60 = <b>$27.60</b>. $39 adds $15, $3.60 is only the tip, "
                   "and $20.40 subtracts it.", value=x))
    x = F(65, 50) * 100
    its.append(mcq("What percent of 50 is 65?", pc(x), ["15%", "65%", "30%"],
                   "65 ÷ 50 = 1.3 = <b>130%</b>. The part is bigger than the whole, so the percent is more than 100%. "
                   "15% is 65 − 50, 65% uses the part as the percent, and 30% is only the increase.", value=x))
    x = F(15000) * F(108, 100)
    its.append(mcq("A town in the Okanagan has 15" + NBSP + "000 people. The population grows by 8%. What is the new population?",
                   num(x), ["15" + NBSP + "008", "1200", "13" + NBSP + "800"],
                   "8% of 15 000 = 0.08 × 15 000 = 1200. 15 000 + 1200 = <b>16 200</b>. 15 008 adds 8 people, "
                   "1200 is only the increase, and 13 800 is a decrease.".replace("15 000", "15" + NBSP + "000")
                   .replace("16 200", "16" + NBSP + "200").replace("15 008", "15" + NBSP + "008")
                   .replace("13 800", "13" + NBSP + "800"), value=x))
    x = F(24) / F(120, 100)
    its.append(mcq("After a 20% raise, Nadia earns $24 an hour. What did she earn before the raise?", money(x),
                   ["$19.20", "$4.80", "$28.80"],
                   "$24 is 120% of the old pay. $24 ÷ 1.2 = <b>$20</b>. Check: 20% of $20 is $4, and $20 + $4 = $24. "
                   "$19.20 takes 20% of $24 away, $4.80 is 20% of $24, and $28.80 adds 20%.", value=x))
    assert len(its) == 20
    return {"title": "Percent problems: percent of, percent change and finding the whole", "items": its}


# ============================================================ set 5: word problems
def set_problems():
    its = []
    x = F(5) * 20
    its.append(mcq("On a map with the scale 1 cm : 20 km, Vancouver and Whistler are 5 cm apart in a straight line. "
                   "About how far apart are they?", num(x) + " km", ["25 km", "4 km", "1000 km"],
                   "Each centimetre is 20 km. 5 × 20 = <b>100 km</b>. 25 km adds 5 and 20, 4 km is 20 ÷ 5, "
                   "and 1000 km is a decimal slip.", value=x))
    x = F(5, 2) * 7
    its.append(mcq(fig(scale_bar_svg(2, 5)) +
                   "The scale bar on a hiking map shows that 2 cm stands for 5 km. Two lakes are 7 cm apart on the map. "
                   "How far apart are they?", num(x) + " km", ["10 km", "35 km", "2.8 km"],
                   "1 cm stands for 5 ÷ 2 = 2.5 km. 7 × 2.5 = <b>17.5 km</b>. 10 km adds 5 because 2 + 5 = 7 "
                   "(additive thinking), 35 km is 7 × 5, and 2.8 km inverts the scale (7 × 2 ÷ 5).", value=x))
    x = F(110, 25)
    its.append(mcq("Victoria and Nanaimo are about 110 km apart. On a map with the scale 1 cm : 25 km, how far apart are they?",
                   num(x) + " cm", ["2750 cm", "85 cm", "44 cm"],
                   "Each 25 km is 1 cm. 110 ÷ 25 = <b>4.4 cm</b>. 2750 multiplies instead of dividing, 85 is 110 − 25, "
                   "and 44 cm is a decimal slip.", value=x))
    x = F(3 * 50000, 100000)
    its.append(mcq("A trail map has the scale 1:50" + NBSP + "000. A trail is 3 cm long on the map. How long is the real trail?",
                   num(x) + " km", ["150 km", "15 km", "0.15 km"],
                   "3 × 50 000 = 150 000 cm. 100 000 cm = 1 km, so 150 000 cm = <b>1.5 km</b>. "
                   "The other answers move the decimal point the wrong number of places."
                   .replace("50 000", "50" + NBSP + "000").replace("150 000", "150" + NBSP + "000")
                   .replace("100 000", "100" + NBSP + "000"), value=x))
    x = F(5, 2) * 30 / 12
    its.append(mcq("A muffin recipe makes 12 muffins with 2.5 cups of flour. How much flour is needed for 30 muffins?",
                   num(x) + " cups", ["20.5 cups", "75 cups", "1 cup"],
                   "30 ÷ 12 = 2.5 times the recipe. 2.5 × 2.5 = <b>6.25 cups</b>. 20.5 adds 18 because 12 + 18 = 30 "
                   "(additive thinking), 75 is 2.5 × 30, and 1 cup inverts the ratio (2.5 × 12 ÷ 30).", value=x))
    x = F(600) * 6 / 8
    its.append(mcq("A salmon chowder recipe for 8 people uses 600 g of salmon. How much salmon is needed for 6 people?",
                   num(x) + " g", ["598 g", "800 g", "75 g"],
                   "600 ÷ 8 = 75 g per person. 6 × 75 = <b>450 g</b>. 598 g subtracts 2 because 8 − 2 = 6, "
                   "800 g inverts the ratio (600 × 8 ÷ 6), and 75 g is for only 1 person.", value=x))
    x = F(750) * 2 / 5
    its.append(mcq("A granola bar recipe uses oats and honey in the ratio 5:2 by mass. Chloe uses 750 g of oats. "
                   "How much honey does she need?", num(x) + " g", ["747 g", "1875 g", "1500 g"],
                   "750 = 5 × 150, so honey = 2 × 150 = <b>300 g</b>. 747 g subtracts 3 like 5 − 3 = 2, "
                   "1875 g inverts the ratio, and 1500 g is 750 × 2.", value=x))
    x = F(3) * 12 / 4
    its.append(mcq("Pancakes for 4 people use 3 eggs. How many eggs are needed for 12 people?", num(x),
                   ["11", "16", "36"],
                   "12 people is 3 times as many as 4, so use 3 × 3 = <b>9</b> eggs. 11 adds 8 because 4 + 8 = 12 "
                   "(additive thinking), 16 is 4 × 12 ÷ 3 (inverted), and 36 is 3 × 12.", value=x))
    x = F(7) * F(350, 100)
    its.append(mcq("A car uses 7 L of gas per 100 km. The drive from Vancouver to Kamloops is about 350 km. "
                   "How much gas does the car use?", num(x) + " L", ["357 L", "2450 L", "50 L"],
                   "350 km is 3.5 × 100 km. 7 × 3.5 = <b>24.5 L</b>. 357 adds 7, 2450 forgets to divide by 100, "
                   "and 50 is 350 ÷ 7.", value=x))
    x = F(8) * F(390, 100) * F(180, 100)
    its.append(mcq("A car uses 8 L of gas per 100 km, and gas costs $1.80 per litre. What does the gas cost for the "
                   "390 km drive from Vancouver to Kelowna?", money(x), ["$31.20", "$14.40", "$561.60"],
                   "Gas: 8 × 3.9 = 31.2 L. Cost: 31.2 × $1.80 = <b>$56.16</b>. $31.20 uses the litres as dollars, "
                   "$14.40 is the cost for only 100 km, and $561.60 is a decimal slip.", value=x))
    x = F(55) / F(55, 10) * 100
    its.append(mcq("A hybrid car’s tank holds 55 L. The car uses 5.5 L of gas per 100 km. How far can it go on a full tank?",
                   num(x) + " km", ["302.5 km", "10 km", "30" + NBSP + "250 km"],
                   "55 ÷ 5.5 = 10, so a full tank lasts 10 × 100 km = <b>1000 km</b>. 302.5 is 55 × 5.5, "
                   "10 km forgets that 5.5 L is for 100 km, and 30 250 km is 55 × 5.5 × 100."
                   .replace("30 250", "30" + NBSP + "250"), value=x))
    x = F(36) / F(3, 2) * F(40, 60)
    its.append(mcq("A BC Ferries boat travels 36 km in 1.5 hours. At the same speed, how far does it travel in 40 minutes?",
                   num(x) + " km", ["24 km", "60 km", "9.6 km"],
                   "Speed: 36 ÷ 1.5 = 24 km/h. 40 minutes is %s of an hour, so %s × 24 = <b>16 km</b>. 24 km is the "
                   "distance in 1 hour, and 60 km and 9.6 km treat 40 minutes as 0.4 hours." % (fr(2, 3), fr(2, 3)),
                   value=x))
    b = F(28) / 4
    assert F(65, 10) < b
    its.append(mcq("Car A uses 6.5 L of gas per 100 km. Car B uses 28 L to drive 400 km. Which car uses less gas?",
                   "Car A", ["Car B", SAME, CANT],
                   "Change Car B to litres per 100 km: 400 km is 4 × 100 km, so 28 ÷ 4 = 7 L per 100 km. "
                   "6.5 &lt; 7, so <b>Car A</b> uses less gas."))
    x = F(25) * 4
    its.append(mcq("A plan of a park in Burnaby uses the scale 1 cm : 4 m. A soccer field is 25 cm long on the plan. "
                   "How long is the real field?", num(x) + " m", ["29 m", "6.25 m", "10 m"],
                   "Each centimetre is 4 m. 25 × 4 = <b>100 m</b>. 29 m adds 4, 6.25 m divides by 4, "
                   "and 10 m is a decimal slip.", value=x))
    x = F(40, 100) * 600
    its.append(mcq("Trail mix for a hike is 40% peanuts by mass. How many grams of peanuts are in a 600 g bag?",
                   num(x) + " g", ["560 g", "15 g", "360 g"],
                   "40% of 600 = 0.4 × 600 = <b>240 g</b>. 560 g subtracts 40, 15 g is 600 ÷ 40, "
                   "and 360 g is the part that is not peanuts.", value=x))
    x = F(35) / F(5, 2)
    its.append(mcq("For the Terry Fox Run, Ryan’s family pledges $2.50 for each kilometre he runs. He raises $35. "
                   "How far does he run?", num(x) + " km", ["87.5 km", "32.5 km", "37.5 km"],
                   "Distance = money ÷ rate: $35 ÷ $2.50 = <b>14 km</b>. Check: 14 × $2.50 = $35. 87.5 multiplies, "
                   "32.5 subtracts, and 37.5 adds.", value=x))
    x = F(750, 300)
    its.append(mcq("A hiking group on Grouse Mountain climbs 300 m of height per hour. How long does it take them to "
                   "climb 750 m?", num(x) + " h", ["2 h 50 min", "0.4 h", "3 h"],
                   "750 ÷ 300 = <b>2.5 h</b>, which is 2 h 30 min. 2 h 50 min reads 2.5 h as 2 h 50 min "
                   "(an hour has 60 minutes, not 100), 0.4 h is 300 ÷ 750, and 3 h counts full hours only.", value=x))
    x = F(3, 8) * 4
    its.append(mcq("A punch recipe uses 3 parts juice to 5 parts sparkling water. How much juice is in 4 L of punch?",
                   num(x) + " L", ["2.4 L", "2.5 L", "0.5 L"],
                   "There are 3 + 5 = 8 parts, and juice is %s of the punch. %s × 4 = <b>1.5 L</b>. "
                   "2.4 L uses %s (part to part), 2.5 L is the sparkling water, and 0.5 L is only one part."
                   % (fr(3, 8), fr(3, 8), fr(3, 5)), value=x))
    its.append(mcq("On a map, 3 cm stands for 12 km. What is the scale?", "1 cm : 4 km",
                   ["1 cm : 9 km", "1 cm : 0.25 km", "1 cm : 36 km"],
                   "Divide both by 3: 3 cm : 12 km = <b>1 cm : 4 km</b>. 9 km is 12 − 3, 0.25 km is 3 ÷ 12 (inverted), "
                   "and 36 km is 12 × 3."))
    x = F(22) / 5
    its.append(mcq("A hybrid car drives 500 km on the highway and uses 22 L of gas. "
                   "How much gas does it use per 100 km?", num(x) + " L", ["110 L", "0.044 L", "44 L"],
                   "500 km is 5 × 100 km. 22 ÷ 5 = <b>4.4 L</b> per 100 km. 110 L multiplies by 5, 0.044 L is the gas "
                   "for 1 km, and 44 L is a decimal slip.", value=x))
    assert len(its) == 20
    return {"title": "Word problems: recipes, map scales and fuel use", "items": its}


# ============================================================ lesson
def table(head, rows):
    h = "".join("<th>%s</th>" % x for x in head)
    b = "".join("<tr>" + "".join("<td>%s</td>" % c for c in r) + "</tr>" for r in rows)
    return "<div class='sn-tw'><table class='sn-table'><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>" % (h, b)


def ex(title, q, s, a):
    return ("<div class='sn-ex'><span class='sn-ex-t'>%s</span><p class='sn-ex-q'>%s</p>"
            "<p class='sn-ex-s'>%s</p><p class='sn-ex-a'>Answer: %s</p></div>" % (title, q, s, a))


def body_html():
    f_dnl = dnl_svg("Eggs", "People", [0, 4, 8, 12], [0, 3, 6, 9], [0, 4, 8, 12],
                    label="double number line of eggs and people")
    f_tab = table_svg(["Flour (cups)", "Eggs"], [[2, 4, 6, 10], [3, 6, 9, 15]], label="ratio table of flour and eggs")
    return (
        "<h2>Rates, ratios and proportions</h2>"
        "<p>A <b>ratio</b> compares two amounts, like 3 eggs to 4 people (3:4). A <b>rate</b> compares amounts with "
        "different units, like 36 km in 3 h. A <b>unit rate</b> is the amount for 1: 12 km per hour.</p>"
        "<p>Two ratios that are equal make a <b>proportion</b>. You get an equal ratio by <b>multiplying</b> "
        "(or dividing) both terms by the same number. Adding the same number does not work.</p>"
        "<figure class='sn-fig'>" + f_dnl +
        "<figcaption>3 eggs for 4 people. Twice the people need twice the eggs: 6 for 8, and 9 for 12.</figcaption></figure>"
        + "<figure class='sn-fig'>" + f_tab +
        "<figcaption>A ratio table: every column is 2:3. 15 eggs = 3 × 5, so flour = 2 × 5 = 10 cups.</figcaption></figure>"
        + ex("Unit rate", "6 granola bars cost $4.80. What do 10 bars cost?",
             "1 bar: $4.80 ÷ 6 = 80¢. 10 bars: 10 × 80¢.", "$8")
        + "<h2>Solving proportions</h2>"
        "<p>Keep the same order in both ratios. Then find the multiplier, or cross-multiply.</p>"
        + ex("Multiplier", "Solve: %s = %s" % (fr(XV, 8), fr(3, 4)),
             "8 = 4 × 2, so multiply the top by 2 too: 3 × 2.", "%s = 6" % XV)
        + ex("Cross-multiply", "Solve: %s = %s" % (fr(9, XV), fr(3, 7)),
             "3%s = 9 × 7 = 63, so %s = 63 ÷ 3." % (XV, XV), "%s = 21" % XV)
        + "<h2>Percent is a ratio out of 100</h2>"
        "<p>Use part ÷ whole = percent ÷ 100. To find a percent of a number, multiply by the decimal. "
        "To find the whole, divide by the decimal. For a percent change, always divide by the <b>original</b> amount.</p>"
        + ex("Percent of", "A $90 rain jacket is 30% off. What is the sale price?",
             "You pay 70%: 0.7 × $90.", "$63")
        + ex("Find the whole", "After 25% off, skates cost $36. What was the original price?",
             "$36 is 75% of the price: $36 ÷ 0.75.", "$48")
        + ex("Fuel use", "A car uses 7 L per 100 km. How much gas for 350 km?",
             "350 km is 3.5 × 100 km. 7 × 3.5 = 24.5.", "24.5 L")
        + "<h2>Common mistakes</h2>"
        + table(["Mistake", "What to do instead"], [
            ["Adding: 3 eggs for 4 people, so 11 eggs for 12 people (4 + 8 = 12)",
             "Multiply: 12 = 4 × 3, so 3 × 3 = 9 eggs"],
            ["Inverting a ratio: 3 eggs for 4 people, so 12 × 4 ÷ 3 = 16 eggs for 12 people",
             "Keep the same order in both ratios: top to top, bottom to bottom"],
            ["Using part to part for a fraction of the whole (2:7 means %s juice)" % fr(2, 7),
             "Add the parts: 2 + 7 = 9, so the juice is %s" % fr(2, 9)],
            ["Dividing a percent change by the new amount", "Divide by the original: 40 to 50 is 10 ÷ 40 = 25%"],
            ["Finding the original price by adding the percent back on", "Divide by the percent that is left: $36 ÷ 0.75 = $48"],
        ])
    )


FAQ = [
    {"q": "What is proportional reasoning in Grade 8 math in BC?",
     "a": "The BC Grade 8 math curriculum lists numerical proportional reasoning with rates, ratios, proportions and percent. Students use it for best buys, recipes, map scales, fuel use and percent change, by multiplying rather than adding."},
    {"q": "What is the difference between a rate and a ratio?",
     "a": "A ratio compares amounts, often with the same unit, like 3 cups of flour to 2 cups of milk. A rate compares amounts with different units, like 36 km in 3 hours; the unit rate is 12 km per hour."},
    {"q": "How do you solve a proportion like x/8 = 3/4?",
     "a": "Find the multiplier: 8 = 4 × 2, so x = 3 × 2 = 6. You can also cross-multiply: 4x = 24, so x = 6. Never add the same number to both terms."},
    {"q": "How do you find the original price after a percent discount?",
     "a": "Divide the sale price by the percent you still pay. After 25% off, $36 is 75% of the price, so the original price is $36 ÷ 0.75 = $48."},
]


def mark_large(u, pattern):
    """Tag wide pictures so they print larger and stay readable."""
    rx = re.compile(r"<svg (?=[^>]*aria-label='" + pattern + ")")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u


def gen():
    rnd = random.Random(58803)
    sets = [set_rates(), set_ratios(), set_solve(), set_percent(), set_problems()]
    seen = set()
    for s in sets:
        assert len(s["items"]) == 20, (s["title"], len(s["items"]))
        for it in s["items"]:
            assert len(set(it["c"])) == 4, it
            assert it["e"], it["q"]
            assert it["q"].count("<svg") <= 1, it["q"]
            k = plain(it["q"]) + "|" + "|".join(sorted(it["c"]))
            assert k not in seen, it["q"]
            seen.add(k)
    balance(sets, rnd)
    for s in sets:
        assert sorted(it["a"] for it in s["items"]) == sorted([0, 1, 2, 3] * 5)
    u = {
        "country": "ca-bc", "subject": "math", "grade": "grade-8", "slug": SLUG, "sort": 3,
        "updated": UPDATED, "pdf_url": "",
        "title": "Proportional Reasoning: Rates, Ratios, Proportions and Percent",
        "seo_title": "Grade 8 Proportional Reasoning Worksheets: Rates, Proportions and Percent (BC Math, Free)",
        "short_title": "Proportional reasoning",
        "domain": "Number",
        "standard_code": "Grade 8: Number",
        "standard_url": "https://curriculum.gov.bc.ca/curriculum/mathematics/8/core",
        "standard_text": "Numerical proportional reasoning (rates, ratio, proportions, and percent)",
        "meta_desc": "Free Grade 8 math worksheets on proportional reasoning for the BC curriculum: unit rates and best buys, equivalent ratios, solving proportions, percent problems and percent change, and word problems with recipes, map scales and fuel use. 100 questions with an answer key.",
        "key_big": "Proportional means multiply, not add: if 3 eggs serve 4 people, 12 people need 3 × 3 = 9 eggs.",
        "key_sub": "Find a unit rate or a multiplier, keep the same order in both ratios, and treat a percent as a ratio out of 100: part ÷ whole = percent ÷ 100.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }
    return mark_large(u, "double number line|map scale bar")


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
