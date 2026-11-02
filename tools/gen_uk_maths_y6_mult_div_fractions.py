# -*- coding: utf-8 -*-
"""
UK Year 6 Maths: Multiplying and Dividing Fractions (National Curriculum in England)
  python3 tools/gen_uk_maths_y6_mult_div_fractions.py
Year 6 multiplies pairs of proper fractions (answer in simplest form) and divides a proper fraction
by a whole number. Fraction × whole number (Year 5) is revised in set 1. No fraction ÷ fraction.
Every answer is checked with fractions.Fraction; no two choices are equal in value.
HTML attributes use single quotes (no backslashes in the JSON). British English.
"""
import json, math, os, random, re
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "uk", "maths", "year-6")
UPDATED = "2026-11-02"
DARK = "#4fae74"      # answer part
LIGHT = "#d7ecdf"     # first fraction / shaded part
LINE = "#2b2b2b"
THIN = "#9a9a9a"
FONT = "Arial, Helvetica, sans-serif"
GIRLS = ["Amelia", "Isla", "Freya", "Poppy", "Ava", "Aisha", "Lily", "Zara", "Grace", "Ruby", "Maya", "Evie"]
BOYS = ["Oliver", "Harry", "Mohammed", "Jack", "Arjun", "Noah", "George", "Leo", "Alfie", "Kai", "Ethan", "Charlie"]
WORD = {2: "halves", 3: "thirds", 4: "quarters", 5: "fifths", 6: "sixths", 7: "sevenths", 8: "eighths",
        9: "ninths", 10: "tenths", 12: "twelfths"}


# ------------------------------------------------------------ helpers
def f(n):
    return "{:,}".format(n)


def fr(a, b):
    return "<span class='fr'><span class='fn'>%d</span><span class='fd'>%d</span></span>" % (a, b)


def show(v):
    """A Fraction in simplest form: whole number, proper fraction or mixed number."""
    v = F(v)
    q, r = divmod(v.numerator, v.denominator)
    if r == 0:
        return f(q)
    if q == 0:
        return fr(r, v.denominator)
    return "%s %s" % (f(q), fr(r, v.denominator))


def R(n, d):
    """A fraction exactly as a pupil wrote it (not simplified), with its value."""
    return (fr(n, d), F(n, d))


def S(v, unit=""):
    """A value in simplest form, with an optional unit after it."""
    v = F(v)
    return (show(v) + (" " + unit if unit else ""), v)


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
    """Tag pictures that must print larger so their grids stay readable."""
    rx = re.compile(r"<svg (?=[^>]*aria-label='" + pattern + ")")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u


def ff(a, b, c, d):
    return "%s × %s" % (fr(a, b), fr(c, d))


def fw(a, b, n):
    return "%s ÷ %d" % (fr(a, b), n)


# ------------------------------------------------------------ figures
def text(x, y, t, fs=18, col=LINE, anchor="middle", weight="700"):
    return ("<text x='%.1f' y='%.1f' font-size='%d' font-weight='%s' fill='%s' text-anchor='%s'>%s</text>"
            % (x, y, fs, weight, col, anchor, t))


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


def rect_svg(cols, light, rows, dark_rows, W, H, dashed, label):
    """A rectangle (1 whole) cut into cols columns; the first `light` columns are light.
    Row lines cut it into `rows` rows; the top `dark_rows` rows of the light columns are dark.
    dashed=True: row lines are solid inside the light part and dashed outside it."""
    L, T = 4, 4
    cw, rh = W / float(cols), H / float(rows)
    s = ["<rect x='%d' y='%d' width='%d' height='%d' fill='#fff'/>" % (L, T, W, H),
         "<rect x='%d' y='%d' width='%.1f' height='%d' fill='%s'/>" % (L, T, light * cw, H, LIGHT),
         "<rect x='%d' y='%d' width='%.1f' height='%.1f' fill='%s'/>" % (L, T, light * cw, dark_rows * rh, DARK)]
    for r in range(1, rows):
        y = T + r * rh
        if dashed:
            s.append("<line x1='%d' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='2'/>" % (L, y, L + light * cw, y, LINE))
            if light < cols:
                s.append("<line x1='%.1f' y1='%.1f' x2='%d' y2='%.1f' stroke='%s' stroke-width='1.6' stroke-dasharray='5 4'/>"
                         % (L + light * cw, y, L + W, y, THIN))
        else:
            s.append("<line x1='%d' y1='%.1f' x2='%d' y2='%.1f' stroke='%s' stroke-width='1.6'/>" % (L, y, L + W, y, LINE))
    for c in range(1, cols):
        x = L + c * cw
        s.append("<line x1='%.1f' y1='%d' x2='%.1f' y2='%d' stroke='%s' stroke-width='3'/>" % (x, T, x, T + H, LINE))
    s.append("<rect x='%d' y='%d' width='%.1f' height='%.1f' fill='none' stroke='#1f6b3e' stroke-width='3.5'/>"
             % (L, T, light * cw, dark_rows * rh))
    s.append("<rect x='%d' y='%d' width='%d' height='%d' fill='none' stroke='%s' stroke-width='3'/>" % (L, T, W, H, LINE))
    return svg_wrap(W + 8, H + 8, "".join(s), label)


def model_svg(a1, b1, a2, b2, U=150):
    """Area model for a2/b2 × a1/b1: a1 of b1 columns light, a2 of b2 rows of them dark."""
    return rect_svg(b1, a1, b2, a2, U, U, False,
                    "area model: a square cut into %d columns and %d rows, %d columns light, %d by %d dark"
                    % (b1, b2, a1, a1, a2))


def div_svg(a, b, n, W=250, H=90):
    """a/b ÷ n: a bar (1 whole) cut into b columns, a shaded; rows cut it into n; the top row of the shaded part is dark."""
    return rect_svg(b, a, n, 1, W, H, True,
                    "bar split: 1 whole cut into %d columns, %d shaded, the shaded part split into %d equal rows" % (b, a, n))


# ------------------------------------------------------------ fraction of an amount / fraction × whole number
def of_e(a, b, q, unit=""):
    p = q // b
    return ("Divide by the denominator: %s%s ÷ %d = %s%s in each part. Multiply by the numerator: %d × %s%s = %s%s. "
            "So %s of %s%s = <b>%s%s</b>." % (unit, f(q), b, unit, f(p), a, unit, f(p), unit, f(a * p),
                                             fr(a, b), unit, f(q), unit, f(a * p)))


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
        elif k == "both":                       # multiplied the numerator and the denominator by q
            if unit or after:
                continue
            out.append(R(a * q, b * q))
            continue
        else:
            raise ValueError(k)
        if v.denominator == 1:
            out.append(("%s%s%s" % (unit, f(v.numerator), after), v))
    return out


def fw_wrongs(n, a, b, order):
    """n × a/b (answer not whole): (html, value) from real mistakes."""
    out = []
    for k in order:
        if k == "both":                         # multiplied the numerator and the denominator
            out.append(R(n * a, n * b))
        elif k == "bottom":                     # multiplied the denominator
            out.append(S(F(a, n * b)))
        elif k == "addtop":                     # added the whole number to the numerator
            out.append(R(n + a, b))
        elif k == "add":                        # added
            out.append(S(n + F(a, b)))
        elif k == "nomix":                      # improper fraction left as it is, then misread
            out.append(R(n * a, b))
    return out


def mixed_e(n, a, b):
    v = F(n * a, b)
    q, r = divmod(v.numerator, v.denominator)
    s = ("Multiply the whole number by the numerator and keep the denominator: %d × %d = %d, so the answer is %s."
         % (n, a, n * a, fr(n * a, b)))
    g = math.gcd(n * a, b)
    if g > 1:
        s += " Simplify: %s = %s." % (fr(n * a, b), fr(v.numerator, v.denominator))
    s += " %d ÷ %d = %d remainder %d, so it is <b>%s</b>." % (v.numerator, v.denominator, q, r, show(v))
    return s


# ------------------------------------------------------------ fraction × fraction
def ff_e(a, b, c, d, lead=""):
    n, m = a * c, b * d
    v = F(n, m)
    s = (lead + "Multiply the numerators: %d × %d = %d. Multiply the denominators: %d × %d = %d. So %s = %s."
         % (a, c, n, b, d, m, ff(a, b, c, d), fr(n, m)))
    g = math.gcd(n, m)
    if g > 1:
        s += " Simplify: divide the numerator and denominator by %d: %s = <b>%s</b>." % (g, fr(n, m), show(v))
    else:
        s += " This is already in its simplest form: <b>%s</b>." % show(v)
    return s


def ff_wrongs(a, b, c, d, order):
    out = []
    for k in order:
        if k == "addboth":                      # added the numerators and the denominators
            out.append(R(a + c, b + d))
        elif k == "topsadd":                    # multiplied the numerators, added the denominators
            out.append(R(a * c, b + d))
        elif k == "add":                        # added the fractions
            out.append(S(F(a, b) + F(c, d)))
        elif k == "lcd":                        # multiplied the numerators, kept a common denominator
            out.append(R(a * c, b * d // math.gcd(b, d)))
        elif k == "cross":                      # cross-multiplied
            out.append(R(a * d, b * c))
        elif k == "topsimp":                    # simplified the numerator only
            n, m = a * c, b * d
            g = math.gcd(n, m)
            if g > 1:
                out.append(R(n // g, m))
        elif k == "botsimp":                    # simplified the denominator only
            n, m = a * c, b * d
            g = math.gcd(n, m)
            if g > 1:
                out.append(R(n, m // g))
        else:
            raise ValueError(k)
    return out


# ------------------------------------------------------------ fraction ÷ whole number
def fw_e(a, b, n, unit=""):
    v = F(a, b * n)
    u = " " + unit if unit else ""
    if a % n == 0:
        s = ("The numerator %d can be divided by %d: %d ÷ %d = %d. Keep the denominator: %s = <b>%s%s</b>."
             % (a, n, a, n, a // n, fw(a, b, n), show(v), u))
    else:
        s = ("Dividing by %d is the same as multiplying by %s. Multiply the denominator by %d: %s = %s"
             % (n, fr(1, n), n, fw(a, b, n), fr(a, b * n)))
        if math.gcd(a, b * n) > 1:
            s += ". Simplify: %s = <b>%s%s</b>." % (fr(a, b * n), show(v), u)
        else:
            s = s[:-len(fr(a, b * n))] + "<b>%s%s</b>." % (fr(a, b * n), u)
    back = fr(v.numerator * n, v.denominator)
    s += " Check: %s × %d = %s%s." % (show(v), n, back, "" if back == fr(a, b) else " = " + fr(a, b))
    return s


def fw_div_wrongs(a, b, n, order, unit=""):
    u = " " + unit if unit else ""
    out = []
    for k in order:
        if k == "times":                        # multiplied instead of dividing
            h, v = R(a * n, b)
        elif k == "both":                       # multiplied the numerator and the denominator
            h, v = R(a * n, b * n)
        elif k == "part":                       # part of the shaded piece, not of the whole
            h, v = S(F(1, n))
        elif k == "add":                        # added the whole number to the denominator
            h, v = R(a, b + n)
        elif k == "subtop":                     # divided the denominator instead (only when it works)
            if b % n:
                continue
            h, v = R(a, b // n)
        else:
            raise ValueError(k)
        out.append((h + u, v))
    return out


# ============================================================ set 1: fraction × whole number
def set_amounts():
    its = []
    # A) bar models
    for a, b, q in [(3, 5, 20), (3, 4, 24), (2, 3, 18), (5, 8, 40), (4, 7, 28)]:
        qq = fig(tape_svg(q, a, b)) + "The whole bar is %d. What is %s × %d?" % (q, fr(a, b), q)
        v = F(a * q, b)
        order = ["both", "one", "times"] if (a, b, q) == (3, 5, 20) else ["one", "times", "unshaded", "swap"]
        e = of_e(a, b, q)
        if "both" in order:
            e += " (Do not multiply the denominator by 20 as well: %s is just %s.)" % (fr(60, 100), fr(3, 5))
        its.append(mcq(qq, S(v), of_wrongs(a, b, q, order), e))
    # B) whole-number answers
    for form, a, b, q in [("fq", 3, 8, 24), ("qf", 3, 4, 36), ("of", 5, 6, 30), ("fq", 7, 10, 50),
                          ("of", 2, 9, 45), ("qf", 5, 12, 48), ("of", 3, 5, 35)]:
        if form == "qf":
            qq = "%d × %s = <b>?</b>" % (q, fr(a, b))
        elif form == "fq":
            qq = "%s × %d = <b>?</b>" % (fr(a, b), q)
        else:
            qq = "Find %s of %d." % (fr(a, b), q)
        e = of_e(a, b, q)
        if form != "of":
            e = "× means “of”. " + e
        v = F(a * q, b)
        its.append(mcq(qq, S(v), of_wrongs(a, b, q, ["times", "one", "swap", "unshaded"]), e))
    # C) answers that are mixed numbers
    for form, n, a, b, order in [("fn", 5, 2, 3, ["both", "addtop", "bottom", "add"]),
                                 ("fn", 6, 3, 4, ["addtop", "both", "add", "bottom"]),
                                 ("nf", 5, 3, 8, ["bottom", "both", "add", "addtop"]),
                                 ("fn", 7, 4, 5, ["add", "addtop", "both", "bottom"]),
                                 ("nf", 7, 5, 6, ["both", "bottom", "add", "addtop"])]:
        expr = "%s × %d" % (fr(a, b), n) if form == "fn" else "%d × %s" % (n, fr(a, b))
        qq = "%s = <b>?</b><br>Give your answer as a mixed number." % expr
        its.append(mcq(qq, S(F(n * a, b)), fw_wrongs(n, a, b, order), mixed_e(n, a, b)))
    # D) reasoning
    qq = "Which is greater: %s of 20 or %s of 24?" % (fr(3, 4), fr(2, 3))
    its.append(mcq(qq, ("%s of 24" % fr(2, 3), None),
                   [("%s of 20" % fr(3, 4), None), ("They are equal.", None), ("You can’t tell.", None)],
                   "%s of 20: 20 ÷ 4 = 5, 5 × 3 = 15. %s of 24: 24 ÷ 3 = 8, 8 × 2 = 16. 16 is greater than 15, "
                   "so <b>%s of 24</b> is greater." % (fr(3, 4), fr(2, 3), fr(2, 3))))
    qq = ("<span class='fr'><span class='fn'>3</span><span class='fd'><b>?</b></span></span> of 40 = 15. "
          "What is the missing denominator?")
    its.append(mcq(qq, ("8", F(8)), [("5", F(5)), ("25", F(25)), ("15", F(15))],
                   "15 is 3 parts, so 1 part is 15 ÷ 3 = 5. 40 ÷ 5 = 8, so 40 is split into 8 equal parts: "
                   "%s of 40 = 15. The missing denominator is <b>8</b>." % fr(3, 8)))
    qq = "%s of a number is 14. What is the number?" % fr(2, 5)
    its.append(mcq(qq, ("35", F(35)), [("28", F(28)), ("7", F(7)), ("70", F(70)), ("5.6", F(28, 5))],
                   "2 parts are 14, so 1 part is 14 ÷ 2 = 7. The whole has 5 parts: 7 × 5 = <b>35</b>. "
                   "Check: %s of 35 = 35 ÷ 5 × 2 = 14." % fr(2, 5)))
    assert len(its) == 20, len(its)
    return {"title": "Fraction × whole number and fractions of amounts", "items": its}


# ============================================================ set 2: area models
def set_models():
    its = []
    # A) which multiplication does the model show
    for a1, b1, a2, b2 in [(3, 4, 1, 3), (2, 3, 1, 4), (1, 3, 1, 4), (4, 5, 2, 3), (1, 5, 1, 3), (3, 5, 1, 4)]:
        q = (fig(model_svg(a1, b1, a2, b2)) + "The square is 1 whole. The light columns are %s of the square. "
             "Which multiplication does the dark part show?" % fr(a1, b1))
        right = ff(a2, b2, a1, b1)
        cands = [(ff(b2 - a2, b2, a1, b1), F(b2 - a2, b2) * F(a1, b1)),       # counted the white rows
                 ("%s + %s" % (fr(a2, b2), fr(a1, b1)), F(a2, b2) + F(a1, b1)),  # added
                 (ff(a2, b2, b1 - a1, b1), F(a2, b2) * F(b1 - a1, b1))]       # counted the white columns
        e = ("The light part is %d of %d columns: %s of the square. The dark part is %d of the %d rows of the light part: "
             "%s of it. So the dark part is %s of %s, which is %s." %
             (a1, b1, fr(a1, b1), a2, b2, fr(a2, b2), fr(a2, b2), fr(a1, b1), right))
        its.append(mcq(q, (right, F(a2, b2) * F(a1, b1)), cands, e))
    # B) what fraction of the square is dark
    cases = [(1, 2, 1, 4), (1, 3, 1, 2), (1, 4, 1, 3), (1, 2, 1, 5), (2, 3, 1, 3), (3, 4, 1, 2), (2, 5, 1, 3), (3, 4, 3, 5)]
    for i, (a1, b1, a2, b2) in enumerate(cases):
        n, d = a1 * a2, b1 * b2
        assert math.gcd(n, d) == 1
        q = (fig(model_svg(a1, b1, a2, b2)) + "The model shows %s. What fraction of the whole square is dark?"
             % ff(a2, b2, a1, b1))
        cands = [R(a1 + a2, b1 + b2),                         # added numerators and denominators
                 R(n, d - n),                                 # dark compared with not dark
                 R(a2, b2),                                   # dark out of the light part only
                 R(a1, b1)]                                   # the light part
        r = i % 4
        cands = cands[r:] + cands[:r]
        e = ("The square is cut into %d × %d = %d equal small rectangles. %d × %d = %d of them %s dark. "
             "So %s = <b>%s</b>." % (b1, b2, d, a1, a2, n, "is" if n == 1 else "are", ff(a2, b2, a1, b1), fr(n, d)))
        its.append(mcq(q, R(n, d), cands, e))
    # C) size of one small rectangle
    for a1, b1, a2, b2 in [(2, 3, 3, 4), (3, 5, 2, 3), (1, 4, 2, 5)]:
        q = (fig(model_svg(a1, b1, a2, b2)) + "The model shows %s. What fraction of the whole square is "
             "<b>one</b> small rectangle?" % ff(a2, b2, a1, b1))
        cands = [R(1, b1 + b2), R(1, a1 * a2), R(1, b1), R(1, b2)]
        e = ("There are %d columns and %d rows, so the square is cut into %d × %d = %d equal parts. "
             "One part is <b>%s</b>. This is why you multiply the denominators." % (b1, b2, b1, b2, b1 * b2, fr(1, b1 * b2)))
        its.append(mcq(q, R(1, b1 * b2), cands, e))
    # D) count dark parts and all parts
    for a1, b1, a2, b2 in [(4, 5, 3, 4), (2, 3, 4, 5), (5, 8, 1, 2)]:
        n, d = a1 * a2, b1 * b2
        q = (fig(model_svg(a1, b1, a2, b2)) + "The model shows %s. How many small rectangles are dark, "
             "out of how many altogether?" % ff(a2, b2, a1, b1))
        cands = [("%d out of %d" % (a1 + a2, d), None),
                 ("%d out of %d" % (d - n, d), None),
                 ("%d out of %d" % (n, a1 * b2), None),
                 ("%d out of %d" % (n, b1 + b2), None) if n < b1 + b2 else ("", None)]
        e = ("Dark: %d %s × %d %s = %d small rectangles. Altogether: %d columns × %d rows = %d. "
             "So %s = %s." % (a1, "column" if a1 == 1 else "columns", a2, "row" if a2 == 1 else "rows", n, b1, b2, d,
                              ff(a2, b2, a1, b1), fr(n, d)))
        its.append(mcq(q, ("%d out of %d" % (n, d), None), cands, e))
    assert len(its) == 20, len(its)
    return {"title": "Multiply two fractions with an area model", "items": its}


# ============================================================ set 3: multiply and simplify
def set_rule():
    its = []
    # A) unit fraction × unit fraction
    for (b, d), order in [((4, 2), ["addboth", "topsadd", "add", "lcd"]),
                          ((3, 5), ["topsadd", "addboth", "add", "lcd"]),
                          ((2, 6), ["add", "addboth", "topsadd", "lcd"]),
                          ((5, 4), ["addboth", "add", "topsadd", "lcd"]),
                          ((3, 3), ["topsadd", "add", "addboth", "cross"]),
                          ((7, 2), ["addboth", "topsadd", "lcd", "add"])]:
        q = "%s = <b>?</b>" % ff(1, b, 1, d)
        e = ff_e(1, b, 1, d) + " The answer is smaller than both fractions, because you are finding a part of a part."
        its.append(mcq(q, S(F(1, b * d)), ff_wrongs(1, b, 1, d, order), e))
    # B) answers already in simplest form
    for (a, b), (c, d), order in [((2, 3), (4, 5), ["addboth", "cross", "add"]),
                                  ((3, 4), (1, 5), ["addboth", "lcd", "cross", "topsadd"]),
                                  ((5, 6), (1, 3), ["lcd", "cross", "topsadd", "addboth"]),
                                  ((3, 7), (2, 5), ["addboth", "topsadd", "cross", "lcd"]),
                                  ((4, 9), (2, 3), ["lcd", "addboth", "cross", "topsadd"]),
                                  ((5, 8), (3, 4), ["cross", "lcd", "addboth", "topsadd"])]:
        q = "%s = <b>?</b>" % ff(a, b, c, d)
        e = ff_e(a, b, c, d) + " You do not need a common denominator to multiply."
        its.append(mcq(q, S(F(a * c, b * d)), ff_wrongs(a, b, c, d, order), e))
    # C) simplify the answer
    for (a, b), (c, d), order in [((2, 3), (3, 4), ["topsimp", "addboth", "cross", "lcd"]),
                                  ((3, 4), (2, 9), ["topsimp", "addboth", "cross", "lcd"]),
                                  ((5, 6), (3, 10), ["botsimp", "cross", "addboth", "lcd"]),
                                  ((4, 5), (5, 8), ["topsimp", "addboth", "lcd", "cross"]),
                                  ((2, 3), (9, 10), ["cross", "topsimp", "lcd", "addboth"]),
                                  ((3, 8), (4, 9), ["topsimp", "addboth", "cross", "lcd"])]:
        q = "%s = <b>?</b><br>Give your answer in its simplest form." % ff(a, b, c, d)
        its.append(mcq(q, S(F(a * c, b * d)), ff_wrongs(a, b, c, d, order), ff_e(a, b, c, d)))
    # D) missing fractions
    q = "%s × <b>?</b> = %s" % (fr(1, 2), fr(1, 10))
    its.append(mcq(q, R(1, 5), [R(1, 8), R(1, 20), ("5", F(5)), R(2, 10)],
                   "The numerators: 1 × 1 = 1. The denominators: 2 × <b>?</b> = 10, so the missing denominator is 5. "
                   "%s = %s, so the missing fraction is <b>%s</b>." % (ff(1, 2, 1, 5), fr(1, 10), fr(1, 5))))
    q = "<b>?</b> × %s = %s" % (fr(2, 3), fr(2, 9))
    its.append(mcq(q, R(1, 3), [R(1, 6), R(2, 6), R(4, 27), ("3", F(3))],
                   "The numerators: 1 × 2 = 2. The denominators: 3 × 3 = 9. %s = %s, so the missing fraction is <b>%s</b>."
                   % (ff(1, 3, 2, 3), fr(2, 9), fr(1, 3))))
    assert len(its) == 20, len(its)
    return {"title": "Multiply fractions and simplify", "items": its}


# ============================================================ set 4: fraction ÷ whole number
def set_divide(P):
    its = []
    # A) unit fractions with a bar
    for b, n, order in [(3, 2, ["times", "part", "add", "both"]), (2, 4, ["part", "times", "both", "add"]),
                        (4, 2, ["add", "times", "part", "both"]), (3, 3, ["times", "both", "add", "part"]),
                        (5, 2, ["part", "add", "times", "both"]), (2, 3, ["both", "times", "part", "add"])]:
        q = (fig(div_svg(1, b, n)) + "The bar is 1 whole. The shaded part is %s. It is split into %d equal parts. "
             "What fraction of the <b>whole</b> bar is the dark part?<br>%s = <b>?</b>" % (fr(1, b), n, fw(1, b, n)))
        e = ("Follow the dashed lines: the whole bar is cut into %d × %d = %d equal parts, and the dark part is 1 of them. "
             % (b, n, b * n)) + fw_e(1, b, n)
        its.append(mcq(q, S(F(1, b * n)), fw_div_wrongs(1, b, n, order), e))
    # B) non-unit fractions with a bar
    for a, b, n, order in [(4, 5, 2, ["times", "both", "part", "add"]), (2, 3, 4, ["both", "times", "add", "part"]),
                           (3, 4, 3, ["times", "add", "both", "part"]), (6, 7, 3, ["both", "add", "times", "part"]),
                           (2, 5, 3, ["add", "times", "both", "part"]), (3, 4, 2, ["times", "both", "subtop", "add"])]:
        q = (fig(div_svg(a, b, n)) + "The bar is 1 whole. The shaded part is %s. It is split into %d equal parts. "
             "What fraction of the whole bar is the dark part?<br>%s = <b>?</b>" % (fr(a, b), n, fw(a, b, n)))
        v = F(a, b * n)
        e = ("The whole bar is cut into %d × %d = %d equal parts, and %d of them %s dark: %s%s. "
             % (b, n, b * n, a, "is" if a == 1 else "are", fr(a, b * n),
                "" if v.denominator == b * n else " = " + show(v))) + fw_e(a, b, n)
        its.append(mcq(q, S(F(a, b * n)), fw_div_wrongs(a, b, n, order), e))
    # C) calculate
    for a, b, n, order in [(1, 4, 3, ["times", "add", "both", "part"]), (1, 6, 2, ["both", "times", "add", "subtop"]),
                           (6, 7, 2, ["times", "both", "add", "part"]), (3, 8, 2, ["add", "times", "subtop", "both"]),
                           (2, 3, 5, ["times", "add", "both", "part"]), (9, 10, 3, ["both", "times", "add", "part"])]:
        q = "%s = <b>?</b>" % fw(a, b, n)
        its.append(mcq(q, S(F(a, b * n)), fw_div_wrongs(a, b, n, order), fw_e(a, b, n)))
    # D) find the mistake
    M = {"times": "multiplied by %d instead of dividing",
         "both": "multiplied the numerator and the denominator by %d",
         "add": "added %d to the denominator",
         "ok": "nothing; the answer is correct"}
    for kind, a, b, n, wrote in [("times", 1, 3, 2, fr(2, 3)), ("both", 4, 5, 2, fr(8, 10))]:
        nm, he, his = P.next()
        q = "%s says %s = %s. What did %s do?" % (nm, fw(a, b, n), wrote, he)

        def say(k):
            return cap(M[k]) + "." if k == "ok" else cap("%s %s." % (he, M[k] % n))
        right = say(kind)
        wrong = [say(k) for k in ["ok", "times", "both", "add"] if k != kind]
        good = fw(a, b, n) + " = " + show(F(a, b * n))
        if kind == "times":
            e = ("%s found %s × %d = %s. Dividing must give a smaller answer. Splitting %s into %d equal parts gives "
                 "<b>%s</b> each: %s." % (nm, fr(a, b), n, fr(a * n, b), fr(a, b), n, show(F(a, b * n)), good))
        else:
            e = ("%s = %s, so %s did not change the size at all. Divide the numerator instead: 4 ÷ 2 = 2, so %s."
                 % (fr(8, 10), fr(4, 5), nm, good))
        its.append(mcq(q, (right, None), [(w, None) for w in wrong], e))
    assert len(its) == 20, len(its)
    return {"title": "Divide a fraction by a whole number", "items": its}


# ============================================================ set 5: SATs-style arithmetic and word problems
def set_words(P):
    its = []
    # arithmetic paper
    its.append(mcq("%s = <b>?</b>" % ff(3, 4, 1, 6), S(F(1, 8)), ff_wrongs(3, 4, 1, 6, ["topsimp", "addboth", "lcd", "cross"]),
                   ff_e(3, 4, 1, 6)))
    its.append(mcq("%s = <b>?</b>" % fw(5, 6, 5), S(F(1, 6)), fw_div_wrongs(5, 6, 5, ["times", "both", "add"]), fw_e(5, 6, 5)))
    its.append(mcq("%s × 35 = <b>?</b>" % fr(2, 5), S(F(14)), of_wrongs(2, 5, 35, ["times", "one", "unshaded", "both"]),
                   "× means “of”. " + of_e(2, 5, 35)))
    its.append(mcq("%s = <b>?</b>" % fw(7, 8, 2), S(F(7, 16)), fw_div_wrongs(7, 8, 2, ["times", "subtop", "add", "both"]),
                   fw_e(7, 8, 2)))
    its.append(mcq("%s = <b>?</b>" % ff(4, 9, 3, 8), S(F(1, 6)), ff_wrongs(4, 9, 3, 8, ["topsimp", "addboth", "cross", "lcd"]),
                   ff_e(4, 9, 3, 8)))

    # word problems
    nm, he, his = P.next()
    q = ("%s of a pizza is left. %s eats half of what is left. What fraction of the whole pizza does %s eat?"
         % (fr(3, 4), nm, he))
    its.append(mcq(q, S(F(3, 8)), [S(F(1, 4)), R(3, 2), R(4, 6), R(3, 6)],
                   "Half of %s means %s. " % (fr(3, 4), ff(1, 2, 3, 4)) + ff_e(1, 2, 3, 4).replace("<b>", "").replace("</b>", "")
                   + " %s eats <b>%s</b> of the pizza." % (cap(he), fr(3, 8))))
    nm, he, his = P.next()
    q = ("%s of a cake is left. %s shares it equally between 4 friends. What fraction of the whole cake does each friend get?"
         % (fr(2, 3), nm))
    its.append(mcq(q, S(F(1, 6)), fw_div_wrongs(2, 3, 4, ["part", "times", "both", "add"]),
                   "Share %s between 4: %s. " % (fr(2, 3), fw(2, 3, 4)) + fw_e(2, 3, 4)))
    q = "A bottle holds %s of a litre of juice. It is poured equally into 3 glasses. How much juice is in each glass?" % fr(3, 4)
    its.append(mcq(q, S(F(1, 4), "litre"), fw_div_wrongs(3, 4, 3, ["times", "add", "both", "part"], "litre"),
                   "%s: " % fw(3, 4, 3) + fw_e(3, 4, 3, "litre")))
    nm, he, his = P.next()
    q = "%s has a ribbon %s m long. %s cuts it into 2 equal pieces. How long is each piece?" % (nm, fr(2, 5), cap(he))
    its.append(mcq(q, S(F(1, 5), "m"), fw_div_wrongs(2, 5, 2, ["times", "both", "add", "part"], "m"),
                   "%s: " % fw(2, 5, 2) + fw_e(2, 5, 2, "m")))
    q = "There are 30 pupils in a Year 6 class. %s of them walk to school. How many pupils walk to school?" % fr(3, 5)
    its.append(mcq(q, ("18 pupils", F(18)), of_wrongs(3, 5, 30, ["one", "unshaded", "times", "swap"], after=" pupils"),
                   of_e(3, 5, 30)))
    nm, he, his = P.next()
    q = "A pair of trainers costs £40. In a sale, %s pays %s of the price. How much does %s pay?" % (nm, fr(5, 8), he)
    its.append(mcq(q, ("£25", F(25)), of_wrongs(5, 8, 40, ["one", "unshaded", "swap", "times"], unit="£"),
                   of_e(5, 8, 40, "£")))
    q = ("%s of a garden is lawn. %s of the lawn has daisies on it. What fraction of the whole garden has daisies?"
         % (fr(2, 3), fr(1, 4)))
    its.append(mcq(q, S(F(1, 6)), [R(3, 7), S(F(11, 12)), R(2, 7), R(1, 4)],
                   "%s of %s means %s. " % (fr(1, 4), fr(2, 3), ff(1, 4, 2, 3)) + ff_e(1, 4, 2, 3)))
    q = "%s kg of flour is shared equally between 4 bags. How much flour is in each bag?" % fr(4, 5)
    its.append(mcq(q, S(F(1, 5), "kg"), fw_div_wrongs(4, 5, 4, ["times", "both", "add", "part"], "kg"),
                   "%s: " % fw(4, 5, 4) + fw_e(4, 5, 4, "kg")))
    q = ("%s of the pupils in a school have school dinners. %s of these pupils choose pasta. "
         "What fraction of all the pupils choose pasta?" % (fr(1, 2), fr(1, 3)))
    its.append(mcq(q, S(F(1, 6)), ff_wrongs(1, 2, 1, 3, ["addboth", "add", "topsadd", "lcd"]),
                   "%s of %s means %s. " % (fr(1, 3), fr(1, 2), ff(1, 3, 1, 2)) + ff_e(1, 3, 1, 2)))
    nm, he, his = P.next()
    q = "One lap of the school field is %s km. %s runs 4 laps. How far does %s run?" % (fr(3, 8), nm, he)
    its.append(mcq(q, ("1 %s km" % fr(1, 2), F(3, 2)),
                   [(fr(12, 32) + " km", F(3, 8)), (fr(3, 32) + " km", F(3, 32)), (fr(7, 8) + " km", F(7, 8)),
                    ("4 %s km" % fr(3, 8), F(35, 8))],
                   "%s × 4 = %s. " % (fr(3, 8), fr(12, 8)) + "Simplify: %s = %s. 3 ÷ 2 = 1 remainder 1, so %s runs <b>1 %s km</b>."
                   % (fr(12, 8), fr(3, 2), he, fr(1, 2))))
    q = "A plank of wood is %s m long. It is cut into 5 equal pieces. How long is each piece?" % fr(5, 6)
    its.append(mcq(q, S(F(1, 6), "m"), fw_div_wrongs(5, 6, 5, ["both", "add", "part", "times"], "m"),
                   "%s: " % fw(5, 6, 5) + fw_e(5, 6, 5, "m")))
    nm, he, his = P.next()
    q = "%s has £15 of pocket money. %s spends %s of it on a book. How much does the book cost?" % (nm, cap(he), fr(2, 5))
    its.append(mcq(q, ("£6", F(6)), of_wrongs(2, 5, 15, ["one", "unshaded", "times"], unit="£"),
                   of_e(2, 5, 15, "£")))
    q = "A rectangle is %s m long and %s m wide. What is its area?" % (fr(3, 4), fr(2, 5))
    its.append(mcq(q, (fr(3, 10) + " m²", F(3, 10)),
                   [(fr(5, 9) + " m²", F(5, 9)), ("1 %s m²" % fr(3, 20), F(23, 20)), (fr(15, 8) + " m²", F(15, 8)),
                    (fr(6, 9) + " m²", F(2, 3))],
                   "Area = length × width = %s = %s. Simplify: divide the numerator and denominator by 2: <b>%s m²</b>."
                   % (ff(3, 4, 2, 5), fr(6, 20), fr(3, 10))))
    n1, h1, _ = P.next()
    n2, h2, _ = P.next()
    q = ("%s eats %s of %s of a pie. %s eats %s of %s of a pie the same size. Who eats more pie?"
         % (n1, fr(1, 2), fr(1, 4), n2, fr(1, 3), fr(1, 3)))
    its.append(mcq(q, (n1, None), [(n2, None), ("They eat the same amount.", None), ("You can’t tell.", None)],
                   "%s: %s = %s. %s: %s = %s. Both have a numerator of 1, and eighths are bigger than ninths, "
                   "so %s is more than %s. <b>%s</b> eats more pie."
                   % (n1, ff(1, 2, 1, 4), fr(1, 8), n2, ff(1, 3, 1, 3), fr(1, 9), fr(1, 8), fr(1, 9), n1)))
    nm, he, his = P.next()
    q = ("A 1 litre jug is %s full of squash. %s pours it equally into 2 cups. How much squash is in each cup?"
         % (fr(5, 6), nm))
    its.append(mcq(q, S(F(5, 12), "litre"), fw_div_wrongs(5, 6, 2, ["times", "both", "subtop", "add"], "litre"),
                   "%s: " % fw(5, 6, 2) + fw_e(5, 6, 2, "litre")))
    assert len(its) == 20, len(its)
    return {"title": "SATs-style arithmetic and word problems", "items": its}


# ============================================================ lesson
def body_html():
    tape_fig = ("<figure class='sn-fig'>" + tape_svg(20, 3, 5, part_labels=True) +
                "<figcaption>" + fr(3, 5) + " × 20: 20 ÷ 5 = 4 in each part, and 3 parts are 3 × 4 = 12.</figcaption></figure>")
    model_fig = ("<figure class='sn-fig'>" + model_svg(1, 2, 1, 4) +
                 "<figcaption>" + ff(1, 4, 1, 2) + ": shade " + fr(1, 2) + " of the square (light column). "
                 "Take " + fr(1, 4) + " of that part (dark). 1 of the 8 equal parts is dark, so "
                 + ff(1, 4, 1, 2) + " = " + fr(1, 8) + ".</figcaption></figure>")
    div_fig = ("<figure class='sn-fig'>" + div_svg(1, 3, 2, W=270, H=96) +
               "<figcaption>" + fw(1, 3, 2) + ": split the shaded third into 2 equal parts. The dashed lines show that "
               "the whole bar has 6 of these parts, so the dark part is " + fr(1, 6) + ".</figcaption></figure>")
    return (
        "<h2>The big idea</h2>"
        "<p>When you multiply by a fraction, <b>× means “of”</b>. " + ff(1, 4, 1, 2) + " means a quarter of a half. "
        "When you divide a fraction by a whole number, you <b>share it into equal parts</b>. " + fw(1, 3, 2)
        + " means half of a third.</p>"
        "<h2>Fraction × whole number</h2>"
        "<p>Divide by the denominator, then multiply by the numerator.</p>"
        + tape_fig
        + ex("Example", fr(2, 3) + " × 5 = ?",
             "Multiply the whole number by the numerator: 5 × 2 = 10, so the answer is " + fr(10, 3) + ". "
             "10 ÷ 3 = 3 remainder 1.", "3 " + fr(1, 3))
        + "<h2>Fraction × fraction</h2>"
        "<p><b>Multiply the numerators. Multiply the denominators. Then simplify.</b> "
        "The area model shows why: the square is cut into (denominator × denominator) equal parts.</p>"
        + model_fig
        + ex("Example", ff(2, 3, 3, 4) + " = ?",
             "2 × 3 = 6 and 3 × 4 = 12, so the answer is " + fr(6, 12) + ". Divide the numerator and denominator by 6.",
             fr(1, 2))
        + "<p>Tip: you can simplify <b>before</b> you multiply. In " + ff(3, 4, 2, 9) + ", divide 3 and 9 by 3, and "
        "2 and 4 by 2: " + ff(1, 2, 1, 3) + " = " + fr(1, 6) + ".</p>"
        "<h2>Fraction ÷ whole number</h2>"
        "<p>Dividing by 2 is the same as finding half, or multiplying by " + fr(1, 2) + ".</p>"
        + div_fig
        + table(["Method", "Example", "When to use it"], [
            ["Divide the numerator", fw(4, 5, 2) + " = " + fr(2, 5), "The numerator divides exactly"],
            ["Multiply the denominator", fw(2, 5, 3) + " = " + fr(2, 15), "Any time"],
        ])
        + ex("Example", fw(2, 3, 4) + " = ?",
             "4 does not go into 2 exactly, so multiply the denominator: 3 × 4 = 12. " + fw(2, 3, 4) + " = " + fr(2, 12)
             + ". Simplify by dividing by 2.", fr(1, 6))
        + "<p>Check by multiplying back: " + fr(1, 6) + " × 4 = " + fr(4, 6) + " = " + fr(2, 3) + ".</p>"
        + "<h2>Common mistakes</h2>"
        + table(["Mistake", "What to do instead"], [
            [ff(1, 4, 1, 2) + " = " + fr(2, 6) + " (adding numerators and denominators)",
             "Multiply: 1 × 1 = 1 and 4 × 2 = 8, so " + fr(1, 8)],
            [fw(1, 3, 2) + " = " + fr(2, 3) + " (multiplying by 2)", "Dividing makes the part smaller: " + fr(1, 6)],
            [fw(4, 5, 2) + " = " + fr(8, 10) + " (multiplying the numerator and denominator)",
             fr(8, 10) + " = " + fr(4, 5) + ", so nothing changed. The answer is " + fr(2, 5)],
            [fr(3, 5) + " × 20 = " + fr(60, 100) + " (multiplying the numerator and denominator by 20)",
             "Only multiply the numerator: " + fr(60, 5) + " = 12"],
        ])
    )


FAQ = [
    {"q": "How do you multiply fractions in Year 6?",
     "a": "Multiply the numerators, multiply the denominators, then simplify. For example, 2/3 × 3/4 = 6/12 = 1/2."},
    {"q": "How do you divide a fraction by a whole number?",
     "a": "If the numerator divides exactly, divide it: 4/5 ÷ 2 = 2/5. Otherwise multiply the denominator by the whole number: 1/3 ÷ 2 = 1/6."},
    {"q": "Do Year 6 pupils divide a fraction by a fraction?",
     "a": "No. In the National Curriculum, Year 6 divides proper fractions by whole numbers only. Dividing by a fraction comes in Key Stage 3."},
    {"q": "Are multiplying and dividing fractions in the Year 6 SATs?",
     "a": "Yes. The arithmetic paper (Paper 1) usually includes calculations such as 3/4 × 1/6 or 2/5 ÷ 4, and the reasoning papers use fractions in word problems."},
]


def gen():
    rnd = random.Random(6608)
    P = People(rnd)
    sets = [set_amounts(), set_models(), set_rule(), set_divide(P), set_words(P)]
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
        "country": "uk", "subject": "maths", "grade": "year-6", "slug": "multiplying-and-dividing-fractions", "sort": 8,
        "updated": UPDATED, "pdf_url": "",
        "title": "Year 6 Multiplying and Dividing Fractions",
        "seo_title": "Year 6 Multiplying and Dividing Fractions Worksheets: Fraction × Fraction, Fraction ÷ Whole Number, Simplest Form (Free, with Answers)",
        "short_title": "Multiplying and dividing fractions",
        "domain": "Fractions (including decimals and percentages)",
        "standard_code": "Year 6: Fractions (including decimals and percentages)",
        "standard_url": "https://www.gov.uk/government/publications/national-curriculum-in-england-mathematics-programmes-of-study",
        "standard_text": "Multiply simple pairs of proper fractions, writing the answer in its simplest form [for example, 1/4 × 1/2 = 1/8]; divide proper fractions by whole numbers [for example, 1/3 ÷ 2 = 1/6].",
        "meta_desc": "Free Year 6 maths worksheets on multiplying and dividing fractions for the National Curriculum: fractions of amounts, area models, fraction × fraction in simplest form, fraction ÷ whole number and SATs-style word problems. 100 questions with an answer key.",
        "key_big": "Fraction × fraction: multiply the numerators, multiply the denominators, then simplify. Fraction ÷ whole number: share it into equal parts.",
        "key_sub": "1/4 × 1/2 = 1/8, not 2/6. 2/3 × 3/4 = 6/12 = 1/2. 1/3 ÷ 2 = 1/6 (multiply the denominator). 4/5 ÷ 2 = 2/5 (divide the numerator).",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    mark_large(u, "(area model|bar split)")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
