# -*- coding: utf-8 -*-
"""
US Grade 2 Math: Compare Three-Digit Numbers (2.NBT.A.4)
  python tools/gen_us_math_g2_compare.py
All numbers are 100-999. Every comparison, order and "only one choice works" is checked in code.
HTML attributes use single quotes (no backslashes in the JSON). In HTML, > and < are written &gt; and &lt;.
"""
import json, os, random, re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "us", "math", "grade-2")
UPDATED = "2026-11-02"
GREEN = "#006633"
FILL = "#cfe6d6"
RED = "#c0392b"
INK = "#2b2b2b"
FONT = "Arial, Helvetica, sans-serif"
GIRLS = ["Maya", "Ava", "Mia", "Zoe", "Lily", "Emma", "Nora", "Ruby", "Sofia", "Grace"]
BOYS = ["Leo", "Noah", "Eli", "Sam", "Ben", "Omar", "Kai", "Jack", "Luis", "Owen"]

PL1 = ["one", "ten", "hundred"]
GT, LT = "&gt;", "&lt;"


# ------------------------------------------------------------ math and words
def digit(n, i):
    return (n // 10 ** i) % 10


def first_diff(a, b):
    for i in (2, 1, 0):
        if digit(a, i) != digit(b, i):
            return i
    return None


def pl(d, i):
    """3 hundreds, 1 ten, 0 ones."""
    return "%d %s%s" % (d, PL1[i], "" if d == 1 else "s")


def hto(n):
    return "%s, %s and %s" % (pl(digit(n, 2), 2), pl(digit(n, 1), 1), pl(digit(n, 0), 0))


def sym(a, b):
    return GT if a > b else (LT if a < b else "=")


def rel(a, b):
    return "%d %s %d" % (a, sym(a, b), b)


def join(xs):
    xs = [str(x) for x in xs]
    return xs[0] if len(xs) == 1 else ", ".join(xs[:-1]) + " and " + xs[-1]


def expanded(n):
    return " + ".join(str(digit(n, i) * 10 ** i) for i in (2, 1, 0) if digit(n, i))


def compare_e(x, y):
    """Hundreds first, then tens, then ones. Ends with 'so x > y' in the order given."""
    i = first_diff(x, y)
    if i == 2:
        s = "Look at the hundreds first. "
    elif i == 1:
        s = "Both have %s. Look at the tens next. " % pl(digit(x, 2), 2)
    else:
        s = "Both have %s and %s. Look at the ones. " % (pl(digit(x, 2), 2), pl(digit(x, 1), 1))
    dx, dy = digit(x, i), digit(y, i)
    s += "%d has %s and %d has %s. %d %s %d, so %s." % (x, pl(dx, i), y, pl(dy, i), dx, sym(dx, dy), dy, rel(x, y))
    big, small = max(x, y), min(x, y)
    if i == 2 and digit(small, 1) > digit(big, 1):
        s += " The tens and ones do not matter."
    elif i == 1 and digit(small, 0) > digit(big, 0):
        s += " The ones do not matter."
    return s


def list_expl(nums, greatest):
    """Find the greatest (or least) number: hundreds, then tens, then ones."""
    cur = list(nums)
    out = []
    for i, name in ((2, "Hundreds"), (1, "Tens"), (0, "Ones")):
        ds = [digit(n, i) for n in cur]
        best = max(ds) if greatest else min(ds)
        if len(set(ds)) == 1:
            out.append("%s %s." % ("Both have" if len(cur) == 2 else "All of them have", pl(best, i)))
            continue
        if len(cur) == len(nums):
            out.append("%s%s: %s. %d is the %s." % (name, " first" if i == 2 else "", join(ds), best,
                                                   "biggest" if greatest else "smallest"))
        else:
            out.append("%s of %s: %s. %d is the %s." % (name, join(cur), join(ds), best, "biggest" if greatest else "smallest"))
        cur = [n for n in cur if digit(n, i) == best]
        if len(cur) == 1:
            break
    assert len(cur) == 1
    return " ".join(out), cur[0]


def lt_reason(a, b):
    """a < b with the reason in brackets."""
    i = first_diff(a, b)
    return "%d &lt; %d (%s &lt; %s)" % (a, b, pl(digit(a, i), i), pl(digit(b, i), i))


def gt_reason(a, b):
    i = first_diff(a, b)
    return "%d &gt; %d (%s &gt; %s)" % (a, b, pl(digit(a, i), i), pl(digit(b, i), i))


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
U = 8              # one small cube
FLAT = 10 * U      # a flat is 10 by 10 cubes
FGAP, RGAP, CGAP, GGAP = 6, 4, 4, 14
LAB = 28           # space for the letter A or B


def blocks_w(n):
    h, t, o = digit(n, 2), digit(n, 1), digit(n, 0)
    parts = []
    if h:
        parts.append(h * FLAT + (h - 1) * FGAP)
    if t:
        parts.append(t * U + (t - 1) * RGAP)
    if o:
        cols = (o + 4) // 5
        parts.append(cols * U + (cols - 1) * CGAP)
    return sum(parts) + GGAP * (len(parts) - 1)


def blocks_row(n, x0, y0):
    """Base-ten blocks for n: flats (hundreds), rods (tens), small cubes (ones). Height = FLAT."""
    h, t, o = digit(n, 2), digit(n, 1), digit(n, 0)
    s = []
    x = x0
    for k in range(h):
        s.append("<rect x='%d' y='%d' width='%d' height='%d' fill='%s' stroke='%s' stroke-width='1.6'/>"
                 % (x, y0, FLAT, FLAT, FILL, GREEN))
        for j in range(1, 10):
            s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='0.6'/>"
                     % (x + j * U, y0, x + j * U, y0 + FLAT, GREEN))
            s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='0.6'/>"
                     % (x, y0 + j * U, x + FLAT, y0 + j * U, GREEN))
        x += FLAT + (FGAP if k < h - 1 else 0)
    if h and (t or o):
        x += GGAP
    for k in range(t):
        s.append("<rect x='%d' y='%d' width='%d' height='%d' fill='%s' stroke='%s' stroke-width='1.4'/>"
                 % (x, y0, U, FLAT, FILL, GREEN))
        for j in range(1, 10):
            s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='0.6'/>"
                     % (x, y0 + j * U, x + U, y0 + j * U, GREEN))
        x += U + (RGAP if k < t - 1 else 0)
    if t and o:
        x += GGAP
    for k in range(o):
        col, row = divmod(k, 5)
        cx = x + col * (U + CGAP)
        cy = y0 + FLAT - U - row * (U + CGAP)          # stack from the bottom
        s.append("<rect x='%d' y='%d' width='%d' height='%d' fill='%s' stroke='%s' stroke-width='1.4'/>"
                 % (cx, cy, U, U, FILL, GREEN))
    return "".join(s)


def blocks_svg(nums, letters=True):
    """One row of blocks per number. With letters, each row is labeled A, B, ..."""
    m = 6
    lab = LAB if letters else 0
    rowgap = 22
    W = 2 * m + lab + max(blocks_w(n) for n in nums)
    H = 2 * m + len(nums) * FLAT + (len(nums) - 1) * rowgap
    s = []
    for r, n in enumerate(nums):
        y = m + r * (FLAT + rowgap)
        if letters:
            s.append(text(m + 9, y + FLAT / 2 + 7, "ABCD"[r], 20, col=INK, wt=800))
        s.append(blocks_row(n, m + lab, y))
        if letters and r:
            yl = y - rowgap / 2
            s.append("<line x1='%d' y1='%.1f' x2='%d' y2='%.1f' stroke='#b9b2a8' stroke-width='1' stroke-dasharray='4 3'/>"
                     % (m, yl, W - m, yl))
    label = ("base-ten blocks for " + join(nums)) if letters else "base-ten blocks for %d" % nums[0]
    return svg_wrap(W, H, "".join(s), label)


CW, HEAD, ROW = 84, 34, 46


def chart_svg(nums, hi=None):
    """Hundreds-tens-ones chart with one number per row. hi = place index whose digits are red."""
    x0, y0 = 6, 6
    W = 2 * x0 + 3 * CW
    H = 2 * y0 + HEAD + ROW * len(nums)
    s = ["<rect x='%d' y='%d' width='%d' height='%d' fill='#fff' stroke='%s' stroke-width='2'/>"
         % (x0, y0, 3 * CW, HEAD + ROW * len(nums), GREEN),
         "<rect x='%d' y='%d' width='%d' height='%d' fill='%s'/>" % (x0, y0, 3 * CW, HEAD, FILL)]
    for k, name in enumerate(["Hundreds", "Tens", "Ones"]):
        i = 2 - k
        x = x0 + k * CW
        if k:
            s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='1.5'/>"
                     % (x, y0, x, y0 + HEAD + ROW * len(nums), GREEN))
        s.append(text(x + CW / 2, y0 + 23, name, 15))
        for r, n in enumerate(nums):
            s.append(text(x + CW / 2, y0 + HEAD + r * ROW + 34, str(digit(n, i)), 28,
                          col=RED if hi == i else INK, wt=800))
    for r in range(len(nums)):
        y = y0 + HEAD + r * ROW
        s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='%s'/>"
                 % (x0, y, x0 + 3 * CW, y, GREEN, "2" if r == 0 else "1"))
    return svg_wrap(W, H, "".join(s), "place-value chart showing " + join(nums))


def symbol_svg():
    """452 > 425 with the open side toward the greater number."""
    W, H = 300, 118
    s = [text(150, 20, "open side", 15, col=RED),
         "<path d='M 128 28 L 136 40' stroke='%s' stroke-width='2' fill='none'/>" % RED,
         "<path d='M 129 36 L 136 40 L 136 32' stroke='%s' stroke-width='2' fill='none'/>" % RED,
         text(70, 72, "452", 34, wt=800), text(150, 74, "&gt;", 44, col=RED, wt=800), text(230, 72, "425", 34, wt=800),
         text(70, 104, "greater", 16, col=GREEN), text(230, 104, "less", 16, col="#6b6259")]
    return svg_wrap(W, H, "".join(s), "452 is greater than 425")


# ------------------------------------------------------------ number makers
def make_pair(rnd, place, kind, used, hmax=4):
    """(big, small): three-digit numbers that first differ at `place`.
    kind: plain | trap (the smaller one has bigger digits after) | swap (452 / 425) | zero (450 / 405)."""
    for _ in range(5000):
        if place == 2:
            hb = rnd.randint(2, hmax)
            hs = rnd.randint(1, hb - 1)
            if kind == "trap":
                hs = hb - 1
                big = hb * 100 + rnd.randint(0, 3) * 10 + rnd.randint(0, 4)
                small = hs * 100 + rnd.randint(7, 9) * 10 + rnd.randint(5, 9)
            else:
                big = hb * 100 + rnd.randint(0, 9) * 10 + rnd.randint(0, 9)
                small = hs * 100 + rnd.randint(0, 9) * 10 + rnd.randint(0, 9)
        elif place == 1:
            h = rnd.randint(1, hmax)
            if kind == "swap":
                t, o = rnd.sample(range(1, 10), 2)
                t, o = max(t, o), min(t, o)
                big, small = h * 100 + t * 10 + o, h * 100 + o * 10 + t
            elif kind == "zero":
                t = rnd.randint(1, 9)
                big, small = h * 100 + t * 10, h * 100 + t
            else:
                tb = rnd.randint(1, 9)
                ts = rnd.randint(0, tb - 1)
                if kind == "trap":
                    ob = rnd.randint(0, 5)
                    os_ = rnd.randint(ob + 3, 9) if ob + 3 <= 9 else 9
                else:
                    ob, os_ = rnd.randint(0, 9), rnd.randint(0, 9)
                big, small = h * 100 + tb * 10 + ob, h * 100 + ts * 10 + os_
        else:
            h, t = rnd.randint(1, hmax), rnd.randint(0, 9)
            ob = rnd.randint(1, 9)
            os_ = rnd.randint(0, ob - 1)
            big, small = h * 100 + t * 10 + ob, h * 100 + t * 10 + os_
        if big <= small or first_diff(big, small) != place or big in used or small in used:
            continue
        pieces = lambda n: digit(n, 2) + digit(n, 1) + digit(n, 0)
        if place == 2 and kind == "trap" and not (digit(small, 1) > digit(big, 1) and pieces(small) > pieces(big)):
            continue
        if max(blocks_w(big), blocks_w(small)) > 440:
            continue
        used.update([big, small])
        return big, small
    raise RuntimeError("no pair")


def make_number(rnd, used, hmax=4):
    for _ in range(5000):
        n = rnd.randint(2, hmax) * 100 + rnd.randint(1, 8) * 10 + rnd.randint(1, 8)
        if n not in used and digit(n, 1) != digit(n, 0) and blocks_w(n) <= 440:
            used.add(n)
            return n
    raise RuntimeError("no number")


def beyond(n, want, rnd):
    """One number greater (want='gt') or less (want='lt') than n, and 3 tempting numbers on the wrong side."""
    h, t, o = digit(n, 2), digit(n, 1), digit(n, 0)
    if want == "gt":
        right = h * 100 + (t + 1) * 10 + rnd.randint(0, o - 1) if t < 9 else (h + 1) * 100 + rnd.randint(0, 3) * 10 + rnd.randint(0, 3)
        wrong = [h * 100 + (t - 1) * 10 + 9 if t else None,             # bigger ones digit, fewer tens
                 (h - 1) * 100 + 90 + rnd.randint(max(o, 5), 9) if h > 1 else None,   # big digits, fewer hundreds
                 h * 100 + o * 10 + t if o < t else None,                # tens and ones swapped
                 n,                                                      # the same number is not greater
                 (h - 1) * 100 + t * 10 + o + 10 if h > 1 and t < 9 else None]   # one more ten, one fewer hundred
    else:
        right = h * 100 + (t - 1) * 10 + rnd.randint(o + 1, 9) if t and o < 9 else (h - 1) * 100 + 90 + rnd.randint(5, 9)
        wrong = [h * 100 + o * 10 + t if o > t else None,                # tens and ones swapped
                 h * 100 + (t + 1) * 10 if t < 9 else None,              # ones digit 0 looks small
                 (h + 1) * 100 + rnd.randint(0, 2) * 10 + rnd.randint(0, 2) if h < 9 else None,  # small digits, more hundreds
                 n]
    wrong = [w for w in wrong if w is not None and 100 <= w <= 999]
    wrong = [w for k, w in enumerate(wrong) if w not in wrong[:k]]
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


# ============================================================ set 1: base-ten blocks
def set_blocks(rnd, used):
    its = []
    specs = [(2, "plain"), (1, "plain"), (2, "trap"), (0, "plain"), (1, "swap"), (2, "trap"),
             (1, "trap"), (1, "zero"), (2, "plain"), (0, "plain"), (2, "trap"), (1, "trap")]
    for k, (place, kind) in enumerate(specs):
        big, small = make_pair(rnd, place, kind, used)
        a, b = (big, small) if k % 2 == 0 else (small, big)
        op = sym(a, b)
        right = "%d %s %d" % (a, op, b)
        wrong = ["%d %s %d" % (a, LT if op == GT else GT, b), "%d = %d" % (a, b), "%d %s %d" % (b, op, a)]
        e = "A has %s: %d. B has %s: %d. " % (hto(a), a, hto(b), b) + compare_e(a, b)
        if place == 2 and kind == "trap":
            e += " %d has more blocks, but 1 flat (100) is more than 9 rods and 9 cubes (99)." % min(a, b)
        its.append(mcq(fig(blocks_svg([a, b])) + "Write the number for A and for B. Which is true?", right, wrong, e))
    for k in range(8):
        want = "gt" if k % 2 == 0 else "lt"
        n = make_number(rnd, used)
        right, wrong = beyond(n, want, rnd)
        e = "The blocks show %s: %d. " % (hto(n), n) + compare_e(right, n) + others_e(n, want, wrong)
        q = fig(blocks_svg([n], letters=False)) + "Which number is %s than the number shown?" % (
            "greater" if want == "gt" else "less")
        its.append(mcq(q, right, wrong, e))
    return {"title": "Compare with base-ten blocks", "items": its}


# ============================================================ set 2: hundreds, then tens, then ones
PLACES = ["the ones", "the tens", "the hundreds"]


def set_places(rnd, used):
    its = []
    for place, kind in [(2, "trap"), (1, "plain"), (0, "plain"), (1, "zero"), (2, "plain"), (1, "trap")]:
        big, small = make_pair(rnd, place, kind, used, hmax=9)
        top, bot = (big, small) if rnd.random() < 0.5 else (small, big)
        e = compare_e(top, bot) + " So %s tell you which number is greater." % PLACES[place]
        its.append(mcq(fig(chart_svg([top, bot])) + "Which place tells you which number is greater?",
                       PLACES[place], [p for p in PLACES if p != PLACES[place]] + ["the biggest digit"], e))
    for k in range(6):
        want = "gt" if k % 2 else "lt"
        n = make_number(rnd, used, hmax=8)
        right, wrong = beyond(n, want, rnd)
        e = "The chart shows %d. " % n + compare_e(right, n) + others_e(n, want, wrong)
        its.append(mcq(fig(chart_svg([n])) + "Which number is %s than the number in the chart?"
                       % ("greater" if want == "gt" else "less"), right, wrong, e))
    for nums, greatest in [([452, 425, 399, 405], True), ([738, 783, 837, 709], False),
                           ([610, 601, 599, 160], True), ([264, 246, 300, 290], False)]:
        ex_, ans = list_expl(nums, greatest)
        e = "The numbers are %s. %s So %d is the %s." % (join(nums), ex_, ans, "greatest" if greatest else "least")
        its.append(mcq("Which number is the %s?" % ("greatest" if greatest else "least"), expanded(ans),
                       [expanded(v) for v in nums if v != ans], e))
    for words, greatest in [
            ([(5, 1, 0), (4, 9, 0), (1, 9, 0), (5, 0, 1)], True),
            ([(3, 2, 0), (2, 9, 0), (3, 0, 2), (2, 0, 9)], False),
            ([(7, 0, 4), (6, 9, 0), (7, 4, 0), (4, 7, 0)], True),
            ([(8, 6, 0), (6, 8, 0), (8, 0, 6), (6, 0, 8)], False)]:
        nums = [h * 100 + t * 10 + o for h, t, o in words]
        say = lambda h, t, o: " ".join([pl(h, 2)] + ([pl(t, 1)] if t else []) + ([pl(o, 0)] if o else []))
        texts = [say(*w) for w in words]
        ex_, ans = list_expl(nums, greatest)
        e = "Write each one as a number: %s. %s So %s (%d) is the %s." % (
            join(nums), ex_, texts[nums.index(ans)], ans, "greatest" if greatest else "least")
        its.append(mcq("Which is the %s?" % ("greatest" if greatest else "least"), texts[nums.index(ans)],
                       [t for t, v in zip(texts, nums) if v != ans], e))
    return {"title": "Compare hundreds, then tens, then ones", "items": its}


# ============================================================ set 3: the symbols >, < and =
def parse(s):
    a, op, b = s.replace("&gt;", ">").replace("&lt;", "<").split(" ")
    a, b = int(a), int(b)
    return {">": a > b, "<": a < b, "=": a == b}[op]


def set_symbols(rnd, used):
    its = []
    pairs = [(452, 425), (405, 450), (199, 301), (362, 326), (587, 584), (639, 671), (812, 218), (780, 708)]
    for x, y in pairs:
        op = sym(x, y)
        right = "%d %s %d" % (x, op, y)
        wrong = ["%d %s %d" % (x, LT if op == GT else GT, y), "%d = %d" % (x, y), "%d %s %d" % (y, op, x)]
        e = compare_e(x, y)
        if 0 in (digit(x, 1), digit(y, 1)) and first_diff(x, y) == 1:
            e += " A 0 in the tens place means no tens."
        its.append(mcq("Compare %d and %d. Which is true?" % (x, y), right, wrong, e))
    its.append(mcq("Which is true?", "500 + 7 = 507", ["500 + 7 = 570", "500 + 7 &gt; 507", "500 + 7 &lt; 507"],
                   "500 + 7 is 5 hundreds and 7 ones. There are no tens, so write 0 in the tens place: 507. "
                   "The two sides are the same number, so use =."))
    its.append(mcq("Which number makes this true? 4 hundreds 6 ones = ☐", "406", ["460", "46", "604"],
                   "4 hundreds and 6 ones, with no tens. Write 0 in the tens place: 406. "
                   "460 has 6 tens, not 6 ones. 46 has no hundreds."))
    for q, right, wrong, e in [
            ("Which number makes this true? ☐ &lt; 506", 498, [560, 605, 510],
             "☐ &lt; 506 means the box is less than 506. 498 has 4 hundreds and 506 has 5 hundreds, so 498 &lt; 506. "
             "560, 605 and 510 are all greater than 506."),
            ("Which number makes this true? ☐ &gt; 739", 741, [739, 709, 397],
             "☐ &gt; 739 means the box is greater than 739. Both have 7 hundreds. 741 has 4 tens and 739 has 3 tens, so 741 &gt; 739. "
             "739 is the same number, not greater. 709 and 397 are less."),
            ("Which number makes this true? 283 &lt; ☐", 300, [238, 280, 199],
             "283 &lt; ☐ means the box is greater than 283. 300 has 3 hundreds and 283 has 2 hundreds, so 283 &lt; 300. "
             "238, 280 and 199 are all less than 283.")]:
        ok = [v for v in [right] + wrong if eval(q.split("? ")[1].replace("☐", str(v)).replace("&lt;", "<").replace("&gt;", ">"))]
        assert ok == [right], q
        its.append(mcq(q, right, wrong, e))
    for x, y in [(718, 781), (640, 604)]:
        w = "greater than" if x > y else "less than"
        o = "less than" if x > y else "greater than"
        its.append(mcq("What does %s mean?" % rel(x, y), "%d is %s %d" % (x, w, y),
                       ["%d is %s %d" % (x, o, y), "%d is %s %d" % (y, w, x), "%d is equal to %d" % (x, y)],
                       "Read from left to right. %s means “greater than” and %s means “less than”. "
                       "Both have %s. %s, because %s." % (GT, LT, pl(digit(x, 2), 2), rel(x, y),
                                           "%s &gt; %s" % (pl(digit(x, 1), 1), pl(digit(y, 1), 1)) if x > y else
                                           "%s &lt; %s" % (pl(digit(x, 1), 1), pl(digit(y, 1), 1)))))
    its.append(mcq("Which shows “three hundred five is less than three hundred fifty”?", "305 &lt; 350",
                   ["305 &gt; 350", "350 &lt; 305", "305 = 350"],
                   "Three hundred five is 305. Three hundred fifty is 350. “Less than” is &lt;. "
                   "305 &lt; 350, because 0 tens &lt; 5 tens."))
    for right, wrong in [("541 &gt; 514", ["199 &gt; 301", "450 &lt; 405", "362 &lt; 326"]),
                         ("608 &lt; 680", ["290 &gt; 302", "735 &lt; 729", "814 &gt; 841"]),
                         ("479 &lt; 497", ["389 &gt; 401", "560 &lt; 506", "932 &lt; 923"]),
                         ("700 &gt; 699", ["599 &gt; 600", "870 &lt; 807", "246 &gt; 264"])]:
        assert parse(right) and not any(parse(w) for w in wrong), right
        a, _, b = right.split(" ")
        nots = []
        for w in wrong:
            x, _, y = w.split(" ")
            x, y = int(x), int(y)
            i = first_diff(x, y)
            nots.append("%s (%s %s %s)" % (w, pl(digit(x, i), i), sym(x, y), pl(digit(y, i), i)))
        e = compare_e(int(a), int(b)) + " Not true: " + "; ".join(nots) + "."
        its.append(mcq("Which comparison is true?", right, wrong, e))
    return {"title": "Use the symbols >, < and =", "items": its}


# ============================================================ set 4: order and between
def set_order(rnd, used):
    its = []
    triples = [((352, 235, 325), True), ((481, 399, 418), True), ((450, 504, 405), True),
               ((726, 762, 672), True), ((190, 109, 901), True), ((843, 834, 438), True),
               ((617, 671, 716), False), ((299, 302, 320), False), ((580, 508, 585), False),
               ((936, 699, 963), False), ((140, 104, 401), False)]
    for given, up in triples:
        order = sorted(given) if up else sorted(given, reverse=True)
        assert list(given) != order
        f = lambda l: ", ".join(str(v) for v in l)
        ones_first = sorted(given, key=lambda v: str(v)[::-1], reverse=not up)   # compared from the right
        cands = [order[::-1], ones_first, [order[1], order[0], order[2]], [order[0], order[2], order[1]], list(given)]
        asc = sorted(given)
        if up:
            e = "%s, and %s. " % (lt_reason(asc[0], asc[1]), lt_reason(asc[1], asc[2]))
        else:
            e = "%s, and %s. " % (gt_reason(asc[2], asc[1]), gt_reason(asc[1], asc[0]))
        e += "So from %s: %s." % ("least to greatest" if up else "greatest to least", f(order))
        q = "Put %s in order from %s." % (join(given), "least to greatest" if up else "greatest to least")
        its.append(mcq(q, f(order), [f(c) for c in cands if c != order], e))
    for lo, hi, right, wrong in [(340, 380, 362, [326, 386, 304]), (600, 700, 659, [596, 706, 560]),
                                 (415, 451, 432, [413, 454, 405]), (798, 803, 800, [789, 830, 808]),
                                 (199, 210, 205, [250, 190, 211])]:
        assert lo < right < hi and not any(lo < w < hi for w in wrong)
        outs = ", ".join("%s" % rel(w, lo if w < lo else hi) for w in wrong)
        e = ("Check both sides: %d &lt; %d and %d &lt; %d. So %d is between them. The others are outside: %s."
             % (lo, right, right, hi, right, outs))
        its.append(mcq("Which number is between %d and %d?" % (lo, hi), right, wrong, e))
    for nums, greatest in [([689, 698, 869, 896], True), ([503, 530, 350, 305], False),
                           ([799, 801, 810, 789], True), ([212, 221, 211, 222], False)]:
        ex_, ans = list_expl(nums, greatest)
        its.append(mcq("Which number is the %s: %s?" % ("greatest" if greatest else "least", join(nums).replace(" and", ",")),
                       ans, [v for v in nums if v != ans], ex_ + " So %d is the %s." % (ans, "greatest" if greatest else "least")))
    return {"title": "Put numbers in order", "items": its}


# ============================================================ set 5: word problems and missing digits
def set_words(rnd, used, P):
    its = []
    # which sentence is true (3)
    for intro, xa, xb, choices, e_tail in [
            ("A red bag has %d beads. A blue bag has %d beads. Which is true?", 516, 561,
             ["The red bag has fewer.", "The blue bag has fewer.", "They have the same number.", "The red bag has more."],
             "So the red bag has fewer beads."),
            ("A train has %d seats. A plane has %d seats. Which is true?", 408, 480,
             ["The plane has more seats.", "The train has more seats.", "They have the same number.", "The plane has fewer seats."],
             "So the plane has more seats."),
            ("On Monday, %d people came to the zoo. On Tuesday, %d people came. Which is true?", 937, 973,
             ["More people came on Tuesday.", "More people came on Monday.", "The same number came each day.",
              "Fewer people came on Tuesday."],
             "So more people came on Tuesday.")]:
        its.append(mcq(intro % (xa, xb), choices[0], choices[1:], compare_e(xa, xb) + " " + e_tail))
    # could have (4)
    for k, (tpl, n, more, right, wrong, unit) in enumerate([
            ("%s has %d stickers. %s has fewer stickers than %s. How many stickers could %s have?", 452, False, 449, [524, 460, 452], "stickers"),
            ("A red book has %d pages. A blue book has more pages. How many pages could the blue book have?", 315, True, 351, [153, 309, 315], "pages"),
            ("%s's team scored %d points. The other team scored fewer points. How many points could the other team have?", 608, False, 599, [680, 806, 610], "points"),
            ("A school has %d students. Another school has more students. How many students could that school have?", 740, True, 802, [704, 470, 740], "students")]):
        assert (right > n) if more else (right < n)
        assert all((w <= n) if more else (w >= n) for w in wrong)
        if k == 0:
            a, _, _ = P.next()
            b, _, _ = P.next()
            q = tpl % (a, n, b, a, b)
        elif k == 2:
            a, _, _ = P.next()
            q = tpl % (a, n)
        else:
            q = tpl % n
        word = "More" if more else "Fewer"
        bad = [w for w in wrong if w != n]
        e = "%s than %d means %s than %d. %s %s %s %s." % (
            word, n, "greater" if more else "less", n, compare_e(right, n),
            join(bad), "is" if len(bad) == 1 else "are", "less" if more else "greater")
        if n in wrong:
            e += " %d is the same number." % n
        its.append(mcq(q, right, wrong, e))
    # most / fewest of four (5)
    def names4():
        return [P.next()[0] for _ in range(4)]
    stories = [
        ("Four friends played a game. %s got %d points. %s got %d points. %s got %d points. %s got %d points. Who got the most points?",
         None, [342, 324, 299, 304], True, "got the most points"),
        ("Four classes collected cans. %s collected %d cans. %s collected %d cans. %s collected %d cans. %s collected %d cans. "
         "Which class collected the fewest cans?", ["Room 1", "Room 2", "Room 3", "Room 4"], [418, 408, 480, 410], False,
         "collected the fewest cans"),
        ("Four kids counted the pages they read this year. %s read %d pages. %s read %d pages. %s read %d pages. "
         "%s read %d pages. Who read the most pages?", None, [506, 499, 550, 560], True, "read the most pages"),
        ("%s has %d beads. %s has %d beads. %s has %d beads. %s has %d beads. Which bag has the fewest beads?",
         ["Bag A", "Bag B", "Bag C", "Bag D"], [263, 326, 236, 362], False, "has the fewest beads"),
        ("Four farms picked apples. %s picked %d apples. %s picked %d apples. %s picked %d apples. %s picked %d apples. "
         "Which farm picked the most apples?", ["Hill Farm", "Oak Farm", "Sun Farm", "Lake Farm"], [709, 790, 779, 797], True,
         "picked the most apples"),
    ]
    for tpl, names, nums, greatest, verb in stories:
        names = names or names4()
        q = tpl % tuple(x for pair in zip(names, nums) for x in pair)
        ex_, ans = list_expl(nums, greatest)
        who = names[nums.index(ans)]
        e = "Compare %s. %s So %s %s: %d." % (join(nums), ex_, who, verb, ans)
        its.append(mcq(q, who, [n for n in names if n != who], e))
    # make a number from digits (3)
    for ds, greatest in [((3, 8, 1), True), ((6, 2, 9), False), ((5, 0, 7), False)]:
        s = sorted(ds, reverse=greatest)
        if not greatest and s[0] == 0:
            s[0], s[1] = s[1], s[0]
        ans = int("".join(map(str, s)))
        perms = sorted({int("%d%d%d" % p) for p in [(a, b, c) for a in ds for b in ds for c in ds if len({a, b, c}) == 3] if p[0]})
        assert ans == (max(perms) if greatest else min(perms))
        if greatest:
            wrong = [int("%d%d%d" % (s[0], s[2], s[1])), int("%d%d%d" % tuple(s[::-1])), int("%d%d%d" % (s[1], s[0], s[2]))]
            e = ("Put the biggest digit in the hundreds place, the next biggest in the tens place, and the smallest in the ones place: "
                 "%d, %d, %d. The greatest number is %d." % (s[0], s[1], s[2], ans))
        elif 0 in ds:
            wrong = [570, 705, 750]
            e = ("A three-digit number cannot start with 0. Put the smallest digit that is not 0 in the hundreds place: 5. "
                 "Then put 0 in the tens place and 7 in the ones place. The least number is 507.")
        else:
            wrong = [int("%d%d%d" % (s[0], s[2], s[1])), int("%d%d%d" % tuple(s[::-1])), int("%d%d%d" % (s[1], s[0], s[2]))]
            e = ("Put the smallest digit in the hundreds place, the next smallest in the tens place, and the biggest in the ones place: "
                 "%d, %d, %d. The least number is %d." % (s[0], s[1], s[2], ans))
        assert all(w in perms for w in wrong)
        q = "What is the %s number you can make with the digits %s? Use each digit once." % (
            "greatest" if greatest else "least", join(ds))
        its.append(mcq(q, ans, wrong, e))
    # missing digit (5): only one choice works
    for pat, op, other, right, wrong in [("4☐7", ">", 462, 8, [5, 3, 1]), ("☐56", "<", 482, 3, [5, 6, 8]),
                                         ("73☐", ">", 736, 9, [6, 5, 3]), ("5☐1", "<", 529, 0, [3, 4, 9]),
                                         ("☐08", ">", 780, 8, [7, 6, 1])]:
        val = lambda d: int(pat.replace("☐", str(d)))
        test = lambda d: val(d) > other if op == ">" else val(d) < other
        assert test(right) and not any(test(w) for w in wrong), pat
        ops = GT if op == ">" else LT
        e = "Try %d in the box: %d. %s So %d works. " % (right, val(right), compare_e(val(right), other), right)
        e += "The other digits make %s, and none of them is %s than %d." % (
            join(val(w) for w in wrong), "greater" if op == ">" else "less", other)
        its.append(mcq("Which digit can go in the box? %s %s %d" % (pat, ops, other), right, wrong, e))
    return {"title": "Word problems and missing digits", "items": its}


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
        "<h2>Hundreds are worth the most</h2>"
        "<p>A three-digit number has <b>hundreds</b>, <b>tens</b> and <b>ones</b>. One hundred is the same as 10 tens. "
        "So the hundreds count the most. Always look at the hundreds first.</p>"
        "<figure class='sn-fig'>" + blocks_svg([301, 299]) +
        "<figcaption>A is 301: 3 hundreds and 1 one. B is 299: 2 hundreds, 9 tens and 9 ones. "
        "B has more blocks, but A has more hundreds. So 301 is greater.</figcaption></figure>"
        "<h2>Compare hundreds, then tens, then ones</h2>"
        "<ol class='rk-step'><li>Look at the <b>hundreds</b>. More hundreds means a greater number.</li>"
        "<li>Same hundreds? Look at the <b>tens</b>.</li>"
        "<li>Same tens too? Look at the <b>ones</b>.</li></ol>"
        "<figure class='sn-fig'>" + chart_svg([452, 425], hi=1) +
        "<figcaption>Both have 4 hundreds. Look at the tens: 5 tens is more than 2 tens. So 452 is greater than 425.</figcaption></figure>" +
        ex("Example", "Compare 405 and 450.",
           "Both have 4 hundreds. Tens: 405 has 0 tens and 450 has 5 tens. 0 is less than 5.", "405 is less than 450") +
        "<h2>The symbols &gt;, &lt; and =</h2>" +
        table(["Symbol", "Say", "Example"], [
            ["&gt;", "is greater than", "452 &gt; 425"],
            ["&lt;", "is less than", "405 &lt; 450"],
            ["=", "is equal to", "500 + 7 = 507"],
        ]) +
        "<p><b>Tip:</b> the <b>open side</b> of &gt; and &lt; always faces the <b>greater</b> number. "
        "The point faces the smaller number.</p>"
        "<figure class='sn-fig'>" + symbol_svg() +
        "<figcaption>Read from left to right: 452 is greater than 425. The open side is next to 452.</figcaption></figure>"
        "<h2>Put numbers in order</h2>"
        "<p>Compare two numbers at a time. Find the least one first, then the next, then the greatest.</p>" +
        ex("Example", "Put 352, 235 and 325 in order from least to greatest.",
           "235 has only 2 hundreds, so it is the least. 325 and 352 both have 3 hundreds. Tens: 2 &lt; 5, so 325 &lt; 352.",
           "235, 325, 352") +
        "<h2>Common mistakes</h2>" +
        table(["Mistake", "What to do instead"], [
            ["Comparing the ones first: “362 &lt; 326, because 2 &lt; 6”", "Start with the hundreds, then the tens: 362 &gt; 326"],
            ["Thinking big digits win: “199 &gt; 301”", "Hundreds first: 1 hundred &lt; 3 hundreds, so 199 &lt; 301"],
            ["Skipping a zero: “405 is the same as 450”", "405 has 0 tens; 450 has 5 tens. 405 &lt; 450"],
            ["Turning the symbol the wrong way: 452 &lt; 425", "The open side faces the greater number: 452 &gt; 425"],
            ["Ordering backwards", "Least to greatest starts with the smallest number"],
        ])
    )


FAQ = [
    {"q": "How do you compare three-digit numbers in 2nd grade?",
     "a": "Look at the hundreds first; the number with more hundreds is greater. If the hundreds are the same, compare the tens, and if those are the same too, compare the ones."},
    {"q": "What is an easy way to remember greater than and less than?",
     "a": "The open side of the symbol always faces the greater number, and the point faces the smaller one. So 452 > 425 and 425 < 452."},
    {"q": "Why do kids think 199 is greater than 301?",
     "a": "They see the big 9s and forget that the hundreds digit counts the most. 199 has only 1 hundred and 301 has 3 hundreds, so 199 < 301."},
    {"q": "How do you compare numbers with a zero, like 405 and 450?",
     "a": "A zero means none in that place. Both have 4 hundreds, but 405 has 0 tens and 450 has 5 tens, so 405 < 450."},
]


def mark_large(u, pattern):
    """Tag pictures that must print larger so the blocks stay readable."""
    rx = re.compile(r"<svg (?=[^>]*aria-label='" + pattern + ")")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u


def gen():
    rnd = random.Random(208)
    P = People(rnd)
    used = {452, 425, 405, 450, 199, 301, 299, 362, 326, 352, 235, 325}
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
        "country": "us", "subject": "math", "grade": "grade-2", "slug": "compare-three-digit-numbers", "sort": 8,
        "updated": UPDATED, "pdf_url": "",
        "title": "Compare Three-Digit Numbers",
        "seo_title": "Grade 2 Comparing Three-Digit Numbers Worksheets: Greater Than, Less Than and Ordering to 1000",
        "short_title": "Compare three-digit numbers",
        "domain": "Number and Operations in Base Ten",
        "standard_code": "2.NBT.A.4",
        "standard_url": "https://www.thecorestandards.org/Math/Content/2/NBT/A/4/",
        "standard_text": "Compare two three-digit numbers based on meanings of the hundreds, tens, and ones digits, using >, =, and < symbols to record the results of comparisons.",
        "meta_desc": "Free Grade 2 comparing numbers worksheets: compare three-digit numbers with base-ten blocks and place-value charts, use the greater than, less than and equal symbols, put numbers in order, and solve word problems. 100 practice questions with explanations.",
        "key_big": "Look at the hundreds first. If they are the same, compare the tens, then the ones.",
        "key_sub": "301 > 299, because 3 hundreds is more than 2 hundreds. The open side of > and < faces the greater number: 452 > 425 and 425 < 452.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }
    return mark_large(u, "base-ten blocks")


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
