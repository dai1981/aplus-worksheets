# -*- coding: utf-8 -*-
"""
UK Year 3 Maths: Mental addition and subtraction (National Curriculum in England)
  python3 tools/gen_uk_maths_y3_mental_add_sub.py
A three-digit number and ones, tens or hundreds. Base-ten blocks and number lines.
Every answer and every wrong answer is computed and checked in code.
HTML attributes use single quotes (no backslashes in the JSON).
"""
import json, os, random, re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "uk", "maths", "year-3")
UPDATED = "2026-11-02"
GREEN = "#006633"
FILL = "#cfe6d6"
RED = "#c0392b"
INK = "#2b2b2b"
FONT = "Arial, Helvetica, sans-serif"
GIRLS = ["Amelia", "Isla", "Freya", "Poppy", "Ava", "Aisha", "Lily", "Zara", "Grace", "Ruby", "Maya", "Evie"]
BOYS = ["Oliver", "Harry", "Mohammed", "Jack", "Arjun", "Noah", "George", "Leo", "Alfie", "Kai", "Ethan", "Charlie"]
PLACE = ["ones", "tens", "hundreds"]
ONE = ["one", "ten", "hundred"]


# ------------------------------------------------------------ numbers
def digits(n):
    return [n % 10, (n // 10) % 10, (n // 100) % 10]          # ones first


def pl(k, i):
    """1 ten, 2 tens, 0 tens …"""
    return "%d %s" % (k, ONE[i] if k == 1 else PLACE[i])


def money(p):
    """Pence below £1, pounds and pence from £1."""
    return "%dp" % p if p < 100 else "£%d.%02d" % divmod(p, 100)


def ok(v):
    return 0 < v <= 999


# ------------------------------------------------------------ typical mistakes
def cands_add(a, b):
    """b is ones, tens or hundreds (one non-zero digit). Wrong answers from real mistakes."""
    s = a + b
    da = digits(a)
    i = 0 if b < 10 else 1 if b < 100 else 2
    k = b // 10 ** i
    out = []
    if da[i] + k >= 10:
        out.append(a - da[i] * 10 ** i + ((da[i] + k) % 10) * 10 ** i)   # did not cross: 347 + 6 = 343
    for j in (1, 0, 2):                                                    # added to the wrong digit
        if j != i:
            out.append(a + k * 10 ** j)
    out += [s + 10 ** i, s - 10 ** i]                                      # counted one too many / few
    if i < 2:
        out += [s + 10 ** (i + 1), s - 10 ** (i + 1)]
    return [v for v in out if ok(v) and v != s]


def cands_sub(a, b):
    r = a - b
    da = digits(a)
    i = 0 if b < 10 else 1 if b < 100 else 2
    k = b // 10 ** i
    out = []
    if da[i] < k:
        out.append(a - da[i] * 10 ** i + (k - da[i]) * 10 ** i)          # smaller from larger: 352 − 7 = 355
        out.append(r + 10 ** (i + 1))                                      # exchanged, but did not take 1 away: 412 − 30 = 482
    for j in (1, 0, 2):
        if j != i:
            out.append(a - k * 10 ** j)
    out += [a + b, r + 10 ** i, r - 10 ** i]
    return [v for v in out if ok(v) and v != r and v != a]


# ------------------------------------------------------------ explanations (short, Year 3 words)
def e_add(a, b):
    s = a + b
    da = digits(a)
    i = 0 if b < 10 else 1 if b < 100 else 2
    k = b // 10 ** i
    if da[i] + k < 10:
        return ("%d is %s. Only the %s digit changes: %d + %d = %d. The other digits stay the same. "
                "%d + %d = <b>%d</b>." % (b, pl(k, i), PLACE[i], da[i], k, da[i] + k, a, b, s))
    if i == 0:
        need = 10 - da[0]
        nxt = a + need
        return ("Make the next ten first. %d + %d = %d. %d is %d + %d, so add %d more: %d + %d = <b>%d</b>."
                % (a, need, nxt, b, need, b - need, b - need, nxt, b - need, s))
    t = da[1] + k
    return ("Tens: %d tens + %d tens = %d tens. Exchange 10 tens for 1 hundred. The hundreds go up from %d to %d, "
            "and %s %s left. %d + %d = <b>%d</b>." % (da[1], k, t, da[2], da[2] + 1, pl(t - 10, 1),
                                                     "is" if t - 10 == 1 else "are", a, b, s))


def e_sub(a, b):
    r = a - b
    da = digits(a)
    i = 0 if b < 10 else 1 if b < 100 else 2
    k = b // 10 ** i
    if da[i] >= k:
        return ("%d is %s. Only the %s digit changes: %d − %d = %d. The other digits stay the same. "
                "%d − %d = <b>%d</b>." % (b, pl(k, i), PLACE[i], da[i], k, da[i] - k, a, b, r))
    if i == 0:
        back = a - da[0]
        return ("Go back to the ten first. %d − %d = %d. %d is %d + %d, so take away %d more: %d − %d = <b>%d</b>."
                % (a, da[0], back, b, da[0], b - da[0], b - da[0], back, b - da[0], r))
    return ("%d has %s. You cannot take %d tens from %d. Exchange 1 hundred for 10 tens: %s and %d tens. "
            "%d tens − %d tens = %s. %d − %d = <b>%d</b>." % (a, pl(da[1], 1), k, da[1], pl(da[2] - 1, 2), da[1] + 10,
                                                            da[1] + 10, k, pl(da[1] + 10 - k, 1), a, b, r))


# ------------------------------------------------------------ helpers
def mcq(q, correct, cands, e):
    """4 choices: correct + the first 3 unique distractors. Positions are set later by balance()."""
    correct = str(correct)
    seen = {correct}
    pick = []
    for c in cands:
        c = str(c)
        if c in seen or not c or c.startswith("-") or c.startswith("0"):
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


# ------------------------------------------------------------ pictures
C = 6              # one small cube; a rod is 1 × 10 cubes, a flat is 10 × 10
FLAT, ROD_GAP, FLAT_GAP, PART_GAP, CUBE_GAP = 10 * C, 4, 6, 16, 4


def part_widths(h, t, o):
    cols = (o + 4) // 5
    return [h * (FLAT + FLAT_GAP) - FLAT_GAP if h else 0,
            t * (C + ROD_GAP) - ROD_GAP if t else 0,
            cols * (C + CUBE_GAP) - CUBE_GAP if o else 0]


def slash(x, y, w, h, full=False):
    s = ("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='2.2' stroke-linecap='round'/>"
         % (x - 2, y + h + 2, x + w + 2, y - 2, RED))
    if full:
        s += ("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='2.2' stroke-linecap='round'/>"
              % (x - 2, y - 2, x + w + 2, y + h + 2, RED))
    return s


def draw_row(xs, y, h, t, o, cross=(0, 0, 0)):
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
        cy = y + FLAT - C - r * (C + CUBE_GAP)
        s.append("<rect x='%d' y='%d' width='%d' height='%d' fill='%s' stroke='%s' stroke-width='1.3'/>"
                 % (cx, cy, C, C, fill(k, o, cross[2]), GREEN))
        if k >= o - cross[2]:
            s.append(slash(cx, cy, C, C))
    return "".join(s)


def blocks_svg(rows, sign=False, cross=(0, 0, 0), label=None):
    """rows: list of (h, t, o). Flats, rods and cubes line up in columns. sign=True puts + before row 2."""
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
        label = " and ".join(str(100 * h + 10 * t + o) for h, t, o in rows)
    return svg_wrap(W, H, "".join(s), "base-ten blocks showing " + label)


def blocks_of(n):
    d = digits(n)
    return (d[2], d[1], d[0])


def jw(j):
    j = abs(j)
    return 116 if j >= 100 else 80 if j >= 10 else 56


def nline_svg(start, jumps, ticks=None, jlabels=None):
    """Open number line. Jumps go right for +, left for −. ticks: one label per point (None = no label)."""
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
    return svg_wrap(W, H, "".join(s), "open number line starting at %d with jumps of %s" % (
        start, ", ".join(jlabels).replace("−", "minus ")))


def bridge_jumps(a, b, sub=False):
    """Split b at the next (or last) ten or hundred: 347 + 6 → +3, +3."""
    i = 0 if b < 10 else 1
    unit = 10 ** (i + 1)
    if sub:
        first = a % unit
        return [-first, -(b - first)]
    first = unit - a % unit
    return [first, b - first]


# ------------------------------------------------------------ picking numbers
def pick(rnd, seen, test, lo=101, hi=989):
    while True:
        a = rnd.randint(lo, hi)
        r = test(a, rnd)
        if r is None:
            continue
        b, op = r
        key = (a, op, b)
        res = a + b if op == "+" else a - b
        if key in seen or not (100 <= res <= 999):
            continue
        seen.add(key)
        return a, b


def q_add(a, b, pre=""):
    return mcq(pre + "What is %d + %d?" % (a, b), a + b, cands_add(a, b), e_add(a, b))


def q_sub(a, b, pre=""):
    return mcq(pre + "What is %d − %d?" % (a, b), a - b, cands_sub(a, b), e_sub(a, b))


# tests: return (b, op) or None
def t_add_ones(cross):
    def f(a, rnd):
        o, t = a % 10, (a // 10) % 10
        b = rnd.randint(2, 9)
        if t == 9 or o == 0:
            return None
        if cross and o + b > 10:
            return b, "+"
        if not cross and o + b < 10:
            return b, "+"
        return None
    return f


def t_sub_ones(cross):
    def f(a, rnd):
        o, t = a % 10, (a // 10) % 10
        b = rnd.randint(2, 9)
        if t == 0 or o == b:
            return None
        if cross and b > o >= 1:
            return b, "−"
        if not cross and b < o:
            return b, "−"
        return None
    return f


def t_add_tens(cross):
    def f(a, rnd):
        t = (a // 10) % 10
        k = rnd.randint(2, 9)
        if a % 10 == 0 or (a // 100) == 9:
            return None
        if cross and t + k > 10:
            return 10 * k, "+"
        if not cross and t + k < 10 and t > 0:
            return 10 * k, "+"
        return None
    return f


def t_sub_tens(cross):
    def f(a, rnd):
        t = (a // 10) % 10
        k = rnd.randint(2, 9)
        if a % 10 == 0 or a < 200:
            return None
        if cross and k > t >= 1:
            return 10 * k, "−"
        if not cross and k < t:
            return 10 * k, "−"
        return None
    return f


def t_add_h(a, rnd):
    h = a // 100
    k = rnd.randint(2, 7)
    if h + k <= 9 and a % 100 > 10 and a % 10:
        return 100 * k, "+"
    return None


def t_sub_h(a, rnd):
    h = a // 100
    k = rnd.randint(2, 7)
    if k < h and a % 100 > 10 and a % 10:
        return 100 * k, "−"
    return None


# ============================================================ set 1: ones
def set_ones(rnd, seen):
    its = []
    for k in range(3):
        its.append(q_add(*pick(rnd, seen, t_add_ones(False))))
    for k in range(3):
        its.append(q_sub(*pick(rnd, seen, t_sub_ones(False))))
    # pictures: blocks
    a, b = 234, 5
    seen.add((a, "+", b))
    its.append(q_add(a, b, fig(blocks_svg([blocks_of(a), (0, 0, b)], sign=True)) + "Use the blocks. "))
    a, b = 147, 6
    seen.add((a, "+", b))
    it = q_add(a, b, fig(blocks_svg([blocks_of(a), (0, 0, b)], sign=True)) + "Use the blocks. ")
    it["e"] = "There are 7 + 6 = 13 cubes. Exchange 10 cubes for 1 rod: 4 tens become 5 tens, and 3 ones are left. 147 + 6 = <b>153</b>."
    its.append(it)
    # pictures: number lines
    a, b = 347, 6
    seen.add((a, "+", b))
    j = bridge_jumps(a, b)
    it = q_add(a, b, fig(nline_svg(a, j, ticks=[str(a), str(a + j[0]), "?"])) + "Jump to the next ten first. ")
    its.append(it)
    a, b = 352, 7
    seen.add((a, "−", b))
    j = bridge_jumps(a, b, sub=True)
    its.append(q_sub(a, b, fig(nline_svg(a, j, ticks=[str(a), str(a + j[0]), "?"])) + "Jump back to the ten first. "))
    for k in range(4):
        its.append(q_add(*pick(rnd, seen, t_add_ones(True))))
    for k in range(4):
        its.append(q_sub(*pick(rnd, seen, t_sub_ones(True))))
    # crossing a hundred too
    its.append(q_add(396, 7))
    its.append(q_sub(403, 5))
    seen.update({(396, "+", 7), (403, "−", 5)})
    assert len(its) == 20, len(its)
    return {"title": "Add and subtract ones", "items": its}


# ============================================================ set 2: tens
def set_tens(rnd, seen):
    its = []
    for k in range(3):
        its.append(q_add(*pick(rnd, seen, t_add_tens(False))))
    for k in range(3):
        its.append(q_sub(*pick(rnd, seen, t_sub_tens(False))))
    a, b = 384, 50
    seen.add((a, "+", b))
    it = q_add(a, b, fig(blocks_svg([blocks_of(a), (0, 5, 0)], sign=True)) + "Use the blocks. ")
    its.append(it)
    a, b = 365, 30
    seen.add((a, "−", b))
    its.append(q_sub(a, b, fig(blocks_svg([blocks_of(a)], cross=(0, 3, 0), label="365 with 3 tens crossed out"))
                     + "The blocks show 365. 3 tens are crossed out. "))
    a, b = 470, 60
    seen.add((a, "+", b))
    j = bridge_jumps(a, b)
    it = mcq(fig(nline_svg(a, j, ticks=[str(a), str(a + j[0]), "?"])) + "Jump to the next hundred first. What is 470 + 60?",
             530, cands_add(a, b) + [430],
             "470 + 30 = 500. 60 is 30 + 30, so add 30 more: 500 + 30 = <b>530</b>.")
    its.append(it)
    a, b = 520, 40
    seen.add((a, "−", b))
    j = bridge_jumps(a, b, sub=True)
    its.append(mcq(fig(nline_svg(a, j, ticks=[str(a), str(a + j[0]), "?"])) + "Jump back to the hundred first. What is 520 − 40?",
                   480, cands_sub(a, b),
                   "520 − 20 = 500. 40 is 20 + 20, so take away 20 more: 500 − 20 = <b>480</b>."))
    for k in range(5):
        its.append(q_add(*pick(rnd, seen, t_add_tens(True))))
    for k in range(4):
        its.append(q_sub(*pick(rnd, seen, t_sub_tens(True))))
    its.append(q_sub(405, 20))
    seen.add((405, "−", 20))
    assert len(its) == 20, len(its)
    return {"title": "Add and subtract tens", "items": its}


# ============================================================ set 3: hundreds
def set_hundreds(rnd, seen, P):
    its = []
    for k in range(6):
        its.append(q_add(*pick(rnd, seen, t_add_h)))
    for k in range(6):
        its.append(q_sub(*pick(rnd, seen, t_sub_h)))
    a, b = 245, 300
    seen.add((a, "+", b))
    its.append(q_add(a, b, fig(blocks_svg([blocks_of(a), (3, 0, 0)], sign=True)) + "Use the blocks. "))
    a, b = 635, 200
    seen.add((a, "−", b))
    its.append(q_sub(a, b, fig(blocks_svg([blocks_of(a)], cross=(2, 0, 0), label="635 with 2 hundreds crossed out"))
                     + "The blocks show 635. 2 hundreds are crossed out. "))
    for a, b, word in [(452, 300, "more"), (718, 200, "less"), (163, 500, "more")]:
        assert (a, "+" if word == "more" else "−", b) not in seen
        seen.add((a, "+" if word == "more" else "−", b))
        if word == "more":
            its.append(mcq("What is %d more than %d?" % (b, a), a + b, cands_add(a, b), e_add(a, b)))
        else:
            its.append(mcq("What is %d less than %d?" % (b, a), a - b, cands_sub(a, b), e_sub(a, b)))
    its.append(mcq("You add 400 to 238. Which digit changes?", "the hundreds digit",
                   ["the ones digit", "the tens digit", "all three digits"],
                   "400 is 4 hundreds, so only the <b>hundreds digit</b> changes: 238 + 400 = 638."))
    its.append(mcq("You take away 20 from 465. Which digit changes?", "the tens digit",
                   ["the ones digit", "the hundreds digit", "all three digits"],
                   "20 is 2 tens, and 465 has 6 tens. Only the <b>tens digit</b> changes: 465 − 20 = 445."))
    names = [P.next()[0] for _ in range(3)]
    its.append(mcq("Each child adds to 456. %s adds 3. %s adds 30. %s adds 300. Who gets 756?" % tuple(names),
                   names[2], [names[0], names[1], "Nobody"],
                   "456 + 3 = 459. 456 + 30 = 486. 456 + 300 = 756. So <b>%s</b> gets 756." % names[2]))
    assert 456 + 300 == 756
    assert len(its) == 20, len(its)
    return {"title": "Add and subtract hundreds", "items": its}


# ============================================================ set 4: missing numbers and number facts
def set_missing():
    its = []

    def add(q, right, wrong, e, check):
        assert check, q
        its.append(mcq(q, right, wrong, e))

    for a, s, wrong in [(465, 495, [3, 300, 960]), (352, 359, [70, 700, 711]), (218, 718, [5, 50, 936])]:
        m = s - a
        add("Find the missing number: %d + <b>?</b> = %d" % (a, s), m, wrong,
            "Compare the digits. Only the %s digit is different. So the missing number is <b>%d</b>. Check: %d + %d = %d."
            % (PLACE[0 if m < 10 else 1 if m < 100 else 2], m, a, m, s), all(w != m for w in wrong))
    add("Find the missing number: 386 + <b>?</b> = 394", 8, [12, 80, 4],
        "Count on from 386. 386 + 4 = 390, then 390 + 4 = 394. 4 + 4 = <b>8</b>. Check: 386 + 8 = 394.", 386 + 8 == 394)
    add("Find the missing number: 457 + <b>?</b> = 517", 60, [140, 6, 70],
        "Count on in tens from 457: 467, 477, 487, 497, 507, 517. That is 6 tens = <b>60</b>. Check: 457 + 60 = 517.",
        457 + 60 == 517)
    add("Find the missing number: 684 − <b>?</b> = 654", 30, [3, 300, 40],
        "Only the tens digit changes: 8 tens become 5 tens. 3 tens = <b>30</b>. Check: 684 − 30 = 654.", 684 - 30 == 654)
    add("Find the missing number: 523 − <b>?</b> = 517", 6, [14, 60, 4],
        "Count back from 523: 523 − 3 = 520, then 520 − 3 = 517. 3 + 3 = <b>6</b>. Check: 523 − 6 = 517.", 523 - 6 == 517)
    add("Find the missing number: <b>?</b> + 40 = 372", 332, [412, 368, 342],
        "Use the inverse. 372 − 40 = <b>332</b>. Check: 332 + 40 = 372. (412 comes from adding 40 instead.)", 332 + 40 == 372)
    add("Find the missing number: <b>?</b> − 6 = 427", 433, [421, 487, 432],
        "Use the inverse. 427 + 6: 427 + 3 = 430, then 430 + 3 = <b>433</b>. Check: 433 − 6 = 427.", 433 - 6 == 427)
    add("Find the missing number: <b>?</b> − 200 = 315", 515, [115, 335, 517],
        "Use the inverse. 315 + 200 = <b>515</b>. Check: 515 − 200 = 315.", 515 - 200 == 315)
    add("Find the missing number: <b>?</b> + 300 = 864", 564, [534, 861, 664],
        "Use the inverse. 864 − 300 = <b>564</b>. Only the hundreds digit changes: 8 − 3 = 5.", 564 + 300 == 864)
    add("8 + 5 = 13. Use this fact. What is 348 + 5?", 353, [343, 398, 453],
        "8 ones + 5 ones = 13 ones = 1 ten and 3 ones. So the tens go up by 1: 348 + 5 = <b>353</b>.", 348 + 5 == 353)
    add("7 + 4 = 11. Use this fact. What is 470 + 40?", 510, [410, 474, 610],
        "7 tens + 4 tens = 11 tens = 1 hundred and 1 ten. So the hundreds go up by 1: 470 + 40 = <b>510</b>.",
        470 + 40 == 510)
    add("13 − 6 = 7. Use this fact. What is 413 − 6?", 407, [417, 353, 403],
        "413 is 4 hundreds and 13 ones. 13 ones − 6 ones = 7 ones. So 413 − 6 = <b>407</b>.", 413 - 6 == 407)
    add("347 + 6 = 353. Which calculation is also true?", "353 − 6 = 347",
        ["347 − 6 = 353", "353 + 6 = 347", "6 − 347 = 353"],
        "Subtraction is the inverse of addition. Start at 353 and take away the 6 you added: <b>353 − 6 = 347</b>.", True)
    add("482 + 50 = 532. Which calculation is also true?", "532 − 50 = 482",
        ["532 − 50 = 582", "482 − 50 = 532", "532 + 50 = 482"],
        "Use the inverse. Start at 532 and take away 50: <b>532 − 50 = 482</b>.", 532 - 50 == 482)
    add("Add 10, then take away 1. What is 456 + 9?", 465, [467, 466, 556],
        "9 is 1 less than 10. 456 + 10 = 466. Then 466 − 1 = <b>465</b>. (466 forgets to take away 1.)", 456 + 9 == 465)
    add("Take away 10, then add 1. What is 532 − 9?", 523, [521, 522, 537],
        "9 is 1 less than 10. 532 − 10 = 522. You took away 1 too many, so add it back: 522 + 1 = <b>523</b>.",
        532 - 9 == 523)
    add("How many more make 500? 470 + <b>?</b> = 500", 30, [3, 70, 130],
        "7 tens + 3 tens = 10 tens = 1 hundred. So 470 + <b>30</b> = 500. (70 + 30 = 100, a number bond.)", 470 + 30 == 500)
    add("How many more make 700? 640 + <b>?</b> = 700", 60, [6, 40, 160],
        "4 tens + 6 tens = 10 tens = 1 hundred. So 640 + <b>60</b> = 700. (40 + 60 = 100, a number bond.)", 640 + 60 == 700)
    assert len(its) == 20, len(its)
    return {"title": "Missing numbers and number facts", "items": its}


# ============================================================ set 5: word problems
def set_words(P):
    its = []

    def story(t, a, op, b, unit, lead):
        nm, he, his = P.next()
        q = t.format(n=nm, he=he, He=cap(he), his=his)
        if op == "+":
            r, cs, e = a + b, cands_add(a, b), e_add(a, b)
        else:
            r, cs, e = a - b, cands_sub(a, b), e_sub(a, b)
        its.append(mcq(q, "%d %s" % (r, unit), ["%d %s" % (v, unit) for v in cs], lead + e))

    def pence(t, a, op, b, lead, bt=None):
        nm, he, his = P.next()
        him = "her" if he == "she" else "him"
        q = t.format(n=nm, he=he, He=cap(he), his=his, him=him, a=money(a), b=bt or money(b))
        r = a + b if op == "+" else a - b
        cs = cands_add(a, b) if op == "+" else cands_sub(a, b)
        how = (e_add(a, b) if op == "+" else e_sub(a, b)).replace("<b>", "").replace("</b>", "")
        e = "%s Work in pence: %s = %dp. %s So the answer is %dp = <b>%s</b>." % (lead, money(a), a, how, r, money(r))
        its.append(mcq(q, money(r), [money(v) for v in cs], e))

    more, left = "More are added, so add. ", "Some are taken away, so subtract. "
    story("A library has 346 books. 7 new books arrive. How many books are there now?", 346, "+", 7, "books", more)
    story("{n} walks 485 steps to the park gate. {He} walks 8 more steps to the swings. How many steps is that?",
          485, "+", 8, "steps", "Put the steps together, so add. ")
    story("A school has 423 pupils. 30 pupils go on a school trip. How many pupils stay at school?",
          423, "−", 30, "pupils", left)
    nm, he, his = P.next()
    its.append(mcq("%s is on page 268 of a book. %s reads 50 more pages. Which page is %s on now?" % (nm, cap(he), he),
                   "page 318", ["page 218", "page 273", "page 768"],
                   "Read on, so add. " + e_add(268, 50)))
    assert cands_add(268, 50)[:3] == [218, 273, 768]
    story("A shop has 615 stickers. It sells 200 stickers. How many stickers are left?", 615, "−", 200, "stickers", left)
    story("A football match has 834 fans. 300 fans leave early. How many fans are still watching?",
          834, "−", 300, "fans", left)
    story("A train has 408 seats. 9 seats are empty. How many seats have people in them?", 408, "−", 9, "seats",
          "Take the empty seats away, so subtract. ")
    story("A garden centre has 572 plants. It sells 60 plants. How many plants are left?", 572, "−", 60, "plants", left)
    story("{n} has 695 points in a game. {He} wins 8 more points. How many points does {he} have now?",
          695, "+", 8, "points", more)
    story("A bakery bakes 380 rolls in the morning and 40 rolls in the afternoon. How many rolls is that?",
          380, "+", 40, "rolls", "Put the two amounts together, so add. ")
    story("There are 517 books on the shelves. Pupils borrow 300 books. How many books are still on the shelves?",
          517, "−", 300, "books", left)
    story("{n} has 452 stamps. Freya has 30 more stamps than {n}. How many stamps does Freya have?",
          452, "+", 30, "stamps", "30 more than means add 30. ")
    story("There are 245 cars in a car park. 9 more cars drive in. How many cars are there now?",
          245, "+", 9, "cars", more)
    story("{n} runs 760 m. Then {he} runs 50 m more. How far does {he} run altogether?", 760, "+", 50, "m",
          "Put the two distances together, so add. ")
    nm, he, his = P.next()
    its.append(mcq("A book has 300 pages. %s has read 270 pages. How many pages are left?" % nm,
                   "30 pages", ["3 pages", "570 pages", "130 pages"],
                   "Count on from 270 to 300: 7 tens + 3 tens = 10 tens. So <b>30 pages</b> are left. Check: 270 + 30 = 300."))
    nm, he, his = P.next()
    its.append(mcq("%s has 548 beads. %s gives away 6 beads. Then %s buys 30 more. How many beads does %s have now?"
                   % (nm, cap(he), he, he), "572 beads", ["578 beads", "512 beads", "584 beads"],
                   "Step 1: 548 − 6 = 542. Step 2: 542 + 30 = <b>572</b>. (578 adds the 6 instead of taking it away.)"))
    assert 548 - 6 + 30 == 572 and 548 + 6 + 30 == 584 and 548 - 6 - 30 == 512
    pence("A comic costs {a}. A rubber costs {b}. {n} buys both. How much does {he} spend?", 245, "+", 8,
          "Buying both means add.")
    pence("{n} has {a}. {He} spends {b} on a pencil. How much money does {he} have left?", 512, "−", 40,
          "Spending means subtract.")
    pence("{n} has {a} in {his} money box. Gran gives {him} {b}. How much does {he} have now?", 360, "+", 200,
          "Getting more means add.", bt="£2")
    pence("{n} has {a}. {He} spends {b} on sweets. How much money does {he} have left?", 403, "−", 6,
          "Spending means subtract.")
    assert len(its) == 20, len(its)
    return {"title": "Word problems", "items": its}


# ============================================================ lesson
def body_html():
    j1 = bridge_jumps(347, 6)
    j2 = bridge_jumps(352, 7, sub=True)
    return (
        "<h2>Which digit changes?</h2>"
        "<p>When you add or take away ones, the <b>ones</b> digit changes. With tens, the <b>tens</b> digit changes. "
        "With hundreds, the <b>hundreds</b> digit changes. The other digits stay the same.</p>"
        + table(["Calculation", "Answer", "What changes"], [
            ["342 + 5", "347", "the ones: 2 + 5 = 7"],
            ["342 + 50", "392", "the tens: 4 + 5 = 9"],
            ["342 + 500", "842", "the hundreds: 3 + 5 = 8"],
            ["768 − 300", "468", "the hundreds: 7 − 3 = 4"],
        ]) +
        "<h2>Crossing a ten: use the next ten</h2>"
        "<p>Sometimes the ones go past 10. Then jump to the next ten first, and add the rest.</p>"
        "<figure class='sn-fig'>" + nline_svg(347, j1, ticks=["347", "350", "353"]) +
        "<figcaption>347 + 6: jump +3 to 350, then +3 more to 353.</figcaption></figure>"
        + ex("Example", "What is 352 − 7?",
             "Jump back 2 to the ten: 352 − 2 = 350. 7 is 2 + 5, so take away 5 more: 350 − 5 = 345.", "345")
        + "<figure class='sn-fig'>" + nline_svg(352, j2, ticks=["352", "350", "345"]) +
        "<figcaption>352 − 7: jump back 2 to 350, then back 5 more to 345.</figcaption></figure>"
        "<h2>Crossing a hundred: exchange 10 tens</h2>"
        "<p><b>10 ones make 1 ten. 10 tens make 1 hundred.</b> When the tens go past 10, exchange 10 tens for 1 hundred.</p>"
        "<figure class='sn-fig'>" + blocks_svg([(3, 8, 4), (0, 5, 0)], sign=True) +
        "<figcaption>384 + 50. 8 tens + 5 tens = 13 tens. Exchange 10 tens for 1 hundred: 4 hundreds, 3 tens and 4 ones. "
        "Answer: 434.</figcaption></figure>"
        + ex("Example", "What is 412 − 30?",
             "412 has only 1 ten. Exchange 1 hundred for 10 tens: 3 hundreds and 11 tens. 11 tens − 3 tens = 8 tens.", "382")
        + "<h2>Check with the inverse</h2>"
        "<p>Addition and subtraction undo each other. If 347 + 6 = 353, then 353 − 6 = 347.</p>"
        "<h2>Common mistakes</h2>"
        + table(["Mistake", "What to do instead"], [
            ["Adding to the wrong digit: 347 + 6 = 947 or 407", "6 is 6 ones. Add it to the ones: 353"],
            ["Not crossing the ten: 347 + 6 = 343", "7 + 6 = 13, so the tens go up by 1: 353"],
            ["Taking the smaller digit from the larger: 352 − 7 = 355", "Jump back to 350, then 5 more: 345"],
            ["Forgetting the exchange: 412 − 30 = 482", "Exchange 1 hundred, so 4 hundreds become 3: 382"],
            ["Not crossing the hundred: 384 + 50 = 334", "13 tens is 1 hundred and 3 tens: 434"],
        ])
    )


FAQ = [
    {"q": "What mental maths should a Year 3 child be able to do?",
     "a": "The National Curriculum says Year 3 children should add and subtract in their heads a three-digit number and ones, tens or hundreds, such as 347 + 6, 412 − 30 and 526 + 300."},
    {"q": "How do you add a three-digit number and ones mentally?",
     "a": "If the ones go past 10, jump to the next ten first. For 347 + 6, add 3 to make 350, then add the other 3 to get 353."},
    {"q": "What does exchange mean in Year 3 maths?",
     "a": "Exchange means swapping 10 ones for 1 ten, or 10 tens for 1 hundred. For 412 − 30, exchange 1 hundred for 10 tens so there are 11 tens, then take away 3 tens to get 382."},
    {"q": "What maths do Year 3 children learn?",
     "a": "Year 3 covers numbers to 1,000, mental and column addition and subtraction, the 3, 4 and 8 times tables, fractions, measures, money, time, shapes, and bar charts and pictograms."},
]


def gen():
    rnd = random.Random(3302)
    P = People(rnd)
    seen = set()
    sets = [set_ones(rnd, seen), set_tens(rnd, seen), set_hundreds(rnd, seen, P), set_missing(), set_words(P)]
    balance(sets, rnd)
    allk = set()
    for s in sets:
        assert len(s["items"]) == 20, (s["title"], len(s["items"]))
        assert sorted(it["a"] for it in s["items"]) == sorted([0, 1, 2, 3] * 5)
        for it in s["items"]:
            assert len(set(it["c"])) == 4, it
            k = it["q"] + "|" + "|".join(sorted(it["c"]))
            assert k not in allk, it["q"]
            allk.add(k)
            # verify plain "What is a ± b?" answers
            m = re.search(r"What is (\d+) ([+−]) (\d+)\?$", it["q"])
            if m:
                a, op, b = int(m.group(1)), m.group(2), int(m.group(3))
                assert int(it["c"][it["a"]]) == (a + b if op == "+" else a - b), it["q"]
    u = {
        "country": "uk", "subject": "maths", "grade": "year-3", "slug": "mental-addition-and-subtraction", "sort": 2,
        "updated": UPDATED, "pdf_url": "",
        "title": "Mental Addition and Subtraction",
        "seo_title": "Year 3 Mental Addition and Subtraction Worksheets: Add and Subtract Ones, Tens and Hundreds",
        "short_title": "Mental addition and subtraction",
        "domain": "Addition and subtraction",
        "standard_code": "Year 3: Addition and subtraction",
        "standard_url": "https://www.gov.uk/government/publications/national-curriculum-in-england-mathematics-programmes-of-study",
        "standard_text": "Add and subtract numbers mentally, including: a three-digit number and ones; a three-digit number and tens; a three-digit number and hundreds.",
        "meta_desc": "Free Year 3 maths worksheets on mental addition and subtraction: add and subtract ones, tens and hundreds to a three-digit number, cross a ten or a hundred, find missing numbers and solve word problems. 100 questions with an answer key, matched to the National Curriculum.",
        "key_big": "Find the digit that changes: ones, tens or hundreds.",
        "key_sub": "342 + 5 = 347, 342 + 50 = 392 and 342 + 500 = 842. If the digit goes past 9, cross to the next ten or hundred: 347 + 6 = 353.",
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
