# -*- coding: utf-8 -*-
"""
UK Year 2 Maths: Adding and subtracting 2-digit numbers (National Curriculum in England)
  python3 tools/gen_uk_maths_y2_add_sub.py
A two-digit number and ones; a two-digit number and tens; two two-digit numbers; three one-digit numbers.
Tens and ones blocks, number lines and counters (no formal columns: those come in Year 3).
Every answer and every wrong answer is computed and checked in code.
HTML attributes use single quotes (no backslashes in the JSON).
"""
import json, os, random, re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "uk", "maths", "year-2")
UPDATED = "2026-11-02"
GREEN = "#006633"
FILL = "#cfe6d6"
RED = "#c0392b"
BLUE = "#2f6db5"
INK = "#2b2b2b"
FONT = "Arial, Helvetica, sans-serif"
GIRLS = ["Amelia", "Isla", "Freya", "Poppy", "Ava", "Aisha", "Lily", "Zara", "Grace", "Ruby", "Maya", "Evie"]
BOYS = ["Oliver", "Harry", "Mohammed", "Jack", "Arjun", "Noah", "George", "Leo", "Alfie", "Kai", "Ethan", "Charlie"]


# ------------------------------------------------------------ typical mistakes
def cands_add(a, b):
    """Wrong answers from real Year 2 mistakes."""
    s = a + b
    ta, oa, tb, ob = a // 10, a % 10, b // 10, b % 10
    out = []
    if oa + ob >= 10:
        out.append((ta + tb) * 10 + (oa + ob) % 10)        # did not cross the ten: 47 + 6 = 43
    if b < 10:
        out.append(a + 10 * b)                              # added the ones to the tens: 47 + 6 = 107
    elif ob == 0 and a >= 10:
        out.append(a + tb)                                  # added the tens to the ones: 34 + 20 = 36
    out += [s + 10, s - 10, s + 1, s - 1]
    return [v for v in out if 0 < v != s]


def cands_sub(a, b):
    r = a - b
    ta, oa, tb, ob = a // 10, a % 10, b // 10, b % 10
    out = []
    if ob > oa:
        out.append((ta - tb) * 10 + (ob - oa))             # smaller from larger: 63 − 28 = 45
        out.append(r + 10)                                  # exchanged but kept the ten: 52 − 7 = 55
    if b < 10 and a - 10 * b > 0:
        out.append(a - 10 * b)                              # took the ones from the tens: 58 − 3 = 28
    elif b >= 10 and ob == 0:
        out.append(a - tb)                                  # took the tens from the ones: 81 − 30 = 78
    out += [a + b, r - 10, r + 1, r - 1]
    return [v for v in out if 0 < v != r and v != a]


# ------------------------------------------------------------ explanations (short, Year 2 words)
def tens_word(k):
    return "1 ten" if k == 1 else "%d tens" % k


def e_add(a, b):
    s = a + b
    ta, oa, tb, ob = a // 10, a % 10, b // 10, b % 10
    if b < 10:
        if oa + b < 10:
            return ("Add the ones: %d + %d = %d. The tens stay the same. %d + %d = <b>%d</b>."
                    % (oa, b, oa + b, a, b, s))
        if oa + b == 10:
            return ("%d ones + %d ones = 10 ones = 1 more ten. So %d + %d = <b>%d</b>." % (oa, b, a, b, s))
        need = 10 - oa
        return ("Make the next ten first. %d + %d = %d. %d is %d + %d, so add %d more: %d + %d = <b>%d</b>."
                % (a, need, a + need, b, need, b - need, b - need, a + need, b - need, s))
    if ob == 0:
        return ("%d is %s. Add the tens: %s + %s = %s. The ones stay the same. %d + %d = <b>%d</b>."
                % (b, tens_word(tb), tens_word(ta), tens_word(tb), tens_word(ta + tb), a, b, s))
    return ("Add the tens: %d + %d = %d. Add the ones: %d + %d = %d. Then %d + %d = <b>%d</b>."
            % (10 * ta, 10 * tb, 10 * (ta + tb), oa, ob, oa + ob, 10 * (ta + tb), oa + ob, s))


def e_sub_ones(a, b):
    r = a - b
    oa = a % 10
    if b < oa:
        return ("Take away the ones: %d − %d = %d. The tens stay the same. %d − %d = <b>%d</b>."
                % (oa, b, oa - b, a, b, r))
    if b == oa:
        return ("%d − %d takes away all the ones. %d − %d = <b>%d</b>." % (a, b, a, b, r))
    back = a - oa
    return ("Go back to the ten first. %d − %d = %d. %d is %d + %d, so take away %d more: %d − %d = <b>%d</b>."
            % (a, oa, back, b, oa, b - oa, b - oa, back, b - oa, r))


def e_sub(a, b):
    r = a - b
    ta, tb, ob = a // 10, b // 10, b % 10
    if b < 10:
        return e_sub_ones(a, b)
    if ob == 0:
        return ("%d is %s. Take away the tens: %s − %s = %s. The ones stay the same. %d − %d = <b>%d</b>."
                % (b, tens_word(tb), tens_word(ta), tens_word(tb), tens_word(ta - tb), a, b, r))
    m = a - 10 * tb
    first = "Take away the tens first: %d − %d = %d. " % (a, 10 * tb, m)
    if ob <= m % 10:
        return first + "Then take away the ones: %d − %d = <b>%d</b>." % (m, ob, r)
    o = m % 10
    if o == 0:
        return first + "Then take away the ones: %d − %d = <b>%d</b>." % (m, ob, r)
    return first + ("Then take away %d. Go back to the ten: %d − %d = %d, then %d − %d = <b>%d</b>."
                    % (ob, m, o, m - o, m - o, ob - o, r))


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


def money(p):
    return "%dp" % p if p < 100 else "£%d.%02d" % divmod(p, 100)


# ------------------------------------------------------------ pictures: tens and ones blocks
C = 6              # one small cube; a rod (one ten) is 1 × 10 cubes
ROD, ROD_GAP, PART_GAP, CUBE_GAP = 10 * C, 4, 16, 4


def part_widths(t, o):
    cols = (o + 4) // 5
    return [t * (C + ROD_GAP) - ROD_GAP if t else 0,
            cols * (C + CUBE_GAP) - CUBE_GAP if o else 0]


def slash(x, y, w, h):
    return ("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='2.2' stroke-linecap='round'/>"
            % (x - 2, y + h + 2, x + w + 2, y - 2, RED))


def draw_row(xs, y, t, o, cross=(0, 0)):
    s = []

    def fill(k, n, c):
        return "#ffffff" if k >= n - c else FILL

    x = xs[0]
    for k in range(t):
        s.append("<rect x='%d' y='%d' width='%d' height='%d' fill='%s' stroke='%s' stroke-width='1.3'/>"
                 % (x, y, C, ROD, fill(k, t, cross[0]), GREEN))
        for g in range(1, 10):
            s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='0.6'/>"
                     % (x, y + g * C, x + C, y + g * C, GREEN))
        if k >= t - cross[0]:
            s.append(slash(x, y + 18, C, ROD - 36))
        x += C + ROD_GAP
    x = xs[1]
    for k in range(o):
        col, r = divmod(k, 5)
        cx = x + col * (C + CUBE_GAP)
        cy = y + ROD - C - r * (C + CUBE_GAP)
        s.append("<rect x='%d' y='%d' width='%d' height='%d' fill='%s' stroke='%s' stroke-width='1.3'/>"
                 % (cx, cy, C, C, fill(k, o, cross[1]), GREEN))
        if k >= o - cross[1]:
            s.append(slash(cx, cy, C, C))
    return "".join(s)


def blocks_svg(rows, sign=False, cross=(0, 0), label=None):
    """rows: list of (tens, ones). Rods and cubes line up in columns. sign=True puts + before row 2."""
    m = 6
    lead = 30 if sign else 0
    cw = [max(part_widths(*r)[k] for r in rows) for k in range(2)]
    xs, x = [], m + lead
    for k in range(2):
        xs.append(x)
        if cw[k]:
            x += cw[k] + PART_GAP
    W = x - PART_GAP + m
    H = 2 * m + len(rows) * ROD + (len(rows) - 1) * 14
    s = []
    for i, r in enumerate(rows):
        y = m + i * (ROD + 14)
        s.append(draw_row(xs, y, *r, cross=cross if i == 0 else (0, 0)))
        if sign and i == 1:
            s.append(text(m + 11, y + ROD / 2 + 9, "+", 28, col=GREEN))
    if label is None:
        label = " and ".join(str(10 * t + o) for t, o in rows)
    return svg_wrap(W, H, "".join(s), "tens and ones blocks showing " + label)


def blocks_of(n):
    return (n // 10, n % 10)


# ------------------------------------------------------------ pictures: number line
def jw(j):
    return 80 if abs(j) >= 10 else 56


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


def bridge(a, b, sub=False):
    """Split ones at the next (or last) ten: 47 + 6 → +3, +3."""
    if sub:
        return [-(a % 10), -(b - a % 10)]
    return [10 - a % 10, b - (10 - a % 10)]


# ------------------------------------------------------------ pictures: counters for three numbers
def counters_svg(nums):
    cols = [GREEN, RED, BLUE]
    r, step, m, sign = 7, 18, 8, 34
    gw = [min(n, 5) * step for n in nums]
    W = 2 * m + sum(gw) + sign * (len(nums) - 1)
    H = 2 * m + 2 * step
    s, x = [], m
    for i, n in enumerate(nums):
        for k in range(n):
            row, c = divmod(k, 5)
            s.append("<circle cx='%d' cy='%d' r='%d' fill='%s'/>" % (x + c * step + step // 2, m + row * step + step // 2,
                                                                      r, cols[i]))
        x += gw[i]
        if i < len(nums) - 1:
            s.append(text(x + sign / 2, m + step + 9, "+", 26))
            x += sign
    return svg_wrap(W, H, "".join(s), "counters in groups of %s" % ", ".join(str(n) for n in nums))


# ------------------------------------------------------------ picking numbers
def pick(rnd, seen, test):
    while True:
        r = test(rnd)
        if r is None:
            continue
        a, op, b = r
        res = a + b if op == "+" else a - b
        if (a, op, b) in seen or ("a", a) in seen or not (10 <= res <= 99):
            continue
        if ("last", op, b) in seen or ("last", op, a % 10) in seen:     # vary the numbers from one question to the next
            continue
        seen.difference_update({x for x in seen if x[0] == "last" and x[1] == op})
        seen.update({("last", op, b), ("last", op, a % 10)})
        seen.add((a, op, b))
        seen.add(("a", a))
        return a, b


def q_add(a, b, pre=""):
    return mcq(pre + "What is %d + %d?" % (a, b), a + b, cands_add(a, b), e_add(a, b))


def q_sub(a, b, pre=""):
    return mcq(pre + "What is %d − %d?" % (a, b), a - b, cands_sub(a, b), e_sub(a, b))


def t_ones(op, cross):
    def f(rnd):
        a, b = rnd.randint(21, 89), rnd.randint(2, 9)
        o = a % 10
        if o == 0:
            return None
        if op == "+":
            return (a, op, b) if (o + b > 10 if cross else o + b < 10) else None
        return (a, op, b) if (b > o if cross else b < o) else None
    return f


def t_tens(op):
    def f(rnd):
        a, k = rnd.randint(12, 89), rnd.randint(2, 6)
        if a % 10 == 0:
            return None
        if op == "+":
            return (a, op, 10 * k) if a + 10 * k <= 99 else None
        return (a, op, 10 * k) if k < a // 10 else None
    return f


def t_two(op, exch):
    def f(rnd):
        a, b = rnd.randint(13, 89), rnd.randint(12, 79)
        oa, ob = a % 10, b % 10
        if oa == 0 or ob == 0 or a // 10 == b // 10 or a % 11 == 0 or b % 11 == 0:
            return None
        if op == "+":
            return (a, op, b) if (oa + ob > 10 if exch else oa + ob < 10) else None
        if b >= a or b // 10 >= a // 10:
            return None
        return (a, op, b) if (ob > oa if exch else ob < oa) else None
    return f


# ============================================================ set 1: a 2-digit number and ones
def set_ones(rnd, seen):
    its = []
    for _ in range(3):
        its.append(q_add(*pick(rnd, seen, t_ones("+", False))))
    for _ in range(3):
        its.append(q_sub(*pick(rnd, seen, t_ones("−", False))))
    a, b = 23, 4
    seen.add((a, "+", b))
    its.append(q_add(a, b, fig(blocks_svg([blocks_of(a), (0, b)], sign=True)) + "Use the blocks. "))
    a, b = 47, 6
    seen.add((a, "+", b))
    it = q_add(a, b, fig(blocks_svg([blocks_of(a), (0, b)], sign=True)) + "Use the blocks. ")
    it["e"] = ("There are 7 + 6 = 13 ones. Exchange 10 ones for 1 ten: 4 tens become 5 tens, and 3 ones are left. "
               "47 + 6 = <b>53</b>.")
    its.append(it)
    a, b = 38, 5
    seen.add((a, "+", b))
    j = bridge(a, b)
    its.append(q_add(a, b, fig(nline_svg(a, j, ticks=[str(a), str(a + j[0]), "?"])) + "Jump to the next ten first. "))
    a, b = 52, 7
    seen.add((a, "−", b))
    j = bridge(a, b, sub=True)
    its.append(q_sub(a, b, fig(nline_svg(a, j, ticks=[str(a), str(a + j[0]), "?"])) + "Jump back to the ten first. "))
    for _ in range(5):
        its.append(q_add(*pick(rnd, seen, t_ones("+", True))))
    for _ in range(5):
        its.append(q_sub(*pick(rnd, seen, t_ones("−", True))))
    assert len(its) == 20, len(its)
    return {"title": "Add and subtract ones", "items": its}


# ============================================================ set 2: a 2-digit number and tens
def set_tens(rnd, seen):
    its = []
    for _ in range(3):
        its.append(q_add(*pick(rnd, seen, t_tens("+"))))
    for _ in range(3):
        its.append(q_sub(*pick(rnd, seen, t_tens("−"))))
    a, b = 34, 20
    seen.add((a, "+", b))
    its.append(q_add(a, b, fig(blocks_svg([blocks_of(a), (2, 0)], sign=True)) + "Use the blocks. "))
    a, b = 76, 30
    seen.add((a, "−", b))
    its.append(q_sub(a, b, fig(blocks_svg([blocks_of(a)], cross=(3, 0), label="76 with 3 tens crossed out"))
                     + "The blocks show 76. 3 tens are crossed out. "))
    a, b = 45, 30
    seen.add((a, "+", b))
    it = q_add(a, b, fig(nline_svg(a, [10, 10, 10], ticks=["45", "55", "65", "?"])) + "Count on in tens. ")
    it["e"] = "Count on 3 tens from 45: 55, 65, 75. The ones stay the same. 45 + 30 = <b>75</b>."
    its.append(it)
    a, b = 82, 40
    seen.add((a, "−", b))
    it = q_sub(a, b, fig(nline_svg(a, [-10, -10, -10, -10], ticks=["82", "72", "62", "52", "?"]))
               + "Count back in tens. ")
    it["e"] = "Count back 4 tens from 82: 72, 62, 52, 42. The ones stay the same. 82 − 40 = <b>42</b>."
    its.append(it)
    seen.update({(57, "+", 10), (63, "−", 10)})
    its.append(mcq("What is 10 more than 57?", 67, [58, 77, 47], "10 more means 1 more ten. 5 tens become 6 tens. "
                   "The ones stay the same: <b>67</b>."))
    its.append(mcq("What is 10 less than 63?", 53, [62, 43, 73], "10 less means 1 fewer ten. 6 tens become 5 tens. "
                   "The ones stay the same: <b>53</b>."))
    its.append(mcq("You add 30 to 24. Which digit changes?", "the tens digit",
                   ["the ones digit", "both digits", "no digits"],
                   "30 is 3 tens, so only the <b>tens digit</b> changes: 24 + 30 = 54."))
    for _ in range(4):
        its.append(q_add(*pick(rnd, seen, t_tens("+"))))
    for _ in range(3):
        its.append(q_sub(*pick(rnd, seen, t_tens("−"))))
    assert len(its) == 20, len(its)
    return {"title": "Add and subtract tens", "items": its}


# ============================================================ set 3: three 1-digit numbers
def e_three(nums):
    s = sum(nums)
    for i in range(3):
        for j in range(i + 1, 3):
            if nums[i] + nums[j] == 10:
                k = 3 - i - j
                return ("Look for a number bond to 10: %d + %d = 10. Then 10 + %d = <b>%d</b>."
                        % (nums[i], nums[j], nums[k], s))
    for i in range(3):
        for j in range(i + 1, 3):
            if nums[i] == nums[j]:
                k = 3 - i - j
                return ("Use a double: %d + %d = %d. Then %d + %d = <b>%d</b>."
                        % (nums[i], nums[j], 2 * nums[i], 2 * nums[i], nums[k], s))
    return ("Add two numbers first: %d + %d = %d. Then %d + %d = <b>%d</b>."
            % (nums[0], nums[1], nums[0] + nums[1], nums[0] + nums[1], nums[2], s))


def cands_three(nums):
    s = sum(nums)
    a, b, c = nums
    return [a + b, b + c, a + c, s - 1, s + 1, s + 10]


def q_three(nums, pre=""):
    q = pre + "What is %d + %d + %d?" % tuple(nums)
    return mcq(q, sum(nums), cands_three(nums), e_three(nums))


def set_three(rnd, seen):
    its = []
    for nums in [(7, 5, 3), (4, 6, 8)]:
        seen.add(tuple(sorted(nums)))
        its.append(q_three(nums, fig(counters_svg(nums)) + "How many counters are there? "))
    its.append(mcq("Look at 7 + 5 + 3. Which two numbers make 10?", "7 and 3", ["7 and 5", "5 and 3", "none of them"],
                   "7 + 3 = 10 is a number bond to 10. So add <b>7 and 3</b> first: 10 + 5 = 15."))
    its.append(mcq("Look at 6 + 9 + 4. Which two numbers make 10?", "6 and 4", ["6 and 9", "9 and 4", "none of them"],
                   "6 + 4 = 10 is a number bond to 10. So add <b>6 and 4</b> first: 10 + 9 = 19."))
    seen.update({(3, 5, 7), (4, 6, 9)})
    # bonds to 10, in different places
    seen.add((5, 5, 7))
    its.append(q_three((5, 7, 5)))
    cap_left = {1: 3, 2: 2, 3: 1, 4: 1}                               # spread the bonds: 1 + 9, 2 + 8, 3 + 7, 4 + 6
    n = 0
    while n < 7:
        x = rnd.choice([1, 2, 3, 4])
        y = rnd.randint(2, 9)
        if cap_left[x] == 0:
            continue
        trio = [x, 10 - x, y]
        rnd.shuffle(trio)
        trio = tuple(trio)
        if tuple(sorted(trio)) in seen or trio[0] + trio[1] == 10 and n % 3:      # mostly not the first two
            continue
        if len(set(trio)) < 3:
            continue
        cap_left[x] -= 1
        seen.add(tuple(sorted(trio)))
        its.append(q_three(trio))
        n += 1
    # near doubles, no bond to 10
    n = 0
    while n < 5:
        d, y = rnd.randint(3, 8), rnd.randint(2, 9)
        if d == 5 or d + y == 10 or y == d:
            continue
        trio = [d, d, y]
        rnd.shuffle(trio)
        trio = tuple(trio)
        if tuple(sorted(trio)) in seen:
            continue
        seen.add(tuple(sorted(trio)))
        its.append(q_three(trio))
        n += 1
    its.append(mcq("Find the missing number: 4 + <b>?</b> + 6 = 17", 7, [13, 11, 8],
                   "4 + 6 = 10. 10 + <b>7</b> = 17. Check: 4 + 7 + 6 = 17."))
    its.append(mcq("Find the missing number: <b>?</b> + 8 + 2 = 19", 9, [11, 17, 10],
                   "8 + 2 = 10. <b>9</b> + 10 = 19. Check: 9 + 8 + 2 = 19."))
    assert 4 + 7 + 6 == 17 and 9 + 8 + 2 == 19
    its.append(mcq("Which is the same as 8 + 3 + 2?", "2 + 8 + 3", ["8 − 3 + 2", "8 + 3 − 2", "8 + 2 + 2"],
                   "You can add numbers in any order. <b>2 + 8 + 3</b> has the same three numbers, so it is also 13."))
    assert len(its) == 20, len(its)
    return {"title": "Add three 1-digit numbers", "items": its}


# ============================================================ set 4: two 2-digit numbers
def set_two(rnd, seen):
    its = []
    for _ in range(2):
        its.append(q_add(*pick(rnd, seen, t_two("+", False))))
    for _ in range(2):
        its.append(q_sub(*pick(rnd, seen, t_two("−", False))))
    a, b = 35, 42
    seen.add((a, "+", b))
    its.append(q_add(a, b, fig(nline_svg(a, [40, 2], ticks=["35", "75", "?"])) + "Add the tens, then the ones. "))
    a, b = 63, 28
    seen.add((a, "−", b))
    it = q_sub(a, b, fig(nline_svg(a, [-20, -3, -5], ticks=["63", "43", "40", "?"]))
               + "Take away the tens, then the ones. ")
    its.append(it)
    a, b = 47, 38
    seen.add((a, "+", b))
    it = q_add(a, b, fig(blocks_svg([blocks_of(a), blocks_of(b)], sign=True)) + "Use the blocks. ")
    it["e"] = ("Tens: 4 + 3 = 7 tens. Ones: 7 + 8 = 15 ones. Exchange 10 ones for 1 ten: 8 tens and 5 ones. "
               "47 + 38 = <b>85</b>.")
    its.append(it)
    a, b = 54, 26
    seen.add((a, "−", b))
    it = q_sub(a, b, fig(blocks_svg([(4, 14)], cross=(2, 6),
                                    label="54 as 4 tens and 14 ones with 2 tens and 6 ones crossed out"))
               + "1 ten was exchanged for 10 ones, so 54 is 4 tens and 14 ones. 26 is crossed out. ")
    it["e"] = ("4 tens − 2 tens = 2 tens. 14 ones − 6 ones = 8 ones. 2 tens and 8 ones make 28. "
               "54 − 26 = <b>28</b>.")
    its.append(it)
    for _ in range(4):
        its.append(q_add(*pick(rnd, seen, t_two("+", True))))
    for _ in range(4):
        its.append(q_sub(*pick(rnd, seen, t_two("−", True))))
    its.append(mcq("Add 20, then take away 1. What is 46 + 19?", 65, [66, 67, 55],
                   "19 is 1 less than 20. 46 + 20 = 66. Then 66 − 1 = <b>65</b>. (66 forgets to take away 1.)"))
    assert 46 + 19 == 65
    its.append(mcq("Find the missing number: 35 + <b>?</b> = 77", 42, [112, 52, 32],
                   "Use the inverse: 77 − 35. 77 − 30 = 47, then 47 − 5 = <b>42</b>. Check: 35 + 42 = 77."))
    assert 35 + 42 == 77
    its.append(mcq("47 + 38 = 85. Which calculation is also true?", "85 − 38 = 47",
                   ["38 − 85 = 47", "85 + 38 = 47", "47 − 38 = 85"],
                   "Subtraction undoes addition. Start at 85 and take away 38: <b>85 − 38 = 47</b>."))
    its.append(mcq("Which is the same as 35 + 42?", "42 + 35", ["42 − 35", "35 − 42", "53 + 24"],
                   "You can add in any order: <b>42 + 35</b> is also 77. You cannot swap the numbers in a subtraction."))
    assert len(its) == 20, len(its)
    return {"title": "Add and subtract two 2-digit numbers", "items": its}


# ============================================================ set 5: word problems
def set_words(P):
    its = []

    def story(t, a, op, b, unit, lead, other=None):
        nm, he, his = P.next()
        q = t.format(n=nm, he=he, He=cap(he), his=his, o=other or "")
        if op == "+":
            r, cs, e = a + b, cands_add(a, b), e_add(a, b)
        else:
            r, cs, e = a - b, cands_sub(a, b), e_sub(a, b)
        its.append(mcq(q, "%d %s" % (r, unit), ["%d %s" % (v, unit) for v in cs], lead + e))

    def three(t, nums, unit, lead):
        nm, he, his = P.next()
        q = t.format(n=nm, he=he, He=cap(he), his=his)
        its.append(mcq(q, "%d %s" % (sum(nums), unit), ["%d %s" % (v, unit) for v in cands_three(nums)],
                       lead + e_three(nums)))

    def pence(t, a, op, b, lead):
        nm, he, his = P.next()
        q = t.format(n=nm, he=he, He=cap(he), his=his, a=money(a), b=money(b))
        r = a + b if op == "+" else a - b
        cs = cands_add(a, b) if op == "+" else cands_sub(a, b)
        e = (e_add(a, b) if op == "+" else e_sub(a, b))
        its.append(mcq(q, money(r), [money(v) for v in cs if v < 100], lead + e.replace("<b>%d</b>" % r, "%d" % r)
                       + " So the answer is <b>%s</b>." % money(r)))

    more, left = "More are added, so add. ", "Some are taken away, so subtract. "
    story("There are 34 books on a shelf. {n} puts 5 more books on the shelf. How many books are on the shelf now?",
          34, "+", 5, "books", more)
    story("{n} has 46 marbles. {He} wins 7 more marbles. How many marbles does {he} have now?",
          46, "+", 7, "marbles", more)
    story("A bus has 52 people on it. 8 people get off. How many people are still on the bus?",
          52, "−", 8, "people", "Some get off, so subtract. ")
    story("There are 26 ducks on a pond. 9 more ducks land. How many ducks are there now?",
          26, "+", 9, "ducks", more)
    story("{n} has 63 stickers. {He} gives 30 stickers to {his} friend. How many stickers does {he} have left?",
          63, "−", 30, "stickers", left)
    story("One bus has 24 children on it. Another bus has 30 children. How many children are there altogether?",
          24, "+", 30, "children", "Altogether means add. ")
    story("There are 81 children in the playground. 40 children go in for lunch. "
          "How many children are still in the playground?", 81, "−", 40, "children", left)
    three("{n} has 7 red pencils, 5 blue pencils and 3 green pencils. How many pencils does {he} have?",
          (7, 5, 3), "pencils", "Add all three numbers. ")
    three("In a game, {n} scores 6 points, then 8 points, then 4 points. How many points does {he} score altogether?",
          (6, 8, 4), "points", "Altogether means add. ")
    story("{n} reads 35 pages on Monday and 42 pages on Tuesday. How many pages does {he} read altogether?",
          35, "+", 42, "pages", "Altogether means add. ")
    story("A farmer has 47 sheep in one field and 38 sheep in another field. How many sheep are there altogether?",
          47, "+", 38, "sheep", "Altogether means add. ")
    story("A shop has 72 apples. It sells 25 apples. How many apples are left?", 72, "−", 25, "apples", left)
    story("A bus has 40 seats. 26 people are sitting down. How many seats are empty?", 40, "−", 26, "seats",
          "Take the seats with people away from all the seats, so subtract. ")
    other = P.next()
    story("{n} has 45 marbles. {o} has 28 marbles. How many more marbles does {n} have than {o}?",
          45, "−", 28, "marbles", "How many more means find the difference, so subtract. ", other=other[0])
    pence("A pencil costs {a}. A rubber costs {b}. {n} buys both. How much does {he} spend?", 45, "+", 38,
          "Buying both means add. ")
    pence("{n} has {a}. {He} spends {b} on a drink. How much money does {he} have left?", 75, "−", 30,
          "Spending means subtract. ")
    nm, he, his = P.next()
    its.append(mcq("An ice lolly costs 35p. %s pays with a £1 coin. How much change does %s get?" % (nm, he),
                   "65p", ["75p", "35p", "66p"],
                   "£1 is 100p. Count on from 35p to 100p: 35p + 5p = 40p, then 40p + 60p = 100p. "
                   "5p + 60p = <b>65p</b>."))
    assert 100 - 35 == 65
    nm, he, his = P.next()
    its.append(mcq("%s has a 50p coin, a 20p coin and a 5p coin. How much money does %s have?" % (nm, he),
                   "75p", ["70p", "55p", "25p"],
                   "Add all three coins: 50p + 20p = 70p, then 70p + 5p = <b>75p</b>."))
    assert 50 + 20 + 5 == 75
    its.append(mcq("There are 45 people on a bus. 8 people get off. Then 20 people get on. "
                   "How many people are on the bus now?", "57 people", ["37 people", "73 people", "17 people"],
                   "Step 1: 45 − 8 = 37. Step 2: 37 + 20 = <b>57</b>. (37 forgets step 2.)"))
    assert 45 - 8 + 20 == 57 and 45 + 8 + 20 == 73 and 45 - 8 - 20 == 17
    nm, he, his = P.next()
    o2 = P.next()
    its.append(mcq("%s has 58 beads. %s has 9 fewer beads than %s. How many beads does %s have?"
                   % (nm, o2[0], nm, o2[0]), "49 beads", ["67 beads", "51 beads", "48 beads"],
                   "Fewer means subtract. 58 − 8 = 50, then 50 − 1 = <b>49</b>."))
    assert 58 - 9 == 49 and 58 + 9 == 67
    assert len(its) == 20, len(its)
    return {"title": "Word problems", "items": its}


# ============================================================ lesson
def body_html():
    return (
        "<h2>Tens and ones</h2>"
        "<p>A 2-digit number is made of <b>tens</b> and <b>ones</b>. 47 is 4 tens and 7 ones. "
        "Add ones to the ones. Add tens to the tens.</p>"
        + table(["Calculation", "Answer", "What changes"], [
            ["42 + 5", "47", "the ones: 2 + 5 = 7"],
            ["42 + 30", "72", "the tens: 4 + 3 = 7"],
            ["68 − 4", "64", "the ones: 8 − 4 = 4"],
            ["68 − 20", "48", "the tens: 6 − 2 = 4"],
        ]) +
        "<h2>Crossing a ten</h2>"
        "<p>Sometimes the ones go past 10. Jump to the next ten first. Then add the rest.</p>"
        "<figure class='sn-fig'>" + nline_svg(47, bridge(47, 6), ticks=["47", "50", "53"]) +
        "<figcaption>47 + 6: jump +3 to 50, then +3 more to 53.</figcaption></figure>"
        + ex("Example", "What is 52 − 7?",
             "Jump back 2 to the ten: 52 − 2 = 50. 7 is 2 + 5, so take away 5 more: 50 − 5 = 45.", "45")
        + "<h2>Adding two 2-digit numbers</h2>"
        "<p>Add the tens. Then add the ones. If there are 10 or more ones, exchange 10 ones for 1 ten.</p>"
        "<figure class='sn-fig'>" + blocks_svg([(4, 7), (3, 8)], sign=True) +
        "<figcaption>47 + 38. 4 tens + 3 tens = 7 tens. 7 ones + 8 ones = 15 ones. "
        "Exchange 10 ones for 1 ten: 8 tens and 5 ones. Answer: 85.</figcaption></figure>"
        + ex("Example", "What is 35 + 42?", "Tens: 30 + 40 = 70. Ones: 5 + 2 = 7. 70 + 7 = 77.", "77")
        + "<h2>Subtracting with an exchange</h2>"
        "<p>If there are not enough ones, exchange 1 ten for 10 ones.</p>"
        "<figure class='sn-fig'>" + blocks_svg([(5, 13)], cross=(2, 8),
                                              label="63 as 5 tens and 13 ones with 28 crossed out") +
        "<figcaption>63 − 28. 63 has only 3 ones. Exchange 1 ten: 5 tens and 13 ones. Take away 2 tens and 8 ones. "
        "3 tens and 5 ones are left. Answer: 35.</figcaption></figure>"
        "<h2>Adding three numbers</h2>"
        "<p>You can add numbers in any order. Look for a number bond to 10 first.</p>"
        "<figure class='sn-fig'>" + counters_svg((7, 5, 3)) +
        "<figcaption>7 + 5 + 3. Add 7 + 3 = 10 first. Then 10 + 5 = 15.</figcaption></figure>"
        "<h2>Check with the inverse</h2>"
        "<p>Subtraction undoes addition. If 47 + 38 = 85, then 85 − 38 = 47.</p>"
        "<h2>Common mistakes</h2>"
        + table(["Mistake", "What to do instead"], [
            ["Adding ones to the tens: 47 + 6 = 107", "6 is 6 ones. Add it to the ones: 53"],
            ["Not crossing the ten: 47 + 6 = 43", "7 + 6 = 13, so the tens go up by 1: 53"],
            ["Adding tens to the ones: 34 + 20 = 36", "20 is 2 tens. Add it to the tens: 54"],
            ["Taking the smaller digit from the larger: 63 − 28 = 45", "Exchange 1 ten for 10 ones: 13 − 8 = 5. Answer: 35"],
        ])
    )


FAQ = [
    {"q": "What addition and subtraction should a Year 2 child know?",
     "a": "The National Curriculum says Year 2 children should add and subtract a two-digit number and ones, a two-digit number and tens, two two-digit numbers, and three one-digit numbers, using objects, pictures and mental methods."},
    {"q": "How do Year 2 children add two 2-digit numbers?",
     "a": "They partition the numbers into tens and ones. For 35 + 42, add the tens (30 + 40 = 70), then the ones (5 + 2 = 7), to get 77. Tens and ones blocks and number lines help."},
    {"q": "Do Year 2 children learn column addition?",
     "a": "Formal column addition and subtraction are taught in Year 3. In Year 2, children use tens and ones blocks, number lines and partitioning, which prepare them for columns."},
    {"q": "How do you add three one-digit numbers?",
     "a": "Look for two numbers that make 10, or a double, and add those first. For 7 + 5 + 3, add 7 + 3 = 10, then 10 + 5 = 15."},
]


def gen():
    rnd = random.Random(2204)
    P = People(rnd)
    seen = set()
    sets = [set_ones(rnd, seen), set_tens(rnd, seen), set_three(rnd, seen), set_two(rnd, seen), set_words(P)]
    balance(sets, rnd)
    allk = set()
    for s in sets:
        assert len(s["items"]) == 20, (s["title"], len(s["items"]))
        assert sorted(it["a"] for it in s["items"]) == sorted([0, 1, 2, 3] * 5)
        for it in s["items"]:
            assert len(set(it["c"])) == 4, it
            k = re.sub(r"<[^>]+>", "", it["q"])
            assert k not in allk, it["q"]
            allk.add(k)
            m = re.search(r"What is (\d+) ([+−]) (\d+)\?$", it["q"])
            if m:
                a, op, b = int(m.group(1)), m.group(2), int(m.group(3))
                assert int(it["c"][it["a"]]) == (a + b if op == "+" else a - b), it["q"]
            m = re.search(r"What is (\d) \+ (\d) \+ (\d)\?$", it["q"])
            if m:
                assert int(it["c"][it["a"]]) == sum(int(x) for x in m.groups()), it["q"]
    u = {
        "country": "uk", "subject": "maths", "grade": "year-2", "slug": "adding-and-subtracting-2-digit-numbers",
        "sort": 4, "updated": UPDATED, "pdf_url": "",
        "title": "Adding and Subtracting 2-Digit Numbers",
        "seo_title": "Year 2 Adding and Subtracting 2-Digit Numbers Worksheets: Tens and Ones, Number Lines and Word Problems",
        "short_title": "Adding and subtracting 2-digit numbers",
        "domain": "Addition and subtraction",
        "standard_code": "Year 2: Addition and subtraction",
        "standard_url": "https://www.gov.uk/government/publications/national-curriculum-in-england-mathematics-programmes-of-study",
        "standard_text": "Add and subtract numbers using concrete objects, pictorial representations, and mentally, including: a two-digit number and ones; a two-digit number and tens; two two-digit numbers; adding three one-digit numbers; solve problems with addition and subtraction.",
        "meta_desc": "Free Year 2 maths worksheets on adding and subtracting 2-digit numbers: add and subtract ones and tens, cross a ten, add two 2-digit numbers, add three 1-digit numbers and solve word problems with tens and ones pictures and number lines. 100 questions with an answer key, matched to the National Curriculum.",
        "key_big": "Add the tens to the tens and the ones to the ones.",
        "key_sub": "34 + 20 = 54 and 34 + 5 = 39. If the ones go past 10, cross to the next ten: 47 + 6 = 53.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }
    return mark_large(u, "tens and ones blocks|open number line|counters")


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
