# -*- coding: utf-8 -*-
"""
SG Primary 1 Maths: Addition and subtraction within 100 (MOE 2021 Primary Mathematics Syllabus, Standard)
  python3 tools/gen_sg_maths_p1_add_sub_100.py
Mental calculation: a 2-digit number and ones (no renaming), a 2-digit number and tens;
column addition with renaming, column subtraction with renaming, and one-step word problems
with number bonds in Singapore settings. Singapore English ("renaming", "pupils").
Very short sentences for 6- and 7-year-olds and a picture in almost every question.
Every answer and every wrong answer is computed and checked in code. All answers are 100 or less.
HTML attributes use single quotes (no backslashes in the JSON).
Helpers are adapted from gen_cabc_math_g2_add_sub.py and gen_sg_maths_p3_add_sub.py.
"""
import json, os, random, re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "sg", "maths", "primary-1")
UPDATED = "2026-11-03"
GREEN = "#006633"
FILL = "#cfe6d6"
RED = "#c0392b"
INK = "#2b2b2b"
FONT = "Arial, Helvetica, sans-serif"


# ------------------------------------------------------------ typical mistakes
def side_by_side(a, b):
    """36 + 27 = 513: wrote the tens sum and the ones sum side by side."""
    return int("%d%d" % (a // 10 + b // 10, a % 10 + b % 10))


def small_from_big(a, b):
    """52 − 17 = 45: took the smaller ones digit from the larger one (no renaming)."""
    return (a // 10 - b // 10) * 10 + abs(a % 10 - b % 10)


def forgot_reduce(a, b):
    """52 − 17 = 45: renamed the ones but did not take 1 from the tens."""
    return (a // 10 - b // 10) * 10 + (a % 10 + 10 - b % 10)


def cands_add(a, b):
    """Wrong answers from real Primary 1 mistakes."""
    s = a + b
    ta, oa, tb, ob = a // 10, a % 10, b // 10, b % 10
    out = []
    if b < 10:
        out.append(a + 10 * b)                       # added the ones to the tens: 43 + 5 = 93
        if oa + b >= 10:
            out += [s - 10, side_by_side(a, b)]      # did not rename: 37 + 8 = 35 or 315
        out.append(s - 1)                            # counted on from the start number
    elif ob == 0:
        out += [a + tb, s - 10, s + 10]              # added the tens to the ones: 46 + 30 = 49
    else:
        if oa + ob >= 10:
            out += [s - 10, side_by_side(a, b)]      # forgot the renamed ten / 513
        out.append(a + tb + ob)                      # added the tens as ones
    out += [s + 10, s - 10, s + 1, s - 1]
    return [v for v in out if 0 < v != s and v < 1000]


def cands_sub(a, b):
    r = a - b
    ta, oa, tb, ob = a // 10, a % 10, b // 10, b % 10
    out = []
    if b < 10:
        if ob > oa:
            out += [small_from_big(a, b), forgot_reduce(a, b)]
        else:
            if a - 10 * b > 0:
                out.append(a - 10 * b)               # took the ones from the tens: 47 − 3 = 17
            out.append(r + 1)                        # counted back from the start number
        out.append(a + b)
    elif ob == 0:
        out += [a - tb, r + 10, r - 10, a + b]       # took the tens from the ones: 76 − 40 = 72
    else:
        if ob > oa:
            out += [small_from_big(a, b), forgot_reduce(a, b)]
        out += [a + b, r - 10, r + 10]
    out += [r + 10, r - 1, r + 1]
    return [v for v in out if 0 < v != r and v != a and v < 1000]


# ------------------------------------------------------------ explanations (short, Primary 1 words)
def tens_word(k):
    return "1 ten" if k == 1 else "%d tens" % k


def ones_word(k):
    return "1 one" if k == 1 else "%d ones" % k


def e_add(a, b):
    s = a + b
    ta, oa, tb, ob = a // 10, a % 10, b // 10, b % 10
    if b < 10:
        if oa + b < 10:
            return "Add the ones: %d + %d = %d. The tens stay the same. %d + %d = <b>%d</b>." % (oa, b, oa + b, a, b, s)
        return ("Ones: %d + %d = %d. Write %d. Rename 10 ones as 1 ten. Tens: %d + 1 = %d. %d + %d = <b>%d</b>."
                % (oa, b, oa + b, oa + b - 10, ta, ta + 1, a, b, s))
    if ob == 0:
        return ("%d is %s. Add the tens: %s + %s = %s. The ones stay the same. %d + %d = <b>%d</b>."
                % (b, tens_word(tb), tens_word(ta), tens_word(tb), tens_word(ta + tb), a, b, s))
    if oa + ob < 10:
        return ("Ones: %d + %d = %d. Tens: %d + %d = %d. %d + %d = <b>%d</b>."
                % (oa, ob, oa + ob, ta, tb, ta + tb, a, b, s))
    return ("Ones: %d + %d = %d. Write %d. Rename 10 ones as 1 ten. Tens: %d + %d + 1 = %d. %d + %d = <b>%d</b>."
            % (oa, ob, oa + ob, oa + ob - 10, ta, tb, ta + tb + 1, a, b, s))


def e_sub(a, b):
    r = a - b
    ta, oa, tb, ob = a // 10, a % 10, b // 10, b % 10
    if b < 10 and ob <= oa:
        return "Take away the ones: %d − %d = %d. The tens stay the same. %d − %d = <b>%d</b>." % (oa, b, oa - b, a, b, r)
    if b >= 10 and ob == 0:
        return ("%d is %s. Take away the tens: %s − %s = %s. The ones stay the same. %d − %d = <b>%d</b>."
                % (b, tens_word(tb), tens_word(ta), tens_word(tb), tens_word(ta - tb), a, b, r))
    if ob <= oa:
        return ("Ones: %d − %d = %d. Tens: %d − %d = %d. %d − %d = <b>%d</b>."
                % (oa, ob, oa - ob, ta, tb, ta - tb, a, b, r))
    e = ("You cannot take %s from %s. Rename 1 ten as 10 ones. Ones: %d − %d = %d. "
         % (ones_word(ob), ones_word(oa), oa + 10, ob, oa + 10 - ob))
    if b < 10:
        e += "Tens: %d − 1 = %d. " % (ta, ta - 1)
    else:
        e += "Tens: %d − 1 − %d = %d. " % (ta, tb, ta - 1 - tb)
    return e + "%d − %d = <b>%d</b>." % (a, b, r)


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


def digits(n, k=None):
    k = k or len(str(n))
    return [(n // 10 ** i) % 10 for i in range(k)]          # ones first


# ------------------------------------------------------------ pictures: tens and ones blocks
C = 6              # one unit cube; a ten is a rod of 10 cubes
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
        if cross != (0, 0):
            label += " with %d crossed out" % (10 * cross[0] + cross[1])
    return svg_wrap(W, H, "".join(s), "tens and ones blocks showing " + label)


def bo(n):
    return (n // 10, n % 10)


# ------------------------------------------------------------ pictures: number line
def jw(j):
    return 80 if abs(j) >= 10 else 52


def nline_svg(start, jumps, ticks=None):
    """Open number line. Jumps go right for +, left for −. The last point is "?"."""
    if ticks is None:
        v, ticks = start, [str(start)]
        for j in jumps[:-1]:
            v += j
            ticks.append(str(v))
        ticks.append("?")
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
            s.append(text(x, ly + 24, t, 16, col=RED if t == "?" else INK))
    return svg_wrap(W, H, "".join(s), "number line starting at %d with jumps of %s" % (
        start, ", ".join(jlabels).replace("−", "minus ")))


# ------------------------------------------------------------ pictures: column layout
def rename_digits(a, b):
    """Top digits after the renaming of column subtraction (ones first)."""
    k = len(str(a))
    d, db = digits(a, k), digits(b, k)
    for i in range(k):
        if d[i] < db[i]:
            d[i + 1] -= 1
            d[i] += 10
    return d


def add_carry_cols(a, b):
    """Columns (ones = 0) that make 10 or more and send 1 to the next column."""
    k = max(len(str(a)), len(str(b)))
    da, db = digits(a, k), digits(b, k)
    c, cols = 0, []
    for i in range(k):
        c = 1 if da[i] + db[i] + c >= 10 else 0
        if c:
            cols.append(i)
    return cols


def column_svg(a, b, op, answer=False, marks=False, fs=28, shown=None):
    """a over b in columns with the sign and a line.
    answer: also write the answer.  marks: red renaming marks
    (+: the renamed 1 written small under the answer line;  −: the old digits crossed out, new digits above)."""
    cw = fs * (0.82 if marks else 0.62)
    res = a + b if op == "+" else a - b
    if shown is not None:
        answer, res = True, shown
    rows = [str(a), str(b)] + ([str(res)] if answer else [])
    longest = max(len(r) for r in rows) * cw
    pad_l = cw * 1.5 + 8
    W = int(pad_l + longest + 12)
    right = W - 12
    top = 10 + (int(fs * 0.62) if marks and op != "+" else 0)
    s = []

    def put(t, y, color):
        for k, ch in enumerate(reversed(t)):
            s.append("<text x='%.1f' y='%d' font-size='%d' font-weight='700' fill='%s' text-anchor='middle' "
                     "font-family='monospace'>%s</text>" % (right - cw * k - cw / 2, y, fs, color, ch))

    def px(i):
        return right - cw * i - cw / 2

    y1, y2 = top + fs, top + int(fs * 2.15)
    put(rows[0], y1, INK)
    put(rows[1], y2, INK)
    sign_x = right - longest - cw * 0.9
    s.append("<text x='%.1f' y='%d' font-size='%d' font-weight='700' fill='%s' text-anchor='middle'>%s</text>"
             % (sign_x, y2, fs, GREEN, "+" if op == "+" else "−"))
    ly = y2 + 13
    s.append("<line x1='%.1f' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='3'/>" % (sign_x - cw * 0.6, ly, right, ly, INK))
    H = ly + 10
    if answer:
        ay = ly + fs + 6
        put(rows[2], ay, GREEN if shown is None else RED)
        H = ay + 12
        if op == "+":
            ly2 = ay + 11
            s.append("<line x1='%.1f' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='3'/>"
                     % (sign_x - cw * 0.6, ly2, right, ly2, INK))
            H = ly2 + 8
    if marks:
        sm = int(fs * 0.55)
        if op == "+":
            assert answer
            yy = H + sm - 2
            for i in add_carry_cols(a, b):
                s.append("<text x='%.1f' y='%d' font-size='%d' font-weight='700' fill='%s' text-anchor='middle'>1</text>"
                         % (px(i + 1), yy, sm, RED))
            H = yy + 8
        else:
            nd = rename_digits(a, b)
            od = digits(a)
            for i in range(len(str(a))):
                if nd[i] != od[i]:
                    x = px(i)
                    s.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='2.5'/>"
                             % (x - fs * 0.28, y1 + fs * 0.02, x + fs * 0.28, y1 - fs * 0.72, RED))
                    s.append("<text x='%.1f' y='%d' font-size='%d' font-weight='700' fill='%s' text-anchor='middle'>%d</text>"
                             % (x, top - 4, sm if nd[i] < 10 else int(sm * 0.85), RED, nd[i]))
    label = "%d %s %d written in columns" % (a, "plus" if op == "+" else "minus", b)
    if shown is not None:
        label += " with the answer %d" % shown
    return svg_wrap(W, int(H), "".join(s), label)


# ------------------------------------------------------------ pictures: number bond (whole on top, two parts below)
def bond_svg(whole, p1, p2):
    """whole, p1, p2 are labels (str). "?" is drawn in red."""
    W, H, r = 230, 156, 30
    pts = [(115, 40, whole), (52, 116, p1), (178, 116, p2)]
    s = []
    for (x, y, _) in pts[1:]:
        dx, dy = x - 115, y - 40
        d = (dx * dx + dy * dy) ** 0.5
        s.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='2.5'/>"
                 % (115 + dx / d * r, 40 + dy / d * r, x - dx / d * r, y - dy / d * r, GREEN))
    for i, (x, y, lab) in enumerate(pts):
        s.append("<circle cx='%d' cy='%d' r='%d' fill='%s' stroke='%s' stroke-width='2.5'/>"
                 % (x, y, r, FILL if i == 0 else "#ffffff", GREEN))
        s.append(text(x, y + 7, lab, 20, col=RED if lab == "?" else INK))
    return svg_wrap(W, H, "".join(s), "number bond: whole %s, parts %s and %s" % (whole, p1, p2))


# ------------------------------------------------------------ question makers
def q_add(a, b, pre=""):
    assert a + b <= 100
    return mcq(pre + "What is %d + %d?" % (a, b), a + b, cands_add(a, b), e_add(a, b))


def q_sub(a, b, pre=""):
    assert 0 < a - b and a <= 100
    return mcq(pre + "What is %d − %d?" % (a, b), a - b, cands_sub(a, b), e_sub(a, b))


def plus_blocks(a, b):
    return fig(blocks_svg([bo(a), bo(b)], sign=True))


# ============================================================ set 1: add and take away ones (no renaming)
def set_ones():
    its = []
    for a, b, pre in [(43, 5, "Count on the ones. "), (21, 6, ""), (52, 4, "Count on the ones. "), (34, 3, ""),
                      (60, 7, ""), (75, 2, ""), (13, 6, ""), (81, 8, "")]:
        assert a % 10 + b < 10
        its.append(q_add(a, b, plus_blocks(a, b) + pre))
    for a, b in [(47, 3), (58, 6), (29, 4), (66, 5)]:
        assert a % 10 >= b
        its.append(q_sub(a, b, fig(blocks_svg([bo(a)], cross=(0, b))) + "Take away the crossed-out ones. "))
    it = q_add(62, 4, fig(nline_svg(62, [1, 1, 1, 1])) + "Count on 4. ")
    it["e"] = "Count on 4 from 62: 63, 64, 65, 66. 62 + 4 = <b>66</b>."
    its.append(it)
    it = q_sub(89, 3, fig(nline_svg(89, [-1, -1, -1])) + "Count back 3. ")
    it["e"] = "Count back 3 from 89: 88, 87, 86. 89 − 3 = <b>86</b>."
    its.append(it)
    its.append(mcq(plus_blocks(43, 5) + "Siti counts on from 43 to add 5. What does she say?",
                   "44, 45, 46, 47, 48", ["43, 44, 45, 46, 47", "45, 46, 47, 48, 49", "44, 45, 46, 47"],
                   "Start after 43. Say 5 numbers: 44, 45, 46, 47, 48. So 43 + 5 = <b>48</b>. "
                   "Do not say 43 again."))
    assert 43 + 5 == 48
    its.append(mcq(fig(blocks_svg([bo(52), bo(57)])) + "Find the missing number. 52 + <b>?</b> = 57",
                   5, [7, 4, 109],
                   "The tens stay the same. The ones go from 2 to 7. 2 + 5 = 7, so the missing number is <b>5</b>."))
    assert 52 + 5 == 57 and 52 + 57 == 109
    its.append(mcq("Kumar says 34 + 5 = 84. What did he do wrong?", "He added 5 to the tens",
                   ["He added 5 to the ones", "He took away 5", "He counted on 5"],
                   "5 is 5 ones. Add it to the ones: 4 + 5 = 9. 34 + 5 = 39. "
                   "Kumar got 84 because <b>he added 5 to the tens</b>."))
    assert 34 + 5 == 39 and 34 + 50 == 84
    its.append(mcq(fig(blocks_svg([bo(72)])) + "The blocks show 72. What is 4 more than 72?", 76, [112, 75, 68],
                   "4 more means add 4 ones: 2 + 4 = 6. The tens stay the same. 72 + 4 = <b>76</b>."))
    assert 72 + 4 == 76 and 72 + 40 == 112
    its.append(mcq(fig(blocks_svg([bo(98)])) + "The blocks show 98. What is 3 less than 98?", 95, [68, 96, 101],
                   "3 less means take away 3 ones: 8 − 3 = 5. The tens stay the same. 98 − 3 = <b>95</b>."))
    assert 98 - 3 == 95 and 98 - 30 == 68
    its.append(mcq("Which one is equal to 49?", "45 + 4", ["45 + 40", "44 + 4", "40 + 4"],
                   "45 + 4: the ones are 5 + 4 = 9, so <b>45 + 4</b> = 49. "
                   "45 + 40 = 85, 44 + 4 = 48 and 40 + 4 = 44."))
    assert 45 + 4 == 49 and 45 + 40 == 85 and 44 + 4 == 48
    assert len(its) == 20, len(its)
    return {"title": "Add and take away ones", "items": its}


# ============================================================ set 2: add and take away tens
def set_tens():
    its = []
    its.append(q_add(46, 30, plus_blocks(46, 30) + "Use the blocks. "))
    it = q_add(24, 30, fig(nline_svg(24, [10, 10, 10])) + "Count on in tens. ")
    it["e"] = "Count on 3 tens from 24: 34, 44, 54. The ones stay the same. 24 + 30 = <b>54</b>."
    its.append(it)
    it = q_sub(83, 40, fig(nline_svg(83, [-10, -10, -10, -10])) + "Count back in tens. ")
    it["e"] = "Count back 4 tens from 83: 73, 63, 53, 43. The ones stay the same. 83 − 40 = <b>43</b>."
    its.append(it)
    its.append(mcq(fig(blocks_svg([bo(58)])) + "The blocks show 58. What is 10 more than 58?", 68, [59, 78, 48],
                   "10 more means 1 more ten. 5 tens become 6 tens. The ones stay the same: <b>68</b>."))
    its.append(mcq(fig(blocks_svg([bo(64)])) + "The blocks show 64. What is 10 less than 64?", 54, [63, 44, 74],
                   "10 less means 1 less ten. 6 tens become 5 tens. The ones stay the same: <b>54</b>."))
    for a, b in [(35, 40), (52, 20), (17, 60), (63, 30)]:
        its.append(q_add(a, b, plus_blocks(a, b)))
    for a, b in [(78, 30), (91, 50), (66, 20), (87, 60)]:
        its.append(q_sub(a, b, fig(blocks_svg([bo(a)], cross=(b // 10, 0))) + "Take away the crossed-out tens. "))
    it = q_add(41, 50, fig(nline_svg(41, [10] * 5)) + "Count on in tens. ")
    it["e"] = "Count on 5 tens from 41: 51, 61, 71, 81, 91. The ones stay the same. 41 + 50 = <b>91</b>."
    its.append(it)
    it = q_sub(95, 30, fig(nline_svg(95, [-10] * 3)) + "Count back in tens. ")
    it["e"] = "Count back 3 tens from 95: 85, 75, 65. The ones stay the same. 95 − 30 = <b>65</b>."
    its.append(it)
    its.append(q_add(40, 30, plus_blocks(40, 30)))
    its.append(mcq(fig(blocks_svg([bo(37), bo(77)])) + "Find the missing number. 37 + <b>?</b> = 77",
                   40, [4, 114, 30],
                   "The ones stay at 7. The tens go from 3 to 7. That is 4 tens: <b>40</b>. Check: 37 + 40 = 77."))
    assert 37 + 40 == 77 and 37 + 77 == 114
    its.append(mcq(fig(blocks_svg([bo(45)])) + "The blocks show 45. What is 20 more than 45?", 65, [47, 25, 55],
                   "20 is 2 tens. 4 tens + 2 tens = 6 tens. The ones stay the same: <b>65</b>."))
    assert 45 + 20 == 65
    its.append(mcq("Ali says 46 + 30 = 49. What did he do wrong?", "He added 3 to the ones",
                   ["He added 3 to the tens", "He took away 30", "He forgot the ones"],
                   "30 is 3 tens. Add it to the tens: 4 + 3 = 7. 46 + 30 = 76. "
                   "Ali got 49 because <b>he added 3 to the ones</b>."))
    assert 46 + 30 == 76 and 46 + 3 == 49
    its.append(mcq("Start at 25. Count on 3 tens. Where do you stop?", 55, [28, 45, 65],
                   "Count on 3 tens: 35, 45, 55. You stop at <b>55</b>."))
    assert 25 + 30 == 55
    assert len(its) == 20, len(its)
    return {"title": "Add and take away tens", "items": its}


# ============================================================ set 3: column addition with renaming
def col_add(a, b):
    return q_add(a, b, fig(column_svg(a, b, "+")))


def set_col_add():
    its = []
    its.append(mcq(plus_blocks(7, 8) + "7 ones + 8 ones = 15 ones. 15 ones is 1 ten and how many ones?",
                   5, [15, 1, 8],
                   "Make a ten with 10 of the ones. 15 = 10 + 5. So 15 ones is 1 ten and <b>5</b> ones."))
    its.append(mcq(fig(column_svg(37, 8, "+")) + "In 37 + 8, the ones make 15. What do you do?",
                   "Write 5, rename 1 ten", ["Write 15 in the ones", "Write 1, rename 5 tens", "Leave out the 1"],
                   "15 ones is 1 ten and 5 ones. <b>Write 5</b> in the ones and <b>rename 10 ones as 1 ten</b>. "
                   "Add the 1 ten to the tens: 3 + 1 = 4. 37 + 8 = 45."))
    assert 37 + 8 == 45
    for a, b in [(37, 8), (48, 6), (29, 5), (56, 7), (75, 9), (64, 8), (89, 4)]:
        assert a % 10 + b >= 10
        its.append(col_add(a, b))
    for a, b in [(36, 27), (45, 38), (28, 47), (19, 56), (57, 35), (68, 24), (74, 18), (55, 45)]:
        assert a % 10 + b % 10 >= 10 and a + b <= 100
        its.append(col_add(a, b))
    its.append(mcq(fig(column_svg(48, 35, "+", shown=73)) +
                   "Mei Ling says 48 + 35 = 73. What did she do wrong?",
                   "She forgot the renamed ten", ["She added the ones wrongly", "She took away", "She added the tens twice"],
                   "Ones: 8 + 5 = 13. Write 3 and rename 1 ten. Tens: 4 + 3 + 1 = 8. 48 + 35 = 83. "
                   "Mei Ling got 73 because <b>she forgot the renamed ten</b>."))
    assert 48 + 35 == 83
    its.append(mcq("Which sum needs renaming?", "38 + 25", ["32 + 45", "41 + 27", "53 + 16"],
                   "In <b>38 + 25</b>, the ones make 8 + 5 = 13. That is 10 or more, so rename 10 ones as 1 ten. "
                   "In the others, the ones make less than 10."))
    its.append(col_add(27, 63))
    assert len(its) == 20, len(its)
    return {"title": "Add in columns with renaming", "items": its}


# ============================================================ set 4: column subtraction with renaming
def col_sub(a, b):
    return q_sub(a, b, fig(column_svg(a, b, "-")))


def set_col_sub():
    its = []
    its.append(mcq(fig(blocks_svg([bo(52)])) + "The blocks show 52. You want to take away 17. "
                   "There are not enough ones. What do you do?",
                   "Rename 1 ten", ["Do 7 − 2", "Write 0 ones", "Take away 2 tens"],
                   "52 has only 2 ones. You need to take away 7. <b>Rename 1 ten</b> as 10 ones. "
                   "Then there are 12 ones. Doing 7 − 2 is a common mistake."))
    its.append(mcq(fig(blocks_svg([(4, 12)], label="52 as 4 tens and 12 ones")) +
                   "You rename 1 ten in 52. What is 52 now?", "4 tens and 12 ones",
                   ["5 tens and 12 ones", "4 tens and 2 ones", "3 tens and 12 ones"],
                   "Take 1 ten from the 5 tens: 4 tens are left. The 10 ones join the 2 ones: 12 ones. "
                   "So 52 = <b>4 tens and 12 ones</b>."))
    assert 40 + 12 == 52
    for a, b in [(43, 7), (52, 6), (71, 4), (36, 9), (65, 8), (90, 3), (84, 5)]:
        assert b > a % 10
        its.append(col_sub(a, b))
    for a, b in [(53, 17), (63, 28), (81, 36), (74, 49), (90, 45), (45, 18), (62, 37), (93, 56)]:
        assert b % 10 > a % 10 and a // 10 - 1 - b // 10 >= 1
        its.append(col_sub(a, b))
    its.append(mcq(fig(column_svg(52, 17, "-", shown=45)) +
                   "Jun Jie says 52 − 17 = 45. What did he do wrong?", "He did 7 − 2",
                   ["He added the ones", "He forgot the tens", "He did 12 − 7"],
                   "In the ones, Jun Jie took 2 from 7. But you must take 7 from 2. You cannot, so rename 1 ten. "
                   "12 − 7 = 5 and 4 − 1 = 3. 52 − 17 = 35. His mistake: <b>he did 7 − 2</b>."))
    assert small_from_big(52, 17) == 45 and 52 - 17 == 35
    its.append(mcq("Hui Min works out 63 − 28 = 35. Which sum checks her answer?", "35 + 28",
                   ["35 + 63", "63 + 28", "35 − 28"],
                   "Add the answer and the number you took away. You should get 63. <b>35 + 28</b> = 63, "
                   "so she is right."))
    assert 35 + 28 == 63
    its.append(mcq("Which subtraction needs renaming?", "64 − 27", ["67 − 24", "78 − 42", "59 − 13"],
                   "In <b>64 − 27</b>, there are only 4 ones. You need to take away 7, so rename 1 ten. "
                   "In the others, the top ones digit is big enough."))
    assert len(its) == 20, len(its)
    return {"title": "Subtract in columns with renaming", "items": its}


# ============================================================ set 5: word problems
def set_words():
    its = []

    def unit(v, u):
        return "$%d" % v if u == "$" else "%d %s" % (v, u)

    def add_story(q, a, b, u, lead, pic=True):
        s = a + b
        pre = fig(bond_svg("?", unit(a, u) if u == "$" else str(a), unit(b, u) if u == "$" else str(b))) if pic else ""
        e = lead + e_add(a, b) + (" The answer is <b>$%d</b>." % s if u == "$" else "")
        its.append(mcq(pre + q, unit(s, u), [unit(v, u) for v in cands_add(a, b)], e))

    def sub_story(q, whole, take, u, lead, pic=True):
        r = whole - take
        lab = (lambda v: unit(v, u)) if u == "$" else str
        pre = fig(bond_svg(lab(whole), lab(take), "?")) if pic else ""
        e = lead + e_sub(whole, take) + (" The answer is <b>$%d</b>." % r if u == "$" else "")
        its.append(mcq(pre + q, unit(r, u), [unit(v, u) for v in cands_sub(whole, take)], e))

    ALL = "Put the two parts together, so add. "
    LEFT = "You know the whole and one part. Find the other part, so subtract. "
    add_story("Siti has 34 stickers. She gets 5 more. How many stickers does she have now?", 34, 5, "stickers", ALL)
    add_story("There are 45 people on a bus. 20 more people get on. How many people are on the bus now?",
              45, 20, "people", ALL)
    sub_story("The school canteen has 56 curry puffs. Pupils buy 30 of them at recess. How many curry puffs are left?",
              56, 30, "curry puffs", LEFT)
    add_story("Wei Ming reads 27 pages on Monday. He reads 18 pages on Tuesday. How many pages does he read in all?",
              27, 18, "pages", ALL)
    sub_story("Mdm Wong has 72 mandarin oranges for Chinese New Year. She gives away 25. How many are left?",
              72, 25, "oranges", LEFT)
    add_story("A class has 19 boys and 16 girls. How many pupils are in the class?", 19, 16, "pupils", ALL)
    sub_story("There are 60 books on a library shelf. Pupils borrow 23 of them. How many books are still on the shelf?",
              60, 23, "books", LEFT)
    add_story("Jun Jie gets $38 in red packets. Then he gets $26 more. How much money does he get in all?",
              38, 26, "$", ALL)
    sub_story("Kavya has $50. She spends $18 on a book. How much money does she have left?", 50, 18, "$", LEFT)
    # comparison: the bigger number is the whole
    r = 52 - 38
    its.append(mcq(fig(bond_svg("52", "38", "?")) + "Raju has 52 marbles. Hafiz has 38 marbles. "
                   "How many more marbles does Raju have?", unit(r, "marbles"),
                   [unit(v, "marbles") for v in cands_sub(52, 38)],
                   "How many more means find the difference, so subtract. " + e_sub(52, 38)))
    sub_story("Mr Tan has 83 rambutans. He sells 45 of them. How many rambutans does he have left?",
              83, 45, "rambutans", LEFT)
    add_story("On Sports Day, 46 pupils run a race. Then 38 more pupils run. How many pupils run in all?",
              46, 38, "pupils", ALL)
    add_story("For Deepavali, Priya lights 24 oil lamps. Then she lights 9 more. How many oil lamps does she light?",
              24, 9, "lamps", ALL)
    sub_story("There are 64 people on an MRT train. 28 people get off at the next station. "
              "How many people are still on the train?", 64, 28, "people", LEFT)
    add_story("Ryan has 57 shells. He finds 6 more at East Coast Park. How many shells does he have now?",
              57, 6, "shells", ALL)
    sub_story("Mrs Lim has 90 paper cups for Children’s Day. The class uses 42 cups. How many cups are left?",
              90, 42, "cups", LEFT)
    add_story("Xin Yi has 46 beads. Hui Min has 9 more beads than Xin Yi. How many beads does Hui Min have?",
              46, 9, "beads", "Hui Min has more, so add. ")
    sub_story("Zhi Hao has 70 cards. He gives 35 cards to his brother. How many cards does Zhi Hao have left?",
              70, 35, "cards", LEFT)
    its.append(mcq(fig(bond_svg("63", "27", "?")) + "Sarah has 63 stickers. She gives away 27. "
                   "Which number sentence finds how many are left?", "63 − 27 = ?",
                   ["63 + 27 = ?", "27 − 63 = ?", "? − 63 = 27"],
                   "She gives some away, so take away. Start with 63 and take away 27: <b>63 − 27 = ?</b>. "
                   "The answer is 36."))
    assert 63 - 27 == 36
    add_story("At a hawker centre, Mr Rahman sells 36 plates of chicken rice in the morning. "
              "He sells 45 plates at lunch. How many plates does he sell in all?", 36, 45, "plates", ALL)
    assert len(its) == 20, len(its)
    return {"title": "Word problems with number bonds", "items": its}


# ============================================================ lesson
def body_html():
    assert 43 + 5 == 48 and 46 + 30 == 76 and 36 + 27 == 63 and 52 - 17 == 35 and 72 - 25 == 47
    assert side_by_side(36, 27) == 513 and small_from_big(52, 17) == 45 and 43 + 50 == 93 and 46 + 3 == 49
    return (
        "<h2>The idea: ones with ones, tens with tens</h2>"
        "<p>A 2-digit number has <b>tens</b> and <b>ones</b>. 43 is 4 tens and 3 ones. "
        "Add ones to ones. Add tens to tens.</p>"
        "<figure class='sn-fig'>" + blocks_svg([bo(43), bo(5)], sign=True) +
        "<figcaption>43 + 5. Add the ones: 3 + 5 = 8. The tens stay the same. 43 + 5 = 48.</figcaption></figure>"
        "<figure class='sn-fig'>" + blocks_svg([bo(46), bo(30)], sign=True) +
        "<figcaption>46 + 30. 30 is 3 tens. Add the tens: 4 + 3 = 7. The ones stay the same. "
        "46 + 30 = 76.</figcaption></figure>"
        "<h2>Add in columns: rename 10 ones as 1 ten</h2>"
        "<p>Write ones under ones and tens under tens. Start with the ones. "
        "If the ones make 10 or more, <b>rename</b> 10 ones as 1 ten.</p>"
        "<figure class='sn-fig'>" + column_svg(36, 27, "+", answer=True, marks=True, fs=34) +
        "<figcaption>Ones: 6 + 7 = 13. Write 3. Rename 10 ones as 1 ten. "
        "Tens: 3 + 2 + 1 = 6. Answer: 63.</figcaption></figure>"
        "<h2>Subtract in columns: rename 1 ten as 10 ones</h2>"
        "<p>Take the <b>bottom</b> digit from the <b>top</b> digit. "
        "If the top digit is too small, rename 1 ten as 10 ones.</p>"
        "<figure class='sn-fig'>" + column_svg(52, 17, "-", answer=True, marks=True, fs=34) +
        "<figcaption>You cannot take 7 ones from 2 ones. Rename 1 ten: 4 tens and 12 ones. "
        "Ones: 12 − 7 = 5. Tens: 4 − 1 = 3. Answer: 35.</figcaption></figure>"
        "<h2>Word problems: use a number bond</h2>"
        "<p>Find the whole and the parts. If you know both parts, add. "
        "If you know the whole and one part, subtract.</p>"
        "<figure class='sn-fig'>" + bond_svg("72", "25", "?") +
        "<figcaption>The whole is 72. One part is 25. The other part is 72 − 25.</figcaption></figure>" +
        ex("Number bond", "Mdm Wong has 72 oranges. She gives away 25. How many are left?",
           "72 − 25. You cannot take 5 from 2, so rename 1 ten. 12 − 5 = 7. 6 − 2 = 4.", "47 oranges") +
        "<h2>Common mistakes</h2>" +
        table(["Mistake", "What to do instead"], [
            ["Adding ones to the tens: 43 + 5 = 93", "5 is 5 ones. Add it to the ones: 48"],
            ["Adding tens to the ones: 46 + 30 = 49", "30 is 3 tens. Add it to the tens: 76"],
            ["Not renaming: 36 + 27 = 513", "13 ones is 1 ten and 3 ones. Answer: 63"],
            ["Taking the smaller digit from the larger: 52 − 17 = 45",
             "You cannot take 7 from 2. Rename 1 ten: 12 − 7 = 5. Answer: 35"],
        ])
    )


FAQ = [
    {"q": "What is taught in P1 addition and subtraction?",
     "a": "Primary 1 pupils add and subtract within 100. They add or take away ones and tens in their heads, "
          "use the column method with renaming, and solve one-step word problems."},
    {"q": "How do I explain renaming to my child?",
     "a": "Renaming means changing 10 ones for 1 ten, or 1 ten for 10 ones. Use bundles of 10 straws: "
          "when you have 13 loose straws, tie 10 of them into 1 bundle."},
    {"q": "What is the most common mistake in P1 addition and subtraction?",
     "a": "Mixing up tens and ones is the most common mistake, such as 46 + 30 = 49. In subtraction, many children "
          "take the smaller digit from the larger one, so 52 − 17 becomes 45 instead of 35."},
    {"q": "Is addition and subtraction within 100 in the MOE syllabus?",
     "a": "Yes. Adding and subtracting within 100, with the column method and mental calculation, is part of "
          "Number and Algebra in the MOE 2021 Primary 1 Mathematics Syllabus (Standard)."},
]


def verify(sets):
    n = 0
    for s in sets:
        for it in s["items"]:
            right = it["c"][it["a"]]
            m = re.search(r"What is (\d+) ([+−]) (\d+)\?$", it["q"])
            if m:
                a, op, b = int(m.group(1)), m.group(2), int(m.group(3))
                v = a + b if op == "+" else a - b
                assert int(right) == v and 0 < v <= 100, it["q"]
                n += 1
            m = re.search(r"aria-label='(\d+) (plus|minus) (\d+) written in columns'", it["q"])
            if m and "What is" in it["q"]:
                a, op, b = int(m.group(1)), m.group(2), int(m.group(3))
                assert int(right) == (a + b if op == "plus" else a - b), it["q"]
                n += 1
            m = re.search(r"aria-label='number bond: whole (\S+), parts (\S+) and (\S+)'", it["q"])
            if m and "number sentence" not in it["q"]:
                vals = [m.group(1), m.group(2), m.group(3)]
                k = vals.index("?")
                nums = [int(x.lstrip("$")) for x in vals if x != "?"]
                want = nums[0] + nums[1] if k == 0 else nums[0] - nums[1]
                assert int(right.lstrip("$").split()[0]) == want, it["q"]
                n += 1
            for c in it["c"]:
                mm = re.match(r"\$?(\d+)", c)
                if mm and re.fullmatch(r"\$?\d+( [a-z ]+)?", c):
                    assert int(mm.group(1)) < 1000, c
    return n


def gen():
    rnd = random.Random(61805)
    sets = [set_ones(), set_tens(), set_col_add(), set_col_sub(), set_words()]
    balance(sets, rnd)
    n = verify(sets)
    assert n >= 70, n
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
            for x in [it["q"], it["e"]] + it["c"]:
                assert "\\" not in x and '"' not in x, x
    u = {
        "country": "sg", "subject": "maths", "grade": "primary-1", "slug": "addition-and-subtraction-within-100",
        "sort": 5, "updated": UPDATED, "pdf_url": "",
        "title": "Primary 1 Addition and Subtraction Within 100",
        "seo_title": "P1 Addition and Subtraction Within 100 Worksheets: Free Primary 1 Maths with Answers (MOE Syllabus)",
        "short_title": "Addition and Subtraction Within 100",
        "domain": "Number and Algebra",
        "standard_code": "Primary 1: Addition and Subtraction",
        "standard_url": "https://www.moe.gov.sg/primary/curriculum/syllabus",
        "standard_text": "Adding and subtracting within 100, using algorithms; mental calculation with a 2-digit number and ones or tens",
        "meta_desc": "Free P1 maths practice: add and take away ones and tens, column addition and subtraction "
                     "with renaming, and word problems. 100 questions with answers.",
        "key_big": "Add ones to ones and tens to tens. Rename 10 ones as 1 ten.",
        "key_sub": "36 + 27: 6 + 7 = 13, write 3 and rename 1 ten. 3 + 2 + 1 = 6 tens. Answer: 63.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }
    assert len(u["meta_desc"]) <= 160, len(u["meta_desc"])
    return mark_large(u, "tens and ones blocks|number line")


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
