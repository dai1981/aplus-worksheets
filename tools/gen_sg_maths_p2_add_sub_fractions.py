# -*- coding: utf-8 -*-
"""
Singapore Primary 2 Maths: Adding and Subtracting Fractions
(MOE 2021 Primary Mathematics Syllabus, Standard. Primary 2: Fractions)
  python3 tools/gen_sg_maths_p2_add_sub_fractions.py
Like fractions within one whole (denominators up to 12): adding with fraction bars, subtracting,
making 1 whole, mixed practice and word problems with bar models.
Every answer is already in its simplest form, or is 1 whole (no simplifying in P2).
Wrong choices come from real mistakes (adding the denominators, writing the part taken away, miscounting)
and are never equal in value to the answer or to each other. Every answer is checked with fractions.Fraction.
HTML attributes use single quotes (no backslashes in the JSON). Singapore English, short sentences.
"""
import json, math, os, random, re
from fractions import Fraction

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "sg", "maths", "primary-2")
UPDATED = "2026-11-03"
FILL = "#4fae74"      # first fraction
FILL2 = "#f2b84b"     # second fraction
FILL3 = "#8fb8e8"     # bar models
WATER = "#8fc6ee"
CAKE = "#f3d9b1"
RED = "#c0392b"
LINE = "#2b2b2b"
WORD = {2: "halves", 3: "thirds", 4: "quarters", 5: "fifths", 6: "sixths", 7: "sevenths", 8: "eighths", 9: "ninths",
        10: "tenths", 11: "elevenths", 12: "twelfths"}
ONE = {2: "half", 3: "third", 4: "quarter", 5: "fifth", 6: "sixth", 7: "seventh", 8: "eighth", 9: "ninth",
       10: "tenth", 11: "eleventh", 12: "twelfth"}
USED = set()   # (op, n1, n2, d) of every sum or difference asked, so none is asked twice


def fr(a, b):
    return "<span class='fr'><span class='fn'>%s</span><span class='fd'>%s</span></span>" % (a, b)


def show(t):
    """(n, d) as written by a P2 student: n/d, or 1 when n = d."""
    n, d = t
    return "1" if n == d else fr(n, d)


def parts(n, d):
    """'3 eighths', '1 eighth'."""
    return "%d %s" % (n, ONE[d] if n == 1 else WORD[d])


def note(op, n1, n2, d):
    k = (op, n1, n2, d)
    assert k not in USED, k
    USED.add(k)


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
    """correct and cands are (n, d) tuples or strings. A tuple that is 0 or less, more than 1, or equal in value
    to the answer or to another choice is skipped."""
    def norm(c):
        if isinstance(c, tuple):
            return Fraction(*c), show(c)
        return None, c
    cv, cs = norm(correct)
    if cv is not None:
        assert 0 < cv <= 1 and (cv == 1 or math.gcd(*correct) == 1), correct
    seen, vals, pick = {cs}, {cv} if cv is not None else set(), []
    for c in cands:
        if c is None:
            continue
        v, s = norm(c)
        if v is not None and (v <= 0 or v > 1 or v in vals):
            continue
        if s in seen:
            continue
        if v is not None:
            vals.add(v)
        seen.add(s)
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


def lab_w(lab, size=15):
    if isinstance(lab, str):
        return (size + 2) * 0.6 * len(lab)
    n, d = lab
    return size * 0.62 * max(len(str(n)), len(str(d))) + 4


def lab_svg(cx, yc, lab, size=15):
    """Fraction (n, d) or a string such as '?' centred at cx; yc is the middle line."""
    if isinstance(lab, str):
        return txt(cx, yc + size * 0.36, lab, size + 2)
    n, d = lab
    return sfr(cx, yc - 5, n, d, size)


def brace(x0, x1, y, up=True):
    """Curly brace from x0 to x1 at height y. up=True: the point is above."""
    m = (x0 + x1) / 2
    k = -8 if up else 8
    return ("<path d='M%.1f %.1f Q%.1f %.1f %.1f %.1f L%.1f %.1f Q%.1f %.1f %.1f %.1f "
            "Q%.1f %.1f %.1f %.1f L%.1f %.1f Q%.1f %.1f %.1f %.1f' fill='none' stroke='%s' stroke-width='1.8'/>"
            % (x0, y, x0, y + k, x0 + 8, y + k, m - 6, y + k, m, y + k, m, y + 2 * k,
               m, y + k, m + 6, y + k, x1 - 8, y + k, x1, y + k, x1, y, LINE))


def cross(cx, cy, r):
    return ("<path d='M%.1f %.1f L%.1f %.1f M%.1f %.1f L%.1f %.1f' stroke='%s' stroke-width='3' stroke-linecap='round'/>"
            % (cx - r, cy - r, cx + r, cy + r, cx - r, cy + r, cx + r, cy - r, RED))


# ------------------------------------------------------------ pictures
def one_bar_svg(L, k1, k2=0, crossed=0, W=264, Hh=40):
    """One bar of L equal parts: k1 green then k2 yellow. crossed = how many of the last green parts get a red X."""
    s = []
    for i in range(L):
        col = FILL if i < k1 else (FILL2 if i < k1 + k2 else "#fff")
        x = 6 + i * W / L
        s.append("<rect x='%.2f' y='6' width='%.2f' height='%d' fill='%s' stroke='%s' stroke-width='2.2'/>" % (x, W / L, Hh, col, LINE))
        if k1 - crossed <= i < k1:
            c = W / L
            r = min(c, Hh) / 2 - min(c, Hh) * 0.2
            s.append(cross(x + c / 2, 6 + Hh / 2, r))
    s.append("<rect x='6' y='6' width='%d' height='%d' fill='none' stroke='%s' stroke-width='3'/>" % (W, Hh, LINE))
    if crossed:
        lab = "bar of %d equal parts: %d shaded and the last %d of them crossed out" % (L, k1, crossed)
    else:
        lab = "bar of %d equal parts: %d green and %d yellow" % (L, k1, k2)
    return svg_wrap(W + 12, Hh + 12, "".join(s), lab)


def pie_body(cx, cy, R, d, k1, k2=0, crossed=0, base="#fff"):
    """A circle cut into d equal slices from 12 o'clock, clockwise. First k1 slices green, next k2 yellow,
    the rest in base colour. The first `crossed` slices get a red X."""
    s = []
    for i in range(d):
        col = FILL if i < k1 else (FILL2 if i < k1 + k2 else base)
        a0 = -math.pi / 2 + 2 * math.pi * i / d
        a1 = a0 + 2 * math.pi / d
        s.append("<path d='M%.1f %.1f L%.2f %.2f A%.1f %.1f 0 0 1 %.2f %.2f Z' fill='%s' stroke='%s' stroke-width='2.2'/>"
                 % (cx, cy, cx + R * math.cos(a0), cy + R * math.sin(a0), R, R,
                    cx + R * math.cos(a1), cy + R * math.sin(a1), col, LINE))
    s.append("<circle cx='%.1f' cy='%.1f' r='%.1f' fill='none' stroke='%s' stroke-width='3'/>" % (cx, cy, R, LINE))
    for i in range(crossed):
        am = -math.pi / 2 + 2 * math.pi * (i + 0.5) / d
        s.append(cross(cx + 0.6 * R * math.cos(am), cy + 0.6 * R * math.sin(am), min(9, 0.6 * R * math.pi / d * 0.75)))
    return "".join(s)


def pie_svg(d, k1=0, k2=0, crossed=0, base="#fff", R=46, label="circle"):
    lab = "%s cut into %d equal slices, %d green, %d yellow, %d crossed out" % (label, d, k1, k2, crossed)
    return svg_wrap(12 + 2 * R, 12 + 2 * R, pie_body(6 + R, 6 + R, R, d, k1, k2, crossed, base), lab)


def bottle_svg(d, k, crossed=0, k2=0):
    """A bottle cut into d equal bands. The bottom k bands hold water; the top `crossed` of them get a red X.
    k2 more bands above the water are yellow (water added)."""
    bw, bh = 64, 120
    x0, y0 = 6, 34
    s = ["<rect x='%d' y='6' width='24' height='16' rx='2' fill='#fff' stroke='%s' stroke-width='2.2'/>" % (x0 + bw / 2 - 12, LINE),
         "<path d='M%d %d L%d %d L%d %d L%d %d' fill='none' stroke='%s' stroke-width='2.2'/>"
         % (x0 + bw / 2 - 12, 22, x0 + bw / 2 - 12, 26, x0 + bw / 2 + 12, 26, x0 + bw / 2 + 12, 22, LINE),
         "<path d='M%d %d L%d %d L%d %d L%d %d' fill='none' stroke='%s' stroke-width='2.2'/>"
         % (x0 + bw / 2 - 12, 26, x0, y0, x0 + bw, y0, x0 + bw / 2 + 12, 26, LINE)]
    h = bh / d
    for i in range(d):
        y = y0 + bh - (i + 1) * h
        col = WATER if i < k else (FILL2 if i < k + k2 else "#fff")
        s.append("<rect x='%d' y='%.2f' width='%d' height='%.2f' fill='%s' stroke='%s' stroke-width='1.6'/>"
                 % (x0, y, bw, h, col, LINE))
        if k - crossed <= i < k:
            s.append(cross(x0 + bw / 2, y + h / 2, min(9, h / 2 - 2)))
    s.append("<rect x='%d' y='%d' width='%d' height='%d' fill='none' stroke='%s' stroke-width='3'/>" % (x0, y0, bw, bh, LINE))
    lab = "bottle marked in %d equal parts: water in %d parts, %d of them crossed out, %d parts added" % (d, k, crossed, k2)
    return svg_wrap(x0 + bw + 6, y0 + bh + 6, "".join(s), lab)


def model_svg(segs, total, units=None, W=300):
    """Part-whole bar model. segs: list of (value, label) where label is (n, d) or '?'.
    total: label for the whole bar, (n, d) or a string, shown with a brace above.
    Each segment is drawn as its units (thin lines), so 3/8 shows 3 small boxes."""
    tv = sum(v for v, _ in segs)
    x0 = 6
    s = []
    yb = 58
    Hh = 36
    s.append(lab_svg(x0 + W / 2, 16, total))
    s.append(brace(x0, x0 + W, 50, up=True))
    x = x0
    cols = [FILL3, "#ffffff", "#d7e6f7"]
    for i, (v, lab) in enumerate(segs):
        w = W * v / tv
        s.append("<rect x='%.2f' y='%d' width='%.2f' height='%d' fill='%s' stroke='%s' stroke-width='2.4'/>"
                 % (x, yb, w, Hh, cols[i % 3], LINE))
        n = int(v * units) if units else None
        if n and n > 1:
            for j in range(1, n):
                xx = x + w * j / n
                s.append("<line x1='%.2f' y1='%d' x2='%.2f' y2='%d' stroke='%s' stroke-width='1.2'/>" % (xx, yb, xx, yb + Hh, LINE))
        s.append(brace(x + 2, x + w - 2, yb + Hh + 6, up=False))
        s.append(lab_svg(x + w / 2, yb + Hh + 38, lab))
        assert lab_w(lab) < w + 6, (lab, w)
        x += w
    lab = "bar model: a whole bar split into %d parts" % len(segs)
    return svg_wrap(x0 + W + 8, yb + Hh + 62, "".join(s), lab)


def compare_svg(rows, diff, W=230):
    """Comparison bar model. rows: [(name, value, label)] (two rows, the first is longer). The longer bar has its
    extra part marked with a dashed line and diff ('?') inside it. Each known value is written to the right of its bar."""
    (n1, v1, l1), (n2, v2, l2) = rows
    assert v1 > v2
    x0 = 14 + 8.6 * max(len(n1), len(n2))
    Hh = 40
    s = []
    right = x0 + W
    for j, (nm, v, lab) in enumerate(rows):
        y = 8 + j * (Hh + 16)
        w = W * v / v1
        s.append(txt(6, y + Hh / 2 + 5, nm, 15, anchor="start"))
        s.append("<rect x='%.2f' y='%d' width='%.2f' height='%d' fill='%s' stroke='%s' stroke-width='2.2'/>"
                 % (x0, y, w, Hh, FILL3 if j == 0 else FILL2, LINE))
        if j == 0:
            ws = W * v2 / v1
            s.append("<line x1='%.2f' y1='%d' x2='%.2f' y2='%d' stroke='%s' stroke-width='2' stroke-dasharray='5 4'/>"
                     % (x0 + ws, y, x0 + ws, y + Hh, LINE))
            assert lab_w(diff) < W - ws - 4, (diff, W - ws)
            s.append(lab_svg(x0 + (ws + W) / 2, y + Hh / 2, diff))
        s.append(lab_svg(x0 + w + 8 + lab_w(lab) / 2, y + Hh / 2, lab))
        right = max(right, x0 + w + 12 + lab_w(lab))
    return svg_wrap(right + 6, 8 + 2 * Hh + 16 + 8, "".join(s), "bar model comparing two bars")


# ------------------------------------------------------------ explanations and mistakes
def e_add(n1, n2, d):
    N = n1 + n2
    t = "The parts are %s, so the denominator stays %d. Add the numerators: %d + %d = %d. " % (WORD[d], d, n1, n2, N)
    if N == d:
        return t + "%s is all the parts, so %s = 1 whole. The answer is <b>1</b>." % (fr(d, d), fr(d, d))
    return t + "The answer is <b>%s</b>." % fr(N, d)


def e_sub(n1, n2, d):
    N = n1 - n2
    return ("The parts are %s, so the denominator stays %d. Subtract the numerators: %d − %d = %d. "
            "The answer is <b>%s</b>." % (WORD[d], d, n1, n2, N, fr(N, d)))


def e_one(n, d):
    """Explanation for n/d + ? = 1 (or 1 − n/d)."""
    return ("1 whole is %s. %d − %d = %d, so %s + %s = %s = 1. The answer is <b>%s</b>."
            % (fr(d, d), d, n, d - n, fr(n, d), fr(d - n, d), fr(d, d), fr(d - n, d)))


def wrong_add(n1, n2, d, rnd):
    """Adding the denominators first, then two more real mistakes."""
    N = n1 + n2
    rest = [(N - 1, d), (N + 1, d), (abs(n1 - n2), d) if n1 != n2 else None, (max(n1, n2), d), (min(n1, n2), d)]
    rnd.shuffle(rest)
    return [(N, 2 * d)] + rest


def wrong_sub(n1, n2, d, rnd):
    """Writing the part taken away, adding instead, miscounting, forgetting to subtract."""
    N = n1 - n2
    rest = [(n1 + n2, d), (N + 1, d), (N - 1, d) if N > 1 else None, (n1, d), (N, 2 * d)]
    rnd.shuffle(rest)
    return [(n2, d) if n2 != N else None] + rest


def wrong_one(n, d, rnd):
    """For n/d + ? = 1: copying the fraction, taking 1 from the numerator (1 − 3/8 = 2/8), miscounting."""
    rest = [(d - n + 1, d) if d - n + 1 < d else None, (d - n - 1, d) if d - n > 1 else None, (n - 1, d) if n > 1 else None]
    rnd.shuffle(rest)
    return [(n, d)] + rest + [(d - n - 2, d) if d - n > 2 else None, (d - n + 2, d) if d - n + 2 < d else None]


def add_q(n1, n2, d, rnd, pre="", figure="", post=" = ?"):
    note("+", n1, n2, d)
    N = n1 + n2
    assert 0 < n1 < d and 0 < n2 < d and N <= d and (N == d or math.gcd(N, d) == 1), (n1, n2, d)
    q = figure + pre + "%s + %s%s" % (fr(n1, d), fr(n2, d), post)
    return mcq(q, (N, d), wrong_add(n1, n2, d, rnd), e_add(n1, n2, d), rnd)


def sub_q(n1, n2, d, rnd, pre="", figure="", post=" = ?"):
    note("-", n1, n2, d)
    N = n1 - n2
    assert 0 < n2 < n1 <= d and math.gcd(N, d) == 1, (n1, n2, d)
    q = figure + pre + "%s − %s%s" % (show((n1, d)), fr(n2, d), post)
    e = e_sub(n1, n2, d) if n1 < d else ("Write 1 whole as %s. " % fr(d, d) + e_sub(n1, n2, d))
    return mcq(q, (N, d), wrong_sub(n1, n2, d, rnd), e, rnd)


def one_q(n, d, rnd, q, pre=""):
    note("1", n, 0, d)
    assert 0 < n < d and math.gcd(d - n, d) == 1, (n, d)
    return mcq(q, (d - n, d), wrong_one(n, d, rnd), pre + e_one(n, d), rnd)


# ============================================================ set 1: adding with fraction bars
def set_add(rnd):
    SPOTS.left = []
    its = []
    # A: bars, count the parts
    for d, a, b in [(5, 1, 2), (7, 2, 3), (8, 3, 2), (9, 4, 3), (6, 1, 4), (10, 3, 4), (12, 5, 2)]:
        its.append(add_q(a, b, d, rnd, figure=fig(one_bar_svg(d, a, b)),
                         pre="The bar has %d equal parts. Green shows %s. Yellow shows %s. " % (d, fr(a, d), fr(b, d))))
    # B: circles
    for d, a, b in [(4, 1, 2), (8, 1, 6), (11, 4, 5)]:
        its.append(add_q(a, b, d, rnd, figure=fig(pie_svg(d, a, b)),
                         pre="The circle has %d equal parts. " % d))
    # C: in words
    e = "3 sevenths and 1 more seventh make 4 sevenths. The parts stay sevenths. The answer is <b>4 sevenths</b>."
    note("+", 3, 1, 7)
    its.append(mcq("3 sevenths + 1 seventh = ?", "4 sevenths", ["4 fourteenths", "3 sevenths", "2 sevenths"], e, rnd))
    e = "2 fifths and 2 more fifths make 4 fifths. The parts stay fifths. The answer is <b>4 fifths</b>."
    note("+", 2, 2, 5)
    its.append(mcq("2 fifths + 2 fifths = ?", "4 fifths", ["4 tenths", "5 fifths", "3 fifths"], e, rnd))
    # D: no picture
    for d, a, b in [(9, 1, 7), (11, 3, 5), (12, 1, 6), (10, 2, 5), (12, 5, 6)]:
        its.append(add_q(a, b, d, rnd))
    # E: missing part
    note("+?", 2, 0, 9)
    e = "%s + ? = %s. 2 ninths and how many more make 7 ninths? 7 − 2 = 5. The answer is <b>%s</b>." % (fr(2, 9), fr(7, 9), fr(5, 9))
    its.append(mcq("%s + <b>?</b> = %s" % (fr(2, 9), fr(7, 9)), (5, 9), [(7, 9), (9, 9), (5, 18), (4, 9)], e, rnd))
    # F: spot the mistake
    e = ("The parts are fifths. 1 fifth + 3 fifths = 4 fifths, so the answer is %s. "
         "Farah added the denominators too, so she got tenths. Her mistake: <b>she added the denominators</b>." % fr(4, 5))
    its.append(mcq("Farah wrote %s + %s = %s. What mistake did she make?" % (fr(1, 5), fr(3, 5), fr(4, 10)),
                   "She added the denominators",
                   ["She added the numerators", "She took away instead", "There is no mistake"], e, rnd))
    # G: which picture
    note("+pic", 2, 3, 6)
    its.append(letter_q(rnd, 6, 5, [3, 4, 2], "Which bar shows %s + %s?" % (fr(2, 6), fr(3, 6)),
                        "2 sixths + 3 sixths = 5 sixths."))
    assert len(its) == 20, len(its)
    return {"title": "Adding like fractions with fraction bars", "items": its}


def letter_q(rnd, d, k, others, q, why):
    """Choices A-D in that order: the bar with k of d parts shaded goes where SPOTS says."""
    pos = SPOTS.next(rnd)
    ks = others[:pos] + [k] + others[pos:]
    assert len(set(ks)) == 4
    L = "ABCD"[pos]
    e = "Count the shaded parts of each bar. %s Bar %s has %d of %d parts shaded. The answer is <b>%s</b>." % (why, L, k, d, L)
    return {"q": fig(abcd_bars(d, ks)) + q, "c": list("ABCD"), "a": pos, "e": e}


def abcd_bars(d, ks, W=200, Hh=30):
    """Four bars A-D of d parts each with ks[i] parts shaded, in one picture."""
    s = []
    for i, k in enumerate(ks):
        y = 6 + i * (Hh + 12)
        s.append(txt(14, y + Hh / 2 + 6, "ABCD"[i], 16))
        for j in range(d):
            s.append("<rect x='%.2f' y='%d' width='%.2f' height='%d' fill='%s' stroke='%s' stroke-width='2'/>"
                     % (32 + j * W / d, y, W / d, Hh, FILL if j < k else "#fff", LINE))
        s.append("<rect x='32' y='%d' width='%d' height='%d' fill='none' stroke='%s' stroke-width='2.6'/>" % (y, W, Hh, LINE))
    return svg_wrap(32 + W + 6, 6 + 4 * (Hh + 12) - 6, "".join(s), "bars A to D each cut into %d equal parts" % d)


# ============================================================ set 2: subtracting
def set_sub(rnd):
    SPOTS.left = []
    its = []
    # A: bars with crosses
    for d, a, b in [(5, 4, 1), (7, 6, 2), (8, 7, 4), (9, 8, 3), (6, 5, 4), (10, 9, 2)]:
        its.append(sub_q(a, b, d, rnd, figure=fig(one_bar_svg(d, a, 0, crossed=b)),
                         pre="The green parts show %s. Then %s is crossed out. " % (fr(a, d), fr(b, d))))
    # B: circles with crosses
    for d, a, b in [(4, 3, 2), (11, 9, 4), (12, 10, 3)]:
        its.append(sub_q(a, b, d, rnd, figure=fig(pie_svg(d, a, 0, crossed=b)),
                         pre="The circle has %d equal parts. %d are green. %d green parts are crossed out. " % (d, a, b)))
    # C: in words
    note("-", 6, 1, 9)
    e = "6 ninths take away 1 ninth leaves 5 ninths. The parts stay ninths. The answer is <b>5 ninths</b>."
    its.append(mcq("6 ninths − 1 ninth = ?", "5 ninths", ["5 eighths", "1 ninth", "7 ninths"], e, rnd))
    # D: no picture
    for d, a, b in [(7, 5, 3), (8, 6, 1), (11, 10, 3), (12, 11, 4), (10, 8, 1), (5, 3, 1)]:
        its.append(sub_q(a, b, d, rnd))
    # E: missing number
    note("?-", 0, 2, 7)
    e = ("? − %s = %s. Work backwards and add: %s + %s = %s. Check: 5 sevenths − 2 sevenths = 3 sevenths. "
         "The answer is <b>%s</b>." % (fr(2, 7), fr(3, 7), fr(3, 7), fr(2, 7), fr(5, 7), fr(5, 7)))
    its.append(mcq("<b>?</b> − %s = %s" % (fr(2, 7), fr(3, 7)), (5, 7), [(1, 7), (5, 14), (6, 7), (4, 7)], e, rnd))
    # F: spot the mistake
    e = ("The parts are eighths, so the denominator stays 8. 5 eighths − 2 eighths = 3 eighths = %s. "
         "Ryan took away the denominators too, so he got 0 at the bottom. His mistake: <b>he subtracted the denominators</b>." % fr(3, 8))
    its.append(mcq("Ryan wrote %s − %s = %s. What mistake did he make?" % (fr(5, 8), fr(2, 8), fr(3, 0)),
                   "He subtracted the denominators",
                   ["He added the numerators", "He forgot to take away", "There is no mistake"], e, rnd))
    # G: from 1 whole
    its.append(sub_q(5, 2, 5, rnd))
    # H: which picture
    note("-pic", 5, 3, 6)
    its.append(letter_q(rnd, 6, 2, [3, 1, 4], "Which bar shows %s − %s?" % (fr(5, 6), fr(3, 6)),
                        "5 sixths − 3 sixths = 2 sixths."))
    assert len(its) == 20, len(its)
    return {"title": "Subtracting like fractions", "items": its}


# ============================================================ set 3: making 1 whole
def set_whole(rnd):
    SPOTS.left = []
    its = []
    # A: bar, count the empty parts
    for d, n in [(8, 3), (5, 2), (9, 4), (7, 6)]:
        its.append(one_q(n, d, rnd, fig(one_bar_svg(d, n, 0)) +
                         "%s of the bar is green. How much more must be green to make 1 whole bar?" % fr(n, d),
                         pre="Count the white parts: %d. " % (d - n)))
    # B: circles
    for d, n in [(6, 1), (10, 3)]:
        its.append(one_q(n, d, rnd, fig(pie_svg(d, n, 0)) + "%s + <b>?</b> = 1" % fr(n, d),
                         pre="The circle has %d parts. %d %s green, so %d are white. " % (d, n, "is" if n == 1 else "are", d - n)))
    # C: 1 = ?/d
    for d in (4, 9):
        e = "1 whole cut into %s has %d %s. So 1 = %s. The answer is <b>%d</b>." % (WORD[d], d, WORD[d], fr(d, d), d)
        its.append(mcq("1 = %s. What is the missing number?" % fr("<b>?</b>", d), str(d), ["1", str(d - 1), str(d + 1)], e, rnd))
    # D: number bonds to 1, no picture
    for d, n in [(8, 5), (11, 4), (12, 7), (7, 2), (9, 8)]:
        its.append(one_q(n, d, rnd, "%s + <b>?</b> = 1" % fr(n, d)))
    for d, n in [(10, 7), (5, 1)]:
        its.append(one_q(n, d, rnd, "<b>?</b> + %s = 1" % fr(n, d)))
    # E: 1 − a fraction
    for d, n in [(6, 5), (12, 1)]:
        note("1-", n, 0, d)
        e = "Write 1 whole as %s. %s − %s = <b>%s</b>." % (fr(d, d), fr(d, d), fr(n, d), fr(d - n, d))
        its.append(mcq("1 − %s = ?" % fr(n, d), (d - n, d), wrong_one(n, d, rnd), e, rnd))
    # F: which two make 1
    e = ("Two fractions make 1 when the numerators add up to the denominator. 3 + 4 = 7, so %s + %s = %s = 1. "
         "The answer is <b>%s and %s</b>." % (fr(3, 7), fr(4, 7), fr(7, 7), fr(3, 7), fr(4, 7)))
    its.append(mcq("Which two fractions make 1 whole?", "%s and %s" % (fr(3, 7), fr(4, 7)),
                   ["%s and %s" % (fr(3, 7), fr(3, 7)), "%s and %s" % (fr(2, 7), fr(4, 7)), "%s and %s" % (fr(1, 7), fr(7, 7))],
                   e, rnd))
    # G: bottle
    note("1", 3, 0, 7)
    e = ("The bottle has 7 equal parts. 3 parts have water. 4 parts are empty. %s + %s = 1. "
         "The answer is <b>4 sevenths</b>." % (fr(3, 7), fr(4, 7)))
    its.append(mcq(fig(bottle_svg(7, 3)) + "How much more water is needed to fill the bottle?",
                   "4 sevenths", ["3 sevenths", "5 sevenths", "4 fourteenths"], e, rnd))
    # H: Kumar's mistake
    e = ("1 whole is %s, not 1 part. %s − %s = %s. Kumar took 1 from the numerator 3. "
         "The answer is <b>%s</b>." % (fr(8, 8), fr(8, 8), fr(3, 8), fr(5, 8), fr(5, 8)))
    its.append(mcq("Kumar wrote 1 − %s = %s. What is the correct answer?" % (fr(3, 8), fr(2, 8)), (5, 8),
                   [(2, 8), (3, 8), (4, 8)], e, rnd))
    assert len(its) == 20, len(its)
    return {"title": "Making 1 whole", "items": its}


# ============================================================ set 4: mixed practice within 1 whole
def set_mixed(rnd):
    SPOTS.left = []
    its = []
    # A: 4/4 = 1
    e = "%s means 4 quarters out of 4 quarters. That is all of it, so %s = <b>1</b>." % (fr(4, 4), fr(4, 4))
    its.append(mcq("%s = ?" % fr(4, 4), "1", [fr(1, 4), fr(4, 8), "4"], e, rnd))
    e = ("A fraction is 1 whole when the numerator and denominator are the same. %s = 1. "
         "The answer is <b>%s</b>." % (fr(9, 9), fr(9, 9)))
    its.append(mcq("Which fraction is equal to 1?", fr(9, 9), [fr(1, 9), fr(8, 9), fr(9, 10)], e, rnd))
    # B: sums equal to 1
    for d, a, b in [(4, 1, 3), (8, 3, 5), (10, 4, 6), (6, 2, 4)]:
        its.append(add_q(a, b, d, rnd))
    its.append(add_q(1, 2, 3, rnd, figure=fig(pie_svg(3, 1, 2)), pre="The circle has 3 equal parts. "))
    # C: three fractions
    for d, a, b, c in [(9, 1, 2, 4), (11, 2, 3, 1), (12, 3, 2, 2)]:
        N = a + b + c
        assert N < d and math.gcd(N, d) == 1
        e = ("The parts are %s, so the denominator stays %d. Add the numerators: %d + %d + %d = %d. "
             "The answer is <b>%s</b>." % (WORD[d], d, a, b, c, N, fr(N, d)))
        rest = [(N - 1, d), (N + 1, d), (a + b, d)]
        rnd.shuffle(rest)
        its.append(mcq("%s + %s + %s = ?" % (fr(a, d), fr(b, d), fr(c, d)), (N, d), [(N, 3 * d)] + rest, e, rnd))
    # D: add then take away
    for d, a, b, c in [(7, 2, 4, 3), (10, 6, 3, 2)]:
        N = a + b - c
        assert 0 < N < d and math.gcd(N, d) == 1
        e = ("Work from left to right. %d + %d = %d, then %d − %d = %d. The denominator stays %d. "
             "The answer is <b>%s</b>." % (a, b, a + b, a + b, c, N, d, fr(N, d)))
        rest = [(a + b, d) if a + b <= d else None, (N + 1, d), (N - 1, d), (a + b + c, d)]
        rnd.shuffle(rest)
        its.append(mcq("%s + %s − %s = ?" % (fr(a, d), fr(b, d), fr(c, d)), (N, d), rest + [(N, d + d)], e, rnd))
    # E: mixed + and −, no picture
    for op, d, a, b in [("+", 5, 1, 3), ("-", 9, 7, 5), ("+", 7, 1, 5), ("-", 12, 9, 2)]:
        its.append(add_q(a, b, d, rnd) if op == "+" else sub_q(a, b, d, rnd))
    # F: missing numerator
    note("n?", 4, 0, 11)
    e = "The parts are elevenths. 4 + ? = 9, and 9 − 4 = 5. So %s + %s = %s. The answer is <b>5</b>." % (fr(4, 11), fr(5, 11), fr(9, 11))
    its.append(mcq("%s + %s = %s. What is the missing number?" % (fr(4, 11), fr("<b>?</b>", 11), fr(9, 11)),
                   "5", ["13", "4", "9"], e, rnd))
    note("n?", 8, 0, 10)
    e = "The parts are tenths. 8 − ? = 1, and 8 − 1 = 7. So %s − %s = %s. The answer is <b>7</b>." % (fr(8, 10), fr(7, 10), fr(1, 10))
    its.append(mcq("%s − %s = %s. What is the missing number?" % (fr(8, 10), fr("<b>?</b>", 10), fr(1, 10)),
                   "7", ["9", "1", "6"], e, rnd))
    # G: which sum is 1
    e = ("Two fifths make 1 when the numerators add up to 5. 2 + 3 = 5, so %s + %s = %s = 1. "
         "The answer is <b>%s + %s</b>." % (fr(2, 5), fr(3, 5), fr(5, 5), fr(2, 5), fr(3, 5)))
    its.append(mcq("Which is equal to 1?", "%s + %s" % (fr(2, 5), fr(3, 5)),
                   ["%s + %s" % (fr(2, 5), fr(2, 5)), "%s + %s" % (fr(1, 5), fr(3, 5)), "%s + %s" % (fr(1, 5), fr(1, 5))], e, rnd))
    # H: greater
    assert Fraction(2, 8) + Fraction(3, 8) == Fraction(5, 8) and Fraction(7, 8) - Fraction(1, 8) == Fraction(6, 8)
    e = ("%s + %s = %s and %s − %s = %s. 6 eighths is more than 5 eighths. "
         "The answer is <b>%s − %s</b>." % (fr(2, 8), fr(3, 8), fr(5, 8), fr(7, 8), fr(1, 8), fr(6, 8), fr(7, 8), fr(1, 8)))
    its.append(mcq("Which is greater?", "%s − %s" % (fr(7, 8), fr(1, 8)),
                   ["%s + %s" % (fr(2, 8), fr(3, 8)), "They are equal", "We cannot tell"], e, rnd))
    assert len(its) == 20, len(its)
    return {"title": "Adding and subtracting within 1 whole", "items": its}


# ============================================================ set 5: word problems
def set_words(rnd):
    SPOTS.left = []
    its = []

    def add_w(q, n1, n2, d, pre="", figure=""):
        note("w+", n1, n2, d)
        N = n1 + n2
        assert N <= d and (N == d or math.gcd(N, d) == 1)
        its.append(mcq(figure + q, (N, d), wrong_add(n1, n2, d, rnd), pre + e_add(n1, n2, d), rnd))

    def sub_w(q, n1, n2, d, pre="", figure=""):
        note("w-", n1, n2, d)
        N = n1 - n2
        assert 0 < N and math.gcd(N, d) == 1
        its.append(mcq(figure + q, (N, d), wrong_sub(n1, n2, d, rnd), pre + e_sub(n1, n2, d), rnd))

    def left_w(q, n, d, pre="", figure=""):
        note("w1", n, 0, d)
        assert math.gcd(d - n, d) == 1
        e = "1 whole is %s. %s − %s = <b>%s</b>." % (fr(d, d), fr(d, d), fr(n, d), fr(d - n, d))
        its.append(mcq(figure + q, (d - n, d), wrong_one(n, d, rnd), pre + e, rnd))

    F = Fraction
    # 1 pizza altogether
    add_w("Ali and Siti shared a pizza. Ali ate %s of it (green). Siti ate %s of it (yellow). "
          "How much of the pizza did they eat altogether?" % (fr(2, 8), fr(3, 8)), 2, 3, 8,
          pre="“Altogether” means add. ", figure=fig(pie_svg(8, 2, 3, label="pizza")))
    # 2 pandan cake, model
    add_w("Mrs Lim cut a pandan cake into 6 equal slices. Her family ate %s of the cake at lunch. "
          "They ate %s of it at dinner. How much of the cake did they eat?" % (fr(1, 6), fr(4, 6)), 1, 4, 6,
          pre="The model has 6 units. 1 unit + 4 units = 5 units. ",
          figure=fig(model_svg([(F(1, 6), (1, 6)), (F(4, 6), (4, 6)), (F(1, 6), "?")], "1 cake", 6)))
    # 3 chocolate bar
    add_w("A chocolate bar has 10 equal pieces. Wei Ming ate %s of the bar. His sister ate %s of it. "
          "How much of the bar did they eat?" % (fr(3, 10), fr(4, 10)), 3, 4, 10,
          figure=fig(one_bar_svg(10, 3, 4)))
    # 4 water bottle
    add_w("Mei Ling drank %s of her water before recess. She drank %s of it after recess. "
          "How much of her water did she drink?" % (fr(1, 5), fr(2, 5)), 1, 2, 5,
          pre="Add the two parts. ")
    # 5 fence = 1 whole
    add_w("Jun Jie and his father painted a fence. They painted %s of it on Saturday and %s of it on Sunday. "
          "How much of the fence did they paint?" % (fr(3, 7), fr(4, 7)), 3, 4, 7,
          figure=fig(one_bar_svg(7, 3, 4)))
    # 6 watermelon left
    left_w("Raju’s family cut a watermelon into 8 equal slices. They ate %s of it. "
           "How much of the watermelon was left?" % fr(5, 8), 5, 8,
           pre="The whole watermelon is 1. Left = 1 − eaten. ",
           figure=fig(pie_svg(8, 0, 0, 5, base="#f7a8a8", label="watermelon")))
    # 7 ribbon left, model
    left_w("Priya had a ribbon. She used %s of it to make a bow. How much of the ribbon was left?" % fr(4, 9), 4, 9,
           pre="The model shows 9 units. 4 units were used, so 9 − 4 = 5 units are left. ",
           figure=fig(model_svg([(F(4, 9), (4, 9)), (F(5, 9), "?")], "1 ribbon", 9)))
    # 8 jug
    sub_w("A jug was %s full of soya bean milk. Mdm Wong poured out %s of the jug. "
          "How full is the jug now?" % (fr(7, 10), fr(4, 10)), 7, 4, 10,
          pre="“Poured out” means take away. ", figure=fig(bottle_svg(10, 7, crossed=4)))
    # 9 comparison, pizza
    sub_w("Ahmad ate %s of a pizza. Nurul ate %s of the same pizza. How much more did Ahmad eat than Nurul?"
          % (fr(7, 12), fr(2, 12)), 7, 2, 12, pre="“How much more” means subtract. The difference is 5 units. ",
          figure=fig(compare_svg([("Ahmad", F(7, 12), (7, 12)), ("Nurul", F(2, 12), (2, 12))], "?")))
    # 10 book read
    add_w("Xin Yi read %s of a library book on Monday. She read %s of it on Tuesday. "
          "How much of the book did she read on the two days?" % (fr(3, 11), fr(5, 11)), 3, 5, 11)
    # 11 book not read yet
    left_w("Hafiz has read %s of his storybook. How much of the book has he not read yet?" % fr(2, 9), 2, 9,
           pre="The whole book is 1. Not read = 1 − read. ")
    # 12 cake, two steps
    v = 1 - F(2, 9) - F(3, 9)
    assert v == F(4, 9)
    note("w2", 2, 3, 9)
    e = ("The model has 9 units. Chloe and Ryan ate 2 + 3 = 5 units. 9 − 5 = 4 units are left. "
         "So %s − %s = <b>%s</b> of the cake is left." % (fr(9, 9), fr(5, 9), fr(4, 9)))
    its.append(mcq(fig(model_svg([(F(2, 9), (2, 9)), (F(3, 9), (3, 9)), (v, "?")], "1 cake", 9)) +
                   "Chloe ate %s of a cake. Ryan ate %s of the cake. How much of the cake was left?" % (fr(2, 9), fr(3, 9)),
                   (4, 9), [(5, 9), (5, 18), (3, 9), (6, 9)], e, rnd))
    # 13 garden planted
    add_w("Mr Tan planted vegetables in %s of his garden. He planted flowers in %s of it. "
          "How much of the garden has plants?" % (fr(4, 7), fr(2, 7)), 4, 2, 7)
    # 14 comparison, bottles
    sub_w("Kumar and Devi have bottles of the same size. Kumar’s bottle is %s full. Devi’s bottle is %s full. "
          "How much more water is in Kumar’s bottle?" % (fr(5, 8), fr(2, 8)), 5, 2, 8,
          pre="Find the difference. ",
          figure=fig(compare_svg([("Kumar", F(5, 8), (5, 8)), ("Devi", F(2, 8), (2, 8))], "?")))
    # 15 paper strip
    add_w("For art, Sarah coloured %s of a paper strip red. She coloured %s of it blue. "
          "How much of the strip did she colour?" % (fr(3, 12), fr(4, 12)), 3, 4, 12,
          figure=fig(one_bar_svg(12, 3, 4)))
    # 16 kueh given away
    sub_w("Mdm Wong made a tray of kueh lapis cut into 12 equal pieces. %s of the tray was left after the party. "
          "She gave %s of the tray to her neighbour. How much of the tray is left now?" % (fr(11, 12), fr(6, 12)), 11, 6, 12,
          pre="“Gave” means take away. ")
    # 17 at first
    note("wa", 3, 4, 10)
    e = ("At first = poured out + left. The parts are tenths. 3 + 4 = 7. "
         "The bottle was <b>%s</b> full at first." % fr(7, 10))
    its.append(mcq(fig(model_svg([(F(3, 10), (3, 10)), (F(4, 10), (4, 10))], "?", 10)) +
                   "Siti poured %s of a bottle of water into a cup. %s of the bottle was left. "
                   "How full was the bottle at first?" % (fr(3, 10), fr(4, 10)),
                   (7, 10), [(7, 20), (1, 10), (4, 10), (8, 10)], e, rnd))
    # 18 trail, two steps
    v = 1 - F(4, 9) - F(3, 9)
    assert v == F(2, 9)
    note("w2", 4, 3, 9)
    e = ("The model has 9 units. The class walked 4 + 3 = 7 units. 9 − 7 = 2 units are still to walk. "
         "The answer is <b>%s</b>." % fr(2, 9))
    its.append(mcq(fig(model_svg([(F(4, 9), (4, 9)), (F(3, 9), (3, 9)), (v, "?")], "1 trail", 9)) +
                   "Class 2A visited Gardens by the Bay. They walked %s of a trail before lunch and %s of it after lunch. "
                   "How much of the trail did they still have to walk?" % (fr(4, 9), fr(3, 9)),
                   (2, 9), [(7, 9), (7, 18), (1, 9), (3, 9)], e, rnd))
    # 19 shared the whole pizza
    left_w("Nurul and Farah shared a pizza. They ate the whole pizza. Nurul ate %s of it. "
           "How much of the pizza did Farah eat?" % fr(3, 8), 3, 8,
           pre="The whole pizza is 1. Farah ate 1 − %s. " % fr(3, 8))
    # 20 fish tank
    add_w("Ethan’s water bottle was %s full (blue). At the water cooler, he poured in %s more (yellow). "
          "How full is the bottle now?" % (fr(1, 4), fr(2, 4)), 1, 2, 4,
          pre="“More” means add. ", figure=fig(bottle_svg(4, 1, k2=2)))
    assert len(its) == 20, len(its)
    return {"title": "Word problems with bar models", "items": its}


# ============================================================ lesson
def body_html():
    f_add = one_bar_svg(7, 2, 3)
    f_sub = one_bar_svg(8, 6, 0, crossed=2)
    f_one = one_bar_svg(8, 3, 5)
    f_model = model_svg([(Fraction(2, 8), (2, 8)), (Fraction(3, 8), (3, 8)), (Fraction(3, 8), "?")], "1 pizza", 8)
    return (
        "<h2>Like fractions</h2>"
        "<p>Like fractions have the same denominator, such as " + fr(2, 7) + " and " + fr(3, 7) + ". "
        "The parts are the same size. So we just count the parts.</p>"
        "<h2>Adding like fractions</h2>"
        "<p>Add the numerators. The denominator stays the same.</p>"
        "<figure class='sn-fig'>" + f_add +
        "<figcaption>2 sevenths + 3 sevenths = 5 sevenths.</figcaption></figure>"
        + ex("Example", fr(2, 7) + " + " + fr(3, 7) + " = ?", "Add the numerators: 2 + 3 = 5. Keep the denominator 7.", fr(5, 7)) +
        "<h2>Subtracting like fractions</h2>"
        "<p>Subtract the numerators. The denominator stays the same.</p>"
        "<figure class='sn-fig'>" + f_sub +
        "<figcaption>6 eighths take away 2 eighths leaves 4 eighths.</figcaption></figure>"
        + ex("Example", fr(7, 9) + " − " + fr(3, 9) + " = ?", "Subtract the numerators: 7 − 3 = 4. Keep the denominator 9.", fr(4, 9)) +
        "<h2>Making 1 whole</h2>"
        "<p>1 whole has all the parts: 1 = " + fr(4, 4) + " = " + fr(8, 8) + ". "
        "To make 1, the numerators must add up to the denominator.</p>"
        "<figure class='sn-fig'>" + f_one +
        "<figcaption>" + fr(3, 8) + " + " + fr(5, 8) + " = " + fr(8, 8) + " = 1.</figcaption></figure>"
        + ex("Example", fr(3, 8) + " + ? = 1", "1 = " + fr(8, 8) + ". 8 − 3 = 5.", fr(5, 8)) +
        "<h2>Word problems: draw a model</h2>"
        "<p>Draw a bar for the whole. Cut it into equal units. Mark what you know. Put “?” on the part to find.</p>"
        "<figure class='sn-fig'>" + f_model +
        "<figcaption>1 pizza = 8 units. Ali ate 2 units. Siti ate 3 units.</figcaption></figure>"
        + ex("Example", "Ali ate " + fr(2, 8) + " of a pizza. Siti ate " + fr(3, 8) + " of it. How much of the pizza was left?",
             "Eaten: 2 + 3 = 5 units. Left: 8 − 5 = 3 units.", fr(3, 8)) +
        "<h2>Common mistakes</h2>" +
        table(["Mistake", "Correct"], [
            [fr(1, 5) + " + " + fr(2, 5) + " = " + fr(3, 10) + " (adding the denominators)",
             "Keep the denominator: " + fr(3, 5)],
            [fr(5, 8) + " − " + fr(2, 8) + " = " + fr(3, 0) + " (subtracting the denominators)",
             "Keep the denominator: " + fr(3, 8)],
            ["1 − " + fr(3, 8) + " = " + fr(2, 8) + " (taking 1 from the numerator)",
             "Write 1 as " + fr(8, 8) + ": " + fr(8, 8) + " − " + fr(3, 8) + " = " + fr(5, 8)],
        ])
    )


FAQ = [
    {"q": "What is taught in P2 fractions?",
     "a": "In Primary 2, students learn halves, thirds, quarters and other unit fractions, compare fractions, and add and subtract like fractions within one whole, such as 2/7 + 3/7 = 5/7."},
    {"q": "How do I explain adding fractions to my child?",
     "a": "Cut a paper strip into equal parts and colour them. 2 fifths and 1 more fifth make 3 fifths, so only the numerator changes: 2/5 + 1/5 = 3/5."},
    {"q": "What is the most common mistake when adding fractions?",
     "a": "Adding the denominators, as in 1/5 + 2/5 = 3/10. The parts are still fifths, so the answer is 3/5."},
    {"q": "Is adding and subtracting fractions in the MOE syllabus for Primary 2?",
     "a": "Yes. Adding and subtracting like fractions within one whole, with denominators up to 12, is part of Fractions in the Primary 2 Standard Mathematics syllabus (MOE 2021). Related fractions and simplest form come in Primary 3."},
]


def gen_unit():
    USED.clear()
    rnd = random.Random(62807)
    sets = [set_add(rnd), set_sub(rnd), set_whole(rnd), set_mixed(rnd), set_words(rnd)]
    seen = set()
    for s in sets:
        assert len(s["items"]) == 20, (s["title"], len(s["items"]))
        assert sorted(it["a"] for it in s["items"]) == sorted([0, 1, 2, 3] * 5), s["title"]
        for it in s["items"]:
            assert len(set(it["c"])) == 4, it
            assert it["q"] not in seen, it["q"]
            seen.add(it["q"])
            assert it["q"].count("<svg") <= 1, it["q"]
    return {
        "country": "sg", "subject": "maths", "grade": "primary-2", "slug": "adding-and-subtracting-fractions", "sort": 7,
        "updated": UPDATED, "pdf_url": "",
        "title": "Primary 2 Adding and Subtracting Fractions",
        "seo_title": "P2 Adding and Subtracting Fractions Worksheets: Free Primary 2 Maths with Answers (MOE Syllabus)",
        "short_title": "Adding and Subtracting Fractions",
        "domain": "Number and Algebra",
        "standard_code": "Primary 2: Fractions",
        "standard_url": "https://www.moe.gov.sg/primary/curriculum/syllabus",
        "standard_text": "Adding and subtracting like fractions within one whole (denominators not exceeding 12)",
        "meta_desc": "Free P2 maths practice: add and subtract like fractions with fraction bars, make 1 whole and solve word problems. 100 questions with answers.",
        "key_big": "When the denominators are the same, add or subtract only the numerators.",
        "key_sub": "2/7 + 3/7 = 5/7, and the denominator stays 7.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }


if __name__ == "__main__":
    u = gen_unit()
    mark_large(u, "(bar of|bar model|bars A)")
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(u, f, ensure_ascii=False, indent=1)
    print("wrote", path)
