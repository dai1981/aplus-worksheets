# -*- coding: utf-8 -*-
"""
US Grade 1 Math: Compare Two-Digit Numbers (1.NBT.B.3)
  python tools/gen_us_math_g1_compare.py
Numbers are 10-99 (a few one-digit numbers like 7 to show 70 vs 7). Every comparison, order and
"only one choice works" is checked in code. HTML attributes use single quotes (no backslashes in the JSON).
In HTML, > and < are written &gt; and &lt;.
"""
import json, os, random, re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "us", "math", "grade-1")
UPDATED = "2026-11-02"
GREEN = "#006633"
FILL = "#cfe6d6"
CUBE = "#fbe3a8"
CUBE_EDGE = "#b7791f"
RED = "#c0392b"
INK = "#2b2b2b"
GREY = "#6b6259"
FONT = "Arial, Helvetica, sans-serif"
GIRLS = ["Maya", "Ava", "Mia", "Zoe", "Lily", "Emma", "Nora", "Ruby", "Sofia", "Grace"]
BOYS = ["Leo", "Noah", "Eli", "Sam", "Ben", "Omar", "Kai", "Jack", "Luis", "Owen"]

GT, LT = "&gt;", "&lt;"


# ------------------------------------------------------------ math and words
def tens(n):
    return n // 10


def ones(n):
    return n % 10


def pl(d, word):
    return "%d %s%s" % (d, word, "" if d == 1 else "s")


def to(n):
    """3 tens and 4 ones"""
    return "%s and %s" % (pl(tens(n), "ten"), pl(ones(n), "one"))


def sym(a, b):
    return GT if a > b else (LT if a < b else "=")


def rel(a, b):
    return "%d %s %d" % (a, sym(a, b), b)


def words_rel(a, b):
    return "%d is %s %d" % (a, "greater than" if a > b else ("less than" if a < b else "equal to"), b)


def swap(n):
    """Digits swapped (34 -> 43). None when that is not a new two-digit number."""
    if ones(n) == 0 or ones(n) == tens(n):
        return None
    return ones(n) * 10 + tens(n)


def join(xs):
    xs = [str(x) for x in xs]
    return xs[0] if len(xs) == 1 else ", ".join(xs[:-1]) + " and " + xs[-1]


def compare_e(x, y):
    """Tens first, then ones. Ends with 'so x ? y' in the order given."""
    if tens(x) != tens(y):
        big, small = max(x, y), min(x, y)
        s = "Look at the tens first. %d has %s and %d has %s. %s is more than %s, so %s." % (
            x, pl(tens(x), "ten"), y, pl(tens(y), "ten"), pl(tens(big), "ten"), pl(tens(small), "ten"), rel(x, y))
        if ones(small) > ones(big):
            s += " The ones do not matter."
        return s
    if x == y:
        return "Both are %s. They are the same, so %d = %d." % (to(x), x, y)
    big, small = max(x, y), min(x, y)
    return "Both have %s. Look at the ones. %d has %s and %d has %s. %s is more than %s, so %s." % (
        pl(tens(x), "ten"), x, pl(ones(x), "one"), y, pl(ones(y), "one"),
        pl(ones(big), "one"), pl(ones(small), "one"), rel(x, y))


def list_expl(nums, greatest):
    """Find the greatest (or least): tens first, then ones."""
    word = "most" if greatest else "fewest"
    ts = [tens(n) for n in nums]
    best = max(ts) if greatest else min(ts)
    cur = [n for n in nums if tens(n) == best]
    s = "Look at the tens first: %s. " % join(ts)
    if len(cur) == 1:
        s += "%d has the %s tens." % (cur[0], word)
        return s, cur[0]
    os_ = [ones(n) for n in cur]
    b2 = max(os_) if greatest else min(os_)
    win = [n for n in cur if ones(n) == b2]
    assert len(win) == 1
    s += "%s have %s. Now look at their ones: %s. %d has the %s ones." % (
        join(cur), pl(best, "ten"), join(os_), win[0], word)
    return s, win[0]


# ------------------------------------------------------------ helpers
def mcq(q, correct, cands, e):
    """4 choices: correct + the first 3 unique distractors. Positions are set later by balance()."""
    correct = str(correct)
    seen = {correct}
    pick = []
    for c in cands:
        if c is None:
            continue
        c = str(c)
        if c in seen or not c or c.startswith("-"):
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
        self.pool = [(n, "she", "her") for n in GIRLS] + [(n, "he", "his") for n in BOYS]
        rnd.shuffle(self.pool)
        self.i = 0

    def next(self):
        p = self.pool[self.i % len(self.pool)]
        self.i += 1
        return p


def fig(svg):
    return "<div class='qfig'>" + svg + "</div>"


def svg_wrap(w, h, body, label):
    return ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 %d %d' width='%d' height='%d' "
            "role='img' aria-label='%s'><g font-family='%s'>%s</g></svg>" % (w, h, w, h, label, FONT, body))


def text(x, y, t, fs=16, anchor="middle", col=INK, wt=700):
    return ("<text x='%.1f' y='%.1f' font-size='%d' font-weight='%d' fill='%s' text-anchor='%s'>%s</text>"
            % (x, y, fs, wt, col, anchor, t))


# ------------------------------------------------------------ figures
U = 10             # one small cube; a ten rod is U x 10U
ROD = 10 * U
RGAP, CGAP, GGAP = 5, 5, 16
M = 8


def blocks_w(n):
    t, o = tens(n), ones(n)
    parts = []
    if t:
        parts.append(t * U + (t - 1) * RGAP)
    if o:
        cols = (o + 4) // 5
        parts.append(cols * U + (cols - 1) * CGAP)
    return sum(parts) + GGAP * (len(parts) - 1)


def blocks_group(n, x0, y0):
    """Tens rods and ones cubes for n. Height = ROD. Cubes stack from the bottom in columns of 5."""
    t, o = tens(n), ones(n)
    s = []
    x = x0
    for k in range(t):
        s.append("<rect x='%d' y='%d' width='%d' height='%d' fill='%s' stroke='%s' stroke-width='1.5'/>"
                 % (x, y0, U, ROD, FILL, GREEN))
        for j in range(1, 10):
            s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='0.7'/>"
                     % (x, y0 + j * U, x + U, y0 + j * U, GREEN))
        x += U + (RGAP if k < t - 1 else 0)
    if t and o:
        x += GGAP
    for k in range(o):
        col, row = divmod(k, 5)
        cx = x + col * (U + CGAP)
        cy = y0 + ROD - U - row * (U + CGAP)
        s.append("<rect x='%d' y='%d' width='%d' height='%d' fill='%s' stroke='%s' stroke-width='1.5'/>"
                 % (cx, cy, U, U, CUBE, CUBE_EDGE))
    return "".join(s)


def blocks_svg(nums, letters=True):
    """Groups side by side. With letters, each group gets A, B above it."""
    lab = 26 if letters else 0
    colw = max(max(blocks_w(n) for n in nums), 30)
    gap = 40
    W = 2 * M + len(nums) * colw + (len(nums) - 1) * gap
    H = 2 * M + lab + ROD
    s = []
    for k, n in enumerate(nums):
        x = M + k * (colw + gap)
        if letters:
            s.append(text(x + colw / 2, M + 18, "AB"[k], 20, wt=800))
        s.append(blocks_group(n, x + (colw - blocks_w(n)) // 2, M + lab))
        if k:
            xl = x - gap / 2
            s.append("<line x1='%.1f' y1='%d' x2='%.1f' y2='%d' stroke='#b9b2a8' stroke-width='1' stroke-dasharray='4 3'/>"
                     % (xl, M, xl, H - M))
    label = ("tens and ones blocks for A and B") if letters else "tens and ones blocks"
    return svg_wrap(W, H, "".join(s), label)


CW, HEAD, ROW = 84, 34, 46


def chart_svg(nums, hi=None):
    """Tens-ones chart with one number per row. hi = 'tens' or 'ones' for red digits."""
    x0 = y0 = 6
    W = 2 * x0 + 2 * CW
    H = 2 * y0 + HEAD + ROW * len(nums)
    s = ["<rect x='%d' y='%d' width='%d' height='%d' fill='#fff' stroke='%s' stroke-width='2'/>"
         % (x0, y0, 2 * CW, HEAD + ROW * len(nums), GREEN),
         "<rect x='%d' y='%d' width='%d' height='%d' fill='%s'/>" % (x0, y0, 2 * CW, HEAD, FILL),
         "<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='1.5'/>"
         % (x0 + CW, y0, x0 + CW, y0 + HEAD + ROW * len(nums), GREEN)]
    for k, (name, f) in enumerate([("Tens", tens), ("Ones", ones)]):
        x = x0 + k * CW
        s.append(text(x + CW / 2, y0 + 23, name, 16))
        for r, n in enumerate(nums):
            s.append(text(x + CW / 2, y0 + HEAD + r * ROW + 34, str(f(n)), 28,
                          col=RED if hi == name.lower() else INK, wt=800))
    for r in range(len(nums)):
        y = y0 + HEAD + r * ROW
        s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='%s'/>"
                 % (x0, y, x0 + 2 * CW, y, GREEN, "2" if r == 0 else "1"))
    return svg_wrap(W, H, "".join(s), "tens and ones chart showing " + join(nums))


def gator_svg(a, b, labels=True):
    """a [mouth] b. The open mouth faces the greater number."""
    assert a != b
    W, H = 300, 120 if labels else 96
    cx, cy = 150, 52
    d = 1 if a > b else -1          # 1: mouth opens to the left (>)
    g = []
    # jaws: a thick > shape, drawn for d = 1 and mirrored for d = -1
    g.append("<path d='M -30 -34 L 28 0 L -30 34' fill='none' stroke='%s' stroke-width='9' "
             "stroke-linecap='round' stroke-linejoin='round'/>" % GREEN)
    # teeth on the inside of both jaws, pointing into the mouth
    L = (58 ** 2 + 34 ** 2) ** 0.5
    ux, uy = -58 / L, -34 / L                  # along the upper jaw, from the hinge
    nx, ny = -uy, ux                           # (0.506, -0.863) -> flip to point into the mouth
    nx, ny = -nx, -ny
    for t in (0.44, 0.64, 0.84):
        px, py = 28 + 58 * t * ux, 58 * t * uy
        for sgn in (1, -1):                    # upper jaw, then lower jaw (mirror in y)
            pts = [(px + nx * 4 - ux * 4, py + ny * 4 - uy * 4), (px + nx * 4 + ux * 4, py + ny * 4 + uy * 4),
                   (px + nx * 12, py + ny * 12)]
            g.append("<path d='M %.1f %.1f L %.1f %.1f L %.1f %.1f Z' fill='#fff' stroke='%s' stroke-width='1.2'/>"
                     % (pts[0][0], pts[0][1] * sgn, pts[1][0], pts[1][1] * sgn, pts[2][0], pts[2][1] * sgn, GREEN))
    ex_, ey_ = 28 + 58 * 0.3 * ux - nx * 11, 58 * 0.3 * uy - ny * 11   # eye sits on top of the upper jaw
    g.append("<circle cx='%.1f' cy='%.1f' r='5' fill='#fff' stroke='%s' stroke-width='2'/>" % (ex_, ey_, GREEN))
    g.append("<circle cx='%.1f' cy='%.1f' r='2.2' fill='%s'/>" % (ex_ - 1, ey_, INK))
    s = ["<g transform='translate(%d %d) scale(%d 1)'>%s</g>" % (cx, cy, d, "".join(g)),
         text(58, cy + 12, str(a), 36, wt=800), text(242, cy + 12, str(b), 36, wt=800)]
    if labels:
        s.append(text(58, 112, "greater" if a > b else "less", 16, col=GREEN if a > b else GREY))
        s.append(text(242, 112, "greater" if b > a else "less", 16, col=GREEN if b > a else GREY))
    return svg_wrap(W, H, "".join(s), "alligator mouth between %d and %d" % (a, b))


def numline_svg(lo, hi, marks):
    """Number line lo..hi with dots at marks."""
    step = 16
    W = 2 * 24 + (hi - lo) * step
    H = 86
    y = 52
    s = ["<line x1='14' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='2'/>" % (y, W - 14, y, INK),
         "<path d='M 14 %d l 8 -5 l 0 10 Z' fill='%s'/>" % (y, INK),
         "<path d='M %d %d l -8 -5 l 0 10 Z' fill='%s'/>" % (W - 14, y, INK)]
    for v in range(lo, hi + 1):
        x = 24 + (v - lo) * step
        big = v % 5 == 0
        s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='%s'/>"
                 % (x, y - (8 if big else 5), x, y + (8 if big else 5), INK, "2" if big else "1.2"))
        if big:
            s.append(text(x, y + 28, str(v), 15))
    for v, col in marks:
        x = 24 + (v - lo) * step
        s.append("<circle cx='%d' cy='%d' r='6' fill='%s'/>" % (x, y, col))
        s.append(text(x, y - 16, str(v), 16, col=col, wt=800))
    return svg_wrap(W, H, "".join(s), "number line from %d to %d" % (lo, hi))


def table_svg(head, rows):
    """Small data table: name | number."""
    c1, c2, rh = 120, 96, 30
    x0 = y0 = 4
    W, H = 2 * x0 + c1 + c2, 2 * y0 + rh * (len(rows) + 1)
    s = ["<rect x='%d' y='%d' width='%d' height='%d' fill='#fff' stroke='%s' stroke-width='2'/>"
         % (x0, y0, c1 + c2, rh * (len(rows) + 1), GREEN),
         "<rect x='%d' y='%d' width='%d' height='%d' fill='%s'/>" % (x0, y0, c1 + c2, rh, FILL),
         "<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='1.5'/>"
         % (x0 + c1, y0, x0 + c1, y0 + rh * (len(rows) + 1), GREEN),
         text(x0 + c1 / 2, y0 + 21, head[0], 16), text(x0 + c1 + c2 / 2, y0 + 21, head[1], 16)]
    for r, (name, v) in enumerate(rows):
        y = y0 + rh * (r + 1)
        s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='1'/>" % (x0, y, x0 + c1 + c2, y, GREEN))
        s.append(text(x0 + c1 / 2, y + 21, name, 16, wt=400))
        s.append(text(x0 + c1 + c2 / 2, y + 21, str(v), 17, wt=800))
    return svg_wrap(W, H, "".join(s), "table of " + head[1].lower())


# ------------------------------------------------------------ number makers
def make_pair(rnd, kind, used):
    """(big, small), both 10-99. kind: tens | trap (smaller has more pieces) | ones | swap."""
    for _ in range(5000):
        if kind == "tens":
            tb = rnd.randint(2, 9)
            ts = rnd.randint(1, tb - 1)
            big, small = tb * 10 + rnd.randint(0, 9), ts * 10 + rnd.randint(0, 9)
        elif kind == "trap":
            tb = rnd.randint(2, 7)
            ts = tb - 1
            big, small = tb * 10 + rnd.randint(0, 3), ts * 10 + rnd.randint(6, 9)
            if tens(small) + ones(small) <= tens(big) + ones(big):
                continue
        elif kind == "ones":
            t = rnd.randint(1, 9)
            ob = rnd.randint(1, 9)
            big, small = t * 10 + ob, t * 10 + rnd.randint(0, ob - 1)
        else:
            t, o = rnd.sample(range(1, 10), 2)
            big = max(t, o) * 10 + min(t, o)
            small = swap(big)
        if big in used or small in used or big <= small:
            continue
        used.update([big, small])
        return big, small
    raise RuntimeError("no pair")


def make_number(rnd, used):
    for _ in range(5000):
        n = rnd.randint(2, 8) * 10 + rnd.randint(1, 8)
        if n not in used and tens(n) != ones(n):
            used.add(n)
            return n
    raise RuntimeError("no number")


def beyond(n, want, rnd):
    """One number greater (want='gt') or less (want='lt') than n, and tempting numbers on the wrong side."""
    t, o = tens(n), ones(n)
    assert 2 <= t <= 8 and 1 <= o <= 8
    if want == "gt":
        right = (t + 1) * 10 + rnd.randint(0, o - 1)       # more tens, fewer ones
        wrong = [(t - 1) * 10 + 9,                           # 9 ones looks big
                 swap(n) if swap(n) and swap(n) < n else None,   # digits swapped
                 n,                                          # the same number is not greater
                 n - 10, n - 1]
    else:
        right = (t - 1) * 10 + rnd.randint(o + 1, 9)        # fewer tens, more ones
        wrong = [swap(n) if swap(n) and swap(n) > n else None,
                 (t + 1) * 10,                               # 0 ones looks small
                 n, n + 10, n + 1]
    wrong = [w for w in wrong if w is not None and 10 <= w <= 99]
    wrong = [w for k, w in enumerate(wrong) if w not in wrong[:k] and w != right]
    for w in wrong:
        assert (w <= n) if want == "gt" else (w >= n), (n, want, w)
    assert (right > n) if want == "gt" else (right < n)
    return right, wrong[:3]


def others_e(n, want, wrong):
    side = "less" if want == "gt" else "greater"
    ws = [w for w in wrong if w != n]
    s = ""
    if ws:
        s += " %s %s %s than %d." % (join(ws), "is" if len(ws) == 1 else "are", side, n)
    if n in wrong:
        s += " %d is the same number, so it is not %s." % (n, "greater" if want == "gt" else "less")
    return s


# ============================================================ set 1: tens and ones blocks
def set_blocks(rnd, used):
    its = []
    kinds = ["tens", "trap", "ones", "tens", "swap", "trap", "ones", "tens", "trap", "swap", "ones", "trap"]
    for k, kind in enumerate(kinds):
        big, small = make_pair(rnd, kind, used)
        a, b = (big, small) if rnd.random() < 0.5 else (small, big)
        greater = k % 2 == 0
        right, other = (big, small) if greater else (small, big)
        cands = [other, swap(right), tens(right) + ones(right), swap(other), tens(other) + ones(other),
                 right + 1 if ones(right) < 9 else right - 1]   # last: one cube miscounted
        cands = [c for c in cands if c is not None and c != right]
        e = "A has %s: %d. B has %s: %d. " % (to(a), a, to(b), b) + compare_e(a, b)
        if kind == "trap":
            e += " %d has more blocks, but each ten is worth 10 ones." % small
        if kind == "swap":
            e += " The same digits in a different order make a different number."
        e += " %d is the %s number." % (right, "greater" if greater else "smaller")
        q = fig(blocks_svg([a, b])) + "What number does each group show? Which number is %s?" % (
            "greater" if greater else "less")
        its.append(mcq(q, right, cands, e))
    for k in range(8):
        want = "gt" if k % 2 == 0 else "lt"
        n = make_number(rnd, used)
        right, wrong = beyond(n, want, rnd)
        e = "The blocks show %s: %d. " % (to(n), n) + compare_e(right, n) + others_e(n, want, wrong)
        q = fig(blocks_svg([n], letters=False)) + "Which number is %s than the number shown?" % (
            "greater" if want == "gt" else "less")
        its.append(mcq(q, right, wrong, e))
    return {"title": "Compare with tens and ones blocks", "items": its}


# ============================================================ set 2: tens first, then ones
def word_choices(x, y):
    right = words_rel(x, y)
    w = "less than" if x > y else "greater than"
    wrong = ["%d is %s %d" % (x, w, y), "%d is equal to %d" % (x, y), "%d is %s %d" % (y, "greater than" if x > y else "less than", x)]   # reversed: false
    return right, wrong


def set_places(rnd, used):
    its = []
    tens_pairs = [(43, 61), (31, 29), (75, 58), (19, 42), (60, 57), (86, 93)]
    ones_pairs = [(47, 42), (53, 58), (89, 81), (24, 26), (70, 73), (95, 92)]
    for k, (x, y) in enumerate(tens_pairs):
        assert tens(x) != tens(y)
        right, wrong = word_choices(x, y)
        if k in (1, 4):
            q = fig(chart_svg([x, y])) + "Look at the tens first. Which is true?"
        else:
            q = "Compare %d and %d. Look at the tens first. Which is true?" % (x, y)
        its.append(mcq(q, right, wrong, compare_e(x, y)))
    for k, (x, y) in enumerate(ones_pairs):
        assert tens(x) == tens(y) and x != y
        right, wrong = word_choices(x, y)
        if k in (1, 4):
            q = fig(chart_svg([x, y])) + "The tens are the same. Which is true?"
        elif k < 3:
            q = "Compare %d and %d. Both have %s. Which is true?" % (x, y, pl(tens(x), "ten"))
        else:
            q = "Compare %d and %d. Which is true?" % (x, y)
        its.append(mcq(q, right, wrong, compare_e(x, y)))
    # what should you compare? (4)
    for x, y in [(52, 48), (67, 63), (73, 69), (84, 89)]:
        tx, ty, ox, oy = tens(x), tens(y), ones(x), ones(y)
        T = lambda a, b: "%s and %s" % (pl(a, "ten"), pl(b, "ten"))
        O = lambda a, b: "%s and %s" % (pl(a, "one"), pl(b, "one"))
        if tx != ty:
            right = T(tx, ty)
            wrong = [O(ox, oy), "%s and %s" % (pl(tx, "ten"), pl(oy, "one")), "%s and %s" % (pl(ox, "one"), pl(ty, "ten"))]
            e = ("Always start with the tens. %d has %s and %d has %s. The tens are different, so they tell you: %s."
                 % (x, pl(tx, "ten"), y, pl(ty, "ten"), rel(x, y)))
            if (ox > oy) != (x > y):
                e += " Comparing the ones would give the wrong answer."
        else:
            right = O(ox, oy)
            wrong = [T(tx, ty), "%s and %s" % (pl(tx, "ten"), pl(oy, "one")), "%s and %s" % (pl(ox, "one"), pl(ty, "ten"))]
            e = ("Start with the tens. Both have %s, so the tens do not tell you. Now compare the ones: "
                 "%s and %s. So %s." % (pl(tx, "ten"), pl(ox, "one"), pl(oy, "one"), rel(x, y)))
        its.append(mcq("Which number is greater, %d or %d? What should you compare to find out?" % (x, y), right, wrong, e))
    # same digits, zeros (4)
    for x, y in [(36, 63), (81, 18), (70, 7), (90, 89)]:
        right, wrong = word_choices(x, y)
        e = compare_e(x, y)
        if swap(x) == y:
            e += " %d and %d use the same digits, but they are not equal." % (x, y)
        if y < 10:
            e += " %d is just %s. %d is %s." % (y, pl(y, "one"), x, pl(tens(x), "ten"))
        if x == 90:
            e += " A 0 in the ones place still leaves 9 tens."
        its.append(mcq("Compare %d and %d. Which is true?" % (x, y), right, wrong, e))
    return {"title": "Compare the tens first, then the ones", "items": its}


# ============================================================ set 3: the symbols >, < and =
def parse(s):
    a, op, b = s.replace("&gt;", ">").replace("&lt;", "<").split(" ")
    a, b = int(a), int(b)
    return {">": a > b, "<": a < b, "=": a == b}[op]


def set_symbols(rnd, used):
    its = []
    pairs = [(52, 25), (34, 39), (29, 31), (64, 46), (70, 69), (18, 81), (57, 75), (88, 83), (40, 44)]
    for x, y in pairs:
        op = sym(x, y)
        right = "%d %s %d" % (x, op, y)
        wrong = ["%d %s %d" % (x, LT if op == GT else GT, y), "%d = %d" % (x, y), "%d %s %d" % (y, op, x)]
        assert parse(right) and not any(parse(w) for w in wrong)
        its.append(mcq("Compare %d and %d. Which is true?" % (x, y), right, wrong, compare_e(x, y)))
    # equal (3)
    its.append(mcq("Which is true?", "30 + 6 = 36", ["30 + 6 = 63", "30 + 6 &gt; 36", "30 + 6 &lt; 36"],
                   "30 + 6 is 3 tens and 6 ones. That is 36. Both sides are the same number, so use =. "
                   "63 is 6 tens and 3 ones, not the same."))
    its.append(mcq("Which is true?", "4 tens 2 ones = 42", ["4 tens 2 ones = 24", "4 tens 2 ones &gt; 42", "4 tens 2 ones &lt; 42"],
                   "4 tens and 2 ones is 42. Both sides are the same number, so use =. "
                   "24 is 2 tens and 4 ones, not the same."))
    its.append(mcq("Which number makes this true? 50 + 8 = ☐", "58", ["85", "13", "508"],
                   "50 + 8 is 5 tens and 8 ones. That is 58. = means both sides are the same number. "
                   "85 is 8 tens and 5 ones. 13 adds 5 and 8. 508 writes 50 and 8 side by side."))
    # the alligator (3)
    for a, b in [(65, 56), (38, 83)]:
        e = ("The alligator mouth opens toward the greater number. Here it opens toward %d. "
             "%s The picture says %s." % (max(a, b), compare_e(a, b), words_rel(a, b)))
        right, wrong = word_choices(a, b)
        its.append(mcq(fig(gator_svg(a, b, labels=False)) + "The alligator mouth opens toward the greater number. "
                       "What does the picture say?", right, wrong, e))
    its.append(mcq("The alligator mouth eats the greater number. Which is correct?", "49 &lt; 94",
                   ["49 &gt; 94", "94 &lt; 49", "49 = 94"],
                   "94 has 9 tens and 49 has 4 tens, so 94 is greater. The open side of &lt; faces 94, so 49 &lt; 94."))
    # read and write (1)
    its.append(mcq("Which shows “27 is greater than 19”?", "27 &gt; 19", ["27 &lt; 19", "19 &gt; 27", "27 = 19"],
                   "“Greater than” is &gt;. Write 27, then &gt;, then 19: 27 &gt; 19. "
                   "The open side faces 27, the greater number."))
    # which comparison is true (4)
    for right, wrong in [("61 &gt; 59", ["29 &gt; 31", "45 &lt; 41", "72 &lt; 27"]),
                         ("38 &lt; 41", ["48 &gt; 51", "63 &lt; 36", "70 &lt; 69"]),
                         ("80 &gt; 79", ["19 &gt; 21", "56 &lt; 54", "93 &lt; 39"]),
                         ("26 &lt; 62", ["39 &gt; 42", "85 &lt; 58", "14 = 41"])]:
        assert parse(right) and not any(parse(w) for w in wrong), right
        a, _, b = right.split(" ")
        nots = []
        for w in wrong:
            x, _, y = w.split(" ")
            x, y = int(x), int(y)
            nots.append("%s is not true, because %s" % (w, rel(x, y)))
        e = compare_e(int(a), int(b)) + " " + ". ".join(nots) + "."
        its.append(mcq("Which comparison is true?", right, wrong, e))
    return {"title": "Use the symbols >, < and =", "items": its}


# ============================================================ set 4: greatest, least, order
def set_order(rnd, used):
    its = []
    for nums, greatest in [([47, 74, 69, 71], True), ([58, 49, 61, 56], True), ([90, 89, 39, 87], True),
                           ([36, 63, 46, 64], True),
                           ([27, 72, 31, 40], False), ([60, 56, 65, 59], False), ([45, 54, 39, 41], False),
                           ([83, 38, 80, 33], False)]:
        ex_, ans = list_expl(nums, greatest)
        e = ex_ + " So %d is the %s." % (ans, "greatest" if greatest else "least")
        its.append(mcq("Which number is the %s? %s" % ("greatest" if greatest else "least", ", ".join(map(str, nums))),
                       ans, [v for v in nums if v != ans], e))
    f = lambda l: ", ".join(str(v) for v in l)
    for given, up in [((52, 25, 43), True), ((31, 29, 13), True), ((68, 86, 70), False), ((44, 49, 94), False)]:
        order = sorted(given) if up else sorted(given, reverse=True)
        assert list(given) != order
        ones_first = sorted(given, key=lambda v: (ones(v), tens(v)), reverse=not up)
        cands = [order[::-1], ones_first, [order[1], order[0], order[2]], [order[0], order[2], order[1]], list(given)]
        asc = sorted(given)
        e = "%s and %s. " % (rel(asc[0], asc[1]), rel(asc[1], asc[2]))
        e += "So from %s: %s." % ("least to greatest" if up else "greatest to least", f(order))
        e = "Compare the tens first, then the ones. " + e
        q = "Put %s in order from %s." % (join(given), "least to greatest" if up else "greatest to least")
        its.append(mcq(q, f(order), [f(c) for c in cands if c != order], e))
    # greater than / less than a number (6)
    for k, n in enumerate([58, 40 + 3, 27, 64, 35, 72]):
        want = "gt" if k % 2 == 0 else "lt"
        right, wrong = beyond(n, want, rnd)
        word = "greater" if want == "gt" else "less"
        if k < 3:
            q = "Which number is %s than %d?" % (word, n)
        else:
            q = "Which number makes this true? ☐ %s %d" % (GT if want == "gt" else LT, n)
            word_e = "☐ %s %d means the box is %s than %d. " % (GT if want == "gt" else LT, n, word, n)
        e = (word_e if k >= 3 else "") + compare_e(right, n) + others_e(n, want, wrong)
        its.append(mcq(q, right, wrong, e))
    # between (2)
    for lo, hi, right, wrong in [(30, 40, 36, [63, 41, 29]), (50, 60, 54, [45, 61, 49])]:
        assert lo < right < hi and not any(lo < w < hi for w in wrong)
        outs = ", ".join(rel(w, lo if w < lo else hi) for w in wrong)
        e = ("%d has %s, so it is more than %d and less than %d: %d &lt; %d &lt; %d. The others are not between: %s."
             % (right, to(right), lo, hi, lo, right, hi, outs))
        its.append(mcq("Which number is between %d and %d?" % (lo, hi), right, wrong, e))
    return {"title": "Greatest, least and in order", "items": its}


# ============================================================ set 5: word problems
def set_words(rnd, used, P):
    its = []
    # table: most / fewest (8)
    stories = [
        ("Marbles", None, [34, 43, 29, 41], True, "Who has the most marbles?", "has the most marbles"),
        ("Books", ["Room 1", "Room 2", "Room 3", "Room 4"], [58, 61, 49, 56], True,
         "The table shows how many books each class read. Which class read the most books?", "read the most books"),
        ("Stickers", None, [72, 27, 31, 40], False, "Who has the fewest stickers?", "has the fewest stickers"),
        ("Shells", None, [60, 56, 65, 59], False, "Who found the fewest shells?", "found the fewest shells"),
        ("Points", ["Red team", "Blue team", "Green team", "Gold team"], [88, 79, 87, 80], True,
         "The table shows the points for each team. Which team got the most points?", "got the most points"),
        ("Apples", None, [45, 54, 39, 41], False, "Who picked the fewest apples?", "picked the fewest apples"),
        ("Cars", None, [70, 69, 59, 66], True, "Who has the most toy cars?", "has the most toy cars"),
        ("Pages", None, [93, 39, 90, 38], False, "Who read the fewest pages?", "read the fewest pages"),
    ]
    for head, names, nums, greatest, ask, verb in stories:
        names = names or [P.next()[0] for _ in range(4)]
        ex_, ans = list_expl(nums, greatest)
        who = names[nums.index(ans)]
        q = fig(table_svg(["Name" if head not in ("Books", "Points") else ("Class" if head == "Books" else "Team"), head],
                          list(zip(names, nums))))
        q += ask if names[0].startswith(("Room", "Red")) else "Look at the table. " + ask
        e = "Compare %s. %s So %s %s: %d." % (join(nums), ex_, "the " + who if who.endswith("team") else who, verb, ans)
        its.append(mcq(q, who, [n for n in names if n != who], e))
    # two numbers with a symbol (7)
    tpls = [("%s has %d marbles. %s has %d marbles. Which is true?", 46, 64, "%s has more marbles."),
            ("%s read %d books. %s read %d books. Which is true?", 51, 48, "%s read more books."),
            ("%s picked %d strawberries. %s picked %d strawberries. Which is true?", 37, 33, "%s picked more strawberries."),
            ("%s has %d blocks. %s has %d blocks. Which is true?", 29, 32, "%s has more blocks."),
            ("%s saw %d birds. %s saw %d birds. Which is true?", 15, 51, "%s saw more birds."),
            ("%s jumped rope %d times. %s jumped rope %d times. Which is true?", 80, 78, "%s jumped more times."),
            ("%s has %d stamps. %s has %d stamps. Which is true?", 62, 67, "%s has more stamps.")]
    for tpl, x, y, tail in tpls:
        A, B = P.next()[0], P.next()[0]
        op = sym(x, y)
        right = "%d %s %d" % (x, op, y)
        wrong = ["%d %s %d" % (x, LT if op == GT else GT, y), "%d = %d" % (x, y), "%d %s %d" % (y, op, x)]
        e = compare_e(x, y) + " " + tail % (A if x > y else B)
        its.append(mcq(tpl % (A, x, B, y), right, wrong, e))
    # equal (1)
    (A, she, _), (B, _, _) = P.next(), P.next()
    its.append(mcq("%s has 2 boxes with 10 crayons in each box. %s also has 7 more crayons. %s has 27 crayons. Which is true?"
                   % (A, she.capitalize(), B),
                   "They have the same number.", ["%s has more crayons." % A, "%s has more crayons." % B, "%s has 9 crayons." % A],
                   "2 boxes of 10 is 2 tens. With 7 more, %s has 2 tens and 7 ones: 27. %s also has 27. "
                   "27 = 27, so they have the same number. Do not count a box as 1." % (A, B)))
    # could have (4)
    p1, p2 = P.next(), P.next()
    p3 = P.next()
    sis = "sister" if p3[0] in BOYS else "brother"
    for q, n, more, right, wrong, unit in [
            ("%s has 52 stickers. %s has more stickers than %s. How many stickers could %s have?"
             % (p1[0], p2[0], p1[0], p2[0]), 52, True, 61, [25, 49, 52], "stickers"),
            ("%s has 45 toy cars. %s %s has fewer cars. How many cars could %s %s have?"
             % (p3[0], p3[2].capitalize(), sis, p3[2], sis), 45, False, 39, [54, 50, 45], "cars"),
            ("A red box has 70 beads. A blue box has fewer beads. How many beads could the blue box have?",
             70, False, 69, [70, 71, 80], "beads"),
            ("Room 2 read 38 books. Room 3 read more books. How many books could Room 3 have read?",
             38, True, 40, [29, 38, 19], "books")]:
        assert (right > n) if more else (right < n)
        assert all((w <= n) if more else (w >= n) for w in wrong)
        word = "More" if more else "Fewer"
        bad = [w for w in wrong if w != n]
        e = "%s than %d means %s than %d. %s %s %s %s than %d." % (
            word, n, "greater" if more else "less", n, compare_e(right, n),
            join(bad), "is" if len(bad) == 1 else "are", "less" if more else "greater", n)
        if n in wrong:
            e += " %d is the same number." % n
        its.append(mcq(q, right, wrong, e))
    return {"title": "Word problems", "items": its}


# ============================================================ lesson
def ex(title, q, s, a):
    return ("<div class='sn-ex'><span class='sn-ex-t'>%s</span><p class='sn-ex-q'>%s</p>"
            "<p class='sn-ex-s'>%s</p><p class='sn-ex-a'>Answer: %s</p></div>" % (title, q, s, a))


def table(head, rows):
    h = "".join("<th>%s</th>" % x for x in head)
    b = "".join("<tr>" + "".join("<td>%s</td>" % c for c in r) + "</tr>" for r in rows)
    return "<div class='sn-tw'><table class='sn-table'><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>" % (h, b)


def body_html():
    return (
        "<h2>Tens are worth more than ones</h2>"
        "<p>A two-digit number has <b>tens</b> and <b>ones</b>. One ten is the same as 10 ones. "
        "So the tens count the most. Always look at the tens first.</p>"
        "<figure class='sn-fig'>" + blocks_svg([31, 29]) +
        "<figcaption>A is 31: 3 tens and 1 one. B is 29: 2 tens and 9 ones. "
        "B has more pieces, but A has more tens. So 31 is greater.</figcaption></figure>"
        "<h2>Compare the tens, then the ones</h2>"
        "<ol class='rk-step'><li>Look at the <b>tens</b>. More tens means a greater number.</li>"
        "<li>Same tens? Look at the <b>ones</b>.</li>"
        "<li>Same tens and same ones? The numbers are <b>equal</b>.</li></ol>"
        "<figure class='sn-fig'>" + chart_svg([47, 42], hi="ones") +
        "<figcaption>Both have 4 tens. Look at the ones: 7 ones is more than 2 ones. So 47 is greater than 42.</figcaption></figure>" +
        ex("Example", "Compare 43 and 61.",
           "Look at the tens. 43 has 4 tens. 61 has 6 tens. 6 tens is more.", "43 is less than 61") +
        "<h2>The symbols &gt;, &lt; and =</h2>" +
        table(["Symbol", "Say", "Example"], [
            ["&gt;", "is greater than", "52 &gt; 25"],
            ["&lt;", "is less than", "29 &lt; 31"],
            ["=", "is equal to", "30 + 6 = 36"],
        ]) +
        "<p><b>The alligator trick:</b> think of &gt; and &lt; as a hungry alligator mouth. "
        "The mouth is open toward the <b>greater</b> number, because it wants to eat more. "
        "The small point faces the smaller number.</p>"
        "<figure class='sn-fig'>" + gator_svg(52, 25) +
        "<figcaption>Read from left to right: 52 is greater than 25, so 52 &gt; 25.</figcaption></figure>"
        "<p>On a number line, greater numbers are farther to the right.</p>"
        "<figure class='sn-fig'>" + numline_svg(20, 40, [(29, GREY), (31, GREEN)]) +
        "<figcaption>31 is to the right of 29, so 31 &gt; 29.</figcaption></figure>"
        "<h2>Common mistakes</h2>" +
        table(["Mistake", "What to do instead"], [
            ["Comparing the ones first: “29 &gt; 31, because 9 &gt; 1”", "Start with the tens: 2 tens &lt; 3 tens, so 29 &lt; 31"],
            ["Counting all the pieces: 29 has more blocks than 31", "A ten is worth 10 ones. Count tens first"],
            ["Thinking 36 and 63 are equal", "Same digits, different places: 36 &lt; 63"],
            ["Thinking 70 is like 7", "70 is 7 tens. 7 is 7 ones. 70 &gt; 7"],
            ["Turning the symbol the wrong way: 52 &lt; 25", "The open mouth faces the greater number: 52 &gt; 25"],
        ])
    )


FAQ = [
    {"q": "How do you compare two-digit numbers in 1st grade?",
     "a": "Look at the tens first; the number with more tens is greater. If the tens are the same, compare the ones, and if both are the same, the numbers are equal."},
    {"q": "What is the alligator trick for greater than and less than?",
     "a": "Think of > and < as an alligator mouth that always opens toward the greater number, because it wants to eat more. So 52 > 25 and 25 < 52."},
    {"q": "Why do kids think 29 is greater than 31?",
     "a": "They see the big 9 or count more pieces. But 29 has only 2 tens and 31 has 3 tens, so 29 < 31."},
    {"q": "Are 36 and 63 the same?",
     "a": "No. They use the same digits, but 36 is 3 tens and 6 ones, and 63 is 6 tens and 3 ones. So 36 < 63."},
]


def mark_large(u, pattern):
    """Tag pictures that must print larger so the blocks and tables stay readable."""
    rx = re.compile(r"<svg (?=[^>]*aria-label='(?:" + pattern + "))")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u


def gen():
    rnd = random.Random(106)
    P = People(rnd)
    used = {31, 29, 47, 42, 43, 61, 52, 25, 36, 63}
    sets = [set_blocks(rnd, used), set_places(rnd, used), set_symbols(rnd, used), set_order(rnd, used),
            set_words(rnd, used, P)]
    balance(sets, rnd)
    seen = set()
    for s in sets:
        assert len(s["items"]) == 20, (s["title"], len(s["items"]))
        assert sorted(it["a"] for it in s["items"]) == sorted([0, 1, 2, 3] * 5)
        for it in s["items"]:
            assert len(set(it["c"])) == 4, it
            k = it["q"] + "|" + "|".join(sorted(it["c"]))
            assert k not in seen, it["q"]
            seen.add(k)
    u = {
        "country": "us", "subject": "math", "grade": "grade-1", "slug": "compare-two-digit-numbers", "sort": 6,
        "updated": UPDATED, "pdf_url": "",
        "title": "Compare Two-Digit Numbers",
        "seo_title": "Grade 1 Comparing Two-Digit Numbers Worksheets: Greater Than, Less Than and Equal To",
        "short_title": "Compare two-digit numbers",
        "domain": "Number and Operations in Base Ten",
        "standard_code": "1.NBT.B.3",
        "standard_url": "https://www.thecorestandards.org/Math/Content/1/NBT/B/3/",
        "standard_text": "Compare two two-digit numbers based on meanings of the tens and ones digits, recording the results of comparisons with the symbols >, =, and <.",
        "meta_desc": "Free 1st grade comparing numbers worksheets: compare two-digit numbers with tens and ones blocks, use the >, < and = symbols with the alligator trick, find the greatest and least, and solve word problems. 100 questions with an answer key.",
        "key_big": "Look at the tens first. If the tens are the same, compare the ones.",
        "key_sub": "31 > 29, because 3 tens is more than 2 tens. The open mouth of > and < faces the greater number.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }
    return mark_large(u, "tens and ones blocks|table of")


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
