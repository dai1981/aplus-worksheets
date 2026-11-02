# -*- coding: utf-8 -*-
"""
Canada (British Columbia) Grade 6 Math: Improper fractions and mixed numbers
(BC Mathematics Curriculum K-9 — Grade 6, Number: "improper fractions and mixed numbers")
  python3 tools/gen_cabc_math_g6_fractions.py
Improper fractions with bar and circle models, mixed numbers (models, number lines, writing them correctly),
converting both ways (including whole-number answers), comparing and ordering improper fractions and
mixed numbers, and number lines and word problems in BC contexts.
Every choice carries its value; a wrong choice never equals the right value or another wrong one.
Every conversion, comparison and order is checked in code with exact fractions.
Canadian English. HTML attributes use single quotes (no backslashes in the JSON).
"""
import json, math, os, random, re, itertools
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "ca-bc", "math", "grade-6")
SLUG = "improper-fractions-and-mixed-numbers"
UPDATED = "2026-11-02"
FILL = "#4fae74"
BLUE = "#2f6fc0"
LINE = "#2b2b2b"
FONT = "Arial, Helvetica, sans-serif"
CANT = "You can’t tell"
SAME = "They are equal"
WORD = {2: "halves", 3: "thirds", 4: "fourths", 5: "fifths", 6: "sixths", 7: "sevenths", 8: "eighths",
        9: "ninths", 10: "tenths", 12: "twelfths"}
ONE = {2: "half", 3: "third", 4: "fourth", 5: "fifth", 6: "sixth", 7: "seventh", 8: "eighth", 9: "ninth",
       10: "tenth", 12: "twelfth"}
NUMW = {2: "two", 3: "three", 4: "four", 5: "five", 6: "six", 7: "seven", 8: "eight", 9: "nine"}


# ------------------------------------------------------------ numbers
def fr(a, b):
    return "<span class='fr'><span class='fn'>%s</span><span class='fd'>%s</span></span>" % (a, b)


def frq(b):
    return fr("<b>?</b>", b)


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


def mixed(v, d=None):
    """Mixed number of v; d keeps an unsimplified denominator."""
    d = d or v.denominator
    n = v * d
    assert n.denominator == 1
    q, r = divmod(n.numerator, d)
    return mx(q, r, d)


def eqL(h, v, L):
    """'h = n/L', or just h when h already is that fraction."""
    t = fr((v * L).numerator, L)
    return h if h == t else "%s = %s" % (h, t)


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
def bars_svg(d, N, maxw=392, H=38, gap=14):
    """Bars of d equal parts side by side (each bar is 1 whole), N parts shaded in order."""
    nb = -(-N // d)
    cell = min(30.0, (maxw - 8 - (nb - 1) * gap) / float(nb * d))
    bw = cell * d
    s = []
    for b in range(nb):
        x0 = 4 + b * (bw + gap)
        on = min(d, N - b * d)
        for i in range(d):
            s.append("<rect x='%.1f' y='4' width='%.2f' height='%d' fill='%s' stroke='%s' stroke-width='2.5'/>"
                     % (x0 + i * cell, cell, H, FILL if i < on else "#fff", LINE))
        s.append("<rect x='%.1f' y='4' width='%.1f' height='%d' fill='none' stroke='%s' stroke-width='3'/>" % (x0, bw, H, LINE))
    return svg_wrap(8 + nb * bw + (nb - 1) * gap, H + 8, "".join(s),
                    "bars of %d equal parts, %d bars, %d parts shaded" % (d, nb, N))


def circles_svg(d, N, R=30, gap=14):
    """Circles of d equal sectors side by side (each circle is 1 whole), N sectors shaded in order."""
    nc = -(-N // d)
    s = []
    for c in range(nc):
        cx = 4 + R + c * (2 * R + gap)
        cy = 4 + R
        on = min(d, N - c * d)
        if on == d:
            s.append("<circle cx='%.1f' cy='%.1f' r='%d' fill='%s'/>" % (cx, cy, R, FILL))
        else:
            for i in range(on):
                a0 = -math.pi / 2 + 2 * math.pi * i / d
                a1 = -math.pi / 2 + 2 * math.pi * (i + 1) / d
                s.append("<path d='M%.2f %.2f L%.2f %.2f A%d %d 0 0 1 %.2f %.2f Z' fill='%s'/>"
                         % (cx, cy, cx + R * math.cos(a0), cy + R * math.sin(a0), R, R,
                            cx + R * math.cos(a1), cy + R * math.sin(a1), FILL))
        for i in range(d):
            a = -math.pi / 2 + 2 * math.pi * i / d
            s.append("<line x1='%.2f' y1='%.2f' x2='%.2f' y2='%.2f' stroke='%s' stroke-width='2'/>"
                     % (cx, cy, cx + R * math.cos(a), cy + R * math.sin(a), LINE))
        s.append("<circle cx='%.1f' cy='%.1f' r='%d' fill='none' stroke='%s' stroke-width='3'/>" % (cx, cy, R, LINE))
    return svg_wrap(8 + nc * 2 * R + (nc - 1) * gap, 2 * R + 8, "".join(s),
                    "circles of %d equal parts, %d circles, %d parts shaded" % (d, nc, N))


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


# ------------------------------------------------------------ shared wrong answers and explanations
def imp_cands(n, d, rnd=None):
    """Wrong mixed numbers for n/d, from real mistakes (7/4 = 1 3/7 first)."""
    q, r = divmod(n, d)
    c = [Mc(q, r, n), Mc(r, q, d) if 0 < q < d and r > 0 else None, Mc(q, d - r, d) if r and d - r != r else None,
         Mc(q + 1, r, d), Mc(q - 1, r, d) if q > 1 else None, Mc(q, r + 1, d) if r + 1 < d else None, Fc(d, n)]
    return c


def imp_e(n, d):
    q, r = divmod(n, d)
    if r == 0:
        return ("How many %ds are in %d? %d × %d = %d, with nothing left over. So %s = <b>%d</b> wholes."
                % (d, n, q, d, n, fr(n, d), q))
    return ("How many groups of %d are in %d? %d × %d = %d, so there %s <b>%d</b> whole%s. %d − %d = %d %s left over. "
            "The denominator stays %d. So %s = <b>%s</b>."
            % (d, n, q, d, q * d, "is" if q == 1 else "are", q, "" if q == 1 else "s", n, q * d, r, ONE[d] if r == 1 else WORD[d], d, fr(n, d), mx(q, r, d)))


def mix_e(w, n, d):
    return ("Each whole is %s, so %d whole%s %d × %d = %d %s. Add the %d: %d + %d = %d. So %s = <b>%s</b>."
            % (fr(d, d), w, " is" if w == 1 else "s are", w, d, w * d, WORD[d], n, w * d, n, w * d + n,
               mx(w, n, d), fr(w * d + n, d)))


def mix_cands(w, n, d):
    return [Fc(w * n, d), Fc(10 * w + n, d) if w < 10 else None, Fc(w * n + d, d), Fc(w + n, d),
            Fc(w * d, d), Fc(w * d + n, w * d), Fc(w * d + n + 1, d)]


# ============================================================ set 1: improper fractions with models
def set_models(rnd):
    SPOTS.left = []
    its = []
    for d, N in [(4, 7), (3, 5), (6, 11), (5, 13), (8, 19), (2, 5)]:
        nb = -(-N // d)
        e = ("Each bar is 1 whole cut into %d equal parts, so each part is %s. Count the shaded parts in all the bars: "
             "<b>%d</b>. So <b>%s</b> is shaded. The denominator is %d (parts in <b>one</b> whole), not %d (parts in all the bars)."
             % (d, fr(1, d), N, fr(N, d), d, nb * d))
        q = fig(bars_svg(d, N)) + "Each bar is 1 whole. What improper fraction is shaded?"
        cands = [Fc(N, nb * d), Fc(d, N), Fc(N - d, d), Fc(N, nb * d - N), Fc(nb * d - N, d)]
        its.append(mcq(q, Fc(N, d), cands, e, rnd))

    for d, N in [(4, 9), (3, 7), (6, 13), (8, 11), (2, 7)]:
        nc = -(-N // d)
        e = ("Each circle is 1 whole cut into %d equal parts. %d parts are shaded, so the amount is <b>%s</b>. "
             "Use the parts in one circle (%d) as the denominator." % (d, N, fr(N, d), d))
        q = fig(circles_svg(d, N)) + "Each circle is 1 whole. What improper fraction is shaded?"
        cands = [Fc(N, nc * d), Fc(d, N), Fc(N - d, d), Fc(nc * d - N, d), Fc(N, nc * d - N)]
        its.append(mcq(q, Fc(N, d), cands, e, rnd))

    for right, others in [((7, 5), [(5, 7), (3, 8), (4, 9)]), ((11, 6), [(6, 11), (5, 6), (9, 10)]),
                          ((9, 2), [(2, 9), (1, 2), (7, 8)])]:
        assert F(*right) > 1 and all(F(*o) < 1 for o in others)
        e = ("In an improper fraction the numerator is greater than the denominator, so it is more than 1 whole. "
             "%d &gt; %d, so <b>%s</b> is improper. The others are less than 1." % (right[0], right[1], fr(*right)))
        its.append(mcq("Which fraction is an improper fraction?", fr(*right), [fr(*o) for o in others], e, rnd))

    for w, d in [(3, 5), (4, 6), (5, 8)]:
        e = ("Each whole is %s. %d wholes are %d × %d = <b>%d</b> %s. So %d = %s."
             % (fr(d, d), w, w, d, w * d, WORD[d], w, fr(w * d, d)))
        its.append(mcq("%d wholes = %s" % (w, frq(d)), Nc(w * d), [Nc(w + d), Nc(10 * w + d), Nc(w), Nc(d)], e, rnd))

    for w, n, d in [(2, 3, 4), (3, 2, 5), (1, 5, 6)]:
        N = w * d + n
        e = ("The full bars are %d × %d = %d %s. Add the %d shaded parts in the last bar: %d + %d = <b>%d</b>. "
             "So %d whole%s and %s = %s." % (w, d, w * d, WORD[d], n, w * d, n, N, w, "" if w == 1 else "s",
                                            parts(n, d), fr(N, d)))
        q = (fig(bars_svg(d, N)) + "Each bar is 1 whole. There %s %d full bar%s and %s more. "
             "How many %s are shaded?" % ("is" if w == 1 else "are", w, "" if w == 1 else "s", parts(n, d), WORD[d]))
        its.append(mcq(q, Nc(N), [Nc(w + n), Nc(w * n), Nc((w + 1) * d), Nc(N - 1), Nc(w * d)], e, rnd))
    assert len(its) == 20, len(its)
    return {"title": "Improper fractions with models", "items": its}


# ============================================================ set 2: mixed numbers
def set_mixed(rnd):
    SPOTS.left = []
    its = []
    for w, n, d, wrongs in [(3, 2, 5, [Mc(2, 3, 5), Mc(3, 5, 2), Mc(2, 5, 3), Fc(32, 5)]),
                            (2, 5, 8, [Mc(5, 2, 8), Mc(2, 8, 5), Mc(8, 2, 5), Fc(25, 8)]),
                            (4, 1, 6, [Mc(1, 4, 6), Mc(4, 1, 4), Fc(41, 6), Mc(6, 1, 4)])]:
        e = ("“%s and %s %s” has %d wholes and the fraction %s. So it is written <b>%s</b>."
             % (NUMW[w].capitalize(), "one" if n == 1 else NUMW[n], ONE[d] if n == 1 else WORD[d], w, fr(n, d), mx(w, n, d)))
        q = "Which mixed number is “%s and %s %s”?" % (NUMW[w], "one" if n == 1 else NUMW[n], ONE[d] if n == 1 else WORD[d])
        its.append(mcq(q, Mc(w, n, d), wrongs, e, rnd))

    for d, N in [(3, 10), (5, 9), (6, 17), (4, 13), (8, 21)]:
        q, r = divmod(N, d)
        e = ("Each bar is 1 whole. %d bar%s full and %d more %s shaded in the last bar. So %s = <b>%s</b>."
             % (q, " is" if q == 1 else "s are", r, "part is" if r == 1 else "parts are", fr(N, d), mx(q, r, d)))
        nb = q + 1
        its.append(mcq(fig(bars_svg(d, N)) + "Each bar is 1 whole. Write the shaded amount as a mixed number.",
                       Mc(q, r, d), [Mc(q, r, nb * d), Mc(nb, r, d), Mc(q, d - r, d) if d - r != r else None,
                                     Mc(q, r, N)] + imp_cands(N, d), e, rnd))

    for d, N in [(4, 11), (3, 8), (5, 12), (2, 7)]:
        q, r = divmod(N, d)
        e = ("Each circle is 1 whole. %d circle%s full. The last circle has %s shaded. So the amount is <b>%s</b> (= %s)."
             % (q, " is" if q == 1 else "s are", parts(r, d), mx(q, r, d), fr(N, d)))
        nc = q + 1
        its.append(mcq(fig(circles_svg(d, N)) + "Each circle is 1 whole. Write the shaded amount as a mixed number.",
                       Mc(q, r, d), [Mc(q, d - r, d) if d - r != r else None, Mc(q, r, nc * d), Mc(nc, r, d),
                                     Mc(q, r, N)] + imp_cands(N, d), e, rnd))

    for t, L, d in [(F(7, 3), 3, 3), (F(13, 4), 4, 4), (F(17, 5), 4, 5), (F(11, 6), 3, 6), (F(19, 8), 3, 8)]:
        w = int(t)
        r = int((t - w) * d)
        e = ("Each whole is split into %d equal parts, so each mark is %s. The arrow is %d mark%s after %d. "
             "So it shows <b>%s</b> (= %s)." % (d, fr(1, d), r, "" if r == 1 else "s", w, mx(w, r, d), fr(t.numerator, d)))
        its.append(mcq(fig(arrow_line_svg(L, d, t)) + "What number does the arrow show? Give a mixed number.",
                       Mc(w, r, d), [Mc(w, r, d * L), Mc(w + 1, r, d), Mc(w, d - r, d) if d - r != r else None,
                                     Mc(w, r + 1, d) if r + 1 < d else None, Mc(w - 1, r, d) if w > 1 else None,
                                     Fc(r, d), Mc(w, r, d + 1)], e, rnd))

    # a mixed number's fraction part must be less than 1
    for w, n, d in [(2, 7, 4), (3, 8, 5), (1, 11, 6)]:
        q, r = divmod(n, d)
        right = Mc(w + q, r, d)
        e = ("The fraction part %s is more than 1 whole: %s = 1 %s. Add that 1 to the %d whole%s: %d + 1 = %d. "
             "So the mixed number is <b>%s</b>." % (fr(n, d), fr(n, d), fr(r, d), w, "" if w == 1 else "s", w, w + 1, mx(w + q, r, d)))
        assert F(w) + F(n, d) == right[1]
        its.append(mcq("Mia wrote %d %s. The fraction part should be less than 1. Write it correctly as a mixed number."
                       % (w, fr(n, d)), right,
                       [Mc(w, r, d), Mc(w + n, r, d), Mc(w + q, n, d), Mc(w, d, n) if d < n else None,
                        Mc(w + q, r, n)], e, rnd))
    assert len(its) == 20, len(its)
    return {"title": "Mixed numbers", "items": its}


# ============================================================ set 3: convert both ways
def set_convert(rnd):
    SPOTS.left = []
    its = []
    for n, d in [(7, 4), (23, 6), (31, 8), (29, 12), (38, 9), (53, 7), (47, 10)]:
        q, r = divmod(n, d)
        e = imp_e(n, d)
        if (n, d) == (7, 4):
            e += " (Not 1 %s: the parts are still fourths.)" % fr(3, 7)
        its.append(mcq("Write %s as a mixed number." % fr(n, d), Mc(q, r, d), imp_cands(n, d), e, rnd))

    for n, d in [(24, 6), (45, 9)]:
        q = n // d
        its.append(mcq("Write %s as a whole number or a mixed number." % fr(n, d), Nc(q),
                       [Nc(n - d), Nc(n + d), Fc(d, n), Mc(q - 1, 1, d), Nc(q + 1)], imp_e(n, d), rnd))

    for w, n, d in [(2, 3, 5), (3, 1, 4), (4, 5, 6), (5, 2, 3), (6, 3, 8), (2, 4, 9), (3, 7, 12)]:
        its.append(mcq("Write %s as an improper fraction." % mx(w, n, d), Fc(w * d + n, d), mix_cands(w, n, d),
                       mix_e(w, n, d), rnd))

    # missing numbers
    its.append(mcq("3 %s = %s" % (fr(2, 5), frq(5)), Nc(17), [Nc(6), Nc(32), Nc(15), Nc(11)],
                   "3 wholes = 3 × 5 = 15 fifths. 15 + 2 = <b>17</b>. So 3 %s = %s." % (fr(2, 5), fr(17, 5)), rnd))
    its.append(mcq("%s = 7 %s" % (fr(29, 4), frq(4)), Nc(1), [Nc(3), Nc(2), Nc(5)],
                   "7 × 4 = 28. 29 − 28 = <b>1</b> fourth is left over. So %s = 7 %s." % (fr(29, 4), fr(1, 4)), rnd))
    its.append(mcq("%s = 4 %s" % (frq(6), fr(5, 6)), Nc(29), [Nc(20), Nc(45), Nc(15), Nc(24)],
                   "4 wholes = 4 × 6 = 24 sixths. 24 + 5 = <b>29</b>. So %s = 4 %s." % (fr(29, 6), fr(5, 6)), rnd))
    its.append(mcq("%s = <b>?</b> %s" % (fr(43, 8), fr(3, 8)), Nc(5), [Nc(4), Nc(6), Nc(40)],
                   "5 × 8 = 40 and 43 − 40 = 3. So there are <b>5</b> wholes: %s = 5 %s." % (fr(43, 8), fr(3, 8)), rnd))
    assert len(its) == 20, len(its)
    return {"title": "Convert both ways", "items": its}


# ============================================================ set 4: compare and order
def set_compare(rnd):
    SPOTS.left = []
    its = []

    def as_mixed_e(v):
        return "%s = %s" % (fr(v.numerator, v.denominator), mixed(v))

    def which(x, y, e):
        """x, y are (html, value)."""
        X, Y = x[1], y[1]
        right = SAME if X == Y else (x[0] if X > Y else y[0])
        return mcq("Which is greater: %s or %s?" % (x[0], y[0]), right, [x[0], y[0], SAME, CANT], e, rnd)

    # same denominator
    for imp, mix in [((11, 4), (2, 1, 4)), ((17, 5), (3, 3, 5)), ((13, 3), (4, 1, 3)), ((22, 7), (3, 2, 7))]:
        x, y = Fc(*imp), Mc(*mix)
        X, Y = x[1], y[1]
        w, n, d = mix
        e = "Change the mixed number: %s = %d × %d + %d = %s. " % (mx(*mix), w, d, n, fr(w * d + n, d))
        if X == Y:
            e += "Both are %s, so <b>they are equal</b>." % fr(imp[0], d)
        else:
            e += "%d &%s; %d, so <b>%s</b> is greater." % (imp[0], "gt" if X > Y else "lt", w * d + n,
                                                          x[0] if X > Y else y[0])
        its.append(which(x, y, e))

    # different denominators
    for x, y in [(Fc(7, 3), Mc(2, 1, 4)), (Fc(11, 8), Mc(1, 1, 2)), (Mc(3, 2, 5), Fc(17, 6)), (Fc(14, 5), Mc(2, 3, 4))]:
        X, Y = x[1], y[1]
        assert X != Y
        mxs = []
        for h, v in (x, y):
            mxs.append(as_mixed_e(v) if "fd'>" in h and not re.match(r"\d", h) else mixed(v))
        if int(X) != int(Y):
            e = ("%s and %s. Compare the wholes first: %d &%s; %d, so <b>%s</b> is greater."
                 % (mxs[0], mxs[1], int(X), "gt" if X > Y else "lt", int(Y), x[0] if X > Y else y[0]))
        else:
            a, b = X - int(X), Y - int(Y)
            L = lcm(a.denominator, b.denominator)
            e = ("%s and %s. Both have %d whole%s, so compare the fraction parts with the denominator %d: "
                 "%s and %s. So <b>%s</b> is greater."
                 % (mxs[0], mxs[1], int(X), "" if int(X) == 1 else "s", L, eqL(show(a), a, L),
                    eqL(show(b), b, L), x[0] if X > Y else y[0]))
        its.append(which(x, y, e))

    # choose the sign
    for x, y in [(Fc(15, 4), Mc(3, 1, 2)), (Mc(2, 2, 3), Fc(17, 6))]:
        X, Y = x[1], y[1]
        sign = "&gt;" if X > Y else ("&lt;" if X < Y else "=")
        a, b = X - int(X), Y - int(Y)
        L = lcm(X.denominator, Y.denominator)
        e = ("Write both with the denominator %d: %s and %s. %d %s %d, so %s <b>%s</b> %s."
             % (L, eqL(x[0], X, L), eqL(y[0], Y, L), (X * L).numerator, sign,
                (Y * L).numerator, x[0], sign, y[0]))
        its.append(mcq("Which sign makes this true?<br>%s ☐ %s" % (x[0], y[0]), sign,
                       [s for s in ["&gt;", "&lt;", "="] if s != sign] + [CANT], e, rnd))

    # between two whole numbers
    for lo, right, others in [(2, F(11, 4), [F(7, 4), F(9, 3), F(13, 4)]),
                              (3, F(17, 5), [F(15, 5), F(21, 5), F(14, 5)]),
                              (1, F(11, 6), [F(5, 6), F(13, 6), F(12, 6)])]:
        assert lo < right < lo + 1 and all(not (lo < o < lo + 1) for o in others)
        d = right.denominator
        e = ("%s = %s, which is between %d and %d. Check the others: %s."
             % (fr(right.numerator, d), mixed(right), lo, lo + 1,
                ", ".join(("%s = %s" % (fr((o * d).numerator, d), mixed(o, d))) if o > 1 else
                          ("%s is less than 1" % fr((o * d).numerator, d)) for o in others)))
        its.append(mcq("Which fraction is between %d and %d?" % (lo, lo + 1),
                       (fr(right.numerator, d), right),
                       [(fr((o * d).numerator, d), o) for o in others], e, rnd))

    # greatest / least
    for word, vals in [("greatest", [(Fc(9, 4)), Mc(2, 1, 3), Fc(13, 6), Mc(1, 5, 6)]),
                       ("least", [Mc(3, 1, 2), Fc(10, 3), Fc(17, 5), Mc(2, 5, 6)]),
                       ("greatest", [Fc(21, 8), Mc(2, 3, 4), Fc(19, 8), Mc(2, 1, 2)])]:
        vs = [v for _, v in vals]
        assert len(set(vs)) == 4
        best = max(vals, key=lambda x: x[1]) if word == "greatest" else min(vals, key=lambda x: x[1])
        e = ("Write each as a mixed number: %s. "
             % ", ".join(mixed(v) for v in vs))
        same = [v for v in vs if int(v) == int(best[1])]
        if len(same) > 1:
            L = lcd([v - int(v) for v in same])
            e += ("Compare the fraction parts of the numbers with %d wholes in %s: %s. "
                  % (int(best[1]), WORD[L], ", ".join(fr(((v - int(v)) * L).numerator, L) for v in same)))
        e += "The %s is <b>%s</b>." % (word, best[0])
        its.append(mcq("Which is the %s?" % word, best, [v for v in vals if v is not best], e, rnd))

    # order three
    def s_of(seq):
        return ", ".join(h for h, _ in seq)
    for vals, up in [([Fc(9, 4), Mc(1, 1, 2), Mc(2, 1, 3)], True), ([Fc(7, 2), Mc(3, 1, 3), Fc(13, 4)], True),
                     ([Mc(1, 3, 5), Fc(9, 5), Fc(3, 2)], False), ([Fc(17, 6), Mc(2, 1, 2), Fc(8, 3)], False)]:
        right = sorted(vals, key=lambda x: x[1], reverse=not up)
        assert len(set(v for _, v in vals)) == 3
        L = lcd([v for _, v in vals])
        perms = [list(p) for p in itertools.permutations(vals)]
        perms = [list(reversed(right))] + [p for p in perms if p != right and p != list(reversed(right))]
        e = ("Write all three with the denominator %d: %s. So the order is <b>%s</b>."
             % (L, ", ".join(eqL(h, v, L) for h, v in vals), s_of(right)))
        its.append(mcq("Order from %s:<br>%s" % ("least to greatest" if up else "greatest to least", s_of(vals)),
                       s_of(right), [s_of(p) for p in perms], e, rnd))
    assert len(its) == 20, len(its)
    return {"title": "Compare and order", "items": its}


# ============================================================ set 5: number lines and word problems
def nl_item(t, L, d, cands, as_mixed, rnd):
    pos = SPOTS.next(rnd)
    lo = sorted([c for c in cands if c < t], reverse=True)
    hi = sorted([c for c in cands if c > t])
    pts = sorted(lo[:pos] + [t] + hi[:3 - pos])
    assert len(pts) == 4 and len(set(pts)) == 4, (t, pts)
    for v in pts:
        assert (v * d).denominator == 1 and 0 < v < L
    for a, b in zip(pts, pts[1:]):
        assert (b - a) * d >= 2, pts
    letter = "ABCD"[pts.index(t)]
    w = int(t)
    r = int((t - w) * d)
    name = mx(w, r, d) if as_mixed else fr(t.numerator, d)
    e = ("Each whole is split into %d equal parts, so each mark is %s. %s = %s: go to %d, then %d more mark%s. "
         "That is letter <b>%s</b>." % (d, fr(1, d), fr(t.numerator, d), mx(w, r, d), w, r, "" if r == 1 else "s", letter))
    q = fig(letters_line_svg(L, d, pts)) + "Which letter shows %s?" % name
    return {"q": q, "c": ["A", "B", "C", "D"], "a": pts.index(t), "e": e}


def set_words(rnd):
    SPOTS.left = []
    its = []
    for t, L, d, cands, as_mixed in [
            (F(9, 4), 4, 4, [F(7, 4), F(5, 4), F(3, 4), F(11, 4), F(13, 4), F(15, 4)], False),
            (F(13, 5), 4, 5, [F(11, 5), F(9, 5), F(7, 5), F(15, 5), F(17, 5), F(19, 5)], True),
            (F(7, 3), 5, 3, [F(5, 3), F(3, 3), F(1, 3), F(9, 3), F(11, 3), F(13, 3)], False),
            (F(17, 8), 3, 8, [F(15, 8), F(13, 8), F(11, 8), F(19, 8), F(21, 8), F(23, 8)], True),
            (F(19, 6), 5, 6, [F(16, 6), F(13, 6), F(10, 6), F(22, 6), F(25, 6), F(28, 6)], False)]:
        its.append(nl_item(t, L, d, cands, as_mixed, rnd))

    # word problems
    its.append(mcq("Ava walks %s km in the Terry Fox Run. Write this distance as a mixed number." % fr(13, 4),
                   Mc(3, 1, 4, " km"), [Mc(1, 3, 4, " km"), Mc(3, 1, 13, " km"), Mc(4, 1, 4, " km"), Mc(3, 3, 4, " km")],
                   "4 fourths make 1 km. 3 × 4 = 12, and 13 − 12 = 1 fourth is left over. So %s km = <b>3 %s km</b>."
                   % (fr(13, 4), fr(1, 4)), rnd))
    its.append(mcq("Jasleen says %s = 1 %s. What is the correct mixed number?" % (fr(7, 4), fr(3, 7)),
                   Mc(1, 3, 4), [Mc(1, 3, 7), Mc(3, 1, 4), Mc(1, 4, 7), Mc(2, 3, 4)],
                   "Jasleen used the numerator 7 as the new denominator. The parts are still fourths. "
                   "4 fourths make 1 whole, with 3 fourths left over: %s = <b>1 %s</b>." % (fr(7, 4), fr(3, 4)), rnd))
    its.append(mcq("Harjot says 3 %s = %s. What is the correct improper fraction?" % (fr(2, 5), fr(6, 5)),
                   Fc(17, 5), [Fc(6, 5), Fc(32, 5), Fc(17, 15), Fc(11, 5)],
                   "Harjot multiplied 3 × 2. Instead, 3 wholes = 3 × 5 = 15 fifths. Add 2 fifths: 15 + 2 = 17. "
                   "So 3 %s = <b>%s</b>." % (fr(2, 5), fr(17, 5)), rnd))
    its.append(mcq("A pizza is cut into 8 equal slices. At a class party, students eat 19 slices. "
                   "How many pizzas do they eat?",
                   Mc(2, 3, 8, " pizzas"), [Mc(3, 2, 8, " pizzas"), Mc(2, 3, 19, " pizzas"), Mc(2, 5, 8, " pizzas"),
                                            Mc(3, 3, 8, " pizzas")],
                   "8 slices make 1 pizza. 2 × 8 = 16, and 19 − 16 = 3 slices are left. So %s = <b>2 %s pizzas</b>."
                   % (fr(19, 8), fr(3, 8)), rnd))
    its.append(mcq("Liam needs 3 %s cups of flour for banana bread. He only has a %s cup measure. "
                   "How many times does he fill it?" % (fr(1, 2), fr(1, 4)),
                   Nc(14, " times"), [Nc(13, " times"), Nc(7, " times"), Nc(12, " times")],
                   "Count in fourths. 3 cups = 3 × 4 = 12 fourths, and %s cup = %s. 12 + 2 = <b>14</b>. "
                   "So 3 %s = %s." % (fr(1, 2), fr(2, 4), fr(1, 2), fr(14, 4)), rnd))
    its.append(mcq("A jug holds 2 %s L of water. Each cup holds %s L. How many cups can Chloe fill?" % (fr(3, 4), fr(1, 4)),
                   Nc(11, " cups"), [Nc(6, " cups"), Nc(9, " cups"), Nc(23, " cups")],
                   "2 L = 2 × 4 = 8 fourths. Add 3 fourths: 8 + 3 = <b>11</b>. So 2 %s = %s, which is 11 cups."
                   % (fr(3, 4), fr(11, 4)), rnd))
    its.append(mcq("3 friends share 7 sub sandwiches equally at a soccer tournament. How much does each friend get?",
                   Mc(2, 1, 3, " sandwiches"), [Fc(3, 7, " of a sandwich"), Mc(2, 1, 7, " sandwiches"),
                                                Mc(1, 1, 3, " sandwiches"), Mc(2, 2, 3, " sandwiches")],
                   "Each friend gets 7 ÷ 3 = %s sandwiches. 2 × 3 = 6, with 1 third left over. "
                   "So each friend gets <b>2 %s sandwiches</b>." % (fr(7, 3), fr(1, 3)), rnd))
    its.append(mcq("4 hikers on Grouse Mountain share 10 granola bars equally. How many bars does each hiker get?",
                   Mc(2, 1, 2, " bars"), [Fc(4, 10, " of a bar"), Mc(2, 1, 4, " bars"), Mc(2, 2, 10, " bars"),
                                          Mc(3, 1, 2, " bars")],
                   "Each hiker gets 10 ÷ 4 = %s bars. 2 × 4 = 8, with 2 fourths left over: 2 %s = <b>2 %s bars</b>."
                   % (fr(10, 4), fr(2, 4), fr(1, 2)), rnd))
    assert F(11, 3) > F(11, 4)
    its.append(mcq("Arjun hikes 2 %s km in Stanley Park. Mei hikes %s km. Who hikes farther?" % (fr(3, 4), fr(11, 3)),
                   "Mei", ["Arjun", "They hike the same distance", CANT],
                   "%s = 3 %s. Mei hikes more than 3 km, and Arjun hikes less than 3 km. So <b>Mei</b> hikes farther."
                   % (fr(11, 3), fr(2, 3)), rnd))
    assert F(7, 2) > F(13, 4)
    its.append(mcq("It rains %s cm in Vancouver on Monday and 3 %s cm on Tuesday. Which day has more rain?"
                   % (fr(13, 4), fr(1, 2)),
                   "Tuesday", ["Monday", "They have the same", CANT],
                   "%s = 3 %s. Both are 3 and a part. 3 %s = 3 %s, and %s &gt; %s. So <b>Tuesday</b> has more rain."
                   % (fr(13, 4), fr(1, 4), fr(1, 2), fr(2, 4), fr(2, 4), fr(1, 4)), rnd))
    its.append(mcq("The BC Ferries trip from Horseshoe Bay to Nanaimo takes about 1 %s hours. "
                   "Write this time as an improper fraction." % fr(3, 4),
                   Fc(7, 4, " hours"), [Fc(13, 4, " hours"), Fc(3, 4, " hours"), Fc(4, 4, " hours"), Fc(7, 3, " hours")],
                   "1 hour = 4 fourths. Add 3 fourths: 4 + 3 = 7. So 1 %s hours = <b>%s hours</b>."
                   % (fr(3, 4), fr(7, 4)), rnd))
    tr = [("Lynn Loop", F(5, 2)), ("Cedar Trail", F(9, 4)), ("Eagle Ridge", F(8, 3))]
    disp = {"Lynn Loop": "2 " + fr(1, 2) + " km", "Cedar Trail": fr(9, 4) + " km", "Eagle Ridge": "2 " + fr(2, 3) + " km"}
    order = [n for n, v in sorted(tr, key=lambda x: x[1])]
    assert order == ["Cedar Trail", "Lynn Loop", "Eagle Ridge"]
    its.append(mcq("Three hiking trails: Lynn Loop is %s, Cedar Trail is %s and Eagle Ridge is %s. "
                   "Order them from shortest to longest." % (disp["Lynn Loop"], disp["Cedar Trail"], disp["Eagle Ridge"]),
                   ", ".join(order),
                   [", ".join(p) for p in [["Eagle Ridge", "Lynn Loop", "Cedar Trail"], ["Lynn Loop", "Cedar Trail", "Eagle Ridge"],
                                           ["Cedar Trail", "Eagle Ridge", "Lynn Loop"]]],
                   "Use twelfths for the fraction parts. %s = 2 %s = 2 %s, 2 %s = 2 %s, 2 %s = 2 %s. "
                   "So the order is <b>Cedar Trail, Lynn Loop, Eagle Ridge</b>."
                   % (fr(9, 4), fr(1, 4), fr(3, 12), fr(1, 2), fr(6, 12), fr(2, 3), fr(8, 12)), rnd))
    its.append(mcq("Muffin trays hold 6 muffins each. Simran bakes 4 %s trays of muffins for a bake sale. "
                   "How many muffins is that?" % fr(5, 6),
                   Nc(29, " muffins"), [Nc(20, " muffins"), Nc(24, " muffins"), Nc(45, " muffins")],
                   "4 full trays = 4 × 6 = 24 muffins. %s of a tray = 5 muffins. 24 + 5 = <b>29 muffins</b>."
                   % fr(5, 6), rnd))
    its.append(mcq("A Grade 6 class uses 23 L of paint for a mural. Each can holds 4 L. "
                   "How many cans of paint is that, as a mixed number?",
                   Mc(5, 3, 4, " cans"), [Mc(5, 3, 23, " cans"), Mc(3, 5, 4, " cans"), Mc(6, 3, 4, " cans"),
                                          Mc(5, 1, 4, " cans")],
                   "23 ÷ 4: 5 × 4 = 20, and 23 − 20 = 3 L left over, which is %s of a can. So it is <b>5 %s cans</b>."
                   % (fr(3, 4), fr(3, 4)), rnd))
    its.append(mcq("Kai cuts a cedar board into pieces that are each %s m long. He makes 11 pieces with nothing left over. "
                   "How long was the board?" % fr(1, 3),
                   Mc(3, 2, 3, " m"), [Mc(3, 1, 3, " m"), Mc(2, 2, 3, " m"), Mc(3, 2, 11, " m"), Mc(4, 2, 3, " m")],
                   "11 pieces of %s m = %s m. 3 × 3 = 9, and 11 − 9 = 2 thirds left over. So the board was <b>3 %s m</b> long."
                   % (fr(1, 3), fr(11, 3), fr(2, 3)), rnd))
    assert len(its) == 20, len(its)
    return {"title": "Number lines and word problems", "items": its}


# ============================================================ lesson
def body_html():
    return (
        "<h2>Improper fractions</h2>"
        "<p>In an <b>improper fraction</b>, the numerator is greater than the denominator, so it is more than 1 whole. "
        "The denominator tells how many equal parts are in <b>one</b> whole.</p>"
        "<figure class='sn-fig'>" + bars_svg(4, 11) +
        "<figcaption>Each bar is 1 whole cut into fourths. 11 fourths are shaded: " + fr(11, 4) + ".</figcaption></figure>"
        + "<h2>Mixed numbers</h2>"
        "<p>A <b>mixed number</b> shows the same amount as wholes and a fraction less than 1. "
        "The bars above show 2 full wholes and 3 more fourths, so " + fr(11, 4) + " = 2 " + fr(3, 4) + ".</p>"
        "<figure class='sn-fig'>" + arrow_line_svg(3, 4, F(11, 4)) +
        "<figcaption>On a number line, " + fr(11, 4) + " = 2 " + fr(3, 4) + " is 3 marks after 2.</figcaption></figure>"
        + "<h2>Improper fraction to mixed number</h2>"
        "<p>Divide the numerator by the denominator. The answer is the number of wholes. "
        "The remainder is the new numerator. <b>The denominator does not change.</b></p>"
        + ex("Example", "Write " + fr(23, 6) + " as a mixed number.",
             "3 × 6 = 18, so there are 3 wholes. 23 − 18 = 5 sixths are left over.", "3 " + fr(5, 6))
        + "<h2>Mixed number to improper fraction</h2>"
        "<p>Multiply the wholes by the denominator, then add the numerator. Keep the same denominator.</p>"
        + ex("Example", "Write 3 " + fr(2, 5) + " as an improper fraction.",
             "3 wholes = 3 × 5 = 15 fifths. Add 2 fifths: 15 + 2 = 17.", fr(17, 5))
        + "<h2>Comparing and ordering</h2>"
        "<p>Change the numbers to mixed numbers and <b>compare the wholes first</b>. "
        "If the wholes are the same, compare the fraction parts with a common denominator. "
        "You can also write every number as an improper fraction with the same denominator.</p>"
        + ex("Example", "Which is greater: " + fr(7, 3) + " or 2 " + fr(1, 4) + "?",
             fr(7, 3) + " = 2 " + fr(1, 3) + ". Both have 2 wholes. In twelfths, " + fr(1, 3) + " = " + fr(4, 12)
             + " and " + fr(1, 4) + " = " + fr(3, 12) + ".", fr(7, 3))
        + "<h2>Common mistakes</h2>"
        + table(["Mistake", "What to do instead"], [
            [fr(7, 4) + " = 1 " + fr(3, 7) + " (the numerator becomes the denominator)",
             "The parts are still fourths: " + fr(7, 4) + " = 1 " + fr(3, 4)],
            ["2 " + fr(3, 5) + " = " + fr(6, 5) + " (2 × 3)",
             "Wholes × denominator, then add the numerator: 2 × 5 + 3 = 13, so " + fr(13, 5)],
            ["Counting all the parts in the model as the denominator: " + fr(11, 12),
             "The denominator is the parts in <b>one</b> whole: " + fr(11, 4)],
            ["Leaving a fraction part of 1 or more: 2 " + fr(7, 4),
             fr(7, 4) + " = 1 " + fr(3, 4) + ", so 2 " + fr(7, 4) + " = 3 " + fr(3, 4)],
        ])
    )


FAQ = [
    {"q": "What do Grade 6 students learn about improper fractions and mixed numbers in BC?",
     "a": "The BC Grade 6 math curriculum lists improper fractions and mixed numbers as a Number learning standard. Students model them with bars, circles and number lines, change one form into the other, and compare and order them."},
    {"q": "How do you change an improper fraction to a mixed number?",
     "a": "Divide the numerator by the denominator. The quotient is the number of wholes and the remainder is the new numerator, while the denominator stays the same: 23/6 = 3 5/6. A common mistake is 7/4 = 1 3/7; the right answer is 1 3/4."},
    {"q": "How do you change a mixed number to an improper fraction?",
     "a": "Multiply the whole number by the denominator, then add the numerator, and keep the same denominator. For 3 2/5, 3 × 5 + 2 = 17, so 3 2/5 = 17/5."},
    {"q": "How do you compare an improper fraction and a mixed number?",
     "a": "Write both in the same form. For 7/3 and 2 1/4, 7/3 = 2 1/3; both have 2 wholes, and 1/3 = 4/12 is more than 1/4 = 3/12, so 7/3 is greater."},
]


def gen():
    rnd = random.Random(56803)
    SPOTS.left = []
    sets = [set_models(rnd), set_mixed(rnd), set_convert(rnd), set_compare(rnd), set_words(rnd)]
    seen = set()
    for s in sets:
        assert len(s["items"]) == 20, (s["title"], len(s["items"]))
        cnt = [0, 0, 0, 0]
        for it in s["items"]:
            assert len(set(re.sub(r"<[^>]+>", "|", x) for x in it["c"])) == 4, it
            assert it["q"].count("<svg") <= 1
            k = re.sub(r"<[^>]+>", "|", it["q"]) + "|" + "|".join(sorted(it["c"]))
            assert k not in seen, it["q"]
            seen.add(k)
            cnt[it["a"]] += 1
        assert cnt == [5, 5, 5, 5], (s["title"], cnt)
    return {
        "country": "ca-bc", "subject": "math", "grade": "grade-6", "slug": SLUG, "sort": 3,
        "updated": UPDATED, "pdf_url": "",
        "title": "Grade 6 Improper Fractions and Mixed Numbers",
        "seo_title": "Grade 6 Improper Fractions and Mixed Numbers Worksheets: Free Math with Answer Key (BC Curriculum)",
        "short_title": "Improper fractions and mixed numbers",
        "domain": "Number",
        "standard_code": "Grade 6: Number",
        "standard_url": "https://curriculum.gov.bc.ca/curriculum/mathematics/6/core",
        "standard_text": "Improper fractions and mixed numbers",
        "meta_desc": "Free Grade 6 math worksheets on improper fractions and mixed numbers for the BC curriculum: bar and circle models, number lines, converting both ways, comparing and ordering, and word problems. 100 questions with an answer key.",
        "key_big": "The denominator never changes: 7/4 = 1 3/4, and 3 2/5 = 17/5.",
        "key_sub": "Improper to mixed: divide (7 ÷ 4 = 1 remainder 3). Mixed to improper: wholes × denominator + numerator (3 × 5 + 2 = 17). To compare, look at the wholes first: 17/6 = 2 5/6 < 3 2/5.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, SLUG + ".json")
    mark_large(u, "(number line|bars of|circles of)")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(u, f, ensure_ascii=False, indent=1)
    print("wrote", path)
