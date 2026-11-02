# -*- coding: utf-8 -*-
"""
UK Year 2 Maths: Fractions (National Curriculum in England, Year 2: Fractions)
  python3 tools/gen_uk_maths_y2_fractions.py
Halves, thirds and quarters only (1/2, 1/3, 1/4, 2/4, 3/4): equal parts, naming fractions of shapes,
2/4 = 1/2, fractions of a set of objects, fractions of a quantity and a length, word problems.
Every choice carries its value; a wrong choice never equals the right value or another wrong one.
HTML attributes use single quotes (no backslashes in the JSON). British English. Numbers to 100.
"""
import json, math, os, random, re
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "uk", "maths", "year-2")
UPDATED = "2026-11-02"
FILL = "#4fae74"      # shaded part
RED = "#d6453b"
LINE = "#2b2b2b"
GIRLS = ["Amelia", "Isla", "Freya", "Poppy", "Ava", "Aisha", "Lily", "Zara", "Grace", "Ruby", "Maya", "Evie"]
BOYS = ["Oliver", "Harry", "Mohammed", "Jack", "Arjun", "Noah", "George", "Leo", "Alfie", "Kai", "Ethan", "Charlie"]
WORD = {2: "halves", 3: "thirds", 4: "quarters"}
ONE = {2: "half", 3: "third", 4: "quarter"}


# ------------------------------------------------------------ numbers
def fr(a, b):
    return "<span class='fr'><span class='fn'>%s</span><span class='fd'>%s</span></span>" % (a, b)


def frq(b):
    return fr("<b>?</b>", b)


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


def sfr(x, y, a, b, size=16):
    """Stacked fraction drawn in SVG, centred at x. y is the numerator baseline."""
    w = size * 0.62 * max(len(str(a)), len(str(b))) + 4
    return (txt(x, y, a, size) +
            "<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='1.5'/>"
            % (x - w / 2, y + 4, x + w / 2, y + 4, LINE) + txt(x, y + size + 4, b, size))


def poly(pts, filled):
    return ("<polygon points='%s' fill='%s' stroke='%s' stroke-width='2.5' stroke-linejoin='round'/>"
            % (" ".join("%.1f,%.1f" % p for p in pts), FILL if filled else "#fff", LINE))


def rect(x, y, w, h, filled):
    return ("<rect x='%.1f' y='%.1f' width='%.2f' height='%.2f' fill='%s' stroke='%s' stroke-width='2.5'/>"
            % (x, y, w, h, FILL if filled else "#fff", LINE))


def bar_row(x0, y, W, H, n, shaded, widths=None):
    """n parts (equal unless widths given, as parts of 1). shaded: set of part indexes."""
    ws = [w * W for w in widths] if widths else [W / n] * n
    s, x = [], x0
    for i, w in enumerate(ws):
        s.append(rect(x, y, w, H, i in shaded))
        x += w
    return "".join(s)


def piece(kind, n, sh, x, y, S, widths=None):
    """One shape in an S x S box at (x, y).
    kinds: circle (n equal slices), square (n upright strips), grid (2 x 2), diag (cut on the diagonals),
    chord (circle cut into 2 unequal parts off the centre), bar (a long thin rectangle)."""
    s = []
    if kind == "circle":
        r = S / 2.0
        cx, cy = x + r, y + r
        for i in range(n):
            a0 = math.radians(-90 + 360.0 * i / n)
            a1 = math.radians(-90 + 360.0 * (i + 1) / n)
            s.append("<path d='M%.1f %.1f L%.1f %.1f A%.1f %.1f 0 0 1 %.1f %.1f Z' fill='%s' stroke='%s' stroke-width='2.5' stroke-linejoin='round'/>"
                     % (cx, cy, cx + r * math.cos(a0), cy + r * math.sin(a0), r, r,
                        cx + r * math.cos(a1), cy + r * math.sin(a1), FILL if i in sh else "#fff", LINE))
    elif kind == "chord":
        r = S / 2.0
        cx, cy = x + r, y + r
        d = 0.42 * r
        h = math.sqrt(r * r - d * d)
        s.append("<circle cx='%.1f' cy='%.1f' r='%.1f' fill='%s' stroke='%s' stroke-width='2.5'/>"
                 % (cx, cy, r, FILL if 1 in sh else "#fff", LINE))
        s.append("<path d='M%.1f %.1f A%.1f %.1f 0 0 1 %.1f %.1f Z' fill='%s' stroke='%s' stroke-width='2.5' stroke-linejoin='round'/>"
                 % (cx + d, cy - h, r, r, cx + d, cy + h, FILL if 0 in sh else "#fff", LINE))
    elif kind == "square":
        s.append(bar_row(x, y, S, S, n, sh, widths))
    elif kind == "bar":
        H = S * 0.42
        s.append(bar_row(x, y + (S - H) / 2, S, H, n, sh, widths))
    elif kind == "grid":
        c = S / 2.0
        for i in range(4):
            s.append(rect(x + (i % 2) * c, y + (i // 2) * c, c, c, i in sh))
    elif kind == "diag":
        TL, TR, BR, BL = (x, y), (x + S, y), (x + S, y + S), (x, y + S)
        C = (x + S / 2.0, y + S / 2.0)
        tris = [(TL, TR, BR), (TL, BR, BL)] if n == 2 else [(TL, TR, C), (TR, BR, C), (BR, BL, C), (BL, TL, C)]
        for i, t in enumerate(tris):
            s.append(poly(t, i in sh))
    else:
        raise ValueError(kind)
    return "".join(s)


def shape_svg(kind, n, sh, widths=None, S=100):
    if kind == "bar":
        W, H = 240, 54
        return svg_wrap(W + 12, H + 12, bar_row(6, 6, W, H, n, sh, widths),
                        "bar split into %d %sparts with %d shaded" % (n, "" if widths else "equal ", len(sh)))
    eq = "" if kind == "chord" or widths else "equal "
    return svg_wrap(S + 12, S + 12, piece(kind, n, sh, 6, 6, S, widths),
                    "%s split into %d %sparts with %d shaded" % ("circle" if kind in ("circle", "chord") else "square", n, eq, len(sh)))


def four_svg(specs, S=78):
    """Four shapes A-D in a row, the letter above each. specs: (kind, n, shaded, widths)."""
    s = []
    cw = S + 26
    for i, (kind, n, sh, ws) in enumerate(specs):
        x0 = 6 + i * cw
        s.append(txt(x0 + S / 2, 22, "ABCD"[i], 18))
        s.append(piece(kind, n, sh, x0, 32, S, ws))
    return svg_wrap(6 + 4 * cw - 26 + 6, 32 + S + 6, "".join(s), "four pictures A to D")


def two_bars_svg(n1, k1, n2, k2, W=240, H=40):
    s = bar_row(6, 6, W, H, n1, set(range(k1))) + bar_row(6, 6 + H + 14, W, H, n2, set(range(k2)))
    return svg_wrap(W + 12, 2 * H + 26, s, "two bars of the same size, top bar %d of %d parts shaded, bottom bar %d of %d parts shaded"
                    % (k1, n1, k2, n2))


COLS = {2: 2, 3: 3, 4: 2, 5: 3, 6: 3, 7: 4, 8: 4}
STEP, CR = 22, 8


def groups_svg(b, per, ring=0):
    """b equal groups of per counters, each in a box. The first `ring` boxes are shaded."""
    cols = COLS[per]
    rows = -(-per // cols)
    bw, bh = cols * STEP + 10, rows * STEP + 10
    gap = 10
    s = []
    for g in range(b):
        gx = 6 + g * (bw + gap)
        s.append("<rect x='%d' y='6' width='%d' height='%d' rx='8' fill='%s' stroke='%s' stroke-width='2'/>"
                 % (gx, bw, bh, "#dff0e5" if g < ring else "#fff", LINE))
        for i in range(per):
            cx = gx + 5 + STEP / 2 + (i % cols) * STEP
            cy = 6 + 5 + STEP / 2 + (i // cols) * STEP
            s.append("<circle cx='%.1f' cy='%.1f' r='%d' fill='%s' stroke='%s' stroke-width='1.8'/>" % (cx, cy, CR, RED, LINE))
    W = 12 + b * bw + (b - 1) * gap
    return svg_wrap(W, 12 + bh, "".join(s), "counters: %d in %d equal groups of %d" % (b * per, b, per))


def row_svg(n, red, all_red=False):
    """A row of n counters; the ones in `red` are red, the rest white."""
    s = []
    for i in range(n):
        s.append("<circle cx='%d' cy='20' r='13' fill='%s' stroke='%s' stroke-width='2'/>"
                 % (20 + i * 34, RED if (all_red or i in red) else "#fff", LINE))
    lab = ("counters: a row of %d" % n) if all_red else ("counters: a row of %d, %d red" % (n, len(red)))
    return svg_wrap(n * 34 + 6, 40, "".join(s), lab)


def strip_svg(L, n, k, W=300, H=40, unit="cm"):
    """A ribbon L cm long cut into n equal parts, k shaded, with its length marked above."""
    x0, y0 = 8, 34
    s = ["<line x1='%d' y1='16' x2='%d' y2='16' stroke='%s' stroke-width='2'/>" % (x0, x0 + W, LINE),
         "<line x1='%d' y1='9' x2='%d' y2='23' stroke='%s' stroke-width='2'/>" % (x0, x0, LINE),
         "<line x1='%d' y1='9' x2='%d' y2='23' stroke='%s' stroke-width='2'/>" % (x0 + W, x0 + W, LINE),
         "<rect x='%.1f' y='4' width='64' height='22' fill='#fff'/>" % (x0 + W / 2.0 - 32),
         txt(x0 + W / 2.0, 22, "%d %s" % (L, unit), 17),
         bar_row(x0, y0, W, H, n, set(range(k)))]
    return svg_wrap(W + 16, y0 + H + 6, "".join(s), "strip %d %s long cut into %d equal parts, %d shaded" % (L, unit, n, k))


# ============================================================ set 1: equal parts, halves, thirds, quarters
def unit_cands(n):
    """Wrong answers for 1/n shaded: counting the parts not shaded, mixing up the names."""
    return {2: [Fc(1, 4), Fc(1, 3), Fc(2, 2)],
            3: [Fc(2, 3), Fc(1, 2), Fc(1, 4)],
            4: [Fc(3, 4), Fc(1, 3), Fc(1, 2)]}[n]


def abcd(rnd, q, good, bad, e_good):
    """good: spec; bad: list of (spec, why). Puts the right picture at the next spot."""
    pos = SPOTS.next(rnd)
    order = [x[0] for x in bad[:pos]] + [good] + [x[0] for x in bad[pos:]]
    letters = [L for i, L in enumerate("ABCD") if i != pos]
    why = " ".join("%s %s." % (L, d) for L, (_, d) in zip(letters, bad))
    return mcq_abcd(fig(four_svg(order)) + q, pos, "%s That is <b>%s</b>. %s" % (e_good, "ABCD"[pos], why))


def set_parts(rnd):
    SPOTS.left = []
    its = []
    its.append(abcd(rnd, "Which shape is cut into <b>halves</b>?",
                    ("square", 2, set(), None),
                    [(("chord", 2, set(), None), "has 2 parts, but they are <b>not equal</b>"),
                     (("square", 3, set(), None), "has 3 equal parts"),
                     (("square", 2, set(), [0.3, 0.7]), "has 2 parts, but they are <b>not equal</b>")],
                    "Halves are <b>2 equal parts</b>."))
    its.append(abcd(rnd, "Which shape is cut into <b>quarters</b>?",
                    ("grid", 4, set(), None),
                    [(("square", 4, set(), [0.1, 0.2, 0.3, 0.4]), "has 4 parts, but they are <b>not equal</b>"),
                     (("circle", 3, set(), None), "has 3 equal parts"),
                     (("diag", 2, set(), None), "has 2 equal parts")],
                    "Quarters are <b>4 equal parts</b>."))
    its.append(abcd(rnd, "Which shape is cut into <b>thirds</b>?",
                    ("circle", 3, set(), None),
                    [(("square", 3, set(), [0.15, 0.25, 0.6]), "has 3 parts, but they are <b>not equal</b>"),
                     (("circle", 4, set(), None), "has 4 equal parts"),
                     (("chord", 2, set(), None), "has 2 parts that are not equal")],
                    "Thirds are <b>3 equal parts</b>."))
    its.append(abcd(rnd, "Which shape is <b>not</b> cut into equal parts?",
                    ("square", 4, set(), [0.15, 0.35, 0.2, 0.3]),
                    [(("diag", 4, set(), None), "has 4 equal parts"),
                     (("circle", 2, set(), None), "has 2 equal parts"),
                     (("square", 3, set(), None), "has 3 equal parts")],
                    "Look for parts that are different sizes."))

    for kind, n in [("square", 2), ("circle", 2), ("diag", 2), ("bar", 3), ("circle", 3), ("square", 3),
                    ("grid", 4), ("circle", 4), ("diag", 4), ("bar", 4)]:
        sh = {0} if kind != "grid" else {rnd.randrange(4)}
        e = ("The shape has <b>%d equal parts</b>. <b>1 part</b> is shaded. So %s is shaded (one %s)."
             % (n, fr(1, n), ONE[n]))
        its.append(mcq(fig(shape_svg(kind, n, sh)) + "What fraction is shaded?", Fc(1, n), unit_cands(n), e, rnd))

    for n in (4, 2, 3):
        right = "one " + ONE[n]
        e = "%d equal parts are called <b>%s</b>. Each part is <b>one %s</b>: %s." % (n, WORD[n], ONE[n], fr(1, n))
        kind = {4: "grid", 2: "circle", 3: "bar"}[n]
        its.append(mcq(fig(shape_svg(kind, n, set())) + "The shape has %d equal parts. What is each part called?" % n,
                       right, ["one " + ONE[m] for m in (2, 3, 4) if m != n] + ["one whole"], e, rnd))
    for n in (4, 2, 3):
        e = "One whole cut into %s has <b>%d</b> equal parts. So %d %s make 1 whole: %s = 1." % (WORD[n], n, n, WORD[n], fr(n, n))
        its.append(mcq("How many %s make 1 whole?" % WORD[n], Nc(n), [Nc(1), Nc(2), Nc(3), Nc(4)], e, rnd))
    assert len(its) == 20, len(its)
    return {"title": "Equal parts: halves, thirds and quarters", "items": its}


# ============================================================ set 2: 2/4, 3/4 and 2/4 = 1/2
SAME, TOP, BOT, CANT = "They are the same", "The top bar has more", "The bottom bar has more", "You can’t tell"


def set_quarters(rnd):
    SPOTS.left = []
    its = []
    for kind, k in [("grid", 2), ("circle", 2), ("bar", 2), ("grid", 3), ("circle", 3), ("diag", 3)]:
        sh = set(range(k)) if kind != "grid" else set(rnd.sample(range(4), k))
        cands = [Fc(1, 4), Fc(3, 4), Fc(2, 2), Fc(1, 3)] if k == 2 else [Fc(1, 4), Fc(1, 3), Fc(2, 4)]
        e = ("There are <b>4 equal parts</b>, so they are quarters. <b>%d parts</b> are shaded. So %s is shaded."
             % (k, fr(k, 4)))
        its.append(mcq(fig(shape_svg(kind, 4, sh)) + "What fraction is shaded?", Fc(k, 4), cands, e, rnd))

    for kind, k in [("circle", 3), ("bar", 1)]:
        e = ("There are 4 equal parts. %d %s shaded, so <b>%d %s not shaded</b>. The answer is %s."
             % (k, "is" if k == 1 else "are", 4 - k, "is" if 4 - k == 1 else "are", fr(4 - k, 4)))
        its.append(mcq(fig(shape_svg(kind, 4, set(range(k)))) + "What fraction is <b>not</b> shaded?",
                       Fc(4 - k, 4), [Fc(k, 4), Fc(1, 3), Fc(2, 4)], e, rnd))

    its.append(abcd(rnd, "Which shape has %s shaded?" % fr(3, 4),
                    ("grid", 4, {0, 1, 3}, None),
                    [(("grid", 4, {2}, None), "shows %s" % fr(1, 4)),
                     (("circle", 4, {0, 1}, None), "shows %s" % fr(2, 4)),
                     (("square", 4, {0, 1, 2}, [0.12, 0.18, 0.25, 0.45]), "has 4 parts, but they are <b>not equal</b>")],
                    "%s needs <b>4 equal parts</b> with <b>3</b> shaded." % fr(3, 4)))
    its.append(abcd(rnd, "Which shape has %s shaded?" % fr(2, 4),
                    ("diag", 4, {0, 2}, None),
                    [(("diag", 4, {0, 1, 2}, None), "shows %s" % fr(3, 4)),
                     (("square", 3, {0, 1}, None), "has 3 parts, not 4"),
                     (("circle", 4, {0}, None), "shows %s" % fr(1, 4))],
                    "%s needs <b>4 equal parts</b> with <b>2</b> shaded." % fr(2, 4)))

    its.append(mcq(fig(two_bars_svg(2, 1, 4, 2)) + "The bars are the same size.<br>%s = %s" % (fr(1, 2), frq(4)),
                   Nc(2), [Nc(1), Nc(4), Nc(3)],
                   "Count the shaded quarters in the bottom bar: <b>2</b>. They cover the same as %s. So %s = %s."
                   % (fr(1, 2), fr(1, 2), fr(2, 4)), rnd))
    its.append(mcq("Which fraction is the same as %s?" % fr(1, 2), Fc(2, 4), [Fc(1, 4), Fc(3, 4), Fc(1, 3)],
                   "Half of 4 quarters is <b>2 quarters</b>. So %s = %s." % (fr(1, 2), fr(2, 4)), rnd))
    its.append(mcq(fig(two_bars_svg(2, 1, 4, 2)) + "The bars are the same size. Look at the shaded parts.",
                   SAME, [TOP, BOT, CANT],
                   "The shading stops at the same place. The bottom bar has more parts, but they are smaller. %s = %s."
                   % (fr(1, 2), fr(2, 4)), rnd))
    its.append(mcq(fig(two_bars_svg(4, 3, 2, 1)) + "The bars are the same size. Look at the shaded parts.",
                   TOP, [SAME, BOT, CANT],
                   "The top bar is shaded further. %s is more than %s (which is %s)." % (fr(3, 4), fr(1, 2), fr(2, 4)), rnd))
    its.append(mcq(fig(two_bars_svg(3, 1, 4, 1)) + "The bars are the same size. Which is bigger?",
                   Fc(1, 3), [Fc(1, 4), "They are the same", "You can’t tell"],
                   "Look at the bars: one third is longer than one quarter. Cutting into <b>more</b> parts makes "
                   "<b>smaller</b> parts. So %s is bigger than %s." % (fr(1, 3), fr(1, 4)), rnd))
    its.append(mcq("Two cakes are the same size. Which is bigger: %s of a cake or %s of a cake?" % (fr(1, 2), fr(1, 4)),
                   Fc(1, 2), [Fc(1, 4), "They are the same", "You can’t tell"],
                   "Cut a cake into 2 and the pieces are big. Cut it into 4 and the pieces are smaller. So %s is bigger."
                   % fr(1, 2), rnd))
    its.append(mcq("Count in quarters.<br>%s, %s, %s, <b>?</b>" % (fr(1, 4), fr(2, 4), fr(3, 4)),
                   Nc(1), [Nc(4), Fc(1, 4), Fc(3, 4)],
                   "The next one is %s. That is all 4 quarters, which is <b>1 whole</b>." % fr(4, 4), rnd))
    its.append(mcq("How many quarters are in %s?" % fr(3, 4), Nc(3), [Nc(4), Nc(1), Nc(7)],
                   "%s means <b>3</b> quarters. The top number tells you how many parts." % fr(3, 4), rnd))
    its.append(mcq(fig(shape_svg("grid", 4, {0, 3})) + "Which two fractions are both right for the shaded part?",
                   "%s and %s" % (fr(2, 4), fr(1, 2)),
                   ["%s and %s" % (fr(2, 4), fr(1, 4)), "%s and %s" % (fr(2, 2), fr(1, 2)), "%s and %s" % (fr(1, 4), fr(1, 2))],
                   "2 of the 4 equal parts are shaded: %s. That is half of the square too, so %s = %s." % (fr(2, 4), fr(2, 4), fr(1, 2)), rnd))
    its.append(mcq("Ava says %s is bigger than %s, because 4 is bigger than 3. Is she right?" % (fr(1, 4), fr(1, 3)),
                   "No, %s is bigger" % fr(1, 3), ["Yes, 4 is bigger", "No, they are the same", "Yes, quarters are bigger"],
                   "Cutting into 4 parts makes <b>smaller</b> parts than cutting into 3. So %s is bigger than %s."
                   % (fr(1, 3), fr(1, 4)), rnd))
    assert len(its) == 20, len(its)
    return {"title": "Two quarters, three quarters and one half", "items": its}


# ============================================================ set 3: fractions of a set of objects
def e_set(T, a, b, unit=""):
    one = T // b
    if a == 1 and unit == " cm":
        return ("Share %d cm into <b>%d equal parts</b>: %d ÷ %d = <b>%d cm</b>. One part is %s."
                % (T, b, T, b, one, fr(1, b)))
    if a == 1:
        return ("Share %d into <b>%d equal groups</b>: %d ÷ %d = <b>%d%s</b>. One group is %s."
                % (T, b, T, b, one, unit, fr(1, b)))
    if (a, b) == (2, 4):
        return ("%s of %d is %d. Take <b>2 groups</b>: %d + %d = <b>%d%s</b>. (%s is the same as %s, and half of %d is %d.)"
                % (fr(1, 4), T, one, one, one, 2 * one, unit, fr(2, 4), fr(1, 2), T, 2 * one))
    g = "parts" if unit == " cm" else "groups"
    return (("First find %s: %d ÷ %d = %d. You need <b>%d " + g + "</b>, not 1: %s = <b>%d%s</b>.")
            % (fr(1, b), T, b, one, a, " + ".join([str(one)] * a), one * a, unit))


def set_cands(T, a, b, unit=""):
    ans = T * a // b
    one = T // b
    if a == 1:
        return [Nc(T - one, unit), Nc(b, unit), Nc(T, unit), Nc(one + 1, unit), Nc(one - 1, unit) if one > 1 else None]
    return [Nc(one, unit), Nc(a, unit), Nc(T - ans, unit), Nc(T, unit), Nc(ans + 1, unit), Nc(ans - 1, unit)]


def set_objects(rnd):
    SPOTS.left = []
    its = []
    for n, k, cands in [(4, 1, [Fc(3, 4), Fc(1, 3), Fc(1, 2)]), (3, 1, [Fc(2, 3), Fc(1, 2), Fc(1, 4)]),
                        (4, 2, [Fc(2, 2), Fc(1, 4), Fc(3, 4)]), (4, 3, [Fc(1, 4), Fc(1, 3), Fc(2, 4)])]:
        red = set(rnd.sample(range(n), k))
        e = ("There are <b>%d counters</b>. <b>%d %s red</b>. So %s of the counters %s red."
             % (n, k, "is" if k == 1 else "are", fr(k, n), "are"))
        its.append(mcq(fig(row_svg(n, red)) + "What fraction of the counters are red?", Fc(k, n), cands, e, rnd))
    for a, b, T in [(1, 2, 6), (1, 2, 10), (1, 4, 8), (1, 3, 9), (1, 3, 6), (1, 4, 12), (1, 2, 14), (1, 3, 12),
                    (3, 4, 8), (3, 4, 12), (2, 4, 8)]:
        q = fig(groups_svg(b, T // b)) + "There are %d counters in %d equal groups. What is %s of %d?" % (T, b, fr(a, b), T)
        its.append(mcq(q, Nc(T * a // b), set_cands(T, a, b), e_set(T, a, b), rnd))
    for a, b, T in [(1, 2, 12), (1, 4, 12), (1, 3, 6), (3, 4, 4), (1, 2, 8)]:
        q = fig(row_svg(T, set(), all_red=True)) + "What is %s of these counters?" % fr(a, b)
        e = ("There are %d counters. " % T) + e_set(T, a, b)
        its.append(mcq(q, Nc(T * a // b), set_cands(T, a, b), e, rnd))
    assert len(its) == 20, len(its)
    return {"title": "Fractions of a set of objects", "items": its}


# ============================================================ set 4: fractions of a quantity and a length
def set_quantity(rnd):
    SPOTS.left = []
    its = []
    for L, n, k in [(10, 2, 1), (12, 4, 1), (12, 3, 1), (20, 4, 1), (8, 4, 3), (16, 2, 1)]:
        q = (fig(strip_svg(L, n, k)) + "The ribbon is %d cm long. It is cut into %d equal parts. How long is %s of the ribbon?"
             % (L, n, fr(k, n)))
        its.append(mcq(q, Nc(L * k // n, " cm"), set_cands(L, k, n, " cm"), e_set(L, k, n, " cm"), rnd))
    for a, b, T in [(1, 2, 20), (1, 2, 30), (1, 3, 15), (1, 4, 20), (1, 2, 50), (1, 3, 30), (1, 4, 40),
                    (3, 4, 20), (2, 4, 12), (3, 4, 16)]:
        its.append(mcq("What is %s of %d?" % (fr(a, b), T), Nc(T * a // b), set_cands(T, a, b), e_set(T, a, b), rnd))
    its.append(mcq("Which number sentence is true?", "%s of 6 = 3" % fr(1, 2),
                   ["%s of 6 = 12" % fr(1, 2), "%s of 6 = 3" % fr(1, 3), "%s of 8 = 4" % fr(1, 4)],
                   "Half of 6: share 6 into 2 equal groups. Each group has 3, so %s of 6 = 3. "
                   "(%s of 6 is 2, and %s of 8 is 2.)" % (fr(1, 2), fr(1, 3), fr(1, 4)), rnd))
    its.append(mcq("Which is more: %s of 12 or %s of 12?" % (fr(1, 3), fr(1, 4)),
                   "%s of 12" % fr(1, 3), ["%s of 12" % fr(1, 4), "They are the same", "You can’t tell"],
                   "%s of 12 is 12 ÷ 3 = <b>4</b>. %s of 12 is 12 ÷ 4 = <b>3</b>. 4 is more than 3." % (fr(1, 3), fr(1, 4)), rnd))
    its.append(mcq("What is %s of 10?" % fr(2, 4), Nc(5), [Nc(2), Nc(8), Nc(4)],
                   "%s is the same as %s. Half of 10 is <b>5</b>." % (fr(2, 4), fr(1, 2)), rnd))
    its.append(mcq("%s of <b>?</b> = 8" % fr(1, 2), Nc(16), [Nc(4), Nc(8), Nc(10)],
                   "8 is one half, so the whole is 2 halves: 8 + 8 = <b>16</b>. Check: half of 16 is 8.", rnd))
    assert len(its) == 20, len(its)
    return {"title": "Fractions of numbers and lengths", "items": its}


# ============================================================ set 5: word problems
def set_words(rnd):
    SPOTS.left = []
    its = []
    P = People(rnd)
    nm, he, his = P.next()
    its.append(mcq("A pizza is cut into 4 equal slices. %s eats 1 slice. What fraction of the pizza does %s eat?" % (nm, he),
                   Fc(1, 4), [Fc(3, 4), Fc(1, 3), Fc(1, 2)],
                   "There are 4 equal slices, so each slice is a quarter. %s eats 1 slice: <b>%s</b>." % (nm, fr(1, 4)), rnd))
    nm, he, his = P.next()
    its.append(mcq("A pizza is cut into 4 equal slices. %s eats 1 slice. What fraction of the pizza is <b>left</b>?" % nm,
                   Fc(3, 4), [Fc(1, 4), Fc(1, 3), Fc(2, 4)],
                   "4 − 1 = <b>3 slices</b> are left out of 4 equal slices. That is %s." % fr(3, 4), rnd))
    its.append(mcq("There are 30 children in a Year 2 class. Half of them have school dinners. How many children have school dinners?",
                   Nc(15, " children"), set_cands(30, 1, 2, " children"), e_set(30, 1, 2, " children"), rnd))
    its.append(mcq("How many minutes are in a quarter of an hour?", Nc(15, " minutes"),
                   [Nc(30, " minutes"), Nc(25, " minutes"), Nc(4, " minutes")],
                   "An hour has 60 minutes. Share 60 into 4 equal parts: 15 + 15 + 15 + 15 = 60. "
                   "So a quarter of an hour is <b>15 minutes</b>.", rnd))
    its.append(mcq("How many minutes are in half an hour?", Nc(30, " minutes"),
                   [Nc(50, " minutes"), Nc(15, " minutes"), Nc(2, " minutes")],
                   "An hour has 60 minutes. Half of 60 is <b>30</b>: 30 + 30 = 60.", rnd))
    nm, he, his = P.next()
    its.append(mcq("%s has 12 biscuits. %s eats %s of them. How many biscuits does %s eat?" % (nm, he.capitalize(), fr(1, 3), he),
                   Nc(4, " biscuits"), set_cands(12, 1, 3, " biscuits"), e_set(12, 1, 3, " biscuits"), rnd))
    nm, he, his = P.next()
    its.append(mcq("%s has 8 pencils. %s of them are red. How many red pencils are there?" % (nm, fr(3, 4)),
                   Nc(6, " pencils"), set_cands(8, 3, 4, " pencils"), e_set(8, 3, 4, " pencils"), rnd))
    nm, he, his = P.next()
    its.append(mcq("%s has 20p. %s spends half of it. How much does %s spend?" % (nm, he.capitalize(), he),
                   "10p", ["2p", "20p", "5p"],
                   "Half of 20p: share 20p into 2 equal parts. 10p + 10p = 20p, so the answer is <b>10p</b>.", rnd))
    nm, he, his = P.next()
    its.append(mcq("%s has 50p. %s gives half of it to %s brother. How much does %s give?" % (nm, he.capitalize(), his, he),
                   "25p", ["2p", "50p", "20p"],
                   "Half of 50p: 25p + 25p = 50p. So the answer is <b>25p</b>.", rnd))
    its.append(mcq("4 friends share 16 sweets equally. Each friend gets %s of the sweets. How many sweets does each friend get?" % fr(1, 4),
                   Nc(4, " sweets"), [Nc(12, " sweets"), Nc(16, " sweets"), Nc(5, " sweets")],
                   e_set(16, 1, 4, " sweets"), rnd))
    nm, he, his = P.next()
    its.append(mcq("%s has a ribbon 20 cm long. %s cuts it in half. How long is each piece?" % (nm, he.capitalize()),
                   Nc(10, " cm"), set_cands(20, 1, 2, " cm"), e_set(20, 1, 2, " cm"), rnd))
    its.append(mcq("A box has 12 eggs. %s of the eggs are brown. How many eggs are brown?" % fr(3, 4),
                   Nc(9, " eggs"), set_cands(12, 3, 4, " eggs"), e_set(12, 3, 4, " eggs"), rnd))
    (n1, _, _), (n2, _, _) = P.next(), P.next()
    its.append(mcq("Two cakes are the same size. %s eats %s of one cake. %s eats %s of the other cake. Who eats more?"
                   % (n1, fr(1, 3), n2, fr(1, 4)),
                   n1, [n2, "They eat the same", "You can’t tell"],
                   "A cake cut into 3 has bigger pieces than a cake cut into 4. %s is bigger than %s, so <b>%s</b> eats more."
                   % (fr(1, 3), fr(1, 4), n1), rnd))
    (n1, _, _), (n2, _, _) = P.next(), P.next()
    its.append(mcq("Two sandwiches are the same size. %s eats %s of one. %s eats %s of the other. Who eats more?"
                   % (n1, fr(1, 2), n2, fr(2, 4)),
                   "They eat the same", [n1, n2, "You can’t tell"],
                   "%s = %s. %s has more pieces, but they are smaller. They eat the <b>same amount</b>." % (fr(2, 4), fr(1, 2), n2), rnd))
    nm, he, his = P.next()
    its.append(mcq("%s cuts a sandwich into 2 pieces. One piece is big and one is small. %s says each piece is a half. Is %s right?"
                   % (nm, he.capitalize(), he),
                   "No, the pieces are not equal", ["Yes, there are 2 pieces", "No, each piece is a quarter", "Yes, it is cut once"],
                   "Halves must be <b>2 equal parts</b>. One piece is bigger, so they are not halves.", rnd))
    nm, he, his = P.next()
    its.append(mcq("%s has 20 apples. %s gives away %s of them. How many apples does %s give away?" % (nm, he.capitalize(), fr(1, 4), he),
                   Nc(5, " apples"), set_cands(20, 1, 4, " apples"), e_set(20, 1, 4, " apples"), rnd))
    nm, he, his = P.next()
    its.append(mcq("%s has 20 grapes. %s eats %s of them. How many grapes are <b>left</b>?" % (nm, he.capitalize(), fr(1, 4)),
                   Nc(15, " grapes"), [Nc(5, " grapes"), Nc(16, " grapes"), Nc(4, " grapes")],
                   "%s of 20 is 20 ÷ 4 = 5. %s eats 5 grapes. 20 − 5 = <b>15 grapes</b> are left (that is %s)."
                   % (fr(1, 4), nm, fr(3, 4)), rnd))
    its.append(mcq("There are 10 children in the playground. Half of them are girls. How many are boys?",
                   Nc(5, " boys"), [Nc(10, " boys"), Nc(2, " boys"), Nc(8, " boys")],
                   "Half of 10 is 5, so 5 are girls. The other half are boys: 10 − 5 = <b>5 boys</b>.", rnd))
    nm, he, his = P.next()
    its.append(mcq("Half of %s’s beads are blue. %s has 9 blue beads. How many beads does %s have altogether?" % (nm, he.capitalize(), he),
                   Nc(18, " beads"), [Nc(9, " beads"), Nc(11, " beads"), Nc(7, " beads")],
                   "9 beads are one half. The whole is 2 halves: 9 + 9 = <b>18 beads</b>. Check: half of 18 is 9.", rnd))
    (n1, h1, x1), (n2, _, _) = P.next(), P.next()
    its.append(mcq("%s has 9 stickers. %s gives %s of them to %s. How many stickers does %s get?" % (n1, h1.capitalize(), fr(1, 3), n2, n2),
                   Nc(3, " stickers"), set_cands(9, 1, 3, " stickers"), e_set(9, 1, 3, " stickers"), rnd))
    assert len(its) == 20, len(its)
    return {"title": "Fraction word problems", "items": its}


# ============================================================ lesson
def body_html():
    names_fig = svg_wrap(372, 140, "".join(
        [piece("square", 2, {0}, 10, 6, 100), piece("circle", 3, {0}, 136, 6, 100), piece("grid", 4, {0}, 262, 6, 100),
         txt(60, 132, "one half", 16), txt(186, 132, "one third", 16), txt(312, 132, "one quarter", 16)]),
        "one half of a square, one third of a circle and one quarter of a square shaded")
    eq_fig = svg_wrap(312, 112, "".join(
        [sfr(20, 24 + r * 56, 1 if r == 0 else 2, n, 16) for r, n in enumerate([2, 4])] +
        [bar_row(48, 6 + r * 56, 256, 42, n, set(range(n // 2))) for r, n in enumerate([2, 4])]),
        "one half and two quarters shaded on two bars of the same size")
    set_fig = ("<figure class='sn-fig'>" + groups_svg(4, 2, ring=1) +
               "<figcaption>8 counters in 4 equal groups. One group is " + fr(1, 4) + " of 8, which is 2.</figcaption></figure>")
    return (
        "<h2>Equal parts</h2>"
        "<p>A fraction is a part of a whole. The parts must be <b>equal</b> (the same size).</p>"
        "<figure class='sn-fig'>" + names_fig +
        "<figcaption>2 equal parts are halves. 3 equal parts are thirds. 4 equal parts are quarters.</figcaption></figure>"
        + table(["Equal parts", "Each part is", "We write"], [
            ["2", "one half", fr(1, 2)],
            ["3", "one third", fr(1, 3)],
            ["4", "one quarter", fr(1, 4)],
        ]) +
        "<p>The bottom number tells you how many equal parts. The top number tells you how many parts you have.</p>"
        "<h2>Two quarters and three quarters</h2>"
        "<figure class='sn-fig'>" + shape_svg("grid", 4, {0, 1, 2}) +
        "<figcaption>4 equal parts and 3 are shaded: " + fr(3, 4) + " is shaded.</figcaption></figure>"
        "<p>Two quarters are the same as one half: " + fr(2, 4) + " = " + fr(1, 2) + ".</p>"
        "<figure class='sn-fig'>" + eq_fig +
        "<figcaption>The shading stops at the same place.</figcaption></figure>"
        "<h2>Fractions of a set and a number</h2>"
        "<p>To find " + fr(1, 4) + " of a group, share it into <b>4 equal groups</b>. Count one group.</p>"
        + set_fig
        + ex("Example", "What is " + fr(1, 3) + " of 9?", "Share 9 into 3 equal groups: 3, 3 and 3. One group is 3.", "3")
        + ex("Example", "What is " + fr(3, 4) + " of 12?", "Share 12 into 4 equal groups of 3. Take 3 groups: 3 + 3 + 3 = 9.", "9")
        + ex("Example", "What is " + fr(1, 2) + " of 10 cm?", "Share 10 cm into 2 equal parts: 5 cm and 5 cm.", "5 cm")
        + "<h2>Common mistakes</h2>"
        + table(["Mistake", "What to do instead"], [
            ["Calling 2 unequal parts “halves”", "Halves must be <b>equal</b>"],
            ["Saying " + fr(1, 3) + " of 9 is 6", "6 is two groups. One group is 3"],
            ["Saying " + fr(3, 4) + " of 12 is 3", "3 is only one quarter. Take 3 groups: 9"],
            ["Thinking " + fr(1, 4) + " is bigger than " + fr(1, 3) + " because 4 is bigger", "More parts means <b>smaller</b> parts"],
            ["Counting the parts that are <b>not</b> shaded", "The top number counts the shaded parts"],
        ])
    )


FAQ = [
    {"q": "What fractions do Year 2 children learn?",
     "a": "Year 2 children learn halves, thirds and quarters: 1/2, 1/3, 1/4, 2/4 and 3/4. They find them of shapes, lengths, groups of objects and numbers, and learn that 2/4 is the same as 1/2."},
    {"q": "How do you find 1/3 of a number?",
     "a": "Share the number into 3 equal groups and count one group. For 1/3 of 12, make 3 groups of 4, so the answer is 4."},
    {"q": "Why is 2/4 the same as 1/2?",
     "a": "Cut two same-size shapes into 2 parts and into 4 parts. Shade 1 half and 2 quarters: the shading covers the same amount."},
    {"q": "Is 1/4 bigger than 1/3?",
     "a": "No. A whole cut into 4 equal parts has smaller parts than a whole cut into 3, so 1/3 is bigger than 1/4."},
]


def gen():
    rnd = random.Random(2207)
    SPOTS.left = []
    sets = [set_parts(rnd), set_quarters(rnd), set_objects(rnd), set_quantity(rnd), set_words(rnd)]
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
        "country": "uk", "subject": "maths", "grade": "year-2", "slug": "fractions", "sort": 7,
        "updated": UPDATED, "pdf_url": "",
        "title": "Year 2 Fractions",
        "seo_title": "Year 2 Fractions Worksheets: Halves, Thirds and Quarters of Shapes, Objects and Numbers",
        "short_title": "Fractions",
        "domain": "Fractions",
        "standard_code": "Year 2: Fractions",
        "standard_url": "https://www.gov.uk/government/publications/national-curriculum-in-england-mathematics-programmes-of-study",
        "standard_text": "Recognise, find, name and write fractions 1/3, 1/4, 2/4 and 3/4 of a length, shape, set of objects or quantity; write simple fractions for example, 1/2 of 6 = 3 and recognise the equivalence of 2/4 and 1/2.",
        "meta_desc": "Free Year 2 fractions worksheets for the National Curriculum: equal parts, halves, thirds and quarters of shapes, 2/4 = 1/2, fractions of a set of objects, fractions of numbers and lengths, and word problems. 100 questions with an answer key.",
        "key_big": "A fraction needs equal parts. 2 equal parts are halves, 3 are thirds and 4 are quarters.",
        "key_sub": "To find 1/4 of 8, share 8 into 4 equal groups: each group has 2. Two quarters are the same as one half.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, "fractions.json")
    mark_large(u, "(two bars|counters|four pictures|strip)")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(u, f, ensure_ascii=False, indent=1)
    print("wrote", path)
