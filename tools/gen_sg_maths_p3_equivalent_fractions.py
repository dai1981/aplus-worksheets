# -*- coding: utf-8 -*-
"""
Singapore Primary 3 Maths: Equivalent Fractions
(MOE 2021 Primary Mathematics Syllabus, Standard. Primary 3: Fractions)
  python3 tools/gen_sg_maths_p3_equivalent_fractions.py
Equivalent fractions with fraction bars, circles and fraction walls; multiplying and dividing the
numerator and denominator; simplest form; missing numerators and denominators; comparing and ordering
unlike fractions (denominators up to 12) and word problems with bar models.
Wrong choices come from real mistakes (adding the same number to the top and bottom, thinking 1/8 > 1/4,
not simplifying fully, changing only the numerator or only the denominator) and are never equal in value
to the answer or to each other. Every answer is checked in code with fractions.Fraction.
HTML attributes use single quotes (no backslashes in the JSON). Singapore English.
"""
import json, math, os, random, re
from fractions import Fraction

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "sg", "maths", "primary-3")
UPDATED = "2026-11-03"
FILL = "#4fae74"      # shaded parts
FILL2 = "#f2b84b"     # second colour
FILL3 = "#8fb8e8"     # bar models
LINE = "#2b2b2b"
WALL = ["#d7e6f7", "#cfe9d8", "#fbe3b4", "#f3d1d1"]
WORD = {2: "halves", 3: "thirds", 4: "quarters", 5: "fifths", 6: "sixths", 7: "sevenths", 8: "eighths", 9: "ninths",
        10: "tenths", 11: "elevenths", 12: "twelfths"}
SIMPLE = "<br>Give your answer in its simplest form."


# ------------------------------------------------------------ numbers
def fr(a, b):
    return "<span class='fr'><span class='fn'>%s</span><span class='fd'>%s</span></span>" % (a, b)


def show(v):
    """A proper Fraction in simplest form."""
    return fr(v.numerator, v.denominator)


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


def place(q, cs, pick, e, rnd):
    assert len(pick) == 3, (q, cs, pick)
    rnd.shuffle(pick)
    pos = SPOTS.next(rnd)
    ch = pick[:pos] + [cs] + pick[pos:]
    assert len(set(ch)) == 4, ch
    return {"q": q, "c": ch, "a": ch.index(cs), "e": e}


def mcq(q, correct, cands, e, rnd):
    """String answer and string candidates (the first 3 new ones are used)."""
    seen, pick = {correct}, []
    for c in cands:
        if c is None or c in seen:
            continue
        seen.add(c)
        pick.append(c)
        if len(pick) == 3:
            break
    return place(q, correct, pick, e, rnd)


def mcq_n(q, correct, cands, e, rnd):
    """Whole-number answer; candidates that are 0 or less or repeat are skipped."""
    return mcq(q, str(correct), [str(c) for c in cands if c is not None and c > 0], e, rnd)


def mcq_fr(q, ans, cands, e, rnd):
    """ans and cands are (n, d) pairs shown as written (not simplified).
    A candidate equal in VALUE to the answer or to another choice is skipped."""
    av = Fraction(*ans)
    vals, pick = {av}, []
    for c in cands:
        if c is None:
            continue
        n, d = c
        if n <= 0 or d <= 0 or Fraction(n, d) in vals:
            continue
        vals.add(Fraction(n, d))
        pick.append(fr(n, d))
        if len(pick) == 3:
            break
    return place(q, fr(*ans), pick, e, rnd)


def mcq_letters(q, pos, e):
    """Choices A-D for a picture; pos is where the right picture was drawn."""
    ch = ["A", "B", "C", "D"]
    return {"q": q, "c": ch, "a": pos, "e": e}


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
    """Tag pictures that must print larger so their parts stay readable."""
    rx = re.compile(r"<svg (?=[^>]*aria-label='" + pattern + ")")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u


# ------------------------------------------------------------ SVG text
def txt(x, y, s, size=15, anchor="middle", weight="700", color=LINE):
    return ("<text x='%.1f' y='%.1f' font-size='%d' font-weight='%s' fill='%s' text-anchor='%s'>%s</text>"
            % (x, y, size, weight, color, anchor, s))


def sfr(x, y, a, b, size=15, color=LINE):
    """Stacked fraction drawn in SVG, centred at x. y is the numerator baseline."""
    w = size * 0.62 * max(len(str(a)), len(str(b))) + 4
    return (txt(x, y, a, size, color=color) +
            "<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='1.6'/>"
            % (x - w / 2, y + 5, x + w / 2, y + 5, color) + txt(x, y + size + 5, b, size, color=color))


def brace(x0, x1, y, up=True):
    """Curly brace from x0 to x1 at height y. up=True: the point is above."""
    m = (x0 + x1) / 2
    k = -8 if up else 8
    return ("<path d='M%.1f %.1f Q%.1f %.1f %.1f %.1f L%.1f %.1f Q%.1f %.1f %.1f %.1f "
            "Q%.1f %.1f %.1f %.1f L%.1f %.1f Q%.1f %.1f %.1f %.1f' fill='none' stroke='%s' stroke-width='1.8'/>"
            % (x0, y, x0, y + k, x0 + 8, y + k, m - 6, y + k, m, y + k, m, y + 2 * k,
               m, y + k, m + 6, y + k, x1 - 8, y + k, x1, y + k, x1, y, LINE))


# ------------------------------------------------------------ pictures
def bar_cells(x0, y0, W, Hh, d, k, col=FILL, sw=2.2):
    s = "".join("<rect x='%.2f' y='%.1f' width='%.2f' height='%d' fill='%s' stroke='%s' stroke-width='%.1f'/>"
                % (x0 + i * W / d, y0, W / d, Hh, col if i < k else "#fff", LINE, sw) for i in range(d))
    return s + ("<rect x='%.2f' y='%.1f' width='%.2f' height='%d' fill='none' stroke='%s' stroke-width='3'/>"
                % (x0, y0, W, Hh, LINE))


def bars_svg(rows, W=264, Hh=36, gap=12, name="bars"):
    """rows: list of (d, k, label). label is a pair (n, d) drawn as a fraction, a string ('A', '?') or None.
    All bars have the same length, so equal shaded lengths mean equal fractions."""
    has = any(r[2] is not None for r in rows)
    x0 = 50 if has else 6
    s = []
    for j, (d, k, lab) in enumerate(rows):
        y = 6 + j * (Hh + gap)
        s.append(bar_cells(x0, y, W, Hh, d, k))
        yc = y + Hh / 2
        if isinstance(lab, tuple):
            s.append(sfr(24, yc - 5, lab[0], lab[1], 15))
        elif lab:
            s.append(txt(24, yc + 6, lab, 18))
    n = len(rows)
    desc = "; ".join("%d of %d parts shaded" % (k, d) for d, k, _ in rows)
    return svg_wrap(x0 + W + 6, 12 + n * Hh + (n - 1) * gap, "".join(s), "%s of the same length: %s" % (name, desc))


def group_bar_svg(d, k, g, W=264, Hh=40):
    """One bar of d parts, k shaded, with thick lines that put the parts into groups of g."""
    s = [bar_cells(6, 6, W, Hh, d, k)]
    for i in range(g, d, g):
        x = 6 + W * i / d
        s.append("<line x1='%.2f' y1='2' x2='%.2f' y2='%d' stroke='%s' stroke-width='5'/>" % (x, x, Hh + 10, LINE))
    return svg_wrap(W + 12, Hh + 12, "".join(s),
                    "bar of %d equal parts, %d shaded, thick lines make groups of %d" % (d, k, g))


def wall_svg(ds, W=336, Hh=42):
    """Fraction wall: one row for each denominator in ds (1 = the whole)."""
    s = []
    for j, d in enumerate(ds):
        y = 6 + j * Hh
        for i in range(d):
            x = 6 + i * W / d
            s.append("<rect x='%.2f' y='%d' width='%.2f' height='%d' fill='%s' stroke='%s' stroke-width='2'/>"
                     % (x, y, W / d, Hh, WALL[j % 4], LINE))
            if d == 1:
                s.append(txt(x + W / 2, y + Hh / 2 + 6, "1", 17))
            else:
                s.append(sfr(x + W / d / 2, y + Hh / 2 - 5, 1, d, 14))
    s.append("<rect x='6' y='6' width='%d' height='%d' fill='none' stroke='%s' stroke-width='3'/>" % (W, len(ds) * Hh, LINE))
    return svg_wrap(W + 12, len(ds) * Hh + 12, "".join(s),
                    "fraction wall with rows of " + ", ".join(WORD.get(d, "1 whole") for d in ds))


def pie_body(cx, cy, R, d, k):
    s = []
    for i in range(d):
        a0 = -math.pi / 2 + 2 * math.pi * i / d
        a1 = a0 + 2 * math.pi / d
        s.append("<path d='M%.1f %.1f L%.2f %.2f A%.1f %.1f 0 0 1 %.2f %.2f Z' fill='%s' stroke='%s' stroke-width='2.2'/>"
                 % (cx, cy, cx + R * math.cos(a0), cy + R * math.sin(a0), R, R,
                    cx + R * math.cos(a1), cy + R * math.sin(a1), FILL if i < k else "#fff", LINE))
    s.append("<circle cx='%.1f' cy='%.1f' r='%.1f' fill='none' stroke='%s' stroke-width='3'/>" % (cx, cy, R, LINE))
    return "".join(s)


def pies_svg(pies, R=44):
    s = [pie_body(6 + R + j * (2 * R + 24), 6 + R, R, d, k) for j, (d, k) in enumerate(pies)]
    n = len(pies)
    lab = "circles of the same size: " + "; ".join("%d of %d slices shaded" % (k, d) for d, k in pies)
    return svg_wrap(12 + n * 2 * R + (n - 1) * 24, 12 + 2 * R, "".join(s), lab)


def units_svg(units, shaded, top, bottom, W=264, Hh=36):
    """Bar model: a bar of equal units, the first `shaded` units coloured.
    top labels the whole bar (brace above), bottom labels the shaded units (brace below)."""
    s = [txt(6 + W / 2, 18, top, 16), brace(6, 6 + W, 48, up=True)]
    yb = 56
    for i in range(units):
        s.append("<rect x='%.2f' y='%d' width='%.2f' height='%d' fill='%s' stroke='%s' stroke-width='2.2'/>"
                 % (6 + i * W / units, yb, W / units, Hh, FILL3 if i < shaded else "#fff", LINE))
    xs = 6 + W * shaded / units
    s.append(brace(8, xs - 2, yb + Hh + 6, up=False))
    s.append(txt((6 + xs) / 2, yb + Hh + 40, bottom, 16))
    assert 9 * len(bottom) < xs + 40, bottom
    return svg_wrap(W + 12, yb + Hh + 50, "".join(s),
                    "bar model of %d equal units, %d shaded" % (units, shaded))


# ------------------------------------------------------------ explanations
def e_times(n, d, k):
    return ("Multiply the numerator and the denominator by %d: %d × %d = %d and %d × %d = %d. So %s = <b>%s</b>."
            % (k, n, k, n * k, d, k, d * k, fr(n, d), fr(n * k, d * k)))


def e_div(n, d, k):
    return ("Divide the numerator and the denominator by %d: %d ÷ %d = %d and %d ÷ %d = %d. So %s = <b>%s</b>."
            % (k, n, k, n // k, d, k, d // k, fr(n, d), fr(n // k, d // k)))


def e_simplest(n, d):
    g = math.gcd(n, d)
    return ("%d and %d can both be divided by %d. %d ÷ %d = %d and %d ÷ %d = %d. "
            "1 is the only number that divides both %d and %d, so %s is in simplest form. %s = <b>%s</b>."
            % (n, d, g, n, g, n // g, d, g, d // g, n // g, d // g, fr(n // g, d // g), fr(n, d), fr(n // g, d // g)))


# ============================================================ set 1: fraction bars
def set_bars(rnd):
    SPOTS.left = []
    its = []
    # A: what fraction of the bottom bar is shaded?
    for n1, d1, n2, d2 in [(1, 2, 3, 6), (1, 3, 2, 6), (3, 4, 6, 8), (2, 5, 4, 10), (1, 4, 3, 12), (2, 3, 8, 12)]:
        assert Fraction(n1, d1) == Fraction(n2, d2)
        q = (fig(bars_svg([(d1, n1, (n1, d1)), (d2, n2, "?")])) +
             "The two bars are the same length. The top bar shows %s. What fraction of the bottom bar is shaded?" % fr(n1, d1))
        e = ("The bottom bar has %d equal parts and %d of them are shaded, so it shows %s. "
             "The shaded parts are the same length, so %s = <b>%s</b>." % (d2, n2, fr(n2, d2), fr(n1, d1), fr(n2, d2)))
        cands = [(n1, d2),                 # kept the numerator of the top bar
                 (n2, d2 - n2),            # shaded parts over the white parts
                 (n2, d1),                 # kept the denominator of the top bar
                 (n2 + 1, d2), (n2 - 1, d2)]
        its.append(mcq_fr(q, (n2, d2), cands, e, rnd))
    # B: how many parts to shade?
    for n1, d1, d2 in [(1, 2, 8), (2, 3, 9), (3, 5, 10), (1, 4, 8), (5, 6, 12)]:
        k = d2 // d1
        n2 = n1 * k
        q = (fig(bars_svg([(d1, n1, (n1, d1)), (d2, 0, "?")])) +
             "The two bars are the same length. The bottom bar has %d equal parts. "
             "How many parts must be shaded to show a fraction equal to %s?" % (d2, fr(n1, d1)))
        e = ("Each part of the top bar is cut into %d small parts (%d × %d = %d). "
             "%d shaded part%s × %d = %d. So %s = %s. Shade <b>%d</b> parts."
             % (k, d1, k, d2, n1, "" if n1 == 1 else "s", k, n2, fr(n1, d1), fr(n2, d2), n2))
        cands = [n1,                        # kept the numerator
                 n1 + d2 - d1,              # added the same number to the top and bottom
                 d2 - n2,                   # counted the white parts
                 n2 + 1, n2 - 1, k]
        its.append(mcq_n(q, n2, cands, e, rnd))
    # C: circles
    for n1, d1, n2, d2 in [(1, 2, 4, 8), (1, 3, 2, 6), (3, 4, 6, 8)]:
        assert Fraction(n1, d1) == Fraction(n2, d2)
        q = (fig(pies_svg([(d1, n1), (d2, n2)])) +
             "The two circles are the same size. Which shows the shaded parts as equivalent fractions?")
        e = ("The first circle has %d of %d equal slices shaded: %s. The second circle has %d of %d slices shaded: %s. "
             "The same amount is shaded, so <b>%s = %s</b>." % (n1, d1, fr(n1, d1), n2, d2, fr(n2, d2), fr(n1, d1), fr(n2, d2)))
        r = "%s = %s" % (fr(n1, d1), fr(n2, d2))
        cands = ["%s = %s" % (fr(n1, d1), fr(n1, d2)),        # kept the numerator
                 "%s = %s" % (fr(n1, d1), fr(n2, d1)),        # kept the denominator
                 "%s = %s" % (fr(n1, d1), fr(n2 + 1, d2))]    # miscounted the slices
        its.append(mcq(q, r, cands, e, rnd))
    # D: which bar? (A-D pictures)
    for (n, d), right, wrongs in [((2, 3), (4, 6), [(2, 6), (3, 4), (4, 8)]),
                                  ((1, 4), (2, 8), [(1, 8), (2, 5), (2, 6)]),
                                  ((3, 5), (6, 10), [(3, 10), (4, 6), (6, 8)]),
                                  ((3, 4), (9, 12), [(3, 12), (5, 6), (6, 12)])]:
        vals = [Fraction(*right)] + [Fraction(*w) for w in wrongs]
        assert vals[0] == Fraction(n, d) and len(set(vals)) == 4
        pos = SPOTS.next(rnd)
        w = wrongs[:]
        rnd.shuffle(w)
        rows = w[:pos] + [right] + w[pos:]
        q = (fig(bars_svg([(b, a, "ABCD"[i]) for i, (a, b) in enumerate(rows)], Hh=30, gap=10)) +
             "All the bars are the same length. Which bar shows a fraction equal to %s?" % fr(n, d))
        k = right[1] // d
        e = ("Multiply the numerator and the denominator of %s by %d: %s = %s. Bar %s has %d of %d parts shaded, "
             "so it shows %s. The answer is <b>%s</b>."
             % (fr(n, d), k, fr(n, d), fr(*right), "ABCD"[pos], right[0], right[1], fr(*right), "ABCD"[pos]))
        its.append(mcq_letters(q, pos, e))
    # E: fraction wall
    q = fig(wall_svg([1, 2, 4, 8])) + "Use the fraction wall. Which fraction is equal to %s?" % fr(3, 4)
    e = ("Each quarter is as long as 2 eighths. So 3 quarters are as long as 6 eighths: %s = <b>%s</b>."
         % (fr(3, 4), fr(6, 8)))
    its.append(mcq_fr(q, (6, 8), [(3, 8), (5, 6), (4, 8), (7, 8)], e, rnd))
    q = fig(wall_svg([1, 3, 6, 12])) + "Use the fraction wall. Which fraction is equal to %s?" % fr(2, 3)
    e = ("Each third is as long as 4 twelfths. So 2 thirds are as long as 8 twelfths: %s = <b>%s</b>."
         % (fr(2, 3), fr(8, 12)))
    its.append(mcq_fr(q, (8, 12), [(2, 12), (5, 6), (4, 12), (9, 12)], e, rnd))
    assert len(its) == 20, len(its)
    return {"title": "Equivalent fractions with fraction bars", "items": its}


# ============================================================ set 2: multiply or divide
def set_times(rnd):
    SPOTS.left = []
    its = []
    # A: multiply by a number
    for n, d, k in [(1, 2, 3), (3, 5, 2), (2, 3, 4), (3, 4, 3), (1, 6, 2)]:
        q = "Multiply the numerator and the denominator of %s by %d. Which fraction do you get?" % (fr(n, d), k)
        cands = [(n * k, d),            # multiplied only the numerator
                 (n, d * k),            # multiplied only the denominator
                 (n + k, d + k),        # added instead of multiplying
                 (n * k + 1, d * k)]
        its.append(mcq_fr(q, (n * k, d * k), cands, e_times(n, d, k), rnd))
    # B: divide by a number
    for n, d, k in [(6, 8, 2), (8, 12, 4), (6, 9, 3), (4, 12, 4)]:
        q = "Divide the numerator and the denominator of %s by %d. Which fraction do you get?" % (fr(n, d), k)
        cands = [(n // k, d),           # divided only the numerator
                 (n, d // k),           # divided only the denominator
                 (n - k, d - k),        # subtracted instead of dividing
                 (n // k + 1, d // k)]
        its.append(mcq_fr(q, (n // k, d // k), cands, e_div(n, d, k), rnd))
    # C: find the number to multiply by
    for n, d, D in [(2, 3, 12), (3, 4, 8), (1, 5, 10)]:
        k = D // d
        q = ("To write %s in %s, you multiply the numerator and the denominator by the same number. "
             "What is the number?" % (fr(n, d), WORD[D]))
        e = ("The denominator must change from %d to %d. %d × %d = %d, so the number is <b>%d</b>. %s = %s."
             % (d, D, d, k, D, k, fr(n, d), fr(n * k, D)))
        cands = [D - d,                 # added: d + ? = D
                 D // n if D % n == 0 and n > 1 else None,
                 n * k,                 # wrote the new numerator
                 D, k + 1]
        its.append(mcq_n(q, k, cands, e, rnd))
    # D: which fraction is equal?
    for (n, d), right, wrongs, how in [((3, 4), (6, 8), [(4, 5), (3, 8), (6, 4)], ("×", 2)),
                                       ((2, 5), (4, 10), [(3, 6), (2, 10), (4, 5)], ("×", 2)),
                                       ((4, 6), (2, 3), [(2, 6), (3, 5), (4, 3)], ("÷", 2)),
                                       ((9, 12), (3, 4), [(3, 12), (8, 11), (6, 9)], ("÷", 3))]:
        vals = [Fraction(*right)] + [Fraction(*w) for w in wrongs]
        assert vals[0] == Fraction(n, d) and len(set(vals)) == 4, (n, d)
        q = "Which fraction is equal to %s?" % fr(n, d)
        e = e_times(n, d, how[1]) if how[0] == "×" else e_div(n, d, how[1])
        its.append(mcq_fr(q, right, wrongs, e, rnd))
    # E: spot the mistake
    e = ("Adding the same number to the top and bottom does not give an equal fraction. %s = %s, but %s = %s, "
         "which is bigger. Multiply instead: %s = <b>%s</b>." % (fr(1, 3), fr(4, 12), fr(2, 4), fr(6, 12), fr(1, 3), fr(2, 6)))
    its.append(mcq("Siti wrote %s = %s. What mistake did she make?" % (fr(1, 3), fr(2, 4)),
                   "She added 1 to the top and bottom",
                   ["She multiplied by 2", "She divided by 2", "There is no mistake"], e, rnd))
    e = ("Hui Min multiplied only the numerator, so the parts did not change: %s is twice %s. "
         "Multiply the denominator too: %s = <b>%s</b>." % (fr(4, 5), fr(2, 5), fr(2, 5), fr(4, 10)))
    its.append(mcq("Hui Min wrote %s = %s. What mistake did she make?" % (fr(2, 5), fr(4, 5)),
                   "She multiplied only the numerator",
                   ["She multiplied only the denominator", "She added 2 to the top and bottom", "There is no mistake"], e, rnd))
    # F: which pair?
    def pair(a, b, c, d):
        return "%s and %s" % (fr(a, b), fr(c, d))
    e = "Multiply the numerator and the denominator of %s by 2: %s. So <b>%s and %s</b> are equivalent." % (
        fr(3, 5), fr(6, 10), fr(3, 5), fr(6, 10))
    its.append(mcq("Which pair of fractions are equivalent fractions?", pair(3, 5, 6, 10),
                   [pair(3, 5, 4, 6), pair(3, 5, 3, 10), pair(3, 5, 6, 5)], e, rnd))
    e = "Divide the numerator and the denominator of %s by 3: %s. So <b>%s and %s</b> are equivalent." % (
        fr(3, 12), fr(1, 4), fr(1, 4), fr(3, 12))
    its.append(mcq("Which two fractions show the same amount?", pair(1, 4, 3, 12),
                   [pair(1, 4, 3, 6), pair(1, 4, 1, 12), pair(1, 4, 4, 12)], e, rnd))
    assert len(its) == 20, len(its)
    return {"title": "Multiply or divide the numerator and denominator", "items": its}


# ============================================================ set 3: simplest form
def set_simplest(rnd):
    SPOTS.left = []
    its = []
    # A: pictures with groups
    for d, k, g in [(8, 6, 2), (9, 6, 3)]:
        q = (fig(group_bar_svg(d, k, g)) + "The bar shows %s. The thick lines put the parts into groups of %d. "
             "What is %s in simplest form?" % (fr(k, d), g, fr(k, d)))
        e = ("There are %d groups and %d of them are shaded. " % (d // g, k // g) + e_simplest(k, d))
        cands = [(k // g, d), (k, d // g), (k - g, d - g), (k - 1, d - 1)]
        its.append(mcq_fr(q, (k // g, d // g), cands, e, rnd))
    # B: write in simplest form
    for n, d in [(2, 4), (3, 6), (2, 8), (5, 10), (3, 9), (4, 8), (6, 8), (2, 10), (4, 10), (6, 9), (8, 12), (6, 12), (10, 12)]:
        g = math.gcd(n, d)
        assert g > 1
        cands = [(n // g, d),            # divided only the numerator
                 (n, d // g),            # divided only the denominator
                 (n - g, d - g),         # subtracted instead of dividing
                 (n - 1, d - 1),
                 (n // g + 1, d // g)]
        its.append(mcq_fr("Write %s in its simplest form." % fr(n, d), (n // g, d // g), cands, e_simplest(n, d), rnd))
    # C: which is in simplest form?
    for right, wrongs in [((3, 8), [(2, 6), (4, 10), (6, 9)]), ((5, 12), [(3, 9), (4, 6), (2, 8)])]:
        vals = [Fraction(*right)] + [Fraction(*w) for w in wrongs]
        assert len(set(vals)) == 4 and math.gcd(*right) == 1 and all(math.gcd(*w) > 1 for w in wrongs)
        e = ("%s: 1 is the only number that divides both %d and %d, so it is in simplest form. " % (fr(*right), right[0], right[1]) +
             " ".join("%s = %s." % (fr(*w), show(Fraction(*w))) for w in wrongs) +
             " The answer is <b>%s</b>." % fr(*right))
        its.append(mcq_fr("Which fraction is in its simplest form?" if right == (3, 8) else
                          "Only one of these fractions is in simplest form. Which one?", right, wrongs, e, rnd))
    # D: the biggest common number
    e = ("2 divides both 8 and 12, but 4 is bigger and also divides both: 8 ÷ 4 = 2 and 12 ÷ 4 = 3. "
         "6 does not divide 8, and 8 does not divide 12. The answer is <b>4</b>, so %s = %s." % (fr(8, 12), fr(2, 3)))
    its.append(mcq("To write %s in simplest form in one step, what is the biggest number you can divide 8 and 12 by?"
                   % fr(8, 12), "4", ["2", "6", "8"], e, rnd))
    # E: not fully simplified
    e = ("%s is equal to %s, but 4 and 6 can both still be divided by 2: %s = <b>%s</b>. "
         "Keep dividing until 1 is the only number that divides both." % (fr(4, 6), fr(8, 12), fr(4, 6), fr(2, 3)))
    its.append(mcq("Wei Ming wrote %s in simplest form as %s. What should he do next?" % (fr(8, 12), fr(4, 6)),
                   "Divide 4 and 6 by 2 to get %s" % fr(2, 3),
                   ["Nothing. The answer is finished", "Multiply 4 and 6 by 2 to get %s" % fr(8, 12),
                    "Subtract 2 from 4 and 6 to get %s" % fr(2, 4)], e, rnd))
    e = ("6 and 9 can both be divided by 3: 6 ÷ 3 = 2 and 9 ÷ 3 = 3. So %s is not in simplest form. "
         "<b>%s = %s</b>." % (fr(6, 9), fr(6, 9), fr(2, 3)))
    its.append(mcq("Ali says %s is in simplest form because 6 and 9 are not both even. Is he right?" % fr(6, 9),
                   "No, %s = %s" % (fr(6, 9), fr(2, 3)),
                   ["Yes, %s is in simplest form" % fr(6, 9), "No, %s = %s" % (fr(6, 9), fr(3, 6)),
                    "No, %s = %s" % (fr(6, 9), fr(2, 9))], e, rnd))
    assert len(its) == 20, len(its)
    return {"title": "Simplest form", "items": its}


# ============================================================ set 4: missing numbers
def set_missing(rnd):
    SPOTS.left = []
    its = []
    # A: missing numerator (multiply)
    for n, d, D in [(1, 2, 8), (2, 3, 12), (3, 4, 8), (2, 5, 10), (1, 3, 9), (5, 6, 12), (3, 4, 12), (2, 3, 9)]:
        k = D // d
        N = n * k
        q = "%s = %s. What is the missing number?" % (fr(n, d), fr("<b>?</b>", D))
        e = ("%d × %d = %d, so the denominator was multiplied by %d. Multiply the numerator by %d too: %d × %d = <b>%d</b>. "
             "%s = %s." % (d, k, D, k, k, n, k, N, fr(n, d), fr(N, D)))
        cands = [n + D - d,          # added the same number to the top and bottom
                 n,                  # kept the numerator
                 D - N,              # the other part of the whole
                 k, N + 1, N - 1]
        its.append(mcq_n(q, N, cands, e, rnd))
    # B: missing denominator (multiply)
    for n, d, N in [(1, 2, 4), (2, 3, 6), (3, 5, 6), (3, 4, 9), (1, 3, 4), (5, 6, 10)]:
        k = N // n
        D = d * k
        q = "%s = %s. What is the missing number?" % (fr(n, d), fr(N, "<b>?</b>"))
        e = ("%d × %d = %d, so the numerator was multiplied by %d. Multiply the denominator by %d too: %d × %d = <b>%d</b>. "
             "%s = %s." % (n, k, N, k, k, d, k, D, fr(n, d), fr(N, D)))
        cands = [d + N - n,          # added the same number to the top and bottom
                 d,                  # kept the denominator
                 N + 1 if N + 1 != D else None,
                 D + 1, D - 1, d * 2 if d * 2 != D else None]
        its.append(mcq_n(q, D, cands, e, rnd))
    # C: going to a smaller denominator (divide)
    for (n, d), (a, b), miss in [((9, 12), (None, 4), "n"), ((8, 10), (4, None), "d"),
                                 ((10, 12), (None, 6), "n"), ((6, 9), (2, None), "d")]:
        if miss == "n":
            k = d // b
            r = n // k
            q = "%s = %s. What is the missing number?" % (fr(n, d), fr("<b>?</b>", b))
            e = ("%d ÷ %d = %d, so the denominator was divided by %d. Divide the numerator by %d too: %d ÷ %d = <b>%d</b>. "
                 "%s = %s." % (d, k, b, k, k, n, k, r, fr(n, d), fr(r, b)))
            cands = [n - (d - b), n, k, r + 1, r - 1]
        else:
            k = n // a
            r = d // k
            q = "%s = %s. What is the missing number?" % (fr(n, d), fr(a, "<b>?</b>"))
            e = ("%d ÷ %d = %d, so the numerator was divided by %d. Divide the denominator by %d too: %d ÷ %d = <b>%d</b>. "
                 "%s = %s." % (n, k, a, k, k, d, k, r, fr(n, d), fr(a, r)))
            cands = [d - (n - a), d, k, r + 1, r - 1]
        assert Fraction(n, d) == (Fraction(r, b) if miss == "n" else Fraction(a, r))
        its.append(mcq_n(q, r, cands, e, rnd))
    # D: two missing numbers
    for (n, d), (a, B) , (C, D) in [((1, 2), (3, None), (None, 10)), ((2, 3), (4, None), (None, 12))]:
        b = d * (a // n)
        c = n * (D // d)
        assert Fraction(n, d) == Fraction(a, b) == Fraction(c, D)
        q = "%s = %s = %s. What are the two missing numbers, in order?" % (fr(n, d), fr(a, "<b>?</b>"), fr("<b>?</b>", D))
        e = ("%d × %d = %d, so %s = %s. %d × %d = %d, so %s = %s. The answer is <b>%d and %d</b>."
             % (n, a // n, a, fr(n, d), fr(a, b), d, D // d, D, fr(n, d), fr(c, D), b, c))
        r = "%d and %d" % (b, c)
        cands = ["%d and %d" % (d + a - n, n + D - d),     # added the same number each time
                 "%d and %d" % (c, b),                     # wrote them in the wrong order
                 "%d and %d" % (b, n),                     # kept the numerator in the second one
                 "%d and %d" % (b, c + 1)]
        its.append(mcq(q, r, cands, e, rnd))
    assert len(its) == 20, len(its)
    return {"title": "Missing numerators and denominators", "items": its}


# ============================================================ set 5: compare, order and word problems
def order_str(fs):
    return ", ".join(fr(*f) for f in fs)


def common_e(fs, L):
    """'3/4 = 6/8, 1/2 = 4/8' for the fractions that need renaming to L."""
    return ", ".join("%s = %s" % (fr(n, d), fr(n * L // d, L)) for n, d in fs if d != L)


def set_compare(rnd):
    SPOTS.left = []
    its = []
    # A: unit fractions
    pos = 0
    rows = [(2, 1, (1, 2)), (3, 1, (1, 3)), (4, 1, (1, 4)), (8, 1, (1, 8))]
    q = (fig(bars_svg(rows, Hh=30, gap=10)) + "All the bars are the same length. Which fraction is the smallest?")
    e = ("The more equal parts a whole is cut into, the smaller each part is. The bar cut into 8 parts has the "
         "shortest shaded part. The answer is <b>%s</b>." % fr(1, 8))
    its.append(mcq_fr(q, (1, 8), [(1, 2), (1, 3), (1, 4)], e, rnd))
    e = ("When the numerators are both 1, the fraction with the smaller denominator is greater. "
         "A whole cut into 4 parts has bigger parts than a whole cut into 8 parts. <b>%s &gt; %s</b> is true."
         % (fr(1, 4), fr(1, 8)))
    its.append(mcq("Which statement is true?", "%s &gt; %s" % (fr(1, 4), fr(1, 8)),
                   ["%s &gt; %s" % (fr(1, 8), fr(1, 4)), "%s &gt; %s" % (fr(1, 6), fr(1, 3)),
                    "%s &gt; %s" % (fr(1, 12), fr(1, 2))], e, rnd))
    e = ("All the numerators are 1. The smallest denominator gives the biggest parts. The greatest fraction is <b>%s</b>."
         % fr(1, 3))
    its.append(mcq_fr("Which is the greatest: %s, %s, %s or %s?" % (fr(1, 5), fr(1, 12), fr(1, 3), fr(1, 9)),
                      (1, 3), [(1, 12), (1, 9), (1, 5)], e, rnd))
    e = ("All the numerators are 1. The biggest denominator gives the smallest parts. The smallest fraction is <b>%s</b>."
         % fr(1, 10))
    its.append(mcq_fr("Which is the smallest: %s, %s, %s or %s?" % (fr(1, 6), fr(1, 4), fr(1, 10), fr(1, 7)),
                      (1, 10), [(1, 4), (1, 6), (1, 7)], e, rnd))
    # B: greatest / smallest with a common denominator
    for word, fs, L in [("greatest", [(3, 4), (5, 8), (1, 2), (3, 8)], 8),
                        ("smallest", [(1, 2), (2, 3), (5, 6), (7, 12)], 12),
                        ("greatest", [(7, 10), (3, 5), (1, 2), (2, 5)], 10),
                        ("greatest", [(5, 6), (3, 4), (2, 3), (7, 12)], 12),
                        ("smallest", [(2, 3), (4, 9), (1, 3), (5, 9)], 9)]:
        vs = [Fraction(*f) for f in fs]
        best = (max if word == "greatest" else min)(vs)
        right = fs[vs.index(best)]
        assert len(set(vs)) == 4
        e = ("Write them all in %s: %s. Now compare the numerators. The %s is <b>%s</b>."
             % (WORD[L], ", ".join(fr(n * L // d, L) for n, d in fs), word, fr(*right)))
        its.append(mcq_fr("Which is the %s: %s, %s, %s or %s?" % ((word,) + tuple(fr(*f) for f in fs)),
                          right, [f for f in fs if f != right], e, rnd))
    # C: order
    for fs, L, up in [([(1, 2), (3, 8), (3, 4)], 8, True), ([(2, 3), (5, 9), (1, 3)], 9, True),
                      ([(5, 6), (1, 2), (2, 3), (7, 12)], 12, False)]:
        srt = sorted(fs, key=lambda f: Fraction(*f), reverse=not up)
        r = order_str(srt)
        e = ("Write them in %s: %s. Then order the numerators. %s: <b>%s</b>."
             % (WORD[L], common_e(fs, L), "Smallest to greatest" if up else "Greatest to smallest", r))
        cands = [order_str(sorted(fs, key=lambda f: Fraction(*f), reverse=up)),     # wrong direction
                 order_str(sorted(fs, key=lambda f: (f[1], f[0]))),                 # by denominator
                 order_str(sorted(fs, key=lambda f: (-f[1], f[0]))),                # by denominator, reversed
                 order_str(sorted(fs, key=lambda f: (f[0], -f[1]))),                # by numerator
                 order_str(fs)]
        q = "Arrange %s in order, %s." % (", ".join(fr(*f) for f in fs),
                                          "from the smallest to the greatest" if up else "from the greatest to the smallest")
        its.append(mcq(q, r, cands, e, rnd))
    # D: word problems
    e = ("Write the distances in eighths: %s, %s. Compare the numerators: 6, 5, 4 and 3. "
         "<b>Ryan</b> ran the furthest." % (common_e([(3, 4)], 8), common_e([(1, 2)], 8)))
    its.append(mcq("On Sports Day, Ryan ran %s km, Chloe ran %s km, Arjun ran %s km and Priya ran %s km. "
                   "Who ran the furthest?" % (fr(3, 4), fr(5, 8), fr(1, 2), fr(3, 8)),
                   "Ryan", ["Chloe", "Priya", "Arjun"], e, rnd))
    e = ("Write the lengths in twelfths: %s. Compare the numerators: 8, 10, 7 and 9. "
         "7 is the smallest, so the <b>green ribbon</b> is the shortest." % common_e([(2, 3), (5, 6), (3, 4)], 12))
    its.append(mcq("Mrs Lim has four ribbons. The red ribbon is %s m long, the blue ribbon is %s m long, "
                   "the green ribbon is %s m long and the yellow ribbon is %s m long. Which ribbon is the shortest?"
                   % (fr(2, 3), fr(5, 6), fr(7, 12), fr(3, 4)),
                   "The green ribbon", ["The red ribbon", "The blue ribbon", "The yellow ribbon"], e, rnd))
    e = ("The bottles are the same size. Write the fractions in twelfths: %s. Compare the numerators: 9, 8, 5 and 6. "
         "<b>Mei Ling</b> has the most water." % common_e([(3, 4), (2, 3), (1, 2)], 12))
    its.append(mcq("Mei Ling, Kumar, Devi and Ethan have water bottles of the same size. Mei Ling’s bottle is %s full, "
                   "Kumar’s is %s full, Devi’s is %s full and Ethan’s is %s full. Whose bottle has the most water?"
                   % (fr(3, 4), fr(2, 3), fr(5, 12), fr(1, 2)),
                   "Mei Ling’s", ["Devi’s", "Kumar’s", "Ethan’s"], e, rnd))
    e = ("Write %s in eighths: %s. Raju read %s and Kavya read %s. 6 &gt; 5, so <b>Raju read more</b>. "
         "You cannot compare 5 and 3 when the parts are different sizes." % (fr(3, 4), fr(6, 8), fr(6, 8), fr(5, 8)))
    its.append(mcq("Kavya read %s of a storybook. Raju read %s of the same storybook. Who read more?" % (fr(5, 8), fr(3, 4)),
                   "Raju, because %s = %s" % (fr(3, 4), fr(6, 8)),
                   ["Kavya, because 5 &gt; 3", "Kavya, because 8 &gt; 4", "They read the same amount"], e, rnd))
    e = ("Siti ate %s. Write Jun Jie’s %s in eighths: %s. %s = %s, so <b>they ate the same amount</b>."
         % (fr(2, 8), fr(1, 4), fr(2, 8), fr(2, 8), fr(1, 4)))
    its.append(mcq("Siti ate %s of a pizza. Jun Jie ate %s of another pizza of the same size. Which is true?"
                   % (fr(2, 8), fr(1, 4)),
                   "They ate the same amount", ["Siti ate more", "Jun Jie ate more", "Siti ate twice as much"], e, rnd))
    # equivalent fractions in a story, with bar models
    assert Fraction(3, 4) == Fraction(9, 12)
    q = (fig(units_svg(4, 3, "12 pieces", "?")) +
         "Mrs Ng cut a pandan cake into 12 equal pieces. Her family ate %s of the cake. "
         "How many pieces did they eat?" % fr(3, 4))
    e = ("Draw a model of 4 units for quarters. 4 units = 12 pieces, so 1 unit = 12 ÷ 4 = 3 pieces. "
         "3 units = 3 × 3 = <b>9 pieces</b>. So %s = %s." % (fr(3, 4), fr(9, 12)))
    its.append(mcq_n(q, 9, [3, 11, 4, 8], e, rnd))
    assert Fraction(1, 3) == Fraction(4, 12)
    q = (fig(units_svg(3, 1, "? parts", "4 parts")) +
         "Xin Yi folded a paper strip into equal parts. She coloured 4 parts. The coloured parts are %s of the strip. "
         "How many equal parts are there?" % fr(1, 3))
    e = ("Draw a model of 3 units for thirds. 1 unit = 4 parts. 3 units = 3 × 4 = <b>12 parts</b>. So %s = %s."
         % (fr(1, 3), fr(4, 12)))
    its.append(mcq_n(q, 12, [3, 6, 7, 8], e, rnd))
    e = ("He gave away 4 of the 10 pieces: %s. " % fr(4, 10) + e_simplest(4, 10))
    its.append(mcq_fr("Zhi Hao had a bar of chocolate with 10 equal pieces. He gave 4 pieces to his sister. "
                      "What fraction of the bar did he give away?" + SIMPLE, (2, 5),
                      [(2, 10), (4, 5), (3, 5), (6, 10)], e, rnd))
    assert len(its) == 20, len(its)
    return {"title": "Compare, order and word problems", "items": its}


# ============================================================ lesson
def body_html():
    f_eq = bars_svg([(2, 1, (1, 2)), (4, 2, (2, 4)), (8, 4, (4, 8))], W=300)
    f_wall = wall_svg([1, 3, 6, 12])
    f_group = group_bar_svg(8, 6, 2)
    f_unit = bars_svg([(4, 1, (1, 4)), (8, 1, (1, 8))], W=300)
    f_model = units_svg(4, 3, "12 pieces", "?")
    return (
        "<h2>What are equivalent fractions?</h2>"
        "<p>Equivalent fractions show the same amount. They have different numerators and denominators. "
        "Look at the three bars. They are the same length, and the shaded parts are the same length too.</p>"
        "<figure class='sn-fig'>" + f_eq +
        "<figcaption>" + fr(1, 2) + " = " + fr(2, 4) + " = " + fr(4, 8) + "</figcaption></figure>"
        "<p>A fraction wall helps you see more equivalent fractions.</p>"
        "<figure class='sn-fig'>" + f_wall +
        "<figcaption>1 third is as long as 2 sixths and 4 twelfths: " + fr(1, 3) + " = " + fr(2, 6) + " = " + fr(4, 12) +
        ".</figcaption></figure>" +
        "<h2>Multiply or divide the top and bottom by the same number</h2>"
        "<p>To find an equivalent fraction, multiply the numerator and the denominator by the same number. "
        "You can also divide them both by the same number.</p>"
        + ex("Example", "Find a fraction equal to " + fr(2, 3) + " with denominator 12.",
             "3 × 4 = 12, so multiply the numerator by 4 too: 2 × 4 = 8.", fr(2, 3) + " = " + fr(8, 12))
        + ex("Example", fr(3, 5) + " = " + fr(6, "?"),
             "3 × 2 = 6, so multiply the denominator by 2 too: 5 × 2 = 10.", fr(3, 5) + " = " + fr(6, 10)) +
        "<h2>Simplest form</h2>"
        "<p>A fraction is in simplest form when 1 is the only number that divides both the numerator and the denominator. "
        "Divide them both by the biggest number you can.</p>"
        "<figure class='sn-fig'>" + f_group +
        "<figcaption>Put the eighths into groups of 2: " + fr(6, 8) + " = " + fr(3, 4) + ".</figcaption></figure>" +
        table(["Fraction", "Divide both by", "Simplest form"], [
            [fr(6, 8), "2", fr(3, 4)],
            [fr(6, 9), "3", fr(2, 3)],
            [fr(8, 12), "4", fr(2, 3)],
        ]) +
        "<h2>Comparing and ordering fractions</h2>"
        "<p>If the numerators are both 1, the fraction with the smaller denominator is greater. "
        "A whole cut into 4 parts has bigger parts than a whole cut into 8 parts.</p>"
        "<figure class='sn-fig'>" + f_unit +
        "<figcaption>" + fr(1, 4) + " &gt; " + fr(1, 8) + "</figcaption></figure>"
        "<p>For other fractions, write them with the same denominator first. Then compare the numerators.</p>"
        + ex("Example", "Which is greater, " + fr(3, 4) + " or " + fr(5, 8) + "?",
             fr(3, 4) + " = " + fr(6, 8) + ". 6 eighths is more than 5 eighths.", fr(3, 4))
        + ex("Example", "Arrange " + fr(1, 2) + ", " + fr(3, 8) + ", " + fr(3, 4) + " from the smallest to the greatest.",
             "In eighths: " + fr(4, 8) + ", " + fr(3, 8) + ", " + fr(6, 8) + ". Order the numerators: 3, 4, 6.",
             fr(3, 8) + ", " + fr(1, 2) + ", " + fr(3, 4)) +
        "<h2>Word problems: draw a model</h2>"
        "<p>Draw a bar and cut it into equal units. The denominator tells you how many units.</p>"
        "<figure class='sn-fig'>" + f_model +
        "<figcaption>A cake is cut into 12 equal pieces. How many pieces are " + fr(3, 4) + " of the cake?</figcaption></figure>"
        + ex("Example", "Mrs Ng cut a cake into 12 equal pieces. Her family ate " + fr(3, 4) + " of it. How many pieces did they eat?",
             "4 units = 12 pieces. 1 unit = 3 pieces. 3 units = 9 pieces.", "9 pieces") +
        "<h2>Common mistakes</h2>" +
        table(["Mistake", "What to do instead"], [
            [fr(1, 3) + " = " + fr(2, 4) + " (adding 1 to the top and bottom)",
             "Multiply both by the same number: " + fr(1, 3) + " = " + fr(2, 6)],
            [fr(1, 8) + " &gt; " + fr(1, 4) + " (because 8 &gt; 4)",
             "More parts means smaller parts: " + fr(1, 8) + " &lt; " + fr(1, 4)],
            [fr(8, 12) + " = " + fr(4, 6) + " (not fully simplified)",
             "Keep dividing: " + fr(4, 6) + " = " + fr(2, 3)],
            [fr(2, 5) + " = " + fr(4, 5) + " (multiplying only the numerator)",
             "Multiply the denominator too: " + fr(2, 5) + " = " + fr(4, 10)],
        ])
    )


FAQ = [
    {"q": "What is taught in P3 fractions?",
     "a": "In Primary 3, students learn equivalent fractions, write fractions in simplest form, and compare and order fractions with different denominators up to 12. They also add and subtract simple fractions within 1 whole."},
    {"q": "How do I explain equivalent fractions to my child?",
     "a": "Show two strips of paper of the same length: fold one into halves and the other into quarters. 1 half covers the same length as 2 quarters, so 1/2 = 2/4. To find more, multiply the top and bottom by the same number."},
    {"q": "What is the most common mistake with equivalent fractions?",
     "a": "Adding the same number to the top and bottom, as in 1/3 = 2/4. This changes the amount. Multiply instead: 1/3 = 2/6."},
    {"q": "Is equivalent fractions in the MOE syllabus for Primary 3?",
     "a": "Yes. Equivalent fractions, simplest form, and comparing and ordering fractions are part of Fractions in the Primary 3 Standard Mathematics syllabus (MOE 2021). In Primary 4, students go on to mixed numbers and improper fractions."},
]


def gen_unit():
    rnd = random.Random(63805)
    sets = [set_bars(rnd), set_times(rnd), set_simplest(rnd), set_missing(rnd), set_compare(rnd)]
    seen = set()
    for s in sets:
        assert len(s["items"]) == 20, (s["title"], len(s["items"]))
        assert sorted(it["a"] for it in s["items"]) == sorted([0, 1, 2, 3] * 5), (s["title"], [it["a"] for it in s["items"]])
        for it in s["items"]:
            assert len(set(it["c"])) == 4, it
            assert it["q"] not in seen, it["q"]
            assert it["q"].count("<svg") <= 1
            seen.add(it["q"])
    return {
        "country": "sg", "subject": "maths", "grade": "primary-3", "slug": "equivalent-fractions", "sort": 5,
        "updated": UPDATED, "pdf_url": "",
        "title": "Primary 3 Equivalent Fractions",
        "seo_title": "P3 Equivalent Fractions Worksheets: Free Primary 3 Maths with Answers (MOE Syllabus)",
        "short_title": "Equivalent Fractions",
        "domain": "Number and Algebra",
        "standard_code": "Primary 3: Fractions",
        "standard_url": "https://www.moe.gov.sg/primary/curriculum/syllabus",
        "standard_text": "Equivalent fractions; simplest form; comparing and ordering unlike fractions (denominators not exceeding 12); writing an equivalent fraction given the numerator or denominator",
        "meta_desc": "Free P3 maths practice: equivalent fractions with fraction bars, simplest form, missing numbers and comparing fractions. 100 questions with answers.",
        "key_big": "Multiply or divide the numerator and the denominator by the same number.",
        "key_sub": "2/3 = (2 × 4)/(3 × 4) = 8/12",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }


if __name__ == "__main__":
    u = gen_unit()
    mark_large(u, "(bars of|bar of|bar model|fraction wall)")
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(u, f, ensure_ascii=False, indent=1)
    print("wrote", path)
