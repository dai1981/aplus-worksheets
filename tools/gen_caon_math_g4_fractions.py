# -*- coding: utf-8 -*-
"""
CA Grade 4 Math: Fractions (Ontario Mathematics Curriculum 2020, B1.4, B1.5, B1.6, B2.7)
  python3 tools/gen_caon_math_g4_fractions.py
Halves to tenths: what the numerator and denominator mean, fractions of shapes and sets,
comparing and ordering fractions with the same numerator or the same denominator (fair shares),
counting by halves, thirds, fourths and tenths past 1 (5/4 = 1 1/4), and repeated addition of a
unit fraction (3 x 1/4 = 1/4 + 1/4 + 1/4). Canadian English; Ontario terms ("fourths", "mixed numbers").
Every choice carries its value; a wrong choice never equals the right value or another wrong one.
HTML attributes use single quotes (no backslashes in the JSON).
"""
import json, math, os, random, re
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "ca-on", "math", "grade-4")
UPDATED = "2026-11-02"
FILL = "#4fae74"      # shaded part
RED = "#d6453b"
LINE = "#2b2b2b"
WORD = {2: "halves", 3: "thirds", 4: "fourths", 5: "fifths", 6: "sixths", 7: "sevenths", 8: "eighths", 10: "tenths"}
ONE = {2: "half", 3: "third", 4: "fourth", 5: "fifth", 6: "sixth", 7: "seventh", 8: "eighth", 10: "tenth"}
NUMW = {1: "one", 2: "two", 3: "three", 4: "four", 5: "five", 6: "six", 7: "seven", 8: "eight", 9: "nine", 10: "ten"}


# ------------------------------------------------------------ numbers
def fr(a, b):
    return "<span class='fr'><span class='fn'>%s</span><span class='fd'>%s</span></span>" % (a, b)


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


def plus(k, n):
    return " + ".join([fr(1, n)] * k)


def times(k, n):
    return "%d × %s" % (k, fr(1, n))


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


def mcq_abcd(q, pos, e):
    """Choices are the picture labels A-D, in order. pos is the right one."""
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
    """Tag pictures that must print larger so their labels stay readable."""
    rx = re.compile(r"<svg (?=[^>]*aria-label='" + pattern + ")")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u


# ------------------------------------------------------------ pictures
def txt(x, y, s, size=16, anchor="middle", weight="700"):
    return ("<text x='%.1f' y='%.1f' font-size='%d' font-weight='%s' fill='%s' text-anchor='%s'>%s</text>"
            % (x, y, size, weight, LINE, anchor, s))


def sfr(x, cy, a, b, size=16):
    """Stacked fraction in SVG, centred at x, fraction bar at cy."""
    w = max(len(str(a)), len(str(b))) * size * 0.62 + 6
    return (txt(x, cy - 4, a, size) +
            "<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='1.8'/>"
            % (x - w / 2, cy, x + w / 2, cy, LINE) + txt(x, cy + size + 1, b, size))


def bar_row(x0, y, W, H, n, shaded, widths=None, sw=2.5):
    """n parts (equal unless widths given). shaded: set of part indexes."""
    s = []
    ws = widths or [W / n] * n
    x = x0
    for i, w in enumerate(ws):
        s.append("<rect x='%.1f' y='%.1f' width='%.2f' height='%d' fill='%s' stroke='%s' stroke-width='%s'/>"
                 % (x, y, w, H, FILL if i in shaded else "#fff", LINE, sw))
        x += w
    return "".join(s)


def bar_svg(n, shaded, W=260, H=46):
    return svg_wrap(W + 12, H + 12, bar_row(6, 6, W, H, n, shaded),
                    "bar split into %d equal parts with %d shaded" % (n, len(shaded)))


def pie(cx, cy, r, n, shaded, sw=2.5):
    s = []
    for i in range(n):
        a0 = math.radians(-90 + 360.0 * i / n)
        a1 = math.radians(-90 + 360.0 * (i + 1) / n)
        x0, y0 = cx + r * math.cos(a0), cy + r * math.sin(a0)
        x1, y1 = cx + r * math.cos(a1), cy + r * math.sin(a1)
        s.append("<path d='M%.1f %.1f L%.1f %.1f A%d %d 0 0 1 %.1f %.1f Z' fill='%s' stroke='%s' stroke-width='%s' stroke-linejoin='round'/>"
                 % (cx, cy, x0, y0, r, r, x1, y1, FILL if i in shaded else "#fff", LINE, sw))
    return "".join(s)


def circle_svg(n, shaded, r=60):
    d = 2 * r + 12
    return svg_wrap(d, d, pie(r + 6, r + 6, r, n, shaded), "circle split into %d equal parts with %d shaded" % (n, len(shaded)))


def grid_svg(rows, cols, shaded, cell=40):
    s = []
    for r in range(rows):
        for c in range(cols):
            i = r * cols + c
            s.append("<rect x='%d' y='%d' width='%d' height='%d' fill='%s' stroke='%s' stroke-width='2.5'/>"
                     % (6 + c * cell, 6 + r * cell, cell, cell, FILL if i in shaded else "#fff", LINE))
    return svg_wrap(cols * cell + 12, rows * cell + 12, "".join(s),
                    "rectangle split into %d equal parts with %d shaded" % (rows * cols, len(shaded)))


def counters_svg(n, k, per_row=6, r=15, sizes=None):
    """n counters, the first k green, the rest white. sizes: optional radius per counter."""
    gap = 8
    rows = (n + per_row - 1) // per_row
    cols = min(n, per_row)
    s = []
    cell = 2 * r + gap
    for i in range(n):
        row, col = divmod(i, per_row)
        cx = 6 + r + col * cell
        cy = 6 + r + row * cell
        rr = sizes[i] if sizes else r
        s.append("<circle cx='%d' cy='%d' r='%d' fill='%s' stroke='%s' stroke-width='2.2'/>"
                 % (cx, cy, rr, FILL if i < k else "#fff", LINE))
    return svg_wrap(12 + cols * 2 * r + (cols - 1) * gap, 12 + rows * 2 * r + (rows - 1) * gap, "".join(s),
                    "set of %d counters, %d green and %d white" % (n, k, n - k))


def four_bars_svg(specs, W=150, H=34):
    """Four labelled bars A-D in a 2 x 2 layout. specs: (n, shaded set, widths or None)."""
    s = []
    for i, (n, sh, ws) in enumerate(specs):
        col, row = i % 2, i // 2
        x0 = 6 + col * (W + 46)
        y0 = 6 + row * (H + 20)
        s.append(txt(x0 + 8, y0 + H / 2 + 6, "ABCD"[i], 17))
        s.append(bar_row(x0 + 22, y0, W, H, n, sh, [w * W for w in ws] if ws else None))
    return svg_wrap(6 + (W + 46) + 22 + W + 6, 2 * H + 20 + 12, "".join(s), "four pictures A to D")


def four_sets_svg(specs, r=12):
    """Four rows of counters A-D. specs: (n, k) with the first k green."""
    gap = 6
    s = []
    mx_n = max(n for n, _ in specs)
    for i, (n, k) in enumerate(specs):
        y = 6 + i * (2 * r + 12)
        s.append(txt(14, y + r + 6, "ABCD"[i], 17))
        for j in range(n):
            s.append("<circle cx='%d' cy='%d' r='%d' fill='%s' stroke='%s' stroke-width='2'/>"
                     % (34 + r + j * (2 * r + gap), y + r, r, FILL if j < k else "#fff", LINE))
    return svg_wrap(34 + mx_n * (2 * r + gap) - gap + 6, 12 + 4 * (2 * r + 12) - 12, "".join(s), "four sets of counters A to D")


def two_bars_svg(a, b, c, d, W=250, H=38):
    """Two bars of the same whole: a/b on top, c/d below, fraction labels on the left."""
    LW = 44
    s = []
    for row, (num, den) in enumerate([(a, b), (c, d)]):
        y = 6 + row * (H + 14)
        s.append(sfr(6 + LW / 2 - 4, y + H / 2, num, den))
        s.append(bar_row(6 + LW, y, W, H, den, set(range(num))))
    return svg_wrap(W + LW + 12, 2 * H + 26, "".join(s),
                    "two bars of the same size showing %d/%d and %d/%d" % (a, b, c, d))


def wholes_svg(d, k, H=36, W=200):
    """Bars that are each 1 whole, split into d parts; the first k parts (over all bars) are shaded."""
    nb = -(-k // d)
    s = []
    for b in range(nb):
        sh = set(i for i in range(d) if b * d + i < k)
        s.append(bar_row(6, 6 + b * (H + 12), W, H, d, sh))
    return svg_wrap(W + 12, nb * H + (nb - 1) * 12 + 12, "".join(s),
                    "%d bars, each 1 whole split into %d equal parts, %d parts shaded" % (nb, d, k))


def line_svg(L, d, k, W=380):
    """Number line 0..L, each whole in d equal spaces, red dot k spaces from 0."""
    Lx, R, Y = 24, W - 24, 34
    N = L * d

    def X(i):
        return Lx + (R - Lx) * i / N
    s = ["<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='2.5'/>" % (Lx, Y, R, Y, LINE)]
    for i in range(N + 1):
        whole = i % d == 0
        s.append("<line x1='%.1f' y1='%d' x2='%.1f' y2='%d' stroke='%s' stroke-width='%s'/>"
                 % (X(i), Y - (13 if whole else 8), X(i), Y + (13 if whole else 8), LINE, "2.5" if whole else "1.8"))
        if whole:
            s.append(txt(X(i), Y + 34, str(i // d), 17))
    s.append("<circle cx='%.1f' cy='%d' r='8' fill='%s'/>" % (X(k), Y, RED))
    return svg_wrap(W, Y + 44, "".join(s), "number line from 0 to %d, each whole split into %d equal spaces" % (L, d))


def unit_strip_svg(k, n, W=60, H=38):
    """k copies of the same 1/n piece in a row, each labelled, then the total bar under them."""
    s = []
    gap = 10
    for i in range(k):
        x = 6 + i * (W + gap)
        s.append(bar_row(x, 6, W, H, 1, {0}))
        s.append(sfr(x + W / 2, 6 + H + 22, 1, n, 15))
    total = 6 + k * W + (k - 1) * gap
    return svg_wrap(total + 6, 6 + H + 48, "".join(s), "%d pieces, each 1/%d" % (k, n))


UNEQ = {3: [0.2, 0.35, 0.45], 4: [0.15, 0.2, 0.25, 0.4], 5: [0.1, 0.15, 0.2, 0.25, 0.3]}


def pic_item(rnd, a, b, good, bad):
    """'Which picture shows a/b shaded?' good: spec; bad: [(spec, why)]."""
    pos = SPOTS.next(rnd)
    order = [x[0] for x in bad[:pos]] + [good] + [x[0] for x in bad[pos:]]
    letters = [L for i, L in enumerate("ABCD") if i != pos]
    why = " ".join("%s %s." % (L, d) for L, (_, d) in zip(letters, bad))
    e = ("%s needs <b>%d equal parts</b> with <b>%d</b> shaded. That is picture <b>%s</b>. %s"
         % (fr(a, b), b, a, "ABCD"[pos], why))
    return mcq_abcd(fig(four_bars_svg(order)) + "Which picture shows %s shaded?" % fr(a, b), pos, e)


def pic_sets_item(rnd, a, b, good, bad):
    """'Which set has a/b of the counters green?' good: (n, k); bad: [((n, k), why)]."""
    pos = SPOTS.next(rnd)
    order = [x[0] for x in bad[:pos]] + [good] + [x[0] for x in bad[pos:]]
    letters = [L for i, L in enumerate("ABCD") if i != pos]
    why = " ".join("%s %s." % (L, d) for L, (_, d) in zip(letters, bad))
    e = ("%s of a set means <b>%d counters in all</b> with <b>%d</b> green. That is set <b>%s</b>. %s"
         % (fr(a, b), b, a, "ABCD"[pos], why))
    return mcq_abcd(fig(four_sets_svg(order)) + "In which set are %s of the counters green?" % fr(a, b), pos, e)


# ============================================================ set 1: numerator and denominator
def e_name(n, k, what="shape", unshaded=False):
    if unshaded:
        return ("The %s has <b>%d equal parts</b>, so the denominator is %d. %d %s shaded, "
                "so %d − %d = <b>%d</b> parts are not shaded. The answer is <b>%s</b>."
                % (what, n, n, k, "part is" if k == 1 else "parts are", n, k, n - k, fr(n - k, n)))
    return ("The %s has <b>%d equal parts</b>, so the denominator (bottom number) is %d. "
            "<b>%d</b> parts are shaded, so the numerator (top number) is %d. The answer is <b>%s</b>."
            % (what, n, n, k, k, fr(k, n)))


def name_cands(k, n):
    return [Fc(n - k, n), Fc(k, n - k), Fc(n, k), Fc(k, n + 1), Fc(k + 1, n)]


def set_numden(rnd):
    SPOTS.left = []
    its = []
    # what the parts are called / how to say it
    e = ("4 equal parts are called <b>fourths</b>. Each part is one fourth, %s. Four fourths make the whole shape." % fr(1, 4))
    its.append(mcq(fig(circle_svg(4, set())) + "The circle is cut into 4 equal parts. What is each part called?",
                   "one fourth", ["one four", "one third", "four fourths"], e, rnd))
    for k, n, wrong in [(3, 10, ["three tens", "ten thirds", "three and ten"]),
                        (5, 8, ["five eights", "eight fifths", "five and eight"])]:
        e = ("Read the numerator first, then the name of the parts. %s is <b>%s %s</b>: %s of the %s equal parts."
             % (fr(k, n), NUMW[k], WORD[n], NUMW[k], NUMW[n]))
        its.append(mcq("How do you say %s in words?" % fr(k, n), "%s %s" % (NUMW[k], WORD[n]), wrong, e, rnd))

    # shaded shapes
    for kind, n, k in [("c", 3, 2), ("b", 5, 2), ("c", 4, 3), ("r", (2, 3), 5), ("b", 10, 7), ("c", 8, 3)]:
        if kind == "b":
            svg, N, what = bar_svg(n, set(range(k))), n, "bar"
        elif kind == "c":
            svg, N, what = circle_svg(n, set(range(k))), n, "circle"
        else:
            sh = set(rnd.sample(range(n[0] * n[1]), k))
            svg, N, what = grid_svg(n[0], n[1], sh), n[0] * n[1], "rectangle"
        its.append(mcq(fig(svg) + "What fraction of the %s is shaded?" % what, Fc(k, N), name_cands(k, N),
                       e_name(N, k, what), rnd))

    # meaning of numerator and denominator
    e = ("The <b>denominator</b> is the bottom number. In %s it tells you the whole is cut into <b>8 equal parts</b> (eighths)."
         % fr(3, 8))
    its.append(mcq("In %s, what does the denominator 8 tell you?" % fr(3, 8),
                   "The whole has 8 equal parts.",
                   ["8 parts are shaded.", "There are 8 wholes.", "Each part is 8 times bigger."], e, rnd))
    e = ("The <b>numerator</b> is the top number. In %s it tells you <b>5</b> of the 6 equal parts are counted."
         % fr(5, 6))
    its.append(mcq("In %s, what does the numerator 5 tell you?" % fr(5, 6),
                   "5 equal parts are counted.",
                   ["The whole has 5 parts.", "Each part is %s." % fr(1, 5), "There are 5 wholes."], e, rnd))
    e = "The denominator is the <b>bottom</b> number. In %s the denominator is <b>6</b>." % fr(4, 6)
    its.append(mcq("What is the denominator of %s?" % fr(4, 6), Nc(6), [Nc(4), Nc(10), Nc(2)], e, rnd))
    e = "The numerator is the <b>top</b> number. In %s the numerator is <b>7</b>." % fr(7, 10)
    its.append(mcq("What is the numerator of %s?" % fr(7, 10), Nc(7), [Nc(10), Nc(3), Nc(17)], e, rnd))
    e = "The numerator (top) is 2 and the denominator (bottom) is 5, so the fraction is <b>%s</b>." % fr(2, 5)
    its.append(mcq("Which fraction has a numerator of 2 and a denominator of 5?", Fc(2, 5),
                   [Fc(5, 2), Fc(2, 7), Fc(3, 5)], e, rnd))

    # not shaded
    for kind, n, k in [("b", 6, 1), ("c", 5, 3)]:
        svg = bar_svg(n, set(range(k))) if kind == "b" else circle_svg(n, set(range(k)))
        what = "bar" if kind == "b" else "circle"
        its.append(mcq(fig(svg) + "What fraction of the %s is <b>not</b> shaded?" % what, Fc(n - k, n),
                       [Fc(k, n), Fc(n - k, k), Fc(k, n - k), Fc(n, n - k)], e_name(n, k, what, unshaded=True), rnd))

    # pictures A to D
    its.append(pic_item(rnd, 3, 4, (4, {0, 1, 2}, None), [
        ((4, {0, 1, 2}, UNEQ[4]), "has 4 parts, but they are <b>not equal</b>"),
        ((4, {0}, None), "shows %s" % fr(1, 4)),
        ((5, {0, 1, 2}, None), "has 5 parts, so it shows %s" % fr(3, 5))]))
    its.append(pic_item(rnd, 2, 5, (5, {0, 1}, None), [
        ((5, {0, 1, 2}, None), "shows %s" % fr(3, 5)),
        ((5, {0, 1}, UNEQ[5]), "has 5 parts, but they are <b>not equal</b>"),
        ((7, {0, 1}, None), "has 7 parts, so it shows %s" % fr(2, 7))]))

    # unequal parts
    q = (fig(svg_wrap(272, 58, bar_row(6, 6, 260, 46, 3, {0}, [0.5 * 260, 0.25 * 260, 0.25 * 260]),
                      "bar cut into 3 parts that are not equal, 1 part shaded"))
         + "Leah says %s of this bar is shaded. Is she right?" % fr(1, 3))
    e = ("<b>No. The 3 parts are not equal.</b> Thirds must be 3 <b>equal</b> parts. "
         "The shaded part is bigger than the others. It is really %s of the bar." % fr(1, 2))
    its.append(mcq(q, "No. The parts are not equal.",
                   ["Yes. 1 of 3 parts is shaded.", "No. It shows %s." % fr(2, 3), "Yes. Each part is a third."], e, rnd))

    # one whole
    e = ("%s means 6 of the 6 equal parts, so the whole thing is counted. %s = <b>1 whole</b>." % (fr(6, 6), fr(6, 6)))
    its.append(mcq("Which fraction is equal to 1 whole?", Fc(6, 6), [Fc(1, 6), Fc(6, 1), Fc(5, 6)], e, rnd))
    assert len(its) == 20, len(its)
    return {"title": "Numerator and denominator", "items": its}


# ============================================================ set 2: fractions of shapes and sets
def set_shapes_sets(rnd):
    SPOTS.left = []
    its = []
    for rows, cols, k in [(2, 5, 4), (2, 4, 6)]:
        N = rows * cols
        sh = set(rnd.sample(range(N), k))
        its.append(mcq(fig(grid_svg(rows, cols, sh)) + "What fraction of the rectangle is shaded?", Fc(k, N),
                       name_cands(k, N), e_name(N, k, "rectangle") + " The shaded parts do not need to be side by side.", rnd))
    for n, k, per in [(6, 2, 6), (8, 3, 4), (10, 4, 5), (5, 3, 5)]:
        q = fig(counters_svg(n, k, per)) + "What fraction of the counters are green?"
        e = ("The whole is the <b>set</b> of %d counters, so the denominator is %d. <b>%d</b> are green: <b>%s</b>. "
             "Do not compare green with white (%d to %d)." % (n, n, k, fr(k, n), k, n - k))
        its.append(mcq(q, Fc(k, n), [Fc(k, n - k), Fc(n - k, n), Fc(n, k)], e, rnd))
    n, k = 8, 5
    q = fig(counters_svg(n, k, 4)) + "What fraction of the counters are <b>not</b> green?"
    e = ("There are %d counters in the set. %d are green, so %d − %d = %d are not green. The answer is <b>%s</b>."
         % (n, k, n, k, n - k, fr(n - k, n)))
    its.append(mcq(q, Fc(n - k, n), [Fc(k, n), Fc(n - k, k), Fc(k, n - k)], e, rnd))

    sizes = [22, 11, 11, 11]
    q = (fig(svg_wrap(170, 56, "".join("<circle cx='%d' cy='28' r='%d' fill='%s' stroke='%s' stroke-width='2.2'/>"
                                      % (x, r, FILL if r == 22 else "#fff", LINE) for x, r in zip([28, 76, 112, 148], sizes)),
                      "set of 4 balls, 1 big green ball and 3 small white balls"))
         + "What fraction of the balls are big?")
    e = ("In a set, <b>each object is one part</b>, even if it is bigger. There are 4 balls and 1 is big: <b>%s</b>."
         % fr(1, 4))
    its.append(mcq(q, Fc(1, 4), [Fc(1, 2), Fc(1, 3), Fc(3, 4)], e, rnd))

    W = [
        ("A bag has 5 red marbles and 3 blue marbles. What fraction of the marbles are blue?", Fc(3, 8),
         [Fc(3, 5), Fc(5, 8), Fc(8, 3)],
         "The whole set is 5 + 3 = 8 marbles. 3 are blue, so <b>%s</b> are blue. %s compares blue with red; it does not use the whole set." % (fr(3, 8), fr(3, 5))),
        ("A box has 10 pencil crayons. 3 of them are broken. What fraction of the pencil crayons are broken?", Fc(3, 10),
         [Fc(7, 10), Fc(3, 7), Fc(10, 3)],
         "There are 10 pencil crayons in the set and 3 are broken. So <b>%s</b> are broken." % fr(3, 10)),
        ("4 friends go skating. 3 of them wear mitts. What fraction of the friends wear mitts?", Fc(3, 4),
         [Fc(1, 4), Fc(4, 3), Fc(3, 1)],
         "The set is the 4 friends, so the denominator is 4. 3 wear mitts: <b>%s</b>." % fr(3, 4)),
        ("A box has 6 muffins. 5 are blueberry and the rest are bran. What fraction of the muffins are bran?", Fc(1, 6),
         [Fc(5, 6), Fc(1, 5), Fc(6, 5)],
         "6 − 5 = 1 muffin is bran. 1 out of 6 muffins: <b>%s</b>." % fr(1, 6)),
        ("Maya has 8 hockey cards. 3 of them are goalie cards. What fraction of her cards are <b>not</b> goalie cards?", Fc(5, 8),
         [Fc(3, 8), Fc(5, 3), Fc(3, 5)],
         "8 − 3 = 5 cards are not goalie cards. 5 out of 8 cards: <b>%s</b>." % fr(5, 8)),
    ]
    for q, r, c, e in W:
        its.append(mcq(q, r, c, e, rnd))

    # shade more
    for n, k, a in [(8, 3, 7), (10, 4, 9)]:
        e = ("To show %s, <b>%d</b> parts must be shaded. %d are shaded now, so shade %d − %d = <b>%d</b> more."
             % (fr(a, n), a, k, a, k, a - k))
        its.append(mcq(fig(bar_svg(n, set(range(k)))) + "How many more parts must be shaded to show %s?" % fr(a, n),
                       Nc(a - k), [Nc(a), Nc(n - k), Nc(a + k), Nc(n - a)], e, rnd))

    # pictures of sets A to D
    its.append(pic_sets_item(rnd, 3, 5, (5, 3), [
        ((8, 3), "has 8 counters, so it shows %s" % fr(3, 8)),
        ((5, 2), "shows %s green" % fr(2, 5)),
        ((8, 5), "has 8 counters, so it shows %s" % fr(5, 8))]))
    its.append(pic_sets_item(rnd, 2, 6, (6, 2), [
        ((6, 4), "shows %s green" % fr(4, 6)),
        ((8, 2), "has 8 counters, so it shows %s" % fr(2, 8)),
        ((4, 2), "has 4 counters, so it shows %s" % fr(2, 4))]))

    # whole set from a part
    for part, b in [(3, 3), (4, 2)]:
        whole = part * b
        q = fig(counters_svg(part, part, part)) + "These %d counters are %s of a set. How many counters are in the whole set?" % (part, fr(1, b))
        e = ("%s means the set has <b>%d equal groups</b>, and this is 1 group. %d groups of %d is %d × %d = <b>%d</b> counters."
             % (fr(1, b), b, b, part, b, part, whole))
        its.append(mcq(q, Nc(whole), [Nc(part + b), Nc(part), Nc(part * (b + 1)), Nc(b), Nc(part + 1)], e, rnd))

    # fraction of a set that is all of it
    e = "All 5 counters are green. 5 out of 5 is %s, which is <b>1 whole set</b>." % fr(5, 5)
    its.append(mcq(fig(counters_svg(5, 5, 5)) + "What fraction of the counters are green?", Fc(5, 5),
                   [Fc(1, 5), Fc(5, 1), Fc(4, 5)], e, rnd))
    assert len(its) == 20, len(its)
    return {"title": "Fractions of shapes and sets", "items": its}


# ============================================================ set 3: compare and order
def cmp_choices(a, b, c, d):
    lt = "%s &lt; %s" % (fr(a, b), fr(c, d))
    gt = "%s &gt; %s" % (fr(a, b), fr(c, d))
    eq = "%s = %s" % (fr(a, b), fr(c, d))
    x, y = F(a, b), F(c, d)
    right = lt if x < y else (gt if x > y else eq)
    return right, [lt, gt, eq, "You can’t compare them"]


def e_same_den(a, b, c, d):
    big, small = (fr(a, b), fr(c, d)) if a > c else (fr(c, d), fr(a, b))
    return ("Same denominator, so the parts are the <b>same size</b>. Compare the numerators: more parts is more. "
            "%s &gt; %s." % (big, small))


def e_same_num(a, b, c, d):
    big, small = (fr(a, b), fr(c, d)) if b < d else (fr(c, d), fr(a, b))
    return ("Same numerator, so you have the same number of parts. A <b>smaller denominator means bigger parts</b>. "
            "%s &gt; %s." % (big, small))


def set_compare(rnd):
    SPOTS.left = []
    its = []
    # with pictures
    for a, b, c, d in [(3, 8, 5, 8), (2, 3, 2, 5), (3, 4, 3, 10)]:
        big = F(a, b) if F(a, b) > F(c, d) else F(c, d)
        right = Fc(big.numerator, big.denominator) if (big.numerator, big.denominator) in [(a, b), (c, d)] else None
        bn, bd = (a, b) if F(a, b) > F(c, d) else (c, d)
        sn, sd = (c, d) if (bn, bd) == (a, b) else (a, b)
        e = e_same_den(a, b, c, d) if b == d else e_same_num(a, b, c, d)
        its.append(mcq(fig(two_bars_svg(a, b, c, d)) + "The bars are the same size. Which fraction is greater?",
                       Fc(bn, bd), [Fc(sn, sd), "They are equal", "You can’t tell"], e, rnd))
    # symbols
    for a, b, c, d in [(4, 6, 5, 6), (7, 10, 3, 10), (1, 4, 1, 8), (3, 5, 3, 4), (2, 10, 2, 6)]:
        right, ch = cmp_choices(a, b, c, d)
        e = e_same_den(a, b, c, d) if b == d else e_same_num(a, b, c, d)
        its.append(mcq("Compare. Choose &lt;, &gt; or =.", right, ch, e, rnd))
    # greatest / least
    e = ("All the numerators are 3, so look at the denominators. The <b>smallest</b> denominator (4) gives the biggest parts. "
         "<b>%s</b> is the greatest." % fr(3, 4))
    its.append(mcq("Which fraction is the <b>greatest</b>?", Fc(3, 4), [Fc(3, 10), Fc(3, 8), Fc(3, 5)], e, rnd))
    e = ("All the denominators are 8, so the parts are the same size. The <b>smallest</b> numerator is the least: <b>%s</b>."
         % fr(2, 8))
    its.append(mcq("Which fraction is the <b>least</b>?", Fc(2, 8), [Fc(7, 8), Fc(5, 8), Fc(4, 8)], e, rnd))
    # ordering
    s = lambda fs: ", ".join(fr(a, b) for a, b in fs)
    o1 = [(1, 10), (1, 5), (1, 3)]
    e = ("Same numerator. The <b>biggest</b> denominator is the <b>smallest</b> fraction, so start with %s. "
         "Least to greatest: %s." % (fr(1, 10), s(o1)))
    its.append(mcq("Order from least to greatest: %s" % s([(1, 3), (1, 10), (1, 5)]), s(o1),
                   [s(o1[::-1]), s([(1, 5), (1, 3), (1, 10)]), s([(1, 3), (1, 10), (1, 5)])], e, rnd))
    o2 = [(2, 8), (2, 6), (2, 4)]
    e = ("Same numerator, 2. Eighths are smaller than sixths, and sixths are smaller than fourths. "
         "Least to greatest: %s." % s(o2))
    its.append(mcq("Order from least to greatest: %s" % s([(2, 4), (2, 8), (2, 6)]), s(o2),
                   [s(o2[::-1]), s([(2, 6), (2, 8), (2, 4)]), s([(2, 4), (2, 8), (2, 6)])], e, rnd))
    o3 = [(9, 10), (6, 10), (4, 10)]
    e = "Same denominator, so compare the numerators: 9 &gt; 6 &gt; 4. Greatest to least: %s." % s(o3)
    its.append(mcq("Order from greatest to least: %s" % s([(4, 10), (9, 10), (6, 10)]), s(o3),
                   [s(o3[::-1]), s([(6, 10), (9, 10), (4, 10)]), s([(9, 10), (4, 10), (6, 10)])], e, rnd))
    # fair-share scenarios (B1.5)
    its.append(mcq("Group A: 3 pizzas are shared equally by 4 friends. Group B: 3 pizzas are shared equally by 5 friends. "
                   "In which group does each friend get more pizza?",
                   "Group A", ["Group B, because 5 is more", "They get the same", "You can’t tell"],
                   "Group A: each friend gets %s of a pizza. Group B: each gets %s. Same numerator, and fewer sharers "
                   "means bigger shares, so %s &gt; %s. <b>Group A</b> gets more." % (fr(3, 4), fr(3, 5), fr(3, 4), fr(3, 5)), rnd))
    its.append(mcq("Group A: 6 friends share 5 subs equally. Group B: 6 friends share 4 subs equally. "
                   "In which group does each friend get more?",
                   "Group A", ["Group B", "They get the same", "You can’t tell"],
                   "Group A: each friend gets %s of a sub. Group B: each gets %s. Same denominator, so compare numerators: "
                   "%s &gt; %s. <b>Group A</b> gets more." % (fr(5, 6), fr(4, 6), fr(5, 6), fr(4, 6)), rnd))
    its.append(mcq("2 granola bars are shared equally by 3 friends. How much does each friend get?",
                   Fc(2, 3), [Fc(3, 2), Fc(1, 3), Fc(2, 5)],
                   "Cut each bar into thirds. Each friend gets 1 third from each of the 2 bars: <b>%s</b> of a bar. "
                   "The number of sharers is the denominator." % fr(2, 3), rnd))
    its.append(mcq("Which share is bigger: 2 pancakes shared by 3 friends, or 2 pancakes shared by 8 friends?",
                   "Shared by 3 friends", ["Shared by 8 friends", "They are the same", "You can’t tell"],
                   "Shared by 3: %s of a pancake each. Shared by 8: %s each. Same numerator, so the smaller denominator "
                   "is bigger: %s &gt; %s." % (fr(2, 3), fr(2, 8), fr(2, 3), fr(2, 8)), rnd))
    # true statements / misconception
    st = lambda a, b, c, d: "%s &gt; %s" % (fr(a, b), fr(c, d))
    e = ("Check each one. With the same numerator, a bigger denominator means a <b>smaller</b> fraction. "
         "%s is true, because fifths are bigger than tenths." % st(4, 5, 4, 10))
    its.append(mcq("Which one is <b>true</b>?", st(4, 5, 4, 10),
                   [st(4, 10, 4, 5), st(3, 8, 5, 8), st(1, 6, 1, 2)], e, rnd))
    e = ("With the same denominator, the parts are the same size, so the fraction with more parts is greater. "
         "%s is true." % st(7, 10, 3, 10))
    its.append(mcq("Which one is <b>true</b>?", st(7, 10, 3, 10),
                   [st(3, 10, 7, 10), st(1, 8, 1, 4), st(2, 6, 2, 3)], e, rnd))
    its.append(mcq("Arjun says %s is greater than %s because 8 is greater than 4. Is he right?" % (fr(1, 8), fr(1, 4)),
                   "No. %s is greater." % fr(1, 4), ["Yes. 8 is greater than 4.", "No. They are equal.", "Yes. Eighths are bigger."],
                   "A whole cut into 8 parts has <b>smaller</b> parts than a whole cut into 4 parts. So %s &gt; %s." % (fr(1, 4), fr(1, 8)), rnd))
    assert len(its) == 20, len(its)
    return {"title": "Compare and order fractions", "items": its}


# ============================================================ set 4: count by fractions past 1
def set_counting(rnd):
    SPOTS.left = []
    its = []
    # bars with more than one whole
    for d, k in [(4, 5), (2, 5), (4, 7), (10, 13)]:
        w, r = divmod(k, d)
        e = ("Each bar is 1 whole cut into %d equal parts. <b>%d %s</b> are shaded, which is %s. %d %s make 1 whole, "
             "and %d more %s %s. So %s = <b>%s</b>."
             % (d, k, WORD[d], fr(k, d), d, WORD[d], r, ONE[d] if r == 1 else WORD[d], "is " + fr(r, d),
                fr(k, d), mx(w, r, d)))
        its.append(mcq(fig(wholes_svg(d, k)) + "Each bar is 1 whole. How much is shaded?", Mc(w, r, d),
                       [Fc(k, 2 * d), Fc(r, d), Mc(w, r, k), Nc(k), Mc(w, r + 1, d) if r + 1 < d else Mc(w + 1, r, d)], e, rnd))
    # counting sequences (to 10)
    seqs = [
        ("fourths", [fr(3, 4), "1", mx(1, 1, 4)], Mc(1, 2, 4), [Mc(1, 1, 5), Mc(2, 1, 4), Nc(2)],
         "Add %s each time. %s + %s = <b>%s</b>." % (fr(1, 4), mx(1, 1, 4), fr(1, 4), mx(1, 2, 4))),
        ("halves", ["3", mx(3, 1, 2)], Nc(4), [Mc(4, 1, 2), Mc(3, 1, 4), Nc(5)],
         "Add %s each time. %s + %s = <b>4</b>, because 2 halves make 1 whole." % (fr(1, 2), mx(3, 1, 2), fr(1, 2))),
        ("thirds", [mx(1, 1, 3), mx(1, 2, 3)], Nc(2), [Mc(2, 1, 3), Mc(1, 1, 3), Nc(3)],
         "Add %s each time. %s + %s = %s, which is <b>2</b>. 3 thirds make a whole." % (fr(1, 3), mx(1, 2, 3), fr(1, 3), mx(1, 3, 3))),
        ("tenths", [mx(2, 8, 10), mx(2, 9, 10)], Nc(3), [Mc(3, 1, 10), Nc(4), Mc(3, 9, 10)],
         "Add %s each time. %s + %s = %s, which is <b>3</b>." % (fr(1, 10), mx(2, 9, 10), fr(1, 10), mx(2, 10, 10))),
    ]
    for name, terms, right, wrong, e in seqs:
        its.append(mcq("Count by %s. What comes next?<br>%s, <b>?</b>" % (name, ", ".join(terms)), right, wrong, e, rnd))
    e = ("Count by tenths: %s, %s, %s, 10. Each step adds %s." % (mx(9, 7, 10), mx(9, 8, 10), mx(9, 9, 10), fr(1, 10)))
    its.append(mcq("Count by tenths. What number is missing?<br>%s, <b>?</b>, %s, 10" % (mx(9, 7, 10), mx(9, 9, 10)),
                   Mc(9, 8, 10), [Mc(9, 7, 10), Mc(10, 8, 10), Mc(9, 6, 10)], e, rnd))
    # how many
    e = "4 fourths make 1 whole. 2 wholes need 4 + 4 = <b>8 fourths</b>, so %s = 2." % fr(8, 4)
    its.append(mcq("How many fourths make 2 wholes?", Nc(8), [Nc(4), Nc(6), Nc(2)], e, rnd))
    e = "2 halves make 1 whole. 10 wholes need 10 × 2 = <b>20 halves</b>."
    its.append(mcq("You count by halves from 0 to 10. How many halves do you count?", Nc(20), [Nc(10), Nc(5), Nc(12)], e, rnd))
    # more than 1
    e = ("A fraction is more than 1 when the numerator is <b>greater</b> than the denominator. "
         "%s is 4 thirds, and 3 thirds make 1, so %s is more than 1. %s is exactly 1." % (fr(4, 3), fr(4, 3), fr(3, 3)))
    its.append(mcq("Which fraction is <b>more</b> than 1 whole?", Fc(4, 3), [Fc(3, 4), Fc(3, 3), Fc(1, 3)], e, rnd))
    # improper -> mixed
    for a, d, wrong in [(5, 4, [Mc(1, 1, 5), Mc(5, 1, 4), Mc(4, 1, 5)]),
                        (7, 2, [Mc(2, 1, 2), Mc(7, 1, 2), Mc(2, 1, 7)]),
                        (7, 3, [Mc(2, 1, 7), Mc(3, 1, 3), Fc(3, 7)]),
                        (13, 10, [Mc(1, 3, 13), Mc(3, 1, 10), Mc(13, 1, 10)])]:
        w, r = divmod(a, d)
        e = ("%d %s make 1 whole. %s is %d %s: that is <b>%d whole%s</b> (%d %s) and <b>%d %s</b> left over. So %s = <b>%s</b>."
             % (d, WORD[d], fr(a, d), a, WORD[d], w, "" if w == 1 else "s", w * d, WORD[d], r, ONE[d] if r == 1 else WORD[d],
                fr(a, d), mx(w, r, d)))
        its.append(mcq("%s = ?" % fr(a, d), Mc(w, r, d), wrong, e, rnd))
    # mixed -> improper
    for w, r, d, wrong in [(1, 3, 4, [Fc(4, 4), Fc(13, 4), Fc(3, 4)]),
                           (2, 1, 2, [Fc(3, 2), Fc(21, 2), Fc(1, 2)])]:
        a = w * d + r
        e = ("Each whole is %d %s. %d whole%s = %d %s. Add %d more: %d + %d = %d. So %s = <b>%s</b>."
             % (d, WORD[d], w, "" if w == 1 else "s", w * d, WORD[d], r, w * d, r, a, mx(w, r, d), fr(a, d)))
        its.append(mcq("%s = ?" % mx(w, r, d), Fc(a, d), wrong, e, rnd))
    # number lines
    for L, d, k in [(2, 4, 7), (3, 3, 8)]:
        w, r = divmod(k, d)
        e = ("Each whole has <b>%d equal spaces</b>, so each space is %s. The dot is %d spaces from 0: "
             "that is %s = <b>%s</b>." % (d, fr(1, d), k, fr(k, d), mx(w, r, d)))
        its.append(mcq(fig(line_svg(L, d, k)) + "Count by %s. What number is at the red dot?" % WORD[d], Mc(w, r, d),
                       [Fc(k, L * d), Mc(w, r - 1, d), Mc(w, r, L * d), Mc(w + 1, r, d)], e, rnd))
    assert len(its) == 20, len(its)
    return {"title": "Count by fractions past 1", "items": its}


# ============================================================ set 5: repeated addition and word problems
def set_words(rnd):
    SPOTS.left = []
    its = []
    # repeated addition = whole number x unit fraction
    e = ("%s is %s added <b>3 times</b>. That is 3 groups of %s: <b>%s</b>." % (plus(3, 4), fr(1, 4), fr(1, 4), times(3, 4)))
    its.append(mcq("Which multiplication is the same as %s?" % plus(3, 4), (times(3, 4), F(3, 4)),
                   [(times(4, 3), F(4, 3)), ("3 × 4", F(12)), ("3 + %s" % fr(1, 4), F(13, 4))], e, rnd))
    e = ("%s means %s. Three fourths is <b>%s</b>. The parts are still fourths, so the denominator stays 4."
         % (times(3, 4), plus(3, 4), fr(3, 4)))
    its.append(mcq(fig(unit_strip_svg(3, 4)) + "%s = ?" % times(3, 4), Fc(3, 4), [Fc(3, 12), Fc(4, 3), Fc(1, 12)], e, rnd))
    e = ("%s means 5 copies of %s: 5 eighths, or <b>%s</b>. Do not multiply the denominator." % (times(5, 8), fr(1, 8), fr(5, 8)))
    its.append(mcq("%s = ?" % times(5, 8), Fc(5, 8), [Fc(5, 40), Fc(8, 5), Fc(6, 8)], e, rnd))
    e = "%s means add %s <b>4 times</b>: %s = %s." % (times(4, 10), fr(1, 10), plus(4, 10), fr(4, 10))
    its.append(mcq("Which addition is the same as %s?" % times(4, 10), (plus(4, 10), F(4, 10)),
                   [(plus(3, 10), F(3, 10)), (plus(5, 10), F(5, 10)), ("%s + 4" % fr(1, 10), F(41, 10))], e, rnd))
    e = ("%s is 6 fourths, %s. 4 fourths make 1 whole, and 2 fourths are left. So it is <b>%s</b>."
         % (times(6, 4), fr(6, 4), mx(1, 2, 4)))
    its.append(mcq("%s = ?" % times(6, 4), Mc(1, 2, 4), [Fc(6, 24), Mc(1, 1, 4), Mc(6, 1, 4)], e, rnd))
    e = ("%s is 7 thirds, %s. 6 thirds make 2 wholes, and 1 third is left. So it is <b>%s</b>."
         % (times(7, 3), fr(7, 3), mx(2, 1, 3)))
    its.append(mcq("%s = ?" % times(7, 3), Mc(2, 1, 3), [Fc(7, 21), Mc(2, 1, 7), Fc(3, 7)], e, rnd))
    e = "%s is 4 fifths, so you need <b>4</b> copies of %s: 4 × %s = %s." % (fr(4, 5), fr(1, 5), fr(1, 5), fr(4, 5))
    its.append(mcq("? × %s = %s" % (fr(1, 5), fr(4, 5)), Nc(4), [Nc(5), Nc(20), Nc(1)], e, rnd))

    # word problems
    W = [
        ("Hana skates %s of a lap around the rink, 3 times. How much of a lap does she skate in all?" % fr(1, 4),
         Fc(3, 4, " lap"), [Fc(3, 12, " lap"), Nc(3, " laps"), Mc(3, 1, 4, " laps")],
         "%s = %s = <b>%s of a lap</b>." % (times(3, 4), plus(3, 4), fr(3, 4))),
        ("A hockey game has 3 periods of the same length. Ethan watches 2 periods. What fraction of the game does he watch?",
         Fc(2, 3), [Fc(3, 2), Fc(1, 3), Fc(2, 5)],
         "The game has 3 equal parts, so the denominator is 3. He watches 2 of them: <b>%s</b>." % fr(2, 3)),
        ("A tourtière is cut into 8 equal pieces. The family eats 5 pieces. What fraction of the tourtière do they eat?",
         Fc(5, 8), [Fc(3, 8), Fc(8, 5), Fc(5, 13)],
         "There are 8 equal pieces, so the denominator is 8. They eat 5 pieces: <b>%s</b>." % fr(5, 8)),
        ("A pizza is cut into 6 equal slices. Chloe’s family eats 4 slices. What fraction of the pizza is <b>left</b>?",
         Fc(2, 6), [Fc(4, 6), Fc(2, 4), Fc(1, 6)],
         "6 − 4 = <b>2 slices</b> are left out of 6 equal slices. That is <b>%s</b> of the pizza." % fr(2, 6)),
        ("A ringette team has 10 players. 7 wear blue helmets and the rest wear white helmets. What fraction of the players wear white helmets?",
         Fc(3, 10), [Fc(7, 10), Fc(3, 7), Fc(10, 3)],
         "10 − 7 = 3 players wear white helmets. 3 out of 10 players: <b>%s</b>." % fr(3, 10)),
        ("Mei uses %s cup of flour for each batch of maple cookies. She makes 5 batches. How much flour does she use?" % fr(1, 3),
         Mc(1, 2, 3, " cups"), [Fc(5, 15, " cup"), Mc(5, 1, 3, " cups"), Mc(1, 1, 3, " cups")],
         "%s = %s cups. 3 thirds make 1 cup, and 2 thirds are left: <b>%s cups</b>." % (times(5, 3), fr(5, 3), mx(1, 2, 3))),
        ("Each lap of the school field is %s km. Owen runs 5 laps in the Terry Fox Run. How far does he run?" % fr(1, 4),
         Mc(1, 1, 4, " km"), [Fc(5, 20, " km"), Mc(5, 1, 4, " km"), Mc(1, 1, 5, " km")],
         "%s = %s km. 4 fourths make 1 km, and 1 fourth is left: <b>%s km</b>." % (times(5, 4), fr(5, 4), mx(1, 1, 4))),
        ("Noah drinks 3 bottles of water on a canoe trip. Each bottle holds %s L. How much water does he drink?" % fr(1, 2),
         Mc(1, 1, 2, " L"), [Fc(3, 6, " L"), Mc(3, 1, 2, " L"), Fc(2, 3, " L")],
         "%s = %s L. 2 halves make 1 L, and 1 half is left: <b>%s L</b>." % (times(3, 2), fr(3, 2), mx(1, 1, 2))),
        ("Kai has granola bars cut into fourths. He eats 5 fourths. How many granola bars does he eat?",
         Mc(1, 1, 4, " bars"), [Fc(5, 8, " bar"), Fc(1, 4, " bar"), Nc(5, " bars")],
         "4 fourths make 1 whole bar. 5 fourths is 1 whole bar and %s more: <b>%s bars</b>." % (fr(1, 4), mx(1, 1, 4))),
        ("Zoe says %s = %s. Is she right?" % (times(3, 5), fr(3, 15)),
         "No. It is %s." % fr(3, 5), ["Yes. 3 × 5 = 15.", "No. It is %s." % fr(5, 3), "No. It is %s." % fr(1, 15)],
         "%s means %s. The parts stay fifths, so the answer is <b>%s</b>. Only the number of parts changes." % (times(3, 5), plus(3, 5), fr(3, 5))),
        ("Arjun ran %s km. Sofia ran %s km. Who ran farther?" % (fr(3, 10), fr(3, 4)),
         "Sofia", ["Arjun, because 10 is greater", "They ran the same distance", "You can’t tell"],
         "Same numerator, 3. Fourths are bigger than tenths, so %s &gt; %s. <b>Sofia</b> ran farther." % (fr(3, 4), fr(3, 10))),
        ("Ava’s group of 4 shares 3 subs equally. Liam’s group of 4 shares 2 subs equally. In which group does each person get more?",
         "Ava’s group", ["Liam’s group", "They get the same", "You can’t tell"],
         "Ava’s group: %s of a sub each. Liam’s group: %s each. Same denominator, and 3 &gt; 2, so <b>Ava’s group</b> gets more." % (fr(3, 4), fr(2, 4))),
        ("A sugar bush worker fills %s of a barrel with sap each hour. How much of a barrel is filled after 12 hours?" % fr(1, 10),
         Mc(1, 2, 10, " barrels"), [Fc(12, 100, " barrel"), Fc(2, 10, " barrel"), Mc(12, 1, 10, " barrels")],
         "%s = %s. 10 tenths make 1 barrel, and 2 tenths are left: <b>%s barrels</b>." % (times(12, 10), fr(12, 10), mx(1, 2, 10))),
    ]
    assert len(W) == 13, len(W)
    for q, right, cands, e in W:
        its.append(mcq(q, right, cands, e, rnd))
    assert len(its) == 20, len(its)
    return {"title": "Repeated addition and word problems", "items": its}


# ============================================================ lesson
def body_html():
    lab = svg_wrap(272, 100, bar_row(6, 6, 260, 46, 4, {0, 1, 2}) +
                   sfr(136, 80, 3, 4, 16), "bar split into 4 equal parts with 3 shaded, labelled 3/4")
    parts_fig = ("<figure class='sn-fig'>" + lab +
                 "<figcaption>4 equal parts, 3 shaded: " + fr(3, 4) + " (three fourths). The numerator 3 counts the shaded parts. "
                 "The denominator 4 tells how many equal parts make the whole.</figcaption></figure>")
    set_fig = ("<figure class='sn-fig'>" + counters_svg(5, 2, 5) +
               "<figcaption>A set of 5 counters. 2 are green, so " + fr(2, 5) + " of the set is green.</figcaption></figure>")
    cmp1 = ("<figure class='sn-fig'>" + two_bars_svg(2, 3, 2, 5) +
            "<figcaption>Same numerator: thirds are bigger than fifths, so " + fr(2, 3) + " &gt; " + fr(2, 5) + ".</figcaption></figure>")
    count_fig = ("<figure class='sn-fig'>" + wholes_svg(4, 5) +
                 "<figcaption>5 fourths are shaded. 4 fourths make 1 whole, so " + fr(5, 4) + " = " + mx(1, 1, 4) + ".</figcaption></figure>")
    line_fig = ("<figure class='sn-fig'>" + line_svg(2, 4, 5) +
                "<figcaption>Counting by fourths: the dot is 5 fourths from 0, at " + mx(1, 1, 4) + ".</figcaption></figure>")
    mult_fig = ("<figure class='sn-fig'>" + unit_strip_svg(3, 4) +
                "<figcaption>3 pieces of " + fr(1, 4) + ": " + plus(3, 4) + " = " + times(3, 4) + " = " + fr(3, 4) + ".</figcaption></figure>")
    return (
        "<h2>Numerator and denominator</h2>"
        "<p>A fraction names <b>equal parts</b> of a whole. The <b>denominator</b> (bottom number) tells how many equal parts make the whole. "
        "The <b>numerator</b> (top number) tells how many of those parts you are counting.</p>"
        + parts_fig +
        "<p>Halves, thirds, fourths, fifths, sixths, eighths and tenths: the name comes from the denominator.</p>"
        "<h2>Fractions of a set</h2>"
        "<p>The whole can be a <b>set</b> of objects. The denominator is the number of objects in the set.</p>"
        + set_fig +
        ex("Example", "A bag has 5 red marbles and 3 blue marbles. What fraction are blue?",
           "The whole set is 5 + 3 = 8 marbles. 3 are blue.", fr(3, 8))
        + "<h2>Compare and order</h2>"
        "<p><b>Same denominator:</b> the parts are the same size, so more parts is more. " + fr(5, 8) + " &gt; " + fr(3, 8) + ".</p>"
        "<p><b>Same numerator:</b> you have the same number of parts, so look at their size. "
        "A <b>bigger denominator means smaller parts</b>.</p>"
        + cmp1 +
        ex("Example", "3 pizzas are shared by 4 friends. 3 pizzas are shared by 5 friends. Which share is bigger?",
           "Each friend gets " + fr(3, 4) + " or " + fr(3, 5) + ". Fewer sharers means bigger shares.", fr(3, 4) + " &gt; " + fr(3, 5))
        + "<h2>Count by fractions past 1</h2>"
        "<p>Count by fourths: " + ", ".join([fr(1, 4), fr(2, 4), fr(3, 4), "1", mx(1, 1, 4), mx(1, 2, 4)]) +
        ". After 4 fourths, you have 1 whole. A whole number and a fraction together, like " + mx(1, 1, 4) +
        ", is a <b>mixed number</b>.</p>"
        + count_fig + line_fig +
        "<h2>Adding the same unit fraction</h2>"
        "<p>Adding the same unit fraction again and again is multiplication.</p>"
        + mult_fig +
        ex("Example", "Owen runs " + fr(1, 4) + " km, 5 times. How far does he run?",
           times(5, 4) + " = " + fr(5, 4) + ". 4 fourths make 1 km, and 1 fourth is left.", mx(1, 1, 4) + " km")
        + "<h2>Common mistakes</h2>"
        + table(["Mistake", "What to do instead"], [
            ["Thinking " + fr(1, 8) + " is bigger than " + fr(1, 4) + " because 8 is bigger than 4",
             "A bigger denominator means <b>smaller</b> parts, so " + fr(1, 8) + " &lt; " + fr(1, 4)],
            ["Mixing up the numbers: writing " + fr(4, 3) + " for 3 of 4 equal parts", "Parts counted on top, parts in the whole on the bottom: " + fr(3, 4)],
            ["Calling unequal parts “thirds” or “fourths”", "Fractions need <b>equal</b> parts"],
            ["In a set of 5 red and 3 blue, writing " + fr(3, 5) + " for blue", "Use the whole set: " + fr(3, 8)],
            [times(3, 4) + " = " + fr(3, 12), "Only the number of parts changes: " + fr(3, 4)],
            ["Writing " + fr(5, 4) + " as " + mx(1, 1, 5), "4 fourths make 1, and 1 fourth is left: " + mx(1, 1, 4)],
        ])
    )


FAQ = [
    {"q": "What fractions do Grade 4 students learn in Ontario?",
     "a": "In the Ontario math curriculum, Grade 4 students work with fractions from halves to tenths. They name fractions of shapes and sets, compare fractions with the same numerator or denominator, count by fractions past 1 (like 5/4 = 1 1/4) and see that 3 × 1/4 = 1/4 + 1/4 + 1/4."},
    {"q": "What is the difference between the numerator and the denominator?",
     "a": "The denominator (bottom number) tells how many equal parts make the whole. The numerator (top number) tells how many of those parts you are counting, so 3/4 means 3 of 4 equal parts."},
    {"q": "Why is 1/4 bigger than 1/8?",
     "a": "Cut the same pizza into 4 pieces and into 8 pieces. With fewer pieces each piece is bigger, so 1/4 is bigger than 1/8, even though 8 is a bigger number."},
    {"q": "How do you explain 3 × 1/4 to a Grade 4 student?",
     "a": "3 × 1/4 means 3 groups of 1/4, or 1/4 + 1/4 + 1/4. That is 3 fourths, 3/4; the denominator stays 4 because the pieces are still fourths."},
]


def gen():
    rnd = random.Random(44807)
    SPOTS.left = []
    sets = [set_numden(rnd), set_shapes_sets(rnd), set_compare(rnd), set_counting(rnd), set_words(rnd)]
    for s in sets:
        assert len(s["items"]) == 20, (s["title"], len(s["items"]))
        cnt = [0, 0, 0, 0]
        for it in s["items"]:
            assert len(set(it["c"])) == 4, it
            cnt[it["a"]] += 1
        assert cnt == [5, 5, 5, 5], (s["title"], cnt)
    return {
        "country": "ca-on", "subject": "math", "grade": "grade-4", "slug": "fractions", "sort": 7,
        "updated": UPDATED, "pdf_url": "",
        "title": "Grade 4 Fractions",
        "seo_title": "Grade 4 Fractions Worksheets: Free Math Practice with Answer Key (Ontario Curriculum)",
        "short_title": "Fractions",
        "domain": "Number",
        "standard_code": "Grade 4: B1.4",
        "standard_url": "https://www.dcp.edu.gov.on.ca/en/curriculum/elementary-mathematics",
        "standard_text": "Represent fractions from halves to tenths using drawings, tools, and standard fractional notation, and explain the meanings of the denominator and the numerator",
        "meta_desc": "Free Grade 4 math worksheets on fractions for the Ontario curriculum: numerator and denominator, fractions of shapes and sets, comparing fractions, counting past 1 with mixed numbers, and 3 × 1/4. 100 questions with an answer key.",
        "key_big": "The denominator tells how many equal parts make the whole. The numerator tells how many parts you count.",
        "key_sub": "A bigger denominator means smaller parts, so 1/8 < 1/4. Count by fourths past 1: 3/4, 1, 1 1/4. And 3 × 1/4 = 1/4 + 1/4 + 1/4 = 3/4.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, "fractions.json")
    mark_large(u, "(number line|two bars|four pictures|four sets|[0-9]+ bars|[0-9]+ pieces)")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(u, f, ensure_ascii=False, indent=1)
    print("wrote", path)
