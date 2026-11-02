# -*- coding: utf-8 -*-
"""
Singapore Primary 1 Maths: Numbers to 100
(MOE 2021 Primary Mathematics Syllabus, Standard, Primary 1: Whole Numbers —
 numbers up to 100: counting, place values (tens, ones), reading and writing in numerals and words,
 comparing and ordering, patterns)
  python3 tools/gen_sg_maths_p1_numbers.py
Counting objects in groups of ten (rows of 10, bundles of ice cream sticks, ten frames), tens and ones
(base ten blocks, tens and ones charts), numbers in words, comparing and ordering, and number patterns on a
hundred chart with simple Singapore word problems (money in $10 notes and $1 coins).
Very short sentences for 6-7 year olds and a picture in almost every question.
Wrong answers come from real mistakes: swapping the digits (43 -> 34), counting an object twice or missing
one (n + 1, n - 1), counting each group of ten as 1 (4 bundles and 3 sticks -> 7), writing each part
you hear (forty-three -> 403), teen / -ty words (fourteen / forty, seventeen / seventy), the spellings
"fourty" and "ninty", "fifty-ten" after fifty-nine, "after 39 comes 310", giving the digit instead of its
value (the 5 in 58 is 5), and moving across instead of down on a hundred chart (1 more instead of 10 more).
HTML attributes use single quotes (no backslashes in the JSON).
"""
import json, math, os, random, re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "sg", "maths", "primary-1")
UPDATED = "2026-11-03"
GREEN = "#006633"
FILL = "#cfe6d6"
CUBE = "#8fc7a0"
RED = "#c0392b"
INK = "#2b2b2b"
STICK = "#c9954c"
FONT = "Arial, Helvetica, sans-serif"


# ------------------------------------------------------------ helpers
def mcq(q, correct, wrong, e):
    """4 choices: correct + 3 wrong. Positions are set later by balance()."""
    correct = str(correct)
    wrong = [str(w) for w in wrong]
    assert len(wrong) == 3 and len(set(wrong + [correct])) == 4, (q, correct, wrong)
    assert ("<b>%s</b>" % correct) in e, (correct, e)
    return {"q": q, "c": [correct] + wrong, "a": 0, "e": e}


def mcq_n(q, correct, wrong, e):
    assert isinstance(correct, int) and 0 <= correct <= 100, (q, correct)
    assert all(isinstance(w, int) and 0 <= w <= 9999 and w != correct for w in wrong), (q, correct, wrong)
    assert len(set(wrong)) == 3, wrong
    return mcq(q, correct, wrong, e)


def fixed(q, labels, ans, e):
    """Choices are labels for parts of one picture (A, B ...). They keep this order."""
    assert ans in labels and len(labels) == 4 and len(set(labels)) == 4
    assert ("<b>%s</b>" % ans) in e, (ans, e)
    return {"q": q, "c": list(labels), "a": labels.index(ans), "e": e, "_fixed": True}


def balance(sets, rnd):
    """Each answer position (A to D) is correct 5 times in every set. Picture-label items keep their order."""
    for s in sets:
        targets = [0, 1, 2, 3] * 5
        for it in s["items"]:
            if it.get("_fixed"):
                targets.remove(it["a"])
        rnd.shuffle(targets)
        k = 0
        for it in s["items"]:
            if it.pop("_fixed", False):
                continue
            t = targets[k]
            k += 1
            c = it["c"]
            right = c[it["a"]]
            wrong = [x for i, x in enumerate(c) if i != it["a"]]
            rnd.shuffle(wrong)
            it["c"] = wrong[:t] + [right] + wrong[t:]
            it["a"] = t
        assert sorted(it["a"] for it in s["items"]) == sorted([0, 1, 2, 3] * 5), s["title"]


def fig(svg):
    return "<div class='qfig'>" + svg + "</div>"


def svg_wrap(w, h, body, label):
    return ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 %d %d' width='%d' height='%d' "
            "role='img' aria-label='%s'><g font-family='%s'>%s</g></svg>" % (w, h, w, h, label, FONT, body))


def text(x, y, t, fs=16, anchor="middle", col=INK):
    return ("<text x='%.1f' y='%.1f' font-size='%d' font-weight='700' fill='%s' text-anchor='%s'>%s</text>"
            % (x, y, fs, col, anchor, t))


def lst(xs):
    return ", ".join(str(x) for x in xs)


def unit(k, one, many):
    return "%d %s" % (k, one if k == 1 else many)


def T(k):
    return unit(k, "ten", "tens")


def O(k):
    return unit(k, "one", "ones")


def TO(t, o):
    return "%s and %s" % (T(t), O(o))


ONES = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten",
        "eleven", "twelve", "thirteen", "fourteen", "fifteen", "sixteen", "seventeen", "eighteen", "nineteen"]
TENS = ["", "", "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety"]


def words(n):
    assert 0 <= n <= 100
    if n == 100:
        return "one hundred"
    if n < 20:
        return ONES[n]
    return TENS[n // 10] + ("-" + ONES[n % 10] if n % 10 else "")


assert words(14) == "fourteen" and words(40) == "forty" and words(34) == "thirty-four" and words(90) == "ninety"


# ------------------------------------------------------------ pictures: objects
OS, OGAP, M = 26, 12, 6          # object cell, extra gap after 5 in a row, margin


def obj(kind, cx, cy):
    if kind == "apples":
        return ("<circle cx='%.1f' cy='%.1f' r='9' fill='#e05a4f' stroke='#9b2d24' stroke-width='1.2'/>"
                "<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='#6b4423' stroke-width='2' stroke-linecap='round'/>"
                "<ellipse cx='%.1f' cy='%.1f' rx='3.6' ry='2' fill='%s' transform='rotate(-30 %.1f %.1f)'/>"
                % (cx, cy + 2, cx, cy - 6, cx + 1, cy - 10, cx + 4.5, cy - 9, GREEN, cx + 4.5, cy - 9))
    if kind == "oranges":
        return ("<circle cx='%.1f' cy='%.1f' r='9.5' fill='#f39c34' stroke='#b0651a' stroke-width='1.2'/>"
                "<ellipse cx='%.1f' cy='%.1f' rx='4' ry='2' fill='%s' transform='rotate(-25 %.1f %.1f)'/>"
                % (cx, cy + 1.5, cx + 3, cy - 8, GREEN, cx + 3, cy - 8))
    if kind == "stars":
        pts = []
        for k in range(10):
            r = 10.5 if k % 2 == 0 else 4.6
            a = -math.pi / 2 + k * math.pi / 5
            pts.append("%.1f,%.1f" % (cx + r * math.cos(a), cy + 1 + r * math.sin(a)))
        return "<polygon points='%s' fill='#f4c430' stroke='#a57c00' stroke-width='1.2'/>" % " ".join(pts)
    if kind == "balls":
        return ("<circle cx='%.1f' cy='%.1f' r='9.5' fill='#5b9bd5' stroke='#2e5f8a' stroke-width='1.2'/>"
                "<path d='M %.1f %.1f Q %.1f %.1f %.1f %.1f' fill='none' stroke='#ffffff' stroke-width='1.6'/>"
                % (cx, cy, cx - 9, cy, cx, cy - 6, cx + 9, cy))
    if kind == "buttons":
        s = ["<circle cx='%.1f' cy='%.1f' r='9.5' fill='%s' stroke='%s' stroke-width='1.4'/>" % (cx, cy, FILL, GREEN)]
        for dx, dy in [(-2.6, -2.6), (2.6, -2.6), (-2.6, 2.6), (2.6, 2.6)]:
            s.append("<circle cx='%.1f' cy='%.1f' r='1.4' fill='%s'/>" % (cx + dx, cy + dy, GREEN))
        return "".join(s)
    if kind == "eggs":
        return ("<ellipse cx='%.1f' cy='%.1f' rx='7.5' ry='9.5' fill='#fbf3e4' stroke='#a0855b' stroke-width='1.3'/>"
                % (cx, cy))
    raise ValueError(kind)


def objects_svg(n, kind):
    """n objects in rows of 10. Each row has a small gap after 5, like a ten frame."""
    rows = [10] * (n // 10) + ([n % 10] if n % 10 else [])
    width = min(n, 10)
    W = 2 * M + width * OS + (OGAP if width > 5 else 0)
    H = 2 * M + len(rows) * OS
    s = []
    for r, k in enumerate(rows):
        for i in range(k):
            s.append(obj(kind, M + OS / 2 + i * OS + (OGAP if i >= 5 else 0), M + OS / 2 + r * OS))
    assert sum(rows) == n
    return svg_wrap(W, H, "".join(s), "%s in rows of 10" % kind)


# ------------------------------------------------------------ pictures: ten frames
TC = 22


def tenframes_svg(n, frames=None):
    """Ten frames with red counters. Each frame fills row by row before the next one starts.
    1-3 frames sit in one row; 4 frames as 2 + 2; 5 frames as 3 + 2."""
    frames = frames or max(1, (n + 9) // 10)
    assert 0 <= n <= 10 * frames <= 50
    per_row = frames if frames <= 3 else (2 if frames == 4 else 3)
    m, gx, gy = 4, 14, 12
    nrows = (frames + per_row - 1) // per_row
    W = 2 * m + per_row * 5 * TC + (per_row - 1) * gx
    H = 2 * m + nrows * 2 * TC + (nrows - 1) * gy
    s = []
    for f in range(frames):
        x0 = m + (f % per_row) * (5 * TC + gx)
        y0 = m + (f // per_row) * (2 * TC + gy)
        s.append("<rect x='%d' y='%d' width='%d' height='%d' fill='#ffffff' stroke='%s' stroke-width='2'/>"
                 % (x0, y0, 5 * TC, 2 * TC, GREEN))
        for i in range(1, 5):
            s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='1.2'/>"
                     % (x0 + i * TC, y0, x0 + i * TC, y0 + 2 * TC, GREEN))
        s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='1.2'/>"
                 % (x0, y0 + TC, x0 + 5 * TC, y0 + TC, GREEN))
        for k in range(10):
            if f * 10 + k < n:
                s.append("<circle cx='%.1f' cy='%.1f' r='7.5' fill='%s'/>"
                         % (x0 + (k % 5) * TC + TC / 2, y0 + (k // 5) * TC + TC / 2, RED))
    return svg_wrap(W, H, "".join(s), "ten frames with counters")


# ------------------------------------------------------------ pictures: base ten blocks
U = 9                      # a small cube is U x U, a rod is U x 10U (exactly 10 cubes)


def blocks_part(t, o, x0, y0):
    """Rods, then small cubes in columns of 5. Returns (elements, width, height). Groups sit on one base line."""
    F = 10 * U
    s = []
    rw = t * U + (t - 1) * 6 if t else 0
    cc = (o + 4) // 5
    cw = cc * U + (cc - 1) * 7 if o else 0
    ch = min(o, 5) * U + (min(o, 5) - 1) * 7 if o else 0
    hgt = F if t else ch
    for k in range(t):
        x = x0 + k * (U + 6)
        s.append("<rect x='%d' y='%d' width='%d' height='%d' fill='%s' stroke='%s' stroke-width='1.4'/>"
                 % (x, y0 + hgt - F, U, F, FILL, GREEN))
        for i in range(1, 10):
            s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='0.6'/>"
                     % (x, y0 + hgt - F + i * U, x + U, y0 + hgt - F + i * U, GREEN))
    cx0 = x0 + (rw + 18 if t else 0)
    for k in range(o):
        x = cx0 + (k // 5) * (U + 7)
        rows_here = min(5, o - (k // 5) * 5)
        top = y0 + hgt - (rows_here * U + (rows_here - 1) * 7)
        y = top + (k % 5) * (U + 7)
        s.append("<rect x='%d' y='%d' width='%d' height='%d' fill='%s' stroke='%s' stroke-width='1.4'/>"
                 % (x, y, U, U, CUBE, GREEN))
    w = rw + (18 if t and o else 0) + cw
    return s, w, hgt


def blocks_svg(t, o, labels=False):
    m = 8
    s, w, h = blocks_part(t, o, m, m)
    W = 2 * m + w
    H = 2 * m + h
    if labels:
        rw = t * U + (t - 1) * 6
        parts = []
        if t:
            parts.append((m + rw / 2, T(t)))
        if o:
            cc = (o + 4) // 5
            parts.append((m + (rw + 18 if t else 0) + (cc * U + (cc - 1) * 7) / 2, O(o)))
        need = max(len(lab) * 9 + 8 for _, lab in parts)
        if len(parts) == 2:
            gap_needed = need - (parts[1][0] - parts[0][0])
            if gap_needed > 0:
                s, w, h = blocks_part(t, o, m, m)
                s2, _, _ = blocks_part(0, o, m + rw + 18 + gap_needed, m)
                s = blocks_part(t, 0, m, m)[0] + s2
                w += gap_needed
                parts[1] = (parts[1][0] + gap_needed, parts[1][1])
        shift = max(0, need / 2 - parts[0][0] + 2)
        s = ["<g transform='translate(%.1f 0)'>%s</g>" % (shift, "".join(s))]
        right = max(cx + shift + (len(lab) * 9 + 8) / 2.0 for cx, lab in parts)
        W = int(max(2 * m + w + shift, right + 4) + 0.999)
        for cx, lab in parts:
            s.append(text(cx + shift, m + h + 22, lab, 15))
        H = m + h + 30
    return svg_wrap(W, H, "".join(s), "base ten blocks")


def pair_svg(a, b):
    """Two sets of base ten blocks, A and B, with a line between them."""
    m, gap = 8, 40
    sa, wa, ha = blocks_part(a // 10, a % 10, m, m)
    sb, wb, hb = blocks_part(b // 10, b % 10, m + wa + gap, m)
    h = max(ha, hb)
    if ha < h:
        sa, wa, ha = blocks_part(a // 10, a % 10, m, m + h - ha)
    if hb < h:
        sb, wb, hb = blocks_part(b // 10, b % 10, m + wa + gap, m + h - hb)
    W = 2 * m + wa + gap + wb
    s = sa + sb
    s.append("<line x1='%.1f' y1='%d' x2='%.1f' y2='%d' stroke='#bbbbbb' stroke-width='1.5'/>"
             % (m + wa + gap / 2, m, m + wa + gap / 2, m + h + 26))
    s.append(text(m + wa / 2, m + h + 24, "A", 18, col=GREEN))
    s.append(text(m + wa + gap + wb / 2, m + h + 24, "B", 18, col=GREEN))
    return svg_wrap(W, m + h + 32, "".join(s), "base ten blocks A and B")


CW, HEAD, ROW = 84, 32, 48


def chart_svg(n, hi=None):
    """Tens / ones chart. hi = 1 colours the tens digit red, 0 the ones digit."""
    x0 = y0 = 6
    W, H = 2 * x0 + 2 * CW, 2 * y0 + HEAD + ROW
    t, o = divmod(n, 10)
    assert t <= 9
    s = ["<rect x='%d' y='%d' width='%d' height='%d' fill='#ffffff' stroke='%s' stroke-width='2'/>"
         % (x0, y0, 2 * CW, HEAD + ROW, GREEN),
         "<rect x='%d' y='%d' width='%d' height='%d' fill='%s'/>" % (x0, y0, 2 * CW, HEAD, FILL)]
    for k, (lab, d, place) in enumerate([("Tens", t, 1), ("Ones", o, 0)]):
        x = x0 + k * CW
        if k:
            s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='1.5'/>"
                     % (x, y0, x, y0 + HEAD + ROW, GREEN))
        s.append(text(x + CW / 2, y0 + 22, lab, 16))
        s.append(text(x + CW / 2, y0 + HEAD + 35, str(d), 30, col=RED if hi == place else INK))
    s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='2'/>"
             % (x0, y0 + HEAD, x0 + 2 * CW, y0 + HEAD, GREEN))
    return svg_wrap(W, H, "".join(s), "tens and ones chart")


def sticks_svg(b, loose):
    """b bundles of 10 ice cream sticks (with a red rubber band) and loose single sticks.
    More than 5 bundles go on two rows, so the picture stays compact."""
    SW, SG, SH = 2.6, 3.0, 56
    BW = 9 * SG + SW
    BG = 9
    m = 8
    per = b if b <= 5 else (b + 1) // 2
    nrows = 1 if b <= 5 else 2
    s = []

    def bundle(x, y):
        out = []
        for j in range(10):
            out.append("<rect x='%.1f' y='%d' width='%.1f' height='%d' rx='1' fill='%s' stroke='%s' stroke-width='0.5'/>"
                       % (x + j * SG, y, SW, SH, STICK, "#8a6430"))
        out.append("<rect x='%.1f' y='%d' width='%.1f' height='7' fill='%s'/>" % (x - 1.5, y + SH / 2 - 3, BW + 3, RED))
        return out

    for k in range(b):
        r, c = divmod(k, per) if b else (0, 0)
        s += bundle(m + 1.5 + c * (BW + BG), m + r * (SH + 10))
    x = m + 1.5 + (per * (BW + BG) - BG if b else 0)
    if loose:
        x += 16 if b else 0
        y = m + (nrows - 1) * (SH + 10)
        for j in range(loose):
            s.append("<rect x='%.1f' y='%d' width='%.1f' height='%d' rx='1' fill='%s' stroke='%s' stroke-width='0.5'/>"
                     % (x + j * 9, y, SW, SH, STICK, "#8a6430"))
        x += (loose - 1) * 9 + SW
    W = int(x + 1.5 + m)
    H = 2 * m + nrows * SH + (nrows - 1) * 10
    return svg_wrap(W, H, "".join(s), "ice cream sticks in bundles of 10")


def packs_svg(t, o, kind):
    """t trays/packets, each with 10 things (2 rows of 5), and o loose things."""
    P = 15
    bw, bh = 5 * P + 8, 2 * P + 8
    m, g = 6, 8
    per = t if t <= 4 else (t + 1) // 2
    nrows = 1 if t <= 4 else 2
    s = []
    small = {"eggs": ("#fbf3e4", "#a0855b"), "stars": ("#f4c430", "#a57c00")}[kind]

    def dot(cx, cy):
        if kind == "eggs":
            return "<ellipse cx='%.1f' cy='%.1f' rx='5.2' ry='6.4' fill='%s' stroke='%s' stroke-width='1.1'/>" % (
                cx, cy, small[0], small[1])
        pts = []
        for k in range(10):
            r = 7 if k % 2 == 0 else 3
            a = -math.pi / 2 + k * math.pi / 5
            pts.append("%.1f,%.1f" % (cx + r * math.cos(a), cy + 0.6 + r * math.sin(a)))
        return "<polygon points='%s' fill='%s' stroke='%s' stroke-width='1'/>" % (" ".join(pts), small[0], small[1])

    for k in range(t):
        r, c = divmod(k, per)
        x, y = m + c * (bw + g), m + r * (bh + g)
        s.append("<rect x='%d' y='%d' width='%d' height='%d' rx='5' fill='%s' stroke='%s' stroke-width='1.6'/>"
                 % (x, y, bw, bh, FILL, GREEN))
        for j in range(10):
            s.append(dot(x + 4 + P / 2 + (j % 5) * P, y + 4 + P / 2 + (j // 5) * P))
    x = m + (per * (bw + g) - g if t else 0) + (18 if t and o else 0)
    y0 = m + (nrows - 1) * (bh + g)
    for j in range(o):
        s.append(dot(x + P / 2 + (j // 2) * P, y0 + 4 + P / 2 + (j % 2) * P))
    W = int(x + ((o + 1) // 2) * P + m) if o else int(x + m)
    H = 2 * m + nrows * bh + (nrows - 1) * g
    return svg_wrap(W, H, "".join(s), "packs of 10 %s" % kind)


def money_svg(notes, coins):
    """$10 notes (up to 4 in a row) and $1 coins (up to 5 in a row)."""
    NW, NH, NG = 74, 38, 8
    R, CG = 16, 6
    m = 6
    per = min(notes, 4)
    nrows = (notes + 3) // 4
    s = []
    for k in range(notes):
        r, c = divmod(k, 4)
        x, y = m + c * (NW + NG), m + r * (NH + NG)
        s.append("<rect x='%d' y='%d' width='%d' height='%d' rx='4' fill='#f6d3cc' stroke='#a5432f' stroke-width='1.6'/>"
                 % (x, y, NW, NH))
        s.append("<rect x='%d' y='%d' width='%d' height='%d' rx='2' fill='none' stroke='#a5432f' stroke-width='0.8'/>"
                 % (x + 4, y + 4, NW - 8, NH - 8))
        s.append(text(x + NW / 2, y + NH / 2 + 6, "$10", 17, col="#7a2a1c"))
    xs = m + (per * (NW + NG) - NG + 20 if notes else 0)
    cper = min(coins, 5)
    for k in range(coins):
        r, c = divmod(k, 5)
        cx, cy = xs + R + c * (2 * R + CG), m + R + 2 + r * (2 * R + CG)
        s.append("<circle cx='%d' cy='%d' r='%d' fill='#ecd27a' stroke='#9a7b1c' stroke-width='1.6'/>" % (cx, cy, R))
        s.append(text(cx, cy + 5, "$1", 14, col="#5c4a10"))
    W = (xs + cper * (2 * R + CG) - CG if coins else m + per * (NW + NG) - NG) + m
    crow = (coins + 4) // 5
    H = max(2 * m + nrows * NH + (nrows - 1) * NG, 2 * m + 4 + crow * 2 * R + (crow - 1) * CG)
    return svg_wrap(W, H, "".join(s), "money: notes and coins")


# ------------------------------------------------------------ pictures: cards, tracks, chart pieces
def card_svg(word, fs=22):
    """A big word or number card."""
    W = max(120, int(len(word) * fs * 0.62) + 36)
    H = 56
    s = ("<rect x='3' y='3' width='%d' height='%d' rx='8' fill='#ffffff' stroke='%s' stroke-width='2'/>"
         % (W - 6, H - 6, GREEN)) + text(W / 2, 36, word, fs)
    return svg_wrap(W, H, s, "card")


CWD, CHT = 54, 42


def cards_svg(vals):
    """Number cards in a row."""
    m, g = 4, 10
    W = 2 * m + len(vals) * CWD + (len(vals) - 1) * g
    H = 2 * m + CHT
    s = []
    for k, v in enumerate(vals):
        x = m + k * (CWD + g)
        s.append("<rect x='%d' y='%d' width='%d' height='%d' rx='6' fill='#ffffff' stroke='%s' stroke-width='2'/>"
                 % (x, m, CWD, CHT, GREEN))
        s.append(text(x + CWD / 2, m + 28, str(v), 20))
    return svg_wrap(W, H, "".join(s), "number cards")


NCW, NCH = 92, 60


def name_cards_svg(pairs):
    """Cards with a name on top and a number below."""
    m, g = 4, 8
    W = 2 * m + len(pairs) * NCW + (len(pairs) - 1) * g
    H = 2 * m + NCH
    s = []
    for k, (nm, v) in enumerate(pairs):
        x = m + k * (NCW + g)
        s.append("<rect x='%d' y='%d' width='%d' height='%d' rx='6' fill='#ffffff' stroke='%s' stroke-width='2'/>"
                 % (x, m, NCW, NCH, GREEN))
        s.append("<rect x='%d' y='%d' width='%d' height='22' rx='6' fill='%s'/>" % (x, m, NCW, FILL))
        s.append(text(x + NCW / 2, m + 16, nm, 14, col=GREEN))
        s.append(text(x + NCW / 2, m + 48, str(v), 20))
    return svg_wrap(W, H, "".join(s), "name cards with numbers")


TW, TH = 50, 38


def track_svg(vals):
    """A number track. A “?” box is shaded with a red ?."""
    m = 4
    W, H = 2 * m + len(vals) * TW, 2 * m + TH
    s = []
    for k, v in enumerate(vals):
        x = m + k * TW
        q = str(v) == "?"
        s.append("<rect x='%d' y='%d' width='%d' height='%d' fill='%s' stroke='%s' stroke-width='1.5'/>"
                 % (x, m, TW, TH, FILL if q else "#ffffff", GREEN))
        s.append(text(x + TW / 2, m + 26, str(v), 18, col=RED if q else INK))
    return svg_wrap(W, H, "".join(s), "number track")


HCW, HCH = 48, 34


def hchart_svg(tl, nrows, ncols, target, hide=(), shade=()):
    """A piece of the hundred chart. tl = top-left number. target (r, c) shows a red ?;
    hide = cells left out (not drawn), shade = cells coloured."""
    assert (tl - 1) % 10 + ncols <= 10, "piece must stay inside one row of the hundred chart"
    assert tl + 10 * (nrows - 1) + ncols - 1 <= 100
    m = 4
    W, H = 2 * m + ncols * HCW, 2 * m + nrows * HCH
    s = []
    for r in range(nrows):
        for c in range(ncols):
            if (r, c) in hide:
                continue
            x, y = m + c * HCW, m + r * HCH
            isT = (r, c) == target
            s.append("<rect x='%d' y='%d' width='%d' height='%d' fill='%s' stroke='%s' stroke-width='1.5'/>"
                     % (x, y, HCW, HCH, FILL if (isT or (r, c) in shade) else "#ffffff", GREEN))
            if isT:
                s.append(text(x + HCW / 2, y + 23, "?", 18, col=RED))
            else:
                s.append(text(x + HCW / 2, y + 23, str(tl + 10 * r + c), 16))
    return svg_wrap(W, H, "".join(s), "hundred chart piece")


def chart_val(tl, r, c):
    return tl + 10 * r + c


def bus_svg(n):
    """A public bus with its service number on the front panel."""
    W, H = 200, 96
    s = ("<rect x='6' y='8' width='188' height='66' rx='10' fill='#7fb98f' stroke='#2f6b40' stroke-width='2'/>"
         "<rect x='14' y='16' width='72' height='26' rx='4' fill='#2b2b2b'/>" +
         text(50, 36, str(n), 20, col="#f4c430") +
         "".join("<rect x='%d' y='16' width='24' height='26' rx='3' fill='#e9f3f8' stroke='#2f6b40' stroke-width='1'/>"
                 % x for x in (94, 124, 154)) +
         "<rect x='14' y='48' width='172' height='5' fill='#ffffff'/>"
         "<circle cx='46' cy='76' r='12' fill='#2b2b2b'/><circle cx='46' cy='76' r='4.5' fill='#bbbbbb'/>"
         "<circle cx='156' cy='76' r='12' fill='#2b2b2b'/><circle cx='156' cy='76' r='4.5' fill='#bbbbbb'/>")
    return svg_wrap(W, H, s, "bus with service number")


def numline_svg(lo, span=20, marks=None):
    """Number line lo to lo+span, a tick for every 1, numbers at every 5.
    marks = {value: letter} puts red letters above those ticks."""
    sp, m = 18, 18
    W = 2 * m + span * sp
    ly = 34
    H = ly + 30
    s = ["<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='2'/>" % (m - 8, ly, m + span * sp + 8, ly, INK)]
    for k in range(span + 1):
        x = m + k * sp
        big = (lo + k) % 5 == 0
        s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='%s'/>"
                 % (x, ly - (8 if big else 5), x, ly + (8 if big else 5), INK, "2" if big else "1.3"))
        if big:
            s.append(text(x, ly + 26, str(lo + k), 15))
    for v, lab in (marks or {}).items():
        x = m + (v - lo) * sp
        s.append("<circle cx='%d' cy='%d' r='4' fill='%s'/>" % (x, ly, RED))
        s.append(text(x, ly - 14, lab, 16, col=RED))
    return svg_wrap(W, H, "".join(s), "number line %d to %d" % (lo, lo + span))


# ------------------------------------------------------------ explanations
def count_e(n, what):
    t, o = divmod(n, 10)
    tens = lst(range(10, 10 * t + 1, 10))
    if n == 10:
        return "Touch each one once. A full row has 10. There are <b>10</b> %s." % what
    if t == 1 and o:
        return ("The full row has 10. Then count on: %s. There are <b>%d</b> %s."
                % (lst(range(11, n + 1)), n, what))
    if o == 0:
        return "Each full row has 10. Count the rows in tens: %s. There are <b>%d</b> %s." % (tens, n, what)
    return ("Each full row has 10. Count the rows in tens: %s. Then count on: %s. There are <b>%d</b> %s."
            % (tens, lst(range(10 * t + 1, n + 1)), n, what))


def sticks_e(t, o, what="sticks"):
    n = 10 * t + o
    e = "Each bundle has 10. Count the bundles in tens: %s." % lst(range(10, 10 * t + 1, 10))
    if o:
        e += " Then count on: %s." % lst(range(10 * t + 1, n + 1))
    return e + " There are <b>%d</b> %s." % (n, what)


def frames_e(n):
    t, o = divmod(n, 10)
    e = "Each full ten frame is 10. Count in tens: %s." % lst(range(10, 10 * t + 1, 10))
    if o:
        e += " Then count on: %s." % lst(range(10 * t + 1, n + 1))
    return e + " There are <b>%d</b> counters." % n


def blocks_e(t, o):
    n = 10 * t + o
    e = "Each rod is 10. Count the rods in tens: %s." % lst(range(10, 10 * t + 1, 10))
    if o:
        e += " Then count on the cubes: %s." % lst(range(10 * t + 1, n + 1))
    return e + " %s is <b>%d</b>." % (TO(t, o), n)


def swap(n):
    return (n % 10) * 10 + n // 10


# ============================================================ set 1: count in tens and ones
def set_count():
    k = {}
    for key, n, kind, wrong, extra in [
        ("o10", 10, "balls", [11, 9, 1], " 11 means one ball was counted twice. 1 counts the row as 1."),
        ("o14", 14, "stars", [41, 15, 4], " Write the 1 ten first: 14, not 41."),
        ("o20", 20, "apples", [2, 21, 19], " 2 tens is 20, not 2."),
        ("o23", 23, "buttons", [32, 24, 5], " 5 counts each row as 1. A full row is 10."),
        ("o31", 31, "balls", [13, 32, 4], " Write the tens first: 31, not 13."),
        ("o37", 37, "apples", [73, 38, 10], " 10 counts each full row as 1."),
    ]:
        k[key] = mcq_n(fig(objects_svg(n, kind)) + "How many %s are there?" % kind, n, wrong,
                       count_e(n, kind) + extra)
    for key, t, o, wrong, extra in [
        ("s30", 3, 0, [3, 31, 300], " 3 bundles are 3 tens. 3 tens is 30, not 3."),
        ("s43", 4, 3, [34, 7, 403], " 4 tens and 3 ones is 43, not 34. 7 counts each bundle as 1."),
        ("s28", 2, 8, [82, 10, 27], " 27 means one stick was missed."),
        ("s56", 5, 6, [65, 11, 57], " 57 means one stick was counted twice."),
        ("s70", 7, 0, [7, 17, 700], " 7 bundles are 7 tens: 70."),
        ("s69", 6, 9, [96, 15, 70], " Write the tens first: 6 tens and 9 ones is 69."),
        ("s94", 9, 4, [49, 13, 95], " 13 counts each bundle as 1."),
    ]:
        k[key] = mcq_n(fig(sticks_svg(t, o)) + "How many ice cream sticks are there?", 10 * t + o, wrong,
                       sticks_e(t, o) + extra)
    k["f35"] = mcq_n(fig(tenframes_svg(35)) + "How many counters are there?", 35, [53, 8, 36],
                     frames_e(35) + " 8 counts each full frame as 1.")
    k["f48"] = mcq_n(fig(tenframes_svg(48)) + "How many counters are there?", 48, [84, 12, 49],
                     frames_e(48) + " Write the tens first: 48, not 84.")
    k["twice"] = mcq_n(fig(objects_svg(26, "stars")) +
                       "Ali counts 27 stars. He counted one star twice. How many stars are there?",
                       26, [27, 28, 62],
                       "27 is 1 too many, because one star was counted two times. Touch each star once: "
                       "10, 20, then 21, 22, 23, 24, 25, 26. There are <b>26</b> stars.")
    k["s100"] = mcq_n(fig(sticks_svg(10, 0)) + "There are 10 bundles of 10 sticks. How many sticks are there?",
                      100, [10, 1000, 99],
                      "Count the bundles in tens: 10, 20, 30, 40, 50, 60, 70, 80, 90, 100. "
                      "10 tens make <b>100</b>. 10 is the number of bundles, not sticks.")
    k["groups"] = mcq_n(fig(sticks_svg(5, 0)) + "How many groups of 10 make 50?", 5, [50, 10, 6],
                        "Count in tens: 10, 20, 30, 40, 50. That is <b>5</b> groups of 10. 50 is the number of sticks.")
    k["more39"] = mcq_n(fig(sticks_svg(3, 9)) + "Add 1 more stick. How many sticks are there now?", 40,
                        [310, 49, 38],
                        "The picture shows 39. 1 more makes 10 loose sticks. 10 sticks make a new bundle. "
                        "Now there are 4 tens: <b>40</b>. Do not write 310. 49 adds 10, not 1.")
    assert 39 + 1 == 40 and 26 + 1 == 27 and 10 * 10 == 100 and 5 * 10 == 50
    order = ["o10", "o14", "o20", "o23", "s30", "o31", "s28", "f35", "s43", "o37", "twice", "groups",
             "s56", "f48", "s70", "s69", "more39", "s94", "s100"]
    assert set(order) == set(k), set(k) ^ set(order)
    return k, order


def set_count_full():
    k, order = set_count()
    # one more: count backward from a picture
    k["less"] = mcq_n(fig(objects_svg(30, "oranges")) + "Take away 1 orange. How many oranges are left?", 29,
                      [31, 20, 39],
                      "There are 3 rows of 10: 30 oranges. 1 less than 30 is <b>29</b>. Count back: 30, 29. "
                      "31 is 1 more. 20 is 10 less.")
    order.insert(13, "less")
    assert len(order) == 20 and set(order) == set(k)
    return {"title": "Count in tens and ones", "items": [k[x] for x in order]}


# ============================================================ set 2: tens and ones
def set_tens_ones():
    k = {}
    k["b25"] = mcq_n(fig(blocks_svg(2, 5)) + "What number do the blocks show?", 25, [52, 7, 205],
                     blocks_e(2, 5) + " 7 counts each rod as 1.")
    k["t41"] = mcq_n(fig(blocks_svg(4, 1)) + "How many tens are there?", 4, [1, 40, 5],
                     "Each rod is 1 ten. There are 4 rods, so there are <b>4</b> tens. The number is 41.")
    k["o36"] = mcq_n(fig(blocks_svg(3, 6)) + "How many ones are there?", 6, [3, 36, 60],
                     "Each small cube is 1 one. There are <b>6</b> cubes, so there are 6 ones. The number is 36.")
    k["b50"] = mcq_n(fig(blocks_svg(5, 0)) + "What number do the blocks show?", 50, [5, 15, 500],
                     "Count the rods in tens: 10, 20, 30, 40, 50. There are no ones, so write 0: <b>50</b>.")
    k["c43"] = mcq_n(fig(chart_svg(43)) + "What number does the chart show?", 43, [34, 7, 403],
                     "The tens digit is 4 and the ones digit is 3. Write the tens first: <b>43</b>. "
                     "Not 34, and not 403.")
    k["b62"] = mcq_n(fig(blocks_svg(6, 2)) + "6 tens and 2 ones = ☐", 62, [26, 8, 602],
                     "6 tens is 60. 2 more ones make 62. Write 6, then 2: <b>62</b>.")
    k["m47"] = mcq(fig(card_svg("47", 30)) + "Which is the same as 47?", "4 tens and 7 ones",
                   ["7 tens and 4 ones", "4 tens and 0 ones", "40 tens and 7 ones"],
                   "The 4 is in the tens place and the 7 is in the ones place. 47 is <b>4 tens and 7 ones</b>. "
                   "7 tens and 4 ones is 74.")
    k["v58"] = mcq_n(fig(chart_svg(58, hi=1)) + "What is the value of the red digit?", 50, [5, 8, 58],
                     "The red 5 is in the tens place. 5 tens is <b>50</b>. Its value is 50, not 5.")
    k["v73"] = mcq_n(fig(card_svg("73", 30)) + "What is the value of the digit 7?", 70, [7, 3, 73],
                     "73 is 7 tens and 3 ones. The 7 is in the tens place, so it is worth <b>70</b>.")
    k["d39"] = mcq_n(fig(card_svg("39", 30)) + "Which digit is in the ones place?", 9, [3, 90, 39],
                     "The ones digit is the last digit. 39 is 3 tens and 9 ones. The ones digit is <b>9</b>.")
    k["t80"] = mcq_n(fig(blocks_svg(8, 0)) + "80 = ☐ tens", 8, [80, 0, 18],
                     "Count the rods in tens: 10, 20 … 80. That is 8 rods. 80 = <b>8</b> tens.")
    k["e54"] = mcq_n(fig(blocks_svg(5, 4)) + "50 + 4 = ☐", 54, [45, 9, 504],
                     "50 is 5 tens. 4 is 4 ones. 5 tens and 4 ones is <b>54</b>. 504 writes each part you hear.")
    k["e76"] = mcq_n(fig(blocks_svg(7, 6)) + "70 + 6 = ☐", 76, [67, 13, 706],
                     "70 is 7 tens. 6 is 6 ones. 7 tens and 6 ones is <b>76</b>. 13 adds 7 and 6.")
    k["e35"] = mcq_n(fig(chart_svg(35)) + "35 = 30 + ☐", 5, [3, 50, 35],
                     "35 is 3 tens and 5 ones. 3 tens is 30. So 35 = 30 + <b>5</b>.")
    k["e91"] = mcq_n(fig(blocks_svg(9, 1)) + "91 = ☐ + 1", 90, [9, 91, 10],
                     "91 is 9 tens and 1 one. 9 tens is 90, not 9. So 91 = <b>90</b> + 1.")
    k["r82"] = mcq_n(fig(card_svg("2 ones and 8 tens", 18)) + "Which number is this?", 82, [28, 10, 802],
                     "Read it carefully. There are 8 tens and 2 ones. Write the tens first: <b>82</b>. "
                     "The ones were said first, but they go last.")
    k["ren33"] = mcq_n(fig(blocks_svg(2, 13)) + "What number do the blocks show?", 33, [213, 15, 23],
                       "There are 13 cubes. 10 cubes make 1 ten, so 13 ones = 1 ten and 3 ones. "
                       "2 tens and 1 ten make 3 tens. The number is <b>33</b>.")
    k["t100"] = mcq_n(fig(sticks_svg(10, 0)) + "100 = ☐ tens", 10, [100, 1, 0],
                      "Count in tens: 10, 20 … 100. That is 10 tens. 100 = <b>10</b> tens.")
    k["h55"] = mcq_n(fig(blocks_svg(4, 15)) + "Hui Min has 4 tens and 15 ones. What is her number?", 55,
                     [415, 19, 45],
                     "15 ones = 1 ten and 5 ones. 4 tens and 1 ten make 5 tens. 5 tens and 5 ones is <b>55</b>.")
    k["s64"] = mcq(fig(sticks_svg(6, 4)) + "Which is the same as 64?", "60 + 4",
                   ["6 + 4", "40 + 6", "600 + 4"],
                   "64 is 6 tens and 4 ones. 6 tens is 60. So 64 = <b>60 + 4</b>. 6 + 4 is only 10.")
    for n, t, o in [(25, 2, 5), (41, 4, 1), (36, 3, 6), (62, 6, 2), (54, 5, 4), (76, 7, 6), (91, 9, 1),
                    (82, 8, 2), (33, 3, 3), (55, 5, 5), (64, 6, 4)]:
        assert n == 10 * t + o
    assert 20 + 13 == 33 and 40 + 15 == 55 and 6 + 4 != 64 and 40 + 6 != 64 and 600 + 4 != 64
    order = ["b25", "t41", "o36", "b50", "c43", "b62", "d39", "m47", "v58", "t80", "e54", "e35",
             "v73", "e76", "e91", "s64", "r82", "t100", "ren33", "h55"]
    assert len(order) == 20 and set(order) == set(k)
    return {"title": "Tens and ones", "items": [k[x] for x in order]}


# ============================================================ set 3: numbers in words
def set_words():
    k = {}
    k["w34"] = mcq_n(fig(card_svg("thirty-four")) + "Write this number in numerals.", 34, [43, 304, 30],
                     "Thirty is 3 tens. Four is 4 ones. 3 tens and 4 ones is <b>34</b>. "
                     "Not 43, and not 304.")
    k["n26"] = mcq(fig(card_svg("26", 30)) + "Which is 26 in words?", "twenty-six",
                   ["sixty-two", "twenty", "sixteen"],
                   "26 is 2 tens and 6 ones. 2 tens is twenty. Say <b>twenty-six</b>. Sixty-two is 62.")
    k["w14"] = mcq_n(fig(card_svg("fourteen")) + "Write this number in numerals.", 14, [40, 41, 4],
                     "Fourteen is 1 ten and 4 ones: <b>14</b>. You hear the 4 first, but write the 1 first. "
                     "Forty is 40.")
    k["w40"] = mcq_n(fig(card_svg("forty")) + "Write this number in numerals.", 40, [14, 4, 400],
                     "Forty is 4 tens and 0 ones: <b>40</b>. Fourteen is 14.")
    k["n17"] = mcq(fig(card_svg("17", 30)) + "How do you say this number?", "seventeen",
                   ["seventy", "seven", "seventy-one"],
                   "17 is 1 ten and 7 ones. Say <b>seventeen</b>. Seventy is 70.")
    k["n70"] = mcq(fig(card_svg("70", 30)) + "How do you say this number?", "seventy",
                   ["seventeen", "seven", "seven hundred"],
                   "70 is 7 tens and 0 ones. Say <b>seventy</b>. Seventeen is 17.")
    k["w58"] = mcq_n(fig(card_svg("fifty-eight")) + "Write this number in numerals.", 58, [85, 508, 13],
                     "Fifty is 5 tens. Eight is 8 ones. 5 tens and 8 ones is <b>58</b>.")
    k["n91"] = mcq(fig(card_svg("91", 30)) + "Which is 91 in words?", "ninety-one",
                   ["nineteen", "ninety", "nine"],
                   "91 is 9 tens and 1 one. 9 tens is ninety. Say <b>ninety-one</b>. Nineteen is 19.")
    k["sp40"] = mcq(fig(card_svg("40", 30)) + "Which is the correct spelling?", "forty",
                    ["fourty", "fourteen", "four"],
                    "40 is spelt <b>forty</b>. There is no u in forty: f-o-r-t-y. Fourteen is 14.")
    k["sp90"] = mcq(fig(card_svg("90", 30)) + "Which is the correct spelling?", "ninety",
                    ["ninty", "nineteen", "nine"],
                    "90 is spelt <b>ninety</b>. Ninety keeps the e from nine: n-i-n-e-t-y.")
    k["c62"] = mcq(fig(chart_svg(62)) + "Write this number in words.", "sixty-two",
                   ["twenty-six", "sixty", "sixteen"],
                   "The chart shows 6 tens and 2 ones: 62. 6 tens is sixty. Say <b>sixty-two</b>.")
    k["t85"] = mcq_n(fig(card_svg("eighty-five")) + "How many tens are in this number?", 8, [5, 80, 85],
                     "Eighty-five is 85. Eighty is 8 tens. So there are <b>8</b> tens and 5 ones.")
    k["w100"] = mcq_n(fig(card_svg("one hundred")) + "Write this number in numerals.", 100, [1000, 10, 101],
                      "One hundred is 10 tens: <b>100</b>. It has a 1 and two zeros.")
    k["b30"] = mcq(fig(blocks_svg(3, 0)) + "Which word matches the blocks?", "thirty",
                   ["thirteen", "three", "thirty-one"],
                   "There are 3 rods: 3 tens. 3 tens is 30. Say <b>thirty</b>. Thirteen is 13.")
    k["b15"] = mcq(fig(blocks_svg(1, 5)) + "Which word matches the blocks?", "fifteen",
                   ["fifty", "five", "fifty-one"],
                   "There is 1 rod and 5 cubes: 1 ten and 5 ones. That is 15. Say <b>fifteen</b>. Fifty is 50.")
    k["w11"] = mcq_n(fig(card_svg("eleven")) + "Write this number in numerals.", 11, [110, 2, 12],
                     "Eleven is 1 ten and 1 one: <b>11</b>. Twelve is 12.")
    k["w63"] = mcq_n(fig(card_svg("sixty-three")) + "Siti writes this number as 603. What is the correct numeral?",
                     63, [603, 36, 6],
                     "Sixty-three is 6 tens and 3 ones. Write only 2 digits: <b>63</b>. "
                     "603 writes 60 and then 3.")
    k["next"] = mcq(fig(card_svg("fifty-eight, fifty-nine, ?", 18)) + "Which number word comes next?", "sixty",
                    ["fifty-ten", "sixty-nine", "fifty"],
                    "After 59 comes 60. 60 is 6 tens. Say <b>sixty</b>. There is no “fifty-ten”.")
    k["teen"] = mcq(fig(card_svg("thirteen or thirty?", 18)) + "Which number is greater?", "thirty",
                    ["thirteen", "They are the same", "You cannot tell"],
                    "Thirteen is 13. Thirty is 30. 30 is greater than 13, so <b>thirty</b> is greater.")
    k["f29"] = mcq(fig(tenframes_svg(29)) + "Which word matches the ten frames?", "twenty-nine",
                   ["ninety-two", "nineteen", "twenty-eight"],
                   "2 full frames are 20. The last frame has 9 counters. 20 and 9 make 29. "
                   "Say <b>twenty-nine</b>. Twenty-eight means one counter was missed.")
    order = ["w14", "w40", "n17", "n70", "n26", "w34", "sp40", "b30", "b15", "w58", "n91", "c62",
             "w11", "sp90", "t85", "f29", "w100", "teen", "w63", "next"]
    assert len(order) == 20 and set(order) == set(k)
    return {"title": "Numbers in words", "items": [k[x] for x in order]}


# ============================================================ set 4: compare and order
PAIRCH = ["A", "B", "They are the same", "You cannot tell"]


def set_compare():
    k = {}

    for key, vals, kind, e in [
        ("g54", [45, 54, 39, 50], "greatest",
         "Look at the tens first. 54 and 50 have 5 tens. 4 ones is more than 0 ones. <b>54</b> is the greatest. "
         "45 has the same digits, but only 4 tens."),
        ("s19", [28, 82, 19, 31], "smallest",
         "Look at the tens first. 19 has only 1 ten. <b>19</b> is the smallest, even though 9 is a big digit."),
        ("g88", [81, 88, 18, 80], "greatest",
         "81, 88 and 80 have 8 tens. Look at the ones: 8 is the most. <b>88</b> is the greatest."),
        ("s19b", [100, 99, 90, 19], "smallest",
         "19 has only 1 ten. 90 and 99 have 9 tens. 100 is 10 tens. <b>19</b> is the smallest."),
    ]:
        ans = max(vals) if kind == "greatest" else min(vals)
        k[key] = mcq_n(fig(cards_svg(vals)) + "Which number is the %s?" % kind, ans,
                       [v for v in vals if v != ans], e)
    k["gt60"] = mcq_n(fig(cards_svg([59, 16, 65, 6])) + "Which number is greater than 60?", 65, [59, 16, 6],
                      "65 has 6 tens and 5 ones. 60 has 6 tens and 0 ones. So <b>65</b> is greater than 60. "
                      "59 has only 5 tens.")
    k["lt40"] = mcq_n(fig(cards_svg([41, 38, 44, 40])) + "Which number is smaller than 40?", 38, [41, 44, 40],
                      "38 has only 3 tens. 40, 41 and 44 have 4 tens. So <b>38</b> is smaller than 40. "
                      "40 is equal to 40, not smaller.")
    k["p43"] = fixed(fig(pair_svg(43, 34)) + "Which blocks show the greater number?", PAIRCH, "A",
                     "A is 4 tens and 3 ones: 43. B is 3 tens and 4 ones: 34. 4 tens is more than 3 tens, "
                     "so <b>A</b> is greater.")
    k["p29"] = fixed(fig(pair_svg(29, 31)) + "Which blocks show the greater number?", PAIRCH, "B",
                     "A is 29. B is 31. 3 tens is more than 2 tens, so <b>B</b> is greater. "
                     "A has more pieces, but each rod is 10.")
    k["t47"] = mcq(fig(cards_svg([47, 74])) + "Which is true?", "47 is smaller than 74",
                   ["47 is greater than 74", "74 is smaller than 47", "47 is the same as 74"],
                   "47 has 4 tens. 74 has 7 tens. 4 tens is less than 7 tens. "
                   "So <b>47 is smaller than 74</b>.")
    k["nl62"] = mcq(fig(numline_svg(50, 20, {58: "A", 62: "B"})) + "A is 58. B is 62. Which is true?",
                    "62 is greater than 58",
                    ["58 is greater than 62", "62 is smaller than 58", "58 is the same as 62"],
                    "On a number line, numbers get bigger to the right. 62 is to the right of 58. "
                    "So <b>62 is greater than 58</b>.")
    k["m49"] = mcq_n(fig(track_svg([47, 48, 49, "?"])) + "What number is 1 more than 49?", 50, [410, 48, 59],
                     "1 more than 49: 9 ones and 1 one make 10 ones, which is a new ten. "
                     "So 49 + 1 is <b>50</b>. Do not write 410. 59 is 10 more.")
    k["l70"] = mcq_n(fig(track_svg(["?", 70, 71, 72])) + "What number is 1 less than 70?", 69, [71, 60, 79],
                     "1 less means count back 1: 70, <b>69</b>. 71 is 1 more. 60 is 10 less.")
    k["m36"] = mcq_n(fig(blocks_svg(3, 6)) + "What number is 10 more than 36?", 46, [37, 26, 136],
                     "10 more is 1 more rod. 3 tens become 4 tens. The ones stay the same: <b>46</b>. "
                     "37 is only 1 more. 26 is 10 less.")
    k["l82"] = mcq_n(fig(blocks_svg(8, 2)) + "What number is 10 less than 82?", 72, [81, 92, 71],
                     "10 less is 1 rod fewer. 8 tens become 7 tens. The ones stay the same: <b>72</b>. "
                     "81 is only 1 less. 92 is 10 more.")
    k["o3"] = mcq(fig(cards_svg([56, 65, 15])) + "Put the numbers in order. Begin with the smallest.",
                  "15, 56, 65", ["65, 56, 15", "56, 65, 15", "15, 65, 56"],
                  "15 has only 1 ten, so it is the smallest. 56 has 5 tens and 65 has 6 tens. "
                  "The order is <b>15, 56, 65</b>.")
    k["o3g"] = mcq(fig(cards_svg([39, 93, 63])) + "Put the numbers in order. Begin with the greatest.",
                   "93, 63, 39", ["39, 63, 93", "93, 39, 63", "63, 93, 39"],
                   "Look at the tens: 9 tens, 6 tens, 3 tens. The order is <b>93, 63, 39</b>.")
    k["btw"] = mcq_n(fig(numline_svg(60, 20)) + "Which number is between 67 and 71?", 69, [66, 72, 71],
                     "Count on from 67: 68, 69, 70, 71. <b>69</b> comes between them. "
                     "71 is the end, so it is not between.")
    k["o4"] = mcq(fig(cards_svg([72, 27, 70, 7])) + "Put the numbers in order. Begin with the smallest.",
                  "7, 27, 70, 72", ["27, 7, 70, 72", "72, 70, 27, 7", "7, 70, 27, 72"],
                  "7 has no tens. 27 has 2 tens. 70 and 72 have 7 tens, and 0 ones is less than 2 ones. "
                  "The order is <b>7, 27, 70, 72</b>.")
    k["dg85"] = mcq_n(fig(cards_svg([5, 8])) + "Use both digits once. What is the greatest number you can make?",
                      85, [58, 13, 80],
                      "Put the bigger digit in the tens place: 8 tens and 5 ones. That is <b>85</b>. "
                      "58 is smaller. 13 adds the digits.")
    k["dg60"] = mcq_n(fig(cards_svg([0, 6])) + "Use both digits once. Make a 2-digit number. What is it?",
                      60, [6, 66, 16],
                      "A 2-digit number cannot start with 0. So the 6 goes in the tens place: <b>60</b>. "
                      "06 is just 6.")
    for a, b in [(34, 43), (29, 31), (47, 74), (58, 62), (15, 56), (56, 65), (39, 63), (63, 93), (7, 27),
                 (27, 70), (70, 72), (67, 69), (69, 71)]:
        assert a < b
    assert 49 + 1 == 50 and 70 - 1 == 69 and 36 + 10 == 46 and 82 - 10 == 72
    order = ["g54", "s19", "gt60", "lt40", "p43", "t47", "m49", "l70", "g88", "nl62", "p29", "m36",
             "o3", "l82", "btw", "s19b", "o3g", "dg85", "o4", "dg60"]
    assert len(order) == 20 and set(order) == set(k)
    return {"title": "Compare and order", "items": [k[x] for x in order]}


# ============================================================ set 5: hundred chart patterns and word problems
def set_patterns():
    k = {}
    # hundred chart pieces
    tl = 23
    assert chart_val(tl, 0, 3) == 26
    k["h26"] = mcq_n(fig(hchart_svg(23, 1, 4, (0, 3))) + "This is part of a hundred chart. "
                     "What number goes in the red box?", 26, [27, 36, 25],
                     "Going right on a hundred chart adds 1: 23, 24, 25, <b>26</b>.")
    assert chart_val(34, 2, 0) == 54
    k["h54"] = mcq_n(fig(hchart_svg(34, 3, 1, (2, 0))) + "Going down adds 10. What number goes in the red box?",
                     54, [36, 64, 45],
                     "Each row down is 10 more: 34, 44, <b>54</b>. 36 adds 1 each time instead of 10.")
    assert chart_val(46, 1, 1) == 57
    k["h57"] = mcq_n(fig(hchart_svg(46, 2, 3, (1, 1))) + "What number goes in the red box?", 57,
                     [48, 67, 75],
                     "The box is below 47. 10 more than 47 is <b>57</b>. "
                     "75 swaps the digits.")
    assert chart_val(27, 1, 1) == 38
    k["h38"] = mcq_n(fig(hchart_svg(27, 3, 3, (1, 1), hide=((0, 0), (0, 2), (2, 0), (2, 2)))) +
                     "What number goes in the red box?", 38, [29, 83, 48],
                     "The box is below 28 and above 48. 28 + 10 = <b>38</b>. It is also 1 more than 37.")
    assert chart_val(97, 0, 3) == 100
    k["h100"] = mcq_n(fig(hchart_svg(97, 1, 4, (0, 3))) + "What number goes in the red box?", 100,
                      [910, 10, 101],
                      "After 99 comes <b>100</b>. 9 tens and 10 ones make 10 tens. Do not write 910.")
    assert chart_val(59, 1, 1) == 70
    k["h70"] = mcq_n(fig(hchart_svg(59, 2, 2, (1, 1))) + "What number goes in the red box?", 70,
                     [610, 80, 61],
                     "The box is after 69 and below 60. 60 + 10 = <b>70</b>. Do not write 610 after 69.")
    # counting patterns on a number track
    for key, seq, ans, wrong, e in [
        ("p42", [12, 22, 32], 42, [33, 40, 52],
         "Each number is 10 more. Only the tens digit goes up: 12, 22, 32, <b>42</b>."),
        ("p55", [85, 75, 65], 55, [64, 45, 56],
         "Each number is 10 less. Only the tens digit goes down: 85, 75, 65, <b>55</b>."),
        ("p46", [40, 42, 44], 46, [45, 48, 54],
         "Count on in twos: 40, 42, 44, <b>46</b>. 45 counts on in ones."),
        ("p80", [65, 70, 75], 80, [76, 85, 90],
         "Count on in fives: 65, 70, 75, <b>80</b>. 76 counts on in ones."),
    ]:
        step = seq[1] - seq[0]
        assert seq[2] - seq[1] == step and seq[2] + step == ans
        k[key] = mcq_n(fig(track_svg(seq + ["?"])) + "What number comes next?", ans, wrong, e)
    k["rule"] = mcq(fig(track_svg([31, 41, 51, 61])) + "What is the pattern?", "Count on in tens",
                    ["Count on in ones", "Count back in tens", "Count on in twos"],
                    "41 is 10 more than 31. 51 is 10 more than 41. The numbers get bigger by 10. "
                    "<b>Count on in tens</b>.")
    # word problems
    k["m34"] = mcq(fig(money_svg(3, 4)) + "Siti has this money. How much money does she have?", "$34",
                   ["$7", "$43", "$304"],
                   "Count the $10 notes in tens: $10, $20, $30. Then count on the $1 coins: $31, $32, $33, $34. "
                   "She has <b>$34</b>. $7 counts each note as $1.")
    k["m80"] = mcq(fig(money_svg(8, 0)) + "Hafiz has 8 $10 notes. How much money does he have?", "$80",
                   ["$8", "$18", "$800"],
                   "Count in tens: $10, $20, $30, $40, $50, $60, $70, $80. He has <b>$80</b>.")
    k["oranges"] = mcq_n(fig(objects_svg(46, "oranges")) +
                         "Mrs Lim puts mandarin oranges in rows of 10 for Chinese New Year. How many oranges are there?",
                         46, [64, 10, 45],
                         "There are 4 full rows: 10, 20, 30, 40. Then count on: 41, 42, 43, 44, 45, 46. "
                         "There are <b>46</b> oranges.")
    k["stamps"] = mcq(fig(name_cards_svg([("Ali", 52), ("Farah", 25)])) +
                      "Ali has 52 stamps. Farah has 25 stamps. Who has more stamps?", "Ali",
                      ["Farah", "They have the same", "You cannot tell"],
                      "52 has 5 tens. 25 has 2 tens. 52 is greater than 25, so <b>Ali</b> has more stamps.")
    k["bus"] = mcq_n(fig(bus_svg(76)) + "Ahmad takes this bus to school. How many tens are in the bus number?",
                     7, [6, 70, 76],
                     "The bus number is 76. 76 is 7 tens and 6 ones. There are <b>7</b> tens.")
    k["page"] = mcq_n(fig(track_svg([37, 38, 39, "?"])) +
                      "Kumar is on page 39 of a library book. He reads 1 more page. Which page is he on now?",
                      40, [310, 49, 30],
                      "1 more than 39 is <b>40</b>. After 39 comes a new ten. Do not write 310.")
    k["stickers"] = mcq_n(fig(packs_svg(7, 5, "stars")) +
                          "Ethan has 7 packets of 10 star stickers and 5 more stickers. How many stickers does he have?",
                          75, [57, 12, 705],
                          "Count the packets in tens: 10, 20 … 70. Then count on 5: 71, 72, 73, 74, 75. "
                          "He has <b>75</b> stickers. 12 counts each packet as 1.")
    k["eggs"] = mcq_n(fig(packs_svg(5, 2, "eggs")) +
                      "Mdm Wong buys 5 trays of 10 eggs and 2 more eggs. How many eggs does she buy?",
                      52, [25, 7, 502],
                      "5 trays of 10 is 5 tens: 50. 2 more eggs make <b>52</b>.")
    k["raju"] = mcq_n(fig(hchart_svg(27, 6, 1, None, shade=tuple((r, 0) for r in range(1, 6)))) +
                      "Raju counts on in tens from 27. He stops at 77. How many numbers does he say after 27?",
                      5, [50, 4, 6],
                      "He says 37, 47, 57, 67, 77. That is <b>5</b> numbers. Do not count 27, because he starts there.")
    assert 30 + 4 == 34 and 8 * 10 == 80 and 70 + 5 == 75 and 50 + 2 == 52 and (77 - 27) // 10 == 5
    order = ["h26", "p42", "h54", "p55", "h57", "p46", "rule", "h38", "p80", "h70", "h100",
             "m80", "m34", "bus", "stamps", "oranges", "page", "eggs", "stickers", "raju"]
    assert len(order) == 20 and set(order) == set(k)
    return {"title": "Hundred chart patterns and word problems", "items": [k[x] for x in order]}


# ------------------------------------------------------------ lesson
def ex(title, q, s, a):
    return ("<div class='sn-ex'><span class='sn-ex-t'>%s</span><p class='sn-ex-q'>%s</p>"
            "<p class='sn-ex-s'>%s</p><p class='sn-ex-a'>Answer: %s</p></div>" % (title, q, s, a))


def table(head, rows, cls="sn-table"):
    h = "".join("<th>%s</th>" % x for x in head)
    b = "".join("<tr>" + "".join("<td>%s</td>" % x for x in r) + "</tr>" for r in rows)
    return "<div class='sn-tw'><table class='%s'><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>" % (cls, h, b)


def body_html():
    return (
        "<h2>Count in groups of ten</h2>"
        "<p>Put things in groups of 10. Count the groups in tens: 10, 20, 30. "
        "Then count on the ones. Touch each thing <b>only once</b>.</p>"
        "<figure class='sn-fig'>" + sticks_svg(4, 3) +
        "<figcaption>4 bundles of 10 and 3 more sticks. Count 10, 20, 30, 40, then 41, 42, 43. "
        "There are 43 sticks.</figcaption></figure>"
        "<h2>Tens and ones</h2>"
        "<p>A 2-digit number has a <b>tens</b> digit and a <b>ones</b> digit. "
        "The tens digit comes first. 10 ones make 1 ten.</p>"
        "<figure class='sn-fig'>" + blocks_svg(4, 3, labels=True) +
        "<figcaption>4 tens and 3 ones is 43. A rod is 10. A small cube is 1.</figcaption></figure>"
        "<figure class='sn-fig'>" + chart_svg(43, hi=1) +
        "<figcaption>In 43 the digit 4 is in the tens place. Its value is 40.</figcaption></figure>" +
        ex("Tens and ones", "34 = ☐ tens and ☐ ones", "The first digit is the tens. The last digit is the ones.",
           "3 tens and 4 ones") +
        "<h2>Numbers in words</h2>" +
        table(["Number", "Word", "Number", "Word"], [
            ["14", "fourteen", "40", "forty"],
            ["15", "fifteen", "50", "fifty"],
            ["17", "seventeen", "70", "seventy"],
            ["19", "nineteen", "90", "ninety"],
            ["34", "thirty-four", "100", "one hundred"],
        ]) +
        "<p>A word ending in <b>-teen</b> is 1 ten and some ones. A word ending in <b>-ty</b>, like forty or ninety, is a number of tens. "
        "Forty has no u. Ninety keeps the e.</p>"
        "<h2>Compare and order</h2>"
        "<p>Look at the tens first. More tens means a greater number. "
        "If the tens are the same, look at the ones.</p>"
        "<figure class='sn-fig'>" + pair_svg(43, 34) +
        "<figcaption>A is 43. B is 34. 4 tens is more than 3 tens, so 43 is greater than 34.</figcaption></figure>" +
        ex("Which is greater?", "Which is greater, 58 or 62?", "58 has 5 tens. 62 has 6 tens.",
           "62 is greater than 58") +
        "<h2>Patterns on a hundred chart</h2>"
        "<p>On a hundred chart, going right adds 1. Going down adds 10. "
        "So the numbers in a column all end with the same digit.</p>"
        "<figure class='sn-fig'>" + hchart_svg(46, 2, 3, None, shade=((0, 1), (1, 1))) +
        "<figcaption>57 is below 47, so 57 is 10 more than 47. 57 is also 1 more than 56.</figcaption></figure>"
        "<h2>Common mistakes</h2>" +
        table(["Mistake", "What to do instead"], [
            ["Writing 34 for 43", "Write the tens first: 4 tens and 3 ones is 43"],
            ["Counting one thing twice", "Touch each thing once, or cross it off"],
            ["Counting a bundle of 10 as 1", "Count the bundles in tens: 10, 20, 30"],
            ["Mixing up fourteen and forty", "Fourteen is 14. Forty is 40"],
            ["Writing forty-three as 403", "Write only 2 digits: 43"],
            ["Writing 310 after 39", "After 39 comes a new ten: 40"],
        ])
    )


FAQ = [
    {"q": "What is taught in P1 numbers to 100?",
     "a": "Primary 1 students count to 100 in tens and ones, read and write numbers in numerals and in words, "
          "say how many tens and ones a number has, compare and order numbers, and find patterns on a hundred chart."},
    {"q": "How do I explain tens and ones to my child?",
     "a": "Bundle ice cream sticks or straws into groups of 10. Then 43 is 4 bundles and 3 loose sticks, "
          "so it is 4 tens and 3 ones."},
    {"q": "Why does my child write 34 for 43?",
     "a": "Children often write the digits in the order they notice them. Build the number with bundles first "
          "and say “tens first, then ones” as they write it."},
    {"q": "Is numbers to 100 in the MOE syllabus?",
     "a": "Yes. Numbers up to 100, including counting, tens and ones, numerals and words, comparing and ordering, "
          "and patterns, are part of Whole Numbers in the MOE 2021 Primary 1 Mathematics syllabus."},
]


def mark_large(u, pattern):
    """Tag wide pictures (rows of objects, bundles, ten frames, blocks, charts, money) so they print larger."""
    rx = re.compile(r"<svg (?=[^>]*aria-label='(?:" + pattern + ")')")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u


def gen_unit():
    rnd = random.Random(61801)
    sets = [set_count_full(), set_tens_ones(), set_words(), set_compare(), set_patterns()]
    balance(sets, rnd)
    seen = set()
    for s in sets:
        assert len(s["items"]) == 20, (s["title"], len(s["items"]))
        for it in s["items"]:
            assert len(set(it["c"])) == 4, it
            assert it["q"].count("<svg") <= 1
            key = re.sub(r"<[^>]+>", "", it["q"]) + "|" + it["q"] + "|" + "|".join(sorted(it["c"]))
            assert key not in seen, key
            seen.add(key)
    u = {
        "country": "sg", "subject": "maths", "grade": "primary-1", "slug": "numbers-to-100", "sort": 1,
        "updated": UPDATED, "pdf_url": "",
        "title": "Primary 1 Numbers to 100",
        "seo_title": "P1 Numbers to 100 Worksheets: Free Primary 1 Maths with Answers (MOE Syllabus)",
        "short_title": "Numbers to 100",
        "domain": "Number and Algebra",
        "standard_code": "Primary 1: Whole Numbers",
        "standard_url": "https://www.moe.gov.sg/primary/curriculum/syllabus",
        "standard_text": "Numbers up to 100: counting, place values (tens, ones), reading and writing in numerals "
                         "and words, comparing and ordering, patterns",
        "meta_desc": "Free P1 maths practice on numbers to 100: count in tens, tens and ones, number words, "
                     "comparing and hundred chart patterns. 100 questions with answers.",
        "key_big": "Write the tens first: 4 tens and 3 ones is 43, not 34.",
        "key_sub": "Thirty-four is 3 tens and 4 ones: 30 + 4 = 34.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }
    assert len(u["meta_desc"]) <= 160, len(u["meta_desc"])
    return mark_large(u, "[a-z]+ in rows of 10|ten frames with counters|base ten blocks|"
                         "number line [0-9]+ to [0-9]+|ice cream sticks in bundles of 10|number track|"
                         "name cards with numbers|number cards|packs of 10 [a-z]+|money: notes and coins|"
                         "bus with service number")


if __name__ == "__main__":
    u = gen_unit()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(u, f, ensure_ascii=False, indent=1)
    print("wrote", path)
