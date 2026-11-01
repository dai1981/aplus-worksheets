# -*- coding: utf-8 -*-
"""
US Grade 4 Math: Equivalent Fractions (4.NF.A.1)
  python tools/gen_us_math_g4_equivalent_fractions.py
Grade 4 denominators only: 2, 3, 4, 5, 6, 8, 10, 12, 100.
Every wrong fraction choice is checked in code: it must NOT be equal to the right answer.
HTML attributes use single quotes (no backslashes in the JSON).
"""
import json, re, os, random
from fractions import Fraction

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "us", "math", "grade-4")
UPDATED = "2026-11-02"
FILL = "#4fae74"      # shaded part
LINE = "#2b2b2b"
DASH = "#2b2b2b"
RED = "#d6453b"
GIRLS = ["Maya", "Ava", "Mia", "Zoe", "Lily", "Emma", "Nora", "Ruby", "Grace", "Sofia", "Chloe", "Hana"]
BOYS = ["Leo", "Noah", "Eli", "Sam", "Ben", "Omar", "Kai", "Jack", "Luis", "Owen", "Max", "Theo"]
DENS = {2, 3, 4, 5, 6, 8, 10, 12, 100}
WORD = {2: "halves", 3: "thirds", 4: "fourths", 5: "fifths", 6: "sixths", 8: "eighths", 10: "tenths",
        12: "twelfths", 100: "hundredths"}
ONE = {2: "half", 3: "third", 4: "fourth", 5: "fifth", 6: "sixth", 8: "eighth", 10: "tenth", 12: "twelfth"}


# ------------------------------------------------------------ helpers
def fr(a, b):
    return "<span class='fr'><span class='fn'>%d</span><span class='fd'>%d</span></span>" % (a, b)


def frq(b):
    """Fraction with a missing top number."""
    return "<span class='fr'><span class='fn'><b>?</b></span><span class='fd'>%d</span></span>" % b


def frq_d(a):
    """Fraction with a missing bottom number."""
    return "<span class='fr'><span class='fn'>%d</span><span class='fd'><b>?</b></span></span>" % a


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
    correct = str(correct)
    seen = {correct}
    pick = []
    for c in cands:
        if c is None:
            continue
        c = str(c)
        if c in seen or not c or c.startswith("-") or c == "0":
            continue
        seen.add(c)
        pick.append(c)
        if len(pick) == 3:
            break
    assert len(pick) == 3, (q, correct, cands)
    rnd.shuffle(pick)
    pos = SPOTS.next(rnd)
    ch = pick[:pos] + [correct] + pick[pos:]
    return {"q": q, "c": ch, "a": ch.index(correct), "e": e}


def fmcq(q, right, cands, e, rnd):
    """right and cands are (top, bottom). Wrong choices that equal the right value are dropped."""
    v = Fraction(*right)
    keep = []
    for c in cands:
        if c is None or c[0] <= 0 or c[1] <= 0 or Fraction(*c) == v:
            continue
        keep.append(fr(*c))
    return mcq(q, fr(*right), keep, e, rnd)


def nmcq(q, right, cands, e, rnd):
    return mcq(q, str(right), [str(c) for c in cands if c is not None and c > 0 and c != right], e, rnd)


def fig(svg):
    return "<div class='qfig'>" + svg + "</div>"


def svg_wrap(w, h, body, label):
    return ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 %d %d' width='%d' height='%d' "
            "role='img' aria-label='%s'>%s</svg>" % (w, h, w, h, label, body))


def table(head, rows):
    h = "".join("<th>%s</th>" % x for x in head)
    b = "".join("<tr>" + "".join("<td>%s</td>" % c for c in r) + "</tr>" for r in rows)
    return "<div class='sn-tw'><table class='sn-table'><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>" % (h, b)


def ex(title, q, s, a):
    return ("<div class='sn-ex'><span class='sn-ex-t'>%s</span><p class='sn-ex-q'>%s</p>"
            "<p class='sn-ex-s'>%s</p><p class='sn-ex-a'>Answer: %s</p></div>" % (title, q, s, a))


def parts(n):
    return "1 part" if n == 1 else "%d parts" % n


def pieces(n):
    return "1 piece" if n == 1 else "%d pieces" % n


class People:
    def __init__(self, rnd):
        self.pool = [(n, "she", "her") for n in GIRLS] + [(n, "he", "his") for n in BOYS]
        rnd.shuffle(self.pool)
        self.i = 0

    def next(self):
        p = self.pool[self.i % len(self.pool)]
        self.i += 1
        return p


def cap(s):
    return s[0].upper() + s[1:]


# ------------------------------------------------------------ pictures
def sfr(x, y, a, b, size=16, color=LINE):
    """Stacked fraction drawn in SVG, centered at x. y is the numerator baseline."""
    w = size * 0.62 * max(len(str(a)), len(str(b))) + 4
    return ("<text x='%.1f' y='%.1f' font-size='%d' font-weight='700' fill='%s' text-anchor='middle'>%d</text>"
            "<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='1.6'/>"
            "<text x='%.1f' y='%.1f' font-size='%d' font-weight='700' fill='%s' text-anchor='middle'>%d</text>"
            % (x, y, size, color, a, x - w / 2, y + 5, x + w / 2, y + 5, color, x, y + size + 5, size, color, b))


def bar_row(x0, y, W, H, n, k):
    return "".join("<rect x='%.1f' y='%.1f' width='%.2f' height='%d' fill='%s' stroke='%s' stroke-width='2.5'/>"
                   % (x0 + i * W / n, y, W / n, H, FILL if i < k else "#fff", LINE) for i in range(n))


def two_bars_svg(n1, k1, n2, k2, W=260, H=40):
    s = bar_row(6, 6, W, H, n1, k1) + bar_row(6, 6 + H + 14, W, H, n2, k2)
    return svg_wrap(W + 12, 2 * H + 26, s, "two bars of the same size, top bar %d of %d parts shaded, bottom bar %d of %d parts shaded"
                    % (k1, n1, k2, n2))


def area_svg(b, a, n, W=200, H=100):
    """Rectangle cut into b columns, a shaded. n-1 dashed lines across cut every column into n equal pieces."""
    x0 = y0 = 6
    s = [bar_row(x0, y0, W, H, b, a)]
    for j in range(1, n):
        y = y0 + H * j / n
        s.append("<line x1='%d' y1='%.1f' x2='%d' y2='%.1f' stroke='%s' stroke-width='2' stroke-dasharray='7 5'/>"
                 % (x0, y, x0 + W, y, DASH))
    s.append("<rect x='%d' y='%d' width='%d' height='%d' fill='none' stroke='%s' stroke-width='2.5'/>" % (x0, y0, W, H, LINE))
    return svg_wrap(W + 12, H + 12, "".join(s),
                    "rectangle in %d equal columns with %d shaded, cut across by %d dashed %s" % (b, a, n - 1, "line" if n == 2 else "lines"))


def line_svg(b, d, a=None, W=330):
    """Number line 0..1. Long labeled ticks every 1/b, short ticks every 1/d, red dot at a/b."""
    L, R, Y = 22, W - 22, 70
    s = ["<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='2.5'/>" % (L, Y, R, Y, LINE)]
    for i in range(d + 1):
        x = L + (R - L) * i / d
        s.append("<line x1='%.1f' y1='%d' x2='%.1f' y2='%d' stroke='%s' stroke-width='1.8'/>" % (x, Y - 8, x, Y + 8, LINE))
    m = d // b
    for i in range(b + 1):
        x = L + (R - L) * i / b
        s.append("<line x1='%.1f' y1='%d' x2='%.1f' y2='%d' stroke='%s' stroke-width='2.8'/>" % (x, Y - 15, x, Y + 15, LINE))
        if 0 < i < b:
            s.append(sfr(x, 20, i, b, 15))
    for v, x in ((0, L), (1, R)):
        s.append("<text x='%d' y='%d' font-size='17' font-weight='700' fill='%s' text-anchor='middle'>%d</text>" % (x, Y + 36, LINE, v))
    if a is not None:
        s.append("<circle cx='%.1f' cy='%d' r='8' fill='%s'/>" % (L + (R - L) * a / b, Y, RED))
    assert m * b == d
    return svg_wrap(W, Y + 44, "".join(s), "number line from 0 to 1 with %s labeled and small ticks for %s" % (WORD[b], WORD[d]))


def hundred_svg(k, cell=14):
    """10 by 10 grid, the first k columns shaded."""
    o = 6
    s = []
    for c in range(10):
        for r in range(10):
            s.append("<rect x='%d' y='%d' width='%d' height='%d' fill='%s' stroke='#555' stroke-width='1'/>"
                     % (o + c * cell, o + r * cell, cell, cell, FILL if c < k else "#fff"))
    for c in range(1, 10):
        s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='2'/>"
                 % (o + c * cell, o, o + c * cell, o + 10 * cell, LINE))
    s.append("<rect x='%d' y='%d' width='%d' height='%d' fill='none' stroke='%s' stroke-width='2.5'/>" % (o, o, 10 * cell, 10 * cell, LINE))
    return svg_wrap(10 * cell + 2 * o, 10 * cell + 2 * o, "".join(s), "grid of 100 squares in 10 columns, %d columns shaded" % k)


def check_fr(a, b):
    assert b in DENS and 0 < a, (a, b)


# ============================================================ set 1: see it in a model
def set_models(rnd):
    its = []
    for a, b, d in [(1, 2, 4), (1, 3, 6), (3, 4, 8), (2, 5, 10), (1, 4, 12), (2, 3, 12), (5, 6, 12), (1, 2, 8)]:
        n = d // b
        c = a * n
        check_fr(c, d)
        q = (fig(two_bars_svg(b, a, d, c)) + "The bars are the same size and show the same amount.<br>%s = %s"
             % (fr(a, b), frq(d)))
        e = ("The bottom bar has %d equal parts, so each %s of the top bar is cut into %d small parts. "
             "The %s become%s %d × %d = <b>%d</b> shaded small parts, so %s = %s."
             % (d, ONE[b], n, "shaded " + ONE[b] if a == 1 else "%d shaded %s" % (a, WORD[b]), "s" if a == 1 else "",
                a, n, c, fr(a, b), fr(c, d)))
        its.append(nmcq(q, c, [a + (d - b), a, d - c, c + 1, d, c - 1, n], e, rnd))

    for a, b, n in [(1, 2, 3), (2, 3, 2), (3, 4, 2), (1, 3, 4), (3, 5, 2), (1, 4, 3)]:
        check_fr(n * a, n * b)
        q = (fig(area_svg(b, a, n)) + "The rectangle shows %s. The dashed %s cut every part into %d equal pieces. "
             "What fraction is shaded now?" % (fr(a, b), "line" if n == 2 else "lines", n))
        e = ("Now there are %d × %d = <b>%d</b> equal pieces, and %d × %d = <b>%d</b> of them are shaded: %s. "
             "The pieces are smaller, but the shaded amount did not change, so %s = %s."
             % (b, n, n * b, a, n, n * a, fr(n * a, n * b), fr(a, b), fr(n * a, n * b)))
        its.append(fmcq(q, (n * a, n * b), [(a, n * b), (n * a, b), (n * b - n * a, n * b), (a + n, b + n), (n * a, n * b - n * a)],
                        e, rnd))

    SAME, TOP, BOT, CANT = "They are equal", "The top bar has more", "The bottom bar has more", "You can’t tell"
    for b, a, d, c in [(3, 2, 6, 4), (2, 1, 6, 3), (4, 3, 8, 5), (4, 2, 10, 5), (3, 1, 6, 3), (4, 3, 12, 9)]:
        x, y = Fraction(a, b), Fraction(c, d)
        right = SAME if x == y else (TOP if x > y else BOT)
        if x == y:
            e = ("Both bars are shaded up to the same place. The bottom bar has more parts, but each part is smaller, "
                 "so %s = %s." % (fr(a, b), fr(c, d)))
        else:
            eq = Fraction(a, b) * d
            e = ("%s would be %d %s. The bottom bar has %d shaded, so the %s bar has more: %s %s %s. "
                 "More parts does not mean more shaded."
                 % (fr(a, b), eq.numerator, WORD[d], c, "top" if x > y else "bottom",
                    fr(a, b), "&gt;" if x > y else "&lt;", fr(c, d)))
        its.append(mcq(fig(two_bars_svg(b, a, d, c)) + "The bars are the same size. Compare the shaded amounts.",
                       right, [SAME, TOP, BOT, CANT], e, rnd))
    assert len(its) == 20, len(its)
    return {"title": "Equivalent fractions in models", "items": its}


# ============================================================ set 2: multiply top and bottom
def set_multiply(rnd):
    its = []
    for a, b, d in [(1, 3, 12), (2, 5, 10), (3, 4, 12), (5, 6, 12), (1, 2, 10), (1, 4, 8),
                    (4, 5, 10), (2, 3, 6), (1, 6, 12), (1, 2, 12), (3, 5, 10), (3, 4, 100)]:
        n = d // b
        assert n * b == d
        c = a * n
        e = ("%d × <b>%d</b> = %d, so multiply the bottom by %d. Do the same to the top: %d × %d = <b>%d</b>. "
             "So %s = %s." % (b, n, d, n, a, n, c, fr(a, b), fr(c, d)))
        its.append(nmcq("%s = %s" % (fr(a, b), frq(d)), c, [a + (d - b), a, n, d - c, c + n], e, rnd))

    for a, b, c in [(1, 2, 5), (2, 3, 8), (3, 4, 6), (2, 5, 4)]:
        n = c // a
        d = b * n
        assert n * a == c
        e = ("%d × <b>%d</b> = %d, so the top was multiplied by %d. Multiply the bottom by %d too: %d × %d = <b>%d</b>. "
             "So %s = %s." % (a, n, c, n, n, b, n, d, fr(a, b), fr(c, d)))
        its.append(nmcq("%s = %s" % (fr(a, b), frq_d(c)), d, [b + (c - a), b * c, b, d + 1, d - 1], e, rnd))

    for a, b, n in [(3, 4, 3), (2, 5, 2), (1, 6, 2), (5, 10, 10)]:
        e = ("Multiply <b>both</b> numbers by %d: %d × %d = %d and %d × %d = %d. The answer is %s. "
             "Each part is cut into %d, so there are %d times as many parts, each %s as big."
             % (n, a, n, a * n, b, n, b * n, fr(a * n, b * n), n, n, fr(1, n)))
        its.append(fmcq("Multiply the top and bottom of %s by %d. Which fraction do you get?" % (fr(a, b), n),
                        (a * n, b * n), [(a * n, b), (a, b * n), (a + n, b + n), (b * n, a * n)], e, rnd))
    assert len(its) == 20, len(its)
    return {"title": "Multiply the top and bottom by the same number", "items": its}


# ============================================================ set 3: divide, and spot the odd one out
def set_divide(rnd):
    its = []
    for a, b, d in [(6, 8, 4), (8, 12, 3), (4, 10, 5), (9, 12, 4)]:
        g = b // d
        assert g * d == b and a % g == 0
        c = a // g
        e = ("%d ÷ <b>%d</b> = %d, so divide the bottom by %d. Do the same to the top: %d ÷ %d = <b>%d</b>. "
             "So %s = %s." % (b, g, d, g, a, g, c, fr(a, b), fr(c, d)))
        its.append(nmcq("%s = %s" % (fr(a, b), frq(d)), c, [a - (b - d), a, d - c, g, a * g, c + 1], e, rnd))

    for a, b, g in [(10, 12, 2), (4, 12, 4), (6, 10, 2), (75, 100, 25)]:
        e = ("Divide <b>both</b> numbers by %d: %d ÷ %d = %d and %d ÷ %d = %d. So %s = %s. "
             "The parts are bigger, but there are fewer of them." % (g, a, g, a // g, b, g, b // g, fr(a, b), fr(a // g, b // g)))
        its.append(fmcq("Divide the top and bottom of %s by %d. Which fraction do you get?" % (fr(a, b), g),
                        (a // g, b // g), [(a // g, b), (a, b // g), (a - g, b - g), (b // g, a // g)], e, rnd))

    for a, b, n in [(3, 5, 2), (2, 3, 4), (3, 4, 3), (5, 6, 2)]:
        e = ("Multiply the top and bottom by the <b>same</b> number: %d × %d = %d and %d × %d = %d, so %s = %s. "
             "Adding the same number, or multiplying only one number, gives a different amount."
             % (a, n, a * n, b, n, b * n, fr(a, b), fr(a * n, b * n)))
        its.append(fmcq("Which fraction is equal to %s?" % fr(a, b), (a * n, b * n),
                        [(a + 1, b + 1), (a, b * n), (a * (n + 1), b * n), (a * n, b), (b, a)], e, rnd))

    # which fraction is NOT equal?
    for (a, b), trues, bad, why in [
        ((1, 2), [(3, 6), (5, 10), (50, 100)], (2, 3), "1 was added to the top and bottom"),
        ((3, 4), [(6, 8), (9, 12), (75, 100)], (7, 8), "4 was added to the top and bottom"),
        ((1, 4), [(2, 8), (3, 12), (25, 100)], (2, 4), "only the top was multiplied by 2"),
        ((6, 12), [(1, 2), (4, 8), (50, 100)], (3, 12), "only the top was divided by 2"),
    ]:
        for t in trues:
            assert Fraction(*t) == Fraction(a, b) and t[1] in DENS
        assert Fraction(*bad) != Fraction(a, b) and len(trues) == 3
        e = ("%s ≠ %s: %s. The others name the same amount, because the top and bottom were changed by the same number."
             % (fr(*bad), fr(a, b), why))
        ch = [fr(*t) for t in trues]
        its.append(mcq("Which fraction is <b>not</b> equal to %s?" % fr(a, b), fr(*bad), ch, e, rnd))

    def eq_txt(a, b, c, d):
        return "%s = %s" % (fr(a, b), fr(c, d))
    pool = [(2, 3, 4, 6), (2, 5, 4, 10), (3, 4, 6, 8), (1, 3, 4, 12), (5, 6, 10, 12), (1, 2, 6, 12), (3, 10, 30, 100),
            (4, 5, 8, 10), (1, 4, 3, 12), (3, 5, 60, 100), (1, 6, 2, 12), (2, 4, 5, 10)]
    for t in pool:
        assert Fraction(t[0], t[1]) == Fraction(t[2], t[3])
    rnd.shuffle(pool)
    falses = [((1, 3, 2, 4), "1 was added to the top and bottom of %s" % fr(1, 3)),
              ((3, 4, 3, 8), "only the bottom of %s was multiplied by 2" % fr(3, 4)),
              ((4, 6, 2, 4), "2 was taken away from the top and bottom of %s" % fr(4, 6)),
              ((5, 10, 1, 5), "the top and bottom of %s were divided by different numbers" % fr(5, 10))]
    for i, (f, why) in enumerate(falses):
        assert Fraction(f[0], f[1]) != Fraction(f[2], f[3])
        ch = [eq_txt(*t) for t in pool[3 * i:3 * i + 3]]
        e = "%s is false: %s. The others are true, because the same number multiplies the top and bottom." % (eq_txt(*f), why)
        its.append(mcq("Which is <b>not</b> true?", eq_txt(*f), ch, e, rnd))
    assert len(its) == 20, len(its)
    return {"title": "Divide to find equivalent fractions", "items": its}


# ============================================================ set 4: number lines, tenths and hundredths
def set_lines(rnd):
    its = []
    for a, b, d in [(1, 2, 6), (2, 3, 6), (3, 4, 8), (1, 3, 12), (3, 5, 10), (1, 4, 12)]:
        n = d // b
        c = a * n
        e = ("Each %s is split into %d small spaces, so there are %d spaces from 0 to 1. "
             "Count the spaces from 0 to the dot: <b>%d</b>. So %s = %s." % (ONE[b], n, d, c, fr(a, b), fr(c, d)))
        its.append(fmcq(fig(line_svg(b, d, a)) + "The red dot is at %s. Name the same point in %s." % (fr(a, b), WORD[d]),
                        (c, d), [(a, d), (c + 1, d), (a + d - b, d), (c - 1, d), (c + 2, d)], e, rnd))

    for k in [3, 7, 5]:
        e = ("Each column is %s, and each column has 10 small squares. %d columns = %d × 10 = <b>%d</b> squares, so %s = %s."
             % (fr(1, 10), k, k, 10 * k, fr(k, 10), fr(10 * k, 100)))
        its.append(fmcq(fig(hundred_svg(k)) + "The grid has 100 equal squares. What fraction is shaded, in hundredths?",
                        (10 * k, 100), [(k, 100), (k + 90, 100), (100 - 10 * k, 100), (10 * k, 10)], e, rnd))
    for k in [4, 6, 9]:
        e = ("The grid has 10 equal columns, so each column is %s. %d columns are shaded: %s. "
             "That is the same as %s." % (fr(1, 10), k, fr(k, 10), fr(10 * k, 100)))
        its.append(fmcq(fig(hundred_svg(k)) + "What fraction of the grid is shaded, in tenths?",
                        (k, 10), [(10 * k, 10), (k, 100), (10 - k, 10), (k + 1, 10)], e, rnd))

    for a in [7, 2]:
        e = "Tenths to hundredths: multiply the top and bottom by 10. %d × 10 = <b>%d</b>, so %s = %s." % (a, 10 * a, fr(a, 10), fr(10 * a, 100))
        its.append(nmcq("%s = %s" % (fr(a, 10), frq(100)), 10 * a, [a, a + 90, 100 * a, 100 - 10 * a], e, rnd))
    for c in [60, 90]:
        e = ("Hundredths to tenths: divide the top and bottom by 10. %d ÷ 10 = <b>%d</b>, so %s = %s."
             % (c, c // 10, fr(c, 100), fr(c // 10, 10)))
        its.append(nmcq("%s = %s" % (fr(c, 100), frq(10)), c // 10, [c, 10 * c, 10 - c // 10, c // 10 + 1], e, rnd))

    for a, b in [(1, 2), (1, 4), (3, 5), (4, 5)]:
        n = 100 // b
        c = a * n
        e = ("%d × <b>%d</b> = 100, so multiply the top by %d too: %d × %d = <b>%d</b>. So %s = %s."
             % (b, n, n, a, n, c, fr(a, b), fr(c, 100)))
        its.append(nmcq("%s = %s" % (fr(a, b), frq(100)), c, [int("%d%d" % (a, b)), 10 * a, a, a + 100 - b], e, rnd))
    assert len(its) == 20, len(its)
    return {"title": "Number lines, tenths and hundredths", "items": its}


# ============================================================ set 5: word problems and explain why
def set_words(rnd):
    its = []
    P = People(rnd)

    # who ate more?  (same size pizzas)
    for a, b, c, d in [(2, 4, 4, 8), (2, 3, 4, 6), (3, 4, 5, 8), (2, 6, 4, 12)]:
        (n1, _, _), (n2, _, _) = P.next(), P.next()
        q = ("%s ate %s of a pizza. %s ate %s of a pizza of the same size. Who ate more?" % (n1, fr(a, b), n2, fr(c, d)))
        n = d // b
        if Fraction(a, b) == Fraction(c, d):
            right = "They ate the same"
            e = ("Multiply the top and bottom of %s by %d: %s = %s. %s ate more slices, but they were smaller, "
                 "so they ate the same amount." % (fr(a, b), n, fr(a, b), fr(a * n, b * n), n2))
        else:
            right = n1
            e = ("Change %s to %s: multiply the top and bottom by %d to get %s. %s is more than %s, so <b>%s</b> ate more."
                 % (fr(a, b), WORD[d], n, fr(a * n, d), fr(a * n, d), fr(c, d), n1))
        its.append(mcq(q, right, [n1, n2, "They ate the same", "You can’t tell"], e, rnd))

    # measuring cups
    for a, b, d in [(3, 4, 8), (1, 2, 4), (2, 3, 6), (1, 2, 8)]:
        nm, he, his = P.next()
        n = d // b
        c = a * n
        q = ("A recipe needs %s cup of milk. %s only has a %s cup scoop. How many scoops does %s need?"
             % (fr(a, b), nm, fr(1, d), he))
        e = ("%s = %s, because %d × %d = %d and %d × %d = %d. So %s needs <b>%d</b> scoops of %s cup."
             % (fr(a, b), fr(c, d), a, n, c, b, n, d, he, c, fr(1, d)))
        its.append(nmcq(q, c, [a, a + (d - b), d, b, c + 1], e, rnd))

    # money
    nm, he, his = P.next()
    its.append(fmcq("A dime is %s of a dollar. A penny is %s of a dollar. %s has 3 dimes. "
                    "What fraction of a dollar is that, in hundredths?" % (fr(1, 10), fr(1, 100), nm),
                    (30, 100), [(3, 100), (93, 100), (70, 100)],
                    "3 dimes are %s of a dollar. Multiply the top and bottom by 10: %s. That is 30 cents." % (fr(3, 10), fr(30, 100)), rnd))
    nm, he, his = P.next()
    its.append(mcq("%s has 70 pennies, which is %s of a dollar. %s trades them for dimes. How many dimes does %s get?"
                   % (nm, fr(70, 100), cap(he), he), "7 dimes", ["70 dimes", "10 dimes", "3 dimes"],
                   "%s = %s: divide the top and bottom by 10. Each dime is %s of a dollar, so %s gets <b>7 dimes</b>."
                   % (fr(70, 100), fr(7, 10), fr(1, 10), he), rnd))

    # pieces of the same whole
    nm, he, his = P.next()
    its.append(nmcq("A cake is cut into 6 equal pieces, and %s eats 3. A cake of the same size is cut into 12 equal pieces. "
                    "How many of those pieces make the same amount?" % nm, 6, [9, 3, 12, 7],
                    "%s = %s: the 12 pieces are half as big, so you need twice as many. 3 × 2 = <b>6</b> pieces."
                    % (fr(3, 6), fr(6, 12)), rnd))
    nm, he, his = P.next()
    its.append(fmcq("A pizza is cut into 8 equal slices. %s eats 2 slices. Which fraction also names how much %s ate?" % (nm, he),
                    (1, 4), [(2, 4), (1, 8), (6, 8), (1, 6)],
                    "%s ate %s. Divide the top and bottom by 2: %s. Two eighths fill one fourth." % (he.capitalize(), fr(2, 8), fr(1, 4)), rnd))
    (n1, h1, _), (n2, h2, _) = P.next(), P.next()
    its.append(nmcq("%s cuts a ribbon into 4 equal pieces and uses 3 of them. %s cuts a ribbon of the same length into "
                    "8 equal pieces. How many pieces must %s use to use the same length?" % (n1, n2, h2), 6, [7, 3, 8, 4],
                    "%s = %s. Each eighth is half of a fourth, so %s needs 3 × 2 = <b>6</b> pieces." % (fr(3, 4), fr(6, 8), h2), rnd))
    nm, he, his = P.next()
    its.append(fmcq("A pan of brownies is cut into 12 equal pieces. %s eats 4 of them. What fraction of the pan is that, in thirds?" % nm,
                    (1, 3), [(4, 3), (1, 12), (1, 4), (4, 12)],
                    "%s = %s: divide the top and bottom by 4 (12 ÷ 4 = 3). Four twelfths fill one third." % (fr(4, 12), fr(1, 3)), rnd))

    # explain why
    its.append(mcq(fig(two_bars_svg(3, 2, 6, 4)) + "Why is %s equal to %s?" % (fr(2, 3), fr(4, 6)),
                   "Each third is cut into 2 equal parts",
                   ["2 was added to the top and bottom", "%s has more parts, so it is more" % fr(4, 6), "Sixths are bigger than thirds"],
                   "Cut each third in half: 2 shaded thirds become 4 shaded sixths. There are twice as many parts, "
                   "each half as big, so the amount stays the same.", rnd))
    its.append(mcq("You change %s into %s. What happens to the parts?" % (fr(3, 4), fr(9, 12)),
                   "3 times as many, each " + fr(1, 3) + " as big",
                   ["3 times as many, each the same size", "The parts get 3 times bigger", "The amount gets 3 times bigger"],
                   "4 × 3 = 12: each fourth is cut into 3 equal parts. So there are 3 times as many parts, and each one is "
                   "%s as big. The amount does not change." % fr(1, 3), rnd))
    (nm, he, his) = P.next()
    its.append(mcq("%s says %s = %s, because %s added 1 to the top and the bottom. Is %s right?" % (nm, fr(1, 2), fr(2, 3), he, he),
                   "No. Multiply both by the same number",
                   ["Yes. Do the same to both numbers", "No. Add 2 to both numbers", "Yes. Thirds are just smaller parts"],
                   "%s is more than %s. Adding the same number changes the amount. Multiply instead: %s = %s."
                   % (fr(2, 3), fr(1, 2), fr(1, 2), fr(2, 4)), rnd))
    (nm, he, his) = P.next()
    its.append(mcq("%s says %s is more than %s because it has more parts. Is %s right?" % (nm, fr(4, 10), fr(2, 5), he),
                   "No. They are equal",
                   ["Yes. 4 is more than 2", "Yes. 10 parts is more than 5", "No. %s is less" % fr(4, 10)],
                   "Each fifth is cut into 2 tenths, so %s = %s. Tenths are smaller parts, so it takes more of them "
                   "to make the same amount." % (fr(2, 5), fr(4, 10)), rnd))
    (nm, he, his) = P.next()
    its.append(mcq("%s multiplied only the top of %s by 2 and got %s. What should %s do?" % (nm, fr(3, 5), fr(6, 5), he),
                   "Multiply the bottom by 2 too",
                   ["Add 2 to the bottom", "Multiply the bottom by 5", "Nothing. %s = %s" % (fr(6, 5), fr(3, 5))],
                   "To keep the amount the same, multiply the top <b>and</b> bottom by the same number: %s = %s."
                   % (fr(3, 5), fr(6, 10)), rnd))
    its.append(mcq("Which is true about %s and %s?" % (fr(1, 4), fr(3, 12)), "They are equal",
                   ["%s is more. 3 is more than 1" % fr(3, 12), "%s is more. 4 is less than 12" % fr(1, 4), "You can’t compare them"],
                   "Cut each fourth into 3 equal parts: %s = %s. Three twelfths fill one fourth." % (fr(1, 4), fr(3, 12)), rnd))
    assert len(its) == 20, len(its)
    return {"title": "Word problems and explain why", "items": its}


# ============================================================ lesson
def body_html():
    rows = [(3, 2), (6, 4), (12, 8)]
    s = []
    for r, (n, k) in enumerate(rows):
        y = 6 + r * 56
        s.append(sfr(22, y + 14, k, n, 16))
        s.append(bar_row(54, y, 300, 42, n, k))
    eq_fig = svg_wrap(366, 170, "".join(s), "two thirds, four sixths and eight twelfths shaded on three bars of the same size")
    return (
        "<h2>What equivalent fractions are</h2>"
        "<p><b>Equivalent fractions</b> name the <b>same amount</b> with different numbers. "
        "Cut every part into the same number of smaller parts: you get more parts, each smaller, "
        "but the shaded amount does not change.</p>"
        "<figure class='sn-fig'>" + eq_fig +
        "<figcaption>Same bar, same shaded amount: " + fr(2, 3) + " = " + fr(4, 6) + " = " + fr(8, 12) +
        ". Each time the parts are cut in half, there are twice as many.</figcaption></figure>"
        "<h2>The rule: multiply or divide both numbers by the same number</h2>"
        + table(["Do this", "Example", "Why it works"], [
            ["Multiply the top and bottom by the same number", fr(2, 3) + " = " + fr(2 * 4, 3 * 4) + " (×&nbsp;4)",
             "Each part is cut into 4 smaller parts"],
            ["Divide the top and bottom by the same number", fr(6, 8) + " = " + fr(3, 4) + " (÷&nbsp;2)",
             "Every 2 small parts are joined into 1 bigger part"],
        ]) +
        "<figure class='sn-fig'>" + area_svg(4, 3, 2) +
        "<figcaption>" + fr(3, 4) + " of the rectangle is shaded. The dashed line cuts every part in 2: now 6 of 8 parts are shaded, so "
        + fr(3, 4) + " = " + fr(6, 8) + ".</figcaption></figure>"
        + ex("Example", "Find the missing number: " + fr(3, 5) + " = " + frq(10),
             "5 × 2 = 10, so multiply the bottom by 2. Do the same to the top: 3 × 2 = 6.", "6")
        + "<h2>On a number line</h2>"
        "<p>Equivalent fractions are at the <b>same point</b> on a number line.</p>"
        "<figure class='sn-fig'>" + line_svg(4, 8, 3) +
        "<figcaption>The dot is at " + fr(3, 4) + ". With eighths, it is 6 small spaces from 0, so " + fr(3, 4) + " = " + fr(6, 8) + ".</figcaption></figure>"
        "<h2>Tenths and hundredths</h2>"
        "<figure class='sn-fig'>" + hundred_svg(3) +
        "<figcaption>3 columns of 10 are shaded: " + fr(3, 10) + " = " + fr(30, 100) + ".</figcaption></figure>"
        + ex("Example", "Write " + fr(1, 4) + " in hundredths.", "4 × 25 = 100, so multiply the top by 25 too: 1 × 25 = 25.",
             fr(25, 100))
        + "<h2>Common mistakes</h2>"
        + table(["Mistake", "What to do instead"], [
            ["Adding the same number: " + fr(2, 3) + " → " + fr(4, 5), "<b>Multiply</b> the top and bottom: " + fr(2, 3) + " = " + fr(4, 6)],
            ["Multiplying only the bottom: " + fr(1, 2) + " → " + fr(1, 4), "Change <b>both</b> numbers by the same number"],
            ["Thinking " + fr(4, 8) + " is more than " + fr(1, 2) + " because it has more parts", "More parts means smaller parts. The amount is the same"],
            ["Writing " + fr(3, 10) + " as " + fr(3, 100), "Multiply both by 10: " + fr(30, 100)],
        ])
    )


FAQ = [
    {"q": "How do you explain equivalent fractions to a 4th grader?",
     "a": "Show the same bar shaded two ways. Cut each third of 2/3 in half: there are twice as many parts, each half as big, so 2/3 = 4/6. The amount does not change."},
    {"q": "How do you find an equivalent fraction?",
     "a": "Multiply or divide the top and bottom by the same number. For 2/3 = ?/12, 3 × 4 = 12, so 2 × 4 = 8 and 2/3 = 8/12."},
    {"q": "Why can’t you add the same number to the top and bottom?",
     "a": "Adding changes the amount. 1/2 + 1 on top and bottom gives 2/3, which is more than 1/2. Only multiplying or dividing both numbers by the same number keeps the amount the same."},
    {"q": "How do you change tenths to hundredths?",
     "a": "Multiply the top and bottom by 10. 3/10 = 30/100, because each tenth is 10 hundredths."},
]


def gen():
    rnd = random.Random(103)
    SPOTS.left = []
    sets = [set_models(rnd), set_multiply(rnd), set_divide(rnd), set_lines(rnd), set_words(rnd)]
    for s in sets:
        assert len(s["items"]) == 20, (s["title"], len(s["items"]))
        for it in s["items"]:
            assert len(set(it["c"])) == 4, it
    return {
        "country": "us", "subject": "math", "grade": "grade-4", "slug": "equivalent-fractions", "sort": 3,
        "updated": UPDATED, "pdf_url": "",
        "title": "Equivalent Fractions",
        "seo_title": "Grade 4 Equivalent Fractions Worksheets: Fraction Models, Missing Numbers, Number Lines and Hundredths",
        "short_title": "Equivalent Fractions",
        "domain": "Number and Operations—Fractions",
        "standard_code": "4.NF.A.1",
        "standard_url": "https://www.thecorestandards.org/Math/Content/4/NF/A/1/",
        "standard_text": "Explain why a fraction a/b is equivalent to a fraction (n × a)/(n × b) by using visual fraction models, with attention to how the number and size of the parts differ even though the two fractions themselves are the same size. Use this principle to recognize and generate equivalent fractions.",
        "meta_desc": "Free Grade 4 equivalent fractions worksheets with pictures: see equal amounts in fraction bars and area models, find the missing number, simplify, use number lines, and change tenths to hundredths. 100 practice questions with step-by-step answers.",
        "key_big": "Multiply or divide the top and bottom by the same number. The amount stays the same.",
        "key_sub": "2/3 = 4/6: each third is cut into 2 equal parts, so there are twice as many parts, each half as big. Adding the same number to the top and bottom does not work.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }


def mark_large(u, pattern):
    """Tag pictures that must print larger so their labels stay readable."""
    rx = re.compile(r"<svg (?=[^>]*aria-label='" + pattern + ")")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u


if __name__ == "__main__":
    u = gen()
    path = os.path.join(OUT, "equivalent-fractions.json")
    with open(path, "w", encoding="utf-8") as f:
        mark_large(u, "number line")
        json.dump(u, f, ensure_ascii=False, indent=1)
    print("wrote", path)
