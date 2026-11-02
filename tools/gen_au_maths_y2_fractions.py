# -*- coding: utf-8 -*-
"""
AU Year 2 Maths: Halves, quarters and eighths (Australian Curriculum v9.0, AC9M2N03)
  python3 tools/gen_au_maths_y2_fractions.py
Equal and unequal parts, one half / one quarter / one eighth of shapes, pizzas and sandwiches,
repeated halving (half of a half is a quarter), half and quarter of a collection, everyday problems
(half an hour, quarter past, sharing food). Unit fractions only, plus "2 quarters make a half" in words.
Every choice carries its value; a wrong choice never equals the right value or another wrong one.
HTML attributes use single quotes (no backslashes in the JSON). Australian English. Numbers to 100.
"""
import json, math, os, random, re
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "au", "maths", "year-2")
UPDATED = "2026-11-02"
FILL = "#4fae74"      # shaded part
RED = "#d6453b"
LINE = "#2b2b2b"
GIRLS = ["Charlotte", "Isla", "Mia", "Amelia", "Ava", "Harper", "Chloe", "Ruby", "Mei", "Zara", "Matilda", "Sienna", "Grace"]
BOYS = ["Oliver", "Jack", "Noah", "William", "Leo", "Lachlan", "Liam", "Aarav", "Kai", "Cooper", "Ethan"]
WORD = {2: "halves", 4: "quarters", 8: "eighths"}
ONE = {2: "half", 4: "quarter", 8: "eighth"}
# food looks: (fill of a piece that is there, outline colour). Missing pieces are drawn dashed.
STYLES = {"pizza": ("#f6cf63", "#a0522d"), "sandwich": ("#f3dca8", "#a8742f"), "orange": ("#f59b2b", "#b35f00")}


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


def fixed(q, choices, right, e):
    """Choices in a fixed order (the same list for a run of questions)."""
    return {"q": q, "c": list(choices), "a": choices.index(right), "e": e}


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


def att(i, sh, style):
    """Fill and outline of part i. Plain shapes: parts in sh are shaded green.
    Food (pizza, sandwich, orange): parts in sh are eaten, drawn as a dashed empty space."""
    if style is None:
        return "fill='%s' stroke='%s' stroke-width='2.5'" % (FILL if i in sh else "#fff", LINE)
    if i in sh:
        return "fill='#fff' stroke='#9a9a9a' stroke-width='2' stroke-dasharray='5 4'"
    f, s = STYLES[style]
    return "fill='%s' stroke='%s' stroke-width='3'" % (f, s)


def order(n, sh, style):
    """Draw eaten pieces first so the solid outlines of the other pieces sit on top."""
    if style is None:
        return list(range(n))
    return [i for i in range(n) if i in sh] + [i for i in range(n) if i not in sh]


def part_rect(x, y, w, h, i, sh, style):
    return "<rect x='%.1f' y='%.1f' width='%.2f' height='%.2f' %s/>" % (x, y, w, h, att(i, sh, style))


def part_poly(pts, i, sh, style):
    return ("<polygon points='%s' %s stroke-linejoin='round'/>"
            % (" ".join("%.1f,%.1f" % p for p in pts), att(i, sh, style)))


def bar_row(x0, y, W, H, n, sh, widths=None, style=None):
    """n parts (equal unless widths given, as parts of 1). sh: set of part indexes."""
    ws = [w * W for w in widths] if widths else [W / n] * n
    xs = [x0 + sum(ws[:i]) for i in range(n)]
    return "".join(part_rect(xs[i], y, ws[i], H, i, sh, style) for i in order(n, sh, style))


def piece(kind, n, sh, x, y, S, widths=None, style=None):
    """One shape in an S x S box at (x, y).
    kinds: circle (n slices, equal unless widths), square (n upright strips), grid (2 x 2), grid8 (4 x 2),
    diag (cut on the diagonals: 2 or 4 triangles), chord (circle cut into 2 unequal parts off the centre),
    bar (a long thin rectangle)."""
    s = []
    if kind == "circle":
        r = S / 2.0
        cx, cy = x + r, y + r
        ws = widths or [1.0 / n] * n
        st = [sum(ws[:i]) for i in range(n + 1)]
        for i in order(n, sh, style):
            a0 = math.radians(-90 + 360.0 * st[i])
            a1 = math.radians(-90 + 360.0 * st[i + 1])
            big = 1 if ws[i] > 0.5 else 0
            s.append("<path d='M%.1f %.1f L%.1f %.1f A%.1f %.1f 0 %d 1 %.1f %.1f Z' %s stroke-linejoin='round'/>"
                     % (cx, cy, cx + r * math.cos(a0), cy + r * math.sin(a0), r, r, big,
                        cx + r * math.cos(a1), cy + r * math.sin(a1), att(i, sh, style)))
    elif kind == "chord":
        r = S / 2.0
        cx, cy = x + r, y + r
        d = 0.42 * r
        h = math.sqrt(r * r - d * d)
        s.append("<circle cx='%.1f' cy='%.1f' r='%.1f' %s/>" % (cx, cy, r, att(1, sh, style)))
        s.append("<path d='M%.1f %.1f A%.1f %.1f 0 0 1 %.1f %.1f Z' %s stroke-linejoin='round'/>"
                 % (cx + d, cy - h, r, r, cx + d, cy + h, att(0, sh, style)))
    elif kind == "square":
        s.append(bar_row(x, y, S, S, n, sh, widths, style))
    elif kind == "bar":
        H = S * 0.42
        s.append(bar_row(x, y + (S - H) / 2, S, H, n, sh, widths, style))
    elif kind in ("grid", "grid8"):
        cols, rows = (2, 2) if kind == "grid" else (4, 2)
        cw, ch = S / float(cols), S / float(rows)
        for i in order(cols * rows, sh, style):
            s.append(part_rect(x + (i % cols) * cw, y + (i // cols) * ch, cw, ch, i, sh, style))
    elif kind == "diag":
        TL, TR, BR, BL = (x, y), (x + S, y), (x + S, y + S), (x, y + S)
        C = (x + S / 2.0, y + S / 2.0)
        tris = [(TL, TR, BR), (TL, BR, BL)] if n == 2 else [(TL, TR, C), (TR, BR, C), (BR, BL, C), (BL, TL, C)]
        for i in order(len(tris), sh, style):
            s.append(part_poly(tris[i], i, sh, style))
    else:
        raise ValueError(kind)
    return "".join(s)


def nparts(kind, n):
    return {"grid": 4, "grid8": 8, "chord": 2}.get(kind, n)


def shape_svg(kind, n, sh, widths=None, S=100, style=None):
    n = nparts(kind, n)
    eq = "" if kind == "chord" or widths else "equal "
    what = style or ("bar" if kind == "bar" else "circle" if kind in ("circle", "chord") else "square")
    lab = "%s cut into %d %sparts with %d %s" % (what, n, eq, len(sh), "eaten" if style else "shaded")
    if kind == "bar":
        W, H = 240, 54
        return svg_wrap(W + 12, H + 12, bar_row(6, 6, W, H, n, sh, widths, style), lab)
    return svg_wrap(S + 12, S + 12, piece(kind, n, sh, 6, 6, S, widths, style), lab)


def four_svg(specs, S=78):
    """Four shapes A-D in a row, the letter above each. specs: (kind, n, shaded, widths)."""
    s = []
    cw = S + 26
    for i, (kind, n, sh, ws) in enumerate(specs):
        x0 = 6 + i * cw
        s.append(txt(x0 + S / 2, 22, "ABCD"[i], 18))
        s.append(piece(kind, nparts(kind, n), sh, x0, 32, S, ws))
    return svg_wrap(6 + 4 * cw - 26 + 6, 32 + S + 6, "".join(s), "four pictures A to D")


def two_bars_svg(n1, k1, n2, k2, W=240, H=40):
    s = bar_row(6, 6, W, H, n1, set(range(k1))) + bar_row(6, 6 + H + 14, W, H, n2, set(range(k2)))
    return svg_wrap(W + 12, 2 * H + 26, s, "two bars of the same size, top bar %d of %d parts shaded, bottom bar %d of %d parts shaded"
                    % (k1, n1, k2, n2))


def halving_svg(rows=4, W=220, H=34):
    """1 whole, 2 halves, 4 quarters, 8 eighths: the same bar halved again and again, names on the left."""
    names = ["1 whole", "2 halves", "4 quarters", "8 eighths"][:rows]
    LW = 96
    s = []
    for r, nm in enumerate(names):
        y = 6 + r * (H + 10)
        s.append(txt(6, y + H / 2.0 + 6, nm, 16, "start"))
        s.append(bar_row(LW, y, W, H, 2 ** r, {0}))
    return svg_wrap(LW + W + 8, 6 + rows * (H + 10) - 4, "".join(s),
                    "halving bars: 1 whole, then halves, quarters and eighths, one part shaded in each")


def apple(cx, cy, r=8):
    return ("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='#6b4423' stroke-width='2' stroke-linecap='round'/>"
            "<circle cx='%.1f' cy='%.1f' r='%d' fill='%s' stroke='%s' stroke-width='1.6'/>"
            % (cx, cy - r + 1, cx + 1.5, cy - r - 3, cx, cy, r, RED, LINE))


COLS = {2: 2, 3: 3, 4: 2, 5: 3, 6: 3, 7: 4, 8: 4, 10: 5}
STEP = 22


def groups_svg(b, per, ring=0):
    """b equal groups of per apples, each in a box. The first `ring` boxes are tinted."""
    cols = COLS[per]
    rows = -(-per // cols)
    bw, bh = cols * STEP + 10, rows * STEP + 12
    gap = 10
    s = []
    for g in range(b):
        gx = 6 + g * (bw + gap)
        s.append("<rect x='%d' y='6' width='%d' height='%d' rx='8' fill='%s' stroke='%s' stroke-width='2'/>"
                 % (gx, bw, bh, "#dff0e5" if g < ring else "#fff", LINE))
        for i in range(per):
            cx = gx + 5 + STEP / 2 + (i % cols) * STEP
            cy = 6 + 7 + STEP / 2 + (i // cols) * STEP
            s.append(apple(cx, cy))
    W = 12 + b * bw + (b - 1) * gap
    return svg_wrap(W, 12 + bh, "".join(s), "apples: %d in %d equal groups of %d" % (b * per, b, per))


def apples_svg(T, cols):
    """T apples in rows of `cols`, not grouped."""
    rows = -(-T // cols)
    st = 26
    s = [apple(6 + st / 2 + (i % cols) * st, 10 + st / 2 + (i // cols) * st, 10) for i in range(T)]
    return svg_wrap(12 + cols * st, 14 + rows * st, "".join(s), "apples: %d in rows" % T)


def clock_svg(h, m, size=150):
    R = size / 2.0 - 5
    cx = cy = size / 2.0
    s = ["<circle cx='%.1f' cy='%.1f' r='%.1f' fill='#fff' stroke='%s' stroke-width='3.5'/>" % (cx, cy, R, FILL)]
    for i in range(12):
        a = math.radians(i * 30 - 90)
        s.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='2'/>"
                 % (cx + (R - 8) * math.cos(a), cy + (R - 8) * math.sin(a), cx + (R - 2) * math.cos(a), cy + (R - 2) * math.sin(a), LINE))
    rn = R - 15
    for n in range(1, 13):
        a = math.radians(n * 30 - 90)
        s.append(txt(cx + rn * math.cos(a), cy + rn * math.sin(a) + 5.5, n, 15))
    ah = math.radians(((h % 12) + m / 60.0) * 30 - 90)
    am = math.radians(m * 6 - 90)
    s.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='6' stroke-linecap='round'/>"
             % (cx, cy, cx + R * 0.4 * math.cos(ah), cy + R * 0.4 * math.sin(ah), LINE))
    s.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='3.5' stroke-linecap='round'/>"
             % (cx, cy, cx + R * 0.64 * math.cos(am), cy + R * 0.64 * math.sin(am), RED))
    s.append("<circle cx='%.1f' cy='%.1f' r='4.5' fill='%s'/>" % (cx, cy, LINE))
    return svg_wrap(size, size, "".join(s), "analog clock")


# ============================================================ set 1: equal or not equal parts
def abcd(rnd, q, good, bad, e_good):
    """good: spec; bad: list of (spec, why). Puts the right picture at the next spot."""
    pos = SPOTS.next(rnd)
    order_ = [x[0] for x in bad[:pos]] + [good] + [x[0] for x in bad[pos:]]
    letters = [L for i, L in enumerate("ABCD") if i != pos]
    why = " ".join("%s %s." % (L, d) for L, (_, d) in zip(letters, bad))
    return mcq_abcd(fig(four_svg(order_)) + q, pos, "%s That is <b>%s</b>. %s" % (e_good, "ABCD"[pos], why))


NAMES = ["halves", "quarters", "eighths", "not equal parts"]


def set_parts(rnd):
    SPOTS.left = []
    its = []
    its.append(abcd(rnd, "Which shape is cut into <b>halves</b>?",
                    ("square", 2, set(), None),
                    [(("chord", 2, set(), None), "has 2 parts, but they are <b>not equal</b>"),
                     (("grid", 4, set(), None), "has 4 equal parts"),
                     (("square", 2, set(), [0.3, 0.7]), "has 2 parts, but they are <b>not equal</b>")],
                    "Halves are <b>2 equal parts</b>."))
    its.append(abcd(rnd, "Which shape is cut into <b>quarters</b>?",
                    ("diag", 4, set(), None),
                    [(("square", 4, set(), [0.1, 0.2, 0.3, 0.4]), "has 4 parts, but they are <b>not equal</b>"),
                     (("circle", 8, set(), None), "has 8 equal parts"),
                     (("circle", 2, set(), None), "has 2 equal parts")],
                    "Quarters are <b>4 equal parts</b>."))
    its.append(abcd(rnd, "Which shape is cut into <b>eighths</b>?",
                    ("grid8", 8, set(), None),
                    [(("circle", 4, set(), None), "has 4 equal parts"),
                     (("circle", 8, set(), [0.05, 0.2, 0.1, 0.15, 0.05, 0.2, 0.1, 0.15]), "has 8 parts, but they are <b>not equal</b>"),
                     (("square", 2, set(), None), "has 2 equal parts")],
                    "Eighths are <b>8 equal parts</b>."))
    its.append(abcd(rnd, "Which shape is <b>not</b> cut into equal parts?",
                    ("circle", 4, set(), [0.15, 0.35, 0.2, 0.3]),
                    [(("grid", 4, set(), None), "has 4 equal parts"),
                     (("diag", 2, set(), None), "has 2 equal parts"),
                     (("bar", 8, set(), None), "has 8 equal parts")],
                    "Look for parts that are different sizes."))

    # 12 pictures with the same 4 names in a fixed order: 3 of each answer
    pics = [("square", 2, None, "halves"), ("grid8", 8, None, "eighths"), ("chord", 2, None, "not equal parts"),
            ("grid", 4, None, "quarters"), ("circle", 8, None, "eighths"), ("square", 2, [0.3, 0.7], "not equal parts"),
            ("circle", 2, None, "halves"), ("circle", 4, None, "quarters"), ("bar", 4, [0.1, 0.2, 0.3, 0.4], "not equal parts"),
            ("diag", 2, None, "halves"), ("bar", 8, None, "eighths"), ("diag", 4, None, "quarters")]
    for kind, n, ws, right in pics:
        n = nparts(kind, n)
        if right == "not equal parts":
            e = ("There are %d parts, but they are <b>not the same size</b>. So they are not %s." % (n, WORD.get(n, "halves")))
        else:
            e = "There are <b>%d equal parts</b>. %d equal parts are called <b>%s</b>." % (n, n, right)
        its.append(fixed(fig(shape_svg(kind, n, set(), ws)) + "What are the parts called?", NAMES, right, e))

    its.append(mcq("Halves are how many equal parts?", Nc(2), [Nc(1), Nc(4), Nc(8)],
                   "<b>2</b> equal parts make halves. Each part is one half.", rnd))
    its.append(mcq("Quarters are how many equal parts?", Nc(4), [Nc(2), Nc(8), Nc(3)],
                   "<b>4</b> equal parts make quarters. Each part is one quarter.", rnd))
    its.append(mcq("Eighths are how many equal parts?", Nc(8), [Nc(4), Nc(2), Nc(6)],
                   "<b>8</b> equal parts make eighths. Each part is one eighth.", rnd))
    its.append(mcq("Leo cuts his toast into 2 pieces. One piece is big. One piece is small. Are the pieces halves?",
                   "No, they are not equal", ["Yes, there are 2 pieces", "Yes, each is one half", "No, they are quarters"],
                   "Halves must be <b>2 equal parts</b>. One piece is bigger, so they are not halves.", rnd))
    assert len(its) == 20, len(its)
    return {"title": "Equal or not equal parts", "items": its}


# ============================================================ set 2: one half, one quarter, one eighth
def unit_cands(n):
    """Wrong answers for 1/n shaded: counting the parts not shaded, mixing up the names."""
    return {2: [Fc(1, 4), Fc(1, 8), Fc(1, 1)],
            4: [Fc(1, 2), Fc(1, 8), Fc(1, 3)],
            8: [Fc(1, 4), Fc(1, 2), Fc(1, 7)]}[n]


def unit_e(n, food=None):
    if food:
        return ("The %s has <b>%d equal pieces</b>. <b>1 piece</b> is eaten. So %s of the %s is eaten (one %s)."
                % (food, n, fr(1, n), food, ONE[n]))
    return ("The shape has <b>%d equal parts</b>. <b>1 part</b> is shaded. So %s is shaded (one %s)."
            % (n, fr(1, n), ONE[n]))


def set_names(rnd):
    SPOTS.left = []
    its = []
    for kind, n in [("square", 2), ("grid", 4), ("circle", 8), ("bar", 2), ("circle", 4), ("grid8", 8), ("diag", 4), ("bar", 8)]:
        sh = {0} if kind not in ("grid", "grid8") else {rnd.randrange(nparts(kind, n))}
        its.append(mcq(fig(shape_svg(kind, n, sh)) + "What fraction is shaded?", Fc(1, n), unit_cands(n), unit_e(n), rnd))
    for kind, n, food in [("circle", 8, "pizza"), ("circle", 4, "pizza"), ("circle", 2, "pizza"),
                          ("diag", 4, "sandwich"), ("square", 2, "sandwich"), ("grid8", 8, "sandwich")]:
        sh = {rnd.randrange(n)}
        q = fig(shape_svg(kind, n, sh, style=food)) + "1 piece of the %s is eaten. What fraction of the %s is eaten?" % (food, food)
        its.append(mcq(q, Fc(1, n), unit_cands(n), unit_e(n, food), rnd))
    its.append(abcd(rnd, "Which shape has <b>one half</b> shaded?",
                    ("circle", 2, {0}, None),
                    [(("chord", 2, {0}, None), "has 2 parts, but they are <b>not equal</b>"),
                     (("grid", 4, {1}, None), "shows one quarter"),
                     (("square", 2, {0}, [0.3, 0.7]), "has 2 parts, but they are <b>not equal</b>")],
                    "One half is <b>1 of 2 equal parts</b>."))
    its.append(abcd(rnd, "Which shape has <b>one quarter</b> shaded?",
                    ("diag", 4, {0}, None),
                    [(("grid8", 8, {0}, None), "shows one eighth"),
                     (("circle", 2, {0}, None), "shows one half"),
                     (("square", 4, {0}, [0.1, 0.2, 0.3, 0.4]), "has 4 parts, but they are <b>not equal</b>")],
                    "One quarter is <b>1 of 4 equal parts</b>."))
    its.append(abcd(rnd, "Which shape has <b>one eighth</b> shaded?",
                    ("circle", 8, {0}, None),
                    [(("grid", 4, {0}, None), "shows one quarter"),
                     (("circle", 8, {0}, [0.2, 0.1, 0.15, 0.05, 0.2, 0.1, 0.15, 0.05]), "has 8 parts, but they are <b>not equal</b>"),
                     (("square", 2, {0}, None), "shows one half")],
                    "One eighth is <b>1 of 8 equal parts</b>."))
    its.append(mcq("What do we call 1 of 4 equal parts?", "one quarter", ["one half", "one eighth", "four wholes"],
                   "4 equal parts are quarters. One part is <b>one quarter</b>, written %s." % fr(1, 4), rnd))
    its.append(mcq("What do we call 1 of 8 equal parts?", "one eighth", ["one quarter", "one half", "eight wholes"],
                   "8 equal parts are eighths. One part is <b>one eighth</b>, written %s." % fr(1, 8), rnd))
    its.append(mcq("How do we write <b>one half</b>?", Fc(1, 2), [Fc(2, 1), Fc(1, 4), Fc(1, 8)],
                   "One half is 1 part out of 2 equal parts. The 1 goes on top and the 2 goes underneath: %s." % fr(1, 2), rnd))
    assert len(its) == 20, len(its)
    return {"title": "One half, one quarter and one eighth", "items": its}


# ============================================================ set 3: repeated halving
SAME, TOP, BOT, CANT = "They are the same", "The top bar has more", "The bottom bar has more", "You can’t tell"


def set_halving(rnd):
    SPOTS.left = []
    its = []
    H = fig(halving_svg())
    its.append(mcq(H + "Fold a paper strip in half. How many equal parts are there?", Nc(2), [Nc(1), Nc(4), Nc(3)],
                   "One fold makes <b>2 equal parts</b>: 2 halves.", rnd))
    its.append(mcq(H + "Fold a paper strip in half, then in half again. How many equal parts are there?", Nc(4), [Nc(3), Nc(2), Nc(8)],
                   "Each half is folded in half. 2 halves become <b>4 equal parts</b>: 4 quarters.", rnd))
    its.append(mcq(H + "Fold a paper strip in half 3 times. How many equal parts are there?", Nc(8), [Nc(6), Nc(4), Nc(3)],
                   "The parts double each time: 2, then 4, then <b>8</b>. That is 8 eighths.", rnd))
    its.append(mcq(H + "What is half of one half?", Fc(1, 4), [Fc(1, 8), Fc(1, 1), Fc(1, 3)],
                   "Cut a half into 2 equal parts. Each part is <b>one quarter</b>, %s." % fr(1, 4), rnd))
    its.append(mcq(H + "What is half of one quarter?", Fc(1, 8), [Fc(1, 2), Fc(1, 4), Fc(1, 6)],
                   "Cut a quarter into 2 equal parts. Each part is <b>one eighth</b>, %s." % fr(1, 8), rnd))
    its.append(mcq(H + "How many quarters make one half?", Nc(2), [Nc(4), Nc(1), Nc(8)],
                   "Halve a half and you get <b>2</b> quarters. So 2 quarters make one half.", rnd))
    its.append(mcq(H + "How many eighths make one quarter?", Nc(2), [Nc(4), Nc(8), Nc(1)],
                   "Halve a quarter and you get <b>2</b> eighths. So 2 eighths make one quarter.", rnd))
    its.append(mcq(H + "How many eighths make one half?", Nc(4), [Nc(2), Nc(8), Nc(6)],
                   "One half is 2 quarters, and each quarter is 2 eighths. 2 + 2 = <b>4</b> eighths.", rnd))
    its.append(mcq("How many quarters make one whole?", Nc(4), [Nc(2), Nc(8), Nc(1)],
                   "A whole cut into quarters has <b>4</b> equal parts. 4 quarters make 1 whole.", rnd))
    its.append(mcq("How many eighths make one whole?", Nc(8), [Nc(4), Nc(6), Nc(2)],
                   "A whole cut into eighths has <b>8</b> equal parts. 8 eighths make 1 whole.", rnd))
    its.append(mcq(fig(two_bars_svg(4, 1, 8, 1)) + "The bars are the same size. Which is bigger?",
                   Fc(1, 4), [Fc(1, 8), "They are the same", "You can’t tell"],
                   "Look at the bars: one quarter is longer than one eighth. Cutting into <b>more</b> parts makes "
                   "<b>smaller</b> parts. So %s is bigger." % fr(1, 4), rnd))
    its.append(mcq("Two cakes are the same size. Which is bigger: %s of a cake or %s of a cake?" % (fr(1, 2), fr(1, 4)),
                   Fc(1, 2), [Fc(1, 4), "They are the same", "You can’t tell"],
                   "Cut a cake into 2 and the pieces are big. Cut it into 4 and the pieces are smaller. So %s is bigger."
                   % fr(1, 2), rnd))
    its.append(mcq("The wholes are the same size. Which part is the <b>smallest</b>?", "one eighth",
                   ["one half", "one quarter", "one whole"],
                   "The more equal parts, the smaller each part. 8 parts is the most, so <b>one eighth</b> is the smallest.", rnd))
    its.append(mcq("The wholes are the same size. Which part is the <b>biggest</b>?", "one half",
                   ["one eighth", "one quarter", "They are the same"],
                   "Only 2 equal parts, so each part is big. <b>One half</b> is bigger than a quarter or an eighth.", rnd))
    its.append(mcq("Kai says %s is bigger than %s, because 8 is bigger than 4. Is he right?" % (fr(1, 8), fr(1, 4)),
                   "No, %s is bigger" % fr(1, 4), ["Yes, 8 is bigger", "No, they are the same", "Yes, eighths are bigger"],
                   "Cutting into 8 parts makes <b>smaller</b> parts than cutting into 4. So %s is bigger than %s."
                   % (fr(1, 4), fr(1, 8)), rnd))
    its.append(mcq(fig(two_bars_svg(2, 1, 4, 2)) + "The bars are the same size. Look at the shaded parts.",
                   SAME, [TOP, BOT, CANT],
                   "The shading stops at the same place. One half is the same as <b>2 quarters</b>.", rnd))
    its.append(mcq(fig(two_bars_svg(4, 1, 8, 2)) + "The bars are the same size. Look at the shaded parts.",
                   SAME, [TOP, BOT, CANT],
                   "The shading stops at the same place. One quarter is the same as <b>2 eighths</b>.", rnd))
    its.append(mcq(fig(shape_svg("grid8", 8, {0, 1, 4, 5})) + "4 eighths are shaded. Which fraction is the same?",
                   Fc(1, 2), [Fc(1, 4), Fc(1, 8), Nc(4)],
                   "4 of the 8 equal parts are shaded. That is half of the shape, so 4 eighths = <b>one half</b>.", rnd))
    its.append(mcq(fig(shape_svg("circle", 8, {0, 1})) + "2 eighths are shaded. Which fraction is the same?",
                   Fc(1, 4), [Fc(1, 2), Fc(1, 8), Nc(2)],
                   "2 eighths fill one quarter of the circle. So 2 eighths = <b>one quarter</b>.", rnd))
    its.append(mcq("Cut a square in half. Cut each part in half. Then cut each part in half again. What is each part called?",
                   "one eighth", ["one quarter", "one sixth", "one half"],
                   "2 parts, then 4 parts, then <b>8</b> equal parts. Each part is <b>one eighth</b>.", rnd))
    assert len(its) == 20, len(its)
    return {"title": "Halving again: halves, quarters and eighths", "items": its}


# ============================================================ set 4: half and quarter of a collection
def e_set(T, b, unit=""):
    one = T // b
    name = {2: "one half", 4: "one quarter", 8: "one eighth"}[b]
    return ("Share %d into <b>%d equal groups</b>: %d ÷ %d = <b>%d%s</b>. One group is %s."
            % (T, b, T, b, one, unit, name))


def set_cands(T, b, unit=""):
    one = T // b
    return [Nc(T - one, unit), Nc(b, unit), Nc(T, unit), Nc(T * 2, unit) if T * 2 <= 100 else None,
            Nc(one + 1, unit), Nc(one - 1, unit) if one > 1 else None, Nc(one + 2, unit)]


def set_collection(rnd):
    SPOTS.left = []
    its = []
    for b, T in [(2, 6), (2, 10), (2, 14), (4, 8), (4, 12), (4, 20), (8, 16)]:
        q = (fig(groups_svg(b, T // b)) + "There are %d apples in %d equal groups. What is one %s of %d?"
             % (T, b, ONE[b], T))
        its.append(mcq(q, Nc(T // b), set_cands(T, b), e_set(T, b), rnd))
    for b, T, cols in [(2, 12, 6), (2, 16, 8), (4, 8, 4), (4, 16, 8), (2, 20, 10)]:
        q = fig(apples_svg(T, cols)) + "What is one %s of these apples?" % ONE[b]
        e = ("There are %d apples. " % T) + e_set(T, b)
        its.append(mcq(q, Nc(T // b), set_cands(T, b), e, rnd))
    for b, T in [(2, 40), (2, 60), (2, 100), (4, 40)]:
        its.append(mcq("What is one %s of %d?" % (ONE[b], T), Nc(T // b), set_cands(T, b), e_set(T, b), rnd))
    its.append(mcq("Half of 12 is 6. Half of 6 is 3. What is one quarter of 12?", Nc(3), [Nc(6), Nc(4), Nc(9)],
                   "A quarter is half of a half. Halve 12 to get 6, then halve 6 to get <b>3</b>.", rnd))
    its.append(mcq("Find one quarter of 24. Halve it, then halve it again.", Nc(6), [Nc(12), Nc(4), Nc(8)],
                   "Half of 24 is 12. Half of 12 is <b>6</b>. So one quarter of 24 is 6.", rnd))
    its.append(mcq("Find one eighth of 24. Halve it 3 times.", Nc(3), [Nc(6), Nc(12), Nc(8)],
                   "Half of 24 is 12. Half of 12 is 6. Half of 6 is <b>3</b>. So one eighth of 24 is 3.", rnd))
    its.append(mcq("Half of a number is 7. What is the number?", Nc(14), [Nc(7), Nc(3), Nc(9)],
                   "7 is one half. The whole is 2 halves: 7 + 7 = <b>14</b>. Check: half of 14 is 7.", rnd))
    assert len(its) == 20, len(its)
    return {"title": "Half and quarter of a collection", "items": its}


# ============================================================ set 5: everyday problems
def set_words(rnd):
    SPOTS.left = []
    its = []
    P = People(rnd)
    its.append(mcq(fig(clock_svg(3, 30)) + "What time does the clock show?", "half past 3",
                   ["half past 6", "3 o’clock", "quarter past 3"],
                   "The long hand points to 6. It has gone <b>half way</b> round, so it is half past. "
                   "The short hand is just past 3. It is <b>half past 3</b>.", rnd))
    its.append(mcq(fig(clock_svg(9, 15)) + "What time does the clock show?", "quarter past 9",
                   ["quarter to 9", "half past 9", "quarter past 3"],
                   "The long hand points to 3. It has gone <b>one quarter</b> of the way round, so it is quarter past. "
                   "The short hand is just past 9. It is <b>quarter past 9</b>.", rnd))
    its.append(mcq("How many minutes are in half an hour?", Nc(30, " minutes"),
                   [Nc(50, " minutes"), Nc(15, " minutes"), Nc(2, " minutes")],
                   "An hour has 60 minutes. Half of 60 is <b>30</b>: 30 + 30 = 60.", rnd))
    its.append(mcq("How many minutes are in a quarter of an hour?", Nc(15, " minutes"),
                   [Nc(30, " minutes"), Nc(25, " minutes"), Nc(4, " minutes")],
                   "An hour has 60 minutes. Half of 60 is 30, and half of 30 is <b>15</b>. "
                   "So a quarter of an hour is 15 minutes.", rnd))
    nm, he, his = P.next()
    its.append(mcq(fig(shape_svg("circle", 4, {1}, style="pizza")) +
                   "A pizza is cut into 4 equal slices. %s eats 1 slice. What fraction of the pizza does %s eat?" % (nm, he),
                   Fc(1, 4), [Fc(1, 3), Fc(1, 2), Fc(1, 8)],
                   "4 equal slices are quarters. %s eats 1 slice: <b>one quarter</b>, %s." % (nm, fr(1, 4)), rnd))
    nm, he, his = P.next()
    its.append(mcq(fig(shape_svg("circle", 8, {3}, style="orange")) +
                   "%s cuts an orange into 8 equal pieces. %s eats 1 piece. What fraction of the orange does %s eat?"
                   % (nm, he.capitalize(), he),
                   Fc(1, 8), [Fc(1, 7), Fc(1, 4), Fc(1, 2)],
                   "8 equal pieces are eighths. 1 piece is <b>one eighth</b>, %s." % fr(1, 8), rnd))
    its.append(mcq("Mum cuts a sandwich in half. Then she cuts each half in half again. How many equal pieces are there?",
                   Nc(4, " pieces"), [Nc(3, " pieces"), Nc(2, " pieces"), Nc(8, " pieces")],
                   "Each of the 2 halves becomes 2 pieces: 2 + 2 = <b>4</b> pieces. Each piece is one quarter.", rnd))
    (n1, _, _), (n2, _, _) = P.next(), P.next()
    its.append(mcq("Two pizzas are the same size. %s eats %s of one pizza. %s eats %s of the other pizza. Who eats more?"
                   % (n1, fr(1, 4), n2, fr(1, 8)),
                   n1, [n2, "They eat the same", "You can’t tell"],
                   "A pizza cut into 4 has bigger slices than a pizza cut into 8. %s is bigger than %s, so <b>%s</b> eats more."
                   % (fr(1, 4), fr(1, 8), n1), rnd))
    nm, he, his = P.next()
    its.append(mcq("%s cuts a pizza into 2 pieces. One piece is much bigger. %s says %s piece is one half. Is %s right?"
                   % (nm, he.capitalize(), his, he),
                   "No, the pieces are not equal", ["Yes, there are 2 pieces", "No, it is one quarter", "Yes, it was cut once"],
                   "Halves must be <b>2 equal parts</b>. One piece is bigger, so the pieces are not halves.", rnd))
    its.append(mcq("There are 24 students in a Year 2 class. Half of them walk to school. How many students walk?",
                   Nc(12, " students"), set_cands(24, 2, " students"), e_set(24, 2, " students"), rnd))
    nm, he, his = P.next()
    its.append(mcq("%s has 20c. %s spends half of it at the school canteen. How much does %s spend?" % (nm, he.capitalize(), he),
                   "10c", ["20c", "40c", "5c"],
                   "Half of 20c: share 20c into 2 equal parts. 10c + 10c = 20c, so the answer is <b>10c</b>.", rnd))
    its.append(mcq("A carton has 12 eggs. One quarter of the eggs are brown. How many eggs are brown?",
                   Nc(3, " eggs"), set_cands(12, 4, " eggs"), e_set(12, 4, " eggs"), rnd))
    nm, he, his = P.next()
    its.append(mcq("%s has $10. %s gives half of it to %s sister. How much does %s give?" % (nm, he.capitalize(), his, he),
                   "$5", ["$2", "$10", "$20"],
                   "Half of $10: $5 + $5 = $10. So the answer is <b>$5</b>.", rnd))
    nm, he, his = P.next()
    its.append(mcq("%s sees 16 kangaroos in a paddock. Half of them are eating grass. How many kangaroos are eating grass?" % nm,
                   Nc(8, " kangaroos"), set_cands(16, 2, " kangaroos"), e_set(16, 2, " kangaroos"), rnd))
    nm, he, his = P.next()
    its.append(mcq("%s has a ribbon 20 cm long. %s cuts it in half. How long is each piece?" % (nm, he.capitalize()),
                   Nc(10, " cm"), set_cands(20, 2, " cm"),
                   "Share 20 cm into <b>2 equal parts</b>: 10 cm + 10 cm = 20 cm. Each piece is <b>10 cm</b>.", rnd))
    nm, he, his = P.next()
    its.append(mcq("An orange is cut into 8 equal pieces. %s eats 2 pieces. What fraction of the orange is that?" % nm,
                   "one quarter", ["one eighth", "one half", "two quarters"],
                   "2 eighths make one quarter, because halving a quarter gives 2 eighths. So %s eats <b>one quarter</b>." % nm, rnd))
    nm, he, his = P.next()
    its.append(mcq("%s has 18 stickers. Half of them are koalas. How many koala stickers does %s have?" % (nm, he),
                   Nc(9, " stickers"), set_cands(18, 2, " stickers"), e_set(18, 2, " stickers"), rnd))
    its.append(mcq("A cake is cut into 4 equal pieces. One quarter of the cake is eaten. How many quarters are left?",
                   Nc(3, " quarters"), [Nc(1, " quarter"), Nc(4, " quarters"), Nc(2, " quarters")],
                   "The cake has 4 quarters. 1 is eaten: 4 − 1 = <b>3 quarters</b> are left.", rnd))
    nm, he, his = P.next()
    its.append(mcq("%s has 20 grapes. %s eats one quarter of them. How many grapes are <b>left</b>?" % (nm, he.capitalize()),
                   Nc(15, " grapes"), [Nc(5, " grapes"), Nc(16, " grapes"), Nc(4, " grapes")],
                   "Half of 20 is 10. Half of 10 is 5. So one quarter of 20 is 5. %s eats 5 grapes. "
                   "20 − 5 = <b>15 grapes</b> are left." % nm, rnd))
    nm, he, his = P.next()
    its.append(mcq("%s finds some shells at the beach. Half of them are white. 9 shells are white. How many shells does %s find?"
                   % (nm, he),
                   Nc(18, " shells"), [Nc(9, " shells"), Nc(11, " shells"), Nc(5, " shells")],
                   "9 shells are one half. The whole is 2 halves: 9 + 9 = <b>18 shells</b>. Check: half of 18 is 9.", rnd))
    assert len(its) == 20, len(its)
    return {"title": "Everyday halves, quarters and eighths", "items": its}


# ============================================================ lesson
def body_html():
    names_fig = svg_wrap(372, 140, "".join(
        [piece("square", 2, {0}, 10, 6, 100), piece("grid", 4, {0}, 136, 6, 100), piece("circle", 8, {0}, 262, 6, 100),
         txt(60, 132, "one half", 16), txt(186, 132, "one quarter", 16), txt(312, 132, "one eighth", 16)]),
        "one half of a square, one quarter of a square and one eighth of a circle shaded")
    uneq_fig = svg_wrap(250, 112, piece("square", 2, set(), 6, 6, 100) + piece("chord", 2, set(), 144, 6, 100),
                        "a square cut into 2 equal parts and a circle cut into 2 parts that are not equal")
    set_fig = ("<figure class='sn-fig'>" + groups_svg(2, 6, ring=1) +
               "<figcaption>12 apples in 2 equal groups. One half of 12 is 6.</figcaption></figure>")
    return (
        "<h2>Equal parts</h2>"
        "<p>A fraction is a part of a whole. The parts must be <b>equal</b> (the same size).</p>"
        "<p><b>One half</b> is one of <b>2 equal parts</b>.</p>"
        "<figure class='sn-fig'>" + uneq_fig +
        "<figcaption>The square is cut into 2 equal parts: halves. The circle has 2 parts, but they are not equal, so they are not halves.</figcaption></figure>"
        "<figure class='sn-fig'>" + names_fig +
        "<figcaption>2 equal parts are halves. 4 equal parts are quarters. 8 equal parts are eighths.</figcaption></figure>"
        + table(["Equal parts", "Each part is", "We write"], [
            ["2", "one half", fr(1, 2)],
            ["4", "one quarter", fr(1, 4)],
            ["8", "one eighth", fr(1, 8)],
        ]) +
        "<h2>Halve, then halve again</h2>"
        "<p>Cut a half in half and you get quarters. Cut a quarter in half and you get eighths.</p>"
        "<figure class='sn-fig'>" + halving_svg() +
        "<figcaption>Half of one half is one quarter. Half of one quarter is one eighth.</figcaption></figure>"
        "<p>So 2 quarters make one half, and 2 eighths make one quarter.</p>"
        "<p>More parts means <b>smaller</b> parts. One eighth is smaller than one quarter.</p>"
        "<h2>Half and quarter of a collection</h2>"
        "<p>To find one half of a group, share it into <b>2 equal groups</b>. Count one group.</p>"
        + set_fig
        + ex("Example", "What is one quarter of 8?", "Share 8 into 4 equal groups: 2, 2, 2 and 2. One group is 2.", "2")
        + ex("Example", "What is one quarter of 20?", "Halve 20 to get 10. Halve 10 to get 5.", "5")
        + ex("Example", "How many minutes are in half an hour?", "An hour is 60 minutes. Half of 60 is 30.", "30 minutes")
        + "<h2>Common mistakes</h2>"
        + table(["Mistake", "What to do instead"], [
            ["Calling 2 unequal parts “halves”", "Halves must be <b>equal</b>"],
            ["Thinking " + fr(1, 8) + " is bigger than " + fr(1, 4) + " because 8 is bigger", "More parts means <b>smaller</b> parts"],
            ["Saying half of 12 is 2", "2 is the number of groups. Count one group: 6"],
            ["Counting the parts that are <b>not</b> shaded", "Count the shaded part, then all the equal parts"],
        ])
    )


FAQ = [
    {"q": "What fractions do Year 2 students learn in the Australian Curriculum?",
     "a": "In Year 2 (AC9M2N03) students recognise one half as one of 2 equal parts of a whole. They connect halves, quarters and eighths by halving again and again."},
    {"q": "Why is one eighth smaller than one quarter?",
     "a": "A whole cut into 8 equal parts has smaller parts than the same whole cut into 4. Each quarter is cut in half to make 2 eighths."},
    {"q": "How do you find a quarter of a number?",
     "a": "Halve the number, then halve it again. For a quarter of 12, half of 12 is 6 and half of 6 is 3, so the answer is 3."},
    {"q": "Do Year 2 students sit NAPLAN?",
     "a": "No. NAPLAN starts in Year 3. Halves, quarters and eighths in Year 2 build the fraction skills used in Year 3."},
]


def gen():
    rnd = random.Random(2808)
    SPOTS.left = []
    sets = [set_parts(rnd), set_names(rnd), set_halving(rnd), set_collection(rnd), set_words(rnd)]
    for s in sets:
        assert len(s["items"]) == 20, (s["title"], len(s["items"]))
        cnt = [0, 0, 0, 0]
        for it in s["items"]:
            assert len(set(it["c"])) == 4, it
            cnt[it["a"]] += 1
        assert cnt == [5, 5, 5, 5], (s["title"], cnt)
    qs = [it["q"] for s in sets for it in s["items"]]
    assert len(set(qs)) == 100, "duplicate question"
    return {
        "country": "au", "subject": "maths", "grade": "year-2", "slug": "halves-quarters-and-eighths", "sort": 8,
        "updated": UPDATED, "pdf_url": "",
        "title": "Year 2 Halves, Quarters and Eighths",
        "seo_title": "Year 2 Fractions Worksheets: Halves, Quarters and Eighths (Australian Curriculum)",
        "short_title": "Halves, quarters and eighths",
        "domain": "Number",
        "standard_code": "AC9M2N03",
        "standard_url": "https://v9.australiancurriculum.edu.au/f-10-curriculum/learning-areas/mathematics",
        "standard_text": "Recognise and describe one-half as one of 2 equal parts of a whole and connect halves, quarters and eighths through repeated halving",
        "meta_desc": "Free Year 2 maths worksheets on halves, quarters and eighths for the Australian Curriculum: equal parts, one half, one quarter and one eighth of shapes, pizzas and sandwiches, repeated halving, half and quarter of a collection, and everyday problems. 100 questions with an answer key.",
        "key_big": "One half is one of 2 equal parts. Halve a half to get a quarter. Halve a quarter to get an eighth.",
        "key_sub": "The parts must be equal. More parts means smaller parts, so one eighth is smaller than one quarter.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, "halves-quarters-and-eighths.json")
    mark_large(u, "(two bars|apples|four pictures|halving|bar cut)")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(u, f, ensure_ascii=False, indent=1)
    print("wrote", path)
