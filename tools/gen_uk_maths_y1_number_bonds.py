# -*- coding: utf-8 -*-
"""
UK Year 1 Maths: Number bonds to 10 and 20 (National Curriculum in England)
  python3 tools/gen_uk_maths_y1_number_bonds.py
Five frames, ten frames and part-whole models. Bonds to 5, 10 and 20 and the related subtraction facts.
Every answer and every wrong answer is computed and checked in code.
HTML attributes use single quotes (no backslashes in the JSON).
"""
import json, os, random, re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "uk", "maths", "year-1")
UPDATED = "2026-11-02"
GREEN = "#006633"
FILL = "#cfe6d6"
RED = "#c0392b"
BLUE = "#1f5fa8"
INK = "#2b2b2b"
EGG = "#f3e3c3"
FONT = "Arial, Helvetica, sans-serif"
M = "−"   # real minus sign
GIRLS = ["Amelia", "Isla", "Freya", "Poppy", "Ava", "Aisha", "Lily", "Zara", "Grace", "Ruby", "Maya", "Evie"]
BOYS = ["Oliver", "Harry", "Mohammed", "Jack", "Arjun", "Noah", "George", "Leo", "Alfie", "Kai", "Ethan", "Charlie"]


# ------------------------------------------------------------ helpers
def mcq(q, correct, cands, e):
    """4 choices: correct + the first 3 unique distractors (no 0 or negatives). Positions are set by balance()."""
    correct = str(correct)
    seen = {correct}
    pick = []
    for c in cands:
        c = str(c)
        if c in seen or not c or c.startswith("-") or c.startswith(M) or re.match(r"^0\b", c):
            continue
        seen.add(c)
        pick.append(c)
        if len(pick) == 3:
            break
    assert len(pick) == 3, (q, correct, cands)
    return {"q": q, "c": [correct] + pick, "a": 0, "e": e}


def balance(sets, rnd):
    """Spread the correct answers evenly over the 4 positions in every set."""
    for s in sets:
        targets = [0, 1, 2, 3] * 5
        rnd.shuffle(targets)
        for it, t in zip(s["items"], targets):
            c = it["c"]
            right = c[it["a"]]
            wrong = [x for i, x in enumerate(c) if i != it["a"]]
            rnd.shuffle(wrong)
            it["c"] = wrong[:t] + [right] + wrong[t:]
            it["a"] = t


class People:
    def __init__(self, rnd):
        self.pool = [(x, "she", "her") for x in GIRLS] + [(x, "he", "his") for x in BOYS]
        rnd.shuffle(self.pool)
        self.i = 0

    def next(self):
        p = self.pool[self.i % len(self.pool)]
        self.i += 1
        return p


def cap(s):
    return s[0].upper() + s[1:]


def unit(n, one, many):
    return "%d %s" % (n, one if n == 1 else many)


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


def mark_large(u, pattern):
    """Tag wide pictures so they print larger."""
    rx = re.compile(r"<svg (?=[^>]*aria-label='(?:" + pattern + "))")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u


def add(a, b, w=None):
    return "%d + %d = %d" % (a, b, a + b if w is None else w)


def sub(a, b, w=None):
    return "%d %s %d = %d" % (a, M, b, a - b if w is None else w)


def is_true(eq):
    x, op, y, _, z = eq.split()
    x, y, z = int(x), int(y), int(z)
    return (x + y if op == "+" else x - y) == z


# ------------------------------------------------------------ pictures: five and ten frames
CELL = 30


def frame(x0, y0, cells, rows=2, kind="counter"):
    """A frame of 5 × rows boxes. cells: list of colours (counters) or 'egg' / 'x' (crossed-out egg)."""
    FW, FH = 5 * CELL, rows * CELL
    assert len(cells) <= 5 * rows
    bg = EGG if kind == "egg" else "#fff"
    s = ["<rect x='%d' y='%d' width='%d' height='%d' fill='#fff' stroke='%s' stroke-width='3'/>" % (x0, y0, FW, FH, INK)]
    for i in range(1, 5):
        s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='2'/>"
                 % (x0 + i * CELL, y0, x0 + i * CELL, y0 + FH, INK))
    for r in range(1, rows):
        s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='2'/>"
                 % (x0, y0 + r * CELL, x0 + FW, y0 + r * CELL, INK))
    for k, col in enumerate(cells):
        r, c = divmod(k, 5)
        cx, cy = x0 + c * CELL + CELL // 2, y0 + r * CELL + CELL // 2
        if kind == "egg":
            s.append("<ellipse class='o' cx='%d' cy='%d' rx='9' ry='11' fill='%s' stroke='%s' stroke-width='1.5'%s/>"
                     % (cx, cy, bg, INK, " opacity='0.45'" if col == "x" else ""))
            if col == "x":
                s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='3'/>"
                         "<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='3'/>"
                         % (cx - 11, cy - 11, cx + 11, cy + 11, INK, cx + 11, cy - 11, cx - 11, cy + 11, INK))
        else:
            s.append("<circle class='o' cx='%d' cy='%d' r='10' fill='%s'/>" % (cx, cy, col))
    return "".join(s)


def five_frame_svg(r, g=0):
    o = 6
    lab = "five frame with %d red%s counters" % (r, " and %d green" % g if g else "")
    return svg_wrap(5 * CELL + 2 * o, CELL + 2 * o, frame(o, o, [RED] * r + [GREEN] * g, rows=1), lab)


def ten_frame_svg(r, g=0):
    o = 6
    lab = "ten frame with %d red%s counters" % (r, " and %d green" % g if g else "")
    return svg_wrap(5 * CELL + 2 * o, 2 * CELL + 2 * o, frame(o, o, [RED] * r + [GREEN] * g), lab)


def two_frames_svg(n):
    """Two ten frames side by side, n red counters (first frame filled first)."""
    o, gap = 6, 14
    a, b = min(n, 10), max(n - 10, 0)
    body = frame(o, o, [RED] * a) + frame(o + 5 * CELL + gap, o, [RED] * b)
    return svg_wrap(10 * CELL + gap + 2 * o, 2 * CELL + 2 * o, body, "two ten frames with %d red counters" % n)


def egg_box_svg(n, crossed=0):
    o = 6
    cells = ["egg"] * (n - crossed) + ["x"] * crossed
    lab = "egg box with %d eggs" % n + (", %d crossed out" % crossed if crossed else "")
    return svg_wrap(5 * CELL + 2 * o, 2 * CELL + 2 * o, frame(o, o, cells, kind="egg"), lab)


def pw_svg(whole, a, b):
    """Part-whole model: the whole on top, two parts below. Values may be '?'."""
    W, H, r = 176, 136, 26
    top, left, right = (88, 32), (34, 104), (142, 104)
    s = []
    for p in (left, right):
        s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='3'/>" % (top[0], top[1], p[0], p[1], INK))
    for (cx, cy), v, fill in [(top, whole, FILL), (left, a, "#fff"), (right, b, "#fff")]:
        s.append("<circle cx='%d' cy='%d' r='%d' fill='%s' stroke='%s' stroke-width='3'/>" % (cx, cy, r, fill, GREEN))
        s.append(text(cx, cy + 7, str(v), 20, col=RED if v == "?" else INK))
    return svg_wrap(W, H, "".join(s), "part-whole model: whole %s, parts %s and %s" % (whole, a, b))


# ------------------------------------------------------------ explanations
def more_e(have, whole, frames):
    k = whole - have
    return ("%s %d boxes. %d %s full, so <b>%d</b> %s empty. %d + %d = %d." % (
        frames, whole, have, "is" if have == 1 else "are", k, "is" if k == 1 else "are", have, k, whole))


def bond_wrong(r, g):
    """Wrong number sentences for a frame with r red and g green: other bonds (not the turn-around) and miscounts."""
    w = r + g
    out = []
    for x, y in [(r + 1, g - 1), (r - 1, g + 1), (r, g - 1), (r + 1, g), (r - 1, g)]:
        if x > 0 and y > 0 and (x, y) not in [(r, g), (g, r)]:
            out.append("%d + %d = %d" % (x, y, x + y))
    return out


# ============================================================ set 1: bonds to 5 and 10 with frames
def set_frames():
    its = []
    for n in [4, 2, 3, 1]:
        k = 5 - n
        q = fig(five_frame_svg(n)) + "How many more counters make 5?"
        its.append(mcq(q, k, [k + 1, k - 1, n, 5], more_e(n, 5, "A five frame has")))
    for r, g in [(3, 2), (1, 4)]:
        q = fig(five_frame_svg(r, g)) + "Which number bond to 5 does it show?"
        e = "Count the red: %d. Count the green: %d. So <b>%s</b>." % (r, g, add(r, g))
        its.append(mcq(q, add(r, g), bond_wrong(r, g), e))
    for n in [8, 6, 9, 3, 7, 1, 4, 2]:
        k = 10 - n
        q = fig(ten_frame_svg(n)) + "How many more counters make 10?"
        its.append(mcq(q, k, [k + 1, k - 1, n, 10], more_e(n, 10, "A ten frame has")))
    for r, g in [(7, 3), (4, 6), (2, 8), (5, 5)]:
        q = fig(ten_frame_svg(r, g)) + "Which number bond to 10 does it show?"
        e = "Count the red: %d. Count the green: %d. So <b>%s</b>." % (r, g, add(r, g))
        its.append(mcq(q, add(r, g), bond_wrong(r, g), e))
    its.append(mcq(fig(ten_frame_svg(5)) + "10 = 5 + <b>?</b>", 5, [4, 6, 15, 10],
                   "5 boxes are full and 5 are empty. 10 = 5 + <b>5</b>."))
    its.append(mcq("Which is a number bond to 10?", "6 + 4", ["6 + 3", "5 + 4", "7 + 4"],
                   "6 + 4 = 10, so <b>6 + 4</b> is a number bond to 10. 6 + 3 = 9, 5 + 4 = 9 and 7 + 4 = 11."))
    assert len(its) == 20, len(its)
    return {"title": "Number bonds to 5 and 10 with frames", "items": its}


# ============================================================ set 2: number bonds to 10
def set_pairs():
    its = []
    for i, a in enumerate([3, 7, 1, 6, 4, 8, 2, 9]):
        k = 10 - a
        q = fig(pw_svg(10, a, "?") if i % 2 == 0 else pw_svg(10, "?", a)) + "What is the missing part?"
        e = "The whole is 10. One part is %d. %d + <b>%d</b> = 10. So the missing part is <b>%d</b>." % (a, a, k, k)
        its.append(mcq(q, k, [k + 1, k - 1, a, 10 + a], e))
    for qt, a in [("%d + <b>?</b> = 10", 8), ("<b>?</b> + %d = 10", 4), ("10 = %d + <b>?</b>", 7), ("10 = <b>?</b> + %d", 1)]:
        k = 10 - a
        q = fig(ten_frame_svg(a)) + qt % a
        e = "%s. %s empty. %d + %d = 10, so the missing number is <b>%d</b>." % (
            unit(a, "counter", "counters"), "1 box is" if k == 1 else "%d boxes are" % k, a, k, k)
        its.append(mcq(q, k, [k + 1, k - 1, 10 + a, a], e))
    for a in [3, 6, 1, 8, 4, 2]:
        k = 10 - a
        right = "%d and %d" % (a, k)
        wrong = []
        for x, y in [(a, k + 1), (a, k - 1), (a + 1, k), (a - 1, k)]:
            if x > 0 and y > 0:
                assert x + y != 10
                wrong.append("%d and %d" % (x, y))
        e = "%d + %d = 10, so <b>%s</b> make 10. The others make 9 or 11." % (a, k, right)
        its.append(mcq("Which two numbers make 10?", right, wrong, e))
    for right, wrong in [("4 + 5", ["3 + 7", "9 + 1", "2 + 8"]), ("3 + 8", ["6 + 4", "5 + 5", "1 + 9"])]:
        x, y = map(int, right.split(" + "))
        assert x + y != 10 and all(sum(map(int, w.split(" + "))) == 10 for w in wrong)
        e = "%s = %d, not 10. So <b>%s</b> is not a number bond to 10. The others all make 10." % (right, x + y, right)
        its.append(mcq("Which is <b>not</b> a number bond to 10?", right, wrong, e))
    assert len(its) == 20, len(its)
    return {"title": "Number bonds to 10", "items": its}


# ============================================================ set 3: number bonds to 20
def set_twenty():
    its = []
    for t in [13, 16, 11, 18, 14, 17]:
        k = 20 - t
        q = fig(two_frames_svg(t)) + "How many more counters make 20?"
        e = ("Two ten frames hold 20. %d boxes are full. The second frame has %d empty boxes, so <b>%d</b> more. "
             "%d + %d = 20, just like %d + %d = 10." % (t, k, k, t, k, t - 10, k))
        its.append(mcq(q, k, [k + 1, k - 1, t + 20, k + 10], e))
    for a, b in [(2, 8), (4, 6)]:
        q = "%s. So 1%d + %d = <b>?</b>" % (add(a, b), a, b)
        e = "1%d is 10 and %d. %d + %d = 10. So 1%d + %d = 10 + 10 = <b>20</b>." % (a, a, a, b, a, b)
        its.append(mcq(q, 20, [10, 19, 21, 30], e))
    for a, b in [(6, 4), (3, 7)]:
        q = "%s. So 1%d + <b>?</b> = 20" % (add(a, b), a)
        e = "%d + %d = 10, so 1%d + <b>%d</b> = 20. The ten stays the same." % (a, b, a, b)
        its.append(mcq(q, b, [b + 10, b - 1, b + 1, 20 + 10 + a], e))
    for qt, a in [("20 = %d + <b>?</b>", 15), ("<b>?</b> + %d = 20", 12), ("%d + <b>?</b> = 20", 19), ("20 = <b>?</b> + %d", 11)]:
        k = 20 - a
        q = fig(two_frames_svg(a)) + qt % a
        e = "%d counters. %s empty. %d + %d = 20, so the missing number is <b>%d</b>." % (
            a, "1 box is" if k == 1 else "%d boxes are" % k, a, k, k)
        its.append(mcq(q, k, [k + 1, k - 1, a + 20, k + 10], e))
    for a in [14, 17, 11]:
        k = 20 - a
        right = "%d and %d" % (a, k)
        wrong = ["%d and %d" % (a, 10 + k), "%d and %d" % (a, k + 1), "%d and %d" % (a + 1, k)]
        for w in wrong:
            assert sum(map(int, w.split(" and "))) != 20
        e = ("%d + %d = 10, so %d + %d = 20. <b>%s</b> make 20. %d and %d make 30, not 20."
             % (a - 10, k, a, k, right, a, 10 + k))
        its.append(mcq("Which two numbers make 20?", right, wrong, e))
    its.append(mcq(fig(two_frames_svg(10)) + "20 is 2 tens. 10 + <b>?</b> = 20", 10, [20, 9, 11, 2],
                   "One ten frame is full. One more full ten frame makes 20. 10 + <b>10</b> = 20."))
    for a, right, wrong in [(17, add(7, 3), [add(1, 9), add(7, 4), add(7, 2)]),
                            (12, add(2, 8), [add(1, 9), add(2, 7), add(2, 9)])]:
        k = 20 - a
        assert is_true(right)
        q = "Which number bond to 10 helps you find %d + <b>?</b> = 20?" % a
        e = "Look at the ones in %d: %d. <b>%s</b>, so %d + %d = 20." % (a, a - 10, right, a, k)
        its.append(mcq(q, right, wrong, e))
    assert len(its) == 20, len(its)
    return {"title": "Number bonds to 20", "items": its}


# ============================================================ set 4: related subtraction facts
def set_subtraction():
    its = []
    for a, b in [(6, 4), (7, 3), (2, 8), (13, 7), (15, 5), (11, 9)]:
        w = a + b
        q = "%s. So %d %s %d = <b>?</b>" % (add(a, b), w, M, b)
        e = "The parts are %d and %d. The whole is %d. Take away the part %d, and the other part is left: %d %s %d = <b>%d</b>." % (
            a, b, w, b, w, M, b, a)
        its.append(mcq(q, a, [a - 1, a + 1, w + b, b], e))
    for w, a, b in [(10, 7, 3), (10, 2, 8), (10, 6, 4), (20, 14, 6), (20, 9, 11), (20, 17, 3)]:
        assert a + b == w and a != b
        q = fig(pw_svg(w, a, b)) + "Which subtraction fact does it show?"
        right = sub(w, a)
        big, small = max(a, b), min(a, b)
        wrong = [sub(big, small), sub(w, a, b + 1), add(a, b)]
        e = ("Start with the whole, %d. Take away one part, %d. The other part, %d, is left: <b>%s</b>. "
             "%s uses only the parts." % (w, a, b, right, sub(big, small)))
        its.append(mcq(q, right, wrong, e))
    for w, a in [(10, 3), (10, 9), (20, 4), (20, 15)]:
        b = w - a
        q = fig(pw_svg(w, a, "?")) + "%d %s %d = <b>?</b>" % (w, M, a)
        e = "The whole is %d. One part is %d. %d + %d = %d, so %d %s %d = <b>%d</b>." % (w, a, a, b, w, w, M, a, b)
        its.append(mcq(q, b, [b + 1, b - 1, w + a, a], e))
    for a, b in [(8, 2), (9, 1), (16, 4), (12, 8)]:
        w = a + b
        right = sub(w, b)
        big, small = max(a, b), min(a, b)
        wrong = [sub(big, small), add(w, b), sub(w, b, a + 1)]
        q = "Which fact goes with %s?" % add(a, b)
        e = ("%s uses %d, %d and %d. <b>%s</b> uses the same three numbers. %s is true, but it uses %d."
             % (add(a, b), a, b, w, right, sub(big, small), big - small))
        its.append(mcq(q, right, wrong, e))
    for it in its:
        r = it["c"][it["a"]]
        if re.match(r"^\d+ [+−] \d+ = \d+$", r):
            assert is_true(r), r
    assert len(its) == 20, len(its)
    return {"title": "Related subtraction facts", "items": its}


# ============================================================ set 5: word problems
NOUNS = {"sweets": ("sweet", "sweets"), "pencils": ("pencil", "pencils"), "cubes": ("cube", "cubes"),
         "eggs": ("egg", "eggs"), "biscuits": ("biscuit", "biscuits"), "stickers": ("sticker", "stickers"),
         "children": ("child", "children"), "grapes": ("grape", "grapes"), "pupils": ("pupil", "pupils"),
         "marbles": ("marble", "marbles"), "cakes": ("cake", "cakes"), "pages": ("page", "pages"),
         "conkers": ("conker", "conkers"), "ducks": ("duck", "ducks"), "raisins": ("raisin", "raisins"),
         "p": None}


def set_stories(P):
    its = []

    def story(tpl, ans, cands, e, kind, pic=""):
        nm, he, his = P.next()
        m = P.next()[0] if "{M}" in tpl else ""
        f = dict(N=nm, M=m, he=he, He=cap(he), his=his)
        q = pic + tpl.format(**f)
        if kind == "p":
            u = lambda n: "%dp" % n
        else:
            one, many = NOUNS[kind]
            u = lambda n: unit(n, one, many)
        its.append(mcq(q, u(ans), [u(c) for c in cands if c > 0], e.format(**f)))

    story("A bag has 10 sweets. {N} eats 3. How many sweets are left?", 7, [6, 8, 13, 3],
          "10 %s 3 = <b>7</b>. Check: 3 + 7 = 10. 7 sweets are left." % M, "sweets")
    story("A pot holds 10 pencils. It has 6 pencils in it. How many more pencils fit?", 4, [3, 5, 16, 6],
          "6 + <b>4</b> = 10. So 4 more pencils fit.", "pencils")
    story("{N} has 4 red cubes and 6 blue cubes. How many cubes does {he} have?", 10, [9, 11, 2, 12],
          "4 + 6 = <b>10</b>. 4 and 6 are a number bond to 10.", "cubes")
    story("A box holds 10 eggs. How many more eggs fill the box?", 3, [2, 4, 7, 17],
          "There are 7 eggs. 7 + <b>3</b> = 10. So 3 more eggs fill the box.", "eggs", fig(egg_box_svg(7)))
    story("There are 10 biscuits on a plate. The class eats 8. How many biscuits are left?", 2, [1, 3, 18, 8],
          "10 %s 8 = <b>2</b>. Check: 8 + 2 = 10." % M, "biscuits")
    story("{N} needs 10 stickers. {He} has 5. How many more stickers does {he} need?", 5, [4, 6, 15, 10],
          "5 + <b>5</b> = 10. {N} needs 5 more stickers.", "stickers")
    story("10 children play football. 7 have red shirts. The rest have blue shirts. How many have blue shirts?",
          3, [2, 4, 17, 7], "7 + <b>3</b> = 10. So 3 children have blue shirts.", "children")
    story("{N} had 10 grapes. Now {he} has 1. How many grapes did {he} eat?", 9, [8, 10, 11, 1],
          "1 + <b>9</b> = 10, so 10 %s 1 = 9. {N} ate 9 grapes." % M, "grapes")
    story("A box has 10 eggs. {N} uses 4 for a cake. How many eggs are left?", 6, [5, 7, 14, 4],
          "10 %s 4 = <b>6</b>. Check: 4 + 6 = 10. 6 eggs are left." % M, "eggs", fig(egg_box_svg(10, 4)))
    story("There are 10 ducks on a pond. 5 swim away. How many ducks are left?", 5, [4, 6, 15, 10],
          "10 %s 5 = <b>5</b>. 5 + 5 = 10." % M, "ducks")
    story("{N} has 13 marbles. {He} wants 20. How many more marbles does {he} need?", 7, [6, 8, 33, 17],
          "13 + <b>7</b> = 20, because 3 + 7 = 10. {N} needs 7 more marbles.", "marbles")
    story("A tray holds 20 cakes. There are 15 cakes on it. How many more cakes fit?", 5, [4, 6, 35, 15],
          "15 + <b>5</b> = 20, because 5 + 5 = 10. So 5 more cakes fit.", "cakes")
    story("{N} has 20p. {He} spends 6p. How much money is left?", 14, [13, 15, 26, 6],
          "20 %s 6 = <b>14</b>. Check: 14 + 6 = 20. {N} has 14p left." % M, "p")
    story("There are 17 children on a bus. 3 more get on. How many children are on the bus now?", 20, [19, 21, 14, 10],
          "17 + 3 = <b>20</b>, because 7 + 3 = 10.", "children")
    story("A book has 20 pages. {N} has read 11 pages. How many pages are left?", 9, [8, 10, 31, 11],
          "11 + <b>9</b> = 20, because 1 + 9 = 10. So 9 pages are left.", "pages")
    story("{N} has 10 conkers. {M} has 4 conkers. How many more conkers does {N} have?", 6, [5, 7, 14, 4],
          "4 + <b>6</b> = 10, so 10 %s 4 = 6. {N} has 6 more conkers." % M, "conkers")
    story("There are 20 pupils in a class. 14 pupils have a packed lunch. The rest have school dinners. "
          "How many pupils have school dinners?", 6, [5, 7, 34, 14],
          "14 + <b>6</b> = 20, because 4 + 6 = 10. So 6 pupils have school dinners.", "pupils")
    story("{N} knows 7 + 3 = 10. {He} has 10 raisins and eats 3. How many raisins are left?", 7, [6, 8, 13, 3],
          "7 + 3 = 10, so 10 %s 3 = <b>7</b>. 7 raisins are left." % M, "raisins")
    nm, he, _ = P.next()
    its.append(mcq("%s has 10 sweets. %s gives some away. Now %s has 6. Which fact finds how many %s gave away?"
                   % (nm, cap(he), he, he),
                   "6 + <b>?</b> = 10", ["10 + 6 = <b>?</b>", "6 %s 10 = <b>?</b>" % M, "10 + <b>?</b> = 6"],
                   "6 and the sweets given away make 10. 6 + 4 = 10, so %s gave away 4 sweets." % he))
    story("There are 20 pupils. 12 are in the hall. The rest are in the classroom. How many pupils are in the classroom?",
          8, [7, 9, 32, 12], "12 + <b>8</b> = 20, because 2 + 8 = 10. So 8 pupils are in the classroom.", "pupils")
    assert len(its) == 20, len(its)
    return {"title": "Word problems with number bonds", "items": its}


# ============================================================ lesson
def body_html():
    return (
        "<h2>What is a number bond?</h2>"
        "<p>A number bond is two parts that make a whole. 7 and 3 make 10. So 7 + 3 = 10 is a number bond to 10.</p>"
        "<figure class='sn-fig'>" + pw_svg(10, 7, 3) +
        "<figcaption>A part-whole model. The whole is 10. The parts are 7 and 3.</figcaption></figure>"
        "<h2>Number bonds to 10 on a ten frame</h2>"
        "<p>A ten frame has 10 boxes. Count the counters. The empty boxes show how many more make 10.</p>"
        "<figure class='sn-fig'>" + ten_frame_svg(7) +
        "<figcaption>7 boxes are full. 3 boxes are empty. 7 + 3 = 10.</figcaption></figure>"
        + table(["Number bond to 10", "Turned around"], [["0 + 10", "10 + 0"], ["1 + 9", "9 + 1"], ["2 + 8", "8 + 2"],
                                            ["3 + 7", "7 + 3"], ["4 + 6", "6 + 4"], ["5 + 5", ""]])
        + "<h2>Number bonds to 20</h2>"
        "<p>20 is 2 tens. Use a bond to 10 to find a bond to 20.</p>"
        "<figure class='sn-fig'>" + two_frames_svg(13) +
        "<figcaption>13 counters. 7 boxes are empty. 3 + 7 = 10, so 13 + 7 = 20.</figcaption></figure>"
        + ex("Example", "16 + ? = 20", "Look at the ones: 6. 6 + 4 = 10. So 16 + 4 = 20.", "4")
        + "<h2>Related subtraction facts</h2>"
        "<p>If you know the parts, you can take one away. The other part is left.</p>"
        + ex("Example", "6 + 4 = 10. So 10 − 4 = ?", "The whole is 10. Take away the part 4. The part 6 is left.", "6")
        + "<h2>Common mistakes</h2>"
        + table(["Mistake", "What to do instead"], [
            ["7 counters: “7, 8, 9, 10”, so 4 more", "Count only the empty boxes: 3"],
            ["10 − 4 = 5 or 14", "Think: 4 + 6 = 10, so 10 − 4 = 6"],
            ["13 + ? = 20: writing 33", "You need the missing part, not 13 + 20. 13 + 7 = 20"],
            ["13 + ? = 20: writing 6", "3 + 7 = 10, so the missing part is 7"],
            ["6 − 4 = 2 for the model 10, 6, 4", "Start with the whole: 10 − 6 = 4"],
        ])
    )


FAQ = [
    {"q": "What are number bonds in Year 1?",
     "a": "Number bonds are pairs of numbers that make a whole, such as 7 and 3 making 10. The National Curriculum says Year 1 children should know number bonds and the related subtraction facts within 20."},
    {"q": "What are the number bonds to 10?",
     "a": "They are 0 + 10, 1 + 9, 2 + 8, 3 + 7, 4 + 6 and 5 + 5, and the same pairs the other way round, such as 9 + 1."},
    {"q": "How can I help my child learn number bonds to 10?",
     "a": "Use 10 small objects or a ten frame. Hide some and ask how many are hidden, or ask “I have 6, how many more make 10?” A few minutes each day helps the facts stick."},
    {"q": "What is a part-whole model?",
     "a": "A part-whole model shows a whole number at the top and its two parts below. For 10, 6 and 4 it shows that 6 + 4 = 10, 10 − 4 = 6 and 10 − 6 = 4."},
]


def check(sets):
    seen = set()
    for s in sets:
        assert len(s["items"]) == 20, (s["title"], len(s["items"]))
        assert sorted(it["a"] for it in s["items"]) == sorted([0, 1, 2, 3] * 5)
        for it in s["items"]:
            assert len(set(it["c"])) == 4, it
            k = it["q"] + "|" + "|".join(sorted(it["c"]))
            assert k not in seen, it["q"]
            seen.add(k)
            q, right = it["q"], it["c"][it["a"]]
            assert len(re.findall(r"<svg", q)) <= 1, q
            # counters / eggs drawn match the label
            m = re.search(r"aria-label='(five|ten) frame with (\d+) red(?: and (\d+) green)? counters'", q)
            if m:
                n = int(m.group(2)) + int(m.group(3) or 0)
                assert q.count("class='o'") == n, q
                if "How many more" in q:
                    assert int(right) == (5 if m.group(1) == "five" else 10) - n
                if "does it show" in q:
                    assert right == add(int(m.group(2)), int(m.group(3)))
            m = re.search(r"aria-label='two ten frames with (\d+) red counters'", q)
            if m:
                assert q.count("class='o'") == int(m.group(1)), q
                if "How many more" in q:
                    assert int(right) == 20 - int(m.group(1))
            m = re.search(r"aria-label='egg box with (\d+) eggs", q)
            if m:
                assert q.count("class='o'") == int(m.group(1))
            # part-whole model: missing part / subtraction fact
            m = re.search(r"aria-label='part-whole model: whole (\d+), parts (\S+) and (\S+)'", q)
            if m:
                w = int(m.group(1))
                parts = [m.group(2), m.group(3)]
                known = [int(p) for p in parts if p != "?"]
                if "?" in parts:
                    assert int(right) == w - known[0]
                else:
                    assert is_true(right) and right.startswith("%d %s" % (w, M))
            # bare equations with one '?'
            pl = re.sub(r"<[^>]+>", "", q.split("</div>")[-1])
            m = re.search(r"(?:^|So )(\?|\d+) ([+−]) (\?|\d+) = (\?|\d+)$", pl)
            if m and right.isdigit():
                x, op, y, z = m.group(1), m.group(2), m.group(3), m.group(4)
                v = int(right)
                x, y, z = [v if t == "?" else int(t) for t in (x, y, z)]
                assert (x + y if op == "+" else x - y) == z, (pl, right)
            m = re.search(r"^10 = (\?|\d+) \+ (\?|\d+)$|^20 = (\?|\d+) \+ (\?|\d+)$", pl)
            if m and right.isdigit():
                g = [t for t in m.groups() if t is not None]
                w = 10 if pl.startswith("10") else 20
                assert sum(int(right) if t == "?" else int(t) for t in g) == w, pl
            # any equation given as the answer is true; wrong equations in "Which number bond" are false or not shown
            if re.match(r"^\d+ [+−] \d+ = \d+$", right):
                assert is_true(right), right
            if q.endswith("Which two numbers make 10?") or q.endswith("Which two numbers make 20?"):
                tot = int(q[-3:-1])
                for c in it["c"]:
                    assert (sum(map(int, c.split(" and "))) == tot) == (c == right), c
            for c in it["c"]:
                assert "  " not in c


def gen():
    rnd = random.Random(1102)
    P = People(rnd)
    sets = [set_frames(), set_pairs(), set_twenty(), set_subtraction(), set_stories(P)]
    balance(sets, rnd)
    check(sets)
    u = {
        "country": "uk", "subject": "maths", "grade": "year-1", "slug": "number-bonds-to-10-and-20", "sort": 2,
        "updated": UPDATED, "pdf_url": "",
        "title": "Number Bonds to 10 and 20",
        "seo_title": "Year 1 Number Bonds to 10 and 20 Worksheets: Ten Frames, Part-Whole Models and Subtraction Facts",
        "short_title": "Number bonds to 10 and 20",
        "domain": "Addition and subtraction",
        "standard_code": "Year 1: Addition and subtraction",
        "standard_url": "https://www.gov.uk/government/publications/national-curriculum-in-england-mathematics-programmes-of-study",
        "standard_text": "Represent and use number bonds and related subtraction facts within 20.",
        "meta_desc": "Free Year 1 maths worksheets on number bonds to 10 and 20: ten frames, part-whole models, related subtraction facts and simple word problems. 100 picture-based questions with an answer key, matched to the National Curriculum.",
        "key_big": "Two parts make a whole: 7 + 3 = 10, so 17 + 3 = 20.",
        "key_sub": "Count the empty boxes on a ten frame to find how many more make 10. If 6 + 4 = 10, then 10 − 4 = 6 and 10 − 6 = 4.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }
    return mark_large(u, "two ten frames")


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
