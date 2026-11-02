# -*- coding: utf-8 -*-
"""
BC Grade 1 Math: Numbers to 20 (BC Mathematics Curriculum, Grade 1 Content: Number concepts to 20)
  python3 tools/gen_cabc_math_g1_numbers.py
HTML attributes use single quotes (no backslashes in the JSON).
Grade 1: whole numbers to 20, very short sentences for 6-7 year olds, a picture in almost every question.
Canadian English (colour, centre, math, grade). BC contexts (salmon, bald eagles, BC Ferries, hockey).
Wrong answers come from real mistakes: swapping the digits (12 -> 21), counting an object twice or
missing one (n + 1, n - 1), reading the rod as 1 (1 rod and 4 cubes -> 5), writing 1 ten and 3 ones
as 103, counting the empty boxes in a ten frame, teen / -ty words (seventeen -> 70 or 71),
"after 19 comes 110", a longer row looks like more, and more pieces looks like more.
"""
import json, math, os, random, re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "ca-bc", "math", "grade-1")
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
    assert 0 <= correct <= 20, (q, correct)
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
    if kind == "salmon":
        return ("<path d='M %.1f %.1f Q %.1f %.1f %.1f %.1f Q %.1f %.1f %.1f %.1f Z' fill='#e07a5f' stroke='#9b3d24' stroke-width='1.2'/>"
                "<path d='M %.1f %.1f L %.1f %.1f L %.1f %.1f Z' fill='#e07a5f' stroke='#9b3d24' stroke-width='1.2'/>"
                "<circle cx='%.1f' cy='%.1f' r='1.3' fill='#2b2b2b'/>"
                % (cx - 6, cy, cx + 1, cy - 7, cx + 10, cy, cx + 1, cy + 7, cx - 6, cy,
                   cx - 6, cy, cx - 11, cy - 5, cx - 11, cy + 5, cx + 5.5, cy - 1.2))
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
    if t == 1 and o:
        return ("The full row has 10. Then count on: %s. There are <b>%d</b> %s."
                % (lst(range(11, n + 1)), n, what))
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
    if t == 1 and o:
        return ("The full ten frame is 10. Then count on: %s. There are <b>%d</b> counters."
                % (lst(range(11, n + 1)), n))
    e = "Each full ten frame is 10. Count by tens: %s." % lst(range(10, 10 * t + 1, 10))
    if o:
        e += " Then count on: %s." % lst(range(10 * t + 1, n + 1))
    return e + " There are <b>%d</b> counters." % n


def blocks_e(t, o):
    n = 10 * t + o
    if t == 0:
        return "There are no rods. Count the cubes: <b>%d</b>." % n
    if t == 1 and o:
        return "The rod is 10. Then count on the cubes: %s. %s is <b>%d</b>." % (lst(range(11, n + 1)), TO(t, o), n)
    e = "Each rod is 10. Count the rods by tens: %s." % lst(range(10, 10 * t + 1, 10))
    if o:
        e += " Then count on the cubes: %s." % lst(range(10 * t + 1, n + 1))
    return e + " %s is <b>%d</b>." % (TO(t, o), n)



# ============================================================ set 1: count objects to 20
def set_count():
    k = {}
    for key, n, kind, wrong in [
        ("c5", 5, "balls", [6, 4, 7]),
        ("c7", 7, "apples", [8, 6, 2]),
        ("c8", 8, "stars", [9, 7, 3]),
        ("c10", 10, "buttons", [11, 9, 5]),
        ("c11", 11, "pucks", [12, 10, 2]),
        ("c12", 12, "balls", [21, 13, 11]),
        ("c13", 13, "apples", [31, 14, 12]),
        ("c14", 14, "stars", [41, 15, 13]),
        ("c15", 15, "buttons", [51, 16, 5]),
        ("c16", 16, "pucks", [61, 17, 6]),
        ("c17", 17, "apples", [71, 18, 7]),
        ("c18", 18, "balls", [81, 19, 17]),
        ("c19", 19, "stars", [91, 20, 9]),
        ("c20", 20, "buttons", [2, 21, 19]),
    ]:
        e = count_e(n, kind)
        if n <= 10 and n + 1 in wrong:
            e += " %d means one was counted twice." % (n + 1)
        if n in (7, 8):
            e += " %d counts only the ones after the group of 5." % (n - 5)
        if n == 10:
            e += " 5 counts only one group of 5."
        if n == 11:
            e += " Do not write 2. The first row is 1 ten, not 1."
        if 11 < n < 20:
            e += " Write the 1 ten first: %d, not %d." % (n, (n % 10) * 10 + 1)
        if n % 10 in wrong and n > 10:
            e += " %d counts only the second row." % (n % 10)
        if n == 20:
            e += " 2 tens is 20, not 2."
        k[key] = mcq_n(fig(objects_svg(n, kind)) + "How many %s?" % kind, n, wrong, e)
    k["twice"] = mcq_n(fig(objects_svg(12, "balls")) + "Ava counts 13 balls. She counted one ball twice. How many balls are there?",
                       12, [13, 14, 21],
                       "Ava counted one ball two times, so 13 is 1 too many. Count again and touch each ball once: "
                       "10, then 11, 12. There are <b>12</b> balls.")
    k["more9"] = mcq_n(fig(objects_svg(9, "stars")) + "Add 1 more star. How many stars now?", 10, [9, 11, 8],
                       "There are 9 stars. 1 more than 9 is <b>10</b>. Count on: 9, 10.")
    k["less15"] = mcq_n(fig(objects_svg(15, "apples")) + "Leah eats 1 apple. How many apples are left?", 14, [16, 15, 41],
                        "There are 15 apples. 1 less than 15 is <b>14</b>. Count back: 15, 14. 16 is 1 more, not 1 less.")
    k["w17"] = mcq_n(fig(card_svg("seventeen")) + "Which number is this?", 17, [70, 71, 7],
                     "Seventeen is 1 ten and 7 ones. Write <b>17</b>. You hear “seven” first, but write the 1 first. "
                     "Seventy is 70.")
    k["s13"] = mcq(fig(card_svg("13", 30)) + "How do you say this number?", "thirteen",
                   ["thirty", "three", "fourteen"],
                   "13 is 1 ten and 3 ones. We say <b>thirteen</b>. Thirty is 30.")
    k["after19"] = mcq_n(fig(track_svg([17, 18, 19, "?"])) + "Count by 1s. What comes next?", 20, [110, 10, 21],
                         "After 19 comes a new ten: <b>20</b>. Do not write 110.")
    order = ["c5", "c7", "c8", "more9", "c10", "c11", "c12", "s13", "c13", "c14", "c15", "less15", "c16",
             "w17", "c17", "c18", "twice", "c19", "after19", "c20"]
    assert len(order) == 20 and set(order) == set(k)
    return {"title": "Count objects to 20", "items": [k[x] for x in order]}


# ============================================================ set 2: ten frames
def set_frames():
    k = {}
    for key, n, wrong in [("f4", 4, [6, 5, 3]), ("f6", 6, [4, 7, 5]), ("f8", 8, [2, 9, 7])]:
        e = frames_e(n) + " %d is the number of empty boxes." % (10 - n)
        k[key] = mcq_n(fig(tenframes_svg(n)) + "How many counters are in the ten frame?", n, wrong, e)
    k["f10"] = mcq_n(fig(tenframes_svg(10)) + "How many counters are in the ten frame?", 10, [1, 9, 11],
                     "Every box has a counter. A full ten frame is <b>10</b>. It is 1 ten, but the number is 10, not 1.")
    for key, n, wrong in [("m7", 7, [7, 4, 2]), ("m5", 5, [10, 4, 6]), ("m9", 9, [9, 10, 2]),
                          ("m2", 2, [2, 7, 12])]:
        need = 10 - n
        e = "Count the empty boxes: there %s. %d and <b>%d</b> make 10." % (
            "is 1" if need == 1 else "are %d" % need, n, need)
        if n in wrong:
            e += " %d is how many counters there are now." % n
        if 10 in wrong:
            e += " 10 is the whole frame, not the missing part."
        k[key] = mcq_n(fig(tenframes_svg(n)) + "How many more counters make 10?", need, wrong, e)
    teen = [("f11", 11, [12, 1, 9], " 9 is the number of empty boxes."),
            ("f12", 12, [21, 2, 13], " Write the tens first: 12, not 21."),
            ("f13", 13, [31, 3, 7], " 7 is the number of empty boxes."),
            ("f14", 14, [41, 4, 15], " 4 counts only the second frame."),
            ("f16", 16, [61, 6, 17], " Write the tens first: 16, not 61."),
            ("f17", 17, [71, 7, 18], " 18 means one counter was counted twice."),
            ("f19", 19, [91, 9, 18], " 18 means one counter was missed.")]
    for key, n, wrong, extra in teen:
        q = "What number do the ten frames show?" if n == 17 else "How many counters are there?"
        k[key] = mcq_n(fig(tenframes_svg(n)) + q, n, wrong, frames_e(n) + extra)
    k["f20"] = mcq_n(fig(tenframes_svg(20)) + "How many counters are there?", 20, [2, 10, 21],
                     "Both ten frames are full. Count by tens: 10, 20. There are <b>20</b> counters. 2 tens is 20, not 2.")
    for key, n, wrong in [("t13", 13, [3, 13, 6]), ("t18", 18, [8, 18, 3]), ("t15", 15, [15, 4, 6]),
                          ("t11", 11, [1, 11, 8])]:
        need = 20 - n
        e = ("The first frame is full. The second frame has %s and %d empty boxes. %d and <b>%d</b> make 20."
             % (unit(n - 10, "counter", "counters"), need, n, need))
        if n in wrong:
            e += " %d is how many counters there are now." % n
        k[key] = mcq_n(fig(tenframes_svg(n)) + "How many more counters make 20?", need, wrong, e)
    for n, m in [(7, 3), (5, 5), (9, 1), (2, 8), (13, 7), (18, 2), (15, 5), (11, 9)]:
        assert n + m == (10 if n < 10 else 20)
    order = ["f4", "f6", "m5", "f8", "m7", "f10", "m9", "m2", "f11", "f12", "f13", "f14", "t15", "f16",
             "t18", "f17", "t13", "f19", "f20", "t11"]
    assert len(order) == 20 and set(order) == set(k)
    return {"title": "Ten frames", "items": [k[x] for x in order]}


# ============================================================ set 3: 10 and some more
def set_ten_and():
    k = {}
    k["b13"] = mcq_n(fig(blocks_svg(1, 3)) + "What number do the blocks show?", 13, [31, 4, 103],
                     blocks_e(1, 3) + " Write the ten first: 13, not 31 or 103.")
    k["tens19"] = mcq_n(fig(blocks_svg(1, 9)) + "How many tens are in 19?", 1, [9, 10, 19],
                        "There is 1 rod. A rod is 1 ten. 19 has <b>1</b> ten and 9 ones.")
    k["ones16"] = mcq_n(fig(blocks_svg(1, 6)) + "How many ones are in 16?", 6, [1, 16, 10],
                        "Count the small cubes: 6. 16 has 1 ten and <b>6</b> ones.")
    k["b16"] = mcq_n(fig(blocks_svg(1, 6)) + "What number do the blocks show?", 16, [61, 7, 106],
                     blocks_e(1, 6) + " 7 counts the rod as 1, not 10.")
    k["s12"] = mcq_n(fig(sticks_svg(1, 2)) + "10 + 2 = ☐", 12, [21, 3, 102],
                     "1 bundle is 10 sticks. 2 more sticks: 11, 12. So 10 + 2 = <b>12</b>.")
    k["eq14"] = mcq_n(fig(blocks_svg(1, 4)) + "14 = 10 + ☐", 4, [14, 1, 40],
                      "14 is 1 ten and 4 ones. The rod is 10. The cubes are 4. So 14 = 10 + <b>4</b>.")
    k["lhs15"] = mcq_n(fig(tenframes_svg(15)) + "10 + 5 = ☐", 15, [51, 6, 105],
                       "One full frame is 10. 5 more counters: 11, 12, 13, 14, 15. So 10 + 5 = <b>15</b>. "
                       "6 adds 1 and 5, but the full frame is 10.")
    k["match12"] = mcq(fig(tenframes_svg(12)) + "Which matches the ten frames?", TO(1, 2),
                       [TO(2, 1), TO(1, 8), TO(1, 12)],
                       "1 frame is full: 1 ten. The other frame has 2 counters: 2 ones. That is <b>%s</b>. "
                       "8 is the number of empty boxes." % TO(1, 2))
    k["has11"] = mcq_n(fig(blocks_svg(1, 1)) + "Which number is 1 ten and 1 one?", 11, [2, 101, 10],
                       "1 ten is 10. 1 more one makes <b>11</b>. Use only 2 digits, not 101.")
    k["eq17"] = mcq_n(fig(tenframes_svg(17)) + "17 = 10 + ☐", 7, [17, 3, 1],
                      "The full frame is 10. The other frame has 7 counters. So 17 = 10 + <b>7</b>. "
                      "3 is the number of empty boxes.")
    k["s18"] = mcq_n(fig(sticks_svg(1, 8)) + "1 bundle of 10 sticks and 8 more. How many sticks?", 18, [81, 9, 108],
                     "The bundle is 10. Count on 8: 11, 12, 13, 14, 15, 16, 17, 18. There are <b>18</b> sticks.")
    k["rod10"] = mcq_n(fig(blocks_svg(1, 9)) + "☐ + 9 = 19", 10, [1, 9, 19],
                       "19 is 1 ten and 9 ones. The rod is 10, not 1. So <b>10</b> + 9 = 19.")
    k["way13"] = mcq(fig(sticks_svg(1, 3)) + "Which is the same as 13?", "10 + 3", ["1 + 3", "30 + 1", "10 + 13"],
                     "13 is 1 ten and 3 ones. 1 ten is 10. So 13 = <b>10 + 3</b>. 1 + 3 is only 4.")
    assert 10 + 3 == 13 and 1 + 3 != 13 and 30 + 1 != 13 and 10 + 13 != 13
    k["c19"] = mcq_n(fig(blocks_svg(1, 9)) + "Add 1 more cube. What number is it now?", 20, [110, 29, 19],
                     "The blocks show 19. 1 more cube makes 10 cubes. 10 cubes make 1 more ten. "
                     "Now there are 2 tens: <b>20</b>. Do not write 110.")
    k["left15"] = mcq_n(fig(blocks_svg(0, 15)) + "Put 10 cubes together to make a rod. How many cubes are left?",
                        5, [15, 1, 10],
                        "15 is 10 and 5 more. 10 cubes make the rod. <b>5</b> cubes are left. So 15 is 1 ten and 5 ones.")
    k["eq20"] = mcq_n(fig(tenframes_svg(20)) + "20 = 10 + ☐", 10, [2, 0, 20],
                      "Both frames are full. Each frame is 10. So 20 = 10 + <b>10</b>.")
    k["eq11"] = mcq_n(fig(blocks_svg(1, 1)) + "10 + ☐ = 11", 1, [11, 10, 0],
                      "11 is 1 ten and 1 one. 10 and <b>1</b> more make 11.")
    k["has10"] = mcq_n(fig(blocks_svg(1, 0)) + "Which number has 1 ten and 0 ones?", 10, [1, 100, 11],
                       "1 ten is 10 cubes in a rod. There are no loose cubes, so write 0 ones: <b>10</b>.")
    k["take17"] = mcq_n(fig(blocks_svg(1, 7)) + "Take away the rod. How many are left? 17 − 10 = ☐", 7, [16, 10, 1],
                        "17 is 10 and 7 more. Take away the 10. <b>7</b> are left. 16 takes away only 1.")
    k["tt20"] = mcq_n(fig(sticks_svg(2, 0)) + "10 + 10 = ☐", 20, [2, 11, 100],
                      "Each bundle is 10. Count by tens: 10, 20. So 10 + 10 = <b>20</b>.")
    for n, t, o in [(13, 1, 3), (16, 1, 6), (12, 1, 2), (14, 1, 4), (15, 1, 5), (17, 1, 7), (18, 1, 8), (19, 1, 9),
                    (11, 1, 1), (10, 1, 0), (20, 2, 0)]:
        assert n == 10 * t + o
    assert 17 - 10 == 7 and 10 + 10 == 20
    order = ["b13", "tens19", "ones16", "b16", "s12", "has11", "eq14", "lhs15", "match12", "has10", "eq17",
             "s18", "eq11", "rod10", "way13", "left15", "take17", "eq20", "tt20", "c19"]
    assert len(order) == 20 and set(order) == set(k)
    return {"title": "10 and some more", "items": [k[x] for x in order]}


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
    k["r4"] = fixed(fig(rows_svg([("A", 11, 22), ("B", 9, 30)], "buttons")) + "Which row has fewer buttons?",
                    ROWCH, "Row B",
                    "Row A has 11. Row B has 9. 9 is less than 11, so <b>Row B</b> has fewer. "
                    "Row B is longer, but its buttons are far apart.")
    k["more3"] = mcq_n(fig(rows_svg([("A", 6, 26), ("B", 9, 26)], "balls")) + "How many more balls are in Row B?",
                       3, [9, 15, 6],
                       "Match each ball in Row A with one in Row B. 3 balls in Row B have no match. "
                       "Row B has <b>3</b> more. 9 is all of Row B, and 15 adds the rows.")
    k["fewer3"] = mcq_n(fig(rows_svg([("A", 10, 24), ("B", 7, 24)], "apples")) + "How many fewer apples are in Row B?",
                        3, [7, 17, 10],
                        "Row A has 10. Row B has 7. 7 and 3 make 10, so Row B has <b>3</b> fewer.")
    assert 9 - 6 == 3 and 10 - 7 == 3
    k["g19"] = mcq_n(fig(cards_svg([13, 19, 16, 11])) + "Which number is the greatest?", 19, [13, 16, 11],
                     "All the numbers have 1 ten. Look at the ones: 9 is the most. <b>19</b> is the greatest.")
    k["l12"] = mcq_n(fig(cards_svg([17, 12, 20, 15])) + "Which number is the least?", 12, [17, 20, 15],
                     "20 has 2 tens, so it is not the least. 17, 12 and 15 have 1 ten. "
                     "Look at the ones: 2 is the fewest. <b>12</b> is the least.")
    k["gt15"] = mcq_n(fig(cards_svg([12, 18, 15, 9])) + "Which number is greater than 15?", 18, [12, 15, 9],
                      "18 comes after 15 when you count. So <b>18</b> is greater than 15. "
                      "15 is equal to 15, not greater.")
    k["lt10"] = mcq_n(fig(cards_svg([12, 10, 8, 11])) + "Which number is less than 10?", 8, [12, 10, 11],
                      "8 has no tens. 10, 11 and 12 have 1 ten. So <b>8</b> is less than 10.")
    k["g20"] = mcq_n(fig(cards_svg([10, 20, 2, 12])) + "Which number is the greatest?", 20, [12, 10, 2],
                     "20 has 2 tens. 10 and 12 have 1 ten. 2 has no tens. <b>20</b> is the greatest.")
    k["p9"] = fixed(fig(pair_svg(9, 11)) + "Which blocks show the greater number?", PAIRCH, "B",
                    "A is 9 cubes: 9. B is 1 rod and 1 cube: 11. 11 is more than 9, so <b>B</b> is greater. "
                    "A has more pieces, but the rod is 10.")
    k["p14"] = fixed(fig(pair_svg(14, 17)) + "Which blocks show the smaller number?", PAIRCH, "A",
                     "Both have 1 ten. A has 4 ones and B has 7 ones. 14 is less than 17, so <b>A</b> is smaller.")
    k["p18"] = fixed(fig(pair_svg(18, 15)) + "Which blocks show the greater number?", PAIRCH, "A",
                     "Both have 1 ten. Look at the ones: A has 8 and B has 5. 18 is more than 15, so <b>A</b> "
                     "is greater.")
    k["t13"] = mcq(fig(numline_svg(10, None, 10)) + "Which is true?", "13 is less than 16",
                   ["13 is more than 16", "16 is less than 13", "13 is the same as 16"],
                   "On a number line, numbers get bigger to the right. 13 is to the left of 16. "
                   "So <b>13 is less than 16</b>.")
    k["o3"] = mcq(fig(cards_svg([15, 8, 12])) + "Put the numbers in order from least to greatest.",
                  "8, 12, 15", ["15, 8, 12", "15, 12, 8", "8, 15, 12"],
                  "8 has no tens, so it is the least. 12 and 15 have 1 ten. 2 ones is less than 5 ones. "
                  "The order is <b>8, 12, 15</b>.")
    k["o20"] = mcq(fig(cards_svg([11, 20, 17])) + "Put the numbers in order from greatest to least.",
                   "20, 17, 11", ["11, 17, 20", "17, 20, 11", "20, 11, 17"],
                   "20 has 2 tens, so it comes first. 17 has more ones than 11. The order is <b>20, 17, 11</b>.")
    k["btw"] = mcq_n(fig(numline_svg(10, None, 10)) + "Which number is between 14 and 17?", 16, [13, 18, 17],
                     "Between 14 and 17 come 15 and 16. <b>16</b> is one of them. 17 is the end, not between.")
    k["less16"] = mcq_n(fig(track_svg([13, 14, 15, 16])) + "Which number is 1 less than 16?", 15, [17, 6, 14],
                        "1 less means count back 1: 16, <b>15</b>. 17 is 1 more. 6 is 10 less.")
    k["o4"] = mcq(fig(cards_svg([19, 9, 10, 1])) + "Put the numbers in order from least to greatest.",
                  "1, 9, 10, 19", ["9, 1, 10, 19", "19, 10, 9, 1", "1, 10, 19, 9"],
                  "1 and 9 have no tens, and 1 is less than 9. 10 and 19 have 1 ten, and 10 has fewer ones. "
                  "The order is <b>1, 9, 10, 19</b>.")
    for a, b in [(8, 12), (12, 15), (11, 17), (17, 20), (1, 9), (9, 10), (10, 19), (13, 16), (9, 11), (14, 17),
                 (15, 18)]:
        assert a < b
    order = ["r1", "r2", "g19", "r3", "l12", "more3", "lt10", "p9", "r4", "gt15", "fewer3", "p14", "t13",
             "less16", "p18", "o3", "g20", "btw", "o20", "o4"]
    assert len(order) == 20 and set(order) == set(k)
    return {"title": "Compare and order: more and fewer", "items": [k[x] for x in order]}


# ============================================================ set 5: number lines and word problems
def set_lines_words():
    k = {}
    for key, v, wrong, extra in [
        ("n8", 8, [7, 9, 10], " Count from 5: 6, 7, 8."),
        ("n13", 13, [12, 14, 31], " Count from 10: 11, 12, 13."),
        ("n17", 17, [16, 18, 71], " Count from 15: 16, 17."),
        ("n19", 19, [18, 20, 91], " It is 1 before 20."),
    ]:
        e = "Each small mark is 1. The long marks show 0, 5, 10, 15 and 20.%s The arrow points to <b>%d</b>." % (extra, v)
        k[key] = mcq_n(fig(numline_svg(0, v)) + "What number does the arrow point to?", v, wrong, e)
    k["where16"] = fixed(fig(numline_svg(0, None, 20, {11: "A", 14: "B", 16: "C", 19: "D"})) +
                         "Which letter shows 16?", ["A", "B", "C", "D"], "C",
                         "Find 15. Count on 1 mark: 16. The letter is <b>C</b>. B is 14, which is 1 mark before 15.")
    k["jump"] = mcq_n(fig(numline_svg(0, 12)) + "The arrow is at 12. Jump 3 to the right. Where do you land?",
                      15, [9, 14, 16],
                      "Jump right 1 mark at a time: 13, 14, <b>15</b>. Do not count 12 as a jump. "
                      "9 is 3 to the left.")
    k["salmon"] = mcq_n(fig(objects_svg(12, "salmon")) +
                        "Kai sees 12 salmon in the river. 1 more swims by. How many now?",
                        13, [12, 11, 31],
                        "1 more than 12 is <b>13</b>. Count on 1: 12, 13. 11 is 1 less.")
    k["pucks"] = mcq_n(fig(objects_svg(16, "pucks")) + "Liam puts hockey pucks in rows of 10. How many pucks?",
                       16, [61, 6, 17],
                       "1 full row is 10. Then count on: 11, 12, 13, 14, 15, 16. There are <b>16</b> pucks.")
    k["cones"] = mcq_n(fig(tenframes_svg(18)) + "Nadia needs 20 pine cones for art. She has 18. How many more?",
                       2, [38, 20, 3],
                       "There are 2 empty boxes. 18 and <b>2</b> make 20.")
    assert 18 + 2 == 20
    k["shells"] = mcq(fig(name_cards_svg([("Zara", 15), ("Owen", 12)])) +
                      "Zara finds 15 shells. Owen finds 12 shells. Who has more?",
                      "Zara", ["Owen", "They are the same", "You cannot tell"],
                      "Both have 1 ten. Look at the ones: 5 is more than 2. <b>Zara</b> has more.")
    k["fewer"] = mcq(fig(name_cards_svg([("Mei", 17), ("Wei", 19)])) +
                     "Mei reads 17 books. Wei reads 19 books. Who reads fewer?",
                     "Mei", ["Wei", "They are the same", "You cannot tell"],
                     "17 comes before 19 when you count. 17 is less, so <b>Mei</b> reads fewer.")
    k["mystery"] = mcq_n(fig(numline_svg(10, None, 10)) + "My number is between 10 and 20. It has 6 ones. What is it?",
                         16, [61, 6, 26],
                         "Between 10 and 20 means 1 ten. 1 ten and 6 ones is <b>16</b>.")
    k["ferry"] = mcq_n(fig(tenframes_svg(15)) +
                       "A BC Ferries boat has 10 cars on one deck. It has 5 cars on the other deck. How many cars?",
                       15, [105, 51, 6],
                       "10 and 5 more is 1 ten and 5 ones. 10 + 5 = <b>15</b> cars.")
    k["eagles"] = mcq_n(fig(tenframes_svg(9)) + "Lucas sees 9 bald eagles. Then 1 more lands. How many now?",
                        10, [9, 11, 8],
                        "1 more than 9 is <b>10</b>. Now the ten frame is full.")
    k["day20"] = mcq_n(fig(track_svg([17, 18, 19, "?"])) + "Yesterday was day 19 of school. What day is today?",
                       20, [110, 10, 18],
                       "Today is 1 day after 19. After 19 comes <b>20</b>.")
    k["jersey"] = mcq_n(fig(jersey_svg(17)) + "Owen wears this hockey jersey. How many tens are in his number?",
                        1, [7, 17, 10],
                        "The number is 17. The 1 is in the tens place. 17 has <b>1</b> ten and 7 ones.")
    k["room"] = mcq_n(fig(door_svg(12)) + "Hana’s class is in Room 12. Which digit is in the ones place?",
                      2, [1, 12, 21],
                      "12 is 1 ten and 2 ones. The ones digit is the last digit: <b>2</b>.")
    k["sticks"] = mcq_n(fig(sticks_svg(1, 4)) + "Sofia has 1 bundle of 10 sticks and 4 more. How many sticks?",
                        14, [41, 5, 104],
                        "The bundle is 10. Count on: 11, 12, 13, 14. She has <b>14</b> sticks.")
    k["most"] = mcq(fig(name_cards_svg([("Lucas", 13), ("Mei", 18), ("Ethan", 11), ("Chloe", 16)])) +
                    "Four friends count rocks at the beach. Who has the most?", "Mei", ["Lucas", "Ethan", "Chloe"],
                    "All the numbers have 1 ten. Look at the ones: 8 is the most. <b>Mei</b> has 18.")
    k["twice"] = mcq_n(fig(objects_svg(15, "apples")) +
                       "Arjun counts 16 apples. He counted one apple twice. How many apples are there?",
                       15, [16, 17, 51],
                       "16 is 1 too many, because one apple was counted twice. "
                       "Touch each apple once: 10, then 11, 12, 13, 14, 15. There are <b>15</b> apples.")
    order = ["n8", "n13", "where16", "n17", "n19", "jump", "eagles", "salmon", "pucks", "sticks", "cones",
             "day20", "jersey", "room", "shells", "fewer", "ferry", "twice", "mystery", "most"]
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
        "<figure class='sn-fig'>" + objects_svg(13, "apples") +
        "<figcaption>A full row is 10. Count on: 11, 12, 13. There are 13 apples.</figcaption></figure>"
        "<h2>Ten frames</h2>"
        "<p>A ten frame has 10 boxes. A full ten frame is <b>10</b>. "
        "The empty boxes tell you how many more make 10. For numbers past 10, use two ten frames.</p>"
        "<figure class='sn-fig'>" + tenframes_svg(14) +
        "<figcaption>1 full ten frame and 4 more. That is 14.</figcaption></figure>"
        "<h2>10 and some more</h2>"
        "<p>Every number from 11 to 19 is <b>10 and some more</b>. A rod is 10. A small cube is 1.</p>"
        "<figure class='sn-fig'>" + blocks_svg(1, 6, labels=True) +
        "<figcaption>1 ten and 6 ones. 10 + 6 = 16.</figcaption></figure>" +
        ex("10 and some more", "17 = 10 + ☐", "17 is 1 ten and 7 ones. The ten is 10. The ones are 7.", "7") +
        "<h2>Read and write number words</h2>" +
        table(["Number", "Word", "Number", "Word"], [
            ["11", "eleven", "16", "sixteen"],
            ["12", "twelve", "17", "seventeen"],
            ["13", "thirteen", "18", "eighteen"],
            ["14", "fourteen", "19", "nineteen"],
            ["15", "fifteen", "20", "twenty"],
        ]) +
        "<p>In “fourteen” you hear the 4 first. But you write the 1 first: 14.</p>"
        "<h2>Compare: more and fewer</h2>"
        "<p>Count both groups. Do not look at how long a row is. "
        "To compare numbers, look at the tens first, then the ones.</p>"
        "<figure class='sn-fig'>" + pair_svg(9, 11) +
        "<figcaption>A is 9. B is 11. A has more pieces, but the rod is 10. 11 is greater.</figcaption></figure>" +
        ex("Which is greater?", "Which is greater, 15 or 12?", "Both have 1 ten. 5 ones is more than 2 ones.", "15") +
        "<h2>Number lines</h2>"
        "<p>On a number line, numbers get bigger to the right. Find a number you know. Then count the marks.</p>"
        "<figure class='sn-fig'>" + numline_svg(0, 17) +
        "<figcaption>From 15, count on 2 marks: 16, 17. The arrow points to 17.</figcaption></figure>"
        "<h2>Common mistakes</h2>" +
        table(["Mistake", "What to do instead"], [
            ["Writing 21 for 12", "Write the 1 ten first: 1 ten and 2 ones is 12"],
            ["Counting one thing twice", "Touch each thing once, or cross it off"],
            ["Counting the empty boxes in a ten frame", "Count the counters. Empty boxes show how many more make 10"],
            ["Reading the rod as 1 (1 rod and 4 cubes = 5)", "A rod is 10: 10, then 11, 12, 13, 14"],
            ["Writing 110 after 19", "After 19 comes a new ten: 20"],
            ["Thinking a longer row has more", "Count both rows. Spread-out things can be fewer"],
        ])
    )


FAQ = [
    {"q": "What numbers should a Grade 1 student know in BC?",
     "a": "In the BC curriculum, Grade 1 students learn number concepts to 20. They count, read, write and show numbers to 20, see teen numbers as 10 and some more, and compare and order them."},
    {"q": "How do ten frames help Grade 1 students?",
     "a": "A ten frame shows 10 in two rows of 5, so children see amounts at a glance and see how many more make 10. One full frame and 4 more is 14."},
    {"q": "Why does my child write 21 for 12?",
     "a": "In words like “sixteen” you hear the 6 first, so children often write the digits in the wrong order. Build the number with 1 rod and some cubes and say “1 ten first, then the ones” while writing it."},
    {"q": "How can I practise numbers to 20 at home?",
     "a": "Count real things together, like shells, pine cones or toys, and touch each one once. Put 10 in a group, then count on: 10, 11, 12."},
]


def mark_large(u, pattern):
    """Tag wide pictures (rows of objects, ten frames, blocks, number lines) so they print larger."""
    rx = re.compile(r"<svg (?=[^>]*aria-label='(?:" + pattern + ")')")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u


def gen_unit():
    rnd = random.Random(51801)
    sets = [set_count(), set_frames(), set_ten_and(), set_compare(), set_lines_words()]
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
        "country": "ca-bc", "subject": "math", "grade": "grade-1", "slug": "numbers-to-20", "sort": 1,
        "updated": UPDATED, "pdf_url": "",
        "title": "Numbers to 20: Count, Ten Frames, Compare",
        "seo_title": "Grade 1 Math Numbers to 20 Worksheets: Ten Frames, Free with Answer Key (BC Curriculum)",
        "short_title": "Numbers to 20",
        "domain": "Number",
        "standard_code": "Grade 1: Number",
        "standard_url": "https://curriculum.gov.bc.ca/curriculum/mathematics/1/core",
        "standard_text": "Number concepts to 20",
        "meta_desc": "Free Grade 1 math worksheets on numbers to 20 for the BC curriculum: count objects, ten frames, teen numbers as 10 and some more, compare and order with more and fewer, and number lines and word problems. 100 questions with pictures and an answer key.",
        "key_big": "Every teen number is 10 and some more: 14 = 10 + 4.",
        "key_sub": "Write the 1 ten first: 1 ten and 2 ones is 12, not 21. Touch each thing once when you count, so nothing is counted twice.",
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
