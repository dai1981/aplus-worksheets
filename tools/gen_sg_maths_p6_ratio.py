# -*- coding: utf-8 -*-
"""
Singapore Primary 6 Maths: Ratio (MOE 2021 Primary Mathematics Syllabus, Standard, Primary 6: Ratio)
  python3 tools/gen_sg_maths_p6_ratio.py
Writing ratios a : b and a : b : c from pictures and words, equivalent ratios, simplest form and
missing terms, ratio and fraction, dividing a quantity in a ratio with bar models (units),
and PSLE-style multi-step word problems (before and after, constant total, constant difference).
Wrong answers come from real mistakes: reversed order, part-to-part read as part-to-whole,
adding instead of multiplying, dividing the total by one term of the ratio, one unit only.
Every choice carries its value; no two choices are equal in value.
HTML attributes use single quotes (no backslashes in the JSON). Singapore English.
"""
import json, math, os, random, re
from fractions import Fraction as F
from math import gcd

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "sg", "maths", "primary-6")
UPDATED = "2026-11-03"
NBSP = " "
GREEN = "#2e7d4f"
FILL = "#4fae74"
FILL_L = "#cfe6d6"
FILL2 = "#f2b84b"
FILL2_E = "#a8761a"
FILL3 = "#bcd4f0"
RED = "#c0392b"
INK = "#2b2b2b"
FONT = "Arial, Helvetica, sans-serif"
GIRLS = ["Siti", "Nurul", "Farah", "Mei Ling", "Hui Min", "Xin Yi", "Priya", "Devi", "Kavya", "Chloe", "Sarah"]
BOYS = ["Ali", "Ahmad", "Hafiz", "Wei Ming", "Jun Jie", "Zhi Hao", "Raju", "Kumar", "Arjun", "Ethan", "Ryan"]


# ------------------------------------------------------------ numbers and choices
def num(x):
    """Exact decimal text; 5 or more digits grouped with a no-break space."""
    x = F(x)
    assert x >= 0, x
    d, k = x.denominator, 0
    while (10 ** k) % d:
        k += 1
        assert k < 8, x
    v = x.numerator * (10 ** k // d)
    i, r = divmod(v, 10 ** k)
    s = str(i) if i < 10000 else "{:,}".format(i).replace(",", NBSP)
    if r:
        s += "." + str(r).zfill(k).rstrip("0")
    return s


def money(x):
    """x in dollars: $45, $2.40, 85¢ under $1."""
    c = F(x) * 100
    assert c.denominator == 1 and c > 0, x
    c = int(c)
    if c < 100:
        return "%d¢" % c
    if c % 100:
        return "$%s.%02d" % (num(c // 100), c % 100)
    return "$" + num(c // 100)


def R(*t):
    return " : ".join(num(x) for x in t)


def rv(*t):
    g = 0
    for x in t:
        g = gcd(g, x)
    return ("ratio",) + tuple(x // g for x in t)


def Rc(*t):
    return (R(*t), rv(*t))


def fr(a, b):
    return "<span class='fr'><span class='fn'>%s</span><span class='fd'>%s</span></span>" % (a, b)


def Fc(a, b):
    return (fr(a, b), F(a, b))


def Nc(n, u=""):
    return ("%s%s" % (num(n), u), F(n))


def Mc(x):
    return (money(x), F(x))


def plain(s):
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", s)).strip()


def mcq(q, right, cands, e):
    """right / cands are (html, value). The first 3 usable wrong choices are kept: positive, and
    different in text and in value from the answer and from each other. Answer stored at 0."""
    seen, vals, pick = {plain(right[0])}, {right[1]}, []
    for c in cands:
        if c is None:
            continue
        s, v = c
        if plain(s) in seen or v in vals:
            continue
        if isinstance(v, F) and v <= 0:
            continue
        if isinstance(v, tuple) and min(v[1:]) <= 0:
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
        self.rnd = rnd
        self.pool = [(n, "she", "her") for n in GIRLS] + [(n, "he", "his") for n in BOYS]
        rnd.shuffle(self.pool)
        self.i = 0

    def next(self):
        if self.i == len(self.pool):
            last = self.pool[-1]
            while True:
                self.rnd.shuffle(self.pool)
                if self.pool[0] != last:
                    break
            self.i = 0
        p = self.pool[self.i]
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
    return (len(t) - t.count(" ") * 0.3 - t.count(".") * 0.5) * fs * 0.6


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
            % (cx, cy - 11, cx + 12, cy + 10, cx - 12, cy + 10, FILL3, "#2f5d8a"))


def shapes_svg(kinds):
    """Shapes in order, one row up to 9, otherwise two rows."""
    n = len(kinds)
    per = n if n <= 9 else (n + 1) // 2
    cell = 32
    rows = (n + per - 1) // per
    body = []
    for i, k in enumerate(kinds):
        r, c = divmod(i, per)
        body.append(shape(k, 4 + cell * c + cell / 2, 4 + cell * r + cell / 2))
    counts = [unit(kinds.count(k), *SHAPE_NAMES[k]) for k in "cst" if kinds.count(k)]
    return svg_wrap(8 + cell * per, 8 + cell * rows, "".join(body), "shapes picture: " + " and ".join(counts))


ROWCOL = [FILL_L, "#fde7bd", FILL3]


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


def bars(names, parts, total=None, ask=None, cells=None, rights=None):
    """Bar model for a ratio; ask = index of the row whose value is asked ('?' on the right)."""
    rows = []
    for i, (nm, p) in enumerate(zip(names, parts)):
        r = "?" if ask == i else (rights[i] if rights else "")
        rows.append((nm, p, cells[i] if cells else "", r, ROWCOL[i % 3]))
    lab = "bar model: %s is %s" % (" to ".join(names), R(*parts))
    if total:
        lab += ", total %s" % total
    return fig(bar_svg(rows, total, lab))


# ============================================================ set 1: writing ratios
def set_writing(rnd):
    its = []
    used = set()

    def draw(cnt):
        kinds = []
        for k, m in zip("cst", cnt):
            kinds += [k] * m
        rnd.shuffle(kinds)
        return fig(shapes_svg(kinds))

    def counts2():
        while True:
            a, b = rnd.randint(2, 8), rnd.randint(2, 8)
            if a != b and gcd(a, b) == 1 and a + b <= 14 and (a, b) not in used:
                used.add((a, b))
                return a, b

    # 1) two kinds, order matters (5)
    for i in range(5):
        a, b = counts2()
        t = a + b
        if i % 2 == 0:
            q = "What is the ratio of the number of circles to the number of squares?"
            right, c = Rc(a, b), [Rc(b, a), Rc(a, t), Rc(t, b), Rc(b, t)]
            e = ("Count: %d circles and %d squares. Circles are named first, so %d comes first: <b>%s</b>. "
                 "%s would be squares to circles." % (a, b, a, R(a, b), R(b, a)))
        else:
            q = "What is the ratio of the number of squares to the number of circles?"
            right, c = Rc(b, a), [Rc(a, b), Rc(b, t), Rc(t, a), Rc(a, t)]
            e = ("Count: %d squares and %d circles. Squares are named first, so %d comes first: <b>%s</b>. "
                 "%s would be circles to squares." % (b, a, b, R(b, a), R(a, b)))
        its.append(mcq(draw((a, b, 0)) + q, right, c, e))

    # 2) one kind to all the shapes (3)
    for i in range(3):
        a, b = counts2()
        t = a + b
        if i < 2:
            q = "What is the ratio of the number of circles to the total number of shapes?"
            right, c = Rc(a, t), [Rc(a, b), Rc(t, a), Rc(b, t), Rc(b, a)]
            e = ("There are %d + %d = %d shapes altogether. Circles to all the shapes is <b>%s</b>. "
                 "%s compares circles with squares only." % (a, b, t, R(a, t), R(a, b)))
        else:
            q = "What is the ratio of the total number of shapes to the number of squares?"
            right, c = Rc(t, b), [Rc(b, t), Rc(a, b), Rc(t, a), Rc(b, a)]
            e = ("There are %d + %d = %d shapes altogether and %d squares. The total is named first: <b>%s</b>."
                 % (a, b, t, b, R(t, b)))
        its.append(mcq(draw((a, b, 0)) + q, right, c, e))

    # 3) three kinds, a : b : c (5)
    ORD = [("t", "c", "s"), ("s", "t", "c"), ("c", "s", "t"), ("s", "c", "t"), ("t", "s", "c")]
    used3 = set()
    for order in ORD:
        while True:
            cnt = {"c": rnd.randint(1, 6), "s": rnd.randint(1, 6), "t": rnd.randint(1, 6)}
            v = tuple(cnt[k] for k in "cst")
            g = gcd(gcd(v[0], v[1]), v[2])
            ans = tuple(cnt[k] for k in order)
            if (len(set(v)) == 3 and g == 1 and sum(v) <= 15 and min(v) >= 2 and v not in used3
                    and ans not in used3):
                used3.add(v)
                used3.add(ans)
                break
        x, y, z = (cnt[k] for k in order)
        names = [SHAPE_NAMES[k][1] for k in order]
        q = "What is the ratio of the number of %s to the number of %s to the number of %s?" % tuple(names)
        c = [Rc(z, y, x), Rc(y, x, z), Rc(x, z, y), Rc(cnt["c"], cnt["s"], cnt["t"]), Rc(x, y, x + y + z)]
        e = ("Count each shape: %s, %s and %s. Write the numbers in the same order as the words: <b>%s</b>."
             % tuple([unit(n, *SHAPE_NAMES[k]) for n, k in zip((x, y, z), order)] + [R(x, y, z)]))
        its.append(mcq(draw((cnt["c"], cnt["s"], cnt["t"])) + q, Rc(x, y, z), c, e))

    # 4) words, two quantities (4)
    W2 = [("In a CCA group, there are %d boys and %d girls.", "girls", "boys", True),
          ("At a hawker stall, %d plates of chicken rice and %d plates of laksa were sold in an hour.",
           "laksa", "chicken rice", True),
          ("A class library has %d storybooks and %d comics.", "storybooks", "comics", False),
          ("At a void deck, %d adults and %d children are waiting for a bus.", "children", "all the people", "all")]
    for tmpl, X, Y, rev in W2:
        while True:
            a, b = rnd.randint(7, 25), rnd.randint(7, 25)
            if a != b and gcd(a, b) == 1:
                break
        t = a + b
        if rev == "all":
            q = (tmpl % (a, b)) + " What is the ratio of the number of children to the total number of people?"
            right, c = Rc(b, t), [Rc(b, a), Rc(t, b), Rc(a, t), Rc(a, b)]
            e = "There are %d + %d = %d people. Children to all the people is <b>%s</b>." % (a, b, t, R(b, t))
        elif rev:
            unitw = "plates of " if X == "laksa" else ""
            q = (tmpl % (a, b)) + " What is the ratio of the number of %s%s to the number of %s%s?" % (unitw, X, unitw, Y)
            right, c = Rc(b, a), [Rc(a, b), Rc(b, t), Rc(a, t), Rc(t, b)]
            e = ("The question names %s first, so write %d first: <b>%s</b>. "
                 "Do not copy the numbers in the order they appear in the sentence." % (X, b, R(b, a)))
        else:
            q = (tmpl % (a, b)) + " What is the ratio of the number of %s to the number of %s?" % (X, Y)
            right, c = Rc(a, b), [Rc(b, a), Rc(a, t), Rc(t, a), Rc(b, t)]
            e = "%s are named first, so write %d first: <b>%s</b>." % (cap(X), a, R(a, b))
        its.append(mcq(q, right, c, e))

    # 5) words, three quantities (3)
    W3 = [("Mdm Wong bought %d kg of rice, %d kg of sugar and %d kg of flour.",
           "What is the ratio of the mass of sugar to the mass of flour to the mass of rice?", (1, 2, 0)),
          ("At the Singapore Zoo, a class counted %d monkeys, %d otters and %d tortoises.",
           "What is the ratio of the number of tortoises to the number of monkeys to the number of otters?", (2, 0, 1)),
          ("For National Day, Mr Tan bought %d red balloons, %d white balloons and %d gold balloons.",
           "What is the ratio of the number of white balloons to the number of gold balloons to the number of red balloons?", (1, 2, 0))]
    for tmpl, ask, order in W3:
        while True:
            v = (rnd.randint(2, 11), rnd.randint(2, 11), rnd.randint(2, 11))
            if len(set(v)) == 3 and gcd(gcd(v[0], v[1]), v[2]) == 1:
                break
        x, y, z = (v[k] for k in order)
        c = [Rc(*v), Rc(z, y, x), Rc(y, x, z), Rc(x, z, y)]
        e = ("Write the amounts in the order the question asks for them: %d, %d and %d. The answer is <b>%s</b>, not %s "
             "(the order in the first sentence)." % (x, y, z, R(x, y, z), R(*v)))
        its.append(mcq((tmpl % v) + " " + ask, Rc(x, y, z), c, e))

    assert len(its) == 20, len(its)
    return {"title": "Writing ratios a : b and a : b : c", "items": its}


# ============================================================ set 2: equivalent ratios, simplest form, missing terms
def set_equivalent(rnd):
    its = []
    seen = set()

    def pq(lo=2, hi=9, maxsum=15):
        while True:
            p, q = coprime_pair(rnd, lo, hi, maxsum)
            if (p, q) not in seen:
                seen.add((p, q))
                return p, q

    # 1) simplest form a : b (4)
    for g in [6, 4, 9, 8]:
        while True:
            p, q = pq()
            if p * g <= 96 and q * g <= 96:
                break
        a, b = p * g, q * g
        c = [Rc(q, p), Rc(p, b), Rc(a, q), Rc(a - (g - 1), b - (g - 1)), Rc(p + 1, q + 1)]
        its.append(mcq("Express %s in its simplest form." % R(a, b), Rc(p, q), c,
                       "The highest common factor of %d and %d is %d. Divide <b>both</b> terms by %d: "
                       "%d ÷ %d = %d and %d ÷ %d = %d, so the answer is <b>%s</b>."
                       % (a, b, g, g, a, g, p, b, g, q, R(p, q))))

    # 2) simplest form a : b : c (4)
    for (p, q, r), g in [((2, 3, 5), 4), ((3, 1, 4), 6), ((4, 5, 2), 3), ((5, 2, 3), 7)]:
        a, b, cc = p * g, q * g, r * g
        c = [Rc(r, q, p), Rc(p, q, cc), Rc(a, q, r), Rc(q, p, r)]
        its.append(mcq("Express %s in its simplest form." % R(a, b, cc), Rc(p, q, r), c,
                       "%d is a factor of all three terms, and it is the largest one. Divide <b>every</b> term by %d: "
                       "<b>%s</b>. Keep the terms in the same order." % (g, g, R(p, q, r))))

    # 3) which ratio is equivalent? (2)
    for p, q, k in [(3, 5, 4), (2, 7, 3)]:
        c = [Rc(p + k, q + k), Rc(q * k, p * k), Rc(p * k, q * (k + 1)), Rc(p * k, q + k)]
        its.append(mcq("Which ratio is equivalent to %s?" % R(p, q), Rc(p * k, q * k), c,
                       "Multiply <b>both</b> terms by the same number: %d × %d = %d and %d × %d = %d, so %s = <b>%s</b>. "
                       "Adding %d to both terms (%s) does not give an equivalent ratio."
                       % (p, k, p * k, q, k, q * k, R(p, q), R(p * k, q * k), k, R(p + k, q + k))))

    # 4) missing terms (8)
    def miss_second(p, q, k):
        given, ans = k * p, k * q
        c = [Nc(q + given - p), Nc(k), Nc(given), Nc(q * given), Nc(ans + q)]
        e = ("%d × %d = %d, so multiply the second term by %d too: %d × %d = <b>%d</b>. "
             "Adding %d to %d gives %d, which does not keep the ratio." % (p, k, given, k, q, k, ans, given - p, q, q + given - p))
        its.append(mcq("Find the missing term. %s = %s : ?" % (R(p, q), num(given)), Nc(ans), c, e))

    def miss_first(p, q, k):
        given, ans = k * q, k * p
        c = [Nc(p + given - q) if given > q else None, Nc(k), Nc(given), Nc(p * given), Nc(ans + p)]
        e = ("%d × %d = %d, so multiply the first term by %d too: %d × %d = <b>%d</b>."
             % (q, k, given, k, p, k, ans))
        its.append(mcq("Find the missing term. %s = ? : %s" % (R(p, q), num(given)), Nc(ans), c, e))

    for _ in range(2):
        p, q = pq()
        miss_second(p, q, rnd.randint(3, 8))
    for _ in range(2):
        p, q = pq()
        miss_first(p, q, rnd.randint(3, 8))
    # dividing
    p, q = pq()
    k = 6
    its.append(mcq("Find the missing term. %s = %d : ?" % (R(p * k, q * k), p), Nc(q),
                   [Nc(q * k - (p * k - p)) if q * k > p * k - p else None, Nc(q * k), Nc(k), Nc(p * q), Nc(q + k)],
                   "%d ÷ %d = %d, so divide the second term by %d too: %d ÷ %d = <b>%d</b>."
                   % (p * k, k, p, k, q * k, k, q)))
    # three terms
    its.append(mcq("Find the missing term. %s = 12 : ? : 28" % R(3, 5, 7), Nc(20),
                   [Nc(14), Nc(4), Nc(35), Nc(21)],
                   "12 ÷ 3 = 4 and 28 ÷ 7 = 4, so every term is multiplied by 4. 5 × 4 = <b>20</b>. "
                   "14 comes from adding 9 to 5 (12 − 3 = 9)."))
    assert F(12, 3) == F(28, 7) == F(20, 5)
    # non-whole scale factor: simplify first
    for a, b, c_, ans in [(4, 6, 10, 15), (6, 9, 8, 12)]:
        assert F(a, b) == F(c_, ans)
        g = gcd(a, b)
        its.append(mcq("Find the missing term. %s = %s : ?" % (R(a, b), num(c_)), Nc(ans),
                       [Nc(b + c_ - a), Nc(c_ * (b // g)), Nc(c_ * b)],
                       "%d is not a multiple of %d, so simplify first: %s = %s. %d ÷ %d = %d, so the missing term is "
                       "%d × %d = <b>%d</b>." % (c_, a, R(a, b), R(a // g, b // g), c_, a // g, c_ // (a // g),
                                                 b // g, c_ // (a // g), ans)))
    # units (2)
    its.append(mcq("Express 2 m : 80 cm in its simplest form.", Rc(5, 2),
                   [Rc(1, 40), Rc(2, 5), Rc(1, 4), Rc(5, 8)],
                   "Change to the same unit first: 2 m = 200 cm. 200 : 80 = <b>5 : 2</b> (divide both by 40). "
                   "1 : 40 comes from 2 : 80 without changing the units."))
    its.append(mcq("Express 1 ℓ 200 ml : 800 ml in its simplest form.", Rc(3, 2),
                   [Rc(2, 3), Rc(1, 4), Rc(3, 5), Rc(1, 800)],
                   "Change to the same unit first: 1 ℓ 200 ml = 1200 ml. 1200 : 800 = <b>3 : 2</b> (divide both by 400). "
                   "1 : 4 comes from forgetting the 1 ℓ."))
    assert len(its) == 20, len(its)
    return {"title": "Equivalent ratios, simplest form and missing terms", "items": its}


# ============================================================ set 3: ratio and fraction
def set_fraction(rnd, P):
    its = []
    seen = set()

    def pq(maxsum=12, ok=lambda p, q: True):
        while True:
            p, q = coprime_pair(rnd, 1, 9, maxsum)
            if (p, q) not in seen and p > 1 and q > 1 and ok(p, q):
                seen.add((p, q))
                return p, q

    # 1) from a bar model (3)
    for i in range(3):
        p, q = pq(11)
        (A, _, _), (B, _, _) = P.two()
        F_ = bars([A, B], [p, q])
        if i < 2:
            right, c = Fc(q, p + q), [Fc(q, p), Fc(p, p + q), Fc(p, q), Fc(1, q)]
            e = ("%s has %d units and %s has %d units, so the total is %d + %d = %d units. "
                 "%s has %d of the %d units: <b>%s</b>." % (A, p, B, q, p, q, p + q, B, q, p + q, fr(q, p + q)))
            qq = "The model shows the ratio of %s’s stickers to %s’s stickers. What fraction of all the stickers does %s have?" % (A, B, B)
        else:
            right, c = Fc(p, q), [Fc(p, p + q), Fc(q, p), Fc(q, p + q), Fc(1, q)]
            e = ("%s has %d units and %s has %d units. Compare %s with %s only: <b>%s</b>. "
                 "Do not use the total here." % (A, p, B, q, A, B, fr(p, q)))
            qq = "The model shows the ratio of %s’s stickers to %s’s stickers. %s’s stickers are what fraction of %s’s stickers?" % (A, B, A, B)
        its.append(mcq(F_ + qq, right, c, e))

    CTX = [("boys", "girls", "pupils", "in a choir"), ("red beads", "blue beads", "beads", "in a box"),
           ("adults", "children", "people", "in the queue for the Singapore Flyer"),
           ("durians", "rambutans", "fruits", "at a fruit stall"),
           ("fiction books", "non-fiction books", "books", "in a class library"),
           ("buses", "cars", "vehicles", "in a car park"), ("chicken wings", "satay sticks", "items", "on a barbecue tray"),
           ("blue pens", "black pens", "pens", "in a pencil case"), ("goldfish", "guppies", "fish", "in a tank"),
           ("roses", "orchids", "flowers", "in a garden at Gardens by the Bay"),
           ("cats", "dogs", "animals", "at an animal shelter"), ("apples", "oranges", "fruits", "in a basket")]
    rnd.shuffle(CTX)
    ci = iter(CTX)

    # 2) part of the total (5)
    for i in range(5):
        X, Y, W, pl = next(ci)
        p, q = pq()
        if i < 3:
            right, c = Fc(p, p + q), [Fc(p, q), Fc(q, p + q), Fc(q, p), Fc(1, p)]
            n, who = p, X
        else:
            right, c = Fc(q, p + q), [Fc(q, p), Fc(p, p + q), Fc(p, q), Fc(1, q)]
            n, who = q, Y
        qq = ("%s, the ratio of the number of %s to the number of %s is %s. What fraction of the %s are %s?"
              % (cap(pl), X, Y, R(p, q), W, who))
        e = ("There are %d + %d = %d units in all. %s are %d of the %d units: <b>%s</b>. "
             "%s is wrong: the denominator must be the total, %d units."
             % (p, q, p + q, cap(who), n, p + q, fr(n, p + q), c[0][0], p + q))
        its.append(mcq(qq, right, c, e))

    # 3) one part as a fraction of the other (4)
    for i in range(4):
        X, Y, W, pl = next(ci)
        p, q = pq()
        if i < 3:
            right, c = Fc(p, q), [Fc(p, p + q), Fc(q, p), Fc(q, p + q)]
            qq = ("%s, the ratio of the number of %s to the number of %s is %s. The number of %s is what fraction "
                  "of the number of %s?" % (cap(pl), X, Y, R(p, q), X, Y))
            e = ("%s are %d units and %s are %d units. The number of %s is the whole, so it goes in the denominator: <b>%s</b>. "
                 "Do not use the total here." % (cap(X), p, Y, q, Y, fr(p, q)))
        else:
            right, c = Fc(q, p), [Fc(p, q), Fc(q, p + q), Fc(p, p + q)]
            qq = ("%s, the ratio of the number of %s to the number of %s is %s. The number of %s is what fraction "
                  "of the number of %s?" % (cap(pl), X, Y, R(p, q), Y, X))
            e = ("%s are %d units and %s are %d units. The number of %s is the whole, so it goes in the denominator: <b>%s</b>."
                 % (cap(Y), q, X, p, X, fr(q, p)))
            if q > p:
                e += " The answer can be an improper fraction."
        its.append(mcq(qq, right, c, e))

    # 4) fraction of the other -> ratio (3)
    FA = [("Siti’s savings", "Ali’s savings", "are", 3, 4),
          ("the length of the red ribbon", "the length of the blue ribbon", "is", 5, 8),
          ("the mass of the bag of flour", "the mass of the bag of rice", "is", 2, 7)]
    for A, B, verb, p, q in FA:
        c = [Rc(q, p), Rc(p, p + q), Rc(p, q - p), Rc(q - p, q)]
        qq = "%s %s %s of %s. What is the ratio of %s to %s?" % (cap(A), verb, fr(p, q), B, A, B)
        e = ("Think of %s as %d units. Then %s %s %d units. So the ratio is <b>%s</b>, not %s."
             % (B, q, A, verb, p, R(p, q), R(q, p)))
        its.append(mcq(qq, Rc(p, q), c, e))

    # 5) fraction of the total -> ratio (3)
    for i in range(3):
        X, Y, W, pl = next(ci)
        while True:
            p, q = pq()
            if p != q:
                break
        t = p + q
        if i < 2:
            right, c = Rc(p, q), [Rc(p, t), Rc(q, p), Rc(t, p), Rc(q, t)]
            ask = "the number of %s to the number of %s" % (X, Y)
            e = ("%s means %d units out of %d. The rest are %d − %d = %d units. So the ratio is <b>%s</b>, not %s."
                 % (fr(p, t), p, t, t, p, q, R(p, q), R(p, t)))
        else:
            right, c = Rc(q, p), [Rc(p, q), Rc(q, t), Rc(t, q), Rc(p, t)]
            ask = "the number of %s to the number of %s" % (Y, X)
            e = ("%s means %d units out of %d are %s. The rest, %d − %d = %d units, are %s. "
                 "%s come first, so the ratio is <b>%s</b>." % (fr(p, t), p, t, X, t, p, q, Y, cap(Y), R(q, p)))
        qq = "%s, %s of the %s are %s. The rest are %s. What is the ratio of %s?" % (cap(pl), fr(p, t), W, X, Y, ask)
        its.append(mcq(qq, right, c, e))

    # 6) times as many (2)
    its.append(mcq("Jun Jie has 3 times as many marbles as Wei Ming. What fraction of their marbles does Wei Ming have?",
                   Fc(1, 4), [Fc(1, 3), Fc(3, 4), Fc(1, 2), Fc(3, 1)],
                   "Jun Jie : Wei Ming = 3 : 1, which is 4 units in all. Wei Ming has 1 of the 4 units: <b>" + fr(1, 4) + "</b>. "
                   + fr(1, 3) + " compares Wei Ming with Jun Jie, not with the total."))
    its.append(mcq("The number of girls in a hall is " + fr(2, 3) + " of the number of boys. What fraction of the children are girls?",
                   Fc(2, 5), [Fc(2, 3), Fc(1, 3), Fc(3, 5), Fc(1, 2)],
                   "Girls : boys = 2 : 3, which is 5 units in all. Girls are 2 of the 5 units: <b>" + fr(2, 5) + "</b>."))
    assert len(its) == 20, len(its)
    return {"title": "Ratio and fraction", "items": its}


# ============================================================ set 4: dividing a quantity in a ratio
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

    # 1) share a total in a : b (6)
    THINGS = [("stickers", "sticker"), ("marbles", "marble"), ("stamps", "stamp")]
    for i in range(6):
        askA = i % 2 == 0
        p, q, u = pqu(9, 4, 12, lambda p, q, u: ((p + q) * u) % (p if askA else q) == 0)
        T = (p + q) * u
        (A, _, _), (B, _, _) = P.two()
        n = p if askA else q
        ans = n * u
        who = A if askA else B
        if i < 3:
            fmt = money
            mk = lambda v: Mc(v)
            q_ = "%s and %s shared %s in the ratio %s. How much money did %s get?" % (A, B, money(T), R(p, q), who)
        else:
            many, one = THINGS[i - 3]
            fmt = num
            mk = lambda v, one=one, many=many: (unit(v, one, many), F(v))
            q_ = "%s and %s shared %d %s in the ratio %s. How many %s did %s get?" % (A, B, T, many, R(p, q), many, who)
        F_ = bars([A, B], [p, q], fmt(T), 0 if askA else 1)
        c = [mk(T // n) if T % n == 0 else None, mk((p + q - n) * u), mk(u), mk(ans + u), mk(ans - u)]
        e = ("There are %d + %d = %d units. 1 unit = %s ÷ %d = %s. %s got %d units: %d × %s = <b>%s</b>. "
             "Do not divide %s by %d on its own." % (p, q, p + q, fmt(T), p + q, fmt(u), who, n, n, fmt(u), fmt(ans), fmt(T), n))
        its.append(mcq(F_ + q_, mk(ans), c, e))

    # 2) share in a : b : c (4)
    for (p, q, r), u, ask, kind in [((2, 3, 4), 15, 2, "$"), ((1, 2, 5), 12, 1, "n"), ((3, 4, 5), 8, 0, "n"),
                                    ((2, 5, 3), 7, "diff", "$")]:
        T = (p + q + r) * u
        (A, _, _), (B, _, _) = P.two()
        C = P.next()[0]
        names = [A, B, C]
        if kind == "$":
            fmt, mk = money, (lambda v: Mc(v))
            share = "%s, %s and %s shared %s in the ratio %s." % (A, B, C, money(T), R(p, q, r))
        else:
            fmt, mk = num, (lambda v: Nc(v))
            share = "%s, %s and %s shared %d cards in the ratio %s." % (A, B, C, T, R(p, q, r))
        parts = (p, q, r)
        if ask == "diff":
            d = q - p
            ans = d * u
            qq = share + " How much more money did %s get than %s?" % (B, A)
            c = [mk(q * u), mk(T // d) if T % d == 0 else None, mk(u), mk(T - ans), mk(p * u)]
            e = ("%d + %d + %d = %d units. 1 unit = %s ÷ %d = %s. %s got %d − %d = %d units more: %d × %s = <b>%s</b>."
                 % (p, q, r, p + q + r, fmt(T), p + q + r, fmt(u), B, q, p, d, d, fmt(u), fmt(ans)))
            F_ = bars(names, parts, fmt(T))
        else:
            n = parts[ask]
            ans = n * u
            if kind == "$":
                qq = share + " How much money did %s get?" % names[ask]
            else:
                qq = share + " How many cards did %s get?" % names[ask]
            c = [mk(T // n) if T % n == 0 else None, mk(T // (p + q + r - n)) if T % (p + q + r - n) == 0 else None,
                 mk(u), mk(ans + u), mk((p + q + r - n) * u)]
            e = ("%d + %d + %d = %d units. 1 unit = %s ÷ %d = %s. %s got %d units: %d × %s = <b>%s</b>."
                 % (p, q, r, p + q + r, fmt(T), p + q + r, fmt(u), names[ask], n, n, fmt(u), fmt(ans)))
            F_ = bars(names, parts, fmt(T), ask)
        its.append(mcq(F_ + qq, mk(ans), c, e))

    # 3) one share known (4)
    for i in range(4):
        if i == 0:
            seen.clear()
        p, q, u = pqu(11, 3, 9)
        (A, _, _), (B, _, _) = P.two()
        a = p * u
        if i < 2:
            ans = q * u
            qq = "%s and %s shared some money in the ratio %s. %s got %s. How much money did %s get?" % (
                A, B, R(p, q), A, money(a), B)
            c = [Mc(a + q - p) if a + q - p > 0 else None, Mc(u), Mc((p + q) * u), Mc(a * q)]
            e = ("%s’s %d units are %s, so 1 unit = %s ÷ %d = %s. %s got %d units: %d × %s = <b>%s</b>."
                 % (A, p, money(a), money(a), p, money(u), B, q, q, money(u), money(ans)))
            F_ = bars([A, B], [p, q], None, 1, rights=[money(a), ""])
            its.append(mcq(F_ + qq, Mc(ans), c, e))
        else:
            ans = (p + q) * u
            qq = ("%s and %s shared some beads in the ratio %s. %s got %d beads. How many beads were there altogether?"
                  % (A, B, R(p, q), A, a))
            c = [Nc(q * u), Nc(a * (p + q)), Nc(a + q)]
            e = ("1 unit = %d ÷ %d = %d. There are %d + %d = %d units altogether: %d × %d = <b>%d</b>."
                 % (a, p, u, p, q, p + q, p + q, u, ans))
            F_ = bars([A, B], [p, q], "?", None, rights=[num(a), ""])
            its.append(mcq(F_ + qq, Nc(ans), c, e))

    # 4) difference known (4)
    for i in range(4):
        if i == 0:
            seen.clear()
        p, q, u = pqu(11, 3, 9, lambda p, q, u: q - p >= 2)
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
        F_ = bars([A, B], [p, q])
        qq = "The ratio of the number of %s’s cards to the number of %s’s cards is %s. %s has %d more cards than %s. %s" % (
            A, B, R(p, q), B, d, A, ask)
        e = ("%s has %d − %d = %d more units. %d units = %d, so 1 unit = %d ÷ %d = %d. "
             "%s: %d × %d = %d. %s: %d × %d = %d. Answer: <b>%d</b>."
             % (B, q, p, q - p, q - p, d, d, q - p, u, A, p, u, p * u, B, q, u, q * u, ans))
        its.append(mcq(F_ + qq, Nc(ans), c, e))

    # 5) times as many (2)
    for X, Y, pl, W, k, T, askX in [("adults", "children", "a swimming pool", "people", 4, 45, False),
                                    ("cars", "motorcycles", "a car park", "vehicles", 3, 56, True)]:
        u = T // (k + 1)
        assert u * (k + 1) == T
        ans = k * u if askX else u
        other = u if askX else k * u
        c = [Nc(other), Nc(T // k) if T % k == 0 else None, Nc(u * (k - 1)), Nc(T - k)]
        F_ = bars([cap(X), cap(Y)], [k, 1], str(T), 0 if askX else 1)
        qq = ("In %s, there are %d times as many %s as %s. There are %d %s altogether. How many %s are there?"
              % (pl, k, X, Y, T, W, X if askX else Y))
        e = ("%d times as many means %s : %s = %s, which is %d + 1 = %d units. 1 unit = %d ÷ %d = %d. "
             % (k, X, Y, R(k, 1), k, k + 1, T, k + 1, u))
        e += ("%s: %d × %d = <b>%d</b>." % (cap(X), k, u, ans)) if askX else ("%s: 1 unit = <b>%d</b>." % (cap(Y), ans))
        its.append(mcq(F_ + qq, Nc(ans), c, e))
    assert len(its) == 20, len(its)
    return {"title": "Dividing a quantity in a ratio (model method)", "items": its}


# ============================================================ set 5: PSLE-style word problems
def set_words(rnd, P):
    its = []

    def add(q, right, c, e):
        its.append(mcq(q, right, c, e))

    # 1 difference -> total, with model
    b, g, d = 3, 5, 24
    u = d // (g - b)
    assert u * (g - b) == d
    add(bars(["Boys", "Girls"], [b, g], "?") +
        "The ratio of the number of boys to the number of girls in a school choir is 3 : 5. There are 24 more girls than boys. "
        "How many pupils are there in the choir?", Nc((b + g) * u),
        [Nc(d * (b + g)), Nc(g * u), Nc(d + b + g), Nc(64)],
        "Girls have 5 − 3 = 2 more units. 2 units = 24, so 1 unit = 12. Total: 8 units = 8 × 12 = <b>96</b>.")
    # 2 transfer, total unchanged
    add("Ahmad and Ryan had money in the ratio 5 : 3. After Ahmad gave Ryan $12, they had the same amount of money. "
        "How much money did Ahmad have at first?", Mc(60),
        [Mc(30), Mc(96), Mc(36), Mc(48)],
        "The total stays the same: 5 + 3 = 8 units. Equal shares are 4 units each, so Ahmad gave 5 − 4 = 1 unit. "
        "1 unit = $12. Ahmad at first: 5 × $12 = <b>$60</b>.")
    # 3 one quantity changes
    red, blue, add_r = 2, 5, 18
    u = add_r // (4 - 2)
    add("In a box, the ratio of the number of red beads to the number of blue beads was 2 : 5. Then 18 red beads were added. "
        "The ratio became 4 : 5. How many blue beads are there?", Nc(blue * u),
        [Nc(90), Nc(18), Nc(36), Nc(23)],
        "The blue beads do not change, so they stay at 5 units. Red went from 2 units to 4 units: 2 units = 18, "
        "so 1 unit = 9. Blue: 5 × 9 = <b>45</b>. 90 uses 18 as 1 unit.")
    assert 2 * u + 18 == 4 * u
    # 4 constant difference, ages
    add("The ratio of Siti’s age to her mother’s age is 1 : 4. Her mother is 30 years older than Siti. "
        "In how many years’ time will the ratio of their ages be 1 : 3?", Nc(5, " years"),
        [Nc(10, " years"), Nc(15, " years"), Nc(45, " years")],
        "The difference in age never changes. Now: 3 units = 30, so 1 unit = 10. Siti is 10 and her mother is 40. "
        "Later: 1 : 3 has a difference of 2 units = 30, so 1 unit = 15. Siti will be 15: 15 − 10 = <b>5 years</b>.")
    assert F(10 + 5, 40 + 5) == F(1, 3)
    # 5 three terms, difference -> total, with model
    add(bars(["Raju", "Priya", "Kumar"], [2, 3, 4], "?") +
        "Raju, Priya and Kumar shared some money in the ratio 2 : 3 : 4. Kumar got $40 more than Raju. "
        "How much money did they share?", Mc(180),
        [Mc(360), Mc(80), Mc(120), Mc(20)],
        "Kumar has 4 − 2 = 2 more units. 2 units = $40, so 1 unit = $20. Total: 2 + 3 + 4 = 9 units = 9 × $20 = <b>$180</b>.")
    # 6 fraction -> ratio
    add("In a CCA, " + fr(3, 5) + " of the members are girls. There are 12 more girls than boys. How many members are there?",
        Nc(60), [Nc(20), Nc(30), Nc(36), Nc(24)],
        "Girls : boys = 3 : 2. The difference is 3 − 2 = 1 unit = 12. Total: 5 units = 5 × 12 = <b>60</b>. "
        "36 is only the number of girls.")
    # 7 one quantity leaves
    add("The ratio of the number of boys to the number of girls in a hall was 4 : 5. After 20 boys left the hall, "
        "the ratio became 2 : 5. How many children were in the hall at first?", Nc(90),
        [Nc(70), Nc(45), Nc(180), Nc(50)],
        "The girls do not change: 5 units. Boys went from 4 units to 2 units, so 2 units = 20 and 1 unit = 10. "
        "At first: 4 + 5 = 9 units = <b>90</b>. 70 is the number of children after the boys left.")
    # 8 combining ratios
    add("The ratio of A to B is 2 : 3. The ratio of B to C is 4 : 5. What is the ratio of A to C?", Rc(8, 15),
        [Rc(2, 5), Rc(8, 5), Rc(6, 5), Rc(2, 15)],
        "Make B the same in both ratios. 2 : 3 = 8 : 12 and 4 : 5 = 12 : 15. So A : B : C = 8 : 12 : 15, and A : C = <b>8 : 15</b>.")
    # 9 transfer, new ratio
    add("Mei Ling and Hui Min had stickers in the ratio 3 : 1. After Mei Ling gave 20 stickers to Hui Min, "
        "the ratio became 5 : 3. How many stickers did Mei Ling have at first?", Nc(120),
        [Nc(60), Nc(100), Nc(160), Nc(40)],
        "The total stays the same. Make the totals equal: 3 : 1 = 6 : 2 (8 units) and 5 : 3 (8 units). "
        "Mei Ling went from 6 units to 5 units, so 1 unit = 20. At first she had 6 × 20 = <b>120</b>.")
    # 10 drink mix, units of volume
    add("Mrs Ng mixes orange cordial and water in the ratio 2 : 9. She makes 2.2 ℓ of orange drink. "
        "How much cordial does she use?", Nc(400, " ml"),
        [Nc(1100, " ml"), Nc(200, " ml"), Nc(1800, " ml"), Nc(440, " ml")],
        "2.2 ℓ = 2200 ml. 2 + 9 = 11 units, so 1 unit = 2200 ÷ 11 = 200 ml. Cordial: 2 × 200 = <b>400 ml</b>. "
        "1100 ml comes from dividing 2200 by 2.")
    # 11 fraction of total, three terms
    add("Some money was shared among Ethan, Chloe and Arjun in the ratio 3 : 4 : 5. What fraction of the money did Chloe get?",
        Fc(1, 3), [Fc(4, 5), Fc(1, 2), Fc(1, 4), Fc(5, 12)],
        "3 + 4 + 5 = 12 units. Chloe got 4 of the 12 units: " + fr(4, 12) + " = <b>" + fr(1, 3) + "</b>. "
        + fr(1, 2) + " compares Chloe with the other two only.")
    # 12 hawker stall, model
    add(bars(["Chicken rice", "Nasi lemak"], [5, 3], "?") +
        "A hawker stall sold plates of chicken rice and nasi lemak in the ratio 5 : 3. It sold 84 more plates of chicken rice "
        "than nasi lemak. How many plates did it sell altogether?", Nc(336),
        [Nc(672), Nc(210), Nc(168), Nc(92)],
        "5 − 3 = 2 units = 84, so 1 unit = 42. Altogether: 8 units = 8 × 42 = <b>336</b>. 672 uses 84 as 1 unit.")
    # 13 rectangle
    add("The ratio of the length to the breadth of a rectangle is 5 : 3. Its perimeter is 64 cm. What is its area?",
        Nc(240, " cm²"), [Nc(60, " cm²"), Nc(960, " cm²"), Nc(15, " cm²"), Nc(180, " cm²")],
        "Length + breadth = 64 ÷ 2 = 32 cm = 8 units, so 1 unit = 4 cm. Length 20 cm, breadth 12 cm. "
        "Area: 20 × 12 = <b>240 cm²</b>. 960 cm² forgets to halve the perimeter.")
    assert 2 * (20 + 12) == 64
    # 14 one spends
    add("The ratio of Zhi Hao’s savings to Xin Yi’s savings was 7 : 4. After Zhi Hao spent $45, they had the same amount. "
        "How much did Zhi Hao have at first?", Mc(105),
        [Mc(60), Mc(165), Mc(315), Mc(49)],
        "Xin Yi’s savings do not change. Zhi Hao spent 7 − 4 = 3 units = $45, so 1 unit = $15. "
        "Zhi Hao at first: 7 × $15 = <b>$105</b>.")
    # 15 both receive the same (difference unchanged)
    add("Farah and Nurul had stamps in the ratio 2 : 5. Each of them received 12 more stamps. The ratio became 1 : 2. "
        "How many stamps did Nurul have at first?", Nc(60),
        [Nc(72), Nc(24), Nc(36), Nc(30)],
        "The difference stays the same. Before: 2 : 5, a difference of 3 units. After: 1 : 2 = 3 : 6, also a difference of 3 units. "
        "Farah went from 2 units to 3 units, so 1 unit = 12. Nurul at first: 5 × 12 = <b>60</b>.")
    assert F(24 + 12, 60 + 12) == F(1, 2)
    # 16 money decimals, model
    add(bars(["Book", "Pen"], [9, 2]) +
        "The ratio of the cost of a book to the cost of a pen is 9 : 2. The book costs $8.40 more than the pen. "
        "How much does the pen cost?", Mc(F(240, 100)),
        [Mc(F(120, 100)), Mc(F(1080, 100)), Mc(F(420, 100)), Mc(F(168, 100))],
        "9 − 2 = 7 units = $8.40, so 1 unit = $8.40 ÷ 7 = $1.20. Pen: 2 × $1.20 = <b>$2.40</b>.")
    assert F(84, 10) / 7 * 9 - F(84, 10) / 7 * 2 == F(84, 10)
    # 17 fraction then ratio
    add("Arjun, Kavya and Sarah shared some stickers. Arjun got " + fr(1, 4) + " of them. Kavya and Sarah shared the rest in the "
        "ratio 1 : 2. Sarah got 30 stickers. How many stickers were there altogether?", Nc(60),
        [Nc(45), Nc(40), Nc(120), Nc(90)],
        "Kavya and Sarah: 1 + 2 = 3 units, Sarah 2 units = 30, so 1 unit = 15. The rest is 15 + 30 = 45, which is "
        + fr(3, 4) + " of all. " + fr(1, 4) + " of all = 45 ÷ 3 = 15. Altogether: 4 × 15 = <b>60</b>.")
    # 18 three colours
    add("For National Day, a class put up red, white and blue balloons in the ratio 2 : 5 : 3. There are 60 balloons. "
        "How many more white balloons than red balloons are there?", Nc(18),
        [Nc(30), Nc(3), Nc(12), Nc(20)],
        "2 + 5 + 3 = 10 units = 60, so 1 unit = 6. White has 5 − 2 = 3 more units: 3 × 6 = <b>18</b>. "
        "30 is the number of white balloons.")
    # 19 fraction of the other, model
    add(bars(["Sarah", "Chloe"], [3, 5], "$96", 1) +
        "Sarah’s money is " + fr(3, 5) + " of Chloe’s money. They have $96 altogether. How much money does Chloe have?",
        Mc(60), [Mc(36), Mc(F(576, 10)), Mc(F(3840, 100)), Mc(F(192, 10))],
        "Sarah : Chloe = 3 : 5, which is 8 units = $96. 1 unit = $12. Chloe: 5 × $12 = <b>$60</b>. "
        "$57.60 is " + fr(3, 5) + " of $96, which uses the wrong whole.")
    # 20 one receives
    add("During Chinese New Year, the ratio of the number of red packets Jun Jie had to the number Wei Ming had was 4 : 3. "
        "After Jun Jie received 6 more red packets, the ratio became 2 : 1. How many red packets did they have altogether at the end?",
        Nc(27), [Nc(21), Nc(9), Nc(18), Nc(13)],
        "Wei Ming’s packets do not change. Make his units equal: 4 : 3 and 2 : 1 = 6 : 3. Jun Jie went from 4 units to 6 units, "
        "so 2 units = 6 and 1 unit = 3. At the end: 6 + 3 = 9 units = <b>27</b>.")
    assert F(12 + 6, 9) == 2
    assert len(its) == 20, len(its)
    return {"title": "PSLE-style ratio word problems", "items": its}


# ============================================================ lesson
def body_html():
    pic = shapes_svg(["c", "s", "t", "s", "c", "s", "t", "s", "s"])
    bar = bar_svg([("Siti", 2, "$12", "$24", FILL_L), ("Ali", 3, "$12", "$36", "#fde7bd")], "$60",
                  "bar model: Siti to Ali is 2 : 3, total $60, each unit $12")
    return (
        "<h2>What is a ratio?</h2>"
        "<p>A <b>ratio</b> compares two or more quantities. We write it with a colon: <b>a : b</b> or <b>a : b : c</b>. "
        "A ratio has no units.</p>"
        "<figure class='sn-fig'>" + pic + "<figcaption>2 circles, 5 squares and 2 triangles. "
        "Circles : squares : triangles = 2 : 5 : 2.</figcaption></figure>"
        "<p><b>Order matters.</b> Write the numbers in the same order as the words. Circles to squares is 2 : 5. "
        "Squares to circles is 5 : 2.</p>"
        "<h2>Equivalent ratios and simplest form</h2>"
        "<p>Multiply or divide <b>every</b> term by the same number to get an equivalent ratio. "
        "A ratio is in its <b>simplest form</b> when the terms have no common factor except 1.</p>"
        + ex("Example", "Express 12 : 18 in its simplest form.",
             "The highest common factor of 12 and 18 is 6. 12 ÷ 6 = 2 and 18 ÷ 6 = 3.", "2 : 3")
        + ex("Example", "Find the missing term. 3 : 5 = 12 : ?",
             "3 × 4 = 12, so multiply the second term by 4 too: 5 × 4 = 20.", "20")
        + "<h2>Ratio and fraction</h2>"
        "<p>If A : B = 2 : 3, then A is 2 units and B is 3 units. The total is 2 + 3 = 5 units.</p>"
        + table(["A : B = 2 : 3", "Fraction"], [
            ["A as a fraction of the total", fr(2, 5)],
            ["B as a fraction of the total", fr(3, 5)],
            ["A as a fraction of B", fr(2, 3)],
            ["B as a fraction of A", fr(3, 2)],
        ])
        + "<h2>Dividing a quantity in a ratio</h2>"
        "<p>Draw a <b>model</b> with one box for each unit. Every unit has the same value. Find 1 unit first.</p>"
        + ex("Example", "Siti and Ali shared $60 in the ratio 2 : 3. How much did each of them get?",
             "2 + 3 = 5 units. 5 units = $60, so 1 unit = $60 ÷ 5 = $12. Siti: 2 × $12 = $24. Ali: 3 × $12 = $36.",
             "Siti $24, Ali $36")
        + "<figure class='sn-fig'>" + bar + "<figcaption>5 units make $60, so each unit is $12. "
        "Check: $24 + $36 = $60.</figcaption></figure>"
        "<p>In before-and-after problems, look for what does <b>not</b> change: the total, one person’s amount, "
        "or the difference. Make those units the same, then compare.</p>"
        + ex("Example", "Wei Ming and Siti had money in the ratio 7 : 3. After Wei Ming gave Siti $20, they had the same amount. "
             "How much did Wei Ming have at first?",
             "The total, 10 units, does not change. Equal shares are 5 units each, so Wei Ming gave 7 − 5 = 2 units. "
             "2 units = $20, so 1 unit = $10. At first: 7 × $10 = $70.",
             "$70")
        + "<h2>Common mistakes</h2>"
        + table(["Mistake", "What to do instead"], [
            ["Writing the ratio the wrong way round", "The first quantity named goes first: boys to girls is boys : girls"],
            ["Reading A : B = 2 : 3 as “A is " + fr(2, 3) + " of the total”",
             "Add the units to find the total: A is " + fr(2, 5) + " of the total"],
            ["Adding the same number to both terms: 3 : 5 = 6 : 8", "Multiply both terms: 3 : 5 = 6 : 10"],
            ["Sharing $60 in 2 : 3 by working out $60 ÷ 2", "Add the units first: 2 + 3 = 5, so 1 unit = $12"],
            ["Simplifying 2 m : 80 cm as 2 : 80", "Use the same unit first: 200 cm : 80 cm = 5 : 2"],
        ])
    )


FAQ = [
    {"q": "What is taught in P6 ratio?",
     "a": "Primary 6 students write ratios as a : b and a : b : c, find equivalent ratios and the simplest form, find missing terms, divide a quantity in a given ratio and link ratio with fractions."},
    {"q": "How do I explain ratio to my child?",
     "a": "Use units: a ratio of 2 : 3 means 2 equal units and 3 equal units. Draw a bar model, find the value of 1 unit, then multiply."},
    {"q": "What is the most common mistake with ratio?",
     "a": "Mixing up part and whole. If boys : girls = 2 : 3, the boys are 2/3 of the girls but only 2/5 of all the children. Writing the ratio in the wrong order is the next most common mistake."},
    {"q": "Is ratio tested in the PSLE?",
     "a": "Yes. Ratio is in the MOE Primary 6 syllabus and often appears in PSLE Paper 2 word problems, especially before-and-after questions solved with the model method."},
]


def gen():
    rnd = random.Random(66804)
    P = People(rnd)
    sets = [set_writing(rnd), set_equivalent(rnd), set_fraction(rnd, P), set_sharing(rnd, P), set_words(rnd, P)]
    for s in sets:
        rnd.shuffle(s["items"])
    balance(sets, rnd)
    seen = set()
    for s in sets:
        assert len(s["items"]) == 20, (s["title"], len(s["items"]))
        cnt = [0, 0, 0, 0]
        for it in s["items"]:
            assert len(set(plain(x) for x in it["c"])) == 4, it
            assert it["q"].count("<svg") <= 1, it["q"]
            assert it["q"] not in seen, it["q"]
            seen.add(it["q"])
            cnt[it["a"]] += 1
        assert cnt == [5, 5, 5, 5], (s["title"], cnt)
    return {
        "country": "sg", "subject": "maths", "grade": "primary-6", "slug": "ratio", "sort": 4,
        "updated": UPDATED, "pdf_url": "",
        "title": "Primary 6 Ratio",
        "seo_title": "P6 Ratio Worksheets: Free Primary 6 Maths with Answers (MOE Syllabus, PSLE Practice)",
        "short_title": "Ratio",
        "domain": "Number and Algebra",
        "standard_code": "Primary 6: Ratio",
        "standard_url": "https://www.moe.gov.sg/primary/curriculum/syllabus",
        "standard_text": "Notation and interpretation of a : b and a : b : c; equivalent ratios; simplest form; dividing a quantity in a given ratio; missing terms; relationship between fraction and ratio",
        "meta_desc": "P6 ratio practice: simplest form, missing terms, ratio and fraction, sharing in a ratio with models and PSLE-style problems. 100 questions with answers.",
        "key_big": "A ratio 2 : 3 means 2 units and 3 units. Find 1 unit first, then multiply.",
        "key_sub": "Share $60 in the ratio 2 : 3: 5 units = $60, 1 unit = $12, so $24 and $36.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    mark_large(u, "(bar model|shapes picture)")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
