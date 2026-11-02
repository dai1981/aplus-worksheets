# -*- coding: utf-8 -*-
"""
UK Year 6 Maths: Simplifying and comparing fractions
(National Curriculum in England, Year 6: Fractions (including decimals and percentages))
  python3 tools/gen_uk_maths_y6_simplify_compare_fractions.py
Simplify with the highest common factor, improper fractions and mixed numbers, common
denominators (lowest common multiple), compare and order fractions including fractions > 1
(number lines), and word problems.
Every choice carries its value; a wrong choice never equals the right value or another wrong one.
Every comparison and order is checked in code with exact fractions.
HTML attributes use single quotes (no backslashes in the JSON). British English.
"""
import json, math, os, random, re, itertools
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "uk", "maths", "year-6")
SLUG = "simplifying-and-comparing-fractions"
UPDATED = "2026-11-02"
FILL = "#4fae74"
FILL2 = "#f2b84b"
RED = "#c0392b"
BLUE = "#2f6db5"
LINE = "#2b2b2b"
THIN = "#8a8a8a"
SYM = {"<": "&lt;", ">": "&gt;", "=": "="}
CANT = "You can’t tell"


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


def Nc(n, unit="", pre=""):
    return ("%s%s%s" % (pre, "{:,}".format(n), unit), F(n))


def lcm(a, b):
    return a * b // math.gcd(a, b)


def show(v, mixed=False):
    """HTML for a Fraction: a/b, or a mixed number when mixed and v > 1."""
    if mixed and v > 1 and v.denominator > 1:
        return mx(v.numerator // v.denominator, v.numerator % v.denominator, v.denominator)
    if v.denominator == 1:
        return str(v.numerator)
    return fr(v.numerator, v.denominator)


def factors(n):
    return [k for k in range(1, n + 1) if n % k == 0]


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


def mark_large(u, pattern):
    """Tag pictures that must print larger so their labels stay readable."""
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
            "<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='1.5'/>"
            "<text x='%.1f' y='%.1f' font-size='%d' font-weight='700' fill='%s' text-anchor='middle'>%s</text>"
            % (x, y, size, color, a, x - w / 2, y + 4, x + w / 2, y + 4, color, x, y + size + 4, size, color, b))


def group_bar(x0, y, W, H, n, k, g):
    """Bar of n thin parts, first k shaded, a thick line after every g parts."""
    s = []
    for i in range(n):
        s.append("<rect x='%.1f' y='%.1f' width='%.2f' height='%d' fill='%s' stroke='none'/>"
                 % (x0 + i * W / n, y, W / n, H, FILL if i < k else "#fff"))
    for i in range(1, n):
        xx = x0 + i * W / n
        thick = (i % g == 0)
        s.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='%s'%s/>"
                 % (xx, y, xx, y + H, LINE if thick else THIN, "3" if thick else "1.5",
                    "" if thick else " stroke-dasharray='4 3'"))
    s.append("<rect x='%.1f' y='%.1f' width='%.1f' height='%d' fill='none' stroke='%s' stroke-width='3'/>" % (x0, y, W, H, LINE))
    return "".join(s)


def group_bar_svg(n, k, g, W=280, H=40):
    return svg_wrap(W + 12, H + 12, group_bar(6, 6, W, H, n, k, g),
                    "fraction bar of %d equal parts with %d shaded, thick lines around groups of %d" % (n, k, g))


def cd_bars_svg(a, b, c, d, W=300, H=38):
    """Two bars cut into L = lcm(b, d) thin parts; thick lines show b parts (top) and d parts (bottom)."""
    L = lcm(b, d)
    LW = 40
    s = []
    for row, (num, den) in enumerate([(a, b), (c, d)]):
        y = 6 + row * (H + 14)
        s.append(sfr(6 + LW / 2 - 2, y + 15, num, den))
        s.append(group_bar(6 + LW, y, W, H, L, num * L // den, L // den))
    return svg_wrap(W + LW + 12, 2 * H + 26, "".join(s),
                    "two fraction bars of the same size cut into %d equal parts, showing %d/%d and %d/%d" % (L, a, b, c, d))


def wholes_svg(d, N, cell=30, H=40, gap=14):
    """N parts of 1/d shaded across bars of d parts, side by side."""
    nb = -(-N // d)
    bw = cell * d
    s = []
    for b in range(nb):
        x0 = 6 + b * (bw + gap)
        k = min(d, N - b * d)
        s.append(group_bar(x0, 6, bw, H, d, k, d))
    return svg_wrap(12 + nb * bw + (nb - 1) * gap, H + 12, "".join(s),
                    "bars of %d equal parts, %d bars, %d parts shaded" % (d, nb, N))


def tick_line(L, d, Y, x0, x1, labels=True):
    s = ["<line x1='%.1f' y1='%d' x2='%.1f' y2='%d' stroke='%s' stroke-width='2.5'/>" % (x0, Y, x1, Y, LINE)]
    n = L * d
    for i in range(n + 1):
        X = x0 + (x1 - x0) * i / n
        whole = (i % d == 0)
        s.append("<line x1='%.1f' y1='%d' x2='%.1f' y2='%d' stroke='%s' stroke-width='%s'/>"
                 % (X, Y - (11 if whole else 7), X, Y + (11 if whole else 7), LINE, "2.5" if whole else "1.6"))
        if whole and labels:
            s.append("<text x='%.1f' y='%d' font-size='16' font-weight='700' fill='%s' text-anchor='middle'>%d</text>"
                     % (X, Y + 30, LINE, i // d))
    return "".join(s)


def letters_line_svg(L, d, pts, W=380):
    """Number line 0..L in steps of 1/d with letters A-D above the points pts (sorted)."""
    x0, x1 = 16, W - 16
    Y = 44
    s = [tick_line(L, d, Y, x0, x1)]
    for i, v in enumerate(pts):
        X = x0 + (x1 - x0) * float(v) / L
        s.append("<path d='M%.1f %d L%.1f %d L%.1f %d Z' fill='%s'/>" % (X - 6, Y - 18, X + 6, Y - 18, X, Y - 9, BLUE))
        s.append("<text x='%.1f' y='%d' font-size='17' font-weight='700' fill='%s' text-anchor='middle'>%s</text>"
                 % (X, Y - 22, BLUE, "ABCD"[i]))
    return svg_wrap(W, Y + 38, "".join(s),
                    "number line from 0 to %d with each whole split into %d equal parts and letters A, B, C and D marked" % (L, d))


def two_lines_svg(L, p, q, W=380):
    """Lesson: two number lines 0..L, top in steps of 1/p.denominator with a dot at p, bottom likewise for q."""
    x0, x1 = 60, W - 16
    s = []
    for row, (v, col) in enumerate([(p, RED), (q, BLUE)]):
        Y = 26 + row * 70
        s.append(sfr(28, Y - 4, v.numerator, v.denominator, 15, col))
        s.append(tick_line(L, v.denominator, Y, x0, x1))
        s.append("<circle cx='%.1f' cy='%d' r='7' fill='%s'/>" % (x0 + (x1 - x0) * float(v) / L, Y, col))
    return svg_wrap(W, 26 + 70 + 38, "".join(s),
                    "two number lines from 0 to %d with dots at %s and %s" % (L, p, q))


# ============================================================ set 1: simplify
def simp_cands(n, d):
    h = math.gcd(n, d)
    sn, sd = n // h, d // h
    c = [Fc(sd, sn), Fc(sn, d - n + sn), Fc(sn, d), Fc(n, sd)]
    for f in factors(d):
        if f not in (1, h, d):
            c.append(Fc(sn, d // f))
    c.append(Fc(sn + 1, sd))
    return c


def simp_e(n, d):
    h = math.gcd(n, d)
    sn, sd = n // h, d // h
    return ("The highest common factor of %d and %d is %d. Divide both numbers by %d: %d ÷ %d = %d and %d ÷ %d = %d. "
            "So %s = <b>%s</b>. %d and %d have no common factor except 1, so it is fully simplified."
            % (n, d, h, h, n, h, sn, d, h, sd, fr(n, d), fr(sn, sd), sn, sd))


def set_simplify(rnd):
    SPOTS.left = []
    its = []
    for n, d, g in [(6, 8, 2), (4, 10, 2), (6, 9, 3)]:
        sn, sd = n // g, d // g
        q = (fig(group_bar_svg(d, n, g)) + "%s of the bar is shaded. The thick lines split it into groups of %d. "
             "Write %s in its simplest form." % (fr(n, d), g, fr(n, d)))
        e = ("There are %d groups and %d of them are shaded, so %s = <b>%s</b>. "
             "This is the same as dividing %d and %d by %d." % (sd, sn, fr(n, d), fr(sn, sd), n, d, g))
        its.append(mcq(q, Fc(sn, sd), simp_cands(n, d), e, rnd))

    for a, b, wrong in [(18, 24, [2, 3, 12, 72]), (12, 30, [2, 3, 60, 4]), (16, 40, [4, 2, 80, 16]), (27, 36, [3, 108, 12, 4])]:
        h = math.gcd(a, b)
        fa, fb = factors(a), factors(b)
        e = ("Factors of %d: %s. Factors of %d: %s. The common factors are %s, and the highest is <b>%d</b>."
             % (a, ", ".join(map(str, fa)), b, ", ".join(map(str, fb)),
                ", ".join(str(x) for x in fa if x in fb), h))
        its.append(mcq("What is the highest common factor of %d and %d?" % (a, b), Nc(h), [Nc(x) for x in wrong], e, rnd))

    for n, d in [(18, 24), (12, 16), (15, 20), (10, 25), (14, 21), (24, 36), (16, 40), (21, 28), (30, 45), (20, 12)]:
        e = simp_e(n, d)
        if n > d:
            e += " (It is still more than 1, so the numerator stays bigger than the denominator.)"
        its.append(mcq("Write %s in its simplest form." % fr(n, d), Fc(n // math.gcd(n, d), d // math.gcd(n, d)),
                       simp_cands(n, d), e, rnd))

    for good, others in [((5, 8), [(6, 9), (4, 10), (9, 12)]), ((7, 12), [(8, 14), (10, 15), (3, 9)]),
                         ((9, 16), [(6, 14), (15, 25), (12, 22)])]:
        assert math.gcd(*good) == 1 and all(math.gcd(*o) > 1 for o in others)
        bits = []
        for a, b in others:
            h = math.gcd(a, b)
            bits.append("%s = %s (÷ %d)" % (fr(a, b), fr(a // h, b // h), h))
        e = ("%d and %d have no common factor except 1, so <b>%s</b> is in its simplest form. The others can be simplified: %s."
             % (good[0], good[1], fr(*good), "; ".join(bits)))
        its.append(mcq("Which fraction is in its simplest form?", Fc(*good), [Fc(*o) for o in others], e, rnd))
    assert len(its) == 20, len(its)
    return {"title": "Simplify fractions using the highest common factor", "items": its}


# ============================================================ set 2: improper fractions and mixed numbers
def imp_cands(n, d):
    q, r = divmod(n, d)
    c = []
    if r:
        c.append(Mc(r, q, d))
    c += [Mc(q, r, n), Mc(q + 1, r, d), Mc(q, d - r, d), Mc(q - 1, r, d), Fc(d, n)]
    return c


def imp_e(n, d, simplify=False):
    q, r = divmod(n, d)
    t = ("How many %ds go into %d? %d × %d = %d, so there are %d wholes. %d − %d = %d %s left over. "
         % (d, n, q, d, q * d, q, n, q * d, r, "is" if r == 1 else "are"))
    if simplify:
        h = math.gcd(r, d)
        return t + ("So %s = %s. Simplify the fraction part: %s = %s (÷ %d). So the answer is <b>%s</b>."
                    % (fr(n, d), mx(q, r, d), fr(r, d), fr(r // h, d // h), h, mx(q, r // h, d // h)))
    return t + "So %s = <b>%s</b>." % (fr(n, d), mx(q, r, d))


def mix_e(w, n, d):
    return ("Each whole is %s, so %d wholes are %d × %d = %d %s. Add the %d: %d + %d = %d. So %s = <b>%s</b>."
            % (fr(d, d), w, w, d, w * d, "parts", n, w * d, n, w * d + n, mx(w, n, d), fr(w * d + n, d)))


def mix_cands(w, n, d):
    return [Fc(w * n, d), Fc(w + n, d), Fc(w * d + n, w * d), Fc(n * d + w, d), Fc(w * d + n + 1, d), Fc(w * d, d + n)]


def set_mixed(rnd):
    SPOTS.left = []
    its = []
    for d, N in [(4, 11), (3, 7)]:
        q, r = divmod(N, d)
        e = ("Each bar is 1 whole. %d bars are full and %d more %s shaded in the last bar. So it shows %s = <b>%s</b>."
             % (q, r, "part is" if r == 1 else "parts are", fr(N, d), mx(q, r, d)))
        its.append(mcq(fig(wholes_svg(d, N)) + "Each bar is 1 whole. Write the shaded amount as a mixed number.",
                       Mc(q, r, d), [Fc(N, d * (q + 1)), Mc(r, q, d)] + imp_cands(N, d), e, rnd))

    for n, d in [(17, 5), (11, 4), (23, 6), (19, 8), (29, 10), (13, 3), (31, 7)]:
        q, r = divmod(n, d)
        its.append(mcq("Write %s as a mixed number." % fr(n, d), Mc(q, r, d), imp_cands(n, d), imp_e(n, d), rnd))
    for n, d in [(14, 4), (22, 8)]:
        q, r = divmod(n, d)
        h = math.gcd(r, d)
        its.append(mcq("Write %s as a mixed number in its simplest form." % fr(n, d), Mc(q, r // h, d // h),
                       [Mc(q, r // h, d), Mc(q, r, n), Mc(q + 1, r // h, d // h)],
                       imp_e(n, d, True), rnd))

    for w, n, d in [(2, 3, 5), (3, 1, 4), (4, 2, 3), (5, 3, 8), (2, 7, 10), (6, 1, 2), (3, 5, 6)]:
        its.append(mcq("Write %s as an improper fraction." % mx(w, n, d), Fc(w * d + n, d), mix_cands(w, n, d),
                       mix_e(w, n, d), rnd))

    its.append(mcq("3 %s = %s" % (fr(1, 4), fr("<b>?</b>", 4)), Nc(13), [Nc(4), Nc(12), Nc(7), Nc(3)],
                   "3 wholes = 3 × 4 = 12 quarters. Add 1 more quarter: 12 + 1 = <b>13</b>. So 3 %s = %s."
                   % (fr(1, 4), fr(13, 4)), rnd))
    its.append(mcq("%s = <b>?</b> %s" % (fr(47, 8), fr(7, 8)), Nc(5), [Nc(6), Nc(4), Nc(39)],
                   "8 × 5 = 40 and 47 − 40 = 7. So %s = <b>5</b> %s." % (fr(47, 8), fr(7, 8)), rnd))
    assert len(its) == 20, len(its)
    return {"title": "Improper fractions and mixed numbers", "items": its}


# ============================================================ set 3: common denominators
def pair(a, b, c, d):
    return "%s and %s" % (fr(a, b), fr(c, d))


def set_common(rnd):
    SPOTS.left = []
    its = []
    for a, b, wrong in [(4, 6, [24, 2, 10]), (6, 8, [48, 2, 14, 12]), (3, 5, [8, 30, 35]), (9, 12, [108, 3, 21, 24])]:
        L = lcm(a, b)
        ma = [a * k for k in range(1, L // a + 1)]
        mb = [b * k for k in range(1, L // b + 1)]
        e = ("Multiples of %d: %s, … Multiples of %d: %s, … The first number in both lists is <b>%d</b>."
             % (a, ", ".join(map(str, ma)), b, ", ".join(map(str, mb)), L))
        if L < a * b:
            e += " %d × %d = %d is a common multiple too, but it is not the lowest." % (a, b, a * b)
        its.append(mcq("What is the lowest common multiple of %d and %d?" % (a, b), Nc(L), [Nc(x) for x in wrong], e, rnd))

    for a, b, d in [(3, 5, 20), (2, 3, 12), (5, 6, 18), (7, 8, 24), (4, 9, 36)]:
        k = d // b
        c = a * k
        e = ("%d × <b>%d</b> = %d, so multiply the numerator by %d too: %d × %d = <b>%d</b>. So %s = %s."
             % (b, k, d, k, a, k, c, fr(a, b), fr(c, d)))
        its.append(mcq("%s = %s" % (fr(a, b), fr("<b>?</b>", d)), Nc(c), [Nc(a + (d - b)), Nc(a), Nc(k), Nc(d - c)], e, rnd))
    its.append(mcq("%s = %s" % (fr(3, 4), fr(15, "<b>?</b>")), Nc(20), [Nc(16), Nc(4), Nc(60), Nc(19)],
                   "3 × <b>5</b> = 15, so multiply the denominator by 5 too: 4 × 5 = <b>20</b>. So %s = %s." % (fr(3, 4), fr(15, 20)), rnd))

    for a, b, c, d in [(2, 3, 3, 4), (1, 2, 3, 5), (3, 4, 5, 6), (1, 3, 5, 12), (5, 6, 7, 9), (3, 8, 1, 6), (2, 5, 3, 10)]:
        L = lcm(b, d)
        A, C = a * L // b, c * L // d
        right = pair(A, L, C, L)
        wr = [pair(a, L, c, L), pair(a * (L // d), L, c * (L // b), L),
              pair(a + L - b, L, c + L - d, L) if a + L - b != c + L - d else pair(C, L, A, L)]
        parts = []
        for num, den, cc in [(a, b, A), (c, d, C)]:
            k = L // den
            parts.append("%s = %s (× %d)" % (fr(num, den), fr(cc, L), k) if k > 1 else "%s stays %s" % (fr(num, den), fr(cc, L)))
        e = ("The lowest common multiple of %d and %d is %d, so use %d as the denominator. "
             "Multiply the numerator and the denominator by the same number: %s. Answer: <b>%s</b>."
             % (b, d, L, L, "; ".join(parts), right))
        its.append(mcq("Write %s and %s as fractions with the lowest common denominator." % (fr(a, b), fr(c, d)),
                       right, wr, e, rnd))

    for b, d, right, wrong in [(4, 6, 12, [10, 18, 8]), (3, 8, 24, [11, 16, 32]), (5, 4, 20, [9, 15, 25])]:
        for w in wrong:
            assert w % b or w % d
        e = ("A common denominator must be in the %d times table <b>and</b> the %d times table. %d = %d × %d = %d × %d. "
             "%s" % (b, d, right, b, right // b, d, right // d,
                     "%d is the sum of %d and %d, which does not work." % (b + d, b, d) if b + d in wrong else ""))
        its.append(mcq("Which number could be a common denominator for %s and %s?" % (fr(1, b), fr(1, d)),
                       Nc(right), [Nc(w) for w in wrong], e.strip(), rnd))
    assert len(its) == 20, len(its)
    return {"title": "Write fractions with a common denominator", "items": its}


# ============================================================ set 4: compare and order
def cmp_e(vals, mixed_flags=None):
    """Explain by writing all values over their lowest common denominator."""
    L = 1
    for v in vals:
        L = lcm(L, v.denominator)
    bits = []
    for i, v in enumerate(vals):
        bits.append("%s = %s" % (show(v, mixed_flags and mixed_flags[i]), fr(v * L, L) if v.denominator != L or True else ""))
    return L, "Use the common denominator %d: %s." % (L, ", ".join(bits))


def nl_item(t, L, d, cands, mixed, rnd):
    pos = SPOTS.next(rnd)
    lo = [c for c in cands if c < t]
    hi = [c for c in cands if c > t]
    pts = sorted(lo[:pos] + [t] + hi[:3 - pos])
    assert len(pts) == 4 and len(set(pts)) == 4, (t, pts)
    for v in pts:
        assert (v * d).denominator == 1 and 0 < v < L
    letter = "ABCD"[pts.index(t)]
    w = int(t)
    r = (t - w) * d
    e = ("Each whole is split into %d equal parts, so each mark is %s. " % (d, fr(1, d)))
    if mixed:
        e += "Count %d whole%s, then %d more mark%s. That is letter <b>%s</b>." % (w, "" if w == 1 else "s", r, "" if r == 1 else "s", letter)
        name = mx(w, int(r), d)
    else:
        e += ("%s = %s: go to %d, then %d more mark%s. That is letter <b>%s</b>."
              % (fr(t.numerator, d), mx(w, int(r), d), w, r, "" if r == 1 else "s", letter))
        name = fr(t.numerator, d)
    q = fig(letters_line_svg(L, d, pts)) + "Which letter shows %s?" % name
    return {"q": q, "c": ["A", "B", "C", "D"], "a": pts.index(t), "e": e}


def over(v, L):
    return fr((v * L).numerator, L)


def set_compare(rnd):
    SPOTS.left = []
    its = []
    # number lines (letters fixed in A-D order)
    for t, L, d, mixed in [(F(7, 4), 3, 4, False), (F(5, 3), 3, 3, True), (F(9, 4), 3, 4, True),
                           (F(7, 5), 3, 5, False), (F(11, 6), 3, 6, False)]:
        cands = [t - 1, t + F(1, d), t - F(1, d), t + F(2, d), t - F(2, d), t - F(3, d), t + F(3, d), t - F(4, d)]
        cands = [c for c in cands if 0 < c < L]
        its.append(nl_item(t, L, d, cands, mixed, rnd))

    # greatest / smallest / between
    def lcd(vs):
        L = 1
        for v in vs:
            L = lcm(L, v.denominator)
        return L
    for word, vs, disp in [
        ("greatest", [F(3, 4), F(5, 8), F(2, 3), F(7, 12)], None),
        ("smallest", [F(5, 6), F(7, 9), F(3, 4), F(2, 3)], None),
        ("smallest", [F(5, 12), F(3, 8), F(1, 3), F(7, 24)], None),
    ]:
        best = max(vs) if word == "greatest" else min(vs)
        L = lcd(vs)
        e = ("Write them all with the denominator %d: %s. The %s is %s, so the answer is <b>%s</b>."
             % (L, ", ".join("%s = %s" % (show(v), over(v, L)) for v in vs), word, over(best, L), show(best)))
        its.append(mcq("Which fraction is the %s?" % word, (show(best), best),
                       [(show(v), v) for v in vs if v != best], e, rnd))
    vs = [F(7, 4), F(5, 3), F(9, 5), F(13, 8)]
    best = max(vs)
    e = ("All four are between 1 and 2. Look at how much each one is short of 2: "
         "%s = 1 %s (%s short), 1 %s (%s short), %s = 1 %s (%s short), 1 %s (%s short). "
         "The smallest gap is %s, so <b>%s</b> is the greatest."
         % (fr(7, 4), fr(3, 4), fr(1, 4), fr(2, 3), fr(1, 3), fr(9, 5), fr(4, 5), fr(1, 5), fr(5, 8), fr(3, 8),
            fr(1, 5), fr(9, 5)))
    its.append(mcq("Which number is the greatest?", Fc(9, 5), [Fc(7, 4), Mc(1, 2, 3), Mc(1, 5, 8)], e, rnd))
    assert F(1, 2) < F(5, 8) < F(3, 4) and not F(1, 2) < F(7, 8) < F(3, 4) and not F(1, 2) < F(4, 5) < F(3, 4)
    its.append(mcq("Which fraction is between %s and %s?" % (fr(1, 2), fr(3, 4)), Fc(5, 8), [Fc(7, 8), Fc(3, 8), Fc(4, 5)],
                   "In eighths: %s = %s and %s = %s. <b>%s</b> is between them. %s and %s are more than %s, and %s is less than %s."
                   % (fr(1, 2), fr(4, 8), fr(3, 4), fr(6, 8), fr(5, 8), fr(7, 8), fr(4, 5), fr(3, 4), fr(3, 8), fr(1, 2)), rnd))

    # ordering
    for items in [
        [(F(2, 3), False), (F(5, 6), False), (F(7, 12), False)],
        [(F(3, 5), False), (F(1, 2), False), (F(7, 10), False)],
        [(F(3, 2), False), (F(5, 4), False), (F(4, 3), True)],
        [(F(9, 4), False), (F(7, 3), True), (F(13, 6), False)],
    ]:
        def s_of(perm):
            return ", ".join(show(v, m) for v, m in perm)
        right = sorted(items, key=lambda x: x[0])
        perms = [sorted(items, key=lambda x: x[0].numerator if not x[1] else x[0].numerator % x[0].denominator),
                 sorted(items, key=lambda x: x[0].denominator),
                 sorted(items, key=lambda x: -x[0].denominator),
                 list(reversed(right))]
        perms += [list(p) for p in itertools.permutations(items)]
        vs = [v for v, _ in items]
        L = lcd(vs)
        e = ("Use the common denominator %d: %s. So the order is <b>%s</b>."
             % (L, ", ".join("%s = %s" % (show(v, m), over(v, L)) for v, m in items), s_of(right)))
        its.append(mcq("Order from smallest to largest:<br>%s" % s_of(items), s_of(right),
                       [s_of(p) for p in perms], e, rnd))

    # which statement is true (a (num, den) tuple is shown as written, not simplified)
    def val(x):
        return F(*x) if isinstance(x, tuple) else x

    def sh(x, m):
        return fr(*x) if isinstance(x, tuple) else show(x, m)
    def st(x, op, y, mx_=(False, False)):
        txt = "%s %s %s" % (sh(x, mx_[0]), SYM[op], sh(y, mx_[1]))
        x, y = val(x), val(y)
        truth = {"<": x < y, ">": x > y, "=": x == y}[op]
        return txt, truth
    for true, falses in [
        ((F(5, 4), "<", F(4, 3), (False, True)), [(F(1, 8), ">", F(1, 6)), (F(4, 9), ">", F(3, 5)), (F(2, 3), "=", F(3, 4))]),
        ((F(7, 8), ">", F(5, 6)), [(F(3, 10), ">", F(3, 7)), (F(7, 3), "<", F(2)), (F(3, 5), "=", (4, 6))]),
        ((F(3, 5), "<", F(5, 8)), [(F(5, 12), ">", F(4, 7)), (F(9, 4), ">", F(5, 2), (False, True)), (F(2, 9), ">", F(2, 5))]),
        ((F(12, 5), ">", F(9, 4), (True, False)), [(F(11, 8), ">", F(3, 2), (False, True)), (F(3, 4), "<", F(5, 8)), (F(5, 12), ">", F(5, 8))]),
        (((4, 6), "=", (10, 15)), [(F(7, 10), ">", F(5, 6)), (F(5, 2), "<", F(9, 4), (False, True)), (F(6, 11), ">", F(4, 5))]),
        ((F(11, 6), "<", F(15, 8), (False, True)), [(F(9, 4), "=", F(3, 4)), (F(5, 7), ">", F(3, 4)), (F(7, 12), "<", F(1, 2))]),
    ]:
        tt, ok = st(*true)
        assert ok, tt
        fs = []
        for f in falses:
            t2, ok2 = st(*f)
            assert not ok2, t2
            fs.append(t2)
        x, op, y = true[0], true[1], true[2]
        mflags = true[3] if len(true) > 3 else (False, False)
        xs, ys = sh(x, mflags[0]), sh(y, mflags[1])
        x, y = val(x), val(y)
        L = lcm(x.denominator, y.denominator)
        e = ("Use the common denominator %d: %s = %s and %s = %s. So <b>%s</b> is true."
             % (L, xs, over(x, L), ys, over(y, L), tt))
        if op == "=":
            e = ("Simplify both: %s = %s (÷ %d) and %s = %s (÷ %d). They are equal, so <b>%s</b> is true."
                 % (xs, show(x), true[0][0] // x.numerator, ys, show(y), true[2][0] // y.numerator, tt))
        its.append(mcq("Which statement is true?", tt, fs, e, rnd))
    # nl items used the shared SPOTS; mcq items too
    assert len(its) == 20, len(its)
    return {"title": "Compare and order fractions, including fractions greater than 1", "items": its}


# ============================================================ set 5: word problems
def set_words(rnd):
    SPOTS.left = []
    its = []
    # 1
    its.append(mcq("Oliver eats %s of a pizza. Amelia eats %s of a pizza of the same size. Who eats more?" % (fr(3, 8), fr(1, 3)),
                   "Oliver", ["Amelia", "They eat the same", CANT],
                   "Use 24ths: %s = %s and %s = %s. 9 is more than 8, so <b>Oliver</b> eats more."
                   % (fr(3, 8), fr(9, 24), fr(1, 3), fr(8, 24)), rnd))
    # 2
    assert F(18, 30) < F(14, 20)
    its.append(mcq("In Class 6A, 18 of the 30 pupils bring a packed lunch. In Class 6B, 14 of the 20 pupils bring a packed lunch. "
                   "Which class has the greater fraction of pupils with a packed lunch?",
                   "Class 6B", ["Class 6A", "They are the same", CANT],
                   "Class 6A: %s = %s = %s. Class 6B: %s = %s. %s is more than %s, so <b>Class 6B</b>. "
                   "Class 6A has more pupils, but a smaller fraction of them."
                   % (fr(18, 30), fr(3, 5), fr(6, 10), fr(14, 20), fr(7, 10), fr(7, 10), fr(6, 10)), rnd))
    # 3
    its.append(mcq("24 of the 32 pupils in Year 6 went on the school trip. What fraction of the pupils went? "
                   "Give your answer in its simplest form.", Fc(3, 4), [Fc(1, 4), Fc(4, 3), Fc(3, 11), Fc(3, 32)],
                   "The fraction is %s. The highest common factor of 24 and 32 is 8: 24 ÷ 8 = 3 and 32 ÷ 8 = 4. "
                   "So <b>%s</b> of the pupils went." % (fr(24, 32), fr(3, 4)), rnd))
    # 4
    its.append(mcq("Flour comes in bags of %s kg. How many bags make 2 %s kg?" % (fr(1, 4), fr(3, 4)),
                   Nc(11, " bags"), [Nc(6, " bags"), Nc(5, " bags"), Nc(8, " bags")],
                   "Each whole kilogram is 4 bags, so 2 kg is 2 × 4 = 8 bags. Add 3 more bags for %s kg: 8 + 3 = <b>11 bags</b>. "
                   "(2 %s = %s.)" % (fr(3, 4), fr(3, 4), fr(11, 4)), rnd))
    # 5
    its.append(mcq("Harry runs %s km. Write this distance as a mixed number." % fr(13, 4),
                   Mc(3, 1, 4, " km"), [Mc(1, 3, 4, " km"), Mc(3, 1, 13, " km"), Mc(4, 1, 3, " km")],
                   "4 × 3 = 12 and 13 − 12 = 1. So %s km = <b>3 %s km</b>." % (fr(13, 4), fr(1, 4)), rnd))
    # 6
    rib = [("Isla", F(5, 6)), ("Jack", F(7, 9)), ("Poppy", F(3, 4)), ("Arjun", F(2, 3))]
    assert max(rib, key=lambda x: x[1])[0] == "Isla"
    its.append(mcq("Four children measure their ribbons. Isla: %s m. Jack: %s m. Poppy: %s m. Arjun: %s m. "
                   "Who has the longest ribbon?" % (fr(5, 6), fr(7, 9), fr(3, 4), fr(2, 3)),
                   "Isla", ["Jack", "Poppy", "Arjun"],
                   "Use the common denominator 36: %s = %s, %s = %s, %s = %s, %s = %s. The longest is <b>Isla’s</b>."
                   % (fr(5, 6), fr(30, 36), fr(7, 9), fr(28, 36), fr(3, 4), fr(27, 36), fr(2, 3), fr(24, 36)), rnd))
    # 7
    its.append(mcq("Bottle A holds 1 %s litres of water. Bottle B holds %s litres. Which bottle holds more?" % (fr(1, 4), fr(7, 5)),
                   "Bottle B", ["Bottle A", "They hold the same", CANT],
                   "%s = 1 %s. Compare %s and %s using twentieths: %s and %s. So <b>Bottle B</b> holds more."
                   % (fr(7, 5), fr(2, 5), fr(1, 4), fr(2, 5), fr(5, 20), fr(8, 20)), rnd))
    # 8
    its.append(mcq("Ruby says, “%s is greater than %s, because 4 is greater than 3.” Is she right?" % (fr(4, 9), fr(3, 5)),
                   "No. %s is less than %s" % (fr(4, 9), fr(3, 5)),
                   ["Yes. 4 is greater than 3", "Yes. Ninths are bigger than fifths", "No. They are equal"],
                   "You cannot compare only the numerators when the denominators are different. Use 45ths: "
                   "%s = %s and %s = %s. So %s is <b>less</b> than %s." % (fr(4, 9), fr(20, 45), fr(3, 5), fr(27, 45), fr(4, 9), fr(3, 5)), rnd))
    # 9
    its.append(mcq("Ethan simplified %s and wrote %s. What did he do wrong?" % (fr(20, 30), fr(10, 20)),
                   "He took 10 away from the top and the bottom",
                   ["He divided by the highest common factor", "Nothing. He is right", "He divided only the numerator by 2"],
                   "20 − 10 = 10 and 30 − 10 = 20. Subtracting changes the value: %s = %s, not %s. "
                   "Divide by the highest common factor, 10: %s = <b>%s</b>." % (fr(10, 20), fr(1, 2), fr(2, 3), fr(20, 30), fr(2, 3)), rnd))
    # 10
    its.append(mcq("Kai says 3 %s = %s. What is the correct improper fraction?" % (fr(2, 5), fr(6, 5)),
                   Fc(17, 5), [Fc(6, 5), Fc(17, 15), Fc(13, 5)],
                   "Kai multiplied 3 × 2. Instead, 3 wholes = 3 × 5 = 15 fifths. Add 2 fifths: 15 + 2 = 17. So 3 %s = <b>%s</b>."
                   % (fr(2, 5), fr(17, 5)), rnd))
    # 11
    assert F(7, 12) < F(5, 8)
    its.append(mcq("The Reds football team won 7 of their 12 matches. The Blues won 5 of their 8 matches. "
                   "Which team won the greater fraction of their matches?", "The Blues",
                   ["The Reds", "They are the same", CANT],
                   "Use 24ths: Reds %s = %s, Blues %s = %s. 15 is more than 14, so <b>the Blues</b>. "
                   "The Reds won more matches, but they also played more." % (fr(7, 12), fr(14, 24), fr(5, 8), fr(15, 24)), rnd))
    # 12
    walk = [("Lily", F(3, 2)), ("George", F(7, 4)), ("Maya", F(7, 5)), ("Zara", F(8, 5))]
    assert max(walk, key=lambda x: x[1])[0] == "George"
    its.append(mcq("Lily lives 1 %s km from school, George %s km, Maya 1 %s km and Zara 1 %s km. Who lives furthest from school?"
                   % (fr(1, 2), fr(7, 4), fr(2, 5), fr(3, 5)),
                   "George", ["Lily", "Maya", "Zara"],
                   "%s = 1 %s. Compare the fraction parts with the denominator 20: %s = %s, %s = %s, %s = %s, %s = %s. "
                   "The largest is %s, so <b>George</b> lives furthest."
                   % (fr(7, 4), fr(3, 4), fr(1, 2), fr(10, 20), fr(3, 4), fr(15, 20), fr(2, 5), fr(8, 20), fr(3, 5), fr(12, 20),
                      fr(15, 20)), rnd))
    # 13
    its.append(mcq("There are 36 pupils on a coach. 27 of them are in Year 6. What fraction of the pupils are in Year 6, in its simplest form?",
                   Fc(3, 4), [Fc(1, 4), Fc(4, 3), Fc(3, 6), Fc(3, 36)],
                   "The fraction is %s. The highest common factor of 27 and 36 is 9: 27 ÷ 9 = 3 and 36 ÷ 9 = 4. So <b>%s</b>."
                   % (fr(27, 36), fr(3, 4)), rnd))
    # 14
    its.append(mcq("Two cakes are each cut into 12 equal slices. 15 slices are eaten. How many cakes are eaten? "
                   "Give a mixed number in its simplest form.", Mc(1, 1, 4, " cakes"),
                   [Mc(1, 1, 3, " cakes"), Mc(3, 1, 12, " cakes"), Mc(1, 3, 15, " cakes"), Fc(12, 15, " cakes")],
                   "15 slices = %s cakes. 12 slices make 1 whole cake and 3 are left: 1 %s. Simplify: %s = %s (÷ 3). "
                   "So <b>1 %s cakes</b>." % (fr(15, 12), fr(3, 12), fr(3, 12), fr(1, 4), fr(1, 4)), rnd))
    # 15
    its.append(mcq("Charlie reads for %s of an hour. Evie reads for %s of an hour. Who reads for longer?" % (fr(5, 6), fr(3, 4)),
                   "Charlie", ["Evie", "They read for the same time", CANT],
                   "Use 12ths: %s = %s and %s = %s, so <b>Charlie</b> reads for longer. "
                   "(In minutes: 50 minutes and 45 minutes.)" % (fr(5, 6), fr(10, 12), fr(3, 4), fr(9, 12)), rnd))
    # 16
    assert F(3, 8) < F(2, 5)
    its.append(mcq("Freya and Leo get the same pocket money. Freya spends %s of hers and Leo spends %s of his. Who spends more?"
                   % (fr(3, 8), fr(2, 5)), "Leo", ["Freya", "They spend the same", CANT],
                   "Use 40ths: %s = %s and %s = %s. 16 is more than 15, so <b>Leo</b> spends more."
                   % (fr(3, 8), fr(15, 40), fr(2, 5), fr(16, 40)), rnd))
    # 17
    assert F(16, 20) < F(21, 25)
    its.append(mcq("In a spelling test, Mohammed scores 16 out of 20 and Aisha scores 21 out of 25. Who did better?",
                   "Aisha, because %s = %s and %s = %s" % (fr(21, 25), fr(84, 100), fr(16, 20), fr(80, 100)),
                   ["Mohammed, because 20 is less than 25", "They did the same, because both lost 4 or 5 marks",
                    "Mohammed, because %s = %s" % (fr(16, 20), fr(4, 5))],
                   "Write both out of 100: %s = %s (× 5) and %s = %s (× 4). 84 is more than 80, so <b>Aisha</b> did better."
                   % (fr(16, 20), fr(80, 100), fr(21, 25), fr(84, 100)), rnd))
    # 18
    its.append(mcq("A pizza is cut into 6 equal slices. At a party, 19 slices of the same-sized pizzas are eaten. "
                   "How many pizzas is that?", Mc(3, 1, 6, " pizzas"),
                   [Mc(1, 3, 6, " pizzas"), Mc(3, 1, 19, " pizzas"), Mc(4, 1, 6, " pizzas"), Mc(6, 1, 3, " pizzas")],
                   "6 slices make 1 pizza. 3 × 6 = 18, and 19 − 18 = 1 slice is left. So %s = <b>3 %s pizzas</b>."
                   % (fr(19, 6), fr(1, 6)), rnd))
    # 19
    its.append(mcq("Arjun eats %s of a cake. Zara eats %s of the same cake. He writes both fractions as twelfths to compare them. "
                   "What should he write?" % (fr(1, 4), fr(1, 6)),
                   pair(3, 12, 2, 12), [pair(1, 12, 1, 12), pair(2, 12, 3, 12), pair(4, 12, 6, 12)],
                   "4 × 3 = 12, so %s = %s. 6 × 2 = 12, so %s = %s. Answer: <b>%s</b>. Arjun eats more."
                   % (fr(1, 4), fr(3, 12), fr(1, 6), fr(2, 12), pair(3, 12, 2, 12)), rnd))
    # 20
    assert F(12, 28) == F(9, 21)
    its.append(mcq("In Class 6R, 12 of the 28 pupils walk to school. In Class 6T, 9 of the 21 pupils walk to school. "
                   "Which class has the greater fraction of pupils who walk?", "They are the same",
                   ["Class 6R", "Class 6T", CANT],
                   "Simplify both. %s = %s (÷ 4) and %s = %s (÷ 3). The fractions are equal, so <b>they are the same</b>."
                   % (fr(12, 28), fr(3, 7), fr(9, 21), fr(3, 7)), rnd))
    assert len(its) == 20, len(its)
    return {"title": "Fraction word problems and reasoning", "items": its}


# ============================================================ lesson
def body_html():
    return (
        "<h2>Simplifying fractions</h2>"
        "<p>A fraction is in its <b>simplest form</b> when the numerator and the denominator have no common factor except 1. "
        "To simplify, <b>divide both numbers by their highest common factor</b> (HCF). The value does not change.</p>"
        "<figure class='sn-fig'>" + group_bar_svg(8, 6, 2) +
        "<figcaption>" + fr(6, 8) + " is shaded. In groups of 2 there are 4 groups and 3 are shaded, so "
        + fr(6, 8) + " = " + fr(3, 4) + ".</figcaption></figure>"
        + ex("Example", "Write " + fr(18, 24) + " in its simplest form.",
             "Factors of 18: 1, 2, 3, 6, 9, 18. Factors of 24: 1, 2, 3, 4, 6, 8, 12, 24. The HCF is 6. "
             "18 ÷ 6 = 3 and 24 ÷ 6 = 4.", fr(3, 4))
        + "<p>If you divide by a smaller common factor, such as 2, you get " + fr(9, 12) + ". That is correct but not finished: "
        "keep going until there is no common factor left.</p>"
        "<h2>Improper fractions and mixed numbers</h2>"
        "<p>An <b>improper fraction</b> such as " + fr(7, 4) + " is greater than 1. "
        "A <b>mixed number</b> such as 1 " + fr(3, 4) + " shows the same amount as wholes and a fraction.</p>"
        "<figure class='sn-fig'>" + wholes_svg(4, 7) +
        "<figcaption>" + fr(7, 4) + " = 4 quarters (1 whole) and 3 more quarters = 1 " + fr(3, 4) + ".</figcaption></figure>"
        + ex("Example", "Write " + fr(17, 5) + " as a mixed number.",
             "5 goes into 17 three times (15), with 2 left over.", "3 " + fr(2, 5))
        + ex("Example", "Write 2 " + fr(3, 5) + " as an improper fraction.",
             "2 wholes = 2 × 5 = 10 fifths. Add 3 fifths: 10 + 3 = 13.", fr(13, 5))
        + "<h2>Common denominators</h2>"
        "<p>To compare fractions with different denominators, give them the <b>same denominator</b>. "
        "Use the <b>lowest common multiple</b> (LCM) of the denominators.</p>"
        "<figure class='sn-fig'>" + cd_bars_svg(2, 3, 3, 4) +
        "<figcaption>Both bars are cut into twelfths: " + fr(2, 3) + " = " + fr(8, 12) + " and " + fr(3, 4) + " = "
        + fr(9, 12) + ".</figcaption></figure>"
        + ex("Example", "Write " + fr(2, 3) + " and " + fr(3, 4) + " with a common denominator.",
             "The LCM of 3 and 4 is 12. " + fr(2, 3) + " = " + fr(8, 12) + " (× 4) and " + fr(3, 4) + " = " + fr(9, 12) + " (× 3).",
             fr(8, 12) + " and " + fr(9, 12))
        + "<h2>Comparing and ordering</h2>"
        "<p>Once the denominators are the same, compare the numerators. For numbers greater than 1, compare the wholes first, "
        "then the fractions.</p>"
        "<figure class='sn-fig'>" + two_lines_svg(2, F(5, 4), F(4, 3)) +
        "<figcaption>" + fr(5, 4) + " = 1 " + fr(1, 4) + " and 1 " + fr(1, 3) + " = " + fr(4, 3)
        + ". The blue dot is further along, so " + fr(5, 4) + " &lt; 1 " + fr(1, 3) + ".</figcaption></figure>"
        + ex("Example", "Which is greater: " + fr(5, 4) + " or 1 " + fr(1, 3) + "?",
             "Both are 1 and a bit. Compare " + fr(1, 4) + " and " + fr(1, 3) + " using twelfths: "
             + fr(3, 12) + " &lt; " + fr(4, 12) + ".", "1 " + fr(1, 3))
        + "<h2>Common mistakes</h2>"
        + table(["Mistake", "What to do instead"], [
            ["Taking the same number away from the top and bottom: " + fr(20, 30) + " → " + fr(10, 20),
             "Divide both by the HCF: " + fr(20, 30) + " = " + fr(2, 3)],
            ["Thinking a bigger denominator means a bigger fraction: " + fr(1, 8) + " &gt; " + fr(1, 6),
             "A bigger denominator means <b>smaller</b> parts: " + fr(1, 8) + " &lt; " + fr(1, 6)],
            ["Comparing only the numerators: " + fr(4, 9) + " &gt; " + fr(3, 5) + " because 4 &gt; 3",
             "Use a common denominator: " + fr(20, 45) + " &lt; " + fr(27, 45)],
            ["2 " + fr(3, 5) + " = " + fr(6, 5) + " (multiplying 2 × 3)",
             "Wholes × denominator, then add the numerator: 2 × 5 + 3 = 13, so " + fr(13, 5)],
        ])
    )


FAQ = [
    {"q": "How do you simplify fractions in Year 6?",
     "a": "Find the highest common factor of the numerator and denominator, then divide both by it. For 18/24 the highest common factor is 6, so 18/24 = 3/4."},
    {"q": "How do you compare fractions with different denominators?",
     "a": "Write them with a common denominator, using the lowest common multiple of the denominators, then compare the numerators. For 2/3 and 3/4, use twelfths: 8/12 is less than 9/12."},
    {"q": "What is the difference between an improper fraction and a mixed number?",
     "a": "An improper fraction has a numerator bigger than (or equal to) its denominator, such as 7/4. A mixed number shows the same amount as wholes and a fraction, such as 1 3/4."},
    {"q": "Are fractions in the Year 6 SATs?",
     "a": "Yes. Fractions appear in the arithmetic paper and in both reasoning papers, including simplifying, comparing and ordering fractions and solving word problems with them."},
]


def gen():
    rnd = random.Random(6606)
    SPOTS.left = []
    sets = [set_simplify(rnd), set_mixed(rnd), set_common(rnd), set_compare(rnd), set_words(rnd)]
    for s in sets:
        assert len(s["items"]) == 20, (s["title"], len(s["items"]))
        cnt = [0, 0, 0, 0]
        for it in s["items"]:
            assert len(set(it["c"])) == 4, it
            cnt[it["a"]] += 1
        assert cnt == [5, 5, 5, 5], (s["title"], cnt)
    return {
        "country": "uk", "subject": "maths", "grade": "year-6", "slug": SLUG, "sort": 6,
        "updated": UPDATED, "pdf_url": "",
        "title": "Year 6 Simplifying and Comparing Fractions",
        "seo_title": "Year 6 Simplifying and Comparing Fractions Worksheets: Simplest Form, Mixed Numbers, Ordering (Free, with Answers)",
        "short_title": "Simplifying and comparing fractions",
        "domain": "Fractions (including decimals and percentages)",
        "standard_code": "Year 6: Fractions (including decimals and percentages)",
        "standard_url": "https://www.gov.uk/government/publications/national-curriculum-in-england-mathematics-programmes-of-study",
        "standard_text": "Use common factors to simplify fractions; use common multiples to express fractions in the same denomination; compare and order fractions, including fractions > 1.",
        "meta_desc": "Free Year 6 maths worksheets on simplifying and comparing fractions for the National Curriculum: simplest form with the highest common factor, improper fractions and mixed numbers, common denominators, ordering fractions greater than 1 and word problems. 100 questions with an answer key.",
        "key_big": "Simplify by dividing by the highest common factor. Compare by giving the fractions a common denominator.",
        "key_sub": "18/24 = 3/4 (÷ 6). 2/3 and 3/4 become 8/12 and 9/12, so 3/4 is greater. A bigger denominator means smaller parts.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, SLUG + ".json")
    mark_large(u, "(number line|two fraction bars|bars of|fraction bar)")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(u, f, ensure_ascii=False, indent=1)
    print("wrote", path)
