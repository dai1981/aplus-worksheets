# -*- coding: utf-8 -*-
"""
Australia Year 5 Maths: Adding and Subtracting Fractions (Australian Curriculum v9.0, AC9M5N05)
  python3 tools/gen_uk_maths_y5_add_sub_fractions.py
Same denominators, and denominators where one is a multiple of the other (1/4 + 3/8, 5/6 − 1/3).
No unrelated denominators (those are Year 6). Answers greater than 1 are written as mixed numerals.
Every answer is shown in simplest form; the question says so when simplifying is needed.
Wrong choices come from real mistakes; a wrong choice is never equal in value to the right
answer or to another choice. Every answer is checked in code with fractions.Fraction.
HTML attributes use single quotes (no backslashes in the JSON). Australian English.
"""
import json, math, os, random, re
from fractions import Fraction

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "au", "maths", "year-5")
UPDATED = "2026-11-02"
FILL = "#4fae74"      # first fraction
FILL2 = "#f2b84b"     # second fraction
RED = "#c0392b"
LINE = "#2b2b2b"
GIRLS = ["Charlotte", "Isla", "Mia", "Amelia", "Ava", "Harper", "Chloe", "Ruby", "Mei", "Zara", "Matilda", "Sienna", "Grace"]
BOYS = ["Oliver", "Jack", "Noah", "William", "Leo", "Lachlan", "Liam", "Aarav", "Kai", "Cooper", "Ethan"]
WORD = {2: "halves", 3: "thirds", 4: "quarters", 5: "fifths", 6: "sixths", 7: "sevenths", 8: "eighths", 9: "ninths",
        10: "tenths", 11: "elevenths", 12: "twelfths"}


# ------------------------------------------------------------ numbers
def fr(a, b):
    return "<span class='fr'><span class='fn'>%s</span><span class='fd'>%s</span></span>" % (a, b)


def frq(b):
    return fr("<b>?</b>", b)


def mx(w, n, d):
    """Whole part w and fraction n/d written as given."""
    if n == 0:
        return str(w)
    if w == 0:
        return fr(n, d)
    return "%d %s" % (w, fr(n, d))


def show(v):
    """A positive Fraction in simplest form: '7/12', '1 1/6', '2'."""
    w, r = divmod(v.numerator, v.denominator)
    return mx(w, r, v.denominator)


def val(x):
    w, n, d = x
    return Fraction(w) + Fraction(n, d)


def lcm(a, b):
    return a * b // math.gcd(a, b)


# units: (less than 1, exactly 1, more than 1)
M = (" m", " m", " m")
KM = (" km", " km", " km")
KG = (" kg", " kg", " kg")
LITRE = (" L", " L", " L")
HOUR = (" of an hour", " hour", " hours")


def unit_for(v, units):
    if not units:
        return ""
    return units[0] if v < 1 else (units[1] if v == 1 else units[2])


def withu(v, units):
    return show(v) + unit_for(v, units)


def cap(s):
    return s[0].upper() + s[1:]


def prompt_for(x, y, op):
    """Say 'mixed numeral' when two proper fractions make more than 1, and 'simplest form' when needed."""
    (w1, n1, d1), (w2, n2, d2) = x, y
    L = lcm(d1, d2)
    r = val(x) + val(y) if op == "+" else val(x) - val(y)
    rem = (r * L).numerator % L
    simp = rem and math.gcd(rem, L) > 1
    mixed = r > 1 and not (w1 or w2) and rem
    if mixed and simp:
        return "<br>Give your answer as a mixed numeral in its simplest form."
    if mixed:
        return "<br>Give your answer as a mixed numeral."
    if simp:
        return "<br>Give your answer in its simplest form."
    return ""


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


def mcq(q, correct, cands, e, rnd, units=None):
    """correct is a Fraction (shown in simplest form, with units) or a string.
    cands are Fractions or strings. A Fraction equal to the answer, another choice, zero or less is skipped."""
    if isinstance(correct, Fraction):
        cv, cs = correct, withu(correct, units)
    else:
        cv, cs = None, correct
    seen, vals, pick = {cs}, set(), []
    for c in cands:
        if c is None:
            continue
        if isinstance(c, Fraction):
            if c <= 0 or c == cv or c in vals:
                continue
            vals.add(c)
            c = withu(c, units)
        if c in seen:
            continue
        seen.add(c)
        pick.append(c)
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


class People:
    def __init__(self, rnd):
        self.pool = [(n, "she", "her") for n in GIRLS] + [(n, "he", "his") for n in BOYS]
        rnd.shuffle(self.pool)
        self.i = 0

    def next(self):
        p = self.pool[self.i % len(self.pool)]
        self.i += 1
        return p


def table(head, rows):
    h = "".join("<th>%s</th>" % x for x in head)
    b = "".join("<tr>" + "".join("<td>%s</td>" % c for c in r) + "</tr>" for r in rows)
    return "<div class='sn-tw'><table class='sn-table'><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>" % (h, b)


def ex(title, q, s, a):
    return ("<div class='sn-ex'><span class='sn-ex-t'>%s</span><p class='sn-ex-q'>%s</p>"
            "<p class='sn-ex-s'>%s</p><p class='sn-ex-a'>Answer: %s</p></div>" % (title, q, s, a))


def mark_large(u, pattern):
    """Tag pictures that must print larger so their parts stay readable."""
    rx = re.compile(r"<svg (?=[^>]*aria-label='" + pattern + ")")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u


# ------------------------------------------------------------ pictures
def sfr(x, y, a, b, size=15, color=LINE):
    """Stacked fraction drawn in SVG, centred at x. y is the numerator baseline."""
    w = size * 0.62 * max(len(str(a)), len(str(b))) + 4
    return ("<text x='%.1f' y='%.1f' font-size='%d' font-weight='700' fill='%s' text-anchor='middle'>%s</text>"
            "<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='1.6'/>"
            "<text x='%.1f' y='%.1f' font-size='%d' font-weight='700' fill='%s' text-anchor='middle'>%s</text>"
            % (x, y, size, color, a, x - w / 2, y + 5, x + w / 2, y + 5, color, x, y + size + 5, size, color, b))


def bar_cells(x0, y0, W, H, d, k, col):
    return "".join("<rect x='%.2f' y='%.1f' width='%.2f' height='%d' fill='%s' stroke='%s' stroke-width='2.2'/>"
                   % (x0 + i * W / d, y0, W / d, H, col if i < k else "#fff", LINE) for i in range(d))


def dashes(x0, y0, W, H, d, L):
    """Dashed lines that cut a bar of d parts into L parts (only where there is no solid line yet)."""
    s = []
    for i in range(1, L):
        if (i * d) % L == 0:
            continue
        x = x0 + W * i / L
        s.append("<line x1='%.2f' y1='%.1f' x2='%.2f' y2='%.1f' stroke='%s' stroke-width='1.6' stroke-dasharray='5 4'/>"
                 % (x, y0 + 2, x, y0 + H - 2, LINE))
    return "".join(s)


def two_bars_svg(d1, k1, d2, k2, L, W=264, H=40, labels=False):
    """Top bar: k1 of d1 parts (green). Bottom bar: k2 of d2 parts (yellow). Dashed lines cut both into L parts."""
    x0 = 58 if labels else 6
    s = [bar_cells(x0, 6, W, H, d1, k1, FILL), dashes(x0, 6, W, H, d1, L),
         bar_cells(x0, 6 + H + 14, W, H, d2, k2, FILL2), dashes(x0, 6 + H + 14, W, H, d2, L)]
    s.append("<rect x='%d' y='6' width='%d' height='%d' fill='none' stroke='%s' stroke-width='3'/>" % (x0, W, H, LINE))
    s.append("<rect x='%d' y='%d' width='%d' height='%d' fill='none' stroke='%s' stroke-width='3'/>" % (x0, 6 + H + 14, W, H, LINE))
    if labels:
        g1, g2 = math.gcd(k1, d1), math.gcd(k2, d2)
        s.append(sfr(26, 22, k1 // g1, d1 // g1, 15))
        s.append(sfr(26, 22 + H + 14, k2 // g2, d2 // g2, 15))
    return svg_wrap(x0 + W + 6, 2 * H + 26, "".join(s),
                    "two bars of the same size: %d of %d parts green and %d of %d parts yellow, dashed lines cut both into %d parts"
                    % (k1, d1, k2, d2, L))


def one_bar_svg(L, k1, k2, crossed=0, W=264, H=40):
    """One bar of L parts: k1 green then k2 yellow. crossed = how many of the last green parts get a red X."""
    s = []
    for i in range(L):
        col = FILL if i < k1 else (FILL2 if i < k1 + k2 else "#fff")
        x = 6 + i * W / L
        s.append("<rect x='%.2f' y='6' width='%.2f' height='%d' fill='%s' stroke='%s' stroke-width='2.2'/>" % (x, W / L, H, col, LINE))
        if k1 - crossed <= i < k1:
            c = W / L
            r = min(c, H) / 2 - min(c, H) * 0.2
            cx, cy = x + c / 2, 6 + H / 2
            s.append("<path d='M%.1f %.1f L%.1f %.1f M%.1f %.1f L%.1f %.1f' stroke='%s' stroke-width='3' stroke-linecap='round'/>"
                     % (cx - r, cy - r, cx + r, cy + r, cx - r, cy + r, cx + r, cy - r, RED))
    s.append("<rect x='6' y='6' width='%d' height='%d' fill='none' stroke='%s' stroke-width='3'/>" % (W, H, LINE))
    if crossed:
        lab = "bar of %d equal parts: %d shaded and the last %d of them crossed out" % (L, k1, crossed)
    else:
        lab = "bar of %d equal parts: %d green and %d yellow" % (L, k1, k2)
    return svg_wrap(W + 12, H + 12, "".join(s), lab)


def wholes_svg(d, k1, k2, W=264, H=40):
    """Two bars (two wholes) of d parts each. The first k1 parts are green, the next k2 yellow, filling bar 1 then bar 2."""
    s = []
    for b in range(2):
        y0 = 6 + b * (H + 14)
        for i in range(d):
            j = b * d + i
            col = FILL if j < k1 else (FILL2 if j < k1 + k2 else "#fff")
            s.append("<rect x='%.2f' y='%d' width='%.2f' height='%d' fill='%s' stroke='%s' stroke-width='2.2'/>"
                     % (6 + i * W / d, y0, W / d, H, col, LINE))
        s.append("<rect x='6' y='%d' width='%d' height='%d' fill='none' stroke='%s' stroke-width='3'/>" % (y0, W, H, LINE))
    return svg_wrap(W + 12, 2 * H + 26, "".join(s),
                    "two bars of %d equal parts each: %d parts green then %d parts yellow" % (d, k1, k2))


# ------------------------------------------------------------ explanation and mistakes
def finish(W, N, L, units=None):
    """W wholes and N/L (N may be L or more). Convert, simplify, state the answer."""
    t = ""
    if N >= L:
        w2, r = divmod(N, L)
        if r:
            t += "%s is an improper fraction: %s = %s. " % (fr(N, L), fr(N, L), mx(w2, r, L))
        else:
            t += "%s = %d. " % (fr(N, L), w2)
        if W:
            t += "%d + %s = %s. " % (W, mx(w2, r, L), mx(W + w2, r, L))
        W, N = W + w2, r
    g = math.gcd(N, L) if N else 1
    if N and g > 1:
        t += "Simplify: divide the numerator and denominator of %s by %d to get %s. " % (fr(N, L), g, fr(N // g, L // g))
    v = W + Fraction(N, L)
    return t + "The answer is <b>%s</b>." % withu(v, units), v


def e_calc(x, y, op, units=None):
    """Step explanation for x op y. x, y = (whole, numerator, denominator). A whole number x is (w, 0, d)."""
    (w1, n1, d1), (w2, n2, d2) = x, y
    if n1 == 0:                                   # whole number minus a fraction
        assert op == "-" and w2 == 0
        d = d2
        if w1 == 1:
            t = "Write 1 whole as %s. " % fr(d, d)
        else:
            t = "Rename 1 whole as %s: %d = %s. " % (fr(d, d), w1, mx(w1 - 1, d, d))
        t += "Subtract the fractions: %s − %s = %s. " % (fr(d, d), fr(n2, d), fr(d - n2, d))
        if w1 > 1:
            t += "The whole number left is %d. " % (w1 - 1)
        s, v = finish(w1 - 1, d - n2, d, units)
        assert v == val(x) - val(y)
        return t + s
    L = lcm(d1, d2)
    a, b = n1 * L // d1, n2 * L // d2
    if d1 == d2:
        t = "The denominators are the same. "
    else:
        t = "%d is a multiple of %d, so use %d as the denominator. " % (L, min(d1, d2), L)
        rw = ["%s = %s" % (fr(n, d), fr(n * L // d, L)) for w, n, d in (x, y) if d != L]
        t += "Write the equivalent fraction: " + " and ".join(rw) + ". "
    mixed = w1 or w2
    if op == "+":
        if not mixed:
            if d1 == d2:
                t += "Add the numerators: %d + %d = %d. The denominator stays %d. " % (a, b, a + b, L)
            else:
                t += "Add the numerators: %s + %s = %s. " % (fr(a, L), fr(b, L), fr(a + b, L))
            s, v = finish(0, a + b, L, units)
        else:
            t += "Add the fractions: %s + %s = %s. " % (fr(a, L), fr(b, L), fr(a + b, L))
            t += ("Add the whole numbers: %d + %d = %d. " % (w1, w2, w1 + w2)) if (w1 and w2) else "The whole number is %d. " % (w1 + w2)
            s, v = finish(w1 + w2, a + b, L, units)
        assert v == val(x) + val(y)
    else:
        if not mixed:
            if d1 == d2:
                t += "Subtract the numerators: %d − %d = %d. The denominator stays %d. " % (a, b, a - b, L)
            else:
                t += "Subtract the numerators: %s − %s = %s. " % (fr(a, L), fr(b, L), fr(a - b, L))
            s, v = finish(0, a - b, L, units)
        elif a >= b:
            t += "Subtract the fractions: %s − %s = %s. " % (fr(a, L), fr(b, L), fr(a - b, L))
            t += ("Subtract the whole numbers: %d − %d = %d. " % (w1, w2, w1 - w2)) if w2 else "The whole number stays %d. " % w1
            s, v = finish(w1 - w2, a - b, L, units)
        else:
            t += ("%s is less than %s, so rename 1 whole as %s: %s = %s. Subtract the fractions: %s − %s = %s. "
                  % (fr(a, L), fr(b, L), fr(L, L), mx(w1, a, L), mx(w1 - 1, a + L, L), fr(a + L, L), fr(b, L), fr(a + L - b, L)))
            if w2:
                t += "Subtract the whole numbers: %d − %d = %d. " % (w1 - 1, w2, w1 - 1 - w2)
            elif w1 > 1:
                t += "The whole number left is %d. " % (w1 - 1)
            s, v = finish(w1 - 1 - w2, a + L - b, L, units)
        assert v == val(x) - val(y)
    return t + s


def wrong(x, y, op):
    """Wrong answers from real mistakes, most common first."""
    (w1, n1, d1), (w2, n2, d2) = x, y
    right = val(x) + val(y) if op == "+" else val(x) - val(y)
    if n1 == 0:                                                   # whole number minus a fraction: 3 − 3/8
        d = d2
        return [w1 + Fraction(n2, d),                             # wrote 3 3/8
                right + 1,                                        # renamed but did not take 1 from the wholes
                w1 - 1 + Fraction(n2, d),                         # took 1 whole but kept 3/8
                Fraction(d - n2, d),                              # forgot the whole numbers
                Fraction(w1 * d - n2, d * d) if w1 * d > n2 else None,
                right + Fraction(1, d), right - Fraction(1, d)]
    L = lcm(d1, d2)
    a, b = n1 * L // d1, n2 * L // d2
    mixed = w1 or w2
    c = []
    if op == "+":
        W = w1 + w2
        c.append(W + Fraction(n1 + n2, d1 + d2))                 # added numerators and denominators
        if d1 != d2:
            c.append(W + Fraction(n1 + n2, L))                   # changed the denominator but not the numerators
        if a + b >= L:
            c.append(right - 1)                                  # lost the whole from the improper fraction
            c.append(right + 1)                                  # counted one whole too many
        if mixed:
            c.append(Fraction(a + b, L) if a + b < L else Fraction(a + b - L, L))   # forgot the whole numbers
        if d1 != d2:
            c.append(W + Fraction(a + n2, L) if d2 != L else W + Fraction(n1 + b, L))   # changed only one fraction
            c.append(W + Fraction(n1 + n2, d1 * d2))             # multiplied the denominators, kept the numerators
        c.append(W + Fraction(n1 * n2, d1 * d2))                 # multiplied numerators and denominators
        c.append(miscount(W, a + b + 1, L))                      # miscounted the parts
        c.append(miscount(W, a + b - 1, L))
        c.append(W + Fraction(abs(a - b), L) if a != b else None)   # subtracted instead
    else:
        W = w1 - w2
        if a >= b:
            if d1 != d2:
                if n1 > n2 and d1 > d2:
                    c.append(W + Fraction(n1 - n2, d1 - d2))     # subtracted numerators and denominators
                c.append(W + Fraction(abs(n1 - n2), L) if n1 != n2 else None)   # changed the denominator only
                c.append(W + Fraction(a - n2, L) if d2 != L else W + Fraction(n1 - b, L))   # changed only one fraction
            if mixed and W:
                c.append(Fraction(a - b, L))                     # forgot the whole numbers
            c.append(val(x) + val(y))                            # added instead
            if not mixed:
                c.append(Fraction(L - (a - b), L))               # counted the parts that are not left
            c.append(miscount(W, a - b + 1, L))                  # miscounted the parts
            c.append(miscount(W, a - b - 1, L))
            if d1 != d2 and n1 != n2:
                c.append(W + Fraction(abs(n1 - n2), abs(d1 - d2)))   # took the smaller from the larger, top and bottom
                c.append(W + Fraction(abs(n1 - n2), d1 * d2))
        else:
            c.append(W + Fraction(b - a, L))                     # took the smaller fraction from the larger
            c.append(right + 1)                                  # renamed but did not take 1 from the wholes
            c.append(Fraction(a + L - b, L))                     # forgot the whole numbers
            if W > 1:
                c.append(W - 1 + Fraction(b - a, L))
            if L != 10 and 10 + a - b > 0:
                c.append(W - 1 + Fraction(10 + a - b, L))        # renamed 1 whole as 10, like with whole numbers
            c.append(W + Fraction(abs(n1 - n2), L) if n1 != n2 else None)
            c.append(val(x) + val(y))
    return c


def miscount(W, N, L):
    """One part too many or too few. Only kept when it is already in simplest form, so the slip stays visible."""
    r = N % L
    if N <= 0 or (r and math.gcd(r, L) > 1):
        return None
    return W + Fraction(N, L)


def P0(n, d):
    return (0, n, d)


def calc_q(x, y, op):
    sym = "+" if op == "+" else "−"
    return "%s %s %s = ?" % (mx(*x), sym, mx(*y)) + prompt_for(x, y, op)


def calc(x, y, op, rnd, extra=None):
    r = val(x) + val(y) if op == "+" else val(x) - val(y)
    c = wrong(x, y, op)
    if extra:
        c = extra + c
    return mcq(calc_q(x, y, op), r, c, e_calc(x, y, op), rnd)


def pair(a, b, c, d):
    return "%s and %s" % (fr(a, b), fr(c, d))


# ============================================================ set 1: same denominator
def set_same(rnd, P):
    SPOTS.left = []
    its = []
    # A: bar models
    for n1, n2, d, op in [(2, 3, 7, "+"), (1, 3, 5, "+"), (5, 3, 7, "-")]:
        x, y = P0(n1, d), P0(n2, d)
        if op == "+":
            q = (fig(one_bar_svg(d, n1, n2)) +
                 "The bar is split into %s. Green shows %s and yellow shows %s. What is %s + %s?"
                 % (WORD[d], fr(n1, d), fr(n2, d), fr(n1, d), fr(n2, d)))
            its.append(mcq(q, val(x) + val(y), [Fraction(d - n1 - n2, d)] + wrong(x, y, "+"), e_calc(x, y, "+"), rnd))
        else:
            q = (fig(one_bar_svg(d, n1, 0, crossed=n2)) +
                 "The bar is split into %s. The shaded part is %s, and %s is crossed out. What is %s − %s?"
                 % (WORD[d], fr(n1, d), fr(n2, d), fr(n1, d), fr(n2, d)))
            look = [Fraction(d - n1 + n2, d), Fraction(n1, d)]   # counted white + crossed parts; ignored the crosses
            its.append(mcq(q, val(x) - val(y), look + wrong(x, y, "-"), e_calc(x, y, "-"), rnd))
    # B: add
    assert Fraction(1, 5) * 2 + Fraction(2, 5) == Fraction(4, 5)
    e = ("The denominators are the same. Add the numerators: 1 + 1 + 2 = 4. The denominator stays 5. "
         "The answer is <b>%s</b>." % fr(4, 5))
    its.append(mcq("%s + %s + %s = ?" % (fr(1, 5), fr(1, 5), fr(2, 5)), Fraction(4, 5),
                   [Fraction(4, 15), Fraction(2, 5), Fraction(3, 5)], e, rnd))
    for n1, n2, d in [(3, 5, 11), (2, 5, 9), (2, 4, 7), (4, 6, 11), (1, 7, 9), (3, 1, 7)]:
        x, y = P0(n1, d), P0(n2, d)
        assert val(x) + val(y) < 1
        its.append(calc(x, y, "+", rnd))
    # C: subtract
    for n1, n2, d in [(6, 2, 7), (8, 5, 11), (4, 1, 5), (10, 3, 11), (7, 5, 9)]:
        x, y = P0(n1, d), P0(n2, d)
        its.append(calc(x, y, "-", rnd))
    its.append(calc((1, 0, 5), P0(2, 5), "-", rnd))
    # D: missing numbers
    assert Fraction(3, 7) + Fraction(3, 7) == Fraction(6, 7)
    e = "Work out %s − %s = %s. Check: %s + %s = %s. The answer is <b>%s</b>." % (
        fr(6, 7), fr(3, 7), fr(3, 7), fr(3, 7), fr(3, 7), fr(6, 7), fr(3, 7))
    its.append(mcq("%s + %s = %s" % (fr(3, 7), frq(7), fr(6, 7)), Fraction(3, 7),
                   [Fraction(9, 7), Fraction(3, 14), Fraction(2, 7)], e, rnd))
    assert Fraction(7, 9) - Fraction(2, 9) == Fraction(5, 9)
    e = "Use the inverse: %s + %s = %s. Check: %s − %s = %s. The answer is <b>%s</b>." % (
        fr(5, 9), fr(2, 9), fr(7, 9), fr(7, 9), fr(2, 9), fr(5, 9), fr(7, 9))
    its.append(mcq("%s − %s = %s" % (frq(9), fr(2, 9), fr(5, 9)), Fraction(7, 9),
                   [Fraction(1, 3), Fraction(7, 18), Fraction(8, 9)], e, rnd))
    # E: spot the mistake
    n, he, his = P.next()
    q = "%s wrote %s + %s = %s. What mistake did %s make?" % (n, fr(2, 7), fr(3, 7), fr(5, 14), he)
    e = ("The parts are all sevenths, so the answer is in sevenths too. Add only the numerators: "
         "%s + %s = <b>%s</b>. %s added the denominators as well." % (fr(2, 7), fr(3, 7), fr(5, 7), cap(he)))
    its.append(mcq(q, "%s added the denominators" % cap(he),
                   ["%s added the numerators" % cap(he), "%s should have multiplied" % cap(he), "There is no mistake"], e, rnd))
    sums = [("2 4 7 +", Fraction(6, 7)), ("3 2 7 +", Fraction(5, 7)), ("4 3 7 +", Fraction(1)), ("5 1 7 -", Fraction(4, 7))]
    ch = []
    for s, v in sums:
        a, b, d, op = s.split()
        a, b, d = int(a), int(b), int(d)
        assert (Fraction(a, d) + Fraction(b, d) if op == "+" else Fraction(a, d) - Fraction(b, d)) == v
        ch.append("%s %s %s" % (fr(a, d), "+" if op == "+" else "−", fr(b, d)))
    e = ("%s + %s = %s. The others make %s, %s = 1 and %s."
         % (fr(2, 7), fr(4, 7), fr(6, 7), fr(5, 7), fr(7, 7), fr(4, 7)))
    e = e.replace(fr(6, 7) + ".", "<b>" + fr(6, 7) + "</b>.", 1)
    its.append(mcq("Which calculation has an answer of %s?" % fr(6, 7), ch[0], ch[1:], e, rnd))
    assert len(its) == 20, len(its)
    return {"title": "Same denominator", "items": its}


# ============================================================ set 2: one denominator a multiple of the other
def set_related(rnd):
    SPOTS.left = []
    its = []
    # A: bar models
    for n1, d1, n2, d2, op in [(1, 2, 1, 4, "+"), (2, 5, 3, 10, "+"), (3, 4, 1, 8, "-"), (5, 6, 1, 3, "-")]:
        L = lcm(d1, d2)
        k1, k2 = n1 * L // d1, n2 * L // d2
        x, y = P0(n1, d1), P0(n2, d2)
        if op == "+":
            q = (fig(one_bar_svg(L, k1, k2)) +
                 "The bar is split into %s. Green shows %s and yellow shows %s. What is %s + %s?"
                 % (WORD[L], fr(n1, d1), fr(n2, d2), fr(n1, d1), fr(n2, d2)) + prompt_for(x, y, "+"))
            its.append(mcq(q, val(x) + val(y), wrong(x, y, "+"), e_calc(x, y, "+"), rnd))
        else:
            q = (fig(one_bar_svg(L, k1, 0, crossed=k2)) +
                 "The bar is split into %s. The shaded part is %s, and %s is crossed out. What is %s − %s?"
                 % (WORD[L], fr(n1, d1), fr(n2, d2), fr(n1, d1), fr(n2, d2)) + prompt_for(x, y, "-"))
            look = [Fraction(L - k1 + k2, L), Fraction(n1, d1)]
            its.append(mcq(q, val(x) - val(y), look + wrong(x, y, "-"), e_calc(x, y, "-"), rnd))
    # B: two bars – the same fraction in smaller parts
    for n1, d1, n2, d2 in [(1, 4, 3, 8), (2, 3, 1, 6)]:
        L = d2
        k = L // d1
        q = (fig(two_bars_svg(d1, n1, d2, n2, L)) +
             "The green part is %s and the yellow part is %s. The dashed lines split the green bar into %s. "
             "How many %s is the green part?" % (fr(n1, d1), fr(n2, d2), WORD[L], WORD[L]))
        e = ("Each %s is split into %d. So %s = %s: there are <b>%s</b> in the green part. "
             "Now both fractions are in %s, so you can add or subtract them."
             % (WORD[d1][:-1] if d1 != 4 else "quarter", k, fr(n1, d1), fr(n1 * k, L), fr(n1 * k, L), WORD[L]))
        its.append(mcq(q, fr(n1 * k, L), [fr(n1, L), fr(n2, L), fr(n1 * k + n2, L)], e, rnd))
    # C: the first step
    for n1, d1, L in [(3, 5, 10), (5, 6, 12)]:
        k = L // d1
        q = "Which fraction is equal to %s?" % fr(n1, d1)
        e = ("%d × %d = %d, so multiply the numerator by %d too: %d × %d = %d. %s = <b>%s</b>."
             % (d1, k, L, k, n1, k, n1 * k, fr(n1, d1), fr(n1 * k, L)))
        bad = [fr(n1, L), fr(n1 + L - d1, L), fr(n1 * k, d1)]   # changed only the denominator; added the same number; multiplied only the numerator
        assert Fraction(n1, d1) == Fraction(n1 * k, L)
        its.append(mcq(q, fr(n1 * k, L), bad, e, rnd))
    # D: add
    for n1, d1, n2, d2 in [(1, 4, 3, 8), (1, 3, 4, 9), (1, 6, 7, 12), (3, 8, 1, 2), (1, 10, 3, 5), (2, 9, 1, 3)]:
        x, y = P0(n1, d1), P0(n2, d2)
        assert val(x) + val(y) < 1
        its.append(calc(x, y, "+", rnd))
    # E: subtract
    for n1, d1, n2, d2 in [(7, 8, 1, 4), (9, 10, 1, 5), (11, 12, 1, 3), (4, 5, 3, 10), (5, 9, 1, 3), (3, 4, 5, 8)]:
        x, y = P0(n1, d1), P0(n2, d2)
        assert val(x) - val(y) > 0
        its.append(calc(x, y, "-", rnd))
    assert len(its) == 20, len(its)
    return {"title": "Related denominators", "items": its}


# ============================================================ set 3: answers greater than 1
def set_improper(rnd):
    SPOTS.left = []
    its = []
    # A: improper fraction to mixed numeral
    for n, d in [(7, 5), (11, 4), (17, 6)]:
        w, r = divmod(n, d)
        bad = [fr(r, d), mx(w + 1, r, d), mx(w, r, n)]     # dropped the whole; one whole too many; used the numerator as denominator
        e = ("%d ÷ %d = %d remainder %d. So %s is %d whole%s and %s left over: <b>%s</b>."
             % (n, d, w, r, fr(n, d), w, "" if w == 1 else "s", fr(r, d), mx(w, r, d)))
        its.append(mcq("Write %s as a mixed numeral." % fr(n, d), mx(w, r, d), bad, e, rnd))
    # B: pictures
    for n1, d1, n2, d2 in [(4, 5, 3, 5), (7, 8, 3, 4)]:
        L = lcm(d1, d2)
        k1, k2 = n1 * L // d1, n2 * L // d2
        x, y = P0(n1, d1), P0(n2, d2)
        q = (fig(wholes_svg(L, k1, k2)) +
             "Each bar is 1 whole, split into %s. Green shows %s and yellow shows %s. What is %s + %s?"
             % (WORD[L], fr(n1, d1), fr(n2, d2), fr(n1, d1), fr(n2, d2)) + prompt_for(x, y, "+"))
        e = "One bar is full, and %d more %s are shaded in the second bar. " % (k1 + k2 - L, WORD[L]) + e_calc(x, y, "+")
        its.append(mcq(q, val(x) + val(y), wrong(x, y, "+"), e, rnd))
    # C: same denominator, more than 1
    for n1, n2, d in [(2, 4, 5), (5, 4, 7), (7, 5, 9), (7, 9, 10), (5, 7, 8)]:
        x, y = P0(n1, d), P0(n2, d)
        assert val(x) + val(y) > 1
        its.append(calc(x, y, "+", rnd))
    # D: related denominators, more than 1
    for n1, d1, n2, d2 in [(3, 4, 5, 8), (2, 3, 5, 6), (4, 5, 9, 10), (5, 6, 7, 12), (1, 2, 7, 10), (7, 9, 2, 3), (3, 4, 7, 12)]:
        x, y = P0(n1, d1), P0(n2, d2)
        assert val(x) + val(y) > 1
        its.append(calc(x, y, "+", rnd))
    # E: three fractions
    for fs, L in [([(3, 4), (1, 2), (1, 8)], 8), ([(2, 3), (5, 6), (1, 6)], 6), ([(3, 5), (7, 10), (1, 2)], 10)]:
        tot = sum(Fraction(a, b) for a, b in fs)
        nums = [a * L // b for a, b in fs]
        N = sum(nums)
        assert Fraction(N, L) == tot and tot > 1
        rw = ["%s = %s" % (fr(a, b), fr(a * L // b, L)) for a, b in fs if b != L]
        e = ("%d is a multiple of the other denominators, so use %s. %s. Add the numerators: %s = %d, so the total is %s. "
             % (L, WORD[L], cap(" and ".join(rw)) if rw else "", " + ".join(map(str, nums)), N, fr(N, L)))
        s, v = finish(0, N, L)
        assert v == tot
        e += s
        cands = [Fraction(sum(a for a, b in fs), sum(b for a, b in fs)),   # added numerators and denominators
                 Fraction(sum(a for a, b in fs), L),                      # changed the denominator only
                 tot - 1, tot + 1]
        q = " + ".join(fr(a, b) for a, b in fs) + " = ?"
        rem = N % L
        q += "<br>Give your answer as a mixed numeral%s." % (" in its simplest form" if math.gcd(rem, L) > 1 else "")
        its.append(mcq(q, tot, cands, e, rnd))
    assert len(its) == 20, len(its)
    return {"title": "Answers greater than 1", "items": its}


# ============================================================ set 4: mixed numerals
def set_mixed(rnd):
    SPOTS.left = []
    its = []
    groups = [
        ("+", [((1, 2, 5), (2, 1, 5)), ((2, 3, 7), (1, 2, 7))]),                       # same denominator
        ("+", [((1, 4, 5), (1, 3, 5)), ((2, 5, 7), (1, 4, 7))]),                       # same denominator, renaming
        ("+", [((1, 1, 2), (2, 1, 4)), ((1, 1, 5), (3, 1, 10)), ((2, 1, 4), (1, 3, 8))]),  # related
        ("+", [((1, 1, 2), (2, 3, 4)), ((2, 5, 6), (1, 1, 3)), ((3, 7, 10), (1, 1, 2))]),  # related, renaming
        ("-", [((3, 0, 8), P0(3, 8)), ((2, 0, 5), P0(2, 5)), ((4, 0, 6), P0(5, 6))]),     # whole number minus a fraction
        ("-", [((2, 7, 8), P0(1, 2)), ((3, 1, 4), P0(3, 8))]),                          # mixed numeral minus a fraction
        ("-", [((5, 9, 10), (2, 1, 5)), ((3, 4, 5), (1, 2, 5))]),                       # no renaming
        ("-", [((4, 1, 5), (1, 3, 5)), ((5, 1, 4), (2, 5, 8)), ((6, 3, 10), (2, 1, 2))]),  # renaming
    ]
    for op, grp in groups:
        for x, y in grp:
            its.append(calc(x, y, op, rnd))
    assert len(its) == 20, len(its)
    return {"title": "Add and subtract mixed numerals", "items": its}


# ============================================================ set 5: word problems
def set_words(rnd, P):
    SPOTS.left = []
    its = []

    def word(q, x, y, op, units, extra=None, pre="", post=""):
        r = val(x) + val(y) if op == "+" else val(x) - val(y)
        c = wrong(x, y, op)
        if extra:
            c = extra + c
        its.append(mcq(q + prompt_for(x, y, op), r, c, pre + e_calc(x, y, op, units) + post, rnd, units))

    def amt(x, units):
        return mx(*x) + unit_for(val(x), units)

    n, he, his = P.next()
    word("A bottle holds %s of juice. %s drinks %s. How much juice is left in the bottle?"
         % (amt(P0(7, 10), LITRE), n, amt(P0(1, 5), LITRE)), P0(7, 10), P0(1, 5), "-", LITRE)
    n, he, his = P.next()
    word("%s walks %s to %s friend’s house, then %s to the park. How far does %s walk altogether?"
         % (n, amt(P0(3, 4), KM), his, amt(P0(5, 8), KM), he), P0(3, 4), P0(5, 8), "+", KM)
    word("In a school garden bed, %s is planted with lettuce and %s with carrots. What fraction of the garden bed is planted?"
         % (fr(1, 3), fr(1, 6)), P0(1, 3), P0(1, 6), "+", None)

    assert 1 - Fraction(2, 5) - Fraction(3, 10) == Fraction(3, 10)
    e = ("First add the parts you know. Use tenths: %s = %s, so %s + %s = %s. "
         "The whole garden bed is %s. Herbs: %s − %s = <b>%s</b>."
         % (fr(2, 5), fr(4, 10), fr(4, 10), fr(3, 10), fr(7, 10), fr(10, 10), fr(10, 10), fr(7, 10), fr(3, 10)))
    its.append(mcq("In a garden bed, %s is tomatoes and %s is beans. The rest is herbs. What fraction of the garden bed is herbs?"
                   % (fr(2, 5), fr(3, 10)), Fraction(3, 10),
                   [Fraction(7, 10), Fraction(1, 2), Fraction(5, 15)], e, rnd))

    n, he, his = P.next()
    word("%s has %s of ribbon. %s uses %s to wrap a birthday present. How much ribbon is left?"
         % (n, amt((2, 1, 2), M), cap(he), amt(P0(3, 4), M)), (2, 1, 2), P0(3, 4), "-", M)
    (n1, _, _), (n2, _, _) = P.next(), P.next()
    word("%s and %s share a pizza. %s eats %s of it and %s eats %s. What fraction of the pizza do they eat altogether?"
         % (n1, n2, n1, fr(3, 8), n2, fr(1, 4)), P0(3, 8), P0(1, 4), "+", None)

    (n1, _, _), (n2, _, _) = P.next(), P.next()
    assert 1 - Fraction(1, 6) - Fraction(1, 3) == Fraction(1, 2)
    e = ("First add what they eat. Use sixths: %s = %s, so %s + %s = %s. The whole pavlova is %s. "
         "Left: %s − %s = %s. Simplify: %s = <b>%s</b>."
         % (fr(1, 3), fr(2, 6), fr(1, 6), fr(2, 6), fr(3, 6), fr(6, 6), fr(6, 6), fr(3, 6), fr(3, 6), fr(3, 6), fr(1, 2)))
    its.append(mcq("%s eats %s of a pavlova and %s eats %s of it. What fraction of the pavlova is left?" % (n1, fr(1, 6), n2, fr(1, 3))
                   + "<br>Give your answer in its simplest form.", Fraction(1, 2),
                   [Fraction(2, 9), Fraction(7, 9), Fraction(2, 3)], e, rnd))

    n, he, his = P.next()
    word("%s spends %s at netball training and half an hour on homework. How long does %s spend altogether?"
         % (n, amt(P0(3, 4), HOUR), he), P0(3, 4), P0(1, 2), "+", HOUR,
         post=" (That is 1 hour 15 minutes.)")
    n, he, his = P.next()
    word("%s runs %s on Monday and %s on Tuesday to train for the cross-country. How far does %s run in total?"
         % (n, amt((1, 3, 10), KM), amt((1, 4, 5), KM), he), (1, 3, 10), (1, 4, 5), "+", KM)
    (n1, _, _), (n2, _, _) = P.next(), P.next()
    word("At the beach, %s swims %s. %s swims %s. How much further does %s swim than %s?"
         % (n1, amt(P0(4, 5), KM), n2, amt(P0(7, 10), KM), n1, n2), P0(4, 5), P0(7, 10), "-", KM,
         pre="“How much further” means subtract. ")
    word("A tin holds %s of paint. A painter uses %s on a fence. How much paint is left in the tin?"
         % (amt((2, 0, 8), LITRE), amt(P0(5, 8), LITRE)), (2, 0, 8), P0(5, 8), "-", LITRE)
    word("For a bake sale, a class uses %s of flour for bread and %s for Anzac biscuits. How much flour do they use altogether?"
         % (amt((1, 1, 4), KG), amt(P0(3, 8), KG)), (1, 1, 4), P0(3, 8), "+", KG)
    word("In a class, %s of the students walk to school and %s come by car. What fraction of the class walk or come by car?"
         % (fr(5, 12), fr(1, 3)), P0(5, 12), P0(1, 3), "+", None)
    n, he, his = P.next()
    word("%s’s drink bottle holds %s of water. At sport, %s drinks %s. How much water is left?"
         % (n, amt(P0(3, 4), LITRE), he, amt(P0(5, 12), LITRE)), P0(3, 4), P0(5, 12), "-", LITRE)
    word("On a school excursion, a class walks %s along a bush track and %s back to the bus. How far do they walk altogether?"
         % (amt((2, 1, 2), KM), amt((1, 3, 4), KM)), (2, 1, 2), (1, 3, 4), "+", KM)
    n, he, his = P.next()
    word("A movie lasts %s. %s has watched %s of it. How much of the movie is left to watch?"
         % (amt((1, 1, 2), HOUR), n, amt(P0(3, 4), HOUR)), (1, 1, 2), P0(3, 4), "-", HOUR,
         post=" (That is 45 minutes.)")
    n, he, his = P.next()
    word("%s eats %s of a block of chocolate after lunch and %s of the block after dinner. How much of the block does %s eat?"
         % (n, fr(2, 9), fr(1, 3), he), P0(2, 9), P0(1, 3), "+", None)

    n, he, his = P.next()
    assert Fraction(1, 4) + Fraction(1, 8) == Fraction(3, 8)
    e = ("%s added the numerators and the denominators. Quarters and eighths are different sizes, so use eighths: "
         "%s = %s, and %s + %s = %s. The answer is <b>%s</b>."
         % (n, fr(1, 4), fr(2, 8), fr(2, 8), fr(1, 8), fr(3, 8), fr(3, 8)))
    its.append(mcq("%s works out %s + %s and gets %s. Which is true?" % (n, fr(1, 4), fr(1, 8), fr(2, 12)),
                   "%s is wrong. It is %s" % (cap(he), fr(3, 8)),
                   ["%s is right" % cap(he), "%s is wrong. It is %s" % (cap(he), fr(2, 8)),
                    "%s is wrong. It is %s" % (cap(he), fr(1, 32))], e, rnd))

    pairs = [((2, 3), (2, 6)), ((3, 5), (3, 10)), ((1, 2), (3, 8)), ((5, 6), (1, 3))]
    sums = [Fraction(*p) + Fraction(*q) for p, q in pairs]
    assert sums[0] == 1 and all(s != 1 for s in sums[1:]) and len(set(sums)) == 4
    e = ("%s = %s, and %s + %s = %s = 1, so <b>%s</b> is correct. The other totals are %s, %s and %s."
         % (fr(2, 3), fr(4, 6), fr(4, 6), fr(2, 6), fr(6, 6), pair(2, 3, 2, 6),
            show(sums[1]), show(sums[2]), show(sums[3])))
    its.append(mcq("Which pair of fractions has a total of 1?", pair(2, 3, 2, 6),
                   [pair(p[0], p[1], q[0], q[1]) for p, q in pairs[1:]], e, rnd))

    assert 1 - Fraction(3, 8) - Fraction(1, 4) == Fraction(3, 8)
    e = ("1 L = %s L. In it now: %s + %s = %s + %s = %s L. Space left: %s − %s = <b>%s L</b>."
         % (fr(8, 8), fr(3, 8), fr(1, 4), fr(3, 8), fr(2, 8), fr(5, 8), fr(8, 8), fr(5, 8), fr(3, 8)))
    its.append(mcq("A 1 L jug has %s L of orange juice and %s L of pineapple juice in it. How much more can it hold?"
                   % (fr(3, 8), fr(1, 4)), Fraction(3, 8),
                   [Fraction(5, 8), Fraction(3, 4), Fraction(1, 2)], e, rnd, LITRE))
    assert len(its) == 20, len(its)
    return {"title": "Word problems", "items": its}


# ============================================================ lesson
def body_html():
    f_same = one_bar_svg(7, 2, 3, W=360)
    f_bars = two_bars_svg(4, 1, 8, 3, 8, W=360, labels=True)
    f_wholes = wholes_svg(5, 4, 3, W=360)
    return (
        "<h2>Same denominator: add the numerators</h2>"
        "<p>The <b>denominator</b> tells you the size of the parts. The <b>numerator</b> tells you how many parts. "
        "When the denominators are the same, the parts are the same size, so you just add or subtract the numerators. "
        "The denominator stays the same.</p>"
        "<figure class='sn-fig'>" + f_same +
        "<figcaption>2 sevenths and 3 sevenths make 5 sevenths: " + fr(2, 7) + " + " + fr(3, 7) + " = " + fr(5, 7) +
        ".</figcaption></figure>"
        + ex("Example", fr(6, 7) + " − " + fr(2, 7) + " = ?",
             "The denominators are the same. Subtract the numerators: 6 − 2 = 4. The denominator stays 7.", fr(4, 7)) +
        "<h2>Related denominators: one is a multiple of the other</h2>"
        "<p>Quarters and eighths are different sizes. 8 is a multiple of 4, so change the quarters into eighths. "
        "Multiply the numerator and the denominator by the <b>same number</b>.</p>"
        "<figure class='sn-fig'>" + f_bars +
        "<figcaption>The dashed lines split the quarters into eighths. " + fr(1, 4) + " = " + fr(2, 8) +
        ".</figcaption></figure>"
        + ex("Example", fr(1, 4) + " + " + fr(3, 8) + " = ?",
             "4 × 2 = 8, so " + fr(1, 4) + " = " + fr(2, 8) + ". Add the numerators: " + fr(2, 8) + " + " + fr(3, 8) +
             " = " + fr(5, 8) + ".", fr(5, 8))
        + ex("Example", fr(5, 6) + " − " + fr(1, 3) + " = ?",
             "6 is a multiple of 3, so " + fr(1, 3) + " = " + fr(2, 6) + ". " + fr(5, 6) + " − " + fr(2, 6) + " = " + fr(3, 6) +
             ". This is the same as " + fr(1, 2) + ".", fr(3, 6) + " = " + fr(1, 2)) +
        "<h2>Answers greater than 1</h2>"
        "<p>If the numerator is bigger than the denominator, the answer is an <b>improper fraction</b>. "
        "Change it to a <b>mixed numeral</b>: divide the numerator by the denominator.</p>"
        "<figure class='sn-fig'>" + f_wholes +
        "<figcaption>" + fr(4, 5) + " + " + fr(3, 5) + " = " + fr(7, 5) + ". One whole bar and 2 more fifths: 1 " +
        fr(2, 5) + ".</figcaption></figure>"
        + ex("Example", fr(2, 5) + " + " + fr(4, 5) + " = ?",
             fr(2, 5) + " + " + fr(4, 5) + " = " + fr(6, 5) + ". 6 ÷ 5 = 1 remainder 1, so " + fr(6, 5) + " = 1 " + fr(1, 5) + ".",
             "1 " + fr(1, 5)) +
        "<h2>Mixed numerals</h2>"
        "<p>Add or subtract the fractions, then the whole numbers. If the fractions make more than 1, add 1 more whole. "
        "If the first fraction is too small to subtract from, <b>rename 1 whole</b>.</p>" +
        table(["Calculation", "Fractions", "Whole numbers", "Answer"], [
            ["1 " + fr(1, 2) + " + 2 " + fr(3, 4), fr(2, 4) + " + " + fr(3, 4) + " = " + fr(5, 4) + " = 1 " + fr(1, 4),
             "1 + 2 + 1 = 4", "4 " + fr(1, 4)],
            ["3 − " + fr(3, 8), "rename: 3 = 2 " + fr(8, 8) + ", " + fr(8, 8) + " − " + fr(3, 8) + " = " + fr(5, 8),
             "2", "2 " + fr(5, 8)],
            ["5 " + fr(1, 4) + " − 2 " + fr(5, 8), "rename: 4 " + fr(10, 8) + " − 2 " + fr(5, 8) + ", " + fr(10, 8) + " − " +
             fr(5, 8) + " = " + fr(5, 8), "4 − 2 = 2", "2 " + fr(5, 8)],
        ])
        + ex("Example", "3 − " + fr(3, 8) + " = ?",
             "Rename 1 whole as " + fr(8, 8) + ": 3 = 2 " + fr(8, 8) + ". Then " + fr(8, 8) + " − " + fr(3, 8) + " = " +
             fr(5, 8) + ".", "2 " + fr(5, 8)) +
        "<h2>Common mistakes</h2>" +
        table(["Mistake", "What to do instead"], [
            [fr(2, 7) + " + " + fr(3, 7) + " = " + fr(5, 14) + " (adding the denominators)",
             "Keep the denominator: " + fr(5, 7)],
            [fr(1, 4) + " + " + fr(3, 8) + " = " + fr(4, 8) + " (changing the denominator but not the numerator)",
             "Multiply the numerator too: " + fr(1, 4) + " = " + fr(2, 8) + ", so the total is " + fr(5, 8)],
            [fr(7, 5) + " = 2 " + fr(2, 5) + " (one whole too many)",
             "7 ÷ 5 = 1 remainder 2, so " + fr(7, 5) + " = 1 " + fr(2, 5)],
            ["3 − " + fr(3, 8) + " = 3 " + fr(3, 8) + " (writing the numbers side by side)",
             "Rename 1 whole: 2 " + fr(8, 8) + " − " + fr(3, 8) + " = 2 " + fr(5, 8)],
        ])
    )


FAQ = [
    {"q": "What fractions do Year 5 students add and subtract in the Australian Curriculum?",
     "a": "Fractions with the same denominator, and fractions with related denominators, where one denominator is a multiple of the other, such as 1/4 + 3/8 or 5/6 − 1/3 (AC9M5N05). Answers greater than 1 are written as mixed numerals."},
    {"q": "How do you teach adding fractions with different denominators in Year 5?",
     "a": "Start with a bar model. Show that 1/4 is the same as 2/8, so 1/4 + 3/8 becomes 2/8 + 3/8 = 5/8. Then practise changing one fraction by multiplying the numerator and denominator by the same number."},
    {"q": "How do you subtract a fraction from a whole number?",
     "a": "Rename 1 whole as a fraction with the same denominator. For 3 − 3/8, write 3 as 2 8/8, then 8/8 − 3/8 = 5/8, so the answer is 2 5/8. A common mistake is to write 3 3/8."},
    {"q": "Are fractions on the Year 5 NAPLAN numeracy test?",
     "a": "NAPLAN numeracy is based on the Australian Curriculum, so Year 5 students can meet fraction questions in March. Practising same and related denominators, mixed numerals and word problems helps students prepare."},
]


def gen_unit():
    rnd = random.Random(5805)
    P = People(rnd)
    sets = [set_same(rnd, P), set_related(rnd), set_improper(rnd), set_mixed(rnd), set_words(rnd, P)]
    seen = set()
    for s in sets:
        assert len(s["items"]) == 20, (s["title"], len(s["items"]))
        assert sorted(it["a"] for it in s["items"]) == sorted([0, 1, 2, 3] * 5), s["title"]
        for it in s["items"]:
            assert len(set(it["c"])) == 4, it
            assert it["q"] not in seen, it["q"]
            seen.add(it["q"])
    return {
        "country": "au", "subject": "maths", "grade": "year-5", "slug": "adding-and-subtracting-fractions", "sort": 5,
        "updated": UPDATED, "pdf_url": "",
        "title": "Year 5 Adding and Subtracting Fractions",
        "seo_title": "Year 5 Adding and Subtracting Fractions Worksheets: Free Maths with Answer Key (Australian Curriculum)",
        "short_title": "Adding and Subtracting Fractions",
        "domain": "Number",
        "standard_code": "AC9M5N05",
        "standard_url": "https://v9.australiancurriculum.edu.au/f-10-curriculum/learning-areas/mathematics",
        "standard_text": "Solve problems involving addition and subtraction of fractions with the same or related denominators, using different strategies",
        "meta_desc": "Free Year 5 maths worksheets on adding and subtracting fractions, aligned to the Australian Curriculum (AC9M5N05): same and related denominators, bar models, answers as mixed numerals, mixed numerals and word problems. 100 questions with an answer key, great for NAPLAN practice.",
        "key_big": "Make the parts the same size, then add or subtract the numerators. The denominator stays the same.",
        "key_sub": "1/4 + 3/8 = 2/8 + 3/8 = 5/8, not 4/12. If the answer is more than 1, write it as a mixed numeral: 6/5 = 1 1/5.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }


if __name__ == "__main__":
    u = gen_unit()
    mark_large(u, "(two bars|bar of)")
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(u, f, ensure_ascii=False, indent=1)
    print("wrote", path)
