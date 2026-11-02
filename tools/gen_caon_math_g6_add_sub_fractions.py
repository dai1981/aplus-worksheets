# -*- coding: utf-8 -*-
"""
CA Grade 6 Math: Adding and Subtracting Fractions
(Ontario Curriculum 2020, Grade 6: Number, B2)
  python3 tools/gen_ca_math_g6_add_sub_fractions.py
Like, related and unlike denominators, answers greater than 1, mixed numbers with regrouping,
fraction bars, number lines and word problems. Every answer is in
simplest form; wrong choices come from real mistakes and are also in simplest form, so the
form never gives the answer away. A wrong choice is never equal in value to the right answer
or to another choice. Every answer is checked in code with fractions.Fraction.
HTML attributes use single quotes (no backslashes in the JSON). Canadian English.
"""
import json, math, os, random, re
from fractions import Fraction

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "ca-on", "math", "grade-6")
UPDATED = "2026-11-02"
FILL = "#4fae74"      # first fraction
FILL2 = "#f2b84b"     # second fraction
RED = "#c0392b"
BLUE = "#2f6db5"
LINE = "#2b2b2b"
GIRLS = ["Olivia", "Emma", "Maya", "Zoe", "Amira", "Mei", "Chloe", "Priya", "Leah", "Hana", "Ava", "Sofia"]
BOYS = ["Liam", "Noah", "Aiden", "Lucas", "Owen", "Arjun", "Ethan", "Jayden", "Benjamin", "Mateo", "Nathan", "Kai"]
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


# ============================================================ set 1: like denominators
def set_like(rnd, P):
    SPOTS.left = []
    its = []
    # A: fraction bars
    q = (fig(one_bar_svg(8, 2, 3)) + "The bar is split into eighths. Green shows %s and yellow shows %s. What is %s + %s?"
         % (fr(2, 8), fr(3, 8), fr(2, 8), fr(3, 8)) + SIMPLE)
    its.append(like_q(2, 3, 8, "+", rnd, q=q))
    q = (fig(one_bar_svg(10, 3, 4)) + "The bar is split into tenths. Green shows %s and yellow shows %s. What is %s + %s?"
         % (fr(3, 10), fr(4, 10), fr(3, 10), fr(4, 10)) + SIMPLE)
    its.append(like_q(3, 4, 10, "+", rnd, q=q))
    q = (fig(one_bar_svg(6, 5, 0, crossed=2)) + "The bar is split into sixths. The shaded part is %s, and %s is crossed out. What is %s − %s?"
         % (fr(5, 6), fr(2, 6), fr(5, 6), fr(2, 6)) + SIMPLE)
    its.append(like_q(5, 2, 6, "-", rnd, q=q, extra=[Fraction(5, 6)]))
    # B: spot the mistake
    n, he, his = P.next()
    assert Fraction(2, 5) + Fraction(1, 5) == Fraction(3, 5)
    e = ("Fifths stay fifths. 2 fifths + 1 fifth = 3 fifths, so the answer is %s. Only the numerators are added. "
         "Also, %s is less than %s, so it cannot be the total." % (fr(3, 5), fr(3, 10), fr(2, 5)))
    its.append(mcq("%s wrote %s + %s = %s. What mistake did %s make?" % (n, fr(2, 5), fr(1, 5), fr(3, 10), he),
                   "%s added the denominators too" % cap(he),
                   ["%s forgot to simplify" % cap(he), "%s should have multiplied" % cap(he), "There is no mistake"], e, rnd))
    # C: add, answer less than 1
    for n1, n2, d in [(1, 2, 4), (2, 3, 7), (3, 4, 9), (1, 3, 8), (5, 1, 12), (3, 5, 11)]:
        assert n1 + n2 < d
        its.append(like_q(n1, n2, d, "+", rnd))
    # D: subtract
    for n1, n2, d in [(4, 1, 5), (6, 2, 7), (7, 3, 8), (7, 4, 9), (11, 7, 12)]:
        its.append(like_q(n1, n2, d, "-", rnd))
    # E: answers greater than 1
    for n1, n2, d in [(4, 3, 5), (7, 5, 8), (5, 5, 6)]:
        assert n1 + n2 > d
        its.append(like_q(n1, n2, d, "+", rnd, prompt=MIXED))
    # F: three fractions
    assert Fraction(1, 6) + Fraction(2, 6) + Fraction(5, 6) == Fraction(4, 3)
    e = ("All three are sixths, so add the numerators: 1 + 2 + 5 = 8. The total is %s. %s = 1 %s. "
         "Simplify: %s = %s. The answer is <b>1 %s</b>." % (fr(8, 6), fr(8, 6), fr(2, 6), fr(2, 6), fr(1, 3), fr(1, 3)))
    its.append(mcq("%s + %s + %s = ?" % (fr(1, 6), fr(2, 6), fr(5, 6)) + MIXED, Fraction(4, 3),
                   [Fraction(8, 18), Fraction(1, 3), Fraction(5, 3)], e, rnd))
    # G: 1 whole minus a fraction
    assert 1 - Fraction(3, 8) == Fraction(5, 8)
    e = ("Write 1 whole as eighths: 1 = %s. Then %s − %s = <b>%s</b>." % (fr(8, 8), fr(8, 8), fr(3, 8), fr(5, 8)))
    its.append(mcq("1 − %s = ?" % fr(3, 8) + SIMPLE, Fraction(5, 8),
                   [Fraction(3, 8), Fraction(1, 4), Fraction(11, 8)], e, rnd))
    assert len(its) == 20, len(its)
    return {"title": "Like denominators", "items": its}


# ============================================================ set 2: related denominators
def set_related(rnd):
    SPOTS.left = []
    its = []
    # A: fraction bars
    for n1, d1, n2, d2, op in [(1, 2, 3, 8, "+"), (1, 3, 1, 6, "+"), (3, 4, 3, 8, "-"), (5, 6, 1, 3, "-")]:
        L = lcm(d1, d2)
        k1, k2 = n1 * L // d1, n2 * L // d2
        x, y = P0(n1, d1), P0(n2, d2)
        if op == "+":
            q = (fig(one_bar_svg(L, k1, k2)) +
                 "The bar is split into %s. Green shows %s and yellow shows %s. What is %s + %s?"
                 % (WORD[L], fr(n1, d1), fr(n2, d2), fr(n1, d1), fr(n2, d2)) + SIMPLE)
            its.append(mcq(q, val(x) + val(y), wrong(x, y, "+"), e_calc(x, y, "+"), rnd))
        else:
            q = (fig(one_bar_svg(L, k1, 0, crossed=k2)) +
                 "The bar is split into %s. The shaded part is %s, and %s of the bar is crossed out. What is %s − %s?"
                 % (WORD[L], fr(n1, d1), fr(n2, d2), fr(n1, d1), fr(n2, d2)) + SIMPLE)
            look = [Fraction(L - k1 + k2, L), Fraction(n1, d1)]   # counted white + crossed parts; ignored the crosses
            its.append(mcq(q, val(x) - val(y), look + wrong(x, y, "-"), e_calc(x, y, "-"), rnd))
    # B: the first step
    for n1, d1, n2, d2, bad in [(3, 4, 1, 8, [fr(3, 8), fr(7, 8), fr(5, 8)]),
                                (2, 3, 1, 12, [fr(2, 12), fr(11, 12), fr(6, 12)])]:
        L = d2
        k = L // d1
        q = ("To work out %s + %s, you change %s into %s. Which fraction is equal to %s?"
             % (fr(n1, d1), fr(n2, d2), fr(n1, d1), WORD[L], fr(n1, d1)))
        e = ("%d × %d = %d, so multiply the numerator by %d too: %d × %d = %d. %s = <b>%s</b>. "
             "Then %s + %s = %s."
             % (d1, k, L, k, n1, k, n1 * k, fr(n1, d1), fr(n1 * k, L), fr(n1 * k, L), fr(n2, L), fr(n1 * k + n2, L)))
        assert Fraction(n1, d1) == Fraction(n1 * k, L)
        its.append(mcq(q, fr(n1 * k, L), bad, e, rnd))
    # C: add
    for n1, d1, n2, d2 in [(1, 4, 3, 8), (2, 5, 3, 10), (1, 6, 7, 12), (1, 3, 4, 9), (1, 4, 5, 12), (1, 2, 3, 10), (1, 2, 1, 6)]:
        x, y = P0(n1, d1), P0(n2, d2)
        assert val(x) + val(y) < 1
        its.append(calc(x, y, "+", rnd))
    # D: subtract
    for n1, d1, n2, d2 in [(9, 10, 2, 5), (2, 3, 4, 9), (11, 12, 1, 4), (7, 12, 1, 3), (7, 8, 1, 2), (4, 5, 3, 10), (5, 6, 1, 2)]:
        x, y = P0(n1, d1), P0(n2, d2)
        assert val(x) - val(y) > 0
        its.append(calc(x, y, "-", rnd))
    assert len(its) == 20, len(its)
    return {"title": "Related denominators", "items": its}


# ============================================================ set 3: unlike denominators
def set_unlike(rnd, P):
    SPOTS.left = []
    its = []
    # A: lowest common denominator
    for n1, d1, n2, d2 in [(2, 3, 3, 4), (1, 4, 1, 6), (3, 8, 5, 6)]:
        L = lcm(d1, d2)
        big, small = max(d1, d2), min(d1, d2)
        mb = ", ".join(str(big * i) for i in range(1, L // big + 1))
        ms = ", ".join(str(small * i) for i in range(1, L // small + 1))
        e = ("Multiples of %d: %s. Multiples of %d: %s. The first number in both lists is <b>%d</b>."
             % (big, mb, small, ms, L))
        if d1 * d2 != L:
            e += " %d × %d = %d also works, but it is not the lowest." % (d1, d2, d1 * d2)
        cands = [d1 * d2 if d1 * d2 != L else None, d1 + d2, big, 2 * L]
        its.append(mcq("What is the lowest common denominator of %s and %s?" % (fr(n1, d1), fr(n2, d2)),
                       str(L), [str(v) for v in cands if v], e, rnd))
    # B: fraction bars
    for n1, d1, n2, d2 in [(2, 3, 1, 4), (1, 2, 2, 5)]:
        L = lcm(d1, d2)
        q = (fig(two_bars_svg(d1, n1, d2, n2, L)) +
             "The green part is %s and the yellow part is %s. The dashed lines split both bars into %s. "
             "Which shows both fractions in %s?" % (fr(n1, d1), fr(n2, d2), WORD[L], WORD[L]))
        r, c = rename_choices(n1, d1, n2, d2, L)
        e = "Count the small parts in each shaded piece. " + e_rename(n1, d1, n2, d2, L)
        its.append(mcq(q, r, c, e, rnd))
    # C: spot the mistake
    n, he, his = P.next()
    q = "%s wrote %s + %s = %s. What mistake did %s make?" % (n, fr(1, 2), fr(1, 3), fr(2, 5), he)
    e = ("Halves and thirds are different sizes, so you cannot add the numerators and the denominators. "
         "Use sixths: %s + %s = %s. Also, %s is less than %s, so it cannot be the total."
         % (fr(3, 6), fr(2, 6), fr(5, 6), fr(2, 5), fr(1, 2)))
    assert Fraction(1, 2) + Fraction(1, 3) == Fraction(5, 6) and Fraction(2, 5) < Fraction(1, 2)
    its.append(mcq(q, "%s added the numerators and the denominators" % cap(he),
                   ["%s forgot to simplify" % cap(he), "%s should have multiplied" % cap(he), "There is no mistake"], e, rnd))
    # D: number lines
    its.append(jump_item(1, 3, 1, 4, "+", 1, rnd))
    its.append(jump_item(5, 6, 1, 4, "-", 1, rnd))
    # E: add, answer less than 1
    for n1, d1, n2, d2 in [(1, 5, 1, 2), (1, 3, 2, 5), (3, 8, 1, 6), (2, 9, 1, 6)]:
        x, y = P0(n1, d1), P0(n2, d2)
        assert val(x) + val(y) < 1 and lcm(d1, d2) != max(d1, d2)
        its.append(calc(x, y, "+", rnd))
    # F: add, answer greater than 1
    for n1, d1, n2, d2 in [(5, 6, 3, 4), (2, 3, 3, 5), (5, 8, 5, 6)]:
        x, y = P0(n1, d1), P0(n2, d2)
        assert val(x) + val(y) > 1 and lcm(d1, d2) != max(d1, d2)
        its.append(calc(x, y, "+", rnd, prompt=MIXED))
    # G: subtract
    for n1, d1, n2, d2 in [(2, 3, 1, 4), (4, 5, 1, 2), (5, 6, 3, 4), (3, 4, 2, 5), (9, 10, 3, 4)]:
        x, y = P0(n1, d1), P0(n2, d2)
        assert val(x) - val(y) > 0 and lcm(d1, d2) != max(d1, d2)
        its.append(calc(x, y, "-", rnd))
    assert len(its) == 20, len(its)
    return {"title": "Unlike denominators (common denominators)", "items": its}


# ============================================================ set 4: mixed numbers
def set_mixed(rnd):
    SPOTS.left = []
    its = []
    add_easy = [((2, 1, 3), (1, 1, 4)), ((1, 1, 2), (2, 1, 5)), ((2, 3, 8), (4, 1, 4)), ((1, 1, 6), (2, 3, 4))]
    add_carry = [((2, 1, 3), (1, 3, 4)), ((2, 5, 6), (1, 1, 2)), ((3, 4, 5), (1, 1, 2)), ((1, 7, 8), (2, 1, 4)), ((2, 3, 4), (3, 5, 6))]
    sub_easy = [((3, 3, 4), (1, 1, 3)), ((5, 5, 6), (2, 1, 2)), ((4, 7, 10), (1, 2, 5)), ((6, 2, 3), (4, 1, 6))]
    sub_ex = [((4, 1, 5), (1, 2, 3)), ((3, 1, 4), (1, 2, 3)), ((4, 1, 3), (2, 1, 2)), ((5, 1, 6), (2, 3, 4)),
              ((6, 2, 5), (3, 1, 2)), ((7, 1, 8), (4, 3, 4))]
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
    # a whole number minus a mixed number
    assert 4 - Fraction(5, 3) == Fraction(7, 3)
    e = ("There is no fraction to take %s from, so regroup: rename 1 whole as %s. 4 = 3 %s. "
         "Subtract the fractions: %s − %s = %s. Subtract the whole numbers: 3 − 1 = 2. The answer is <b>2 %s</b>."
         % (fr(2, 3), fr(3, 3), fr(3, 3), fr(3, 3), fr(2, 3), fr(1, 3), fr(1, 3)))
    its.append(mcq("4 − 1 %s = ?" % fr(2, 3) + SIMPLE, Fraction(7, 3),
                   [Fraction(11, 3), Fraction(10, 3), Fraction(8, 3)], e, rnd))
    assert len(its) == 20, len(its)
    return {"title": "Mixed numbers with regrouping", "items": its}


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

    # 1 pancake recipe
    n, he, his = P.next()
    word("%s is making pancakes for a weekend breakfast. The recipe uses %s of milk and %s of water. How much liquid is that altogether?"
         % (n, amt(P0(3, 4), CUP), amt(P0(1, 3), CUP)), P0(3, 4), P0(1, 3), "+", CUP)
    # 2 the 2 L jug
    (n1, _, _), (n2, _, _) = P.next(), P.next()
    assert 2 - Fraction(3, 4) - Fraction(2, 3) == Fraction(7, 12)
    e = ("First add what they pour. Use twelfths: %s + %s = %s = 1 %s L. "
         "Then 2 − 1 %s: regroup 1 whole, 2 = 1 %s. 1 %s − 1 %s = <b>%s L</b>."
         % (fr(9, 12), fr(8, 12), fr(17, 12), fr(5, 12), fr(5, 12), fr(12, 12), fr(12, 12), fr(5, 12), fr(7, 12)))
    its.append(mcq("A 2 L jug of lemonade is full. At the class picnic, %s pours %s L into cups and %s pours %s L. "
                   "How much lemonade is left in the jug?" % (n1, fr(3, 4), n2, fr(2, 3)) + SIMPLE, Fraction(7, 12),
                   [Fraction(17, 12), Fraction(19, 12), Fraction(9, 7)], e, rnd, LITRE))
    # 3 piano practice
    n, he, his = P.next()
    assert Fraction(2, 3) + Fraction(1, 4) == Fraction(11, 12)
    word("%s practises piano for %s on Monday and %s on Tuesday. How long does %s practise altogether?"
         % (n, amt(P0(2, 3), HOUR), amt(P0(1, 4), HOUR), he), P0(2, 3), P0(1, 4), "+", HOUR,
         post=" (That is 55 minutes.)")
    # 4 practice time left
    n, he, his = P.next()
    assert Fraction(5, 4) - Fraction(2, 3) == Fraction(7, 12)
    word("%s plans to practise guitar for %s this week. %s has practised for %s so far. How much practice time is left?"
         % (n, amt((1, 1, 4), HOUR), cap(he), amt(P0(2, 3), HOUR)), (1, 1, 4), P0(2, 3), "-", HOUR,
         post=" (That is 35 minutes.)")
    # 5 ribbon
    n, he, his = P.next()
    word("%s has %s of ribbon. %s uses %s to decorate a Thanksgiving centrepiece. How much ribbon is left?"
         % (n, amt((3, 1, 3), M), cap(he), amt((1, 3, 4), M)), (3, 1, 3), (1, 3, 4), "-", M)
    # 6 garden
    assert 1 - Fraction(1, 3) - Fraction(2, 5) == Fraction(4, 15)
    e = ("First add the parts that are used. Use fifteenths: %s = %s and %s = %s, so %s + %s = %s. "
         "The whole garden is %s. Flowers: %s − %s = <b>%s</b>."
         % (fr(1, 3), fr(5, 15), fr(2, 5), fr(6, 15), fr(5, 15), fr(6, 15), fr(11, 15), fr(15, 15), fr(15, 15), fr(11, 15), fr(4, 15)))
    its.append(mcq("In the school garden, %s of the ground is for vegetables and %s is for herbs. The rest is for flowers. "
                   "What fraction of the garden is for flowers?" % (fr(1, 3), fr(2, 5)) + SIMPLE, Fraction(4, 15),
                   [Fraction(11, 15), Fraction(5, 8), Fraction(3, 8)], e, rnd))
    # 7 pizza
    (n1, _, _), (n2, _, _) = P.next(), P.next()
    assert 1 - Fraction(1, 4) - Fraction(1, 3) == Fraction(5, 12)
    e = ("First add what they eat. Use twelfths: %s + %s = %s. The whole pizza is %s. Left: %s − %s = <b>%s</b>."
         % (fr(3, 12), fr(4, 12), fr(7, 12), fr(12, 12), fr(12, 12), fr(7, 12), fr(5, 12)))
    its.append(mcq("%s eats %s of a pizza and %s eats %s of it. What fraction of the pizza is left?" % (n1, fr(1, 4), n2, fr(1, 3))
                   + SIMPLE, Fraction(5, 12), [Fraction(7, 12), Fraction(5, 7), Fraction(2, 7)], e, rnd))
    # 8 canoe trip
    word("On a canoe trip, a family paddles %s to an island and then %s to their campsite. How far do they paddle altogether?"
         % (amt((2, 1, 4), KM), amt((1, 2, 3), KM)), (2, 1, 4), (1, 2, 3), "+", KM)
    # 9 farther
    (n1, _, _), (n2, _, _) = P.next(), P.next()
    word("At the Terry Fox Run, %s runs %s. %s runs %s. How much farther does %s run than %s?"
         % (n1, amt((1, 3, 4), KM), n2, amt((1, 5, 6), KM), n2, n1), (1, 5, 6), (1, 3, 4), "-", KM,
         extra=[Fraction(43, 12), Fraction(1), Fraction(1, 6)], pre="“How much farther” means subtract. ")
    # 10 juice jug
    n, he, his = P.next()
    word("A jug holds %s of apple juice. %s pours %s into glasses. How much juice is left in the jug?"
         % (amt((1, 1, 2), LITRE), n, amt(P0(5, 8), LITRE)), (1, 1, 2), P0(5, 8), "-", LITRE)
    # 11 flour recipe
    n, he, his = P.next()
    assert Fraction(3, 4) - Fraction(1, 2) - Fraction(1, 8) == Fraction(1, 8)
    e = ("%s has %s + %s = %s + %s = %s kg. %s needs %s = %s kg. %s − %s = <b>%s kg</b> more."
         % (cap(he), fr(1, 2), fr(1, 8), fr(4, 8), fr(1, 8), fr(5, 8), cap(he), fr(3, 4), fr(6, 8), fr(6, 8), fr(5, 8), fr(1, 8)))
    its.append(mcq("A bread recipe needs %s kg of flour. %s has two open bags with %s kg and %s kg left in them. How much more flour does %s need?"
                   % (fr(3, 4), n, fr(1, 2), fr(1, 8), he) + SIMPLE, Fraction(1, 8),
                   [Fraction(5, 8), Fraction(1, 4), Fraction(11, 8)], e, rnd, KG))
    # 12 maple oatmeal cookies
    word("A recipe for maple oatmeal cookies uses %s of rolled oats and %s of flour. How many cups is that altogether?"
         % (amt((1, 1, 4), CUP), amt(P0(5, 6), CUP)), (1, 1, 4), P0(5, 6), "+", CUP)
    # 13 hockey tournament
    word("A Saturday hockey tournament lasts %s. The lunch break takes %s. How much time is left for games?"
         % (amt((4, 1, 2), HOUR), amt(P0(3, 4), HOUR)), (4, 1, 2), P0(3, 4), "-", HOUR,
         post=" (That is 3 hours 45 minutes.)")
    # 14 soccer practice
    n, he, his = P.next()
    word("%s has soccer practice for %s on Tuesday and %s on Thursday. How many hours of practice is that altogether?"
         % (n, amt((1, 1, 3), HOUR), amt((1, 1, 2), HOUR)), (1, 1, 3), (1, 1, 2), "+", HOUR,
         post=" (That is 2 hours 50 minutes.)")
    # 15 boards
    word("Two boards, %s and %s long, are joined end to end to edge a garden bed. What is the total length?"
         % (amt((2, 2, 3), M), amt((1, 4, 5), M)), (2, 2, 3), (1, 4, 5), "+", M)
    # 16 class travel
    assert 1 - Fraction(1, 2) - Fraction(1, 3) == Fraction(1, 6)
    e = ("Add the two groups. Use sixths: %s + %s = %s. The whole class is %s. Driven by car: %s − %s = <b>%s</b>."
         % (fr(3, 6), fr(2, 6), fr(5, 6), fr(6, 6), fr(6, 6), fr(5, 6), fr(1, 6)))
    its.append(mcq("In a Grade 6 class, %s of the students walk to school and %s take the school bus. The rest come by car. "
                   "What fraction of the class comes by car?" % (fr(1, 2), fr(1, 3)) + SIMPLE, Fraction(1, 6),
                   [Fraction(5, 6), Fraction(3, 5), Fraction(2, 5)], e, rnd))
    # 17 bike ride
    n, he, his = P.next()
    assert Fraction(3, 4) + Fraction(5, 12) == Fraction(7, 6)
    e = ("Work out 1 %s − %s. Use twelfths: 1 %s = %s and %s = %s. %s − %s = <b>%s km</b>. "
         "Check: %s + %s = %s = 1 %s."
         % (fr(1, 6), fr(3, 4), fr(1, 6), fr(14, 12), fr(3, 4), fr(9, 12), fr(14, 12), fr(9, 12), fr(5, 12),
            fr(9, 12), fr(5, 12), fr(14, 12), fr(1, 6)))
    its.append(mcq("%s’s bike ride to the community centre is 1 %s km. %s has ridden %s km so far. How far is left to ride?"
                   % (n, fr(1, 6), cap(he), fr(3, 4)) + SIMPLE, Fraction(5, 12),
                   [Fraction(23, 12), Fraction(7, 12), Fraction(17, 12)], e, rnd, KM))
    # 18 spot the mistake
    n, he, his = P.next()
    assert Fraction(2, 5) + Fraction(1, 3) == Fraction(11, 15) and Fraction(3, 8) < Fraction(2, 5)
    e = ("%s added the numerators and the denominators. Use fifteenths: %s + %s = %s. "
         "Also, %s is less than %s, so it cannot be the total. The answer is <b>%s</b>."
         % (n, fr(6, 15), fr(5, 15), fr(11, 15), fr(3, 8), fr(2, 5), fr(11, 15)))
    its.append(mcq("%s spends %s of an hour on math homework and %s of an hour reading. %s says that is %s of an hour altogether. Which is true?"
                   % (n, fr(2, 5), fr(1, 3), cap(he), fr(3, 8)),
                   "%s is wrong. It is %s" % (cap(he), fr(11, 15)),
                   ["%s is right" % cap(he), "%s is wrong. It is %s" % (cap(he), fr(1, 5)),
                    "%s is wrong. It is %s" % (cap(he), fr(2, 15))], e, rnd))
    # 19 which pair makes 1
    pairs = [((3, 4), (3, 12)), ((2, 3), (1, 6)), ((3, 5), (3, 10)), ((1, 2), (3, 8))]
    sums = [Fraction(*p) + Fraction(*q) for p, q in pairs]
    assert sums[0] == 1 and all(s != 1 for s in sums[1:]) and len(set(sums)) == 4
    e = ("%s = %s, and %s + %s = %s = 1, so <b>%s</b> is correct. The other totals are %s, %s and %s."
         % (fr(3, 4), fr(9, 12), fr(9, 12), fr(3, 12), fr(12, 12), pair(3, 4, 3, 12),
            show(sums[1]), show(sums[2]), show(sums[3])))
    its.append(mcq("A pizza is cut into equal slices. Which two fractions of the pizza make the whole pizza?", pair(3, 4, 3, 12),
                   [pair(p[0], p[1], q[0], q[1]) for p, q in pairs[1:]], e, rnd))
    # 20 Thanksgiving dinner
    word("For Thanksgiving dinner, a family buys %s of potatoes and %s of squash. How many kilograms of vegetables is that altogether?"
         % (amt((1, 3, 4), KG), amt((2, 1, 3), KG)), (1, 3, 4), (2, 1, 3), "+", KG)

    assert len(its) == 20, len(its)
    return {"title": "Word problems", "items": its}


# ============================================================ lesson
def body_html():
    f_like = one_bar_svg(8, 3, 2, W=360)
    f_bars = two_bars_svg(3, 1, 4, 1, 12, W=360, labels=True)
    f_line = jump_line_svg(1, 12, Fraction(1, 3), Fraction(7, 12), W=380)
    return (
        "<h2>Same denominator: add the numerators</h2>"
        "<p>The denominator tells the <b>size</b> of the parts. The numerator tells <b>how many</b> parts. "
        "When the denominators are the same, add or subtract the numerators and keep the denominator.</p>"
        "<figure class='sn-fig'>" + f_like +
        "<figcaption>3 eighths + 2 eighths = 5 eighths: " + fr(3, 8) + " + " + fr(2, 8) + " = " + fr(5, 8) +
        ", not " + fr(5, 16) + ".</figcaption></figure>"
        + ex("Example", fr(7, 10) + " − " + fr(3, 10) + " = ?",
             "Subtract the numerators: 7 − 3 = 4. Keep tenths: " + fr(4, 10) + ". Simplify: divide both by 2.", fr(2, 5)) +
        "<h2>Different denominators: make the parts the same size</h2>"
        "<p>Thirds and fourths are different sizes, so first find a <b>common denominator</b>: a number that both denominators divide into. "
        "Then write each fraction as an <b>equivalent fraction</b> with that denominator.</p>"
        "<figure class='sn-fig'>" + f_bars +
        "<figcaption>The dashed lines split both bars into twelfths. " + fr(1, 3) + " = " + fr(4, 12) + " and " +
        fr(1, 4) + " = " + fr(3, 12) + ".</figcaption></figure>"
        + ex("Example", fr(1, 3) + " + " + fr(1, 4) + " = ?",
             "Common denominator: 12. " + fr(1, 3) + " = " + fr(4, 12) + " and " + fr(1, 4) + " = " + fr(3, 12) +
             ". Add the numerators: 4 + 3 = 7.", fr(7, 12)) +
        "<p>On a number line split into twelfths, start at " + fr(1, 3) + " (4 steps) and jump forward " + fr(1, 4) +
        " (3 steps). You land on " + fr(7, 12) + ".</p>"
        "<figure class='sn-fig'>" + f_line +
        "<figcaption>" + fr(1, 3) + " + " + fr(1, 4) + " = " + fr(7, 12) + " on a number line.</figcaption></figure>"
        "<h2>Find the common denominator</h2>"
        "<p>If one denominator is a multiple of the other (<b>related denominators</b>), use the bigger one. Otherwise, find the "
        "<b>lowest common multiple</b> of the two denominators. Multiplying the denominators always works too, "
        "but the numbers get bigger.</p>" +
        table(["Fractions", "Common denominator", "Equivalent fractions"], [
            [fr(1, 2) + " and " + fr(3, 8), "8", fr(4, 8) + " and " + fr(3, 8)],
            [fr(2, 3) + " and " + fr(1, 4), "12", fr(8, 12) + " and " + fr(3, 12)],
            [fr(5, 6) + " and " + fr(3, 4), "12", fr(10, 12) + " and " + fr(9, 12)],
        ]) +
        "<p>Give answers in <b>simplest form</b>. If the answer is an improper fraction, write it as a <b>mixed number</b>.</p>"
        + ex("Example", fr(5, 6) + " + " + fr(3, 4) + " = ?",
             fr(10, 12) + " + " + fr(9, 12) + " = " + fr(19, 12) + ". 19 ÷ 12 = 1 remainder 7, so " +
             fr(19, 12) + " = 1 " + fr(7, 12) + ".", "1 " + fr(7, 12)) +
        "<h2>Mixed numbers and regrouping</h2>"
        "<p>Write the fraction parts with a common denominator. Then add or subtract the fractions and the whole numbers.</p>" +
        table(["Calculation", "Equivalent fractions", "Fractions", "Whole numbers", "Answer"], [
            ["2 " + fr(1, 3) + " + 1 " + fr(1, 4), "2 " + fr(4, 12) + " + 1 " + fr(3, 12), fr(7, 12), "2 + 1 = 3", "3 " + fr(7, 12)],
            ["2 " + fr(2, 3) + " + 1 " + fr(3, 4), "2 " + fr(8, 12) + " + 1 " + fr(9, 12), fr(17, 12) + " = 1 " + fr(5, 12), "2 + 1 + 1 = 4", "4 " + fr(5, 12)],
            ["3 " + fr(1, 4) + " − 1 " + fr(2, 3), "3 " + fr(3, 12) + " − 1 " + fr(8, 12), "regroup: 2 " + fr(15, 12), "2 − 1 = 1", "1 " + fr(7, 12)],
        ]) +
        "<p>In the last row, " + fr(3, 12) + " is less than " + fr(8, 12) + ", so <b>regroup</b>: rename 1 whole as " + fr(12, 12) +
        ". 3 " + fr(3, 12) + " = 2 " + fr(15, 12) + ".</p>"
        + ex("Example", "3 " + fr(1, 4) + " − 1 " + fr(2, 3) + " = ?",
             "3 " + fr(3, 12) + " − 1 " + fr(8, 12) + ". Regroup: 3 " + fr(3, 12) + " = 2 " + fr(15, 12) +
             ". Fractions: " + fr(15, 12) + " − " + fr(8, 12) + " = " + fr(7, 12) + ". Whole numbers: 2 − 1 = 1.", "1 " + fr(7, 12)) +
        "<p>Another way: change both to improper fractions. 3 " + fr(1, 4) + " = " + fr(39, 12) + " and 1 " + fr(2, 3) +
        " = " + fr(20, 12) + ". " + fr(39, 12) + " − " + fr(20, 12) + " = " + fr(19, 12) + " = 1 " + fr(7, 12) + ".</p>"
        "<h2>Common mistakes</h2>" +
        table(["Mistake", "What to do instead"], [
            [fr(3, 8) + " + " + fr(2, 8) + " = " + fr(5, 16) + " (adding the denominators)",
             "Keep the denominator: 3 eighths + 2 eighths = " + fr(5, 8)],
            [fr(1, 3) + " + " + fr(1, 4) + " = " + fr(2, 7) + " (adding the numerators and the denominators)",
             "Use a common denominator: " + fr(4, 12) + " + " + fr(3, 12) + " = " + fr(7, 12)],
            [fr(1, 2) + " + " + fr(3, 8) + " = " + fr(4, 8) + " (changing the denominator but not the numerator)",
             "Multiply the numerator by the same number: " + fr(1, 2) + " = " + fr(4, 8) + ", so the total is " + fr(7, 8)],
            ["3 " + fr(1, 4) + " − 1 " + fr(2, 3) + " = 2 " + fr(5, 12) + " (taking " + fr(3, 12) + " from " + fr(8, 12) + ")",
             "Regroup 1 whole: 2 " + fr(15, 12) + " − 1 " + fr(8, 12) + " = 1 " + fr(7, 12)],
            ["2 " + fr(2, 3) + " + 1 " + fr(3, 4) + " = 3 " + fr(17, 12) + " (not regrouping)",
             "Change " + fr(17, 12) + " to 1 " + fr(5, 12) + " and add it to the wholes: 4 " + fr(5, 12)],
        ])
    )


FAQ = [
    {"q": "What does the Ontario Grade 6 math curriculum say about adding and subtracting fractions?",
     "a": "In strand B (Number), Grade 6 students use tools to add and subtract fractions, including fractions with unlike denominators, in various contexts. Fraction bars, number lines and common denominators are all good tools."},
    {"q": "How do you add fractions with different denominators?",
     "a": "Find a common denominator, write both fractions as equivalent fractions with it, then add the numerators. For 1/3 + 1/4, use twelfths: 4/12 + 3/12 = 7/12."},
    {"q": "How do you subtract mixed numbers when you need to regroup?",
     "a": "If the first fraction is smaller, rename 1 whole as a fraction. For 3 1/4 − 1 2/3, write 3 3/12 − 1 8/12, regroup to 2 15/12 − 1 8/12, and the answer is 1 7/12."},
    {"q": "Are fractions on the Grade 6 EQAO math test?",
     "a": "The Grade 6 EQAO math assessment is based on the Ontario curriculum expectations, and Number, including fractions, is a big part of it. Practising with fraction models and word problems is good preparation."},
]


def gen_unit():
    rnd = random.Random(36804)
    P = People(rnd)
    sets = [set_like(rnd, P), set_related(rnd), set_unlike(rnd, P), set_mixed(rnd), set_words(rnd, P)]
    seen = set()
    for s in sets:
        assert len(s["items"]) == 20, (s["title"], len(s["items"]))
        assert sorted(it["a"] for it in s["items"]) == sorted([0, 1, 2, 3] * 5), s["title"]
        for it in s["items"]:
            assert len(set(it["c"])) == 4, it
            assert it["q"] not in seen, it["q"]
            seen.add(it["q"])
    return {
        "country": "ca-on", "subject": "math", "grade": "grade-6", "slug": "adding-and-subtracting-fractions", "sort": 4,
        "updated": UPDATED, "pdf_url": "",
        "title": "Adding and Subtracting Fractions",
        "seo_title": "Grade 6 Adding and Subtracting Fractions Worksheets: Free Math with Answer Key (Ontario Curriculum)",
        "short_title": "Adding and subtracting fractions",
        "domain": "Number",
        "standard_code": "Grade 6: Number, B2",
        "standard_url": "https://www.dcp.edu.gov.on.ca/en/curriculum/elementary-mathematics",
        "standard_text": "Use tools to add and subtract fractions, including fractions with unlike denominators, in various contexts",
        "meta_desc": "Free Grade 6 math worksheets on adding and subtracting fractions for the Ontario curriculum: like, related and unlike denominators, fraction bars, number lines, mixed numbers with regrouping and word problems. 100 questions with an answer key, great for EQAO practice.",
        "key_big": "Add or subtract fractions only when the parts are the same size: use a common denominator, then add or subtract the numerators.",
        "key_sub": "3/8 + 2/8 = 5/8 (keep the denominator). 1/3 + 1/4 = 4/12 + 3/12 = 7/12, not 2/7. With mixed numbers, regroup 1 whole when the first fraction is smaller.",
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
