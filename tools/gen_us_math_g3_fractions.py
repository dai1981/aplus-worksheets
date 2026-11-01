# -*- coding: utf-8 -*-
"""
US Grade 3 Math: Understanding Fractions (3.NF.A.1, 3.NF.A.2, 3.NF.A.3)
  python tools/gen_us_math_g3_fractions.py
Grade 3 denominators only: 2, 3, 4, 6, 8.
HTML attributes use single quotes (no backslashes in the JSON).
"""
import json, math, os, random

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "us", "math", "grade-3")
UPDATED = "2026-11-01"
GREEN = "#006633"
FILL = "#4fae74"      # shaded part
LINE = "#2b2b2b"
DENS = [2, 3, 4, 6, 8]
NAMES = ["Maya", "Leo", "Ava", "Noah", "Mia", "Eli", "Zoe", "Sam", "Lily", "Ben", "Emma", "Omar", "Kai", "Nora"]
WORD = {2: "halves", 3: "thirds", 4: "fourths", 6: "sixths", 8: "eighths"}


# ------------------------------------------------------------ helpers
def fr(a, b):
    return "<span class='fr'><span class='fn'>%d</span><span class='fd'>%d</span></span>" % (a, b)


def mcq(q, correct, cands, e, rnd):
    seen = {correct}
    pick = []
    for c in cands:
        if c in seen or not c:
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


def bar_svg(n, k, W=260, H=50, widths=None, label=None):
    """Bar split into n parts (equal unless widths given), first k shaded."""
    x = 6
    s = []
    ws = widths or [W / n] * n
    for i, w in enumerate(ws):
        s.append("<rect x='%.1f' y='6' width='%.1f' height='%d' fill='%s' stroke='%s' stroke-width='2.5'/>"
                 % (x, w, H, FILL if i < k else "#fff", LINE))
        x += w
    return svg_wrap(W + 12, H + 12, "".join(s), label or "bar split into %d parts with %d shaded" % (n, k))


def circle_svg(n, k, r=62):
    cx = cy = r + 6
    s = []
    for i in range(n):
        a0 = math.radians(-90 + 360.0 * i / n)
        a1 = math.radians(-90 + 360.0 * (i + 1) / n)
        x0, y0 = cx + r * math.cos(a0), cy + r * math.sin(a0)
        x1, y1 = cx + r * math.cos(a1), cy + r * math.sin(a1)
        s.append("<path d='M%.1f %.1f L%.1f %.1f A%d %d 0 0 1 %.1f %.1f Z' fill='%s' stroke='%s' stroke-width='2.5' stroke-linejoin='round'/>"
                 % (cx, cy, x0, y0, r, r, x1, y1, FILL if i < k else "#fff", LINE))
    d = 2 * r + 12
    return svg_wrap(d, d, "".join(s), "circle split into %d equal parts with %d shaded" % (n, k))


def grid_svg(rows, cols, k, cell=40):
    s = []
    i = 0
    for r in range(rows):
        for c in range(cols):
            s.append("<rect x='%d' y='%d' width='%d' height='%d' fill='%s' stroke='%s' stroke-width='2.5'/>"
                     % (6 + c * cell, 6 + r * cell, cell, cell, FILL if i < k else "#fff", LINE))
            i += 1
    return svg_wrap(cols * cell + 12, rows * cell + 12, "".join(s),
                    "rectangle split into %d equal parts with %d shaded" % (rows * cols, k))


GRIDS = {4: (2, 2), 6: (2, 3), 8: (2, 4)}


def shape_svg(n, k, kind):
    if kind == "circle":
        return circle_svg(n, k)
    if kind == "grid" and n in GRIDS:
        return grid_svg(GRIDS[n][0], GRIDS[n][1], k)
    return bar_svg(n, k)


def line_svg(d, k, wholes=1, W=380):
    """Number line 0..wholes, ticks every 1/d, red dot at k/d."""
    L, R, Y = 24, W - 24, 46
    total = d * wholes
    def X(i):
        return L + (R - L) * i / total
    s = ["<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='2.5'/>" % (L, Y, R, Y, LINE)]
    for i in range(total + 1):
        whole = (i % d == 0)
        s.append("<line x1='%.1f' y1='%d' x2='%.1f' y2='%d' stroke='%s' stroke-width='%s'/>"
                 % (X(i), Y - (13 if whole else 8), X(i), Y + (13 if whole else 8), LINE, "2.5" if whole else "1.8"))
        if whole:
            s.append("<text x='%.1f' y='%d' font-size='17' font-weight='700' fill='%s' text-anchor='middle'>%d</text>"
                     % (X(i), Y + 36, LINE, i // d))
    if k is not None:
        s.append("<circle cx='%.1f' cy='%d' r='8' fill='#d6453b'/>" % (X(k), Y))
    return svg_wrap(W, 92, "".join(s), "number line from 0 to %d split into %d equal parts per whole" % (wholes, d))


def two_bars_svg(n1, k1, n2, k2, W=260, H=40):
    s = []
    for row, (n, k) in enumerate([(n1, k1), (n2, k2)]):
        y = 6 + row * (H + 14)
        for i in range(n):
            s.append("<rect x='%.1f' y='%d' width='%.1f' height='%d' fill='%s' stroke='%s' stroke-width='2.5'/>"
                     % (6 + i * W / n, y, W / n, H, FILL if i < k else "#fff", LINE))
    return svg_wrap(W + 12, 2 * H + 26, "".join(s), "two bars of the same size")


def table(head, rows):
    h = "".join("<th>%s</th>" % x for x in head)
    b = "".join("<tr>" + "".join("<td>%s</td>" % c for c in r) + "</tr>" for r in rows)
    return "<div class='sn-tw'><table class='sn-table'><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>" % (h, b)


def ex(title, q, s, a):
    return ("<div class='sn-ex'><span class='sn-ex-t'>%s</span><p class='sn-ex-q'>%s</p>"
            "<p class='sn-ex-s'>%s</p><p class='sn-ex-a'>Answer: %s</p></div>" % (title, q, s, a))


def frac_cands(a, b):
    """Typical wrong answers for 'a/b shaded'."""
    c = [fr(b - a, b) if b - a > 0 else None, fr(a, b + 1), fr(a, b - a) if b - a > 0 else None,
         fr(b, a) if a > 0 else None, fr(a + 1, b) if a + 1 <= b else None, fr(a, b + 2), fr(a - 1, b) if a > 1 else None]
    return [x for x in c if x]


# ============================================================ set 1: what fraction is shaded?
def set_shaded(rnd):
    its = []
    kinds = ["bar", "circle", "grid"]
    combos = [(n, k) for n in DENS for k in range(1, n)]
    rnd.shuffle(combos)
    for i, (n, k) in enumerate(combos[:12]):
        kind = kinds[i % 3]
        if kind == "grid" and n not in GRIDS:
            kind = "bar"
        e = ("The whole has <b>%d equal parts</b>, so the bottom number is %d. <b>%s shaded, "
             "so the top number is %d. The shaded part is %s." % (n, n, "1 part</b> is" if k == 1 else "%d parts</b> are" % k, k, fr(k, n)))
        its.append(mcq(fig(shape_svg(n, k, kind)) + "What fraction of the shape is shaded?",
                       fr(k, n), frac_cands(k, n), e, rnd))

    # what fraction is NOT shaded
    for n, k in [(4, 1), (6, 2), (8, 3)]:
        e = ("There are %d equal parts and %d are shaded, so %d − %d = <b>%d parts are not shaded</b>. "
             "That is %s." % (n, k, n, k, n - k, fr(n - k, n)))
        its.append(mcq(fig(shape_svg(n, k, "bar" if n != 6 else "circle")) + "What fraction of the shape is <b>not</b> shaded?",
                       fr(n - k, n), [fr(k, n), fr(n - k, k), fr(n - k, n + 1), fr(n, n - k)], e, rnd))

    # equal parts
    eq = [
        (4, [0.16, 0.34, 0.2, 0.3], False),
        (3, [1 / 3.0] * 3, True),
        (3, [0.2, 0.5, 0.3], False),
        (6, [1 / 6.0] * 6, True),
        (4, [0.25] * 4, True),
    ]
    rnd.shuffle(eq)
    for n, ws, ok in eq[:5]:
        widths = [w * 260 for w in ws]
        svg = bar_svg(n, 1, widths=widths, label="bar split into %d parts" % n)
        right = ("Yes. It has %d equal parts." % n) if ok else "No. The parts are not equal."
        cands = ["Yes. Any %d parts make %s." % (n, WORD[n]), "No. It needs more parts.",
                 ("No. The parts are not equal." if ok else "Yes. It has %d equal parts." % n),
                 "Yes. One part is shaded."]
        e = ("Fractions only work with <b>equal parts</b>. " +
             ("All %d parts are the same size, so each part is %s of the whole." % (n, fr(1, n)) if ok
              else "These %d parts are different sizes, so they are <b>not</b> %s." % (n, WORD[n])))
        its.append(mcq(fig(svg) + "Is this bar split into <b>%s</b>?" % WORD[n], right, cands, e, rnd))
    assert len(its) == 20
    return {"title": "What fraction is shaded?", "items": its}


# ============================================================ set 2: unit fractions & number lines
def set_line(rnd):
    its = []
    # building fractions from unit fractions
    for a, b in [(3, 4), (5, 6), (2, 3), (7, 8), (4, 6), (3, 8)]:
        plus = " + ".join([fr(1, b)] * a)
        if (a + b) % 2:
            q = "%s = ?" % plus
            e = ("You are adding <b>%d pieces</b> that are each %s. %d pieces of size %s make %s."
                 % (a, fr(1, b), a, fr(1, b), fr(a, b)))
            its.append(mcq(q, fr(a, b), [fr(a, a * b) if a * b <= 64 else None, fr(1, a * b), fr(a, b + a), fr(1, b), fr(b, a)], e, rnd))
        else:
            q = "How many %s pieces make %s?" % (fr(1, b), fr(a, b))
            e = "%s means <b>%d</b> pieces that are each %s: %s." % (fr(a, b), a, fr(1, b), plus)
            its.append(mcq(q, str(a), [str(b), str(a + 1), str(b - a) if b - a != a else str(a + 2), "1"], e, rnd))

    # point on a number line
    pts = [(d, k, 1) for d in DENS for k in range(1, d)]
    rnd.shuffle(pts)
    pts = pts[:11] + [(4, 5, 2), (3, 4, 2), (2, 3, 2)]
    for d, k, wh in pts:
        e = ("Count the <b>spaces</b>, not the tick marks. From 0 to 1 there are <b>%d equal spaces</b>, so each space is %s. "
             "The dot is <b>%d %s</b> from 0, so it is at %s." % (d, fr(1, d), k, "space" if k == 1 else "spaces", fr(k, d)))
        if k > d:
            e += " It is past 1 because %s is more than %s." % (fr(k, d), fr(d, d))
        cands = [fr(k, d + 1), fr(k + 1, d), fr(k - 1, d) if k > 1 else None, fr(d, k), fr(k, wh * d + 1)]
        its.append(mcq(fig(line_svg(d, k, wh)) + "What fraction is at the red dot?", fr(k, d),
                       [c for c in cands if c], e, rnd))
    assert len(its) == 20
    return {"title": "Unit fractions and number lines", "items": its}


# ============================================================ set 3: equivalent fractions & wholes
EQ = [((1, 2), (2, 4)), ((1, 2), (3, 6)), ((1, 2), (4, 8)), ((1, 3), (2, 6)), ((2, 3), (4, 6)),
      ((1, 4), (2, 8)), ((3, 4), (6, 8)), ((2, 4), (4, 8)), ((1, 2), (2, 4)), ((2, 3), (4, 6))]


def set_equiv(rnd):
    its = []
    for (a, b), (c, d) in EQ[:8]:
        q = (fig(two_bars_svg(b, a, d, c)) + "Both bars show the same amount.<br>%s = "
             "<span class='fr'><span class='fn'><b>?</b></span><span class='fd'>%d</span></span>" % (fr(a, b), d))
        e = ("Both bars have the same amount shaded. The bottom bar has %d equal parts and <b>%d</b> are shaded, "
             "so %s = %s." % (d, c, fr(a, b), fr(c, d)))
        its.append(mcq(q, str(c), [str(c + 1), str(c - 1) if c > 1 else str(c + 2), str(a), str(d - c) if d - c != c else str(d)], e, rnd))

    for (a, b), (c, d) in [((1, 2), (3, 6)), ((2, 3), (4, 6)), ((1, 4), (2, 8)), ((3, 4), (6, 8)), ((1, 3), (2, 6)), ((1, 2), (4, 8))]:
        wrong = [fr(c, d + 1), fr(a + 1, b + 1) if a + 1 < b + 1 else fr(a, b + 1), fr(c - 1, d), fr(b, a), fr(a, d)]
        e = ("Equivalent fractions show the <b>same amount</b>. Cut each %s piece into %d smaller pieces: "
             "%s becomes %s." % (fr(1, b), d // b, fr(a, b), fr(c, d)))
        its.append(mcq("Which fraction is <b>equal</b> to %s?" % fr(a, b), fr(c, d), wrong, e, rnd))

    whole = [
        ("%s = ?" % fr(4, 4), "1", ["4", "0", fr(1, 4)], "%s means all 4 of the 4 equal parts. That is <b>one whole</b>." % fr(4, 4)),
        ("%s = ?" % fr(6, 1), "6", ["1", fr(1, 6), "0"], "%s means 6 wholes, each cut into just 1 part. That is <b>6</b>." % fr(6, 1)),
        ("Which fraction is equal to 1?", fr(8, 8), [fr(1, 8), fr(8, 1), fr(7, 8)], "When the top and bottom numbers are the same, every part is taken: %s = 1." % fr(8, 8)),
        ("Which fraction is equal to 3?", fr(3, 1), [fr(1, 3), fr(3, 3), fr(3, 4)], "A bottom number of 1 means each whole has 1 part. 3 parts = 3 wholes, so %s = 3." % fr(3, 1)),
        (fig(line_svg(3, 6, 2)) + "The dot is on a whole number. Which fraction names it?", fr(6, 3),
         [fr(2, 3), fr(3, 6), fr(6, 2)], "Each whole has 3 equal spaces. The dot is 6 spaces from 0: %s, which is the same as 2." % fr(6, 3)),
        ("%s = ?" % fr(2, 2), "1", ["2", "0", fr(1, 2)], "Both halves are taken, so %s is one whole: <b>1</b>." % fr(2, 2)),
    ]
    for q, a, w, e in whole:
        its.append(mcq(q, a, w + ["2"], e, rnd))
    assert len(its) == 20
    return {"title": "Equivalent fractions and whole numbers", "items": its}


# ============================================================ set 4: comparing
def cmp_choices(a, b, c, d, sign):
    lt = "%s &lt; %s" % (fr(a, b), fr(c, d))
    gt = "%s &gt; %s" % (fr(a, b), fr(c, d))
    eq = "%s = %s" % (fr(a, b), fr(c, d))
    return {"<": lt, ">": gt, "=": eq}[sign], [lt, gt, eq, "You can’t compare them"]


def set_compare(rnd):
    its = []
    # same denominator
    for _ in range(7):
        b = rnd.choice([4, 6, 8])
        a, c = rnd.sample(range(1, b), 2)
        sign = "<" if a < c else ">"
        right, ch = cmp_choices(a, b, c, b, sign)
        e = ("Same bottom number: the pieces are the <b>same size</b>. Compare how many pieces: %d %s %d, so %s."
             % (a, "is less than" if a < c else "is more than", c, right))
        its.append(mcq("Compare the fractions.", right, ch, e, rnd))
    # same numerator
    pairs = [(1, 3, 1, 6), (1, 8, 1, 4), (2, 3, 2, 8), (3, 4, 3, 6), (1, 2, 1, 8), (2, 6, 2, 4), (3, 8, 3, 4)]
    for i, (a, b, c, d) in enumerate(pairs):
        sign = "<" if b > d else ">"
        right, ch = cmp_choices(a, b, c, d, sign)
        q = "Compare the fractions."
        if i < 3:
            q = fig(two_bars_svg(b, a, d, c)) + "The bars are the same size. Compare the fractions."
        e = ("Same top number: you have the <b>same number of pieces</b>. Fewer parts in the whole means <b>bigger</b> pieces, "
             "so %s pieces are bigger than %s pieces. That makes %s." % (fr(1, min(b, d)), fr(1, max(b, d)), right))
        its.append(mcq(q, right, ch, e, rnd))
    # equal
    for (a, b), (c, d) in [((1, 2), (2, 4)), ((2, 3), (4, 6))]:
        right, ch = cmp_choices(a, b, c, d, "=")
        e = "%s and %s cover the <b>same amount</b> of the whole, so they are equal." % (fr(a, b), fr(c, d))
        its.append(mcq(fig(two_bars_svg(b, a, d, c)) + "Compare the fractions.", right, ch, e, rnd))
    # greatest of four
    for b in [8, 6]:
        nums = rnd.sample(range(1, b), 4)
        best = max(nums)
        e = "All the fractions have the same bottom number, so the pieces are the same size. The most pieces wins: %s." % fr(best, b)
        its.append(mcq("Which fraction is the <b>greatest</b>?", fr(best, b), [fr(x, b) for x in nums if x != best], e, rnd))
    for a in [1, 2]:
        dens = [d for d in DENS if d > a]
        rnd.shuffle(dens)
        dens = dens[:4]
        small = max(dens)
        e = ("All the fractions have the same top number. The biggest bottom number means the <b>smallest</b> pieces: %s."
             % fr(a, small))
        its.append(mcq("Which fraction is the <b>smallest</b>?", fr(a, small), [fr(a, d) for d in dens if d != small], e, rnd))
    assert len(its) == 20, len(its)
    return {"title": "Compare fractions", "items": its}


# ============================================================ set 5: word problems
def set_words(rnd):
    its = []
    names = NAMES[:]
    rnd.shuffle(names)
    nm = iter(names * 3)

    food = [("pizza", "slices", 8), ("pan of brownies", "pieces", 6), ("chocolate bar", "pieces", 8),
            ("pie", "slices", 6), ("sandwich", "pieces", 4), ("watermelon", "slices", 8)]
    for i, (thing, parts, n) in enumerate(food):
        k = rnd.randint(1, n - 1)
        p = next(nm)
        if i % 2 == 0:
            verb = "planted flowers in" if thing == "garden" else "ate"
            q = "A %s is cut into %d equal %s. %s %s %d of them. What fraction of the %s did %s %s?" % (
                thing, n, parts, p, verb, k, thing, p, "use" if thing == "garden" else "eat")
            if thing == "garden":
                q = "A garden is split into %d equal beds. %s planted flowers in %d of them. What fraction of the garden has flowers?" % (n, p, k)
            e = "The whole is %d equal %s, so the bottom number is %d. %d were used, so the answer is %s." % (n, parts, n, k, fr(k, n))
            its.append(mcq(q, fr(k, n), frac_cands(k, n), e, rnd))
        else:
            q = "A %s is cut into %d equal %s. %s ate %d of them. What fraction of the %s is <b>left</b>?" % (thing, n, parts, p, k, thing)
            e = "%d − %d = <b>%d %s are left</b> out of %d equal %s. The answer is %s." % (n, k, n - k, parts, n, parts, fr(n - k, n))
            its.append(mcq(q, fr(n - k, n), [fr(k, n), fr(n - k, k), fr(k, n - k), fr(n - k, n + 1)], e, rnd))

    # who has more (same numerator: same-size wholes)
    ctx = [("ran", None), ("painted", "fence"), ("filled", "jug"), ("mowed", "lawn"),
           ("swam", None), ("drank", "water bottle")]
    for i, (a, b, d) in enumerate([(3, 4, 8), (2, 3, 6), (1, 2, 4), (5, 6, 8), (1, 3, 8), (3, 6, 8)]):
        p1, p2 = next(nm), next(nm)
        v, thing = ctx[i]
        if thing is None:
            w = "of a mile" if v == "ran" else "of the pool"
            q = "%s %s %s %s. %s %s %s %s. Who %s more?" % (p1, v, fr(a, b), w, p2, v, fr(a, d), w, v)
        else:
            q = ("There are two %ss of the same size. %s %s %s of one %s. %s %s %s of the other. Who %s more?"
                 % (thing, p1, v, fr(a, b), thing, p2, v, fr(a, d), v))
        e = ("Both have <b>%d %s</b>. %s pieces are bigger than %s pieces, so %s is more than %s. <b>%s</b> %s more."
             % (a, "piece" if a == 1 else "pieces", fr(1, b), fr(1, d), fr(a, b), fr(a, d), p1, v))
        its.append(mcq(q, p1, [p2, "They are the same", "You can’t tell"], e, rnd))

    # same denominator comparisons
    for i in range(3):
        b = rnd.choice([4, 6, 8])
        a, c = sorted(rnd.sample(range(1, b), 2))
        p1, p2 = next(nm), next(nm)
        q = "%s ate %s of a pizza. %s ate %s of the same size pizza. Who ate <b>less</b>?" % (p1, fr(c, b), p2, fr(a, b))
        e = "The pieces are the same size (%s). %d pieces is less than %d pieces, so <b>%s</b> ate less." % (fr(1, b), a, c, p2)
        its.append(mcq(q, p2, [p1, "They ate the same", "You can’t tell"], e, rnd))

    # equal amounts
    for (a, b), (c, d) in [((1, 2), (4, 8)), ((1, 3), (2, 6))]:
        p1, p2 = next(nm), next(nm)
        q = "%s walked %s of a mile. %s walked %s of a mile. Who walked farther?" % (p1, fr(a, b), p2, fr(c, d))
        e = "%s and %s are <b>equivalent</b>: they are the same distance. Neither walked farther." % (fr(a, b), fr(c, d))
        its.append(mcq(q, "They walked the same distance", [p1, p2, "You can’t tell"], e, rnd))

    # how many pieces make a whole / sharing
    for b, thing in [(3, "ribbon"), (6, "cake")]:
        q = "A %s is cut into pieces that are each %s of the whole. How many pieces make the whole %s?" % (thing, fr(1, b), thing)
        e = "Each piece is %s, so it takes <b>%d</b> pieces to make %s = 1 whole." % (fr(1, b), b, fr(b, b))
        its.append(mcq(q, "%d pieces" % b, ["1 piece", "%d pieces" % (b - 1), "%d pieces" % (b + 1), "%d pieces" % (2 * b)], e, rnd))

    q = "4 friends share a sandwich equally. What fraction of the sandwich does each friend get?"
    e = "The sandwich is split into 4 equal parts and each friend gets 1 part: %s." % fr(1, 4)
    its.append(mcq(q, fr(1, 4), [fr(4, 1), fr(1, 3), fr(3, 4), fr(4, 4)], e, rnd))
    assert len(its) == 20, len(its)
    return {"title": "Fraction word problems", "items": its}


# ============================================================ lesson
def body_html():
    anat = (
        "<figure class='sn-fig'>" + bar_svg(4, 3, W=320, H=56) +
        "<figcaption>4 equal parts, 3 shaded: " + fr(3, 4) + " of the bar is shaded.</figcaption></figure>"
    )
    eq_fig = svg_wrap(372, 168, "".join(
        ["<text x='0' y='%d' font-size='18' font-weight='800' fill='%s'>%s</text>" % (28 + r * 54, LINE, lab) for r, lab in enumerate(["1/2", "2/4", "4/8"])] +
        ["<rect x='%.1f' y='%d' width='%.1f' height='38' fill='%s' stroke='%s' stroke-width='2.5'/>"
         % (56 + i * 300.0 / n, 6 + r * 54, 300.0 / n, FILL if i < n // 2 else "#fff", LINE)
         for r, n in enumerate([2, 4, 8]) for i in range(n)]), "one half, two fourths and four eighths shaded on three bars of the same size")
    cmp_fig = svg_wrap(372, 114, "".join(
        ["<text x='0' y='%d' font-size='18' font-weight='800' fill='%s'>%s</text>" % (32 + r * 56, LINE, lab) for r, lab in enumerate(["1/3", "1/6"])] +
        ["<rect x='%.1f' y='%d' width='%.1f' height='42' fill='%s' stroke='%s' stroke-width='2.5'/>"
         % (56 + i * 300.0 / n, 6 + r * 56, 300.0 / n, FILL if i < 1 else "#fff", LINE)
         for r, n in enumerate([3, 6]) for i in range(n)]), "one third is bigger than one sixth")

    return (
        "<h2>What a fraction means</h2>"
        "<p>A fraction is a number that names <b>part of a whole</b>. The whole must be cut into <b>equal parts</b>.</p>"
        + anat +
        table(["Part", "What it tells you", "In " + fr(3, 4)], [
            ["Bottom number (denominator)", "How many <b>equal parts</b> make one whole", "4 equal parts"],
            ["Top number (numerator)", "How many of those parts you have", "3 parts"],
        ]) +
        "<p>A fraction with 1 on top, like " + fr(1, 4) + ", is a <b>unit fraction</b>: just one piece. "
        "Every fraction is made of unit fractions: " + fr(3, 4) + " = " + fr(1, 4) + " + " + fr(1, 4) + " + " + fr(1, 4) + ".</p>"
        "<h2>Fractions on a number line</h2>"
        "<p>Split the space from 0 to 1 into equal spaces. Each space is one unit fraction. "
        "Count <b>spaces</b> from 0, not tick marks.</p>"
        "<figure class='sn-fig'>" + line_svg(4, 3) +
        "<figcaption>From 0 to 1 there are 4 equal spaces, so each space is " + fr(1, 4) + ". The dot is 3 spaces from 0: it is at " + fr(3, 4) + ".</figcaption></figure>"
        + ex("Example", "Where is " + fr(5, 4) + " on a number line?",
             "Each whole has 4 spaces. Count 5 spaces from 0: 4 spaces reach 1, then 1 more.", "just past 1, one space after 1")
        + "<h2>Equivalent fractions</h2>"
        "<p>Different fractions can name the <b>same amount</b>. These are called <b>equivalent fractions</b>.</p>"
        "<figure class='sn-fig'>" + eq_fig +
        "<figcaption>The shaded parts are the same size: " + fr(1, 2) + " = " + fr(2, 4) + " = " + fr(4, 8) + ".</figcaption></figure>"
        "<p>Whole numbers can be fractions too: " + fr(4, 4) + " = 1 (all 4 parts), and " + fr(3, 1) + " = 3 (3 wholes).</p>"
        "<h2>Comparing fractions</h2>"
        + table(["When", "Rule", "Example"], [
            ["Same bottom number", "Pieces are the same size. <b>More pieces</b> is greater.", fr(5, 8) + " &gt; " + fr(3, 8)],
            ["Same top number", "Same number of pieces. <b>Smaller bottom number</b> means bigger pieces.", fr(1, 3) + " &gt; " + fr(1, 6)],
            ["Same amount", "They are equivalent.", fr(1, 2) + " = " + fr(2, 4)],
        ]) +
        "<figure class='sn-fig'>" + cmp_fig +
        "<figcaption>Cut the same bar into 3 parts or into 6 parts. Each third is bigger than each sixth, so " + fr(1, 3) + " &gt; " + fr(1, 6) + ".</figcaption></figure>"
        "<p>You can only compare fractions of the <b>same size whole</b>. Half of a large pizza is more than half of a small pizza.</p>"
        + ex("Example", "Which is greater: " + fr(2, 3) + " or " + fr(2, 8) + "?",
             "Both have 2 pieces. Thirds are bigger pieces than eighths.", fr(2, 3) + " is greater")
        + "<h2>Common mistakes</h2>"
        + table(["Mistake", "What to do instead"], [
            ["Thinking " + fr(1, 8) + " is bigger than " + fr(1, 4) + " because 8 is bigger than 4", "A bigger bottom number means <b>smaller</b> pieces"],
            ["Counting tick marks on a number line", "Count the <b>spaces</b> between the marks"],
            ["Naming a shape with unequal parts", "Fractions need <b>equal</b> parts"],
            ["Writing the shaded part on the bottom", "Bottom: parts in the whole. Top: parts you have"],
        ])
    )


FAQ = [
    {"q": "What fractions do 3rd graders learn?",
     "a": "In Grade 3, students work with halves, thirds, fourths, sixths and eighths. They learn what fractions mean, place them on a number line, find equivalent fractions and compare fractions."},
    {"q": "How do you explain the numerator and denominator?",
     "a": "The denominator (bottom number) says how many equal parts make one whole. The numerator (top number) says how many of those parts you have. In 3/4, the whole has 4 equal parts and you have 3."},
    {"q": "Why is 1/3 bigger than 1/6?",
     "a": "Cut two same-size bars: one into 3 parts and one into 6 parts. Each third is bigger than each sixth, because the whole is shared by fewer pieces."},
    {"q": "How do you find a fraction on a number line?",
     "a": "Look at how many equal spaces there are between 0 and 1. That number is the denominator. Count the spaces from 0 to the point. That number is the numerator."},
    {"q": "What are equivalent fractions?",
     "a": "Equivalent fractions name the same amount, like 1/2, 2/4 and 4/8. You can see it with same-size bars: the shaded parts line up exactly."},
]


def gen_fractions():
    rnd = random.Random(35)
    sets = [set_shaded(rnd), set_line(rnd), set_equiv(rnd), set_compare(rnd), set_words(rnd)]
    for s in sets:
        assert len(s["items"]) == 20
        for it in s["items"]:
            assert len(set(it["c"])) == 4, it
    return {
        "country": "us", "subject": "math", "grade": "grade-3", "slug": "fractions", "sort": 4,
        "updated": UPDATED, "pdf_url": "",
        "title": "Understanding Fractions",
        "seo_title": "Grade 3 Fractions Worksheets: Fraction Models, Number Lines, Equivalent and Comparing Fractions",
        "short_title": "Fractions",
        "domain": "Number and Operations—Fractions",
        "standard_code": "3.NF.A.1–3",
        "standard_url": "https://www.thecorestandards.org/Math/Content/3/NF/",
        "standard_text": "Understand fractions as numbers: unit fractions, fractions on a number line, equivalent fractions and comparing fractions.",
        "meta_desc": "Free Grade 3 fractions worksheets with pictures: name shaded fractions, place fractions on a number line, find equivalent fractions and compare fractions. 100 practice questions with step-by-step hints and a printable answer key.",
        "key_big": "The bottom number says how many equal parts make the whole. The top number says how many parts you have.",
        "key_sub": "In 3/4, the whole is cut into 4 equal parts and you have 3 of them. A bigger bottom number means smaller pieces, so 1/3 is bigger than 1/6.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }


if __name__ == "__main__":
    u = gen_fractions()
    path = os.path.join(OUT, "fractions.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(u, f, ensure_ascii=False, indent=1)
    print("wrote", path)
