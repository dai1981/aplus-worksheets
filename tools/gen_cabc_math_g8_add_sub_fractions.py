# -*- coding: utf-8 -*-
"""
BC Grade 8 Math: Adding and Subtracting Fractions
(BC Mathematics Curriculum, Grade 8: Computational fluency — operations with fractions)
  python3 tools/gen_cabc_math_g8_add_sub_fractions.py
Unlike denominators (lowest common denominators), mixed numbers with regrouping, simplest form,
order of operations with + and − (left to right, brackets) and BC word problems.
Every answer is in simplest form; wrong choices come from
real mistakes (adding the denominators, not regrouping, changing only the denominator) and are
also in simplest form. A wrong choice is never equal in value to the right answer or to another
choice. Every answer is checked in code with fractions.Fraction.
HTML attributes use single quotes (no backslashes in the JSON). Canadian English.
"""
import json, math, os, random, re
from fractions import Fraction

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "ca-bc", "math", "grade-8")
UPDATED = "2026-11-02"
FILL = "#4fae74"      # first fraction
FILL2 = "#f2b84b"     # second fraction
RED = "#c0392b"
BLUE = "#2f6db5"
LINE = "#2b2b2b"
GIRLS = ["Olivia", "Ava", "Chloe", "Simran", "Jasleen", "Mei", "Ji-woo", "Hana", "Sofia", "Emma", "Leah", "Zara", "Nadia"]
BOYS = ["Liam", "Ethan", "Noah", "Arjun", "Harjot", "Wei", "Mateo", "Lucas", "Kai", "Owen", "Ryan"]
WORD = {2: "halves", 3: "thirds", 4: "fourths", 7: "sevenths", 11: "elevenths", 5: "fifths", 6: "sixths", 8: "eighths", 9: "ninths", 10: "tenths",
        12: "twelfths", 15: "fifteenths", 18: "eighteenths", 20: "twentieths", 24: "twenty-fourths", 30: "thirtieths"}
SIMPLE = "<br>Give your answer in simplest form."
MIXED = "<br>Give your answer as a mixed number in simplest form."


# ------------------------------------------------------------ numbers
def fr(a, b):
    return "<span class='fr'><span class='fn'>%s</span><span class='fd'>%s</span></span>" % (a, b)


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
CUP = (" cup", " cup", " cups")
HOUR = (" of an hour", " hour", " hours")


def unit_for(v, units):
    if not units:
        return ""
    return units[0] if v < 1 else (units[1] if v == 1 else units[2])


def withu(v, units):
    return show(v) + unit_for(v, units)


def cap(s):
    return s[0].upper() + s[1:]


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


def tick_line(Lw, d, Y, x0, x1):
    s = ["<line x1='%.1f' y1='%d' x2='%.1f' y2='%d' stroke='%s' stroke-width='2.5'/>" % (x0, Y, x1, Y, LINE)]
    n = Lw * d
    for i in range(n + 1):
        X = x0 + (x1 - x0) * i / n
        whole = (i % d == 0)
        s.append("<line x1='%.1f' y1='%d' x2='%.1f' y2='%d' stroke='%s' stroke-width='%s'/>"
                 % (X, Y - (11 if whole else 7), X, Y + (11 if whole else 7), LINE, "2.5" if whole else "1.6"))
        if whole:
            s.append("<text x='%.1f' y='%d' font-size='16' font-weight='700' fill='%s' text-anchor='middle'>%d</text>"
                     % (X, Y + 30, LINE, i // d))
    return "".join(s)


def jump_line_svg(Lw, d, start, end, W=380):
    """Number line 0..Lw in steps of 1/d. A dot at start and a curved arrow (jump) from start to end."""
    x0, x1 = 16, W - 16
    Y = 58
    Xs = x0 + (x1 - x0) * float(start) / Lw
    Xe = x0 + (x1 - x0) * float(end) / Lw
    top = Y - 20
    s = [tick_line(Lw, d, Y, x0, x1),
         "<circle cx='%.1f' cy='%d' r='6' fill='%s'/>" % (Xs, Y, BLUE),
         "<path d='M%.1f %d Q%.1f %d %.1f %d' fill='none' stroke='%s' stroke-width='3'/>"
         % (Xs, Y - 8, (Xs + Xe) / 2, top - 52, Xe, top + 2, BLUE),
         "<path d='M%.1f %d L%.1f %d L%.1f %d Z' fill='%s'/>" % (Xe - 7, top - 4, Xe + 7, top - 4, Xe, Y - 9, BLUE)]
    return svg_wrap(W, Y + 38, "".join(s),
                    "number line from 0 to %d with each whole split into %d equal parts, a dot and a curved jump arrow" % (Lw, d))


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


def common(d1, d2):
    L = lcm(d1, d2)
    if L == max(d1, d2):
        return "%d is a multiple of %d, so use %d as the common denominator. " % (max(d1, d2), min(d1, d2), L)
    return "The lowest common multiple of %d and %d is %d, so use %d as the common denominator. " % (d1, d2, L, L)


def e_calc(x, y, op, units=None):
    """Step explanation for x op y. x, y = (whole, numerator, denominator)."""
    (w1, n1, d1), (w2, n2, d2) = x, y
    L = lcm(d1, d2)
    a, b = n1 * L // d1, n2 * L // d2
    t = common(d1, d2)
    rw = ["%s = %s" % (mx(w, n, d), mx(w, n * L // d, L)) for w, n, d in (x, y) if d != L]
    t += "Write the equivalent fraction: " if len(rw) == 1 else "Write equivalent fractions: "
    t += " and ".join(rw) + ". "
    mixed = w1 or w2
    if op == "+":
        if not mixed:
            t += "Add the numerators: %s + %s = %s. " % (fr(a, L), fr(b, L), fr(a + b, L))
            s, v = finish(0, a + b, L, units)
        else:
            t += "Add the fractions: %s + %s = %s. " % (fr(a, L), fr(b, L), fr(a + b, L))
            t += ("Add the whole numbers: %d + %d = %d. " % (w1, w2, w1 + w2)) if (w1 and w2) else "The whole number is %d. " % (w1 + w2)
            s, v = finish(w1 + w2, a + b, L, units)
        assert v == val(x) + val(y)
    else:
        if not mixed:
            t += "Subtract the numerators: %s − %s = %s. " % (fr(a, L), fr(b, L), fr(a - b, L))
            s, v = finish(0, a - b, L, units)
        elif a >= b:
            t += "Subtract the fractions: %s − %s = %s. " % (fr(a, L), fr(b, L), fr(a - b, L))
            t += ("Subtract the whole numbers: %d − %d = %d. " % (w1, w2, w1 - w2)) if w2 else "The whole number stays %d. " % w1
            s, v = finish(w1 - w2, a - b, L, units)
        else:
            t += ("%s is less than %s, so regroup: rename 1 whole as %s. %s = %s. Subtract the fractions: %s − %s = %s. "
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
    L = lcm(d1, d2)
    a, b = n1 * L // d1, n2 * L // d2
    right = val(x) + val(y) if op == "+" else val(x) - val(y)
    mixed = w1 or w2
    c = []
    if op == "+":
        W = w1 + w2
        c.append(W + Fraction(n1 + n2, d1 + d2))                 # added numerators and denominators
        c.append(W + Fraction(n1 + n2, L))                       # changed the denominator but not the numerators
        if a + b >= L:
            c.append(right - 1)                                  # lost the whole from the improper fraction
        if mixed:
            c.append(Fraction(a + b, L) if a + b < L else Fraction(a + b - L, L))   # forgot the whole numbers
        c.append(W + Fraction(a + n2, L) if d2 != L else W + Fraction(n1 + b, L))   # changed only one fraction
        c.append(W + Fraction(n1 + n2, d1 * d2))                 # multiplied the denominators, kept the numerators
        c.append(W + Fraction(n1 * n2, d1 * d2))                 # multiplied numerators and denominators
    else:
        W = w1 - w2
        if a >= b:
            if d1 != d2 and n1 > n2 and d1 > d2:
                c.append(W + Fraction(n1 - n2, d1 - d2))         # subtracted numerators and denominators
            c.append(W + Fraction(abs(n1 - n2), L) if n1 != n2 else None)   # changed the denominator only
            c.append(W + Fraction(a - n2, L) if d2 != L else W + Fraction(n1 - b, L))   # changed only one fraction
            if mixed:
                c.append(Fraction(a - b, L))                     # forgot the whole numbers
            c.append(val(x) + val(y))                            # added instead
            if d1 != d2 and n1 != n2:
                c.append(W + Fraction(abs(n1 - n2), abs(d1 - d2)))   # took the smaller from the larger, top and bottom
            c.append(W + Fraction(abs(n1 - n2), d1 * d2) if n1 != n2 else None)
        else:
            c.append(W + Fraction(b - a, L))                     # took the smaller fraction from the larger (no regrouping)
            c.append(right + 1)                                  # renamed a whole but did not take 1 from the wholes
            c.append(Fraction(a + L - b, L))                     # forgot the whole numbers
            if W > 1:
                c.append(W - 1 + Fraction(b - a, L))
            if L != 10 and 10 + a - b > 0:
                c.append(W - 1 + Fraction(10 + a - b, L))        # renamed 1 whole as 10, like with whole numbers
            c.append(W + Fraction(abs(n1 - n2), L) if n1 != n2 else None)
            c.append(val(x) + val(y))
    return c


def P0(n, d):
    return (0, n, d)


def calc_q(x, y, op, prompt=SIMPLE):
    sym = "+" if op == "+" else "−"
    return "%s %s %s = ?" % (mx(*x), sym, mx(*y)) + prompt


def calc(x, y, op, rnd, prompt=SIMPLE, extra=None):
    r = val(x) + val(y) if op == "+" else val(x) - val(y)
    c = wrong(x, y, op)
    if extra:
        c = extra + c
    return mcq(calc_q(x, y, op, prompt), r, c, e_calc(x, y, op), rnd)


def pair(a, b, c, d):
    return "%s and %s" % (fr(a, b), fr(c, d))


def rename_choices(n1, d1, n2, d2, L):
    k1, k2 = L // d1, L // d2
    right = (n1 * k1, n2 * k2)
    cands = [(n1, n2),                                   # changed the denominator only
             (n1 * k2, n2 * k1),                         # multiplied by the wrong number
             (n1 + L - d1, n2 + L - d2),                 # added the same number to the top and bottom
             (n1 * k1, n2), (n1, n2 * k2)]               # changed only one fraction
    return pair(right[0], L, right[1], L), [pair(p, L, q, L) for p, q in cands if (p, q) != right]


def e_rename(n1, d1, n2, d2, L):
    parts = []
    for n, d in ((n1, d1), (n2, d2)):
        k = L // d
        if k == 1:
            parts.append("%s already has the denominator %d" % (fr(n, d), L))
        else:
            parts.append("%d × %d = %d, so multiply the numerator and denominator of %s by %d: %s"
                         % (d, k, L, fr(n, d), k, fr(n * k, L)))
    return ". ".join(parts) + ". The answer is <b>%s</b>." % pair(n1 * L // d1, L, n2 * L // d2, L)


def jump_item(n1, d1, n2, d2, op, Lw, rnd, prompt=SIMPLE):
    """Number line in steps of 1/L (L = lcm). Start at n1/d1 and jump forward or back n2/d2."""
    L = lcm(d1, d2)
    a, b = n1 * L // d1, n2 * L // d2
    x, y = P0(n1, d1), P0(n2, d2)
    r = val(x) + val(y) if op == "+" else val(x) - val(y)
    assert 0 < r <= Lw
    end = Fraction(a + b if op == "+" else a - b, L)
    assert end == r
    move = "jumps forward" if op == "+" else "jumps back"
    sym = "+" if op == "+" else "−"
    q = (fig(jump_line_svg(Lw, L, Fraction(n1, d1), end)) +
         "Each whole is split into %s. The dot is at %s. The arrow %s %s. Where does it land? (%s %s %s)"
         % (WORD[L], fr(n1, d1), move, fr(n2, d2), fr(n1, d1), sym, fr(n2, d2)) + prompt)
    e = ("Each small step is %s. %s = %s, so the dot is %d steps from 0. %s = %s, so the arrow %s %d steps. "
         % (fr(1, L), fr(n1, d1), fr(a, L), a, fr(n2, d2), fr(b, L), "jumps forward" if op == "+" else "jumps back", b))
    N = a + b if op == "+" else a - b
    e += "It lands on step %d: %s. " % (N, fr(N, L))
    s, v = finish(0, N, L)
    assert v == r
    w = wrong(x, y, op)
    if op == "+":
        cands = w[:1] + [Fraction(N - 1, L)] + w[1:]          # counted the starting tick as a step
    else:
        cands = [Fraction(N + 1, L)] + w[1:]                    # counted the starting tick as a step
    cands = [c for c in cands if c is None or c <= Lw]          # every choice is on the line
    return mcq(q, r, cands, e + s, rnd)




def wrong_like(n1, n2, d, op):
    """Wrong answers from real mistakes when the denominators are already the same."""
    c = []
    if op == "+":
        right = Fraction(n1 + n2, d)
        c.append(Fraction(n1 + n2, 2 * d))                       # added the denominators too
        if n1 + n2 > d:
            c.append(right - 1)                                  # lost the whole from the improper fraction
            c.append(Fraction(n1 + n2 - d, 2 * d) + 1)           # added denominators and kept a whole
        c.append(Fraction(n1 + n2 - 1, d))                       # counted one part too few
        c.append(Fraction(n1 * n2, d))                           # multiplied the numerators
        c.append(Fraction(n1 + n2 + 1, d))                       # counted one part too many
        c.append(Fraction(n1 + n2, d * d))                       # multiplied the denominators
    else:
        c.append(Fraction(n2, d))                                # gave the part taken away
        c.append(Fraction(n1 + n2, d))                           # added instead
        c.append(Fraction(n1 - n2, 2 * d))                       # added the denominators
        c.append(Fraction(n1 - n2 + 1, d))
        c.append(Fraction(n1 - n2 - 1, d) if n1 - n2 > 1 else None)
    return c


def e_like(n1, n2, d, op, units=None):
    if op == "+":
        t = ("The denominators are the same, so the parts are the same size. Add the numerators and keep the denominator: "
             "%d + %d = %d, so %s + %s = %s. " % (n1, n2, n1 + n2, fr(n1, d), fr(n2, d), fr(n1 + n2, d)))
        s, v = finish(0, n1 + n2, d, units)
        assert v == Fraction(n1 + n2, d)
    else:
        t = ("The denominators are the same, so the parts are the same size. Subtract the numerators and keep the denominator: "
             "%d − %d = %d, so %s − %s = %s. " % (n1, n2, n1 - n2, fr(n1, d), fr(n2, d), fr(n1 - n2, d)))
        s, v = finish(0, n1 - n2, d, units)
        assert v == Fraction(n1 - n2, d)
    return t + s


def like_q(n1, n2, d, op, rnd, prompt=SIMPLE, q=None, extra=None):
    sym = "+" if op == "+" else "−"
    r = Fraction(n1 + n2, d) if op == "+" else Fraction(n1 - n2, d)
    assert r > 0
    if q is None:
        q = "%s %s %s = ?" % (fr(n1, d), sym, fr(n2, d)) + prompt
    c = wrong_like(n1, n2, d, op)
    if extra:
        c = extra + c
    return mcq(q, r, c, e_like(n1, n2, d, op), rnd)


CM = (" cm", " cm", " cm")



def F(a, b=1):
    return Fraction(a, b)


# ============================================================ set 1: unlike denominators
def set_unlike(rnd, P):
    SPOTS.left = []
    its = []
    # A: lowest common denominator
    for n1, d1, n2, d2 in [(3, 8, 5, 12), (2, 9, 5, 6)]:
        L = lcm(d1, d2)
        big, small = max(d1, d2), min(d1, d2)
        mb = ", ".join(str(big * i) for i in range(1, L // big + 1))
        ms = ", ".join(str(small * i) for i in range(1, L // small + 1))
        e = ("Multiples of %d: %s. Multiples of %d: %s. The first number in both lists is <b>%d</b>."
             % (big, mb, small, ms, L))
        if d1 * d2 != L:
            e += " %d × %d = %d also works, but it is not the lowest." % (d1, d2, d1 * d2)
        e += " Adding the denominators (%d + %d = %d) does not give a common denominator." % (d1, d2, d1 + d2)
        cands = [d1 * d2 if d1 * d2 != L else None, d1 + d2, big, 2 * L]
        its.append(mcq("What is the lowest common denominator of %s and %s?" % (fr(n1, d1), fr(n2, d2)),
                       str(L), [str(v) for v in cands if v], e, rnd))
    # B: fraction bars
    n1, d1, n2, d2, L = 5, 6, 1, 4, 12
    q = (fig(two_bars_svg(d1, n1, d2, n2, L)) +
         "The green part is %s and the yellow part is %s. The dashed lines split both bars into %s. "
         "Which shows both fractions in %s?" % (fr(n1, d1), fr(n2, d2), WORD[L], WORD[L]))
    r, c = rename_choices(n1, d1, n2, d2, L)
    e = "Count the small parts in each shaded piece. " + e_rename(n1, d1, n2, d2, L)
    its.append(mcq(q, r, c, e, rnd))
    # C: number line
    its.append(jump_item(5, 6, 1, 4, "-", 1, rnd))
    # D: spot the mistake (adding the denominators)
    n, he, his = P.next()
    assert F(3, 4) + F(1, 6) == F(11, 12) and F(4, 10) < F(3, 4)
    e = ("Fourths and sixths are different sizes, so you cannot add the numerators and the denominators. "
         "Use twelfths: %s + %s = %s. Also, %s is less than %s, so it cannot be the total."
         % (fr(9, 12), fr(2, 12), fr(11, 12), fr(4, 10), fr(3, 4)))
    its.append(mcq("%s wrote %s + %s = %s. What mistake did %s make?" % (n, fr(3, 4), fr(1, 6), fr(4, 10), he),
                   "%s added the numerators and the denominators" % cap(he),
                   ["%s forgot to simplify" % cap(he), "%s should have multiplied" % cap(he), "There is no mistake"], e, rnd))
    n, he, his = P.next()
    assert F(5, 6) - F(1, 2) == F(1, 3)
    e = ("%s subtracted the numerators (5 − 1 = 4) and the denominators (6 − 2 = 4). That gives 1, but taking something away "
         "from %s cannot give more than %s. Use sixths: %s − %s = %s = <b>%s</b>."
         % (cap(he), fr(5, 6), fr(5, 6), fr(5, 6), fr(3, 6), fr(2, 6), fr(1, 3)))
    its.append(mcq("%s wrote %s − %s = %s = 1. What is the correct answer?" % (n, fr(5, 6), fr(1, 2), fr(4, 4)) + SIMPLE,
                   F(1, 3), [F(2, 3), F(1), F(4, 3)], e, rnd))
    # E: add, answer less than 1
    for n1, d1, n2, d2 in [(1, 4, 3, 10), (2, 9, 5, 12), (1, 6, 4, 15), (3, 8, 1, 6)]:
        x, y = P0(n1, d1), P0(n2, d2)
        assert val(x) + val(y) < 1 and lcm(d1, d2) != max(d1, d2)
        its.append(calc(x, y, "+", rnd))
    # F: add, answer greater than 1
    for n1, d1, n2, d2 in [(3, 4, 5, 6), (7, 10, 3, 4), (4, 9, 5, 6)]:
        x, y = P0(n1, d1), P0(n2, d2)
        assert val(x) + val(y) > 1 and lcm(d1, d2) != max(d1, d2)
        its.append(calc(x, y, "+", rnd, prompt=MIXED))
    # G: subtract
    for n1, d1, n2, d2 in [(7, 9, 1, 6), (9, 10, 2, 3), (3, 4, 2, 7), (11, 12, 3, 8)]:
        x, y = P0(n1, d1), P0(n2, d2)
        assert val(x) - val(y) > 0 and lcm(d1, d2) != max(d1, d2)
        its.append(calc(x, y, "-", rnd))
    # H: missing number
    assert F(5, 6) - F(3, 8) == F(11, 24)
    e = ("Find the missing part by subtracting: %s − %s. Use twenty-fourths: %s − %s = <b>%s</b>. "
         "Check: %s + %s = %s = %s." % (fr(5, 6), fr(3, 8), fr(20, 24), fr(9, 24), fr(11, 24),
                                       fr(11, 24), fr(9, 24), fr(20, 24), fr(5, 6)))
    its.append(mcq("? + %s = %s" % (fr(3, 8), fr(5, 6)) + SIMPLE, F(11, 24),
                   [F(5, 6) + F(3, 8), F(2, 24), F(2, 6)], e, rnd))
    # I: three fractions
    assert F(2, 3) + F(1, 4) - F(1, 6) == F(3, 4)
    e = ("The lowest common denominator of 3, 4 and 6 is 12. %s + %s − %s = %s, because 8 + 3 − 2 = 9. "
         "Simplify: divide by 3. The answer is <b>%s</b>." % (fr(8, 12), fr(3, 12), fr(2, 12), fr(9, 12), fr(3, 4)))
    its.append(mcq("%s + %s − %s = ?" % (fr(2, 3), fr(1, 4), fr(1, 6)) + SIMPLE, F(3, 4),
                   [F(9, 36), F(2, 12), F(2, 3) + F(1, 4) + F(1, 6)], e, rnd))
    assert F(1, 2) + F(2, 5) + F(3, 10) == F(6, 5)
    e = ("The lowest common denominator of 2, 5 and 10 is 10. %s + %s + %s = %s. %s = 1 %s = <b>1 %s</b>."
         % (fr(5, 10), fr(4, 10), fr(3, 10), fr(12, 10), fr(12, 10), fr(2, 10), fr(1, 5)))
    its.append(mcq("%s + %s + %s = ?" % (fr(1, 2), fr(2, 5), fr(3, 10)) + MIXED, F(6, 5),
                   [F(6, 17), F(6, 10), F(12, 30)], e, rnd))
    assert len(its) == 20, len(its)
    return {"title": "Unlike denominators", "items": its}


# ============================================================ set 2: mixed numbers
def set_mixed(rnd, P):
    SPOTS.left = []
    its = []
    add_easy = [((2, 1, 6), (3, 3, 8)), ((5, 2, 9), (1, 1, 6))]
    add_carry = [((3, 5, 8), (1, 2, 3)), ((2, 4, 5), (4, 1, 2)), ((1, 7, 12), (2, 5, 8)), ((4, 5, 6), (3, 4, 9)),
                 ((6, 3, 4), (2, 9, 10)), ((2, 2, 3), (5, 5, 7))]
    sub_easy = [((6, 7, 9), (2, 1, 6)), ((7, 5, 8), (4, 1, 6))]
    sub_ex = [((5, 1, 4), (2, 5, 6)), ((8, 1, 3), (3, 7, 10)), ((6, 1, 6), (4, 4, 9)), ((9, 2, 5), (3, 3, 4)),
              ((4, 3, 10), (1, 5, 6)), ((7, 1, 8), (2, 5, 12)), ((10, 1, 2), (6, 7, 9))]
    for grp, op in ((add_easy, "+"), (add_carry, "+"), (sub_easy, "-"), (sub_ex, "-")):
        for x, y in grp:
            L = lcm(x[2], y[2])
            a, b = x[1] * L // x[2], y[1] * L // y[2]
            if grp is add_carry:
                assert a + b >= L
            if grp is add_easy:
                assert a + b < L
            if grp is sub_easy:
                assert a >= b
            if grp is sub_ex:
                assert a < b
            its.append(calc(x, y, op, rnd))
    # the regrouping step
    n, he, his = P.next()
    assert 5 + F(16, 12) == 6 + F(4, 12) and 6 + F(1, 3) - (3 + F(3, 4)) == 2 + F(7, 12)
    e = ("%s is less than %s, so take 1 whole from the 6 and rename it as %s. 6 %s = 5 + %s + %s = <b>5 %s</b>. "
         "Then 5 %s − 3 %s = 2 %s."
         % (fr(4, 12), fr(9, 12), fr(12, 12), fr(4, 12), fr(12, 12), fr(4, 12), fr(16, 12), fr(16, 12), fr(9, 12), fr(7, 12)))
    its.append(mcq("To work out 6 %s − 3 %s, %s first writes 6 %s − 3 %s. What should %s write next?"
                   % (fr(1, 3), fr(3, 4), n, fr(4, 12), fr(9, 12), he),
                   "5 %s − 3 %s" % (fr(16, 12), fr(9, 12)),
                   ["6 %s − 3 %s" % (fr(16, 12), fr(9, 12)), "5 %s − 3 %s" % (fr(14, 12), fr(9, 12)),
                    "6 %s − 3 %s" % (fr(9, 12), fr(4, 12))], e, rnd))
    # spot the mistake: no regrouping
    n, he, his = P.next()
    assert 5 + F(1, 6) - (2 + F(3, 4)) == 2 + F(5, 12)
    e = ("5 %s − 2 %s = 5 %s − 2 %s. %s took %s from %s instead of regrouping. "
         "Regroup: 5 %s = 4 %s. Then 4 %s − 2 %s = <b>2 %s</b>."
         % (fr(1, 6), fr(3, 4), fr(2, 12), fr(9, 12), cap(he), fr(2, 12), fr(9, 12), fr(2, 12), fr(14, 12),
            fr(14, 12), fr(9, 12), fr(5, 12)))
    its.append(mcq("%s wrote 5 %s − 2 %s = 3 %s. What mistake did %s make?" % (n, fr(1, 6), fr(3, 4), fr(7, 12), he),
                   "%s did not regroup" % cap(he),
                   ["%s did not use a common denominator" % cap(he), "%s should have added" % cap(he), "There is no mistake"], e, rnd))
    # a whole number minus a mixed number
    assert 5 - (1 + F(4, 9)) == 3 + F(5, 9)
    e = ("There is no fraction to take %s from, so regroup: rename 1 whole as %s. 5 = 4 %s. "
         "Subtract the fractions: %s − %s = %s. Subtract the whole numbers: 4 − 1 = 3. The answer is <b>3 %s</b>."
         % (fr(4, 9), fr(9, 9), fr(9, 9), fr(9, 9), fr(4, 9), fr(5, 9), fr(5, 9)))
    its.append(mcq("5 − 1 %s = ?" % fr(4, 9) + SIMPLE, 3 + F(5, 9),
                   [4 + F(4, 9), 4 + F(5, 9), 3 + F(4, 9)], e, rnd))
    assert len(its) == 20, len(its)
    return {"title": "Mixed numbers", "items": its}


# ============================================================ set 3: simplest form
def set_simplest(rnd, P):
    SPOTS.left = []
    its = []
    # A: greatest common factor
    for a, b, bad in [(24, 36, ["6", "4", "72"]), (30, 45, ["5", "3", "90"])]:
        g = math.gcd(a, b)
        fa = [k for k in range(1, a + 1) if a % k == 0]
        fb = [k for k in range(1, b + 1) if b % k == 0]
        e = ("Factors of %d: %s. Factors of %d: %s. The greatest factor in both lists is <b>%d</b>. "
             "Dividing by the GCF simplifies %s in one step: %s."
             % (a, ", ".join(map(str, fa)), b, ", ".join(map(str, fb)), g, fr(a, b), fr(a // g, b // g)))
        assert str(g) not in bad and all(a % int(x) == 0 or b % int(x) == 0 or int(x) % a == 0 for x in bad)
        its.append(mcq("To write %s in simplest form, divide by the greatest common factor (GCF). What is the GCF of %d and %d?"
                       % (fr(a, b), a, b), str(g), bad, e, rnd))
    # B: simplify a fraction
    for a, b in [(28, 42), (45, 60)]:
        g = math.gcd(a, b)
        e = ("Divide the numerator and the denominator by the same number. The GCF of %d and %d is %d. "
             "%d ÷ %d = %d and %d ÷ %d = %d. The answer is <b>%s</b>." % (
                 a, b, g, a, g, a // g, b, g, b // g, fr(a // g, b // g)))
        cands = [fr(a // g, b),         # divided only the numerator
                 fr(a, b // g),         # divided only the denominator
                 fr(b // g, a // g)]    # turned the fraction upside down
        assert F(a // g, b) != F(a, b) and F(a, b // g) != F(a, b) and F(b, a) != F(a, b)
        its.append(mcq("Write %s in simplest form." % fr(a, b), fr(a // g, b // g), cands, e, rnd))
    # C: which is in simplest form
    opts = [(10, 21), (14, 35), (9, 24), (16, 36)]
    assert math.gcd(10, 21) == 1 and all(math.gcd(p, q) > 1 for p, q in opts[1:])
    assert len({F(p, q) for p, q in opts}) == 4
    e = ("10 = 2 × 5 and 21 = 3 × 7 have no common factor other than 1, so <b>%s</b> is in simplest form. "
         "The others can be simplified: %s = %s, %s = %s and %s = %s."
         % (fr(10, 21), fr(14, 35), fr(2, 5), fr(9, 24), fr(3, 8), fr(16, 36), fr(4, 9)))
    its.append(mcq("Which fraction is already in simplest form?", fr(10, 21), [fr(p, q) for p, q in opts[1:]], e, rnd))
    # D: is it finished?
    n, he, his = P.next()
    assert F(18, 30) == F(3, 5)
    e = ("6 and 10 still have a common factor, 2. %s ÷ 2 = %s. The GCF of 18 and 30 is 6, so dividing by 6 gives "
         "<b>%s</b> in one step." % (fr(6, 10), fr(3, 5), fr(3, 5)))
    its.append(mcq("%s simplified %s to %s. Is %s answer in simplest form?" % (n, fr(18, 30), fr(6, 10), his),
                   "No. Divide by 2 again to get %s" % fr(3, 5),
                   ["Yes, %s is in simplest form" % fr(6, 10), "No. It should be %s" % fr(1, 2),
                    "Yes, because %s has a smaller denominator than %s" % (fr(6, 10), fr(18, 30))], e, rnd))
    # E: add or subtract, then simplify
    for n1, d1, n2, d2, op in [(7, 12, 1, 4, "+"), (2, 15, 1, 6, "+"), (3, 8, 5, 24, "+"), (13, 18, 2, 9, "-"),
                               (7, 10, 1, 6, "-"), (19, 20, 7, 10, "-")]:
        x, y = P0(n1, d1), P0(n2, d2)
        L = lcm(d1, d2)
        N = n1 * L // d1 + (n2 * L // d2 if op == "+" else -(n2 * L // d2))
        assert math.gcd(N, L) > 1 and 0 < N < L
        its.append(calc(x, y, op, rnd))
    assert F(5, 14) + F(3, 14) == F(4, 7)
    its.append(like_q(5, 3, 14, "+", rnd))
    assert F(3, 4) - F(5, 12) == F(1, 3)
    its.append(calc(P0(3, 4), P0(5, 12), "-", rnd))
    # F: improper results
    for n1, d1, n2, d2 in [(7, 8, 5, 24), (9, 10, 3, 5)]:
        x, y = P0(n1, d1), P0(n2, d2)
        L = lcm(d1, d2)
        N = n1 * L // d1 + n2 * L // d2
        assert N > L and math.gcd(N - L, L) > 1
        its.append(calc(x, y, "+", rnd, prompt=MIXED))
    # G: mixed numbers that need simplifying
    x, y = (3, 1, 6), (1, 7, 12)
    assert val(x) + val(y) == 4 + F(3, 4)
    its.append(calc(x, y, "+", rnd))
    x, y = (5, 5, 6), (2, 1, 3)
    assert val(x) - val(y) == 3 + F(1, 2)
    its.append(calc(x, y, "-", rnd))
    # H: improper fraction to a mixed number
    assert F(50, 12) == 4 + F(1, 6)
    e = ("50 ÷ 12 = 4 remainder 2, so %s = 4 %s. Simplify %s: the GCF of 2 and 12 is 2, so %s = %s. "
         "The answer is <b>4 %s</b>." % (fr(50, 12), fr(2, 12), fr(2, 12), fr(2, 12), fr(1, 6), fr(1, 6)))
    its.append(mcq("Write %s as a mixed number in simplest form." % fr(50, 12), 4 + F(1, 6),
                   [4 + F(1, 2), 2 + F(1, 3), 5 + F(1, 6)], e, rnd))
    # I: three fractions
    assert F(1, 3) + F(1, 4) + F(1, 12) == F(2, 3)
    e = ("Use twelfths: %s + %s + %s = %s. The GCF of 8 and 12 is 4, so %s = <b>%s</b>."
         % (fr(4, 12), fr(3, 12), fr(1, 12), fr(8, 12), fr(8, 12), fr(2, 3)))
    its.append(mcq("%s + %s + %s = ?" % (fr(1, 3), fr(1, 4), fr(1, 12)) + SIMPLE, F(2, 3),
                   [F(3, 19), F(3, 12), F(8, 36)], e, rnd))
    assert len(its) == 20, len(its)
    return {"title": "Simplest form", "items": its}


# ============================================================ set 4: order of operations with + and −
def st(x, op, y):
    """One step x op y with a common denominator. Returns (text, result)."""
    L = lcm(x.denominator, y.denominator)
    a, b = x * L, y * L
    assert a.denominator == 1 and b.denominator == 1
    a, b = a.numerator, b.numerator
    N = a + b if op == "+" else a - b
    r = x + y if op == "+" else x - y
    assert r > 0 and F(N, L) == r
    sym = "+" if op == "+" else "−"
    if x.denominator == L and y.denominator == L and x < 1 and y < 1:
        t = "%s %s %s = %s" % (show(x), sym, show(y), fr(N, L))
    else:
        t = "%s %s %s = %s %s %s = %s" % (show(x), sym, show(y), fr(a, L), sym, fr(b, L), fr(N, L))
    if show(r) != fr(N, L):
        t += " = %s" % show(r)
    return t, r


def chain(start, steps):
    """Left to right: start, then [(op, value), ...]. Returns (list of step texts, result)."""
    v, out = start, []
    for op, y in steps:
        t, v = st(v, op, y)
        out.append(t)
    return out, v


def set_order(rnd, P):
    SPOTS.left = []
    its = []
    LR = "+ and − have the same rank, so work from left to right. "

    def flat(start, steps, wrongs, prompt=SIMPLE):
        txt = [show(start)]
        for op, y in steps:
            txt += ["+" if op == "+" else "−", show(y)]
        q = " ".join(txt) + " = ?" + prompt
        ts, r = chain(start, steps)
        e = LR + "First: " + ts[0] + ". " + " ".join("Then: %s." % t for t in ts[1:]) + " The answer is <b>%s</b>." % show(r)
        its.append(mcq(q, r, wrongs, e, rnd))
        return r

    # A: left to right
    r = flat(F(9, 10), [("-", F(1, 2)), ("+", F(1, 5))], [F(1, 5), F(9, 17), F(9, 10)])
    assert r == F(3, 5) and F(9, 10) - (F(1, 2) + F(1, 5)) == F(1, 5)
    r = flat(F(3, 4), [("-", F(1, 6)), ("+", F(1, 3))], [F(3, 4) - (F(1, 6) + F(1, 3)), F(3, 13), F(3, 4) + F(1, 6) + F(1, 3)])
    assert r == F(11, 12)
    r = flat(F(7, 8), [("-", F(1, 2)), ("-", F(1, 4))], [F(7, 8) - (F(1, 2) - F(1, 4)), F(7, 8) + F(1, 2) + F(1, 4), F(5, 14)])
    assert r == F(1, 8)
    r = flat(F(2), [("-", F(2, 3)), ("-", F(1, 4))], [2 - (F(2, 3) - F(1, 4)), 2 + F(2, 3) + F(1, 4), F(1, 12)])
    assert r == 1 + F(1, 12)
    r = flat(F(3, 2), [("-", F(3, 4)), ("+", F(1, 6))], [F(3, 2) - (F(3, 4) + F(1, 6)), F(3, 2) + F(3, 4) + F(1, 6),
                                                       1 + F(1, 4) + F(1, 6)])
    assert r == F(11, 12)
    r = flat(3 + F(1, 3), [("-", F(3, 2)), ("+", F(3, 4))], [F(10, 3) - (F(3, 2) + F(3, 4)), F(10, 3) + F(3, 2) + F(3, 4),
                                                           2 + F(1, 6) + F(3, 4)])
    assert r == 2 + F(7, 12)
    r = flat(4 + F(1, 4), [("-", 1 + F(5, 6)), ("-", F(2, 3))], [F(17, 4) - (F(11, 6) - F(2, 3)), F(17, 4) + F(11, 6) + F(2, 3),
                                                               3 + F(7, 12) - F(2, 3)])
    assert r == 1 + F(3, 4)
    r = flat(F(5, 6), [("+", F(1, 4)), ("-", F(2, 3)), ("-", F(1, 12))],
             [(F(5, 6) + F(1, 4)) - (F(2, 3) - F(1, 12)), F(5, 6) + F(1, 4) + F(2, 3) + F(1, 12), F(3, 25)])
    assert r == F(1, 3)

    # B: brackets first
    def br(q, inner, outer, wrongs, extra_e=""):
        """inner: (x, op, y) inside the brackets. outer: function(bracket value) -> list of (start, op, y) steps text."""
        t1, b = st(*inner)
        rest = outer(b)
        ts, r = [], None
        for x, op, y in rest:
            t, r = st(x, op, y)
            ts.append(t)
        e = "Brackets first: %s. " % t1 + " ".join("Then: %s." % t for t in ts) + " The answer is <b>%s</b>." % show(r) + extra_e
        its.append(mcq(q + SIMPLE, r, wrongs, e, rnd))
        return r

    r = br("%s − (%s + %s) = ?" % (fr(5, 6), fr(1, 3), fr(1, 4)), (F(1, 3), "+", F(1, 4)),
           lambda b: [(F(5, 6), "-", b)], [F(5, 6) - F(1, 3) + F(1, 4), F(5, 6) - F(2, 7), F(5, 6) + F(1, 3) + F(1, 4)])
    assert r == F(1, 4)
    r = br("1 %s − (%s − %s) = ?" % (fr(1, 2), fr(3, 4), fr(1, 3)), (F(3, 4), "-", F(1, 3)),
           lambda b: [(F(3, 2), "-", b)], [F(3, 2) - F(3, 4) - F(1, 3), F(3, 2) + F(5, 12), F(3, 2) - F(2, 12)])
    assert r == 1 + F(1, 12)
    # two brackets
    t1, b1 = st(F(2, 3), "+", F(1, 4))
    t2, b2 = st(F(1, 2), "-", F(1, 6))
    t3, r = st(b1, "-", b2)
    assert r == F(7, 12)
    e = "Work out each bracket first: %s and %s. Then: %s. The answer is <b>%s</b>." % (t1, t2, t3, show(r))
    its.append(mcq("(%s + %s) − (%s − %s) = ?" % (fr(2, 3), fr(1, 4), fr(1, 2), fr(1, 6)) + SIMPLE, r,
                   [F(2, 3) + F(1, 4) - F(1, 2) - F(1, 6), F(2, 3) + F(1, 4) + F(1, 2) + F(1, 6), F(3, 7) - F(1, 3)], e, rnd))
    r = br("2 − (%s + %s) = ?" % (fr(1, 2), fr(3, 8)), (F(1, 2), "+", F(3, 8)),
           lambda b: [(F(2), "-", b)], [2 - F(1, 2) + F(3, 8), 2 - F(4, 10), F(1, 8)])
    assert r == 1 + F(1, 8)
    r = br("1 %s − (%s + %s) = ?" % (fr(3, 4), fr(2, 3), fr(5, 6)), (F(2, 3), "+", F(5, 6)),
           lambda b: [(F(7, 4), "-", b)], [F(7, 4) - F(2, 3) + F(5, 6), F(7, 4) + F(2, 3) + F(5, 6), F(7, 4) - F(7, 9)])
    assert r == F(1, 4)
    r = br("3 − (1 %s − %s) = ?" % (fr(1, 4), fr(5, 6)), (F(5, 4), "-", F(5, 6)),
           lambda b: [(F(3), "-", b)], [3 - F(5, 4) - F(5, 6), 3 + F(5, 12), 3 - (1 + F(7, 12))])
    assert r == 2 + F(7, 12)
    r = br("4 %s − (1 %s + 1 %s) = ?" % (fr(1, 2), fr(2, 3), fr(1, 4)), (F(5, 3), "+", F(5, 4)),
           lambda b: [(F(9, 2), "-", b)], [F(9, 2) - F(5, 3) + F(5, 4), F(9, 2) + F(5, 3) + F(5, 4), F(9, 2) - (2 + F(3, 7))])
    assert r == 1 + F(7, 12)
    # nested brackets
    t1, b1 = st(F(1, 2), "-", F(1, 3))
    t2, b2 = st(F(3, 4), "-", b1)
    t3, r = st(F(2), "-", b2)
    assert r == 1 + F(5, 12)
    e = ("Start with the inner brackets: %s. Then the square brackets: %s. Last: %s. The answer is <b>%s</b>."
         % (t1, t2, t3, show(r)))
    its.append(mcq("2 − [%s − (%s − %s)] = ?" % (fr(3, 4), fr(1, 2), fr(1, 3)) + SIMPLE, r,
                   [2 - F(3, 4) - F(1, 2) - F(1, 3), 2 + F(7, 12), 2 - F(3, 4) - F(1, 6)], e, rnd))
    # one more: brackets in the middle
    t1, b1 = st(F(1, 2), "-", F(1, 8))
    t2, b2 = st(F(1), "-", b1)
    t3, r = st(b2, "+", F(1, 4))
    assert r == F(7, 8)
    e = "Brackets first: %s. Then work from left to right: %s. Then: %s. The answer is <b>%s</b>." % (t1, t2, t3, show(r))
    its.append(mcq("1 − (%s − %s) + %s = ?" % (fr(1, 2), fr(1, 8), fr(1, 4)) + SIMPLE, r,
                   [1 - F(1, 2) - F(1, 8) + F(1, 4), 1 - (F(3, 8) + F(1, 4)), 1 + F(1, 4)], e, rnd))

    # C: reasoning
    assert 1 + F(1, 4) - F(2, 3) == F(7, 12) and F(7, 12) + F(2, 3) - F(1, 4) == 1
    e = ("Work backward. Undo “− %s” by adding %s, then undo “+ %s” by subtracting %s: 1 + %s − %s = %s + %s − %s = <b>%s</b>. "
         "Check: %s + %s − %s = %s + %s − %s = %s = 1."
         % (fr(1, 4), fr(1, 4), fr(2, 3), fr(2, 3), fr(1, 4), fr(2, 3), fr(12, 12), fr(3, 12), fr(8, 12), fr(7, 12),
            fr(7, 12), fr(2, 3), fr(1, 4), fr(7, 12), fr(8, 12), fr(3, 12), fr(12, 12)))
    its.append(mcq("? + %s − %s = 1" % (fr(2, 3), fr(1, 4)) + SIMPLE, F(7, 12),
                   [1 - F(2, 3) - F(1, 4), 1 + F(2, 3) - F(1, 4), F(2, 3) - F(1, 4)], e, rnd))
    a, b, c = F(5, 6), F(1, 2), F(1, 3)
    assert a - (b + c) == 0 and (a - b) + c == F(2, 3) and a - b + c == F(2, 3)
    e = ("Brackets around %s + %s make you add them first: %s + %s = %s. Then %s − %s = 0. "
         "Without these brackets, work from left to right: %s − %s = %s, then %s + %s = %s."
         % (fr(1, 2), fr(1, 3), fr(3, 6), fr(2, 6), fr(5, 6), fr(5, 6), fr(5, 6), fr(5, 6), fr(1, 2), fr(1, 3),
            fr(1, 3), fr(1, 3), fr(2, 3)))
    its.append(mcq("Where do the brackets go so that %s − %s + %s = 0?" % (fr(5, 6), fr(1, 2), fr(1, 3)),
                   "%s − (%s + %s)" % (fr(5, 6), fr(1, 2), fr(1, 3)),
                   ["(%s − %s) + %s" % (fr(5, 6), fr(1, 2), fr(1, 3)), "(%s − %s + %s)" % (fr(5, 6), fr(1, 2), fr(1, 3)),
                    "No brackets are needed"], e, rnd))
    n, he, his = P.next()
    assert F(3, 4) - (F(1, 4) + F(1, 2)) == 0 and F(3, 4) - F(1, 4) + F(1, 2) == 1
    e = ("%s worked out %s + %s = %s first, then %s − %s = 0. That is working from right to left. "
         "Work from left to right: %s − %s = %s, then %s + %s = <b>1</b>."
         % (n, fr(1, 4), fr(1, 2), fr(3, 4), fr(3, 4), fr(3, 4), fr(3, 4), fr(1, 4), fr(1, 2), fr(1, 2), fr(1, 2)))
    its.append(mcq("%s says %s − %s + %s = 0. What did %s do wrong?" % (n, fr(3, 4), fr(1, 4), fr(1, 2), he),
                   "%s added before subtracting" % cap(he),
                   ["%s added the denominators" % cap(he), "%s forgot to simplify" % cap(he), "Nothing. The answer is correct"],
                   e, rnd))
    assert len(its) == 20, len(its)
    return {"title": "Order of operations with + and −", "items": its}


# ============================================================ set 5: word problems
def set_words(rnd, P):
    SPOTS.left = []
    its = []

    def word(q, x, y, op, units, extra=None, pre="", post=""):
        r = val(x) + val(y) if op == "+" else val(x) - val(y)
        c = wrong(x, y, op)
        if extra:
            c = extra + c
        its.append(mcq(q + SIMPLE, r, c, pre + e_calc(x, y, op, units) + post, rnd, units))
        return r

    def amt(x, units):
        return mx(*x) + unit_for(val(x), units)

    # 1 blueberries
    n, he, his = P.next()
    word("%s’s family picks blueberries at a farm in the Fraser Valley. They pick %s on Saturday and %s on Sunday. "
         "How many kilograms do they pick altogether?" % (n, amt((2, 1, 2), KG), amt((1, 3, 4), KG)),
         (2, 1, 2), (1, 3, 4), "+", KG)
    # 2 hiking trail
    n, he, his = P.next()
    word("A hiking trail on Vancouver Island is %s long. %s has hiked %s so far. How much farther does %s have to hike?"
         % (amt((4, 1, 3), KM), n, amt((2, 3, 4), KM), he), (4, 1, 3), (2, 3, 4), "-", KM)
    # 3 pizza
    (n1, _, _), (n2, _, _) = P.next(), P.next()
    assert 1 - F(1, 4) - F(2, 5) == F(7, 20)
    e = ("First add what they eat. Use twentieths: %s + %s = %s. The whole pizza is %s. Left: %s − %s = <b>%s</b>."
         % (fr(5, 20), fr(8, 20), fr(13, 20), fr(20, 20), fr(20, 20), fr(13, 20), fr(7, 20)))
    its.append(mcq("%s eats %s of a pizza and %s eats %s of it. What fraction of the pizza is left?" % (n1, fr(1, 4), n2, fr(2, 5))
                   + SIMPLE, F(7, 20), [F(13, 20), F(3, 9), F(6, 9)], e, rnd))
    # 4 class survey
    assert 1 - F(1, 3) - F(3, 8) == F(7, 24)
    e = ("Add the two groups. Use twenty-fourths: %s + %s = %s. The whole class is %s. Basketball: %s − %s = <b>%s</b>."
         % (fr(8, 24), fr(9, 24), fr(17, 24), fr(24, 24), fr(24, 24), fr(17, 24), fr(7, 24)))
    its.append(mcq("In a Grade 8 class in Surrey, each student chose one favourite sport. %s chose hockey and %s chose lacrosse. "
                   "The rest chose basketball. What fraction of the class chose basketball?" % (fr(1, 3), fr(3, 8)) + SIMPLE,
                   F(7, 24), [F(17, 24), F(7, 11), F(4, 11)], e, rnd))
    # 5 volunteering
    n, he, his = P.next()
    word("%s volunteers at the Terry Fox Run in Port Coquitlam. %s helps set up for %s and hands out water for %s. "
         "How many hours is that altogether?" % (n, cap(he), amt((1, 1, 4), HOUR), amt((2, 2, 3), HOUR)),
         (1, 1, 4), (2, 2, 3), "+", HOUR, post=" (That is 3 hours 55 minutes.)")
    # 6 cedar plank
    n, he, his = P.next()
    assert 4 - (1 + F(5, 6)) == 2 + F(1, 6)
    e = ("Regroup: 4 = 3 %s. Subtract the fractions: %s − %s = %s. Subtract the whole numbers: 3 − 1 = 2. "
         "The answer is <b>2 %s m</b>." % (fr(6, 6), fr(6, 6), fr(5, 6), fr(1, 6), fr(1, 6)))
    its.append(mcq("%s cuts a piece %s long from a 4 m cedar plank to build a bench. How long is the plank that is left?"
                   % (n, amt((1, 5, 6), M)) + SIMPLE, 2 + F(1, 6),
                   [3 + F(5, 6), 3 + F(1, 6), 2 + F(5, 6)], e, rnd, M))
    # 7 run
    (n1, _, _), (n2, _, _) = P.next(), P.next()
    word("On a training run in Stanley Park, %s runs %s and %s runs %s. How much farther does %s run than %s?"
         % (n1, amt((3, 2, 3), KM), n2, amt((2, 3, 4), KM), n1, n2), (3, 2, 3), (2, 3, 4), "-", KM,
         pre="“How much farther” means subtract. ")
    # 8 rainfall
    word("In Vancouver, it rains %s on Monday and %s on Tuesday. What is the total rainfall for the two days?"
         % (amt((1, 1, 5), CM), amt((0, 3, 4), CM)), (1, 1, 5), (0, 3, 4), "+", CM)
    # 9 blueberry muffins
    n, he, his = P.next()
    word("A blueberry muffin recipe needs %s of blueberries. %s has %s. How much more does %s need?"
         % (amt(P0(3, 4), CUP), n, amt(P0(1, 3), CUP), he), P0(3, 4), P0(1, 3), "-", CUP)
    # 10 stain
    n, he, his = P.next()
    assert 4 - (1 + F(3, 4)) - (1 + F(1, 3)) == F(11, 12)
    e = ("First add what is used. Use twelfths: 1 %s + 1 %s = 2 %s = 3 %s L. "
         "Then 4 − 3 %s: regroup, 4 = 3 %s. 3 %s − 3 %s = <b>%s L</b>."
         % (fr(9, 12), fr(4, 12), fr(13, 12), fr(1, 12), fr(1, 12), fr(12, 12), fr(12, 12), fr(1, 12), fr(11, 12)))
    its.append(mcq("A can holds 4 L of wood stain. %s uses %s on a deck and %s on a fence. How much stain is left?"
                   % (n, amt((1, 3, 4), LITRE), amt((1, 1, 3), LITRE)) + SIMPLE, F(11, 12),
                   [3 + F(1, 12), 1 + F(11, 12), F(1, 12)], e, rnd, LITRE))
    # 11 fresh snow
    word("At Whistler, %s of fresh snow falls on Friday night and %s falls on Saturday night. How much fresh snow is that altogether?"
         % (amt((12, 1, 2), CM), amt((8, 2, 3), CM)), (12, 1, 2), (8, 2, 3), "+", CM)
    # 12 kayak trip
    word("A kayak trip in the Gulf Islands is %s long. The group has paddled %s. How far do they still have to paddle?"
         % (amt((8, 1, 3), KM), amt((5, 3, 4), KM)), (8, 1, 3), (5, 3, 4), "-", KM)
    # 13 practice time
    n, he, his = P.next()
    assert F(3, 4) + F(2, 3) + F(1, 3) == 1 + F(3, 4)
    e = ("Use twelfths: %s + %s + %s = %s. %s = 1 %s = <b>1 %s hours</b>. (That is 1 hour 45 minutes.)"
         % (fr(9, 12), fr(8, 12), fr(4, 12), fr(21, 12), fr(21, 12), fr(9, 12), fr(3, 4)))
    its.append(mcq("%s practises piano for %s of an hour, does math homework for %s of an hour and reads for %s of an hour. "
                   "How long is that altogether?" % (n, fr(3, 4), fr(2, 3), fr(1, 3)) + SIMPLE, 1 + F(3, 4),
                   [F(6, 10), F(3, 4), 2 + F(1, 4)], e, rnd, HOUR))
    # 14 spot the mistake: adding the denominators
    n, he, his = P.next()
    assert F(1, 3) + F(2, 5) == F(11, 15) and F(3, 8) < F(2, 5)
    e = ("%s added the numerators and the denominators. Use fifteenths: %s + %s = %s. "
         "Also, %s is less than %s, so it cannot be the total. The answer is <b>%s</b>."
         % (n, fr(5, 15), fr(6, 15), fr(11, 15), fr(3, 8), fr(2, 5), fr(11, 15)))
    its.append(mcq("%s reads %s of a novel on the weekend and %s of it on Monday. %s says %s has read %s of the novel. Which is true?"
                   % (n, fr(1, 3), fr(2, 5), cap(he), he, fr(3, 8)),
                   "%s is wrong. It is %s" % (cap(he), fr(11, 15)),
                   ["%s is right" % cap(he), "%s is wrong. It is %s" % (cap(he), fr(3, 15)),
                    "%s is wrong. It is %s" % (cap(he), fr(1, 15))], e, rnd))
    # 15 gas tank
    word("Before a drive from Kelowna to Kamloops, the car’s gas tank is %s full. When the family arrives, it is %s full. "
         "What fraction of a tank did they use?" % (fr(5, 6), fr(1, 4)), P0(5, 6), P0(1, 4), "-", None)
    # 16 ferry
    n, he, his = P.next()
    word("A BC Ferries trip to Vancouver Island takes %s. %s reads for %s during the trip. For how long is %s not reading?"
         % (amt((1, 3, 4), HOUR), n, amt(P0(5, 6), HOUR), he), (1, 3, 4), P0(5, 6), "-", HOUR,
         post=" (That is 55 minutes.)")
    # 17 flour needed
    n, he, his = P.next()
    word("A bread recipe needs %s of flour. %s has only %s. How much more flour does %s need?"
         % (amt((2, 1, 4), CUP), n, amt((1, 2, 3), CUP), he), (2, 1, 4), (1, 2, 3), "-", CUP)
    # 18 weekly running goal
    n, he, his = P.next()
    tot = (4 + F(1, 2)) + (3 + F(3, 4)) + (2 + F(1, 3))
    assert tot == 10 + F(7, 12) and 12 - tot == 1 + F(5, 12)
    e = ("Add the three runs. Use twelfths: 4 %s + 3 %s + 2 %s = 9 %s = 10 %s km. "
         "Then 12 − 10 %s: regroup, 12 = 11 %s. 11 %s − 10 %s = <b>1 %s km</b>."
         % (fr(6, 12), fr(9, 12), fr(4, 12), fr(19, 12), fr(7, 12), fr(7, 12), fr(12, 12), fr(12, 12), fr(7, 12), fr(5, 12)))
    its.append(mcq("%s’s goal is to run 12 km this week. %s has run 4 %s km, 3 %s km and 2 %s km. How much farther does %s need to run?"
                   % (n, cap(he), fr(1, 2), fr(3, 4), fr(1, 3), he) + SIMPLE, 1 + F(5, 12),
                   [10 + F(7, 12), 2 + F(5, 12), F(5, 12)], e, rnd, KM))
    # 19 backpack lunch
    n, he, his = P.next()
    word("On a field trip, %s’s backpack with lunch in it has a mass of %s. After lunch, the backpack has a mass of %s. "
         "What was the mass of the lunch?" % (n, amt((4, 1, 4), KG), amt((3, 5, 8), KG)), (4, 1, 4), (3, 5, 8), "-", KG)
    # 20 commute
    n, he, his = P.next()
    assert 1 - F(2, 3) - F(1, 5) == F(2, 15)
    e = ("Add the two parts. Use fifteenths: %s + %s = %s. The whole trip is %s. Walking: %s − %s = <b>%s</b>."
         % (fr(10, 15), fr(3, 15), fr(13, 15), fr(15, 15), fr(15, 15), fr(13, 15), fr(2, 15)))
    its.append(mcq("%s spends %s of %s trip to school on the SkyTrain and %s of it on a bus. %s walks for the rest. "
                   "What fraction of the trip does %s spend walking?" % (n, fr(2, 3), his, fr(1, 5), cap(he), he) + SIMPLE,
                   F(2, 15), [F(13, 15), F(5, 8), F(1, 3)], e, rnd))
    assert len(its) == 20, len(its)
    return {"title": "Word problems", "items": its}


# ============================================================ lesson
def body_html():
    f_bars = two_bars_svg(6, 5, 4, 1, 12, W=360, labels=True)
    f_line = jump_line_svg(1, 12, F(5, 6), F(7, 12), W=380)
    return (
        "<h2>Unlike denominators: make the parts the same size</h2>"
        "<p>The denominator tells the <b>size</b> of the parts. The numerator tells <b>how many</b> parts. "
        "You can only add or subtract parts of the same size. So first find a <b>common denominator</b>. "
        "The best choice is the <b>lowest common multiple</b> of the denominators. Then write <b>equivalent fractions</b>: "
        "multiply the numerator and the denominator by the same number. Add or subtract the numerators. Keep the denominator.</p>"
        "<figure class='sn-fig'>" + f_bars +
        "<figcaption>The dashed lines split both bars into twelfths. " + fr(5, 6) + " = " + fr(10, 12) + " and " +
        fr(1, 4) + " = " + fr(3, 12) + ".</figcaption></figure>" +
        table(["Fractions", "Lowest common denominator", "Equivalent fractions"], [
            [fr(3, 8) + " and " + fr(5, 12), "24", fr(9, 24) + " and " + fr(10, 24)],
            [fr(2, 9) + " and " + fr(5, 6), "18", fr(4, 18) + " and " + fr(15, 18)],
            [fr(7, 10) + " and " + fr(3, 4), "20", fr(14, 20) + " and " + fr(15, 20)],
        ])
        + ex("Example 1", fr(3, 4) + " + " + fr(5, 6) + " = ?",
             "Lowest common denominator: 12. " + fr(3, 4) + " = " + fr(9, 12) + " and " + fr(5, 6) + " = " + fr(10, 12) +
             ". Add the numerators: 9 + 10 = 19. " + fr(19, 12) + " = 1 " + fr(7, 12) + ".", "1 " + fr(7, 12)) +
        "<p>On a number line split into twelfths, start at " + fr(5, 6) + " (10 steps) and jump back " + fr(1, 4) +
        " (3 steps). You land on " + fr(7, 12) + ".</p>"
        "<figure class='sn-fig'>" + f_line +
        "<figcaption>" + fr(5, 6) + " − " + fr(1, 4) + " = " + fr(7, 12) + " on a number line.</figcaption></figure>"
        "<h2>Simplest form</h2>"
        "<p>A fraction is in <b>simplest form</b> when the numerator and denominator have no common factor except 1. "
        "Divide both by their <b>greatest common factor (GCF)</b>. Write an improper fraction as a mixed number.</p>"
        + ex("Example 2", fr(2, 15) + " + " + fr(1, 6) + " = ?",
             fr(4, 30) + " + " + fr(5, 30) + " = " + fr(9, 30) + ". The GCF of 9 and 30 is 3. 9 ÷ 3 = 3 and 30 ÷ 3 = 10.", fr(3, 10)) +
        "<h2>Mixed numbers and regrouping</h2>"
        "<p>Write the fraction parts with a common denominator. Then add or subtract the fractions and the whole numbers. "
        "If the first fraction is too small to subtract from, <b>regroup</b>: rename 1 whole as a fraction.</p>" +
        table(["Calculation", "Equivalent fractions", "Fractions", "Whole numbers", "Answer"], [
            ["3 " + fr(5, 8) + " + 1 " + fr(2, 3), "3 " + fr(15, 24) + " + 1 " + fr(16, 24), fr(31, 24) + " = 1 " + fr(7, 24), "3 + 1 + 1 = 5", "5 " + fr(7, 24)],
            ["6 " + fr(7, 9) + " − 2 " + fr(1, 6), "6 " + fr(14, 18) + " − 2 " + fr(3, 18), fr(11, 18), "6 − 2 = 4", "4 " + fr(11, 18)],
            ["5 " + fr(1, 4) + " − 2 " + fr(5, 6), "5 " + fr(3, 12) + " − 2 " + fr(10, 12), "regroup: 4 " + fr(15, 12), "4 − 2 = 2", "2 " + fr(5, 12)],
        ])
        + ex("Example 3", "5 " + fr(1, 4) + " − 2 " + fr(5, 6) + " = ?",
             "5 " + fr(3, 12) + " − 2 " + fr(10, 12) + ". " + fr(3, 12) + " is less than " + fr(10, 12) + ", so regroup: 5 " +
             fr(3, 12) + " = 4 " + fr(15, 12) + ". Fractions: " + fr(15, 12) + " − " + fr(10, 12) + " = " + fr(5, 12) +
             ". Whole numbers: 4 − 2 = 2.", "2 " + fr(5, 12)) +
        "<p>Another way: change both to improper fractions. 5 " + fr(1, 4) + " = " + fr(63, 12) + " and 2 " + fr(5, 6) +
        " = " + fr(34, 12) + ". " + fr(63, 12) + " − " + fr(34, 12) + " = " + fr(29, 12) + " = 2 " + fr(5, 12) + ".</p>"
        "<h2>Order of operations with + and −</h2>"
        "<p>Brackets come first. Addition and subtraction have the same rank, so then work <b>from left to right</b>.</p>"
        + ex("Example 4", fr(9, 10) + " − " + fr(1, 2) + " + " + fr(1, 5) + " = ?",
             "Left to right: " + fr(9, 10) + " − " + fr(5, 10) + " = " + fr(4, 10) + ". Then " + fr(4, 10) + " + " + fr(2, 10) +
             " = " + fr(6, 10) + " = " + fr(3, 5) + ". (Adding " + fr(1, 2) + " + " + fr(1, 5) + " first gives " + fr(1, 5) +
             ", which is wrong.)", fr(3, 5))
        + ex("Example 5", fr(5, 6) + " − (" + fr(1, 3) + " + " + fr(1, 4) + ") = ?",
             "Brackets first: " + fr(4, 12) + " + " + fr(3, 12) + " = " + fr(7, 12) + ". Then " + fr(10, 12) + " − " + fr(7, 12) +
             " = " + fr(3, 12) + " = " + fr(1, 4) + ".", fr(1, 4)) +
        "<h2>Common mistakes</h2>" +
        table(["Mistake", "What to do instead"], [
            [fr(3, 4) + " + " + fr(1, 6) + " = " + fr(4, 10) + " (adding the numerators and the denominators)",
             "Use a common denominator: " + fr(9, 12) + " + " + fr(2, 12) + " = " + fr(11, 12)],
            [fr(7, 12) + " + " + fr(3, 12) + " = " + fr(10, 24) + " (adding the denominators)",
             "Keep the denominator: " + fr(10, 12) + " = " + fr(5, 6)],
            [fr(5, 6) + " − " + fr(3, 8) + " = " + fr(5, 24) + " − " + fr(3, 24) + " (changing the denominators but not the numerators)",
             "Multiply the numerator by the same number: " + fr(20, 24) + " − " + fr(9, 24) + " = " + fr(11, 24)],
            ["5 " + fr(1, 4) + " − 2 " + fr(5, 6) + " = 3 " + fr(7, 12) + " (taking " + fr(3, 12) + " from " + fr(10, 12) + ")",
             "Regroup 1 whole: 4 " + fr(15, 12) + " − 2 " + fr(10, 12) + " = 2 " + fr(5, 12)],
            [fr(3, 4) + " − " + fr(1, 4) + " + " + fr(1, 2) + " = 0 (adding first)",
             "Work from left to right: " + fr(2, 4) + " + " + fr(1, 2) + " = 1"],
        ])
    )


FAQ = [
    {"q": "Where are fractions in the BC Grade 8 math curriculum?",
     "a": "They are in the Grade 8 Computational fluency standard: operations with fractions (addition, subtraction, multiplication, division, and order of operations). This page covers addition and subtraction, including mixed numbers and the order of operations with + and −."},
    {"q": "Why can’t you just add the denominators?",
     "a": "The denominator tells the size of the parts, and the size does not change when you add. 1/4 + 1/4 is 2/4 = 1/2, not 2/8 = 1/4, so keep the common denominator and add only the numerators."},
    {"q": "How do you subtract mixed numbers when you need to regroup?",
     "a": "If the first fraction is smaller, rename 1 whole as a fraction. For 5 1/4 − 2 5/6, write 5 3/12 − 2 10/12, regroup to 4 15/12 − 2 10/12, and the answer is 2 5/12."},
    {"q": "What is the order of operations when there is only + and −?",
     "a": "Do anything in brackets first, then add and subtract from left to right. For example, 9/10 − 1/2 + 1/5 = 2/5 + 1/5 = 3/5, but 5/6 − (1/3 + 1/4) = 5/6 − 7/12 = 1/4."},
]


def gen_unit():
    rnd = random.Random(58804)
    P = People(rnd)
    sets = [set_unlike(rnd, P), set_mixed(rnd, P), set_simplest(rnd, P), set_order(rnd, P), set_words(rnd, P)]
    seen = set()
    for s in sets:
        assert len(s["items"]) == 20, (s["title"], len(s["items"]))
        assert sorted(it["a"] for it in s["items"]) == sorted([0, 1, 2, 3] * 5), s["title"]
        for it in s["items"]:
            assert len(set(it["c"])) == 4, it
            assert it["q"] not in seen, it["q"]
            seen.add(it["q"])
    return {
        "country": "ca-bc", "subject": "math", "grade": "grade-8", "slug": "adding-and-subtracting-fractions", "sort": 4,
        "updated": UPDATED, "pdf_url": "",
        "title": "Grade 8 Adding and Subtracting Fractions",
        "seo_title": "Grade 8 Adding and Subtracting Fractions Worksheets: Free Math with Answer Key (BC Curriculum)",
        "short_title": "Adding and Subtracting Fractions",
        "domain": "Computational fluency",
        "standard_code": "Grade 8: Computational fluency",
        "standard_url": "https://curriculum.gov.bc.ca/curriculum/mathematics/8/core",
        "standard_text": "Operations with fractions (addition, subtraction, multiplication, division, and order of operations)",
        "meta_desc": "Free Grade 8 math worksheets on adding and subtracting fractions, matched to the BC curriculum: unlike denominators, mixed numbers with regrouping, simplest form, order of operations with + and −, and word problems. 100 questions with an answer key.",
        "key_big": "Make the parts the same size first: use a common denominator, add or subtract only the numerators, then simplify.",
        "key_sub": "3/4 + 1/6 = 9/12 + 2/12 = 11/12, not 4/10. With + and − only, do brackets first, then work from left to right.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }


if __name__ == "__main__":
    u = gen_unit()
    mark_large(u, "(two bars|bar of|number line)")
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(u, f, ensure_ascii=False, indent=1)
    print("wrote", path)
