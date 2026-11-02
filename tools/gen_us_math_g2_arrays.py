# -*- coding: utf-8 -*-
"""
US Grade 2 Math: Arrays and Repeated Addition (2.OA.C.4)
  python tools/gen_us_math_g2_arrays.py
Arrays are at most 5 rows x 5 columns. Every total and every drawn array is checked in code.
HTML attributes use single quotes (no backslashes in the JSON).
"""
import json, math, os, random, re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "us", "math", "grade-2")
UPDATED = "2026-11-02"
GREEN = "#006633"
FILL = "#cfe6d6"
RED = "#c0392b"
ORANGE = "#d9822b"
BLUE = "#2e6da4"
GRAY = "#9a9a9a"
INK = "#2b2b2b"
FONT = "Arial, Helvetica, sans-serif"
GIRLS = ["Maya", "Ava", "Mia", "Zoe", "Lily", "Emma", "Nora", "Ruby", "Sofia", "Grace"]
BOYS = ["Leo", "Noah", "Eli", "Sam", "Ben", "Omar", "Kai", "Jack", "Luis", "Owen"]
SHAPES = {"dot": "dots", "star": "stars", "square": "squares"}


# ------------------------------------------------------------ helpers
def mcq(q, correct, cands, e):
    """4 choices: correct + the first 3 unique distractors (no 0 or negatives). Positions are set by balance()."""
    correct = str(correct)
    seen = {correct}
    pick = []
    for c in cands:
        c = str(c)
        if c in seen or not c or c.startswith("-") or re.match(r"^0\b", c):
            continue
        seen.add(c)
        pick.append(c)
        if len(pick) == 3:
            break
    assert len(pick) == 3, (q, correct, cands)
    return {"q": q, "c": [correct] + pick, "a": 0, "e": e}


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


def pl(n, word, plural=None):
    return "%d %s" % (n, word if n == 1 else (plural or word + "s"))


def fig(svg):
    return "<div class='qfig'>" + svg + "</div>"


def svg_wrap(w, h, body, label):
    return ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 %d %d' width='%d' height='%d' "
            "role='img' aria-label='%s'><g font-family='%s'>%s</g></svg>" % (w, h, w, h, label, FONT, body))


def text(x, y, t, fs=16, anchor="middle", col=INK):
    return ("<text x='%.1f' y='%.1f' font-size='%d' font-weight='700' fill='%s' text-anchor='%s'>%s</text>"
            % (x, y, fs, col, anchor, t))


def table(head, rows):
    h = "".join("<th>%s</th>" % x for x in head)
    b = "".join("<tr>" + "".join("<td>%s</td>" % c for c in r) + "</tr>" for r in rows)
    return "<div class='sn-tw'><table class='sn-table'><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>" % (h, b)


def ex(title, q, s, a):
    return ("<div class='sn-ex'><span class='sn-ex-t'>%s</span><p class='sn-ex-q'>%s</p>"
            "<p class='sn-ex-s'>%s</p><p class='sn-ex-a'>Answer: %s</p></div>" % (title, q, s, a))


def rep(n, times):
    """n + n + n (times addends)."""
    return " + ".join([str(n)] * times)


# ------------------------------------------------------------ figures
def shape(kind, cx, cy, r, col):
    if kind == "dot":
        return "<circle cx='%.1f' cy='%.1f' r='%.1f' fill='%s'/>" % (cx, cy, r, col)
    if kind == "square":
        return ("<rect x='%.1f' y='%.1f' width='%.1f' height='%.1f' rx='2' fill='%s'/>"
                % (cx - r * 0.9, cy - r * 0.9, r * 1.8, r * 1.8, col))
    pts = []
    for k in range(10):
        rr = r * 1.15 if k % 2 == 0 else r * 0.48
        a = -math.pi / 2 + k * math.pi / 5
        pts.append("%.1f,%.1f" % (cx + rr * math.cos(a), cy + rr * math.sin(a)))
    return "<polygon points='%s' fill='%s'/>" % (" ".join(pts), col)


COL = {"dot": GREEN, "star": ORANGE, "square": BLUE}


def array_body(rows_len, x0, y0, S, r, kind):
    """rows_len: list of how many objects are in each row (left aligned)."""
    return "".join(shape(kind, x0 + c * S + S / 2.0, y0 + i * S + S / 2.0, r, COL[kind])
                   for i, n in enumerate(rows_len) for c in range(n))


def array_svg(rows, cols, kind="dot"):
    assert 1 <= rows <= 5 and 1 <= cols <= 5
    S, o = 30, 6
    body = array_body([cols] * rows, o, o, S, 10, kind)
    assert body.count("<") == rows * cols
    return svg_wrap(cols * S + 2 * o, rows * S + 2 * o, body,
                    "array of %s and %s of %s" % (pl(rows, "row"), pl(cols, "column"), SHAPES[kind]))


def drawing_svg(rows_len, kind="dot"):
    """A drawing that may not be an array (rows of different lengths)."""
    S, o = 30, 6
    body = array_body(rows_len, o, o, S, 10, kind)
    return svg_wrap(max(rows_len) * S + 2 * o, len(rows_len) * S + 2 * o, body,
                    "drawing with rows of " + ", ".join(str(n) for n in rows_len) + " " + SHAPES[kind])


def abcd_svg(panels, kind="dot"):
    """Four drawings in a row labeled A to D. panels: list of row-length lists."""
    S, R = 22, 7
    PW = 5 * S + 20
    rows_max = max(len(p) for p in panels)
    H = 28 + rows_max * S + 6
    W = 4 * PW
    el = []
    for k, p in enumerate(panels):
        assert len(p) <= 5 and max(p) <= 5
        x0 = k * PW
        if k:
            el.append("<line x1='%d' y1='4' x2='%d' y2='%d' stroke='%s' stroke-width='1'/>" % (x0, x0, H - 4, GRAY))
        el.append(text(x0 + 8, 20, "ABCD"[k], 18, "start"))
        dx = x0 + (PW - max(p) * S) / 2.0
        el.append(array_body(p, dx, 28, S, R, kind))
    return svg_wrap(W, H, "".join(el), "four drawings labeled A to D")


def lesson_rc_svg():
    """3 x 4 array: one row and one column outlined and labeled."""
    S, R, x0, y0 = 40, 12, 14, 14
    rows, cols = 3, 4
    el = [array_body([cols] * rows, x0, y0, S, R, "dot")]
    # row 1 outline
    el.append("<rect x='%d' y='%d' width='%d' height='%d' rx='18' fill='none' stroke='%s' stroke-width='3'/>"
              % (x0 + 2, y0 + 2, cols * S - 4, S - 4, RED))
    el.append(text(x0 + cols * S + 12, y0 + S / 2 + 6, "a row", 16, "start", RED))
    # column 1 outline
    el.append("<rect x='%d' y='%d' width='%d' height='%d' rx='18' fill='none' stroke='%s' stroke-width='3' "
              "stroke-dasharray='7 4'/>" % (x0 + 2, y0 + 2, S - 4, rows * S - 4, BLUE))
    el.append(text(x0 + S / 2, y0 + rows * S + 24, "a column", 16, "start", BLUE))
    W = x0 + cols * S + 70
    H = y0 + rows * S + 34
    return svg_wrap(W, H, "".join(el), "array of 3 rows and 4 columns with one row and one column marked")


def lesson_sum_svg(rows, cols, by):
    """Array with the count of each row (to the right) or each column (below)."""
    S, R, x0, y0 = 40, 12, 14, 14
    el = [array_body([cols] * rows, x0, y0, S, R, "dot")]
    if by == "rows":
        for i in range(rows):
            el.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='2'/>"
                      % (x0 + cols * S + 4, y0 + i * S + S / 2, x0 + cols * S + 22, y0 + i * S + S / 2, RED))
            el.append(text(x0 + cols * S + 28, y0 + i * S + S / 2 + 6, str(cols), 18, "start", RED))
        W, H = x0 + cols * S + 50, y0 + rows * S + 14
    else:
        for c in range(cols):
            el.append(text(x0 + c * S + S / 2, y0 + rows * S + 26, str(rows), 18, "middle", BLUE))
        W, H = x0 + cols * S + 14, y0 + rows * S + 36
    return svg_wrap(W, H, "".join(el), "array of %d rows and %d columns, %s counted" % (rows, cols, by))


# ============================================================ set 1: rows and columns
def set_rows_cols(P):
    its = []
    kinds = ["dot", "star", "square"]
    k = 0

    def kind():
        nonlocal k
        k += 1
        return kinds[(k - 1) % 3]

    for r, c in [(3, 5), (2, 4), (4, 3), (5, 2)]:
        kd = kind()
        e = ("Rows go across. Count them from top to bottom: there are <b>%d</b> rows. "
             "Each row has %d %s, but %d is the number of columns." % (r, c, SHAPES[kd], c))
        its.append(mcq(fig(array_svg(r, c, kd)) + "How many rows are in this array?", r, [c, r + 1, r * c, r - 1], e))

    for r, c in [(2, 5), (4, 2), (3, 4), (5, 3)]:
        kd = kind()
        e = ("Columns go up and down. Count them from left to right: there are <b>%d</b> columns. "
             "%d is the number of rows." % (c, r))
        its.append(mcq(fig(array_svg(r, c, kd)) + "How many columns are in this array?", c, [r, c + 1, r * c, c - 1], e))

    for r, c in [(4, 5), (2, 3), (3, 2)]:
        kd = kind()
        e = "Look at one row, across. It has <b>%d</b> %s. Every row has the same number." % (c, SHAPES[kd])
        its.append(mcq(fig(array_svg(r, c, kd)) + "How many %s are in each row?" % SHAPES[kd], c,
                       [r, c + 1, r * c, c - 1], e))

    for r, c in [(5, 4), (3, 1), (4, 2)]:
        kd = kind()
        e = "Look at one column, up and down. It has <b>%d</b> %s. Every column has the same number." % (r, SHAPES[kd])
        its.append(mcq(fig(array_svg(r, c, kd)) + "How many %s are in each column?" % SHAPES[kd], r,
                       [c, r + 1, r * c, r - 1], e))

    for r, c in [(2, 3), (4, 5), (5, 3)]:
        kd = kind()
        rc = lambda a, b: "%s, %s" % (pl(a, "row"), pl(b, "column"))
        e = ("Count across for rows: %d. Count up and down for columns: %d. "
             "So it is <b>%s</b>." % (r, c, rc(r, c)))
        its.append(mcq(fig(array_svg(r, c, kd)) + "Which words tell about this array?", rc(r, c),
                       [rc(c, r), rc(r, r), rc(c, c), rc(r, c + 1)], e))

    its.append(mcq("An array has 4 rows. Each row has 5 dots. How many columns does it have?", 5, [4, 9, 20, 6],
                   "Each row has 5 dots, so there are 5 dots across. That makes <b>5</b> columns."))
    its.append(mcq("An array has 3 columns. Each column has 2 stars. How many rows does it have?", 2, [3, 5, 6, 1],
                   "Each column has 2 stars, so there are 2 stars from top to bottom. That makes <b>2</b> rows."))
    its.append(mcq("In an array, which way does a row go?", "across",
                   ["up and down", "corner to corner", "around the edge"],
                   "A row goes <b>across</b>, like the words in a line of a book. A column goes up and down."))
    assert len(its) == 20, len(its)
    return {"title": "Rows and columns", "items": its}


# ============================================================ set 2: add the rows
def set_add_rows(P):
    its = []
    for r, c, kd in [(3, 4, "dot"), (2, 5, "star"), (4, 3, "square"), (5, 2, "dot"), (3, 5, "star"), (4, 4, "square")]:
        right = rep(c, r)
        wrong = [rep(c, r - 1) if r > 2 else rep(c, r + 2), rep(c, r + 1), "%d + %d" % (r, c), rep(r, r)]
        e = "There are %d rows. Each row has %d. So add %d, %d times: <b>%s</b> = %d." % (r, c, c, r, right, r * c)
        its.append(mcq(fig(array_svg(r, c, kd)) + "Which addition adds the rows?", right, wrong, e))

    for r, c, kd in [(2, 3, "square"), (5, 3, "dot"), (3, 3, "star"), (4, 5, "dot"), (5, 5, "square")]:
        t = r * c
        e = "Add one row at a time: %s. The total is <b>%d</b>." % (
            ", ".join(str(c * (i + 1)) for i in range(r)), t)
        its.append(mcq(fig(array_svg(r, c, kd)) + "Add the rows. %s = <b>?</b>" % rep(c, r), t,
                       [r + c, (r + 1) * c, (r - 1) * c, t - 1], e))

    for r, c, what in [(3, 5, "dots"), (2, 4, "stars"), (5, 4, "squares")]:
        right = rep(c, r)
        e = "%s means %d rows with %d in each row. Add %d, %d times: <b>%s</b>." % (
            pl(r, "row") + " of " + str(c), r, c, c, r, right)
        its.append(mcq("Which addition shows %d rows of %d %s?" % (r, c, what), right,
                       ["%d + %d" % (r, c), rep(c, r + 1), rep(r, r), rep(c, r - 1)], e))

    for n, times in [(3, 4), (5, 3), (2, 5)]:
        t = n * times
        e = "Count on by %d: %s. So the total is <b>%d</b>." % (n, ", ".join(str(n * (i + 1)) for i in range(times)), t)
        its.append(mcq("%s = <b>?</b>" % rep(n, times), t, [n + times, n * (times - 1), n * (times + 1), t + 1], e))

    for n, times in [(4, 3), (5, 4), (3, 5)]:
        t = n * times
        q = "%s + <b>?</b> = %d" % (rep(n, times - 1), t)
        e = ("In repeated addition, every addend is the same. %s = %d, and %d + %d = %d. "
             "The missing number is <b>%d</b>." % (rep(n, times - 1), n * (times - 1), n * (times - 1), n, t, n))
        its.append(mcq(q, n, [t - n, times, n + 1, n - 1], e))
    assert len(its) == 20, len(its)
    return {"title": "Add the rows", "items": its}


# ============================================================ set 3: add the columns
def set_add_cols(P):
    its = []
    for r, c, kd in [(3, 4, "star"), (2, 5, "dot"), (4, 3, "dot"), (2, 3, "square"), (5, 4, "star")]:
        right = rep(r, c)
        wrong = [rep(r, c - 1), rep(r, c + 1), "%d + %d" % (r, c), rep(c, c)]
        assert rep(c, r) not in wrong
        e = "There are %d columns. Each column has %d. So add %d, %d times: <b>%s</b> = %d." % (c, r, r, c, right, r * c)
        its.append(mcq(fig(array_svg(r, c, kd)) + "Which addition adds the columns?", right, wrong, e))

    for r, c, kd in [(2, 4, "dot"), (3, 5, "square"), (4, 2, "star"), (5, 3, "square")]:
        t = r * c
        e = "Add one column at a time: %s. The total is <b>%d</b>." % (
            ", ".join(str(r * (i + 1)) for i in range(c)), t)
        its.append(mcq(fig(array_svg(r, c, kd)) + "Add the columns. %s = <b>?</b>" % rep(r, c), t,
                       [r + c, (c + 1) * r, (c - 1) * r, t + 1], e))

    for r, c, kd in [(3, 4, "square"), (2, 5, "star"), (4, 5, "dot")]:
        t = r * c
        e = ("It is the same array, so it has the same %s. The columns are %s = <b>%d</b>. "
             "Rows or columns, the total does not change." % (SHAPES[kd], rep(r, c), t))
        q = fig(array_svg(r, c, kd)) + "The rows add up: %s = %d. What do the columns add up to?" % (rep(c, r), t)
        its.append(mcq(q, t, [r + c, c * c, r * r, t + 1], e))

    for r, c, kd in [(2, 4, "star"), (3, 2, "dot"), (2, 3, "star")]:
        right = "%s and %s" % (rep(c, r), rep(r, c))
        wrong = ["%s and %s" % (rep(c, r), rep(c, c)), "%s and %s" % (rep(r, r), rep(r, c)),
                 "%s and %s" % (rep(c, r + 1), rep(r, c + 1))]
        e = "Rows: %s = %d. Columns: %s = %d. <b>Both</b> give %d." % (rep(c, r), r * c, rep(r, c), r * c, r * c)
        its.append(mcq(fig(array_svg(r, c, kd)) + "Which two additions both match this array?", right, wrong, e))

    for c, r, what in [(4, 2, "dots"), (5, 3, "stars")]:
        right = rep(r, c)
        e = "%d columns with %d in each column. Add %d, %d times: <b>%s</b> = %d." % (c, r, r, c, right, r * c)
        its.append(mcq("An array has %d columns. Each column has %d %s. Which addition adds the columns?" % (c, r, what),
                       right, [rep(c, c), "%d + %d" % (c, r), rep(r, c - 1)], e))

    for r, c in [(3, 5), (2, 3), (4, 3)]:
        nm, he, his = P.next()
        m, mhe, _ = P.next()
        right = rep(r, c)
        e = ("The array has %d rows of %d, so it has %d columns of %d. %s adds the columns: <b>%s</b> = %d. "
             "The total is the same as %s's." % (r, c, c, r, m, right, r * c, nm))
        its.append(mcq("%s adds the rows of an array: %s. %s adds the columns of the same array. "
                       "Which addition does %s write?" % (nm, rep(c, r), m, mhe),
                       right, [rep(c, r), rep(r, r), "%d + %d" % (c, r), rep(r, c - 1)], e))
    assert len(its) == 20, len(its)
    return {"title": "Add the columns", "items": its}


# ============================================================ set 4: match arrays and equations
def abcd_item(prompt, right_panel, wrong_panels, e, kind):
    """A-D picture question. The picture is built in balance() so the right letter lands on its target."""
    it = {"q": "", "c": ["A", "B", "C", "D"], "a": 0, "e": e,
          "_abcd": (prompt, right_panel, wrong_panels, kind)}
    return it


def set_match(P):
    its = []
    for r, c, kd in [(3, 4, "dot"), (2, 5, "square"), (4, 2, "star"), (5, 3, "dot"), (3, 3, "square")]:
        t = r * c
        right = "%s = %d" % (rep(c, r), t)
        wrong = ["%s = %d" % (rep(c, r - 1), c * (r - 1)) if r > 2 else "%s = %d" % (rep(c, r + 2), c * (r + 2)),
                 "%d + %d = %d" % (r, c, r + c),
                 "%s = %d" % (rep(c, r + 1), c * (r + 1)),
                 "%s = %d" % (rep(r, r), r * r)]
        if r == c:
            wrong[3] = "%s = %d" % (rep(r, r), t - 1)
        e = "There are %d rows of %d. Add the rows: <b>%s</b>." % (r, c, right)
        its.append(mcq(fig(array_svg(r, c, kd)) + "Which equation matches this array?", right, wrong, e))

    # which array shows the addition? (never use the turned array: it matches by columns)
    for r, c, kd in [(3, 4, "dot"), (2, 5, "star"), (4, 3, "square"), (5, 2, "dot"), (3, 5, "square"), (4, 4, "star")]:
        cands = [(r - 1, c), (r + 1, c), (r, c - 1), (r, c + 1), (r - 1, c + 1)]
        wrong = [x for x in cands if 1 <= x[0] <= 5 and 1 <= x[1] <= 5 and x != (c, r)][:3]
        assert len(wrong) == 3
        wd = ", ".join("%s of %d" % (pl(w[0], "row"), w[1]) for w in wrong)
        e = ("%s means %d rows with %d in each row. <b>{L}</b> has %d rows of %d. "
             "The others have %s." % (rep(c, r), r, c, r, c, wd))
        its.append(abcd_item("Which array shows %s?" % rep(c, r), [c] * r, [[w[1]] * w[0] for w in wrong], e, kd))

    for r, c, kd, wrong in [(3, 4, "dot", [[4, 4, 3], [4, 5, 4], [3, 4, 4]]),
                            (4, 5, "square", [[5, 5, 5, 4], [4, 5, 5, 5], [5, 5, 3, 5]]),
                            (2, 3, "star", [[3, 2], [3, 4], [2, 3]]),
                            (5, 4, "dot", [[4, 4, 4, 4, 3], [4, 4, 5, 4, 4], [4, 3, 4, 4, 4]])]:
        # every wrong drawing has rows of different lengths, so it is not an array
        assert all(len(set(w)) > 1 for w in wrong) and len({tuple(w) for w in wrong}) == 3
        e = ("In an array, every row has the same number. <b>{L}</b> has %d rows with %d in each row. "
             "In the other drawings, one row is longer or shorter." % (r, c))
        its.append(abcd_item("Which drawing is an array?", [c] * r, wrong, e, kd))

    for r, c in [(4, 2), (2, 3), (5, 3)]:
        t = r * c
        right = "%s = %d" % (rep(c, r), t)
        e = "%d rows of %d: add %d, %d times. <b>%s</b>." % (r, c, c, r, right)
        its.append(mcq("Which equation shows %d rows of %d?" % (r, c), right,
                       ["%d + %d = %d" % (r, c, r + c), "%s = %d" % (rep(r, r), r * r),
                        "%s = %d" % (rep(c, r - 1), c * (r - 1)) if r > 2 else "%s = %d" % (rep(c, r + 1), c * (r + 1))],
                       e))

    its.append(mcq("Which addition could match an array?", "4 + 4 + 4", ["4 + 3 + 4", "4 + 5 + 4", "3 + 4 + 5"],
                   "In an array, every row has the same number. Only <b>4 + 4 + 4</b> has equal addends."))
    its.append(mcq("Which addition could show the rows of an array?", "5 + 5", ["5 + 4", "2 + 5 + 2", "5 + 3 + 5"],
                   "Every row in an array is the same size. Only <b>5 + 5</b> adds the same number each time."))
    assert len(its) == 20, len(its)
    return {"title": "Match arrays and equations", "items": its}


# ============================================================ set 5: word problems
STORIES = [
    # (text, rows, cols, unit, ask)  ask: "all" = how many in all, "eq" = which equation
    ("An egg carton has 2 rows of eggs. Each row has 5 eggs. How many eggs are in the carton?", 2, 5, "eggs", "all"),
    ("{N} puts chairs in 4 rows. Each row has 3 chairs. How many chairs are there in all?", 4, 3, "chairs", "all"),
    ("A muffin pan has 3 rows. Each row has 4 cups. How many muffins can it bake at one time?", 3, 4, "muffins", "all"),
    ("{N} plants carrots in 5 rows. {He} puts 4 carrots in each row. How many carrots does {he} plant?", 5, 4, "carrots", "all"),
    ("A building has 4 floors. Each floor has 5 windows in a row. How many windows are there?", 4, 5, "windows", "all"),
    ("There are 5 rows of desks in a classroom. Each row has 5 desks. How many desks are there?", 5, 5, "desks", "all"),
    ("{N} bakes cookies on a tray. There are 3 rows with 3 cookies in each row. How many cookies are on the tray?", 3, 3, "cookies", "all"),
    ("A box of paints has 2 rows. Each row has 3 paints. How many paints are in the box?", 2, 3, "paints", "all"),
    ("Kids march in a band. There are 5 rows with 2 kids in each row. How many kids are in the band?", 5, 2, "kids", "all"),
    ("A wall has 4 rows of tiles. Each row has 4 tiles. How many tiles are on the wall?", 4, 4, "tiles", "all"),
    ("{N} has a sheet of stamps. It has 3 rows of 5 stamps. Which equation shows how many stamps there are?", 3, 5, "stamps", "eq"),
    ("A parking lot has 5 rows. Each row has 3 cars. Which equation shows how many cars there are?", 5, 3, "cars", "eq"),
    ("{N} puts stickers on a page in 2 rows. Each row has 4 stickers. Which equation shows the total?", 2, 4, "stickers", "eq"),
    ("A farm has 3 rows of apple trees. Each row has 2 trees. Which equation shows how many trees there are?", 3, 2, "trees", "eq"),
    ("{N} lines up toy cars in 4 rows of 5. Which equation shows how many toy cars {he} has?", 4, 5, "toy cars", "eq"),
    ("A garden has 4 rows of flowers. Each row has 2 flowers. Which equation shows how many flowers there are?", 4, 2, "flowers", "eq"),
]


def set_stories(P):
    its = []
    for tpl, r, c, unit, ask in STORIES:
        nm, he, his = P.next()
        q = tpl.format(N=nm, He=cap(he), he=he)
        t = r * c
        if ask == "all":
            u = lambda x: "%d %s" % (x, unit)
            e = "%d rows of %d is an array. Add the rows: %s = <b>%d</b> %s." % (r, c, rep(c, r), t, unit)
            its.append(mcq(q, u(t), [u(r + c), u((r - 1) * c), u((r + 1) * c), u(t - 1)], e))
        else:
            right = "%s = %d" % (rep(c, r), t)
            wrong = ["%d + %d = %d" % (r, c, r + c),
                     "%s = %d" % (rep(c, r + 1), c * (r + 1)),
                     "%s = %d" % (rep(c, r - 1), c * (r - 1)) if r > 2 else "%s = %d" % (rep(r, r), r * r),
                     "%s = %d" % (rep(r, r), r * r)]
            if r == c:
                wrong[2] = "%s = %d" % (rep(c, r), t + 1)
                wrong[3] = "%d + %d + %d = %d" % (c, c, c, 3 * c)
            e = "%d rows of %d: add %d, %d times. <b>%s</b>." % (r, c, c, r, right)
            its.append(mcq(q, right, wrong, e))

    opts = ["1 dot is missing", "1 dot too many", "1 row too many", "1 row is missing", "Nothing is wrong"]
    checks = [  # (rows, cols wanted, drawn rows, answer index into opts)
        (3, 4, [4, 4, 3], 0, "The last row has only 3 dots. It needs 4, so <b>1 dot is missing</b>."),
        (2, 5, [5, 5, 5], 2, "There are 3 rows, but %s wants 2 rows. There is <b>1 row too many</b>."),
        (4, 3, [3, 4, 3, 3], 1, "The second row has 4 dots. Every row needs 3, so there is <b>1 dot too many</b>."),
        (3, 5, [5, 5, 5], 4, "There are 3 rows with 5 dots in each row. <b>Nothing is wrong</b>. It is 5 + 5 + 5 = 15."),
    ]
    for r, c, drawn, ai, e in checks:
        nm, he, his = P.next()
        assert len(drawn) <= 5 and max(drawn) <= 5
        q = (fig(drawing_svg(drawn)) +
             "%s wants to draw %d rows of %d dots. What is wrong with %s drawing?" % (nm, r, c, his))
        if "%s" in e:
            e = e % nm
        others = [o for i, o in enumerate(opts) if i != ai]
        its.append(mcq(q, opts[ai], others, e))
    assert len(its) == 20, len(its)
    return {"title": "Array word problems", "items": its}


# ============================================================ balance (and build A-D pictures)
def balance(sets, rnd):
    """Spread the correct answers evenly over the 4 positions in every set."""
    for s in sets:
        targets = [0, 1, 2, 3] * 5
        rnd.shuffle(targets)
        for it, t in zip(s["items"], targets):
            if "_abcd" in it:
                prompt, right, wrong, kind = it.pop("_abcd")
                wrong = list(wrong)
                rnd.shuffle(wrong)
                panels = wrong[:t] + [right] + wrong[t:]
                it["q"] = fig(abcd_svg(panels, kind)) + prompt
                it["a"] = t
                it["e"] = it["e"].replace("{L}", "ABCD"[t])
                continue
            c = it["c"]
            right = c[it["a"]]
            wrong = [x for i, x in enumerate(c) if i != it["a"]]
            rnd.shuffle(wrong)
            it["c"] = wrong[:t] + [right] + wrong[t:]
            it["a"] = t


def mark_large(u, pattern):
    """Tag pictures that must print larger (A-D drawings) so the dots stay easy to count."""
    rx = re.compile(r"<svg (?=[^>]*aria-label='" + pattern + ")")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u


# ============================================================ lesson
def body_html():
    return (
        "<h2>What is an array?</h2>"
        "<p>An <b>array</b> is a set of objects in straight lines. "
        "<b>Rows</b> go across. <b>Columns</b> go up and down. "
        "Every row has the same number, and every column has the same number.</p>"
        "<figure class='sn-fig'>" + lesson_rc_svg() +
        "<figcaption>This array has 3 rows and 4 columns. Each row has 4 dots. Each column has 3 dots.</figcaption></figure>"
        "<h2>Add the rows</h2>"
        "<p>Count how many are in one row. Then add that number once for every row. "
        "This is called <b>repeated addition</b>, because you add the same number again and again.</p>"
        "<figure class='sn-fig'>" + lesson_sum_svg(3, 4, "rows") +
        "<figcaption>3 rows of 4: 4 + 4 + 4 = 12.</figcaption></figure>"
        + ex("Example", "An egg carton has 2 rows of 5 eggs. How many eggs?",
             "There are 2 rows, so add 5 two times: 5 + 5 = 10.", "10 eggs")
        + "<h2>Add the columns</h2>"
        "<p>You can also add the columns. The array does not change, so the total is the same.</p>"
        "<figure class='sn-fig'>" + lesson_sum_svg(3, 4, "columns") +
        "<figcaption>4 columns of 3: 3 + 3 + 3 + 3 = 12. Same dots, same total.</figcaption></figure>"
        + table(["Array", "Add the rows", "Add the columns"], [
            ["2 rows of 5", "5 + 5 = 10", "2 + 2 + 2 + 2 + 2 = 10"],
            ["3 rows of 4", "4 + 4 + 4 = 12", "3 + 3 + 3 + 3 = 12"],
            ["4 rows of 3", "3 + 3 + 3 + 3 = 12", "4 + 4 + 4 = 12"],
            ["5 rows of 5", "5 + 5 + 5 + 5 + 5 = 25", "5 + 5 + 5 + 5 + 5 = 25"],
        ])
        + "<p>In Grade 3, you will write 3 rows of 4 as 3 × 4. That is multiplication. "
        "Repeated addition is the first step.</p>"
        "<h2>Common mistakes</h2>"
        + table(["Mistake", "What to do instead"], [
            ["Adding the rows and the columns: 3 rows of 4 → 3 + 4 = 7", "Add 4 once for each row: 4 + 4 + 4 = 12"],
            ["Adding one row too many or too few: 4 + 4 + 4 + 4", "Count the rows first. 3 rows means 3 addends"],
            ["Mixing up rows and columns", "Rows go across, like a line of words. Columns go up and down"],
            ["Calling any group of dots an array", "Check that every row has the same number. One missing dot means it is not an array"],
        ])
    )


FAQ = [
    {"q": "What is an array in 2nd grade math?",
     "a": "An array is a set of objects in equal rows and equal columns, like eggs in a carton. In Grade 2, children add the rows or the columns to find the total (Common Core 2.OA.C.4)."},
    {"q": "How do you write a repeated addition equation for an array?",
     "a": "Count the objects in one row and add that number once for each row. 3 rows of 4 is 4 + 4 + 4 = 12."},
    {"q": "Do you get the same total if you add the columns?",
     "a": "Yes. 3 rows of 4 is 4 + 4 + 4 = 12, and its 4 columns of 3 are 3 + 3 + 3 + 3 = 12. The objects are the same, so the total is the same."},
    {"q": "How do arrays lead to multiplication?",
     "a": "Repeated addition of equal rows is what multiplication means. In Grade 3, 4 + 4 + 4 becomes 3 × 4 = 12, so arrays in Grade 2 build the idea first."},
]


def gen():
    rnd = random.Random(211)
    P = People(rnd)
    sets = [set_rows_cols(P), set_add_rows(P), set_add_cols(P), set_match(P), set_stories(P)]
    balance(sets, rnd)
    seen = set()
    for s in sets:
        assert len(s["items"]) == 20, (s["title"], len(s["items"]))
        assert sorted(it["a"] for it in s["items"]) == sorted([0, 1, 2, 3] * 5), s["title"]
        for it in s["items"]:
            assert len(set(it["c"])) == 4, it
            assert it["q"] not in seen, it["q"]
            assert "{" not in it["e"] and "_abcd" not in it
            seen.add(it["q"])
            # objects drawn in each array match its label
            m = re.search(r"aria-label='array of (\d+) rows? and (\d+) columns?", it["q"])
            if m:
                assert it["q"].count("fill='%s'" % GREEN) + it["q"].count("fill='%s'" % ORANGE) \
                    + it["q"].count("fill='%s'" % BLUE) == int(m.group(1)) * int(m.group(2)), it["q"]
    u = {
        "country": "us", "subject": "math", "grade": "grade-2", "slug": "arrays-repeated-addition", "sort": 11,
        "updated": UPDATED, "pdf_url": "",
        "title": "Arrays and Repeated Addition",
        "seo_title": "Grade 2 Arrays and Repeated Addition Worksheets: Rows, Columns and Equal Addends",
        "short_title": "Arrays and repeated addition",
        "domain": "Operations and Algebraic Thinking",
        "standard_code": "2.OA.C.4",
        "standard_url": "https://www.thecorestandards.org/Math/Content/2/OA/C/4/",
        "standard_text": "Use addition to find the total number of objects arranged in rectangular arrays with up to 5 rows and up to 5 columns; write an equation to express the total as a sum of equal addends.",
        "meta_desc": "Free Grade 2 arrays worksheets: count rows and columns, add the rows or the columns with repeated addition, match arrays to equations, and solve array word problems. 100 practice questions with simple answers.",
        "key_big": "Add the same number once for every row.",
        "key_sub": "Rows go across and columns go up and down. 3 rows of 4 is 4 + 4 + 4 = 12. Adding the columns, 3 + 3 + 3 + 3, gives the same total.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }
    return mark_large(u, "four drawings labeled A to D")


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
