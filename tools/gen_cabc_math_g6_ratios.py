# -*- coding: utf-8 -*-
"""
BC Grade 6 Math: Ratios (BC Mathematics Curriculum, Grade 6: Number — introduction to ratios)
  python3 tools/gen_cabc_math_g6_ratios.py
Write ratios from pictures (part to part and part to whole), equivalent ratios and simplest form,
ratio tables and double number lines, comparing ratios, then word problems (recipes and teams) in BC contexts.
Wrong answers come from real mistakes: terms in the wrong order, part to part used as part to whole,
adding instead of multiplying, "bigger numbers mean stronger".
Every answer is checked with fractions.Fraction (never float).
Canadian English, dollars and cents, metric units, SI number spacing. HTML attributes use single quotes.
"""
import json, os, random, re
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "ca-bc", "math", "grade-6")
SLUG = "ratios"
UPDATED = "2026-11-02"
NBSP = "\u00a0"
FILL = "#4fae74"
LINE = "#2b2b2b"
THIN = "#8a8a8a"
RED = "#d6453b"
BLUE = "#2f6fc0"
YELLOW = "#e8b923"
FONT = "Arial, Helvetica, sans-serif"
CANT = "You can’t tell"


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
    return F(p) * F(n) / 100


def fr(a, b):
    return "<span class='fr'><span class='fn'>%s</span><span class='fd'>%s</span></span>" % (a, b)


def R(*t):
    return ":".join(str(x) for x in t)


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
        v = val(right)
        assert v is not None and v[0] == F(value), (q, right, value)
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
COL = {"red": RED, "blue": BLUE, "yellow": YELLOW, "green": FILL}


def counters_svg(*groups):
    """One row of counters. groups: (count, colour) pairs in order. Blue counters have a white ring and
    yellow counters a dark dot, so the colours stay different in black-and-white print."""
    r, gap = 13, 7
    seq = [c for n, c in groups for _ in range(n)]
    n = len(seq)
    W = 8 + n * (2 * r + gap) - gap + 8
    s = []
    for i, c in enumerate(seq):
        cx = 8 + r + i * (2 * r + gap)
        s.append("<circle cx='%d' cy='%d' r='%d' fill='%s' stroke='%s' stroke-width='2'/>" % (cx, 8 + r, r, COL[c], LINE))
        if c == "blue":
            s.append("<circle cx='%d' cy='%d' r='5' fill='#fff'/>" % (cx, 8 + r))
        if c == "yellow":
            s.append("<circle cx='%d' cy='%d' r='3' fill='%s'/>" % (cx, 8 + r, LINE))
    label = "counters: " + ", ".join("%d %s" % (k, c) for k, c in groups)
    return svg_wrap(W, 2 * r + 16, "".join(s), label)


def grid_svg(rows, cols, shaded):
    """A rows × cols grid of squares; the first `shaded` squares (row by row) are shaded."""
    sq = 30
    W, H = cols * sq + 8, rows * sq + 8
    s = []
    for i in range(rows * cols):
        x, y = 4 + (i % cols) * sq, 4 + (i // cols) * sq
        s.append("<rect x='%d' y='%d' width='%d' height='%d' fill='%s' stroke='%s' stroke-width='2'/>"
                 % (x, y, sq, sq, FILL if i < shaded else "#ffffff", LINE))
    return svg_wrap(W, H, "".join(s), "grid of %d squares, %d shaded" % (rows * cols, shaded))


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



# ============================================================ set 1: writing ratios from pictures
def set_pictures():
    its = []
    its.append(mcq(fig(counters_svg((3, "red"), (4, "blue"))) + "What is the ratio of red counters to blue counters?",
                   R(3, 4), [R(4, 3), R(3, 7), R(4, 7)],
                   "3 red and 4 blue. Red is named first, so the ratio is <b>3:4</b>. "
                   "4:3 is blue to red, and 3:7 is red to <b>all</b> the counters."))
    its.append(mcq(fig(counters_svg((5, "red"), (2, "blue"))) + "What is the ratio of blue counters to red counters?",
                   R(2, 5), [R(5, 2), R(2, 7), R(5, 7)],
                   "Blue is named first: 2 blue, then 5 red, so <b>2:5</b>. "
                   "5:2 has the terms in the wrong order, and 2:7 compares blue to all 7 counters."))
    its.append(mcq(fig(counters_svg((4, "red"), (3, "blue"))) + "What is the ratio of red counters to <b>all</b> the counters?",
                   R(4, 7), [R(4, 3), R(7, 4), R(3, 7)],
                   "This is part to whole. There are 4 + 3 = 7 counters, and 4 are red: <b>4:7</b>. "
                   "4:3 is red to blue (part to part), and 3:7 is blue to all."))
    its.append(mcq(fig(counters_svg((2, "yellow"), (6, "blue"))) + "What is the ratio of blue counters to all the counters?",
                   R(6, 8), [R(6, 2), R(8, 6), R(2, 8)],
                   "There are 2 + 6 = 8 counters, and 6 are blue: <b>6:8</b>. "
                   "6:2 is blue to yellow (part to part), and 8:6 has the terms in the wrong order."))
    its.append(mcq(fig(counters_svg((3, "green"), (5, "blue"))) + "What is the ratio of blue counters to green counters?",
                   R(5, 3), [R(3, 5), R(5, 8), R(3, 8)],
                   "Blue is named first: 5 blue to 3 green, so <b>5:3</b>. "
                   "3:5 is green to blue, and 5:8 is blue to all the counters."))
    its.append(mcq(fig(grid_svg(2, 4, 3)) + "What is the ratio of shaded squares to unshaded squares?",
                   R(3, 5), [R(3, 8), R(5, 3), R(5, 8)],
                   "3 squares are shaded and 8 − 3 = 5 are not: <b>3:5</b>. "
                   "3:8 is shaded to the whole grid (part to whole)."))
    its.append(mcq(fig(grid_svg(3, 3, 4)) + "What is the ratio of shaded squares to <b>all</b> the squares?",
                   R(4, 9), [R(4, 5), R(9, 4), R(5, 9)],
                   "The grid has 3 × 3 = 9 squares, and 4 are shaded: <b>4:9</b>. "
                   "4:5 is shaded to unshaded, and 5:9 is unshaded to all."))
    its.append(mcq(fig(grid_svg(2, 5, 6)) + "What is the ratio of unshaded squares to shaded squares?",
                   R(4, 6), [R(6, 4), R(4, 10), R(6, 10)],
                   "10 − 6 = 4 squares are unshaded and 6 are shaded. Unshaded comes first: <b>4:6</b>. "
                   "6:4 is shaded to unshaded, and 4:10 is unshaded to all."))
    its.append(mcq(fig(grid_svg(1, 7, 5)) + "What is the ratio of shaded squares to unshaded squares?",
                   R(5, 2), [R(2, 5), R(5, 7), R(2, 7)],
                   "5 shaded and 7 − 5 = 2 unshaded: <b>5:2</b>. "
                   "2:5 has the terms in the wrong order, and 5:7 is shaded to all."))
    its.append(mcq(fig(counters_svg((2, "red"), (3, "blue"), (4, "yellow"))) +
                   "What is the ratio of red to blue to yellow counters?",
                   R(2, 3, 4), [R(4, 3, 2), R(2, 4, 3), R(2, 3, 9)],
                   "Keep the order of the words: 2 red, 3 blue, 4 yellow, so <b>2:3:4</b>. "
                   "4:3:2 is yellow to blue to red, and 9 is the total, not the yellow."))
    its.append(mcq(fig(counters_svg((3, "red"), (1, "blue"), (4, "yellow"))) +
                   "What is the ratio of blue counters to all the counters?",
                   R(1, 8), [R(1, 7), R(8, 1), R(1, 4)],
                   "There are 3 + 1 + 4 = 8 counters, and 1 is blue: <b>1:8</b>. "
                   "1:7 is blue to the other counters (part to part), and 1:4 is blue to yellow."))
    its.append(mcq(fig(counters_svg((4, "red"), (2, "blue"))) + "Which statement about the counters is <b>not</b> true?",
                   "Blue to red is 4:2", ["Red to blue is 4:2", "Blue to all is 2:6", "Red to all is 4:6"],
                   "There are 4 red and 2 blue. Blue to red puts blue first, so it is 2:4, not 4:2. "
                   "The false statement is <b>Blue to red is 4:2</b>. The other three are true."))
    its.append(mcq(fig(counters_svg((6, "red"), (2, "blue"))) +
                   "Finish the sentence: “For every 1 blue counter, there are ___ red counters.”",
                   "3", ["6", "4", "8"],
                   "6 red and 2 blue. Split them into 2 equal groups: each group has 1 blue and 6 ÷ 2 = <b>3</b> red. "
                   "6 is all the red, 4 is the difference 6 − 2, and 8 is all the counters.", value=3))
    its.append(mcq(fig(counters_svg((2, "red"), (8, "blue"))) +
                   "Finish the sentence: “For every 1 red counter, there are ___ blue counters.”",
                   "4", ["8", "6", "10"],
                   "8 blue shared between 2 red is 8 ÷ 2 = <b>4</b> blue for each red. "
                   "8 is all the blue, 6 is the difference 8 − 2, and 10 is all the counters.", value=4))
    its.append(mcq(fig(grid_svg(2, 6, 4)) + "What fraction of the grid is shaded?",
                   fr(4, 12), [fr(4, 8), fr(8, 12), fr(12, 4)],
                   "A fraction is part to whole. 4 of the 2 × 6 = 12 squares are shaded: <b>%s</b>. "
                   "%s compares shaded to unshaded (part to part), and %s is the unshaded part."
                   % (fr(4, 12), fr(4, 8), fr(8, 12)), value=F(4, 12)))
    its.append(mcq(fig(counters_svg((3, "red"), (6, "blue"))) + "Which sentence describes the counters?",
                   "For every 1 red, there are 2 blue",
                   ["For every 2 red, there is 1 blue", "For every 1 red, there are 3 blue",
                    "For every 1 red, there are 6 blue"],
                   "3 red and 6 blue. Make 3 groups: each has 1 red and 6 ÷ 3 = 2 blue, so "
                   "<b>for every 1 red, there are 2 blue</b>. “2 red for 1 blue” has the order backwards."))
    its.append(mcq(fig(counters_svg((5, "red"), (3, "blue"))) +
                   "Kai adds 1 more blue counter. What is the new ratio of red to blue counters?",
                   R(5, 4), [R(6, 4), R(5, 3), R(5, 9)],
                   "Blue goes from 3 to 3 + 1 = 4. Red stays 5. The new ratio is <b>5:4</b>. "
                   "6:4 adds 1 to the red too, and 5:9 is red to all the counters."))
    its.append(mcq(fig(grid_svg(3, 4, 9)) + "What is the ratio of unshaded squares to all the squares?",
                   R(3, 12), [R(3, 9), R(9, 12), R(12, 3)],
                   "The grid has 3 × 4 = 12 squares. 12 − 9 = 3 are unshaded: <b>3:12</b>. "
                   "3:9 is unshaded to shaded, and 9:12 is shaded to all."))
    its.append(mcq(fig(counters_svg((4, "red"), (2, "blue"), (3, "yellow"))) +
                   "Which two colours are in the ratio 2:1?",
                   "red to blue", ["blue to red", "yellow to blue", "red to yellow"],
                   "Red to blue is 4:2. For every 2 red there is 1 blue, so 4:2 is the same as 2:1: <b>red to blue</b>. "
                   "Blue to red is 2:4, which is 1:2, the wrong order."))
    its.append(mcq(fig(counters_svg((3, "red"), (5, "blue"))) +
                   "Nadia says the ratio of red counters to blue counters is 5:3. What mistake did she make?",
                   "She wrote the terms in the wrong order",
                   ["She compared red with all the counters", "She counted the red counters wrong", "She made no mistake"],
                   "There are 3 red and 5 blue. Red is named first, so the ratio is 3:5. "
                   "Nadia wrote 5:3, which is blue to red: <b>she wrote the terms in the wrong order</b>."))
    assert len(its) == 20, len(its)
    return {"title": "Writing ratios from pictures: part to part and part to whole", "items": its}


# ============================================================ set 2: equivalent ratios
def set_equivalent():
    its = []
    its.append(mcq("Which ratio is equivalent to 1:3?", R(2, 6), [R(2, 4), R(3, 1), R(2, 3)],
                   "Multiply <b>both</b> terms by 2: 1 × 2 = 2 and 3 × 2 = 6, so 1:3 = <b>2:6</b>. "
                   "2:4 adds 1 to both terms, and 2:3 multiplies only the first term."))
    its.append(mcq("Which ratio is equivalent to 2:5?", R(4, 10), [R(4, 7), R(5, 2), R(4, 5)],
                   "2 × 2 = 4 and 5 × 2 = 10, so 2:5 = <b>4:10</b>. "
                   "4:7 adds 2 to both terms, and 4:5 doubles only the 2."))
    its.append(mcq("Which ratio is equivalent to 3:4?", R(9, 12), [R(6, 7), R(4, 3), R(9, 4)],
                   "3 × 3 = 9 and 4 × 3 = 12, so 3:4 = <b>9:12</b>. 6:7 adds 3 to both terms, "
                   "and 9:4 multiplies only the 3."))
    its.append(mcq("Multiply both terms of 4:7 by 3. What equivalent ratio do you get?", R(12, 21),
                   [R(12, 7), R(7, 10), R(21, 12)],
                   "4 × 3 = 12 and 7 × 3 = 21: <b>12:21</b>. 12:7 forgets the second term, "
                   "7:10 adds 3 instead of multiplying, and 21:12 has the terms in the wrong order."))
    its.append(mcq("Find the missing term: 2:3 = ?:12", "8", ["11", "4", "18"],
                   "3 × 4 = 12, so multiply the first term by 4 too: 2 × 4 = <b>8</b>. "
                   "11 adds 9, like 3 + 9 = 12, but equivalent ratios never come from adding. "
                   "4 is only the number you multiply by.", value=8))
    its.append(mcq("Find the missing term: 5:2 = 15:?", "6", ["12", "3", "30"],
                   "5 × 3 = 15, so multiply 2 by 3 too: <b>6</b>. 12 adds 10 like 5 + 10 = 15, "
                   "3 is the number you multiply by, and 30 multiplies 15 by 2.", value=6))
    its.append(mcq("Find the missing term: 4:9 = 20:?", "45", ["25", "5", "36"],
                   "4 × 5 = 20, so 9 × 5 = <b>45</b>. 25 adds 16 to both terms, "
                   "5 is the number you multiply by, and 36 multiplies 9 by 4.", value=45))
    its.append(mcq("Find the missing term: 6:8 = 3:?", "4", ["5", "2", "16"],
                   "6 ÷ 2 = 3, so divide 8 by 2 too: <b>4</b>. 5 subtracts 3 from both terms, "
                   "2 is the number you divide by, and 16 multiplies instead of dividing.", value=4))
    its.append(mcq("Write 6:9 in simplest form.", R(2, 3), [R(3, 2), R(3, 6), R(2, 9)],
                   "3 is the greatest number that divides both 6 and 9. 6 ÷ 3 = 2 and 9 ÷ 3 = 3: <b>2:3</b>. "
                   "3:6 subtracts 3 from both terms, and 2:9 divides only the first term."))
    its.append(mcq("Write 12:16 in simplest form.", R(3, 4), [R(4, 3), R(6, 10), R(3, 16)],
                   "Divide both terms by 4: 12 ÷ 4 = 3 and 16 ÷ 4 = 4, so <b>3:4</b>. "
                   "6:10 subtracts 6 from both terms, and 3:16 divides only the 12."))
    its.append(mcq("Write 16:12 in simplest form.", R(4, 3), [R(3, 4), R(4, 12), R(8, 4)],
                   "Divide both terms by 4: 16 ÷ 4 = 4 and 12 ÷ 4 = 3, so <b>4:3</b>. "
                   "3:4 has the terms in the wrong order, and 8:4 subtracts 8 from both terms."))
    its.append(mcq("Which ratio is <b>not</b> equivalent to 2:3?", R(5, 6), [R(4, 6), R(6, 9), R(10, 15)],
                   "4:6, 6:9 and 10:15 are 2:3 times 2, 3 and 5. <b>5:6</b> adds 3 to both terms, "
                   "so it is not equivalent.", same_ok=True))
    its.append(mcq("Which ratio is <b>not</b> equivalent to 4:5?", R(6, 7), [R(8, 10), R(12, 15), R(40, 50)],
                   "8:10, 12:15 and 40:50 are 4:5 times 2, 3 and 10. <b>6:7</b> adds 2 to both terms, "
                   "so it is not equivalent.", same_ok=True))
    its.append(mcq("Liam says 3:4 = 5:6 because he added 2 to both terms. Is he right?",
                   "No. Multiply both terms: 3:4 = 6:8",
                   ["Yes. Add the same number to both terms", "Yes. Both terms went up by 2", "No. 3:4 = 5:8"],
                   "Equivalent ratios come from <b>multiplying</b> (or dividing) both terms by the same number. "
                   "3:4 × 2 = 6:8. Adding 2 gives 5:6, which is a different ratio."))
    its.append(mcq("Are 2:5 and 6:15 equivalent ratios?",
                   "Yes. 2:5 × 3 = 6:15",
                   ["No. 6 − 2 is not the same as 15 − 5", "No. 6:15 has bigger numbers", "No. 2:5 = 6:9"],
                   "2 × 3 = 6 and 5 × 3 = 15, so <b>yes</b>, they are equivalent. "
                   "Checking by subtracting does not work for ratios."))
    its.append(mcq("Find the missing term: ?:7 = 18:21", "6", ["4", "3", "54"],
                   "7 × 3 = 21, so the missing term times 3 is 18. 18 ÷ 3 = <b>6</b>. "
                   "4 subtracts 14 from both terms, 3 is the number you multiply by, and 54 multiplies 18 by 3.", value=6))
    its.append(mcq("Find the missing term: 7:3 = 28:?", "12", ["24", "4", "84"],
                   "7 × 4 = 28, so 3 × 4 = <b>12</b>. 24 adds 21 like 7 + 21 = 28, "
                   "and 84 multiplies 28 by 3.", value=12))
    its.append(mcq("Which pair shows two equivalent ratios?",
                   "3:5 and 9:15", ["3:5 and 5:7", "3:5 and 5:3", "3:5 and 6:8"],
                   "3 × 3 = 9 and 5 × 3 = 15, so <b>3:5 and 9:15</b> are equivalent. "
                   "5:7 and 6:8 add the same number to both terms, and 5:3 has the terms in the other order."))
    its.append(mcq("Which ratio is equivalent to 12:18 <b>and</b> in simplest form?", R(2, 3),
                   [R(6, 9), R(4, 6), R(3, 2)],
                   "Divide both terms by 6, the greatest common factor: 12:18 = <b>2:3</b>. "
                   "6:9 and 4:6 are equivalent too, but they can still be simplified. 3:2 is the wrong order.",
                   same_ok=True))
    its.append(mcq("Which list shows ratios equivalent to 3:5?",
                   "6:10, 9:15, 12:20", ["4:6, 5:7, 6:8", "6:5, 9:5, 12:5", "5:3, 10:6, 15:9"],
                   "Multiply both terms by 2, 3 and 4: <b>6:10, 9:15, 12:20</b>. "
                   "4:6, 5:7, 6:8 adds 1 each time, 6:5 multiplies only the first term, "
                   "and 5:3, 10:6, 15:9 has the terms in the wrong order."))
    assert len(its) == 20, len(its)
    return {"title": "Equivalent ratios and simplest form", "items": its}


# ============================================================ set 3: ratio tables
def set_tables():
    its = []
    its.append(mcq(fig(ratio_table_svg(["Juice (cups)", "Water (cups)"], [["1", "2", "3"], ["3", "6", "?"]])) +
                   "The table shows juice mixed with water. What number is missing?",
                   "9", ["7", "12", "18"],
                   "The top row is 1 × 1, 1 × 2, 1 × 3. Do the same to the bottom row: 3 × 3 = <b>9</b>. "
                   "7 adds 1 like the top row, 12 doubles 6, and 18 multiplies 6 by 3.", value=9))
    its.append(mcq(fig(ratio_table_svg(["Canoes", "People"], [["1", "2", "3", "4"], ["2", "4", "6", "?"]])) +
                   "Each canoe holds the same number of people. What number is missing?",
                   "8", ["7", "12", "24"],
                   "Each canoe holds 2 people, so 4 canoes hold 4 × 2 = <b>8</b>. "
                   "7 adds 1 like the top row, 12 doubles 6, and 24 multiplies 6 by 4.", value=8))
    its.append(mcq(fig(ratio_table_svg(["Bags", "Apples"], [["2", "4", "6"], ["5", "10", "?"]])) +
                   "The table shows bags of apples. What number is missing?",
                   "15", ["12", "20", "30"],
                   "6 = 2 × 3, so multiply 5 by 3 too: <b>15</b>. "
                   "12 adds 2 like the top row, 20 doubles 10, and 30 multiplies 5 by 6.", value=15))
    its.append(mcq(fig(ratio_table_svg(["Eggs", "Milk (cups)"], [["2", "4", "?"], ["1", "2", "5"]])) +
                   "A pancake recipe uses eggs and milk in the same ratio. What number is missing?",
                   "10", ["7", "5", "6"],
                   "There are 2 eggs for every 1 cup of milk. 5 cups need 5 × 2 = <b>10</b> eggs. "
                   "7 adds 3 like 2 + 3 = 5, 5 copies the milk, and 6 is only the next step after 4.", value=10))
    its.append(mcq(fig(ratio_table_svg(["Pages", "Minutes"], [["24", "12", "?"], ["8", "4", "2"]])) +
                   "Kai reads at a steady pace. What number is missing?",
                   "6", ["10", "8", "3"],
                   "The minutes are halved: 4 ÷ 2 = 2. Halve the pages too: 12 ÷ 2 = <b>6</b>. "
                   "10 subtracts 2 like the minutes row, 8 subtracts 4, and 3 divides 12 by 4.", value=6))
    its.append(mcq(fig(ratio_table_svg(["Hours", "Distance (km)"], [["1", "3", "5"], ["4", "12", "?"]])) +
                   "Sofia hikes at a steady pace. What number is missing?",
                   "20", ["14", "16", "60"],
                   "She hikes 4 km in 1 hour. In 5 hours: 5 × 4 = <b>20 km</b>. "
                   "14 adds 2 like the hours row, 16 adds one more 4, and 60 multiplies 12 by 5.", value=20))
    its.append(mcq(fig(ratio_table_svg(["Red beads", "White beads"], [["3", "6", "9"], ["2", "4", "6"]])) +
                   "What ratio of red beads to white beads does the table show?",
                   R(3, 2), [R(2, 3), R(3, 5), R(3, 6)],
                   "Every column is 3 red to 2 white, times a number: <b>3:2</b>. "
                   "2:3 has the terms in the wrong order, 3:5 is red to all the beads, "
                   "and 3:6 reads along the top row instead of down a column."))
    its.append(mcq("A ratio table shows the ratio 2:7. Which column could be in the table?",
                   "8 and 28", ["8 and 13", "7 and 2", "4 and 9"],
                   "Multiply both terms by 4: 2 × 4 = 8 and 7 × 4 = 28, so <b>8 and 28</b>. "
                   "“8 and 13” and “4 and 9” add the same number to both terms, and “7 and 2” is the wrong order."))
    its.append(mcq("Which is a ratio table?",
                   "1, 2, 3 and 6, 12, 18",
                   ["1, 2, 3 and 6, 7, 8", "2, 4, 6 and 3, 5, 7", "1, 2, 4 and 6, 12, 18"],
                   "In a ratio table, every column is the first column times a number. "
                   "1:6, 2:12 and 3:18 are all 1:6 times 1, 2 and 3, so <b>1, 2, 3 and 6, 12, 18</b>. "
                   "The others add to a row, or (in the last one) 4:18 is not 1:6."))
    its.append(mcq(fig(ratio_table_svg(["Rice (cups)", "Servings"], [["2", "4", "6", "8"], ["6", "12", "?", "24"]])) +
                   "A rice recipe makes servings in the same ratio. What number is missing?",
                   "18", ["14", "36", "16"],
                   "6 = 2 × 3, so multiply 6 by 3 too: 6 × 3 = <b>18</b> servings. "
                   "14 adds 2 like the top row, 36 multiplies 6 by 6, and 16 adds 4 to 12.", value=18))
    its.append(mcq(fig(double_line_svg("Laps", ["0", "2", "4", "6"], "Minutes", ["0", "5", "10", "?"])) +
                   "Owen runs laps at a steady pace. How many minutes does 6 laps take?",
                   "15", ["12", "20", "30"],
                   "2 laps take 5 minutes. 6 laps is 3 × 2 laps, so 3 × 5 = <b>15</b> minutes. "
                   "12 adds 2 like the laps row, 20 doubles 10, and 30 multiplies 5 by 6.", value=15))
    its.append(mcq(fig(double_line_svg("Tickets", ["0", "1", "2", "3"], "Cost", ["$0", "$4", "?", "$12"])) +
                   "Each ticket for the school play costs the same. What is the cost of 2 tickets?",
                   "$8", ["$5", "$6", "$24"],
                   "1 ticket costs $4, so 2 tickets cost 2 × $4 = <b>$8</b>. "
                   "$5 adds 1 like the ticket row, $6 is half of $12, and $24 doubles the $12 instead of the $4.",
                   value=8))
    its.append(mcq(fig(ratio_table_svg(["Kids", "Adults"], [["4", "8", "12", "?"], ["1", "2", "3", "10"]])) +
                   "On a field trip there are 4 kids for every adult. How many kids go with 10 adults?",
                   "40", ["16", "19", "14"],
                   "Each adult has 4 kids, so 10 adults go with 10 × 4 = <b>40</b> kids. "
                   "16 just counts on by 4, 19 adds 7 like 3 + 7 = 10, and 14 adds 10 to 4.", value=40))
    its.append(mcq(fig(ratio_table_svg(["Muffins", "Eggs"], [["12", "6", "?"], ["4", "2", "1"]])) +
                   "A muffin recipe uses eggs in the same ratio. How many muffins can you make with 1 egg?",
                   "3", ["4", "5", "1"],
                   "2 eggs make 6 muffins, so halve both: 1 egg makes 6 ÷ 2 = <b>3</b> muffins. "
                   "4 subtracts 2 like 6 − 2, 5 subtracts 1 like the egg row, and 1 copies the eggs.", value=3))
    its.append(mcq(fig(ratio_table_svg(["Sugar (cups)", "Cookies"], [["1", "2", "?"], ["24", "48", "120"]])) +
                   "A cookie recipe uses sugar in the same ratio. How many cups of sugar make 120 cookies?",
                   "5", ["3", "72", "6"],
                   "1 cup makes 24 cookies. 120 ÷ 24 = <b>5</b> cups. "
                   "3 only counts on by 1, 72 is the number of cookies for 3 cups, and 6 divides 120 by 20.", value=5))
    its.append(mcq(fig(ratio_table_svg(["Green (mL)", "Blue (mL)"], [["3", "6", "9"], ["5", "?", "15"]])) +
                   "Green and blue paint are mixed in the same ratio. What number is missing?",
                   "10", ["8", "12", "30"],
                   "6 = 3 × 2, so multiply 5 by 2 too: <b>10</b>. Check: 9:15 is 3:5 × 3. "
                   "8 adds 3 like the top row, 12 doubles 6, and 30 multiplies 6 by 5.", value=10))
    its.append(mcq(fig(ratio_table_svg(["Hours", "Distance (km)"], [["1", "2", "4", "10"], ["3", "6", "?", "30"]])) +
                   "A canoe moves at a steady speed. How far does it go in 4 hours?",
                   "12", ["9", "8", "24"],
                   "The canoe goes 3 km each hour. 4 hours: 4 × 3 = <b>12 km</b>. "
                   "9 counts on by 3, but the hours jumped from 2 to 4. 8 adds 2, and 24 multiplies 6 by 4.", value=12))
    its.append(mcq(fig(ratio_table_svg(["Packets", "Seeds"], [["4", "?", "12"], ["36", "54", "108"]])) +
                   "Every packet holds the same number of seeds. What number is missing?",
                   "6", ["8", "22", "9"],
                   "4 packets hold 36 seeds, so 1 packet holds 36 ÷ 4 = 9. 54 ÷ 9 = <b>6</b> packets. "
                   "8 doubles 4, 22 adds 18 like 36 + 18 = 54, and 9 is the seeds in 1 packet.", value=6))
    its.append(mcq(fig(ratio_table_svg(["Water (cups)", "Scoops"], [["2", "4", "6", "8"], ["5", "10", "13", "20"]])) +
                   "Mei wants every column to show the same ratio. Which column does <b>not</b> belong?",
                   "6 and 13", ["2 and 5", "4 and 10", "8 and 20"],
                   "The ratio is 2:5, so the scoops are 5 × (cups ÷ 2). 6 cups need 3 × 5 = 15 scoops, not 13. "
                   "<b>6 and 13</b> does not belong. The others are 2:5 times 1, 2 and 4."))
    its.append(mcq(fig(ratio_table_svg(["Red beads", "Yellow beads"], [["3", "6", "9", "12"], ["4", "8", "12", "16"]])) +
                   "A bracelet pattern uses beads in the ratio shown. How many yellow beads go with 30 red beads?",
                   "40", ["34", "31", "120"],
                   "30 = 3 × 10, so yellow = 4 × 10 = <b>40</b>. "
                   "34 adds 4 to 30, 31 adds 1 (the difference between 3 and 4), and 120 multiplies 30 by 4.", value=40))
    assert len(its) == 20, len(its)
    return {"title": "Ratio tables and double number lines", "items": its}


# ============================================================ set 4: comparing ratios
SAME = "They are the same"


def set_compare():
    its = []
    its.append(mcq("Mix A has juice and water in the ratio 1:2. Mix B has juice and water in the ratio 1:3. "
                   "Which mix tastes more of juice?",
                   "Mix A", ["Mix B", SAME, CANT],
                   "Both use 1 cup of juice. Mix A adds only 2 cups of water, Mix B adds 3. "
                   "Less water for the same juice means <b>Mix A</b> is stronger. Bigger numbers do not mean more juice."))
    its.append(mcq("Paint A uses red and white in the ratio 2:5. Paint B uses red and white in the ratio 2:3. "
                   "Which paint is a darker red?",
                   "Paint B", ["Paint A", SAME, CANT],
                   "Both use 2 parts red. Paint B adds only 3 parts white, so it is <b>Paint B</b>. "
                   "Paint A has more white, so it is a lighter pink."))
    its.append(mcq("Lemonade A has lemon juice and water in the ratio 3:4. Lemonade B has the ratio 6:8. "
                   "Which tastes more of lemon?",
                   SAME, ["Lemonade A", "Lemonade B", CANT],
                   "6:8 = 3:4 × 2. The ratios are equivalent, so <b>they are the same</b>. "
                   "Lemonade B is just a bigger batch."))
    its.append(mcq("Mix A has juice and water in the ratio 2:3. Mix B has juice and water in the ratio 4:5. "
                   "Which mix tastes more of juice?",
                   "Mix B", ["Mix A", SAME, CANT],
                   "Make the juice the same: 2:3 = 4:6. Now compare 4:6 with 4:5. Mix B has less water for 4 cups of juice, "
                   "so <b>Mix B</b>. Both have 1 more cup of water than juice, but that does not make them equal."))
    its.append(mcq("The Kelowna team’s ratio of wins to losses is 4:2. The Kamloops team’s ratio of wins to losses is 6:4. "
                   "Which team has the better record?",
                   "Kelowna", ["Kamloops", SAME, CANT],
                   "Make the wins the same: 4:2 = 2:1 = 6:3. Compare 6:3 with 6:4. Kelowna loses fewer games "
                   "for the same 6 wins, so <b>Kelowna</b>. Kamloops has more wins, but also more losses."))
    its.append(mcq("In Class A the ratio of boys to girls is 3:4. In Class B it is 5:4. "
                   "In which class are there more boys than girls?",
                   "Class B", ["Class A", "Both classes", "Neither class"],
                   "In 5:4, the first term (boys) is bigger, so <b>Class B</b> has more boys than girls. "
                   "In Class A, 3:4 means fewer boys than girls."))
    its.append(mcq("Mix A uses 2 scoops of powder for 6 cups of water. Mix B uses 3 scoops for 9 cups. "
                   "Which mix is stronger?",
                   SAME, ["Mix A", "Mix B", CANT],
                   "2:6 = 1:3 and 3:9 = 1:3. Both are 1 scoop for every 3 cups, so <b>they are the same</b>."))
    its.append(mcq("Hot chocolate A uses cocoa and milk in the ratio 3:4. Hot chocolate B uses the ratio 5:8. "
                   "Which tastes more of chocolate?",
                   "Hot chocolate A", ["Hot chocolate B", SAME, CANT],
                   "Make the milk the same: 3:4 = 6:8. Compare 6:8 with 5:8. "
                   "A has more cocoa in 8 cups of milk, so <b>Hot chocolate A</b>."))
    its.append(mcq("At Shelter A the ratio of dogs to cats is 5:10. At Shelter B it is 4:6. "
                   "Which shelter has more dogs for each cat?",
                   "Shelter B", ["Shelter A", SAME, CANT],
                   "5:10 = 1:2, so Shelter A has 1 dog for every 2 cats (3:6). Shelter B has 4:6. "
                   "4 &gt; 3, so <b>Shelter B</b>. Shelter A has bigger numbers, but not more dogs per cat."))
    its.append(mcq("Which juice mix (concentrate to water) is the strongest?", R(1, 2), [R(1, 5), R(1, 4), R(1, 3)],
                   "All four use 1 part concentrate. The one with the least water is strongest: <b>1:2</b>. "
                   "1:5 has the most water, so it is the weakest, even though 5 is the biggest number."))
    its.append(mcq("Which juice mix (concentrate to water) is the weakest?", R(2, 7), [R(2, 3), R(2, 5), R(2, 4)],
                   "All four use 2 parts concentrate. The one with the most water is weakest: <b>2:7</b>."))
    its.append(mcq("Trail Mix A has raisins and nuts in the ratio 2:3. Trail Mix B has the ratio 3:2. "
                   "Which mix has more raisins than nuts?",
                   "Trail Mix B", ["Trail Mix A", "Both mixes", "Neither mix"],
                   "In 3:2 the raisins (first term) are more than the nuts, so <b>Trail Mix B</b>. "
                   "The order of the terms matters: 2:3 and 3:2 are different ratios."))
    its.append(mcq("Ji-woo says 3:5 and 5:7 are equivalent because both have a difference of 2. Is she right?",
                   "No. 3:5 = 21:35 and 5:7 = 25:35",
                   ["Yes. Both have a difference of 2", "Yes. 3 + 2 = 5 and 5 + 2 = 7", "No. 3:5 = 6:10 and 5:7 = 6:8"],
                   "Make the second terms the same: 3:5 × 7 = 21:35 and 5:7 × 5 = 25:35. 21 is not 25, so "
                   "<b>no</b>. The difference does not tell you if ratios are equivalent. (5:7 is not 6:8.)"))
    its.append(mcq("Kai mixes blue and yellow paint in the ratio 1:3. Zara mixes them in the ratio 2:5. "
                   "Whose green paint is bluer?",
                   "Zara’s", ["Kai’s", SAME, CANT],
                   "Make the blue the same: 1:3 = 2:6. Compare 2:6 with 2:5. Zara uses less yellow for 2 parts blue, "
                   "so <b>Zara’s</b> paint is bluer."))
    its.append(mcq("Hana scored 6 goals in 8 hockey games. Owen scored 9 goals in 12 games. "
                   "Who has the better ratio of goals to games?",
                   SAME, ["Hana", "Owen", CANT],
                   "6:8 = 3:4 and 9:12 = 3:4. Both scored 3 goals for every 4 games, so <b>they are the same</b>. "
                   "Owen has more goals, but he also played more games."))
    its.append(mcq("Which ratio of red counters to blue counters has the most red for each blue?", R(3, 1),
                   [R(5, 2), R(8, 4), R(7, 3)],
                   "Find the red for 1 blue: 3:1 is 3, 5:2 is 2.5, 8:4 is 2, and 7:3 is a little more than 2. "
                   "The most is <b>3:1</b>. 8:4 has the biggest numbers but only 2 red for each blue."))
    its.append(mcq("In Tray A, 12 of 16 seeds sprouted. In Tray B, 14 of 20 seeds sprouted. "
                   "Which tray has the greater ratio of sprouted seeds to seeds planted?",
                   "Tray A", ["Tray B", SAME, CANT],
                   "12:16 = 3:4 = 15:20. Compare 15:20 with 14:20. <b>Tray A</b> is greater. "
                   "Tray B has more sprouted seeds, but more seeds were planted."))
    its.append(mcq("In Class A, 8 of 24 students bike to school. In Class B, 9 of 30 students bike. "
                   "Which class has the greater ratio of bikers to all students?",
                   "Class A", ["Class B", SAME, CANT],
                   "8:24 = 1:3 = 10:30. Compare 10:30 with 9:30. <b>Class A</b> is greater, "
                   "even though Class B has more bikers."))
    its.append(mcq("A drink uses 2 scoops of powder for 5 cups of water. Which mix tastes the same?",
                   "4 scoops for 10 cups", ["5 scoops for 8 cups", "3 scoops for 6 cups", "4 scoops for 7 cups"],
                   "2:5 × 2 = 4:10, so <b>4 scoops for 10 cups</b> tastes the same. "
                   "4 scoops for 7 cups and 5 scoops for 8 cups add the same number to both terms, "
                   "and 3:6 = 1:2 is stronger."))
    its.append(mcq("Mix A has juice and water in the ratio 3:7. Mix B has juice and water in the ratio 4:9. "
                   "Which mix tastes more of juice?",
                   "Mix B", ["Mix A", SAME, CANT],
                   "Make the water the same: 3:7 × 9 = 27:63 and 4:9 × 7 = 28:63. "
                   "28 &gt; 27, so <b>Mix B</b> has a little more juice."))
    assert len(its) == 20, len(its)
    return {"title": "Comparing ratios", "items": its}


# ============================================================ set 5: word problems
def set_problems():
    its = []
    its.append(mcq("A pancake recipe uses 3 cups of flour for every 2 eggs. Mei uses 9 cups of flour. "
                   "How many eggs does she need?",
                   "6", ["8", "3", "18"],
                   "3 × 3 = 9, so multiply the eggs by 3 too: 2 × 3 = <b>6</b> eggs. "
                   "8 adds 6 like 3 + 6 = 9, 3 is the number you multiply by, and 18 multiplies 9 by 2.", value=6))
    its.append(mcq("On a soccer team, the ratio of boys to girls is 2:3. There are 8 boys. How many girls are there?",
                   "12", ["9", "20", "4"],
                   "2 × 4 = 8, so the girls are 3 × 4 = <b>12</b>. 9 adds 6 like 2 + 6 = 8, "
                   "20 is the whole team, and 4 is the number you multiply by.", value=12))
    its.append(mcq("A hockey team has 12 forwards and 6 defence players. "
                   "What is the ratio of forwards to defence players in simplest form?",
                   R(2, 1), [R(1, 2), R(2, 3), R(1, 3)],
                   "12:6. Divide both terms by 6: <b>2:1</b>. 1:2 is defence to forwards, "
                   "2:3 is 12:18, forwards to the whole team, and 1:3 is defence to the whole team."))
    its.append(mcq("Trail mix for a hike on Vancouver Island uses 3 cups of nuts for every 2 cups of raisins. "
                   "How many cups of raisins go with 12 cups of nuts?",
                   "8 cups", ["11 cups", "4 cups", "18 cups"],
                   "3 × 4 = 12, so 2 × 4 = <b>8 cups</b>. 11 adds 9 like 3 + 9 = 12, "
                   "and 18 uses the ratio the wrong way round (12 ÷ 2 × 3).", value=8))
    its.append(mcq("A smoothie recipe uses 2 bananas for 4 people. How many bananas are needed for 10 people?",
                   "5", ["8", "20", "10"],
                   "2 bananas for 4 people is 1 banana for every 2 people. 10 ÷ 2 = <b>5</b> bananas. "
                   "8 adds 6 because there are 6 more people, 20 multiplies 2 by 10, and 10 gives 1 banana each.", value=5))
    its.append(mcq("In a volleyball club, the ratio of Grade 6 players to Grade 7 players is 3:5. "
                   "There are 24 players in all. How many are in Grade 6?",
                   "9", ["15", "8", "12"],
                   "Each group has 3 + 5 = 8 players. 24 ÷ 8 = 3 groups. Grade 6: 3 × 3 = <b>9</b>. "
                   "15 is the Grade 7 players, 8 divides 24 by 3, and 12 is just half the club.", value=9))
    its.append(mcq("A muffin recipe uses 2 cups of oats to make 12 muffins. How many muffins can you make with 5 cups of oats?",
                   "30", ["15", "60", "24"],
                   "1 cup makes 12 ÷ 2 = 6 muffins. 5 cups make 5 × 6 = <b>30</b>. "
                   "15 adds 3 like 2 + 3 = 5, 60 multiplies 12 by 5, and 24 is for 4 cups.", value=30))
    its.append(mcq("At the school’s Terry Fox Run, the ratio of students who walked to students who ran was 5:3. "
                   "15 students ran. How many walked?",
                   "25", ["17", "9", "40"],
                   "3 × 5 = 15, so the walkers are 5 × 5 = <b>25</b>. 17 adds 12 like 3 + 12 = 15, "
                   "9 uses the ratio the wrong way round, and 40 is everyone.", value=25))
    its.append(mcq("A basketball team’s ratio of wins to losses is 3:2. They played 20 games with no ties. "
                   "How many games did they win?",
                   "12", ["8", "10", "4"],
                   "Each group has 3 + 2 = 5 games. 20 ÷ 5 = 4 groups. Wins: 3 × 4 = <b>12</b>. "
                   "8 is the losses, 10 is just half the games, and 4 is the number of groups.", value=12))
    its.append(mcq("Olivia makes 16 tablespoons of salad dressing with oil and vinegar in the ratio 3:1. "
                   "How much oil does she use?",
                   "12 tablespoons", ["4 tablespoons", "48 tablespoons", "15 tablespoons"],
                   "Each batch has 3 + 1 = 4 parts. 16 ÷ 4 = 4 tablespoons per part. Oil is 3 parts: <b>12 tablespoons</b>. "
                   "4 is the vinegar, 48 multiplies 16 by 3, and 15 takes away just 1.", value=12))
    its.append(mcq("A hockey coach brings 3 oranges for every 4 players. There are 16 players. How many oranges does the coach bring?",
                   "12", ["15", "4", "48"],
                   "4 × 4 = 16, so 3 × 4 = <b>12</b> oranges. 15 adds 12 like 4 + 12 = 16, "
                   "4 is the number you multiply by, and 48 multiplies 16 by 3.", value=12))
    its.append(mcq("For an art class, Emma mixes blue and white paint in the ratio 1:4. "
                   "She makes 25 mL of paint. How much white paint does she use?",
                   "20 mL", ["5 mL", "100 mL", "6.25 mL"],
                   "Each batch has 1 + 4 = 5 parts. 25 ÷ 5 = 5 mL per part. White is 4 parts: 4 × 5 = <b>20 mL</b>. "
                   "5 mL is the blue, 100 mL multiplies 25 by 4, and 6.25 mL divides by 4 instead of 5.", value=20))
    its.append(mcq("A chili recipe serves 8 people and uses 6 tomatoes. How many tomatoes are needed to serve 4 people?",
                   "3", ["2", "12", "4"],
                   "4 people is half of 8, so use half the tomatoes: 6 ÷ 2 = <b>3</b>. "
                   "2 subtracts 4 like 8 − 4, 12 doubles instead of halving, and 4 copies the number of people.", value=3))
    its.append(mcq("A soccer team pays $45 for 3 new balls. At the same price, what do 7 balls cost?",
                   "$105", ["$49", "$315", "$90"],
                   "1 ball costs $45 ÷ 3 = $15. 7 balls cost 7 × $15 = <b>$105</b>. "
                   "$49 adds $4 for 4 more balls, $315 multiplies $45 by 7, and $90 is for 6 balls.", value=105))
    its.append(mcq("On a BC Ferries sailing, the ratio of cars to trucks is 9:1. There are 270 cars. How many trucks are there?",
                   "30", ["262", "2430", "27"],
                   "1 truck for every 9 cars: 270 ÷ 9 = <b>30</b> trucks. 262 subtracts 8, "
                   "2430 multiplies by 9, and 27 divides by 10 as if 270 were all the vehicles.", value=30))
    its.append(mcq("At a hockey camp in Prince George, the ratio of kids to coaches is 8:1. There are 5 coaches. "
                   "How many kids are there?",
                   "40", ["13", "45", "32"],
                   "Each coach has 8 kids: 5 × 8 = <b>40</b>. 13 adds 8 and 5, 45 counts the coaches too, "
                   "and 32 is for only 4 coaches.", value=40))
    its.append(mcq("In a Grade 6 class of 28 students, the ratio of students who play on a team to students who do not is 4:3. "
                   "How many play on a team?",
                   "16", ["12", "7", "21"],
                   "Each group has 4 + 3 = 7 students. 28 ÷ 7 = 4 groups. Team players: 4 × 4 = <b>16</b>. "
                   "12 is the students who do not, 7 divides 28 by 4, and 21 is 28 ÷ 4 × 3, as if 4:3 meant 3 out of every 4.", value=16))
    its.append(mcq("Granola bars use 4 cups of oats for every 1 cup of honey. Ryan uses 2 cups of honey. "
                   "How many cups of oats does he need?",
                   "8 cups", ["5 cups", "6 cups", "0.5 cups"],
                   "Double the honey, so double the oats: 4 × 2 = <b>8 cups</b>. "
                   "5 adds 1 like 1 + 1 = 2, 6 adds 2 to 4, and 0.5 divides 2 by 4 (the wrong way round).", value=8))
    its.append(mcq("The Surrey team won 7 of its 10 games. The Burnaby team won 9 of its 15 games. "
                   "Which team has the greater ratio of wins to games played?",
                   "Surrey", ["Burnaby", SAME, CANT],
                   "Make the games the same: 7:10 = 21:30 and 9:15 = 18:30. 21 &gt; 18, so <b>Surrey</b>. "
                   "Burnaby has more wins, but it played more games."))
    its.append(mcq("A banana bread recipe uses 2 cups of flour for every 3 bananas. Sofia has 8 cups of flour and 9 bananas. "
                   "She uses all the bananas. How much flour is left over?",
                   "2 cups", ["6 cups", "1 cup", "0 cups"],
                   "9 bananas = 3 × 3 bananas, so she uses 3 × 2 = 6 cups of flour. 8 − 6 = <b>2 cups</b> left over. "
                   "6 cups is the flour she uses, 1 cup is 9 − 8, and 0 cups forgets that 9 bananas need only 6 cups.", value=2))
    assert len(its) == 20, len(its)
    return {"title": "Word problems: recipes and teams", "items": its}


# ============================================================ lesson
def body_html():
    f_cnt = counters_svg((3, "red"), (5, "blue"))
    f_tab = ratio_table_svg(["Flour (cups)", "Eggs"], [["3", "6", "9", "12"], ["2", "4", "6", "8"]])
    return (
        "<h2>What a ratio is</h2>"
        "<p>A <b>ratio</b> compares two amounts. 3:5 is read “3 to 5”. Keep the order of the words: "
        "red to blue means the red number comes first.</p>"
        "<p>A <b>part-to-part</b> ratio compares two parts. A <b>part-to-whole</b> ratio compares one part with "
        "everything. Part to whole can also be written as a fraction.</p>"
        "<figure class='sn-fig'>" + f_cnt +
        "<figcaption>Red to blue is 3:5 (part to part). Blue to red is 5:3. Red to all is 3:8, so " + fr(3, 8) +
        " of the counters are red (part to whole).</figcaption></figure>"
        "<h2>Equivalent ratios</h2>"
        "<p>Multiply or divide <b>both</b> terms by the same number. The ratio stays the same. "
        "Never add the same number to both terms.</p>"
        + ex("Example", "Find the missing term: 2:3 = ?:12",
             "3 × 4 = 12, so multiply 2 by 4 too.", "8")
        + ex("Simplest form", "Write 12:16 in simplest form.",
             "Divide both terms by 4: 12 ÷ 4 = 3 and 16 ÷ 4 = 4.", "3:4")
        + "<h2>Ratio tables</h2>"
        "<p>Each column of a ratio table is the first column times a number.</p>"
        "<figure class='sn-fig'>" + f_tab +
        "<figcaption>Every column is 3:2 times a number. 12 = 3 × 4, so the eggs are 2 × 4 = 8.</figcaption></figure>"
        "<h2>Comparing ratios</h2>"
        "<p>Make one term the same, then compare the other term.</p>"
        + ex("Example", "Mix A is juice to water 2:3. Mix B is 4:5. Which tastes more of juice?",
             "2:3 = 4:6. Both now have 4 cups of juice. Mix B has less water (5 &lt; 6).", "Mix B")
        + ex("Part of a total", "A team has boys and girls in the ratio 3:5. There are 24 players. How many are boys?",
             "Each group has 3 + 5 = 8 players. 24 ÷ 8 = 3 groups. Boys: 3 × 3 = 9.", "9 boys")
        + "<h2>Common mistakes</h2>"
        + table(["Mistake", "What to do instead"], [
            ["3 red and 5 blue: red to blue is 5:3", "Keep the order of the words: red to blue is 3:5"],
            ["Red to blue is 3:5, so " + fr(3, 5) + " are red", "3:5 is part to part. The whole is 3 + 5 = 8, so " + fr(3, 8) + " are red"],
            ["2:3 = 5:6 (add 3 to both)", "Multiply both terms: 2:3 = 6:9"],
            ["1:5 is stronger than 1:2 because 5 is bigger", "Make one term the same, then compare. 1:2 has less water"],
        ])
    )


FAQ = [
    {"q": "What do Grade 6 students learn about ratios in BC?",
     "a": "The BC Grade 6 math curriculum introduces ratios. Students write part-to-part and part-to-whole ratios, find equivalent ratios, use ratio tables and compare ratios in real situations like recipes and teams."},
    {"q": "What is the difference between a part-to-part and a part-to-whole ratio?",
     "a": "Part to part compares two groups, like 3 red to 5 blue (3:5). Part to whole compares one group with everything, like 3 red out of 8 counters (3:8), which is the fraction 3/8."},
    {"q": "How do you find equivalent ratios?",
     "a": "Multiply or divide both terms by the same number: 2:3 = 4:6 = 6:9. Adding the same number to both terms (2:3 to 5:6) does not give an equivalent ratio."},
    {"q": "How do you compare two ratios?",
     "a": "Make one term the same in both ratios, then compare the other term. For juice to water, 2:3 = 4:6, so 4:5 has less water and tastes stronger."},
]


def mark_large(u, pattern):
    """Tag wide pictures so they print larger and stay readable."""
    rx = re.compile(r"<svg (?=[^>]*aria-label='" + pattern + ")")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u


def gen():
    rnd = random.Random(56804)
    sets = [set_pictures(), set_equivalent(), set_tables(), set_compare(), set_problems()]
    seen = set()
    for s in sets:
        assert len(s["items"]) == 20, (s["title"], len(s["items"]))
        for it in s["items"]:
            assert len(set(it["c"])) == 4, it
            assert it["q"].count("<svg") <= 1, it["q"]
            k = plain(it["q"]) + "|" + "|".join(sorted(it["c"]))
            assert k not in seen, it["q"]
            seen.add(k)
    balance(sets, rnd)
    for s in sets:
        assert sorted(it["a"] for it in s["items"]) == sorted([0, 1, 2, 3] * 5)
    u = {
        "country": "ca-bc", "subject": "math", "grade": "grade-6", "slug": SLUG, "sort": 4,
        "updated": UPDATED, "pdf_url": "",
        "title": "Ratios: Part to Part, Part to Whole, Equivalent Ratios and Ratio Tables",
        "seo_title": "Grade 6 Ratios Worksheets (BC Curriculum) – Free Math with Answer Key",
        "short_title": "Ratios",
        "domain": "Number",
        "standard_code": "Grade 6: Number",
        "standard_url": "https://curriculum.gov.bc.ca/curriculum/mathematics/6/core",
        "standard_text": "Introduction to ratios",
        "meta_desc": "Free Grade 6 ratio worksheets for the BC math curriculum: write part-to-part and part-to-whole ratios, find equivalent ratios, use ratio tables, compare ratios and solve recipe and team problems. 100 questions with an answer key.",
        "key_big": "A ratio compares two amounts in order. Multiply or divide both terms by the same number to get an equivalent ratio.",
        "key_sub": "Red to blue 3:5 is part to part; red to all 3:8 is part to whole (3/8). Never add the same number to both terms.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }
    return mark_large(u, "(ratio table|double number line|counters)")


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
