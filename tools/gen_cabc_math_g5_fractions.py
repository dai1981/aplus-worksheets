# -*- coding: utf-8 -*-
"""
British Columbia Grade 5 Math: Equivalent fractions
(BC Mathematics Curriculum, Grade 5 — Content: Number, "Equivalent fractions")
  python3 tools/gen_cabc_math_g5_fractions.py
Equivalent fractions with models (fraction bars, a fraction wall, double number lines, grouped bars),
multiplying and dividing the numerator and denominator by the same number, simplest form,
comparing and ordering fractions by writing them with a common denominator, and word problems set in BC.
Every choice carries its value where it is a number; a wrong choice never equals the right value or another
wrong one. Every comparison and order is checked in code with exact fractions.
Canadian English. HTML attributes use single quotes (no backslashes in the JSON).
"""
import json, math, os, random, re, itertools
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "ca-bc", "math", "grade-5")
SLUG = "equivalent-fractions"
UPDATED = "2026-11-02"
FILL = "#4fae74"
BLUE = "#2f6fc0"
LINE = "#2b2b2b"
THIN = "#8a8a8a"
FONT = "Arial, Helvetica, sans-serif"
CANT = "You can’t tell"
SAME = "They are equal"
WORD = {2: "halves", 3: "thirds", 4: "fourths", 5: "fifths", 6: "sixths", 7: "sevenths", 8: "eighths",
        9: "ninths", 10: "tenths", 12: "twelfths", 15: "fifteenths", 16: "sixteenths", 18: "eighteenths",
        20: "twentieths", 24: "twenty-fourths", 30: "thirtieths"}
ONE = {2: "half", 3: "third", 4: "fourth", 5: "fifth", 6: "sixth", 7: "seventh", 8: "eighth", 9: "ninth",
       10: "tenth", 12: "twelfth"}


# ------------------------------------------------------------ numbers
def fr(a, b):
    return "<span class='fr'><span class='fn'>%s</span><span class='fd'>%s</span></span>" % (a, b)


def frq(b):
    return fr("<b>?</b>", b)


def frq_d(a):
    return fr(a, "<b>?</b>")


def Fc(a, b, unit=""):
    return (fr(a, b) + unit, F(a, b))


def Nc(n, unit=""):
    assert 0 < n < 10000
    return ("%d%s" % (n, unit), F(n))


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
            "role='img' aria-label='%s'><g font-family='%s'>%s</g></svg>" % (w, h, w, h, label, FONT, body))


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


def wall_svg(dens, shade=None, W=312, H=38):
    """Fraction wall: a row for 1 whole, then one row per denominator, every cell labelled."""
    s = []
    x0 = 4
    for r, d in enumerate([1] + list(dens)):
        y = 4 + r * H
        k = shade[1] if shade and shade[0] == d else 0
        s.append(bar_row(x0, y, W, H, d, k))
        for i in range(d):
            cx = x0 + (i + 0.5) * W / float(d)
            if d == 1:
                s.append("<text x='%.1f' y='%.1f' font-size='16' font-weight='700' fill='%s' text-anchor='middle'>1</text>"
                         % (cx, y + 25, LINE))
            else:
                s.append(sfr(cx, y + 16, 1, d, 14))
    lab = "fraction wall with rows for 1 whole and %s" % ", ".join(WORD[d] for d in dens)
    if shade:
        lab += ", %d %s shaded" % (shade[1], WORD[shade[0]] if shade[1] > 1 else ONE[shade[0]])
    return svg_wrap(W + 8, (len(dens) + 1) * H + 8, "".join(s), lab)


def tick_line(d, Y, x0, x1):
    """Number line from 0 to 1 in steps of 1/d, with 0 and 1 labelled below."""
    s = ["<line x1='%.1f' y1='%d' x2='%.1f' y2='%d' stroke='%s' stroke-width='2.5'/>" % (x0, Y, x1, Y, LINE)]
    for i in range(d + 1):
        X = x0 + (x1 - x0) * i / float(d)
        end = i in (0, d)
        s.append("<line x1='%.1f' y1='%d' x2='%.1f' y2='%d' stroke='%s' stroke-width='%s'/>"
                 % (X, Y - (11 if end else 8), X, Y + (11 if end else 8), LINE, "2.5" if end else "1.8"))
        if end:
            s.append("<text x='%.1f' y='%d' font-size='16' font-weight='700' fill='%s' text-anchor='middle'>%d</text>"
                     % (X, Y + 29, LINE, i // d))
    return "".join(s)


def double_line_svg(d1, d2, t, W=384):
    """Two number lines 0..1: the top one in steps of 1/d1 with an arrow at t, the bottom one in steps of 1/d2.
    A dashed guide drops from the arrow to the bottom line."""
    x0, x1 = 16, W - 16
    Y1, Y2 = 40, 106
    X = x0 + (x1 - x0) * float(t)
    s = [tick_line(d1, Y1, x0, x1), tick_line(d2, Y2, x0, x1),
         "<line x1='%.1f' y1='%d' x2='%.1f' y2='%d' stroke='%s' stroke-width='2' stroke-dasharray='5 4'/>"
         % (X, Y1 + 12, X, Y2 - 12, BLUE),
         "<line x1='%.1f' y1='4' x2='%.1f' y2='%d' stroke='%s' stroke-width='3'/>" % (X, X, Y1 - 18, BLUE),
         "<path d='M%.1f %d L%.1f %d L%.1f %d Z' fill='%s'/>" % (X - 7, Y1 - 20, X + 7, Y1 - 20, X, Y1 - 9, BLUE)]
    return svg_wrap(W, Y2 + 36, "".join(s),
                    "two number lines from 0 to 1, the top one split into %s and the bottom one split into %s, "
                    "with an arrow on the top line" % (WORD[d1], WORD[d2]))


# ============================================================ set 1: equivalent fractions with models
def set_models(rnd):
    SPOTS.left = []
    its = []
    # 1-6 two bars: find the missing numerator
    for a, b, d in [(1, 2, 6), (1, 3, 6), (2, 5, 10), (3, 4, 8), (2, 3, 12), (5, 6, 12)]:
        n = d // b
        c = a * n
        q = (fig(two_bars_svg(b, a, d, c)) + "The bars are the same size and show the same amount.<br>%s = %s"
             % (fr(a, b), frq(d)))
        e = ("The bottom bar has %d equal parts, so each %s of the top bar is split into %d parts. "
             "%s become%s %d × %d = <b>%d</b> %s. So %s = %s."
             % (d, ONE[b], n, parts(a, b), "s" if a == 1 else "", a, n, c, WORD[d], fr(a, b), fr(c, d)))
        its.append(mcq(q, Nc(c), [Nc(a + (d - b)), Nc(a), Nc(d - c), Nc(c + 1), Nc(n)], e, rnd))

    # 7-9 which equation do the bars show?
    for a, b, d in [(1, 4, 8), (2, 3, 9), (4, 5, 10)]:
        n = d // b
        c = a * n
        right = "%s = %s" % (fr(a, b), fr(c, d))
        add = "%s = %s" % (fr(a, b), fr(a + d - b, d))
        same_top = "%s = %s" % (fr(a, b), fr(a, d))
        unshaded = "%s = %s" % (fr(a, b), fr(d - c, d))
        assert F(a + d - b, d) != F(a, b) and F(a, d) != F(a, b) and F(d - c, d) != F(a, b)
        q = fig(two_bars_svg(b, a, d, c)) + "The bars are the same size. Which equation do they show?"
        e = ("The top bar shows %s. The bottom bar shows %d shaded parts out of %d, so it shows %s. "
             "The shaded amounts are the same, so <b>%s</b>. Both numbers were multiplied by %d."
             % (fr(a, b), c, d, fr(c, d), right, n))
        its.append(mcq(q, right, [add, same_top, unshaded], e, rnd))

    # 10-13 fraction wall
    for dens, (sd, k), t in [((2, 4, 8), (4, 3), 8), ((3, 6, 12), (3, 2), 12), ((5, 10), (5, 4), 10),
                             ((2, 6, 12), (6, 5), 12)]:
        n = t // sd
        c = k * n
        q = (fig(wall_svg(dens, (sd, k))) + "Use the fraction wall. %s is shaded. How many %s are equal to %s?"
             % (fr(k, sd), WORD[t], fr(k, sd)))
        e = ("Look down the fraction wall. Each %s is the same as %d %s, so %s line%s up with %d × %d = <b>%d</b> %s. "
             "So %s = %s." % (ONE[sd], n, WORD[t], parts(k, sd), "s" if k == 1 else "", k, n, c, WORD[t],
                              fr(k, sd), fr(c, t)))
        its.append(mcq(q, Nc(c), [Nc(k + (t - sd)), Nc(k), Nc(t - c), Nc(c + n), Nc(c + 1)], e, rnd))

    # 14-17 double number lines
    for d1, d2, a in [(4, 8, 3), (3, 6, 2), (5, 10, 2), (4, 12, 1)]:
        n = d2 // d1
        c = a * n
        t = F(a, d1)
        q = (fig(double_line_svg(d1, d2, t)) + "The arrow points to %s on the top line. "
             "Which fraction on the bottom line is at the same point?" % fr(a, d1))
        e = ("The bottom line is split into %s, so each %s on the top line is %d %s. Count %d × %d = <b>%d</b> marks "
             "from 0 on the bottom line. So %s = <b>%s</b>." % (WORD[d2], ONE[d1], n, WORD[d2], a, n, c,
                                                                fr(a, d1), fr(c, d2)))
        its.append(mcq(q, Fc(c, d2), [Fc(a + d2 - d1, d2), Fc(a, d2), Fc(d2 - c, d2), Fc(c + 1, d2), Fc(c - 1, d2)],
                       e, rnd))

    # 18-20 group the parts
    for n, k, g in [(12, 9, 3), (10, 6, 2), (12, 8, 4)]:
        sn, sd = k // g, n // g
        q = (fig(group_bar_svg(n, k, g)) + "%s of the bar is shaded. The thick lines make groups of %d parts. "
             "Which equivalent fraction does the bar show?" % (fr(k, n), g))
        e = ("There are %d groups and %d of them are shaded, so %s = <b>%s</b>. "
             "This is the same as dividing %d and %d by %d." % (sd, sn, fr(k, n), fr(sn, sd), k, n, g))
        cands = [Fc(sn, n), Fc(k - g, n - g), Fc(sd, sn), Fc(k, sd), Fc(sn + 1, sd), Fc(sn, sd + 1)]
        its.append(mcq(q, Fc(sn, sd), cands, e, rnd))
    assert len(its) == 20, len(its)
    return {"title": "Equivalent fractions with models", "items": its}


# ============================================================ set 2: multiply or divide the top and bottom
def set_multiply(rnd):
    SPOTS.left = []
    its = []
    # 1-4 multiply: missing numerator
    for a, b, d in [(1, 3, 9), (3, 5, 15), (2, 7, 14), (3, 8, 24)]:
        n = d // b
        c = a * n
        e = ("Look at the denominators: %d × <b>%d</b> = %d. Multiply the numerator by %d too: %d × %d = <b>%d</b>. "
             "So %s = %s." % (b, n, d, n, a, n, c, fr(a, b), fr(c, d)))
        its.append(mcq("%s = %s" % (fr(a, b), frq(d)), Nc(c), [Nc(a + (d - b)), Nc(a), Nc(n), Nc(d - c), Nc(c + n)], e, rnd))
    # 5-7 multiply: missing denominator
    for a, b, c in [(2, 5, 8), (3, 4, 9), (5, 6, 15)]:
        n = c // a
        d = b * n
        e = ("Look at the numerators: %d × <b>%d</b> = %d. Multiply the denominator by %d too: %d × %d = <b>%d</b>. "
             "So %s = %s." % (a, n, c, n, b, n, d, fr(a, b), fr(c, d)))
        its.append(mcq("%s = %s" % (fr(a, b), frq_d(c)), Nc(d), [Nc(b + (c - a)), Nc(b), Nc(c * b), Nc(d + 1), Nc(n)],
                       e, rnd))
    # 8-11 divide
    for (a, b), (x, y), miss in [((6, 9), (None, 3), "n"), ((10, 15), (2, None), "d"), ((12, 16), (None, 4), "n"),
                                 ((14, 21), (2, None), "d")]:
        g = b // y if miss == "n" else a // x
        sa, sb = a // g, b // g
        if miss == "n":
            q = "%s = %s" % (fr(a, b), frq(sb))
            e = ("%d ÷ <b>%d</b> = %d, so divide the numerator by %d too: %d ÷ %d = <b>%d</b>. So %s = %s."
                 % (b, g, sb, g, a, g, sa, fr(a, b), fr(sa, sb)))
            ans = sa
            cands = [Nc(a - (b - sb)) if a - (b - sb) > 0 else None, Nc(g), Nc(sb - sa), Nc(sa + 1), Nc(a)]
        else:
            q = "%s = %s" % (fr(a, b), frq_d(sa))
            e = ("%d ÷ <b>%d</b> = %d, so divide the denominator by %d too: %d ÷ %d = <b>%d</b>. So %s = %s."
                 % (a, g, sa, g, b, g, sb, fr(a, b), fr(sa, sb)))
            ans = sb
            cands = [Nc(b - (a - sa)), Nc(g), Nc(sb + 1), Nc(sb - 1), Nc(b)]
        its.append(mcq(q, Nc(ans), cands, e, rnd))
    # 12-13 what number were both multiplied by?
    for a, b, n in [(4, 7, 5), (3, 8, 4)]:
        c, d = a * n, b * n
        e = ("%d × <b>%d</b> = %d and %d × <b>%d</b> = %d. Both numbers were multiplied by <b>%d</b>. "
             "(%d − %d = %d is a difference, not a multiplier.)" % (a, n, c, b, n, d, n, c, a, c - a))
        its.append(mcq("%s = %s<br>What number were the numerator and the denominator both multiplied by?"
                       % (fr(a, b), fr(c, d)), Nc(n), [Nc(c - a), Nc(d - b), Nc(a), Nc(b)], e, rnd))
    # 14-16 which fraction is equivalent?
    for (a, b), n, k in [((2, 5), 3, 3), ((3, 4), 5, 1), ((4, 9), 2, 2)]:
        c, d = a * n, b * n
        e = ("Multiply the numerator and the denominator by %d: %d × %d = %d and %d × %d = %d. So %s = <b>%s</b>. "
             "%s adds %d to both numbers, so it is a different amount."
             % (n, a, n, c, b, n, d, fr(a, b), fr(c, d), fr(a + k + 1, b + k + 1), k + 1))
        cands = [Fc(a + k + 1, b + k + 1), Fc(c, b), Fc(a, d), Fc(c, d + 1)]
        its.append(mcq("Which fraction is equivalent to %s?" % fr(a, b), Fc(c, d), cands, e, rnd))
    # 17-18 which is NOT equivalent?
    for (a, b), trues, bad, k in [((3, 5), [(6, 10), (9, 15), (12, 20)], (5, 7), 2),
                                  ((3, 4), [(6, 8), (9, 12), (15, 20)], (6, 7), 3)]:
        for t in trues:
            assert F(*t) == F(a, b)
        assert F(*bad) != F(a, b) and bad == (a + k, b + k)
        e = ("<b>%s</b> is not equivalent to %s: %d was added to the numerator and the denominator, and adding changes "
             "the amount. The others are equivalent, because both numbers were multiplied by the same number."
             % (fr(*bad), fr(a, b), k))
        its.append(mcq("Which fraction is <b>not</b> equivalent to %s?" % fr(a, b), fr(*bad), [fr(*t) for t in trues],
                       e, rnd))
    # 19-20 which pair is equivalent?
    for right, wrongs in [(((4, 6), (10, 15)), [((3, 4), (5, 6)), ((2, 5), (4, 5)), ((1, 3), (2, 9))]),
                          (((6, 8), (9, 12)), [((2, 3), (4, 5)), ((1, 4), (2, 4)), ((5, 6), (10, 18))])]:
        assert F(*right[0]) == F(*right[1])
        for p in wrongs:
            assert F(*p[0]) != F(*p[1])
        pr = lambda p: "%s and %s" % (fr(*p[0]), fr(*p[1]))
        (a, b), (c, d) = right
        g = math.gcd(a, b)
        e = ("Simplify both: %s = %s and %s = %s. They are the same, so <b>%s</b> are equivalent. "
             "In the other pairs the two fractions show different amounts."
             % (fr(a, b), show(F(a, b)), fr(c, d), show(F(c, d)), pr(right)))
        its.append(mcq("Which pair of fractions is equivalent?", pr(right), [pr(p) for p in wrongs], e, rnd))
    assert len(its) == 20, len(its)
    return {"title": "Multiply or divide the top and bottom", "items": its}


# ============================================================ set 3: simplest form
def simp_cands(a, b):
    g = math.gcd(a, b)
    sa, sb = a // g, b // g
    sub = a - sa
    return [Fc(sa, b - sub) if b - sub > sa else None, Fc(sa, b), Fc(a, sb), Fc(sb, sa),
            Fc(sa + 1, sb), Fc(sa, sb + 1), Fc(sa - 1, sb) if sa > 1 else None, Fc(1, sb) if sa > 1 else None]


def set_simplest(rnd):
    SPOTS.left = []
    its = []
    # 1-3 which is in simplest form?
    for right, others in [((5, 8), [(4, 6), (6, 10), (3, 9)]), ((7, 12), [(9, 12), (2, 10), (4, 8)]),
                          ((4, 9), [(6, 15), (10, 12), (3, 12)])]:
        assert math.gcd(*right) == 1 and all(math.gcd(*o) > 1 for o in others)
        e = ("%s is in simplest form, because no number except 1 divides both %d and %d. The others can be simplified: "
             "%s." % (fr(*right), right[0], right[1],
                      ", ".join("%s = %s" % (fr(*o), show(F(*o))) for o in others)))
        its.append(mcq("Which fraction is in simplest form?", fr(*right), [fr(*o) for o in others], e, rnd))
    # 4-5 greatest common factor
    for a, b in [(12, 18), (16, 24)]:
        g = math.gcd(a, b)
        small = [x for x in range(2, g) if a % x == 0 and b % x == 0]
        e = ("Factors of %d: %s. Factors of %d: %s. The greatest number in both lists is <b>%d</b>. "
             "%s also divide both, but %d is greater. So %s = %s."
             % (a, ", ".join(str(x) for x in range(1, a + 1) if a % x == 0),
                b, ", ".join(str(x) for x in range(1, b + 1) if b % x == 0), g,
                " and ".join(str(x) for x in small), g, fr(a, b), fr(a // g, b // g)))
        its.append(mcq("To write %s in simplest form, Kai divides the numerator and the denominator by the greatest "
                       "number that divides both. What is that number?" % fr(a, b),
                       Nc(g), [Nc(small[-1]), Nc(small[0]), Nc(b - a), Nc(lcm(a, b))], e, rnd))
    # 6-17 write in simplest form
    for a, b in [(6, 8), (4, 10), (3, 9), (5, 15), (8, 12), (9, 12), (10, 15), (12, 16), (14, 20), (12, 18),
                 (16, 24), (18, 24)]:
        g = math.gcd(a, b)
        sa, sb = a // g, b // g
        e = ("%d is the greatest number that divides both %d and %d. %d ÷ %d = %d and %d ÷ %d = %d. So %s = <b>%s</b>."
             % (g, a, b, a, g, sa, b, g, sb, fr(a, b), fr(sa, sb)))
        if g in (4, 6, 8):
            p = 2
            e += " (Dividing by %d first gives %s, which can still be simplified.)" % (p, fr(a // p, b // p))
        its.append(mcq("Write %s in simplest form." % fr(a, b), Fc(sa, sb), simp_cands(a, b), e, rnd))
    # 18-20 check someone's work
    its.append(mcq("Harjot writes %s in simplest form as %s. Is he right?" % (fr(12, 18), fr(6, 9)),
                   "No. %s = %s" % (fr(6, 9), fr(2, 3)),
                   ["Yes. %s is in simplest form" % fr(6, 9), "No. %s = %s" % (fr(12, 18), fr(3, 4)),
                    "No. %s = %s" % (fr(12, 18), fr(10, 16))],
                   "Harjot divided by 2, but 3 still divides both 6 and 9: %s = %s. "
                   "Divide by 6 in one step: 12 ÷ 6 = 2 and 18 ÷ 6 = 3. So the simplest form is <b>%s</b>."
                   % (fr(6, 9), fr(2, 3), fr(2, 3)), rnd))
    its.append(mcq("Mei says %s in simplest form is %s. Is she right?" % (fr(15, 20), fr(3, 4)),
                   "Yes. Divide both by 5",
                   ["No. It is %s" % fr(3, 5), "No. It is %s" % fr(5, 10), "No. It is already in simplest form"],
                   "5 divides both 15 and 20: 15 ÷ 5 = 3 and 20 ÷ 5 = 4. 3 and 4 have no common factor except 1, "
                   "so <b>%s</b> is the simplest form. Mei is right." % fr(3, 4), rnd))
    its.append(mcq("Ava takes 6 away from the top and the bottom of %s and gets %s. Is that right?" % (fr(9, 12), fr(3, 6)),
                   "No. %s = %s" % (fr(9, 12), fr(3, 4)),
                   ["Yes. %s = %s" % (fr(9, 12), fr(3, 6)), "No. %s = %s" % (fr(9, 12), fr(1, 2)),
                    "No. %s = %s" % (fr(9, 12), fr(3, 5))],
                   "Subtracting changes the amount: %s is %s, not %s. Divide instead: 9 ÷ 3 = 3 and 12 ÷ 3 = 4, so "
                   "%s = <b>%s</b>." % (fr(3, 6), fr(1, 2), fr(9, 12), fr(9, 12), fr(3, 4)), rnd))
    assert F(3, 6) != F(9, 12) and F(15, 20) == F(3, 4) and F(6, 9) == F(2, 3)
    assert len(its) == 20, len(its)
    return {"title": "Simplest form", "items": its}


# ============================================================ set 4: compare using equivalent fractions
def set_compare(rnd):
    SPOTS.left = []
    its = []

    def which(x, y, bars=False):
        a, b = x
        c, d = y
        X, Y = F(a, b), F(c, d)
        if X == Y:
            right = SAME
        else:
            right = fr(a, b) if X > Y else fr(c, d)
        if a == c:
            e = ("The numerators are the same, so compare the size of the parts. %s are smaller than %s, because the whole "
                 "is cut into more parts. So <b>%s</b> is greater." % (WORD[max(b, d)].capitalize(), WORD[min(b, d)],
                                                                        show(max(X, Y))))
        else:
            L = lcm(b, d)
            e = "Use %s for both: %s and %s. " % (WORD[L], fr(a, b) if b == L else eqL(X, L), fr(c, d) if d == L else eqL(Y, L))
            if X == Y:
                e += "The numerators are the same, so <b>they are equal</b>."
            else:
                e += "%d &gt; %d, so <b>%s</b> is greater." % (max(X, Y) * L, min(X, Y) * L, show(max(X, Y)))
        q = "Which is greater: %s or %s?" % (fr(a, b), fr(c, d))
        if bars:
            q = fig(two_bars_svg(b, a, d, c)) + "The bars are the same size. " + q
        return mcq(q, right, [fr(a, b), fr(c, d), SAME, CANT], e, rnd)

    for x, y in [((3, 8), (3, 5)), ((2, 9), (2, 7))]:
        its.append(which(x, y))
    its.append(which((2, 3), (7, 12), True))
    its.append(which((5, 8), (3, 4), True))
    for x, y in [((3, 5), (7, 10)), ((5, 6), (11, 12)), ((3, 4), (9, 12)), ((1, 2), (5, 12)), ((2, 3), (3, 4)),
                 ((4, 5), (7, 10)), ((2, 5), (1, 3)), ((5, 8), (2, 3))]:
        its.append(which(x, y))

    # 13 common denominator
    its.append(mcq("To compare %s and %s, Lucas writes both with the same denominator. Which denominator works?"
                   % (fr(2, 3), fr(3, 4)),
                   Nc(12), [Nc(7), Nc(6), Nc(4)],
                   "The denominator must be a multiple of both 3 and 4. 12 is: 3 × 4 = 12. So %s = %s and %s = %s. "
                   "7 = 3 + 4 does not work: you can’t make sevenths from thirds or fourths." %
                   (fr(2, 3), fr(8, 12), fr(3, 4), fr(9, 12)), rnd))

    # 14-16 greatest / smallest
    for word, vs in [("greatest", [F(3, 4), F(5, 8), F(1, 2), F(3, 8)]),
                     ("smallest", [F(2, 3), F(5, 6), F(7, 12), F(5, 12)]),
                     ("greatest", [F(3, 5), F(7, 10), F(1, 2), F(2, 5)])]:
        best = max(vs) if word == "greatest" else min(vs)
        L = lcd(vs)
        e = ("Write them all with the denominator %d: %s. The %s is %s, so the answer is <b>%s</b>."
             % (L, ", ".join(eqL(v, L) for v in vs), word, over(best, L), show(best)))
        its.append(mcq("Which fraction is the %s?<br>%s" % (word, ", ".join(show(v) for v in vs)), (show(best), best),
                       [(show(v), v) for v in vs if v != best], e, rnd))

    # 17-18 order
    def s_of(seq):
        return ", ".join(show(v) for v in seq)
    for vs, up in [([F(3, 4), F(5, 8), F(1, 2)], True), ([F(3, 10), F(1, 2), F(2, 5)], False)]:
        right = sorted(vs, reverse=not up)
        perms = [sorted(vs, key=lambda v: v.numerator), sorted(vs, key=lambda v: v.denominator),
                 sorted(vs, key=lambda v: -v.denominator), list(reversed(right))]
        perms += [list(p) for p in itertools.permutations(vs)]
        L = lcd(vs)
        e = ("Use the denominator %d: %s. So the order is <b>%s</b>."
             % (L, ", ".join(eqL(v, L) for v in vs), s_of(right)))
        its.append(mcq("Order from %s:<br>%s" % ("least to greatest" if up else "greatest to least", s_of(vs)),
                       s_of(right), [s_of(p) for p in perms if p != right], e, rnd))

    # 19-20 between
    assert F(1, 2) < F(5, 8) < F(3, 4)
    its.append(mcq("Which fraction is between %s and %s?" % (fr(1, 2), fr(3, 4)), Fc(5, 8), [Fc(7, 8), Fc(3, 8), Fc(5, 6)],
                   "In eighths: %s = %s and %s = %s. <b>%s</b> is between them. %s is less than %s. %s and %s are more than %s."
                   % (fr(1, 2), fr(4, 8), fr(3, 4), fr(6, 8), fr(5, 8), fr(3, 8), fr(1, 2), fr(7, 8), fr(5, 6), fr(3, 4)), rnd))
    assert F(1, 3) < F(5, 12) < F(1, 2) and F(1, 4) < F(1, 3) and F(7, 12) > F(1, 2) and F(2, 3) > F(1, 2)
    its.append(mcq("Which fraction is between %s and %s?" % (fr(1, 3), fr(1, 2)), Fc(5, 12), [Fc(1, 4), Fc(7, 12), Fc(2, 3)],
                   "In twelfths: %s = %s and %s = %s. <b>%s</b> is between them. %s = %s is too small. "
                   "%s and %s = %s are too big."
                   % (fr(1, 3), fr(4, 12), fr(1, 2), fr(6, 12), fr(5, 12), fr(1, 4), fr(3, 12), fr(7, 12), fr(2, 3),
                      fr(8, 12)), rnd))
    assert len(its) == 20, len(its)
    return {"title": "Compare fractions using equivalents", "items": its}


# ============================================================ set 5: word problems
def set_words(rnd):
    SPOTS.left = []
    its = []
    # 1
    its.append(mcq("A pizza is cut into 8 equal slices. Liam eats %s of the pizza. How many slices does he eat?" % fr(3, 4),
                   Nc(6, " slices"), [Nc(3, " slices"), Nc(7, " slices"), Nc(4, " slices")],
                   "4 × 2 = 8, so multiply the top by 2 too: %s = %s. Liam eats <b>6 slices</b>." % (fr(3, 4), fr(6, 8)), rnd))
    # 2
    its.append(mcq("A muffin recipe needs %s cup of milk. Ava’s measuring cup is marked in sixths. "
                   "How many sixths of a cup should she pour?" % fr(2, 3),
                   Nc(4, " sixths"), [Nc(2, " sixths"), Nc(5, " sixths"), Nc(3, " sixths")],
                   "3 × 2 = 6, so multiply the top by 2 too: %s = %s. Ava pours <b>4 sixths</b> of a cup." % (fr(2, 3), fr(4, 6)),
                   rnd))
    # 3
    its.append(mcq("On a field trip to a salmon hatchery, Mei counts 12 fish in a tank. 8 of them are coho salmon. "
                   "What fraction of the fish are coho, in simplest form?",
                   Fc(2, 3), [Fc(1, 3), Fc(3, 2), Fc(2, 12)],
                   "8 out of 12 is %s. 4 divides both: 8 ÷ 4 = 2 and 12 ÷ 4 = 3. So <b>%s</b> of the fish are coho."
                   % (fr(8, 12), fr(2, 3)), rnd))
    # 4
    assert F(7, 10) > F(3, 5)
    its.append(mcq("In the Terry Fox Run, Ethan has run %s of the route. Nadia has run %s of the same route. "
                   "Who has run farther?" % (fr(3, 5), fr(7, 10)),
                   "Nadia", ["Ethan", "They have run the same distance", CANT],
                   "Use tenths: %s = %s. 7 tenths is more than 6 tenths, so <b>Nadia</b> has run farther."
                   % (fr(3, 5), fr(6, 10)), rnd))
    # 5
    its.append(mcq("A BC Ferries boat has gone %s of the way to Nanaimo. Kai says that is %s of the way. Is he right?"
                   % (fr(6, 8), fr(3, 4)),
                   "Yes. %s = %s" % (fr(6, 8), fr(3, 4)),
                   ["No. %s is less than %s" % (fr(3, 4), fr(6, 8)), "No. %s = %s" % (fr(6, 8), fr(4, 6)),
                    "No. %s = %s" % (fr(6, 8), fr(2, 4))],
                   "Divide the top and the bottom of %s by 2: 6 ÷ 2 = 3 and 8 ÷ 2 = 4. So %s = %s. <b>Kai is right.</b>"
                   % (fr(6, 8), fr(6, 8), fr(3, 4)), rnd))
    # 6
    its.append(mcq("Liam’s class plants 20 cedar seedlings. After a month, 15 of them are taller than 10 cm. "
                   "What fraction of the seedlings are taller than 10 cm, in simplest form?",
                   Fc(3, 4), [Fc(1, 4), Fc(4, 3), Fc(13, 18)],
                   "15 out of 20 is %s. 5 divides both: 15 ÷ 5 = 3 and 20 ÷ 5 = 4. So <b>%s</b>. "
                   "(%s takes 2 from both, which changes the amount.)" % (fr(15, 20), fr(3, 4), fr(13, 18)), rnd))
    # 7
    its.append(mcq("Owen says, “%s is greater than %s, because 6 is greater than 3.” Is he right?" % (fr(1, 6), fr(1, 3)),
                   "No. %s is less than %s" % (fr(1, 6), fr(1, 3)),
                   ["Yes. 6 is greater than 3", "No. They are equal", "Yes. Sixths are bigger than thirds"],
                   "A bigger denominator means the whole is cut into <b>more, smaller</b> parts. %s = %s, which is more than %s. "
                   "So %s is <b>less</b> than %s." % (fr(1, 3), fr(2, 6), fr(1, 6), fr(1, 6), fr(1, 3)), rnd))
    # 8
    its.append(mcq("Simran wants a fraction equivalent to %s. She writes %s. What did she do wrong?" % (fr(3, 5), fr(5, 7)),
                   "She added 2 to the top and the bottom",
                   ["She multiplied both numbers by 2", "Nothing. She is right", "She multiplied only the denominator"],
                   "3 + 2 = 5 and 5 + 2 = 7. Adding changes the amount. Multiply both numbers by 2 instead: %s = <b>%s</b>."
                   % (fr(3, 5), fr(6, 10)), rnd))
    # 9
    assert F(3, 5) > F(4, 10)
    its.append(mcq("In a lacrosse game, Olivia scored on 4 of her 10 shots. Zara scored on 3 of her 5 shots. "
                   "Who scored on a greater fraction of her shots?",
                   "Zara", ["Olivia", "They are the same", CANT],
                   "Olivia: %s. Zara: %s = %s. 6 tenths is more than 4 tenths, so <b>Zara</b> scored on a greater fraction."
                   % (fr(4, 10), fr(3, 5), fr(6, 10)), rnd))
    # 10
    assert F(5, 6) > F(3, 4)
    its.append(mcq("On a hike in Stanley Park, Lucas has walked %s of a trail. Jasleen has walked %s of the same trail. "
                   "Who has walked farther?" % (fr(5, 6), fr(3, 4)),
                   "Lucas", ["Jasleen", "They have walked the same distance", CANT],
                   "Use twelfths: %s = %s and %s = %s. 10 twelfths is more than 9 twelfths, so <b>Lucas</b> has walked farther."
                   % (fr(5, 6), fr(10, 12), fr(3, 4), fr(9, 12)), rnd))
    # 11
    its.append(mcq("It rained in Vancouver on 18 of the 30 days in November. What fraction of the days had rain, "
                   "in simplest form?",
                   Fc(3, 5), [Fc(2, 5), Fc(5, 3), Fc(16, 28)],
                   "18 out of 30 is %s. 6 divides both: 18 ÷ 6 = 3 and 30 ÷ 6 = 5. So <b>%s</b> of the days had rain."
                   % (fr(18, 30), fr(3, 5)), rnd))
    # 12
    rib = [("Mateo", F(3, 4)), ("Hana", F(7, 8)), ("Kai", F(5, 8)), ("Sofia", F(1, 2))]
    assert max(rib, key=lambda x: x[1])[0] == "Hana"
    its.append(mcq("Four students cut ribbons for a class project. Mateo: %s m. Hana: %s m. Kai: %s m. Sofia: %s m. "
                   "Who has the longest ribbon?" % (fr(3, 4), fr(7, 8), fr(5, 8), fr(1, 2)),
                   "Hana", ["Mateo", "Kai", "Sofia"],
                   "Use eighths: %s = %s, %s, %s, %s = %s. The longest is <b>Hana’s</b> ribbon."
                   % (fr(3, 4), fr(6, 8), fr(7, 8), fr(5, 8), fr(1, 2), fr(4, 8)), rnd))
    # 13
    its.append(mcq("Two pizzas are the same size. One is cut into 6 equal slices and the other into 12. "
                   "Noah eats 2 slices of the first pizza. How many slices of the second pizza must Leah eat "
                   "to eat the same amount?",
                   Nc(4, " slices"), [Nc(2, " slices"), Nc(8, " slices"), Nc(3, " slices")],
                   "Noah eats %s. 6 × 2 = 12, so multiply the top by 2 too: %s = %s. Leah must eat <b>4 slices</b>."
                   % (fr(2, 6), fr(2, 6), fr(4, 12)), rnd))
    # 14
    its.append(mcq("At a ski hill near Kelowna, 10 of the 16 runs are open. What fraction of the runs are open, "
                   "in simplest form?",
                   Fc(5, 8), [Fc(3, 8), Fc(8, 5), Fc(8, 14)],
                   "10 out of 16 is %s. 2 divides both: 10 ÷ 2 = 5 and 16 ÷ 2 = 8. 5 and 8 have no other common factor, "
                   "so <b>%s</b> of the runs are open." % (fr(10, 16), fr(5, 8)), rnd))
    # 15
    its.append(mcq("A whale-watching boat near Victoria sees 12 orcas. 4 of them are calves. Ji-woo writes %s for the "
                   "fraction that are calves. Which fraction is equivalent to %s?" % (fr(4, 12), fr(4, 12)),
                   Fc(2, 6), [Fc(2, 12), Fc(4, 6), Fc(6, 14)],
                   "Divide the top and the bottom of %s by 2: 4 ÷ 2 = 2 and 12 ÷ 2 = 6. So %s = <b>%s</b> (and also %s)."
                   % (fr(4, 12), fr(4, 12), fr(2, 6), fr(1, 3)), rnd))
    # 16
    pots = [("Group A", F(5, 6)), ("Group B", F(7, 12)), ("Group C", F(2, 3))]
    assert min(pots, key=lambda x: x[1])[0] == "Group B"
    its.append(mcq("Three groups each have the same size pot of paint for a mural. Group A uses %s of its pot, "
                   "Group B uses %s and Group C uses %s. Which group uses the least paint?" % (fr(5, 6), fr(7, 12), fr(2, 3)),
                   "Group B", ["Group A", "Group C", "They all use the same"],
                   "Use twelfths: %s = %s, %s, %s = %s. The smallest is %s, so <b>Group B</b> uses the least. "
                   "12 is the biggest denominator, but that does not make it the biggest fraction."
                   % (fr(5, 6), fr(10, 12), fr(7, 12), fr(2, 3), fr(8, 12), fr(7, 12)), rnd))
    # 17
    assert F(6, 8) == F(9, 12)
    its.append(mcq("The school soccer team won 6 of its 8 games. The lacrosse team won 9 of its 12 games. "
                   "Which team won a greater fraction of its games?",
                   "They won the same fraction", ["The soccer team", "The lacrosse team", CANT],
                   "Soccer: %s = %s. Lacrosse: %s = %s. Both are %s, so <b>they won the same fraction</b>."
                   % (fr(6, 8), fr(3, 4), fr(9, 12), fr(3, 4), fr(3, 4)), rnd))
    # 18
    its.append(mcq("On a family trip along the Sea-to-Sky Highway, Jasleen says they have driven more than %s but less "
                   "than %s of the way. Which fraction could it be?" % (fr(1, 2), fr(3, 4)),
                   Fc(5, 8), [Fc(7, 8), Fc(3, 8), Fc(5, 6)],
                   "In eighths: %s = %s and %s = %s. Only <b>%s</b> is between them. %s = %s is more than %s."
                   % (fr(1, 2), fr(4, 8), fr(3, 4), fr(6, 8), fr(5, 8), fr(5, 6), fr(10, 12), fr(3, 4)), rnd))
    # 19
    assert F(15, 20) == F(6, 8)
    its.append(mcq("Wei has read 15 of the 20 pages in his story. Harjot has read the same fraction of a story with "
                   "8 pages. How many pages has Harjot read?",
                   Nc(6, " pages"), [Nc(3, " pages"), Nc(4, " pages"), Nc(2, " pages")],
                   "%s = %s (divide both by 5). Then %s = %s (multiply both by 2). Harjot has read <b>6 pages</b>."
                   % (fr(15, 20), fr(3, 4), fr(3, 4), fr(6, 8)), rnd))
    # 20
    assert F(18, 20) > F(8, 10)
    its.append(mcq("Sofia gets %s on a math quiz. Ryan gets %s on a different quiz. Who got the greater fraction "
                   "of the questions right?" % (fr(18, 20), fr(8, 10)),
                   "Sofia", ["Ryan", "They are the same", CANT],
                   "Simplify Sofia’s score: %s = %s (divide both by 2). 9 tenths is more than 8 tenths, so "
                   "<b>Sofia</b> got the greater fraction right." % (fr(18, 20), fr(9, 10)), rnd))
    assert len(its) == 20, len(its)
    return {"title": "Equivalent fraction word problems", "items": its}


# ============================================================ lesson
def body_html():
    return (
        "<h2>Equivalent fractions</h2>"
        "<p><b>Equivalent fractions</b> show the same amount of the same whole. To find one, <b>multiply the numerator and "
        "the denominator by the same number</b>. The parts get smaller, but there are more of them.</p>"
        "<figure class='sn-fig'>" + two_bars_svg(4, 3, 12, 9) +
        "<figcaption>The bars are the same size. " + fr(3, 4) + " = " + fr(9, 12) + ": each fourth is split into 3.</figcaption></figure>"
        + ex("Example", fr(3, 4) + " = " + frq(12),
             "4 × 3 = 12, so multiply the numerator by 3 too: 3 × 3 = 9.", fr(9, 12))
        + "<p>A number line shows the same idea. " + fr(2, 3) + " and " + fr(4, 6) + " are at the same point.</p>"
        "<figure class='sn-fig'>" + double_line_svg(3, 6, F(2, 3)) +
        "<figcaption>Top line in thirds, bottom line in sixths: " + fr(2, 3) + " = " + fr(4, 6) + ".</figcaption></figure>"
        + "<h2>Dividing and simplest form</h2>"
        "<p>You can also <b>divide the numerator and the denominator by the same number</b>. A fraction is in "
        "<b>simplest form</b> when no number except 1 divides both. Divide by the greatest number you can.</p>"
        "<figure class='sn-fig'>" + group_bar_svg(12, 8, 4) +
        "<figcaption>Groups of 4 parts: " + fr(8, 12) + " = " + fr(2, 3) + ".</figcaption></figure>"
        + ex("Example", "Write " + fr(8, 12) + " in simplest form.",
             "4 divides both 8 and 12. 8 ÷ 4 = 2 and 12 ÷ 4 = 3.", fr(2, 3))
        + "<h2>Comparing fractions</h2>"
        "<p>Write the fractions with the <b>same denominator</b>, then compare the numerators. "
        "If the numerators are the same, the fraction with the <b>smaller</b> denominator is greater, because its parts are bigger.</p>"
        "<figure class='sn-fig'>" + two_bars_svg(3, 2, 12, 7) +
        "<figcaption>" + fr(2, 3) + " = " + fr(8, 12) + ", which is more than " + fr(7, 12) + ".</figcaption></figure>"
        + ex("Example", "Which is greater: " + fr(3, 5) + " or " + fr(7, 10) + "?",
             "Use tenths: " + fr(3, 5) + " = " + fr(6, 10) + ". 7 tenths is more than 6 tenths.", fr(7, 10))
        + ex("Example", "Order " + fr(3, 4) + ", " + fr(5, 8) + " and " + fr(1, 2) + " from least to greatest.",
             "Use eighths: " + fr(3, 4) + " = " + fr(6, 8) + ", " + fr(5, 8) + ", " + fr(1, 2) + " = " + fr(4, 8) + ".",
             fr(1, 2) + ", " + fr(5, 8) + ", " + fr(3, 4))
        + "<h2>Common mistakes</h2>"
        + table(["Mistake", "What to do instead"], [
            ["Adding the same number to the top and bottom: " + fr(2, 3) + " = " + fr(4, 5),
             "Multiply or divide, never add: " + fr(2, 3) + " = " + fr(4, 6)],
            ["Multiplying only the numerator: " + fr(2, 3) + " = " + fr(4, 3),
             "Multiply both: " + fr(2, 3) + " = " + fr(4, 6)],
            ["Stopping too early: " + fr(12, 18) + " = " + fr(6, 9),
             "Keep going, or divide by the greatest common factor: " + fr(12, 18) + " = " + fr(2, 3)],
            ["Thinking a bigger denominator means a bigger fraction: " + fr(1, 8) + " &gt; " + fr(1, 4),
             "A bigger denominator means <b>smaller</b> parts: " + fr(1, 8) + " &lt; " + fr(1, 4)],
        ])
    )


FAQ = [
    {"q": "What do Grade 5 students learn about fractions in BC?",
     "a": "In the BC Grade 5 math curriculum, students work with equivalent fractions. They use models such as fraction bars and number lines, find equivalent fractions by multiplying or dividing, write fractions in simplest form, and compare fractions."},
    {"q": "How do you find an equivalent fraction?",
     "a": "Multiply or divide the numerator and the denominator by the same number. For example, 3/4 = 9/12 (both × 3) and 8/12 = 2/3 (both ÷ 4). Adding the same number to both does not work: 2/3 is not equal to 4/5."},
    {"q": "How do you write a fraction in simplest form?",
     "a": "Find the greatest number that divides both the numerator and the denominator, and divide both by it. For 12/18, divide by 6 to get 2/3. If you divide by a smaller number first, keep going until only 1 divides both."},
    {"q": "How do you compare fractions with different denominators?",
     "a": "Write both fractions with the same denominator, then compare the numerators. For 3/5 and 7/10, 3/5 = 6/10, so 7/10 is greater."},
]


def gen():
    rnd = random.Random(55803)
    SPOTS.left = []
    sets = [set_models(rnd), set_multiply(rnd), set_simplest(rnd), set_compare(rnd), set_words(rnd)]
    seen = set()
    for s in sets:
        assert len(s["items"]) == 20, (s["title"], len(s["items"]))
        cnt = [0, 0, 0, 0]
        for it in s["items"]:
            assert len(set(re.sub(r"<[^>]+>", "", x) for x in it["c"])) == 4, it
            assert it["q"].count("<svg") <= 1
            k = re.sub(r"<[^>]+>", "", it["q"]) + "|" + "|".join(sorted(it["c"]))
            assert k not in seen, it["q"]
            seen.add(k)
            cnt[it["a"]] += 1
        assert cnt == [5, 5, 5, 5], (s["title"], cnt)
    return {
        "country": "ca-bc", "subject": "math", "grade": "grade-5", "slug": SLUG, "sort": 3,
        "updated": UPDATED, "pdf_url": "",
        "title": "Equivalent Fractions",
        "seo_title": "Grade 5 Equivalent Fractions Worksheets (BC Curriculum) – Free with Answer Key",
        "short_title": "Equivalent Fractions",
        "domain": "Number",
        "standard_code": "Grade 5: Number",
        "standard_url": "https://curriculum.gov.bc.ca/curriculum/mathematics/5/core",
        "standard_text": "Equivalent fractions",
        "meta_desc": "Free Grade 5 math worksheets on equivalent fractions for the BC curriculum: fraction bars, fraction walls and number lines, multiplying and dividing the numerator and denominator, simplest form, comparing fractions, and word problems. 100 questions with an answer key.",
        "key_big": "Equivalent fractions: multiply or divide the top and the bottom by the same number.",
        "key_sub": "3/4 = 9/12 (× 3) and 8/12 = 2/3 (÷ 4). Never add the same number to both: 2/3 is not 4/5. To compare, use a common denominator: 3/5 = 6/10 < 7/10.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, SLUG + ".json")
    mark_large(u, "(two number lines|fraction bar|two fraction bars|fraction wall)")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(u, f, ensure_ascii=False, indent=1)
    print("wrote", path)
