# -*- coding: utf-8 -*-
"""
AU Year 6 Maths: Comparing and ordering fractions (Australian Curriculum v9.0, AC9M6N03)
  python3 tools/gen_au_maths_y6_compare_fractions.py
Equivalent fractions and simplest form, comparing fractions with unrelated denominators
(common denominators), ordering 3-4 fractions including mixed numerals and improper fractions,
halves, thirds and quarters on the same number line, then fractions, decimals and percentages
in word problems set in Australian contexts.
Every choice carries its value; a wrong choice never equals the right value or another wrong one.
Every comparison and order is checked in code with exact fractions.
HTML attributes use single quotes (no backslashes in the JSON). Australian English.
"""
import json, math, os, random, re, itertools
from fractions import Fraction as F
from decimal import Decimal

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "au", "maths", "year-6")
SLUG = "comparing-and-ordering-fractions"
UPDATED = "2026-11-02"
FILL = "#4fae74"
RED = "#c0392b"
BLUE = "#2f6db5"
LINE = "#2b2b2b"
THIN = "#8a8a8a"
CANT = "You can’t tell"
SAME = "They are equal"
WORD = {2: "halves", 3: "thirds", 4: "quarters", 5: "fifths", 6: "sixths", 7: "sevenths", 8: "eighths", 9: "ninths",
        10: "tenths", 12: "twelfths"}
ONE = {2: "half", 3: "third", 4: "quarter", 5: "fifth", 6: "sixth", 8: "eighth", 10: "tenth", 12: "twelfth"}


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


def dec(v):
    s = str(Decimal(v.numerator) / Decimal(v.denominator))
    if "." in s:
        s = s.rstrip("0").rstrip(".")
    return s


def Dc(v):
    v = F(v)
    return (dec(v), v)


def pct(v):
    return dec(F(v) * 100) + "%"


def Pc(p):
    """p is the percentage number (e.g. 75 or F(25, 2))."""
    return (dec(F(p)) + "%", F(p) / 100)


def lcm(a, b):
    return a * b // math.gcd(a, b)


def lcd(vals):
    L = 1
    for v in vals:
        L = lcm(L, v.denominator)
    return L


def show(v, mixed=False):
    if mixed and v > 1 and v.denominator > 1:
        return mx(v.numerator // v.denominator, v.numerator % v.denominator, v.denominator)
    if v.denominator == 1:
        return str(v.numerator)
    return fr(v.numerator, v.denominator)


def over(v, L):
    return fr((v * L).numerator, L)


def factors(n):
    return [k for k in range(1, n + 1) if n % k == 0]


# A number shown as it is written in the question: (html, value, kind, den)
def M(w, n, d):
    return (mx(w, n, d), F(w) + F(n, d), "mix", d)


def I(n, d):
    return (fr(n, d), F(n, d), "imp", d)


def as_over(t, L):
    """'1 3/8 = 11/8' or '5/4 = 10/8' or '11/8' (already over L)."""
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

    def refill(self, rnd):
        if not self.left:
            self.left = [0, 1, 2, 3]
            rnd.shuffle(self.left)

    def next(self, rnd):
        self.refill(rnd)
        return self.left.pop()

    def take(self, rnd, ok):
        """Next free position that is in ok (for number lines, where not every letter is possible)."""
        self.refill(rnd)
        for i in range(len(self.left) - 1, -1, -1):
            if self.left[i] in ok:
                return self.left.pop(i)
        raise AssertionError("no free position in %s (left %s)" % (ok, self.left))


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


def cd_bars_svg(a, b, c, d, W=288, H=38):
    """Two bars cut into L = lcm(b, d) thin parts; thick lines show b parts (top) and d parts (bottom)."""
    L = lcm(b, d)
    LW = 40
    s = []
    for row, (num, den) in enumerate([(a, b), (c, d)]):
        y = 6 + row * (H + 14)
        s.append(sfr(6 + LW / 2 - 2, y + 15, num, den))
        s.append(group_bar(6 + LW, y, W, H, L, num * L // den, L // den))
    return svg_wrap(W + LW + 12, 2 * H + 26, "".join(s),
                    "two fraction bars of the same size cut into %d equal parts, showing %d/%d and %d/%d" % (L, a, b, c, d))


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


def two_lines_svg(L, p, q, W=380):
    """Two number lines 0..L of the same length: top in steps of 1/p.denominator with a red dot at p,
    bottom in steps of 1/q.denominator with a blue dot at q."""
    x0, x1 = 60, W - 16
    s = []
    for row, (v, col) in enumerate([(p, RED), (q, BLUE)]):
        Y = 26 + row * 70
        s.append(sfr(28, Y - 4, v.numerator, v.denominator, 15, col))
        s.append(tick_line(L, v.denominator, Y, x0, x1))
        s.append("<circle cx='%.1f' cy='%d' r='7' fill='%s'/>" % (x0 + (x1 - x0) * float(v) / L, Y, col))
    return svg_wrap(W, 26 + 70 + 38, "".join(s),
                    "two number lines from 0 to %d of the same length with dots at %s and %s" % (L, p, q))


def lesson_line_svg(W=400):
    """Lesson: 0 to 1 cut into twelfths, with 1/4, 1/3, 1/2, 2/3 and 3/4 marked above."""
    x0, x1 = 20, W - 20
    Y = 64
    s = [tick_line(1, 12, Y, x0, x1)]
    for v, col in [(F(1, 4), RED), (F(1, 3), BLUE), (F(1, 2), LINE), (F(2, 3), BLUE), (F(3, 4), RED)]:
        X = x0 + (x1 - x0) * float(v)
        s.append("<circle cx='%.1f' cy='%d' r='5' fill='%s'/>" % (X, Y, col))
        s.append(sfr(X, 18, v.numerator, v.denominator, 15, col))
    return svg_wrap(W, Y + 38, "".join(s),
                    "number line from 0 to 1 cut into twelfths with one quarter, one third, one half, two thirds and three quarters marked")


# ============================================================ set 1: equivalent fractions and simplest form
def simp_cands(n, d):
    h = math.gcd(n, d)
    sn, sd = n // h, d // h
    c = [Fc(sd, sn), Fc(sn, d - n + sn), Fc(sn, d), Fc(n, sd)]
    for f in factors(d):
        if f not in (1, h, d):
            c.append(Fc(sn, d // f))
    c.append(Fc(sn + 1, sd))
    return c


def simp_e(n, d):
    h = math.gcd(n, d)
    sn, sd = n // h, d // h
    return ("The highest common factor of %d and %d is %d. Divide both numbers by %d: %d ÷ %d = %d and %d ÷ %d = %d. "
            "So %s = <b>%s</b>." % (n, d, h, h, n, h, sn, d, h, sd, fr(n, d), fr(sn, sd)))


def set_equivalent(rnd):
    SPOTS.left = []
    its = []
    for a, b, d in [(1, 3, 6), (3, 4, 12), (2, 5, 10)]:
        n = d // b
        c = a * n
        q = (fig(two_bars_svg(b, a, d, c)) + "The bars are the same size and show the same amount.<br>%s = %s"
             % (fr(a, b), frq(d)))
        e = ("The bottom bar has %d equal parts, so each %s of the top bar is split into %d parts. "
             "%d %s become%s %d × %d = <b>%d</b> %s. So %s = %s."
             % (d, ONE[b], n, a, ONE[b] if a == 1 else WORD[b], "s" if a == 1 else "", a, n, c, WORD[d], fr(a, b), fr(c, d)))
        its.append(mcq(q, Nc(c), [Nc(a + (d - b)), Nc(a), Nc(d - c), Nc(c + 1), Nc(n)], e, rnd))

    for a, b, d in [(2, 3, 12), (5, 6, 18), (3, 8, 24), (4, 5, 20)]:
        n = d // b
        c = a * n
        e = ("Look at the denominators: %d × <b>%d</b> = %d. Multiply the numerator by %d too: %d × %d = <b>%d</b>. "
             "So %s = %s." % (b, n, d, n, a, n, c, fr(a, b), fr(c, d)))
        its.append(mcq("%s = %s" % (fr(a, b), frq(d)), Nc(c), [Nc(a + (d - b)), Nc(a), Nc(n), Nc(d - c), Nc(c + n)], e, rnd))

    for a, b, c in [(3, 4, 15), (2, 3, 10)]:
        n = c // a
        d = b * n
        assert n * a == c
        e = ("Look at the numerators: %d × <b>%d</b> = %d. Multiply the denominator by %d too: %d × %d = <b>%d</b>. "
             "So %s = %s." % (a, n, c, n, b, n, d, fr(a, b), fr(c, d)))
        its.append(mcq("%s = %s" % (fr(a, b), frq_d(c)), Nc(d), [Nc(b + (c - a)), Nc(b), Nc(b * c), Nc(n)], e, rnd))

    for n, d, g in [(6, 8, 2), (8, 12, 4)]:
        sn, sd = n // g, d // g
        q = (fig(group_bar_svg(d, n, g)) + "%s of the bar is shaded. The thick lines split it into groups of %d. "
             "Write %s in its simplest form." % (fr(n, d), g, fr(n, d)))
        e = ("There are %d groups and %d of them are shaded, so %s = <b>%s</b>. "
             "This is the same as dividing %d and %d by %d." % (sd, sn, fr(n, d), fr(sn, sd), n, d, g))
        its.append(mcq(q, Fc(sn, sd), simp_cands(n, d), e, rnd))

    for n, d in [(10, 12), (12, 15), (14, 16), (16, 24), (18, 30), (21, 28)]:
        h = math.gcd(n, d)
        e = simp_e(n, d)
        if h in (4, 6, 8):
            e += " If you divide by a smaller common factor first, keep going until you can’t divide any more."
        its.append(mcq("Write %s in its simplest form." % fr(n, d), Fc(n // h, d // h), simp_cands(n, d), e, rnd))

    eqs = [(4, 6), (8, 12), (10, 15)]
    for t in eqs:
        assert F(*t) == F(2, 3)
    assert F(4, 5) != F(2, 3)
    its.append(mcq("Which fraction is <b>not</b> equivalent to %s?" % fr(2, 3), fr(4, 5), [fr(*t) for t in eqs],
                   "<b>%s</b> is not equal to %s: 2 was added to the numerator and the denominator. Adding changes the value. "
                   "The others are equivalent, because both numbers were multiplied by the same number (× 2, × 4, × 5)."
                   % (fr(4, 5), fr(2, 3)), rnd))
    assert F(9, 12) == F(3, 4)
    its.append(mcq("Which fraction is equivalent to %s?" % fr(3, 4), Fc(9, 12), [Fc(6, 4), Fc(3, 12), Fc(5, 6)],
                   "4 × 3 = 12, so multiply the numerator by 3 too: 3 × 3 = 9. So %s = <b>%s</b>. "
                   "%s only multiplies the numerator, %s only changes the denominator, and %s adds 2 to both numbers."
                   % (fr(3, 4), fr(9, 12), fr(6, 4), fr(3, 12), fr(5, 6)), rnd))
    good, others = (7, 12), [(8, 14), (10, 15), (3, 9)]
    assert math.gcd(*good) == 1 and all(math.gcd(*o) > 1 for o in others)
    bits = ["%s = %s (÷ %d)" % (fr(a, b), fr(a // math.gcd(a, b), b // math.gcd(a, b)), math.gcd(a, b)) for a, b in others]
    its.append(mcq("Which fraction is in its simplest form?", Fc(*good), [Fc(*o) for o in others],
                   "7 and 12 have no common factor except 1, so <b>%s</b> is in its simplest form. "
                   "The others can be simplified: %s." % (fr(*good), "; ".join(bits)), rnd))
    assert len(its) == 20, len(its)
    return {"title": "Equivalent fractions and simplest form", "items": its}


# ============================================================ set 2: compare two fractions
def cmp_text(a, b, c, d):
    """Explanation that ends with the greater fraction in bold (or 'they are equal')."""
    X, Y = F(a, b), F(c, d)
    big = fr(a, b) if X > Y else fr(c, d)
    if b == d:
        return ("The denominators are the same, so compare the numerators: %d &gt; %d. So <b>%s</b> is greater."
                % (max(a, c), min(a, c), big))
    if a == c:
        return ("The numerators are the same. %s are bigger parts than %s, because the whole is cut into fewer parts. "
                "So <b>%s</b> is greater. A bigger denominator does not make a bigger fraction."
                % (WORD[min(b, d)].capitalize(), WORD[max(b, d)], big))
    L = lcm(b, d)
    A, C = a * L // b, c * L // d
    s = ("Use the common denominator %d: %s and %s. " % (
        L, fr(a, b) if b == L else "%s = %s" % (fr(a, b), fr(A, L)), fr(c, d) if d == L else "%s = %s" % (fr(c, d), fr(C, L))))
    if X == Y:
        return s + "The numerators are the same, so <b>they are equal</b>."
    s += "%d &gt; %d, so <b>%s</b> is greater." % (max(A, C), min(A, C), big)
    if (a > c) != (X > Y) and a != c:
        s += " Comparing only the numerators (%d and %d) gives the wrong answer." % (a, c)
    return s


def which(x, y, rnd, fig_=None, smaller=False):
    a, b = x
    c, d = y
    X, Y = F(a, b), F(c, d)
    if smaller:
        assert X != Y
        right = fr(a, b) if X < Y else fr(c, d)
        e = cmp_text(a, b, c, d)
        e = e.replace("<b>", "").replace("</b>", "") + " So the smaller one is <b>%s</b>." % right
        q = "Which is smaller: %s or %s?" % (fr(a, b), fr(c, d))
    else:
        right = SAME if X == Y else (fr(a, b) if X > Y else fr(c, d))
        e = cmp_text(a, b, c, d)
        q = "Which is greater: %s or %s?" % (fr(a, b), fr(c, d))
    if fig_:
        q = fig(fig_) + "The bars are the same size. " + q
    return mcq(q, right, [fr(a, b), fr(c, d), SAME, CANT], e, rnd)


def set_compare(rnd):
    SPOTS.left = []
    its = []
    its.append(which((4, 7), (6, 7), rnd))
    its.append(which((3, 5), (3, 8), rnd))
    its.append(which((4, 5), (4, 7), rnd))
    its.append(which((2, 3), (3, 4), rnd, cd_bars_svg(2, 3, 3, 4)))
    its.append(which((3, 5), (1, 2), rnd, cd_bars_svg(3, 5, 1, 2)))
    its.append(which((5, 12), (1, 3), rnd))
    for x, y in [((3, 5), (2, 3)), ((5, 6), (7, 8)), ((3, 4), (4, 5)), ((2, 5), (3, 8)), ((7, 12), (5, 8)),
                 ((6, 9), (4, 6))]:
        its.append(which(x, y, rnd))
    its.append(which((5, 6), (9, 10), rnd, smaller=True))

    # symbol in the box
    for (a, b), (c, d) in [((5, 6), (4, 5)), ((3, 4), (9, 12)), ((3, 8), (2, 5))]:
        X, Y = F(a, b), F(c, d)
        sym = "=" if X == Y else ("&gt;" if X > Y else "&lt;")
        L = lcm(b, d)
        if d == L and X == Y:
            e = "Use the common denominator %d: %s = %s. So %s <b>%s</b> %s." % (L, fr(a, b), over(X, L), fr(a, b), sym, fr(c, d))
        else:
            e = "Use the common denominator %d: %s and %s. So %s <b>%s</b> %s." % (
                L, fr(a, b) if b == L else "%s = %s" % (fr(a, b), over(X, L)),
                fr(c, d) if d == L else "%s = %s" % (fr(c, d), over(Y, L)), fr(a, b), sym, fr(c, d))
        if X != Y:
            e += " The open side of the sign faces the greater fraction."
        its.append(mcq("Which sign goes in the box?<br>%s □ %s" % (fr(a, b), fr(c, d)),
                       sym, ["&lt;", "&gt;", "=", CANT], e, rnd))

    # which statement is true
    stm = [((2, 3), "&gt;", (3, 5)), ((3, 4), "&lt;", (5, 8)), ((5, 6), "&lt;", (4, 5)), ((2, 5), "&gt;", (1, 2))]
    ok = [F(*p) > F(*r) if s == "&gt;" else F(*p) < F(*r) for p, s, r in stm]
    assert ok == [True, False, False, False]
    sh = ["%s %s %s" % (fr(*p), s, fr(*r)) for p, s, r in stm]
    its.append(mcq("Which statement is true?", sh[0], sh[1:],
                   "Use a common denominator for each pair. %s = %s and %s = %s, so %s &gt; %s is <b>true</b>. "
                   "The others are false: %s = %s &gt; %s; %s = %s &gt; %s = %s; %s = %s &lt; %s = %s."
                   % (fr(2, 3), fr(10, 15), fr(3, 5), fr(9, 15), fr(2, 3), fr(3, 5),
                      fr(3, 4), fr(6, 8), fr(5, 8), fr(5, 6), fr(25, 30), fr(4, 5), fr(24, 30),
                      fr(2, 5), fr(4, 10), fr(1, 2), fr(5, 10)), rnd))

    # benchmark 1/2
    for v in [F(3, 8), F(2, 5), F(5, 12)]:
        assert v < F(1, 2)
    assert F(4, 7) > F(1, 2)
    its.append(mcq("Which fraction is greater than %s?" % fr(1, 2), Fc(4, 7), [Fc(3, 8), Fc(2, 5), Fc(5, 12)],
                   "Half of the denominator is the numerator of one half. Half of 7 is 3.5, and 4 &gt; 3.5, so "
                   "<b>%s</b> is greater than %s. Half of 8 is 4 (3 &lt; 4), half of 5 is 2.5 (2 &lt; 2.5) and "
                   "half of 12 is 6 (5 &lt; 6), so the others are less than %s." % (fr(4, 7), fr(1, 2), fr(1, 2)), rnd))

    # mixed numeral and improper fraction
    assert F(7, 4) > F(5, 3)
    its.append(mcq("Which is greater: 1 %s or %s?" % (fr(2, 3), fr(7, 4)), Fc(7, 4), [Mc(1, 2, 3), SAME, CANT],
                   "%s = 1 %s. Both have 1 whole, so compare %s and %s. Use twelfths: %s = %s and %s = %s. "
                   "9 &gt; 8, so <b>%s</b> is greater." % (fr(7, 4), fr(3, 4), fr(2, 3), fr(3, 4),
                                                         fr(2, 3), fr(8, 12), fr(3, 4), fr(9, 12), fr(7, 4)), rnd))

    # the mistake
    assert F(4, 9) < F(1, 2)
    its.append(mcq("Jack says, “%s is greater than %s, because 4 is greater than 1.” Is he right?" % (fr(4, 9), fr(1, 2)),
                   "No. %s is less than %s" % (fr(4, 9), fr(1, 2)),
                   ["Yes. 4 is greater than 1", "Yes. 9 is greater than 2", "No. They are equal"],
                   "Comparing only the numerators does not work. Use eighteenths: %s = %s and %s = %s. "
                   "8 &lt; 9, so <b>%s is less than %s</b>." % (fr(4, 9), fr(8, 18), fr(1, 2), fr(9, 18), fr(4, 9), fr(1, 2)), rnd))
    assert len(its) == 20, len(its)
    return {"title": "Compare fractions with different denominators", "items": its}


# ============================================================ set 3: order fractions
def s_of(seq):
    return ", ".join(t[0] for t in seq)


def set_order(rnd):
    SPOTS.left = []
    its = []
    # same numerator / gaps to 1 (easiest)
    assert max([F(3, 4), F(3, 5), F(3, 8), F(3, 10)]) == F(3, 4)
    its.append(mcq("Which fraction is the greatest?", Fc(3, 4), [Fc(3, 10), Fc(3, 8), Fc(3, 5)],
                   "All the numerators are 3, so look at the size of the parts. Quarters are the biggest parts here, "
                   "so <b>%s</b> is the greatest. %s has the biggest denominator, so it is the smallest." % (fr(3, 4), fr(3, 10)), rnd))

    for word, ts in [("greatest", [I(2, 3), I(3, 4), I(5, 8), I(7, 12)]),
                     ("smallest", [I(2, 3), I(3, 5), I(7, 10), I(5, 6)]),
                     ("greatest", [I(7, 4), M(1, 2, 3), M(1, 5, 6), I(13, 8)]),
                     ("smallest", [M(2, 1, 4), I(7, 3), M(2, 1, 6), I(5, 2)])]:
        assert len({t[1] for t in ts}) == 4
        best = max(ts, key=lambda t: t[1]) if word == "greatest" else min(ts, key=lambda t: t[1])
        L = lcd([t[1] for t in ts])
        e = ("Use the common denominator %d: %s. The %s is %s, so the answer is <b>%s</b>."
             % (L, ", ".join(as_over(t, L) for t in ts), word, over(best[1], L), best[0]))
        its.append(mcq("Which %s is the %s?" % ("number" if any(t[2] == "mix" for t in ts) else "fraction", word),
                       (best[0], best[1]), [(t[0], t[1]) for t in ts if t is not best], e, rnd))

    for ts, up in [([I(3, 4), I(2, 3), I(1, 2)], True), ([I(2, 5), I(1, 3), I(1, 2)], True),
                   ([I(5, 6), I(3, 4), I(7, 8)], False), ([I(3, 8), I(1, 4), I(1, 3)], True),
                   ([I(4, 5), I(7, 10), I(3, 4)], False), ([I(5, 4), M(1, 1, 3), I(7, 6)], True),
                   ([I(5, 3), M(1, 5, 8), M(1, 3, 4)], False), ([M(2, 1, 2), I(7, 3), I(9, 4)], True),
                   ([I(2, 3), I(1, 2), I(3, 4), I(1, 3)], True), ([I(5, 6), I(2, 3), I(3, 4), I(7, 12)], True),
                   ([M(1, 1, 4), I(3, 2), I(4, 3), M(1, 1, 6)], False)]:
        assert len({t[1] for t in ts}) == len(ts)
        right = sorted(ts, key=lambda t: t[1], reverse=not up)
        assert right != ts, s_of(ts)
        perms = [sorted(ts, key=lambda t: t[1].numerator), sorted(ts, key=lambda t: t[3]),
                 sorted(ts, key=lambda t: -t[3]), list(reversed(right))]
        perms += [list(p) for p in itertools.permutations(ts)]
        L = lcd([t[1] for t in ts])
        e = ("Use the common denominator %d: %s. So the order is <b>%s</b>."
             % (L, ", ".join(as_over(t, L) for t in ts), s_of(right)))
        its.append(mcq("Order from %s:<br>%s" % ("smallest to largest" if up else "largest to smallest", s_of(ts)),
                       s_of(right), [s_of(p) for p in perms], e, rnd))

    assert F(1, 3) < F(5, 12) < F(1, 2) and F(1, 4) < F(1, 3) and F(2, 3) > F(1, 2) and F(7, 12) > F(1, 2)
    its.append(mcq("Which fraction is between %s and %s?" % (fr(1, 3), fr(1, 2)), Fc(5, 12), [Fc(1, 4), Fc(2, 3), Fc(7, 12)],
                   "Use twelfths: %s = %s and %s = %s. <b>%s</b> is between them. %s = %s is too small, and "
                   "%s = %s and %s are too big." % (fr(1, 3), fr(4, 12), fr(1, 2), fr(6, 12), fr(5, 12), fr(1, 4), fr(3, 12),
                                                  fr(2, 3), fr(8, 12), fr(7, 12)), rnd))
    assert F(3, 2) < F(13, 8) < F(7, 4) and F(11, 8) < F(3, 2) and F(15, 8) > F(7, 4) and F(5, 4) < F(3, 2)
    its.append(mcq("Which number is between 1 %s and 1 %s?" % (fr(1, 2), fr(3, 4)), Fc(13, 8),
                   [Fc(11, 8), Fc(15, 8), Fc(5, 4)],
                   "Use eighths: 1 %s = %s and 1 %s = %s. <b>%s</b> = 1 %s is between them. %s and %s are too small, "
                   "and %s is too big." % (fr(1, 2), fr(12, 8), fr(3, 4), fr(14, 8), fr(13, 8), fr(5, 8),
                                           fr(11, 8), fr(5, 4), fr(15, 8)), rnd))
    gaps = {v: 1 - v for v in [F(7, 8), F(4, 5), F(5, 6), F(9, 10)]}
    assert min(gaps, key=gaps.get) == F(9, 10)
    its.append(mcq("Which fraction is closest to 1?", Fc(9, 10), [Fc(7, 8), Fc(4, 5), Fc(5, 6)],
                   "Look at the part that is missing from 1 whole: %s needs %s, %s needs %s, %s needs %s and %s needs %s. "
                   "%s is the smallest missing part, so <b>%s</b> is closest to 1."
                   % (fr(7, 8), fr(1, 8), fr(4, 5), fr(1, 5), fr(5, 6), fr(1, 6), fr(9, 10), fr(1, 10), fr(1, 10), fr(9, 10)), rnd))
    gaps = {v: 1 - v for v in [F(5, 6), F(6, 7), F(7, 8), F(4, 5)]}
    assert max(gaps, key=gaps.get) == F(4, 5)
    its.append(mcq("Which fraction is the smallest?", Fc(4, 5), [Fc(5, 6), Fc(6, 7), Fc(7, 8)],
                   "Each fraction is 1 part short of 1 whole: %s, %s, %s and %s are missing. "
                   "%s is the biggest missing part, so <b>%s</b> is the smallest."
                   % (fr(1, 5), fr(1, 6), fr(1, 7), fr(1, 8), fr(1, 5), fr(4, 5)), rnd))
    assert len(its) == 20, len(its)
    return {"title": "Order fractions, mixed numerals and improper fractions", "items": its}


# ============================================================ set 4: the same number line
def nl_item(t, L, d, pool, name, rnd):
    """Letters A-D on a line 0..L in steps of 1/d. pool: likely wrong points (real mistakes) first."""
    grid = [F(i, d) for i in range(1, L * d) if i % d]
    assert t in grid, t
    for p in pool:
        assert p in grid and p != t, p
    lo = [p for p in pool if p < t] + sorted([g for g in grid if g < t and g not in pool], key=lambda g: t - g)
    hi = [p for p in pool if p > t] + sorted([g for g in grid if g > t and g not in pool], key=lambda g: g - t)
    ok = [p for p in range(4) if p <= len(lo) and 3 - p <= len(hi)]
    pos = SPOTS.take(rnd, ok)
    pts = sorted(lo[:pos] + [t] + hi[:3 - pos])
    assert len(set(pts)) == 4
    q = fig(letters_line_svg(L, d, pts)) + "Which letter shows %s?" % name
    return {"q": q, "c": ["A", "B", "C", "D"], "a": pts.index(t), "e": ""}  # the caller writes the explanation


def arrow_item(t, L, d, cands, rnd, mixed):
    w = int(t)
    r = int((t - w) * d)
    raw = mx(w, r, d)
    simple = show(t, mixed)
    e = ("Each whole is split into %d equal parts, so each mark is %s. The arrow is %d mark%s after %d, so it shows %s"
         % (d, fr(1, d), r, "" if r == 1 else "s", w, raw))
    frac = t - w
    if frac.denominator != d:
        h = d // frac.denominator
        e += ". Simplify: %s = %s (÷ %d). The answer is <b>%s</b>." % (fr(r, d), show(frac), h, simple)
    else:
        e += " = <b>%s</b>." % simple
    e += " Count the spaces between marks, not the marks themselves."
    q = fig(arrow_line_svg(L, d, t)) + "What number does the arrow show? Give the %s in simplest form." % (
        "mixed numeral" if mixed else "fraction")
    return mcq(q, (simple, t), cands, e, rnd)


def set_numberline(rnd):
    SPOTS.left = []
    its = []
    # letters on a line. 0 to 1 in twelfths: halves, thirds and quarters on the same line.
    # Items whose point is near the right end go first in each round of A-D, so every letter stays possible.
    TW = None
    rows = [(F(5, 3), 2, 6, [F(5, 6), F(3, 2), F(11, 6), F(4, 3)], fr(5, 3)),
            (F(2, 3), 1, 12, [F(2, 12), F(3, 4), F(1, 2), F(5, 6)], TW),
            (F(3, 4), 1, 12, [F(3, 12), F(2, 3), F(5, 6), F(1, 2)], TW),
            (F(1, 3), 1, 12, [F(3, 12), F(1, 2), F(1, 6), F(5, 12)], TW),
            (F(5, 6), 1, 12, [F(5, 12), F(3, 4), F(2, 3), F(11, 12)], TW),
            (F(4, 3), 2, 6, [F(1, 3), F(3, 2), F(5, 3), F(7, 6)], mx(1, 1, 3)),
            (F(5, 4), 2, 8, [F(5, 8), F(9, 8), F(3, 2), F(11, 8)], fr(5, 4)),
            (F(9, 4), 3, 4, [F(5, 4), F(5, 2), F(11, 4), F(7, 4)], fr(9, 4)),
            (F(7, 4), 2, 8, [F(11, 8), F(3, 4), F(3, 2), F(13, 8)], mx(1, 3, 4))]
    for t, L, d, pool, name in rows:
        if name is TW:
            name = fr(t.numerator, t.denominator)
            it = nl_item(t, L, d, pool, name, rnd)
            k = 12 // t.denominator
            it["e"] = ("The line from 0 to 1 is split into twelfths. %s = %s (multiply both numbers by %d), "
                       "so count %d marks from 0. That is letter <b>%s</b>. Don’t count only %d mark%s: each mark is %s, not %s."
                       % (name, fr(t.numerator * k, 12), k, t.numerator * k, "ABCD"[it["a"]], t.numerator,
                          "" if t.numerator == 1 else "s", fr(1, 12),
                          fr(1, t.denominator)))
            its.append(it)
            continue
        it = nl_item(t, L, d, pool, name, rnd)
        w = int(t)
        part = t - w
        r = int(part * d)
        start = "" if name.startswith("%d " % w) else "%s = %s. " % (name, mx(w, part.numerator, part.denominator))
        steps = "" if part.denominator == d else "%s = %s. " % (fr(part.numerator, part.denominator), fr(r, d))
        it["e"] = ("Each whole is split into %d equal parts, so each mark is %s. %s%sGo to %d, then %d more mark%s. "
                   "That is letter <b>%s</b>." % (d, fr(1, d), start, steps, w, r, "" if r == 1 else "s", "ABCD"[it["a"]]))
        its.append(it)

    # arrows: name the point in simplest form
    its.append(arrow_item(F(2, 3), 1, 6, [Fc(4, 7), Fc(3, 4), Fc(1, 3), Fc(4, 5)], rnd, False))
    its.append(arrow_item(F(3, 4), 1, 12, [Fc(9, 13), Fc(2, 3), Fc(1, 4), Fc(5, 6)], rnd, False))
    its.append(arrow_item(F(3, 2), 2, 6, [Fc(3, 4), Mc(1, 2, 3), Mc(1, 1, 3), Mc(1, 1, 4)], rnd, True))
    its.append(arrow_item(F(7, 4), 2, 8, [Fc(7, 8), Mc(1, 5, 8), Mc(1, 2, 3), Mc(1, 3, 8)], rnd, True))

    # two number lines of the same length
    for p, q, L in [(F(2, 3), F(3, 4), 1), (F(5, 6), F(3, 4), 1), (F(4, 3), F(5, 4), 2)]:
        right = fr(p.numerator, p.denominator) if p > q else fr(q.numerator, q.denominator)
        Lc = lcm(p.denominator, q.denominator)
        e = ("The dot further to the right shows the greater number. Check with the common denominator %d: "
             "%s = %s and %s = %s. So <b>%s</b> is greater." % (Lc, fr(p.numerator, p.denominator), over(p, Lc),
                                                               fr(q.numerator, q.denominator), over(q, Lc), right))
        qq = (fig(two_lines_svg(L, p, q)) + "The two number lines are the same length. Which is greater: %s or %s?"
              % (fr(p.numerator, p.denominator), fr(q.numerator, q.denominator)))
        its.append(mcq(qq, right, [fr(p.numerator, p.denominator), fr(q.numerator, q.denominator), SAME, CANT], e, rnd))

    # halfway and closest to 0
    assert (F(1, 2) + 1) / 2 == F(3, 4)
    its.append(mcq("Which fraction is exactly halfway between %s and 1 on a number line?" % fr(1, 2), Fc(3, 4),
                   [Fc(2, 3), Fc(1, 4), Fc(5, 8)],
                   "Use quarters: %s = %s and 1 = %s. Halfway between 2 quarters and 4 quarters is <b>%s</b>. "
                   "%s is between them too, but it is not halfway." % (fr(1, 2), fr(2, 4), fr(4, 4), fr(3, 4), fr(2, 3)), rnd))
    assert (F(1, 4) + F(1, 2)) / 2 == F(3, 8) and F(1, 4) < F(1, 3) < F(1, 2)
    its.append(mcq("Which fraction is exactly halfway between %s and %s on a number line?" % (fr(1, 4), fr(1, 2)), Fc(3, 8),
                   [Fc(1, 3), Fc(3, 4), Fc(1, 8)],
                   "Use eighths: %s = %s and %s = %s. Halfway between 2 eighths and 4 eighths is <b>%s</b>. "
                   "%s = %s is between them, but it is not halfway." % (fr(1, 4), fr(2, 8), fr(1, 2), fr(4, 8), fr(3, 8),
                                                                       fr(1, 3), fr(8, 24)), rnd))
    assert (1 + F(3, 2)) / 2 == F(5, 4)
    its.append(mcq("Which number is exactly halfway between 1 and 1 %s on a number line?" % fr(1, 2), Mc(1, 1, 4),
                   [Mc(1, 1, 3), Mc(1, 3, 4), Fc(1, 4)],
                   "Use quarters: 1 %s = 1 %s. Halfway between 1 and 1 %s is <b>1 %s</b>. "
                   "1 %s is between them, but it is not halfway." % (fr(1, 2), fr(2, 4), fr(2, 4), fr(1, 4), fr(1, 3)), rnd))
    assert min([F(1, 2), F(1, 3), F(1, 4)]) == F(1, 4)
    its.append(mcq("Mia marks %s, %s and %s on the same number line from 0 to 1. Which one is closest to 0?"
                   % (fr(1, 2), fr(1, 3), fr(1, 4)), fr(1, 4), [fr(1, 2), fr(1, 3), "They are all the same distance"],
                   "Use twelfths: %s = %s, %s = %s and %s = %s. The smallest is %s, so <b>%s</b> is closest to 0. "
                   "Quarters are smaller parts than thirds and halves." % (fr(1, 2), fr(6, 12), fr(1, 3), fr(4, 12),
                                                                          fr(1, 4), fr(3, 12), fr(3, 12), fr(1, 4)), rnd))
    assert len(its) == 20, len(its)
    return {"title": "Halves, thirds and quarters on the same number line", "items": its}


# ============================================================ set 5: fractions, decimals and percentages in word problems
def set_words(rnd):
    SPOTS.left = []
    its = []
    # 1
    its.append(mcq("Write %s as a percentage." % fr(3, 4), Pc(75), [Pc(34), Pc(25), Pc(F(3, 4))],
                   "%s = %s, because 4 × 25 = 100 and 3 × 25 = 75. So %s = <b>75%%</b>. "
                   "34%% just writes the digits 3 and 4 side by side." % (fr(3, 4), fr(75, 100), fr(3, 4)), rnd))
    # 2
    its.append(mcq("Write %s as a decimal." % fr(2, 5), Dc(F(2, 5)), [Dc(F(25, 100)), Dc(F(5, 2)), Dc(F(4, 100))],
                   "%s = %s (multiply both numbers by 2). 4 tenths = <b>0.4</b>. "
                   "0.25 just writes the digits 2 and 5, and 2.5 is 5 ÷ 2." % (fr(2, 5), fr(4, 10)), rnd))
    # 3
    its.append(mcq("Write 0.6 as a fraction in simplest form.", Fc(3, 5), [Fc(1, 6), Fc(6, 100), Fc(2, 3)],
                   "0.6 is 6 tenths = %s. Divide both numbers by 2: <b>%s</b>. %s is 0.06, not 0.6, and %s is about 0.67."
                   % (fr(6, 10), fr(3, 5), fr(6, 100), fr(2, 3)), rnd))
    # 4
    its.append(mcq("Which percentage is equal to %s?" % fr(1, 5), Pc(20), [Pc(15), Pc(5), Pc(50)],
                   "%s = %s, because 5 × 20 = 100. So %s = <b>20%%</b>." % (fr(1, 5), fr(20, 100), fr(1, 5)), rnd))
    # 5
    its.append(mcq("Write %s as a percentage." % fr(1, 8), Pc(F(25, 2)), [Pc(8), Pc(18), Pc(80)],
                   "%s is half of %s. %s = 25%%, so %s = 25%% ÷ 2 = <b>12.5%%</b>. It is not 8%% or 18%%."
                   % (fr(1, 8), fr(1, 4), fr(1, 4), fr(1, 8)), rnd))
    # 6
    its.append(mcq("Which is <b>not</b> equal to %s?" % fr(1, 2), "0.05", ["0.5", "50%", fr(5, 10)],
                   "%s = %s = 0.5 = 50%%. <b>0.05</b> is 5 hundredths, which is much smaller than one half."
                   % (fr(1, 2), fr(5, 10)), rnd))
    # 7
    trio = [("0.7", F(7, 10)), (fr(3, 4), F(3, 4)), ("65%", F(65, 100))]
    right = sorted(trio, key=lambda x: x[1])
    perms = [", ".join(x[0] for x in p) for p in itertools.permutations(trio)]
    its.append(mcq("Order from smallest to largest:<br>0.7, %s, 65%%" % fr(3, 4), ", ".join(x[0] for x in right),
                   perms,
                   "Write them all as percentages: 0.7 = 70%%, %s = 75%%, 65%%. So the order is <b>65%%, 0.7, %s</b>."
                   % (fr(3, 4), fr(3, 4)), rnd))
    # 8
    four = [Dc(F(35, 100)), Fc(2, 5), Pc(30), Fc(3, 8)]
    assert max(four, key=lambda x: x[1])[1] == F(2, 5)
    its.append(mcq("Which is the greatest?", Fc(2, 5), [four[0], four[2], four[3]],
                   "Write them all as decimals: 0.35, %s = 0.4, 30%% = 0.3, %s = 0.375. "
                   "The greatest is 0.4, so <b>%s</b>." % (fr(2, 5), fr(3, 8), fr(2, 5)), rnd))
    # 9
    sc = {"Mia": F(4, 5), "Leo": F(78, 100), "Zara": F(3, 4)}
    assert max(sc, key=sc.get) == "Mia"
    its.append(mcq("In a maths quiz, Mia scores %s of the marks, Leo scores 78%% and Zara scores 0.75. Who does best?" % fr(4, 5),
                   "Mia", ["Leo", "Zara", "They all score the same"],
                   "Write them all as percentages: %s = 80%%, 78%% and 0.75 = 75%%. So <b>Mia</b> does best." % fr(4, 5), rnd))
    # 10
    assert F(30, 100) > F(1, 4)
    its.append(mcq("The forecast gives a 30%% chance of rain on Saturday and a %s chance on Sunday. "
                   "Which day is more likely to be wet?" % fr(1, 4),
                   "Saturday", ["Sunday", "They are equally likely", CANT],
                   "%s = 25%%, and 30%% is more than 25%%. So rain is more likely on <b>Saturday</b>." % fr(1, 4), rnd))
    # 11
    assert F(1, 2) > F(45, 100)
    its.append(mcq("Kai’s tablet battery shows 45%%. Sienna’s tablet battery is %s full. Whose tablet has more charge?" % fr(1, 2),
                   "Sienna’s", ["Kai’s", "They have the same", CANT],
                   "%s = 50%%, and 50%% is more than 45%%. So <b>Sienna’s</b> tablet has more charge." % fr(1, 2), rnd))
    # 12
    assert F(3, 5) == F(60, 100)
    its.append(mcq("At the swimming carnival, %s of the Year 6 students swim in a race. What percentage is that?" % fr(3, 5),
                   Pc(60), [Pc(35), Pc(30), Pc(F(3, 5))],
                   "%s = %s (multiply both numbers by 20). So <b>60%%</b> of the students swim in a race, "
                   "which is more than half." % (fr(3, 5), fr(60, 100)), rnd))
    # 13
    assert F(2, 3) > F(6, 10)
    its.append(mcq("On Monday the canteen sells 0.6 of its sausage rolls. On Tuesday it sells %s of the same number of "
                   "sausage rolls. On which day does it sell more?" % fr(2, 3),
                   "Tuesday", ["Monday", "They sell the same", CANT],
                   "Use fifteenths: 0.6 = %s = %s and %s = %s. 10 &gt; 9, so it sells more on <b>Tuesday</b>. "
                   "(%s is about 0.67.)" % (fr(3, 5), fr(9, 15), fr(2, 3), fr(10, 15), fr(2, 3)), rnd))
    # 14
    its.append(mcq("Grace has a 1 L water bottle with 750 mL of water in it. What fraction of the bottle is full?",
                   Fc(3, 4), [Fc(1, 4), Fc(7, 10), Fc(4, 5)],
                   "1 L = 1000 mL. %s = %s (divide both numbers by 250). So the bottle is <b>%s</b> full. "
                   "%s is the empty part." % (fr(750, 1000), fr(3, 4), fr(3, 4), fr(1, 4)), rnd))
    # 15
    assert F(3, 8) < F(40, 100)
    its.append(mcq("Mum fills the car with petrol when the tank is below 40%%. The fuel gauge shows %s of a tank. "
                   "Should she fill it now?" % fr(3, 8),
                   "Yes. %s = 37.5%%" % fr(3, 8), ["No. %s is about half a tank" % fr(3, 8),
                                                    "No. %s is more than 40%%" % fr(3, 8), "No. It is exactly 40%"],
                   "%s = 3 ÷ 8 = 0.375 = 37.5%%. 37.5%% is below 40%%, so <b>yes</b>, she should fill it now."
                   % fr(3, 8), rnd))
    # 16
    its.append(mcq("A footy team wins 13 of its 20 games. What percentage of its games does it win?",
                   Pc(65), [Pc(13), Pc(33), Pc(F(65, 100))],
                   "%s = %s (multiply both numbers by 5). So the team wins <b>65%%</b> of its games." % (fr(13, 20), fr(65, 100)), rnd))
    # 17
    run = [("Oliver", F(8, 10)), ("Isla", F(3, 4)), ("Noah", F(7, 10))]
    order = [n for n, v in sorted(run, key=lambda x: -x[1])]
    assert order == ["Oliver", "Isla", "Noah"]
    perms = [", ".join(p) for p in itertools.permutations(["Oliver", "Isla", "Noah"])]
    its.append(mcq("In a fun run, Oliver has run 0.8 km, Isla has run %s km and Noah has run %s km. "
                   "Order them from the furthest to the shortest distance." % (fr(3, 4), fr(7, 10)),
                   ", ".join(order), [", ".join(["Noah", "Isla", "Oliver"]), ", ".join(["Isla", "Oliver", "Noah"])] + perms,
                   "Write them all as decimals: 0.8, %s = 0.75 and %s = 0.7. So the order is <b>Oliver, Isla, Noah</b>."
                   % (fr(3, 4), fr(7, 10)), rnd))
    # 18
    assert F(25, 100) > F(1, 5)
    its.append(mcq("A pair of shoes costs the same price in two shops. Shop A takes 25%% off. Shop B takes %s off. "
                   "Which shop gives the bigger discount?" % fr(1, 5),
                   "Shop A", ["Shop B", "Both are the same", CANT],
                   "%s = 20%%, and 25%% is more than 20%%. So <b>Shop A</b> gives the bigger discount. "
                   "Don’t compare 25 with 5." % fr(1, 5), rnd))
    # 19
    assert F(1, 3) > F(3, 10)
    its.append(mcq("Ava says 0.3 = %s. Is she right?" % fr(1, 3),
                   "No. %s is more than 0.3" % fr(1, 3),
                   ["Yes. They both have a 3", "No. %s is less than 0.3" % fr(1, 3), "Yes. Both are 30%"],
                   "0.3 = %s. In thirtieths: %s = %s and %s = %s. So <b>%s is more than 0.3</b>. "
                   "(%s = 0.333…)" % (fr(3, 10), fr(3, 10), fr(9, 30), fr(1, 3), fr(10, 30), fr(1, 3), fr(1, 3)), rnd))
    # 20
    assert F(5, 8) > F(60, 100)
    its.append(mcq("Liam has read %s of a book. Matilda has read 60%% of the same book. Who has read more?" % fr(5, 8),
                   "Liam", ["Matilda", "They have read the same", CANT],
                   "%s = 5 ÷ 8 = 0.625 = 62.5%%. 62.5%% is more than 60%%, so <b>Liam</b> has read more." % fr(5, 8), rnd))
    assert len(its) == 20, len(its)
    return {"title": "Fractions, decimals and percentages in word problems", "items": its}


# ============================================================ lesson
def body_html():
    return (
        "<h2>Equivalent fractions</h2>"
        "<p>Equivalent fractions show the same amount. <b>Multiply or divide the numerator and the denominator by the same number.</b> "
        "For example, " + fr(2, 3) + " = " + fr(8, 12) + " (× 4). A fraction is in <b>simplest form</b> when the numerator "
        "and the denominator have no common factor except 1: " + fr(16, 24) + " = " + fr(2, 3) + " (÷ 8).</p>"
        "<h2>Compare with a common denominator</h2>"
        "<p>Find a number that both denominators go into. Write both fractions with that denominator. Then compare the numerators.</p>"
        "<figure class='sn-fig'>" + cd_bars_svg(2, 3, 3, 4) +
        "<figcaption>Both bars are cut into twelfths: " + fr(2, 3) + " = " + fr(8, 12) + " and " + fr(3, 4) + " = "
        + fr(9, 12) + ".</figcaption></figure>"
        + ex("Example", "Which is greater: " + fr(2, 3) + " or " + fr(3, 4) + "?",
             "3 and 4 both go into 12. " + fr(2, 3) + " = " + fr(8, 12) + " and " + fr(3, 4) + " = " + fr(9, 12)
             + ". 9 twelfths &gt; 8 twelfths.", fr(3, 4))
        + "<h2>Order fractions, mixed numerals and improper fractions</h2>"
        "<p>Write every number with the same denominator. Change mixed numerals into improper fractions first. "
        "Then put the numerators in order.</p>"
        + ex("Example", "Order " + fr(5, 4) + ", 1 " + fr(1, 3) + " and " + fr(7, 6) + " from smallest to largest.",
             "Use twelfths: " + fr(5, 4) + " = " + fr(15, 12) + ", 1 " + fr(1, 3) + " = " + fr(16, 12) + ", "
             + fr(7, 6) + " = " + fr(14, 12) + ".",
             fr(7, 6) + ", " + fr(5, 4) + ", 1 " + fr(1, 3))
        + "<h2>Halves, thirds and quarters on the same number line</h2>"
        "<p>Cut the line from 0 to 1 into twelfths, because 2, 3 and 4 all go into 12. "
        "Then every half, third and quarter sits on a mark. Numbers further to the right are greater.</p>"
        "<figure class='sn-fig'>" + lesson_line_svg() +
        "<figcaption>" + fr(1, 4) + " = " + fr(3, 12) + ", " + fr(1, 3) + " = " + fr(4, 12) + ", " + fr(1, 2) + " = "
        + fr(6, 12) + ", " + fr(2, 3) + " = " + fr(8, 12) + ", " + fr(3, 4) + " = " + fr(9, 12)
        + ".</figcaption></figure>"
        "<h2>Fractions, decimals and percentages</h2>"
        "<p>To compare a fraction with a decimal or a percentage, write them all the same way.</p>"
        + table(["Fraction", "Decimal", "Percentage"], [
            [fr(1, 2), "0.5", "50%"], [fr(1, 4), "0.25", "25%"], [fr(3, 4), "0.75", "75%"],
            [fr(1, 5), "0.2", "20%"], [fr(1, 10), "0.1", "10%"], [fr(1, 8), "0.125", "12.5%"],
            [fr(1, 3), "about 0.33", "about 33%"]])
        + "<h2>Common mistakes</h2>"
        + table(["Mistake", "What to do instead"], [
            ["Thinking a bigger denominator means a bigger fraction: " + fr(1, 8) + " &gt; " + fr(1, 4),
             "A bigger denominator means <b>smaller</b> parts: " + fr(1, 8) + " &lt; " + fr(1, 4)],
            ["Comparing only the numerators: " + fr(4, 9) + " &gt; " + fr(1, 2) + " because 4 &gt; 1",
             "Use a common denominator: " + fr(4, 9) + " = " + fr(8, 18) + " and " + fr(1, 2) + " = " + fr(9, 18)
             + ", so " + fr(4, 9) + " &lt; " + fr(1, 2)],
            ["Adding the same number to the top and the bottom: " + fr(2, 3) + " = " + fr(4, 5),
             "Multiply both by the same number: " + fr(2, 3) + " = " + fr(4, 6)],
            ["Writing the digits side by side: " + fr(3, 4) + " = 34%",
             fr(3, 4) + " = " + fr(75, 100) + " = 75%"],
        ])
    )


FAQ = [
    {"q": "What do Year 6 students learn about comparing and ordering fractions?",
     "a": "In the Australian Curriculum (AC9M6N03), Year 6 students use equivalent fractions to compare and order common fractions, place halves, thirds and quarters on the same number line, and explain why the order is correct."},
    {"q": "How do you compare fractions with different denominators?",
     "a": "Write both fractions with a common denominator, then compare the numerators. For 2/3 and 3/4, use twelfths: 2/3 = 8/12 and 3/4 = 9/12, so 3/4 is greater."},
    {"q": "How do you put halves, thirds and quarters on the same number line?",
     "a": "Split the line from 0 to 1 into twelfths, because 2, 3 and 4 all go into 12. Then 1/4 = 3/12, 1/3 = 4/12, 1/2 = 6/12, 2/3 = 8/12 and 3/4 = 9/12."},
    {"q": "Do Year 6 students sit NAPLAN?",
     "a": "No. NAPLAN is for Years 3, 5, 7 and 9. Comparing fractions, decimals and percentages in Year 6 helps students get ready for high school and the Year 7 numeracy test."},
]


def gen():
    rnd = random.Random(6803)
    SPOTS.left = []
    sets = [set_equivalent(rnd), set_compare(rnd), set_order(rnd), set_numberline(rnd), set_words(rnd)]
    for s in sets:
        assert len(s["items"]) == 20, (s["title"], len(s["items"]))
        cnt = [0, 0, 0, 0]
        for it in s["items"]:
            assert len(set(it["c"])) == 4, it
            cnt[it["a"]] += 1
        assert cnt == [5, 5, 5, 5], (s["title"], cnt)
    return {
        "country": "au", "subject": "maths", "grade": "year-6", "slug": SLUG, "sort": 3,
        "updated": UPDATED, "pdf_url": "",
        "title": "Year 6 Comparing and Ordering Fractions",
        "seo_title": "Year 6 Comparing and Ordering Fractions Worksheets: Common Denominators, Number Lines and Percentages (Free, with Answer Key)",
        "short_title": "Comparing and ordering fractions",
        "domain": "Number",
        "standard_code": "AC9M6N03",
        "standard_url": "https://v9.australiancurriculum.edu.au/f-10-curriculum/learning-areas/mathematics",
        "standard_text": "Apply knowledge of equivalence to compare, order and represent common fractions including halves, thirds and quarters on the same number line and justify their order",
        "meta_desc": "Free Year 6 maths worksheets on comparing and ordering fractions for the Australian Curriculum (AC9M6N03): equivalent fractions, simplest form, common denominators, mixed numerals, halves, thirds and quarters on the same number line, and fractions as decimals and percentages. 100 questions with an answer key.",
        "key_big": "To compare fractions, write them with a common denominator, then compare the numerators.",
        "key_sub": "2/3 = 8/12 and 3/4 = 9/12, so 2/3 < 3/4. On a number line cut into twelfths, halves, thirds and quarters all sit on a mark.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, SLUG + ".json")
    mark_large(u, "(number line|two number lines|bars of|two bars|two fraction bars|fraction bar)")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(u, f, ensure_ascii=False, indent=1)
    print("wrote", path)
