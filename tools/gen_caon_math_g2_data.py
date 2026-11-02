# -*- coding: utf-8 -*-
"""
CA Grade 2 Math: Data and graphs (Ontario Curriculum 2020, Data: D1.1 to D1.5)
  python3 tools/gen_caon_math_g2_data.py
Sorting by two attributes in Venn and Carroll diagrams, two-way tally tables, pictographs and line plots with
one-to-one correspondence, bar graphs with a scale of 1 (with sources, titles and labels), the mode (one mode,
two modes or no mode), and asking questions and drawing conclusions in Canadian contexts.
Wrong answers come from real student mistakes: counting a tally group of 5 as 4, reading one cell of a table
instead of the whole row or column, forgetting the overlap or the items outside a Venn diagram, adding the
numbers on a line plot axis instead of counting the X's, giving the biggest number (or the count) as the mode,
adding when the question asks “how many more”.
HTML attributes use single quotes (no backslashes in the JSON). Canadian English.
"""
import json, re, math, os, random

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "ca-on", "math", "grade-2")
UPDATED = "2026-11-02"
GREEN = "#006633"
BAR = "#2e8b57"
BAR2 = "#3a6ea5"
FILL = "#cfe6d6"
FILL2 = "#e6f2ea"
RED = "#c0392b"
INK = "#2b2b2b"
GRID = "#c9d3cc"
MUTE = "#555555"
FONT = "Arial, Helvetica, sans-serif"
COLS = {"red": "#d7263d", "blue": "#2b59c3", "yellow": "#f4c430", "green": "#3aa655"}


# ------------------------------------------------------------ helpers
def mcq(q, correct, cands, e):
    """4 choices: correct + 3 unique distractors from real mistakes (no zero or negative numbers).
    Positions are balanced later for the whole set."""
    correct = str(correct)
    seen = {correct}
    pick = []
    for c in cands:
        c = str(c)
        lead = c.split(" ")[0]
        if c in seen or not c or lead.startswith("-") or lead.startswith("−") or lead == "0":
            continue
        seen.add(c)
        pick.append(c)
        if len(pick) == 3:
            break
    assert len(pick) == 3, (q, correct, cands)
    return {"q": q, "c": pick + [correct], "a": 3, "e": e}


def mcq_fixed(q, choices, ai, e):
    """Choices keep their order (A, B, C, D). The answer position is not moved later."""
    assert len(set(choices)) == 4 and 0 <= ai < 4
    return {"q": q, "c": list(choices), "a": ai, "e": e, "_fix": True}


def fig(svg):
    return "<div class='qfig'>" + svg + "</div>"


def svg_wrap(w, h, body, label):
    w, h = int(math.ceil(w)), int(math.ceil(h))
    return ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 %d %d' width='%d' height='%d' "
            "role='img' aria-label='%s'><g font-family='%s'>%s</g></svg>" % (w, h, w, h, label, FONT, body))


def part_svg(part, label):
    W, H, body = part
    return svg_wrap(W, H, body, label)


def tw(t, fs, bold=False):
    """Approximate text width in px (Arial)."""
    return len(str(t)) * fs * (0.62 if bold else 0.58)


def text(x, y, t, fs=14, anchor="middle", bold=False, col=INK, extra=""):
    return ("<text x='%.1f' y='%.1f' font-size='%d'%s fill='%s' text-anchor='%s'%s>%s</text>"
            % (x, y, fs, " font-weight='700'" if bold else "", col, anchor, extra, t))


def fmt(v, unit):
    """unit = (singular, plural)."""
    return "%d %s" % (v, unit[0] if v == 1 else unit[1])


def ones(cnt, word):
    return "%d %s" % (cnt, word if cnt == 1 else word + "s")


def plus(vals):
    return " + ".join(str(v) for v in vals)


STU = ("student", "students")
B = ("bird", "birds")


# ------------------------------------------------------------ shapes
def star_pts(cx, cy, R=9.5, r=4.0):
    pts = []
    for i in range(10):
        ang = -math.pi / 2 + i * math.pi / 5
        rad = R if i % 2 == 0 else r
        pts.append((cx + rad * math.cos(ang), cy + rad * math.sin(ang)))
    return pts


def obj(o, cx, cy, r=None):
    """o = (kind, colour, big). Dark outline so it still reads in black and white."""
    kind, col, big = o
    if r is None:
        r = 13.5 if big else 8
    f = COLS[col]
    st = " stroke='%s' stroke-width='1.3'" % INK
    if kind == "circle":
        return "<circle cx='%.1f' cy='%.1f' r='%.1f' fill='%s'%s/>" % (cx, cy, r, f, st)
    if kind == "square":
        a = r * 0.88
        return "<rect x='%.1f' y='%.1f' width='%.1f' height='%.1f' fill='%s'%s/>" % (cx - a, cy - a, 2 * a, 2 * a, f, st)
    if kind == "triangle":
        pts = [(cx, cy - r * 1.05), (cx - r * 1.12, cy + r * 0.85), (cx + r * 1.12, cy + r * 0.85)]
    else:
        pts = star_pts(cx, cy, R=r * 1.15, r=r * 0.5)
    return "<polygon points='%s' fill='%s'%s/>" % (" ".join("%.1f,%.1f" % p for p in pts), f, st)


def symbol(kind, cx, cy, col=GREEN):
    if kind == "circle":
        return "<circle cx='%.1f' cy='%.1f' r='8.5' fill='%s'/>" % (cx, cy, col)
    if kind == "square":
        return "<rect x='%.1f' y='%.1f' width='15' height='15' rx='2' fill='%s'/>" % (cx - 7.5, cy - 7.5, col)
    return "<polygon points='%s' fill='%s'/>" % (" ".join("%.1f,%.1f" % p for p in star_pts(cx, cy)), col)


def source_line(y, src):
    return text(8, y, src, 14, anchor="start", col=MUTE, extra=" font-style='italic'")


# ------------------------------------------------------------ Venn and Carroll diagrams
VW, VCX1, VCX2, VCY, VR = 410, 165, 245, 132, 90


def venn_svg(la, lb, a_only, both, b_only, outside, label, fs=15):
    """Two overlapping circles in a box. Items are text or shapes (tuples); each is checked to sit inside its region."""
    H = VCY + VR + 42
    s = ["<rect x='3' y='3' width='%d' height='%d' rx='6' fill='#ffffff' stroke='%s' stroke-width='1.5'/>" % (VW - 6, H - 6, GREEN),
         "<circle cx='%d' cy='%d' r='%d' fill='%s' fill-opacity='0.45' stroke='%s' stroke-width='2'/>" % (VCX1, VCY, VR, FILL, GREEN),
         "<circle cx='%d' cy='%d' r='%d' fill='%s' fill-opacity='0.35' stroke='%s' stroke-width='2'/>" % (VCX2, VCY, VR, "#d6e2f0", BAR2),
         text(VCX1 - 40, 30, la, 15, bold=True, col=GREEN),
         text(VCX2 + 40, 30, lb, 15, bold=True, col=BAR2)]
    assert VCX1 - 40 - tw(la, 15, True) / 2 > 6 and VCX2 + 40 + tw(lb, 15, True) / 2 < VW - 6, (la, lb)
    assert VCX1 - 40 + tw(la, 15, True) / 2 < VCX2 + 40 - tw(lb, 15, True) / 2 - 8, (la, lb)

    def inside(px, py, cx):
        return (px - cx) ** 2 + (py - VCY) ** 2 < (VR - 3) ** 2

    def outside_c(px, py, cx):
        return (px - cx) ** 2 + (py - VCY) ** 2 > (VR + 3) ** 2

    def place(items, x, region):
        n = len(items)
        step = 29 if items and isinstance(items[0], tuple) else 25
        for k, t in enumerate(items):
            yc = VCY + (k - (n - 1) / 2.0) * step
            if isinstance(t, tuple):
                hw, hh = 12, 12
            else:
                hw, hh = tw(t, fs) / 2, 7
            for px in (x - hw, x + hw):
                for py in (yc - hh, yc + hh):
                    a, b = inside(px, py, VCX1), inside(px, py, VCX2)
                    oa, ob = outside_c(px, py, VCX1), outside_c(px, py, VCX2)
                    ok = {"a": a and ob, "b": b and oa, "ab": a and b}[region]
                    assert ok, (t, region, px, py)
            if isinstance(t, tuple):
                s.append(obj(t, x, yc, r=10.5))
            else:
                s.append(text(x, yc + 5, t, fs))
    place(a_only, 113, "a")
    place(both, (VCX1 + VCX2) / 2.0, "ab")
    place(b_only, 297, "b")
    if outside:
        widths = [24 if isinstance(t, tuple) else tw(t, fs) for t in outside]
        gap = 22
        tot = sum(widths) + gap * (len(outside) - 1)
        x = (VW - tot) / 2
        yb = VCY + VR + 22
        for t, w in zip(outside, widths):
            if isinstance(t, tuple):
                s.append(obj(t, x + w / 2, yb - 4, r=10.5))
            else:
                s.append(text(x + w / 2, yb + 1, t, fs))
            x += w + gap
        assert tot < VW - 20
    return svg_wrap(VW, H, "".join(s), label)


def carroll_svg(cols, rows, cells, label, letters=False, fs=15):
    """2 x 2 Carroll diagram. cells[r][c] = list of shapes (tuples) or lines of text."""
    hw = int(max(tw(r, fs, True) for r in rows) + 20)
    shapes = isinstance(cells[0][0][0], tuple)
    if shapes:
        cw = int(max(max(tw(c, fs, True) for c in cols) + 20,
                     max(len(cell) for row in cells for cell in row) * 32 + (44 if letters else 20)))
        rh = 52
    else:
        cw = int(max(max(tw(c, fs, True) for c in cols) + 20,
                     max(tw(line, fs) for row in cells for cell in row for line in cell) + (44 if letters else 24)))
        nl = max(len(cell) for row in cells for cell in row)
        rh = max(40, 16 + 22 * nl)
    hh = 30
    W = hw + 2 * cw + 8
    H = hh + 2 * rh + 8
    x0, y0 = 4, 4
    s = []
    for c in range(2):
        x = x0 + hw + c * cw
        s.append("<rect x='%d' y='%d' width='%d' height='%d' fill='%s' stroke='%s' stroke-width='1.5'/>" % (x, y0, cw, hh, FILL2, GREEN))
        s.append(text(x + cw / 2, y0 + 20, cols[c], fs, bold=True))
    for r in range(2):
        y = y0 + hh + r * rh
        s.append("<rect x='%d' y='%d' width='%d' height='%d' fill='%s' stroke='%s' stroke-width='1.5'/>" % (x0, y, hw, rh, FILL2, GREEN))
        s.append(text(x0 + hw / 2, y + rh / 2 + 5, rows[r], fs, bold=True))
        for c in range(2):
            x = x0 + hw + c * cw
            s.append("<rect x='%d' y='%d' width='%d' height='%d' fill='#ffffff' stroke='%s' stroke-width='1.5'/>" % (x, y, cw, rh, GREEN))
            if letters:
                s.append(text(x + 8, y + 19, "ABCD"[r * 2 + c], 16, anchor="start", bold=True, col=BAR2))
            cell = cells[r][c]
            off = 10 if letters else 0
            if shapes:
                n = len(cell)
                for k, o in enumerate(cell):
                    cx = x + cw / 2 + off + (k - (n - 1) / 2.0) * 32
                    assert x + 30 < cx - 14 if letters else x < cx - 14
                    assert cx + 14 < x + cw
                    s.append(obj(o, cx, y + rh / 2))
            else:
                for k, line in enumerate(cell):
                    ly = y + rh / 2 + 5 + (k - (len(cell) - 1) / 2.0) * 22
                    s.append(text(x + cw / 2 + off, ly, line, fs))
    return svg_wrap(W, H, "".join(s), label)


# ------------------------------------------------------------ tally marks and two-way tally tables
def tally_marks(x, cy, v):
    """Groups of five: four upright lines and the fifth line across."""
    s = []
    for g in range(v // 5):
        for k in range(4):
            xx = x + k * 6
            s.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='2'/>" % (xx, cy - 8, xx, cy + 8, INK))
        s.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='2'/>" % (x - 3, cy + 6, x + 21, cy - 6, INK))
        x += 34
    for k in range(v % 5):
        xx = x + k * 6
        s.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='2'/>" % (xx, cy - 8, xx, cy + 8, INK))
    return "".join(s)


def tally_width(v):
    return (v // 5) * 34 + (v % 5) * 6


def tally_only_svg(v):
    W = max(tally_width(v) + 30, 80)
    return svg_wrap(W, 34, "<rect x='1' y='1' width='%d' height='32' rx='4' fill='#ffffff' stroke='%s' stroke-width='1.5'/>"
                    % (W - 2, GRID) + tally_marks(15, 17, v), "tally marks")


def two_way_svg(title, head, cats, groups, data, label, tally=True, missing=None, source=None):
    """Two-way tally table: one row per category, one column per group. data[g][r] = count.
    missing = (g, r) for a red ?."""
    fs, rh = 15, 30
    c1 = int(max(max(tw(c, fs) for c in cats), tw(head, fs, True)) + 20)
    gws = []
    for g, name in enumerate(groups):
        inner = max(tally_width(v) for v in data[g]) + 26 if tally else 0
        gws.append(int(max(inner, tw(name, fs, True) + 20, 60)))
    cols = [c1] + gws
    top = 30
    tot = sum(cols)
    W = int(max(tot + 8, tw(title, 16, True) + 16, tw(source, 14) + 16 if source else 0))
    x0 = (W - tot) / 2
    s = [text(W / 2, 20, title, 16, bold=True)]
    rows = [head] + cats
    for r, c in enumerate(rows):
        y = top + r * rh
        x = x0
        for k, cw in enumerate(cols):
            hd = r == 0
            s.append("<rect x='%.1f' y='%d' width='%d' height='%d' fill='%s' stroke='%s' stroke-width='1.5'/>"
                     % (x, y, cw, rh, FILL2 if hd or k == 0 else "#ffffff", GREEN))
            if k == 0:
                s.append(text(x + 10, y + 20, c, fs, anchor="start", bold=hd))
            elif hd:
                s.append(text(x + cw / 2, y + 20, groups[k - 1], fs, bold=True))
            else:
                v = data[k - 1][r - 1]
                if missing == (k - 1, r - 1):
                    s.append(text(x + cw / 2, y + 21, "?", 17, bold=True, col=RED))
                elif tally:
                    s.append(tally_marks(x + 14, y + rh / 2, v))
                else:
                    s.append(text(x + cw / 2, y + 20, v, fs))
            x += cw
    H = top + len(rows) * rh + 6
    if source:
        s.append(source_line(H + 14, source))
        H += 22
    return svg_wrap(W, H, "".join(s), label)


def tally_text(v):
    g, r = v // 5, v % 5
    if g and r:
        return "%s of 5 and %d more. Count %s, then %s. So it is %d." % (
            ones(g, "group"), r, ", ".join(str(5 * k) for k in range(1, g + 1)),
            ", ".join(str(5 * g + k) for k in range(1, r + 1)), v)
    if g:
        return "%s of 5. Count %s. So it is %d." % (ones(g, "group"), ", ".join(str(5 * k) for k in range(1, g + 1)), v)
    return "%s. So it is %d." % (ones(r, "single mark"), v)


def tally_cands(v):
    g, r = v // 5, v % 5
    return [g * 4 + r, v + 1, v - 1, g + r, v + 5]


# ------------------------------------------------------------ pictograph (one symbol for each)
def pic_part(title, cats, vals, sym, unit, source=None, minsym=4):
    fs, rh, gap = 15, 26, 23
    lw = max(tw(c, fs) for c in cats) + 22
    m = max(max(vals), minsym)
    keytxt = "= " + fmt(1, unit)
    kw = tw("Key:", fs, True) + 32 + tw(keytxt, fs)
    W = int(max(lw + 12 + m * gap + 14, tw(title, 16, True) + 16, kw + 16, tw(source, 14) + 16 if source else 0))
    top = 28
    s = [text(W / 2, 19, title, 16, bold=True)]
    H_tab = len(cats) * rh
    s.append("<rect x='4' y='%d' width='%d' height='%d' fill='none' stroke='%s' stroke-width='1.5'/>" % (top, W - 8, H_tab, GREEN))
    s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='1.5'/>" % (lw, top, lw, top + H_tab, GREEN))
    for i, (c, v) in enumerate(zip(cats, vals)):
        y = top + i * rh
        if i:
            s.append("<line x1='4' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='1'/>" % (y, W - 4, y, GRID))
        s.append(text(lw - 8, y + 18, c, fs, anchor="end"))
        for j in range(v):
            s.append(symbol(sym, lw + 12 + j * gap + 9, y + rh / 2))
    ky = top + H_tab + 22
    x = (W - kw) / 2
    s.append(text(x, ky, "Key:", fs, anchor="start", bold=True))
    x += tw("Key:", fs, True) + 16
    s.append(symbol(sym, x, ky - 5))
    s.append(text(x + 14, ky, keytxt, fs, anchor="start"))
    H = ky + 8
    if source:
        s.append(source_line(ky + 24, source))
        H = ky + 30
    return (W, H, "".join(s))


def pic_svg(title, cats, vals, sym, unit, source=None):
    return part_svg(pic_part(title, cats, vals, sym, unit, source), "pictograph: " + title.lower())


def uneven_svg():
    """Two rows that do not line up: 5 big, spread-out symbols and 7 small, close ones."""
    s = [text(170, 19, "Favourite sport", 16, bold=True)]
    lw = 84
    s.append(text(lw - 8, 50, "Hockey", 15, anchor="end"))
    s.append(text(lw - 8, 86, "Skating", 15, anchor="end"))
    for j in range(5):
        s.append("<circle cx='%.1f' cy='45' r='12' fill='%s'/>" % (lw + 18 + j * 54, GREEN))
    for j in range(7):
        s.append("<circle cx='%.1f' cy='81' r='6' fill='%s'/>" % (lw + 12 + j * 18, GREEN))
    s.append("<line x1='%d' y1='28' x2='%d' y2='100' stroke='%s' stroke-width='1.5'/>" % (lw, lw, GREEN))
    return svg_wrap(340, 106, "".join(s), "pictograph with rows that do not line up")


# ------------------------------------------------------------ line plot
def plot_svg(title, start, counts, axis, label, gap=46):
    n = len(counts)
    mx = max(counts)
    pad = 28
    pw = int(2 * pad + gap * (n - 1))
    W = int(max(pw, tw(title, 16, True) + 16, tw(axis, 15, True) + 16))
    ox = (W - pw) / 2
    Y = 44 + 18 * (mx - 1) + 10
    H = Y + 54
    X = lambda i: ox + pad + gap * i
    s = [text(W / 2, 19, title, 16, bold=True),
         "<line x1='%.1f' y1='%d' x2='%.1f' y2='%d' stroke='%s' stroke-width='2'/>" % (ox + pad - 18, Y, ox + pw - pad + 18, Y, INK)]
    for i in range(n):
        x = X(i)
        s.append("<line x1='%.1f' y1='%d' x2='%.1f' y2='%d' stroke='%s' stroke-width='1.8'/>" % (x, Y - 6, x, Y + 6, INK))
        s.append(text(x, Y + 24, start + i, 16))
        for k in range(counts[i]):
            cy = Y - 18 - 18 * k
            s.append("<path d='M%.1f %d L%.1f %d M%.1f %d L%.1f %d' stroke='%s' stroke-width='2.4' stroke-linecap='round'/>"
                     % (x - 6, cy - 6, x + 6, cy + 6, x - 6, cy + 6, x + 6, cy - 6, GREEN))
    assert Y - 18 - 18 * (mx - 1) - 6 > 28
    s.append(text(W / 2, Y + 46, axis, 15, bold=True))
    return svg_wrap(W, H, "".join(s), label)


# ------------------------------------------------------------ bar graph (scale of 1)
def bar_svg(title, cat_axis, val_axis, cats, vals, label, source=None, top_v=None):
    fs = 14
    top_v = top_v or max(max(vals), 5)
    nt = top_v
    assert 5 <= nt <= 12, (title, vals)
    gy = 16 if nt > 8 else 19
    ph = nt * gy
    x0 = 22 + tw(top_v, fs) + 6
    slot = max(50, max(tw(c, fs) for c in cats) + 12)
    pw = slot * len(cats)
    y0 = 32
    yb = y0 + ph
    W = max(x0 + pw + 8, tw(title, 16, True) + 16, tw(source, 14) + 16 if source else 0)
    s = []
    if title:
        s.append(text(W / 2, 18, title, 16, bold=True))
    for k in range(nt + 1):
        y = yb - k * gy
        s.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='1'/>" % (x0, y, x0 + pw, y, GRID))
        s.append(text(x0 - 5, y + 5, k, fs, anchor="end"))
    for i, (c, v) in enumerate(zip(cats, vals)):
        cx = x0 + slot * i + slot / 2
        bw = 30
        h = v * gy
        s.append("<rect x='%.1f' y='%.1f' width='%.1f' height='%.1f' fill='%s'/>" % (cx - bw / 2, yb - h, bw, h, BAR))
        s.append(text(cx, yb + 17, c, fs))
    s.append("<path d='M%.1f %d V%d H%.1f' fill='none' stroke='%s' stroke-width='2'/>" % (x0, y0 - 6, yb, x0 + pw, INK))
    s.append(text(x0 + pw / 2, yb + 36, cat_axis, fs, bold=True))
    mid = y0 + ph / 2
    s.append(text(13, mid, val_axis, fs, bold=True, extra=" transform='rotate(-90 13 %.1f)'" % mid))
    assert tw(val_axis, fs, True) < ph + 26, (val_axis, ph)
    H = yb + 42
    if source:
        s.append(source_line(yb + 60, source))
        H = yb + 66
    return svg_wrap(W, H, "".join(s), label)


# ------------------------------------------------------------ A to D panels (one picture)
PW, PH = 218, 172


def mini_bar(x0, y0, cats, vals, top_v):
    fs = 14
    gy = 112.0 / top_v
    ax = x0 + 34
    yb = y0 + 142
    slot = 44
    s = []
    for k in range(top_v + 1):
        y = yb - k * gy
        s.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='1'/>" % (ax, y, ax + slot * len(cats), y, GRID))
        if top_v <= 8 or k % 2 == 0:
            s.append(text(ax - 4, y + 5, k, fs, anchor="end"))
    for i, (c, v) in enumerate(zip(cats, vals)):
        cx = ax + slot * i + slot / 2
        h = v * gy
        s.append("<rect x='%.1f' y='%.1f' width='24' height='%.1f' fill='%s'/>" % (cx - 12, yb - h, h, BAR))
        s.append(text(cx, yb + 17, c, fs))
        assert tw(c, fs) <= slot - 2, c
    s.append("<path d='M%.1f %.1f V%.1f H%.1f' fill='none' stroke='%s' stroke-width='2'/>" % (ax, yb - 116, yb, ax + slot * len(cats), INK))
    assert ax + slot * len(cats) <= x0 + PW - 2
    return "".join(s)


def panel_svg(draws, label):
    W, H = 2 * PW, 2 * PH
    s = ["<line x1='%d' y1='4' x2='%d' y2='%d' stroke='%s' stroke-width='1'/>" % (PW, PW, H - 4, GRID),
         "<line x1='4' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='1'/>" % (PH, W - 4, PH, GRID)]
    for k, d in enumerate(draws):
        x0, y0 = (k % 2) * PW, (k // 2) * PH
        s.append(d(x0, y0))
        s.append(text(x0 + 8, y0 + 20, "ABCD"[k], 18, anchor="start", bold=True))
    return svg_wrap(W, H, "".join(s), label)


# ------------------------------------------------------------ set 1: sort by two attributes
def sh(kind, col, big=False):
    return (kind, col, big)


def set_sort(rnd):
    its = []
    # Carroll diagram of shapes: colour (columns) and size (rows)
    cells = [[[sh("circle", "red", True), sh("star", "red", True), sh("square", "red", True)],
              [sh("triangle", "blue", True), sh("circle", "blue", True)]],
             [[sh("square", "red"), sh("triangle", "red"), sh("circle", "red"), sh("star", "red")],
              [sh("circle", "blue"), sh("square", "blue"), sh("star", "blue"), sh("triangle", "blue"),
               sh("circle", "blue"), sh("square", "blue")]]]
    n = [[len(c) for c in row] for row in cells]
    assert n == [[3, 2], [4, 6]]
    cf = fig(carroll_svg(["Red", "Blue"], ["Big", "Small"], cells,
                         "carroll diagram: shapes sorted by colour and size", letters=True))
    its.append(mcq(cf + "How many shapes are big <b>and</b> red?", 3, [7, 5, 4],
                   "Find the box in the Big row and the Red column. That is box A. It has 3 shapes. "
                   "(7 is all the red shapes, and 5 is all the big shapes.)"))
    its.append(mcq(cf + "How many shapes are blue?", 8, [6, 2, 15],
                   "Add both boxes in the Blue column: 2 big + 6 small. 2 + 6 = 8. "
                   "(6 is only the small blue shapes.)"))
    its.append(mcq(cf + "How many shapes are small?", 10, [4, 6, 5],
                   "Add both boxes in the Small row: 4 red + 6 blue. 4 + 6 = 10."))
    its.append(mcq_fixed(cf + "Which box should a small blue triangle go in?", ["A", "B", "C", "D"], 3,
                         "It is small, so it goes in the Small row. It is blue, so it goes in the Blue column. "
                         "That is box D. (The shape does not matter here. Only size and colour.)"))
    its.append(mcq_fixed(cf + "Which box should a big blue star go in?", ["A", "B", "C", "D"], 1,
                         "It is big: Big row. It is blue: Blue column. That is box B."))
    its.append(mcq(cf + "How many more small shapes are there than big shapes?", 5, [15, 10, 3],
                   "Small: 4 + 6 = 10. Big: 3 + 2 = 5. How many more means take away: 10 − 5 = 5. "
                   "(15 adds them.)"))
    # Venn diagram of shapes: Red and Triangles
    a = [sh("circle", "red"), sh("square", "red"), sh("star", "red")]
    ab = [sh("triangle", "red"), sh("triangle", "red")]
    b = [sh("triangle", "blue"), sh("triangle", "yellow"), sh("triangle", "blue"), sh("triangle", "green")]
    o = [sh("circle", "blue"), sh("square", "yellow"), sh("square", "blue"), sh("star", "green")]
    vf = fig(venn_svg("Red", "Triangles", a, ab, b, o, "venn diagram: red shapes and triangles"))
    WH = ["In the overlap", "Only in Red", "Only in Triangles", "Outside the circles"]
    its.append(mcq(vf + "How many shapes are red triangles?", 2, [5, 6, 4],
                   "Red triangles are red <b>and</b> triangles, so they are in the overlap, where the circles cross. "
                   "There are 2. (5 counts the whole Red circle.)"))
    its.append(mcq(vf + "How many triangles are there?", 6, [4, 2, 13],
                   "Count the whole Triangles circle, and do not forget the overlap: 4 + 2 = 6. "
                   "(4 forgets the red triangles in the overlap.)"))
    its.append(mcq(vf + "Where should a new red triangle go?", WH[0], WH[1:],
                   "It is red and it is a triangle. It belongs in both circles, so it goes in the overlap."))
    its.append(mcq(vf + "Where should a blue circle go?", WH[3], WH[:3],
                   "A blue circle is not red and not a triangle. It does not fit either circle, "
                   "so it goes outside the circles."))
    its.append(mcq(vf + "Where should a yellow triangle go?", WH[2], [WH[0], WH[1], WH[3]],
                   "It is a triangle, but it is not red. It goes only in the Triangles circle, not in the overlap."))
    its.append(mcq(vf + "How many shapes are <b>not</b> red?", 8, [4, 5, 13],
                   "Shapes that are not red are outside the Red circle: 4 in the Triangles part and 4 outside both "
                   "circles. 4 + 4 = 8. (4 forgets the shapes outside the circles.)"))
    # Venn diagram of numbers
    WN = ["In the overlap", "Only in Even", "Only in More than 50", "Outside the circles"]
    v1 = fig(venn_svg("Even", "More than 50", ["14", "30", "6", "48"], ["62", "96", "70"], ["75", "81", "59"],
                      ["23", "7", "41"], "venn diagram: even numbers and numbers more than 50"))
    its.append(mcq(v1 + "How many numbers are even <b>and</b> more than 50?", 3, [7, 6, 4],
                   "Numbers that fit both labels are in the overlap: 62, 96 and 70. That is 3 numbers. "
                   "(7 is the whole Even circle, and 6 is the whole More than 50 circle.)"))
    its.append(mcq(v1 + "Where should 50 go?", WN[1], [WN[0], WN[2], WN[3]],
                   "50 is even (it ends in 0). But 50 is not <b>more than</b> 50. It is equal to 50. "
                   "So 50 goes only in the Even circle."))
    its.append(mcq(v1 + "Where should 49 go?", WN[3], WN[:3],
                   "49 is odd (it ends in 9), so it is not even. 49 is less than 50. "
                   "It fits neither circle, so it goes outside."))
    v2 = fig(venn_svg("Even", "More than 50", ["14", "30", "6"], ["62", "46", "70"], ["75", "81", "59"],
                      ["23", "7", "41"], "venn diagram with one number in the wrong place"))
    its.append(mcq(v2 + "One number is in the wrong place. Which number is it?", 46, [62, 59, 23],
                   "46 is even, but 46 is less than 50. It should be only in the Even circle, not in the overlap."))
    # Venn diagram of students
    vs = fig(venn_svg("Has a dog", "Has a cat", ["Liam", "Ava", "Mateo", "Chloe"], ["Emma", "Kai"],
                      ["Priya", "Ethan", "Leah"], ["Mei", "Arjun", "Zoe"], "venn diagram: students with a dog or a cat"))
    its.append(mcq(vs + "How many students have a dog <b>and</b> a cat?", fmt(2, STU), [fmt(x, STU) for x in [6, 5, 4]],
                   "Students with both pets are in the overlap: Emma and Kai. That is 2 students."))
    its.append(mcq(vs + "How many students have a dog?", fmt(6, STU), [fmt(x, STU) for x in [4, 2, 12]],
                   "Count the whole dog circle: Liam, Ava, Mateo, Chloe and Emma, Kai in the overlap. 4 + 2 = 6. "
                   "(4 forgets the students in the overlap.)"))
    its.append(mcq(vs + "How many students have no dog and no cat?", fmt(3, STU), [fmt(x, STU) for x in [2, 9, 12]],
                   "No dog and no cat means outside both circles: Mei, Arjun and Zoe. That is 3 students."))
    its.append(mcq("Hana sorts 12, 35, 40 and 7 in a Venn diagram. The circles are “Even” and “More than 30”. "
                   "Which number goes in the overlap?", 40, [35, 12, 7],
                   "40 is even, and 40 is more than 30, so it goes in the overlap. 35 is more than 30 but odd. "
                   "12 is even but not more than 30. 7 goes outside both circles."))
    assert len(its) == 20
    return {"title": "Sort by two attributes: Venn and Carroll diagrams", "items": its}


# ------------------------------------------------------------ set 2: two-way tally tables
def set_tally(rnd):
    its = []
    for v in (7, 12, 15, 18):
        its.append(mcq(fig(tally_only_svg(v)) + "What number do these tally marks show?", v, tally_cands(v),
                       "The fifth mark goes across the other four, so each group is 5. " + tally_text(v)))
    # which tally shows 13
    order = [18, 13, 12, 14]
    s = []
    for k, v in enumerate(order):
        x0, y0 = (k % 2) * 190, (k // 2) * 44
        s.append(text(x0 + 8, y0 + 27, "ABCD"[k], 17, anchor="start", bold=True))
        s.append(tally_marks(x0 + 34, y0 + 21, v))
        assert x0 + 34 + tally_width(v) < x0 + 186
    svg = svg_wrap(380, 88, "".join(s), "four sets of tally marks")
    its.append(mcq_fixed(fig(svg) + "Which tally marks show 13?", ["A", "B", "C", "D"], 1,
                         "13 = 5 + 5 + 3. Look for 2 groups of 5 and 3 single marks. That is B. "
                         "A shows 18 (one group too many), C shows 12 (one mark missing), D shows 14 (one mark too many)."))
    # favourite snack, two-way tally table
    cats = ["Apples", "Cheese", "Crackers", "Yogurt"]
    g1, g2 = [6, 3, 8, 4], [5, 9, 4, 7]
    assert sum(g1) == 21 and sum(g2) == 25
    T = fig(two_way_svg("Favourite snack", "Snack", cats, ["Grade 1", "Grade 2"], [g1, g2],
                        "two-way tally table: favourite snack", source="Source: class survey"))
    its.append(mcq(T + "How many Grade 2 students chose cheese?", fmt(9, STU), [fmt(x, STU) for x in [8, 3, 12, 10]],
                   "Find the Cheese row and the Grade 2 column. " + tally_text(9) +
                   " (3 is the Grade 1 box. 12 adds both grades.)"))
    its.append(mcq(T + "How many students chose apples?", fmt(11, STU), [fmt(x, STU) for x in [6, 5, 10, 12]],
                   "Add both boxes in the Apples row: Grade 1 has 6 and Grade 2 has 5. 6 + 5 = 11. "
                   "(6 or 5 reads only one box.)"))
    its.append(mcq(T + "How many Grade 1 students answered the survey?", fmt(21, STU), [fmt(x, STU) for x in [25, 19, 46]],
                   "Add every box in the Grade 1 column: 6 + 3 + 8 + 4 = 21. "
                   "(19 counts each group of 5 as 4. 25 is the Grade 2 column.)"))
    its.append(mcq(T + "Which snack did the most Grade 2 students choose?", "Cheese", ["Crackers", "Yogurt", "Apples"],
                   "Look only at the Grade 2 column: apples 5, cheese 9, crackers 4, yogurt 7. Cheese has the most. "
                   "(Crackers is the most in Grade 1.)"))
    its.append(mcq(T + "How many more Grade 1 students than Grade 2 students chose crackers?", fmt(4, STU),
                   [fmt(x, STU) for x in [12, 8, 3]],
                   "Crackers: Grade 1 has 8 and Grade 2 has 4. How many more means take away: 8 − 4 = 4. "
                   "(12 adds them.)"))
    its.append(mcq(T + "How many students answered altogether?", fmt(46, STU), [fmt(x, STU) for x in [41, 25, 21]],
                   "Grade 1: 21. Grade 2: 5 + 9 + 4 + 7 = 25. Altogether: 21 + 25 = 46. "
                   "(41 counts each group of 5 tally marks as 4.)"))
    its.append(mcq(T + "This table shows two things about each student. What are they?", "Grade and snack",
                   ["Name and snack", "Grade and age", "Snack and drink"],
                   "Each tally mark is in a row (the snack) and a column (the grade). "
                   "So the table shows each student’s grade and favourite snack."))
    its.append(mcq(T + "One more Grade 2 student chooses yogurt. Where does the new tally mark go?",
                   "Yogurt row, Grade 2", ["Yogurt row, Grade 1", "Cheese row, Grade 2", "A new row"],
                   "Find the Yogurt row. Then go across to the Grade 2 column. Add one mark there."))
    # mitts or gloves
    M = fig(two_way_svg("Mitts or gloves?", "We wear", ["Mitts", "Gloves"], ["Grade 1", "Grade 2"], [[14, 5], [8, 11]],
                        "two-way tally table: mitts or gloves"))
    its.append(mcq(M + "How many students wear mitts?", fmt(22, STU), [fmt(x, STU) for x in [14, 20, 16]],
                   "Add the Mitts row: Grade 1 has 14 and Grade 2 has 8. 14 + 8 = 22. "
                   "(20 counts each group of 5 as 4. 16 is the Gloves row.)"))
    its.append(mcq(M + "Which sentence is true?", "In Grade 2, more wear gloves.",
                   ["In Grade 1, more wear gloves.", "Most students wear gloves.", "Grade 2 has 20 students."],
                   "Grade 2: gloves 11 and mitts 8. 11 is more than 8, so this is true. "
                   "In Grade 1, mitts (14) is more than gloves (5). Mitts 22 is more than gloves 16. "
                   "Grade 2 has 8 + 11 = 19 students."))
    its.append(mcq(M + "How many fewer Grade 1 students wear gloves than mitts?", fmt(9, STU),
                   [fmt(x, STU) for x in [19, 5, 11]],
                   "Grade 1: mitts 14, gloves 5. How many fewer means take away: 14 − 5 = 9. "
                   "(19 adds them. 11 is the Grade 2 box.)"))
    its.append(mcq(fig(tally_only_svg(13)) + "Owen says these tally marks show 11. They show 13. What did he do wrong?",
                   "He counted each 5 as 4.", ["He missed a group of 5.", "He added 2 extra marks.", "He counted by 10s."],
                   "Each group has 4 lines and 1 line across, so it is 5. Owen counted 4 + 4 + 3 = 11. "
                   "The right way: 5 + 5 + 3 = 13."))
    its.append(mcq("Sofia counts 14 votes for hockey. How should she draw the tally marks?",
                   "2 groups of 5 and 4 marks", ["1 group of 5 and 9 marks", "3 groups of 5 and 1 mark",
                                                 "14 groups of 5"],
                   "14 = 5 + 5 + 4. Draw 2 groups of 5 and 4 single marks. When you get to the fifth mark, "
                   "draw it across the other four."))
    its.append(mcq("A two-way tally table shows that 9 Grade 1 students and 7 Grade 2 students like hockey. "
                   "6 Grade 1 students and 8 Grade 2 students like skating. How many students like skating?",
                   fmt(14, STU), [fmt(x, STU) for x in [16, 30, 2]],
                   "Skating: 6 in Grade 1 and 8 in Grade 2. 6 + 8 = 14. (16 is the hockey row.)"))
    its.append(mcq("Use the same table: 9 Grade 1 and 7 Grade 2 students like hockey, and 6 Grade 1 and 8 Grade 2 "
                   "students like skating. How many Grade 2 students are in the table?",
                   fmt(15, STU), [fmt(x, STU) for x in [16, 14, 30]],
                   "Grade 2: 7 like hockey and 8 like skating. 7 + 8 = 15. "
                   "(16 and 14 add a row, not the Grade 2 column.)"))
    assert len(its) == 20
    return {"title": "Two-way tally tables", "items": its}


# ------------------------------------------------------------ set 3: pictographs and line plots (one-to-one)
def set_picture(rnd):
    its = []
    sc, sv = ["Winter", "Spring", "Summer", "Fall"], [6, 4, 9, 5]
    P1 = fig(pic_svg("Favourite season", sc, sv, "star", STU, source="Source: Grade 2 class vote"))
    its.append(mcq(P1 + "How many students chose fall?", fmt(5, STU), [fmt(x, STU) for x in [4, 6, 9]],
                   "Each star = 1 student. Touch each star in the Fall row and count: 1, 2, 3, 4, 5. So 5 students."))
    its.append(mcq(P1 + "Which season did the most students choose?", "Summer", ["Winter", "Fall", "Spring"],
                   "The stars line up, so the longest row has the most. Summer has 9 stars."))
    its.append(mcq(P1 + "Which row shows 6 students?", "Winter", ["Fall", "Summer", "Spring"],
                   "Count the stars in each row: winter 6, spring 4, summer 9, fall 5. Winter has 6."))
    its.append(mcq(P1 + "How many more students chose summer than spring?", fmt(5, STU),
                   [fmt(x, STU) for x in [13, 9, 4]],
                   "Summer 9, spring 4. How many more means take away: 9 − 4 = 5. (13 adds them.)"))
    its.append(mcq(P1 + "How many students voted altogether?", fmt(24, STU), [fmt(x, STU) for x in [23, 4, 25]],
                   "Add every row: 6 + 4 + 9 + 5 = 24. (4 is the number of rows, not students.)"))
    bc, bv = ["Chickadee", "Blue jay", "Cardinal", "Junco"], [7, 3, 5, 8]
    P2 = fig(pic_svg("Birds at our feeder", bc, bv, "circle", B, source="Source: our class bird count"))
    its.append(mcq(P2 + "How many fewer blue jays than juncos did the class see?", fmt(5, B),
                   [fmt(x, B) for x in [11, 3, 8]],
                   "Juncos 8, blue jays 3. How many fewer means take away: 8 − 3 = 5. (11 adds them.)"))
    its.append(mcq(P2 + "How many chickadees and cardinals did the class see altogether?", fmt(12, B),
                   [fmt(x, B) for x in [2, 7, 13]],
                   "Chickadees 7, cardinals 5. Altogether means add: 7 + 5 = 12. (2 takes away.)"))
    its.append(mcq(P2 + "The class saw 6 sparrows. How many circles should go in a new Sparrow row?", "6 circles",
                   ["1 circle", "5 circles", "7 circles"],
                   "The key says each circle = 1 bird. 6 sparrows need 6 circles, one for each bird."))
    its.append(mcq(fig(uneven_svg()) + "Which sport got more votes?", "Skating",
                   ["Hockey", "They are the same", "You cannot tell"],
                   "Count, do not look at the length. Hockey has 5 circles and skating has 7. "
                   "The hockey row looks longer only because its circles are big and far apart. "
                   "In a good pictograph, all symbols are the same size and line up."))
    its.append(mcq("Leah makes a pictograph. 5 students chose skating, but the Skating row has 4 stars. "
                   "What should she do?", "Draw 1 more star", ["Draw 5 more stars", "Take away 1 star",
                                                              "Make the stars bigger"],
                   "Each star stands for 1 student, so 5 students need 5 stars. 5 − 4 = 1. She needs 1 more star."))
    # line plot: teeth lost
    tc = [2, 4, 6, 5, 3, 1]
    L1 = fig(plot_svg("Teeth we have lost", 0, tc, "Number of teeth lost", "line plot: teeth we have lost"))
    its.append(mcq(L1 + "How many students have lost 3 teeth?", fmt(5, STU), [fmt(x, STU) for x in [3, 6, 4]],
                   "Find 3 on the number line. Count the X’s above it: 5. Each X is 1 student. "
                   "(3 is the number of teeth, not the number of students.)"))
    its.append(mcq(L1 + "How many students are shown on the line plot?", fmt(21, STU), [fmt(x, STU) for x in [15, 6, 20]],
                   "Each X is one student. Count all the X’s: 2 + 4 + 6 + 5 + 3 + 1 = 21. "
                   "(15 adds the numbers 0 + 1 + 2 + 3 + 4 + 5 under the line.)"))
    its.append(mcq(L1 + "How many students have lost more than 3 teeth?", fmt(4, STU), [fmt(x, STU) for x in [9, 3, 2]],
                   "More than 3 means 4 or 5 teeth: 3 + 1 = 4 students. Do not count the students above 3. "
                   "(9 adds the 5 students who lost exactly 3.)"))
    its.append(mcq(L1 + "What number of teeth lost is the most common?", "2 teeth", ["6 teeth", "5 teeth", "3 teeth"],
                   "The tallest stack of X’s is above 2. It has 6 X’s. So 2 teeth is the most common. "
                   "(6 is how many students, and 5 is the biggest number on the line.)"))
    # line plot: pets
    pc = [4, 7, 5, 2, 1]
    L2 = fig(plot_svg("Pets we have", 0, pc, "Number of pets", "line plot: pets we have"))
    its.append(mcq(L2 + "How many students have 2 pets?", fmt(5, STU), [fmt(x, STU) for x in [2, 4, 7]],
                   "Find 2 on the number line and count the X’s above it: 5 students."))
    its.append(mcq(L2 + "How many students have 1 pet or 2 pets?", fmt(12, STU), [fmt(x, STU) for x in [3, 7, 11]],
                   "1 pet: 7 X’s. 2 pets: 5 X’s. 7 + 5 = 12. (3 adds the numbers 1 + 2 on the line.)"))
    its.append(mcq(L2 + "How many more students have 1 pet than 3 pets?", fmt(5, STU), [fmt(x, STU) for x in [9, 2, 7]],
                   "1 pet: 7 students. 3 pets: 2 students. 7 − 2 = 5. (2 takes away the numbers on the line: 3 − 1.)"))
    its.append(mcq(L2 + "Kai asks 6 more students. Each of them has 3 pets. How many X’s will be above 3 now?", 8,
                   [6, 9, 3],
                   "There are 2 X’s above 3 now. Add one X for each new student: 2 + 6 = 8."))
    its.append(mcq(L1 + "In this line plot, what does each X stand for?", "One student",
                   ["One tooth", "Two students", "The number 1"],
                   "The line plot shows how many teeth each student has lost. Each X is one student, "
                   "put above the number of teeth that student lost."))
    its.append(mcq("Owen makes a line plot of the letters in his friends’ names: Liam 4, Emma 4, Kai 3, Zoe 3, "
                   "Owen 4, Mateo 5. How many X’s go above 4?", 3, [4, 6, 2],
                   "Liam, Emma and Owen have 4 letters. That is 3 names, so 3 X’s go above 4. "
                   "(4 is the number on the line, and 6 is all the names.)"))
    assert len(its) == 20
    return {"title": "Pictographs and line plots (1 picture = 1)", "items": its}


# ------------------------------------------------------------ set 4: bar graphs (scale of 1) and the mode
MATCH_WHY = {"swap": "two bars are the wrong way round", "high": "one bar is 1 too tall", "low": "one bar is 1 too short"}


def set_bar(rnd):
    its = []
    wc, wv = ["Hockey", "Skating", "Sledding", "Skiing"], [8, 6, 11, 4]
    W1 = fig(bar_svg("Favourite winter sport", "Sport", "Students", wc, wv, "bar graph: favourite winter sport",
                     source="Source: Grade 2 class vote", top_v=12))
    its.append(mcq(W1 + "What does the scale on this bar graph count by?", "1s", ["2s", "5s", "10s"],
                   "Read the numbers up the side: 0, 1, 2, 3 … Each line is 1 more, so the scale counts by 1s."))
    its.append(mcq(W1 + "How many students chose hockey?", fmt(8, STU), [fmt(x, STU) for x in [7, 9, 11]],
                   "Go to the top of the Hockey bar, then across to the scale. It ends on the line for 8."))
    its.append(mcq(W1 + "Which bar shows 6 students?", "Skating", ["Hockey", "Skiing", "Sledding"],
                   "Find 6 on the scale and go across. The Skating bar ends on the line for 6."))
    its.append(mcq(W1 + "How many more students chose sledding than skiing?", fmt(7, STU),
                   [fmt(x, STU) for x in [15, 11, 6]],
                   "Sledding 11, skiing 4. How many more means take away: 11 − 4 = 7. (15 adds them.)"))
    its.append(mcq(W1 + "What is the mode of this data?", "Sledding", ["11", "Hockey", "Skiing"],
                   "The mode is the answer chosen most often. The tallest bar is Sledding, so the mode is sledding. "
                   "11 is how many students chose it. 11 is not the mode."))
    its.append(mcq(W1 + "How many students voted altogether?", fmt(29, STU), [fmt(x, STU) for x in [11, 4, 28]],
                   "Read every bar: 8, 6, 11 and 4. 8 + 6 + 11 + 4 = 29. (4 is the number of bars.)"))
    fc, fv = ["Apple", "Banana", "Grapes", "Orange"], [7, 5, 7, 3]
    F = fig(bar_svg("Favourite fruit", "Fruit", "Students", fc, fv, "bar graph: favourite fruit",
                    source="Source: class survey", top_v=8))
    its.append(mcq(F + "What is the mode of this data?", "Apple and grapes", ["Apple", "7", "Orange"],
                   "Apple and grapes both have 7 votes, the most. Two bars are tallest and the same height, "
                   "so this data has two modes: apple and grapes."))
    its.append(mcq(F + "How many fewer students chose orange than banana?", fmt(2, STU), [fmt(x, STU) for x in [8, 3, 4]],
                   "Banana 5, orange 3. How many fewer means take away: 5 − 3 = 2. (8 adds them.)"))
    its.append(mcq("Kai scored these goals in 5 hockey games: 4, 1, 4, 6, 2. What is the mode?", 4, [6, 2, 5],
                   "The mode is the number that appears most often. 4 appears two times. The other numbers appear "
                   "once. The mode is 4. (6 is the biggest number, not the mode.)"))
    its.append(mcq("Mitts lost at recess each day: 3, 5, 2, 5, 3, 1. What is the mode?", "3 and 5",
                   ["5", "3", "2"],
                   "3 appears two times and 5 appears two times. No number appears more often. "
                   "So there are two modes: 3 and 5."))
    its.append(mcq("Which set of data has <b>no</b> mode?", "2, 4, 6, 8", ["2, 4, 4, 8", "1, 1, 3, 5", "6, 3, 6, 3"],
                   "In 2, 4, 6, 8 every number appears only once, so there is no mode. "
                   "2, 4, 4, 8 has mode 4. 1, 1, 3, 5 has mode 1. 6, 3, 6, 3 has two modes, 3 and 6."))
    its.append(mcq("Which set of data has a mode of 6?", "6, 2, 6, 9", ["2, 6, 9, 9", "1, 6, 3, 1", "9, 8, 6, 8"],
                   "In 6, 2, 6, 9 the number 6 appears two times, so the mode is 6. "
                   "The others have modes 9, 1 and 8."))
    an = fig(bar_svg("", "Animal", "Votes", ["Beaver", "Moose", "Loon", "Bear"], [8, 5, 9, 6],
                     "bar graph with no title", source="Source: Grade 2 class vote", top_v=10))
    its.append(mcq(an + "A good bar graph has a title, labels, a scale and a source. What is missing here?",
                   "A title", ["A scale", "Labels", "A source"],
                   "There is a scale (0, 1, 2 …), labels (Animal and Votes) and a source under the graph. "
                   "There is no title at the top. A good title is “Favourite Canadian animal”."))
    its.append(mcq(W1 + "Where did the data in this bar graph come from?", "A Grade 2 class vote",
                   ["The scale", "A weather report", "The title"],
                   "The source is written under the graph: “Source: Grade 2 class vote”. "
                   "The source tells where the data came from."))
    # table -> bar graph (A to D)
    pc, pv = ["Dog", "Cat", "Fish", "Bird"], [6, 4, 2, 3]
    order = [("high", [6, 5, 2, 3]), ("swap", [6, 4, 3, 2]), ("ok", pv), ("low", [5, 4, 2, 3])]
    assert len({tuple(v) for _, v in order}) == 4
    g = panel_svg([(lambda x0, y0, v=v: mini_bar(x0, y0, pc, v, 7)) for _, v in order], "bar graphs: pets in our class")
    why = "; ".join("%s: %s" % ("ABCD"[k], MATCH_WHY[t]) for k, (t, v) in enumerate(order) if t != "ok")
    its.append(mcq_fixed(fig(g) + "<b>Pets in our class</b>: dog 6, cat 4, fish 2, bird 3. "
                         "Which bar graph shows this data?", ["A", "B", "C", "D"], 2,
                         "Check each bar against the numbers: dog 6, cat 4, fish 2, bird 3. C matches every number. "
                         + why + "."))
    ac, av = ["Noah", "Emma", "Aiden", "Zoe"], [9, 12, 7, 10]
    AP = fig(bar_svg("Apples we picked", "Student", "Apples", ac, av, "bar graph: apples we picked",
                     source="Source: field trip tally sheet", top_v=12))
    lst = lambda vs: ", ".join(str(v) for v in vs)
    its.append(mcq(AP + "Which list matches the bar graph? The order is Noah, Emma, Aiden, Zoe.", lst(av),
                   [lst([12, 9, 7, 10]), lst([v + 1 for v in av]), lst([9, 12, 10, 7])],
                   "Read each bar against the scale: Noah 9, Emma 12, Aiden 7, Zoe 10."))
    its.append(mcq(AP + "How many apples did Noah and Zoe pick altogether?", fmt(19, ("apple", "apples")),
                   [fmt(x, ("apple", "apples")) for x in [1, 18, 20]],
                   "Noah 9, Zoe 10. Altogether means add: 9 + 10 = 19. (1 takes away.)"))
    its.append(mcq(AP + "How many more apples did Emma pick than Aiden?", fmt(5, ("apple", "apples")),
                   [fmt(x, ("apple", "apples")) for x in [19, 12, 4]],
                   "Emma 12, Aiden 7. How many more means take away: 12 − 7 = 5. (19 adds them.)"))
    its.append(mcq(AP + "Zoe picks 3 more apples. Where will the top of her bar be now?", "At 13",
                   ["At 3", "At 10", "At 12"],
                   "Zoe’s bar is at 10 now. 3 more: 10 + 3 = 13. (The scale would need to go up to 13.)"))
    its.append(mcq("Every bar in a bar graph is the same height. What is the mode?", "There is no mode",
                   ["The first bar", "The last bar", "All the bars"],
                   "The mode is the answer that appears most often. If every answer appears the same number of times, "
                   "no answer is chosen more often, so there is no mode."))
    assert len(its) == 20
    return {"title": "Bar graphs (scale of 1) and the mode", "items": its}


# ------------------------------------------------------------ set 5: questions and conclusions
def set_words(rnd):
    its = []
    tc, tv = ["Walk", "Bus", "Car", "Bike"], [9, 12, 7, 3]
    TR = fig(bar_svg("How we get to school", "Way to school", "Students", tc, tv, "bar graph: how we get to school",
                     source="Source: survey in Ms. Lee’s class", top_v=12))
    its.append(mcq(TR + "How many students are in this survey?", fmt(31, STU), [fmt(x, STU) for x in [12, 4, 30]],
                   "Each student answered once. Add every bar: 9 + 12 + 7 + 3 = 31. "
                   "(12 is only the tallest bar. 4 is the number of bars.)"))
    its.append(mcq(TR + "Which sentence is true?", "More students walk than come by car.",
                   ["Bike is the mode.", "The bus has 2 more students than walk.", "Half of the class walks."],
                   "Walk 9 and car 7: 9 is more than 7, so this is true. The mode is bus (the tallest bar). "
                   "Bus has 12 − 9 = 3 more, not 2. 9 is not half of 31."))
    its.append(mcq(TR + "The school wants fewer cars. If 4 car students start to walk, how many students will walk?",
                   fmt(13, STU), [fmt(x, STU) for x in [3, 9, 16]],
                   "9 students walk now. 4 more will walk: 9 + 4 = 13. (3 is how many will still come by car.)"))
    its.append(mcq(TR + "What question did the class ask?", "How do you get to school?",
                   ["How far is the school?", "What is your favourite car?", "How many buses are there?"],
                   "The bars are ways to get to school: walk, bus, car and bike. Each student answered "
                   "“How do you get to school?”"))
    its.append(mcq(TR + "Arjun says, “Most students in Canada take the bus to school.” Is he right?",
                   "No. The data is from one class.", ["Yes. Bus has the tallest bar.", "Yes. 12 students take the bus.",
                                                      "No. Walk has the tallest bar."],
                   "The source says the data is from Ms. Lee’s class. It tells us about this class only, "
                   "not every student in Canada."))
    dc, dv = ["Pumpkin pie", "Apple pie", "Butter tarts", "Ice cream"], [8, 6, 4, 6]
    D = fig(pic_svg("Favourite Thanksgiving dessert", dc, dv, "circle", STU, source="Source: Grade 2 class vote"))
    its.append(mcq(D + "The class will make one dessert. Which one will make the most students happy?", "Pumpkin pie",
                   ["Apple pie", "Butter tarts", "Ice cream"],
                   "Pumpkin pie has the longest row: 8 students. It is the mode, so most students will be happy with it."))
    its.append(mcq(D + "How many students did <b>not</b> choose pumpkin pie?", fmt(16, STU),
                   [fmt(x, STU) for x in [8, 24, 10]],
                   "Add the other rows: 6 + 4 + 6 = 16. (24 is everyone. 10 forgets the apple pie row.)"))
    its.append(mcq(D + "5 more students vote for butter tarts. What is the mode now?", "Butter tarts",
                   ["Pumpkin pie", "9", "Apple pie"],
                   "Butter tarts now has 4 + 5 = 9 votes. 9 is more than 8 (pumpkin pie), "
                   "so butter tarts is the new mode."))
    lc = [1, 3, 4, 5, 3, 2]
    LP = fig(plot_svg("Laps we ran at the Terry Fox Run", 3, lc, "Number of laps", "line plot: laps at the terry fox run"))
    its.append(mcq(LP + "What is the mode of this data?", "6 laps", ["5 laps", "8 laps", "4 laps"],
                   "The tallest stack of X’s is above 6. So 6 laps is the mode. "
                   "(5 is how many students ran 6 laps. 8 is the biggest number.)"))
    its.append(mcq(LP + "How many students ran more than 6 laps?", fmt(5, STU), [fmt(x, STU) for x in [10, 3, 2]],
                   "More than 6 means 7 or 8 laps: 3 + 2 = 5 students. (10 also counts the students who ran 6.)"))
    its.append(mcq(LP + "The goal was at least 5 laps. How many students ran fewer than 5 laps?", fmt(4, STU),
                   [fmt(x, STU) for x in [8, 3, 1]],
                   "Fewer than 5 means 3 or 4 laps: 1 + 3 = 4 students. (8 also counts the students who ran 5.)"))
    its.append(mcq(LP + "How many students ran 4 or 5 laps?", fmt(7, STU), [fmt(x, STU) for x in [9, 4, 1]],
                   "4 laps: 3 X’s. 5 laps: 4 X’s. 3 + 4 = 7. (9 adds the numbers 4 + 5 on the line.)"))
    its.append(mcq("Mei wants to find out the favourite fruit of her class. Which question should she ask?",
                   "What is your favourite fruit?", ["Do you like apples?", "How many fruits are there?",
                                                     "What fruit is red?"],
                   "Her question must ask each student for their favourite fruit. "
                   "“Do you like apples?” only tells her about apples."))
    its.append(mcq("Ethan wants to know which birds come to the school feeder. What is the best way to collect the data?",
                   "Watch the feeder and tally", ["Ask friends their favourite bird", "Count the trees",
                                                   "Read a book about birds"],
                   "He can find out by watching. He makes one tally mark for each bird he sees at the feeder. "
                   "A favourite bird is not the same as a bird that comes to the feeder."))
    its.append(mcq("Kai asks 10 Grade 1 students and 10 Grade 2 students, “Do you like snow?” 8 Grade 1 students and "
                   "6 Grade 2 students say yes. How many students say no?", fmt(6, STU), [fmt(x, STU) for x in [14, 2, 4]],
                   "20 students answered. 8 + 6 = 14 say yes. 20 − 14 = 6 say no. "
                   "(Grade 1: 10 − 8 = 2. Grade 2: 10 − 6 = 4. 2 + 4 = 6.)"))
    its.append(mcq("For the food drive, Zoe’s class collected 15 cans in week 1, 22 cans in week 2 and 30 cans in "
                   "week 3. How many cans did they collect?", fmt(67, ("can", "cans")),
                   [fmt(x, ("can", "cans")) for x in [37, 52, 45]],
                   "Add all three weeks. 15 + 22 = 37. Then 37 + 30 = 67 cans. "
                   "(37, 52 and 45 add only two of the weeks.)"))
    its.append(mcq("The class wanted 80 cans. They collected 67 cans. How many more cans do they need?",
                   fmt(13, ("can", "cans")), [fmt(x, ("can", "cans")) for x in [27, 147, 3]],
                   "80 − 67: count up from 67 to 70 (3), then 70 to 80 (10). 3 + 10 = 13 cans. "
                   "(27 takes 0 from 7 in the ones place instead of 7 from 0. 3 stops counting at 70.)"))
    its.append(mcq(TR + "How many more students take the bus than ride a bike?", fmt(9, STU),
                   [fmt(x, STU) for x in [15, 12, 3]],
                   "Bus 12, bike 3. How many more means take away: 12 − 3 = 9. (15 adds them.)"))
    its.append(mcq(TR + "Owen says, “Bike is the mode, because it is the shortest bar.” What is the mode?", "Bus",
                   ["Bike", "12", "Walk"],
                   "The mode is the answer chosen most often, so look for the tallest bar. "
                   "The tallest bar is Bus (12 students). The mode is bus, not the number 12."))
    its.append(mcq(TR + "This survey was done in June. The class does it again in January. "
                   "Why might fewer students ride a bike?", "Snow and ice make biking hard.",
                   ["The bus is yellow.", "The graph has a title.", "Bikes have 2 wheels."],
                   "In January, Ontario has snow and ice, so fewer students bike. When we explain data, "
                   "we think about when and where it was collected."))
    assert len(its) == 20
    return {"title": "Questions and conclusions: word problems", "items": its}


# ------------------------------------------------------------ lesson
def ex(title, q, s, a):
    return ("<div class='sn-ex'><span class='sn-ex-t'>%s</span><p class='sn-ex-q'>%s</p>"
            "<p class='sn-ex-s'>%s</p><p class='sn-ex-a'>Answer: %s</p></div>" % (title, q, s, a))


def table(head, rows, cls="sn-table"):
    h = "".join("<th>%s</th>" % x for x in head)
    b = "".join("<tr>" + "".join("<td>%s</td>" % c for c in r) + "</tr>" for r in rows)
    return "<div class='sn-tw'><table class='%s'><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>" % (cls, h, b)


def body_html():
    sp = ["Hockey", "Skating", "Sledding", "Skiing"]
    spv = [7, 4, 6, 3]
    return (
        "<h2>Ask, sort, count, show, explain</h2>"
        "<p>Data is information we collect. We can ask a question, such as “What is your favourite winter sport?”, "
        "or we can watch and count, such as birds at the feeder. "
        "Then we <b>sort</b> the data, <b>count</b> it with tally marks, <b>show</b> it in a graph, "
        "and say what it tells us.</p>"
        "<h2>Sort by two things</h2>"
        "<p>A <b>Venn diagram</b> has two circles. Things that fit both labels go in the <b>overlap</b>, "
        "where the circles cross. Things that fit neither label go outside the circles.</p>"
        "<figure class='sn-fig'>" + venn_svg("Red", "Triangles", [sh("circle", "red"), sh("square", "red")],
                                            [sh("triangle", "red")], [sh("triangle", "blue"), sh("triangle", "yellow")],
                                            [sh("circle", "blue"), sh("square", "yellow")],
                                            "venn diagram: red shapes and triangles") +
        "<figcaption>The red triangle is red and a triangle, so it goes in the overlap.</figcaption></figure>"
        "<p>A <b>Carroll diagram</b> is a table of boxes. Each thing goes in the box for its row and its column.</p>" +
        ex("Example", "Where does a blue circle go in the Venn diagram above?", "It is not red. It is not a triangle.",
           "Outside the circles") +
        "<h2>Two-way tally tables</h2>"
        "<p>A two-way tally table shows two things about each person, such as their grade and their favourite snack. "
        "Make one mark for each answer. The fifth mark goes across the other four.</p>"
        "<figure class='sn-fig'>" + two_way_svg("Favourite snack", "Snack", ["Apples", "Cheese", "Crackers"],
                                               ["Grade 1", "Grade 2"], [[6, 3, 8], [5, 9, 4]],
                                               "two-way tally table: favourite snack") +
        "<figcaption>Grade 2 cheese: 1 group of 5 and 4 more, so 9. Apples in both grades: 6 + 5 = 11.</figcaption></figure>" +
        "<h2>Pictographs and line plots</h2>"
        "<p>In Grade 2, one symbol or one X stands for one thing. Line the symbols up, all the same size, "
        "so the rows are easy to compare.</p>"
        "<figure class='sn-fig'>" + pic_svg("Favourite winter sport", sp, spv, "star", STU,
                                            source="Source: Grade 2 class vote") +
        "<figcaption>Each star = 1 student. Hockey has 7 stars, so 7 students chose hockey.</figcaption></figure>"
        "<p>A <b>line plot</b> puts an X above a number line for each answer.</p>"
        "<figure class='sn-fig'>" + plot_svg("Pets we have", 0, [4, 7, 5, 2, 1], "Number of pets",
                                             "line plot: pets we have") +
        "<figcaption>5 X’s are above 2, so 5 students have 2 pets.</figcaption></figure>" +
        "<h2>Bar graphs</h2>"
        "<p>A good bar graph has a <b>title</b>, <b>labels</b>, a <b>scale</b> and a <b>source</b> "
        "(where the data came from). In Grade 2 the scale counts by 1s. "
        "Go to the top of a bar, then across to the scale.</p>"
        "<figure class='sn-fig'>" + bar_svg("Favourite winter sport", "Sport", "Students", sp, spv,
                                            "bar graph: favourite winter sport", source="Source: Grade 2 class vote",
                                            top_v=8) +
        "<figcaption>The Sledding bar ends on 6, so 6 students chose sledding.</figcaption></figure>" +
        ex("Example", "How many more students chose hockey than skiing?", "Hockey 7, skiing 3. 7 − 3 = 4.",
           "4 more students") +
        "<h2>The mode</h2>"
        "<p>The <b>mode</b> is the answer that appears most often. In a graph, it is the tallest bar or the longest row. "
        "Data can have one mode, two modes, or no mode.</p>" +
        ex("Example", "Goals: 2, 3, 1, 3, 2, 3. What is the mode?", "3 appears three times. That is the most.", "3") +
        "<h2>Common mistakes</h2>" +
        table(["Mistake", "What to do instead"], [
            ["Counting a group of 5 tally marks as 4", "The line across is the 5th mark"],
            ["Reading one box of a two-way table for the whole row", "Add both boxes in the row"],
            ["Forgetting the overlap or the things outside the circles", "Count every part of the Venn diagram"],
            ["Adding the numbers under a line plot", "Count the X’s: each X is one answer"],
            ["Giving the biggest number as the mode", "The mode is the answer that appears most often"],
            ["Adding when the question says how many more", "How many more means take away"],
        ])
    )


FAQ = [
    {"q": "What do Grade 2 students learn about data in the Ontario math curriculum?",
     "a": "They sort data by two attributes in Venn and Carroll diagrams, organize it in two-way tally tables, and show it in pictographs, line plots and bar graphs where one symbol stands for one. They also find the mode and explain what the data tells them."},
    {"q": "What is a two-way tally table?",
     "a": "It is a tally table that shows two pieces of information at once, such as a student’s grade (columns) and favourite snack (rows). Each tally mark goes in the box where its row and column meet."},
    {"q": "What is the mode in Grade 2 math?",
     "a": "The mode is the answer or number that appears most often. Data can have one mode, two modes (a tie), or no mode when every answer appears the same number of times."},
    {"q": "What is a line plot in Grade 2?",
     "a": "A line plot shows data with an X above a number line for each answer, such as the number of teeth each student has lost. Count the X’s above a number to see how many students gave that answer."},
]


def balance(sets, rnd):
    """Move the answers of the free questions so every position is right 5 times in each set."""
    for s in sets:
        cnt, free = [0] * 4, []
        for it in s["items"]:
            if it.pop("_fix", False):
                cnt[it["a"]] += 1
            else:
                free.append(it)
        targets = []
        for p in range(4):
            assert cnt[p] <= 5, (s["title"], cnt)
            targets += [p] * (5 - cnt[p])
        rnd.shuffle(targets)
        for it, t in zip(free, targets):
            corr = it["c"][it["a"]]
            wrong = [c for k, c in enumerate(it["c"]) if k != it["a"]]
            rnd.shuffle(wrong)
            wrong.insert(t, corr)
            it["c"] = wrong
            it["a"] = t
        final = [sum(1 for it in s["items"] if it["a"] == i) for i in range(4)]
        assert final == [5, 5, 5, 5], (s["title"], final)


def gen_unit():
    rnd = random.Random(42810)
    sets = [set_sort(rnd), set_tally(rnd), set_picture(rnd), set_bar(rnd), set_words(rnd)]
    balance(sets, rnd)
    seen = set()
    for s in sets:
        assert len(s["items"]) == 20, (s["title"], len(s["items"]))
        for it in s["items"]:
            assert len(set(it["c"])) == 4, it
            assert it["e"], it
            assert it["q"].count("<svg") <= 1, it["q"]
            k = it["q"] + "|" + "|".join(sorted(it["c"]))
            assert k not in seen, it["q"]
            seen.add(k)
    return {
        "country": "ca-on", "subject": "math", "grade": "grade-2", "slug": "data-and-graphs", "sort": 10,
        "updated": UPDATED, "pdf_url": "",
        "title": "Data and Graphs: Sorting, Tally Tables, Pictographs, Line Plots and Bar Graphs",
        "seo_title": "Grade 2 Data and Graphs Worksheets: Tally Tables, Pictographs, Bar Graphs (Free, Answer Key, Ontario)",
        "short_title": "Data and graphs",
        "domain": "Data",
        "standard_code": "Grade 2: D1.3",
        "standard_url": "https://www.dcp.edu.gov.on.ca/en/curriculum/elementary-mathematics",
        "standard_text": "Display sets of data, using one-to-one correspondence, in concrete graphs, pictographs, line plots, and bar graphs with proper sources, titles, and labels",
        "meta_desc": "Free Grade 2 math worksheets on data and graphs for the Ontario curriculum: sort in Venn and Carroll diagrams, two-way tally tables, pictographs and line plots, bar graphs with a scale of 1, and the mode. 100 questions with an answer key.",
        "key_big": "One symbol, one X or one tally mark stands for one answer. Count carefully, then compare.",
        "key_sub": "A group of tally marks is 5, not 4. In a Venn diagram, count the overlap and the things outside the circles. The mode is the answer that appears most often, not the biggest number.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }


def mark_large(u, pattern):
    """Tag pictures that must print larger (graphs, tables, diagrams, A to D panels) so their labels stay readable."""
    rx = re.compile(r"<svg (?=[^>]*aria-label='" + pattern + ")")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u


if __name__ == "__main__":
    u = gen_unit()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        mark_large(u, "(pictograph|bar graph|two-way|four sets|venn|carroll|line plot)")
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
