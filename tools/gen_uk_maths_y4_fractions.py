# -*- coding: utf-8 -*-
"""
UK Year 4 Maths: Fractions (National Curriculum in England, Year 4: Fractions)
  python3 tools/gen_uk_maths_y4_fractions.py
Equivalent fractions (fraction wall, bars), families and missing numbers, a few improper
fractions and mixed numbers, adding and subtracting with the same denominator, fractions of
amounts (bar model) and word problems. Decimals are a separate unit.
Every choice carries its value; a wrong choice never equals the right value or another wrong one.
HTML attributes use single quotes (no backslashes in the JSON). British English.
"""
import json, math, os, random, re
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "uk", "maths", "year-4")
UPDATED = "2026-11-02"
FILL = "#4fae74"      # shaded / first part
FILL2 = "#f2b84b"     # second part
RED = "#c0392b"
LINE = "#2b2b2b"
GIRLS = ["Amelia", "Isla", "Freya", "Poppy", "Ava", "Aisha", "Lily", "Zara", "Grace", "Ruby", "Maya", "Evie"]
BOYS = ["Oliver", "Harry", "Mohammed", "Jack", "Arjun", "Noah", "George", "Leo", "Alfie", "Kai", "Ethan", "Charlie"]
WORD = {2: "halves", 3: "thirds", 4: "quarters", 5: "fifths", 6: "sixths", 7: "sevenths", 8: "eighths",
        9: "ninths", 10: "tenths", 11: "elevenths", 12: "twelfths", 14: "fourteenths", 15: "fifteenths", 16: "sixteenths",
        20: "twentieths"}
ONE = {2: "half", 3: "third", 4: "quarter", 5: "fifth", 6: "sixth", 7: "seventh", 8: "eighth", 9: "ninth",
       10: "tenth", 12: "twelfth"}


# ------------------------------------------------------------ numbers
def fr(a, b):
    return "<span class='fr'><span class='fn'>%s</span><span class='fd'>%s</span></span>" % (a, b)


def frq(b):
    return fr("<b>?</b>", b)


def frq_d(a):
    return fr(a, "<b>?</b>")


def mx(w, n, d):
    if n == 0:
        return str(w)
    if w == 0:
        return fr(n, d)
    return "%d %s" % (w, fr(n, d))


def Fc(a, b, unit=""):
    """Choice: fraction a/b (as written) with its value."""
    return (fr(a, b) + unit, F(a, b))


def Mc(w, n, d, unit=""):
    """Choice: mixed number w n/d (as written) with its value."""
    return (mx(w, n, d) + unit, F(w) + F(n, d))


def Nc(n, unit="", pre=""):
    """Choice: whole number."""
    return ("%s%s%s" % (pre, "{:,}".format(n), unit), F(n))


def num(n):
    return "{:,}".format(n)


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
def sfr(x, y, a, b, size=14, color=LINE):
    """Stacked fraction drawn in SVG, centred at x. y is the numerator baseline."""
    w = size * 0.62 * max(len(str(a)), len(str(b))) + 4
    return ("<text x='%.1f' y='%.1f' font-size='%d' font-weight='700' fill='%s' text-anchor='middle'>%s</text>"
            "<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='1.5'/>"
            "<text x='%.1f' y='%.1f' font-size='%d' font-weight='700' fill='%s' text-anchor='middle'>%s</text>"
            % (x, y, size, color, a, x - w / 2, y + 4, x + w / 2, y + 4, color, x, y + size + 4, size, color, b))


def bar_row(x0, y, W, H, n, k, crossed=(), fills=None):
    s = []
    for i in range(n):
        col = (fills[i] if fills and i < len(fills) else (FILL if i < k else "#fff"))
        x = x0 + i * W / n
        s.append("<rect x='%.1f' y='%.1f' width='%.2f' height='%d' fill='%s' stroke='%s' stroke-width='2.5'/>"
                 % (x, y, W / n, H, col, LINE))
        if i in crossed:
            cw = W / n
            r = min(cw, H) / 2 - min(cw, H) * 0.2
            cx, cy = x + cw / 2, y + H / 2
            s.append("<path d='M%.1f %.1f L%.1f %.1f M%.1f %.1f L%.1f %.1f' stroke='%s' stroke-width='3' stroke-linecap='round'/>"
                     % (cx - r, cy - r, cx + r, cy + r, cx - r, cy + r, cx + r, cy - r, RED))
    return "".join(s)


def two_bars_svg(n1, k1, n2, k2, W=260, H=40):
    s = bar_row(6, 6, W, H, n1, k1) + bar_row(6, 6 + H + 14, W, H, n2, k2)
    return svg_wrap(W + 12, 2 * H + 26, s, "two bars of the same size, top bar %d of %d parts shaded, bottom bar %d of %d parts shaded"
                    % (k1, n1, k2, n2))


def wall_svg(dens, shade=None, W=300, H=40):
    """Fraction wall: a row for 1 whole, then one row per denominator, every cell labelled.
    shade = (den, k): shade the first k cells of that row."""
    s = []
    x0 = 6
    for r, d in enumerate([1] + list(dens)):
        y = 6 + r * H
        k = shade[1] if shade and shade[0] == d else 0
        s.append(bar_row(x0, y, W, H, d, k))
        for i in range(d):
            cx = x0 + (i + 0.5) * W / d
            if d == 1:
                s.append("<text x='%.1f' y='%.1f' font-size='16' font-weight='700' fill='%s' text-anchor='middle'>1</text>"
                         % (cx, y + 26, LINE))
            else:
                s.append(sfr(cx, y + 16, 1, d, 14))
    lab = "fraction wall with rows for 1 whole and %s" % ", ".join(WORD[d] for d in dens)
    if shade:
        lab += ", %d %s shaded" % (shade[1], WORD[shade[0]] if shade[1] > 1 else ONE[shade[0]])
    return svg_wrap(W + 12, (len(dens) + 1) * H + 12, "".join(s), lab)


def add_bar_svg(d, x, y, W=280, H=44):
    fills = [FILL] * x + [FILL2] * y
    s = bar_row(6, 6, W, H, d, 0, fills=fills)
    s += "<rect x='6' y='6' width='%d' height='%d' fill='none' stroke='%s' stroke-width='3'/>" % (W, H, LINE)
    return svg_wrap(W + 12, H + 12, s, "bar of %d equal parts: %d green and %d yellow" % (d, x, y))


def sub_bar_svg(d, x, y, W=280, H=44):
    s = bar_row(6, 6, W, H, d, x, crossed=set(range(x - y, x)))
    s += "<rect x='6' y='6' width='%d' height='%d' fill='none' stroke='%s' stroke-width='3'/>" % (W, H, LINE)
    return svg_wrap(W + 12, H + 12, s, "bar of %d equal parts: %d shaded and %d of them crossed out" % (d, x, y))


def wholes_svg(d, N, cell=None, H=40, gap=14):
    """N parts of 1/d shaded across bars of d parts, side by side."""
    nb = -(-N // d)
    cell = cell or 30
    bw = cell * d
    s = []
    for b in range(nb):
        x0 = 6 + b * (bw + gap)
        k = min(d, N - b * d)
        s.append(bar_row(x0, 6, bw, H, d, k))
        s.append("<rect x='%.1f' y='6' width='%.1f' height='%d' fill='none' stroke='%s' stroke-width='3'/>" % (x0, bw, H, LINE))
    return svg_wrap(12 + nb * bw + (nb - 1) * gap, H + 12, "".join(s),
                    "%d bars of %d equal parts, %d parts shaded" % (nb, d, N))


def model_svg(T, b, k, W=300, H=36, label_total=None, parts_text=None):
    """Bar model: whole bar labelled T, then the same bar in b equal parts, k shaded, ? under the shaded parts.
    parts_text: write this in every part (for the lesson)."""
    x0, y1 = 6, 6
    s = ["<rect x='%d' y='%d' width='%d' height='%d' fill='#fff' stroke='%s' stroke-width='2.5'/>" % (x0, y1, W, H, LINE),
         "<text x='%.1f' y='%d' font-size='17' font-weight='700' fill='%s' text-anchor='middle'>%s</text>"
         % (x0 + W / 2, y1 + 24, LINE, label_total or num(T))]
    y2 = y1 + H + 10
    s.append(bar_row(x0, y2, W, H, b, k))
    if parts_text:
        for i in range(b):
            s.append("<text x='%.1f' y='%d' font-size='15' font-weight='700' fill='%s' text-anchor='middle'>%s</text>"
                     % (x0 + (i + 0.5) * W / b, y2 + 24, LINE, parts_text))
    xr = x0 + W * k / b
    yb = y2 + H + 6
    s.append("<path d='M%d %d L%d %d L%.1f %d L%.1f %d' fill='none' stroke='%s' stroke-width='2'/>"
             % (x0 + 1, yb, x0 + 1, yb + 8, xr - 1, yb + 8, xr - 1, yb, LINE))
    s.append("<text x='%.1f' y='%d' font-size='17' font-weight='700' fill='%s' text-anchor='middle'>%s</text>"
             % ((x0 + xr) / 2, yb + 27, LINE, "?" if not parts_text else num(T * k // b)))
    return svg_wrap(W + 12, yb + 34, "".join(s),
                    "bar model: a whole of %s, and the same bar in %d equal parts with %d shaded" % (num(T), b, k))


# ============================================================ set 1: equivalent fractions with diagrams
def set_diagrams(rnd):
    SPOTS.left = []
    its = []
    for a, b, d in [(1, 2, 4), (1, 3, 6), (3, 4, 8), (2, 5, 10), (1, 2, 8), (2, 3, 6), (1, 4, 8)]:
        n = d // b
        c = a * n
        q = (fig(two_bars_svg(b, a, d, c)) + "The bars are the same size and show the same amount.<br>%s = %s"
             % (fr(a, b), frq(d)))
        e = ("The bottom bar has %d equal parts, so each %s of the top bar is split into %d parts. "
             "%d shaded %s become%s %d × %d = <b>%d</b> shaded parts. So %s = %s."
             % (d, ONE[b], n, a, ONE[b] if a == 1 else WORD[b], "s" if a == 1 else "", a, n, c, fr(a, b), fr(c, d)))
        its.append(mcq(q, Nc(c), [Nc(a + (d - b)), Nc(a), Nc(d - c), Nc(d), Nc(c + 1), Nc(n)], e, rnd))

    for dens, (sd, k), t in [((2, 4, 8), (2, 1), 8), ((2, 4, 8), (4, 3), 8), ((3, 6), (3, 2), 6),
                              ((5, 10), (5, 1), 10), ((5, 10), (5, 4), 10), ((2, 4, 8), (4, 1), 8)]:
        n = t // sd
        c = k * n
        q = (fig(wall_svg(dens, (sd, k))) + "Use the fraction wall. %s is shaded. How many %s are equal to %s?"
             % (fr(k, sd), WORD[t], fr(k, sd)))
        e = ("Look down the fraction wall. %s lines up with <b>%d</b> %s, because each %s is the same as %d %s. "
             "So %s = %s." % (fr(k, sd), c, WORD[t] if c > 1 else ONE[t], ONE[sd], n, WORD[t], fr(k, sd), fr(c, t)))
        its.append(mcq(q, Nc(c), [Nc(k + (t - sd)), Nc(k), Nc(t - c), Nc(t), Nc(c + n)], e, rnd))

    SAME, TOP, BOT, CANT = "They are equal", "The top bar has more", "The bottom bar has more", "You can’t tell"
    for b, a, d, c in [(3, 2, 6, 4), (2, 1, 6, 3), (4, 3, 8, 5), (4, 2, 10, 5), (3, 1, 6, 3), (4, 1, 8, 3), (2, 1, 8, 3)]:
        x, y = F(a, b), F(c, d)
        right = SAME if x == y else (TOP if x > y else BOT)
        if x == y:
            e = ("Both bars are shaded up to the same place. The bottom bar has more parts, but each part is smaller, "
                 "so %s = %s." % (fr(a, b), fr(c, d)))
        else:
            eq = x * d
            if eq.denominator == 1:
                e = ("%s is the same as %d %s. The bottom bar has %d shaded, so the %s bar has more: %s %s %s. "
                     "More parts does not mean more shaded."
                     % (fr(a, b), eq.numerator, WORD[d], c, "top" if x > y else "bottom",
                        fr(a, b), "&gt;" if x > y else "&lt;", fr(c, d)))
            else:
                e = ("Look at where the shading ends: the %s bar is shaded further, so %s %s %s. "
                     "More parts does not mean more shaded." % ("top" if x > y else "bottom", fr(a, b), "&gt;" if x > y else "&lt;", fr(c, d)))
        its.append(mcq(fig(two_bars_svg(b, a, d, c)) + "The bars are the same size. Compare the shaded amounts.",
                       right, [SAME, TOP, BOT, CANT], e, rnd))
    assert len(its) == 20, len(its)
    return {"title": "Equivalent fractions with diagrams", "items": its}


# ============================================================ set 2: families and missing numbers
def set_families(rnd):
    SPOTS.left = []
    its = []
    for a, b, d in [(3, 4, 12), (2, 3, 9), (2, 5, 15), (5, 6, 12), (3, 8, 16), (1, 3, 12), (4, 5, 20), (3, 7, 14)]:
        n = d // b
        assert n * b == d
        c = a * n
        e = ("Look at the denominators: %d × <b>%d</b> = %d. Multiply the numerator by %d too: %d × %d = <b>%d</b>. "
             "So %s = %s." % (b, n, d, n, a, n, c, fr(a, b), fr(c, d)))
        its.append(mcq("%s = %s" % (fr(a, b), frq(d)), Nc(c), [Nc(a + (d - b)), Nc(a), Nc(n), Nc(d - c), Nc(c + n)], e, rnd))

    for a, b, c in [(2, 3, 8), (3, 4, 9), (2, 5, 6)]:
        n = c // a
        d = b * n
        assert n * a == c and b * c != d
        e = ("Look at the numerators: %d × <b>%d</b> = %d. Multiply the denominator by %d too: %d × %d = <b>%d</b>. "
             "So %s = %s." % (a, n, c, n, b, n, d, fr(a, b), fr(c, d)))
        its.append(mcq("%s = %s" % (fr(a, b), frq_d(c)), Nc(d), [Nc(b + (c - a)), Nc(b), Nc(b * c)], e, rnd))

    for a, b, n in [(3, 4, 3), (2, 5, 2), (5, 6, 2)]:
        e = ("Multiply the numerator <b>and</b> the denominator by the same number: %d × %d = %d and %d × %d = %d. "
             "So %s = %s. Multiplying only the numerator makes a bigger amount."
             % (a, n, a * n, b, n, b * n, fr(a, b), fr(a * n, b * n)))
        its.append(mcq("Which fraction is equal to %s?" % fr(a, b), Fc(a * n, b * n),
                       [Fc(a * n, b), Fc(a, b * n), Fc(a + n, b + n), Fc(b, a)], e, rnd))

    for (a, b), trues, bad, why in [
        ((1, 2), [(2, 4), (3, 6), (5, 10)], (2, 3), "1 was added to the numerator and the denominator of %s" % fr(1, 2)),
        ((1, 3), [(2, 6), (3, 9), (4, 12)], (3, 4), "2 was added to the numerator and the denominator of %s" % fr(1, 3)),
    ]:
        for t in trues:
            assert F(*t) == F(a, b)
        assert F(*bad) != F(a, b)
        e = ("%s is not equal to %s: %s. The others are in the family, because both numbers were multiplied by the same number."
             % (fr(*bad), fr(a, b), why))
        its.append(mcq("Which fraction is <b>not</b> in the same family as %s?" % fr(a, b), fr(*bad),
                       [fr(*t) for t in trues], e, rnd))

    # improper fractions and mixed numbers (a few)
    its.append(mcq(fig(wholes_svg(4, 5)) + "Each bar is 1 whole. %s are shaded. Write this as a mixed number." % (fr(5, 4)),
                   Mc(1, 1, 4), [Fc(4, 5), Mc(1, 1, 5), Mc(2, 1, 4), Mc(5, 1, 4)],
                   "%s = 1 whole. One more quarter is shaded. So %s = <b>1 %s</b>." % (fr(4, 4), fr(5, 4), fr(1, 4)), rnd))
    its.append(mcq("%s = ?" % fr(7, 4), Mc(1, 3, 4), [Mc(3, 1, 4), Mc(1, 4, 7), Mc(7, 1, 4), Fc(4, 7)],
                   "%s make 1 whole. 7 − 4 = 3 quarters are left over. So %s = <b>1 %s</b>." % (fr(4, 4), fr(7, 4), fr(3, 4)), rnd))
    its.append(mcq("1 %s = %s" % (fr(2, 3), frq(3)), Nc(5), [Nc(3), Nc(6), Nc(2)],
                   "1 whole = %s. Add the 2 thirds: 3 + 2 = <b>5</b>. So 1 %s = %s." % (fr(3, 3), fr(2, 3), fr(5, 3)), rnd))
    its.append(mcq("Which improper fraction is equal to 2 %s?" % fr(1, 2), Fc(5, 2),
                   [Fc(3, 2), Fc(2, 2), Fc(4, 2), Fc(21, 2)],
                   "2 wholes = %s. Add the half: 4 + 1 = 5 halves. So 2 %s = <b>%s</b>." % (fr(4, 2), fr(1, 2), fr(5, 2)), rnd))
    assert len(its) == 20, len(its)
    return {"title": "Equivalent fraction families and missing numbers", "items": its}


# ============================================================ set 3: add and subtract
def set_add_sub(rnd):
    SPOTS.left = []
    its = []
    # A: with a bar
    for x, y, d in [(2, 3, 7), (1, 4, 6), (3, 2, 8), (4, 5, 12)]:
        s = x + y
        e = ("The parts are all %s. Count them: %d + %d = <b>%d</b> %s. The denominator stays %d. So %s + %s = %s."
             % (WORD[d], x, y, s, WORD[d], d, fr(x, d), fr(y, d), fr(s, d)))
        its.append(mcq(fig(add_bar_svg(d, x, y)) + "%s + %s = ?" % (fr(x, d), fr(y, d)), Fc(s, d),
                       [Fc(s, 2 * d), Fc(abs(x - y), d), Fc(d - s, d)], e, rnd))
    x, y, d = 7, 3, 8
    its.append(mcq(fig(sub_bar_svg(d, x, y)) + "%s − %s = ?" % (fr(x, d), fr(y, d)), Fc(x - y, d),
                   [Fc(x + y, d), Fc(y, d), Fc(d - x, d)],
                   "%d eighths are shaded and %d are crossed out. %d − %d = <b>%d</b> eighths are left: %s."
                   % (x, y, x, y, x - y, fr(x - y, d)), rnd))
    # B: plain
    for x, y, d, op in [(1, 5, 9, "+"), (4, 3, 11, "+"), (3, 4, 10, "+"), (9, 4, 10, "−"), (5, 2, 6, "−"), (11, 7, 12, "−")]:
        if op == "+":
            s = x + y
            e = ("Add the numerators: %d + %d = <b>%d</b>. Keep the denominator: the parts are still %s. "
                 "So the answer is %s, not %s." % (x, y, s, WORD[d], fr(s, d), fr(s, 2 * d)))
            cands = [Fc(s, 2 * d), Fc(abs(x - y), d), Fc(s + 1, d), Fc(s, d + d)]
        else:
            s = x - y
            e = ("Subtract the numerators: %d − %d = <b>%d</b>. Keep the denominator: the parts are still %s. So the answer is %s."
                 % (x, y, s, WORD[d], fr(s, d)))
            cands = [Fc(x + y, d), Nc(s), Fc(y, d)]
        its.append(mcq("%s %s %s = ?" % (fr(x, d), op, fr(y, d)), Fc(s, d), cands, e, rnd))
    # C: from 1 whole
    for x, d in [(3, 8), (2, 5), (4, 9)]:
        e = ("1 whole = %s. Then %s − %s = <b>%s</b>." % (fr(d, d), fr(d, d), fr(x, d), fr(d - x, d)))
        its.append(mcq("1 − %s = ?" % fr(x, d), Fc(d - x, d), [Fc(x - 1, d), Fc(x, d), Fc(d + x, d)], e, rnd))
    # D: totals over 1
    for x, y, d in [(3, 4, 5), (5, 6, 8), (2, 2, 3)]:
        s = x + y
        r = s - d
        e = ("%s + %s = %s. %s make 1 whole, and %d − %d = %d %s left over. So the answer is <b>1 %s</b>."
             % (fr(x, d), fr(y, d), fr(s, d), fr(d, d), s, d, r, (WORD[d] + " are") if r > 1 else (ONE[d] + " is"), fr(r, d)))
        its.append(mcq("%s + %s = ?<br>Write the answer as a mixed number." % (fr(x, d), fr(y, d)), Mc(1, r, d),
                       [Fc(s, 2 * d), Mc(1, d - r, d), Mc(2, r, d), Mc(s, r, d)], e, rnd))
    # E: missing numbers
    its.append(mcq("%s + %s = %s" % (fr(2, 9), frq(9), fr(7, 9)), Nc(5), [Nc(9), Nc(7), Nc(2)],
                   "Think: 2 + <b>5</b> = 7. So %s + %s = %s." % (fr(2, 9), fr(5, 9), fr(7, 9)), rnd))
    its.append(mcq("%s − %s = %s" % (frq(10), fr(3, 10), fr(4, 10)), Nc(7), [Nc(1), Nc(4), Nc(3)],
                   "Use the inverse: 4 + 3 = <b>7</b>. So %s − %s = %s." % (fr(7, 10), fr(3, 10), fr(4, 10)), rnd))
    its.append(mcq("%s − %s = %s" % (fr(8, 12), frq(12), fr(3, 12)), Nc(5), [Nc(11), Nc(3), Nc(8)],
                   "Think: 8 − <b>5</b> = 3. So %s − %s = %s." % (fr(8, 12), fr(5, 12), fr(3, 12)), rnd))
    assert len(its) == 20, len(its)
    return {"title": "Add and subtract fractions with the same denominator", "items": its}


# ============================================================ set 4: fractions of amounts
def amount_cands(T, a, b, unit="", pre=""):
    ans = T * a // b
    c = [Nc(T // b, unit, pre)]
    if a > 1 and T % a == 0:
        c.append(Nc(T // a, unit, pre))
    c += [Nc(T - ans, unit, pre), Nc(T * a, unit, pre), Nc(T // b + a, unit, pre)]
    if a == 1:
        c = [Nc(T - b, unit, pre), Nc(T * b, unit, pre)] + ([Nc(T // 2, unit, pre)] if T % 2 == 0 else []) + [Nc(T + b, unit, pre)]
    return c


def e_amount(T, a, b, unit="", pre=""):
    one = T // b
    if a == 1:
        return ("To find %s, divide by the denominator: %s%s ÷ %d = <b>%s%s</b>."
                % (fr(1, b), pre, num(T), b, pre, num(one) + unit))
    return ("First find %s: %s%s ÷ %d = %s%s. Then multiply by the numerator: %s%s × %d = <b>%s%s</b>."
            % (fr(1, b), pre, num(T), b, pre, num(one) + unit, pre, num(one) + unit, a, pre, num(one * a) + unit))


def set_amounts(rnd):
    SPOTS.left = []
    its = []
    for b, T in [(5, 30), (3, 21), (4, 28), (6, 42), (8, 40)]:
        its.append(mcq(fig(model_svg(T, b, 1)) + "Find %s of %d." % (fr(1, b), T), Nc(T // b),
                       amount_cands(T, 1, b), e_amount(T, 1, b), rnd))
    for b, T in [(4, 36), (7, 35), (10, 60), (9, 54), (12, 48)]:
        its.append(mcq("What is %s of %d?" % (fr(1, b), T), Nc(T // b), amount_cands(T, 1, b), e_amount(T, 1, b), rnd))
    for a, b, T in [(3, 4, 24), (2, 5, 30), (2, 3, 18), (5, 6, 36), (3, 8, 40)]:
        its.append(mcq(fig(model_svg(T, b, a)) + "Find %s of %d." % (fr(a, b), T), Nc(T * a // b),
                       amount_cands(T, a, b), e_amount(T, a, b), rnd))
    for a, b, T, unit in [(2, 5, 35, " cm"), (3, 4, 1000, " g"), (4, 7, 63, ""), (5, 8, 48, ""), (3, 10, 90, " ml")]:
        its.append(mcq("What is %s of %s%s?" % (fr(a, b), num(T), unit), Nc(T * a // b, unit),
                       amount_cands(T, a, b, unit), e_amount(T, a, b, unit), rnd))
    assert len(its) == 20, len(its)
    return {"title": "Fractions of amounts", "items": its}


# ============================================================ set 5: word problems
def set_words(rnd):
    SPOTS.left = []
    its = []
    P = People(rnd)

    its.append(mcq("There are 32 pupils in a Year 4 class. %s of them have school dinners. How many pupils have school dinners?"
                   % fr(3, 8), Nc(12, " pupils"), [Nc(4, " pupils"), Nc(20, " pupils"), Nc(96, " pupils")],
                   e_amount(32, 3, 8, " pupils"), rnd))
    nm, he, his = P.next()
    its.append(mcq("%s has £40. %s spends %s of it on a new football. How much does the football cost?" % (nm, cap(he), fr(2, 5)),
                   Nc(16, pre="£"), [Nc(8, pre="£"), Nc(20, pre="£"), Nc(24, pre="£")],
                   e_amount(40, 2, 5, pre="£"), rnd))
    (n1, _, _), (n2, _, _) = P.next(), P.next()
    its.append(mcq("A pizza is cut into 8 equal slices. %s eats %s of the pizza and %s eats %s. What fraction of the pizza do they eat altogether?"
                   % (n1, fr(3, 8), n2, fr(2, 8)), Fc(5, 8), [Fc(5, 16), Fc(1, 8), Fc(3, 8)],
                   "The slices are all eighths. 3 + 2 = <b>5</b> eighths: %s. Keep the denominator 8." % fr(5, 8), rnd))
    nm, he, his = P.next()
    its.append(mcq("%s has a ribbon 60 cm long. %s uses %s of it to make a bow. How long is the piece for the bow?"
                   % (nm, cap(he), fr(3, 4)), Nc(45, " cm"), [Nc(15, " cm"), Nc(20, " cm"), Nc(180, " cm")],
                   e_amount(60, 3, 4, " cm"), rnd))
    nm, he, his = P.next()
    its.append(mcq("%s has %s m of ribbon. %s uses %s m for a card. How much ribbon is left?" % (nm, fr(9, 10), cap(he), fr(4, 10)),
                   Fc(5, 10, " m"), [Fc(13, 10, " m"), Fc(4, 10, " m"), Nc(5, " m")],
                   "9 − 4 = <b>5</b> tenths. The denominator stays 10, so %s m is left." % fr(5, 10), rnd))
    nm, he, his = P.next()
    its.append(mcq("%s practises the piano for %s of an hour. How many minutes is that?" % (nm, fr(3, 4)),
                   Nc(45, " minutes"), [Nc(15, " minutes"), Nc(75, " minutes"), Nc(20, " minutes")],
                   "There are 60 minutes in an hour (not 100). 60 ÷ 4 = 15, so %s of an hour is 15 minutes. "
                   "15 × 3 = <b>45 minutes</b>." % fr(1, 4), rnd))
    nm, he, his = P.next()
    its.append(mcq("A book has 48 pages. %s has read %s of it. How many pages does %s have left to read?" % (nm, fr(5, 6), he),
                   Nc(8, " pages"), [Nc(40, " pages"), Nc(43, " pages"), Nc(6, " pages")],
                   "%s of 48: 48 ÷ 6 = 8, so %s is 8 × 5 = 40 pages read. 48 − 40 = <b>8 pages</b> left. "
                   "(Quicker: %s is left, and %s of 48 is 8.)" % (fr(5, 6), fr(5, 6), fr(1, 6), fr(1, 6)), rnd))
    nm, he, his = P.next()
    its.append(mcq("A nature trail is 1,000 m long. %s has walked %s of it. How far has %s walked?" % (nm, fr(3, 10), he),
                   Nc(300, " m"), [Nc(100, " m"), Nc(30, " m"), Nc(700, " m")],
                   e_amount(1000, 3, 10, " m"), rnd))
    nm, he, his = P.next()
    its.append(mcq("%s has a bag of 24 sweets. %s of them are red. How many red sweets are there?" % (nm, fr(1, 3)),
                   Nc(8, " sweets"), [Nc(21, " sweets"), Nc(72, " sweets"), Nc(12, " sweets")],
                   e_amount(24, 1, 3, " sweets"), rnd))
    its.append(mcq("A school car park has 60 spaces. %s of the spaces are full. How many spaces are empty?" % fr(7, 10),
                   Nc(18, " spaces"), [Nc(42, " spaces"), Nc(6, " spaces"), Nc(53, " spaces")],
                   "%s of 60: 60 ÷ 10 = 6, and 6 × 7 = 42 spaces are full. 60 − 42 = <b>18 spaces</b> are empty."
                   % fr(7, 10), rnd))
    (n1, _, _), (n2, _, _) = P.next(), P.next()
    its.append(mcq("%s eats %s of a chocolate bar. %s eats %s of a bar of the same size. Who eats more?" % (n1, fr(2, 4), n2, fr(4, 8)),
                   "They eat the same", [n1, n2, "You can’t tell"],
                   "Multiply the numerator and denominator of %s by 2: %s = %s. %s eats more pieces, but they are smaller, "
                   "so they eat the same amount." % (fr(2, 4), fr(2, 4), fr(4, 8), n2), rnd))
    (n1, _, _), (n2, h2, _) = P.next(), P.next()
    its.append(mcq("%s eats %s of a pizza. %s eats %s of a pizza of the same size. Who eats more?" % (n1, fr(3, 4), n2, fr(5, 8)),
                   n1, [n2 + ", because 8 is bigger than 4", "They eat the same", "You can’t tell"],
                   "Change %s to eighths: %s = %s. %s is more than %s, so <b>%s</b> eats more. "
                   "A bigger denominator means smaller pieces." % (fr(3, 4), fr(3, 4), fr(6, 8), fr(6, 8), fr(5, 8), n1), rnd))
    nm, he, his = P.next()
    its.append(mcq("A jug holds 1 litre of water. %s pours out %s of a litre, then %s of a litre. What fraction of a litre is left in the jug?"
                   % (nm, fr(3, 10), fr(4, 10)), Fc(3, 10, " litre"), [Fc(7, 10, " litre"), Fc(1, 10, " litre"), Fc(7, 20, " litre")],
                   "%s pours out 3 + 4 = 7 tenths: %s. 1 litre = %s, and %s − %s = <b>%s</b> of a litre is left."
                   % (cap(he), fr(7, 10), fr(10, 10), fr(10, 10), fr(7, 10), fr(3, 10)), rnd))
    nm, he, his = P.next()
    its.append(mcq("%s runs %s km on Monday and %s km on Tuesday. How far does %s run altogether? Give the answer as a mixed number."
                   % (nm, fr(5, 8), fr(7, 8), he), Mc(1, 4, 8, " km"),
                   [Fc(12, 16, " km"), Fc(2, 8, " km"), Mc(2, 4, 8, " km")],
                   "5 + 7 = 12 eighths: %s. %s make 1 km, and 4 eighths are left over. So %s runs <b>1 %s km</b>."
                   % (fr(12, 8), fr(8, 8), he, fr(4, 8)), rnd))
    its.append(mcq("There are 25 pupils in a class. %s of them walk to school. How many pupils walk to school?" % fr(3, 5),
                   Nc(15, " pupils"), [Nc(5, " pupils"), Nc(10, " pupils"), Nc(75, " pupils")],
                   e_amount(25, 3, 5, " pupils"), rnd))
    nm, he, his = P.next()
    its.append(mcq("A football team scored 18 goals this term. %s scored %s of them. How many goals did %s score?" % (nm, fr(2, 9), he),
                   Nc(4, " goals"), [Nc(2, " goals"), Nc(9, " goals"), Nc(14, " goals")],
                   e_amount(18, 2, 9, " goals"), rnd))
    (n1, _, _), (n2, _, _) = P.next(), P.next()
    its.append(mcq("A packet has 20 biscuits. %s eats %s of them and %s eats %s of them. How many biscuits are left?"
                   % (n1, fr(1, 4), n2, fr(2, 4)), Nc(5, " biscuits"), [Nc(15, " biscuits"), Nc(10, " biscuits"), Nc(17, " biscuits")],
                   "Together they eat %s + %s = %s, so %s is left. 20 ÷ 4 = <b>5 biscuits</b> are left."
                   % (fr(1, 4), fr(2, 4), fr(3, 4), fr(1, 4)), rnd))
    nm, he, his = P.next()
    its.append(mcq("%s has £1. %s spends %s of it on sweets. How much does %s spend?" % (nm, cap(he), fr(3, 4), he),
                   Nc(75, "p"), [Nc(25, "p"), Nc(34, "p"), Nc(30, "p")],
                   "£1 = 100p. %s of 100p: 100 ÷ 4 = 25p, and 25p × 3 = <b>75p</b>." % fr(3, 4), rnd))
    nm, he, his = P.next()
    its.append(mcq("A cake is cut into 12 equal pieces. %s’s family eats %s of the cake. How many pieces do they eat?" % (nm, fr(2, 3)),
                   Nc(8, " pieces"), [Nc(4, " pieces"), Nc(6, " pieces"), Nc(24, " pieces")],
                   e_amount(12, 2, 3, " pieces"), rnd))
    nm, he, his = P.next()
    its.append(mcq("%s says %s + %s = %s. What went wrong?" % (nm, fr(2, 7), fr(3, 7), fr(5, 14)),
                   "%s added the denominators" % cap(he),
                   ["%s should multiply the numerators" % cap(he), "Nothing. %s is right" % cap(he),
                    "%s should add 2 to both numbers" % cap(he)],
                   "The parts are sevenths, and they stay sevenths. Add only the numerators: 2 + 3 = 5. "
                   "So %s + %s = <b>%s</b>." % (fr(2, 7), fr(3, 7), fr(5, 7)), rnd))
    assert len(its) == 20, len(its)
    return {"title": "Fraction word problems", "items": its}


# ============================================================ lesson
def body_html():
    wall = wall_svg((2, 4, 8), (4, 3))
    return (
        "<h2>Numerator and denominator</h2>"
        "<p>The <b>denominator</b> (bottom number) tells you how many equal parts the whole is split into. "
        "The <b>numerator</b> (top number) tells you how many of those parts you have. "
        "In " + fr(3, 4) + ", the whole is split into 4 equal parts and we have 3 of them.</p>"
        "<h2>Equivalent fractions</h2>"
        "<p><b>Equivalent fractions</b> are worth the same amount. A <b>fraction wall</b> shows them: "
        "look straight down to find fractions that line up.</p>"
        "<figure class='sn-fig'>" + wall +
        "<figcaption>" + fr(3, 4) + " lines up with " + fr(6, 8) + ". Also " + fr(1, 2) + " = " + fr(2, 4) + " = " + fr(4, 8) +
        ".</figcaption></figure>"
        "<p>To find an equivalent fraction, <b>multiply or divide the numerator and the denominator by the same number</b>.</p>"
        + ex("Example", "Find the missing number: " + fr(3, 4) + " = " + frq(12),
             "4 × 3 = 12, so multiply the denominator by 3. Do the same to the numerator: 3 × 3 = 9.", "9")
        + "<p>Fractions in one <b>family</b> are all equal: " + fr(1, 3) + " = " + fr(2, 6) + " = " + fr(3, 9) + " = " + fr(4, 12) + ".</p>"
        "<p>When the numerator is bigger than the denominator, the fraction is more than 1 whole. "
        + fr(5, 4) + " is 4 quarters (1 whole) and 1 more quarter, so " + fr(5, 4) + " = 1 " + fr(1, 4) + ". This is a <b>mixed number</b>.</p>"
        "<h2>Adding and subtracting</h2>"
        "<p>When the denominators are the same, the parts are the same size. "
        "Add or subtract the <b>numerators</b>. Keep the <b>denominator</b>.</p>"
        "<figure class='sn-fig'>" + add_bar_svg(7, 2, 3) +
        "<figcaption>" + fr(2, 7) + " + " + fr(3, 7) + " = " + fr(5, 7) + ": 2 green sevenths and 3 yellow sevenths make 5 sevenths.</figcaption></figure>"
        + ex("Example", fr(9, 10) + " − " + fr(4, 10) + " = ?", "Subtract the numerators: 9 − 4 = 5. The parts are still tenths.", fr(5, 10))
        + ex("Example", fr(3, 5) + " + " + fr(4, 5) + " = ?",
             "3 + 4 = 7, so the total is " + fr(7, 5) + ". " + fr(5, 5) + " is 1 whole, and 2 fifths are left over.", "1 " + fr(2, 5))
        + "<h2>Fractions of amounts</h2>"
        "<p>To find a fraction of an amount, <b>divide by the denominator</b> to find one part, "
        "then <b>multiply by the numerator</b>.</p>"
        "<figure class='sn-fig'>" + model_svg(24, 4, 3, parts_text="6") +
        "<figcaption>" + fr(3, 4) + " of 24: 24 ÷ 4 = 6 in each part. 3 parts are 6 × 3 = 18.</figcaption></figure>"
        + ex("Example", "What is " + fr(2, 5) + " of £40?", "£40 ÷ 5 = £8 for one fifth. Two fifths: £8 × 2 = £16.", "£16")
        + "<h2>Common mistakes</h2>"
        + table(["Mistake", "What to do instead"], [
            ["Adding the denominators: " + fr(2, 7) + " + " + fr(3, 7) + " = " + fr(5, 14),
             "Keep the denominator: " + fr(2, 7) + " + " + fr(3, 7) + " = " + fr(5, 7)],
            ["Multiplying only the numerator: " + fr(3, 4) + " = " + fr(9, 4),
             "Multiply <b>both</b> numbers: " + fr(3, 4) + " = " + fr(9, 12)],
            ["For " + fr(3, 4) + " of 24, stopping at one part (6) or dividing by 3 (8)",
             "Divide by the denominator, then multiply by the numerator: 24 ÷ 4 × 3 = 18"],
            ["Thinking " + fr(1, 8) + " is bigger than " + fr(1, 4) + " because 8 is bigger",
             "A bigger denominator means more parts, so each part is <b>smaller</b>"],
        ])
    )


FAQ = [
    {"q": "What fractions should a Year 4 child know?",
     "a": "In Year 4 children find families of equivalent fractions (1/2 = 2/4 = 4/8), add and subtract fractions with the same denominator, and find fractions of amounts such as 3/4 of 24. They also start to meet tenths and hundredths as decimals."},
    {"q": "How do you find a fraction of an amount?",
     "a": "Divide by the denominator to find one part, then multiply by the numerator. For 3/4 of 24: 24 ÷ 4 = 6, and 6 × 3 = 18."},
    {"q": "Why don’t you add the denominators when adding fractions?",
     "a": "The denominator tells you the size of the parts, and adding does not change their size. 2/7 + 3/7 is 5 sevenths, so the answer is 5/7, not 5/14."},
    {"q": "What is a fraction wall?",
     "a": "A fraction wall is a set of bars of the same length, each split into a different number of equal parts. Fractions that line up, such as 1/2 and 4/8, are equivalent."},
]


def gen():
    rnd = random.Random(4408)
    SPOTS.left = []
    sets = [set_diagrams(rnd), set_families(rnd), set_add_sub(rnd), set_amounts(rnd), set_words(rnd)]
    for s in sets:
        assert len(s["items"]) == 20, (s["title"], len(s["items"]))
        cnt = [0, 0, 0, 0]
        for it in s["items"]:
            assert len(set(it["c"])) == 4, it
            cnt[it["a"]] += 1
        assert cnt == [5, 5, 5, 5], (s["title"], cnt)
    return {
        "country": "uk", "subject": "maths", "grade": "year-4", "slug": "fractions", "sort": 8,
        "updated": UPDATED, "pdf_url": "",
        "title": "Year 4 Fractions",
        "seo_title": "Year 4 Fractions Worksheets: Equivalent Fractions, Adding and Subtracting, Fractions of Amounts (Free, with Answers)",
        "short_title": "Fractions",
        "domain": "Fractions",
        "standard_code": "Year 4: Fractions",
        "standard_url": "https://www.gov.uk/government/publications/national-curriculum-in-england-mathematics-programmes-of-study",
        "standard_text": "Recognise and show, using diagrams, families of common equivalent fractions; solve problems involving increasingly harder fractions to calculate quantities, and fractions to divide quantities, including non-unit fractions where the answer is a whole number; add and subtract fractions with the same denominator.",
        "meta_desc": "Free Year 4 fractions worksheets for the National Curriculum: equivalent fractions on a fraction wall, missing numbers, adding and subtracting with the same denominator, fractions of amounts and word problems. 100 questions with an answer key.",
        "key_big": "Same denominator: add the numerators and keep the denominator. Fraction of an amount: divide by the denominator, then multiply by the numerator.",
        "key_sub": "2/7 + 3/7 = 5/7, not 5/14. 3/4 of 24: 24 ÷ 4 = 6, then 6 × 3 = 18. Equivalent fractions: multiply the numerator and denominator by the same number, so 3/4 = 9/12.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, "fractions.json")
    mark_large(u, "(fraction wall|bar model)")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(u, f, ensure_ascii=False, indent=1)
    print("wrote", path)
