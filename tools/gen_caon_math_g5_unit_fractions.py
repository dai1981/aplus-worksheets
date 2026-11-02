# -*- coding: utf-8 -*-
"""
CA Grade 5 Math: Multiplying and Dividing with Unit Fractions (Ontario Mathematics Curriculum 2020, B2.8)
  python3 tools/gen_caon_math_g5_unit_fractions.py
Grade 5 multiplies and divides ONE-DIGIT whole numbers by UNIT fractions (1/2 to 1/12):
  4 × 1/3 = 4/3 with bars, writing products as mixed numbers, 3 ÷ 1/4 = 12 (how many fourths),
  choosing × or ÷ for a story, word problems (pizza slices, laps).
Every answer is checked with fractions.Fraction; no two choices are equal in value.
Canadian English, metric units. HTML attributes use single quotes (no backslashes in the JSON).
"""
import json, math, os, random, re
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "ca-on", "math", "grade-5")
UPDATED = "2026-11-02"
G1 = "#4fae74"        # shaded / group colour 1
G2 = "#a6dbb7"        # group colour 2
LINE = "#2b2b2b"
RED = "#d6453b"
FONT = "Arial, Helvetica, sans-serif"
NBSP = " "
GIRLS = ["Olivia", "Emma", "Maya", "Zoe", "Amira", "Mei", "Chloe", "Priya", "Leah", "Hana", "Ava", "Sofia"]
BOYS = ["Liam", "Noah", "Aiden", "Lucas", "Owen", "Arjun", "Ethan", "Jayden", "Benjamin", "Mateo", "Nathan", "Kai"]
PARTS = {2: ("half", "halves"), 3: ("third", "thirds"), 4: ("fourth", "fourths"), 5: ("fifth", "fifths"),
         6: ("sixth", "sixths"), 7: ("seventh", "sevenths"), 8: ("eighth", "eighths"), 9: ("ninth", "ninths"),
         10: ("tenth", "tenths"), 12: ("twelfth", "twelfths")}


# ------------------------------------------------------------ numbers
def num(n):
    """Ontario style: 4 digits plain, 5 or more digits grouped with a no-break space."""
    s = str(n)
    if len(s) <= 4:
        return s
    out = []
    while s:
        out.insert(0, s[-3:])
        s = s[:-3]
    return NBSP.join(out)


def fr(a, b):
    return "<span class='fr'><span class='fn'>%d</span><span class='fd'>%d</span></span>" % (a, b)


def show(v):
    """A Fraction in simplest form: whole number, proper fraction or mixed number."""
    v = F(v)
    q, r = divmod(v.numerator, v.denominator)
    if r == 0:
        return num(q)
    if q == 0:
        return fr(r, v.denominator)
    return "%s %s" % (num(q), fr(r, v.denominator))


def R(n, d, unit=""):
    """A fraction exactly as a student wrote it (not simplified), with its value."""
    return (fr(n, d) + (" " + unit if unit else ""), F(n, d))


def S(v, unit="", pre=""):
    """A value in simplest form with an optional unit."""
    v = F(v)
    return (pre + show(v) + (" " + unit if unit else ""), v)


def M(w, n, d, unit=""):
    """A mixed number exactly as written (w n/d), with its value."""
    return ("%d %s" % (w, fr(n, d)) + (" " + unit if unit else ""), w + F(n, d))


def parts(b, k=2):
    return PARTS[b][0] if k == 1 else PARTS[b][1]


def pl(k, one, many):
    return one if k == 1 else many


def cap(s):
    return s[0].upper() + s[1:]


def him(he):
    return "her" if he == "she" else "him"


def mcq(q, correct, cands, e):
    """correct and cands are (html, value). A candidate equal in value to an earlier choice is skipped.
    Positions are set later by balance()."""
    ch, vals = [correct[0]], [correct[1]]
    for h, v in cands:
        if not h or h in ch or (v is not None and (v in vals or v <= 0)):
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


def fig(svg):
    return "<div class='qfig'>" + svg + "</div>"


def svg_wrap(w, h, body, label):
    w, h = int(math.ceil(w)), int(math.ceil(h))
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
    """Tag wide pictures (rows of bars, number lines) so they print larger."""
    rx = re.compile(r"<svg (?=[^>]*aria-label='" + pattern + ")")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u


def nu(n, b):
    return "%d × %s" % (n, fr(1, b))


def un(b, n):
    return "%s × %d" % (fr(1, b), n)


def du(n, b):
    return "%d ÷ %s" % (n, fr(1, b))


# ------------------------------------------------------------ figures
def text(x, y, t, fs=16, col=LINE, anchor="middle", weight="700"):
    return ("<text x='%.1f' y='%.1f' font-size='%d' font-weight='%s' fill='%s' text-anchor='%s'>%s</text>"
            % (x, y, fs, weight, col, anchor, t))


def copies_svg(n, b, BW=None):
    """n bars side by side, each 1 whole cut into b equal parts with 1 part shaded (n × 1/b)."""
    if BW is None:
        BW = max(48, min(84, (430 - (n - 1) * 12) // n))
    gap, x0, y0, H = 12, 6, 6, 40
    s = []
    for k in range(n):
        bx = x0 + k * (BW + gap)
        pw = BW / float(b)
        for i in range(b):
            s.append("<rect x='%.1f' y='%d' width='%.1f' height='%d' fill='%s' stroke='%s' stroke-width='1.6'/>"
                     % (bx + i * pw, y0, pw, H, G1 if i < 1 else "#fff", LINE))
        s.append("<rect x='%d' y='%d' width='%d' height='%d' fill='none' stroke='%s' stroke-width='2.5'/>"
                 % (bx, y0, BW, H, LINE))
    W = x0 * 2 + n * BW + (n - 1) * gap
    return svg_wrap(W, y0 + H + 6, "".join(s),
                    "row of %d bars, each 1 whole cut into %d equal parts with 1 part shaded" % (n, b))


def fill_svg(n, b, PW=None):
    """n pieces of 1/b put together: whole bars of b pieces side by side, the first n pieces shaded."""
    bars = -(-n // b)
    if PW is None:
        PW = max(18, min(36, (420 - (bars - 1) * 12) // (bars * b)))
    gap, x0, y0, H = 12, 6, 6, 40
    BW = PW * b
    s = []
    for k in range(bars):
        bx = x0 + k * (BW + gap)
        for i in range(b):
            sh = k * b + i < n
            s.append("<rect x='%d' y='%d' width='%d' height='%d' fill='%s' stroke='%s' stroke-width='1.6'/>"
                     % (bx + i * PW, y0, PW, H, G1 if sh else "#fff", LINE))
        s.append("<rect x='%d' y='%d' width='%d' height='%d' fill='none' stroke='%s' stroke-width='2.5'/>"
                 % (bx, y0, BW, H, LINE))
    W = x0 * 2 + bars * BW + (bars - 1) * gap
    return svg_wrap(W, y0 + H + 6, "".join(s),
                    "row of %d bars, each 1 whole cut into %d equal parts, with %d parts shaded in all" % (bars, b, n))


def wholes_svg(n, b, PW=None):
    """n wholes in a row, each cut into b pieces (two greens). Labels 0..n under the thick whole lines."""
    k = n * b
    if PW is None:
        PW = max(16, min(40, 400 // k))
    X0, BH, T = 14, 36, 8
    W = X0 * 2 + k * PW
    s = []
    for i in range(k):
        col = G1 if i % 2 == 0 else G2
        s.append("<rect x='%d' y='%d' width='%d' height='%d' fill='%s' stroke='%s' stroke-width='1.4'/>"
                 % (X0 + i * PW, T, PW, BH, col, LINE))
    for j in range(n + 1):
        x = X0 + j * b * PW
        s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='3.5'/>" % (x, T - 2, x, T + BH + 8, LINE))
        s.append(text(x, T + BH + 26, str(j), 16))
    s.append("<rect x='%d' y='%d' width='%d' height='%d' fill='none' stroke='%s' stroke-width='3'/>" % (X0, T, k * PW, BH, LINE))
    return svg_wrap(W, T + BH + 32, "".join(s), "%d %s, each cut into %d equal pieces" % (n, pl(n, "whole", "wholes"), b))


def line_svg(ends, b, jumps, W=440):
    """Number line 0..ends with ticks every 1/b and `jumps` jumps of 1/b from 0."""
    total = ends * b
    L, Rr, Y = 18, W - 18, 46

    def X(i):
        return L + (Rr - L) * i / float(total)
    s = ["<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='2.5'/>" % (L, Y, Rr, Y, LINE)]
    for i in range(total + 1):
        whole = (i % b == 0)
        s.append("<line x1='%.1f' y1='%d' x2='%.1f' y2='%d' stroke='%s' stroke-width='%s'/>"
                 % (X(i), Y - (12 if whole else 7), X(i), Y + (12 if whole else 7), LINE, "2.5" if whole else "1.6"))
        if whole:
            s.append(text(X(i), Y + 34, str(i // b), 18))
    h = 26 if (Rr - L) / float(total) > 24 else 18
    for j in range(jumps):
        x0, x1 = X(j), X(j + 1)
        s.append("<path d='M%.1f %d Q%.1f %d %.1f %d' fill='none' stroke='%s' stroke-width='2.2'/>"
                 % (x0 + 1, Y - 3, (x0 + x1) / 2, Y - 3 - h, x1 - 1, Y - 3, RED))
        s.append("<path d='M%.1f %d l-6 -8 l8 1 z' fill='%s'/>" % (x1 - 1, Y - 3, RED))
    return svg_wrap(W, Y + 42, "".join(s), "number line from 0 to %d with %d jumps of 1/%d" % (ends, jumps, b))


# ------------------------------------------------------------ multiply: n × 1/b
def nu_e(n, b, lead=""):
    """n × 1/b: n pieces of one b-th."""
    v = F(n, b)
    s = lead + "%s means %d %s of %s. That is %d %s, so the answer is %s." % (
        nu(n, b), n, pl(n, "group", "groups"), fr(1, b), n, parts(b, n), fr(n, b))
    q, r = divmod(n, b)
    if r == 0:
        s += " %d ÷ %d = %d, so it is <b>%d</b> %s." % (n, b, q, q, pl(q, "whole", "wholes"))
    elif q > 0:
        s += " %d ÷ %d = %d remainder %d, so it is <b>%s</b>." % (n, b, q, r, show(v))
    else:
        s = s[:-len(fr(n, b)) - 1] + "<b>%s</b>." % fr(n, b)
    return s


def nu_wrongs(n, b, order, unit=""):
    """n × 1/b: (html, value) from real mistakes."""
    out = []
    for k in order:
        if k == "bottom":                       # multiplied the denominator
            out.append(R(1, n * b, unit))
        elif k == "both":                       # multiplied the numerator and the denominator
            out.append(R(n, n * b, unit))
        elif k == "addtop":                     # added 1 more piece
            out.append(R(n + 1, b, unit))
        elif k == "flip":                       # wrote the fraction upside down
            if n != b:
                out.append(R(b, n, unit))
        elif k == "attach":                     # wrote the whole number in front: n 1/b
            out.append(M(n, 1, b, unit))
        elif k == "times":                      # multiplied the whole numbers: n × b
            out.append(S(F(n * b), unit))
        else:
            raise ValueError(k)
    return out


def mixed_e(n, b, lead=""):
    q, r = divmod(n, b)
    return (lead + "%s = %s. %d %s make 1 whole. %d ÷ %d = %d remainder %d: %d %s and %d %s left over. "
            "So %s = <b>%s</b>." % (nu(n, b), fr(n, b), b, parts(b), n, b, q, r, q, pl(q, "whole", "wholes"),
                                    r, parts(b, r), fr(n, b), show(F(n, b))))


def mixed_wrongs(n, b, order):
    q, r = divmod(n, b)
    out = []
    for k in order:
        if k == "attach":                       # n 1/b
            out.append(M(n, 1, b))
        elif k == "den":                        # used the whole number as the denominator: q r/n
            out.append(M(q, r, n))
        elif k == "swap":                       # swapped quotient and remainder: r q/b
            if q < b:
                out.append(M(r, q, b))
        elif k == "up":                         # counted the bars: (q+1) r/b
            out.append(M(q + 1, r, b))
        elif k == "both":                       # multiplied the denominator too
            out.append(R(n, n * b))
        else:
            raise ValueError(k)
    return out


# ------------------------------------------------------------ divide: n ÷ 1/b
def du_e(n, b):
    s = ("%s asks how many %s are in %d. Each whole has %d %s, so %d wholes have %d × %d = <b>%d</b> %s."
         % (du(n, b), parts(b), n, b, parts(b), n, n, b, n * b, parts(b)))
    return s + " Check: %s = %s = %d." % (nu(n * b, b), fr(n * b, b), n)


def du_wrongs(n, b, order, unit="", unit1=None):
    out = []
    u = " " + unit if unit else ""
    for k in order:
        if k == "times":                        # multiplied by the fraction: “dividing makes smaller”
            out.append(R(n, b, unit1 if (unit1 and n < b) else unit))
        elif k == "one":                        # counted the pieces in 1 whole only
            out.append((num(b) + u, F(b)))
        elif k == "add":                        # added
            out.append((num(n + b) + u, F(n + b)))
        elif k == "flip":                       # multiplied the denominator
            out.append(R(1, n * b, unit))
        elif k == "sub":                        # subtracted
            if b > n:
                out.append((num(b - n) + u, F(b - n)))
        else:
            raise ValueError(k)
    return out


# ============================================================ set 1: whole number × unit fraction
def set_times():
    its = []
    # A) rows of bars
    for n, b, order in [(4, 3, ["bottom", "flip", "attach", "addtop"]),
                        (3, 5, ["both", "flip", "addtop", "times"]),
                        (5, 2, ["flip", "bottom", "attach", "times"]),
                        (2, 3, ["attach", "bottom", "flip", "both"]),
                        (5, 6, ["bottom", "addtop", "flip", "times"]),
                        (7, 4, ["times", "both", "flip", "attach"])]:
        qq = (fig(copies_svg(n, b)) + "Each bar is 1 whole. %s of each bar is shaded. What is %s?"
              % (fr(1, b), nu(n, b)))
        lead = "Count the shaded parts: %d bars with 1 %s each. " % (n, parts(b, 1))
        its.append(mcq(qq, R(n, b), nu_wrongs(n, b, order), nu_e(n, b, lead)))
    # B) number-line jumps
    for n, b, order in [(3, 4, ["bottom", "flip", "times", "attach"]),
                        (5, 3, ["flip", "both", "attach", "times"]),
                        (2, 5, ["times", "bottom", "flip", "addtop"]),
                        (7, 2, ["attach", "flip", "times", "bottom"])]:
        ends = max(1, -(-n // b))
        qq = (fig(line_svg(ends, b, n)) + "Each jump is %s. Where do %d jumps from 0 land? %s = <b>?</b>"
              % (fr(1, b), n, nu(n, b)))
        lead = "Count the jumps: %d jumps of %s. " % (n, fr(1, b))
        its.append(mcq(qq, R(n, b), nu_wrongs(n, b, order), nu_e(n, b, lead)))
    # C) calculate
    for form, n, b, order in [("nu", 2, 7, ["bottom", "flip", "attach", "times"]),
                              ("un", 3, 8, ["both", "flip", "times", "attach"]),
                              ("nu", 4, 9, ["flip", "bottom", "attach", "times"]),
                              ("un", 5, 12, ["bottom", "attach", "flip", "times"]),
                              ("nu", 7, 10, ["times", "both", "flip", "attach"]),
                              ("un", 9, 4, ["both", "flip", "attach", "times"])]:
        expr = nu(n, b) if form == "nu" else un(b, n)
        qq = "%s = <b>?</b><br>Write the answer as a fraction." % expr
        e = nu_e(n, b, "" if form == "nu" else "%s is the same as %s. " % (un(b, n), nu(n, b)))
        its.append(mcq(qq, R(n, b), nu_wrongs(n, b, order), e))
    # D) repeated addition and reasoning
    qq = "%s + %s + %s = <b>?</b>" % (fr(1, 5), fr(1, 5), fr(1, 5))
    its.append(mcq(qq, R(3, 5), [R(3, 15), ("3", F(3)), R(5, 3)],
                   "Add the numerators and keep the denominator: 1 + 1 + 1 = 3 fifths, so the sum is <b>%s</b>. "
                   "Do not add the denominators: the pieces are still fifths. This is the same as %s."
                   % (fr(3, 5), nu(3, 5))))
    qq = "Which multiplication is the same as %s?" % " + ".join([fr(1, 6)] * 4)
    its.append(mcq(qq, (nu(4, 6), None), [(nu(6, 4), None), ("4 × 6", None), ("4 + %s" % fr(1, 6), None)],
                   "There are 4 groups of %s, so it is <b>%s</b> = %s. Check the other choices: %s = %s, 4 × 6 = 24, "
                   "and 4 + %s = 4 %s." % (fr(1, 6), nu(4, 6), fr(4, 6), nu(6, 4), fr(6, 4), fr(1, 6), fr(1, 6))))
    qq = "<b>?</b> × %s = %s" % (fr(1, 8), fr(5, 8))
    its.append(mcq(qq, ("5", F(5)), [("40", F(40)), ("8", F(8)), ("3", F(3))],
                   "%s means 5 eighths. 5 groups of %s make 5 eighths, so the missing number is <b>5</b>. "
                   "Check: %s = %s." % (fr(5, 8), fr(1, 8), nu(5, 8), fr(5, 8))))
    qq = "Which is the same as %s?" % nu(3, 4)
    its.append(mcq(qq, ("3 fourths", None), [("4 thirds", None), ("12 fourths", None), ("3 wholes and 1 fourth", None)],
                   "%s is 3 groups of 1 fourth, which is <b>3 fourths</b> = %s." % (nu(3, 4), fr(3, 4))))
    assert len(its) == 20, len(its)
    return {"title": "Whole number × unit fraction with bars", "items": its}


# ============================================================ set 2: products as mixed numbers
def set_mixed():
    its = []
    # A) pictures: pieces put together into wholes
    for n, b, order in [(7, 3, ["attach", "den", "swap", "up"]),
                        (5, 2, ["attach", "up", "den", "both"]),
                        (9, 4, ["den", "attach", "swap", "up"]),
                        (7, 5, ["up", "attach", "den", "swap"]),
                        (8, 3, ["swap", "attach", "den", "up"])]:
        qq = (fig(fill_svg(n, b)) + "The shaded parts show %s = %s. Write it as a mixed number."
              % (nu(n, b), fr(n, b)))
        lead = "Count the full bars, then the extra pieces. "
        its.append(mcq(qq, S(F(n, b)), mixed_wrongs(n, b, order), mixed_e(n, b, lead)))
    # B) calculate
    for n, b, order in [(7, 2, ["attach", "den", "up", "both"]),
                        (9, 2, ["den", "attach", "up", "both"]),
                        (4, 3, ["attach", "swap", "den", "up"]),
                        (7, 4, ["swap", "attach", "den", "up"]),
                        (8, 5, ["attach", "den", "swap", "up"]),
                        (9, 5, ["den", "swap", "attach", "up"]),
                        (7, 6, ["attach", "den", "up", "both"]),
                        (9, 8, ["den", "attach", "up", "both"]),
                        (5, 4, ["attach", "swap", "up", "den"]),
                        (9, 7, ["attach", "den", "swap", "up"])]:
        qq = "%s = <b>?</b><br>Write the answer as a mixed number." % nu(n, b)
        its.append(mcq(qq, S(F(n, b)), mixed_wrongs(n, b, order), mixed_e(n, b)))
    # C) whole-number answers
    for n, b, order in [(6, 3, ["times", "both", "attach", "flip"]),
                        (8, 4, ["both", "attach", "times", "flip"]),
                        (9, 3, ["attach", "times", "flip", "both"])]:
        qq = "%s = <b>?</b>" % nu(n, b)
        its.append(mcq(qq, S(F(n, b)), nu_wrongs(n, b, order), nu_e(n, b)))
    # D) reasoning
    qq = "Between which two whole numbers is %s?" % nu(7, 2)
    its.append(mcq(qq, ("3 and 4", None), [("7 and 8", None), ("2 and 3", None), ("0 and 1", None)],
                   "%s = %s. 7 ÷ 2 = 3 remainder 1, so it is 3 %s. That is <b>between 3 and 4</b>."
                   % (nu(7, 2), fr(7, 2), fr(1, 2))))
    qq = "Which is greater: %s or 2?" % nu(7, 4)
    its.append(mcq(qq, ("2", None), [(nu(7, 4), None), ("They are equal.", None), ("You can’t tell.", None)],
                   "%s = %s = 1 %s. 2 wholes would be 8 fourths, and 7 fourths is 1 fourth less. So <b>2</b> is greater."
                   % (nu(7, 4), fr(7, 4), fr(3, 4))))
    assert len(its) == 20, len(its)
    return {"title": "Products as mixed numbers", "items": its}


# ============================================================ set 3: whole number ÷ unit fraction
def set_divide(P):
    its = []
    # A) bar pictures
    for n, b, order in [(3, 4, ["times", "one", "add", "flip"]), (2, 3, ["one", "times", "flip", "add"]),
                        (4, 2, ["times", "add", "flip", "one"]), (2, 5, ["flip", "times", "one", "add"]),
                        (3, 3, ["times", "one", "flip", "add"]), (2, 6, ["one", "times", "add", "flip"])]:
        qq = (fig(wholes_svg(n, b)) + "Each whole is cut into %s. How many %s are in %d? %s = <b>?</b>"
              % (parts(b), parts(b), n, du(n, b)))
        its.append(mcq(qq, S(F(n * b)), du_wrongs(n, b, order), du_e(n, b)))
    # B) number-line jumps
    for n, b, order in [(2, 4, ["times", "one", "flip", "add"]), (3, 2, ["one", "times", "add", "flip"]),
                        (3, 5, ["flip", "one", "times", "add"]), (4, 3, ["times", "add", "one", "flip"])]:
        qq = (fig(line_svg(n, b, n * b)) + "Each jump is %s. How many jumps from 0 to %d? %s = <b>?</b>"
              % (fr(1, b), n, du(n, b)))
        e = "Count the jumps: %d in each whole. " % b + du_e(n, b)
        its.append(mcq(qq, S(F(n * b)), du_wrongs(n, b, order), e))
    # C) calculate
    for n, b, order in [(5, 3, ["times", "one", "add", "flip"]), (4, 6, ["times", "add", "flip", "one"]),
                        (7, 4, ["flip", "times", "one", "add"]), (9, 5, ["times", "one", "add", "flip"]),
                        (6, 8, ["times", "flip", "add", "one"]), (2, 12, ["times", "sub", "one", "add"])]:
        qq = "%s = <b>?</b>" % du(n, b)
        its.append(mcq(qq, S(F(n * b)), du_wrongs(n, b, order), du_e(n, b)))
    # D) reasoning and mistakes
    nm, he, his = P.next()
    qq = "%s says %s = %s. What mistake did %s make?" % (nm, du(3, 4), fr(3, 4), he)
    its.append(mcq(qq, ("%s multiplied by %s instead of dividing." % (cap(he), fr(1, 4)), None),
                   [("%s counted the fourths in 1 whole only." % cap(he), None),
                    ("%s added 3 and 4." % cap(he), None),
                    ("Nothing. The answer is correct.", None)],
                   "3 × %s = %s, so %s multiplied. %s asks how many fourths are in 3. Each whole has 4 fourths, "
                   "so the answer is 3 × 4 = <b>12</b>, which is more than 3." % (fr(1, 4), fr(3, 4), nm, du(3, 4))))
    qq = "Which is the same as %s?" % du(6, 3)
    its.append(mcq(qq, ("6 × 3", None), [(nu(6, 3), None), ("6 ÷ 3", None), ("3 ÷ 6", None)],
                   "%s asks how many thirds are in 6. Each whole has 3 thirds, so it is <b>6 × 3</b> = 18. "
                   "%s and 6 ÷ 3 are both 2, and 3 ÷ 6 is %s." % (du(6, 3), nu(6, 3), fr(1, 2))))
    qq = "<b>?</b> ÷ %s = 30" % fr(1, 5)
    its.append(mcq(qq, ("6", F(6)), [("150", F(150)), ("25", F(25)), ("35", F(35))],
                   "Each whole has 5 fifths. How many wholes make 30 fifths? 30 ÷ 5 = <b>6</b>. "
                   "Check: %s = 6 × 5 = 30." % du(6, 5)))
    qq = "8 ÷ <b>?</b> = 24"
    its.append(mcq(qq, R(1, 3), [("3", F(3)), ("16", F(16)), R(1, 16)],
                   "24 ÷ 8 = 3, so each whole holds 3 equal pieces. The pieces are thirds: "
                   "%s = 8 × 3 = 24. The missing number is <b>%s</b>." % (du(8, 3), fr(1, 3))))
    assert len(its) == 20, len(its)
    return {"title": "Whole number ÷ unit fraction", "items": its}


# ============================================================ set 4: choose × or ÷
def set_choose(P):
    its = []

    def ch4(n, b):
        return [(nu(n, b), None), (du(n, b), None), ("%s ÷ %d" % (fr(1, b), n), None), ("%d + %s" % (n, fr(1, b)), None)]

    def story(qq, n, b, op, why):
        c = ch4(n, b)
        right = c[0] if op == "x" else c[1]
        rest = [x for x in c if x is not right]
        if op == "x":
            e = ("%s There are %d equal groups of %s, so multiply: <b>%s</b> = %s."
                 % (why, n, fr(1, b), nu(n, b), show(F(n, b))))
        else:
            e = ("%s The question asks how many pieces fit, so divide: <b>%s</b> = %d × %d = %d."
                 % (why, du(n, b), n, b, n * b))
        its.append(mcq(qq + " Which expression answers the question?", right, rest, e))

    nm, he, his = P.next()
    story("%s eats %s of a sandwich each day for 3 days. How much sandwich does %s eat in all?" % (nm, fr(1, 4), he),
          3, 4, "x", "Each day is one group of %s." % fr(1, 4))
    story("A bag holds 3 cups of flour. A scoop holds %s cup. How many scoops of flour are in the bag?" % fr(1, 4),
          3, 4, "d", "Count how many %s cup scoops make 3 cups." % fr(1, 4))
    story("Each of 5 friends drinks %s L of juice. How much juice do they drink altogether?" % fr(1, 3),
          5, 3, "x", "Each friend is one group of %s L." % fr(1, 3))
    nm, he, his = P.next()
    story("%s has a 2 m board. %s cuts it into pieces that are each %s m long. How many pieces does %s get?"
          % (nm, cap(he), fr(1, 3), he), 2, 3, "d", "Count how many %s m pieces fit in 2 m." % fr(1, 3))
    story("A muffin recipe uses %s cup of oats for each batch. How many cups of oats do 7 batches need?" % fr(1, 2),
          7, 2, "x", "Each batch is one group of %s cup." % fr(1, 2))
    story("A class has 4 pizzas. Each student gets %s of a pizza. How many students get a slice?" % fr(1, 8),
          4, 8, "d", "Count how many %s pizza slices are in 4 pizzas." % fr(1, 8))
    nm, he, his = P.next()
    story("%s walks %s km with %s dog, 4 times a week. How far does %s walk with the dog each week?"
          % (nm, fr(1, 5), his, he), 4, 5, "x", "Each walk is one group of %s km." % fr(1, 5))
    story("A trail loop at the conservation area is %s km long. How many loops make 5 km?" % fr(1, 2),
          5, 2, "d", "Count how many %s km loops fit in 5 km." % fr(1, 2))
    nm, he, his = P.next()
    story("%s uses %s m of ribbon for each bow. How much ribbon does %s need for 8 bows?" % (nm, fr(1, 3), he),
          8, 3, "x", "Each bow is one group of %s m." % fr(1, 3))
    story("A 2 L jug of milk is poured into cups. Each cup holds %s L. How many cups can be filled?" % fr(1, 5),
          2, 5, "d", "Count how many %s L cups fit in 2 L." % fr(1, 5))
    story("Each hockey drill at practice lasts %s h. The coach runs 5 drills. How many hours do the drills take?" % fr(1, 6),
          5, 6, "x", "Each drill is one group of %s h." % fr(1, 6))
    nm, he, his = P.next()
    story("%s has 9 m of rope for a canoe trip. %s cuts it into pieces %s m long. How many pieces does %s get?"
          % (nm, cap(he), fr(1, 2), he), 9, 2, "d", "Count how many %s m pieces fit in 9 m." % fr(1, 2))
    story("A bag of trail mix has a mass of %s kg. How many kilograms do 9 bags have?" % fr(1, 10),
          9, 10, "x", "Each bag is one group of %s kg." % fr(1, 10))
    story("A sugar shack has 6 L of maple syrup. It fills small bottles that each hold %s L. How many bottles can it fill?"
          % fr(1, 4), 6, 4, "d", "Count how many %s L bottles fit in 6 L." % fr(1, 4))

    # B) expression → question
    def match(expr_html, op, n, b, unit, right, wrongs, e):
        qq = "Which question is answered by %s?" % expr_html
        its.append(mcq(qq, (right, None), [(w, None) for w in wrongs], e))

    match(du(3, 5), "d", 3, 5, "m", "How many %s m pieces can you cut from 3 m of string?" % fr(1, 5),
          ["How long are 3 pieces of string that are each %s m long?" % fr(1, 5),
           "How much longer is 3 m than %s m?" % fr(1, 5),
           "A %s m piece is cut into 3 equal parts. How long is each part?" % fr(1, 5)],
          "%s asks how many pieces of %s fit in 3. That matches <b>how many %s m pieces are in 3 m</b>: 3 × 5 = 15 pieces."
          % (du(3, 5), fr(1, 5), fr(1, 5)))
    match(nu(3, 5), "x", 3, 5, "m", "How long are 3 pieces of string that are each %s m long?" % fr(1, 5),
          ["How many %s m pieces can you cut from 3 m of string?" % fr(1, 5),
           "How much longer is 3 m than %s m?" % fr(1, 5),
           "A %s m piece is cut into 3 equal parts. How long is each part?" % fr(1, 5)],
          "%s means 3 groups of %s. That matches <b>3 pieces that are each %s m long</b>: %s m in all."
          % (nu(3, 5), fr(1, 5), fr(1, 5), fr(3, 5)))
    match(du(4, 3), "d", 4, 3, "", "How many %s cup scoops of rice are in 4 cups?" % fr(1, 3),
          ["How much rice is in 4 scoops that each hold %s cup?" % fr(1, 3),
           "How much rice is left if you use %s cup from 4 cups?" % fr(1, 3),
           "How much rice is in each bowl if %s cup is shared among 4 bowls?" % fr(1, 3)],
          "%s asks how many pieces of %s fit in 4. That matches <b>how many %s cup scoops are in 4 cups</b>: 4 × 3 = 12 scoops."
          % (du(4, 3), fr(1, 3), fr(1, 3)))
    match(nu(4, 3), "x", 4, 3, "", "How much rice is in 4 scoops that each hold %s cup?" % fr(1, 3),
          ["How many %s cup scoops of rice are in 4 cups?" % fr(1, 3),
           "How much rice is left if you use %s cup from 4 cups?" % fr(1, 3),
           "How much rice is in each bowl if %s cup is shared among 4 bowls?" % fr(1, 3)],
          "%s means 4 groups of %s. That matches <b>4 scoops of %s cup each</b>: %s = 1 %s cups."
          % (nu(4, 3), fr(1, 3), fr(1, 3), fr(4, 3), fr(1, 3)))
    match(du(2, 10), "d", 2, 10, "", "How many laps of a %s km path make 2 km?" % fr(1, 10),
          ["How far do you go in 2 laps of a %s km path?" % fr(1, 10),
           "How much farther is 2 km than %s km?" % fr(1, 10),
           "What is 2 km plus %s km?" % fr(1, 10)],
          "%s asks how many pieces of %s fit in 2. That matches <b>how many %s km laps make 2 km</b>: 2 × 10 = 20 laps."
          % (du(2, 10), fr(1, 10), fr(1, 10)))
    match(nu(6, 10), "x", 6, 10, "", "How far do you go in 6 laps of a %s km path?" % fr(1, 10),
          ["How many laps of a %s km path make 6 km?" % fr(1, 10),
           "How much farther is 6 km than %s km?" % fr(1, 10),
           "What is 6 km plus %s km?" % fr(1, 10)],
          "%s means 6 groups of %s. That matches <b>6 laps of %s km</b>: %s km."
          % (nu(6, 10), fr(1, 10), fr(1, 10), fr(6, 10)))
    assert len(its) == 20, len(its)
    return {"title": "Choose × or ÷ for a story", "items": its}


# ============================================================ set 5: word problems
def set_words(P):
    its = []

    def add(qq, correct, cands, e):
        its.append(mcq(qq, correct, cands, e))

    def xe(n, b, why, unit):
        """× explanation with a unit after the answer."""
        s = nu_e(n, b, why + " ")
        if n % b == 0:
            w = n // b
            return s.replace("<b>%d</b> %s." % (w, pl(w, "whole", "wholes")), "<b>%d %s</b>." % (w, unit))
        return s.replace("</b>.", " %s</b>." % unit)

    def de(n, b, why, unit, whole, verb=("holds", "hold")):
        """÷ explanation: each whole (pizza, km, L ...) holds b pieces."""
        w1, wn = whole
        return ("%s Each %s %s %d %s, so %d %s %s %d × %d = <b>%d %s</b>. Check: %s = %s = %d."
                % (why, w1, verb[0], b, unit, n, wn, verb[1], n, b, n * b, unit, nu(n * b, b), fr(n * b, b), n))

    # 1 pizza slices
    add("The class orders 3 pizzas. Each pizza is cut into 8 equal slices, so each slice is %s of a pizza. "
        "How many slices are there?" % fr(1, 8),
        ("24 slices", F(24)), du_wrongs(3, 8, ["times", "add", "one"], "slices", "slice"),
        de(3, 8, "Find how many eighths are in 3 pizzas: %s." % du(3, 8), "slices", ("pizza", "pizzas"), ("has", "have")))
    # 2 pizza eaten
    nm, he, his = P.next()
    add("%s eats 3 slices of pizza. Each slice is %s of a pizza. How much of a pizza does %s eat?" % (nm, fr(1, 8), he),
        R(3, 8, "of a pizza"), [R(3, 24, "of a pizza"), ("24 pizzas", F(24)), R(1, 24, "of a pizza"), M(3, 1, 8, "pizzas")],
        nu_e(3, 8, "3 slices of %s each: %s. " % (fr(1, 8), nu(3, 8))) + " Do not multiply the denominator.")
    # 3 laps run
    nm, he, his = P.next()
    add("One lap around the school field is %s km. %s runs 7 laps. How far does %s run?" % (fr(1, 4), nm, he),
        S(F(7, 4), "km"), nu_wrongs(7, 4, ["both", "times", "attach", "flip"], "km"),
        xe(7, 4, "7 laps of %s km each: %s." % (fr(1, 4), nu(7, 4)), "km"))
    # 4 laps needed
    nm, he, his = P.next()
    add("One lap around the school field is %s km. %s wants to run 3 km for the Terry Fox Run. How many laps is that?"
        % (fr(1, 4), nm),
        ("12 laps", F(12)), du_wrongs(3, 4, ["times", "add", "one"], "laps", "lap"),
        de(3, 4, "Find how many %s km laps fit in 3 km: %s." % (fr(1, 4), du(3, 4)), "laps", ("kilometre", "kilometres"), ("is", "are")))
    # 5 rink laps
    nm, he, his = P.next()
    add("One lap of the outdoor skating rink is %s km. %s skates 9 laps. How far does %s skate?" % (fr(1, 10), nm, he),
        R(9, 10, "km"), nu_wrongs(9, 10, ["both", "times", "attach"], "km"),
        xe(9, 10, "9 laps of %s km each: %s." % (fr(1, 10), nu(9, 10)), "km"))
    # 6 rink laps needed
    add("One lap of a skating trail is %s km. How many laps make 2 km?" % fr(1, 5),
        ("10 laps", F(10)), du_wrongs(2, 5, ["times", "one", "add"], "laps", "lap"),
        de(2, 5, "Find how many %s km laps fit in 2 km: %s." % (fr(1, 5), du(2, 5)), "laps", ("kilometre", "kilometres"), ("is", "are")))
    # 7 maple syrup
    add("A sugar shack has 5 L of maple syrup. It pours it into bottles that each hold %s L. How many bottles can it fill?"
        % fr(1, 2),
        ("10 bottles", F(10)), du_wrongs(5, 2, ["times", "add", "one"], "bottles"),
        de(5, 2, "Find how many %s L bottles fit in 5 L: %s." % (fr(1, 2), du(5, 2)), "bottles", ("litre", "litres"), ("fills", "fill")))
    # 8 cookies
    nm, he, his = P.next()
    add("Each batch of cookies uses %s cup of chocolate chips. %s bakes 5 batches. How many cups of chocolate chips does %s use?"
        % (fr(1, 3), nm, he),
        S(F(5, 3), "cups"), nu_wrongs(5, 3, ["attach", "both", "times", "flip"], "cups"),
        xe(5, 3, "5 batches of %s cup each: %s." % (fr(1, 3), nu(5, 3)), "cups"))
    # 9 oranges
    add("At the soccer game, 4 oranges are cut into pieces. Each piece is %s of an orange. How many pieces are there?"
        % fr(1, 6),
        ("24 pieces", F(24)), du_wrongs(4, 6, ["times", "add", "one"], "pieces", "piece"),
        de(4, 6, "Find how many sixths are in 4 oranges: %s." % du(4, 6), "pieces", ("orange", "oranges"), ("has", "have")))
    # 10 jug
    nm, he, his = P.next()
    add("%s fills a 2 L jug using a cup that holds %s L. How many cups does %s pour in?" % (nm, fr(1, 4), he),
        ("8 cups", F(8)), du_wrongs(2, 4, ["times", "add", "one"], "cups", "cup"),
        de(2, 4, "Find how many %s L cups fit in 2 L: %s." % (fr(1, 4), du(2, 4)), "cups", ("litre", "litres"), ("is", "are")))
    # 11 rope
    nm, he, his = P.next()
    add("%s cuts 5 m of rope into pieces that are each %s m long for knot practice. How many pieces does %s get?"
        % (nm, fr(1, 2), he),
        ("10 pieces", F(10)), [R(5, 2, "pieces"), ("7 pieces", F(7)), ("3 pieces", F(3))],
        de(5, 2, "Find how many %s m pieces fit in 5 m: %s." % (fr(1, 2), du(5, 2)), "pieces", ("metre", "metres"), ("makes", "make")))
    # 12 piano
    nm, he, his = P.next()
    add("%s practises piano for %s h each day. How many hours does %s practise in 7 days?" % (nm, fr(1, 3), he),
        S(F(7, 3), "h"), nu_wrongs(7, 3, ["both", "attach", "times", "flip"], "h"),
        xe(7, 3, "7 days of %s h each: %s." % (fr(1, 3), nu(7, 3)), "h"))
    # 13 talks
    add("Each student gives a talk that lasts %s h (10 minutes). The class has 2 h for talks. How many talks fit?"
        % fr(1, 6),
        ("12 talks", F(12)), du_wrongs(2, 6, ["times", "one", "add", "sub"], "talks", "talk"),
        de(2, 6, "Find how many %s h talks fit in 2 h: %s." % (fr(1, 6), du(2, 6)), "talks", ("hour", "hours")))
    # 14 garden
    add("Each tomato plant in the school garden needs %s m of the row. The row is 9 m long. How many plants fit?"
        % fr(1, 2),
        ("18 plants", F(18)), [R(9, 2, "plants"), ("11 plants", F(11)), ("2 plants", F(2))],
        de(9, 2, "Find how many %s m spaces fit in 9 m: %s." % (fr(1, 2), du(9, 2)), "plants", ("metre", "metres")))
    # 15 dog food
    nm, he, his = P.next()
    add("%s’s dog eats %s kg of food each day. How much food does the dog eat in 5 days?" % (nm, fr(1, 4)),
        S(F(5, 4), "kg"), nu_wrongs(5, 4, ["attach", "both", "times", "flip"], "kg"),
        xe(5, 4, "5 days of %s kg each: %s." % (fr(1, 4), nu(5, 4)), "kg"))
    # 16 trail mix
    add("A bag of trail mix for the field trip has a mass of %s kg. The class buys 9 bags. What is the total mass?"
        % fr(1, 8),
        S(F(9, 8), "kg"), nu_wrongs(9, 8, ["both", "attach", "times", "flip"], "kg"),
        xe(9, 8, "9 bags of %s kg each: %s." % (fr(1, 8), nu(9, 8)), "kg"))
    # 17 stickers
    add("Each student gets %s of a sheet of stickers. The teacher has 6 sheets. How many students get stickers?"
        % fr(1, 5),
        ("30 students", F(30)), du_wrongs(6, 5, ["times", "add", "one"], "students"),
        de(6, 5, "Find how many fifths are in 6 sheets: %s." % du(6, 5), "students", ("sheet", "sheets"), ("is enough for", "are enough for")))
    # 18 compare laps
    g, gh, gp = P.next()
    while gh != "she":
        g, gh, gp = P.next()
    bname, bh, bp = P.next()
    while bh != "he":
        bname, bh, bp = P.next()
    add("%s runs 5 laps of a %s km track. %s runs 3 laps of a %s km track. Who runs farther?"
        % (g, fr(1, 4), bname, fr(1, 2)),
        (bname, None), [(g, None), ("They run the same distance.", None), ("You can’t tell.", None)],
        "%s: %s = %s = 1 %s km. %s: %s = %s = 1 %s km. 1 %s is greater than 1 %s, so <b>%s</b> runs farther."
        % (g, nu(5, 4), fr(5, 4), fr(1, 4), bname, nu(3, 2), fr(3, 2), fr(1, 2), fr(1, 2), fr(1, 4), bname))
    # 19 relay
    add("In a relay race, each of 8 runners runs %s km. How far do the runners go altogether?" % fr(1, 4),
        ("2 km", F(2)), nu_wrongs(8, 4, ["both", "times", "attach"], "km"),
        xe(8, 4, "8 runners of %s km each: %s." % (fr(1, 4), nu(8, 4)), "km"))
    # 20 pizza two-step
    nm, he, his = P.next()
    add("%s cuts 2 pizzas into slices that are each %s of a pizza. 9 friends each eat 1 slice. How many slices are left?"
        % (nm, fr(1, 6)),
        ("3 slices", F(3)), [("12 slices", F(12)), ("7 slices", F(7)), ("1 slice", F(1))],
        "First find the number of slices: %s = 2 × 6 = 12 slices. Then subtract the slices eaten: 12 − 9 = <b>3 slices</b>."
        % du(2, 6))
    assert len(its) == 20, len(its)
    return {"title": "Word problems: pizza, laps and more", "items": its}


# ============================================================ lesson
def body_html():
    copies_fig = ("<figure class='sn-fig'>" + copies_svg(4, 3) +
                  "<figcaption>" + nu(4, 3) + ": 4 bars with 1 third shaded in each make 4 thirds = "
                  + fr(4, 3) + ".</figcaption></figure>")
    fill_fig = ("<figure class='sn-fig'>" + fill_svg(7, 3) +
                "<figcaption>" + fr(7, 3) + ": 2 full wholes and 1 third more, so " + fr(7, 3) + " = 2 "
                + fr(1, 3) + ".</figcaption></figure>")
    unit_fig = ("<figure class='sn-fig'>" + wholes_svg(3, 4) +
                "<figcaption>" + du(3, 4) + ": each whole has 4 fourths, so 3 wholes have 12 fourths.</figcaption></figure>")
    return (
        "<h2>The big idea</h2>"
        "<p>A <b>unit fraction</b> has 1 on top, like " + fr(1, 3) + " or " + fr(1, 8) + ". "
        "<b>× a unit fraction</b> means “groups of that piece”. " + nu(4, 3) + " is 4 thirds. "
        "<b>÷ a unit fraction</b> asks “how many pieces fit?” " + du(3, 4) + " asks how many fourths are in 3.</p>"
        "<h2>Whole number × unit fraction</h2>"
        "<p>Count the pieces. The whole number tells how many pieces. The denominator stays the same.</p>"
        + copies_fig
        + ex("Example", nu(5, 6) + " = ?", "5 pieces of 1 sixth make 5 sixths.", fr(5, 6))
        + "<h2>Writing the answer as a mixed number</h2>"
        "<p>When the top number is bigger than the bottom number, make full wholes. Divide the top by the bottom.</p>"
        + fill_fig
        + ex("Example", nu(9, 4) + " = ?",
             "9 × " + fr(1, 4) + " = " + fr(9, 4) + ". 9 ÷ 4 = 2 remainder 1, so 2 wholes and 1 fourth.",
             "2 " + fr(1, 4))
        + "<h2>Whole number ÷ unit fraction</h2>"
        "<p>Each whole has as many pieces as the denominator. Multiply the whole number by the denominator.</p>"
        + unit_fig
        + ex("Example", du(5, 3) + " = ?", "Each whole has 3 thirds. 5 × 3 = 15 thirds.", "15")
        + "<h2>× or ÷?</h2>"
        + table(["The story says…", "Use", "Example"], [
            ["equal groups of a piece: “how much in all?”", "×", "3 days of " + fr(1, 4) + " sandwich: " + nu(3, 4) + " = " + fr(3, 4)],
            ["“how many pieces fit?”, “how many laps?”", "÷", "How many " + fr(1, 4) + " km laps in 3 km? " + du(3, 4) + " = 12"],
        ])
        + "<p>Check your answer: multiplying by a unit fraction gives a <b>smaller</b> answer. "
        "Dividing by a unit fraction gives a <b>bigger</b> answer.</p>"
        + "<h2>Common mistakes</h2>"
        + table(["Mistake", "What to do instead"], [
            [du(3, 4) + " = " + fr(3, 4) + " (multiplying instead of dividing)",
             "Count the fourths: each whole has 4, so 3 wholes have 12. " + du(3, 4) + " = 12."],
            [nu(4, 3) + " = " + fr(4, 12) + " (multiplying the denominator too)",
             "Only the number of pieces changes: 4 thirds = " + fr(4, 3) + "."],
            [fr(7, 3) + " = 7 " + fr(1, 3) + " (writing the whole number in front)",
             "7 ÷ 3 = 2 remainder 1, so " + fr(7, 3) + " = 2 " + fr(1, 3) + "."],
        ])
    )


FAQ = [
    {"q": "How do you multiply a whole number by a unit fraction in Grade 5?",
     "a": "Multiply the whole number by the numerator 1 and keep the denominator. For example, 4 × 1/3 = 4/3, which is 1 1/3."},
    {"q": "How do you divide a whole number by a unit fraction?",
     "a": "Ask how many pieces fit. Multiply the whole number by the denominator: 3 ÷ 1/4 = 3 × 4 = 12, because each whole has 4 fourths."},
    {"q": "Why is 3 ÷ 1/4 bigger than 3?",
     "a": "Dividing by 1/4 counts how many fourths are in 3. There are 4 fourths in every whole, so there are 12 fourths in 3."},
    {"q": "Is multiplying and dividing by unit fractions in the Grade 5 Ontario curriculum?",
     "a": "Yes. Expectation B2.8 in the Grade 5 Number strand asks students to multiply and divide one-digit whole numbers by unit fractions, using tools and drawings."},
]


def gen():
    rnd = random.Random(45809)
    P = People(rnd)
    sets = [set_times(), set_mixed(), set_divide(P), set_choose(P), set_words(P)]
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
        "country": "ca-on", "subject": "math", "grade": "grade-5", "slug": "multiplying-and-dividing-with-unit-fractions",
        "sort": 9, "updated": UPDATED, "pdf_url": "",
        "title": "Multiplying and Dividing with Unit Fractions",
        "seo_title": "Grade 5 Multiplying and Dividing with Unit Fractions Worksheets: 4 × 1/3, 3 ÷ 1/4 (Free, Answer Key, Ontario)",
        "short_title": "Multiplying and dividing with unit fractions",
        "domain": "Number",
        "standard_code": "Grade 5: B2.8",
        "standard_url": "https://www.dcp.edu.gov.on.ca/en/curriculum/elementary-mathematics",
        "standard_text": "Multiply and divide one-digit whole numbers by unit fractions, using appropriate tools and drawings",
        "meta_desc": "Free Grade 5 math worksheets on multiplying and dividing whole numbers by unit fractions: 4 × 1/3 with bar models, mixed-number answers, 3 ÷ 1/4 = 12, choosing × or ÷, and word problems with pizza slices and laps. 100 questions with an answer key, following the Ontario curriculum.",
        "key_big": "4 × 1/3 = 4 thirds = 4/3. 3 ÷ 1/4 asks how many fourths are in 3: 3 × 4 = 12.",
        "key_sub": "Multiplying by a unit fraction gives a smaller answer, so keep the denominator and count the pieces. Dividing by a unit fraction gives a bigger answer, because every whole holds as many pieces as the denominator.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    mark_large(u, "(row of|number line|[0-9]+ wholes?,)")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
