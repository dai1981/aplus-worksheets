# -*- coding: utf-8 -*-
"""
BC Grade 4 Math: Comparing and ordering fractions (BC Mathematics Curriculum, Grade 4: Number)
  python3 tools/gen_cabc_math_g4_fractions.py
Name fractions of shapes and sets, equivalent fractions with models (1/2 = 2/4 = 4/8),
compare with the same denominator or the same numerator (unit fractions), order fractions
and use the benchmarks 0, 1/2 and 1, then word problems in BC contexts.
Every choice that is a number carries its value; a wrong choice never equals the right value
or another wrong one. Comparisons and orders are checked with exact fractions.
Canadian English. HTML attributes use single quotes (no backslashes in the JSON).
"""
import json, math, os, random, re, itertools
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "ca-bc", "math", "grade-4")
SLUG = "comparing-and-ordering-fractions"
UPDATED = "2026-11-02"
FILL = "#4fae74"      # shaded part
LINE = "#2b2b2b"
THIN = "#7a7a7a"
RED = "#d6453b"
BLUE = "#2f6db5"
CANT = "You can’t tell"
SYM = {"<": "&lt;", ">": "&gt;", "=": "="}
WORD = {2: "halves", 3: "thirds", 4: "fourths", 5: "fifths", 6: "sixths", 8: "eighths", 9: "ninths",
        10: "tenths", 12: "twelfths", 100: "hundredths"}
ONE = {2: "half", 3: "third", 4: "fourth", 5: "fifth", 6: "sixth", 8: "eighth", 9: "ninth",
       10: "tenth", 12: "twelfth", 100: "hundredth"}


# ------------------------------------------------------------ numbers
def fr(a, b):
    return "<span class='fr'><span class='fn'>%s</span><span class='fd'>%s</span></span>" % (a, b)


def frq(b):
    return fr("<b>?</b>", b)


def Fc(a, b):
    return (fr(a, b), F(a, b))


def Nc(n):
    return (str(n), F(n))


def parts(n, d):
    return "%d %s" % (n, ONE[d] if n == 1 else WORD[d])


def sign(a, b, c, d):
    x, y = F(a, b), F(c, d)
    return "<" if x < y else (">" if x > y else "=")


def st(a, b, s, c, d):
    return "%s %s %s" % (fr(a, b), SYM[s], fr(c, d))


def show(lst):
    return ", ".join(fr(*x) for x in lst)


# ------------------------------------------------------------ helpers
def mcq(q, correct, cands, e):
    """correct and cands are html strings or (html, value) pairs. Right answer first; balance() places it."""
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
        if not s or s in seen:
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
    return {"q": q, "c": [cs] + pick, "a": 0, "e": e}


def fixed(q, ans, e):
    """Choices are the letters of one picture (A, B, C, D). They keep this order."""
    labels = ["A", "B", "C", "D"]
    return {"q": q, "c": labels, "a": labels.index(ans), "e": e, "_fixed": True}


def balance(sets, rnd):
    """Each answer position (A to D) is correct 5 times in every set. Picture-letter items keep their order."""
    for s in sets:
        targets = [0, 1, 2, 3] * 5
        for it in s["items"]:
            if it.get("_fixed"):
                targets.remove(it["a"])
        rnd.shuffle(targets)
        k = 0
        for it in s["items"]:
            if it.pop("_fixed", False):
                continue
            t = targets[k]
            k += 1
            c = it["c"]
            right = c[it["a"]]
            wrong = [x for i, x in enumerate(c) if i != it["a"]]
            rnd.shuffle(wrong)
            it["c"] = wrong[:t] + [right] + wrong[t:]
            it["a"] = t
        assert sorted(it["a"] for it in s["items"]) == sorted([0, 1, 2, 3] * 5), s["title"]


def cmp_mcq(q, a, b, c, d, e):
    """Choices: the three signs, plus the statement read backwards."""
    s = sign(a, b, c, d)
    right = st(a, b, s, c, d)
    wrong = [st(a, b, o, c, d) for o in "<>=" if o != s]
    wrong.append(st(c, d, ">" if s == "=" else s, a, b))
    assert ("<b>%s</b>" % right) in e or right in e, e
    return mcq(q, right, wrong, e)


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
    """Tag wide pictures so they print larger and stay readable."""
    rx = re.compile(r"<svg (?=[^>]*aria-label='" + pattern + ")")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u


# ------------------------------------------------------------ pictures
def txt(x, y, s, size=16, color=LINE):
    return ("<text x='%.1f' y='%.1f' font-size='%d' font-weight='700' fill='%s' text-anchor='middle'>%s</text>"
            % (x, y, size, color, s))


def sfr(x, cy, a, b, size=16, color=LINE):
    """Stacked fraction in SVG, centred at x, fraction bar at cy."""
    w = max(len(str(a)), len(str(b))) * size * 0.62 + 6
    return (txt(x, cy - 4, a, size, color) +
            "<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='1.8'/>"
            % (x - w / 2, cy, x + w / 2, cy, color) + txt(x, cy + size + 1, b, size, color))


def bar_cuts(x, y, W, H, cuts, shaded):
    """Bar cut at the given fractions of its length (0 < cut < 1); parts in `shaded` are filled."""
    edges = [0.0] + list(cuts) + [1.0]
    s = []
    for i in range(len(edges) - 1):
        s.append("<rect x='%.1f' y='%.1f' width='%.1f' height='%d' fill='%s' stroke='none'/>"
                 % (x + edges[i] * W, y, (edges[i + 1] - edges[i]) * W, H, FILL if i in shaded else "#fff"))
    for c in cuts:
        s.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='2.5'/>"
                 % (x + c * W, y, x + c * W, y + H, LINE))
    s.append("<rect x='%.1f' y='%.1f' width='%.1f' height='%d' fill='none' stroke='%s' stroke-width='2.5'/>" % (x, y, W, H, LINE))
    return "".join(s)


def bar_row(x, y, W, H, n, k):
    return bar_cuts(x, y, W, H, [i / n for i in range(1, n)], set(range(k)))


def bar_svg(n, k, W=260, H=42):
    return svg_wrap(W + 12, H + 12, bar_row(6, 6, W, H, n, k), "bar split into %d equal parts with %d shaded" % (n, k))


def wedges(cx, cy, r, n, k):
    s = []
    if n == 1:
        return "<circle cx='%.1f' cy='%.1f' r='%d' fill='%s' stroke='%s' stroke-width='2.2'/>" % (cx, cy, r, FILL if k else "#fff", LINE)
    for i in range(n):
        t0 = math.radians(-90 + 360.0 * i / n)
        t1 = math.radians(-90 + 360.0 * (i + 1) / n)
        s.append("<path d='M%.1f %.1f L%.1f %.1f A%d %d 0 0 1 %.1f %.1f Z' fill='%s' stroke='%s' stroke-width='2.2' stroke-linejoin='round'/>"
                 % (cx, cy, cx + r * math.cos(t0), cy + r * math.sin(t0), r, r,
                    cx + r * math.cos(t1), cy + r * math.sin(t1), FILL if i < k else "#fff", LINE))
    return "".join(s)


def circle_svg(n, k, r=56):
    d = 2 * r + 12
    return svg_wrap(d, d, wedges(r + 6, r + 6, r, n, k), "circle split into %d equal parts with %d shaded" % (n, k))


def rect_svg(rows, cols, k, cell=40):
    s = []
    for r in range(rows):
        for c in range(cols):
            i = r * cols + c
            s.append("<rect x='%d' y='%d' width='%d' height='%d' fill='%s' stroke='%s' stroke-width='2.5'/>"
                     % (6 + c * cell, 6 + r * cell, cell, cell, FILL if i < k else "#fff", LINE))
    return svg_wrap(cols * cell + 12, rows * cell + 12, "".join(s),
                    "rectangle split into %d equal parts with %d shaded" % (rows * cols, k))


def counters_svg(n, k, per_row=6, r=15):
    """n counters, the first k green, the rest white."""
    rows = (n + per_row - 1) // per_row
    cols = min(n, per_row)
    gap = 8
    s = []
    for i in range(n):
        row, col = divmod(i, per_row)
        cx = 6 + r + col * (2 * r + gap)
        cy = 6 + r + row * (2 * r + gap)
        s.append("<circle cx='%d' cy='%d' r='%d' fill='%s' stroke='%s' stroke-width='2.2'/>"
                 % (cx, cy, r, FILL if i < k else "#fff", LINE))
    return svg_wrap(12 + cols * 2 * r + (cols - 1) * gap, 12 + rows * 2 * r + (rows - 1) * gap, "".join(s),
                    "set of %d counters, %d green and %d white" % (n, k, n - k))


def two_bars_svg(a, b, c, d, W=250, H=38, labels=True):
    """Two bars of the same whole: a/b on top, c/d below, fraction labels on the left."""
    LW = 44 if labels else 0
    s = []
    for row, (n, k) in enumerate([(b, a), (d, c)]):
        y = 6 + row * (H + 14)
        if labels:
            num, den = (a, b) if row == 0 else (c, d)
            s.append(sfr(6 + LW / 2 - 4, y + H / 2, num, den))
        s.append(bar_row(6 + LW, y, W, H, n, k))
    return svg_wrap(W + LW + 12, 2 * H + 26, "".join(s),
                    "two bars of the same size showing %d/%d and %d/%d" % (a, b, c, d))


def eq_bars_svg(rows, W=260, H=36, labels=None):
    """Bars of the same size, one per (n, k); optional stacked labels on the left."""
    LW = 44 if labels else 0
    s = []
    for i, (n, k) in enumerate(rows):
        y = 6 + i * (H + 12)
        if labels:
            s.append(sfr(6 + LW / 2 - 4, y + H / 2, *labels[i]))
        s.append(bar_row(6 + LW, y, W, H, n, k))
    return svg_wrap(W + LW + 12, len(rows) * (H + 12) + 0, "".join(s),
                    "%d bars of the same size, %s" % (len(rows), ", ".join("%d of %d parts shaded" % (k, n) for n, k in rows)))


def two_circles_svg(a, b, c, d, r=40):
    cy = 6 + r
    x1 = 6 + 34 + r
    x2 = x1 + r + 26 + 34 + r
    s = [sfr(6 + 15, cy, a, b), wedges(x1, cy, r, b, a), sfr(x1 + r + 26 + 15, cy, c, d), wedges(x2, cy, r, d, c)]
    return svg_wrap(x2 + r + 6, 2 * r + 12, "".join(s),
                    "two circles of the same size showing %d/%d and %d/%d" % (a, b, c, d))


def diff_bars_svg(n1, k1, W1, n2, k2, W2, H=34):
    s = []
    for row, (lab, n, k, W) in enumerate([("A", n1, k1, W1), ("B", n2, k2, W2)]):
        y = 6 + row * (H + 14)
        s.append("<text x='12' y='%.1f' font-size='17' font-weight='800' fill='%s' text-anchor='middle'>%s</text>" % (y + H / 2 + 6, LINE, lab))
        s.append(bar_row(30, y, W, H, n, k))
    return svg_wrap(30 + max(W1, W2) + 6, 2 * H + 26, "".join(s), "bar A and bar B are different lengths")


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
    """Two number lines 0..1: top in b parts with an arrow at a/b, bottom in d parts, dashed guide."""
    x0, x1 = 20, W - 20
    Y1, Y2 = 36, 104
    X = x0 + (x1 - x0) * a / b
    s = [ticks(b, Y1, x0, x1), ticks(d, Y2, x0, x1), tri(X, Y1),
         "<line x1='%.1f' y1='%d' x2='%.1f' y2='%d' stroke='%s' stroke-width='2' stroke-dasharray='5 4'/>"
         % (X, Y1 + 12, X, Y2 - 12, BLUE)]
    return svg_wrap(W, Y2 + 38, "".join(s),
                    "two number lines from 0 to 1 of the same length, the top one in %d equal parts with an arrow at %d of them, "
                    "the bottom one in %d equal parts" % (b, a, d))


def two_lines_svg(a, b, c, d, W=330):
    """Two number lines from 0 to 1 with a dot at a/b and at c/d."""
    LW, L = 44, 56
    R = W - 18
    s = []
    for row, (num, den, col) in enumerate([(a, b, RED), (c, d, BLUE)]):
        Y = 22 + row * 64
        s.append(sfr(6 + LW / 2 - 4, Y, num, den, color=col))
        s.append(ticks(den, Y, L, R, labels=False))
        for i, t in ((0, "0"), (den, "1")):
            X = L + (R - L) * i / den
            s.append(txt(X, Y + 29, t, 15))
        s.append("<circle cx='%.1f' cy='%d' r='7' fill='%s'/>" % (L + (R - L) * num / den, Y, col))
    return svg_wrap(W, 22 + 64 + 36, "".join(s),
                    "two number lines from 0 to 1 with dots at %d/%d and %d/%d" % (a, b, c, d))


def bench_line_svg(a, b, W=380):
    """Number line 0..1 in b parts with labels 0, 1/2, 1 and a dot at a/b."""
    x0, x1 = 24, W - 24
    Y = 26
    s = [ticks(b, Y, x0, x1)]
    Xh = (x0 + x1) / 2
    if b % 2:
        s.append("<line x1='%.1f' y1='%d' x2='%.1f' y2='%d' stroke='%s' stroke-width='2' stroke-dasharray='4 3'/>"
                 % (Xh, Y - 11, Xh, Y + 11, RED))
    s.append(sfr(Xh, Y + 32, 1, 2, 15, RED if b % 2 else LINE))
    X = x0 + (x1 - x0) * a / b
    s.append("<circle cx='%.1f' cy='%d' r='7' fill='%s'/>" % (X, Y, BLUE))
    return svg_wrap(W, Y + 58, "".join(s), "number line from 0 to 1 in %d equal parts with a dot" % b)


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


def four_bars_svg(specs, W=150, H=34):
    """Pictures A to D in a 2 x 2 grid: each spec is (cuts, shaded set)."""
    s = []
    for i, (cuts, sh) in enumerate(specs):
        col, row = i % 2, i // 2
        x = 6 + col * (W + 46)
        y = 6 + row * (H + 18)
        s.append("<text x='%d' y='%.1f' font-size='17' font-weight='800' fill='%s' text-anchor='middle'>%s</text>"
                 % (x + 8, y + H / 2 + 6, LINE, "ABCD"[i]))
        s.append(bar_cuts(x + 22, y, W, H, cuts, sh))
    return svg_wrap(6 + 2 * (W + 22) + 24 + 6, 2 * H + 18 + 12, "".join(s), "pictures A to D, four bars")


def eq_cuts(n):
    return [i / n for i in range(1, n)]


# ============================================================ set 1: name fractions of shapes and sets
def e_name(n, k, what="parts", unshaded=False):
    if unshaded:
        return ("There are %d equal %s. %d %s shaded, so %d − %d = %d %s <b>not</b> shaded. "
                "The answer is <b>%s</b>. The bottom number counts <b>all</b> the equal %s."
                % (n, what, k, "is" if k == 1 else "are", n, k, n - k, "is" if n - k == 1 else "are", fr(n - k, n), what))
    return ("There are %d equal %s and %d %s shaded. So <b>%s</b> is shaded. "
            "The bottom number counts all the equal %s, not just the white ones."
            % (n, what, k, "is" if k == 1 else "are", fr(k, n), what))


def set_name(rnd):
    its = []
    # shaded shapes
    shapes = [("c", 3, 1), ("b", 5, 3), ("c", 8, 5), ("r", (2, 3), 4), ("c", 4, 3), ("b", 10, 7), ("r", (2, 4), 3)]
    for kind, n, k in shapes:
        if kind == "b":
            svg, N = bar_svg(n, k), n
        elif kind == "c":
            svg, N = circle_svg(n, k), n
        else:
            svg, N = rect_svg(n[0], n[1], k), n[0] * n[1]
        q = fig(svg) + "What fraction of the shape is shaded?"
        its.append(mcq(q, Fc(k, N), [Fc(N - k, N), Fc(k, N - k), Fc(N, k), Fc(N - k, k)], e_name(N, k)))
    # not shaded
    for kind, n, k in [("b", 5, 2), ("c", 6, 1)]:
        svg = bar_svg(n, k) if kind == "b" else circle_svg(n, k)
        q = fig(svg) + "What fraction of the shape is <b>not</b> shaded?"
        its.append(mcq(q, Fc(n - k, n), [Fc(k, n), Fc(n - k, k), Fc(k, n - k), Fc(n, n - k)], e_name(n, k, unshaded=True)))

    # sets of counters
    for n, k, per in [(6, 2, 6), (8, 3, 4), (10, 4, 5)]:
        q = fig(counters_svg(n, k, per)) + "What fraction of the counters are green?"
        e = ("The whole is the <b>set</b> of %d counters. %d of them are green, so <b>%s</b> of the set is green. "
             "Do not compare green with white (%d to %d)." % (n, k, fr(k, n), k, n - k))
        its.append(mcq(q, Fc(k, n), [Fc(n - k, n), Fc(k, n - k), Fc(n, k)], e))
    n, k = 9, 2
    q = fig(counters_svg(n, k, 5)) + "What fraction of the counters are <b>not</b> green?"
    e = ("There are %d counters in the set. %d are green, so %d − %d = %d are not green. The answer is <b>%s</b>."
         % (n, k, n, k, n - k, fr(n - k, n)))
    its.append(mcq(q, Fc(n - k, n), [Fc(k, n), Fc(n - k, k), Fc(k, n - k)], e))

    q = "A bag has 4 red marbles and 3 blue marbles. What fraction of the marbles are blue?"
    e = ("The whole set is 4 + 3 = 7 marbles. 3 are blue, so <b>%s</b> are blue. "
         "%s compares blue with red; it does not use the whole set." % (fr(3, 7), fr(3, 4)))
    its.append(mcq(q, Fc(3, 7), [Fc(3, 4), Fc(4, 7), Fc(7, 3)], e))
    q = "A box has 12 pencil crayons. 5 of them are broken. What fraction of the pencil crayons are broken?"
    e = "There are 12 pencil crayons in the whole set and 5 are broken. So <b>%s</b> are broken." % fr(5, 12)
    its.append(mcq(q, Fc(5, 12), [Fc(7, 12), Fc(5, 7), Fc(12, 5)], e))

    # pictures A to D
    specs = [([0.18, 0.5, 0.82], {0, 1, 2}), (eq_cuts(4), {0}), (eq_cuts(4), {0, 1, 2}), (eq_cuts(5), {0, 1, 2})]
    q = fig(four_bars_svg(specs)) + "Which picture shows %s shaded?" % fr(3, 4)
    e = ("Picture <b>C</b> has 4 <b>equal</b> parts with 3 shaded. Picture A has 4 parts, but they are not equal. "
         "B shows %s and D shows %s." % (fr(1, 4), fr(3, 5)))
    its.append(fixed(q, "C", e))
    specs = [(eq_cuts(3), {0}), ([0.25, 0.5], {0, 1}), (eq_cuts(5), {0, 1}), (eq_cuts(3), {0, 1})]
    q = fig(four_bars_svg(specs)) + "Which picture shows %s shaded?" % fr(2, 3)
    e = ("Picture <b>D</b> has 3 <b>equal</b> parts with 2 shaded. Picture B has 3 parts, but they are not equal. "
         "A shows %s and C shows %s." % (fr(1, 3), fr(2, 5)))
    its.append(fixed(q, "D", e))

    # unequal parts
    q = (fig(svg_wrap(272, 54, bar_cuts(6, 6, 260, 42, [0.4, 0.62, 0.8], {0}), "bar cut into 4 parts that are not equal, 1 part shaded"))
         + "Leah says %s of this bar is shaded. Is she right?" % fr(1, 4))
    e = ("<b>No. The 4 parts are not equal.</b> A fraction names <b>equal</b> parts of a whole. "
         "The shaded part is bigger than the other parts, so it is more than %s." % fr(1, 4))
    its.append(mcq(q, "No. The 4 parts are not equal.",
                   ["Yes. 1 of 4 parts is shaded.", "No. It shows %s." % fr(1, 3), "No. It shows %s." % fr(3, 4)], e))

    # whole set from a part
    for part, (a, b) in [(4, (1, 3)), (5, (1, 2))]:
        whole = part * b
        q = fig(counters_svg(part, part, part)) + "These %d counters are %s of a set. How many counters are in the whole set?" % (part, fr(a, b))
        e = ("%s means the set has %d equal groups, and this is 1 group. %d groups of %d is %d × %d = <b>%d</b> counters."
             % (fr(a, b), b, b, part, b, part, whole))
        its.append(mcq(q, Nc(whole), [Nc(part + b), Nc(part * (b + 1)), Nc(part * (b - 1)) if b > 2 else None, Nc(b), Nc(part + 1)], e))
    assert len(its) == 20, len(its)
    return {"title": "Name fractions of shapes and sets", "items": its}


# ============================================================ set 2: equivalent fractions with models
def set_equiv(rnd):
    its = []
    for a, b, d in [(1, 2, 4), (1, 3, 6), (1, 2, 8), (2, 4, 8), (2, 3, 6), (3, 4, 8), (2, 5, 10)]:
        n = d // b
        c = a * n
        q = (fig(two_bars_svg(a, b, c, d, labels=False)) + "The bars are the same size, and the shaded parts are equal.<br>%s = %s"
             % (fr(a, b), frq(d)))
        e = ("The bottom bar has %d equal parts, so each %s of the top bar is cut into %d parts. "
             "%s become%s %d × %d = <b>%d</b> %s. So %s = %s."
             % (d, ONE[b], n, parts(a, b), "s" if a == 1 else "", a, n, c, WORD[d], fr(a, b), fr(c, d)))
        its.append(mcq(q, Nc(c), [Nc(a + (d - b)), Nc(a), Nc(d - c), Nc(c + 1), Nc(n), Nc(d)], e))

    q = (fig(eq_bars_svg([(2, 1), (4, 2), (8, 4)], labels=[(1, 2), (2, 4), ("?", 8)])) +
         "Look at the three bars. Which number is missing?<br>%s = %s = %s" % (fr(1, 2), fr(2, 4), frq(8)))
    e = ("All three bars are shaded to the same place. The bottom bar has 8 parts and 4 are shaded, so %s = %s = <b>%s</b>. "
         "The numbers double each time: 1, 2, <b>4</b> and 2, 4, 8." % (fr(1, 2), fr(2, 4), fr(4, 8)))
    its.append(mcq(q, Nc(4), [Nc(3), Nc(6), Nc(2)], e))

    for d, c, b in [(8, 6, 4), (6, 4, 3), (10, 8, 5), (8, 2, 4)]:
        n = d // b
        a = c // n
        q = (fig(circle_svg(d, c)) + "The circle has %d equal parts. %s is shaded.<br>%s = %s" % (d, fr(c, d), fr(c, d), frq(b)))
        e = ("Put the %d parts in groups of %d. That makes %d equal groups. The %d shaded parts make %d ÷ %d = <b>%d</b> group%s. "
             "So %s = %s." % (d, n, b, c, c, n, a, "" if a == 1 else "s", fr(c, d), fr(a, b)))
        its.append(mcq(q, Nc(a), [Nc(c - (d - b)), Nc(c), Nc(b - a), Nc(a + 1), Nc(c + 1), Nc(b)], e))

    # double number lines
    for b, a, d in [(2, 1, 8), (5, 2, 10)]:
        c = a * d // b
        q = fig(double_line_svg(b, a, d)) + "The arrow points to %s. Use the bottom number line.<br>%s = %s" % (fr(a, b), fr(a, b), frq(d))
        e = ("Follow the dashed line down. It lands on mark %d of %d on the bottom line, so %s = <b>%s</b>."
             % (c, d, fr(a, b), fr(c, d)))
        its.append(mcq(q, Nc(c), [Nc(a + (d - b)), Nc(a), Nc(c + 1), Nc(d - c)], e))

    q = "Which fraction is equal to %s?" % fr(1, 2)
    e = ("Half of 8 is 4, so <b>%s</b> = %s. %s is less than half and %s is more than half. "
         "%s has the same top number, but fourths are smaller than halves." % (fr(4, 8), fr(1, 2), fr(3, 8), fr(5, 8), fr(1, 4)))
    its.append(mcq(q, Fc(4, 8), [Fc(3, 8), Fc(1, 4), Fc(5, 8)], e))
    q = "Which fraction is equal to %s?" % fr(2, 3)
    e = ("Cut each third into 2 equal parts: 2 × 2 = 4 and 3 × 2 = 6, so %s = <b>%s</b>. "
         "Multiply the top <b>and</b> the bottom by the same number." % (fr(2, 3), fr(4, 6)))
    its.append(mcq(q, Fc(4, 6), [Fc(2, 6), Fc(5, 6), Fc(3, 6)], e))
    q = "Which fraction is <b>not</b> equal to %s?" % fr(1, 2)
    e = ("Half of 4 is 2, half of 10 is 5 and half of 6 is 3, so %s, %s and %s are all equal to %s. "
         "Half of 8 is 4, not 3, so <b>%s</b> is not equal to %s." % (fr(2, 4), fr(5, 10), fr(3, 6), fr(1, 2), fr(3, 8), fr(1, 2)))
    its.append(mcq(q, fr(3, 8), [fr(2, 4), fr(5, 10), fr(3, 6)], e))

    SAME, TOP, BOT = "They are equal", "The top bar has more", "The bottom bar has more"
    for a, b, c, d in [(1, 2, 2, 4), (3, 4, 5, 8), (1, 3, 3, 6)]:
        x, y = F(a, b), F(c, d)
        right = SAME if x == y else (TOP if x > y else BOT)
        if x == y:
            e = ("Both bars are shaded to the same place. The bottom bar has more parts, but each part is smaller. "
                 "So <b>they are equal</b>: %s = %s." % (fr(a, b), fr(c, d)))
        else:
            eq = (x * d).numerator
            e = ("%s is the same as %s, and the bottom bar has %s shaded. So <b>%s</b>: %s %s %s. "
                 "More shaded parts does not always mean more shaded."
                 % (fr(a, b), fr(eq, d), fr(c, d), right.lower(), fr(a, b), SYM[sign(a, b, c, d)], fr(c, d)))
        its.append(mcq(fig(two_bars_svg(a, b, c, d, labels=False)) + "The bars are the same size. Compare the shaded parts.",
                       right, [SAME, TOP, BOT, CANT], e))
    assert len(its) == 20, len(its)
    return {"title": "Equivalent fractions with models", "items": its}


# ============================================================ set 3: same denominator or same numerator
def e_same_den(a, b, c, d):
    s = sign(a, b, c, d)
    return ("Both are %s, so the pieces are the same size. %s %s %s, so <b>%s</b>."
            % (WORD[b], parts(a, b), {"<": "is less than", ">": "is more than", "=": "is the same as"}[s], parts(c, d), st(a, b, s, c, d)))


def e_same_num(a, b, c, d):
    s = sign(a, b, c, d)
    small, big = min(b, d), max(b, d)
    pieces = "1 piece" if a == 1 else "%d pieces" % a
    return ("Both have <b>%s</b>. %s are bigger than %s, because the whole is cut into fewer parts. "
            "So <b>%s</b>." % (pieces, WORD[small].capitalize(), WORD[big], st(a, b, s, c, d)))


def order_mcq(fs, way, why):
    up = sorted(fs, key=lambda x: F(*x))
    assert len(set(F(*x) for x in fs)) == len(fs)
    right_l = up if way == "up" else up[::-1]
    rev = way == "down"
    cands = [sorted(fs, key=lambda x: x[1], reverse=rev),        # bigger denominator = bigger fraction
             sorted(fs, key=lambda x: x[0], reverse=rev),        # compare only the top numbers
             right_l[::-1]]                                      # wrong direction
    cands += [list(p) for p in itertools.permutations(fs)]
    q = "Order from <b>%s</b>:<br>%s" % ("least to greatest" if way == "up" else "greatest to least", show(fs))
    e = why + " So the order is <b>%s</b>." % show(right_l)
    return mcq(q, show(right_l), [show(c) for c in cands], e)


def set_compare(rnd):
    its = []
    Q = "Which statement is true?"
    # same denominator
    for a, b, c, d in [(3, 5, 2, 5), (4, 8, 7, 8)]:
        its.append(cmp_mcq(fig(two_bars_svg(a, b, c, d)) + "The two bars are the same size. " + Q, a, b, c, d, e_same_den(a, b, c, d)))
    for a, b, c, d in [(5, 6, 1, 6), (7, 10, 9, 10), (2, 3, 1, 3)]:
        its.append(cmp_mcq("Compare %s and %s. %s" % (fr(a, b), fr(c, d), Q), a, b, c, d, e_same_den(a, b, c, d)))
    e = "All four are eighths, so the pieces are the same size. 7 is the most pieces, so <b>%s</b> is the greatest." % fr(7, 8)
    its.append(mcq("Which fraction is the <b>greatest</b>?", Fc(7, 8), [Fc(5, 8), Fc(2, 8), Fc(3, 8)], e))
    its.append(order_mcq([(4, 10), (9, 10), (1, 10)], "up", "All are tenths, so compare the top numbers: 1 &lt; 4 &lt; 9."))
    q = (fig(diff_bars_svg(4, 2, 150, 4, 3, 90)) +
         "%s of bar A is shaded. %s of bar B is shaded. Ethan says the picture shows %s &gt; %s. What is wrong?"
         % (fr(2, 4), fr(3, 4), fr(2, 4), fr(3, 4)))
    e = ("<b>The bars are different wholes.</b> Bar A is longer than bar B, so %s of A can look as big as %s of B. "
         "Compare fractions of the <b>same</b> whole: %s &lt; %s." % (fr(2, 4), fr(3, 4), fr(2, 4), fr(3, 4)))
    its.append(mcq(q, "The bars are different wholes.",
                   ["Nothing. %s &gt; %s." % (fr(2, 4), fr(3, 4)), "He should count the white parts.",
                    "Both bars have 4 parts, so they are equal."], e))

    # same numerator
    for a, b, c, d in [(1, 4, 1, 8)]:
        its.append(cmp_mcq(fig(two_bars_svg(a, b, c, d)) + "The two bars are the same size. " + Q, a, b, c, d, e_same_num(a, b, c, d)))
    its.append(cmp_mcq(fig(two_circles_svg(1, 6, 1, 3)) + "The two circles are the same size. " + Q, 1, 6, 1, 3, e_same_num(1, 6, 1, 3)))
    for a, b, c, d in [(1, 10, 1, 5), (1, 6, 1, 12), (1, 100, 1, 10)]:
        e = e_same_num(a, b, c, d) + " A bigger bottom number means <b>smaller</b> pieces."
        its.append(cmp_mcq("Compare %s and %s. %s" % (fr(a, b), fr(c, d), Q), a, b, c, d, e))
    for a, b, c, d in [(3, 4, 3, 8), (2, 5, 2, 3), (5, 6, 5, 10)]:
        its.append(cmp_mcq("Compare %s and %s. %s" % (fr(a, b), fr(c, d), Q), a, b, c, d, e_same_num(a, b, c, d)))
    e = ("All four are 1 piece. The biggest bottom number makes the smallest pieces, so <b>%s</b> is the smallest." % fr(1, 10))
    its.append(mcq("Which fraction is the <b>smallest</b>?", Fc(1, 10), [Fc(1, 3), Fc(1, 6), Fc(1, 4)], e))
    e = ("All four have 3 pieces. The smallest bottom number makes the biggest pieces, so <b>%s</b> is the greatest." % fr(3, 4))
    its.append(mcq("Which fraction is the <b>greatest</b>?", Fc(3, 4), [Fc(3, 10), Fc(3, 8), Fc(3, 5)], e))
    its.append(order_mcq([(1, 3), (1, 8), (1, 5)], "up",
                         "All are 1 piece. More parts means smaller parts: eighths are the smallest and thirds are the biggest."))
    q = "Liam says %s &gt; %s because 8 &gt; 4. Is he right?" % (fr(1, 8), fr(1, 4))
    e = ("<b>No. Eighths are smaller than fourths.</b> Cut the same whole into 8 parts and each part is smaller than when you cut it into 4 parts. "
         "So %s &lt; %s." % (fr(1, 8), fr(1, 4)))
    its.append(mcq(q, "No. Eighths are smaller than fourths.",
                   ["Yes. 8 is greater than 4.", "Yes. Eighths have more parts.", "No. %s = %s." % (fr(1, 8), fr(1, 4))], e))
    assert len(its) == 20, len(its)
    return {"title": "Compare with the same denominator or numerator", "items": its}


# ============================================================ set 4: benchmarks and ordering
def half_reason(a, b):
    if b % 2 == 0:
        h = b // 2
        if a == h:
            return "Half of %d is %d, so %s is exactly %s." % (b, h, fr(a, b), fr(1, 2))
        return "Half of %d is %d. %d is %s %d, so %s is %s %s." % (
            b, h, a, "less than" if a < h else "more than", h, fr(a, b), "less than" if a < h else "more than", fr(1, 2))
    return "Double the top: 2 × %d = %d, which is %s %d, so %s is %s %s." % (
        a, 2 * a, "less than" if 2 * a < b else "more than", b, fr(a, b), "less than" if 2 * a < b else "more than", fr(1, 2))


def closest(a, b):
    x = F(a, b)
    ds = sorted((abs(x - v), k) for k, v in (("0", F(0)), ("h", F(1, 2)), ("1", F(1))))
    assert ds[0][0] != ds[1][0], (a, b)
    return ds[0][1]


def set_bench(rnd):
    its = []
    lab = {"0": "Closest to 0", "h": "Closest to %s" % fr(1, 2), "1": "Closest to 1", "g": "Greater than 1"}
    reason = {"0": "only %s away from 0", "h": "only %s away from %s" % ("%s", fr(1, 2)), "1": "only %s away from 1"}
    for i, (a, b) in enumerate([(1, 8), (9, 10), (2, 5), (5, 6)]):
        k = closest(a, b)
        tgt = {"0": F(0), "h": F(1, 2), "1": F(1)}[k]
        dist = abs(F(a, b) - tgt)
        e = ("%s is <b>%s</b>: it is %s." % (fr(a, b), lab[k].lower(), reason[k] % fr(dist.numerator, dist.denominator)))
        q = ((fig(bench_line_svg(a, b)) + "The dot shows %s. " % fr(a, b)) if i < 2 else "") + \
            "Which benchmark is %s closest to: 0, %s or 1?" % (fr(a, b), fr(1, 2))
        its.append(mcq(q, lab[k], [lab[x] for x in ("0", "h", "1", "g")], e))

    where = {"lt": "Less than %s" % fr(1, 2), "eq": "Exactly %s" % fr(1, 2),
             "mid": "Between %s and 1" % fr(1, 2), "gt": "Greater than 1"}
    for a, b in [(3, 8), (5, 10), (4, 6), (5, 4)]:
        x = F(a, b)
        w = "lt" if x < F(1, 2) else "eq" if x == F(1, 2) else "mid" if x < 1 else "gt"
        if w == "gt":
            e = ("The top number (%d) is bigger than the bottom number (%d), so %s is <b>greater than 1</b>: %s = 1 whole and %s more."
                 % (a, b, fr(a, b), fr(b, b), fr(a - b, b)))
        else:
            e = half_reason(a, b) + " So the answer is <b>%s</b>." % where[w].lower()
            if w == "mid":
                e += " It is less than 1 because %d is less than %d." % (a, b)
        its.append(mcq("Where is %s?" % fr(a, b), where[w], [where[k] for k in ("lt", "eq", "mid", "gt")], e))

    for a, b, c, d in [(3, 8, 4, 6), (2, 5, 7, 12), (5, 6, 4, 10)]:
        s = sign(a, b, c, d)
        e = "Use %s as a benchmark. %s %s So <b>%s</b>." % (fr(1, 2), half_reason(a, b), half_reason(c, d), st(a, b, s, c, d))
        its.append(cmp_mcq("Compare %s and %s. Which statement is true?" % (fr(a, b), fr(c, d)), a, b, c, d, e))
    a, b, c, d = 5, 4, 7, 8
    e = ("Use 1 as a benchmark. %s is more than 1 (the top is bigger than the bottom). %s is less than 1 (the top is smaller than the bottom). "
         "So <b>%s</b>." % (fr(5, 4), fr(7, 8), st(a, b, sign(a, b, c, d), c, d)))
    its.append(cmp_mcq("Compare %s and %s. Which statement is true?" % (fr(a, b), fr(c, d)), a, b, c, d, e))

    e = ("%s, %s and %s are all more than %s. %s So <b>%s</b> is the one less than %s."
         % (fr(4, 6), fr(5, 8), fr(7, 10), fr(1, 2), half_reason(5, 12), fr(5, 12), fr(1, 2)))
    its.append(mcq("Which fraction is <b>less than</b> %s?" % fr(1, 2), Fc(5, 12), [Fc(4, 6), Fc(5, 8), Fc(7, 10)], e))
    e = ("%s %s %s %s A small top number like 3 can still be more than half."
         % (half_reason(3, 5), half_reason(4, 10), half_reason(6, 12), half_reason(2, 8))
         ).replace("so %s is more than" % fr(3, 5), "so <b>%s</b> is more than" % fr(3, 5))
    its.append(mcq("Which fraction is <b>greater than</b> %s?" % fr(1, 2), fr(3, 5), [fr(4, 10), fr(6, 12), fr(2, 8)], e))

    orders = [
        ([(7, 8), (1, 5), (1, 2)], "up", "%s is less than %s and %s is more than %s." % (fr(1, 5), fr(1, 2), fr(7, 8), fr(1, 2))),
        ([(1, 3), (5, 6), (1, 2)], "down", "%s is close to 1, and %s is less than %s." % (fr(5, 6), fr(1, 3), fr(1, 2))),
        ([(6, 10), (3, 10), (9, 10)], "down", "All are tenths, so compare the top numbers: 9 &gt; 6 &gt; 3."),
        ([(3, 4), (1, 10), (4, 8)], "up", "%s is close to 0. %s is exactly %s. %s is more than %s." % (fr(1, 10), fr(4, 8), fr(1, 2), fr(3, 4), fr(1, 2))),
    ]
    for fs, way, why in orders:
        its.append(order_mcq(fs, way, why))

    q = fig(letters_line_svg(8, [2, 3, 6, 7])) + "Which letter shows %s?" % fr(3, 4)
    e = "%s = %s. Count 6 eighths from 0: letter <b>C</b> is at %s. Letter A is at %s, which is a common mix-up." % (fr(3, 4), fr(6, 8), fr(6, 8), fr(2, 8))
    its.append(fixed(q, "C", e))
    q = fig(letters_line_svg(6, [1, 2, 3, 4])) + "Which letter shows %s?" % fr(1, 3)
    e = "%s = %s. Count 2 sixths from 0: letter <b>B</b> is at %s. Letter C is at %s = %s." % (fr(1, 3), fr(2, 6), fr(2, 6), fr(3, 6), fr(1, 2))
    its.append(fixed(q, "B", e))
    assert len(its) == 20, len(its)
    return {"title": "Order fractions and use benchmarks 0, 1/2 and 1", "items": its}


# ============================================================ set 5: word problems
def set_words(rnd):
    its = []

    def two(q, n1, n2, a, b, c, d, same, verb, e_core):
        s = sign(a, b, c, d)
        right = n1 if s == ">" else n2 if s == "<" else same
        e = e_core + (" So <b>%s</b> %s." % (right, verb) if s != "=" else " So <b>%s</b>." % same.lower())
        its.append(mcq(q, right, [n1, n2, same, CANT], e))

    two("Ethan ate %s of a pizza. Chloe ate %s of the same pizza. Who ate more?" % (fr(3, 8), fr(5, 8)),
        "Ethan", "Chloe", 3, 8, 5, 8, "They ate the same amount", "ate more", e_same_den(3, 8, 5, 8).replace("<b>", "").replace("</b>", ""))
    two("Mateo hiked %s of a trail in Stanley Park. Sofia hiked %s of the same trail. Who hiked farther?" % (fr(3, 4), fr(3, 5)),
        "Mateo", "Sofia", 3, 4, 3, 5, "They hiked the same distance", "hiked farther", e_same_num(3, 4, 3, 5).replace("<b>", "").replace("</b>", ""))
    two("Emma’s family cut a pizza into 8 equal slices. Owen’s family cut the same size pizza into 4 equal slices. "
        "Emma and Owen each ate 1 slice. Who ate more pizza?",
        "Emma", "Owen", 1, 8, 1, 4, "They ate the same amount", "ate more",
        "Emma ate %s and Owen ate %s. The same pizza cut into fewer slices makes bigger slices, so %s &lt; %s." % (fr(1, 8), fr(1, 4), fr(1, 8), fr(1, 4)))
    two("At the Terry Fox Run, Zara walked %s of the route. Ryan walked %s of the same route. Who walked farther?" % (fr(2, 4), fr(1, 2)),
        "Zara", "Ryan", 2, 4, 1, 2, "They walked the same distance", "walked farther",
        "Half of 4 is 2, so %s = %s." % (fr(2, 4), fr(1, 2)))
    two("Liam biked %s of the Stanley Park Seawall. Nadia biked %s of the Seawall. Who biked farther?" % (fr(2, 5), fr(7, 10)),
        "Liam", "Nadia", 2, 5, 7, 10, "They biked the same distance", "biked farther",
        "Use %s as a benchmark. %s %s" % (fr(1, 2), half_reason(2, 5), half_reason(7, 10)))
    two("Arjun painted %s of a fence. Jasleen painted %s of the same fence. Who painted more?" % (fr(4, 6), fr(4, 8)),
        "Arjun", "Jasleen", 4, 6, 4, 8, "They painted the same amount", "painted more", e_same_num(4, 6, 4, 8).replace("<b>", "").replace("</b>", ""))
    two("On Grouse Mountain, Hana skied %s of a ski run before she stopped. Lucas skied %s of the same run before he stopped. Who skied farther before stopping?"
        % (fr(1, 3), fr(1, 2)), "Hana", "Lucas", 1, 3, 1, 2, "They skied the same distance", "skied farther",
        "Both are 1 piece. Halves are bigger than thirds, so %s &lt; %s." % (fr(1, 3), fr(1, 2)))
    two("Mei planted beans in %s of a garden bed. Wei planted beans in %s of a garden bed that is the same size. Who planted more of the bed?"
        % (fr(3, 4), fr(6, 8)), "Mei", "Wei", 3, 4, 6, 8, "They planted the same amount", "planted more",
        "Cut each fourth into 2 equal parts: %s = %s." % (fr(3, 4), fr(6, 8)))
    two("Owen and Nadia take BC Ferries from Vancouver to Victoria on the same route. Owen’s ferry has gone %s of the way. "
        "Nadia’s ferry has gone %s of the way. Whose ferry has gone farther?" % (fr(5, 8), fr(3, 4)),
        "Owen’s ferry", "Nadia’s ferry", 5, 8, 3, 4, "They have gone the same distance", "has gone farther",
        "Write both in eighths: %s = %s, and 5 &lt; 6, so %s &lt; %s." % (fr(3, 4), fr(6, 8), fr(5, 8), fr(3, 4)))

    # different wholes
    q = ("Simran ate %s of a small pizza. Harjot ate %s of a large pizza. Simran says she ate more because %s &gt; %s. Is she right?"
         % (fr(1, 2), fr(1, 3), fr(1, 2), fr(1, 3)))
    e = ("The pizzas are <b>different wholes</b>. %s of a large pizza can be more than %s of a small pizza. "
         "Comparing %s and %s only works when the wholes are the same size. So: <b>not for sure</b>." % (fr(1, 3), fr(1, 2), fr(1, 2), fr(1, 3)))
    its.append(mcq(q, "Not for sure. The pizzas are different sizes.",
                   ["Yes, because %s &gt; %s." % (fr(1, 2), fr(1, 3)), "No, because %s &gt; %s." % (fr(1, 3), fr(1, 2)),
                    "Yes, because 2 is less than 3."], e))
    q = "Olivia hiked %s of a short trail near Kelowna. Noah hiked %s of a long trail near Kamloops. Who hiked farther?" % (fr(3, 4), fr(1, 2))
    e = ("The trails are <b>different wholes</b>. %s is more than %s of the same trail, but the long trail may be many kilometres longer. "
         "Without the lengths, <b>you can’t tell</b>." % (fr(3, 4), fr(1, 2)))
    its.append(mcq(q, CANT, ["Olivia", "Noah", "They hiked the same distance"], e))
    q = ("Jasleen ate %s of her sandwich. Harjot ate %s of his sandwich. Harjot’s sandwich is twice as long as Jasleen’s. Who ate more?"
         % (fr(2, 3), fr(2, 3)))
    e = ("Both ate %s, but the wholes are different. %s of a longer sandwich is more food, so <b>Harjot</b> ate more." % (fr(2, 3), fr(2, 3)))
    its.append(mcq(q, "Harjot", ["Jasleen", "They ate the same amount", CANT], e))

    # four people / four things
    def four(q, items, best, e):
        right = [n for n, f in items if f == best][0]
        its.append(mcq(q, right, [n for n, f in items], e))
    fs = [("Kai", (1, 2)), ("Leah", (3, 8)), ("Ryan", (7, 8)), ("Ava", (1, 4))]
    vals = [(n, F(*f)) for n, f in fs]
    assert max(v for n, v in vals) == F(7, 8)
    four("Four friends hiked the same trail on Vancouver Island. Kai hiked %s of it, Leah hiked %s, Ryan hiked %s and Ava hiked %s. Who hiked the farthest?"
         % tuple(fr(*f) for n, f in fs), vals, F(7, 8),
         "Use eighths: %s = %s, %s, %s, %s = %s. 7 eighths is the most, so <b>Ryan</b> hiked the farthest."
         % (fr(1, 2), fr(4, 8), fr(3, 8), fr(7, 8), fr(1, 4), fr(2, 8)))
    fs = [("Pepperoni", (2, 3)), ("Cheese", (1, 6)), ("Veggie", (1, 2)), ("Hawaiian", (5, 6))]
    vals = [(n, F(*f)) for n, f in fs]
    assert min(v for n, v in vals) == F(1, 6)
    four("After a class party, four pizzas of the same size have some left. Pepperoni has %s left, cheese has %s left, veggie has %s left and Hawaiian has %s left. "
         "Which pizza has the <b>least</b> left?" % tuple(fr(*f) for n, f in fs), vals, F(1, 6),
         "Use sixths: %s = %s, %s, %s = %s, %s. 1 sixth is the least, so <b>Cheese</b> has the least left."
         % (fr(2, 3), fr(4, 6), fr(1, 6), fr(1, 2), fr(3, 6), fr(5, 6)))

    fs = [("Kai", (5, 6)), ("Leah", (1, 6)), ("Owen", (1, 2))]
    up = [n for n, f in sorted(fs, key=lambda x: F(*x[1]))]
    assert up == ["Leah", "Owen", "Kai"]
    q = ("Kai, Leah and Owen are reading the same book. Kai has read %s of it, Leah has read %s and Owen has read %s. "
         "Order them from who has read the <b>least</b> to who has read the <b>most</b>." % (fr(5, 6), fr(1, 6), fr(1, 2)))
    e = ("Use sixths: %s = %s. 1 &lt; 3 &lt; 5, so the order is <b>Leah, Owen, Kai</b>." % (fr(1, 2), fr(3, 6)))
    its.append(mcq(q, "Leah, Owen, Kai", ["Kai, Owen, Leah", "Owen, Leah, Kai", "Leah, Kai, Owen"], e))
    q = "Ryan says %s of a cake is more than %s of the same cake because 10 &gt; 5. Is he right?" % (fr(1, 10), fr(1, 5))
    e = ("<b>No. Tenths are smaller pieces than fifths.</b> The same cake cut into 10 pieces has smaller pieces than when it is cut into 5. "
         "So %s &lt; %s." % (fr(1, 10), fr(1, 5)))
    its.append(mcq(q, "No. Tenths are smaller pieces than fifths.",
                   ["Yes. 10 is greater than 5.", "Yes. Tenths have more pieces.", "No. They are the same size."], e))
    q = "Ava’s class hiked %s of a trail in Whistler before lunch. Did they hike more than half of the trail before lunch?" % fr(4, 10)
    e = half_reason(4, 10) + " So <b>no, less than half</b>."
    its.append(mcq(q, "No, less than half", ["Yes, more than half", "Exactly half", "They hiked the whole trail"], e))
    q = "A pizza is cut into 8 equal slices. 3 slices have mushrooms. What fraction of the pizza has mushrooms?"
    e = "There are 8 equal slices in the whole pizza and 3 have mushrooms, so <b>%s</b> has mushrooms. %s has no mushrooms." % (fr(3, 8), fr(5, 8))
    its.append(mcq(q, Fc(3, 8), [Fc(5, 8), Fc(3, 5), Fc(8, 3)], e))
    q = "There are 6 canoes at a dock on the Fraser River. 3 of them are red. What fraction of the canoes are red?"
    e = "The whole set is 6 canoes and 3 are red, so <b>%s</b> of the canoes are red. (That is the same as %s.)" % (fr(3, 6), fr(1, 2))
    its.append(mcq(q, Fc(3, 6), [Fc(3, 3), Fc(6, 3), Fc(1, 6)], e))
    q = ("A trail has a sign at every %s of the way. Sofia stops for a snack at the sign for %s. Which fraction is equal to %s?"
         % (fr(1, 8), fr(4, 8), fr(4, 8)))
    e = "Half of 8 is 4, so %s = <b>%s</b>. Sofia is halfway along the trail." % (fr(4, 8), fr(1, 2))
    its.append(mcq(q, Fc(1, 2), [Fc(1, 4), Fc(4, 4), Fc(3, 4)], e))
    assert len(its) == 20, len(its)
    return {"title": "Fraction word problems", "items": its}


# ============================================================ lesson
def body_html():
    eq_fig = eq_bars_svg([(2, 1), (4, 2), (8, 4)], labels=[(1, 2), (2, 4), (4, 8)])
    sd_fig = two_bars_svg(2, 5, 4, 5, W=280)
    sn_fig = two_bars_svg(1, 4, 1, 8, W=280)
    L, R, Y = 24, 356, 54
    s = ["<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='2.5'/>" % (L, Y, R, Y, LINE)]
    for v, t in ((0, "0"), (1, "1")):
        X = L + (R - L) * v
        s.append("<line x1='%.1f' y1='%d' x2='%.1f' y2='%d' stroke='%s' stroke-width='2.5'/>" % (X, Y - 11, X, Y + 11, LINE))
        s.append(txt(X, Y + 32, t))
    Xh = (L + R) / 2
    s.append("<line x1='%.1f' y1='%d' x2='%.1f' y2='%d' stroke='%s' stroke-width='2.5'/>" % (Xh, Y - 11, Xh, Y + 11, LINE))
    s.append(sfr(Xh, Y + 30, 1, 2))
    for (a, b), col in (((1, 8), RED), ((3, 8), RED), ((5, 6), BLUE)):
        X = L + (R - L) * a / b
        s.append("<circle cx='%.1f' cy='%d' r='7' fill='%s'/>" % (X, Y, col))
        s.append(sfr(X, Y - 30, a, b, color=col))
    bm_fig = svg_wrap(380, 104, "".join(s), "number line from 0 to 1 with 1/8 and 3/8 left of one half and 5/6 right of one half")
    dw_fig = diff_bars_svg(4, 2, 260, 4, 3, 130)

    return (
        "<h2>The idea</h2>"
        "<p>A fraction names <b>equal parts</b> of a whole. The bottom number (denominator) tells how many equal parts the whole has. "
        "The top number (numerator) tells how many parts you count.</p>"
        "<p>The whole can be a shape or a <b>set</b>. If 2 of 6 counters are green, then " + fr(2, 6) + " of the set is green.</p>"
        "<h2>Equivalent fractions</h2>"
        "<p>Different fractions can show the <b>same amount</b>. Cut every part into 2 and you get twice as many parts, "
        "and twice as many are shaded.</p>"
        "<figure class='sn-fig'>" + eq_fig +
        "<figcaption>The bars are the same size and are shaded to the same place: " + fr(1, 2) + " = " + fr(2, 4) + " = " + fr(4, 8) + ".</figcaption></figure>"
        "<h2>Same denominator: compare the top numbers</h2>"
        "<p>When the bottom numbers are the same, the pieces are the same size. More pieces means more.</p>"
        "<figure class='sn-fig'>" + sd_fig +
        "<figcaption>Both are fifths. 2 fifths is less than 4 fifths, so " + fr(2, 5) + " &lt; " + fr(4, 5) + ".</figcaption></figure>"
        "<h2>Same numerator: more parts means smaller parts</h2>"
        "<p>When the top numbers are the same, you have the same number of pieces. Then look at the size of the pieces. "
        "A whole cut into <b>more</b> parts has <b>smaller</b> parts.</p>"
        "<figure class='sn-fig'>" + sn_fig +
        "<figcaption>One fourth is bigger than one eighth, so " + fr(1, 4) + " &gt; " + fr(1, 8) + ", even though 8 &gt; 4.</figcaption></figure>"
        + ex("Example", "Compare " + fr(3, 4) + " and " + fr(3, 8) + ".",
             "Both have 3 pieces. Fourths are bigger than eighths.",
             fr(3, 4) + " &gt; " + fr(3, 8))
        + "<h2>Benchmarks: 0, " + fr(1, 2) + " and 1</h2>"
        "<p>Ask: is the fraction close to 0, close to " + fr(1, 2) + " or close to 1? "
        "To check " + fr(1, 2) + ", compare the top number with <b>half</b> of the bottom number.</p>"
        "<figure class='sn-fig'>" + bm_fig +
        "<figcaption>" + fr(1, 8) + " is close to 0. Half of 8 is 4, so " + fr(3, 8) + " is less than " + fr(1, 2) + ". "
        + fr(5, 6) + " is close to 1.</figcaption></figure>"
        + ex("Example", "Order " + fr(5, 6) + ", " + fr(1, 8) + " and " + fr(3, 8) + " from least to greatest.",
             fr(1, 8) + " and " + fr(3, 8) + " are both eighths, and 1 &lt; 3. Both are less than " + fr(1, 2) + ". "
             + fr(5, 6) + " is more than " + fr(1, 2) + ".",
             fr(1, 8) + ", " + fr(3, 8) + ", " + fr(5, 6))
        + table(["When", "Try", "Example"], [
            ["Same bottom number", "Compare the top numbers", fr(3, 8) + " &lt; " + fr(5, 8)],
            ["Same top number", "Fewer parts means bigger parts", fr(2, 3) + " &gt; " + fr(2, 5)],
            ["One is below " + fr(1, 2) + ", one is above", "Benchmark " + fr(1, 2), fr(2, 5) + " &lt; " + fr(7, 10)],
            ["One is more than 1, one is less", "Benchmark 1", fr(5, 4) + " &gt; " + fr(7, 8)],
        ])
        + "<h2>Use the same whole</h2>"
        "<p>Compare fractions only when they are parts of the <b>same size whole</b>. "
        "Half of a large pizza can be more than " + fr(3, 4) + " of a small pizza.</p>"
        "<figure class='sn-fig'>" + dw_fig +
        "<figcaption>" + fr(2, 4) + " of bar A looks as big as " + fr(3, 4) + " of bar B, because bar A is a bigger whole.</figcaption></figure>"
        + "<h2>Common mistakes</h2>"
        + table(["Mistake", "What to do instead"], [
            ["Thinking " + fr(1, 8) + " &gt; " + fr(1, 4) + " because 8 &gt; 4", "A bigger bottom number means <b>smaller</b> pieces"],
            ["Counting only the white parts for the bottom number: calling 3 of 5 shaded " + fr(3, 2), "The bottom number counts <b>all</b> the equal parts: " + fr(3, 5)],
            ["Naming parts that are not equal", "A fraction needs <b>equal</b> parts"],
            ["Adding to make equivalent fractions: " + fr(1, 2) + " = " + fr(3, 4), "<b>Multiply</b> the top and bottom by the same number: " + fr(1, 2) + " = " + fr(2, 4)],
            ["Comparing parts of different-size wholes", "Make sure both fractions are of the <b>same whole</b>"],
        ])
    )


FAQ = [
    {"q": "What fractions do Grade 4 students learn in BC?",
     "a": "In the BC curriculum, Grade 4 students compare and order fractions, use models to see equal fractions such as 1/2 = 2/4, and use benchmarks such as 0, 1/2 and 1. They also connect tenths and hundredths to decimals."},
    {"q": "Why is 1/8 smaller than 1/4?",
     "a": "Both are one piece of the same whole. A whole cut into 8 equal parts has smaller parts than a whole cut into 4, so 1/8 < 1/4."},
    {"q": "What is a benchmark fraction?",
     "a": "A benchmark is an easy number to compare with, like 0, 1/2 or 1. For example, 3/8 is less than 1/2 and 5/6 is close to 1, so 3/8 < 5/6."},
    {"q": "Do fractions help with the Grade 4 FSA?",
     "a": "The Grade 4 FSA numeracy section checks how students reason with numbers. Comparing fractions with pictures and benchmarks builds that number sense."},
]


def gen():
    rnd = random.Random(34805)
    sets = [set_name(rnd), set_equiv(rnd), set_compare(rnd), set_bench(rnd), set_words(rnd)]
    for s in sets:
        assert len(s["items"]) == 20, (s["title"], len(s["items"]))
        for it in s["items"]:
            assert len(set(it["c"])) == 4, it
            assert it["q"].count("<svg") <= 1, it["q"]
    balance(sets, rnd)
    u = {
        "country": "ca-bc", "subject": "math", "grade": "grade-4", "slug": SLUG, "sort": 5,
        "updated": UPDATED, "pdf_url": "",
        "title": "Comparing and Ordering Fractions",
        "seo_title": "Grade 4 Comparing and Ordering Fractions Worksheets (BC Curriculum) – Free with Answer Key",
        "short_title": "Comparing and Ordering Fractions",
        "domain": "Number",
        "standard_code": "Grade 4: Number",
        "standard_url": "https://curriculum.gov.bc.ca/curriculum/mathematics/4/core",
        "standard_text": "Ordering and comparing fractions",
        "meta_desc": "Free Grade 4 math worksheets on comparing and ordering fractions for the BC curriculum: name fractions, equivalent fractions, same denominator or numerator, benchmarks 0, 1/2 and 1, and word problems. 100 questions with an answer key. Good FSA practice.",
        "key_big": "Same bottom number: compare the top numbers. Same top number: more parts means smaller parts.",
        "key_sub": "3/8 < 5/8, and 1/8 < 1/4. Use 0, 1/2 and 1 as benchmarks, and only compare fractions of the same whole.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }
    return mark_large(u, "(two number lines|number line|pictures A to D|two bars|two circles|bar A and bar B|3 bars)")


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, SLUG + ".json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(u, f, ensure_ascii=False, indent=1)
    print("wrote", path)
