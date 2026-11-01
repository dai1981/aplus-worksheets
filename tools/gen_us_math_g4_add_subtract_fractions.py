# -*- coding: utf-8 -*-
"""
US Grade 4 Math: Add and Subtract Fractions and Mixed Numbers (4.NF.B.3)
  python tools/gen_us_math_g4_add_subtract_fractions.py
Like denominators only: 2, 3, 4, 5, 6, 8, 10, 12.
Answers keep the denominator of the problem (4/8 is not simplified to 1/2), and the
choices never contain a second form of the correct value.
Amounts are whole numbers of 1/d pieces: N = 11, d = 4 means 2 3/4.
HTML attributes use single quotes (no backslashes in the JSON).
"""
import json, math, os, random, re
from fractions import Fraction

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "us", "math", "grade-4")
UPDATED = "2026-11-02"
GREEN = "#006633"
FILL = "#4fae74"      # first part
FILL2 = "#f2b84b"     # second part
RED = "#c0392b"
LINE = "#2b2b2b"
GIRLS = ["Maya", "Ava", "Mia", "Zoe", "Lily", "Emma", "Nora", "Ruby", "Sofia", "Grace"]
BOYS = ["Leo", "Noah", "Eli", "Sam", "Ben", "Omar", "Kai", "Jack", "Luis", "Owen"]
WORD = {2: "halves", 3: "thirds", 4: "fourths", 5: "fifths", 6: "sixths", 8: "eighths", 10: "tenths", 12: "twelfths"}


# ------------------------------------------------------------ numbers
def fr(a, b):
    return "<span class='fr'><span class='fn'>%s</span><span class='fd'>%d</span></span>" % (a, b)


def mx(w, n, d):
    """Whole part w and fraction n/d written as given (no renaming): '3 12/8', '5/8', '2'."""
    if n == 0:
        return str(w)
    if w == 0:
        return fr(n, d)
    return "%d %s" % (w, fr(n, d))


def mixed(N, d):
    """N pieces of 1/d as a mixed number in simplest whole-number form (fraction part < 1)."""
    w, r = divmod(N, d)
    return mx(w, r, d)


def C(w, n, d):
    """A choice: (html, value)."""
    return (mx(w, n, d), Fraction(w) + Fraction(n, d))


def CN(N, d):
    return (mixed(N, d), Fraction(N, d))


def amt(N, d, one, many):
    """'3/4 mile', '1 mile', '1 1/2 miles'."""
    return "%s %s" % (mixed(N, d), one if N <= d else many)


def plus(*parts):
    return " + ".join(parts)


def unit_sum(k, d):
    return plus(*([fr(1, d)] * k))


# ------------------------------------------------------------ helpers
def mcq(q, correct, cands, e, rnd, same_value_ok=False):
    """correct and cands are (html, value) pairs or plain strings. A candidate with the same
    value as the correct answer is never used (it would also be right)."""
    if isinstance(correct, tuple):
        cs, cv = correct
    else:
        cs, cv = correct, None
    seen = {cs}
    vals = set()
    pick = []
    for c in cands:
        if c is None:
            continue
        if isinstance(c, tuple):
            s, v = c
            if v is not None and (v <= 0 or (cv is not None and v == cv)):
                continue
            if v is not None and v in vals and not same_value_ok:
                continue                      # two forms of the same wrong value
            vals.add(v)
        else:
            s = c
        if s in seen or not s:
            continue
        seen.add(s)
        pick.append(s)
        if len(pick) == 3:
            break
    assert len(pick) == 3, (q, cs, cands)
    ch = pick + [cs]
    rnd.shuffle(ch)
    return {"q": q, "c": ch, "a": ch.index(cs), "e": e}


def fig(svg):
    return "<div class='qfig'>" + svg + "</div>"


def svg_wrap(w, h, body, label):
    return ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 %d %d' width='%d' height='%d' "
            "role='img' aria-label='%s'>%s</svg>" % (w, h, w, h, label, body))


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
def bars_svg(d, nbars, segs, crossed=(), cell=None, gap=12, side=False, label="fraction bars"):
    """nbars bars of d equal cells (each bar is one whole). segs = [(count, color)] fill cells in
    order across the bars. crossed = cell indexes with a red X (taken away)."""
    if cell is None:
        cell = 260.0 / d
    H = 40
    bw = cell * d
    s = []
    i = 0
    colors = []
    for k, col in segs:
        colors += [col] * k
    for b in range(nbars):
        x0 = 6 + (b * (bw + gap) if side else 0)
        y0 = 6 + (0 if side else b * (H + gap))
        for c in range(d):
            col = colors[i] if i < len(colors) else "#fff"
            x = x0 + c * cell
            s.append("<rect x='%.1f' y='%d' width='%.1f' height='%d' fill='%s' stroke='%s' stroke-width='2'/>"
                     % (x, y0, cell, H, col, LINE))
            if i in crossed:
                p = min(cell, H) * 0.22
                cx, cy = x + cell / 2, y0 + H / 2
                r = min(cell, H) / 2 - p
                s.append("<path d='M%.1f %.1f L%.1f %.1f M%.1f %.1f L%.1f %.1f' stroke='%s' stroke-width='3' stroke-linecap='round'/>"
                         % (cx - r, cy - r, cx + r, cy + r, cx - r, cy + r, cx + r, cy - r, RED))
            i += 1
        # thicker outline for the whole
        s.append("<rect x='%.1f' y='%d' width='%.1f' height='%d' fill='none' stroke='%s' stroke-width='3'/>" % (x0, y0, bw, H, LINE))
    if side:
        W = 12 + nbars * bw + (nbars - 1) * gap
        Ht = H + 12
    else:
        W = 12 + bw
        Ht = 12 + nbars * H + (nbars - 1) * gap
    return svg_wrap(int(math.ceil(W)), Ht, "".join(s), label)


def arc(x0, x1, y, h, col):
    """Jump arrow from x0 to x1 above the line at y."""
    cx, cy = (x0 + x1) / 2.0, y - 2 * h
    s = "<path d='M%.1f %d Q%.1f %.1f %.1f %d' fill='none' stroke='%s' stroke-width='2.6'/>" % (x0, y - 3, cx, cy, x1, y - 3, col)
    dx, dy = x1 - cx, (y - 3) - cy
    L = math.hypot(dx, dy)
    ux, uy = dx / L, dy / L
    px, py = -uy, ux
    tip = (x1, y - 3)
    a = (x1 - 11 * ux + 6 * px, y - 3 - 11 * uy + 6 * py)
    b = (x1 - 11 * ux - 6 * px, y - 3 - 11 * uy - 6 * py)
    s += "<polygon points='%.1f,%.1f %.1f,%.1f %.1f,%.1f' fill='%s'/>" % (tip[0], tip[1], a[0], a[1], b[0], b[1], col)
    return s


def nl_svg(d, wholes, jumps, W=380, label=None):
    """Number line 0..wholes with ticks every 1/d. jumps = [(start, end, color)] in pieces."""
    L, R, Y = 24, W - 24, 62
    total = d * wholes

    def X(i):
        return L + (R - L) * float(i) / total
    s = ["<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='2.5'/>" % (L, Y, R, Y, LINE)]
    for i in range(total + 1):
        whole = (i % d == 0)
        s.append("<line x1='%.1f' y1='%d' x2='%.1f' y2='%d' stroke='%s' stroke-width='%s'/>"
                 % (X(i), Y - (13 if whole else 8), X(i), Y + (13 if whole else 8), LINE, "2.5" if whole else "1.6"))
        if whole:
            s.append("<text x='%.1f' y='%d' font-size='17' font-weight='700' fill='%s' text-anchor='middle'>%d</text>"
                     % (X(i), Y + 36, LINE, i // d))
    for a, b, col in jumps:
        h = min(26, 8 + 2.2 * abs(b - a) * 12.0 / d)
        s.append(arc(X(a), X(b), Y, h, col))
    s.append("<circle cx='%.1f' cy='%d' r='5' fill='%s'/>" % (X(jumps[0][0]), Y, LINE))
    return svg_wrap(W, Y + 44, "".join(s), label or "number line from 0 to %d with jumps" % wholes)


# ------------------------------------------------------------ explanations
def e_add(N1, N2, d, unit=""):
    u = (" " + unit) if unit else ""
    w1, f1 = divmod(N1, d)
    w2, f2 = divmod(N2, d)
    s, W = f1 + f2, w1 + w2
    ans = mixed(N1 + N2, d)
    if w1 == 0 and w2 == 0:
        t = "Same denominator, so add only the numerators: %d + %d = %d. Keep the denominator %d: " % (f1, f2, s, d)
        if s > d:
            return t + "%s. That is more than 1. Take out %s = 1, so %s = <b>%s%s</b>." % (fr(s, d), fr(d, d), fr(s, d), ans, u)
        if s == d:
            return t + "%s = <b>1</b>." % fr(s, d)
        return t + "<b>%s%s</b>." % (ans, u)
    t = "Add the fractions: %s + %s = %s. " % (fr(f1, d), fr(f2, d), fr(s, d))
    if w1 and w2:
        t += "Add the whole numbers: %d + %d = %d. " % (w1, w2, W)
    else:
        t += "The whole number is %d. " % W
    if s > d:
        t += "%s is more than 1: %s = 1 %s. So %d + 1 %s = <b>%s%s</b>." % (fr(s, d), fr(s, d), fr(s - d, d), W, fr(s - d, d), ans, u)
    elif s == d:
        t += "%s = 1, so %d + 1 = <b>%s%s</b>." % (fr(s, d), W, ans, u)
    else:
        t += "Put them together: <b>%s%s</b>." % (ans, u)
    return t


def e_sub(N1, N2, d, unit=""):
    u = (" " + unit) if unit else ""
    w1, f1 = divmod(N1, d)
    w2, f2 = divmod(N2, d)
    ans = mixed(N1 - N2, d)
    if w1 == 0 and w2 == 0:
        return ("Same denominator, so subtract only the numerators: %d − %d = %d. Keep the denominator %d: <b>%s%s</b>."
                % (f1, f2, f1 - f2, d, ans, u))
    if N1 == d and w2 == 0:
        return "Write 1 as %s. Then %s − %s = <b>%s%s</b>." % (fr(d, d), fr(d, d), fr(f2, d), ans, u)
    if f1 >= f2:
        t = "Subtract the fractions: %s − %s = %s. " % (fr(f1, d), fr(f2, d), fr(f1 - f2, d)) if f2 else ""
        t += ("Subtract the whole numbers: %d − %d = %d. " % (w1, w2, w1 - w2)) if w2 else "The whole number stays %d. " % w1
        return t + "The answer is <b>%s%s</b>." % (ans, u)
    if f1 == 0:
        t = "There is no fraction to take %s from, so rename 1 whole: %d = %s. " % (fr(f2, d), w1, mx(w1 - 1, d, d))
    else:
        t = ("%s is less than %s, so rename 1 whole as %s: %s = %s. "
             % (fr(f1, d), fr(f2, d), fr(d, d), mx(w1, f1, d), mx(w1 - 1, d + f1, d)))
    t += "Subtract the fractions: %s − %s = %s. " % (fr(d + f1, d), fr(f2, d), fr(d + f1 - f2, d))
    t += "Subtract the whole numbers: %d − %d = %d. " % (w1 - 1, w2, w1 - 1 - w2)
    return t + "The answer is <b>%s%s</b>." % (ans, u)


def add_cands(N1, N2, d):
    """Wrong sums from real mistakes."""
    w1, f1 = divmod(N1, d)
    w2, f2 = divmod(N2, d)
    W, s = w1 + w2, f1 + f2
    c = [C(W, s, 2 * d)]                                    # added the denominators
    if s > d:
        c += [C(W, s - d, d)]                               # forgot to carry the 1 whole
        c += [C(W + 1, s, d)] if W else [C(1, s, d)]          # carried 1 but kept s/d
        c += [C(W, 0, d)] if W else []                      # added only the whole numbers
    elif s == d:
        c += [C(W, 0, d) if W else None, C(W, s, 2 * d), C(W + 1, s, d)]
    else:
        c += [C(W, 0, d) if W else None, C(W, s + 1, d) if (s + 1 < d or W == 0) else None,
              C(W, s - 1, d) if s > 1 else None, C(W + 1, s, d)]
    c += [CN(N1 + N2 + 1, d), CN(N1 + N2 - 1, d), CN(N1 + N2 + d, d)]
    return c


def sub_cands(N1, N2, d):
    w1, f1 = divmod(N1, d)
    w2, f2 = divmod(N2, d)
    W = w1 - w2
    c = []
    if f1 >= f2:
        c += [C(W, f1 + f2, d) if (f1 + f2 < d or W == 0) else CN(W * d + f1 + f2, d)]      # added the fractions
        c += [CN(N1 + N2, d)]                                                    # added everything
        c += [C(W, f1 - f2 + 1, d) if f1 - f2 + 1 < d else None, C(W, f1 - f2 - 1, d) if f1 - f2 > 1 else None]
        c += [C(W, 0, d) if W else None]
    elif f1 == 0:
        c += [C(W, f2, d)]                     # kept the fraction part: 5 - 2 3/8 = 3 3/8
        c += [C(W, d - f2, d)]                 # did not take 1 from the whole
        c += [C(W - 1, f2, d) if W > 1 else None]
    else:
        c += [C(W, f2 - f1, d)]                # subtracted the smaller numerator from the bigger
        c += [C(W, d + f1 - f2, d)]            # renamed but did not lower the whole
        if d != 10 and 10 + f1 - f2 > 0 and 10 + f1 - f2 != d:
            c += [C(W - 1, 10 + f1 - f2, d)]   # renamed 1 whole as 10, like with whole numbers
        c += [C(W - 1, f2 - f1, d) if W > 1 else None]
        c += [CN(N1 + N2, d)]
    return c


# ============================================================ set 1: decompose
def set_decompose(rnd):
    its = []
    # A: unit fractions
    for a, b in [(3, 5), (5, 8), (4, 6), (3, 10)]:
        e = ("%s means %d pieces that are each %s. Add %s %d times: %s."
             % (fr(a, b), a, fr(1, b), fr(1, b), a, unit_sum(a, b)))
        its.append(mcq(fig(bars_svg(b, 1, [(a, FILL)], label="bar split into %d equal parts with %d shaded" % (b, a))) +
                       "Which sum of unit fractions equals %s?" % fr(a, b),
                       unit_sum(a, b), [unit_sum(a - 1, b), unit_sum(a + 1, b), unit_sum(b, b)], e, rnd))
    # B: a two-color bar shows one way to split
    for x, y, d in [(2, 3, 8), (4, 1, 6), (3, 4, 10), (1, 3, 5)]:
        e = ("The bar has %d equal parts, so each part is %s. %s green (%s) and %d %s yellow (%s). "
             "Together they make %s." % (d, fr(1, d), "1 part is" if x == 1 else "%d parts are" % x, fr(x, d),
                                          y, "is" if y == 1 else "are", fr(y, d), fr(x + y, d)))
        q = (fig(bars_svg(d, 1, [(x, FILL), (y, FILL2)], label="bar with %d equal parts: %d green and %d yellow" % (d, x, y))) +
             "The bar shows %s split into two parts. Which sum does it show?" % fr(x + y, d))
        its.append(mcq(q, (plus(fr(x, d), fr(y, d)), Fraction(x + y, d)),
                       [(plus(fr(x, x + y), fr(y, x + y)), Fraction(1)),               # used the shaded parts as the denominator
                        (plus(fr(x, d), fr(d - x - y, d)), Fraction(d - y, d)),        # counted the white parts, not the yellow
                        (plus(fr(x, d), fr(d - x, d)), Fraction(1)),                   # counted every part that is not green
                        (plus(fr(d - x - y, d), fr(y, d)), Fraction(d - x, d)),
                        (plus(fr(x, d), fr(y + 1, d)), Fraction(x + y + 1, d))], e, rnd, same_value_ok=True))
    # C: which sum equals a/d
    for a, d, (x, y), trap in [(7, 10, (2, 5), (3, 4)), (5, 8, (1, 4), (2, 3)), (7, 12, (4, 3), (2, 5)),
                               (4, 6, (1, 3), (2, 2)), (9, 12, (5, 4), (4, 5)), (3, 8, (1, 2), (1, 2))]:
        h = d // 2
        wrong = [plus(fr(trap[0], h), fr(trap[1], h)), plus(fr(x, d), fr(y + 1, d)), plus(fr(x, d), fr(y - 1, d)) if y > 1 else plus(fr(1, d), fr(1, d), fr(x, d))]
        e = ("The denominators stay %d. Add the numerators: %d + %d = %d, so %s + %s = %s. "
             "In %s + %s the pieces are %s, not %s." % (d, x, y, a, fr(x, d), fr(y, d), fr(a, d),
                                                          fr(trap[0], h), fr(trap[1], h), WORD[h], WORD[d]))
        its.append(mcq("Which sum equals %s?" % fr(a, d), plus(fr(x, d), fr(y, d)), wrong, e, rnd))
    # D: which is NOT a way to write a/d
    for a, d, good, bad in [(5, 6, [(1, 4), (2, 3), (1, 1, 3)], (2, 2)),
                            (7, 8, [(3, 4), (5, 2), (1, 2, 4)], (3, 5)),
                            (6, 10, [(1, 5), (2, 4), (2, 2, 2)], (3, 4))]:
        right = plus(*[fr(k, d) for k in bad])
        e = ("Add the numerators of each sum. %s gives %d + %d = %d, so it equals %s, not %s. "
             "The other three sums all have numerators that add to %d." % (right, bad[0], bad[1], sum(bad), fr(sum(bad), d), fr(a, d), a))
        its.append(mcq("Which is <b>not</b> a way to write %s?" % fr(a, d), right,
                       [plus(*[fr(k, d) for k in g]) for g in good], e, rnd))
    # E: mixed numbers as fractions
    for w, n, d in [(1, 3, 8), (2, 1, 4)]:
        N = w * d + n
        ones = plus(*([fr(d, d)] * w))
        e = ("Each whole is %s, so %s = %s + %s = %s." % (fr(d, d), mx(w, n, d), ones, fr(n, d), fr(N, d)))
        q = "Which sum equals %s?" % mx(w, n, d)
        its.append(mcq(q, plus(ones, fr(n, d)),
                       [plus(fr(w, d), fr(n, d)),      # read the whole number as w/d
                        fr(n, d),                      # dropped the whole number
                        unit_sum(w + n, d)], e, rnd))  # counted w + n pieces
    w, n, d = 2, 3, 5
    N = w * d + n
    e = "Each whole is %s, so 2 wholes are %s. Add the %s: %s + %s = %s." % (fr(5, 5), fr(10, 5), fr(3, 5), fr(10, 5), fr(3, 5), fr(N, 5))
    q = "%s = <span class='fr'><span class='fn'><b>?</b></span><span class='fd'>5</span></span>" % mx(w, n, d)
    its.append(mcq(q, fr(N, d), [fr(w + n, d), fr(23, d), fr(w * d, d)], e, rnd))
    assert len(its) == 20, len(its)
    return {"title": "Break apart fractions", "items": its}


# ============================================================ set 2: add
def set_add(rnd, P):
    its = []
    # F1: bar model, sum less than 1
    for x, y, d in [(2, 3, 8), (1, 2, 4), (3, 4, 10), (1, 3, 6), (5, 4, 12)]:
        q = (fig(bars_svg(d, 1, [(x, FILL), (y, FILL2)], label="bar with %d equal parts: %d green and %d yellow" % (d, x, y))) +
             "What is %s + %s?" % (fr(x, d), fr(y, d)))
        its.append(mcq(q, CN(x + y, d), add_cands(x, y, d), e_add(x, y, d), rnd))
    # F2: no picture, sum less than 1
    used = set()
    for d in [5, 6, 8, 10, 12]:
        while True:
            x, y = rnd.randint(1, d - 2), rnd.randint(1, d - 2)
            if x + y < d and (x, y, d) not in used and x + y > 2:
                break
        used.add((x, y, d))
        its.append(mcq("%s + %s = ?" % (fr(x, d), fr(y, d)), CN(x + y, d), add_cands(x, y, d), e_add(x, y, d), rnd))
    # sum is exactly 1
    its.append(mcq("%s + %s = ?<br>Write the answer as a whole number." % (fr(3, 8), fr(5, 8)), CN(8, 8),
                   [C(0, 8, 16), C(2, 0, 8), C(0, 7, 8)], "Add the numerators: 3 + 5 = 8, so the sum is %s. "
                   "8 eighths make one whole: %s = <b>1</b>." % (fr(8, 8), fr(8, 8)), rnd))
    # F3: number line
    for x, y, d, wh in [(2, 3, 6, 1), (3, 4, 5, 2)]:
        q = (fig(nl_svg(d, wh, [(0, x, FILL), (x, x + y, "#d08a12")])) +
             "The jumps show %s + %s. Where does the second jump end?" % (fr(x, d), fr(y, d)) +
             (" Write the answer as a mixed number." if x + y > d else ""))
        e = ("Each space is %s. The first jump is %d spaces and the second is %d spaces: %d + %d = %d spaces, or %s."
             % (fr(1, d), x, y, x, y, x + y, fr(x + y, d)))
        if x + y > d:
            e += " That is %d spaces past 1, so it is <b>%s</b>." % (x + y - d, mixed(x + y, d))
        its.append(mcq(q, CN(x + y, d), add_cands(x, y, d), e, rnd))
    # F4: sums more than 1
    for i, (x, y, d) in enumerate([(5, 7, 8), (11, 5, 12), (3, 3, 4), (7, 9, 10), (5, 4, 6)]):
        q = "%s + %s = ?<br>Write the answer as a mixed number." % (fr(x, d), fr(y, d))
        if i == 0:
            q = fig(bars_svg(d, 2, [(x, FILL), (y, FILL2)], label="two bars of %d equal parts: %d green and %d yellow" % (d, x, y))) + q
        its.append(mcq(q, CN(x + y, d), add_cands(x, y, d), e_add(x, y, d), rnd))
    # F5: three addends
    q = "%s + %s + %s = ?" % (fr(2, 10), fr(3, 10), fr(4, 10))
    e = "Add all three numerators: 2 + 3 + 4 = 9. Keep the denominator 10: <b>%s</b>." % fr(9, 10)
    its.append(mcq(q, CN(9, 10), [C(0, 9, 30), C(0, 5, 10), C(0, 7, 10)], e, rnd))
    # F6: find the mistake
    n, he, his = P.next()
    q = "%s wrote %s + %s = %s. What mistake did %s make?" % (n, fr(2, 8), fr(3, 8), fr(5, 16), he)
    e = ("Eighths plus eighths are still eighths, so the denominator stays 8. %s added the denominators. "
         "The right answer is %s + %s = %s." % (n, fr(2, 8), fr(3, 8), fr(5, 8)))
    its.append(mcq(q, "%s added the denominators" % cap(he),
                   ["%s added the numerators" % cap(he), "%s should have subtracted" % cap(he), "There is no mistake"], e, rnd))
    assert len(its) == 20, len(its)
    return {"title": "Add fractions", "items": its}


# ============================================================ set 3: subtract
def set_subtract(rnd, P):
    its = []
    # G1: bar model with crossed-out parts
    for a, b, d in [(5, 2, 6), (7, 3, 8), (4, 1, 5), (9, 4, 10), (5, 3, 12)]:
        q = (fig(bars_svg(d, 1, [(a, FILL)], crossed=set(range(a - b, a)),
                          label="bar with %d equal parts: %d shaded and %d of them crossed out" % (d, a, b))) +
             "What is %s − %s?" % (fr(a, d), fr(b, d)))
        e = ("%d parts are shaded and %d %s crossed out. %s left: %d − %d = %d, so the answer is <b>%s</b>."
             % (a, b, "is" if b == 1 else "are", "1 part is" if a - b == 1 else "%d parts are" % (a - b), a, b, a - b, fr(a - b, d)))
        its.append(mcq(q, CN(a - b, d), [C(0, a + b, d), C(0, b, d)] + sub_cands(a, b, d), e, rnd))
    # G2: no picture
    used = set()
    for d in [8, 12, 10, 6, 4, 5, 12]:
        while True:
            a = rnd.randint(2, d - 1)
            b = rnd.randint(1, a - 1)
            if (a, b, d) not in used and a - b != b and a - b >= 2:
                break
        used.add((a, b, d))
        its.append(mcq("%s − %s = ?" % (fr(a, d), fr(b, d)), CN(a - b, d),
                       [C(0, b, d)] + sub_cands(a, b, d), e_sub(a, b, d), rnd))
    # G3: number line, jump back
    q = fig(nl_svg(8, 1, [(7, 2, RED)], label="number line from 0 to 1 with a jump back")) + \
        "The jump shows %s − %s. Where does it end?" % (fr(7, 8), fr(5, 8))
    e = "Start at %s and jump back 5 spaces of %s. You land 2 spaces from 0: <b>%s</b>." % (fr(7, 8), fr(1, 8), fr(2, 8))
    its.append(mcq(q, CN(2, 8), [C(0, 5, 8), C(0, 3, 8), C(1, 4, 8), C(0, 12, 8)], e, rnd))
    # G4: 1 minus a fraction
    for a, d in [(3, 8), (2, 5), (5, 12), (1, 4)]:
        q = "1 − %s = ?" % fr(a, d)
        its.append(mcq(q, CN(d - a, d), [C(0, a, d), C(0, d - a + 1, d), C(0, d - a - 1, d) if d - a > 1 else None, C(1, a, d)],
                       e_sub(d, a, d), rnd))
    # G5: missing part
    for a, b, d in [(7, 3, 10), (5, 1, 6)]:
        q = "%s − <b>?</b> = %s" % (fr(a, d), fr(b, d))
        e = ("Think: what do you take from %s to leave %s? %d − %d = %d, so the missing fraction is <b>%s</b>. "
             "Check: %s − %s = %s." % (fr(a, d), fr(b, d), a, b, a - b, fr(a - b, d), fr(a, d), fr(a - b, d), fr(b, d)))
        its.append(mcq(q, CN(a - b, d), [C(0, a + b, d) if a + b < d else C(0, a + b, d), C(0, b, d), C(0, a - b + 1, d), C(0, a - b, 2 * d)], e, rnd))
    # G6: find the mistake
    n, he, his = P.next()
    q = "%s says %s − %s = %s because 7 − 3 = 4 and 8 − 8 = 0. What is wrong?" % (
        n, fr(7, 8), fr(3, 8), "<span class='fr'><span class='fn'>4</span><span class='fd'>0</span></span>")
    e = ("The pieces are eighths before and after you take some away. Subtract only the numerators: "
         "%s − %s = %s." % (fr(7, 8), fr(3, 8), fr(4, 8)))
    its.append(mcq(q, "The pieces are still eighths",
                   ["%s should add 7 and 3" % cap(he), "%s should subtract 7 from 8" % cap(he), "Nothing is wrong"], e, rnd))
    assert len(its) == 20, len(its)
    return {"title": "Subtract fractions", "items": its}


# ============================================================ set 4: mixed numbers
def set_mixed(rnd):
    its = []
    # H1: add, no renaming
    for (w1, f1), (w2, f2), d in [((2, 1), (1, 3), 5), ((3, 2), (4, 1), 6), ((1, 3), (2, 4), 10), ((5, 1), (2, 1), 4)]:
        N1, N2 = w1 * d + f1, w2 * d + f2
        its.append(mcq("%s + %s = ?" % (mx(w1, f1, d), mx(w2, f2, d)), CN(N1 + N2, d), add_cands(N1, N2, d), e_add(N1, N2, d), rnd))
    # H2: subtract, no renaming
    for (w1, f1), (w2, f2), d in [((4, 5), (1, 2), 6), ((6, 7), (3, 4), 8), ((3, 3), (2, 1), 4)]:
        N1, N2 = w1 * d + f1, w2 * d + f2
        its.append(mcq("%s − %s = ?" % (mx(w1, f1, d), mx(w2, f2, d)), CN(N1 - N2, d), sub_cands(N1, N2, d), e_sub(N1, N2, d), rnd))
    # H3: renaming
    for w, n, d in [(2, 9, 8), (3, 7, 5)]:
        q = "Rename %s so the fraction part is less than 1." % mx(w, n, d)
        e = ("%s is more than 1: %s = 1 %s. Add that 1 to the %d: %s = <b>%s</b>."
             % (fr(n, d), fr(n, d), fr(n - d, d), w, mx(w, n, d), mx(w + 1, n - d, d)))
        its.append(mcq(q, C(w + 1, n - d, d), [C(w, n - d, d), C(w + 1, n, d), C(0, w + n, d), C(w, n, 2 * d)], e, rnd))
    for w, n, d in [(3, 1, 4), (5, 2, 6)]:
        q = ("Rename 1 whole to get more %s.<br>%s = %d <span class='fr'><span class='fn'><b>?</b></span>"
             "<span class='fd'>%d</span></span>" % (WORD[d], mx(w, n, d), w - 1, d))
        e = ("Take 1 whole from %d and write it as %s. Add it to %s: %s + %s = %s. So %s = %s, and the missing number is <b>%d</b>."
             % (w, fr(d, d), fr(n, d), fr(d, d), fr(n, d), fr(d + n, d), mx(w, n, d), mx(w - 1, d + n, d), d + n))
        its.append(mcq(q, str(d + n), [str(n), str(10 + n), str(d), str(w * d + n)], e, rnd))
    # H4: add with renaming
    for (w1, f1), (w2, f2), d in [((2, 5), (1, 7), 8), ((1, 2), (3, 2), 3), ((4, 3), (2, 3), 4), ((2, 7), (2, 8), 12)]:
        N1, N2 = w1 * d + f1, w2 * d + f2
        q = "%s + %s = ?<br>Write the answer as a mixed number." % (mx(w1, f1, d), mx(w2, f2, d))
        its.append(mcq(q, CN(N1 + N2, d), add_cands(N1, N2, d), e_add(N1, N2, d), rnd))
    # H5: subtract with renaming
    for (w1, f1), (w2, f2), d in [((3, 1), (1, 3), 4), ((5, 2), (2, 4), 5), ((4, 1), (1, 5), 6), ((6, 3), (3, 7), 10), ((5, 0), (2, 3), 8)]:
        N1, N2 = w1 * d + f1, w2 * d + f2
        its.append(mcq("%s − %s = ?" % (mx(w1, f1, d), mx(w2, f2, d)), CN(N1 - N2, d), sub_cands(N1, N2, d), e_sub(N1, N2, d), rnd))
    assert len(its) == 20, len(its)
    return {"title": "Add and subtract mixed numbers", "items": its}


# ============================================================ set 5: word problems
def w_hike(r, P, N1, N2, d):
    n, he, his = P.next()
    q = ("%s hiked %s in the morning and %s in the afternoon. How many miles did %s hike in all?"
         % (n, amt(N1, d, "mile", "miles"), amt(N2, d, "mile", "miles"), he))
    return q, CN(N1 + N2, d), add_cands(N1, N2, d), e_add(N1, N2, d, "miles" if N1 + N2 > d else "mile")


def w_ribbon(r, P, N1, N2, d):
    n, he, his = P.next()
    q = ("%s had a ribbon that was %s long. %s cut off %s to wrap a gift. How many feet of ribbon are left?"
         % (n, amt(N1, d, "foot", "feet"), cap(he), amt(N2, d, "foot", "feet")))
    return q, CN(N1 - N2, d), sub_cands(N1, N2, d), e_sub(N1, N2, d, "feet" if N1 - N2 > d else "foot")


def w_pizza(r, P, a, b, d):
    n, he, his = P.next()
    sib = r.choice(["sister", "brother", "dad", "mom"])
    q = ("A pizza is cut into %d equal slices. %s ate %s of the pizza, and %s %s ate %s of it. "
         "What fraction of the pizza is left?" % (d, n, fr(a, d), his, sib, fr(b, d)))
    e = ("First find how much was eaten: %s + %s = %s. The whole pizza is %s. Left: %s − %s = <b>%s</b>."
         % (fr(a, d), fr(b, d), fr(a + b, d), fr(d, d), fr(d, d), fr(a + b, d), fr(d - a - b, d)))
    return q, CN(d - a - b, d), [C(0, a + b, d), C(0, d - a, d), C(0, a + b, 2 * d), C(0, d - b, d)], e


def w_recipe(r, P, N1, N2, d, food, x1, x2):
    q = ("A recipe for %s uses %s of %s and %s of %s. How many cups is that in all?"
         % (food, amt(N1, d, "cup", "cups"), x1, amt(N2, d, "cup", "cups"), x2))
    return q, CN(N1 + N2, d), add_cands(N1, N2, d), e_add(N1, N2, d, "cups" if N1 + N2 > d else "cup")


def w_more(r, P, a, b, d, what):
    n1, he1, his1 = P.next()
    n2, he2, his2 = P.next()
    if what == "bottle":
        q = ("%s drank %s of a bottle of water. %s drank %s of a bottle the same size. "
             "How much more of a bottle did %s drink than %s?" % (n1, fr(a, d), n2, fr(b, d), n1, n2))
    else:
        q = ("%s and %s are painting a fence. %s painted %s of the fence, and %s painted %s of it. "
             "How much more of the fence did %s paint than %s?" % (n1, n2, n1, fr(a, d), n2, fr(b, d), n1, n2))
    e = "“How much more” means subtract: %s − %s. " % (fr(a, d), fr(b, d)) + e_sub(a, b, d)
    return q, CN(a - b, d), [CN(a + b, d), C(0, a - b + 1, d), C(0, a - b - 1, d) if a - b > 1 else None, C(0, b, d)], e


def w_rain(r, P, N1, N2, d, days):
    q = ("It rained %s on %s and %s on %s. How many inches of rain fell on the two days in all?"
         % (amt(N1, d, "inch", "inches"), days[0], amt(N2, d, "inch", "inches"), days[1]))
    return q, CN(N1 + N2, d), add_cands(N1, N2, d), e_add(N1, N2, d, "inches" if N1 + N2 > d else "inch")


def w_board(r, P, N1, N2, d, thing, one, many):
    n, he, his = P.next()
    q = ("A %s is %s long. %s cuts off a piece that is %s long. How long is the part that is left?"
         % (thing, amt(N1, d, one, many), n, amt(N2, d, one, many)))
    return q, CN(N1 - N2, d), sub_cands(N1, N2, d), e_sub(N1, N2, d, many if N1 - N2 > d else one)


def w_time(r, P, N1, N2, d, act):
    n, he, his = P.next()
    q = ("%s %s for %s on Saturday and %s on Sunday. How many hours did %s spend in all?"
         % (n, act, amt(N1, d, "hour", "hours"), amt(N2, d, "hour", "hours"), he))
    return q, CN(N1 + N2, d), add_cands(N1, N2, d), e_add(N1, N2, d, "hours" if N1 + N2 > d else "hour")


def w_farther(r, P, N1, N2, d, verb):
    n1, he1, his1 = P.next()
    n2, he2, his2 = P.next()
    q = ("%s %s %s. %s %s %s. How much farther did %s %s than %s?"
         % (n1, verb[1], amt(N1, d, "mile", "miles"), n2, verb[1], amt(N2, d, "mile", "miles"), n1, verb[0], n2))
    e = "“How much farther” means subtract. " + e_sub(N1, N2, d, "miles" if N1 - N2 > d else "mile")
    return q, CN(N1 - N2, d), sub_cands(N1, N2, d) + [CN(N1 + N2, d)], e


def w_need(r, P, N1, N2, d, what, dish):
    n, he, his = P.next()
    q = ("%s needs %s of %s to make %s. %s has %s. How much more %s does %s need?"
         % (n, amt(N1, d, "cup", "cups"), what, dish, cap(he), amt(N2, d, "cup", "cups"), what, he))
    e = "Subtract what %s has from what %s needs. " % (he, he) + e_sub(N1, N2, d, "cups" if N1 - N2 > d else "cup")
    return q, CN(N1 - N2, d), sub_cands(N1, N2, d) + [CN(N1 + N2, d)], e


def set_words(rnd, P):
    probs = [
        w_hike(rnd, P, 2 * 4 + 3, 1 * 4 + 2, 4),
        w_pizza(rnd, P, 3, 2, 8),
        w_recipe(rnd, P, 2, 2, 3, "granola bars", "oats", "raisins"),
        w_more(rnd, P, 7, 4, 8, "bottle"),
        w_ribbon(rnd, P, 4 * 4 + 1, 1 * 4 + 3, 4),
        w_rain(rnd, P, 1 * 10 + 3, 9, 10, ("Monday", "Tuesday")),
        w_time(rnd, P, 1 * 4 + 3, 3, 4, "practiced the piano"),
        w_board(rnd, P, 6 * 4, 2 * 4 + 3, 4, "board", "foot", "feet"),
        w_farther(rnd, P, 3 * 4 + 3, 2 * 4 + 1, 4, ("run", "ran")),
        w_need(rnd, P, 2 * 3 + 1, 1 * 3 + 2, 3, "milk", "pancakes"),
        w_hike(rnd, P, 1 * 10 + 4, 2 * 10 + 5, 10),
        w_pizza(rnd, P, 2, 3, 6),
        w_recipe(rnd, P, 1 * 4 + 1, 3, 4, "muffins", "flour", "milk"),
        w_more(rnd, P, 9, 5, 12, "fence"),
        w_ribbon(rnd, P, 3 * 8 + 5, 1 * 8 + 2, 8),
        w_rain(rnd, P, 2 * 10 + 6, 1 * 10 + 8, 10, ("Friday", "Saturday")),
        w_time(rnd, P, 1 * 3 + 2, 2, 3, "read"),
        w_board(rnd, P, 5 * 8, 1 * 8 + 5, 8, "rope", "yard", "yards"),
        w_farther(rnd, P, 4 * 10 + 2, 1 * 10 + 6, 10, ("bike", "biked")),
        w_need(rnd, P, 3 * 4 + 1, 1 * 4 + 3, 4, "flour", "bread"),
    ]
    its = [mcq(q, a, c, e, rnd) for q, a, c, e in probs]
    return {"title": "Fraction word problems", "items": its}


# ============================================================ lesson
def body_html():
    dec_fig = bars_svg(8, 1, [(2, FILL), (3, FILL2)], cell=40, label="bar of 8 equal parts with 2 green and 3 yellow")
    add_fig = bars_svg(8, 2, [(5, FILL), (7, FILL2)], cell=36, label="two bars of 8 equal parts: 5 green and 7 yellow")
    reg_fig = bars_svg(4, 4, [(13, FILL)], crossed={0, 1, 2, 3, 10, 11, 12}, cell=22, gap=14, side=True,
                       label="3 and 1 fourth wholes shaded, with 1 and 3 fourths crossed out")
    return (
        "<h2>Add and subtract the same size pieces</h2>"
        "<p>When fractions have the <b>same denominator</b>, the pieces are the same size. "
        "Add or subtract the <b>numerators</b> (how many pieces). Keep the <b>denominator</b> (the size of the pieces).</p>"
        "<p>A fraction like " + fr(5, 8) + " is 5 pieces of " + fr(1, 8) + ": " + unit_sum(5, 8) +
        ". You can break it apart in more than one way.</p>"
        "<figure class='sn-fig'>" + dec_fig +
        "<figcaption>" + fr(5, 8) + " = " + fr(2, 8) + " + " + fr(3, 8) + ". It is also " + fr(1, 8) + " + " + fr(4, 8) +
        " or " + fr(1, 8) + " + " + fr(1, 8) + " + " + fr(3, 8) + ".</figcaption></figure>"
        + ex("Example", fr(5, 8) + " + " + fr(7, 8) + " = ?",
             "Add the numerators: 5 + 7 = 12. Keep eighths: " + fr(12, 8) + ". That is more than 1, because " + fr(8, 8) +
             " = 1. So " + fr(12, 8) + " = 1 " + fr(4, 8) + ".", fr(12, 8) + " = 1 " + fr(4, 8)) +
        "<figure class='sn-fig'>" + add_fig +
        "<figcaption>5 green eighths and 7 yellow eighths fill one whole bar and 4 parts of the next: 1 " + fr(4, 8) + ".</figcaption></figure>"
        + ex("Example", fr(7, 10) + " − " + fr(3, 10) + " = ?", "Subtract the numerators: 7 − 3 = 4. The pieces are still tenths.", fr(4, 10)) +
        "<h2>Mixed numbers</h2>"
        "<p>Add or subtract the fractions, then the whole numbers.</p>" +
        table(["Problem", "Fractions", "Whole numbers", "Answer"], [
            ["2 " + fr(1, 5) + " + 1 " + fr(3, 5), fr(1, 5) + " + " + fr(3, 5) + " = " + fr(4, 5), "2 + 1 = 3", "3 " + fr(4, 5)],
            ["2 " + fr(5, 8) + " + 1 " + fr(7, 8), fr(5, 8) + " + " + fr(7, 8) + " = " + fr(12, 8) + " = 1 " + fr(4, 8), "2 + 1 + 1 = 4", "4 " + fr(4, 8)],
            ["4 " + fr(5, 6) + " − 1 " + fr(2, 6), fr(5, 6) + " − " + fr(2, 6) + " = " + fr(3, 6), "4 − 1 = 3", "3 " + fr(3, 6)],
        ]) +
        "<p>If the first fraction is too small to subtract from, <b>rename 1 whole</b> as " + fr(4, 4) + ", " + fr(8, 8) + " and so on.</p>"
        "<figure class='sn-fig'>" + reg_fig +
        "<figcaption>3 " + fr(1, 4) + " − 1 " + fr(3, 4) + ": you cannot take " + fr(3, 4) + " from " + fr(1, 4) +
        ", so break 1 whole into fourths. 3 " + fr(1, 4) + " = 2 " + fr(5, 4) + ". Cross out 1 whole and 3 fourths. "
        "1 whole and 2 fourths are left.</figcaption></figure>"
        + ex("Example", "3 " + fr(1, 4) + " − 1 " + fr(3, 4) + " = ?",
             "Rename: 3 " + fr(1, 4) + " = 2 " + fr(5, 4) + ". Fractions: " + fr(5, 4) + " − " + fr(3, 4) + " = " + fr(2, 4) +
             ". Whole numbers: 2 − 1 = 1.", "1 " + fr(2, 4)) +
        "<p>On this page, answers keep the same denominator as the problem. " + fr(2, 4) + " is right, and so is " + fr(1, 2) + ".</p>"
        "<h2>Common mistakes</h2>" +
        table(["Mistake", "What to do instead"], [
            [fr(2, 8) + " + " + fr(3, 8) + " = " + fr(5, 16) + " (adding the denominators)", "The pieces stay eighths: " + fr(5, 8)],
            [fr(5, 8) + " + " + fr(7, 8) + " = " + fr(12, 8) + ", and stopping there", "When asked for a mixed number, take out the whole: 1 " + fr(4, 8)],
            ["2 " + fr(5, 8) + " + 1 " + fr(7, 8) + " = 3 " + fr(4, 8), "Add the 1 whole from " + fr(12, 8) + ": 4 " + fr(4, 8)],
            ["3 " + fr(1, 4) + " − 1 " + fr(3, 4) + " = 2 " + fr(2, 4) + " (taking " + fr(1, 4) + " from " + fr(3, 4) + " instead)", "Rename 1 whole: 2 " + fr(5, 4) + " − 1 " + fr(3, 4) + " = 1 " + fr(2, 4)],
            ["5 − 2 " + fr(3, 8) + " = 3 " + fr(3, 8), "Rename 5 as 4 " + fr(8, 8) + ": the answer is 2 " + fr(5, 8)],
        ])
    )


FAQ = [
    {"q": "How do you add fractions with the same denominator?",
     "a": "Add the numerators and keep the denominator. For example, 2/8 + 3/8 = 5/8, because 2 eighths and 3 eighths make 5 eighths."},
    {"q": "Why don't you add the denominators?",
     "a": "The denominator tells the size of the pieces, and the size does not change when you put pieces together. Eighths plus eighths are still eighths, so 2/8 + 3/8 is 5/8, not 5/16."},
    {"q": "How do you subtract mixed numbers when the first fraction is smaller?",
     "a": "Rename 1 whole as a fraction first. For 3 1/4 − 1 3/4, write 3 1/4 as 2 5/4, then subtract: 5/4 − 3/4 = 2/4 and 2 − 1 = 1, so the answer is 1 2/4."},
    {"q": "Do 4th graders have to simplify fractions?",
     "a": "No. The Grade 4 standard asks students to add and subtract fractions with like denominators, so 4/8 is a correct answer. Writing it as 1/2 is also correct but not required."},
]


def gen_unit():
    rnd = random.Random(105)
    P = People(rnd)
    sets = [set_decompose(rnd), set_add(rnd, P), set_subtract(rnd, P), set_mixed(rnd), set_words(rnd, P)]
    seen = set()
    for s in sets:
        assert len(s["items"]) == 20, (s["title"], len(s["items"]))
        for it in s["items"]:
            assert len(set(it["c"])) == 4, it
            assert it["q"] not in seen, it["q"]
            seen.add(it["q"])
    return {
        "country": "us", "subject": "math", "grade": "grade-4", "slug": "add-subtract-fractions", "sort": 5,
        "updated": UPDATED, "pdf_url": "",
        "title": "Add and Subtract Fractions and Mixed Numbers",
        "seo_title": "Grade 4 Adding and Subtracting Fractions Worksheets: Like Denominators, Mixed Numbers and Word Problems",
        "short_title": "Add and Subtract Fractions",
        "domain": "Number and Operations—Fractions",
        "standard_code": "4.NF.B.3",
        "standard_url": "https://www.thecorestandards.org/Math/Content/4/NF/B/3/",
        "standard_text": "Understand a fraction a/b with a > 1 as a sum of fractions 1/b. Understand addition and subtraction of fractions as joining and separating parts referring to the same whole. Decompose a fraction into a sum of fractions with the same denominator in more than one way. Add and subtract mixed numbers with like denominators. Solve word problems involving addition and subtraction of fractions referring to the same whole and having like denominators.",
        "meta_desc": "Free Grade 4 worksheets on adding and subtracting fractions with like denominators: break apart fractions, add and subtract with models, mixed numbers with renaming, and word problems. 100 practice questions with step-by-step answers.",
        "key_big": "Same denominator: add or subtract the numerators. The denominator stays the same.",
        "key_sub": "The denominator is the size of the pieces, and it does not change: 2/8 + 3/8 = 5/8, not 5/16. With mixed numbers, rename 1 whole when you need more pieces: 3 1/4 = 2 5/4.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }


if __name__ == "__main__":
    u = gen_unit()
    mark_large(u, "(number line|two bars)")
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(u, f, ensure_ascii=False, indent=1)
    print("wrote", path)
