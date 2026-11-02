# -*- coding: utf-8 -*-
"""
CA Grade 2 Math: Adding and subtracting to 100 (Ontario Curriculum 2020, B2.3, B2.4)
  python3 tools/gen_caon_math_g2_add_sub.py
Adding tens and ones with jumps on an open number line, subtracting with regrouping
(base ten block pictures), mental strategies (make a ten, compensate), estimating and checking,
and word problems. Canadian English. All answers are 100 or less.
Every answer and every wrong answer is computed and checked in code.
HTML attributes use single quotes (no backslashes in the JSON).
Helpers are copied from gen_au_maths_y2_add_sub.py and gen_caon_math_g3_add_sub.py.
"""
import json, os, random, re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "ca-on", "math", "grade-2")
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


# ------------------------------------------------------------ pictures: two ten frames
def tenframe_svg(a, b):
    """a green counters, then b white counters, filling the first ten frame before the second."""
    assert a < 10 and b < 10 and a + b > 10
    m, cell, gap = 8, 26, 20
    fw = 5 * cell
    W, H = 2 * m + 2 * fw + gap, 2 * m + 2 * cell
    s = []
    for f in range(2):
        x0 = m + f * (fw + gap)
        for r in range(2):
            for c in range(5):
                s.append("<rect x='%d' y='%d' width='%d' height='%d' fill='#ffffff' stroke='%s' stroke-width='1.5'/>"
                         % (x0 + c * cell, m + r * cell, cell, cell, GREEN))
    for k in range(a + b):
        f, i = divmod(k, 10)
        r, c = divmod(i, 5)
        cx = m + f * (fw + gap) + c * cell + cell / 2.0
        cy = m + r * cell + cell / 2.0
        if k < a:
            s.append("<circle cx='%.1f' cy='%.1f' r='9' fill='%s'/>" % (cx, cy, GREEN))
        else:
            s.append("<circle cx='%.1f' cy='%.1f' r='8.5' fill='#ffffff' stroke='%s' stroke-width='2.5'/>" % (cx, cy, RED))
    return svg_wrap(W, H, "".join(s), "ten frames with %d green counters and %d red counters" % (a, b))


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
    seen = {(45, "+"), (23, "+"), (82, "−"), (57, "+"), (63, "−"), (35, "+"), (26, "+"), (41, "+"), (52, "+"),
            (68, "−"), (79, "−"), (38, "+"), (47, "+"), (56, "+"), (36, "+"), (64, "−")}
    its.append(q_add(45, 30, fig(blocks_svg([bo(45), (3, 0)], sign=True)) + "Use the base ten blocks. "))
    it = q_add(23, 30, fig(nline_svg(23, [10, 10, 10])) + "Count on by tens. ")
    it["e"] = "Count on 3 tens from 23: 33, 43, 53. The ones stay the same. 23 + 30 = <b>53</b>."
    its.append(it)
    it = q_sub(82, 40, fig(nline_svg(82, [-10, -10, -10, -10])) + "Count back by tens. ")
    it["e"] = "Count back 4 tens from 82: 72, 62, 52, 42. The ones stay the same. 82 − 40 = <b>42</b>."
    its.append(it)
    its.append(mcq("What is 10 more than 57?", 67, [58, 77, 47],
                   "10 more means 1 more ten. 5 tens become 6 tens. The ones stay the same: <b>67</b>."))
    its.append(mcq("What is 10 less than 63?", 53, [62, 43, 73],
                   "10 less means 1 less ten. 6 tens become 5 tens. The ones stay the same: <b>53</b>."))
    for i in range(2):
        a, b = pick_tens(rnd, seen, "+")
        its.append(q_add(a, b, fig(nline_svg(a, [10] * (b // 10))) + "Count on by tens. " if i == 0 else ""))
    a, b = pick_tens(rnd, seen, "−")
    its.append(q_sub(a, b))
    its.append(jump_q(35, [40, 2], "Jump the tens, then the ones. "))
    its.append(jump_q(26, [50, 3], "Jump the tens, then the ones. "))
    its.append(jump_q(41, [30, 7], text_only=True))
    its.append(jump_q(52, [20, 6], "Jump the tens, then the ones. "))
    its.append(jump_q(68, [-20, -5], "Jump back the tens, then the ones. "))
    its.append(jump_q(79, [-40, -6], "Jump back the tens, then the ones. "))
    its.append(mcq(fig(nline_svg(45, [30, 4], ["45", "75", "79"], ["?", "+4"])) + "What is the missing jump?",
                   "+30", ["+3", "+34", "+40"],
                   "From 45 to 75, the tens digit goes from 4 to 7. That is 3 tens, so the jump is <b>+30</b>. "
                   "Check: 45 + 34 = 79."))
    assert 45 + 34 == 79
    its.append(mcq(fig(nline_svg(29, [50, 6], ["29", "79", "85"])) + "Which number sentence does the number line show?",
                   "29 + 56 = 85", ["29 + 65 = 85", "85 + 56 = 29", "56 − 29 = 85"],
                   "It starts at 29. It jumps +50 and +6. 50 + 6 = 56, so it shows <b>29 + 56 = 85</b>."))
    assert 29 + 56 == 85
    its.append(jump_q(38, [20, 2, 3], "Jump to the next ten. "))
    its.append(jump_q(47, [30, 3, 3], "Jump to the next ten. "))
    its.append(jump_q(64, [-20, -4, -5], "Jump back to the ten. "))
    its.append(mcq("Find the missing number: 36 + <b>?</b> = 76", 40, [4, 112, 30],
                   "The ones stay at 6. The tens go from 3 to 7. That is 4 tens: <b>40</b>. Check: 36 + 40 = 76."))
    assert 36 + 40 == 76 and 36 + 76 == 112
    assert len(its) == 20, len(its)
    return {"title": "Add tens and ones: jump on a number line", "items": its}


# ============================================================ set 2: subtract with regrouping (base ten pictures)
def set_regroup():
    its = []
    its.append(mcq(fig(blocks_svg([bo(52)])) + "The blocks show 52. You need to take away 17. "
                   "There are not enough ones. What do you do?",
                   "Regroup 1 ten", ["Do 7 − 2", "Write 0 ones", "Take away 2 tens"],
                   "52 has only 2 ones. You need to take away 7. <b>Regroup 1 ten</b> as 10 ones. "
                   "Then there are 12 ones. Doing 7 − 2 instead is a common mistake."))
    its.append(mcq("You regroup 1 ten in 52. What does 52 look like now?", "4 tens and 12 ones",
                   ["5 tens and 12 ones", "4 tens and 2 ones", "3 tens and 12 ones"],
                   "Take 1 ten from the 5 tens: 4 tens are left. The 10 ones join the 2 ones: 12 ones. "
                   "So 52 = <b>4 tens and 12 ones</b>. Check: 40 + 12 = 52."))
    assert 40 + 12 == 52
    for a, b in [(43, 18), (61, 25), (74, 36), (35, 19), (82, 46), (53, 8), (90, 34)]:
        ta, oa = bo(a)
        its.append(q_sub(a, b, fig(regroup_svg(a, b)) +
                         "%d − %d. 1 ten was regrouped as 10 ones. Now there are %s and %d ones. %d is crossed out. "
                         % (a, b, tens_word(ta - 1), oa + 10, b)))
    its.append(mcq("Maya says 52 − 17 = 45. What mistake did she make?", "She did 7 − 2",
                   ["She added the tens", "She added the ones", "She did 12 − 7"],
                   "In the ones, Maya took 2 from 7. But it must be 2 − 7, and you cannot take 7 from 2. "
                   "Regroup: 12 − 7 = 5 and 4 − 1 = 3. So 52 − 17 = 35. Her mistake: <b>she did 7 − 2</b>."))
    assert small_from_big(52, 17) == 45 and 52 - 17 == 35
    for a, b, pic in [(64, 27, True), (91, 45, False), (70, 34, True), (56, 29, False), (83, 57, True),
                      (45, 26, False), (81, 9, False)]:
        assert b % 10 > a % 10
        its.append(q_sub(a, b, (fig(blocks_svg([bo(a)])) + "The blocks show %d. " % a) if pic else ""))
    its.append(q_sub(92, 68))
    its.append(mcq("Find the missing number: 52 − <b>?</b> = 35", 17, [27, 87, 23],
                   "Count on from 35 to 52. 35 + 5 = 40. 40 + 12 = 52. 5 + 12 = <b>17</b>. Check: 52 − 17 = 35."))
    assert 52 - 17 == 35 and 52 + 35 == 87 and small_from_big(52, 35) == 23
    its.append(mcq("Which subtraction needs regrouping?", "63 − 28", ["68 − 23", "75 − 41", "49 − 16"],
                   "In <b>63 − 28</b>, there are only 3 ones. You need to take away 8, so regroup 1 ten. "
                   "In the others, the top ones digit is big enough."))
    assert len(its) == 20, len(its)
    return {"title": "Subtract with regrouping using base ten blocks", "items": its}


# ============================================================ set 3: mental strategies
def set_mental():
    its = []
    its.append(mcq(fig(tenframe_svg(8, 5)) + "Fill the first ten frame to make a ten. What is 8 + 5?", 13,
                   [12, 14, 3],
                   "8 needs 2 more to make 10. 5 is 2 + 3. So 8 + 5 = 10 + 3 = <b>13</b>."))
    its.append(mcq(fig(tenframe_svg(9, 6)) + "Fill the first ten frame to make a ten. What is 9 + 6?", 15,
                   [14, 16, 5],
                   "9 needs 1 more to make 10. 6 is 1 + 5. So 9 + 6 = 10 + 5 = <b>15</b>."))
    its.append(mcq(fig(tenframe_svg(7, 6)) + "Make a ten. What is 7 + 6?", 13, [12, 14, 3],
                   "7 needs 3 more to make 10. 6 is 3 + 3. So 7 + 6 = 10 + 3 = <b>13</b>."))
    assert 8 + 5 == 13 and 9 + 6 == 15 and 7 + 6 == 13
    its.append(mcq("Make a ten for 8 + 5. 8 + 2 = 10. How many more do you add?", 3, [5, 2, 7],
                   "5 is 2 + 3. You used 2 to make the ten, so add <b>3</b> more. 10 + 3 = 13."))
    its.append(mcq("Which pair makes a ten?", "6 + 4", ["6 + 5", "7 + 4", "5 + 4"],
                   "<b>6 + 4</b> = 10. The others make 11, 11 and 9."))
    for a, b in [(38, 5), (27, 6), (36, 7)]:
        need = 10 - a % 10
        e = "Make the next ten. %d + %d = %d. Then add the rest: %d + %d = <b>%d</b>." % (
            a, need, a + need, a + need, b - need, a + b)
        its.append(mcq("Make a ten. What is %d + %d?" % (a, b), a + b, cands_add(a, b), e))
    its.append(mcq("Make a ten. What is 28 + 14?", 42, [32, 41, 312],
                   "28 needs 2 to make 30. 14 is 2 + 12. 30 + 12 = <b>42</b>."))
    assert 28 + 14 == 42
    its.append(mcq("39 is close to 40. 40 + 25 = 65. Now take away 1. What is 39 + 25?", 64, [65, 66, 54],
                   "You added 1 too many when you used 40. Take it away: 65 − 1 = <b>64</b>. "
                   "(65 forgets to take away 1. 66 adds 1 instead.)"))
    assert 39 + 25 == 64
    for a, b in [(19, 23), (29, 18)]:
        up = a + 1
        its.append(mcq("Use a friendly number. What is %d + %d?" % (a, b), a + b,
                       [up + b, up + b + 1, a + b - 10],
                       "%d is 1 less than %d. %d + %d = %d. Take away 1: <b>%d</b>." % (a, up, up, b, up + b, a + b)))
    its.append(mcq("28 is 2 less than 30. What is 28 + 16?", 44, [46, 34, 42],
                   "30 + 16 = 46. You added 2 too many, so take away 2: 46 − 2 = <b>44</b>. "
                   "(46 forgets to take away 2.)"))
    assert 28 + 16 == 44
    its.append(mcq("Which is the same as 26 + 9?", "26 + 10 − 1", ["26 + 10 + 1", "26 + 9 − 1", "20 + 9 + 1"],
                   "9 is 1 less than 10. Add 10, then take away 1: <b>26 + 10 − 1</b> = 35."))
    assert 26 + 10 - 1 == 26 + 9
    its.append(mcq("Add 10, then take away 1. What is 32 + 9?", 41, [42, 40, 31],
                   "32 + 10 = 42. You added 1 too many, so take away 1: 42 − 1 = <b>41</b>. "
                   "(42 forgets to take away 1.)"))
    assert 32 + 9 == 41
    its.append(mcq("Which is the same as 34 + 19?", "34 + 20 − 1", ["34 + 20 + 1", "34 + 10 − 1", "30 + 19 + 1"],
                   "19 is 1 less than 20. Add 20, then take away 1: <b>34 + 20 − 1</b> = 53."))
    assert 34 + 20 - 1 == 34 + 19 == 53
    its.append(mcq("Take away 10, then add 1. What is 43 − 9?", 34, [33, 46, 32],
                   "43 − 10 = 33. You took away 1 too many, so add 1: 33 + 1 = <b>34</b>. "
                   "(46 takes 3 from 9 instead of 9 from 3.)"))
    assert 43 - 9 == 34 and small_from_big(43, 9) == 46
    its.append(mcq("Take away 20, then add 1. What is 50 − 19?", 31, [30, 29, 49],
                   "50 − 20 = 30. You took away 1 too many, so add 1: 30 + 1 = <b>31</b>. "
                   "(29 takes away 1 more instead of adding it back.)"))
    assert 50 - 19 == 31 and small_from_big(50, 19) == 49
    its.append(mcq("Use a double. 24 + 24 = 48. What is 24 + 25?", 49, [48, 50, 47],
                   "25 is 1 more than 24. So 24 + 25 is 1 more than 48: <b>49</b>."))
    its.append(mcq("Use a double. 15 + 15 = 30. What is 15 + 16?", 31, [30, 32, 29],
                   "16 is 1 more than 15. So 15 + 16 is 1 more than 30: <b>31</b>."))
    assert 24 + 25 == 49 and 15 + 16 == 31
    assert len(its) == 20, len(its)
    return {"title": "Mental math: make a ten and compensate", "items": its}


# ============================================================ set 4: estimate and check
def near_ten(n):
    assert n % 10 != 5
    return int(round(n / 10.0)) * 10


def set_estimate():
    its = []
    for n, w in [(38, [30, 50, 39]), (54, [60, 40, 55])]:
        t = near_ten(n)
        its.append(mcq(fig(tens_line_svg(n)) + "Which ten is %d closest to?" % n, t, w,
                       "%d is between %d and %d. It is closer to <b>%d</b>." % (n, n // 10 * 10, n // 10 * 10 + 10, t)))
    for n in (71, 29, 86, 62):
        t = near_ten(n)
        other = n // 10 * 10 if t != n // 10 * 10 else n // 10 * 10 + 10
        its.append(mcq("Which ten is %d closest to?" % n, t, [other, n + 1 if n % 10 != 9 else n - 1, t + 10 if t + 10 != other else t - 10],
                       "%d is between %d and %d. It is closer to <b>%d</b>." % (n, n // 10 * 10, n // 10 * 10 + 10, t)))
    for a, op, b in [(38, "+", 21), (49, "+", 32), (22, "+", 67), (81, "−", 38), (72, "−", 19), (39, "+", 41)]:
        ra, rb = near_ten(a), near_ten(b)
        est = ra + rb if op == "+" else ra - rb
        wrong = [est - 10, est + 10, (ra - rb) if op == "+" else (ra + rb)]
        wrong = [w for w in wrong if w > 0][:3]
        if len(wrong) < 3:
            wrong.append(est + 20)
        its.append(mcq("Estimate. %d %s %d is about how much?" % (a, op, b), "about %d" % est,
                       ["about %d" % w for w in wrong],
                       "%d is close to %d. %d is close to %d. %d %s %d = <b>%d</b>." % (a, ra, b, rb, ra, op, rb, est)))
    its.append(mcq("Estimate first: 52 − 29 is about 50 − 30 = 20. What is 52 − 29?", 23, [37, 33, 13],
                   "52 has only 2 ones, so regroup: 4 tens and 12 ones. 12 − 9 = 3. 4 − 2 = 2. 52 − 29 = <b>23</b>. "
                   "23 is close to 20, so it makes sense."))
    assert 52 - 29 == 23 and small_from_big(52, 29) == 37
    its.append(mcq("Estimate first: 28 + 43 is about 30 + 40 = 70. What is 28 + 43?", 71, [61, 81, 70],
                   "Tens: 20 + 40 = 60. Ones: 8 + 3 = 11. 60 + 11 = <b>71</b>. 71 is close to 70, so it makes sense."))
    assert 28 + 43 == 71
    its.append(mcq("Estimate first. Which answer to 47 + 26 makes sense?", 73, [613, 21, 55],
                   "47 + 26 is about 50 + 30 = 80. Only <b>73</b> is close to 80. "
                   "613 writes 6 tens and 13 ones side by side. 21 subtracts. 55 adds the tens as ones."))
    assert 47 + 26 == 73 and 47 - 26 == 21 and 47 + 2 + 6 == 55
    its.append(mcq("Liam says 63 − 28 = 45. He estimates 60 − 30 = 30. What should he think?", "45 is too big",
                   ["45 is right", "45 is too small", "30 is the answer"],
                   "45 is far from 30, so <b>45 is too big</b>. Liam did 8 − 3 in the ones. "
                   "Regroup: 13 − 8 = 5 and 5 − 2 = 3. 63 − 28 = 35."))
    assert small_from_big(63, 28) == 45 and 63 - 28 == 35
    its.append(mcq("64 − 27 = 37. Which addition checks the answer?", "37 + 27", ["64 + 27", "37 + 64", "37 + 72"],
                   "Add the answer and the number you took away. You should get back to the start: "
                   "<b>37 + 27</b> = 64."))
    assert 37 + 27 == 64
    its.append(mcq("45 + 38 = 83. Which subtraction checks the answer?", "83 − 38", ["83 + 38", "45 − 38", "83 − 83"],
                   "Take one part away from the total. You should get the other part: <b>83 − 38</b> = 45."))
    assert 83 - 38 == 45
    its.append(mcq("Priya says 52 − 17 = 45. She checks: 45 + 17 = 62. Is she right?", "No, 62 is not 52",
                   ["Yes, she is right", "No, 45 + 17 is 52", "Yes, 62 is close"],
                   "The check must give back 52. It gives 62, so <b>she is not right</b>. 52 − 17 = 35."))
    assert 45 + 17 == 62 and 52 - 17 == 35
    its.append(mcq("Which addition checks 90 − 34 = 56?", "56 + 34 = 90", ["56 + 90 = 34", "90 + 34 = 56", "56 − 34 = 90"],
                   "Add the answer and the number you took away: <b>56 + 34 = 90</b>. You get back to 90."))
    assert 56 + 34 == 90
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
    add_story("Liam has 34 hockey cards. He gets 25 more. How many hockey cards does he have now?",
              34, 25, "cards", whole_lead)
    add_story("At recess, 27 students play soccer and 18 students play tag. How many students play?",
              27, 18, "students", whole_lead)
    sub_story("The book fair has 63 books. The students buy 28 books. How many books are left?",
              63, 28, "books", part_lead)
    sub_story("Owen has 71 hockey cards. He gives 27 cards to his brother. How many cards does he have left?",
              71, 27, "cards", part_lead)
    its.append(mcq(fig(bar_svg(28, 35, "p2")) + "Which number sentence finds the missing part?", "63 − 28 = ?",
                   ["63 + 28 = ?", "28 − 63 = ?", "? − 28 = 35"],
                   "The whole is 63. One part is 28. Take the part away from the whole: <b>63 − 28 = ?</b>. "
                   "The missing part is 35."))
    assert 28 + 35 == 63
    add_story("In the Terry Fox Run, 38 Grade 2 students and 45 Grade 3 students ran. How many students ran?",
              38, 45, "students", whole_lead)
    sub_story("There are 54 Canada geese on a pond. 18 geese fly away. How many geese are still on the pond?",
              54, 18, "geese", part_lead)
    sub_story("Maya has $20 at the book fair. She buys a book for $13. How much money does she have left?",
              20, 13, "", part_lead, money=True)
    sub_story("Zoe read 52 pages. Ethan read 37 pages. How many more pages did Zoe read?",
              52, 37, "pages", "How many more means find the difference, so subtract. ", pic=False)
    its.append(mcq(fig(bar_svg(17, 14, "p1")) + "Some children were skating at the rink. 14 more children came. "
                   "Now there are 31. How many children were skating at first?", "17 children",
                   ["45 children", "23 children", "27 children"],
                   "The whole is 31. One part is 14. Subtract. 31 has only 1 one, so regroup: 2 tens and 11 ones. "
                   "11 − 4 = 7. 2 − 1 = 1. 31 − 14 = <b>17</b>. Check: 17 + 14 = 31."))
    assert 31 - 14 == 17 and small_from_big(31, 14) == 23 and 31 + 14 == 45
    its.append(mcq("There are 45 children at the rink. 18 children go home. Then 26 more children come. "
                   "How many children are at the rink now?", "53 children",
                   ["27 children", "89 children", "63 children"],
                   "Step 1: 45 − 18. Regroup: 15 − 8 = 7 and 3 − 1 = 2, so 27. Step 2: 27 + 26. "
                   "Tens: 20 + 20 = 40. Ones: 7 + 6 = 13. 40 + 13 = <b>53</b>. (27 forgets step 2.)"))
    assert 45 - 18 + 26 == 53 and 45 + 18 + 26 == 89
    add_story("The lost and found box has 36 mitts. Students find 29 more mitts. How many mitts are in the box now?",
              36, 29, "mitts", "Find the total, so add. ", pic=False)
    sub_story("The class wants to sell 80 tickets for the book fair. They have sold 57 tickets. How many more do they need to sell?",
              80, 57, "tickets", part_lead)
    add_story("For a recess snack, the class has 24 apples and 36 granola bars. How many snacks is that in all?",
              24, 36, "snacks", "In all means add. ", pic=False)
    its.append(mcq("Mateo has 48 hockey cards. Kai has 23 more cards than Mateo. How many cards does Kai have?",
                   "71 cards", ["25 cards", "61 cards", "81 cards"],
                   "Kai has more, so add: 48 + 23. Tens: 40 + 20 = 60. Ones: 8 + 3 = 11. 60 + 11 = <b>71</b>. "
                   "(25 subtracts. 61 forgets to regroup.)"))
    assert 48 + 23 == 71 and 48 - 23 == 25
    sub_story("A sugar bush has 65 sap buckets. 37 buckets are full. How many buckets are not full?",
              65, 37, "buckets", part_lead, pic=False)
    add_story("Two Grade 2 classes collect cans for the food drive. One class has 63 cans. The other has 37 cans. "
              "How many cans do they have in all?", 63, 37, "cans", whole_lead)
    its.append(mcq("Ava has 72 stickers. She gives away 35. Which number sentence finds how many are left?",
                   "72 − 35 = ?", ["72 + 35 = ?", "35 − 72 = ?", "? − 72 = 35"],
                   "She gives some away, so take away. Start with 72 and take away 35: <b>72 − 35 = ?</b>. "
                   "The answer is 37."))
    assert 72 - 35 == 37
    sub_story("A school bus has 72 seats. 46 students are sitting down. How many seats are empty?",
              72, 46, "seats", part_lead, pic=False)
    add_story("Leah read 34 pages on Saturday and 47 pages on Sunday. How many pages did she read?",
              34, 47, "pages", "Put the two days together, so add. ", pic=False)
    assert len(its) == 20, len(its)
    return {"title": "Word problems: recess, the book fair and hockey cards", "items": its}


# ============================================================ lesson
def body_html():
    assert 38 + 25 == 63 and 52 - 17 == 35 and 39 + 25 == 64 and 47 + 26 == 73
    return (
        "<h2>The idea: tens with tens, ones with ones</h2>"
        "<p>A 2-digit number has <b>tens</b> and <b>ones</b>. 45 is 4 tens and 5 ones. "
        "Add tens to tens. Add ones to ones.</p>"
        + table(["Number sentence", "Answer", "What changes"], [
            ["45 + 30", "75", "the tens: 4 + 3 = 7"],
            ["45 + 3", "48", "the ones: 5 + 3 = 8"],
            ["76 − 40", "36", "the tens: 7 − 4 = 3"],
        ]) +
        "<h2>Jump on an open number line</h2>"
        "<p>Start at the first number. Jump the tens. Then jump the ones. "
        "Jumping to the next ten makes it easier.</p>"
        "<figure class='sn-fig'>" + nline_svg(38, [20, 2, 3], ["38", "58", "60", "63"]) +
        "<figcaption>38 + 25: jump +20 to 58, +2 to 60, then +3 to 63.</figcaption></figure>"
        "<h2>Subtract with regrouping</h2>"
        "<p>Sometimes there are not enough ones to take away. Regroup 1 ten as 10 ones.</p>"
        "<figure class='sn-fig'>" + regroup_svg(52, 17) +
        "<figcaption>52 − 17. 52 has only 2 ones. Regroup 1 ten: 4 tens and 12 ones. "
        "Ones: 12 − 7 = 5. Tens: 4 − 1 = 3. Answer: 35.</figcaption></figure>"
        "<h2>Mental math: make a ten and compensate</h2>"
        "<p><b>Make a ten:</b> fill up to the next ten first.</p>"
        "<figure class='sn-fig'>" + tenframe_svg(8, 5) +
        "<figcaption>8 + 5: move 2 to make 10. Then 3 are left. 10 + 3 = 13.</figcaption></figure>"
        + ex("Compensate", "What is 39 + 25?", "39 is close to 40. 40 + 25 = 65. You added 1 too many, so take away 1: "
             "65 − 1 = 64.", "64") +
        "<h2>Estimate and check</h2>"
        "<p>Before you add, find the closest tens. Your answer should be close to the estimate. "
        "To check a subtraction, add back what you took away.</p>"
        + ex("Estimate", "What is 47 + 26?", "47 is close to 50. 26 is close to 30. 50 + 30 = 80. "
             "The exact answer is 73. 73 is close to 80, so it makes sense.", "73") +
        "<h2>Common mistakes</h2>"
        + table(["Mistake", "What to do instead"], [
            ["Not regrouping: 52 − 17 = 45", "2 − 7 cannot be done. Regroup 1 ten: 12 − 7 = 5. Answer: 35"],
            ["Not regrouping: 36 + 27 = 53", "6 + 7 = 13 ones is 1 ten and 3 ones. Answer: 63"],
            ["Adding tens to ones: 45 + 30 = 48", "30 is 3 tens. Add it to the tens: 75"],
            ["Writing tens and ones side by side: 47 + 26 = 613", "Add the parts: 60 + 13 = 73"],
        ])
    )


FAQ = [
    {"q": "What does Grade 2 learn about adding and subtracting in the Ontario math curriculum?",
     "a": "Grade 2 students add and subtract whole numbers that add up to no more than 100. They use objects, diagrams such as number lines and base ten blocks, and equations, and they use mental math for sums up to 50."},
    {"q": "What mental math strategies do Grade 2 students use?",
     "a": "Common strategies are making a ten (8 + 5 = 10 + 3), using doubles (24 + 25 is 1 more than 48) and compensating (39 + 25 = 40 + 25 − 1 = 64)."},
    {"q": "What is regrouping in Grade 2 subtraction?",
     "a": "Regrouping means trading 1 ten for 10 ones when there are not enough ones. For 52 − 17, 52 becomes 4 tens and 12 ones, so the answer is 35."},
    {"q": "How can my child check an addition or subtraction answer?",
     "a": "First estimate with the closest tens: 47 + 26 is about 50 + 30 = 80. Then check a subtraction by adding back: 64 − 27 = 37 because 37 + 27 = 64."},
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
            m = re.search(r"aria-label='ten frames with (\d+) green counters and (\d+) red", it["q"])
            if m:
                assert int(right) == int(m.group(1)) + int(m.group(2)), it["q"]
            m = re.search(r"aria-label='number line from \d+ to \d+ with (\d+) marked", it["q"])
            if m:
                assert int(right) == near_ten(int(m.group(1))), it["q"]
            m = re.search(r"Estimate\. (\d+) ([+−]) (\d+) is about", it["q"])
            if m:
                a, op, b = int(m.group(1)), m.group(2), int(m.group(3))
                est = near_ten(a) + near_ten(b) if op == "+" else near_ten(a) - near_ten(b)
                assert right == "about %d" % est, it["q"]


def gen():
    rnd = random.Random(42805)
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
        "country": "ca-on", "subject": "math", "grade": "grade-2", "slug": "adding-and-subtracting-to-100",
        "sort": 5, "updated": UPDATED, "pdf_url": "",
        "title": "Adding and Subtracting to 100",
        "seo_title": "Grade 2 Adding and Subtracting to 100 Worksheets: Regrouping and Mental Math (Ontario)",
        "short_title": "Adding and subtracting to 100",
        "domain": "Number",
        "standard_code": "Grade 2: B2.4",
        "standard_url": "https://www.dcp.edu.gov.on.ca/en/curriculum/elementary-mathematics",
        "standard_text": "Use objects, diagrams, and equations to represent, describe, and solve situations involving "
                         "addition and subtraction of whole numbers that add up to no more than 100",
        "meta_desc": "Free Grade 2 math worksheets on adding and subtracting to 100, matched to the Ontario curriculum: "
                     "jumps on a number line, regrouping with base ten blocks, make a ten, estimating and checking, "
                     "and word problems. 100 questions with an answer key.",
        "key_big": "Add tens to tens and ones to ones. Regroup when you need to.",
        "key_sub": "38 + 25: jump +20 to 58, then +2 to 60 and +3 to 63. For 52 − 17 there are not enough ones, "
                   "so regroup 1 ten as 10 ones: 12 − 7 = 5 and 4 − 1 = 3, so 35.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }
    return mark_large(u, "tens and ones blocks|open number line|number line from|ten frames|bar model")


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
