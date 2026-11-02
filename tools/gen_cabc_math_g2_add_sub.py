# -*- coding: utf-8 -*-
"""
CA-BC Grade 2 Math: Adding and subtracting to 100 (BC Mathematics Curriculum, Computational fluency)
  python3 tools/gen_cabc_math_g2_add_sub.py
Adding tens and ones with jumps on an open number line, subtracting with regrouping
(base ten block pictures), mental strategies (make a ten, compensate), estimating and checking,
and British Columbia word problems (salmon counts, a school book fair). Canadian English. All answers are 100 or less.
Every answer and every wrong answer is computed and checked in code.
HTML attributes use single quotes (no backslashes in the JSON).
Helpers are copied from gen_caon_math_g2_add_sub.py.
"""
import json, os, random, re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "ca-bc", "math", "grade-2")
UPDATED = "2026-11-02"
GREEN = "#006633"
FILL = "#cfe6d6"
RED = "#c0392b"
INK = "#2b2b2b"
FONT = "Arial, Helvetica, sans-serif"


# ------------------------------------------------------------ typical mistakes
def small_from_big(a, b):
    """52 − 17 = 45: took the smaller ones digit from the larger one (no regrouping)."""
    ta, oa, tb, ob = a // 10, a % 10, b // 10, b % 10
    return (ta - tb) * 10 + abs(oa - ob)


def cands_add(a, b):
    """Wrong answers from real Grade 2 mistakes."""
    s = a + b
    ta, oa, tb, ob = a // 10, a % 10, b // 10, b % 10
    out = []
    if b >= 10 and ob == 0:
        out.append(a + tb)                                  # added the tens as ones: 45 + 30 = 48
    if oa + ob >= 10:
        out.append(s - 10)                                  # did not regroup: 36 + 27 = 53
    if b < 10:
        out.append(a + 10 * b)                              # added the ones to the tens: 47 + 6 = 107
    elif ob:
        out.append(a + tb + ob)                             # added the tens as ones: 36 + 27 = 45
    out += [s + 10, s - 10, s + 1, s - 1]
    return [v for v in out if 0 < v != s]


def cands_sub(a, b):
    r = a - b
    ta, oa, tb, ob = a // 10, a % 10, b // 10, b % 10
    out = []
    if ob > oa:
        out.append(small_from_big(a, b))                    # 52 − 17 = 45
        out.append(r + 10)                                  # regrouped but did not take the ten away
    if b >= 10 and ob == 0 and a - tb > 0:
        out.append(a - tb)                                  # took the tens away as ones: 76 − 40 = 72
    elif b < 10 and a - 10 * b > 0:
        out.append(a - 10 * b)                              # took the ones away from the tens
    elif b >= 10:
        out.append(a - tb - ob)                             # took the tens away as ones: 68 − 25 = 61
    out += [a + b, r - 10, r + 1, r - 1]
    return [v for v in out if 0 < v != r and v != a]


# ------------------------------------------------------------ explanations (short, Grade 2 words)
def tens_word(k):
    return "1 ten" if k == 1 else "%d tens" % k


def cap(s):
    return s[0].upper() + s[1:]


def e_add(a, b):
    s = a + b
    ta, oa, tb, ob = a // 10, a % 10, b // 10, b % 10
    if b < 10:
        if oa + b < 10:
            return "Add the ones: %d + %d = %d. The tens stay the same. %d + %d = <b>%d</b>." % (oa, b, oa + b, a, b, s)
        need = 10 - oa
        return ("Make the next ten first. %d + %d = %d. %d is %d + %d, so add %d more: %d + %d = <b>%d</b>."
                % (a, need, a + need, b, need, b - need, b - need, a + need, b - need, s))
    if ob == 0:
        return ("%d is %s. Add the tens: %s + %s = %s. The ones stay the same. %d + %d = <b>%d</b>."
                % (b, tens_word(tb), tens_word(ta), tens_word(tb), tens_word(ta + tb), a, b, s))
    e = "Tens: %d + %d = %d. Ones: %d + %d = %d. " % (10 * ta, 10 * tb, 10 * (ta + tb), oa, ob, oa + ob)
    if oa + ob >= 10:
        e += "%d ones is 1 ten and %s. " % (oa + ob, "1 one" if oa + ob == 11 else "%d ones" % (oa + ob - 10))
    return e + "%d + %d = <b>%d</b>." % (10 * (ta + tb), oa + ob, s)


def e_sub(a, b):
    r = a - b
    ta, oa, tb, ob = a // 10, a % 10, b // 10, b % 10
    if b >= 10 and ob == 0:
        return ("%d is %s. Take away the tens: %s − %s = %s. The ones stay the same. %d − %d = <b>%d</b>."
                % (b, tens_word(tb), tens_word(ta), tens_word(tb), tens_word(ta - tb), a, b, r))
    if ob <= oa:
        if b < 10:
            return "Ones: %d − %d = %d. The tens stay the same. %d − %d = <b>%d</b>." % (oa, ob, oa - ob, a, b, r)
        return ("Tens: %d − %d = %d. Ones: %d − %d = %d. %d + %d = <b>%d</b>."
                % (10 * ta, 10 * tb, 10 * (ta - tb), oa, ob, oa - ob, 10 * (ta - tb), oa - ob, r))
    has = "0 ones" if oa == 0 else ("only 1 one" if oa == 1 else "only %d ones" % oa)
    e = ("%d has %s, so regroup 1 ten as 10 ones: %s and %d ones. Ones: %d − %d = %d. "
         % (a, has, tens_word(ta - 1), oa + 10, oa + 10, ob, oa + 10 - ob))
    if b < 10:
        e += ("%s are left. " % cap(tens_word(ta - 1))) if ta - 1 != 1 else "1 ten is left. "
    else:
        e += "Tens: %d − %d = %d. " % (ta - 1, tb, ta - 1 - tb)
    return e + "%d − %d = <b>%d</b>." % (a, b, r)


def e_jumps(start, jumps):
    steps, v = [], start
    for j in jumps:
        w = v + j
        steps.append("%d %s %d = %d." % (v, "+" if j > 0 else "−", abs(j), w))
        v = w
    steps[-1] = steps[-1][:-1].rsplit("= ", 1)[0] + "= <b>%d</b>." % v
    return " ".join(steps)


# ------------------------------------------------------------ helpers
def mcq(q, correct, cands, e):
    """4 choices: correct + the first 3 unique distractors. Positions are set later by balance()."""
    correct = str(correct)
    seen = {correct}
    pick = []
    for c in cands:
        c = str(c)
        lead = c.lstrip("$")
        if c in seen or not c or lead.startswith("-") or lead.startswith("0"):
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


# ------------------------------------------------------------ pictures: base ten blocks (rods and unit cubes)
C = 6              # one unit cube; a rod (one ten) is 1 × 10 cubes
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


def bo(n):
    return (n // 10, n % 10)


def regroup_svg(a, b):
    """a after regrouping 1 ten as 10 ones, with b crossed out."""
    ta, oa = bo(a)
    tb, ob = bo(b)
    assert ob > oa and ta >= 1
    return blocks_svg([(ta - 1, oa + 10)], cross=(tb, ob),
                      label="%d as %d tens and %d ones with %d crossed out" % (a, ta - 1, oa + 10, b))


# ------------------------------------------------------------ pictures: open number line
def jw(j):
    return 80 if abs(j) >= 10 else 56


def nline_svg(start, jumps, ticks=None, jlabels=None):
    """Open number line. Jumps go right for +, left for −. ticks: one label per point (None = no label)."""
    if ticks is None:
        v, ticks = start, [str(start)]
        for j in jumps[:-1]:
            v += j
            ticks.append(str(v))
        ticks.append("?")
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
        s.append(text((x1 + x2) / 2, ly - ry - 7, jlabels[k], 15, col=RED if jlabels[k] == "?" else GREEN))
    for x, t in zip(xs, ticks):
        s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='2'/>" % (x, ly - 6, x, ly + 6, INK))
        if t is not None:
            s.append(text(x, ly + 24, t, 16, col=RED if t == "?" else INK))
    return svg_wrap(W, H, "".join(s), "open number line starting at %d with jumps of %s" % (
        start, ", ".join(jlabels).replace("−", "minus ").replace("?", "an unknown amount")))


# ------------------------------------------------------------ pictures: number line between two tens
def tens_line_svg(n):
    """A number line from the ten below n to the ten above, with n marked."""
    lo = n // 10 * 10
    m, step, ly = 24, 26, 30
    W, H = 2 * m + 10 * step, 72
    s = ["<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='2.5'/>" % (m - 10, ly, W - m + 10, ly, INK)]
    for k in range(11):
        x = m + k * step
        big = k in (0, 5, 10)
        s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='%s'/>"
                 % (x, ly - (9 if big else 6), x, ly + (9 if big else 6), INK, "2.2" if big else "1.4"))
    s.append(text(m, ly + 30, str(lo), 16))
    s.append(text(m + 10 * step, ly + 30, str(lo + 10), 16))
    xn = m + (n - lo) * step
    s.append("<circle cx='%d' cy='%d' r='6' fill='%s'/>" % (xn, ly, RED))
    s.append(text(xn, ly - 13, str(n), 15, col=RED))
    return svg_wrap(W, H, "".join(s), "number line from %d to %d with %d marked" % (lo, lo + 10, n))


# ------------------------------------------------------------ pictures: part-part-whole bar model
def bar_svg(p1, p2, unknown=None):
    """Whole bar on top, the two parts below, drawn to scale. unknown: 'whole', 'p1', 'p2' or None."""
    whole = p1 + p2
    m, BW, bh, gap, minw = 8, 264, 38, 10, 64
    w1 = int(round(BW * p1 / float(whole)))
    w1 = max(minw, min(BW - minw, w1))
    W, H = BW + 2 * m, 2 * m + 2 * bh + gap
    lab = {"whole": whole, "p1": p1, "p2": p2}
    if unknown:
        lab[unknown] = "?"
    y2 = m + bh + gap
    s = ["<rect x='%d' y='%d' width='%d' height='%d' fill='%s' stroke='%s' stroke-width='2'/>" % (m, m, BW, bh, FILL, GREEN),
         "<rect x='%d' y='%d' width='%d' height='%d' fill='#ffffff' stroke='%s' stroke-width='2'/>" % (m, y2, w1, bh, GREEN),
         "<rect x='%d' y='%d' width='%d' height='%d' fill='#ffffff' stroke='%s' stroke-width='2'/>" % (m + w1, y2, BW - w1, bh, GREEN)]
    for cx, cy, k in [(m + BW / 2.0, m + 26, "whole"), (m + w1 / 2.0, y2 + 26, "p1"), (m + w1 + (BW - w1) / 2.0, y2 + 26, "p2")]:
        v = lab[k]
        s.append(text(cx, cy, str(v), 19, col=RED if v == "?" else INK))
    return svg_wrap(W, H, "".join(s), "bar model: whole %s, parts %s and %s" % (lab["whole"], lab["p1"], lab["p2"]))


# ------------------------------------------------------------ question makers
def q_add(a, b, pre=""):
    assert a + b <= 100
    return mcq(pre + "What is %d + %d?" % (a, b), a + b, cands_add(a, b), e_add(a, b))


def q_sub(a, b, pre=""):
    assert 0 < a - b and a <= 100
    return mcq(pre + "What is %d − %d?" % (a, b), a - b, cands_sub(a, b), e_sub(a, b))


def pick_tens(rnd, seen, op):
    while True:
        a, k = rnd.randint(12, 89), rnd.randint(2, 6)
        if a % 10 == 0 or a % 11 == 0:
            continue
        if op == "+" and a + 10 * k > 99:
            continue
        if op == "−" and k >= a // 10:
            continue
        if (a, op) in seen or ("k", op, k) in seen:
            continue
        seen.update({(a, op), ("k", op, k)})
        return a, 10 * k


def jump_q(a, jumps, pre="", text_only=False):
    end = a + sum(jumps)
    b = abs(sum(jumps))
    op = "+" if jumps[0] > 0 else "−"
    assert 0 < end <= 100
    c = [end - jumps[-1]] + (cands_add(a, b) if op == "+" else cands_sub(a, b))
    if text_only:
        words = ", then ".join(str(abs(j)) for j in jumps)
        q = "Start at %d. Jump %s %s. Where do you land?" % (a, "forward" if op == "+" else "back", words)
    else:
        q = fig(nline_svg(a, jumps)) + pre + "What is %d %s %d?" % (a, op, b)
    e = e_jumps(a, jumps) + " So %d %s %d = %d." % (a, op, b, end)
    return mcq(q, end, c, e)


# ============================================================ set 1: add tens and ones with jumps
def set_jump(rnd):
    its = []
    seen = {(46, "+"), (24, "+"), (83, "−"), (58, "+"), (64, "−"), (34, "+"), (27, "+"), (42, "+"), (53, "+"),
            (69, "−"), (78, "−"), (37, "+"), (48, "+"), (65, "−"), (28, "+"), (57, "+")}
    its.append(q_add(46, 30, fig(blocks_svg([bo(46), (3, 0)], sign=True)) + "Use the base ten blocks. "))
    it = q_add(24, 30, fig(nline_svg(24, [10, 10, 10])) + "Count on by tens. ")
    it["e"] = "Count on 3 tens from 24: 34, 44, 54. The ones stay the same. 24 + 30 = <b>54</b>."
    its.append(it)
    it = q_sub(83, 40, fig(nline_svg(83, [-10, -10, -10, -10])) + "Count back by tens. ")
    it["e"] = "Count back 4 tens from 83: 73, 63, 53, 43. The ones stay the same. 83 − 40 = <b>43</b>."
    its.append(it)
    its.append(mcq("What is 10 more than 58?", 68, [59, 78, 48],
                   "10 more means 1 more ten. 5 tens become 6 tens. The ones stay the same: <b>68</b>."))
    its.append(mcq("What is 10 less than 64?", 54, [63, 44, 74],
                   "10 less means 1 less ten. 6 tens become 5 tens. The ones stay the same: <b>54</b>."))
    for i in range(2):
        a, b = pick_tens(rnd, seen, "+")
        its.append(q_add(a, b, fig(nline_svg(a, [10] * (b // 10))) + "Count on by tens. " if i == 0 else ""))
    a, b = pick_tens(rnd, seen, "−")
    its.append(q_sub(a, b))
    its.append(jump_q(34, [40, 3], "Jump the tens, then the ones. "))
    its.append(jump_q(27, [50, 2], "Jump the tens, then the ones. "))
    its.append(jump_q(42, [30, 6], text_only=True))
    its.append(jump_q(53, [20, 5], "Jump the tens, then the ones. "))
    its.append(jump_q(69, [-20, -4], "Jump back the tens, then the ones. "))
    its.append(jump_q(78, [-40, -5], "Jump back the tens, then the ones. "))
    its.append(mcq(fig(nline_svg(46, [30, 3], ["46", "76", "79"], ["?", "+3"])) + "What is the missing jump?",
                   "+30", ["+3", "+33", "+40"],
                   "From 46 to 76, the tens digit goes from 4 to 7. That is 3 tens, so the jump is <b>+30</b>. "
                   "Check: 46 + 33 = 79."))
    assert 46 + 30 == 76 and 46 + 33 == 79
    its.append(mcq(fig(nline_svg(28, [50, 7], ["28", "78", "85"])) + "Which number sentence does the number line show?",
                   "28 + 57 = 85", ["28 + 75 = 85", "85 + 57 = 28", "57 − 28 = 85"],
                   "It starts at 28. It jumps +50 and +7. 50 + 7 = 57, so it shows <b>28 + 57 = 85</b>."))
    assert 28 + 57 == 85
    its.append(jump_q(37, [20, 3, 4], "Jump to the next ten. "))
    its.append(jump_q(48, [30, 2, 5], "Jump to the next ten. "))
    its.append(jump_q(65, [-20, -5, -3], "Jump back to the ten. "))
    its.append(mcq("Find the missing number: 37 + <b>?</b> = 77", 40, [4, 114, 30],
                   "The ones stay at 7. The tens go from 3 to 7. That is 4 tens: <b>40</b>. Check: 37 + 40 = 77."))
    assert 37 + 40 == 77 and 37 + 77 == 114
    assert len(its) == 20, len(its)
    return {"title": "Add tens and ones: jump on a number line", "items": its}


# ============================================================ set 2: subtract with regrouping (base ten pictures)
def set_regroup():
    its = []
    its.append(mcq(fig(blocks_svg([bo(54)])) + "The blocks show 54. You need to take away 18. "
                   "There are not enough ones. What do you do?",
                   "Regroup 1 ten", ["Do 8 − 4", "Write 0 ones", "Take away 2 tens"],
                   "54 has only 4 ones. You need to take away 8. <b>Regroup 1 ten</b> as 10 ones. "
                   "Then there are 14 ones. Doing 8 − 4 instead is a common mistake."))
    its.append(mcq("You regroup 1 ten in 54. What does 54 look like now?", "4 tens and 14 ones",
                   ["5 tens and 14 ones", "4 tens and 4 ones", "3 tens and 14 ones"],
                   "Take 1 ten from the 5 tens: 4 tens are left. The 10 ones join the 4 ones: 14 ones. "
                   "So 54 = <b>4 tens and 14 ones</b>. Check: 40 + 14 = 54."))
    assert 40 + 14 == 54
    for a, b in [(42, 17), (63, 25), (75, 38), (34, 16), (81, 47), (52, 7), (80, 36)]:
        ta, oa = bo(a)
        its.append(q_sub(a, b, fig(regroup_svg(a, b)) +
                         "%d − %d. 1 ten was regrouped as 10 ones. Now there are %s and %d ones. %d is crossed out. "
                         % (a, b, tens_word(ta - 1), oa + 10, b)))
    its.append(mcq("Simran says 54 − 18 = 44. What mistake did she make?", "She did 8 − 4",
                   ["She added the tens", "She added the ones", "She did 14 − 8"],
                   "In the ones, Simran took 4 from 8. But it must be 4 − 8, and you cannot take 8 from 4. "
                   "Regroup: 14 − 8 = 6 and 4 − 1 = 3. So 54 − 18 = 36. Her mistake: <b>she did 8 − 4</b>."))
    assert small_from_big(54, 18) == 44 and 54 - 18 == 36
    for a, b, pic in [(62, 28, True), (93, 47, False), (60, 35, True), (57, 38, False), (84, 56, True),
                      (46, 27, False), (71, 8, False)]:
        assert b % 10 > a % 10
        its.append(q_sub(a, b, (fig(blocks_svg([bo(a)])) + "The blocks show %d. " % a) if pic else ""))
    its.append(q_sub(91, 64))
    its.append(mcq("Find the missing number: 54 − <b>?</b> = 36", 18, [28, 90, 22],
                   "Count on from 36 to 54. 36 + 4 = 40. 40 + 14 = 54. 4 + 14 = <b>18</b>. Check: 54 − 18 = 36."))
    assert 54 - 18 == 36 and 54 + 36 == 90 and small_from_big(54, 36) == 22
    its.append(mcq("Which subtraction needs regrouping?", "64 − 27", ["67 − 24", "78 − 42", "59 − 13"],
                   "In <b>64 − 27</b>, there are only 4 ones. You need to take away 7, so regroup 1 ten. "
                   "In the others, the top ones digit is big enough."))
    assert len(its) == 20, len(its)
    return {"title": "Subtract with regrouping using base ten blocks", "items": its}


# ============================================================ set 3: mental strategies
def set_mental():
    its = []
    its.append(mcq("You want to find 46 + 7. How many does 46 need to make 50?", 4, [3, 6, 10],
                   "46 + 4 = 50. So add <b>4</b> first. 7 is 4 + 3, so then add 3 more: 50 + 3 = 53."))
    assert 46 + 4 == 50 and 46 + 7 == 53
    its.append(jump_q(58, [2, 5], "Jump to the next ten. "))
    its.append(mcq("Which one makes 50?", "43 + 7", ["43 + 8", "42 + 7", "44 + 7"],
                   "3 + 7 = 10, so 43 + 7 = <b>50</b>. The others make 51, 49 and 51."))
    assert 43 + 7 == 50 and 43 + 8 == 51 and 42 + 7 == 49 and 44 + 7 == 51
    its.append(jump_q(63, [-3, -2], "Jump back to the ten. "))
    its.append(mcq("Use a double. 40 + 40 = 80. What is 40 + 39?", 79, [80, 81, 78],
                   "39 is 1 less than 40. So 40 + 39 is 1 less than 80: <b>79</b>."))
    assert 40 + 39 == 79
    for a, b in [(37, 5), (28, 6), (65, 8)]:
        need = 10 - a % 10
        e = "Make the next ten. %d + %d = %d. Then add the rest: %d + %d = <b>%d</b>." % (
            a, need, a + need, a + need, b - need, a + b)
        its.append(mcq("Make a ten. What is %d + %d?" % (a, b), a + b, cands_add(a, b), e))
    its.append(mcq("Make a ten. What is 27 + 15?", 42, [32, 41, 312],
                   "27 needs 3 to make 30. 15 is 3 + 12. 30 + 12 = <b>42</b>."))
    assert 27 + 15 == 42
    its.append(mcq("49 is close to 50. 50 + 26 = 76. Now take away 1. What is 49 + 26?", 75, [76, 77, 65],
                   "You added 1 too many when you used 50. Take it away: 76 − 1 = <b>75</b>. "
                   "(76 forgets to take away 1. 77 adds 1 instead.)"))
    assert 49 + 26 == 75
    for a, b in [(19, 24), (29, 17)]:
        up = a + 1
        its.append(mcq("Use a friendly number. What is %d + %d?" % (a, b), a + b,
                       [up + b, up + b + 1, a + b - 10],
                       "%d is 1 less than %d. %d + %d = %d. Take away 1: <b>%d</b>." % (a, up, up, b, up + b, a + b)))
    its.append(mcq("38 is 2 less than 40. What is 38 + 15?", 53, [55, 43, 51],
                   "40 + 15 = 55. You added 2 too many, so take away 2: 55 − 2 = <b>53</b>. "
                   "(55 forgets to take away 2.)"))
    assert 38 + 15 == 53
    its.append(mcq("Which is the same as 27 + 9?", "27 + 10 − 1", ["27 + 10 + 1", "27 + 9 − 1", "20 + 9 + 1"],
                   "9 is 1 less than 10. Add 10, then take away 1: <b>27 + 10 − 1</b> = 36."))
    assert 27 + 10 - 1 == 27 + 9 == 36
    its.append(mcq("Add 10, then take away 1. What is 33 + 9?", 42, [43, 41, 32],
                   "33 + 10 = 43. You added 1 too many, so take away 1: 43 − 1 = <b>42</b>. "
                   "(43 forgets to take away 1.)"))
    assert 33 + 9 == 42
    its.append(mcq("Which is the same as 35 + 19?", "35 + 20 − 1", ["35 + 20 + 1", "35 + 10 − 1", "30 + 19 + 1"],
                   "19 is 1 less than 20. Add 20, then take away 1: <b>35 + 20 − 1</b> = 54."))
    assert 35 + 20 - 1 == 35 + 19 == 54
    its.append(mcq("Take away 10, then add 1. What is 42 − 9?", 33, [32, 47, 31],
                   "42 − 10 = 32. You took away 1 too many, so add 1: 32 + 1 = <b>33</b>. "
                   "(47 takes 2 from 9 instead of 9 from 2.)"))
    assert 42 - 9 == 33 and small_from_big(42, 9) == 47
    its.append(mcq("Take away 20, then add 1. What is 60 − 19?", 41, [40, 39, 59],
                   "60 − 20 = 40. You took away 1 too many, so add 1: 40 + 1 = <b>41</b>. "
                   "(39 takes away 1 more instead of adding it back.)"))
    assert 60 - 19 == 41 and small_from_big(60, 19) == 59
    its.append(mcq("Use a double. 23 + 23 = 46. What is 23 + 24?", 47, [46, 48, 45],
                   "24 is 1 more than 23. So 23 + 24 is 1 more than 46: <b>47</b>."))
    its.append(mcq("Use a double. 16 + 16 = 32. What is 16 + 17?", 33, [32, 34, 31],
                   "17 is 1 more than 16. So 16 + 17 is 1 more than 32: <b>33</b>."))
    assert 23 + 24 == 47 and 16 + 17 == 33
    assert len(its) == 20, len(its)
    return {"title": "Mental math: next ten, doubles and friendly numbers", "items": its}


# ============================================================ set 4: estimate and check
def near_ten(n):
    assert n % 10 != 5
    return int(round(n / 10.0)) * 10


def set_estimate():
    its = []
    for n, w in [(37, [30, 50, 38]), (53, [60, 40, 54])]:
        t = near_ten(n)
        its.append(mcq(fig(tens_line_svg(n)) + "Which ten is %d closest to?" % n, t, w,
                       "%d is between %d and %d. It is closer to <b>%d</b>." % (n, n // 10 * 10, n // 10 * 10 + 10, t)))
    for n in (72, 28, 84, 61):
        t = near_ten(n)
        other = n // 10 * 10 if t != n // 10 * 10 else n // 10 * 10 + 10
        its.append(mcq("Which ten is %d closest to?" % n, t, [other, n + 1 if n % 10 != 9 else n - 1, t + 10 if t + 10 != other else t - 10],
                       "%d is between %d and %d. It is closer to <b>%d</b>." % (n, n // 10 * 10, n // 10 * 10 + 10, t)))
    for a, op, b in [(39, "+", 22), (48, "+", 31), (62, "+", 27), (63, "−", 37), (71, "−", 18), (41, "+", 28)]:
        ra, rb = near_ten(a), near_ten(b)
        est = ra + rb if op == "+" else ra - rb
        wrong = [est - 10, est + 10, (ra - rb) if op == "+" else (ra + rb)]
        wrong = [w for w in wrong if w > 0][:3]
        assert len(wrong) == 3 and max(wrong) <= 100
        its.append(mcq("Estimate. %d %s %d is about how much?" % (a, op, b), "about %d" % est,
                       ["about %d" % w for w in wrong],
                       "%d is close to %d. %d is close to %d. %d %s %d = <b>%d</b>." % (a, ra, b, rb, ra, op, rb, est)))
    its.append(mcq("Estimate first: 54 − 27 is about 50 − 30 = 20. What is 54 − 27?", 27, [33, 37, 17],
                   "54 has only 4 ones, so regroup: 4 tens and 14 ones. 14 − 7 = 7. 4 − 2 = 2. 54 − 27 = <b>27</b>. "
                   "27 is close to 20, so it makes sense."))
    assert 54 - 27 == 27 and small_from_big(54, 27) == 33
    its.append(mcq("Estimate first: 27 + 44 is about 30 + 40 = 70. What is 27 + 44?", 71, [61, 81, 70],
                   "Tens: 20 + 40 = 60. Ones: 7 + 4 = 11. 60 + 11 = <b>71</b>. 71 is close to 70, so it makes sense."))
    assert 27 + 44 == 71
    its.append(mcq("Estimate first. Which answer to 48 + 25 makes sense?", 73, [613, 23, 55],
                   "48 + 25 is about 50 + 30 = 80. Only <b>73</b> is close to 80. "
                   "613 writes 6 tens and 13 ones side by side. 23 subtracts. 55 adds the tens as ones."))
    assert 48 + 25 == 73 and 48 - 25 == 23 and 48 + 2 + 5 == 55
    its.append(mcq("Noah says 64 − 27 = 43. He estimates 60 − 30 = 30. What should he think?", "43 is too big",
                   ["43 is right", "43 is too small", "30 is the answer"],
                   "43 is far from 30, so <b>43 is too big</b>. Noah did 7 − 4 in the ones. "
                   "Regroup: 14 − 7 = 7 and 5 − 2 = 3. 64 − 27 = 37."))
    assert small_from_big(64, 27) == 43 and 64 - 27 == 37
    its.append(mcq("62 − 25 = 37. Which addition checks the answer?", "37 + 25", ["62 + 25", "37 + 62", "37 + 52"],
                   "Add the answer and the number you took away. You should get back to the start: "
                   "<b>37 + 25</b> = 62."))
    assert 37 + 25 == 62
    its.append(mcq("46 + 37 = 83. Which subtraction checks the answer?", "83 − 37", ["83 + 37", "46 − 37", "83 − 83"],
                   "Take one part away from the total. You should get the other part: <b>83 − 37</b> = 46."))
    assert 83 - 37 == 46
    its.append(mcq("Jasleen says 53 − 16 = 43. She checks: 43 + 16 = 59. Is she right?", "No, 59 is not 53",
                   ["Yes, she is right", "No, 43 + 16 is 53", "Yes, 59 is close"],
                   "The check must give back 53. It gives 59, so <b>she is not right</b>. 53 − 16 = 37."))
    assert 43 + 16 == 59 and 53 - 16 == 37 and small_from_big(53, 16) == 43
    its.append(mcq("Which addition checks 80 − 26 = 54?", "54 + 26 = 80", ["54 + 80 = 26", "80 + 26 = 54", "54 − 26 = 80"],
                   "Add the answer and the number you took away: <b>54 + 26 = 80</b>. You get back to 80."))
    assert 54 + 26 == 80
    assert len(its) == 20, len(its)
    return {"title": "Estimate and check", "items": its}


# ============================================================ set 5: word problems
def set_words():
    its = []

    def add_story(q, a, b, unit, lead, pic=True, money=False):
        s = a + b
        u = (lambda v: "$%d" % v) if money else (lambda v: "%d %s" % (v, unit))
        pre = fig(bar_svg(a, b, "whole")) if pic else ""
        its.append(mcq(pre + q, u(s), [u(v) for v in cands_add(a, b)], lead + e_add(a, b)))

    def sub_story(q, whole, take, unit, lead, pic=True, money=False):
        r = whole - take
        u = (lambda v: "$%d" % v) if money else (lambda v: "%d %s" % (v, unit))
        pre = fig(bar_svg(take, r, "p2")) if pic else ""
        its.append(mcq(pre + q, u(r), [u(v) for v in cands_sub(whole, take)], lead + e_sub(whole, take)))

    whole_lead = "The bar model shows two parts. Find the whole, so add. "
    part_lead = "You know the whole and one part. Find the other part, so subtract. "
    add_story("On a field trip to the river, Liam’s class counts 34 salmon in the morning and 25 salmon after lunch. "
              "How many salmon do they count?", 34, 25, "salmon", whole_lead)
    add_story("At the school book fair, 27 students buy a book on Monday. 18 students buy a book on Tuesday. "
              "How many students buy a book?", 27, 18, "students", whole_lead)
    sub_story("The book fair has 64 picture books. Students buy 28 of them. How many picture books are left?",
              64, 28, "books", part_lead)
    sub_story("A Grade 2 class raises salmon in a tank at school. They have 72 baby salmon. They let 27 go in the creek. "
              "How many baby salmon are still in the tank?", 72, 27, "salmon", part_lead)
    its.append(mcq(fig(bar_svg(29, 36, "p2")) + "Which number sentence finds the missing part?", "65 − 29 = ?",
                   ["65 + 29 = ?", "29 − 65 = ?", "? − 29 = 36"],
                   "The whole is 65. One part is 29. Take the part away from the whole: <b>65 − 29 = ?</b>. "
                   "The missing part is 36."))
    assert 29 + 36 == 65
    add_story("In the Terry Fox Run, 37 Grade 2 students and 46 Grade 3 students ran. How many students ran?",
              37, 46, "students", whole_lead)
    sub_story("There are 53 bald eagles by the river. 17 eagles fly away. How many eagles are still by the river?",
              53, 17, "eagles", part_lead)
    sub_story("Arjun has $20 at the book fair. He buys a book for $12. How much money does he have left?",
              20, 12, "", part_lead, money=True)
    sub_story("Mei read 53 pages. Owen read 38 pages. How many more pages did Mei read?",
              53, 38, "pages", "How many more means find the difference, so subtract. ", pic=False)
    its.append(mcq(fig(bar_svg(18, 15, "p1")) + "Some salmon were in a pool in the river. 15 more salmon swam in. "
                   "Now there are 33. How many salmon were in the pool at first?", "18 salmon",
                   ["48 salmon", "22 salmon", "28 salmon"],
                   "The whole is 33. One part is 15. Subtract. 33 has only 3 ones, so regroup: 2 tens and 13 ones. "
                   "13 − 5 = 8. 2 − 1 = 1. 33 − 15 = <b>18</b>. Check: 18 + 15 = 33."))
    assert 33 - 15 == 18 and small_from_big(33, 15) == 22 and 33 + 15 == 48
    its.append(mcq("There are 46 people at the book fair. 19 people go home. Then 25 more people come. "
                   "How many people are at the book fair now?", "52 people",
                   ["27 people", "90 people", "42 people"],
                   "Step 1: 46 − 19. Regroup: 16 − 9 = 7 and 3 − 1 = 2, so 27. Step 2: 27 + 25. "
                   "Tens: 20 + 20 = 40. Ones: 7 + 5 = 12. 40 + 12 = <b>52</b>. (27 forgets step 2.)"))
    assert 46 - 19 + 25 == 52 and 46 - 19 == 27 and 46 + 19 + 25 == 90
    add_story("On a rainy day in Vancouver, 38 students wear rain boots and 27 students wear running shoes. "
              "How many students is that?", 38, 27, "students", "Find the total, so add. ", pic=False)
    sub_story("The book fair wants to sell 90 books today. It has sold 56 books. How many more books does it need to sell?",
              90, 56, "books", part_lead)
    add_story("For a field trip snack, the class has 26 apples and 34 granola bars. How many snacks is that in all?",
              26, 34, "snacks", "In all means add. ", pic=False)
    its.append(mcq("Kai counts 47 salmon. Ava counts 24 more salmon than Kai. How many salmon does Ava count?",
                   "71 salmon", ["23 salmon", "61 salmon", "81 salmon"],
                   "Ava counts more, so add: 47 + 24. Tens: 40 + 20 = 60. Ones: 7 + 4 = 11. 60 + 11 = <b>71</b>. "
                   "(23 subtracts. 61 forgets to regroup.)"))
    assert 47 + 24 == 71 and 47 - 24 == 23
    sub_story("A BC Ferries boat gets to Nanaimo with 82 cars. 47 cars have driven off. How many cars are still on the boat?",
              82, 47, "cars", part_lead, pic=False)
    add_story("Two classes count salmon at the creek. One class counts 64 salmon. The other class counts 36 salmon. "
              "How many salmon do they count in all?", 64, 36, "salmon", whole_lead)
    its.append(mcq("Harjot has 73 stickers. He gives away 36. Which number sentence finds how many are left?",
                   "73 − 36 = ?", ["73 + 36 = ?", "36 − 73 = ?", "? − 73 = 36"],
                   "He gives some away, so take away. Start with 73 and take away 36: <b>73 − 36 = ?</b>. "
                   "The answer is 37."))
    assert 73 - 36 == 37
    sub_story("A school bus has 72 seats. 47 students are sitting down. How many seats are empty?",
              72, 47, "seats", part_lead, pic=False)
    add_story("Nadia buys a book at the book fair. She reads 36 pages on Saturday and 47 pages on Sunday. "
              "How many pages does she read?", 36, 47, "pages", "Put the two days together, so add. ", pic=False)
    assert len(its) == 20, len(its)
    return {"title": "Word problems: salmon counts and the school book fair", "items": its}


# ============================================================ lesson
def body_html():
    assert 37 + 25 == 62 and 54 - 18 == 36 and 49 + 26 == 75 and 48 + 25 == 73 and 37 + 26 == 63
    return (
        "<h2>The idea: tens with tens, ones with ones</h2>"
        "<p>A 2-digit number has <b>tens</b> and <b>ones</b>. 46 is 4 tens and 6 ones. "
        "Add tens to tens. Add ones to ones.</p>"
        + table(["Number sentence", "Answer", "What changes"], [
            ["46 + 30", "76", "the tens: 4 + 3 = 7"],
            ["46 + 3", "49", "the ones: 6 + 3 = 9"],
            ["78 − 40", "38", "the tens: 7 − 4 = 3"],
        ]) +
        "<h2>Jump on an open number line</h2>"
        "<p>Start at the first number. Jump the tens. Then jump the ones. "
        "Jumping to the next ten makes it easier.</p>"
        "<figure class='sn-fig'>" + nline_svg(37, [20, 3, 2], ["37", "57", "60", "62"]) +
        "<figcaption>37 + 25: jump +20 to 57, +3 to 60, then +2 to 62.</figcaption></figure>"
        "<h2>Subtract with regrouping</h2>"
        "<p>Sometimes there are not enough ones to take away. Regroup 1 ten as 10 ones.</p>"
        "<figure class='sn-fig'>" + regroup_svg(54, 18) +
        "<figcaption>54 − 18. 54 has only 4 ones. Regroup 1 ten: 4 tens and 14 ones. "
        "Ones: 14 − 8 = 6. Tens: 4 − 1 = 3. Answer: 36.</figcaption></figure>"
        "<h2>Mental math: next ten and friendly numbers</h2>"
        "<p><b>Next ten:</b> fill up to the next ten first. 46 + 7: 46 + 4 = 50, then 50 + 3 = 53.</p>"
        + ex("Friendly number", "What is 49 + 26?", "49 is close to 50. 50 + 26 = 76. You added 1 too many, so take away 1: "
             "76 − 1 = 75.", "75") +
        "<h2>Estimate and check</h2>"
        "<p>Before you add, find the closest tens. Your answer should be close to the estimate. "
        "To check a subtraction, add back what you took away.</p>"
        + ex("Estimate", "What is 48 + 25?", "48 is close to 50. 25 is close to 30. 50 + 30 = 80. "
             "The exact answer is 73. 73 is close to 80, so it makes sense.", "73") +
        "<h2>Common mistakes</h2>"
        + table(["Mistake", "What to do instead"], [
            ["Not regrouping: 54 − 18 = 44", "4 − 8 cannot be done. Regroup 1 ten: 14 − 8 = 6. Answer: 36"],
            ["Not regrouping: 37 + 26 = 53", "7 + 6 = 13 ones is 1 ten and 3 ones. Answer: 63"],
            ["Adding tens to ones: 46 + 30 = 49", "30 is 3 tens. Add it to the tens: 76"],
            ["Writing tens and ones side by side: 48 + 25 = 613", "Add the parts: 60 + 13 = 73"],
        ])
    )


FAQ = [
    {"q": "What does Grade 2 learn about adding and subtracting in the BC math curriculum?",
     "a": "In the BC curriculum, Grade 2 students add and subtract to 100. They use number lines, base ten blocks and mental math strategies, and they build on facts to 20."},
    {"q": "What mental math strategies do Grade 2 students use?",
     "a": "Common strategies are jumping to the next ten (46 + 7 = 50 + 3), using doubles (23 + 24 is 1 more than 46) and using a friendly number (49 + 26 = 50 + 26 − 1 = 75)."},
    {"q": "What is regrouping in Grade 2 subtraction?",
     "a": "Regrouping means trading 1 ten for 10 ones when there are not enough ones. For 54 − 18, 54 becomes 4 tens and 14 ones, so the answer is 36."},
    {"q": "How can my child check an addition or subtraction answer?",
     "a": "First estimate with the closest tens: 48 + 25 is about 50 + 30 = 80. Then check a subtraction by adding back: 62 − 25 = 37 because 37 + 25 = 62."},
]


def verify(sets):
    for s in sets:
        for it in s["items"]:
            right = it["c"][it["a"]]
            m = re.search(r"What is (\d+) ([+−]) (\d+)\?$", it["q"])
            if m:
                a, op, b = int(m.group(1)), m.group(2), int(m.group(3))
                v = a + b if op == "+" else a - b
                assert int(right) == v and 0 < v <= 100, it["q"]
            m = re.search(r"Start at (\d+)\. Jump (forward|back) ([\d, then]+)\. Where", it["q"])
            if m:
                js = [int(x) for x in re.findall(r"\d+", m.group(3))]
                v = int(m.group(1)) + (sum(js) if m.group(2) == "forward" else -sum(js))
                assert int(right) == v, it["q"]
            m = re.search(r"aria-label='bar model: whole (\S+), parts (\S+) and (\S+)'", it["q"])
            if m and "number sentence" not in it["q"]:
                vals = [m.group(1), m.group(2), m.group(3)]
                k = vals.index("?")
                n = [int(x) for x in vals if x != "?"]
                want = n[0] + n[1] if k == 0 else n[0] - n[1]
                assert int(right.lstrip("$").split()[0]) == want, it["q"]
            m = re.search(r"aria-label='number line from \d+ to \d+ with (\d+) marked", it["q"])
            if m:
                assert int(right) == near_ten(int(m.group(1))), it["q"]
            m = re.search(r"Estimate\. (\d+) ([+−]) (\d+) is about", it["q"])
            if m:
                a, op, b = int(m.group(1)), m.group(2), int(m.group(3))
                est = near_ten(a) + near_ten(b) if op == "+" else near_ten(a) - near_ten(b)
                assert right == "about %d" % est, it["q"]


def gen():
    rnd = random.Random(52804)
    sets = [set_jump(rnd), set_regroup(), set_mental(), set_estimate(), set_words()]
    balance(sets, rnd)
    verify(sets)
    allk = set()
    for s in sets:
        assert len(s["items"]) == 20, (s["title"], len(s["items"]))
        assert sorted(it["a"] for it in s["items"]) == sorted([0, 1, 2, 3] * 5)
        for it in s["items"]:
            assert len(set(it["c"])) == 4, it
            assert it["q"].count("<svg") <= 1
            k = re.sub(r"<[^>]+>", "", it["q"])
            assert k not in allk, it["q"]
            allk.add(k)
    u = {
        "country": "ca-bc", "subject": "math", "grade": "grade-2", "slug": "adding-and-subtracting-to-100",
        "sort": 4, "updated": UPDATED, "pdf_url": "",
        "title": "Adding and Subtracting to 100: Number Lines, Regrouping and Mental Math",
        "seo_title": "Grade 2 Math Adding and Subtracting to 100 Worksheets (BC Curriculum, Free, Answer Key)",
        "short_title": "Adding and subtracting to 100",
        "domain": "Computational fluency",
        "standard_code": "Grade 2: Computational fluency",
        "standard_url": "https://curriculum.gov.bc.ca/curriculum/mathematics/2/core",
        "standard_text": "Addition and subtraction to 100",
        "meta_desc": "Free Grade 2 math worksheets on adding and subtracting to 100: jumps on a number line, "
                     "regrouping with base ten blocks, mental math, estimating and checking, and word problems "
                     "about salmon counts and a school book fair. 100 questions with an answer key, following the BC curriculum.",
        "key_big": "Add tens to tens and ones to ones. Regroup when you need to.",
        "key_sub": "37 + 25: jump +20 to 57, then +3 to 60 and +2 to 62. For 54 − 18 there are not enough ones, "
                   "so regroup 1 ten as 10 ones: 14 − 8 = 6 and 4 − 1 = 3, so 36.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }
    return mark_large(u, "tens and ones blocks|open number line|number line from|bar model")


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
