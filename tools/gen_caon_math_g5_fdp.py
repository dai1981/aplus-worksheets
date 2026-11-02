# -*- coding: utf-8 -*-
"""
Canada (Ontario) Grade 5 Math: Fractions, decimals and percents
(Ontario Curriculum, Grades 1-8: Mathematics, 2020 — Grade 5, B1.7)
  python3 tools/gen_caon_math_g5_fdp.py
Sets: hundred grids as a fraction, a decimal and a percent; fractions with denominators 2, 4, 5, 10, 20, 25 and 50
as decimals (and back); decimals and fractions as percents; comparing and ordering mixed forms;
word problems (test scores, 25% off, sharing money).
Wrong answers come from real mistakes: 0.4 = 4%, 1/4 = 0.4 (denominator read as tenths), 3/5 = 0.35 (digits written
side by side), 0.9 = 9%, 8% = 0.8, the unshaded part, the discount instead of the sale price, 7/20 = 0.27 (adding).
Every answer is checked with fractions.Fraction / decimal.Decimal (never float).
Decimals stay at hundredths; whole numbers to 100 000 (no-break space). Canadian English, dollars and cents (¢).
HTML attributes use single quotes (no backslashes in the JSON).
"""
import json, os, random, re
from decimal import Decimal as Dm
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "ca-on", "math", "grade-5")
UPDATED = "2026-11-02"
FILL = "#4fae74"
LINE = "#2b2b2b"
THIN = "#8a8a8a"
RED = "#d6453b"
FONT = "Arial, Helvetica, sans-serif"
GIRLS = ["Olivia", "Emma", "Maya", "Zoe", "Amira", "Mei", "Chloe", "Priya", "Leah", "Hana", "Ava", "Sofia"]
BOYS = ["Liam", "Noah", "Aiden", "Lucas", "Owen", "Arjun", "Ethan", "Jayden", "Benjamin", "Mateo", "Nathan", "Kai"]


# ------------------------------------------------------------ helpers
def fr(a, b):
    return "<span class='fr'><span class='fn'>%s</span><span class='fd'>%s</span></span>" % (a, b)


def mixed(w, a, b):
    return "%d %s" % (w, fr(a, b))


FRX = re.compile(r"^(?:(\d+) )?<span class='fr'><span class='fn'>(\d+)</span><span class='fd'>(\d+)</span></span>( .+)?$")
NUM = re.compile(r"^(\$)?(\d*\.?\d+)(¢|%)?( .+)?$")


def val(c):
    """Value of a choice (Fraction) with its unit; 20% is 1/5 with unit '' so 20% and 0.2 count as equal.
    None for choices that are not a single number."""
    m = FRX.match(c)
    if m:
        return (int(m.group(1) or 0) + F(int(m.group(2)), int(m.group(3))), (m.group(4) or "").strip())
    m = NUM.match(c)
    if not m:
        return None
    v = F(m.group(2))
    if m.group(1):
        return (v, "$")
    if m.group(3) == "¢":
        return (v / 100, "$")
    if m.group(3) == "%":
        v = v / 100
    return (v, (m.group(4) or "").strip())


def mcq(q, correct, wrong, e, same_ok=False, value=None):
    """4 choices: correct first + 3 wrong. Positions are set by balance(). No two choices may have the same value
    (same_ok=True only where a 'NOT equal' or 'compare' choice is meant). value: the exact answer to check."""
    correct = str(correct)
    wrong = [str(x) for x in wrong]
    assert len(wrong) == 3, (q, wrong)
    ch = [correct] + wrong
    assert len(set(re.sub(r"<[^>]+>", "", x) for x in ch)) == 4, (q, ch)
    if value is not None:
        assert val(correct)[0] == F(value), (q, correct, value)
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


def table(head, rows):
    h = "".join("<th>%s</th>" % x for x in head)
    b = "".join("<tr>" + "".join("<td>%s</td>" % c for c in r) + "</tr>" for r in rows)
    return "<div class='sn-tw'><table class='sn-table'><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>" % (h, b)


def ex(title, q, s, a):
    return ("<div class='sn-ex'><span class='sn-ex-t'>%s</span><p class='sn-ex-q'>%s</p>"
            "<p class='sn-ex-s'>%s</p><p class='sn-ex-a'>Answer: %s</p></div>" % (title, q, s, a))


def D(s):
    return F(Dm(s))


def pct(s):
    """'35%' -> Fraction 35/100."""
    return F(s.rstrip("%")) / 100


# ------------------------------------------------------------ pictures
def grid_body(k, x0, pad=4, cell=18):
    """10 x 10 hundred grid at x0 with k squares shaded: full columns first, then from the top of the next column."""
    s = []
    for c in range(10):
        for r in range(10):
            if c * 10 + r < k:
                s.append("<rect x='%d' y='%d' width='%d' height='%d' fill='%s'/>"
                         % (x0 + c * cell, pad + r * cell, cell, cell, FILL))
    for i in range(1, 10):
        s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='1.2'/>"
                 % (x0 + i * cell, pad, x0 + i * cell, pad + 10 * cell, THIN))
        s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='1.2'/>"
                 % (x0, pad + i * cell, x0 + 10 * cell, pad + i * cell, THIN))
    s.append("<rect x='%d' y='%d' width='%d' height='%d' fill='none' stroke='%s' stroke-width='2.5'/>"
             % (x0, pad, 10 * cell, 10 * cell, LINE))
    return "".join(s)


def grid_svg(k, cell=18):
    pad = 4
    w = 10 * cell + 2 * pad
    return svg_wrap(w, w, grid_body(k, pad, pad, cell), "hundred grid with %d of 100 squares shaded" % k)


def grids2_svg(k1, k2, cell=16):
    """Two hundred grids side by side (k1 and k2 squares shaded)."""
    pad, gap = 4, 18
    s = grid_body(k1, pad, pad, cell) + grid_body(k2, pad + 10 * cell + gap, pad, cell)
    w = 20 * cell + gap + 2 * pad
    return svg_wrap(w, 10 * cell + 2 * pad, s,
                    "2 hundred grids side by side, %d and %d squares shaded" % (k1, k2))


def line_svg(parts, dot, labels, W=400):
    """Number line from 0 to 1 with `parts` equal spaces, red dot at tick `dot`. labels: {tick: text}."""
    L, R, Y = 26, W - 26, 30

    def X(i):
        return L + (R - L) * i / float(parts)
    s = ["<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='2.5'/>" % (L, Y, R, Y, LINE)]
    for i in range(parts + 1):
        big = i in labels
        s.append("<line x1='%.1f' y1='%d' x2='%.1f' y2='%d' stroke='%s' stroke-width='%s'/>"
                 % (X(i), Y - (13 if big else 9), X(i), Y + (13 if big else 9), LINE, "2.5" if big else "1.8"))
    for i, t in labels.items():
        s.append(text(X(i), Y + 36, t, 17))
    s.append("<circle cx='%.1f' cy='%d' r='8' fill='%s'/>" % (X(dot), Y, RED))
    return svg_wrap(W, Y + 46, "".join(s), "number line from 0 to 1 split into %d equal parts" % parts)


# ============================================================ set 1: hundred grids
def set_grids():
    its = []

    def g(k, q, right, wrong, e, value=None, same_ok=False):
        its.append(mcq(fig(grid_svg(k)) + q, right, wrong, e, value=value, same_ok=same_ok))

    g(30, "What fraction of the hundred grid is shaded?", fr(30, 100), [fr(3, 100), fr(70, 100), fr(30, 10)],
      "30 of the 100 squares are shaded, so it is <b>%s</b>. %s is the white part." % (fr(30, 100), fr(70, 100)),
      value=F(30, 100))
    g(60, "What decimal of the hundred grid is shaded?", "0.6", ["0.06", "6", "0.4"],
      "60 of 100 squares = 60 hundredths = 6 tenths = <b>0.6</b>. Each full column is one tenth. "
      "0.06 would be only 6 squares, and 0.4 is the white part.", value=F(6, 10))
    g(45, "What percent of the hundred grid is shaded?", "45%", ["4.5%", "55%", "0.45%"],
      "Percent means <b>out of 100</b>. 45 of 100 squares are shaded, so it is <b>45%</b>. 55% is the white part.",
      value=F(45, 100))
    g(6, "What decimal of the hundred grid is shaded?", "0.06", ["0.6", "6", "0.94"],
      "6 of 100 squares = 6 hundredths. Write a 0 in the tenths place: <b>0.06</b>. 0.6 would be 6 full columns.",
      value=F(6, 100))
    g(9, "What percent of the hundred grid is shaded?", "9%", ["90%", "0.9%", "91%"],
      "9 of 100 squares are shaded: <b>9%</b>. 90% would be 9 full columns, and 91% is the white part.", value=F(9, 100))
    g(100, "The whole hundred grid is shaded. What decimal is that?", "1", ["100", "0.1", "0.01"],
      "100 out of 100 is the whole grid: %s = <b>1</b> = 100%%. 0.1 is only one column." % fr(100, 100), value=1)
    g(72, "Which shows the shaded part as a decimal and a percent?", "0.72 and 72%",
      ["7.2 and 72%", "0.72 and 7.2%", "0.28 and 28%"],
      "72 of 100 squares: %s = <b>0.72</b> = <b>72%%</b>. 0.28 and 28%% describe the white part." % fr(72, 100))
    g(40, "Which does <b>not</b> describe the shaded part?", "4%", ["0.4", "40%", fr(2, 5)],
      "40 of 100 squares: %s = 0.4 = 40%% = %s. <b>4%%</b> would be only 4 squares." % (fr(40, 100), fr(2, 5)),
      same_ok=True)
    g(50, "What fraction of the hundred grid is shaded, in simplest form?", fr(1, 2), [fr(1, 50), fr(1, 5), fr(5, 1)],
      "50 of 100 squares = %s. Divide the top and bottom by 50: <b>%s</b>. Half the grid is shaded." % (fr(50, 100), fr(1, 2)),
      value=F(1, 2))
    g(25, "What fraction of the hundred grid is shaded, in simplest form?", fr(1, 4), [fr(1, 25), fr(2, 5), fr(3, 4)],
      "25 of 100 squares = %s. 4 groups of 25 make 100, so it is <b>%s</b>. %s is the white part."
      % (fr(25, 100), fr(1, 4), fr(3, 4)), value=F(1, 4))
    g(20, "What fraction of the hundred grid is shaded, in simplest form?", fr(1, 5), [fr(1, 20), fr(4, 5), fr(2, 100)],
      "20 of 100 squares = %s = %s = <b>%s</b>. %s would be only 2 squares." % (fr(20, 100), fr(2, 10), fr(1, 5), fr(2, 100)),
      value=F(1, 5))
    g(75, "What percent of the hundred grid is <b>not</b> shaded?", "25%", ["75%", "2.5%", "0.25%"],
      "75 squares are shaded, so 100 − 75 = 25 are white: <b>25%</b>. 75% is the shaded part.", value=F(25, 100))
    g(35, "What fraction of the grid is shaded, in simplest form?", fr(7, 20), [fr(3, 5), fr(7, 10), fr(13, 20)],
      "35 of 100 squares = %s. Divide the top and bottom by 5: <b>%s</b>. %s just uses the digits 3 and 5, "
      "and %s is the white part." % (fr(35, 100), fr(7, 20), fr(3, 5), fr(13, 20)), value=F(7, 20))
    g(64, "Which shows the shaded part three ways?", "%s, 0.64, 64%%" % fr(64, 100),
      ["%s, 6.4, 64%%" % fr(64, 100), "%s, 0.64, 6.4%%" % fr(64, 100), "%s, 0.36, 36%%" % fr(36, 100)],
      "64 of 100 squares: <b>%s = 0.64 = 64%%</b>. The 36 white squares give %s, 0.36 and 36%%." % (fr(64, 100), fr(36, 100)))
    g(5, "What fraction of the hundred grid is shaded, in simplest form?", fr(1, 20), [fr(1, 5), fr(5, 10), fr(19, 20)],
      "5 of 100 squares = %s. Divide the top and bottom by 5: <b>%s</b>. %s is 20 squares, not 5." % (fr(5, 100), fr(1, 20), fr(1, 5)),
      value=F(1, 20))

    def shade(q, right, wrong, e, v):
        assert F(int(right), 100) == v
        its.append(mcq(q, right, wrong, e))

    shade("How many squares of a hundred grid would you shade to show <b>0.6</b>?", "60", ["6", "40", "16"],
          "0.6 = 6 tenths = 60 hundredths, so shade <b>60</b> squares (6 full columns). 6 squares would be 0.06.", D("0.6"))
    shade("How many squares of a hundred grid would you shade to show <b>8%</b>?", "8", ["80", "92", "18"],
          "8% means 8 out of 100, so shade <b>8</b> squares. 80 squares would be 80%.", pct("8%"))
    shade("How many squares of a hundred grid would you shade to show %s?" % fr(2, 5), "40", ["25", "20", "60"],
          "%s = %s, so shade <b>40</b> squares. 25 just uses the digits 2 and 5, and 60 is the part left white."
          % (fr(2, 5), fr(40, 100)), F(2, 5))
    shade("How many squares of a hundred grid would you shade to show %s?" % fr(3, 4), "75", ["34", "25", "30"],
          "%s = %s (multiply the top and bottom by 25), so shade <b>75</b> squares. 34 just writes the digits."
          % (fr(3, 4), fr(75, 100)), F(3, 4))
    its.append(mcq(fig(grids2_svg(100, 25)) + "Each grid is one whole. What decimal is shaded in all?", "1.25",
                   ["0.125", "12.5", "0.25"],
                   "The first grid is 1 whole. The second has 25 hundredths. 1 + 0.25 = <b>1.25</b>. "
                   "0.25 forgets the full grid.", value=F(5, 4)))
    order = [0, 1, 2, 3, 15, 4, 16, 5, 6, 7, 8, 9, 17, 10, 18, 11, 12, 13, 14, 19]
    its = [its[i] for i in order]
    assert len(its) == 20 and len(set(order)) == 20
    return {"title": "Hundred grids: fraction, decimal and percent", "items": its}


# ============================================================ set 2: fractions as decimals
def set_fraction_decimal():
    its = []

    def f2d(n, d, right, wrong, e, q=None, fg=""):
        assert D(right) == F(n, d), (n, d, right)
        its.append(mcq(fg + (q or "Write %s as a decimal." % fr(n, d)), right, wrong, e))

    f2d(3, 10, "0.3", ["0.03", "3.1", "0.13"],
        "3 tenths: the 3 goes in the tenths place, the first place after the decimal point. %s = <b>0.3</b>." % fr(3, 10))
    f2d(47, 100, "0.47", ["4.7", "47", "0.53"],
        "47 hundredths: the 7 goes in the hundredths place, the second place after the point. %s = <b>0.47</b>." % fr(47, 100))
    f2d(8, 100, "0.08", ["0.8", "8", "0.92"],
        "8 hundredths: write a 0 in the tenths place to hold it. %s = <b>0.08</b>. 0.8 would be 8 tenths." % fr(8, 100))
    f2d(1, 2, "0.5", ["0.12", "1.2", "0.2"],
        "Multiply the top and bottom by 5: %s = %s = <b>0.5</b>. 0.12 and 1.2 just write the digits of the fraction."
        % (fr(1, 2), fr(5, 10)))
    f2d(1, 4, "0.25", ["0.4", "0.14", "1.4"],
        "4 × 25 = 100, so multiply the top by 25 too: %s = %s = <b>0.25</b>. "
        "0.4 is a common mistake: it reads the denominator 4 as tenths." % (fr(1, 4), fr(25, 100)))
    f2d(3, 4, "0.75", ["0.34", "0.4", "0.25"],
        "The line from 0 to 1 has 4 equal parts, so each part is %s. The dot is 3 parts along: %s = %s = <b>0.75</b>. "
        "0.25 is only one part." % (fr(1, 4), fr(3, 4), fr(75, 100)),
        q="The line from 0 to 1 is split into 4 equal parts. What decimal is at the red dot?",
        fg=fig(line_svg(4, 3, {0: "0", 4: "1"})))
    f2d(2, 5, "0.4", ["0.25", "2.5", "0.2"],
        "5 × 2 = 10, so %s = %s = <b>0.4</b>. 0.25 just writes the digits, and 2.5 is 5 ÷ 2, the wrong way round."
        % (fr(2, 5), fr(4, 10)))
    f2d(4, 5, "0.8", ["0.45", "0.2", "4.5"],
        "%s = %s = <b>0.8</b>. 0.2 is the part that is left, %s." % (fr(4, 5), fr(8, 10), fr(1, 5)))
    f2d(1, 5, "0.2", ["0.15", "0.5", "1.5"],
        "%s = %s = <b>0.2</b>. 0.5 reads the denominator 5 as tenths, the same mistake as %s = 0.4." % (fr(1, 5), fr(2, 10), fr(1, 4)))
    f2d(7, 20, "0.35", ["0.7", "0.27", "0.72"],
        "20 × 5 = 100, so multiply the top by 5 too: %s = %s = <b>0.35</b>. 0.7 would be %s, and 0.27 adds 7 + 20."
        % (fr(7, 20), fr(35, 100), fr(7, 10)))
    f2d(9, 20, "0.45", ["0.9", "0.29", "0.92"],
        "20 × 5 = 100, so %s = %s = <b>0.45</b>. 0.9 would be %s." % (fr(9, 20), fr(45, 100), fr(9, 10)))
    f2d(6, 25, "0.24", ["0.6", "0.31", "0.19"],
        "25 × 4 = 100, so multiply the top by 4 too: %s = %s = <b>0.24</b>. 0.6 forgets to multiply, and 0.31 adds 6 + 25."
        % (fr(6, 25), fr(24, 100)))
    f2d(13, 25, "0.52", ["0.13", "0.38", "0.12"],
        "25 × 4 = 100, so %s = %s = <b>0.52</b>. 0.13 forgets to multiply the top by 4." % (fr(13, 25), fr(52, 100)))
    f2d(3, 50, "0.06", ["0.03", "0.6", "0.53"],
        "50 × 2 = 100, so multiply the top by 2 too: %s = %s = <b>0.06</b>. 0.6 would be %s." % (fr(3, 50), fr(6, 100), fr(6, 10)))
    f2d(27, 50, "0.54", ["0.27", "0.77", "5.4"],
        "50 × 2 = 100, so %s = %s = <b>0.54</b>. 0.27 forgets to multiply the top by 2, and 0.77 adds 27 + 50."
        % (fr(27, 50), fr(54, 100)))
    f2d(11, 4, "2.75", ["2.3", "11.4", "2.34"],
        "The 2 wholes stay as 2. %s = 0.75, so %s = <b>2.75</b>. 2.3 writes the 3 quarters as 3 tenths."
        % (fr(3, 4), mixed(2, 3, 4)), q="Write %s as a decimal." % mixed(2, 3, 4))

    def d2f(s, right, wrong, e, v):
        assert D(s) == v
        its.append(mcq("Write <b>%s</b> as a fraction in simplest form." % s, right, wrong, e, value=v))

    d2f("0.5", fr(1, 2), [fr(1, 5), fr(5, 100), fr(1, 50)],
        "0.5 = 5 tenths = %s. Divide the top and bottom by 5: <b>%s</b>. %s would be 0.2." % (fr(5, 10), fr(1, 2), fr(1, 5)), F(1, 2))
    d2f("0.4", fr(2, 5), [fr(1, 4), fr(4, 100), fr(3, 5)],
        "0.4 = %s. Divide the top and bottom by 2: <b>%s</b>. %s is 0.25, not 0.4." % (fr(4, 10), fr(2, 5), fr(1, 4)), F(2, 5))
    d2f("0.75", fr(3, 4), [fr(75, 10), fr(7, 5), fr(1, 4)],
        "0.75 = 75 hundredths = %s. Divide the top and bottom by 25: <b>%s</b>. %s would be 7.5." % (fr(75, 100), fr(3, 4), fr(75, 10)),
        F(3, 4))
    d2f("0.04", fr(1, 25), [fr(4, 10), fr(1, 4), fr(25, 1)],
        "0.04 = 4 hundredths = %s. Divide the top and bottom by 4: <b>%s</b>. %s would be 0.4, and %s is 25 wholes." % (fr(4, 100), fr(1, 25), fr(4, 10), fr(25, 1)),
        F(1, 25))
    order = [0, 1, 2, 3, 4, 16, 5, 6, 7, 17, 8, 18, 9, 10, 11, 12, 13, 14, 19, 15]
    its = [its[i] for i in order]
    assert len(its) == 20 and len(set(order)) == 20
    return {"title": "Fractions as decimals: halves to fiftieths", "items": its}


# ============================================================ set 3: decimals and percents
def set_percent():
    its = []
    for d_, right, wrong, e in [
        ("0.4", "40%", ["4%", "0.4%", "400%"],
         "0.4 = 4 tenths = 40 hundredths = <b>40%</b>. 4% is a common mistake: 4% would be 0.04."),
        ("0.07", "7%", ["70%", "0.07%", "0.7%"],
         "0.07 = 7 hundredths = <b>7%</b>. 70% would be 0.7."),
        ("0.25", "25%", ["2.5%", "0.25%", "250%"],
         "0.25 = 25 hundredths = <b>25%</b>. Multiply by 100: 0.25 × 100 = 25."),
        ("0.9", "90%", ["9%", "0.9%", "10%"],
         "0.9 = 0.90 = 90 hundredths = <b>90%</b>. 9% would be 0.09."),
        ("0.6", "60%", ["6%", "0.6%", "40%"],
         "0.6 = 0.60 = 60 hundredths = <b>60%</b>. 40% is the part that is left."),
        ("0.15", "15%", ["1.5%", "150%", "0.15%"],
         "0.15 = 15 hundredths = <b>15%</b>. 150% would be 1.5."),
        ("0.83", "83%", ["8.3%", "0.83%", "17%"],
         "0.83 = 83 hundredths = <b>83%</b>. 17% is the part that is left."),
        ("1", "100%", ["1%", "10%", "0%"],
         "1 is one whole, 100 out of 100: <b>100%</b>. 1% would be 0.01."),
    ]:
        assert D(d_) == pct(right)
        its.append(mcq("Write <b>%s</b> as a percent." % d_, right, wrong, e))
    for p_, right, wrong, e in [
        ("35%", "0.35", ["3.5", "0.035", "35"],
         "35% = 35 hundredths = <b>0.35</b>. Divide by 100."),
        ("6%", "0.06", ["0.6", "6", "0.006"],
         "6% = 6 hundredths. Hundredths are the second place after the point: <b>0.06</b>. 0.6 is 60%."),
        ("70%", "0.7", ["0.07", "7", "70"],
         "70% = 70 hundredths = 7 tenths = <b>0.7</b>. 0.07 is only 7%."),
        ("50%", "0.5", ["0.05", "5", "50"],
         "50% = 50 hundredths = 5 tenths = <b>0.5</b>. 0.05 is only 5%."),
    ]:
        assert pct(p_) == D(right)
        its.append(mcq("Write <b>%s</b> as a decimal." % p_, right, wrong, e))
    for (n, d), right, wrong, e in [
        ((1, 2), "50%", ["12%", "2%", "20%"],
         "%s = %s = <b>50%%</b>. 12%% just writes the digits of the fraction." % (fr(1, 2), fr(50, 100))),
        ((1, 4), "25%", ["40%", "14%", "4%"],
         "%s = %s = <b>25%%</b>. 40%% reads the denominator 4 as tenths." % (fr(1, 4), fr(25, 100))),
        ((3, 4), "75%", ["34%", "25%", "3%"],
         "%s = %s = <b>75%%</b>. 34%% just writes the digits, and 25%% is only %s." % (fr(3, 4), fr(75, 100), fr(1, 4))),
        ((4, 5), "80%", ["45%", "20%", "8%"],
         "5 × 20 = 100, so %s = %s = <b>80%%</b>. 45%% just writes the digits 4 and 5." % (fr(4, 5), fr(80, 100))),
        ((3, 10), "30%", ["3%", "13%", "70%"],
         "%s = %s = <b>30%%</b>. 3%% would be %s." % (fr(3, 10), fr(30, 100), fr(3, 100))),
        ((7, 20), "35%", ["7%", "27%", "72%"],
         "20 × 5 = 100, so %s = %s = <b>35%%</b>. 27%% adds 7 + 20." % (fr(7, 20), fr(35, 100))),
        ((9, 25), "36%", ["9%", "34%", "16%"],
         "25 × 4 = 100, so %s = %s = <b>36%%</b>. 34%% adds 9 + 25, and 16%% is 25 − 9." % (fr(9, 25), fr(36, 100))),
        ((1, 50), "2%", ["50%", "20%", "1%"],
         "50 × 2 = 100, so %s = %s = <b>2%%</b>. 50%% uses the denominator, and 20%% would be %s."
         % (fr(1, 50), fr(2, 100), fr(1, 5))),
    ]:
        assert pct(right) == F(n, d)
        its.append(mcq("Write %s as a percent." % fr(n, d), right, wrong, e))
    order = [0, 1, 2, 8, 9, 12, 13, 3, 4, 10, 11, 14, 5, 6, 15, 16, 7, 17, 18, 19]
    its = [its[i] for i in order]
    assert len(its) == 20 and len(set(order)) == 20
    return {"title": "Decimals and fractions as percents", "items": its}


# ============================================================ set 4: compare and order
def cmp_item(x, xv, y, yv, e):
    lt, gt, eq = "%s &lt; %s" % (x, y), "%s &gt; %s" % (x, y), "%s = %s" % (x, y)
    right = lt if xv < yv else gt if xv > yv else eq
    wrong = [c for c in (lt, gt, eq) if c != right] + ["You can’t tell"]
    return mcq("Compare <b>%s</b> and <b>%s</b>." % (x, y), right, wrong, e, same_ok=True)


def set_compare():
    its = []
    its.append(cmp_item("0.4", D("0.4"), "4%", pct("4%"),
                        "4% = 0.04. 0.4 = 0.40. 40 hundredths &gt; 4 hundredths, so <b>0.4 &gt; 4%</b>."))
    its.append(cmp_item("0.7", D("0.7"), "0.65", D("0.65"),
                        "0.7 = 0.70. Compare the tenths: 7 tenths &gt; 6 tenths. So <b>0.7 &gt; 0.65</b>, even though 65 &gt; 7."))
    its.append(cmp_item("0.09", D("0.09"), "0.1", D("0.1"),
                        "0.1 = 0.10. Compare the tenths: 0 &lt; 1. So <b>0.09 &lt; 0.1</b>."))
    its.append(cmp_item(fr(1, 4), F(1, 4), "0.4", D("0.4"),
                        "%s = %s = 0.25. 0.25 &lt; 0.40, so <b>%s &lt; 0.4</b>. %s is <b>not</b> 0.4."
                        % (fr(1, 4), fr(25, 100), fr(1, 4), fr(1, 4))))
    its.append(cmp_item(fr(3, 5), F(3, 5), "0.6", D("0.6"),
                        "%s = %s = 0.6. So <b>%s = 0.6</b>." % (fr(3, 5), fr(6, 10), fr(3, 5))))
    its.append(cmp_item(fr(1, 2), F(1, 2), "45%", pct("45%"),
                        "%s = %s = 50%%. 50%% &gt; 45%%, so <b>%s &gt; 45%%</b>." % (fr(1, 2), fr(50, 100), fr(1, 2))))
    its.append(cmp_item("0.3", D("0.3"), "30%", pct("30%"),
                        "0.3 = 0.30 = 30 hundredths = 30%. So <b>0.3 = 30%</b>."))
    its.append(cmp_item(fr(3, 4), F(3, 4), "0.8", D("0.8"),
                        "%s = 0.75 and 0.8 = 0.80. 75 hundredths &lt; 80 hundredths, so <b>%s &lt; 0.8</b>." % (fr(3, 4), fr(3, 4))))
    its.append(cmp_item(fr(7, 20), F(7, 20), "0.3", D("0.3"),
                        "%s = %s = 0.35. 0.35 &gt; 0.30, so <b>%s &gt; 0.3</b>." % (fr(7, 20), fr(35, 100), fr(7, 20))))
    its.append(cmp_item("12%", pct("12%"), "0.2", D("0.2"),
                        "0.2 = 0.20 = 20%. 12% &lt; 20%, so <b>12% &lt; 0.2</b>."))

    def order_q(q, vals, asc, wrongs, e):
        s = sorted(vals, key=lambda t: t[1], reverse=not asc)
        assert len(set(v for _, v in vals)) == len(vals)
        right = ", ".join(h for h, _ in s)
        return mcq(q, right, [", ".join(w) for w in wrongs], e, same_ok=True)

    its.append(order_q("Order from <b>least to greatest</b>:<br><b>0.5, 0.45, 0.05, 0.54</b>",
                       [("0.5", D("0.5")), ("0.45", D("0.45")), ("0.05", D("0.05")), ("0.54", D("0.54"))], True,
                       [["0.5", "0.05", "0.45", "0.54"], ["0.05", "0.5", "0.45", "0.54"], ["0.54", "0.5", "0.45", "0.05"]],
                       "Write them all with 2 places: 0.50, 0.45, 0.05, 0.54. Compare 50, 45, 5 and 54 hundredths. "
                       "So <b>0.05, 0.45, 0.5, 0.54</b>."))
    its.append(order_q("Order from <b>least to greatest</b>:<br><b>0.3, %s, 28%%</b>" % fr(1, 4),
                       [("0.3", D("0.3")), (fr(1, 4), F(1, 4)), ("28%", pct("28%"))], True,
                       [["0.3", fr(1, 4), "28%"], ["28%", "0.3", fr(1, 4)], [fr(1, 4), "0.3", "28%"]],
                       "Make them all decimals: 0.3 = 0.30, %s = 0.25, 28%% = 0.28. So the order is <b>%s, 28%%, 0.3</b>."
                       % (fr(1, 4), fr(1, 4))))
    its.append(order_q("Order from <b>greatest to least</b>:<br><b>%s, 0.65, 58%%</b>" % fr(3, 5),
                       [(fr(3, 5), F(3, 5)), ("0.65", D("0.65")), ("58%", pct("58%"))], False,
                       [[fr(3, 5), "0.65", "58%"], ["58%", fr(3, 5), "0.65"], ["58%", "0.65", fr(3, 5)]],
                       "As decimals: %s = 0.60, 0.65 and 58%% = 0.58. Greatest first: <b>0.65, %s, 58%%</b>."
                       % (fr(3, 5), fr(3, 5))))
    its.append(order_q("Order from <b>least to greatest</b>:<br><b>52%%, %s, 0.48</b>" % fr(1, 2),
                       [("52%", pct("52%")), (fr(1, 2), F(1, 2)), ("0.48", D("0.48"))], True,
                       [["52%", fr(1, 2), "0.48"], [fr(1, 2), "0.48", "52%"], ["0.48", "52%", fr(1, 2)]],
                       "As decimals: 52%% = 0.52, %s = 0.50, 0.48. So <b>0.48, %s, 52%%</b>." % (fr(1, 2), fr(1, 2))))
    its.append(order_q("Order from <b>least to greatest</b>:<br><b>%s, 0.75, 85%%</b>" % fr(4, 5),
                       [(fr(4, 5), F(4, 5)), ("0.75", D("0.75")), ("85%", pct("85%"))], True,
                       [[fr(4, 5), "0.75", "85%"], ["0.75", "85%", fr(4, 5)], ["85%", fr(4, 5), "0.75"]],
                       "As decimals: %s = 0.80, 0.75, 85%% = 0.85. So <b>0.75, %s, 85%%</b>." % (fr(4, 5), fr(4, 5))))
    its.append(mcq("Which is the <b>greatest</b>?", fr(3, 4), ["0.7", "72%", "0.07"],
                   "As decimals: %s = 0.75, 0.70, 72%% = 0.72, 0.07. The greatest is <b>%s</b>." % (fr(3, 4), fr(3, 4))))
    its.append(mcq("Which is the <b>least</b>?", "18%", ["0.2", fr(1, 4), "0.21"],
                   "As decimals: 18%% = 0.18, 0.20, %s = 0.25, 0.21. The least is <b>18%%</b>." % fr(1, 4)))
    its.append(mcq("Which number is between 0.4 and 0.5?", fr(9, 20), [fr(1, 4), "52%", "0.04"],
                   "%s = %s = 0.45, which is between 0.40 and 0.50. %s = 0.25, 52%% = 0.52 and 0.04 are not."
                   % (fr(9, 20), fr(45, 100), fr(1, 4))))
    its.append(mcq(fig(line_svg(5, 2, {0: "0%", 5: "100%"})) +
                   "The line from 0% to 100% is split into 5 equal parts. What percent is at the red dot?",
                   "40%", ["2%", "20%", "25%"],
                   "5 equal parts, so each part is %s = 20%%. The dot is 2 parts along: 2 × 20%% = <b>40%%</b>. "
                   "20%% is only one part." % fr(1, 5), value=F(2, 5)))
    its.append(mcq(fig(line_svg(20, 7, {0: "0", 10: "0.5", 20: "1"})) +
                   "The line from 0 to 1 is split into 20 equal parts. What decimal is at the red dot?",
                   "0.35", ["0.7", "0.07", "0.65"],
                   "20 equal parts, so each part is %s = 0.05. The dot is 7 parts along: %s = %s = <b>0.35</b>. "
                   "0.7 counts the parts as tenths, but there are 20 parts, not 10." % (fr(1, 20), fr(7, 20), fr(35, 100)),
                   value=F(7, 20)))
    order = [0, 1, 2, 3, 4, 6, 5, 7, 8, 9, 10, 15, 16, 18, 11, 17, 12, 13, 14, 19]
    its = [its[i] for i in order]
    assert len(its) == 20 and len(set(order)) == 20
    return {"title": "Compare and order fractions, decimals and percents", "items": its}


# ============================================================ set 5: word problems
def set_problems(P):
    its = []
    n, he, his = P.next()
    its.append(mcq("%s scores 18 out of 20 on a spelling test. What percent does %s score?" % (n, he),
                   "90%", ["18%", "10%", "9%"],
                   "%s = %s (multiply the top and bottom by 5) = <b>90%%</b>. 10%% is the part %s got wrong."
                   % (fr(18, 20), fr(90, 100), he), value=F(18, 20)))
    n, he, his = P.next()
    its.append(mcq("%s gets 23 out of 25 on a math quiz. What percent is that?" % n,
                   "92%", ["23%", "8%", "2%"],
                   "25 × 4 = 100, so %s = %s = <b>92%%</b>. 23%% forgets to multiply by 4, and 8%% is the part %s missed."
                   % (fr(23, 25), fr(92, 100), he), value=F(23, 25)))
    its.append(mcq("15 of the 25 students in a Grade 5 class are going on a field trip. What percent of the class is going?",
                   "60%", ["15%", "40%", "10%"],
                   "%s = %s = <b>60%%</b>. 40%% is the part of the class that is not going." % (fr(15, 25), fr(60, 100)),
                   value=F(15, 25)))
    its.append(mcq("A pair of winter boots costs $80. The store takes 25% off. How much money is taken off?",
                   "$20", ["$25", "$60", "$40"],
                   "25%% = %s. %s of $80 is $80 ÷ 4 = <b>$20</b>. $60 is the sale price, and $25 confuses 25%% with $25."
                   % (fr(1, 4), fr(1, 4)), value=20))
    its.append(mcq("A hockey stick costs $40. It is on sale for 25% off. What is the sale price?",
                   "$30", ["$10", "$15", "$50"],
                   "25%% = %s, and %s of $40 is $10. The sale price is $40 − $10 = <b>$30</b>. "
                   "$10 is only the amount taken off, and $15 takes away $25 instead of 25%%." % (fr(1, 4), fr(1, 4)), value=30))
    its.append(mcq("A T-shirt costs $30. It is 10% off. What is the sale price?", "$27", ["$3", "$20", "$29.90"],
                   "10%% = %s. %s of $30 is $3. $30 − $3 = <b>$27</b>. $20 takes away $10 instead of 10%%."
                   % (fr(1, 10), fr(1, 10)), value=27))
    its.append(mcq("Store A has %s off a pair of skates. Store B has 20%% off the same skates. Which store takes off more?"
                   % fr(1, 4), "Store A", ["Store B", "They take off the same", "You can’t tell"],
                   "%s = 25%%, and 25%% &gt; 20%%. The skates cost the same to start with, so <b>Store A</b> takes off more."
                   % fr(1, 4)))
    a, ah, _ = P.next()
    b, bh, _ = P.next()
    its.append(mcq("On a science test, %s scores 21 out of 25 and %s scores 17 out of 20. Who has the higher percent?" % (a, b),
                   b, [a, "They are the same", "You can’t tell"],
                   "%s = %s = 84%%. %s = %s = 85%%. 85%% &gt; 84%%, so <b>%s</b> did better, even with fewer marks."
                   % (fr(21, 25), fr(84, 100), fr(17, 20), fr(85, 100), b)))
    its.append(mcq("At one school, 0.7 of the students stay for lunch. The rest go home for lunch. "
                   "What percent go home?", "30%", ["70%", "3%", "7%"],
                   "0.7 = 70% stay. All the students are 100%, so 100% − 70% = <b>30%</b> go home."))
    its.append(mcq("In a Grade 5 class, %s of the students walk to school. What percent of the class walk?" % fr(3, 5),
                   "60%", ["35%", "40%", "53%"],
                   "%s = %s = <b>60%%</b>. 35%% just writes the digits 3 and 5." % (fr(3, 5), fr(60, 100)), value=F(3, 5)))
    its.append(mcq("The forecast says there is a <b>75% chance of snow</b> tomorrow. What fraction is that?", fr(3, 4),
                   [fr(1, 4), fr(75, 10), fr(7, 5)],
                   "75%% = %s. Divide the top and bottom by 25: <b>%s</b>. %s is the chance that it does <b>not</b> snow."
                   % (fr(75, 100), fr(3, 4), fr(1, 4)), value=F(3, 4)))
    its.append(mcq("There is a 75% chance of snow tomorrow. What is the chance that it does <b>not</b> snow, as a decimal?",
                   "0.25", ["0.75", "0.025", "2.5"],
                   "Snow or no snow makes 100%. 100% − 75% = 25% = <b>0.25</b>. 0.75 is the chance of snow.", value=F(1, 4)))
    its.append(mcq("A hockey team won 12 of its 20 games this season. What percent of its games did it win?",
                   "60%", ["12%", "40%", "8%"],
                   "20 × 5 = 100, so %s = %s = <b>60%%</b>. 40%% is the games it did not win." % (fr(12, 20), fr(60, 100)),
                   value=F(3, 5)))
    its.append(mcq("Two maple syrup jugs are the same size. Jug A is %s full. Jug B is 0.4 full. Which jug has more syrup?"
                   % fr(1, 4), "Jug B", ["Jug A", "They have the same", "You can’t tell"],
                   "%s = %s = 0.25. 0.4 = 0.40. 0.40 &gt; 0.25, so <b>Jug B</b> has more. Watch out: %s is not 0.4."
                   % (fr(1, 4), fr(25, 100), fr(1, 4))))
    n, he, his = P.next()
    its.append(mcq("%s’s tablet battery shows 45%%. What fraction of a full charge is that, in simplest form?" % n, fr(9, 20),
                   [fr(4, 5), fr(1, 45), fr(11, 20)],
                   "45%% = %s. Divide the top and bottom by 5: <b>%s</b>. %s is the part that is empty."
                   % (fr(45, 100), fr(9, 20), fr(11, 20)), value=F(9, 20)))
    n, he, his = P.next()
    its.append(mcq("%s has 1 m of ribbon. %s uses 0.35 m for a craft. What fraction of the metre is left, in simplest form?"
                   % (n, he.capitalize()), fr(13, 20), [fr(7, 20), fr(65, 10), fr(3, 5)],
                   "1 − 0.35 = 0.65 m is left. 0.65 = %s = <b>%s</b> (divide by 5). %s is the part %s used."
                   % (fr(65, 100), fr(13, 20), fr(7, 20), he), value=F(13, 20)))
    its.append(mcq("A loonie ($1) is shared equally among 4 friends. How much does each friend get?", "25¢",
                   ["40¢", "$4", "4¢"],
                   "$1 ÷ 4 = %s of a dollar = %s = $0.25 = <b>25¢</b>. 40¢ is the mistake %s = 0.4."
                   % (fr(1, 4), fr(25, 100), fr(1, 4)), value=F(1, 4)))
    its.append(mcq("50 students from one school run in the Terry Fox Run. 41 of them run the whole 5 km. "
                   "What percent run the whole 5 km?", "82%", ["41%", "18%", "9%"],
                   "50 × 2 = 100, so %s = %s = <b>82%%</b>. 41%% forgets to multiply by 2, and 18%% is the part that did not run the whole way."
                   % (fr(41, 50), fr(82, 100)), value=F(41, 50)))
    a, _, _ = P.next()
    b, _, _ = P.next()
    c, _, _ = P.next()
    its.append(mcq("On a reading test, %s gets %s of the questions right, %s gets 0.8 of them right and %s gets 82%%. "
                   "Who has the highest score?" % (a, fr(17, 20), b, c), a, [b, c, "They are all the same"],
                   "Make them all percents: %s = %s = 85%%, 0.8 = 80%%, and 82%%. 85%% is the highest, so <b>%s</b>."
                   % (fr(17, 20), fr(85, 100), a)))
    n, he, his = P.next()
    its.append(mcq("A quiz has 20 questions. %s gets 0.75 of them right. How many questions does %s get right?" % (n, he),
                   "15", ["75", "7.5", "5"],
                   "0.75 = %s, and %s of 20 is 20 ÷ 4 × 3 = <b>15</b> questions. 5 is the number %s gets wrong, and 7.5 multiplies by 10 instead of 20."
                   % (fr(3, 4), fr(3, 4), he)))
    assert len(its) == 20, len(its)
    return {"title": "Word problems: test scores and 25% off", "items": its}


# ============================================================ lesson
def body_html():
    f_grid = grid_svg(35, cell=22)
    f_line = line_svg(4, 1, {0: "0", 2: "0.5", 4: "1"})
    return (
        "<h2>Three ways to show the same amount</h2>"
        "<p>A hundred grid has 100 equal squares. The shaded part can be named as a <b>fraction</b>, a <b>decimal</b> "
        "or a <b>percent</b>. Percent means <b>out of 100</b>.</p>"
        "<figure class='sn-fig'>" + f_grid +
        "<figcaption>35 of 100 squares are shaded: " + fr(35, 100) + " = 0.35 = 35%.</figcaption></figure>"
        + ex("Example", "40 of 100 squares are shaded. Name the shaded part three ways.",
             "40 out of 100 is " + fr(40, 100) + ". That is 40 hundredths, or 4 tenths.", fr(40, 100) + " = 0.4 = 40%")
        + "<h2>Fractions as decimals</h2>"
        "<p>Make an equivalent fraction with a denominator of 10 or 100. Multiply the top and bottom by the same number.</p>"
        + table(["Denominator", "Multiply by", "Example"], [
            ["2", "5 (to make 10)", fr(1, 2) + " = " + fr(5, 10) + " = 0.5"],
            ["5", "2 (to make 10)", fr(3, 5) + " = " + fr(6, 10) + " = 0.6"],
            ["4", "25 (to make 100)", fr(1, 4) + " = " + fr(25, 100) + " = 0.25"],
            ["20", "5 (to make 100)", fr(7, 20) + " = " + fr(35, 100) + " = 0.35"],
            ["25", "4 (to make 100)", fr(6, 25) + " = " + fr(24, 100) + " = 0.24"],
            ["50", "2 (to make 100)", fr(3, 50) + " = " + fr(6, 100) + " = 0.06"],
        ])
        + "<figure class='sn-fig'>" + f_line +
        "<figcaption>The line from 0 to 1 has 4 equal parts. The dot is at " + fr(1, 4) + " = 0.25, not 0.4.</figcaption></figure>"
        + ex("Example", "Write " + fr(9, 20) + " as a decimal and a percent.",
             "20 × 5 = 100, so multiply the top by 5 too: " + fr(9, 20) + " = " + fr(45, 100) + ".", "0.45 = 45%")
        + "<h2>Decimals and percents</h2>"
        "<p>Read the decimal as hundredths. 0.4 = 0.40 = 40 hundredths = 40%. 0.07 = 7 hundredths = 7%.</p>"
        + table(["Fraction", "Decimal", "Percent"], [
            [fr(1, 2), "0.5", "50%"],
            [fr(1, 4), "0.25", "25%"],
            [fr(3, 4), "0.75", "75%"],
            [fr(1, 5), "0.2", "20%"],
            [fr(1, 10), "0.1", "10%"],
            [fr(1, 20), "0.05", "5%"],
            [fr(1, 25), "0.04", "4%"],
        ])
        + "<h2>Comparing</h2>"
        "<p>Change all the numbers into the same form first. Hundredths are easiest: write each decimal with 2 places.</p>"
        + ex("Example", "Order 0.3, " + fr(1, 4) + " and 28% from least to greatest.",
             "0.3 = 0.30. " + fr(1, 4) + " = 0.25. 28% = 0.28. Compare 30, 25 and 28 hundredths.",
             fr(1, 4) + ", 28%, 0.3")
        + ex("25% off", "Boots cost $80. They are 25% off. What is the sale price?",
             "25% = " + fr(1, 4) + ". " + fr(1, 4) + " of $80 is $20. $80 − $20 = $60.", "$60")
        + "<h2>Common mistakes</h2>"
        + table(["Mistake", "What to do instead"], [
            ["0.4 = 4%", "0.4 = 0.40 = 40 hundredths = 40%"],
            [fr(1, 4) + " = 0.4", "Make hundredths: " + fr(1, 4) + " = " + fr(25, 100) + " = 0.25"],
            [fr(3, 5) + " = 0.35", "Make tenths: " + fr(3, 5) + " = " + fr(6, 10) + " = 0.6"],
            ["8% = 0.8", "8% = 8 hundredths = 0.08"],
            ["0.65 &gt; 0.7 because 65 &gt; 7", "Use 2 places: 0.65 &lt; 0.70"],
            ["25% off $80 means the price is $20", "$20 is the amount taken off. The sale price is $60."],
        ])
    )


FAQ = [
    {"q": "What do Grade 5 students learn about fractions, decimals and percents in Ontario?",
     "a": "In the Ontario Grade 5 math curriculum, students show how fractions, decimals to hundredths and whole-number percents are related, using tools like hundred grids and number lines, for example 3/4 = 0.75 = 75%."},
    {"q": "Is 1/4 equal to 0.4?",
     "a": "No. 1/4 = 25/100 = 0.25 = 25%. The 4 in 1/4 is the number of equal parts, not tenths, so 0.4 is a different number (2/5)."},
    {"q": "How do you change a decimal to a percent?",
     "a": "Read the decimal as hundredths. 0.4 = 0.40 = 40 hundredths = 40%, and 0.07 = 7 hundredths = 7%. A common mistake is writing 0.4 as 4%."},
    {"q": "How do you work out 25% off a price?",
     "a": "25% is 1/4, so divide the price by 4 to find the amount taken off, then subtract. For $80 boots, 1/4 of $80 is $20, so the sale price is $60."},
]


def mark_large(u, pattern):
    """Tag pictures that must print larger (hundred grids, number lines)."""
    rx = re.compile(r"<svg (?=[^>]*aria-label='" + pattern + ")")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u


def gen():
    rnd = random.Random(45808)
    P = People(rnd)
    sets = [set_grids(), set_fraction_decimal(), set_percent(), set_compare(), set_problems(P)]
    balance(sets, rnd)
    seen = set()
    for s in sets:
        assert len(s["items"]) == 20, (s["title"], len(s["items"]))
        assert sorted(it["a"] for it in s["items"]) == sorted([0, 1, 2, 3] * 5)
        for it in s["items"]:
            assert len(set(it["c"])) == 4, it
            assert it["q"].count("<svg") <= 1
            k = re.sub(r"<[^>]+>", "", it["q"]) + "|" + "|".join(sorted(it["c"]))
            assert k not in seen, it["q"]
            seen.add(k)
    u = {
        "country": "ca-on", "subject": "math", "grade": "grade-5", "slug": "fractions-decimals-and-percents", "sort": 8,
        "updated": UPDATED, "pdf_url": "",
        "title": "Fractions, Decimals and Percents",
        "seo_title": "Grade 5 Fractions, Decimals and Percents Worksheets with Answer Key (Ontario)",
        "short_title": "Fractions, decimals and percents",
        "domain": "Number",
        "standard_code": "Grade 5: B1.7",
        "standard_url": "https://www.dcp.edu.gov.on.ca/en/curriculum/elementary-mathematics",
        "standard_text": "Describe relationships and show equivalences among fractions, decimal numbers up to hundredths, and whole-number percents, using appropriate tools and drawings, in various contexts",
        "meta_desc": "Free Grade 5 math worksheets on fractions, decimals and percents: hundred grids, 1/4 = 0.25 = 25%, decimals as percents, comparing and ordering, and word problems with test scores and 25% off. 100 questions with an answer key, following the Ontario curriculum.",
        "key_big": "Percent means out of 100: 3/4 = 75/100 = 0.75 = 75%",
        "key_sub": "Make an equivalent fraction with a denominator of 10 or 100, then read it as tenths or hundredths. 0.4 = 40%, not 4%, and 1/4 = 0.25, not 0.4.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }
    return mark_large(u, "(hundred grid|2 hundred grids|number line)")


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
