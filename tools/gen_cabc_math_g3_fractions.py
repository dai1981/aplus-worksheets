# -*- coding: utf-8 -*-
"""
CA-BC Grade 3 Math: Fractions (BC Mathematics Curriculum, Grade 3 Content: "Fraction concepts")
  python3 tools/gen_cabc_math_g3_fractions.py
Equal parts, naming fractions of shapes (halves to tenths), fractions of sets, comparing unit fractions,
fractions on a number line and word problems. Canadian English, BC contexts, "fourths".
Every choice carries its value; a wrong choice never equals the right value or another wrong one.
HTML attributes use single quotes (no backslashes in the JSON).
"""
import json, math, os, random, re
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "ca-bc", "math", "grade-3")
UPDATED = "2026-11-02"
FILL = "#4fae74"      # shaded part
RED = "#d6453b"
LINE = "#2b2b2b"
WORD = {2: "halves", 3: "thirds", 4: "fourths", 5: "fifths", 6: "sixths", 8: "eighths", 10: "tenths"}
ONE = {2: "half", 3: "third", 4: "fourth", 5: "fifth", 6: "sixth", 8: "eighth", 10: "tenth"}
NUMW = {1: "one", 2: "two", 3: "three", 4: "four", 5: "five", 6: "six", 7: "seven", 8: "eight", 9: "nine", 10: "ten"}


# ------------------------------------------------------------ numbers
def fr(a, b):
    return "<span class='fr'><span class='fn'>%s</span><span class='fd'>%s</span></span>" % (a, b)


def Fc(a, b, unit=""):
    return (fr(a, b) + unit, F(a, b))


def Nc(n, unit=""):
    return ("%d%s" % (n, unit), F(n))


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
def txt(x, y, s, size=16, anchor="middle", weight="700", fill=LINE):
    return ("<text x='%.1f' y='%.1f' font-size='%d' font-weight='%s' fill='%s' text-anchor='%s'>%s</text>"
            % (x, y, size, weight, fill, anchor, s))


def sfr(x, y, a, b, size=15):
    """Stacked fraction drawn in SVG, centred at x. y is the numerator baseline."""
    w = size * 0.62 * max(len(str(a)), len(str(b))) + 4
    return (txt(x, y, a, size) +
            "<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='1.5'/>"
            % (x - w / 2, y + 4, x + w / 2, y + 4, LINE) + txt(x, y + size + 4, b, size))


def bar_row(x0, y, W, H, n, shaded, widths=None, sw=2.5):
    """n parts (equal unless widths given, as shares of W). shaded: set of part indexes."""
    s = []
    ws = [w * W for w in widths] if widths else [W / n] * n
    x = x0
    for i, w in enumerate(ws):
        s.append("<rect x='%.1f' y='%.1f' width='%.2f' height='%d' fill='%s' stroke='%s' stroke-width='%s'/>"
                 % (x, y, w, H, FILL if i in shaded else "#fff", LINE, sw))
        x += w
    return "".join(s)


def bar_svg(n, shaded, W=260, H=50, widths=None, label=None):
    return svg_wrap(W + 12, H + 12, bar_row(6, 6, W, H, n, shaded, widths),
                    label or "bar split into %d equal parts with %d shaded" % (n, len(shaded)))


def pie(cx, cy, r, n, shaded, sw=2.5, fracs=None):
    """Circle cut into n parts (equal unless fracs given)."""
    if n == 1:
        return ("<circle cx='%.1f' cy='%.1f' r='%d' fill='%s' stroke='%s' stroke-width='%s'/>"
                % (cx, cy, r, FILL if 0 in shaded else "#fff", LINE, sw))
    fs = fracs or [1.0 / n] * n
    s, acc = [], 0.0
    for i in range(n):
        a0 = math.radians(-90 + 360.0 * acc)
        acc += fs[i]
        a1 = math.radians(-90 + 360.0 * acc)
        x0, y0 = cx + r * math.cos(a0), cy + r * math.sin(a0)
        x1, y1 = cx + r * math.cos(a1), cy + r * math.sin(a1)
        large = 1 if fs[i] > 0.5 else 0
        s.append("<path d='M%.1f %.1f L%.1f %.1f A%d %d 0 %d 1 %.1f %.1f Z' fill='%s' stroke='%s' stroke-width='%s' stroke-linejoin='round'/>"
                 % (cx, cy, x0, y0, r, r, large, x1, y1, FILL if i in shaded else "#fff", LINE, sw))
    return "".join(s)


def circle_svg(n, shaded, r=62, fracs=None, label=None):
    d = 2 * r + 12
    return svg_wrap(d, d, pie(r + 6, r + 6, r, n, shaded, fracs=fracs),
                    label or "circle split into %d equal parts with %d shaded" % (n, len(shaded)))


GRIDS = {4: (2, 2), 6: (2, 3), 8: (2, 4), 10: (2, 5)}


def grid_svg(n, shaded, cell=40):
    rows, cols = GRIDS[n]
    s = []
    for r in range(rows):
        for c in range(cols):
            i = r * cols + c
            s.append("<rect x='%d' y='%d' width='%d' height='%d' fill='%s' stroke='%s' stroke-width='2.5'/>"
                     % (6 + c * cell, 6 + r * cell, cell, cell, FILL if i in shaded else "#fff", LINE))
    return svg_wrap(cols * cell + 12, rows * cell + 12, "".join(s),
                    "rectangle split into %d equal parts with %d shaded" % (n, len(shaded)))


def shape_svg(n, shaded, kind):
    if kind == "circle":
        return circle_svg(n, shaded)
    if kind == "grid":
        return grid_svg(n, shaded)
    return bar_svg(n, shaded)


SHAPE = {"circle": "circle", "grid": "rectangle", "bar": "bar"}

UNEQ = {2: [0.36, 0.64], 3: [0.2, 0.35, 0.45], 4: [0.15, 0.2, 0.25, 0.4], 5: [0.1, 0.15, 0.2, 0.25, 0.3],
        6: [0.1, 0.22, 0.12, 0.2, 0.16, 0.2], 8: [0.08, 0.16, 0.1, 0.14, 0.12, 0.18, 0.1, 0.12]}


def four_bars_svg(specs, W=150, H=34):
    """Four labelled bars A-D in a 2 x 2 layout. specs: (n, shaded set, widths or None)."""
    s = []
    for i, (n, sh, ws) in enumerate(specs):
        col, row = i % 2, i // 2
        x0 = 6 + col * (W + 46)
        y0 = 6 + row * (H + 20)
        s.append(txt(x0 + 8, y0 + H / 2 + 6, "ABCD"[i], 17))
        s.append(bar_row(x0 + 22, y0, W, H, n, sh, ws))
    return svg_wrap(2 * (W + 22) + 24 + 6, 2 * H + 20 + 12, "".join(s), "four bar pictures A to D")


def four_pies_svg(specs, r=34):
    """Four labelled circles A-D in a row. specs: (n, shaded set, fracs or None)."""
    s = []
    cw = 2 * r + 34
    for i, (n, sh, fs) in enumerate(specs):
        x0 = 6 + i * cw
        s.append(txt(x0 + 8, 6 + r + 6, "ABCD"[i], 17))
        s.append(pie(x0 + 24 + r, 6 + r, r, n, sh, sw=2, fracs=fs))
    return svg_wrap(4 * cw - 10 + 12, 2 * r + 12, "".join(s), "four circle pictures A to D")


def counters_svg(n, k, groups=None, R=15, step=38, gap=20):
    """n counters; the first k are shaded. groups: list of group sizes (drawn with a box around each)."""
    gs = groups or [n]
    s, x, idx = [], 6, 0
    pad = 6 if groups else 0
    for g in gs:
        gx = x
        x += pad
        for j in range(g):
            cx = x + R + j * step
            s.append("<circle cx='%.1f' cy='%.1f' r='%d' fill='%s' stroke='%s' stroke-width='2.5'/>"
                     % (cx, 6 + pad + R, R, FILL if idx < k else "#fff", LINE))
            idx += 1
        x += 2 * R + (g - 1) * step + pad
        if groups:
            s.append("<rect x='%.1f' y='6' width='%.1f' height='%d' rx='10' fill='none' stroke='#8a8a8a' stroke-width='2' stroke-dasharray='6 4'/>"
                     % (gx, x - gx, 2 * R + 2 * pad))
        x += gap if groups else 0
    W = x - (gap if groups else 0) + 6
    lab = ("%d counters in %d equal groups, %d shaded" % (n, len(gs), k)) if groups else ("%d counters, %d shaded" % (n, k))
    return svg_wrap(W, 2 * R + 2 * pad + 12, "".join(s), lab)


def four_counters_svg(specs, R=11, step=27):
    """Four labelled rows of counters A-D in a 2 x 2 layout. specs: (shaded, white)."""
    s = []
    mx = max(a + b for a, b in specs)
    cw = 26 + 2 * R + (mx - 1) * step + 24
    for i, (a, b) in enumerate(specs):
        col, row = i % 2, i // 2
        x0 = 6 + col * cw
        y0 = 6 + row * (2 * R + 16)
        s.append(txt(x0 + 8, y0 + R + 6, "ABCD"[i], 17))
        for j in range(a + b):
            s.append("<circle cx='%.1f' cy='%.1f' r='%d' fill='%s' stroke='%s' stroke-width='2'/>"
                     % (x0 + 26 + R + j * step, y0 + R, R, FILL if j < a else "#fff", LINE))
    return svg_wrap(2 * cw - 24 + 12, 2 * (2 * R) + 16 + 12, "".join(s), "four groups of counters A to D")


def line1_svg(d, k=None, letters=None, W=380):
    """Number line 0..1 in d equal spaces. k: red dot. letters: {tick index: letter}."""
    L, R = 24, W - 24
    Y = 46 if letters else 30
    s = ["<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='2.5'/>" % (L, Y, R, Y, LINE)]

    def X(i):
        return L + (R - L) * i / d
    for i in range(d + 1):
        end = i in (0, d)
        s.append("<line x1='%.1f' y1='%d' x2='%.1f' y2='%d' stroke='%s' stroke-width='%s'/>"
                 % (X(i), Y - (13 if end else 9), X(i), Y + (13 if end else 9), LINE, "2.5" if end else "2"))
    s.append(txt(X(0), Y + 34, "0", 17) + txt(X(d), Y + 34, "1", 17))
    if k is not None:
        s.append("<circle cx='%.1f' cy='%d' r='8' fill='%s'/>" % (X(k), Y, RED))
    for i, Lt in sorted((letters or {}).items()):
        s.append("<circle cx='%.1f' cy='%d' r='6' fill='%s'/>" % (X(i), Y, RED))
        s.append(txt(X(i), Y - 18, Lt, 17))
    return svg_wrap(W, Y + 44, "".join(s), "number line from 0 to 1 in %d equal spaces" % d)


def two_bars_svg(n1, k1, n2, k2, W=260, H=40):
    s = bar_row(6, 6, W, H, n1, set(range(k1))) + bar_row(6, 6 + H + 14, W, H, n2, set(range(k2)))
    return svg_wrap(W + 12, 2 * H + 26, s, "two bars of the same size, top bar %d of %d parts shaded, bottom bar %d of %d parts shaded"
                    % (k1, n1, k2, n2))


def abcd_item(rnd, good, bad, draw, q, lead):
    """Picture-choice item. good: spec; bad: [(spec, why)]. draw(list of 4 specs) -> svg."""
    pos = SPOTS.next(rnd)
    order = [x[0] for x in bad[:pos]] + [good] + [x[0] for x in bad[pos:]]
    letters = [L for i, L in enumerate("ABCD") if i != pos]
    why = " ".join("%s %s." % (L, d) for L, (_, d) in zip(letters, bad))
    e = "%s That is picture <b>%s</b>. %s" % (lead, "ABCD"[pos], why)
    return mcq_abcd(fig(draw(order)) + q, pos, e)


# ============================================================ set 1: equal parts
def set_equal(rnd):
    SPOTS.left = []
    its = []
    # how many equal parts (mistake: counting the lines)
    for n, kind in [(5, "bar"), (6, "circle"), (8, "grid"), (10, "bar")]:
        e = ("Count the <b>parts</b>, not the lines. The %s has <b>%d equal parts</b>. "
             "(It has only %d lines inside, because the ends are not cuts.)" % (SHAPE[kind], n, n - 1))
        if kind != "bar":
            e = "Count the <b>parts</b>, not the lines. The %s has <b>%d equal parts</b>." % (SHAPE[kind], n)
        its.append(mcq(fig(shape_svg(n, set(), kind)) + "How many equal parts does the %s have?" % SHAPE[kind],
                       Nc(n), [Nc(n - 1), Nc(n + 1), Nc(n // 2), Nc(2 * n)], e, rnd))
    # what are the parts called
    for n, kind, wrong in [(2, "circle", ["twos", "thirds", "fourths"]), (3, "bar", ["threes", "halves", "fourths"]),
                           (4, "grid", ["fours", "thirds", "fifths"]), (8, "circle", ["eights", "sixths", "fourths"])]:
        e = "There are <b>%d equal parts</b>. %d equal parts are called <b>%s</b>." % (n, n, WORD[n])
        if n == 2:
            e += " We say halves, not “twos”."
        its.append(mcq(fig(shape_svg(n, set(), kind)) + "The %s is cut into equal parts. What are the parts called?" % SHAPE[kind],
                       WORD[n], wrong, e, rnd))
    # is the shaded part 1/n?
    for kind, n, eq in [("bar", 4, True), ("bar", 4, False), ("circle", 3, True), ("circle", 2, False),
                        ("grid", 6, True), ("circle", 4, False)]:
        if kind == "bar":
            svg = bar_svg(n, {0}, widths=None if eq else UNEQ[n], label="bar split into %d parts with 1 shaded" % n)
        elif kind == "circle":
            svg = circle_svg(n, {0}, fracs=None if eq else UNEQ[n], label="circle split into %d parts with 1 shaded" % n)
        else:
            svg = grid_svg(n, {0})
        yes = "Yes. It has %d equal parts." % n
        no = "No. The parts are not equal."
        if eq:
            right, cands = yes, [no, "No. It shows %s." % fr(1, n + 1), "No. It shows %s." % fr(1, n - 1)]
            e = ("All %d parts are the <b>same size</b>, and 1 part is shaded. So the shaded part is %s."
                 % (n, fr(1, n)))
        else:
            right, cands = no, ["Yes. It has %d parts." % n, "Yes. One part is shaded.", "No. It shows %s." % fr(1, n + 1)]
            e = ("A fraction needs <b>equal parts</b>. These %d parts are different sizes, so the shaded part is <b>not</b> %s."
                 % (n, fr(1, n)))
        its.append(mcq(fig(svg) + "Is the shaded part %s of the %s?" % (fr(1, n), SHAPE[kind]), right, cands, e, rnd))
    # which picture shows equal parts / fourths / sixths
    its.append(abcd_item(rnd, (3, set(), None),
                         [((3, set(), UNEQ[3]), "has 3 parts, but they are different sizes"),
                          ((4, set(), UNEQ[4]), "has 4 parts of different sizes"),
                          ((2, set(), UNEQ[2]), "has 2 parts of different sizes")],
                         four_bars_svg, "Which bar is cut into <b>equal</b> parts?",
                         "Equal parts are all the <b>same size</b>."))
    its.append(abcd_item(rnd, (4, set(), None),
                         [((4, set(), UNEQ[4]), "has 4 parts, but they are different sizes"),
                          ((3, set(), UNEQ[3]), "has 3 parts of different sizes"),
                          ((2, set(), UNEQ[2]), "has 2 parts of different sizes")],
                         four_pies_svg, "Which circle is cut into <b>equal</b> parts?",
                         "Equal parts are all the <b>same size</b>."))
    its.append(abcd_item(rnd, (4, set(), None),
                         [((4, set(), UNEQ[4]), "has 4 parts, but they are not equal, so they are not fourths"),
                          ((3, set(), None), "has 3 equal parts, which are thirds"),
                          ((5, set(), None), "has 5 equal parts, which are fifths")],
                         four_bars_svg, "Which bar is cut into <b>fourths</b>?",
                         "Fourths are <b>4 equal parts</b>."))
    its.append(abcd_item(rnd, (6, set(), None),
                         [((6, set(), UNEQ[6]), "has 6 parts, but they are not equal, so they are not sixths"),
                          ((5, set(), None), "has 5 equal parts, which are fifths"),
                          ((8, set(), None), "has 8 equal parts, which are eighths")],
                         four_pies_svg, "Which circle is cut into <b>sixths</b>?",
                         "Sixths are <b>6 equal parts</b>."))
    # folding paper
    its.append(mcq("Nadia folds a square piece of paper in half. Then she folds it in half again. "
                   "She opens it. How many equal parts are there?", Nc(4), [Nc(2), Nc(3), Nc(8)],
                   "The first fold makes 2 equal parts. The second fold cuts each of those in half: 2 × 2 = <b>4 equal parts</b>.", rnd))
    its.append(mcq("Wei folds a paper strip in half, then in half again. What is each part called?",
                   "one fourth", ["one half", "one third", "one eighth"],
                   "Two folds in half make <b>4 equal parts</b>. Each part is <b>one fourth</b>, %s." % fr(1, 4), rnd))
    assert len(its) == 20, len(its)
    return {"title": "Equal parts", "items": its}


# ============================================================ set 2: name fractions of shapes
def shaded_cands(k, n):
    return [Fc(n - k, n), Fc(k, n - k) if n - k > 0 else None, Fc(n, k), Fc(k, n + 1), Fc(k + 1, n) if k + 1 < n else None,
            Fc(1, n), Nc(k)]


def set_names(rnd):
    SPOTS.left = []
    its = []
    for k, n, kind in [(1, 2, "circle"), (2, 3, "bar"), (3, 4, "grid"), (2, 5, "bar"), (5, 6, "circle"),
                       (3, 8, "grid"), (7, 10, "bar"), (4, 6, "grid"), (1, 5, "circle")]:
        e = ("The %s has <b>%d equal parts</b>, so the bottom number is %d. <b>%d</b> %s shaded, so the top number is %d. "
             "The answer is %s." % (SHAPE[kind], n, n, k, "part is" if k == 1 else "parts are", k, fr(k, n)))
        if n - k > 0 and k > 1:
            e += " (%s compares shaded parts with white parts. The bottom number must be <b>all</b> the parts.)" % fr(k, n - k)
        cands = [Fc(2, 1), Fc(1, 3), Fc(2, 2)] if (k, n) == (1, 2) else shaded_cands(k, n)
        its.append(mcq(fig(shape_svg(n, set(range(k)), kind)) + "What fraction of the %s is shaded?" % SHAPE[kind],
                       Fc(k, n), cands, e, rnd))
    # not shaded
    for k, n, kind in [(3, 8, "circle"), (4, 10, "grid"), (1, 4, "bar")]:
        w = n - k
        e = ("There are %d equal parts and %d %s shaded. %d − %d = <b>%d</b> parts are <b>not</b> shaded, so the answer is %s."
             % (n, k, "is" if k == 1 else "are", n, k, w, fr(w, n)))
        its.append(mcq(fig(shape_svg(n, set(range(k)), kind)) + "What fraction of the %s is <b>not</b> shaded?" % SHAPE[kind],
                       Fc(w, n), [Fc(k, n), Fc(w, k), Fc(n, w), Fc(w, n + 1), Fc(1, n)], e, rnd))
    # which picture shows k/n
    for k, n, bad in [
        (3, 4, [((4, {0}, None), "shows %s" % fr(1, 4)),
                ((7, {0, 1, 2}, None), "has 3 shaded and 4 white parts, so it shows %s" % fr(3, 7)),
                ((4, {0, 1, 2}, UNEQ[4]), "has 4 parts, but they are <b>not equal</b>")]),
        (2, 5, [((5, {0, 1, 2}, None), "shows %s" % fr(3, 5)),
                ((5, {0, 1}, UNEQ[5]), "has 5 parts, but they are <b>not equal</b>"),
                ((7, {0, 1}, None), "has 2 shaded and 5 white parts, so it shows %s" % fr(2, 7))]),
        (5, 8, [((8, {0, 1, 2}, None), "shows %s" % fr(3, 8)),
                ((6, {0, 1, 2, 3, 4}, None), "has 6 parts, so it shows %s" % fr(5, 6)),
                ((8, {0, 1, 2, 3, 4}, UNEQ[8]), "has 8 parts, but they are <b>not equal</b>")]),
    ]:
        its.append(abcd_item(rnd, (n, set(range(k)), None), bad, four_bars_svg,
                             "Which picture shows %s shaded?" % fr(k, n),
                             "%s needs <b>%d equal parts</b> with <b>%d</b> shaded." % (fr(k, n), n, k)))
    # fraction words
    for k, n, wrong in [(2, 3, [(3, 2), (2, 5), (1, 3)]), (3, 10, [(10, 3), (3, 7), (1, 10)])]:
        e = "“%s %s” means <b>%d</b> parts out of <b>%d</b> equal parts: %s. The number of parts in the whole goes on the bottom." % (
            NUMW[k], WORD[n], k, n, fr(k, n))
        its.append(mcq("Which fraction is <b>%s %s</b>?" % (NUMW[k], WORD[n]), Fc(k, n), [Fc(a, b) for a, b in wrong], e, rnd))
    # all shaded
    its.append(mcq(fig(grid_svg(6, set(range(6)))) + "What fraction of the rectangle is shaded?", Fc(6, 6),
                   [Fc(1, 6), Fc(6, 1), Fc(5, 6)],
                   "All <b>6</b> of the 6 equal parts are shaded: %s. That is the whole rectangle, 1 whole." % fr(6, 6), rnd))
    # what the numbers mean
    its.append(mcq("In the fraction %s, what does the <b>8</b> tell you?" % fr(3, 8),
                   "The whole has 8 equal parts.", ["8 parts are shaded.", "There are 8 wholes.", "Each part is 8 cm long."],
                   "The bottom number tells how many <b>equal parts make the whole</b>. In %s, the whole has 8 equal parts." % fr(3, 8), rnd))
    its.append(mcq("In the fraction %s, what does the <b>3</b> tell you?" % fr(3, 5),
                   "3 of the parts are counted.", ["The whole has 3 parts.", "3 parts are not shaded.", "There are 3 wholes."],
                   "The top number tells how many parts we <b>count</b> (for example, how many are shaded). In %s, 3 of the 5 equal parts are counted." % fr(3, 5), rnd))
    assert len(its) == 20, len(its)
    return {"title": "Name fractions of shapes", "items": its}


# ============================================================ set 3: fractions of sets
def set_sets(rnd):
    SPOTS.left = []
    its = []
    for k, n in [(1, 3), (2, 4), (3, 5), (4, 6), (5, 8)]:
        e = ("There are <b>%d counters</b> in the set, so the bottom number is %d. <b>%d</b> %s green, so the answer is %s."
             % (n, n, k, "is" if k == 1 else "are", fr(k, n)))
        if k > 1:
            e += " Do not write %s: the bottom number is <b>all</b> the counters, not just the white ones." % fr(k, n - k)
        its.append(mcq(fig(counters_svg(n, k)) + "What fraction of the counters are green?", Fc(k, n),
                       [Fc(k, n - k), Fc(n - k, n), Fc(n, k), Fc(k, n + 1), Fc(1, n)], e, rnd))
    for k, n in [(3, 7), (2, 10)]:
        w = n - k
        e = ("%d − %d = <b>%d</b> counters are white (not green) out of %d counters. The answer is %s." % (n, k, w, n, fr(w, n)))
        its.append(mcq(fig(counters_svg(n, k)) + "What fraction of the counters are <b>not</b> green?", Fc(w, n),
                       [Fc(k, n), Fc(w, k), Fc(n, w), Fc(w, n + 1)], e, rnd))
    for q, k, n, e in [
        ("Leah has 5 apples. 2 are red and 3 are green. What fraction of the apples are red?", 2, 5,
         "There are 5 apples in all, so the bottom number is 5. 2 are red: <b>%s</b>." % fr(2, 5)),
        ("A bag has 10 marbles. 7 are blue. What fraction of the marbles are <b>not</b> blue?", 3, 10,
         "10 − 7 = 3 marbles are not blue, out of 10 marbles: <b>%s</b>." % fr(3, 10)),
        ("Ryan has 8 hockey cards. 3 of them are Vancouver Canucks cards. What fraction of his cards are Canucks cards?", 3, 8,
         "There are 8 cards in all, so the bottom number is 8. 3 are Canucks cards: <b>%s</b>." % fr(3, 8)),
    ]:
        o = n - k
        its.append(mcq(q, Fc(k, n), [Fc(k, o), Fc(o, n), Fc(n, k), Fc(o, k)], e, rnd))
    its.append(mcq("Simran picks 7 flowers. 4 are pink and the rest are yellow. What fraction of the flowers are yellow?",
                   Fc(3, 7), [Fc(4, 7), Fc(3, 4), Fc(7, 3)],
                   "7 − 4 = 3 flowers are yellow, out of 7 flowers in all: <b>%s</b>." % fr(3, 7), rnd))
    its.append(mcq("Jasleen has 6 eggs. %s of them are brown. How many eggs are brown?" % fr(1, 3),
                   Nc(2, " eggs"), [Nc(3, " eggs"), Nc(4, " eggs"), Nc(6, " eggs")],
                   "%s of 6 means 6 shared into <b>3 equal groups</b>: 2, 2 and 2. So <b>2 eggs</b> are brown. "
                   "(3 is the number of groups, not the number in each group.)" % fr(1, 3), rnd))
    # one equal group out of the set
    for n, g in [(12, 3), (10, 5)]:
        per = n // g
        e = ("The %d counters are in <b>%d equal groups</b>. One group out of %d is shaded, so the shaded part is <b>%s</b>. "
             "(%d is the number of counters in each group, not the number of groups.)" % (n, g, g, fr(1, g), per))
        its.append(mcq(fig(counters_svg(n, per, [per] * g)) + "What fraction of the counters is shaded?", Fc(1, g),
                       [Fc(1, per), Fc(per, g) if per != g else None, Fc(g, n), Fc(1, n), Fc(per - 1, n)], e, rnd))
    # find 1/g of n with a picture
    for n, g in [(8, 2), (12, 4), (9, 3), (10, 2)]:
        per = n // g
        e = ("Make <b>%d equal groups</b> of the %d counters. Each group has %d counters. So %s of %d is <b>%d</b>."
             % (g, n, per, fr(1, g), n, per))
        cands = [Nc(g), Nc(n), Nc(n - per), Nc(n + g), Nc(n - g), Nc(per + 1)]
        q = fig(counters_svg(n, per, [per] * g)) + "What is %s of %d?" % (fr(1, g), n)
        if (n, g) == (10, 2):
            q = fig(counters_svg(n, 0)) + "What is %s of %d counters?" % (fr(1, g), n)
            e = "Share the %d counters into <b>2 equal groups</b>: 5 and 5. So %s of 10 is <b>5</b>." % (n, fr(1, 2))
            cands = [Nc(2), Nc(10), Nc(8), Nc(20)]
        its.append(mcq(q, Nc(per), cands, e, rnd))
    # which picture shows k/n of the counters
    its.append(abcd_item(rnd, (3, 1), [((3, 4), "has 3 green and 4 white, so it shows %s" % fr(3, 7)),
                                       ((1, 3), "shows %s" % fr(1, 4)),
                                       ((4, 3), "has 4 green out of 7, so it shows %s" % fr(4, 7))],
                         four_counters_svg, "Which picture shows %s of the counters green?" % fr(3, 4),
                         "%s needs <b>4 counters</b> in all with <b>3</b> green." % fr(3, 4)))
    its.append(abcd_item(rnd, (2, 3), [((3, 2), "shows %s" % fr(3, 5)),
                                       ((2, 5), "has 2 green and 5 white, so it shows %s" % fr(2, 7)),
                                       ((2, 2), "has 4 counters, so it shows %s" % fr(2, 4))],
                         four_counters_svg, "Which picture shows %s of the counters green?" % fr(2, 5),
                         "%s needs <b>5 counters</b> in all with <b>2</b> green." % fr(2, 5)))
    assert len(its) == 20, len(its)
    return {"title": "Fractions of sets", "items": its}


# ============================================================ set 4: compare unit fractions
def cmp_choices(a, b, c, d):
    lt = "%s &lt; %s" % (fr(a, b), fr(c, d))
    gt = "%s &gt; %s" % (fr(a, b), fr(c, d))
    eq = "%s = %s" % (fr(a, b), fr(c, d))
    x, y = F(a, b), F(c, d)
    right = lt if x < y else (gt if x > y else eq)
    return right, [lt, gt, eq, "You can’t compare them"]


def set_compare(rnd):
    SPOTS.left = []
    its = []
    for n1, n2 in [(2, 4), (8, 3), (5, 10), (6, 4)]:
        big, small = min(n1, n2), max(n1, n2)
        e = ("The top bar has %d parts and the bottom bar has %d parts. <b>More parts means smaller parts</b>, "
             "so %s is bigger than %s." % (n1, n2, fr(1, big), fr(1, small)))
        its.append(mcq(fig(two_bars_svg(n1, 1, n2, 1)) + "The bars are the same size. Which shaded part is bigger?",
                       Fc(1, big), [Fc(1, small), "They are the same size", "You can’t tell"], e, rnd))
    for b, d in [(8, 4), (3, 5), (2, 3), (10, 6), (5, 4)]:
        right, ch = cmp_choices(1, b, 1, d)
        x, y = (b, d) if b < d else (d, b)
        e = ("Both fractions have 1 on top. A whole cut into %d equal parts has bigger parts than a whole cut into %d equal parts. "
             "So %s." % (x, y, right))
        if b == 8 and d == 4:
            e += " 8 is bigger than 4, but %s is <b>smaller</b> than %s." % (fr(1, 8), fr(1, 4))
        its.append(mcq("Compare the fractions. Choose &lt;, &gt; or =.", right, ch, e, rnd))
    for want, opts in [("largest", [6, 3, 10, 4]), ("smallest", [2, 5, 8, 3]), ("smallest", [4, 10, 6, 5])]:
        ans = min(opts) if want == "largest" else max(opts)
        e = ("A unit fraction has 1 on top. The <b>%s</b> bottom number means the %s parts. %s is the %s."
             % ("smallest" if want == "largest" else "biggest", "biggest" if want == "largest" else "smallest", fr(1, ans), want))
        its.append(mcq("Which unit fraction is the <b>%s</b>?" % want, Fc(1, ans), [Fc(1, x) for x in opts if x != ans], e, rnd))
    for ds in [(4, 2, 8), (5, 10, 3)]:
        inc = sorted(ds, reverse=True)       # least to greatest: biggest denominator first
        dec = sorted(ds)
        s = lambda o: ", ".join(fr(1, x) for x in o)
        mid = [inc[0], inc[2], inc[1]]
        e = ("Order from least to greatest. The <b>biggest</b> bottom number is the <b>smallest</b> fraction, so start with %s. "
             "The order is %s." % (fr(1, inc[0]), s(inc)))
        its.append(mcq("Order from least to greatest: %s" % s(ds), s(inc), [s(dec), s(mid), s([dec[1], dec[0], dec[2]])], e, rnd))
    for n1, n2, food, a1, a2 in [(3, 6, "pizza", "Ava", "Lucas"), (8, 5, "pan of lasagna", "Owen", "Simran"),
                                 (4, 10, "cake", "Ji-woo", "Mateo")]:
        big = a1 if n1 < n2 else a2
        nb, ns = min(n1, n2), max(n1, n2)
        other = a2 if big == a1 else a1
        e = ("A %s shared by %d people gives bigger pieces than one shared by %d people. %s &gt; %s, so <b>%s’s group</b> gets bigger pieces."
             % (food, nb, ns, fr(1, nb), fr(1, ns), big))
        its.append(mcq("%s’s group of %d shares a %s equally. %s’s group of %d shares the same size %s equally. "
                       "Whose group gets bigger pieces?" % (a1, n1, food, a2, n2, food),
                       "%s’s group" % big, ["%s’s group, because %d is bigger" % (other, ns), "They get the same size",
                                            "You can’t tell"], e, rnd))
    for good, bads in [((8, 4), [(2, 8), (3, 6), (4, 10)]), ((6, 2), [(3, 5), (2, 4), (5, 10)]),
                       ((10, 3), [(4, 6), (2, 3), (3, 8)])]:
        assert good[0] > good[1] and all(b[0] < b[1] for b in bads)
        st = lambda p: "%s &lt; %s" % (fr(1, p[0]), fr(1, p[1]))
        e = ("Check each one. A bigger bottom number means a <b>smaller</b> unit fraction. %s is true, because %d equal parts are smaller than %d equal parts."
             % (st(good), good[0], good[1]))
        its.append(mcq("Which one is <b>true</b>?", st(good), [st(b) for b in bads], e, rnd))
    assert len(its) == 20, len(its)
    return {"title": "Compare unit fractions", "items": its}


# ============================================================ set 5: number line and word problems
def set_line_words(rnd):
    SPOTS.left = []
    its = []
    for d, k in [(4, 1), (3, 2), (5, 3), (6, 5), (8, 3), (10, 7)]:
        e = ("The line from 0 to 1 has <b>%d equal spaces</b>, so each space is %s. The dot is <b>%d</b> %s from 0: <b>%s</b>. "
             "Count the spaces, not the tick marks." % (d, fr(1, d), k, "space" if k == 1 else "spaces", fr(k, d)))
        its.append(mcq(fig(line1_svg(d, k)) + "What fraction is at the red dot?", Fc(k, d),
                       [Fc(k, d + 1), Fc(k + 1, d) if k + 1 < d else None, Fc(d - k, d), Fc(1, k) if k > 1 else None,
                        Fc(k + 1, d + 1), Nc(k)], e, rnd))
    for d, k in [(10, 6), (8, 4)]:
        pos = SPOTS.next(rnd)
        lo, hi = list(range(1, k)), list(range(k + 1, d))
        pick_lo, pick_hi = [], []
        if pos >= 1:
            pick_lo.append(k - 1)              # counted the 0 tick as 1
        if pos <= 2:
            pick_hi.append(k + 1)              # counted one tick too many
        rest_lo = [t for t in lo if t not in pick_lo]
        rest_hi = [t for t in hi if t not in pick_hi]
        pick_lo += rnd.sample(rest_lo, pos - len(pick_lo))
        pick_hi += rnd.sample(rest_hi, 3 - pos - len(pick_hi))
        ticks = sorted(pick_lo + pick_hi + [k])
        assert ticks.index(k) == pos and len(set(ticks)) == 4
        lt = {t: "ABCD"[i] for i, t in enumerate(ticks)}
        e = ("The line has %d equal spaces, so each space is %s. Start at 0 and count <b>%d spaces</b>. "
             "The letter there is <b>%s</b>. Do not count the tick mark at 0." % (d, fr(1, d), k, lt[k]))
        its.append(mcq_abcd(fig(line1_svg(d, None, lt)) + "Which letter is at %s?" % fr(k, d), pos, e))
    W = []

    def add(q, right, cands, e):
        W.append((q, right, cands, e))

    add("A pizza is cut into 8 equal slices. Liam eats 3 slices. What fraction of the pizza does he eat?",
        Fc(3, 8), [Fc(5, 8), Fc(3, 5), Fc(8, 3)],
        "There are 8 equal slices, so the bottom number is 8. Liam eats 3: <b>%s</b>." % fr(3, 8))
    add("A cedar fence has 10 equal boards. Owen paints 7 of them. What fraction of the fence is painted?",
        Fc(7, 10), [Fc(3, 10), Fc(7, 3), Fc(10, 7)],
        "7 of the 10 equal boards are painted: <b>%s</b>." % fr(7, 10))
    add("A hiking trail in Stanley Park has 4 equal parts. Chloe’s family walks 3 parts. What fraction of the trail is <b>left</b>?",
        Fc(1, 4), [Fc(3, 4), Fc(1, 3), Fc(4, 3)],
        "4 − 3 = <b>1 part</b> is left out of 4 equal parts: %s of the trail." % fr(1, 4))
    add("Ava eats %s of a sandwich. Sofia eats %s of the same size sandwich. Who eats more?" % (fr(1, 3), fr(1, 6)),
        "Ava", ["Sofia", "They eat the same", "You can’t tell"],
        "Thirds are bigger than sixths, because a sandwich cut into 3 equal parts has bigger parts than one cut into 6. "
        "%s &gt; %s, so <b>Ava</b> eats more." % (fr(1, 3), fr(1, 6)))
    add("Arjun says %s of a pizza is more than %s of the same pizza, because 8 is more than 4. Is he right?" % (fr(1, 8), fr(1, 4)),
        "No. %s is more." % fr(1, 4), ["Yes. 8 is more than 4.", "No. They are the same.", "Yes. Eighths are bigger."],
        "A pizza cut into 8 equal slices has smaller slices than a pizza cut into 4. So %s &gt; %s." % (fr(1, 4), fr(1, 8)))
    add("Mei cuts a cake into 4 pieces. The pieces are different sizes. She says each piece is %s. Is she right?" % fr(1, 4),
        "No. The pieces are not equal.", ["Yes. There are 4 pieces.", "No. Each piece is %s." % fr(1, 3), "Yes. Each piece is one part."],
        "Fourths must be <b>4 equal parts</b>. The pieces are different sizes, so they are not fourths.")
    add("It is raining in Vancouver. 8 children play soccer, and 3 of them wear rain jackets. What fraction of the children wear rain jackets?",
        Fc(3, 8), [Fc(3, 5), Fc(5, 8), Fc(8, 3)],
        "There are 8 children in all, so the bottom number is 8. 3 wear rain jackets: <b>%s</b>. (%s compares jackets with no jackets.)"
        % (fr(3, 8), fr(3, 5)))
    add("Ethan sees 6 bald eagles. %s of them sit in a cedar tree. How many eagles sit in the tree?" % fr(1, 2),
        Nc(3, " eagles"), [Nc(2, " eagles"), Nc(6, " eagles"), Nc(4, " eagles")],
        "%s of 6 means 6 shared into <b>2 equal groups</b>: 3 and 3. So <b>3 eagles</b> sit in the tree." % fr(1, 2))
    add("The Terry Fox Run route at school has 5 equal parts. Leah’s class walks 2 parts. What fraction of the route does the class walk?",
        Fc(2, 5), [Fc(3, 5), Fc(2, 3), Fc(5, 2)],
        "2 of the 5 equal parts: <b>%s</b> of the route." % fr(2, 5))
    add("On Grouse Mountain, Zara skis %s of a run. Kai skis %s of the same run. Who skis farther?" % (fr(1, 2), fr(1, 3)),
        "Zara", ["Kai", "They ski the same", "You can’t tell"],
        "%s &gt; %s, because halves are bigger than thirds. So <b>Zara</b> skis farther." % (fr(1, 2), fr(1, 3)))
    add("A garden bed has 6 equal parts. Hana plants beans in 4 parts. What fraction of the garden bed has <b>no</b> beans?",
        Fc(2, 6), [Fc(4, 6), Fc(2, 4), Fc(1, 6)],
        "6 − 4 = <b>2 parts</b> have no beans, out of 6 equal parts: %s." % fr(2, 6))
    add("A basket has 10 peaches from the Okanagan. Noah eats 1 peach, then 1 more, then 1 more. What fraction of the peaches does he eat?",
        Fc(3, 10), [Fc(7, 10), Fc(1, 10), Fc(3, 7)],
        "There are 10 peaches, so each one is %s of the basket. Noah eats 3 peaches: <b>%s</b>." % (fr(1, 10), fr(3, 10)))
    assert len(W) == 12, len(W)
    for q, right, cands, e in W:
        its.append(mcq(q, right, cands, e, rnd))
    assert len(its) == 20, len(its)
    return {"title": "Fractions on a number line and word problems", "items": its}


# ============================================================ lesson
def body_html():
    dens = [2, 3, 4, 5, 6, 8, 10]
    eq_fig = svg_wrap(272, 116, bar_row(6, 6, 260, 44, 4, {0}) + bar_row(6, 66, 260, 44, 4, {0}, UNEQ[4]),
                      "two bars with 4 parts each, the top bar has equal parts and the bottom bar does not")
    unit_fig = svg_wrap(372, 6 + len(dens) * 50, "".join(
        [sfr(22, 22 + r * 50, 1, n, 15) for r, n in enumerate(dens)] +
        [bar_row(56, 6 + r * 50, 300, 38, n, {0}) for r, n in enumerate(dens)]),
        "bars of the same size showing one half, one third, one fourth, one fifth, one sixth, one eighth and one tenth")
    names = table(["Equal parts", "Name", "One part"],
                  [[str(n), WORD[n], "one %s, %s" % (ONE[n], fr(1, n))] for n in dens])
    return (
        "<h2>Equal parts</h2>"
        "<p>A fraction is <b>part of a whole</b>. The whole must be cut into <b>equal parts</b>: parts that are all the same size.</p>"
        "<figure class='sn-fig'>" + eq_fig +
        "<figcaption>Top: 4 equal parts, so the shaded part is " + fr(1, 4) + ". Bottom: 4 parts that are not equal, so the shaded part is not " + fr(1, 4) + ".</figcaption></figure>"
        + names +
        "<h2>Name a fraction</h2>"
        "<p>The <b>bottom number</b> tells how many equal parts make the whole. The <b>top number</b> tells how many parts you count.</p>"
        "<figure class='sn-fig'>" + grid_svg(4, {0, 1, 2}) +
        "<figcaption>4 equal parts, 3 shaded: " + fr(3, 4) + ", three fourths.</figcaption></figure>"
        + ex("Example", "A bar has 5 equal parts. 2 are shaded. What fraction is shaded? What fraction is not shaded?",
             "There are 5 equal parts, so the bottom number is 5. 2 are shaded and 5 − 2 = 3 are not.",
             fr(2, 5) + " shaded, " + fr(3, 5) + " not shaded")
        + "<h2>Fractions of a set</h2>"
        "<p>A fraction can be part of a <b>group</b> of things. The bottom number is how many things are in the whole group.</p>"
        "<figure class='sn-fig'>" + counters_svg(5, 2) +
        "<figcaption>2 of the 5 counters are green: " + fr(2, 5) + " of the counters are green.</figcaption></figure>"
        + ex("Example", "What is " + fr(1, 4) + " of 12?", "Share the 12 into 4 equal groups. Each group has 3.", "3")
        + "<h2>Compare unit fractions</h2>"
        "<p>A <b>unit fraction</b> has 1 on top. <b>More equal parts means smaller parts.</b> "
        "So the bigger the bottom number, the smaller the fraction.</p>"
        "<figure class='sn-fig'>" + unit_fig +
        "<figcaption>The bars are the same size. " + fr(1, 2) + " is the biggest part and " + fr(1, 10) +
        " is the smallest.</figcaption></figure>"
        + ex("Example", "Compare " + fr(1, 8) + " and " + fr(1, 4) + ".",
             "A whole cut into 4 equal parts has bigger parts than a whole cut into 8 equal parts.",
             fr(1, 8) + " &lt; " + fr(1, 4))
        + "<h2>Fractions on a number line</h2>"
        "<p>The space from 0 to 1 is the whole. Cut it into equal spaces and <b>count the spaces</b> from 0.</p>"
        "<figure class='sn-fig'>" + line1_svg(4, 3) +
        "<figcaption>4 equal spaces, so each space is " + fr(1, 4) + ". The dot is 3 spaces from 0: " + fr(3, 4) + ".</figcaption></figure>"
        + "<h2>Common mistakes</h2>"
        + table(["Mistake", "What to do instead"], [
            ["Calling unequal parts “fourths” or “thirds”", "Fractions need <b>equal</b> parts"],
            ["Thinking " + fr(1, 8) + " is bigger than " + fr(1, 4) + " because 8 is bigger than 4",
             "More parts means <b>smaller</b> parts, so " + fr(1, 8) + " &lt; " + fr(1, 4)],
            ["Writing " + fr(2, 3) + " for 2 green and 3 white counters", "The bottom number is <b>all</b> the counters: " + fr(2, 5)],
            ["Counting tick marks on a number line", "Count the <b>spaces</b> between the marks"],
            ["Counting the lines instead of the parts", "A bar with 3 lines inside has <b>4</b> parts"],
        ])
    )


FAQ = [
    {"q": "What fractions do Grade 3 students learn in BC?",
     "a": "The BC Grade 3 math curriculum lists fraction concepts. Students learn that a fraction is part of a whole cut into equal parts, name fractions such as halves, thirds, fourths, eighths and tenths with shapes, sets and number lines, and compare unit fractions."},
    {"q": "Why is 1/8 smaller than 1/4?",
     "a": "Both are one piece of the same whole. A pizza cut into 8 equal slices has smaller slices than a pizza cut into 4, so 1/8 < 1/4."},
    {"q": "What is a fraction of a set?",
     "a": "It is part of a group of things. If 2 of 5 apples are red, then 2/5 of the apples are red, because the bottom number is all the apples."},
    {"q": "How can I help my child practise fractions at home?",
     "a": "Cut sandwiches, pizza or paper into equal parts and name each part. Ask questions like “Is 1/3 or 1/6 of the pizza bigger?” and check that the parts are really equal."},
]


def gen():
    rnd = random.Random(53802)
    SPOTS.left = []
    sets = [set_equal(rnd), set_names(rnd), set_sets(rnd), set_compare(rnd), set_line_words(rnd)]
    for s in sets:
        assert len(s["items"]) == 20, (s["title"], len(s["items"]))
        cnt = [0, 0, 0, 0]
        for it in s["items"]:
            assert len(set(it["c"])) == 4, it
            cnt[it["a"]] += 1
        assert cnt == [5, 5, 5, 5], (s["title"], cnt)
    return {
        "country": "ca-bc", "subject": "math", "grade": "grade-3", "slug": "fractions", "sort": 2,
        "updated": UPDATED, "pdf_url": "",
        "title": "Grade 3 Fractions: Equal Parts, Sets and Number Lines",
        "seo_title": "Grade 3 Fractions Math Worksheets (BC Curriculum, Free, Answer Key)",
        "short_title": "Fractions",
        "domain": "Number",
        "standard_code": "Grade 3: Number",
        "standard_url": "https://curriculum.gov.bc.ca/curriculum/mathematics/3/core",
        "standard_text": "Fraction concepts",
        "meta_desc": "Free Grade 3 math worksheets on fractions: equal parts, naming halves to tenths, fractions of a set, comparing unit fractions and fractions on a number line. 100 questions with an answer key, following the BC curriculum.",
        "key_big": "A fraction needs equal parts. More parts means smaller parts.",
        "key_sub": "In 3/4, the whole has 4 equal parts and 3 are counted. 1/8 is smaller than 1/4, because eighths are smaller pieces than fourths.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, "fractions.json")
    mark_large(u, "(number line|two bars|four |[0-9]+ counters)")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(u, f, ensure_ascii=False, indent=1)
    print("wrote", path)
