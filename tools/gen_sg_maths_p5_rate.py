# -*- coding: utf-8 -*-
"""
Singapore Primary 5 Maths: Rate (MOE 2021 Primary Mathematics Syllabus, Standard, Number and Algebra:
"Rate as the amount of a quantity per unit of another quantity; finding rate, total amount or number of units
given the other two quantities")
  python3 tools/gen_sg_maths_p5_rate.py
Finding the rate per unit, finding the total from the rate, finding the number of units, rate tables and
best buys, then word problems with bar models (taxi fares, car park charges, taps filling tanks, typing).
Wrong answers come from real mistakes: dividing the wrong way, multiplying when you should divide,
adding instead of multiplying, mixing per hour and per minute, reading 1 h 30 min as 1.3 h, and decimal slips.
Every numeric answer is checked with fractions.Fraction (never float).
Singapore English, $ and ¢, ℓ and ml, MOE number spacing (no-break space). HTML attributes use single quotes.
"""
import json, math, os, random, re
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "sg", "maths", "primary-5")
SLUG = "rate"
UPDATED = "2026-11-03"
NBSP = " "
GREEN = "#006633"
FILL = "#cfe6d6"
LINE = "#2b2b2b"
RED = "#c0392b"
FONT = "Arial, Helvetica, sans-serif"
CANT = "You cannot tell"
SAME = "They are the same"
L_ = "ℓ"  # ℓ


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


def fr(a, b):
    return "<span class='fr'><span class='fn'>%s</span><span class='fd'>%s</span></span>" % (a, b)


def plain(s):
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", s)).strip()


NUM = re.compile(r"^(\$)?(\d[\d" + NBSP + r"]*(?:\.\d+)?)(¢)?( .+)?$")


def val(c):
    """Value of a choice with its unit, or None when it is not a single number."""
    m = NUM.match(c)
    if not m:
        return None
    v = F(m.group(2).replace(NBSP, ""))
    if (m.group(1) or m.group(3)) and m.group(4):
        return None
    if m.group(1):
        return (v, "$")
    if m.group(3) == "¢":
        return (v / 100, "$")
    return (v, (m.group(4) or "").strip())


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


def table_svg(names, rows, label="rate table"):
    """Two-row rate table. names: row headings; rows: two lists of numbers or text ('?' is red)."""
    rows = [[cell(c) for c in r] for r in rows]
    fs = 16
    hw = max(tw(n, 15) for n in names) + 22
    cw = max([56] + [tw(c, fs) + 20 for r in rows for c in r])
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


def model_svg(rows, label, W=440):
    """Bar model drawn to scale. rows: list of dicts
         name:  text at the left of the bar ('' for none)
         segs:  [(length, text inside, shaded)] drawn left to right
         over:  [(start, end, text)] brackets above the bar (positions in the same length units)
         under: [(start, end, text)] brackets below the bar
       Text containing '?' is drawn red."""
    names = [r.get("name", "") for r in rows]
    nw = (max(tw(n, 15) for n in names) + 12) if any(names) else 0
    L = 8 + nw
    R = W - 10
    tot = max(sum(F(a) for a, _, _ in r["segs"]) for r in rows)
    sc = (R - L) / float(tot)
    s = []
    y = 4
    for r in rows:
        over, under = r.get("over", []), r.get("under", [])
        if over:
            y += 24
            for a, b, t in over:
                x1, x2 = L + float(a) * sc, L + float(b) * sc
                col = RED if "?" in t else LINE
                s.append("<path d='M%.1f %d L%.1f %d L%.1f %d L%.1f %d' fill='none' stroke='%s' stroke-width='2'/>"
                         % (x1, y + 6, x1, y, x2, y, x2, y + 6, col))
                cx = (x1 + x2) / 2
                half = tw(t, 15) / 2 + 2
                cx = min(max(cx, half + 2), W - half - 2)
                s.append(text(cx, y - 6, t, 15, col=col))
            y += 8
        y0 = y
        bh = 34
        x = L
        for a, t, sh in r["segs"]:
            w = float(a) * sc
            s.append("<rect x='%.1f' y='%d' width='%.1f' height='%d' fill='%s' stroke='%s' stroke-width='2'/>"
                     % (x, y0, w, bh, FILL if sh else "#ffffff", LINE))
            if t:
                assert tw(t, 14) + 4 <= w, ("text too wide for segment", t, w)
                s.append(text(x + w / 2, y0 + bh / 2 + 5, t, 14, col=RED if "?" in t else LINE))
            x += w
        if r.get("name"):
            s.append(text(8, y0 + bh / 2 + 5, r["name"], 15, "start"))
        y = y0 + bh
        if under:
            for a, b, t in under:
                x1, x2 = L + float(a) * sc, L + float(b) * sc
                col = RED if "?" in t else LINE
                s.append("<path d='M%.1f %d L%.1f %d L%.1f %d L%.1f %d' fill='none' stroke='%s' stroke-width='2'/>"
                         % (x1, y + 4, x1, y + 10, x2, y + 10, x2, y + 4, col))
                cx = (x1 + x2) / 2
                half = tw(t, 15) / 2 + 2
                cx = min(max(cx, half + 2), W - half - 2)
                s.append(text(cx, y + 28, t, 15, col=col))
            y += 32
        y += 10
    return svg_wrap(W, y - 4, "".join(s), label)


def units_row(name, n, total=None, each=None, ask_one=False, ask_all=False):
    """A row of n equal units. total: text over the whole row; each: text inside every unit;
    ask_one: '?' under the first unit; ask_all: '?' over the whole row."""
    segs = [(1, each or "", True) for _ in range(n)]
    r = {"name": name, "segs": segs}
    if total is not None or ask_all:
        r["over"] = [(0, n, "?" if ask_all else total)]
    if ask_one:
        r["under"] = [(0, 1, "?")]
    return r


# ============================================================ set 1: rate per unit
def set_rate():
    its = []
    x = F(10, 4)
    its.append(mcq("4 kg of rice cost $10. What is the cost per kilogram?", money(x), ["40¢", "$40", "$6"],
                   "Rate = total ÷ number of units: $10 ÷ 4 = <b>$2.50</b> per kg. 40¢ divides the wrong way (4 ÷ 10), "
                   "$40 multiplies, and $6 subtracts.", value=x))
    x = F(240, 6)
    its.append(mcq("Mei Ling types 240 words in 6 minutes. How many words does she type per minute?", num(x),
                   ["1440", "4", "234"],
                   "Words per minute = 240 ÷ 6 = <b>40</b>. 1440 multiplies, 4 drops a zero, and 234 subtracts 6.", value=x))
    x = F(90, 6)
    its.append(mcq("A tap fills a pail with 90 %s of water in 6 minutes. How many litres flow per minute?" % L_,
                   num(x) + " " + L_, ["540 " + L_, "1.5 " + L_, "96 " + L_],
                   "90 ÷ 6 = <b>15 %s</b> per minute. 540 %s multiplies, 1.5 %s is a decimal slip, and 96 %s adds."
                   % (L_, L_, L_, L_), value=x))
    x = F(9, 2) / 3
    its.append(mcq("3 m of ribbon cost $4.50. What is the cost per metre?", money(x), ["$13.50", "15¢", "$7.50"],
                   "$4.50 ÷ 3 = <b>$1.50</b> per metre. $13.50 multiplies, 15¢ is a decimal slip, and $7.50 adds $3.",
                   value=x))
    x = F(84, 3)
    its.append(mcq("Priya reads 84 pages in 3 days. She reads the same number of pages each day. "
                   "How many pages does she read per day?", num(x), ["252", "81", "2.8"],
                   "84 ÷ 3 = <b>28</b> pages per day. 252 multiplies, 81 subtracts, and 2.8 is a decimal slip.", value=x))
    x = F(35, 2) / 5
    its.append(mcq(fig(model_svg([units_row("", 5, total="$17.50", ask_one=True)],
                                 label="bar model: 5 units make $17.50")) +
                   "5 cups of bubble tea cost $17.50. What is the cost of 1 cup?", money(x),
                   ["$87.50", "$12.50", "35¢"],
                   "5 units = $17.50, so 1 unit = $17.50 ÷ 5 = <b>$3.50</b>. $87.50 multiplies, $12.50 subtracts 5, "
                   "and 35¢ is a decimal slip.", value=x))
    x = F(56, 8)
    its.append(mcq("8 %s of paint can cover 56 m² of wall. What area can 1 %s of paint cover?" % (L_, L_),
                   num(x) + " m²", ["448 m²", "64 m²", "0.7 m²"],
                   "56 ÷ 8 = <b>7 m²</b> per litre. 448 m² multiplies, 64 m² adds, and 0.7 m² is a decimal slip.",
                   value=x))
    x = F(240, 20)
    its.append(mcq("Mr Tan’s car travels 240 km on 20 %s of petrol. How many kilometres does it travel per litre?" % L_,
                   num(x) + " km", ["4800 km", "220 km", "1.2 km"],
                   "Distance per litre = 240 ÷ 20 = <b>12 km</b>. 4800 km multiplies, 220 km subtracts, "
                   "and 1.2 km is a decimal slip.", value=x))
    x = F(150, 6)
    its.append(mcq("A hawker sells 150 plates of chicken rice in 6 hours. On average, how many plates does he sell per hour?",
                   num(x), ["900", "144", "2.5"],
                   "150 ÷ 6 = <b>25</b> plates per hour. 900 multiplies, 144 subtracts, and 2.5 is a decimal slip.",
                   value=x))
    x = F(18, 6)
    its.append(mcq(fig(table_svg(["Water (%s)" % L_, "Time (min)"], [[18, 36, 54], [2, 4, 6]],
                                 label="rate table of water and time")) +
                   "The table shows how much water flows from a tap. How many litres flow per minute?",
                   "9 " + L_, ["18 " + L_, "4.5 " + L_, "36 " + L_],
                   "Divide water by time in any column: 18 ÷ 2 = <b>9 %s</b> per minute. Check: 54 ÷ 6 = 9. "
                   "18 %s is the water in 2 min, 4.5 %s halves it again, and 36 %s doubles it." % (L_, L_, L_, L_),
                   value=9))
    x = F(18, 10)
    its.append(mcq(fig(table_svg(["Pens", "Cost"], [[2, 4, 6], ["$1.80", "$3.60", "$5.40"]],
                                 label="rate table of pens and cost")) +
                   "What is the cost of 1 pen?", money(x / 2), ["$1.80", "45¢", "$3.60"],
                   "2 pens cost $1.80, so 1 pen costs $1.80 ÷ 2 = <b>90¢</b>. $1.80 is the cost of 2 pens, "
                   "45¢ halves again, and $3.60 is the cost of 4 pens.", value=x / 2))
    x = F(3000, 60)
    its.append(mcq("A baker uses 3 kg of flour to make 60 buns. How many grams of flour are in each bun?",
                   "50 g", ["20 g", "180 g", "0.05 g"],
                   "3 kg = 3000 g. 3000 ÷ 60 = <b>50 g</b>. 20 g divides the wrong way (60 ÷ 3), "
                   "180 g multiplies, and 0.05 g forgets to change kg to g.", value=x))
    x = F(1800, 60)
    its.append(mcq("A machine prints 1800 pages per hour. How many pages does it print per minute?", num(x),
                   ["18", "1800", "108" + NBSP + "000"],
                   "1 h = 60 min, so 1800 ÷ 60 = <b>30</b> pages per minute. 18 uses 1 h = 100 min, 1800 forgets "
                   "to change hours to minutes, and 108 000 multiplies by 60 instead of dividing."
                   .replace("108 000", "108" + NBSP + "000"), value=x))
    x = F(12) * 60
    its.append(mcq("Nurul’s printer prints 12 pages per minute. How many pages is that per hour?", num(x),
                   ["72", "0.2", "1200"],
                   "There are 60 min in 1 h. 12 × 60 = <b>720</b> pages per hour. 72 is a decimal slip, 0.2 divides "
                   "by 60 instead of multiplying, and 1200 uses 1 h = 100 min.", value=x))
    x = F(4) * 2
    its.append(mcq("A hose lets out 4 %s of water every 30 seconds. How many litres is that per minute?" % L_,
                   "8 " + L_, ["2 " + L_, "120 " + L_, "7.5 " + L_],
                   "1 min = 60 s = 2 × 30 s, so 2 × 4 = <b>8 %s</b> per minute. 2 %s halves instead of doubling, "
                   "120 %s is 4 × 30, and 7.5 %s divides the wrong way (30 ÷ 4)." % (L_, L_, L_, L_), value=x))
    x = F(18) * 4
    its.append(mcq("Jun Jie counts 18 heartbeats in 15 seconds. What is his heart rate per minute?", num(x),
                   ["63", "270", "1.2"],
                   "1 min = 60 s = 4 × 15 s, so 4 × 18 = <b>72</b> beats per minute. 63 adds 45 because 15 + 45 = 60, "
                   "270 is 18 × 15, and 1.2 is beats per second.", value=x))
    x = F(520, 400) * 100
    assert F(520, 100) / 4 == F(13, 10)
    its.append(mcq("400 g of grapes cost $5.20. What is the cost per 100 g?", money(F(13, 10)),
                   ["$2.60", "13¢", "$20.80"],
                   "400 g = 4 × 100 g, so $5.20 ÷ 4 = <b>$1.30</b> per 100 g. $2.60 divides by 2, 13¢ is a decimal slip, "
                   "and $20.80 multiplies by 4.", value=F(13, 10)))
    x = F(750) / F(5, 2)
    its.append(mcq("A machine fills 750 bottles in 2 h 30 min. How many bottles does it fill per hour?", num(x),
                   ["375", "1875", "30"],
                   "2 h 30 min = 2.5 h. 750 ÷ 2.5 = <b>300</b> bottles per hour. 375 forgets the 30 min (750 ÷ 2), "
                   "1875 multiplies, and 30 is a decimal slip.", value=x))
    x = F(27) / F(3, 2)
    its.append(mcq("1 kg 500 g of prawns cost $27. What is the cost per kilogram?", money(x),
                   ["$27", "$40.50", "$13.50"],
                   "1 kg 500 g = 1.5 kg. $27 ÷ 1.5 = <b>$18</b> per kg. Check: $18 + $9 (half a kilogram) = $27. "
                   "$27 forgets the 500 g, $40.50 multiplies by 1.5, and $13.50 divides by 2.", value=x))
    x = F(1500) / 75
    its.append(mcq("A full tank has 1500 %s of water. It empties at a steady rate in 1 h 15 min. "
                   "How many litres flow out per minute?" % L_, num(x) + " " + L_,
                   ["25 " + L_, "100 " + L_, "1200 " + L_],
                   "1 h 15 min = 60 + 15 = 75 min. 1500 ÷ 75 = <b>20 %s</b> per minute. 25 %s forgets the 15 min, "
                   "100 %s divides by 15 only, and 1200 %s is the rate per hour (1500 ÷ 1.25)." % (L_, L_, L_, L_),
                   value=x))
    assert len(its) == 20
    return {"title": "Finding the rate per unit", "items": its}


# ============================================================ set 2: find the total
def set_total():
    its = []
    x = F(6) * 4
    its.append(mcq("1 kg of grapes costs $6. What is the cost of 4 kg?", money(x), ["$10", "$1.50", "$240"],
                   "Total = rate × number of units: $6 × 4 = <b>$24</b>. $10 adds, $1.50 divides, and $240 is a decimal slip.",
                   value=x))
    x = F(12) * 15
    its.append(mcq("A tap fills a tank at 12 %s per minute. How much water flows in 15 minutes?" % L_,
                   num(x) + " " + L_, ["27 " + L_, "0.8 " + L_, "1.25 " + L_],
                   "12 × 15 = <b>180 %s</b>. 27 %s adds, 0.8 %s divides 12 by 15, and 1.25 %s divides 15 by 12. "
                   "To find the total, multiply." % (L_, L_, L_, L_), value=x))
    x = F(35) * 8
    its.append(mcq("Siti types 35 words per minute. How many words can she type in 8 minutes?", num(x),
                   ["43", "245", "2800"],
                   "35 × 8 = <b>280</b> words. 43 adds, 245 is only 7 minutes (35 × 7), and 2800 is a decimal slip.",
                   value=x))
    x = F(12, 5) * 6
    its.append(mcq(fig(model_svg([units_row("1 set", 1, each="$2.40"),
                                  dict(units_row("6 sets", 6, ask_all=True), segs=[(1, "$2.40", True)] * 6)],
                                 label="bar model: 1 unit is $2.40, 6 units are unknown")) +
                   "A set of kaya toast costs $2.40. Mr Kumar buys 6 sets. How much does he pay?", money(x),
                   ["$8.40", "40¢", "$1.44"],
                   "1 unit = $2.40, so 6 units = 6 × $2.40 = <b>$14.40</b>. $8.40 adds 6, 40¢ divides, "
                   "and $1.44 is a decimal slip.", value=x))
    x = F(6) * 5
    its.append(mcq(fig(table_svg(["Hours", "Cost"], [[1, 2, 3, 5], ["$6", "$12", "$18", "?"]],
                                 label="rate table of hours and bicycle rental cost")) +
                   "A shop rents out bicycles. The table shows the cost. What is the cost for 5 hours?", money(x),
                   ["$24", "$20", "$36"],
                   "$6 per hour, so 5 × $6 = <b>$30</b>. $24 is the next column after 3 hours (4 hours), "
                   "$20 adds 2 because 3 + 2 = 5, and $36 is 6 hours.", value=x))
    x = F(180, 60) * 20
    its.append(mcq("A machine makes 180 cans per hour. How many cans does it make in 20 minutes?", num(x),
                   ["3600", "9", "160"],
                   "180 per hour is 180 ÷ 60 = 3 cans per minute. 3 × 20 = <b>60</b>. Or: 20 min is "
                   "%s h, and 180 ÷ 3 = 60. 3600 treats 180 as a rate per minute, 9 is 180 ÷ 20, and 160 subtracts." % fr(1, 3),
                   value=x))
    x = F(14) * 35
    its.append(mcq("A car travels 14 km on 1 %s of petrol. How far can it travel on 35 %s?" % (L_, L_),
                   num(x) + " km", ["2.5 km", "49 km", "21 km"],
                   "14 × 35 = <b>490 km</b>. 2.5 km divides 35 by 14, 49 km adds, and 21 km subtracts.", value=x))
    x = F(15) * F(6, 10)
    its.append(mcq("Fish costs $15 per kilogram. What is the cost of 600 g of fish?", money(x),
                   ["$90", "$25", "$1.50"],
                   "600 g = 0.6 kg. $15 × 0.6 = <b>$9</b>. $90 multiplies by 6 instead of 0.6, $25 divides by 0.6, "
                   "and $1.50 is the cost of 100 g.", value=x))
    x = F(3, 2) * 12
    its.append(mcq("A plant grows 1.5 cm per week. How much does it grow in 12 weeks?", num(x) + " cm",
                   ["13.5 cm", "8 cm", "180 cm"],
                   "1.5 × 12 = <b>18 cm</b>. 13.5 cm adds, 8 cm divides 12 by 1.5, and 180 cm is a decimal slip.",
                   value=x))
    x = F(17, 2) * 6
    its.append(mcq("1 %s of paint covers 8.5 m² of wall. How much wall can 6 %s of paint cover?" % (L_, L_),
                   num(x) + " m²", ["14.5 m²", "48 m²", "510 m²"],
                   "8.5 × 6 = <b>51 m²</b>. 14.5 m² adds, 48 m² forgets the 0.5 (8 × 6), and 510 m² is a decimal slip.",
                   value=x))
    x = F(300) * F(3, 4)
    its.append(mcq("A ceiling fan turns 300 times per minute. How many times does it turn in 45 seconds?", num(x),
                   ["13" + NBSP + "500", "400", "255"],
                   "45 s is %s of a minute. %s of 300 = <b>225</b>. 13 500 multiplies 300 by 45, 400 divides by %s, "
                   "and 255 subtracts 45.".replace("13 500", "13" + NBSP + "500") % (fr(3, 4), fr(3, 4), fr(3, 4)),
                   value=x))
    x = F(24) * F(7, 2)
    its.append(mcq("A printer prints 24 pages per minute. How many pages does it print in 3%s minutes?" % fr(1, 2),
                   num(x), ["72", "96", "27.5"],
                   "24 × 3 = 72 and 24 × %s = 12. 72 + 12 = <b>84</b>. 72 forgets the half minute, 96 rounds up to 4 min, "
                   "and 27.5 adds." % fr(1, 2), value=x))
    x = F(18, 2) * 5
    its.append(mcq("A stall sells durians at $18 for 2 kg. What is the cost of 5 kg?", money(x),
                   ["$90", "$21", "$36"],
                   "Find the rate first: $18 ÷ 2 = $9 per kg. Then 5 × $9 = <b>$45</b>. $90 multiplies $18 by 5, "
                   "$21 adds 3 because 2 + 3 = 5, and $36 is the cost of 4 kg.", value=x))
    x = F(3, 4) * 60
    its.append(mcq("A tap lets out 3 %s of water every 4 minutes. How much water flows out in 1 hour?" % L_,
                   num(x) + " " + L_, ["180 " + L_, "80 " + L_, "15 " + L_],
                   "1 h = 60 min = 15 × 4 min, so 15 × 3 = <b>45 %s</b>. 180 %s treats 3 %s as a rate per minute, "
                   "80 %s divides the wrong way (60 × 4 ÷ 3), and 15 %s is the number of 4-minute blocks."
                   % (L_, L_, L_, L_, L_), value=x))
    x = F(14) * F(15, 2)
    its.append(mcq("Mr Rahman earns $14 per hour. He works 7 h 30 min a day. How much does he earn in a day?",
                   money(x), ["$102.20", "$98", "$1050"],
                   "7 h 30 min = 7.5 h. $14 × 7.5 = <b>$105</b>. $102.20 reads 7 h 30 min as 7.3 h, $98 forgets the 30 min, "
                   "and $1050 is a decimal slip.", value=x))
    x = F(27, 3) * 15
    its.append(mcq(fig(table_svg(["Tickets", "Cost"], [[3, 6, 9, 15], ["$27", "$54", "$81", "?"]],
                                 label="rate table of tickets and cost")) +
                   "The table shows the cost of museum tickets for a class trip. What is the cost of 15 tickets?",
                   money(x), ["$108", "$99", "$405"],
                   "1 ticket costs $27 ÷ 3 = $9, so 15 × $9 = <b>$135</b>. $108 just continues the table by $27 "
                   "(that is 12 tickets), $99 adds $18 because 9 + 6 = 15, and $405 is 15 × $27.", value=x))
    x = F(250) * 12
    its.append(mcq("A water dispenser fills 250 ml every 10 seconds. How many litres does it fill in 2 minutes?",
                   "3 " + L_, ["0.5 " + L_, "30 " + L_, "1.5 " + L_],
                   "2 min = 120 s = 12 × 10 s. 12 × 250 ml = 3000 ml = <b>3 %s</b>. 0.5 %s uses 2 instead of 12, "
                   "30 %s is a decimal slip, and 1.5 %s is only 1 minute." % (L_, L_, L_, L_), value=x / 1000))
    x = F(45) * 80
    its.append(mcq("Arjun types 45 words per minute. How many words does he type in 1 h 20 min?", num(x),
                   ["2700", "3240", "900"],
                   "1 h 20 min = 80 min. 45 × 80 = <b>3600</b> words. 2700 forgets the 20 min, 3240 reads "
                   "1 h 20 min as 1.2 h (72 min), and 900 is only 20 min.", value=x))
    x = F(24) * F(9, 4)
    its.append(mcq("Prawns cost $24 per kilogram. Mrs Ng buys 2 kg 250 g. How much does she pay?", money(x),
                   ["$48", "$48.60", "$6"],
                   "2 kg 250 g = 2.25 kg. $24 × 2.25 = <b>$54</b> ($48 for 2 kg and $6 for 250 g). "
                   "$48 forgets the 250 g, $48.60 reads 2 kg 250 g as 2.025 kg, and $6 is only the 250 g.", value=x))
    x = F(25) * 120
    its.append(mcq("A leaking tap drips 25 ml of water per minute. How much water drips in 2 hours?",
                   num(x) + " ml", ["50 ml", "1500 ml", "5000 ml"],
                   "2 h = 120 min. 25 × 120 = <b>3000 ml</b> (3 %s). 50 ml treats 2 h as 2 min, 1500 ml is only 1 hour, "
                   "and 5000 ml uses 1 h = 100 min." % L_, value=x))
    assert len(its) == 20
    return {"title": "Finding the total amount", "items": its}


# ============================================================ set 3: find the number of units
def set_units():
    its = []
    x = F(600, 40)
    its.append(mcq("A pencil costs 40¢. How many pencils can Ali buy with exactly $6?", num(x),
                   ["240", "150", "1.5"],
                   "$6 = 600¢. 600 ÷ 40 = <b>15</b> pencils. 240 multiplies, 150 divides 600 by 4, "
                   "and 1.5 divides 6 by 4.", value=x))
    x = F(96, 8)
    its.append(mcq("A tap fills a tank at 8 %s per minute. The tank holds 96 %s. How long does it take to fill?" % (L_, L_),
                   num(x) + " min", ["768 min", "88 min", "9.6 min"],
                   "Number of minutes = total ÷ rate: 96 ÷ 8 = <b>12 min</b>. 768 min multiplies, 88 min subtracts, "
                   "and 9.6 min divides by 10.", value=x))
    x = F(600, 50)
    its.append(mcq("Hafiz types 50 words per minute. How long does he take to type a 600-word composition?",
                   num(x) + " min", ["30" + NBSP + "000 min", "550 min", "120 min"],
                   "600 ÷ 50 = <b>12 min</b>. 30 000 min multiplies, 550 min subtracts, and 120 min is a decimal slip."
                   .replace("30 000", "30" + NBSP + "000"), value=x))
    x = F(180, 12)
    its.append(mcq("A car uses 1 %s of petrol for every 12 km. How much petrol does it use for 180 km?" % L_,
                   num(x) + " " + L_, ["2160 " + L_, "168 " + L_, "1.5 " + L_],
                   "180 ÷ 12 = <b>15 %s</b>. 2160 %s multiplies, 168 %s subtracts, and 1.5 %s is a decimal slip."
                   % (L_, L_, L_, L_), value=x))
    x = F(1200, 30)
    its.append(mcq("A photocopier makes 30 copies per minute. How long does it take to make 1200 copies?",
                   num(x) + " min", ["36" + NBSP + "000 min", "1170 min", "4 min"],
                   "1200 ÷ 30 = <b>40 min</b>. 36 000 min multiplies, 1170 min subtracts, and 4 min drops a zero."
                   .replace("36 000", "36" + NBSP + "000"), value=x))
    x = F(252, 18)
    its.append(mcq("Hui Min reads 18 pages a day. Her book has 252 pages. How many days does she take to finish it?",
                   num(x), ["4536", "234", "140"],
                   "252 ÷ 18 = <b>14</b> days. 4536 multiplies, 234 subtracts, and 140 is a decimal slip.", value=x))
    x = F(9) / F(6, 5)
    its.append(mcq("Ribbon costs $1.20 per metre. Farah pays $9 for some ribbon. How many metres does she buy?",
                   num(x) + " m", ["10.8 m", "7.8 m", "0.75 m"],
                   "$9 ÷ $1.20 = 90 ÷ 12 = <b>7.5 m</b>. 10.8 m multiplies, 7.8 m subtracts, and 0.75 m is a decimal slip.",
                   value=x))
    x = F(1960, 280)
    its.append(mcq(fig(table_svg(["Litres", "Cost"], [[1, 2, "?"], ["$2.80", "$5.60", "$19.60"]],
                                 label="rate table of litres and cost")) +
                   "The table shows the cost of cooking oil. How many litres cost $19.60?", num(x),
                   ["3", "70", "54.88"],
                   "1 litre costs $2.80. $19.60 ÷ $2.80 = <b>7</b> litres. 3 just continues the top row (1, 2, 3), "
                   "70 is a decimal slip, and 54.88 multiplies $19.60 by 2.80.", value=x))
    x = F(45) / F(3, 2)
    its.append(mcq("A tank holds 45 %s of water. A tap fills it at 1 %s 500 ml per minute. How long does it take to fill "
                   "the empty tank?" % (L_, L_), num(x) + " min", ["45 min", "67.5 min", "3 min"],
                   "1 %s 500 ml = 1.5 %s. 45 ÷ 1.5 = <b>30 min</b>. 45 min ignores the 500 ml, 67.5 min multiplies, "
                   "and 3 min divides 45 by 15." % (L_, L_), value=x))
    x = F(1050, 42)
    its.append(mcq("Xin Yi types 42 words per minute. How long does she take to type 1050 words?", num(x) + " min",
                   ["44" + NBSP + "100 min", "1008 min", "2.5 min"],
                   "1050 ÷ 42 = <b>25 min</b>. 44 100 min multiplies, 1008 min subtracts, and 2.5 min is a decimal slip."
                   .replace("44 100", "44" + NBSP + "100"), value=x))
    x = F(20) / F(5, 2)
    its.append(mcq("A candle burns 2.5 cm per hour. The candle is 20 cm long. How many hours does it take to burn completely?",
                   num(x) + " h", ["50 h", "17.5 h", "0.125 h"],
                   "20 ÷ 2.5 = <b>8 h</b>. Check: 8 × 2.5 = 20. 50 h multiplies, 17.5 h subtracts, "
                   "and 0.125 h divides the wrong way (2.5 ÷ 20).", value=x))
    assert F(6) // F(4, 5) == 7
    its.append(mcq("A drink costs 80¢ at the school canteen. Ryan has $6. What is the greatest number of drinks he can buy?",
                   "7", ["8", "7.5", "4.8"],
                   "$6 ÷ 80¢ = 600 ÷ 80 = 7.5. He cannot buy half a drink, and 8 drinks cost $6.40, so the answer is "
                   "<b>7</b> (with 40¢ left). 4.8 multiplies 6 by 0.8.", value=7))
    assert -(-200 // 15) == 14
    its.append(mcq("A lift carries at most 15 people per trip. 200 people need to go up. What is the least number of trips?",
                   "14", ["13", "13.3", "3000"],
                   "200 ÷ 15 = 13 remainder 5. 13 trips take only 195 people, so the 5 people left need one more trip: "
                   "<b>14</b>. 13.3 is not a whole number of trips, and 3000 multiplies.", value=14))
    x = F(3000, 150)
    its.append(mcq("Mdm Wong cooks 150 g of rice for each bowl. How many bowls can she cook from a 3 kg bag?",
                   num(x), ["450", "2", "0.05"],
                   "3 kg = 3000 g. 3000 ÷ 150 = <b>20</b> bowls. 450 multiplies 3 by 150, 2 uses 3 kg = 300 g, "
                   "and 0.05 divides the wrong way.", value=x))
    x = F(300) / F(1200, 60)
    its.append(mcq("A printer prints 1200 pages per hour. How many minutes does it take to print 300 pages?",
                   num(x) + " min", ["0.25 min", "4 min", "25 min"],
                   "1200 per hour = 1200 ÷ 60 = 20 pages per minute. 300 ÷ 20 = <b>15 min</b>. "
                   "0.25 min is 300 ÷ 1200 (that answer is in hours: %s h = 15 min), 4 min divides the wrong way, "
                   "and 25 min divides 300 by 12." % fr(1, 4), value=x))
    x = F(28, 4) * 3
    its.append(mcq("A tap fills a pail with 4 %s of water every 3 minutes. How long does it take to fill a 28 %s tub?" % (L_, L_),
                   num(x) + " min", ["7 min", "84 min", "31 min"],
                   "28 %s = 7 × 4 %s, so it takes 7 × 3 = <b>21 min</b>. 7 min forgets that each 4 %s takes 3 minutes, "
                   "84 min is 28 × 3, and 31 min adds." % (L_, L_, L_), value=x))
    its.append(mcq("An oven bakes 48 buns every 20 minutes. How long does it take to bake 240 buns?",
                   "1 h 40 min", ["5 min", "12 min", "1 h 4 min"],
                   "240 ÷ 48 = 5 batches. 5 × 20 min = 100 min = <b>1 h 40 min</b>. 5 min forgets to multiply by 20 min, "
                   "12 min is 240 ÷ 20, and 1 h 4 min reads 100 min as 1.04 h."))
    assert F(9) / F(12, 5) == F(15, 4)
    its.append(mcq("Potatoes cost $2.40 per kilogram. Mrs Lim spends $9 on potatoes. What mass of potatoes does she buy?",
                   "3 kg 750 g", ["3 kg 75 g", "21 kg 600 g", "6 kg 600 g"],
                   "$9 ÷ $2.40 = 3.75 kg = <b>3 kg 750 g</b>. 3 kg 75 g writes 0.75 kg as 75 g (it is 750 g), "
                   "21 kg 600 g multiplies, and 6 kg 600 g subtracts."))
    assert F(360, 6) * 5 == 300
    its.append(mcq("A machine seals 6 packets every 5 seconds. How long does it take to seal 360 packets?",
                   "5 min", ["1 min", "7 min 12 s", "3 min"],
                   "360 ÷ 6 = 60 groups. 60 × 5 s = 300 s = <b>5 min</b>. 1 min uses 60 s and forgets the 5 s per group, "
                   "7 min 12 s divides the wrong way (360 × 6 ÷ 5 = 432 s), and 3 min uses 100 s = 1 min."))
    x = F(135, 2) / F(15, 2)
    its.append(mcq(fig(table_svg(["Hours", "Cost"], [[2, 4, "?"], ["$15", "$30", "$67.50"]],
                                 label="rate table of hours and cost")) +
                   "The table shows the cost of hiring a kayak. For how many hours can Ethan hire it with $67.50?",
                   num(x), ["6", "4.5", "135"],
                   "1 hour costs $15 ÷ 2 = $7.50. $67.50 ÷ $7.50 = <b>9</b> hours. 6 just continues the top row, "
                   "4.5 divides by $15 (the cost of 2 hours), and 135 multiplies $67.50 by 2.", value=x))
    assert len(its) == 20
    return {"title": "Finding the number of units", "items": its}


# ============================================================ set 4: rate tables and best buys
def set_best():
    its = []
    a, b = F(5, 2), F(72, 30)
    assert b < a
    its.append(mcq("Which is cheaper per kilogram: 2 kg of sugar for $5 or 3 kg of sugar for $7.20?",
                   "3 kg for $7.20", ["2 kg for $5", SAME, CANT],
                   "Cost per kg: $5 ÷ 2 = $2.50 and $7.20 ÷ 3 = $2.40. <b>3 kg for $7.20</b> is cheaper per kilogram, "
                   "even though it costs more in total."))
    x = F(12) * 3
    its.append(mcq(fig(table_svg(["Hours", "Water (%s)" % L_], [[1, 3, 5], [12, "?", 60]],
                                 label="rate table of hours and water")) +
                   "A pump moves water at a steady rate. Find the missing number.", num(x),
                   ["24", "14", "30"],
                   "12 %s per hour, so 3 hours give 3 × 12 = <b>36</b>. Check: 5 × 12 = 60. 24 doubles instead of tripling, "
                   "14 adds 2 because 1 + 2 = 3, and 30 is half of 60 (3 is not half of 5)." % L_, value=x))
    x = F(7, 2) * 8
    its.append(mcq(fig(table_svg(["Mass (kg)", "Cost"], [[2, 5, 8], ["$7", "$17.50", "?"]],
                                 label="rate table of mass and cost")) +
                   "The table shows the cost of mandarin oranges. What is the cost of 8 kg?", money(x),
                   ["$24.50", "$20.50", "$56"],
                   "$7 ÷ 2 = $3.50 per kg. 8 × $3.50 = <b>$28</b>. $24.50 adds $7 to $17.50, $20.50 adds $3 because "
                   "5 + 3 = 8, and $56 is 8 × $7.", value=x))
    a, b = F(180, 4), F(220, 5)
    assert a > b
    its.append(mcq("Wei Ming types 180 words in 4 minutes. Chloe types 220 words in 5 minutes. Who types faster?",
                   "Wei Ming", ["Chloe", SAME, CANT],
                   "Words per minute: Wei Ming 180 ÷ 4 = 45 and Chloe 220 ÷ 5 = 44. <b>Wei Ming</b> is faster, "
                   "even though Chloe types more words in all."))
    a, b = F(54, 6), F(40, 4)
    assert b > a
    its.append(mcq("Tap A fills 54 %s in 6 minutes. Tap B fills 40 %s in 4 minutes. Which tap fills faster?" % (L_, L_),
                   "Tap B", ["Tap A", SAME, CANT],
                   "Litres per minute: Tap A 54 ÷ 6 = 9 %s and Tap B 40 ÷ 4 = 10 %s. <b>Tap B</b> is faster, "
                   "although Tap A lets out more water in all." % (L_, L_)))
    a, b = F(240, 3), F(380, 5)
    assert b < a
    its.append(mcq("Shop A sells 3 pens for $2.40. Shop B sells 5 pens of the same kind for $3.80. Which shop is cheaper per pen?",
                   "Shop B", ["Shop A", SAME, CANT],
                   "Cost per pen: Shop A $2.40 ÷ 3 = 80¢ and Shop B $3.80 ÷ 5 = 76¢. <b>Shop B</b> is cheaper per pen."))
    a, b = F(45, 3), F(32, 2)
    assert b > a
    its.append(mcq("Ahmad earns $45 for 3 hours of work. Kavya earns $32 for 2 hours of work. Who earns more per hour?",
                   "Kavya", ["Ahmad", SAME, CANT],
                   "Ahmad: $45 ÷ 3 = $15 per hour. Kavya: $32 ÷ 2 = $16 per hour. <b>Kavya</b> earns more per hour, "
                   "even though Ahmad earns more in all."))
    assert F(12) * 60 > 600
    its.append(mcq("Machine A makes 600 cups per hour. Machine B makes 12 cups per minute. Which machine is faster?",
                   "Machine B", ["Machine A", SAME, CANT],
                   "Use the same unit of time. Machine B makes 12 × 60 = 720 cups per hour, which is more than 600. "
                   "<b>Machine B</b> is faster. Comparing 600 with 12 mixes per hour and per minute."))
    x = F(13, 2) * 7
    its.append(mcq(fig(table_svg(["Tickets", "Cost"], [[4, 7], ["$26", "?"]],
                                 label="rate table of tickets and cost")) +
                   "The table shows the cost of tickets to a school concert. What is the cost of 7 tickets?",
                   money(x), ["$29", "$182", "$6.50"],
                   "1 ticket costs $26 ÷ 4 = $6.50. 7 × $6.50 = <b>$45.50</b>. $29 adds $3 because 4 + 3 = 7, "
                   "$182 is 7 × $26, and $6.50 is the cost of only 1 ticket.", value=x))
    eggs = [(6, F(18, 10)), (10, F(28, 10)), (30, F(87, 10))]
    u = [c / n for n, c in eggs]
    assert min(u) == u[1] and len(set(u)) == 3
    its.append(mcq("Which tray of eggs is the best buy?", "10 eggs for $2.80",
                   ["6 eggs for $1.80", "30 eggs for $8.70", SAME],
                   "Cost per egg: %s, %s and %s. The lowest is <b>10 eggs for $2.80</b>. The biggest tray is not always "
                   "the best buy." % tuple(money(v) for v in u)))
    a, b = F(450, 375) * 100, F(580, 500) * 100
    assert b < a
    its.append(mcq("A 375 g box of cereal costs $4.50. A 500 g box of the same cereal costs $5.80. Which is the better buy?",
                   "The 500 g box", ["The 375 g box", SAME, CANT],
                   "Cost per 100 g: $4.50 ÷ 3.75 = $1.20 and $5.80 ÷ 5 = $1.16. <b>The 500 g box</b> is the better buy."))
    x = F(40, 5) * 60
    its.append(mcq(fig(table_svg(["Time (min)", "Water (%s)" % L_], [[5, 10, 15], [40, 80, 120]],
                                 label="rate table of time and water")) +
                   "A sprinkler uses water at the rate shown. How much water does it use in 1 hour?",
                   num(x) + " " + L_, ["8 " + L_, "160 " + L_, "2400 " + L_],
                   "Rate: 40 ÷ 5 = 8 %s per minute. 1 h = 60 min, so 8 × 60 = <b>480 %s</b>. 8 %s is only the rate per minute, "
                   "160 %s is 20 min, and 2400 %s multiplies 40 by 60." % (L_, L_, L_, L_, L_), value=x))
    milk = [(F(1), F(32, 10)), (F(2), F(6)), (F(1, 2), F(17, 10))]
    u = [c / v for v, c in milk]
    assert min(u) == u[1] and len(set(u)) == 3
    its.append(mcq("Which bottle of milk is the best buy?", "2 %s for $6" % L_,
                   ["1 %s for $3.20" % L_, "500 ml for $1.70", SAME],
                   "Cost per litre: 1 %s costs $3.20; 2 %s cost $6, so $3 per litre; 500 ml is half a litre, so "
                   "$1.70 × 2 = $3.40 per litre. <b>2 %s for $6</b> is the best buy. 500 ml costs the least in all, "
                   "but the most per litre." % (L_, L_, L_)))
    its.append(mcq("Which rate is the same as $1.50 per 100 g?", "$15 per kg",
                   ["$1.50 per kg", "$150 per kg", "15¢ per kg"],
                   "1 kg = 1000 g = 10 × 100 g, so $1.50 × 10 = <b>$15 per kg</b>. $1.50 per kg forgets to convert, "
                   "$150 multiplies by 100, and 15¢ divides by 10."))
    its.append(mcq("Which rate is the same as 3 %s per minute?" % L_, "180 %s per hour" % L_,
                   ["30 %s per hour" % L_, "0.05 %s per hour" % L_, "300 %s per hour" % L_],
                   "In 1 hour there are 60 minutes, so 3 × 60 = <b>180 %s per hour</b>. 30 %s multiplies by 10, "
                   "0.05 %s divides by 60 instead of multiplying, and 300 %s uses 1 h = 100 min." % (L_, L_, L_, L_)))
    x = F(90, 2) * 7
    its.append(mcq(fig(table_svg(["Time (min)", "Words"], [[2, 5, 7], [90, 225, "?"]],
                                 label="rate table of time and words typed")) +
                   "Kumar types at a steady rate. How many words does he type in 7 minutes?", num(x),
                   ["227", "1575", "270"],
                   "90 ÷ 2 = 45 words per minute. 7 × 45 = <b>315</b>. 227 adds 2 because 5 + 2 = 7, "
                   "1575 is 225 × 7, and 270 is only 6 minutes.", value=x))
    x = F(560, 200) - F(750, 300)
    its.append(mcq("Brand A sells 2 %s of juice for $5.60. Brand B sells 3 %s for $7.50. How much cheaper per litre is Brand B?"
                   % (L_, L_), money(x), ["$1.90", "$2.50", "$2.80"],
                   "Brand A: $5.60 ÷ 2 = $2.80 per litre. Brand B: $7.50 ÷ 3 = $2.50 per litre. $2.80 − $2.50 = <b>30¢</b>. "
                   "$1.90 compares the total prices, and $2.50 and $2.80 are the two rates.", value=x))
    x = F(12, 10) * 4
    its.append(mcq(fig(table_svg(["Mass (g)", "Cost"], [[100, 250, 400], ["$1.20", "$3", "?"]],
                                 label="rate table of mass and cost")) +
                   "The table shows the cost of nuts sold by mass. What is the cost of 400 g?", money(x),
                   ["$4.20", "$6", "$48"],
                   "$1.20 per 100 g, and 400 g = 4 × 100 g, so 4 × $1.20 = <b>$4.80</b>. $4.20 adds $1.20 to $3 "
                   "(as if the next column were 350 g), $6 doubles $3 (400 g is not 2 × 250 g), and $48 is a decimal slip.",
                   value=x))
    juice = [(F(1, 4), F(11, 10)), (F(1), F(38, 10)), (F(3, 2), F(585, 100))]
    u = [c / v for v, c in juice]
    assert min(u) == u[1] and len(set(u)) == 3
    its.append(mcq("Which carton of orange juice is the best buy?", "1 %s for $3.80" % L_,
                   ["250 ml for $1.10", "1.5 %s for $5.85" % L_, SAME],
                   "Cost per litre: 250 ml × 4 = 1 %s, so $1.10 × 4 = $4.40; 1 %s costs $3.80; and $5.85 ÷ 1.5 = $3.90. "
                   "<b>1 %s for $3.80</b> is the best buy." % (L_, L_, L_)))
    rice = [(5, F(1150, 100)), (1, F(5, 2)), (2, F(47, 10)), (10, F(24))]
    u = [c / n for n, c in rice]
    assert min(u) == u[0] and len(set(u)) == 4
    its.append(mcq("Which bag of rice is the best buy?", "5 kg for $11.50",
                   ["1 kg for $2.50", "2 kg for $4.70", "10 kg for $24"],
                   "Cost per kg: %s, %s, %s and %s. The lowest is <b>5 kg for $11.50</b>. The 10 kg bag is bigger, "
                   "but it costs more per kilogram." % tuple(money(v) for v in u)))
    assert len(its) == 20
    return {"title": "Rate tables and best buys", "items": its}


# ============================================================ set 5: word problems
def set_problems():
    its = []
    x = F(15, 2) / 3 * 7
    its.append(mcq(fig(model_svg([units_row("3 kg", 3, total="$7.50"),
                                  units_row("7 kg", 7, ask_all=True)],
                                 label="bar model: 3 units are $7.50, 7 units are unknown")) +
                   "3 kg of rambutans cost $7.50. How much do 7 kg of rambutans cost?", money(x),
                   ["$11.50", "$52.50", "$2.50"],
                   "3 units = $7.50, so 1 unit = $7.50 ÷ 3 = $2.50. 7 units = 7 × $2.50 = <b>$17.50</b>. "
                   "$11.50 adds $4 because 3 + 4 = 7, $52.50 is 7 × $7.50, and $2.50 is only 1 kg.", value=x))
    x = F(840, 7) * 3
    its.append(mcq(fig(model_svg([units_row("7 h", 7, total="840 packets"),
                                  units_row("3 h", 3, ask_all=True)],
                                 label="bar model: 7 units are 840 packets, 3 units are unknown")) +
                   "A machine packs 840 packets of biscuits in 7 hours. How many packets does it pack in 3 hours?",
                   num(x), ["836", "1960", "280"],
                   "7 units = 840, so 1 unit = 840 ÷ 7 = 120. 3 units = 3 × 120 = <b>360</b>. 836 subtracts 4, "
                   "1960 divides the wrong way (840 × 7 ÷ 3), and 280 is 840 ÷ 3.", value=x))
    x = F(12, 3) * 8
    its.append(mcq(fig(model_svg([units_row("3 pages", 3, total="12 min"),
                                  units_row("8 pages", 8, ask_all=True)],
                                 label="bar model: 3 units are 12 min, 8 units are unknown")) +
                   "Siti types 3 pages of her project in 12 minutes. At the same rate, how long does she take to type 8 pages?",
                   num(x) + " min", ["17 min", "96 min", "4 min"],
                   "3 units = 12 min, so 1 unit = 4 min. 8 units = 8 × 4 = <b>32 min</b>. 17 min adds 5 because 3 + 5 = 8, "
                   "96 min is 12 × 8, and 4 min is only 1 page.", value=x))
    x = F(21, 7) * 4
    its.append(mcq("4 bottles of soya bean milk cost $7. How many bottles can Raju buy with $21?", num(x),
                   ["3", "84", "5"],
                   "$21 = 3 × $7, so he can buy 3 × 4 = <b>12</b> bottles. 3 is the number of $7 groups, "
                   "84 is 21 × 4, and 5 divides $21 by 4 and rounds.", value=x))
    x = F(45) * 35
    its.append(mcq("Kavya types 45 words per minute. She types for 20 minutes, rests for 5 minutes, then types for "
                   "15 more minutes. How many words does she type?", num(x), ["1800", "900", "675"],
                   "She types for 20 + 15 = 35 min. 45 × 35 = <b>1575</b> words. 1800 counts the 5-minute rest too, "
                   "900 is only the first 20 min, and 675 is only the last 15 min.", value=x))
    x = F(240 - 60, 15)
    its.append(mcq(fig(model_svg([{"name": "", "segs": [(60, "60 " + L_, True), (180, "?", False)],
                                   "over": [(0, 240, "240 " + L_)]}],
                                 label="bar model: a 240 litre tank with 60 litres in it")) +
                   "A tank holds 240 %s when full. It already has 60 %s of water. A tap fills it at 15 %s per minute. "
                   "How long does the tap take to fill the tank?" % (L_, L_, L_), num(x) + " min",
                   ["16 min", "4 min", "20 min"],
                   "Water still needed: 240 − 60 = 180 %s. 180 ÷ 15 = <b>12 min</b>. 16 min fills the whole 240 %s, "
                   "4 min is only the 60 %s, and 20 min adds 60 %s to 240 %s." % (L_, L_, L_, L_, L_), value=x))
    x = F(150, 20 - 5)
    its.append(mcq("An empty tank holds 150 %s. A tap fills it at 20 %s per minute, but a hole lets out 5 %s per minute. "
                   "How long does the tank take to fill?" % (L_, L_, L_), num(x) + " min",
                   ["6 min", "7.5 min", "30 min"],
                   "Each minute the tank gains 20 − 5 = 15 %s. 150 ÷ 15 = <b>10 min</b>. 6 min adds the rates (25 %s), "
                   "7.5 min ignores the hole, and 30 min uses only the hole (150 ÷ 5)." % (L_, L_), value=x))
    x = F(600) * 3 / 4 / 25
    its.append(mcq(fig(model_svg([{"name": "", "segs": [(1, "", True), (1, "", True), (1, "", True), (1, "", False)],
                                   "over": [(0, 4, "600 " + L_)], "under": [(0, 3, "?")]}],
                                 label="bar model: a 600 litre tank in 4 units, 3 units shaded")) +
                   "A tank holds 600 %s when full. It is %s full. Water drains out at 25 %s per minute. "
                   "How long does it take to empty the tank?" % (L_, fr(3, 4), L_), num(x) + " min",
                   ["24 min", "6 min", "32 min"],
                   "4 units = 600 %s, so 1 unit = 150 %s and 3 units = 450 %s. 450 ÷ 25 = <b>18 min</b>. "
                   "24 min drains a full tank, 6 min drains only %s, and 32 min divides by %s instead of multiplying."
                   % (L_, L_, L_, fr(1, 4), fr(3, 4)), value=x))
    x = 4 + F(30, 100) * ((5 - 1) * 1000 // 400)
    assert (5 - 1) * 1000 % 400 == 0
    its.append(mcq("A taxi charges $4 for the first 1 km and 30¢ for every 400 m after that. "
                   "What is the fare for a 5 km ride?", money(x), ["$7.60", "$3", "$5.20"],
                   "After the first 1 km there are 4 km = 4000 m. 4000 ÷ 400 = 10, so 10 × 30¢ = $3. "
                   "$4 + $3 = <b>$7</b>. $7.60 charges the first 1 km again (5000 ÷ 400 = 12.5, so 12 × 30¢), "
                   "$3 forgets the $4, and $5.20 charges 30¢ per km.", value=x))
    x = F(3, 2) + F(1, 2) * 5
    its.append(mcq("A car park charges $1.50 for the first hour and 50¢ for every half hour after that. "
                   "Mrs Lim parks from 9.30 am to 1.00 pm. How much does she pay?", money(x),
                   ["$3.50", "$5", "$2.75"],
                   "9.30 am to 1.00 pm is 3 h 30 min. After the first hour there are 2 h 30 min = 5 half hours. "
                   "$1.50 + 5 × 50¢ = <b>$4</b>. $3.50 charges every half hour at 50¢, $5 charges 7 half hours after "
                   "the first hour, and $2.75 charges 50¢ per hour.", value=x))
    x = 100 - (F(18) * F(5, 2) + F(15) * F(6, 5))
    its.append(mcq("Prawns cost $18 per kg and fish costs $15 per kg. Mrs Ng buys 2.5 kg of prawns and 1.2 kg of fish. "
                   "She pays with a $100 note. How much change does she get?", money(x),
                   ["$63", "$67", "$46"],
                   "Prawns: 2.5 × $18 = $45. Fish: 1.2 × $15 = $18. Total $45 + $18 = $63. $100 − $63 = <b>$37</b>. "
                   "$63 is the cost, not the change, $67 is $100 − $33 (one kilogram of each), and $46 uses 2 kg of prawns.",
                   value=x))
    x = F(36) * F(7, 2) * 4
    its.append(mcq("A hawker sells about 36 plates of chicken rice per hour from 11.00 am to 2.30 pm. "
                   "Each plate costs $4. How much money does he collect?", money(x),
                   ["$432", "$576", "$126"],
                   "11.00 am to 2.30 pm is 3 h 30 min = 3.5 h. 36 × 3.5 = 126 plates. 126 × $4 = <b>$504</b>. "
                   "$432 counts only 3 h, $576 counts 4 h, and $126 is the number of plates, not the money.", value=x))
    x = 120 * 2 + 3 * 120
    its.append(mcq("Machine A fills 120 bottles per hour. Machine B fills 3 bottles per minute. "
                   "Both machines work for 2 hours. How many bottles do they fill altogether?", num(x),
                   ["246", "480", "360"],
                   "Machine A: 120 × 2 = 240. Machine B: 2 h = 120 min, so 3 × 120 = 360. 240 + 360 = <b>600</b>. "
                   "246 treats 3 bottles per minute as 3 per hour, 480 treats both machines as 120 per hour, "
                   "and 360 is Machine B only.", value=x))
    its.append(mcq("A printer prints 20 pages per minute. It starts at 2.45 pm and prints 1500 pages. At what time does it finish?",
                   "4.00 pm", ["3.20 pm", "3.00 pm", "3.45 pm"],
                   "1500 ÷ 20 = 75 min = 1 h 15 min. 2.45 pm + 1 h 15 min = <b>4.00 pm</b>. 3.20 pm adds 75 min as if it "
                   "were 0.75 h, 3.00 pm adds only 15 min, and 3.45 pm adds only 1 h."))
    x = F(1800, 40 + 35)
    its.append(mcq("Ali types 40 words per minute and Mei Ling types 35 words per minute. They share the typing of an "
                   "1800-word report. If they type at the same time, how long do they take?", num(x) + " min",
                   ["45 min", "12 min", "360 min"],
                   "Together they type 40 + 35 = 75 words per minute. 1800 ÷ 75 = <b>24 min</b>. 45 min is Ali alone, "
                   "12 min halves 24 min again, and 360 min uses the difference 40 − 35 = 5.", value=x))
    x = F(1260) / (F(1260, 28) + 15)
    its.append(mcq("Jun Jie typed a 1260-word essay in 28 minutes. Xin Yi types 15 words per minute faster than Jun Jie. "
                   "How long would Xin Yi take to type the same essay?", num(x) + " min",
                   ["13 min", "84 min", "43 min"],
                   "Jun Jie: 1260 ÷ 28 = 45 words per minute. Xin Yi: 45 + 15 = 60 words per minute. "
                   "1260 ÷ 60 = <b>21 min</b>. 13 min subtracts 15 from 28, 84 min is 1260 ÷ 15, and 43 min adds 15 to 28.",
                   value=x))
    km = (F(10) - 4) / F(30, 100) * F(4, 10) + 1
    its.append(mcq("The same taxi charges $4 for the first 1 km and 30¢ for every 400 m after that. Sarah’s fare is $10. "
                   "How long is her ride?", num(km) + " km", ["8 km", "21 km", "6 km"],
                   "$10 − $4 = $6 for the distance after 1 km. $6 ÷ 30¢ = 20 lots of 400 m = 8000 m = 8 km. "
                   "8 km + 1 km = <b>9 km</b>. 8 km forgets the first 1 km, 21 km treats each 30¢ as 1 km, and 6 km "
                   "charges $1 per km.", value=km))
    x = F(12, 10) * 8 * 30 * F(30, 100)
    its.append(mcq("An air-conditioner uses 1.2 units of electricity per hour. Each unit costs 30¢. The air-conditioner "
                   "is on for 8 hours a night for 30 nights. How much does the electricity cost?", money(x),
                   ["$2.88", "$10.80", "$864"],
                   "Units used: 1.2 × 8 × 30 = 288 units. Cost: 288 × 30¢ = <b>$86.40</b>. $2.88 is only 1 night, "
                   "$10.80 forgets the 8 hours, and $864 is a decimal slip.", value=x))
    vol = 50 * 40 * 30
    x = F(vol, 1000) / 4
    its.append(mcq("An empty tank is a cuboid 50 cm long, 40 cm wide and 30 cm high. A tap fills it at 4 %s per minute. "
                   "How long does it take to fill the tank completely?" % L_, num(x) + " min",
                   ["15" + NBSP + "000 min", "1.5 min", "240 min"],
                   "Volume = 50 × 40 × 30 = 60 000 cm³ = 60 %s (1 %s = 1000 cm³). 60 ÷ 4 = <b>15 min</b>. "
                   "15 000 min forgets to change cm³ to litres, 1.5 min is a decimal slip, and 240 min multiplies 60 by 4."
                   .replace("60 000", "60" + NBSP + "000").replace("15 000", "15" + NBSP + "000") % (L_, L_), value=x))
    x = F(6 * 10 * 1000, 60 * 50)
    its.append(mcq("An empty cuboid tank has a base 60 cm by 50 cm. Water flows in at 6 %s per minute. "
                   "What is the height of the water after 10 minutes?" % L_, num(x) + " cm",
                   ["2 cm", "200 cm", "30 cm"],
                   "Water in 10 min: 6 × 10 = 60 %s = 60 000 cm³. Base area = 60 × 50 = 3000 cm². "
                   "Height = 60 000 ÷ 3000 = <b>20 cm</b>. 2 cm uses 60 %s = 6000 cm³, 200 cm is a decimal slip, "
                   "and 30 cm divides by 2000 cm² (a wrong base)."
                   .replace("60 000", "60" + NBSP + "000") % (L_, L_), value=x))
    assert len(its) == 20
    return {"title": "Word problems: taxi fares, tanks and typing", "items": its}


# ============================================================ lesson
def table(head, rows):
    h = "".join("<th>%s</th>" % x for x in head)
    b = "".join("<tr>" + "".join("<td>%s</td>" % c for c in r) + "</tr>" for r in rows)
    return "<div class='sn-tw'><table class='sn-table'><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>" % (h, b)


def ex(title, q, s, a):
    return ("<div class='sn-ex'><span class='sn-ex-t'>%s</span><p class='sn-ex-q'>%s</p>"
            "<p class='sn-ex-s'>%s</p><p class='sn-ex-a'>Answer: %s</p></div>" % (title, q, s, a))


def body_html():
    f_model = model_svg([units_row("4 kg", 4, total="$10", ask_one=True)], label="bar model: 4 units make $10")
    f_model2 = model_svg([units_row("3 kg", 3, total="$7.50"), units_row("7 kg", 7, ask_all=True)],
                         label="bar model: 3 units are $7.50, 7 units are unknown")
    f_tab = table_svg(["Time (min)", "Water (%s)" % L_], [[1, 2, 3, 10], [12, 24, 36, "?"]],
                      label="rate table of time and water")
    return (
        "<h2>What is a rate?</h2>"
        "<p>A <b>rate</b> tells you how much of one quantity there is for <b>1 unit</b> of another quantity. "
        "$2.50 per kg, 40 words per minute and 12 %s per minute are all rates.</p>"
        "<p>There are three things in every rate problem: the rate, the number of units and the total. "
        "If you know two of them, you can find the third.</p>" % L_
        + table(["To find", "Do this", "Example"], [
            ["the rate", "total ÷ number of units", "$10 for 4 kg: $10 ÷ 4 = $2.50 per kg"],
            ["the total", "rate × number of units", "$2.50 per kg for 6 kg: 6 × $2.50 = $15"],
            ["the number of units", "total ÷ rate", "$15 at $2.50 per kg: 15 ÷ 2.50 = 6 kg"],
        ])
        + "<figure class='sn-fig'>" + f_model +
        "<figcaption>4 kg of rice cost $10. 4 units = $10, so 1 unit = $10 ÷ 4 = $2.50. The rate is $2.50 per kg."
        "</figcaption></figure>"
        + ex("Find the total", "3 kg of rambutans cost $7.50. How much do 7 kg cost?",
             "3 units = $7.50, so 1 unit = $2.50. 7 units = 7 × $2.50.", "$17.50")
        + "<figure class='sn-fig'>" + f_model2 +
        "<figcaption>Draw the units for both amounts. Find 1 unit first, then multiply.</figcaption></figure>"
        + "<h2>Rate tables</h2>"
        "<p>In a rate table every column has the same rate. Multiply or divide both rows by the same number. "
        "Do not just add the same amount.</p>"
        + "<figure class='sn-fig'>" + f_tab +
        "<figcaption>12 %s per minute. In 10 minutes: 10 × 12 = 120 %s.</figcaption></figure>" % (L_, L_)
        + ex("Find the number of units", "A tap fills a 96 %s tank at 8 %s per minute. How long does it take?" % (L_, L_),
             "Number of minutes = total ÷ rate = 96 ÷ 8.", "12 min")
        + ex("Per hour and per minute", "A machine prints 1800 pages per hour. How many pages per minute?",
             "1 h = 60 min, so 1800 ÷ 60.", "30 pages per minute")
        + ex("Best buy", "Which is cheaper: 2 kg for $5 or 3 kg for $7.20?",
             "Find the cost of 1 kg each: $5 ÷ 2 = $2.50 and $7.20 ÷ 3 = $2.40.", "3 kg for $7.20")
        + "<h2>Common mistakes</h2>"
        + table(["Mistake", "What to do instead"], [
            ["Dividing the wrong way: $10 for 4 kg, so 4 ÷ 10 = 40¢ per kg",
             "Divide the quantity you want “per” 1 of: dollars ÷ kilograms = $2.50 per kg"],
            ["Multiplying when you should divide: 96 %s at 8 %s per minute, so 96 × 8" % (L_, L_),
             "To find how many units, divide the total by the rate: 96 ÷ 8 = 12 min"],
            ["Adding instead of multiplying: 3 kg cost $7.50, so 7 kg cost $7.50 + $4",
             "Find 1 unit first: $7.50 ÷ 3 = $2.50, then 7 × $2.50 = $17.50"],
            ["Mixing per hour and per minute: 600 cups per hour is less than 12 cups per minute?",
             "Change to the same unit of time: 12 × 60 = 720 cups per hour"],
            ["Reading 1 h 30 min as 1.3 h", "30 min is half an hour, so 1 h 30 min = 1.5 h"],
        ])
    )


FAQ = [
    {"q": "What is rate in Primary 5 maths?",
     "a": "Rate is the amount of one quantity for 1 unit of another quantity, such as $2.50 per kg or 12 ℓ per minute. In P5, students find the rate, the total amount or the number of units when the other two are given."},
    {"q": "How do I explain rate to my child?",
     "a": "Use the bar model: if 4 kg cost $10, then 4 units = $10 and 1 unit = $2.50. Once your child knows the value of 1 unit, finding any other amount is just multiplying or dividing."},
    {"q": "What is the most common mistake in rate questions?",
     "a": "Dividing the wrong way or mixing units. $10 for 4 kg is $10 ÷ 4 = $2.50 per kg, not 4 ÷ 10, and 600 cups per hour must be changed to 10 cups per minute before you compare it with a rate per minute."},
    {"q": "Is rate in the MOE Primary 5 syllabus?",
     "a": "Yes. Rate is a Primary 5 topic in the Number and Algebra strand of the MOE 2021 Primary Mathematics syllabus. Finding the value of 1 unit is used again in Primary 6 ratio and percentage problems and in the PSLE."},
]


def mark_large(u, pattern):
    """Tag wide pictures so they print larger and stay readable."""
    rx = re.compile(r"<svg (?=[^>]*aria-label='" + pattern + ")")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u


def gen():
    rnd = random.Random(65810)
    sets = [set_rate(), set_total(), set_units(), set_best(), set_problems()]
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
        "country": "sg", "subject": "maths", "grade": "primary-5", "slug": SLUG, "sort": 10,
        "updated": UPDATED, "pdf_url": "",
        "title": "Primary 5 Rate",
        "seo_title": "P5 Rate Worksheets: Free Primary 5 Maths with Answers (MOE Syllabus)",
        "short_title": "Rate",
        "domain": "Number and Algebra",
        "standard_code": "Primary 5: Rate",
        "standard_url": "https://www.moe.gov.sg/primary/curriculum/syllabus",
        "standard_text": "Rate as the amount of a quantity per unit of another quantity; finding rate, total amount or number of units given the other two quantities",
        "meta_desc": "Free P5 rate worksheets: find the rate, total or number of units, use rate tables, pick best buys and solve word problems. 100 questions with answers.",
        "key_big": "A rate is the amount for 1 unit: find 1 unit first, then multiply or divide.",
        "key_sub": "4 kg cost $10, so 1 kg costs $10 ÷ 4 = $2.50, and 7 kg cost 7 × $2.50 = $17.50.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }
    assert len(u["meta_desc"]) <= 160, len(u["meta_desc"])
    return mark_large(u, "bar model|rate table")


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
