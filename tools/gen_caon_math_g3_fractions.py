# -*- coding: utf-8 -*-
"""
CA Grade 3 Math: Fractions and Fair Shares (Ontario Mathematics Curriculum 2020, B1.7, B1.8, B2.8)
  python3 tools/gen_ca_math_g3_fractions.py
Halves, thirds, fourths, fifths, sixths, eighths and tenths. Fair-share problems (up to 20 items,
2, 3, 4, 5, 6, 8 or 10 sharers) with whole-number, mixed-number and fractional results,
comparing unit fractions, counting by unit fractions. Canadian English; Ontario terms ("fourths", "mixed numbers").
Every choice carries its value; a wrong choice never equals the right value or another wrong one.
HTML attributes use single quotes (no backslashes in the JSON).
"""
import json, math, os, random, re
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "ca-on", "math", "grade-3")
UPDATED = "2026-11-02"
FILL = "#4fae74"      # shaded part
RED = "#d6453b"
LINE = "#2b2b2b"
WORD = {2: "halves", 3: "thirds", 4: "fourths", 5: "fifths", 6: "sixths", 8: "eighths", 10: "tenths"}
ONE = {2: "half", 3: "third", 4: "fourth", 5: "fifth", 6: "sixth", 8: "eighth", 10: "tenth"}


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


def share(m, n):
    """m items shared by n: (whole part, leftover items)."""
    return divmod(m, n)


def Sc(m, n, unit=""):
    w, r = share(m, n)
    return Mc(w, r, n, unit)


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


def sfr(x, y, a, b, size=15):
    """Stacked fraction drawn in SVG, centred at x. y is the numerator baseline."""
    w = size * 0.62 * max(len(str(a)), len(str(b))) + 4
    return (txt(x, y, a, size) +
            "<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='1.5'/>"
            % (x - w / 2, y + 4, x + w / 2, y + 4, LINE) + txt(x, y + size + 4, b, size))


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


def bar_svg(n, shaded, W=260, H=50, widths=None, label=None):
    return svg_wrap(W + 12, H + 12, bar_row(6, 6, W, H, n, shaded, widths),
                    label or "bar split into %d equal parts with %d shaded" % (n, len(shaded)))


def pie(cx, cy, r, n, shaded, sw=2.5):
    if n == 1:
        return ("<circle cx='%.1f' cy='%.1f' r='%d' fill='%s' stroke='%s' stroke-width='%s'/>"
                % (cx, cy, r, FILL if 0 in shaded else "#fff", LINE, sw))
    s = []
    for i in range(n):
        a0 = math.radians(-90 + 360.0 * i / n)
        a1 = math.radians(-90 + 360.0 * (i + 1) / n)
        x0, y0 = cx + r * math.cos(a0), cy + r * math.sin(a0)
        x1, y1 = cx + r * math.cos(a1), cy + r * math.sin(a1)
        s.append("<path d='M%.1f %.1f L%.1f %.1f A%d %d 0 0 1 %.1f %.1f Z' fill='%s' stroke='%s' stroke-width='%s' stroke-linejoin='round'/>"
                 % (cx, cy, x0, y0, r, r, x1, y1, FILL if i in shaded else "#fff", LINE, sw))
    return "".join(s)


def circle_svg(n, shaded, r=62):
    d = 2 * r + 12
    return svg_wrap(d, d, pie(r + 6, r + 6, r, n, shaded), "circle split into %d equal parts with %d shaded" % (n, len(shaded)))


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


def two_bars_svg(n1, k1, n2, k2, W=260, H=40):
    s = bar_row(6, 6, W, H, n1, set(range(k1))) + bar_row(6, 6 + H + 14, W, H, n2, set(range(k2)))
    return svg_wrap(W + 12, 2 * H + 26, s, "two bars of the same size, top bar %d of %d parts shaded, bottom bar %d of %d parts shaded"
                    % (k1, n1, k2, n2))


def wholes_svg(d, k, H=40, W=200):
    """Bars that are each 1 whole, split into d parts; the first k parts (over all bars) are shaded."""
    nb = -(-k // d)
    s = []
    for b in range(nb):
        sh = set(i for i in range(d) if b * d + i < k)
        s.append(bar_row(6, 6 + b * (H + 12), W, H, d, sh))
    return svg_wrap(W + 12, nb * H + (nb - 1) * 12 + 12, "".join(s),
                    "%d bars, each 1 whole split into %d equal parts, %d parts shaded" % (nb, d, k))


def line2_svg(d, k, W=380):
    """Number line 0..2, each whole in d equal spaces, red dot k spaces from 0."""
    L, R, Y = 24, W - 24, 40
    N = 2 * d

    def X(i):
        return L + (R - L) * i / N
    s = ["<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='2.5'/>" % (L, Y, R, Y, LINE)]
    for i in range(N + 1):
        whole = i % d == 0
        s.append("<line x1='%.1f' y1='%d' x2='%.1f' y2='%d' stroke='%s' stroke-width='%s'/>"
                 % (X(i), Y - (13 if whole else 9), X(i), Y + (13 if whole else 9), LINE, "2.5" if whole else "2"))
        if whole:
            s.append(txt(X(i), Y + 36, str(i // d), 17))
    s.append("<circle cx='%.1f' cy='%d' r='8' fill='%s'/>" % (X(k), Y, RED))
    return svg_wrap(W, Y + 46, "".join(s), "number line from 0 to 2, each whole split into %d equal spaces" % d)


def share_svg(m, n, kind, per_row=4):
    """m items shared by n people. Whole items go out first; each leftover item is cut into n equal pieces.
    One person's share is shaded."""
    w, r = share(m, n)
    s = []
    if kind == "pizza":
        R, cw, ch = 26, 64, 62
    else:
        R, cw, ch = 0, 92, 48
    rows = -(-m // per_row)
    cols = min(m, per_row)
    for i in range(m):
        x0 = 6 + (i % per_row) * cw
        y0 = 6 + (i // per_row) * ch
        if i < w * n:
            parts, sh = 1, ({0} if i < w else set())
        else:
            parts, sh = n, {0}
        if kind == "pizza":
            s.append(pie(x0 + R + 2, y0 + R + 2, R, parts, sh, sw=2))
        else:
            s.append(bar_row(x0, y0, 80, 36, parts, sh, sw=2))
    Wd = 12 + (cols - 1) * cw + (2 * R + 4 if kind == "pizza" else 80)
    Hd = 12 + (rows - 1) * ch + (2 * R + 4 if kind == "pizza" else 36)
    return svg_wrap(Wd, Hd, "".join(s), "shared items: %d %s shared by %d, one share shaded" % (m, kind, n))


UNEQ = {3: [0.2, 0.35, 0.45], 4: [0.15, 0.2, 0.25, 0.4], 5: [0.1, 0.15, 0.2, 0.25, 0.3],
        6: [0.1, 0.22, 0.12, 0.2, 0.16, 0.2], 8: [0.08, 0.16, 0.1, 0.14, 0.12, 0.18, 0.1, 0.12]}


def pic_item(rnd, a, b, good, bad, q=None):
    """'Which picture shows a/b shaded?' good: spec; bad: [(spec, why)]."""
    pos = SPOTS.next(rnd)
    order = [x[0] for x in bad[:pos]] + [good] + [x[0] for x in bad[pos:]]
    letters = [L for i, L in enumerate("ABCD") if i != pos]
    why = " ".join("%s %s." % (L, d) for L, (_, d) in zip(letters, bad))
    e = ("%s needs <b>%d equal parts</b> with <b>%d</b> shaded. That is picture <b>%s</b>. %s"
         % (fr(a, b), b, a, "ABCD"[pos], why))
    return mcq_abcd(fig(four_bars_svg(order)) + (q or "Which picture shows %s shaded?" % fr(a, b)), pos, e)


# ============================================================ set 1: name fractions of shapes
def set_names(rnd):
    SPOTS.left = []
    its = []
    for n, kind in [(2, "circle"), (4, "grid"), (3, "bar"), (6, "circle"), (5, "bar"), (8, "grid"), (10, "bar"), (8, "circle")]:
        sh = {rnd.randrange(n)} if kind == "grid" else {0}
        e = ("The %s has <b>%d equal parts</b>, so the bottom number is %d. "
             "<b>1 part</b> is shaded, so the top number is 1. The answer is %s, one %s."
             % (SHAPE[kind], n, n, fr(1, n), ONE[n]))
        cands = [Fc(n - 1, n), Fc(1, n - 1) if n > 2 else None, Fc(1, n + 1), Nc(n), Fc(1, n + 2)]
        its.append(mcq(fig(shape_svg(n, sh, kind)) + "What fraction of the %s is shaded?" % SHAPE[kind],
                       Fc(1, n), cands, e, rnd))

    for n, kind, wrong in [(8, "circle", [6, 4, 10]), (5, "bar", [4, 6, 10]), (6, "grid", [3, 8, 5])]:
        e = ("Count the parts: there are <b>%d equal parts</b>. %d equal parts are called <b>%s</b>."
             % (n, n, WORD[n]))
        its.append(mcq(fig(shape_svg(n, set(), kind)) + "The %s is cut into equal parts. What are the parts called?" % SHAPE[kind],
                       WORD[n], [WORD[x] for x in wrong], e, rnd))

    for n, wrong in [(4, ["one four", "one third", "four fourths"]), (6, ["one six", "one fifth", "six sixths"]),
                     (10, ["one ten", "one eighth", "ten tenths"])]:
        e = ("%d equal parts are called <b>%s</b>. Each part is one %s, %s. %s %s make the whole shape."
             % (n, WORD[n], ONE[n], fr(1, n), {4: "Four", 6: "Six", 10: "Ten"}[n], WORD[n]))
        its.append(mcq("A shape is cut into %d equal parts. What is each part called?" % n, "one " + ONE[n], wrong, e, rnd))

    for n, bad in [
        (4, [((5, {0}, None), "has 5 parts, so it shows %s" % fr(1, 5)), ((4, {0, 1, 2}, None), "shows %s" % fr(3, 4)),
             ((4, {0}, UNEQ[4]), "has 4 parts, but they are <b>not equal</b>")]),
        (6, [((6, {0}, UNEQ[6]), "has 6 parts, but they are <b>not equal</b>"),
             ((8, {0}, None), "has 8 parts, so it shows %s" % fr(1, 8)), ((6, {0, 1}, None), "shows %s" % fr(2, 6))]),
        (8, [((8, {0, 1}, None), "shows %s" % fr(2, 8)), ((6, {0}, None), "has 6 parts, so it shows %s" % fr(1, 6)),
             ((8, {0}, UNEQ[8]), "has 8 parts, but they are <b>not equal</b>")]),
    ]:
        its.append(pic_item(rnd, 1, n, (n, {0}, None), bad))

    for n, ws, ok in [(4, [0.16, 0.34, 0.2, 0.3], False), (6, None, True), (3, [0.25, 0.25, 0.5], False)]:
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
    return {"title": "Name fractions of shapes", "items": its}


# ============================================================ set 2: fair shares
ITEM = {"pizza": ("pizza", "pizzas"), "sandwich": ("sandwich", "sandwiches"), "granola": ("granola bar", "granola bars"),
        "pancake": ("pancake", "pancakes"), "brownie": ("brownie", "brownies"), "sub": ("sub", "subs"),
        "muffin": ("muffin", "muffins"), "orange": ("orange", "oranges"), "pie": ("pie", "pies")}


def e_share(m, n, it):
    one, many = ITEM[it]
    w, r = share(m, n)
    if r == 0:
        return ("Share %d %s into <b>%d equal groups</b>: %d ÷ %d = <b>%d</b>. Each person gets %d %s."
                % (m, many, n, m, n, w, w, one if w == 1 else many))
    if m == 1:
        return ("Cut the %s into <b>%d equal pieces</b> (%s). Each person gets 1 piece: <b>%s</b> of a %s."
                % (one, n, WORD[n], fr(1, n), one))
    if w == 0:
        return ("Cut each %s into <b>%d equal pieces</b> (%s). Each person gets 1 piece from each %s. "
                "There %s %d %s, so each person gets <b>%s</b> of a %s."
                % (one, n, WORD[n], one, "is" if m == 1 else "are", m, one if m == 1 else many, fr(m, n), one))
    return ("First give out whole %s: %d ÷ %d = %d each, with %d %s left. Cut %s into %d equal pieces. "
            "Each person gets %s more. So each person gets <b>%s</b> %s."
            % (many, m, n, w, r, one if r == 1 else many, "it" if r == 1 else "each one", n,
               fr(r, n) if r == 1 else "%d pieces, %s" % (r, fr(r, n)), mx(w, r, n), many if w >= 1 else one))


def share_cands(m, n):
    w, r = share(m, n)
    if r == 0:
        return [Nc(n), Nc(m - n), Nc(w + 1), Nc(m + n), Nc(w - 1) if w > 1 else None]
    if m == 1:
        return [Nc(n), Fc(1, n + 1), Fc(1, n - 1), Fc(n - 1, n)]
    if w == 0:
        return [Fc(n, m), Fc(1, n), Fc(1, m), Fc(m, n + m), Fc(m - 1, n) if m > 1 else None]
    return [Nc(w), Nc(w + 1), Mc(w, r, m), Mc(w, 1, n) if r > 1 else None, Fc(n, m), Mc(w, r, n + 1)]


def set_shares(rnd):
    SPOTS.left = []
    its = []
    # whole-number shares
    for m, n, it in [(12, 4, "muffin"), (15, 5, "orange"), (16, 8, "granola"), (18, 6, "brownie")]:
        one, many = ITEM[it]
        its.append(mcq("%d %s are shared equally by %d friends. How many %s does each friend get?" % (m, many, n, many),
                       Nc(m // n), share_cands(m, n), e_share(m, n, it), rnd))
    # fractional shares, with a picture
    for m, n, it in [(1, 6, "pizza"), (2, 3, "sandwich"), (3, 4, "pizza"), (2, 5, "granola"), (5, 6, "pizza"), (3, 8, "pizza")]:
        one, many = ITEM[it]
        kind = "pizza" if it == "pizza" else "bar"
        q = (fig(share_svg(m, n, kind)) + "%d %s %s shared equally by %d friends. The shaded part is one friend’s share. "
             "How much %s does each friend get?" % (m, one if m == 1 else many, "is" if m == 1 else "are", n,
                                                   "pizza" if it == "pizza" else "of a " + one))
        its.append(mcq(q, Sc(m, n), share_cands(m, n), e_share(m, n, it), rnd))
    # mixed-number shares
    for m, n, it, pic in [(3, 2, "pancake", True), (5, 2, "sandwich", True), (4, 3, "pizza", True),
                          (7, 4, "pizza", True), (11, 4, "pancake", False), (13, 6, "muffin", False)]:
        one, many = ITEM[it]
        q = "%d %s are shared equally by %d friends. How many %s does each friend get?" % (m, many, n, many)
        if pic:
            kind = "pizza" if it in ("pizza", "pancake") else "bar"
            q = fig(share_svg(m, n, kind)) + q.replace(" How many", " The shaded parts are one friend’s share. How many")
        its.append(mcq(q, Sc(m, n), share_cands(m, n), e_share(m, n, it), rnd))
    # more or less than 1
    for m, n in [(3, 4), (6, 5)]:
        right = "Less than 1 pizza" if m < n else "More than 1 pizza"
        e = ("Compare the number of pizzas with the number of people. %d pizzas for %d people: " % (m, n) +
             ("there are <b>fewer pizzas than people</b>, so each person gets less than 1 pizza (%s)." % fr(m, n) if m < n
              else "there are <b>more pizzas than people</b>, so each person gets 1 pizza and a bit more (%s)." % mx(1, m - n, n)))
        its.append(mcq("%d friends share %d pizzas equally. Does each friend get more or less than 1 pizza?" % (n, m),
                       right, ["More than 1 pizza" if m < n else "Less than 1 pizza", "Exactly 1 pizza",
                               "Exactly %d pizzas" % m], e, rnd))
    # count the pieces
    for m, n, it in [(3, 4, "granola"), (5, 8, "pie")]:
        one, many = ITEM[it]
        e = ("Each %s is cut into %d equal pieces. Each friend gets <b>1 piece from each %s</b>. "
             "There are %d %s, so each friend gets <b>%d %s</b>, which is %s of a %s."
             % (one, n, one, m, many, m, WORD[n], fr(m, n), one))
        its.append(mcq("%d friends share %d %s equally. Each %s is cut into %s. How many %s does each friend get?"
                       % (n, m, many, one, WORD[n], WORD[n]),
                       Nc(m, " " + WORD[n]), [Nc(n, " " + WORD[n]), Nc(1, " " + ONE[n]), Nc(m * n, " " + WORD[n]),
                                              Nc(n - m, " " + WORD[n])], e, rnd))
    assert len(its) == 20, len(its)
    return {"title": "Fair shares", "items": its}


# ============================================================ set 3: compare unit fractions
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
    for n1, n2 in [(3, 5), (8, 4), (2, 6), (10, 5)]:
        big, small = min(n1, n2), max(n1, n2)
        e = ("The top bar has %d parts and the bottom bar has %d parts. <b>Fewer parts means bigger parts</b>, "
             "so %s is bigger than %s." % (n1, n2, fr(1, big), fr(1, small)))
        its.append(mcq(fig(two_bars_svg(n1, 1, n2, 1)) + "The bars are the same size. Which shaded part is bigger?",
                       Fc(1, big), [Fc(1, small), "They are the same size", "You can’t tell"], e, rnd))
    for b, d in [(4, 3), (2, 8), (6, 10), (5, 3), (8, 6)]:
        right, ch = cmp_choices(1, b, 1, d)
        x, y = (b, d) if b < d else (d, b)
        e = ("Both fractions have 1 on top. A whole cut into %d parts has bigger parts than a whole cut into %d parts. "
             "So %s." % (x, y, right))
        its.append(mcq("Compare the fractions. Choose &lt;, &gt; or =.", right, ch, e, rnd))
    for want, opts in [("largest", [2, 10, 5, 3]), ("smallest", [8, 2, 4, 6]), ("largest", [6, 10, 8, 4])]:
        ans = min(opts) if want == "largest" else max(opts)
        e = ("%s The <b>%s</b> bottom number means the %s parts. %s is the %s."
             % ("A unit fraction has 1 on top.", "smallest" if want == "largest" else "biggest",
                "biggest" if want == "largest" else "smallest", fr(1, ans), want))
        its.append(mcq("Which unit fraction is the <b>%s</b>?" % want, Fc(1, ans), [Fc(1, x) for x in opts if x != ans], e, rnd))
    for ds in [(2, 8, 4), (10, 3, 6)]:
        inc = sorted(ds, reverse=True)       # least to greatest: biggest denominator first
        dec = sorted(ds)
        s = lambda o: ", ".join(fr(1, x) for x in o)
        mid = [inc[0], inc[2], inc[1]]
        e = ("Order from least to greatest. The <b>biggest</b> bottom number is the <b>smallest</b> fraction, so start with %s. "
             "The order is %s." % (fr(1, inc[0]), s(inc)))
        its.append(mcq("Order from least to greatest: %s" % s(ds), s(inc), [s(dec), s(mid), s([dec[1], dec[0], dec[2]])], e, rnd))
    for n1, n2, food, a1, a2 in [(4, 6, "pizza", "Zoe", "Liam"), (3, 8, "pan of brownies", "Maya", "Owen"),
                                 (10, 5, "cake", "Priya", "Noah")]:
        big = a1 if n1 < n2 else a2
        nb, ns = min(n1, n2), max(n1, n2)
        other = a2 if big == a1 else a1
        e = ("A %s shared by %d gives bigger pieces than one shared by %d. %s &gt; %s, so <b>%s’s group</b> gets bigger pieces."
             % (food, nb, ns, fr(1, nb), fr(1, ns), big))
        its.append(mcq("%s’s group of %d shares a %s equally. %s’s group of %d shares the same size %s. "
                       "Whose group gets bigger pieces?" % (a1, n1, food, a2, n2, food),
                       "%s’s group" % big, ["%s’s group, because %d is bigger" % (other, ns), "They get the same size",
                                            "You can’t tell"], e, rnd))
    for good, bads in [((8, 4), [(2, 4), (3, 10), (5, 6)]), ((3, 2), [(4, 5), (6, 8), (2, 10)]),
                       ((10, 6), [(2, 8), (3, 5), (4, 6)])]:
        assert good[0] > good[1] and all(b[0] < b[1] for b in bads)
        st = lambda p: "%s &lt; %s" % (fr(1, p[0]), fr(1, p[1]))
        e = ("Check each one. A bigger bottom number means a <b>smaller</b> unit fraction. %s is true, because %d &gt; %d."
             % (st(good), good[0], good[1]))
        its.append(mcq("Which one is <b>true</b>?", st(good), [st(b) for b in bads], e, rnd))
    assert len(its) == 20, len(its)
    return {"title": "Compare unit fractions", "items": its}


# ============================================================ set 4: count unit fractions
def plus(k, n):
    return " + ".join([fr(1, n)] * k)


def set_counting(rnd):
    SPOTS.left = []
    its = []
    for k, n in [(3, 4), (2, 5), (5, 6), (5, 5)]:
        ans = Fc(k, n) if k < n else Nc(1)
        e = ("%d %s make <b>%s</b>. The parts stay %s, so the bottom number stays %d. Do not add the bottom numbers."
             % (k, WORD[n], fr(k, n), WORD[n], n))
        if k == n:
            e += " %s is 1 whole." % fr(n, n)
        its.append(mcq(plus(k, n) + " = ?", ans, [Fc(k, k * n), Fc(1, k * n), Fc(1, n), Fc(n, k), Fc(k - 1, n)], e, rnd))
    for k, n in [(3, 8), (4, 10)]:
        right = (plus(k, n), F(k, n))
        e = "%s means <b>%d %s</b>, so add %s %d times." % (fr(k, n), k, WORD[n], fr(1, n), k)
        its.append(mcq("Which addition is the same as %s?" % fr(k, n), right,
                       [(plus(k - 1, n), F(k - 1, n)), (plus(k + 1, n), F(k + 1, n)), (plus(k, k), F(1))], e, rnd))
    for k, n in [(5, 6), (7, 10)]:
        e = "%s means <b>%d %s</b>: %d lots of %s." % (fr(k, n), k, WORD[n], k, fr(1, n))
        its.append(mcq("How many %s make %s?" % (fr(1, n), fr(k, n)), Nc(k), [Nc(n), Nc(1), Nc(n - k), Nc(k + n)], e, rnd))
    for n, wrong in [(4, [1, 2, 8]), (6, [1, 3, 12])]:
        e = "1 whole cut into %s has <b>%d</b> equal parts: %s = 1." % (WORD[n], n, fr(n, n))
        its.append(mcq("How many %s make 1 whole?" % WORD[n], Nc(n), [Nc(x) for x in wrong], e, rnd))
    its.append(pic_item(rnd, 3, 6, (6, {0, 1, 2}, None), [
        ((8, {0, 1, 2}, None), "has 8 parts, so it shows %s" % fr(3, 8)),
        ((6, {0}, None), "shows only %s" % fr(1, 6)),
        ((6, {0, 1, 2}, UNEQ[6]), "has 6 parts, but they are <b>not equal</b>")],
        q="Which picture shows %s?" % plus(3, 6)))
    # counting sequences
    seqs = [
        (4, [1, 2, 3], Fc(4, 4), [Fc(4, 5), Fc(3, 4), Fc(4, 8)], "The bottom number stays 4. The top number goes up by 1: 1, 2, 3, <b>4</b>. %s is 1 whole." % fr(4, 4)),
        (8, [3, 4, 5], Fc(6, 8), [Fc(6, 9), Fc(5, 9), Fc(7, 8)], "The bottom number stays 8. The top number goes up by 1: 3, 4, 5, <b>6</b>."),
    ]
    for n, ks, right, wrong, e in seqs:
        its.append(mcq("Count by %s. What comes next?<br>%s, <b>?</b>" % (WORD[n], ", ".join(fr(k, n) for k in ks)),
                       right, wrong, e, rnd))
    its.append(mcq("Count by halves. What comes next?<br>%s, 1, %s, <b>?</b>" % (fr(1, 2), mx(1, 1, 2)),
                   Nc(2), [Mc(2, 1, 2), Nc(3), Mc(1, 1, 4)],
                   "Each step adds %s. %s + %s = <b>2</b>, because two halves make 1 whole." % (fr(1, 2), mx(1, 1, 2), fr(1, 2)), rnd))
    # more than one whole, with pictures
    for d, k in [(4, 5), (2, 3), (3, 5), (8, 11)]:
        w, r = divmod(k, d)
        e = ("Each bar is 1 whole cut into %d equal parts. <b>%d %s</b> are shaded. %d %s make 1 whole, "
             "and %d more %s %s. So %s are shaded: <b>%s</b>."
             % (d, k, WORD[d], d, WORD[d], r, ONE[d] if r == 1 else WORD[d], "is " + fr(r, d) if r else "", plus(k, d) if k <= 5 else "%d %s" % (k, WORD[d]), mx(w, r, d)))
        its.append(mcq(fig(wholes_svg(d, k)) + "Each bar is 1 whole. How much is shaded?", Mc(w, r, d),
                       [Fc(k, 2 * d), Fc(r, d), Nc(k), Mc(w, r, 2 * d), Mc(w, r + 1, d) if r + 1 < d else None], e, rnd))
    # number line beyond 1
    for d, k in [(4, 5), (3, 5)]:
        w, r = divmod(k, d)
        e = ("Each whole has <b>%d equal spaces</b>, so each space is %s. The dot is %d spaces from 0: "
             "%d %s is 1 whole and %d more is %s. The dot is at <b>%s</b>."
             % (d, fr(1, d), k, d, WORD[d], r, fr(r, d), mx(w, r, d)))
        its.append(mcq(fig(line2_svg(d, k)) + "Count by %s. What number is at the red dot?" % WORD[d], Mc(w, r, d),
                       [Fc(k, 2 * d), Fc(r, d), Mc(w, r - 1, d) if r > 1 else Nc(1), Mc(w, r + 1, d), Mc(w, r, 2 * d)], e, rnd))
    assert len(its) == 20, len(its)
    return {"title": "Count by unit fractions", "items": its}


# ============================================================ set 5: word problems
def set_words(rnd):
    SPOTS.left = []
    its = []
    W = []

    def add(q, right, cands, e):
        W.append((q, right, cands, e))

    add("Liam and 3 friends share 3 pizzas equally at a birthday party. How much pizza does each person get?",
        Fc(3, 4), [Fc(4, 3), Fc(1, 4), Fc(1, 3)],
        "Liam and 3 friends are <b>4 people</b>. Cut each pizza into fourths. Each person gets 1 piece from each of the 3 pizzas: <b>%s</b> of a pizza." % fr(3, 4))
    add("Olivia and Noah share 5 pancakes equally at breakfast. How many pancakes does each child get?",
        Sc(5, 2), [Nc(2), Nc(3), Mc(2, 1, 5)],
        "5 ÷ 2 = 2 each, with 1 pancake left. Cut it into halves. Each child gets <b>%s</b> pancakes." % mx(2, 1, 2))
    add("On a canoe trip, 3 friends share 2 granola bars equally. How much of a granola bar does each friend get?",
        Fc(2, 3), [Fc(3, 2), Fc(1, 3), Fc(1, 2)],
        "Cut each granola bar into thirds. Each friend gets 1 third from each bar: %s + %s = <b>%s</b>." % (fr(1, 3), fr(1, 3), fr(2, 3)))
    add("Owen and 3 friends share 20 hockey cards equally. How many cards does each person get?",
        Nc(5, " cards"), [Nc(4, " cards"), Nc(16, " cards"), Nc(10, " cards"), Nc(6, " cards")],
        "Owen and 3 friends are <b>4 people</b>. 20 ÷ 4 = <b>5 cards</b> each.")
    add("At hockey practice, 8 players share 5 oranges equally. How much orange does each player get?",
        Fc(5, 8), [Fc(8, 5), Fc(1, 8), Fc(1, 5)],
        "Cut each orange into eighths. Each player gets 1 piece from each of the 5 oranges: <b>%s</b> of an orange." % fr(5, 8))
    add("On a field trip, 4 students share 7 sandwiches equally. How many sandwiches does each student get?",
        Sc(7, 4), [Nc(1), Nc(2), Mc(1, 3, 7)],
        "7 ÷ 4 = 1 each, with 3 sandwiches left. Cut each one into fourths. Each student gets 3 more fourths: <b>%s</b> sandwiches." % mx(1, 3, 4))
    add("After soccer, 4 players share 9 muffins equally. How many muffins does each player get?",
        Sc(9, 4), [Nc(2), Nc(3), Mc(2, 1, 9)],
        "9 ÷ 4 = 2 each, with 1 muffin left. Cut it into fourths. Each player gets <b>%s</b> muffins." % mx(2, 1, 4))
    add("Emma and Aiden share 7 maple cookies equally. How many cookies does each child get?",
        Sc(7, 2), [Nc(3), Nc(4), Mc(3, 1, 7)],
        "7 ÷ 2 = 3 each, with 1 cookie left. Cut it in half. Each child gets <b>%s</b> cookies." % mx(3, 1, 2))
    add("Mateo shares 3 subs equally with 4 friends. How much of a sub does each person get?",
        Fc(3, 5), [Fc(3, 4), Fc(5, 3), Fc(1, 5)],
        "Mateo and 4 friends are <b>5 people</b>. Cut each sub into fifths. Each person gets 1 piece from each sub: <b>%s</b> of a sub." % fr(3, 5))
    add("10 friends share 3 pizzas equally. How much pizza does each friend get?",
        Fc(3, 10), [Fc(10, 3), Fc(1, 10), Fc(1, 3)],
        "Cut each pizza into tenths. Each friend gets 1 piece from each of the 3 pizzas: <b>%s</b> of a pizza." % fr(3, 10))
    add("At a class party, 10 students share 12 pizzas equally. Does each student get more or less than 1 pizza?",
        "More than 1 pizza", ["Less than 1 pizza", "Exactly 1 pizza", "Exactly 12 pizzas"],
        "There are <b>more pizzas than students</b>. Each student gets 1 pizza. The 2 pizzas left are cut into tenths, so each student gets %s pizzas." % mx(1, 2, 10))
    add("Zoe’s group of 3 shares a pan of lasagna. Ethan’s group of 5 shares the same size pan. Whose group gets bigger pieces?",
        "Zoe’s group", ["Ethan’s group, because 5 is bigger", "They get the same size", "You can’t tell"],
        "Fewer people means bigger pieces. %s &gt; %s, so <b>Zoe’s group</b> gets bigger pieces." % (fr(1, 3), fr(1, 5)))
    add("Arjun says %s of a pizza is more than %s of the same pizza, because 8 is more than 4. Is he right?" % (fr(1, 8), fr(1, 4)),
        "No. %s is more." % fr(1, 4), ["Yes. 8 is more than 4.", "No. They are the same.", "Yes. Eighths are bigger."],
        "A pizza cut into 8 pieces has smaller pieces than a pizza cut into 4 pieces. So %s &gt; %s." % (fr(1, 4), fr(1, 8)))
    add("Jayden cuts a pizza into 4 pieces. The pieces are different sizes. He says each piece is %s. Is he right?" % fr(1, 4),
        "No. The pieces are not equal.", ["Yes. There are 4 pieces.", "No. Each piece is %s." % fr(1, 3), "Yes. Each piece is one part."],
        "Fourths must be <b>4 equal parts</b>. The pieces are different sizes, so they are not fourths.")
    add("A tourtière is cut into 8 equal pieces. The family eats 5 pieces. What fraction of the tourtière do they eat?",
        Fc(5, 8), [Fc(3, 8), Fc(8, 5), Fc(5, 13)],
        "There are 8 equal pieces, so the bottom number is 8. They eat 5 pieces: <b>%s</b>." % fr(5, 8))
    add("A pizza is cut into 6 equal slices. Chloe’s family eats 4 slices. What fraction of the pizza is <b>left</b>?",
        Fc(2, 6), [Fc(4, 6), Fc(2, 4), Fc(1, 6)],
        "6 − 4 = <b>2 slices</b> are left out of 6 equal slices. That is %s of the pizza." % fr(2, 6))
    add("A pan of maple fudge is cut into 10 equal pieces. Priya eats 1 piece, then 1 more, then 1 more. How much of the pan does she eat?",
        Fc(3, 10), [Fc(7, 10), Fc(1, 10), Fc(10, 3)],
        "Each piece is %s. %s = <b>%s</b>. The pieces stay tenths, so the bottom number stays 10." % (fr(1, 10), plus(3, 10), fr(3, 10)))
    add("The Terry Fox Run route at school has 5 equal parts. Each part is %s of the route. Leah’s class has walked 3 parts. What fraction of the route have they walked?" % fr(1, 5),
        Fc(3, 5), [Fc(3, 15), Fc(2, 5), Fc(5, 3)],
        "3 parts of %s each: %s = <b>%s</b>." % (fr(1, 5), plus(3, 5), fr(3, 5)))
    add("Hana skates %s of a lap around the rink, 4 times. How many laps does she skate?" % fr(1, 3),
        Mc(1, 1, 3, " laps"), [Fc(4, 12, " lap"), Nc(4, " laps"), Fc(3, 4, " lap")],
        "%s is 4 thirds. 3 thirds make 1 whole lap, and 1 more third is %s. She skates <b>%s laps</b>."
        % (plus(4, 3), fr(1, 3), mx(1, 1, 3)))
    add("Kai has 2 granola bars. Each bar is cut into fourths. He eats 5 fourths. How many bars does he eat?",
        Mc(1, 1, 4, " bars"), [Fc(5, 8, " bar"), Fc(1, 4, " bar"), Nc(5, " bars")],
        "4 fourths make 1 whole bar. 5 fourths is 1 whole bar and %s more: <b>%s bars</b>." % (fr(1, 4), mx(1, 1, 4)))
    assert len(W) == 20, len(W)
    for q, right, cands, e in W:
        its.append(mcq(q, right, cands, e, rnd))
    return {"title": "Fraction and fair-share word problems", "items": its}


# ============================================================ lesson
def body_html():
    dens = [2, 3, 4, 5, 6, 8, 10]
    unit_fig = svg_wrap(372, 6 + len(dens) * 50, "".join(
        [sfr(22, 22 + r * 50, 1, n, 15) for r, n in enumerate(dens)] +
        [bar_row(56, 6 + r * 50, 300, 38, n, {0}) for r, n in enumerate(dens)]),
        "bars of the same size showing one half, one third, one fourth, one fifth, one sixth, one eighth and one tenth")
    names = table(["Equal parts", "Name", "One part"],
                  [[str(n), WORD[n], "one %s, %s" % (ONE[n], fr(1, n))] for n in dens])
    share1 = ("<figure class='sn-fig'>" + share_svg(3, 4, "pizza") +
              "<figcaption>3 pizzas shared by 4 friends. Cut each pizza into fourths. One friend gets the shaded pieces: "
              + fr(3, 4) + " of a pizza.</figcaption></figure>")
    share2 = ("<figure class='sn-fig'>" + share_svg(5, 2, "bar") +
              "<figcaption>5 sandwiches shared by 2 friends. Each gets 2 whole sandwiches and " + fr(1, 2) +
              " of the last one: " + mx(2, 1, 2) + " sandwiches.</figcaption></figure>")
    count_fig = ("<figure class='sn-fig'>" + wholes_svg(4, 5) +
                 "<figcaption>5 fourths are shaded. 4 fourths make 1 whole, so 5 fourths is " + mx(1, 1, 4) + ".</figcaption></figure>")
    return (
        "<h2>Equal parts</h2>"
        "<p>A fraction is <b>part of a whole</b>. The whole must be cut into <b>equal parts</b>.</p>"
        "<p>The bottom number tells how many equal parts make the whole. The top number tells how many parts you have.</p>"
        + names +
        "<h2>Fair shares</h2>"
        "<p>A fair share means everyone gets <b>the same amount</b>. Give out whole items first. "
        "Then cut each leftover item into as many equal pieces as there are people.</p>"
        + share1 + share2 +
        ex("Example", "12 muffins are shared by 4 friends.", "12 ÷ 4 = 3. Nothing is left over.", "3 muffins each")
        + ex("Example", "2 granola bars are shared by 3 friends.",
             "Fewer bars than friends, so each gets less than 1. Cut each bar into thirds. Each friend gets 1 third from each bar.",
             fr(2, 3) + " of a granola bar")
        + "<h2>Compare unit fractions</h2>"
        "<p>A <b>unit fraction</b> has 1 on top. <b>More sharers means smaller pieces.</b> "
        "So the bigger the bottom number, the smaller the fraction.</p>"
        "<figure class='sn-fig'>" + unit_fig +
        "<figcaption>The bars are the same size. " + fr(1, 2) + " is the biggest part and " + fr(1, 10) +
        " is the smallest.</figcaption></figure>"
        + ex("Example", "Compare " + fr(1, 3) + " and " + fr(1, 5) + ".", "A whole cut into 3 parts has bigger parts than a whole cut into 5 parts.",
             fr(1, 3) + " &gt; " + fr(1, 5))
        + "<h2>Count by unit fractions</h2>"
        "<p>" + fr(3, 4) + " means 3 fourths: " + plus(3, 4) + " = " + fr(3, 4) + ". The parts stay fourths, so the bottom number stays 4.</p>"
        "<p>Keep counting past 1 whole: " + ", ".join([fr(1, 4), fr(2, 4), fr(3, 4), "1", mx(1, 1, 4)]) +
        ". A whole number and a fraction together, like " + mx(1, 1, 4) + ", is a <b>mixed number</b>.</p>"
        + count_fig
        + "<h2>Common mistakes</h2>"
        + table(["Mistake", "What to do instead"], [
            ["Calling unequal parts “fourths” or “thirds”", "Fractions need <b>equal</b> parts"],
            ["Thinking " + fr(1, 8) + " is bigger than " + fr(1, 4) + " because 8 is bigger than 4",
             "More parts means <b>smaller</b> parts, so " + fr(1, 8) + " &lt; " + fr(1, 4)],
            ["Writing " + fr(4, 3) + " for 3 pizzas shared by 4", "The number of sharers goes on the bottom: " + fr(3, 4)],
            ["Leaving out the leftover: 5 sandwiches for 2 is “2 each”", "Cut the leftover sandwich too: " + mx(2, 1, 2) + " each"],
            ["Adding the bottom numbers: " + fr(1, 4) + " + " + fr(1, 4) + " = " + fr(2, 8), "The parts stay fourths: " + fr(2, 4)],
            ["Forgetting to count yourself: “Mateo and 4 friends” is 4 people", "Count everyone who shares: 5 people"],
        ])
    )


FAQ = [
    {"q": "What fractions do Grade 3 students learn in Ontario?",
     "a": "In the Ontario math curriculum, Grade 3 students work with halves, thirds, fourths, fifths, sixths, eighths and tenths. They use drawings to solve fair-share problems, compare unit fractions and count by unit fractions, including mixed numbers like 1 1/4."},
    {"q": "What is a fair-share problem in Grade 3 math?",
     "a": "A fair-share problem shares items equally, like 3 pizzas shared by 4 friends. Students cut each pizza into fourths and find that each friend gets 3/4 of a pizza; the answer can be a whole number, a fraction or a mixed number."},
    {"q": "Why is 1/3 bigger than 1/5?",
     "a": "Share the same pizza by 3 people and by 5 people. With fewer people each piece is bigger, so 1/3 is bigger than 1/5."},
    {"q": "Are fractions on the Grade 3 EQAO math assessment?",
     "a": "The Grade 3 EQAO math assessment is based on the Ontario curriculum, and fractions are part of the Number strand, so fraction questions can appear. Practising fair shares, comparing and counting fractions with pictures helps."},
]


def gen():
    rnd = random.Random(33805)
    SPOTS.left = []
    sets = [set_names(rnd), set_shares(rnd), set_compare(rnd), set_counting(rnd), set_words(rnd)]
    for s in sets:
        assert len(s["items"]) == 20, (s["title"], len(s["items"]))
        cnt = [0, 0, 0, 0]
        for it in s["items"]:
            assert len(set(it["c"])) == 4, it
            cnt[it["a"]] += 1
        assert cnt == [5, 5, 5, 5], (s["title"], cnt)
    return {
        "country": "ca-on", "subject": "math", "grade": "grade-3", "slug": "fractions-and-fair-shares", "sort": 5,
        "updated": UPDATED, "pdf_url": "",
        "title": "Grade 3 Fractions and Fair Shares",
        "seo_title": "Grade 3 Fractions and Fair Shares Worksheets: Free Math Practice with Answer Key (Ontario Curriculum)",
        "short_title": "Fractions and Fair Shares",
        "domain": "Number",
        "standard_code": "Grade 3: B1.7",
        "standard_url": "https://www.dcp.edu.gov.on.ca/en/curriculum/elementary-mathematics",
        "standard_text": "Use drawings to represent, solve, and compare the results of fair-share problems that involve sharing up to 20 items among 2, 3, 4, 5, 6, 8, and 10 sharers, including problems that result in whole numbers, mixed numbers, and fractional amounts",
        "meta_desc": "Free Grade 3 math worksheets on fractions and fair shares for the Ontario curriculum: name halves to tenths, share pizzas fairly, compare unit fractions and count by unit fractions. 100 questions with an answer key, great EQAO practice.",
        "key_big": "Fractions need equal parts. More sharers means smaller pieces.",
        "key_sub": "3 pizzas shared by 4 friends: cut each pizza into fourths, and each friend gets 3/4 of a pizza. 1/4 + 1/4 + 1/4 = 3/4.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, "fractions-and-fair-shares.json")
    mark_large(u, "(number line|two bars|shared items|four pictures|[0-9]+ bars)")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(u, f, ensure_ascii=False, indent=1)
    print("wrote", path)
