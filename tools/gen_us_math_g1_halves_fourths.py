# -*- coding: utf-8 -*-
"""
US Grade 1 Math: Halves and Fourths (1.G.A.3)
  python tools/gen_us_math_g1_halves_fourths.py
Only circles and rectangles (squares are rectangles). Only 2 or 4 shares. Words only, no fraction numbers.
Every picture is computed from exact coordinates. The area of every share is checked in code:
"equal" pictures have shares of exactly the same area, "not equal" pictures have a biggest share
at least 1.4 times the smallest, so the difference can be seen.
HTML attributes use single quotes (no backslashes in the JSON).
"""
import json, math, os, random, re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "us", "math", "grade-1")
UPDATED = "2026-11-02"
FILL = "#4fae74"      # shaded share
LINE = "#2b2b2b"
FONT = "Arial, Helvetica, sans-serif"
WORD = {2: "halves", 4: "fourths"}
A_ONE = {2: "a half", 4: "a fourth"}


# ------------------------------------------------------------ helpers
def mcq(q, correct, cands, e):
    """4 choices: correct + the first 3 unique distractors. Positions are set later by balance()."""
    seen = {correct}
    pick = []
    for c in cands:
        if c is None or c in seen or not c:
            continue
        seen.add(c)
        pick.append(c)
        if len(pick) == 3:
            break
    assert len(pick) == 3, (q, correct, cands)
    return {"q": q, "c": [correct] + pick, "a": 0, "e": e}


def letters_item(build):
    return {"build": build}


def balance(sets, rnd):
    """Every set: each answer position (A, B, C, D) is used exactly 5 times."""
    for s in sets:
        targets = [0, 1, 2, 3] * 5
        rnd.shuffle(targets)
        out = []
        for it, t in zip(s["items"], targets):
            if "build" in it:
                it = it["build"](t)
                assert it["a"] == t
            else:
                c = it["c"]
                right = c[it["a"]]
                wrong = [x for i, x in enumerate(c) if i != it["a"]]
                rnd.shuffle(wrong)
                it["c"] = wrong[:t] + [right] + wrong[t:]
                it["a"] = t
            out.append(it)
        s["items"] = out


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


# ------------------------------------------------------------ shapes made of exact pieces
# A shape: kind, w, h, pieces [{"d": path, "area": float}], lines (cut lines a child might count), n (pieces).
def poly(pts):
    a = 0.0
    for i in range(len(pts)):
        x1, y1 = pts[i]
        x2, y2 = pts[(i + 1) % len(pts)]
        a += x1 * y2 - x2 * y1
    d = "M" + " L".join("%.1f %.1f" % p for p in pts) + " Z"
    return {"d": d, "area": abs(a) / 2}


def shape(kind, w, h, pieces, lines):
    return {"kind": kind, "w": w, "h": h, "pieces": pieces, "lines": lines, "n": len(pieces)}


def r_vstrips(fracs, w=120, h=72, kind="rectangle"):
    assert abs(sum(fracs) - 1) < 1e-9
    ps, x = [], 0.0
    for f in fracs:
        ps.append(poly([(x, 0), (x + f * w, 0), (x + f * w, h), (x, h)]))
        x += f * w
    return shape(kind, w, h, ps, len(fracs) - 1)


def r_hstrips(fracs, w=120, h=72, kind="rectangle"):
    assert abs(sum(fracs) - 1) < 1e-9
    ps, y = [], 0.0
    for f in fracs:
        ps.append(poly([(0, y), (w, y), (w, y + f * h), (0, y + f * h)]))
        y += f * h
    return shape(kind, w, h, ps, len(fracs) - 1)


def r_grid(rows, cols, w=120, h=72, kind="rectangle"):
    ps = []
    for r in range(rows):
        for c in range(cols):
            x0, y0 = w * c / cols, h * r / rows
            ps.append(poly([(x0, y0), (x0 + w / cols, y0), (x0 + w / cols, y0 + h / rows), (x0, y0 + h / rows)]))
    return shape(kind, w, h, ps, rows - 1 + cols - 1)


def r_diag1(w=120, h=72, kind="rectangle"):
    return shape(kind, w, h, [poly([(0, 0), (w, 0), (w, h)]), poly([(0, 0), (w, h), (0, h)])], 1)


def r_x(w=84, h=84, kind="square"):
    c = (w / 2, h / 2)
    return shape(kind, w, h, [poly([(0, 0), (w, 0), c]), poly([(w, 0), (w, h), c]),
                              poly([(w, h), (0, h), c]), poly([(0, h), (0, 0), c])], 2)


def r_cross(fx, fy, w=120, h=72, kind="rectangle"):
    X, Y = fx * w, fy * h
    return shape(kind, w, h, [poly([(0, 0), (X, 0), (X, Y), (0, Y)]), poly([(X, 0), (w, 0), (w, Y), (X, Y)]),
                              poly([(0, Y), (X, Y), (X, h), (0, h)]), poly([(X, Y), (w, Y), (w, h), (X, h)])], 2)


def r_corner(t, w=120, h=72, kind="rectangle"):
    """Cut from the top-left corner to a point on the bottom side: a triangle and a 4-sided piece."""
    return shape(kind, w, h, [poly([(0, 0), (t * w, h), (0, h)]), poly([(0, 0), (w, 0), (w, h), (t * w, h)])], 1)


def r_whole(w=120, h=72, kind="rectangle"):
    return shape(kind, w, h, [poly([(0, 0), (w, 0), (w, h), (0, h)])], 0)


def sq(fn, *a, s=84):
    return fn(*a, w=s, h=s, kind="square")


def c_sectors(angles, r=44, start=0):
    """Pie pieces. start = angle of the first cut, clockwise from the top."""
    assert abs(sum(angles) - 360) < 1e-9 and len(angles) > 1
    ps, a0 = [], float(start)
    for a in angles:
        a1 = a0 + a
        t0, t1 = math.radians(a0 - 90), math.radians(a1 - 90)
        x0, y0 = r + r * math.cos(t0), r + r * math.sin(t0)
        x1, y1 = r + r * math.cos(t1), r + r * math.sin(t1)
        d = "M%.1f %.1f L%.1f %.1f A%d %d 0 %d 1 %.1f %.1f Z" % (r, r, x0, y0, r, r, 1 if a > 180 else 0, x1, y1)
        ps.append({"d": d, "area": math.pi * r * r * a / 360.0})
        a0 = a1
    n = len(angles)
    eq = max(angles) - min(angles) < 1e-9
    return shape("circle", 2 * r, 2 * r, ps, n // 2 if eq and n % 2 == 0 else n)


def c_whole(r=44):
    d = "M0 %d A%d %d 0 1 1 %d %d A%d %d 0 1 1 0 %d Z" % (r, r, r, 2 * r, r, r, r, r)
    return shape("circle", 2 * r, 2 * r, [{"d": d, "area": math.pi * r * r}], 0)


def c_parallel(cuts, r=44):
    """Circle cut by straight up-and-down lines at x = cut * r (from the center)."""
    xs = [-1.0] + list(cuts) + [1.0]

    def left_area(d):
        d = max(-1.0, min(1.0, d))
        return r * r * (math.acos(-d) + d * math.sqrt(1 - d * d))

    def top(d):
        k = r * math.sqrt(max(0.0, 1 - d * d))
        return (r + d * r, r - k), (r + d * r, r + k)
    ps = []
    for a, b in zip(xs, xs[1:]):
        if a <= -1:
            (tx, ty), (bx, by) = top(b)
            d = "M%.1f %.1f A%d %d 0 %d 0 %.1f %.1f Z" % (tx, ty, r, r, 1 if b > 0 else 0, bx, by)
        elif b >= 1:
            (tx, ty), (bx, by) = top(a)
            d = "M%.1f %.1f A%d %d 0 %d 1 %.1f %.1f Z" % (tx, ty, r, r, 1 if a < 0 else 0, bx, by)
        else:
            (t1x, t1y), (b1x, b1y) = top(a)
            (t2x, t2y), (b2x, b2y) = top(b)
            d = ("M%.1f %.1f A%d %d 0 0 1 %.1f %.1f L%.1f %.1f A%d %d 0 0 1 %.1f %.1f Z"
                 % (t1x, t1y, r, r, t2x, t2y, b2x, b2y, r, r, b1x, b1y))
        ps.append({"d": d, "area": left_area(b) - left_area(a)})
    return shape("circle", 2 * r, 2 * r, ps, len(cuts))


def c_chord(off, r=44):
    return c_parallel([off], r)


def is_equal(sh):
    a = [p["area"] for p in sh["pieces"]]
    return max(a) - min(a) < 1e-6 * max(a)


def check_unequal(sh):
    a = [p["area"] for p in sh["pieces"]]
    assert max(a) / min(a) >= 1.4, ("not visibly unequal", a)
    return sh


def check_equal(sh):
    assert is_equal(sh), [p["area"] for p in sh["pieces"]]
    return sh


def draw(sh, shaded=(), ox=0, oy=0):
    s = []
    for i, p in enumerate(sh["pieces"]):
        s.append("<path transform='translate(%.1f %.1f)' d='%s' fill='%s' stroke='%s' stroke-width='2.5' "
                 "stroke-linejoin='round'/>" % (ox, oy, p["d"], FILL if i in shaded else "#fff", LINE))
    return "".join(s)


NOUN = {"rectangle": "rectangle", "square": "square", "circle": "circle"}


def one_svg(sh, shaded=(), label=None):
    pad = 5
    w, h = sh["w"] + 2 * pad, sh["h"] + 2 * pad
    lab = label or "%s cut into %d pieces%s" % (NOUN[sh["kind"]], sh["n"], ", %d shaded" % len(shaded) if shaded else "")
    return svg_wrap(int(math.ceil(w)), int(math.ceil(h)), draw(sh, shaded, pad, pad), lab)


def panel_svg(shapes, label, letters="ABCD", cols=2):
    n = len(shapes)
    cw = max(s["w"] for s, _ in shapes)
    ch = max(s["h"] for s, _ in shapes)
    LW, gap, pad = 24, 18, 6
    rws = (n + cols - 1) // cols
    W = pad + cols * (LW + cw) + (cols - 1) * gap + pad
    H = pad + rws * ch + (rws - 1) * gap + pad
    s = []
    for i, (sh, shaded) in enumerate(shapes):
        r, c = divmod(i, cols)
        x0 = pad + c * (LW + cw + gap)
        y0 = pad + r * (ch + gap)
        s.append("<text x='%.1f' y='%.1f' font-size='20' font-weight='800' fill='%s'>%s</text>"
                 % (x0, y0 + 17, LINE, letters[i]))
        s.append(draw(sh, shaded, x0 + LW + (cw - sh["w"]) / 2, y0 + (ch - sh["h"]) / 2))
    return svg_wrap(int(math.ceil(W)), int(math.ceil(H)), "".join(s), label)


def letters_q(good, bads, question, label, e_fn, rnd):
    """Picture question: good = (shape, shaded), bads = 3 x (shape, shaded). e_fn(letter) -> explanation."""
    bads = bads[:]
    rnd.shuffle(bads)

    def build(pos):
        shapes = bads[:pos] + [good] + bads[pos:]
        svg = panel_svg(shapes, label)
        return {"q": fig(svg) + question, "c": ["A", "B", "C", "D"], "a": pos, "e": e_fn("ABCD"[pos])}
    return letters_item(build)


def pair_svg(a, sa, b, sb, label):
    return panel_svg([(a, sa), (b, sb)], label, letters="AB", cols=2)


# ------------------------------------------------------------ catalogs of exact pictures for panels (about 90 x 90)
def EQ(n, i):
    lib = {
        2: [lambda: r_vstrips([.5, .5], w=90, h=56), lambda: c_sectors([180, 180]), lambda: r_hstrips([.5, .5], w=90, h=56),
            lambda: c_sectors([180, 180], start=90), lambda: r_diag1(w=90, h=56), lambda: sq(r_vstrips, [.5, .5], s=76)],
        4: [lambda: r_grid(2, 2, w=90, h=56), lambda: c_sectors([90] * 4), lambda: r_vstrips([.25] * 4, w=90, h=56),
            lambda: c_sectors([90] * 4, start=45), lambda: r_hstrips([.25] * 4, w=90, h=64), lambda: sq(r_grid, 2, 2, s=76)],
    }
    return check_equal(lib[n][i % len(lib[n])]())


def UNEQ(n, i):
    lib = {
        2: [lambda: c_chord(0.4), lambda: r_vstrips([.3, .7], w=90, h=56), lambda: r_corner(.5, w=90, h=56),
            lambda: c_sectors([240, 120]), lambda: r_hstrips([.3, .7], w=90, h=56)],
        4: [lambda: r_cross(.3, .35, w=90, h=56), lambda: r_vstrips([.15, .35, .2, .3], w=90, h=56),
            lambda: c_sectors([140, 50, 100, 70]), lambda: c_parallel([-.5, 0, .5])],
    }
    return check_unequal(lib[n][i % len(lib[n])]())


def shares(k):
    return "1 equal share" if k == 1 else "%d equal shares" % k


# ============================================================ set 1: equal or not equal shares?
NOT_EQ = "Not equal shares"


def set_equal(rnd):
    its = []
    singles = [
        (c_sectors([180, 180], start=90), True), (r_vstrips([.5, .5]), True), (r_grid(2, 2), True),
        (c_sectors([90] * 4, start=45), True), (sq(r_diag1), True), (r_hstrips([.25] * 4, h=80), True),
        (c_chord(0.4), False), (r_vstrips([.3, .7]), False), (c_sectors([140, 50, 100, 70]), False),
        (r_corner(.5), False), (r_cross(.3, .35), False), (c_parallel([-.5, 0, .5]), False),
    ]
    rnd.shuffle(singles)
    for sh, ok in singles:
        (check_equal if ok else check_unequal)(sh)
        n, L = sh["n"], sh["lines"]
        noun = NOUN[sh["kind"]]
        if ok:
            e = "There are %d pieces. %s the <b>same size</b>. So there are %d equal shares." % (
                n, "Both are" if n == 2 else "They are all", n)
            if L > 1 and L != n:
                e += " Count the pieces, not the lines."
            right = shares(n)
            cands = [shares(L) if L != n else None, NOT_EQ, shares(3), shares(6 - n)]
        else:
            e = ("There are %d pieces, but they are <b>not the same size</b>. %s. So they are not equal shares."
                 % (n, "One piece is much bigger" if n == 2 else "Some pieces are bigger"))
            right = NOT_EQ
            cands = [shares(n), shares(L) if L != n else None, shares(6 - n), shares(3)]
        its.append(mcq(fig(one_svg(sh)) + "Is this %s cut into equal shares? How many?" % noun, right, cands, e))

    plan = [(2, False, 0), (4, False, 1), (2, True, 2), (4, True, 3), (2, False, 3), (4, False, 4), (2, True, 4), (4, True, 0)]
    for qi, (n, find_not, pi) in enumerate(plan):
        if not find_not:
            good, bads = EQ(n, pi), [UNEQ(n, qi + j) for j in range(3)]
            q = "Each shape has %d pieces. Which shape has <b>equal</b> shares?" % n
            e = (lambda n: lambda L: "All the shapes have %d pieces. Only in shape <b>%s</b> are the pieces "
                 "all the same size." % (n, L))(n)
        else:
            good, bads = UNEQ(n, pi), [EQ(n, qi + j) for j in range(3)]
            q = "Each shape has %d pieces. Which shape does <b>not</b> have equal shares?" % n
            e = (lambda n: lambda L: "In shape <b>%s</b> the pieces are not the same size. The other shapes have "
                 "%d pieces that are all the same size." % (L, n))(n)
        its.append(letters_q((good, ()), [(b, ()) for b in bads], q,
                             "four shapes A to D, each cut into %d pieces" % n, e, rnd))
    assert len(its) == 20, len(its)
    return {"title": "Equal or not equal shares?", "items": its}


# ============================================================ set 2: halves
def yes_no(sh, want):
    """Is this shape cut into halves (want=2) or fourths (want=4)? Answer by the real shares."""
    n, L = sh["n"], sh["lines"]
    noun = NOUN[sh["kind"]]
    W = WORD[want].capitalize()
    if not is_equal(sh):
        right = "No, not equal"
        e = ("There are %d pieces, but they are <b>not the same size</b>. %s must be equal shares." % (n, W))
        cands = ["Yes, %d pieces" % n, "Yes, %s" % WORD[want], "No, %s" % WORD[6 - want]]
    elif n == want:
        right = "Yes, %s" % WORD[want]
        e = "There are <b>%d equal shares</b>. %d equal shares are %s." % (n, n, WORD[n])
        if L > 1 and L != n:
            e += " Count the shares, not the %d lines." % L
        cands = ["No, not equal", "No, %s" % WORD[6 - want],
                 "No, %s" % ("only 1 line" if L == 1 else "%d lines" % L)]
    else:
        right = "No, %s" % WORD[n]
        e = ("There are <b>%d equal shares</b>, so they are %s, not %s." % (n, WORD[n], WORD[want]))
        if L == 2 and want == 2:
            e += " There are 2 lines, but 4 shares. Count the shares."
        cands = ["Yes, %s" % WORD[want], "Yes, %d lines" % L if L == want else "Yes, quarters", "No, not equal"]
    return mcq(fig(one_svg(sh)) + "Is this %s cut into %s?" % (noun, WORD[want]), right, cands, e)


def set_halves(rnd):
    its = []
    for sh in [c_sectors([180, 180]), r_hstrips([.5, .5]), sq(r_diag1), check_unequal(c_chord(-0.45)),
               check_unequal(r_hstrips([.3, .7])), c_sectors([90] * 4)]:
        its.append(yes_no(sh, 2))

    def which_halves(gi, bads):
        e = lambda L: ("Shape <b>%s</b> has 2 equal shares. That is halves. Check the others: halves are "
                       "2 pieces that are the <b>same size</b>." % L)
        return letters_q((EQ(2, gi), ()), [(b, ()) for b in bads], "Which shape shows <b>halves</b>?",
                         "four shapes A to D for halves", e, rnd)
    its.append(which_halves(0, [UNEQ(2, 0), EQ(4, 1), UNEQ(2, 2)]))
    its.append(which_halves(1, [UNEQ(2, 1), EQ(4, 0), UNEQ(2, 3)]))
    its.append(which_halves(4, [UNEQ(2, 4), EQ(4, 2), UNEQ(2, 0)]))
    its.append(which_halves(5, [UNEQ(2, 2), EQ(4, 3), UNEQ(2, 1)]))

    sh = check_equal(r_vstrips([.5, .5]))
    its.append(mcq(fig(one_svg(sh)) + "The rectangle is cut into halves. Which words name the whole rectangle?",
                   "two halves", ["one half", "four halves", "two fourths"],
                   "The rectangle has 2 equal shares. Each one is a half. The whole is <b>two halves</b>."))
    its.append(mcq("What do we call 2 equal shares?", "halves", ["twos", "fourths", "wholes"],
                   "2 equal shares are called <b>halves</b>. We do not say twos."))
    its.append(mcq("How many halves make a whole?", "2", ["1", "4", "3"],
                   "A whole cut into halves has 2 equal shares. <b>2 halves</b> make a whole."))
    its.append(mcq("A circle is cut into halves. How many equal shares are there?", "2", ["1", "4", "3"],
                   "Halves means <b>2 equal shares</b>."))
    its.append(mcq("A circle is cut into 2 equal shares. What is each share?", "half of the circle",
                   ["a fourth of it", "two circles", "the whole circle"],
                   "2 equal shares are halves. Each share is <b>half of the circle</b>."))
    its.append(mcq("One straight cut goes down the middle of a square. How many equal shares are there?",
                   "2", ["1", "4", "3"],
                   "1 cut makes <b>2 shares</b>. The cut is in the middle, so the shares are equal. They are halves."))
    its.append(mcq("A shape has 2 pieces. One piece is big. One piece is small. Are they halves?",
                   "No, not equal", ["Yes, 2 pieces", "Yes, 1 cut", "No, fourths"],
                   "Halves must be the <b>same size</b>. A big piece and a small piece are not halves."))
    its.append(mcq("Ella cuts a cookie in half. How many pieces does she have?", "2 pieces",
                   ["1 piece", "4 pieces", "3 pieces"],
                   "Cutting in half makes <b>2 equal pieces</b>. Each piece is half of the cookie."))
    its.append(mcq("Max cuts a pancake into halves. He eats one half. How much is left?", "half of it",
                   ["the whole pancake", "a fourth of it", "2 halves"],
                   "The whole pancake is 2 halves. Max eats 1 half, so <b>1 half</b> is left."))
    its.append(mcq("Which is <b>not</b> a way to cut a rectangle in half?", "a cut near one end",
                   ["a cut down the middle", "a cut across the middle", "a cut corner to corner"],
                   "A cut near one end makes a big piece and a small piece. The other cuts make 2 equal shares."))
    assert len(its) == 20, len(its)
    return {"title": "Halves", "items": its}


# ============================================================ set 3: fourths and quarters
def set_fourths(rnd):
    its = []
    for sh in [c_sectors([90] * 4), r_vstrips([.25] * 4), sq(r_grid, 2, 2), r_x(),
               check_unequal(r_cross(.3, .35)), check_unequal(c_parallel([-.5, 0, .5])), r_vstrips([.5, .5])]:
        its.append(yes_no(sh, 4))

    def which_fourths(gi, bads):
        e = lambda L: ("Shape <b>%s</b> has 4 equal shares. That is fourths. Check the others: fourths are "
                       "4 pieces that are the <b>same size</b>." % L)
        return letters_q((EQ(4, gi), ()), [(b, ()) for b in bads], "Which shape shows <b>fourths</b>?",
                         "four shapes A to D for fourths", e, rnd)
    its.append(which_fourths(0, [UNEQ(4, 2), EQ(2, 1), UNEQ(4, 1)]))
    its.append(which_fourths(1, [UNEQ(4, 0), EQ(2, 0), UNEQ(4, 3)]))
    its.append(which_fourths(4, [UNEQ(4, 1), EQ(2, 3), UNEQ(4, 2)]))
    its.append(which_fourths(5, [UNEQ(4, 3), EQ(2, 5), UNEQ(4, 0)]))

    sx = check_equal(r_x())
    its.append(mcq(fig(one_svg(sx, (), "square cut corner to corner both ways into 4 triangles")) +
                   "This square has 2 lines. How many equal shares does it have?", "4", ["2", "3", "1"],
                   "Count the shares, not the lines. 2 lines cross and make <b>4 equal shares</b>. They are fourths."))
    its.append(mcq("What do we call 4 equal shares?", "fourths", ["fours", "halves", "wholes"],
                   "4 equal shares are called <b>fourths</b>. They are also called quarters."))
    its.append(mcq("What is another name for a fourth?", "a quarter", ["a half", "a whole", "a four"],
                   "A fourth is also called <b>a quarter</b>. Both mean 1 of 4 equal shares."))
    its.append(mcq("Which is bigger: a fourth of a pizza or a quarter of the same pizza?", "They are the same",
                   ["a fourth", "a quarter", "You can’t tell"],
                   "A fourth and a quarter are the <b>same</b>. Both are 1 of 4 equal shares of the pizza."))
    its.append(mcq("How many fourths make a whole?", "4", ["2", "3", "1"],
                   "Fourths are 4 equal shares. <b>4 fourths</b> make a whole."))
    its.append(mcq("How many quarters make a whole?", "4", ["2", "1", "3"],
                   "Quarters are 4 equal shares. <b>4 quarters</b> make a whole."))
    its.append(mcq("A square is cut into 4 equal shares. What is each share?", "a quarter of it",
                   ["half of it", "four of it", "the whole square"],
                   "4 equal shares are quarters. Each share is <b>a quarter of the square</b>."))
    its.append(mcq("Ana cuts a waffle into fourths. How many pieces does she have?", "4 pieces",
                   ["2 pieces", "3 pieces", "1 piece"],
                   "Fourths means <b>4 equal pieces</b>."))
    its.append(mcq("Sam cuts a cake into 4 pieces. One piece is much bigger. Are they fourths?",
                   "No, not equal", ["Yes, 4 pieces", "No, halves", "Yes, quarters"],
                   "Fourths must be <b>4 equal shares</b>. Sam has 4 pieces, but they are not the same size."))
    assert len(its) == 20, len(its)
    return {"title": "Fourths and quarters", "items": its}


# ============================================================ set 4: what part is shaded?
def set_shaded(rnd):
    its = []
    halves = [(c_sectors([180, 180]), 1), (r_vstrips([.5, .5]), 0), (r_hstrips([.5, .5]), 1),
              (sq(r_diag1), 0), (c_sectors([180, 180], start=90), 0)]
    for sh, k in halves:
        check_equal(sh)
        noun = NOUN[sh["kind"]]
        e = "The %s has <b>2 equal shares</b>. 1 share is shaded. So one half of the %s is shaded." % (noun, noun)
        its.append(mcq(fig(one_svg(sh, (k,))) + "What part of the %s is shaded?" % noun, "one half",
                       ["one fourth", "two halves", "the whole %s" % noun], e))
    fourths = [(c_sectors([90] * 4), 2, "fourth"), (r_grid(2, 2), 0, "fourth"), (r_vstrips([.25] * 4), 3, "fourth"),
               (r_x(), 1, "quarter"), (c_sectors([90] * 4, start=45), 3, "quarter"),
               (r_hstrips([.25] * 4, h=80), 1, "quarter")]
    for sh, k, w in fourths:
        check_equal(sh)
        noun = NOUN[sh["kind"]]
        e = ("The %s has <b>4 equal shares</b>. 1 share is shaded. So one %s of the %s is shaded. "
             "Count all 4 shares, not only the white ones." % (noun, w, noun))
        its.append(mcq(fig(one_svg(sh, (k,))) + "What part of the %s is shaded?" % noun, "one %s" % w,
                       ["one half", "four %ss" % w, "four halves"], e))

    def pic(n, good, bads, e_extra):
        e = (lambda n: lambda L: "Shape <b>%s</b> has %d equal shares and 1 is shaded, so %s is shaded. %s"
             % (L, n, A_ONE[n], e_extra))(n)
        return letters_q(good, bads, "Which shape has <b>one %s</b> shaded?" % ("half" if n == 2 else "fourth"),
                         "four shapes A to D with shading", e, rnd)
    its.append(pic(2, (EQ(2, 0), (0,)), [(UNEQ(2, 1), (0,)), (EQ(4, 1), (0,)), (EQ(2, 1), (0, 1))],
                   "The shares must be equal, and only 1 of 2 is shaded."))
    its.append(pic(2, (EQ(2, 1), (1,)), [(UNEQ(2, 0), (1,)), (EQ(4, 0), (3,)), (EQ(2, 2), (0, 1))],
                   "The shares must be equal, and only 1 of 2 is shaded."))
    its.append(pic(4, (EQ(4, 1), (2,)), [(UNEQ(4, 2), (1,)), (EQ(2, 1), (0,)), (EQ(4, 2), (0, 1))],
                   "The shares must be equal, and only 1 of 4 is shaded."))
    its.append(pic(4, (EQ(4, 0), (3,)), [(UNEQ(4, 0), (0,)), (EQ(2, 0), (1,)), (EQ(4, 3), (0, 2))],
                   "The shares must be equal, and only 1 of 4 is shaded."))

    sh = check_equal(r_grid(2, 2))
    its.append(mcq(fig(one_svg(sh)) + "The rectangle is cut into fourths. Which words name the whole rectangle?",
                   "four fourths", ["two fourths", "four halves", "one fourth"],
                   "The rectangle has 4 equal shares. The whole is <b>four fourths</b>. "
                   "(It has 2 lines, but 4 shares.)"))
    sh = check_equal(c_sectors([90] * 4))
    its.append(mcq(fig(one_svg(sh)) + "The circle is cut into quarters. Which words name the whole circle?",
                   "four quarters", ["two quarters", "four halves", "one quarter"],
                   "The circle has 4 equal shares. The whole is <b>four quarters</b>."))
    sh = check_equal(r_vstrips([.5, .5]))
    its.append(mcq(fig(one_svg(sh, (0, 1))) + "What part of the rectangle is shaded?", "the whole rectangle",
                   ["one half", "two rectangles", "one fourth"],
                   "Both halves are shaded. 2 halves make <b>the whole</b> rectangle."))
    sh = check_equal(c_sectors([90] * 4, start=45))
    its.append(mcq(fig(one_svg(sh, (0, 1, 2, 3))) + "What part of the circle is shaded?", "the whole circle",
                   ["one fourth", "four circles", "one half"],
                   "All 4 fourths are shaded. 4 fourths make <b>the whole</b> circle."))
    sh = check_equal(sq(r_grid, 2, 2))
    its.append(mcq(fig(one_svg(sh, (1,))) + "How many more fourths must be shaded to shade the whole square?",
                   "3 more", ["4 more", "1 more", "2 more"],
                   "The whole square is 4 fourths. 1 is shaded. 1 + 3 = 4, so <b>3 more</b> must be shaded."))
    assert len(its) == 20, len(its)
    return {"title": "What part is shaded?", "items": its}


# ============================================================ set 5: bigger or smaller, and real life
SAME, A_BIG, B_BIG, CANT = "Same size", "A is bigger", "B is bigger", "You can’t tell"


def set_stories(rnd):
    its = []
    pairs = [
        (c_sectors([180, 180]), (0,), c_sectors([90] * 4), (1,), A_BIG,
         "A is cut into halves. B is cut into fourths. A half is bigger than a fourth, so <b>A is bigger</b>. "
         "(4 is more than 2, but more shares means smaller shares.)"),
        (r_grid(2, 2, w=90, h=56), (2,), r_vstrips([.5, .5], w=90, h=56), (0,), B_BIG,
         "A is cut into fourths. B is cut into halves. A half is bigger than a fourth, so <b>B is bigger</b>."),
        (sq(r_x, s=84), (0,), sq(r_grid, 2, 2, s=84), (3,), SAME,
         "Both squares are cut into fourths. Each shaded share is a fourth of the same square. "
         "A triangle and a small square can be the <b>same size</b>."),
        (sq(r_vstrips, [.5, .5], s=84), (1,), sq(r_diag1, s=84), (0,), SAME,
         "Both squares are cut into halves. Half of a square is the <b>same size</b>, whether the cut goes "
         "down the middle or corner to corner."),
    ]
    for a, sa, b, sb, right, e in pairs:
        check_equal(a)
        check_equal(b)
        q = fig(pair_svg(a, sa, b, sb, "shapes A and B of the same size, each with one share shaded")) + \
            "A and B are the same size. Which shaded share is bigger?"
        its.append(mcq(q, right, [c for c in [SAME, A_BIG, B_BIG, CANT] if c != right], e))

    its.append(letters_q((c_sectors([90] * 4), ()),
                         [(c_sectors([180, 180]), ()), (c_sectors([180, 180], start=90), ()), (c_whole(), ())],
                         "The circles are the same size. Which circle has the <b>smallest</b> shares?",
                         "four same-size circles A to D",
                         lambda L: ("Circle <b>%s</b> is cut into fourths. That is the most shares. "
                                    "More shares means smaller shares." % L), rnd))
    its.append(letters_q((r_vstrips([.5, .5], w=90, h=56), ()),
                         [(r_grid(2, 2, w=90, h=56), ()), (r_vstrips([.25] * 4, w=90, h=56), ()),
                          (r_hstrips([.25] * 4, w=90, h=56), ())],
                         "The rectangles are the same size. Which rectangle has the <b>biggest</b> shares?",
                         "four same-size rectangles A to D",
                         lambda L: ("Rectangle <b>%s</b> is cut into halves. The others are cut into fourths. "
                                    "Fewer shares means bigger shares." % L), rnd))

    cmp_q = [
        ("Which is bigger: half of a pizza or a fourth of the same pizza?", "half of the pizza",
         ["a fourth of the pizza", "They are the same", "You can’t tell"],
         "A half is 1 of 2 equal shares. A fourth is 1 of 4 equal shares. More shares means smaller shares. "
         "So <b>half</b> is bigger."),
        ("Which is smaller: a quarter of a cake or half of the same cake?", "a quarter of it",
         ["half of it", "They are the same", "You can’t tell"],
         "A quarter is 1 of 4 shares. Half is 1 of 2 shares. 4 shares are smaller, so <b>a quarter</b> is smaller."),
        ("You cut the same pie into more equal shares. What happens to each share?", "It gets smaller",
         ["It gets bigger", "It stays the same", "The pie gets bigger"],
         "The pie stays the same. More shares means each share is <b>smaller</b>."),
        ("Mia cuts her pancake into halves. Ben cuts the same size pancake into fourths. Whose pieces are bigger?",
         "Mia’s pieces", ["Ben’s pieces", "They are the same", "You can’t tell"],
         "Ben has more pieces, so his pieces are smaller. Halves are bigger than fourths, so <b>Mia’s pieces</b> are bigger."),
    ]
    for q, right, cands, e in cmp_q:
        its.append(mcq(q, right, cands, e))

    st = [
        ("Ava shares a sandwich fairly with 3 friends. What share does each person get?", "a fourth",
         ["a half", "the whole sandwich", "four halves"],
         "Ava and 3 friends are <b>4 people</b>. 4 equal shares are fourths. Do not forget to count Ava."),
        ("Leo and his sister share a pizza fairly. What share does each one get?", "a half",
         ["a fourth", "the whole pizza", "two halves"],
         "Leo and his sister are <b>2 people</b>. 2 equal shares are halves. Each one gets a half."),
        ("Four kids share a big cookie fairly. What share does each kid get?", "a quarter",
         ["a half", "four quarters", "the whole cookie"],
         "Four kids means <b>4 equal shares</b>. Each kid gets a quarter (a fourth) of the cookie."),
        ("Nora folds a paper in half. Then she opens it. How many equal shares does she see?", "2",
         ["1", "4", "3"],
         "One fold makes <b>2 equal shares</b>: 2 halves. The fold is 1 line, but it makes 2 shares."),
        ("Kai folds a square paper in half. He folds it in half again the other way. He opens it. What are the shares?",
         "fourths", ["halves", "2 shares", "not equal"],
         "The 2 folds cross and make <b>4 equal shares</b>. 4 equal shares are fourths."),
        ("Owen cuts a sandwich into 2 pieces. One is big and one is small. Did he cut it in half?",
         "No, not equal", ["Yes, 2 pieces", "Yes, 1 cut", "No, fourths"],
         "Halves must be the <b>same size</b>. A big piece and a small piece are not halves."),
        ("Ella gets half of an apple. Max gets a fourth of the same size apple. Who gets more?", "Ella",
         ["Max", "They get the same", "You can’t tell"],
         "Half is bigger than a fourth. So <b>Ella</b> gets more apple."),
        ("Omar is very hungry. Should he take half of a pie or a quarter of the same pie?", "half of the pie",
         ["a quarter of it", "They are the same", "You can’t tell"],
         "Half of a pie is bigger than a quarter of the same pie. Omar should take <b>half</b>."),
        ("Grace eats 2 halves of an orange. How much of the orange does she eat?", "the whole orange",
         ["half of it", "2 oranges", "a fourth of it"],
         "2 halves make 1 whole. Grace eats <b>the whole orange</b>."),
        ("Lily cuts a square cake with 2 cuts. The cuts cross in the middle. How many equal shares are there?",
         "4", ["2", "3", "1"],
         "2 cuts that cross in the middle make <b>4 equal shares</b>. Count the shares, not the cuts."),
    ]
    for q, right, cands, e in st:
        its.append(mcq(q, right, cands, e))
    assert len(its) == 20, len(its)
    return {"title": "Bigger or smaller? Sharing stories", "items": its}


# ============================================================ lesson
def labeled_row(shapes, labels, label, gap=26):
    pad = 6
    cw = max(s["w"] for s, _ in shapes)
    ch = max(s["h"] for s, _ in shapes)
    W = pad * 2 + len(shapes) * cw + (len(shapes) - 1) * gap
    H = pad * 2 + ch + 28
    s = []
    for i, ((sh, shaded), t) in enumerate(zip(shapes, labels)):
        x0 = pad + i * (cw + gap)
        s.append(draw(sh, shaded, x0 + (cw - sh["w"]) / 2, pad + (ch - sh["h"]) / 2))
        s.append("<text x='%.1f' y='%.1f' font-size='16' font-weight='700' fill='%s' text-anchor='middle'>%s</text>"
                 % (x0 + cw / 2, pad + ch + 22, LINE, t))
    return svg_wrap(int(math.ceil(W)), int(math.ceil(H)), "".join(s), label)


def whole_svg():
    """A rectangle of 4 equal strips, each labeled a fourth."""
    pad, w, h = 6, 336, 64
    sh = check_equal(r_vstrips([.25] * 4, w=w, h=h))
    s = [draw(sh, (), pad, pad)]
    for i in range(4):
        s.append("<text x='%.1f' y='%.1f' font-size='16' font-weight='700' fill='%s' text-anchor='middle'>a fourth</text>"
                 % (pad + w / 8 + i * w / 4, pad + h / 2 + 6, LINE))
    return svg_wrap(w + 2 * pad, h + 2 * pad, "".join(s), "rectangle cut into 4 equal shares, each labeled a fourth")


def body_html():
    f1 = labeled_row([(check_equal(c_sectors([180, 180], r=46)), ()), (check_unequal(c_chord(0.4, r=46)), ())],
                     ["Equal", "Not equal"], "a circle cut into 2 equal shares and a circle cut into 2 pieces that are not equal",
                     gap=40)
    f2 = labeled_row([(check_equal(c_sectors([180, 180], r=46)), (0,)), (check_equal(r_vstrips([.5, .5], w=110, h=70)), (1,)),
                      (check_equal(sq(r_diag1, s=84)), (0,))],
                     ["a half", "a half", "a half"], "a circle, a rectangle and a square, each with one half shaded")
    f3 = labeled_row([(check_equal(c_sectors([90] * 4, r=46)), (0,)), (check_equal(r_grid(2, 2, w=110, h=70)), (3,)),
                      (check_equal(r_x()), (1,))],
                     ["a fourth", "a fourth", "a fourth"], "a circle, a rectangle and a square, each with one fourth shaded")
    f4 = whole_svg()
    f5 = labeled_row([(check_equal(c_sectors([180, 180], r=46)), (0,)), (check_equal(c_sectors([90] * 4, r=46)), (0,))],
                     ["a half", "a fourth"], "two same-size circles: one half shaded and one fourth shaded", gap=40)
    return (
        "<h2>Equal shares</h2>"
        "<p>To share fairly, cut a shape into <b>equal shares</b>. Equal shares are all the <b>same size</b>.</p>"
        "<figure class='sn-fig'>" + f1 +
        "<figcaption>Both circles have 2 pieces. Only the first one has equal shares.</figcaption></figure>"
        "<h2>Halves</h2>"
        "<p>2 equal shares are <b>halves</b>. Each share is <b>half of</b> the shape.</p>"
        "<figure class='sn-fig'>" + f2 +
        "<figcaption>One half is shaded in each shape. The whole is two halves.</figcaption></figure>"
        "<h2>Fourths and quarters</h2>"
        "<p>4 equal shares are <b>fourths</b>. They are also called <b>quarters</b>. "
        "A fourth of a shape and a quarter of a shape are the same.</p>"
        "<figure class='sn-fig'>" + f3 +
        "<figcaption>One fourth (one quarter) is shaded in each shape.</figcaption></figure>" +
        table(["Equal shares", "Name", "One share", "The whole"], [
            ["2", "halves", "half of", "two halves"],
            ["4", "fourths or quarters", "a fourth of, a quarter of", "four fourths"],
        ]) +
        "<h2>The whole</h2>"
        "<p>All the shares together make the <b>whole</b>.</p>"
        "<figure class='sn-fig'>" + f4 +
        "<figcaption>4 fourths make 1 whole. 2 halves make 1 whole, too.</figcaption></figure>"
        "<h2>More shares, smaller shares</h2>"
        "<p>Cut the same shape into <b>more</b> shares, and each share gets <b>smaller</b>.</p>"
        "<figure class='sn-fig'>" + f5 +
        "<figcaption>Same-size circles. A half is bigger than a fourth.</figcaption></figure>" +
        ex("Example", "Ava shares a sandwich fairly with 3 friends. What share does each person get?",
           "Ava and 3 friends are 4 people. 4 equal shares are fourths.", "a fourth (a quarter) of the sandwich") +
        "<h2>Common mistakes</h2>" +
        table(["Mistake", "What to do instead"], [
            ["Calling 2 pieces halves when they are not the same size", "Check that the shares are equal first"],
            ["Thinking a fourth is bigger than a half because 4 is more than 2", "More shares means smaller shares. A half is bigger"],
            ["Counting the lines instead of the shares", "Count the shares: 2 lines can make 4 shares"],
            ["Calling 4 equal shares halves", "4 equal shares are fourths. 2 equal shares are halves"],
        ])
    )


FAQ = [
    {"q": "What are halves and fourths in 1st grade math?",
     "a": "Halves are 2 equal shares of a shape. Fourths are 4 equal shares of a shape. First graders cut circles and rectangles into halves and fourths."},
    {"q": "Is a fourth bigger than a half?",
     "a": "No. When the same shape is cut into more shares, each share is smaller. Half of a pizza is bigger than a fourth of the same pizza."},
    {"q": "Is a fourth the same as a quarter?",
     "a": "Yes. A fourth and a quarter both mean 1 of 4 equal shares. 4 fourths, or 4 quarters, make 1 whole."},
    {"q": "What are equal shares?",
     "a": "Equal shares are pieces of a shape that are all the same size. If one piece is bigger, the pieces are not halves or fourths."},
]


def mark_large(u, pattern):
    """Tag pictures that must print larger (A-D and A-B choices) so the letters stay readable."""
    rx = re.compile(r"<svg (?=[^>]*aria-label='" + pattern + ")")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u


def gen():
    rnd = random.Random(116)
    sets = [set_equal(rnd), set_halves(rnd), set_fourths(rnd), set_shaded(rnd), set_stories(rnd)]
    balance(sets, rnd)
    seen = set()
    for s in sets:
        assert len(s["items"]) == 20, (s["title"], len(s["items"]))
        assert sorted(it["a"] for it in s["items"]) == sorted([0, 1, 2, 3] * 5), s["title"]
        for it in s["items"]:
            assert len(set(it["c"])) == 4, it
            key = json.dumps([it["q"], it["c"]])
            assert key not in seen, it["q"]
            seen.add(key)
            txt = re.sub(r"<[^>]+>", " ", it["q"] + " " + " ".join(it["c"]) + " " + it["e"])
            assert not re.search(r"\b\d+/\d+\b", txt), it["q"]      # words, not fraction numbers
            assert "class='fr'" not in it["q"] + "".join(it["c"]) + it["e"]
            assert "third" not in txt, it["q"]                      # Grade 1: halves and fourths only
    u = {
        "country": "us", "subject": "math", "grade": "grade-1", "slug": "halves-and-fourths", "sort": 16,
        "updated": UPDATED, "pdf_url": "",
        "title": "Halves and Fourths",
        "seo_title": "Grade 1 Halves and Fourths Worksheets: Equal Shares and Quarters (Free, with Answers)",
        "short_title": "Halves and fourths",
        "domain": "Geometry",
        "standard_code": "1.G.A.3",
        "standard_url": "https://www.thecorestandards.org/Math/Content/1/G/A/3/",
        "standard_text": "Partition circles and rectangles into two and four equal shares, describe the shares using the words halves, fourths, and quarters, and use the phrases half of, fourth of, and quarter of. Describe the whole as two of, or four of the shares. Understand for these examples that decomposing into more equal shares creates smaller shares.",
        "meta_desc": "Free Grade 1 halves and fourths worksheets with pictures of circles and rectangles: equal or not equal shares, halves, fourths and quarters, what part is shaded, and why a half is bigger than a fourth. 100 practice questions with an answer key.",
        "key_big": "2 equal shares are halves. 4 equal shares are fourths, or quarters.",
        "key_sub": "The shares must be the same size. The whole is two halves or four fourths. More shares means smaller shares, so a half is bigger than a fourth.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }
    return mark_large(u, "(four shapes A to D|four same-size|shapes A and B)")


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
