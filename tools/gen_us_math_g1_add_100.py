# -*- coding: utf-8 -*-
"""
US Grade 1 Math: Add Within 100 (1.NBT.C.4)
  python tools/gen_us_math_g1_add_100.py
Grade 1: addition only. 2-digit + 1-digit, 2-digit + a multiple of 10, and a few easy 2-digit + 2-digit.
All sums are 99 or less. Every answer is computed in code.
Wrong answers come from real Grade 1 mistakes: adding the ones to the tens (23 + 4 = 63), forgetting the
new ten (38 + 5 = 33), writing the whole ones sum (38 + 5 = 313), adding tens to the ones (34 + 20 = 36),
adding all the digits (23 + 4 = 9), and counting on from the start number (off by one).
HTML attributes use single quotes (no backslashes in the JSON).
"""
import json, os, random, re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "us", "math", "grade-1")
UPDATED = "2026-11-02"
GREEN = "#006633"
FILL = "#cfe6d6"
RED = "#c0392b"
INK = "#2b2b2b"
FONT = "Arial, Helvetica, sans-serif"
GIRLS = ["Maya", "Ava", "Mia", "Zoe", "Lily", "Emma", "Nora", "Ruby", "Sofia", "Grace"]
BOYS = ["Leo", "Noah", "Eli", "Sam", "Ben", "Omar", "Kai", "Jack", "Luis", "Owen"]


# ------------------------------------------------------------ helpers
def mcq(q, correct, cands, e):
    """4 choices: correct + the first 3 unique distractors. Positions are set later by balance()."""
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
        self.pool = [(n, "she", "her", "her") for n in GIRLS] + [(n, "he", "his", "him") for n in BOYS]
        rnd.shuffle(self.pool)
        self.i = 0

    def next(self):
        p = self.pool[self.i % len(self.pool)]
        self.i += 1
        return p


def cap(s):
    return s[0].upper() + s[1:]


def pl(n, word):
    return "%d %s" % (n, word if n == 1 else word + "s")


def fig(svg):
    return "<div class='qfig'>" + svg + "</div>"


def svg_wrap(w, h, body, label):
    return ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 %d %d' width='%d' height='%d' "
            "role='img' aria-label='%s'><g font-family='%s'>%s</g></svg>" % (w, h, w, h, label, FONT, body))


def text(x, y, t, fs=16, anchor="middle", col=INK, fam=None):
    f = " font-family='%s'" % fam if fam else ""
    return ("<text x='%.1f' y='%.1f' font-size='%d' font-weight='700' fill='%s' text-anchor='%s'%s>%s</text>"
            % (x, y, fs, col, anchor, f, t))


def table(head, rows):
    h = "".join("<th>%s</th>" % x for x in head)
    b = "".join("<tr>" + "".join("<td>%s</td>" % c for c in r) + "</tr>" for r in rows)
    return "<div class='sn-tw'><table class='sn-table'><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>" % (h, b)


def ex(title, q, s, a):
    return ("<div class='sn-ex'><span class='sn-ex-t'>%s</span><p class='sn-ex-q'>%s</p>"
            "<p class='sn-ex-s'>%s</p><p class='sn-ex-a'>Answer: %s</p></div>" % (title, q, s, a))


def mark_large(u, pattern):
    """Tag pictures that must print larger (blocks, number lines) so every block and label can be read."""
    rx = re.compile(r"<svg (?=[^>]*aria-label='(?:" + pattern + "))")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u


# ------------------------------------------------------------ pictures
CELL = 11          # one unit cube; a ten rod is 10 cubes tall


def blocks_group(x0, base, n_tens, n_ones, ones_col=FILL):
    """Draw tens rods and ones cubes standing on the line y = base. Returns (svg, width)."""
    s = []
    x = x0
    for _ in range(n_tens):
        top = base - 10 * CELL
        s.append("<rect x='%d' y='%d' width='%d' height='%d' fill='%s' stroke='%s' stroke-width='1.6'/>"
                 % (x, top, CELL, 10 * CELL, FILL, GREEN))
        for k in range(1, 10):
            y = top + k * CELL
            s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='1'/>" % (x, y, x + CELL, y, GREEN))
        x += CELL + 5
    if n_tens and n_ones:
        x += 6
    cols = (n_ones + 4) // 5
    for c in range(cols):
        for r in range(min(5, n_ones - 5 * c)):
            s.append("<rect x='%d' y='%d' width='%d' height='%d' fill='%s' stroke='%s' stroke-width='1.6'/>"
                     % (x, base - (r + 1) * (CELL + 3) + 3, CELL, CELL, ones_col, GREEN))
        x += CELL + 4
    return "".join(s), x - x0 - (4 if cols else 5)


def blocks_svg(groups, labels=True):
    """groups: list of (tens, ones). Two groups are joined with a + sign."""
    o, top = 8, 8
    base = top + 10 * CELL
    H = base + (30 if labels else 8)
    body, x = [], o
    for gi, (t, n) in enumerate(groups):
        if gi:
            body.append(text(x + 16, base - 5 * CELL + 10, "+", 30, col=GREEN))
            x += 32
        g, w = blocks_group(x, base, t, n)
        body.append(g)
        if labels:
            body.append(text(x + w / 2, base + 22, str(10 * t + n), 18))
        x += w
    W = x + o
    what = " plus ".join(("%s and %s" % (pl(t, "ten"), pl(n, "one"))) if t and n else pl(t, "ten") if t else pl(n, "one")
                         for t, n in groups)
    return svg_wrap(W, H, "".join(body), "base-ten blocks: " + what)


def frames_svg(have, add):
    """Two ten-frames for the ones: `have` green dots, then `add` red dots that fill the first frame first."""
    c, gap, m = 24, 18, 6
    fw = 5 * c
    W, H = 2 * fw + gap + 2 * m, 2 * c + 2 * m
    s = []
    for f in range(2):
        x0 = m + f * (fw + gap)
        s.append("<rect x='%d' y='%d' width='%d' height='%d' fill='#ffffff' stroke='%s' stroke-width='2'/>"
                 % (x0, m, fw, 2 * c, INK))
        for k in range(1, 5):
            s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='1.5'/>"
                     % (x0 + k * c, m, x0 + k * c, m + 2 * c, INK))
        s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='1.5'/>"
                 % (x0, m + c, x0 + fw, m + c, INK))
    for i in range(have + add):
        f, k = divmod(i, 10)
        r, col = divmod(k, 5)
        cx = m + f * (fw + gap) + col * c + c / 2
        cy = m + r * c + c / 2
        s.append("<circle cx='%.1f' cy='%.1f' r='8' fill='%s'/>" % (cx, cy, GREEN if i < have else RED))
    return svg_wrap(W, H, "".join(s), "two ten-frames: %s green dots and %s red dots" % (have, add))


def column_svg(nums, big=False, carry=False):
    """Numbers in columns (ones under ones), plus sign and line. carry=True (lesson only) shows the new ten."""
    fs = 34 if big else 28
    cw = fs * (0.9 if carry else 0.64)
    pad = 22 if carry else 6
    W = int(cw * 3.6 + 22)
    rows = len(nums)
    H = int(pad + fs * rows + 22)
    right = W - 10
    s = []

    def cx(i):
        return right - cw * (i + 0.5)

    for row, n in enumerate(nums):
        y = pad + fs * (row + 1) - 4
        for i, ch in enumerate(reversed(str(n))):
            s.append(text(cx(i), y, ch, fs, col=INK, fam="monospace"))
    s.append(text(right - cw * 2.9, pad + fs * rows - 4, "+", fs, col=GREEN))
    ly = pad + fs * rows + 8
    s.append("<line x1='%.0f' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='3'/>"
             % (right - cw * 3.4, ly, right, ly, INK))
    if carry and sum(n % 10 for n in nums) >= 10:
        s.append(text(cx(1), pad - 4, "1", 18, col=RED))
    return svg_wrap(W, H, "".join(s), " plus ".join(str(n) for n in nums) + " written in columns")


def jw(j):
    return 80 if abs(j) >= 10 else 56


def nline_svg(start, jumps, ticks=None):
    """Open number line. ticks: one label per point (None = no label)."""
    if ticks is None:
        ticks = [str(start)] + [None] * (len(jumps) - 1) + ["?"]
    labels = ["+%d" % j for j in jumps]
    m, ry, ly = 30, 24, 50
    W = 2 * m + sum(jw(j) for j in jumps)
    H = ly + 32
    xs = [m]
    for j in jumps:
        xs.append(xs[-1] + jw(j))
    s = ["<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='2.5'/>" % (m - 18, ly, W - m + 18, ly, INK)]
    for k in range(len(jumps)):
        x1, x2 = xs[k], xs[k + 1]
        rx = (x2 - x1) / 2
        s.append("<path d='M %d %d A %.1f %d 0 0 1 %d %d' fill='none' stroke='%s' stroke-width='2.5'/>"
                 % (x1, ly, rx, ry, x2, ly, GREEN))
        s.append("<polyline points='%d,%d %d,%d %d,%d' fill='none' stroke='%s' stroke-width='2.5' "
                 "stroke-linejoin='round'/>" % (x2 - 5, ly - 10, x2, ly - 2, x2 + 5, ly - 10, GREEN))
        s.append(text((x1 + x2) / 2, ly - ry - 7, labels[k], 15, col=GREEN))
    for x, t in zip(xs, ticks):
        s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='2'/>" % (x, ly - 6, x, ly + 6, INK))
        if t is not None:
            s.append(text(x, ly + 24, t, 16))
    return svg_wrap(W, H, "".join(s), "open number line starting at %d with jumps of %s" % (start, ", ".join(labels)))


# ------------------------------------------------------------ steps and typical mistakes
def steps(a, b):
    """Explanation for a + b (a is the 2-digit number; b may be 1-digit, tens, or 2-digit)."""
    s = a + b
    t1, o1, t2, o2 = a // 10, a % 10, b // 10, b % 10
    o = o1 + o2
    if b < 10:
        if o < 10:
            return ("The tens stay %s. Ones: %d + %d = %d. %s and %s is %d."
                    % (pl(t1, "ten"), o1, o2, o, cap(pl(t1, "ten")), pl(o, "one"), s))
        need = 10 - o1
        return ("Make a ten: %d + %d = %d. Then %d + %d = %d. (Ones: %d + %d = %d. 10 ones make 1 new ten.)"
                % (a, need, a + need, a + need, b - need, s, o1, o2, o))
    if o2 == 0:
        return ("%d is %s. Add tens to tens: %d + %d = %s. The ones stay %d. %s and %s is %d."
                % (b, pl(t2, "ten"), t1, t2, pl(t1 + t2, "ten"), o1, cap(pl(t1 + t2, "ten")), pl(o1, "one"), s))
    if o < 10:
        return ("Tens: %d + %d = %s. Ones: %d + %d = %s. %s and %s is %d."
                % (t1, t2, pl(t1 + t2, "ten"), o1, o2, pl(o, "one"), cap(pl(t1 + t2, "ten")), pl(o, "one"), s))
    return ("Tens: %d + %d = %s. Ones: %d + %d = %d ones. 10 ones make 1 new ten. %s + 1 ten = %s. %s and %s is %d."
            % (t1, t2, pl(t1 + t2, "ten"), o1, o2, o, cap(pl(t1 + t2, "ten")), pl(t1 + t2 + 1, "ten"),
               cap(pl(s // 10, "ten")), pl(s % 10, "one"), s))


def digit_sum(*ns):
    return sum(int(ch) for n in ns for ch in str(n))


def concat(a, b):
    """Wrote the whole ones sum: 38 + 5 = 3|13 = 313."""
    return int("%d%d" % (a // 10 + b // 10, a % 10 + b % 10))


def cands(a, b):
    """Typical wrong answers for a + b, most likely first."""
    s = a + b
    o = a % 10 + b % 10
    if b < 10:
        big = [a + 10 * b] if a + 10 * b <= 99 else []          # 23 + 4 = 63 (only while it stays a 2-digit number)
        c = [s - 10, concat(a, b)] + big if o >= 10 else big + [digit_sum(a, b)]
        return c + [s - 1, s + 1, s + 10]
    if b % 10 == 0:
        return [a + b // 10, a + 10 if b > 10 else s + 10, s + 10, s - 10, digit_sum(a, b)]
    if o >= 10:
        return [s - 10, concat(a, b), s + 10, s - 1, s + 1]
    return [a + b % 10, s + 10, s - 10, digit_sum(a, b), s + 1]


# ------------------------------------------------------------ number pickers
def pick(rnd, kind, seen, max_tens=9):
    """kind: '1' 2-digit + 1-digit no new ten, '1t' with a new ten, '10' + tens, '2' 2-digit + 2-digit,
    '2t' 2-digit + 2-digit with a new ten. The ones of the sum are never 0."""
    while True:
        a = rnd.randint(11, 89)
        if kind in ("1", "1t"):
            b = rnd.randint(2, 9)
        elif kind == "10":
            b = 10 * rnd.randint(2, 6)
        else:
            b = rnd.randint(11, 59)
        s = a + b
        if a % 10 == 0 or (b >= 10 and kind != "10" and b % 10 == 0) or s > 99 or s % 10 == 0:
            continue
        if a // 10 + b // 10 > max_tens:
            continue
        o = a % 10 + b % 10
        if (o >= 10) != (kind in ("1t", "2t")):
            continue
        if (a, b) in seen or (b, a) in seen:
            continue
        seen.add((a, b))
        return a, b


# ============================================================ set 1: add ones (no new ten)
def set_ones(rnd, seen):
    its = []
    for _ in range(8):                                  # with blocks
        a, b = pick(rnd, "1", seen, max_tens=6)
        its.append(mcq(fig(blocks_svg([(a // 10, a % 10), (0, b)])) + "Use the blocks. What is %d + %d?" % (a, b),
                       a + b, cands(a, b), steps(a, b)))
    for _ in range(3):                                  # count on by ones
        while True:
            a, b = pick(rnd, "1", seen)
            if 3 <= b <= 5:
                break
            seen.discard((a, b))
        s = a + b
        e = "Start at %d. Count on %d: %s. You land on %d. So %d + %d = %d." % (
            a, b, ", ".join(str(a + k) for k in range(1, b + 1)), s, a, b, s)
        its.append(mcq(fig(nline_svg(a, [1] * b)) + "Start at %d. Count on %d. Where do you land?" % (a, b),
                       s, [s - 1] + ([a + 10 * b] if a + 10 * b <= 99 else []) + [s + 1, s + 10], e))
    for i in range(5):                                  # plain, two with the small number first
        a, b = pick(rnd, "1", seen)
        if i < 2:
            q = "What is %d + %d?" % (b, a)
            e = "Start with the bigger number: %d + %d. " % (a, b) + steps(a, b)
        else:
            q = "What is %d + %d?" % (a, b)
            e = steps(a, b)
        its.append(mcq(q, a + b, cands(a, b), e))
    for _ in range(2):                                  # in columns
        a, b = pick(rnd, "1", seen)
        its.append(mcq(fig(column_svg([a, b])) + "Add. The ones go under the ones.", a + b, cands(a, b),
                       "The %d goes under the ones. " % b + steps(a, b)))
    for _ in range(2):                                  # tens and ones box
        a, b = pick(rnd, "1", seen)
        s = a + b
        t, o = a // 10, a % 10
        q = "%d + %d = %s and ☐ ones. What number goes in the box?" % (a, b, pl(t, "ten"))
        e = "The tens stay %s. Ones: %d + %d = %d. So %d + %d = %d." % (pl(t, "ten"), o, b, o + b, a, b, s)
        its.append(mcq(q, s % 10, [t + b, b, o, s % 10 + 1], e))
    assert len(its) == 20, len(its)
    its = its[:4] + its[8:11] + its[4:8] + its[11:]
    return {"title": "Add ones to a 2-digit number", "items": its}


# ============================================================ set 2: add tens
def set_tens(rnd, seen):
    its = []
    for _ in range(7):                                  # with blocks
        a, b = pick(rnd, "10", seen, max_tens=7)
        its.append(mcq(fig(blocks_svg([(a // 10, a % 10), (b // 10, 0)])) + "Use the blocks. What is %d + %d?" % (a, b),
                       a + b, cands(a, b), steps(a, b)))
    for _ in range(3):                                  # jumps of 10
        while True:
            a, b = pick(rnd, "10", seen)
            if b <= 30:
                break
            seen.discard((a, b))
        s = a + b
        n = b // 10
        e = "Each jump adds 1 ten. Start at %d: %s. You land on %d. So %d + %d = %d." % (
            a, ", ".join(str(a + 10 * k) for k in range(1, n + 1)), s, a, b, s)
        its.append(mcq(fig(nline_svg(a, [10] * n)) + "Start at %d. Jump 10 each time. Where do you land?" % a,
                       s, [a + n, s - 10, s + 10, s + 1], e))
    for i in range(5):                                  # plain, two with the tens first
        a, b = pick(rnd, "10", seen)
        if i < 2:
            q = "What is %d + %d?" % (b, a)
            e = "You can add in any order: %d + %d = %d + %d. " % (b, a, a, b) + steps(a, b)
        else:
            q = "What is %d + %d?" % (a, b)
            e = steps(a, b)
        its.append(mcq(q, a + b, cands(a, b), e))
    for _ in range(2):                                  # in columns
        a, b = pick(rnd, "10", seen)
        its.append(mcq(fig(column_svg([a, b])) + "Add. Add the tens to the tens.", a + b, cands(a, b),
                       steps(a, b)))
    for _ in range(3):                                  # ☐ tens and ones
        a, b = pick(rnd, "10", seen)
        s = a + b
        t, n, o = a // 10, b // 10, a % 10
        q = "%d + %d = ☐ tens and %s. What number goes in the box?" % (a, b, pl(o, "one"))
        e = "%d is %s. %s + %s = %s. So %d + %d = %d." % (b, pl(n, "ten"), cap(pl(t, "ten")), pl(n, "ten"),
                                                        pl(s // 10, "ten"), a, b, s)
        its.append(mcq(q, s // 10, [t, n, t + 1, o + n], e))
    assert len(its) == 20, len(its)
    its = its[:4] + its[7:10] + its[4:7] + its[10:]
    return {"title": "Add tens to a 2-digit number", "items": its}


# ============================================================ set 3: make a new ten
def set_make_ten(rnd, seen):
    its = []
    for _ in range(6):                                  # with blocks
        a, b = pick(rnd, "1t", seen, max_tens=6)
        its.append(mcq(fig(blocks_svg([(a // 10, a % 10), (0, b)])) +
                       "Use the blocks. Make a ten with the ones. What is %d + %d?" % (a, b),
                       a + b, cands(a, b), steps(a, b)))
    for _ in range(4):                                  # ten-frames
        a, b = pick(rnd, "1t", seen)
        s = a + b
        o = a % 10
        need = 10 - o
        left = b - need
        e = ("The first ten-frame fills up: %d + %d = 10. That is 1 new ten. %s left. "
             "%s + 1 ten = %s. So %d + %d = %d."
             % (o, need, "1 dot is" if left == 1 else "%d dots are" % left, cap(pl(a // 10, "ten")),
                pl(a // 10 + 1, "ten"), a, b, s))
        its.append(mcq(fig(frames_svg(o, b)) + "The ten-frames show the ones in %d + %d. What is %d + %d?" % (a, b, a, b),
                       s, cands(a, b), e))
    for _ in range(3):                                  # how many to the next ten
        a, b = pick(rnd, "1t", seen)
        o = a % 10
        nt = a // 10 * 10 + 10
        e = "%d has %s. %d + %d = 10, so %d + %d = %d." % (a, pl(o, "one"), o, 10 - o, a, 10 - o, nt)
        its.append(mcq("How many more does %d need to make %d?" % (a, nt), 10 - o, [11 - o, o, 9 - o, 10], e))
    for a, b in [(38, 5), (47, 6)]:                     # which is the same (kept out of the other questions)
        need = 10 - a % 10
        nt = a + need
        e = "Take %d from %d to make %d. %d − %d = %d left. So %d + %d = %d + %d = %d." % (
            need, b, nt, b, need, b - need, a, b, nt, b - need, a + b)
        its.append(mcq("Which is the same as %d + %d?" % (a, b), "%d + %d" % (nt, b - need),
                       ["%d + %d" % (nt, b), "%d + %d" % (nt - 10, b - need), "%d + %d" % (a, need)], e))
    for _ in range(3):                                  # number line to the next ten
        a, b = pick(rnd, "1t", seen)
        need = 10 - a % 10
        nt = a + need
        e = "Jump %d to get to %d. Then jump %d more. %d + %d = %d. So %d + %d = %d." % (
            need, nt, b - need, nt, b - need, a + b, a, b, a + b)
        its.append(mcq(fig(nline_svg(a, [need, b - need], [str(a), str(nt), "?"])) +
                       "Jump to %d first. What is %d + %d?" % (nt, a, b), a + b, cands(a, b), e))
    for i in range(2):                                  # plain
        a, b = pick(rnd, "1t", seen)
        q = "What is %d + %d?" % ((b, a) if i == 0 else (a, b))
        its.append(mcq(q, a + b, cands(a, b), steps(a, b)))
    assert len(its) == 20, len(its)
    its = its[:3] + its[6:10] + its[3:6] + its[10:]
    return {"title": "Add ones and make a new ten", "items": its}


# ============================================================ set 4: add two 2-digit numbers
def set_two_digit(rnd, seen):
    its = []
    for k in range(8):                                  # with blocks
        a, b = pick(rnd, "2" if k < 5 else "2t", seen, max_tens=6)
        its.append(mcq(fig(blocks_svg([(a // 10, a % 10), (b // 10, b % 10)])) + "Use the blocks. What is %d + %d?" % (a, b),
                       a + b, cands(a, b), steps(a, b)))
    for k in range(4):                                  # number line: tens jump, then ones jump
        a, b = pick(rnd, "2" if k < 2 else "2t", seen)
        t, o = b // 10 * 10, b % 10
        e = "%d is %d and %d. Jump %d: %d + %d = %d. Then jump %d: %d + %d = %d. So %d + %d = %d." % (
            b, t, o, t, a, t, a + t, o, a + t, o, a + b, a, b, a + b)
        its.append(mcq(fig(nline_svg(a, [t, o])) + "Jump the tens, then the ones. What is %d + %d?" % (a, b),
                       a + b, cands(a, b), e))
    for k in range(4):                                  # columns
        a, b = pick(rnd, "2" if k < 2 else "2t", seen)
        its.append(mcq(fig(column_svg([a, b])) + "Add. Add ones to ones and tens to tens.", a + b, cands(a, b), steps(a, b)))
    for _ in range(2):                                  # break apart
        a, b = pick(rnd, "2", seen)
        t = (a // 10 + b // 10) * 10
        o = a % 10 + b % 10
        q = "Add tens and tens, then ones and ones. %d + %d = %d + ☐. What number goes in the box?" % (a, b, t)
        e = "Tens: %d + %d = %d. Ones: %d + %d = %d. So %d + %d = %d + %d = %d." % (
            a // 10 * 10, b // 10 * 10, t, a % 10, b % 10, o, a, b, t, o, a + b)
        its.append(mcq(q, o, [b % 10, a % 10, a + b, o + 1], e))
    for _ in range(2):                                  # plain with a new ten
        a, b = pick(rnd, "2t", seen)
        its.append(mcq("What is %d + %d?" % (a, b), a + b, cands(a, b), steps(a, b)))
    assert len(its) == 20, len(its)
    its = its[:3] + its[8:10] + its[12:14] + its[3:5] + its[16:18] + its[5:8] + its[10:12] + its[14:16] + its[18:]
    return {"title": "Add two 2-digit numbers", "items": its}


# ============================================================ set 5: word problems
STORIES = [
    # (template, a, b, unit, people needed)
    ("{n} has {a} shells. {He} finds {b} more. How many shells does {he} have now?", 22, 5, "shells"),
    ("There are {a} kids on the playground. {b} more kids come. How many kids are there now?", 41, 6, "kids"),
    ("{n} has {a} stickers. {His} friend gives {him} {b} more. How many stickers does {he} have now?", 35, 3, "stickers"),
    ("A farm has {a} cows and {b} horses. How many animals are there?", 52, 7, "animals"),
    ("{n} has {a} marbles. {He} gets {b} more. How many marbles does {he} have now?", 33, 40, "marbles"),
    ("One box has {a} crayons. Another box has {b} crayons. How many crayons are there in all?", 40, 25, "crayons"),
    ("{n} puts {a} beads on a string. Then {he} adds {b} more. How many beads are on the string?", 46, 30, "beads"),
    ("There are {a} books on a shelf. The teacher puts {b} more books on it. How many books are on the shelf now?", 62, 20, "books"),
    ("{n} has {a} cents. {His} mom gives {him} {b} cents. How many cents does {he} have now?", 42, 30, "cents"),
    ("{n} has {a} cards. {He} gets {b} more cards. How many cards does {he} have now?", 37, 5, "cards"),
    ("{a} birds sit in a tree. {b} more birds come. How many birds are in the tree now?", 27, 6, "birds"),
    ("{n} has {a} blocks. {He} gets {b} more. How many blocks does {he} have now?", 49, 4, "blocks"),
    ("A pond has {a} red fish and {b} blue fish. How many fish are in the pond?", 56, 8, "fish"),
    ("There are {a} people on a bus. {b} more people get on. How many people are on the bus now?", 25, 9, "people"),
    ("A baker makes {a} muffins. Then she makes {b} more. How many muffins does she make in all?", 36, 7, "muffins"),
    ("{n} has {a} red balloons and {b} blue balloons. How many balloons does {he} have?", 24, 15, "balloons"),
    ("A zoo has {a} ducks and {b} geese. How many birds are there in all?", 33, 26, "birds"),
    ("{n} picks {a} strawberries. {His} brother picks {b}. How many strawberries do they pick in all?", 28, 14, "strawberries"),
    ("One room has {a} chairs. Another room has {b} chairs. How many chairs are there in all?", 47, 36, "chairs"),
    ("{n} has {a} toy cars. {He} gets {b} more for {his} birthday. How many toy cars does {he} have now?", 51, 40, "toy cars"),
]


def story_e(t, a, b):
    """Short reason for adding, then the place-value steps."""
    why = "Getting more means add. " if "more" in t or "gives" in t else "Put the two groups together: add. "
    return why + steps(a, b)


def set_stories(P):
    its = []
    for t, a, b, unit in STORIES:
        n, he, his, him = P.next()
        q = t.format(n=n, a=a, b=b, he=he, He=cap(he), his=his, His=cap(his), him=him)
        its.append(mcq(q, "%d %s" % (a + b, unit), ["%d %s" % (v, unit) for v in cands(a, b) if v > 0],
                       story_e(t, a, b)))
    assert len(its) == 20, len(its)
    return {"title": "Addition word problems within 100", "items": its}


# ============================================================ lesson
def body_html():
    return (
        "<h2>Tens and ones</h2>"
        "<p>A 2-digit number has <b>tens</b> and <b>ones</b>. 23 is 2 tens and 3 ones. "
        "When you add, put ones with ones and tens with tens.</p>"
        "<h2>Add ones</h2>"
        "<p>Add the ones. The tens stay the same.</p>"
        "<figure class='sn-fig'>" + blocks_svg([(2, 3), (0, 4)]) +
        "<figcaption>23 + 4. The tens stay 2 tens. Ones: 3 + 4 = 7. 2 tens and 7 ones is 27.</figcaption></figure>"
        "<h2>Add tens</h2>"
        "<p>20 is 2 tens. Add tens to tens. The ones stay the same.</p>"
        "<figure class='sn-fig'>" + blocks_svg([(3, 4), (2, 0)]) +
        "<figcaption>34 + 20. Tens: 3 + 2 = 5 tens. The ones stay 4. 5 tens and 4 ones is 54.</figcaption></figure>"
        "<figure class='sn-fig'>" + nline_svg(34, [10, 10], ["34", "44", "54"]) +
        "<figcaption>Or jump 10 two times: 34, 44, 54.</figcaption></figure>"
        "<h2>Make a new ten</h2>"
        "<p>Sometimes the ones make 10 or more. Then 10 ones make <b>1 new ten</b>.</p>"
        "<figure class='sn-fig'>" + frames_svg(8, 5) +
        "<figcaption>38 + 5. The ones are 8 + 5. 2 red dots fill the ten-frame. 3 dots are left. "
        "So 8 + 5 is 1 ten and 3 ones.</figcaption></figure>"
        "<figure class='sn-fig'>" + nline_svg(38, [2, 3], ["38", "40", "43"]) +
        "<figcaption>Jump 2 to make 40. Then jump 3 more. 38 + 5 = 43.</figcaption></figure>"
        + ex("Make a ten", "What is 47 + 6?",
             "47 needs 3 more to make 50. Take 3 from 6. 3 are left. 50 + 3 = 53.", "53") +
        "<h2>Add two 2-digit numbers</h2>"
        "<p>Add tens and tens. Add ones and ones. Then put them together.</p>"
        "<figure class='sn-fig'>" + column_svg([26, 35], big=True, carry=True) +
        "<figcaption>Ones: 6 + 5 = 11. That is 1 new ten and 1 one. Tens: 2 + 3 + 1 = 6. Answer: 61.</figcaption></figure>"
        + ex("Tens and ones", "What is 24 + 35?",
             "Tens: 20 + 30 = 50. Ones: 4 + 5 = 9. 50 + 9 = 59.", "59") +
        "<h2>Common mistakes</h2>"
        + table(["Mistake", "What to do instead"], [
            ["Adding ones to the tens: 23 + 4 = 63", "4 is 4 ones. Add it to the 3 ones"],
            ["Adding tens to the ones: 34 + 20 = 36", "20 is 2 tens. Add it to the 3 tens"],
            ["Forgetting the new ten: 38 + 5 = 33", "8 + 5 = 13 is 1 ten and 3 ones. Add the new ten"],
            ["Writing 13 in the ones: 38 + 5 = 313", "Only one digit goes in the ones place"],
            ["Adding all the digits: 23 + 4 = 9", "Keep tens and ones apart"],
        ])
    )


FAQ = [
    {"q": "How do you teach adding within 100 in 1st grade?",
     "a": "Use base-ten blocks: rods for tens and cubes for ones. Show that you add ones to ones and tens to tens, then write the same steps as numbers."},
    {"q": "How do you add a 2-digit and a 1-digit number, like 38 + 5?",
     "a": "Make the next ten first: 38 + 2 = 40, then add the 3 that are left: 40 + 3 = 43. The 10 ones make 1 new ten."},
    {"q": "How do you add a multiple of 10, like 34 + 20?",
     "a": "20 is 2 tens, so add it to the tens: 3 tens + 2 tens = 5 tens. The ones do not change, so 34 + 20 = 54."},
    {"q": "What does 1.NBT.C.4 mean?",
     "a": "It is the Common Core standard for Grade 1: add within 100, including a 2-digit number plus a 1-digit number and a 2-digit number plus a multiple of 10, using models and place value. Children learn that sometimes 10 ones make a new ten."},
]


def gen():
    rnd = random.Random(107)
    P = People(rnd)
    seen = {(a, b) for _, a, b, _ in STORIES}
    seen |= {(23, 4), (34, 20), (38, 5), (47, 6), (26, 35), (24, 35)}      # lesson and set 3 examples
    sets = [set_ones(rnd, seen), set_tens(rnd, seen), set_make_ten(rnd, seen), set_two_digit(rnd, seen), set_stories(P)]
    balance(sets, rnd)
    keys = set()
    for s in sets:
        assert len(s["items"]) == 20, (s["title"], len(s["items"]))
        assert sorted(it["a"] for it in s["items"]) == sorted([0, 1, 2, 3] * 5)
        for it in s["items"]:
            assert len(set(it["c"])) == 4, it
            k = it["q"]
            assert k not in keys, it["q"]
            keys.add(k)
    u = {
        "country": "us", "subject": "math", "grade": "grade-1", "slug": "add-within-100", "sort": 7,
        "updated": UPDATED, "pdf_url": "",
        "title": "Add Within 100 (Grade 1)",
        "seo_title": "Grade 1 Addition Within 100 Worksheets: Add Ones, Add Tens and Make a Ten",
        "short_title": "Add within 100",
        "domain": "Number and Operations in Base Ten",
        "standard_code": "1.NBT.C.4",
        "standard_url": "https://www.thecorestandards.org/Math/Content/1/NBT/C/4/",
        "standard_text": "Add within 100, including adding a two-digit number and a one-digit number, and adding a two-digit number and a multiple of 10, using concrete models or drawings and strategies based on place value, properties of operations, and/or the relationship between addition and subtraction; relate the strategy to a written method and explain the reasoning used. Understand that in adding two-digit numbers, one adds tens and tens, ones and ones; and sometimes it is necessary to compose a ten.",
        "meta_desc": "Free 1st grade addition within 100 worksheets: add a 1-digit number to a 2-digit number, add tens like 34 + 20, make a new ten with ten-frames and number lines, and short word problems. 100 practice questions with base-ten block pictures and an answer key.",
        "key_big": "Add ones to ones and tens to tens. 10 ones make 1 new ten.",
        "key_sub": "23 + 4: add the 4 to the ones (27). 34 + 20: add the 2 tens to the tens (54). 38 + 5: 8 + 5 = 13 ones, so you get 1 new ten (43).",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }
    return mark_large(u, "base-ten blocks|open number line")


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
