# -*- coding: utf-8 -*-
"""
UK Year 1 Maths: Halves and Quarters (National Curriculum in England, Year 1: Fractions)
  python3 tools/gen_uk_maths_y1_halves_quarters.py
Halves and quarters of shapes, objects and quantities. Words only in the questions (no 1/2, 1/4).
Shape pictures are computed from exact coordinates. The area of every part is checked in code:
"equal" pictures have parts of exactly the same area, "not equal" pictures have a biggest part
at least 1.4 times the smallest, so the difference can be seen.
Quantity pictures (counters, sweets) are drawn from the numbers; every answer is checked in code.
HTML attributes use single quotes (no backslashes in the JSON).
"""
import json, math, os, random, re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "uk", "maths", "year-1")
UPDATED = "2026-11-02"
FILL = "#4fae74"      # shaded part
RED = "#d6453b"
SWEET = "#8e6ccf"
LINE = "#2b2b2b"
FONT = "Arial, Helvetica, sans-serif"
WORD = {2: "halves", 4: "quarters"}
A_ONE = {2: "a half", 4: "a quarter"}


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
    """Circle cut by straight up-and-down lines at x = cut * r (from the centre)."""
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


def parts(k):
    return "1 equal part" if k == 1 else "%d equal parts" % k


# ------------------------------------------------------------ quantity pictures (counters, sweets)
def item(kind, cx, cy, fill=None):
    if kind == "counter":
        return ("<circle cx='%.1f' cy='%.1f' r='10' fill='%s' stroke='%s' stroke-width='1.8'/>"
                % (cx, cy, fill or RED, LINE))
    # a wrapped sweet: a round middle with a twist on each side
    c = fill or SWEET
    return ("<path d='M%.1f %.1f L%.1f %.1f L%.1f %.1f Z' fill='%s' stroke='%s' stroke-width='1.5' stroke-linejoin='round'/>"
            "<path d='M%.1f %.1f L%.1f %.1f L%.1f %.1f Z' fill='%s' stroke='%s' stroke-width='1.5' stroke-linejoin='round'/>"
            "<circle cx='%.1f' cy='%.1f' r='6.5' fill='%s' stroke='%s' stroke-width='1.8'/>"
            % (cx - 5, cy, cx - 11, cy - 5, cx - 11, cy + 5, c, LINE,
               cx + 5, cy, cx + 11, cy - 5, cx + 11, cy + 5, c, LINE, cx, cy, c, LINE))


PLURAL = {"counter": "counters", "sweet": "sweets"}
STEP = 30


def items_svg(n, kind):
    """n objects in rows of 7 (8 for 14), with no gaps, so the rows never show the halves or quarters."""
    per = 8 if n == 14 else 7
    cols = min(n, per)
    rows = -(-n // per)
    for d in (2, 4):                      # a row length must not split n into its halves or quarters
        assert rows == 1 or n % d or per != n // d, (n, per)
    s = []
    for i in range(n):
        r, c = divmod(i, per)
        s.append(item(kind, 6 + STEP / 2 + c * STEP, 6 + STEP / 2 + r * STEP))
    return svg_wrap(12 + cols * STEP, 12 + rows * STEP, "".join(s), "row of %d %s" % (n, PLURAL[kind]))


def groups_svg(sizes, shaded, kind):
    """Objects in boxes. sizes = number in each box; the box with index `shaded` is green."""
    mx = max(sizes)
    cols = 2 if mx <= 4 else (3 if mx <= 6 else 4)
    rows = -(-mx // cols)
    bw, bh = cols * STEP + 10, rows * STEP + 10
    gap = 12
    s = []
    for g, k in enumerate(sizes):
        gx = 6 + g * (bw + gap)
        gy = 6
        s.append("<rect x='%d' y='%d' width='%d' height='%d' rx='8' fill='%s' stroke='%s' stroke-width='2'/>"
                 % (gx, gy, bw, bh, "#cfe9d8" if g == shaded else "#fff", LINE))
        for i in range(k):
            cx = gx + 5 + STEP / 2 + (i % cols) * STEP
            cy = gy + 5 + STEP / 2 + (i // cols) * STEP
            s.append(item(kind, cx, cy))
    W = 12 + len(sizes) * bw + (len(sizes) - 1) * gap
    H = 12 + bh
    return svg_wrap(W, H, "".join(s), "groups of %s: %s" % (PLURAL[kind], " and ".join(str(k) for k in sizes)))


# ============================================================ set 1: equal parts or not?
NOT_EQ = "Not equal parts"


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
            e = "There are %d parts. %s the <b>same size</b>. So there are %d equal parts." % (
                n, "Both are" if n == 2 else "They are all", n)
            if L > 1 and L != n:
                e += " Count the parts, not the lines."
            right = parts(n)
            cands = [parts(L) if L != n else None, NOT_EQ, parts(3), parts(6 - n)]
        else:
            e = ("There are %d parts, but they are <b>not the same size</b>. %s. So they are not equal parts."
                 % (n, "One part is much bigger" if n == 2 else "Some parts are bigger"))
            right = NOT_EQ
            cands = [parts(n), parts(L) if L != n else None, parts(6 - n), parts(3)]
        its.append(mcq(fig(one_svg(sh)) + "Is this %s cut into equal parts? How many?" % noun, right, cands, e))

    plan = [(2, False, 0), (4, False, 1), (2, True, 2), (4, True, 3), (2, False, 3), (4, False, 4), (2, True, 4), (4, True, 0)]
    for qi, (n, find_not, pi) in enumerate(plan):
        if not find_not:
            good, bads = EQ(n, pi), [UNEQ(n, qi + j) for j in range(3)]
            q = "Each shape has %d parts. Which shape has <b>equal</b> parts?" % n
            e = (lambda n: lambda L: "All the shapes have %d parts. Only in shape <b>%s</b> are the parts "
                 "all the same size." % (n, L))(n)
        else:
            good, bads = UNEQ(n, pi), [EQ(n, qi + j) for j in range(3)]
            q = "Each shape has %d parts. Which shape does <b>not</b> have equal parts?" % n
            e = (lambda n: lambda L: "In shape <b>%s</b> the parts are not the same size. The other shapes have "
                 "%d parts that are all the same size." % (L, n))(n)
        its.append(letters_q((good, ()), [(b, ()) for b in bads], q,
                             "four shapes A to D, each cut into %d parts" % n, e, rnd))
    assert len(its) == 20, len(its)
    return {"title": "Equal parts or not?", "items": its}


# ============================================================ sets 2 and 3: halves, quarters of shapes
def yes_no(sh, want):
    """Is this shape cut into halves (want=2) or quarters (want=4)? Answer by the real parts."""
    n, L = sh["n"], sh["lines"]
    noun = NOUN[sh["kind"]]
    W = WORD[want].capitalize()
    if not is_equal(sh):
        right = "No, not equal"
        e = "There are %d parts, but they are <b>not the same size</b>. %s must be equal parts." % (n, W)
        cands = ["Yes, %d parts" % n, "Yes, %s" % WORD[want], "No, %s" % WORD[6 - want]]
    elif n == want:
        right = "Yes, %s" % WORD[want]
        e = "There are <b>%d equal parts</b>. %d equal parts are %s." % (n, n, WORD[n])
        if L > 1 and L != n:
            e += " Count the parts, not the %d lines." % L
        cands = ["No, not equal", "No, %s" % WORD[6 - want],
                 "No, %s" % ("only 1 line" if L == 1 else "%d lines" % L)]
    else:
        right = "No, %s" % WORD[n]
        e = "There are <b>%d equal parts</b>, so they are %s, not %s." % (n, WORD[n], WORD[want])
        if L == 2 and want == 2:
            e += " There are 2 lines, but 4 parts. Count the parts."
        cands = ["Yes, %s" % WORD[want], "Yes, %d lines" % L if L == want else "Yes, %d parts" % n, "No, not equal"]
    return mcq(fig(one_svg(sh)) + "Is this %s cut into %s?" % (noun, WORD[want]), right, cands, e)


def which_cut(n, gi, bads, rnd):
    w = WORD[n]
    e = (lambda L: "Shape <b>%s</b> has %d equal parts. That is %s. Check the others: %s are "
         "%d parts that are the <b>same size</b>." % (L, n, w, w, n))
    return letters_q((EQ(n, gi), ()), [(b, ()) for b in bads], "Which shape is cut into <b>%s</b>?" % w,
                     "four shapes A to D for %s" % w, e, rnd)


def which_shaded(n, good, bads, rnd):
    e = (lambda L: "Shape <b>%s</b> has %d equal parts and 1 is shaded, so %s is shaded. "
         "The parts must be equal, and only 1 of %d is shaded." % (L, n, A_ONE[n], n))
    return letters_q(good, bads, "Which shape has <b>%s</b> shaded?" % A_ONE[n],
                     "four shapes A to D with shading", e, rnd)


def set_halves(rnd):
    its = []
    for sh in [c_sectors([180, 180]), r_hstrips([.5, .5]), sq(r_diag1), check_unequal(c_chord(-0.45)),
               check_unequal(r_hstrips([.3, .7])), c_sectors([90] * 4)]:
        its.append(yes_no(sh, 2))
    its.append(which_cut(2, 0, [UNEQ(2, 0), EQ(4, 1), UNEQ(2, 2)], rnd))
    its.append(which_cut(2, 1, [UNEQ(2, 1), EQ(4, 0), UNEQ(2, 3)], rnd))
    its.append(which_cut(2, 4, [UNEQ(2, 4), EQ(4, 2), UNEQ(2, 0)], rnd))
    its.append(which_cut(2, 5, [UNEQ(2, 2), EQ(4, 3), UNEQ(2, 1)], rnd))
    its.append(which_shaded(2, (EQ(2, 0), (0,)), [(UNEQ(2, 1), (0,)), (EQ(4, 1), (0,)), (EQ(2, 1), (0, 1))], rnd))
    its.append(which_shaded(2, (EQ(2, 3), (1,)), [(UNEQ(2, 0), (1,)), (EQ(4, 0), (3,)), (EQ(2, 2), (0, 1))], rnd))
    for sh, k in [(c_sectors([180, 180]), 1), (r_vstrips([.5, .5]), 0), (sq(r_diag1), 0)]:
        check_equal(sh)
        noun = NOUN[sh["kind"]]
        its.append(mcq(fig(one_svg(sh, (k,))) + "How much of the %s is shaded?" % noun, "a half",
                       ["a quarter", "two halves", "the whole %s" % noun],
                       "The %s has <b>2 equal parts</b>. 1 part is shaded. So <b>a half</b> is shaded." % noun))
    sh = check_equal(r_vstrips([.5, .5]))
    its.append(mcq(fig(one_svg(sh, (0,))) + "A half is shaded. How many more halves make the whole?",
                   "1 more", ["2 more", "0 more", "3 more"],
                   "The whole is <b>2 halves</b>. 1 half is shaded. 1 more half makes the whole."))
    its.append(mcq("What do we call 2 equal parts?", "halves", ["twos", "quarters", "wholes"],
                   "2 equal parts are called <b>halves</b>. We do not say twos."))
    its.append(mcq("How many halves make a whole?", "2", ["1", "4", "3"],
                   "A whole cut into halves has 2 equal parts. <b>2 halves</b> make a whole."))
    its.append(mcq("A square has 1 cut down the middle. How many equal parts are there?",
                   "2", ["1", "4", "3"],
                   "1 cut makes <b>2 parts</b>. The cut is in the middle, so the parts are equal. They are halves."))
    its.append(mcq("A shape has 2 parts. One is big. One is small. Are they halves?",
                   "No, not equal", ["Yes, 2 parts", "Yes, 1 cut", "No, quarters"],
                   "Halves must be the <b>same size</b>. A big part and a small part are not halves."))
    assert len(its) == 20, len(its)
    return {"title": "Halves of shapes and objects", "items": its}


def set_quarters(rnd):
    its = []
    for sh in [c_sectors([90] * 4), r_vstrips([.25] * 4), sq(r_grid, 2, 2), r_x(),
               check_unequal(r_cross(.3, .35)), check_unequal(c_parallel([-.5, 0, .5])), r_vstrips([.5, .5])]:
        its.append(yes_no(sh, 4))
    its.append(which_cut(4, 0, [UNEQ(4, 2), EQ(2, 1), UNEQ(4, 1)], rnd))
    its.append(which_cut(4, 1, [UNEQ(4, 0), EQ(2, 0), UNEQ(4, 3)], rnd))
    its.append(which_cut(4, 4, [UNEQ(4, 1), EQ(2, 3), UNEQ(4, 2)], rnd))
    its.append(which_cut(4, 5, [UNEQ(4, 3), EQ(2, 5), UNEQ(4, 0)], rnd))
    its.append(which_shaded(4, (EQ(4, 1), (2,)), [(UNEQ(4, 2), (1,)), (EQ(2, 1), (0,)), (EQ(4, 2), (0, 1))], rnd))
    its.append(which_shaded(4, (EQ(4, 0), (3,)), [(UNEQ(4, 0), (0,)), (EQ(2, 0), (1,)), (EQ(4, 3), (0, 2))], rnd))
    for sh, k in [(c_sectors([90] * 4, start=45), 3), (r_grid(2, 2), 0), (r_hstrips([.25] * 4, h=80), 1)]:
        check_equal(sh)
        noun = NOUN[sh["kind"]]
        its.append(mcq(fig(one_svg(sh, (k,))) + "How much of the %s is shaded?" % noun, "a quarter",
                       ["a half", "four quarters", "the whole %s" % noun],
                       "The %s has <b>4 equal parts</b>. 1 part is shaded. So <b>a quarter</b> is shaded. "
                       "Count all 4 parts, not only the white ones." % noun))
    sx = check_equal(r_x())
    its.append(mcq(fig(one_svg(sx, (), "square cut corner to corner both ways into 4 triangles")) +
                   "This square has 2 lines. How many equal parts does it have?", "4", ["2", "3", "1"],
                   "Count the parts, not the lines. 2 lines cross and make <b>4 equal parts</b>. They are quarters."))
    its.append(mcq("What do we call 4 equal parts?", "quarters", ["fours", "halves", "wholes"],
                   "4 equal parts are called <b>quarters</b>. We do not say fours."))
    its.append(mcq("How many quarters make a whole?", "4", ["2", "3", "1"],
                   "Quarters are 4 equal parts. <b>4 quarters</b> make a whole."))
    its.append(mcq("A cake is cut into 4 parts. One part is much bigger. Are they quarters?",
                   "No, not equal", ["Yes, 4 parts", "No, halves", "Yes, quarters"],
                   "Quarters must be <b>4 equal parts</b>. The cake has 4 parts, but they are not the same size."))
    assert len(its) == 20, len(its)
    return {"title": "Quarters of shapes and objects", "items": its}


# ============================================================ set 4: half and a quarter of an amount
def half_q(n, kind):
    h = n // 2
    assert n % 2 == 0 and h * 2 == n
    noun = PLURAL[kind]
    cands = [n // 4 if n % 4 == 0 else None, n * 2, n, 2, h + 1, h - 1]
    e = ("Share the %d %s into <b>2 equal groups</b>. Each group has %d. %d + %d = %d. So half of %d is <b>%d</b>."
         % (n, noun, h, h, h, n, n, h))
    return mcq(fig(items_svg(n, kind)) + "Find half of %d %s." % (n, noun), str(h),
               [str(c) for c in cands if c is not None and c > 0], e)


def quarter_q(n, kind):
    k = n // 4
    assert n % 4 == 0 and k * 4 == n
    noun = PLURAL[kind]
    cands = [n // 2, 4, n - 4, n, n - k, k + 1]
    e = ("Share the %d %s into <b>4 equal groups</b>. Each group has %d. %d + %d + %d + %d = %d. "
         "So a quarter of %d is <b>%d</b>." % (n, noun, k, k, k, k, k, n, n, k))
    return mcq(fig(items_svg(n, kind)) + "Find a quarter of %d %s." % (n, noun), str(k),
               [str(c) for c in cands if c > 0], e)


NOT_EQ_G = "Not equal groups"
GROUP_CH = ["half", "a quarter", "the whole", NOT_EQ_G]


def group_q(sizes, kind):
    total = sum(sizes)
    noun = PLURAL[kind]
    eq = len(set(sizes)) == 1
    if not eq:
        right = NOT_EQ_G
        e = ("There are 2 groups, but one has %d and one has %d. They are <b>not equal</b>, so the green group "
             "is not a half." % (max(sizes), min(sizes)))
    else:
        right = "half" if len(sizes) == 2 else "a quarter"
        e = ("There are %d %s in <b>%d equal groups</b> of %d. 1 group is green. So the green group is <b>%s</b> "
             "of the %s." % (total, noun, len(sizes), sizes[0], right, noun))
    q = fig(groups_svg(sizes, 0, kind)) + "What part of the %s is in the green box?" % noun
    return mcq(q, right, [c for c in GROUP_CH if c != right], e)


def set_amounts(rnd):
    its = []
    for n, kind in [(4, "counter"), (6, "sweet"), (8, "counter"), (10, "sweet"), (12, "counter"),
                    (14, "sweet"), (16, "counter"), (20, "sweet")]:
        its.append(half_q(n, kind))
    for n, kind in [(4, "sweet"), (8, "counter"), (12, "sweet"), (16, "sweet"), (20, "counter")]:
        its.append(quarter_q(n, kind))
    for sizes, kind in [([3, 3], "counter"), ([8, 8], "sweet"), ([3, 3, 3, 3], "sweet"),
                        ([2, 2, 2, 2], "counter"), ([5, 3], "counter")]:
        its.append(group_q(sizes, kind))
    its.append(mcq(fig(groups_svg([4, 4, 4], 0, "counter")) +
                   "12 counters are in 3 equal groups. Is the green box a quarter?",
                   "No, 3 groups", ["Yes, 4 counters", "Yes, a quarter", "No, a half"],
                   "A quarter is 1 of <b>4 equal groups</b>. Here there are only 3 groups. "
                   "There are 4 counters in the box, but that does not make it a quarter."))
    its.append(mcq("Freya and Jack share 10 sweets. Freya gets 6. Jack gets 4. Do they each get half?",
                   "No, not equal", ["Yes, 2 people", "Yes, 10 sweets", "No, quarters"],
                   "Half of 10 is 5. Halves are <b>equal</b>: 5 and 5. 6 and 4 are not equal."))
    assert len(its) == 20, len(its)
    return {"title": "Half and a quarter of an amount", "items": its}


# ============================================================ set 5: real-life problems
def set_stories(rnd):
    its = []
    pz = check_equal(c_sectors([90] * 4, start=45))
    its.append(mcq(fig(one_svg(pz, (0,), "a pizza cut into 4 equal slices, 1 green")) +
                   "Ruby eats the green slice of pizza. How much of the pizza does she eat?", "a quarter",
                   ["a half", "4 slices", "the whole pizza"],
                   "The pizza has <b>4 equal slices</b>. Ruby eats 1 of them. That is <b>a quarter</b>."))
    ck = check_equal(r_vstrips([.5, .5]))
    its.append(mcq(fig(one_svg(ck, (1,), "a cake cut into 2 equal parts, 1 green")) +
                   "Harry has the green part of the cake. How much does he have?", "a half",
                   ["a quarter", "2 parts", "the whole cake"],
                   "The cake has <b>2 equal parts</b>. Harry has 1 of them. That is <b>a half</b>."))
    bar = check_equal(r_grid(2, 4, w=120, h=60))
    its.append(mcq(fig(one_svg(bar, (), "a chocolate bar of 8 squares")) +
                   "Alfie breaks this chocolate bar in half. How many squares are in each half?", "4",
                   ["2", "8", "16"],
                   "The bar has 8 squares. Half of 8 is <b>4</b>, because 4 + 4 = 8."))
    its.append(mcq(fig(items_svg(18, "sweet")) +
                   "Arjun has these sweets. He gives half to Maya. How many sweets does Maya get?", "9",
                   ["18", "36", "8"],
                   "There are 18 sweets. Share them into 2 equal groups. 9 + 9 = 18. Maya gets <b>9</b>."))
    st = [
        ("Freya has half of a cake. Leo has a quarter of the same cake. Who has more?", "Freya",
         ["Leo", "They have the same", "You can’t tell"],
         "A half is 1 of 2 equal parts. A quarter is 1 of 4 equal parts. 4 parts are smaller. "
         "So <b>Freya</b> has more."),
        ("Which is bigger: half of an orange or a quarter of the same orange?", "a half",
         ["a quarter", "They are the same", "You can’t tell"],
         "4 is more than 2, but more parts means <b>smaller</b> parts. So <b>a half</b> is bigger."),
        ("Amelia shares a pizza equally with 1 friend. How much does each one get?", "a half",
         ["a quarter", "the whole pizza", "two halves"],
         "Amelia and 1 friend are <b>2 people</b>. 2 equal parts are halves. Each one gets a half."),
        ("Oliver shares a cake equally with 3 friends. How much does each one get?", "a quarter",
         ["a half", "the whole cake", "3 parts"],
         "Oliver and 3 friends are <b>4 people</b>. 4 equal parts are quarters. Do not forget to count Oliver."),
        ("Isla and Noah share 10 grapes equally. How many grapes does each one get?", "5",
         ["10", "20", "2"],
         "Share 10 into 2 equal groups. 5 + 5 = 10. Each one gets <b>5</b>."),
        ("4 friends share 8 strawberries equally. How many does each friend get?", "2",
         ["4", "8", "12"],
         "Share 8 into 4 equal groups. 2 + 2 + 2 + 2 = 8. A quarter of 8 is <b>2</b>."),
        ("There are 14 children in a group. Half of them play football. How many play football?", "7",
         ["14", "28", "6"],
         "Half of 14 is <b>7</b>, because 7 + 7 = 14."),
        ("A box has 16 crayons. A quarter of them are red. How many are red?", "4",
         ["8", "12", "16"],
         "Share 16 into 4 equal groups. 4 + 4 + 4 + 4 = 16. A quarter of 16 is <b>4</b>."),
        ("Evie shares 12 stickers equally with her friend. How many does each one get?", "6",
         ["12", "24", "3"],
         "2 people share. Half of 12 is <b>6</b>, because 6 + 6 = 12."),
        ("Jack has 6 biscuits. He gives half of them to Zara. How many does Jack have left?", "3",
         ["6", "2", "12"],
         "Half of 6 is 3. Jack gives 3 away, so he has <b>3</b> left."),
        ("Kai cuts a sandwich into 2 parts. One is big and one is small. Is each part a half?",
         "No, not equal", ["Yes, 2 parts", "Yes, 1 cut", "No, quarters"],
         "Halves must be the <b>same size</b>. A big part and a small part are not halves."),
        ("Ava folds some paper in half. Then she folds it in half again. She opens it. How many equal parts are there?",
         "4", ["2", "3", "1"],
         "2 folds that cross make <b>4 equal parts</b>. They are quarters."),
        ("Mohammed eats half of a pizza. Then he eats the other half. How much does he eat?", "the whole pizza",
         ["a half", "2 pizzas", "a quarter"],
         "2 halves make 1 whole. Mohammed eats <b>the whole pizza</b>."),
        ("Lily cuts a cake into quarters. She eats 1 quarter. How many quarters are left?", "3",
         ["4", "1", "2"],
         "The whole cake is 4 quarters. Lily eats 1. 4 − 1 = <b>3</b> quarters are left."),
        ("Poppy cuts an apple into quarters. How many pieces does she have?", "4",
         ["2", "1", "8"],
         "Quarters means <b>4 equal pieces</b>."),
        ("Charlie wants to cut a cake in half. Where should he cut?", "down the middle",
         ["near one end", "at a corner", "twice"],
         "A cut <b>down the middle</b> makes 2 equal parts. A cut near one end makes a big part and a small part."),
    ]
    for q, right, cands, e in st:
        its.append(mcq(q, right, cands, e))
    assert len(its) == 20, len(its)
    return {"title": "Real-life halves and quarters", "items": its}


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


def fr(a, b):
    return "<span class='fr'><span class='fn'>%d</span><span class='fd'>%d</span></span>" % (a, b)


def body_html():
    f1 = labeled_row([(check_equal(c_sectors([180, 180], r=46)), ()), (check_unequal(c_chord(0.4, r=46)), ())],
                     ["Equal", "Not equal"],
                     "a circle cut into 2 equal parts and a circle cut into 2 parts that are not equal", gap=40)
    f2 = labeled_row([(check_equal(c_sectors([180, 180], r=46)), (0,)), (check_equal(r_vstrips([.5, .5], w=110, h=70)), (1,)),
                      (check_equal(sq(r_diag1, s=84)), (0,))],
                     ["a half", "a half", "a half"], "a circle, a rectangle and a square, each with a half shaded")
    f3 = labeled_row([(check_equal(c_sectors([90] * 4, r=46)), (0,)), (check_equal(r_grid(2, 2, w=110, h=70)), (3,)),
                      (check_equal(r_x()), (1,))],
                     ["a quarter", "a quarter", "a quarter"],
                     "a circle, a rectangle and a square, each with a quarter shaded")
    f4 = groups_svg([4, 4], 0, "counter")
    f5 = groups_svg([3, 3, 3, 3], 0, "sweet")
    f6 = labeled_row([(check_equal(c_sectors([180, 180], r=46)), (0,)), (check_equal(c_sectors([90] * 4, r=46)), (0,))],
                     ["a half", "a quarter"], "two same-size circles: a half shaded and a quarter shaded", gap=40)
    return (
        "<h2>Equal parts</h2>"
        "<p>To share fairly, cut a shape into <b>equal parts</b>. Equal parts are all the <b>same size</b>.</p>"
        "<figure class='sn-fig'>" + f1 +
        "<figcaption>Both circles have 2 parts. Only the first one has equal parts.</figcaption></figure>"
        "<h2>A half</h2>"
        "<p>Cut a whole into <b>2 equal parts</b>. Each part is <b>a half</b>. 2 halves make the whole.</p>"
        "<figure class='sn-fig'>" + f2 +
        "<figcaption>A half is shaded in each shape.</figcaption></figure>"
        "<h2>A quarter</h2>"
        "<p>Cut a whole into <b>4 equal parts</b>. Each part is <b>a quarter</b>. 4 quarters make the whole.</p>"
        "<figure class='sn-fig'>" + f3 +
        "<figcaption>A quarter is shaded in each shape.</figcaption></figure>" +
        table(["Equal parts", "Each part is", "Written", "The whole"], [
            ["2", "a half", fr(1, 2), "2 halves"],
            ["4", "a quarter", fr(1, 4), "4 quarters"],
        ]) +
        "<h2>Half of an amount</h2>"
        "<p>To find half of a number of things, share them into <b>2 equal groups</b>. Count one group.</p>"
        "<figure class='sn-fig'>" + f4 +
        "<figcaption>Half of 8 counters is 4, because 4 + 4 = 8.</figcaption></figure>"
        "<h2>A quarter of an amount</h2>"
        "<p>To find a quarter, share them into <b>4 equal groups</b>. Count one group.</p>"
        "<figure class='sn-fig'>" + f5 +
        "<figcaption>A quarter of 12 sweets is 3, because 3 + 3 + 3 + 3 = 12.</figcaption></figure>"
        "<h2>A half is bigger than a quarter</h2>"
        "<p>Cut the same whole into <b>more</b> parts, and each part gets <b>smaller</b>.</p>"
        "<figure class='sn-fig'>" + f6 +
        "<figcaption>Same-size circles. A half is bigger than a quarter.</figcaption></figure>" +
        ex("Example 1", "Find half of 10 biscuits.",
           "Share 10 into 2 equal groups. Each group has 5. 5 + 5 = 10.", "5 biscuits") +
        ex("Example 2", "Oliver shares a cake equally with 3 friends. How much does each one get?",
           "Oliver and 3 friends are 4 people. 4 equal parts are quarters.", "a quarter of the cake") +
        "<h2>Common mistakes</h2>" +
        table(["Mistake", "What to do instead"], [
            ["Calling 2 parts halves when they are not the same size", "Check that the parts are equal first"],
            ["Half of 8 is 2, or half of 8 is 16", "Share 8 into 2 equal groups: 4 and 4. Half of 8 is 4"],
            ["Thinking a quarter is bigger than a half because 4 is more than 2",
             "More parts means smaller parts. A half is bigger"],
            ["Counting the lines instead of the parts", "Count the parts: 2 lines can make 4 parts"],
        ])
    )


FAQ = [
    {"q": "What fractions do children learn in Year 1?",
     "a": "In Year 1, children learn to recognise, find and name a half and a quarter. They find halves and quarters of shapes, objects and small amounts, such as half of 8 sweets or a quarter of 12 counters."},
    {"q": "How do you find half of a number in Year 1?",
     "a": "Share the objects into 2 equal groups and count one group. Half of 10 is 5, because 5 + 5 = 10."},
    {"q": "Is a quarter bigger than a half?",
     "a": "No. A quarter is 1 of 4 equal parts and a half is 1 of 2 equal parts, so a half of the same thing is bigger. Folding a piece of paper in half and then in half again shows this well."},
    {"q": "What is a quarter in maths for children?",
     "a": "A quarter is one of four equal parts of a whole. Four quarters make one whole, just like four slices of a pizza cut into quarters."},
]


def mark_large(u, pattern):
    """Tag pictures that must print larger (A-D choices, rows and groups of objects) so they stay readable."""
    rx = re.compile(r"<svg (?=[^>]*aria-label='" + pattern + ")")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u


def gen():
    rnd = random.Random(1105)
    sets = [set_equal(rnd), set_halves(rnd), set_quarters(rnd), set_amounts(rnd), set_stories(rnd)]
    balance(sets, rnd)
    seen = set()
    for s in sets:
        assert len(s["items"]) == 20, (s["title"], len(s["items"]))
        assert sorted(it["a"] for it in s["items"]) == sorted([0, 1, 2, 3] * 5), s["title"]
        for it in s["items"]:
            assert len(set(it["c"])) == 4, it
            assert it["q"].count("<svg") <= 1, it["q"]
            key = json.dumps([it["q"], it["c"]])
            assert key not in seen, it["q"]
            seen.add(key)
            txt = re.sub(r"<[^>]+>", " ", it["q"] + " " + " ".join(it["c"]) + " " + it["e"])
            assert not re.search(r"\b\d+/\d+\b", txt), it["q"]      # words, not fraction numbers
            assert "class='fr'" not in it["q"] + "".join(it["c"]) + it["e"]
            assert "third" not in txt and "fourth" not in txt, it["q"]
    u = {
        "country": "uk", "subject": "maths", "grade": "year-1", "slug": "halves-and-quarters", "sort": 5,
        "updated": UPDATED, "pdf_url": "",
        "title": "Year 1 Halves and Quarters",
        "seo_title": "Year 1 Halves and Quarters Worksheets: Half and Quarter of Shapes and Amounts (Free, with Answers)",
        "short_title": "Halves and quarters",
        "domain": "Fractions",
        "standard_code": "Year 1: Fractions",
        "standard_url": "https://www.gov.uk/government/publications/national-curriculum-in-england-mathematics-programmes-of-study",
        "standard_text": "Recognise, find and name a half as one of two equal parts of an object, shape or quantity; recognise, find and name a quarter as one of four equal parts of an object, shape or quantity.",
        "meta_desc": "Free Year 1 halves and quarters worksheets for the National Curriculum: equal parts, a half and a quarter of shapes and objects, half and a quarter of an amount with counters and sweets, and real-life sharing problems. 100 picture questions with an answer key.",
        "key_big": "A half is 1 of 2 equal parts. A quarter is 1 of 4 equal parts.",
        "key_sub": "The parts must be the same size. To find half of 8, share 8 into 2 equal groups: 4 and 4. A half of something is bigger than a quarter of it.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }
    return mark_large(u, "(four shapes A to D|row of|groups of)")


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
