# -*- coding: utf-8 -*-
"""
Singapore Primary 2 Maths: Picture Graphs
(MOE 2021 Primary Mathematics Syllabus, Standard, Primary 2: Statistics — picture graphs with scales)
  python3 tools/gen_sg_maths_p2_picture_graphs.py
Read picture graphs where 1 picture stands for 1, then picture graphs with scales (1 picture stands for
2, 5 or 10), find the most and the fewest, how many more and how many fewer, totals, and solve word
problems (favourite recess food, books read) in Singapore settings, with bar models.
Wrong answers come from real mistakes: counting the pictures instead of their value (ignoring the key),
using the wrong scale, miscounting by one picture, reading the next row, adding when the question asks
“how many more”, subtracting when it asks “altogether”, and leaving out a row in a total.
Every value, difference and total is checked in code. HTML attributes use single quotes.
Primary 2: short sentences for 7-8-year-olds.
"""
import json, math, os, random, re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "sg", "maths", "primary-2")
UPDATED = "2026-11-03"
GREEN = "#006633"
FILL = "#cfe6d6"
FILL2 = "#e6f2ea"
RED = "#c0392b"
GOLD = "#e3a81b"
BLUE = "#2f6db5"
INK = "#2b2b2b"
GRID = "#c9d3cc"
FONT = "Arial, Helvetica, sans-serif"


# ------------------------------------------------------------ helpers
def mcq(q, correct, cands, e):
    """4 choices: correct + the first 3 unique distractors. Positions are set by balance()."""
    correct = str(correct)
    seen = {correct}
    pick = []
    for c in cands:
        c = str(c)
        if c in seen or not c or c.startswith("-") or c.startswith("0 "):
            continue
        seen.add(c)
        pick.append(c)
        if len(pick) == 3:
            break
    assert len(pick) == 3, (q, correct, cands)
    return {"q": q, "c": [correct] + pick, "a": 0, "e": e}


def balance(sets, rnd):
    """Spread the correct answers evenly (5/5/5/5) over the 4 positions in every set."""
    for s in sets:
        targets = [p for p in range(4) for _ in range(5)]
        rnd.shuffle(targets)
        assert len(s["items"]) == len(targets)
        for it, t in zip(s["items"], targets):
            c = it["c"]
            right = c[it["a"]]
            wrong = [x for i, x in enumerate(c) if i != it["a"]]
            rnd.shuffle(wrong)
            it["c"] = wrong[:t] + [right] + wrong[t:]
            it["a"] = t


def fig(svg):
    return "<div class='qfig'>" + svg + "</div>"


def svg_wrap(w, h, body, label):
    w, h = int(math.ceil(w)), int(math.ceil(h))
    return ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 %d %d' width='%d' height='%d' "
            "role='img' aria-label='%s'><g font-family='%s'>%s</g></svg>" % (w, h, w, h, label, FONT, body))


def tw(t, fs, bold=False):
    """Approximate text width in px (Arial)."""
    return len(str(t)) * fs * (0.62 if bold else 0.56)


def text(x, y, t, fs=15, anchor="middle", bold=False, col=INK):
    return ("<text x='%.1f' y='%.1f' font-size='%d'%s fill='%s' text-anchor='%s'>%s</text>"
            % (x, y, fs, " font-weight='700'" if bold else "", col, anchor, t))


def table(head, rows):
    h = "".join("<th>%s</th>" % x for x in head)
    b = "".join("<tr>" + "".join("<td>%s</td>" % c for c in r) + "</tr>" for r in rows)
    return "<div class='sn-tw'><table class='sn-table'><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>" % (h, b)


def ex(title, q, s, a):
    return ("<div class='sn-ex'><span class='sn-ex-t'>%s</span><p class='sn-ex-q'>%s</p>"
            "<p class='sn-ex-s'>%s</p><p class='sn-ex-a'>Answer: %s</p></div>" % (title, q, s, a))


def fmt(v, unit):
    return "%d %s" % (v, unit[0] if v == 1 else unit[1])


def count_in(step, n):
    return ", ".join(str(step * t) for t in range(1, n + 1))


def times(n, key):
    """The counting step shown in explanations."""
    if key == 1:
        return "Count the pictures: %s." % count_in(1, n)
    return "Count in %ss: %s." % (key, count_in(key, n))


# ------------------------------------------------------------ picture symbols (about 20 x 20)
def star_pts(cx, cy, R=10.0, r=4.2):
    pts = []
    for i in range(10):
        ang = -math.pi / 2 + i * math.pi / 5
        rad = R if i % 2 == 0 else r
        pts.append((cx + rad * math.cos(ang), cy + 1 + rad * math.sin(ang)))
    return pts


def symbol(kind, cx, cy):
    if kind == "face":
        return ("<circle cx='%.1f' cy='%.1f' r='9.5' fill='%s' stroke='%s' stroke-width='1.2'/>"
                "<circle cx='%.1f' cy='%.1f' r='1.5' fill='%s'/><circle cx='%.1f' cy='%.1f' r='1.5' fill='%s'/>"
                "<path d='M%.1f %.1f Q%.1f %.1f %.1f %.1f' fill='none' stroke='%s' stroke-width='1.4'/>"
                % (cx, cy, GOLD, INK, cx - 3.4, cy - 2.6, INK, cx + 3.4, cy - 2.6, INK,
                   cx - 4.6, cy + 2.4, cx, cy + 7, cx + 4.6, cy + 2.4, INK))
    if kind == "star":
        return "<polygon points='%s' fill='%s' stroke='%s' stroke-width='1'/>" % (
            " ".join("%.1f,%.1f" % p for p in star_pts(cx, cy)), GOLD, INK)
    if kind == "book":
        return ("<rect x='%.1f' y='%.1f' width='16' height='19' rx='1.5' fill='%s' stroke='%s' stroke-width='1.2'/>"
                "<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='#ffffff' stroke-width='1.6'/>"
                % (cx - 8, cy - 9.5, BLUE, INK, cx - 4.5, cy - 8.5, cx - 4.5, cy + 8.5))
    if kind == "cup":
        return ("<path d='M%.1f %.1f L%.1f %.1f L%.1f %.1f L%.1f %.1f Z' fill='%s' stroke='%s' stroke-width='1.2'/>"
                "<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='1.2'/>"
                % (cx - 8, cy - 8, cx + 8, cy - 8, cx + 5.5, cy + 9.5, cx - 5.5, cy + 9.5, RED, INK,
                   cx + 2, cy - 8, cx + 5, cy - 13, INK))
    assert kind == "circle"
    return "<circle cx='%.1f' cy='%.1f' r='9' fill='%s' stroke='%s' stroke-width='1.2'/>" % (cx, cy, GREEN, INK)


# ------------------------------------------------------------ picture graph data
class Graph:
    def __init__(self, title, cats, vals, key, sym, unit, how, more, fewer, both, total, most, fewest,
                 ph=None, sumq=None):
        assert len(set(vals)) == len(vals) and all(v % key == 0 for v in vals)
        self.title, self.cats, self.vals, self.key, self.sym, self.unit = title, cats, vals, key, sym, unit
        self.how_f, self.more_f, self.fewer_f, self.both_f = how, more, fewer, both
        self.total_q, self.most_q, self.fewest_q = total, most, fewest
        self.ph = ph or {}
        self.d = dict(zip(cats, vals))

    def p(self, c):
        return self.ph.get(c, c.lower())

    def v(self, c):
        return self.d[c]

    def n(self, c):
        return self.d[c] // self.key

    def how(self, c):
        return self.how_f.format(a=self.p(c))

    def more(self, a, b):
        return self.more_f.format(a=self.p(a), b=self.p(b))

    def fewer(self, a, b):
        return self.fewer_f.format(a=self.p(a), b=self.p(b))

    def both(self, a, b):
        return self.both_f.format(a=self.p(a), b=self.p(b))

    def key_text(self):
        return "stands for " + fmt(self.key, self.unit)

    def key_words(self):
        return "Each picture stands for %s." % fmt(self.key, self.unit)

    def svg(self):
        return pic_svg(self)

    def fig(self):
        return fig(self.svg())

    def row_text(self, c):
        n, k = self.n(c), self.key
        if k == 1:
            return "The %s row has %d pictures. Each picture stands for 1." % (c, n)
        return "The %s row has %d pictures. Each picture stands for %d. %s" % (c, n, k, times(n, k))


def pic_svg(g):
    """Picture graph: one row per item, pictures worth g.key each, the key under the graph."""
    fs, rh, gap = 15, 28, 24
    lw = max(tw(c, fs) for c in g.cats) + 20
    m = max(max(g.n(c) for c in g.cats), 5)
    ktxt = g.key_text()
    kw = tw("Each", fs) + 34 + tw(ktxt, fs)
    W = int(max(lw + 10 + m * gap + 12, tw(g.title, 16, True) + 16, kw + 16))
    top = 30
    s = [text(W / 2.0, 20, g.title, 16, bold=True)]
    H_tab = len(g.cats) * rh
    s.append("<rect x='4' y='%d' width='%d' height='%d' fill='none' stroke='%s' stroke-width='1.5'/>"
             % (top, W - 8, H_tab, GREEN))
    s.append("<line x1='%.1f' y1='%d' x2='%.1f' y2='%d' stroke='%s' stroke-width='1.5'/>"
             % (lw, top, lw, top + H_tab, GREEN))
    for i, c in enumerate(g.cats):
        y = top + i * rh
        if i:
            s.append("<line x1='4' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='1'/>" % (y, W - 4, y, GRID))
        s.append(text(lw - 8, y + 19, c, fs, anchor="end"))
        for j in range(g.n(c)):
            s.append(symbol(g.sym, lw + 10 + j * gap + 11, y + rh / 2.0))
    ky = top + H_tab + 25
    x = (W - kw) / 2.0
    s.append(text(x, ky, "Each", fs, anchor="start"))
    x += tw("Each", fs) + 17
    s.append(symbol(g.sym, x, ky - 5))
    s.append(text(x + 17, ky, ktxt, fs, anchor="start"))
    return svg_wrap(W, ky + 9, "".join(s), "picture graph: " + g.title.lower())


# ------------------------------------------------------------ bar model (Singapore model method)
def bar_svg(rows, total=None, label="bar model"):
    """Bar model drawn to scale.
    rows = [(name, [(value, dashed)], [(first seg, last seg, text)], right text (optional))];
    total = text for a brace on the right spanning all the rows."""
    BW, BH = 270, 30
    LW = int(max([84] + [tw(r[0], 15) + 22 for r in rows]))
    big = max(sum(v for v, _ in r[1]) for r in rows)
    sc = BW / float(big)
    right = max([tw(r[3], 16, True) + 14 for r in rows if len(r) > 3] + [0])
    W = LW + BW + max(right, 84 if total else 14)
    y = 6
    s = []
    tops = []
    for row in rows:
        name, segs, over = row[:3]
        y += 24
        tops.append(y)
        s.append(text(LW - 10, y + BH / 2.0 + 5, name, 15, anchor="end"))
        xs = [LW]
        for v, dashed in segs:
            xs.append(xs[-1] + v * sc)
        for k, (v, dashed) in enumerate(segs):
            s.append("<rect x='%.1f' y='%d' width='%.1f' height='%d' fill='%s' stroke='%s' stroke-width='1.6'%s/>"
                     % (xs[k], y, xs[k + 1] - xs[k], BH, "#fff" if dashed else FILL, RED if dashed else INK,
                        " stroke-dasharray='5 4'" if dashed else ""))
        for a, b, t in over:
            x1, x2 = xs[a] + 1, xs[b + 1] - 1
            s.append("<path d='M%.1f %d L%.1f %d L%.1f %d L%.1f %d' fill='none' stroke='%s' stroke-width='1.4'/>"
                     % (x1, y - 2, x1, y - 7, x2, y - 7, x2, y - 2, INK))
            s.append(text((x1 + x2) / 2.0, y - 11, t, 14, col=RED if "?" in t else INK))
        if len(row) > 3:
            s.append(text(xs[-1] + 10, y + BH / 2.0 + 6, row[3], 16, anchor="start", bold=True, col=RED))
        y += BH + 12
    H = y
    if total:
        xb = LW + BW + 10
        y1, y2 = tops[0], tops[-1] + BH
        ym = (y1 + y2) / 2.0
        s.append("<path d='M%d %d q6 0 6 6 L%d %.1f q0 3 4 3 q-4 0 -4 3 L%d %d q0 6 -6 6' fill='none' "
                 "stroke='%s' stroke-width='1.6'/>" % (xb, y1, xb + 6, ym - 3, xb + 6, y2 - 6, INK))
        s.append(text(xb + 16, ym + 5, total, 15, anchor="start", col=RED if "?" in total else INK))
    return svg_wrap(W, H, "".join(s), label)


# ------------------------------------------------------------ question makers
def q_read(g, c, extra=""):
    """How many …? Mistakes: counting pictures, one picture more or less, the wrong scale, the next row."""
    v, n, k = g.v(c), g.n(c), g.key
    i = g.cats.index(c)
    nb = g.vals[i + 1] if i + 1 < len(g.vals) else g.vals[i - 1]
    if k == 1:
        cands = [v - 1, v + 1, nb, v + 2]
        why = "(%d is the %s row.)" % (nb, g.cats[g.vals.index(nb)])
    else:
        other = {2: 5, 5: 10, 10: 5}[k]
        cands = [n, v + k, v - k, n * other, nb]
        why = "Do not just count the pictures: %d pictures are not %s." % (n, fmt(n, g.unit))
    return mcq(g.fig() + extra + g.how(c), fmt(v, g.unit), [fmt(x, g.unit) for x in cands if x > 0],
               g.row_text(c) + " So the answer is <b>%s</b>. %s" % (fmt(v, g.unit), why))


def q_which(g, c, qtext):
    """Which row shows v? Mistake: picking the row with v pictures."""
    v, k = g.v(c), g.key
    others = [x for x in g.cats if x != c]
    trap = [x for x in others if g.v(x) == v * k] if k > 1 else []
    rest = [x for x in others if x not in trap]
    e = "Each picture stands for %d. %s has %d pictures. %s So %s shows %d." % (
        k, c, g.n(c), times(g.n(c), k), c, v)
    if k > 1 and any(g.n(x) == v for x in others):
        e += " The row with %d pictures does not show %d." % (v, v)
    return mcq(g.fig() + qtext, c, trap + rest, e)


def q_key(g):
    """What does each picture stand for? Mistakes: 1, the number of rows, another scale."""
    k = g.key
    cands = [1, 2, 5, 10, len(g.cats)]
    return mcq(g.fig() + "What does each picture stand for?", fmt(k, g.unit),
               [fmt(x, g.unit) for x in cands if x != k],
               "Look at the key under the graph: each picture stands for <b>%s</b>. "
               "Always read the key before you count." % fmt(k, g.unit))


def q_pics(g, value, who, qtext):
    """How many pictures for a value? Mistakes: the value itself, ×key instead of ÷key, one more."""
    k = g.key
    assert value % k == 0
    n = value // k
    cands = [value, n + 1, value * k if k > 1 else n + 2, n - 1]
    return mcq(g.fig() + qtext, "%d pictures" % n, ["%d pictures" % x for x in cands if x > 1],
               "Each picture stands for %d. Count in %ss until you reach %d: %s. That is <b>%d pictures</b>."
               % (k, k, value, count_in(k, n), n)
               if k > 1 else "Each picture stands for 1, so %d needs <b>%d pictures</b>." % (value, n))


def q_most(g, most=True, extra=""):
    order = sorted(g.cats, key=g.v, reverse=most)
    ans = order[0]
    cands = order[1:]
    word = "most" if most else "fewest"
    e = "The longest row" if most else "The shortest row"
    e += " has the %s pictures. %s has %d pictures, which is %s. " % (
        word, ans, g.n(ans), fmt(g.v(ans), g.unit))
    e += "All the pictures stand for the same number, so you can compare the rows."
    return mcq(g.fig() + extra + (g.most_q if most else g.fewest_q), ans, cands, e)


def q_diff(g, a, b, fewer=False):
    """How many more / fewer? Mistakes: the difference in pictures, adding, one picture off."""
    va, vb, k = g.v(a), g.v(b), g.key
    assert va > vb, (a, b)
    d = va - vb
    assert d > 0
    na, nb = g.n(a), g.n(b)
    cands = [abs(na - nb) if k > 1 else d + 1, va + vb, d + k, d - k if d > k else d + 2 * k]
    qtext = g.fewer(b, a) if fewer else g.more(a, b)
    big, small = (a, b) if g.v(a) > g.v(b) else (b, a)
    e = ("%s: %s. %s: %s. " % (big, fmt(g.v(big), g.unit), small, fmt(g.v(small), g.unit)) +
         "Subtract: %d − %d = <b>%d</b>." % (g.v(big), g.v(small), d))
    if k > 1:
        dp = g.n(big) - g.n(small)
        e += " Or: %s has %s more, and %d × %d = %d." % (big, "1 picture" if dp == 1 else "%d pictures" % dp, dp, k, d)
        e += " Do not stop at %d." % dp
    else:
        e += " Do not add."
    return mcq(g.fig() + qtext, fmt(d, g.unit), [fmt(x, g.unit) for x in cands if x > 0], e)


def q_both(g, a, b):
    """Altogether for two rows. Mistakes: pictures, subtracting, one picture off."""
    va, vb, k = g.v(a), g.v(b), g.key
    t = va + vb
    cands = [g.n(a) + g.n(b) if k > 1 else t - 1, abs(va - vb), t + k, t - k]
    e = "%s: %d. %s: %d. Add: %d + %d = <b>%d</b>." % (a, va, b, vb, va, vb, t)
    if k > 1:
        e += " Or count all %d pictures in %ss." % (g.n(a) + g.n(b), k)
    return mcq(g.fig() + g.both(a, b), fmt(t, g.unit), [fmt(x, g.unit) for x in cands if x > 0], e)


def q_total(g):
    """Total of every row. Mistakes: total pictures, leaving out the last row, one picture off."""
    t, k = sum(g.vals), g.key
    np_ = t // k
    cands = [np_ if k > 1 else t - 1, t - g.vals[-1], t + k, t - k]
    e = "Add all the rows: %s = <b>%d</b>." % (" + ".join(str(x) for x in g.vals), t)
    if k > 1:
        e += " Or: there are %d pictures, and each stands for %d. %d pictures is not %d." % (np_, k, np_, np_)
    return mcq(g.fig() + g.total_q, fmt(t, g.unit), [fmt(x, g.unit) for x in cands if x > 0], e)


def q_not(g, c, qtext):
    """How many did not choose c? Mistakes: c itself, the total, pictures."""
    t, v, k = sum(g.vals), g.v(c), g.key
    r = t - v
    cands = [(t - v) // k if k > 1 else r - 1, t, v, r + k]
    e = ("Add the other rows: %s = <b>%d</b>. Or take away from the total: %d − %d = %d."
         % (" + ".join(str(g.v(x)) for x in g.cats if x != c), r, t, v, r))
    return mcq(g.fig() + qtext, fmt(r, g.unit), [fmt(x, g.unit) for x in cands if x > 0], e)


STU = ("student", "students")
BK = ("book", "books")
ST = ("sticker", "stickers")


def sgraph(title, cats, vals, key, sym, verb_ph, thing, most, fewest, total=None, unit=STU):
    """Graph of students' choices. verb_ph: how the 'how many' question reads."""
    return Graph(title, cats, vals, key, sym, unit,
                 "How many students " + verb_ph + "?",
                 "How many more students " + verb_ph.replace("{a}", "{a}") + " than {b}?",
                 "How many fewer students " + verb_ph + " than {b}?",
                 "How many students " + verb_ph.replace("{a}", "{a} or {b}") + "?",
                 total or "How many students are there altogether?", most, fewest)


def pgraph(title, names, vals, key, sym, unit, verb, most, fewest, total):
    """Graph of what children have or did (books read, stickers)."""
    noun = unit[1]
    return Graph(title, names, vals, key, sym, unit,
                 "How many %s did {a} %s?" % (noun, verb),
                 "How many more %s did {a} %s than {b}?" % (noun, verb),
                 "How many fewer %s did {a} %s than {b}?" % (noun, verb),
                 "How many %s did {a} and {b} %s altogether?" % (noun, verb),
                 total, most, fewest, ph={c: c for c in names})


# ============================================================ set 1: 1 picture stands for 1
def set_one():
    its = []
    G1 = sgraph("How we come to school", ["MRT", "Bus", "Car", "Walk"], [6, 9, 4, 3], 1, "face",
                "come to school by {a}", "", "Which way to school is the most popular?",
                "Which way to school is the least popular?")
    G1.ph = {"MRT": "MRT", "Bus": "bus", "Car": "car"}
    G1.how_f = "How many students come to school by {a}?"
    its.append(q_read(G1, "MRT"))
    its.append(q_read(G1, "Bus"))
    G1w = Graph(G1.title, G1.cats, G1.vals, 1, "face", STU, "How many students walk to school?",
                "", "", "", "", "", "")
    its.append(q_read(G1w, "Walk"))
    its.append(q_which(G1, "Car", "Which row shows 4 students?"))
    its.append(q_most(G1, True))

    G2 = pgraph("Stickers we collected", ["Siti", "Jun Jie", "Priya", "Ethan"], [5, 8, 6, 3], 1, "star", ST,
                "collect", "Who collected the most stickers?", "Who collected the fewest stickers?",
                "How many stickers are there altogether?")
    its.append(q_read(G2, "Siti"))
    its.append(q_read(G2, "Jun Jie"))
    its.append(q_read(G2, "Ethan"))
    its.append(q_which(G2, "Priya", "Who collected 6 stickers?"))
    its.append(q_key(G2))

    G3 = sgraph("Our favourite fruit", ["Durian", "Rambutan", "Mango", "Watermelon"], [4, 7, 8, 5], 1, "face",
                "chose {a}", "", "Which fruit is the most popular?", "Which fruit is the least popular?")
    G3.ph = {"Durian": "durian", "Rambutan": "rambutan", "Mango": "mango", "Watermelon": "watermelon"}
    its.append(q_read(G3, "Rambutan"))
    its.append(q_read(G3, "Mango"))
    its.append(q_read(G3, "Watermelon"))
    its.append(q_which(G3, "Durian", "Which fruit did 4 students choose?"))
    its.append(q_most(G3, False))

    G4 = Graph("Books we borrowed", ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
               [4, 7, 2, 6, 5], 1, "book", BK, "How many books were borrowed on {a}?",
               "", "", "", "", "On which day were the most books borrowed?",
               "On which day were the fewest books borrowed?", ph={d: d for d in
                                                                  ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]})
    its.append(q_read(G4, "Tuesday"))
    its.append(q_read(G4, "Thursday"))
    its.append(q_read(G4, "Friday"))
    its.append(q_which(G4, "Wednesday", "On which day were 2 books borrowed?"))
    its.append(q_pics(G4, 3, "", "On Saturday, 3 books were borrowed. How many pictures should be drawn for Saturday?"))
    assert len(its) == 20, len(its)
    return {"title": "Picture graphs: 1 picture stands for 1", "items": its}


# ============================================================ set 2: scales of 2, 5 and 10
def set_scales():
    its = []
    H1 = sgraph("Our favourite CCA", ["Football", "Choir", "Art club", "Scouts"], [14, 10, 16, 8], 2, "face",
                "chose {a}", "", "Which CCA is the most popular?", "Which CCA is the least popular?")
    H1.ph = {"Football": "football", "Choir": "choir", "Art club": "art club", "Scouts": "scouts"}
    its.append(q_key(H1))
    its.append(q_read(H1, "Football"))
    its.append(q_read(H1, "Choir"))
    its.append(q_read(H1, "Art club"))
    its.append(q_pics(H1, 12, "Basketball", "12 students chose basketball. How many pictures are needed for basketball?"))

    H2 = pgraph("Stickers collected", ["Hui Min", "Zhi Hao", "Kavya", "Ryan"], [30, 20, 35, 15], 5, "star", ST,
                "collect", "Who collected the most stickers?", "Who collected the fewest stickers?",
                "How many stickers are there altogether?")
    its.append(q_key(H2))
    its.append(q_read(H2, "Hui Min"))
    its.append(q_read(H2, "Kavya"))
    its.append(q_read(H2, "Ryan"))
    its.append(q_which(H2, "Zhi Hao", "Who collected 20 stickers?"))

    CUP = ("cup", "cups")
    H3 = Graph("Drinks sold at recess", ["Milo", "Soya milk", "Orange juice", "Water"], [80, 50, 60, 30], 10, "cup",
               CUP, "How many cups of {a} were sold?", "", "", "", "", "", "",
               ph={"Milo": "Milo", "Soya milk": "soya milk", "Orange juice": "orange juice", "Water": "water"})
    its.append(q_read(H3, "Milo"))
    its.append(q_read(H3, "Soya milk"))
    its.append(q_read(H3, "Water"))
    its.append(q_which(H3, "Orange juice", "Which drink sold 60 cups?"))
    its.append(q_pics(H3, 40, "Lime juice", "40 cups of lime juice were sold. How many pictures should be drawn for lime juice?"))

    H4 = pgraph("Books read in May", ["Arjun", "Nurul", "Wei Ming", "Sarah"], [18, 12, 8, 14], 2, "book", BK,
                "read", "Who read the most books?", "Who read the fewest books?",
                "How many books did they read altogether?")
    its.append(q_read(H4, "Arjun"))
    its.append(q_read(H4, "Nurul"))
    its.append(q_read(H4, "Wei Ming"))
    its.append(q_which(H4, "Sarah", "Who read 14 books?"))
    its.append(q_pics(H4, 10, "Ahmad", "Ahmad read 10 books in May. How many pictures should be drawn for him?"))
    assert len(its) == 20, len(its)
    return {"title": "Picture graphs with scales: 2, 5 and 10", "items": its}


# ============================================================ set 3: most, fewest, how many more
def set_compare():
    its = []
    K1 = sgraph("Our favourite hawker food", ["Laksa", "Chicken rice", "Satay", "Fish soup"], [20, 40, 30, 25], 5,
                "face", "chose {a}", "", "Which food is the most popular?", "Which food is the least popular?")
    its.append(q_most(K1, True))
    its.append(q_most(K1, False))
    its.append(q_diff(K1, "Chicken rice", "Laksa"))
    its.append(q_diff(K1, "Satay", "Fish soup"))
    its.append(q_diff(K1, "Chicken rice", "Satay", fewer=True))

    DUR = ("durian", "durians")
    K2 = Graph("Durians sold at a stall", ["Friday", "Saturday", "Sunday", "Monday"], [60, 90, 80, 30], 10, "circle",
               DUR, "How many durians were sold on {a}?",
               "How many more durians were sold on {a} than on {b}?",
               "How many fewer durians were sold on {a} than on {b}?", "", "",
               "On which day were the most durians sold?", "On which day were the fewest durians sold?",
               ph={d: d for d in ["Friday", "Saturday", "Sunday", "Monday"]})
    its.append(q_most(K2, True))
    its.append(q_most(K2, False))
    its.append(q_diff(K2, "Saturday", "Friday"))
    its.append(q_diff(K2, "Sunday", "Monday"))
    its.append(q_diff(K2, "Saturday", "Monday", fewer=True))

    STAR = ("star", "stars")
    K3 = pgraph("Stars earned this week", ["Ali", "Farah", "Hafiz", "Devi"], [14, 18, 8, 12], 2, "star", STAR,
                "earn", "Who earned the most stars?", "Who earned the fewest stars?",
                "How many stars did they earn altogether?")
    its.append(q_most(K3, True))
    its.append(q_most(K3, False))
    its.append(q_diff(K3, "Farah", "Hafiz"))
    its.append(q_diff(K3, "Ali", "Devi"))
    its.append(q_diff(K3, "Farah", "Ali", fewer=True))

    K4 = sgraph("How P2 students go home", ["School bus", "MRT", "Car", "Walk"], [35, 20, 30, 10], 5, "face",
                "go home by {a}", "", "Which way do the most students go home?",
                "Which way do the fewest students go home?")
    K4.ph = {"School bus": "school bus", "MRT": "MRT", "Car": "car"}
    K4.more_f = "How many more students go home by {a} than by {b}?"
    its.append(q_diff(K4, "School bus", "MRT"))
    its.append(q_diff(K4, "Car", "MRT"))
    K4.fewer_f = "How many fewer students walk home than go home by {b}?"
    its.append(q_diff(K4, "Car", "Walk", fewer=True))
    # Which two rows differ by a given amount?
    its.append(mcq(K4.fig() + "Which way home has 15 more students than MRT?", "School bus", ["Walk", "Car", "MRT"],
                   "MRT has 20 students. 20 + 15 = 35. School bus has 7 pictures. %s So the answer is "
                   "<b>school bus</b>. (Car has 30, which is only 10 more.)" % times(7, 5)))
    assert 35 - 20 == 15 and 30 - 20 == 10
    its.append(mcq(K4.fig() + "Jun Jie says, “Car has 2 more pictures than MRT, so 2 more students go home by car.” "
                   "How many more students really go home by car than by MRT?", "10 students",
                   ["2 students", "50 students", "5 students"],
                   "Each picture stands for 5 students, so 2 more pictures is 5 + 5 = <b>10 students</b>. "
                   "Car: 30. MRT: 20. 30 − 20 = 10. Jun Jie counted pictures and forgot the key."))
    assert len(its) == 20, len(its)
    return {"title": "Most, fewest and how many more", "items": its}


# ============================================================ set 4: totals
def set_totals():
    its = []
    T1 = sgraph("Our favourite colour", ["Red", "Blue", "Yellow", "Green"], [12, 16, 6, 10], 2, "face",
                "chose {a}", "", "", "", total="How many students chose a colour altogether?")
    its.append(q_both(T1, "Red", "Blue"))
    its.append(q_both(T1, "Yellow", "Green"))
    its.append(q_total(T1))
    its.append(q_not(T1, "Blue", "How many students did not choose blue?"))
    pair = {("Red", "Blue"): 28, ("Red", "Green"): 22, ("Blue", "Yellow"): 22, ("Blue", "Green"): 26}
    for (x, y), t in pair.items():
        assert T1.v(x) + T1.v(y) == t
    its.append(mcq(T1.fig() + "Which two colours were chosen by 26 students altogether?", "Blue and green",
                   ["Red and blue", "Red and green", "Blue and yellow"],
                   "Blue: 16. Green: 10. 16 + 10 = <b>26</b>. Red and blue make 28, and red and green "
                   "make 22, and so do blue and yellow."))
    shells = ("shell", "shells")
    T2 = pgraph("Shells found at East Coast Park", ["Chloe", "Ahmad", "Mei Ling", "Kumar"], [35, 20, 30, 15], 5,
                "circle", shells, "find", "", "", "How many shells did they find altogether?")
    its.append(q_both(T2, "Chloe", "Ahmad"))
    its.append(q_both(T2, "Mei Ling", "Kumar"))
    its.append(q_total(T2))
    assert 20 + 15 == 35
    its.append(mcq(T2.fig() + "Who found more shells: Chloe, or Ahmad and Kumar together?",
                   "They found the same", ["Chloe", "Ahmad and Kumar", "Kumar"],
                   "Chloe found 35 shells. Ahmad and Kumar found 20 + 15 = 35 shells. "
                   "35 = 35, so <b>they found the same</b>. Ahmad and Kumar have 7 pictures together, "
                   "the same as Chloe."))
    its.append(q_not(T2, "Mei Ling", "How many shells did the other three children find, "
                                     "not counting Mei Ling?"))

    ICE = ("ice pop", "ice pops")
    T3 = Graph("Ice pops sold on Sports Day", ["Mango", "Orange", "Grape", "Lime"], [50, 70, 40, 30], 10, "cup",
               ICE, "", "", "", "How many {a} and {b} ice pops were sold altogether?",
               "How many ice pops were sold altogether?", "", "")
    T3.sym = "star"
    T3.ph = {"Mango": "mango", "Orange": "orange", "Grape": "grape", "Lime": "lime"}
    its.append(q_both(T3, "Mango", "Orange"))
    its.append(q_both(T3, "Grape", "Lime"))
    its.append(q_total(T3))
    its.append(q_not(T3, "Orange", "How many ice pops were sold that were not orange?"))
    assert 50 + 70 + 40 + 30 == 190
    its.append(mcq(T3.fig() + "The stall had 200 ice pops. How many ice pops were not sold?", "10 ice pops",
                   ["19 ice pops", "190 ice pops", "20 ice pops"],
                   "First find the total sold: 50 + 70 + 40 + 30 = 190. Then subtract: 200 − 190 = <b>10</b>. "
                   "(19 is the number of pictures, not ice pops.)"))

    VIS = ("visitor", "visitors")
    T4 = Graph("Visitors to our art show", ["Monday", "Tuesday", "Wednesday", "Thursday"], [40, 60, 80, 50], 10,
               "face", VIS, "", "", "", "How many visitors came on {a} and {b} altogether?",
               "How many visitors came in the four days altogether?", "", "",
               ph={d: d for d in ["Monday", "Tuesday", "Wednesday", "Thursday"]})
    its.append(q_both(T4, "Monday", "Tuesday"))
    its.append(q_both(T4, "Wednesday", "Thursday"))
    its.append(q_total(T4))
    its.append(q_not(T4, "Wednesday", "How many visitors came on the days other than Wednesday?"))
    assert 40 + 60 + 80 == 180
    its.append(mcq(T4.fig() + "How many visitors came from Monday to Wednesday?", "180 visitors",
                   ["18 visitors", "230 visitors", "140 visitors"],
                   "Monday to Wednesday is 3 days: 40 + 60 + 80 = <b>180</b>. Do not add Thursday. "
                   "(18 is the number of pictures.)"))
    assert len(its) == 20, len(its)
    return {"title": "Finding totals", "items": its}


# ============================================================ set 5: word problems
def set_words():
    its = []
    R = sgraph("Favourite recess food", ["Chicken rice", "Fried noodles", "Prata", "Nasi lemak"], [40, 25, 35, 15],
               5, "face", "chose {a}", "", "", "", total="How many students were asked altogether?")
    R.ph = {"Chicken rice": "chicken rice", "Fried noodles": "fried noodles", "Prata": "prata",
            "Nasi lemak": "nasi lemak"}
    lead = "The P2 students chose their favourite recess food. "
    assert 40 - 15 == 25
    its.append(mcq(R.fig() + lead + "How many more students chose chicken rice than nasi lemak?", "25 students",
                   ["5 students", "55 students", "20 students"],
                   "Chicken rice: 8 pictures = 40. Nasi lemak: 3 pictures = 15. 40 − 15 = <b>25</b>. "
                   "(5 is the difference in pictures, and 55 is what you get if you add.)"))
    assert 25 + 35 + 15 == 75
    its.append(mcq(R.fig() + "How many students did not choose chicken rice?", "75 students",
                   ["115 students", "40 students", "15 students"],
                   "Add the other rows: 25 + 35 + 15 = <b>75</b>. Or: 115 − 40 = 75. "
                   "(15 is the number of pictures in the other rows.)"))
    assert (35 + 10) // 5 == 9
    its.append(mcq(R.fig() + "On Friday, 10 more students chose prata. How many pictures should prata have now?",
                   "9 pictures", ["17 pictures", "8 pictures", "45 pictures"],
                   "Prata had 35. 35 + 10 = 45 students. Each picture stands for 5: 45 is 9 fives. "
                   "So prata needs <b>9 pictures</b>, 2 more than before. (7 + 10 = 17 forgets the key.)"))
    sums = {("Chicken rice", "Fried noodles"): 65, ("Chicken rice", "Prata"): 75, ("Chicken rice", "Nasi lemak"): 55,
            ("Fried noodles", "Prata"): 60, ("Fried noodles", "Nasi lemak"): 40, ("Prata", "Nasi lemak"): 50}
    for (a, b), t in sums.items():
        assert R.v(a) + R.v(b) == t
    assert list(sums.values()).count(60) == 1
    its.append(mcq(R.fig() + "Which two foods were chosen by 60 students altogether?", "Fried noodles and prata",
                   ["Chicken rice and prata", "Prata and nasi lemak", "Fried noodles and nasi lemak"],
                   "Fried noodles 25 + prata 35 = <b>60</b>. Chicken rice and prata make 75, prata and nasi lemak "
                   "make 50, and fried noodles and nasi lemak make 40."))
    its.append(mcq(R.fig() + "Ryan says, “7 students chose prata.” What mistake did he make?",
                   "He did not use the key", ["He read the wrong row", "He added 5", "He made no mistake"],
                   "Ryan counted 7 pictures. But each picture stands for 5 students: "
                   "5, 10, 15, 20, 25, 30, 35. So 35 students chose prata. He <b>did not use the key</b>."))
    assert 30 - 25 == 5
    its.append(mcq(R.fig() + "The canteen cooks 30 plates of fried noodles. Each student who chose fried noodles "
                   "gets 1 plate. How many plates are left?", "5 plates", ["25 plates", "55 plates", "10 plates"],
                   "Fried noodles has 5 pictures, so 25 students chose it. 30 − 25 = <b>5 plates</b> left. "
                   "(30 − 5 = 25 uses the pictures, not the students.)"))
    assert sum(R.vals) == 115
    its.append(mcq(R.fig() + "How many students were asked altogether?", "115 students",
                   ["23 students", "100 students", "120 students"],
                   "Add all the rows: 40 + 25 + 35 + 15 = <b>115</b>. "
                   "(23 is the number of pictures, and 100 leaves out nasi lemak.)"))

    B = pgraph("Books read in June", ["Ali", "Mei Ling", "Raju", "Chloe"], [12, 18, 8, 14], 2, "book", BK, "read",
               "", "", "")
    lead = "Four friends read books in the June holidays. "
    assert 8 + 4 == 12
    its.append(mcq(B.fig() + lead + "Who read 4 more books than Raju?", "Ali", ["Mei Ling", "Chloe", "Raju"],
                   "Raju read 8 books. 8 + 4 = 12. Ali has 6 pictures: 2, 4, 6, 8, 10, 12. So <b>Ali</b> read 12. "
                   "4 more books is only 2 more pictures."))
    assert 18 - 8 == 10
    its.append(mcq(B.fig() + "Raju wants to read as many books as Mei Ling. How many more books must he read?",
                   "10 books", ["5 books", "26 books", "8 books"],
                   "Mei Ling read 18. Raju read 8. 18 − 8 = <b>10 books</b>. "
                   "(5 is the difference in pictures.)"))
    assert 12 + 14 == 26
    its.append(mcq(B.fig() + "How many books did Ali and Chloe read altogether?", "26 books",
                   ["13 books", "2 books", "28 books"],
                   "Ali: 12. Chloe: 14. 12 + 14 = <b>26 books</b>. (13 is the number of pictures.)"))
    assert (18 - 6) // 2 == 6
    its.append(mcq(B.fig() + "In July, Mei Ling read 6 fewer books than in June. How many pictures are needed "
                   "for her July row?", "6 pictures", ["12 pictures", "3 pictures", "9 pictures"],
                   "June: 18 books. 18 − 6 = 12 books in July. Each picture stands for 2, so 12 needs "
                   "<b>6 pictures</b>. (9 − 6 = 3 takes 6 pictures away instead of 6 books.)"))
    assert 14 - 8 == 6
    its.append(mcq(B.fig() + "How many fewer books did Raju read than Chloe?", "6 books",
                   ["3 books", "22 books", "4 books"],
                   "Chloe: 14. Raju: 8. 14 − 8 = <b>6 books</b>. Raju has 3 fewer pictures, and 3 × 2 = 6."))
    assert 60 - 52 == 8 and 12 + 18 + 8 + 14 == 52
    its.append(mcq(B.fig() + "The four friends want to read 60 books altogether. How many more books must they read?",
                   "8 books", ["52 books", "34 books", "18 books"],
                   "Total so far: 12 + 18 + 8 + 14 = 52. 60 − 52 = <b>8 books</b>. "
                   "(60 − 26 pictures = 34 forgets the key.)"))
    its.append(mcq(B.fig() + "Hafiz read 16 books in June. How many pictures should be drawn for him?",
                   "8 pictures", ["16 pictures", "32 pictures", "7 pictures"],
                   "Each picture stands for 2 books. Count in 2s: 2, 4, 6, 8, 10, 12, 14, 16. That is "
                   "<b>8 pictures</b>. (32 is 16 × 2: do not multiply.)"))

    # bar model problems (the graph is described in words)
    assert 6 * 5 == 30 and 30 + 10 == 40
    its.append(mcq(bar_fig([("Siti", [(30, False)], [(0, 0, "30")]),
                            ("Ahmad", [(30, False), (10, False)], [(1, 1, "10")], "?")], None,
                           "bar model: Ahmad has 10 more than Siti") +
                   "In a picture graph, each picture stands for 5 stickers. Siti has 6 pictures. "
                   "Ahmad has 10 more stickers than Siti. How many stickers does Ahmad have?",
                   "40 stickers", ["16 stickers", "20 stickers", "35 stickers"],
                   "Siti: 6 pictures × 5 = 30 stickers. Ahmad has 10 more: 30 + 10 = <b>40 stickers</b>. "
                   "(6 + 10 = 16 forgets the key.)"))
    assert 4 * 10 + 7 * 10 == 110
    its.append(mcq(bar_fig([("Kumar", [(40, False)], [(0, 0, "40")]), ("Devi", [(70, False)], [(0, 0, "70")])], "?",
                           "bar model: Kumar 40 and Devi 70 altogether") +
                   "Each picture stands for 10 marbles. Kumar has 4 pictures and Devi has 7 pictures. "
                   "How many marbles do they have altogether?", "110 marbles",
                   ["11 marbles", "30 marbles", "100 marbles"],
                   "Kumar: 4 tens = 40. Devi: 7 tens = 70. 40 + 70 = <b>110 marbles</b>. "
                   "Or: 11 pictures × 10 = 110. (11 counts pictures; 30 subtracts.)"))
    assert 8 * 2 - 5 * 2 == 6
    its.append(mcq(bar_fig([("Prata", [(10, False), (6, True)], [(0, 0, "10"), (1, 1, "?")]),
                            ("Laksa", [(10, False)], [(0, 0, "10")])], None,
                           "bar model: prata 16 and laksa 10") +
                   "Xin Yi made a picture graph. Each picture stands for 2 students. Prata has 8 pictures and "
                   "laksa has 5 pictures. How many more students chose prata than laksa?",
                   "6 students", ["3 students", "26 students", "13 students"],
                   "Prata: 8 × 2 = 16. Laksa: 5 × 2 = 10. The model shows 16 − 10 = <b>6 students</b>. "
                   "(3 is the difference in pictures.)"))
    assert 15 * 2 == 30 and 40 - 30 == 10
    its.append(mcq(bar_fig([("Class", [(30, False), (10, True)], [(0, 0, "30 walk"), (1, 1, "? bus")])], "40",
                           "bar model: 40 students, 30 walk and the rest take the bus") +
                   "Mr Tan’s class has 40 students. In a picture graph, each picture stands for 2 students. "
                   "There are 15 pictures for “Walk”. The rest take the bus. How many students take the bus?",
                   "10 students", ["25 students", "30 students", "70 students"],
                   "Walk: 15 × 2 = 30 students. Bus: 40 − 30 = <b>10 students</b>. "
                   "(40 − 15 = 25 uses the pictures, not the students.)"))
    assert 9 * 5 == 45
    its.append(mcq("The canteen sold 45 cups of Milo. In a picture graph, each picture stands for 5 cups. "
                   "How many pictures are drawn for Milo?", "9 pictures",
                   ["45 pictures", "8 pictures", "50 pictures"],
                   "Count in 5s until you reach 45: 5, 10, 15, 20, 25, 30, 35, 40, 45. That is "
                   "<b>9 pictures</b>."))
    its.append(mcq("Priya drew a picture graph of 30 students. Each picture stands for 10 students. "
                   "How many pictures did she draw?", "3 pictures",
                   ["30 pictures", "10 pictures", "4 pictures"],
                   "Count in 10s: 10, 20, 30. That is <b>3 pictures</b>. 30 pictures would show 300 students."))
    assert len(its) == 20, len(its)
    return {"title": "Picture graph word problems", "items": its}


def bar_fig(rows, total, label):
    return fig(bar_svg(rows, total, label))


# ============================================================ lesson
def body_html():
    L1 = sgraph("Our favourite fruit", ["Durian", "Mango", "Rambutan"], [3, 5, 4], 1, "face",
                "chose {a}", "", "", "")
    L2 = sgraph("Favourite recess food", ["Chicken rice", "Prata", "Nasi lemak"], [30, 20, 15], 5, "face",
                "chose {a}", "", "", "")
    model = bar_svg([("Chicken rice", [(20, False), (10, True)], [(0, 0, "20"), (1, 1, "?")]),
                     ("Prata", [(20, False)], [(0, 0, "20")])], None, "bar model: chicken rice 30 and prata 20")
    return (
        "<h2>What is a picture graph?</h2>"
        "<p>A picture graph uses pictures to show data. Each row is one group. "
        "The <b>key</b> tells you what one picture stands for. Always read the key first.</p>"
        "<figure class='sn-fig'>" + pic_svg(L1) +
        "<figcaption>Each picture stands for 1 student. Durian 3, mango 5, rambutan 4. "
        "Mango is the most popular.</figcaption></figure>"
        "<h2>Picture graphs with a scale</h2>"
        "<p>A picture can stand for more than 1, like 2, 5 or 10. "
        "Then count in 2s, 5s or 10s along the row.</p>"
        "<figure class='sn-fig'>" + pic_svg(L2) +
        "<figcaption>Each picture stands for 5 students. Chicken rice has 6 pictures: "
        "5, 10, 15, 20, 25, 30. So 30 students chose chicken rice.</figcaption></figure>"
        + table(["Key: each picture stands for", "4 pictures show", "Count"], [
            ["1", "4", "1, 2, 3, 4"],
            ["2", "8", "2, 4, 6, 8"],
            ["5", "20", "5, 10, 15, 20"],
            ["10", "40", "10, 20, 30, 40"],
        ])
        + ex("Read a row", "In the recess food graph, how many students chose prata?",
             "Prata has 4 pictures. Each picture stands for 5. Count in 5s: 5, 10, 15, 20.", "20 students")
        + "<h2>Most, fewest, how many more, altogether</h2>"
        "<p>The longest row is the <b>most</b>. The shortest row is the <b>fewest</b>. "
        "For <b>how many more</b>, subtract. For <b>altogether</b>, add.</p>"
        "<figure class='sn-fig'>" + model +
        "<figcaption>Chicken rice 30, prata 20. 30 − 20 = 10. "
        "So 10 more students chose chicken rice.</figcaption></figure>"
        + ex("Altogether", "How many students chose chicken rice or nasi lemak?",
             "Chicken rice: 30. Nasi lemak: 3 pictures = 15. Add: 30 + 15 = 45.", "45 students")
        + "<h2>Common mistakes</h2>"
        + table(["Mistake", "What to do instead"], [
            ["Counting the pictures: prata has 4 pictures, so 4 students",
             "Use the key: 4 pictures × 5 = 20 students"],
            ["Not reading the key at all", "Read the key first: each picture may stand for 2, 5 or 10"],
            ["Giving the difference in pictures: 2 more pictures, so 2 more",
             "2 more pictures × 5 = 10 more students"],
            ["Adding when the question asks “how many more”", "How many more means subtract"],
            ["Leaving out a row in a total", "Add every row, then check you used them all"],
        ])
    )


FAQ = [
    {"q": "What is taught in P2 picture graphs?",
     "a": "Primary 2 students read picture graphs where one picture stands for 1, 2, 5 or 10. They find the most "
          "and the fewest, how many more and how many altogether, and solve simple word problems."},
    {"q": "How do I explain a picture graph with a scale to my child?",
     "a": "Point to the key first and say what one picture stands for, for example 5 students. "
          "Then count along the row in 5s: 5, 10, 15, 20."},
    {"q": "What is the most common mistake in picture graphs?",
     "a": "Counting the pictures and forgetting the key. If each picture stands for 5 and a row has "
          "4 pictures, the answer is 20, not 4."},
    {"q": "Are picture graphs in the MOE syllabus for Primary 2?",
     "a": "Yes. Picture graphs with scales are in the Statistics strand of the MOE 2021 Primary 2 "
          "Mathematics syllabus. Bar graphs come later, in Primary 3."},
]


def mark_large(u, pattern):
    """Tag wide pictures so they print larger and the pictures stay easy to count."""
    rx = re.compile(r"<svg (?=[^>]*aria-label='" + pattern + ")")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u


def gen():
    rnd = random.Random(62813)
    sets = [set_one(), set_scales(), set_compare(), set_totals(), set_words()]
    balance(sets, rnd)
    seen = set()
    for s in sets:
        assert len(s["items"]) == 20, (s["title"], len(s["items"]))
        assert sorted(it["a"] for it in s["items"]) == sorted([0, 1, 2, 3] * 5), s["title"]
        for it in s["items"]:
            assert len(set(it["c"])) == 4, it
            assert it["e"]
            assert it["q"].count("<svg") <= 1
            k = it["q"] + "|" + "|".join(sorted(it["c"]))
            assert k not in seen, it["q"]
            seen.add(k)
            assert "\\" not in it["q"] + it["e"] + "".join(it["c"])
    u = {
        "country": "sg", "subject": "maths", "grade": "primary-2", "slug": "picture-graphs", "sort": 13,
        "updated": UPDATED, "pdf_url": "",
        "title": "Primary 2 Picture Graphs",
        "seo_title": "P2 Picture Graphs Worksheets: Free Primary 2 Maths with Answers (MOE Syllabus)",
        "short_title": "Picture graphs",
        "domain": "Statistics",
        "standard_code": "Primary 2: Statistics",
        "standard_url": "https://www.moe.gov.sg/primary/curriculum/syllabus",
        "standard_text": "Reading and interpreting data from picture graphs with scales",
        "meta_desc": "Free P2 maths practice on picture graphs with scales of 1, 2, 5 and 10: reading the key, "
                     "most and fewest, how many more, totals. 100 questions with answers.",
        "key_big": "Read the key first, then count in its steps.",
        "key_sub": "If each picture stands for 5, a row of 4 pictures shows 5, 10, 15, 20: that is 20, not 4.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }
    assert len(u["meta_desc"]) <= 160, len(u["meta_desc"])
    return mark_large(u, "(picture graph|bar model)")


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
