# -*- coding: utf-8 -*-
"""
AU Year 4 Maths: Equivalent fractions (Australian Curriculum v9.0, AC9M4N03)
  python3 tools/gen_au_maths_y4_equivalent_fractions.py
Equivalent fractions with related denominators only (halves/quarters/eighths,
thirds/sixths/twelfths, fifths/tenths/hundredths): shaded shapes and fraction walls,
missing numerators and denominators, number lines, fractions as decimals (tenths and
hundredths), then word problems in Australian contexts.
Every choice carries its value; a wrong choice never equals the right value or another wrong one.
HTML attributes use single quotes (no backslashes in the JSON). Australian English.
"""
import json, math, os, random, re
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "au", "maths", "year-4")
SLUG = "equivalent-fractions"
UPDATED = "2026-11-02"
FILL = "#4fae74"
BLUE = "#2f6db5"
LINE = "#2b2b2b"
CANT = "You can’t tell"
WORD = {2: "halves", 3: "thirds", 4: "quarters", 5: "fifths", 6: "sixths", 8: "eighths",
        10: "tenths", 12: "twelfths", 100: "hundredths"}
ONE = {2: "half", 3: "third", 4: "quarter", 5: "fifth", 6: "sixth", 8: "eighth",
       10: "tenth", 12: "twelfth", 100: "hundredth"}


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
    return ("%d%s" % (n, unit), F(n))


def Dc(s, unit=""):
    """Decimal choice, written as given (e.g. '0.6')."""
    return (s + unit, F(s))


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
def txt(x, y, s, size=16, color=LINE):
    return ("<text x='%.1f' y='%.1f' font-size='%d' font-weight='700' fill='%s' text-anchor='middle'>%s</text>"
            % (x, y, size, color, s))


def sfr(x, y, a, b, size=14, color=LINE):
    """Stacked fraction drawn in SVG, centred at x. y is the numerator baseline."""
    w = size * 0.62 * max(len(str(a)), len(str(b))) + 4
    return (txt(x, y, a, size, color) +
            "<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='1.5'/>"
            % (x - w / 2, y + 4, x + w / 2, y + 4, color) + txt(x, y + size + 4, b, size, color))


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
                s.append(txt(cx, y + 26, "1"))
            else:
                s.append(sfr(cx, y + 16, 1, d, 14))
    lab = "fraction wall with rows for 1 whole and %s" % ", ".join(WORD[d] for d in dens)
    if shade:
        lab += ", %d %s shaded" % (shade[1], WORD[shade[0]] if shade[1] > 1 else ONE[shade[0]])
    return svg_wrap(W + 12, (len(dens) + 1) * H + 12, "".join(s), lab)


def circle_svg(n, k, r=60):
    cx = cy = r + 6
    s = []
    for i in range(n):
        a0 = math.radians(-90 + 360.0 * i / n)
        a1 = math.radians(-90 + 360.0 * (i + 1) / n)
        x0, y0 = cx + r * math.cos(a0), cy + r * math.sin(a0)
        x1, y1 = cx + r * math.cos(a1), cy + r * math.sin(a1)
        s.append("<path d='M%.1f %.1f L%.1f %.1f A%d %d 0 0 1 %.1f %.1f Z' fill='%s' stroke='%s' stroke-width='2.5' stroke-linejoin='round'/>"
                 % (cx, cy, x0, y0, r, r, x1, y1, FILL if i < k else "#fff", LINE))
    d = 2 * r + 12
    return svg_wrap(d, d, "".join(s), "circle split into %d equal parts with %d shaded" % (n, k))


def rect_svg(rows, cols, k, cell=40):
    s = []
    for r in range(rows):
        for c in range(cols):
            i = r * cols + c
            s.append("<rect x='%d' y='%d' width='%d' height='%d' fill='%s' stroke='%s' stroke-width='2.5'/>"
                     % (6 + c * cell, 6 + r * cell, cell, cell, FILL if i < k else "#fff", LINE))
    return svg_wrap(cols * cell + 12, rows * cell + 12, "".join(s),
                    "rectangle split into %d equal parts with %d shaded" % (rows * cols, k))


def hundred_svg(k, cell=13):
    """10 x 10 grid, k squares shaded column by column."""
    s = []
    for c in range(10):
        for r in range(10):
            i = c * 10 + r
            s.append("<rect x='%d' y='%d' width='%d' height='%d' fill='%s' stroke='%s' stroke-width='1'/>"
                     % (6 + c * cell, 6 + r * cell, cell, cell, FILL if i < k else "#fff", LINE))
    s.append("<rect x='6' y='6' width='%d' height='%d' fill='none' stroke='%s' stroke-width='2.5'/>" % (10 * cell, 10 * cell, LINE))
    return svg_wrap(10 * cell + 12, 10 * cell + 12, "".join(s), "hundredths grid of 100 squares with %d shaded" % k)


def ticks(d, Y, x0, x1, labels=True):
    s = ["<line x1='%.1f' y1='%d' x2='%.1f' y2='%d' stroke='%s' stroke-width='2.5'/>" % (x0, Y, x1, Y, LINE)]
    for i in range(d + 1):
        X = x0 + (x1 - x0) * i / d
        end = i in (0, d)
        s.append("<line x1='%.1f' y1='%d' x2='%.1f' y2='%d' stroke='%s' stroke-width='%s'/>"
                 % (X, Y - (11 if end else 8), X, Y + (11 if end else 8), LINE, "2.5" if end else "1.8"))
        if end and labels:
            s.append(txt(X, Y + 30, str(i // d)))
    return "".join(s)


def tri(X, Y, color=BLUE):
    return "<path d='M%.1f %d L%.1f %d L%.1f %d Z' fill='%s'/>" % (X - 7, Y - 20, X + 7, Y - 20, X, Y - 9, color)


def double_line_svg(b, a, d, W=380):
    """Two number lines 0..1: top in b parts with a marker at a/b, bottom in d parts, dashed guide."""
    x0, x1 = 20, W - 20
    Y1, Y2 = 36, 104
    X = x0 + (x1 - x0) * a / b
    s = [ticks(b, Y1, x0, x1), ticks(d, Y2, x0, x1), tri(X, Y1),
         "<line x1='%.1f' y1='%d' x2='%.1f' y2='%d' stroke='%s' stroke-width='2' stroke-dasharray='5 4'/>"
         % (X, Y1 + 12, X, Y2 - 12, BLUE)]
    return svg_wrap(W, Y2 + 38, "".join(s),
                    "two number lines from 0 to 1 of the same length, the top one in %d equal parts with an arrow at %d of them, "
                    "the bottom one in %d equal parts" % (b, a, d))


def arrow_line_svg(d, k, W=380):
    x0, x1 = 20, W - 20
    Y = 36
    X = x0 + (x1 - x0) * k / d
    s = [ticks(d, Y, x0, x1),
         "<line x1='%.1f' y1='4' x2='%.1f' y2='%d' stroke='%s' stroke-width='3'/>" % (X, X, Y - 18, BLUE), tri(X, Y + 1)]
    return svg_wrap(W, Y + 38, "".join(s), "number line from 0 to 1 in %d equal parts with an arrow" % d)


def letters_line_svg(d, pts, W=380):
    """Number line 0..1 in d parts with letters A-D above the marks pts (sorted)."""
    x0, x1 = 20, W - 20
    Y = 46
    s = [ticks(d, Y, x0, x1)]
    for i, k in enumerate(pts):
        X = x0 + (x1 - x0) * k / d
        s.append(tri(X, Y))
        s.append(txt(X, Y - 24, "ABCD"[i], 17, BLUE))
    return svg_wrap(W, Y + 38, "".join(s),
                    "number line from 0 to 1 in %d equal parts with letters A, B, C and D marked" % d)


# ============================================================ set 1: shapes and fraction walls
def set_shapes(rnd):
    SPOTS.left = []
    its = []
    for a, b, d in [(1, 2, 4), (1, 3, 6), (3, 4, 8), (2, 5, 10), (1, 2, 8), (2, 3, 12)]:
        n = d // b
        c = a * n
        q = (fig(two_bars_svg(b, a, d, c)) + "The bars are the same size and show the same amount.<br>%s = %s"
             % (fr(a, b), frq(d)))
        e = ("The bottom bar has %d equal parts, so each %s of the top bar is split into %d parts. "
             "%s become%s %d × %d = <b>%d</b> %s. So %s = %s."
             % (d, ONE[b], n, parts(a, b), "s" if a == 1 else "", a, n, c, WORD[d], fr(a, b), fr(c, d)))
        its.append(mcq(q, Nc(c), [Nc(a + (d - b)), Nc(a), Nc(d - c), Nc(d), Nc(c + 1), Nc(n), Nc(c + 2)], e, rnd))

    # pizza-style circles: divide
    for d, c, b in [(8, 6, 4), (6, 4, 3), (12, 9, 4), (10, 8, 5)]:
        n = d // b
        a = c // n
        q = (fig(circle_svg(d, c)) + "The circle is cut into %d equal parts. %s is shaded.<br>%s = %s"
             % (d, fr(c, d), fr(c, d), frq(b)))
        e = ("%d ÷ <b>%d</b> = %d, so put the parts in groups of %d. %d shaded parts make %d ÷ %d = <b>%d</b> groups. "
             "So %s = %s." % (d, n, b, n, c, c, n, a, fr(c, d), fr(a, b)))
        its.append(mcq(q, Nc(a), [Nc(c - (d - b)), Nc(c), Nc(b - a), Nc(a + 1), Nc(c + 1)], e, rnd))

    for dens, (sd, k), t in [((2, 4, 8), (2, 1), 8), ((3, 6, 12), (3, 2), 12), ((5, 10), (5, 3), 10), ((3, 6), (3, 1), 6)]:
        n = t // sd
        c = k * n
        q = (fig(wall_svg(dens, (sd, k))) + "Use the fraction wall. %s is shaded. How many %s are equal to %s?"
             % (fr(k, sd), WORD[t], fr(k, sd)))
        e = ("Look straight down the fraction wall. Each %s is the same as %d %s, so %s line%s up with %d × %d = <b>%d</b> %s. "
             "So %s = %s." % (ONE[sd], n, WORD[t], parts(k, sd), "s" if k == 1 else "", k, n, c, WORD[t], fr(k, sd), fr(c, t)))
        its.append(mcq(q, Nc(c), [Nc(k + (t - sd)), Nc(k), Nc(t - c), Nc(c + n), Nc(n), Nc(c + 1)], e, rnd))

    SAME, TOP, BOT = "They are equal", "The top bar has more", "The bottom bar has more"
    for b, a, d, c in [(3, 2, 6, 4), (4, 3, 8, 5), (2, 1, 8, 5)]:
        x, y = F(a, b), F(c, d)
        right = SAME if x == y else (TOP if x > y else BOT)
        if x == y:
            e = ("Both bars are shaded up to the same place. The bottom bar has more parts, but each part is smaller. "
                 "So <b>they are equal</b>: %s = %s." % (fr(a, b), fr(c, d)))
        else:
            eq = (x * d).numerator
            e = ("%s is the same as %s. The bottom bar has %d parts shaded, so <b>the %s bar has more</b>: %s %s %s. "
                 "More parts does not mean more shaded."
                 % (fr(a, b), fr(eq, d), c, "top" if x > y else "bottom", fr(a, b), "&gt;" if x > y else "&lt;", fr(c, d)))
        its.append(mcq(fig(two_bars_svg(b, a, d, c)) + "The bars are the same size. Compare the shaded parts.",
                       right, [SAME, TOP, BOT, CANT], e, rnd))

    # which fraction is equal to the shaded part
    its.append(mcq(fig(circle_svg(12, 3)) + "Which fraction is equal to the shaded part?", Fc(1, 4),
                   [Fc(1, 3), Fc(3, 4), Fc(1, 12)],
                   "%s is shaded. 12 ÷ 3 = 4, so make groups of 3 parts: there are 4 groups and 1 is shaded. "
                   "%s = <b>%s</b>. %s is the part that is not shaded." % (fr(3, 12), fr(3, 12), fr(1, 4), fr(9, 12)), rnd))
    its.append(mcq(fig(rect_svg(2, 5, 4)) + "Which fraction is equal to the shaded part?", Fc(2, 5),
                   [Fc(4, 5), Fc(3, 5), Fc(2, 10)],
                   "%s is shaded. Divide the numerator and the denominator by 2: %s = <b>%s</b>. "
                   "%s only changes the denominator, and %s only changes the numerator." % (fr(4, 10), fr(4, 10), fr(2, 5), fr(4, 5), fr(2, 10)), rnd))
    its.append(mcq(fig(circle_svg(8, 2)) + "Which fraction is equal to the shaded part?", Fc(1, 4),
                   [Fc(2, 4), Fc(1, 8), Fc(3, 4)],
                   "%s is shaded. Divide the numerator and the denominator by 2: %s = <b>%s</b>. "
                   "%s is the part that is not shaded." % (fr(2, 8), fr(2, 8), fr(1, 4), fr(6, 8)), rnd))
    assert len(its) == 20, len(its)
    return {"title": "Equivalent fractions with shapes and fraction walls", "items": its}


# ============================================================ set 2: missing numbers
def set_missing(rnd):
    SPOTS.left = []
    its = []
    for a, b, d in [(1, 4, 8), (3, 4, 8), (1, 3, 12), (2, 3, 12), (5, 6, 12), (3, 5, 10), (4, 5, 10), (9, 10, 100)]:
        n = d // b
        c = a * n
        e = ("Look at the denominators: %d × <b>%d</b> = %d. Multiply the numerator by %d too: %d × %d = <b>%d</b>. "
             "So %s = %s." % (b, n, d, n, a, n, c, fr(a, b), fr(c, d)))
        its.append(mcq("%s = %s" % (fr(a, b), frq(d)), Nc(c),
                       [Nc(a + (d - b)), Nc(a), Nc(d - c), Nc(n), Nc(c + n), Nc(d)], e, rnd))

    for a, b, c in [(1, 3, 2), (3, 4, 6), (2, 5, 4), (1, 2, 6)]:
        n = c // a
        d = b * n
        assert n * a == c
        e = ("Look at the numerators: %d × <b>%d</b> = %d. Multiply the denominator by %d too: %d × %d = <b>%d</b>. "
             "So %s = %s." % (a, n, c, n, b, n, d, fr(a, b), fr(c, d)))
        its.append(mcq("%s = %s" % (fr(a, b), frq_d(c)), Nc(d),
                       [Nc(b + (c - a)), Nc(b), Nc(b * c), Nc(n), Nc(d + n)], e, rnd))

    for a, b, d in [(6, 8, 4), (8, 12, 3), (8, 10, 5), (50, 100, 10)]:
        n = b // d
        c = a // n
        assert F(a, b) == F(c, d)
        e = ("%d ÷ <b>%d</b> = %d, so divide the numerator by %d too: %d ÷ %d = <b>%d</b>. So %s = %s."
             % (b, n, d, n, a, n, c, fr(a, b), fr(c, d)))
        if a - (b - d) > 0:
            e += " Taking %d away from the top and the bottom changes the value." % (b - d)
        its.append(mcq("%s = %s" % (fr(a, b), frq(d)), Nc(c),
                       [Nc(a - (b - d)), Nc(a), Nc(d - c), Nc(c + 1), Nc(d), Nc(a // 2)], e, rnd))

    its.append(mcq("Which fraction is equal to %s?" % fr(2, 3), Fc(8, 12),
                   [Fc(4, 5), Fc(2, 6), Fc(8, 3)],
                   "3 × 4 = 12, so multiply the numerator by 4 too: 2 × 4 = 8. So %s = <b>%s</b>. "
                   "%s adds 2 to both numbers, %s changes only the denominator and %s changes only the numerator."
                   % (fr(2, 3), fr(8, 12), fr(4, 5), fr(2, 6), fr(8, 3)), rnd))
    its.append(mcq("Which fraction is equal to %s?" % fr(4, 5), Fc(8, 10),
                   [Fc(6, 7), Fc(4, 10), Fc(8, 5)],
                   "5 × 2 = 10, so multiply the numerator by 2 too: 4 × 2 = 8. So %s = <b>%s</b>. "
                   "%s adds 2 to both numbers. Adding changes the value." % (fr(4, 5), fr(8, 10), fr(6, 7)), rnd))
    for (a, b), trues, (wa, wb), k in [((1, 2), [(2, 4), (4, 8), (5, 10)], (3, 4), 2), ((3, 4), [(6, 8), (9, 12), (75, 100)], (5, 6), 2)]:
        for t in trues:
            assert F(*t) == F(a, b)
        assert F(wa, wb) != F(a, b) and (wa - a, wb - b) == (k, k)
        its.append(mcq("Which fraction is <b>not</b> equal to %s?" % fr(a, b), fr(wa, wb), [fr(*t) for t in trues],
                       "<b>%s</b> is not equal to %s: %d was added to the numerator and the denominator. Adding changes the value. "
                       "The others are equal, because both numbers were multiplied by the same number (× %d, × %d, × %d)."
                       % (fr(wa, wb), fr(a, b), k, trues[0][1] // b, trues[1][1] // b, trues[2][1] // b), rnd))
    assert len(its) == 20, len(its)
    return {"title": "Find the missing numerator or denominator", "items": its}


# ============================================================ set 3: number lines
def letter_item(a, b, d, rnd):
    n = d // b
    c = a * n
    pref = [a, a + (d - b), c + 1, c - 1, c + 2, c - 2, c + 3, c - 3]
    pref = [p for i, p in enumerate(pref) if 0 < p < d and p != c and p not in pref[:i]]
    lo = [p for p in pref if p < c]
    hi = [p for p in pref if p > c]
    ok = [p for p in range(4) if p <= len(lo) and 3 - p <= len(hi)]
    if not SPOTS.left:
        SPOTS.left = [0, 1, 2, 3]
        rnd.shuffle(SPOTS.left)
    fit = [p for p in SPOTS.left if p in ok]
    assert fit, (a, b, d, SPOTS.left)
    pos = fit[-1]
    SPOTS.left.remove(pos)
    pts = sorted(lo[:pos] + [c] + hi[:3 - pos])
    assert len(pts) == 4 and len(set(pts)) == 4, (a, b, d, pts)
    letter = "ABCD"[pts.index(c)]
    e = ("The line is split into %d equal parts, so each mark is %s. %s = %s (multiply both numbers by %d). "
         "Count %d marks from 0: that is letter <b>%s</b>." % (d, fr(1, d), fr(a, b), fr(c, d), n, c, letter))
    q = fig(letters_line_svg(d, pts)) + "Which letter shows %s?" % fr(a, b)
    return {"q": q, "c": ["A", "B", "C", "D"], "a": pts.index(c), "e": e}


def set_lines(rnd):
    SPOTS.left = []
    its = []
    for a, b, d in [(1, 2, 6), (1, 3, 6), (3, 4, 8), (2, 3, 6), (1, 2, 10), (4, 5, 10), (5, 6, 12), (1, 4, 8)]:
        n = d // b
        c = a * n
        q = (fig(double_line_svg(b, a, d)) + "The number lines are the same length. The arrow shows %s. "
             "Which fraction on the bottom line is at the same point?" % fr(a, b))
        e = ("The bottom line has %d equal parts. Follow the dashed line down and count the marks from 0: %d. "
             "So %s = <b>%s</b> (%d × %d = %d and %d × %d = %d)." % (d, c, fr(a, b), fr(c, d), a, n, c, b, n, d))
        its.append(mcq(q, Fc(c, d), [Fc(a, d), Fc(a + (d - b), d), Fc(c + 1, d), Fc(c - 1, d), Fc(d - c, d)], e, rnd))

    for a, b, d in [(3, 4, 8), (1, 2, 8), (2, 3, 6), (3, 5, 10), (1, 4, 8), (5, 6, 12)]:
        its.append(letter_item(a, b, d, rnd))

    for c, d, b in [(6, 8, 4), (8, 12, 3), (2, 8, 4), (8, 10, 5), (10, 12, 6), (4, 10, 5)]:
        n = d // b
        a = c // n
        assert F(a, b) == F(c, d)
        q = fig(arrow_line_svg(d, c)) + "The arrow points to %s. Which fraction is at the same point?" % fr(c, d)
        e = ("The line has %d equal parts and the arrow is %d marks from 0. Group the marks in %ss: %d ÷ %d = %d groups, "
             "so the line is also split into %s. %d ÷ %d = %d, so %s = <b>%s</b>."
             % (d, c, n, d, n, b, WORD[b], c, n, a, fr(c, d), fr(a, b)))
        its.append(mcq(q, Fc(a, b), [Fc(c, b), Fc(a, d), Fc(c - (d - b), b), Fc(b - a, b), Fc(a + 1, b)], e, rnd))
    assert len(its) == 20, len(its)
    return {"title": "Equivalent fractions on number lines", "items": its}


# ============================================================ set 4: decimals
def set_decimals(rnd):
    SPOTS.left = []
    its = []
    for a, show in [(3, True), (1, True), (4, False), (2, False)]:
        t = 2 * a
        q = ("%s = %s = ?" % (fr(a, 5), fr(t, 10))) if show else "Write %s as a decimal." % fr(a, 5)
        e = ("5 × 2 = 10, so %s = %s. %d tenths is written <b>0.%d</b>. Do not just write the digits %d and 5 as a decimal."
             % (fr(a, 5), fr(t, 10), t, t, a))
        its.append(mcq(q, Dc("0.%d" % t), [Dc("0.%d5" % a), Dc("%d.5" % a), Dc("0.0%d" % t)], e, rnd))
    its.append(mcq("%s = %s = ?" % (fr(1, 2), fr(5, 10)), Dc("0.5"), [Dc("0.12"), Dc("1.2"), Dc("0.05")],
                   "2 × 5 = 10, so %s = %s. 5 tenths is written <b>0.5</b>. 0.12 and 1.2 just join the digits 1 and 2."
                   % (fr(1, 2), fr(5, 10)), rnd))

    its.append(mcq("%s = %s" % (fr(7, 10), frq(100)), Nc(70), [Nc(7), Nc(97), Nc(700)],
                   "10 × 10 = 100, so multiply the numerator by 10 too: 7 × 10 = <b>70</b>. So %s = %s. "
                   "Both are 0.7." % (fr(7, 10), fr(70, 100)), rnd))
    its.append(mcq("0.9 = %s" % frq(100), Nc(90), [Nc(9), Nc(900), Nc(10)],
                   "0.9 is 9 tenths, %s. 10 × 10 = 100, so 9 × 10 = <b>90</b>. So 0.9 = %s = %s."
                   % (fr(9, 10), fr(9, 10), fr(90, 100)), rnd))
    its.append(mcq("%s = %s = ?" % (fr(1, 4), fr(25, 100)), Dc("0.25"), [Dc("0.14"), Dc("1.4"), Dc("0.4")],
                   "%s is 25 hundredths, written <b>0.25</b>. 0.14 and 1.4 just join the digits, and 0.4 is 4 tenths."
                   % fr(25, 100), rnd))
    its.append(mcq("%s = %s" % (fr(3, 4), frq(100)), Nc(75), [Nc(3), Nc(25), Nc(34)],
                   "4 × 25 = 100, so multiply the numerator by 25 too: 3 × 25 = <b>75</b>. So %s = %s = 0.75. "
                   "25 is the part that is left." % (fr(3, 4), fr(75, 100)), rnd))
    its.append(mcq("Which fraction is equal to 0.4?", Fc(2, 5), [Fc(1, 4), Fc(4, 100), Fc(4, 5)],
                   "0.4 is 4 tenths, %s. Divide the numerator and the denominator by 2: %s = <b>%s</b>. "
                   "%s is 0.04, and %s is 0.25." % (fr(4, 10), fr(4, 10), fr(2, 5), fr(4, 100), fr(1, 4)), rnd))
    its.append(mcq("Which fraction is equal to 0.75?", Fc(3, 4), [Fc(7, 5), Fc(75, 10), Fc(1, 4)],
                   "0.75 is 75 hundredths, %s. 100 ÷ 25 = 4 and 75 ÷ 25 = 3, so %s = <b>%s</b>. %s is 0.25, the part that is left."
                   % (fr(75, 100), fr(75, 100), fr(3, 4), fr(1, 4)), rnd))
    its.append(mcq("0.8 = %s" % frq(5), Nc(4), [Nc(8), Nc(16), Nc(1)],
                   "0.8 is 8 tenths, %s. 10 ÷ 2 = 5, so divide the numerator by 2 too: 8 ÷ 2 = <b>4</b>. So 0.8 = %s."
                   % (fr(8, 10), fr(4, 5)), rnd))

    its.append(mcq(fig(hundred_svg(60)) + "The grid has 100 equal squares. Which decimal shows the shaded part?",
                   Dc("0.6"), [Dc("0.06"), Dc("6"), Dc("0.4")],
                   "60 of 100 squares are shaded: %s = %s. 6 tenths is <b>0.6</b>. 0.4 is the part that is not shaded."
                   % (fr(60, 100), fr(6, 10)), rnd))
    its.append(mcq(fig(hundred_svg(25)) + "The grid has 100 equal squares. Which decimal shows the shaded part?",
                   Dc("0.25"), [Dc("2.5"), Dc("0.75"), Dc("25")],
                   "25 of 100 squares are shaded: %s, which is written <b>0.25</b>. It is also %s."
                   % (fr(25, 100), fr(1, 4)), rnd))
    its.append(mcq(fig(hundred_svg(30)) + "Which of these is <b>not</b> equal to the shaded part?",
                   fr(3, 100), [fr(3, 10), fr(30, 100), "0.3"],
                   "30 of 100 squares are shaded: %s = %s = 0.3. <b>%s</b> would be only 3 squares."
                   % (fr(30, 100), fr(3, 10), fr(3, 100)), rnd))
    assert F(1, 5) != F(1, 2)
    its.append(mcq("Which of these is <b>not</b> equal to 0.5?", fr(1, 5), [fr(1, 2), fr(5, 10), fr(50, 100)],
                   "0.5 = %s = %s = %s. <b>%s</b> = %s = 0.2, so it is not equal to 0.5."
                   % (fr(5, 10), fr(50, 100), fr(1, 2), fr(1, 5), fr(2, 10)), rnd))
    its.append(mcq("Which of these is <b>not</b> equal to %s?" % fr(3, 5), "0.35", [fr(6, 10), "0.6", fr(60, 100)],
                   "%s = %s = %s = 0.6. <b>0.35</b> just joins the digits 3 and 5, so it is not equal."
                   % (fr(3, 5), fr(6, 10), fr(60, 100)), rnd))
    its.append(mcq(fig(arrow_line_svg(10, 7)) + "The line is split into tenths. Which decimal does the arrow show?",
                   Dc("0.7"), [Dc("0.07"), Dc("7"), Dc("0.3"), Dc("0.8")],
                   "Each mark is %s = 0.1. The arrow is 7 marks from 0, so it shows %s = <b>0.7</b>." % (fr(1, 10), fr(7, 10)), rnd))
    its.append(mcq(fig(arrow_line_svg(5, 4)) + "The line is split into fifths. Which decimal does the arrow show?",
                   Dc("0.8"), [Dc("0.4"), Dc("0.45"), Dc("4.5")],
                   "The arrow shows %s. 5 × 2 = 10, so %s = %s = <b>0.8</b>. The line has fifths, not tenths, so 0.4 is wrong."
                   % (fr(4, 5), fr(4, 5), fr(8, 10)), rnd))
    assert F(3, 5) > F(1, 2)
    its.append(mcq("Which is greater: %s or 0.5?" % fr(3, 5), fr(3, 5), ["0.5", "They are equal", CANT],
                   "%s = %s = 0.6. 0.6 is more than 0.5, so <b>%s</b> is greater." % (fr(3, 5), fr(6, 10), fr(3, 5)), rnd))
    assert len(its) == 20, len(its)
    return {"title": "Fractions as decimals: tenths and hundredths", "items": its}


# ============================================================ set 5: word problems
def set_words(rnd):
    SPOTS.left = []
    its = []
    # 1
    its.append(mcq("A pizza is cut into 8 equal slices. Jack eats %s of the pizza. How many slices does he eat?" % fr(3, 4),
                   Nc(6, " slices"), [Nc(3, " slices"), Nc(7, " slices"), Nc(2, " slices")],
                   "4 × 2 = 8, so %s = %s. Jack eats <b>6 slices</b>." % (fr(3, 4), fr(6, 8)), rnd))
    # 2
    its.append(mcq("A tray holds 12 lamingtons. Oliver’s family eats %s of the tray. How many lamingtons do they eat?" % fr(2, 3),
                   Nc(8, " lamingtons"), [Nc(2, " lamingtons"), Nc(11, " lamingtons"), Nc(4, " lamingtons")],
                   "3 × 4 = 12, so multiply the numerator by 4 too: %s = %s. They eat <b>8 lamingtons</b>." % (fr(2, 3), fr(8, 12)), rnd))
    # 3
    its.append(mcq("A 2 L bottle of juice is poured equally into 10 cups. How much juice is in each cup?",
                   Dc("0.2", " L"), [Dc("5", " L"), Dc("0.5", " L"), Dc("0.02", " L")],
                   "Each cup gets %s L. Divide both numbers by 2: %s = %s = <b>0.2 L</b>." % (fr(2, 10), fr(2, 10), fr(1, 5)), rnd))
    # 4
    its.append(mcq("Mia and Leo share a 2 L bottle of water. Mia drinks 0.5 L and Leo drinks %s L. Who drinks more?" % fr(1, 2),
                   "They drink the same", ["Mia", "Leo", CANT],
                   "%s = %s = 0.5. So <b>they drink the same</b> amount." % (fr(1, 2), fr(5, 10)), rnd))
    # 5
    its.append(mcq("A 2 L bottle of lemonade is shared equally by 4 friends. Each friend gets %s L. "
                   "Which is the same amount?" % fr(2, 4),
                   Dc("0.5", " L"), [Dc("0.24", " L"), Dc("2.4", " L"), Dc("0.2", " L")],
                   "%s = %s = %s, which is <b>0.5 L</b>. 0.24 and 2.4 just join the digits." % (fr(2, 4), fr(1, 2), fr(5, 10)), rnd))
    # 6
    its.append(mcq("Noah says %s = %s, because he added 2 to the top and the bottom. Is he right?" % (fr(2, 3), fr(4, 5)),
                   "No. %s = %s" % (fr(2, 3), fr(4, 6)),
                   ["Yes. He added the same number", "No. %s = %s" % (fr(2, 3), fr(4, 3)), "No. %s = %s" % (fr(2, 3), fr(2, 6))],
                   "Adding the same number changes the value. Multiply both numbers by 2 instead: %s = <b>%s</b>."
                   % (fr(2, 3), fr(4, 6)), rnd))
    # 7
    its.append(mcq("Ruby says %s = %s, because the numerators are the same. Is she right?" % (fr(3, 4), fr(3, 8)),
                   "No. %s = %s" % (fr(3, 4), fr(6, 8)),
                   ["Yes. The numerators are the same", "No. %s = %s" % (fr(3, 4), fr(7, 8)), "No. %s = %s" % (fr(3, 4), fr(3, 2))],
                   "Ruby changed only the denominator. Eighths are smaller than quarters, so she needs more of them. "
                   "Multiply both numbers by 2: %s = <b>%s</b>." % (fr(3, 4), fr(6, 8)), rnd))
    # 8
    its.append(mcq("At footy training, Cooper runs %s of a lap and Kai runs %s of a lap. Who runs further?" % (fr(3, 4), fr(6, 8)),
                   "They run the same", ["Cooper", "Kai", CANT],
                   "Multiply both numbers in %s by 2: %s = %s. So <b>they run the same</b> distance." % (fr(3, 4), fr(3, 4), fr(6, 8)), rnd))
    # 9
    its.append(mcq("At netball, Amelia scores 4 goals from 10 shots. Which fraction in fifths shows the shots she scored?",
                   Fc(2, 5), [Fc(4, 5), Fc(3, 5), Fc(1, 5)],
                   "She scored %s of her shots. Divide both numbers by 2: %s = <b>%s</b>. %s are the shots she missed."
                   % (fr(4, 10), fr(4, 10), fr(2, 5), fr(3, 5)), rnd))
    # 10
    its.append(mcq("In a Year 4 class, %s of the students walk to school. Write this as a decimal." % fr(6, 10),
                   Dc("0.6"), [Dc("6.1"), Dc("0.06"), Dc("0.4")],
                   "%s is 6 tenths, written <b>0.6</b>. 0.4 is the students who do not walk." % fr(6, 10), rnd))
    # 11
    its.append(mcq("Grace has a 1 m ribbon. She cuts off 0.25 m. What fraction of a metre does she cut off?",
                   Fc(1, 4), [Fc(2, 5), Fc(1, 2), Fc(25, 10)],
                   "0.25 m = %s m. 25 × 4 = 100, so %s = <b>%s</b>." % (fr(25, 100), fr(25, 100), fr(1, 4)), rnd))
    # 12
    assert F(1, 3) > F(3, 12)
    its.append(mcq("A block of chocolate has 12 equal pieces. Liam eats %s of the block and Sienna eats %s. Who eats more?"
                   % (fr(1, 3), fr(3, 12)),
                   "Liam", ["Sienna", "They eat the same", CANT],
                   "%s = %s, so Liam eats 4 pieces. Sienna eats 3 pieces. <b>Liam</b> eats more." % (fr(1, 3), fr(4, 12)), rnd))
    # 13
    its.append(mcq("At the sausage sizzle, a tray holds 10 sausages. %s of them are cooked. How many sausages are cooked?" % fr(4, 5),
                   Nc(8, " sausages"), [Nc(4, " sausages"), Nc(9, " sausages"), Nc(2, " sausages")],
                   "5 × 2 = 10, so %s = %s. <b>8 sausages</b> are cooked." % (fr(4, 5), fr(8, 10)), rnd))
    # 14
    its.append(mcq("At the swimming carnival, Charlotte has swum 50 m of a 100 m race. Which fraction of the race has she swum?",
                   Fc(1, 2), [Fc(5, 100), Fc(1, 5), Fc(50, 10)],
                   "She has swum %s of the race. 50 × 2 = 100, so %s = <b>%s</b>." % (fr(50, 100), fr(50, 100), fr(1, 2)), rnd))
    # 15
    its.append(mcq("A cake is cut into 6 equal pieces. Mum keeps %s of the cake for tomorrow. How many pieces is that?" % fr(1, 3),
                   Nc(2, " pieces"), [Nc(1, " piece"), Nc(4, " pieces"), Nc(3, " pieces")],
                   "3 × 2 = 6, so %s = %s. That is <b>2 pieces</b>." % (fr(1, 3), fr(2, 6)), rnd))
    # 16
    its.append(mcq("Kai has 10 apples. 7 of them are green. Which decimal shows the part that is green?",
                   Dc("0.7"), [Dc("0.07"), Dc("7.1"), Dc("0.3")],
                   "7 out of 10 is %s, which is written <b>0.7</b>. 0.3 is the part that is not green." % fr(7, 10), rnd))
    # 17
    its.append(mcq("How many cents is %s of $1?" % fr(3, 4),
                   Nc(75, "c"), [Nc(34, "c"), Nc(30, "c"), Nc(25, "c")],
                   "$1 is 100 cents. 4 × 25 = 100, so %s = %s. That is <b>75c</b>." % (fr(3, 4), fr(75, 100)), rnd))
    # 18
    its.append(mcq("The school vegetable garden has 100 equal squares. 30 squares have tomatoes. "
                   "Mei says that is 0.3 of the garden. Is she right?",
                   "Yes. %s = %s = 0.3" % (fr(30, 100), fr(3, 10)),
                   ["No. It is 0.03", "No. It is 3.0", "No. It is 0.7"],
                   "30 of 100 squares is %s. Divide both numbers by 10: %s = 0.3. <b>Yes</b>, she is right."
                   % (fr(30, 100), fr(3, 10)), rnd))
    # 19
    its.append(mcq("Matilda eats %s of a pizza. Aarav eats %s of a pizza of the same size. Who eats more?" % (fr(2, 8), fr(1, 4)),
                   "They eat the same", ["Matilda", "Aarav", CANT],
                   "Divide both numbers in %s by 2: %s = %s. So <b>they eat the same</b> amount." % (fr(2, 8), fr(2, 8), fr(1, 4)), rnd))
    # 20
    assert F(4, 10) == F(2, 5) == F("0.4")
    its.append(mcq("Three students run around the oval. Oliver runs 0.4 km, Ava runs %s km and Jack runs %s km. "
                   "Who runs the furthest?" % (fr(2, 5), fr(4, 10)),
                   "They all run the same", ["Oliver", "Ava", "Jack"],
                   "%s = %s = 0.4. All three distances are the same, so <b>they all run the same</b>."
                   % (fr(2, 5), fr(4, 10)), rnd))
    assert len(its) == 20, len(its)
    return {"title": "Equivalent fraction word problems", "items": its}


# ============================================================ lesson
def body_html():
    return (
        "<h2>What are equivalent fractions?</h2>"
        "<p><b>Equivalent fractions</b> are worth the same amount, but use different numbers. "
        "A <b>fraction wall</b> shows them: look straight down to see which fractions line up.</p>"
        "<figure class='sn-fig'>" + wall_svg((2, 4, 8), (4, 3)) +
        "<figcaption>" + fr(3, 4) + " lines up with " + fr(6, 8) + ". Also " + fr(1, 2) + " = " + fr(2, 4) + " = " + fr(4, 8)
        + ".</figcaption></figure>"
        "<h2>Multiply or divide both numbers</h2>"
        "<p>To find an equivalent fraction, <b>multiply or divide the numerator and the denominator by the same number</b>. "
        "Use related denominators: halves, quarters and eighths; thirds, sixths and twelfths; fifths, tenths and hundredths.</p>"
        + ex("Example", fr(2, 3) + " = " + frq(12),
             "3 × 4 = 12, so multiply the numerator by 4 too: 2 × 4 = 8.", "8")
        + "<figure class='sn-fig'>" + two_bars_svg(3, 2, 12, 8) +
        "<figcaption>Each third is split into 4 twelfths, so " + fr(2, 3) + " = " + fr(8, 12) + ".</figcaption></figure>"
        + ex("Example", fr(6, 8) + " = " + frq(4), "8 ÷ 2 = 4, so divide the numerator by 2 too: 6 ÷ 2 = 3.", "3")
        + "<h2>On a number line</h2>"
        "<p>Equivalent fractions sit at the <b>same point</b> on number lines of the same length.</p>"
        "<figure class='sn-fig'>" + double_line_svg(4, 3, 8) +
        "<figcaption>" + fr(3, 4) + " (top) and " + fr(6, 8) + " (bottom) are at the same point.</figcaption></figure>"
        "<h2>Fractions and decimals</h2>"
        "<p>Change the fraction to <b>tenths</b> or <b>hundredths</b>, then write it as a decimal. "
        "Tenths have one digit after the decimal point. Hundredths have two.</p>"
        + ex("Example", "Write " + fr(3, 5) + " as a decimal.",
             "5 × 2 = 10, so " + fr(3, 5) + " = " + fr(6, 10) + ". 6 tenths = 0.6.", "0.6")
        + "<figure class='sn-fig'>" + hundred_svg(25) +
        "<figcaption>25 of 100 squares: " + fr(25, 100) + " = " + fr(1, 4) + " = 0.25.</figcaption></figure>"
        + "<h2>Common mistakes</h2>"
        + table(["Mistake", "What to do instead"], [
            ["Adding the same number to the top and the bottom: " + fr(2, 3) + " = " + fr(4, 5),
             "Multiply both by the same number: " + fr(2, 3) + " = " + fr(4, 6)],
            ["Changing only one part: " + fr(3, 4) + " = " + fr(3, 8),
             "Change <b>both</b> numbers: " + fr(3, 4) + " = " + fr(6, 8)],
            ["Writing the digits as a decimal: " + fr(3, 5) + " = 0.35",
             "Make tenths first: " + fr(3, 5) + " = " + fr(6, 10) + " = 0.6"],
            ["Mixing up tenths and hundredths: " + fr(6, 100) + " = 0.6",
             fr(6, 100) + " = 0.06, but " + fr(6, 10) + " = 0.6"],
        ])
    )


FAQ = [
    {"q": "What do Year 4 students learn about equivalent fractions?",
     "a": "In the Australian Curriculum (AC9M4N03), Year 4 students find equivalent fractions with related denominators, such as 1/2 = 2/4 = 4/8 and 1/3 = 2/6 = 4/12. They also connect fractions to decimals, for example 3/5 = 6/10 = 0.6."},
    {"q": "How do you find an equivalent fraction?",
     "a": "Multiply or divide the numerator and the denominator by the same number. For 3/4 = ?/8, 4 × 2 = 8, so 3 × 2 = 6 and 3/4 = 6/8. Never add the same number to both."},
    {"q": "How do you change a fraction into a decimal in Year 4?",
     "a": "Make an equivalent fraction with a denominator of 10 or 100, then write it as tenths or hundredths. For example, 3/5 = 6/10 = 0.6 and 1/4 = 25/100 = 0.25."},
    {"q": "Do Year 4 students sit NAPLAN?",
     "a": "No. NAPLAN is for Years 3, 5, 7 and 9. Equivalent fractions and decimals in Year 4 build the skills students need for the Year 5 NAPLAN numeracy test."},
]


def gen():
    rnd = random.Random(4803)
    SPOTS.left = []
    sets = [set_shapes(rnd), set_missing(rnd), set_lines(rnd), set_decimals(rnd), set_words(rnd)]
    for s in sets:
        assert len(s["items"]) == 20, (s["title"], len(s["items"]))
        cnt = [0, 0, 0, 0]
        for it in s["items"]:
            assert len(set(it["c"])) == 4, it
            cnt[it["a"]] += 1
        assert cnt == [5, 5, 5, 5], (s["title"], cnt)
    return {
        "country": "au", "subject": "maths", "grade": "year-4", "slug": SLUG, "sort": 3,
        "updated": UPDATED, "pdf_url": "",
        "title": "Year 4 Equivalent Fractions",
        "seo_title": "Year 4 Equivalent Fractions Worksheets: Fraction Walls, Number Lines and Decimals (Free, with Answer Key)",
        "short_title": "Equivalent fractions",
        "domain": "Number",
        "standard_code": "AC9M4N03",
        "standard_url": "https://v9.australiancurriculum.edu.au/f-10-curriculum/learning-areas/mathematics",
        "standard_text": "Find equivalent representations of fractions using related denominators and make connections between fractions and decimal notation",
        "meta_desc": "Free Year 4 maths worksheets on equivalent fractions for the Australian Curriculum (AC9M4N03): shaded shapes, fraction walls, missing numerators and denominators, number lines, tenths, hundredths and decimals, and word problems. 100 questions with an answer key.",
        "key_big": "Equivalent fractions: multiply or divide the numerator and the denominator by the same number.",
        "key_sub": "3/4 = 6/8, because 3 × 2 = 6 and 4 × 2 = 8. Never add the same number to both: 2/3 is not 4/5. To write a decimal, make tenths or hundredths first: 3/5 = 6/10 = 0.6.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, SLUG + ".json")
    mark_large(u, "(number line|two number lines|two bars|fraction wall)")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(u, f, ensure_ascii=False, indent=1)
    print("wrote", path)
