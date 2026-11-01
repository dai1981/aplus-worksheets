# -*- coding: utf-8 -*-
"""
US Grade 4 Math: Multiply Fractions by Whole Numbers (4.NF.B.4)
  python tools/gen_us_math_g4_multiply_fractions.py
Grade 4 denominators: 2, 3, 4, 5, 6, 8, 10, 12.
Mixed-number answers are always in simplest form (the fraction part is never like 2/4),
because simplifying is not part of this standard.
HTML attributes use single quotes (no backslashes in the JSON).
"""
import json, math, os, random, re
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "us", "math", "grade-4")
UPDATED = "2026-11-02"
FILL = "#4fae74"      # shaded part
LINE = "#2b2b2b"
RED = "#d6453b"
GIRLS = ["Maya", "Ava", "Mia", "Zoe", "Lily", "Emma", "Nora", "Ruby", "Sofia", "Grace"]
BOYS = ["Leo", "Noah", "Eli", "Sam", "Ben", "Omar", "Kai", "Jack", "Luis", "Owen"]


# ------------------------------------------------------------ helpers
def fr(a, b):
    return "<span class='fr'><span class='fn'>%d</span><span class='fd'>%d</span></span>" % (a, b)


def mixed(w, r, b):
    """Whole number followed by the fraction span (3 <fr>)."""
    if r == 0:
        return str(w)
    if w == 0:
        return fr(r, b)
    return "%d %s" % (w, fr(r, b))


def mixed_of(n, b):
    """n/b as a mixed number (or whole number / proper fraction)."""
    return mixed(n // b, n % b, b)


def reduced(n, b):
    return n % b == 0 or math.gcd(n % b, b) == 1


def mcq(q, correct, cands, e, rnd):
    """cands: html strings, or (html, value) pairs; a pair whose value equals the answer is skipped."""
    cv = None
    if isinstance(correct, tuple):
        correct, cv = correct
    seen = {correct}
    pick = []
    for c in cands:
        v = None
        if isinstance(c, tuple):
            c, v = c
        if not c or c in seen or (cv is not None and v is not None and v == cv):
            continue
        seen.add(c)
        pick.append(c)
        if len(pick) == 3:
            break
    assert len(pick) == 3, (q, correct, cands)
    ch = pick + [correct]
    rnd.shuffle(ch)
    return {"q": q, "c": ch, "a": ch.index(correct), "e": e}


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


def times(n, a, b):
    return "%d × %s" % (n, fr(a, b))


def pl(k, one, many):
    return one if k == 1 else many


# ------------------------------------------------------------ figures
def bar_svg(n, k, W=264, H=46):
    """One bar split into n equal parts, first k shaded."""
    s = []
    for i in range(n):
        s.append("<rect x='%.1f' y='6' width='%.1f' height='%d' fill='%s' stroke='%s' stroke-width='2.5'/>"
                 % (6 + i * W / float(n), W / float(n), H, FILL if i < k else "#fff", LINE))
    return svg_wrap(W + 12, H + 12, "".join(s), "bar split into %d equal parts with %d shaded" % (n, k))


def groups_svg(n, a, b, BW=96, BH=34, GX=18, GY=14):
    """n equal bars (each 1 whole) split into b parts, a parts of each shaded. Up to 3 bars per row."""
    cols = min(n, 3)
    rows = (n + cols - 1) // cols
    s = []
    for g in range(n):
        x0 = 6 + (g % cols) * (BW + GX)
        y0 = 6 + (g // cols) * (BH + GY)
        for i in range(b):
            s.append("<rect x='%.1f' y='%d' width='%.2f' height='%d' fill='%s' stroke='%s' stroke-width='2'/>"
                     % (x0 + i * BW / float(b), y0, BW / float(b), BH, FILL if i < a else "#fff", LINE))
    W = cols * BW + (cols - 1) * GX + 12
    H = rows * BH + (rows - 1) * GY + 12
    return svg_wrap(W, H, "".join(s), "%d bars, each split into %d equal parts with %d shaded" % (n, b, a))


def jumps_svg(n, a, b, W=440, show_end=True):
    """Number line from 0 to the next whole number at or above n*a/b, ticks every 1/b, n jumps of a/b."""
    wholes = max(1, -(-n * a // b))
    total = wholes * b
    L, R, Y = 18, W - 18, 62
    def X(i):
        return L + (R - L) * i / float(total)
    s = ["<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='2.5'/>" % (L, Y, R, Y, LINE)]
    for i in range(total + 1):
        whole = (i % b == 0)
        s.append("<line x1='%.1f' y1='%d' x2='%.1f' y2='%d' stroke='%s' stroke-width='%s'/>"
                 % (X(i), Y - (12 if whole else 7), X(i), Y + (12 if whole else 7), LINE, "2.5" if whole else "1.6"))
        if whole:
            s.append("<text x='%.1f' y='%d' font-size='18' font-weight='700' fill='%s' text-anchor='middle'>%d</text>"
                     % (X(i), Y + 34, LINE, i // b))
    h = 40 if a > 1 else 30
    for j in range(n):
        x0, x1 = X(j * a), X((j + 1) * a)
        s.append("<path d='M%.1f %d Q%.1f %d %.1f %d' fill='none' stroke='%s' stroke-width='2.5'/>"
                 % (x0, Y - 2, (x0 + x1) / 2, Y - 2 - h, x1, Y - 2, RED))
        # small arrowhead at the end of the jump
        s.append("<path d='M%.1f %d l-7 -9 l9 1 z' fill='%s'/>" % (x1, Y - 2, RED))
    if show_end:
        s.append("<circle cx='%.1f' cy='%d' r='6' fill='%s'/>" % (X(n * a), Y, RED))
    return svg_wrap(W, Y + 42, "".join(s),
                    "number line from 0 to %d with %d %s of %d/%d" % (wholes, n, pl(n, "jump", "jumps"), a, b))


def mark_large(u, pattern):
    """Tag pictures that must print larger (number lines with many labels) so their labels stay readable."""
    rx = re.compile(r"<svg (?=[^>]*aria-label='" + pattern + ")")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u


# ------------------------------------------------------------ typical wrong answers for n × a/b
def frac_wrongs(n, a, b):
    """(html, value) pairs from real mistakes, most common first."""
    return [
        (fr(n * a, n * b), F(a, b)),          # multiplied the top and the bottom
        (fr(a, n * b), F(a, n * b)),          # multiplied only the bottom
        (fr(n + a, b), F(n + a, b)),          # added the whole number to the top
        (fr(b, n * a), F(b, n * a)),          # flipped the answer
        (fr(n * a, b + n), F(n * a, b + n)),  # added to the bottom
    ]


def mixed_wrongs(n, a, b):
    t = n * a
    q, r = divmod(t, b)
    out = [
        (mixed(n, a, b), F(n * b + a, b)),            # wrote n + a/b: added instead of multiplied
        (fr(t, n * b), F(a, b)),                      # multiplied the bottom too
        (mixed(r, q, b) if r and q < b and r != q else None, None),   # swapped whole and top
        (mixed(q + 1, r, b), F(q + 1) + F(r, b)),     # off by one whole
        (mixed(q - 1, r, b) if q > 1 else None, None),
    ]
    return [(h, v) for h, v in out if h]


def mixed_e(t, b):
    q, r = divmod(t, b)
    return ("%s: %d ÷ %d = %d with %d left over, so %s = <b>%s</b>." %
            (fr(t, b), t, b, q, r, fr(t, b), mixed(q, r, b)))


# ============================================================ set 1: a/b as a multiple of 1/b
def set_unit(rnd):
    its = []
    # A) bar pictures: which multiplication matches?
    bars = [(5, 6), (3, 4), (7, 8), (2, 3), (4, 5), (7, 10), (5, 12)]
    for a, b in bars:
        right = times(a, 1, b)
        wrong = [times(b, 1, b), times(b, 1, a), "%d + %s" % (a, fr(1, b)), times(1, 1, b)]
        e = ("The bar has %d equal parts, so each part is %s. <b>%d parts</b> are shaded, so the shaded part is "
             "%s = %s." % (b, fr(1, b), a, right, fr(a, b)))
        its.append(mcq(fig(bar_svg(b, a)) + "Which multiplication matches the shaded part?", right, wrong, e, rnd))

    # B) a/b = ? × 1/b
    for a, b in [(5, 8), (3, 5), (9, 10), (4, 6), (11, 12), (7, 4)]:
        q = "%s = <b>?</b> × %s" % (fr(a, b), fr(1, b))
        e = "%s means <b>%d</b> pieces that are each %s, so %s = %s." % (fr(a, b), a, fr(1, b), fr(a, b), times(a, 1, b))
        if a > b:
            e += " A top number bigger than the bottom number is fine: it is more than 1 whole."
        wrong = [str(b), "1", str(b - a) if b > a else str(a + b), str(a + 1), str(a - 1)]
        its.append(mcq(q, str(a), wrong, e, rnd))

    # C) which fraction equals k × 1/b?
    for k, b in [(3, 8), (2, 5), (5, 3), (4, 10)]:
        q = "Which fraction is equal to %s?" % times(k, 1, b)
        e = ("%s means %d pieces that are each %s. The pieces stay the same size, so the bottom number stays %d: "
             "%s." % (times(k, 1, b), k, fr(1, b), b, fr(k, b)))
        its.append(mcq(q, (fr(k, b), F(k, b)), frac_wrongs(k, 1, b), e, rnd))

    # D) number-line jumps of 1/b
    for k, b in [(3, 4), (5, 6), (4, 3)]:
        right = times(k, 1, b)
        q = fig(jumps_svg(k, 1, b, show_end=True)) + "Which multiplication does the number line show?"
        wrong = [times(b, 1, k), times(b, 1, b), "%d + %s" % (k, fr(1, b)), times(k, 1, k + b)]
        e = ("Each whole has %d equal spaces, so each jump is %s. There are <b>%d jumps</b>: %s = %s."
             % (b, fr(1, b), k, right, fr(k, b)))
        its.append(mcq(q, right, wrong, e, rnd))
    assert len(its) == 20, len(its)
    return {"title": "Fractions as multiples of unit fractions", "items": its}


# ============================================================ set 2: whole number × unit fraction
def unit_e(n, b):
    e = "%s means %d pieces that are each %s. That is %s: the bottom number stays %d." % (
        times(n, 1, b), n, fr(1, b), fr(n, b), b)
    return e


def set_unit_times(rnd):
    its = []
    # equal groups pictures
    for n, b in [(4, 3), (3, 8), (5, 4), (2, 6), (6, 5), (4, 10)]:
        q = (fig(groups_svg(n, 1, b)) + "Each bar is 1 whole. %s of each bar is shaded. "
             "How much is shaded in all? Write the answer as a fraction." % fr(1, b))
        e = ("There are %d bars with %s shaded in each: %s. Count the shaded pieces: %d pieces of size %s = %s."
             % (n, fr(1, b), times(n, 1, b), n, fr(1, b), fr(n, b)))
        its.append(mcq(q, (fr(n, b), F(n, b)), frac_wrongs(n, 1, b), e, rnd))

    # number line jumps
    for n, b in [(5, 3), (3, 6), (7, 4), (2, 5), (5, 2), (8, 6)]:
        q = (fig(jumps_svg(n, 1, b)) + "Each jump is %s. Where does the last jump land? "
             "Write the answer as a fraction." % fr(1, b))
        e = ("Each whole has %d spaces, so one jump is %s. %d jumps: %s = %s." % (b, fr(1, b), n, times(n, 1, b), fr(n, b)))
        if n > b:
            e += " That is past 1, because %s is more than %s." % (fr(n, b), fr(b, b))
        its.append(mcq(q, (fr(n, b), F(n, b)), frac_wrongs(n, 1, b), e, rnd))

    # plain products
    for n, b in [(6, 4), (2, 3), (9, 10), (7, 8), (11, 12)]:
        q = "%s = <b>?</b>" % times(n, 1, b)
        its.append(mcq(q, (fr(n, b), F(n, b)), frac_wrongs(n, 1, b), unit_e(n, b), rnd))

    # missing whole number
    for n, b in [(7, 5), (3, 10), (5, 8)]:
        q = "<b>?</b> × %s = %s" % (fr(1, b), fr(n, b))
        e = "%s is %d pieces of size %s, so %s = %s. The missing number is <b>%d</b>." % (
            fr(n, b), n, fr(1, b), times(n, 1, b), fr(n, b), n)
        wrong = [str(b), str(n * b), "1", str(n + b), str(b - n) if b > n else str(n - b)]
        its.append(mcq(q, str(n), wrong, e, rnd))
    assert len(its) == 20, len(its)
    return {"title": "Whole number × unit fraction", "items": its}


# ============================================================ set 3: whole number × any fraction
def any_e(n, a, b):
    return ("%s = %s = %s. Multiply the whole number by the <b>top number</b> only (%d × %d = %d). "
            "The bottom number stays %d." % (times(n, a, b), times(n * a, 1, b), fr(n * a, b), n, a, n * a, b))


def set_any(rnd):
    its = []
    # equal groups pictures
    for n, a, b in [(3, 2, 5), (2, 3, 4), (4, 2, 3), (3, 5, 8)]:
        q = (fig(groups_svg(n, a, b)) + "Each bar is 1 whole and %s of each bar is shaded. "
             "How much is shaded in all? Write the answer as a fraction." % fr(a, b))
        e = ("%d bars with %d shaded pieces each: %d × %d = %d pieces of size %s. That is %s."
             % (n, a, n, a, n * a, fr(1, b), fr(n * a, b)))
        its.append(mcq(q, (fr(n * a, b), F(n * a, b)), frac_wrongs(n, a, b), e, rnd))

    # number line jumps of a/b
    for n, a, b in [(5, 2, 3), (3, 3, 4), (4, 3, 6)]:
        q = (fig(jumps_svg(n, a, b)) + "Each jump is %s. Where does the last jump land? "
             "Write the answer as a fraction." % fr(a, b))
        e = ("Each jump covers %d spaces of %s. %d jumps cover %d × %d = %d spaces: %s = %s."
             % (a, fr(1, b), n, n, a, n * a, times(n, a, b), fr(n * a, b)))
        if n * a % b == 0:
            e += " That lands on the whole number %d." % (n * a // b)
        its.append(mcq(q, (fr(n * a, b), F(n * a, b)), frac_wrongs(n, a, b), e, rnd))

    # plain products as fractions
    for n, a, b in [(4, 3, 10), (2, 5, 6), (7, 3, 8), (6, 5, 12), (3, 3, 5)]:
        q = "%s = <b>?</b><br>Write the answer as a fraction." % times(n, a, b)
        its.append(mcq(q, (fr(n * a, b), F(n * a, b)), frac_wrongs(n, a, b), any_e(n, a, b), rnd))

    # mixed numbers
    for n, a, b in [(8, 2, 3), (9, 3, 4), (2, 4, 5), (5, 3, 8), (3, 7, 10)]:
        t = n * a
        assert t > b and t % b and reduced(t, b)
        q = "%s = <b>?</b><br>Write the answer as a mixed number." % times(n, a, b)
        e = "First multiply: %s = %s. Then %s" % (times(n, a, b), fr(t, b), mixed_e(t, b))
        right = mixed_of(t, b)
        its.append(mcq(q, (right, F(t, b)), mixed_wrongs(n, a, b), e, rnd))

    # whole-number products
    for n, a, b in [(3, 2, 3), (4, 3, 4), (5, 2, 5)]:
        t = n * a
        w = t // b
        q = "%s = <b>?</b><br>Write the answer as a whole number." % times(n, a, b)
        e = ("%s = %s. %d pieces of size %s make %d wholes, because %d ÷ %d = %d. So the answer is <b>%d</b>."
             % (times(n, a, b), fr(t, b), t, fr(1, b), w, t, b, w, w))
        wrong = [str(t), fr(t, n * b), str(w + 1), str(n), str(t + b)]
        its.append(mcq(q, str(w), wrong, e, rnd))
    assert len(its) == 20, len(its)
    return {"title": "Whole number × fraction", "items": its}


# ============================================================ set 4: expressions, estimating, mistakes
def rep(a, b, n):
    return " + ".join([fr(a, b)] * n)


def set_reason(rnd, P):
    its = []
    # repeated addition
    for n, a, b in [(3, 3, 10), (4, 3, 4), (2, 7, 8), (3, 3, 8), (4, 2, 5)]:
        q = "Which addition has the same value as %s?" % times(n, a, b)
        wrong = [rep(n, b, a) if a != n and a <= 4 else rep(a, b, n + 1),
                 "%d + %s" % (n, fr(a, b)),
                 rep(a, n * b, n),
                 rep(a, b, n + 1)]
        e = "%s means %d groups of %s, so add %s %d times: %s = %s." % (
            times(n, a, b), n, fr(a, b), fr(a, b), n, rep(a, b, n), fr(n * a, b))
        its.append(mcq(q, rep(a, b, n), wrong, e, rnd))

    # equal to a multiple of a unit fraction
    for n, a, b in [(3, 2, 5), (2, 4, 6), (6, 3, 10), (2, 5, 12), (7, 2, 3)]:
        right = times(n * a, 1, b)
        wrong = [times(n * a, 1, n * b), times(b, 1, n * a), times(n, 1, b), times(n + a, 1, b)]
        e = ("%s is %d groups of %d pieces of size %s. That is %d × %d = %d pieces of size %s, so it equals %s."
             % (times(n, a, b), n, a, fr(1, b), n, a, n * a, fr(1, b), right))
        its.append(mcq("Which is equal to %s?" % times(n, a, b), right, wrong, e, rnd))

    # between which two whole numbers
    for n, a, b in [(8, 2, 5), (5, 3, 4), (3, 4, 5), (7, 1, 2), (5, 5, 8)]:
        t = n * a
        q_, r = divmod(t, b)
        assert r
        right = "%d and %d" % (q_, q_ + 1)
        wrong = ["%d and %d" % (t, t + 1), "0 and 1", "%d and %d" % (q_ + 1, q_ + 2),
                 "%d and %d" % (q_ - 1, q_) if q_ >= 1 else "%d and %d" % (n, n + 1)]
        e = ("%s = %s. %d ÷ %d = %d with %d left over, so %s = %s. That is between <b>%d and %d</b>."
             % (times(n, a, b), fr(t, b), t, b, q_, r, fr(t, b), mixed(q_, r, b), q_, q_ + 1))
        its.append(mcq("%s is between which two whole numbers?" % times(n, a, b), right, wrong, e, rnd))

    # find the mistake
    M = {
        "both": "multiplied the bottom number too",
        "add": "added instead of multiplying",
        "den": "multiplied only the bottom number",
        "mix": "wrote the mixed number wrong",
        "ok": "nothing; the answer is correct",
    }
    cases = [
        ("both", 4, 3, 5, fr(12, 20)),
        ("add", 2, 3, 8, mixed(2, 3, 8)),
        ("den", 5, 1, 6, fr(1, 30)),
        ("mix", 7, 2, 5, mixed(4, 2, 5)),
        ("ok", 2, 5, 8, fr(10, 8)),
    ]
    for kind, n, a, b, wrote in cases:
        nm, he, his = P.next()
        t = n * a
        q = "%s says %s = %s. What did %s do?" % (nm, times(n, a, b), wrote, he)

        def say(k):
            return cap(M[k]) + "." if k == "ok" else cap("%s %s." % (he, M[k]))
        right = say(kind)
        wrong = [say(k) for k in ["ok", "both", "add", "den", "mix"] if k != kind]
        if kind == "both":
            e = ("Only the top number is multiplied: %s = %s. %s multiplied %d by %d as well, but the pieces are still the same size (%s)."
                 % (times(n, a, b), fr(t, b), nm, b, n, fr(1, b)))
        elif kind == "add":
            e = ("%s wrote %d + %s. %s means %d groups of %s: %s = %s."
                 % (nm, n, fr(a, b), times(n, a, b), n, fr(a, b), rep(a, b, n), fr(t, b)))
        elif kind == "den":
            e = ("%s means %d pieces of size %s. Keep the bottom number: %s, not %s."
                 % (times(n, a, b), n, fr(1, b), fr(t, b), wrote))
        elif kind == "mix":
            e = ("%s = %s is right, but %s mixed up the whole number and the top number. %s"
                 % (times(n, a, b), fr(t, b), nm, mixed_e(t, b)))
        else:
            e = ("%s = %s = %s. Only the top number is multiplied, so %s is right."
                 % (times(n, a, b), times(t, 1, b), fr(t, b), nm))
        its.append(mcq(q, right, wrong, e, rnd))
    assert len(its) == 20, len(its)
    return {"title": "Expressions, estimating and finding mistakes", "items": its}


# ============================================================ set 5: word problems
UNITS = {
    "cup": ("cup", "cups"), "mile": ("mile", "miles"), "pound": ("pound", "pounds"), "yard": ("yard", "yards"),
    "hour": ("hour", "hours"), "can": ("can", "cans"), "meter": ("meter", "meters"), "inch": ("inch", "inches"),
    "foot": ("foot", "feet"), "stick": ("stick", "sticks"), "pizza": ("pizza", "pizzas"), "liter": ("liter", "liters"),
}


def qty(v, unit, form="mixed"):
    """A value (Fraction) with its unit. 1 or less uses the singular word."""
    one, many = UNITS[unit]
    word = one if v <= 1 else many
    if form == "frac" or v < 1:
        num = fr(v.numerator, v.denominator) if v.denominator > 1 else str(v.numerator)
    else:
        num = mixed_of(v.numerator, v.denominator)
    return "%s %s" % (num, word)


def word_wrongs(n, a, b, unit, form="mixed"):
    t = n * a
    out = []
    # multiplied top and bottom: written as an unsimplified fraction
    out.append(("%s %s" % (fr(t, n * b), UNITS[unit][0]), F(a, b)))
    out.append((qty(F(n) + F(a, b), unit), F(n) + F(a, b)))        # added instead of multiplying
    many = UNITS[unit][1]
    if form == "mixed" and t > b and t % b:
        q, r = divmod(t, b)
        if r != q and q < b:
            out.append(("%s %s" % (mixed(r, q, b), many), F(r) + F(q, b)))   # swapped whole and top
        out.append(("%s %s" % (mixed(q + 1, r, b), many), F(q + 1) + F(r, b)))
    if n + a > b:
        out.append(("%s %s" % (fr(n + a, b) if form == "frac" else mixed_of(n + a, b), many), F(n + a, b)))
    out.append(("%s %s" % (fr(a, n * b), UNITS[unit][0]), F(a, n * b)))
    out.append((qty(F(t), unit), F(t)))
    return out


def set_words(rnd, P):
    its = []

    def add(story, n, a, b, unit, how, form="mixed"):
        t = n * a
        v = F(t, b)
        assert form == "frac" or reduced(t, b), (story, t, b)
        right = qty(v, unit, form)
        e = "%s: %s = %s." % (how, times(n, a, b), fr(t, b))
        if form == "mixed" and t > b:
            if t % b:
                e += " As a mixed number, that is %s %s." % (mixed_of(t, b), UNITS[unit][1])
            else:
                e += " %d ÷ %d = %d, so that is %d %s." % (t, b, t // b, t // b, UNITS[unit][1] if t // b > 1 else UNITS[unit][0])
        q = story + ("<br>Write the answer as a fraction." if form == "frac" else "")
        its.append(mcq(q, (right, v), word_wrongs(n, a, b, unit, form), e, rnd))

    nm, he, his = P.next()
    add("A muffin recipe needs %s cup of flour for each batch. %s makes 5 batches. How much flour does %s need?"
        % (fr(3, 4), nm, he), 5, 3, 4, "cup", "5 batches of %s cup each" % fr(3, 4))
    nm, he, his = P.next()
    add("%s runs %s mile every day for 6 days. How far does %s run in all?" % (nm, fr(2, 3), he),
        6, 2, 3, "mile", "6 days of %s mile" % fr(2, 3))
    nm, he, his = P.next()
    add("Each bag of trail mix holds %s pound. %s fills 4 bags. How many pounds of trail mix is that?" % (fr(2, 5), nm),
        4, 2, 5, "pound", "4 bags of %s pound" % fr(2, 5))
    nm, he, his = P.next()
    add("%s walks %s dog for %s hour each day. How many hours does %s walk the dog in 7 days?" % (nm, his, fr(3, 4), he),
        7, 3, 4, "hour", "7 days of %s hour" % fr(3, 4))
    add("Each plant in a garden gets %s cup of water. There are 7 plants. How much water do they get in all?" % fr(2, 3),
        7, 2, 3, "cup", "7 plants with %s cup each" % fr(2, 3))
    nm, he, his = P.next()
    add("%s uses %s can of paint for each birdhouse. %s paints 9 birdhouses. How many cans of paint does %s use?"
        % (nm, fr(1, 4), cap(he), he), 9, 1, 4, "can", "9 birdhouses with %s can each" % fr(1, 4))
    nm, he, his = P.next()
    add("%s swims %s mile each morning. How far does %s swim in 3 mornings?" % (nm, fr(5, 8), he),
        3, 5, 8, "mile", "3 mornings of %s mile" % fr(5, 8))
    nm, he, his = P.next()
    add("%s cuts 7 pieces of wood. Each piece is %s meter long. What is the total length?" % (nm, fr(3, 10)),
        7, 3, 10, "meter", "7 pieces of %s meter" % fr(3, 10))
    nm, he, his = P.next()
    add("%s reads for %s hour every night. How long does %s read in 5 nights?" % (nm, fr(5, 6), he),
        5, 5, 6, "hour", "5 nights of %s hour" % fr(5, 6))
    nm, he, his = P.next()
    add("A cookie recipe uses %s cup of sugar for each batch. %s makes 2 batches. How much sugar does %s use?"
        % (fr(1, 3), nm, he), 2, 1, 3, "cup", "2 batches of %s cup" % fr(1, 3))
    add("It rained %s inch each day for 6 days. How much rain fell in all?" % fr(2, 5),
        6, 2, 5, "inch", "6 days of %s inch" % fr(2, 5))
    add("A snail crawls %s foot each minute. How far does it crawl in 8 minutes?" % fr(3, 5),
        8, 3, 5, "foot", "8 minutes of %s foot" % fr(3, 5))
    nm, he, his = P.next()
    add("%s makes 7 bows. Each bow uses %s yard of ribbon. How much ribbon does %s use?" % (nm, fr(5, 6), he),
        7, 5, 6, "yard", "7 bows with %s yard each" % fr(5, 6))
    add("Each loaf of banana bread needs %s stick of butter. A baker makes 9 loaves. How many sticks of butter are needed?"
        % fr(1, 2), 9, 1, 2, "stick", "9 loaves with %s stick each" % fr(1, 2))
    # fraction form
    nm, he, his = P.next()
    add("One lap around the track is %s mile. %s runs 7 laps. How far does %s run?" % (fr(1, 4), nm, he),
        7, 1, 4, "mile", "7 laps of %s mile" % fr(1, 4), form="frac")
    nm, he, his = P.next()
    add("%s pours %s liter of juice into each of 5 cups. How much juice does %s pour in all?" % (nm, fr(3, 8), he),
        5, 3, 8, "liter", "5 cups with %s liter each" % fr(3, 8), form="frac")
    # whole-number answer
    add("8 friends each eat %s of a pizza. All the pizzas are the same size. How many pizzas do they eat in all?" % fr(3, 8),
        8, 3, 8, "pizza", "8 friends with %s of a pizza each" % fr(3, 8))

    # which expression
    nm, he, his = P.next()
    q = ("%s fills 6 bottles with %s liter of water each. Which expression shows how much water %s uses?"
         % (nm, fr(3, 4), he))
    e = "6 bottles with %s liter in each is 6 equal groups of %s: 6 × %s. (It equals %s liters.)" % (fr(3, 4), fr(3, 4), fr(3, 4), fr(18, 4))
    its.append(mcq(q, times(6, 3, 4), ["6 + %s" % fr(3, 4), "6 − %s" % fr(3, 4), "%s + %s" % (fr(3, 4), fr(3, 4))], e, rnd))

    # how many to make (round up)
    nm, he, his = P.next()
    q = ("%s is making sandwiches for 5 friends. Each friend will eat %s of a sandwich. "
         "What is the fewest whole sandwiches %s must make?" % (nm, fr(3, 4), he))
    e = ("5 × %s = %s = %s sandwiches. 3 sandwiches are not enough, so %s must make <b>4</b>."
         % (fr(3, 4), fr(15, 4), mixed(3, 3, 4), he))
    its.append(mcq(q, "4 sandwiches", ["3 sandwiches", "15 sandwiches", "5 sandwiches", "20 sandwiches"], e, rnd))

    # compare two people
    (n1, h1, _), (n2, h2, _) = P.next(), P.next()
    q = ("%s runs %s mile a day for 5 days. %s runs %s mile a day for 6 days. Who runs farther?"
         % (n1, fr(3, 4), n2, fr(2, 3)))
    e = ("%s: 5 × %s = %s = %s miles. %s: 6 × %s = %s = 4 miles. 4 is more than %s, so <b>%s</b> runs farther."
         % (n1, fr(3, 4), fr(15, 4), mixed(3, 3, 4), n2, fr(2, 3), fr(12, 3), mixed(3, 3, 4), n2))
    its.append(mcq(q, n2, [n1, "They run the same distance", "You can’t tell"], e, rnd))
    assert len(its) == 20, len(its)
    return {"title": "Word problems", "items": its}


# ============================================================ lesson
def body_html():
    unit_fig = ("<figure class='sn-fig'>" + bar_svg(6, 5, W=320, H=50) +
                "<figcaption>Each part is " + fr(1, 6) + ". 5 parts are shaded: " + fr(5, 6) + " = 5 × " + fr(1, 6) + ".</figcaption></figure>")
    group_fig = ("<figure class='sn-fig'>" + groups_svg(3, 2, 5) +
                 "<figcaption>3 groups of " + fr(2, 5) + ": 3 × 2 = 6 shaded fifths, so 3 × " + fr(2, 5) + " = " + fr(6, 5) + ".</figcaption></figure>")
    line_fig = ("<figure class='sn-fig'>" + jumps_svg(3, 2, 5, W=400) +
                "<figcaption>3 jumps of " + fr(2, 5) + " land on " + fr(6, 5) + ", which is " + mixed(1, 1, 5) + ".</figcaption></figure>")
    return (
        "<h2>The big idea</h2>"
        "<p>Every fraction is made of <b>unit fractions</b> (fractions with 1 on top). "
        + fr(5, 6) + " is 5 pieces that are each " + fr(1, 6) + ", so " + fr(5, 6) + " = 5 × " + fr(1, 6) + ".</p>"
        + unit_fig +
        "<p>To multiply a whole number by a fraction, count the pieces. "
        "<b>Multiply the top number by the whole number. Keep the bottom number.</b> "
        "The bottom number tells the size of the pieces, and the size does not change.</p>"
        + table(["Problem", "Think", "Answer"], [
            [times(4, 1, 3), "4 pieces of size " + fr(1, 3), fr(4, 3)],
            [times(3, 2, 5), "3 × 2 = 6 pieces of size " + fr(1, 5), fr(6, 5)],
            [times(5, 3, 4), "5 × 3 = 15 pieces of size " + fr(1, 4), fr(15, 4)],
        ]) +
        "<h2>Example with pictures</h2>"
        + group_fig + line_fig
        + ex("Example", "Find " + times(3, 2, 5) + ". Write the answer as a mixed number.",
             "3 × " + fr(2, 5) + " = " + fr(6, 5) + ". Five fifths make 1 whole, and 1 fifth is left over.",
             mixed(1, 1, 5))
        + "<h2>Changing to a mixed number</h2>"
        "<p>Divide the top number by the bottom number. The answer is the whole number, and the remainder is the new top number.</p>"
        + ex("Example", "A recipe needs " + fr(3, 4) + " cup of milk for each batch. How much milk for 5 batches?",
             "5 × " + fr(3, 4) + " = " + fr(15, 4) + ". 15 ÷ 4 = 3 with 3 left over.",
             mixed(3, 3, 4) + " cups")
        + "<p>Multiplying by a fraction less than 1 gives an answer <b>smaller than the whole number</b>: "
        "5 × " + fr(3, 4) + " is less than 5.</p>"
        + "<h2>Common mistakes</h2>"
        + table(["Mistake", "What to do instead"], [
            ["3 × " + fr(2, 5) + " = " + fr(6, 15) + " (multiplying the bottom too)", "Keep the bottom number: " + fr(6, 5)],
            ["3 × " + fr(2, 5) + " = 3 " + fr(2, 5) + " (adding)", "3 × means 3 groups of " + fr(2, 5)],
            [fr(15, 4) + " = 4 " + fr(3, 4) + " (wrong whole number)", "15 ÷ 4 = 3 R 3, so " + fr(15, 4) + " = " + mixed(3, 3, 4)],
            ["Thinking the answer must be less than 1", "Fractions can be more than 1: " + fr(6, 5) + " &gt; 1"],
        ])
    )


FAQ = [
    {"q": "How do you multiply a fraction by a whole number?",
     "a": "Multiply the top number (numerator) by the whole number and keep the bottom number. For example, 3 × 2/5 = 6/5, which is 1 1/5."},
    {"q": "Why doesn't the denominator change when you multiply by a whole number?",
     "a": "The denominator tells the size of each piece. 3 × 2/5 means 3 groups of 2 fifths, so you get more fifths, not smaller pieces."},
    {"q": "What does 4.NF.B.4 mean?",
     "a": "Standard 4.NF.B.4 asks 4th graders to see a fraction like 5/6 as 5 × 1/6, multiply a whole number by a fraction, and solve word problems such as 5 servings of 3/4 cup."},
    {"q": "How do you use a number line to multiply a fraction by a whole number?",
     "a": "Make jumps the size of the fraction from 0. For 4 × 2/3, make 4 jumps of 2/3; you land on 8/3, which is 2 2/3."},
]


def gen():
    rnd = random.Random(106)
    P = People(rnd)
    sets = [set_unit(rnd), set_unit_times(rnd), set_any(rnd), set_reason(rnd, P), set_words(rnd, P)]
    for s in sets:
        assert len(s["items"]) == 20
        for it in s["items"]:
            assert len(set(it["c"])) == 4, it
    return {
        "country": "us", "subject": "math", "grade": "grade-4", "slug": "multiply-fractions-by-whole-numbers", "sort": 6,
        "updated": UPDATED, "pdf_url": "",
        "title": "Multiply Fractions by Whole Numbers",
        "seo_title": "Grade 4 Multiplying Fractions by Whole Numbers Worksheets: Models, Number Lines, Mixed Numbers and Word Problems",
        "short_title": "Multiply fractions by whole numbers",
        "domain": "Number and Operations—Fractions",
        "standard_code": "4.NF.B.4",
        "standard_url": "https://www.thecorestandards.org/Math/Content/4/NF/B/4/",
        "standard_text": "Apply and extend previous understandings of multiplication to multiply a fraction by a whole number. Understand a fraction a/b as a multiple of 1/b. Understand a multiple of a/b as a multiple of 1/b, and use this understanding to multiply a fraction by a whole number. Solve word problems involving multiplication of a fraction by a whole number.",
        "meta_desc": "Free Grade 4 worksheets on multiplying fractions by whole numbers: see 5/6 as 5 × 1/6, use equal groups and number lines, write answers as fractions or mixed numbers, and solve recipe and distance word problems. 100 practice questions with answers.",
        "key_big": "Multiply the top number by the whole number. Keep the bottom number.",
        "key_sub": "3 × 2/5 means 3 groups of 2 fifths: 6 fifths, or 6/5. The pieces stay fifths, so the bottom number does not change. 6/5 is the same as 1 1/5.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    mark_large(u, "(number line|[0-9]+ bars, each split into (8|10|12) )")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(u, f, ensure_ascii=False, indent=1)
    print("wrote", path)
