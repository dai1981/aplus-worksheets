# -*- coding: utf-8 -*-
"""
AU Year 5 Maths: Factors and multiples (Australian Curriculum v9.0, AC9M5N02)
  python3 tools/gen_au_maths_y5_factors.py
Factor pairs and all factors, writing a number as a product of factors (factor trees), multiples,
divisibility rules for 2, 3, 5, 9 and 10, and word problems. Prime and composite numbers are Year 6 in v9,
so they get only a light mention in the lesson.
Every factor, multiple, product and divisibility fact is checked in code.
Wrong answers come from real mistakes: confusing factors and multiples, a missing factor pair, forgetting 1
(and the number itself), using the digit-sum rule for 4, looking at the first digit instead of the last,
adding instead of multiplying, a digit in the number "making" it a multiple.
HTML attributes use single quotes (no backslashes in the JSON).
"""
import json, os, random, re
from math import prod

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "au", "maths", "year-5")
UPDATED = "2026-11-02"
GREEN = "#006633"
FILL = "#cfe6d6"
RED = "#c0392b"
INK = "#2b2b2b"
GREY = "#8a8a8a"
FONT = "Arial, Helvetica, sans-serif"
GIRLS = ["Charlotte", "Isla", "Mia", "Amelia", "Ava", "Harper", "Chloe", "Ruby", "Mei", "Zara", "Matilda", "Sienna"]
BOYS = ["Oliver", "Jack", "Noah", "William", "Leo", "Lachlan", "Liam", "Aarav", "Kai", "Cooper", "Ethan"]


# ------------------------------------------------------------ maths
def factors(x):
    return [d for d in range(1, x + 1) if x % d == 0]


def pairs(x):
    return [(d, x // d) for d in factors(x) if d * d <= x]


def dsum(x):
    return sum(int(c) for c in str(x))


def lst(xs):
    return ", ".join(str(x) for x in xs)


def times(xs):
    return " × ".join(str(x) for x in xs)


def pair_txt(x):
    return ", ".join("%d × %d" % p for p in pairs(x))


# ------------------------------------------------------------ helpers
def mcq(q, correct, cands, e):
    """4 choices: correct + the first 3 unique distractors. Positions are set later by balance()."""
    correct = str(correct)
    seen = {correct}
    pick = []
    for c in cands:
        c = str(c)
        if c in seen or not c:
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
            wrong = [x for i, x in enumerate(c) if i != it["a"]]
            rnd.shuffle(wrong)
            right = c[it["a"]]
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


def fig(svg):
    return "<div class='qfig'>" + svg + "</div>"


def svg_wrap(w, h, body, label):
    return ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 %d %d' width='%d' height='%d' "
            "role='img' aria-label='%s'><g font-family='%s'>%s</g></svg>" % (w, h, w, h, label, FONT, body))


def text(x, y, t, fs=16, anchor="middle", col=INK, weight=700):
    return ("<text x='%.1f' y='%.1f' font-size='%d' font-weight='%d' fill='%s' text-anchor='%s'>%s</text>"
            % (x, y, fs, weight, col, anchor, t))


def table(head, rows):
    h = "".join("<th>%s</th>" % x for x in head)
    b = "".join("<tr>" + "".join("<td>%s</td>" % c for c in r) + "</tr>" for r in rows)
    return "<div class='sn-tw'><table class='sn-table'><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>" % (h, b)


def ex(title, q, s, a):
    return ("<div class='sn-ex'><span class='sn-ex-t'>%s</span><p class='sn-ex-q'>%s</p>"
            "<p class='sn-ex-s'>%s</p><p class='sn-ex-a'>Answer: %s</p></div>" % (title, q, s, a))


def mark_large(u, pattern):
    """Tag pictures that must print larger so every number stays readable."""
    rx = re.compile(r"<svg (?=[^>]*aria-label='(?:" + pattern + "))")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u


# ------------------------------------------------------------ pictures
def T(v, a=None, b=None):
    """Tree node: v splits into a and b (themselves nodes or ints)."""
    if a is None:
        return (v, None)
    a = a if isinstance(a, tuple) else (a, None)
    b = b if isinstance(b, tuple) else (b, None)
    assert a[0] * b[0] == v, (v, a[0], b[0])
    return (v, [a, b])


def leaves(t):
    return [t[0]] if t[1] is None else leaves(t[1][0]) + leaves(t[1][1])


def depth(t):
    return 1 if t[1] is None else 1 + max(depth(c) for c in t[1])


def tree_svg(t, hide=None, step=46, dy=50):
    """Factor tree: each number splits into a factor pair; the numbers at the ends of the branches are circled.
    'hide' is a value shown as ? (in a red box)."""
    assert prod(leaves(t)) == t[0]
    o = 22
    W = (len(leaves(t)) - 1) * step + 2 * o
    H = (depth(t) - 1) * dy + 2 * o
    pos = {}
    s = []
    cnt = [0]

    def place(node, lvl):
        if node[1] is None:
            px = o + cnt[0] * step
            cnt[0] += 1
        else:
            xs = [place(c, lvl + 1) for c in node[1]]
            px = sum(xs) / 2
        pos[id(node)] = (px, o + lvl * dy)
        return px

    place(t, 0)

    def draw(node):
        px, py = pos[id(node)]
        if node[1] is not None:
            for c in node[1]:
                cx, cy = pos[id(c)]
                s.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='2'/>"
                         % (px, py + 9, cx, cy - 15, GREY))
                draw(c)
        if node[0] == hide:
            s.append("<rect x='%.1f' y='%.1f' width='30' height='28' rx='4' fill='#fff' stroke='%s' stroke-width='2'/>"
                     % (px - 15, py - 14, RED))
            s.append(text(px, py + 6, "?", 18, col=RED))
            return
        if node[1] is None:
            s.append("<circle cx='%.1f' cy='%.1f' r='15' fill='%s' stroke='%s' stroke-width='2'/>" % (px, py, FILL, GREEN))
        s.append(text(px, py + 6, str(node[0]), 17))

    draw(t)
    lab = "factor tree for %d" % t[0] + (" with one number missing" if hide else "")
    return svg_wrap(W, H, "".join(s), lab)


def rainbow_svg(x, hide=None, step=40):
    """Factor rainbow: the factors of x in a row, each factor pair joined by an arc. 'hide' shows as ?."""
    fs = factors(x)
    ps = pairs(x)
    o = 20
    top = 16 + 14 * (len(ps) - 1) + 8
    W = (len(fs) - 1) * step + 2 * o
    xs = {f: o + i * step for i, f in enumerate(fs)}
    s = []
    for k, (a, b) in enumerate(ps):
        if a == b:
            continue
        ry = 16 + 14 * (len(ps) - 1 - k)
        s.append("<path d='M %d %d A %d %d 0 0 1 %d %d' fill='none' stroke='%s' stroke-width='2.5'/>"
                 % (xs[a], top, (xs[b] - xs[a]) // 2, ry, xs[b], top, GREEN))
    for f in fs:
        if f == hide:
            s.append("<rect x='%d' y='%d' width='28' height='26' rx='4' fill='#fff' stroke='%s' stroke-width='2'/>"
                     % (xs[f] - 14, top + 3, RED))
            s.append(text(xs[f], top + 22, "?", 18, col=RED))
        else:
            s.append(text(xs[f], top + 22, str(f), 18))
    lab = "factor rainbow for %d" % x + (" with one factor missing" if hide else "")
    return svg_wrap(W, top + 34, "".join(s), lab)


def array_svg(r, c, cell=18):
    """r rows of c dots."""
    o = 6
    W, H = c * cell + 2 * o, r * cell + 2 * o
    s = ["<circle cx='%.1f' cy='%.1f' r='6' fill='%s'/>" % (o + j * cell + cell / 2, o + i * cell + cell / 2, GREEN)
         for i in range(r) for j in range(c)]
    return svg_wrap(W, H, "".join(s), "array of dots in %d rows" % r)


def track_svg(top, shaded, cell=34):
    """Number track 1..top in one row; shaded squares filled."""
    o = 4
    W, H = top * cell + 2 * o, cell + 2 * o
    s = []
    for v in range(1, top + 1):
        x = o + (v - 1) * cell
        s.append("<rect x='%d' y='%d' width='%d' height='%d' fill='%s' stroke='%s' stroke-width='1.5'/>"
                 % (x, o, cell, cell, FILL if v in shaded else "#fff", GREEN))
        s.append(text(x + cell / 2, o + cell / 2 + 6, str(v), 15))
    return svg_wrap(W, H, "".join(s), "number track from 1 to %d" % top)


# ============================================================ set 1: factors and factor pairs
def set_factors(P):
    its = []
    for x, drop in [(12, (3, 4)), (20, (4, 5)), (18, (3, 6)), (30, (5, 6))]:
        fs = factors(x)
        assert x % drop[0] == 0 and drop[0] * drop[1] == x
        right = lst(fs)
        missing = lst([d for d in fs if d not in drop])
        multi = lst([x * k for k in range(1, 5)])
        no_ends = lst(fs[1:-1])
        e = ("Find the factor pairs: %s. So the factors are <b>%s</b>. Do not forget 1 and %d, and do not miss %d × %d. "
             "%s are multiples of %d, not factors." % (pair_txt(x), right, x, drop[0], drop[1], multi, x))
        its.append(mcq("Which list shows <b>all</b> the factors of %d?" % x, right, [missing, no_ends, multi], e))

    for r, c, other in [(3, 6, (2, 9)), (4, 7, (2, 14))]:
        x = r * c
        assert other[0] * other[1] == x
        its.append(mcq(fig(array_svg(r, c)) + "This array shows %d dots. Which factor pair of %d does it show?" % (x, x),
                       "%d × %d" % (r, c), ["%d + %d" % (r, c), "%d × %d" % other, "%d × %d" % (r, c + 1)],
                       "There are %d rows of %d dots: %d × %d = %d. So <b>%d × %d</b> is a factor pair of %d. "
                       "%d × %d is another pair, but it is not the one shown, and %d + %d = %d, not %d."
                       % (r, c, r, c, x, r, c, x, other[0], other[1], r, c, r + c, x)))

    assert 4 * 9 == 36 and 6 * 5 == 30 and 3 * 13 == 39 and 2 * 16 == 32
    its.append(mcq("Which of these is a factor pair of 36?", "4 × 9", ["6 × 5", "3 × 13", "2 × 16"],
                   "4 × 9 = <b>36</b>, so 4 and 9 are a factor pair. 6 × 5 = 30, 3 × 13 = 39 and 2 × 16 = 32. "
                   "The other pairs of 36 are 1 × 36, 2 × 18, 3 × 12 and 6 × 6."))

    for x, hide, partner, wrong in [(24, 8, 3, [21, 9, 7]), (30, 15, 2, [28, 60, 10])]:
        assert hide * partner == x and hide in factors(x)
        e = "The arc joins ? to %d, so %d × ? = %d. %d ÷ %d = <b>%d</b>. " % (partner, partner, x, x, partner, hide)
        if x == 24:
            assert 24 % 9 and 24 % 7
            e += "21 is 24 − 3, not 24 ÷ 3. 9 and 7 are not factors of 24."
        else:
            e += "28 is 30 − 2, 60 is 30 × 2, and 10 is already in the rainbow (it pairs with 3)."
        its.append(mcq(fig(rainbow_svg(x, hide)) + "The factor rainbow shows all the factors of %d. "
                       "Which number is missing?" % x, hide, wrong, e))

    for x, bad, good in [(32, 6, [4, 8, 16]), (45, 6, [3, 9, 15]), (56, 12, [7, 8, 14])]:
        assert x % bad and all(x % g == 0 for g in good)
        e = ("%d ÷ %d = %d remainder %d, so <b>%d</b> is not a factor of %d. %s"
             % (x, bad, x // bad, x % bad, bad, x, " ".join("%d × %d = %d." % (g, x // g, x) for g in good)))
        its.append(mcq("Which number is <b>not</b> a factor of %d?" % x, bad, good, e))

    for x, good, bad in [(42, 7, [84, 8, 12]), (54, 9, [108, 8, 12])]:
        assert x % good == 0 and all(x % b for b in bad) and bad[0] == 2 * x
        e = ("%d × %d = %d, so <b>%d</b> is a factor of %d. %d is a multiple of %d, not a factor, and %d and %d "
             "leave a remainder." % (good, x // good, x, good, x, bad[0], x, bad[1], bad[2]))
        its.append(mcq("Which number is a factor of %d?" % x, good, bad, e))

    assert len(factors(16)) == 5 and len(pairs(16)) == 3
    its.append(mcq("How many factors does 16 have?", 5, [6, 3, 4],
                   "The factor pairs are 1 × 16, 2 × 8 and 4 × 4. The factors are 1, 2, 4, 8, 16: <b>5</b> factors. "
                   "4 × 4 uses 4 only once, so do not count it twice (6). 3 is the number of pairs."))

    nm, he, his = P.next()
    shown = [(1, 48), (2, 24), (3, 16), (6, 8)]
    assert sorted(shown + [(4, 12)]) == pairs(48)
    its.append(mcq("%s lists the factor pairs of 48: %s. Which pair did %s miss?"
                   % (nm, ", ".join("%d × %d" % p for p in shown), he), "4 × 12", ["8 × 6", "5 × 10", "7 × 7"],
                   "Test 1, 2, 3, 4 … in order. 48 ÷ 4 = 12, so <b>4 × 12</b> is missing. 8 × 6 is the same pair as 6 × 8. "
                   "5 × 10 = 50 and 7 × 7 = 49, not 48."))

    nm, he, his = P.next()
    assert factors(15) == [1, 3, 5, 15]
    its.append(mcq("%s says the factors of 15 are 3 and 5. Which factors has %s left out?" % (nm, he), "1 and 15",
                   ["30 and 45", "2 and 7", "None. That is all of them"],
                   "1 × 15 = 15 is a factor pair too. The factors of 15 are 1, 3, 5 and 15, so %s left out <b>1 and 15</b>. "
                   "1 is a factor of every number, and every number is a factor of itself. 30 and 45 are multiples of 15."
                   % he))

    nm, he, his = P.next()
    assert 27 % 7 == 6
    its.append(mcq("%s says 7 is a factor of 27 because 27 has a 7 in it. Is %s right?" % (nm, he),
                   "No. 27 ÷ 7 = 3 r 6", ["Yes. 27 ends in 7", "Yes. 7 × 3 = 27", "No. 7 is a multiple of 27"],
                   "7 × 3 = 21 and 7 × 4 = 28, so 27 is not in the 7 times table. 27 ÷ 7 = 3 remainder 6, so 7 is "
                   "<b>not</b> a factor. The digits of a number do not tell you its factors."))

    assert factors(35) == [1, 5, 7, 35]
    its.append(mcq("What is the largest factor of 35 that is less than 35?", 7, [5, 34, 17],
                   "The factors of 35 are 1, 5, 7 and 35. The largest one below 35 is <b>7</b>. "
                   "34 is 35 − 1, and 35 ÷ 2 is not a whole number, so 17 is not a factor."))

    assert len(factors(24)) == 8 and len(pairs(24)) == 4
    its.append(mcq("How many factors does 24 have?", 8, [4, 6, 48],
                   "The factor pairs are 1 × 24, 2 × 12, 3 × 8 and 4 × 6. Each pair gives 2 factors: "
                   "1, 2, 3, 4, 6, 8, 12, 24. That is <b>8</b> factors. 4 is the number of pairs, 6 leaves out 1 and 24, "
                   "and 48 is a multiple of 24."))
    assert len(its) == 20, len(its)
    return {"title": "Factors and factor pairs", "items": its}


# ============================================================ set 2: writing a number as a product of factors
def set_products(P):
    its = []
    for x, right, wrong in [(24, (3, 8), [(20, 4, "+"), (2, 14), (4, 5)]),
                            (36, (4, 9), [(30, 6, "+"), (6, 7), (4, 8)])]:
        assert prod(right) == x
        ws = []
        exp = []
        for w in wrong:
            if len(w) == 3:
                ws.append("%d + %d" % w[:2])
                exp.append("%d + %d adds, so it is a sum, not a product" % w[:2])
            else:
                assert prod(w) != x
                ws.append(times(w))
                exp.append("%s = %d" % (times(w), prod(w)))
        e = ("A product is the answer to a multiplication. %s = %d, so <b>%s</b> shows %d as a product of two factors. %s."
             % (times(right), x, times(right), x, cap("; ".join(exp))))
        its.append(mcq("Which shows %d as a product of two factors?" % x, times(right), ws, e))

    assert 2 * 3 * 4 == 24 and 2 * 3 * 5 == 30
    its.append(mcq("Which shows 24 as a product of <b>three</b> factors?", "2 × 3 × 4",
                   ["2 × 3 × 5", "2 × 12", "2 + 10 + 12"],
                   "2 × 3 = 6 and 6 × 4 = <b>24</b>. 2 × 3 × 5 = 30, 2 × 12 has only two factors, and 2 + 10 + 12 is a sum."))

    for a, b, ans, wrong, ex_txt in [
            (30, (2, 3, None), 5, [15, 10, 25],
             "15 is 30 ÷ 2 and 10 is 30 ÷ 3: each uses only one of the factors. 25 is 30 − 2 − 3."),
            (40, (2, None, 5), 4, [20, 8, 33],
             "20 is 40 ÷ 2 and 8 is 40 ÷ 5: each uses only one of the factors. 33 is 40 − 2 − 5.")]:
        known = [v for v in b if v]
        assert prod(known) * ans == a
        shown = times(["?" if v is None else v for v in b])
        e = ("Multiply the factors you know: %s = %d. Then %d ÷ %d = <b>%d</b>. Check: %s = %d. %s"
             % (times(known), prod(known), a, prod(known), ans, times([ans if v is None else v for v in b]), a, ex_txt))
        its.append(mcq("Find the missing factor: %d = %s" % (a, shown), ans, wrong, e))

    assert 48 // 4 == 12 and 48 - 4 == 44 and 48 * 4 == 192
    its.append(mcq("Find the missing factor: 48 = 4 × ?", 12, [44, 192, 11],
                   "48 ÷ 4 = <b>12</b>. Check: 4 × 12 = 48. 44 is 48 − 4, 192 is 48 × 4, and 4 × 11 = 44, not 48."))

    t = T(24, T(4, 2, 2), T(6, 2, 3))
    assert leaves(t) == [2, 2, 2, 3]
    its.append(mcq(fig(tree_svg(t)) + "Which number sentence does this factor tree show?", "24 = 2 × 2 × 2 × 3",
                   ["24 = 2 × 2 × 3", "24 = 4 × 6 × 2 × 2 × 2 × 3", "24 = 2 + 2 + 2 + 3"],
                   "Multiply the circled numbers at the ends of the branches: 2 × 2 × 2 × 3 = <b>24</b>. "
                   "2 × 2 × 3 = 12 misses one 2. 4 and 6 have already been split, so do not use them again. "
                   "2 + 2 + 2 + 3 = 9 adds instead of multiplying."))

    t = T(36, T(4, 2, 2), T(9, 3, 3))
    assert leaves(t) == [2, 2, 3, 3]
    its.append(mcq(fig(tree_svg(t)) + "Which number sentence does this factor tree show?", "36 = 2 × 2 × 3 × 3",
                   ["36 = 2 × 3", "36 = 4 × 9 × 2 × 2 × 3 × 3", "36 = 2 + 2 + 3 + 3"],
                   "Multiply the circled numbers: 2 × 2 = 4, 3 × 3 = 9, 4 × 9 = <b>36</b>. 2 × 3 = 6 counts each "
                   "number only once. 4 and 9 have already been split. 2 + 2 + 3 + 3 = 10 adds instead of multiplying."))

    t = T(40, T(8, 2, 4), 5)
    assert leaves(t) == [2, 4, 5]
    its.append(mcq(fig(tree_svg(t, hide=5)) + "What number is missing from this factor tree?", 5, [32, 4, 10],
                   "40 splits into a factor pair: 8 × ? = 40. 40 ÷ 8 = <b>5</b>. 32 is 40 − 8. 4 and 10 are factors "
                   "of 40, but 8 × 4 = 32 and 8 × 10 = 80."))

    assert 2 * 2 * 3 * 5 == 60
    its.append(mcq("What is 2 × 2 × 3 × 5?", 60, [12, 30, 120],
                   "2 × 2 = 4, 4 × 3 = 12, 12 × 5 = <b>60</b>. 12 comes from adding (2 + 2 + 3 + 5), 30 uses only one 2, "
                   "and 120 uses three 2s."))

    assert 2 * 18 == 36 and 3 * 12 == 36 and 6 * 6 == 36 and 5 * 7 == 35
    its.append(mcq("Which is <b>not</b> equal to 36?", "5 × 7", ["2 × 18", "3 × 12", "6 × 6"],
                   "<b>5 × 7</b> = 35, not 36. 2 × 18, 3 × 12 and 6 × 6 all equal 36: they are factor pairs of 36."))

    assert 6 * 4 == 2 * 3 * 4 and 5 * 4 == 20 and 2 * 7 == 14
    its.append(mcq("Which is equal to 2 × 3 × 4?", "6 × 4", ["5 × 4", "2 × 7", "9"],
                   "2 × 3 = 6, so 2 × 3 × 4 = <b>6 × 4</b> = 24. 5 × 4 adds 2 + 3, 2 × 7 adds 3 + 4, and 9 adds all three."))

    assert 4 * 7 * 5 == 140
    its.append(mcq("Work out 4 × 7 × 5. Tip: multiply 4 × 5 first.", 140, [16, 28, 280],
                   "You can multiply in any order. 4 × 5 = 20, then 20 × 7 = <b>140</b>. 16 is 4 + 7 + 5, "
                   "28 forgets the × 5, and 280 is 4 × 7 × 10."))

    assert 2 * 9 * 5 == 90
    its.append(mcq("Work out 2 × 9 × 5.", 90, [16, 18, 45],
                   "2 × 5 = 10, then 10 × 9 = <b>90</b>. 16 is 2 + 9 + 5, 18 forgets the × 5, and 45 forgets the × 2."))

    assert pairs(12) == [(1, 12), (2, 6), (3, 4)]
    its.append(mcq("In how many ways can you write 12 as a product of two whole numbers? (3 × 4 and 4 × 3 count "
                   "as one way.)", 3, [6, 2, 4],
                   "1 × 12, 2 × 6 and 3 × 4: <b>3</b> ways. 6 is the number of factors, not pairs. 2 forgets 1 × 12, and 4 counts one pair twice."))

    assert 2 * 2 * 2 == 8 and 2 * 2 * 4 == 16
    its.append(mcq("Write 8 as a product of three factors, each greater than 1.", "2 × 2 × 2",
                   ["2 × 4", "1 × 2 × 4", "2 × 2 × 4"],
                   "8 = 2 × 4 and 4 = 2 × 2, so 8 = <b>2 × 2 × 2</b>. 2 × 4 has only two factors, 1 × 2 × 4 uses 1, "
                   "and 2 × 2 × 4 = 16."))

    assert 3 * 4 * 5 == 60 and 3 + 4 + 5 == 12
    its.append(mcq("Which number is equal to 3 × 4 × 5?", 60, [12, 20, 345],
                   "3 × 4 = 12, then 12 × 5 = <b>60</b>. 12 is 3 + 4 + 5, 20 is only 4 × 5, and 345 writes the digits "
                   "side by side."))

    assert 2 * 9 == 18 and 3 * 6 == 18 and 2 * 3 * 3 == 18 and 2 * 3 * 4 == 24
    its.append(mcq("Which is <b>not</b> a way to write 18 as a product of factors?", "2 × 3 × 4",
                   ["2 × 9", "3 × 6", "2 × 3 × 3"],
                   "<b>2 × 3 × 4</b> = 24, not 18. 2 × 9 = 18, 3 × 6 = 18 and 2 × 3 × 3 = 6 × 3 = 18."))

    assert 2 * 2 * 5 * 5 == 100
    its.append(mcq("100 = 4 × 25. Find the missing factor: 100 = 2 × 2 × 5 × ?", 5, [25, 10, 20],
                   "4 = 2 × 2 and 25 = 5 × 5, so 100 = 2 × 2 × 5 × <b>5</b>. Check: 4 × 5 × 5 = 20 × 5 = 100. "
                   "25 would give 2 × 2 × 5 × 25 = 500. 10 and 20 give 200 and 400."))

    assert 8 * 3 * 3 == 72 and 8 * 9 == 72
    its.append(mcq("72 = 8 × 9. Find the missing factor: 72 = 8 × 3 × ?", 3, [6, 24, 9],
                   "9 = 3 × 3, so 72 = 8 × 3 × <b>3</b>. Check: 8 × 3 = 24 and 24 × 3 = 72. 6 is 9 − 3, 24 is 8 × 3, "
                   "and 9 would give 8 × 3 × 9 = 216."))
    assert len(its) == 20, len(its)
    return {"title": "Writing a number as a product of factors", "items": its}


# ============================================================ set 3: multiples
def set_multiples(P):
    its = []
    for v, right, wrong in [(6, 42, [16, 26, 63]), (8, 72, [28, 18, 84]), (9, 81, [19, 39, 89])]:
        assert right % v == 0 and all(w % v for w in wrong)
        e = "%d × %d = %d, so <b>%d</b> is a multiple of %d. %s" % (
            v, right // v, right, right, v,
            " ".join("%d ÷ %d = %d remainder %d." % (w, v, w // v, w % v) for w in wrong))
        e += " Having %s %d as a digit does not make a number a multiple of %d." % ("an" if v == 8 else "a", v, v)
        its.append(mcq("Which number is a multiple of %d?" % v, right, wrong, e))

    assert 47 % 7 and all(x % 7 == 0 for x in (49, 56, 35))
    its.append(mcq("Which number is <b>not</b> a multiple of 7?", 47, [49, 56, 35],
                   "7 × 6 = 42 and 7 × 7 = 49, so <b>47</b> is not in the 7 times table. "
                   "7 × 7 = 49, 7 × 8 = 56 and 7 × 5 = 35."))

    its.append(mcq("What is the 6th multiple of 8?", 48, [40, 56, 14],
                   "The 6th multiple of 8 is 8 × 6 = <b>48</b>. 40 is the 5th multiple, 56 is the 7th, and 14 is 8 + 6."))

    its.append(mcq("Which list shows the first five multiples of 7?", "7, 14, 21, 28, 35",
                   ["1, 7", "14, 21, 28, 35, 42", "7, 17, 27, 37, 47"],
                   "The multiples of 7 are 7 × 1, 7 × 2, 7 × 3 …: <b>7, 14, 21, 28, 35</b>. The first multiple is 7 itself. "
                   "1, 7 are the factors of 7, and 7, 17, 27 … add 10 each time."))

    nm, he, his = P.next()
    shaded = [3, 6, 9, 12, 18]
    assert [v for v in range(3, 21, 3) if v not in shaded] == [15]
    its.append(mcq(fig(track_svg(20, shaded)) + "%s shades the multiples of 3 on this number track. "
                   "Which multiple of 3 has %s missed?" % (nm, he), 15, [13, 16, 10],
                   "Count in 3s: 3, 6, 9, 12, <b>15</b>, 18. 3 × 5 = 15 is not shaded. 13 has a 3 as a digit, "
                   "but 13 ÷ 3 = 4 remainder 1. 16 and 10 are not multiples of 3."))

    assert 54 % 6 == 0 and 6 * 9 == 54
    its.append(mcq("Is 54 a multiple of 6?", "Yes. 6 × 9 = 54",
                   ["No. 54 does not end in 6", "No. 54 ÷ 6 = 8 r 6", "No. 6 × 8 = 54"],
                   "6 × 9 = 54, so <b>yes</b>, 54 is a multiple of 6. Multiples of 6 do not have to end in 6 (12, 18, 24 …). "
                   "6 × 8 = 48, so 54 ÷ 6 is not 8 r 6: a remainder of 6 means one more 6 fits."))

    nm, he, his = P.next()
    its.append(mcq("%s says 30 is a factor of 5. Is %s right?" % (nm, he), "No. 30 is a multiple of 5",
                   ["Yes. 5 × 6 = 30", "Yes. 30 ÷ 5 = 6", "No. 5 is a multiple of 30"],
                   "5 × 6 = 30, so 30 is a <b>multiple</b> of 5, and 5 is a factor of 30. A factor divides the number; "
                   "a multiple is in its times table."))

    assert 56 % 7 == 0 and 56 % 6
    its.append(mcq("Which statement is true?", "7 is a factor of 56",
                   ["56 is a factor of 7", "7 is a multiple of 56", "6 is a factor of 56"],
                   "7 × 8 = 56, so <b>7 is a factor of 56</b> (and 56 is a multiple of 7). 56 ÷ 6 = 9 remainder 2, "
                   "so 6 is not a factor of 56."))

    assert 12 % 4 == 0 and 12 % 6 == 0 and 10 % 4 and 18 % 4 and 16 % 6
    its.append(mcq("Which number is a multiple of both 4 and 6?", 12, [10, 18, 16],
                   "4 × 3 = 12 and 6 × 2 = 12, so <b>12</b> is a multiple of both. 10 is 4 + 6. 18 is a multiple of 6 only, "
                   "and 16 is a multiple of 4 only."))

    assert 72 % 9 == 0 and 63 % 9 == 0
    its.append(mcq("What is the next multiple of 9 after 63?", 72, [64, 73, 81],
                   "63 = 9 × 7, so the next multiple is 9 × 8 = <b>72</b>. 64 adds 1, 73 adds 10, and 81 = 9 × 9 skips 72."))

    assert 175 % 25 == 0 and all(v % 25 for v in (155, 205, 260))
    its.append(mcq("Which number is a multiple of 25?", 175, [155, 205, 260],
                   "Multiples of 25 end in 00, 25, 50 or 75. 25 × 7 = <b>175</b>. 155 and 205 end in 5, so they are "
                   "multiples of 5, but not of 25. 260 ends in 60."))

    m = [v for v in range(1, 51) if v % 6 == 0]
    assert len(m) == 8 and m[-1] == 48
    its.append(mcq("How many multiples of 6 are there from 1 to 50?", 8, [9, 7, 10],
                   "6, 12, 18, 24, 30, 36, 42, 48: <b>8</b> multiples. 6 × 9 = 54 is more than 50, so 9 is too many. "
                   "7 means one was missed, and 10 counts in 5s."))

    assert 64 % 4 == 0 and all(v % 4 for v in (42, 54, 70))
    nm, he, his = P.next()
    its.append(mcq("%s counts in 4s from 4. Which number will %s say?" % (nm, he), 64, [42, 54, 70],
                   "4 × 16 = <b>64</b>, so 64 is in the count. 42, 54 and 70 are even, but each leaves a remainder of 2 "
                   "when divided by 4. Even numbers are not all multiples of 4."))

    good = [15, 40, 65, 90]
    b1, b2 = [10, 25, 51, 70], [5, 15, 52, 65]
    assert all(v % 5 == 0 for v in good) and sum(v % 5 != 0 for v in b1) == 1 and sum(v % 5 != 0 for v in b2) == 1
    its.append(mcq("Which list shows only multiples of 5?", lst(good), [lst(b1), lst(b2), "1, 5"],
                   "Multiples of 5 end in 0 or 5. <b>%s</b> all do. 51 and 52 have a 5 in them but end in 1 and 2. "
                   "1 and 5 are the factors of 5." % lst(good)))

    assert 7 * 100 == 700
    its.append(mcq("What is the 100th multiple of 7?", 700, [107, 70, 7000],
                   "The 100th multiple of 7 is 7 × 100 = <b>700</b>. 107 is 7 + 100, 70 is 7 × 10, and 7000 is 7 × 1000."))

    nm, he, his = P.next()
    its.append(mcq("%s says 12 is a multiple of 24. Is %s right?" % (nm, he), "No. 24 is a multiple of 12",
                   ["Yes. 12 × 2 = 24", "Yes. 12 is in the 24 times table", "No. 12 and 24 are not linked"],
                   "12 × 2 = 24, so <b>24 is a multiple of 12</b>, and 12 is a factor of 24. A multiple of 24 is 24 or "
                   "more: 24, 48, 72 …"))

    best = min((abs(50 - v), v) for v in range(8, 80, 8))[1]
    assert best == 48
    its.append(mcq("Which multiple of 8 is closest to 50?", 48, [56, 40, 50],
                   "8 × 6 = 48 and 8 × 7 = 56. 48 is 2 away from 50, and 56 is 6 away, so the answer is <b>48</b>. "
                   "40 is 10 away, and 50 is not a multiple of 8 (50 ÷ 8 = 6 r 2)."))

    ans = [v for v in range(41, 50) if v % 7 == 0 and v % 2]
    assert ans == [49] and 42 % 7 == 0 and 47 % 7 and 45 % 7
    its.append(mcq("I am a multiple of 7 between 40 and 50. I am an odd number. What number am I?", 49, [42, 47, 45],
                   "The multiples of 7 between 40 and 50 are 42 and 49. 42 is even, so the answer is <b>49</b> (7 × 7). "
                   "47 and 45 are odd but not multiples of 7."))
    assert len(its) == 20, len(its)
    return {"title": "Multiples", "items": its}


# ============================================================ set 4: divisibility rules
def set_divisibility(P):
    its = []
    assert 538 % 2 == 0 and all(v % 2 for v in (825, 467, 2001))
    its.append(mcq("Which number is divisible by 2?", 538, [825, 467, 2001],
                   "A number is divisible by 2 if its <b>last</b> digit is even (0, 2, 4, 6 or 8). <b>538</b> ends in 8. "
                   "825 starts with an even digit and 467 has even digits in it, but they end in 5 and 7. 2001 ends in 1."))

    assert 735 % 5 == 0 and all(v % 5 for v in (557, 5052, 508))
    its.append(mcq("Which number is divisible by 5?", 735, [557, 5052, 508],
                   "A number is divisible by 5 if it ends in 0 or 5. <b>735</b> ends in 5. 557, 5052 and 508 have 5s in "
                   "them, but they end in 7, 2 and 8."))

    assert 4990 % 10 == 0 and all(v % 10 for v in (1005, 1001, 4099))
    its.append(mcq("Which number is divisible by 10?", 4990, [1005, 1001, 4099],
                   "A number is divisible by 10 if it ends in 0. <b>4990</b> ends in 0. 1005 ends in 5 (it is divisible "
                   "by 5, not 10). 1001 and 4099 end in 1 and 9."))

    assert 471 % 3 == 0 and dsum(471) == 12 and all(v % 3 for v in (473, 3401, 532))
    its.append(mcq("Which number is divisible by 3?", 471, [473, 3401, 532],
                   "Add the digits. If the sum is a multiple of 3, the number is divisible by 3. 4 + 7 + 1 = 12, so "
                   "<b>471</b> works (471 = 3 × 157). 473 ends in 3 but 4 + 7 + 3 = 14. 3401 starts with 3 but "
                   "3 + 4 + 0 + 1 = 8. 5 + 3 + 2 = 10."))

    assert 738 % 9 == 0 and dsum(738) == 18 and all(v % 9 for v in (919, 829, 9001))
    its.append(mcq("Which number is divisible by 9?", 738, [919, 829, 9001],
                   "Add the digits. If the sum is a multiple of 9, the number is divisible by 9. 7 + 3 + 8 = 18, so "
                   "<b>738</b> works (738 = 9 × 82). 919 and 829 have digit sums of 19, and 9001 has 10. "
                   "Having a 9 in the number does not matter."))

    assert 57 % 3 == 0 and 57 % 9 and 81 % 9 == 0 and 58 % 3 and 44 % 3
    its.append(mcq("Which number is divisible by 3 but <b>not</b> by 9?", 57, [81, 58, 44],
                   "5 + 7 = 12. 12 is a multiple of 3 but not of 9, so <b>57</b> (= 3 × 19) is divisible by 3 only. "
                   "8 + 1 = 9, so 81 is divisible by both. 5 + 8 = 13 and 4 + 4 = 8, so 58 and 44 are not divisible by 3."))

    nm, he, his = P.next()
    assert 316 % 4 == 0 and 316 // 4 == 79 and dsum(316) == 10
    its.append(mcq("%s says 316 is not divisible by 4, because 3 + 1 + 6 = 10 and 10 is not a multiple of 4. "
                   "Is %s right?" % (nm, he), "No. 316 ÷ 4 = 79",
                   ["Yes. 10 is not a multiple of 4", "Yes. 316 is odd", "No. 10 is a multiple of 4"],
                   "The digit-sum rule only works for 3 and 9. It does not work for 4. 4 × 79 = 316, so 316 <b>is</b> "
                   "divisible by 4. 316 is even, and 10 is not a multiple of 4."))

    good = [d for d in range(10) if (470 + d) % 3 == 0]
    assert good == [1, 4, 7] and all((470 + d) % 3 for d in (3, 0, 2))
    its.append(mcq("Which digit can go in the box to make 47<b>□</b> divisible by 3?", 1, [3, 0, 2],
                   "4 + 7 = 11. The digit sum must be a multiple of 3: 11 + 1 = 12 works, so <b>1</b> (471). "
                   "4 or 7 would also work. 3 gives 14, 0 gives 11 and 2 gives 13. The last digit being 3 does not help."))

    good = [d for d in range(10) if (504 + 10 * d) % 9 == 0]
    assert good == [0, 9] and (564 % 3 == 0) and 564 % 9 and 534 % 9 and 514 % 9
    its.append(mcq("Which digit can go in the box to make 5<b>□</b>4 divisible by 9?", 9, [3, 6, 1],
                   "5 + 4 = 9. The digit sum must be a multiple of 9: 9 + 9 = 18 works, so <b>9</b> (594 = 9 × 66). "
                   "6 gives 564: 5 + 6 + 4 = 15, which is a multiple of 3 but not of 9. 3 gives 12 and 1 gives 10."))

    assert 370 % 10 == 0 and 255 % 2 and 252 % 5 and 525 % 2
    its.append(mcq("Which number is divisible by both 2 <b>and</b> 5?", 370, [255, 252, 525],
                   "Divisible by 2 means the last digit is even. Divisible by 5 means it ends in 0 or 5. Both together "
                   "means it ends in <b>0</b>: 370. 255 and 525 are odd, and 252 does not end in 0 or 5."))

    assert 240 % 30 == 0 and 250 % 3 and 245 % 2 and 236 % 5
    its.append(mcq("Which number is divisible by 2, 3 <b>and</b> 5?", 240, [250, 245, 236],
                   "It must end in 0 (for 2 and 5) and have a digit sum that is a multiple of 3. 2 + 4 + 0 = 6, so "
                   "<b>240</b> works. 250 has digit sum 7, 245 is odd, and 236 does not end in 0 or 5."))

    assert 96 % 8 == 0 and 8 * 12 == 96 and 8 * 11 == 88
    its.append(mcq("Is 96 divisible by 8?", "Yes. 8 × 12 = 96",
                   ["No. 9 + 6 = 15", "No. 96 ÷ 8 = 11 r 8", "No. 8 × 11 = 96"],
                   "8 × 10 = 80 and 8 × 2 = 16, so 8 × 12 = 96. <b>Yes</b>, 96 is divisible by 8. The digit sum only "
                   "works for 3 and 9. A remainder of 8 means one more 8 fits, and 8 × 11 = 88."))

    assert 91 % 7 == 0 and 91 // 7 == 13 and all(91 % d for d in (3, 9, 2))
    its.append(mcq("Which number divides 91 exactly?", 7, [3, 9, 2],
                   "7 × 13 = 91, so <b>7</b> divides 91 exactly. 9 + 1 = 10, which is not a multiple of 3 or 9. "
                   "91 is odd, so 2 does not divide it."))

    assert 135 % 9 == 0 and dsum(135) == 9 and all(135 % d for d in (2, 10, 4))
    its.append(mcq("Which number divides 135 exactly?", 9, [2, 10, 4],
                   "1 + 3 + 5 = 9, so 135 is divisible by <b>9</b>: 135 = 9 × 15. 135 is odd, so 2 and 4 do not divide it, "
                   "and it does not end in 0, so 10 does not divide it."))

    assert 132 % 6 == 0 and 132 // 6 == 22
    its.append(mcq("Is 132 divisible by 6?", "Yes. 132 ÷ 6 = 22",
                   ["No. It does not end in 6", "No. 1 + 3 + 2 = 6 is too small", "No. 132 ÷ 6 = 21 r 2"],
                   "6 × 22 = 132, so <b>yes</b>. A quick check: 132 is even (divisible by 2) and 1 + 3 + 2 = 6 "
                   "(divisible by 3), so it is divisible by 6. Multiples of 6 do not have to end in 6. 6 × 21 = 126, "
                   "and 132 − 126 = 6, so 21 r 2 is wrong."))

    assert 1045 % 3 and all(v % 3 == 0 for v in (1035, 2001, 1236))
    its.append(mcq("Which number is <b>not</b> divisible by 3?", 1045, [1035, 2001, 1236],
                   "1 + 0 + 4 + 5 = 10, which is not a multiple of 3, so <b>1045</b> is not divisible by 3. "
                   "1035 has digit sum 9, 2001 has 3, and 1236 has 12: all multiples of 3."))

    assert 3726 % 9 == 0 and dsum(3726) == 18 and 3729 % 9 and 3729 % 3 == 0 and 9100 % 9 and 1999 % 9
    its.append(mcq("Which number is divisible by 9?", 3726, [3729, 9100, 1999],
                   "3 + 7 + 2 + 6 = 18, so <b>3726</b> is divisible by 9 (3726 = 9 × 414). 3729 has digit sum 21: "
                   "divisible by 3 but not 9. 9100 has 10 and 1999 has 28."))

    assert all(450 % d == 0 for d in (2, 3, 5, 9, 10))
    its.append(mcq("Which numbers is 450 divisible by?", "2, 3, 5, 9 and 10",
                   ["5 and 10 only", "2, 5 and 10 only", "3, 5 and 9 only"],
                   "450 ends in 0, so it is divisible by 2, 5 and 10. 4 + 5 + 0 = 9, so it is divisible by 3 and 9. "
                   "The answer is <b>2, 3, 5, 9 and 10</b>."))

    assert all(v % 3 == 0 for v in (9, 18, 27, 36))
    its.append(mcq("If a number is divisible by 9, which number must it also be divisible by?", 3, [18, 6, 2],
                   "9 = 3 × 3, so every multiple of 9 is also a multiple of <b>3</b>. 9 itself is not divisible by 18, "
                   "6 or 2, so those do not always work."))

    assert 54 % 9 == 0 and 54 % 4 and 54 % 5
    its.append(mcq("Which statement is true?", "54 is divisible by 9",
                   ["9 is divisible by 54", "54 is divisible by 4", "54 is divisible by 5"],
                   "5 + 4 = 9, and 9 × 6 = 54, so <b>54 is divisible by 9</b>. 9 ÷ 54 is not a whole number. "
                   "54 ÷ 4 = 13 r 2, and 54 does not end in 0 or 5."))
    assert len(its) == 20, len(its)
    return {"title": "Divisibility rules for 2, 3, 5, 9 and 10", "items": its}


# ============================================================ set 5: word problems
def set_words(P):
    its = []
    assert 36 % 8 and all(36 % g == 0 for g in (4, 6, 9))
    its.append(mcq("A teacher puts 36 chairs in equal rows for a class assembly, with none left over. Which could "
                   "<b>not</b> be the number of chairs in each row?", "8 chairs", ["4 chairs", "6 chairs", "9 chairs"],
                   "The number in each row must be a factor of 36. 36 ÷ 8 = 4 remainder 4, so <b>8 chairs</b> does not work. "
                   "4 × 9 = 36 and 6 × 6 = 36."))

    opts = [(5, 6), (4, 8), (3, 9), (7, 4)]
    assert [r * c == 30 for r, c in opts] == [True, False, False, False]
    its.append(mcq("A school hall has 30 chairs. Which layout uses all 30 chairs in equal rows?",
                   "5 rows of 6", ["%d rows of %d" % p for p in opts[1:]],
                   "5 × 6 = <b>30</b>, so 5 rows of 6 works. 4 × 8 = 32, 3 × 9 = 27 and 7 × 4 = 28."))

    assert 24 % 6 == 0 and all(24 % v for v in (5, 7, 9))
    its.append(mcq("24 students make equal teams for sport, with no one left out. Which team size works?",
                   "6 students", ["5 students", "7 students", "9 students"],
                   "The team size must be a factor of 24. 24 ÷ 6 = 4, so teams of <b>6 students</b> give 4 teams. "
                   "24 ÷ 5, 24 ÷ 7 and 24 ÷ 9 all leave a remainder."))

    assert 54 % 6 == 0 and all(v % 6 for v in (46, 56, 64))
    its.append(mcq("Cupcakes for the school fete are packed in boxes of 6. Which number of cupcakes fills the boxes "
                   "with none left over?", 54, [46, 56, 64],
                   "The number must be a multiple of 6. 6 × 9 = <b>54</b>. 46, 56 and 64 have a 6 as a digit, but they "
                   "are not multiples of 6: each leaves a remainder of 4."))

    nm, he, his = P.next()
    assert 8 * 3 < 30 <= 8 * 4
    its.append(mcq("Sausages come in packets of 8. %s needs at least 30 sausages for the sausage sizzle. What is the "
                   "fewest packets %s can buy?" % (nm, he), "4 packets", ["3 packets", "5 packets", "8 packets"],
                   "Multiples of 8: 8, 16, 24, 32. 3 packets give 24, which is not enough. <b>4 packets</b> give 32. "
                   "5 packets give 40, which is more than needed."))

    assert 48 * 2 < 130 <= 48 * 3
    its.append(mcq("130 students go on a school excursion. Each bus holds 48 students. What is the fewest buses "
                   "they need?", "3 buses", ["2 buses", "4 buses", "82 buses"],
                   "Multiples of 48: 48, 96, 144. 2 buses hold 96, which is not enough. <b>3 buses</b> hold 144. "
                   "82 is 130 − 48."))

    nm, he, his = P.next()
    assert 12 % 6 == 0 and 18 % 6 == 0 and 18 % 4 and 12 % 9
    its.append(mcq("%s has 12 red beads and 18 blue beads. %s makes bracelets that are all the same, using every bead. "
                   "How many bracelets could %s make?" % (nm, cap(he), he), "6 bracelets",
                   ["4 bracelets", "9 bracelets", "36 bracelets"],
                   "The number of bracelets must be a factor of both 12 and 18. 6 works: each bracelet has 2 red and "
                   "3 blue beads, so <b>6 bracelets</b>. 4 divides 12 but not 18, 9 divides 18 but not 12, and 36 is "
                   "a multiple, not a factor."))

    ans = [v for v in range(1, 40) if v % 2 == 0 and v % 3 == 0 and v % 5 == 0]
    assert ans == [30] and 10 % 3 and 15 % 2 and 35 % 2
    its.append(mcq("A class has fewer than 40 students. They can line up in 2s, 3s or 5s with no one left over. "
                   "How many students are in the class?", 30, [10, 15, 35],
                   "The number must be a multiple of 2, 3 and 5. 2 × 3 × 5 = <b>30</b>. 10 is not a multiple of 3, "
                   "and 15 and 35 are odd, so they are not multiples of 2."))

    nm, he, his = P.next()
    ans = [v for v in range(10, 16) if 36 % v == 0 and v % 4 == 0]
    assert ans == [12] and 36 % 9 == 0 and 16 % 4 == 0 and 36 % 16 and 36 % 14
    its.append(mcq("%s is between 10 and 15 years old. %s age is a factor of 36 and a multiple of 4. How old is %s?"
                   % (nm, cap(his), he), 12, [9, 16, 14],
                   "Factors of 36 between 10 and 15: only 12. 12 = 4 × 3, so it is also a multiple of 4. %s is <b>12</b>. "
                   "9 is a factor of 36 but not a multiple of 4, 16 is a multiple of 4 but not a factor of 36, and 14 "
                   "is neither." % nm))

    assert 7 * 7 == 49
    its.append(mcq("A square courtyard is paved with 49 square tiles. How many tiles are along each side?", "7 tiles",
                   ["14 tiles", "49 tiles", "9 tiles"],
                   "A square has the same number of tiles along each side, so find a factor pair with two equal numbers: "
                   "7 × 7 = 49. There are <b>7 tiles</b>. 14 is 7 × 2, 49 is the total number of tiles, and 9 × 9 = 81."))

    assert 63 // 7 == 9 and 63 % 7 == 0
    its.append(mcq("A netball team has 7 players. 63 students want to play. How many full teams can they make?",
                   "9 teams", ["8 teams", "56 teams", "70 teams"],
                   "7 × 9 = 63, so they can make <b>9 teams</b> with no one left over. 7 × 8 = 56 is too few. "
                   "56 is 63 − 7, and 70 is 63 + 7."))

    assert 30 % 4 and all(v % 4 == 0 for v in (24, 32, 36))
    its.append(mcq("Tennis balls come in cans of 4. Which number of balls can you <b>not</b> buy in full cans?", 30,
                   [24, 32, 36],
                   "You can only buy a multiple of 4. 30 ÷ 4 = 7 remainder 2, so <b>30</b> balls is not possible. "
                   "4 × 6 = 24, 4 × 8 = 32 and 4 × 9 = 36."))

    nm, he, his = P.next()
    ans = [v for v in range(11, 30) if v % 4 == 0 and 40 % v == 0]
    assert ans == [20] and 40 % 12 and 10 % 4 and 40 % 24
    its.append(mcq("%s thinks of a number between 10 and 30. It is a multiple of 4 and a factor of 40. What is %s number?"
                   % (nm, his), 20, [12, 10, 24],
                   "Factors of 40: 1, 2, 4, 5, 8, 10, 20, 40. Between 10 and 30 there is only 20, and 20 = 4 × 5, so the number "
                   "is <b>20</b>. 12 and 24 are multiples of 4 but not factors of 40, and 10 is not a multiple of 4."))

    sizes = [d for d in factors(28) if 1 < d < 10]
    assert sizes == [2, 4, 7]
    its.append(mcq("28 students split into equal groups. Each group has more than 1 and fewer than 10 students. How many "
                   "different group sizes are possible?", 3, [6, 4, 2],
                   "The group size must be a factor of 28: 1, 2, 4, 7, 14, 28. Between 1 and 10 that leaves 2, 4 and 7: "
                   "<b>3</b> sizes. 6 counts every factor, 4 wrongly includes 14, and 2 misses one."))

    assert 48 // 8 == 6 and 48 % 8 == 0
    its.append(mcq("At the swimming carnival, 48 students swim in races. Each race fills all 8 lanes. How many races "
                   "are there?", "6 races", ["40 races", "56 races", "5 races"],
                   "8 × 6 = 48, so there are <b>6 races</b>. 40 is 48 − 8, 56 is 48 + 8, and 8 × 5 = 40 is too few."))

    nm, he, his = P.next()
    assert 135 % 9 == 0 and 135 // 9 == 15 and 14 * 9 == 126
    its.append(mcq("%s has 135 stickers to share equally among 9 friends. Can %s do it with none left over?" % (nm, he),
                   "Yes, 15 each", ["No, 135 is odd", "Yes, 14 each", "No, 135 ends in 5"],
                   "1 + 3 + 5 = 9, so 135 is divisible by 9. 9 × 15 = 135, so <b>yes, 15 each</b>. Odd numbers can still "
                   "be divisible by 9, and 9 × 14 = 126."))

    assert 100 // 12 == 8 and 100 % 12 == 4
    its.append(mcq("A farmer packs 100 eggs into cartons of 12. How many cartons can be filled?", "8 cartons",
                   ["9 cartons", "4 cartons", "88 cartons"],
                   "Multiples of 12: 12, 24, 36, 48, 60, 72, 84, 96, 108. 96 = 12 × 8, so <b>8 cartons</b> are full and "
                   "4 eggs are left over. 9 cartons need 108 eggs, 4 is the number left over, and 88 is 100 − 12."))

    days = [d for d in range(1, 30) if d % 3 == 0 and d % 4 == 0]
    assert days[0] == 12
    its.append(mcq("At the zoo, a koala is weighed every 3 days and has a health check every 4 days. Today it has both. "
                   "In how many days will it next have both on the same day?", "12 days", ["7 days", "24 days", "4 days"],
                   "Multiples of 3: 3, 6, 9, 12. Multiples of 4: 4, 8, 12. The first number in both lists is "
                   "<b>12</b>. 7 is 3 + 4, 24 is also in both lists but it is not the first, and 4 is not a multiple of 3."))

    nm, he, his = P.next()
    assert 5 * 6 == 30 and 30 // 10 == 3
    its.append(mcq("%s buys 5 packs of juice boxes. Each pack has 6 boxes. %s shares them equally among 10 friends. "
                   "How many does each friend get?" % (nm, cap(he)), 3, [6, 2, 20],
                   "5 × 6 = 30 juice boxes. 30 ÷ 10 = <b>3</b> each. 6 is the number in one pack, 2 is 10 ÷ 5, "
                   "and 20 is 30 − 10."))

    ans = [v for v in range(100, 121) if v % 9 == 0 and v % 2 == 0]
    assert ans == [108] and 117 % 9 == 0 and 117 % 2 and 112 % 9 and 99 < 100
    its.append(mcq("I am a multiple of 9 between 100 and 120. I am an even number. What number am I?", 108,
                   [117, 112, 99],
                   "Multiples of 9 between 100 and 120: 108 (1 + 0 + 8 = 9) and 117 (1 + 1 + 7 = 9). 117 is odd, so the "
                   "answer is <b>108</b>. 112 has digit sum 4, so it is not a multiple of 9, and 99 is less than 100."))
    assert len(its) == 20, len(its)
    return {"title": "Word problems with factors and multiples", "items": its}


# ============================================================ lesson
def body_html():
    return (
        "<h2>Factors and factor pairs</h2>"
        "<p>A <b>factor</b> divides a number exactly, with no remainder. Factors come in <b>pairs</b> that multiply "
        "to make the number. 3 × 4 = 12, so 3 and 4 are a factor pair of 12.</p>"
        "<figure class='sn-fig'>" + array_svg(3, 4) +
        "<figcaption>12 dots in 3 rows of 4: 3 × 4 = 12.</figcaption></figure>"
        "<p>To find <b>all</b> the factors, test 1, 2, 3, 4 … in order. Stop when the pairs meet. "
        "1 and the number itself are always factors.</p>"
        "<figure class='sn-fig'>" + rainbow_svg(24) +
        "<figcaption>A factor rainbow for 24: 1 × 24, 2 × 12, 3 × 8 and 4 × 6. 24 has 8 factors.</figcaption></figure>"
        + ex("Example", "Find all the factors of 30.",
             "1 × 30, 2 × 15, 3 × 10, 5 × 6. 4 does not divide 30. The next number, 6, is already in a pair, so stop.",
             "1, 2, 3, 5, 6, 10, 15, 30")
        + "<h2>Writing a number as a product of factors</h2>"
        "<p>A <b>product</b> is the answer to a multiplication. One number can be written as a product in many ways: "
        "24 = 3 × 8 = 4 × 6 = 2 × 3 × 4. A <b>factor tree</b> keeps splitting a number into factor pairs.</p>"
        "<figure class='sn-fig'>" + tree_svg(T(36, T(4, 2, 2), T(9, 3, 3))) +
        "<figcaption>36 = 4 × 9 = 2 × 2 × 3 × 3. Multiply the circled numbers to check.</figcaption></figure>"
        "<p>The circled numbers 2 and 3 cannot be split any further: they are <b>prime numbers</b>, with exactly "
        "two factors. You will meet primes in Year 6.</p>"
        + ex("Example", "Write 40 as a product of three factors.", "40 = 8 × 5, and 8 = 2 × 4.", "40 = 2 × 4 × 5")
        + "<h2>Multiples</h2>"
        "<p>A <b>multiple</b> is in a number’s times table: 7, 14, 21, 28, 35 … are multiples of 7. "
        "4 is a factor of 12, and 12 is a multiple of 4.</p>"
        + ex("Example", "Is 54 a multiple of 6?", "Count in 6s or use a fact: 6 × 9 = 54.", "Yes")
        + "<h2>Divisibility rules</h2>"
        "<p>“Divisible by 3” means 3 divides the number with no remainder. These quick checks save time:</p>"
        + table(["Divisible by", "Check", "Example"], [
            ["2", "The last digit is even (0, 2, 4, 6, 8)", "538"],
            ["5", "The last digit is 0 or 5", "735"],
            ["10", "The last digit is 0", "4990"],
            ["3", "The digits add to a multiple of 3", "471: 4 + 7 + 1 = 12"],
            ["9", "The digits add to a multiple of 9", "738: 7 + 3 + 8 = 18"],
        ])
        + "<p>For any other number, divide and look at the remainder: 96 ÷ 8 = 12, so 96 is divisible by 8.</p>"
        + ex("Example", "Is 1236 divisible by 3? Is it divisible by 9?",
             "1 + 2 + 3 + 6 = 12. 12 is a multiple of 3 but not of 9.", "Divisible by 3, not by 9")
        + "<h2>Common mistakes</h2>"
        + table(["Mistake", "What to do instead"], [
            ["Mixing up factors and multiples: 4 is a multiple of 12", "4 is a factor of 12; 12 is a multiple of 4"],
            ["Missing a factor pair", "Test 1, 2, 3, 4 … in order until the pairs meet"],
            ["Forgetting 1 and the number itself", "Every number has 1 and itself as factors"],
            ["Using the digit sum to test 4, 6 or 8", "The digit sum works only for 3 and 9. Divide to check 4"],
            ["Looking at the first digit to test 2, 5 or 10", "Look at the last digit"],
            ["Thinking 27 is a multiple of 7 because it has a 7", "27 ÷ 7 = 3 r 6. Digits do not decide"],
        ])
    )


FAQ = [
    {"q": "What is the difference between a factor and a multiple?",
     "a": "A factor divides a number exactly, and a multiple is in its times table. 4 is a factor of 12, and 12 is a multiple of 4."},
    {"q": "What do Year 5 students learn about factors and multiples in the Australian Curriculum?",
     "a": "In Year 5 (AC9M5N02) students write numbers as products of their factors, recognise multiples and work out whether one number is divisible by another. Prime and composite numbers follow in Year 6."},
    {"q": "What are the divisibility rules for 3 and 9?",
     "a": "Add the digits. If the sum is a multiple of 3, the number is divisible by 3; if it is a multiple of 9, the number is divisible by 9. For 471, 4 + 7 + 1 = 12, so it is divisible by 3 but not 9."},
    {"q": "Is 1 a factor of every number?",
     "a": "Yes. 1 divides every whole number exactly, and every number is also a factor of itself. So 1 and the number are always a factor pair."},
]


def gen():
    rnd = random.Random(5802)
    P = People(rnd)
    sets = [set_factors(P), set_products(P), set_multiples(P), set_divisibility(P), set_words(P)]
    balance(sets, rnd)
    seen = set()
    for s in sets:
        assert len(s["items"]) == 20, (s["title"], len(s["items"]))
        assert sorted(it["a"] for it in s["items"]) == sorted([0, 1, 2, 3] * 5)
        for it in s["items"]:
            assert len(set(it["c"])) == 4, it
            assert it["q"].count("<svg") <= 1
            k = it["q"] + "|" + "|".join(sorted(it["c"]))
            assert k not in seen, it["q"]
            seen.add(k)
    u = {
        "country": "au", "subject": "maths", "grade": "year-5", "slug": "factors-and-multiples", "sort": 2,
        "updated": UPDATED, "pdf_url": "",
        "title": "Factors and Multiples",
        "seo_title": "Year 5 Factors and Multiples Worksheets: Factor Pairs, Factor Trees and Divisibility Rules",
        "short_title": "Factors and multiples",
        "domain": "Number",
        "standard_code": "AC9M5N02",
        "standard_url": "https://v9.australiancurriculum.edu.au/f-10-curriculum/learning-areas/mathematics",
        "standard_text": "Express natural numbers as products of their factors, recognise multiples and determine if one number is divisible by another",
        "meta_desc": "Free Year 5 maths worksheets on factors and multiples: factor pairs, writing numbers as products of factors, factor trees, multiples and divisibility rules for 2, 3, 5, 9 and 10. 100 questions with an answer key, aligned to the Australian Curriculum and useful for NAPLAN practice.",
        "key_big": "A factor divides a number exactly; a multiple is in its times table.",
        "key_sub": "4 is a factor of 12, and 12 is a multiple of 4. 1 and the number itself are always factors. To test 3 or 9, add the digits.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }
    return mark_large(u, "factor tree|factor rainbow|number track")


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
