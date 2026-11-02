# -*- coding: utf-8 -*-
"""
AU Year 4 Maths: Counting by fractions and mixed numerals (Australian Curriculum v9.0, AC9M4N04)
  python3 tools/gen_au_maths_y4_counting_fractions.py
Counting on and back by halves, thirds, quarters and fifths (1/4, 2/4, 3/4, 1, 1 1/4),
the next number in a fraction count, improper fractions and mixed numerals from pictures,
fractions and mixed numerals on number lines from 0 to 3, then word problems in Australian contexts.
Every choice carries its value; a wrong choice never equals the right value or another wrong one.
Every answer is checked in code with exact fractions.
HTML attributes use single quotes (no backslashes in the JSON). Australian English.
"""
import json, math, os, random, re
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "au", "maths", "year-4")
SLUG = "counting-by-fractions-and-mixed-numerals"
UPDATED = "2026-11-02"
FILL = "#4fae74"
BLUE = "#2f6db5"
LINE = "#2b2b2b"
CANT = "You can’t tell"
WORD = {2: "halves", 3: "thirds", 4: "quarters", 5: "fifths", 6: "sixths", 8: "eighths", 10: "tenths", 12: "twelfths"}
ONE = {2: "half", 3: "third", 4: "quarter", 5: "fifth", 6: "sixth", 8: "eighth", 10: "tenth", 12: "twelfth"}


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


def Nc(n, unit=""):
    return ("%d%s" % (n, unit), F(n))


def Dc(s, unit=""):
    return (s + unit, F(s))


def term(i, d, unit=""):
    """i steps of 1/d, written the way we count: 0, 1/4, 2/4, 3/4, 1, 1 1/4, 1 2/4 ..."""
    w, r = divmod(i, d)
    return Mc(w, r, d, unit)


def T(i, d):
    return term(i, d)[0]


def parts(n, d):
    return "%d %s" % (n, ONE[d] if n == 1 else WORD[d])


def lcm(a, b):
    return a * b // math.gcd(a, b)


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
def sfr(x, y, a, b, size=14, color=LINE):
    """Stacked fraction drawn in SVG, centred at x. y is the numerator baseline."""
    w = size * 0.62 * max(len(str(a)), len(str(b))) + 4
    return ("<text x='%.1f' y='%.1f' font-size='%d' font-weight='700' fill='%s' text-anchor='middle'>%s</text>"
            "<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='1.5'/>"
            "<text x='%.1f' y='%.1f' font-size='%d' font-weight='700' fill='%s' text-anchor='middle'>%s</text>"
            % (x, y, size, color, a, x - w / 2, y + 4, x + w / 2, y + 4, color, x, y + size + 4, size, color, b))


def bar_row(x0, y, W, H, n, k):
    s = []
    for i in range(n):
        s.append("<rect x='%.1f' y='%.1f' width='%.2f' height='%d' fill='%s' stroke='%s' stroke-width='2.5'/>"
                 % (x0 + i * W / n, y, W / n, H, FILL if i < k else "#fff", LINE))
    return "".join(s)


def wholes_svg(d, N, bw=96, H=40, gap=16):
    """N parts of 1/d shaded across bars of d parts (each bar is 1 whole), side by side."""
    nb = -(-N // d)
    s = []
    for b in range(nb):
        x0 = 6 + b * (bw + gap)
        k = min(d, N - b * d)
        s.append(bar_row(x0, 6, bw, H, d, k))
        s.append("<rect x='%.1f' y='6' width='%.1f' height='%d' fill='none' stroke='%s' stroke-width='3'/>" % (x0, bw, H, LINE))
    return svg_wrap(12 + nb * bw + (nb - 1) * gap, H + 12, "".join(s),
                    "bars of %d equal parts, %d bars, %d parts shaded" % (d, nb, N))


def circles_svg(d, N, R=34, gap=14):
    """N parts of 1/d shaded across circles of d equal parts (each circle is 1 whole)."""
    nc = -(-N // d)
    s = []
    for c in range(nc):
        cx = 6 + R + c * (2 * R + gap)
        cy = 6 + R
        k = min(d, N - c * d)
        for i in range(d):
            a0 = -math.pi / 2 + 2 * math.pi * i / d
            a1 = -math.pi / 2 + 2 * math.pi * (i + 1) / d
            s.append("<path d='M%.1f %.1f L%.2f %.2f A%d %d 0 0 1 %.2f %.2f Z' fill='%s' stroke='%s' stroke-width='2.5' "
                     "stroke-linejoin='round'/>"
                     % (cx, cy, cx + R * math.cos(a0), cy + R * math.sin(a0), R, R,
                        cx + R * math.cos(a1), cy + R * math.sin(a1), FILL if i < k else "#fff", LINE))
        s.append("<circle cx='%.1f' cy='%.1f' r='%d' fill='none' stroke='%s' stroke-width='3'/>" % (cx, cy, R, LINE))
    return svg_wrap(12 + nc * 2 * R + (nc - 1) * gap, 2 * R + 12, "".join(s),
                    "circles of %d equal parts, %d circles, %d parts shaded" % (d, nc, N))


def tick_line(L, d, Y, x0, x1, labels=False, hide=None):
    s = ["<line x1='%.1f' y1='%d' x2='%.1f' y2='%d' stroke='%s' stroke-width='2.5'/>" % (x0, Y, x1, Y, LINE)]
    n = L * d
    for i in range(n + 1):
        X = x0 + (x1 - x0) * i / n
        whole = (i % d == 0)
        s.append("<line x1='%.1f' y1='%d' x2='%.1f' y2='%d' stroke='%s' stroke-width='%s'/>"
                 % (X, Y - (11 if whole else 7), X, Y + (11 if whole else 7), LINE, "2.5" if whole else "1.6"))
        if hide is not None and i == hide:
            s.append("<text x='%.1f' y='%d' font-size='20' font-weight='700' fill='%s' text-anchor='middle'>?</text>"
                     % (X, Y + 38, BLUE))
        elif whole:
            s.append("<text x='%.1f' y='%d' font-size='16' font-weight='700' fill='%s' text-anchor='middle'>%d</text>"
                     % (X, Y + (38 if labels else 30), LINE, i // d))
        elif labels:
            w, r = divmod(i, d)
            if w == 0:
                s.append(sfr(X, Y + 30, r, d, 14))
            else:
                s.append("<text x='%.1f' y='%d' font-size='16' font-weight='700' fill='%s' text-anchor='middle'>%d</text>"
                         % (X - 6, Y + 38, LINE, w))
                s.append(sfr(X + 5, Y + 30, r, d, 14))
    return "".join(s)


def labelled_line_svg(L, d, hide=None, W=420):
    """Number line 0..L in steps of 1/d with every mark labelled (one label may be a blue ?)."""
    x0, x1 = 18, W - 18
    Y = 16
    lab = "number line from 0 to %d counting in %s with every mark labelled" % (L, WORD[d])
    if hide is not None:
        lab += " and one label missing"
    return svg_wrap(W, Y + 56, tick_line(L, d, Y, x0, x1, True, hide), lab)


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


# ------------------------------------------------------------ counting helpers
def on_cands(i, d):
    """Real mistakes when counting on to step i (from i-1)."""
    w, r = divmod(i, d)
    pw, pr = divmod(i - 1, d)
    c = []
    if pr > 0:
        c.append(Mc(pw, pr + 1, d + 1))      # 3/4 then 4/5
    if r == 0:
        c.append(term(i + 1, d))             # skipping the whole: 3/4 then 1 1/4
        c.append(Nc(i))                      # writing the count of parts as wholes: 4
    else:
        if w >= 1:
            c.append(Fc(r, d))               # forgot the whole
        c.append(Mc(w + 1, r, d))            # one whole too many
        c.append(term(i + 1, d))
    c += [term(i + 2, d), term(i - 2, d)]
    return c


def back_cands(i, d):
    """Real mistakes when counting back to step i (from i+1)."""
    w, r = divmod(i, d)
    pw, pr = divmod(i + 1, d)
    c = []
    if pr == 0:
        c.append(Mc(pw, d - 1, d))           # keeps the whole: 1 then 1 3/4
    if r > 0 and w >= 1:
        c.append(Fc(r, d))
    c += [term(i - 1, d), term(i + 2, d), term(i - 2, d), Mc(w, r, d + 1) if r else None]
    return c


def step_e(prev, i, d, back=False):
    s = ("Count %s by %s: each number is %s %s than the one before. %s %s %s = <b>%s</b>."
         % ("back" if back else "on", WORD[d], fr(1, d), "less" if back else "more",
            T(prev, d), "−" if back else "+", fr(1, d), T(i, d)))
    if not back and i % d == 0:
        s += " %s make 1 whole, so after %s comes %d. Do not skip %d." % (parts(d, d).capitalize(), T(prev, d), i // d, i // d)
    if back and (i + 1) % d == 0:
        s += " One %s less than %d is %s." % (ONE[d], (i + 1) // d, T(i, d))
    return s


def seq(idx, d, miss=None):
    return ", ".join("<b>?</b>" if k == miss else T(i, d) for k, i in enumerate(idx))


# ============================================================ set 1: count on
def set_count_on(rnd):
    SPOTS.left = []
    its = []
    # with a labelled number line
    for L, d, i in [(2, 4, 3), (2, 4, 4), (3, 2, 3), (2, 3, 4), (2, 5, 5), (2, 4, 6)]:
        q = fig(labelled_line_svg(L, d, i)) + "Count on by %s. Which number goes where the <b>?</b> is?" % WORD[d]
        its.append(mcq(q, term(i, d), on_cands(i, d), step_e(i - 1, i, d), rnd))
    # missing number in a count
    for d, start, miss in [(2, 1, 2), (3, 1, 2), (4, 2, 3), (5, 2, 2), (5, 4, 1), (4, 5, 2), (3, 3, 3), (2, 3, 1)]:
        idx = list(range(start, start + 4))
        i = idx[miss]
        q = "Count on by %s. What is the missing number?<br>%s" % (WORD[d], seq(idx, d, miss))
        its.append(mcq(q, term(i, d), on_cands(i, d), step_e(i - 1, i, d), rnd))
    # how many parts make a number
    for w, r, d in [(1, 0, 4), (2, 0, 3), (2, 1, 2), (1, 1, 5), (1, 3, 4), (2, 2, 3)]:
        n = w * d + r
        what = str(w) if r == 0 else mx(w, r, d)
        q = "Count by %s from 0. How many %s make %s%s?" % (WORD[d], WORD[d], what, " whole" if (w, r) == (1, 0) else "")
        c = [Nc(w + r), Nc(d + r), Nc(n - 1), Nc(n + 1), Nc(w * d), Nc(d)]
        if w == 1:
            e = "1 whole = %s = %d %s." % (fr(d, d), d, WORD[d])
        else:
            e = "1 whole = %s, so %d wholes = %d × %d = %d %s." % (fr(d, d), w, w, d, w * d, WORD[d])
        if r:
            e += " Add %s more: %d + %d = <b>%d</b>." % (parts(r, d), w * d, r, n)
        else:
            e = e.replace("= %d %s." % (w * d, WORD[d]), "= <b>%d</b> %s." % (w * d, WORD[d]))
        its.append(mcq(q, Nc(n), c, e, rnd))
    assert len(its) == 20, len(its)
    return {"title": "Count on by halves, thirds, quarters and fifths", "items": its}


# ============================================================ set 2: next number
def set_next(rnd):
    SPOTS.left = []
    its = []
    for d, idx in [(4, [5, 6, 7]), (3, [5, 6, 7]), (5, [7, 8, 9]), (2, [3, 4, 5]), (4, [9, 10, 11]), (5, [12, 13, 14])]:
        i = idx[-1] + 1
        q = "Count on by %s. What comes next?<br>%s, <b>?</b>" % (WORD[d], seq(idx, d))
        its.append(mcq(q, term(i, d), on_cands(i, d), step_e(i - 1, i, d), rnd))
    for d, idx in [(4, [6, 5, 4]), (3, [5, 4, 3]), (2, [6, 5, 4]), (5, [7, 6, 5]), (4, [10, 9, 8])]:
        i = idx[-1] - 1
        q = "Count back by %s. What comes next?<br>%s, <b>?</b>" % (WORD[d], seq(idx, d))
        its.append(mcq(q, term(i, d), back_cands(i, d), step_e(i + 1, i, d, True), rnd))

    def S(*ts):
        return ", ".join(mx(*t) for t in ts)

    rows = [
        ("on", 4, S((0, 2, 4), (0, 3, 4), (1, 0, 4), (1, 1, 4)),
         [S((0, 2, 4), (0, 3, 4), (0, 4, 5), (1, 0, 4)), S((0, 2, 4), (0, 3, 4), (1, 1, 4), (1, 2, 4)),
          S((0, 2, 4), (0, 3, 4), (1, 0, 4), (2, 0, 4))],
         "After %s comes %s = 1, then 1 %s. %s is not the next number, and 1 must not be skipped." % (fr(3, 4), fr(4, 4), fr(1, 4), fr(4, 5))),
        ("on", 3, S((1, 1, 3), (1, 2, 3), (2, 0, 3), (2, 1, 3)),
         [S((1, 1, 3), (1, 2, 3), (1, 3, 4), (2, 0, 3)), S((1, 1, 3), (1, 2, 3), (2, 1, 3), (2, 2, 3)),
          S((1, 1, 3), (1, 2, 3), (2, 0, 3), (3, 0, 3))],
         "After 1 %s comes 1 %s = 2, then 2 %s. Each step is only %s." % (fr(2, 3), fr(3, 3), fr(1, 3), fr(1, 3))),
        ("on", 5, S((0, 3, 5), (0, 4, 5), (1, 0, 5), (1, 1, 5)),
         [S((0, 3, 5), (0, 4, 5), (0, 5, 6), (1, 0, 5)), S((0, 3, 5), (0, 4, 5), (1, 1, 5), (1, 2, 5)),
          S((0, 3, 5), (0, 4, 5), (1, 0, 5), (2, 0, 5))],
         "After %s comes %s = 1, then 1 %s. The denominator stays 5." % (fr(4, 5), fr(5, 5), fr(1, 5))),
        ("back", 2, S((2, 1, 2), (2, 0, 2), (1, 1, 2), (1, 0, 2)),
         [S((2, 1, 2), (2, 0, 2), (1, 0, 2), (0, 1, 2)), S((2, 1, 2), (2, 0, 2), (1, 1, 2), (1, 1, 4)),
          S((2, 1, 2), (1, 1, 2), (1, 0, 2), (0, 1, 2))],
         "Take away %s each time: 2 %s, 2, 1 %s, 1. One half less than 2 is 1 %s, not 1." % (fr(1, 2), fr(1, 2), fr(1, 2), fr(1, 2))),
    ]
    for way, d, right, wrong, e in rows:
        its.append(mcq("Which shows counting %s by %s correctly?" % (way, WORD[d]), right, wrong,
                       "<b>%s</b>. %s" % (right, e), rnd))

    for i0, k, d in [(2, 4, 3), (5, 3, 4), (3, 4, 5)]:
        i = i0 + k
        t = F(i, d)
        q = "Start at %s. Count on %s. Where do you land?" % (T(i0, d), parts(k, d))
        c = [term(i - 1, d), term(i + 1, d), Mc(i0 // d + k, i0 % d, d), term(i + 2, d)]
        e = ("Count on %d step%s of %s: %s. You land on <b>%s</b>. Do not count the start number."
             % (k, "" if k == 1 else "s", fr(1, d), ", ".join(T(j, d) for j in range(i0 + 1, i + 1)), T(i, d)))
        assert F(i0, d) + F(k, d) == t
        its.append(mcq(q, term(i, d), c, e, rnd))

    its.append(mcq("Isla counts by fifths: %s, %s, %s. What is another way to write %s?" % (fr(3, 5), fr(4, 5), fr(5, 5), fr(5, 5)),
                   Nc(1), [Nc(5), Fc(1, 5), Fc(10, 5)],
                   "5 fifths make 1 whole, so %s = <b>1</b>." % fr(5, 5), rnd))
    assert F(2) + F(2, 4) == F(5, 2)
    its.append(mcq("Counting by quarters, Jack says 2 %s. Which number is the same as 2 %s?" % (fr(2, 4), fr(2, 4)),
                   Mc(2, 1, 2), [Mc(2, 1, 4), Fc(22, 4), Fc(2, 4)],
                   "%s is the same as %s, so 2 %s = <b>2 %s</b>." % (fr(2, 4), fr(1, 2), fr(2, 4), fr(1, 2)), rnd))
    assert len(its) == 20, len(its)
    return {"title": "What comes next in a fraction count?", "items": its}


# ============================================================ set 3: pictures
def imp_cands(n, d):
    q, r = divmod(n, d)
    return [Mc(q, r, n), Mc(q + 1, r, d), Mc(r, q, d) if q < d else None, Mc(q, d - r, d), Mc(q - 1, r, d), Fc(d, n)]


def mix_cands(w, n, d):
    return [Fc(w + n, d), Fc(w * n, d), Fc(10 * w + n, d), Fc(w * d, d + n), Fc(w * d + n + 1, d), Fc(w * d + n, w * d)]


def set_pictures(rnd):
    SPOTS.left = []
    its = []
    for shape, d, N in [("bar", 4, 7), ("bar", 3, 5), ("bar", 2, 5), ("bar", 5, 8), ("circle", 4, 9), ("circle", 3, 7)]:
        nb = -(-N // d)
        pic = wholes_svg(d, N) if shape == "bar" else circles_svg(d, N)
        q = fig(pic) + "Each %s is 1 whole. Which improper fraction is shaded?" % shape
        e = ("Each %s is cut into %d equal parts, so each part is %s. Count the shaded parts: %d. So it is <b>%s</b>. "
             "The denominator is the number of parts in <b>one</b> whole, not in all the %ss."
             % (shape, d, fr(1, d), N, fr(N, d), shape))
        its.append(mcq(q, Fc(N, d), [Fc(N, nb * d), Fc(nb * d - N, d) if nb * d - N > 1 else None, Fc(d, N),
                                     Fc(N - 1, d), Fc(N + 1, d)], e, rnd))
    for shape, d, N in [("bar", 4, 11), ("bar", 3, 8), ("bar", 5, 7), ("bar", 2, 7), ("circle", 4, 6), ("circle", 3, 10)]:
        q, r = divmod(N, d)
        pic = wholes_svg(d, N) if shape == "bar" else circles_svg(d, N)
        e = ("%d %s%s full, so that is %d whole%s. %s more %s shaded. So it is <b>%s</b> (= %s)."
             % (q, shape, "s are" if q > 1 else " is", q, "s" if q > 1 else "", parts(r, d).capitalize(),
                "is" if r == 1 else "are", mx(q, r, d), fr(N, d)))
        its.append(mcq(fig(pic) + "Each %s is 1 whole. Which mixed numeral is shaded?" % shape,
                       Mc(q, r, d), [Mc(q, r, N), Mc(q, r, (q + 1) * d), Mc(q + 1, r, d), Mc(q, d - r, d), Fc(r, d)], e, rnd))
    for w, r, d in [(2, 1, 3), (1, 3, 5), (1, 1, 4), (2, 1, 2)]:
        n = w * d + r
        q = fig(wholes_svg(d, n)) + "Each bar is 1 whole. The shaded part is %s. Which improper fraction is that?" % mx(w, r, d)
        e = ("Each whole is %s. %d whole%s = %d × %d = %d %s. Add %d more: %d + %d = %d. So %s = <b>%s</b>."
             % (fr(d, d), w, "" if w == 1 else "s", w, d, w * d, WORD[d], r, w * d, r, n, mx(w, r, d), fr(n, d)))
        its.append(mcq(q, Fc(n, d), mix_cands(w, r, d), e, rnd))
    for n, d in [(13, 4), (11, 3)]:
        q, r = divmod(n, d)
        e = ("How many %ss go into %d? %d × %d = %d, so there are %d wholes. %d − %d = %d left over. So %s = <b>%s</b>."
             % (d, n, q, d, q * d, q, n, q * d, r, fr(n, d), mx(q, r, d)))
        its.append(mcq("Write %s as a mixed numeral." % fr(n, d), Mc(q, r, d), imp_cands(n, d), e, rnd))
    for w, r, d in [(2, 4, 5), (3, 1, 2)]:
        n = w * d + r
        e = ("Each whole is %s, so %d wholes = %d × %d = %d %s. Add %d: %d + %d = %d. So %s = <b>%s</b>."
             % (fr(d, d), w, w, d, w * d, WORD[d], r, w * d, r, n, mx(w, r, d), fr(n, d)))
        its.append(mcq("Write %s as an improper fraction." % mx(w, r, d), Fc(n, d), mix_cands(w, r, d), e, rnd))
    assert len(its) == 20, len(its)
    return {"title": "Improper fractions and mixed numerals from pictures", "items": its}


# ============================================================ set 4: number lines
def arrow_item(t, L, d, mode, rnd):
    w = int(t)
    r = int((t - w) * d)
    n = int(t * d)
    assert (t * d).denominator == 1 and r > 0
    e = ("Each whole is split into %d equal parts, so each mark is %s. The arrow is %d mark%s after %d. "
         "So it shows %s = %s." % (d, fr(1, d), r, "" if r == 1 else "s", w, mx(w, r, d), fr(n, d)))
    if w == 0:
        e = e.replace("%s = %s." % (mx(w, r, d), fr(n, d)), "%s." % fr(n, d))
    if mode == "mix":
        e = e.replace("So it shows %s" % mx(w, r, d), "So it shows <b>%s</b>" % mx(w, r, d))
        c = []
        if r == 1 and w >= 1:
            c.append(Dc("%d.%d" % (w, d)))
            e += " It is not %d.%d: the 4 means quarters, not tenths." % (w, d) if d == 4 else \
                " It is not %d.%d: the %d means %s, not tenths." % (w, d, d, WORD[d])
        c += [Mc(w, r, d * L), Mc(w + 1, r, d), Mc(w, d - r, d) if d - r != r else None, Mc(w, r + 1, d), Fc(r, d)]
        ask = "Give a mixed numeral." if w else "Give a fraction."
        return mcq(fig(arrow_line_svg(L, d, t)) + "What number does the arrow show? " + ask, Mc(w, r, d), c, e, rnd)
    e = e.replace("= %s." % fr(n, d), "= <b>%s</b>. Count all the marks from 0: %d." % (fr(n, d), n))
    return mcq(fig(arrow_line_svg(L, d, t)) + "What number does the arrow show? Give an improper fraction.",
               Fc(n, d), [Fc(n, d * L), Fc(n + 1, d), Fc(r, d), Fc(n - 1, d), Fc(d, n)], e, rnd)


def nl_item(t, tshow, L, d, rnd):
    cands = [t + F(k, d) for k in (-4, -3, -2, -1, 1, 2, 3, 4)]
    cands = [c for c in cands if 0 < c < L]
    pos = SPOTS.next(rnd)
    lo = sorted([c for c in cands if c < t], reverse=True)
    hi = sorted([c for c in cands if c > t])
    # a classic mistake: counting d marks after the whole (1 1/4 put at 2)
    pts = sorted(lo[:pos] + [t] + hi[:3 - pos])
    assert len(pts) == 4 and len(set(pts)) == 4, (t, pts)
    for v in pts:
        assert (v * d).denominator == 1 and 0 < v < L
    letter = "ABCD"[pts.index(t)]
    w = int(t)
    r = int((t - w) * d)
    n = int(t * d)
    imp, mix = fr(n, d), mx(w, r, d)
    if tshow == "imp":
        e = ("Each whole is split into %d equal parts, so each mark is %s. %s = %s: go to %d, then %d more mark%s. "
             "That is letter <b>%s</b>." % (d, fr(1, d), imp, mix, w, r, "" if r == 1 else "s", letter))
    else:
        e = ("Each whole is split into %d equal parts, so each mark is %s. For %s, go to %d, then %d more mark%s. "
             "That is letter <b>%s</b>." % (d, fr(1, d), mix, w, r, "" if r == 1 else "s", letter))
    q = fig(letters_line_svg(L, d, pts)) + "Which letter shows %s?" % (imp if tshow == "imp" else mix)
    return {"q": q, "c": ["A", "B", "C", "D"], "a": pts.index(t), "e": e}


def set_lines(rnd):
    SPOTS.left = []
    its = []
    for t, d, mode in [(F(3, 4), 4, "mix"), (F(5, 4), 4, "mix"), (F(5, 2), 2, "mix"),
                       (F(7, 5), 5, "mix")]:
        its.append(arrow_item(t, 3, d, mode, rnd))
    for t, show_as, d in [(F(6, 4), "mix", 4), (F(5, 3), "imp", 3), (F(6, 5), "mix", 5), (F(4, 3), "mix", 3)]:
        its.append(nl_item(t, show_as, 3, d, rnd))
    for t, d, mode in [(F(9, 4), 4, "mix"), (F(11, 4), 4, "imp"), (F(8, 3), 3, "imp"), (F(9, 5), 5, "imp")]:
        its.append(arrow_item(t, 3, d, mode, rnd))
    for t, show_as, d in [(F(7, 4), "imp", 4), (F(11, 5), "mix", 5), (F(8, 5), "imp", 5), (F(5, 4), "imp", 4)]:
        its.append(nl_item(t, show_as, 3, d, rnd))

    assert 2 < F(11, 4) < 3 and F(7, 4) < 2 and F(13, 4) > 3 and F(8, 4) == 2
    its.append(mcq("Which improper fraction is between 2 and 3 on a number line?", Fc(11, 4), [Fc(7, 4), Fc(13, 4), Fc(8, 4)],
                   "2 = %s and 3 = %s. <b>%s</b> is between them (= 2 %s). %s is less than 2, %s is more than 3, "
                   "and %s is exactly 2." % (fr(8, 4), fr(12, 4), fr(11, 4), fr(3, 4), fr(7, 4), fr(13, 4), fr(8, 4)), rnd))
    its.append(mcq("A number line from 0 to 3 is split into fifths. How many marks after 0 is 2 %s?" % fr(1, 5),
                   Nc(11, " marks"), [Nc(3, " marks"), Nc(6, " marks"), Nc(10, " marks"), Nc(12, " marks")],
                   "Each whole has 5 marks. 2 wholes = 2 × 5 = 10 marks. 1 more mark: 10 + 1 = <b>11 marks</b>. "
                   "So 2 %s = %s." % (fr(1, 5), fr(11, 5)), rnd))
    dist = {v: abs(v - 2) for v in [F(9, 4), F(6, 4), F(11, 4), F(5, 4)]}
    assert min(dist, key=dist.get) == F(9, 4) and list(dist.values()).count(min(dist.values())) == 1
    its.append(mcq("Which number is closest to 2 on a number line?", Mc(2, 1, 4), [Mc(1, 2, 4), Mc(2, 3, 4), Mc(1, 1, 4)],
                   "Count the quarter marks from 2: 2 %s is 1 mark away, 1 %s is 2 marks away, 2 %s is 3 marks away and "
                   "1 %s is 3 marks away. So <b>2 %s</b> is closest." % (fr(1, 4), fr(2, 4), fr(3, 4), fr(1, 4), fr(1, 4)), rnd))
    assert F(5, 3) < 2 and F(7, 3) > 2
    its.append(mcq("On a number line, which number comes just before 2 when you count by thirds?", Mc(1, 2, 3),
                   [Mc(2, 1, 3), Mc(1, 1, 3), Fc(2, 3)],
                   "Counting by thirds: 1 %s, 1 %s, 2. So <b>1 %s</b> comes just before 2. %s comes just after 2."
                   % (fr(1, 3), fr(2, 3), fr(2, 3), mx(2, 1, 3)), rnd))
    assert len(its) == 20, len(its)
    return {"title": "Fractions and mixed numerals on number lines from 0 to 3", "items": its}


# ============================================================ set 5: word problems
def set_words(rnd):
    SPOTS.left = []
    its = []
    # 1
    assert 5 * F(1, 4) == F(5, 4)
    its.append(mcq("The school track is %s km around. Ethan runs 5 laps. How far does he run?" % fr(1, 4),
                   Mc(1, 1, 4, " km"), [Dc("1.4", " km"), Mc(1, 2, 4, " km"), Nc(5, " km"), Mc(1, 1, 5, " km")],
                   "Count by quarters: %s, %s, %s, 1, 1 %s. 5 quarters = %s = <b>1 %s km</b>. "
                   "It is not 1.4 km: the 4 means quarters, not tenths." % (fr(1, 4), fr(2, 4), fr(3, 4), fr(1, 4), fr(5, 4), fr(1, 4)), rnd))
    # 2
    assert 2 / F(1, 4) == 8
    its.append(mcq("The track is %s km around. How many laps does Jack need to run to go 2 km?" % fr(1, 4),
                   Nc(8, " laps"), [Nc(2, " laps"), Nc(4, " laps"), Nc(6, " laps")],
                   "4 laps make 1 km (4 quarters = 1 whole). 2 km = 2 × 4 = <b>8 laps</b>.", rnd))
    # 3
    its.append(mcq("Mia’s scoop holds %s cup of flour. She puts in 4 scoops. How much flour is that?" % fr(1, 3),
                   Mc(1, 1, 3, " cups"), [Nc(4, " cups"), Mc(1, 2, 3, " cups"), Mc(1, 1, 4, " cups"), Fc(4, 12, " cup")],
                   "Count by thirds: %s, %s, 1, 1 %s. 4 thirds = <b>1 %s cups</b>." % (fr(1, 3), fr(2, 3), fr(1, 3), fr(1, 3)), rnd))
    # 4
    its.append(mcq("A recipe needs 2 cups of flour. Oliver only has a %s cup measure. How many times must he fill it?" % fr(1, 2),
                   Nc(4), [Nc(2), Nc(3), Nc(5)],
                   "2 halves make 1 cup, so 2 cups = 2 × 2 = <b>4</b> half cups.", rnd))
    # 5
    its.append(mcq("At footy, the coach cuts oranges into quarters. The team eats 9 quarters. How many oranges is that?",
                   Mc(2, 1, 4, " oranges"), [Nc(9, " oranges"), Nc(2, " oranges"), Nc(3, " oranges"), Mc(2, 1, 9, " oranges")],
                   "4 quarters make 1 orange. 9 = 4 + 4 + 1, so 9 quarters = 2 oranges and 1 quarter = <b>2 %s oranges</b>."
                   % fr(1, 4), rnd))
    # 6
    its.append(mcq("Charlotte has 5 water bottles. Each bottle holds %s L. How much water is there in all?" % fr(1, 2),
                   Mc(2, 1, 2, " L"), [Nc(5, " L"), Mc(2, 1, 5, " L"), Mc(5, 1, 2, " L"), Nc(2, " L")],
                   "Count by halves: %s, 1, 1 %s, 2, 2 %s. 5 halves = <b>2 %s L</b>." % (fr(1, 2), fr(1, 2), fr(1, 2), fr(1, 2)), rnd))
    # 7
    its.append(mcq("Jack counts the distance as he runs %s km laps: %s, %s, %s … What does he say next?"
                   % (fr(1, 4), fr(1, 4), fr(2, 4), fr(3, 4)),
                   Nc(1, " km"), [Fc(4, 5, " km"), Mc(1, 1, 4, " km"), Nc(4, " km")],
                   "%s + %s = %s, and %s is 1 whole. So he says <b>1 km</b>. %s is a mistake, and 1 must not be skipped."
                   % (fr(3, 4), fr(1, 4), fr(4, 4), fr(4, 4), fr(4, 5)), rnd))
    # 8
    its.append(mcq("Isla cuts 7 pieces of ribbon. Each piece is %s m long. How long are they all together?" % fr(1, 3),
                   Mc(2, 1, 3, " m"), [Nc(7, " m"), Mc(2, 1, 7, " m"), Mc(2, 2, 3, " m"), Mc(1, 1, 3, " m")],
                   "3 thirds make 1 metre. 7 = 3 + 3 + 1, so 7 thirds = <b>2 %s m</b>." % fr(1, 3), rnd))
    # 9
    assert 2 - 3 * F(1, 4) == F(5, 4)
    its.append(mcq("A jug holds 2 L of juice. Mei pours 3 cups of %s L each. How much juice is left in the jug?" % fr(1, 4),
                   Mc(1, 1, 4, " L"), [Fc(3, 4, " L"), Mc(1, 3, 4, " L"), Mc(1, 2, 4, " L")],
                   "Count back by quarters from 2: 1 %s, 1 %s, 1 %s. <b>1 %s L</b> is left. %s L is what she poured."
                   % (fr(3, 4), fr(2, 4), fr(1, 4), fr(1, 4), fr(3, 4)), rnd))
    # 10
    assert 6 * F(1, 4) == F(3, 2)
    its.append(mcq("Amelia reads for %s of an hour each night. How long does she read in 6 nights?" % fr(1, 4),
                   Mc(1, 1, 2, " hours"), [Nc(6, " hours"), Mc(1, 1, 4, " hours"), Mc(6, 1, 4, " hours"), Mc(1, 3, 4, " hours")],
                   "Count by quarters: %s, %s, %s, 1, 1 %s, 1 %s. 6 quarters = 1 %s = <b>1 %s hours</b>."
                   % (fr(1, 4), fr(2, 4), fr(3, 4), fr(1, 4), fr(2, 4), fr(2, 4), fr(1, 2)), rnd))
    # 11
    assert 7 * F(1, 4) > F(3, 2)
    its.append(mcq("Oliver runs 7 laps of a %s km track. Harper runs 1 %s km. Who runs further?" % (fr(1, 4), fr(1, 2)),
                   "Oliver", ["Harper", "They run the same", CANT],
                   "7 quarters = 1 %s km. 1 %s = 1 %s. 3 quarters is more than 2 quarters, so <b>Oliver</b> runs further."
                   % (fr(3, 4), fr(1, 2), fr(2, 4)), rnd))
    # 12
    assert F(3, 2) / F(1, 4) == 6
    its.append(mcq("Chloe needs 1 %s cups of flour. She uses a %s cup measure. How many scoops does she need?" % (fr(1, 2), fr(1, 4)),
                   Nc(6), [Nc(5), Nc(4), Nc(3)],
                   "1 cup = 4 quarters and %s = 2 quarters. 4 + 2 = <b>6</b> scoops." % fr(1, 2), rnd))
    # 13
    its.append(mcq("A 3 km bike path has a sign every %s km. There is a sign at the finish but not at the start. How many signs are there?"
                   % fr(1, 2), Nc(6, " signs"), [Nc(3, " signs"), Nc(5, " signs"), Nc(7, " signs")],
                   "Count by halves: %s, 1, 1 %s, 2, 2 %s, 3. That is <b>6 signs</b>." % (fr(1, 2), fr(1, 2), fr(1, 2)), rnd))
    # 14
    its.append(mcq("At a class party, each cake is cut into thirds. The students eat 8 thirds. How many cakes is that?",
                   Mc(2, 2, 3, " cakes"), [Nc(8, " cakes"), Mc(3, 2, 3, " cakes"), Mc(2, 1, 3, " cakes"), Mc(2, 2, 8, " cakes")],
                   "3 thirds make 1 cake. 8 = 3 + 3 + 2, so 8 thirds = <b>2 %s cakes</b>." % fr(2, 3), rnd))
    # 15
    its.append(mcq("Kai counts by quarters. He says, “2 %s, 2 %s, 2 %s, 2 %s.” What should he say after 2 %s?"
                   % (fr(1, 4), fr(2, 4), fr(3, 4), fr(4, 5), fr(3, 4)),
                   Nc(3), [Mc(2, 4, 5), Mc(3, 1, 4), Mc(2, 1, 4)],
                   "2 %s + %s = 2 %s = <b>3</b>. The denominator stays 4, so 2 %s is wrong." % (fr(3, 4), fr(1, 4), fr(4, 4), fr(4, 5)), rnd))
    # 16
    assert F(2) + F(1, 4) == F(9, 4)
    its.append(mcq("A recipe says %s cups of milk. Sienna pours 2 %s cups. Is that the right amount?" % (fr(9, 4), fr(1, 4)),
                   "Yes. 2 %s = %s" % (fr(1, 4), fr(9, 4)),
                   ["No. 2 %s = %s" % (fr(1, 4), fr(3, 4)), "No. 2 %s = %s" % (fr(1, 4), fr(21, 4)),
                    "No. %s is less than 2" % fr(9, 4)],
                   "2 wholes = 8 quarters. Add 1 quarter: 8 + 1 = 9. So 2 %s = %s. <b>Yes</b>, it is right."
                   % (fr(1, 4), fr(9, 4)), rnd))
    # 17
    assert F(7, 4) / F(1, 4) == 7
    its.append(mcq("Ava has run 1 %s km on a %s km track. How many laps has she run?" % (fr(3, 4), fr(1, 4)),
                   Nc(7, " laps"), [Nc(4, " laps"), Nc(8, " laps"), Nc(3, " laps")],
                   "1 km = 4 laps. %s km = 3 more laps. 4 + 3 = <b>7 laps</b>." % fr(3, 4), rnd))
    # 18
    assert (3 - F(7, 3)) / F(1, 3) == 2
    its.append(mcq("Noah needs 3 cups of flour. He has put in 2 %s cups with a %s cup scoop. How many more scoops does he need?"
                   % (fr(1, 3), fr(1, 3)), Nc(2), [Nc(1), Nc(3), Nc(7)],
                   "Count on by thirds from 2 %s: 2 %s, 3. That is <b>2</b> more scoops." % (fr(1, 3), fr(2, 3)), rnd))
    # 19
    assert F(5, 4) < F(14, 10)
    its.append(mcq("Matilda walks 1 %s km to school. Her brother says that is 1.4 km. Which is true?" % fr(1, 4),
                   "1 %s km is less than 1.4 km" % fr(1, 4),
                   ["1 %s km is the same as 1.4 km" % fr(1, 4), "1 %s km is more than 1.4 km" % fr(1, 4), CANT],
                   "1 %s is 1 whole and 1 quarter. A quarter is 25 hundredths, so 1 %s = 1.25. 1.4 is 1 and 4 tenths = 1.40. "
                   "So <b>1 %s km is less than 1.4 km</b>." % (fr(1, 4), fr(1, 4), fr(1, 4)), rnd))
    # 20
    assert 2 / F(1, 5) == 10
    its.append(mcq("Grace fills cups of %s L from a 2 L bottle of water. How many cups can she fill?" % fr(1, 5),
                   Nc(10, " cups"), [Nc(2, " cups"), Nc(5, " cups"), Nc(7, " cups")],
                   "5 fifths make 1 L. 2 L = 2 × 5 = <b>10 cups</b>.", rnd))
    assert len(its) == 20, len(its)
    return {"title": "Counting by fractions word problems", "items": its}


# ============================================================ lesson
def body_html():
    return (
        "<h2>Counting by fractions</h2>"
        "<p>Counting by quarters means adding " + fr(1, 4) + " each time. "
        "After " + fr(3, 4) + " comes " + fr(4, 4) + ", which is <b>1 whole</b>. Then keep going: 1 " + fr(1, 4) + ", 1 " + fr(2, 4) + " …</p>"
        "<figure class='sn-fig'>" + labelled_line_svg(2, 4) +
        "<figcaption>Counting by quarters from 0 to 2.</figcaption></figure>"
        + ex("Example", "Count on by thirds from " + fr(1, 3) + " to 2.",
             "Add " + fr(1, 3) + " each time. " + fr(3, 3) + " = 1 and 1 " + fr(3, 3) + " = 2.",
             ", ".join(T(i, 3) for i in range(1, 7)))
        + ex("Example", "Count back by halves from 2 " + fr(1, 2) + ".",
             "Take away " + fr(1, 2) + " each time. One half less than 2 is 1 " + fr(1, 2) + ".",
             ", ".join(T(i, 2) for i in range(5, 0, -1)))
        + "<h2>Improper fractions and mixed numerals</h2>"
        "<p>An <b>improper fraction</b> such as " + fr(7, 4) + " has a numerator bigger than its denominator. "
        "A <b>mixed numeral</b> such as 1 " + fr(3, 4) + " shows the same amount as wholes and a fraction.</p>"
        "<figure class='sn-fig'>" + wholes_svg(4, 7) +
        "<figcaption>Each bar is 1 whole. 7 quarters = 1 whole and 3 more quarters: " + fr(7, 4) + " = 1 " + fr(3, 4) + ".</figcaption></figure>"
        + ex("Example", "Write 2 " + fr(1, 3) + " as an improper fraction.",
             "2 wholes = 2 × 3 = 6 thirds. Add 1 third: 6 + 1 = 7.", fr(7, 3))
        + "<h2>Mixed numerals on a number line</h2>"
        "<p>Find the whole number first. Then count on the marks for the fraction part.</p>"
        "<figure class='sn-fig'>" + arrow_line_svg(3, 4, F(5, 4)) +
        "<figcaption>Go to 1, then 1 quarter mark more: the arrow shows 1 " + fr(1, 4) + ".</figcaption></figure>"
        + ex("Example", "Where is 2 " + fr(2, 3) + " on a number line split into thirds?",
             "Go to 2. Each mark is " + fr(1, 3) + ", so count on 2 marks.", "2 marks after 2, just before 3")
        + "<h2>Common mistakes</h2>"
        + table(["Mistake", "What to do instead"], [
            [fr(3, 4) + ", " + fr(4, 5) + ", …",
             "Add " + fr(1, 4) + " each time. The denominator stays 4: " + fr(3, 4) + ", 1, 1 " + fr(1, 4)],
            ["Skipping the whole: " + fr(3, 4) + ", 1 " + fr(1, 4),
             fr(4, 4) + " = 1 comes first: " + fr(3, 4) + ", 1, 1 " + fr(1, 4)],
            ["Putting 1 " + fr(1, 4) + " at 1.4",
             "1 " + fr(1, 4) + " is 1 whole and 1 quarter: 1 quarter mark after 1. (It is 1.25, not 1.4.)"],
            ["Counting all the parts in all the bars for the denominator: " + fr(7, 8),
             "The denominator is the number of parts in <b>one</b> whole: " + fr(7, 4)],
        ])
    )


FAQ = [
    {"q": "What do Year 4 students learn about counting by fractions?",
     "a": "In the Australian Curriculum (AC9M4N04), Year 4 students count by fractions such as quarters, thirds, halves and fifths, including mixed numerals, and show these numbers on a number line. For example: 1/4, 2/4, 3/4, 1, 1 1/4."},
    {"q": "What is a mixed numeral?",
     "a": "A mixed numeral is a whole number and a fraction written together, such as 1 3/4. It is the same amount as the improper fraction 7/4, because 1 whole is 4 quarters and 4 + 3 = 7."},
    {"q": "How do you put a mixed numeral on a number line?",
     "a": "Go to the whole number first, then count on the fraction part. For 2 1/3 on a line split into thirds, go to 2 and count 1 more mark."},
    {"q": "Is 1 1/4 the same as 1.4?",
     "a": "No. 1 1/4 is 1 whole and 1 quarter, which is 1.25. 1.4 is 1 whole and 4 tenths, so 1 1/4 is less than 1.4."},
]


def gen():
    rnd = random.Random(4807)
    SPOTS.left = []
    sets = [set_count_on(rnd), set_next(rnd), set_pictures(rnd), set_lines(rnd), set_words(rnd)]
    for s in sets:
        assert len(s["items"]) == 20, (s["title"], len(s["items"]))
        cnt = [0, 0, 0, 0]
        for it in s["items"]:
            assert len(set(it["c"])) == 4, it
            cnt[it["a"]] += 1
        assert cnt == [5, 5, 5, 5], (s["title"], cnt)
    return {
        "country": "au", "subject": "maths", "grade": "year-4", "slug": SLUG, "sort": 7,
        "updated": UPDATED, "pdf_url": "",
        "title": "Year 4 Counting by Fractions and Mixed Numerals",
        "seo_title": "Year 4 Counting by Fractions Worksheets: Mixed Numerals and Number Lines (Free, with Answer Key)",
        "short_title": "Counting by fractions",
        "domain": "Number",
        "standard_code": "AC9M4N04",
        "standard_url": "https://v9.australiancurriculum.edu.au/f-10-curriculum/learning-areas/mathematics",
        "standard_text": "Count by fractions including mixed numerals; locate and represent these fractions as numbers on number lines",
        "meta_desc": "Free Year 4 maths worksheets on counting by fractions for the Australian Curriculum (AC9M4N04): count on and back by halves, thirds, quarters and fifths, improper fractions, mixed numerals, number lines from 0 to 3 and word problems. 100 questions with an answer key.",
        "key_big": "Count on by the same fraction each time. After 3/4 comes 4/4 = 1, then 1 1/4.",
        "key_sub": "A mixed numeral like 1 1/4 is 1 whole and 1 quarter (not 1.4). On a number line, go to 1, then count on 1 quarter mark.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, SLUG + ".json")
    mark_large(u, "(number line|bars of|circles of)")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(u, f, ensure_ascii=False, indent=1)
    print("wrote", path)
