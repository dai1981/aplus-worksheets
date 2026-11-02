# -*- coding: utf-8 -*-
"""
BC Grade 7 Math: Ratios (BC Mathematics Curriculum, Grade 7: Number —
relationships between decimals, fractions, ratios, and percents)
  python3 tools/gen_cabc_math_g7_ratios.py
Write ratios from pictures (part to part and part to whole), equivalent ratios and ratio tables,
ratios as fractions, decimals and percents, unit rates and best buys, then word problems in BC
contexts (mixing paint, a muffin recipe, kids to adults on a field trip).
Wrong answers come from real mistakes: part to part used as part to whole, reversed ratios,
adding instead of multiplying in a ratio table, multiplying instead of dividing for a unit rate.
Every answer is checked with fractions.Fraction (never float).
Canadian English, dollars and cents (¢), metric units, SI number spacing. HTML attributes use single quotes.
"""
import json, os, random, re
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "ca-bc", "math", "grade-7")
SLUG = "ratios"
UPDATED = "2026-11-02"
NBSP = " "
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


# ============================================================ set 1: writing ratios from pictures
def set_pictures():
    its = []
    its.append(mcq(fig(counters_svg((3, "red"), (5, "blue"))) + "What is the ratio of red counters to blue counters?",
                   R(3, 5), [R(5, 3), R(3, 8), R(5, 8)],
                   "3 red and 5 blue. Red is named first, so the ratio is <b>3:5</b> (part to part). "
                   "5:3 is blue to red, and 3:8 is red to <b>all</b> the counters."))
    its.append(mcq(fig(counters_svg((4, "red"), (3, "blue"))) + "What is the ratio of blue counters to red counters?",
                   R(3, 4), [R(4, 3), R(3, 7), R(4, 7)],
                   "Blue is named first: 3 blue, then 4 red, so <b>3:4</b>. 4:3 is red to blue, "
                   "and 3:7 compares blue to all 7 counters."))
    its.append(mcq(fig(counters_svg((2, "red"), (5, "blue"))) + "What is the ratio of red counters to <b>all</b> the counters?",
                   R(2, 7), [R(2, 5), R(7, 2), R(5, 7)],
                   "This is part to whole. There are 2 + 5 = 7 counters, and 2 are red: <b>2:7</b>. "
                   "2:5 is red to blue (part to part)."))
    its.append(mcq(fig(counters_svg((5, "red"), (4, "blue"))) + "What is the ratio of blue counters to all the counters?",
                   R(4, 9), [R(4, 5), R(9, 4), R(5, 9)],
                   "There are 5 + 4 = 9 counters. 4 are blue, so blue to all is <b>4:9</b>. "
                   "4:5 is blue to red, and 5:9 is red to all."))
    its.append(mcq(fig(counters_svg((3, "yellow"), (4, "blue"))) + "What fraction of the counters are yellow?",
                   fr(3, 7), [fr(3, 4), fr(4, 7), fr(4, 3)],
                   "A fraction is part to whole. 3 of the 3 + 4 = 7 counters are yellow: <b>%s</b>. "
                   "%s compares yellow to blue (part to part)." % (fr(3, 7), fr(3, 4)), value=F(3, 7)))
    its.append(mcq(fig(counters_svg((6, "red"), (4, "blue"))) + "What is the ratio of red to blue counters in simplest form?",
                   R(3, 2), [R(2, 3), R(3, 5), R(2, 5)],
                   "6:4. Divide both terms by 2: <b>3:2</b>. 2:3 is blue to red, and 3:5 is 6:10, red to all."))
    its.append(mcq(fig(counters_svg((2, "green"), (6, "blue"))) +
                   "What fraction of the counters are green? Write it in simplest form.",
                   fr(1, 4), [fr(1, 3), fr(3, 4), fr(1, 8)],
                   "2 of the 2 + 6 = 8 counters are green: %s = <b>%s</b>. %s is green to blue (2:6), "
                   "and %s divides only the top number by 2." % (fr(2, 8), fr(1, 4), fr(1, 3), fr(1, 8)), value=F(1, 4)))
    its.append(mcq(fig(counters_svg((2, "red"), (3, "blue"), (4, "yellow"))) +
                   "What is the ratio of red to blue to yellow counters?",
                   R(2, 3, 4), [R(2, 4, 3), R(4, 3, 2), R(2, 3, 9)],
                   "Keep the order of the words: 2 red, 3 blue, 4 yellow, so <b>2:3:4</b>. "
                   "4:3:2 is yellow to blue to red, and 9 is the total, not the yellow."))
    its.append(mcq(fig(counters_svg((2, "red"), (3, "blue"), (4, "yellow"))) +
                   "What is the ratio of yellow counters to all the counters?",
                   R(4, 9), [R(4, 5), R(9, 4), R(4, 3)],
                   "There are 2 + 3 + 4 = 9 counters, and 4 are yellow: <b>4:9</b>. "
                   "4:5 is yellow to the other counters (part to part), and 4:3 is yellow to blue."))
    its.append(mcq(fig(grid_svg(3, 4, 5)) + "What is the ratio of shaded squares to unshaded squares?",
                   R(5, 7), [R(5, 12), R(7, 5), R(7, 12)],
                   "5 squares are shaded and 12 − 5 = 7 are not: <b>5:7</b>. "
                   "5:12 is shaded to the whole grid (part to whole)."))
    its.append(mcq(fig(grid_svg(2, 5, 4)) + "What is the ratio of unshaded squares to all the squares, in simplest form?",
                   R(3, 5), [R(3, 2), R(2, 5), R(2, 3)],
                   "6 of the 10 squares are unshaded: 6:10. Divide both terms by 2: <b>3:5</b>. "
                   "3:2 is unshaded to shaded (6:4), and 2:5 is shaded to all."))
    its.append(mcq(fig(grid_svg(4, 5, 8)) + "What is the ratio of shaded squares to unshaded squares, in simplest form?",
                   R(2, 3), [R(2, 5), R(3, 2), R(3, 5)],
                   "8 shaded and 20 − 8 = 12 unshaded: 8:12. Divide both terms by 4: <b>2:3</b>. "
                   "2:5 is 8:20, shaded to the whole grid."))
    its.append(mcq(fig(counters_svg((4, "red"), (6, "blue"))) + "Which statement about the counters is <b>not</b> true?",
                   "Blue to red is 2:3", ["Red to blue is 2:3", "Red to all is 2:5", "Blue to all is 3:5"],
                   "Red to blue is 4:6 = 2:3, so blue to red is 6:4 = <b>3:2</b>, not 2:3. "
                   "Red to all is 4:10 = 2:5, and blue to all is 6:10 = 3:5."))
    its.append(mcq(fig(counters_svg((3, "red"), (4, "blue"))) +
                   "Ji-woo adds 2 more red counters. What is the new ratio of red to blue counters?",
                   R(5, 4), [R(3, 4), R(5, 6), R(5, 9)],
                   "Red goes from 3 to 3 + 2 = 5. Blue stays 4. The new ratio is <b>5:4</b>. "
                   "5:6 adds 2 to the blue too, and 5:9 is red to all."))
    its.append(mcq(fig(counters_svg((4, "red"), (5, "blue"))) +
                   "How many blue counters must you <b>add</b> so that red to blue is 1:2?",
                   "3", ["8", "4", "12"],
                   "1:2 means twice as many blue as red. 4 red need 2 × 4 = 8 blue. There are 5, so add 8 − 5 = <b>3</b>. "
                   "8 is how many blue in all, 4 adds the number of red, and 12 is how many counters in all.", value=3))
    its.append(mcq("A bag has 5 red marbles and 7 green marbles. What is the ratio of green marbles to all the marbles?",
                   R(7, 12), [R(7, 5), R(5, 12), R(12, 7)],
                   "There are 5 + 7 = 12 marbles, and 7 are green: <b>7:12</b>. 7:5 is green to red (part to part)."))
    its.append(mcq("A class has 28 students. 12 are boys. What is the ratio of boys to girls in simplest form?",
                   R(3, 4), [R(3, 7), R(4, 3), R(4, 7)],
                   "Girls: 28 − 12 = 16. Boys to girls is 12:16. Divide both terms by 4: <b>3:4</b>. "
                   "3:7 is 12:28, boys to the whole class."))
    its.append(mcq("The ratio of red counters to blue counters in a bag is 2:3. What fraction of the counters are red?",
                   fr(2, 5), [fr(2, 3), fr(3, 5), fr(3, 2)],
                   "2:3 means 2 red for every 3 blue, so every group has 2 + 3 = 5 counters. Red is <b>%s</b>. "
                   "%s is red to blue (part to part), not part to whole." % (fr(2, 5), fr(2, 3)), value=F(2, 5)))
    its.append(mcq("On a soccer team, the ratio of boys to girls is 5:4. What fraction of the team are girls?",
                   fr(4, 9), [fr(4, 5), fr(5, 9), fr(5, 4)],
                   "Every group has 5 + 4 = 9 players, and 4 are girls: <b>%s</b>. "
                   "%s compares girls to boys, and %s is the boys." % (fr(4, 9), fr(4, 5), fr(5, 9)), value=F(4, 9)))
    its.append(mcq("In a fruit bowl, the ratio of apples to oranges is 3:5. Which statement <b>must</b> be true?",
                   "%s of the fruit are apples" % fr(3, 8),
                   ["%s of the fruit are apples" % fr(3, 5), "There are exactly 8 pieces of fruit",
                    "There are 2 more oranges than apples"],
                   "Each group has 3 apples and 5 oranges, so 3 of every 8 pieces are apples: <b>%s</b>. "
                   "The bowl could have 6 apples and 10 oranges, so it need not have 8 pieces or 2 more oranges." % fr(3, 8)))
    assert len(its) == 20, len(its)
    return {"title": "Writing ratios from pictures: part to part and part to whole", "items": its}


# ============================================================ set 2: equivalent ratios and ratio tables
def set_equivalent():
    its = []
    its.append(mcq("Which ratio is equivalent to 2:5?", R(6, 15), [R(5, 8), R(6, 5), R(4, 7)],
                   "Multiply <b>both</b> terms by 3: 2 × 3 = 6 and 5 × 3 = 15, so 2:5 = <b>6:15</b>. "
                   "5:8 adds 3 to both terms, and 6:5 multiplies only the first term."))
    its.append(mcq("Which ratio is equivalent to 3:4?", R(9, 12), [R(6, 7), R(9, 4), R(4, 3)],
                   "3 × 3 = 9 and 4 × 3 = 12, so 3:4 = <b>9:12</b>. 6:7 adds 3 to both terms, "
                   "and 9:4 multiplies only the 3."))
    its.append(mcq("Write 18:24 in simplest form.", R(3, 4), [R(4, 3), R(9, 15), R(6, 12)],
                   "The greatest common factor of 18 and 24 is 6. 18 ÷ 6 = 3 and 24 ÷ 6 = 4: <b>3:4</b>. "
                   "9:15 subtracts 9 from both terms, and 6:12 subtracts 12."))
    its.append(mcq("Write 15:35 in simplest form.", R(3, 7), [R(7, 3), R(3, 5), R(1, 21)],
                   "Divide <b>both</b> terms by 5: 15 ÷ 5 = 3 and 35 ÷ 5 = 7, so <b>3:7</b>. "
                   "3:5 divides 15 by 5 but 35 by 7, and 1:21 subtracts 14 from both terms."))
    its.append(mcq("Find the missing term: 3:4 = ?:20", "15", ["19", "5", "12"],
                   "4 × 5 = 20, so multiply the first term by 5 too: 3 × 5 = <b>15</b>. "
                   "19 adds 16, like 4 + 16 = 20, but equivalent ratios never come from adding.", value=15))
    its.append(mcq("Find the missing term: 5:8 = 20:?", "32", ["23", "4", "160"],
                   "5 × 4 = 20, so multiply 8 by 4 too: 8 × 4 = <b>32</b>. 23 adds 15 to both terms, "
                   "and 4 is only the number you multiply by.", value=32))
    its.append(mcq("Find the missing term: 12:18 = 2:?", "3", ["8", "6", "9"],
                   "12 ÷ 6 = 2, so divide 18 by 6 too: <b>3</b>. 8 subtracts 10 from both terms, "
                   "and 6 is the number you divide by.", value=3))
    its.append(mcq(fig(ratio_table_svg(["Water (cups)", "Mix (scoops)"], [["3", "6", "9"], ["2", "4", "?"]])) +
                   "The ratio table is for a jug of iced tea. What number is missing?",
                   "6", ["5", "9", "8"],
                   "The top row is 3 × 1, 3 × 2, 3 × 3. Do the same to the bottom row: 2 × 3 = <b>6</b>. "
                   "5 adds 3 like the top row, but each row grows by its own amount.", value=6))
    its.append(mcq(fig(ratio_table_svg(["Juice (L)", "Water (L)"], [["1", "2", "3", "?"], ["4", "8", "12", "20"]])) +
                   "The table shows juice and water mixed in the same ratio. What number is missing?",
                   "5", ["4", "16", "80"],
                   "The ratio is 1:4, so the water is always 4 times the juice. 20 ÷ 4 = <b>5</b>. "
                   "4 just counts on by 1, but 20 is not the next step after 12.", value=5))
    its.append(mcq(fig(ratio_table_svg(["Flour (cups)", "Eggs"], [["2", "4", "8", "?"], ["3", "6", "12", "15"]])) +
                   "A recipe uses flour and eggs in the same ratio. What number is missing?",
                   "10", ["11", "16", "13"],
                   "The ratio is 2:3. 15 = 3 × 5, so the flour is 2 × 5 = <b>10</b> cups. "
                   "11 adds 3 like the egg row, and 16 doubles 8 although 15 is not double 12.", value=10))
    its.append(mcq(fig(ratio_table_svg(["Blue (mL)", "Yellow (mL)"], [["4", "8", "?"], ["6", "12", "21"]])) +
                   "Blue and yellow paint are mixed in the same ratio. What number is missing?",
                   "14", ["17", "7", "42"],
                   "4:6 = 2:3. 21 = 3 × 7, so blue = 2 × 7 = <b>14</b> mL. "
                   "17 adds 9 because 12 + 9 = 21, but you must multiply, not add.", value=14))
    its.append(mcq("Which ratio is <b>not</b> equivalent to 4:6?", R(6, 8), [R(2, 3), R(8, 12), R(10, 15)],
                   "4:6 = 2:3. 8:12 and 10:15 also simplify to 2:3. <b>6:8</b> adds 2 to both terms "
                   "and simplifies to 3:4, so it is not equivalent.", same_ok=True))
    its.append(mcq(fig(ratio_table_svg(["Students", "Granola bars"], [["3", "6", "30"], ["2", "4", "?"]])) +
                   "What number is missing in the ratio table?",
                   "20", ["28", "24", "45"],
                   "6 × 5 = 30, so 4 × 5 = <b>20</b>. 28 adds 24 because 6 + 24 = 30, "
                   "and 45 uses the ratio the wrong way round (3:2).", value=20))
    its.append(mcq("Liam says 2:3 = 5:6 because he added 3 to both terms. Is he right?",
                   "No. Multiply both terms: 2:3 = 6:9",
                   ["Yes. Add the same number to both terms", "Yes. Both terms got bigger", "No. 2:3 = 5:9"],
                   "Equivalent ratios come from <b>multiplying</b> (or dividing) both terms by the same number. "
                   "2:3 means the second amount is 1.5 times the first. 5:6 breaks that, but 6:9 keeps it."))
    its.append(mcq("Which ratio table shows the ratio 3:5?",
                   "3, 6, 9 and 5, 10, 15",
                   ["3, 6, 9 and 5, 8, 11", "3, 5, 7 and 5, 7, 9", "3, 6, 9 and 5, 10, 20"],
                   "Every column must be 3:5 times the same number: 3:5, 6:10, 9:15, so <b>3, 6, 9 and 5, 10, 15</b>. "
                   "5, 8, 11 adds 3 each time, and 9:20 is not 3:5."))
    its.append(mcq("Find the missing term: 1.5:2 = ?:8", "6", ["7.5", "4", "3"],
                   "2 × 4 = 8, so multiply 1.5 by 4 too: 1.5 × 4 = <b>6</b>. "
                   "7.5 adds 6 because 2 + 6 = 8, and 4 is only the number you multiply by.", value=6))
    its.append(mcq("Are 4:10 and 6:15 equivalent ratios?",
                   "Yes. Both simplify to 2:5",
                   ["No. 4 + 2 = 6, but 10 + 2 is not 15", "No. 6:15 has bigger numbers", "Yes. Both simplify to 1:2"],
                   "4:10 ÷ 2 = 2:5 and 6:15 ÷ 3 = 2:5. They are <b>equivalent</b>. "
                   "Checking by adding does not work for ratios."))
    its.append(mcq("Find the missing term: 7:4 = 42:?", "24", ["39", "6", "168"],
                   "7 × 6 = 42, so 4 × 6 = <b>24</b>. 39 adds 35 to both terms, and 168 multiplies 4 by 42.",
                   value=24))
    its.append(mcq("A ratio table for 2:7 goes 2:7, 4:14, 6:21 and so on. Which number goes with 18?",
                   "63", ["23", "56", "9"],
                   "18 = 2 × 9, so multiply 7 by 9: <b>63</b>. 23 adds 5 (the difference in 2:7), "
                   "and 9 is only the number you multiply by.", value=63))
    its.append(mcq("Find the missing term: 9:12 = 6:?", "8", ["9", "18", "4"],
                   "Simplify first: 9:12 = 3:4. Then 6 = 3 × 2, so 4 × 2 = <b>8</b>. "
                   "9 subtracts 3 from both terms, and 18 multiplies 6 by 3.", value=8))
    assert len(its) == 20, len(its)
    return {"title": "Equivalent ratios and ratio tables", "items": its}


# ============================================================ set 3: ratios as fractions, decimals and percents
def set_percents():
    its = []
    its.append(mcq("In a bag, the ratio of red marbles to <b>all</b> the marbles is 1:4. What percent of the marbles are red?",
                   "25%", ["14%", "75%", "20%"],
                   "1:4 part to whole is %s = <b>25%%</b>. 14%% just writes the digits, 75%% is the other marbles, "
                   "and 20%% treats 1:4 as part to part." % fr(1, 4)))
    its.append(mcq("The ratio of red to blue counters is 2:3. What percent of the counters are red?",
                   "40%", ["about 67%", "60%", "23%"],
                   "Each group has 2 + 3 = 5 counters. Red is %s = %s = <b>40%%</b>. "
                   "About 67%% is %s, part to part, and 60%% is the blue." % (fr(2, 5), fr(40, 100), fr(2, 3))))
    its.append(mcq("Write %s as a percent." % fr(3, 5), "60%", ["35%", "30%", "53%"],
                   "%s = %s = <b>60%%</b>: multiply the top and bottom by 20. 35%% just writes the digits, "
                   "and 30%% multiplies by 10 instead of 20." % (fr(3, 5), fr(60, 100))))
    its.append(mcq("Write %s as a percent." % fr(7, 20), "35%", ["7%", "70%", "14%"],
                   "20 × 5 = 100, so %s = %s = <b>35%%</b>. 70%% treats it as %s, and 14%% multiplies by 2."
                   % (fr(7, 20), fr(35, 100), fr(7, 10))))
    its.append(mcq("Write 45% as a fraction in simplest form.", fr(9, 20), [fr(4, 5), fr(9, 2), fr(11, 20)],
                   "45%% = %s. Divide the top and bottom by 5: <b>%s</b>. %s is 4.5, and %s is 55%%."
                   % (fr(45, 100), fr(9, 20), fr(9, 2), fr(11, 20)), value=F(9, 20)))
    its.append(mcq("Write 0.6 as a percent.", "60%", ["6%", "0.6%", "600%"],
                   "0.6 = 0.60 = %s = <b>60%%</b>. Move the decimal point 2 places right. 6%% is 0.06." % fr(60, 100)))
    its.append(mcq("In a choir, the ratio of girls to boys is 3:2. What percent of the choir are girls?",
                   "60%", ["150%", "40%", "32%"],
                   "Each group has 3 + 2 = 5 singers. Girls are %s = <b>60%%</b>. "
                   "150%% is %s (girls to boys), and 40%% is the boys." % (fr(3, 5), fr(3, 2))))
    its.append(mcq("On a hike, 9 of the 12 hikers wore rain jackets. What percent wore rain jackets?",
                   "75%", ["9%", "25%", "90%"],
                   "%s = %s = <b>75%%</b>. 25%% is the hikers without jackets, and 90%% reads 9 as 90." % (fr(9, 12), fr(3, 4))))
    its.append(mcq(fig(percent_bar_svg("30 students", 10, 3, "3")) +
                   "The bar shows a class of 30 students. The shaded part is the students who walk to school. "
                   "What percent walk?",
                   "30%", ["3%", "9%", "70%"],
                   "3 of the 10 equal parts are shaded. Each part is 10%, so 3 parts are <b>30%</b> (9 students). "
                   "3% counts parts as percent, 9% uses the number of students, and 70% is the students who do not walk."))
    its.append(mcq("A muffin mix has flour and sugar in the ratio 4:1. What percent of the mix is sugar?",
                   "20%", ["25%", "80%", "41%"],
                   "Each group has 4 + 1 = 5 cups. Sugar is %s = <b>20%%</b>. 25%% is %s, sugar to flour (part to part), "
                   "and 80%% is the flour." % (fr(1, 5), fr(1, 4))))
    its.append(mcq("Which is <b>not</b> equal to %s?" % fr(3, 4), "34%", ["75%", "0.75", fr(6, 8)],
                   "%s = %s = 0.75 = 75%%. <b>34%%</b> just writes the digits 3 and 4." % (fr(3, 4), fr(6, 8)), same_ok=True))
    its.append(mcq("35% of the students in a class bike to school. What is the ratio of students who bike to students who do not?",
                   R(7, 13), [R(7, 20), R(13, 7), R(13, 20)],
                   "35 out of 100 bike, so 65 do not. 35:65. Divide both terms by 5: <b>7:13</b>. "
                   "7:20 is 35:100, bikers to the whole class (part to whole)."))
    its.append(mcq("The ratio of boys to girls in a club is 5:4. The number of boys is what percent of the number of girls?",
                   "125%", ["80%", "54%", "about 56%"],
                   "Boys ÷ girls = %s = 1.25 = <b>125%%</b>. 80%% is girls as a percent of boys, "
                   "and about 56%% is %s, boys out of the whole club." % (fr(5, 4), fr(5, 9))))
    its.append(mcq("In Class A, 12 of 20 students ski. In Class B, 15 of 25 students ski. Which class has the greater "
                   "percent of skiers?",
                   "They are the same", ["Class A", "Class B", CANT],
                   "Class A: %s = %s = 60%%. Class B: %s = %s = 60%%. <b>They are the same</b>, "
                   "even though Class B has more skiers." % (fr(12, 20), fr(60, 100), fr(15, 25), fr(60, 100))))
    its.append(mcq("Mix A has juice and water in the ratio 3:7. Mix B has juice and water in the ratio 2:3. "
                   "Which mix has the greater percent of juice?",
                   "Mix B", ["Mix A", "They are the same", CANT],
                   "Mix A: %s = 30%% juice. Mix B: %s = 40%% juice. So <b>Mix B</b>. "
                   "Mix A has more cups of juice in its ratio, but it also has much more water." % (fr(3, 10), fr(2, 5))))
    its.append(mcq("60% of the trees in a park are cedars. What is the ratio of cedars to other trees?",
                   R(3, 2), [R(3, 5), R(2, 3), R(2, 5)],
                   "60% are cedars, so 40% are other trees. 60:40 = <b>3:2</b>. "
                   "3:5 is 60:100, cedars to all the trees (part to whole)."))
    its.append(mcq("Write %s as a percent." % fr(3, 8), "37.5%", ["38%", "3.8%", "62.5%"],
                   "3 ÷ 8 = 0.375 = <b>37.5%%</b>. Check: %s = 12.5%%, and 3 × 12.5%% = 37.5%%. "
                   "38%% just writes the digits, and 62.5%% is %s." % (fr(1, 8), fr(5, 8))))
    its.append(mcq("On a bus there is 1 adult for every 7 kids. What percent of the people on the bus are adults?",
                   "12.5%", ["about 14%", "17%", "87.5%"],
                   "Each group has 1 + 7 = 8 people. Adults are %s = 0.125 = <b>12.5%%</b>. "
                   "About 14%% is %s, adults to kids (part to part), and 87.5%% is the kids." % (fr(1, 8), fr(1, 7))))
    its.append(mcq("The ratio of shaded parts to all the parts is 9:25. Write this as a decimal.",
                   "0.36", ["9.25", "0.09", "0.9"],
                   "%s = %s = <b>0.36</b>: multiply the top and bottom by 4. 9.25 just writes the digits, "
                   "and 0.9 is %s." % (fr(9, 25), fr(36, 100), fr(9, 10)), value=F(36, 100)))
    its.append(mcq("In a survey, 18 of 24 students chose soccer. Which shows the same amount in three ways?",
                   "%s = 0.75 = 75%%" % fr(3, 4),
                   ["%s = 0.18 = 18%%" % fr(18, 24), "%s = 0.34 = 34%%" % fr(3, 4), "%s = 0.75 = 7.5%%" % fr(3, 4)],
                   "%s = %s (divide by 6). 3 ÷ 4 = 0.75, and 0.75 = 75%%. So <b>%s = 0.75 = 75%%</b>."
                   % (fr(18, 24), fr(3, 4), fr(3, 4))))
    assert len(its) == 20, len(its)
    return {"title": "Ratios as fractions, decimals and percents", "items": its}


# ============================================================ set 4: unit rates and best buys
def set_rates():
    its = []
    its.append(mcq("A car drives 270 km in 3 hours at a steady speed. What is its speed?",
                   "90 km/h", ["810 km/h", "267 km/h", "273 km/h"],
                   "A unit rate is the amount for <b>1</b> hour: 270 ÷ 3 = <b>90 km/h</b>. "
                   "810 multiplies instead of dividing, and 267 subtracts.", value=90))
    its.append(mcq("A pack of 6 juice boxes costs $4.50. What is the cost of 1 juice box?",
                   "75¢", ["$7.50", "$27", "$10.50"],
                   "$4.50 ÷ 6: 450¢ ÷ 6 = <b>75¢</b>. $7.50 puts the decimal point in the wrong place, "
                   "$27 multiplies, and $10.50 adds.", value=F(75, 100)))
    its.append(mcq("Pencils are 4 for $1.80. What is the cost of 1 pencil?",
                   "45¢", ["$7.20", "$4.50", "18¢"],
                   "$1.80 ÷ 4 = 180¢ ÷ 4 = <b>45¢</b>. $7.20 multiplies by 4, and 18¢ divides by 10.",
                   value=F(45, 100)))
    its.append(mcq("A hose fills a 90 L tub in 6 minutes. How many litres does it pour per minute?",
                   "15 L", ["540 L", "84 L", "96 L"],
                   "Litres for 1 minute: 90 ÷ 6 = <b>15 L</b>. 540 L multiplies, 84 L subtracts, and 96 L adds.", value=15))
    its.append(mcq("Arjun reads 135 pages in 5 days. He reads the same number of pages each day. "
                   "How many pages a day is that?", "27", ["675", "130", "140"],
                   "Pages for 1 day: 135 ÷ 5 = <b>27</b>. 675 multiplies, and 130 subtracts.", value=27))
    its.append(mcq(fig(ratio_table_svg(["Distance (km)", "Time (h)"], [["80", "160", "?"], ["1", "2", "4"]], "rate table")) +
                   "A bus drives at a steady speed. What distance is missing?",
                   "320", ["240", "164", "640"],
                   "The unit rate is 80 km in 1 h. In 4 h: 80 × 4 = <b>320 km</b>. "
                   "240 adds only one more 80, but 4 h is 2 hours after 2 h. 164 adds 4.", value=320))
    its.append(mcq("Leah’s heart beats 18 times in 15 seconds. At this rate, how many times does it beat in 1 minute?",
                   "72", ["1080", "33", "270"],
                   "1 minute = 60 seconds = 4 × 15 seconds. 18 × 4 = <b>72</b> beats per minute. "
                   "1080 multiplies by 60, but 18 beats is for 15 seconds, not 1 second.", value=72))
    its.append(mcq("Owen cycles 21 km in 1.5 hours. What is his average speed?",
                   "14 km/h", ["31.5 km/h", "19.5 km/h", "22.5 km/h"],
                   "Speed = distance ÷ time: 21 ÷ 1.5 = <b>14 km/h</b>. Check: 14 + 7 = 21 km in 1.5 h. "
                   "31.5 multiplies, and 19.5 subtracts.", value=14))
    its.append(mcq("Ava earns $48 for 4 hours of babysitting. At the same rate, how much does she earn in 7 hours?",
                   "$84", ["$51", "$336", "$72"],
                   "Unit rate: $48 ÷ 4 = $12 an hour. 7 hours: 7 × $12 = <b>$84</b>. "
                   "$51 adds 3 dollars instead of 3 hours, and $72 is only 6 hours.", value=84))
    its.append(mcq("Which is the better buy for milk?", "4 L for $6.40",
                   ["2 L for $3.50", "They cost the same per litre", CANT],
                   "Find the price for 1 L. 4 L: $6.40 ÷ 4 = $1.60. 2 L: $3.50 ÷ 2 = $1.75. "
                   "<b>4 L for $6.40</b> costs less per litre, even though its price is higher."))
    its.append(mcq("Which is the better buy for cereal?", "750 g for $5.25",
                   ["1 kg for $7.20", "They cost the same per 100 g", CANT],
                   "Price per 100 g. 750 g: $5.25 ÷ 7.5 = 70¢. 1 kg = 1000 g: $7.20 ÷ 10 = 72¢. "
                   "<b>750 g for $5.25</b> is cheaper per 100 g. A bigger box is not always the better buy."))
    its.append(mcq("Which is the best buy for apple juice?", "2 L for $4.20",
                   ["1 L for $2.40", "500 mL for $1.15", "3 L for $6.60"],
                   "Price per litre: 1 L is $2.40, 2 L is $4.20 ÷ 2 = $2.10, 500 mL is 2 × $1.15 = $2.30, "
                   "and 3 L is $6.60 ÷ 3 = $2.20. The lowest is <b>2 L for $4.20</b>."))
    its.append(mcq("A 6-pack of yogurt costs $4.86. What is the cost of 1 yogurt?",
                   "81¢", ["$8.10", "$29.16", "$1.62"],
                   "$4.86 ÷ 6: 486¢ ÷ 6 = <b>81¢</b>. $8.10 puts the decimal point in the wrong place, "
                   "$29.16 multiplies, and $1.62 divides by 3.", value=F(81, 100)))
    its.append(mcq("A car uses 6 L of gas for every 100 km. How much gas does it use for 250 km?",
                   "15 L", ["12 L", "18 L", "150 L"],
                   "250 km = 2.5 × 100 km. 6 × 2.5 = <b>15 L</b>. 12 L forgets the last 50 km, "
                   "and 18 L counts 300 km.", value=15))
    its.append(mcq("Mei swims 400 m in 8 minutes. Owen swims 300 m in 5 minutes. Who swims faster?",
                   "Owen", ["Mei", "They swim at the same speed", CANT],
                   "Metres per minute: Mei 400 ÷ 8 = 50 m. Owen 300 ÷ 5 = 60 m. 60 &gt; 50, so <b>Owen</b> is faster, "
                   "even though Mei swims farther."))
    its.append(mcq(fig(double_line_svg("km", ["0", "?", "?", "?", "312"], "h", ["0", "1", "2", "3", "4"])) +
                   "A family drives at a steady speed. What is their speed?",
                   "78 km/h", ["62.4 km/h", "104 km/h", "312 km/h"],
                   "312 km in 4 h. Speed = 312 ÷ 4 = <b>78 km/h</b>. 62.4 divides by 5, the number of marks, "
                   "and 104 divides by 3.", value=78))
    its.append(mcq("A 2.5 kg bag of apples costs $6.25. What is the price per kilogram?",
                   "$2.50", ["$3.75", "40¢", "$8.75"],
                   "$6.25 ÷ 2.5 = <b>$2.50</b> per kg. Check: 2.5 × $2.50 = $6.25. $3.75 subtracts, "
                   "40¢ divides 2.5 by 6.25 (the wrong way), and $8.75 adds.", value=F(5, 2)))
    its.append(mcq("On Grouse Mountain, snow falls at 3 cm per hour. How long does it take for 21 cm to fall?",
                   "7 h", ["63 h", "18 h", "24 h"],
                   "21 ÷ 3 = <b>7 h</b>. Check: 3 × 7 = 21. 63 multiplies, and 18 subtracts.", value=7))
    its.append(mcq("Which is the better buy for rice?", "600 g for $5.10",
                   ["400 g for $3.60", "They cost the same per 100 g", CANT],
                   "Price per 100 g. 400 g: $3.60 ÷ 4 = 90¢. 600 g: $5.10 ÷ 6 = 85¢. "
                   "<b>600 g for $5.10</b> is cheaper per 100 g."))
    its.append(mcq("3 kg of carrots cost $4.20. At the same price per kilogram, what do 5 kg cost?",
                   "$7", ["$6.20", "$21", "$8.40"],
                   "Unit price: $4.20 ÷ 3 = $1.40 per kg. 5 × $1.40 = <b>$7</b>. "
                   "$6.20 adds 2 dollars for 2 more kilograms, and $8.40 is the price of 6 kg.", value=7))
    assert len(its) == 20, len(its)
    return {"title": "Unit rates and best buys", "items": its}


# ============================================================ set 5: word problems
def set_problems():
    its = []
    its.append(mcq("Chloe mixes blue and yellow paint in the ratio 2:3 to make green for an art project. "
                   "She uses 8 mL of blue. How much yellow does she need?",
                   "12 mL", ["9 mL", "20 mL", "4 mL"],
                   "2 × 4 = 8, so multiply the yellow by 4 too: 3 × 4 = <b>12 mL</b>. "
                   "9 mL adds 6 like 2 + 6 = 8, and 20 mL is the total paint.", value=12))
    its.append(mcq("To make pink paint, Simran mixes red and white in the ratio 1:4. She wants 500 mL of pink paint. "
                   "How much red does she need?",
                   "100 mL", ["125 mL", "400 mL", "200 mL"],
                   "Each batch has 1 + 4 = 5 parts. 500 ÷ 5 = 100 mL per part. Red is 1 part: <b>100 mL</b>. "
                   "125 mL divides by 4 (part to part), 400 mL is the white, and 200 mL is 2 parts.", value=100))
    its.append(mcq("A muffin recipe makes 12 muffins with 2 eggs. The class bake sale needs 30 muffins. "
                   "How many eggs are needed?",
                   "5", ["20", "4", "6"],
                   "12 muffins for 2 eggs is 6 muffins per egg. 30 ÷ 6 = <b>5</b> eggs. "
                   "20 adds 18 eggs because there are 18 more muffins, and 4 eggs only make 24 muffins.", value=5))
    its.append(mcq("A blueberry muffin recipe uses 1.5 cups of blueberries for 12 muffins. "
                   "How many cups are needed for 36 muffins?",
                   "4.5 cups", ["25.5 cups", "3 cups", "54 cups"],
                   "36 = 12 × 3, so 1.5 × 3 = <b>4.5 cups</b>. 25.5 adds 24 like the muffins, "
                   "and 3 cups only makes 24 muffins.", value=F(9, 2)))
    its.append(mcq("A muffin recipe uses flour and sugar in the ratio 5:2. Sofia uses 7.5 cups of flour. "
                   "How much sugar does she need?",
                   "3 cups", ["4.5 cups", "18.75 cups", "2.5 cups"],
                   "5 × 1.5 = 7.5, so 2 × 1.5 = <b>3 cups</b>. 4.5 adds 2.5 like 5 + 2.5 = 7.5, "
                   "and 18.75 uses the ratio the wrong way round.", value=3))
    its.append(mcq("A school rule says 1 adult for every 6 kids on a field trip. 42 kids are going to Science World. "
                   "How many adults are needed?",
                   "7", ["36", "252", "8"],
                   "42 ÷ 6 = <b>7</b> adults. 36 subtracts 6, and 252 multiplies.", value=7))
    its.append(mcq("There must be at least 1 adult for every 8 kids on a field trip to Stanley Park. 52 kids are going. "
                   "What is the fewest number of adults needed?",
                   "7", ["6", "6.5", "44"],
                   "52 ÷ 8 = 6.5. 6 adults can take only 48 kids, so 4 kids would have no adult. "
                   "You can’t have half an adult, so round up to <b>7</b>.", value=7))
    its.append(mcq("On a field trip to the Vancouver Aquarium, the ratio of kids to adults is 15:2. "
                   "There are 6 adults. How many kids are there?",
                   "45", ["19", "90", "51"],
                   "2 × 3 = 6, so the kids are 15 × 3 = <b>45</b>. 19 adds 4 like 2 + 4 = 6, "
                   "and 51 is everyone on the trip.", value=45))
    its.append(mcq("On a field trip bus, the ratio of kids to adults is 5:1. There are 48 people on the bus. "
                   "How many adults are there?",
                   "8", ["40", "9.6", "43"],
                   "Each group has 5 + 1 = 6 people. 48 ÷ 6 = <b>8</b> groups, so there are 8 adults and 40 kids. "
                   "9.6 treats 48 as the number of kids (48 ÷ 5).", value=8))
    its.append(mcq("Harjot hikes 9 km in 2 hours on a trail near Whistler. At the same rate, how far does he hike in 5 hours?",
                   "22.5 km", ["12 km", "45 km", "18 km"],
                   "Unit rate: 9 ÷ 2 = 4.5 km per hour. 5 × 4.5 = <b>22.5 km</b>. 12 km adds 3 for 3 more hours, "
                   "and 18 km is only 4 hours.", value=F(45, 2)))
    its.append(mcq("Smoked salmon costs $9 for 200 g or $12.90 for 300 g. Which is the better buy?",
                   "300 g for $12.90", ["200 g for $9", "They cost the same per 100 g", CANT],
                   "Price per 100 g: $9 ÷ 2 = $4.50 and $12.90 ÷ 3 = $4.30. <b>300 g for $12.90</b> costs less per 100 g."))
    its.append(mcq("For the Terry Fox Run, 120 of the 160 students in a school run the full route. "
                   "What percent is that?",
                   "75%", ["25%", "40%", "34%"],
                   "%s = %s = <b>75%%</b>. 25%% is the students who did not, 40%% uses the 40 students who did not, "
                   "and 34%% writes 3:4 as digits." % (fr(120, 160), fr(3, 4))))
    its.append(mcq("A can of paint is mixed from white and blue in the ratio 7:3. What percent of the paint is blue?",
                   "30%", ["about 43%", "70%", "73%"],
                   "Each batch has 7 + 3 = 10 parts. Blue is %s = <b>30%%</b>. About 43%% is %s, blue to white (part to part), "
                   "and 70%% is the white." % (fr(3, 10), fr(3, 7))))
    its.append(mcq("A salmon chowder recipe serves 6 people and uses 900 g of salmon. "
                   "How much salmon is needed to serve 4 people?",
                   "600 g", ["450 g", "1350 g", "150 g"],
                   "Unit rate: 900 ÷ 6 = 150 g per person. 4 × 150 = <b>600 g</b>. 450 g is for 3 people, "
                   "1350 g multiplies by 1.5 instead of dividing, and 150 g is for 1 person.", value=600))
    its.append(mcq("Mateo makes green paint with blue and yellow in the ratio 2:3. Kai uses the ratio 3:4. "
                   "Whose paint has the greater part of blue?",
                   "Kai’s", ["Mateo’s", "They are the same", CANT],
                   "Mateo: %s = 40%% blue. Kai: %s ≈ 43%% blue. So <b>Kai’s</b> paint is bluer. "
                   "Both have 1 more part yellow than blue, but that does not make the ratios equal." % (fr(2, 5), fr(3, 7))))
    its.append(mcq("A field trip must have at least 1 adult for every 10 kids. 45 kids are going, and 4 adults have signed up. "
                   "How many <b>more</b> adults are needed?",
                   "1", ["5", "0", "4.5"],
                   "4 adults can take only 40 kids. 45 kids need 5 adults (45 ÷ 10 = 4.5, round up). 5 − 4 = <b>1</b> more. "
                   "5 is how many adults in all.", value=1))
    its.append(mcq("A lacrosse team buys 15 balls for $33.75. At the same price, what do 24 balls cost?",
                   "$54", ["$42.75", "$2.25", "$67.50"],
                   "Unit price: $33.75 ÷ 15 = $2.25 a ball. 24 × $2.25 = <b>$54</b>. "
                   "$42.75 adds $9 for 9 more balls, and $67.50 is the price of 30 balls.", value=54))
    its.append(mcq("A ferry crosses 36 km in 1.5 hours. What is its average speed?",
                   "24 km/h", ["54 km/h", "34.5 km/h", "37.5 km/h"],
                   "Speed = distance ÷ time: 36 ÷ 1.5 = <b>24 km/h</b>. Check: 24 + 12 = 36 km in 1.5 h. "
                   "54 km/h multiplies, and 34.5 subtracts.", value=24))
    its.append(mcq("30 Grade 7 students vote on a field trip. The ratio of votes for Science World to votes for the aquarium "
                   "is 3:2. How many more students voted for Science World?",
                   "6", ["1", "18", "12"],
                   "Each group has 3 + 2 = 5 votes. 30 ÷ 5 = 6 groups. Science World: 3 × 6 = 18. Aquarium: 2 × 6 = 12. "
                   "18 − 12 = <b>6</b> more. 1 is only 3 − 2.", value=6))
    its.append(mcq("Liam mixes juice concentrate and water in the ratio 1:4. He uses 300 mL of concentrate. "
                   "How much juice does he make in all?",
                   "1500 mL", ["1200 mL", "375 mL", "75 mL"],
                   "Water: 4 × 300 = 1200 mL. Total: 300 + 1200 = <b>1500 mL</b>. 1200 mL is only the water, "
                   "375 mL treats 300 mL as the water, and 75 mL divides 300 by 4.", value=1500))
    assert len(its) == 20, len(its)
    return {"title": "Word problems: paint, muffins and field trips", "items": its}


# ============================================================ lesson
def body_html():
    f_cnt = counters_svg((3, "red"), (5, "blue"))
    f_tab = ratio_table_svg(["Flour (cups)", "Eggs"], [["2", "4", "6", "10"], ["3", "6", "9", "15"]])
    f_bar = percent_bar_svg("40 counters", 5, 2, "8")
    f_dl = double_line_svg("km", ["0", "80", "160", "240"], "h", ["0", "1", "2", "3"])
    return (
        "<h2>What a ratio is</h2>"
        "<p>A <b>ratio</b> compares two amounts. 3:5 is read “3 to 5”. Keep the order of the words: "
        "red to blue means the red number comes first.</p>"
        "<p>A <b>part-to-part</b> ratio compares two parts. A <b>part-to-whole</b> ratio compares one part with "
        "everything. Only part to whole can be written as a fraction of the group.</p>"
        "<figure class='sn-fig'>" + f_cnt +
        "<figcaption>Red to blue is 3:5 (part to part). Red to all is 3:8, so " + fr(3, 8) +
        " of the counters are red (part to whole).</figcaption></figure>"
        "<h2>Equivalent ratios and ratio tables</h2>"
        "<p>Multiply or divide <b>both</b> terms by the same number. Never add the same number to both terms.</p>"
        "<figure class='sn-fig'>" + f_tab +
        "<figcaption>Every column is 2:3 times a number. 15 = 3 × 5, so the flour is 2 × 5 = 10 cups.</figcaption></figure>"
        + ex("Example", "Find the missing term: 3:4 = ?:20",
             "4 × 5 = 20, so multiply 3 by 5 too.", "15")
        + "<h2>Ratios as fractions, decimals and percents</h2>"
        "<p>Turn a ratio into part to whole first. Then write the fraction, the decimal and the percent.</p>"
        "<figure class='sn-fig'>" + f_bar +
        "<figcaption>Red to blue is 2:3, so every 5 counters have 2 red. With 40 counters, each fifth is 8: "
        "red is 2 × 8 = 16, which is " + fr(2, 5) + " = 0.4 = 40%.</figcaption></figure>"
        + ex("Example", "In a choir, girls to boys is 3:2. What percent are girls?",
             "Each group has 3 + 2 = 5 singers. Girls: " + fr(3, 5) + " = " + fr(60, 100) + ".", "60%")
        + "<h2>Unit rates and best buys</h2>"
        "<p>A <b>rate</b> compares two different units, like km and hours or dollars and grams. "
        "A <b>unit rate</b> is the amount for 1: divide to find it. Then multiply to find any other amount.</p>"
        "<figure class='sn-fig'>" + f_dl +
        "<figcaption>80 km in 1 h is the unit rate: 80 km/h. In 3 h the car goes 3 × 80 = 240 km.</figcaption></figure>"
        + ex("Best buy", "Milk: 4 L for $6.40 or 2 L for $3.50?",
             "Price for 1 L: $6.40 ÷ 4 = $1.60 and $3.50 ÷ 2 = $1.75.", "4 L for $6.40")
        + ex("Part of a total", "Kids to adults on a field trip bus is 5:1. There are 48 people. How many adults?",
             "Each group has 5 + 1 = 6 people. 48 ÷ 6 = 8 groups, and each group has 1 adult.", "8 adults")
        + "<h2>Common mistakes</h2>"
        + table(["Mistake", "What to do instead"], [
            ["Red to blue is 2:3, so " + fr(2, 3) + " are red", "2:3 is part to part. The whole is 2 + 3 = 5, so " + fr(2, 5) + " are red"],
            ["2:5 = 5:8 (add 3 to both)", "Multiply both terms: 2:5 = 6:15"],
            ["Ratio table 4, 8, ? and 6, 12, 21: 12 + 9 = 21, so 8 + 9 = 17", "21 = 3 × 7, and 4:6 = 2:3, so 2 × 7 = 14"],
            ["270 km in 3 h = 810 km/h", "Unit rate: divide. 270 ÷ 3 = 90 km/h"],
            ["The bigger package is always the better buy", "Compare the price for 1 L, 1 kg or 100 g"],
        ])
    )


FAQ = [
    {"q": "What do Grade 7 students learn about ratios in BC?",
     "a": "In the BC Grade 7 math curriculum, students study the relationships between decimals, fractions, ratios and percents. They write ratios, find equivalent ratios, and turn a ratio into a fraction, a decimal or a percent."},
    {"q": "What is the difference between a part-to-part and a part-to-whole ratio?",
     "a": "Part to part compares two groups, like 3 red to 5 blue (3:5). Part to whole compares one group with everything, like 3 red out of 8 counters (3:8), which is the fraction 3/8."},
    {"q": "How do you use a ratio table?",
     "a": "Multiply or divide both rows by the same number to get each new column. For 2:3, the columns are 4:6, 6:9 and 10:15; adding the same number to both rows does not keep the ratio."},
    {"q": "Are ratios on the Grade 7 FSA?",
     "a": "The Grade 7 FSA numeracy section asks students to reason with numbers in real situations. Ratios, unit rates and percents often appear in those problems, so this practice helps."},
]


def mark_large(u, pattern):
    """Tag wide pictures so they print larger and stay readable."""
    rx = re.compile(r"<svg (?=[^>]*aria-label='" + pattern + ")")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u


def gen():
    rnd = random.Random(37807)
    sets = [set_pictures(), set_equivalent(), set_percents(), set_rates(), set_problems()]
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
        "country": "ca-bc", "subject": "math", "grade": "grade-7", "slug": SLUG, "sort": 7,
        "updated": UPDATED, "pdf_url": "",
        "title": "Ratios: Part to Part, Ratio Tables, Percents and Unit Rates",
        "seo_title": "Grade 7 Ratios Worksheets (BC Curriculum) – Free Math with Answer Key",
        "short_title": "Ratios",
        "domain": "Number",
        "standard_code": "Grade 7: Number",
        "standard_url": "https://curriculum.gov.bc.ca/curriculum/mathematics/7/core",
        "standard_text": "Relationships between decimals, fractions, ratios, and percents",
        "meta_desc": "Free Grade 7 ratio worksheets for the BC math curriculum: part-to-part and part-to-whole ratios, equivalent ratios and ratio tables, ratios as fractions, decimals and percents, unit rates and best buys. 100 questions with an answer key. Good FSA practice.",
        "key_big": "Multiply or divide both terms by the same number. A ratio of 2:3 means 2 out of every 5, not 2/3.",
        "key_sub": "Part to part (2:3) compares two groups; part to whole (2:5) is the fraction 2/5 = 40%. For a unit rate, divide to find the amount for 1.",
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
