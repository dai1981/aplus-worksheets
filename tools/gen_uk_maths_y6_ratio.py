# -*- coding: utf-8 -*-
"""
UK Year 6 Maths: Ratio and proportion (National Curriculum in England, Year 6: Ratio and proportion)
  python3 tools/gen_uk_maths_y6_ratio.py
Ratios from pictures (a : b, "for every ... there are ..."), ratio and fraction of the whole,
scaling recipes and missing values, scale factors and similar shapes, unequal sharing with
bar models, and SATs-style word problems (paint, maps, sweets, recipes, prices).
Wrong answers come from real mistakes: reversed order, 3 : 2 read as 3/2 instead of 3/5,
adding instead of multiplying, dividing the total by each number of the ratio, one part only.
Every choice carries its value; no two choices are equal in value.
HTML attributes use single quotes (no backslashes in the JSON). British English.
"""
import json, math, os, random, re
from fractions import Fraction as F
from math import gcd

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "uk", "maths", "year-6")
UPDATED = "2026-11-02"
GREEN = "#2e7d4f"
FILL = "#4fae74"
FILL_L = "#cfe6d6"
FILL2 = "#f2b84b"
FILL2_E = "#a8761a"
RED = "#c0392b"
INK = "#2b2b2b"
FONT = "Arial, Helvetica, sans-serif"
GIRLS = ["Amelia", "Isla", "Freya", "Poppy", "Ava", "Aisha", "Lily", "Zara", "Grace", "Ruby", "Maya", "Evie"]
BOYS = ["Oliver", "Harry", "Mohammed", "Jack", "Arjun", "Noah", "George", "Leo", "Alfie", "Kai", "Ethan", "Charlie"]


# ------------------------------------------------------------ numbers and choices
def num(n):
    if isinstance(n, F):
        n = float(n) if n.denominator != 1 else n.numerator
    if isinstance(n, float):
        s = ("%.2f" % n).rstrip("0").rstrip(".")
        whole, _, dec = s.partition(".")
        return "{:,}".format(int(whole)) + ("." + dec if dec else "")
    return "{:,}".format(n)


def R(a, b):
    return "%s : %s" % (num(a), num(b))


def fr(a, b):
    return "<span class='fr'><span class='fn'>%s</span><span class='fd'>%s</span></span>" % (a, b)


def money(p, pence_ok=True):
    """p in pence. 75p, £1.50, £12 (whole pounds) or £4.00 when pence_ok is False-ish context."""
    if p < 100 and pence_ok:
        return "%dp" % p
    if p % 100 == 0 and pence_ok == "whole":
        return "£%s" % num(p // 100)
    return "£%s.%02d" % (num(p // 100), p % 100)


def Rc(a, b):
    return (R(a, b), F(a, b))


def Fc(a, b):
    return (fr(a, b), F(a, b))


def Nc(n, unit=""):
    return ("%s%s" % (num(n), unit), F(n))


def Pc(p, style=True):
    return (money(p, style), F(p))


def plain(s):
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", s)).strip()


def mcq(q, right, cands, e):
    """right / cands are (html, value). First 3 usable wrong choices are kept: positive,
    different text and different value from the answer and from each other. Answer stored at 0."""
    seen, vals, pick = {plain(right[0])}, {right[1]}, []
    for c in cands:
        if c is None:
            continue
        s, v = c
        if plain(s) in seen or v in vals:
            continue
        if isinstance(v, F) and v <= 0:
            continue
        seen.add(plain(s))
        vals.add(v)
        pick.append(s)
        if len(pick) == 3:
            break
    assert len(pick) == 3, (q, right, cands)
    return {"q": q, "c": [right[0]] + pick, "a": 0, "e": e}


def balance(sets, rnd):
    """Spread the correct answers evenly (5/5/5/5) over the 4 positions in every set."""
    for s in sets:
        targets = [0, 1, 2, 3] * 5
        rnd.shuffle(targets)
        for it, t in zip(s["items"], targets):
            right = it["c"][0]
            wrong = it["c"][1:]
            rnd.shuffle(wrong)
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

    def two(self):
        return self.next(), self.next()


def cap(s):
    return s[0].upper() + s[1:]


def unit(n, one, many=None):
    return "%s %s" % (num(n), one if n == 1 else (many or one + "s"))


def coprime_pair(rnd, lo=1, hi=7, maxsum=12):
    while True:
        p, q = rnd.randint(lo, hi), rnd.randint(lo, hi)
        if p != q and gcd(p, q) == 1 and p + q <= maxsum:
            return p, q


# ------------------------------------------------------------ html helpers
def fig(svg):
    return "<div class='qfig'>" + svg + "</div>"


def svg_wrap(w, h, body, label):
    w, h = int(math.ceil(w)), int(math.ceil(h))
    return ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 %d %d' width='%d' height='%d' "
            "role='img' aria-label='%s'><g font-family='%s'>%s</g></svg>" % (w, h, w, h, label, FONT, body))


def tw(t, fs):
    t = str(t)
    return (len(t) - t.count(",") * 0.6 - t.count(" ") * 0.3) * fs * 0.6


def text(x, y, t, fs=15, anchor="middle", col=INK):
    return ("<text x='%.1f' y='%.1f' font-size='%d' font-weight='700' fill='%s' text-anchor='%s'>%s</text>"
            % (x, y, fs, col, anchor, t))


def table(head, rows):
    h = "".join("<th>%s</th>" % x for x in head)
    b = "".join("<tr>" + "".join("<td>%s</td>" % c for c in r) + "</tr>" for r in rows)
    return "<div class='sn-tw'><table class='sn-table'><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>" % (h, b)


def ex(title, q, s, a):
    return ("<div class='sn-ex'><span class='sn-ex-t'>%s</span><p class='sn-ex-q'>%s</p>"
            "<p class='sn-ex-s'>%s</p><p class='sn-ex-a'>Answer: %s</p></div>" % (title, q, s, a))


def mark_large(u, pattern):
    """Tag pictures that must print larger so their parts and labels stay readable."""
    rx = re.compile(r"<svg (?=[^>]*aria-label='" + pattern + ")")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u


# ------------------------------------------------------------ figures
SHAPE_NAMES = {"c": ("circle", "circles"), "s": ("square", "squares"), "t": ("triangle", "triangles")}


def shape(kind, cx, cy):
    if kind == "c":
        return "<circle cx='%.1f' cy='%.1f' r='11' fill='%s' stroke='%s' stroke-width='2'/>" % (cx, cy, FILL, GREEN)
    if kind == "s":
        return ("<rect x='%.1f' y='%.1f' width='21' height='21' fill='%s' stroke='%s' stroke-width='2'/>"
                % (cx - 10.5, cy - 10.5, FILL2, FILL2_E))
    return ("<path d='M%.1f %.1f L%.1f %.1f L%.1f %.1f Z' fill='%s' stroke='%s' stroke-width='2' stroke-linejoin='round'/>"
            % (cx, cy - 11, cx + 12, cy + 10, cx - 12, cy + 10, FILL_L, GREEN))


def shapes_svg(kinds):
    """Shapes in order, one row up to 8, otherwise two rows."""
    n = len(kinds)
    per = n if n <= 8 else (n + 1) // 2
    cell = 32
    rows = (n + per - 1) // per
    body = []
    for i, k in enumerate(kinds):
        r, c = divmod(i, per)
        body.append(shape(k, 4 + cell * c + cell / 2, 4 + cell * r + cell / 2))
    counts = [unit(kinds.count(k), *SHAPE_NAMES[k]) for k in "cst" if kinds.count(k)]
    return svg_wrap(8 + cell * per, 8 + cell * rows, "".join(body), "shapes picture: " + " and ".join(counts))


def bar_svg(rows, total=None, label="bar model"):
    """rows: [(label, boxes, cell_text, right_text, colour)]; optional bracket on the right with the total."""
    fs = 15
    lw = max(tw(r[0], fs) for r in rows) + 12
    x0 = 6 + lw
    cw = max([32] + [tw(r[2], fs) + 14 for r in rows if r[2]])
    bh, gap, y0 = 28, 10, 4
    s, ends = [], []
    for i, (lab, n, cell, right, col) in enumerate(rows):
        y = y0 + i * (bh + gap)
        s.append(text(x0 - 8, y + bh / 2 + 5.5, lab, fs, "end"))
        for j in range(n):
            x = x0 + j * cw
            s.append("<rect x='%.1f' y='%d' width='%.1f' height='%d' fill='%s' stroke='%s' stroke-width='2.5'/>"
                     % (x, y, cw, bh, col, INK))
            if cell:
                s.append(text(x + cw / 2, y + bh / 2 + 5.5, cell, fs, col=RED if cell == "?" else INK))
        xe = x0 + n * cw
        if right:
            s.append(text(xe + 8, y + bh / 2 + 5.5, right, fs, "start", RED if right == "?" else INK))
            xe += 8 + tw(right, fs)
        ends.append(xe)
    ybot = y0 + len(rows) * (bh + gap) - gap
    W = max(ends) + 6
    if total:
        xb = max(ends) + 10
        s.append("<path d='M%.1f %d h8 V%d h-8' fill='none' stroke='%s' stroke-width='2'/>" % (xb, y0, ybot, INK))
        s.append(text(xb + 14, (y0 + ybot) / 2 + 5.5, total, fs, "start", RED if total == "?" else INK))
        W = xb + 14 + tw(total, fs) + 6
    return svg_wrap(W, ybot + 4, "".join(s), label)


def similar_svg(kind, a, b, labels, unit_cm="cm"):
    """Two similar shapes A and B drawn to the same scale, side by side, bottoms aligned.
    kind: 'rect' or 'tri' (right-angled, right angle bottom-left).
    a, b: (width, height) in cm. labels: ((wA, hA), (wB, hB)) texts, None = no label."""
    fs = 15
    big = max(a[0], a[1], b[0], b[1])
    sc = min(120.0 / big, 16.0)
    maxh = max(a[1], b[1]) * sc
    top = 22
    x = 6
    s = []
    for (w, h), (lw_, lh_), name in zip((a, b), labels, ("A", "B")):
        if lh_:
            x += tw(lh_, fs) + 8
        W, H = w * sc, h * sc
        yb = top + maxh
        if kind == "rect":
            s.append("<rect x='%.1f' y='%.1f' width='%.1f' height='%.1f' fill='%s' stroke='%s' stroke-width='2.5'/>"
                     % (x, yb - H, W, H, FILL_L if name == "A" else "#fde7bd", INK))
        else:
            s.append("<path d='M%.1f %.1f L%.1f %.1f L%.1f %.1f Z' fill='%s' stroke='%s' stroke-width='2.5' stroke-linejoin='round'/>"
                     % (x, yb - H, x, yb, x + W, yb, FILL_L if name == "A" else "#fde7bd", INK))
            s.append("<path d='M%.1f %.1f h8 v-8' fill='none' stroke='%s' stroke-width='1.5'/>" % (x, yb - 8, INK))
        s.append(text(x + (W / 2 if kind == "rect" else 4), yb - H - 6, name, fs, "middle" if kind == "rect" else "start"))
        if lh_:
            s.append(text(x - 6, yb - H / 2 + 5.5, lh_, fs, "end", RED if lh_ == "?" else INK))
        if lw_:
            s.append(text(x + W / 2, yb + 18, lw_, fs, "middle", RED if lw_ == "?" else INK))
        wl = tw(lw_, fs) if lw_ else 0
        x = max(x + W, x + W / 2 + wl / 2) + 26
    Wt = x - 26 + 8
    return svg_wrap(Wt, top + maxh + 24, "".join(s),
                    "similar shapes: %s A %s by %s cm, B %s by %s cm" % ("rectangle" if kind == "rect" else "triangle",
                                                                        num(a[0]), num(a[1]), num(b[0]), num(b[1])))


# ============================================================ set 1: ratios from pictures, ratio and fractions
def set_pictures(rnd):
    its = []
    used = set()

    def counts():
        while True:
            a, b = rnd.randint(2, 8), rnd.randint(2, 8)
            if a != b and a + b <= 14 and (a, b) not in used:
                used.add((a, b))
                return a, b

    def draw(cnt):
        kinds = []
        for k, m in zip("cst", cnt):
            kinds += [k] * m
        rnd.shuffle(kinds)
        return fig(shapes_svg(kinds))

    # 1) ratio from a picture (6)
    for i in range(6):
        a, b = counts()
        t = a + b
        if i < 4:
            q = "What is the ratio of circles to squares?"
            right, c = Rc(a, b), [Rc(b, a), Rc(a, t), Rc(t, b), Rc(b, t)]
            e = ("Count: %d circles and %d squares. Circles are named first, so write %d first: <b>%s</b>. "
                 "%s would be squares to circles." % (a, b, a, R(a, b), R(b, a)))
        else:
            q = "What is the ratio of squares to circles?"
            right, c = Rc(b, a), [Rc(a, b), Rc(b, t), Rc(t, a), Rc(a, t)]
            e = ("Count: %d squares and %d circles. Squares are named first, so write %d first: <b>%s</b>. "
                 "%s would be circles to squares." % (b, a, b, R(b, a), R(a, b)))
        its.append(mcq(draw((a, b)) + q, right, c, e))

    # 2) "for every" sentence from a grouped picture (3)
    for _ in range(3):
        while True:
            p, q = coprime_pair(rnd, 1, 4, 7)
            g = rnd.randint(2, 3)
            if (p * g + q * g) <= 16 and (p, q) not in used:
                used.add((p, q))
                break
        a, b = p * g, q * g

        def sent(x, y):
            return ("For every %s there %s %s." % (unit(x, "circle"), "is" if y == 1 else "are", unit(y, "square")), F(x, y))

        right = sent(p, q)
        c = [sent(q, p), sent(p, p + q), sent(a, q), sent(p, b)]
        its.append(mcq(draw((a, b)) + "Which sentence is true for this picture?", right, c,
                       "There are %d circles and %d squares, so circles : squares = %s. Divide both by %d: %s. "
                       "So for every %s there %s <b>%s</b>." % (a, b, R(a, b), g, R(p, q), unit(p, "circle"),
                                                                 "is" if q == 1 else "are", unit(q, "square"))))

    # 3) fraction of the shapes from a picture (3)
    for i in range(3):
        a, b = counts()
        t = a + b
        if i < 2:
            right, c = Fc(a, t), [Fc(a, b), Fc(b, t), Fc(b, a)]
            e = ("There are %d + %d = %d shapes. %d of them are circles, so <b>%s</b> of the shapes are circles. "
                 "%s compares circles with squares, not with all the shapes." % (a, b, t, a, fr(a, t), fr(a, b)))
            q = "What fraction of the shapes are circles?"
        else:
            right, c = Fc(b, t), [Fc(b, a), Fc(a, t), Fc(a, b)]
            e = ("There are %d + %d = %d shapes. %d of them are squares, so <b>%s</b> of the shapes are squares. "
                 "%s compares squares with circles, not with all the shapes." % (a, b, t, b, fr(b, t), fr(b, a)))
            q = "What fraction of the shapes are squares?"
        its.append(mcq(draw((a, b)) + q, right, c, e))

    # 4) ratio -> fraction of the whole (5)
    CTX = [("red counters", "blue counters", "counters", "a bag", "red", "blue"),
           ("apples", "pears", "pieces of fruit", "a bowl", "apples", "pears"),
           ("girls", "boys", "children", "a choir", "girls", "boys"),
           ("cars", "vans", "vehicles", "a car park", "cars", "vans"),
           ("fiction books", "non-fiction books", "books", "a class library", "fiction", "non-fiction"),
           ("milk chocolates", "dark chocolates", "chocolates", "a box", "milk chocolate", "dark chocolate"),
           ("tulips", "daffodils", "flowers", "a flower bed", "tulips", "daffodils"),
           ("cats", "dogs", "animals", "an animal rescue centre", "cats", "dogs")]
    rnd.shuffle(CTX)
    seenpq = set()
    for i in range(5):
        X, Y, W, pl, sx, sy = CTX[i]
        while True:
            p, q = coprime_pair(rnd, 1, 7, 11)
            if (p, q) not in seenpq and p > 1 and q > 1:
                seenpq.add((p, q))
                break
        on = "in" if pl not in ("a car park",) else "in"
        if i < 3:
            right, c = Fc(p, p + q), [Fc(p, q), Fc(q, p + q), Fc(q, p)]
            ask, n, who = sx, p, X
        else:
            right, c = Fc(q, p + q), [Fc(q, p), Fc(p, p + q), Fc(p, q)]
            ask, n, who = sy, q, Y
        q_ = ("In %s, the ratio of %s to %s is %s. What fraction of the %s are %s?"
              % (pl, X, Y, R(p, q), W, ask))
        e = ("For every %d %s there are %d %s, so each group has %d + %d = %d %s. %d of every %d are %s: <b>%s</b>. "
             "%s is the wrong fraction: the denominator must be the whole group, %d."
             % (p, X, q, Y, p, q, p + q, W, n, p + q, who, fr(n, p + q), c[0][0], p + q))
        its.append(mcq(q_, right, c, e))

    # 5) fraction of the whole -> ratio (3)
    for i in range(3):
        X, Y, W, pl, sx, sy = CTX[5 + i]
        while True:
            p, q = coprime_pair(rnd, 1, 7, 11)
            if (p, q) not in seenpq and q > 1:
                seenpq.add((p, q))
                break
        t = p + q
        right, c = Rc(p, q), [Rc(p, t), Rc(q, p), Rc(t, p), Rc(q, t)]
        q_ = ("In %s, %s of the %s are %s. The rest are %s. What is the ratio of %s to %s?"
              % (pl, fr(p, t), W, X, Y, X, Y))
        e = ("%s means %d out of every %d. The rest is %d − %d = %d out of every %d. So %s : %s = <b>%s</b>, not %s."
             % (fr(p, t), p, t, t, p, q, t, X, Y, R(p, q), R(p, t)))
        its.append(mcq(q_, right, c, e))

    assert len(its) == 20, len(its)
    return {"title": "Ratios from pictures, and ratio as a fraction", "items": its}


# ============================================================ set 2: scaling recipes and missing values
def set_scaling(rnd, P):
    its = []
    # 1) recipes (6): (dish, people from, to, ingredient, amount, unit)
    RECIPES = [("pancakes", 4, 6, "flour", 300, "g"),
               ("vegetable soup", 4, 10, "stock", 600, "ml"),
               ("apple crumble", 6, 9, "flour", 180, "g"),
               ("a fruit smoothie", 2, 5, "milk", 250, "ml"),
               ("pizza dough", 8, 2, "flour", 480, "g"),
               ("shortbread", 6, 15, "butter", 120, "g")]
    for dish, n1, n2, ing, A, u in RECIPES:
        assert A % n1 == 0
        one = A // n1
        ans = one * n2
        c = [Nc(one, " " + u), Nc(A * n2, " " + u), Nc(A * n1 // n2, " " + u) if (A * n1) % n2 == 0 else None,
             Nc(A * 2, " " + u), Nc(A // 2, " " + u), Nc(A + n2 - n1, " " + u) if n2 > n1 else None]
        q = ("A recipe for %s for %d people uses %s %s of %s. How much %s is needed for %d people?"
             % (dish, n1, num(A), u, ing, ing, n2))
        e = ("For 1 person: %s ÷ %d = %s %s. For %d people: %s × %d = <b>%s %s</b>."
             % (num(A), n1, num(one), u, n2, num(one), n2, num(ans), u))
        if n2 < n1:
            e += " Fewer people need less, so the answer must be smaller than %s %s." % (num(A), u)
        its.append(mcq(q, Nc(ans, " " + u), c, e))

    # 2) missing values a : b = c : ? (4)
    seen = set()
    for i in range(4):
        while True:
            p, q = coprime_pair(rnd, 2, 9, 15)
            k = rnd.randint(3, 8)
            if (p, q) not in seen:
                seen.add((p, q))
                break
        if i < 2:
            given, ans = k * p, k * q
            q_ = "Find the missing number. %s = %s : ☐" % (R(p, q), num(given))
            c = [Nc(q + given - p), Nc(k), Nc(q * given), Nc(given)]
            e = ("%d × %d = %d, so multiply the second number by %d too: %d × %d = <b>%d</b>. "
                 "Adding %d to both numbers (%d) does not keep the ratio." % (p, k, given, k, q, k, ans, given - p, q + given - p))
        else:
            given, ans = k * q, k * p
            q_ = "Find the missing number. %s = ☐ : %s" % (R(p, q), num(given))
            c = [Nc(p + given - q), Nc(k), Nc(p * given), Nc(given)]
            e = ("%d × %d = %d, so multiply the first number by %d too: %d × %d = <b>%d</b>. "
                 "Adding %d to both numbers (%d) does not keep the ratio." % (q, k, given, k, p, k, ans, given - q, p + given - q))
        its.append(mcq(q_, Nc(ans), c, e))

    # 3) simplest form (3)
    for _ in range(3):
        while True:
            p, q = coprime_pair(rnd, 2, 9, 15)
            g = rnd.choice([4, 6, 8, 9])
            if (p, q) not in seen and p * g <= 72 and q * g <= 72 and p * g - g > 0:
                seen.add((p, q))
                break
        a, b = p * g, q * g
        c = [Rc(q, p), Rc(a - (g - 1), b - (g - 1)), Rc(p, b), Rc(a, q)]
        its.append(mcq("Write %s in its simplest form." % R(a, b), Rc(p, q), c,
                       "%d is the highest common factor of %d and %d. Divide <b>both</b> numbers by %d: "
                       "%d ÷ %d = %d and %d ÷ %d = %d, so the answer is <b>%s</b>."
                       % (g, a, b, g, a, g, p, b, g, q, R(p, q))))

    # 4) prices (4): (item, n1, cost1 pence, n2)
    PRICES = [("pencils", 5, 150, 8), ("apples", 4, 80, 10), ("cupcakes", 6, 420, 9), ("bread rolls", 3, 135, 7)]
    for item, n1, c1, n2 in PRICES:
        one = c1 // n1
        assert one * n1 == c1
        ans = one * n2
        c = [Pc(one), Pc(c1 * n2), Pc(c1 + n2 - n1), Pc(c1 * 2)]
        its.append(mcq("%d %s cost %s. How much do %d %s cost?" % (n1, item, money(c1), n2, item), Pc(ans), c,
                       "1 costs %s ÷ %d = %s. %d cost %s × %d = <b>%s</b>." % (money(c1), n1, money(one), n2, money(one), n2, money(ans))))

    # 5) "for every" missing values (3)
    FE = [("adults", "children", "school trip", 2, 15, 6, True),
          ("roses", "tulips", "garden", 3, 5, 20, False),
          ("pencils", "pens", "pot", 4, 7, 28, False)]
    for X, Y, pl, p, q, given, knowX in FE:
        if knowX:
            k = given // p
            ans = k * q
            q_ = "On a %s, for every %d %s there are %d %s. There are %d %s. How many %s are there?" % (pl, p, X, q, Y, given, X, Y)
            c = [Nc(given + q - p, " " + Y), Nc(k, " " + Y), Nc(given * q, " " + Y), Nc(given + q, " " + Y)]
            e = "%d %s is %d groups of %d (%d ÷ %d = %d). Each group has %d %s: %d × %d = <b>%d %s</b>." % (
                given, X, k, p, given, p, k, q, Y, k, q, ans, Y)
            its.append(mcq(q_, Nc(ans, " " + Y), c, e))
        else:
            k = given // q
            ans = k * p
            q_ = "In a %s, for every %d %s there are %d %s. There are %d %s. How many %s are there?" % (pl, p, X, q, Y, given, Y, X)
            c = [Nc(given - (q - p), " " + X), Nc(k, " " + X), Nc(given * p, " " + X), Nc(given + p, " " + X)]
            e = "%d %s is %d groups of %d (%d ÷ %d = %d). Each group has %d %s: %d × %d = <b>%d %s</b>." % (
                given, Y, k, q, given, q, k, p, X, k, p, ans, X)
            its.append(mcq(q_, Nc(ans, " " + X), c, e))
    assert len(its) == 20, len(its)
    return {"title": "Scaling recipes and finding missing values", "items": its}


# ============================================================ set 3: scale factors and similar shapes
def rect_txt(w, h):
    return ("%s cm by %s cm" % (num(w), num(h)), ("r", F(w), F(h)))


def set_scale(rnd):
    its = []
    # 1) enlarge a rectangle (4)
    for w, h, k in [(3, 5, 3), (2, 7, 4), (4, 6, 2), (5, 3, 5)]:
        right = rect_txt(w * k, h * k)
        c = [rect_txt(w + k, h + k), rect_txt(w * k, h), rect_txt(w * 2, h * 2), rect_txt(w, h * k)]
        F_ = fig(similar_svg("rect", (w, h), (w * k, h * k), ((num(w) + " cm", num(h) + " cm"), ("?", "?"))))
        its.append(mcq(F_ + "Rectangle A is %s cm by %s cm. It is enlarged by scale factor %d to make rectangle B. "
                       "What size is rectangle B?" % (num(w), num(h), k), right, c,
                       "Multiply <b>every</b> length by %d: %d × %d = %d and %d × %d = %d. B is <b>%d cm by %d cm</b>. "
                       "Adding %d (%d cm by %d cm) is not an enlargement." % (k, w, k, w * k, h, k, h * k, w * k, h * k, k, w + k, h + k)))

    # 2) find the scale factor (4)
    for w, h, k, kind in [(2, 3, 3, "rect"), (3, 4, 2, "tri"), (2, 5, 4, "rect"), (4, 3, 3, "tri")]:
        W2, H2 = w * k, h * k
        c = [Nc(W2 - w), Nc(W2), Nc(H2 - h), Nc(W2 + w), Nc(H2)]
        F_ = fig(similar_svg(kind, (w, h), (W2, H2), ((num(w) + " cm", num(h) + " cm"), (num(W2) + " cm", num(H2) + " cm"))))
        nm = "rectangle" if kind == "rect" else "triangle"
        its.append(mcq(F_ + "%s B is an enlargement of %s A. What is the scale factor?" % (cap(nm), nm), Nc(k), c,
                       "Compare matching sides: %d ÷ %d = %d and %d ÷ %d = %d. Each side is %d times as long, so the scale factor is <b>%d</b>. "
                       "The difference (%d − %d = %d) is not the scale factor." % (W2, w, k, H2, h, k, k, k, W2, w, W2 - w)))

    # 3) missing side of similar shapes (5)
    for w, h, k, kind, askw in [(3, 2, 4, "rect", False), (2, 5, 3, "tri", True), (4, 3, 2, "rect", True),
                                (3, 5, 3, "tri", False), (5, 2, 3, "rect", False)]:
        W2, H2 = w * k, h * k
        if askw:
            ans, labB, known, kv, oth = W2, ("?", num(H2) + " cm"), h, H2, w
        else:
            ans, labB, known, kv, oth = H2, (num(W2) + " cm", "?"), w, W2, h
        c = [Nc(oth + kv - known, " cm"), Nc(kv, " cm"), Nc(k, " cm"), Nc(oth * kv, " cm")]
        nm = "rectangles" if kind == "rect" else "triangles"
        F_ = fig(similar_svg(kind, (w, h), (W2, H2), ((num(w) + " cm", num(h) + " cm"), labB)))
        its.append(mcq(F_ + "The two %s are similar. What is the missing length?" % nm, Nc(ans, " cm"), c,
                       "Scale factor: %d ÷ %d = %d. Missing length: %d × %d = <b>%d cm</b>. "
                       "Adding %d cm (%d cm) does not keep the shape the same." % (kv, known, k, oth, k, ans, kv - known, oth + kv - known)))

    # 4) shapes made smaller (3)
    for big, oth, k, thing in [(12, 18, 3, "photo"), (25, 30, 5, "poster"), (16, 24, 4, "painting")]:
        small = big // k
        ans = oth // k
        c = [Nc(oth - (big - small), " cm"), Nc(k, " cm"), Nc(oth * k, " cm"), Nc(oth - k, " cm")]
        its.append(mcq("A %s is %d cm wide and %d cm tall. A smaller copy is made with the same shape. "
                       "The copy is %d cm wide. How tall is the copy?" % (thing, big, oth, small), Nc(ans, " cm"), c,
                       "%d ÷ %d = %d, so every length of the copy is the original length divided by %d. Height: %d ÷ %d = <b>%d cm</b>. "
                       "Taking away %d cm (%d − %d) does not keep the same shape." % (big, small, k, k, oth, k, ans, big - small, oth, big - small)))

    # 5) which rectangle is an enlargement? (4)
    for w, h, k in [(2, 3, 3), (3, 4, 2), (1, 4, 5), (2, 5, 4)]:
        right = rect_txt(w * k, h * k)
        c = [rect_txt(w + k, h + k), rect_txt(w * k, h * (k + 1)), rect_txt(w * k, h), rect_txt(w * (k + 1), h * k)]
        its.append(mcq("Which rectangle is an enlargement of a rectangle %s cm by %s cm?" % (num(w), num(h)), right, c,
                       "In an enlargement both sides are multiplied by the <b>same</b> number. "
                       "%d × %d = %d and %d × %d = %d, so <b>%d cm by %d cm</b> is an enlargement with scale factor %d."
                       % (w, k, w * k, h, k, h * k, w * k, h * k, k)))
    assert len(its) == 20, len(its)
    return {"title": "Scale factors and similar shapes", "items": its}


# ============================================================ set 4: unequal sharing with bar models
def set_sharing(rnd, P):
    its = []
    seen = set()

    def pqu(maxsum=9, ulo=3, uhi=12, ok=lambda p, q, u: True):
        for _ in range(10000):
            p, q = coprime_pair(rnd, 1, 7, maxsum)
            u = rnd.randint(ulo, uhi)
            if (p, q) not in seen and p > 1 and q > 1 and ok(p, q, u):
                seen.add((p, q))
                return p, q, u
        raise AssertionError("no ratio left")

    # 1) share an amount in a ratio (6)
    THINGS = [("stickers", "sticker"), ("marbles", "marble"), ("cards", "card")]
    for i in range(6):
        askA = i % 2 == 0
        p, q, u = pqu(9, 4, 12, lambda p, q, u: ((p + q) * u) % (p if askA else q) == 0)
        T = (p + q) * u
        (A, _, _), (B, _, _) = P.two()
        n = p if askA else q
        ans = n * u
        who = A if askA else B
        if i < 3:
            fmt = lambda v: "£" + num(v)
            q_ = "%s and %s share £%s in the ratio %s. How much does %s get?" % (A, B, num(T), R(p, q), who)
            mk = lambda v: ("£" + num(v), F(v))
            tot_lab = "£" + num(T)
        else:
            many, one = THINGS[i - 3]
            q_ = "%s and %s share %d %s in the ratio %s. How many %s does %s get?" % (A, B, T, many, R(p, q), many, who)
            mk = lambda v, one=one, many=many: (unit(v, one, many), F(v))
            fmt = lambda v: num(v)
            tot_lab = num(T)
        rows = [(A, p, "", "?" if askA else "", FILL_L), (B, q, "", "" if askA else "?", "#fde7bd")]
        F_ = fig(bar_svg(rows, tot_lab, "bar model: %s to %s is %s, total %s" % (A, B, R(p, q), tot_lab)))
        c = [mk(T // p) if T % p == 0 else None, mk(T // q) if T % q == 0 else None,
             mk((p + q - n) * u), mk(u), mk(ans + u), mk(T // 2) if T % 2 == 0 else None, mk(ans - u)]
        if askA:
            c = [c[0], c[2], c[1]] + c[3:]
        else:
            c = [c[1], c[2], c[0]] + c[3:]
        e = ("There are %d + %d = %d equal parts. One part is %s ÷ %d = %s. %s gets %d parts: %d × %s = <b>%s</b>. "
             "Do not divide %s by %d on its own." % (p, q, p + q, fmt(T), p + q, fmt(u), who, n, n, fmt(u), fmt(ans), fmt(T), n))
        its.append(mcq(F_ + q_, mk(ans), c, e))

    # 2) "times as many" (4)
    TA = [("boys", "girls", "a football club", "children", 3, 36, False),
          ("adults", "children", "a swimming pool", "people", 4, 40, True),
          ("blue pens", "red pens", "a box", "pens", 5, 30, False),
          ("cars", "bikes", "a car park", "vehicles", 3, 48, True)]
    for X, Y, pl, W, k, T, askX in TA:
        u = T // (k + 1)
        assert u * (k + 1) == T
        ans = k * u if askX else u
        other = u if askX else k * u
        c = [Nc(other), Nc(T // k) if T % k == 0 else None, Nc(T // 2), Nc(T - k), Nc(u * (k - 1))]
        rows = [(X, k, "", "?" if askX else "", FILL_L), (Y, 1, "", "" if askX else "?", "#fde7bd")]
        F_ = fig(bar_svg(rows, str(T), "bar model: %s %d parts, %s 1 part, total %d" % (X, k, Y, T)))
        q_ = ("In %s there are %d times as many %s as %s. There are %d %s altogether. How many %s are there?"
              % (pl, k, X, Y, T, W, X if askX else Y))
        e = ("%d times as many means the ratio %s : %s is %s. That is %d + 1 = %d equal parts. One part: %d ÷ %d = %d. "
             "%s: <b>%d</b>." % (k, X, Y, R(k, 1), k, k + 1, T, k + 1, u, cap(X if askX else Y), ans))
        if askX:
            e = e[:-len("<b>%d</b>." % ans)] + "%d × %d = <b>%d</b>." % (k, u, ans)
        its.append(mcq(F_ + q_, Nc(ans), c, e))

    # 3) fractions to share (3)
    FS = [("beads", "red", "blue", 2, 5, 30), ("pupils", "have school dinners", "bring a packed lunch", 3, 8, 32),
          ("sweets", "strawberry", "lemon", 4, 7, 35)]
    for W, X, Y, a, b, T in FS:
        part = T // b
        ans = (b - a) * part
        if W == "pupils":
            q_ = "In a class of %d pupils, %s of the pupils %s. The rest %s. How many pupils %s?" % (T, fr(a, b), X, Y, Y)
        else:
            q_ = "A bag has %d %s. %s of them are %s and the rest are %s. How many %s %s are there?" % (T, W, fr(a, b), X, Y, Y, W)
        c = [Nc(a * part), Nc(part), Nc(T // 2) if T % 2 == 0 else None, Nc(T - a), Nc(T * a // (a + b)) if (T * a) % (a + b) == 0 else None]
        e = ("%s of %d: %d ÷ %d = %d, and %d × %d = %d. The rest: %d − %d = <b>%d</b>. "
             "(Or: the rest is %s, and %d × %d = %d.)" % (fr(a, b), T, T, b, part, a, part, a * part, T, a * part, ans,
                                                          fr(b - a, b), b - a, part, ans))
        its.append(mcq(q_, Nc(ans), c, e))

    # 4) difference known (3)
    for i in range(3):
        if i == 0:
            seen.clear()
        p, q, u = pqu(10, 3, 9, lambda p, q, u: q - p >= 2)
        d = (q - p) * u
        (A, _, _), (B, _, _) = P.two()
        if i == 0:
            ans, ask = p * u, "How many cards does %s have?" % A
            c = [Nc(d), Nc(q * u), Nc(u), Nc(d * p)]
        elif i == 1:
            ans, ask = q * u, "How many cards does %s have?" % B
            c = [Nc(d), Nc(p * u), Nc(d * q), Nc(u)]
        else:
            ans, ask = (p + q) * u, "How many cards do they have altogether?"
            c = [Nc(d * (p + q)), Nc(q * u), Nc(d), Nc(d + p + q)]
        rows = [(A, p, "", "", FILL_L), (B, q, "", "", "#fde7bd")]
        F_ = fig(bar_svg(rows, None, "bar model: %s %d parts, %s %d parts" % (A, p, B, q)))
        q_ = "The ratio of %s’s cards to %s’s cards is %s. %s has %d more cards than %s. %s" % (A, B, R(p, q), B, d, A, ask)
        e = ("%s has %d − %d = %d more parts. Those %d parts are %d cards, so one part is %d ÷ %d = %d. "
             "%s: %d × %d = %d. %s: %d × %d = %d. Answer: <b>%d</b>."
             % (B, q, p, q - p, q - p, d, d, q - p, u, A, p, u, p * u, B, q, u, q * u, ans))
        its.append(mcq(F_ + q_, Nc(ans), c, e))

    # 5) one share known (4)
    for i in range(4):
        if i == 0:
            seen.clear()
        p, q, u = pqu(11, 3, 9)
        (A, _, _), (B, _, _) = P.two()
        a = p * u
        if i < 2:
            ans = q * u
            q_ = "%s and %s share some money in the ratio %s. %s gets £%d. How much does %s get?" % (A, B, R(p, q), A, a, B)
            c = [("£%d" % (a + q - p), F(a + q - p)) if a + q - p > 0 else None, ("£%d" % u, F(u)),
                 ("£%d" % ((p + q) * u), F((p + q) * u)), ("£%d" % (a * q), F(a * q))]
            e = ("%s’s %d parts are £%d, so one part is £%d ÷ %d = £%d. %s gets %d parts: %d × £%d = <b>£%d</b>."
                 % (A, p, a, a, p, u, B, q, q, u, ans))
            its.append(mcq(q_, ("£%d" % ans, F(ans)), c, e))
        else:
            ans = (p + q) * u
            q_ = ("%s and %s share some stickers in the ratio %s. %s gets %d stickers. How many stickers were there altogether?"
                  % (A, B, R(p, q), A, a))
            c = [Nc(q * u), Nc(a * (p + q)), Nc(a + p + q), Nc(a + q)]
            e = ("One part: %d ÷ %d = %d. There are %d + %d = %d parts altogether: %d × %d = <b>%d</b>."
                 % (a, p, u, p, q, p + q, p + q, u, ans))
            its.append(mcq(q_, Nc(ans), c, e))
    assert len(its) == 20, len(its)
    return {"title": "Unequal sharing with bar models", "items": its}


# ============================================================ set 5: SATs-style word problems
def set_words(rnd, P):
    its = []

    def add(q, right, c, e):
        its.append(mcq(q, right, c, e))

    ml = lambda v: Nc(v, " ml")
    km = lambda v: Nc(v, " km")
    cm = lambda v: Nc(v, " cm")
    # paint (3)
    nm, he, his = P.next()
    add("To make green paint, %s mixes blue paint and yellow paint in the ratio 2 : 3. %s uses 400 ml of blue paint. "
        "How much yellow paint does %s need?" % (nm, cap(he), he), ml(600), [ml(401), ml(1200), ml(200), ml(1000)],
        "400 ml is 2 parts, so 1 part is 400 ÷ 2 = 200 ml. Yellow is 3 parts: 3 × 200 = <b>600 ml</b>. "
        "Adding 1 (401 ml) keeps the difference, not the ratio.")
    add("Orange paint is made by mixing red paint and yellow paint in the ratio 1 : 4. "
        "A teacher makes 2 litres of orange paint. How much red paint does she use?", ml(400), [ml(500), ml(1600), ml(2000), ml(200)],
        "2 litres = 2,000 ml. There are 1 + 4 = 5 parts, so 1 part is 2,000 ÷ 5 = 400 ml. Red is 1 part: <b>400 ml</b>. "
        "Dividing by 4 (500 ml) forgets the red part.")
    nm, he, his = P.next()
    add("Grey paint is made by mixing black paint and white paint in the ratio 1 : 5. %s has 150 ml of black paint and uses all of it. "
        "How much grey paint can %s make?" % (nm, he), ml(900), [ml(750), ml(155), ml(30), ml(156)],
        "White: 5 × 150 = 750 ml. Grey paint is the black and the white together: 150 + 750 = <b>900 ml</b>.")
    # maps (4)
    add("On a map, 1 cm represents 5 km. Two towns are 7 cm apart on the map. How far apart are they in real life?",
        km(35), [km(12), Nc(F(7, 5), " km"), km(75)],
        "Each centimetre stands for 5 km. 7 × 5 = <b>35 km</b>. Do not add (7 + 5) or divide (7 ÷ 5).")
    add("On a map, 1 cm represents 5 km. A lake is 40 km from a village. How far is this on the map?",
        cm(8), [cm(200), cm(35), cm(4), cm(45)],
        "Every 5 km is 1 cm on the map. 40 ÷ 5 = <b>8 cm</b>. Multiplying (40 × 5 = 200) gives a map bigger than the real distance.")
    add("On a map, 1 cm represents 250 m. A footpath is 6 cm long on the map. How long is the real footpath in kilometres?",
        Nc(F(3, 2), " km"), [km(1500), km(15), Nc(F(15, 100), " km")],
        "6 × 250 m = 1,500 m. There are 1,000 m in 1 km, so 1,500 m = <b>1.5 km</b>.")
    add("On a map, 2 cm represents 3 km. Two villages are 10 cm apart on the map. How far apart are they in real life?",
        km(15), [km(11), km(30), km(5), km(20)],
        "10 cm is 10 ÷ 2 = 5 lots of 2 cm. Each lot is 3 km: 5 × 3 = <b>15 km</b>. "
        "10 + 1 = 11 km adds instead of multiplying.")
    # sweets (3)
    (A, _, _), (B, _, _) = P.two()
    add("%s and %s share 45 sweets in the ratio 4 : 5. How many sweets does %s get?" % (A, B, B),
        Nc(25, " sweets"), [Nc(9, " sweets"), Nc(20, " sweets"), Nc(5, " sweets"), Nc(11, " sweets")],
        "4 + 5 = 9 parts. One part is 45 ÷ 9 = 5. %s gets 5 parts: 5 × 5 = <b>25 sweets</b>. "
        "45 ÷ 5 = 9 divides by the wrong number." % B)
    add("In a bag of sweets, for every 3 red sweets there are 4 green sweets. There are 21 red sweets. "
        "How many sweets are in the bag altogether?", Nc(49, " sweets"), [Nc(28, " sweets"), Nc(22, " sweets"), Nc(7, " sweets"), Nc(25, " sweets")],
        "21 ÷ 3 = 7 groups. Each group has 3 + 4 = 7 sweets: 7 × 7 = <b>49 sweets</b>. 28 is only the green sweets.")
    (A, _, _), (B, _, _) = P.two()
    add("%s has 3 times as many sweets as %s. Together they have 48 sweets. How many sweets does %s have?" % (A, B, A),
        Nc(36, " sweets"), [Nc(16, " sweets"), Nc(12, " sweets"), Nc(24, " sweets"), Nc(45, " sweets")],
        "The ratio is 3 : 1, so there are 4 equal parts. One part: 48 ÷ 4 = 12. %s has 3 × 12 = <b>36 sweets</b>. "
        "48 ÷ 3 = 16 forgets %s’s part." % (A, B))
    # recipes (2)
    add("A recipe for 12 flapjacks uses 150 g of oats. How many grams of oats are needed for 18 flapjacks?",
        Nc(225, " g"), [Nc(156, " g"), Nc(2700, " g"), Nc(300, " g"), Nc(100, " g")],
        "18 is 12 + 6, and 6 is half of 12. So add half of 150 g: 150 + 75 = <b>225 g</b>. "
        "(Or: 150 ÷ 12 × 18 = 225.) 156 g adds 6 instead of scaling.")
    add("A pancake recipe for 4 people uses 300 ml of milk. Ruby makes pancakes for 10 people. How much milk does she need?",
        ml(750), [ml(306), ml(3000), ml(600), ml(120)],
        "For 1 person: 300 ÷ 4 = 75 ml. For 10 people: 75 × 10 = <b>750 ml</b>.")
    # prices (2)
    add("3 notebooks cost £2.40. How much do 5 notebooks cost?", Pc(400, False), [Pc(80), Pc(1200, False), Pc(242, False), Pc(480, False)],
        "1 notebook costs £2.40 ÷ 3 = 80p. 5 notebooks cost 5 × 80p = <b>£4.00</b>.")
    add("4 bananas cost 96p. How much do 7 bananas cost?", Pc(168), [Pc(24), Pc(672), Pc(99)],
        "1 banana costs 96p ÷ 4 = 24p. 7 bananas cost 7 × 24p = 168p = <b>£1.68</b>.")
    # similar shapes in context (2)
    add("A photo is 10 cm wide and 15 cm tall. It is enlarged so that it is 30 cm wide. How tall is the enlarged photo?",
        cm(45), [cm(35), cm(30), cm(3), cm(25)],
        "30 ÷ 10 = 3, so the scale factor is 3. Height: 15 × 3 = <b>45 cm</b>. 15 + 20 = 35 cm adds instead of multiplying.")
    add("A toy lorry is 12 cm long. The real lorry is 50 times as long. How long is the real lorry in metres?",
        Nc(6, " m"), [Nc(600, " m"), Nc(62, " m"), Nc(60, " m"), Nc(F(6, 10), " m")],
        "12 × 50 = 600 cm. There are 100 cm in 1 m, so 600 cm = <b>6 m</b>.")
    # class ratios (2)
    add("In a class of 36 pupils, the ratio of boys to girls is 4 : 5. How many more girls than boys are there?",
        Nc(4, " more girls"), [Nc(1, " more girl"), Nc(20, " more girls"), Nc(9, " more girls"), Nc(16, " more girls")],
        "4 + 5 = 9 parts, so one part is 36 ÷ 9 = 4. Boys: 4 × 4 = 16. Girls: 5 × 4 = 20. 20 − 16 = <b>4 more girls</b>.")
    add("In a school choir, the ratio of adults to children is 2 : 7. There are 63 people in the choir. How many children are there?",
        Nc(49, " children"), [Nc(14, " children"), Nc(9, " children"), Nc(7, " children"), Nc(56, " children")],
        "2 + 7 = 9 parts, so one part is 63 ÷ 9 = 7. Children: 7 × 7 = <b>49 children</b>. 14 is the number of adults.")
    # two-step (2)
    (A, _, _), (B, _, _) = P.two()
    add("%s and %s share some sweets in the ratio 3 : 5. %s gets 12 more sweets than %s. How many sweets are there altogether?" % (A, B, B, A),
        Nc(48, " sweets"), [Nc(24, " sweets"), Nc(96, " sweets"), Nc(30, " sweets"), Nc(20, " sweets")],
        "%s has 5 − 3 = 2 more parts. 2 parts are 12, so one part is 6. Altogether: 8 parts × 6 = <b>48 sweets</b>. "
        "96 uses 12 as one part." % B)
    add("A bag has red beads and blue beads in the ratio 2 : 7. There are 35 more blue beads than red beads. How many red beads are there?",
        Nc(14, " red beads"), [Nc(5, " red beads"), Nc(49, " red beads"), Nc(70, " red beads"), Nc(10, " red beads")],
        "Blue has 7 − 2 = 5 more parts. 5 parts are 35, so one part is 7. Red is 2 parts: 2 × 7 = <b>14 red beads</b>.")
    assert len(its) == 20, len(its)
    return {"title": "Ratio and proportion word problems (SATs style)", "items": its}


# ============================================================ lesson
def body_html():
    pic = shapes_svg(["c", "s", "s", "c", "s", "s", "c", "s", "s"])
    sim = similar_svg("rect", (3, 2), (9, 6), (("3 cm", "2 cm"), ("9 cm", "6 cm")))
    bar = bar_svg([("Amelia", 2, "£12", "£24", FILL_L), ("Jack", 3, "£12", "£36", "#fde7bd")], "£60",
                  "bar model: Amelia to Jack is 2 : 3, total £60, each part £12")
    return (
        "<h2>What is a ratio?</h2>"
        "<p>A <b>ratio</b> compares one amount with another. We write it with a colon: <b>a : b</b>. "
        "We say it with “for every … there are …”.</p>"
        "<figure class='sn-fig'>" + pic + "<figcaption>3 circles and 6 squares. Circles : squares = 3 : 6 = 1 : 2. "
        "For every 1 circle there are 2 squares.</figcaption></figure>"
        "<p><b>Order matters.</b> Circles to squares is 1 : 2. Squares to circles is 2 : 1.</p>"
        "<p>To simplify a ratio, divide <b>both</b> numbers by the same number, just like a fraction.</p>"
        "<h2>Ratio and fractions</h2>"
        "<p>Add the numbers in the ratio to find the whole. If red : blue = 3 : 2, every group has 3 + 2 = 5 counters, so "
        + fr(3, 5) + " of the counters are red and " + fr(2, 5) + " are blue.</p>"
        + table(["Ratio red : blue", "Red as a fraction of all", "Blue as a fraction of all"], [
            ["3 : 2", fr(3, 5), fr(2, 5)],
            ["1 : 4", fr(1, 5), fr(4, 5)],
            ["5 : 3", fr(5, 8), fr(3, 8)],
        ])
        + "<h2>Proportion: scaling up and down</h2>"
        "<p>When amounts are in proportion, you <b>multiply or divide</b> them all by the same number. You never add.</p>"
        + ex("Example", "A recipe for 4 people needs 300 g of flour. How much flour is needed for 6 people?",
             "Find 1 person first: 300 ÷ 4 = 75 g. Then 6 people: 75 × 6 = 450 g.", "450 g")
        + "<h2>Scale factors and similar shapes</h2>"
        "<p>An <b>enlargement</b> multiplies every length by the same <b>scale factor</b>. "
        "The new shape is <b>similar</b>: the same shape, a different size. The angles do not change.</p>"
        "<figure class='sn-fig'>" + sim + "<figcaption>Rectangle B is rectangle A enlarged by scale factor 3: "
        "3 × 3 = 9 cm and 2 × 3 = 6 cm.</figcaption></figure>"
        + ex("Example", "Find the scale factor from a 4 cm side to a 20 cm side.", "Divide the new length by the old length: 20 ÷ 4 = 5.", "scale factor 5")
        + "<h2>Sharing in a ratio</h2>"
        "<p>Draw a <b>bar model</b> with one box for each part. Every box is worth the same.</p>"
        + ex("Example", "Amelia and Jack share £60 in the ratio 2 : 3. How much does each get?",
             "2 + 3 = 5 equal parts. £60 ÷ 5 = £12 in each part. Amelia: 2 × £12 = £24. Jack: 3 × £12 = £36.",
             "Amelia £24, Jack £36")
        + "<figure class='sn-fig'>" + bar + "<figcaption>5 equal parts make £60, so each part is £12. "
        "Check: £24 + £36 = £60.</figcaption></figure>"
        "<p>“3 times as many boys as girls” means boys : girls = 3 : 1. That is 4 parts, not 3.</p>"
        "<h2>Common mistakes</h2>"
        + table(["Mistake", "What to do instead"], [
            ["Writing red : blue = 3 : 2 as the fraction " + fr(3, 2) + " or " + fr(2, 3),
             "Add the parts to find the whole: red is " + fr(3, 5) + " of all"],
            ["Adding instead of multiplying: 3 cm enlarged by scale factor 3 is 6 cm",
             "Multiply: 3 cm × 3 = 9 cm"],
            ["Sharing £60 in 2 : 3 by working out £60 ÷ 2 and £60 ÷ 3",
             "Add the parts first: 2 + 3 = 5, so one part is £60 ÷ 5 = £12"],
            ["Writing the ratio the wrong way round",
             "The first thing named goes first: boys to girls is boys : girls"],
            ["“3 times as many” shared into 3 parts",
             "3 times as many is 3 : 1, which is 3 + 1 = 4 parts"],
        ])
    )


FAQ = [
    {"q": "What is ratio and proportion in Year 6?",
     "a": "Year 6 is the first year that ratio appears in the National Curriculum. Children use the a : b notation, scale recipes up and down, use scale factors with similar shapes and share amounts in a given ratio."},
    {"q": "How do you share an amount in a ratio?",
     "a": "Add the numbers in the ratio to find the number of equal parts, divide the amount by that number, then multiply. For £60 in the ratio 2 : 3: 60 ÷ 5 = 12, so the shares are £24 and £36."},
    {"q": "What is a scale factor?",
     "a": "A scale factor tells you how many times bigger an enlarged shape is. Every length is multiplied by it, so a 3 cm by 5 cm rectangle enlarged by scale factor 3 becomes 9 cm by 15 cm."},
    {"q": "Is ratio tested in the Year 6 SATs?",
     "a": "Yes. Ratio and proportion is part of the Year 6 curriculum, so it can come up in the KS2 SATs, usually as word problems in the reasoning papers (Papers 2 and 3), such as recipes, maps and sharing."},
]


def gen():
    rnd = random.Random(6612)
    P = People(rnd)
    sets = [set_pictures(rnd), set_scaling(rnd, P), set_scale(rnd), set_sharing(rnd, P), set_words(rnd, P)]
    for s in sets:
        rnd.shuffle(s["items"])
    balance(sets, rnd)
    seen = set()
    for s in sets:
        assert len(s["items"]) == 20, (s["title"], len(s["items"]))
        cnt = [0, 0, 0, 0]
        for it in s["items"]:
            assert len(set(it["c"])) == 4, it
            assert it["q"] not in seen, it["q"]
            seen.add(it["q"])
            cnt[it["a"]] += 1
        assert cnt == [5, 5, 5, 5], (s["title"], cnt)
    return {
        "country": "uk", "subject": "maths", "grade": "year-6", "slug": "ratio-and-proportion", "sort": 12,
        "updated": UPDATED, "pdf_url": "",
        "title": "Year 6 Ratio and Proportion",
        "seo_title": "Year 6 Ratio and Proportion Worksheets: Scaling, Scale Factors and Sharing in a Ratio (Free, with Answers)",
        "short_title": "Ratio and proportion",
        "domain": "Ratio and proportion",
        "standard_code": "Year 6: Ratio and proportion",
        "standard_url": "https://www.gov.uk/government/publications/national-curriculum-in-england-mathematics-programmes-of-study",
        "standard_text": "Solve problems involving the relative sizes of two quantities where missing values can be found by using integer multiplication and division facts; solve problems involving similar shapes where the scale factor is known or can be found; solve problems involving unequal sharing and grouping using knowledge of fractions and multiples.",
        "meta_desc": "Free Year 6 ratio and proportion worksheets for the National Curriculum: write ratios as a : b, link ratios and fractions, scale recipes, use scale factors with similar shapes, share in a ratio with bar models and solve SATs-style problems. 100 questions with an answer key.",
        "key_big": "Ratio 2 : 3 means 2 + 3 = 5 equal parts. Find one part, then multiply.",
        "key_sub": "Share £60 in the ratio 2 : 3: £60 ÷ 5 = £12, so £24 and £36. Red : blue = 3 : 2 means 3/5 are red. In proportion and enlargements, multiply or divide — never add.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    mark_large(u, "(bar model|similar shapes|shapes picture)")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
