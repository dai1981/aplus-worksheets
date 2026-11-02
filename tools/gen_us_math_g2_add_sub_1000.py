# -*- coding: utf-8 -*-
"""
US Grade 2 Math: Add and Subtract Within 1000 with Models (2.NBT.B.7, 2.NBT.B.8)
  python tools/gen_us_math_g2_add_sub_1000.py
Models first: base-ten blocks, break apart by place, open number lines, and mental +10/+100.
(Grade 3 has the standard algorithm unit with the same slug.)
Every answer, block picture and number-line jump is computed and checked in code.
HTML attributes use single quotes (no backslashes in the JSON).
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
PLACE = ["ones", "tens", "hundreds"]
ONE = ["one", "ten", "hundred"]


# ------------------------------------------------------------ math
def digits(n):
    return [n % 10, (n // 10) % 10, (n // 100) % 10]          # ones first


def num(d):
    return d[0] + 10 * d[1] + 100 * d[2]


def pv(h, t, o):
    """3 hundreds, 1 ten, 12 ones"""
    def w(k, i):
        return "%d %s" % (k, ONE[i] if k == 1 else PLACE[i])
    return "%s, %s, %s" % (w(h, 2), w(t, 1), w(o, 0))


def pl(k, i):
    """1 ten, 2 tens, 1 hundred …"""
    return "%d %s" % (k, ONE[i] if k == 1 else PLACE[i])


def regroups_add(a, b):
    da, db = digits(a), digits(b)
    c, n = 0, 0
    where = []
    for i in range(3):
        t = da[i] + db[i] + c
        c = 1 if t >= 10 else 0
        if c:
            where.append(i)
    return where


def regroups_sub(a, b):
    d, db = digits(a), digits(b)
    where = []
    for i in range(2):
        if d[i] < db[i]:
            where.append(i)
            d[i] += 10
            d[i + 1] -= 1
    return where


# ------------------------------------------------------------ explanations (short, Grade 2 words)
def add_e(a, b):
    da, db = digits(a), digits(b)
    carry, parts = 0, []
    for i in range(3):
        t = da[i] + db[i] + carry
        ex = "%d + %d" % (da[i], db[i]) + (" + 1" if carry else "")
        if i == 2 and da[2] == 0 and db[2] == 0 and not carry:
            continue
        if t >= 10:
            assert i < 2
            parts.append("%s: %s = %d %s. Make a %s: 1 %s and %d %s." % (
                PLACE[i].capitalize(), ex, t, PLACE[i], ONE[i + 1], ONE[i + 1], t - 10, PLACE[i] if t - 10 != 1 else ONE[i]))
            carry = 1
        else:
            parts.append("%s: %s = %d." % (PLACE[i].capitalize(), ex, t))
            carry = 0
    return " ".join(parts) + " Answer: <b>%d</b>." % (a + b)


def split_e(a, b):
    """Break apart by place: 300 + 100, 50 + 70, 2 + 5."""
    da, db = digits(a), digits(b)
    h, t, o = (da[2] + db[2]) * 100, (da[1] + db[1]) * 10, da[0] + db[0]
    s = []
    if da[2] or db[2]:
        s.append("Hundreds: %d + %d = %d." % (da[2] * 100, db[2] * 100, h))
    s.append("Tens: %d + %d = %d." % (da[1] * 10, db[1] * 10, t))
    s.append("Ones: %d + %d = %d." % (da[0], db[0], o))
    s.append("%d + %d + %d = <b>%d</b>." % (h, t, o, a + b))
    return " ".join(s)


def sub_e(a, b, check=True):
    d, db = digits(a), digits(b)
    parts = []
    for i in range(3):
        if i == 2 and d[2] == 0 and db[2] == 0:
            continue
        if d[i] < db[i]:
            assert i < 2
            if i == 0 and d[1] == 0:
                d[2] -= 1
                d[1] = 9
                d[0] += 10
                parts.append("Ones: %d − %d? Not enough ones, and there are 0 tens. Trade 1 hundred for 10 tens. "
                             "Then trade 1 ten for 10 ones: %d − %d = %d." % (d[0] - 10, db[0], d[0], db[0], d[0] - db[0]))
            else:
                d[i + 1] -= 1
                d[i] += 10
                parts.append("%s: %d − %d? Not enough %s. Trade 1 %s for 10 %s: %d − %d = %d." % (
                    PLACE[i].capitalize(), d[i] - 10, db[i], PLACE[i], ONE[i + 1], PLACE[i], d[i], db[i], d[i] - db[i]))
        else:
            parts.append("%s: %d − %d = %d." % (PLACE[i].capitalize(), d[i], db[i], d[i] - db[i]))
    s = " ".join(parts) + " Answer: <b>%d</b>." % (a - b)
    if check:
        s += " Check: %d + %d = %d." % (a - b, b, a)
    return s


# ------------------------------------------------------------ typical mistakes
def add_no_regroup(a, b):
    """Forgot to move the new ten or hundred."""
    da, db = digits(a), digits(b)
    return sum(((da[i] + db[i]) % 10) * 10 ** i for i in range(3))


def sub_small_from_big(a, b):
    """Took the smaller digit from the bigger one in every place."""
    da, db = digits(a), digits(b)
    return sum(abs(da[i] - db[i]) * 10 ** i for i in range(3))


def sub_forgot_reduce(a, b):
    """Traded, but did not take 1 away from the next place."""
    r = a - b
    for i in regroups_sub(a, b):
        r += 10 ** (i + 1)
    return r


def add_cands(a, b, rnd):
    s = a + b
    rest = [s + 10, s - 10, s + 100, s - 100]
    rnd.shuffle(rest)
    return [add_no_regroup(a, b)] + rest + [s + 1, s - 1]


def near_cands(s, rnd):
    """Miscounting one block: one rod, one flat or one cube too many or too few."""
    c = [s + 10, s - 10, s + 100, s - 100, s + 1, s - 1]
    rnd.shuffle(c)
    return c


def sub_cands(a, b, rnd):
    r = a - b
    rest = [r + 10, r - 10, r + 100]
    rnd.shuffle(rest)
    return [sub_small_from_big(a, b), sub_forgot_reduce(a, b)] + rest + [a + b]


# ------------------------------------------------------------ helpers
def mcq(q, correct, cands, e):
    """4 choices: correct + the first 3 unique distractors. Positions are set later by balance()."""
    correct = str(correct)
    seen = {correct}
    pick = []
    for c in cands:
        c = str(c)
        lead = c.split(" ")[0]
        if c in seen or not c or lead.startswith("-") or lead in ("0", "+0", "−0"):
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
        self.pool = [(n, "she", "her") for n in GIRLS] + [(n, "he", "his") for n in BOYS]
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
    """Tag pictures that must print larger so they stay readable."""
    rx = re.compile(r"<svg (?=[^>]*aria-label='" + pattern + ")")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u


# ------------------------------------------------------------ pictures
C = 6              # one small cube; a rod is 1 × 10 cubes, a flat is 10 × 10
FLAT, ROD_GAP, FLAT_GAP, PART_GAP, CUBE_GAP = 10 * C, 4, 6, 16, 4


def part_widths(h, t, o):
    cols = (o + 4) // 5
    return [h * (FLAT + FLAT_GAP) - FLAT_GAP if h else 0,
            t * (C + ROD_GAP) - ROD_GAP if t else 0,
            cols * (C + CUBE_GAP) - CUBE_GAP if o else 0]


def slash(x, y, w, h, full=False):
    """Red cross-out: an X over a flat, one slash over a rod or a cube."""
    s = ("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='2.2' stroke-linecap='round'/>"
         % (x - 2, y + h + 2, x + w + 2, y - 2, RED))
    if full:
        s += ("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='2.2' stroke-linecap='round'/>"
              % (x - 2, y - 2, x + w + 2, y + h + 2, RED))
    return s


def draw_row(xs, y, h, t, o, cross=(0, 0, 0)):
    """Base-ten blocks for h hundreds, t tens, o ones, starting at the column positions xs.
    The last `cross` of each kind are faded and crossed out."""
    s = []

    def fill(k, n, c):
        return "#ffffff" if k >= n - c else FILL

    x = xs[0]
    for k in range(h):
        s.append("<rect x='%d' y='%d' width='%d' height='%d' fill='%s' stroke='%s' stroke-width='1.5'/>"
                 % (x, y, FLAT, FLAT, fill(k, h, cross[0]), GREEN))
        for g in range(1, 10):
            s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='0.6'/>"
                     % (x + g * C, y, x + g * C, y + FLAT, GREEN))
            s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='0.6'/>"
                     % (x, y + g * C, x + FLAT, y + g * C, GREEN))
        if k >= h - cross[0]:
            s.append(slash(x, y, FLAT, FLAT, full=True))
        x += FLAT + FLAT_GAP
    x = xs[1]
    for k in range(t):
        s.append("<rect x='%d' y='%d' width='%d' height='%d' fill='%s' stroke='%s' stroke-width='1.3'/>"
                 % (x, y, C, FLAT, fill(k, t, cross[1]), GREEN))
        for g in range(1, 10):
            s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='0.6'/>"
                     % (x, y + g * C, x + C, y + g * C, GREEN))
        if k >= t - cross[1]:
            s.append(slash(x, y + 18, C, FLAT - 36))
        x += C + ROD_GAP
    x = xs[2]
    for k in range(o):
        col, r = divmod(k, 5)
        cx = x + col * (C + CUBE_GAP)
        cy = y + FLAT - C - r * (C + CUBE_GAP)                 # stack from the bottom
        s.append("<rect x='%d' y='%d' width='%d' height='%d' fill='%s' stroke='%s' stroke-width='1.3'/>"
                 % (cx, cy, C, C, fill(k, o, cross[2]), GREEN))
        if k >= o - cross[2]:
            s.append(slash(cx, cy, C, C))
    return "".join(s)


def blocks_svg(rows, sign=False, cross=(0, 0, 0), label=None):
    """rows: list of (h, t, o). Flats, rods and cubes line up in columns, so the same kinds sit together.
    sign=True puts a big + in front of the second row."""
    m = 6
    lead = 30 if sign else 0
    cw = [max(part_widths(*r)[k] for r in rows) for k in range(3)]
    xs, x = [], m + lead
    for k in range(3):
        xs.append(x)
        if cw[k]:
            x += cw[k] + PART_GAP
    W = x - PART_GAP + m
    H = 2 * m + len(rows) * FLAT + (len(rows) - 1) * 14
    s = []
    for i, r in enumerate(rows):
        y = m + i * (FLAT + 14)
        s.append(draw_row(xs, y, *r, cross=cross if i == 0 else (0, 0, 0)))
        if sign and i == 1:
            s.append(text(m + 11, y + FLAT / 2 + 9, "+", 28, col=GREEN))
    if label is None:
        label = " and ".join(str(num([o, t, h])) for h, t, o in rows)
    return svg_wrap(W, H, "".join(s), "base-ten blocks showing " + label)


def jw(j):
    j = abs(j)
    return 116 if j >= 100 else 80 if j >= 10 else 56


def nline_svg(start, jumps, ticks=None, jlabels=None):
    """Open number line. Jumps go right for +, left for −. ticks: one label per point (None = no label)."""
    pts = [start]
    for j in jumps:
        pts.append(pts[-1] + j)
    if ticks is None:
        ticks = [str(start)] + [None] * (len(jumps) - 1) + ["?"]
    if jlabels is None:
        jlabels = [("+%d" % j) if j > 0 else ("−%d" % -j) for j in jumps]
    m, ry, ly = 30, 24, 50
    W = 2 * m + sum(jw(j) for j in jumps)
    H = ly + 32
    xs = [m] if jumps[0] > 0 else [W - m]
    for j in jumps:
        xs.append(xs[-1] + (jw(j) if j > 0 else -jw(j)))
    s = ["<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='2.5'/>" % (m - 18, ly, W - m + 18, ly, INK)]
    for k, j in enumerate(jumps):
        x1, x2 = xs[k], xs[k + 1]
        rx = abs(x2 - x1) / 2
        s.append("<path d='M %d %d A %.1f %d 0 0 %d %d %d' fill='none' stroke='%s' stroke-width='2.5'/>"
                 % (x1, ly, rx, ry, 1 if x2 > x1 else 0, x2, ly, GREEN))
        s.append("<polyline points='%d,%d %d,%d %d,%d' fill='none' stroke='%s' stroke-width='2.5' "
                 "stroke-linejoin='round'/>" % (x2 - 5, ly - 10, x2, ly - 2, x2 + 5, ly - 10, GREEN))
        s.append(text((x1 + x2) / 2, ly - ry - 7, jlabels[k], 15, col=GREEN))
    for x, t in zip(xs, ticks):
        s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='2'/>" % (x, ly - 6, x, ly + 6, INK))
        if t is not None:
            s.append(text(x, ly + 24, t, 16))
    op = "plus" if jumps[0] > 0 else "minus"
    return svg_wrap(W, H, "".join(s), "open number line starting at %d with jumps of %s" % (
        start, ", ".join(jlabels).replace("−", "minus ")))


# ============================================================ set 1: add and subtract 10 or 100
def set_mental(rnd, P):
    its = []

    def plus10(n, word):
        d = digits(n)
        q = ("What is %d + 10?" % n) if word == 0 else ("What is 10 more than %d?" % n)
        e = ("Adding 10 changes only the tens digit. It goes from %d to %d. The hundreds and ones stay the same. "
             "%d + 10 = <b>%d</b>." % (d[1], d[1] + 1, n, n + 10))
        return mcq(q, n + 10, [n + 1, n + 100, n - 10, n + 11], e)

    def minus10(n, word):
        d = digits(n)
        q = ("What is %d − 10?" % n) if word == 0 else ("What is 10 less than %d?" % n)
        e = ("Subtracting 10 changes only the tens digit. It goes from %d to %d. %d − 10 = <b>%d</b>."
             % (d[1], d[1] - 1, n, n - 10))
        return mcq(q, n - 10, [n - 1, n - 100, n + 10], e)

    def plus100(n, word):
        d = digits(n)
        q = ("What is %d + 100?" % n) if word == 0 else ("What is 100 more than %d?" % n)
        e = ("Adding 100 changes only the hundreds digit. It goes from %d to %d. %d + 100 = <b>%d</b>."
             % (d[2], d[2] + 1, n, n + 100))
        return mcq(q, n + 100, [n + 10, n + 1, n - 100], e)

    def minus100(n, word):
        d = digits(n)
        q = ("What is %d − 100?" % n) if word == 0 else ("What is 100 less than %d?" % n)
        e = ("Subtracting 100 changes only the hundreds digit. It goes from %d to %d. %d − 100 = <b>%d</b>."
             % (d[2], d[2] - 1, n, n - 100))
        return mcq(q, n - 100, [n - 10, n - 1, n + 100], e)

    easy = []
    for k, n in enumerate([345, 512, 768, 230]):
        assert digits(n)[1] < 9
        easy.append(plus10(n, k % 2))
    for k, n in enumerate([486, 853, 627]):
        assert digits(n)[1] > 0
        easy.append(minus10(n, k % 2))
    for k, n in enumerate([274, 509, 836]):
        easy.append(plus100(n, k % 2))
    for k, n in enumerate([718, 405]):
        easy.append(minus100(n, k % 2))
    rnd.shuffle(easy)
    its += easy

    # pictures
    its.append(mcq(fig(blocks_svg([(2, 4, 3)])) + "The blocks show 243. What number is 10 more?", 253, [244, 343, 233],
                   "10 more is 1 more rod. 4 tens become 5 tens: <b>253</b>. The flats and cubes stay the same."))
    its.append(mcq(fig(blocks_svg([(3, 1, 5)])) + "The blocks show 315. What number is 100 less?", 215, [305, 314, 415],
                   "100 less is 1 flat fewer. 3 hundreds become 2 hundreds: <b>215</b>. The rod and cubes stay the same."))

    # crossing a hundred
    for n, wrong in [(395, [305, 396, 495]), (692, [602, 693, 792])]:
        d = digits(n)
        assert d[1] == 9 and n + 10 not in wrong
        e = ("%d has 9 tens. 1 more ten makes 10 tens, and 10 tens make 1 hundred. So %d hundreds become %d hundreds, "
             "and the tens become 0. %d + 10 = <b>%d</b>." % (n, d[2], d[2] + 1, n, n + 10))
        its.append(mcq("What is %d + 10?" % n, n + 10, wrong, e))
    for n, wrong in [(402, [492, 401, 302]), (805, [895, 804, 705])]:
        d = digits(n)
        assert d[1] == 0 and n - 10 not in wrong
        e = ("%d has 0 tens. Trade 1 hundred for 10 tens: %d hundreds and 10 tens. Take away 1 ten: 9 tens are left. "
             "%d − 10 = <b>%d</b>. The hundreds go down too." % (n, d[2] - 1, n, n - 10))
        its.append(mcq("What is %d − 10?" % n, n - 10, wrong, e))

    # counting patterns
    its.append(mcq("Count by 10s: 470, 480, 490, ☐. What comes next?", 500, [4100, 491, 590],
                   "490 + 10 = <b>500</b>. 49 tens and 1 more ten make 50 tens, which is 5 hundreds."))
    its.append(mcq("Count back by 100s: 850, 750, 650, ☐. What comes next?", 550, [640, 450, 649],
                   "Each number is 100 less. 650 − 100 = <b>550</b>. Only the hundreds digit changes."))
    assert len(its) == 20, len(its)
    return {"title": "Add and subtract 10 or 100", "items": its}


# ============================================================ set 2: add with base-ten blocks (no regrouping)
def pick_pair(rnd, seen, test, hmax=3, tmax=6):
    while True:
        da = [rnd.randint(1, 7), rnd.randint(0, tmax), rnd.randint(1, hmax)]
        db = [rnd.randint(1, 7), rnd.randint(0, tmax), rnd.randint(1, hmax)]
        a, b = num(da), num(db)
        if (a, b) in seen or (b, a) in seen or not test(a, b):
            continue
        seen.add((a, b))
        return a, b


def set_blocks(rnd, P, seen):
    its = []
    for k in range(8):
        a, b = pick_pair(rnd, seen, lambda a, b: not regroups_add(a, b) and digits(a)[1] + digits(b)[1] > 1)
        da, db = digits(a), digits(b)
        pic = fig(blocks_svg([(da[2], da[1], da[0]), (db[2], db[1], db[0])], sign=True))
        s = a + b
        ds = digits(s)
        count = ("Count the same kinds together. Flats: %d + %d = %d hundreds. Rods: %d + %d = %d tens. "
                 "Cubes: %d + %d = %d ones. That is <b>%d</b>." % (da[2], db[2], ds[2], da[1], db[1], ds[1], da[0], db[0], ds[0], s))
        if k % 2 == 0:
            q = pic + "What is %d + %d? Use the blocks." % (a, b)
        else:
            q = pic + "Put the blocks together. What number do they show?"
        its.append(mcq(q, s, near_cands(s, rnd), count))

    its.append(mcq("What is 300 + 400?", 700, [70, 3400, 600],
                   "3 hundreds + 4 hundreds = 7 hundreds. 300 + 400 = <b>700</b>."))
    its.append(mcq("What is 250 + 300?", 550, [280, 253, 650],
                   "300 is 3 hundreds. Add them to the hundreds: 2 + 3 = 5 hundreds. 250 + 300 = <b>550</b>."))
    its.append(mcq("What is 600 + 40?", 640, [1000, 604, 6040],
                   "600 is 6 hundreds and 40 is 4 tens. They are different places, so do not add 6 + 4. "
                   "600 + 40 = <b>640</b>."))
    its.append(mcq("What is 120 + 70?", 190, [820, 127, 180],
                   "70 is 7 tens. 2 tens + 7 tens = 9 tens. 120 + 70 = <b>190</b>."))

    for a, b in [(341, 225), (513, 264)]:
        da, db = digits(a), digits(b)
        h, t, o = (da[2] + db[2]) * 100, (da[1] + db[1]) * 10, da[0] + db[0]
        right = "%d + %d + %d" % (h, t, o)
        wrong = ["%d + %d + %d" % (h, t, da[0]), "%d + %d + %d" % (da[2] * 100, t, o), "%d + %d + %d" % (h // 100, t // 10, o)]
        its.append(mcq("Which is the same as %d + %d?" % (a, b), right, wrong,
                       "Add each place. " + split_e(a, b)))
    for a, b in [(432, 156), (217, 361)]:
        assert not regroups_add(a, b)
        da, db = digits(a), digits(b)
        q = ("Break apart %d + %d. Hundreds: %d + %d. Tens: %d + %d. Ones: %d + %d. What is the total?"
             % (a, b, da[2] * 100, db[2] * 100, da[1] * 10, db[1] * 10, da[0], db[0]))
        its.append(mcq(q, a + b, near_cands(a + b, rnd), split_e(a, b)))

    for a, b in [(425, 32), (413, 54), (342, 26), (351, 47)]:
        assert not regroups_add(a, b)
        s = a + b
        db = digits(b)
        e = ("%d is %d tens and %d ones. It has no hundreds. Tens: %d + %d = %d. Ones: %d + %d = %d. Answer: <b>%d</b>."
             % (b, db[1], db[0], digits(a)[1], db[1], digits(s)[1], digits(a)[0], db[0], digits(s)[0], s))
        its.append(mcq("What is %d + %d?" % (a, b), s, [a + b * 10, a + db[1] * 10, s + 10, s + 100], e))
    assert len(its) == 20, len(its)
    return {"title": "Add with base-ten blocks", "items": its}


# ============================================================ set 3: add with regrouping
def set_regroup_add(rnd, P, seen):
    its = []
    for h, t, o, wrong in [(3, 14, 2, [3142, 342, 432]), (5, 2, 13, [5213, 523, 633]), (2, 11, 6, [2116, 216, 306])]:
        n = 100 * h + 10 * t + o
        if t >= 10:
            e = ("%d tens is 1 hundred and %s. So there are %s, %s and %s: <b>%d</b>."
                 % (t, pl(t - 10, 1), pl(h + 1, 2), pl(t - 10, 1), pl(o, 0), n))
        else:
            e = ("%d ones is 1 ten and %s. So there are %s, %s and %s: <b>%d</b>."
                 % (o, pl(o - 10, 0), pl(h, 2), pl(t + 1, 1), pl(o - 10, 0), n))
        assert n not in wrong
        its.append(mcq("You have %s. What number is that?" % pv(h, t, o), n, wrong, e))

    for k in range(6):
        a, b = pick_pair(rnd, seen, lambda a, b: regroups_add(a, b) == [0] and digits(a)[1] + digits(b)[1] <= 8)
        da, db = digits(a), digits(b)
        pic = fig(blocks_svg([(da[2], da[1], da[0]), (db[2], db[1], db[0])], sign=True))
        e = ("There are %d cubes. Trade 10 cubes for 1 rod. " % (da[0] + db[0])) + add_e(a, b)
        its.append(mcq(pic + "What is %d + %d? Use the blocks." % (a, b), a + b, add_cands(a, b, rnd), e))

    for k in range(3):
        a, b = pick_pair(rnd, seen, lambda a, b: regroups_add(a, b) == [0], hmax=4, tmax=8)
        its.append(mcq("What is %d + %d?" % (a, b), a + b, add_cands(a, b, rnd), add_e(a, b)))
    for k in range(6):
        a, b = pick_pair(rnd, seen, lambda a, b: regroups_add(a, b) == [1] and digits(a)[0] + digits(b)[0] < 10,
                         hmax=4, tmax=9)
        tt = digits(a)[1] + digits(b)[1]
        e = split_e(a, b) + (" (%d tens make 1 hundred%s.)" % (tt, " and " + pl(tt - 10, 1) if tt > 10 else ""))
        its.append(mcq("What is %d + %d?" % (a, b), a + b, add_cands(a, b, rnd), e))

    for a, b in [(298, 145), (399, 226)]:
        need = 100 - a % 100
        top = a + need
        s = a + b
        e = ("Take %d from %d to make %d + %d = %d. Now add the rest: %d + %d = <b>%d</b>."
             % (need, b, a, need, top, top, b - need, s))
        its.append(mcq("Make a hundred first. What is %d + %d?" % (a, b), s,
                       [top + b, add_no_regroup(a, b), s + 10, s - 10], e))
    assert len(its) == 20, len(its)
    return {"title": "Add with regrouping", "items": its}


# ============================================================ set 4: subtract with models and regrouping
def set_subtract(rnd, P, seen):
    its = []
    for k in range(5):
        while True:
            da = [rnd.randint(3, 8), rnd.randint(2, 6), rnd.randint(2, 4)]
            db = [rnd.randint(1, da[0] - 1), rnd.randint(1, da[1] - 1), rnd.randint(1, da[2] - 1)]
            a, b = num(da), num(db)
            if (a, b) not in seen:
                seen.add((a, b))
                break
        r = a - b
        dr = digits(r)
        pic = fig(blocks_svg([(da[2], da[1], da[0])], cross=(db[2], db[1], db[0]),
                             label="%d with %d crossed out" % (a, b)))
        e = ("Count the blocks that are not crossed out. Flats: %d − %d = %d. Rods: %d − %d = %d. Cubes: %d − %d = %d. "
             "%d − %d = <b>%d</b>." % (da[2], db[2], dr[2], da[1], db[1], dr[1], da[0], db[0], dr[0], a, b, r))
        its.append(mcq(pic + "The blocks show %d. The crossed-out blocks are %d. What is %d − %d?" % (a, b, a, b),
                       r, near_cands(r, rnd), e))

    trades = [
        (452, (4, 4, 12), [(4, 5, 12), (3, 4, 12), (4, 4, 2)],
         "Trade 1 ten for 10 ones. 5 tens become 4 tens, and 2 ones become 12 ones. It is still 452."),
        (615, (5, 11, 5), [(6, 11, 5), (5, 1, 5), (5, 11, 15)],
         "Trade 1 hundred for 10 tens. 6 hundreds become 5 hundreds, and 1 ten becomes 11 tens. It is still 615."),
        (503, (4, 10, 3), [(5, 10, 3), (4, 0, 3), (4, 10, 13)],
         "503 has 0 tens. Trade 1 hundred for 10 tens: 4 hundreds and 10 tens. It is still 503."),
    ]
    for n, right, wrong, e in trades:
        assert 100 * right[0] + 10 * right[1] + right[2] == n
        assert all(100 * w[0] + 10 * w[1] + w[2] != n for w in wrong)
        its.append(mcq("Which is the same as %d?" % n, pv(*right), [pv(*w) for w in wrong], e))

    for k, where in enumerate([[0]] * 4 + [[1]] * 3):
        while True:
            a = rnd.randint(300, 980)
            b = rnd.randint(110, a - 100)
            if regroups_sub(a, b) == where and digits(a)[1] != 0 and (a, b) not in seen and a - b >= 100:
                seen.add((a, b))
                break
        its.append(mcq("What is %d − %d?" % (a, b), a - b, sub_cands(a, b, rnd), sub_e(a, b)))

    for a, b in [(503, 128), (402, 156)]:
        assert regroups_sub(a, b) == [0, 1] and digits(a)[1] == 0
        its.append(mcq("What is %d − %d?" % (a, b), a - b, sub_cands(a, b, rnd), sub_e(a, b, check=False)))

    nm, he, his = P.next()
    its.append(mcq("%s says 534 − 218 = 316. Which addition checks %s answer?" % (nm, his), "316 + 218 = 534",
                   ["316 + 534 = 850", "534 + 218 = 752", "316 + 200 = 516"],
                   "Add the answer to the number you took away. You should get the number you started with. "
                   "316 + 218 = 534, so the answer is right."))
    its.append(mcq("397 and 402 are close. Count up to find 402 − 397.", 5, [195, 15, 105],
                   "Count up from 397: 397 + 3 = 400, then 400 + 2 = 402. 3 + 2 = <b>5</b>."))
    its.append(mcq("598 and 600 are close. Count up to find 600 − 598.", 2, [198, 12, 102],
                   "Count up from 598: 598 + 2 = 600. So 600 − 598 = <b>2</b>."))
    assert len(its) == 20, len(its)
    return {"title": "Subtract with models and regrouping", "items": its}


# ============================================================ set 5: number lines and stories
def jumps_of(n):
    d = digits(n)
    return [x for x in (d[2] * 100, d[1] * 10, d[0]) if x]


def set_lines(rnd, P):
    its = []
    for start, b in [(245, 123), (316, 245), (478, 122)]:
        j = jumps_of(b)
        end = start + b
        pts = [start]
        for x in j:
            pts.append(pts[-1] + x)
        steps = ", ".join("+%d to %d" % (x, p) for x, p in zip(j, pts[1:]))
        e = "Start at %d. Jump %s. You land on <b>%d</b>. So %d + %d = %d." % (start, steps, end, start, b, end)
        its.append(mcq(fig(nline_svg(start, j)) + "Start at %d. Make the jumps. Where do you land?" % start,
                       end, [end - 10, end + 10, end - 100, end + 100], e))
    for start, b in [(587, 234), (650, 145)]:
        j = [-x for x in jumps_of(b)]
        end = start - b
        pts = [start]
        for x in j:
            pts.append(pts[-1] + x)
        steps = ", ".join("back %d to %d" % (-x, p) for x, p in zip(j, pts[1:]))
        e = "Start at %d. Jump %s. You land on <b>%d</b>. So %d − %d = %d." % (start, steps, end, start, b, end)
        its.append(mcq(fig(nline_svg(start, j)) + "Start at %d. Jump back. Where do you land?" % start,
                       end, [end + 10, end - 10, end + 100, start + b], e))

    its.append(mcq(fig(nline_svg(380, [20, 100], ticks=["380", "400", "500"])) +
                   "The number line counts up from 380 to 500. What is 500 − 380?", 120, [220, 20, 100, 880],
                   "Add the jumps: 20 + 100 = <b>120</b>. Counting up from 380 to 500 is 120, so 500 − 380 = 120."))
    its.append(mcq(fig(nline_svg(425, [100, 50], ticks=["425", "525", "575"], jlabels=["+100", "+?"])) +
                   "What is the missing jump?", "+50", ["+5", "+500", "+150"],
                   "From 525 to 575, only the tens change: 2 tens become 7 tens. That is 5 tens, so the jump is <b>+50</b>."))
    its.append(mcq("Which jumps show 263 + 134 on a number line?", "+100, +30, +4",
                   ["+100, +40, +3", "+1, +3, +4", "+100, +3, +4"],
                   "134 is 1 hundred, 3 tens and 4 ones. So jump <b>+100, +30, +4</b>: 263, 363, 393, 397."))

    def add_story(t, a, b, unit):
        nm, he, his = P.next()
        q = t.format(n=nm, he=he, He=cap(he), his=his)
        return mcq(q, "%d %s" % (a + b, unit), ["%d %s" % (v, unit) for v in add_cands(a, b, rnd)],
                   "Put the two groups together, so add. " + add_e(a, b))

    def sub_story(t, a, b, unit, lead="Some are taken away, so subtract. "):
        nm, he, his = P.next()
        q = t.format(n=nm, he=he, He=cap(he), his=his)
        return mcq(q, "%d %s" % (a - b, unit), ["%d %s" % (v, unit) for v in sub_cands(a, b, rnd)],
                   lead + sub_e(a, b))

    its.append(add_story("A school has 352 boys and 325 girls. How many children are there in all?", 352, 325, "children"))
    its.append(add_story("A farm has 168 hens and 225 ducks. How many birds are there in all?", 168, 225, "birds"))
    its.append(add_story("{n} read 136 pages last month and 182 pages this month. How many pages did {he} read in all?",
                         136, 182, "pages"))
    its.append(add_story("A store has 457 red balloons and 236 blue balloons. How many balloons does it have?",
                         457, 236, "balloons"))
    nm, he, his = P.next()
    its.append(mcq("%s has 245 stickers. %s gets 100 more. How many stickers does %s have now?" % (nm, cap(he), he),
                   "345 stickers", ["255 stickers", "246 stickers", "145 stickers"],
                   "Adding 100 changes only the hundreds: 2 hundreds become 3 hundreds. 245 + 100 = <b>345</b>."))
    nm, he, his = P.next()
    its.append(mcq("%s has 390 points in a game. %s wins 10 more points. How many points does %s have now?"
                   % (nm, cap(he), he), "400 points", ["3100 points", "391 points", "490 points"],
                   "390 has 9 tens. 1 more ten makes 10 tens, which is 1 hundred. So 390 + 10 = <b>400</b>."))
    its.append(sub_story("A box has 486 beads. {n} uses 152 beads. How many beads are left?", 486, 152, "beads"))
    its.append(sub_story("A library has 725 books. Kids take home 318 books. How many books are still there?",
                         725, 318, "books"))
    its.append(sub_story("A bakery made 540 cookies. It sold 270 cookies. How many cookies are left?", 540, 270, "cookies"))
    its.append(sub_story("A school has 300 milk cartons. Kids drink 125 at lunch. How many cartons are left?",
                         300, 125, "cartons"))
    its.append(sub_story("A red tower has 365 blocks. A blue tower has 142 blocks. How many more blocks does the red tower have?",
                         365, 142, "blocks", lead="How many more means find the difference, so subtract. "))
    nm, he, his = P.next()
    its.append(mcq("%s needs 600 points to win. %s has 450 points. How many more points does %s need?" % (nm, cap(he), he),
                   "150 points", ["1050 points", "250 points", "50 points"],
                   "Count up from 450: 450 + 50 = 500, then 500 + 100 = 600. 50 + 100 = <b>150</b>. Check: 450 + 150 = 600."))
    assert len(its) == 20, len(its)
    return {"title": "Number lines and word problems", "items": its}


# ============================================================ lesson
def body_html():
    return (
        "<h2>Add the same places</h2>"
        "<p>A 3-digit number has <b>hundreds, tens and ones</b>. To add, put hundreds with hundreds, tens with tens "
        "and ones with ones. To subtract, take away hundreds from hundreds, tens from tens and ones from ones.</p>"
        "<h2>Add or take away 10 and 100 in your head</h2>"
        "<p>Adding 10 changes the <b>tens</b> digit. Adding 100 changes the <b>hundreds</b> digit. "
        "Watch for 9 tens or 0 tens: then the hundreds change too.</p>"
        + table(["Number", "+ 10", "+ 100", "− 10", "− 100"], [
            ["345", "355", "445", "335", "245"],
            ["395", "<b>405</b>", "495", "385", "295"],
            ["602", "612", "702", "<b>592</b>", "502"],
        ]) +
        "<h2>Add with base-ten blocks</h2>"
        "<p>A flat is 1 hundred. A rod is 1 ten. A small cube is 1 one. Build both numbers. "
        "Then count the flats, the rods and the cubes.</p>"
        "<figure class='sn-fig'>" + blocks_svg([(2, 3, 4), (1, 5, 2)], sign=True) +
        "<figcaption>234 + 152. Flats: 2 + 1 = 3 hundreds. Rods: 3 + 5 = 8 tens. Cubes: 4 + 2 = 6 ones. "
        "Answer: 386.</figcaption></figure>"
        "<h2>Regroup: make a ten or a hundred</h2>"
        "<p><b>10 ones make 1 ten. 10 tens make 1 hundred.</b> When you have 10 or more cubes, trade 10 cubes for 1 rod.</p>"
        "<figure class='sn-fig'>" + blocks_svg([(3, 4, 12)], label="3 hundreds, 4 tens and 12 ones") +
        "<figcaption>3 hundreds, 4 tens and 12 ones. Trade 10 cubes for 1 rod: 3 hundreds, 5 tens and 2 ones. "
        "That is 352.</figcaption></figure>"
        + ex("Add", "What is 256 + 127?",
             "Ones: 6 + 7 = 13. Make a ten: 1 ten and 3 ones. Tens: 5 + 2 + 1 = 8. Hundreds: 2 + 1 = 3.", "383")
        + "<p>To subtract when there are not enough ones, do it the other way: trade 1 ten for 10 ones.</p>"
        + ex("Subtract", "What is 352 − 126?",
             "Ones: 2 − 6? Not enough ones. Trade 1 ten for 10 ones: 12 − 6 = 6. Tens: 4 − 2 = 2. Hundreds: 3 − 1 = 2. "
             "Check: 226 + 126 = 352.", "226")
        + "<h2>Jump on an open number line</h2>"
        "<p>Start at the first number. Jump the hundreds, then the tens, then the ones.</p>"
        "<figure class='sn-fig'>" + nline_svg(245, [100, 20, 3], ticks=["245", "345", "365", "368"]) +
        "<figcaption>245 + 123: jump +100 to 345, +20 to 365 and +3 to 368. To subtract, jump back to the left.</figcaption></figure>"
        "<h2>Common mistakes</h2>"
        + table(["Mistake", "What to do instead"], [
            ["Adding 10 to the ones: 345 + 10 = 346", "10 is 1 ten. Change the tens digit: 355"],
            ["Writing 395 + 10 = 3105", "10 tens make 1 hundred: 405"],
            ["Not making a ten: 256 + 127 = 373", "13 ones is 1 ten and 3 ones. Add the new ten: 383"],
            ["Taking the small digit from the big one: 352 − 126 = 234", "Trade 1 ten for 10 ones: 12 − 6 = 6. Answer: 226"],
            ["Adding a 2-digit number to the hundreds: 425 + 32 = 745", "32 is 3 tens and 2 ones: 457"],
        ])
    )


FAQ = [
    {"q": "How do you teach adding 10 and 100 in your head in 2nd grade?",
     "a": "Show that adding 10 changes only the tens digit and adding 100 changes only the hundreds digit: 345 + 10 = 355 and 345 + 100 = 445. Practice the tricky ones too: 395 + 10 = 405, because 10 tens make 1 hundred."},
    {"q": "How do base-ten blocks help with 3-digit addition?",
     "a": "Children build each number with flats (hundreds), rods (tens) and cubes (ones), then put the same kinds together. When there are 10 or more cubes, they trade 10 cubes for 1 rod. That trade is regrouping."},
    {"q": "How do you subtract across a zero, like 503 − 128?",
     "a": "There are no tens to trade, so first trade 1 hundred for 10 tens, then 1 ten for 10 ones. Now 503 is 4 hundreds, 9 tens and 13 ones, and 503 − 128 = 375."},
    {"q": "What is an open number line?",
     "a": "It is a line with no fixed scale. Children start at one number and jump by hundreds, tens and ones: for 245 + 123, jump +100 to 345, +20 to 365 and +3 to 368."},
]


def gen():
    rnd = random.Random(207)
    P = People(rnd)
    seen_add, seen_sub = set(), set()
    sets = [set_mental(rnd, P), set_blocks(rnd, P, seen_add), set_regroup_add(rnd, P, seen_add),
            set_subtract(rnd, P, seen_sub), set_lines(rnd, P)]
    balance(sets, rnd)
    seen = set()
    for s in sets:
        assert len(s["items"]) == 20, (s["title"], len(s["items"]))
        assert sorted(it["a"] for it in s["items"]) == sorted([0, 1, 2, 3] * 5)
        for it in s["items"]:
            assert len(set(it["c"])) == 4, it
            for c in it["c"]:
                v = int(re.sub(r"[^0-9]", "", c.split(" ")[0]) or 1)
                # numbers stay within 1000, except a few wrong answers that show a real mistake (3105, 1050 …)
                assert 0 < v <= 1000 or v in (3105, 3100, 3142, 5213, 2116, 3400, 6040, 4100, 1050), c
            k = it["q"] + "|" + "|".join(sorted(it["c"]))
            assert k not in seen, it["q"]
            seen.add(k)
    u = {
        "country": "us", "subject": "math", "grade": "grade-2", "slug": "add-subtract-within-1000", "sort": 7,
        "updated": UPDATED, "pdf_url": "",
        "title": "Add and Subtract Within 1000 with Models",
        "seo_title": "Grade 2 Add and Subtract Within 1000 Worksheets: Base-Ten Blocks, Number Lines, Adding 10 and 100",
        "short_title": "Add and subtract within 1000",
        "domain": "Number and Operations in Base Ten",
        "standard_code": "2.NBT.B.7–8",
        "standard_url": "https://www.thecorestandards.org/Math/Content/2/NBT/B/",
        "standard_text": "Add and subtract within 1000, using concrete models or drawings and strategies based on place value, properties of operations, and/or the relationship between addition and subtraction; relate the strategy to a written method. Understand that in adding or subtracting three-digit numbers, one adds or subtracts hundreds and hundreds, tens and tens, ones and ones; and sometimes it is necessary to compose or decompose tens or hundreds. Mentally add 10 or 100 to a given number 100–900, and mentally subtract 10 or 100 from a given number 100–900.",
        "meta_desc": "Free Grade 2 worksheets for adding and subtracting within 1000 with models: add 10 and 100 in your head, add with base-ten blocks, make a ten or a hundred, subtract across zeros and jump on an open number line. 100 practice questions with simple answers explained.",
        "key_big": "Add hundreds to hundreds, tens to tens and ones to ones.",
        "key_sub": "10 ones make 1 ten, and 10 tens make 1 hundred. Adding 10 changes the tens digit, and adding 100 changes the hundreds digit: 345 + 10 = 355 and 345 + 100 = 445.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }
    mark_large(u, "(base-ten blocks|open number line)")
    return u


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
