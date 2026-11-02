# -*- coding: utf-8 -*-
"""
Canada (Ontario) Grade 5 Math: Ratios and rates
(Ontario Curriculum, Grades 1-8: Mathematics, 2020 - Grade 5: B2.9)
  python3 tools/gen_caon_math_g5_ratios.py
Part-to-part ratios from pictures (counters, shaded strips, groups), equivalent ratios and ratio tables,
rates (km per hour, dollars per item, unit rates), double number lines, and word problems
(recipes, juice mixes, field trips, road trips).
Wrong answers come from real mistakes: adding the same number to both terms instead of multiplying,
writing the terms in the wrong order, using part to whole instead of part to part, multiplying when
you should divide, reading the other line of a double number line, counting one mark too many,
and counting the marks instead of the hours.
Every answer is checked with fractions.Fraction (never float).
Canadian English, dollars and cents (¢), metric units, SI number spacing. HTML attributes use single quotes.
"""
import json, os, random, re
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "ca-on", "math", "grade-5")
UPDATED = "2026-11-02"
NBSP = " "
FILL = "#4fae74"
LINE = "#2b2b2b"
THIN = "#8a8a8a"
RED = "#d6453b"
BLUE = "#2f6fc0"
YELLOW = "#e8b923"
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
        s.append("<line x1='4' y1='%d' x2='%.1f' y2='%d' stroke='%s' stroke-width='2'/>"
                 % (4 + j * rh, 4 + hw + n * cw, 4 + j * rh, LINE))
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
    sp = max([58] + [tw(t, fs) + 14 for t in tops + bots])
    x0 = 8 + nw + 14
    x1 = x0 + (n - 1) * sp
    W = int(x1 + max(sp / 2, 22) + 4)
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


COL = {"red": RED, "blue": BLUE, "yellow": YELLOW, "green": FILL}


def counter(cx, cy, c, r=13):
    """One counter. Blue has a white ring and green a white cross, so the colours differ in print too."""
    s = "<circle cx='%.1f' cy='%.1f' r='%d' fill='%s' stroke='%s' stroke-width='2'/>" % (cx, cy, r, COL[c], LINE)
    if c == "blue":
        s += "<circle cx='%.1f' cy='%.1f' r='5' fill='#fff'/>" % (cx, cy)
    if c == "green":
        s += ("<path d='M%.1f %.1fh12M%.1f %.1fv12' stroke='#fff' stroke-width='3'/>"
              % (cx - 6, cy, cx, cy - 6))
    return s


def counters_svg(groups):
    """groups: list of groups, each a list of (count, colour). Groups are drawn with a wider gap
    (and a dashed ring when there is more than one group)."""
    r, gap, ggap = 13, 7, 24
    s, x = [], 8
    many = len(groups) > 1
    desc = []
    for gi, g in enumerate(groups):
        if gi:
            x += ggap - gap
        gx0 = x
        for cnt, c in g:
            for _ in range(cnt):
                s.append(counter(x + r, 12 + r, c))
                x += 2 * r + gap
        if many:
            s.append("<rect x='%.1f' y='6' width='%.1f' height='%d' rx='12' fill='none' stroke='%s' "
                     "stroke-width='1.6' stroke-dasharray='5 4'/>" % (gx0 - 5, x - gap - gx0 + 10, 2 * r + 12, THIN))
    W = x - gap + 8 + (5 if many else 0)
    tot = {}
    for g in groups:
        for cnt, c in g:
            tot[c] = tot.get(c, 0) + cnt
    desc = ", ".join("%d %s" % (v, k) for k, v in tot.items())
    lab = "counters: " + desc + (" in %d equal groups" % len(groups) if many else "")
    return svg_wrap(int(W), 2 * r + 24, "".join(s), lab)


def strip_svg(shaded, total):
    """A row of equal squares, the first `shaded` shaded green."""
    sz = 30
    W = 8 + total * sz + 8
    s = []
    for i in range(total):
        s.append("<rect x='%d' y='8' width='%d' height='%d' fill='%s' stroke='%s' stroke-width='2'/>"
                 % (8 + i * sz, sz, sz, FILL if i < shaded else "#ffffff", LINE))
    return svg_wrap(W, sz + 16, "".join(s), "strip of %d squares, %d shaded" % (total, shaded))


# ============================================================ set 1: ratios from pictures
def set_pictures():
    its = []

    def cq(groups, q, right, wrong, e):
        its.append(mcq(fig(counters_svg(groups)) + q, right, wrong, e))

    cq([[(2, "red"), (3, "blue")]], "What is the ratio of red counters to blue counters?",
       R(2, 3), [R(3, 2), R(2, 5), R(3, 5)],
       "Count each colour: 2 red and 3 blue. Red is named first, so its number goes first: <b>2:3</b>. "
       "3:2 is blue to red, and 2:5 compares red to <b>all</b> the counters.")
    cq([[(4, "red"), (1, "blue")]], "What is the ratio of blue counters to red counters?",
       R(1, 4), [R(4, 1), R(1, 5), R(4, 5)],
       "There is 1 blue and 4 red. Blue is named first: <b>1:4</b>. 4:1 is red to blue, the wrong order.")
    cq([[(3, "yellow"), (5, "green")]], "What is the ratio of green counters to yellow counters?",
       R(5, 3), [R(3, 5), R(5, 8), R(3, 8)],
       "5 green and 3 yellow. Green comes first in the question: <b>5:3</b>. "
       "5:8 compares green to all 8 counters, not to yellow.")
    cq([[(2, "red"), (6, "blue")]], "What is the ratio of red counters to blue counters?",
       R(2, 6), [R(6, 2), R(2, 8), R(6, 8)],
       "2 red and 6 blue, so red to blue is <b>2:6</b>. 2:8 counts all the counters as the second term.")
    its.append(mcq(fig(strip_svg(3, 7)) + "What is the ratio of shaded squares to white squares?",
                   R(3, 4), [R(4, 3), R(3, 7), R(4, 7)],
                   "3 squares are shaded and 7 − 3 = 4 are white. Shaded to white is <b>3:4</b>. "
                   "3:7 compares the shaded squares to all 7 squares."))
    cq([[(2, "red"), (3, "blue"), (4, "yellow")]], "What is the ratio of blue counters to yellow counters?",
       R(3, 4), [R(4, 3), R(3, 9), R(2, 3)],
       "Use only the two colours in the question: 3 blue and 4 yellow, so <b>3:4</b>. "
       "2:3 is red to blue, and 3:9 is blue to all the counters.")
    cq([[(3, "red"), (4, "blue")]], "What is the ratio of red counters to <b>all</b> the counters?",
       R(3, 7), [R(3, 4), R(4, 7), R(7, 3)],
       "There are 3 + 4 = 7 counters, and 3 are red. Red to all is <b>3:7</b>. "
       "3:4 is red to blue (part to part).")
    cq([[(1, "red"), (2, "blue")]] * 3, "Look at one group. What is the ratio of red counters to blue counters in each group?",
       R(1, 2), [R(2, 1), R(1, 3), R(2, 3)],
       "Each group has 1 red and 2 blue: <b>1:2</b>. 2:1 is blue to red, 1:3 is red to all the counters "
       "in a group, and 2:3 is blue to all of them.")
    cq([[(1, "red"), (2, "blue")]] * 4, "What is the ratio of red counters to blue counters for <b>all</b> the groups?",
       R(4, 8), [R(8, 4), R(4, 12), R(5, 6)],
       "4 groups, each with 1 red and 2 blue: 4 × 1 = 4 red and 4 × 2 = 8 blue. Red to blue is <b>4:8</b>. "
       "5:6 adds 4 to each term of 1:2, but the groups multiply.")
    cq([[(3, "red"), (1, "blue")]] * 4, "For every 1 blue counter, how many red counters are there?",
       "3", ["12", "4", "16"],
       "Each group has 1 blue and 3 red, so there are <b>3</b> red for every 1 blue. 12 is all the red "
       "counters, 4 is the number of groups, and 16 is all the counters.")
    its.append(mcq("At a pet store, there are 5 fish for every 2 turtles. What is the ratio of turtles to fish?",
                   R(2, 5), [R(5, 2), R(2, 7), R(5, 7)],
                   "Turtles are named first, so their number goes first: <b>2:5</b>. 5:2 is fish to turtles."))
    its.append(mcq("A fruit bowl has 3 apples and 7 oranges. What is the ratio of oranges to apples?",
                   R(7, 3), [R(3, 7), R(7, 10), R(3, 10)],
                   "Oranges first: 7 oranges to 3 apples is <b>7:3</b>. 7:10 compares oranges to all 10 pieces of fruit."))
    its.append(mcq("The ratio of cats to dogs at a shelter is 3:5. What does this mean?",
                   "3 cats for every 5 dogs", ["5 cats for every 3 dogs", "3 cats and 8 dogs", "3 cats out of 5 animals"],
                   "The first term goes with the first word. 3:5 for cats to dogs means <b>3 cats for every 5 dogs</b>. "
                   "“3 out of 5 animals” would be part to whole."))
    its.append(mcq("Look at the letters in the word TORONTO. What is the ratio of vowels to consonants?",
                   R(3, 4), [R(4, 3), R(3, 7), R(4, 7)],
                   "TORONTO has 7 letters. The vowels are O, O, O (3). The consonants are T, R, N, T (4). "
                   "Vowels to consonants is <b>3:4</b>. 3:7 compares the vowels to all the letters."))
    its.append(mcq("Look at the letters in the word WINNIPEG. What is the ratio of consonants to vowels?",
                   R(5, 3), [R(3, 5), R(5, 8), R(3, 8)],
                   "WINNIPEG has 8 letters. Vowels: I, I, E (3). Consonants: W, N, N, P, G (5). "
                   "Consonants come first: <b>5:3</b>."))
    its.append(mcq(fig(strip_svg(4, 10)) + "What is the ratio of white squares to shaded squares?",
                   R(6, 4), [R(4, 6), R(6, 10), R(4, 10)],
                   "4 squares are shaded and 10 − 4 = 6 are white. White comes first: <b>6:4</b>. "
                   "4:6 is shaded to white, the wrong order."))
    its.append(mcq("A ringette team has 7 girls and 5 boys. What is the ratio of boys to girls?",
                   R(5, 7), [R(7, 5), R(5, 12), R(7, 12)],
                   "Boys first: 5 boys to 7 girls is <b>5:7</b>. 5:12 compares the boys to the whole team."))
    cq([[(3, "red"), (2, "blue"), (6, "green")]], "What is the ratio of red counters to green counters?",
       R(3, 6), [R(6, 3), R(3, 11), R(3, 2)],
       "3 red and 6 green, so red to green is <b>3:6</b>. 3:2 is red to blue, and 3:11 is red to all the counters.")
    its.append(mcq("On a pond there are 8 loons and 3 Canada geese. What is the ratio of geese to loons?",
                   R(3, 8), [R(8, 3), R(3, 11), R(8, 11)],
                   "Geese first: 3 geese to 8 loons is <b>3:8</b>. 8:3 is loons to geese."))
    its.append(mcq("Maya makes a bracelet. She puts on 2 red beads, then 5 white beads, and repeats this 4 times. "
                   "What is the ratio of red beads to white beads on the bracelet?",
                   R(8, 20), [R(20, 8), R(8, 28), R(6, 9)],
                   "4 repeats: 4 × 2 = 8 red and 4 × 5 = 20 white. Red to white is <b>8:20</b>. "
                   "6:9 adds 4 to each term, but 4 repeats means multiply by 4. 8:28 is red to all the beads."))
    assert len(its) == 20, len(its)
    return {"title": "Ratios from pictures: part to part", "items": its}


# ============================================================ set 2: equivalent ratios and ratio tables
def set_equivalent():
    its = []

    def miss(q, right, wrong, e, a=None):
        its.append(mcq(q, str(right), [str(w) for w in wrong], e))

    its.append(mcq("Which ratio is equivalent to 1:3?", R(2, 6), [R(3, 1), R(2, 4), R(1, 6)],
                   "Multiply <b>both</b> terms by 2: 1 × 2 = 2 and 3 × 2 = 6, so 1:3 = <b>2:6</b>. "
                   "2:4 adds 1 to both terms, and 1:6 changes only the second term."))
    its.append(mcq("Which ratio is equivalent to 2:5?", R(4, 10), [R(5, 2), R(4, 7), R(4, 5)],
                   "Multiply both terms by 2: 2 × 2 = 4 and 5 × 2 = 10, so 2:5 = <b>4:10</b>. "
                   "4:7 adds 2 to both terms, and 4:5 changes only the first term."))
    its.append(mcq("Which ratio is equivalent to 3:4?", R(9, 12), [R(6, 7), R(4, 3), R(9, 4)],
                   "Multiply both terms by 3: 3 × 3 = 9 and 4 × 3 = 12, so 3:4 = <b>9:12</b>. "
                   "6:7 adds 3 to both terms. Adding never makes an equivalent ratio."))
    for a, b, c, d, k, q, right, wrong, e in [
        (3, 4, None, 12, 3, "Find the missing number: 3:4 = ?:12", 9, [11, 16, 36],
         "4 × 3 = 12, so multiply the first term by 3 too: 3 × 3 = <b>9</b>. "
         "11 adds 8 to each term, and 16 uses the ratio the wrong way round (4:3)."),
        (2, 7, 6, None, 3, "Find the missing number: 2:7 = 6:?", 21, [11, 14, 42],
         "2 × 3 = 6, so multiply 7 by 3 too: 7 × 3 = <b>21</b>. 11 adds 4 to each term, "
         "and 42 multiplies 7 by 6 instead of by 3."),
        (5, 2, None, 10, 5, "Find the missing number: 5:2 = ?:10", 25, [13, 4, 50],
         "2 × 5 = 10, so multiply 5 by 5 too: 5 × 5 = <b>25</b>. 13 adds 8 to each term, "
         "and 4 uses the ratio the wrong way round (2:5)."),
        (4, 5, 20, None, 5, "Find the missing number: 4:5 = 20:?", 25, [21, 16, 100],
         "4 × 5 = 20, so multiply 5 by 5 too: 5 × 5 = <b>25</b>. 21 adds 16 to each term, "
         "and 100 multiplies 20 by 5."),
    ]:
        if c is None:
            assert F(a, b) == F(right, d) and d == b * k
        else:
            assert F(a, b) == F(c, right) and c == a * k
        miss(q, right, wrong, e)
    its.append(mcq("Find the missing number: 12:16 = 3:?", "4", ["7", "13", "48"],
                   "12 ÷ 4 = 3, so divide 16 by 4 too: 16 ÷ 4 = <b>4</b>. 7 subtracts 9 from each term, "
                   "and 13 subtracts 3 from 16."))
    assert F(12, 16) == F(3, 4)
    its.append(mcq("Which ratio is <b>not</b> equivalent to 2:3?", R(5, 6), [R(4, 6), R(6, 9), R(10, 15)],
                   "4:6, 6:9 and 10:15 multiply both terms of 2:3 by 2, 3 and 5. <b>5:6</b> adds 3 to both terms, "
                   "so it is not equivalent.", same_ok=True))

    def tab(names, rows, q, right, wrong, e, k):
        its.append(mcq(fig(ratio_table_svg(names, rows)) + q, str(right), [str(w) for w in wrong], e))

    # each table checked: every column equals the first column times a number
    def chk(rows, right):
        t = [[F(right) if x == "?" else F(x) for x in r] for r in rows]
        r0 = t[0][0] / t[1][0]
        assert all(t[0][i] / t[1][i] == r0 for i in range(len(t[0]))), rows

    rows = [["1", "2", "3", "5"], ["4", "8", "12", "?"]]
    chk(rows, 20)
    tab(["Tables", "Chairs"], rows, "Each table has the same number of chairs. What number is missing?", 20,
        [16, 13, 14],
        "1 table has 4 chairs, so 5 tables have 5 × 4 = <b>20</b> chairs. 16 is the next number after 12, "
        "but the table jumps from 3 to 5. 13 and 14 add 1 or 2 like the top row.", 4)
    rows = [["2", "4", "6", "?"], ["3", "6", "9", "15"]]
    chk(rows, 10)
    tab(["Red paint", "Blue paint"], rows, "Red and blue paint are mixed in the same ratio. What number is missing?", 10,
        [8, 12, 30],
        "The ratio is 2:3. 15 = 3 × 5, so the red is 2 × 5 = <b>10</b>. 8 is the next step of 2, but 15 skips "
        "a column after 9. 12 is 15 − 3.", 5)
    rows = [["3", "6", "9", "?"], ["12", "24", "36", "60"]]
    chk(rows, 15)
    tab(["Cups of flour", "Muffins"], rows, "A muffin recipe is made bigger. What number is missing?", 15,
        [12, 33, 20],
        "3 cups for 12 muffins. 60 = 12 × 5, so the flour is 3 × 5 = <b>15</b> cups. "
        "33 adds 24 to 9 because 60 is 24 more than 36, and 20 is 60 ÷ 3.", 5)
    rows = [["4", "2", "12"], ["10", "?", "30"]]
    chk(rows, 5)
    tab(["Laps", "Minutes"], rows, "A runner keeps the same speed. What number is missing?", 5,
        [8, 20, 6],
        "4 laps take 10 minutes. 2 laps is half of 4, so the time is half of 10: <b>5</b> minutes. "
        "8 takes 2 away like the top row, and 20 doubles instead of halving.", 0)
    rows = [["5", "10", "20"], ["2", "4", "?"]]
    chk(rows, 8)
    tab(["Granola bars", "Kids"], rows, "Each group of kids gets granola bars in the same ratio. What number is missing?", 8,
        [6, 14, 18],
        "10 to 20 is double, so 4 doubles too: 4 × 2 = <b>8</b>. 6 adds 2 like the step from 2 to 4, "
        "and 14 adds 10 like the top row.", 2)
    its.append(mcq("Liam says 2:3 = 4:5 because he added 2 to each term. Which ratio is really equivalent to 2:3?",
                   R(4, 6), [R(4, 5), R(6, 4), R(5, 6)],
                   "To get from 2 to 4, multiply by 2. Multiply 3 by 2 too: 3 × 2 = 6. So 2:3 = <b>4:6</b>. "
                   "Liam’s 4:5 comes from adding, which does not keep the ratio the same."))
    its.append(mcq("Write 6:8 in simplest form.", R(3, 4), [R(4, 3), R(2, 4), R(3, 8)],
                   "Divide both terms by 2: 6 ÷ 2 = 3 and 8 ÷ 2 = 4. 6:8 = <b>3:4</b>. 2:4 subtracts 4 from both terms, "
                   "and 3:8 divides only the first term."))
    its.append(mcq("Write 10:15 in simplest form.", R(2, 3), [R(3, 2), R(5, 10), R(2, 15)],
                   "Divide both terms by 5: 10 ÷ 5 = 2 and 15 ÷ 5 = 3. 10:15 = <b>2:3</b>. "
                   "5:10 subtracts 5 from both terms."))
    its.append(mcq("Which pair of ratios is equivalent?", "3:5 and 6:10", ["3:5 and 5:7", "3:5 and 5:3", "3:5 and 6:8"],
                   "Multiply both terms of 3:5 by 2: 6:10. So <b>3:5 and 6:10</b> are equivalent. "
                   "5:7 adds 2 to both terms, 5:3 swaps the order, and 6:8 adds 3 to both terms."))
    its.append(mcq("Which ratio is equivalent to 3:8 and has 15 as its first term?", R(15, 40),
                   [R(15, 20), R(15, 24), R(40, 15)],
                   "3 × 5 = 15, so multiply 8 by 5 too: 8 × 5 = 40. The ratio is <b>15:40</b>. "
                   "15:20 adds 12 to both terms, and 40:15 is in the wrong order."))
    its.append(mcq("Hana says 4:6 and 6:9 are equivalent. Is she right?", "Yes, both are equal to 2:3",
                   ["No, because 6 − 4 is not 9 − 6", "No, because 6:9 uses bigger numbers", "Yes, because 4 + 2 = 6"],
                   "Divide 4:6 by 2 to get 2:3. Divide 6:9 by 3 to get 2:3. Both are 2:3, so <b>yes</b>. "
                   "Equivalent ratios come from multiplying or dividing, not from adding or subtracting."))
    assert F(4, 6) == F(6, 9)
    order = [0, 1, 2, 15, 16, 3, 4, 5, 6, 7, 9, 10, 11, 12, 13, 14, 17, 8, 18, 19]
    its = [its[i] for i in order]
    assert len(its) == 20, len(its)
    return {"title": "Equivalent ratios and ratio tables", "items": its}


# ============================================================ set 3: rates
def set_rates(P):
    its = []

    def r(q, right, wrong, e, value):
        its.append(mcq(q, right, wrong, e, value=value))

    r("A car drives 180 km in 2 hours at a steady speed. How many kilometres does it drive in 1 hour?",
      "90 km", ["360 km", "178 km", "182 km"],
      "For 1 hour, divide: 180 ÷ 2 = <b>90 km</b>. The speed is 90 km/h. 360 km multiplies instead of dividing.", 90)
    r("4 pens cost $8. Each pen costs the same. What does 1 pen cost?", "$2", ["$32", "$4", "$12"],
      "Divide the cost by the number of pens: $8 ÷ 4 = <b>$2</b>. $32 multiplies, and $4 subtracts 8 − 4.", 2)
    r("6 muffins cost $9. What does 1 muffin cost?", "$1.50", ["$54", "$3", "$15"],
      "$9 ÷ 6 = <b>$1.50</b>. Check: 6 × $1.50 = $9. $3 subtracts 9 − 6, and $54 multiplies.", F(3, 2))
    r("A train goes 300 km in 3 hours at a steady speed. What is its speed?", "100 km/h",
      ["900 km/h", "297 km/h", "10 km/h"],
      "Speed is the distance in 1 hour: 300 ÷ 3 = <b>100 km/h</b>. 900 km/h multiplies, and 10 km/h drops a zero.", 100)
    r("A cyclist rides at 15 km/h. How far does she ride in 4 hours?", "60 km", ["19 km", "45 km", "75 km"],
      "15 km each hour for 4 hours: 15 × 4 = <b>60 km</b>. 19 km adds 15 + 4, and 45 km is only 3 hours.", 60)
    r("5 granola bars cost $4. What does 1 bar cost?", "80¢", ["$1.25", "$20", "$1"],
      "$4 ÷ 5 = 400¢ ÷ 5 = <b>80¢</b>. $1.25 divides 5 by 4 (the wrong way), and $1 subtracts 5 − 4.", F(4, 5))
    r("Apples cost 60¢ each. What do 5 apples cost?", "$3", ["65¢", "12¢", "$30"],
      "60¢ × 5 = 300¢ = <b>$3</b>. 65¢ adds 5 cents, 12¢ divides, and $30 writes 300¢ as $30.", 3)
    n, he, his = P.next()
    r("%s earns $24 for 3 hours of raking leaves. At the same rate, how much does %s earn in 5 hours?" % (n, he),
      "$40", ["$26", "$120", "$8"],
      "First the unit rate: $24 ÷ 3 = $8 per hour. Then 5 hours: 5 × $8 = <b>$40</b>. "
      "$26 adds 2 dollars for 2 more hours, $120 is $24 × 5, and $8 is only 1 hour.", 40)
    r("A printer prints 40 pages in 2 minutes. How many pages does it print in 5 minutes?", "100",
      ["43", "200", "20"],
      "Unit rate: 40 ÷ 2 = 20 pages per minute. 5 minutes: 5 × 20 = <b>100</b> pages. "
      "200 is 40 × 5, the pages for 10 minutes, and 20 is only 1 minute.", 100)
    its.append(mcq("Which juice boxes cost less per box?", "6 for $3",
                   ["4 for $2.40", "They cost the same per box", "You can’t tell"],
                   "Find the cost of 1 box. $3 ÷ 6 = 50¢. $2.40 ÷ 4 = 60¢. 50¢ is less, so <b>6 for $3</b> is the better buy."))
    a, ah, _ = P.next()
    b, bh, _ = P.next()
    its.append(mcq("%s runs 400 m in 2 minutes. %s runs 600 m in 4 minutes. Who runs faster?" % (a, b),
                   a, [b, "They run at the same speed", "You can’t tell"],
                   "Metres in 1 minute: %s 400 ÷ 2 = 200 m. %s 600 ÷ 4 = 150 m. 200 &gt; 150, so <b>%s</b> is faster, "
                   "even though %s runs farther." % (a, b, a, b)))
    r("A tap drips 30 mL of water every minute. How much water drips in 1 hour?", "1800 mL",
      ["90 mL", "180 mL", "2 mL"],
      "1 hour = 60 minutes. 30 × 60 = <b>1800 mL</b> (that is 1.8 L). 90 mL adds 30 + 60, "
      "and 180 mL is only 6 minutes.", 1800)
    its.append(mcq("A <b>rate</b> compares two amounts with different units. Which of these is a rate?",
                   "90 km in 1 hour", ["3 cups to 2 cups", "4 kg to 6 kg", "5 m to 8 m"],
                   "<b>90 km in 1 hour</b> compares kilometres with hours, two different units. "
                   "The others compare amounts with the same unit, so they are ratios but not rates."))
    r("3 kg of apples cost $7.50. What does 1 kg cost?", "$2.50", ["$22.50", "$4.50", "$10.50"],
      "$7.50 ÷ 3 = <b>$2.50</b> per kilogram. Check: 3 × $2.50 = $7.50. $4.50 subtracts 7.50 − 3, "
      "and $22.50 multiplies.", F(5, 2))
    r("A plane flies at 800 km/h. How far does it fly in 3 hours?", "2400 km", ["803 km", "1600 km", "3200 km"],
      "800 km each hour: 800 × 3 = <b>2400 km</b>. 803 km adds 800 + 3, and 1600 km is only 2 hours.", 2400)
    r("A bus travels at 60 km/h. How far does it go in 30 minutes?", "30 km", ["1800 km", "90 km", "120 km"],
      "30 minutes is half an hour, so the bus goes half of 60 km: <b>30 km</b>. "
      "1800 km multiplies 60 × 30, but 60 km is for 60 minutes, not 1 minute.", 30)
    r("A pack of 8 hot dogs costs $6. What does 1 hot dog cost?", "75¢", ["$1.33", "$48", "$2"],
      "$6 ÷ 8 = 600¢ ÷ 8 = <b>75¢</b>. $1.33 divides 8 by 6 (the wrong way), and $2 subtracts 8 − 6.", F(3, 4))
    r("Hockey cards are 3 for $2. How much do 24 cards cost?", "$16", ["$48", "$23", "$8"],
      "24 cards = 8 packs of 3 (24 ÷ 3 = 8). 8 × $2 = <b>$16</b>. $8 is the number of packs, "
      "and $48 multiplies 24 × $2 as if each card cost $2.", 16)
    n, he, his = P.next()
    r("%s’s family drives 270 km in 3 hours. At the same speed, how far do they drive in 5 hours?" % n,
      "450 km", ["272 km", "1350 km", "90 km"],
      "Unit rate: 270 ÷ 3 = 90 km/h. 5 hours: 5 × 90 = <b>450 km</b>. 272 km adds 2 for 2 more hours, "
      "and 1350 km is 270 × 5.", 450)
    its.append(mcq("Store A sells 3 notebooks for $4.50. Store B sells 5 of the same notebooks for $7. "
                   "Which store has the lower price per notebook?", "Store B",
                   ["Store A", "They are the same", "You can’t tell"],
                   "Store A: $4.50 ÷ 3 = $1.50. Store B: $7 ÷ 5 = $1.40. $1.40 is less, so <b>Store B</b>, "
                   "even though its total price is higher."))
    assert F(9, 2) / 3 == F(3, 2) and F(7, 5) == F(14, 10)
    order = [0, 1, 3, 2, 4, 6, 12, 5, 7, 8, 13, 14, 15, 9, 11, 16, 10, 17, 18, 19]
    its = [its[i] for i in order]
    assert len(its) == 20, len(its)
    return {"title": "Rates: km per hour and dollars per item", "items": its}


# ============================================================ set 4: double number lines
def set_double():
    its = []

    def dl(top, tops, bot, bots, q, right, wrong, e, value=None):
        """Check that the line is proportional, then add the question."""
        t = [x for x in tops]
        b = [x for x in bots]
        known = [(F(t[i]), F(b[i])) for i in range(1, len(t)) if t[i] not in ("?", "") and b[i] not in ("?", "")]
        k = known[0][0] / known[0][1]
        assert all(x / y == k for x, y in known), (tops, bots)
        assert F(t[0]) == 0 and F(b[0]) == 0
        miss = [i for i in range(1, len(t)) if "?" in (t[i], b[i])]
        assert len(miss) <= 1, (tops, bots)
        if len(miss) == 1 and value is not None:   # one missing value: it must be the answer
            i = miss[0]
            assert F(value) == (k * F(b[i]) if t[i] == "?" else F(t[i]) / k), (q, value)
        steps = [F(b[i]) - F(b[i - 1]) for i in range(1, len(b)) if b[i] not in ("?", "") and b[i - 1] not in ("?", "")]
        assert len(set(steps)) <= 1, bots
        its.append(mcq(fig(double_line_svg(top, tops, bot, bots)) + q, right, wrong, e, value=value))

    dl("km", ["0", "60", "?", "180"], "hours", ["0", "1", "2", "3"],
       "A car drives at a steady speed. How far does it go in 2 hours?", "120 km", ["61 km", "2 km", "90 km"],
       "1 hour is 60 km, so 2 hours is 2 × 60 = <b>120 km</b>. 61 km adds 1 instead of multiplying, "
       "and 90 km is half of 180, but 2 hours is not half of 3 hours.", 120)
    dl("tickets", ["0", "1", "2", "3", "4"], "$", ["0", "5", "10", "?", "20"],
       "Movie tickets all cost the same. What do 3 tickets cost?", "$15", ["$13", "$3", "$25"],
       "1 ticket costs $5, so 3 tickets cost 3 × $5 = <b>$15</b>. $13 adds 3 to $10, "
       "and $3 reads the number from the other line.", 15)
    dl("batches", ["0", "1", "2", "3"], "muffins", ["0", "12", "?", "36"],
       "Each batch makes the same number of muffins. How many muffins are in 2 batches?", "24",
       ["14", "2", "48"],
       "1 batch is 12 muffins, so 2 batches are 2 × 12 = <b>24</b>. 14 adds 2, and 48 is 4 batches.", 24)
    dl("hours", ["0", "1", "2", "3", "4"], "km", ["0", "?", "", "", "200"],
       "A cyclist rides 200 km in 4 hours at a steady speed. What is the speed in kilometres per hour?",
       "50 km/h", ["40 km/h", "800 km/h", "196 km/h"],
       "There are 4 equal jumps from 0 to 4 hours. 200 ÷ 4 = <b>50 km/h</b>. "
       "40 km/h divides by 5, the number of marks, but there are only 4 jumps.", 50)
    dl("pencils", ["0", "1", "2", "3", "4"], "$", ["0", "?", "", "", "6"],
       "4 pencils cost $6. What does 1 pencil cost?", "$1.50", ["$1.20", "$24", "$2"],
       "4 equal jumps share the $6: $6 ÷ 4 = <b>$1.50</b>. $1.20 divides by the 5 marks, "
       "and $2 subtracts 6 − 4.", F(3, 2))
    dl("hours", ["0", "1", "2", "3", "4", "5"], "km", ["0", "45", "", "", "", "?"],
       "A bus goes 45 km each hour. How far does it go in 5 hours?",
       "225 km", ["50 km", "180 km", "270 km"],
       "45 km for each hour: 5 × 45 = <b>225 km</b>. 50 km adds 45 + 5, 180 km is 4 hours, and 270 km is 6 hours.", 225)
    dl("hours", ["0", "2", "4", "6"], "km", ["0", "30", "?", "90"],
       "A hiker walks at a steady speed. How far does the hiker walk in 4 hours?", "60 km",
       ["32 km", "4 km", "120 km"],
       "Each jump is 2 hours and 30 km. 4 hours is 2 jumps: 2 × 30 = <b>60 km</b>. "
       "120 km multiplies 30 by 4, but 30 km is for 2 hours, not 1 hour.", 60)
    dl("litres", ["0", "5", "10", "15"], "$", ["0", "4", "?", "12"],
       "Fruit punch is sold by the litre. What do 10 L cost?", "$8", ["$9", "$10", "$40"],
       "Each jump is 5 L and $4. 10 L is 2 jumps: 2 × $4 = <b>$8</b>. $9 adds 5 to $4, "
       "$10 reads the other line, and $40 multiplies $4 by 10.", 8)
    dl("cups of flour", ["0", "2", "4", "?", "8"], "cookies", ["0", "24", "48", "72", "96"],
       "A cookie recipe is made bigger. How many cups of flour are needed for 72 cookies?", "6",
       ["5", "3", "70"],
       "The top line goes up by 2 cups for every 24 cookies: 0, 2, 4, <b>6</b>, 8. "
       "5 counts up by 1, and 3 is the number of jumps, not the cups.", 6)
    dl("juice", ["0", "1", "2", "3"], "water", ["0", "3", "6", "?"],
       "A juice mix uses cans of juice and cans of water in the same ratio. How many cans of water go with 3 cans of juice?",
       "9", ["7", "3", "12"],
       "1 can of juice goes with 3 cans of water, so 3 cans go with 3 × 3 = <b>9</b>. "
       "7 adds 1 like the top line, and 12 is one jump too far.", 9)
    dl("red paint", ["0", "2", "4", "6"], "blue paint", ["0", "5", "10", "?"],
       "Red and blue paint are mixed in the same ratio. How much blue paint goes with 6 cups of red?",
       "15 cups", ["12 cups", "6 cups", "20 cups"],
       "Each jump is 2 cups of red and 5 cups of blue. 6 cups of red is 3 jumps: 3 × 5 = <b>15 cups</b>. "
       "12 cups adds 2 to 10, and 20 cups is 4 jumps.", 15)
    dl("hours", ["0", "1", "2", "3", "4"], "$", ["0", "15", "30", "?", "60"],
       "A babysitter earns the same amount each hour. How much does she earn in 3 hours?", "$45",
       ["$33", "$3", "$90"],
       "$15 each hour: 3 × $15 = <b>$45</b>. $33 adds 3 to $30, and $90 doubles $45 as if each jump doubled.", 45)
    dl("cm on map", ["0", "1", "2", "3", "4"], "km", ["0", "25", "50", "?", "100"],
       "On a map, every 1 cm stands for the same distance. How many kilometres is 3 cm?", "75 km",
       ["53 km", "3 km", "150 km"],
       "1 cm stands for 25 km, so 3 cm stand for 3 × 25 = <b>75 km</b>. 53 km adds 3 to 50, "
       "and 150 km doubles 75.", 75)
    dl("hours", ["0", "1", "2", "3", "4"], "cm of snow", ["0", "3", "6", "9", "?"],
       "On a snow day, snow falls at the same rate all morning. How much snow falls in 4 hours?", "12 cm",
       ["13 cm", "4 cm", "15 cm"],
       "3 cm each hour: 4 × 3 = <b>12 cm</b>. 13 cm adds 4 to 9, and 15 cm is 5 hours.", 12)
    dl("apples", ["0", "4", "8", "12", "16"], "$", ["0", "3", "6", "?", "12"],
       "Apples are sold at the same price. What do 12 apples cost?", "$9", ["$10", "$12", "$36"],
       "Each jump is 4 apples and $3. 12 apples is 3 jumps: 3 × $3 = <b>$9</b>. $10 adds 4 to $6, "
       "$12 reads the other line, and $36 multiplies 12 × $3.", 9)
    dl("minutes", ["0", "10", "20", "30"], "pages", ["0", "4", "8", "?"],
       "Zoe reads at a steady speed. How many pages does she read in 30 minutes?", "12",
       ["18", "30", "120"],
       "Each jump is 10 minutes and 4 pages. 30 minutes is 3 jumps: 3 × 4 = <b>12</b> pages. "
       "18 adds 10 to 8, and 120 multiplies 4 × 30.", 12)
    dl("hours", ["0", "2", "4", "6"], "km", ["0", "", "", "90"],
       "A boat goes 90 km in 6 hours at a steady speed. What is its speed in kilometres per hour?", "15 km/h",
       ["30 km/h", "22.5 km/h", "540 km/h"],
       "90 km in 6 hours: 90 ÷ 6 = <b>15 km/h</b>. 30 km/h divides by the 3 jumps, but each jump is 2 hours. "
       "22.5 km/h divides by the 4 marks.", 15)
    dl("tickets", ["0", "3", "6", "9", "12"], "$", ["0", "8", "16", "24", "?"],
       "Ride tickets come in packs at the same price. What do 12 tickets cost?", "$32",
       ["$27", "$96", "$48"],
       "Each jump is 3 tickets and $8. 12 tickets is 4 jumps: 4 × $8 = <b>$32</b>. "
       "$27 adds 3 to $24, and $96 multiplies 12 × $8.", 32)
    dl("hours", ["0", "1", "2", "3", "4", "5"], "km", ["0", "", "", "?", "", "350"],
       "A car drives 350 km in 5 hours at a steady speed. How far does it go in 3 hours?", "210 km",
       ["70 km", "175 km", "280 km"],
       "First find 1 hour: 350 ÷ 5 = 70 km. Then 3 hours: 3 × 70 = <b>210 km</b>. 70 km is only 1 hour, "
       "175 km is half of 350 (that is 2.5 hours), and 280 km is 4 hours.", 210)
    dl("L of sap", ["0", "40", "80", "120", "?"], "L of syrup", ["0", "1", "2", "3", "4"],
       "It takes about 40 L of maple sap to make 1 L of maple syrup. How much sap is needed for 4 L of syrup?",
       "160 L", ["124 L", "44 L", "200 L"],
       "40 L of sap for each litre of syrup: 4 × 40 = <b>160 L</b>. 124 L adds 4 to 120, "
       "44 L adds 40 + 4, and 200 L is 5 L of syrup.", 160)
    order = [0, 1, 2, 9, 12, 13, 5, 11, 3, 4, 6, 7, 10, 14, 15, 17, 8, 19, 16, 18]
    its = [its[i] for i in order]
    assert len(its) == 20, len(its)
    return {"title": "Double number lines", "items": its}


# ============================================================ set 5: word problems
def set_problems(P):
    its = []

    def w(q, right, wrong, e, value=None):
        its.append(mcq(q, right, wrong, e, value=value))

    w("A juice mix uses 1 can of concentrate for every 3 cans of water. How many cans of water go with 4 cans of concentrate?",
      "12", ["6", "3", "16"],
      "1:3 = 4:? Multiply both terms by 4: 3 × 4 = <b>12</b> cans of water. "
      "6 adds 3 to both terms, and 16 is all the cans (4 + 12).", 12)
    w("A pancake recipe uses 2 cups of flour to make 8 pancakes. How much flour is needed for 24 pancakes?",
      "6 cups", ["18 cups", "3 cups", "12 cups"],
      "24 = 8 × 3, so use 3 times the flour: 2 × 3 = <b>6 cups</b>. 18 cups adds 16 because there are "
      "16 more pancakes, and 3 cups is only the number of batches.", 6)
    w("A lemonade mix uses 3 scoops for every 2 L of water. How many scoops are needed for 6 L of water?",
      "9", ["7", "4", "12"],
      "6 L = 2 L × 3, so the scoops are 3 × 3 = <b>9</b>. 7 adds 4 like the water, 4 uses the ratio the wrong "
      "way round (2 scoops for 3 L), and 12 multiplies 6 × 2.", 9)
    w("Trail mix has 2 cups of raisins for every 5 cups of peanuts. How many cups of peanuts go with 10 cups of raisins?",
      "25", ["13", "4", "35"],
      "10 = 2 × 5, so the peanuts are 5 × 5 = <b>25</b> cups. 13 adds 8 to both terms, 4 uses the ratio the wrong "
      "way round, and 35 is the whole mix.", 25)
    n, he, his = P.next()
    w("A fruit punch uses 2 L of juice for every 3 L of ginger ale. %s has 6 L of juice. How much ginger ale does %s need?"
      % (n, he), "9 L", ["7 L", "4 L", "15 L"],
      "6 = 2 × 3, so the ginger ale is 3 × 3 = <b>9 L</b>. 7 L adds 4, and 4 L uses the ratio the wrong way round. "
      "15 L is all the punch.", 9)
    w("On the Terry Fox Run, Leah walks 3 km each hour. How long does it take her to walk 12 km?",
      "4 hours", ["36 hours", "9 hours", "15 hours"],
      "Each hour is 3 km. 12 ÷ 3 = <b>4 hours</b>. 36 multiplies, 9 subtracts 12 − 3, and 15 adds.", 4)
    w("A car uses 6 L of gas for every 100 km. How much gas does it use to drive 300 km?",
      "18 L", ["9 L", "50 L", "24 L"],
      "300 km = 3 × 100 km, so the car uses 3 × 6 = <b>18 L</b>. 9 L adds 6 + 3, 50 L divides 300 by 6, "
      "and 24 L is enough for 400 km.", 18)
    w("3 hot chocolates cost $6.75. How much do 5 hot chocolates cost?", "$11.25", ["$8.75", "$2.25", "$33.75"],
      "1 hot chocolate: $6.75 ÷ 3 = $2.25. 5 hot chocolates: 5 × $2.25 = <b>$11.25</b>. "
      "$8.75 adds $2 for 2 more drinks, and $33.75 is $6.75 × 5.", F(45, 4))
    n, he, his = P.next()
    w("At the skating rink, %s skates 4 laps every 3 minutes. How many laps does %s skate in 12 minutes?" % (n, he),
      "16", ["13", "9", "48"],
      "12 = 3 × 4, so the laps are 4 × 4 = <b>16</b>. 13 adds 9, 9 uses the ratio the wrong way round "
      "(3 laps every 4 minutes), and 48 multiplies 4 × 12.", 16)
    w("A field trip needs 1 adult for every 6 students. 30 students are going. How many adults are needed?",
      "5", ["24", "180", "36"],
      "30 ÷ 6 = <b>5</b> groups of 6 students, so 5 adults. 24 subtracts 30 − 6, and 180 multiplies 30 × 6.", 5)
    n, he, his = P.next()
    w("On a canoe trip, %s paddles 6 km each hour. How far does %s paddle in 5 hours?" % (n, he),
      "30 km", ["11 km", "36 km", "24 km"],
      "6 km for each hour: 5 × 6 = <b>30 km</b>. 11 km adds 6 + 5, 36 km is 6 hours, and 24 km is 4 hours.", 30)
    w("A soup recipe for 8 people uses 6 cups of broth. How much broth is needed for 4 people?",
      "3 cups", ["2 cups", "12 cups", "4 cups"],
      "4 people is half of 8, so use half the broth: 6 ÷ 2 = <b>3 cups</b>. 2 cups subtracts 4 from 6, "
      "and 12 cups doubles instead of halving.", 3)
    its.append(mcq("Mix A uses 1 can of orange concentrate and 3 cans of water. Mix B uses 2 cans of concentrate and "
                   "5 cans of water. Which mix tastes more of orange?", "Mix B",
                   ["Mix A", "They taste the same", "You can’t tell"],
                   "Double Mix A to get the same concentrate: 1:3 = 2:6. Mix B is 2:5. Both have 2 cans of concentrate, "
                   "but Mix B has less water, so <b>Mix B</b> tastes more of orange."))
    assert F(2, 5) > F(1, 3)
    its.append(mcq("Store A sells 4 juice boxes for $3. Store B sells 6 juice boxes for $4.80. Which is the better buy?",
                   "Store A", ["Store B", "They cost the same per box", "You can’t tell"],
                   "Cost of 1 box. Store A: $3 ÷ 4 = 75¢. Store B: $4.80 ÷ 6 = 80¢. <b>Store A</b> costs less per box."))
    assert F(3, 4) < F(48, 10) / 6
    w("In a class, there are 2 boys for every 3 girls. There are 25 students. How many are girls?",
      "15", ["10", "22", "5"],
      "Each group has 2 + 3 = 5 students. 25 ÷ 5 = 5 groups. Girls: 5 × 3 = <b>15</b>. "
      "10 is the number of boys, 22 subtracts 25 − 3, and 5 is the number of groups.", 15)
    w("On a map, 1 cm stands for 5 km. Two towns are 7 cm apart on the map. How far apart are they really?",
      "35 km", ["12 km", "2 km", "30 km"],
      "Each centimetre is 5 km: 7 × 5 = <b>35 km</b>. 12 km adds 7 + 5, and 30 km is only 6 cm.", 35)
    n, he, his = P.next()
    w("%s earns $9 for every 2 hours of yard work. How much does %s earn in 8 hours?" % (n, he),
      "$36", ["$15", "$72", "$18"],
      "8 hours = 4 × 2 hours, so %s earns 4 × $9 = <b>$36</b>. $15 adds $6 for 6 more hours, "
      "$72 is $9 × 8, and $18 is only 4 hours." % he, 36)
    w("A muffin recipe uses 2 cups of flour for 12 muffins. The class needs 30 muffins. How much flour is needed?",
      "5 cups", ["20 cups", "6 cups", "4 cups"],
      "1 cup makes 12 ÷ 2 = 6 muffins. 30 ÷ 6 = <b>5 cups</b>. 20 cups adds 18 because there are 18 more "
      "muffins, 6 is the muffins for 1 cup, and 4 cups is only enough for 24 muffins.", 5)
    w("A bike shop has 3 helmets for every 4 bikes. There are 20 bikes. How many helmets are there?",
      "15", ["19", "27", "5"],
      "20 = 4 × 5, so the helmets are 3 × 5 = <b>15</b>. 19 subtracts 1 from 20 like 3 is 1 less than 4, "
      "27 uses the ratio the wrong way round, and 5 is the number of groups.", 15)
    assert F(3, 4) == F(15, 20)
    w("A juice mix uses 1 can of concentrate for every 4 cans of water. Kai wants to make 20 cans of juice in all. "
      "How many cans of concentrate does he need?", "4", ["5", "16", "80"],
      "Each batch is 1 + 4 = 5 cans. 20 ÷ 5 = 4 batches, so he needs <b>4</b> cans of concentrate (and 16 of water). "
      "5 divides 20 by 4, and 16 is the water.", 4)
    order = [0, 1, 2, 3, 4, 5, 6, 10, 9, 11, 7, 8, 15, 16, 12, 13, 17, 18, 14, 19]
    its = [its[i] for i in order]
    assert len(its) == 20, len(its)
    return {"title": "Word problems: recipes, juice mixes and trips", "items": its}


# ============================================================ lesson
def body_html():
    f_cnt = counters_svg([[(2, "red"), (3, "blue")]])
    f_grp = counters_svg([[(2, "red"), (3, "blue")]] * 3)
    f_tab = ratio_table_svg(["Juice (cans)", "Water (cans)"], [["1", "2", "3", "5"], ["3", "6", "9", "15"]])
    f_dl = double_line_svg("km", ["0", "60", "120", "180"], "hours", ["0", "1", "2", "3"])
    return (
        "<h2>What is a ratio?</h2>"
        "<p>A <b>ratio</b> compares two amounts. 2:3 is read “2 to 3”. "
        "The order matters: the first word in the question gives the first number.</p>"
        "<figure class='sn-fig'>" + f_cnt +
        "<figcaption>Red to blue is 2:3. Blue to red is 3:2. Both compare a part to a part.</figcaption></figure>"
        "<h2>Equivalent ratios</h2>"
        "<p>Equivalent ratios describe the same mix. To make one, <b>multiply</b> (or divide) both terms by the same number.</p>"
        "<figure class='sn-fig'>" + f_grp +
        "<figcaption>3 groups of 2 red and 3 blue: 2:3 = 6:9. Multiply both terms by 3, the number of groups.</figcaption></figure>"
        + ex("Example", "Find the missing number: 3:4 = ?:12",
             "4 × 3 = 12, so multiply the first term by 3 too: 3 × 3 = 9.", "9")
        + "<h2>Ratio tables</h2>"
        "<p>Each column of a ratio table is the first column multiplied by a number.</p>"
        "<figure class='sn-fig'>" + f_tab +
        "<figcaption>1 can of juice for every 3 cans of water. 15 = 3 × 5, so 5 cans of juice go with 15 cans of water.</figcaption></figure>"
        "<h2>Rates</h2>"
        "<p>A <b>rate</b> compares two amounts with different units, like kilometres and hours, or dollars and items. "
        "The amount for 1 is the <b>unit rate</b>. Divide to find it, then multiply.</p>"
        + ex("Example", "4 pens cost $8. What do 7 pens cost?",
             "1 pen: $8 ÷ 4 = $2. 7 pens: 7 × $2 = $14.", "$14")
        + "<h2>Double number lines</h2>"
        "<p>Two lines share the same marks. Each jump adds the same amount on the top line and on the bottom line.</p>"
        "<figure class='sn-fig'>" + f_dl +
        "<figcaption>60 km in 1 hour is 60 km/h. 3 hours is 3 jumps: 3 × 60 = 180 km.</figcaption></figure>"
        + "<h2>Common mistakes</h2>"
        + table(["Mistake", "What to do instead"], [
            ["3:4 = 11:12 (add 8 to both terms)", "Multiply both terms: 3:4 = 9:12"],
            ["Blue to red written as 2:3 when there are 2 red and 3 blue", "Follow the words: blue first, 3:2"],
            ["2 red and 3 blue, so red to blue is 2:5", "2:5 is red to all. Red to blue is 2:3"],
            ["180 km in 2 h = 360 km/h", "For 1 hour, divide: 180 ÷ 2 = 90 km/h"],
        ])
    )


FAQ = [
    {"q": "What do Grade 5 students learn about ratios and rates in Ontario?",
     "a": "In the Ontario Grade 5 math curriculum, students represent and create equivalent ratios and rates with tools such as counters, ratio tables and double number lines, in contexts like recipes, juice mixes, speeds and prices."},
    {"q": "What is the difference between a ratio and a rate?",
     "a": "A ratio compares two amounts, like 2 red counters to 3 blue counters (2:3). A rate compares amounts with different units, like 180 km in 2 hours, and the unit rate gives the amount for 1, like 90 km/h."},
    {"q": "How do you find an equivalent ratio?",
     "a": "Multiply or divide both terms by the same number: 3:4 = 9:12 because both terms are multiplied by 3. Adding the same number to both terms does not make an equivalent ratio."},
    {"q": "How does a double number line help with rates?",
     "a": "It shows two amounts on lines with the same marks, so each jump adds the same amount on both lines. If 1 hour matches 60 km, then 3 hours matches 3 × 60 = 180 km."},
]


def mark_large(u, pattern):
    """Tag pictures that must print larger (ratio tables, double number lines, rows of counters, strips)."""
    rx = re.compile(r"<svg (?=[^>]*aria-label='" + pattern + ")")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u


def gen():
    rnd = random.Random(45810)
    P = People(rnd)
    sets = [set_pictures(), set_equivalent(), set_rates(P), set_double(), set_problems(P)]
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
        "country": "ca-on", "subject": "math", "grade": "grade-5", "slug": "ratios-and-rates", "sort": 10,
        "updated": UPDATED, "pdf_url": "",
        "title": "Ratios and Rates: Equivalent Ratios, Ratio Tables and Double Number Lines",
        "seo_title": "Grade 5 Ratios and Rates Worksheets (Ontario Math): Free with Answer Key",
        "short_title": "Ratios and rates",
        "domain": "Number",
        "standard_code": "Grade 5: B2.9",
        "standard_url": "https://www.dcp.edu.gov.on.ca/en/curriculum/elementary-mathematics",
        "standard_text": "Represent and create equivalent ratios and rates, using a variety of tools and models, in various contexts",
        "meta_desc": "Free Grade 5 ratios and rates worksheets for the Ontario curriculum: ratios from pictures, equivalent ratios and ratio tables, km per hour and price per item, double number lines, and recipe and juice mix word problems. 100 math questions with an answer key.",
        "key_big": "Equivalent ratios come from multiplying both terms by the same number: 3:4 = 9:12.",
        "key_sub": "Never add the same number to both terms (3:4 is not 11:12). Keep the order of the words: 2 red and 3 blue is red to blue 2:3, blue to red 3:2. For a rate, find the amount for 1 first: 180 km in 2 hours is 90 km/h.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }
    return mark_large(u, "(ratio table|double number line|counters|strip)")


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
