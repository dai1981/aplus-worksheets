# -*- coding: utf-8 -*-
"""
US Grade 6 Math: Understanding Ratios (6.RP.A.1)
  python tools/gen_us_math_g6_ratios.py
Ratio from a picture, ratio language (a:b, a to b, "for every"), part-to-part vs part-to-whole,
equivalent ratios and simplest form, tape diagrams, word problems.
Wrong answers come from real mistakes: reversed order, part:whole instead of part:part,
adding the same number to both terms, using only one part, dividing by one term, using the difference.
HTML attributes use single quotes (no backslashes in the JSON).
"""
import json, os, random, re
from fractions import Fraction as F
from math import gcd

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "us", "math", "grade-6")
UPDATED = "2026-11-02"
GREEN = "#006633"
FILL = "#cfe6d6"
INK = "#2b2b2b"
RED = "#c0392b"
YEL = "#f4d35e"
YEL_E = "#9a7b0a"
FONT = "Arial, Helvetica, sans-serif"
GIRLS = ["Maya", "Ava", "Mia", "Zoe", "Lily", "Emma", "Nora", "Ruby", "Sofia", "Grace"]
BOYS = ["Leo", "Noah", "Eli", "Sam", "Ben", "Omar", "Kai", "Jack", "Luis", "Owen"]


# ------------------------------------------------------------ helpers
def f(n):
    return "{:,}".format(n)


def R(a, b):
    return "%s:%s" % (f(a), f(b))


def fr(a, b):
    return "<span class='fr'><span class='fn'>%d</span><span class='fd'>%d</span></span>" % (a, b)


def plain(s):
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", s)).strip()


def value(c):
    """Numeric value of a choice, so that no two choices are equal in value."""
    m = re.search(r"<span class='fn'>(\d+)</span><span class='fd'>(\d+)</span>", c)
    if m:
        return F(int(m.group(1)), int(m.group(2)))
    t = plain(c).replace(",", "")
    m = re.match(r"^(\d+) ?(?::|to) ?(\d+)$", t)
    if m:
        return F(int(m.group(1)), int(m.group(2)))
    m = re.match(r"^\$?(\d+)( [a-z ]+)?$", t)
    if m:
        return F(int(m.group(1)))
    return t


def mcq(q, right, wrongs, e, same_ok=False):
    """right first; balance() moves it. 4 different choices, none equal in value (unless same_ok)."""
    ch = [right] + list(wrongs)
    assert len(ch) == 4, (q, ch)
    assert len({plain(c) for c in ch}) == 4, ch
    if not same_ok:
        assert len({value(c) for c in ch}) == 4, ch
    return {"q": q, "c": ch, "a": 0, "e": e}


def ok_choices(right, wrongs, same_ok=False):
    ch = [right] + list(wrongs)
    if len({plain(c) for c in ch}) != 4:
        return False
    return same_ok or len({value(c) for c in ch}) == 4


def pick3(right, cands):
    """First 3 usable distractors: positive, different from the answer and each other (in value)."""
    out, seen = [], {value(right)}
    for c in cands:
        if c is None:
            continue
        v = value(c)
        lead = re.match(r"^\$?(\d+)", plain(c).replace(",", ""))
        if lead and int(lead.group(1)) <= 0:
            continue
        if v in seen:
            continue
        seen.add(v)
        out.append(c)
        if len(out) == 3:
            return out
    raise AssertionError((right, cands))


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

    def two(self):
        return self.next(), self.next()


def cap(s):
    return s[0].upper() + s[1:]


def unit(n, one, many=None):
    if one == "$":
        return "$" + f(n)
    return "%s %s" % (f(n), one if n == 1 else (many or one + "s"))


def fig(svg):
    return "<div class='qfig'>" + svg + "</div>"


def svg_wrap(w, h, body, label):
    return ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 %d %d' width='%d' height='%d' "
            "role='img' aria-label='%s'><g font-family='%s'>%s</g></svg>" % (w, h, w, h, label, FONT, body))


def tw(t, fs):
    t = str(t)
    return (len(t) - t.count(",") * 0.6) * fs * 0.6


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
        return "<circle cx='%.1f' cy='%.1f' r='11' fill='%s' stroke='%s' stroke-width='2'/>" % (cx, cy, GREEN, GREEN)
    if kind == "s":
        return ("<rect x='%.1f' y='%.1f' width='21' height='21' fill='%s' stroke='%s' stroke-width='2.5'/>"
                % (cx - 10.5, cy - 10.5, FILL, GREEN))
    return ("<path d='M%.1f %.1f L%.1f %.1f L%.1f %.1f Z' fill='%s' stroke='%s' stroke-width='2' stroke-linejoin='round'/>"
            % (cx, cy - 11, cx + 12, cy + 10, cx - 12, cy + 10, YEL, YEL_E))


def shapes_svg(kinds):
    """kinds: list like ['c','s','c',...] drawn in order, one row up to 8, else two rows."""
    n = len(kinds)
    per = n if n <= 8 else (n + 1) // 2
    cell = 32
    rows = (n + per - 1) // per
    body = []
    for i, k in enumerate(kinds):
        r, c = divmod(i, per)
        body.append(shape(k, 4 + cell * c + cell / 2, 4 + cell * r + cell / 2))
    W = 8 + cell * per
    H = 8 + cell * rows
    counts = []
    for k in ["c", "s", "t"]:
        m = kinds.count(k)
        if m:
            counts.append(unit(m, *SHAPE_NAMES[k]))
    return svg_wrap(W, H, "".join(body), "shapes picture: " + " and ".join(counts))


def tape_svg(rows, total=None, label="tape diagram"):
    """rows: [(label, boxes, cell_text, right_text)]; optional bracket on the right with the total."""
    fs = 15
    lw = max(tw(r[0], fs) for r in rows) + 12
    x0 = 6 + lw
    cw = max([30] + [tw(r[2], fs) + 12 for r in rows if r[2]])
    bh, gap, y0 = 28, 10, 4
    s = []
    ends = []
    for i, (lab, n, cell, right) in enumerate(rows):
        y = y0 + i * (bh + gap)
        s.append(text(x0 - 8, y + bh / 2 + 5.5, lab, fs, "end"))
        for j in range(n):
            x = x0 + j * cw
            s.append("<rect x='%.1f' y='%d' width='%.1f' height='%d' fill='%s' stroke='%s' stroke-width='2.5'/>"
                     % (x, y, cw, bh, FILL, GREEN))
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
    return svg_wrap(int(W + 0.99), ybot + 4, "".join(s), label)


# ------------------------------------------------------------ set 1: ratio from a picture
def set_pictures(rnd):
    its = []
    used = set()

    def counts(k):
        while True:
            v = tuple(rnd.randint(2, 7 if k == 3 else 8) for _ in range(k))
            if len(set(v)) == k and sum(v) <= (15 if k == 3 else 14) and v not in used:
                used.add(v)
                return v

    def draw(cnt):
        kinds = []
        for k, m in zip(["c", "s", "t"], cnt):
            kinds += [k] * m
        rnd.shuffle(kinds)
        return fig(shapes_svg(kinds))

    def two_kind(ask):
        while True:
            a, b = counts(2)
            t = a + b
            if ask == "cs":
                right, wr = R(a, b), [R(b, a), R(a, t), R(b, t)]
            elif ask == "sc":
                right, wr = R(b, a), [R(a, b), R(b, t), R(a, t)]
            elif ask == "ca":
                right, wr = R(a, t), [R(a, b), R(b, t), R(t, a)]
            else:
                right, wr = R(b, t), [R(b, a), R(a, t), R(t, b)]
            if ok_choices(right, wr):
                return a, b, t, right, wr

    for ask, n in [("cs", 6), ("sc", 4), ("ca", 2), ("sa", 2)]:
        for _ in range(n):
            a, b, t, right, wr = two_kind(ask)
            F_ = draw((a, b))
            if ask == "cs":
                q = "What is the ratio of circles to squares?"
                e = ("Count: %d circles and %d squares. Circles are named first, so write %d first: %s. "
                     "%s would compare squares to circles." % (a, b, a, R(a, b), R(b, a)))
            elif ask == "sc":
                q = "What is the ratio of squares to circles?"
                e = ("Count: %d squares and %d circles. Squares are named first, so write %d first: %s. "
                     "%s would compare circles to squares." % (b, a, b, R(b, a), R(a, b)))
            elif ask == "ca":
                q = "What is the ratio of circles to all the shapes?"
                e = ("There are %d circles and %d + %d = %d shapes in all. Circles to all shapes is %s. "
                     "%s compares circles to squares, not to all the shapes." % (a, a, b, t, R(a, t), R(a, b)))
            else:
                q = "What is the ratio of squares to all the shapes?"
                e = ("There are %d squares and %d + %d = %d shapes in all. Squares to all shapes is %s. "
                     "%s compares squares to circles, not to all the shapes." % (b, a, b, t, R(b, t), R(b, a)))
            its.append(mcq(F_ + q, right, wr, e))
    # three kinds of shapes
    for x, y in [("t", "c"), ("s", "t"), ("c", "t")]:
        while True:
            cnt = counts(3)
            d = dict(zip(["c", "s", "t"], cnt))
            z = [k for k in "cst" if k not in (x, y)][0]
            tot = sum(cnt)
            right, wr = R(d[x], d[y]), [R(d[y], d[x]), R(d[x], tot), R(d[x], d[z])]
            if ok_choices(right, wr):
                break
        nx, ny, nz = SHAPE_NAMES[x][1], SHAPE_NAMES[y][1], SHAPE_NAMES[z][1]
        its.append(mcq(draw(cnt) + "What is the ratio of %s to %s?" % (nx, ny), right, wr,
                       "Count only the two kinds named: %d %s and %d %s. %s come first, so the ratio is %s. "
                       "Leave out the %s." % (d[x], nx, d[y], ny, cap(nx), R(d[x], d[y]), nz)))
    # which sentence describes the picture?
    for _ in range(3):
        a, b = counts(2)
        t = a + b

        def sent(n1, w1, n2, w2):
            return "For every %s, there %s %s." % (unit(n1, *w1), "is" if n2 == 1 else "are", unit(n2, *w2))

        C, S, SH = SHAPE_NAMES["c"], SHAPE_NAMES["s"], ("shape", "shapes")
        right = sent(a, C, b, S)
        wr = [sent(b, C, a, S), sent(a, C, t, S), sent(a, SH, b, S)]
        its.append(mcq(draw((a, b)) + "Which sentence describes the picture?", right, wr,
                       "There are %d circles and %d squares, so the ratio of circles to squares is %s: "
                       "for every %d circles, there are %d squares. There are %d shapes in all, not %d."
                       % (a, b, R(a, b), a, b, t, a)))
    rnd.shuffle(its)
    return {"title": "Write a ratio from a picture", "items": its}


# ------------------------------------------------------------ set 2: ratio language and part-to-whole
# (one X, many X, one Y, many Y, whole (plural), place, short label X, short label Y)
PAIRS = [
    ("red marble", "red marbles", "blue marble", "blue marbles", "marbles", "a bag", "red", "blue"),
    ("girl", "girls", "boy", "boys", "students", "a class", "girls", "boys"),
    ("tulip", "tulips", "daisy", "daisies", "flowers", "a garden", "tulips", "daisies"),
    ("goldfish", "goldfish", "guppy", "guppies", "fish", "a fish tank", "goldfish", "guppies"),
    ("cat", "cats", "dog", "dogs", "animals", "an animal shelter", "cats", "dogs"),
    ("apple", "apples", "orange", "oranges", "pieces of fruit", "a fruit bowl", "apples", "oranges"),
    ("car", "cars", "truck", "trucks", "vehicles", "a parking lot", "cars", "trucks"),
    ("cow", "cows", "horse", "horses", "animals", "a farm", "cows", "horses"),
    ("novel", "novels", "comic book", "comic books", "books", "a bookshelf", "novels", "comics"),
    ("drummer", "drummers", "trumpet player", "trumpet players", "band members", "a school band", "drums", "trumpets"),
    ("sixth grader", "sixth graders", "fifth grader", "fifth graders", "runners", "a running club", "6th", "5th"),
    ("red pepper", "red peppers", "green pepper", "green peppers", "peppers", "a basket", "red", "green"),
]


def prep(pl):
    return "on" if pl in ("a farm", "a bookshelf") else "in"


def every(n1, one1, many1, n2, one2, many2):
    first = "For every %s" % one1 if n1 == 1 else "For every %d %s" % (n1, many1)
    return "%s, there %s." % (first, "is 1 %s" % one2 if n2 == 1 else "are %d %s" % (n2, many2))


def coprime_pair(rnd, lo=1, hi=7, maxsum=12):
    while True:
        p, q = rnd.randint(lo, hi), rnd.randint(lo, hi)
        if p != q and gcd(p, q) == 1 and p + q <= maxsum:
            return p, q


def set_language(rnd):
    its = []
    ctx = PAIRS[:]
    rnd.shuffle(ctx)
    k = [0]
    seen = set()

    def nxt():
        c = ctx[k[0] % len(ctx)]
        k[0] += 1
        return c

    def pq(lo=1, hi=7, maxsum=12):
        while True:
            p, q = coprime_pair(rnd, lo, hi, maxsum)
            if (p, q) not in seen:
                seen.add((p, q))
                return p, q

    # 1) another way to write a:b
    for _ in range(3):
        X1, Xm, Y1, Ym, W, pl, _, _ = nxt()
        p, q = pq(2)
        its.append(mcq("%s has only %s and %s. The ratio of %s to %s is %s. Which also shows this ratio?"
                       % (cap(pl), Xm, Ym, Xm, Ym, R(p, q)),
                       "%d to %d" % (p, q), ["%d to %d" % (q, p), "%d to %d" % (p, p + q), "%d to %d" % (q, p + q)],
                       "%s and “%d to %d” mean the same thing. Keep the order: %s first, then %s." % (R(p, q), p, q, Xm, Ym)))
    # 2) colon -> "for every" sentence
    for _ in range(2):
        X1, Xm, Y1, Ym, W, pl, _, _ = nxt()
        p, q = pq(1, 6)
        right = every(p, X1, Xm, q, Y1, Ym)
        wr = [every(p, Y1, Ym, q, X1, Xm), every(p, X1, Xm, p + q, Y1, Ym), every(q, W[:-1] if W != "fish" else W, W, p, X1, Xm)]
        its.append(mcq("%s has only %s and %s. The ratio of %s to %s is %s. Which sentence means the same thing?"
                       % (cap(pl), Xm, Ym, Xm, Ym, R(p, q)), right, wr,
                       "%s means %s The first number goes with %s, the second with %s."
                       % (R(p, q), right[0].lower() + right[1:], Xm, Ym), same_ok=True))
    # 3) "for every" sentence -> ratio (asked in the other order)
    for _ in range(2):
        X1, Xm, Y1, Ym, W, pl, _, _ = nxt()
        p, q = pq(2)
        s = every(p, X1, Xm, q, Y1, Ym)
        its.append(mcq("%s %s, %s What is the ratio of %s to %s?" % (cap(prep(pl)), pl, s[0].lower() + s[1:], Ym, Xm),
                       R(q, p), [R(p, q), R(q, p + q), R(p, p + q)],
                       "The question asks for %s first, then %s. There are %d %s for every %d %s, so the ratio is %s."
                       % (Ym, Xm, q, Ym, p, Xm, R(q, p))))
    # 4) part-to-whole from counts
    for i in range(4):
        X1, Xm, Y1, Ym, W, pl, _, _ = nxt()
        while True:
            a, b = rnd.randint(3, 15), rnd.randint(3, 15)
            if a != b and (a, b) not in seen:
                seen.add((a, b))
                break
        t = a + b
        if i < 2:
            right, wr, who, n = R(a, t), [R(a, b), R(b, t), R(t, a)], Xm, a
        else:
            right, wr, who, n = R(b, t), [R(b, a), R(a, t), R(t, b)], Ym, b
        its.append(mcq("%s has %s and %s. What is the ratio of %s to all the %s?" % (cap(pl), unit(a, X1, Xm), unit(b, Y1, Ym), who, W),
                       right, wr,
                       "All the %s: %d + %d = %d. %s to all the %s is %d:%d. This is a part-to-whole ratio."
                       % (W, a, b, t, cap(who), W, n, t)))
    # 5) the rest: find the other part
    for _ in range(3):
        X1, Xm, Y1, Ym, W, pl, _, _ = nxt()
        while True:
            t, a = rnd.randint(18, 32), rnd.randint(5, 15)
            b = t - a
            if b != a and b > 2 and (a, b) not in seen:
                seen.add((a, b))
                break
        its.append(mcq("%s has %d %s. %d of them are %s, and the rest are %s. What is the ratio of %s to %s?"
                       % (cap(pl), t, W, a, Xm, Ym, Ym, Xm),
                       R(b, a), [R(a, b), R(b, t), R(a, t)],
                       "%s: %d − %d = %d. %s to %s is %s. Use the two parts, not the total, %d." % (cap(Ym), t, a, b, cap(Ym), Xm, R(b, a), t)))
    # 6) ratio given -> part-to-whole ratio
    for _ in range(3):
        X1, Xm, Y1, Ym, W, pl, _, _ = nxt()
        p, q = pq(2)
        its.append(mcq("%s has only %s and %s. The ratio of %s to %s is %s. What is the ratio of %s to all the %s?"
                       % (cap(pl), Xm, Ym, Xm, Ym, R(p, q), Ym, W),
                       R(q, p + q), [R(p, q), R(q, p), R(p, p + q)],
                       "For every %d %s there are %d %s, so every group has %d + %d = %d %s. %s to all is %s."
                       % (p, Xm, q, Ym, p, q, p + q, W, cap(Ym), R(q, p + q))))
    # 7) ratio given -> fraction of the whole
    for _ in range(3):
        X1, Xm, Y1, Ym, W, pl, _, _ = nxt()
        p, q = pq(2)
        its.append(mcq("%s has only %s and %s. The ratio of %s to %s is %s. What fraction of the %s are %s?"
                       % (cap(pl), Xm, Ym, Xm, Ym, R(p, q), W, Xm),
                       fr(p, p + q), [fr(p, q), fr(q, p + q), fr(q, p)],
                       "Out of every %d + %d = %d %s, %d are %s. So %s of the %s are %s, not %s."
                       % (p, q, p + q, W, p, Xm, fr(p, p + q), W, Xm, fr(p, q))))
    assert len(its) == 20, len(its)
    rnd.shuffle(its)
    return {"title": "Ratio language and part-to-whole", "items": its}


# ------------------------------------------------------------ set 3: equivalent ratios and simplest form
def set_equivalent(rnd):
    its = []
    seen = set()

    def base(lo=1, hi=9):
        while True:
            p, q = coprime_pair(rnd, lo, hi, 15)
            if (p, q) not in seen:
                seen.add((p, q))
                return p, q

    # 1) simplest form
    for _ in range(5):
        while True:
            p, q = base(2)
            g = rnd.randint(2, 8)
            a, b = p * g, q * g
            right, wr = R(p, q), [R(q, p), R(a - g, b - g), R(p, b)]
            if a <= 72 and b <= 72 and ok_choices(right, wr):
                break
        its.append(mcq("What is %s in simplest form?" % R(a, b), right, wr,
                       "Divide <b>both</b> terms by %d, the greatest number that divides both: %d ÷ %d = %d and %d ÷ %d = %d. "
                       "So %s = %s. Subtracting %d from each term does not keep the ratio."
                       % (g, a, g, p, b, g, q, R(a, b), R(p, q), g)))
    # 2) which ratio is equivalent?
    for _ in range(4):
        while True:
            p, q = base()
            k = rnd.randint(2, 6)
            right, wr = R(k * p, k * q), [R(p + k, q + k), R(k * q, k * p), R(k * p, q)]
            if ok_choices(right, wr):
                break
        its.append(mcq("Which ratio is equivalent to %s?" % R(p, q), right, wr,
                       "Multiply both terms by the same number, %d: %d × %d = %d and %d × %d = %d. "
                       "Adding %d to both terms (%s) does not keep the ratio." % (k, p, k, k * p, q, k, k * q, k, R(p + k, q + k))))
    # 3) which ratio is NOT equivalent?
    for _ in range(3):
        p, q = base(1, 6)
        m = rnd.choice([2, 3])
        a, b = m * p, m * q
        d = rnd.choice([1, 2, 3])
        right = R(a + d, b + d)
        mult = [x for x in [2, 3, 4, 5] if x != 1]
        rnd.shuffle(mult)
        wr = [R(p, q), R(mult[0] * a, mult[0] * b), R(mult[1] * a, mult[1] * b)]
        assert F(a + d, b + d) != F(p, q)
        its.append(mcq("Which ratio is <b>not</b> equivalent to %s?" % R(a, b), right, wr,
                       "%s simplifies to %s. %s and %s are %s with both terms multiplied by the same number. "
                       "%s adds %d to both terms, so it is not equivalent."
                       % (R(a, b), R(p, q), wr[1], wr[2], R(a, b), right, d), same_ok=True))
    # 4) missing term
    for i in range(4):
        while True:
            p, q = base(2)
            k = rnd.randint(3, 8)
            if i < 2:
                ans, given = k * p, k * q
                q_ = "%s = ☐:%d. What number goes in the box?" % (R(p, q), given)
                cands = [str(p + given - q), str(k), str(p * given)]
                e = ("%d × %d = %d, so multiply the first term by %d too: %d × %d = %d. "
                     "Adding %d to both terms would give %d, which is wrong." % (q, k, given, k, p, k, ans, given - q, p + given - q))
            else:
                ans, given = k * q, k * p
                q_ = "%s = %d:☐. What number goes in the box?" % (R(p, q), given)
                cands = [str(q + given - p), str(k), str(q * given)]
                e = ("%d × %d = %d, so multiply the second term by %d too: %d × %d = %d. "
                     "Adding %d to both terms would give %d, which is wrong." % (p, k, given, k, q, k, ans, given - p, q + given - p))
            if ok_choices(str(ans), cands) and all(int(c) > 0 for c in cands):
                break
        its.append(mcq(q_, str(ans), cands, e))
    # 5) "for every" from the standard: animals and parts
    while True:
        n = rnd.randint(6, 12)
        right, wr = "2:1", ["1:2", R(2 * n, 1), R(2, n)]
        if ok_choices(right, wr):
            break
    its.append(mcq("Each bird at the zoo has 2 wings and 1 beak. The bird house has %d birds. "
                   "What is the ratio of wings to beaks in simplest form?" % n, right, wr,
                   "%d birds have %d × 2 = %d wings and %d beaks. %s = 2:1, because for every 2 wings there is 1 beak."
                   % (n, n, 2 * n, n, R(2 * n, n))))
    n = rnd.randint(5, 9)
    its.append(mcq("Each tricycle has 3 wheels and 1 seat. A store has %d tricycles. What is the ratio of seats to wheels "
                   "in simplest form?" % n, "1:3", ["3:1", R(1, 3 * n), R(3, n)],
                   "%d tricycles have %d seats and %d × 3 = %d wheels. Seats to wheels is %s = 1:3: "
                   "for every 1 seat, there are 3 wheels." % (n, n, n, 3 * n, R(n, 3 * n))))
    # 6) which pair is equivalent?
    for j in range(2):
        p, q = base(2, 6)
        k1, k2 = rnd.sample([2, 3, 4, 5], 2)
        d = rnd.choice([1, 2])
        a2, b2 = rnd.randint(2, 6), rnd.randint(2, 6)
        while a2 == b2 or F(a2, b2) == F(p, q):
            a2, b2 = rnd.randint(2, 6), rnd.randint(2, 6)
        right = "%s and %s" % (R(k1 * p, k1 * q), R(k2 * p, k2 * q))
        wr = ["%s and %s" % (R(k1 * p, k1 * q), R(k1 * p + d, k1 * q + d)),
              "%s and %s" % (R(a2, b2), R(b2, a2)),
              "%s and %s" % (R(a2, b2), R(a2 + 2, b2 + 2))]
        its.append(mcq(["Which pair of ratios is equivalent?", "Which two ratios are equivalent to each other?"][j], right, wr,
                       "%s and %s both simplify to %s. Adding the same number to both terms, or switching the order, "
                       "makes a different ratio." % (R(k1 * p, k1 * q), R(k2 * p, k2 * q), R(p, q))))
    assert len(its) == 20, len(its)
    rnd.shuffle(its)
    return {"title": "Equivalent ratios and simplest form", "items": its}


# ------------------------------------------------------------ set 4: tape diagrams
def set_tape(rnd, P):
    its = []
    ctx = PAIRS[:]
    rnd.shuffle(ctx)
    k = [0]
    seen = set()

    def nxt():
        c = ctx[k[0] % len(ctx)]
        k[0] += 1
        return c

    def pqu(maxsum=9, ulo=2, uhi=12):
        while True:
            p, q = coprime_pair(rnd, 1, 7, maxsum)
            u = rnd.randint(ulo, uhi)
            if (p, q, u) not in seen and p * u > 1 and q * u > 1:
                seen.add((p, q, u))
                return p, q, u

    def stmt(c, p, q):
        X1, Xm, Y1, Ym, W, pl, la, lb = c
        return "The ratio of %s to %s %s %s is %s." % (Xm, Ym, prep(pl), pl, R(p, q))

    # 1) total and ratio -> one part (4 counts + 2 money)
    for i in range(6):
        p, q, u = pqu()
        T = (p + q) * u
        askX = i % 2 == 0
        ans, oth, n = (p * u, q * u, p) if askX else (q * u, p * u, q)
        if i < 4:
            c = nxt()
            X1, Xm, Y1, Ym, W, pl, la, lb = c
            one, many = (X1, Xm) if askX else (Y1, Ym)
            q_ = stmt(c, p, q) + " There are %d %s in all. How many %s are there?" % (T, W, many)
            U = lambda v: unit(v, one, many)
            rows = [(la, p, "", "?" if askX else ""), (lb, q, "", "" if askX else "?")]
            F_ = fig(tape_svg(rows, f(T), "tape diagram: %s to %s is %s, total %d" % (la, lb, R(p, q), T)))
            who = many
        else:
            (A, _, _), (B, _, _) = P.two()
            q_ = "%s and %s share $%d in the ratio %s. How much money does %s get?" % (A, B, T, R(p, q), A if askX else B)
            U = lambda v: "$" + f(v)
            rows = [(A, p, "", "?" if askX else ""), (B, q, "", "" if askX else "?")]
            F_ = fig(tape_svg(rows, "$%d" % T, "tape diagram: %s to %s is %s, total $%d" % (A, B, R(p, q), T)))
            who = A if askX else B
        cands = [U(oth), U(u), U(T // n) if T % n == 0 and n > 1 else None, U(T // abs(q - p)) if T % abs(q - p) == 0 and abs(q - p) > 1 else None,
                 U(ans + u), U(ans - u)]
        e = ("There are %d + %d = %d equal parts. Each part is %s ÷ %d = %s. %s: %d × %s = %s."
             % (p, q, p + q, U(T).split(" ")[0], p + q, U(u).split(" ")[0], cap(who), n, U(u).split(" ")[0], U(ans)))
        its.append(mcq(F_ + q_, U(ans), pick3(U(ans), cands), e))
    # 2) one quantity known -> the other quantity
    for i in range(5):
        c = nxt()
        X1, Xm, Y1, Ym, W, pl, la, lb = c
        while True:
            p, q, u = pqu()
            if p > 1:
                break
        A, B = p * u, q * u
        U = lambda v: unit(v, Y1, Ym)
        rows = [(la, p, "", f(A)), (lb, q, "", "?")]
        F_ = fig(tape_svg(rows, None, "tape diagram: %s to %s is %s, %s is %d" % (la, lb, R(p, q), la, A)))
        q_ = stmt(c, p, q) + " There are %s. How many %s are there?" % (unit(A, X1, Xm), Ym)
        cands = [U(A + q - p) if A + q - p > 0 else None, U(u), U(A + B), U(A * q), U(B + u)]
        e = ("%s fill %d equal parts, so each part is %d ÷ %d = %d. %s %s %d %s: %d × %d = %d. "
             "Adding the same number to both terms does not work." % (cap(Xm), p, A, p, u, cap(Ym), "are", q, "part" if q == 1 else "parts", q, u, B))
        its.append(mcq(F_ + q_, U(B), pick3(U(B), cands), e))
    # 3) one quantity known -> total
    for i in range(3):
        c = nxt()
        X1, Xm, Y1, Ym, W, pl, la, lb = c
        while True:
            p, q, u = pqu()
            if p > 1:
                break
        A, B = p * u, q * u
        T = A + B
        U = lambda v: unit(v, W[:-1] if W.endswith("s") else W, W)
        if W == "pieces of fruit":
            U = lambda v: unit(v, "piece of fruit", "pieces of fruit")
        rows = [(la, p, "", f(A)), (lb, q, "", "")]
        F_ = fig(tape_svg(rows, "?", "tape diagram: %s to %s is %s, %s is %d, total unknown" % (la, lb, R(p, q), la, A)))
        q_ = stmt(c, p, q) + " There are %s. How many %s are there in all?" % (unit(A, X1, Xm), W)
        cands = [U(B), U(A * (p + q)), U(T + u), U(A + q)]
        e = ("Each part is %d ÷ %d = %d. There are %d + %d = %d parts in all: %d × %d = %d."
             % (A, p, u, p, q, p + q, p + q, u, T))
        its.append(mcq(F_ + q_, U(T), pick3(U(T), cands), e))
    # 4) difference known (no picture)
    for i in range(3):
        c = nxt()
        X1, Xm, Y1, Ym, W, pl, la, lb = c
        while True:
            p, q, u = pqu()
            if q - p >= 2 and p >= 2:
                break
        d = (q - p) * u
        A, B = p * u, q * u
        if i == 0:
            ans, U, ask = A, (lambda v: unit(v, X1, Xm)), "How many %s are there?" % Xm
            cands = [U(d), U(d * p), U(B), U(u), U(A + u)]
        elif i == 1:
            ans, U, ask = B, (lambda v: unit(v, Y1, Ym)), "How many %s are there?" % Ym
            cands = [U(d), U(d * q), U(A), U(d + q)]
        else:
            Wone = W[:-1] if W.endswith("s") else W
            ans, U, ask = A + B, (lambda v: unit(v, Wone, W)), "How many %s are there in all?" % W
            cands = [U(d * (p + q)), U(d), U(B), U(A)]
        q_ = stmt(c, p, q) + " There are %d more %s than %s. %s" % (d, Ym, Xm, ask)
        e = ("%s have %d − %d = %d more parts than %s. Those %d parts are %d, so each part is %d ÷ %d = %d. "
             "%s: %d, %s: %d. So the answer is %s." % (cap(Ym), q, p, q - p, Xm, q - p, d, d, q - p, u,
                                                     cap(Xm), A, Ym, B, U(ans)))
        its.append(mcq(q_, U(ans), pick3(U(ans), cands), e))
    # 5) read a filled tape diagram
    for i in range(3):
        c = nxt()
        X1, Xm, Y1, Ym, W, pl, la, lb = c
        p, q, u = pqu(9, 3, 9)
        T = (p + q) * u
        Wone = "piece of fruit" if W == "pieces of fruit" else (W[:-1] if W.endswith("s") else W)
        U = lambda v: unit(v, Wone, W)
        rows = [(la, p, str(u), ""), (lb, q, "", "")]
        F_ = fig(tape_svg(rows, "?", "tape diagram: %s to %s is %s, each part %d" % (la, lb, R(p, q), u)))
        q_ = ("The tape diagram shows the ratio of %s to %s in %s. Every box stands for the same number. "
              "How many %s are there in all?" % (Xm, Ym, pl, W))
        cands = [U(p * u), U(q * u), U(p * u + q), U(p + q + u)]
        e = ("Every box is %d. There are %d + %d = %d boxes: %d × %d = %d. Count the boxes in both rows, not only the top row."
             % (u, p, q, p + q, p + q, u, T))
        its.append(mcq(F_ + q_, U(T), pick3(U(T), cands), e))
    assert len(its) == 20, len(its)
    rnd.shuffle(its)
    return {"title": "Tape diagrams: find the parts and the total", "items": its}


# ------------------------------------------------------------ set 5: word problems
def set_words(rnd, P):
    its = []

    def add(q, ans, cands, e):
        its.append(mcq(q, ans, pick3(ans, cands), e))

    cup = lambda v: unit(v, "cup", "cups")
    # recipes
    m = rnd.randint(2, 5)
    n, he, his = P.next()
    add("A pancake recipe uses 3 cups of flour for every 2 cups of milk. %s uses %s of flour. How much milk does %s need?"
        % (n, cup(3 * m), he), cup(2 * m), [cup(3 * m - 1), cup(m), cup(5 * m)],
        "%s of flour is %d groups of 3 cups (%d ÷ 3 = %d). Milk: %d × 2 = %d cups. "
        "Adding the same amount to both (%d − 3 + 2 = %d) does not keep the ratio." % (cup(3 * m), m, 3 * m, m, m, 2 * m, 3 * m, 3 * m - 1))
    m = rnd.choice([3, 6])
    add("A lemonade recipe uses 1 cup of lemon juice for every 4 cups of water. A big jug holds %d cups of lemonade. "
        "How many cups of lemon juice are in the jug?" % (5 * m), cup(m), [cup(4 * m), cup(5 * m // 3), cup(4)],
        "Each batch has 1 + 4 = 5 cups. %d ÷ 5 = %d batches, so there are %d × 1 = %s of lemon juice." % (5 * m, m, m, cup(m)))
    m = rnd.randint(2, 4)
    add("A trail mix has 2 cups of raisins for every 5 cups of peanuts. How many cups of raisins go with %s of peanuts?"
        % cup(5 * m), cup(2 * m), [cup(5 * m - 3), cup(m), cup(7 * m)],
        "%d ÷ 5 = %d, so there are %d groups. Raisins: %d × 2 = %s. Subtracting 3 from both terms does not keep the ratio."
        % (5 * m, m, m, m, cup(2 * m)))
    n, he, his = P.next()
    m = rnd.randint(3, 5)
    add("A banana bread recipe uses 3 bananas for every 2 cups of oats. %s has %d bananas and uses all of them. "
        "How many cups of oats does %s need?" % (n, 3 * m, he), cup(2 * m), [cup(3 * m - 1), cup(9 * m // 2) if m % 2 == 0 else cup(m), cup(5 * m)],
        "%d bananas is %d groups of 3. Oats: %d × 2 = %s. The ratio stays 3:2 because both terms are multiplied by %d."
        % (3 * m, m, m, cup(2 * m), m))
    # classes and schools
    m = rnd.choice([9, 18])
    T = lambda v: unit(v, "teacher", "teachers")
    add("On a field trip, the ratio of students to teachers is 8:1. There are %d students. How many teachers are there?" % (8 * m),
        T(m), [T(8 * m - 7), T(8 * m // 9), T(64 * m)],
        "For every 8 students, there is 1 teacher. %d ÷ 8 = %d groups, so there are %s. "
        "Do not multiply (%d × 8), and do not divide by 9: the %d are only the students." % (8 * m, m, T(m), 8 * m, 8 * m))
    m = rnd.randint(3, 5)
    S = lambda v: unit(v, "student", "students")
    add("A class has %d students. The ratio of boys to girls is 3:4. How many more girls than boys are in the class?" % (7 * m),
        S(m), [S(1), S(3 * m), S(4 * m)],
        "There are 3 + 4 = 7 parts, so each part is %d ÷ 7 = %d. Boys: 3 × %d = %d. Girls: 4 × %d = %d. "
        "%d − %d = %d more girls." % (7 * m, m, m, 3 * m, m, 4 * m, 4 * m, 3 * m, m))
    m = rnd.randint(3, 6)
    add("At a school, the ratio of students who walk to students who ride the bus is 2:5. %d students ride the bus. "
        "How many students walk?" % (5 * m), S(2 * m), [S(5 * m - 3), S(m), S(7 * m)],
        "%d ÷ 5 = %d, so each part is %d. Walkers: 2 × %d = %d. Taking 3 away from %d does not keep the ratio."
        % (5 * m, m, m, m, 2 * m, 5 * m))
    while True:
        p, q = coprime_pair(rnd, 2, 5, 9)
        g = rnd.randint(3, 6)
        if p < q:
            break
    a, b = p * g, q * g
    add("In a class of %d students, %d wear glasses and the rest do not. What is the ratio of students with glasses "
        "to students without glasses, in simplest form?" % (a + b, a), R(p, q), [R(q, p), R(p, p + q), R(q, p + q)],
        "Without glasses: %d − %d = %d. With to without is %s. Divide both by %d: %s." % (a + b, a, b, R(a, b), g, R(p, q)))
    # paint
    m = rnd.randint(3, 6)
    n, he, his = P.next()
    add("To make green paint, %s mixes 2 cups of blue paint for every 3 cups of yellow paint. %s uses %s of blue. "
        "How much yellow paint does %s need?" % (n, cap(he), cup(2 * m), he), cup(3 * m), [cup(2 * m + 1), cup(5 * m), cup(m)],
        "%d ÷ 2 = %d, so %s has %d groups. Yellow: %d × 3 = %s. %d + 1 = %d keeps the same difference, not the same ratio."
        % (2 * m, m, he, m, m, cup(3 * m), 2 * m, 2 * m + 1))
    p, q = rnd.choice([(2, 5), (3, 4), (1, 3)])
    k = rnd.randint(2, 4)
    mix = lambda r, w: "%s red, %s white" % (cup(r), cup(w))
    its.append(mcq("Pink paint is made with %s of red paint for every %s of white paint. Which mix makes the same shade of pink?"
                   % (cup(p), cup(q)), mix(k * p, k * q), [mix(p + k, q + k), mix(k * q, k * p), mix(k * p, q)],
                   "The same shade needs an equivalent ratio. Multiply both amounts by %d: %d × %d = %d and %d × %d = %d. "
                   "Adding %d cups to each changes the shade." % (k, p, k, k * p, q, k, k * q, k), same_ok=True))
    m = rnd.choice([2, 3, 4])
    add("Orange paint is 1 part red to 3 parts yellow. A painter needs %d cups of orange paint. How many cups of yellow paint "
        "does the painter use?" % (4 * m), cup(3 * m), [cup(m), cup(4 * m // 3) if (4 * m) % 3 == 0 else cup(2 * m), cup(4 * m - 3)],
        "1 + 3 = 4 parts. Each part is %d ÷ 4 = %d cups. Yellow is 3 parts: 3 × %d = %s." % (4 * m, m, m, cup(3 * m)))
    n, he, his = P.next()
    m = rnd.randint(2, 4)
    add("Light blue paint is 1 part blue to 4 parts white. %s has %s of blue paint and uses all of it. "
        "How many cups of light blue paint can %s make?" % (n, cup(m), he), cup(5 * m), [cup(4 * m), cup(m + 4), cup(5)],
        "White: 4 × %d = %d cups. Light blue paint is blue and white together: %d + %d = %s."
        % (m, 4 * m, m, 4 * m, cup(5 * m)))
    # sports
    p, q = rnd.choice([(5, 3), (3, 2), (7, 3)])
    m = rnd.randint(3, 4)
    G = lambda v: unit(v, "game", "games")
    add("A soccer team has a ratio of wins to losses of %s. It played %d games with no ties. How many games did it win?"
        % (R(p, q), (p + q) * m), G(p * m), [G(q * m), G(m), G((p - q) * m)],
        "%d + %d = %d parts. Each part is %d ÷ %d = %d. Wins: %d × %d = %d." % (p, q, p + q, (p + q) * m, p + q, m, p, m, p * m))
    n, he, his = P.next()
    m = rnd.randint(3, 6)
    Sh = lambda v: unit(v, "shot", "shots")
    add("For every 2 shots %s makes in basketball practice, %s misses 3. %s made %d shots. How many shots did %s miss?"
        % (n, he, cap(he), 2 * m, he), Sh(3 * m), [Sh(2 * m + 1), Sh(5 * m), Sh(m)],
        "%d ÷ 2 = %d groups. Each group has 3 misses: %d × 3 = %s." % (2 * m, m, m, Sh(3 * m)))
    p, q = rnd.choice([(4, 5), (5, 4), (2, 7)])
    m = rnd.randint(2, 3)
    Pl = lambda v: unit(v, "player", "players")
    tot = (p + q) * m
    add("A swim team has %d players. The ratio of girls to boys is %s. How many girls are on the team?" % (tot, R(p, q)),
        Pl(p * m), [Pl(q * m), Pl(m), Pl(tot // 2) if tot % 2 == 0 else Pl(p * m + m)],
        "%d + %d = %d parts. Each part is %d ÷ %d = %d. Girls: %d × %d = %d. The team is not split in half, because the ratio is not 1:1."
        % (p, q, p + q, tot, p + q, m, p, m, p * m))
    (A, heA, _), (B, _, _) = P.two()
    m = rnd.randint(4, 8)
    Pt = lambda v: unit(v, "point", "points")
    add("The ratio of points %s scored to points %s scored this season is 3:2. %s scored %d more points than %s. "
        "How many points did %s score?" % (A, B, A, m, B, A), Pt(3 * m), [Pt(m), Pt(2 * m), Pt(5 * m)],
        "3 − 2 = 1 part is the difference, so each part is %d. %s: 3 × %d = %s." % (m, A, m, Pt(3 * m)))
    # standard examples and more
    m = rnd.randint(21, 39)
    V = lambda v: unit(v, "vote", "votes")
    add("In a school election, for every vote Candidate A got, Candidate C got 3 votes. Candidate C got %d votes. "
        "How many votes did Candidate A get?" % (3 * m), V(m), [V(3 * m - 2), V(9 * m), V(4 * m)],
        "The ratio of A’s votes to C’s votes is 1:3. %d ÷ 3 = %d, so Candidate A got %s." % (3 * m, m, V(m)))
    m = rnd.randint(13, 24)
    Bk = lambda v: unit(v, "beak", "beaks")
    add("The ratio of wings to beaks in the bird house at the zoo is 2:1. There are %d wings. How many beaks are there?" % (2 * m),
        Bk(m), [Bk(4 * m), Bk(2 * m - 1), Bk(3 * m)],
        "For every 2 wings, there is 1 beak. %d ÷ 2 = %s." % (2 * m, Bk(m)))
    while True:
        p, q = coprime_pair(rnd, 2, 5, 9)
        g = rnd.randint(4, 7)
        if p != q:
            break
    add("A parking lot has %d cars and %d trucks. What is the ratio of trucks to cars in simplest form?" % (p * g, q * g),
        R(q, p), [R(p, q), R(q, p + q), R(p, p + q)],
        "Trucks to cars is %s. Divide both terms by %d: %s." % (R(q * g, p * g), g, R(q, p)))
    m = rnd.randint(4, 8)
    D = lambda v: unit(v, "juice box", "juice boxes")
    add("For a party, the ratio of juice boxes to water bottles is 3:1. There are %d drinks in all. How many are juice boxes?" % (4 * m),
        D(3 * m), [D(m), D(4 * m // 3) if (4 * m) % 3 == 0 else D(2 * m), D(2 * m)],
        "3 + 1 = 4 parts. Each part is %d ÷ 4 = %d. Juice boxes: 3 × %d = %d." % (4 * m, m, m, 3 * m))
    assert len(its) == 20, len(its)
    rnd.shuffle(its)
    return {"title": "Ratio word problems", "items": its}


# ------------------------------------------------------------ lesson
def body_html():
    pic = shapes_svg(["c", "s", "s", "c", "s", "c", "s", "c", "s", "s"])
    tape = tape_svg([("boys", 2, "8", "16"), ("girls", 3, "8", "24")], "40",
                    "tape diagram: boys to girls is 2:3, total 40, each part 8")
    return (
        "<h2>What is a ratio?</h2>"
        "<p>A <b>ratio</b> compares two amounts. You can write it three ways. They all mean the same thing:</p>"
        + table(["Write it", "Say it"], [
            ["4:6", "“4 to 6”"],
            ["4 to 6", "“4 to 6”"],
            ["for every 4 circles, there are 6 squares", "a “for every” sentence"],
        ])
        + "<figure class='sn-fig'>" + pic + "<figcaption>4 circles and 6 squares. The ratio of circles to squares is 4:6. "
        "The ratio of squares to circles is 6:4.</figcaption></figure>"
        "<p><b>Order matters.</b> The first number goes with the first thing named. 4:6 and 6:4 are different ratios.</p>"
        "<h2>Part-to-part and part-to-whole</h2>"
        "<p>A <b>part-to-part</b> ratio compares two parts. A <b>part-to-whole</b> ratio compares one part with the total.</p>"
        + table(["Ratio", "Type", "In the picture"], [
            ["circles to squares", "part to part", "4:6"],
            ["circles to all shapes", "part to whole", "4:10"],
            ["squares to all shapes", "part to whole", "6:10"],
        ])
        + "<p>A part-to-whole ratio is also a fraction: " + fr(4, 10) + " of the shapes are circles.</p>"
        "<h2>Equivalent ratios</h2>"
        "<p>Multiply or divide <b>both</b> terms by the same number. The ratio stays the same.</p>"
        + ex("Example", "Write 4:6 in simplest form.",
             "4 and 6 can both be divided by 2. 4 ÷ 2 = 2 and 6 ÷ 2 = 3.", "2:3. For every 2 circles, there are 3 squares.")
        + "<h2>Tape diagrams</h2>"
        "<p>Draw one box for each part of the ratio. Every box is the same size.</p>"
        + ex("Example", "The ratio of boys to girls in a club is 2:3. There are 40 students. How many are boys and how many are girls?",
             "2 + 3 = 5 equal boxes. 40 ÷ 5 = 8 in each box. Boys: 2 × 8 = 16. Girls: 3 × 8 = 24.", "16 boys and 24 girls")
        + "<figure class='sn-fig'>" + tape + "<figcaption>5 equal boxes make 40, so each box is 8. "
        "Check: 16 + 24 = 40, and 16:24 = 2:3.</figcaption></figure>"
        "<h2>Common mistakes</h2>"
        + table(["Mistake", "What to do instead"], [
            ["Writing the numbers in the wrong order (6:4 for circles to squares)", "Write the first thing named first: 4:6"],
            ["Using the total when the question asks for two parts (4:10)", "Part to part: 4:6. Use the total only for “to all”"],
            ["Adding the same number to both terms (2:3 → 4:5)", "Multiply both terms by the same number: 2:3 = 4:6"],
            ["Dividing the total by one term (40 ÷ 2 = 20 boys)", "Divide by the number of parts: 40 ÷ 5 = 8 in each part"],
            ["Using the difference of the terms (40 ÷ 1)", "Use the difference only when the problem gives “how many more”"],
        ])
    )


FAQ = [
    {"q": "What is a ratio in 6th grade math?",
     "a": "A ratio compares two amounts, such as 3 cups of flour for every 2 cups of milk. It can be written 3:2, 3 to 2, or “for every 3 … there are 2 ….”"},
    {"q": "What is the difference between a part-to-part and a part-to-whole ratio?",
     "a": "Part-to-part compares two parts, like 4 boys to 6 girls (4:6). Part-to-whole compares one part with the total, like 4 boys to 10 students (4:10)."},
    {"q": "How do you write a ratio in simplest form?",
     "a": "Divide both terms by the greatest number that divides both. For 6:9, divide both by 3 to get 2:3."},
    {"q": "How do you solve a ratio problem with a tape diagram?",
     "a": "Draw one box for each part of the ratio, divide the total by the number of boxes, then multiply. For 2:3 with a total of 40, each of the 5 boxes is 8, so the parts are 16 and 24."},
]


def gen():
    rnd = random.Random(601)
    P = People(rnd)
    sets = [set_pictures(rnd), set_language(rnd), set_equivalent(rnd), set_tape(rnd, P), set_words(rnd, P)]
    balance(sets, rnd)
    seen = set()
    for s in sets:
        assert len(s["items"]) == 20, (s["title"], len(s["items"]))
        for it in s["items"]:
            assert len(set(it["c"])) == 4, it
            assert it["q"] not in seen, it["q"]
            seen.add(it["q"])
    return {
        "country": "us", "subject": "math", "grade": "grade-6", "slug": "ratios", "sort": 1,
        "updated": UPDATED, "pdf_url": "",
        "title": "Understanding Ratios",
        "seo_title": "Grade 6 Ratio Worksheets: Ratio Language, Part-to-Whole, Equivalent Ratios and Tape Diagrams",
        "short_title": "Ratios",
        "domain": "Ratios and Proportional Relationships",
        "standard_code": "6.RP.A.1",
        "standard_url": "https://www.thecorestandards.org/Math/Content/6/RP/A/1/",
        "standard_text": "Understand the concept of a ratio and use ratio language to describe a ratio relationship between two quantities. For example, “The ratio of wings to beaks in the bird house at the zoo was 2:1, because for every 2 wings there was 1 beak.” “For every vote candidate A received, candidate C received nearly three votes.”",
        "meta_desc": "Free Grade 6 ratio worksheets: write ratios from pictures, use ratio language (3:5, 3 to 5, for every), tell part-to-part from part-to-whole, find equivalent ratios and simplest form, and solve tape diagram and word problems. 100 practice questions with an answer key and explanations.",
        "key_big": "A ratio compares two amounts. Order matters: 3:5 is not 5:3.",
        "key_sub": "3:5, 3 to 5 and “for every 3 … there are 5 …” all mean the same ratio. Multiply or divide both terms by the same number to get an equivalent ratio: 3:5 = 6:10.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    mark_large(u, "tape diagram")
    mark_large(u, "shapes picture")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
