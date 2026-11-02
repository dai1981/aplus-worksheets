# -*- coding: utf-8 -*-
"""
US Grade 2 Math: Halves, Thirds and Fourths (2.G.A.2-3)
  python tools/gen_us_math_g2_shares.py
Every picture is computed from exact coordinates. The area of every share is checked in code:
"equal" pictures have shares of exactly the same area, "not equal" pictures have a biggest share
at least 1.4 times the smallest, so the difference can be seen.
Grade 2 uses words (halves, thirds, fourths), not fraction numbers.
HTML attributes use single quotes (no backslashes in the JSON).
"""
import json, math, os, random, re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "us", "math", "grade-2")
UPDATED = "2026-11-02"
FILL = "#4fae74"      # shaded share
LINE = "#2b2b2b"
THIN = "#a8a8a8"
FONT = "Arial, Helvetica, sans-serif"
WORD = {2: "halves", 3: "thirds", 4: "fourths"}
ONE = {2: "one half", 3: "one third", 4: "one fourth"}
A_ONE = {2: "a half", 3: "a third", 4: "a fourth"}
NUM = {1: "one", 2: "two", 3: "three", 4: "four", 5: "five"}


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
    """A question whose answer is a picture A-D: build(pos) returns the item with the right picture at pos."""
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


def fr(a, b):
    return "<span class='fr'><span class='fn'>%d</span><span class='fd'>%d</span></span>" % (a, b)


def plural(n, one, many):
    return "%d %s" % (n, one if n == 1 else many)


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


def r_x(w=120, h=72, kind="rectangle"):
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


def sq(fn, *a, s=84):
    return fn(*a, w=s, h=s, kind="square")


def c_sectors(angles, r=44, start=0):
    """Pie pieces. start = angle of the first cut, clockwise from the top."""
    assert abs(sum(angles) - 360) < 1e-9
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


def c_parallel(cuts, r=44):
    """Circle cut by straight up-and-down lines at x = cut * r (from the center). Like cutting a pizza in strips."""
    xs = [-1.0] + list(cuts) + [1.0]

    def left_area(d):            # area of the circle to the left of x = d*r
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
    """Straight cut that misses the center: a big piece and a small piece."""
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
    if sh["kind"] == "grid":
        return draw_grid(sh, shaded, ox, oy)
    s = []
    for i, p in enumerate(sh["pieces"]):
        s.append("<path transform='translate(%.1f %.1f)' d='%s' fill='%s' stroke='%s' stroke-width='2.5' "
                 "stroke-linejoin='round'/>" % (ox, oy, p["d"], FILL if i in shaded else "#fff", LINE))
    return "".join(s)


NOUN = {"rectangle": "rectangle", "square": "square", "circle": "circle", "grid": "rectangle"}


def one_svg(sh, shaded=(), label=None):
    pad = 5
    w, h = sh["w"] + 2 * pad, sh["h"] + 2 * pad
    lab = label or "%s cut into %d pieces%s" % (NOUN[sh["kind"]], sh["n"], ", %d shaded" % len(shaded) if shaded else "")
    return svg_wrap(int(math.ceil(w)), int(math.ceil(h)), draw(sh, shaded, pad, pad), lab)


# ------------------------------------------------------------ rectangles on a grid (shares made of unit squares)
def g_map(rows, cell=22):
    H, W = len(rows), len(rows[0])
    ids = sorted({ch for r in rows for ch in r})
    count = {k: sum(r.count(k) for r in rows) for k in ids}
    for k in ids:                                    # every share must be one connected piece
        cells = [(c, r) for r in range(H) for c in range(W) if rows[r][c] == k]
        seen, todo = {cells[0]}, [cells[0]]
        while todo:
            c, r = todo.pop()
            for dc, dr in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                q = (c + dc, r + dr)
                if q in cells and q not in seen:
                    seen.add(q)
                    todo.append(q)
        assert len(seen) == len(cells), ("share not connected", rows, k)
    pieces = [{"id": k, "area": float(count[k])} for k in ids]
    return {"kind": "grid", "rows": rows, "cols_n": W, "rows_n": H, "cell": cell, "w": W * cell, "h": H * cell,
            "pieces": pieces, "n": len(ids), "lines": None, "total": W * H, "sizes": [count[k] for k in ids]}


def draw_grid(sh, shaded, ox, oy):
    rows, cell, W, H = sh["rows"], sh["cell"], sh["cols_n"], sh["rows_n"]
    ids = [p["id"] for p in sh["pieces"]]
    sh_ids = {ids[i] for i in shaded}
    s = []
    for r in range(H):
        for c in range(W):
            s.append("<rect x='%.1f' y='%.1f' width='%d' height='%d' fill='%s'/>"
                     % (ox + c * cell, oy + r * cell, cell, cell, FILL if rows[r][c] in sh_ids else "#fff"))
    for c in range(1, W):
        s.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='1'/>"
                 % (ox + c * cell, oy, ox + c * cell, oy + H * cell, THIN))
    for r in range(1, H):
        s.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='1'/>"
                 % (ox, oy + r * cell, ox + W * cell, oy + r * cell, THIN))
    for r in range(H):                               # thick lines between shares
        for c in range(W):
            if c + 1 < W and rows[r][c] != rows[r][c + 1]:
                x = ox + (c + 1) * cell
                s.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='3' stroke-linecap='round'/>"
                         % (x, oy + r * cell, x, oy + (r + 1) * cell, LINE))
            if r + 1 < H and rows[r][c] != rows[r + 1][c]:
                y = oy + (r + 1) * cell
                s.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='3' stroke-linecap='round'/>"
                         % (ox + c * cell, y, ox + (c + 1) * cell, y, LINE))
    s.append("<rect x='%.1f' y='%.1f' width='%d' height='%d' fill='none' stroke='%s' stroke-width='3'/>"
             % (ox, oy, W * cell, H * cell, LINE))
    return "".join(s)


GRIDS = {
    "h8_eq": ["AAAB", "ABBB"], "h8_bad": ["AAAB", "AABB"],
    "t12_eq": ["AAAB", "ACBB", "CCCB"], "f12_eq": ["AAAB", "CCBB", "CDDD"],
}
for _k, _rows in GRIDS.items():
    _g = g_map(_rows)
    _eq = len(set(_g["sizes"])) == 1
    assert _eq == ("_eq" in _k), (_k, _g["sizes"])
    if not _eq:
        assert max(_g["sizes"]) / min(_g["sizes"]) >= 1.4, _k


# ------------------------------------------------------------ rows and columns of squares
def rc_svg(rows, cols, cell=24, partial=False):
    """A rectangle cut into rows and columns of same-size squares.
    partial: only the top row and the left column are drawn (the cutting is not finished)."""
    pad = 5
    W, H = cols * cell, rows * cell
    s = ["<rect x='%d' y='%d' width='%d' height='%d' fill='#fff' stroke='%s' stroke-width='2.5'/>" % (pad, pad, W, H, LINE)]
    if not partial:
        for c in range(1, cols):
            s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='2'/>"
                     % (pad + c * cell, pad, pad + c * cell, pad + H, LINE))
        for r in range(1, rows):
            s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='2'/>"
                     % (pad, pad + r * cell, pad + W, pad + r * cell, LINE))
        lab = "rectangle cut into %d rows and %d columns of same-size squares" % (rows, cols)
    else:
        cells = [(0, c) for c in range(cols)] + [(r, 0) for r in range(1, rows)]
        for r, c in cells:
            s.append("<rect x='%d' y='%d' width='%d' height='%d' fill='#e8f3ec' stroke='%s' stroke-width='2'/>"
                     % (pad + c * cell, pad + r * cell, cell, cell, LINE))
        s.append("<rect x='%d' y='%d' width='%d' height='%d' fill='none' stroke='%s' stroke-width='2.5'/>"
                 % (pad, pad, W, H, LINE))
        lab = "rectangle with only the top row and left column of squares drawn"
    return svg_wrap(W + 2 * pad, H + 2 * pad, "".join(s), lab)


def row_sum(rows, cols):
    return " + ".join([str(cols)] * rows) + " = %d" % (rows * cols)


# ------------------------------------------------------------ several shapes in one picture
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


# ------------------------------------------------------------ catalogs of exact pictures for panels (about 90 x 90)
def EQ(n, i):
    lib = {
        2: [lambda: r_vstrips([.5, .5], w=90, h=56), lambda: c_sectors([180, 180]), lambda: r_hstrips([.5, .5], w=90, h=56),
            lambda: c_sectors([180, 180], start=90), lambda: r_diag1(w=90, h=56)],
        3: [lambda: r_vstrips([1 / 3.0] * 3, w=90, h=56), lambda: c_sectors([120] * 3), lambda: r_hstrips([1 / 3.0] * 3, w=90, h=60)],
        4: [lambda: r_grid(2, 2, w=90, h=56), lambda: c_sectors([90] * 4), lambda: r_vstrips([.25] * 4, w=90, h=56),
            lambda: c_sectors([90] * 4, start=45), lambda: r_hstrips([.25] * 4, w=90, h=64)],
    }
    return check_equal(lib[n][i % len(lib[n])]())


def UNEQ(n, i):
    lib = {
        2: [lambda: c_chord(0.4), lambda: r_vstrips([.3, .7], w=90, h=56), lambda: r_corner(.5, w=90, h=56),
            lambda: c_sectors([240, 120]), lambda: r_hstrips([.3, .7], w=90, h=56)],
        3: [lambda: r_vstrips([.2, .5, .3], w=90, h=56), lambda: c_sectors([170, 100, 90]), lambda: c_parallel([-1 / 3.0, 1 / 3.0]),
            lambda: r_hstrips([.25, .5, .25], w=90, h=60)],
        4: [lambda: r_cross(.3, .35, w=90, h=56), lambda: r_vstrips([.15, .35, .2, .3], w=90, h=56),
            lambda: c_sectors([140, 50, 100, 70]), lambda: c_parallel([-.5, 0, .5])],
    }
    return check_unequal(lib[n][i % len(lib[n])]())


# ============================================================ set 1: rows and columns of squares
def set_rows(rnd):
    its = []
    plain = [(2, 3), (3, 3), (2, 5), (3, 4), (4, 2), (4, 5)]
    asks = ["How many squares are there in all?", "How many same-size squares make this rectangle?"]
    for i, (r, c) in enumerate(plain):
        e = ("There are <b>%d rows</b> with <b>%d squares</b> in each row. Count by rows: %s squares."
             % (r, c, row_sum(r, c)))
        its.append(mcq(fig(rc_svg(r, c)) + asks[i % 2], str(r * c),
                       [str(r + c), str((r - 1) * c), str(r * c + c), str(c), str(r * c - 1)], e))

    for r, c in [(2, 4), (3, 5), (4, 3)]:
        right = "%s, %s" % (plural(r, "row", "rows"), plural(c, "column", "columns"))
        e = ("Rows go <b>across</b>. Columns go <b>up and down</b>. Count the squares, not the lines: "
             "%d rows and %d columns. That is %s squares." % (r, c, row_sum(r, c)))
        its.append(mcq(fig(rc_svg(r, c)) + "How many rows and columns does this rectangle have?", right,
                       ["%s, %s" % (plural(c, "row", "rows"), plural(r, "column", "columns")),
                        "%s, %s" % (plural(r - 1, "row", "rows"), plural(c - 1, "column", "columns")),
                        "%s, %s" % (plural(r + 1, "row", "rows"), plural(c + 1, "column", "columns"))], e))

    names = ["Ava", "Eli", "Zoe"]
    for (r, c), nm in zip([(3, 4), (4, 4), (2, 6)], names):
        e = ("Only %d squares are drawn so far. The rectangle will have <b>%d rows</b> of <b>%d squares</b>: "
             "%s squares." % (r + c - 1, r, c, row_sum(r, c)))
        its.append(mcq(fig(rc_svg(r, c, partial=True)) +
                       "%s is cutting this rectangle into same-size squares. When the cutting is done, how many squares will there be?" % nm,
                       str(r * c), [str(r + c - 1), str(r + c), str((r - 1) * c), str(r * c + c)], e))

    for a, d in [(1, 2), (2, 3), (1, 4), (3, 3)]:
        r, c = a + 1, d + 1
        e = ("%s across %s <b>%s</b>. %s down %s <b>%s</b>. %d rows of %d: %s squares."
             % (plural(a, "line", "lines").capitalize(), "makes" if a == 1 else "make", plural(r, "row", "rows"),
                plural(d, "line", "lines").capitalize(), "makes" if d == 1 else "make",
                plural(c, "column", "columns"), r, c, row_sum(r, c)))
        its.append(mcq("A rectangle is cut with %s across and %s down. All the pieces are same-size squares. "
                       "How many squares are there?" % (plural(a, "line", "lines"), plural(d, "line", "lines")),
                       str(r * c), [str(a * d), str(a + d), str(r + c), str(r * c - 1)], e))

    stories = [
        ("A muffin pan has 3 rows. Each row has 4 cups. How many cups are in the pan?", 3, 4, "cups"),
        ("A window has 2 rows of square panes. There are 5 panes in each row. How many panes are there?", 2, 5, "panes"),
        ("A chocolate bar has 4 rows and 5 columns of squares. How many squares are there?", 4, 5, "squares"),
        ("Grace makes a quilt with 4 rows of 4 squares. How many squares are in the quilt?", 4, 4, "squares"),
    ]
    for q, r, c, unit in stories:
        e = "%d rows of %d. Add a row at a time: %s %s." % (r, c, row_sum(r, c), unit)
        its.append(mcq(q, str(r * c), [str(r + c), str((r - 1) * c), str(c), str(r * c + c)], e))
    assert len(its) == 20, len(its)
    return {"title": "Rows and columns of squares", "items": its}


# ============================================================ set 2: equal shares or not?
def shares(k):
    return "1 equal share" if k == 1 else "%d equal shares" % k


NOT_EQ = "Not equal shares"


def set_equal(rnd):
    its = []
    singles = [
        (c_sectors([180, 180], start=90), True), (c_sectors([120] * 3), True), (r_grid(2, 2), True),
        (r_hstrips([1 / 3.0] * 3), True), (c_sectors([90] * 4, start=45), True), (sq(r_diag1), True),
        (c_chord(0.4), False), (r_vstrips([.3, .7]), False), (c_parallel([-1 / 3.0, 1 / 3.0]), False),
        (r_vstrips([.2, .5, .3]), False), (r_cross(.3, .35), False), (c_parallel([-.5, 0, .5]), False),
    ]
    rnd.shuffle(singles)
    for sh, ok in singles:
        (check_equal if ok else check_unequal)(sh)
        n, L = sh["n"], sh["lines"]
        noun = NOUN[sh["kind"]]
        if ok:
            e = "There are %d pieces and %s the <b>same size</b>. So the %s shows %d equal shares: <b>%s</b>." % (
                n, "both are" if n == 2 else "they are all", noun, n, WORD[n])
            if L != n:
                e += " Count the pieces, not the lines: %s %s %d pieces." % (plural(L, "line", "lines"), "makes" if L == 1 else "make", n)
            right = shares(n)
            cands = [shares(L) if L != n and L > 1 else None, NOT_EQ, shares(n + 1), shares(n - 1) if n > 2 else None, shares(n + 2)]
        else:
            e = ("There are %d pieces, but they are <b>not the same size</b>. %s, so these are not equal shares."
                 % (n, "One piece is much bigger than the other" if n == 2 else "Some pieces are bigger than others"))
            right = NOT_EQ
            cands = [shares(n), shares(L) if L != n and L > 1 else None, shares(n + 1), shares(n - 1) if n > 2 else None, shares(n + 2)]
        its.append(mcq(fig(one_svg(sh)) + "Is this %s cut into equal shares? If yes, how many?" % noun, right, cands, e))

    # (shares, find the odd one?, picture index): every right answer is a different picture
    plan = [(2, False, 0), (3, False, 1), (4, False, 2), (2, True, 3), (3, True, 4), (4, True, 5), (4, False, 3), (3, False, 2)]
    for qi, (n, find_not, pi) in enumerate(plan):
        if not find_not:
            good, bads = EQ(n, pi), [UNEQ(n, qi + j) for j in range(3)]
            q = "Each shape has %d pieces. Which shape is cut into <b>equal</b> shares?" % n
            e = (lambda n: lambda L: "All four shapes have %d pieces, so counting is not enough. Only in shape <b>%s</b> "
                 "are all the pieces the same size. It shows %s." % (n, L, WORD[n]))(n)
        else:
            good, bads = UNEQ(n, pi), [EQ(n, qi + j) for j in range(3)]
            q = "Each shape has %d pieces. Which shape is <b>not</b> cut into equal shares?" % n
            e = (lambda n: lambda L: "In shape <b>%s</b> some pieces are bigger than others. The other three shapes have "
                 "%d pieces that are all the same size." % (L, n))(n)
        its.append(letters_q((good, ()), [(b, ()) for b in bads], q,
                             "four shapes A to D, each cut into %d pieces" % n, e, rnd))
    assert len(its) == 20, len(its)
    return {"title": "Equal shares or not?", "items": its}


# ============================================================ set 3: halves, thirds, fourths
NAME_WRONG = {
    2: ["two halves", "one third", "one fourth"],
    3: ["one half", "three thirds", "one fourth"],
    4: ["one third", "one half", "four fourths"],
}


def set_names(rnd):
    its = []
    shaded_q = [(c_sectors([180, 180]), 0), (r_vstrips([.5, .5]), 1), (sq(r_diag1), 0),
                (c_sectors([120] * 3), 2), (r_vstrips([1 / 3.0] * 3), 1), (r_hstrips([1 / 3.0] * 3), 0),
                (c_sectors([90] * 4), 1), (r_grid(2, 2), 3), (r_vstrips([.25] * 4), 2)]
    for sh, k in shaded_q:
        check_equal(sh)
        n = sh["n"]
        noun = NOUN[sh["kind"]]
        e = "The %s has <b>%d equal shares</b> and 1 is shaded. So %s of the %s is shaded." % (noun, n, "half" if n == 2 else A_ONE[n], noun)
        if n > 2:
            e += " Count all %d shares, not only the %d white ones." % (n, n - 1)
        its.append(mcq(fig(one_svg(sh, (k,))) + "What part of the %s is shaded?" % noun, ONE[n], NAME_WRONG[n], e))

    call = ["halves", "thirds", "fourths", "not equal shares"]
    name_q = [c_sectors([90] * 4), r_vstrips([1 / 3.0] * 3), r_hstrips([.25] * 4, h=80), check_unequal(c_parallel([-1 / 3.0, 1 / 3.0]))]
    for sh in name_q:
        n, L = sh["n"], sh["lines"]
        noun = NOUN[sh["kind"]]
        if is_equal(sh):
            right = WORD[n]
            e = "There are %d equal shares. %d equal shares are called <b>%s</b>." % (n, n, WORD[n])
            if L != n:
                e += " Count the shares, not the %s." % plural(L, "line", "lines")
        else:
            right = "not equal shares"
            e = ("There are 3 pieces, but the middle piece is bigger than the two side pieces. "
                 "Thirds must be <b>equal</b> shares, so these are not thirds.")
        its.append(mcq(fig(one_svg(sh)) + "What are the shares of this %s called?" % noun, right,
                       [c for c in call if c != right], e))

    its.append(mcq("A shape is cut into 4 equal shares. What is 1 share called?", "a fourth",
                   ["a third", "a half", "a whole"],
                   "4 equal shares are fourths. So 1 share is <b>a fourth</b> of the shape. "
                   "(It is not a third: count the 4 shares, not the 3 that are left.)"))
    its.append(mcq("Which is another name for a fourth?", "a quarter", ["a third", "a half", "a whole"],
                   "A fourth is also called <b>a quarter</b>. 4 quarters make a whole, just like 4 quarters make a dollar."))
    its.append(mcq("Which word names 3 equal shares?", "thirds", ["threes", "fourths", "halves"],
                   "3 equal shares are called <b>thirds</b>, not threes. Each share is a third."))
    its.append(mcq("Which word names 2 equal shares?", "halves", ["twos", "seconds", "thirds"],
                   "2 equal shares are called <b>halves</b>. Each share is a half. (We do not say twos or seconds.)"))

    def pic_q(n, good, bads):
        noun = "shape"
        e = (lambda n: lambda L: "Shape <b>%s</b> has %d equal shares and 1 is shaded, so %s is shaded. Check the "
             "others: the shares must be equal, and you count <b>all</b> the shares." % (L, n, A_ONE[n]))(n)
        return letters_q(good, bads, "Which %s has <b>%s</b> shaded?" % (noun, ONE[n]),
                         "four shapes A to D with one piece shaded", e, rnd)
    its.append(pic_q(3, (EQ(3, 0), (1,)), [(UNEQ(3, 1), (0,)), (EQ(4, 1), (2,)), (EQ(2, 0), (0,))]))
    its.append(pic_q(4, (EQ(4, 1), (3,)), [(UNEQ(4, 0), (0,)), (EQ(3, 2), (1,)), (EQ(2, 1), (1,))]))
    its.append(pic_q(2, (EQ(2, 4), (1,)), [(UNEQ(2, 0), (1,)), (EQ(3, 1), (0,)), (EQ(4, 2), (0,))]))
    assert len(its) == 20, len(its)
    return {"title": "Halves, thirds and fourths", "items": its}


# ============================================================ set 4: the whole, and bigger or smaller shares
def set_whole(rnd):
    its = []
    whole_q = [c_sectors([180, 180], start=90), r_hstrips([1 / 3.0] * 3, h=78), c_sectors([90] * 4, start=45),
               sq(r_grid, 2, 2), c_sectors([120] * 3)]
    for sh in whole_q:
        check_equal(sh)
        n, L = sh["n"], sh["lines"]
        noun = NOUN[sh["kind"]]
        right = "%s %s" % (NUM[n], WORD[n])
        other = 3 if n != 3 else 4
        cands = ["%s %s" % (NUM[L], WORD[L]) if L != n and L in WORD else None,
                 "%s %s" % (NUM[n], WORD[other]), "%s %s" % (NUM[n - 1], WORD[n]) if n > 2 else None,
                 "%s %s" % (NUM[n + 1], WORD[n]), "%s %s" % (NUM[n], WORD[2] if n != 2 else WORD[4])]
        e = "The %s has %d equal shares, so they are %s. Together they make the whole: <b>%s</b>." % (
            noun, n, WORD[n], right)
        its.append(mcq(fig(one_svg(sh)) + "The %s is cut into equal shares. Which words name the whole %s?" % (noun, noun), right, cands, e))

    its.append(mcq("How many halves make 1 whole?", "2 halves", ["1 half", "4 halves", "3 halves"],
                   "A whole cut into 2 equal shares has 2 halves. <b>2 halves</b> make 1 whole."))
    its.append(mcq("Leo cuts a pie into thirds. How many thirds are in the whole pie?", "3 thirds",
                   ["2 thirds", "1 third", "4 thirds"],
                   "Thirds means 3 equal shares. The whole pie is <b>3 thirds</b>."))
    its.append(mcq("Mia cuts a pizza into fourths. How many fourths make the whole pizza?", "4 fourths",
                   ["3 fourths", "2 fourths", "1 fourth"],
                   "Fourths means 4 equal shares. The whole pizza is <b>4 fourths</b>. "
                   "(It is not 3: count the shares, not the cuts.)"))
    its.append(mcq("2 halves make a whole. How many fourths make a whole?", "4 fourths",
                   ["2 fourths", "3 fourths", "1 fourth"],
                   "Fourths are 4 equal shares, so <b>4 fourths</b> make a whole. 2 fourths make only a half."))
    its.append(mcq("Ben eats 3 thirds of a sandwich. How much of the sandwich does he eat?", "the whole sandwich",
                   ["3 sandwiches", "a third of it", "half of it"],
                   "3 thirds make 1 whole. So Ben eats <b>the whole sandwich</b>, not 3 sandwiches."))

    more_q = [(c_sectors([90] * 4), (0,)), (r_vstrips([1 / 3.0] * 3), (2,)), (r_grid(2, 2), (0, 3))]
    for sh, shaded in more_q:
        check_equal(sh)
        n, k = sh["n"], len(shaded)
        noun = NOUN[sh["kind"]]
        left = n - k
        e = "The whole %s is %s %s. %d %s shaded, so %d more must be shaded: %d + %d = %d." % (
            noun, NUM[n], WORD[n], k, "is" if k == 1 else "are", left, k, left, n)
        its.append(mcq(fig(one_svg(sh, shaded)) +
                       "How many more %s must be shaded to shade the whole %s?" % (WORD[n], noun),
                       "%d more" % left, ["%d more" % v for v in [n, k, left + 1, left - 1, n + 1] if v > 0], e))

    cmp_q = [
        ("Which is bigger: half of a pizza or a third of the same pizza?", "half of the pizza", "a third of the pizza",
         "A half is 1 of 2 equal shares. A third is 1 of 3 equal shares. "
         "When the same pizza is cut into <b>more</b> shares, each share is <b>smaller</b>. So half is bigger."),
        ("Which is bigger: a third of a cake or a fourth of the same cake?", "a third of the cake", "a fourth of the cake",
         "Cutting the same cake into 4 shares makes smaller shares than cutting it into 3. So a third is bigger."),
        ("Which is smaller: half of a sandwich or a fourth of the same sandwich?", "a fourth of it", "half of it",
         "4 is more than 2, so a fourth is <b>smaller</b>. More shares means smaller shares."),
    ]
    for q, right, trap, e in cmp_q:
        its.append(mcq(q, right, [trap, "They are the same", "You can’t tell"], e))

    pairs = [
        (c_sectors([180, 180]), (0,), c_sectors([90] * 4), (1,), A_BIG,
         "A is cut into halves. B is cut into fourths. A half is bigger than a fourth, so <b>A is bigger</b>. "
         "(4 is more than 2, but more shares means smaller shares.)"),
        (r_vstrips([1 / 3.0] * 3, w=108, h=66), (2,), r_vstrips([.5, .5], w=108, h=66), (0,), B_BIG,
         "A is cut into thirds. B is cut into halves. A half is bigger than a third, so <b>B is bigger</b>."),
    ]
    for a, sa, b, sb, right, e in pairs:
        check_equal(a)
        check_equal(b)
        q = fig(pair_svg(a, sa, b, sb, "shapes A and B of the same size, each with one share shaded")) + \
            "Shapes A and B are the same size. Which shaded share is bigger?"
        its.append(mcq(q, right, [c for c in [SAME, A_BIG, B_BIG, CANT] if c != right], e))

    def biggest(find_small, eq_list, right_n, q, nouns):
        good = eq_list[0]
        bads = eq_list[1:]
        if find_small:
            e = lambda L: ("All four %s are the same size. %s <b>%s</b> is cut into %s, the most shares. "
                           "More shares means smaller shares." % (nouns, nouns[:-1].capitalize(), L, WORD[right_n]))
        else:
            e = lambda L: ("All four %s are the same size. %s <b>%s</b> is cut into %s, the fewest shares. "
                           "Fewer shares means bigger shares." % (nouns, nouns[:-1].capitalize(), L, WORD[right_n]))
        return letters_q((good, ()), [(b, ()) for b in bads], q, "four same-size shapes A to D cut into equal shares", e, rnd)
    its.append(biggest(False, [c_sectors([180, 180]), c_sectors([120] * 3), c_sectors([90] * 4), c_sectors([90] * 4, start=45)],
                       2, "The circles are the same size. Which circle has the <b>biggest</b> shares?", "circles"))
    its.append(biggest(True, [r_grid(2, 2, w=90, h=56), r_vstrips([.5, .5], w=90, h=56), r_hstrips([.5, .5], w=90, h=56),
                              r_vstrips([1 / 3.0] * 3, w=90, h=56)],
                       4, "The rectangles are the same size. Which rectangle has the <b>smallest</b> shares?", "rectangles"))
    assert len(its) == 20, len(its)
    return {"title": "The whole, and which share is bigger", "items": its}


# ============================================================ set 5: same size, different shape; stories
SAME, A_BIG, B_BIG, CANT = "Same size", "A is bigger", "B is bigger", "You can’t tell"


def pair_svg(a, sa, b, sb, label):
    return panel_svg([(a, sa), (b, sb)], label, letters="AB", cols=2)


def set_stories(rnd):
    its = []
    S = 84
    pairs = [
        (sq(r_x, s=S), (0,), sq(r_grid, 2, 2, s=S), (3,), SAME,
         "Both squares are cut into 4 equal shares, so each shaded share is <b>a fourth</b> of the same square. "
         "A triangle and a small square can be the same size."),
        (sq(r_diag1, s=S), (1,), sq(r_vstrips, [.5, .5], s=S), (0,), SAME,
         "Both squares are cut in half. Half of a square is the same size, whether the cut goes straight down or corner to corner."),
        (sq(r_vstrips, [.25] * 4, s=S), (1,), sq(r_x, s=S), (2,), SAME,
         "Both squares show fourths. A thin strip and a triangle look different, but each is a fourth of the same square."),
        (r_vstrips([1 / 3.0] * 3, w=108, h=66), (0,), r_hstrips([1 / 3.0] * 3, w=108, h=66), (2,), SAME,
         "Both rectangles are cut into 3 equal shares, so each shaded share is a third of the same rectangle. "
         "One is tall and thin, one is short and wide, but they are the same size."),
        (sq(r_x, s=S), (1,), sq(r_vstrips, [.5, .5], s=S), (1,), B_BIG,
         "A is cut into fourths. B is cut into halves. A half is bigger than a fourth, so <b>B is bigger</b>."),
    ]
    for a, sa, b, sb, right, e in pairs:
        check_equal(a)
        check_equal(b)
        q = fig(pair_svg(a, sa, b, sb, "shapes A and B of the same size, each with one share shaded")) + \
            "Shapes A and B are the same size. Compare the shaded shares."
        its.append(mcq(q, right, [c for c in [SAME, A_BIG, B_BIG, CANT] if c != right], e))

    sx = check_equal(sq(r_x))
    its.append(mcq(fig(one_svg(sx, (), "square cut corner to corner both ways into 4 triangles")) +
                   "Is this square cut into fourths?", "Yes, 4 equal shares",
                   ["No, they are triangles", "No, it has 2 lines", "No, they are halves"],
                   "There are 4 triangles and they are all the same size. So they are <b>fourths</b>. "
                   "Fourths do not have to be squares, and you count the shares, not the 2 lines."))
    for key, n in [("h8_eq", 2), ("t12_eq", 3), ("h8_bad", 2)]:
        g = g_map(GRIDS[key])
        sizes = g["sizes"]
        svg = one_svg(g, (), "rectangle on a grid cut into %d shares" % n)
        if len(set(sizes)) == 1:
            right = "Yes, %d squares each" % sizes[0]
            e = ("Count the small squares in each share: every share has <b>%d squares</b>. The shares have different "
                 "shapes, but they are the same size. So they are %s." % (sizes[0], WORD[n]))
            cands = ["No, not the same shape", "No, one is bigger", "Yes, %d squares each" % g["total"]]
        else:
            big, small = max(sizes), min(sizes)
            right = "No, %d and %d squares" % (big, small)
            e = ("Count the small squares: one share has %d squares and the other has %d. They are <b>not</b> the same "
                 "size, so they are not halves." % (big, small))
            cands = ["Yes, there are 2 shares", "Yes, %d squares each" % small, "Yes, same shape"]
        its.append(mcq(fig(svg) + "Are these %d shares %s?" % (n, WORD[n]), right, cands, e))

    its.append(letters_q((sq(r_cross, .3, .35, s=72), ()),
                         [(sq(r_x, s=72), ()), (sq(r_grid, 2, 2, s=72), ()), (sq(r_vstrips, [.25] * 4, s=72), ())],
                         "The squares are the same size. Which square is <b>not</b> cut into fourths?",
                         "four same-size squares A to D, each cut into 4 pieces",
                         lambda L: ("In square <b>%s</b> the 4 pieces are different sizes. The other squares show fourths: "
                                    "triangles, small squares and strips can all be fourths of the same square." % L), rnd))

    st = [
        ("Mia shares a pizza fairly with 2 friends. What share of the pizza does each person get?", "a third",
         ["a half", "a fourth", "two thirds"],
         "Mia and 2 friends are <b>3 people</b>. The pizza is cut into 3 equal shares, so each person gets a third. "
         "Do not forget to count Mia."),
        ("Leo and 3 friends share a sandwich fairly. What share does each person get?", "a fourth",
         ["a third", "a half", "four fourths"],
         "Leo and 3 friends are <b>4 people</b>. 4 equal shares are fourths, so each person gets a fourth."),
        ("Kai folds a paper in half. Then he opens it. How many equal shares does he see?", "2",
         ["1", "3", "4"],
         "One fold makes <b>2 equal shares</b>: 2 halves. The fold is 1 line, but it makes 2 shares."),
        ("Nora folds a square paper in half. She folds it in half again the other way. Then she opens it. What are the shares?",
         "four fourths", ["two halves", "three thirds", "two fourths"],
         "The 2 folds cross and make <b>4 equal shares</b>. 4 equal shares are fourths, so the paper is four fourths."),
        ("Ava cuts a pie into halves. Ben cuts the same size pie into fourths. Whose pieces are bigger?", "Ava’s pieces",
         ["Ben’s pieces", "They are the same", "You can’t tell"],
         "Ben cut his pie into more shares, so his shares are smaller. Halves are bigger than fourths, so "
         "<b>Ava’s pieces</b> are bigger."),
        ("Noah gets a third of a cake. Zoe gets a fourth of the same size cake. Who gets more cake?", "Noah",
         ["Zoe", "They get the same", "You can’t tell"],
         "A third is 1 of 3 shares. A fourth is 1 of 4 shares. Fewer shares are bigger, so <b>Noah</b> gets more."),
        ("Sam cuts a cake into 4 pieces. One piece is much bigger than the others. Did he cut the cake into fourths?",
         "No, not equal", ["Yes, 4 pieces", "No, it is thirds", "No, it is halves"],
         "Fourths must be <b>4 equal shares</b>. Sam has 4 pieces, but they are not the same size, so they are not fourths."),
        ("Ruby eats 2 halves of an apple. How much of the apple does she eat?", "the whole apple",
         ["half of it", "2 apples", "a fourth of it"],
         "2 halves make 1 whole. Ruby eats <b>the whole apple</b>."),
        ("A brownie is cut into fourths. Omar eats 1 fourth. How many fourths are left?", "3 fourths",
         ["4 fourths", "1 fourth", "2 fourths"],
         "The whole brownie is 4 fourths. 4 fourths take away 1 fourth leaves <b>3 fourths</b>."),
        ("Owen cuts a pan of cornbread into 3 rows and 5 columns of same-size squares. How many pieces are there?",
         "15", ["8", "5", "10"],
         "3 rows of 5 pieces: 5 + 5 + 5 = 15 pieces. (3 + 5 = 8 adds the rows and columns. That is not the number of pieces.)"),
    ]
    for q, right, cands, e in st:
        its.append(mcq(q, right, cands, e))
    assert len(its) == 20, len(its)
    return {"title": "Same size, different shape, and stories", "items": its}


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
    f1 = labeled_row([(check_equal(c_sectors([90] * 4, r=50)), ()), (check_unequal(c_parallel([-.5, 0, .5], r=50)), ())],
                     ["Equal shares", "Not equal"], "a circle cut into 4 equal shares and a circle cut into 4 pieces that are not equal",
                     gap=40)
    f2 = labeled_row([(check_equal(c_sectors([180, 180], r=46)), (0,)), (check_equal(c_sectors([120] * 3, r=46)), (0,)),
                      (check_equal(c_sectors([90] * 4, r=46)), (0,))],
                     ["a half", "a third", "a fourth"], "three same-size circles: one half, one third and one fourth shaded")
    f3 = whole_svg()
    S = 84
    f4 = labeled_row([(check_equal(sq(r_x, s=S)), (0,)), (check_equal(sq(r_grid, 2, 2, s=S)), (0,)),
                      (check_equal(sq(r_vstrips, [.25] * 4, s=S)), (0,))],
                     ["a fourth", "a fourth", "a fourth"], "three same-size squares, each cut into 4 equal shares of different shapes")
    f5 = rc_svg(3, 4, cell=30)
    return (
        "<h2>Equal shares</h2>"
        "<p>To share fairly, cut a shape into <b>equal shares</b>. Equal shares are all the <b>same size</b>.</p>"
        "<figure class='sn-fig'>" + f1 +
        "<figcaption>Both circles have 4 pieces. Only the first one has equal shares.</figcaption></figure>"
        "<h2>Halves, thirds and fourths</h2>"
        "<p>2 equal shares are <b>halves</b>. 3 equal shares are <b>thirds</b>. 4 equal shares are <b>fourths</b> "
        "(also called <b>quarters</b>).</p>"
        "<figure class='sn-fig'>" + f2 +
        "<figcaption>Same-size circles. More shares means smaller shares: a half is bigger than a third, "
        "and a third is bigger than a fourth.</figcaption></figure>" +
        table(["Equal shares", "Name", "One share", "The whole"], [
            ["2", "halves", "a half (half of)", "2 halves"],
            ["3", "thirds", "a third (a third of)", "3 thirds"],
            ["4", "fourths (quarters)", "a fourth (a quarter of)", "4 fourths"],
        ]) +
        "<p>In Grade 3 you will write a half as " + fr(1, 2) + ". For now, use the words.</p>"
        "<h2>The whole</h2>"
        "<p>All the shares together make the <b>whole</b>.</p>"
        "<figure class='sn-fig'>" + f3 +
        "<figcaption>4 fourths make 1 whole. 2 halves and 3 thirds make 1 whole, too.</figcaption></figure>"
        "<h2>Same size, different shape</h2>"
        "<p>Equal shares do <b>not</b> have to be the same shape. They only need to be the same size.</p>"
        "<figure class='sn-fig'>" + f4 +
        "<figcaption>Three same-size squares, each cut into 4 equal shares. A triangle, a small square and a strip: "
        "each one is a fourth of the square.</figcaption></figure>"
        "<h2>Rows and columns of squares</h2>"
        "<p>A rectangle can be cut into rows and columns of same-size squares. Rows go across. Columns go up and down.</p>"
        "<figure class='sn-fig'>" + f5 +
        "<figcaption>3 rows of 4 squares: 4 + 4 + 4 = 12 squares.</figcaption></figure>" +
        ex("Example", "Mia shares a pizza fairly with 2 friends. What share does each person get?",
           "Mia and 2 friends are 3 people. 3 equal shares are thirds.", "a third of the pizza") +
        "<h2>Common mistakes</h2>" +
        table(["Mistake", "What to do instead"], [
            ["Counting pieces without checking they are equal", "First check that all the shares are the same size"],
            ["Thinking a third is bigger than a half because 3 is more than 2", "More shares means smaller shares. A half is bigger"],
            ["Counting the cut lines instead of the shares", "Count the shares: 2 lines can make 3 or 4 shares"],
            ["Thinking shares of different shapes cannot be equal", "Check the size, not the shape"],
            ["Adding rows and columns: 3 rows, 4 columns → 7", "Count by rows: 4 + 4 + 4 = 12"],
        ])
    )


FAQ = [
    {"q": "What are equal shares in 2nd grade math?",
     "a": "Equal shares are pieces of a shape that are all the same size. A circle cut into 4 same-size pieces has 4 equal shares, called fourths."},
    {"q": "Is a third bigger than a half?",
     "a": "No. When the same shape is cut into more shares, each share is smaller. A half of a pizza is bigger than a third, and a third is bigger than a fourth."},
    {"q": "Is a fourth the same as a quarter?",
     "a": "Yes. A fourth and a quarter both mean 1 of 4 equal shares. 4 fourths, or 4 quarters, make 1 whole."},
    {"q": "Do equal shares have to be the same shape?",
     "a": "No. Equal shares must be the same size, not the same shape. A square cut corner to corner into 4 triangles and a square cut into 4 strips both show fourths."},
]


def mark_large(u, pattern):
    """Tag pictures that must print larger (A-D and A-B choices) so the letters stay readable."""
    rx = re.compile(r"<svg (?=[^>]*aria-label='" + pattern + ")")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u


def gen():
    rnd = random.Random(216)
    sets = [set_rows(rnd), set_equal(rnd), set_names(rnd), set_whole(rnd), set_stories(rnd)]
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
            txt = re.sub(r"<[^>]+>", " ", it["q"] + " " + " ".join(it["c"]))
            assert not re.search(r"\b\d+/\d+\b", txt), it["q"]      # Grade 2: words, not fraction numbers
            assert "class='fr'" not in it["q"] + "".join(it["c"]) + it["e"]
    u = {
        "country": "us", "subject": "math", "grade": "grade-2", "slug": "halves-thirds-fourths", "sort": 16,
        "updated": UPDATED, "pdf_url": "",
        "title": "Halves, Thirds and Fourths",
        "seo_title": "Grade 2 Halves, Thirds and Fourths Worksheets: Equal Shares of Circles and Rectangles",
        "short_title": "Halves, thirds and fourths",
        "domain": "Geometry",
        "standard_code": "2.G.A.2–3",
        "standard_url": "https://www.thecorestandards.org/Math/Content/2/G/A/",
        "standard_text": "Partition a rectangle into rows and columns of same-size squares and count to find the total number of them. Partition circles and rectangles into two, three, or four equal shares, describe the shares using the words halves, thirds, half of, a third of, etc., and describe the whole as two halves, three thirds, four fourths. Recognize that equal shares of identical wholes need not have the same shape.",
        "meta_desc": "Free Grade 2 halves, thirds and fourths worksheets with pictures: rows and columns of squares, equal or not equal shares, naming halves, thirds and fourths, the whole as 2 halves or 4 fourths, and equal shares with different shapes. 100 practice questions with answers.",
        "key_big": "Equal shares are the same size. 2 shares are halves, 3 are thirds, 4 are fourths.",
        "key_sub": "The whole is 2 halves, 3 thirds or 4 fourths. More shares means smaller shares, so a half is bigger than a fourth. Equal shares can have different shapes: a triangle and a strip can both be a fourth of the same square.",
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
