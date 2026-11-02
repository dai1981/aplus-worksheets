# -*- coding: utf-8 -*-
"""
AU Year 2 Maths: Adding and subtracting 2-digit numbers (Australian Curriculum v9.0, AC9M2N04)
  python3 tools/gen_au_maths_y2_add_sub.py
Add and subtract tens, the split strategy with MAB, the jump strategy on an empty number line,
subtracting with regrouping (pictures), and word problems with part-part-whole bar models.
Australian English; Australian school word "regroup". Answers are 199 or less.
Every answer and every wrong answer is computed and checked in code.
HTML attributes use single quotes (no backslashes in the JSON).
Helpers are copied from gen_uk_maths_y2_add_sub.py and gen_au_maths_y3_add_sub.py.
"""
import json, os, random, re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "au", "maths", "year-2")
UPDATED = "2026-11-02"
GREEN = "#006633"
FILL = "#cfe6d6"
RED = "#c0392b"
INK = "#2b2b2b"
FONT = "Arial, Helvetica, sans-serif"


# ------------------------------------------------------------ typical mistakes
def small_from_big(a, b):
    """52 − 17 = 45: took the smaller ones digit from the larger one."""
    ta, oa, tb, ob = a // 10, a % 10, b // 10, b % 10
    return (ta - tb) * 10 + abs(oa - ob)


def cands_add(a, b):
    """Wrong answers from real Year 2 mistakes."""
    s = a + b
    ta, oa, tb, ob = a // 10, a % 10, b // 10, b % 10
    out = []
    if b >= 10 and ob == 0:
        out.append(a + tb)                                  # added the tens as ones: 45 + 30 = 48
        if s >= 100:
            out.append(s - 100)                             # lost the hundred: 74 + 40 = 14
    if oa + ob >= 10:
        out.append(s - 10)                                  # forgot to regroup: 36 + 27 = 53
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


# ------------------------------------------------------------ explanations (short, Year 2 words)
def tens_word(k):
    return "1 ten" if k == 1 else "%d tens" % k


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
        e += "%s are left. " % cap(tens_word(ta - 1)) if ta - 1 != 1 else "1 ten is left. "
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


# ------------------------------------------------------------ pictures: MAB (tens and ones)
C = 6              # one mini; a long (one ten) is 1 × 10 minis
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
    """rows: list of (tens, ones). Longs and minis line up in columns. sign=True puts + before row 2."""
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


# ------------------------------------------------------------ pictures: split strategy
def parts(n):
    return [p for p in (n // 10 * 10, n % 10) if p]


def split_svg(a, b, op):
    """Both numbers on top, each split into tens and ones underneath."""
    S, m, gap = 50, 12, 56
    pa, pb = parts(a), parts(b)
    gwa, gwb = (len(pa) - 1) * S + 44, (len(pb) - 1) * S + 44
    cxa = m + gwa / 2.0
    cxb = m + gwa + gap + gwb / 2.0
    W = int(m + gwa + gap + gwb + m)
    H = 84
    s = [text(cxa, 24, str(a), 22), text(cxb, 24, str(b), 22),
         text((cxa + cxb) / 2.0, 24, "+" if op == "+" else "−", 22, col=GREEN)]
    for cx, ps in ((cxa, pa), (cxb, pb)):
        x0 = cx - (len(ps) - 1) * S / 2.0
        for k, p in enumerate(ps):
            px = x0 + k * S
            s.append("<line x1='%.1f' y1='32' x2='%.1f' y2='52' stroke='%s' stroke-width='2'/>" % (cx, px, GREEN))
            s.append("<rect x='%.1f' y='54' width='42' height='26' rx='5' fill='%s' stroke='%s' stroke-width='1.5'/>"
                     % (px - 21, FILL, GREEN))
            s.append(text(px, 73, str(p), 16))
    lab = "split strategy: %d split into %s; %d split into %s" % (
        a, " and ".join(map(str, pa)), b, " and ".join(map(str, pb)))
    return svg_wrap(W, H, "".join(s), lab)


# ------------------------------------------------------------ pictures: empty number line
def jw(j):
    return 80 if abs(j) >= 10 else 56


def nline_svg(start, jumps, ticks=None, jlabels=None):
    """Empty number line. Jumps go right for +, left for −. ticks: one label per point (None = no label)."""
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
    return svg_wrap(W, H, "".join(s), "empty number line starting at %d with jumps of %s" % (
        start, ", ".join(jlabels).replace("−", "minus ").replace("?", "an unknown amount")))


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
    assert a + b <= 199
    return mcq(pre + "What is %d + %d?" % (a, b), a + b, cands_add(a, b), e_add(a, b))


def q_sub(a, b, pre=""):
    assert 0 < a - b
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
        if (a, op) in seen or (a, op, 10 * k) in seen or ("k", op, k) in seen:
            continue
        seen.difference_update({x for x in seen if x[0] == "k" and x[1] == op})
        seen.update({(a, op), (a, op, 10 * k), ("k", op, k)})
        return a, 10 * k


# ============================================================ set 1: add and subtract tens
def set_tens(rnd, seen):
    its = []
    seen.update({(45, "+"), (76, "−"), (23, "+"), (82, "−"), (57, "+"), (63, "−"), (24, "+"), (36, "+"), (93, "−")})
    its.append(q_add(45, 30, fig(blocks_svg([bo(45), (3, 0)], sign=True)) + "Use the MAB. "))
    its.append(q_sub(76, 40, fig(blocks_svg([bo(76)], cross=(4, 0), label="76 with 4 tens crossed out"))
                     + "The MAB show 76. 4 tens are crossed out. "))
    it = q_add(23, 30, fig(nline_svg(23, [10, 10, 10])) + "Count on in tens. ")
    it["e"] = "Count on 3 tens from 23: 33, 43, 53. The ones stay the same. 23 + 30 = <b>53</b>."
    its.append(it)
    it = q_sub(82, 40, fig(nline_svg(82, [-10, -10, -10, -10])) + "Count back in tens. ")
    it["e"] = "Count back 4 tens from 82: 72, 62, 52, 42. The ones stay the same. 82 − 40 = <b>42</b>."
    its.append(it)
    its.append(mcq("What is 10 more than 57?", 67, [58, 77, 47],
                   "10 more means 1 more ten. 5 tens become 6 tens. The ones stay the same: <b>67</b>."))
    its.append(mcq("What is 10 less than 63?", 53, [62, 43, 73],
                   "10 less means 1 less ten. 6 tens become 5 tens. The ones stay the same: <b>53</b>."))
    its.append(mcq("You add 30 to 24. Which digit changes?", "the tens digit",
                   ["the ones digit", "both digits", "no digits"],
                   "30 is 3 tens, so only the <b>tens digit</b> changes: 24 + 30 = 54."))
    for i in range(5):
        a, b = pick_tens(rnd, seen, "+")
        pre = fig(blocks_svg([bo(a), bo(b)], sign=True)) + "Use the MAB. " if i in (0, 3) else ""
        its.append(q_add(a, b, pre))
    for i in range(4):
        a, b = pick_tens(rnd, seen, "−")
        pre = (fig(blocks_svg([bo(a)], cross=(b // 10, 0), label="%d with %d tens crossed out" % (a, b // 10)))
               + "The MAB show %d. %d tens are crossed out. " % (a, b // 10)) if i == 1 else ""
        its.append(q_sub(a, b, pre))
    # past 100
    it = q_add(74, 40, fig(nline_svg(74, [10, 10, 10, 10])) + "Count on in tens. ")
    it["e"] = ("Count on 4 tens from 74: 84, 94, 104, 114. After 94 comes 104. The ones stay the same. "
               "74 + 40 = <b>114</b>.")
    its.append(it)
    its.append(q_add(86, 50))
    its[-1]["e"] = "Tens: 8 tens + 5 tens = 13 tens = 130. The ones stay the same. 86 + 50 = <b>136</b>."
    assert 74 + 40 == 114 and 86 + 50 == 136
    its.append(mcq("Find the missing number: 36 + <b>?</b> = 76", 40, [4, 112, 30],
                   "The ones stay at 6. The tens go from 3 to 7. That is 4 tens: <b>40</b>. Check: 36 + 40 = 76."))
    assert 36 + 40 == 76 and 36 + 76 == 112
    its.append(mcq("Find the missing number: 93 − <b>?</b> = 53", 40, [4, 30, 50],
                   "The ones stay at 3. The tens go from 9 down to 5. That is 4 tens: <b>40</b>. Check: 93 − 40 = 53."))
    assert 93 - 40 == 53
    assert len(its) == 20, len(its)
    return {"title": "Add and subtract tens", "items": its}


# ============================================================ set 2: split strategy with MAB
def side_by_side(a, b):
    """36 + 27: tens 5, ones 13 written side by side as 513."""
    t, o = a // 10 + b // 10, a % 10 + b % 10
    return int("%d%d" % (t, o)) if o >= 10 and t < 10 else None


def split_add(a, b, pre):
    s = a + b
    c = [side_by_side(a, b)] + cands_add(a, b)
    e = "Split both numbers: %d = %s and %d = %s. " % (a, " + ".join(map(str, parts(a))), b, " + ".join(map(str, parts(b))))
    return mcq(pre + "What is %d + %d?" % (a, b), s, [v for v in c if v], e + e_add(a, b))


def set_split():
    its = []
    its.append(mcq("Which shows 36 split into tens and ones?", "30 + 6", ["3 + 6", "30 + 60", "3 + 60"],
                   "36 is 3 tens and 6 ones: <b>30 + 6</b>. The 3 is in the tens place, so it is worth 30."))
    its.append(mcq("Which is the same as 36 + 27?", "30 + 20 + 6 + 7",
                   ["3 + 2 + 6 + 7", "30 + 70 + 6 + 2", "30 + 6 + 2 + 7"],
                   "Split both numbers into tens and ones: 36 = 30 + 6 and 27 = 20 + 7. "
                   "So 36 + 27 = <b>30 + 20 + 6 + 7</b>."))
    for a, b, pic in [(34, 25, True), (42, 36, True), (53, 24, False)]:
        assert (a % 10) + (b % 10) < 10
        its.append(split_add(a, b, fig(split_svg(a, b, "+")) + "Use the split strategy. " if pic else
                             "Use the split strategy. "))
    its.append(mcq("Use the split strategy. 36 + 27 = 50 + <b>?</b>", 13, [3, 12, 14],
                   "Tens: 30 + 20 = 50. Ones: 6 + 7 = <b>13</b>. So 36 + 27 = 50 + 13 = 63."))
    its.append(mcq("Use the split strategy. 48 + 35 = <b>?</b> + 13", 70, [7, 80, 60],
                   "Tens: 40 + 30 = <b>70</b>. Ones: 8 + 5 = 13. 70 + 13 = 83. (7 adds the tens as if they were ones.)"))
    assert 48 + 35 == 70 + 13 and 36 + 27 == 63
    for a, b in [(28, 15), (47, 26), (39, 44), (58, 25)]:
        assert (a % 10) + (b % 10) >= 10
        it = split_add(a, b, fig(blocks_svg([bo(a), bo(b)], sign=True)) + "The MAB show two numbers. ")
        ta, tb, o = a // 10, b // 10, a % 10 + b % 10
        it["e"] = ("Count the longs: %d + %d = %d tens. Count the minis: %d + %d = %d ones. "
                   "Regroup 10 ones as 1 ten: %d tens and %d ones. %d + %d = <b>%d</b>."
                   % (ta, tb, ta + tb, a % 10, b % 10, o, ta + tb + 1, o - 10, a, b, a + b))
        its.append(it)
    for a, b, pic in [(46, 38, True), (57, 29, False), (64, 28, True), (35, 47, False)]:
        assert (a % 10) + (b % 10) >= 10
        its.append(split_add(a, b, fig(split_svg(a, b, "+")) + "Use the split strategy. " if pic else
                             "Use the split strategy. "))
    for a, b in [(68, 45), (76, 58)]:
        its.append(split_add(a, b, fig(split_svg(a, b, "+")) + "Use the split strategy. "))
    for a, b, pic in [(67, 24, True), (79, 34, False), (87, 53, True)]:
        assert a % 10 >= b % 10
        it = q_sub(a, b, fig(split_svg(a, b, "−")) + "Use the split strategy. " if pic else "Use the split strategy. ")
        its.append(it)
    assert len(its) == 20, len(its)
    return {"title": "Split strategy with MAB", "items": its}


# ============================================================ set 3: jump strategy
def jump_q(a, jumps, pre="", text_only=False):
    end = a + sum(jumps)
    b = abs(sum(jumps))
    op = "+" if jumps[0] > 0 else "−"
    c = [end - jumps[-1]] + (cands_add(a, b) if op == "+" else cands_sub(a, b))
    if text_only:
        words = ", then ".join(str(abs(j)) for j in jumps)
        q = "Start at %d. Jump %s %s. Where do you land?" % (a, "forward" if op == "+" else "back", words)
    else:
        q = fig(nline_svg(a, jumps)) + pre + "What is %d %s %d?" % (a, op, b)
    e = e_jumps(a, jumps) + " So %d %s %d = %d." % (a, op, b, end)
    return mcq(q, end, c, e)


def set_jump():
    its = []
    its.append(jump_q(35, [40, 2], "Jump the tens, then the ones. "))
    its.append(jump_q(26, [50, 3], "Jump the tens, then the ones. "))
    its.append(jump_q(41, [30, 7], text_only=True))
    its.append(jump_q(68, [-20, -5], "Jump back the tens, then the ones. "))
    its.append(jump_q(79, [-40, -6], "Jump back the tens, then the ones. "))
    its.append(jump_q(38, [20, 2, 3], "Jump to the next ten. "))
    its.append(jump_q(47, [30, 3, 3], "Jump to the next ten. "))
    its.append(jump_q(56, [20, 4, 4], "Jump to the next ten. "))
    its.append(jump_q(63, [-20, -3, -5], "Jump back to the ten. "))
    its.append(jump_q(82, [-40, -2, -5], "Jump back to the ten. "))
    its.append(jump_q(71, [-30, -1, -5], "Jump back to the ten. "))
    its.append(mcq(fig(nline_svg(45, [30, 4], ["45", "75", "79"], ["?", "+4"])) + "What is the missing jump?",
                   "+30", ["+3", "+34", "+40"],
                   "From 45 to 75 the tens digit goes from 4 to 7. That is 3 tens, so the jump is <b>+30</b>. "
                   "Check: 45 + 34 = 79."))
    assert 45 + 34 == 79
    its.append(mcq(fig(nline_svg(29, [50, 6], ["29", "79", "85"])) + "Which number sentence does the number line show?",
                   "29 + 56 = 85", ["29 + 65 = 85", "85 + 56 = 29", "56 − 29 = 85"],
                   "It starts at 29 and jumps +50 and +6. 50 + 6 = 56, so it shows <b>29 + 56 = 85</b>."))
    assert 29 + 56 == 85
    for a, b, js in [(52, 47, [3, 2]), (83, 77, [3, 3])]:
        d = a - b
        assert sum(js) == d and (b + js[0]) % 10 == 0
        e = ("The numbers are close, so count on from %d. %d + %d = %d. %d + %d = %d. "
             "The jumps are %d + %d = <b>%d</b>. So %d − %d = %d." % (b, b, js[0], b + js[0], b + js[0], js[1], a,
                                                                      js[0], js[1], d, a, b, d))
        its.append(mcq(fig(nline_svg(b, js, [str(b), str(b + js[0]), str(a)])) +
                       "Count on to find the difference. What is %d − %d?" % (a, b), d,
                       [small_from_big(a, b), js[0], js[1], d + 10], e))
    its.append(mcq("19 is 1 less than 20. Add 20, then take away 1. What is 46 + 19?", 65,
                   [66, 67, 55], "Add 20, then take away 1. 46 + 20 = 66. 66 − 1 = <b>65</b>. (66 forgets to take away 1.)"))
    its.append(mcq("29 is 1 less than 30. Take away 30, then add 1. What is 73 − 29?", 44,
                   [43, small_from_big(73, 29), 54],
                   "Take away 30, then add 1. 73 − 30 = 43. 43 + 1 = <b>44</b>. "
                   "You took away 1 too many, so add 1 back."))
    assert 46 + 19 == 65 and 73 - 29 == 44 and small_from_big(73, 29) == 56
    its.append(jump_q(87, [40, 3, 3], "Jump to the next ten. "))
    its.append(jump_q(64, [50, 6, 2], text_only=True))
    its.append(jump_q(94, [-50, -4, -3], text_only=True))
    assert len(its) == 20, len(its)
    return {"title": "Jump strategy on an empty number line", "items": its}


# ============================================================ set 4: subtract with regrouping
def set_regroup():
    its = []
    its.append(mcq(fig(blocks_svg([bo(52)])) + "The MAB show 52. You need to take away 17. "
                   "There are not enough ones. What do you do?",
                   "Regroup 1 ten", ["Do 7 − 2", "Write 0 ones", "Take away 2 tens"],
                   "52 has only 2 ones, and you need to take away 7. <b>Regroup 1 ten</b> as 10 ones. "
                   "Then there are 12 ones. Doing 7 − 2 instead is a common mistake."))
    its.append(mcq("You regroup 1 ten in 52. What does 52 look like now?", "4 tens and 12 ones",
                   ["5 tens and 12 ones", "4 tens and 2 ones", "3 tens and 12 ones"],
                   "Take 1 ten from the 5 tens: 4 tens are left. The 10 ones join the 2 ones: 12 ones. "
                   "So 52 = <b>4 tens and 12 ones</b>. Check: 40 + 12 = 52."))
    for a, b in [(43, 18), (61, 25), (74, 36), (35, 19), (82, 46), (53, 8), (90, 34)]:
        ta, oa = bo(a)
        its.append(q_sub(a, b, fig(regroup_svg(a, b)) +
                         "%d − %d. 1 ten was regrouped as 10 ones: %s and %d ones. %d is crossed out. "
                         % (a, b, tens_word(ta - 1), oa + 10, b)))
    its.append(mcq("Mia says 52 − 17 = 45. What mistake did she make?", "She did 7 − 2",
                   ["She added the tens", "She added the ones", "She did 12 − 7"],
                   "In the ones, Mia took 2 from 7. But it must be 2 − 7, and you cannot take 7 from 2. "
                   "Regroup: 12 − 7 = 5 and 4 − 1 = 3. So 52 − 17 = <b>35</b>. Her mistake: <b>she did 7 − 2</b>."))
    assert small_from_big(52, 17) == 45 and 52 - 17 == 35
    for a, b, pic in [(64, 27, True), (91, 45, False), (70, 34, True), (56, 29, False), (83, 57, True),
                      (45, 26, False), (92, 68, False)]:
        assert b % 10 > a % 10
        its.append(q_sub(a, b, (fig(blocks_svg([bo(a)])) + "The MAB show %d. " % a) if pic else ""))
    its.append(mcq("64 − 27 = 37. Which addition checks the answer?", "37 + 27", ["64 + 27", "37 + 64", "37 + 72"],
                   "Add the answer and the number you took away. You should get back to the start: "
                   "<b>37 + 27</b> = 64."))
    assert 37 + 27 == 64 and 37 + 72 != 64
    its.append(mcq("Find the missing number: 52 − <b>?</b> = 35", 17, [27, 87, 23],
                   "Count on from 35 to 52. 35 + 5 = 40. 40 + 12 = 52. 5 + 12 = <b>17</b>. Check: 52 − 17 = 35."))
    assert 52 - 17 == 35 and 52 + 35 == 87 and small_from_big(52, 35) == 23
    its.append(mcq("Which subtraction needs regrouping?", "63 − 28", ["68 − 23", "75 − 41", "49 − 16"],
                   "In <b>63 − 28</b>, there are only 3 ones and you need to take away 8. So regroup 1 ten. "
                   "In the others, the top ones digit is big enough."))
    assert len(its) == 20, len(its)
    return {"title": "Subtract with regrouping", "items": its}


# ============================================================ set 5: word problems with bar models
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
    add_story("A bucket has 34 shells. Ruby finds 25 more shells. How many shells are in the bucket now?",
              34, 25, "shells", whole_lead)
    add_story("The canteen sold 46 icy poles at recess and 38 at lunch. How many icy poles did it sell altogether?",
              46, 38, "icy poles", whole_lead)
    sub_story("There are 57 students on the bus. 23 students get off at the pool. How many students are still on the bus?",
              57, 23, "students", part_lead)
    sub_story("Isla has 62 footy cards. She gives 27 cards to her brother. How many cards does she have left?",
              62, 27, "cards", part_lead)
    its.append(mcq(fig(bar_svg(28, 35, "p2")) + "Which number sentence finds the missing part?", "63 − 28 = ?",
                   ["63 + 28 = ?", "28 − 63 = ?", "? − 28 = 35"],
                   "The whole is 63. One part is 28. Take the part away from the whole: <b>63 − 28 = ?</b>. "
                   "The missing part is 35."))
    its.append(mcq(fig(bar_svg(45, 36, "whole")) + "Which number sentence finds the whole?", "45 + 36 = ?",
                   ["45 − 36 = ?", "36 − 45 = ?", "45 + ? = 36"],
                   "The parts are 45 and 36. Put the parts together to find the whole: <b>45 + 36 = ?</b>. "
                   "The whole is 81."))
    assert 28 + 35 == 63 and 45 + 36 == 81
    sub_story("The sausage sizzle cooked 75 sausages. 48 sausages were sold. How many sausages are left?",
              75, 48, "sausages", part_lead)
    add_story("Our cricket team scored 68 runs before lunch and 57 runs after lunch. How many runs did we score?",
              68, 57, "runs", whole_lead)
    sub_story("Year 2 needs 90 cans for a recycling project. They have 54 cans. How many more cans do they need?",
              90, 54, "cans", part_lead)
    sub_story("Leo has $45. He buys a book for $28. How much money does he have left?",
              45, 28, "", part_lead, money=True)
    sub_story("83 people watch a race at the swimming carnival. 47 of them are students. The rest are parents. "
              "How many parents are there?", 83, 47, "parents", part_lead)
    sub_story("Mia scored 52 points in a game. Jack scored 37 points. How many more points did Mia score?",
              52, 37, "points", "How many more means find the difference, so subtract. ")
    # start unknown
    its.append(mcq(fig(bar_svg(17, 14, "p1")) + "Some students were in the library. 14 more students came in. "
                   "Now there are 31. How many students were there at first?", "17 students",
                   ["45 students", "23 students", "27 students"],
                   "The whole is 31. One part is 14. Subtract: 31 has only 1 one, so regroup 1 ten: 2 tens and 11 ones. "
                   "11 − 4 = 7. 2 − 1 = 1. 31 − 14 = <b>17</b>. Check: 17 + 14 = 31."))
    assert 31 - 14 == 17 and small_from_big(31, 14) == 23 and 31 + 14 == 45
    add_story("The class garden has 26 carrot plants and 39 lettuce plants. How many plants are there altogether?",
              26, 39, "plants", "Altogether means add. ", pic=False)
    add_story("A netball team scored 18 goals in the first half and 23 goals in the second half. "
              "How many goals did it score?", 18, 23, "goals", "Put the two halves together, so add. ", pic=False)
    its.append(mcq(fig(bar_svg(25, 38, "whole")) + "Grace had some stickers. She gave away 25 stickers. "
                   "Now she has 38. How many stickers did she have at the start?", "63 stickers",
                   ["13 stickers", "53 stickers", "73 stickers"],
                   "The stickers she gave away and the stickers she has now make the whole. Add: 25 + 38. "
                   "Tens: 20 + 30 = 50. Ones: 5 + 8 = 13. 50 + 13 = <b>63</b>. Check: 63 − 25 = 38."))
    assert 25 + 38 == 63 and 38 - 25 == 13
    its.append(mcq("There are 45 children at the beach. 18 children go home. Then 26 more children come. "
                   "How many children are at the beach now?", "53 children",
                   ["27 children", "89 children", "63 children"],
                   "Step 1: 45 − 18. Regroup: 15 − 8 = 7 and 3 − 1 = 2, so 27. Step 2: 27 + 26. "
                   "Tens: 20 + 20 = 40. Ones: 7 + 6 = 13. 40 + 13 = <b>53</b>. (27 forgets step 2.)"))
    assert 45 - 18 + 26 == 53 and 45 + 18 + 26 == 89
    its.append(mcq("Aarav has 72 marbles. He loses 35 marbles. Which number sentence finds how many are left?",
                   "72 − 35 = ?", ["72 + 35 = ?", "35 − 72 = ?", "? − 72 = 35"],
                   "He loses some, so take away. Start with 72 and take away 35: <b>72 − 35 = ?</b>. "
                   "The answer is 37."))
    assert 72 - 35 == 37
    sub_story("A bus has 60 seats. 43 students are sitting down. How many seats are empty?",
              60, 43, "seats", part_lead, pic=False)
    add_story("Charlotte read 34 pages on Saturday and 47 pages on Sunday. How many pages did she read?",
              34, 47, "pages", "Put the two days together, so add. ", pic=False)
    assert len(its) == 20, len(its)
    return {"title": "Word problems with bar models", "items": its}


# ============================================================ lesson
def body_html():
    assert 36 + 27 == 63 and 52 - 17 == 35 and 45 + 30 == 75 and 63 - 28 == 35
    return (
        "<h2>The idea: tens with tens, ones with ones</h2>"
        "<p>A 2-digit number is made of <b>tens</b> and <b>ones</b>. 45 is 4 tens and 5 ones. "
        "Add tens to tens. Add ones to ones.</p>"
        + table(["Number sentence", "Answer", "What changes"], [
            ["45 + 30", "75", "the tens: 4 + 3 = 7"],
            ["45 + 3", "48", "the ones: 5 + 3 = 8"],
            ["76 − 40", "36", "the tens: 7 − 4 = 3"],
        ]) +
        "<h2>The split strategy</h2>"
        "<p>Split both numbers into tens and ones. Add the tens. Add the ones. Then put them together.</p>"
        "<figure class='sn-fig'>" + split_svg(36, 27, "+") +
        "<figcaption>36 + 27. Tens: 30 + 20 = 50. Ones: 6 + 7 = 13. 50 + 13 = 63.</figcaption></figure>"
        "<p>If there are 10 or more ones, <b>regroup</b>: 10 ones make 1 ten.</p>"
        "<figure class='sn-fig'>" + blocks_svg([(3, 6), (2, 7)], sign=True) +
        "<figcaption>36 + 27 with MAB. 5 longs and 13 minis. Regroup 10 minis as 1 long: "
        "6 tens and 3 ones. Answer: 63.</figcaption></figure>"
        "<h2>The jump strategy</h2>"
        "<p>Start at the first number on an empty number line. Jump the tens, then the ones. "
        "Jumping to the next ten makes it easier.</p>"
        "<figure class='sn-fig'>" + nline_svg(38, [20, 2, 3], ["38", "58", "60", "63"]) +
        "<figcaption>38 + 25: jump +20 to 58, +2 to 60, then +3 to 63.</figcaption></figure>"
        + ex("Jump back", "What is 63 − 28?", "63 − 20 = 43. 43 − 3 = 40. 40 − 5 = 35.", "35") +
        "<h2>Subtracting with regrouping</h2>"
        "<p>Sometimes there are not enough ones to take away. Regroup 1 ten as 10 ones.</p>"
        "<figure class='sn-fig'>" + regroup_svg(52, 17) +
        "<figcaption>52 − 17. 52 has only 2 ones. Regroup 1 ten: 4 tens and 12 ones. "
        "Ones: 12 − 7 = 5. Tens: 4 − 1 = 3. Answer: 35.</figcaption></figure>"
        "<h2>Part-part-whole bar models</h2>"
        "<p>Two parts make the whole. To find the whole, add. To find a missing part, subtract.</p>"
        "<figure class='sn-fig'>" + bar_svg(28, 35, "p2") +
        "<figcaption>The whole is 63. One part is 28. The missing part is 63 − 28 = 35.</figcaption></figure>"
        "<h2>Common mistakes</h2>"
        + table(["Mistake", "What to do instead"], [
            ["Taking the smaller digit from the larger one: 52 − 17 = 45", "2 − 7 cannot be done. Regroup 1 ten: 12 − 7 = 5. Answer: 35"],
            ["Adding tens as ones: 45 + 30 = 48", "30 is 3 tens. Add it to the tens: 75"],
            ["Forgetting to regroup: 36 + 27 = 53", "6 + 7 = 13 ones is 1 ten and 3 ones. Answer: 63"],
            ["Writing 50 and 13 side by side: 36 + 27 = 513", "Add the parts: 50 + 13 = 63"],
        ])
    )


FAQ = [
    {"q": "What does Year 2 learn about adding and subtracting in the Australian Curriculum?",
     "a": "Year 2 students add and subtract one- and two-digit numbers. They write number sentences, use part-part-whole thinking and choose strategies such as the split strategy and the jump strategy."},
    {"q": "What is the split strategy?",
     "a": "The split strategy splits numbers into tens and ones. For 36 + 27, add 30 + 20 = 50 and 6 + 7 = 13, then 50 + 13 = 63."},
    {"q": "What is the jump strategy?",
     "a": "The jump strategy uses an empty number line. Start at one number and jump the tens, then the ones: for 38 + 25, jump +20 to 58, +2 to 60 and +3 to 63."},
    {"q": "What is regrouping in Year 2 subtraction?",
     "a": "Regrouping (also called trading) means swapping 1 ten for 10 ones when there are not enough ones. For 52 − 17, 52 becomes 4 tens and 12 ones, so the answer is 35."},
]


def verify(sets):
    for s in sets:
        for it in s["items"]:
            right = it["c"][it["a"]]
            m = re.search(r"What is (\d+) ([+−]) (\d+)\?$", it["q"])
            if m:
                a, op, b = int(m.group(1)), m.group(2), int(m.group(3))
                v = a + b if op == "+" else a - b
                assert int(right) == v and 0 < v <= 199, it["q"]
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
            for c in it["c"]:
                for x in re.findall(r"\d+", c):
                    assert int(x) < 1000, c


def gen():
    rnd = random.Random(2803)
    seen = set()
    sets = [set_tens(rnd, seen), set_split(), set_jump(), set_regroup(), set_words()]
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
        "country": "au", "subject": "maths", "grade": "year-2", "slug": "adding-and-subtracting-2-digit-numbers",
        "sort": 3, "updated": UPDATED, "pdf_url": "",
        "title": "Adding and Subtracting 2-Digit Numbers",
        "seo_title": "Year 2 Adding and Subtracting 2-Digit Numbers Worksheets: Split Strategy, Jump Strategy and Bar Models",
        "short_title": "Adding and subtracting 2-digit numbers",
        "domain": "Number",
        "standard_code": "AC9M2N04",
        "standard_url": "https://v9.australiancurriculum.edu.au/f-10-curriculum/learning-areas/mathematics",
        "standard_text": "Add and subtract one- and two-digit numbers, representing problems using number sentences, "
                         "and solve using part-part-whole reasoning and a variety of calculation strategies",
        "meta_desc": "Free Year 2 maths worksheets on adding and subtracting 2-digit numbers, matched to the Australian "
                     "Curriculum (AC9M2N04): add and subtract tens, the split strategy with MAB, the jump strategy, "
                     "regrouping and part-part-whole bar models. 100 questions with an answer key.",
        "key_big": "Add tens to tens and ones to ones. Regroup when you need to.",
        "key_sub": "36 + 27: 30 + 20 = 50 and 6 + 7 = 13, so 63. For 52 − 17 there are not enough ones, "
                   "so regroup 1 ten as 10 ones: 12 − 7 = 5 and 4 − 1 = 3, so 35.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }
    return mark_large(u, "tens and ones blocks|empty number line|split strategy|bar model")


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
