# -*- coding: utf-8 -*-
"""
Canada (Ontario) Grade 5 Math: Equivalent fractions and mixed numbers
(Ontario Curriculum, Grades 1-8: Mathematics, 2020 — Grade 5, Number, B1.3 and B1.4)
  python3 tools/gen_caon_math_g5_fractions.py
Equivalent fractions with models (fraction bars, a fraction wall, sharing several wholes among several
people), simplest form, improper fractions and mixed numbers (bars, number lines), comparing and ordering
fractions from halves to twelfths (including improper fractions and mixed numbers), and word problems.
Every choice carries its value; a wrong choice never equals the right value or another wrong one.
Every comparison and order is checked in code with exact fractions.
Canadian English. HTML attributes use single quotes (no backslashes in the JSON).
"""
import json, math, os, random, re, itertools
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "ca-on", "math", "grade-5")
SLUG = "equivalent-fractions-and-mixed-numbers"
UPDATED = "2026-11-02"
FILL = "#4fae74"
BLUE = "#2f6fc0"
LINE = "#2b2b2b"
THIN = "#8a8a8a"
FONT = "Arial, Helvetica, sans-serif"
CANT = "You can’t tell"
SAME = "They are equal"
WORD = {2: "halves", 3: "thirds", 4: "fourths", 5: "fifths", 6: "sixths", 7: "sevenths", 8: "eighths",
        9: "ninths", 10: "tenths", 12: "twelfths", 24: "twenty-fourths"}
ONE = {2: "half", 3: "third", 4: "fourth", 5: "fifth", 6: "sixth", 7: "seventh", 8: "eighth", 9: "ninth",
       10: "tenth", 12: "twelfth"}


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


def Nc(n, unit=""):
    assert n < 10000
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


def bars_svg(d, N, label, per_bar=None, maxw=392, H=38, gap=14):
    """Bars of d parts, side by side. per_bar(b) gives the set of shaded part indexes in bar b."""
    nb = -(-N // d) if per_bar is None else N
    cell = min(30.0, (maxw - 8 - (nb - 1) * gap) / float(nb * d))
    bw = cell * d
    s = []
    for b in range(nb):
        x0 = 4 + b * (bw + gap)
        on = set(range(min(d, N - b * d))) if per_bar is None else per_bar(b)
        for i in range(d):
            s.append("<rect x='%.1f' y='4' width='%.2f' height='%d' fill='%s' stroke='%s' stroke-width='2.5'/>"
                     % (x0 + i * cell, cell, H, FILL if i in on else "#fff", LINE))
        s.append("<rect x='%.1f' y='4' width='%.1f' height='%d' fill='none' stroke='%s' stroke-width='3'/>" % (x0, bw, H, LINE))
    return svg_wrap(8 + nb * bw + (nb - 1) * gap, H + 8, "".join(s), label)


def wholes_svg(d, N):
    nb = -(-N // d)
    return bars_svg(d, N, "bars of %d equal parts, %d bars, %d parts shaded" % (d, nb, N))


def share_svg(W, s):
    """W wholes (bars) each cut into s equal parts; one part of each bar shaded (one person's share)."""
    return bars_svg(s, W, "bars of %d equal parts, %d bars, one part of each bar shaded for one person" % (s, W),
                    per_bar=lambda b: {0})


def tick_line(L, d, Y, x0, x1):
    s = ["<line x1='%.1f' y1='%d' x2='%.1f' y2='%d' stroke='%s' stroke-width='2.5'/>" % (x0, Y, x1, Y, LINE)]
    n = L * d
    for i in range(n + 1):
        X = x0 + (x1 - x0) * i / float(n)
        whole = (i % d == 0)
        s.append("<line x1='%.1f' y1='%d' x2='%.1f' y2='%d' stroke='%s' stroke-width='%s'/>"
                 % (X, Y - (11 if whole else 7), X, Y + (11 if whole else 7), LINE, "2.5" if whole else "1.6"))
        if whole:
            s.append("<text x='%.1f' y='%d' font-size='16' font-weight='700' fill='%s' text-anchor='middle'>%d</text>"
                     % (X, Y + 30, LINE, i // d))
    return "".join(s)


def arrow_line_svg(L, d, t, W=384):
    """Number line 0..L in steps of 1/d with a blue arrow pointing at t."""
    x0, x1 = 16, W - 16
    Y = 40
    X = x0 + (x1 - x0) * float(t) / L
    s = [tick_line(L, d, Y, x0, x1),
         "<line x1='%.1f' y1='6' x2='%.1f' y2='%d' stroke='%s' stroke-width='3'/>" % (X, X, Y - 18, BLUE),
         "<path d='M%.1f %d L%.1f %d L%.1f %d Z' fill='%s'/>" % (X - 7, Y - 20, X + 7, Y - 20, X, Y - 9, BLUE)]
    return svg_wrap(W, Y + 38, "".join(s),
                    "number line from 0 to %d with each whole split into %d equal parts and an arrow" % (L, d))


def letters_line_svg(L, d, pts, W=384):
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


# ============================================================ set 1: equivalent fractions with models
def set_models(rnd):
    SPOTS.left = []
    its = []
    for a, b, d in [(1, 2, 8), (1, 3, 6), (3, 4, 8), (2, 5, 10), (2, 3, 12), (5, 6, 12)]:
        n = d // b
        c = a * n
        q = (fig(two_bars_svg(b, a, d, c)) + "The bars are the same size and show the same amount.<br>%s = %s"
             % (fr(a, b), frq(d)))
        e = ("The bottom bar has %d equal parts, so each %s of the top bar is split into %d parts. "
             "%s become%s %d × %d = <b>%d</b> %s. So %s = %s."
             % (d, ONE[b], n, parts(a, b), "s" if a == 1 else "", a, n, c, WORD[d], fr(a, b), fr(c, d)))
        its.append(mcq(q, Nc(c), [Nc(a + (d - b)), Nc(a), Nc(d - c), Nc(c + 1), Nc(n)], e, rnd))

    for dens, (sd, k), t in [((2, 4, 8), (4, 3), 8), ((3, 6, 12), (3, 2), 12), ((5, 10), (5, 4), 10), ((2, 6, 12), (2, 1), 12)]:
        n = t // sd
        c = k * n
        q = (fig(wall_svg(dens, (sd, k))) + "Use the fraction wall. %s is shaded. How many %s are equal to %s?"
             % (fr(k, sd), WORD[t], fr(k, sd)))
        e = ("Look down the fraction wall. Each %s is the same as %d %s, so %s line%s up with %d × %d = <b>%d</b> %s. "
             "So %s = %s." % (ONE[sd], n, WORD[t], parts(k, sd), "s" if k == 1 else "", k, n, c, WORD[t], fr(k, sd), fr(c, t)))
        its.append(mcq(q, Nc(c), [Nc(k + (t - sd)), Nc(k), Nc(t - c), Nc(c + n), Nc(c + 1)], e, rnd))

    for n, k, g in [(12, 9, 3), (10, 4, 2), (8, 6, 2), (12, 10, 2), (9, 6, 3)]:
        sn, sd = k // g, n // g
        q = (fig(group_bar_svg(n, k, g)) + "%s of the bar is shaded. The thick lines make groups of %d. "
             "Which equivalent fraction does the bar show?" % (fr(k, n), g))
        e = ("There are %d groups and %d of them are shaded, so %s = <b>%s</b>. "
             "This is the same as dividing %d and %d by %d." % (sd, sn, fr(k, n), fr(sn, sd), k, n, g))
        cands = [Fc(sn, n), Fc(k - g, n - g), Fc(sd, sn), Fc(k, sd), Fc(sn + 1, sd), Fc(sn, sd + 1)]
        its.append(mcq(q, Fc(sn, sd), cands, e, rnd))

    for W, s, thing, one in [(3, 4, "pancakes", "pancake"), (2, 3, "granola bars", "granola bar"),
                             (4, 5, "sub sandwiches", "sub sandwich")]:
        e = ("Cut each of the %d %s into %d equal parts. Each person gets 1 part from every %s: %d × %s = <b>%s of a %s</b>. "
             "This is the same as %d ÷ %d." % (W, thing, s, one, W, fr(1, s), fr(W, s), one, W, s))
        q = (fig(share_svg(W, s)) + "%d %s are shared equally by %d friends. The shaded parts are one friend’s share. "
             "How much does each friend get?" % (W, thing, s))
        u = " of a " + one
        its.append(mcq(q, Fc(W, s, u), [Fc(s, W, u), Fc(1, s, u), Fc(1, W, u), Fc(W, W * s, u)], e, rnd))

    its.append(mcq("Which fraction is equivalent to %s?" % fr(1, 2), Fc(6, 12), [Fc(6, 7), Fc(5, 12), Fc(2, 1), Fc(1, 4)],
                   "Multiply the numerator and the denominator by 6: 1 × 6 = 6 and 2 × 6 = 12. So %s = <b>%s</b>. "
                   "Adding 5 to both (%s) does not keep the amount the same." % (fr(1, 2), fr(6, 12), fr(6, 7)), rnd))
    its.append(mcq("Which fraction is equivalent to %s?" % fr(3, 4), Fc(9, 12), [Fc(5, 6), Fc(6, 4), Fc(3, 8), Fc(6, 12)],
                   "Multiply the numerator and the denominator by 3: 3 × 3 = 9 and 4 × 3 = 12. So %s = <b>%s</b>. "
                   "%s adds 2 to both numbers, %s multiplies only the top, and %s multiplies only the bottom."
                   % (fr(3, 4), fr(9, 12), fr(5, 6), fr(6, 4), fr(3, 8)), rnd))
    assert len(its) == 20, len(its)
    return {"title": "Equivalent fractions with models", "items": its}


# ============================================================ set 2: missing numbers and simplest form
def simp_cands(a, b):
    g = math.gcd(a, b)
    sa, sb = a // g, b // g
    sub = a - sa
    return [Fc(sa, b - sub) if b - sub > sa else None, Fc(sa, b), Fc(a, sb), Fc(sb, sa),
            Fc(sa + 1, sb), Fc(sa, sb + 1), Fc(sa - 1, sb) if sa > 1 else None, Fc(1, sb) if sa > 1 else None]


def set_simplest(rnd):
    SPOTS.left = []
    its = []
    for a, b, d in [(2, 5, 10), (3, 4, 12), (2, 3, 9)]:
        n = d // b
        c = a * n
        e = ("Look at the denominators: %d × <b>%d</b> = %d. Multiply the numerator by %d too: %d × %d = <b>%d</b>. "
             "So %s = %s." % (b, n, d, n, a, n, c, fr(a, b), fr(c, d)))
        its.append(mcq("%s = %s" % (fr(a, b), frq(d)), Nc(c), [Nc(a + (d - b)), Nc(a), Nc(n), Nc(d - c), Nc(c + n)], e, rnd))
    a, b, c = 5, 6, 10
    its.append(mcq("%s = %s" % (fr(a, b), frq_d(c)), Nc(12), [Nc(11), Nc(6), Nc(60), Nc(2)],
                   "Look at the numerators: 5 × <b>2</b> = 10. Multiply the denominator by 2 too: 6 × 2 = <b>12</b>. "
                   "So %s = %s. Adding 5 to the top and the bottom (%s) does not keep the amount the same." % (fr(5, 6), fr(10, 12), fr(10, 11)), rnd))
    its.append(mcq("%s = %s" % (fr(8, 12), frq(3)), Nc(2), [Nc(8), Nc(4), Nc(3)],
                   "12 ÷ <b>4</b> = 3, so divide the numerator by 4 too: 8 ÷ 4 = <b>2</b>. So %s = %s."
                   % (fr(8, 12), fr(2, 3)), rnd))
    its.append(mcq("%s = %s" % (fr(10, 12), frq_d(5)), Nc(6), [Nc(7), Nc(12), Nc(2)],
                   "10 ÷ <b>2</b> = 5, so divide the denominator by 2 too: 12 ÷ 2 = <b>6</b>. So %s = %s. "
                   "Taking 5 from both (to get %s) changes the amount." % (fr(10, 12), fr(5, 6), fr(5, 7)), rnd))

    its.append(mcq("Which fraction is in simplest form?", fr(5, 8), [fr(4, 6), fr(6, 10), fr(3, 9)],
                   "%s is in simplest form, because no number except 1 divides both 5 and 8. The others can be divided: "
                   "%s = %s, %s = %s, %s = %s." % (fr(5, 8), fr(4, 6), fr(2, 3), fr(6, 10), fr(3, 5), fr(3, 9), fr(1, 3)), rnd))
    its.append(mcq("Which fraction is in simplest form?", fr(7, 12), [fr(9, 12), fr(2, 10), fr(4, 8)],
                   "%s is in simplest form: 7 and 12 have no common factor except 1. "
                   "%s = %s, %s = %s and %s = %s can all be simplified." % (fr(7, 12), fr(9, 12), fr(3, 4), fr(2, 10), fr(1, 5),
                                                                            fr(4, 8), fr(1, 2)), rnd))

    for a, b in [(6, 8), (4, 10), (3, 9), (8, 10), (6, 9), (4, 12), (2, 8), (9, 12), (10, 12), (8, 12)]:
        g = math.gcd(a, b)
        sa, sb = a // g, b // g
        e = ("%d is the greatest number that divides both %d and %d. %d ÷ %d = %d and %d ÷ %d = %d. So %s = <b>%s</b>."
             % (g, a, b, a, g, sa, b, g, sb, fr(a, b), fr(sa, sb)))
        if g == 4:
            e += " (Dividing by 2 gives %s, which can still be simplified.)" % fr(a // 2, b // 2)
        its.append(mcq("Write %s in simplest form." % fr(a, b), Fc(sa, sb), simp_cands(a, b), e, rnd))

    for (a, b), trues, bad in [((2, 3), [(4, 6), (6, 9), (8, 12)], (4, 5)), ((1, 2), [(2, 4), (3, 6), (6, 12)], (3, 4))]:
        for t in trues:
            assert F(*t) == F(a, b)
        assert F(*bad) != F(a, b)
        e = ("<b>%s</b> is not equivalent to %s: 2 was added to the numerator and the denominator, and adding changes "
             "the amount. The others are equivalent, because both numbers were multiplied by the same number."
             % (fr(*bad), fr(a, b)))
        its.append(mcq("Which fraction is <b>not</b> equivalent to %s?" % fr(a, b), fr(*bad), [fr(*t) for t in trues], e, rnd))
    assert len(its) == 20, len(its)
    return {"title": "Missing numbers and simplest form", "items": its}


# ============================================================ set 3: improper fractions and mixed numbers
def imp_cands(n, d):
    q, r = divmod(n, d)
    return [Mc(r, q, d) if q < d else None, Mc(q, r, n), Mc(q + 1, r, d), Mc(q, d - r, d), Mc(q - 1, r, d) if q > 1 else None,
            Fc(d, n), Mc(q, r + 1, d) if r + 1 < d else None]


def imp_e(n, d):
    q, r = divmod(n, d)
    return ("How many %ds are in %d? %d × %d = %d, so there are %d wholes. %d − %d = %d %s left over. So %s = <b>%s</b>."
            % (d, n, q, d, q * d, q, n, q * d, r, ONE[d] if r == 1 else WORD[d], fr(n, d), mx(q, r, d)))


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
    for d, N in [(4, 11), (3, 8), (5, 7)]:
        q, r = divmod(N, d)
        e = ("Each bar is 1 whole. %d bar%s full and %d more %s shaded in the last bar. So %s = <b>%s</b>."
             % (q, " is" if q == 1 else "s are", r, "part is" if r == 1 else "parts are", fr(N, d), mx(q, r, d)))
        its.append(mcq(fig(wholes_svg(d, N)) + "Each bar is 1 whole. %s are shaded. Write this as a mixed number." % fr(N, d),
                       Mc(q, r, d), [Fc(N, d * (q + 1))] + imp_cands(N, d), e, rnd))

    its.append(mcq(fig(share_svg(5, 4)) + "5 pancakes are shared equally by 4 friends. The shaded parts are one friend’s share. "
                   "How many pancakes does each friend get?",
                   Mc(1, 1, 4, " pancakes"), [Fc(4, 5, " of a pancake"), Fc(1, 4, " of a pancake"), Mc(1, 1, 5, " pancakes"),
                                              Mc(1, 4, 5, " pancakes")],
                   "Each friend gets %s of each of the 5 pancakes: 5 × %s = %s. 4 fourths make 1 whole, with 1 fourth left over. "
                   "So each friend gets <b>1 %s pancakes</b>." % (fr(1, 4), fr(1, 4), fr(5, 4), fr(1, 4)), rnd))

    # the other letters are at least 2 marks away, so the letters never crowd
    for t, L, d, cands in [(F(7, 4), 3, 4, [F(5, 4), F(9, 4), F(3, 4), F(11, 4), F(1, 4)]),
                           (F(13, 6), 3, 6, [F(10, 6), F(16, 6), F(7, 6), F(4, 6), F(1, 6)])]:
        its.append(nl_item(t, L, d, cands, rnd))

    for t, L, d in [(F(8, 3), 3, 3), (F(5, 2), 3, 2), (F(9, 4), 3, 4)]:
        w = int(t)
        r = int((t - w) * d)
        e = ("Each whole is split into %d equal parts, so each mark is %s. The arrow is %d mark%s after %d. "
             "So it shows <b>%s</b> (= %s)." % (d, fr(1, d), r, "" if r == 1 else "s", w, mx(w, r, d), fr(t.numerator, d)))
        its.append(mcq(fig(arrow_line_svg(L, d, t)) + "What number does the arrow show? Give a mixed number.",
                       Mc(w, r, d), [Mc(w, r, d * L), Mc(w + 1, r, d), Mc(w, d - r, d) if d - r != r else None,
                                     Mc(w - 1, r, d) if w > 1 else None, Mc(w, r + 1, d) if r + 1 < d else None,
                                     Fc(r, d), Mc(w, r, d + 1)], e, rnd))

    for n, d in [(13, 5), (17, 4), (19, 6), (23, 10), (29, 8), (25, 12)]:
        q, r = divmod(n, d)
        its.append(mcq("Write %s as a mixed number." % fr(n, d), Mc(q, r, d), imp_cands(n, d), imp_e(n, d), rnd))

    for w, n, d in [(2, 3, 5), (3, 1, 4), (4, 2, 3), (1, 7, 10), (5, 3, 8)]:
        its.append(mcq("Write %s as an improper fraction." % mx(w, n, d), Fc(w * d + n, d), mix_cands(w, n, d),
                       mix_e(w, n, d), rnd))
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

    for x, y in [((1, 8), (1, 4)), ((3, 5), (3, 10)), ((2, 3), (2, 9))]:
        its.append(which(x, y))
    its.append(which((2, 3), (7, 12), True))
    its.append(which((5, 8), (3, 4), True))
    for x, y in [((3, 5), (7, 10)), ((5, 6), (11, 12)), ((3, 4), (6, 8)), ((1, 2), (5, 12)), ((2, 3), (3, 4))]:
        its.append(which(x, y))

    # improper fractions and mixed numbers
    assert F(7, 4) > F(3, 2)
    its.append(mcq("Which is greater: %s or 1 %s?" % (fr(7, 4), fr(1, 2)), fr(7, 4), ["1 " + fr(1, 2), SAME, CANT],
                   "%s = 1 %s. Both have 1 whole. Compare the parts: %s = %s, and %s &gt; %s. So <b>%s</b> is greater."
                   % (fr(7, 4), fr(3, 4), fr(1, 2), fr(2, 4), fr(3, 4), fr(2, 4), fr(7, 4)), rnd))
    assert F(8, 3) > F(7, 3)
    its.append(mcq("Which is greater: 2 %s or %s?" % (fr(1, 3), fr(8, 3)), fr(8, 3), ["2 " + fr(1, 3), SAME, CANT],
                   "2 %s = 2 × 3 + 1 = %s. %s &gt; %s, so <b>%s</b> is greater. (%s = 2 %s.)"
                   % (fr(1, 3), fr(7, 3), fr(8, 3), fr(7, 3), fr(8, 3), fr(8, 3), fr(2, 3)), rnd))
    assert F(11, 5) == F(2) + F(1, 5)
    its.append(mcq("Which is greater: %s or 2 %s?" % (fr(11, 5), fr(1, 5)), SAME, [fr(11, 5), "2 " + fr(1, 5), CANT],
                   "%s: 5 × 2 = 10, with 1 fifth left over, so %s = 2 %s. <b>They are equal.</b>"
                   % (fr(11, 5), fr(11, 5), fr(1, 5)), rnd))

    for word, vs in [("greatest", [F(3, 4), F(5, 8), F(1, 2), F(3, 8)]),
                     ("smallest", [F(2, 3), F(5, 6), F(7, 12), F(5, 12)])]:
        best = max(vs) if word == "greatest" else min(vs)
        L = lcd(vs)
        e = ("Write them all with the denominator %d: %s. The %s is %s, so the answer is <b>%s</b>."
             % (L, ", ".join(eqL(v, L) for v in vs), word, over(best, L), show(best)))
        its.append(mcq("Which fraction is the %s?" % word, (show(best), best),
                       [(show(v), v) for v in vs if v != best], e, rnd))

    def s_of(seq):
        return ", ".join(show(v) for v in seq)
    for vs, up in [([F(3, 4), F(5, 8), F(1, 2)], True), ([F(2, 3), F(7, 12), F(5, 6)], True),
                   ([F(3, 10), F(1, 2), F(2, 5)], False)]:
        right = sorted(vs, reverse=not up)
        perms = [sorted(vs, key=lambda v: v.numerator), sorted(vs, key=lambda v: v.denominator),
                 sorted(vs, key=lambda v: -v.denominator), list(reversed(right))]
        perms += [list(p) for p in itertools.permutations(vs)]
        L = lcd(vs)
        e = ("Use the denominator %d: %s. So the order is <b>%s</b>."
             % (L, ", ".join(eqL(v, L) for v in vs), s_of(right)))
        its.append(mcq("Order from %s:<br>%s" % ("least to greatest" if up else "greatest to least", s_of(vs)),
                       s_of(right), [s_of(p) for p in perms if p != right], e, rnd))

    # order with improper fractions and mixed numbers
    vals = {"a": F(9, 4), "b": F(3, 2), "c": F(7, 3)}
    disp = {"a": fr(9, 4), "b": "1 " + fr(1, 2), "c": "2 " + fr(1, 3)}
    right = sorted(vals, key=lambda k: vals[k])
    assert right == ["b", "a", "c"]

    def j(ks):
        return ", ".join(disp[k] for k in ks)
    its.append(mcq("Order from least to greatest:<br>%s" % j(["a", "b", "c"]), j(right),
                   [j(p) for p in itertools.permutations("abc") if list(p) != right][::-1],
                   "%s = 2 %s. 1 %s has only 1 whole, so it is the least. Compare 2 %s and 2 %s in twelfths: "
                   "%s = %s and %s = %s. So the order is <b>%s</b>."
                   % (fr(9, 4), fr(1, 4), fr(1, 2), fr(1, 4), fr(1, 3), fr(1, 4), fr(3, 12), fr(1, 3), fr(4, 12), j(right)), rnd))

    assert F(1, 2) < F(5, 8) < F(3, 4)
    its.append(mcq("Which fraction is between %s and %s?" % (fr(1, 2), fr(3, 4)), Fc(5, 8), [Fc(7, 8), Fc(3, 8), Fc(5, 6)],
                   "In eighths: %s = %s and %s = %s. <b>%s</b> is between them. %s is less than %s. %s and %s are more than %s."
                   % (fr(1, 2), fr(4, 8), fr(3, 4), fr(6, 8), fr(5, 8), fr(3, 8), fr(1, 2), fr(7, 8), fr(5, 6), fr(3, 4)), rnd))
    assert len(its) == 20, len(its)
    return {"title": "Compare and order fractions", "items": its}


# ============================================================ set 5: word problems
def set_words(rnd):
    SPOTS.left = []
    its = []
    # 1
    its.append(mcq("A pizza is cut into 8 equal slices. Liam eats %s of it. How many slices does he eat?" % fr(3, 4),
                   Nc(6, " slices"), [Nc(3, " slices"), Nc(7, " slices"), Nc(4, " slices")],
                   "4 × 2 = 8, so %s = %s. Liam eats <b>6 slices</b>." % (fr(3, 4), fr(6, 8)), rnd))
    # 2
    its.append(mcq("A tray of 12 butter tarts is on the table. Maya’s family eats 9 of them. "
                   "What fraction of the tray is eaten, in simplest form?",
                   Fc(3, 4), [Fc(1, 4), Fc(4, 3), Fc(1, 3)],
                   "9 out of 12 = %s. Divide both numbers by 3: %s = <b>%s</b>." % (fr(9, 12), fr(9, 12), fr(3, 4)), rnd))
    # 3
    its.append(mcq("Mrs. Patel brings 3 loaves of banana bread for 4 tables. Each table gets an equal share. "
                   "How much banana bread does each table get?",
                   Fc(3, 4, " of a loaf"), [Fc(4, 3, " of a loaf"), Fc(1, 4, " of a loaf"), Fc(1, 3, " of a loaf")],
                   "Cut each loaf into 4 equal parts. Each table gets 1 part of each loaf: 3 × %s = <b>%s of a loaf</b>. "
                   "This is the same as 3 ÷ 4." % (fr(1, 4), fr(3, 4)), rnd))
    # 4
    its.append(mcq("5 friends share 7 sub sandwiches equally at a soccer tournament. How much does each friend get?",
                   Mc(1, 2, 5, " sandwiches"), [Fc(5, 7, " of a sandwich"), Mc(1, 2, 7, " sandwiches"),
                                                Mc(2, 2, 5, " sandwiches"), Mc(1, 1, 5, " sandwiches")],
                   "Each friend gets %s of each sandwich: 7 × %s = %s. 5 fifths make 1 whole, with 2 fifths left over. "
                   "So each friend gets <b>1 %s sandwiches</b>." % (fr(1, 5), fr(1, 5), fr(7, 5), fr(2, 5)), rnd))
    # 5
    assert F(3, 4) > F(2, 3)
    its.append(mcq("Group A: 2 pizzas are shared equally by 3 students. Group B: 3 pizzas are shared equally by 4 students. "
                   "In which group does each student get more pizza?",
                   "Group B", ["Group A", "They get the same", CANT],
                   "Group A: each student gets %s. Group B: each student gets %s. In twelfths: %s = %s and %s = %s. "
                   "So each student in <b>Group B</b> gets more." % (fr(2, 3), fr(3, 4), fr(2, 3), fr(8, 12), fr(3, 4), fr(9, 12)), rnd))
    # 6
    its.append(mcq("Olivia’s maple syrup jug holds %s L. Noah’s jug holds %s L. Whose jug holds more?" % (fr(3, 5), fr(7, 10)),
                   "Noah’s jug", ["Olivia’s jug", "They hold the same", CANT],
                   "Use tenths: %s = %s. 7 tenths is more than 6 tenths, so <b>Noah’s jug</b> holds more." % (fr(3, 5), fr(6, 10)), rnd))
    # 7
    its.append(mcq("Aiden says, “%s is greater than %s, because 8 is greater than 4.” Is he right?" % (fr(1, 8), fr(1, 4)),
                   "No. %s is less than %s" % (fr(1, 8), fr(1, 4)),
                   ["Yes. 8 is greater than 4", "No. They are equal", "Yes. Eighths are bigger than fourths"],
                   "A bigger denominator means the whole is cut into <b>more, smaller</b> parts. %s = %s, which is more than %s. "
                   "So %s is <b>less</b> than %s." % (fr(1, 4), fr(2, 8), fr(1, 8), fr(1, 8), fr(1, 4)), rnd))
    # 8
    its.append(mcq("Zoe changed %s into an equivalent fraction and wrote %s. What did she do wrong?" % (fr(2, 3), fr(4, 5)),
                   "She added 2 to the top and the bottom",
                   ["She multiplied both numbers by 2", "Nothing. She is right", "She multiplied only the numerator by 2"],
                   "2 + 2 = 4 and 3 + 2 = 5. Adding changes the amount. Multiply both numbers by 2 instead: %s = <b>%s</b>."
                   % (fr(2, 3), fr(4, 6)), rnd))
    # 9
    its.append(mcq("Ethan runs %s km in the Terry Fox Run. Write this distance as a mixed number." % fr(7, 4),
                   Mc(1, 3, 4, " km"), [Mc(3, 1, 4, " km"), Mc(1, 3, 7, " km"), Mc(1, 4, 7, " km"), Mc(2, 3, 4, " km")],
                   "4 fourths make 1 km. 7 − 4 = 3 fourths are left over. So %s km = <b>1 %s km</b>." % (fr(7, 4), fr(3, 4)), rnd))
    # 10
    its.append(mcq("Each glass holds %s L of milk. Chloe fills 9 glasses. How much milk is that, as a mixed number?" % fr(1, 4),
                   Mc(2, 1, 4, " L"), [Mc(9, 1, 4, " L"), Mc(2, 1, 9, " L"), Mc(2, 3, 4, " L"), Mc(3, 1, 4, " L")],
                   "9 glasses of %s L = %s L. 4 fourths make 1 L, so 8 fourths make 2 L, with 1 fourth left over: "
                   "<b>2 %s L</b>." % (fr(1, 4), fr(9, 4), fr(1, 4)), rnd))
    # 11
    its.append(mcq("Arjun says 2 %s = %s. What is the correct improper fraction?" % (fr(3, 5), fr(6, 5)),
                   Fc(13, 5), [Fc(6, 5), Fc(23, 5), Fc(13, 10), Fc(11, 5)],
                   "Arjun multiplied 2 × 3. Instead, 2 wholes = 2 × 5 = 10 fifths. Add 3 fifths: 10 + 3 = 13. So 2 %s = <b>%s</b>."
                   % (fr(3, 5), fr(13, 5)), rnd))
    # 12
    rib = [("Mateo", F(3, 4)), ("Hana", F(7, 8)), ("Kai", F(5, 8)), ("Sofia", F(1, 2))]
    assert max(rib, key=lambda x: x[1])[0] == "Hana"
    its.append(mcq("Four students measure their ribbons. Mateo: %s m. Hana: %s m. Kai: %s m. Sofia: %s m. "
                   "Who has the longest ribbon?" % (fr(3, 4), fr(7, 8), fr(5, 8), fr(1, 2)),
                   "Hana", ["Mateo", "Kai", "Sofia"],
                   "Use eighths: %s = %s, %s, %s, %s = %s. The longest is <b>Hana’s</b> ribbon."
                   % (fr(3, 4), fr(6, 8), fr(7, 8), fr(5, 8), fr(1, 2), fr(4, 8)), rnd))
    # 13
    its.append(mcq("Priya’s family paddles 2 %s km on a canoe trip. How many half kilometres is that?" % fr(1, 2),
                   Nc(5, " halves"), [Nc(3, " halves"), Nc(4, " halves"), Nc(6, " halves")],
                   "2 km = 2 × 2 = 4 halves. Add 1 more half: 4 + 1 = <b>5 halves</b>. So 2 %s km = %s km."
                   % (fr(1, 2), fr(5, 2)), rnd))
    # 14
    its.append(mcq("Students eat 19 slices of pizza on a field trip. Each pizza is cut into 6 equal slices. "
                   "How many pizzas do they eat?",
                   Mc(3, 1, 6, " pizzas"), [Mc(1, 3, 6, " pizzas"), Mc(3, 1, 19, " pizzas"), Mc(4, 1, 6, " pizzas"),
                                            Mc(3, 5, 6, " pizzas")],
                   "6 slices make 1 pizza. 3 × 6 = 18, and 19 − 18 = 1 slice is left. So %s = <b>3 %s pizzas</b>."
                   % (fr(19, 6), fr(1, 6)), rnd))
    # 15
    pots = [("Grade 5A", F(5, 6)), ("Grade 5B", F(7, 12)), ("Grade 5C", F(2, 3))]
    assert min(pots, key=lambda x: x[1])[0] == "Grade 5B"
    its.append(mcq("Three classes each have the same size pot of paint for a mural. Grade 5A uses %s of its pot, Grade 5B uses %s "
                   "and Grade 5C uses %s. Which class uses the least paint?" % (fr(5, 6), fr(7, 12), fr(2, 3)),
                   "Grade 5B", ["Grade 5A", "Grade 5C", "They all use the same"],
                   "Use twelfths: %s = %s, %s, %s = %s. The smallest is %s, so <b>Grade 5B</b> uses the least. "
                   "12 is the biggest denominator, but that does not make it the biggest fraction."
                   % (fr(5, 6), fr(10, 12), fr(7, 12), fr(2, 3), fr(8, 12), fr(7, 12)), rnd))
    # 16
    its.append(mcq("Emma gets %s on a spelling quiz. Owen gets %s on the same quiz. Who did better?" % (fr(7, 10), fr(4, 5)),
                   "Owen", ["Emma", "They did the same", CANT],
                   "Use tenths: %s = %s. 8 is more than 7, so <b>Owen</b> did better." % (fr(4, 5), fr(8, 10)), rnd))
    # 17
    assert F(3, 2) > F(5, 4)
    its.append(mcq("Nathan practises hockey for 1 %s hours. Benjamin practises for %s hours. Who practises longer?"
                   % (fr(1, 2), fr(5, 4)),
                   "Nathan", ["Benjamin", "They practise the same time", CANT],
                   "%s = 1 %s. Both have 1 whole hour. Compare the parts: %s = %s, which is more than %s. "
                   "So <b>Nathan</b> practises longer." % (fr(5, 4), fr(1, 4), fr(1, 2), fr(2, 4), fr(1, 4)), rnd))
    # 18
    its.append(mcq("4 friends at the cottage share 6 granola bars equally. How many granola bars does each friend get?",
                   Mc(1, 1, 2, " bars"), [Fc(4, 6, " of a bar"), Mc(1, 2, 6, " bars"), Mc(1, 1, 4, " bars"), Mc(2, 1, 2, " bars")],
                   "Each friend gets 6 ÷ 4 = %s bars. 4 fourths make 1 whole, with 2 fourths left over: 1 %s = <b>1 %s bars</b>."
                   % (fr(6, 4), fr(2, 4), fr(1, 2)), rnd))
    # 19
    its.append(mcq("A maple cookie recipe needs 2 %s cups of flour. Leah only has a %s cup scoop. How many scoops does she need?"
                   % (fr(1, 4), fr(1, 4)),
                   Nc(9, " scoops"), [Nc(3, " scoops"), Nc(8, " scoops"), Nc(6, " scoops")],
                   "1 cup = 4 fourths, so 2 cups = 8 fourths. Add 1 more fourth: 8 + 1 = <b>9 scoops</b>. "
                   "So 2 %s = %s." % (fr(1, 4), fr(9, 4)), rnd))
    # 20
    its.append(mcq("Jayden has a board %s m long. He says it is longer than 2 m. Is he right?" % fr(9, 4),
                   "Yes. %s m = 2 %s m" % (fr(9, 4), fr(1, 4)),
                   ["No. %s m = %s m" % (fr(9, 4), fr(4, 9)), "No. It is exactly 2 m", "No. %s m = 1 %s m" % (fr(9, 4), fr(1, 4))],
                   "4 fourths make 1 m, so 8 fourths make 2 m. 9 − 8 = 1 fourth is left over. "
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
        "<figcaption>The bars are the same size. " + fr(3, 4) + " = " + fr(9, 12) + ": each fourth is split into 3.</figcaption></figure>"
        + ex("Example", fr(3, 4) + " = " + frq(12),
             "4 × 3 = 12, so multiply the numerator by 3 too: 3 × 3 = 9.", fr(9, 12))
        + "<h2>Simplest form</h2>"
        "<p>A fraction is in <b>simplest form</b> when no number except 1 divides both the numerator and the denominator. "
        "Divide both by the greatest number you can.</p>"
        + ex("Example", "Write " + fr(8, 12) + " in simplest form.",
             "4 divides both 8 and 12. 8 ÷ 4 = 2 and 12 ÷ 4 = 3.", fr(2, 3))
        + "<h2>Sharing wholes</h2>"
        "<p>When some wholes are shared equally, each person gets <b>wholes ÷ people</b>. "
        "3 pancakes shared by 4 friends: each friend gets " + fr(3, 4) + " of a pancake.</p>"
        "<figure class='sn-fig'>" + share_svg(3, 4) +
        "<figcaption>Cut each pancake into 4. One friend gets 1 part of each pancake: " + fr(3, 4) + ".</figcaption></figure>"
        + "<h2>Improper fractions and mixed numbers</h2>"
        "<p>An <b>improper fraction</b> such as " + fr(11, 4) + " is greater than 1. "
        "A <b>mixed number</b> such as 2 " + fr(3, 4) + " shows the same amount as wholes and a fraction.</p>"
        "<figure class='sn-fig'>" + wholes_svg(4, 11) +
        "<figcaption>" + fr(11, 4) + " = 2 wholes and 3 more fourths = 2 " + fr(3, 4) + ".</figcaption></figure>"
        + ex("Example", "Write " + fr(17, 5) + " as a mixed number.",
             "There are three 5s in 17 (15), with 2 left over.", "3 " + fr(2, 5))
        + ex("Example", "Write 2 " + fr(3, 5) + " as an improper fraction.",
             "2 wholes = 2 × 5 = 10 fifths. Add 3 fifths: 10 + 3 = 13.", fr(13, 5))
        + "<h2>Comparing and ordering</h2>"
        "<p>Give the fractions the <b>same denominator</b>, then compare the numerators. "
        "If the numerators are the same, the fraction with the <b>smaller</b> denominator is greater, because its parts are bigger.</p>"
        "<figure class='sn-fig'>" + two_bars_svg(3, 2, 12, 7) +
        "<figcaption>" + fr(2, 3) + " = " + fr(8, 12) + ", which is more than " + fr(7, 12) + ".</figcaption></figure>"
        + ex("Example", "Order " + fr(3, 4) + ", " + fr(5, 8) + " and " + fr(1, 2) + " from least to greatest.",
             "Use eighths: " + fr(3, 4) + " = " + fr(6, 8) + ", " + fr(5, 8) + ", " + fr(1, 2) + " = " + fr(4, 8) + ".",
             fr(1, 2) + ", " + fr(5, 8) + ", " + fr(3, 4))
        + ex("Example", "Which is greater: " + fr(7, 4) + " or 1 " + fr(1, 2) + "?",
             fr(7, 4) + " = 1 " + fr(3, 4) + ". Both have 1 whole, and " + fr(3, 4) + " &gt; " + fr(2, 4) + ".", fr(7, 4))
        + "<h2>Common mistakes</h2>"
        + table(["Mistake", "What to do instead"], [
            ["Adding the same number to the top and bottom: " + fr(2, 3) + " = " + fr(4, 5),
             "Multiply or divide, never add: " + fr(2, 3) + " = " + fr(4, 6)],
            ["Thinking a bigger denominator means a bigger fraction: " + fr(1, 8) + " &gt; " + fr(1, 4),
             "A bigger denominator means <b>smaller</b> parts: " + fr(1, 8) + " &lt; " + fr(1, 4)],
            ["Multiplying only the numerator: " + fr(2, 3) + " = " + fr(4, 3),
             "Multiply both: " + fr(2, 3) + " = " + fr(4, 6)],
            ["2 " + fr(3, 5) + " = " + fr(6, 5),
             "Wholes × denominator, then add the numerator: 2 × 5 + 3 = 13, so " + fr(13, 5)],
        ])
    )


FAQ = [
    {"q": "What do Grade 5 students learn about fractions in Ontario?",
     "a": "In the Ontario Grade 5 math curriculum, students use drawings and models to find equivalent fractions from halves to twelfths, work with improper fractions and mixed numbers, and compare and order fractions. They also model sharing several wholes equally, such as 3 pancakes shared by 4 friends."},
    {"q": "How do you find an equivalent fraction?",
     "a": "Multiply or divide the numerator and the denominator by the same number. For example, 3/4 = 9/12 (both × 3) and 8/12 = 2/3 (both ÷ 4). Adding the same number to both does not work."},
    {"q": "How do you change an improper fraction to a mixed number?",
     "a": "Divide the numerator by the denominator. The answer is the number of wholes and the remainder is the new numerator, so 17/5 = 3 2/5. To go back, multiply the wholes by the denominator and add the numerator: 3 × 5 + 2 = 17."},
    {"q": "How do you compare fractions with different denominators?",
     "a": "Change them so both have the same denominator, then compare the numerators. For 2/3 and 7/12, 2/3 = 8/12, so 2/3 is greater. A bigger denominator alone does not mean a bigger fraction: 1/8 is less than 1/4."},
]


def gen():
    rnd = random.Random(45806)
    SPOTS.left = []
    sets = [set_models(rnd), set_simplest(rnd), set_mixed(rnd), set_compare(rnd), set_words(rnd)]
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
        "country": "ca-on", "subject": "math", "grade": "grade-5", "slug": SLUG, "sort": 6,
        "updated": UPDATED, "pdf_url": "",
        "title": "Equivalent Fractions and Mixed Numbers",
        "seo_title": "Grade 5 Equivalent Fractions and Mixed Numbers Worksheets (Ontario Math): Free with Answer Key",
        "short_title": "Equivalent fractions and mixed numbers",
        "domain": "Number",
        "standard_code": "Grade 5: B1.3",
        "standard_url": "https://www.dcp.edu.gov.on.ca/en/curriculum/elementary-mathematics",
        "standard_text": "Use drawings and models to represent, compare, and order fractions representing the individual portions that result from multiple wholes being shared by any number of sharers, and equivalent fractions from halves to twelfths, including improper fractions and mixed numbers",
        "meta_desc": "Free Grade 5 math worksheets on equivalent fractions and mixed numbers for the Ontario curriculum: fraction bars and walls, sharing wholes, simplest form, improper fractions, comparing and ordering fractions to twelfths, and word problems. 100 questions with an answer key.",
        "key_big": "Equivalent fractions: multiply or divide the top and the bottom by the same number.",
        "key_sub": "3/4 = 9/12 (× 3) and 8/12 = 2/3 (÷ 4). 11/4 = 2 3/4, because there are two 4s in 11 with 3 left over. A bigger denominator means smaller parts: 1/8 < 1/4.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, SLUG + ".json")
    mark_large(u, "(number line|bars of|fraction bar|two fraction bars|fraction wall)")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(u, f, ensure_ascii=False, indent=1)
    print("wrote", path)
