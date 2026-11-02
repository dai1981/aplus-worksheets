# -*- coding: utf-8 -*-
"""
Singapore Primary 2 Maths: Fractions
(MOE 2021 Primary Mathematics Syllabus, Standard. Primary 2: Fractions)
  python3 tools/gen_sg_maths_p2_fractions.py
Fraction as part of a whole: equal parts, naming and writing the fraction shaded (numerator and
denominator), unit fractions (more parts, smaller parts), comparing like fractions, ordering unit and
like fractions, and word problems with bar models. Denominators do not exceed 12.
Wrong choices come from real mistakes (calling unequal parts halves or quarters, thinking 1/8 > 1/4,
counting the unshaded parts, writing shaded over unshaded, counting the cut lines instead of the parts,
writing the fraction upside down) and are never equal in value to the answer or to each other.
Every answer is checked in code with fractions.Fraction.
HTML attributes use single quotes (no backslashes in the JSON). Singapore English. 7-8-year-olds.
"""
import json, math, os, random, re
from fractions import Fraction

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "sg", "maths", "primary-2")
UPDATED = "2026-11-03"
FILL = "#4fae74"      # shaded parts
FILL3 = "#8fb8e8"     # bar models
LINE = "#2b2b2b"
WORD = {2: "halves", 3: "thirds", 4: "quarters", 5: "fifths", 6: "sixths", 7: "sevenths", 8: "eighths", 9: "ninths",
        10: "tenths", 11: "elevenths", 12: "twelfths"}
ONE = {2: "half", 3: "third", 4: "quarter", 5: "fifth", 6: "sixth", 7: "seventh", 8: "eighth", 9: "ninth",
       10: "tenth", 11: "eleventh", 12: "twelfth"}
NUM = {1: "one", 2: "two", 3: "three", 4: "four", 5: "five", 6: "six", 7: "seven", 8: "eight", 9: "nine",
       10: "ten", 11: "eleven", 12: "twelve"}
GRID = {4: (2, 2), 6: (2, 3), 8: (2, 4), 9: (3, 3), 10: (2, 5), 12: (3, 4)}   # rows, columns


# ------------------------------------------------------------ numbers
def fr(a, b):
    return "<span class='fr'><span class='fn'>%s</span><span class='fd'>%s</span></span>" % (a, b)


def frs(fs):
    return ", ".join(fr(*f) for f in fs)


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
    """ans and cands are (n, d) pairs. A candidate equal in VALUE to the answer or to another choice is skipped."""
    vals, pick = {Fraction(*ans)}, []
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
    return {"q": q, "c": ["A", "B", "C", "D"], "a": pos, "e": e}


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


def cmp_sym(a, b):
    """The true sign between two fractions (as HTML)."""
    return "&gt;" if a > b else ("&lt;" if a < b else "=")


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


# ------------------------------------------------------------ shapes
def rect(x, y, w, h, filled, col=FILL):
    return ("<rect x='%.2f' y='%.2f' width='%.2f' height='%.2f' fill='%s' stroke='%s' stroke-width='2.4'/>"
            % (x, y, w, h, col if filled else "#fff", LINE))


def poly(pts, filled):
    return ("<polygon points='%s' fill='%s' stroke='%s' stroke-width='2.4' stroke-linejoin='round'/>"
            % (" ".join("%.1f,%.1f" % p for p in pts), FILL if filled else "#fff", LINE))


def slices(cx, cy, r, parts, sh):
    """Circle cut from the centre; parts are the sizes (as parts of 1)."""
    s, a = [], -90.0
    for i, p in enumerate(parts):
        a0, a1 = math.radians(a), math.radians(a + 360.0 * p)
        big = 1 if p > 0.5 else 0
        s.append("<path d='M%.1f %.1f L%.2f %.2f A%.1f %.1f 0 %d 1 %.2f %.2f Z' fill='%s' stroke='%s' "
                 "stroke-width='2.4' stroke-linejoin='round'/>"
                 % (cx, cy, cx + r * math.cos(a0), cy + r * math.sin(a0), r, r, big,
                    cx + r * math.cos(a1), cy + r * math.sin(a1), FILL if i in sh else "#fff", LINE))
        a += 360.0 * p
    return "".join(s)


def piece(kind, n, sh, x, y, S, widths=None):
    """One shape in an S x S box at (x, y). sh: set of shaded part indexes.
    kinds: circle (n slices, sizes from widths if given), chord (circle cut into 2 unequal parts),
    square (n upright strips), bar (a long thin strip), grid (rows x columns), diag (square cut on the diagonals)."""
    s = []
    if kind == "circle":
        parts = widths or [1.0 / n] * n
        s.append(slices(x + S / 2.0, y + S / 2.0, S / 2.0, parts, sh))
    elif kind == "chord":
        r = S / 2.0
        cx, cy = x + r, y + r
        d = 0.42 * r
        h = math.sqrt(r * r - d * d)
        s.append("<circle cx='%.1f' cy='%.1f' r='%.1f' fill='%s' stroke='%s' stroke-width='2.4'/>"
                 % (cx, cy, r, FILL if 1 in sh else "#fff", LINE))
        s.append("<path d='M%.1f %.1f A%.1f %.1f 0 0 1 %.1f %.1f Z' fill='%s' stroke='%s' stroke-width='2.4' stroke-linejoin='round'/>"
                 % (cx + d, cy - h, r, r, cx + d, cy + h, FILL if 0 in sh else "#fff", LINE))
    elif kind in ("square", "bar"):
        H = S if kind == "square" else S * 0.42
        y0 = y + (S - H) / 2
        ws = [w * S for w in widths] if widths else [S / float(n)] * n
        xx = x
        for i, w in enumerate(ws):
            s.append(rect(xx, y0, w, H, i in sh))
            xx += w
    elif kind == "grid":
        r, c = GRID[n]
        for i in range(n):
            s.append(rect(x + (i % c) * S / float(c), y + (i // c) * S / float(r), S / float(c), S / float(r), i in sh))
    elif kind == "diag":
        TL, TR, BR, BL = (x, y), (x + S, y), (x + S, y + S), (x, y + S)
        C = (x + S / 2.0, y + S / 2.0)
        tris = [(TL, TR, BR), (TL, BR, BL)] if n == 2 else [(TL, TR, C), (TR, BR, C), (BR, BL, C), (BL, TL, C)]
        for i, t in enumerate(tris):
            s.append(poly(t, i in sh))
    else:
        raise ValueError(kind)
    return "".join(s)


def shape_name(kind):
    return {"circle": "circle", "chord": "circle", "square": "square", "diag": "square",
            "grid": "rectangle", "bar": "strip"}[kind]


def shape_svg(kind, n, sh, widths=None):
    """A single shape. Bars and grids get their own sizes so the parts look right."""
    eq = "" if (kind == "chord" or widths) else "equal "
    lab = "%s cut into %d %sparts with %d shaded" % (shape_name(kind), n, eq, len(sh))
    if kind == "bar":
        W, H = 264, 48
        ws = [w * W for w in widths] if widths else [W / float(n)] * n
        s, xx = [], 6.0
        for i, w in enumerate(ws):
            s.append(rect(xx, 6, w, H, i in sh))
            xx += w
        return svg_wrap(W + 12, H + 12, "".join(s), "bar of " + lab)
    if kind == "grid":
        r, c = GRID[n]
        cs = 40
        s = [rect(6 + (i % c) * cs, 6 + (i // c) * cs, cs, cs, i in sh) for i in range(n)]
        return svg_wrap(c * cs + 12, r * cs + 12, "".join(s), lab)
    return svg_wrap(112, 112, piece(kind, n, sh, 6, 6, 100, widths), lab)


def four_svg(specs, S=78):
    """Four shapes A-D in a row, the letter above each. specs: (kind, n, shaded, widths)."""
    s = []
    cw = S + 26
    for i, (kind, n, sh, ws) in enumerate(specs):
        x0 = 6 + i * cw
        s.append(txt(x0 + S / 2, 22, "ABCD"[i], 18))
        s.append(piece(kind, n, sh, x0, 32, S, ws))
    return svg_wrap(6 + 4 * cw - 26 + 6, 32 + S + 6, "".join(s), "four pictures A to D")


def bar_cells(x0, y0, W, Hh, d, k, col=FILL):
    s = "".join("<rect x='%.2f' y='%.1f' width='%.2f' height='%d' fill='%s' stroke='%s' stroke-width='2.2'/>"
                % (x0 + i * W / float(d), y0, W / float(d), Hh, col if i < k else "#fff", LINE) for i in range(d))
    return s + ("<rect x='%.2f' y='%.1f' width='%.2f' height='%d' fill='none' stroke='%s' stroke-width='3'/>"
                % (x0, y0, W, Hh, LINE))


def bars_svg(rows, W=264, Hh=34, gap=10, name="bars", col=FILL):
    """rows: list of (d, k, label). label is a pair (n, d) drawn as a fraction or a string (a name).
    All bars have the same length, so equal shaded lengths mean equal fractions."""
    words = [r[2] for r in rows if isinstance(r[2], str)]
    x0 = (max(len(w) for w in words) * 9.4 + 16) if words else 50
    s = []
    for j, (d, k, lab) in enumerate(rows):
        y = 6 + j * (Hh + gap)
        s.append(bar_cells(x0, y, W, Hh, d, k, col))
        yc = y + Hh / 2.0
        if isinstance(lab, tuple):
            s.append(sfr(24, yc - 5, lab[0], lab[1], 15))
        elif lab:
            s.append(txt(x0 - 8, yc + 5, lab, 15, anchor="end"))
    n = len(rows)
    desc = "; ".join("%d of %d parts shaded" % (k, d) for d, k, _ in rows)
    return svg_wrap(x0 + W + 6, 12 + n * Hh + (n - 1) * gap, "".join(s), "%s of the same length: %s" % (name, desc))


def units_svg(units, shaded, top, bottom, W=264, Hh=36, rest=None):
    """Bar model: a bar of equal units, the first `shaded` units coloured.
    top labels the whole bar (brace above), bottom labels the shaded units (brace below),
    rest (if given) labels the white units (brace below)."""
    s = [txt(6 + W / 2.0, 18, top, 16), brace(6, 6 + W, 48, up=True)]
    yb = 56
    for i in range(units):
        s.append("<rect x='%.2f' y='%d' width='%.2f' height='%d' fill='%s' stroke='%s' stroke-width='2.2'/>"
                 % (6 + i * W / float(units), yb, W / float(units), Hh, FILL3 if i < shaded else "#fff", LINE))
    xs = 6 + W * shaded / float(units)
    s.append(brace(8, xs - 2, yb + Hh + 6, up=False))
    cx = max((6 + xs) / 2.0, 6 + 4.6 * len(bottom))
    s.append(txt(cx, yb + Hh + 40, bottom, 16))
    if rest:
        s.append(brace(xs + 2, 4 + W, yb + Hh + 6, up=False))
        s.append(txt(min((xs + 6 + W) / 2.0, 6 + W - 4.6 * len(rest)), yb + Hh + 40, rest, 16))
        assert (xs + 6 + W) / 2.0 - 4.6 * len(rest) > cx + 4.6 * len(bottom) + 8, (bottom, rest)
    return svg_wrap(W + 12, yb + Hh + 50, "".join(s), "bar model of %d equal units, %d shaded" % (units, shaded))


# ============================================================ set 1: equal parts
def abcd(rnd, q, good, bad, e_good):
    """good: spec; bad: list of (spec, why). Puts the right picture at the next spot."""
    pos = SPOTS.next(rnd)
    order = [x[0] for x in bad[:pos]] + [good] + [x[0] for x in bad[pos:]]
    letters = [L for i, L in enumerate("ABCD") if i != pos]
    why = " ".join("%s %s." % (L, d) for L, (_, d) in zip(letters, bad))
    return mcq_letters(fig(four_svg(order)) + q, pos, "%s That is <b>%s</b>. %s" % (e_good, "ABCD"[pos], why))


NOTEQ = "Not equal parts"


def set_equal(rnd):
    SPOTS.left = []
    its = []
    NE = "has %d parts, but they are <b>not equal</b>"
    its.append(abcd(rnd, "Which shape is cut into <b>halves</b>?",
                    ("square", 2, set(), None),
                    [(("chord", 2, set(), None), NE % 2),
                     (("square", 3, set(), None), "has 3 equal parts"),
                     (("square", 2, set(), [0.3, 0.7]), NE % 2)],
                    "Halves are <b>2 equal parts</b>."))
    its.append(abcd(rnd, "Which shape is cut into <b>thirds</b>?",
                    ("circle", 3, set(), None),
                    [(("square", 3, set(), [0.2, 0.3, 0.5]), NE % 3),
                     (("circle", 4, set(), None), "has 4 equal parts"),
                     (("circle", 3, set(), [0.5, 0.25, 0.25]), NE % 3)],
                    "Thirds are <b>3 equal parts</b>."))
    its.append(abcd(rnd, "Which shape is cut into <b>quarters</b>?",
                    ("grid", 4, set(), None),
                    [(("square", 4, set(), [0.1, 0.2, 0.3, 0.4]), NE % 4),
                     (("circle", 3, set(), None), "has 3 equal parts"),
                     (("diag", 2, set(), None), "has 2 equal parts")],
                    "Quarters are <b>4 equal parts</b>."))
    its.append(abcd(rnd, "Which shape is cut into <b>sixths</b>?",
                    ("circle", 6, set(), None),
                    [(("square", 6, set(), [0.06, 0.1, 0.12, 0.18, 0.24, 0.3]), NE % 6),
                     (("circle", 8, set(), None), "has 8 equal parts"),
                     (("grid", 4, set(), None), "has 4 equal parts")],
                    "Sixths are <b>6 equal parts</b>."))
    its.append(abcd(rnd, "Which shape is cut into <b>fifths</b>?",
                    ("square", 5, set(), None),
                    [(("square", 5, set(), [0.06, 0.1, 0.16, 0.28, 0.4]), NE % 5),
                     (("circle", 6, set(), None), "has 6 equal parts"),
                     (("diag", 4, set(), None), "has 4 equal parts")],
                    "Fifths are <b>5 equal parts</b>."))
    its.append(abcd(rnd, "Which shape is <b>not</b> cut into equal parts?",
                    ("circle", 4, set(), [0.4, 0.2, 0.2, 0.2]),
                    [(("diag", 4, set(), None), "has 4 equal parts"),
                     (("square", 3, set(), None), "has 3 equal parts"),
                     (("circle", 5, set(), None), "has 5 equal parts")],
                    "Look for parts of different sizes."))
    # how many equal parts? (some are not equal)
    for kind, n, ws in [("circle", 5, None), ("bar", 4, [0.15, 0.35, 0.2, 0.3]), ("grid", 6, None),
                        ("circle", 3, [0.5, 0.3, 0.2]), ("bar", 8, None), ("square", 2, [0.36, 0.64])]:
        q = fig(shape_svg(kind, n, set(), ws)) + "How many equal parts is the %s cut into?" % shape_name(kind)
        if ws:
            e = ("The %s has %d parts, but they are <b>not the same size</b>. So they are <b>not equal parts</b>. "
                 "We cannot use them to make a fraction." % (shape_name(kind), n))
            its.append(mcq(q, NOTEQ, [str(n), str(n + 1), str(n - 1) if n > 2 else str(n * 2)], e, rnd))
        else:
            lines = n - 1 if kind in ("bar", "grid") else n
            e = ("Count the parts, not the lines. All the parts are the same size. There are <b>%d equal parts</b>." % n)
            cands = [NOTEQ, str(n - 1), str(n + 1), str(lines)]
            its.append(mcq(q, str(n), cands, e, rnd))
    # what fraction is each part?
    for kind, n in [("bar", 6), ("grid", 8), ("circle", 7), ("bar", 10)]:
        q = fig(shape_svg(kind, n, set())) + "The %s is cut into %d equal parts. What fraction of the whole is <b>1 part</b>?" % (shape_name(kind), n)
        e = ("There are <b>%d</b> equal parts, so each part is <b>one %s</b>: %s. "
             "The bottom number is the number of equal parts." % (n, ONE[n], fr(1, n)))
        its.append(mcq_fr(q, (1, n), [(1, n - 1),      # counted the cut lines
                                      (n, 1),          # wrote it upside down
                                      (n - 1, n),      # counted the other parts
                                      (1, n + 1)], e, rnd))
    # names and wholes
    for n in (8, 12):
        e = ("One whole cut into %s has <b>%d</b> equal parts. So %d %s make 1 whole: %s = 1." % (WORD[n], n, n, WORD[n], fr(n, n)))
        its.append(mcq_n("How many %s make 1 whole?" % WORD[n], n, [1, n - 1, 2 * n, n // 2], e, rnd))
    its.append(mcq("A shape is cut into 3 equal parts. What is each part called?", "one third",
                   ["one three", "one half", "one quarter"],
                   "3 equal parts are called <b>thirds</b>. Each part is one third: %s." % fr(1, 3), rnd))
    its.append(mcq("Mei Ling cuts a paper strip into 2 parts. One part is longer than the other. "
                   "Is each part a half?",
                   "No, they are not equal", ["Yes, there are 2 parts", "Yes, she cut it once", "No, they are quarters"],
                   "Halves must be <b>2 equal parts</b>. One part is longer, so they are not halves.", rnd))
    assert len(its) == 20, len(its)
    return {"title": "Equal parts", "items": its}


# ============================================================ set 2: name the fraction shaded
def set_name(rnd):
    SPOTS.left = []
    its = []
    for kind, n, k in [("bar", 3, 2), ("circle", 5, 2), ("grid", 6, 1), ("bar", 8, 3), ("circle", 6, 5), ("grid", 9, 4),
                       ("bar", 10, 7), ("grid", 12, 5), ("circle", 8, 3), ("bar", 7, 4), ("grid", 10, 3), ("circle", 12, 7)]:
        sh = set(rnd.sample(range(n), k)) if kind == "grid" else set(range(k))
        q = fig(shape_svg(kind, n, sh)) + "What fraction of the %s is shaded?" % shape_name(kind)
        e = ("There are <b>%d equal parts</b> in all. <b>%d %s shaded</b>. So %s of the %s is shaded."
             % (n, k, "is" if k == 1 else "are", fr(k, n), shape_name(kind)))
        its.append(mcq_fr(q, (k, n), [(n - k, n),        # counted the unshaded parts
                                      (k, n - k),        # shaded over unshaded
                                      (k + 1, n), (k - 1, n), (k, n + 1)], e, rnd))
    for kind, n, k in [("circle", 5, 3), ("bar", 8, 5), ("grid", 6, 4)]:
        sh = set(rnd.sample(range(n), k)) if kind == "grid" else set(range(k))
        q = fig(shape_svg(kind, n, sh)) + "What fraction of the %s is <b>not</b> shaded?" % shape_name(kind)
        e = ("There are %d equal parts. %d are shaded, so <b>%d %s not shaded</b>. The answer is %s."
             % (n, k, n - k, "is" if n - k == 1 else "are", fr(n - k, n)))
        its.append(mcq_fr(q, (n - k, n), [(k, n),             # gave the shaded part
                                          (n - k, k),         # unshaded over shaded
                                          (n - k + 1, n), (n - k - 1, n)], e, rnd))
    its.append(abcd(rnd, "Which shape has %s shaded?" % fr(3, 5),
                    ("square", 5, {0, 1, 2}, None),
                    [(("square", 5, {0, 1}, None), "shows %s" % fr(2, 5)),
                     (("circle", 6, {0, 1, 2}, None), "has 6 parts, so it shows %s" % fr(3, 6)),
                     (("square", 5, {0, 1, 2}, [0.08, 0.12, 0.2, 0.25, 0.35]), "has 5 parts, but they are <b>not equal</b>")],
                    "%s needs <b>5 equal parts</b> with <b>3</b> shaded." % fr(3, 5)))
    its.append(abcd(rnd, "Which shape has %s shaded?" % fr(2, 3),
                    ("circle", 3, {0, 1}, None),
                    [(("circle", 3, {0}, None), "shows %s" % fr(1, 3)),
                     (("square", 3, {0, 1}, [0.2, 0.25, 0.55]), "has 3 parts, but they are <b>not equal</b>"),
                     (("diag", 4, {0, 1}, None), "has 4 parts, so it shows %s" % fr(2, 4))],
                    "%s needs <b>3 equal parts</b> with <b>2</b> shaded." % fr(2, 3)))
    its.append(mcq_fr("Which fraction is <b>two fifths</b>?", (2, 5), [(5, 2), (1, 5), (3, 5)],
                      "Two fifths means <b>2</b> parts out of <b>5</b> equal parts. The 2 goes on top and the 5 goes "
                      "at the bottom: %s." % fr(2, 5), rnd))
    its.append(mcq("In %s, what does the <b>9</b> tell you?" % fr(4, 9), "9 equal parts in all",
                   ["9 parts are shaded", "9 parts are not shaded", "The whole is 9 cm"],
                   "The bottom number (the <b>denominator</b>) tells you how many equal parts make the whole: 9. "
                   "The top number (the numerator) tells you how many parts we take: 4.", rnd))
    its.append(mcq_n("In %s, which number is the <b>numerator</b>?" % fr(5, 11), 5, [11, 6, 16],
                     "The numerator is the <b>top</b> number: 5. The denominator is the bottom number: 11.", rnd))
    assert len(its) == 20, len(its)
    return {"title": "Name the fraction shaded", "items": its}


# ============================================================ set 3: unit fractions
def stmt_q(rnd, pairs, true_i):
    """pairs: list of (a, b) unit-fraction denominators with sign '>'. Exactly pairs[true_i] is true."""
    ch = []
    for i, (a, b, sym) in enumerate(pairs):
        ok = (Fraction(1, a) > Fraction(1, b)) if sym == ">" else (Fraction(1, a) < Fraction(1, b))
        assert ok == (i == true_i), (a, b, sym)
        ch.append("%s %s %s" % (fr(1, a), "&gt;" if sym == ">" else "&lt;", fr(1, b)))
    return ch[true_i], [c for i, c in enumerate(ch) if i != true_i]


def set_unit(rnd):
    SPOTS.left = []
    its = []
    # A: pictures of four unit fractions
    for word, ds in [("greatest", [4, 2, 8, 3]), ("smallest", [3, 6, 10, 5]), ("greatest", [6, 12, 3, 9]),
                     ("smallest", [2, 4, 5, 12])]:
        best = min(ds) if word == "greatest" else max(ds)
        q = (fig(bars_svg([(d, 1, (1, d)) for d in ds])) +
             "All the bars are the same length. Which fraction is the %s?" % word)
        e = ("Look at the shaded parts. The bar cut into the <b>%s</b> parts has the %s part. "
             "%s The answer is <b>%s</b>."
             % ("fewest" if word == "greatest" else "most", "longest" if word == "greatest" else "shortest",
                "Fewer parts means bigger parts." if word == "greatest" else "More parts means smaller parts.", fr(1, best)))
        its.append(mcq_fr(q, (1, best), [(1, d) for d in ds if d != best], e, rnd))
    # B: no pictures
    for word, ds in [("greatest", [5, 12, 3, 9]), ("smallest", [6, 4, 10, 7]), ("greatest", [8, 11, 6, 7]),
                     ("smallest", [2, 9, 3, 5]), ("greatest", [10, 4, 12, 8]), ("smallest", [7, 12, 11, 9])]:
        best = min(ds) if word == "greatest" else max(ds)
        e = ("All the numerators are 1. The %s denominator gives the %s parts. The %s is <b>%s</b>."
             % ("smallest" if word == "greatest" else "biggest", "biggest" if word == "greatest" else "smallest",
                word, fr(1, best)))
        its.append(mcq_fr("Which is the %s: %s?" % (word, frs([(1, d) for d in ds])),
                          (1, best), [(1, d) for d in ds if d != best], e, rnd))
    # C: true statements
    for qn, (pairs, ti, e) in enumerate([
            ([(4, 8, ">"), (8, 4, ">"), (6, 3, ">"), (10, 2, ">")], 0,
             "A whole cut into 4 parts has bigger parts than a whole cut into 8 parts. So <b>%s &gt; %s</b>."
             % (fr(1, 4), fr(1, 8))),
            ([(3, 5, "<"), (9, 6, "<"), (2, 12, "<"), (4, 7, "<")], 1,
             "More parts means smaller parts. Ninths are smaller than sixths, so <b>%s &lt; %s</b>." % (fr(1, 9), fr(1, 6))),
            ([(12, 10, ">"), (7, 5, ">"), (6, 2, ">"), (5, 11, ">")], 3,
             "Fifths are bigger than elevenths (fewer parts, bigger parts). So <b>%s &gt; %s</b>." % (fr(1, 5), fr(1, 11)))]):
        r, w = stmt_q(rnd, pairs, ti)
        its.append(mcq(["Which is true?", "Which is correct?", "Which one is true?"][qn], r, w, e, rnd))
    # D: greater than / smaller than
    its.append(mcq_fr("Which unit fraction is <b>greater</b> than %s?" % fr(1, 6), (1, 5), [(1, 7), (1, 9), (1, 12)],
                      "A unit fraction is greater when its denominator is <b>smaller</b>. 5 is smaller than 6, so "
                      "<b>%s &gt; %s</b>." % (fr(1, 5), fr(1, 6)), rnd))
    its.append(mcq_fr("Which unit fraction is <b>smaller</b> than %s?" % fr(1, 5), (1, 8), [(1, 2), (1, 3), (1, 4)],
                      "A unit fraction is smaller when its denominator is <b>bigger</b>. 8 is bigger than 5, so "
                      "<b>%s &lt; %s</b>." % (fr(1, 8), fr(1, 5)), rnd))
    # E: missing denominator
    for d, sym, right, cands in [(4, ">", 3, [5, 8, 4]), (6, "<", 7, [5, 2, 6]), (9, ">", 8, [10, 12, 9])]:
        assert (Fraction(1, right) > Fraction(1, d)) == (sym == ">") and Fraction(1, right) != Fraction(1, d)
        for c in cands:
            assert not ((Fraction(1, c) > Fraction(1, d)) if sym == ">" else (Fraction(1, c) < Fraction(1, d)))
        q = "Which number can go in the box?<br>%s %s %s" % (fr(1, "☐"), "&gt;" if sym == ">" else "&lt;", fr(1, d))
        e = ("%s: the denominator must be <b>%s</b> than %d. Only %d works: %s %s %s. "
             "(%s is not %s than %s, so %d does not work.)"
             % ("To be greater, the parts must be bigger" if sym == ">" else "To be smaller, the parts must be smaller",
                "smaller" if sym == ">" else "bigger", d, right, fr(1, right), "&gt;" if sym == ">" else "&lt;", fr(1, d),
                fr(1, d), "greater" if sym == ">" else "smaller", fr(1, d), d))
        its.append(mcq_n(q, right, cands, e, rnd))
    its.append(mcq("A cake is cut into <b>more</b> equal pieces. What happens to each piece?", "It gets smaller",
                   ["It gets bigger", "It stays the same", "It gets heavier"],
                   "The same cake is shared into more pieces, so each piece is <b>smaller</b>. "
                   "That is why %s is smaller than %s." % (fr(1, 8), fr(1, 4)), rnd))
    its.append(mcq("Kavya says %s is greater than %s because 10 is greater than 5. Is she right?" % (fr(1, 10), fr(1, 5)),
                   "No, %s is greater" % fr(1, 5), ["Yes, 10 &gt; 5", "No, they are equal", "Yes, tenths are bigger"],
                   "A whole cut into 10 parts has <b>smaller</b> parts than a whole cut into 5. So %s &gt; %s."
                   % (fr(1, 5), fr(1, 10)), rnd))
    assert len(its) == 20, len(its)
    return {"title": "Unit fractions: more parts, smaller parts", "items": its}


# ============================================================ set 4: compare like fractions
def set_like(rnd):
    SPOTS.left = []
    its = []
    for word, d, ns in [("greatest", 5, [2, 4, 1, 3]), ("smallest", 8, [5, 3, 7, 6]), ("greatest", 6, [4, 1, 5, 3]),
                        ("smallest", 10, [9, 4, 6, 7])]:
        best = max(ns) if word == "greatest" else min(ns)
        q = (fig(bars_svg([(d, n, (n, d)) for n in ns])) +
             "All the bars are the same length. Which fraction is the %s?" % word)
        e = ("All the bars have %d equal parts. The bar with the %s shaded parts shows the %s fraction: <b>%s</b>."
             % (d, "most" if word == "greatest" else "fewest", word, fr(best, d)))
        its.append(mcq_fr(q, (best, d), [(n, d) for n in ns if n != best], e, rnd))
    for word, d, ns in [("greatest", 9, [2, 7, 4, 5]), ("smallest", 7, [6, 3, 5, 4]), ("greatest", 12, [5, 11, 7, 9]),
                        ("smallest", 11, [8, 10, 2, 6]), ("greatest", 8, [3, 1, 5, 7]), ("smallest", 12, [7, 5, 10, 11])]:
        best = max(ns) if word == "greatest" else min(ns)
        e = ("The denominators are all %d, so the parts are the same size. Compare the numerators: the %s is %d. "
             "The answer is <b>%s</b>." % (d, word, best, fr(best, d)))
        its.append(mcq_fr("Which is the %s: %s?" % (word, frs([(n, d) for n in ns])),
                          (best, d), [(n, d) for n in ns if n != best], e, rnd))
    # true statements
    for qn, (rows, e) in enumerate([
            ([((3, 8), "<", (5, 8)), ((5, 8), "<", (3, 8)), ((3, 8), ">", (7, 8)), ((1, 8), ">", (2, 8))],
             "Both are eighths. 3 eighths is less than 5 eighths, so <b>%s &lt; %s</b>." % (fr(3, 8), fr(5, 8))),
            ([((2, 6), ">", (4, 6)), ((6, 9), ">", (4, 9)), ((5, 7), "<", (2, 7)), ((3, 5), ">", (4, 5))],
             "Both are ninths. 6 ninths is more than 4 ninths, so <b>%s &gt; %s</b>." % (fr(6, 9), fr(4, 9))),
            ([((7, 10), "<", (3, 10)), ((4, 12), ">", (9, 12)), ((2, 3), "<", (1, 3)), ((5, 11), "<", (8, 11))],
             "Both are elevenths. 5 elevenths is less than 8 elevenths, so <b>%s &lt; %s</b>." % (fr(5, 11), fr(8, 11))),
            ([((4, 9), "=", (5, 9)), ((5, 6), ">", (1, 6)), ((2, 4), ">", (3, 4)), ((7, 12), "<", (5, 12))],
             "Both are sixths. 5 sixths is more than 1 sixth, so <b>%s &gt; %s</b>." % (fr(5, 6), fr(1, 6)))]):
        ch, right = [], None
        for a, sym, b in rows:
            fa, fb = Fraction(*a), Fraction(*b)
            ok = {"<": fa < fb, ">": fa > fb, "=": fa == fb}[sym]
            s = "%s %s %s" % (fr(*a), {"<": "&lt;", ">": "&gt;", "=": "="}[sym], fr(*b))
            if ok:
                assert right is None
                right = s
            else:
                ch.append(s)
        assert right is not None and len(ch) == 3
        its.append(mcq(["Look at the denominators. Which is true?", "Compare the numerators. Which is true?",
                        "Which of these is true?", "Only one of these is true. Which one?"][qn], right, ch, e, rnd))
    its.append(mcq_fr("Which fraction is <b>smaller</b> than %s?" % fr(3, 8), (2, 8), [(5, 8), (7, 8), (4, 8)],
                      "Eighths are all the same size. 2 eighths is less than 3 eighths, so <b>%s &lt; %s</b>."
                      % (fr(2, 8), fr(3, 8)), rnd))
    its.append(mcq_fr("Which fraction is <b>greater</b> than %s?" % fr(4, 9), (7, 9), [(2, 9), (3, 9), (1, 9)],
                      "Ninths are all the same size. 7 ninths is more than 4 ninths, so <b>%s &gt; %s</b>."
                      % (fr(7, 9), fr(4, 9)), rnd))
    for d, (a, sym), right, cands in [(7, (4, ">"), 5, [3, 4, 1]), (10, (3, "<"), 2, [3, 4, 7])]:
        if sym == ">":
            q = "Which number can go in the box?<br>%s &gt; %s" % (fr("☐", d), fr(a, d))
            assert right > a and all(c <= a for c in cands)
            e = ("The denominators are the same, so the numerator in the box must be <b>greater than %d</b>. "
                 "Only %d works: %s &gt; %s. (%s is not greater than %s, so %d does not work.)"
                 % (a, right, fr(right, d), fr(a, d), fr(a, d), fr(a, d), a))
        else:
            q = "Which number can go in the box?<br>%s &gt; %s" % (fr(a, d), fr("☐", d))
            assert right < a and all(c >= a for c in cands)
            e = ("The denominators are the same, so the numerator in the box must be <b>smaller than %d</b>. "
                 "Only %d works: %s &gt; %s." % (a, right, fr(a, d), fr(right, d)))
        its.append(mcq_n(q, right, cands, e, rnd))
    its.append(mcq_fr("Which fraction is equal to <b>1 whole</b>?", (6, 6), [(1, 6), (5, 6), (6, 7)],
                      "1 whole cut into 6 equal parts has 6 sixths. All 6 parts make the whole: <b>%s = 1</b>." % fr(6, 6), rnd))
    its.append(mcq("How do you compare %s and %s?" % (fr(4, 11), fr(7, 11)), "Compare the numerators",
                   ["Compare the denominators", "Count the parts not shaded", "Add the two numbers"],
                   "Both fractions are elevenths, so the parts are the same size. Compare the <b>numerators</b>: "
                   "7 &gt; 4, so %s &gt; %s." % (fr(7, 11), fr(4, 11)), rnd))
    assert len(its) == 20, len(its)
    return {"title": "Compare like fractions", "items": its}


# ============================================================ set 5: order fractions and word problems
def order_q(rnd, fs, up):
    srt = sorted(fs, key=lambda f: Fraction(*f), reverse=not up)
    r = frs(srt)
    sw1 = [srt[1], srt[0]] + srt[2:]
    sw2 = srt[:-2] + [srt[-1], srt[-2]]
    cands = [frs(list(reversed(srt))), frs(fs), frs(sw1), frs(sw2)]
    unit = all(n == 1 for n, _ in fs)
    if unit:
        e = ("All the numerators are 1. The bigger the denominator, the smaller the fraction. "
             "%s: <b>%s</b>." % ("Smallest to greatest" if up else "Greatest to smallest", r))
    else:
        e = ("The denominators are the same, so order the numerators: %s. "
             "%s: <b>%s</b>." % (", ".join(str(n) for n, _ in srt), "Smallest to greatest" if up else "Greatest to smallest", r))
    q = "Arrange %s in order, %s." % (frs(fs), "from the smallest to the greatest" if up else "from the greatest to the smallest")
    return mcq(q, r, cands, e, rnd)


def set_order(rnd):
    SPOTS.left = []
    its = []
    for fs, up in [([(1, 3), (1, 8), (1, 5)], True), ([(5, 9), (2, 9), (7, 9)], True),
                   ([(1, 6), (1, 2), (1, 10), (1, 4)], False), ([(4, 6), (1, 6), (5, 6)], False),
                   ([(1, 7), (1, 2), (1, 12), (1, 4)], True), ([(3, 12), (11, 12), (7, 12), (5, 12)], False)]:
        its.append(order_q(rnd, fs, up))

    # W1 cake eaten (model)
    q = (fig(units_svg(8, 3, "1 cake", "Wei Ming")) +
         "Mrs Lim cut a pandan cake into 8 equal pieces. Wei Ming ate 3 pieces. What fraction of the cake did he eat?")
    e = ("Draw the cake as <b>8 equal units</b>. Wei Ming ate <b>3 units</b>. So he ate %s of the cake." % fr(3, 8))
    its.append(mcq_fr(q, (3, 8), [(5, 8), (3, 5), (1, 3), (3, 9)], e, rnd))
    # W2 pizza left (model)
    q = (fig(units_svg(6, 4, "1 pizza", "eaten", rest="left ?")) +
         "A pizza was cut into 6 equal slices. Ali’s family ate 4 slices. What fraction of the pizza was <b>left</b>?")
    e = ("6 units − 4 units = <b>2 units</b> left. So %s of the pizza was left." % fr(2, 6))
    its.append(mcq_fr(q, (2, 6), [(4, 6), (2, 4), (4, 2), (1, 6)], e, rnd))
    # W3 water bottles (named bars)
    kids = [("Siti", 2), ("Raju", 4), ("Chloe", 1), ("Hafiz", 3)]
    q = (fig(bars_svg([(5, k, n) for n, k in kids], name="bar models", col=FILL3)) +
         "Siti, Raju, Chloe and Hafiz have water bottles of the same size. Siti drank %s of her water, Raju drank %s, "
         "Chloe drank %s and Hafiz drank %s. Who drank the most?" % (fr(2, 5), fr(4, 5), fr(1, 5), fr(3, 5)))
    e = ("All the bars have 5 equal units. Raju’s bar has the most units shaded: 4. %s is the greatest, so "
         "<b>Raju</b> drank the most." % fr(4, 5))
    its.append(mcq(q, "Raju", ["Siti", "Chloe", "Hafiz"], e, rnd))
    # W4 Sports Day
    e = ("All the distances are in tenths. Compare the numerators: 7, 3, 9 and 5. 3 is the smallest, so "
         "<b>Nurul</b> ran the shortest distance.")
    its.append(mcq("On Sports Day, Arjun ran %s km, Nurul ran %s km, Ethan ran %s km and Priya ran %s km. "
                   "Who ran the shortest distance?" % (fr(7, 10), fr(3, 10), fr(9, 10), fr(5, 10)),
                   "Nurul", ["Arjun", "Ethan", "Priya"], e, rnd))
    # W5 pizzas cut into different numbers of slices (named bars, unit fractions)
    kids = [("Ahmad", 6), ("Sarah", 3), ("Kumar", 8), ("Xin Yi", 4)]
    q = (fig(bars_svg([(d, 1, n) for n, d in kids], name="bar models", col=FILL3)) +
         "Four pizzas are the same size. Ahmad’s pizza is cut into 6 equal slices, Sarah’s into 3, Kumar’s into 8 "
         "and Xin Yi’s into 4. Each child eats 1 slice of their own pizza. Who eats the biggest slice?")
    e = ("Sarah’s pizza has the fewest slices, so each slice is the biggest. %s is the greatest of %s. "
         "<b>Sarah</b> eats the biggest slice." % (fr(1, 3), frs([(1, 6), (1, 3), (1, 8), (1, 4)])))
    its.append(mcq(q, "Sarah", ["Ahmad", "Kumar", "Xin Yi"], e, rnd))
    # W6 painted wall
    e = ("Both fractions are twelfths, so compare the numerators: 5 &lt; 7. %s &lt; %s, so <b>Hui Min</b> painted less."
         % (fr(5, 12), fr(7, 12)))
    its.append(mcq("Hui Min and Jun Jie are painting two walls of the same size. Hui Min has painted %s of her wall. "
                   "Jun Jie has painted %s of his wall. Who has painted less?" % (fr(5, 12), fr(7, 12)),
                   "Hui Min", ["Jun Jie", "They painted the same", "You cannot tell"], e, rnd))
    # W7 ribbon pieces
    e = ("The ribbon is cut into <b>5 equal pieces</b>. 1 piece is one fifth: %s. (She made 4 cuts, but there are 5 pieces.)"
         % fr(1, 5))
    its.append(mcq_fr("Mdm Wong cut a ribbon into 5 equal pieces. What fraction of the ribbon is 1 piece?",
                      (1, 5), [(1, 4), (4, 5), (1, 6)], e, rnd))
    # W8 storybook, unit fractions
    e = ("A whole cut into 5 parts has bigger parts than a whole cut into 10 parts. %s &gt; %s, so <b>Kumar</b> read more."
         % (fr(1, 5), fr(1, 10)))
    its.append(mcq("Zhi Hao read %s of a storybook. Kumar read %s of the same storybook. Who read more?"
                   % (fr(1, 10), fr(1, 5)),
                   "Kumar, as %s &gt; %s" % (fr(1, 5), fr(1, 10)),
                   ["Zhi Hao, as 10 &gt; 5", "They read the same", "Zhi Hao, as tenths are bigger"], e, rnd))
    # W9 watermelon
    e = ("There are <b>10 equal slices</b>. Ryan gave away <b>3</b> of them. So he gave away %s of the watermelon." % fr(3, 10))
    its.append(mcq_fr("Ryan cut a watermelon into 10 equal slices. He gave 3 slices to his friends. "
                      "What fraction of the watermelon did he give away?", (3, 10), [(7, 10), (3, 7), (1, 3), (10, 3)], e, rnd))
    # W10 ribbons, unit fractions
    e = ("All the numerators are 1. The biggest denominator gives the smallest part. %s is the smallest of %s, so the "
         "<b>yellow ribbon</b> is the shortest." % (fr(1, 8), frs([(1, 2), (1, 5), (1, 3), (1, 8)])))
    its.append(mcq("For Children’s Day, Mrs Ng has four ribbons. The red ribbon is %s m long, the blue ribbon is %s m long, "
                   "the green ribbon is %s m long and the yellow ribbon is %s m long. Which ribbon is the shortest?"
                   % (fr(1, 2), fr(1, 5), fr(1, 3), fr(1, 8)),
                   "The yellow ribbon", ["The red ribbon", "The blue ribbon", "The green ribbon"], e, rnd))
    # W11 paper strip, rest blue (model)
    q = (fig(units_svg(9, 4, "1 paper strip", "red", rest="blue ?")) +
         "Devi folded a paper strip into 9 equal parts. She coloured 4 parts red and the rest blue. "
         "What fraction of the strip is blue?")
    e = ("9 units − 4 units = <b>5 units</b> are blue. So %s of the strip is blue." % fr(5, 9))
    its.append(mcq_fr(q, (5, 9), [(4, 9), (5, 4), (4, 5), (1, 9)], e, rnd))
    # W12 garden plot (model)
    q = (fig(units_svg(12, 5, "1 garden plot", "kangkong", rest="chilli ?")) +
         "A community garden plot is cut into 12 equal parts. 5 parts are for kangkong and the rest are for chilli. "
         "What fraction of the plot is for chilli?")
    e = ("12 units − 5 units = <b>7 units</b> are for chilli. So %s of the plot is for chilli." % fr(7, 12))
    its.append(mcq_fr(q, (7, 12), [(5, 12), (7, 5), (5, 7), (6, 12)], e, rnd))
    # W13 chocolate bars, least
    e = ("All the numerators are 1. Ryan’s bar is cut into the most parts (12), so %s is the smallest. "
         "<b>Ryan</b> ate the least." % fr(1, 12))
    its.append(mcq("Farah, Arjun, Mei Ling and Ryan each have a bar of chocolate of the same size. Farah ate %s of her bar, "
                   "Arjun ate %s, Mei Ling ate %s and Ryan ate %s. Who ate the least?"
                   % (fr(1, 3), fr(1, 6), fr(1, 2), fr(1, 12)),
                   "Ryan", ["Farah", "Arjun", "Mei Ling"], e, rnd))
    # W14 kueh (model): pieces eaten altogether
    q = (fig(units_svg(6, 3, "1 tray of kueh", "Ali and sister ?")) +
         "Mr Rahman cut a tray of kueh into 6 equal pieces. Ali ate 1 piece and his sister ate 2 pieces. "
         "What fraction of the tray of kueh did they eat altogether?")
    e = ("1 unit + 2 units = <b>3 units</b> out of 6 equal units. So they ate %s of the tray." % fr(3, 6))
    its.append(mcq_fr(q, (3, 6), [(2, 6), (1, 6), (3, 3), (4, 6)], e, rnd))
    assert len(its) == 20, len(its)
    return {"title": "Order fractions and word problems", "items": its}


# ============================================================ lesson
def body_html():
    names_fig = svg_wrap(372, 140, "".join(
        [piece("square", 2, {0}, 10, 6, 100), piece("circle", 3, {0}, 136, 6, 100), piece("grid", 4, {0}, 262, 6, 100),
         txt(60, 132, "one half", 16), txt(186, 132, "one third", 16), txt(312, 132, "one quarter", 16)]),
        "one half of a square, one third of a circle and one quarter of a square shaded")
    noteq_fig = svg_wrap(250, 140, "".join(
        [piece("square", 2, {0}, 10, 6, 100), piece("square", 2, {0}, 140, 6, 100, [0.3, 0.7]),
         txt(60, 132, "halves", 16), txt(190, 132, "not halves", 16)]),
        "a square cut into 2 equal parts and a square cut into 2 unequal parts")
    f_shaded = shape_svg("bar", 8, set(range(3)))
    f_unit = bars_svg([(4, 1, (1, 4)), (8, 1, (1, 8))], W=300)
    f_like = bars_svg([(7, 3, (3, 7)), (7, 5, (5, 7))], W=300)
    f_model = units_svg(8, 3, "1 cake", "Wei Ming")
    return (
        "<h2>Equal parts</h2>"
        "<p>A fraction is a part of a whole. The parts must be <b>equal</b> (the same size).</p>"
        "<figure class='sn-fig'>" + names_fig +
        "<figcaption>2 equal parts are halves. 3 equal parts are thirds. 4 equal parts are quarters.</figcaption></figure>"
        "<figure class='sn-fig'>" + noteq_fig +
        "<figcaption>Both squares have 2 parts. Only the first one shows halves.</figcaption></figure>"
        "<h2>Name the fraction</h2>"
        "<p>Count all the equal parts. That is the bottom number, the <b>denominator</b>. "
        "Count the shaded parts. That is the top number, the <b>numerator</b>.</p>"
        "<figure class='sn-fig'>" + f_shaded +
        "<figcaption>8 equal parts, 3 shaded: " + fr(3, 8) + " (three eighths) is shaded.</figcaption></figure>"
        + table(["Equal parts", "Each part is", "We write"], [
            ["2", "one half", fr(1, 2)],
            ["4", "one quarter", fr(1, 4)],
            ["5", "one fifth", fr(1, 5)],
            ["10", "one tenth", fr(1, 10)],
        ]) +
        "<h2>Unit fractions: more parts, smaller parts</h2>"
        "<p>A unit fraction has 1 on top, like " + fr(1, 4) + " or " + fr(1, 8) + ". "
        "When the same whole is cut into <b>more</b> parts, each part is <b>smaller</b>.</p>"
        "<figure class='sn-fig'>" + f_unit +
        "<figcaption>" + fr(1, 4) + " &gt; " + fr(1, 8) + ", even though 8 is bigger than 4.</figcaption></figure>"
        + ex("Example", "Which is greater, " + fr(1, 3) + " or " + fr(1, 9) + "?",
             "Thirds are bigger parts than ninths.", fr(1, 3)) +
        "<h2>Compare and order like fractions</h2>"
        "<p>Like fractions have the same denominator, so the parts are the same size. Compare the numerators.</p>"
        "<figure class='sn-fig'>" + f_like +
        "<figcaption>5 sevenths is more than 3 sevenths: " + fr(5, 7) + " &gt; " + fr(3, 7) + ".</figcaption></figure>"
        + ex("Example", "Arrange " + frs([(5, 9), (2, 9), (7, 9)]) + " from the smallest to the greatest.",
             "The denominators are the same. Order the numerators: 2, 5, 7.", frs([(2, 9), (5, 9), (7, 9)]))
        + ex("Example", "Arrange " + frs([(1, 3), (1, 8), (1, 5)]) + " from the smallest to the greatest.",
             "The numerators are all 1. The biggest denominator is the smallest fraction.", frs([(1, 8), (1, 5), (1, 3)])) +
        "<h2>Word problems: draw a model</h2>"
        "<p>Draw a bar for the whole. Cut it into equal units. The number of units is the denominator.</p>"
        "<figure class='sn-fig'>" + f_model +
        "<figcaption>A cake is cut into 8 equal pieces. Wei Ming ate 3 pieces.</figcaption></figure>"
        + ex("Example", "Mrs Lim cut a cake into 8 equal pieces. Wei Ming ate 3 pieces. What fraction of the cake did he eat?",
             "The cake is 8 units. He ate 3 units.", fr(3, 8)) +
        "<h2>Common mistakes</h2>" +
        table(["Mistake", "What to do instead"], [
            ["Calling 2 unequal parts “halves”", "Check that the parts are the <b>same size</b>"],
            [fr(1, 8) + " &gt; " + fr(1, 4) + " (because 8 &gt; 4)",
             "More parts means smaller parts: " + fr(1, 8) + " &lt; " + fr(1, 4)],
            ["3 of 8 parts shaded, writing " + fr(5, 8), "The top number counts the <b>shaded</b> parts: " + fr(3, 8)],
            ["3 of 8 parts shaded, writing " + fr(3, 5), "The bottom number counts <b>all</b> the parts: " + fr(3, 8)],
            ["Counting the lines, not the parts", "A strip with 4 cuts has <b>5</b> parts"],
        ])
    )


FAQ = [
    {"q": "What is taught in P2 fractions?",
     "a": "In Primary 2, students learn that a fraction is a part of a whole cut into equal parts, and how to write it with a numerator and denominator. They compare and order unit fractions and like fractions with denominators up to 12."},
    {"q": "How do I explain fractions to my child?",
     "a": "Fold a paper strip into equal parts and colour some of them. Count all the parts for the bottom number and the coloured parts for the top number: 3 coloured parts out of 8 is 3/8."},
    {"q": "Why is 1/8 smaller than 1/4?",
     "a": "When the same whole is cut into 8 equal parts instead of 4, each part is smaller. So 1/8 < 1/4, even though 8 is bigger than 4. This is the most common P2 fraction mistake."},
    {"q": "Is fractions in the MOE syllabus for Primary 2?",
     "a": "Yes. Fraction as part of a whole, fraction notation, and comparing and ordering unit and like fractions are part of the Primary 2 Standard Mathematics syllabus (MOE 2021). In Primary 3, students go on to equivalent fractions."},
]


def gen_unit():
    rnd = random.Random(62806)
    sets = [set_equal(rnd), set_name(rnd), set_unit(rnd), set_like(rnd), set_order(rnd)]
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
        "country": "sg", "subject": "maths", "grade": "primary-2", "slug": "fractions", "sort": 6,
        "updated": UPDATED, "pdf_url": "",
        "title": "Primary 2 Fractions",
        "seo_title": "P2 Fractions Worksheets: Free Primary 2 Maths with Answers (MOE Syllabus)",
        "short_title": "Fractions",
        "domain": "Number and Algebra",
        "standard_code": "Primary 2: Fractions",
        "standard_url": "https://www.moe.gov.sg/primary/curriculum/syllabus",
        "standard_text": "Fraction as part of a whole; notation; comparing and ordering unit fractions and like fractions (denominators not exceeding 12)",
        "meta_desc": "Free P2 maths practice: equal parts, naming the fraction shaded, unit fractions, and comparing and ordering fractions. 100 questions with answers.",
        "key_big": "A fraction needs equal parts: the bottom number counts all the parts, the top number counts the parts you take.",
        "key_sub": "3 of 8 equal parts shaded = 3/8. More parts means smaller parts, so 1/8 < 1/4.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }


if __name__ == "__main__":
    u = gen_unit()
    mark_large(u, "(bars of|bar of|bar model|four pictures)")
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(u, f, ensure_ascii=False, indent=1)
    print("wrote", path)
