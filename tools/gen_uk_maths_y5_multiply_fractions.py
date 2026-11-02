# -*- coding: utf-8 -*-
"""
UK Year 5 Maths: Multiplying Fractions by Whole Numbers (National Curriculum in England)
  python3 tools/gen_uk_maths_y5_multiply_fractions.py
Year 5 multiplies proper fractions and mixed numbers by whole numbers, supported by diagrams.
Fraction × fraction is Year 6, so it is not used here.
Every answer is checked with fractions.Fraction; no two choices are equal in value.
HTML attributes use single quotes (no backslashes in the JSON). British English.
"""
import json, math, os, random, re
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "uk", "maths", "year-5")
UPDATED = "2026-11-02"
DARK = "#4fae74"      # shaded part
LINE = "#2b2b2b"
RED = "#d6453b"
FONT = "Arial, Helvetica, sans-serif"
GIRLS = ["Amelia", "Isla", "Freya", "Poppy", "Ava", "Aisha", "Lily", "Zara", "Grace", "Ruby", "Maya", "Evie"]
BOYS = ["Oliver", "Harry", "Mohammed", "Jack", "Arjun", "Noah", "George", "Leo", "Alfie", "Kai", "Ethan", "Charlie"]


# ------------------------------------------------------------ helpers
def f(n):
    return "{:,}".format(n)


def fr(a, b):
    return "<span class='fr'><span class='fn'>%d</span><span class='fd'>%d</span></span>" % (a, b)


def mixed(w, a, b):
    """A mixed number exactly as written (not simplified)."""
    return "%s %s" % (f(w), fr(a, b))


def show(v):
    """A Fraction in simplest form: whole number, proper fraction or mixed number."""
    v = F(v)
    q, r = divmod(v.numerator, v.denominator)
    if r == 0:
        return f(q)
    if q == 0:
        return fr(r, v.denominator)
    return mixed(q, r, v.denominator)


def R(n, d):
    """A fraction exactly as a pupil wrote it (not simplified), with its value."""
    return (fr(n, d), F(n, d))


def S(v):
    v = F(v)
    return (show(v), v)


def M(w, a, b):
    return (mixed(w, a, b), w + F(a, b))


def with_unit(c, unit):
    """Add a unit to a (html, value) choice; unit is (singular, plural)."""
    if not unit:
        return c
    h, v = c
    return ("%s %s" % (h, unit[0] if v <= 1 else unit[1]), v)


def mcq(q, correct, cands, e):
    """correct and cands are (html, value). A candidate equal in value to an earlier choice is skipped."""
    ch, vals = [correct[0]], [correct[1]]
    for h, v in cands:
        if not h or h in ch or (v is not None and v in vals) or (v is not None and v <= 0):
            continue
        ch.append(h)
        vals.append(v)
        if len(ch) == 4:
            break
    assert len(ch) == 4, (q, correct, cands)
    return {"q": q, "c": ch, "a": 0, "e": e}


def balance(sets, rnd):
    """Spread the correct answers evenly over the 4 positions in every set."""
    for s in sets:
        targets = [0, 1, 2, 3] * 5
        rnd.shuffle(targets)
        for it, t in zip(s["items"], targets):
            c = it["c"]
            wrong = [x for i, x in enumerate(c) if i != it["a"]]
            rnd.shuffle(wrong)
            right = c[it["a"]]
            it["c"] = wrong[:t] + [right] + wrong[t:]
            it["a"] = t


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


def fig(svg):
    return "<div class='qfig'>" + svg + "</div>"


def svg_wrap(w, h, body, label):
    return ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 %d %d' width='%d' height='%d' "
            "role='img' aria-label='%s'><g font-family='%s'>%s</g></svg>" % (w, h, w, h, label, FONT, body))


def table(head, rows):
    h = "".join("<th>%s</th>" % x for x in head)
    b = "".join("<tr>" + "".join("<td>%s</td>" % c for c in r) + "</tr>" for r in rows)
    return "<div class='sn-tw'><table class='sn-table'><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>" % (h, b)


def ex(title, q, s, a):
    return ("<div class='sn-ex'><span class='sn-ex-t'>%s</span><p class='sn-ex-q'>%s</p>"
            "<p class='sn-ex-s'>%s</p><p class='sn-ex-a'>Answer: %s</p></div>" % (title, q, s, a))


def mark_large(u, pattern):
    """Tag wide pictures that must print larger so they stay readable."""
    rx = re.compile(r"<svg (?=[^>]*aria-label='" + pattern + ")")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u


def nf(n, a, b):
    return "%d × %s" % (n, fr(a, b))


def fn(n, a, b):
    return "%s × %d" % (fr(a, b), n)


def mn(n, w, a, b):
    return "%s × %d" % (mixed(w, a, b), n)


# ------------------------------------------------------------ figures
def text(x, y, t, fs=18, col=LINE, anchor="middle", weight="700"):
    return ("<text x='%.1f' y='%.1f' font-size='%d' font-weight='%s' fill='%s' text-anchor='%s'>%s</text>"
            % (x, y, fs, weight, col, anchor, t))


def bar(x0, y0, BW, BH, b, k):
    return "".join("<rect x='%.1f' y='%.1f' width='%.2f' height='%d' fill='%s' stroke='%s' stroke-width='2'/>"
                   % (x0 + i * BW / float(b), y0, BW / float(b), BH, DARK if i < k else "#fff", LINE)
                   for i in range(b))


def groups_svg(n, a, b, BW=96, BH=34, GX=18, GY=14):
    """n bars (each 1 whole) split into b parts, a parts of each shaded. Up to 3 bars per row."""
    cols = min(n, 3)
    rows = (n + cols - 1) // cols
    s = [bar(6 + (g % cols) * (BW + GX), 6 + (g // cols) * (BH + GY), BW, BH, b, a) for g in range(n)]
    W = cols * BW + (cols - 1) * GX + 12
    H = rows * BH + (rows - 1) * GY + 12
    return svg_wrap(W, H, "".join(s), "%d bars, each split into %d equal parts with %d shaded" % (n, b, a))


def jumps_svg(n, a, b, W=440):
    """Number line from 0 to the next whole number at or above n*a/b, ticks every 1/b, n jumps of a/b."""
    wholes = max(1, -(-n * a // b))
    total = wholes * b
    L, Rr, Y = 18, W - 18, 62

    def X(i):
        return L + (Rr - L) * i / float(total)
    s = ["<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='2.5'/>" % (L, Y, Rr, Y, LINE)]
    for i in range(total + 1):
        whole = (i % b == 0)
        s.append("<line x1='%.1f' y1='%d' x2='%.1f' y2='%d' stroke='%s' stroke-width='%s'/>"
                 % (X(i), Y - (12 if whole else 7), X(i), Y + (12 if whole else 7), LINE, "2.5" if whole else "1.6"))
        if whole:
            s.append(text(X(i), Y + 34, str(i // b)))
    h = 40 if a > 1 else 30
    for j in range(n):
        x0, x1 = X(j * a), X((j + 1) * a)
        s.append("<path d='M%.1f %d Q%.1f %d %.1f %d' fill='none' stroke='%s' stroke-width='2.5'/>"
                 % (x0, Y - 2, (x0 + x1) / 2, Y - 2 - h, x1, Y - 2, RED))
        s.append("<path d='M%.1f %d l-7 -9 l9 1 z' fill='%s'/>" % (x1, Y - 2, RED))
    s.append("<circle cx='%.1f' cy='%d' r='6' fill='%s'/>" % (X(n * a), Y, RED))
    return svg_wrap(W, Y + 42, "".join(s),
                    "number line from 0 to %d with %d jumps of %d/%d" % (wholes, n, a, b))


def tape_svg(q, a, b, part_labels=False, Wt=300):
    """A bar worth q split into b equal parts, a parts shaded; the total is marked above."""
    x0, y0, H = 6, 36, 36
    s = ["<line x1='%d' y1='16' x2='%d' y2='16' stroke='%s' stroke-width='2'/>" % (x0, x0 + Wt, LINE),
         "<line x1='%d' y1='10' x2='%d' y2='26' stroke='%s' stroke-width='2'/>" % (x0, x0, LINE),
         "<line x1='%d' y1='10' x2='%d' y2='26' stroke='%s' stroke-width='2'/>" % (x0 + Wt, x0 + Wt, LINE)]
    lab = f(q)
    lw = len(lab) * 18 * 0.6 + 12
    s.append("<rect x='%.1f' y='4' width='%.1f' height='24' fill='#fff'/>" % (x0 + Wt / 2 - lw / 2, lw))
    s.append(text(x0 + Wt / 2, 23, lab, 18))
    pw = Wt / float(b)
    for i in range(b):
        s.append("<rect x='%.1f' y='%d' width='%.1f' height='%d' fill='%s' stroke='%s' stroke-width='2'/>"
                 % (x0 + i * pw, y0, pw, H, DARK if i < a else "#fff", LINE))
        if part_labels:
            s.append(text(x0 + i * pw + pw / 2, y0 + 24, f(q // b), 16, "#fff" if i < a else LINE))
    return svg_wrap(Wt + 12, y0 + H + 6, "".join(s), "bar model worth %d split into %d equal parts with %d shaded" % (q, b, a))


def rows_svg(n, w, a, b, BW=64, BH=26, GX=10, GY=12):
    """n rows; each row shows the mixed number w a/b: w full bars and one bar with a of b parts shaded."""
    s = []
    for r in range(n):
        y0 = 6 + r * (BH + GY)
        for k in range(w + 1):
            s.append(bar(6 + k * (BW + GX), y0, BW, BH, b, b if k < w else a))
    W = (w + 1) * BW + w * GX + 12
    H = n * BH + (n - 1) * GY + 12
    return svg_wrap(W, H, "".join(s), "rows of bars: %d rows, each showing %d and %d/%d" % (n, w, a, b))


# ------------------------------------------------------------ fraction × whole number
def pw_e(n, a, b, lead=""):
    """Explanation for n × a/b."""
    t = n * a
    s = (lead + "Multiply the numerator by the whole number and keep the denominator: %d × %d = %d, so the answer is %s."
         % (n, a, t, fr(t, b)))
    q, r = divmod(t, b)
    if t < b:
        if math.gcd(t, b) > 1:
            s += " Simplify: <b>%s</b>." % show(F(t, b))
        else:
            s = s[:-len(fr(t, b)) - 1] + "<b>%s</b>." % fr(t, b)
    elif r == 0:
        s += " %d ÷ %d = %d, so the answer is <b>%d</b>." % (t, b, q, q)
    else:
        s += " %d ÷ %d = %d remainder %d, so %s = %s" % (t, b, q, r, fr(t, b), mixed(q, r, b))
        if math.gcd(r, b) > 1:
            s += " = <b>%s</b>." % show(F(t, b))
        else:
            s = s[:-len(mixed(q, r, b))] + "<b>%s</b>." % mixed(q, r, b)
    return s


def pw_wrongs(n, a, b, order):
    """n × a/b: (html, value) from real mistakes."""
    v = F(n * a, b)
    q, r = divmod(n * a, b)
    out = []
    for k in order:
        if k == "both":                         # multiplied the numerator and the denominator
            out.append(R(n * a, n * b))
        elif k == "bottom":                     # multiplied the denominator only
            out.append(R(a, n * b))
        elif k == "addtop":                     # added the whole number to the numerator
            out.append(R(n + a, b))
        elif k == "add":                        # added the whole number
            out.append(M(n, a, b))
        elif k == "up":                         # one whole too many when changing to a mixed number
            out.append(S(v + 1))
        elif k == "down":                       # one whole too few
            if v > 1:
                out.append(S(v - 1))
        elif k == "swap":                       # wrote the remainder as the whole number
            if r and q and q < b and q != r:
                out.append(M(r, q, b))
        elif k == "nodiv":                      # forgot the denominator
            out.append((f(n * a), F(n * a)))
        elif k == "remover":                    # wrote the remainder over the numerator
            if r and q:
                out.append(M(q, r, n * a))
        else:
            raise ValueError(k)
    return out


# ------------------------------------------------------------ fraction of an amount
def of_e(a, b, q, unit="", after=""):
    p = q // b
    return ("Divide by the denominator: %s%s ÷ %d = %s%s in each part. Multiply by the numerator: %d × %s%s = %s%s. "
            "So %s of %s%s = <b>%s%s%s</b>." % (unit, f(q), b, unit, f(p), a, unit, f(p), unit, f(a * p),
                                                fr(a, b), unit, f(q), unit, f(a * p), after))


def of_wrongs(a, b, q, order, unit="", after=""):
    out = []
    for k in order:
        if k == "one":                          # stopped after dividing
            v = F(q, b)
        elif k == "unshaded":                   # found the other part
            v = F((b - a) * q, b)
        elif k == "times":                      # multiplied by the numerator only
            v = F(a * q)
        elif k == "swap":                       # divided by the numerator, multiplied by the denominator
            if q % a or a == 1:
                continue
            v = F(q // a * b)
        elif k == "both":                       # multiplied the numerator and the denominator
            if unit or after:
                continue
            out.append(R(a * q, b * q))
            continue
        else:
            raise ValueError(k)
        if v.denominator == 1:
            out.append(("%s%s%s" % (unit, f(v.numerator), after), v))
    return out


# ------------------------------------------------------------ mixed number × whole number
def mx_e(n, w, a, b):
    v = n * w + F(n * a, b)
    t = n * a
    s = ("Partition %s into %d and %s. Multiply each part by %d: %d × %d = %d and %s × %d = %s"
         % (mixed(w, a, b), w, fr(a, b), n, w, n, n * w, fr(a, b), n, fr(t, b)))
    if t >= b:
        s += " = %s" % show(F(t, b))
        s += ". Add: %d + %s = <b>%s</b>." % (n * w, show(F(t, b)), show(v))
    else:
        s += ". Add: %d + %s = <b>%s</b>." % (n * w, fr(t, b), show(v))
    return s


def mx_wrongs(n, w, a, b, order):
    v = n * w + F(n * a, b)
    out = []
    for k in order:
        if k == "whole":                        # multiplied only the whole number
            out.append(S(n * w + F(a, b)))
        elif k == "frac":                       # multiplied only the fraction
            out.append(S(w + F(n * a, b)))
        elif k == "add":                        # added the whole number
            out.append(S(w + n + F(a, b)))
        elif k == "lost":                       # forgot the whole made from the fraction part
            if n * a >= b:
                out.append(S(n * w + F(n * a % b, b)))
        elif k == "up":
            out.append(S(v + 1))
        elif k == "down":
            out.append(S(v - 1))
        elif k == "both":                       # multiplied the whole, numerator and denominator
            out.append(M(n * w, n * a, n * b))
        else:
            raise ValueError(k)
    return out


def rot(order, i):
    i %= len(order)
    return order[i:] + order[:i]


# ============================================================ set 1: repeated addition
def set_repeat():
    its = []
    # A) bar pictures
    for i, (n, a, b) in enumerate([(3, 2, 5), (4, 1, 3), (5, 1, 4), (3, 4, 7), (3, 3, 8), (4, 2, 5)]):
        q = (fig(groups_svg(n, a, b)) + "Each bar is 1 whole. There are %d bars with %s shaded in each. "
             "What is %s?" % (n, fr(a, b), nf(n, a, b)))
        t = n * a
        e = ("Count the shaded parts: %d lots of %d is %d × %d = %d. Each part is %s, so %s = %s"
             % (n, a, n, a, t, fr(1, b), nf(n, a, b), fr(t, b)))
        if t > b:
            e += ", which is %s" % show(F(t, b))
        e += ". The parts are still %s, so the denominator stays %d." % ("quarters" if b == 4 else "the same size", b)
        e = e.replace(fr(t, b) + ", which", "<b>%s</b>, which" % fr(t, b), 1) if t > b else e.replace(
            "= %s." % fr(t, b), "= <b>%s</b>." % fr(t, b), 1)
        its.append(mcq(q, R(t, b), pw_wrongs(n, a, b, rot(["both", "addtop", "bottom", "add"], i)), e))
    # B) which addition is the same
    for n, a, b in [(4, 3, 8), (3, 2, 9), (5, 2, 3)]:
        plus = lambda k: " + ".join([fr(a, b)] * k)
        q = "Which addition is the same as %s?" % nf(n, a, b)
        cands = [(plus(n - 1), F((n - 1) * a, b)),
                 ("%s + %s" % (fr(n, b), fr(a, b)), F(n + a, b)),
                 ("%d + %s" % (n, fr(a, b)), n + F(a, b))]
        e = ("%s means %d lots of %s, so add %s %d times: %s = %s."
             % (nf(n, a, b), n, fr(a, b), fr(a, b), n, plus(n), fr(n * a, b)))
        its.append(mcq(q, (plus(n), F(n * a, b)), cands, e.replace("%s." % fr(n * a, b), "<b>%s</b>." % fr(n * a, b))))
    # C) repeated addition to a total
    for i, (n, a, b) in enumerate([(4, 2, 9), (5, 1, 8), (3, 3, 10)]):
        plus = " + ".join([fr(a, b)] * n)
        q = "%s = <b>?</b>" % plus
        cands = [R(n * a, n * b), R((n - 1) * a, b), R(n + a, b), R(a, n * b)]
        e = ("Add the numerators and keep the denominator, because the parts are all %s: %s. "
             "This is the same as %s. Do not add the denominators."
             % ({9: "ninths", 8: "eighths", 10: "tenths"}[b], plus + " = <b>%s</b>" % fr(n * a, b), nf(n, a, b)))
        its.append(mcq(q, R(n * a, b), rot(cands, i), e))
    # D) calculate
    for i, (n, a, b) in enumerate([(3, 2, 7), (4, 1, 5), (2, 4, 9), (7, 1, 10), (5, 1, 5), (3, 2, 3), (4, 3, 4), (3, 3, 11)]):
        form = nf if i % 2 == 0 else fn
        q = "%s = <b>?</b>" % form(n, a, b)
        v = F(n * a, b)
        if v.denominator == 1:
            order = rot(["both", "nodiv", "addtop", "bottom"], i)
        else:
            order = rot(["both", "addtop", "bottom", "add"], i)
        e = pw_e(n, a, b)
        if form is fn:
            e = "%s is the same as %s. " % (fn(n, a, b), nf(n, a, b)) + e
        its.append(mcq(q, S(v), pw_wrongs(n, a, b, order), e))
    assert len(its) == 20, len(its)
    return {"title": "Repeated addition and bar models", "items": its}


# ============================================================ set 2: answers as mixed numbers
def set_mixed_answers(P):
    its = []
    # A) number lines
    for i, (n, a, b) in enumerate([(4, 2, 3), (5, 3, 4), (3, 3, 5), (6, 2, 5)]):
        q = (fig(jumps_svg(n, a, b)) + "The number line shows %d jumps of %s. What is %s?<br>Give your answer as a mixed number."
             % (n, fr(a, b), nf(n, a, b)))
        e = "The jumps end at %s. " % show(F(n * a, b)) + pw_e(n, a, b)
        its.append(mcq(q, S(F(n * a, b)), pw_wrongs(n, a, b, rot(["add", "both", "up", "swap", "down"], i)), e))
    # B) calculate
    cases = [(5, 2, 3), (7, 2, 5), (9, 2, 7), (3, 7, 8), (5, 4, 9), (8, 3, 5), (7, 3, 4), (11, 2, 3), (5, 7, 12),
             (6, 3, 4), (3, 5, 6), (4, 7, 10)]
    for i, (n, a, b) in enumerate(cases):
        form = fn if i % 2 == 0 else nf
        simp = math.gcd(n * a % b, b) > 1
        q = "%s = <b>?</b><br>Give your answer as a mixed number%s." % (form(n, a, b), " in its simplest form" if simp else "")
        order = rot(["add", "both", "up", "swap", "down", "remover"], i)
        its.append(mcq(q, S(F(n * a, b)), pw_wrongs(n, a, b, order), pw_e(n, a, b)))
    # C) reasoning
    q = "Which multiplication has an answer between 2 and 3?"
    its.append(mcq(q, (nf(3, 3, 4), None), [(nf(4, 1, 5), None), (nf(5, 2, 3), None), (nf(2, 5, 6), None)],
                   "%s = %s = %s, which is between 2 and 3. %s = %s, %s = %s = %s and %s = %s = %s."
                   % (nf(3, 3, 4), fr(9, 4), mixed(2, 1, 4), nf(4, 1, 5), fr(4, 5), nf(5, 2, 3), fr(10, 3),
                      mixed(3, 1, 3), nf(2, 5, 6), fr(10, 6), mixed(1, 2, 3))))
    for x in [F(9, 4)]:
        assert 2 < x < 3
    for x in [F(4, 5), F(10, 3), F(10, 6)]:
        assert not 2 < x < 3
    q = "<b>?</b> × %s = %s" % (fr(3, 5), mixed(2, 2, 5))
    its.append(mcq(q, ("4", F(4)), [("2", F(2)), ("12", F(12)), ("5", F(5))],
                   "Change %s to an improper fraction: 2 × 5 + 2 = 12, so it is %s. "
                   "The denominator stays 5, so <b>?</b> × 3 = 12. 12 ÷ 3 = <b>4</b>. Check: 4 × %s = %s = %s."
                   % (mixed(2, 2, 5), fr(12, 5), fr(3, 5), fr(12, 5), mixed(2, 2, 5))))
    nm, he, his = P.next()
    q = "%s says %s = %s. What mistake did %s make?" % (nm, nf(4, 2, 3), fr(8, 12), he)
    its.append(mcq(q, (cap("%s multiplied the denominator by 4 as well." % he), None),
                   [(cap("%s added 4 instead of multiplying." % he), None),
                    (cap("%s forgot to change it to a mixed number." % he), None),
                    ("There is no mistake.", None)],
                   "%s = %s, so %s did not change the size at all. Only the numerator is multiplied: 4 × 2 = 8, "
                   "and the parts are still thirds. %s = %s = <b>%s</b>." % (fr(8, 12), fr(2, 3), nm, nf(4, 2, 3),
                                                                            fr(8, 3), mixed(2, 2, 3))))
    nm, he, his = P.next()
    q = "%s works out %s = %s. Which mixed number is the same as %s?" % (nm, nf(7, 3, 4), fr(21, 4), fr(21, 4))
    its.append(mcq(q, M(5, 1, 4), [M(4, 1, 4), M(6, 1, 4), M(5, 1, 21), M(5, 3, 4)],
                   "21 ÷ 4 = 5 remainder 1 (5 × 4 = 20). 5 wholes and 1 quarter left over: %s = <b>%s</b>."
                   % (fr(21, 4), mixed(5, 1, 4))))
    assert len(its) == 20, len(its)
    return {"title": "Fraction × whole number with mixed-number answers", "items": its}


# ============================================================ set 3: fractions of amounts
def set_amounts():
    its = []
    for i, (form, a, b, q) in enumerate([("of", 2, 3, 12), ("fq", 3, 4, 20), ("qf", 3, 5, 25), ("fq", 5, 6, 24),
                                         ("of", 4, 9, 36)]):
        if form == "of":
            ask = "Find %s of %d." % (fr(a, b), q)
        elif form == "fq":
            ask = "%s × %d = <b>?</b>" % (fr(a, b), q)
        else:
            ask = "%d × %s = <b>?</b>" % (q, fr(a, b))
        qq = fig(tape_svg(q, a, b)) + "The whole bar is %d. " % q + ask
        e = of_e(a, b, q)
        if form != "of":
            e = "× means “of”. " + e
        order = rot(["one", "times", "unshaded", "swap", "both"], i)
        its.append(mcq(qq, S(F(a * q, b)), of_wrongs(a, b, q, order), e))
    cases = [("of", 3, 8, 32), ("fq", 3, 4, 28), ("qf", 3, 5, 40), ("of", 2, 7, 35), ("fq", 5, 6, 42), ("qf", 4, 5, 45),
             ("of", 7, 10, 60), ("fq", 2, 9, 54), ("qf", 3, 4, 100), ("of", 5, 8, 64), ("fq", 5, 12, 60), ("qf", 7, 9, 63)]
    for i, (form, a, b, q) in enumerate(cases):
        if form == "of":
            qq = "Find %s of %d." % (fr(a, b), q)
        elif form == "fq":
            qq = "%s × %d = <b>?</b>" % (fr(a, b), q)
        else:
            qq = "%d × %s = <b>?</b>" % (q, fr(a, b))
        e = of_e(a, b, q)
        if form != "of":
            e = "× means “of”. " + e
        order = rot(["times", "one", "swap", "unshaded", "both"], i)
        its.append(mcq(qq, S(F(a * q, b)), of_wrongs(a, b, q, order), e))
    # reasoning
    its.append(mcq("Which calculation gives the same answer as %s × 20?" % fr(3, 4),
                   ("20 ÷ 4 × 3", F(15)), [("20 ÷ 3 × 4", F(80, 3)), ("20 ÷ 4", F(5)), ("20 × 3", F(60))],
                   "%s × 20 means %s of 20: divide by the denominator, then multiply by the numerator. "
                   "<b>20 ÷ 4 × 3</b> = 5 × 3 = 15." % (fr(3, 4), fr(3, 4))))
    qq = ("<span class='fr'><span class='fn'><b>?</b></span><span class='fd'>5</span></span> of 30 = 18. "
          "What is the missing numerator?")
    its.append(mcq(qq, ("3", F(3)), [("6", F(6)), ("2", F(2)), ("12", F(12))],
                   "One fifth of 30 is 30 ÷ 5 = 6. 18 ÷ 6 = 3, so 18 is 3 fifths: %s of 30 = 18. "
                   "The missing numerator is <b>3</b>." % fr(3, 5)))
    qq = "Which is greater: %s of 15 or %s of 20?" % (fr(2, 3), fr(3, 5))
    its.append(mcq(qq, ("%s of 20" % fr(3, 5), None),
                   [("%s of 15" % fr(2, 3), None), ("They are equal.", None), ("You can’t tell.", None)],
                   "%s of 15: 15 ÷ 3 = 5, 5 × 2 = 10. %s of 20: 20 ÷ 5 = 4, 4 × 3 = 12. 12 is greater than 10, "
                   "so <b>%s of 20</b> is greater." % (fr(2, 3), fr(3, 5), fr(3, 5))))
    assert len(its) == 20, len(its)
    return {"title": "Fractions of amounts: × means “of”", "items": its}


# ============================================================ set 4: mixed number × whole number
def set_mixed_numbers(P):
    its = []
    # A) pictures, no exchange
    for i, (n, w, a, b) in enumerate([(3, 2, 1, 4), (2, 1, 2, 5), (4, 1, 1, 5), (2, 2, 1, 3)]):
        q = (fig(rows_svg(n, w, a, b)) + "Each row shows %s. There are %d rows. What is %s?"
             % (mixed(w, a, b), n, mn(n, w, a, b)))
        e = "Count the whole bars: %d × %d = %d. Count the shaded parts in the last column: %d × %d = %d %s. " % (
            n, w, n * w, n, a, n * a, {4: "quarters", 5: "fifths", 3: "thirds"}[b]) + mx_e(n, w, a, b)
        its.append(mcq(q, S(n * w + F(n * a, b)), mx_wrongs(n, w, a, b, rot(["whole", "frac", "add", "up"], i)), e))
    # B) no exchange
    for i, (n, w, a, b) in enumerate([(3, 1, 2, 7), (2, 3, 2, 5), (4, 2, 1, 5), (3, 4, 2, 7), (2, 5, 4, 9), (5, 1, 1, 6),
                                      (3, 3, 1, 4), (2, 7, 1, 3)]):
        q = ("%s = <b>?</b>" % mn(n, w, a, b)) if i % 2 == 0 else ("%d × %s = <b>?</b>" % (n, mixed(w, a, b)))
        its.append(mcq(q, S(n * w + F(n * a, b)), mx_wrongs(n, w, a, b, rot(["whole", "frac", "add", "up", "both"], i)),
                       mx_e(n, w, a, b)))
    # C) the fraction part makes more than 1 whole
    for i, (n, w, a, b) in enumerate([(3, 1, 2, 5), (5, 1, 1, 2), (3, 2, 3, 8), (4, 1, 3, 5), (4, 2, 3, 4), (3, 3, 5, 6)]):
        v = n * w + F(n * a, b)
        simp = v.denominator not in (1, b)
        q = "%s = <b>?</b><br>Give your answer as a %s." % (
            mn(n, w, a, b), "whole number" if v.denominator == 1 else
            "mixed number in its simplest form" if simp else "mixed number")
        its.append(mcq(q, S(v), mx_wrongs(n, w, a, b, rot(["lost", "whole", "frac", "add", "up"], i)), mx_e(n, w, a, b)))
    # D) reasoning
    nm, he, his = P.next()
    q = "%s says %s = %s. What mistake did %s make?" % (nm, mn(3, 2, 1, 4), mixed(6, 1, 4), he)
    its.append(mcq(q, (cap("%s multiplied only the whole number." % he), None),
                   [(cap("%s added 3 instead of multiplying." % he), None),
                    (cap("%s multiplied the denominator by 3." % he), None),
                    ("There is no mistake.", None)],
                   "Both parts must be multiplied by 3: 2 × 3 = 6 and %s × 3 = %s. So %s = <b>%s</b>, not %s."
                   % (fr(1, 4), fr(3, 4), mn(3, 2, 1, 4), mixed(6, 3, 4), mixed(6, 1, 4))))
    q = ("Change %s to an improper fraction, then multiply by 4. What is %s?" % (mixed(1, 2, 3), mn(4, 1, 2, 3)))
    its.append(mcq(q, M(6, 2, 3), [M(4, 2, 3), M(5, 2, 3), R(20, 12), M(7, 2, 3)],
                   "%s = %s (1 × 3 + 2 = 5). %s × 4 = %s. 20 ÷ 3 = 6 remainder 2, so the answer is <b>%s</b>."
                   % (mixed(1, 2, 3), fr(5, 3), fr(5, 3), fr(20, 3), mixed(6, 2, 3))))
    assert len(its) == 20, len(its)
    return {"title": "Multiply mixed numbers by whole numbers", "items": its}


# ============================================================ set 5: word problems
def set_words(P):
    its = []
    L = ("litre", "litres")
    H = ("hour", "hours")

    def pw(q, n, a, b, unit, order, lead=""):
        v = F(n * a, b)
        e = lead + pw_e(n, a, b)
        if unit:
            e = e[:-5] + " %s</b>." % (unit[0] if v <= 1 else unit[1]) if e.endswith("</b>.") else e
        its.append(mcq(q, with_unit(S(v), unit), [with_unit(c, unit) for c in pw_wrongs(n, a, b, order)], e))

    def mx(q, n, w, a, b, unit, order):
        v = n * w + F(n * a, b)
        e = mx_e(n, w, a, b)
        e = e[:-5] + " %s</b>." % (unit[0] if v <= 1 else unit[1])
        its.append(mcq(q, with_unit(S(v), unit), [with_unit(c, unit) for c in mx_wrongs(n, w, a, b, order)], e))

    pw("Each bottle holds %s of a litre of water. How much water is in 6 bottles?" % fr(3, 4), 6, 3, 4, L,
       ["add", "both", "up", "swap"], "%s. " % nf(6, 3, 4))
    pw("A loaf of bread needs %s kg of flour. How much flour is needed for 4 loaves?" % fr(2, 5), 4, 2, 5, ("kg", "kg"),
       ["both", "add", "up", "addtop"], "%s. " % nf(4, 2, 5))
    nm, he, his = P.next()
    pw("Each bow uses %s m of ribbon. %s makes 7 bows. How much ribbon does %s use?" % (fr(3, 5), nm, he), 7, 3, 5,
       ("m", "m"), ["add", "both", "swap", "up"], "%s. " % nf(7, 3, 5))
    pw("Each lesson lasts %s of an hour. How many hours are 5 lessons?" % fr(3, 4), 5, 3, 4, H,
       ["add", "both", "up", "swap"], "%s. " % nf(5, 3, 4))
    pw("Each pizza is cut into 8 equal slices. Each of 6 pupils eats %s of a pizza. How much pizza do they eat altogether?"
       % fr(3, 8), 6, 3, 8, ("pizza", "pizzas"), ["both", "add", "up", "remover"], "%s. " % nf(6, 3, 8))
    nm, he, his = P.next()
    pw("%s reads for %s of an hour every night. How many hours does %s read in 7 nights?" % (nm, fr(2, 3), he), 7, 2, 3, H,
       ["add", "both", "up", "down"], "%s. " % nf(7, 2, 3))
    # fractions of amounts
    its.append(mcq("There are 32 pupils in a Year 5 class. %s of them have school dinners. How many pupils have school dinners?"
                   % fr(3, 8), ("12 pupils", F(12)),
                   of_wrongs(3, 8, 32, ["one", "unshaded", "times"], after=" pupils"), of_e(3, 8, 32, after=" pupils")))
    its.append(mcq("A coat costs £60. In a sale, it costs %s of the price. What is the sale price?" % fr(3, 4),
                   ("£45", F(45)), of_wrongs(3, 4, 60, ["unshaded", "one", "swap", "times"], unit="£"), of_e(3, 4, 60, "£")))
    its.append(mcq("A football match lasts 90 minutes. %s of the match has been played. How many minutes is that?" % fr(2, 3),
                   ("60 minutes", F(60)), of_wrongs(2, 3, 90, ["unshaded", "one", "swap", "times"], after=" minutes"),
                   of_e(2, 3, 90, after=" minutes")))
    nm, he, his = P.next()
    its.append(mcq("%s needs £32 for a school trip. %s has saved %s of it. How much has %s saved?" % (nm, cap(he), fr(5, 8), he),
                   ("£20", F(20)), of_wrongs(5, 8, 32, ["unshaded", "one", "times"], unit="£"), of_e(5, 8, 32, "£")))
    its.append(mcq("A box has 45 packets of crisps. %s of the packets are cheese and onion. How many packets are cheese and onion?"
                   % fr(2, 5), ("18 packets", F(18)), of_wrongs(2, 5, 45, ["one", "unshaded", "times"], after=" packets"),
                   of_e(2, 5, 45, after=" packets")))
    # mixed numbers
    mx("A bag of potatoes weighs %s kg. The school cook buys 3 bags. How much do they weigh altogether?" % mixed(2, 1, 2),
       3, 2, 1, 2, ("kg", "kg"), ["lost", "whole", "add", "up"])
    mx("A jug holds %s litres of squash. How much squash is in 4 full jugs?" % mixed(1, 3, 4), 4, 1, 3, 4, L,
       ["whole", "lost", "add", "up"])
    nm, he, his = P.next()
    mx("A plank is %s m long. %s puts 3 planks end to end. How long is the row of planks?" % (mixed(1, 2, 5), nm),
       3, 1, 2, 5, ("m", "m"), ["whole", "lost", "add", "frac"])
    mx("A sunflower grows %s cm each day. How much does it grow in 6 days?" % mixed(2, 1, 3), 6, 2, 1, 3, ("cm", "cm"),
       ["lost", "whole", "frac", "up"])
    mx("A bucket holds %s litres of water. How much water is in 3 full buckets?" % mixed(4, 1, 2), 3, 4, 1, 2, L,
       ["whole", "lost", "add", "frac"])
    mx("A lorry carries %s tonnes of sand on each trip. How much sand does it carry in 4 trips?" % mixed(3, 3, 4),
       4, 3, 3, 4, ("tonne", "tonnes"), ["lost", "whole", "add", "up"])
    # two-step
    nm, he, his = P.next()
    assert 2 * 5 * F(2, 3) == F(20, 3)
    its.append(mcq("%s walks %s km to school and %s km home every school day. How far does %s walk in 5 school days?"
                   % (nm, fr(2, 3), fr(2, 3), he),
                   ("6 %s km" % fr(2, 3), F(20, 3)),
                   [("3 %s km" % fr(1, 3), F(10, 3)), (fr(20, 30) + " km", F(2, 3)), ("5 %s km" % fr(2, 3), 5 + F(2, 3)),
                    ("7 %s km" % fr(2, 3), F(23, 3))],
                   "Each day %s walks there and back: 2 × %s = %s km. In 5 days: 5 × %s = %s km. "
                   "20 ÷ 3 = 6 remainder 2, so %s walks <b>6 %s km</b>."
                   % (he, fr(2, 3), fr(4, 3), fr(4, 3), fr(20, 3), he, fr(2, 3))))
    nm, he, his = P.next()
    assert 4 - 5 * F(2, 3) == F(2, 3)
    its.append(mcq("%s has 4 m of string. %s cuts 5 pieces, each %s m long. How much string is left?" % (nm, cap(he), fr(2, 3)),
                   (fr(2, 3) + " m", F(2, 3)),
                   [("3 %s m" % fr(1, 3), F(10, 3)), ("1 %s m" % fr(1, 3), F(4, 3)), ("1 %s m" % fr(2, 3), F(5, 3))],
                   "First find the string used: 5 × %s = %s m = 3 %s m. Then subtract: 4 − 3 %s = <b>%s m</b>."
                   % (fr(2, 3), fr(10, 3), fr(1, 3), fr(1, 3), fr(2, 3))))
    n1, h1, _ = P.next()
    n2, h2, _ = P.next()
    assert 4 * F(3, 4) == 3 and 3 * (1 + F(1, 4)) == F(15, 4)
    its.append(mcq("%s has 4 bottles that each hold %s litre. %s has 3 bottles that each hold %s litres. Who has more?"
                   % (n1, fr(3, 4), n2, mixed(1, 1, 4)),
                   (n2, None), [(n1, None), ("They have the same amount.", None), ("You can’t tell.", None)],
                   "%s: %s = %s = 3 litres. %s: 3 × %s = 3 + %s = 3 %s litres. 3 %s litres is more, so <b>%s</b> has more."
                   % (n1, nf(4, 3, 4), fr(12, 4), n2, mixed(1, 1, 4), fr(3, 4), fr(3, 4), fr(3, 4), n2)))
    assert len(its) == 20, len(its)
    return {"title": "Word problems", "items": its}


# ============================================================ lesson
def body_html():
    group_fig = ("<figure class='sn-fig'>" + groups_svg(3, 2, 5) +
                 "<figcaption>3 lots of " + fr(2, 5) + ": 3 × 2 = 6 shaded fifths, so " + nf(3, 2, 5) + " = "
                 + fr(6, 5) + " = " + mixed(1, 1, 5) + ".</figcaption></figure>")
    line_fig = ("<figure class='sn-fig'>" + jumps_svg(5, 3, 4, W=400) +
                "<figcaption>5 jumps of " + fr(3, 4) + " land on " + fr(15, 4) + ", which is " + mixed(3, 3, 4)
                + ".</figcaption></figure>")
    tape_fig = ("<figure class='sn-fig'>" + tape_svg(20, 3, 4, part_labels=True) +
                "<figcaption>" + fr(3, 4) + " × 20 = " + fr(3, 4) + " of 20: 20 ÷ 4 = 5 in each part, and 3 parts are 15."
                "</figcaption></figure>")
    rows_fig = ("<figure class='sn-fig'>" + rows_svg(3, 2, 1, 4) +
                "<figcaption>3 rows of " + mixed(2, 1, 4) + ": 6 wholes and 3 quarters, so " + mn(3, 2, 1, 4) + " = "
                + mixed(6, 3, 4) + ".</figcaption></figure>")
    return (
        "<h2>The big idea</h2>"
        "<p>Multiplying a fraction by a whole number is <b>repeated addition</b>. " + nf(3, 2, 5) + " means "
        + fr(2, 5) + " + " + fr(2, 5) + " + " + fr(2, 5) + ".</p>"
        + group_fig +
        "<p><b>Multiply the numerator by the whole number. Keep the denominator.</b> "
        "The denominator tells you the size of the parts, and the size does not change.</p>"
        + table(["Calculation", "Think", "Answer"], [
            [nf(4, 1, 5), "4 parts that are each " + fr(1, 5), fr(4, 5)],
            [nf(3, 2, 5), "3 × 2 = 6 fifths", fr(6, 5) + " = " + mixed(1, 1, 5)],
            [nf(5, 3, 4), "5 × 3 = 15 quarters", fr(15, 4) + " = " + mixed(3, 3, 4)],
        ]) +
        "<h2>Answers bigger than 1</h2>"
        "<p>Change an improper fraction to a mixed number. Divide the numerator by the denominator. "
        "The answer is the number of wholes, and the remainder is the new numerator.</p>"
        + line_fig
        + ex("Example", nf(6, 3, 4) + " = ?",
             "6 × 3 = 18, so the answer is " + fr(18, 4) + ". 18 ÷ 4 = 4 remainder 2, so it is " + mixed(4, 2, 4)
             + ". Simplify " + fr(2, 4) + " to " + fr(1, 2) + ".", mixed(4, 1, 2))
        + "<h2>Fractions of amounts</h2>"
        "<p>When you multiply a whole number by a fraction, <b>× means “of”</b>. Divide by the denominator, "
        "then multiply by the numerator.</p>"
        + tape_fig
        + "<h2>Mixed number × whole number</h2>"
        "<p>Partition the mixed number into wholes and a fraction. Multiply <b>both</b> parts, then add.</p>"
        + rows_fig
        + ex("Example", mn(4, 1, 2, 5) + " = ?",
             "1 × 4 = 4 and " + fr(2, 5) + " × 4 = " + fr(8, 5) + " = " + mixed(1, 3, 5) + ". Add: 4 + "
             + mixed(1, 3, 5) + ".", mixed(5, 3, 5))
        + "<p>You can also change the mixed number to an improper fraction first: " + mixed(1, 2, 5) + " = " + fr(7, 5)
        + ", and " + fr(7, 5) + " × 4 = " + fr(28, 5) + " = " + mixed(5, 3, 5) + ".</p>"
        + "<h2>Common mistakes</h2>"
        + table(["Mistake", "What to do instead"], [
            [nf(3, 2, 5) + " = " + fr(6, 15) + " (multiplying the denominator too)",
             "Keep the denominator: " + fr(6, 5) + " = " + mixed(1, 1, 5)],
            [nf(3, 2, 5) + " = " + mixed(3, 2, 5) + " (adding the whole number)", "3 × means 3 lots of " + fr(2, 5)],
            [mn(3, 2, 1, 4) + " = " + mixed(6, 1, 4) + " (multiplying only the whole number)",
             "Multiply the fraction too: " + fr(1, 4) + " × 3 = " + fr(3, 4) + ", so " + mixed(6, 3, 4)],
            [mn(4, 1, 2, 5) + " = " + mixed(4, 3, 5) + " (losing the whole from " + fr(8, 5) + ")",
             fr(8, 5) + " = " + mixed(1, 3, 5) + ", so add 1 more whole: " + mixed(5, 3, 5)],
            [fr(21, 4) + " = " + mixed(4, 1, 4) + " (a slip when dividing)", "21 ÷ 4 = 5 remainder 1, so " + mixed(5, 1, 4)],
        ])
    )


FAQ = [
    {"q": "What fractions do Year 5 children learn to multiply?",
     "a": "In the National Curriculum, Year 5 pupils multiply proper fractions and mixed numbers by whole numbers, "
          "using diagrams to help. Multiplying two fractions together, such as 1/4 × 1/2, comes in Year 6."},
    {"q": "How do you multiply a fraction by a whole number?",
     "a": "Multiply the numerator by the whole number and keep the denominator. For example, 3 × 2/5 = 6/5, which is 1 1/5."},
    {"q": "How do you multiply a mixed number by a whole number?",
     "a": "Multiply the whole number part and the fraction part separately, then add. For example, 2 1/4 × 3 = 6 + 3/4 = 6 3/4."},
    {"q": "How do you teach multiplying fractions in Year 5?",
     "a": "Start with bar models and repeated addition, so 3 × 2/5 is 2/5 + 2/5 + 2/5 = 6/5. "
          "Then move on to the rule, changing improper fractions to mixed numbers, and word problems."},
]


def gen():
    rnd = random.Random(5511)
    P = People(rnd)
    sets = [set_repeat(), set_mixed_answers(P), set_amounts(), set_mixed_numbers(P), set_words(P)]
    balance(sets, rnd)
    seen = set()
    for s in sets:
        assert len(s["items"]) == 20, (s["title"], len(s["items"]))
        cnt = [0, 0, 0, 0]
        for it in s["items"]:
            assert len(set(it["c"])) == 4, it
            cnt[it["a"]] += 1
            assert it["q"] not in seen, it["q"]
            seen.add(it["q"])
        assert cnt == [5, 5, 5, 5], (s["title"], cnt)
    return {
        "country": "uk", "subject": "maths", "grade": "year-5", "slug": "multiplying-fractions", "sort": 11,
        "updated": UPDATED, "pdf_url": "",
        "title": "Year 5 Multiplying Fractions by Whole Numbers",
        "seo_title": "Year 5 Multiplying Fractions Worksheets: Fractions and Mixed Numbers × Whole Numbers (Free, with Answer Key)",
        "short_title": "Multiplying fractions",
        "domain": "Fractions (including decimals and percentages)",
        "standard_code": "Year 5: Fractions (including decimals and percentages)",
        "standard_url": "https://www.gov.uk/government/publications/national-curriculum-in-england-mathematics-programmes-of-study",
        "standard_text": "Multiply proper fractions and mixed numbers by whole numbers, supported by materials and diagrams.",
        "meta_desc": "Free Year 5 maths worksheets on multiplying fractions by whole numbers for the National Curriculum: "
                     "bar models and repeated addition, mixed-number answers, fractions of amounts, mixed numbers × whole "
                     "numbers and word problems. 100 questions with an answer key.",
        "key_big": "Multiply the numerator by the whole number. Keep the denominator.",
        "key_sub": "3 × 2/5 = 6/5 = 1 1/5, not 6/15. For a mixed number, multiply the wholes and the fraction: "
                   "2 1/4 × 3 = 6 + 3/4 = 6 3/4.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    mark_large(u, "(\\d+ bars|number line|bar model|rows of bars)")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
