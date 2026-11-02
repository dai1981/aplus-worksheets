# -*- coding: utf-8 -*-
"""
AU Year 5 Maths: Comparing and ordering fractions (Australian Curriculum v9.0, AC9M5N03)
  python3 tools/gen_au_maths_y5_compare_fractions.py
Equivalent fractions with related denominators (bars, fraction wall, missing numbers),
comparing fractions with the same and related denominators, improper fractions and mixed
numerals, ordering fractions (including mixed numerals) and number lines from 0 to 3,
then word problems in Australian contexts.
Every choice carries its value; a wrong choice never equals the right value or another wrong one.
Every comparison and order is checked in code with exact fractions.
HTML attributes use single quotes (no backslashes in the JSON). Australian English.
"""
import json, math, os, random, re, itertools
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "au", "maths", "year-5")
SLUG = "comparing-fractions"
UPDATED = "2026-11-02"
FILL = "#4fae74"
BLUE = "#2f6db5"
LINE = "#2b2b2b"
CANT = "You can’t tell"
SAME = "They are equal"
WORD = {2: "halves", 3: "thirds", 4: "quarters", 5: "fifths", 6: "sixths", 7: "sevenths", 8: "eighths",
        9: "ninths", 10: "tenths", 12: "twelfths", 15: "fifteenths", 16: "sixteenths", 20: "twentieths"}
ONE = {2: "half", 3: "third", 4: "quarter", 5: "fifth", 6: "sixth", 7: "seventh", 8: "eighth", 9: "ninth",
       10: "tenth", 12: "twelfth", 16: "sixteenth", 20: "twentieth"}


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
    return ("%d%s" % (n, unit), F(n))


def lcm(a, b):
    return a * b // math.gcd(a, b)


def show(v):
    if v.denominator == 1:
        return str(v.numerator)
    return fr(v.numerator, v.denominator)


def over(v, L):
    return fr((v * L).numerator, L)


def eqL(v, L):
    if v.denominator == L:
        return show(v)
    return "%s = %s" % (show(v), over(v, L))


def parts(n, d):
    return "%d %s" % (n, ONE[d] if n == 1 else WORD[d])


# A number shown as it is written in the question: ("mix", w, n, d) or ("imp", n, d)
def M(w, n, d):
    return (mx(w, n, d), F(w) + F(n, d), "mix", d)


def I(n, d):
    return (fr(n, d), F(n, d), "imp", d)


def as_imp(t, L):
    """'1 3/8 = 11/8' or '5/4 = 10/8' or '11/8'."""
    h, v, kind, d = t
    s = over(v, L)
    if kind == "imp" and d == L:
        return s
    return "%s = %s" % (h, s)


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


# ============================================================ set 1: equivalent fractions
def set_equivalent(rnd):
    SPOTS.left = []
    its = []
    for a, b, d in [(1, 2, 8), (3, 4, 8), (2, 5, 10), (2, 3, 12), (3, 4, 12)]:
        n = d // b
        c = a * n
        q = (fig(two_bars_svg(b, a, d, c)) + "The bars are the same size and show the same amount.<br>%s = %s"
             % (fr(a, b), frq(d)))
        e = ("The bottom bar has %d equal parts, so each %s of the top bar is split into %d parts. "
             "%s become%s %d × %d = <b>%d</b> %s. So %s = %s."
             % (d, ONE[b], n, parts(a, b), "s" if a == 1 else "", a, n, c, WORD[d], fr(a, b), fr(c, d)))
        its.append(mcq(q, Nc(c), [Nc(a + (d - b)), Nc(a), Nc(d - c), Nc(c + 1), Nc(n)], e, rnd))

    for dens, (sd, k), t in [((2, 4, 8), (2, 1), 8), ((3, 6, 12), (3, 2), 12), ((5, 10), (5, 3), 10), ((4, 8), (4, 3), 8)]:
        n = t // sd
        c = k * n
        q = (fig(wall_svg(dens, (sd, k))) + "Use the fraction wall. %s is shaded. How many %s are equal to %s?"
             % (fr(k, sd), WORD[t], fr(k, sd)))
        e = ("Look down the fraction wall. Each %s is the same as %d %s, so %s line%s up with %d × %d = <b>%d</b> %s. "
             "So %s = %s." % (ONE[sd], n, WORD[t], parts(k, sd), "s" if k == 1 else "", k, n, c, WORD[t], fr(k, sd), fr(c, t)))
        its.append(mcq(q, Nc(c), [Nc(k + (t - sd)), Nc(k), Nc(t - c), Nc(c + n), Nc(n)], e, rnd))

    for a, b, d in [(5, 6, 12), (3, 8, 16), (4, 5, 20), (2, 3, 9)]:
        n = d // b
        c = a * n
        e = ("Look at the denominators: %d × <b>%d</b> = %d. Multiply the numerator by %d too: %d × %d = <b>%d</b>. "
             "So %s = %s." % (b, n, d, n, a, n, c, fr(a, b), fr(c, d)))
        its.append(mcq("%s = %s" % (fr(a, b), frq(d)), Nc(c), [Nc(a + (d - b)), Nc(a), Nc(n), Nc(d - c), Nc(c + n)], e, rnd))

    for a, b, c in [(3, 4, 9), (2, 5, 6), (5, 6, 10)]:
        n = c // a
        d = b * n
        assert n * a == c
        e = ("Look at the numerators: %d × <b>%d</b> = %d. Multiply the denominator by %d too: %d × %d = <b>%d</b>. "
             "So %s = %s." % (a, n, c, n, b, n, d, fr(a, b), fr(c, d)))
        its.append(mcq("%s = %s" % (fr(a, b), frq_d(c)), Nc(d), [Nc(b + (c - a)), Nc(b), Nc(b * c), Nc(n)], e, rnd))

    for a, b, d, wrong in [(6, 8, 4, [2, 6, 12, 8]), (10, 12, 6, [4, 10, 2, 12])]:
        k = b - d
        n = b // d
        c = a // n
        assert F(a, b) == F(c, d)
        e = ("%d ÷ <b>%d</b> = %d, so divide the numerator by %d too: %d ÷ %d = <b>%d</b>. So %s = %s. "
             "Taking %d away from the top and the bottom (to get %s) changes the value."
             % (b, n, d, n, a, n, c, fr(a, b), fr(c, d), k, fr(a - k, d)))
        its.append(mcq("%s = %s" % (fr(a, b), frq(d)), Nc(c), [Nc(w) for w in wrong], e, rnd))

    its.append(mcq("Which fraction is equal to %s?" % fr(2, 3), Fc(8, 12),
                   [Fc(8, 3), Fc(2, 12), Fc(4, 5), Fc(3, 2)],
                   "3 × 4 = 12, so multiply the numerator by 4 too: 2 × 4 = 8. So %s = <b>%s</b>. "
                   "%s only multiplies the numerator, and %s adds 2 to both numbers." % (fr(2, 3), fr(8, 12), fr(8, 3), fr(4, 5)), rnd))
    trues = [(6, 8), (9, 12), (15, 20)]
    for t in trues:
        assert F(*t) == F(3, 4)
    assert F(5, 6) != F(3, 4)
    its.append(mcq("Which fraction is <b>not</b> equivalent to %s?" % fr(3, 4), fr(5, 6), [fr(*t) for t in trues],
                   "<b>%s</b> is not equal to %s: 2 was added to the numerator and the denominator. Adding changes the value. "
                   "The others are equivalent, because both numbers were multiplied by the same number (× 2, × 3, × 5)."
                   % (fr(5, 6), fr(3, 4)), rnd))
    assert len(its) == 20, len(its)
    return {"title": "Equivalent fractions with related denominators", "items": its}


# ============================================================ set 2: compare two fractions
def which(x, y, rnd, bars=False):
    a, b = x
    c, d = y
    X, Y = F(a, b), F(c, d)
    right = SAME if X == Y else (fr(a, b) if X > Y else fr(c, d))
    big, small = max(X, Y), min(X, Y)
    bigs = fr(a, b) if X > Y else fr(c, d)
    if b == d:
        e = ("The denominators are the same, so compare the numerators: %d &gt; %d. So <b>%s</b> is greater."
             % (big * b, small * b, bigs))
    elif a == c:
        e = ("The numerators are the same. %s are bigger parts than %s, because the whole is cut into fewer parts. "
             "So <b>%s</b> is greater. The bigger denominator does not make the bigger fraction."
             % (WORD[min(b, d)].capitalize(), WORD[max(b, d)], bigs))
    else:
        L = lcm(b, d)
        assert L == max(b, d)
        e = ("%d is a multiple of %d, so use %s: %s and %s. "
             % (L, min(b, d), WORD[L], fr(a, b) if b == L else eqL(X, L), fr(c, d) if d == L else eqL(Y, L)))
        if X == Y:
            e += "The numerators are the same, so <b>they are equal</b>."
        else:
            e += "%d &gt; %d, so <b>%s</b> is greater." % (big * L, small * L, bigs)
    q = "Which is greater: %s or %s?" % (fr(a, b), fr(c, d))
    if bars:
        q = fig(two_bars_svg(b, a, d, c)) + "The bars are the same size. " + q
    return mcq(q, right, [fr(a, b), fr(c, d), SAME, CANT], e, rnd)


def set_compare(rnd):
    SPOTS.left = []
    its = []
    for x, y in [((5, 8), (3, 8)), ((4, 7), (6, 7)), ((7, 12), (9, 12))]:
        its.append(which(x, y, rnd))
    for x, y in [((1, 6), (1, 3)), ((1, 10), (1, 5)), ((3, 5), (3, 10))]:
        its.append(which(x, y, rnd))
    its.append(which((5, 8), (3, 4), rnd, True))
    its.append(which((2, 3), (7, 12), rnd, True))
    for x, y in [((3, 5), (7, 10)), ((4, 9), (1, 3)), ((5, 6), (11, 12)), ((3, 4), (6, 8)),
                 ((1, 2), (5, 12)), ((7, 10), (13, 20)), ((2, 3), (5, 9))]:
        its.append(which(x, y, rnd))

    # symbol in the box
    for (a, b), (c, d) in [((5, 6), (11, 12)), ((3, 4), (9, 12))]:
        X, Y = F(a, b), F(c, d)
        L = max(b, d)
        sym = "=" if X == Y else ("&gt;" if X > Y else "&lt;")
        e = "Use %s: %s and %s. So %s <b>%s</b> %s." % (WORD[L], fr(a, b) if b == L else eqL(X, L),
                                                         fr(c, d) if d == L else eqL(Y, L), fr(a, b), sym, fr(c, d))
        if X != Y:
            e += " The open side of the sign faces the greater fraction."
        its.append(mcq("Which sign goes in the box?<br>%s □ %s" % (fr(a, b), fr(c, d)),
                       sym, ["&lt;", "&gt;", "=", CANT], e, rnd))

    # which statement is true
    stm = [((3, 8), "&lt;", (1, 2)), ((5, 6), "&lt;", (2, 3)), ((3, 10), "&gt;", (2, 5)), ((7, 12), "&gt;", (3, 4))]
    ok = []
    for (a, b), s, (c, d) in stm:
        ok.append(F(a, b) < F(c, d) if s == "&lt;" else F(a, b) > F(c, d))
    assert ok == [True, False, False, False]
    sh = ["%s %s %s" % (fr(*p), s, fr(*r)) for p, s, r in stm]
    its.append(mcq("Which statement is true?", sh[0], sh[1:],
                   "Make the denominators the same. %s = %s, so %s &lt; %s is <b>true</b>. "
                   "The others are false: %s = %s &gt; %s, %s &lt; %s = %s and %s &lt; %s = %s."
                   % (fr(1, 2), fr(4, 8), fr(3, 8), fr(4, 8),
                      fr(5, 6), fr(10, 12), fr(8, 12), fr(3, 10), fr(2, 5), fr(4, 10), fr(7, 12), fr(3, 4), fr(9, 12)), rnd))

    # mixed numerals
    assert F(19, 8) > F(9, 4)
    its.append(mcq("Which is greater: 2 %s or 2 %s?" % (fr(1, 4), fr(3, 8)), Mc(2, 3, 8), [Mc(2, 1, 4), SAME, CANT],
                   "Both have 2 wholes, so compare the fractions. %s = %s, and 3 eighths &gt; 2 eighths. "
                   "So <b>2 %s</b> is greater." % (fr(1, 4), fr(2, 8), fr(3, 8)), rnd))
    assert F(5, 2) > F(9, 4)
    its.append(mcq("Which is greater: 2 %s or %s?" % (fr(1, 2), fr(9, 4)), Mc(2, 1, 2), [Fc(9, 4), SAME, CANT],
                   "Write both in quarters: 2 %s = %s (2 × 4 + 2 = 10), and %s is 9 quarters. 10 &gt; 9, so "
                   "<b>2 %s</b> is greater." % (fr(1, 2), fr(10, 4), fr(9, 4), fr(1, 2)), rnd))
    assert len(its) == 20, len(its)
    return {"title": "Compare fractions with the same and related denominators", "items": its}


# ============================================================ set 3: improper fractions and mixed numerals
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


def arrow_item(t, L, d, mode, rnd):
    w = int(t)
    r = int((t - w) * d)
    e = ("Each whole is split into %d equal parts, so each mark is %s. The arrow is %d mark%s after %d. "
         "So it shows %s = %s." % (d, fr(1, d), r, "" if r == 1 else "s", w,
                                   mx(w, r, d), fr(t.numerator * (d // t.denominator), d)))
    if mode == "mix":
        e = e.replace("So it shows %s" % mx(w, r, d), "So it shows <b>%s</b>" % mx(w, r, d))
        return mcq(fig(arrow_line_svg(L, d, t)) + "What number does the arrow show? Give a mixed numeral.",
                   Mc(w, r, d), [Mc(w, r, d * L), Mc(w + 1, r, d), Mc(w, d - r, d), Mc(w, r + 1, d), Fc(r, d)], e, rnd)
    n = t.numerator * (d // t.denominator)
    e = e.replace("= %s." % fr(n, d), "= <b>%s</b>. Count all the marks from 0: %d." % (fr(n, d), n))
    return mcq(fig(arrow_line_svg(L, d, t)) + "What number does the arrow show? Give an improper fraction.",
               Fc(n, d), [Fc(n, d * L), Fc(n + 1, d), Fc(r, d), Fc(n - 1, d), Fc(d, n)], e, rnd)


def set_mixed(rnd):
    SPOTS.left = []
    its = []
    for d, N in [(4, 11), (3, 8)]:
        q, r = divmod(N, d)
        e = ("Each bar is 1 whole. %d bars are full and %d more %s shaded in the last bar. So %s = <b>%s</b>."
             % (q, r, "part is" if r == 1 else "parts are", fr(N, d), mx(q, r, d)))
        its.append(mcq(fig(wholes_svg(d, N)) + "Each bar is 1 whole. %s are shaded. Write this as a mixed numeral." % fr(N, d),
                       Mc(q, r, d), [Fc(N, d * (q + 1))] + imp_cands(N, d), e, rnd))

    its.append(arrow_item(F(5, 3), 3, 3, "mix", rnd))
    its.append(arrow_item(F(9, 4), 3, 4, "mix", rnd))

    for n, d in [(7, 2), (13, 5), (17, 4), (19, 6), (23, 10), (29, 8), (22, 7)]:
        q, r = divmod(n, d)
        its.append(mcq("Write %s as a mixed numeral." % fr(n, d), Mc(q, r, d), imp_cands(n, d), imp_e(n, d), rnd))

    for w, n, d in [(2, 3, 5), (1, 2, 3), (3, 1, 4), (4, 2, 3), (1, 7, 10), (5, 3, 8), (2, 5, 6)]:
        its.append(mcq("Write %s as an improper fraction." % mx(w, n, d), Fc(w * d + n, d), mix_cands(w, n, d),
                       mix_e(w, n, d), rnd))

    assert F(13, 4) > 3 and F(11, 4) < 3 and F(12, 4) == 3
    its.append(mcq("Which improper fraction is greater than 3?", Fc(13, 4), [Fc(11, 4), Fc(12, 4), Fc(3, 4)],
                   "3 wholes = 3 × 4 = 12 quarters. %s is 1 quarter more, so <b>%s</b> = 3 %s is greater than 3. "
                   "%s is exactly 3, and %s is less than 3." % (fr(13, 4), fr(13, 4), fr(1, 4), fr(12, 4), fr(11, 4)), rnd))
    its.append(mcq("Which fraction is equal to 3 wholes?", Fc(15, 5), [Fc(3, 5), Fc(8, 5), Fc(5, 3)],
                   "Each whole is %s, so 3 wholes = 3 × 5 = <b>%s</b>. %s is less than 1, and %s comes from adding 3 + 5."
                   % (fr(5, 5), fr(15, 5), fr(3, 5), fr(8, 5)), rnd))
    assert len(its) == 20, len(its)
    return {"title": "Improper fractions and mixed numerals", "items": its}


# ============================================================ set 4: order and number lines
def nl_item(t, tshow, L, d, cands, rnd):
    pos = SPOTS.next(rnd)
    lo = sorted([c for c in cands if c < t], reverse=True)
    hi = sorted([c for c in cands if c > t])
    pts = sorted(lo[:pos] + [t] + hi[:3 - pos])
    assert len(pts) == 4 and len(set(pts)) == 4, (t, pts)
    for v in pts:
        assert (v * d).denominator == 1 and 0 < v < L
    letter = "ABCD"[pts.index(t)]
    w = int(t)
    p = t - w
    r = int(p * d)
    n = int(t * d)
    imp, mix = fr(n, d), mx(w, p.numerator, p.denominator)
    steps = mix if p.denominator == d else "%s = %s" % (mix, mx(w, r, d))
    e = ("Each whole is split into %d equal parts, so each mark is %s. %s = %s: go to %d, then %d more mark%s. "
         "That is letter <b>%s</b>." % (d, fr(1, d), imp if tshow == "imp" else steps,
                                        mx(w, r, d) if tshow == "imp" else imp, w, r, "" if r == 1 else "s", letter))
    if tshow == "mix" and p.denominator != d:
        e = e.replace("%s = %s: go" % (steps, imp), "%s: go" % steps)
    q = fig(letters_line_svg(L, d, pts)) + "Which letter shows %s?" % (imp if tshow == "imp" else mix)
    return {"q": q, "c": ["A", "B", "C", "D"], "a": pts.index(t), "e": e}


def set_order(rnd):
    SPOTS.left = []
    its = []

    def L_of(ts):
        L = 1
        for t in ts:
            L = lcm(L, t[3])
        return L

    def s_of(seq):
        return ", ".join(t[0] for t in seq)

    for word, ts in [("greatest", [I(3, 4), I(5, 8), I(11, 16), I(1, 2)]),
                     ("smallest", [I(2, 3), I(5, 6), I(7, 12), I(5, 12)]),
                     ("greatest", [I(3, 5), I(7, 10), I(13, 20), I(2, 5)]),
                     ("greatest", [M(1, 3, 4), I(15, 8), M(1, 1, 2), I(13, 8)])]:
        best = max(ts, key=lambda t: t[1]) if word == "greatest" else min(ts, key=lambda t: t[1])
        L = L_of(ts)
        e = ("Write them all in %s: %s. The %s is %s, so the answer is <b>%s</b>."
             % (WORD[L], ", ".join(as_imp(t, L) for t in ts), word, over(best[1], L), best[0]))
        its.append(mcq("Which %s is the %s?" % ("number" if any(t[2] == "mix" for t in ts) else "fraction", word), (best[0], best[1]),
                       [(t[0], t[1]) for t in ts if t is not best], e, rnd))

    for ts, up in [([I(3, 4), I(5, 8), I(1, 2)], True), ([I(2, 3), I(7, 12), I(5, 6)], True),
                   ([I(3, 10), I(1, 5), I(1, 2)], True), ([I(7, 8), I(3, 4), I(13, 16)], False),
                   ([M(1, 1, 2), I(5, 4), M(1, 3, 8)], True), ([M(2, 1, 3), I(13, 6), M(2, 5, 6)], False)]:
        assert len({t[1] for t in ts}) == 3
        right = sorted(ts, key=lambda t: t[1], reverse=not up)
        perms = [sorted(ts, key=lambda t: t[1].numerator), sorted(ts, key=lambda t: t[3]),
                 sorted(ts, key=lambda t: -t[3]), list(reversed(right))]
        perms += [list(p) for p in itertools.permutations(ts)]
        L = L_of(ts)
        e = ("Write them all in %s: %s. So the order is <b>%s</b>."
             % (WORD[L], ", ".join(as_imp(t, L) for t in ts), s_of(right)))
        its.append(mcq("Order from %s:<br>%s" % ("smallest to largest" if up else "largest to smallest", s_of(ts)),
                       s_of(right), [s_of(p) for p in perms], e, rnd))

    for t, show_as, d in [(F(7, 4), "imp", 4), (F(4, 3), "mix", 3), (F(3, 2), "mix", 4), (F(11, 6), "imp", 6)]:
        cands = [t + F(k, d) for k in (-4, -3, -2, -1, 1, 2, 3, 4)]
        cands = [c for c in cands if 0 < c < 3]
        its.append(nl_item(t, show_as, 3, d, cands, rnd))

    its.append(arrow_item(F(13, 6), 3, 6, "mix", rnd))
    its.append(arrow_item(F(11, 5), 3, 5, "imp", rnd))
    its.append(arrow_item(F(8, 3), 3, 3, "mix", rnd))

    assert F(1, 2) < F(5, 8) < F(3, 4) and F(7, 8) > F(3, 4) and F(3, 8) < F(1, 2)
    its.append(mcq("Which fraction is between %s and %s?" % (fr(1, 2), fr(3, 4)), Fc(5, 8), [Fc(7, 8), Fc(3, 8), Fc(4, 5)],
                   "In eighths: %s = %s and %s = %s. <b>%s</b> is between them. %s and %s are more than %s, and %s is less than %s."
                   % (fr(1, 2), fr(4, 8), fr(3, 4), fr(6, 8), fr(5, 8), fr(7, 8), fr(4, 5), fr(3, 4), fr(3, 8), fr(1, 2)), rnd))
    assert F(9, 4) < F(19, 8) < F(11, 4) and F(17, 8) < F(9, 4) and F(23, 8) > F(11, 4)
    its.append(mcq("Which number is between 2 %s and 2 %s?" % (fr(1, 4), fr(3, 4)), Fc(19, 8),
                   [Fc(17, 8), Fc(23, 8), Fc(9, 4)],
                   "In eighths: 2 %s = %s and 2 %s = %s. <b>%s</b> is between them. %s is too small, %s is too big, "
                   "and %s is equal to 2 %s, not between." % (fr(1, 4), fr(18, 8), fr(3, 4), fr(22, 8), fr(19, 8),
                                                              fr(17, 8), fr(23, 8), fr(9, 4), fr(1, 4)), rnd))
    gaps = {v: 1 - v for v in [F(7, 8), F(3, 4), F(5, 8), F(9, 16)]}
    assert min(gaps, key=gaps.get) == F(7, 8)
    its.append(mcq("Which fraction is closest to 1?", Fc(7, 8), [Fc(9, 16), Fc(3, 4), Fc(5, 8)],
                   "Use sixteenths: %s, %s, %s = %s, %s = %s. The one nearest to %s is %s, so <b>%s</b> is closest to 1. "
                   "Big numbers in a fraction do not make it close to 1."
                   % (fr(9, 16), eqL(F(7, 8), 16), fr(3, 4), fr(12, 16), fr(5, 8), fr(10, 16), fr(16, 16), fr(14, 16), fr(7, 8)), rnd))
    assert len(its) == 20, len(its)
    return {"title": "Order fractions and mixed numerals on a number line", "items": its}


# ============================================================ set 5: word problems
def set_words(rnd):
    SPOTS.left = []
    its = []
    # 1
    assert F(3, 8) < F(1, 2)
    its.append(mcq("Mia eats %s of a pizza. Lachlan eats %s of a pizza of the same size. Who eats more?" % (fr(3, 8), fr(1, 2)),
                   "Lachlan", ["Mia", "They eat the same", CANT],
                   "Use eighths: %s = %s. 4 eighths is more than 3 eighths, so <b>Lachlan</b> eats more."
                   % (fr(1, 2), fr(4, 8)), rnd))
    # 2
    its.append(mcq("A pizza is cut into 8 equal slices. Jack eats %s of it. How many slices does he eat?" % fr(3, 4),
                   Nc(6, " slices"), [Nc(3, " slices"), Nc(7, " slices"), Nc(4, " slices")],
                   "4 × 2 = 8, so %s = %s. Jack eats <b>6 slices</b>." % (fr(3, 4), fr(6, 8)), rnd))
    # 3
    assert F(11, 4) > F(21, 8)
    its.append(mcq("At the athletics carnival, Oliver runs 2 %s km and Isla runs 2 %s km. Who runs further?" % (fr(3, 4), fr(5, 8)),
                   "Oliver", ["Isla", "They run the same", CANT],
                   "Both ran 2 whole kilometres, so compare %s and %s. %s = %s, which is more than %s. "
                   "So <b>Oliver</b> runs further." % (fr(3, 4), fr(5, 8), fr(3, 4), fr(6, 8), fr(5, 8)), rnd))
    # 4
    assert F(2, 5) > F(3, 10)
    its.append(mcq("In class 5M, %s of the students play netball. In class 5K, %s of the students play netball. "
                   "Which class has the greater fraction of netball players?" % (fr(2, 5), fr(3, 10)),
                   "5M", ["5K", "They are the same", CANT],
                   "Use tenths: %s = %s. 4 tenths is more than 3 tenths, so <b>5M</b> has the greater fraction. "
                   "A bigger denominator does not mean a bigger fraction." % (fr(2, 5), fr(4, 10)), rnd))
    # 5
    assert F(2, 5) == F(4, 10)
    its.append(mcq("Ava says %s of her class and %s of her class are the same number of students. Is she right?" % (fr(2, 5), fr(4, 10)),
                   "Yes. %s = %s" % (fr(2, 5), fr(4, 10)),
                   ["No. %s is more" % fr(4, 10), "No. %s is more" % fr(2, 5), "You can’t tell without the class size"],
                   "Multiply the numerator and the denominator of %s by 2: %s = %s. "
                   "They are equivalent fractions, so they are the same number of students. <b>Yes</b>, she is right."
                   % (fr(2, 5), fr(2, 5), fr(4, 10)), rnd))
    # 6
    assert F(5, 6) > F(2, 3)
    its.append(mcq("A koala can sleep for about %s of a day. A wombat can sleep for about %s of a day. "
                   "Which animal sleeps for the greater part of the day?" % (fr(5, 6), fr(2, 3)),
                   "The koala", ["The wombat", "They sleep the same", CANT],
                   "Use sixths: %s = %s. 5 sixths is more than 4 sixths, so <b>the koala</b> sleeps for longer."
                   % (fr(2, 3), fr(4, 6)), rnd))
    # 7
    its.append(mcq("For a sausage sizzle, each packet holds 6 sausages. The class cooks 19 sausages. "
                   "How many packets is that, as a mixed numeral?",
                   Mc(3, 1, 6, " packets"), [Mc(1, 3, 6, " packets"), Mc(3, 1, 19, " packets"), Mc(4, 1, 6, " packets"),
                                             Mc(3, 5, 6, " packets")],
                   "6 sausages make 1 packet. 3 × 6 = 18, and 19 − 18 = 1 sausage is left. So %s = <b>3 %s packets</b>."
                   % (fr(19, 6), fr(1, 6)), rnd))
    # 8
    rib = [("Leo", F(3, 4)), ("Chloe", F(7, 8)), ("Kai", F(5, 8)), ("Zara", F(1, 2))]
    assert max(rib, key=lambda x: x[1])[0] == "Chloe"
    its.append(mcq("Four students measure their ribbons. Leo: %s m. Chloe: %s m. Kai: %s m. Zara: %s m. "
                   "Who has the longest ribbon?" % (fr(3, 4), fr(7, 8), fr(5, 8), fr(1, 2)),
                   "Chloe", ["Leo", "Kai", "Zara"],
                   "Use eighths: %s = %s, %s, %s, %s = %s. The longest is <b>Chloe’s</b> ribbon."
                   % (fr(3, 4), fr(6, 8), fr(7, 8), fr(5, 8), fr(1, 2), fr(4, 8)), rnd))
    # 9
    its.append(mcq("Noah says, “%s is greater than %s, because 8 is greater than 4.” Is he right?" % (fr(1, 8), fr(1, 4)),
                   "No. %s is less than %s" % (fr(1, 8), fr(1, 4)),
                   ["Yes. 8 is greater than 4", "No. They are equal", "Yes. Eighths are bigger than quarters"],
                   "A bigger denominator means the whole is cut into <b>more, smaller</b> parts. %s = %s, which is more than %s. "
                   "So %s is <b>less</b> than %s." % (fr(1, 4), fr(2, 8), fr(1, 8), fr(1, 8), fr(1, 4)), rnd))
    # 10
    its.append(mcq("Ruby says 2 %s = %s. What is the correct improper fraction?" % (fr(3, 5), fr(6, 5)),
                   Fc(13, 5), [Fc(6, 5), Fc(23, 5), Fc(13, 10), Fc(11, 5)],
                   "Ruby multiplied 2 × 3. Instead, 2 wholes = 2 × 5 = 10 fifths. Add 3 fifths: 10 + 3 = 13. So 2 %s = <b>%s</b>."
                   % (fr(3, 5), fr(13, 5)), rnd))
    # 11
    assert F(7, 10) > F(3, 5)
    its.append(mcq("At sport, Liam drinks %s L of water and Sienna drinks %s L. Who drinks more?" % (fr(7, 10), fr(3, 5)),
                   "Liam", ["Sienna", "They drink the same", CANT],
                   "Use tenths: %s = %s. 7 tenths is more than 6 tenths, so <b>Liam</b> drinks more." % (fr(3, 5), fr(6, 10)), rnd))
    # 12
    jumps = [("Harper", F(11, 4)), ("Cooper", F(21, 8)), ("Mei", F(5, 2))]
    order = [n for n, v in sorted(jumps, key=lambda x: -x[1])]
    assert order == ["Harper", "Cooper", "Mei"]
    names = [n for n, v in jumps]
    perms = [", ".join(p) for p in itertools.permutations(names) if list(p) != order]
    perms = [", ".join(["Mei", "Cooper", "Harper"]), ", ".join(["Cooper", "Harper", "Mei"])] + perms
    its.append(mcq("In the long jump, Harper jumps 2 %s m, Cooper jumps 2 %s m and Mei jumps 2 %s m. "
                   "Order them from the longest jump to the shortest." % (fr(3, 4), fr(5, 8), fr(1, 2)),
                   ", ".join(order), perms,
                   "All jumped 2 whole metres, so compare the fractions in eighths: %s = %s, %s, %s = %s. "
                   "So the order is <b>Harper, Cooper, Mei</b>." % (fr(3, 4), fr(6, 8), fr(5, 8), fr(1, 2), fr(4, 8)), rnd))
    # 13
    its.append(mcq("A tray of lamingtons is cut into 12 equal pieces. Kai’s family eats 9 pieces. "
                   "Which fraction is equal to the part they eat?", Fc(3, 4),
                   [Fc(1, 4), Fc(9, 4), Fc(3, 12), Fc(1, 3)],
                   "9 out of 12 pieces = %s. Divide the numerator and the denominator by 3: %s = <b>%s</b>. "
                   "%s is the part that is left." % (fr(9, 12), fr(9, 12), fr(3, 4), fr(1, 4)), rnd))
    # 14
    its.append(mcq("Grace walks %s km to the beach. Write this distance as a mixed numeral." % fr(11, 4),
                   Mc(2, 3, 4, " km"), [Mc(3, 2, 4, " km"), Mc(2, 3, 11, " km"), Mc(1, 1, 4, " km"), Mc(3, 3, 4, " km")],
                   "4 × 2 = 8 and 11 − 8 = 3. So %s km = <b>2 %s km</b>." % (fr(11, 4), fr(3, 4)), rnd))
    # 15
    pens = [("5A", F(3, 4)), ("5B", F(9, 16)), ("5C", F(5, 8))]
    assert sorted(pens, key=lambda x: x[1])[0][0] == "5B"
    its.append(mcq("Three classes each have the same size tin of paint. Class 5A uses %s of theirs, class 5B uses %s and "
                   "class 5C uses %s. Which class uses the least paint?" % (fr(3, 4), fr(9, 16), fr(5, 8)),
                   "Class 5B", ["Class 5A", "Class 5C", "They all use the same"],
                   "Use sixteenths: %s = %s, %s, %s = %s. The smallest is %s, so <b>class 5B</b> uses the least. "
                   "16 is the biggest denominator, but that does not make it the biggest fraction."
                   % (fr(3, 4), fr(12, 16), fr(9, 16), fr(5, 8), fr(10, 16), fr(9, 16)), rnd))
    # 16
    assert F(7, 4) < 2
    its.append(mcq("At footy training, Ethan runs 7 laps. Each lap is %s km. That is %s km. Is it more or less than 2 km?"
                   % (fr(1, 4), fr(7, 4)),
                   "Less. %s km = 1 %s km" % (fr(7, 4), fr(3, 4)),
                   ["More. 7 is more than 2", "Exactly 2 km", "More. %s km = 7 %s km" % (fr(7, 4), fr(1, 4))],
                   "4 quarters make 1 km and 8 quarters make 2 km. 7 quarters is 1 quarter short of 2 km, so %s km = "
                   "<b>1 %s km</b>, which is less than 2 km." % (fr(7, 4), fr(3, 4)), rnd))
    # 17
    assert F(2, 3) > F(7, 12)
    its.append(mcq("Aarav has read %s of his book. Matilda has read %s of the same book. Who has read more?" % (fr(7, 12), fr(2, 3)),
                   "Matilda", ["Aarav", "They have read the same", CANT],
                   "Use twelfths: %s = %s. 8 twelfths is more than 7 twelfths, so <b>Matilda</b> has read more."
                   % (fr(2, 3), fr(8, 12)), rnd))
    # 18
    a, b = F(3, 4) * 24, F(5, 8) * 24
    assert (a, b) == (18, 15)
    its.append(mcq("Classes 5W and 5T each have 24 students. %s of 5W and %s of 5T go on the school excursion. "
                   "How many more students from 5W go?" % (fr(3, 4), fr(5, 8)),
                   Nc(3, " students"), [Nc(2, " students"), Nc(18, " students"), Nc(15, " students"), Nc(6, " students")],
                   "%s = %s, which is 2 eighths more than %s. One eighth of 24 is 24 ÷ 8 = 3. "
                   "5W: 18 students (%s of 24). 5T: 15 students. 18 − 15 = <b>3 students</b>."
                   % (fr(3, 4), fr(6, 8), fr(5, 8), fr(3, 4)), rnd))
    # 19
    assert F(3, 2) > F(5, 4)
    its.append(mcq("A recipe needs %s cups of flour. Charlotte has 1 %s cups. Does she have enough?" % (fr(5, 4), fr(1, 2)),
                   "Yes. 1 %s = %s, which is more than %s" % (fr(1, 2), fr(6, 4), fr(5, 4)),
                   ["No. 5 is more than 1", "No. 1 %s = %s, which is less than %s" % (fr(1, 2), fr(3, 4), fr(5, 4)),
                    "No. 1 %s = %s, which is less than %s" % (fr(1, 2), fr(2, 4), fr(5, 4))],
                   "Write 1 %s in quarters: 1 whole = %s and %s = %s, so 1 %s = %s. %s &gt; %s, so <b>yes</b>, she has enough."
                   % (fr(1, 2), fr(4, 4), fr(1, 2), fr(2, 4), fr(1, 2), fr(6, 4), fr(6, 4), fr(5, 4)), rnd))
    # 20
    assert F(5, 6) > F(2, 3)
    its.append(mcq("Two families drive the same road to Adelaide. Amelia’s family has driven %s of the way. "
                   "William’s family has driven %s of the way. Who is closer to Adelaide?" % (fr(5, 6), fr(2, 3)),
                   "Amelia’s family", ["William’s family", "They are the same distance away", CANT],
                   "Use sixths: %s = %s. Amelia’s family has driven 5 sixths, so only 1 sixth is left. "
                   "William’s family has 2 sixths left. <b>Amelia’s family</b> is closer." % (fr(2, 3), fr(4, 6)), rnd))
    assert len(its) == 20, len(its)
    return {"title": "Fraction word problems", "items": its}


# ============================================================ lesson
def body_html():
    return (
        "<h2>Same denominator</h2>"
        "<p>When the denominators are the same, the parts are the same size. <b>Compare the numerators.</b> "
        "For example, " + fr(5, 8) + " &gt; " + fr(3, 8) + ", because 5 eighths is more than 3 eighths.</p>"
        "<p>When the numerators are the same, look at the size of the parts. "
        + fr(1, 3) + " &gt; " + fr(1, 6) + ", because thirds are bigger than sixths.</p>"
        "<h2>Related denominators</h2>"
        "<p>Denominators are <b>related</b> when one is a multiple of the other, like 4 and 8. "
        "Change one fraction into an <b>equivalent fraction</b>: multiply the numerator and the denominator by the same number. "
        "Then compare the numerators.</p>"
        "<figure class='sn-fig'>" + wall_svg((4, 8)) +
        "<figcaption>Each quarter is the same as 2 eighths, so " + fr(3, 4) + " = " + fr(6, 8) + ".</figcaption></figure>"
        + ex("Example", "Which is greater: " + fr(5, 8) + " or " + fr(3, 4) + "?",
             "8 is a multiple of 4. 4 × 2 = 8, so " + fr(3, 4) + " = " + fr(6, 8) + ". 6 eighths &gt; 5 eighths.",
             fr(3, 4))
        + "<figure class='sn-fig'>" + two_bars_svg(8, 5, 4, 3) +
        "<figcaption>" + fr(5, 8) + " (top) is less than " + fr(3, 4) + " (bottom).</figcaption></figure>"
        + "<h2>Improper fractions and mixed numerals</h2>"
        "<p>An <b>improper fraction</b> such as " + fr(11, 4) + " is greater than 1. "
        "A <b>mixed numeral</b> such as 2 " + fr(3, 4) + " shows the same amount as wholes and a fraction.</p>"
        "<figure class='sn-fig'>" + wholes_svg(4, 11) +
        "<figcaption>" + fr(11, 4) + " = 2 wholes and 3 more quarters = 2 " + fr(3, 4) + ".</figcaption></figure>"
        + ex("Example", "Write 2 " + fr(3, 5) + " as an improper fraction.",
             "2 wholes = 2 × 5 = 10 fifths. Add 3 fifths: 10 + 3 = 13.", fr(13, 5))
        + "<h2>Fractions on a number line</h2>"
        "<p>Split each whole into equal parts. Count the marks from 0. Numbers further to the right are greater.</p>"
        "<figure class='sn-fig'>" + arrow_line_svg(3, 4, F(9, 4)) +
        "<figcaption>The arrow is 1 mark after 2, so it shows 2 " + fr(1, 4) + " = " + fr(9, 4) + ".</figcaption></figure>"
        + ex("Example", "Order " + fr(5, 4) + ", 1 " + fr(1, 2) + " and 1 " + fr(3, 8) + " from smallest to largest.",
             "Write them all in eighths: " + fr(5, 4) + " = " + fr(10, 8) + ", 1 " + fr(1, 2) + " = " + fr(12, 8)
             + ", 1 " + fr(3, 8) + " = " + fr(11, 8) + ".",
             fr(5, 4) + ", 1 " + fr(3, 8) + ", 1 " + fr(1, 2))
        + "<h2>Common mistakes</h2>"
        + table(["Mistake", "What to do instead"], [
            ["Thinking a bigger denominator means a bigger fraction: " + fr(1, 8) + " &gt; " + fr(1, 4),
             "A bigger denominator means <b>smaller</b> parts: " + fr(1, 8) + " &lt; " + fr(1, 4)],
            ["Comparing only the numerators: " + fr(5, 8) + " &gt; " + fr(3, 4) + " because 5 &gt; 3",
             "Make the denominators the same first: " + fr(3, 4) + " = " + fr(6, 8) + ", so " + fr(5, 8) + " &lt; " + fr(3, 4)],
            ["Multiplying only the numerator: " + fr(3, 4) + " = " + fr(6, 4),
             "Multiply both: " + fr(3, 4) + " = " + fr(6, 8)],
            ["2 " + fr(3, 5) + " = " + fr(6, 5) + " or " + fr(23, 5),
             "Wholes × denominator, then add the numerator: 2 × 5 + 3 = 13, so " + fr(13, 5)],
        ])
    )


FAQ = [
    {"q": "What do Year 5 students learn about comparing fractions?",
     "a": "In the Australian Curriculum (AC9M5N03), Year 5 students compare and order fractions with the same and related denominators, including mixed numerals, and show them on a number line. Related denominators are ones like 4 and 8, where one is a multiple of the other."},
    {"q": "How do you compare fractions with different denominators?",
     "a": "If one denominator is a multiple of the other, change one fraction so both have the same denominator, then compare the numerators. For 5/8 and 3/4, 3/4 = 6/8, so 3/4 is greater."},
    {"q": "What is a mixed numeral?",
     "a": "A mixed numeral is a whole number and a fraction written together, such as 2 3/4. It shows the same amount as the improper fraction 11/4, because 2 × 4 + 3 = 11."},
    {"q": "Are comparing fractions questions on the Year 5 NAPLAN numeracy test?",
     "a": "Fractions are part of the Number strand that NAPLAN numeracy draws on, so Year 5 students may meet questions on ordering fractions or placing them on a number line. Practising with fraction walls and number lines helps."},
]


def gen():
    rnd = random.Random(5803)
    SPOTS.left = []
    sets = [set_equivalent(rnd), set_compare(rnd), set_mixed(rnd), set_order(rnd), set_words(rnd)]
    for s in sets:
        assert len(s["items"]) == 20, (s["title"], len(s["items"]))
        cnt = [0, 0, 0, 0]
        for it in s["items"]:
            assert len(set(it["c"])) == 4, it
            cnt[it["a"]] += 1
        assert cnt == [5, 5, 5, 5], (s["title"], cnt)
    return {
        "country": "au", "subject": "maths", "grade": "year-5", "slug": SLUG, "sort": 3,
        "updated": UPDATED, "pdf_url": "",
        "title": "Year 5 Comparing and Ordering Fractions",
        "seo_title": "Year 5 Comparing Fractions Worksheets: Related Denominators, Mixed Numerals and Number Lines (Free, with Answer Key)",
        "short_title": "Comparing fractions",
        "domain": "Number",
        "standard_code": "AC9M5N03",
        "standard_url": "https://v9.australiancurriculum.edu.au/f-10-curriculum/learning-areas/mathematics",
        "standard_text": "Compare and order fractions with the same and related denominators including mixed numerals, applying knowledge of factors and multiples; represent these fractions on a number line",
        "meta_desc": "Free Year 5 maths worksheets on comparing and ordering fractions for the Australian Curriculum (AC9M5N03): equivalent fractions with related denominators, fraction walls, improper fractions, mixed numerals, number lines and word problems. 100 questions with an answer key, ideal for NAPLAN practice.",
        "key_big": "To compare fractions, make the denominators the same, then compare the numerators.",
        "key_sub": "3/4 = 6/8, so 5/8 < 3/4. A bigger denominator means smaller parts: 1/8 < 1/4. 2 3/5 = 13/5, because 2 × 5 + 3 = 13.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, SLUG + ".json")
    mark_large(u, "(number line|bars of|two bars|fraction wall)")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(u, f, ensure_ascii=False, indent=1)
    print("wrote", path)
