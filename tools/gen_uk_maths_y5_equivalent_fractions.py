# -*- coding: utf-8 -*-
"""
UK Year 5 Maths: Equivalent fractions and mixed numbers
(National Curriculum in England, Year 5: Fractions (including decimals and percentages))
  python3 tools/gen_uk_maths_y5_equivalent_fractions.py
Equivalent fractions with diagrams (bars, fraction wall, hundred square for tenths and
hundredths), missing numerators and denominators, improper fractions and mixed numbers
(bars, number lines, statements > 1), comparing and ordering fractions whose denominators
are multiples of the same number, and word problems.
Every choice carries its value; a wrong choice never equals the right value or another wrong one.
Every comparison and order is checked in code with exact fractions.
HTML attributes use single quotes (no backslashes in the JSON). British English.
"""
import json, math, os, random, re, itertools
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "uk", "maths", "year-5")
SLUG = "equivalent-fractions-and-mixed-numbers"
UPDATED = "2026-11-02"
FILL = "#4fae74"
RED = "#c0392b"
BLUE = "#2f6db5"
LINE = "#2b2b2b"
THIN = "#8a8a8a"
SYM = {"<": "&lt;", ">": "&gt;", "=": "="}
CANT = "You can’t tell"
SAME = "They are equal"
WORD = {2: "halves", 3: "thirds", 4: "quarters", 5: "fifths", 6: "sixths", 7: "sevenths", 8: "eighths",
        9: "ninths", 10: "tenths", 12: "twelfths", 15: "fifteenths", 16: "sixteenths", 20: "twentieths",
        24: "twenty-fourths", 100: "hundredths"}
ONE = {2: "half", 3: "third", 4: "quarter", 5: "fifth", 6: "sixth", 7: "seventh", 8: "eighth", 9: "ninth",
       10: "tenth", 12: "twelfth", 15: "fifteenth", 16: "sixteenth", 20: "twentieth", 100: "hundredth"}


# ------------------------------------------------------------ numbers
def fr(a, b):
    return "<span class='fr'><span class='fn'>%s</span><span class='fd'>%s</span></span>" % (a, b)


def frq(b):
    return fr("<b>?</b>", b)


def frq_d(a):
    return fr(a, "<b>?</b>")


def mx(w, n, d):
    if n == 0:
        return str(w)
    if w == 0:
        return fr(n, d)
    return "%d %s" % (w, fr(n, d))


def Fc(a, b, unit=""):
    return (fr(a, b) + unit, F(a, b))


def Mc(w, n, d, unit=""):
    return (mx(w, n, d) + unit, F(w) + F(n, d))


def Nc(n, unit="", pre=""):
    return ("%s%s%s" % (pre, "{:,}".format(n), unit), F(n))


def lcm(a, b):
    return a * b // math.gcd(a, b)


def lcd(vs):
    L = 1
    for v in vs:
        L = lcm(L, v.denominator)
    return L


def show(v):
    if v.denominator == 1:
        return str(v.numerator)
    return fr(v.numerator, v.denominator)


def over(v, L):
    return fr((v * L).numerator, L)


def eqL(v, L):
    """'2/3 = 8/12', or just '7/12' when it already has the denominator L."""
    if v.denominator == L:
        return show(v)
    return "%s = %s" % (show(v), over(v, L))


def parts(n, d):
    """'3 quarters', '1 quarter'."""
    return "%d %s" % (n, ONE[d] if n == 1 else WORD[d])


# ------------------------------------------------------------ helpers
class Spots:
    """Where the right answer goes: A-D used equally often, in a shuffled order."""
    def __init__(self):
        self.left = []

    def next(self, rnd):
        if not self.left:
            self.left = [0, 1, 2, 3]
            rnd.shuffle(self.left)
        return self.left.pop()


SPOTS = Spots()


def mcq(q, correct, cands, e, rnd):
    """correct and cands are (html, value) pairs (value may be None for words)."""
    if not isinstance(correct, tuple):
        correct = (correct, None)
    cs, cv = correct
    seen, vals, pick = {cs}, set(), []
    if cv is not None:
        vals.add(cv)
    for c in cands:
        if c is None:
            continue
        if not isinstance(c, tuple):
            c = (c, None)
        s, v = c
        if s in seen or not s:
            continue
        if v is not None and (v <= 0 or v in vals):
            continue
        seen.add(s)
        if v is not None:
            vals.add(v)
        pick.append(s)
        if len(pick) == 3:
            break
    assert len(pick) == 3, (q, cs, cands)
    rnd.shuffle(pick)
    pos = SPOTS.next(rnd)
    ch = pick[:pos] + [cs] + pick[pos:]
    return {"q": q, "c": ch, "a": ch.index(cs), "e": e}


def fig(svg):
    return "<div class='qfig'>" + svg + "</div>"


def svg_wrap(w, h, body, label):
    w, h = int(math.ceil(w)), int(math.ceil(h))
    return ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 %d %d' width='%d' height='%d' "
            "role='img' aria-label='%s'>%s</svg>" % (w, h, w, h, label, body))


def table(head, rows):
    h = "".join("<th>%s</th>" % x for x in head)
    b = "".join("<tr>" + "".join("<td>%s</td>" % c for c in r) + "</tr>" for r in rows)
    return "<div class='sn-tw'><table class='sn-table'><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>" % (h, b)


def ex(title, q, s, a):
    return ("<div class='sn-ex'><span class='sn-ex-t'>%s</span><p class='sn-ex-q'>%s</p>"
            "<p class='sn-ex-s'>%s</p><p class='sn-ex-a'>Answer: %s</p></div>" % (title, q, s, a))


def mark_large(u, pattern):
    """Tag pictures that must print larger so their labels stay readable."""
    rx = re.compile(r"<svg (?=[^>]*aria-label='" + pattern + ")")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u


# ------------------------------------------------------------ pictures
def sfr(x, y, a, b, size=14, color=LINE):
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
                 % (x0 + i * W / n, y, W / n, H, FILL if i < k else "#fff", LINE))
    return "".join(s)


def two_bars_svg(n1, k1, n2, k2, W=260, H=40):
    s = bar_row(6, 6, W, H, n1, k1) + bar_row(6, 6 + H + 14, W, H, n2, k2)
    return svg_wrap(W + 12, 2 * H + 26, s, "two bars of the same size, top bar %d of %d parts shaded, bottom bar %d of %d parts shaded"
                    % (k1, n1, k2, n2))


def group_bar(x0, y, W, H, n, k, g):
    """Bar of n thin parts, first k shaded, a thick line after every g parts."""
    s = []
    for i in range(n):
        s.append("<rect x='%.1f' y='%.1f' width='%.2f' height='%d' fill='%s' stroke='none'/>"
                 % (x0 + i * W / n, y, W / n, H, FILL if i < k else "#fff"))
    for i in range(1, n):
        xx = x0 + i * W / n
        thick = (i % g == 0)
        s.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='%s'%s/>"
                 % (xx, y, xx, y + H, LINE if thick else THIN, "3" if thick else "1.5",
                    "" if thick else " stroke-dasharray='4 3'"))
    s.append("<rect x='%.1f' y='%.1f' width='%.1f' height='%d' fill='none' stroke='%s' stroke-width='3'/>" % (x0, y, W, H, LINE))
    return "".join(s)


def group_bar_svg(n, k, g, W=280, H=40):
    return svg_wrap(W + 12, H + 12, group_bar(6, 6, W, H, n, k, g),
                    "fraction bar of %d equal parts with %d shaded, thick lines around groups of %d" % (n, k, g))


def wall_svg(dens, shade=None, W=336, H=40):
    """Fraction wall: a row for 1 whole, then one row per denominator, every cell labelled."""
    s = []
    x0 = 6
    for r, d in enumerate([1] + list(dens)):
        y = 6 + r * H
        k = shade[1] if shade and shade[0] == d else 0
        s.append(bar_row(x0, y, W, H, d, k))
        for i in range(d):
            cx = x0 + (i + 0.5) * W / d
            if d == 1:
                s.append("<text x='%.1f' y='%.1f' font-size='16' font-weight='700' fill='%s' text-anchor='middle'>1</text>"
                         % (cx, y + 26, LINE))
            else:
                s.append(sfr(cx, y + 16, 1, d, 14))
    lab = "fraction wall with rows for 1 whole and %s" % ", ".join(WORD[d] for d in dens)
    if shade:
        lab += ", %d %s shaded" % (shade[1], WORD[shade[0]] if shade[1] > 1 else ONE[shade[0]])
    return svg_wrap(W + 12, (len(dens) + 1) * H + 12, "".join(s), lab)


def grid_svg(k, cell=14):
    """Hundred square: 10 columns of 10; the first k small squares shaded, column by column."""
    s = []
    x0 = y0 = 4
    for i in range(100):
        c, r = divmod(i, 10)
        s.append("<rect x='%d' y='%d' width='%d' height='%d' fill='%s' stroke='%s' stroke-width='1'/>"
                 % (x0 + c * cell, y0 + r * cell, cell, cell, FILL if i < k else "#fff", THIN))
    for c in range(11):
        s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='%s'/>"
                 % (x0 + c * cell, y0, x0 + c * cell, y0 + 10 * cell, LINE, "2.5" if c in (0, 10) else "1.6"))
    for r in (0, 10):
        s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='2.5'/>"
                 % (x0, y0 + r * cell, x0 + 10 * cell, y0 + r * cell, LINE))
    return svg_wrap(10 * cell + 8, 10 * cell + 8, "".join(s),
                    "hundred square of 10 columns, %d small squares shaded" % k)


def wholes_svg(d, N, cell=30, H=40, gap=14):
    """N parts of 1/d shaded across bars of d parts, side by side."""
    nb = -(-N // d)
    bw = cell * d
    s = []
    for b in range(nb):
        x0 = 6 + b * (bw + gap)
        k = min(d, N - b * d)
        s.append(bar_row(x0, 6, bw, H, d, k))
        s.append("<rect x='%.1f' y='6' width='%.1f' height='%d' fill='none' stroke='%s' stroke-width='3'/>" % (x0, bw, H, LINE))
    return svg_wrap(12 + nb * bw + (nb - 1) * gap, H + 12, "".join(s),
                    "bars of %d equal parts, %d bars, %d parts shaded" % (d, nb, N))


def tick_line(L, d, Y, x0, x1):
    s = ["<line x1='%.1f' y1='%d' x2='%.1f' y2='%d' stroke='%s' stroke-width='2.5'/>" % (x0, Y, x1, Y, LINE)]
    n = L * d
    for i in range(n + 1):
        X = x0 + (x1 - x0) * i / n
        whole = (i % d == 0)
        s.append("<line x1='%.1f' y1='%d' x2='%.1f' y2='%d' stroke='%s' stroke-width='%s'/>"
                 % (X, Y - (11 if whole else 7), X, Y + (11 if whole else 7), LINE, "2.5" if whole else "1.6"))
        if whole:
            s.append("<text x='%.1f' y='%d' font-size='16' font-weight='700' fill='%s' text-anchor='middle'>%d</text>"
                     % (X, Y + 30, LINE, i // d))
    return "".join(s)


def arrow_line_svg(L, d, t, W=380):
    """Number line 0..L in steps of 1/d with a blue arrow pointing at t."""
    x0, x1 = 16, W - 16
    Y = 40
    X = x0 + (x1 - x0) * float(t) / L
    s = [tick_line(L, d, Y, x0, x1),
         "<line x1='%.1f' y1='6' x2='%.1f' y2='%d' stroke='%s' stroke-width='3'/>" % (X, X, Y - 18, BLUE),
         "<path d='M%.1f %d L%.1f %d L%.1f %d Z' fill='%s'/>" % (X - 7, Y - 20, X + 7, Y - 20, X, Y - 9, BLUE)]
    return svg_wrap(W, Y + 38, "".join(s),
                    "number line from 0 to %d with each whole split into %d equal parts and an arrow" % (L, d))


def letters_line_svg(L, d, pts, W=380):
    """Number line 0..L in steps of 1/d with letters A-D above the points pts (sorted)."""
    x0, x1 = 16, W - 16
    Y = 44
    s = [tick_line(L, d, Y, x0, x1)]
    for i, v in enumerate(pts):
        X = x0 + (x1 - x0) * float(v) / L
        s.append("<path d='M%.1f %d L%.1f %d L%.1f %d Z' fill='%s'/>" % (X - 6, Y - 18, X + 6, Y - 18, X, Y - 9, BLUE))
        s.append("<text x='%.1f' y='%d' font-size='17' font-weight='700' fill='%s' text-anchor='middle'>%s</text>"
                 % (X, Y - 22, BLUE, "ABCD"[i]))
    return svg_wrap(W, Y + 38, "".join(s),
                    "number line from 0 to %d with each whole split into %d equal parts and letters A, B, C and D marked" % (L, d))


# ============================================================ set 1: equivalent fractions with diagrams
def set_diagrams(rnd):
    SPOTS.left = []
    its = []
    for a, b, d in [(1, 3, 6), (3, 4, 8), (2, 5, 10), (2, 3, 12), (3, 4, 12)]:
        n = d // b
        c = a * n
        q = (fig(two_bars_svg(b, a, d, c)) + "The bars are the same size and show the same amount.<br>%s = %s"
             % (fr(a, b), frq(d)))
        e = ("The bottom bar has %d equal parts, so each %s of the top bar is split into %d parts. "
             "%s become%s %d × %d = <b>%d</b> %s. So %s = %s."
             % (d, ONE[b], n, parts(a, b), "s" if a == 1 else "", a, n, c, WORD[d], fr(a, b), fr(c, d)))
        its.append(mcq(q, Nc(c), [Nc(a + (d - b)), Nc(a), Nc(d - c), Nc(c + 1), Nc(n)], e, rnd))

    for dens, (sd, k), t in [((3, 6, 12), (3, 2), 12), ((4, 8), (4, 3), 8), ((5, 10), (5, 3), 10), ((3, 6, 12), (6, 5), 12)]:
        n = t // sd
        c = k * n
        q = (fig(wall_svg(dens, (sd, k))) + "Use the fraction wall. %s is shaded. How many %s are equal to %s?"
             % (fr(k, sd), WORD[t], fr(k, sd)))
        e = ("Look down the fraction wall. Each %s is the same as %d %s, so %s line up with %d × %d = <b>%d</b> %s. "
             "So %s = %s." % (ONE[sd], n, WORD[t], parts(k, sd), k, n, c, WORD[t], fr(k, sd), fr(c, t)))
        its.append(mcq(q, Nc(c), [Nc(k + (t - sd)), Nc(k), Nc(t - c), Nc(c + n)], e, rnd))

    # hundred square: tenths and hundredths
    k = 3
    its.append(mcq(fig(grid_svg(30)) + "Each column is %s of the square. 3 columns are shaded.<br>%s = %s"
                   % (fr(1, 10), fr(3, 10), frq(100)), Nc(30), [Nc(3), Nc(97), Nc(13), Nc(300)],
                   "Each column has 10 small squares, so each tenth = 10 hundredths. 3 tenths = 3 × 10 = <b>30</b> hundredths. "
                   "So %s = %s." % (fr(3, 10), fr(30, 100)), rnd))
    its.append(mcq(fig(grid_svg(70)) + "70 small squares are shaded.<br>%s = %s" % (fr(70, 100), frq(10)),
                   Nc(7), [Nc(70), Nc(700), Nc(10)],
                   "70 hundredths fill 7 whole columns. Each column is a tenth, so %s = <b>%s</b>. "
                   "(Divide 70 and 100 by 10.)" % (fr(70, 100), fr(7, 10)), rnd))
    its.append(mcq(fig(grid_svg(90)) + "Which fraction is equal to the shaded part?", Fc(90, 100),
                   [Fc(9, 100), Fc(10, 100), Fc(90, 10)],
                   "90 of the 100 small squares are shaded: %s. That is 9 full columns, so it is also %s. "
                   "<b>%s</b> is the answer. %s is only 9 small squares, and %s is the part that is not shaded."
                   % (fr(90, 100), fr(9, 10), fr(90, 100), fr(9, 100), fr(10, 100)), rnd))
    its.append(mcq(fig(grid_svg(50)) + "What fraction of the square is shaded?", Fc(1, 2),
                   [Fc(1, 50), Fc(5, 100), Fc(50, 10), Fc(1, 5)],
                   "50 of 100 squares = %s = %s. Half of the square is shaded, so %s = <b>%s</b>."
                   % (fr(50, 100), fr(5, 10), fr(50, 100), fr(1, 2)), rnd))
    its.append(mcq(fig(grid_svg(40)) + "%s is shaded. Which fraction is <b>not</b> equal to the shaded part?" % fr(40, 100),
                   fr(4, 100), [fr(4, 10), fr(2, 5), fr(20, 50)],
                   "4 columns are shaded: %s = %s = %s = %s (2 columns out of every 5). "
                   "<b>%s</b> would be only 4 small squares." % (fr(40, 100), fr(4, 10), fr(20, 50), fr(2, 5), fr(4, 100)), rnd))

    for n, k, g in [(12, 9, 3), (10, 4, 2), (8, 6, 2), (15, 10, 5), (12, 8, 4), (16, 12, 4)]:
        sn, sd = k // g, n // g
        q = (fig(group_bar_svg(n, k, g)) + "%s of the bar is shaded. The thick lines make groups of %d. "
             "Which equal fraction does the bar show?" % (fr(k, n), g))
        e = ("There are %d groups and %d of them are shaded, so %s = <b>%s</b>. "
             "This is the same as dividing %d and %d by %d." % (sd, sn, fr(k, n), fr(sn, sd), k, n, g))
        cands = [Fc(sn, n), Fc(k - g, n - g), Fc(sd, sn), Fc(k, sd), Fc(sn + 1, sd)]
        its.append(mcq(q, Fc(sn, sd), cands, e, rnd))
    assert len(its) == 20, len(its)
    return {"title": "Equivalent fractions with diagrams, including tenths and hundredths", "items": its}


# ============================================================ set 2: missing numbers
def set_missing(rnd):
    SPOTS.left = []
    its = []
    for a, b, d in [(2, 3, 12), (3, 5, 20), (5, 8, 24), (4, 7, 28), (5, 6, 30), (7, 10, 100), (1, 4, 100), (2, 5, 100)]:
        n = d // b
        c = a * n
        e = ("Look at the denominators: %d × <b>%d</b> = %d. Multiply the numerator by %d too: %d × %d = <b>%d</b>. "
             "So %s = %s." % (b, n, d, n, a, n, c, fr(a, b), fr(c, d)))
        its.append(mcq("%s = %s" % (fr(a, b), frq(d)), Nc(c), [Nc(a + (d - b)), Nc(a), Nc(n), Nc(d - c), Nc(c + n)], e, rnd))

    for a, b, c in [(3, 4, 15), (2, 5, 8), (5, 6, 25), (7, 9, 21)]:
        n = c // a
        d = b * n
        assert n * a == c
        e = ("Look at the numerators: %d × <b>%d</b> = %d. Multiply the denominator by %d too: %d × %d = <b>%d</b>. "
             "So %s = %s." % (a, n, c, n, b, n, d, fr(a, b), fr(c, d)))
        its.append(mcq("%s = %s" % (fr(a, b), frq_d(c)), Nc(d), [Nc(b + (c - a)), Nc(b), Nc(b * c), Nc(n)], e, rnd))

    its.append(mcq("%s = %s" % (fr(18, 24), frq(4)), Nc(3), [Nc(6), Nc(9), Nc(4)],
                   "24 ÷ <b>6</b> = 4, so divide the numerator by 6 too: 18 ÷ 6 = <b>3</b>. So %s = %s."
                   % (fr(18, 24), fr(3, 4)), rnd))
    its.append(mcq("%s = %s" % (fr(40, 100), frq(10)), Nc(4), [Nc(40), Nc(400), Nc(10)],
                   "100 ÷ <b>10</b> = 10, so divide the numerator by 10 too: 40 ÷ 10 = <b>4</b>. So %s = %s."
                   % (fr(40, 100), fr(4, 10)), rnd))
    its.append(mcq("%s = %s" % (fr(15, 20), frq_d(3)), Nc(4), [Nc(8), Nc(5), Nc(100)],
                   "15 ÷ <b>5</b> = 3, so divide the denominator by 5 too: 20 ÷ 5 = <b>4</b>. So %s = %s. "
                   "Taking 12 from both (to get %s) changes the value." % (fr(15, 20), fr(3, 4), fr(3, 8)), rnd))

    for a, b, n in [(3, 5, 4), (4, 9, 2), (7, 10, 10)]:
        e = ("Multiply the numerator <b>and</b> the denominator by the same number: %d × %d = %d and %d × %d = %d. "
             "So %s = <b>%s</b>. Multiplying only one number changes the value."
             % (a, n, a * n, b, n, b * n, fr(a, b), fr(a * n, b * n)))
        its.append(mcq("Which fraction is equal to %s?" % fr(a, b), Fc(a * n, b * n),
                       [Fc(a * n, b), Fc(a, b * n), Fc(a + n, b + n), Fc(b, a)], e, rnd))

    for (a, b), trues, bad, why in [
        ((2, 3), [(4, 6), (6, 9), (10, 15)], (4, 5), "2 was added to the numerator and the denominator of %s" % fr(2, 3)),
        ((3, 4), [(6, 8), (9, 12), (75, 100)], (5, 6), "2 was added to the numerator and the denominator of %s" % fr(3, 4)),
    ]:
        for t in trues:
            assert F(*t) == F(a, b)
        assert F(*bad) != F(a, b)
        e = ("<b>%s</b> is not equal to %s: %s. Adding the same number changes the value. "
             "The others are equivalent, because both numbers were multiplied by the same number."
             % (fr(*bad), fr(a, b), why))
        its.append(mcq("Which fraction is <b>not</b> equivalent to %s?" % fr(a, b), fr(*bad),
                       [fr(*t) for t in trues], e, rnd))
    assert len(its) == 20, len(its)
    return {"title": "Find the missing numerator or denominator", "items": its}


# ============================================================ set 3: improper fractions and mixed numbers
def imp_cands(n, d):
    q, r = divmod(n, d)
    return [Mc(r, q, d) if q < d else None, Mc(q, r, n), Mc(q + 1, r, d), Mc(q, d - r, d), Mc(q - 1, r, d), Fc(d, n)]


def imp_e(n, d):
    q, r = divmod(n, d)
    return ("How many %ds go into %d? %d × %d = %d, so there are %d wholes. %d − %d = %d %s left over. So %s = <b>%s</b>."
            % (d, n, q, d, q * d, q, n, q * d, r, "is" if r == 1 else "are", fr(n, d), mx(q, r, d)))


def mix_e(w, n, d):
    return ("Each whole is %s, so %d whole%s %d × %d = %d %s. Add the %d: %d + %d = %d. So %s = <b>%s</b>."
            % (fr(d, d), w, " is" if w == 1 else "s are", w, d, w * d, WORD[d], n, w * d, n, w * d + n, mx(w, n, d), fr(w * d + n, d)))


def mix_cands(w, n, d):
    return [Fc(w * n, d), Fc(10 * w + n, d), Fc(w + n, d), Fc(w * d + n, w * d), Fc(w * d, d + n), Fc(w * d + n + 1, d)]


def nl_item(t, L, d, cands, rnd):
    pos = SPOTS.next(rnd)
    lo = sorted([c for c in cands if c < t], reverse=True)
    hi = sorted([c for c in cands if c > t])
    pts = sorted(lo[:pos] + [t] + hi[:3 - pos])
    assert len(pts) == 4 and len(set(pts)) == 4, (t, pts)
    for v in pts:
        assert (v * d).denominator == 1 and 0 < v < L
    letter = "ABCD"[pts.index(t)]
    w = int(t)
    r = int((t - w) * d)
    e = ("Each whole is split into %d equal parts, so each mark is %s. %s = %s: go to %d, then %d more mark%s. "
         "That is letter <b>%s</b>." % (d, fr(1, d), fr(t.numerator, d), mx(w, r, d), w, r, "" if r == 1 else "s", letter))
    q = fig(letters_line_svg(L, d, pts)) + "Which letter shows %s?" % fr(t.numerator, d)
    return {"q": q, "c": ["A", "B", "C", "D"], "a": pts.index(t), "e": e}


def set_mixed(rnd):
    SPOTS.left = []
    its = []
    for d, N in [(4, 11), (3, 8)]:
        q, r = divmod(N, d)
        e = ("Each bar is 1 whole. %d bars are full and %d more %s shaded in the last bar. So %s = <b>%s</b>."
             % (q, r, "part is" if r == 1 else "parts are", fr(N, d), mx(q, r, d)))
        its.append(mcq(fig(wholes_svg(d, N)) + "Each bar is 1 whole. %s are shaded. Write this as a mixed number." % fr(N, d),
                       Mc(q, r, d), [Fc(N, d * (q + 1))] + imp_cands(N, d), e, rnd))

    for t, L, d in [(F(7, 4), 3, 4), (F(13, 5), 3, 5)]:
        cands = [t - 1, t + 1, t + F(1, d), t - F(1, d), t + F(2, d), t - F(2, d), t - F(3, d)]
        cands = [c for c in cands if 0 < c < L]
        its.append(nl_item(t, L, d, cands, rnd))

    for t, L, d in [(F(8, 3), 3, 3), (F(11, 6), 2, 6), (F(9, 4), 3, 4)]:
        w = int(t)
        r = int((t - w) * d)
        e = ("Each whole is split into %d equal parts, so each mark is %s. The arrow is %d mark%s after %d. "
             "So it shows <b>%s</b> (= %s)." % (d, fr(1, d), r, "" if r == 1 else "s", w, mx(w, r, d), fr(t.numerator, d)))
        its.append(mcq(fig(arrow_line_svg(L, d, t)) + "What number does the arrow show? Give a mixed number.",
                       Mc(w, r, d), [Mc(w, r, d * L), Mc(w + 1, r, d), Mc(w, d - r, d), Mc(w, r + 1, d), Fc(r, d)], e, rnd))

    for n, d in [(13, 5), (17, 4), (19, 6), (23, 10), (29, 8), (22, 7)]:
        q, r = divmod(n, d)
        its.append(mcq("Write %s as a mixed number." % fr(n, d), Mc(q, r, d), imp_cands(n, d), imp_e(n, d), rnd))

    for w, n, d in [(2, 3, 5), (3, 1, 4), (4, 2, 3), (1, 7, 10), (5, 3, 8)]:
        its.append(mcq("Write %s as an improper fraction." % mx(w, n, d), Fc(w * d + n, d), mix_cands(w, n, d),
                       mix_e(w, n, d), rnd))

    its.append(mcq("%s + %s = %s = <b>?</b><br>Write the answer as a mixed number." % (fr(2, 5), fr(4, 5), fr(6, 5)),
                   Mc(1, 1, 5), [Fc(6, 10), Mc(1, 1, 10), Mc(1, 4, 5)],
                   "%s + %s = %s (add the numerators, keep the fifths). %s make 1 whole and 1 fifth is left over. "
                   "So the answer is <b>1 %s</b>." % (fr(2, 5), fr(4, 5), fr(6, 5), fr(5, 5), fr(1, 5)), rnd))
    its.append(mcq("%s + %s + %s = <b>?</b><br>Write the answer as a mixed number." % (fr(3, 4), fr(3, 4), fr(3, 4)),
                   Mc(2, 1, 4), [Fc(9, 12), Mc(2, 3, 4), Mc(3, 1, 4), Mc(1, 1, 4)],
                   "3 + 3 + 3 = 9, so the total is %s. 4 × 2 = 8, so that is 2 wholes and 1 quarter left over: <b>2 %s</b>. "
                   "Do not add the denominators." % (fr(9, 4), fr(1, 4)), rnd))
    assert len(its) == 20, len(its)
    return {"title": "Improper fractions and mixed numbers", "items": its}


# ============================================================ set 4: compare and order
def set_compare(rnd):
    SPOTS.left = []
    its = []

    def which(x, y, bars=False):
        a, b = x
        c, d = y
        X, Y = F(a, b), F(c, d)
        L = lcm(b, d)
        if X == Y:
            right = SAME
        else:
            right = fr(a, b) if X > Y else fr(c, d)
        e = ("%d is a multiple of %d, so use %s: %s and %s. "
             % (L, min(b, d), WORD[L], eqL(X, L) if b != L else fr(a, b), eqL(Y, L) if d != L else fr(c, d)))
        if X == Y:
            e += "The numerators are the same, so <b>they are equal</b>."
        else:
            e += "%d %s %d, so <b>%s</b> is greater." % (max(X, Y) * L, "&gt;", min(X, Y) * L, show(max(X, Y)))
        q = "Which is greater: %s or %s?" % (fr(a, b), fr(c, d))
        if bars:
            q = fig(two_bars_svg(b, a, d, c)) + "The bars are the same size. " + q
        return mcq(q, right, [fr(a, b), fr(c, d), SAME, CANT], e, rnd)

    its.append(which((2, 3), (7, 12), True))
    its.append(which((5, 8), (3, 4), True))
    for x, y in [((3, 5), (7, 10)), ((4, 9), (1, 3)), ((5, 6), (11, 12)), ((3, 4), (6, 8)), ((1, 2), (5, 12)), ((7, 10), (13, 20))]:
        its.append(which(x, y))

    for word, vs in [("greatest", [F(3, 4), F(5, 8), F(11, 16), F(1, 2)]),
                     ("smallest", [F(2, 3), F(5, 6), F(7, 12), F(5, 12)]),
                     ("greatest", [F(3, 5), F(7, 10), F(13, 20), F(2, 5)]),
                     ("smallest", [F(4, 9), F(1, 3), F(5, 18), F(2, 9)])]:
        best = max(vs) if word == "greatest" else min(vs)
        L = lcd(vs)
        e = ("Write them all with the denominator %d: %s. The %s is %s, so the answer is <b>%s</b>."
             % (L, ", ".join(eqL(v, L) for v in vs), word, over(best, L), show(best)))
        its.append(mcq("Which fraction is the %s?" % word, (show(best), best),
                       [(show(v), v) for v in vs if v != best], e, rnd))

    def s_of(seq):
        return ", ".join(show(v) for v in seq)
    for vs, up in [([F(3, 4), F(5, 8), F(1, 2)], True), ([F(2, 3), F(7, 12), F(5, 6)], True),
                   ([F(3, 10), F(1, 5), F(1, 2)], True), ([F(7, 8), F(3, 4), F(13, 16)], False),
                   ([F(5, 9), F(2, 3), F(7, 18)], True), ([F(4, 5), F(17, 20), F(7, 10)], False)]:
        right = sorted(vs, reverse=not up)
        perms = [sorted(vs, key=lambda v: v.numerator), sorted(vs, key=lambda v: v.denominator),
                 sorted(vs, key=lambda v: -v.denominator), list(reversed(right))]
        perms += [list(p) for p in itertools.permutations(vs)]
        L = lcd(vs)
        e = ("Use the denominator %d: %s. So the order is <b>%s</b>."
             % (L, ", ".join(eqL(v, L) for v in vs), s_of(right)))
        its.append(mcq("Order from %s:<br>%s" % ("smallest to largest" if up else "largest to smallest", s_of(vs)),
                       s_of(right), [s_of(p) for p in perms], e, rnd))

    assert F(1, 2) < F(5, 8) < F(3, 4)
    its.append(mcq("Which fraction is between %s and %s?" % (fr(1, 2), fr(3, 4)), Fc(5, 8), [Fc(7, 8), Fc(3, 8), Fc(4, 5)],
                   "In eighths: %s = %s and %s = %s. <b>%s</b> is between them. %s and %s are more than %s, and %s is less than %s."
                   % (fr(1, 2), fr(4, 8), fr(3, 4), fr(6, 8), fr(5, 8), fr(7, 8), fr(4, 5), fr(3, 4), fr(3, 8), fr(1, 2)), rnd))
    assert F(1, 3) < F(5, 12) < F(2, 3) and not F(1, 3) < F(1, 12) < F(2, 3) and F(3, 4) > F(2, 3) and F(5, 6) > F(2, 3)
    its.append(mcq("Which fraction is between %s and %s?" % (fr(1, 3), fr(2, 3)), Fc(5, 12), [Fc(1, 12), Fc(3, 4), Fc(5, 6)],
                   "In twelfths: %s = %s and %s = %s. <b>%s</b> is between them. %s is less than %s, and %s = %s and %s = %s are more than %s."
                   % (fr(1, 3), fr(4, 12), fr(2, 3), fr(8, 12), fr(5, 12), fr(1, 12), fr(1, 3),
                      fr(3, 4), fr(9, 12), fr(5, 6), fr(10, 12), fr(2, 3)), rnd))
    assert len(its) == 20, len(its)
    return {"title": "Compare and order fractions", "items": its}


# ============================================================ set 5: word problems
def set_words(rnd):
    SPOTS.left = []
    its = []
    # 1
    assert F(3, 8) < F(1, 2)
    its.append(mcq("Oliver eats %s of a pizza. Amelia eats %s of a pizza of the same size. Who eats more?" % (fr(3, 8), fr(1, 2)),
                   "Amelia", ["Oliver", "They eat the same", CANT],
                   "Use eighths: %s = %s. 4 eighths is more than 3 eighths, so <b>Amelia</b> eats more."
                   % (fr(1, 2), fr(4, 8)), rnd))
    # 2
    its.append(mcq("A pizza is cut into 8 equal slices. Harry eats %s of it. How many slices does he eat?" % fr(3, 4),
                   Nc(6, " slices"), [Nc(3, " slices"), Nc(7, " slices"), Nc(4, " slices")],
                   "4 × 2 = 8, so %s = %s. Harry eats <b>6 slices</b>." % (fr(3, 4), fr(6, 8)), rnd))
    # 3
    its.append(mcq("Isla has a 1 m ribbon. She cuts off %s m. How many centimetres is that?" % fr(3, 10),
                   Nc(30, " cm"), [Nc(3, " cm"), Nc(70, " cm"), Nc(300, " cm")],
                   "1 m = 100 cm. %s = %s, so she cuts off <b>30 cm</b>." % (fr(3, 10), fr(30, 100)), rnd))
    # 4
    its.append(mcq("In a hundred square, Jack colours 45 squares red. What fraction is red, in tenths and hundredths?",
                   "%s + %s" % (fr(4, 10), fr(5, 100)),
                   ["%s + %s" % (fr(5, 10), fr(4, 100)), "%s + %s" % (fr(4, 100), fr(5, 100)), fr(45, 10)],
                   "45 hundredths = 4 full columns (4 tenths) and 5 more squares (5 hundredths). So %s = <b>%s + %s</b>."
                   % (fr(45, 100), fr(4, 10), fr(5, 100)), rnd))
    # 5
    its.append(mcq("Poppy uses %s of a bag of flour. Arjun uses %s of the same size bag. Who uses more flour?" % (fr(2, 3), fr(5, 6)),
                   "Arjun", ["Poppy", "They use the same", CANT],
                   "Use sixths: %s = %s. 5 sixths is more than 4 sixths, so <b>Arjun</b> uses more." % (fr(2, 3), fr(4, 6)), rnd))
    # 6
    its.append(mcq("Ava runs %s km. Write this distance as a mixed number." % fr(11, 4),
                   Mc(2, 3, 4, " km"), [Mc(3, 2, 4, " km"), Mc(2, 3, 11, " km"), Mc(1, 1, 4, " km"), Mc(3, 3, 4, " km")],
                   "4 × 2 = 8 and 11 − 8 = 3. So %s km = <b>2 %s km</b>." % (fr(11, 4), fr(3, 4)), rnd))
    # 7
    its.append(mcq("Each jug holds %s litre of water. Noah pours out 7 jugs. How much water is that, as a mixed number?" % fr(1, 3),
                   Mc(2, 1, 3, " litres"), [Mc(7, 1, 3, " litres"), Mc(3, 1, 3, " litres"), Mc(2, 2, 3, " litres")],
                   "7 jugs of %s litre = %s litres. 3 thirds make 1 litre, so 6 thirds make 2 litres, with 1 third left over: "
                   "<b>2 %s litres</b>." % (fr(1, 3), fr(7, 3), fr(1, 3)), rnd))
    # 8
    its.append(mcq("Aisha says, “%s is greater than %s, because 8 is greater than 4.” Is she right?" % (fr(1, 8), fr(1, 4)),
                   "No. %s is less than %s" % (fr(1, 8), fr(1, 4)),
                   ["Yes. 8 is greater than 4", "No. They are equal", "Yes. Eighths are bigger than quarters"],
                   "A bigger denominator means the whole is cut into <b>more, smaller</b> parts. %s = %s, which is more than %s. "
                   "So %s is <b>less</b> than %s." % (fr(1, 4), fr(2, 8), fr(1, 8), fr(1, 8), fr(1, 4)), rnd))
    # 9
    its.append(mcq("George says 2 %s = %s. What is the correct improper fraction?" % (fr(3, 5), fr(6, 5)),
                   Fc(13, 5), [Fc(6, 5), Fc(23, 5), Fc(13, 10), Fc(11, 5)],
                   "George multiplied 2 × 3. Instead, 2 wholes = 2 × 5 = 10 fifths. Add 3 fifths: 10 + 3 = 13. So 2 %s = <b>%s</b>."
                   % (fr(3, 5), fr(13, 5)), rnd))
    # 10
    its.append(mcq("Lily changed %s into an equivalent fraction and wrote %s. What did she do wrong?" % (fr(2, 3), fr(4, 5)),
                   "She added 2 to the top and the bottom",
                   ["She multiplied both numbers by 2", "Nothing. She is right", "She multiplied only the numerator by 2"],
                   "2 + 2 = 4 and 3 + 2 = 5. Adding changes the value. Multiply both numbers by 2 instead: %s = <b>%s</b>."
                   % (fr(2, 3), fr(4, 6)), rnd))
    # 11
    rib = [("Leo", F(3, 4)), ("Grace", F(7, 8)), ("Kai", F(5, 8)), ("Zara", F(1, 2))]
    assert max(rib, key=lambda x: x[1])[0] == "Grace"
    its.append(mcq("Four children measure their ribbons. Leo: %s m. Grace: %s m. Kai: %s m. Zara: %s m. "
                   "Who has the longest ribbon?" % (fr(3, 4), fr(7, 8), fr(5, 8), fr(1, 2)),
                   "Grace", ["Leo", "Kai", "Zara"],
                   "Use eighths: %s = %s, %s, %s, %s = %s. The longest is <b>Grace’s</b> ribbon."
                   % (fr(3, 4), fr(6, 8), fr(7, 8), fr(5, 8), fr(1, 2), fr(4, 8)), rnd))
    # 12
    its.append(mcq("A cake is cut into 12 equal slices. Ruby eats 3 slices. What fraction of the cake is that, in its simplest form?",
                   Fc(1, 4), [Fc(1, 3), Fc(9, 12), Fc(1, 12), Fc(1, 9)],
                   "3 out of 12 slices = %s. Divide both numbers by 3: %s = <b>%s</b>." % (fr(3, 12), fr(3, 12), fr(1, 4)), rnd))
    # 13
    its.append(mcq("Mohammed cycles 2 %s km to school. Write this distance as an improper fraction." % fr(1, 4),
                   Fc(9, 4, " km"), [Fc(3, 4, " km"), Fc(21, 4, " km"), Fc(2, 4, " km"), Fc(7, 4, " km")],
                   "2 km = 2 × 4 = 8 quarters. Add 1 quarter: 8 + 1 = 9. So 2 %s km = <b>%s km</b>." % (fr(1, 4), fr(9, 4)), rnd))
    # 14
    its.append(mcq("A bottle holds %s litre of squash. A jug holds %s litre. Which holds more?" % (fr(7, 10), fr(3, 5)),
                   "The bottle", ["The jug", "They hold the same", CANT],
                   "Use tenths: %s = %s. 7 tenths is more than 6 tenths, so <b>the bottle</b> holds more." % (fr(3, 5), fr(6, 10)), rnd))
    # 15
    its.append(mcq("At a party, children eat 19 slices of pizza. Each pizza is cut into 6 equal slices. How many pizzas do they eat?",
                   Mc(3, 1, 6, " pizzas"), [Mc(1, 3, 6, " pizzas"), Mc(3, 1, 19, " pizzas"), Mc(4, 1, 6, " pizzas"), Mc(3, 5, 6, " pizzas")],
                   "6 slices make 1 pizza. 3 × 6 = 18, and 19 − 18 = 1 slice is left. So %s = <b>3 %s pizzas</b>."
                   % (fr(19, 6), fr(1, 6)), rnd))
    # 16
    its.append(mcq("Charlie walks %s km to the park and %s km back home. He writes %s + %s = %s km. "
                   "Write the total as a mixed number." % (fr(5, 6), fr(5, 6), fr(5, 6), fr(5, 6), fr(10, 6)),
                   Mc(1, 4, 6, " km"), [Fc(10, 12, " km"), Mc(1, 5, 6, " km"), Mc(2, 4, 6, " km"), Mc(1, 1, 6, " km")],
                   "6 sixths make 1 km. 10 − 6 = 4 sixths are left over. So %s km = <b>1 %s km</b> (which is also 1 %s km)."
                   % (fr(10, 6), fr(4, 6), fr(2, 3)), rnd))
    # 17
    pens = [("Class 5A", F(3, 4)), ("Class 5B", F(9, 16)), ("Class 5C", F(5, 8))]
    assert sorted(pens, key=lambda x: x[1])[0][0] == "Class 5B"
    its.append(mcq("Three classes each have the same size pot of paint. Class 5A uses %s of theirs, Class 5B uses %s and "
                   "Class 5C uses %s. Which class uses the least paint?" % (fr(3, 4), fr(9, 16), fr(5, 8)),
                   "Class 5B", ["Class 5A", "Class 5C", "They all use the same"],
                   "Use sixteenths: %s = %s, %s, %s = %s. The smallest is %s, so <b>Class 5B</b> uses the least. "
                   "16 is the biggest denominator, but that does not make it the biggest fraction."
                   % (fr(3, 4), fr(12, 16), fr(9, 16), fr(5, 8), fr(10, 16), fr(9, 16)), rnd))
    # 18
    its.append(mcq("Evie has 3 %s bars of chocolate. Each bar has 5 equal pieces. How many pieces does she have?" % fr(2, 5),
                   Nc(17, " pieces"), [Nc(15, " pieces"), Nc(6, " pieces"), Nc(32, " pieces"), Nc(10, " pieces")],
                   "3 whole bars = 3 × 5 = 15 pieces. Add 2 more pieces: 15 + 2 = <b>17 pieces</b>. So 3 %s = %s."
                   % (fr(2, 5), fr(17, 5)), rnd))
    # 19
    its.append(mcq("Alfie scores %s in a spelling test. Maya scores %s. Who did better?" % (fr(7, 10), fr(16, 20)),
                   "Maya", ["Alfie", "They did the same", CANT],
                   "Use twentieths: %s = %s. 16 is more than 14, so <b>Maya</b> did better." % (fr(7, 10), fr(14, 20)), rnd))
    # 20
    its.append(mcq("Ethan has a plank of wood %s m long. He says it is longer than 2 m. Is he right?" % fr(9, 4),
                   "Yes. %s m = 2 %s m" % (fr(9, 4), fr(1, 4)),
                   ["No. %s m = %s m" % (fr(9, 4), fr(4, 9)), "No. It is exactly 2 m", "No. %s m = 1 %s m" % (fr(9, 4), fr(1, 4))],
                   "4 quarters make 1 m, so 8 quarters make 2 m. 9 − 8 = 1 quarter is left over. "
                   "So %s m = <b>2 %s m</b>, which is longer than 2 m." % (fr(9, 4), fr(1, 4)), rnd))
    assert len(its) == 20, len(its)
    return {"title": "Fraction word problems", "items": its}


# ============================================================ lesson
def body_html():
    return (
        "<h2>Equivalent fractions</h2>"
        "<p><b>Equivalent fractions</b> show the same amount. To find one, <b>multiply (or divide) the numerator and the "
        "denominator by the same number</b>. The parts get smaller, but there are more of them.</p>"
        "<figure class='sn-fig'>" + two_bars_svg(4, 3, 12, 9) +
        "<figcaption>The bars are the same size. " + fr(3, 4) + " = " + fr(9, 12) + ": each quarter is split into 3.</figcaption></figure>"
        + ex("Example", fr(3, 4) + " = " + frq(12),
             "4 × 3 = 12, so multiply the numerator by 3 too: 3 × 3 = 9.", fr(9, 12))
        + "<h2>Tenths and hundredths</h2>"
        "<p>In a hundred square, each column is 1 tenth and each small square is 1 hundredth. "
        "So 1 tenth = 10 hundredths.</p>"
        "<figure class='sn-fig'>" + grid_svg(30) +
        "<figcaption>3 columns are shaded: " + fr(3, 10) + " = " + fr(30, 100) + ".</figcaption></figure>"
        + "<h2>Improper fractions and mixed numbers</h2>"
        "<p>An <b>improper fraction</b> such as " + fr(11, 4) + " is greater than 1. "
        "A <b>mixed number</b> such as 2 " + fr(3, 4) + " shows the same amount as wholes and a fraction.</p>"
        "<figure class='sn-fig'>" + wholes_svg(4, 11) +
        "<figcaption>" + fr(11, 4) + " = 2 wholes and 3 more quarters = 2 " + fr(3, 4) + ".</figcaption></figure>"
        + ex("Example", "Write " + fr(17, 5) + " as a mixed number.",
             "5 goes into 17 three times (15), with 2 left over.", "3 " + fr(2, 5))
        + ex("Example", "Write 2 " + fr(3, 5) + " as an improper fraction.",
             "2 wholes = 2 × 5 = 10 fifths. Add 3 fifths: 10 + 3 = 13.", fr(13, 5))
        + "<p>When an answer is more than 1, write it as a mixed number: "
        + fr(2, 5) + " + " + fr(4, 5) + " = " + fr(6, 5) + " = 1 " + fr(1, 5) + ".</p>"
        + "<h2>Comparing and ordering</h2>"
        "<p>When one denominator is a multiple of the other, change one fraction so they have the <b>same denominator</b>. "
        "Then compare the numerators.</p>"
        "<figure class='sn-fig'>" + two_bars_svg(3, 2, 12, 7) +
        "<figcaption>" + fr(2, 3) + " = " + fr(8, 12) + ", which is more than " + fr(7, 12) + ".</figcaption></figure>"
        + ex("Example", "Order " + fr(3, 4) + ", " + fr(5, 8) + " and " + fr(1, 2) + " from smallest to largest.",
             "Use eighths: " + fr(3, 4) + " = " + fr(6, 8) + ", " + fr(5, 8) + ", " + fr(1, 2) + " = " + fr(4, 8) + ".",
             fr(1, 2) + ", " + fr(5, 8) + ", " + fr(3, 4))
        + "<h2>Common mistakes</h2>"
        + table(["Mistake", "What to do instead"], [
            ["Multiplying only the numerator: " + fr(2, 3) + " = " + fr(4, 3),
             "Multiply both: " + fr(2, 3) + " = " + fr(4, 6)],
            ["Adding the same number to the top and bottom: " + fr(2, 3) + " = " + fr(4, 5),
             "Multiply or divide, never add: " + fr(2, 3) + " = " + fr(4, 6)],
            ["2 " + fr(3, 5) + " = " + fr(6, 5) + " or " + fr(23, 5),
             "Wholes × denominator, then add the numerator: 2 × 5 + 3 = 13, so " + fr(13, 5)],
            ["Thinking a bigger denominator means a bigger fraction: " + fr(1, 8) + " &gt; " + fr(1, 4),
             "A bigger denominator means <b>smaller</b> parts: " + fr(1, 8) + " &lt; " + fr(1, 4)],
        ])
    )


FAQ = [
    {"q": "What fractions do Year 5 children learn?",
     "a": "Year 5 pupils find equivalent fractions (including tenths and hundredths), convert between improper fractions and mixed numbers, and compare and order fractions whose denominators are multiples of the same number. They also add and subtract fractions and multiply them by whole numbers."},
    {"q": "How do you teach equivalent fractions in Year 5?",
     "a": "Start with bars, a fraction wall and a hundred square so children see that the amount stays the same. Then show the rule: multiply or divide the numerator and the denominator by the same number, for example 3/4 = 9/12."},
    {"q": "How do you change an improper fraction to a mixed number?",
     "a": "Divide the numerator by the denominator. The answer is the number of wholes and the remainder is the new numerator, so 17/5 = 3 2/5. To go back, multiply the wholes by the denominator and add the numerator: 3 × 5 + 2 = 17."},
    {"q": "How do you compare fractions with different denominators?",
     "a": "If one denominator is a multiple of the other, change one fraction so both have the same denominator, then compare the numerators. For 2/3 and 7/12, 2/3 = 8/12, so 2/3 is greater."},
]


def gen():
    rnd = random.Random(5509)
    SPOTS.left = []
    sets = [set_diagrams(rnd), set_missing(rnd), set_mixed(rnd), set_compare(rnd), set_words(rnd)]
    for s in sets:
        assert len(s["items"]) == 20, (s["title"], len(s["items"]))
        cnt = [0, 0, 0, 0]
        for it in s["items"]:
            assert len(set(it["c"])) == 4, it
            cnt[it["a"]] += 1
        assert cnt == [5, 5, 5, 5], (s["title"], cnt)
    return {
        "country": "uk", "subject": "maths", "grade": "year-5", "slug": SLUG, "sort": 9,
        "updated": UPDATED, "pdf_url": "",
        "title": "Year 5 Equivalent Fractions and Mixed Numbers",
        "seo_title": "Year 5 Equivalent Fractions and Mixed Numbers Worksheets: Improper Fractions, Comparing and Ordering (Free, with Answers)",
        "short_title": "Equivalent fractions and mixed numbers",
        "domain": "Fractions (including decimals and percentages)",
        "standard_code": "Year 5: Fractions (including decimals and percentages)",
        "standard_url": "https://www.gov.uk/government/publications/national-curriculum-in-england-mathematics-programmes-of-study",
        "standard_text": "Compare and order fractions whose denominators are all multiples of the same number; identify, name and write equivalent fractions of a given fraction, represented visually, including tenths and hundredths; recognise mixed numbers and improper fractions and convert from one form to the other and write mathematical statements > 1 as a mixed number [for example, 2/5 + 4/5 = 6/5 = 1 1/5].",
        "meta_desc": "Free Year 5 maths worksheets on equivalent fractions and mixed numbers for the National Curriculum: fraction walls, tenths and hundredths, missing numerators and denominators, improper fractions, comparing and ordering fractions and word problems. 100 questions with an answer key.",
        "key_big": "Equivalent fractions: multiply or divide the top and the bottom by the same number.",
        "key_sub": "3/4 = 9/12 (× 3). 3/10 = 30/100. 11/4 = 2 3/4, because 4 goes into 11 twice with 3 left over.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, SLUG + ".json")
    mark_large(u, "(number line|bars of|fraction bar|two bars|fraction wall)")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(u, f, ensure_ascii=False, indent=1)
    print("wrote", path)
