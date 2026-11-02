# -*- coding: utf-8 -*-
"""
AU Year 3 Maths: Fractions (Australian Curriculum v9.0, AC9M3N02)
  python3 tools/gen_au_maths_y3_fractions.py
Unit fractions of shapes, multiples of unit fractions, fractions of a collection and on a 0-1 number line,
combining fractions with the same denominator to make a whole, word problems.
Denominators 2, 3, 4, 5 and 10 only. Australian English.
Every choice carries its value; a wrong choice never equals the right value or another wrong one.
HTML attributes use single quotes (no backslashes in the JSON).
"""
import json, math, os, random, re
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "au", "maths", "year-3")
UPDATED = "2026-11-02"
FILL = "#4fae74"      # shaded part
RED = "#d6453b"
LINE = "#2b2b2b"
GIRLS = ["Charlotte", "Isla", "Mia", "Amelia", "Ava", "Harper", "Chloe", "Ruby", "Mei", "Zara", "Matilda", "Sienna", "Grace"]
BOYS = ["Oliver", "Jack", "Noah", "William", "Leo", "Lachlan", "Liam", "Aarav", "Kai", "Cooper", "Ethan"]
WORD = {2: "halves", 3: "thirds", 4: "quarters", 5: "fifths", 10: "tenths"}
ONE = {2: "half", 3: "third", 4: "quarter", 5: "fifth", 10: "tenth"}


# ------------------------------------------------------------ numbers
def fr(a, b):
    return "<span class='fr'><span class='fn'>%s</span><span class='fd'>%s</span></span>" % (a, b)


def Fc(a, b, unit=""):
    return (fr(a, b) + unit, F(a, b))


def Nc(n, unit=""):
    return ("%d%s" % (n, unit), F(n))


def parts(n, word):
    return "%d %s%s" % (n, word, "" if n == 1 else "s")


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


class People:
    def __init__(self, rnd):
        self.pool = [(n, "she", "her") for n in GIRLS] + [(n, "he", "his") for n in BOYS]
        rnd.shuffle(self.pool)
        self.i = 0

    def next(self):
        p = self.pool[self.i % len(self.pool)]
        self.i += 1
        return p


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


def sfr(x, y, a, b, size=14):
    """Stacked fraction drawn in SVG, centred at x. y is the numerator baseline."""
    w = size * 0.62 * max(len(str(a)), len(str(b))) + 4
    return (txt(x, y, a, size) +
            "<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='1.5'/>"
            % (x - w / 2, y + 4, x + w / 2, y + 4, LINE) + txt(x, y + size + 4, b, size))


def bar_row(x0, y, W, H, n, shaded, widths=None):
    """n parts (equal unless widths given). shaded: set of part indexes."""
    s = []
    ws = widths or [W / n] * n
    x = x0
    for i, w in enumerate(ws):
        s.append("<rect x='%.1f' y='%.1f' width='%.2f' height='%d' fill='%s' stroke='%s' stroke-width='2.5'/>"
                 % (x, y, w, H, FILL if i in shaded else "#fff", LINE))
        x += w
    return "".join(s)


def bar_svg(n, shaded, W=260, H=50, widths=None, label=None):
    return svg_wrap(W + 12, H + 12, bar_row(6, 6, W, H, n, shaded, widths),
                    label or "bar split into %d equal parts with %d shaded" % (n, len(shaded)))


def circle_svg(n, shaded, r=62):
    cx = cy = r + 6
    s = []
    for i in range(n):
        a0 = math.radians(-90 + 360.0 * i / n)
        a1 = math.radians(-90 + 360.0 * (i + 1) / n)
        x0, y0 = cx + r * math.cos(a0), cy + r * math.sin(a0)
        x1, y1 = cx + r * math.cos(a1), cy + r * math.sin(a1)
        s.append("<path d='M%.1f %.1f L%.1f %.1f A%d %d 0 0 1 %.1f %.1f Z' fill='%s' stroke='%s' stroke-width='2.5' stroke-linejoin='round'/>"
                 % (cx, cy, x0, y0, r, r, x1, y1, FILL if i in shaded else "#fff", LINE))
    d = 2 * r + 12
    return svg_wrap(d, d, "".join(s), "circle split into %d equal parts with %d shaded" % (n, len(shaded)))


GRIDS = {4: (2, 2), 10: (2, 5)}


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


def four_bars_svg(specs, W=150, H=34):
    """Four labelled bars A-D in a 2 x 2 layout. specs: (n, shaded set, widths or None)."""
    s = []
    for i, (n, sh, ws) in enumerate(specs):
        col, row = i % 2, i // 2
        x0 = 6 + col * (W + 46)
        y0 = 6 + row * (H + 20)
        s.append(txt(x0 + 8, y0 + H / 2 + 6, "ABCD"[i], 17))
        s.append(bar_row(x0 + 22, y0, W, H, n, sh, [w * W for w in ws] if ws else None))
    return svg_wrap(2 * (W + 22) + 24 + 6, 2 * H + 20 + 12, "".join(s), "four pictures A to D")


def line_svg(d, k=None, letters=None, W=380):
    """Number line 0..1 in d equal spaces, red dot at k/d, or letters A-D above the given positions."""
    L, R, Y = 24, W - 24, 52 if letters else 40
    def X(i):
        return L + (R - L) * i / d
    s = ["<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='2.5'/>" % (L, Y, R, Y, LINE)]
    for i in range(d + 1):
        whole = i in (0, d)
        s.append("<line x1='%.1f' y1='%d' x2='%.1f' y2='%d' stroke='%s' stroke-width='%s'/>"
                 % (X(i), Y - (13 if whole else 9), X(i), Y + (13 if whole else 9), LINE, "2.5" if whole else "2"))
        if whole:
            s.append(txt(X(i), Y + 36, str(i // d), 17))
    if k is not None:
        s.append("<circle cx='%.1f' cy='%d' r='8' fill='%s'/>" % (X(k), Y, RED))
    if letters:
        for j, p in enumerate(letters):
            s.append(txt(X(p), Y - 18, "ABCD"[j], 17))
    lab = "number line from 0 to 1 split into %d equal spaces" % d
    return svg_wrap(W, Y + 46, "".join(s), lab)


def two_bars_svg(n1, k1, n2, k2, W=260, H=40):
    s = bar_row(6, 6, W, H, n1, set(range(k1))) + bar_row(6, 6 + H + 14, W, H, n2, set(range(k2)))
    return svg_wrap(W + 12, 2 * H + 26, s, "two bars of the same size, top bar %d of %d parts shaded, bottom bar %d of %d parts shaded"
                    % (k1, n1, k2, n2))


COLS = {2: 2, 3: 3, 4: 2, 5: 3, 6: 3}
STEP, CR = 22, 8


def groups_svg(b, per, ring=0):
    """b equal groups of per counters, each in a box. The first `ring` boxes are shaded."""
    cols = COLS[per]
    rows = -(-per // cols)
    bw, bh = cols * STEP + 10, rows * STEP + 10
    gpr = 5 if b in (5, 10) else (4 if b > 4 else b)     # groups per row
    nrows = -(-b // gpr)
    gap = 10
    s = []
    for g in range(b):
        gx = 6 + (g % gpr) * (bw + gap)
        gy = 6 + (g // gpr) * (bh + gap)
        s.append("<rect x='%d' y='%d' width='%d' height='%d' rx='8' fill='%s' stroke='%s' stroke-width='2'/>"
                 % (gx, gy, bw, bh, "#dff0e5" if g < ring else "#fff", LINE))
        for i in range(per):
            cx = gx + 5 + STEP / 2 + (i % cols) * STEP
            cy = gy + 5 + STEP / 2 + (i // cols) * STEP
            s.append("<circle cx='%.1f' cy='%.1f' r='%d' fill='%s' stroke='%s' stroke-width='1.8'/>" % (cx, cy, CR, RED, LINE))
    W = 12 + gpr * bw + (gpr - 1) * gap
    H = 12 + nrows * bh + (nrows - 1) * gap
    return svg_wrap(W, H, "".join(s), "counters: %d in %d equal groups of %d" % (b * per, b, per))


def row_svg(n, red):
    """A row of n counters; the ones in `red` are red, the rest white."""
    s = []
    for i in range(n):
        s.append("<circle cx='%d' cy='20' r='13' fill='%s' stroke='%s' stroke-width='2'/>"
                 % (20 + i * 34, RED if i in red else "#fff", LINE))
    return svg_wrap(n * 34 + 6, 40, "".join(s), "counters: a row of %d, %d red" % (n, len(red)))


UNEQ = {3: [0.2, 0.35, 0.45], 4: [0.15, 0.2, 0.25, 0.4], 5: [0.1, 0.15, 0.2, 0.25, 0.3],
        10: [0.05, 0.07, 0.08, 0.1, 0.1, 0.12, 0.13, 0.1, 0.15, 0.1]}


def pic_item(rnd, a, b, good, bad):
    """'Which picture shows a/b shaded?' good: spec; bad: [(spec, why)]."""
    pos = SPOTS.next(rnd)
    order = [x[0] for x in bad[:pos]] + [good] + [x[0] for x in bad[pos:]]
    letters = [L for i, L in enumerate("ABCD") if i != pos]
    why = " ".join("%s %s." % (L, d) for L, (_, d) in zip(letters, bad))
    e = ("%s needs <b>%d equal parts</b> with <b>%d</b> shaded. That is picture <b>%s</b>. %s"
         % (fr(a, b), b, a, "ABCD"[pos], why))
    return mcq_abcd(fig(four_bars_svg(order)) + "Which picture shows %s shaded?" % fr(a, b), pos, e)


# ============================================================ set 1: unit fractions of shapes
def set_unit(rnd):
    SPOTS.left = []
    its = []
    for n, kind in [(2, "circle"), (4, "grid"), (3, "bar"), (5, "bar"), (10, "grid"), (3, "circle"), (4, "bar"), (10, "bar")]:
        sh = {rnd.randrange(n)} if kind == "grid" else {0}
        e = ("The %s has <b>%d equal parts</b>, so the denominator (bottom number) is %d. "
             "<b>1 part</b> is shaded, so the numerator (top number) is 1. The answer is %s."
             % (SHAPE[kind], n, n, fr(1, n)))
        cands = [Fc(n - 1, n), Fc(1, n - 1) if n > 2 else None, Fc(1, n + 1), Fc(n, n), Fc(1, n + 2)]
        its.append(mcq(fig(shape_svg(n, sh, kind)) + "What fraction of the %s is shaded?" % SHAPE[kind],
                       Fc(1, n), cands, e, rnd))

    for n, bad in [
        (3, [((3, {0}, UNEQ[3]), "has 3 parts, but they are <b>not equal</b>"),
             ((4, {0}, None), "shows %s" % fr(1, 4)), ((3, {0, 1}, None), "shows %s" % fr(2, 3))]),
        (4, [((5, {0}, None), "has 5 parts, so it shows %s" % fr(1, 5)), ((4, {0, 1, 2}, None), "shows %s" % fr(3, 4)),
             ((4, {0}, UNEQ[4]), "has 4 parts, but they are <b>not equal</b>")]),
        (5, [((5, {0, 1}, None), "shows %s" % fr(2, 5)),
             ((5, {0}, UNEQ[5]), "has 5 parts, but they are <b>not equal</b>"), ((4, {0}, None), "has 4 parts, so it shows %s" % fr(1, 4))]),
        (10, [((10, {0}, UNEQ[10]), "has 10 parts, but they are <b>not equal</b>"),
              ((5, {0}, None), "has 5 parts, so it shows %s" % fr(1, 5)), ((10, set(range(9)), None), "shows %s" % fr(9, 10))]),
    ]:
        its.append(pic_item(rnd, 1, n, (n, {0}, None), bad))

    for n, ws, ok in [(4, [0.16, 0.34, 0.2, 0.3], False), (5, None, True), (3, [0.25, 0.25, 0.5], False)]:
        widths = [w * 260 for w in ws] if ws else None
        svg = bar_svg(n, {0}, widths=widths, label="bar split into %d parts with 1 shaded" % n)
        right = ("Yes. It has %d equal parts." % n) if ok else "No. The parts are not equal."
        cands = ["Yes. It has %d parts." % n, "No. It needs more parts.",
                 ("No. The parts are not equal." if ok else "Yes. It has %d equal parts." % n),
                 "Yes. One part is shaded."]
        e = ("A fraction needs <b>equal parts</b>. " +
             ("All %d parts are the same size, so the shaded part is %s." % (n, fr(1, n)) if ok
              else "These %d parts are different sizes, so the shaded part is <b>not</b> %s." % (n, fr(1, n))))
        its.append(mcq(fig(svg) + "Does the shaded part show %s of the bar?" % fr(1, n), right, cands, e, rnd))

    its.append(mcq(fig(two_bars_svg(3, 1, 5, 1)) + "The bars are the same size. Which shaded part is bigger?",
                   (fr(1, 3), F(1, 3)), [(fr(1, 5), F(1, 5)), "They are the same size", "You can’t tell"],
                   "The top bar is split into 3 parts and the bottom bar into 5 parts. Fewer parts means <b>bigger</b> parts, "
                   "so %s is bigger than %s." % (fr(1, 3), fr(1, 5)), rnd))
    its.append(mcq("Which unit fraction is the <b>largest</b>?", Fc(1, 2), [Fc(1, 10), Fc(1, 5), Fc(1, 3)],
                   "A unit fraction has 1 on top. The <b>smallest</b> denominator means the whole is cut into the fewest parts, "
                   "so each part is biggest. %s is the largest." % fr(1, 2), rnd))
    its.append(mcq("Which unit fraction is the <b>smallest</b>?", Fc(1, 10), [Fc(1, 2), Fc(1, 4), Fc(1, 5)],
                   "10 is the biggest denominator. A whole cut into 10 equal parts has the smallest parts, "
                   "so %s is the smallest. A bigger number on the bottom does not mean a bigger fraction." % fr(1, 10), rnd))
    its.append(mcq("A shape is split into 3 equal parts. What is each part called?", "one third",
                   ["one three", "one quarter", "three thirds"],
                   "3 equal parts are called <b>thirds</b>. Each part is one third, %s. Three thirds is the whole shape." % fr(1, 3), rnd))
    its.append(mcq("A shape is split into 10 equal parts. What is each part called?", "one tenth",
                   ["one ten", "one fifth", "ten tenths"],
                   "10 equal parts are called <b>tenths</b>. Each part is one tenth, %s." % fr(1, 10), rnd))
    assert len(its) == 20, len(its)
    return {"title": "Unit fractions of shapes", "items": its}


# ============================================================ set 2: multiples of unit fractions
def frac_cands(k, n):
    """Typical wrong answers for k/n shaded."""
    return [Fc(n - k, n), Fc(k, n - k) if n - k != k else None, Fc(k, n + 1), Fc(n, k),
            Fc(k + 1, n) if k + 1 < n else None, Fc(k - 1, n) if k > 1 else None, Fc(k, n + 2), Fc(n, n)]


def cmp_choices(a, b, c, d):
    lt = "%s &lt; %s" % (fr(a, b), fr(c, d))
    gt = "%s &gt; %s" % (fr(a, b), fr(c, d))
    eq = "%s = %s" % (fr(a, b), fr(c, d))
    x, y = F(a, b), F(c, d)
    right = lt if x < y else (gt if x > y else eq)
    return right, [lt, gt, eq, "You can’t compare them"]


def set_multiples(rnd):
    SPOTS.left = []
    its = []
    for n, k, kind in [(4, 3, "circle"), (5, 2, "bar"), (10, 7, "grid"), (3, 2, "bar"), (5, 4, "circle"),
                       (10, 3, "bar"), (4, 2, "grid"), (10, 9, "circle")]:
        sh = set(rnd.sample(range(n), k)) if kind == "grid" else set(range(k))
        e = ("There are <b>%d equal parts</b>, so each part is %s. <b>%d parts</b> are shaded, so the answer is %s "
             "(%d lots of %s)." % (n, fr(1, n), k, fr(k, n), k, fr(1, n)))
        its.append(mcq(fig(shape_svg(n, sh, kind)) + "What fraction of the %s is shaded?" % SHAPE[kind],
                       Fc(k, n), frac_cands(k, n), e, rnd))

    for n, k, kind in [(5, 2, "bar"), (10, 3, "grid"), (4, 1, "circle")]:
        e = ("There are %d equal parts. %d %s shaded, so %d − %d = <b>%d parts are not shaded</b>. "
             "The answer is %s." % (n, k, "is" if k == 1 else "are", n, k, n - k, fr(n - k, n)))
        its.append(mcq(fig(shape_svg(n, set(range(k)), kind)) + "What fraction of the %s is <b>not</b> shaded?" % SHAPE[kind],
                       Fc(n - k, n), [Fc(k, n), Fc(n - k, k), Fc(k, n - k), Fc(n - k, n + 1)], e, rnd))

    its.append(mcq("%s + %s + %s = ?" % (fr(1, 5), fr(1, 5), fr(1, 5)), Fc(3, 5), [Fc(3, 15), Fc(2, 5), Fc(5, 3)],
                   "Three lots of one fifth is <b>3 fifths</b>, %s. The parts stay fifths, so the denominator stays 5. "
                   "Do not add the bottom numbers." % fr(3, 5), rnd))
    its.append(mcq("%s is the same as how many lots of %s?" % (fr(7, 10), fr(1, 10)), Nc(7), [Nc(10), Nc(3), Nc(17)],
                   "%s means <b>7 tenths</b>: 7 lots of %s." % (fr(7, 10), fr(1, 10)), rnd))
    its.append(mcq("Count in fifths. What is the missing fraction?<br>%s, %s, <b>?</b>, %s" % (fr(1, 5), fr(2, 5), fr(4, 5)),
                   Fc(3, 5), [Fc(3, 6), Fc(2, 5), Fc(4, 5), Fc(3, 10)],
                   "The denominator stays 5. The numerator goes up in 1s: 1, 2, <b>3</b>, 4. The missing fraction is %s." % fr(3, 5), rnd))

    its.append(pic_item(rnd, 3, 5, (5, {0, 1, 2}, None), [
        ((5, {0, 1}, None), "shows %s" % fr(2, 5)),
        ((5, {0, 1, 2}, UNEQ[5]), "has 5 parts, but they are <b>not equal</b>"),
        ((10, {0, 1, 2}, None), "has 10 parts, so it shows %s" % fr(3, 10))]))
    its.append(pic_item(rnd, 7, 10, (10, set(range(7)), None), [
        ((10, set(range(3)), None), "shows %s" % fr(3, 10)),
        ((10, set(range(6)), None), "shows %s" % fr(6, 10)),
        ((10, set(range(7)), UNEQ[10]), "has 10 parts, but they are <b>not equal</b>")]))
    its.append(pic_item(rnd, 2, 3, (3, {0, 1}, None), [
        ((3, {0, 1}, [0.2, 0.3, 0.5]), "has 3 parts, but they are <b>not equal</b>"),
        ((4, {0, 1}, None), "has 4 parts, so it shows %s" % fr(2, 4)),
        ((3, {0, 1, 2}, None), "shows %s, the whole bar" % fr(3, 3))]))

    for a, c, b in [(3, 4, 5), (9, 7, 10), (2, 1, 3)]:
        right, ch = cmp_choices(a, b, c, b)
        e = ("The denominators are the same, so the parts are the <b>same size</b>. Compare the numerators: "
             "%d %s %d, so %s." % (a, "is less than" if a < c else "is more than", c, right))
        its.append(mcq("Compare the fractions. Choose &lt;, &gt; or =.", right, ch, e, rnd))
    assert len(its) == 20, len(its)
    return {"title": "Multiples of unit fractions", "items": its}


# ============================================================ set 3: collections and number lines
def e_set(T, a, b, unit=""):
    one = T // b
    if a == 1:
        return ("Share %d into <b>%d equal groups</b>: %d ÷ %d = <b>%d%s</b>. One group is %s."
                % (T, b, T, b, one, unit, fr(1, b)))
    return ("First find %s: %d ÷ %d = %d. You need <b>%d groups</b>, not 1: %d × %d = <b>%d%s</b>."
            % (fr(1, b), T, b, one, a, one, a, one * a, unit))


def set_cands(T, a, b, unit=""):
    ans = T * a // b
    one = T // b
    if a == 1:
        return [Nc(b, unit), Nc(T - one, unit), Nc(T - b, unit), Nc(one + 1, unit), Nc(T // 2, unit) if T % 2 == 0 else None]
    c = [Nc(one, unit)]
    if T % a == 0:
        c.append(Nc(T // a, unit))
    c += [Nc(T - ans, unit), Nc(a, unit), Nc(ans + one, unit), Nc(ans - 1, unit)]
    return c


def pick_letters(d, k, spot):
    low = sorted([p for p in range(1, d) if p < k], key=lambda p: (p != d - k, k - p))
    high = sorted([p for p in range(1, d) if p > k], key=lambda p: (p != d - k, p - k))
    if len(low) < spot or len(high) < 3 - spot:
        return None
    return sorted(low[:spot] + [k] + high[:3 - spot])


def set_collection(rnd):
    SPOTS.left = []
    its = []
    for n, k in [(5, 1), (10, 3), (4, 3)]:
        red = set(rnd.sample(range(n), k))
        e = ("There are <b>%d counters</b> altogether, so the denominator is %d. <b>%d %s red</b>, so the numerator is %d. "
             "The answer is %s." % (n, n, k, "is" if k == 1 else "are", k, fr(k, n)))
        its.append(mcq(fig(row_svg(n, red)) + "What fraction of the counters are red?", Fc(k, n),
                       [Fc(k, n - k), Fc(n - k, n), Fc(k, n + 1), Fc(n, k)], e, rnd))
    for b, T in [(2, 12), (3, 15), (4, 12), (5, 20), (10, 20)]:
        its.append(mcq(fig(groups_svg(b, T // b)) + "The %d counters are in %d equal groups. What is %s of %d?"
                       % (T, b, fr(1, b), T), Nc(T // b), set_cands(T, 1, b), e_set(T, 1, b), rnd))
    for a, b, T in [(3, 4, 16), (2, 5, 15), (7, 10, 30)]:
        its.append(mcq(fig(groups_svg(b, T // b)) + "The %d counters are in %d equal groups. What is %s of %d?"
                       % (T, b, fr(a, b), T), Nc(T * a // b), set_cands(T, a, b), e_set(T, a, b), rnd))
    for a, b, T in [(1, 5, 35), (1, 10, 50), (2, 3, 18)]:
        its.append(mcq("What is %s of %d?" % (fr(a, b), T), Nc(T * a // b), set_cands(T, a, b), e_set(T, a, b), rnd))

    for d, k in [(4, 3), (5, 2), (10, 7), (3, 1)]:
        e = ("Count the <b>spaces</b>, not the marks. From 0 to 1 there are <b>%d equal spaces</b>, so each space is %s. "
             "The dot is <b>%s</b> from 0, so it is at %s." % (d, fr(1, d), parts(k, "space"), fr(k, d)))
        its.append(mcq(fig(line_svg(d, k)) + "What fraction is at the red dot?", Fc(k, d),
                       [Fc(k, d + 1), Fc(d - k, d), Fc(k + 1, d) if k + 1 < d else None, Fc(k - 1, d) if k > 1 else None,
                        Fc(d, k), Fc(1, k + 1), Fc(k, d + 2)], e, rnd))
    opts = [(10, 4), (10, 6), (10, 3), (10, 8), (5, 3)]
    for _ in range(2):
        spot = SPOTS.next(rnd)
        for d, k in opts:
            ps = pick_letters(d, k, spot)
            if ps:
                break
        opts.remove((d, k))
        e = ("The line from 0 to 1 has <b>%d equal spaces</b>, so each space is %s. Count <b>%d spaces</b> from 0. "
             "That is letter <b>%s</b>." % (d, fr(1, d), k, "ABCD"[spot]))
        its.append(mcq_abcd(fig(line_svg(d, letters=ps)) + "Which letter shows %s?" % fr(k, d), spot, e))
    assert len(its) == 20, len(its)
    return {"title": "Fractions of a collection and on a number line", "items": its}


# ============================================================ set 4: make a whole
def set_whole(rnd):
    SPOTS.left = []
    its = []
    for n, k in [(5, 3), (4, 1), (3, 2), (10, 7), (2, 1), (10, 4)]:
        r = n - k
        q = (fig(bar_svg(n, set(range(k)))) + "The bar is 1 whole. %s is shaded.<br>%s + <b>?</b> = 1"
             % (fr(k, n), fr(k, n)))
        e = ("The whole has %d %s. %d %s shaded, so %d − %d = <b>%d</b> %s %s missing. %s + %s = %s = 1."
             % (n, WORD[n], k, "is" if k == 1 else "are", n, k, r, WORD[n] if r > 1 else ONE[n],
                "are" if r > 1 else "is", fr(k, n), fr(r, n), fr(n, n)))
        its.append(mcq(q, Fc(r, n), [Fc(k, n), Fc(r + 1, n), Fc(r, n + 1), Fc(r - 1, n) if r > 1 else None,
                                      Fc(n, n), Fc(1, n), Fc(r, k), Fc(r, n + 2)], e, rnd))

    its.append(mcq("%s + %s + %s + %s = ?" % ((fr(1, 4),) * 4), Nc(1), [Fc(4, 16), Fc(1, 16), Nc(4)],
                   "4 quarters make <b>1 whole</b>: %s = 1. Do not add the bottom numbers." % fr(4, 4), rnd))
    its.append(mcq("%s + %s + %s = ?" % ((fr(1, 3),) * 3), Nc(1), [Fc(3, 9), Fc(1, 9), Nc(3)],
                   "3 thirds make <b>1 whole</b>: %s = 1. The parts stay thirds." % fr(3, 3), rnd))
    its.append(mcq("How many fifths make 1 whole?", Nc(5), [Nc(1), Nc(4), Nc(10)],
                   "1 whole split into fifths has <b>5</b> equal parts: %s = 1." % fr(5, 5), rnd))
    its.append(mcq("How many tenths make 1 whole?", Nc(10), [Nc(1), Nc(9), Nc(100)],
                   "1 whole split into tenths has <b>10</b> equal parts: %s = 1." % fr(10, 10), rnd))

    for n, a in [(5, 2), (10, 3), (4, 1), (3, 1)]:
        r = n - a
        pair = lambda x, y=n: "%s + %s" % (fr(a, n), fr(x, y))
        wrong = [pair(x) for x in (r + 1, r - 1, a, n) if x > 0 and x != r]
        wrong.append(pair(r, n + 1))
        e = ("The fractions must have the same denominator and the numerators must add to %d: %d + %d = %d. "
             "So %s + %s = %s = 1." % (n, a, r, n, fr(a, n), fr(r, n), fr(n, n)))
        its.append(mcq("Which two fractions make 1 whole?", pair(r), wrong, e, rnd))

    for parts3, n in [((1, 2), 5), ((2, 5), 10), ((1, 1), 4)]:
        a, b = parts3
        r = n - a - b
        q = "%s + %s + <b>?</b> = 1" % (fr(a, n), fr(b, n))
        e = ("1 whole is %s. %d + %d = %d, and %d − %d = <b>%d</b>. So the missing fraction is %s."
             % (fr(n, n), a, b, a + b, n, a + b, r, fr(r, n)))
        its.append(mcq(q, Fc(r, n), [Fc(a + b, n), Fc(r + 1, n), Fc(r - 1, n) if r > 1 else None, Fc(r, n * 2), Fc(r, n + 1)],
                       e, rnd))

    for n, k in [(5, 2), (10, 6), (3, 1)]:
        r = n - k
        right = "%s + %s = 1" % (fr(k, n), fr(r, n))
        wrong = ["%s + %s = %s" % (fr(k, n), fr(r, n), fr(n, 2 * n)),
                 "%s + %s = 1" % (fr(k, n), fr(r + 1, n)),
                 "%s + %s = 1" % (fr(k, n), fr(k, n))]
        e = ("%s shaded and %d %s white. %s + %s = %s, which is 1 whole. "
             "Add the numerators only. The denominator stays %d."
             % ("1 part is" if k == 1 else "%d parts are" % k, r, "is" if r == 1 else "are", fr(k, n), fr(r, n), fr(n, n), n))
        its.append(mcq(fig(bar_svg(n, set(range(k)))) + "The bar is 1 whole. Which number sentence matches the bar?",
                       right, wrong, e, rnd))
    assert len(its) == 20, len(its)
    return {"title": "Combine fractions to make a whole", "items": its}


# ============================================================ set 5: word problems
def set_words(rnd):
    SPOTS.left = []
    its = []
    P = People(rnd)

    nm, he, his = P.next()
    its.append(mcq("A pizza is cut into 4 equal slices. %s eats 1 slice. What fraction of the pizza does %s eat?" % (nm, he),
                   Fc(1, 4), [Fc(3, 4), Fc(1, 3), Fc(1, 5)],
                   "The pizza has 4 equal slices, so the denominator is 4. %s eats 1, so the answer is <b>%s</b>." % (nm, fr(1, 4)), rnd))
    its.append(mcq("A family pizza is cut into 10 equal slices. The family eats 7 slices. What fraction of the pizza is <b>left</b>?",
                   Fc(3, 10), [Fc(7, 10), Fc(3, 7), Fc(7, 3)],
                   "10 − 7 = <b>3 slices</b> are left out of 10 equal slices. The answer is %s." % fr(3, 10), rnd))
    nm, he, his = P.next()
    its.append(mcq("A block of chocolate has 20 equal squares. %s eats %s of the block. How many squares does %s eat?" % (nm, fr(1, 5), he),
                   Nc(4, " squares"), set_cands(20, 1, 5, " squares"), e_set(20, 1, 5, " squares"), rnd))
    its.append(mcq("There are 30 students in a Year 3 class. %s of them walk to school. How many students walk to school?" % fr(1, 10),
                   Nc(3, " students"), set_cands(30, 1, 10, " students"), e_set(30, 1, 10, " students"), rnd))
    its.append(mcq("There are 30 students in a class. %s of them ride a bike to school. How many students ride a bike?" % fr(1, 3),
                   Nc(10, " students"), set_cands(30, 1, 3, " students"), e_set(30, 1, 3, " students"), rnd))
    nm, he, his = P.next()
    its.append(mcq("%s has 24 stickers. %s of them are koala stickers. How many koala stickers does %s have?" % (nm, fr(3, 4), he),
                   Nc(18, " stickers"), set_cands(24, 3, 4, " stickers"), e_set(24, 3, 4, " stickers"), rnd))
    its.append(mcq("The school sausage sizzle has 40 sausages. %s of them are vegetarian. How many vegetarian sausages are there?" % fr(1, 10),
                   Nc(4, " sausages"), set_cands(40, 1, 10, " sausages"), e_set(40, 1, 10, " sausages"), rnd))
    nm, he, his = P.next()
    its.append(mcq("%s has 12 strawberries for recess. %s gives %s of them to a friend. How many does %s give away?"
                   % (nm, he.capitalize(), fr(1, 3), he),
                   Nc(4, " strawberries"), set_cands(12, 1, 3, " strawberries"), e_set(12, 1, 3, " strawberries"), rnd))

    (n1, _, _), (n2, _, _) = P.next(), P.next()
    its.append(mcq("%s eats %s of a cake. %s eats the rest. What fraction of the cake does %s eat?" % (n1, fr(2, 5), n2, n2),
                   Fc(3, 5), [Fc(2, 5), Fc(3, 10), Fc(5, 5)],
                   "The whole cake is %s. %s − %s = <b>%s</b>, because 2 + 3 = 5." % (fr(5, 5), fr(5, 5), fr(2, 5), fr(3, 5)), rnd))
    (n1, _, _), (n2, _, _) = P.next(), P.next()
    its.append(mcq("A watermelon is cut into 4 equal pieces. %s and %s each eat 1 piece. What fraction of the watermelon is left?" % (n1, n2),
                   Fc(2, 4), [Fc(3, 4), Fc(1, 4), Fc(2, 2)],
                   "They eat 2 pieces, %s + %s = %s. 4 − 2 = <b>2 pieces</b> are left, so %s is left." % (fr(1, 4), fr(1, 4), fr(2, 4), fr(2, 4)), rnd))
    its.append(mcq("A game of AFL footy has 4 quarters. The teams have played 3 quarters. What fraction of the game is left?",
                   Fc(1, 4), [Fc(3, 4), Fc(1, 3), Fc(4, 4)],
                   "The game is 4 equal quarters. 4 − 3 = <b>1 quarter</b> is left: %s. %s + %s = 1." % (fr(1, 4), fr(3, 4), fr(1, 4)), rnd))
    its.append(mcq("On a school excursion, the class walks 1 km to the park. They have walked %s of the way. What fraction of the way is left?" % fr(6, 10),
                   Fc(4, 10), [Fc(6, 10), Fc(4, 6), Fc(5, 10)],
                   "The whole walk is %s. 10 − 6 = <b>4</b>, so %s of the way is left." % (fr(10, 10), fr(4, 10)), rnd))
    nm, he, his = P.next()
    its.append(mcq("%s’s garden bed has 5 equal parts. 2 parts have tomatoes and 1 part has carrots. The rest have lettuce. What fraction of the garden bed has lettuce?" % nm,
                   Fc(2, 5), [Fc(3, 5), Fc(1, 5), Fc(2, 3)],
                   "Tomatoes and carrots use 2 + 1 = 3 parts. 5 − 3 = <b>2 parts</b> have lettuce: %s." % fr(2, 5), rnd))
    nm, he, his = P.next()
    its.append(mcq("A jar has 10 marbles. 4 are blue and the rest are green. What fraction of the marbles are green?",
                   Fc(6, 10), [Fc(4, 10), Fc(6, 4), Fc(4, 6)],
                   "10 − 4 = <b>6 green</b> marbles out of 10, so %s are green." % fr(6, 10), rnd))
    (n1, _, _), (n2, _, _) = P.next(), P.next()
    its.append(mcq("%s eats %s of a sandwich. %s eats %s of the same sandwich. How much of the sandwich do they eat altogether?"
                   % (n1, fr(1, 4), n2, fr(3, 4)),
                   ("the whole sandwich", F(1)), [(fr(4, 8) + " of it", F(1, 2)), (fr(3, 4) + " of it", F(3, 4)), (fr(1, 4) + " of it", F(1, 4))],
                   "%s + %s = %s, and %s is 1 whole. They eat <b>the whole sandwich</b>. Do not add the bottom numbers."
                   % (fr(1, 4), fr(3, 4), fr(4, 4), fr(4, 4)), rnd))

    (n1, _, _), (n2, _, _) = P.next(), P.next()
    its.append(mcq("%s eats %s of a pizza. %s eats %s of a pizza of the same size. Who eats more?" % (n1, fr(1, 3), n2, fr(1, 5)),
                   n1, [n2 + ", because 5 is bigger than 3", "They eat the same", "You can’t tell"],
                   "A pizza cut into 3 has bigger slices than a pizza cut into 5. %s &gt; %s, so <b>%s</b> eats more."
                   % (fr(1, 3), fr(1, 5), n1), rnd))
    nm, he, his = P.next()
    its.append(mcq("%s says %s is bigger than %s because 10 is bigger than 5. Is %s right?" % (nm, fr(1, 10), fr(1, 5), he),
                   "No, %s is bigger" % fr(1, 5), ["Yes, 10 is bigger", "No, they are the same", "Yes, tenths are bigger"],
                   "Cutting a whole into 10 parts makes smaller parts than cutting it into 5. So %s &gt; %s." % (fr(1, 5), fr(1, 10)), rnd))
    nm, he, his = P.next()
    its.append(mcq("%s cuts a cake into 3 pieces. The pieces are different sizes. %s says each piece is %s of the cake. Is %s right?"
                   % (nm, he.capitalize(), fr(1, 3), he),
                   "No, the pieces are not equal", ["Yes, there are 3 pieces", "No, it should be %s" % fr(1, 4), "Yes, each piece is one part"],
                   "Thirds must be <b>3 equal parts</b>. The pieces are different sizes, so they are not thirds.", rnd))
    nm, he, his = P.next()
    its.append(mcq("%s cuts a ribbon into 5 equal pieces. What fraction of the ribbon is each piece?" % nm,
                   Fc(1, 5), [Fc(1, 4), Fc(5, 5), Fc(1, 6)],
                   "The whole ribbon is shared into <b>5 equal pieces</b>. Each piece is %s. (4 cuts make 5 pieces.)" % fr(1, 5), rnd))
    its.append(mcq("There are 10 players at netball training. %s of them are wearing a hat. How many are <b>not</b> wearing a hat?" % fr(2, 5),
                   Nc(6, " players"), [Nc(4, " players"), Nc(2, " players"), Nc(8, " players")],
                   "%s of 10: 10 ÷ 5 = 2, and 2 × 2 = 4 players wear a hat. 10 − 4 = <b>6 players</b> do not. "
                   "(That is %s of 10.)" % (fr(2, 5), fr(3, 5)), rnd))
    assert len(its) == 20, len(its)
    return {"title": "Fraction word problems", "items": its}


# ============================================================ lesson
def body_html():
    anat = ("<figure class='sn-fig'>" + bar_svg(4, {0, 1, 2}, W=320, H=56) +
            "<figcaption>4 equal parts, 3 shaded: " + fr(3, 4) + " of the bar is shaded.</figcaption></figure>")
    dens = [2, 3, 4, 5, 10]
    unit_fig = svg_wrap(372, 6 + len(dens) * 50, "".join(
        [sfr(22, 22 + r * 50, 1, n, 15) for r, n in enumerate(dens)] +
        [bar_row(56, 6 + r * 50, 300, 38, n, {0}) for r, n in enumerate(dens)]),
        "bars of the same size showing one half, one third, one quarter, one fifth and one tenth")
    set_fig = ("<figure class='sn-fig'>" + groups_svg(5, 4, ring=1) +
               "<figcaption>20 counters in 5 equal groups. One group is " + fr(1, 5) + " of 20, which is 4.</figcaption></figure>")
    whole_fig = svg_wrap(272, 62, bar_row(6, 6, 260, 50, 5, {0, 1, 2}), "bar split into 5 equal parts with 3 shaded")
    return (
        "<h2>Unit fractions</h2>"
        "<p>A fraction is <b>part of a whole</b>. The whole must be split into <b>equal parts</b>.</p>"
        "<p>A <b>unit fraction</b> is one equal part. It has 1 on top: " + fr(1, 2) + ", " + fr(1, 3) + ", " + fr(1, 4) + ", "
        + fr(1, 5) + " and " + fr(1, 10) + ".</p>"
        "<figure class='sn-fig'>" + unit_fig +
        "<figcaption>The bars are the same size. More parts means <b>smaller</b> parts, so " + fr(1, 10) + " is the smallest.</figcaption></figure>"
        "<h2>Multiples of unit fractions</h2>"
        + anat +
        table(["Part", "What it tells you", "In " + fr(3, 4)], [
            ["Denominator (bottom number)", "How many <b>equal parts</b> make the whole", "4 equal parts"],
            ["Numerator (top number)", "How many of those parts you have", "3 parts"],
        ]) +
        "<p>" + fr(3, 4) + " is 3 lots of " + fr(1, 4) + ": " + fr(1, 4) + " + " + fr(1, 4) + " + " + fr(1, 4) + " = " + fr(3, 4) + ".</p>"
        "<h2>Fractions of a collection</h2>"
        "<p>To find " + fr(1, 5) + " of a collection, share it into <b>5 equal groups</b> and count <b>one group</b>.</p>"
        + set_fig
        + ex("Example", "What is " + fr(3, 10) + " of 20?", "20 ÷ 10 = 2, so one tenth is 2. Three tenths: 3 × 2 = 6.", "6")
        + "<h2>Fractions on a number line</h2>"
        "<p>Fractions are numbers between 0 and 1. Split 0 to 1 into equal spaces and count the <b>spaces</b>, not the marks.</p>"
        "<figure class='sn-fig'>" + line_svg(5, 2) +
        "<figcaption>5 equal spaces, so each space is " + fr(1, 5) + ". The dot is 2 spaces from 0: it is at " + fr(2, 5) + ".</figcaption></figure>"
        "<h2>Making a whole</h2>"
        "<p>When the numerator and the denominator are the same, you have the whole: " + fr(5, 5) + " = 1. "
        "Fractions with the same denominator join to make the whole. Add the top numbers only.</p>"
        "<figure class='sn-fig'>" + whole_fig +
        "<figcaption>" + fr(3, 5) + " is shaded and " + fr(2, 5) + " is white. " + fr(3, 5) + " + " + fr(2, 5) + " = 1.</figcaption></figure>"
        + ex("Example", fr(7, 10) + " + ? = 1", "1 whole is " + fr(10, 10) + ". 10 − 7 = 3.", fr(3, 10))
        + "<h2>Common mistakes</h2>"
        + table(["Mistake", "What to do instead"], [
            ["Thinking " + fr(1, 10) + " is bigger than " + fr(1, 5) + " because 10 is bigger than 5",
             "More parts means <b>smaller</b> parts, so " + fr(1, 10) + " &lt; " + fr(1, 5)],
            ["Counting the parts that are <b>not</b> shaded", "The numerator counts the shaded parts"],
            ["Saying " + fr(1, 5) + " of 20 is 5", "5 is the number of groups. Count <b>one group</b>: 20 ÷ 5 = 4"],
            ["Calling unequal parts “thirds” or “quarters”", "Fractions need <b>equal</b> parts"],
            ["Adding the bottom numbers: " + fr(1, 4) + " + " + fr(3, 4) + " = " + fr(4, 8), "The parts stay quarters: " + fr(4, 4) + " = 1"],
            ["Counting the marks on a number line", "Count the <b>spaces</b> between the marks"],
        ])
    )


FAQ = [
    {"q": "What fractions do Year 3 students learn in the Australian Curriculum?",
     "a": "In Year 3 (AC9M3N02) students work with halves, thirds, quarters, fifths and tenths. They show unit fractions such as 1/5 and their multiples such as 3/5 with shapes, collections and number lines, and join fractions with the same denominator to make one whole."},
    {"q": "How do you find a fraction of a collection?",
     "a": "Share the collection into as many equal groups as the denominator, then count the number of groups in the numerator. For 1/5 of 20, make 5 groups of 4, so the answer is 4."},
    {"q": "Why is 1/3 bigger than 1/5?",
     "a": "Cut two same-size bars into 3 parts and into 5 parts. Each third is bigger, because the whole is shared into fewer parts."},
    {"q": "Are fractions in the Year 3 NAPLAN numeracy test?",
     "a": "Yes, simple fraction questions can appear in Year 3 NAPLAN numeracy, such as naming a shaded fraction or finding a fraction of a group. Practising with pictures, collections and number lines helps."},
]


def gen():
    rnd = random.Random(3806)
    SPOTS.left = []
    sets = [set_unit(rnd), set_multiples(rnd), set_collection(rnd), set_whole(rnd), set_words(rnd)]
    for s in sets:
        assert len(s["items"]) == 20, (s["title"], len(s["items"]))
        cnt = [0, 0, 0, 0]
        for it in s["items"]:
            assert len(set(it["c"])) == 4, it
            cnt[it["a"]] += 1
        assert cnt == [5, 5, 5, 5], (s["title"], cnt)
    return {
        "country": "au", "subject": "maths", "grade": "year-3", "slug": "fractions", "sort": 6,
        "updated": UPDATED, "pdf_url": "",
        "title": "Year 3 Fractions",
        "seo_title": "Year 3 Fractions Worksheets: Unit Fractions, Fractions of a Collection and Making a Whole (Australian Curriculum)",
        "short_title": "Fractions",
        "domain": "Number",
        "standard_code": "AC9M3N02",
        "standard_url": "https://v9.australiancurriculum.edu.au/f-10-curriculum/learning-areas/mathematics",
        "standard_text": "Recognise and represent unit fractions including 1/2, 1/3, 1/4, 1/5 and 1/10 and their multiples in different ways; combine fractions with the same denominator to complete the whole",
        "meta_desc": "Free Year 3 fractions worksheets for the Australian Curriculum: unit fractions of shapes, multiples like 3/5 and 7/10, fractions of a collection, number lines, making a whole and word problems. 100 questions with an answer key, great NAPLAN practice.",
        "key_big": "The denominator is how many equal parts make the whole. The numerator is how many parts you have.",
        "key_sub": "1/5 of 20: share 20 into 5 equal groups, and one group is 4. Fractions with the same denominator join to make a whole: 3/5 + 2/5 = 1.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, "fractions.json")
    mark_large(u, "(number line|two bars|counters|four pictures)")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(u, f, ensure_ascii=False, indent=1)
    print("wrote", path)
