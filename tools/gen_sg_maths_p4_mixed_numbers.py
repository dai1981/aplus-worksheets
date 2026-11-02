# -*- coding: utf-8 -*-
"""
Singapore Primary 4 Maths: Mixed Numbers and Improper Fractions
(MOE 2021 Primary Mathematics Syllabus, Standard. Primary 4: Fractions)
  python3 tools/gen_sg_maths_p4_mixed_numbers.py
Improper fractions from bars and circles, mixed numbers from models and number lines,
converting both ways, comparing and ordering, and word problems with bar models.
Every choice carries its value; a wrong choice never equals the right value or another choice.
Every answer is checked in code with fractions.Fraction.
HTML attributes use single quotes (no backslashes in the JSON). Singapore English.
"""
import json, math, os, random, re, itertools
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "sg", "maths", "primary-4")
SLUG = "mixed-numbers-and-improper-fractions"
UPDATED = "2026-11-03"
FILL = "#4fae74"
FILL2 = "#f2b84b"
FILL3 = "#8fb8e8"
RED = "#c0392b"
BLUE = "#2f6db5"
LINE = "#2b2b2b"
CANT = "You cannot tell"
WORD = {2: "halves", 3: "thirds", 4: "quarters", 5: "fifths", 6: "sixths", 7: "sevenths", 8: "eighths",
        9: "ninths", 10: "tenths", 12: "twelfths"}
ONE = {2: "half", 3: "third", 4: "quarter", 5: "fifth", 6: "sixth", 7: "seventh", 8: "eighth",
       9: "ninth", 10: "tenth", 12: "twelfth"}


# ------------------------------------------------------------ numbers
def fr(a, b):
    return "<span class='fr'><span class='fn'>%s</span><span class='fd'>%s</span></span>" % (a, b)


def frq(b):
    return fr("<b>?</b>", b)


def mx(w, n, d):
    if n == 0:
        return str(w)
    if w == 0:
        return fr(n, d)
    return "%d %s" % (w, fr(n, d))


def Fc(a, b, unit=""):
    return (fr(a, b) + unit, F(a, b))


def Mc(w, n, d, unit=""):
    assert 0 < n < d or n == 0, (w, n, d)
    return (mx(w, n, d) + unit, F(w) + F(n, d))


def Nc(n, unit=""):
    return ("%d%s" % (n, unit), F(n))


def parts(n, d):
    return "%d %s" % (n, ONE[d] if n == 1 else WORD[d])


def tomx(v):
    """Fraction as a mixed number (or whole number) string."""
    w, r = divmod(v.numerator, v.denominator)
    return mx(w, r, v.denominator)


def imp(v, d=None):
    """Fraction as an improper fraction with denominator d."""
    d = d or v.denominator
    return fr((v * d).numerator, d)


# number forms used in comparing: ('i', n, d) improper, ('m', w, n, d) mixed
def I(n, d):
    return ("i", n, d)


def M(w, n, d):
    return ("m", w, n, d)


def nval(x):
    return F(x[1], x[2]) if x[0] == "i" else F(x[1]) + F(x[2], x[3])


def nshow(x):
    return fr(x[1], x[2]) if x[0] == "i" else mx(x[1], x[2], x[3])


def nden(x):
    return x[2] if x[0] == "i" else x[3]


def as_mixed_step(x):
    """'11/4 = 2 3/4' for an improper fraction, '' for a mixed number."""
    if x[0] != "i":
        return ""
    return "%s = %s" % (fr(x[1], x[2]), tomx(nval(x)))


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
    """correct and cands are (html, value) pairs or plain strings (words)."""
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
    """Tag pictures that must print larger so their parts stay readable."""
    rx = re.compile(r"<svg (?=[^>]*aria-label='" + pattern + ")")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u


# ------------------------------------------------------------ SVG text
def txt(x, y, s, size=15, anchor="middle", weight="700", color=LINE):
    return ("<text x='%.1f' y='%.1f' font-size='%d' font-weight='%s' fill='%s' text-anchor='%s'>%s</text>"
            % (x, y, size, weight, color, anchor, s))


def sfr(x, y, a, b, size=15, color=LINE):
    """Stacked fraction drawn in SVG, centred at x. y is the numerator baseline."""
    w = size * 0.62 * max(len(str(a)), len(str(b))) + 4
    return (txt(x, y, a, size, color=color) +
            "<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='1.6'/>"
            % (x - w / 2, y + 5, x + w / 2, y + 5, color) + txt(x, y + size + 5, b, size, color=color))


def lab_w(lab, unit, size=15):
    if isinstance(lab, str):
        return size * 0.62 * len(lab)
    w, n, d = lab
    t = 0
    if w:
        t += size * 0.62 * len(str(w)) + 3
    if n:
        t += size * 0.62 * max(len(str(n)), len(str(d))) + 4
    if unit:
        t += size * 0.55 * len(unit) + 3
    return t


def lab_svg(cx, yc, lab, unit, size=15):
    """Mixed number (w, n, d) with unit, or a string such as '?', centred at cx; yc is the middle line."""
    if isinstance(lab, str):
        return txt(cx, yc + size * 0.36, lab, size + 2)
    w, n, d = lab
    x = cx - lab_w(lab, unit, size) / 2
    s = []
    if w:
        ww = size * 0.62 * len(str(w))
        s.append(txt(x, yc + size * 0.36, w, size, anchor="start"))
        x += ww + 3
    if n:
        fw = size * 0.62 * max(len(str(n)), len(str(d))) + 4
        s.append(sfr(x + fw / 2, yc - 5, n, d, size))
        x += fw
    if unit:
        s.append(txt(x + (4 if n else 1), yc + size * 0.36, unit.strip(), size, anchor="start", weight="400"))
    return "".join(s)


def brace(x0, x1, y, up=True):
    m = (x0 + x1) / 2
    k = -8 if up else 8
    if x1 - x0 < 28:      # too narrow for curls: a bracket with a point
        return ("<path d='M%.1f %.1f L%.1f %.1f L%.1f %.1f L%.1f %.1f M%.1f %.1f L%.1f %.1f' fill='none' stroke='%s' stroke-width='1.8'/>"
                % (x0, y, x0, y + k, x1, y + k, x1, y, m, y + k, m, y + 2 * k, LINE))
    return ("<path d='M%.1f %.1f Q%.1f %.1f %.1f %.1f L%.1f %.1f Q%.1f %.1f %.1f %.1f "
            "Q%.1f %.1f %.1f %.1f L%.1f %.1f Q%.1f %.1f %.1f %.1f' fill='none' stroke='%s' stroke-width='1.8'/>"
            % (x0, y, x0, y + k, x0 + 8, y + k, m - 6, y + k, m, y + k, m, y + 2 * k,
               m, y + k, m + 6, y + k, x1 - 8, y + k, x1, y + k, x1, y, LINE))


# ------------------------------------------------------------ pictures
def bar_row(x0, y, W, H, n, k, col=FILL, sw=2.2):
    return "".join("<rect x='%.2f' y='%.1f' width='%.2f' height='%d' fill='%s' stroke='%s' stroke-width='%.1f'/>"
                   % (x0 + i * W / n, y, W / n, H, col if i < k else "#fff", LINE, sw) for i in range(n))


def wholes_svg(d, N, BW=120, H=36, gap=14, nb=None):
    """N parts of 1/d shaded across bars of d parts (each bar is 1 whole), side by side."""
    nb = nb or -(-N // d)
    s = []
    for b in range(nb):
        x0 = 6 + b * (BW + gap)
        k = max(0, min(d, N - b * d))
        s.append(bar_row(x0, 6, BW, H, d, k))
        s.append("<rect x='%.1f' y='6' width='%d' height='%d' fill='none' stroke='%s' stroke-width='3'/>" % (x0, BW, H, LINE))
    return svg_wrap(12 + nb * BW + (nb - 1) * gap, H + 12, "".join(s),
                    "bars of %d equal parts, %d bars, %d parts shaded" % (d, nb, N))


def pie(cx, cy, r, d, k, col=FILL):
    s = []
    for i in range(d):
        a0 = math.radians(-90 + 360.0 * i / d)
        a1 = math.radians(-90 + 360.0 * (i + 1) / d)
        x0, y0 = cx + r * math.cos(a0), cy + r * math.sin(a0)
        x1, y1 = cx + r * math.cos(a1), cy + r * math.sin(a1)
        s.append("<path d='M%.1f %.1f L%.2f %.2f A%d %d 0 0 1 %.2f %.2f Z' fill='%s' stroke='%s' stroke-width='1.8'/>"
                 % (cx, cy, x0, y0, r, r, x1, y1, col if i < k else "#fff", LINE))
    s.append("<circle cx='%.1f' cy='%.1f' r='%d' fill='none' stroke='%s' stroke-width='2.8'/>" % (cx, cy, r, LINE))
    return "".join(s)


def circles_svg(d, N, r=32, gap=14, nb=None):
    nb = nb or -(-N // d)
    s = []
    for b in range(nb):
        s.append(pie(6 + r + b * (2 * r + gap), 6 + r, r, d, max(0, min(d, N - b * d))))
    return svg_wrap(12 + nb * 2 * r + (nb - 1) * gap, 2 * r + 12, "".join(s),
                    "circles each cut into %d equal parts, %d circles, %d parts shaded" % (d, nb, N))


def tick_line(L, d, Y, x0, x1):
    s = ["<line x1='%.1f' y1='%d' x2='%.1f' y2='%d' stroke='%s' stroke-width='2.5'/>" % (x0, Y, x1, Y, LINE)]
    n = L * d
    for i in range(n + 1):
        X = x0 + (x1 - x0) * i / n
        whole = (i % d == 0)
        s.append("<line x1='%.1f' y1='%d' x2='%.1f' y2='%d' stroke='%s' stroke-width='%s'/>"
                 % (X, Y - (11 if whole else 7), X, Y + (11 if whole else 7), LINE, "2.5" if whole else "1.6"))
        if whole:
            s.append(txt(X, Y + 30, i // d, 16))
    return "".join(s)


def arrow_line_svg(L, d, t, W=380):
    """Number line 0..L in steps of 1/d with a blue arrow pointing at t."""
    x0, x1 = 16, W - 16
    Y = 40
    X = x0 + (x1 - x0) * float(t) / L
    s = [tick_line(L, d, Y, x0, x1),
         "<line x1='%.1f' y1='6' x2='%.1f' y2='%d' stroke='%s' stroke-width='3'/>" % (X, X, Y - 18, BLUE),
         "<path d='M%.1f %d L%.1f %d L%.1f %d Z' fill='%s'/>" % (X - 7, Y - 20, X + 7, Y - 20, X, Y - 9, BLUE)]
    return svg_wrap(W, Y + 38, "".join(s),
                    "number line from 0 to %d with each whole split into %d equal parts and an arrow" % (L, d))


def letters_line_svg(L, d, pts, W=380):
    x0, x1 = 16, W - 16
    Y = 44
    s = [tick_line(L, d, Y, x0, x1)]
    for i, v in enumerate(pts):
        X = x0 + (x1 - x0) * float(v) / L
        s.append("<path d='M%.1f %d L%.1f %d L%.1f %d Z' fill='%s'/>" % (X - 6, Y - 18, X + 6, Y - 18, X, Y - 9, BLUE))
        s.append(txt(X, Y - 22, "ABCD"[i], 17, color=BLUE))
    return svg_wrap(W, Y + 38, "".join(s),
                    "number line from 0 to %d with each whole split into %d equal parts and letters A, B, C and D marked" % (L, d))


def units_svg(n, total, unit, below, shade=0, W=300, only_first=False):
    """Bar model of n equal units. total: label above with a brace. below: [(i0, i1, label)] braces under units.
    shade: the first `shade` units are shaded. only_first: draw only the first unit's divider."""
    x0 = 8
    yb = 60
    Hh = 34
    u = W / n
    s = [lab_svg(x0 + W / 2, 22, total, unit), brace(x0, x0 + W, 54, up=True)]
    for i in range(n):
        if only_first and i > 0:
            break
        s.append("<rect x='%.2f' y='%d' width='%.2f' height='%d' fill='%s' stroke='%s' stroke-width='1.8'/>"
                 % (x0 + i * u, yb, u, Hh, FILL3 if i < shade else "#fff", LINE))
    s.append("<rect x='%.1f' y='%d' width='%d' height='%d' fill='none' stroke='%s' stroke-width='2.6'/>" % (x0, yb, W, Hh, LINE))
    if only_first:
        s.append(txt(x0 + u + (W - u) / 2, yb + Hh / 2 + 6, "?", 17))
    for i0, i1, lab in below:
        a, b = x0 + i0 * u, x0 + i1 * u
        s.append(brace(a + 1, b - 1, yb + Hh + 6, up=False))
        s.append(lab_svg((a + b) / 2, yb + Hh + 38, lab, unit))
    return svg_wrap(x0 + W + 10, yb + Hh + 60, "".join(s), "bar model of %d equal units" % n)


def model_svg(segs, total, unit, W=300):
    """Part-whole bar model. segs: list of (value, label)."""
    tv = sum(v for v, _ in segs)
    x0 = 8
    s = []
    yb = 64
    Hh = 36
    s.append(lab_svg(x0 + W / 2, 22, total, unit))
    s.append(brace(x0, x0 + W, 56, up=True))
    x = x0
    cols = [FILL3, "#ffffff", "#d7e6f7"]
    for i, (v, lab) in enumerate(segs):
        w = W * float(v / tv)
        s.append("<rect x='%.2f' y='%d' width='%.2f' height='%d' fill='%s' stroke='%s' stroke-width='2.2'/>"
                 % (x, yb, w, Hh, cols[i % 3], LINE))
        s.append(brace(x + 2, x + w - 2, yb + Hh + 6, up=False))
        s.append(lab_svg(x + w / 2, yb + Hh + 38, lab, unit))
        assert lab_w(lab, unit) < w + 6, (lab, w)
        x += w
    return svg_wrap(x0 + W + 10, yb + Hh + 62, "".join(s), "bar model: a whole bar split into %d parts" % len(segs))


def compare_svg(rows, diff, unit, W=230):
    """Comparison bar model of two bars. rows: [(name, value, label)]; the longer bar's extra part holds diff."""
    (n1, v1, l1), (n2, v2, l2) = rows
    big, small = max(v1, v2), min(v1, v2)
    x0 = 14 + 8.6 * max(len(n1), len(n2))
    Hh = 40
    s = []
    right = x0 + W
    for j, (nm, v, lab) in enumerate(rows):
        y = 8 + j * (Hh + 16)
        w = W * float(v / big)
        s.append(txt(6, y + Hh / 2 + 5, nm, 15, anchor="start"))
        s.append("<rect x='%.2f' y='%d' width='%.2f' height='%d' fill='%s' stroke='%s' stroke-width='2.2'/>"
                 % (x0, y, w, Hh, FILL3 if j == 0 else FILL2, LINE))
        ws = W * float(small / big)
        if v == big:
            s.append("<line x1='%.2f' y1='%d' x2='%.2f' y2='%d' stroke='%s' stroke-width='2' stroke-dasharray='5 4'/>"
                     % (x0 + ws, y, x0 + ws, y + Hh, LINE))
            assert lab_w(diff, unit) < W - ws - 4, (diff, W - ws)
            s.append(lab_svg(x0 + (ws + W) / 2, y + Hh / 2, diff, unit))
            s.append(lab_svg(x0 + W + 8 + lab_w(lab, unit) / 2, y + Hh / 2, lab, unit))
            right = max(right, x0 + W + 12 + lab_w(lab, unit))
        else:
            s.append(lab_svg(x0 + w / 2, y + Hh / 2, lab, unit))
    return svg_wrap(right + 6, 8 + 2 * Hh + 16 + 8, "".join(s), "bar model comparing two bars")


# ============================================================ explanations and mistakes
def imp_e(n, d):
    q, r = divmod(n, d)
    if r == 0:
        return ("%s means %d %s. Every %d %s make 1 whole: %d ÷ %d = %d. So %s = <b>%d</b>."
                % (fr(n, d), n, WORD[d], d, WORD[d], n, d, q, fr(n, d), q))
    return ("Divide the numerator by the denominator: %d ÷ %d = %d remainder %d. "
            "That is %d whole%s and %d %s left over. The denominator stays %d. So %s = <b>%s</b>."
            % (n, d, q, r, q, "" if q == 1 else "s", r, ONE[d] if r == 1 else WORD[d], d, fr(n, d), mx(q, r, d)))


def imp_cands(n, d):
    q, r = divmod(n, d)
    c = [Mc(q, r, n) if r else None,              # 7/4 = 1 3/7: used the numerator as the denominator
         Mc(q + 1, r, d) if r else None,          # one whole too many
         Mc(q, d - r, d) if r and d - r != r else None,   # wrote the parts needed to make the next whole
         Mc(q - 1, r, d) if r and q > 1 else None,
         Mc(r, q, d) if r and q < d and r else None,      # swapped the whole number and the numerator
         Fc(d, n)]                                 # turned the fraction upside down
    return c


def mix_e(w, n, d):
    return ("Each whole is %s, so %d whole%s %d × %d = %d %s. Add the %s more: %d + %d = %d. "
            "The denominator stays %d. So %s = <b>%s</b>."
            % (fr(d, d), w, " is" if w == 1 else "s are", w, d, w * d, WORD[d], parts(n, d), w * d, n, w * d + n,
               d, mx(w, n, d), fr(w * d + n, d)))


def mix_cands(w, n, d):
    return [Fc(w * d, d),            # 2 1/3 = 6/3: forgot to add the numerator
            Fc(w * n + d, d),        # multiplied the whole number by the numerator, then added the denominator
            Fc(10 * w + n, d),       # wrote the digits side by side: 2 1/3 = 21/3
            Fc(w + n, d),            # added the whole number to the numerator
            Fc(w * d + n, w * d),
            Fc(w * d + n + 1, d)]


# ============================================================ set 1: improper fractions from models
def set_improper(rnd):
    SPOTS.left = []
    its = []
    for d, N in [(4, 7), (3, 5), (5, 8), (2, 5), (6, 11), (8, 13)]:
        nb = -(-N // d)
        r = N - (nb - 1) * d
        e = ("Each bar is 1 whole cut into %d equal parts, so each part is %s. Count the shaded parts: there are %d. "
             "So the bars show %d %s = <b>%s</b>. The denominator is %d (the parts in 1 whole), not %d (the parts in all the bars)."
             % (d, fr(1, d), N, N, WORD[d], fr(N, d), d, nb * d))
        its.append(mcq(fig(wholes_svg(d, N)) + "Each bar is 1 whole. What improper fraction is shaded?",
                       Fc(N, d), [Fc(N, nb * d), Fc(d, N), Fc(r, d), Fc(N + 1, d)], e, rnd))
    for d, N in [(4, 9), (3, 7), (6, 13), (5, 12)]:
        nb = -(-N // d)
        r = N - (nb - 1) * d
        e = ("Each circle is 1 whole cut into %d equal parts. %d parts are shaded, so it shows %d %s = <b>%s</b>. "
             "Do not use %d (all the parts in the %d circles) as the denominator."
             % (d, N, N, WORD[d], fr(N, d), nb * d, nb))
        its.append(mcq(fig(circles_svg(d, N)) + "Each circle is 1 whole. What improper fraction is shaded?",
                       Fc(N, d), [Fc(N, nb * d), Fc(d, N), Fc(nb * d - N, d), Fc(r, d)], e, rnd))
    for w, d in [(3, 5), (2, 6), (4, 8)]:
        e = ("1 whole = %d %s. So %d wholes = %d × %d = <b>%d</b> %s."
             % (d, WORD[d], w, w, d, w * d, WORD[d]))
        its.append(mcq("How many %s are there in %d wholes?" % (WORD[d], w), Nc(w * d),
                       [Nc(w + d), Nc(d), Nc(w), Nc(w * d - d)], e, rnd))
    for d, N in [(4, 11), (2, 9)]:
        q, r = divmod(N, d)
        e = ("Each bar holds %d %s. %d %s fill %d bars (%d × %d = %d) and %d more %s left over, so you need 1 more bar. "
             "%d + 1 = <b>%d</b> bars." % (d, WORD[d], N, WORD[d], q, q, d, q * d, r, "is" if r == 1 else "are", q, q + 1))
        its.append(mcq("You want to shade %s using bars that are each cut into %d equal parts. "
                       "How many bars do you need?" % (fr(N, d), d), Nc(q + 1), [Nc(N), Nc(d), Nc(q), Nc(N - d)], e, rnd))
    its.append(mcq("Which of these is an improper fraction?", Fc(7, 5), [Fc(5, 7), Mc(1, 2, 7), Fc(3, 4)],
                   "In an improper fraction, the numerator is equal to or greater than the denominator. "
                   "In %s, 7 is greater than 5, so <b>%s</b> is improper. %s and %s are proper fractions, and 1 %s is a mixed number."
                   % (fr(7, 5), fr(7, 5), fr(5, 7), fr(3, 4), fr(2, 7)), rnd))
    its.append(mcq("Which of these is a proper fraction?", Fc(8, 9), [Fc(9, 8), Mc(1, 1, 9), Fc(10, 10)],
                   "In a proper fraction, the numerator is smaller than the denominator. 8 is smaller than 9, so <b>%s</b> is proper. "
                   "%s and %s are improper fractions, and 1 %s is a mixed number." % (fr(8, 9), fr(9, 8), fr(10, 10), fr(1, 9)), rnd))
    its.append(mcq("Which of these is a mixed number?", Mc(3, 1, 2), [Fc(5, 2), Fc(1, 3), Nc(4)],
                   "A mixed number has a whole number and a proper fraction together. <b>3 %s</b> has 3 wholes and %s. "
                   "%s is an improper fraction, %s is a proper fraction and 4 is a whole number." % (fr(1, 2), fr(1, 2), fr(5, 2), fr(1, 3)), rnd))
    its.append(mcq("Only one of these is an improper fraction. Which one is it?", Fc(6, 6), [Fc(5, 6), Mc(1, 1, 6), Fc(6, 7)],
                   "The numerator can also be <b>equal</b> to the denominator. %s = 1 whole, and it is an improper fraction. "
                   "So the answer is <b>%s</b>. %s and %s are proper fractions." % (fr(6, 6), fr(6, 6), fr(5, 6), fr(6, 7)), rnd))
    its.append(mcq("In the fraction %s, what does the 4 tell you?" % fr(7, 4),
                   "Each whole is cut into 4 equal parts",
                   ["There are 4 wholes", "4 parts are shaded", "There are 4 parts in all"],
                   "The denominator tells you how many equal parts make <b>1 whole</b>. In %s, each whole is cut into 4 equal parts "
                   "(quarters), and the numerator 7 tells you there are 7 quarters." % fr(7, 4), rnd))
    assert len(its) == 20, len(its)
    return {"title": "Improper fractions from models", "items": its}


# ============================================================ set 2: mixed numbers from models and number lines
def nl_item(t, L, d, cands, rnd, as_imp):
    pos = SPOTS.next(rnd)
    lo = sorted([c for c in cands if c < t], reverse=True)
    hi = sorted([c for c in cands if c > t])
    pts = sorted(lo[:pos] + [t] + hi[:3 - pos])
    assert len(pts) == 4 and len(set(pts)) == 4, (t, pts)
    for v in pts:
        assert (v * d).denominator == 1 and 0 < v < L
    letter = "ABCD"[pts.index(t)]
    w = int(t)
    r = int((t - w) * d)
    name = fr((t * d).numerator, d) if as_imp else mx(w, r, d)
    e = "Each whole is split into %d equal parts, so each mark is %s. " % (d, fr(1, d))
    if as_imp:
        e += "%s = %s. " % (fr((t * d).numerator, d), mx(w, r, d))
    e += ("Go to %d, then %d more mark%s. That is letter <b>%s</b>." % (w, r, "" if r == 1 else "s", letter))
    q = fig(letters_line_svg(L, d, pts)) + "Which letter shows %s?" % name
    return {"q": q, "c": ["A", "B", "C", "D"], "a": pts.index(t), "e": e}


def set_mixed(rnd):
    SPOTS.left = []
    its = []
    for d, N in [(3, 7), (4, 11), (5, 13), (6, 13), (8, 19)]:
        nb = -(-N // d)
        q, r = divmod(N, d)
        e = ("Each bar is 1 whole. %d bar%s full, so that is %d whole%s. The last bar has %d of %d parts shaded: %s. "
             "So the shaded part is <b>%s</b>." % (q, " is" if q == 1 else "s are", q, "" if q == 1 else "s", r, d, fr(r, d), mx(q, r, d)))
        its.append(mcq(fig(wholes_svg(d, N)) + "Each bar is 1 whole. Write the shaded part as a mixed number.",
                       Mc(q, r, d), [Mc(q + 1, r, d), Mc(q, d - r, d) if d - r != r else None, Fc(r, d), Mc(q, r, nb * d)], e, rnd))
    for d, N in [(3, 8), (4, 7), (6, 17)]:
        q, r = divmod(N, d)
        e = ("%d circle%s fully shaded: %d whole%s. The last circle has %s shaded. So the picture shows <b>%s</b>."
             % (q, " is" if q == 1 else "s are", q, "" if q == 1 else "s", fr(r, d), mx(q, r, d)))
        its.append(mcq(fig(circles_svg(d, N)) + "Each circle is 1 whole. Write the shaded part as a mixed number.",
                       Mc(q, r, d), [Mc(q + 1, r, d), Mc(q, d - r, d) if d - r != r else None, Fc(r, d), Mc(r, q, d) if q < d else None],
                       e, rnd))
    for t, L, d in [(F(5, 3), 3, 3), (F(9, 4), 3, 4), (F(8, 5), 2, 5), (F(7, 2), 4, 2), (F(17, 6), 3, 6), (F(5, 4), 2, 4)]:
        w = int(t)
        r = int((t - w) * d)
        e = ("Each whole is split into %d equal parts, so each mark is %s. The arrow is %d mark%s after %d. "
             "So it shows <b>%s</b>." % (d, fr(1, d), r, "" if r == 1 else "s", w, mx(w, r, d)))
        cands = [Mc(w, r, d * L),                              # counted all the marks on the line as the denominator
                 Mc(w + 1, r, d),
                 Mc(w, d - r, d) if d - r != r else None,
                 Mc(w, r + 1, d) if r + 1 < d else None,       # counted the whole-number mark as well
                 Fc(r, d), Mc(w - 1, r, d) if w > 1 else None, Mc(w + 1, 0, d)]
        its.append(mcq(fig(arrow_line_svg(L, d, t)) + "What number does the arrow show? Give a mixed number.",
                       Mc(w, r, d), cands, e, rnd))
    for t, L, d, as_imp in [(F(7, 3), 4, 3, False), (F(13, 5), 4, 5, False), (F(7, 4), 3, 4, True), (F(11, 6), 3, 6, True)]:
        cands = [t - 1, t + 1, t + F(1, d), t - F(1, d), t + F(2, d), t - F(2, d), t - F(3, d)]
        cands = sorted(set(c for c in cands if 0 < c < L))
        its.append(nl_item(t, L, d, cands, rnd, as_imp))
    its.append(mcq("2 %s lies between which two whole numbers?" % fr(3, 5), "2 and 3", ["3 and 4", "1 and 2", "3 and 5"],
                   "2 %s is 2 wholes and a bit more. It is more than 2 but less than 3, so it lies between <b>2 and 3</b>." % fr(3, 5), rnd))
    assert 3 < F(17, 5) < 4
    its.append(mcq("%s lies between which two whole numbers?" % fr(17, 5), "3 and 4", ["17 and 18", "5 and 6", "2 and 3"],
                   "%s = 3 %s (17 ÷ 5 = 3 remainder 2). That is more than 3 but less than 4, so it lies between <b>3 and 4</b>."
                   % (fr(17, 5), fr(2, 5)), rnd))
    assert len(its) == 20, len(its)
    return {"title": "Mixed numbers from models and number lines", "items": its}


# ============================================================ set 3: converting
def set_convert(rnd):
    SPOTS.left = []
    its = []
    for n, d in [(7, 4), (11, 3), (13, 5), (17, 6), (12, 4), (19, 8), (23, 10), (25, 7), (31, 9)]:
        q, r = divmod(n, d)
        if r == 0:
            its.append(mcq("Write %s as a whole number." % fr(n, d), Nc(q), [Nc(n - d), Fc(d, n), Nc(n * d), Nc(n + d)],
                           imp_e(n, d), rnd))
            continue
        its.append(mcq("Write %s as a mixed number." % fr(n, d), Mc(q, r, d), imp_cands(n, d), imp_e(n, d), rnd))
    for w, n, d in [(2, 1, 3), (1, 3, 4), (3, 2, 5), (2, 5, 6), (4, 1, 2), (1, 7, 8), (3, 3, 10), (5, 2, 3), (2, 4, 9)]:
        its.append(mcq("Write %s as an improper fraction." % mx(w, n, d), Fc(w * d + n, d), mix_cands(w, n, d),
                       mix_e(w, n, d), rnd))
    assert F(7, 4) == 1 + F(3, 4)
    its.append(mcq("Wei Ming wrote %s = 1 %s. What mistake did he make?" % (fr(7, 4), fr(3, 7)),
                   "He used 7 as the denominator instead of 4",
                   ["He found the wrong whole number", "He forgot the whole number", "There is no mistake"],
                   "7 ÷ 4 = 1 remainder 3, so the whole number 1 and the 3 left over are right. But the parts are still quarters, "
                   "so the denominator must stay 4: %s = <b>1 %s</b>." % (fr(7, 4), fr(3, 4)), rnd))
    assert 2 + F(1, 3) == F(7, 3)
    its.append(mcq("Mei Ling wrote 2 %s = %s. What mistake did she make?" % (fr(1, 3), fr(6, 3)),
                   "She forgot to add the 1 third",
                   ["She should multiply 2 by 1", "She should add 2 and 3", "There is no mistake"],
                   "2 wholes = 2 × 3 = 6 thirds, which is right. Then she must add the 1 more third: 6 + 1 = 7. "
                   "So 2 %s = <b>%s</b>. %s is only 2 wholes." % (fr(1, 3), fr(7, 3), fr(6, 3)), rnd))
    assert len(its) == 20, len(its)
    return {"title": "Convert between improper fractions and mixed numbers", "items": its}


# ============================================================ set 4: compare and order
def cmp_steps(xs):
    """Explain by writing every number as a mixed number with a common denominator."""
    L = 1
    for x in xs:
        L = L * nden(x) // math.gcd(L, nden(x))
    out = []
    for x in xs:
        v = nval(x)
        w, r = divmod((v * L).numerator, L)
        same = mx(w, r, L)
        if x[0] == "i":
            out.append("%s = %s" % (nshow(x), same))
        elif nden(x) != L:
            out.append("%s = %s" % (nshow(x), same))
        else:
            out.append(nshow(x))
    return "Write them as mixed numbers%s: %s. " % ("" if all(nden(x) == L for x in xs) else " in %s" % WORD[L], ", ".join(out))


def set_compare(rnd):
    SPOTS.left = []
    its = []
    for a, b in [(I(11, 4), M(2, 1, 4)), (M(2, 2, 3), I(7, 3)), (I(17, 5), M(3, 3, 5)), (M(2, 5, 8), I(19, 8)),
                 (I(13, 10), M(1, 1, 10)), (M(4, 1, 2), I(7, 2)), (I(23, 6), M(3, 1, 6)), (M(1, 4, 9), I(16, 9)),
                 (M(2, 1, 2), I(9, 4)), (I(11, 6), M(1, 2, 3))]:
        va, vb = nval(a), nval(b)
        assert va != vb
        big = a if va > vb else b
        e = cmp_steps([a, b])
        e += "So <b>%s</b> is greater." % nshow(big)
        if big[0] == "m":
            e += " A big numerator does not always mean a big number."
        its.append(mcq("Which is greater: %s or %s?" % (nshow(a), nshow(b)), nshow(big),
                       [nshow(b if big == a else a), "They are equal", CANT], e, rnd))
    for word, xs in [("greatest", [I(13, 5), M(2, 1, 5), I(9, 5), M(3, 1, 5)]),
                     ("smallest", [I(11, 3), M(2, 2, 3), I(7, 3), M(3, 1, 3)]),
                     ("greatest", [M(1, 7, 8), I(19, 8), I(13, 8), M(2, 1, 8)]),
                     ("smallest", [I(9, 4), M(1, 3, 4), I(11, 4), M(2, 1, 2)])]:
        assert len(set(nval(x) for x in xs)) == 4
        best = max(xs, key=nval) if word == "greatest" else min(xs, key=nval)
        e = cmp_steps(xs) + "The %s is <b>%s</b>." % (word, nshow(best))
        its.append(mcq("Which number is the %s?<br>%s" % (word, ", ".join(nshow(x) for x in xs)), (nshow(best), nval(best)),
                       [(nshow(x), nval(x)) for x in xs if x != best], e, rnd))

    def s_of(seq):
        return ", ".join(nshow(x) for x in seq)
    for xs, up in [([I(7, 4), M(1, 1, 4), I(9, 4)], True), ([M(2, 1, 3), I(8, 3), I(5, 3)], True),
                   ([I(13, 6), M(2, 5, 6), M(1, 5, 6)], False), ([M(3, 1, 2), I(13, 4), I(15, 4)], True)]:
        right = sorted(xs, key=nval, reverse=not up)
        top = lambda x: x[1]       # the first number a child sees: the numerator or the whole number
        perms = [sorted(xs, key=top, reverse=not up), list(reversed(right))]
        perms += [list(p) for p in itertools.permutations(xs)]
        e = cmp_steps(xs) + "So the order is <b>%s</b>." % s_of(right)
        its.append(mcq("Order from %s:<br>%s" % ("smallest to greatest" if up else "greatest to smallest", s_of(xs)),
                       s_of(right), [s_of(p) for p in perms], e, rnd))
    assert 2 < F(11, 4) < 3 and not 2 < F(13, 4) < 3 and not 2 < F(7, 4) < 3 and not 2 < F(3, 2) < 3
    its.append(mcq("Which number is between 2 and 3?", Fc(11, 4), [Fc(7, 4), Fc(13, 4), Fc(3, 2)],
                   "2 = %s and 3 = %s. <b>%s</b> = 2 %s, which is between them. %s = 1 %s and %s = 1 %s are less than 2; %s = 3 %s is more than 3."
                   % (fr(8, 4), fr(12, 4), fr(11, 4), fr(3, 4), fr(7, 4), fr(3, 4), fr(3, 2), fr(1, 2), fr(13, 4), fr(1, 4)), rnd))
    assert F(10, 3) > 3 and F(9, 3) == 3
    its.append(mcq("Which number is greater than 3?", Fc(10, 3), [Fc(8, 3), Fc(9, 3), Fc(5, 3)],
                   "3 wholes = %s. Only <b>%s</b> (= 3 %s) is more than %s. %s is equal to 3, not greater than 3."
                   % (fr(9, 3), fr(10, 3), fr(1, 3), fr(9, 3), fr(9, 3)), rnd))
    assert len(its) == 20, len(its)
    return {"title": "Compare and order mixed numbers and improper fractions", "items": its}


# ============================================================ set 5: word problems
L_ = " ℓ"
M_ = " m"
KG = " kg"
KM = " km"
H_ = " h"


def set_words(rnd):
    SPOTS.left = []
    its = []
    # 1 cups of bandung
    assert F(11, 4) == 2 + F(3, 4)
    its.append(mcq(fig(units_svg(11, "?", L_, [(0, 1, (0, 1, 4))], shade=11)) +
                   "Each cup holds %s ℓ of bandung. Priya filled 11 cups. How many litres of bandung did she pour? "
                   "Give your answer as a mixed number." % fr(1, 4),
                   Mc(2, 3, 4, L_), [Mc(3, 3, 4, L_), Mc(2, 1, 4, L_), Fc(4, 11, L_), Nc(11, L_)],
                   "Model: 1 unit = %s ℓ, so 11 units = 11 quarters = %s ℓ. 11 ÷ 4 = 2 remainder 3, so %s = <b>2 %s ℓ</b>."
                   % (fr(1, 4), fr(11, 4), fr(11, 4), fr(3, 4)), rnd))
    # 2 sugar packets
    assert 7 * F(1, 2) == 3 + F(1, 2)
    its.append(mcq("Mrs Lim bought 7 packets of sugar. Each packet has a mass of %s kg. What is the total mass of the sugar? "
                   "Give your answer as a mixed number." % fr(1, 2),
                   Mc(3, 1, 2, KG), [Nc(7, KG), Nc(14, KG), Fc(2, 7, KG), Mc(4, 1, 2, KG)],
                   "7 packets of %s kg = 7 halves = %s kg. 7 ÷ 2 = 3 remainder 1, so the total is <b>3 %s kg</b>."
                   % (fr(1, 2), fr(7, 2), fr(1, 2)), rnd))
    # 3 kueh lapis
    assert F(17, 6) == 2 + F(5, 6)
    its.append(mcq("Mdm Wong cut each kueh lapis into 6 equal slices. She sold 17 slices. How many kueh lapis did she sell? "
                   "Give your answer as a mixed number.",
                   Mc(2, 5, 6), [Mc(3, 5, 6), Mc(2, 1, 6), Mc(2, 5, 17), Fc(6, 17)],
                   "Each slice is %s of a kueh lapis, so 17 slices = %s. 17 ÷ 6 = 2 remainder 5. "
                   "She sold <b>2 %s</b> kueh lapis. The denominator stays 6, not 17." % (fr(1, 6), fr(17, 6), fr(5, 6)), rnd))
    # 4 watermelons
    assert F(15, 4) == 3 + F(3, 4)
    its.append(mcq(fig(circles_svg(4, 15)) +
                   "Mr Tan cut some watermelons into 4 equal slices each. His class ate 15 slices (shaded). "
                   "How many watermelons did the class eat? Give your answer as a mixed number.",
                   Mc(3, 3, 4), [Mc(4, 3, 4), Mc(3, 1, 4), Fc(4, 15), Mc(4, 0, 4)],
                   "15 slices = %s of a watermelon. 15 ÷ 4 = 3 remainder 3, so the class ate <b>3 %s</b> watermelons."
                   % (fr(15, 4), fr(3, 4)), rnd))
    # 5 laps
    assert 8 * F(1, 3) == 2 + F(2, 3)
    its.append(mcq("One round of the school field is %s km. Zhi Hao ran 8 rounds on Sports Day. How far did he run? "
                   "Give your answer as a mixed number." % fr(1, 3),
                   Mc(2, 2, 3, KM), [Mc(2, 1, 3, KM), Mc(3, 2, 3, KM), Fc(3, 8, KM), Nc(8, KM)],
                   "8 rounds of %s km = 8 thirds = %s km. 8 ÷ 3 = 2 remainder 2, so he ran <b>2 %s km</b>."
                   % (fr(1, 3), fr(8, 3), fr(2, 3)), rnd))
    # 6 milk in a week
    assert 7 * F(1, 3) == 2 + F(1, 3)
    its.append(mcq("Ryan drinks %s ℓ of milk every day. How much milk does he drink in 1 week? "
                   "Give your answer as a mixed number." % fr(1, 3),
                   Mc(2, 1, 3, L_), [Nc(7, L_), Mc(3, 1, 3, L_), Mc(2, 1, 7, L_), Fc(3, 7, L_)],
                   "1 week = 7 days. 7 × %s ℓ = 7 thirds = %s ℓ. 7 ÷ 3 = 2 remainder 1, so he drinks <b>2 %s ℓ</b>."
                   % (fr(1, 3), fr(7, 3), fr(1, 3)), rnd))
    # 7 reading time
    assert 5 * F(1, 2) == 2 + F(1, 2)
    its.append(mcq("Devi reads a storybook for %s h every day. How many hours does she read in 5 days? "
                   "Give your answer as a mixed number." % fr(1, 2),
                   Mc(2, 1, 2, H_), [Nc(5, H_), Mc(5, 1, 2, H_), Fc(2, 5, H_), Nc(10, H_)],
                   "5 × %s h = 5 halves = %s h. 5 ÷ 2 = 2 remainder 1, so she reads <b>2 %s h</b> (2 h 30 min)."
                   % (fr(1, 2), fr(5, 2), fr(1, 2)), rnd))
    # 8 ribbon pieces
    assert (3 + F(2, 5)) / F(1, 5) == 17
    its.append(mcq(fig(units_svg(17, (3, 2, 5), M_, [(0, 1, (0, 1, 5))], shade=1, only_first=True)) +
                   "Siti has a ribbon 3 %s m long. She cuts it into pieces. Each piece is %s m long. How many pieces does she get?"
                   % (fr(2, 5), fr(1, 5)),
                   Nc(17), [Nc(15), Nc(13), Nc(5), Nc(32)],
                   "Change 3 %s m to fifths: 3 wholes = 3 × 5 = 15 fifths, and 15 + 2 = 17 fifths. So 3 %s = %s. "
                   "Each piece is 1 fifth, so she gets <b>17</b> pieces." % (fr(2, 5), fr(2, 5), fr(17, 5)), rnd))
    # 9 rambutan bags
    assert (3 + F(1, 2)) / F(1, 2) == 7
    its.append(mcq("Mr Rahman bought 3 %s kg of rambutans. He packed them into bags of %s kg each. How many bags did he fill?"
                   % (fr(1, 2), fr(1, 2)),
                   Nc(7), [Nc(6), Nc(5), Nc(4)],
                   "3 %s = %s (3 × 2 = 6 halves, and 6 + 1 = 7 halves). Each bag holds 1 half, so he filled <b>7</b> bags."
                   % (fr(1, 2), fr(7, 2)), rnd))
    # 10 paint tins
    assert (2 + F(3, 4)) / F(1, 4) == 11
    its.append(mcq("Mr Kumar has 2 %s ℓ of paint. He pours it into small tins. Each tin holds %s ℓ. How many tins can he fill?"
                   % (fr(3, 4), fr(1, 4)),
                   Nc(11), [Nc(8), Nc(9), Nc(6)],
                   "2 %s = %s (2 × 4 = 8 quarters, and 8 + 3 = 11 quarters). Each tin holds 1 quarter, so he can fill <b>11</b> tins."
                   % (fr(3, 4), fr(11, 4)), rnd))
    # 11 time in h and min
    assert F(7, 4) * 60 == 105
    its.append(mcq("Ali spent %s h on his Science project. How long is that in hours and minutes?" % fr(7, 4),
                   "1 h 45 min", ["1 h 34 min", "7 h 4 min", "1 h 3 min"],
                   "%s = 1 %s. %s h = 3 × 15 min = 45 min (because %s h = 15 min). So it is <b>1 h 45 min</b>."
                   % (fr(7, 4), fr(3, 4), fr(3, 4), fr(1, 4)), rnd))
    # 12 who walked further
    assert F(9, 4) < 2 + F(1, 2)
    its.append(mcq("Jun Jie walked %s km at Gardens by the Bay. Chloe walked 2 %s km. Who walked further?" % (fr(9, 4), fr(1, 2)),
                   "Chloe", ["Jun Jie", "They walked the same distance", CANT],
                   "%s = 2 %s. 2 %s = 2 %s. 2 %s is more than 2 %s, so <b>Chloe</b> walked further."
                   % (fr(9, 4), fr(1, 4), fr(1, 2), fr(2, 4), fr(2, 4), fr(1, 4)), rnd))
    # 13 which jug
    assert F(13, 4) < 3 + F(1, 2)
    its.append(mcq("Jug A has %s ℓ of water. Jug B has 3 %s ℓ of water. Which jug has more water?" % (fr(13, 4), fr(1, 2)),
                   "Jug B", ["Jug A", "They have the same amount", CANT],
                   "%s = 3 %s (13 ÷ 4 = 3 remainder 1). 3 %s = 3 %s. 3 %s is more than 3 %s, so <b>Jug B</b> has more water. "
                   "The bigger numerator 13 does not make Jug A bigger." % (fr(13, 4), fr(1, 4), fr(1, 2), fr(2, 4), fr(2, 4), fr(1, 4)), rnd))
    # 14 cycling
    assert F(11, 3) > 3 + F(1, 3)
    its.append(mcq("Nurul cycled %s km at East Coast Park. Mei Ling cycled 3 %s km. Who cycled further?" % (fr(11, 3), fr(1, 3)),
                   "Nurul", ["Mei Ling", "They cycled the same distance", CANT],
                   "%s = 3 %s (11 ÷ 3 = 3 remainder 2). 3 %s is more than 3 %s, so <b>Nurul</b> cycled further."
                   % (fr(11, 3), fr(2, 3), fr(2, 3), fr(1, 3)), rnd))
    # 15 longest ribbon
    vals = {"Red": 2 + F(1, 4), "Blue": F(7, 4), "Green": F(5, 2)}
    assert max(vals, key=vals.get) == "Green"
    its.append(mcq("Hui Min has three ribbons. The red ribbon is 2 %s m, the blue ribbon is %s m and the green ribbon is %s m long. "
                   "Which ribbon is the longest?" % (fr(1, 4), fr(7, 4), fr(5, 2)),
                   "Green", ["Red", "Blue", "They are all the same length"],
                   "Use quarters: 2 %s = %s, %s, and %s = %s. The greatest is %s, so the <b>green</b> ribbon is the longest."
                   % (fr(1, 4), fr(9, 4), fr(7, 4), fr(5, 2), fr(10, 4), fr(10, 4)), rnd))
    # 16 compare model
    r = 2 + F(3, 5) - F(12, 5)
    assert r == F(1, 5)
    its.append(mcq(fig(compare_svg([("Raju", 2 + F(3, 5), (2, 3, 5)), ("Kavya", F(12, 5), (0, 12, 5))], "?", M_)) +
                   "Raju's ribbon is 2 %s m long. Kavya's ribbon is %s m long. How much longer is Raju's ribbon?"
                   % (fr(3, 5), fr(12, 5)),
                   Fc(1, 5, M_), [Fc(3, 5, M_), Fc(9, 5, M_), Nc(1, M_)],
                   "Change 2 %s to fifths: 2 × 5 + 3 = 13, so 2 %s = %s. %s − %s = <b>%s m</b>. "
                   "(13 − 12 = 1, and the parts are still fifths.)" % (fr(3, 5), fr(3, 5), fr(13, 5), fr(13, 5), fr(12, 5), fr(1, 5)), rnd))
    # 17 flour needed
    r = 3 - F(9, 4)
    assert r == F(3, 4)
    its.append(mcq(fig(model_svg([(F(9, 4), (0, 9, 4)), (r, "?")], (3, 0, 1), KG)) +
                   "Farah needs 3 kg of flour to bake pineapple tarts for Chinese New Year. She has %s kg of flour. "
                   "How much more flour does she need?" % fr(9, 4),
                   Fc(3, 4, KG), [Mc(1, 1, 2, KG), Mc(5, 1, 4, KG), Fc(1, 4, KG)],
                   "3 kg = %s kg. %s − %s = <b>%s kg</b>. Check: %s = 2 %s, and 2 %s + %s = 3."
                   % (fr(12, 4), fr(12, 4), fr(9, 4), fr(3, 4), fr(9, 4), fr(1, 4), fr(1, 4), fr(3, 4)), rnd))
    # 18 wire left
    r = 3 - 5 * F(1, 4)
    assert r == 1 + F(3, 4)
    its.append(mcq(fig(units_svg(12, (3, 0, 1), M_, [(0, 1, (0, 1, 4)), (5, 12, "?")], shade=5)) +
                   "Mrs Ng had 3 m of wire. She cut off 5 pieces. Each piece was %s m long. How much wire was left? "
                   "Give your answer as a mixed number." % fr(1, 4),
                   Mc(1, 3, 4, M_), [Mc(1, 1, 4, M_), Mc(2, 1, 4, M_), Mc(4, 1, 4, M_)],
                   "Model: 3 m = 12 quarters, so the bar has 12 units of %s m. She cut off 5 units. 12 − 5 = 7 units are left: "
                   "%s m = <b>1 %s m</b>." % (fr(1, 4), fr(7, 4), fr(3, 4)), rnd))
    # 19 rice left
    r = 4 + F(1, 4) - F(9, 4)
    assert r == 2
    its.append(mcq("A hawker had 4 %s kg of rice. She cooked %s kg of it for chicken rice in the morning. How much rice was left?"
                   % (fr(1, 4), fr(9, 4)),
                   Nc(2, KG), [Mc(6, 1, 2, KG), Mc(2, 1, 4, KG), Mc(1, 3, 4, KG)],
                   "Change %s to a mixed number: %s = 2 %s. Then 4 %s − 2 %s: the fractions are the same, so only the wholes are left: 4 − 2 = 2. "
                   "So <b>2 kg</b> of rice was left." % (fr(9, 4), fr(9, 4), fr(1, 4), fr(1, 4), fr(1, 4)), rnd))
    # 20 cakes left
    r = 3 - F(19, 8)
    assert r == F(5, 8)
    its.append(mcq(fig(wholes_svg(8, 19)) +
                   "At a class party, there were 3 kaya cakes. Each cake was cut into 8 equal slices. The children ate 19 slices "
                   "(shaded). How much cake was left?",
                   Fc(5, 8), [Mc(2, 3, 8), Fc(5, 24), Mc(1, 5, 8)],
                   "3 cakes = 3 × 8 = 24 slices. 24 − 19 = 5 slices left. Each slice is %s of a cake, so <b>%s</b> of a cake was left. "
                   "(The children ate %s = 2 %s cakes.)" % (fr(1, 8), fr(5, 8), fr(19, 8), fr(3, 8)), rnd))
    assert len(its) == 20, len(its)
    return {"title": "Word problems with bar models", "items": its}


# ============================================================ lesson
def body_html():
    f_bars = wholes_svg(4, 7)
    f_line = arrow_line_svg(3, 4, F(7, 4))
    f_pies = circles_svg(3, 7)
    f_model = units_svg(11, "?", L_, [(0, 1, (0, 1, 4))], shade=11)
    return (
        "<h2>Proper fractions, improper fractions and mixed numbers</h2>"
        "<p>A <b>proper fraction</b> is less than 1: the numerator is smaller than the denominator. "
        "An <b>improper fraction</b> is 1 or more: the numerator is equal to or greater than the denominator. "
        "A <b>mixed number</b> is a whole number and a proper fraction together.</p>" +
        table(["Proper fraction", "Improper fraction", "Mixed number"], [
            [fr(3, 4), fr(7, 4), "1 " + fr(3, 4)],
            [fr(2, 5), fr(5, 5) + " (= 1)", "2 " + fr(2, 5)],
        ]) +
        "<h2>Improper fractions from a model</h2>"
        "<p>The denominator tells you how many equal parts make <b>1 whole</b>. Count all the shaded parts for the numerator.</p>"
        "<figure class='sn-fig'>" + f_bars +
        "<figcaption>Each bar is 1 whole cut into quarters. 7 quarters are shaded: " + fr(7, 4) + ".</figcaption></figure>"
        "<p>The same picture shows 1 full bar and " + fr(3, 4) + " of another bar, so " + fr(7, 4) + " = 1 " + fr(3, 4) + ".</p>"
        "<figure class='sn-fig'>" + f_line +
        "<figcaption>On the number line, " + fr(7, 4) + " is 3 quarter marks after 1: it is 1 " + fr(3, 4) + ".</figcaption></figure>"
        "<h2>Improper fraction to mixed number: divide</h2>"
        "<p>Divide the numerator by the denominator. The answer is the whole number. The remainder is the new numerator. "
        "The denominator stays the same.</p>"
        + ex("Example", "Write " + fr(11, 4) + " as a mixed number.",
             "11 ÷ 4 = 2 remainder 3. That is 2 wholes and 3 quarters.", "2 " + fr(3, 4)) +
        "<h2>Mixed number to improper fraction: multiply and add</h2>"
        "<p>Change the wholes into parts, then add the parts of the fraction.</p>"
        "<figure class='sn-fig'>" + f_pies +
        "<figcaption>2 " + fr(1, 3) + ": 2 wholes = 6 thirds, plus 1 third = 7 thirds.</figcaption></figure>"
        + ex("Example", "Write 2 " + fr(1, 3) + " as an improper fraction.",
             "2 × 3 = 6 thirds. 6 + 1 = 7 thirds.", fr(7, 3)) +
        "<h2>Compare and order</h2>"
        "<p>Write the numbers in the same form first, for example all as mixed numbers. Compare the whole numbers, "
        "then the fractions.</p>"
        + ex("Example", "Which is greater: " + fr(11, 4) + " or 2 " + fr(1, 4) + "?",
             fr(11, 4) + " = 2 " + fr(3, 4) + ". Both have 2 wholes, and " + fr(3, 4) + " is more than " + fr(1, 4) + ".", fr(11, 4)) +
        "<h2>Word problems: draw a model</h2>"
        "<p>When the same small amount is repeated, draw a bar of equal units. Count the units to get an improper fraction, "
        "then change it to a mixed number.</p>"
        "<figure class='sn-fig'>" + f_model +
        "<figcaption>11 cups of " + fr(1, 4) + " ℓ: 11 units of " + fr(1, 4) + " ℓ = " + fr(11, 4) + " ℓ.</figcaption></figure>"
        + ex("Example", "Each cup holds " + fr(1, 4) + " ℓ of bandung. Priya filled 11 cups. How much bandung did she pour?",
             "11 units = 11 quarters = " + fr(11, 4) + " ℓ. 11 ÷ 4 = 2 remainder 3.", "2 " + fr(3, 4) + " ℓ") +
        "<h2>Common mistakes</h2>" +
        table(["Mistake", "What to do instead"], [
            [fr(7, 4) + " = 1 " + fr(3, 7) + " (using the numerator as the denominator)",
             "The parts are still quarters: " + fr(7, 4) + " = 1 " + fr(3, 4)],
            ["2 " + fr(1, 3) + " = " + fr(6, 3) + " (forgetting to add the numerator)",
             "2 × 3 = 6, then 6 + 1 = 7: " + fr(7, 3)],
            ["Writing " + fr(7, 8) + " for 7 quarters shaded in 2 bars (counting all the parts in both bars)",
             "The denominator is the number of parts in 1 whole: " + fr(7, 4)],
            ["Thinking " + fr(11, 4) + " is greater than 3 because 11 is a big number",
             "Change it: " + fr(11, 4) + " = 2 " + fr(3, 4) + ", which is less than 3"],
        ])
    )


FAQ = [
    {"q": "What is taught in P4 fractions?",
     "a": "In Primary 4, students learn mixed numbers and improper fractions and change one into the other. They also compare fractions, find a fraction of a set, and add and subtract fractions with denominators up to 12."},
    {"q": "How do I explain improper fractions to my child?",
     "a": "Use bars or paper circles. Shade 7 quarters across two bars: that is 7/4, and it is also 1 whole bar and 3/4 of another, so 7/4 = 1 3/4."},
    {"q": "What is the most common mistake with mixed numbers?",
     "a": "Changing the denominator, as in 7/4 = 1 3/7. The parts are still quarters, so 7/4 = 1 3/4. Another common slip is 2 1/3 = 6/3; the 1 third must be added, so 2 1/3 = 7/3."},
    {"q": "Is this in the MOE syllabus?",
     "a": "Yes. Mixed numbers, improper fractions and their relationship are part of Fractions in the MOE 2021 Primary 4 Standard Mathematics syllabus. Students use these skills again in Primary 5 when they add, subtract and multiply mixed numbers."},
]


def gen_unit():
    rnd = random.Random(64806)
    sets = [set_improper(rnd), set_mixed(rnd), set_convert(rnd), set_compare(rnd), set_words(rnd)]
    seen = set()
    for s in sets:
        assert len(s["items"]) == 20, (s["title"], len(s["items"]))
        assert sorted(it["a"] for it in s["items"]) == sorted([0, 1, 2, 3] * 5), s["title"]
        for it in s["items"]:
            assert len(set(it["c"])) == 4, it
            assert it["q"] not in seen, it["q"]
            seen.add(it["q"])
    return {
        "country": "sg", "subject": "maths", "grade": "primary-4", "slug": SLUG, "sort": 6,
        "updated": UPDATED, "pdf_url": "",
        "title": "Primary 4 Mixed Numbers and Improper Fractions",
        "seo_title": "P4 Mixed Numbers and Improper Fractions Worksheets: Free Primary 4 Maths with Answers (MOE Syllabus)",
        "short_title": "Mixed Numbers and Improper Fractions",
        "domain": "Number and Algebra",
        "standard_code": "Primary 4: Fractions",
        "standard_url": "https://www.moe.gov.sg/primary/curriculum/syllabus",
        "standard_text": "Mixed numbers, improper fractions and their relationship",
        "meta_desc": "Free P4 maths practice: improper fractions and mixed numbers with models and number lines, converting, comparing and word problems. 100 questions with answers.",
        "key_big": "The denominator tells you how many parts make 1 whole, and it stays the same when you change between improper fractions and mixed numbers.",
        "key_sub": "11/4: 11 ÷ 4 = 2 remainder 3, so 11/4 = 2 3/4. Back again: 2 × 4 + 3 = 11.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }


if __name__ == "__main__":
    u = gen_unit()
    mark_large(u, "(bars of|circles|number line|bar model)")
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(u, f, ensure_ascii=False, indent=1)
    print("wrote", path)
