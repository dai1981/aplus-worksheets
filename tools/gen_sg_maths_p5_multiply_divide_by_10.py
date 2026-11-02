# -*- coding: utf-8 -*-
"""
Singapore Primary 5 Maths: Multiplying and dividing by 10, 100, 1000 and their multiples
(MOE 2021 Primary Mathematics Syllabus, Standard, Primary 5: Whole Numbers)
  python3 tools/gen_sg_maths_p5_multiply_divide_by_10.py
Whole numbers to 10 million. × and ÷ by 10, 100 and 1000 move every digit 1, 2 or 3 places (place value
charts with arrows). Multiples (× 30, × 400, ÷ 20, ÷ 300) split into a basic fact and a power of 10
(step diagrams). Estimation rounds first, then uses the same rules. Word problems use Singapore contexts
and bar models. Every answer is computed in code. Singapore style: 4-digit numbers without a separator,
5 or more digits grouped with a no-break space. HTML attributes use single quotes (no backslashes).
"""
import json, os, random, re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "sg", "maths", "primary-5")
UPDATED = "2026-11-03"
NB = " "              # no-break space between groups of three digits
MINUS = "−"
GREEN = "#006633"
HEADFILL = "#cfe6d6"
BARFILL = "#e3f1e7"
INK = "#2b2b2b"
RED = "#c0392b"
GHOST = "#9a9a9a"          # zeros that only fill empty places
FONT = "Arial, Helvetica, sans-serif"
SHORT = {6: "M", 5: "HTh", 4: "TTh", 3: "Th", 2: "H", 1: "T", 0: "O"}
PLACE = {6: "millions", 5: "hundred thousands", 4: "ten thousands", 3: "thousands", 2: "hundreds", 1: "tens", 0: "ones"}


# ------------------------------------------------------------ numbers
def N(x):
    """Singapore style: 4536, 10 000, 1 250 000 (no-break spaces)."""
    x = int(x)
    assert x >= 0
    return str(x) if x < 10000 else format(x, ",").replace(",", NB)


def I(s):
    return int(str(s).replace(NB, "").replace(" ", "").replace(",", ""))


def D(x):
    return "$" + N(x)


def P10(k):
    return N(10 ** k)


def zeros(k):
    return "1 zero" if k == 1 else "%d zeros" % k


def places(k):
    return "1 place" if k == 1 else "%d places" % k


VAL = re.compile(r"^(?:About )?\$?([\d" + NB + r"]+)(?: ([a-z]+))?$")


def val(c):
    m = VAL.match(c)
    if not m:
        return None
    return (I(m.group(1)), m.group(2) or "")


# ------------------------------------------------------------ helpers
def mcq(q, correct, wrong, e):
    c = [str(correct)] + [str(w) for w in wrong]
    assert len(c) == 4 and len(set(c)) == 4, (q, c)
    vs = [val(x) for x in c if val(x) is not None]
    assert len(set(vs)) == len(vs), (q, c)
    for x in c:
        assert not re.search(r"\d \d", x), ("typed space in number", x)
    return {"q": q, "c": c, "a": 0, "e": e}


def balance(sets, rnd):
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


def fig(svg):
    return "<div class='qfig'>" + svg + "</div>"


def svg_wrap(w, h, body, label):
    return ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 %d %d' width='%d' height='%d' "
            "role='img' aria-label='%s'><g font-family='%s'>%s</g></svg>" % (w, h, w, h, label, FONT, body))


def text(x, y, t, fs=16, anchor="middle", col=INK, weight=700):
    return ("<text x='%.1f' y='%.1f' font-size='%d' font-weight='%d' fill='%s' text-anchor='%s'>%s</text>"
            % (x, y, fs, weight, col, anchor, t))


def table(head, rows):
    h = "".join("<th>%s</th>" % x for x in head)
    b = "".join("<tr>" + "".join("<td>%s</td>" % c for c in r) + "</tr>" for r in rows)
    return "<div class='sn-tw'><table class='sn-table'><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>" % (h, b)


def ex(title, q, s, a):
    return ("<div class='sn-ex'><span class='sn-ex-t'>%s</span><p class='sn-ex-q'>%s</p>"
            "<p class='sn-ex-s'>%s</p><p class='sn-ex-a'>Answer: %s</p></div>" % (title, q, s, a))


def calc(x, op, k):
    x = I(x)
    if op == "×":
        return x * 10 ** k
    assert x % 10 ** k == 0, (x, k)
    return x // 10 ** k


# ------------------------------------------------------------ figure: place value chart with arrows
def digits(x):
    s = str(I(x))
    return {len(s) - 1 - j: ch for j, ch in enumerate(s)}


def pv_move(x, op, k, hi=None, CW=56):
    """Two-row place value chart: x on top, the answer below, arrows from each digit to its new place.
    Zeros that only fill empty places are grey. hi: place of a digit in x; it is red in the answer row."""
    r = calc(x, op, k)
    top, bot = digits(x), digits(r)
    shift = k if op == "×" else -k
    moved = {p + shift for p in top}
    hi_place = None if hi is None else hi + shift
    cols = list(range(max(max(top), max(bot)), -1, -1))
    HEAD, ROW, BAND, LW = 30, 44, 46, 74
    x0, y0 = 4, 4
    gw = len(cols) * CW
    W = 2 * x0 + LW + gw
    yt = y0 + HEAD
    yb = yt + ROW + BAND
    gy = yb + ROW
    H = gy + y0
    xs = {p: x0 + LW + i * CW for i, p in enumerate(cols)}
    cx = {p: xs[p] + CW / 2.0 for p in cols}
    o = ["<rect x='%d' y='%d' width='%d' height='%d' fill='#fff' stroke='%s' stroke-width='2'/>"
         % (x0 + LW, y0, gw, gy - y0, GREEN),
         "<rect x='%d' y='%d' width='%d' height='%d' fill='%s'/>" % (x0 + LW, y0, gw, HEAD, HEADFILL)]
    for p in cols:
        if p != cols[0]:
            o.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='1'/>"
                     % (xs[p], y0, xs[p], gy, GREEN))
        o.append(text(cx[p], y0 + 21, SHORT[p], 15, col=GREEN))
    for yy in (yt, yt + ROW, yb):
        o.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='%d'/>"
                 % (x0 + LW, yy, x0 + LW + gw, yy, GREEN, 2 if yy == yt else 1))
    for p, ch in top.items():
        o.append(text(cx[p], yt + 32, ch, 28, weight=800))
    for p, ch in bot.items():
        col = INK if p in moved else GHOST
        if hi_place == p:
            col = RED
        o.append(text(cx[p], yb + 32, ch, 28, col=col, weight=800))
    y1, y2 = yt + ROW + 5, yb - 5
    for p in top:
        if p + shift not in bot:        # a zero that is taken away when dividing
            continue
        xa, xb = cx[p], cx[p + shift]
        L = ((xb - xa) ** 2 + (y2 - y1) ** 2) ** 0.5
        ux, uy = (xb - xa) / L, (y2 - y1) / L
        hx, hy = xb - ux * 11, y2 - uy * 11
        o.append("<line x1='%.1f' y1='%d' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='2.5'/>" % (xa, y1, hx, hy, RED))
        o.append("<polygon points='%.1f,%.1f %.1f,%.1f %.1f,%.1f' fill='%s'/>"
                 % (xb, y2, hx - uy * 5.5, hy + ux * 5.5, hx + uy * 5.5, hy - ux * 5.5, RED))
    o.append(text(x0 + LW - 10, yt + ROW + BAND / 2.0 + 6, "%s %s" % (op, P10(k)), 17, anchor="end", col=GREEN))
    lab = "place value chart: %s %s %s, every digit moves %s to the %s, giving %s" % (
        N(x), "times" if op == "×" else "divided by", P10(k), places(k), "left" if op == "×" else "right", N(r))
    return svg_wrap(W, H, "".join(o), lab)


# ------------------------------------------------------------ figure: step diagram (400 × 30 → 12 → 12 000)
def tw(s, fs):
    """Rough width of bold Arial text."""
    w = 0.0
    for ch in s:
        w += 0.30 if ch in NB + " " else 0.62 if ch.isdigit() else 0.62 if ch in "×÷?" else 0.6
    return w * fs


def steps(start, ops, label):
    """Boxes joined by arrows; each arrow has its step above it. start and the boxes are strings."""
    FS, OFS, BH, AW, PAD = 20, 16, 40, 96, 16
    boxes = [start] + [b for _, b in ops]
    widths = [max(56, tw(b, FS) + 2 * PAD) for b in boxes]
    x, y0 = 4, 30
    o = []
    for i, b in enumerate(boxes):
        w = widths[i]
        q = b == "?"
        o.append("<rect x='%.1f' y='%d' width='%.1f' height='%d' rx='6' fill='%s' stroke='%s' stroke-width='2'/>"
                 % (x, y0, w, BH, "#fff" if q else BARFILL, RED if q else GREEN))
        o.append(text(x + w / 2.0, y0 + 27, b, FS, col=RED if q else INK, weight=800))
        x += w
        if i < len(ops):
            ax1, ax2, ay = x + 6, x + AW - 6, y0 + BH / 2.0
            o.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='2.5'/>"
                     % (ax1, ay, ax2 - 9, ay, GREEN))
            o.append("<polygon points='%.1f,%.1f %.1f,%.1f %.1f,%.1f' fill='%s'/>"
                     % (ax2, ay, ax2 - 11, ay - 6, ax2 - 11, ay + 6, GREEN))
            o.append(text(x + AW / 2.0, y0 - 9, ops[i][0], OFS, col=GREEN))
            x += AW
    W = int(x + 4 + 0.5)
    H = y0 + BH + 4
    return svg_wrap(W, H, "".join(o), "step diagram: " + label)


# ------------------------------------------------------------ figure: bar model
def brace(x1, x2, y, up=True):
    d = -1 if up else 1
    m = (x1 + x2) / 2.0
    h = 7
    return ("<path d='M%.1f %.1f Q%.1f %.1f %.1f %.1f L%.1f %.1f Q%.1f %.1f %.1f %.1f Q%.1f %.1f %.1f %.1f "
            "L%.1f %.1f Q%.1f %.1f %.1f %.1f' fill='none' stroke='%s' stroke-width='2'/>"
            % (x1, y, x1, y + d * h, x1 + 8, y + d * h, m - 8, y + d * h, m, y + d * h, m, y + d * 2 * h,
               m, y + d * h, m + 8, y + d * h, x2 - 8, y + d * h, x2, y + d * h, x2, y, INK))


def bar_cells(x0, y, n, unit_lab, CW=56, BH=36):
    """A bar of n equal units. Long bars show 3 units, a gap and the last unit."""
    o = []
    if n <= 7:
        cells = [(x0 + i * CW, CW, False) for i in range(n)]
    else:
        cells = [(x0 + i * CW, CW, False) for i in range(3)] + [(x0 + 3 * CW, 2 * CW, True), (x0 + 5 * CW, CW, False)]
    for i, (cx, w, gap) in enumerate(cells):
        if gap:
            for yy in (y, y + BH):
                o.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='2' stroke-dasharray='6 5'/>"
                         % (cx, yy, cx + w, yy, GREEN))
            o.append(text(cx + w / 2.0, y + 24, "…", 20, col=GREEN))
        else:
            o.append("<rect x='%d' y='%d' width='%d' height='%d' fill='%s' stroke='%s' stroke-width='2'/>"
                     % (cx, y, w, BH, BARFILL, GREEN))
    c0 = cells[0]
    o.append(text(c0[0] + c0[1] / 2.0, y + 24, unit_lab, 15, col=RED if unit_lab == "?" else INK))
    end = cells[-1][0] + cells[-1][1]
    return o, end


def bar_model(n, unit_lab, top_lab, bottom_lab, label):
    """One bar of n units: unit value in the first unit, total above (brace), number of units below (brace)."""
    x0, y = 8, 40
    o, end = bar_cells(x0, y, n, unit_lab)
    o.append(brace(x0, end, y - 4, up=True))
    o.append(text((x0 + end) / 2.0, y - 22, top_lab, 16, col=RED if top_lab.startswith("?") else INK))
    o.append(brace(x0, end, y + 36 + 4, up=False))
    o.append(text((x0 + end) / 2.0, y + 36 + 36, bottom_lab, 16, col=RED if bottom_lab.startswith("?") else INK))
    W = int(max(end, x0 + tw(top_lab, 16), x0 + tw(bottom_lab, 16)) + 8)
    H = y + 36 + 42
    return svg_wrap(W, H, "".join(o), "bar model: " + label)


def compare_model(name_a, n, name_b, unit_lab, label):
    """Two bars: A has n units (total ?), B has 1 unit."""
    LW, x0, ya, yb = 70, 78, 40, 112
    o = [text(LW, ya + 24, name_a, 15, anchor="end"), text(LW, yb + 24, name_b, 15, anchor="end")]
    oa, end = bar_cells(x0, ya, n, "")
    o += oa
    o.append(brace(x0, end, ya - 4, up=True))
    o.append(text((x0 + end) / 2.0, ya - 22, "?", 16, col=RED))
    ob, _ = bar_cells(x0, yb, 1, unit_lab)
    o += ob
    o.append(text(x0 + 56 + 10, yb + 24, "(1 unit)", 14, anchor="start", col=GREEN, weight=400))
    o.append(text(x0 + 3 * 56 + 56, ya + 58, "%d units" % n, 14, col=GREEN, weight=400))
    W = int(end + 8)
    H = yb + 36 + 6
    return svg_wrap(W, H, "".join(o), "bar model: " + label)


# ------------------------------------------------------------ question makers
def p10_e(x, op, k, note=""):
    r = calc(x, op, k)
    if op == "×":
        e = ("× %s: every digit moves <b>%s to the left</b>, so write %s at the end. "
             % (P10(k), places(k), zeros(k)))
    else:
        e = ("÷ %s: every digit moves <b>%s to the right</b>, so take away the last %s. "
             % (P10(k), places(k), "zero" if k == 1 else zeros(k)))
    e += "%s %s %s = <b>%s</b>." % (N(x), op, P10(k), N(r))
    if note:
        e += " " + note
    return e


def p10(its, x, op, k, wrong, note=""):
    its.append(mcq("%s %s %s = ?" % (N(x), op, P10(k)), N(calc(x, op, k)), [N(w) for w in wrong], p10_e(x, op, k, note)))


def which_calc(its, x, op, k, wrong):
    r = N(calc(x, op, k))
    e = ("Every digit moved %s to the <b>%s</b>, so it is %s %s. <b>%s %s %s</b> = %s."
         % (places(k), "left" if op == "×" else "right", op, P10(k), N(x), op, P10(k), r))
    its.append(mcq(fig(pv_move(x, op, k)) + "Which calculation does the place value chart show?",
                   "%s %s %s" % (N(x), op, P10(k)), wrong, e))


def red_digit(its, x, op, k, src, wrong):
    r = calc(x, op, k)
    p = src + (k if op == "×" else -k)
    dg = digits(r)[p]
    right = N(int(dg) * 10 ** p)
    e = ("Every digit moved %s to the %s, so the %s is now in the <b>%s</b> place. Its value is <b>%s</b>."
         % (places(k), "left" if op == "×" else "right", dg, PLACE[p], right))
    its.append(mcq(fig(pv_move(x, op, k, hi=src)) +
                   "The chart shows %s %s %s = %s. What is the value of the red digit?" % (N(x), op, P10(k), N(r)),
                   right, [N(w) for w in wrong], e))


def split10(n):
    """2050 -> (205, 1)."""
    k = 0
    while n % 10 == 0 and n > 0:
        n //= 10
        k += 1
    return n, k


def mul_e(a, b, note=""):
    a0, i = split10(a)
    b0, j = split10(b)
    k = i + j
    e = ("%s × %s = %s × %s × %s. %s × %s = %s, and %s × %s = <b>%s</b>."
         % (N(a), N(b), N(a0), N(b0), P10(k), N(a0), N(b0), N(a0 * b0), N(a0 * b0), P10(k), N(a * b)))
    if note:
        e += " " + note
    return e


def div_e(a, b, note=""):
    b0, j = split10(b)
    assert a % 10 ** j == 0 and (a // 10 ** j) % b0 == 0, (a, b)
    t = a // 10 ** j
    if b0 == 1:
        e = "÷ %s takes away the last %s: %s ÷ %s = <b>%s</b>." % (P10(j), "zero" if j == 1 else zeros(j), N(a), N(b), N(t))
    else:
        e = ("%s = %s × %s, so divide by %s first, then by %s. %s ÷ %s = %s, and %s ÷ %s = <b>%s</b>."
             % (N(b), N(b0), P10(j), P10(j), N(b0), N(a), P10(j), N(t), N(t), N(b0), N(t // b0)))
    if note:
        e += " " + note
    return e


def mul(its, a, b, wrong, note=""):
    its.append(mcq("%s × %s = ?" % (N(a), N(b)), N(a * b), [N(w) for w in wrong], mul_e(a, b, note)))


def div(its, a, b, wrong, note=""):
    assert a % b == 0
    its.append(mcq("%s ÷ %s = ?" % (N(a), N(b)), N(a // b), [N(w) for w in wrong], div_e(a, b, note)))


# ============================================================ set 1: × 10, 100, 1000
def set_times():
    its = []
    p10(its, 47, "×", 1, [4700, 57, 407], "(57 adds 10; it does not multiply.)")
    p10(its, 63, "×", 2, [630, 63000, 163])
    p10(its, 8, "×", 3, [800, 80000, 1008])
    p10(its, 250, "×", 1, [25000, 260, 25], "(25 000 has 2 extra zeros: that is × 100.)")
    p10(its, 406, "×", 2, [4060, 406000, 46000], "(Keep the 0 in the tens place of 406.)")
    which_calc(its, 58, "×", 3, ["58 × 100", "58 × 10" + NB + "000", "58 ÷ 1000"])
    p10(its, 3120, "×", 1, [312000, 3130, 312])
    its.append(mcq("72 × ? = 72" + NB + "000", "1000", ["100", "10", "10" + NB + "000"],
                   "72 000 is 72 with 3 zeros at the end: every digit moved 3 places to the left. So it is × <b>1000</b>."))
    p10(its, 905, "×", 3, [90500, 9050000, 95000], "(95 000 drops the 0 in the tens place of 905.)")
    p10(its, 1600, "×", 2, [16000, 1600000, 1700])
    its.append(mcq("? × 100 = 48" + NB + "000", "480", ["48", "4800", "47" + NB + "900"],
                   "Use the inverse: 48 000 ÷ 100. Take away the last 2 zeros: <b>480</b>. Check: 480 × 100 = 48 000."))
    which_calc(its, 2370, "×", 2, ["2370 × 10", "2370 × 1000", "2370 ÷ 100"])
    p10(its, 4050, "×", 3, [405000, 450000, 40500], "(Keep the 0 in the hundreds place of 4050.)")
    red_digit(its, 3684, "×", 2, 2, [600, 6000, 600000])
    p10(its, 7009, "×", 1, [70900, 700900, 7019], "(Keep both zeros inside 7009.)")
    its.append(mcq("? × 1000 = 6" + NB + "400" + NB + "000", "6400", ["640", "64" + NB + "000", "64"],
                   "Use the inverse: 6 400 000 ÷ 1000. Take away the last 3 zeros: <b>6400</b>. Check: 6400 × 1000 = 6 400 000."))
    its.append(mcq("Which number is 1000 times as large as 520?", N(520000), [N(52000), N(5200000), "1520"],
                   "1000 times as large means × 1000. Write 3 zeros at the end: 520 × 1000 = <b>520 000</b>. (1520 adds 1000.)"))
    its.append(mcq("Which calculation has the answer 30" + NB + "000?", "300 × 100", ["30 × 100", "300 × 1000", "3 × 1000"],
                   "300 × 100: write 2 zeros after 300, so <b>300 × 100</b> = 30 000. "
                   "30 × 100 = 3000, 300 × 1000 = 300 000 and 3 × 1000 = 3000."))
    its.append(mcq("Hui Min says 2500 × 100 = 25" + NB + "000. What is her mistake?",
                   "She wrote 1 zero, not 2; it is 250" + NB + "000",
                   ["She should write 3 zeros: 2" + NB + "500" + NB + "000", "She should add 100: 2600", "There is no mistake"],
                   "× 100 means 2 more zeros at the end. 2500 already has 2 zeros; it needs 2 more: "
                   "2500 × 100 = <b>250 000</b>. 25 000 is only 2500 × 10."))
    its.append(mcq("68 × 10 × 100 = ?", N(68000), ["6800", N(680000), "680"],
                   "× 10 and then × 100 is the same as × 1000 (1 + 2 = 3 zeros). 68 × 1000 = <b>68 000</b>."))
    assert len(its) == 20, len(its)
    return {"title": "Multiply by 10, 100 and 1000", "items": its}


# ============================================================ set 2: ÷ 10, 100, 1000
def set_divide():
    its = []
    p10(its, 4800, "÷", 1, [48, 48000, 4790], "(48 takes away 2 zeros: that is ÷ 100.)")
    p10(its, 36000, "÷", 2, [3600, 36, 35900])
    p10(its, 9000, "÷", 3, [90, 900, 8000], "(8000 takes away 1000; it does not divide.)")
    p10(its, 70500, "÷", 2, [75, 7050, 7050000], "(Only the last 2 zeros go. The 0 in 705 stays: it holds a place.)")
    p10(its, 250000, "÷", 3, [25, 2500, 249000])
    which_calc(its, 64000, "÷", 2, ["64" + NB + "000 ÷ 10", "64" + NB + "000 ÷ 1000", "64" + NB + "000 × 100"])
    p10(its, 3060, "÷", 1, [36, 30600, 3050], "(The 0 in the hundreds place of 3060 stays.)")
    p10(its, 5200000, "÷", 3, [520, 52000, 52])
    p10(its, 810000, "÷", 2, [810, 81000, 81])
    its.append(mcq("? ÷ 100 = 47", "4700", ["470", "47" + NB + "000", "4" + NB + "700" + NB + "000"],
                   "Use the inverse: 47 × 100. Write 2 zeros at the end: <b>4700</b>. Check: 4700 ÷ 100 = 47."))
    its.append(mcq("92" + NB + "000 ÷ ? = 92", "1000", ["100", "10", "10" + NB + "000"],
                   "92 000 became 92: the last 3 zeros were taken away, so every digit moved 3 places to the right. It is ÷ <b>1000</b>."))
    red_digit(its, 1380000, "÷", 2, 5, [300000, 30000, 300])
    p10(its, 600000, "÷", 3, [60, 6000, 60000])
    p10(its, 40040, "÷", 1, [4040, 404, 400400], "(Take away the 0 at the end, not the 0 in the middle.)")
    which_calc(its, 8050000, "÷", 3, ["8" + NB + "050" + NB + "000 ÷ 100", "8" + NB + "050" + NB + "000 ÷ 10" + NB + "000",
                                      "8" + NB + "050" + NB + "000 × 1000"])
    its.append(mcq("? ÷ 1000 = 305", N(305000), [N(30500), N(3050000), N(35000)],
                   "Use the inverse: 305 × 1000. Write 3 zeros at the end: <b>305 000</b>. Check: 305 000 ÷ 1000 = 305."))
    its.append(mcq("7200 ÷ ? = 720", "10", ["100", "1000", "10" + NB + "000"],
                   "7200 became 720: only the last zero was taken away, so every digit moved 1 place to the right. It is ÷ <b>10</b>."))
    its.append(mcq("How many hundreds are there in 45" + NB + "000?", "450", ["45", "4500", N(4500000)],
                   "The number of hundreds is 45 000 ÷ 100. Take away the last 2 zeros: <b>450</b> hundreds. "
                   "Check: 450 × 100 = 45 000."))
    its.append(mcq("Zhi Hao says 60" + NB + "300 ÷ 100 = 63. What is his mistake?",
                   "He took away the wrong 0; it is 603",
                   ["He should take away 1 zero: 6030", "He should take away 3 zeros: 60", "There is no mistake"],
                   "÷ 100 takes away the <b>last</b> 2 zeros of 60 300. The 0 in the middle stays: 60 300 ÷ 100 = <b>603</b>."))
    its.append(mcq("Which calculation has the answer 25?", "25" + NB + "000 ÷ 1000",
                   ["25" + NB + "000 ÷ 100", "2" + NB + "500" + NB + "000 ÷ 1000", "2" + NB + "500" + NB + "000 ÷ 100"],
                   "25 000 ÷ 1000 takes away 3 zeros: <b>25</b>. "
                   "25 000 ÷ 100 = 250, 2 500 000 ÷ 1000 = 2500 and 2 500 000 ÷ 100 = 25 000."))
    assert len(its) == 20, len(its)
    return {"title": "Divide by 10, 100 and 1000", "items": its}


# ============================================================ set 3: multiples of 10, 100, 1000
def set_multiples():
    its = []
    mul(its, 23, 30, [69, 6900, 53], "(69 forgets the × 10.)")
    mul(its, 12, 400, [480, 48000, 412])
    mul(its, 400, 30, [1200, 120000, 120], "(1200 has only 2 zeros, but 400 × 30 has 2 + 1 = 3 zeros.)")
    mul(its, 600, 50, [3000, 300000, 300], "(6 × 5 = 30 already ends in 0, so 30 000 has 4 zeros in all.)")
    div(its, 2400, 20, [24, 1200, 12], "(24 divides by 10 and then by 10 again, but 20 = 10 × 2, not 10 × 10.)")
    div(its, 3600, 300, [1200, 36, 120], "(1200 forgets the ÷ 100; 36 forgets the ÷ 3.)")
    mul(its, 156, 20, [312, 31200, 176])
    its.append(mcq(fig(steps("35", [("× 4", "140"), ("× 10", "?")], "35 times 4 is 140, then times 10 is ?")) +
                   "The diagram shows how to work out 35 × 40. What number goes in the last box?",
                   "1400", ["140", N(14000), "350"],
                   "40 = 4 × 10, so multiply by 4, then by 10. 35 × 4 = 140, and 140 × 10 = <b>1400</b>."))
    div(its, 7200, 80, [900, 9, 720], "(900 forgets the ÷ 10; 720 forgets the ÷ 8.)")
    mul(its, 2050, 30, [6150, 615000, 60150], "(60 150 multiplies the 50 by 3 instead of by 30.)")
    div(its, 48000, 600, [8, 800, 8000])
    mul(its, 500, 800, [40000, 4000000, 4000], "(5 × 8 = 40 has its own zero; count it too: 400 000.)")
    div(its, 9600, 400, [2400, 240, 38400], "(2400 forgets the ÷ 100.)")
    its.append(mcq("? × 30 = 2100", "70", ["700", "7", N(63000)],
                   "Use the inverse: 2100 ÷ 30. Divide by 10, then by 3: 2100 ÷ 10 = 210, 210 ÷ 3 = <b>70</b>. Check: 70 × 30 = 2100."))
    its.append(mcq(fig(steps("4500", [("÷ 10", "450"), ("÷ 5", "?")], "4500 divided by 10 is 450, then divided by 5 is ?")) +
                   "The diagram shows how to work out 4500 ÷ 50. What number goes in the last box?",
                   "90", ["900", "9", "45"],
                   "50 = 10 × 5, so divide by 10, then by 5. 4500 ÷ 10 = 450, and 450 ÷ 5 = <b>90</b>. "
                   "(45 divides by 10 and then by 10 again.)"))
    mul(its, 6000, 70, [42000, 4200000, 4200])
    div(its, 56000, 70, [80, 8000, 8])
    its.append(mcq("Which is the same as 500 × 60?", "5 × 6 × 1000", ["5 × 6 × 100", "5 × 6 × 10", "50 × 6 × 10"],
                   "500 = 5 × 100 and 60 = 6 × 10. So 500 × 60 = 5 × 6 × 100 × 10 = <b>5 × 6 × 1000</b> = 30 000."))
    its.append(mcq("Priya says 700 × 20 = 1400. What is her mistake?",
                   "She left out a zero; it is 14" + NB + "000",
                   ["She should write 1" + NB + "400" + NB + "000", "She should add them: 720", "There is no mistake"],
                   "700 × 20 = 7 × 2 × 1000. 7 × 2 = 14, so 700 × 20 = <b>14 000</b>. "
                   "Count the zeros: 2 in 700 and 1 in 20 make 3."))
    div(its, 3600000, 900, [400, 40000, 40])
    assert len(its) == 20, len(its)
    return {"title": "Multiply and divide by multiples of 10, 100 and 1000", "items": its}


# ============================================================ set 4: estimation
def rnd_to(x, p):
    return (x + p // 2) // p * p


def pl(p):
    return {10: "ten", 100: "hundred", 1000: "thousand"}[p]


def est_mul(its, a, pa, b, pb, wrong, note=""):
    ra, rb = rnd_to(a, pa), rnd_to(b, pb)
    if pa == pb:
        q = "Estimate the value of %s × %s by rounding each number to the nearest %s." % (N(a), N(b), pl(pa))
    else:
        q = ("Estimate the value of %s × %s by rounding %s to the nearest %s and %s to the nearest %s."
             % (N(a), N(b), N(a), pl(pa), N(b), pl(pb)))
    r = ra * rb
    e = ("%s ≈ %s and %s ≈ %s. %s × %s = %s." % (N(a), N(ra), N(b), N(rb), N(ra), N(rb), N(r)))
    a0, i = split10(ra)
    b0, j = split10(rb)
    e += " (%s × %s = %s, then write %s.)" % (a0, b0, a0 * b0, zeros(i + j))
    e = e.replace(" = %s." % N(r), " = <b>%s</b>." % N(r), 1)
    if note:
        e += " " + note
    its.append(mcq(q, N(r), [N(w) for w in wrong], e))


def est_div(its, a, pa, b, pb, wrong, note=""):
    ra, rb = rnd_to(a, pa), rnd_to(b, pb)
    assert ra % rb == 0, (a, b)
    q = ("Estimate the value of %s ÷ %s by rounding %s to the nearest %s and %s to the nearest %s."
         % (N(a), N(b), N(a), pl(pa), N(b), pl(pb)))
    e = "%s ≈ %s and %s ≈ %s. " % (N(a), N(ra), N(b), N(rb)) + div_e(ra, rb, note)
    its.append(mcq(q, N(ra // rb), [N(w) for w in wrong], e))


def set_estimate():
    its = []
    est_mul(its, 38, 10, 52, 10, [200, 20000, 1500], "(1500 rounds 38 down to 30, but 38 is nearer to 40.)")
    est_mul(its, 69, 10, 21, 10, [140, 14000, 1200])
    est_div(its, 618, 100, 19, 10, [3, 300, 60], "(60 divides by 10, not by 20.)")
    est_mul(its, 412, 100, 29, 10, [1200, 120000, 8000], "(8000 rounds 29 down to 20.)")
    its.append(mcq("Which is the best estimate for 79 × 32?", "80 × 30", ["70 × 30", "80 × 40", "70 × 40"],
                   "Round each number to the nearest ten: 79 ≈ 80 and 32 ≈ 30. So <b>80 × 30</b> = 2400. "
                   "The exact answer, 2528, is close to 2400."))
    est_div(its, 2385, 100, 61, 10, [4, 400, 240], "(240 divides by 10 only.)")
    est_mul(its, 587, 100, 42, 10, [2400, 240000, 20000], "(20 000 rounds 587 down to 500.)")
    est_mul(its, 47, 10, 615, 100, [3000, 300000, 24000], "(24 000 rounds 47 down to 40.)")
    est_div(its, 1210, 100, 39, 10, [3, 300, 40], "(40 is 1200 ÷ 30, but 39 rounds to 40, not 30.)")
    est_mul(its, 296, 100, 403, 100, [12000, 1200000, 1200])
    its.append(mcq("Which is the best estimate for 4830 ÷ 59?", "4800 ÷ 60", ["4800 ÷ 50", "4000 ÷ 60", "4830 ÷ 50"],
                   "Round 4830 to the nearest hundred (4800) and 59 to the nearest ten (60). "
                   "<b>4800 ÷ 60</b> = 480 ÷ 6 = 80."))
    est_mul(its, 704, 100, 58, 10, [4200, 420000, 35000], "(35 000 rounds 58 down to 50.)")
    est_div(its, 8940, 1000, 31, 10, [30, 3000, 900], "(900 divides by 10, not by 30.)")
    est_mul(its, 3106, 1000, 48, 10, [15000, 1500000, 120000], "(120 000 rounds 48 down to 40.)")
    est_mul(its, 19, 10, 3980, 1000, [8000, 800000, 60000], "(60 000 rounds 3980 down to 3000.)")
    est_div(its, 35840, 1000, 589, 100, [6, 600, 72], "(72 rounds 589 down to 500.)")
    assert 52 * 39 == 2028
    its.append(mcq("Jun Jie works out 52 × 39 = 2028. Which estimate shows that his answer is reasonable?",
                   "50 × 40 = 2000", ["50 × 40 = 200", "50 × 40 = 20" + NB + "000", "60 × 40 = 2400"],
                   "Round to the nearest ten: 52 ≈ 50 and 39 ≈ 40. 5 × 4 = 20, then write 2 zeros: <b>50 × 40 = 2000</b>. "
                   "2028 is close to 2000, so it is reasonable."))
    est_mul(its, 812, 100, 49, 10, [4000, 400000, 32000], "(32 000 rounds 49 down to 40.)")
    est_div(its, 9870, 1000, 52, 10, [20, 2000, 1000], "(1000 divides by 10, not by 50.)")
    assert 61 * 48 == 2928
    its.append(mcq("Ali works out 61 × 48 and gets 29" + NB + "280. Estimate to check. Which is correct?",
                   "About 3000, so it is not reasonable",
                   ["About 3000, so it is reasonable", "About 30" + NB + "000, so it is reasonable",
                    "About 300, so it is not reasonable"],
                   "61 ≈ 60 and 48 ≈ 50. 60 × 50 = <b>3000</b>. 29 280 is about 10 times too big, so Ali’s answer is "
                   "<b>not reasonable</b>. (The exact answer is 2928.)"))
    assert len(its) == 20, len(its)
    return {"title": "Estimate products and quotients", "items": its}


# ============================================================ set 5: word problems
def set_words():
    its = []

    def add(q, right, wrong, e):
        its.append(mcq(q, right, wrong, e))

    t = 20 * 45
    add(fig(bar_model(20, "45", "?", "20 buses", "20 units of 45, total unknown")) +
        "20 buses take the P5 pupils to Gardens by the Bay. Each bus carries 45 pupils. How many pupils are there?",
        N(t), ["90", N(9000), "65"],
        "20 units = 20 × 45. 45 × 2 = 90, and 90 × 10 = <b>%s</b>. There are %s pupils. (90 forgets the × 10.)" % (N(t), N(t)))
    add("Exercise books come in packs of 100. A school needs 3600 exercise books. How many packs does it need?",
        "36", ["360", N(360000), "3500"],
        "3600 ÷ 100: take away the last 2 zeros. The school needs <b>36</b> packs. Check: 36 × 100 = 3600.")
    add("The school prints 1000 copies of its magazine. Each copy has 36 pages. How many pages are printed?",
        N(36000), ["3600", N(360000), "1036"],
        "36 × 1000: write 3 zeros at the end. <b>36 000</b> pages are printed.")
    add(fig(bar_model(40, "$30", "?", "40 chairs", "40 units of 30 dollars, total unknown")) +
        "The school buys 40 chairs for the library. Each chair costs $30. How much do the chairs cost altogether?",
        D(1200), [D(120), D(12000), D(70)],
        "40 × $30 = 4 × 3 × 100 = 12 × 100. The chairs cost <b>$1200</b>. ($70 adds instead of multiplying.)")
    add(fig(bar_model(30, "40", "1200 pupils", "? classes", "1200 pupils in units of 40, number of units unknown")) +
        "There are 1200 pupils in a school. Each class has 40 pupils. How many classes are there?",
        "30", ["300", "3", N(48000)],
        "1200 ÷ 40: divide by 10, then by 4. 1200 ÷ 10 = 120, and 120 ÷ 4 = <b>30</b>. Check: 30 × 40 = 1200.")
    add("During Chinese New Year, Mdm Wong gives 30 red packets. She puts $20 in each red packet. "
        "How much money does she give altogether?",
        D(600), [D(60), D(6000), D(50)],
        "30 × $20 = 3 × 2 × 100 = <b>$600</b>. Count the zeros: 1 in 30 and 1 in 20 make 2.")
    add("A drinks stall orders 300 cartons of drinks. Each carton has 24 packets. How many packets are there?",
        "7200", ["720", N(72000), "324"],
        "24 × 300 = 24 × 3 × 100. 24 × 3 = 72, and 72 × 100 = <b>7200</b>. (324 adds instead of multiplying.)")
    add("The school hall has 50 rows of chairs for Speech Day. There are 40 chairs in each row. How many chairs are there?",
        "2000", ["200", N(20000), "90"],
        "50 × 40 = 5 × 4 × 100. 5 × 4 = 20, and 20 × 100 = <b>2000</b>. (200 forgets the zero in 20.)")
    add("Raju’s family saves $300 every month. How much do they save in 20 months?",
        D(6000), [D(600), D(60000), D(320)],
        "$300 × 20 = 3 × 2 × 1000 = <b>$6000</b>.")
    add(fig(bar_model(120, "50 kg", "6000 kg", "? bags", "6000 kg in units of 50 kg, number of units unknown")) +
        "A lorry carries 6000 kg of rice in bags of 50 kg. How many bags of rice are there?",
        "120", ["12", "1200", N(300000)],
        "6000 ÷ 50: divide by 10, then by 5. 6000 ÷ 10 = 600, and 600 ÷ 5 = <b>120</b> bags. Check: 120 × 50 = 6000.")
    add("A library puts 8400 books on 70 shelves. Each shelf has the same number of books. How many books are on each shelf?",
        "120", ["12", "1200", N(588000)],
        "8400 ÷ 70: divide by 10, then by 7. 8400 ÷ 10 = 840, and 840 ÷ 7 = <b>120</b>.")
    add("A bakery makes 2500 kaya buns a day. How many kaya buns does it make in 30 days?",
        N(75000), ["7500", N(750000), "2530"],
        "2500 × 30 = 25 × 3 × 1000. 25 × 3 = 75, and 75 × 1000 = <b>75 000</b>.")
    add("A printer prints 60 pages in 1 minute. How many minutes does it take to print 4800 pages?",
        "80", ["8", "800", N(288000)],
        "4800 ÷ 60: divide by 10, then by 6. 4800 ÷ 10 = 480, and 480 ÷ 6 = <b>80</b> minutes.")
    add("A stationery shop has 6000 erasers. It packs them in packets of 20. How many packets does it make?",
        "300", ["60", "3000", "30"],
        "20 = 10 × 2, so divide by 10, then by 2. 6000 ÷ 10 = 600, and 600 ÷ 2 = <b>300</b> packets. "
        "(60 divides by 10 and then by 10 again.)")
    add(fig(compare_model("Box A", 100, "Box B", "85", "Box A is 100 units, Box B is 1 unit of 85")) +
        "Box A has 100 times as many beads as Box B. Box B has 85 beads. How many beads are in Box A?",
        "8500", ["850", N(85000), "185"],
        "1 unit = 85, so 100 units = 85 × 100 = <b>8500</b>. Box A has 8500 beads. (185 adds 100.)")
    add(fig(bar_model(30, "?", "4200 cans", "30 days", "4200 cans in 30 equal units, one unit unknown")) +
        "Farah’s school collects 4200 cans for recycling in 30 days. It collects the same number of cans each day. "
        "How many cans does it collect each day?",
        "140", ["14", "1400", N(126000)],
        "30 units = 4200, so 1 unit = 4200 ÷ 30. 4200 ÷ 10 = 420, and 420 ÷ 3 = <b>140</b> cans.")
    add("Ethan runs 20 rounds of a 400 m track during Sports Day practice. How many metres does he run?",
        "8000 m", ["800 m", N(80000) + " m", "420 m"],
        "400 × 20 = 4 × 2 × 1000 = <b>8000 m</b>. (That is 8 km.)")
    add("19 buses take pupils to East Coast Park. Each bus carries 41 pupils. About how many pupils go? "
        "Round each number to the nearest ten.",
        "About 800", ["About 80", "About 8000", "About 600"],
        "19 ≈ 20 and 41 ≈ 40. 20 × 40 = 2 × 4 × 100 = <b>800</b>. About 800 pupils go. (The exact number is 779.)")
    assert 19 * 41 == 779
    tot, left = 20 * 30, 20 * 30 // 40
    assert left == 15
    add(fig(bar_model(40, "?", "600 markers", "40 classes", "600 markers in 40 equal units, one unit unknown")) +
        "A school buys 20 boxes of markers. Each box has 30 markers. The markers are shared equally among 40 classes. "
        "How many markers does each class get?",
        "15", ["600", "150", N(24000)],
        "Step 1: 20 × 30 = 600 markers. Step 2: 40 units = 600, so 1 unit = 600 ÷ 40. "
        "600 ÷ 10 = 60, and 60 ÷ 4 = <b>15</b>. (600 is the total, not one share.)")
    assert 400 - 30 * 12 == 40
    add("Mrs Lim buys 30 tickets for a school concert. Each ticket costs $12. She pays with $400. How much change does she get?",
        D(40), [D(360), D(364), D(440)],
        "Step 1: 30 × $12 = 12 × 3 × 10 = $360. Step 2: $400 %s $360 = <b>$40</b>. "
        "($360 is the cost, not the change. $364 uses 12 × 3 = 36 and forgets the × 10.)" % MINUS)
    assert len(its) == 20, len(its)
    return {"title": "Word problems with bar models", "items": its}


# ============================================================ lesson
def body_html():
    f1 = pv_move(406, "×", 2, CW=60)
    f2 = pv_move(70500, "÷", 2, CW=60)
    f3 = steps("400 × 30", [("4 × 3", "12"), ("× 1000", "12" + NB + "000")], "400 times 30: 4 times 3 is 12, then times 1000 is 12 000")
    f4 = steps("2400", [("÷ 10", "240"), ("÷ 2", "120")], "2400 divided by 20: divided by 10 is 240, then divided by 2 is 120")
    f5 = bar_model(20, "45", "?", "20 buses", "20 units of 45, total unknown")
    return (
        "<h2>Multiply by 10, 100 and 1000</h2>"
        "<p>When you multiply a whole number by 10, 100 or 1000, every digit moves to the <b>left</b>. "
        "When you divide, every digit moves to the <b>right</b>.</p>"
        + table(["Calculation", "Every digit moves", "Zeros"], [
            ["× 10 or ÷ 10", "1 place", "write or take away 1 zero"],
            ["× 100 or ÷ 100", "2 places", "write or take away 2 zeros"],
            ["× 1000 or ÷ 1000", "3 places", "write or take away 3 zeros"]])
        + "<figure class='sn-fig'>" + f1 +
        "<figcaption>406 × 100: the 4 moves from the hundreds to the ten thousands. The 0 in 406 moves too. "
        "The grey zeros fill the empty places. 406 × 100 = 40 600. "
        "(M = millions, HTh = hundred thousands, TTh = ten thousands, Th = thousands, H = hundreds, T = tens, O = ones.)"
        "</figcaption></figure>"
        "<h2>Divide by 10, 100 and 1000</h2>"
        "<figure class='sn-fig'>" + f2 +
        "<figcaption>70 500 ÷ 100: every digit moves 2 places to the right. The last 2 zeros go. "
        "The 0 between 7 and 5 stays, because it holds the tens place. 70 500 ÷ 100 = 705.</figcaption></figure>"
        + ex("Example", "5 200 000 ÷ 1000", "Every digit moves 3 places to the right. Take away the last 3 zeros.", "5200")
        + "<h2>Multiples of 10, 100 and 1000</h2>"
        "<p>Split the multiple into a basic fact and a power of 10: 30 = 3 × 10 and 400 = 4 × 100.</p>"
        "<figure class='sn-fig'>" + f3 +
        "<figcaption>400 × 30 = 4 × 3 × 100 × 10. Work out 4 × 3 = 12, then write 2 + 1 = 3 zeros: 12 000.</figcaption></figure>"
        "<figure class='sn-fig'>" + f4 +
        "<figcaption>2400 ÷ 20: 20 = 10 × 2, so divide by 10, then by 2. 2400 ÷ 20 = 120.</figcaption></figure>"
        + ex("Example", "500 × 800", "5 × 8 = 40. Then write 2 + 2 = 4 more zeros.", "400 000")
        + "<h2>Estimate first</h2>"
        "<p>Round each number, then use the rules above. 38 × 52 ≈ 40 × 50 = 2000. "
        "An estimate shows if an answer is reasonable.</p>"
        "<h2>Word problems: draw a model</h2>"
        "<figure class='sn-fig'>" + f5 +
        "<figcaption>20 buses carry 45 pupils each. 20 units = 20 × 45 = 45 × 2 × 10 = 900 pupils.</figcaption></figure>"
        + ex("Example", "1200 pupils are put into classes of 40. How many classes are there?",
             "1200 ÷ 40: 1200 ÷ 10 = 120, and 120 ÷ 4 = 30.", "30 classes")
        + "<h2>Common mistakes</h2>"
        + table(["Mistake", "What to do instead"], [
            ["2500 × 100 = 25 000 (1 zero written)", "× 100 writes 2 zeros: 250 000"],
            ["70 500 ÷ 100 = 75 (the wrong zero taken away)", "Take away the last zeros only: 705"],
            ["400 × 30 = 1200", "Count all the zeros: 2 + 1 = 3, so 12 000"],
            ["500 × 800 = 40 000", "5 × 8 = 40 has its own zero: 400 000"],
            ["2400 ÷ 20 = 24 (÷ 10, then ÷ 10 again)", "20 = 10 × 2: ÷ 10, then ÷ 2, so 120"],
        ])
    )


FAQ = [
    {"q": "How do you multiply and divide by 10, 100 and 1000 in P5?",
     "a": "Move every digit 1, 2 or 3 places: to the left to multiply and to the right to divide. For whole numbers, write or take away the same number of zeros at the end, so 406 × 100 = 40 600 and 70 500 ÷ 100 = 705."},
    {"q": "How do I explain 400 × 30 to my child?",
     "a": "Split each number into a basic fact and a power of 10: 400 × 30 = 4 × 3 × 1000. Work out 4 × 3 = 12, then write 3 zeros to get 12 000."},
    {"q": "What is the most common mistake?",
     "a": "Writing or taking away the wrong number of zeros, such as 400 × 30 = 1200 or 2400 ÷ 20 = 24. Count the zeros in both numbers, and remember that 20 is 10 × 2, not 10 × 10."},
    {"q": "Is this in the MOE syllabus?",
     "a": "Yes. Multiplying and dividing by 10, 100, 1000 and their multiples without a calculator is part of Whole Numbers in the MOE 2021 Primary 5 Mathematics syllabus. It is also needed for mental calculation and estimation in the PSLE."},
]


GROUP = re.compile(r"(?<=\d) (?=\d{3}(?!\d))")


def nbsp(o):
    """Typed spaces inside numbers (12 000) become no-break spaces everywhere in the unit."""
    if isinstance(o, str):
        parts = re.split(r"(<[^>]*>)", o)          # only text between tags, never SVG attributes
        parts = [x if x.startswith("<") else GROUP.sub(NB, x) for x in parts]
        for x in parts:
            assert x.startswith("<") or not re.search(r"\d \d", x), x
        return "".join(parts)
    if isinstance(o, list):
        return [nbsp(x) for x in o]
    if isinstance(o, dict):
        return {k: nbsp(v) for k, v in o.items()}
    return o


def mark_large(u, pattern):
    rx = re.compile(r"<svg (?=[^>]*aria-label='" + pattern + ")")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u


def check_answers(sets):
    """Re-check every plain '× / ÷' question."""
    rx = re.compile(r"^([\d" + NB + r"]+) ([×÷]) ([\d" + NB + r"]+) = \?$")
    n = 0
    for s in sets:
        for it in s["items"]:
            m = rx.match(it["q"])
            if m:
                a, op, b = I(m.group(1)), m.group(2), I(m.group(3))
                r = a * b if op == "×" else a // b
                assert op == "×" or a % b == 0
                assert val(it["c"][it["a"]])[0] == r, it["q"]
                n += 1
    return n


def gen():
    rnd = random.Random(65802)
    sets = [set_times(), set_divide(), set_multiples(), set_estimate(), set_words()]
    n = check_answers(sets)
    assert n >= 35, n
    balance(sets, rnd)
    seen = set()
    for s in sets:
        assert len(s["items"]) == 20, (s["title"], len(s["items"]))
        assert sorted(it["a"] for it in s["items"]) == sorted([0, 1, 2, 3] * 5)
        for it in s["items"]:
            assert len(set(it["c"])) == 4, it
            assert it["q"].count("<svg") <= 1
            k = re.sub(r"<[^>]+>", "", it["q"]) + "|" + "|".join(sorted(it["c"]))
            assert k not in seen, it["q"]
            seen.add(k)
    u = {
        "country": "sg", "subject": "maths", "grade": "primary-5", "slug": "multiplying-and-dividing-by-10-100-1000",
        "sort": 2, "updated": UPDATED, "pdf_url": "",
        "title": "Primary 5 Multiplying and Dividing by 10, 100 and 1000",
        "seo_title": "P5 Multiplying and Dividing by 10, 100 and 1000 Worksheets: Free Primary 5 Maths with Answers (MOE Syllabus)",
        "short_title": "× and ÷ by 10, 100 and 1000",
        "domain": "Number and Algebra",
        "standard_code": "Primary 5: Whole Numbers",
        "standard_url": "https://www.moe.gov.sg/primary/curriculum/syllabus",
        "standard_text": "Multiplying and dividing by 10, 100, 1000 and their multiples without calculator",
        "meta_desc": "Free P5 maths practice: multiply and divide by 10, 100, 1000 and their multiples, estimate, and solve word problems. 100 questions with answers.",
        "key_big": "× 10, 100, 1000 moves every digit 1, 2, 3 places left; ÷ moves them right.",
        "key_sub": "400 × 30 = 4 × 3 × 1000 = 12 000, and 2400 ÷ 20 = 240 ÷ 2 = 120.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }
    assert len(u["meta_desc"]) <= 160, len(u["meta_desc"])
    return nbsp(mark_large(u, "(place value chart|bar model|step diagram)"))


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
