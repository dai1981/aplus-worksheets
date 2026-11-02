# -*- coding: utf-8 -*-
"""
UK Year 3 Maths: Fractions (National Curriculum in England, Year 3: Fractions)
  python3 tools/gen_uk_maths_y3_fractions.py
Shaded fractions of shapes, fractions of a set of objects (counters), fractions on a 0-1 number line,
equivalent fractions with diagrams, comparing and ordering, word problems.
Denominators 2-8 only. Tenths and adding fractions are a separate unit.
Every choice carries its value; a wrong choice never equals the right value or another wrong one.
HTML attributes use single quotes (no backslashes in the JSON). British English.
"""
import json, math, os, random, re
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "uk", "maths", "year-3")
UPDATED = "2026-11-02"
FILL = "#4fae74"      # shaded part
RED = "#d6453b"
LINE = "#2b2b2b"
GIRLS = ["Amelia", "Isla", "Freya", "Poppy", "Ava", "Aisha", "Lily", "Zara", "Grace", "Ruby", "Maya", "Evie"]
BOYS = ["Oliver", "Harry", "Mohammed", "Jack", "Arjun", "Noah", "George", "Leo", "Alfie", "Kai", "Ethan", "Charlie"]
WORD = {2: "halves", 3: "thirds", 4: "quarters", 5: "fifths", 6: "sixths", 7: "sevenths", 8: "eighths"}
ONE = {2: "half", 3: "third", 4: "quarter", 5: "fifth", 6: "sixth", 7: "seventh", 8: "eighth"}


# ------------------------------------------------------------ numbers
def fr(a, b):
    return "<span class='fr'><span class='fn'>%s</span><span class='fd'>%s</span></span>" % (a, b)


def frq(b):
    return fr("<b>?</b>", b)


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


GRIDS = {4: (2, 2), 6: (2, 3), 8: (2, 4)}


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


def wall_svg(dens, shade=None, W=300, H=40):
    """Fraction wall: a row for 1 whole, then one row per denominator, every cell labelled."""
    s = []
    x0 = 6
    for r, d in enumerate([1] + list(dens)):
        y = 6 + r * H
        k = shade[1] if shade and shade[0] == d else 0
        s.append(bar_row(x0, y, W, H, d, set(range(k))))
        for i in range(d):
            cx = x0 + (i + 0.5) * W / d
            if d == 1:
                s.append(txt(cx, y + 26, "1", 16))
            else:
                s.append(sfr(cx, y + 16, 1, d, 14))
    lab = "fraction wall with rows for 1 whole and %s" % ", ".join(WORD[d] for d in dens)
    if shade:
        lab += ", %d %s shaded" % (shade[1], WORD[shade[0]] if shade[1] > 1 else ONE[shade[0]])
    return svg_wrap(W + 12, (len(dens) + 1) * H + 12, "".join(s), lab)


COLS = {2: 2, 3: 3, 4: 2, 5: 3, 6: 3, 7: 4, 8: 4}
STEP, CR = 22, 8


def groups_svg(b, per, ring=0):
    """b equal groups of per counters, each in a box. The first `ring` boxes are shaded."""
    cols = COLS[per]
    rows = -(-per // cols)
    bw, bh = cols * STEP + 10, rows * STEP + 10
    gpr = 4 if b > 4 else b                      # groups per row
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


# ============================================================ set 1: what fraction is shaded?
def frac_cands(k, n):
    """Typical wrong answers for k/n shaded."""
    c = [Fc(n - k, n), Fc(k, n - k) if n - k != k else None, Fc(k, n + 1), Fc(n, k), Fc(k + 1, n) if k + 1 < n else None, Fc(1, k + 1), Fc(k, n + 2), Fc(n, n)]
    return c


def set_shaded(rnd):
    SPOTS.left = []
    its = []
    combos = [(2, 1, "circle"), (4, 1, "grid"), (3, 1, "bar"), (5, 2, "bar"), (8, 3, "circle"), (6, 5, "grid"),
              (4, 3, "circle"), (7, 4, "bar"), (8, 5, "grid"), (3, 2, "circle"), (6, 1, "bar")]
    for n, k, kind in combos:
        sh = set(range(k)) if kind != "grid" else set(rnd.sample(range(n), k))
        e = ("The whole has <b>%d equal parts</b>, so the denominator (bottom number) is %d. "
             "<b>%s shaded, so the numerator (top number) is %d. The answer is %s."
             % (n, n, "1 part</b> is" if k == 1 else "%d parts</b> are" % k, k, fr(k, n)))
        its.append(mcq(fig(shape_svg(n, sh, kind)) + "What fraction of the shape is shaded?",
                       Fc(k, n), frac_cands(k, n), e, rnd))

    for n, k, kind in [(4, 1, "bar"), (6, 2, "circle"), (8, 3, "bar")]:
        e = ("There are %d equal parts. %d %s shaded, so %d − %d = <b>%d parts are not shaded</b>. "
             "The answer is %s." % (n, k, "is" if k == 1 else "are", n, k, n - k, fr(n - k, n)))
        its.append(mcq(fig(shape_svg(n, set(range(k)), kind)) + "What fraction of the shape is <b>not</b> shaded?",
                       Fc(n - k, n), [Fc(k, n), Fc(n - k, k), Fc(k, n - k), Fc(n - k, n + 1)], e, rnd))

    # which picture shows ...? (A-D in one picture)
    pics = [
        ((1, 3), (3, {0}, None),
         [((3, {0}, [0.2, 0.35, 0.45]), "has 3 parts, but they are <b>not equal</b>"),
          ((4, {0}, None), "shows %s" % fr(1, 4)), ((3, {0, 1}, None), "shows %s" % fr(2, 3))]),
        ((3, 4), (4, {0, 1, 2}, None),
         [((4, {0}, None), "shows %s" % fr(1, 4)), ((7, {0, 1, 2}, None), "has 7 parts, so it shows %s" % fr(3, 7)),
          ((4, {0, 1, 2}, [0.15, 0.2, 0.25, 0.4]), "has 4 parts, but they are <b>not equal</b>")]),
        ((2, 5), (5, {0, 1}, None),
         [((5, {0, 1, 2}, None), "shows %s" % fr(3, 5)),
          ((5, {0, 1}, [0.12, 0.13, 0.25, 0.25, 0.25]), "has 5 parts, but they are <b>not equal</b>"),
          ((7, {0, 1}, None), "has 7 parts, so it shows %s" % fr(2, 7))]),
    ]
    for (a, b), good, bad in pics:
        pos = SPOTS.next(rnd)
        order = [x[0] for x in bad[:pos]] + [good] + [x[0] for x in bad[pos:]]
        letters = [L for i, L in enumerate("ABCD") if i != pos]
        why = " ".join("%s %s." % (L, d) for L, (_, d) in zip(letters, bad))
        e = ("%s needs <b>%d equal parts</b> with <b>%d</b> shaded. That is picture <b>%s</b>. %s"
             % (fr(a, b), b, a, "ABCD"[pos], why))
        its.append(mcq_abcd(fig(four_bars_svg(order)) + "Which picture shows %s shaded?" % fr(a, b), pos, e))

    # equal parts?
    for n, ws, ok in [(4, [0.16, 0.34, 0.2, 0.3], False), (3, None, True), (5, [0.1, 0.15, 0.2, 0.25, 0.3], False)]:
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
    assert len(its) == 20, len(its)
    return {"title": "What fraction is shaded?", "items": its}


# ============================================================ set 2: fractions of a set of objects
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


def set_objects(rnd):
    SPOTS.left = []
    its = []
    for n, k in [(4, 1), (5, 2), (8, 3), (6, 5)]:
        red = set(rnd.sample(range(n), k))
        e = ("There are <b>%d counters</b> altogether, so the denominator is %d. <b>%d %s red</b>, so the numerator is %d. "
             "The answer is %s." % (n, n, k, "is" if k == 1 else "are", k, fr(k, n)))
        its.append(mcq(fig(row_svg(n, red)) + "What fraction of the counters are red?", Fc(k, n),
                       [Fc(k, n - k), Fc(n - k, n), Fc(k, n + 1), Fc(n, k)], e, rnd))
    for b, T in [(4, 12), (3, 15), (2, 16), (5, 20), (8, 24)]:
        its.append(mcq(fig(groups_svg(b, T // b)) + "The %d counters are in %d equal groups. What is %s of %d?"
                       % (T, b, fr(1, b), T), Nc(T // b), set_cands(T, 1, b), e_set(T, 1, b), rnd))
    for a, b, T in [(3, 4, 12), (2, 3, 15), (2, 5, 20), (3, 8, 24), (5, 6, 18)]:
        its.append(mcq(fig(groups_svg(b, T // b)) + "The %d counters are in %d equal groups. What is %s of %d?"
                       % (T, b, fr(a, b), T), Nc(T * a // b), set_cands(T, a, b), e_set(T, a, b), rnd))
    for b, T in [(3, 21), (4, 32), (8, 40)]:
        its.append(mcq("What is %s of %d?" % (fr(1, b), T), Nc(T // b), set_cands(T, 1, b), e_set(T, 1, b), rnd))
    for a, b, T in [(3, 4, 20), (2, 5, 25), (5, 8, 16)]:
        its.append(mcq("What is %s of %d?" % (fr(a, b), T), Nc(T * a // b), set_cands(T, a, b), e_set(T, a, b), rnd))
    assert len(its) == 20, len(its)
    return {"title": "Fractions of a set of objects", "items": its}


# ============================================================ set 3: number lines
def pick_letters(d, k, spot):
    """4 positions on a line of d spaces (1..d-1), k among them at rank `spot` (left to right).
    Wrong letters sit next to k or at d-k (counting from the wrong end)."""
    low = sorted([p for p in range(1, d) if p < k], key=lambda p: (p != d - k, k - p))
    high = sorted([p for p in range(1, d) if p > k], key=lambda p: (p != d - k, p - k))
    if len(low) < spot or len(high) < 3 - spot:
        return None
    return sorted(low[:spot] + [k] + high[:3 - spot])


def set_line(rnd):
    SPOTS.left = []
    its = []
    for d, k in [(2, 1), (4, 1), (4, 3), (3, 2), (5, 2), (6, 1), (8, 5), (5, 4), (7, 3), (8, 7)]:
        e = ("Count the <b>spaces</b>, not the marks. From 0 to 1 there are <b>%d equal spaces</b>, so each space is %s. "
             "The dot is <b>%s</b> from 0, so it is at %s." % (d, fr(1, d), parts(k, "space"), fr(k, d)))
        its.append(mcq(fig(line_svg(d, k)) + "What fraction is at the red dot?", Fc(k, d),
                       [Fc(k, d + 1), Fc(k + 1, d) if k + 1 < d else None, Fc(k - 1, d) if k > 1 else None,
                        Fc(d - k, d), Fc(d, k), Fc(1, k + 1), Fc(d, d), Fc(k, d + 2)], e, rnd))

    opts = [(8, 3), (6, 4), (8, 5), (5, 2), (8, 4), (6, 3), (7, 4)]
    for _ in range(3):
        spot = SPOTS.next(rnd)
        for d, k in opts:
            ps = pick_letters(d, k, spot)
            if ps:
                break
        opts.remove((d, k))
        e = ("The line from 0 to 1 has <b>%d equal spaces</b>, so each space is %s. Count <b>%d spaces</b> from 0. "
             "That is letter <b>%s</b>." % (d, fr(1, d), k, "ABCD"[spot]))
        its.append(mcq_abcd(fig(line_svg(d, letters=ps)) + "Which letter shows %s?" % fr(k, d), spot, e))

    for seq, d, ans, cands in [
        ([1, 2, 3, None], 5, (4, 5), [(4, 6), (3, 5), (5, 5), (4, 10)]),
        ([2, 3, 4, None], 8, (5, 8), [(5, 9), (4, 8), (6, 8), (8, 8)]),
        ([None, 2, 3, 4], 4, (1, 4), [(1, 3), (5, 4), (1, 5), (0, 4)]),
    ]:
        shown = ", ".join(fr(x, d) if x else "<b>?</b>" for x in seq)
        e = "The denominator stays %d. The numerator goes up in 1s, so the missing number is <b>%s</b>." % (d, fr(*ans))
        its.append(mcq("Count in %s. What is the missing fraction?<br>%s" % (WORD[d], shown), Fc(*ans),
                       [Fc(*c) if c[0] > 0 else None for c in cands], e, rnd))

    its.append(mcq("%s = ?" % fr(4, 4), Nc(1), [Nc(4), Fc(1, 4), Nc(8)],
                   "%s means all 4 of the 4 equal parts. That is <b>1 whole</b>." % fr(4, 4), rnd))
    its.append(mcq("Which fraction is equal to 1 whole?", Fc(6, 6), [Fc(1, 6), Fc(5, 6), Fc(6, 7)],
                   "When the numerator and the denominator are the same, all the parts are there. %s = 1." % fr(6, 6), rnd))
    its.append(mcq("How many thirds make 1 whole?", Nc(3), [Nc(1), Nc(2), Nc(4)],
                   "1 whole split into thirds has <b>3</b> equal parts: %s = 1." % fr(3, 3), rnd))
    its.append(mcq(fig(line_svg(5, 5)) + "The dot is at 1. Which fraction is also at the dot?", Fc(5, 5),
                   [Fc(1, 5), Fc(4, 5), Fc(5, 6)],
                   "There are 5 equal spaces from 0 to 1. The dot is 5 spaces from 0, so it is at %s, which is 1." % fr(5, 5), rnd))
    assert len(its) == 20, len(its)
    return {"title": "Fractions on a number line", "items": its}


# ============================================================ set 4: equivalent fractions
def set_equiv(rnd):
    SPOTS.left = []
    its = []
    for a, b, d in [(1, 2, 4), (1, 2, 6), (1, 2, 8), (1, 3, 6), (2, 3, 6), (1, 4, 8), (3, 4, 8)]:
        n = d // b
        c = a * n
        q = (fig(two_bars_svg(b, a, d, c)) + "The bars are the same size. They show the same amount.<br>%s = %s"
             % (fr(a, b), frq(d)))
        e = ("Count the shaded parts in the bottom bar: <b>%d</b> out of %d. They cover the same amount as %s. "
             "So %s = %s." % (c, d, fr(a, b), fr(a, b), fr(c, d)))
        its.append(mcq(q, Nc(c), [Nc(a), Nc(a + (d - b)), Nc(d - c), Nc(c + 1), Nc(d), Nc(c - 1)], e, rnd))

    q = fig(two_bars_svg(2, 1, 6, 3)) + "The bars are the same size. They show the same amount.<br>%s = %s" % (fr(1, 2), fr(3, "<b>?</b>"))
    its.append(mcq(q, Nc(6), [Nc(4), Nc(3), Nc(5)],
                   "The bottom bar has <b>6</b> equal parts and 3 are shaded. So %s = %s." % (fr(1, 2), fr(3, 6)), rnd))

    for dens, (sd, k), t in [((2, 4, 8), (2, 1), 8), ((2, 4, 8), (4, 1), 8), ((2, 4, 8), (4, 3), 8),
                              ((3, 6), (3, 1), 6), ((3, 6), (3, 2), 6)]:
        n = t // sd
        c = k * n
        q = (fig(wall_svg(dens, (sd, k))) + "Use the fraction wall. %s is shaded. How many %s are equal to %s?"
             % (fr(k, sd), WORD[t], fr(k, sd)))
        e = ("Look straight down the fraction wall. %s lines up with <b>%d</b> %s. So %s = %s."
             % (fr(k, sd), c, WORD[t], fr(k, sd), fr(c, t)))
        its.append(mcq(q, Nc(c), [Nc(k), Nc(k + (t - sd)), Nc(t - c), Nc(t), Nc(c + 1)], e, rnd))

    for (a, b), (c, d), wrong in [((1, 2), (4, 8), [(2, 3), (1, 4), (3, 8)]),
                                  ((1, 4), (2, 8), [(2, 5), (4, 8), (1, 8)]),
                                  ((1, 3), (2, 6), [(2, 4), (3, 4), (1, 6)])]:
        e = ("Use a fraction wall: %s lines up with %s. Adding the same number to the top and bottom does <b>not</b> "
             "make an equal fraction." % (fr(a, b), fr(c, d)))
        its.append(mcq("Which fraction is equal to %s?" % fr(a, b), Fc(c, d), [Fc(*w) for w in wrong], e, rnd))

    SAME, TOP, BOT, CANT = "They are equal", "The top bar has more", "The bottom bar has more", "You can’t tell"
    for b, a, d, c in [(2, 1, 4, 2), (3, 1, 6, 3), (4, 1, 8, 2), (4, 3, 8, 5)]:
        x, y = F(a, b), F(c, d)
        right = SAME if x == y else (TOP if x > y else BOT)
        if x == y:
            e = ("The shading stops at the same place. The bottom bar has more parts, but they are smaller. "
                 "So %s = %s." % (fr(a, b), fr(c, d)))
        else:
            sg = "&gt;" if x > y else "&lt;"
            e = ("Look where the shading stops: the %s bar is shaded further. %s is the same as %s, and %s %s %s. "
                 "So %s %s %s. More parts does not mean more shaded."
                 % ("top" if x > y else "bottom", fr(a, b), fr(int(x * d), d), fr(int(x * d), d), sg, fr(c, d), fr(a, b), sg, fr(c, d)))
        its.append(mcq(fig(two_bars_svg(b, a, d, c)) + "The bars are the same size. Compare the shaded parts.",
                       right, [SAME, TOP, BOT, CANT], e, rnd))
    assert len(its) == 20, len(its)
    return {"title": "Equivalent fractions with diagrams", "items": its}


# ============================================================ set 5: compare, order, word problems
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
    P = People(rnd)
    for i, (b, d) in enumerate([(3, 6), (8, 4), (2, 5)]):
        right, ch = cmp_choices(1, b, 1, d)
        q = "Compare the fractions. Choose &lt;, &gt; or =."
        if i == 0:
            q = fig(two_bars_svg(b, 1, d, 1)) + "The bars are the same size. Compare the fractions."
        e = ("Both are unit fractions. The whole is split into %d parts or into %d parts. "
             "More parts means <b>smaller</b> parts, so %s." % (b, d, right))
        its.append(mcq(q, right, ch, e, rnd))
    for a, c, b in [(3, 4, 5), (5, 3, 8), (2, 5, 7)]:
        right, ch = cmp_choices(a, b, c, b)
        e = ("The denominators are the same, so the parts are the <b>same size</b>. Compare the numerators: "
             "%d %s %d, so %s." % (a, "is less than" if a < c else "is more than", c, right))
        its.append(mcq("Compare the fractions. Choose &lt;, &gt; or =.", right, ch, e, rnd))

    its.append(mcq("Which fraction is the <b>smallest</b>?", Fc(1, 8), [Fc(1, 2), Fc(1, 3), Fc(1, 5)],
                   "All are unit fractions. The biggest denominator means the smallest parts, so %s is the smallest." % fr(1, 8), rnd))
    its.append(mcq("Which fraction is the <b>greatest</b>?", Fc(5, 6), [Fc(2, 6), Fc(1, 6), Fc(4, 6)],
                   "The denominators are the same, so the parts are the same size. The biggest numerator wins: %s." % fr(5, 6), rnd))
    o1 = ", ".join
    its.append(mcq("Put the fractions in order, <b>smallest first</b>.",
                   o1([fr(1, 8), fr(1, 4), fr(1, 2)]),
                   [o1([fr(1, 2), fr(1, 4), fr(1, 8)]), o1([fr(1, 4), fr(1, 8), fr(1, 2)]), o1([fr(1, 8), fr(1, 2), fr(1, 4)])],
                   "For unit fractions, a bigger denominator means a smaller part. %s is the smallest and %s is the greatest."
                   % (fr(1, 8), fr(1, 2)), rnd))
    its.append(mcq("Put the fractions in order, <b>greatest first</b>.",
                   o1([fr(6, 7), fr(4, 7), fr(1, 7)]),
                   [o1([fr(1, 7), fr(4, 7), fr(6, 7)]), o1([fr(4, 7), fr(6, 7), fr(1, 7)]), o1([fr(6, 7), fr(1, 7), fr(4, 7)])],
                   "The denominators are the same, so order the numerators: 6, 4, 1. Greatest first: %s, %s, %s."
                   % (fr(6, 7), fr(4, 7), fr(1, 7)), rnd))

    # word problems
    nm, he, his = P.next()
    its.append(mcq("A pizza is cut into 8 equal slices. %s eats 3 slices. What fraction of the pizza does %s eat?" % (nm, he),
                   Fc(3, 8), [Fc(5, 8), Fc(3, 5), Fc(3, 11)],
                   "The pizza has 8 equal slices, so the denominator is 8. %s eats 3, so the answer is <b>%s</b>." % (nm, fr(3, 8)), rnd))
    nm, he, his = P.next()
    its.append(mcq("A bar of chocolate has 5 equal pieces. %s eats 2 pieces. What fraction of the bar is <b>left</b>?" % nm,
                   Fc(3, 5), [Fc(2, 5), Fc(2, 3), Fc(3, 7)],
                   "5 − 2 = <b>3 pieces</b> are left out of 5 equal pieces. The answer is %s." % fr(3, 5), rnd))
    its.append(mcq("There are 30 children in a Year 3 class. %s of them have school dinners. How many children have school dinners?" % fr(1, 3),
                   Nc(10, " children"), [Nc(3, " children"), Nc(20, " children"), Nc(27, " children")],
                   e_set(30, 1, 3, " children"), rnd))
    nm, he, his = P.next()
    its.append(mcq("%s has 20 sweets. %s of them are red. How many red sweets are there?" % (nm, fr(3, 4)),
                   Nc(15, " sweets"), [Nc(5, " sweets"), Nc(3, " sweets"), Nc(17, " sweets")],
                   e_set(20, 3, 4, " sweets"), rnd))
    its.append(mcq("There are 24 pupils in a class. %s of them go to football club. How many pupils go to football club?" % fr(3, 8),
                   Nc(9, " pupils"), [Nc(3, " pupils"), Nc(8, " pupils"), Nc(15, " pupils")],
                   e_set(24, 3, 8, " pupils"), rnd))
    (n1, h1, _), (n2, h2, _) = P.next(), P.next()
    its.append(mcq("%s eats %s of a pizza. %s eats %s of a pizza of the same size. Who eats more?" % (n1, fr(1, 4), n2, fr(1, 6)),
                   n1, [n2 + ", because 6 is bigger than 4", "They eat the same", "You can’t tell"],
                   "A pizza cut into 4 has bigger slices than a pizza cut into 6. %s &gt; %s, so <b>%s</b> eats more."
                   % (fr(1, 4), fr(1, 6), n1), rnd))
    (n1, _, _), (n2, _, _) = P.next(), P.next()
    its.append(mcq("A cake is cut into 8 equal pieces. %s eats %s of it. %s eats %s of it. Who eats <b>less</b>?" % (n1, fr(2, 8), n2, fr(5, 8)),
                   n1, [n2, "They eat the same", "You can’t tell"],
                   "The pieces are the same size (eighths). 2 pieces is less than 5 pieces, so <b>%s</b> eats less." % n1, rnd))
    (n1, _, _), (n2, _, _) = P.next(), P.next()
    its.append(mcq("%s eats %s of a sandwich. %s eats %s of a sandwich of the same size. Who eats more?" % (n1, fr(1, 2), n2, fr(2, 4)),
                   "They eat the same", [n1, n2, "You can’t tell"],
                   "%s = %s. %s has more pieces, but they are smaller. They eat the <b>same amount</b>." % (fr(1, 2), fr(2, 4), n2), rnd))
    nm, he, his = P.next()
    its.append(mcq("%s cuts a cake into 4 pieces. The pieces are different sizes. %s says each piece is %s of the cake. Is %s right?"
                   % (nm, cap(he), fr(1, 4), he),
                   "No, the pieces are not equal", ["Yes, there are 4 pieces", "No, it should be %s" % fr(1, 3), "Yes, each piece is one part"],
                   "Quarters must be <b>4 equal parts</b>. The pieces are different sizes, so they are not quarters.", rnd))
    nm, he, his = P.next()
    its.append(mcq("%s cuts a ribbon into 5 equal pieces. What fraction of the ribbon is each piece?" % nm,
                   Fc(1, 5), [Fc(1, 4), Fc(5, 5), Fc(1, 6)],
                   "The whole ribbon is shared into <b>5 equal pieces</b>. Each piece is %s. (4 cuts make 5 pieces.)" % fr(1, 5), rnd))
    assert len(its) == 20, len(its)
    return {"title": "Compare, order and solve problems", "items": its}


# ============================================================ lesson
def body_html():
    anat = ("<figure class='sn-fig'>" + bar_svg(4, {0, 1, 2}, W=320, H=56) +
            "<figcaption>4 equal parts, 3 shaded: " + fr(3, 4) + " of the bar is shaded.</figcaption></figure>")
    set_fig = ("<figure class='sn-fig'>" + groups_svg(4, 3, ring=3) +
               "<figcaption>12 counters in 4 equal groups. One group is " + fr(1, 4) + " of 12, which is 3. "
               "Three groups are " + fr(3, 4) + " of 12, which is 9.</figcaption></figure>")
    eq_fig = svg_wrap(372, 168, "".join(
        [sfr(20, 22 + r * 54, 1 if r == 0 else (2 if r == 1 else 4), n, 16) for r, n in enumerate([2, 4, 8])] +
        [bar_row(56, 6 + r * 54, 300, 38, n, set(range(n // 2))) for r, n in enumerate([2, 4, 8])]),
        "one half, two quarters and four eighths shaded on three bars of the same size")
    cmp_fig = svg_wrap(372, 114, "".join(
        [sfr(20, 24 + r * 56, 1, n, 16) for r, n in enumerate([3, 6])] +
        [bar_row(56, 6 + r * 56, 300, 42, n, {0}) for r, n in enumerate([3, 6])]),
        "one third is bigger than one sixth")
    return (
        "<h2>What a fraction means</h2>"
        "<p>A fraction is <b>part of a whole</b>. The whole must be split into <b>equal parts</b>.</p>"
        + anat +
        table(["Part", "What it tells you", "In " + fr(3, 4)], [
            ["Denominator (bottom number)", "How many <b>equal parts</b> make the whole", "4 equal parts"],
            ["Numerator (top number)", "How many of those parts you have", "3 parts"],
        ]) +
        "<p>A <b>unit fraction</b> has 1 on top, like " + fr(1, 4) + ". A <b>non-unit fraction</b> has more than 1 on top, like " + fr(3, 4) + ".</p>"
        "<h2>Fractions of a set of objects</h2>"
        "<p>To find " + fr(1, 4) + " of a group, share it into <b>4 equal groups</b> and count one group. "
        "For " + fr(3, 4) + ", count <b>3 groups</b>.</p>"
        + set_fig
        + ex("Example", "What is " + fr(2, 5) + " of 20?", "20 ÷ 5 = 4, so one fifth is 4. Two fifths: 4 × 2 = 8.", "8")
        + "<h2>Fractions on a number line</h2>"
        "<p>Fractions are numbers. They sit between 0 and 1 on a number line. "
        "Split 0 to 1 into equal spaces and count the <b>spaces</b>, not the marks.</p>"
        "<figure class='sn-fig'>" + line_svg(4, 3) +
        "<figcaption>4 equal spaces, so each space is " + fr(1, 4) + ". The dot is 3 spaces from 0: it is at " + fr(3, 4) + ".</figcaption></figure>"
        "<p>When the numerator and denominator are the same, you have the whole: " + fr(4, 4) + " = 1.</p>"
        "<h2>Equivalent fractions</h2>"
        "<p>Different fractions can show the <b>same amount</b>. They are <b>equivalent</b>.</p>"
        "<figure class='sn-fig'>" + eq_fig +
        "<figcaption>The shading stops at the same place: " + fr(1, 2) + " = " + fr(2, 4) + " = " + fr(4, 8) + ".</figcaption></figure>"
        "<h2>Comparing and ordering</h2>"
        + table(["When", "Rule", "Example"], [
            ["Unit fractions", "A <b>bigger</b> denominator means <b>smaller</b> parts.", fr(1, 3) + " &gt; " + fr(1, 6)],
            ["Same denominator", "The parts are the same size. <b>More parts</b> is greater.", fr(5, 8) + " &gt; " + fr(3, 8)],
        ]) +
        "<figure class='sn-fig'>" + cmp_fig +
        "<figcaption>Split the same bar into 3 or into 6. Each third is bigger than each sixth.</figcaption></figure>"
        + ex("Example", "Order " + fr(1, 2) + ", " + fr(1, 8) + ", " + fr(1, 4) + ", smallest first.",
             "All are unit fractions. The biggest denominator is the smallest part.", fr(1, 8) + ", " + fr(1, 4) + ", " + fr(1, 2))
        + "<h2>Common mistakes</h2>"
        + table(["Mistake", "What to do instead"], [
            ["Thinking " + fr(1, 8) + " is bigger than " + fr(1, 4) + " because 8 is bigger than 4",
             "More parts means <b>smaller</b> parts, so " + fr(1, 8) + " &lt; " + fr(1, 4)],
            ["Saying " + fr(3, 4) + " of 12 is 3", "3 is only " + fr(1, 4) + ". Take 3 groups: 3 × 3 = 9"],
            ["Counting the parts that are <b>not</b> shaded", "The numerator counts the shaded parts"],
            ["Calling unequal parts “quarters”", "Fractions need <b>equal</b> parts"],
            ["Counting the marks on a number line", "Count the <b>spaces</b> between the marks"],
        ])
    )


FAQ = [
    {"q": "What fractions do Year 3 children learn?",
     "a": "In Year 3 children work with small denominators such as halves, thirds, quarters, fifths, sixths and eighths. They find fractions of shapes and groups of objects, put fractions on a number line, find simple equivalent fractions and compare fractions."},
    {"q": "How do you find a fraction of a set of objects?",
     "a": "Share the objects into as many equal groups as the denominator, then count the groups in the numerator. For 3/4 of 12, make 4 groups of 3 and take 3 groups: 9."},
    {"q": "Why is 1/3 bigger than 1/6?",
     "a": "Cut two same-size bars into 3 parts and into 6 parts. Each third is bigger, because the whole is shared into fewer parts."},
    {"q": "What is a unit fraction?",
     "a": "A unit fraction has 1 as its numerator, such as 1/2, 1/4 or 1/8. It is one equal part of a whole."},
]


def gen():
    rnd = random.Random(3306)
    SPOTS.left = []
    sets = [set_shaded(rnd), set_objects(rnd), set_line(rnd), set_equiv(rnd), set_compare(rnd)]
    for s in sets:
        assert len(s["items"]) == 20, (s["title"], len(s["items"]))
        cnt = [0, 0, 0, 0]
        for it in s["items"]:
            assert len(set(it["c"])) == 4, it
            cnt[it["a"]] += 1
        assert cnt == [5, 5, 5, 5], (s["title"], cnt)
    return {
        "country": "uk", "subject": "maths", "grade": "year-3", "slug": "fractions", "sort": 6,
        "updated": UPDATED, "pdf_url": "",
        "title": "Year 3 Fractions",
        "seo_title": "Year 3 Fractions Worksheets: Fractions of Shapes and Amounts, Number Lines, Equivalent and Comparing Fractions",
        "short_title": "Fractions",
        "domain": "Fractions",
        "standard_code": "Year 3: Fractions",
        "standard_url": "https://www.gov.uk/government/publications/national-curriculum-in-england-mathematics-programmes-of-study",
        "standard_text": "Recognise, find and write fractions of a discrete set of objects: unit fractions and non-unit fractions with small denominators; recognise and use fractions as numbers: unit fractions and non-unit fractions with small denominators; recognise and show, using diagrams, equivalent fractions with small denominators; compare and order unit fractions, and fractions with the same denominators.",
        "meta_desc": "Free Year 3 fractions worksheets for the National Curriculum: shaded fractions of shapes, fractions of a set of objects, fractions on a number line, equivalent fractions with diagrams, comparing and ordering, and word problems. 100 questions with an answer key.",
        "key_big": "The denominator is how many equal parts make the whole. The numerator is how many parts you have.",
        "key_sub": "3/4 of 12: share 12 into 4 equal groups of 3, then take 3 groups, which is 9. For unit fractions, a bigger denominator means smaller parts, so 1/8 is less than 1/4.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, "fractions.json")
    mark_large(u, "(number line|two bars|fraction wall|counters|four pictures)")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(u, f, ensure_ascii=False, indent=1)
    print("wrote", path)
