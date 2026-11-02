# -*- coding: utf-8 -*-
"""
Canada (Ontario) Grade 6 Math: Fractions, decimals and percents
(Ontario Curriculum, Grades 1-8: Mathematics, 2020 — Grade 6, Number, B1)
  python3 tools/gen_ca_math_g6_fdp.py
Equivalent fractions and simplest form (halves to twelfths, improper fractions, mixed numbers);
fraction <-> decimal (3/8 = 3 ÷ 8 = 0.375, short division drawn from the real working);
decimal <-> whole-number percent; comparing and ordering mixed forms; word problems.
Every answer is checked with fractions.Fraction / decimal.Decimal (never float).
Canadian English, dollars and cents (¢), metric units. HTML attributes use single quotes (no backslashes in the JSON).
"""
import json, os, random, re
from decimal import Decimal as Dm
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "ca-on", "math", "grade-6")
UPDATED = "2026-11-02"
FILL = "#4fae74"
LINE = "#2b2b2b"
THIN = "#8a8a8a"
RED = "#d6453b"
BLUE = "#2f6fc0"
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
    (same_ok=True only where a 'not simplest form' or 'NOT equal' choice is meant). value: the exact answer to check."""
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


def dec(v):
    """Exact decimal text of a Fraction with a terminating decimal."""
    v = F(v)
    d = Dm(v.numerator) / Dm(v.denominator)
    assert F(d) == v, v
    return format(d.normalize(), "f")


def D(s):
    return F(Dm(s))


# ------------------------------------------------------------ pictures
def sfr(x, y, a, b, size=15, color=LINE):
    """Stacked fraction drawn in SVG, centred at x. y is the numerator baseline."""
    w = size * 0.62 * max(len(str(a)), len(str(b))) + 4
    return ("<text x='%.1f' y='%.1f' font-size='%d' font-weight='700' fill='%s' text-anchor='middle'>%s</text>"
            "<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='1.5'/>"
            "<text x='%.1f' y='%.1f' font-size='%d' font-weight='700' fill='%s' text-anchor='middle'>%s</text>"
            % (x, y, size, color, a, x - w / 2, y + 4, x + w / 2, y + 4, color, x, y + size + 4, size, color, b))


def bar_row(x0, y, W, H, n, k):
    s = []
    for i in range(n):
        s.append("<rect x='%.1f' y='%.1f' width='%.2f' height='%d' fill='%s' stroke='%s' stroke-width='2.5'/>"
                 % (x0 + i * W / float(n), y, W / float(n), H, FILL if i < k else "#fff", LINE))
    return "".join(s)


def two_bars_svg(n1, k1, n2, k2, W=264, H=36):
    s = bar_row(4, 4, W, H, n1, k1) + bar_row(4, 4 + H + 14, W, H, n2, k2)
    return svg_wrap(W + 8, 2 * H + 22, s, "two fraction bars of the same size, top bar %d of %d parts shaded, "
                    "bottom bar %d of %d parts shaded" % (k1, n1, k2, n2))


def group_bar_svg(n, k, g, W=276, H=40):
    """Fraction bar of n thin parts, first k shaded, a thick line after every g parts."""
    x0 = y = 4
    s = []
    for i in range(n):
        s.append("<rect x='%.1f' y='%d' width='%.2f' height='%d' fill='%s'/>"
                 % (x0 + i * W / float(n), y, W / float(n), H, FILL if i < k else "#fff"))
    for i in range(1, n):
        xx = x0 + i * W / float(n)
        thick = (i % g == 0)
        s.append("<line x1='%.1f' y1='%d' x2='%.1f' y2='%d' stroke='%s' stroke-width='%s'%s/>"
                 % (xx, y, xx, y + H, LINE if thick else THIN, "3" if thick else "1.5",
                    "" if thick else " stroke-dasharray='4 3'"))
    s.append("<rect x='%d' y='%d' width='%d' height='%d' fill='none' stroke='%s' stroke-width='3'/>" % (x0, y, W, H, LINE))
    return svg_wrap(W + 8, H + 8, "".join(s),
                    "fraction bar of %d equal parts with %d shaded, thick lines around groups of %d" % (n, k, g))


def quarters_line_svg(L, d, t, W=400):
    """Number line 0..L in steps of 1/d with a blue arrow pointing at t."""
    x0, x1, Y = 18, W - 18, 40
    s = ["<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='2.5'/>" % (x0, Y, x1, Y, LINE)]
    n = L * d
    for i in range(n + 1):
        X = x0 + (x1 - x0) * i / float(n)
        whole = (i % d == 0)
        s.append("<line x1='%.1f' y1='%d' x2='%.1f' y2='%d' stroke='%s' stroke-width='%s'/>"
                 % (X, Y - (12 if whole else 8), X, Y + (12 if whole else 8), LINE, "2.5" if whole else "1.6"))
        if whole:
            s.append(text(X, Y + 32, str(i // d), 17))
    X = x0 + (x1 - x0) * float(t) / L
    s.append("<line x1='%.1f' y1='4' x2='%.1f' y2='%d' stroke='%s' stroke-width='3'/>" % (X, X, Y - 20, BLUE))
    s.append("<path d='M%.1f %d L%.1f %d L%.1f %d Z' fill='%s'/>" % (X - 7, Y - 22, X + 7, Y - 22, X, Y - 10, BLUE))
    return svg_wrap(W, Y + 42, "".join(s),
                    "number line from 0 to %d with each whole split into %d equal parts and an arrow" % (L, d))


def grid_svg(k, cell=18):
    """10 x 10 hundred grid with k squares shaded: full columns first, then from the top of the next column."""
    pad = 4
    s = []
    for c in range(10):
        for r in range(10):
            if c * 10 + r < k:
                s.append("<rect x='%d' y='%d' width='%d' height='%d' fill='%s'/>" % (pad + c * cell, pad + r * cell, cell, cell, FILL))
    for i in range(1, 10):
        s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='1.2'/>"
                 % (pad + i * cell, pad, pad + i * cell, pad + 10 * cell, THIN))
        s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='1.2'/>"
                 % (pad, pad + i * cell, pad + 10 * cell, pad + i * cell, THIN))
    s.append("<rect x='%d' y='%d' width='%d' height='%d' fill='none' stroke='%s' stroke-width='2.5'/>"
             % (pad, pad, 10 * cell, 10 * cell, LINE))
    w = 10 * cell + 2 * pad
    return svg_wrap(w, w, "".join(s), "hundred grid with %d of 100 squares shaded" % k)


def short_div(a, b, places, hide=False):
    """Short division of a ÷ b, written to `places` decimal places, drawn from the real working.
    Remainders are carried as small red digits. hide=True draws the answer digits after the point as boxes."""
    w = str(a)
    cells = list(w) + ["."] + ["0"] * places
    q, carry, rem = [], {}, 0
    for i, ch in enumerate(cells):
        if ch == ".":
            q.append(".")
            continue
        cur = rem * 10 + int(ch)
        q.append(str(cur // b))
        rem = cur % b
        nxt = i + 1 if i + 1 < len(cells) and cells[i + 1] != "." else i + 2
        if rem and nxt < len(cells):
            carry[nxt] = str(rem)
    assert rem == 0, (a, b)
    assert F(Dm("".join(q))) == F(a, b), (q, a, b)
    lead = 0
    while lead < len(w) - 1 and q[lead] == "0":
        lead += 1
    CW, DW = 30, 14
    xs, x = [], 62
    for ch in cells:
        xs.append(x)
        x += DW if ch == "." else CW
    W = x + 10
    ytop, ybar, ydig = 34, 46, 78
    o = []
    for i, ch in enumerate(cells):
        cx = xs[i] + (DW if ch == "." else CW) / 2.0
        if ch == ".":
            o.append("<circle cx='%.1f' cy='%d' r='3.5' fill='%s'/>" % (cx, ydig - 2, LINE))
            o.append("<circle cx='%.1f' cy='%d' r='3.5' fill='%s'/>" % (cx, ytop - 2, LINE))
            continue
        o.append(text(cx + 3, ydig, ch, 26))
        if i in carry:
            o.append(text(xs[i] + 5, ydig - 14, carry[i], 15, col=RED))
        if i < lead:
            continue
        if hide and i > len(w):
            o.append("<rect x='%.1f' y='%d' width='20' height='24' fill='#fff' stroke='%s' stroke-width='1.8' rx='3'/>"
                     % (cx - 10, ytop - 22, LINE))
        else:
            o.append(text(cx + 3, ytop, q[i], 26))
    o.append("<line x1='54' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='2.5'/>" % (ybar, W - 6, ybar, LINE))
    o.append("<path d='M 54 %d Q 62 %d 54 %d' fill='none' stroke='%s' stroke-width='2.5'/>" % (ybar, ybar + 22, ybar + 44, LINE))
    o.append(text(30, ydig, str(b), 26))
    return svg_wrap(W, ybar + 50, "".join(o), "short division of %s by %d" % ("".join(cells), b))


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


# ============================================================ set 1: equivalent fractions and simplest form
def set_equivalent():
    its = []
    its.append(mcq(fig(two_bars_svg(4, 3, 8, 6)) + "The two bars are the same size. Which fraction is equal to %s?" % fr(3, 4),
                   fr(6, 8), [fr(3, 8), fr(5, 6), fr(4, 3)],
                   "Each quarter is cut into 2 equal parts, so 3 quarters become 6 eighths: %s = <b>%s</b>. "
                   "%s adds 2 to the top and bottom, which does not keep the same amount." % (fr(3, 4), fr(6, 8), fr(5, 6)),
                   value=F(3, 4)))
    its.append(mcq("Find the missing number: %s = %s" % (fr(1, 2), fr("?", 10)), "5", ["9", "2", "20"],
                   "2 × 5 = 10, so multiply the numerator by 5 too: 1 × 5 = <b>5</b>. %s = %s. "
                   "9 adds 8 to the top as well as the bottom, which does not keep the fraction the same." % (fr(1, 2), fr(5, 10))))
    its.append(mcq(fig(two_bars_svg(3, 2, 12, 8)) + "Find the missing number: %s = %s" % (fr(2, 3), fr("?", 12)), "8", ["11", "4", "6"],
                   "3 × 4 = 12, so multiply the numerator by 4 too: 2 × 4 = <b>8</b>. The bars show 8 of 12 parts shaded. "
                   "4 is only 12 ÷ 3; the top has to be multiplied as well."))
    its.append(mcq("How many twelfths are in %s?" % fr(1, 3), "4", ["3", "9", "36"],
                   "3 × 4 = 12, so %s = %s. There are <b>4</b> twelfths. 36 comes from 12 × 3." % (fr(1, 3), fr(4, 12))))
    its.append(mcq("Which fraction is equal to %s?" % fr(5, 6), fr(10, 12), [fr(5, 12), fr(6, 7), fr(7, 8)],
                   "Multiply the top and bottom by 2: %s = <b>%s</b>. %s only changes the denominator, and %s adds 1 to each."
                   % (fr(5, 6), fr(10, 12), fr(5, 12), fr(6, 7)), value=F(5, 6)))
    its.append(mcq("Which fraction is <b>not</b> equal to %s?" % fr(1, 2), fr(4, 6), [fr(3, 6), fr(5, 10), fr(6, 12)],
                   "In %s, %s and %s the numerator is half of the denominator, so they equal %s. "
                   "Half of 6 is 3, not 4, so <b>%s</b> is not equal to %s. (It equals %s.)"
                   % (fr(3, 6), fr(5, 10), fr(6, 12), fr(1, 2), fr(4, 6), fr(1, 2), fr(2, 3)), same_ok=True))
    its.append(mcq("Write %s in simplest form." % fr(6, 8), fr(3, 4), [fr(3, 8), fr(3, 2), fr(4, 6)],
                   "Divide the top <b>and</b> bottom by 2: 6 ÷ 2 = 3 and 8 ÷ 2 = 4. So %s = <b>%s</b>. "
                   "%s divides only the top. %s subtracts 2 from each." % (fr(6, 8), fr(3, 4), fr(3, 8), fr(4, 6)),
                   value=F(3, 4)))
    its.append(mcq("Write %s in simplest form." % fr(9, 12), fr(3, 4), [fr(3, 12), fr(4, 3), fr(6, 9)],
                   "3 is a factor of 9 and 12. 9 ÷ 3 = 3 and 12 ÷ 3 = 4, so %s = <b>%s</b>. "
                   "%s divides only the top, and %s takes 3 from each." % (fr(9, 12), fr(3, 4), fr(3, 12), fr(6, 9)),
                   value=F(3, 4)))
    its.append(mcq("Write %s in simplest form." % fr(10, 12), fr(5, 6), [fr(5, 12), fr(6, 5), fr(1, 2)],
                   "Divide the top and bottom by 2: %s = <b>%s</b>. 5 and 6 have no common factor except 1, so it is in simplest form."
                   % (fr(10, 12), fr(5, 6)), value=F(5, 6)))
    its.append(mcq("Write %s in simplest form." % fr(8, 12), fr(2, 3), [fr(4, 6), fr(2, 12), fr(3, 2)],
                   "The greatest common factor of 8 and 12 is 4. 8 ÷ 4 = 2 and 12 ÷ 4 = 3, so %s = <b>%s</b>. "
                   "%s is equal, but not in simplest form: 4 and 6 can still both be divided by 2."
                   % (fr(8, 12), fr(2, 3), fr(4, 6)), same_ok=True, value=F(2, 3)))
    its.append(mcq("Which fraction is in simplest form?", fr(7, 12), [fr(4, 10), fr(6, 9), fr(3, 12)],
                   "7 and 12 have no common factor except 1, so <b>%s</b> is in simplest form. "
                   "%s = %s, %s = %s and %s = %s." % (fr(7, 12), fr(4, 10), fr(2, 5), fr(6, 9), fr(2, 3), fr(3, 12), fr(1, 4))))
    its.append(mcq(fig(group_bar_svg(12, 9, 3)) + "What fraction of the bar is shaded, in simplest form?", fr(3, 4),
                   [fr(9, 12), fr(3, 12), fr(4, 3)],
                   "9 of 12 parts are shaded: %s. The thick lines make 4 groups of 3, and 3 groups are shaded: "
                   "%s = <b>%s</b>. %s is equal, but not in simplest form." % (fr(9, 12), fr(9, 12), fr(3, 4), fr(9, 12)),
                   same_ok=True, value=F(3, 4)))
    its.append(mcq("Find the missing number: %s = %s" % (fr(4, 10), fr(6, "?")), "15", ["12", "20", "60"],
                   "Simplify first: %s = %s. Then 2 × 3 = 6, so 5 × 3 = <b>15</b>. %s = %s. "
                   "12 adds 2 to the top and bottom, which does not keep the same amount."
                   % (fr(4, 10), fr(2, 5), fr(6, 15), fr(4, 10))))
    its.append(mcq("Write %s as a mixed number." % fr(11, 4), mixed(2, 3, 4), [mixed(7, 1, 4), mixed(1, 1, 4), mixed(3, 1, 4)],
                   "11 ÷ 4 = 2 R 3. That is 2 wholes and 3 quarters left over: <b>%s</b>. "
                   "%s reads 11 as 1 and 1." % (mixed(2, 3, 4), mixed(1, 1, 4)), value=F(11, 4)))
    its.append(mcq("Write %s as a mixed number." % fr(17, 6), mixed(2, 5, 6), [mixed(3, 1, 6), mixed(1, 7, 6), mixed(2, 6, 5)],
                   "17 ÷ 6 = 2 R 5. That is 2 wholes and 5 sixths: <b>%s</b>. "
                   "%s writes the remainder and the divisor the wrong way round." % (mixed(2, 5, 6), mixed(2, 6, 5)),
                   value=F(17, 6)))
    its.append(mcq("Write %s as an improper fraction." % mixed(3, 2, 5), fr(17, 5), [fr(11, 5), fr(6, 5), fr(32, 5)],
                   "3 wholes = %s. Add the 2 fifths: 15 + 2 = 17, so %s = <b>%s</b>. "
                   "%s multiplies 3 × 2; the whole number is multiplied by the denominator." % (fr(15, 5), mixed(3, 2, 5), fr(17, 5), fr(6, 5)),
                   value=F(17, 5)))
    its.append(mcq("Write %s as an improper fraction." % mixed(2, 3, 8), fr(19, 8), [fr(14, 8), fr(5, 8), fr(23, 8)],
                   "2 × 8 = 16 eighths in 2 wholes. 16 + 3 = 19, so %s = <b>%s</b>. "
                   "%s just adds 2 + 3, and %s writes the digits together." % (mixed(2, 3, 8), fr(19, 8), fr(5, 8), fr(23, 8)),
                   value=F(19, 8)))
    its.append(mcq("Which improper fraction is equal to %s?" % mixed(2, 1, 2), fr(5, 2), [fr(3, 2), fr(21, 2), fr(4, 2)],
                   "2 wholes = %s. Add the half: 4 + 1 = 5, so %s = <b>%s</b>. %s forgets to add the 1 half."
                   % (fr(4, 2), mixed(2, 1, 2), fr(5, 2), fr(4, 2)), value=F(5, 2)))
    its.append(mcq(fig(quarters_line_svg(3, 4, F(9, 4))) + "Each whole is split into quarters. Which fraction is at the arrow?",
                   fr(9, 4), [fr(9, 12), fr(4, 9), fr(1, 4)],
                   "Count the quarters from 0: 4 to reach 1, 8 to reach 2, then 1 more. That is <b>%s</b> = %s. "
                   "%s uses all 12 quarters on the line as the denominator, but each <b>whole</b> has 4 parts."
                   % (fr(9, 4), mixed(2, 1, 4), fr(9, 12)), value=F(9, 4)))
    its.append(mcq("Write %s as a mixed number in simplest form." % fr(18, 12), mixed(1, 1, 2),
                   [mixed(1, 6, 12), mixed(1, 1, 6), fr(6, 4)],
                   "18 ÷ 12 = 1 R 6, so %s = %s. Then simplify %s = %s: <b>%s</b>. "
                   "%s and %s are equal but not in simplest form." % (fr(18, 12), mixed(1, 6, 12), fr(6, 12), fr(1, 2),
                                                                      mixed(1, 1, 2), mixed(1, 6, 12), fr(6, 4)),
                   same_ok=True, value=F(3, 2)))
    order = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 17, 15, 16, 18, 19]
    its = [its[i] for i in order]
    assert len(its) == 20, len(its)
    return {"title": "Equivalent fractions, simplest form and mixed numbers", "items": its}


# ============================================================ set 2: fractions and decimals
def set_fraction_decimal():
    its = []

    def f2d(n, d, right, wrong, e, q=None, fg=""):
        assert D(right) == F(n, d), (n, d, right)
        its.append(mcq(fg + (q or "Write %s as a decimal." % fr(n, d)), right, wrong, e))

    f2d(7, 10, "0.7", ["0.07", "7.10", "0.710"],
        "7 tenths: the 7 goes in the tenths place, the first place after the decimal point. %s = <b>0.7</b>." % fr(7, 10))
    f2d(23, 100, "0.23", ["2.3", "0.023", "23.100"],
        "23 hundredths: the last digit goes in the hundredths place, the second place after the point. %s = <b>0.23</b>." % fr(23, 100))
    f2d(9, 100, "0.09", ["0.9", "0.009", "9.100"],
        "9 hundredths: write a 0 in the tenths place to hold it. %s = <b>0.09</b>. 0.9 would be 9 tenths." % fr(9, 100))
    f2d(47, 1000, "0.047", ["0.47", "4.7", "0.0047"],
        "47 thousandths: the last digit goes in the thousandths place, the third place after the point. "
        "%s = <b>0.047</b>. 0.47 would be 47 hundredths." % fr(47, 1000))
    f2d(1, 2, "0.5", ["0.12", "1.2", "0.2"],
        "%s = %s = <b>0.5</b>. 0.12 and 1.2 just write the digits of the fraction." % (fr(1, 2), fr(5, 10)))
    f2d(1, 4, "0.25", ["0.14", "0.4", "1.4"],
        "%s = %s (multiply the top and bottom by 25) = <b>0.25</b>. 0.4 uses the denominator as tenths." % (fr(1, 4), fr(25, 100)))
    f2d(3, 5, "0.6", ["0.35", "3.5", "0.53"],
        "%s = %s (multiply the top and bottom by 2) = <b>0.6</b>. 0.35 just writes the digits 3 and 5." % (fr(3, 5), fr(6, 10)))
    f2d(2, 5, "0.4", ["0.25", "2.5", "0.2"],
        "%s = %s = <b>0.4</b>. 2.5 is 5 ÷ 2, the wrong way round, and 0.2 is only %s." % (fr(2, 5), fr(4, 10), fr(1, 5)))
    f2d(1, 8, "0.125", ["0.18", "0.8", "0.12"],
        "1 ÷ 8: write 1 as 1.000. 10 ÷ 8 = 1 R 2, 20 ÷ 8 = 2 R 4, 40 ÷ 8 = 5. So %s = <b>0.125</b>. "
        "0.12 stops before the remainder is 0." % fr(1, 8))
    f2d(3, 8, "0.375", ["0.38", "3.8", "0.83"],
        "30 ÷ 8 = 3 R 6, 60 ÷ 8 = 7 R 4, 40 ÷ 8 = 5. So 3 ÷ 8 = <b>0.375</b>. 0.38 and 3.8 just use the digits of the fraction.",
        q="The division shows 3 ÷ 8. What is %s as a decimal?" % fr(3, 8), fg=fig(short_div(3, 8, 3, hide=True)))
    f2d(5, 8, "0.625", ["0.58", "5.8", "1.6"],
        "50 ÷ 8 = 6 R 2, 20 ÷ 8 = 2 R 4, 40 ÷ 8 = 5. So 5 ÷ 8 = <b>0.625</b>. 1.6 is 8 ÷ 5, the wrong way round.",
        q="The division shows 5 ÷ 8. What is %s as a decimal?" % fr(5, 8), fg=fig(short_div(5, 8, 3, hide=True)))
    f2d(7, 20, "0.35", ["0.7", "0.14", "3.5"],
        "20 × 5 = 100, so multiply the top by 5 too: %s = %s = <b>0.35</b>. 0.7 would be %s."
        % (fr(7, 20), fr(35, 100), fr(7, 10)))
    f2d(11, 25, "0.44", ["0.11", "4.4", "0.36"],
        "25 × 4 = 100, so %s = %s = <b>0.44</b>. 0.11 forgets to multiply the top by 4, and 0.36 adds 11 + 25."
        % (fr(11, 25), fr(44, 100)))
    f2d(9, 12, "0.75", ["0.912", "0.9", "0.12"],
        "Simplify first: %s = %s. Then %s = %s = <b>0.75</b>." % (fr(9, 12), fr(3, 4), fr(3, 4), fr(75, 100)),
        q="Write %s as a decimal." % fr(9, 12))
    f2d(11, 4, "2.75", ["11.4", "2.3", "0.275"],
        "11 ÷ 4 = 2 R 3, so %s = %s. %s = 0.75, so the answer is <b>2.75</b>. "
        "2.3 writes the remainder 3 as a decimal digit." % (fr(11, 4), mixed(2, 3, 4), fr(3, 4)))
    f2d(19, 8, "2.375", ["2.38", "23.8", "2.83"],
        "The 2 wholes stay the same. %s = 3 ÷ 8 = 0.375. So %s = <b>2.375</b>." % (fr(3, 8), mixed(2, 3, 8)),
        q="Write %s as a decimal." % mixed(2, 3, 8))

    def d2f(s, right, wrong, e, v):
        assert D(s) == v
        its.append(mcq("Write <b>%s</b> as a fraction in simplest form." % s, right, wrong, e, value=v))

    d2f("0.6", fr(3, 5), [fr(6, 100), fr(1, 6), fr(2, 3)],
        "0.6 = 6 tenths = %s. Divide the top and bottom by 2: <b>%s</b>. %s would be 0.06." % (fr(6, 10), fr(3, 5), fr(6, 100)), F(3, 5))
    d2f("0.25", fr(1, 4), [fr(25, 10), fr(2, 5), fr(1, 25)],
        "0.25 = 25 hundredths = %s. Divide the top and bottom by 25: <b>%s</b>. %s would be 2.5." % (fr(25, 100), fr(1, 4), fr(25, 10)),
        F(1, 4))
    d2f("0.08", fr(2, 25), [fr(8, 10), fr(1, 8), fr(8, 1000)],
        "0.08 = 8 hundredths = %s. Divide the top and bottom by 4: <b>%s</b>. %s would be 0.8." % (fr(8, 100), fr(2, 25), fr(8, 10)),
        F(2, 25))
    d2f("0.375", fr(3, 8), [fr(375, 100), fr(3, 75), fr(3, 5)],
        "0.375 has three decimal places, so it is %s. Divide the top and bottom by 125: <b>%s</b>. %s would be 3.75."
        % (fr(375, 1000), fr(3, 8), fr(375, 100)), F(3, 8))
    order = [0, 1, 2, 3, 4, 5, 6, 7, 16, 17, 8, 9, 10, 11, 12, 13, 18, 19, 14, 15]
    its = [its[i] for i in order]
    assert len(its) == 20, len(its)
    return {"title": "Fractions and decimals: 3/8 = 3 ÷ 8 = 0.375", "items": its}


# ============================================================ set 3: decimals and percents
def set_percent():
    its = []
    its.append(mcq(fig(grid_svg(20)) + "What percent of the hundred grid is shaded?", "20%", ["2%", "80%", "0.2%"],
                   "20 of the 100 squares are shaded. Percent means <b>out of 100</b>, so it is <b>20%</b>. "
                   "80% is the white part."))
    its.append(mcq(fig(grid_svg(35)) + "Which shows the shaded part as a decimal and a percent?",
                   "0.35 and 35%", ["3.5 and 35%", "0.35 and 3.5%", "0.65 and 65%"],
                   "35 of 100 squares: %s = <b>0.35</b> = <b>35%%</b>. 0.65 and 65%% describe the white part." % fr(35, 100)))
    its.append(mcq(fig(grid_svg(7)) + "What decimal of the hundred grid is shaded?", "0.07", ["0.7", "7", "0.93"],
                   "7 of 100 squares = 7 hundredths = <b>0.07</b> = 7%. 0.7 would be 70 squares."))
    for d_, right, wrong, e in [
        ("0.4", "40%", ["4%", "0.4%", "400%"],
         "0.4 = 4 tenths = 40 hundredths = <b>40%</b>. Multiply by 100: 0.4 × 100 = 40. 4% would be 0.04."),
        ("0.07", "7%", ["70%", "0.07%", "0.7%"],
         "0.07 = 7 hundredths = <b>7%</b>. 70% would be 0.7."),
        ("0.25", "25%", ["2.5%", "0.25%", "250%"],
         "0.25 = 25 hundredths = <b>25%</b>. Multiply by 100: the digits move 2 places to the left."),
        ("0.9", "90%", ["9%", "0.9%", "10%"],
         "0.9 = 0.90 = 90 hundredths = <b>90%</b>. 9% would be 0.09."),
        ("0.8", "80%", ["8%", "0.8%", "20%"],
         "0.8 × 100 = 80, so 0.8 = <b>80%</b>. 20% is the part that is left, 1 − 0.8 = 0.2."),
        ("0.12", "12%", ["1.2%", "120%", "0.12%"],
         "0.12 = 12 hundredths = <b>12%</b>. 120% would be 1.2."),
    ]:
        assert D(d_) * 100 == F(right.rstrip("%"))
        its.append(mcq("Write <b>%s</b> as a percent." % d_, right, wrong, e))
    for p_, right, wrong, e in [
        ("45%", "0.45", ["4.5", "0.045", "45"],
         "45% = 45 hundredths = <b>0.45</b>. Divide by 100: the digits move 2 places to the right."),
        ("8%", "0.08", ["0.8", "8", "0.008"],
         "8% = 8 hundredths. Hundredths are the second place after the point: <b>0.08</b>. 0.8 is 80%."),
        ("60%", "0.6", ["0.06", "6", "0.006"],
         "60% = 60 hundredths = 6 tenths = <b>0.6</b>. 0.06 is only 6%."),
        ("100%", "1", ["0.1", "100", "0.01"],
         "100% means 100 out of 100, the whole amount: 100 ÷ 100 = <b>1</b>."),
        ("3%", "0.03", ["0.3", "30", "0.003"],
         "3% = 3 hundredths = <b>0.03</b>. 0.3 would be 30%."),
    ]:
        assert F(p_.rstrip("%")) / 100 == D(right)
        its.append(mcq("Write <b>%s</b> as a decimal." % p_, right, wrong, e))
    for (n, d), right, wrong, e in [
        ((1, 4), "25%", ["14%", "4%", "40%"],
         "%s = %s = <b>25%%</b>. 14%% just writes the digits, and 4%% and 40%% use only the denominator." % (fr(1, 4), fr(25, 100))),
        ((3, 5), "60%", ["35%", "30%", "53%"],
         "%s = %s = <b>60%%</b>. 35%% just writes the digits 3 and 5." % (fr(3, 5), fr(60, 100))),
        ((3, 20), "15%", ["32%", "3%", "60%"],
         "20 × 5 = 100, so %s = %s = <b>15%%</b>. 60%% comes from 3 × 20." % (fr(3, 20), fr(15, 100))),
        ((9, 25), "36%", ["34%", "9%", "0.36%"],
         "25 × 4 = 100, so %s = %s = <b>36%%</b>. 34%% adds 9 + 25." % (fr(9, 25), fr(36, 100))),
    ]:
        assert F(right.rstrip("%")) / 100 == F(n, d)
        its.append(mcq("Write %s as a percent." % fr(n, d), right, wrong, e))
    its.append(mcq("Write <b>5%</b> as a fraction in simplest form.", fr(1, 20), [fr(1, 5), fr(5, 10), fr(1, 50)],
                   "5%% = %s. Divide the top and bottom by 5: <b>%s</b>. %s is 20%%, not 5%%."
                   % (fr(5, 100), fr(1, 20), fr(1, 5)), value=F(1, 20)))
    its.append(mcq("Which of these is <b>not</b> equal to 0.5?", "5%", ["50%", fr(1, 2), "0.50"],
                   "0.5 = 0.50 = %s = 50%%. <b>5%%</b> is 0.05, only one tenth as much." % fr(1, 2), same_ok=True))
    order = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19]
    its = [its[i] for i in order]
    assert len(its) == 20, len(its)
    return {"title": "Decimals and percents", "items": its}


# ============================================================ set 4: compare and order
def cmp_item(x, xv, y, yv, e):
    lt, gt, eq = "%s &lt; %s" % (x, y), "%s &gt; %s" % (x, y), "%s = %s" % (x, y)
    right = lt if xv < yv else gt if xv > yv else eq
    wrong = [c for c in (lt, gt, eq) if c != right] + ["You can’t tell"]
    return mcq("Compare <b>%s</b> and <b>%s</b>." % (x, y), right, wrong, e, same_ok=True)


def set_compare():
    its = []
    its.append(cmp_item("0.7", D("0.7"), "0.65", D("0.65"),
                        "0.7 = 0.70. Compare the tenths: 7 tenths &gt; 6 tenths. So <b>0.7 &gt; 0.65</b>, even though 65 &gt; 7."))
    its.append(cmp_item("0.35", D("0.35"), "0.305", D("0.305"),
                        "Write both with 3 decimal places: 0.350 and 0.305. Compare the hundredths: 5 &gt; 0. "
                        "So <b>0.35 &gt; 0.305</b>. More digits does not mean a greater number."))
    its.append(cmp_item("0.09", D("0.09"), "0.1", D("0.1"),
                        "0.1 = 0.10. Compare the tenths: 0 &lt; 1. So <b>0.09 &lt; 0.1</b>."))
    its.append(cmp_item(fr(1, 8), F(1, 8), fr(1, 6), F(1, 6),
                        "Both have 1 part. Eighths are <b>smaller</b> parts than sixths, because the whole is cut into more pieces. "
                        "So <b>%s &lt; %s</b>. A bigger denominator does not make a bigger fraction." % (fr(1, 8), fr(1, 6))))
    its.append(cmp_item(fr(5, 12), F(5, 12), fr(5, 8), F(5, 8),
                        "Same numerator: 5 twelfths and 5 eighths. Twelfths are smaller parts than eighths, so "
                        "<b>%s &lt; %s</b>." % (fr(5, 12), fr(5, 8))))
    its.append(cmp_item("0.6", D("0.6"), fr(3, 5), F(3, 5),
                        "%s = %s = 0.6. So <b>0.6 = %s</b>." % (fr(3, 5), fr(6, 10), fr(3, 5))))
    its.append(cmp_item("40%", F(2, 5), "0.04", D("0.04"),
                        "40% = 0.40. 0.40 &gt; 0.04, so <b>40% &gt; 0.04</b>. 0.04 is only 4%."))
    its.append(cmp_item(fr(1, 5), F(1, 5), "15%", F(15, 100),
                        "%s = %s = 20%%. 20%% &gt; 15%%, so <b>%s &gt; 15%%</b>." % (fr(1, 5), fr(20, 100), fr(1, 5))))
    its.append(cmp_item(fr(3, 8), F(3, 8), "0.35", D("0.35"),
                        "Change the fraction to a decimal: %s = 3 ÷ 8 = 0.375. 0.375 &gt; 0.350, so <b>%s &gt; 0.35</b>."
                        % (fr(3, 8), fr(3, 8))))
    its.append(cmp_item(fr(2, 3), F(2, 3), "0.66", D("0.66"),
                        "%s = 2 ÷ 3 = 0.666…, which is a little more than 0.66 = 0.660. So <b>%s &gt; 0.66</b>." % (fr(2, 3), fr(2, 3))))

    def order_q(q, vals, asc, wrongs, e):
        s = sorted(vals, key=lambda t: t[1], reverse=not asc)
        assert len(set(v for _, v in vals)) == len(vals)
        right = ", ".join(h for h, _ in s)
        return mcq(q, right, [", ".join(w) for w in wrongs], e, same_ok=True)

    its.append(order_q("Order from <b>least to greatest</b>:<br><b>0.5, 0.45, 0.405, 0.054</b>",
                       [("0.5", D("0.5")), ("0.45", D("0.45")), ("0.405", D("0.405")), ("0.054", D("0.054"))], True,
                       [["0.5", "0.45", "0.405", "0.054"], ["0.054", "0.45", "0.405", "0.5"], ["0.5", "0.054", "0.45", "0.405"]],
                       "Write them with 3 places: 0.500, 0.450, 0.405, 0.054. Compare 500, 450, 405 and 54 thousandths. "
                       "So <b>0.054, 0.405, 0.45, 0.5</b>."))
    its.append(order_q("Order from <b>least to greatest</b>:<br><b>0.35, %s, 37%%</b>" % fr(3, 8),
                       [("0.35", D("0.35")), (fr(3, 8), F(3, 8)), ("37%", F(37, 100))], True,
                       [[fr(3, 8), "0.35", "37%"], ["37%", "0.35", fr(3, 8)], ["0.35", fr(3, 8), "37%"]],
                       "Make them all decimals with 3 places: 0.350, %s = 0.375, 37%% = 0.370. "
                       "So the order is <b>0.35, 37%%, %s</b>." % (fr(3, 8), fr(3, 8))))
    its.append(order_q("Order from <b>greatest to least</b>:<br><b>0.8, %s, 79%%</b>" % fr(3, 4),
                       [("0.8", D("0.8")), (fr(3, 4), F(3, 4)), ("79%", F(79, 100))], False,
                       [["79%", fr(3, 4), "0.8"], [fr(3, 4), "79%", "0.8"], ["79%", "0.8", fr(3, 4)]],
                       "As decimals: 0.8 = 0.80, %s = 0.75, 79%% = 0.79. Greatest first: <b>0.8, 79%%, %s</b>."
                       % (fr(3, 4), fr(3, 4))))
    its.append(order_q("Which list is in order from <b>least to greatest</b>?",
                       [("0.6", D("0.6")), (fr(2, 3), F(2, 3)), ("70%", F(7, 10))], True,
                       [[fr(2, 3), "0.6", "70%"], ["70%", "0.6", fr(2, 3)], ["0.6", "70%", fr(2, 3)]],
                       "0.6 = 0.600, %s = 0.666… and 70%% = 0.700. So <b>0.6, %s, 70%%</b>." % (fr(2, 3), fr(2, 3))))
    its.append(order_q("Order from <b>least to greatest</b>:<br><b>1.2, %s, 1.15</b>" % mixed(1, 1, 4),
                       [("1.2", D("1.2")), (mixed(1, 1, 4), F(5, 4)), ("1.15", D("1.15"))], True,
                       [["1.2", "1.15", mixed(1, 1, 4)], [mixed(1, 1, 4), "1.2", "1.15"], ["1.15", mixed(1, 1, 4), "1.2"]],
                       "As decimals: 1.2 = 1.20, %s = 1.25, 1.15. So <b>1.15, 1.2, %s</b>. "
                       "1.15 has more digits but is the least." % (mixed(1, 1, 4), mixed(1, 1, 4))))
    its.append(mcq("Which is the <b>greatest</b>?", "0.45", [fr(2, 5), "42%", "0.405"],
                   "As decimals: 0.450, %s = 0.400, 42%% = 0.420, 0.405. The greatest is <b>0.45</b>." % fr(2, 5)))
    its.append(mcq("Which is the <b>least</b>?", "0.205", [fr(1, 4), "0.3", "22%"],
                   "As decimals: 0.205, %s = 0.250, 0.300, 22%% = 0.220. The least is <b>0.205</b>, "
                   "even though it has the most digits." % fr(1, 4)))
    its.append(mcq("Which number is between 0.3 and 0.4?", fr(3, 8), [fr(1, 4), "45%", "0.43"],
                   "%s = 0.375, which is between 0.3 and 0.4. %s = 0.25 and 45%% = 0.45 are not, and 0.43 is more than 0.4."
                   % (fr(3, 8), fr(1, 4))))
    its.append(mcq(fig(line_svg(8, 3, {0: "0", 4: "0.5", 8: "1"})) +
                   "The line from 0 to 1 is split into 8 equal parts. What decimal is at the red dot?",
                   "0.375", ["0.3", "0.38", "0.83"],
                   "8 equal parts, so each part is %s. The dot is 3 parts along: %s = 3 ÷ 8 = <b>0.375</b>. "
                   "0.3 would be 3 tenths, but the line has 8 parts, not 10." % (fr(1, 8), fr(3, 8))))
    its.append(mcq(fig(line_svg(5, 4, {0: "0%", 5: "100%"})) +
                   "The line from 0% to 100% is split into 5 equal parts. What percent is at the red dot?",
                   "80%", ["4%", "40%", "45%"],
                   "5 equal parts, so each part is %s = 20%%. The dot is 4 parts along: 4 × 20%% = <b>80%%</b>. "
                   "40%% counts each part as 10%%." % fr(1, 5)))
    order = [0, 2, 1, 3, 4, 5, 6, 7, 8, 9, 10, 15, 16, 18, 19, 11, 12, 17, 13, 14]
    its = [its[i] for i in order]
    assert len(its) == 20, len(its)
    return {"title": "Compare and order fractions, decimals and percents", "items": its}


# ============================================================ set 5: word problems
def set_problems(P):
    its = []
    n, he, his = P.next()
    its.append(mcq("%s scores 18 out of 20 on a spelling test. What percent does %s score?" % (n, he),
                   "90%", ["18%", "10%", "9%"],
                   "%s = %s (multiply the top and bottom by 5) = <b>90%%</b>. 10%% is the part %s got wrong."
                   % (fr(18, 20), fr(90, 100), he)))
    its.append(mcq("The forecast says there is a <b>75% chance of snow</b> tomorrow. What fraction is that?", fr(3, 4),
                   [fr(1, 4), fr(75, 10), fr(7, 5)],
                   "75%% = %s. Divide the top and bottom by 25: <b>%s</b>. %s is the chance that it does <b>not</b> snow."
                   % (fr(75, 100), fr(3, 4), fr(1, 4)), value=F(3, 4)))
    its.append(mcq("There is a 75% chance of snow tomorrow. What is the chance that it does <b>not</b> snow, as a decimal?",
                   "0.25", ["0.75", "0.025", "2.5"],
                   "Snow or no snow makes 100%. 100% − 75% = 25% = <b>0.25</b>. 0.75 is the chance of snow."))
    its.append(mcq("In a Grade 6 class, %s of the students walk to school. What percent of the class walk?" % fr(3, 5),
                   "60%", ["35%", "30%", "3.5%"],
                   "%s = %s = <b>60%%</b>. 35%% just writes the digits 3 and 5." % (fr(3, 5), fr(60, 100))))
    its.append(mcq("At one school, 0.7 of the students stay for lunch. The rest go home for lunch. "
                   "What percent go home?", "30%", ["70%", "3%", "0.3%"],
                   "0.7 = 70% stay. All the students are 100%, so 100% − 70% = <b>30%</b> go home."))
    its.append(mcq("A hockey team won 12 of its 16 games this season. What percent of its games did it win?",
                   "75%", ["12%", "25%", "16%"],
                   "%s = %s (divide by 4) = %s = <b>75%%</b>. 25%% is the games it did not win."
                   % (fr(12, 16), fr(3, 4), fr(75, 100))))
    its.append(mcq("Store A has %s off a pair of skates. Store B has 20%% off the same skates. Which store takes off more?"
                   % fr(1, 4), "Store A", ["Store B", "They take off the same", "You can’t tell"],
                   "%s = 25%%, and 25%% &gt; 20%%. The skates cost the same to start with, so <b>Store A</b> takes off more."
                   % fr(1, 4)))
    a, ah, _ = P.next()
    b, bh, _ = P.next()
    its.append(mcq("On a math test, %s scores 21 out of 25 and %s scores 17 out of 20. Who has the higher percent?" % (a, b),
                   b, [a, "They are the same", "You can’t tell"],
                   "%s = %s = 84%%. %s = %s = 85%%. 85%% &gt; 84%%, so <b>%s</b> does better, even with fewer marks."
                   % (fr(21, 25), fr(84, 100), fr(17, 20), fr(85, 100), b)))
    n, he, his = P.next()
    its.append(mcq("%s’s tablet battery shows 45%%. What fraction of a full charge is that?" % n, fr(9, 20),
                   [fr(4, 5), fr(1, 45), fr(45, 1000)],
                   "45%% = %s. Divide the top and bottom by 5: <b>%s</b>. %s would be 0.045."
                   % (fr(45, 100), fr(9, 20), fr(45, 1000)), value=F(9, 20)))
    n, he, his = P.next()
    its.append(mcq("%s cuts a 3 m rope into 4 equal pieces for a canoe trip. How long is each piece?" % n,
                   "0.75 m", ["1.33 m", "0.34 m", "0.25 m"],
                   "3 ÷ 4 = %s m = <b>0.75 m</b>. 1.33 m is about 4 ÷ 3, the wrong way round. 0.25 m would come from a 1 m rope."
                   % fr(3, 4), value=F(3, 4)))
    its.append(mcq("5 pizzas are shared equally among 8 students at a class party. How much pizza does each student get, as a decimal?",
                   "0.625", ["0.58", "1.6", "0.85"],
                   "5 ÷ 8 = %s. 50 ÷ 8 = 6 R 2, 20 ÷ 8 = 2 R 4, 40 ÷ 8 = 5, so each student gets <b>0.625</b> of a pizza. "
                   "1.6 is 8 ÷ 5." % fr(5, 8), value=F(5, 8)))
    its.append(mcq("Two maple syrup jugs are the same size. Jug A is %s full. Jug B is 0.4 full. Which jug has more syrup?" % fr(3, 8),
                   "Jug B", ["Jug A", "They have the same", "You can’t tell"],
                   "%s = 3 ÷ 8 = 0.375. 0.4 = 0.400. 0.400 &gt; 0.375, so <b>Jug B</b> has more." % fr(3, 8)))
    its.append(mcq("There are 50 students in Grade 6. 23 of them bike to school. What percent bike?",
                   "46%", ["23%", "27%", "2.3%"],
                   "%s = %s (multiply the top and bottom by 2) = <b>46%%</b>. 27%% uses the 27 students who do not bike."
                   % (fr(23, 50), fr(46, 100))))
    its.append(mcq("$2 is shared equally among 5 friends. How much does each friend get?", "40¢",
                   ["$2.50", "25¢", "4¢"],
                   "$2 ÷ 5 = %s of a dollar = %s = $0.40 = <b>40¢</b>. $2.50 is 5 ÷ 2, the wrong way round."
                   % (fr(2, 5), fr(4, 10)), value=F(2, 5)))
    a, ah, _ = P.next()
    b, bh, _ = P.next()
    its.append(mcq("%s scores 33 out of 40 on a reading test. %s scores 82%%. Who has the higher score?" % (a, b),
                   a, [b, "They are the same", "You can’t tell"],
                   "%s = 33 ÷ 40 = 0.825. 82%% = 0.820. 0.825 &gt; 0.820, so <b>%s</b> has the higher score."
                   % (fr(33, 40), a)))
    its.append(mcq("Four stores have a sale on the same winter boots. Which sign gives the <b>biggest</b> discount?",
                   "35% off", [fr(1, 3) + " off", "30% off", fr(1, 4) + " off"],
                   "As decimals: 0.35, %s = 0.333…, 0.30 and %s = 0.25. 0.35 is the greatest, so <b>35%% off</b>."
                   % (fr(1, 3), fr(1, 4))))
    n, he, his = P.next()
    its.append(mcq("%s has paddled 0.375 of the way across a lake in a canoe. What fraction of the way is that?" % n,
                   fr(3, 8), [fr(375, 100), fr(3, 75), fr(1, 375)],
                   "0.375 = %s. Divide the top and bottom by 125: <b>%s</b>. %s would be 3.75."
                   % (fr(375, 1000), fr(3, 8), fr(375, 100)), value=F(3, 8)))
    a, ah, _ = P.next()
    b, bh, bpos = P.next()
    its.append(mcq("In gym class, %s scores on 7 of 8 shots on net. %s scores on 85%% of %s shots. Who has the higher scoring rate?"
                   % (a, b, bpos), a, [b, "They are the same", "You can’t tell"],
                   "%s = 7 ÷ 8 = 0.875. 85%% = 0.850. 0.875 &gt; 0.850, so <b>%s</b> has the higher rate." % (fr(7, 8), a)))
    n, he, his = P.next()
    its.append(mcq("%s’s water bottle holds 1 L. %s drinks 0.35 L at recess. What fraction of the bottle is left?" % (n, he.capitalize()),
                   fr(13, 20), [fr(7, 20), fr(65, 10), fr(3, 5)],
                   "1 − 0.35 = 0.65 L is left. 0.65 = %s = <b>%s</b> (divide by 5). %s is the part %s drank."
                   % (fr(65, 100), fr(13, 20), fr(7, 20), he), value=F(13, 20)))
    n, he, his = P.next()
    its.append(mcq("A quiz has 20 questions. %s gets 0.85 of them right. How many questions does %s get right?" % (n, he),
                   "17", ["85", "8.5", "3"],
                   "0.85 = %s = %s. %s of 20 questions is <b>17</b> questions. 3 is the number %s gets wrong."
                   % (fr(85, 100), fr(17, 20), fr(17, 20), he)))
    assert len(its) == 20, len(its)
    return {"title": "Word problems: test scores, chances and sales", "items": its}


# ============================================================ lesson
def body_html():
    f_bars = two_bars_svg(4, 3, 8, 6)
    f_div = short_div(3, 8, 3)
    f_grid = grid_svg(20, cell=22)
    return (
        "<h2>Equivalent fractions</h2>"
        "<p>Equivalent fractions name the same amount. Multiply or divide the numerator <b>and</b> the denominator "
        "by the same number. A fraction is in <b>simplest form</b> when the only common factor of the top and bottom is 1.</p>"
        "<figure class='sn-fig'>" + f_bars +
        "<figcaption>Cut each quarter into 2 equal parts: " + fr(3, 4) + " = " + fr(6, 8) + ".</figcaption></figure>"
        + ex("Example", "Write " + fr(9, 12) + " in simplest form.",
             "3 is a factor of 9 and 12. 9 ÷ 3 = 3 and 12 ÷ 3 = 4.", fr(3, 4))
        + ex("Improper fraction to mixed number", "Write " + fr(11, 4) + " as a mixed number.",
             "11 ÷ 4 = 2 R 3. That is 2 wholes and 3 quarters.", mixed(2, 3, 4))
        + "<h2>Fractions and decimals</h2>"
        "<p>A fraction is a division: " + fr(3, 8) + " means 3 ÷ 8. Divide the numerator by the denominator. "
        "If the denominator goes into 10, 100 or 1000, you can make an equivalent fraction instead.</p>"
        "<figure class='sn-fig'>" + f_div +
        "<figcaption>3 ÷ 8: 30 ÷ 8 = 3 R 6, 60 ÷ 8 = 7 R 4, 40 ÷ 8 = 5. So " + fr(3, 8) + " = 0.375.</figcaption></figure>"
        + ex("Quicker way", "Write " + fr(7, 20) + " as a decimal.",
             "20 × 5 = 100, so multiply the top by 5 too: " + fr(7, 20) + " = " + fr(35, 100) + ".", "0.35")
        + "<h2>Decimals and percents</h2>"
        "<p>Percent means <b>out of 100</b>. To change a decimal to a percent, multiply by 100: 0.4 = 40%. "
        "To change a percent to a decimal, divide by 100: 7% = 0.07.</p>"
        "<figure class='sn-fig'>" + f_grid +
        "<figcaption>20 of 100 squares are shaded: " + fr(1, 5) + " = " + fr(20, 100) + " = 0.2 = 20%.</figcaption></figure>"
        + table(["Fraction", "Decimal", "Percent"], [
            [fr(1, 2), "0.5", "50%"],
            [fr(1, 4), "0.25", "25%"],
            [fr(3, 4), "0.75", "75%"],
            [fr(1, 5), "0.2", "20%"],
            [fr(1, 10), "0.1", "10%"],
            [fr(1, 20), "0.05", "5%"],
            [fr(1, 8), "0.125", "—"],
        ])
        + "<h2>Comparing and ordering</h2>"
        "<p>Change everything into the same form first. Decimals with the <b>same number of places</b> are easiest to compare.</p>"
        + ex("Example", "Order 0.35, " + fr(3, 8) + " and 37% from least to greatest.",
             "0.35 = 0.350. " + fr(3, 8) + " = 0.375. 37% = 0.370. Compare 350, 370 and 375 thousandths.",
             "0.35, 37%, " + fr(3, 8))
        + ex("Who did better?", "Maya scored 21 out of 25. Owen scored 17 out of 20.",
             fr(21, 25) + " = " + fr(84, 100) + " = 84%. " + fr(17, 20) + " = " + fr(85, 100) + " = 85%.",
             "Owen, with the higher percent")
        + "<h2>Common mistakes</h2>"
        + table(["Mistake", "What to do instead"], [
            ["0.4 = 4%", "0.4 = 0.40 = 40 hundredths = 40%"],
            [fr(3, 5) + " = 0.35", "Divide: " + fr(3, 5) + " = " + fr(6, 10) + " = 0.6"],
            [fr(1, 8) + " &gt; " + fr(1, 6) + " because 8 &gt; 6", "More parts means smaller parts: " + fr(1, 8) + " &lt; " + fr(1, 6)],
            ["0.305 &gt; 0.35 because it has more digits", "Use 3 places: 0.305 &lt; 0.350"],
            [fr(6, 8) + " = " + fr(3, 8), "Divide the top <b>and</b> bottom: " + fr(6, 8) + " = " + fr(3, 4)],
            [fr(11, 4) + " = 2.3", "The remainder is quarters: " + mixed(2, 3, 4) + " = 2.75"],
        ])
    )


FAQ = [
    {"q": "What do Grade 6 students learn about fractions, decimals and percents in Ontario?",
     "a": "In the Ontario Grade 6 math curriculum, students read, represent, compare and order fractions, decimals to thousandths and whole-number percents, and explain how they are equivalent, for example 3/4 = 0.75 = 75%."},
    {"q": "How do you change a fraction to a decimal?",
     "a": "Divide the numerator by the denominator: 3/8 = 3 ÷ 8 = 0.375. If the denominator goes into 10, 100 or 1000, make an equivalent fraction instead: 7/20 = 35/100 = 0.35."},
    {"q": "How do you compare fractions, decimals and percents?",
     "a": "Change them all into decimals with the same number of decimal places, then compare. For 0.35, 3/8 and 37%: 0.350, 0.375 and 0.370, so the order is 0.35, 37%, 3/8."},
    {"q": "Are fractions, decimals and percents on the Grade 6 EQAO math assessment?",
     "a": "Yes. The Grade 6 EQAO math assessment is based on the Ontario curriculum, and Number, including fractions, decimals and percents, is one of the strands it covers."},
]


def mark_large(u, pattern):
    """Tag pictures that must print larger (hundred grids, number lines, fraction bars)."""
    rx = re.compile(r"<svg (?=[^>]*aria-label='" + pattern + ")")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u


def gen():
    rnd = random.Random(36801)
    P = People(rnd)
    sets = [set_equivalent(), set_fraction_decimal(), set_percent(), set_compare(), set_problems(P)]
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
        "country": "ca-on", "subject": "math", "grade": "grade-6", "slug": "fractions-decimals-and-percents", "sort": 1,
        "updated": UPDATED, "pdf_url": "",
        "title": "Fractions, Decimals and Percents",
        "seo_title": "Grade 6 Fractions, Decimals and Percents Worksheets (Ontario Math): Free with Answer Key",
        "short_title": "Fractions, decimals and percents",
        "domain": "Number",
        "standard_code": "Grade 6: Number, B1",
        "standard_url": "https://www.dcp.edu.gov.on.ca/en/curriculum/elementary-mathematics",
        "standard_text": "Read, represent, compare, and order fractions, decimals up to thousandths, and whole-number percents, and describe the equivalences among them",
        "meta_desc": "Free Grade 6 fractions, decimals and percents worksheets for the Ontario curriculum: equivalent fractions and simplest form, mixed numbers, 3/8 = 0.375, decimals to percents, ordering mixed forms and word problems. 100 math questions with an answer key for EQAO practice.",
        "key_big": "A fraction is a division: 3/8 = 3 ÷ 8 = 0.375. Percent means out of 100: 0.4 = 40%.",
        "key_sub": "Know the key facts: 1/2 = 0.5 = 50%, 1/4 = 0.25 = 25%, 3/4 = 0.75 = 75%, 1/5 = 0.2 = 20%. To compare, change everything into decimals with the same number of places.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }
    return mark_large(u, "(hundred grid|number line|two fraction bars|fraction bar)")


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
