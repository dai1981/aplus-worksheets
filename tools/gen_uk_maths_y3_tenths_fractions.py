# -*- coding: utf-8 -*-
"""
UK Year 3 Maths: Tenths and adding fractions (National Curriculum in England, Year 3: Fractions)
  python3 tools/gen_uk_maths_y3_tenths_fractions.py
Tenths of a shape (bars of 10, a chocolate bar, a pizza), counting up and down in tenths on a number line
(9/10, 1, 1 1/10), tenths of amounts and dividing one-digit numbers by 10 (3 ÷ 10 = 3/10), adding and
subtracting fractions with the same denominator within one whole, and word problems.
Year 3 writes tenths as fractions; decimals (0.3) are Year 4 and appear once in the lesson only.
Every choice carries its value (fractions.Fraction); a wrong choice never equals the right value or another wrong one.
Wrong answers come from real mistakes: adding the denominators (2/7 + 3/7 = 5/14), counting the unshaded parts,
counting tick marks instead of spaces, 10/10 -> 11/10 without crossing 1, 1/10 of 30 = 300, 3 ÷ 10 = 10/3.
HTML attributes use single quotes (no backslashes in the JSON). British English.
"""
import json, math, os, random, re
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "uk", "maths", "year-3")
UPDATED = "2026-11-02"
FILL = "#4fae74"      # shaded / first part
FILL2 = "#f2b84b"     # second part
RED = "#c0392b"
LINE = "#2b2b2b"
FONT = "Arial, Helvetica, sans-serif"
GIRLS = ["Amelia", "Isla", "Freya", "Poppy", "Ava", "Aisha", "Lily", "Zara", "Grace", "Ruby", "Maya", "Evie"]
BOYS = ["Oliver", "Harry", "Mohammed", "Jack", "Arjun", "Noah", "George", "Leo", "Alfie", "Kai", "Ethan", "Charlie"]
WORD = {2: "halves", 3: "thirds", 4: "quarters", 5: "fifths", 6: "sixths", 7: "sevenths", 8: "eighths",
        9: "ninths", 10: "tenths", 12: "twelfths"}
ONE = {2: "half", 3: "third", 4: "quarter", 5: "fifth", 6: "sixth", 7: "seventh", 8: "eighth", 9: "ninth",
       10: "tenth", 12: "twelfth"}
NUMW = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten"]


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
    """Choice: fraction a/b (as written) with its value."""
    return (fr(a, b) + unit, F(a, b))


def Mc(w, n, d, unit=""):
    """Choice: mixed number w n/d (or a whole number when n = 0) with its value."""
    return (mx(w, n, d) + unit, F(w) + F(n, d))


def Nc(n, unit="", pre=""):
    return ("%s%s%s" % (pre, "{:,}".format(n), unit), F(n))


def parts(n, d):
    """'3 tenths', '1 tenth'."""
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
        if v is not None and (v < 0 or v in vals):
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


def fixed(q, choices, a, e):
    """Choices kept in order (A, B, C, D labels)."""
    return {"q": q, "c": list(choices), "a": a, "e": e}


def fig(svg):
    return "<div class='qfig'>" + svg + "</div>"


def svg_wrap(w, h, body, label):
    w, h = int(math.ceil(w)), int(math.ceil(h))
    return ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 %d %d' width='%d' height='%d' "
            "role='img' aria-label='%s'><g font-family='%s'>%s</g></svg>" % (w, h, w, h, label, FONT, body))


def text(x, y, t, fs=16, anchor="middle", col=LINE):
    return ("<text x='%.1f' y='%.1f' font-size='%d' font-weight='700' fill='%s' text-anchor='%s'>%s</text>"
            % (x, y, fs, col, anchor, t))


def table(head, rows):
    h = "".join("<th>%s</th>" % x for x in head)
    b = "".join("<tr>" + "".join("<td>%s</td>" % c for c in r) + "</tr>" for r in rows)
    return "<div class='sn-tw'><table class='sn-table'><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>" % (h, b)


def ex(title, q, s, a):
    return ("<div class='sn-ex'><span class='sn-ex-t'>%s</span><p class='sn-ex-q'>%s</p>"
            "<p class='sn-ex-s'>%s</p><p class='sn-ex-a'>Answer: %s</p></div>" % (title, q, s, a))


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


def mark_large(u, pattern):
    """Tag pictures that must print larger so their labels stay readable."""
    rx = re.compile(r"<svg (?=[^>]*aria-label='" + pattern + ")")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u


# ------------------------------------------------------------ pictures
def bar_row(x0, y, W, H, n, k, crossed=(), fills=None, widths=None):
    s = []
    x = x0
    for i in range(n):
        col = (fills[i] if fills and i < len(fills) else (FILL if i < k else "#fff"))
        w = widths[i] if widths else W / n
        s.append("<rect x='%.1f' y='%.1f' width='%.2f' height='%d' fill='%s' stroke='%s' stroke-width='2.5'/>"
                 % (x, y, w, H, col, LINE))
        if i in crossed:
            r = min(w, H) / 2 - min(w, H) * 0.2
            cx, cy = x + w / 2, y + H / 2
            s.append("<path d='M%.1f %.1f L%.1f %.1f M%.1f %.1f L%.1f %.1f' stroke='%s' stroke-width='3' stroke-linecap='round'/>"
                     % (cx - r, cy - r, cx + r, cy + r, cx - r, cy + r, cx + r, cy - r, RED))
        x += w
    return "".join(s)


def tenths_bar_svg(k, W=300, H=44):
    s = bar_row(6, 6, W, H, 10, k)
    s += "<rect x='6' y='6' width='%d' height='%d' fill='none' stroke='%s' stroke-width='3'/>" % (W, H, LINE)
    return svg_wrap(W + 12, H + 12, s, "bar split into 10 equal parts with %d shaded" % k)


def choc_svg(k, cell=40):
    """Chocolate bar: 2 rows of 5 pieces, first k shaded (top row first)."""
    s = []
    for i in range(10):
        r, c = divmod(i, 5)
        s.append("<rect x='%d' y='%d' width='%d' height='%d' rx='4' fill='%s' stroke='%s' stroke-width='2.5'/>"
                 % (6 + c * cell, 6 + r * cell, cell, cell, FILL if i < k else "#fff", LINE))
    return svg_wrap(5 * cell + 12, 2 * cell + 12, "".join(s),
                    "chocolate bar of 10 equal pieces in 2 rows of 5, %d pieces shaded" % k)


def pizza_svg(k, r=56):
    cx = cy = r + 6
    s = []
    for i in range(10):
        a0 = -math.pi / 2 + i * 2 * math.pi / 10
        a1 = a0 + 2 * math.pi / 10
        s.append("<path d='M%d %d L%.1f %.1f A%d %d 0 0 1 %.1f %.1f Z' fill='%s' stroke='%s' stroke-width='2.5'/>"
                 % (cx, cy, cx + r * math.cos(a0), cy + r * math.sin(a0), r, r,
                    cx + r * math.cos(a1), cy + r * math.sin(a1), FILL if i < k else "#fff", LINE))
    return svg_wrap(2 * r + 12, 2 * r + 12, "".join(s), "circle cut into 10 equal slices, %d slices shaded" % k)


def four_bars_svg(right):
    """A-D: bars of the same length. The bar at position `right` has 10 equal parts;
    the others have 10 unequal parts, 9 equal parts and 5 equal parts."""
    W, H, gap, x0 = 240, 26, 12, 34
    unequal = [12, 36, 18, 30, 14, 28, 20, 34, 22, 26]
    assert sum(unequal) == W, sum(unequal)
    others = [("unequal", 10), ("equal", 9), ("equal", 5)]
    rows = others[:right] + [("equal", 10)] + others[right:]
    s = []
    for i, (kind, n) in enumerate(rows):
        y = 6 + i * (H + gap)
        s.append(text(14, y + 19, "ABCD"[i], 17))
        s.append(bar_row(x0, y, W, H, n, 0, widths=unequal if kind == "unequal" else None))
    return svg_wrap(x0 + W + 6, 6 + 4 * H + 3 * gap + 6, "".join(s),
                    "four bars A to D of the same length split into parts")


def add_bar_svg(d, x, y, W=280, H=44):
    fills = [FILL] * x + [FILL2] * y
    s = bar_row(6, 6, W, H, d, 0, fills=fills)
    s += "<rect x='6' y='6' width='%d' height='%d' fill='none' stroke='%s' stroke-width='3'/>" % (W, H, LINE)
    return svg_wrap(W + 12, H + 12, s, "bar of %d equal parts: %d green and %d yellow" % (d, x, y))


def sub_bar_svg(d, x, y, W=280, H=44):
    s = bar_row(6, 6, W, H, d, x, crossed=set(range(x - y, x)))
    s += "<rect x='6' y='6' width='%d' height='%d' fill='none' stroke='%s' stroke-width='3'/>" % (W, H, LINE)
    return svg_wrap(W + 12, H + 12, s, "bar of %d equal parts: %d shaded and %d of them crossed out" % (d, x, y))


def tline_svg(wholes, dot=None, W=None):
    """Number line from 0 to `wholes`, marked in tenths, wholes labelled. dot: position in tenths (red)."""
    W = W or (360 if wholes == 1 else 420)
    L, R, Y = 22, W - 22, 26
    n = 10 * wholes

    def X(v):
        return L + (R - L) * v / float(n)
    s = ["<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='2.5'/>" % (L, Y, R, Y, LINE)]
    for v in range(n + 1):
        big = v % 10 == 0
        s.append("<line x1='%.1f' y1='%d' x2='%.1f' y2='%d' stroke='%s' stroke-width='%s'/>"
                 % (X(v), Y - (13 if big else 8), X(v), Y + (13 if big else 8), LINE, "2.5" if big else "1.8"))
        if big:
            s.append(text(X(v), Y + 34, str(v // 10), 17))
    if dot is not None:
        assert 0 < dot < n
        s.append("<circle cx='%.1f' cy='%d' r='7' fill='%s'/>" % (X(dot), Y, RED))
    return svg_wrap(W, Y + 44, "".join(s), "number line from 0 to %d marked in tenths" % wholes)


def model_svg(T, b, k, W=300, H=36, parts_text=None):
    """Bar model: whole bar labelled T, then the same bar in b equal parts, k shaded, ? under the shaded parts."""
    x0, y1 = 6, 6
    s = ["<rect x='%d' y='%d' width='%d' height='%d' fill='#fff' stroke='%s' stroke-width='2.5'/>" % (x0, y1, W, H, LINE),
         text(x0 + W / 2, y1 + 24, str(T), 17)]
    y2 = y1 + H + 10
    s.append(bar_row(x0, y2, W, H, b, k))
    if parts_text:
        for i in range(b):
            s.append(text(x0 + (i + 0.5) * W / b, y2 + 24, parts_text, 15))
    xr = x0 + W * k / b
    yb = y2 + H + 6
    s.append("<path d='M%d %d L%d %d L%.1f %d L%.1f %d' fill='none' stroke='%s' stroke-width='2'/>"
             % (x0 + 1, yb, x0 + 1, yb + 8, xr - 1, yb + 8, xr - 1, yb, LINE))
    lab = "?" if not parts_text else str(T * k // b)
    s.append(text(max((x0 + xr) / 2, x0 + 12), yb + 27, lab, 17))
    return svg_wrap(W + 12, yb + 34, "".join(s),
                    "bar model: a whole of %d, and the same bar in %d equal parts with %d shaded" % (T, b, k))


# ============================================================ set 1: tenths of a shape
def shaded_cands(k):
    return [Fc(k, 10 - k), Fc(10 - k, 10), Fc(10, k), Nc(k), Fc(1, k)]


def unshaded_cands(k):
    return [Fc(k, 10), Fc(10 - k, k), Nc(10 - k), Fc(10, 10 - k)]


def set_shapes(rnd):
    SPOTS.left = []
    its = []
    for k in [3, 7, 1]:
        e = ("The bar has 10 equal parts, so each part is %s. %s shaded. So %s is shaded."
             % (fr(1, 10), "1 part is" if k == 1 else "%d parts are" % k, fr(k, 10)))
        its.append(mcq(fig(tenths_bar_svg(k)) + "What fraction of the bar is shaded?", Fc(k, 10), shaded_cands(k), e, rnd))
    for k in [2, 5]:
        e = ("%d parts out of 10 are shaded, so 10 − %d = <b>%d</b> parts are not shaded. That is %s."
             % (k, k, 10 - k, fr(10 - k, 10)))
        its.append(mcq(fig(tenths_bar_svg(k)) + "What fraction of the bar is <b>not</b> shaded?", Fc(10 - k, 10),
                       unshaded_cands(k), e, rnd))
    # which bar shows tenths (A-D in order)
    right = SPOTS.next(rnd)
    its.append(fixed(fig(four_bars_svg(right)) + "Which bar is split into tenths?", ["A", "B", "C", "D"], right,
                     "Tenths are <b>10 equal parts</b>. Bar %s has 10 parts that are all the same size. "
                     "One bar has 10 parts, but they are not equal, so they are not tenths." % "ABCD"[right]))
    for k in [9, 4]:
        e = ("Count the shaded parts: %d. There are 10 equal parts in the bar. So %s is shaded."
             % (k, fr(k, 10)))
        its.append(mcq(fig(tenths_bar_svg(k)) + "What fraction of the bar is shaded?", Fc(k, 10), shaded_cands(k), e, rnd))
    for k in [3, 7]:
        e = ("The chocolate bar has 10 equal pieces, so each piece is %s. %d pieces are shaded: %s."
             % (fr(1, 10), k, fr(k, 10)))
        its.append(mcq(fig(choc_svg(k)) + "What fraction of the chocolate bar is shaded?", Fc(k, 10), shaded_cands(k), e, rnd))
    k = 6
    its.append(mcq(fig(choc_svg(k)) + "What fraction of the chocolate bar is <b>not</b> shaded?", Fc(10 - k, 10),
                   unshaded_cands(k), "There are 10 pieces and %d are shaded. 10 − %d = <b>4</b> pieces are not shaded: %s."
                   % (k, k, fr(4, 10)), rnd))
    for k in [4, 8]:
        e = ("The pizza is cut into 10 equal slices, so each slice is %s. %d slices are shaded: %s."
             % (fr(1, 10), k, fr(k, 10)))
        its.append(mcq(fig(pizza_svg(k)) + "What fraction of the pizza is shaded?", Fc(k, 10), shaded_cands(k), e, rnd))
    k = 7
    its.append(mcq(fig(pizza_svg(k)) + "What fraction of the pizza is <b>not</b> shaded?", Fc(10 - k, 10),
                   unshaded_cands(k), "There are 10 slices and %d are shaded. 10 − %d = <b>3</b> slices are not shaded: %s."
                   % (k, k, fr(3, 10)), rnd))
    # words
    for k in [7, 3]:
        its.append(mcq("How do you say %s?" % fr(k, 10), "%s tenths" % NUMW[k],
                       ["%s tens" % NUMW[k], "ten %s" % WORD[k], "%sty" % {7: "seven", 3: "thir"}[k]],
                       "The denominator 10 tells you the parts are <b>tenths</b>. The numerator tells you how many: "
                       "%s = %s tenths." % (fr(k, 10), NUMW[k]), rnd))
    its.append(mcq("How many tenths make 1 whole?", Nc(10), [Nc(1), Nc(100), Nc(9)],
                   "1 whole split into 10 equal parts gives <b>10</b> tenths: %s = 1." % fr(10, 10), rnd))
    for k in [6, 8]:
        its.append(mcq("A bar has 10 equal parts. How many parts do you shade to show %s?" % fr(k, 10), Nc(k),
                       [Nc(10 - k), Nc(10), Nc(1)],
                       "The numerator tells you how many parts to shade: <b>%d</b> of the 10 parts." % k, rnd))
    its.append(mcq("A bar has 10 equal parts. What fraction is <b>one</b> part?", Fc(1, 10),
                   [Fc(10, 1), Fc(1, 9), Fc(9, 10)],
                   "1 part out of 10 equal parts is <b>one tenth</b>: %s." % fr(1, 10), rnd))
    assert len(its) == 20, len(its)
    return {"title": "Tenths of a shape", "items": its}


# ============================================================ set 2: counting in tenths
def seq(terms):
    return ", ".join(terms)


def set_counting(rnd):
    SPOTS.left = []
    its = []
    for k in [3, 7, 5]:
        e = ("The line from 0 to 1 is split into 10 equal spaces, so each space is %s. "
             "Count the spaces from 0 to the dot: %d. The dot is at <b>%s</b>." % (fr(1, 10), k, fr(k, 10)))
        its.append(mcq(fig(tline_svg(1, k)) + "What fraction is at the red dot?", Fc(k, 10),
                       [Fc(k + 1, 10), Fc(10 - k, 10), Nc(k), Fc(k - 1, 10)], e, rnd))
    # counting up within 1
    for a in [4, 1, 6]:
        e = ("Count up in tenths: add 1 to the numerator each time. The denominator stays 10. "
             "%s comes next." % fr(a + 3, 10))
        its.append(mcq("Count up in tenths. What comes next?<br>%s, <b>?</b>" % seq([fr(a + i, 10) for i in range(3)]),
                       Fc(a + 3, 10), [Fc(a + 3, 11), Fc(a + 4, 10), Fc(a + 2, 10), Fc(a + 3, 20)], e, rnd))
    # missing in the middle
    for a in [2, 5]:
        terms = [fr(a, 10), "<b>?</b>", fr(a + 2, 10), fr(a + 3, 10)]
        its.append(mcq("Count up in tenths. What is missing?<br>%s" % seq(terms), Fc(a + 1, 10),
                       [Fc(a + 1, 11), Fc(a + 4, 10), Fc(a, 10), Nc(a + 1)],
                       "The numbers go up by %s each time. %s + %s = <b>%s</b>." % (fr(1, 10), fr(a, 10), fr(1, 10), fr(a + 1, 10)), rnd))
    # across 1
    its.append(mcq("Count up in tenths. What comes next?<br>%s, <b>?</b>" % seq([fr(7, 10), fr(8, 10), fr(9, 10)]),
                   Mc(1, 0, 10), [Fc(10, 11), Fc(1, 10), Mc(1, 1, 10)],
                   "%s and 1 more tenth is %s, and %s is <b>1</b> whole." % (fr(9, 10), fr(10, 10), fr(10, 10)), rnd))
    its.append(mcq("Count up in tenths. What comes next?<br>%s, 1, <b>?</b>" % seq([fr(8, 10), fr(9, 10)]),
                   Mc(1, 1, 10), [Fc(1, 10), Nc(2), Mc(1, 2, 10)],
                   "After 1 whole, start counting tenths again: 1 and %s more is <b>1 %s</b>." % (fr(1, 10), fr(1, 10)), rnd))
    # counting down
    for a in [6, 9]:
        e = ("Count down in tenths: take 1 away from the numerator each time. The denominator stays 10. "
             "%s comes next." % fr(a - 3, 10))
        its.append(mcq("Count down in tenths. What comes next?<br>%s, <b>?</b>" % seq([fr(a - i, 10) for i in range(3)]),
                       Fc(a - 3, 10), [Fc(a - 1, 10), Fc(a - 4, 10), Fc(a - 3, 7), Fc(a - 3, 9)], e, rnd))
    its.append(mcq("Count down in tenths. What comes next?<br>1 %s, 1 %s, 1, <b>?</b>" % (fr(2, 10), fr(1, 10)),
                   Fc(9, 10), [Nc(0), Fc(8, 10), Fc(1, 10)],
                   "1 whole is %s. One tenth less is %s − %s = <b>%s</b>." % (fr(10, 10), fr(10, 10), fr(1, 10), fr(9, 10)), rnd))
    its.append(mcq("Count down in tenths. What is missing?<br>%s" % seq([fr(9, 10), fr(8, 10), "<b>?</b>", fr(6, 10)]),
                   Fc(7, 10), [Fc(8, 10), Fc(5, 10), Fc(7, 9), Nc(7)],
                   "The numbers go down by %s each time. %s − %s = <b>%s</b>." % (fr(1, 10), fr(8, 10), fr(1, 10), fr(7, 10)), rnd))
    its.append(mcq("Count up in tenths. What comes next?<br>1, 1 %s, 1 %s, <b>?</b>" % (fr(1, 10), fr(2, 10)),
                   Mc(1, 3, 10), [Fc(3, 10), Mc(1, 2, 10), Mc(3, 3, 10), Nc(2)],
                   "The whole number stays 1. The tenths go up by 1 each time: 1 %s comes next." % fr(3, 10), rnd))
    # number line 0 to 2
    for k in [3, 6, 8]:
        e = ("The big marks are 0, 1 and 2. Each small space is %s. The dot is past 1, and %d more tenths. "
             "So it is at <b>1 %s</b>." % (fr(1, 10), k, fr(k, 10)))
        its.append(mcq(fig(tline_svg(2, 10 + k)) + "What number is at the red dot?", Mc(1, k, 10),
                       [Fc(k, 10), Mc(1, k + 1, 10), Mc(1, 10 - k, 10), Mc(2, k, 10)], e, rnd))
    # one tenth more / less
    its.append(mcq("What is 1 tenth more than %s?" % fr(6, 10), Fc(7, 10), [Fc(6, 11), Fc(5, 10), Fc(7, 20)],
                   "Add 1 to the numerator: %s + %s = <b>%s</b>. The denominator stays 10." % (fr(6, 10), fr(1, 10), fr(7, 10)), rnd))
    its.append(mcq("What is 1 tenth less than 1?", Fc(9, 10), [Nc(0), Fc(1, 10), Mc(1, 1, 10)],
                   "1 = %s. Take away 1 tenth: %s − %s = <b>%s</b>." % (fr(10, 10), fr(10, 10), fr(1, 10), fr(9, 10)), rnd))
    assert len(its) == 20, len(its)
    return {"title": "Count up and down in tenths", "items": its}


# ============================================================ set 3: tenths of amounts, dividing by 10
def e_tenth(T, unit=""):
    return ("To find %s, divide by 10: %d ÷ 10 = <b>%d%s</b>. It is one of 10 equal parts, so it is smaller than %d."
            % (fr(1, 10), T, T // 10, unit, T))


def e_tenths(T, k, unit=""):
    one = T // 10
    return ("First find %s: %d ÷ 10 = %d. Then take %d of those parts: %d × %d = <b>%d%s</b>."
            % (fr(1, 10), T, one, k, one, k, one * k, unit))


def set_amounts(rnd):
    SPOTS.left = []
    its = []
    for T in [30, 50, 80, 20]:
        its.append(mcq(fig(model_svg(T, 10, 1)) + "Find %s of %d." % (fr(1, 10), T), Nc(T // 10),
                       [Nc(T * 10), Nc(T - 10), Nc(T + 10), Nc(T - T // 10)], e_tenth(T), rnd))
    for T in [70, 40, 90, 100]:
        its.append(mcq("What is %s of %d?" % (fr(1, 10), T), Nc(T // 10),
                       [Nc(T * 10), Nc(T - 10), Nc(T - T // 10), Nc(T + 10)], e_tenth(T), rnd))
    for k, T, pic in [(3, 40, True), (7, 20, True), (2, 50, False), (4, 60, False)]:
        ans = T * k // 10
        q = ("Find %s of %d." % (fr(k, 10), T)) if pic else ("What is %s of %d?" % (fr(k, 10), T))
        its.append(mcq((fig(model_svg(T, 10, k)) if pic else "") + q, Nc(ans),
                       [Nc(T // 10), Nc(T - ans), Nc(T * k), Nc(T // 10 + k)], e_tenths(T, k), rnd))
    for k in [3, 7, 9, 4]:
        e = ("Share %d wholes into 10 equal groups. Cut each whole into tenths: that makes %d tenths. "
             "Each group gets %d tenths. So %d ÷ 10 = <b>%s</b>." % (k, 10 * k, k, k, fr(k, 10)))
        its.append(mcq("%d ÷ 10 = ?" % k, Fc(k, 10), [Nc(10 * k), Fc(10, k), Fc(1, k), Nc(k)], e, rnd))
    for k, thing in [(4, "pizza"), (6, "cake")]:
        e = ("%d ÷ 10 = %s. Each child gets <b>%s of a %s</b>. That is less than 1 whole %s."
             % (k, fr(k, 10), fr(k, 10), thing, thing))
        u = " of a %s" % thing
        its.append(mcq("%s %ss are shared equally between 10 children. How much does each child get?" % (cap(NUMW[k]), thing),
                       Fc(k, 10, u), [Fc(10, k, u), Fc(1, k, u), Fc(1, 10, u), Nc(10 * k, " %ss" % thing)], e, rnd))
    its.append(mcq("What is %s of 1 metre?" % fr(1, 10), Nc(10, " cm"), [Nc(1, " cm"), Nc(100, " cm"), Nc(90, " cm")],
                   "1 m = 100 cm. 100 ÷ 10 = <b>10 cm</b>.", rnd))
    its.append(mcq("What is %s of £1?" % fr(1, 10), Nc(10, "p"), [Nc(1, "p"), ("£10", F(1000)), Nc(90, "p")],
                   "£1 = 100p. 100p ÷ 10 = <b>10p</b>.", rnd))
    assert len(its) == 20, len(its)
    return {"title": "Tenths of amounts and dividing by 10", "items": its}


# ============================================================ set 4: add and subtract within one whole
def add_cands(x, y, d):
    s = x + y
    return [Fc(s, 2 * d), Fc(abs(x - y), d), Fc(s + 1, d), Fc(d - s, d), Fc(s - 1, d)]


def e_add(x, y, d):
    s = x + y
    return ("The parts are all %s. Add the numerators: %d + %d = <b>%d</b>. Keep the denominator %d. "
            "So %s + %s = %s, not %s." % (WORD[d], x, y, s, d, fr(x, d), fr(y, d), fr(s, d), fr(s, 2 * d)))


def sub_cands(x, y, d):
    return [Fc(x + y, d), Nc(x - y), Fc(y, d), Fc(x - y - 1, d), Fc(x - y + 1, d)]


def e_sub(x, y, d):
    return ("Subtract the numerators: %d − %d = <b>%d</b>. Keep the denominator: the parts are still %s. So the answer is %s."
            % (x, y, x - y, WORD[d], fr(x - y, d)))


def set_add_sub(rnd):
    SPOTS.left = []
    its = []
    for d, x, y in [(5, 1, 3), (7, 2, 3), (8, 3, 4), (10, 4, 5)]:
        its.append(mcq(fig(add_bar_svg(d, x, y)) + "%s + %s = ?" % (fr(x, d), fr(y, d)), Fc(x + y, d),
                       add_cands(x, y, d),
                       "Count the coloured parts: %d green and %d yellow make <b>%d</b> %s. So %s + %s = %s."
                       % (x, y, x + y, WORD[d], fr(x, d), fr(y, d), fr(x + y, d)), rnd))
    for d, x, y in [(6, 5, 2), (9, 7, 3), (10, 8, 5)]:
        its.append(mcq(fig(sub_bar_svg(d, x, y)) + "%s − %s = ?" % (fr(x, d), fr(y, d)), Fc(x - y, d),
                       sub_cands(x, y, d),
                       "%d %s are shaded and %d are crossed out. %d − %d = <b>%d</b> %s are left: %s."
                       % (x, WORD[d], y, x, y, x - y, WORD[d] if x - y > 1 else ONE[d], fr(x - y, d)), rnd))
    for x, y, d in [(1, 5, 9), (3, 4, 10), (2, 3, 6), (4, 5, 12)]:
        its.append(mcq("%s + %s = ?" % (fr(x, d), fr(y, d)), Fc(x + y, d), add_cands(x, y, d), e_add(x, y, d), rnd))
    its.append(mcq("%s + %s + %s = ?" % (fr(1, 7), fr(2, 7), fr(3, 7)), Fc(6, 7), [Fc(6, 21), Fc(5, 7), Fc(6, 14)],
                   "All the parts are sevenths. 1 + 2 + 3 = <b>6</b>. Keep the denominator: %s." % fr(6, 7), rnd))
    for x, y, d in [(7, 2, 8), (9, 6, 10), (4, 1, 5), (11, 4, 12)]:
        its.append(mcq("%s − %s = ?" % (fr(x, d), fr(y, d)), Fc(x - y, d), sub_cands(x, y, d), e_sub(x, y, d), rnd))
    for x, d in [(3, 8), (4, 10)]:
        its.append(mcq("1 − %s = ?" % fr(x, d), Fc(d - x, d), [Fc(x - 1, d), Fc(x, d), Fc(d + x, d)],
                       "1 whole = %s. Then %s − %s = <b>%s</b>." % (fr(d, d), fr(d, d), fr(x, d), fr(d - x, d)), rnd))
    its.append(mcq("%s + %s = %s" % (fr(2, 9), frq(9), fr(7, 9)), Nc(5), [Nc(9), Nc(7), Nc(2)],
                   "Think: 2 + <b>5</b> = 7. So %s + %s = %s." % (fr(2, 9), fr(5, 9), fr(7, 9)), rnd))
    its.append(mcq("%s + ? = 1" % fr(3, 5), Fc(2, 5), [Fc(3, 5), Fc(2, 10), Fc(5, 5)],
                   "1 whole = %s. 3 + <b>2</b> = 5, so %s + %s = %s = 1." % (fr(5, 5), fr(3, 5), fr(2, 5), fr(5, 5)), rnd))
    assert len(its) == 20, len(its)
    return {"title": "Add and subtract fractions within one whole", "items": its}


# ============================================================ set 5: word problems
def set_words(rnd):
    SPOTS.left = []
    its = []
    P = People(rnd)

    (n1, _, _), (n2, _, _) = P.next(), P.next()
    its.append(mcq("A cake is cut into 8 equal slices. %s eats 2 slices and %s eats 3 slices. "
                   "What fraction of the cake do they eat altogether?" % (n1, n2),
                   Fc(5, 8), [Fc(5, 16), Fc(1, 8), Fc(3, 8)],
                   "Each slice is %s. 2 + 3 = <b>5</b> slices, so they eat %s. Keep the denominator 8." % (fr(1, 8), fr(5, 8)), rnd))
    nm, he, his = P.next()
    its.append(mcq("A chocolate bar has 10 equal pieces. %s eats %s of the bar. What fraction is left?" % (nm, fr(4, 10)),
                   Fc(6, 10), [Fc(4, 10), Nc(6), Fc(4, 6)],
                   "The whole bar is %s. %s − %s = <b>%s</b> is left." % (fr(10, 10), fr(10, 10), fr(4, 10), fr(6, 10)), rnd))
    nm, he, his = P.next()
    its.append(mcq("A race is 10 laps of the school field. %s has run 7 laps. What fraction of the race has %s run?" % (nm, he),
                   Fc(7, 10), [Fc(3, 10), Fc(1, 7), Fc(10, 7)],
                   "Each lap is %s of the race. 7 laps is <b>%s</b>." % (fr(1, 10), fr(7, 10)), rnd))
    nm, he, his = P.next()
    its.append(mcq("A race is 10 laps. %s has run %s of the race. What fraction does %s still have to run?" % (nm, fr(6, 10), he),
                   Fc(4, 10), [Fc(6, 10), Fc(16, 10), Fc(4, 6)],
                   "The whole race is %s. %s − %s = <b>%s</b> is still to run." % (fr(10, 10), fr(10, 10), fr(6, 10), fr(4, 10)), rnd))
    nm, he, his = P.next()
    its.append(mcq("A pizza is cut into 6 equal slices. %s eats %s of the pizza, then %s more. How much does %s eat altogether?"
                   % (nm, fr(1, 6), fr(2, 6), he), Fc(3, 6), [Fc(3, 12), Fc(1, 6), Fc(2, 6)],
                   "1 + 2 = <b>3</b> sixths. The slices are still sixths, so the answer is %s, not %s." % (fr(3, 6), fr(3, 12)), rnd))
    nm, he, his = P.next()
    its.append(mcq("%s drinks %s of a bottle of juice. %s friend drinks %s of the bottle. What fraction of the juice is left?"
                   % (nm, fr(2, 5), cap(his), fr(1, 5)), Fc(2, 5), [Fc(3, 5), Fc(3, 10), Fc(1, 5)],
                   "They drink %s + %s = %s. The full bottle is %s. %s − %s = <b>%s</b> is left."
                   % (fr(2, 5), fr(1, 5), fr(3, 5), fr(5, 5), fr(5, 5), fr(3, 5), fr(2, 5)), rnd))
    its.append(mcq("A school garden has 9 equal beds. %s of the garden has carrots and %s has peas. "
                   "What fraction of the garden has carrots or peas?" % (fr(4, 9), fr(3, 9)),
                   Fc(7, 9), [Fc(7, 18), Fc(1, 9), Fc(2, 9)],
                   "4 + 3 = <b>7</b> ninths: %s. Keep the denominator 9." % fr(7, 9), rnd))
    nm, he, his = P.next()
    its.append(mcq("%s has 1 m of ribbon. %s cuts off %s m. How much ribbon is left?" % (nm, cap(he), fr(3, 10)),
                   Fc(7, 10, " m"), [Fc(3, 10, " m"), Nc(7, " m"), Fc(13, 10, " m")],
                   "1 m = %s m. %s − %s = <b>%s m</b>." % (fr(10, 10), fr(10, 10), fr(3, 10), fr(7, 10)), rnd))
    its.append(mcq("There are 50 sweets in a jar. %s of them are red. How many red sweets are there?" % fr(1, 10),
                   Nc(5, " sweets"), [Nc(500, " sweets"), Nc(40, " sweets"), Nc(45, " sweets")],
                   e_tenth(50, " sweets"), rnd))
    its.append(mcq("There are 20 pupils in a group. %s of them walk to school. How many pupils walk to school?" % fr(3, 10),
                   Nc(6, " pupils"), [Nc(2, " pupils"), Nc(60, " pupils"), Nc(14, " pupils")],
                   e_tenths(20, 3, " pupils"), rnd))
    its.append(mcq("Two chocolate bars are shared equally between 10 children. How much does each child get?",
                   Fc(2, 10, " of a bar"), [Fc(10, 2, " of a bar"), Fc(1, 2, " of a bar"), Fc(1, 10, " of a bar")],
                   "2 ÷ 10 = %s. Each child gets <b>%s of a bar</b>." % (fr(2, 10), fr(2, 10)), rnd))
    nm, he, his = P.next()
    its.append(mcq("%s says %s + %s = %s. What went wrong?" % (nm, fr(2, 7), fr(3, 7), fr(5, 14)),
                   "%s added the denominators" % cap(he),
                   ["%s added the numerators" % cap(he), "Nothing. %s is right" % cap(he),
                    "%s should take away" % cap(he)],
                   "The parts are sevenths, and they stay sevenths. Add only the numerators: 2 + 3 = 5. "
                   "So %s + %s = <b>%s</b>." % (fr(2, 7), fr(3, 7), fr(5, 7)), rnd))
    nm, he, his = P.next()
    its.append(mcq("%s reads %s of %s book on Monday and %s on Tuesday. What fraction of the book has %s read?"
                   % (nm, fr(2, 9), his, fr(4, 9), he), Fc(6, 9), [Fc(6, 18), Fc(2, 9), Fc(8, 9)],
                   "2 + 4 = <b>6</b> ninths: %s. Keep the denominator 9." % fr(6, 9), rnd))
    its.append(mcq("A tower has 10 cubes. 4 cubes are red and 3 cubes are blue. The rest are white. "
                   "What fraction of the tower is red or blue?", Fc(7, 10), [Fc(7, 20), Fc(3, 10), Fc(1, 10)],
                   "Red: %s. Blue: %s. %s + %s = <b>%s</b>." % (fr(4, 10), fr(3, 10), fr(4, 10), fr(3, 10), fr(7, 10)), rnd))
    its.append(mcq("A cake is cut into 12 equal slices. %s of the cake is eaten at a party. What fraction is left?" % fr(7, 12),
                   Fc(5, 12), [Fc(7, 12), Nc(5), Fc(19, 12)],
                   "The whole cake is %s. %s − %s = <b>%s</b> is left." % (fr(12, 12), fr(12, 12), fr(7, 12), fr(5, 12)), rnd))
    (n1, _, _), (n2, _, _) = P.next(), P.next()
    its.append(mcq("%s has %s of a pizza. %s has %s of the same pizza. How much more does %s have?"
                   % (n1, fr(3, 8), n2, fr(5, 8), n2), Fc(2, 8), [Fc(8, 8), Nc(2), Fc(5, 8)],
                   "Find the difference: %s − %s = <b>%s</b>." % (fr(5, 8), fr(3, 8), fr(2, 8)), rnd))
    nm, he, his = P.next()
    its.append(mcq("%s colours %s of a picture in the morning and %s after lunch. What fraction is <b>not</b> coloured yet?"
                   % (nm, fr(4, 10), fr(5, 10)), Fc(1, 10), [Fc(9, 10), Fc(9, 20), Nc(0)],
                   "%s + %s = %s is coloured. %s − %s = <b>%s</b> is not coloured yet."
                   % (fr(4, 10), fr(5, 10), fr(9, 10), fr(10, 10), fr(9, 10), fr(1, 10)), rnd))
    nm, he, his = P.next()
    its.append(mcq("%s has a ribbon 90 cm long. %s cuts off %s of it. How long is the piece %s cuts off?"
                   % (nm, cap(he), fr(1, 10), he), Nc(9, " cm"), [Nc(900, " cm"), Nc(80, " cm"), Nc(81, " cm")],
                   e_tenth(90, " cm"), rnd))
    its.append(mcq("There are 30 cubes in a box. %s of them are red. How many red cubes are there?" % fr(4, 10),
                   Nc(12, " cubes"), [Nc(3, " cubes"), Nc(120, " cubes"), Nc(18, " cubes")],
                   e_tenths(30, 4, " cubes"), rnd))
    nm, he, his = P.next()
    its.append(mcq("%s cuts a 1 m plank of wood into 10 equal pieces. How long is each piece?" % nm,
                   Nc(10, " cm"), [Nc(1, " cm"), Nc(100, " cm"), Nc(90, " cm")],
                   "1 m = 100 cm. Each piece is %s of 1 m: 100 ÷ 10 = <b>10 cm</b>." % fr(1, 10), rnd))
    assert len(its) == 20, len(its)
    return {"title": "Fraction word problems", "items": its}


# ============================================================ lesson
def body_html():
    return (
        "<h2>What is a tenth?</h2>"
        "<p>Split 1 whole into <b>10 equal parts</b>. Each part is <b>one tenth</b>: " + fr(1, 10) + ". "
        "The parts must be the same size.</p>"
        "<figure class='sn-fig'>" + tenths_bar_svg(3) +
        "<figcaption>3 of the 10 equal parts are shaded: " + fr(3, 10) + " (three tenths). "
        "10 tenths make 1 whole.</figcaption></figure>"
        "<h2>Counting in tenths</h2>"
        "<p>Count up in tenths by adding 1 to the numerator. The denominator stays 10. "
        "When you get to " + fr(10, 10) + ", you have <b>1 whole</b>. Then keep going: 1 " + fr(1, 10) + ", 1 " + fr(2, 10) + " …</p>"
        "<figure class='sn-fig'>" + tline_svg(2, 11) +
        "<figcaption>" + fr(8, 10) + ", " + fr(9, 10) + ", 1, 1 " + fr(1, 10) + ". The dot is at 1 " + fr(1, 10) + ".</figcaption></figure>"
        + ex("Example", "Count down in tenths: 1 " + fr(1, 10) + ", 1, ?",
             "1 whole is " + fr(10, 10) + ". One tenth less is " + fr(9, 10) + ".", fr(9, 10))
        + "<p>In Year 4 you will also write tenths as decimals: " + fr(3, 10) + " = 0.3.</p>"
        "<h2>Tenths of amounts</h2>"
        "<p>To find " + fr(1, 10) + " of a number, <b>divide by 10</b>.</p>"
        "<figure class='sn-fig'>" + model_svg(30, 10, 1, parts_text="3") +
        "<figcaption>" + fr(1, 10) + " of 30: 30 ÷ 10 = 3 in each part.</figcaption></figure>"
        + ex("Example", "What is " + fr(3, 10) + " of 40?", "40 ÷ 10 = 4 for one tenth. Three tenths: 4 × 3 = 12.", "12")
        + "<p>Dividing a one-digit number by 10 gives tenths. Share 3 cakes between 10 children: "
        "each child gets " + fr(3, 10) + " of a cake. So 3 ÷ 10 = " + fr(3, 10) + ".</p>"
        "<h2>Adding and subtracting fractions</h2>"
        "<p>When the denominators are the same, the parts are the same size. "
        "Add or subtract the <b>numerators</b>. Keep the <b>denominator</b>.</p>"
        "<figure class='sn-fig'>" + add_bar_svg(7, 2, 3) +
        "<figcaption>" + fr(2, 7) + " + " + fr(3, 7) + " = " + fr(5, 7) + ": 2 green sevenths and 3 yellow sevenths make 5 sevenths.</figcaption></figure>"
        + ex("Example", fr(9, 10) + " − " + fr(4, 10) + " = ?", "Subtract the numerators: 9 − 4 = 5. The parts are still tenths.", fr(5, 10))
        + ex("Example", "1 − " + fr(3, 8) + " = ?", "1 whole = " + fr(8, 8) + ". Then 8 − 3 = 5.", fr(5, 8))
        + "<h2>Common mistakes</h2>"
        + table(["Mistake", "What to do instead"], [
            ["Adding the denominators: " + fr(2, 7) + " + " + fr(3, 7) + " = " + fr(5, 14),
             "Keep the denominator: " + fr(2, 7) + " + " + fr(3, 7) + " = " + fr(5, 7)],
            ["Counting " + fr(9, 10) + ", " + fr(10, 10) + ", " + fr(11, 10) + " and not seeing the whole",
             fr(10, 10) + " is 1 whole: " + fr(9, 10) + ", 1, 1 " + fr(1, 10)],
            [fr(1, 10) + " of 30 = 300", "A tenth is smaller. Divide by 10: 30 ÷ 10 = 3"],
            ["3 ÷ 10 = " + fr(10, 3), "The number you divide goes on top: 3 ÷ 10 = " + fr(3, 10)],
            ["Counting the tick marks on a number line, not the spaces", "Count the jumps from 0"],
        ])
    )


FAQ = [
    {"q": "What fractions do Year 3 children learn?",
     "a": "In Year 3 children count up and down in tenths, find fractions of amounts, find equivalent fractions with diagrams, compare fractions, and add and subtract fractions with the same denominator within one whole, such as 5/7 + 1/7 = 6/7."},
    {"q": "How do you count in tenths?",
     "a": "Add one tenth each time: 7/10, 8/10, 9/10, 1, 1 1/10. Ten tenths make 1 whole, so 10/10 is written as 1."},
    {"q": "How do you find a tenth of a number?",
     "a": "Divide the number by 10. For example, 1/10 of 30 is 30 ÷ 10 = 3, and 3/10 of 30 is 3 × 3 = 9."},
    {"q": "Why don’t you add the denominators when adding fractions?",
     "a": "The denominator tells you the size of the parts, and adding does not change their size. 2/7 + 3/7 is 5 sevenths, so the answer is 5/7, not 5/14."},
]


def gen():
    rnd = random.Random(3307)
    SPOTS.left = []
    sets = [set_shapes(rnd), set_counting(rnd), set_amounts(rnd), set_add_sub(rnd), set_words(rnd)]
    seen = set()
    for s in sets:
        assert len(s["items"]) == 20, (s["title"], len(s["items"]))
        cnt = [0, 0, 0, 0]
        for it in s["items"]:
            assert len(set(it["c"])) == 4, it
            cnt[it["a"]] += 1
            assert it["q"] not in seen, it["q"]
            seen.add(it["q"])
        assert cnt == [5, 5, 5, 5], (s["title"], cnt)
    return {
        "country": "uk", "subject": "maths", "grade": "year-3", "slug": "tenths-and-adding-fractions", "sort": 7,
        "updated": UPDATED, "pdf_url": "",
        "title": "Year 3 Tenths and Adding Fractions",
        "seo_title": "Year 3 Tenths and Adding Fractions Worksheets: Counting in Tenths, Tenths of Amounts (Free, with Answers)",
        "short_title": "Tenths and adding fractions",
        "domain": "Fractions",
        "standard_code": "Year 3: Fractions",
        "standard_url": "https://www.gov.uk/government/publications/national-curriculum-in-england-mathematics-programmes-of-study",
        "standard_text": "Count up and down in tenths; recognise that tenths arise from dividing an object into 10 equal parts and in dividing one-digit numbers or quantities by 10; add and subtract fractions with the same denominator within one whole [for example, 5/7 + 1/7 = 6/7].",
        "meta_desc": "Free Year 3 maths worksheets on tenths for the National Curriculum: tenths of a shape, counting up and down in tenths, tenths of amounts, dividing by 10, and adding and subtracting fractions within one whole. 100 questions with an answer key.",
        "key_big": "A tenth is 1 of 10 equal parts. To add fractions with the same denominator, add the numerators and keep the denominator.",
        "key_sub": "Count in tenths: 8/10, 9/10, 1, 1 1/10. 1/10 of 30 = 30 ÷ 10 = 3. 3 ÷ 10 = 3/10. 2/7 + 3/7 = 5/7, not 5/14.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, "tenths-and-adding-fractions.json")
    mark_large(u, "(number line|bar model|four bars)")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(u, f, ensure_ascii=False, indent=1)
    print("wrote", path)
