# -*- coding: utf-8 -*-
"""
US Grade 5 Math: Multiply Fractions (5.NF.B.4, 5.NF.B.6)
  python tools/gen_us_math_g5_multiply_fractions.py
Answers are in simplest form (mixed numbers when more than 1), except where a question asks
to count the parts of an area model.
HTML attributes use single quotes (no backslashes in the JSON).
Grade 5 style: numbers 1,000 and above are written with commas.
"""
import json, math, os, random, re
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "us", "math", "grade-5")
UPDATED = "2026-11-02"
DARK = "#4fae74"      # product / shaded part
LIGHT = "#d7ecdf"     # first fraction in an area model
LINE = "#2b2b2b"
THIN = "#9a9a9a"
FONT = "Arial, Helvetica, sans-serif"
GIRLS = ["Maya", "Ava", "Mia", "Zoe", "Lily", "Emma", "Nora", "Ruby", "Sofia", "Grace"]
BOYS = ["Leo", "Noah", "Eli", "Sam", "Ben", "Omar", "Kai", "Jack", "Luis", "Owen"]


# ------------------------------------------------------------ helpers
def f(n):
    """Grade 5 style: 1500 -> 1,500."""
    return "{:,}".format(n)


def fr(a, b):
    return "<span class='fr'><span class='fn'>%d</span><span class='fd'>%d</span></span>" % (a, b)


def mixed(w, r, b):
    if r == 0:
        return f(w)
    if w == 0:
        return fr(r, b)
    return "%s %s" % (f(w), fr(r, b))


def show(v):
    """A Fraction in simplest form: whole number, proper fraction or mixed number."""
    v = F(v)
    q, r = divmod(v.numerator, v.denominator)
    return mixed(q, r, v.denominator)


def raw(v):
    """A Fraction as a (possibly improper) simplest fraction, or a whole number."""
    v = F(v)
    return f(v.numerator) if v.denominator == 1 else fr(v.numerator, v.denominator)


# a factor is (w, n, d): whole part w and fraction part n/d. 3 = (3, 0, 1); 2/5 = (0, 2, 5)
def val(t):
    return F(t[0]) + F(t[1], t[2])


def fx(t):
    return mixed(t[0], t[1], t[2])


def top(t):
    return t[0] * t[2] + t[1]


def improper(t):
    """3 -> 3, 2/5 -> 2/5, 2 1/2 -> 5/2 (never simplified)."""
    if t[1] == 0:
        return f(t[0])
    return fr(top(t), t[2])


def tb(t):
    """(top, bottom) used when multiplying: a whole number is n/1."""
    return (t[0], 1) if t[1] == 0 else (top(t), t[2])


def W(n):
    return (n, 0, 1)


def P(n, d):
    return (0, n, d)


def M(w, n, d):
    return (w, n, d)


def mcq(q, correct, cands, e):
    """correct and cands are (html, value). A distractor whose value equals the answer or an earlier
    distractor is skipped, so no two choices are worth the same. Positions are set by balance()."""
    ch, vals = [correct[0]], [correct[1]]
    for c in cands:
        h, v = c
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
    """Tag pictures that must print larger so their grids and labels stay readable."""
    rx = re.compile(r"<svg (?=[^>]*aria-label='" + pattern + ")")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u


# ------------------------------------------------------------ explanations
def simp_e(n, d, unit=""):
    """Simplify n/d and write it as a mixed number when it is more than 1. unit = (one, many) or a word."""
    v = F(n, d)
    if isinstance(unit, tuple):
        unit = unit[0] if v <= 1 else unit[1]
    ans = "<b>%s%s</b>" % (show(v), " " + unit if unit else "")
    g = math.gcd(n, d)
    mixed_step = v > 1 and v.denominator > 1
    if g > 1 and not mixed_step:
        return " Simplify: divide the top and bottom by %d: %s = %s." % (g, fr(n, d), ans)
    s = ""
    if g > 1:
        s += " Simplify: divide the top and bottom by %d: %s = %s." % (g, fr(n, d), raw(v))
    if mixed_step:
        q, r = divmod(v.numerator, v.denominator)
        return s + " %s ÷ %s = %d R %d, so %s = %s." % (f(v.numerator), f(v.denominator), q, r, raw(v), ans)
    return s + " The answer is %s." % ans


def mul_e(x, y, unit=""):
    """Step-by-step explanation of x × y."""
    s = []
    mx = [t for t in (x, y) if t[0] and t[1]]
    if mx:
        s.append("Change to fractions: " + ", ".join(
            "%s = %s (%d × %d + %d = %d)" % (fx(t), improper(t), t[0], t[2], t[1], top(t)) for t in mx) + ".")
    (a, b), (c, d) = tb(x), tb(y)
    s.append("Multiply the tops and the bottoms: %s × %s = %s." % (
        improper(x) if x[1] else f(a) if b == 1 else fr(a, b),
        improper(y) if y[1] else f(c) if d == 1 else fr(c, d), fr(a * c, b * d)))
    return " ".join(s) + simp_e(a * c, b * d, unit)


# ------------------------------------------------------------ typical wrong answers for x × y
def wrongs(x, y, order, fmt=show):
    """(html, value) pairs from real mistakes, in the order given."""
    (a, b), (c, d) = tb(x), tb(y)
    out = []
    for k in order:
        v = None
        if k == "add":                                  # added instead of multiplying
            v = val(x) + val(y)
        elif k == "parts":                              # multiplied whole parts and fraction parts separately
            if x[0] and x[1] and y[0] and y[1]:
                v = F(x[0] * y[0]) + F(x[1], x[2]) * F(y[1], y[2])
            elif x[1] == 0 and y[0] and y[1]:           # 3 × 2 1/4 -> 6 1/4
                v = F(x[0] * y[0]) + F(y[1], y[2])
            elif y[1] == 0 and x[0] and x[1]:
                v = F(y[0] * x[0]) + F(x[1], x[2])
            elif x[0] == 0 and y[0] and y[1]:           # 3/5 × 1 2/3 -> 1 2/5
                v = F(y[0]) + F(x[1], x[2]) * F(y[1], y[2])
            elif y[0] == 0 and x[0] and x[1]:
                v = F(x[0]) + F(x[1], x[2]) * F(y[1], y[2])
        elif k == "badimp":                             # 2 1/2 -> 3/2 (added the whole number to the top)
            if (x[0] and x[1]) or (y[0] and y[1]):
                def bi(t):
                    return F(t[0] + t[1], t[2]) if t[0] and t[1] else val(t)
                v = bi(x) * bi(y)
        elif k == "cross":                              # cross-multiplied
            if b > 1 or d > 1:
                v = F(a * d, b * c)
        elif k == "lcd":                                # multiplied the tops, kept a common bottom
            if b > 1 and d > 1:
                v = F(a * c, b * d // math.gcd(b, d))
        elif k == "topsadd":                            # multiplied the tops, added the bottoms
            if b > 1 and d > 1:
                v = F(a * c, b + d)
        elif k == "flip":                               # answer upside down
            p = F(a * c, b * d)
            if p != 1:
                v = 1 / p
        elif k == "both":                               # n × a/b: multiplied the top and the bottom
            if b == 1 and d > 1:
                v = F(c, d)
            elif d == 1 and b > 1:
                v = F(a, b)
        elif k == "bottom":                             # n × a/b = a/(n b)
            if b == 1 and d > 1:
                v = F(c, a * d)
            elif d == 1 and b > 1:
                v = F(a, c * b)
        elif k == "addtop":                             # n × a/b = (n + a)/b
            if b == 1 and d > 1:
                v = F(a + c, d)
            elif d == 1 and b > 1:
                v = F(a + c, b)
        elif k == "wholeonly":                          # forgot the fraction part of a mixed number
            if x[0] and x[1]:
                v = F(x[0]) * val(y)
            elif y[0] and y[1]:
                v = val(x) * F(y[0])
        else:
            raise ValueError(k)
        if v is not None and v > 0:
            out.append((fmt(v), v))
    return out


# ------------------------------------------------------------ SVG pieces
def tw(t, fs):
    return len(str(t)) * fs * 0.6


def text(x, y, t, fs=16, col=LINE, anchor="middle", weight="700"):
    return ("<text x='%.1f' y='%.1f' font-size='%d' font-weight='%s' fill='%s' text-anchor='%s'>%s</text>"
            % (x, y, fs, weight, col, anchor, t))


def num_svg(cx, cy, w, n, d, unit=""):
    """A whole, fraction or mixed number (with a unit) centered at (cx, cy). Returns (svg, width, height)."""
    FW, FF, FU = 18, 15, 16
    parts = []
    if w:
        parts.append(("w", tw(w, FW)))
    if n:
        parts.append(("f", max(tw(n, FF), tw(d, FF)) + 4))
    if unit:
        parts.append(("u", len(unit) * FU * 0.72))
    gap = 4
    total = sum(p[1] for p in parts) + gap * (len(parts) - 1)
    x = cx - total / 2
    s = []
    for k, wd in parts:
        if k == "w":
            s.append(text(x + wd / 2, cy + 6, w, FW))
        elif k == "f":
            m = x + wd / 2
            s.append(text(m, cy - 4, n, FF))
            s.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='1.6'/>"
                     % (x + 1, cy + 0.5, x + wd - 1, cy + 0.5, LINE))
            s.append(text(m, cy + 16, d, FF))
        else:
            s.append(text(x + 1, cy + 6, unit, FU, anchor="start", weight="400"))
        x += wd + gap
    h = 36 if n else 22
    return "".join(s), total, h


def groups_svg(q, a, b):
    """q counters in b equal groups; a groups shaded. At most 4 groups in a row."""
    g = q // b
    cols = g if g <= 3 else (g + 1) // 2
    rows = 1 if g <= 3 else 2
    P_, R = 20, 7
    bw, bh = cols * P_ + 10, rows * P_ + 10
    per = b if b <= 5 else (b + 1) // 2
    nrow = (b + per - 1) // per
    GX, GY = 10, 10
    s = []
    for k in range(b):
        x0 = 4 + (k % per) * (bw + GX)
        y0 = 4 + (k // per) * (bh + GY)
        on = k < a
        s.append("<rect x='%d' y='%d' width='%d' height='%d' rx='8' fill='%s' stroke='%s' stroke-width='2'/>"
                 % (x0, y0, bw, bh, LIGHT if on else "#fff", LINE))
        for i in range(g):
            cx = x0 + 5 + P_ / 2 + (i % cols) * P_
            cy = y0 + 5 + P_ / 2 + (i // cols) * P_
            s.append("<circle cx='%.1f' cy='%.1f' r='%d' fill='%s' stroke='%s' stroke-width='1.6'/>"
                     % (cx, cy, R, DARK if on else "#fff", LINE))
    Wd = 8 + per * bw + (per - 1) * GX
    Ht = 8 + nrow * bh + (nrow - 1) * GY
    return svg_wrap(Wd, Ht, "".join(s), "%d counters in %d equal groups with %d groups shaded" % (q, b, a))


def tape_svg(q, a, b, part_labels=False, Wt=300):
    """A bar worth q split into b equal parts, a parts shaded; the total is marked above."""
    x0, y0, H = 6, 36, 36
    s = ["<line x1='%d' y1='16' x2='%d' y2='16' stroke='%s' stroke-width='2'/>" % (x0, x0 + Wt, LINE),
         "<line x1='%d' y1='10' x2='%d' y2='26' stroke='%s' stroke-width='2'/>" % (x0, x0, LINE),
         "<line x1='%d' y1='10' x2='%d' y2='26' stroke='%s' stroke-width='2'/>" % (x0 + Wt, x0 + Wt, LINE)]
    lab = f(q)
    lw = tw(lab, 18) + 12
    s.append("<rect x='%.1f' y='4' width='%.1f' height='24' fill='#fff'/>" % (x0 + Wt / 2 - lw / 2, lw))
    s.append(text(x0 + Wt / 2, 23, lab, 18))
    pw = Wt / float(b)
    for i in range(b):
        s.append("<rect x='%.1f' y='%d' width='%.1f' height='%d' fill='%s' stroke='%s' stroke-width='2'/>"
                 % (x0 + i * pw, y0, pw, H, DARK if i < a else "#fff", LINE))
        if part_labels:
            s.append(text(x0 + i * pw + pw / 2, y0 + 24, f(q // b), 16, "#fff" if i < a else LINE))
    return svg_wrap(Wt + 12, y0 + H + 6, "".join(s), "bar worth %d split into %d equal parts with %d shaded" % (q, b, a))


def grid_svg(cw, rh, b1, b2, sc, sr, light_cols=0, top=None, left=None, bottom=None, U=None, label="grid"):
    """cw × rh whole squares, each cut into b1 columns and b2 rows. The first sc small columns ×
    sr small rows (from the top left) are dark; the first light_cols columns (all rows) are light.
    top / left / bottom are (w, n, d, unit) labels for the dark width, dark height and whole width."""
    if U is None:
        U = min(240.0 / cw, 150.0 / rh)
    cwp, rhp = U / b1, U / b2
    lm = 4
    lab_l = None
    if left:
        lab_l = num_svg(0, 0, *left)
        lm = 10 + lab_l[1] + 4
    tm = 40 if top else 4
    bm = 30 if bottom else 4
    gx, gy = lm, tm
    GW, GH = cw * U, rh * U
    s = []
    if light_cols:
        s.append("<rect x='%.1f' y='%.1f' width='%.1f' height='%.1f' fill='%s'/>" % (gx, gy, light_cols * cwp, GH, LIGHT))
    s.append("<rect x='%.1f' y='%.1f' width='%.1f' height='%.1f' fill='%s'/>" % (gx, gy, sc * cwp, sr * rhp, DARK))
    for i in range(1, cw * b1):                          # thin lines inside the whole squares
        if i % b1:
            x = gx + i * cwp
            s.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='1.4'/>" % (x, gy, x, gy + GH, THIN if not light_cols else LINE))
    for j in range(1, rh * b2):
        if j % b2:
            y = gy + j * rhp
            s.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='1.4'/>" % (gx, y, gx + GW, y, THIN if not light_cols else LINE))
    for i in range(cw + 1):                              # whole squares
        x = gx + i * U
        s.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='3'/>" % (x, gy, x, gy + GH, LINE))
    for j in range(rh + 1):
        y = gy + j * U
        s.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='3'/>" % (gx - 1.5, y, gx + GW + 1.5, y, LINE))
    if sc < cw * b1 or sr < rh * b2:                     # outline the dark rectangle
        s.append("<rect x='%.1f' y='%.1f' width='%.1f' height='%.1f' fill='none' stroke='%s' stroke-width='3.5'/>"
                 % (gx, gy, sc * cwp, sr * rhp, "#1f6b3e"))
    wr = gx + GW + 4
    if top:
        t, tw_, _ = num_svg(gx + sc * cwp / 2, 18, *top)
        s.append(t)
        wr = max(wr, gx + sc * cwp / 2 + tw_ / 2 + 4)
    if lab_l:
        t, _, _ = num_svg(lm - 6 - lab_l[1] / 2, gy + sr * rhp / 2, *left)
        s.append(t)
    if bottom:
        t, _, _ = num_svg(gx + GW / 2, gy + GH + 15, *bottom)
        s.append(t)
    return svg_wrap(int(math.ceil(wr)), int(math.ceil(gy + GH + bm)), "".join(s), label)


def model_svg(a1, b1, a2, b2):
    """Area model for a2/b2 × a1/b1 in a 1-by-1 square: a1 of b1 columns light, a2 of b2 rows of them dark."""
    return grid_svg(1, 1, b1, b2, a1, a2, light_cols=a1, U=150,
                    label="area model: a square cut into %d columns and %d rows, %d columns light, %d by %d dark"
                    % (b1, b2, a1, a1, a2))


# ============================================================ set 1: fraction of a whole number
def of_e(a, b, q):
    p = q // b
    return ("Split %s into %d equal parts: %s ÷ %d = %s in each part. Take %d of the parts: %d × %s = %s. "
            "So %s × %s = <b>%s</b>." % (f(q), b, f(q), b, f(p), a, a, f(p), f(a * p), fr(a, b), f(q), f(a * p)))


def of_wrongs(a, b, q, order):
    out = []
    for k in order:
        v = None
        if k == "one":                   # stopped after dividing: one part only
            v = F(q, b)
        elif k == "unshaded":            # counted the other parts
            v = F(q * (b - a), b)
        elif k == "times":               # multiplied by the top and forgot to divide
            v = F(a * q)
        elif k == "flip":                # used b/a
            v = F(q * b, a)
        elif k == "bya":                 # divided by the top number
            v = F(q, a)
        if v is not None and v.denominator == 1 and v > 0:
            out.append((f(v.numerator), v))
    return out


def set_of(rnd):
    its = []
    # A) equal groups of counters
    for a, b, q in [(2, 3, 12), (3, 8, 16), (3, 5, 15), (3, 7, 21), (2, 5, 10)]:
        qq = fig(groups_svg(q, a, b)) + "The %d counters are in %d equal groups. What is %s of %d?" % (q, b, fr(a, b), q)
        e = of_e(a, b, q) + " In the picture, %d of the %d groups are shaded." % (a, b)
        v = F(a * q, b)
        its.append(mcq(qq, (f(v.numerator), v), of_wrongs(a, b, q, ["one", "unshaded", "times", "flip", "bya"]), e))
    # B) bar models
    for a, b, q in [(3, 5, 20), (3, 4, 24), (5, 8, 40), (4, 7, 28)]:
        qq = fig(tape_svg(q, a, b)) + "The whole bar is %d. What is %s × %d?" % (q, fr(a, b), q)
        e = of_e(a, b, q)
        v = F(a * q, b)
        its.append(mcq(qq, (f(v.numerator), v), of_wrongs(a, b, q, ["one", "times", "unshaded", "flip"]), e))
    # C) whole-number answers without a picture
    for form, a, b, q in [("fq", 3, 8, 24), ("qf", 36, 3, 4), ("of", 5, 6, 30), ("fq", 7, 10, 50),
                          ("of", 2, 9, 45), ("qf", 48, 5, 12)]:
        if form == "qf":
            q, a, b = a, b, q
            qq = "%d × %s = <b>?</b>" % (q, fr(a, b))
        elif form == "fq":
            qq = "%s × %d = <b>?</b>" % (fr(a, b), q)
        else:
            qq = "Find %s of %d." % (fr(a, b), q)
        e = of_e(a, b, q)
        if form == "qf":
            e += " (You can also multiply first: %d × %d = %d, then %d ÷ %d = %d.)" % (q, a, a * q, a * q, b, a * q // b)
        v = F(a * q, b)
        its.append(mcq(qq, (f(v.numerator), v), of_wrongs(a, b, q, ["times", "one", "flip", "bya", "unshaded"]), e))
    # D) answers that are not whole numbers
    for x, y in [(P(2, 3), W(5)), (P(3, 4), W(6)), (W(5), P(3, 8)), (P(4, 5), W(7)), (W(7), P(5, 6))]:
        (a, b), (c, d) = tb(x), tb(y)
        v = val(x) * val(y)
        qq = "%s × %s = <b>?</b><br>Write the answer as a mixed number in simplest form." % (fx(x), fx(y))
        n = x[0] or y[0]
        fa, fb = (x[1], x[2]) if x[1] else (y[1], y[2])
        e = ("Multiply the whole number by the top number and keep the bottom number: %d × %d = %d, so the product is %s."
             % (n, fa, n * fa, fr(n * fa, fb))) + simp_e(n * fa, fb)
        its.append(mcq(qq, (show(v), v), wrongs(x, y, ["both", "add", "bottom", "flip", "addtop"]), e))
    assert len(its) == 20, len(its)
    return {"title": "Fraction of a whole number", "items": its}


# ============================================================ set 2: area models for fraction × fraction
def set_models(rnd):
    its = []
    # A) which multiplication
    for a1, b1, a2, b2 in [(3, 4, 1, 3), (2, 3, 1, 4), (4, 5, 2, 3), (1, 3, 3, 4), (5, 6, 1, 3), (3, 5, 3, 4)]:
        q = (fig(model_svg(a1, b1, a2, b2)) + "The square is 1 whole. The light columns are %s of the square. "
             "Which multiplication does the dark part show?" % fr(a1, b1))
        right = "%s × %s" % (fr(a2, b2), fr(a1, b1))
        cands = [("%s × %s" % (fr(b2 - a2, b2), fr(a1, b1)), F(b2 - a2, b2) * F(a1, b1)),       # counted the white rows
                 ("%s + %s" % (fr(a2, b2), fr(a1, b1)), F(a2, b2) + F(a1, b1)),                 # added
                 ("%s × %s" % (fr(a2, b2), fr(b1 - a1, b1)), F(a2, b2) * F(b1 - a1, b1))]       # counted the white columns
        e = ("The light part is %d of %d columns: %s of the square. The dark part is %d of the %d rows of the light part: "
             "%s of it. So the dark part is %s of %s, which is %s." %
             (a1, b1, fr(a1, b1), a2, b2, fr(a2, b2), fr(a2, b2), fr(a1, b1), right))
        its.append(mcq(q, (right, F(a2, b2) * F(a1, b1)), cands, e))
    # B) what fraction of the square is dark
    cases = [(3, 4, 1, 2), (2, 3, 2, 5), (3, 5, 1, 2), (5, 6, 1, 2), (2, 3, 1, 3), (3, 4, 3, 5), (5, 6, 1, 4), (4, 5, 2, 3)]
    for i, (a1, b1, a2, b2) in enumerate(cases):
        n, d = a1 * a2, b1 * b2
        q = (fig(model_svg(a1, b1, a2, b2)) + "The model shows %s × %s. What fraction of the whole square is dark?"
             % (fr(a2, b2), fr(a1, b1)))
        cands = [(fr(n, d - n), F(n, d - n)),                 # dark compared with not dark
                 (fr(n, a1 * b2), F(n, a1 * b2)),             # dark out of the light part only
                 (fr(a2 + a1, b2 + b1), F(a1 + a2, b1 + b2)), # added tops and bottoms
                 (fr(a1, b1), F(a1, b1))]                     # the light part
        r = i % 4
        cands = cands[r:] + cands[:r]
        e = ("The square is cut into %d × %d = %d equal small rectangles. %d × %d = %d of them are dark. "
             "So %s × %s = %s." % (b1, b2, d, a1, a2, n, fr(a2, b2), fr(a1, b1), fr(n, d)))
        its.append(mcq(q, (fr(n, d), F(n, d)), cands, e))
    # C) size of one small rectangle
    for a1, b1, a2, b2 in [(2, 3, 3, 4), (3, 5, 2, 3), (1, 4, 2, 5)]:
        q = (fig(model_svg(a1, b1, a2, b2)) + "The model shows %s × %s. What fraction of the whole square is "
             "<b>one</b> small rectangle?" % (fr(a2, b2), fr(a1, b1)))
        cands = [(fr(1, b1 + b2), F(1, b1 + b2)), (fr(1, a1 * a2), F(1, a1 * a2)), (fr(1, b1), F(1, b1)),
                 (fr(1, b2), F(1, b2))]
        e = ("There are %d columns and %d rows, so the square is cut into %d × %d = %d equal parts. "
             "One part is %s. This is why you multiply the bottom numbers." % (b1, b2, b1, b2, b1 * b2, fr(1, b1 * b2)))
        its.append(mcq(q, (fr(1, b1 * b2), F(1, b1 * b2)), cands, e))
    # D) count dark parts and all parts
    for a1, b1, a2, b2 in [(4, 5, 3, 4), (2, 3, 4, 5), (5, 8, 1, 2)]:
        n, d = a1 * a2, b1 * b2
        q = (fig(model_svg(a1, b1, a2, b2)) + "The model shows %s × %s. How many small rectangles are dark, "
             "out of how many in all?" % (fr(a2, b2), fr(a1, b1)))
        right = "%d out of %d" % (n, d)
        cands = [("%d out of %d" % (a1 + a2, d), None),      # added columns and rows
                 ("%d out of %d" % (d - n, d), None),        # counted the parts that are not dark
                 ("%d out of %d" % (n, a1 * b2), None),      # out of the light part only
                 ("%d out of %d" % (n, b1 + b2), None) if n < b1 + b2 else ("", None)]
        e = ("Dark: %d %s × %d %s = %d small rectangles. In all: %d columns × %d rows = %d. "
             "So %s × %s = %s." % (a1, "column" if a1 == 1 else "columns", a2, "row" if a2 == 1 else "rows", n, b1, b2, d, fr(a2, b2), fr(a1, b1), fr(n, d)))
        its.append(mcq(q, (right, None), cands, e))
    assert len(its) == 20, len(its)
    return {"title": "Fraction × fraction with area models", "items": its}


# ============================================================ set 3: the rule and simplest form
def set_rule(rnd):
    its = []
    # A) answers already in simplest form
    for (a, b), (c, d), order in [((2, 3), (4, 5), ["lcd", "add", "cross", "topsadd"]),
                                  ((3, 4), (1, 5), ["add", "lcd", "cross", "flip"]),
                                  ((5, 6), (1, 3), ["lcd", "cross", "topsadd", "add"]),
                                  ((3, 7), (2, 5), ["add", "topsadd", "cross", "flip"]),
                                  ((4, 9), (2, 3), ["lcd", "add", "flip", "cross"]),
                                  ((5, 8), (3, 4), ["cross", "lcd", "add", "topsadd"])]:
        x, y = P(a, b), P(c, d)
        v = val(x) * val(y)
        q = "%s × %s = <b>?</b>" % (fr(a, b), fr(c, d))
        e = mul_e(x, y)
        e += " The bottom numbers are multiplied too. You do not need a common denominator."
        its.append(mcq(q, (show(v), v), wrongs(x, y, order), e))
    # B) simplify the answer
    def topsimp(a, b, c, d):            # divided only the top by the common factor
        n, dd = a * c, b * d
        g = math.gcd(n, dd)
        return (fr(n // g, dd), F(n // g, dd)) if g > 1 else ("", None)
    for (a, b), (c, d), order in [((3, 4), (2, 9), ["add", "cross", "lcd"]), ((5, 6), (3, 10), ["cross", "add", "lcd"]),
                                  ((4, 5), (5, 8), ["add", "lcd", "cross"]), ((2, 3), (9, 10), ["cross", "lcd", "add"]),
                                  ((7, 12), (8, 21), ["add", "cross", "lcd"]), ((6, 7), (7, 9), ["lcd", "add", "cross"])]:
        x, y = P(a, b), P(c, d)
        v = val(x) * val(y)
        q = "%s × %s = <b>?</b><br>Write the answer in simplest form." % (fr(a, b), fr(c, d))
        cands = [topsimp(a, b, c, d)] + wrongs(x, y, order)
        its.append(mcq(q, (show(v), v), cands, mul_e(x, y)))
    # C) simplify before multiplying
    for (a, b), (c, d) in [((6, 25), (10, 9)), ((5, 12), (8, 15)), ((9, 14), (7, 12)), ((8, 15), (9, 16))]:
        x, y = P(a, b), P(c, d)
        v = val(x) * val(y)
        g1, g2 = math.gcd(a, d), math.gcd(c, b)
        q = "%s × %s = <b>?</b><br>Write the answer in simplest form." % (fr(a, b), fr(c, d))
        a2_, d2_, c2_, b2_ = a // g1, d // g1, c // g2, b // g2
        e = ("Simplify first: %d and %d share %d, and %d and %d share %d. %s × %s becomes %s × %s = <b>%s</b>. "
             "(Multiplying first gives %s, which also simplifies to %s.)"
             % (a, d, g1, c, b, g2, fr(a, b), fr(c, d), fr(a2_, b2_), fr(c2_, d2_), show(v), fr(a * c, b * d), show(v)))
        cands = [topsimp(a, b, c, d)] + wrongs(x, y, ["cross", "add", "lcd", "topsadd"])
        its.append(mcq(q, (show(v), v), cands, e))
    # D) missing numbers and equal products
    for a, b, m, d, side in [(2, 3, 4, 5, "r"), (3, 5, 7, 8, "l")]:
        n = a * m
        if side == "r":
            q = "%s × <span class='fr'><span class='fn'>?</span><span class='fd'>%d</span></span> = %s" % (fr(a, b), d, fr(n, b * d))
        else:
            q = "<span class='fr'><span class='fn'>?</span><span class='fd'>%d</span></span> × %s = %s" % (d, fr(a, b), fr(n, b * d))
        e = ("The tops are multiplied: %d × ? = %d. %d ÷ %d = %d, so the missing number is <b>%d</b>. Check: %d × %d = %d and %d × %d = %d."
             % (a, n, n, a, m, m, a, m, n, b, d, b * d))
        cands = [(str(n - a), F(n - a)), (str(n * a), F(n * a)), (str(n + a), F(n + a)), (str(b * d // b), F(d))]
        its.append(mcq(q, (str(m), F(m)), cands, e))
    for (a, b), (c, d) in [((3, 5), (4, 7)), ((2, 9), (5, 8))]:
        v = F(a, b) * F(c, d)
        q = "Which product is equal to %s × %s?" % (fr(a, b), fr(c, d))
        right = "%s × %s" % (fr(c, b), fr(a, d))
        cands = [("%s × %s" % (fr(a, c), fr(b, d)), F(a, c) * F(b, d)),
                 ("%s × %s" % (fr(b, a), fr(d, c)), F(b, a) * F(d, c)),
                 ("%s + %s" % (fr(a, b), fr(c, d)), F(a, b) + F(c, d))]
        e = ("Both products have tops %d × %d = %d and bottoms %d × %d = %d, so both equal %s. "
             "Swapping the top numbers does not change the answer." % (a, c, a * c, b, d, b * d, fr(a * c, b * d)))
        its.append(mcq(q, (right, v), cands, e))
    assert len(its) == 20, len(its)
    return {"title": "Multiply tops, multiply bottoms, simplify", "items": its}


# ============================================================ set 4: area with fractional sides, mixed numbers
SQ = {"ft": "sq ft", "m": "sq m", "in": "sq in", "yd": "sq yd", "cm": "sq cm"}


def set_area(rnd):
    its = []
    # A) tiling a unit square
    for (a1, b1), (a2, b2), u in [((3, 4), (2, 3), "ft"), ((2, 5), (3, 4), "m"), ((5, 6), (1, 2), "yd"), ((2, 3), (1, 4), "ft")]:
        x, y = P(a1, b1), P(a2, b2)
        v = val(x) * val(y)
        sq = SQ[u]
        q = (fig(grid_svg(1, 1, b1, b2, a1, a2, top=(0, a1, b1, u), left=(0, a2, b2, u), bottom=(1, 0, 1, u), U=150,
                          label="grid: a 1 %s square cut into %d by %d tiles, %d by %d shaded" % (u, b1, b2, a1, a2)))
             + "The big square is 1 %s on each side. What is the area of the shaded rectangle?" % u)
        e = ("The square is cut into %d × %d = %d tiles, so each tile is %s %s. The shaded rectangle has %d × %d = %d tiles: "
             "%s %s. That is the same as %s × %s = %s." % (b1, b2, b1 * b2, fr(1, b1 * b2), sq, a1, a2, a1 * a2,
                                                           fr(a1 * a2, b1 * b2), sq, fr(a1, b1), fr(a2, b2), fr(a1 * a2, b1 * b2)))
        if math.gcd(a1 * a2, b1 * b2) > 1:
            e += " In simplest form, that is <b>%s %s</b>." % (show(v), sq)
        cands = [("%s %s" % (f(a1 * a2), sq), F(a1 * a2)),                       # counted tiles as whole squares
                 ("%s %s" % (show(val(x) + val(y)), sq), val(x) + val(y)),       # added the sides
                 ("%s %s" % (show(2 * (val(x) + val(y))), sq), 2 * (val(x) + val(y))),   # perimeter
                 ("%s %s" % (fr(1, b1 * b2), sq), F(1, b1 * b2))]                # one tile
        its.append(mcq(q, ("%s %s" % (show(v), sq), v), cands, e))
    # B) rectangles in words
    for (a1, b1), (a2, b2), u, thing in [((5, 6), (3, 5), "m", "A rectangular garden bed"),
                                         ((7, 8), (2, 3), "ft", "A rectangular tray"),
                                         ((3, 4), (4, 9), "yd", "A rectangular rug"),
                                         ((9, 10), (5, 6), "m", "A rectangular window")]:
        x, y = P(a1, b1), P(a2, b2)
        v = val(x) * val(y)
        sq = SQ[u]
        q = "%s is %s %s long and %s %s wide. What is its area? Write the answer in simplest form." % (thing, fr(a1, b1), u, fr(a2, b2), u)
        e = "Area = length × width = %s × %s. %s" % (fr(a1, b1), fr(a2, b2), mul_e(x, y, sq))
        per = 2 * (val(x) + val(y))
        cands = [("%s %s" % (show(val(x) + val(y)), sq), val(x) + val(y)),
                 ("%s %s" % (show(per), u), None),
                 ("%s %s" % (show(F(a1 * b2, b1 * a2)), sq), F(a1 * b2, b1 * a2)),     # cross-multiplied
                 ("%s %s" % (show(F(a1 * a2, b1 * b2 // math.gcd(b1, b2))), sq), F(a1 * a2, b1 * b2 // math.gcd(b1, b2)))]
        ch = mcq(q, ("%s %s" % (show(v), sq), v), [cands[0], cands[3], cands[1], cands[2]], e)
        its.append(ch)
    # C) tiling with mixed-number sides
    for top_, left_, u in [(M(2, 1, 2), M(1, 1, 3), "ft"), (M(1, 1, 2), M(1, 1, 2), "m"),
                           (M(1, 3, 4), M(1, 1, 2), "yd"), (M(2, 1, 3), M(1, 1, 2), "ft")]:
        b1, b2 = top_[2], left_[2]
        sc, sr = top(top_), top(left_)
        cw, rh = top_[0] + 1, left_[0] + 1
        v = val(top_) * val(left_)
        sq = SQ[u]
        q = (fig(grid_svg(cw, rh, b1, b2, sc, sr, top=top_ + (u,), left=left_ + (u,),
                          label="grid: squares of 1 %s cut into %d by %d tiles, %d by %d shaded" % (u, b1, b2, sc, sr)))
             + "Each thick square is 1 %s. Each tile is %s %s. What is the area of the shaded rectangle?" % (sq, fr(1, b1 * b2), sq))
        e = ("The shaded rectangle is %d tiles across and %d tiles down: %d × %d = %d tiles of %s %s, which is %s %s. "
             "Check with the side lengths: %s" % (sc, sr, sc, sr, sc * sr, fr(1, b1 * b2), sq, fr(sc * sr, b1 * b2), sq,
                                                   mul_e(top_, left_, sq)))
        cands = [(s_ + " " + sq, v_) for s_, v_ in wrongs(top_, left_, ["parts", "add", "badimp", "flip"])]
        cands.insert(2, ("%s %s" % (f(top_[0] * left_[0]), sq), F(top_[0] * left_[0])))   # whole squares only
        its.append(mcq(q, ("%s %s" % (show(v), sq), v), cands, e))
    # D) mixed numbers without pictures
    for x, y, order in [(W(3), M(2, 1, 4), ["parts", "add", "both", "badimp"]),
                        (M(1, 2, 3), P(3, 5), ["parts", "add", "badimp", "cross"]),
                        (M(2, 1, 4), M(1, 1, 3), ["parts", "badimp", "add", "flip"]),
                        (M(1, 3, 4), P(2, 7), ["parts", "add", "badimp", "cross"])]:
        v = val(x) * val(y)
        q = "%s × %s = <b>?</b><br>Write the answer in simplest form." % (fx(x), fx(y))
        e = mul_e(x, y)
        if x[1] == 0:
            e += " (Or: 3 × 2 = 6 and 3 × %s = %s, so 6 + %s = %s. Multiply both parts.)" % (fr(1, 4), fr(3, 4), fr(3, 4), show(v))
        else:
            e += " Do not multiply the whole numbers and the fractions separately."
        its.append(mcq(q, (show(v), v), wrongs(x, y, order), e))
    # E) squares and rectangles with mixed-number sides
    for x, y, u, order in [(P(2, 3), None, "yd", ["topsadd", "add"]),
                           (M(1, 1, 2), None, "ft", ["parts", "add", "badimp"]),
                           (W(4), M(2, 3, 4), "ft", ["parts", "add", "badimp", "wholeonly"]),
                           (M(3, 1, 3), P(3, 5), "m", ["parts", "badimp", "add", "cross"])]:
        sq = SQ[u]
        if y is None:
            y = x
            q = "A square tile has sides that are %s %s long. What is the area of the tile?" % (fx(x), u)
            e = "Area of a square = side × side = %s × %s. " % (fx(x), fx(x)) + mul_e(x, x, sq)
            extra = [("%s %s" % (show(4 * val(x)), sq), 4 * val(x)),       # perimeter (4 sides)
                     ("%s %s" % (show(2 * val(x)), sq), 2 * val(x))]        # doubled the side
        else:
            q = "A rectangle is %s %s long and %s %s wide. What is its area?" % (fx(x), u, fx(y), u)
            e = "Area = length × width = %s × %s. " % (fx(x), fx(y)) + mul_e(x, y, sq)
            extra = [("%s %s" % (show(2 * (val(x) + val(y))), sq), 2 * (val(x) + val(y)))]   # perimeter
        v = val(x) * val(y)
        cands = [(s_ + " " + sq, v_) for s_, v_ in wrongs(x, y, order)]
        its.append(mcq(q, ("%s %s" % (show(v), sq), v), cands[:2] + extra + cands[2:], e))
    assert len(its) == 20, len(its)
    return {"title": "Area with fraction sides and mixed numbers", "items": its}


# ============================================================ set 5: word problems
UNITS = {"cup": ("cup", "cups"), "mile": ("mile", "miles"), "pound": ("pound", "pounds"), "yard": ("yard", "yards"),
         "hour": ("hour", "hours"), "gallon": ("gallon", "gallons"), "liter": ("liter", "liters"),
         "sqft": ("sq ft", "sq ft"), "sqin": ("sq in", "sq in"), "meter": ("meter", "meters")}


def qty(v, unit):
    one, many = UNITS[unit]
    return "%s %s" % (show(v), one if v <= 1 else many)


def set_words(rnd, Pp):
    its = []

    def add(story, x, y, unit, how, order):
        v = val(x) * val(y)
        e = how + ": %s × %s. " % (fx(x), fx(y)) + mul_e(x, y, UNITS[unit])
        cands = [(qty(w, unit), w) for _, w in wrongs(x, y, order)]
        its.append(mcq(story, (qty(v, unit), v), cands, e))

    nm, he, his = Pp.next()
    add("A pancake recipe uses %s cups of milk. %s makes %s of the recipe. How much milk does %s use?"
        % (fx(M(2, 2, 3)), nm, fr(3, 4), he), P(3, 4), M(2, 2, 3), "cup", "%s of %s cups" % (fr(3, 4), fx(M(2, 2, 3))),
        ["parts", "badimp", "add", "cross"])
    nm, he, his = Pp.next()
    add("A hiking trail is %s miles long. %s has hiked %s of the trail. How far has %s hiked?"
        % (fx(M(2, 1, 2)), nm, fr(3, 5), he), P(3, 5), M(2, 1, 2), "mile", "%s of %s miles" % (fr(3, 5), fx(M(2, 1, 2))),
        ["parts", "add", "badimp", "flip"])
    nm, he, his = Pp.next()
    add("A can holds %s gallon of paint. %s uses %s of the paint in the can. How much paint does %s use?"
        % (fr(3, 4), nm, fr(2, 3), he), P(2, 3), P(3, 4), "gallon", "%s of %s gallon" % (fr(2, 3), fr(3, 4)),
        ["add", "cross", "lcd", "topsadd"])
    nm, he, his = Pp.next()
    add("A smoothie recipe needs %s cup of yogurt. %s makes %s batches. How much yogurt does %s need?"
        % (fr(3, 4), nm, fx(M(2, 1, 2)), he), M(2, 1, 2), P(3, 4), "cup", "%s batches of %s cup" % (fx(M(2, 1, 2)), fr(3, 4)),
        ["parts", "add", "badimp", "wholeonly"])
    nm, he, his = Pp.next()
    add("One lap of the school track is %s mile. %s runs %s laps. How far does %s run?"
        % (fr(1, 4), nm, fx(M(6, 1, 2)), he), M(6, 1, 2), P(1, 4), "mile", "%s laps of %s mile" % (fx(M(6, 1, 2)), fr(1, 4)),
        ["parts", "wholeonly", "add", "badimp"])
    add("A water jug holds %s liters when it is full. Right now it is %s full. How much water is in the jug?"
        % (fx(M(3, 1, 3)), fr(3, 4)), P(3, 4), M(3, 1, 3), "liter", "%s of %s liters" % (fr(3, 4), fx(M(3, 1, 3))),
        ["parts", "add", "badimp", "flip"])
    nm, he, his = Pp.next()
    add("%s has %s yard of ribbon. %s uses %s of it to wrap a gift. How much ribbon does %s use?"
        % (nm, fr(5, 6), cap(he), fr(3, 5), he), P(3, 5), P(5, 6), "yard", "%s of %s yard" % (fr(3, 5), fr(5, 6)),
        ["add", "lcd", "cross", "topsadd"])
    nm, he, his = Pp.next()
    add("A bag holds %s pounds of flour. %s uses %s of the bag to bake bread. How much flour does %s use?"
        % (fx(M(4, 2, 3)), nm, fr(3, 7), he), P(3, 7), M(4, 2, 3), "pound", "%s of %s pounds" % (fr(3, 7), fx(M(4, 2, 3))),
        ["parts", "badimp", "add", "flip"])
    add("A movie is %s hours long. The class has watched %s of it. How many hours have they watched?"
        % (fx(M(1, 1, 2)), fr(2, 3)), P(2, 3), M(1, 1, 2), "hour", "%s of %s hours" % (fr(2, 3), fx(M(1, 1, 2))),
        ["parts", "add", "badimp", "cross"])
    add("A rectangular rug is %s ft long and %s ft wide. What is the area of the rug?"
        % (fx(M(2, 1, 4)), fx(M(1, 2, 3))), M(2, 1, 4), M(1, 2, 3), "sqft", "Area = length × width",
        ["parts", "add", "badimp", "wholeonly"])
    nm, he, his = Pp.next()
    add("%s prints a photo that is %s in long and %s in wide. What is the area of the photo?"
        % (nm, fx(M(4, 1, 2)), fx(M(3, 1, 3))), M(4, 1, 2), M(3, 1, 3), "sqin", "Area = length × width",
        ["parts", "add", "badimp", "wholeonly"])

    # part of a part, as a fraction
    def frac_q(q, x, y, e0, order):
        v = val(x) * val(y)
        e = e0 + " " + mul_e(x, y)
        its.append(mcq(q, (show(v), v), wrongs(x, y, order, show), e))
    frac_q("In a class, %s of the students walk to school. %s of the walkers walk with a brother or sister. "
           "What fraction of the class walks with a brother or sister?" % (fr(2, 3), fr(3, 4)), P(3, 4), P(2, 3),
           "Find %s of %s." % (fr(3, 4), fr(2, 3)), ["add", "cross", "topsadd", "flip"])
    nm, he, his = Pp.next()
    frac_q("%s of a pizza was left after dinner. %s ate %s of what was left. What fraction of the whole pizza did %s eat?"
           % (fr(1, 2), nm, fr(1, 3), he),
           P(1, 3), P(1, 2), "Find %s of %s." % (fr(1, 3), fr(1, 2)), ["add", "lcd", "topsadd", "cross"])
    frac_q("%s of a park is a field. %s of the field is a soccer field. What fraction of the park is the soccer field?"
           % (fr(5, 8), fr(2, 5)), P(2, 5), P(5, 8), "Find %s of %s." % (fr(2, 5), fr(5, 8)), ["add", "cross", "lcd", "topsadd"])

    # whole-number answers in two steps
    def count_q(q, right, cands, e):
        its.append(mcq(q, (right, None), [(c, None) for c in cands], e))
    count_q("There are 24 students in a class. %s of them play an instrument. %s of those players play the piano. "
            "How many students play the piano?" % (fr(2, 3), fr(3, 8)),
            "6 students", ["16 students", "9 students", "10 students"],
            "%s of 24: 24 ÷ 3 = 8, 2 × 8 = 16 students play an instrument. %s of 16: 16 ÷ 8 = 2, 3 × 2 = <b>6</b>. "
            "(Or: %s × %s = %s, and %s of 24 is 6.)" % (fr(2, 3), fr(3, 8), fr(3, 8), fr(2, 3), fr(1, 4), fr(1, 4)))
    count_q("A bakery made 48 cookies. %s of them are chocolate chip. %s of the chocolate chip cookies have nuts. "
            "How many cookies have nuts?" % (fr(5, 8), fr(2, 5)),
            "12 cookies", ["30 cookies", "19 cookies", "18 cookies"],
            "%s of 48: 48 ÷ 8 = 6, 5 × 6 = 30 chocolate chip cookies. %s of 30: 30 ÷ 5 = 6, 2 × 6 = <b>12</b>."
            % (fr(5, 8), fr(2, 5)))
    count_q("A school has 1,500 students. %s of them ride a bus. How many students ride a bus?" % fr(2, 5),
            "600 students", ["300 students", "900 students", "3,000 students"],
            "%s of 1,500: 1,500 ÷ 5 = 300, and 2 × 300 = <b>600</b>. (300 is only %s, and 900 is the students who do not ride.)"
            % (fr(2, 5), fr(1, 5)))
    count_q("An orchard has 2,400 trees. %s of them are apple trees. %s of the apple trees are red apple trees. "
            "How many red apple trees are there?" % (fr(3, 4), fr(2, 3)),
            "1,200 trees", ["1,800 trees", "1,600 trees", "600 trees"],
            "%s of 2,400 is 1,800 apple trees. %s of 1,800: 1,800 ÷ 3 = 600, 2 × 600 = <b>1,200</b>. "
            "(Or: %s × %s = %s, and half of 2,400 is 1,200.)" % (fr(3, 4), fr(2, 3), fr(2, 3), fr(3, 4), fr(1, 2)))
    nm, he, his = Pp.next()
    count_q("%s practices piano for %s hour. %s spends %s of that time on scales. How many minutes does %s spend on scales?"
            % (nm, fr(3, 4), cap(he), fr(2, 3), he),
            "30 minutes", ["45 minutes", "40 minutes", "20 minutes"],
            "%s hour is %s of 60 minutes: 60 ÷ 4 = 15, 3 × 15 = 45 minutes. %s of 45: 45 ÷ 3 = 15, 2 × 15 = <b>30</b> minutes."
            % (fr(3, 4), fr(3, 4), fr(2, 3)))
    nm, he, his = Pp.next()
    count_q("%s's book has 120 pages. %s has read %s of the book. How many pages are left to read?" % (nm, cap(he), fr(3, 4)),
            "30 pages", ["90 pages", "40 pages", "117 pages"],
            "%s of 120: 120 ÷ 4 = 30, 3 × 30 = 90 pages read. Pages left: 120 − 90 = <b>30</b>. "
            "(90 is the pages already read.)" % fr(3, 4))
    assert len(its) == 20, len(its)
    return {"title": "Word problems", "items": its}


# ============================================================ lesson
def body_html():
    of_fig = ("<figure class='sn-fig'>" + groups_svg(12, 2, 3) +
              "<figcaption>" + fr(2, 3) + " of 12: split 12 into 3 equal groups of 4, then take 2 groups. "
              + fr(2, 3) + " × 12 = 8.</figcaption></figure>")
    tape_fig = ("<figure class='sn-fig'>" + tape_svg(20, 3, 5, part_labels=True) +
                "<figcaption>" + fr(3, 5) + " × 20: 20 ÷ 5 = 4 in each part, and 3 parts are 3 × 4 = 12.</figcaption></figure>")
    model_fig = ("<figure class='sn-fig'>" + model_svg(3, 4, 1, 2) +
                 "<figcaption>" + fr(1, 2) + " × " + fr(3, 4) + ": shade " + fr(3, 4) + " of the square (light columns). "
                 "Take " + fr(1, 2) + " of that part (dark). 3 of the 8 equal parts are dark, so "
                 + fr(1, 2) + " × " + fr(3, 4) + " = " + fr(3, 8) + ".</figcaption></figure>")
    tile_fig = ("<figure class='sn-fig'>" + grid_svg(3, 2, 2, 3, 5, 4, top=(2, 1, 2, "ft"), left=(1, 1, 3, "ft"),
                                                     label="grid: squares of 1 ft cut into halves and thirds") +
                "<figcaption>A rectangle " + mixed(2, 1, 2) + " ft by " + mixed(1, 1, 3) + " ft. Each tile is "
                + fr(1, 6) + " sq ft, and 5 × 4 = 20 tiles are shaded: " + fr(20, 6) + " = " + mixed(3, 1, 3)
                + " sq ft.</figcaption></figure>")
    return (
        "<h2>The big idea</h2>"
        "<p>In multiplication with fractions, <b>× means “of.”</b> " + fr(2, 3) + " × 12 means " + fr(2, 3)
        + " of 12. " + fr(1, 2) + " × " + fr(3, 4) + " means half of " + fr(3, 4) + ".</p>"
        "<h2>A fraction of a whole number</h2>"
        "<p>Split the whole number into equal parts (the bottom number), then take some of the parts (the top number).</p>"
        + of_fig + tape_fig +
        "<h2>A fraction of a fraction: the area model</h2>"
        "<p>Draw a square that is 1 whole. Shade one fraction as columns. Then take the other fraction of the shaded part as rows. "
        "The overlap is the answer.</p>"
        + model_fig +
        "<h2>The rule</h2>"
        "<p><b>Multiply the tops. Multiply the bottoms. Then simplify.</b> The bottoms are multiplied because the square is cut "
        "into (bottom × bottom) equal parts.</p>"
        + table(["Problem", "Multiply", "Simplest form"], [
            [fr(2, 3) + " × " + fr(4, 5), fr(8, 15), fr(8, 15)],
            [fr(3, 4) + " × " + fr(2, 9), fr(6, 36), fr(1, 6)],
            [fr(3, 4) + " × 6", fr(18, 4), mixed(4, 1, 2)],
        ])
        + "<p>Tip: you can simplify <b>before</b> you multiply. In " + fr(3, 4) + " × " + fr(2, 9) + ", divide 3 and 9 by 3 and "
        "divide 2 and 4 by 2: " + fr(1, 2) + " × " + fr(1, 3) + " = " + fr(1, 6) + ".</p>"
        + "<h2>Mixed numbers and area</h2>"
        "<p>Change each mixed number to a fraction first. To find the area of a rectangle, multiply the side lengths.</p>"
        + tile_fig
        + ex("Example", "Find " + mixed(2, 1, 2) + " × " + mixed(1, 1, 3) + ".",
             mixed(2, 1, 2) + " = " + fr(5, 2) + " and " + mixed(1, 1, 3) + " = " + fr(4, 3) + ". "
             + fr(5, 2) + " × " + fr(4, 3) + " = " + fr(20, 6) + " = " + fr(10, 3) + ".",
             mixed(3, 1, 3))
        + "<h2>Common mistakes</h2>"
        + table(["Mistake", "What to do instead"], [
            [fr(1, 2) + " × " + fr(3, 4) + " = " + fr(3, 4) + " (keeping a common bottom number)",
             "No common denominator needed: " + fr(3, 8)],
            [fr(1, 2) + " × " + fr(3, 4) + " = " + fr(4, 6) + " (adding)", "Multiply the tops and the bottoms"],
            [mixed(2, 1, 2) + " × " + mixed(1, 1, 3) + " = " + mixed(2, 1, 6) + " (whole parts and fraction parts separately)",
             "Change to " + fr(5, 2) + " × " + fr(4, 3) + " first: " + mixed(3, 1, 3)],
            [mixed(2, 1, 2) + " = " + fr(3, 2) + " (adding the whole number to the top)",
             "2 × 2 + 1 = 5, so " + mixed(2, 1, 2) + " = " + fr(5, 2)],
        ])
    )


FAQ = [
    {"q": "How do you multiply fractions?",
     "a": "Multiply the numerators, multiply the denominators, then simplify. For example, 2/3 × 3/4 = 6/12 = 1/2."},
    {"q": "How do you multiply mixed numbers?",
     "a": "Change each mixed number to an improper fraction, multiply, then simplify. For example, 2 1/2 × 1 1/3 = 5/2 × 4/3 = 20/6 = 3 1/3."},
    {"q": "What is an area model for multiplying fractions?",
     "a": "Shade one fraction of a square as columns, then shade the other fraction of that part as rows; the overlap is the product. For 1/2 × 3/4, 3 of the 8 equal parts overlap, so the answer is 3/8."},
    {"q": "Why is the answer smaller when you multiply by a fraction?",
     "a": "Multiplying by a fraction less than 1 means taking only part of a number. 1/2 × 3/4 is half of 3/4, so it is 3/8, which is less than 3/4."},
]


def gen():
    rnd = random.Random(502)
    Pp = People(rnd)
    sets = [set_of(rnd), set_models(rnd), set_rule(rnd), set_area(rnd), set_words(rnd, Pp)]
    balance(sets, rnd)
    for s in sets:
        assert len(s["items"]) == 20
        for it in s["items"]:
            assert len(set(it["c"])) == 4, it
    return {
        "country": "us", "subject": "math", "grade": "grade-5", "slug": "multiply-fractions", "sort": 2,
        "updated": UPDATED, "pdf_url": "",
        "title": "Multiply Fractions",
        "seo_title": "Grade 5 Multiplying Fractions Worksheets: Area Models, Simplest Form, Mixed Numbers and Word Problems",
        "short_title": "Multiply fractions",
        "domain": "Number and Operations—Fractions",
        "standard_code": "5.NF.B.4, 5.NF.B.6",
        "standard_url": "https://www.thecorestandards.org/Math/Content/5/NF/B/4/",
        "standard_text": "Apply and extend previous understandings of multiplication to multiply a fraction or whole number by a fraction. Interpret the product (a/b) × q as a parts of a partition of q into b equal parts. Find the area of a rectangle with fractional side lengths by tiling it with unit squares of the appropriate unit fraction side lengths, and show that the area is the same as would be found by multiplying the side lengths. Solve real world problems involving multiplication of fractions and mixed numbers, e.g., by using visual fraction models or equations to represent the problem.",
        "meta_desc": "Free Grade 5 worksheets on multiplying fractions: find a fraction of a whole number, use area models for fraction × fraction, multiply tops and bottoms, simplify, multiply mixed numbers, find areas with fraction sides and solve recipe and part-of-a-part word problems. 100 practice questions with answers.",
        "key_big": "Multiply the tops. Multiply the bottoms. Then simplify.",
        "key_sub": "× means “of”: 1/2 × 3/4 is half of 3/4, which is 3/8. Change mixed numbers to fractions first: 2 1/2 × 1 1/3 = 5/2 × 4/3 = 20/6 = 3 1/3.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    mark_large(u, "(area model|grid)")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
