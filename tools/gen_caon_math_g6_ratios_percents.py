# -*- coding: utf-8 -*-
"""
Canada (Ontario) Grade 6 Math: Ratios, rates and percents
(Ontario Curriculum, Grades 1-8: Mathematics, 2020 — Grade 6, Number, B2)
  python3 tools/gen_ca_math_g6_ratios_percents.py
Ratios and equivalent ratios (ratio tables, part-to-part vs part-to-whole); rates and unit rates
(km/h, unit prices, better buys); percent of a quantity with mental-math benchmarks
(1%, 5%, 10%, 15%, 25%, 50%); discounts and sale prices; word problems.
Wrong answers come from real mistakes: 20% off $45 = $25, reversed ratios, part-to-part used as part-to-whole,
adding instead of multiplying, dividing the wrong way, giving the discount instead of the sale price.
Every answer is checked with fractions.Fraction (never float).
Canadian English, dollars and cents (¢), metric units, SI number spacing. HTML attributes use single quotes.
"""
import json, os, random, re
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "ca-on", "math", "grade-6")
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


def R(a, b):
    return "%s:%s" % (a, b)


def plain(s):
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", s)).strip()


FRX = re.compile(r"^<span class='fr'><span class='fn'>(\d+)</span><span class='fd'>(\d+)</span></span>$")
RAT = re.compile(r"^(\d+):(\d+)$")
NUM = re.compile(r"^(\$)?(\d[\d" + NBSP + r"]*(?:\.\d+)?)(¢|%)?( .+)?$")


def val(c):
    """Value of a choice with its unit, or None when it is not a single number."""
    m = FRX.match(c)
    if m:
        return (F(int(m.group(1)), int(m.group(2))), "")
    m = RAT.match(c)
    if m:
        return (F(int(m.group(1)), int(m.group(2))), "ratio")
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
def counters_svg(a, b, ca="red", cb="blue"):
    """A row of a counters of colour ca, then b counters of colour cb. Blue counters have a white ring
    so the two colours differ in print too."""
    col = {"red": RED, "blue": BLUE, "yellow": "#e8b923", "green": FILL}
    r, gap = 13, 7
    n = a + b
    W = 8 + n * (2 * r + gap) - gap + 8
    s = []
    for i in range(n):
        cx = 8 + r + i * (2 * r + gap)
        c = ca if i < a else cb
        s.append("<circle cx='%d' cy='%d' r='%d' fill='%s' stroke='%s' stroke-width='2'/>" % (cx, 8 + r, r, col[c], LINE))
        if c == cb:
            s.append("<circle cx='%d' cy='%d' r='5' fill='#fff'/>" % (cx, 8 + r))
    return svg_wrap(W, 2 * r + 16, "".join(s), "counters: %d %s and %d %s" % (a, ca, b, cb))


def ratio_table_svg(names, rows, label="ratio table"):
    """Two-row ratio table. names: row headings; rows: two lists of cell texts ('?' in red)."""
    fs = 16
    hw = max(tw(n, fs) for n in names) + 18
    cw = max([46] + [tw(c, fs) + 20 for r in rows for c in r])
    rh = 34
    n = len(rows[0])
    W = int(hw + n * cw + 8)
    H = 2 * rh + 8
    s = ["<rect x='4' y='4' width='%.1f' height='%d' fill='#eef6f0'/>" % (hw, 2 * rh)]
    for j, nm in enumerate(names):
        y = 4 + j * rh
        s.append(text(4 + hw / 2, y + rh / 2 + 5.5, nm, fs))
        for i, c in enumerate(rows[j]):
            x = 4 + hw + i * cw
            s.append(text(x + cw / 2, y + rh / 2 + 5.5, c, fs, col=RED if c == "?" else LINE))
    for j in range(3):
        s.append("<line x1='4' y1='%d' x2='%.1f' y2='%d' stroke='%s' stroke-width='%s'/>"
                 % (4 + j * rh, 4 + hw + n * cw, 4 + j * rh, LINE, "2"))
    for i in range(n + 1):
        x = 4 + hw + i * cw
        s.append("<line x1='%.1f' y1='4' x2='%.1f' y2='%d' stroke='%s' stroke-width='2'/>" % (x, x, 4 + 2 * rh, LINE))
    s.append("<line x1='4' y1='4' x2='4' y2='%d' stroke='%s' stroke-width='2'/>" % (4 + 2 * rh, LINE))
    return svg_wrap(W, H, "".join(s), label)


def double_line_svg(top_name, tops, bot_name, bots, label="double number line"):
    """Double number line: equal spaces, top labels above, bottom labels below ('?' in red)."""
    fs = 16
    nw = max(tw(top_name, fs), tw(bot_name, fs)) + 10
    n = len(tops)
    sp = max([62] + [tw(t, fs) + 14 for t in tops + bots])
    x0 = 8 + nw + 14
    x1 = x0 + (n - 1) * sp
    W = int(x1 + sp / 2 + 4)
    yt, yb = 34, 64
    s = [text(8 + nw / 2, yt + 5, top_name, fs, col=BLUE), text(8 + nw / 2, yb + 5, bot_name, fs, col=BLUE)]
    s.append("<line x1='%.1f' y1='%d' x2='%.1f' y2='%d' stroke='%s' stroke-width='2.5'/>" % (x0 - 6, yt, x1 + 14, yt, LINE))
    s.append("<line x1='%.1f' y1='%d' x2='%.1f' y2='%d' stroke='%s' stroke-width='2.5'/>" % (x0 - 6, yb, x1 + 14, yb, LINE))
    for i in range(n):
        x = x0 + i * sp
        for y in (yt, yb):
            s.append("<line x1='%.1f' y1='%d' x2='%.1f' y2='%d' stroke='%s' stroke-width='2'/>" % (x, y - 8, x, y + 8, LINE))
        s.append(text(x, yt - 14, tops[i], fs, col=RED if tops[i] == "?" else LINE))
        s.append(text(x, yb + 28, bots[i], fs, col=RED if bots[i] == "?" else LINE))
    return svg_wrap(W, yb + 36, "".join(s), label)


def percent_bar_svg(total_txt, parts, shade, part_txt, W=420):
    """A bar for the whole amount (100%) in `parts` equal parts, the first `shade` parts shaded,
    each part labelled with part_txt; percent marks under the bar."""
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


# ============================================================ set 1: ratios and equivalent ratios
def set_ratios(P):
    its = []
    its.append(mcq(fig(counters_svg(3, 5)) + "What is the ratio of red counters to blue counters?",
                   R(3, 5), [R(5, 3), R(3, 8), R(5, 8)],
                   "There are 3 red and 5 blue counters. Red comes first, so the ratio is <b>3:5</b>. "
                   "5:3 is blue to red, and 3:8 compares red to <b>all</b> the counters."))
    its.append(mcq(fig(counters_svg(2, 7, "yellow", "blue")) + "What fraction of the counters are yellow?",
                   fr(2, 9), [fr(2, 7), fr(7, 9), fr(5, 9)],
                   "A fraction compares a part to the <b>whole</b>. There are 2 + 7 = 9 counters, and 2 are yellow: "
                   "<b>%s</b>. %s compares yellow to blue (part to part)." % (fr(2, 9), fr(2, 7)), value=F(2, 9)))
    its.append(mcq("For every 4 laps that Olivia runs, Noah runs 3 laps. What is the ratio of Noah’s laps to Olivia’s laps?",
                   R(3, 4), [R(4, 3), R(3, 7), R(4, 7)],
                   "Noah is named first, so his number goes first: <b>3:4</b>. 4:3 is Olivia to Noah."))
    its.append(mcq("Which ratio is equivalent to 2:5?", R(6, 15), [R(5, 8), R(5, 2), R(6, 5)],
                   "Multiply <b>both</b> terms by 3: 2 × 3 = 6 and 5 × 3 = 15, so 2:5 = <b>6:15</b>. "
                   "5:8 adds 3 to both terms, and 6:5 multiplies only the first term."))
    its.append(mcq("A class has 12 girls and 15 boys. What is the ratio of girls to boys in simplest form?",
                   R(4, 5), [R(5, 4), R(4, 9), R(5, 9)],
                   "12:15. Divide both terms by 3: 12 ÷ 3 = 4 and 15 ÷ 3 = 5. The ratio is <b>4:5</b>. "
                   "4:9 compares the girls to the whole class (12:27)."))
    its.append(mcq("Write 18:24 in simplest form.", R(3, 4), [R(4, 3), R(9, 12), R(3, 9)],
                   "The greatest common factor of 18 and 24 is 6. 18 ÷ 6 = 3 and 24 ÷ 6 = 4, so 18:24 = <b>3:4</b>. "
                   "9:12 is equivalent but not in simplest form: 9 and 12 can both be divided by 3. "
                   "3:9 takes 15 away from each term.", same_ok=True))
    its.append(mcq("Which ratio is equivalent to 16:20?", R(4, 5), [R(5, 4), R(8, 12), R(8, 20)],
                   "Divide both terms by 4: 16 ÷ 4 = 4 and 20 ÷ 4 = 5. So 16:20 = <b>4:5</b>. "
                   "8:12 subtracts 8 from each term, and 8:20 halves only the first term."))
    its.append(mcq("Which ratio is <b>not</b> equivalent to 4:6?", R(6, 8), [R(2, 3), R(8, 12), R(10, 15)],
                   "4:6 = 2:3. 8:12 and 10:15 also simplify to 2:3. <b>6:8</b> adds 2 to both terms, "
                   "and it simplifies to 3:4, so it is not equivalent.", same_ok=True))
    its.append(mcq(fig(ratio_table_svg(["Water (cups)", "Mix (scoops)"], [["3", "6", "9"], ["2", "4", "?"]])) +
                   "The ratio table is for a jug of lemonade. What number is missing?",
                   "6", ["5", "9", "8"],
                   "The top row goes 3, 6, 9: that is 3 × 1, 3 × 2, 3 × 3. Do the same to the bottom row: 2 × 3 = <b>6</b>. "
                   "5 adds 3 like the top row, but each row grows by its own amount."))
    its.append(mcq(fig(ratio_table_svg(["Juice (L)", "Water (L)"], [["1", "2", "3", "?"], ["4", "8", "12", "20"]])) +
                   "The table shows juice and water mixed in the same ratio. What number is missing?",
                   "5", ["4", "16", "80"],
                   "The ratio is 1:4, so the water is always 4 times the juice. 20 ÷ 4 = <b>5</b>. "
                   "4 just counts on by 1, but 20 is not the next number after 12 in steps of 4."))
    its.append(mcq("Find the missing term: 3:4 = ?:20", "15", ["19", "5", "12"],
                   "4 × 5 = 20, so multiply the first term by 5 too: 3 × 5 = <b>15</b>. "
                   "19 adds 16 to the first term, and equivalent ratios never come from adding."))
    its.append(mcq("Find the missing term: 5:8 = 20:?", "32", ["23", "4", "28"],
                   "5 × 4 = 20, so multiply 8 by 4 too: 8 × 4 = <b>32</b>. 23 adds 15 to both terms."))
    its.append(mcq(fig(ratio_table_svg(["Flour (cups)", "Eggs"], [["2", "4", "8", "?"], ["3", "6", "12", "15"]])) +
                   "A muffin recipe uses flour and eggs in the same ratio. What number is missing?",
                   "10", ["11", "16", "13"],
                   "The ratio is 2:3. 15 = 3 × 5, so the flour is 2 × 5 = <b>10</b> cups. "
                   "11 adds 3 like the egg row, and 16 doubles 8 although 15 is not double 12."))
    its.append(mcq(fig(ratio_table_svg(["Red", "White"], [["6", "2", "?"], ["9", "3", "15"]])) +
                   "The table shows red and white paint mixed in the same ratio. What number is missing?",
                   "10", ["12", "5", "30"],
                   "6:9 = 2:3. 15 = 3 × 5, so red = 2 × 5 = <b>10</b>. 12 takes the difference of 3 away from 15 "
                   "(15 − 3), and 5 is only 15 ÷ 3."))
    its.append(mcq("In a bag, the ratio of red marbles to green marbles is 2:3. What fraction of the marbles are red?",
                   fr(2, 5), [fr(2, 3), fr(3, 5), fr(3, 2)],
                   "2:3 means 2 red for every 3 green, so every group has 2 + 3 = 5 marbles. Red is <b>%s</b> of them. "
                   "%s is part to part (red to green), not part to whole." % (fr(2, 5), fr(2, 3)), value=F(2, 5)))
    its.append(mcq("In a basket, 6 of the 10 apples are red and the rest are green. What is the ratio of red apples to green apples?",
                   R(3, 2), [R(3, 5), R(2, 3), R(2, 5)],
                   "10 − 6 = 4 apples are green. Red to green is 6:4 = <b>3:2</b>. 3:5 is 6:10, red to <b>all</b> the apples."))
    n, he, his = P.next()
    its.append(mcq("%s mixes blue and yellow paint in the ratio 3:5 to make green. %s uses 15 mL of blue. "
                   "How much yellow does %s need?" % (n, he.capitalize(), he),
                   "25 mL", ["17 mL", "9 mL", "40 mL"],
                   "3 × 5 = 15, so multiply the yellow by 5 too: 5 × 5 = <b>25 mL</b>. "
                   "17 mL adds 2, and 9 mL uses the ratio the wrong way round (5:3). 40 mL is the total paint.",
                   value=25))
    its.append(mcq("At an animal shelter, the ratio of cats to dogs is 3:2. There are 12 cats. How many dogs are there?",
                   "8", ["18", "11", "20"],
                   "12 cats = 3 × 4, so there are 2 × 4 = <b>8</b> dogs. 18 uses the ratio the wrong way round, "
                   "and 20 is the total number of animals."))
    its.append(mcq("The ratio of boys to girls in a choir is 4:5. There are 36 students in the choir. How many are girls?",
                   "20", ["16", "45", "9"],
                   "Each group has 4 + 5 = 9 students. 36 ÷ 9 = 4 groups, so there are 5 × 4 = <b>20</b> girls. "
                   "45 treats 36 as the number of boys (part to part), and 16 is the number of boys."))
    its.append(mcq("Mix A is 2 cups of orange juice and 3 cups of water. Mix B is 3 cups of orange juice and 5 cups of water. "
                   "Which mix tastes more of orange?", "Mix A", ["Mix B", "They taste the same", "You can’t tell"],
                   "Compare juice to the whole mix. Mix A: %s = 0.4. Mix B: %s = 0.375. 0.4 &gt; 0.375, so <b>Mix A</b>. "
                   "Mix B has more cups of juice, but it also has more water." % (fr(2, 5), fr(3, 8))))
    order = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19]
    its = [its[i] for i in order]
    assert len(its) == 20, len(its)
    return {"title": "Ratios, equivalent ratios and ratio tables", "items": its}


# ============================================================ set 2: rates and unit rates
def set_rates(P):
    its = []
    its.append(mcq("A car travels 240 km in 3 hours at a steady speed. What is its speed in kilometres per hour?",
                   "80 km/h", ["720 km/h", "8 km/h", "60 km/h"],
                   "A unit rate is the amount for <b>1</b> hour: 240 ÷ 3 = <b>80 km/h</b>. 720 multiplies instead of dividing.",
                   value=80))
    n, he, his = P.next()
    its.append(mcq("%s reads 120 pages in 4 days. %s reads the same number of pages each day. How many pages a day is that?"
                   % (n, he.capitalize()), "30", ["480", "116", "40"],
                   "Pages for 1 day: 120 ÷ 4 = <b>30</b> pages. 480 multiplies, and 116 subtracts.", value=30))
    its.append(mcq("A pump fills a 60 L tank in 5 minutes. How many litres does it pump per minute?",
                   "12 L", ["300 L", "55 L", "65 L"],
                   "Litres for 1 minute: 60 ÷ 5 = <b>12 L</b>. 300 L multiplies instead of dividing.", value=12))
    its.append(mcq("A box of 12 granola bars costs $5.40. What is the cost of 1 bar?",
                   "45¢", ["$4.50", "$2.22", "54¢"],
                   "$5.40 ÷ 12: 540¢ ÷ 12 = <b>45¢</b>. $4.50 puts the decimal point in the wrong place, "
                   "and $2.22 divides 12 by 5.40.", value=F(45, 100)))
    its.append(mcq("Pencils are 5 for $1.20. What is the cost of 1 pencil?",
                   "24¢", ["$6", "12¢", "20¢"],
                   "$1.20 ÷ 5 = 120¢ ÷ 5 = <b>24¢</b>. $6 multiplies 1.20 × 5, and 12¢ divides by 10.", value=F(24, 100)))
    its.append(mcq(fig(ratio_table_svg(["Distance (km)", "Time (h)"], [["90", "180", "?"], ["1", "2", "5"]], "rate table")) +
                   "A bus drives at a steady speed. What distance is missing?",
                   "450", ["270", "185", "900"],
                   "The unit rate is 90 km in 1 h. In 5 h: 90 × 5 = <b>450 km</b>. "
                   "270 adds just one more 90, but 5 h is 3 hours after 2 h."))
    its.append(mcq("A pump fills water at 12 L per minute. How long does it take to fill 84 L?",
                   "7 min", ["72 min", "96 min", "8 min"],
                   "84 ÷ 12 = <b>7 min</b>. Check: 12 × 7 = 84. 72 subtracts 12, and 96 adds it.", value=7))
    a, ah, _ = P.next()
    its.append(mcq("%s earns $36 for 3 hours of babysitting. At the same rate, how much does %s earn in 5 hours?" % (a, ah),
                   "$60", ["$38", "$108", "$180"],
                   "Unit rate: $36 ÷ 3 = $12 per hour. 5 hours: 5 × $12 = <b>$60</b>. "
                   "$38 adds 2 more dollars instead of 2 more hours, and $180 is $36 × 5.", value=60))
    its.append(mcq("A printer prints 45 pages in 3 minutes. How many pages does it print in 10 minutes?",
                   "150", ["52", "135", "450"],
                   "45 ÷ 3 = 15 pages per minute. 15 × 10 = <b>150</b> pages. 450 is 45 × 10, the pages for 30 minutes.",
                   value=150))
    its.append(mcq("Emma’s heart beats 21 times in 15 seconds. At this rate, how many times does it beat in 1 minute?",
                   "84", ["1260", "36", "315"],
                   "1 minute = 60 seconds = 4 × 15 seconds. 21 × 4 = <b>84</b> beats per minute. "
                   "1260 multiplies by 60, but 21 beats is for 15 seconds, not 1 second.", value=84))
    n, he, his = P.next()
    its.append(mcq("%s cycles 18 km in 1.5 hours. What is %s average speed?" % (n, his),
                   "12 km/h", ["27 km/h", "16.5 km/h", "19.5 km/h"],
                   "Speed = distance ÷ time: 18 ÷ 1.5 = <b>12 km/h</b>. Check: in 1 h 12 km, in half an hour 6 km, total 18 km. "
                   "27 km/h multiplies.", value=12))
    its.append(mcq("A hiker walks at 5 km/h. How far does the hiker walk in 2.5 hours?",
                   "12.5 km", ["7.5 km", "2 km", "10 km"],
                   "Distance = speed × time: 5 × 2.5 = <b>12.5 km</b>. 7.5 km adds, and 10 km is only 2 hours: "
                   "the half hour adds 2.5 km more.", value=F(25, 2)))
    its.append(mcq("8 m of fabric costs $26. What is the cost of 1 m?",
                   "$3.25", ["$2.60", "$208", "$18"],
                   "$26 ÷ 8 = <b>$3.25</b>. Check: 8 × $3.25 = $26. $208 multiplies, and $18 subtracts 26 − 8.",
                   value=F(13, 4)))
    its.append(mcq("A car uses 7 L of gas for every 100 km. How much gas does it use for 350 km?",
                   "24.5 L", ["50 L", "21 L", "28 L"],
                   "350 km = 3.5 × 100 km. 7 × 3.5 = <b>24.5 L</b>. 21 L forgets the last 50 km, "
                   "and 50 L divides 350 by 7.", value=F(49, 2)))
    its.append(mcq("Which is the better buy for milk?", "4 L for $6.20",
                   ["2 L for $3.40", "They cost the same per litre", "You can’t tell"],
                   "Find the unit price. 4 L: $6.20 ÷ 4 = $1.55 per litre. 2 L: $3.40 ÷ 2 = $1.70 per litre. "
                   "<b>4 L for $6.20</b> costs less per litre, even though its price is higher."))
    its.append(mcq("Which is the better buy for cereal?", "1 kg for $5.80",
                   ["750 g for $4.50", "They cost the same per 100 g", "You can’t tell"],
                   "Price per 100 g. 750 g: $4.50 ÷ 7.5 = 60¢. 1 kg = 1000 g: $5.80 ÷ 10 = 58¢. "
                   "<b>1 kg for $5.80</b> is cheaper per 100 g."))
    a, ah, _ = P.next()
    b, bh, _ = P.next()
    its.append(mcq("%s runs 1200 m in 5 minutes. %s runs 1000 m in 4 minutes. Who runs faster?" % (a, b),
                   b, [a, "They run at the same speed", "You can’t tell"],
                   "Metres per minute: %s 1200 ÷ 5 = 240 m. %s 1000 ÷ 4 = 250 m. 250 &gt; 240, so <b>%s</b> is faster, "
                   "even though %s runs farther." % (a, b, b, a)))
    its.append(mcq(fig(double_line_svg("km", ["0", "?", "?", "285"], "h", ["0", "1", "2", "3"])) +
                   "Owen’s family drives at a steady speed. What is their speed?",
                   "95 km/h", ["71.25 km/h", "285 km/h", "142.5 km/h"],
                   "285 km in 3 h. Speed = 285 ÷ 3 = <b>95 km/h</b>. 71.25 divides by 4, the number of marks, "
                   "but there are only 3 hours.", value=95))
    its.append(mcq("It takes about 40 L of maple sap to make 1 L of maple syrup. How much sap is needed for 2.5 L of syrup?",
                   "100 L", ["42.5 L", "16 L", "80 L"],
                   "40 L of sap for each litre of syrup: 40 × 2.5 = <b>100 L</b>. 80 L forgets the half litre "
                   "(40 × 2), and 16 L divides 40 by 2.5.", value=100))
    its.append(mcq("A 4 kg bag of potatoes costs $6.40. At the same price per kilogram, what do 2.5 kg cost?",
                   "$4", ["$2.56", "$3.90", "$16"],
                   "Unit price: $6.40 ÷ 4 = $1.60 per kg. 2.5 × $1.60 = <b>$4</b>. $3.90 just subtracts 2.5 from 6.40, "
                   "and $16 multiplies 6.40 × 2.5.", value=4))
    order = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19]
    its = [its[i] for i in order]
    assert len(its) == 20, len(its)
    return {"title": "Rates and unit rates: km/h and unit prices", "items": its}


# ============================================================ set 3: percent of a quantity
def set_percent():
    its = []

    def pq(p, n, right, wrong, e, q=None, fg=""):
        assert F(right) == pc(p, n), (p, n, right)
        its.append(mcq(fg + (q or "What is %s%% of %s?" % (num(p), num(n))), num(right), [num(w) for w in wrong], e))

    pq(10, 70, 7, [F(7, 10), 700, 60],
       "10%% = %s. Divide by 10: 70 ÷ 10 = <b>7</b>. 0.7 is 1%%, and 60 subtracts 10 from 70." % fr(1, 10))
    pq(50, 86, 43, [36, 172, F(43, 5)],
       "50% is half. 86 ÷ 2 = <b>43</b>. 36 subtracts 50 from 86, and 172 doubles.")
    pq(1, 300, 3, [30, F(3, 10), 299],
       "1%% = %s. Divide by 100: 300 ÷ 100 = <b>3</b>. 30 is 10%%." % fr(1, 100))
    pq(25, 48, 12, [24, 23, 192],
       "25%% = %s. Divide by 4: 48 ÷ 4 = <b>12</b>. 24 is 50%%, and 23 subtracts 25 from 48." % fr(1, 4))
    pq(25, 360, 90, [180, 335, 36],
       "25%% = %s, so divide by 4 (or halve twice): 360 → 180 → <b>90</b>. 36 is 10%%, and 180 is 50%%." % fr(1, 4))
    pq(5, 60, 3, [6, 12, 55],
       "10% of 60 is 6. 5% is half of 10%: 6 ÷ 2 = <b>3</b>. 12 divides 60 by 5, which gives 20%.")
    pq(1, 450, F(9, 2), [45, F(45, 100), 449],
       "1% means divide by 100: 450 ÷ 100 = <b>4.5</b>. 45 is 10%.")
    pq(3, 200, 6, [60, F(3, 5), 197],
       "1% of 200 is 2. 3% is 3 × 2 = <b>6</b>. 60 is 30%.")
    pq(10, F(7, 2), F(7, 20), [35, F(7, 200), F(5, 2)],
       "10% means divide by 10: 3.5 ÷ 10 = <b>0.35</b>. 35 multiplies by 10, and 2.5 subtracts 1.")
    pq(20, 45, 9, [25, F(9, 2), 90],
       "10% of 45 is 4.5. 20% is double: 2 × 4.5 = <b>9</b>. 25 subtracts 20 from 45, but 20% is not 20.")
    pq(15, 40, 6, [4, 2, 25],
       "15% = 10% + 5%. 10% of 40 = 4, and 5% is half of that, 2. 4 + 2 = <b>6</b>. 4 is only 10%, and 2 is only 5%.")
    pq(15, 80, 12, [8, F(6, 5), 65],
       "10% of 80 = 8. 5% = 4. 15% = 8 + 4 = <b>12</b>. 8 stops at 10%, and 65 subtracts 15 from 80.")
    pq(5, 240, 12, [24, 48, 235],
       "10% of 240 = 24. 5% is half: <b>12</b>. 48 divides 240 by 5, which is 20%.")
    pq(30, 150, 45, [15, 120, F(9, 2)],
       "10% of 150 = 15. 30% = 3 × 15 = <b>45</b>. 15 is only 10%, and 120 subtracts 30 from 150.")
    pq(75, 40, 30, [10, 20, 35],
       "25% of 40 = 10. 75% = 3 × 25%, so 3 × 10 = <b>30</b>. Or 75% = 100% − 25%: 40 − 10 = 30. 10 is only 25%.")
    pq(15, 260, 39, [26, 13, 245],
       "10% of 260 = 26. 5% = 13. 15% = 26 + 13 = <b>39</b>. 26 and 13 are only the two steps.")
    pq(1, 25000, 250, [2500, 25, 24999],
       "1%% means divide by 100: 25%s000 ÷ 100 = <b>250</b>. 2500 is 10%%, and 25 divides by 1000." % NBSP)
    pq(30, 60, 18, [6, 30, 20],
       "The bar shows $60 in 10 equal parts, so each part is 10% = $6. 3 parts: 3 × $6 = <b>$18</b>. "
       "$20 divides $60 by 3, and $30 uses the 30 as dollars.",
       q="The whole bar is $60. What is 30% of $60?",
       fg=fig(percent_bar_svg("$60", 10, 3, "$6")))
    its[-1]["c"] = ["$" + c for c in its[-1]["c"]]
    its.append(mcq("Which has the same value as 25% of 60?", "50% of 30", ["25% of 30", "50% of 120", "60 ÷ 25"],
                   "25% of 60 = 60 ÷ 4 = 15. 50% of 30 = 30 ÷ 2 = 15 too, so <b>50% of 30</b>. "
                   "25% of 30 = 7.5, 50% of 120 = 60, and 60 ÷ 25 = 2.4."))
    its.append(mcq("Which is greater: 25% of 80 or 50% of 30?", "25% of 80",
                   ["50% of 30", "They are equal", "You can’t tell"],
                   "25% of 80 = 80 ÷ 4 = 20. 50% of 30 = 15. 20 &gt; 15, so <b>25% of 80</b> is greater, "
                   "even though 50% is the bigger percent."))
    order = [0, 1, 2, 3, 5, 4, 6, 7, 8, 9, 13, 17, 12, 10, 11, 14, 15, 16, 18, 19]
    its = [its[i] for i in order]
    assert len(its) == 20, len(its)
    return {"title": "Percent of a quantity: 1%, 5%, 10%, 15%, 25% and 50%", "items": its}


# ============================================================ set 4: discounts and sale prices
def set_discounts():
    its = []

    def sale(price, p, q, wrong, e, ask="sale"):
        d = pc(p, price)
        right = price - d if ask == "sale" else d
        its.append(mcq(q, money(right), [money(w) for w in wrong], e, value=right))

    sale(45, 20, "A $45 jacket is 20% off. What is the sale price?", [25, 9, F(81, 2)],
         "10% of $45 = $4.50, so 20% = $9. Sale price: $45 − $9 = <b>$36</b>. "
         "$25 takes away 20 dollars instead of 20 percent. $9 is the discount, not the price.")
    sale(60, 25, "A $60 hockey stick is 25% off. How much money do you save?", [45, 35, F(12, 5)],
         "25%% = %s. $60 ÷ 4 = <b>$15</b> saved. $45 is the sale price, and $35 takes away 25 dollars." % fr(1, 4),
         ask="discount")
    sale(80, 10, "Skates that cost $80 are 10% off. What is the sale price?", [70, 8, 88],
         "10% of $80 = $8. $80 − $8 = <b>$72</b>. $70 takes away 10 dollars, and $88 adds the discount.")
    sale(120, 30, "Winter boots that cost $120 are 30% off. What is the sale price?", [90, 36, 108],
         "10% of $120 = $12, so 30% = $36. $120 − $36 = <b>$84</b>. $90 takes away 30 dollars, "
         "and $108 takes away only 10%.")
    sale(16, 25, "A $16 board game is 25% off. What is the sale price?", [4, 8, F(1575, 100)],
         "25% of $16 = $16 ÷ 4 = $4. $16 − $4 = <b>$12</b>. $4 is the discount, and $8 is 50% off.")
    sale(250, 20, "A $250 bike is 20% off. What is the sale price?", [230, 50, 225],
         "10% of $250 = $25, so 20% = $50. $250 − $50 = <b>$200</b>. $230 takes away 20 dollars.")
    sale(30, 15, "A $30 T-shirt is 15% off. What is the sale price?", [15, F(9, 2), 27],
         "10% of $30 = $3. 5% = $1.50. 15% = $4.50. $30 − $4.50 = <b>$25.50</b>. $27 takes off only 10%, "
         "and $15 takes away 15 dollars.")
    sale(90, 40, "Running shoes that cost $90 are 40% off. What is the sale price?", [50, 36, 86],
         "10% of $90 = $9, so 40% = $36. $90 − $36 = <b>$54</b>. $50 takes away 40 dollars, and $36 is the discount.")
    sale(140, 15, "A store takes 15% off everything. What is the sale price of a $140 scooter?", [125, 21, 126],
         "10% of $140 = $14. 5% = $7. 15% = $21. $140 − $21 = <b>$119</b>. $125 takes away 15 dollars, "
         "and $126 takes off only 10%.")
    sale(260, 5, "A $260 tablet is 5% off. What is the sale price?", [255, 13, 234],
         "10% of $260 = $26, so 5% = $13. $260 − $13 = <b>$247</b>. $255 takes away 5 dollars, and $234 takes off 10%.")
    sale(9, 5, "A $9 book is 5% off. What is the sale price?", [4, F(81, 10), F(45, 100)],
         "10% of $9 = 90¢, so 5% = 45¢. $9.00 − $0.45 = <b>$8.55</b>. $4 takes away 5 dollars, and 45¢ is the discount.")
    sale(95, 50, "All winter coats are 50% off. What is the sale price of a $95 coat?", [45, F(171, 2), F(19, 2)],
         "50% is half: $95 ÷ 2 = <b>$47.50</b>. $45 takes away 50 dollars, and $85.50 takes off only 10%.")
    its.append(mcq("A $28 backpack is 25% off. Which calculation gives the sale price?", "75% of $28",
                   ["25% of $28", "$28 − 25", "$28 ÷ 25"],
                   "You pay what is left: 100% − 25% = 75%. So the sale price is <b>75% of $28</b> = $21. "
                   "25% of $28 = $7 is the discount."))
    for price, save, right, wrong, e in [
        (48, 12, 25, [12, 36, 4],
         "$12 out of $48 = %s = %s = <b>25%%</b>. 12%% uses the dollars as a percent, and 4%% is 48 ÷ 12." % (fr(12, 48), fr(1, 4))),
        (12, F(12, 5), 20, [F(12, 5), 24, 5],
         "10% of $12 is $1.20, and $2.40 is double that, so the discount is <b>20%</b>. 2.4% uses the dollars as a percent, "
         "and 5% is 12 ÷ 2.40."),
    ]:
        assert F(save) / price * 100 == right
        its.append(mcq("You save %s on a %s item. What percent is the discount?" % (money(save), money(price)),
                       num(right) + "%", [num(w) + "%" for w in wrong], e))
    its.append(mcq("Mitts that cost $40 are on sale for $30. What percent is the discount?", "25%", ["10%", "75%", "30%"],
                   "The discount is $40 − $30 = $10. $10 out of $40 = %s = <b>25%%</b>. 10%% uses the $10 as a percent, "
                   "and 75%% is the part you pay." % fr(1, 4)))
    its.append(mcq("Store A takes $35 off a $140 coat. Store B takes 20% off the same coat. Which store saves you more?",
                   "Store A", ["Store B", "They save the same", "You can’t tell"],
                   "20%% of $140 = 2 × $14 = $28. $35 &gt; $28, so <b>Store A</b> saves more. "
                   "($35 out of $140 is %s = 25%%.)" % fr(1, 4)))
    assert pc(20, 140) == 28
    its.append(mcq("A $64 tent is 25% off. You pay with a $50 bill. How much change do you get?",
                   "$2", ["$11", "$16", "$34"],
                   "25% of $64 = $16, so the sale price is $64 − $16 = $48. Change: $50 − $48 = <b>$2</b>. "
                   "$11 comes from taking 25 dollars off ($39), and $16 is the discount.", value=2))
    assert 50 - (64 - pc(25, 64)) == 2
    its.append(mcq("A $20 book is not on sale. Ontario HST is 13%. What is the total with tax?",
                   "$22.60", ["$33", "$2.60", "$20.13"],
                   "13% of $20: 10% = $2, 1% = 20¢, so 3% = 60¢ and 13% = $2.60. $20 + $2.60 = <b>$22.60</b>. "
                   "$33 adds 13 dollars, and $20.13 adds 13 cents.", value=F(226, 10)))
    assert 20 + pc(13, 20) == F(226, 10)
    its.append(mcq("Sofia paid $24 for a sweater that was 20% off. What was the price before the sale?",
                   "$30", ["$28.80", "$44", "$19.20"],
                   "She paid 100% − 20% = 80% of the price. 80% = $24, so 10% = $3 and 100% = <b>$30</b>. "
                   "Check: 20% of $30 = $6, and $30 − $6 = $24. $28.80 adds 20% of $24, but the 20% is of the "
                   "<b>original</b> price.", value=30))
    assert 30 - pc(20, 30) == 24
    order = [0, 2, 11, 1, 4, 3, 5, 7, 8, 9, 6, 10, 12, 15, 13, 14, 16, 17, 18, 19]
    its = [its[i] for i in order]
    assert len(its) == 20, len(its)
    return {"title": "Discounts and sale prices", "items": its}


# ============================================================ set 5: word problems
def set_problems(P):
    its = []
    its.append(mcq("A hockey stick costs $84. It is 25% off. What is the sale price?", "$63",
                   ["$59", "$21", "$75.60"],
                   "25%% = %s. $84 ÷ 4 = $21 off. $84 − $21 = <b>$63</b>. $59 takes away 25 dollars, "
                   "$21 is the discount, and $75.60 takes off only 10%%." % fr(1, 4), value=63))
    assert 84 - pc(25, 84) == 63 and 84 - pc(10, 84) == F(756, 10)
    n, he, his = P.next()
    its.append(mcq("On a road trip, %s’s family drives about 450 km from Toronto to Ottawa in 5 hours. "
                   "What is their average speed?" % n, "90 km/h", ["2250 km/h", "445 km/h", "45 km/h"],
                   "Speed = distance ÷ time: 450 ÷ 5 = <b>90 km/h</b>. 2250 multiplies, and 445 subtracts.", value=90))
    its.append(mcq("A family drives at 100 km/h. How long does it take to drive 350 km?", "3.5 h",
                   ["35 h", "3 h 50 min", "4 h"],
                   "Time = distance ÷ speed: 350 ÷ 100 = <b>3.5 h</b>, which is 3 h 30 min. "
                   "3 h 50 min mixes up 0.5 h with 50 minutes: half an hour is 30 minutes.", value=F(7, 2)))
    its.append(mcq("A class has 28 students. The ratio of students who bike to school to students who walk is 3:4. "
                   "How many students bike?", "12", ["21", "16", "7"],
                   "Each group has 3 + 4 = 7 students. 28 ÷ 7 = 4 groups. Bikers: 3 × 4 = <b>12</b>. "
                   "21 finds %s of 28, but 3:4 is part to part; the bikers are %s of the class." % (fr(3, 4), fr(3, 7)),
                   value=12))
    its.append(mcq("Our school’s goal for the Terry Fox Run is $1500. So far we have raised $1200. "
                   "What percent of the goal is that?", "80%", ["20%", "125%", "30%"],
                   "%s = %s = %s = <b>80%%</b>. 20%% is the part still to raise. 125%% divides the wrong way (1500 ÷ 1200)."
                   % (fr(1200, 1500), fr(4, 5), fr(80, 100))))
    n, he, his = P.next()
    its.append(mcq("On a canoe trip, %s paddles 12 km in 3 hours. At the same rate, how far can %s paddle in 5 hours?" % (n, he),
                   "20 km", ["14 km", "60 km", "36 km"],
                   "Unit rate: 12 ÷ 3 = 4 km per hour. 5 h: 5 × 4 = <b>20 km</b>. 14 km adds 2, and 60 km is 12 × 5.",
                   value=20))
    its.append(mcq("A test has 24 questions. Mateo gets 18 right. What percent does he get right?", "75%",
                   ["18%", "6%", "25%"],
                   "%s = %s = <b>75%%</b>. 6%% and 25%% describe the 6 questions he got wrong." % (fr(18, 24), fr(3, 4))))
    its.append(mcq("A school has 400 students. 15% of them take the bus. How many students take the bus?",
                   "60", ["15", "385", "40"],
                   "10% of 400 = 40. 5% = 20. 15% = 40 + 20 = <b>60</b>. 385 subtracts 15, and 40 is only 10%.",
                   value=60))
    assert pc(15, 400) == 60
    its.append(mcq("On a lake, the ratio of loons to Canada geese is 2:7. There are 63 birds in all. How many are loons?",
                   "14", ["18", "49", "7"],
                   "Each group has 2 + 7 = 9 birds. 63 ÷ 9 = 7 groups, so there are 2 × 7 = <b>14</b> loons. "
                   "18 treats 63 as the number of geese (part to part), and 49 is the geese.", value=14))
    its.append(mcq("A pancake recipe uses 3 eggs for 12 pancakes. How many eggs are needed for 20 pancakes?",
                   "5", ["11", "4", "8"],
                   "12 pancakes ÷ 3 eggs = 4 pancakes per egg. 20 ÷ 4 = <b>5</b> eggs. "
                   "11 adds 8 eggs because there are 8 more pancakes.", value=5))
    its.append(mcq("Snow falls at 6 cm per hour for 4.5 hours on a snow day. How much snow falls?",
                   "27 cm", ["10.5 cm", "24 cm", "30 cm"],
                   "6 × 4.5 = 24 + 3 = <b>27 cm</b>. 24 cm forgets the half hour, and 10.5 cm adds 6 + 4.5.",
                   value=27))
    its.append(mcq("Which is the better buy for maple syrup?", "1 L for $22",
                   ["500 mL for $12.50", "They cost the same per litre", "You can’t tell"],
                   "500 mL is half a litre, so 1 L would cost 2 × $12.50 = $25. $22 &lt; $25, so <b>1 L for $22</b> "
                   "is the better buy."))
    its.append(mcq("In a class of 30 students, 12 play hockey. What is the ratio of students who play hockey to students "
                   "who do not?", R(2, 3), [R(2, 5), R(3, 2), R(3, 5)],
                   "30 − 12 = 18 do not play. 12:18 = <b>2:3</b> (divide by 6). 2:5 is 12:30, hockey players to the "
                   "<b>whole</b> class."))
    its.append(mcq("A hockey arena has 18%s000 seats. 5%% of the seats are empty. How many seats are empty?" % NBSP,
                   num(900), ["90", num(3600), num(17100)],
                   "10%% of 18%s000 = 1800. 5%% is half: <b>900</b>. 3600 divides by 5, which is 20%%, "
                   "and 17%s100 is the full seats." % (NBSP, NBSP), value=900))
    its.append(mcq("A survey asks 35 students their favourite sport. 40% choose soccer. How many students choose soccer?",
                   "14", ["21", "3.5", "75"],
                   "10% of 35 = 3.5. 40% = 4 × 3.5 = <b>14</b> students. 21 is the other 60%.", value=14))
    a, ah, _ = P.next()
    b, bh, _ = P.next()
    its.append(mcq("%s bikes 30 km in 2 hours. %s bikes 42 km in 3 hours. Who bikes faster?" % (a, b),
                   a, [b, "They bike at the same speed", "You can’t tell"],
                   "%s: 30 ÷ 2 = 15 km/h. %s: 42 ÷ 3 = 14 km/h. 15 &gt; 14, so <b>%s</b> is faster, "
                   "even though %s goes farther." % (a, b, a, b)))
    its.append(mcq("A car uses 8 L of gas for every 100 km. How much gas does it use on a 450 km trip?",
                   "36 L", ["56.25 L", "32 L", "40 L"],
                   "450 km = 4.5 × 100 km. 8 × 4.5 = <b>36 L</b>. 32 L forgets the last 50 km, and 56.25 L "
                   "divides 450 by 8.", value=36))
    its.append(mcq("A $40 helmet is 25% off. Then 13% HST is added to the sale price. What is the total?",
                   "$33.90", ["$45.20", "$24.80", "$35.20"],
                   "25% of $40 = $10, so the sale price is $30. 13% of $30 = $3 + 90¢ = $3.90. "
                   "$30 + $3.90 = <b>$33.90</b>. $45.20 forgets the discount, and $24.80 takes away the tax too.",
                   value=F(339, 10)))
    assert (40 - pc(25, 40)) * F(113, 100) == F(339, 10)
    its.append(mcq("A school rule says there must be at least 1 adult for every 8 students on a field trip. "
                   "52 students are going. What is the fewest number of adults needed?",
                   "7", ["6", "6.5", "44"],
                   "52 ÷ 8 = 6.5. 6 adults can take only 48 students, so 4 students would have no adult. "
                   "You can’t have half an adult, so round up to <b>7</b>.", value=7))
    its.append(mcq("A family drives for 3 hours at 90 km/h and then for 2 hours at 100 km/h. How far do they drive in all?",
                   "470 km", ["475 km", "190 km", "950 km"],
                   "3 × 90 = 270 km. 2 × 100 = 200 km. 270 + 200 = <b>470 km</b>. 475 km uses the average of the two speeds "
                   "(95 km/h), but the car spends more time at 90 km/h.", value=470))
    order = [0, 1, 5, 6, 7, 4, 2, 9, 10, 3, 8, 11, 12, 13, 14, 15, 16, 18, 17, 19]
    its = [its[i] for i in order]
    assert len(its) == 20, len(its)
    return {"title": "Word problems: sales, road trips and recipes", "items": its}


# ============================================================ lesson
def body_html():
    f_cnt = counters_svg(3, 5)
    f_tab = ratio_table_svg(["Flour (cups)", "Eggs"], [["2", "4", "6", "10"], ["3", "6", "9", "15"]])
    f_dl = double_line_svg("km", ["0", "90", "180", "270"], "h", ["0", "1", "2", "3"])
    f_bar = percent_bar_svg("$45", 10, 2, "$4.50", W=540)
    return (
        "<h2>Ratios</h2>"
        "<p>A <b>ratio</b> compares two amounts. 3:5 is read “3 to 5”. Keep the order of the words: "
        "red to blue means the red number comes first.</p>"
        "<figure class='sn-fig'>" + f_cnt +
        "<figcaption>Red to blue is 3:5 (part to part). Red to all counters is 3:8, so " + fr(3, 8) +
        " of the counters are red (part to whole).</figcaption></figure>"
        "<h2>Equivalent ratios and ratio tables</h2>"
        "<p>Multiply or divide <b>both</b> terms by the same number. Never add the same number to both terms.</p>"
        "<figure class='sn-fig'>" + f_tab +
        "<figcaption>Every column is 2:3 times a number. 15 = 3 × 5, so the flour is 2 × 5 = 10.</figcaption></figure>"
        + ex("Example", "Write 18:24 in simplest form.", "Divide both terms by 6: 18 ÷ 6 = 3 and 24 ÷ 6 = 4.", "3:4")
        + ex("Part of a total", "The ratio of boys to girls is 4:5. There are 36 students. How many are girls?",
             "Each group has 4 + 5 = 9 students. 36 ÷ 9 = 4 groups. Girls: 5 × 4.", "20 girls")
        + "<h2>Rates and unit rates</h2>"
        "<p>A <b>rate</b> compares two different units, like km and hours. A <b>unit rate</b> is the amount for 1: "
        "divide to find it. Then multiply to find any other amount.</p>"
        "<figure class='sn-fig'>" + f_dl +
        "<figcaption>90 km in 1 h is the unit rate: 90 km/h. In 3 h the car goes 3 × 90 = 270 km.</figcaption></figure>"
        + ex("Better buy", "Milk: 4 L for $6.20 or 2 L for $3.40?",
             "Price for 1 L: $6.20 ÷ 4 = $1.55 and $3.40 ÷ 2 = $1.70.", "4 L for $6.20")
        + "<h2>Percent of a quantity</h2>"
        "<p>Percent means <b>out of 100</b>. Start from easy benchmarks and build the percent you need.</p>"
        + table(["Percent", "How to find it", "Of $80"], [
            ["100%", "the whole amount", "$80"],
            ["50%", "divide by 2", "$40"],
            ["25%", "divide by 4 (half of 50%)", "$20"],
            ["10%", "divide by 10", "$8"],
            ["5%", "half of 10%", "$4"],
            ["1%", "divide by 100", "80¢"],
            ["15%", "10% + 5%", "$12"],
        ])
        + "<h2>Discounts and sale prices</h2>"
        "<p>The <b>discount</b> is the money you save. The <b>sale price</b> is the price minus the discount.</p>"
        "<figure class='sn-fig'>" + f_bar +
        "<figcaption>Each part of $45 is 10% = $4.50. 20% off is 2 parts: $9. You pay the other 8 parts.</figcaption></figure>"
        + ex("Example", "A $45 jacket is 20% off. What is the sale price?",
             "10% of $45 = $4.50, so 20% = $9. $45 − $9 = $36.", "$36")
        + "<h2>Common mistakes</h2>"
        + table(["Mistake", "What to do instead"], [
            ["20% off $45 = $45 − $20 = $25", "Find 20% of $45 first: $9. $45 − $9 = $36"],
            ["Ratio 2:3, so " + fr(2, 3) + " are red", "2:3 is part to part. The whole is 2 + 3 = 5, so " + fr(2, 5) + " are red"],
            ["2:5 = 5:8 (add 3 to both)", "Multiply both terms: 2:5 = 6:15"],
            ["240 km in 3 h = 720 km/h", "Unit rate: divide. 240 ÷ 3 = 80 km/h"],
            ["Giving the discount as the answer", "Read the question: discount or sale price?"],
        ])
    )


FAQ = [
    {"q": "What do Grade 6 students learn about ratios, rates and percents in Ontario?",
     "a": "In the Ontario Grade 6 math curriculum, students use ratios, rates and percents to solve problems, including finding a percent of a quantity, unit rates such as km/h, and discounts and sale prices."},
    {"q": "What is the difference between a ratio and a rate?",
     "a": "A ratio compares amounts of the same kind, like 3 red counters to 5 blue counters (3:5). A rate compares different units, like 240 km in 3 hours, and a unit rate gives the amount for 1, like 80 km/h."},
    {"q": "How do you find a percent of a number in your head?",
     "a": "Use benchmarks: 10% means divide by 10, 5% is half of 10%, 1% means divide by 100, 25% means divide by 4 and 50% means divide by 2. Then combine them, so 15% of 80 is 8 + 4 = 12."},
    {"q": "How do you calculate a sale price?",
     "a": "Find the discount first, then subtract it from the price. For 20% off $45, the discount is $9 and the sale price is $36, not $45 − $20 = $25."},
]


def mark_large(u, pattern):
    """Tag pictures that must print larger (ratio tables, double number lines, percent bars, long rows of counters)."""
    rx = re.compile(r"<svg (?=[^>]*aria-label='" + pattern + ")")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u


def gen():
    rnd = random.Random(36809)
    P = People(rnd)
    sets = [set_ratios(P), set_rates(P), set_percent(), set_discounts(), set_problems(P)]
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
        "country": "ca-on", "subject": "math", "grade": "grade-6", "slug": "ratios-rates-and-percents", "sort": 9,
        "updated": UPDATED, "pdf_url": "",
        "title": "Ratios, Rates and Percents: Ratio Tables, Unit Rates and Sale Prices",
        "seo_title": "Grade 6 Ratios, Rates and Percents Worksheets (Ontario Math): Free with Answer Key",
        "short_title": "Ratios, rates and percents",
        "domain": "Number",
        "standard_code": "Grade 6: Number, B2",
        "standard_url": "https://www.dcp.edu.gov.on.ca/en/curriculum/elementary-mathematics",
        "standard_text": "Represent and solve problems involving ratios, rates, and percents, including percents of quantities, using appropriate tools and strategies",
        "meta_desc": "Free Grade 6 ratios, rates and percents worksheets for the Ontario curriculum: equivalent ratios and ratio tables, unit rates and km/h, percent of a number with 10%, 5% and 25%, and discounts and sale prices. 100 math questions with an answer key for EQAO practice.",
        "key_big": "A unit rate is the amount for 1: divide first. For a percent, start from 10% (divide by 10) and build up.",
        "key_sub": "20% off $45 is not $25: 10% of $45 is $4.50, so 20% is $9 and the sale price is $36. A ratio of 2:3 means 2 out of every 5, not 2/3.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }
    return mark_large(u, "(ratio table|rate table|double number line|percent bar|counters)")


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
