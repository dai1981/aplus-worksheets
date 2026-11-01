# -*- coding: utf-8 -*-
"""
US Grade 4 Math: Compare Fractions (4.NF.A.2)
  python tools/gen_us_math_g4_compare_fractions.py
Grade 4 denominators: 2, 3, 4, 5, 6, 8, 10, 12, 100.
Every comparison, rewrite and order is checked in code with exact fractions.
HTML attributes use single quotes (no backslashes in the JSON).
"""
import json, math, os, random, itertools
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "us", "math", "grade-4")
UPDATED = "2026-11-02"
FILL = "#4fae74"      # shaded part
LINE = "#2b2b2b"
THIN = "#7a7a7a"
RED = "#d6453b"
BLUE = "#2f6db5"
GIRLS = ["Maya", "Ava", "Mia", "Zoe", "Lily", "Emma", "Nora", "Ruby", "Sofia", "Grace", "Ivy", "Chloe"]
BOYS = ["Leo", "Noah", "Eli", "Sam", "Ben", "Omar", "Kai", "Jack", "Luis", "Owen", "Max", "Ryan"]
SYM = {"<": "&lt;", ">": "&gt;", "=": "="}
CANT = "You can’t tell"
PL = {2: "halves", 3: "thirds", 4: "fourths", 5: "fifths", 6: "sixths", 8: "eighths", 10: "tenths",
      12: "twelfths", 24: "24ths", 100: "hundredths"}


# ------------------------------------------------------------ helpers
def fr(a, b):
    return "<span class='fr'><span class='fn'>%d</span><span class='fd'>%d</span></span>" % (a, b)


def mcq(q, correct, cands, e, rnd):
    seen = {correct}
    pick = []
    for c in cands:
        if c in seen or not c:
            continue
        seen.add(c)
        pick.append(c)
        if len(pick) == 3:
            break
    assert len(pick) == 3, (q, correct, cands)
    ch = pick + [correct]
    rnd.shuffle(ch)
    return {"q": q, "c": ch, "a": ch.index(correct), "e": e}


class People:
    def __init__(self, rnd):
        self.pool = [(n, "she", "her") for n in GIRLS] + [(n, "he", "his") for n in BOYS]
        rnd.shuffle(self.pool)
        self.i = 0

    def next(self):
        p = self.pool[self.i % len(self.pool)]
        self.i += 1
        return p


def fig(svg):
    return "<div class='qfig'>" + svg + "</div>"


def svg_wrap(w, h, body, label):
    return ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 %d %d' width='%d' height='%d' "
            "role='img' aria-label='%s'>%s</svg>" % (w, h, w, h, label, body))


def table(head, rows):
    h = "".join("<th>%s</th>" % x for x in head)
    b = "".join("<tr>" + "".join("<td>%s</td>" % c for c in r) + "</tr>" for r in rows)
    return "<div class='sn-tw'><table class='sn-table'><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>" % (h, b)


def ex(title, q, s, a):
    return ("<div class='sn-ex'><span class='sn-ex-t'>%s</span><p class='sn-ex-q'>%s</p>"
            "<p class='sn-ex-s'>%s</p><p class='sn-ex-a'>Answer: %s</p></div>" % (title, q, s, a))


def sign(a, b, c, d):
    x, y = F(a, b), F(c, d)
    return "<" if x < y else (">" if x > y else "=")


def st(a, b, s, c, d):
    """Statement 'a/b < c/d'."""
    return "%s %s %s" % (fr(a, b), SYM[s], fr(c, d))


def word(s):
    return {"<": "is less than", ">": "is greater than", "=": "is equal to"}[s]


def cmp_mcq(q, a, b, c, d, e, rnd):
    """Choices: the three signs, plus the reverse of the wrong order (a symbol read backwards)."""
    s = sign(a, b, c, d)
    right = st(a, b, s, c, d)
    wrong = [st(a, b, o, c, d) for o in "<>=" if o != s]
    wrong.append(st(c, d, ">" if s == "=" else s, a, b))
    return mcq(q, right, wrong, e, rnd)


def lcd(b, d):
    return b * d // math.gcd(b, d)


def rewrite(a, b, D):
    """'a/b = A/D' or just 'a/b' when b == D."""
    if b == D:
        return fr(a, b)
    return "%s = %s" % (fr(a, b), fr(a * D // b, D))


def e_common(a, b, c, d):
    D = lcd(b, d)
    A, C = a * D // b, c * D // d
    s = sign(a, b, c, d)
    parts = [rewrite(x, y, D) for x, y in ((a, b), (c, d)) if y != D]
    pre = "Write both in %s: %s. " % (PL[D], " and ".join(parts))
    if s == "=":
        return pre + "Both are %s, so %s." % (fr(A, D), st(a, b, s, c, d))
    return pre + "%d %s %d, so %s." % (A, "is less than" if A < C else "is greater than", C, st(a, b, s, c, d))


def half_reason(a, b):
    """Why a/b is less than, equal to or more than 1/2."""
    if b % 2 == 0:
        h = b // 2
        if a == h:
            return "Half of %d is %d, so %s is exactly %s." % (b, h, fr(a, b), fr(1, 2))
        return "Half of %d is %d. %d is %s %d, so %s is %s %s." % (
            b, h, a, "less than" if a < h else "more than", h, fr(a, b), "less than" if a < h else "more than", fr(1, 2))
    return "Double the top: 2 × %d = %d, which is %s %d, so %s is %s %s." % (
        a, 2 * a, "less than" if 2 * a < b else "more than", b, fr(a, b), "less than" if 2 * a < b else "more than", fr(1, 2))


# ------------------------------------------------------------ pictures
def svg_fr(x, cy, a, b, size=16, color=LINE):
    """A stacked fraction drawn in SVG, centered at x, fraction bar at cy."""
    w = max(len(str(a)), len(str(b))) * size * 0.62 + 6
    return ("<text x='%.1f' y='%.1f' font-size='%d' font-weight='700' fill='%s' text-anchor='middle'>%d</text>"
            "<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='1.8'/>"
            "<text x='%.1f' y='%.1f' font-size='%d' font-weight='700' fill='%s' text-anchor='middle'>%d</text>"
            % (x, cy - 4, size, color, a, x - w / 2, cy, x + w / 2, cy, color, x, cy + size + 1, size, color, b))


def bar_row(x, y, W, H, n, k, sub=1):
    """Bar split into n equal parts, first k shaded; each part also cut into `sub` thin pieces."""
    s = []
    for i in range(n):
        s.append("<rect x='%.1f' y='%.1f' width='%.1f' height='%d' fill='%s' stroke='none'/>"
                 % (x + i * W / n, y, W / n, H, FILL if i < k else "#fff"))
    if sub > 1:
        for j in range(1, n * sub):
            if j % sub:
                xx = x + j * W / (n * sub)
                s.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='1.2' stroke-dasharray='4 3'/>"
                         % (xx, y, xx, y + H, THIN))
    for i in range(1, n):
        xx = x + i * W / n
        s.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='2.5'/>" % (xx, y, xx, y + H, LINE))
    s.append("<rect x='%.1f' y='%.1f' width='%.1f' height='%d' fill='none' stroke='%s' stroke-width='2.5'/>" % (x, y, W, H, LINE))
    return "".join(s)


def two_bars_svg(a, b, c, d, W=240, H=38, sub1=1, sub2=1, labels=True):
    """Two bars of the same whole: a/b on top, c/d below, fraction labels on the left."""
    LW = 44 if labels else 0
    s = []
    for row, (n, k, sub) in enumerate([(b, a, sub1), (d, c, sub2)]):
        y = 6 + row * (H + 14)
        if labels:
            num, den = (a, b) if row == 0 else (c, d)
            s.append(svg_fr(6 + LW / 2 - 4, y + H / 2, num, den))
        s.append(bar_row(6 + LW, y, W, H, n, k, sub))
    return svg_wrap(int(W + LW + 12), 2 * H + 26, "".join(s),
                    "two bars of the same size showing %d/%d and %d/%d" % (a, b, c, d))


def two_circles_svg(a, b, c, d, r=40):
    def circ(cx, cy, n, k):
        s = []
        for i in range(n):
            t0 = math.radians(-90 + 360.0 * i / n)
            t1 = math.radians(-90 + 360.0 * (i + 1) / n)
            s.append("<path d='M%.1f %.1f L%.1f %.1f A%d %d 0 0 1 %.1f %.1f Z' fill='%s' stroke='%s' stroke-width='2.2' stroke-linejoin='round'/>"
                     % (cx, cy, cx + r * math.cos(t0), cy + r * math.sin(t0), r, r,
                        cx + r * math.cos(t1), cy + r * math.sin(t1), FILL if i < k else "#fff", LINE))
        return "".join(s)
    cy = 6 + r
    x1 = 6 + 34 + r
    x2 = x1 + r + 26 + 34 + r
    s = [svg_fr(6 + 15, cy, a, b), circ(x1, cy, b, a), svg_fr(x1 + r + 26 + 15, cy, c, d), circ(x2, cy, d, c)]
    return svg_wrap(int(x2 + r + 6), 2 * r + 12, "".join(s),
                    "two circles of the same size showing %d/%d and %d/%d" % (a, b, c, d))


def two_lines_svg(a, b, c, d, W=330):
    """Two number lines from 0 to 1, one above the other, with a dot at a/b and at c/d."""
    LW, L = 44, 56
    R = W - 18
    s = []
    for row, (num, den, col) in enumerate([(a, b, RED), (c, d, BLUE)]):
        Y = 22 + row * 64
        s.append(svg_fr(6 + LW / 2 - 4, Y, num, den, color=col))
        s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='2.5'/>" % (L, Y, R, Y, LINE))
        for i in range(den + 1):
            X = L + (R - L) * i / den
            end = i in (0, den)
            s.append("<line x1='%.1f' y1='%d' x2='%.1f' y2='%d' stroke='%s' stroke-width='%s'/>"
                     % (X, Y - (11 if end else 7), X, Y + (11 if end else 7), LINE, "2.5" if end else "1.8"))
        for i, t in ((0, "0"), (den, "1")):
            X = L + (R - L) * i / den
            s.append("<text x='%.1f' y='%d' font-size='15' font-weight='700' fill='%s' text-anchor='middle'>%s</text>" % (X, Y + 29, LINE, t))
        s.append("<circle cx='%.1f' cy='%d' r='7' fill='%s'/>" % (L + (R - L) * num / den, Y, col))
    return svg_wrap(W, 22 + 64 + 36, "".join(s),
                    "two number lines from 0 to 1 with dots at %d/%d and %d/%d" % (a, b, c, d))


def diff_bars_svg(n1, k1, W1, n2, k2, W2, H=34):
    """Bar A and bar B of different lengths (different wholes)."""
    s = []
    for row, (lab, n, k, W) in enumerate([("A", n1, k1, W1), ("B", n2, k2, W2)]):
        y = 6 + row * (H + 14)
        s.append("<text x='12' y='%.1f' font-size='17' font-weight='800' fill='%s' text-anchor='middle'>%s</text>" % (y + H / 2 + 6, LINE, lab))
        s.append(bar_row(30, y, W, H, n, k))
    return svg_wrap(int(30 + max(W1, W2) + 6), 2 * H + 26, "".join(s), "bar A and bar B are different lengths")


def diff_circles_svg(R1, n1, k1, R2, n2, k2):
    def circ(cx, cy, r, n, k):
        s = []
        for i in range(n):
            t0 = math.radians(-90 + 360.0 * i / n)
            t1 = math.radians(-90 + 360.0 * (i + 1) / n)
            s.append("<path d='M%.1f %.1f L%.1f %.1f A%d %d 0 0 1 %.1f %.1f Z' fill='%s' stroke='%s' stroke-width='2.2' stroke-linejoin='round'/>"
                     % (cx, cy, cx + r * math.cos(t0), cy + r * math.sin(t0), r, r,
                        cx + r * math.cos(t1), cy + r * math.sin(t1), FILL if i < k else "#fff", LINE))
        return "".join(s)
    H = 2 * R1 + 12
    x1 = 6 + 22 + R1
    x2 = x1 + R1 + 30 + 22 + R2
    s = ["<text x='15' y='%d' font-size='17' font-weight='800' fill='%s' text-anchor='middle'>A</text>" % (H / 2 + 6, LINE),
         circ(x1, H / 2, R1, n1, k1),
         "<text x='%d' y='%d' font-size='17' font-weight='800' fill='%s' text-anchor='middle'>B</text>" % (x1 + R1 + 30 + 9, H / 2 + 6, LINE),
         circ(x2, H / 2, R2, n2, k2)]
    return svg_wrap(int(x2 + R2 + 6), H, "".join(s), "circle A is bigger than circle B")


# ============================================================ set 1: compare with models
def set_models(rnd, P):
    its = []
    q_bar = "The two bars are the same size. Which statement is true?"
    for a, b, c, d in [(2, 3, 3, 4), (3, 5, 1, 2), (2, 3, 4, 6), (3, 8, 1, 3), (5, 6, 3, 4),
                       (3, 10, 2, 5), (5, 12, 1, 2), (4, 5, 2, 3), (3, 4, 6, 8)]:
        s = sign(a, b, c, d)
        if s == "=":
            e = ("Both bars are the same whole, and the shaded parts end at the <b>same place</b>. "
                 "So %s." % st(a, b, s, c, d))
        else:
            e = ("Both bars are the same whole. Look at how far the shading goes: the shaded part for %s is %s the shaded part for %s. "
                 "So %s." % (fr(a, b), "shorter than" if s == "<" else "longer than", fr(c, d), st(a, b, s, c, d)))
        its.append(cmp_mcq(fig(two_bars_svg(a, b, c, d)) + q_bar, a, b, c, d, e, rnd))

    for a, b, c, d in [(1, 3, 5, 12), (3, 4, 5, 8), (2, 6, 1, 4), (5, 8, 2, 3)]:
        s = sign(a, b, c, d)
        e = ("The circles are the same size, so they are the same whole. The shaded part for %s covers %s of the circle. "
             "So %s. Check: %s" % (fr(a, b), "less" if s == "<" else "more", st(a, b, s, c, d), e_common(a, b, c, d)))
        its.append(cmp_mcq(fig(two_circles_svg(a, b, c, d)) + "The two circles are the same size. Which statement is true?",
                           a, b, c, d, e, rnd))

    for a, b, c, d in [(2, 3, 5, 8), (3, 4, 4, 5), (1, 2, 5, 10), (7, 10, 3, 5)]:
        s = sign(a, b, c, d)
        if s == "=":
            e = "Both number lines go from 0 to 1. The two dots are at the <b>same point</b>, so %s." % st(a, b, s, c, d)
        else:
            e = ("Both number lines go from 0 to 1, so they show the same whole. The dot for %s is %s the dot for %s "
                 "(%s 0). So %s." % (fr(a, b), "to the left of" if s == "<" else "to the right of", fr(c, d),
                                          "closer to" if s == "<" else "farther from", st(a, b, s, c, d)))
        its.append(cmp_mcq(fig(two_lines_svg(a, b, c, d)) + "Each number line goes from 0 to 1. Which statement is true?",
                           a, b, c, d, e, rnd))

    # different wholes
    for (n1, k1, W1, n2, k2, W2) in [(3, 1, 270, 2, 1, 150), (8, 3, 288, 2, 1, 160)]:
        name, he, his = P.next()
        q = (fig(diff_bars_svg(n1, k1, W1, n2, k2, W2)) +
             "%s of bar A is shaded. %s of bar B is shaded. %s says the picture shows %s &gt; %s. What is wrong?"
             % (fr(k1, n1), fr(k2, n2), name, fr(k1, n1), fr(k2, n2)))
        right = "The bars are different wholes."
        e = ("You can only compare fractions of the <b>same whole</b>. Bar A is longer than bar B, so %s of A can look longer than %s of B. "
             "With the same whole, %s." % (fr(k1, n1), fr(k2, n2), st(k1, n1, sign(k1, n1, k2, n2), k2, n2)))
        its.append(mcq(q, right, ["Nothing. %s &gt; %s." % (fr(k1, n1), fr(k2, n2)),
                                  "%s should count the white parts." % name,
                                  "Bar A has more parts, so it wins."], e, rnd))
    name, he, his = P.next()
    q = (fig(diff_circles_svg(54, 4, 1, 30, 2, 1)) +
         "%s of circle A is shaded. %s of circle B is shaded. Does this picture show that %s &gt; %s?"
         % (fr(1, 4), fr(1, 2), fr(1, 4), fr(1, 2)))
    e = ("No. Circle A is a much bigger whole than circle B, so the pictures cannot be compared. "
         "With the same whole, %s &lt; %s: one of 4 equal pieces is smaller than one of 2 equal pieces." % (fr(1, 4), fr(1, 2)))
    its.append(mcq(q, "No. The circles are different sizes.",
                   ["Yes. The shaded part of A is bigger.", "Yes. 4 is greater than 2.", "No. They show the same amount."], e, rnd))
    assert len(its) == 20, len(its)
    return {"title": "Compare with fraction models", "items": its}


# ============================================================ set 2: common denominators
def set_common_den(rnd, P):
    its = []
    for a, b, D in [(2, 3, 12), (3, 4, 12), (5, 6, 12), (3, 5, 10), (7, 10, 100), (3, 4, 8)]:
        k = D // b
        A = a * k
        q = "Find the missing number.<br>%s = <span class='fr'><span class='fn'><b>?</b></span><span class='fd'>%d</span></span>" % (fr(a, b), D)
        e = ("%d ÷ %d = %d, so multiply the top <b>and</b> the bottom by %d: %d × %d = %d. So %s = %s. "
             "(Adding the same number to the top and bottom does not keep the fraction the same.)"
             % (D, b, k, k, a, k, A, fr(a, b), fr(A, D)))
        wrong = [a + D - b, a, a * b, k, a + k]
        wrong = [str(w) for w in wrong if 0 < w < D and w != A]
        its.append(mcq(q, str(A), wrong, e, rnd))

    for (b, d, a, c) in [(4, 6, 3, 5), (2, 5, 1, 3), (3, 4, 2, 3), (10, 100, 3, 47)]:
        right = lcd(b, d)
        wrong = [b + d, max(b, d), min(b, d), 2 * max(b, d), 3 * min(b, d), d - b]
        wrong = [w for w in wrong if w > 1 and (w % b or w % d)]
        q = "Which number can be a common denominator for %s and %s?" % (fr(a, b), fr(c, d))
        e = ("A common denominator must be a multiple of <b>both</b> %d and %d. %d = %d × %d and %d = %d × %d. "
             "Adding the denominators (%d) does not work." % (b, d, right, b, right // b, right, d, right // d, b + d))
        its.append(mcq(q, str(right), [str(w) for w in wrong], e, rnd))

    for a, b, c, d in [(2, 3, 3, 4), (1, 2, 3, 5), (5, 6, 3, 4)]:
        D = lcd(b, d)
        A, C = a * D // b, c * D // d
        right = "%s and %s" % (fr(A, D), fr(C, D))
        pairs = [(a, c), (a + D - b, c + D - d), (a + D // b, c + D // d), (a * b, c * d)]   # kept / added / added the factor / times own bottom
        wrong = ["%s and %s" % (fr(x, D), fr(y, D)) for x, y in pairs if {x, y} != {A, C}]
        q = "Which shows %s and %s with the same denominator, %d?" % (fr(a, b), fr(c, d), D)
        e = ("Multiply the top and bottom by the same number. %s: × %d gives %s. %s: × %d gives %s. "
             "Keeping the top numbers or adding to them changes the size." % (fr(a, b), D // b, fr(A, D), fr(c, d), D // d, fr(C, D)))
        its.append(mcq(q, right, wrong, e, rnd))

    for a, b, c, d in [(3, 4, 5, 6), (2, 5, 3, 10), (5, 8, 3, 4), (7, 10, 65, 100), (5, 12, 1, 3), (3, 5, 7, 10), (8, 12, 4, 6)]:
        e = e_common(a, b, c, d)
        its.append(cmp_mcq("Compare %s and %s. Which statement is true?" % (fr(a, b), fr(c, d)), a, b, c, d, e, rnd))
    assert len(its) == 20, len(its)
    return {"title": "Compare with common denominators", "items": its}


# ============================================================ set 3: common numerators
def e_same_num(a, b, c, d, pre=""):
    s = sign(a, b, c, d)
    small, big = min(b, d), max(b, d)
    pieces = "1 piece" if a == 1 else "%d pieces" % a
    return (pre + "Both have <b>%s</b>. %s are bigger than %s, because the whole is cut into fewer parts. "
            "So %s." % (pieces, PL[small].capitalize(), PL[big], st(a, b, s, c, d)))


def set_common_num(rnd, P):
    its = []
    for a, b, c, d in [(1, 5, 1, 8), (1, 10, 1, 6), (1, 3, 1, 12)]:
        e = e_same_num(a, b, c, d) + " A bigger bottom number does not mean a bigger fraction."
        its.append(cmp_mcq("Compare %s and %s. Which statement is true?" % (fr(a, b), fr(c, d)), a, b, c, d, e, rnd))
    for a, b, c, d in [(3, 5, 3, 8), (2, 10, 2, 6), (5, 6, 5, 12), (4, 10, 4, 5), (7, 8, 7, 12)]:
        its.append(cmp_mcq("Compare %s and %s. Which statement is true?" % (fr(a, b), fr(c, d)), a, b, c, d,
                           e_same_num(a, b, c, d), rnd))

    for a, b, N in [(2, 3, 4), (3, 4, 6), (3, 5, 6)]:
        k = N // a
        B = b * k
        q = "Find the missing number.<br>%s = <span class='fr'><span class='fn'>%d</span><span class='fd'><b>?</b></span></span>" % (fr(a, b), N)
        e = ("%d ÷ %d = %d, so multiply the top <b>and</b> the bottom by %d: %d × %d = %d. So %s = %s."
             % (N, a, k, k, b, k, B, fr(a, b), fr(N, B)))
        wrong = [str(w) for w in [b + N - a, b, b * N, b + k, B + 1] if w != B]
        its.append(mcq(q, str(B), wrong, e, rnd))

    for (a, b), (c, d) in [((2, 3), (4, 5)), ((3, 4), (6, 10)), ((2, 5), (4, 12)), ((3, 5), (6, 8)), ((1, 2), (3, 8))]:
        N = c
        k = N // a
        pre = "Make the top numbers the same: %s = %s. " % (fr(a, b), fr(N, b * k))
        e = e_same_num(N, b * k, c, d, pre).replace(st(N, b * k, sign(a, b, c, d), c, d), st(a, b, sign(a, b, c, d), c, d))
        its.append(cmp_mcq("Compare %s and %s. Which statement is true?" % (fr(a, b), fr(c, d)), a, b, c, d, e, rnd))

    a, dens = 3, [4, 5, 8, 10]
    e = "All four have <b>3 pieces</b>. The smallest bottom number means the biggest pieces, so %s is the greatest." % fr(3, 4)
    its.append(mcq("Which fraction is the <b>greatest</b>?", fr(3, 4), [fr(3, x) for x in [10, 8, 5]], e, rnd))
    e = "All four have <b>5 pieces</b>. The biggest bottom number means the smallest pieces, so %s is the smallest." % fr(5, 12)
    its.append(mcq("Which fraction is the <b>smallest</b>?", fr(5, 12), [fr(5, x) for x in [6, 8, 10]], e, rnd))

    for a, b, c, d in [(4, 5, 5, 6), (7, 8, 9, 10)]:
        s = sign(a, b, c, d)
        e = ("Each fraction is <b>1 piece</b> away from 1 whole. %s is missing %s and %s is missing %s. "
             "%s is the smaller missing piece, so %s is closer to 1. So %s."
             % (fr(a, b), fr(1, b), fr(c, d), fr(1, d), fr(1, max(b, d)), fr(c, d) if d > b else fr(a, b), st(a, b, s, c, d)))
        its.append(cmp_mcq("Compare %s and %s. Which statement is true?" % (fr(a, b), fr(c, d)), a, b, c, d, e, rnd))
    assert len(its) == 20, len(its)
    return {"title": "Compare with common numerators", "items": its}


# ============================================================ set 4: benchmarks and ordering
def where(a, b):
    x = F(a, b)
    if x < F(1, 2):
        return "lt"
    if x == F(1, 2):
        return "eq"
    if x < 1:
        return "mid"
    return "gt"


def set_benchmarks(rnd, P):
    its = []
    labels = {"lt": "Less than %s" % fr(1, 2), "eq": "Exactly %s" % fr(1, 2),
              "mid": "Between %s and 1" % fr(1, 2), "gt": "Greater than 1"}
    for a, b in [(5, 8), (3, 8), (6, 12), (4, 10), (7, 12), (7, 6)]:
        w = where(a, b)
        if w == "gt":
            e = "The top number (%d) is bigger than the bottom number (%d), so %s is <b>more than 1 whole</b>: %s = 1 and %s more." % (
                a, b, fr(a, b), fr(b, b), fr(a - b, b))
        else:
            e = half_reason(a, b)
            if w == "mid":
                e += " It is less than 1 because %d is less than %d." % (a, b)
        its.append(mcq("Where is %s?" % fr(a, b), labels[w], [labels[k] for k in ["lt", "eq", "mid", "gt"]], e, rnd))

    for a, b, c, d in [(3, 8, 4, 6), (2, 5, 7, 12), (5, 6, 4, 10), (3, 4, 5, 12)]:
        s = sign(a, b, c, d)
        e = "Use %s as a benchmark. %s %s So %s." % (fr(1, 2), half_reason(a, b), half_reason(c, d), st(a, b, s, c, d))
        its.append(cmp_mcq("Compare %s and %s. Which statement is true?" % (fr(a, b), fr(c, d)), a, b, c, d, e, rnd))
    for a, b, c, d in [(5, 4, 7, 8), (9, 10, 7, 6)]:
        s = sign(a, b, c, d)
        big, small = ((a, b), (c, d)) if a > b else ((c, d), (a, b))
        e = ("Use 1 as a benchmark. %s is more than 1 (top bigger than bottom). %s is less than 1 (top smaller than bottom). "
             "So %s." % (fr(*big), fr(*small), st(a, b, s, c, d)))
        its.append(cmp_mcq("Compare %s and %s. Which statement is true?" % (fr(a, b), fr(c, d)), a, b, c, d, e, rnd))

    e = ("%s %s are all more than %s (each top number is more than half the bottom). %s"
         % (", ".join(fr(*x) for x in [(4, 6), (5, 8)]) + " and", fr(3, 5), fr(1, 2), half_reason(5, 12)))
    its.append(mcq("Which fraction is <b>less than</b> %s?" % fr(1, 2), fr(5, 12), [fr(4, 6), fr(5, 8), fr(3, 5)], e, rnd))
    e = ("%s %s %s A small top number like 3 can still be more than half." % (half_reason(3, 5), half_reason(4, 10), half_reason(6, 12)))
    its.append(mcq("Which fraction is <b>greater than</b> %s?" % fr(1, 2), fr(3, 5), [fr(4, 10), fr(6, 12), fr(5, 12)], e, rnd))

    orders = [
        ([(2, 3), (1, 4), (5, 8)], "up", "%s is less than %s. %s and %s are both more than %s. Use 24ths: %s = %s and %s = %s."
         % (fr(1, 4), fr(1, 2), fr(5, 8), fr(2, 3), fr(1, 2), fr(5, 8), fr(15, 24), fr(2, 3), fr(16, 24))),
        ([(3, 10), (4, 5), (1, 2)], "up", "Use tenths: %s, %s = %s, %s = %s. 3 &lt; 5 &lt; 8."
         % (fr(3, 10), fr(1, 2), fr(5, 10), fr(4, 5), fr(8, 10))),
        ([(5, 6), (3, 8), (7, 12)], "down", "%s is less than %s (half of 8 is 4). Use twelfths for the others: %s = %s, which is more than %s."
         % (fr(3, 8), fr(1, 2), fr(5, 6), fr(10, 12), fr(7, 12))),
        ([(5, 12), (3, 4), (2, 3)], "up", "Use twelfths: %s, %s = %s, %s = %s. 5 &lt; 8 &lt; 9."
         % (fr(5, 12), fr(2, 3), fr(8, 12), fr(3, 4), fr(9, 12))),
        ([(6, 10), (1, 4), (3, 8)], "up", "%s = %s, which is less than %s. Both are less than %s, and %s is more than %s."
         % (fr(1, 4), fr(2, 8), fr(3, 8), fr(1, 2), fr(6, 10), fr(1, 2))),
        ([(4, 5), (7, 10), (9, 10)], "down", "Use tenths: %s = %s, and 9 &gt; 8 &gt; 7."
         % (fr(4, 5), fr(8, 10))),
    ]
    for fs, way, why in orders:
        def show(lst):
            return ", ".join(fr(*x) for x in lst)
        up = sorted(fs, key=lambda x: F(*x))
        right_l = up if way == "up" else up[::-1]
        rev = way == "down"
        cands = [sorted(fs, key=lambda x: x[1], reverse=rev),        # bigger denominator = bigger fraction
                 sorted(fs, key=lambda x: x[0], reverse=rev),        # compare only the top numbers
                 right_l[::-1]]                                      # wrong direction
        cands += [list(p) for p in itertools.permutations(fs)]
        q = "Order from <b>%s</b>:<br>%s" % ("least to greatest" if way == "up" else "greatest to least", show(fs))
        e = why + " So the order is %s." % show(right_l)
        its.append(mcq(q, show(right_l), [show(c) for c in cands], e, rnd))
    assert len(its) == 20, len(its)
    return {"title": "Benchmarks 1/2 and 1, and ordering", "items": its}


# ============================================================ set 5: word problems
def set_words(rnd, P):
    its = []

    def add(story, a, b, c, d, same_txt, tail, e=None, names=None):
        (n1, h1, s1), (n2, h2, s2) = names or (P.next(), P.next())
        s = sign(a, b, c, d)
        right = n1 if s == ">" else (n2 if s == "<" else same_txt)
        ee = e or e_common(a, b, c, d)
        if s != "=":
            ee += " <b>%s</b> %s." % (right, tail)
        else:
            ee += " " + same_txt + "."
        its.append(mcq(story(n1, n2), right, [n1, n2, same_txt, CANT], ee, rnd))

    add(lambda x, y: "%s ran %s of a mile. %s ran %s of a mile. Who ran farther?" % (x, fr(3, 4), y, fr(2, 3)),
        3, 4, 2, 3, "They ran the same distance", "ran farther")
    add(lambda x, y: "Recipe A uses %s cup of flour. Recipe B uses %s cup of flour. Which recipe uses more flour?" % (fr(3, 4), fr(5, 8)),
        3, 4, 5, 8, "They use the same amount", "uses more flour", names=[("Recipe A", "", ""), ("Recipe B", "", "")])
    add(lambda x, y: "%s and %s each painted a fence. The fences are the same size. %s painted %s of a fence and %s painted %s. Who painted more?"
        % (x, y, x, fr(3, 5), y, fr(4, 10)), 3, 5, 4, 10, "They painted the same amount", "painted more")
    add(lambda x, y: "%s has read %s of a book. %s has read %s of the same book. Who has read more of it?" % (x, fr(5, 12), y, fr(1, 2)),
        5, 12, 1, 2, "They read the same amount", "has read more",
        e="Use %s as a benchmark. %s" % (fr(1, 2), half_reason(5, 12)))
    add(lambda x, y: "%s drank %s of a bottle of water. %s drank %s of the same kind of bottle. Who drank more?" % (x, fr(7, 10), y, fr(4, 5)),
        7, 10, 4, 5, "They drank the same amount", "drank more")
    add(lambda x, y: "%s walked %s of a mile to school. %s walked %s of a mile. Who walked farther?" % (x, fr(2, 3), y, fr(8, 12)),
        2, 3, 8, 12, "They walked the same distance", "walked farther")
    add(lambda x, y: "Jar A has %s liter of juice. Jar B has %s liter of juice. Which jar has more juice?" % (fr(6, 10), fr(58, 100)),
        6, 10, 58, 100, "They have the same amount", "has more juice", names=[("Jar A", "", ""), ("Jar B", "", "")])
    add(lambda x, y: "%s spent %s of an hour on homework. %s spent %s of an hour. Who spent more time?" % (x, fr(5, 6), y, fr(7, 8)),
        5, 6, 7, 8, "They spent the same time", "spent more time",
        e="Each fraction is 1 piece away from 1 whole. %s is missing %s, and %s is missing %s. %s is the smaller missing piece, so %s is closer to 1 hour."
        % (fr(5, 6), fr(1, 6), fr(7, 8), fr(1, 8), fr(1, 8), fr(7, 8)))
    add(lambda x, y: "A green ribbon is %s yard long. A blue ribbon is %s yard long. Which ribbon is longer?" % (fr(4, 5), fr(7, 10)),
        4, 5, 7, 10, "They are the same length", "is longer", names=[("The green ribbon", "", ""), ("The blue ribbon", "", "")])
    add(lambda x, y: "%s hiked %s of a trail. %s hiked %s of the same trail. Who hiked farther?" % (x, fr(5, 12), y, fr(3, 8)),
        5, 12, 3, 8, "They hiked the same distance", "hiked farther")
    add(lambda x, y: "%s colored %s of a poster. %s colored %s of a poster that is the same size. Who colored more?" % (x, fr(3, 4), y, fr(9, 12)),
        3, 4, 9, 12, "They colored the same amount", "colored more")

    # four people / four things
    def four(q, items, best, e):
        right = [n for n, f in items if f == best][0]
        assert best == (max if "farthest" in q or "longest" in q else min)(f for n, f in items)
        its.append(mcq(q, right, [n for n, f in items], e, rnd))
    ps = [P.next() for _ in range(4)]
    fs = [(3, 8), (1, 2), (2, 3), (5, 12)]
    four("Four friends ran on a track. %s ran %s mile, %s ran %s mile, %s ran %s mile and %s ran %s mile. Who ran the farthest?"
         % tuple(x for p, f in zip(ps, fs) for x in (p[0], fr(*f))),
         [(p[0], F(*f)) for p, f in zip(ps, fs)], F(2, 3),
         "Use 24ths: %s = %s, %s = %s, %s = %s, %s = %s. 16 is the most, so <b>%s</b> ran the farthest."
         % (fr(3, 8), fr(9, 24), fr(1, 2), fr(12, 24), fr(2, 3), fr(16, 24), fr(5, 12), fr(10, 24), ps[2][0]))
    fs = [(5, 6), (3, 4), (7, 12), (2, 3)]
    four("Four snails raced. Snail A moved %s foot, Snail B moved %s foot, Snail C moved %s foot and Snail D moved %s foot. Which snail moved the least?"
         % tuple(fr(*f) for f in fs),
         [("Snail " + L, F(*f)) for L, f in zip("ABCD", fs)], F(7, 12),
         "Use twelfths: %s = %s, %s = %s, %s, %s = %s. 7 is the least, so <b>Snail C</b> moved the least."
         % (fr(5, 6), fr(10, 12), fr(3, 4), fr(9, 12), fr(7, 12), fr(2, 3), fr(8, 12)))
    fs = [(7, 10), (3, 5), (1, 2), (65, 100)]
    four("The red ribbon is %s yard, the blue ribbon is %s yard, the green ribbon is %s yard and the yellow ribbon is %s yard. Which ribbon is the longest?"
         % tuple(fr(*f) for f in fs),
         [(c, F(*f)) for c, f in zip(["Red", "Blue", "Green", "Yellow"], fs)], F(7, 10),
         "Use hundredths: %s = %s, %s = %s, %s = %s, %s. 70 is the most, so the <b>red</b> ribbon is the longest."
         % (fr(7, 10), fr(70, 100), fr(3, 5), fr(60, 100), fr(1, 2), fr(50, 100), fr(65, 100)))

    # same whole
    n, he, his = P.next()
    q = ("%s ate %s of a small pizza. %s friend ate %s of a large pizza. %s says %s ate more because %s &gt; %s. Is %s right?"
         % (n, fr(1, 2), his.capitalize(), fr(1, 3), n, he, fr(1, 2), fr(1, 3), he))
    e = ("The pizzas are <b>different wholes</b>. %s of a large pizza can be more than %s of a small pizza. "
         "Comparing %s and %s only works when the wholes are the same size." % (fr(1, 3), fr(1, 2), fr(1, 2), fr(1, 3)))
    its.append(mcq(q, "Not for sure. The pizzas are different sizes.",
                   ["Yes, because %s &gt; %s." % (fr(1, 2), fr(1, 3)), "No, because %s &gt; %s." % (fr(1, 3), fr(1, 2)),
                    "Yes, because 2 is less than 3."], e, rnd))
    (n1, _, _), (n2, _, _) = P.next(), P.next()
    q = "%s read %s of a short book. %s read %s of a long book. Who read more pages?" % (n1, fr(3, 4), n2, fr(1, 2))
    e = ("The books are <b>different wholes</b>. %s is more than %s of the same book, but the long book may have many more pages. "
         "Without the number of pages, you can’t tell." % (fr(3, 4), fr(1, 2)))
    its.append(mcq(q, CANT, [n1, n2, "They read the same number of pages"], e, rnd))
    (n1, _, _), (n2, _, _) = P.next(), P.next()
    q = ("%s ate %s of a 16-inch sandwich. %s ate %s of an 8-inch sandwich. Who ate more sandwich?"
         % (n1, fr(1, 2), n2, fr(3, 4)))
    e = ("The wholes are different, so find the lengths. %s of 16 inches is 8 inches. An 8-inch sandwich cut into 4 equal parts has 2-inch parts, "
         "so %s of it is 6 inches. 8 &gt; 6, so <b>%s</b> ate more, even though %s &lt; %s." % (fr(1, 2), fr(3, 4), n1, fr(1, 2), fr(3, 4)))
    its.append(mcq(q, n1, [n2, "They ate the same amount", CANT], e, rnd))
    q = "Which pair can you compare just by comparing the fractions?"
    e = ("A mile is always the same length, so %s mile and %s mile are parts of the <b>same whole</b>: %s &lt; %s. "
         "The other pairs use wholes of different sizes." % (fr(1, 2), fr(3, 5), fr(1, 2), fr(3, 5)))
    its.append(mcq(q, "%s mile and %s mile" % (fr(1, 2), fr(3, 5)),
                   ["%s of a big box and %s of a small box" % (fr(3, 4), fr(2, 3)),
                    "%s of one class and %s of another class" % (fr(2, 5), fr(1, 2)),
                    "%s of a large pizza and %s of a small pizza" % (fr(1, 3), fr(1, 4))], e, rnd))

    # justify
    n, he, his = P.next()
    q = "%s says %s &lt; %s because eighths are smaller than halves. Is %s right?" % (n, fr(5, 8), fr(1, 2), he)
    e = ("Eighths are smaller pieces, but there are 5 of them. %s So %s &gt; %s." % (half_reason(5, 8), fr(5, 8), fr(1, 2)))
    its.append(mcq(q, "No. %s is more than %s." % (fr(5, 8), fr(1, 2)),
                   ["Yes. Eighths are smaller pieces.", "Yes. 8 is more than 2.", "No. %s = %s." % (fr(5, 8), fr(1, 2))], e, rnd))
    n, he, his = P.next()
    q = "%s says %s = %s because each one is 1 piece away from a whole. Is %s right?" % (n, fr(2, 3), fr(3, 4), he)
    e = ("The missing pieces are different sizes: %s is bigger than %s. So %s is farther from 1 than %s. "
         "Check with twelfths: %s = %s and %s = %s." % (fr(1, 3), fr(1, 4), fr(2, 3), fr(3, 4), fr(2, 3), fr(8, 12), fr(3, 4), fr(9, 12)))
    its.append(mcq(q, "No. %s &lt; %s." % (fr(2, 3), fr(3, 4)),
                   ["Yes. Both are 1 piece from 1.", "No. %s &gt; %s." % (fr(2, 3), fr(3, 4)), "Yes. 3 − 2 = 4 − 3."], e, rnd))
    assert len(its) == 20, len(its)
    return {"title": "Compare fractions word problems", "items": its}


# ============================================================ lesson
def body_html():
    big = two_bars_svg(2, 3, 3, 4, W=300, H=40)
    cd_fig = two_bars_svg(2, 3, 3, 4, W=300, H=40, sub1=4, sub2=3)
    cn_fig = svg_wrap(356, 106, "".join([
        svg_fr(6 + 18, 6 + 20, 4, 6), bar_row(50, 6, 300, 40, 6, 4),
        svg_fr(6 + 18, 60 + 20, 4, 5), bar_row(50, 60, 300, 40, 5, 4)]), "four sixths and four fifths on bars of the same size")
    # benchmark number line
    L, R, Y = 24, 356, 54
    s = ["<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='2.5'/>" % (L, Y, R, Y, LINE)]
    for v, t in ((0, "0"), (1, "1")):
        X = L + (R - L) * v
        s.append("<line x1='%.1f' y1='%d' x2='%.1f' y2='%d' stroke='%s' stroke-width='2.5'/>" % (X, Y - 11, X, Y + 11, LINE))
        s.append("<text x='%.1f' y='%d' font-size='16' font-weight='700' fill='%s' text-anchor='middle'>%s</text>" % (X, Y + 32, LINE, t))
    Xh = (L + R) / 2
    s.append("<line x1='%.1f' y1='%d' x2='%.1f' y2='%d' stroke='%s' stroke-width='2.5'/>" % (Xh, Y - 11, Xh, Y + 11, LINE))
    s.append(svg_fr(Xh, Y + 30, 1, 2))
    for (a, b), col in (((3, 8), RED), ((4, 6), BLUE)):
        X = L + (R - L) * a / b
        s.append("<circle cx='%.1f' cy='%d' r='7' fill='%s'/>" % (X, Y, col))
        s.append(svg_fr(X, Y - 30, a, b, color=col))
    bm_fig = svg_wrap(380, 104, "".join(s), "number line from 0 to 1 with 3/8 left of one half and 4/6 right of one half")
    dw_fig = diff_bars_svg(3, 1, 270, 2, 1, 150)

    return (
        "<h2>The idea</h2>"
        "<p>A fraction’s size depends on <b>both</b> numbers: how many pieces, and how big each piece is. "
        "To compare two fractions, make one of these the same, or compare each fraction to an easy fraction like " + fr(1, 2) + ".</p>"
        "<figure class='sn-fig'>" + big +
        "<figcaption>The bars are the same whole. The shading for " + fr(3, 4) + " goes farther, so " + fr(2, 3) + " &lt; " + fr(3, 4) + ".</figcaption></figure>"
        "<p>Write the result with a symbol: <b>&gt;</b> (greater than), <b>&lt;</b> (less than) or <b>=</b> (equal). "
        "The open side of the symbol faces the bigger fraction.</p>"
        "<h2>Strategy 1: Make a common denominator</h2>"
        "<p>Cut the pieces so both fractions have the <b>same size pieces</b>. Then compare the top numbers. "
        "Multiply the top and bottom by the same number.</p>"
        "<figure class='sn-fig'>" + cd_fig +
        "<figcaption>Cut thirds into 4 and fourths into 3. Both bars now have twelfths: " + fr(2, 3) + " = " + fr(8, 12) +
        " and " + fr(3, 4) + " = " + fr(9, 12) + ".</figcaption></figure>"
        + ex("Example", "Compare " + fr(5, 6) + " and " + fr(3, 4) + ".",
             "Use twelfths: " + fr(5, 6) + " = " + fr(10, 12) + " and " + fr(3, 4) + " = " + fr(9, 12) + ". 10 &gt; 9.",
             fr(5, 6) + " &gt; " + fr(3, 4))
        + "<h2>Strategy 2: Make a common numerator</h2>"
        "<p>If the top numbers are the same, you have the <b>same number of pieces</b>. "
        "Then the fraction with the <b>smaller</b> bottom number has bigger pieces, so it is greater.</p>"
        "<figure class='sn-fig'>" + cn_fig +
        "<figcaption>" + fr(2, 3) + " = " + fr(4, 6) + ". Four fifths are bigger than four sixths, so " + fr(2, 3) + " &lt; " + fr(4, 5) + ".</figcaption></figure>"
        + ex("Example", "Compare " + fr(3, 4) + " and " + fr(6, 10) + ".",
             fr(3, 4) + " = " + fr(6, 8) + ". Eighths are bigger than tenths, so " + fr(6, 8) + " &gt; " + fr(6, 10) + ".",
             fr(3, 4) + " &gt; " + fr(6, 10))
        + "<h2>Strategy 3: Compare to " + fr(1, 2) + " or 1</h2>"
        "<p>Is the top number more or less than <b>half</b> of the bottom number? "
        "If one fraction is less than " + fr(1, 2) + " and the other is more, you are done.</p>"
        "<figure class='sn-fig'>" + bm_fig +
        "<figcaption>Half of 8 is 4, so " + fr(3, 8) + " is less than " + fr(1, 2) + ". Half of 6 is 3, so " + fr(4, 6) +
        " is more than " + fr(1, 2) + ". So " + fr(3, 8) + " &lt; " + fr(4, 6) + ".</figcaption></figure>"
        + table(["When", "Try", "Example"], [
            ["One bottom number is a multiple of the other", "Common denominator", fr(3, 5) + " and " + fr(7, 10) + ": " + fr(6, 10) + " &lt; " + fr(7, 10)],
            ["The top numbers are easy to match", "Common numerator", fr(1, 2) + " and " + fr(3, 8) + ": " + fr(3, 6) + " &gt; " + fr(3, 8)],
            ["One is below " + fr(1, 2) + ", one is above", "Benchmark " + fr(1, 2), fr(2, 5) + " &lt; " + fr(7, 12)],
            ["One is more than 1, one is less", "Benchmark 1", fr(5, 4) + " &gt; " + fr(7, 8)],
        ])
        + "<h2>Use the same whole</h2>"
        "<p>Fractions can only be compared when they are parts of the <b>same size whole</b>. "
        + fr(1, 3) + " of a long bar can be longer than " + fr(1, 2) + " of a short bar, but " + fr(1, 3) + " is still less than " + fr(1, 2) + ".</p>"
        "<figure class='sn-fig'>" + dw_fig +
        "<figcaption>" + fr(1, 3) + " of bar A looks longer than " + fr(1, 2) + " of bar B, because bar A is a bigger whole.</figcaption></figure>"
        + "<h2>Common mistakes</h2>"
        + table(["Mistake", "What to do instead"], [
            ["Thinking " + fr(1, 8) + " &gt; " + fr(1, 5) + " because 8 &gt; 5", "A bigger bottom number means <b>smaller</b> pieces"],
            ["Comparing only the top numbers: " + fr(3, 8) + " &gt; " + fr(2, 3), "Check the piece size too: " + fr(3, 8) + " is less than " + fr(1, 2)],
            ["Adding the same number to the top and bottom: " + fr(2, 3) + " = " + fr(11, 12), "<b>Multiply</b> the top and bottom by the same number: " + fr(2, 3) + " = " + fr(8, 12)],
            ["Saying " + fr(2, 3) + " = " + fr(3, 4) + " because each is 1 piece from a whole", "The missing pieces are different sizes: " + fr(1, 3) + " &gt; " + fr(1, 4)],
            ["Comparing parts of different-size wholes", "Make sure both fractions are of the <b>same whole</b>"],
        ])
    )


FAQ = [
    {"q": "How do you compare fractions with different denominators?",
     "a": "Rewrite them with a common denominator, then compare the numerators. For 2/3 and 3/4, use twelfths: 8/12 is less than 9/12, so 2/3 < 3/4."},
    {"q": "What is a benchmark fraction?",
     "a": "A benchmark is an easy fraction you compare to, usually 1/2 or 1. If 3/8 is less than 1/2 and 4/6 is more than 1/2, then 3/8 < 4/6."},
    {"q": "Why must fractions refer to the same whole?",
     "a": "A fraction is part of a whole, so its size depends on the whole. Half of a small pizza can be less than a third of a large pizza."},
    {"q": "How do you tell if a fraction is more than 1/2?",
     "a": "Compare the top number with half of the bottom number. In 5/8, half of 8 is 4 and 5 is more than 4, so 5/8 is more than 1/2."},
]


def gen_compare():
    rnd = random.Random(104)
    P = People(rnd)
    sets = [set_models(rnd, P), set_common_den(rnd, P), set_common_num(rnd, P), set_benchmarks(rnd, P), set_words(rnd, P)]
    for s in sets:
        assert len(s["items"]) == 20, (s["title"], len(s["items"]))
        for it in s["items"]:
            assert len(set(it["c"])) == 4, it
    return {
        "country": "us", "subject": "math", "grade": "grade-4", "slug": "compare-fractions", "sort": 4,
        "updated": UPDATED, "pdf_url": "",
        "title": "Compare Fractions",
        "seo_title": "Grade 4 Comparing Fractions Worksheets: Common Denominators, Common Numerators and Benchmark 1/2",
        "short_title": "Compare Fractions",
        "domain": "Number and Operations—Fractions",
        "standard_code": "4.NF.A.2",
        "standard_url": "https://www.thecorestandards.org/Math/Content/4/NF/A/2/",
        "standard_text": "Compare two fractions with different numerators and different denominators, e.g., by creating common denominators or numerators, or by comparing to a benchmark fraction such as 1/2. Recognize that comparisons are valid only when the two fractions refer to the same whole. Record the results of comparisons with symbols >, =, or <, and justify the conclusions, e.g., by using a visual fraction model.",
        "meta_desc": "Free Grade 4 comparing fractions worksheets: compare fractions with models, common denominators, common numerators and the benchmark 1/2, order fractions, and solve word problems. 100 practice questions with explanations and a printable answer key.",
        "key_big": "To compare fractions, make the pieces the same size, make the number of pieces the same, or compare each one to 1/2.",
        "key_sub": "2/3 and 3/4 become 8/12 and 9/12, so 2/3 < 3/4. Fractions can only be compared when they are parts of the same whole.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }


if __name__ == "__main__":
    u = gen_compare()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, "compare-fractions.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(u, f, ensure_ascii=False, indent=1)
    print("wrote", path)
