# -*- coding: utf-8 -*-
"""
CA Grade 1 Math: Numbers to 50 (Ontario Mathematics Curriculum 2020, Grade 1: B1.1, also B1.2, B1.3)
  python3 tools/gen_caon_math_g1_numbers.py
HTML attributes use single quotes (no backslashes in the JSON).
Grade 1: whole numbers to 50, very short sentences for 6-7 year olds, a picture in almost every question.
Canadian English (colour, centre, math, grade). Number words only to twenty.
Wrong answers come from real mistakes: swapping tens and ones (13 -> 31), counting an object twice or
missing one (n + 1, n - 1), reading tens as ones (3 rods and 4 cubes -> 7), writing "1 ten and 3 ones"
as 103, counting the empty boxes in a ten frame, teen / -ty words (fourteen -> 40 or 41),
"after 29 comes 210 or 20", a longer row looks like more, and more pieces looks like more.
"""
import json, math, os, random, re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "ca-on", "math", "grade-1")
UPDATED = "2026-11-02"
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
    assert 0 <= correct <= 50, (q, correct)
    assert all(isinstance(w, int) and 0 <= w <= 999 and w != correct for w in wrong), (q, correct, wrong)
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
TENS = ["", "", "twenty", "thirty", "forty", "fifty"]


def words(n):
    assert 0 <= n <= 50
    if n < 20:
        return ONES[n]
    return TENS[n // 10] + ("-" + ONES[n % 10] if n % 10 else "")


assert words(14) == "fourteen" and words(20) == "twenty" and words(31) == "thirty-one"


# ------------------------------------------------------------ pictures: objects
OS, OGAP, M = 26, 12, 6          # object cell, extra gap after 5 in a row, margin


def obj(kind, cx, cy):
    if kind == "apples":
        return ("<circle cx='%.1f' cy='%.1f' r='9' fill='#e05a4f' stroke='#9b2d24' stroke-width='1.2'/>"
                "<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='#6b4423' stroke-width='2' stroke-linecap='round'/>"
                "<ellipse cx='%.1f' cy='%.1f' rx='3.6' ry='2' fill='%s' transform='rotate(-30 %.1f %.1f)'/>"
                % (cx, cy + 2, cx, cy - 6, cx + 1, cy - 10, cx + 4.5, cy - 9, GREEN, cx + 4.5, cy - 9))
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
    if kind == "pucks":
        return ("<rect x='%.1f' y='%.1f' width='20' height='7' fill='#2b2b2b'/>"
                "<ellipse cx='%.1f' cy='%.1f' rx='10' ry='4' fill='#2b2b2b'/>"
                "<ellipse cx='%.1f' cy='%.1f' rx='10' ry='4' fill='#555555' stroke='#2b2b2b' stroke-width='1'/>"
                % (cx - 10, cy - 3, cx, cy + 4, cx, cy - 3))
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


def rows_svg(rows, kind):
    """Two labelled rows of objects. rows = [(label, count, spacing)]. Spacing can differ, so a longer row
    is not always the row with more."""
    lw, rh = 34, 34
    W = max(lw + 8 + n * sp for _, n, sp in rows) + 6
    H = 4 + len(rows) * rh + 4
    s = []
    for r, (lab, n, sp) in enumerate(rows):
        cy = 4 + r * rh + rh / 2
        s.append(text(lw / 2, cy + 6, lab, 18, col=GREEN))
        for i in range(n):
            s.append(obj(kind, lw + 8 + sp / 2 + i * sp, cy))
        if r:
            s.append("<line x1='4' y1='%.1f' x2='%d' y2='%.1f' stroke='#dddddd' stroke-width='1'/>"
                     % (4 + r * rh, W - 4, 4 + r * rh))
    return svg_wrap(W, H, "".join(s), "two rows of %s" % kind)


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
        F = 10 * U
        rw = t * U + (t - 1) * 6
        parts = []
        if t:
            parts.append((m + rw / 2, T(t)))
        if o:
            cc = (o + 4) // 5
            parts.append((m + (rw + 18 if t else 0) + (cc * U + (cc - 1) * 7) / 2, O(o)))
        # labels can be wider than the blocks: widen the picture so nothing is cut off
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
        W = int(2 * m + w + 2 * shift + 6)
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
    """b bundles of 10 craft sticks (with a red band) and loose single sticks."""
    SW, SG, SH = 2.6, 3.0, 64
    BW = 9 * SG + SW
    BG = 9
    y0 = 8
    s = []
    x = 8
    for k in range(b):
        for j in range(10):
            s.append("<rect x='%.1f' y='%d' width='%.1f' height='%d' rx='1' fill='%s' stroke='#8a6430' stroke-width='0.5'/>"
                     % (x + j * SG, y0, SW, SH, STICK))
        s.append("<rect x='%.1f' y='%d' width='%.1f' height='7' fill='%s'/>" % (x - 1.5, y0 + SH / 2 - 3, BW + 3, RED))
        x += BW + BG
    if loose:
        x += 8
        for j in range(loose):
            s.append("<rect x='%.1f' y='%d' width='%.1f' height='%d' rx='1' fill='%s' stroke='#8a6430' stroke-width='0.5'/>"
                     % (x + j * 9, y0, SW, SH, STICK))
        x += (loose - 1) * 9 + SW
    else:
        x -= BG
    return svg_wrap(int(x + 9), SH + 2 * y0, "".join(s), "craft sticks in bundles of 10")


# ------------------------------------------------------------ pictures: cards, tracks, signs
def card_svg(word, fs=22):
    """A big word or number card."""
    W = max(120, int(len(word) * fs * 0.62) + 36)
    H = 56
    s = ("<rect x='3' y='3' width='%d' height='%d' rx='8' fill='#ffffff' stroke='%s' stroke-width='2'/>"
         % (W - 6, H - 6, GREEN)) + text(W / 2, 36, word, fs)
    return svg_wrap(W, H, s, "card")


CWD, CHT = 54, 42


def cards_svg(vals):
    """Number cards in a row. A “?” card is shaded with a red ?."""
    m, g = 4, 10
    W = 2 * m + len(vals) * CWD + (len(vals) - 1) * g
    H = 2 * m + CHT
    s = []
    for k, v in enumerate(vals):
        x = m + k * (CWD + g)
        q = str(v) == "?"
        s.append("<rect x='%d' y='%d' width='%d' height='%d' rx='6' fill='%s' stroke='%s' stroke-width='2'/>"
                 % (x, m, CWD, CHT, FILL if q else "#ffffff", GREEN))
        s.append(text(x + CWD / 2, m + 28, str(v), 20, col=RED if q else INK))
    return svg_wrap(W, H, "".join(s), "number cards")


NCW, NCH = 84, 60


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


TW, TH = 46, 38


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


def jersey_svg(n):
    """A hockey jersey with a number on the front."""
    W, H = 130, 112
    body = ("M 30 8 L 50 8 Q 65 20 80 8 L 100 8 L 126 30 L 112 52 L 100 44 L 100 106 L 30 106 L 30 44 "
            "L 18 52 L 4 30 Z")
    s = ("<path d='%s' fill='#c0392b' stroke='#7a1f15' stroke-width='2'/>" % body +
         "<rect x='30' y='86' width='70' height='8' fill='#ffffff'/>" +
         "<path d='M 50 8 Q 65 22 80 8' fill='none' stroke='#ffffff' stroke-width='4'/>" +
         text(65, 72, str(n), 34, col="#ffffff"))
    return svg_wrap(W, H, s, "hockey jersey")


def door_svg(n):
    """A classroom door with a room number sign."""
    W, H = 110, 120
    s = ("<rect x='20' y='6' width='70' height='110' rx='3' fill='#d9b38c' stroke='#7a5530' stroke-width='2'/>"
         "<rect x='28' y='16' width='54' height='34' rx='4' fill='#ffffff' stroke='%s' stroke-width='2'/>" % GREEN +
         text(55, 31, "Room", 14, col=GREEN) + text(55, 46, str(n), 16) +
         "<circle cx='80' cy='70' r='4' fill='#7a5530'/>")
    return svg_wrap(W, H, s, "classroom door")


# ------------------------------------------------------------ pictures: number lines
NL_SP = 18


def numline_svg(lo, v, span=20, marks=None):
    """Number line lo to lo+span, a tick for every 1, numbers at every 5. A red arrow points at v.
    marks = {value: letter} puts red letters above those ticks instead."""
    m = 18
    W = 2 * m + span * NL_SP
    ly = 34
    H = ly + 30
    s = ["<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='2'/>" % (m - 8, ly, m + span * NL_SP + 8, ly, INK)]
    for k in range(span + 1):
        x = m + k * NL_SP
        big = (lo + k) % 5 == 0
        s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='%s'/>"
                 % (x, ly - (8 if big else 5), x, ly + (8 if big else 5), INK, "2" if big else "1.3"))
        if big:
            s.append(text(x, ly + 26, str(lo + k), 15))
    if v is not None:
        x = m + (v - lo) * NL_SP
        s.append("<line x1='%d' y1='4' x2='%d' y2='%d' stroke='%s' stroke-width='2.5'/>" % (x, x, ly - 12, RED))
        s.append("<polygon points='%d,%d %d,%d %d,%d' fill='%s'/>" % (x - 6, ly - 16, x + 6, ly - 16, x, ly - 9, RED))
    for val, lab in (marks or {}).items():
        x = m + (val - lo) * NL_SP
        s.append("<circle cx='%d' cy='%d' r='4' fill='%s'/>" % (x, ly, RED))
        s.append(text(x, ly - 14, lab, 16, col=RED))
    return svg_wrap(W, H, "".join(s), "number line %d to %d" % (lo, lo + span))


def numline50_svg(v):
    """Number line 0 to 50 with a tick every 5 and numbers every 10. A red arrow points at v."""
    m, sp = 20, 9
    W = 2 * m + 50 * sp
    ly = 34
    H = ly + 30
    s = ["<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='2'/>" % (m - 8, ly, m + 50 * sp + 8, ly, INK)]
    for k in range(0, 51, 5):
        x = m + k * sp
        big = k % 10 == 0
        s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='%s'/>"
                 % (x, ly - (9 if big else 6), x, ly + (9 if big else 6), INK, "2" if big else "1.5"))
        if big:
            s.append(text(x, ly + 26, str(k), 15))
    x = m + v * sp
    s.append("<line x1='%d' y1='4' x2='%d' y2='%d' stroke='%s' stroke-width='2.5'/>" % (x, x, ly - 12, RED))
    s.append("<polygon points='%d,%d %d,%d %d,%d' fill='%s'/>" % (x - 6, ly - 16, x + 6, ly - 16, x, ly - 9, RED))
    return svg_wrap(W, H, "".join(s), "number line 0 to 50")


# ------------------------------------------------------------ explanations
def count_e(n, what):
    t, o = divmod(n, 10)
    if n <= 10:
        if n > 5:
            return ("The first 5 make a group. Count on: %s. Touch each one only once. There are <b>%d</b> %s."
                    % (lst(range(6, n + 1)), n, what))
        return "Touch each one once: %s. There are <b>%d</b> %s." % (lst(range(1, n + 1)), n, what)
    tens = lst(range(10, 10 * t + 1, 10))
    if o == 0:
        return "Each full row has 10. Count the rows by tens: %s. There are <b>%d</b> %s." % (tens, n, what)
    return ("Each full row has 10. Count the rows by tens: %s. Then count on: %s. There are <b>%d</b> %s."
            % (tens, lst(range(10 * t + 1, n + 1)), n, what))


def frames_e(n):
    t, o = divmod(n, 10)
    if t == 0:
        e = "Count the counters, not the empty boxes. The top row has %d. " % min(n, 5)
        if n > 5:
            e += "Count on: %s. " % lst(range(6, n + 1))
        return e + "There are <b>%d</b> counters." % n
    e = "Each full ten frame is 10. Count by tens: %s." % lst(range(10, 10 * t + 1, 10))
    if o:
        e += " Then count on: %s." % lst(range(10 * t + 1, n + 1))
    return e + " There are <b>%d</b> counters." % n


def blocks_e(t, o):
    n = 10 * t + o
    if t == 0:
        return "There are no rods. Count the cubes: <b>%d</b>." % n
    e = "Each rod is 10. Count the rods by tens: %s." % lst(range(10, 10 * t + 1, 10))
    if o:
        e += " Then count on the cubes: %s." % lst(range(10 * t + 1, n + 1))
    return e + " %s is <b>%d</b>." % (TO(t, o), n)


# ============================================================ set 1: count objects and ten frames
def set_count():
    k = {}
    for key, n, kind, wrong in [
        ("o6", 6, "apples", [7, 5, 8]),
        ("o9", 9, "stars", [10, 8, 4]),
        ("o12", 12, "balls", [21, 13, 11]),
        ("o15", 15, "apples", [51, 16, 14]),
        ("o11", 11, "buttons", [12, 10, 2]),
        ("o18", 18, "pucks", [81, 19, 17]),
        ("o23", 23, "balls", [32, 13, 22]),
        ("o27", 27, "stars", [72, 17, 28]),
    ]:
        e = count_e(n, kind)
        if n == 6:
            e += " 7 or 8 means an apple was counted twice."
        if n == 9:
            e += " 4 counts only the stars after the group of 5."
        if n == 11:
            e += " Do not write 2. The first row is 1 ten, not 1."
        if n > 11 and n % 10:
            e += " Write the tens first: %d, not %d." % (n, (n % 10) * 10 + n // 10)
        k[key] = mcq(fig(objects_svg(n, kind)) + "How many %s?" % kind, n, wrong, e)
    for key, n, wrong in [("f7", 7, [8, 6, 3]), ("f9", 9, [10, 8, 1])]:
        e = frames_e(n) + " %d is the number of empty boxes." % (10 - n)
        k[key] = mcq(fig(tenframes_svg(n)) + "How many counters are in the ten frame?", n, wrong, e)
    for key, n, wrong in [("f14", 14, [41, 15, 5]), ("f17", 17, [71, 16, 8]), ("f26", 26, [62, 25, 8]),
                          ("f32", 32, [23, 31, 5])]:
        e = frames_e(n)
        e += " A full frame is 1 ten, not 1 counter."
        k[key] = mcq(fig(tenframes_svg(n)) + "How many counters are there?", n, wrong, e)
    k["f20"] = mcq(fig(tenframes_svg(20)) + "How many counters are there?", 20, [2, 10, 21],
                   "Both ten frames are full. Count by tens: 10, 20. There are <b>20</b> counters. "
                   "2 tens is 20, not 2.")
    k["f30"] = mcq(fig(tenframes_svg(30)) + "How many counters are there?", 30, [3, 20, 31],
                   "All 3 ten frames are full. Count by tens: 10, 20, 30. There are <b>30</b> counters.")
    k["m6"] = mcq(fig(tenframes_svg(6)) + "How many more counters make 10?", 4, [6, 5, 3],
                  "Count the empty boxes: there are 4. 6 and <b>4</b> make 10. 6 is how many counters there are now.")
    k["m3"] = mcq(fig(tenframes_svg(3)) + "How many more counters make 10?", 7, [3, 6, 8],
                  "Count the empty boxes: there are 7. 3 and <b>7</b> make 10.")
    k["m13"] = mcq(fig(tenframes_svg(13)) + "How many more counters make 20?", 7, [3, 13, 6],
                   "The first frame is full. The second frame has 3 counters and 7 empty boxes. "
                   "13 and <b>7</b> make 20.")
    k["m15"] = mcq(fig(tenframes_svg(15)) + "How many more counters make 20?", 5, [15, 4, 6],
                   "The second frame has 5 counters and 5 empty boxes. 15 and <b>5</b> make 20.")
    assert 6 + 4 == 10 and 3 + 7 == 10 and 13 + 7 == 20 and 15 + 5 == 20
    order = ["o6", "f7", "o9", "m6", "f9", "m3", "o11", "o12", "f14", "o15", "f17", "o18", "m13", "f20",
             "m15", "o23", "f26", "o27", "f30", "f32"]
    assert len(order) == 20 and set(order) == set(k)
    return {"title": "Count objects and ten frames", "items": [k[x] for x in order]}


# ============================================================ set 2: tens and ones with rods and cubes
def set_blocks():
    k = {}
    for key, t, o, wrong in [("b13", 1, 3, [31, 4, 103]), ("b25", 2, 5, [52, 7, 205]),
                             ("b31", 3, 1, [13, 4, 301]), ("b47", 4, 7, [74, 11, 407])]:
        n = 10 * t + o
        e = blocks_e(t, o) + " Write the tens first, then the ones: %d, not %d or %d." % (n, wrong[0], wrong[2])
        k[key] = mcq_n(fig(blocks_svg(t, o)) + "What number do the blocks show?", n, wrong, e)
    k["b40"] = mcq_n(fig(blocks_svg(4, 0)) + "What number do the blocks show?", 40, [4, 400, 30],
                     "Each rod is 10. Count by tens: 10, 20, 30, 40. There are no cubes, so write 0 ones: <b>40</b>.")
    k["t26"] = mcq_n(fig(blocks_svg(2, 6)) + "How many tens are there?", 2, [6, 20, 26],
                     "Each rod is 1 ten. There are 2 rods. So there are <b>2</b> tens. The number is 26.")
    k["o34"] = mcq_n(fig(blocks_svg(3, 4)) + "How many ones are there?", 4, [3, 7, 34],
                     "Each small cube is 1 one. There are 4 cubes. So there are <b>4</b> ones. The number is 34.")
    k["m28"] = mcq(fig(blocks_svg(2, 8)) + "Which matches the blocks?", TO(2, 8), [TO(8, 2), TO(2, 7), TO(3, 8)],
                   "Count the rods: 2 tens. Count the cubes: 8 ones. That is <b>%s</b>: 28." % TO(2, 8))
    k["n36"] = mcq_n(fig(blocks_svg(3, 6)) + "3 tens and 6 ones. What number is it?", 36, [63, 9, 306],
                     "3 tens is 30. 6 more ones make <b>36</b>. 3 + 6 = 9 adds the digits, not the tens and ones.")
    k["n42"] = mcq_n(fig(chart_svg(42)) + "What number is 4 tens and 2 ones?", 42, [24, 6, 402],
                     "Write the tens digit first: 4. Then the ones digit: 2. The number is <b>42</b>.")
    k["fr27"] = mcq(fig(tenframes_svg(27)) + "Which matches the ten frames?", TO(2, 7),
                    [TO(7, 2), TO(2, 3), TO(1, 7)],
                    "2 frames are full: 2 tens. The last frame has 7 counters: 7 ones. That is <b>%s</b>. "
                    "3 is the number of empty boxes." % TO(2, 7))
    k["p35"] = mcq_n(fig(blocks_svg(3, 5)) + "35 = 30 + ☐", 5, [3, 50, 35],
                     "35 is 3 tens and 5 ones. The tens make 30. The ones make 5. So 35 = 30 + <b>5</b>.")
    k["p28"] = mcq_n(fig(blocks_svg(2, 8)) + "28 = ☐ + 8", 20, [2, 28, 80],
                     "28 is 2 tens and 8 ones. 2 tens is 20, not 2. So 28 = <b>20</b> + 8.")
    k["h40"] = mcq_n(fig(sticks_svg(4, 0)) + "How many tens are in 40?", 4, [40, 0, 10],
                     "There are 4 bundles of 10 sticks: 10, 20, 30, 40. So 40 has <b>4</b> tens and 0 ones.")
    k["r23"] = mcq_n(fig(blocks_svg(2, 3)) + "Add 1 more rod. What number is it now?", 33, [24, 23, 43],
                     "The blocks show 23. A rod is 10, not 1. 23 and 10 more is <b>33</b>. "
                     "Only the tens digit changes.")
    k["c19"] = mcq_n(fig(blocks_svg(1, 9)) + "Add 1 more cube. What number is it now?", 20, [110, 29, 19],
                     "The blocks show 19. 1 more cube makes 10 cubes. 10 cubes make 1 more ten. "
                     "Now there are 2 tens and 0 ones: <b>20</b>. Do not write 110.")
    k["b24"] = mcq_n(fig(blocks_svg(1, 14)) + "What number do the blocks show?", 24, [114, 15, 14],
                     "1 rod is 10. There are 14 cubes. 10 cubes make 1 more ten, so 14 cubes are 1 ten and 4 ones. "
                     "That is 2 tens and 4 ones: <b>24</b>.")
    k["w32"] = mcq(fig(blocks_svg(3, 2)) + "Which is another way to make 32?", TO(2, 12),
                   [TO(2, 2), TO(3, 12), TO(2, 3)],
                   "Break 1 rod into 10 cubes. 3 tens and 2 ones become 2 tens and 12 ones. "
                   "20 and 12 make 32. The answer is <b>%s</b>." % TO(2, 12))
    assert 20 + 12 == 32 and 20 + 2 != 32 and 30 + 12 != 32 and 20 + 3 != 32
    k["has50"] = mcq_n(fig(sticks_svg(5, 0)) + "5 bundles of 10 sticks. How many sticks?", 50, [5, 500, 40],
                       "Count by tens: 10, 20, 30, 40, 50. 5 tens and 0 ones is <b>50</b>.")
    k["has19"] = mcq_n("Which number has 1 ten and 9 ones?", 19, [91, 10, 109],
                       "Write the tens digit first: 1. Then the ones: 9. The number is <b>19</b>. "
                       "91 has 9 tens.")
    order = ["b13", "t26", "b25", "o34", "b31", "m28", "n36", "fr27", "b40", "n42", "has19", "b47", "p35",
             "p28", "h40", "has50", "r23", "c19", "b24", "w32"]
    assert len(order) == 20 and set(order) == set(k)
    return {"title": "Tens and ones with rods and cubes", "items": [k[x] for x in order]}


# ============================================================ set 3: read and write numbers
def set_read():
    k = {}
    for key, n, wrong, extra in [
        ("w7", 7, [70, 17, 6], ""),
        ("w12", 12, [20, 21, 11], " Twenty is 20."),
        ("w15", 15, [50, 51, 5], " Fifty is 50."),
        ("w14", 14, [40, 41, 4], " You hear “four” first, but the 1 ten is written first."),
    ]:
        if n < 10:
            e = "Seven is the number after six. Write <b>7</b>. Seventy is 70 and seventeen is 17."
        else:
            e = "%s is 1 ten and %s. Write <b>%d</b>.%s" % (words(n).capitalize(), O(n - 10), n, extra)
        k[key] = mcq_n(fig(card_svg(words(n))) + "Which number is this?", n, wrong, e)
    for key, n, wrong, extra in [
        ("s13", 13, ["thirty", "three", "fourteen"], " Thirty is 30."),
        ("s20", 20, ["twelve", "two", "ten"], " Twelve is 12."),
        ("s11", 11, ["twelve", "one", "ten"], ""),
        ("s18", 18, ["eighty", "eight", "seventeen"], " Eighty is 80."),
    ]:
        e = "%d is %s. We say <b>%s</b>.%s" % (n, TO(n // 10, n % 10), words(n), extra)
        k[key] = mcq(fig(card_svg(str(n), 30)) + "How do you say this number?", words(n), wrong, e)
    k["c34"] = mcq_n(fig(chart_svg(34)) + "What number is in the chart?", 34, [43, 7, 304],
                     "The chart shows 3 tens and 4 ones. Write the tens first, then the ones: <b>34</b>.")
    k["c41"] = mcq_n(fig(chart_svg(41)) + "What number is in the chart?", 41, [14, 5, 401],
                     "The chart shows 4 tens and 1 one. Write the tens first, then the ones: <b>41</b>.")
    k["a25"] = mcq_n(fig(track_svg([23, 24, 25, "?"])) + "What number comes next?", 26, [27, 25, 36],
                     "Count on by 1: 23, 24, 25, <b>26</b>. Only the ones digit changes.")
    k["a29"] = mcq_n(fig(track_svg([27, 28, 29, "?"])) + "What number comes next?", 30, [20, 210, 39],
                     "After 29 comes <b>30</b>. 9 ones and 1 more make a new ten. Do not write 210 or go back to 20.")
    k["b40"] = mcq_n(fig(track_svg(["?", 40, 41, 42])) + "What number comes just before 40?", 39, [41, 30, 49],
                     "Count back by 1 from 40: 40, <b>39</b>. 30 is 10 less, not 1 less.")
    k["back"] = mcq_n(fig(track_svg([35, 34, 33, "?"])) + "Count back. What number comes next?", 32, [34, 31, 23],
                      "The numbers go down by 1: 35, 34, 33, <b>32</b>.")
    k["mid20"] = mcq_n(fig(track_svg([18, 19, "?", 21])) + "What number is missing?", 20, [22, 30, 10],
                       "Count on: 18, 19, <b>20</b>, 21. After 19 comes a new ten: 20.")
    k["jersey"] = mcq_n(fig(jersey_svg(31)) + "Owen wears this hockey jersey. How many tens are in his number?",
                        3, [1, 31, 30],
                        "The number is 31. The 3 is in the tens place. 31 has <b>3</b> tens and 1 one.")
    k["room"] = mcq_n(fig(door_svg(17)) + "Maya’s class is in Room 17. Which digit is in the ones place?",
                      7, [1, 17, 10],
                      "17 is 1 ten and 7 ones. The ones digit is the last digit: <b>7</b>.")
    k["t2"] = mcq_n(fig(cards_svg([52, 12, 32, 25])) + "Which number has 2 tens?", 25, [52, 12, 32],
                    "The tens digit is the first digit. In 25 the 2 comes first, so it means 2 tens. "
                    "The answer is <b>25</b>. In 52, 12 and 32, the 2 means 2 ones.")
    k["list"] = mcq(fig(track_svg([37, 38, 39, "?"])) + "Which list counts on by 1 the right way?",
                    "38, 39, 40", ["38, 39, 30", "38, 39, 310", "38, 39, 41"],
                    "After 39 comes 40: 3 tens become 4 tens. The right list is <b>38, 39, 40</b>.")
    k["m49"] = mcq_n(fig(track_svg([47, 48, 49, "?"])) + "What is 1 more than 49?", 50, [40, 410, 48],
                     "1 more than 49 is <b>50</b>. 9 ones and 1 more make a ten, so 4 tens become 5 tens.")
    order = ["w7", "s11", "w12", "c34", "a25", "w15", "s13", "back", "c41", "w14", "s20", "room", "mid20",
             "s18", "a29", "jersey", "b40", "t2", "list", "m49"]
    assert len(order) == 20 and set(order) == set(k)
    return {"title": "Read and write numbers", "items": [k[x] for x in order]}


# ============================================================ set 4: compare and order
ROWCH = ["Row A", "Row B", "They are the same", "You cannot tell"]
PAIRCH = ["A", "B", "They are the same", "You cannot tell"]


def set_compare():
    k = {}
    k["r1"] = fixed(fig(rows_svg([("A", 7, 34), ("B", 9, 22)], "apples")) + "Which row has more apples?",
                    ROWCH, "Row B",
                    "Count each row. Row A has 7. Row B has 9. 9 is more than 7, so <b>Row B</b> has more. "
                    "Row A is longer, but its apples are far apart.")
    k["r2"] = fixed(fig(rows_svg([("A", 4, 38), ("B", 6, 22)], "balls")) + "Which row has fewer balls?",
                    ROWCH, "Row A",
                    "Count each row. Row A has 4. Row B has 6. 4 is less than 6, so <b>Row A</b> has fewer. "
                    "Do not look at how long the row is.")
    k["r3"] = fixed(fig(rows_svg([("A", 8, 24), ("B", 8, 32)], "stars")) + "Which row has more stars?",
                    ROWCH, "They are the same",
                    "Row A has 8. Row B has 8. <b>They are the same</b>. Row B only looks longer.")
    k["g19"] = mcq_n(fig(cards_svg([13, 19, 16, 11])) + "Which number is the greatest?", 19, [13, 16, 11],
                     "All the numbers have 1 ten. Look at the ones: 9 is the most. <b>19</b> is the greatest.")
    k["l12"] = mcq_n(fig(cards_svg([17, 12, 20, 15])) + "Which number is the least?", 12, [17, 20, 15],
                     "20 has 2 tens, so it is not the least. 17, 12 and 15 have 1 ten. "
                     "Look at the ones: 2 is the fewest. <b>12</b> is the least.")
    k["p29"] = fixed(fig(pair_svg(29, 31)) + "Which blocks show the greater number?", PAIRCH, "B",
                     "A is 2 tens and 9 ones: 29. B is 3 tens and 1 one: 31. 3 tens is more than 2 tens, "
                     "so <b>B</b> is greater. A has more pieces, but B has more tens.")
    k["p24"] = fixed(fig(pair_svg(24, 42)) + "Which blocks show the smaller number?", PAIRCH, "A",
                     "A is 24. B is 42. 2 tens is less than 4 tens, so <b>A</b> is smaller.")
    k["p38"] = fixed(fig(pair_svg(38, 35)) + "Which blocks show the greater number?", PAIRCH, "A",
                     "Both have 3 tens. Look at the ones: A has 8 and B has 5. 38 is more than 35, so <b>A</b> "
                     "is greater.")
    k["t23"] = mcq(fig(pair_svg(23, 32)) + "A shows 23. B shows 32. Which is true?", "23 is less than 32",
                   ["23 is more than 32", "32 is less than 23", "23 is the same as 32"],
                   "23 has 2 tens. 32 has 3 tens. So <b>23 is less than 32</b>.")
    k["t19"] = mcq(fig(numline_svg(15, None, 10)) + "Which is true?", "19 is less than 21",
                   ["19 is more than 21", "21 is less than 19", "19 is the same as 21"],
                   "On a number line, numbers get bigger to the right. 19 is to the left of 21. "
                   "So <b>19 is less than 21</b>.")
    k["gt30"] = mcq_n(fig(cards_svg([29, 34, 13, 30])) + "Which number is greater than 30?", 34, [29, 13, 30],
                      "34 has 3 tens and 4 ones. 30 has 3 tens and 0 ones. So <b>34</b> is greater than 30. "
                      "30 is equal to 30, not greater.")
    k["lt20"] = mcq_n(fig(cards_svg([21, 18, 20, 28])) + "Which number is less than 20?", 18, [21, 20, 28],
                      "18 has 1 ten. 20, 21 and 28 have 2 tens. So <b>18</b> is less than 20.")
    k["g41"] = mcq_n(fig(cards_svg([14, 39, 41, 35])) + "Which number is the greatest?", 41, [14, 39, 35],
                     "Look at the tens first. 41 has 4 tens. The others have 1 or 3 tens. <b>41</b> is the greatest. "
                     "39 has more ones, but fewer tens.")
    k["l13"] = mcq_n(fig(cards_svg([31, 30, 13, 23])) + "Which number is the least?", 13, [31, 30, 23],
                     "Look at the tens first. 13 has only 1 ten. <b>13</b> is the least.")
    k["g50"] = mcq_n(fig(cards_svg([45, 49, 50, 5])) + "Which number is the greatest?", 50, [45, 49, 5],
                     "50 has 5 tens. 45 and 49 have 4 tens. 5 has no tens. <b>50</b> is the greatest. "
                     "49 has 9 ones, but 50 has more tens.")
    k["o3"] = mcq(fig(cards_svg([25, 18, 32])) + "Put the numbers in order from least to greatest.",
                  "18, 25, 32", ["25, 18, 32", "32, 25, 18", "18, 32, 25"],
                  "18 has 1 ten, 25 has 2 tens, 32 has 3 tens. The order is <b>18, 25, 32</b>.")
    k["o41"] = mcq(fig(cards_svg([40, 14, 41])) + "Put the numbers in order from greatest to least.",
                   "41, 40, 14", ["14, 40, 41", "40, 41, 14", "41, 14, 40"],
                   "40 and 41 have 4 tens. 41 has 1 more one, so it comes first. 14 has only 1 ten. "
                   "The order is <b>41, 40, 14</b>.")
    k["o36"] = mcq(fig(cards_svg([36, 27, 30])) + "Put the numbers in order from least to greatest.",
                   "27, 30, 36", ["30, 27, 36", "36, 30, 27", "27, 36, 30"],
                   "27 has 2 tens, so it is the least. 30 and 36 have 3 tens. 0 ones is less than 6 ones. "
                   "The order is <b>27, 30, 36</b>.")
    k["btw"] = mcq_n(fig(numline_svg(20, None, 15)) + "Which number is between 25 and 30?", 27, [24, 31, 20],
                     "Between 25 and 30 come 26, 27, 28 and 29. <b>27</b> is one of them.")
    k["o4"] = mcq(fig(cards_svg([12, 21, 20, 2])) + "Put the numbers in order from least to greatest.",
                  "2, 12, 20, 21", ["2, 12, 21, 20", "21, 20, 12, 2", "12, 2, 20, 21"],
                  "2 has no tens. 12 has 1 ten. 20 and 21 have 2 tens, and 20 has fewer ones. "
                  "The order is <b>2, 12, 20, 21</b>.")
    for a, b in [(18, 25), (25, 32), (14, 40), (40, 41), (27, 30), (30, 36), (2, 12), (12, 20), (20, 21),
                 (23, 32), (19, 21), (29, 31), (24, 42), (35, 38)]:
        assert a < b
    order = ["r1", "g19", "r2", "l12", "r3", "p29", "o3", "lt20", "p24", "gt30", "t19", "g41", "p38",
             "l13", "o41", "t23", "btw", "o36", "g50", "o4"]
    assert len(order) == 20 and set(order) == set(k)
    return {"title": "Compare and order numbers to 50", "items": [k[x] for x in order]}


# ============================================================ set 5: number lines and word problems
def set_lines_words():
    k = {}
    for key, lo, v, wrong, extra in [
        ("n8", 0, 8, [7, 9, 10], " Count from 5: 6, 7, 8."),
        ("n13", 0, 13, [12, 14, 31], " Count from 10: 11, 12, 13."),
        ("n22", 10, 22, [21, 23, 12], " Count from 20: 21, 22. 12 is how far it is from 10."),
        ("n36", 20, 36, [34, 63, 16], " Count from 35: 36."),
        ("n29", 20, 29, [28, 30, 19], " It is 1 before 30."),
        ("n47", 30, 47, [46, 74, 43], " Count from 45: 46, 47."),
    ]:
        assert lo <= v <= lo + 20
        e = "Each small mark is 1. The long marks show the numbers ending in 5 and 0.%s The arrow points to <b>%d</b>." % (extra, v)
        k[key] = mcq_n(fig(numline_svg(lo, v)) + "What number does the arrow point to?", v, wrong, e)
    k["n35"] = mcq_n(fig(numline50_svg(35)) + "What number does the arrow point to?", 35, [7, 30, 40],
                     "The numbers go up by 10. Each mark is 5, not 1. Count by 5s: 5, 10, 15, 20, 25, 30, "
                     "<b>35</b>.")
    k["where25"] = fixed(fig(numline_svg(20, None, 20, {23: "A", 27: "B", 33: "C", 37: "D"})) +
                         "Which letter shows 27?", ["A", "B", "C", "D"], "B",
                         "Find 25. Count on 2 marks: 26, 27. The letter is <b>B</b>. "
                         "A is 23, which is 2 marks before 25.")
    k["pucks"] = mcq_n(fig(objects_svg(24, "pucks")) + "Liam puts hockey pucks in rows of 10. How many pucks?",
                       24, [42, 6, 23],
                       "2 full rows: 10, 20. Then count on: 21, 22, 23, 24. There are <b>24</b> pucks.")
    k["geese"] = mcq_n(fig(tenframes_svg(13)) + "Emma sees 13 Canada geese. Then 1 more lands. How many now?",
                       14, [12, 13, 15],
                       "1 more than 13 is <b>14</b>. Count on 1: 13, 14.")
    k["stick35"] = mcq_n(fig(sticks_svg(3, 5)) + "Nathan has 3 bundles of 10 sticks and 5 more. How many sticks?",
                         35, [53, 8, 305],
                         "Count the bundles by tens: 10, 20, 30. Count on: 31, 32, 33, 34, 35. He has <b>35</b> sticks.")
    k["beads"] = mcq_n(fig(tenframes_svg(18)) + "Leah has 18 beads. She needs 20. How many more?",
                       2, [38, 20, 3],
                       "There are 2 empty boxes. 18 and <b>2</b> make 20.")
    assert 18 + 2 == 20
    k["day30"] = mcq_n(fig(track_svg([27, 28, 29, "?"])) + "Yesterday was day 29 of school. What day is today?",
                       30, [20, 210, 28],
                       "Today is 1 day after 29. After 29 comes <b>30</b>.")
    k["cans"] = mcq(fig(name_cards_svg([("Zoe", 38), ("Kai", 32)])) +
                    "Zoe’s class has 38 cans. Kai’s class has 32 cans. Which class has more?",
                    "Zoe’s class", ["Kai’s class", "They are the same", "You cannot tell"],
                    "Both have 3 tens. Look at the ones: 8 is more than 2. <b>Zoe’s class</b> has more.")
    k["stickers"] = mcq(fig(name_cards_svg([("Owen", 34), ("Ava", 43)])) +
                        "Owen has 34 stickers. Ava has 43 stickers. Who has more?",
                        "Ava", ["Owen", "They are the same", "You cannot tell"],
                        "34 has 3 tens. 43 has 4 tens. 43 is more, so <b>Ava</b> has more.")
    k["leaves"] = mcq(fig(blocks_svg(4, 0)) + "Maya counts 40 leaves. Arjun counts 4 tens of leaves. Who has more?",
                      "They are the same", ["Maya", "Arjun", "You cannot tell"],
                      "4 tens is 40. Maya has 40 and Arjun has 40. <b>They are the same</b>.")
    k["mystery"] = mcq_n(fig(numline_svg(30, None, 10)) +
                         "Sofia’s number is between 30 and 40. It has 5 ones. What is it?",
                         35, [53, 45, 25],
                         "Between 30 and 40 means 3 tens. 3 tens and 5 ones is <b>35</b>.")
    k["houses"] = mcq(fig(name_cards_svg([("Chloe", 14), ("Jayden", 41)])) +
                      "Chloe lives at number 14. Jayden lives at number 41. Whose number is greater?",
                      "Jayden’s", ["Chloe’s", "They are the same", "You cannot tell"],
                      "41 has 4 tens. 14 has 1 ten. 41 is greater, so <b>Jayden’s</b> number is greater. "
                      "Both use a 1 and a 4, but the order matters.")
    k["cards10"] = mcq_n(fig(blocks_svg(2, 7)) + "Benjamin has 27 hockey cards. Hana has 10 more. How many does Hana have?",
                         37, [28, 17, 47],
                         "10 more adds 1 ten. 2 tens and 7 ones become 3 tens and 7 ones: <b>37</b>. "
                         "28 is only 1 more.")
    assert 27 + 10 == 37
    k["cones"] = mcq(fig(name_cards_svg([("Lucas", 29), ("Mei", 41), ("Ethan", 38), ("Priya", 14)])) +
                     "Four friends count pine cones. Who has the most?", "Mei", ["Lucas", "Ethan", "Priya"],
                     "Look at the tens first. 41 has 4 tens. No one else has 4 tens. <b>Mei</b> has the most.")
    order = ["n8", "n13", "where25", "n22", "n29", "n36", "n47", "n35", "geese", "pucks", "beads", "stick35",
             "day30", "stickers", "cans", "leaves", "houses", "mystery", "cards10", "cones"]
    assert len(order) == 20 and set(order) == set(k)
    return {"title": "Number lines and word problems", "items": [k[x] for x in order]}


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
        "<h2>Count each thing once</h2>"
        "<p>Touch each thing as you count it. Count each thing <b>only once</b>. "
        "Groups of 5 and 10 make counting fast.</p>"
        "<figure class='sn-fig'>" + objects_svg(15, "apples") +
        "<figcaption>A full row is 10. Count on: 11, 12, 13, 14, 15. There are 15 apples.</figcaption></figure>"
        "<h2>Ten frames</h2>"
        "<p>A ten frame has 10 boxes. A full ten frame is <b>1 ten</b>. "
        "The empty boxes tell you how many more make 10.</p>"
        "<figure class='sn-fig'>" + tenframes_svg(14) +
        "<figcaption>1 full ten frame and 4 more. That is 14.</figcaption></figure>"
        "<h2>Tens and ones</h2>"
        "<p>A <b>rod</b> is 10. A <b>small cube</b> is 1. Count the rods by tens. Then count on the cubes.</p>"
        "<figure class='sn-fig'>" + blocks_svg(3, 4, labels=True) +
        "<figcaption>10, 20, 30, then 31, 32, 33, 34. 3 tens and 4 ones is 34.</figcaption></figure>"
        "<p>Write the <b>tens first</b>, then the ones. 34 = 30 + 4.</p>" +
        ex("Tens and ones", "What number is 2 tens and 8 ones?", "2 tens is 20. 8 more ones make 28.", "28") +
        "<h2>Read and write number words</h2>" +
        table(["Number", "Word", "Number", "Word"], [
            ["11", "eleven", "16", "sixteen"],
            ["12", "twelve", "17", "seventeen"],
            ["13", "thirteen", "18", "eighteen"],
            ["14", "fourteen", "19", "nineteen"],
            ["15", "fifteen", "20", "twenty"],
        ]) +
        "<p>In “fourteen” you hear the 4 first. But you write the 1 ten first: 14.</p>"
        "<h2>Compare and order</h2>"
        "<p>Look at the <b>tens first</b>. More tens means a greater number. "
        "If the tens are the same, look at the ones.</p>"
        "<figure class='sn-fig'>" + pair_svg(29, 31) +
        "<figcaption>A is 29. B is 31. A has more pieces, but B has more tens. 31 is greater.</figcaption></figure>" +
        ex("Which is greater?", "Which is greater, 23 or 32?", "23 has 2 tens. 32 has 3 tens.", "32") +
        "<h2>Number lines</h2>"
        "<p>On a number line, numbers get bigger to the right. Find a number you know. Then count the marks.</p>"
        "<figure class='sn-fig'>" + numline_svg(20, 27) +
        "<figcaption>From 25, count on 2 marks: 26, 27. The arrow points to 27.</figcaption></figure>"
        "<h2>Common mistakes</h2>" +
        table(["Mistake", "What to do instead"], [
            ["Writing 31 for 13", "Write the tens first: 1 ten and 3 ones is 13"],
            ["Counting one thing twice", "Touch each thing once, or cross it off"],
            ["Reading tens as ones (3 rods and 4 cubes = 7)", "Each rod is 10: 10, 20, 30, then 31 to 34"],
            ["Writing 1 ten and 3 ones as 103", "Use only 2 digits: 13"],
            ["Saying 210 after 29", "After 29 comes a new ten: 30"],
            ["Thinking a longer row has more", "Count both rows. Spread-out things can be fewer"],
        ])
    )


FAQ = [
    {"q": "What numbers should a Grade 1 student know in Ontario?",
     "a": "In the Ontario curriculum, Grade 1 students read, write and show whole numbers up to 50. They also break numbers into tens and ones and compare and order numbers to 50."},
    {"q": "How do ten frames help Grade 1 students?",
     "a": "A ten frame shows 10 in two rows of 5, so children see amounts at a glance and see how many more make 10. Two full frames and 4 more is 24."},
    {"q": "Why does my child write 31 for 13?",
     "a": "In words like “thirteen” you hear the 3 first, so children write it first. Build 13 with 1 rod and 3 cubes, then say “1 ten first, then 3 ones” while writing 13."},
    {"q": "What are base ten blocks in Grade 1 math?",
     "a": "Base ten blocks are the place value tools used in Ontario classrooms. A rod is 10 and a small cube is 1, so 3 rods and 4 cubes show 34."},
]


def mark_large(u, pattern):
    """Tag wide pictures (rows of objects, ten frames, blocks, number lines) so they print larger."""
    rx = re.compile(r"<svg (?=[^>]*aria-label='(?:" + pattern + ")')")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u


def gen_unit():
    rnd = random.Random(41801)
    sets = [set_count(), set_blocks(), set_read(), set_compare(), set_lines_words()]
    balance(sets, rnd)
    seen = set()
    for s in sets:
        assert len(s["items"]) == 20, (s["title"], len(s["items"]))
        assert sorted(it["a"] for it in s["items"]) == sorted([0, 1, 2, 3] * 5), s["title"]
        for it in s["items"]:
            assert len(set(it["c"])) == 4, it
            assert it["q"].count("<svg") <= 1
            key = it["q"] + "|" + "|".join(sorted(it["c"]))
            assert key not in seen, key
            seen.add(key)
    u = {
        "country": "ca-on", "subject": "math", "grade": "grade-1", "slug": "numbers-to-50", "sort": 1,
        "updated": UPDATED, "pdf_url": "",
        "title": "Numbers to 50: Count, Tens and Ones, Compare",
        "seo_title": "Grade 1 Numbers to 50 Math Worksheets: Ten Frames, Tens and Ones, Free with Answer Key (Ontario)",
        "short_title": "Numbers to 50",
        "domain": "Number",
        "standard_code": "Grade 1: B1.1",
        "standard_url": "https://www.dcp.edu.gov.on.ca/en/curriculum/elementary-mathematics",
        "standard_text": "Read and represent whole numbers up to and including 50, and describe various ways they are used in everyday life",
        "meta_desc": "Free Grade 1 math worksheets on numbers to 50 for the Ontario curriculum: count objects and ten frames, tens and ones with base ten blocks, number words to twenty, compare and order numbers, and number lines and word problems. 100 questions with pictures and an answer key.",
        "key_big": "Count the tens first, then the ones. 3 tens and 4 ones is 34.",
        "key_sub": "Write the tens digit first: 1 ten and 3 ones is 13, not 31. To compare, look at the tens first: 31 is greater than 29.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }
    return mark_large(u, "[a-z]+ in rows of 10|two rows of [a-z]+|ten frames with counters|base ten blocks|"
                         "number line [0-9]+ to [0-9]+|craft sticks in bundles of 10|number track|"
                         "name cards with numbers|number cards")


if __name__ == "__main__":
    u = gen_unit()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(u, f, ensure_ascii=False, indent=1)
    print("wrote", path)
