# -*- coding: utf-8 -*-
"""
Canada (Ontario) Grade 2 Math: Probability (Ontario Mathematics Curriculum 2020: Grade 2, D2.1)
  python3 tools/gen_caon_math_g2_probability.py
Everyday events, bags and spinners, which is more likely, complementary events (it will rain / it will not rain),
and predictions and decisions. The Grade 2 words: impossible, possible, certain (and more likely / less likely).
In this unit "possible" means "it might happen, or it might not" (not certain).
Wrong answers come from real student mistakes: possible confused with certain (it happens a lot, so it is certain),
"only a few, so impossible", ignoring how many of each colour, counting sections instead of looking at their size,
choosing a favourite colour, taking "not red" as just one other colour, and "tails is due" thinking.
Every picture shows the colour as a letter too (R = red ...), so it still works when printed in black and white.
Grade 2: short sentences for 7-8 year olds, a picture in many questions, numbers to 100.
HTML attributes use single quotes (no backslashes in the JSON). Canadian English.
"""
import json, re, math, os, random

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "ca-on", "math", "grade-2")
UPDATED = "2026-11-02"
GREEN = "#006633"
FILL = "#cfe6d6"
FILL2 = "#e6f2ea"
INK = "#2b2b2b"
SKY = "#dceefb"
FONT = "Arial, Helvetica, sans-serif"

# colour name -> (letter, fill)
COL = {
    "red": ("R", "#f28b82"),
    "blue": ("B", "#8ab4f8"),
    "yellow": ("Y", "#fde293"),
    "green": ("G", "#81c995"),
    "purple": ("P", "#c58af9"),
}
WORDS3 = ["impossible", "possible", "certain"]

# ------------------------------------------------------------ helpers
def mcq(q, correct, cands, e):
    """4 choices: correct + 3 unique distractors from real mistakes. Positions are balanced later."""
    correct = str(correct)
    seen = {correct}
    pick = []
    for c in cands:
        c = str(c)
        if c in seen or not c:
            continue
        seen.add(c)
        pick.append(c)
        if len(pick) == 3:
            break
    assert len(pick) == 3, (q, correct, cands)
    return {"q": q, "c": pick + [correct], "a": 3, "e": e}


def mcq_fixed(q, choices, ai, e):
    """Choices keep their order. The answer position is not moved later."""
    assert len(set(choices)) == 4 and 0 <= ai < 4
    return {"q": q, "c": list(choices), "a": ai, "e": e, "_fix": True}


def abcd_q(q, kind, ai, e):
    return mcq_fixed(q, ["%s %s" % (kind, L) for L in "ABCD"], ai, e)


def fig(svg):
    return "<div class='qfig'>" + svg + "</div>"


def svg_wrap(w, h, body, label):
    return ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 %d %d' width='%d' height='%d' "
            "role='img' aria-label='%s'><g font-family='%s'>%s</g></svg>" % (w, h, w, h, label.replace("'", "’"), FONT, body))


def tw(t, fs, bold=False):
    """Approximate text width in px (Arial)."""
    return len(str(t)) * fs * (0.62 if bold else 0.58)


def text(x, y, t, fs=14, anchor="middle", bold=False, col=INK, extra=""):
    return ("<text x='%.1f' y='%.1f' font-size='%d'%s fill='%s' text-anchor='%s'%s>%s</text>"
            % (x, y, fs, " font-weight='700'" if bold else "", col, anchor, extra, t))


def eq(*labels):
    """Equal sections."""
    return [(str(l), 1) for l in labels]


def amounts(sectors):
    out = {}
    for lab, u in sectors:
        out[lab] = out.get(lab, 0) + u
    return out


def colours_in(items):
    seen = []
    for c in items:
        if c in COL and c not in seen:
            seen.append(c)
    return seen


# ------------------------------------------------------------ spinner
def spinner_body(cx, cy, R, sectors, fs):
    """sectors = [(colour name or number, size)] clockwise from the top. Returns SVG parts."""
    T = sum(u for _, u in sectors)
    s = []
    if len(sectors) == 1:
        lab = sectors[0][0]
        fill = COL[lab][1] if lab in COL else "#ffffff"
        s.append("<circle cx='%.1f' cy='%.1f' r='%d' fill='%s' stroke='%s' stroke-width='2'/>" % (cx, cy, R, fill, INK))
        s.append(text(cx, cy - R * 0.55 + fs * 0.35, COL[lab][0] if lab in COL else lab, fs, bold=True))
    else:
        a0 = -math.pi / 2
        for i, (lab, u) in enumerate(sectors):
            a1 = a0 + 2 * math.pi * u / T
            if lab in COL:
                fill, txt = COL[lab][1], COL[lab][0]
            else:
                fill, txt = (FILL if i % 2 == 0 else "#ffffff"), lab
            x0, y0 = cx + R * math.cos(a0), cy + R * math.sin(a0)
            x1, y1 = cx + R * math.cos(a1), cy + R * math.sin(a1)
            large = 1 if (a1 - a0) > math.pi else 0
            s.append("<path d='M%.1f %.1f L%.1f %.1f A%d %d 0 %d 1 %.1f %.1f Z' fill='%s' stroke='%s' stroke-width='1.5'/>"
                     % (cx, cy, x0, y0, R, R, large, x1, y1, fill, INK))
            am = (a0 + a1) / 2
            rr = R * 0.66
            s.append(text(cx + rr * math.cos(am), cy + rr * math.sin(am) + fs * 0.35, txt, fs, bold=True))
            a0 = a1
        s.append("<circle cx='%.1f' cy='%.1f' r='%d' fill='none' stroke='%s' stroke-width='2'/>" % (cx, cy, R, INK))
    # arrow (points to the upper right, short so it never covers a letter)
    ang = math.radians(-35)
    L = R * 0.40
    tx, ty = cx + L * math.cos(ang), cy + L * math.sin(ang)
    s.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='3'/>" % (cx, cy, tx, ty, INK))
    h1 = ang + math.radians(150)
    h2 = ang - math.radians(150)
    s.append("<polygon points='%.1f,%.1f %.1f,%.1f %.1f,%.1f' fill='%s'/>" % (
        tx + 3 * math.cos(ang), ty + 3 * math.sin(ang), tx + 8 * math.cos(h1), ty + 8 * math.sin(h1),
        tx + 8 * math.cos(h2), ty + 8 * math.sin(h2), INK))
    s.append("<circle cx='%.1f' cy='%.1f' r='4' fill='%s'/>" % (cx, cy, INK))
    return s


def key_lines(cols):
    return ["%s = %s" % (COL[c][0], c) for c in cols]


def spinner_svg(sectors, label="spinner"):
    R, pad = 62, 6
    cx, cy = pad + R, pad + R
    s = spinner_body(cx, cy, R, sectors, 16)
    cols = colours_in([l for l, _ in sectors])
    W = 2 * R + 2 * pad
    if cols:
        kx = 2 * R + 2 * pad + 12
        lines = key_lines(cols)
        y0 = cy - (len(lines) - 1) * 11 + 5
        for i, ln in enumerate(lines):
            s.append(text(kx, y0 + i * 22, ln, 15, anchor="start"))
        W = int(kx + max(tw(l, 15) for l in lines) + 6)
    H = 2 * R + 2 * pad
    return svg_wrap(W, H, "".join(s), label)


def spinners_abcd(spins, label="spinners A to D"):
    R, cw = 42, 104
    cy = 6 + R
    s = []
    allc = []
    for i, sec in enumerate(spins):
        cx = cw / 2 + i * cw
        s += spinner_body(cx, cy, R, sec, 14)
        s.append(text(cx, cy + R + 20, "Spinner " + "ABCD"[i], 15, bold=True))
        allc += [l for l, _ in sec]
    W = cw * 4
    H = cy + R + 26
    cols = colours_in(allc)
    if cols:
        s.append(text(W / 2, H + 14, "\u2003\u2003".join(key_lines(cols)), 14))
        H += 22
    return svg_wrap(W, H, "".join(s), label)


# ------------------------------------------------------------ bag of counters
def bag_items(counts, rnd):
    items = []
    for c, n in counts:
        items += [c] * n
    rnd.shuffle(items)
    return items


def bag_body(x, y, items, cols, r, gap, fs):
    """A drawstring bag with counters in it. (x, y) = top left of the neck area. Returns (parts, w, h)."""
    rows = (len(items) + cols - 1) // cols
    bw = cols * gap + 16
    bh = rows * gap + 16
    top = y + 14
    s = []
    # neck and tie
    s.append("<path d='M%.1f %.1f L%.1f %.1f L%.1f %.1f L%.1f %.1f Z' fill='#f4efe4' stroke='%s' stroke-width='1.5'/>"
             % (x + bw / 2 - 14, y, x + bw / 2 + 14, y, x + bw / 2 + 22, top, x + bw / 2 - 22, top, INK))
    s.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='3'/>"
             % (x + bw / 2 - 16, y + 5, x + bw / 2 + 16, y + 5, INK))
    s.append("<rect x='%.1f' y='%.1f' width='%d' height='%d' rx='16' fill='#f4efe4' stroke='%s' stroke-width='2'/>"
             % (x, top, bw, bh, INK))
    for i, c in enumerate(items):
        rr, cc = divmod(i, cols)
        # centre the last row
        n_row = min(cols, len(items) - rr * cols)
        off = (cols - n_row) * gap / 2
        px = x + 8 + off + cc * gap + gap / 2
        py = top + 8 + rr * gap + gap / 2
        s.append("<circle cx='%.1f' cy='%.1f' r='%d' fill='%s' stroke='%s' stroke-width='1.2'/>" % (px, py, r, COL[c][1], INK))
        s.append(text(px, py + fs * 0.35, COL[c][0], fs, bold=True))
    return s, bw, 14 + bh


def bag_svg(counts, rnd, label="bag of counters"):
    items = bag_items(counts, rnd)
    cols = 5 if len(items) > 8 else 4
    if len(items) <= 4:
        cols = len(items)
    s, bw, bh = bag_body(4, 4, items, cols, 13, 32, 14)
    lines = key_lines(colours_in([c for c, _ in counts]))
    kx = 4 + bw + 14
    cy = 4 + 14 + (bh - 14) / 2
    y0 = cy - (len(lines) - 1) * 11 + 5
    for i, ln in enumerate(lines):
        s.append(text(kx, y0 + i * 22, ln, 15, anchor="start"))
    W = int(kx + max(tw(l, 15) for l in lines) + 6)
    H = int(max(bh + 8, y0 + (len(lines) - 1) * 22 + 10))
    return svg_wrap(W, H, "".join(s), label)


def bags_abcd(bags, rnd, label="bags A to D"):
    cw = 108
    s = []
    allc = []
    hmax = 0
    for i, counts in enumerate(bags):
        items = bag_items(counts, rnd)
        assert len(items) <= 6
        part, bw, bh = bag_body(i * cw + (cw - (3 * 28 + 16)) / 2, 4, items, 3, 12, 28, 14)
        s += part
        hmax = max(hmax, bh)
        allc += [c for c, _ in counts]
    for i in range(4):
        s.append(text(i * cw + cw / 2, 4 + hmax + 20, "Bag " + "ABCD"[i], 15, bold=True))
    W = cw * 4
    H = 4 + hmax + 26
    s.append(text(W / 2, H + 14, "\u2003\u2003".join(key_lines(colours_in(allc))), 14))
    H += 22
    return svg_wrap(W, H, "".join(s), label)


# ------------------------------------------------------------ tally chart and table
def tally_marks(x, cy, v):
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


def tally_svg(title, head, cats, vals, label="tally chart"):
    fs, rh = 15, 28
    c1 = int(max(max(tw(c, fs) for c in cats), tw(head, fs, True)) + 20)
    c2 = int(max(max(tally_width(v) for v in vals) + 24, 90))
    top = 28
    W = int(max(4 + c1 + c2 + 4, tw(title, 16, True) + 16))
    x0 = (W - c1 - c2) / 2
    s = [text(W / 2, 19, title, 16, bold=True)]
    rows = [(head, None)] + list(zip(cats, vals))
    for r, (c, v) in enumerate(rows):
        y = top + r * rh
        hd = r == 0
        s.append("<rect x='%.1f' y='%d' width='%d' height='%d' fill='%s' stroke='%s' stroke-width='1.5'/>"
                 % (x0, y, c1, rh, FILL2 if hd else "#ffffff", GREEN))
        s.append("<rect x='%.1f' y='%d' width='%d' height='%d' fill='%s' stroke='%s' stroke-width='1.5'/>"
                 % (x0 + c1, y, c2, rh, FILL2 if hd else "#ffffff", GREEN))
        s.append(text(x0 + 10, y + 19, c, fs, anchor="start", bold=hd))
        if hd:
            s.append(text(x0 + c1 + 10, y + 19, "Tally", fs, anchor="start", bold=True))
        else:
            s.append(tally_marks(x0 + c1 + 14, y + rh / 2, v))
    H = top + len(rows) * rh + 4
    return svg_wrap(W, H, "".join(s), label)


def table_svg(title, head, rows, label="table"):
    fs, rh = 15, 28
    ncol = len(head)
    cw = []
    for k in range(ncol):
        cells = [head[k]] + [str(r[k]) for r in rows]
        cw.append(int(max(tw(x, fs, True) for x in cells) + 20))
    tot = sum(cw)
    W = int(max(tot + 8, tw(title, 16, True) + 16))
    x0 = (W - tot) / 2
    top = 28
    s = [text(W / 2, 19, title, 16, bold=True)]
    for r, row in enumerate([head] + rows):
        y = top + r * rh
        x = x0
        for k, cell in enumerate(row):
            hd = r == 0 or k == 0
            s.append("<rect x='%.1f' y='%d' width='%d' height='%d' fill='%s' stroke='%s' stroke-width='1.5'/>"
                     % (x, y, cw[k], rh, FILL2 if hd else "#ffffff", GREEN))
            s.append(text(x + cw[k] / 2, y + 19, cell, fs, bold=hd))
            x += cw[k]
    H = top + (len(rows) + 1) * rh + 4
    return svg_wrap(W, H, "".join(s), label)


def cube_faces_svg():
    pips = {1: [(1, 1)], 2: [(0, 0), (2, 2)], 3: [(0, 0), (1, 1), (2, 2)], 4: [(0, 0), (2, 0), (0, 2), (2, 2)],
            5: [(0, 0), (2, 0), (1, 1), (0, 2), (2, 2)], 6: [(0, 0), (2, 0), (0, 1), (2, 1), (0, 2), (2, 2)]}
    sz, gap = 46, 12
    s = []
    for i in range(6):
        x = 4 + i * (sz + gap)
        s.append("<rect x='%d' y='4' width='%d' height='%d' rx='8' fill='#ffffff' stroke='%s' stroke-width='2'/>" % (x, sz, sz, INK))
        for (px, py) in pips[i + 1]:
            s.append("<circle cx='%.1f' cy='%.1f' r='4.5' fill='%s'/>" % (x + 11 + px * 12, 4 + 11 + py * 12, INK))
        s.append(text(x + sz / 2, 4 + sz + 20, str(i + 1), 15, bold=True))
    return svg_wrap(4 + 6 * sz + 5 * gap + 4, 4 + sz + 28, "".join(s), "the six faces of a number cube")





def word3(counts, target):
    """impossible / possible / certain for picking target from counts (dict colour -> number)."""
    n = counts.get(target, 0)
    tot = sum(counts.values())
    return "certain" if n == tot else ("impossible" if n == 0 else "possible")


def cap(s):
    return s[0].upper() + s[1:]


def st_q(q, counts, target, other, e, noun="{}"):
    """Which sentence is true? Correct: the right word for target. Wrong: the other two words for target,
    and a wrong word for another colour (a real mistake)."""
    w = word3(counts, target)
    wo = word3(counts, other)
    bad_o = {"possible": "impossible", "impossible": "possible", "certain": "impossible"}[wo]
    if wo == "possible" and counts.get(other, 0) > sum(counts.values()) / 2:
        bad_o = "certain"
    n = lambda c: cap(noun.format(c))
    correct = "%s is %s." % (n(target), w)
    cands = ["%s is %s." % (n(target), x) for x in WORDS3 if x != w] + ["%s is %s." % (n(other), bad_o)]
    return mcq(q, correct, cands, e)


def pair(a, wa, na, wn):
    return "%s is %s. %s is %s." % (a, wa, na, wn)


def pair_q(q, a, na, wa, wn, wrong, e):
    """Choices are pairs: the event and its complement. wrong = list of (wa, wn) pairs from real mistakes."""
    return mcq(q, pair(a, wa, na, wn), [pair(a, x, na, y) for x, y in wrong], e)


# ------------------------------------------------------------ everyday pictures
def sun(cx, cy, r):
    s = []
    for k in range(8):
        a = k * math.pi / 4
        s.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='#e0a800' stroke-width='2.5'/>"
                 % (cx + (r + 3) * math.cos(a), cy + (r + 3) * math.sin(a), cx + (r + 9) * math.cos(a), cy + (r + 9) * math.sin(a)))
    s.append("<circle cx='%.1f' cy='%.1f' r='%d' fill='#fde293' stroke='#e0a800' stroke-width='2'/>" % (cx, cy, r))
    return "".join(s)


def cloud(cx, cy, k=1.0, fill="#ffffff"):
    parts = [(-22, 4, 14), (0, -6, 18), (22, 4, 14)]
    s = "".join("<circle cx='%.1f' cy='%.1f' r='%.1f' fill='%s' stroke='#7a8a99' stroke-width='1.5'/>"
                % (cx + dx * k, cy + dy * k, r * k, fill) for dx, dy, r in parts)
    s += "<rect x='%.1f' y='%.1f' width='%.1f' height='%.1f' fill='%s'/>" % (cx - 22 * k, cy + 2 * k, 44 * k, 16 * k, fill)
    s += "<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='#7a8a99' stroke-width='1.5'/>" % (cx - 30 * k, cy + 18 * k, cx + 30 * k, cy + 18 * k)
    return s


def frame(W, H):
    return "<rect x='1' y='1' width='%d' height='%d' rx='8' fill='none' stroke='%s' stroke-width='2'/>" % (W - 2, H - 2, INK)


def ground(fill, y):
    return "<path d='M1 %d L159 %d L159 95 Q159 103 151 103 L9 103 Q1 103 1 95 Z' fill='%s'/>" % (y, y, fill)


def scene_svg(name):
    W, H = 160, 104
    s = []
    if name == "winter":
        s.append("<rect x='1' y='1' width='158' height='102' rx='8' fill='%s'/>" % SKY)
        s.append(ground("#ffffff", 76))
        s.append("<line x1='1' y1='76' x2='159' y2='76' stroke='#9fb3c8' stroke-width='1.5'/>")
        for cy, r in ((78, 16), (52, 12), (32, 9)):
            s.append("<circle cx='58' cy='%d' r='%d' fill='#ffffff' stroke='%s' stroke-width='1.8'/>" % (cy, r, INK))
        s.append("<circle cx='55' cy='30' r='1.6' fill='%s'/><circle cx='61' cy='30' r='1.6' fill='%s'/>" % (INK, INK))
        s.append("<path d='M58 33 L68 35 L58 36 Z' fill='#f9a03f'/>")
        s.append("<rect x='49' y='19' width='18' height='6' fill='#c0392b' stroke='%s' stroke-width='1'/>" % INK)
        for (x, y) in [(100, 20), (122, 34), (144, 18), (108, 52), (136, 56), (22, 24), (18, 56)]:
            s.append("<circle cx='%d' cy='%d' r='3' fill='#ffffff' stroke='#9fb3c8' stroke-width='1'/>" % (x, y))
        lab = "a snowy winter day with a snowman"
    elif name == "lake":
        s.append("<rect x='1' y='1' width='158' height='102' rx='8' fill='%s'/>" % SKY)
        s.append(sun(128, 26, 13))
        s.append(ground("#8ab4f8", 60))
        s.append("<path d='M30 74 L96 74 L88 84 L38 84 Z' fill='#c0392b' stroke='%s' stroke-width='1.5'/>" % INK)
        s.append("<line x1='60' y1='66' x2='76' y2='90' stroke='%s' stroke-width='2.5'/>" % INK)
        s.append("<path d='M1 60 L40 32 L70 60 Z' fill='#4f9d69' stroke='%s' stroke-width='1.2'/>" % INK)
        lab = "a sunny summer day at the lake"
    elif name == "night":
        s.append("<rect x='1' y='1' width='158' height='102' rx='8' fill='#2f3e66'/>")
        s.append("<circle cx='42' cy='34' r='18' fill='#fde293'/>")
        s.append("<circle cx='51' cy='28' r='16' fill='#2f3e66'/>")
        for (x, y) in [(90, 20), (120, 36), (140, 16), (100, 52), (70, 62), (132, 64), (20, 70)]:
            s.append("<circle cx='%d' cy='%d' r='2.5' fill='#ffffff'/>" % (x, y))
        s.append(ground("#2e5b3a", 84))
        lab = "the Moon and stars at night"
    elif name == "rain":
        s.append("<rect x='1' y='1' width='158' height='102' rx='8' fill='#e3e7ec'/>")
        s.append(cloud(80, 34, 1.3, "#c4ccd6"))
        for k in range(7):
            x = 40 + k * 13
            s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='#3b78c4' stroke-width='2.5' stroke-linecap='round'/>"
                     % (x, 66 + (k % 2) * 8, x - 4, 78 + (k % 2) * 8))
        lab = "dark grey rain clouds"
    elif name == "school":
        s.append("<rect x='1' y='1' width='158' height='102' rx='8' fill='%s'/>" % SKY)
        s.append("<rect x='30' y='42' width='100' height='54' fill='#f4e2b0' stroke='%s' stroke-width='2'/>" % INK)
        s.append("<path d='M24 42 L80 16 L136 42 Z' fill='#c0392b' stroke='%s' stroke-width='2'/>" % INK)
        s.append("<rect x='70' y='68' width='20' height='28' fill='#8a5a2b' stroke='%s' stroke-width='1.5'/>" % INK)
        for x in (40, 104):
            s.append("<rect x='%d' y='54' width='16' height='14' fill='#8ab4f8' stroke='%s' stroke-width='1.5'/>" % (x, INK))
        s.append(text(80, 38, "SCHOOL", 14, bold=True, col="#ffffff"))
        lab = "a school"
    elif name == "cake":
        s.append("<rect x='1' y='1' width='158' height='102' rx='8' fill='#fdf1f4'/>")
        s.append("<rect x='38' y='56' width='84' height='38' rx='4' fill='#f7c6d0' stroke='%s' stroke-width='2'/>" % INK)
        s.append("<path d='M38 66 Q50 74 62 66 Q74 74 86 66 Q98 74 110 66 Q116 72 122 66' fill='none' stroke='#ffffff' stroke-width='4'/>")
        for k in range(7):
            x = 44 + k * 12
            s.append("<rect x='%d' y='38' width='5' height='18' fill='#8ab4f8' stroke='%s' stroke-width='1'/>" % (x - 2, INK))
            s.append("<path d='M%.1f 36 Q%.1f 28 %.1f 24 Q%.1f 28 %.1f 36 Z' fill='#f9a03f'/>" % (x - 3, x - 3, x + 0.5, x + 4, x + 4))
        s.append("<line x1='28' y1='94' x2='132' y2='94' stroke='%s' stroke-width='2.5'/>" % INK)
        lab = "a birthday cake with 7 candles"
    elif name == "calendar":
        s.append("<rect x='30' y='8' width='100' height='90' rx='6' fill='#ffffff' stroke='%s' stroke-width='2'/>" % INK)
        s.append("<rect x='30' y='8' width='100' height='28' rx='6' fill='#f28b82' stroke='%s' stroke-width='2'/>" % INK)
        s.append(text(80, 28, "Today", 16, bold=True))
        s.append(text(80, 74, "Monday", 22, bold=True))
        s.append("<rect x='52' y='3' width='6' height='12' rx='2' fill='%s'/>" % INK)
        s.append("<rect x='102' y='3' width='6' height='12' rx='2' fill='%s'/>" % INK)
        lab = "a calendar page: today is Monday"
    elif name == "egg":
        s.append("<rect x='1' y='1' width='158' height='102' rx='8' fill='#fbf7ee'/>")
        s.append("<ellipse cx='80' cy='44' rx='18' ry='24' fill='#ffffff' stroke='%s' stroke-width='2'/>" % INK)
        s.append("<line x1='80' y1='74' x2='80' y2='84' stroke='%s' stroke-width='2' stroke-dasharray='3 3'/>" % INK)
        s.append("<path d='M74 82 L80 90 L86 82' fill='none' stroke='%s' stroke-width='2'/>" % INK)
        s.append("<line x1='14' y1='94' x2='146' y2='94' stroke='%s' stroke-width='3'/>" % INK)
        lab = "an egg falling to the floor"
    elif name == "popsicle":
        s.append("<rect x='1' y='1' width='158' height='102' rx='8' fill='%s'/>" % SKY)
        s.append(sun(124, 30, 15))
        s.append("<rect x='46' y='18' width='30' height='52' rx='12' fill='#f9a03f' stroke='%s' stroke-width='2'/>" % INK)
        s.append("<rect x='57' y='70' width='8' height='24' rx='3' fill='#e9c46a' stroke='%s' stroke-width='1.5'/>" % INK)
        lab = "a popsicle in the hot sun"
    elif name == "hockey":
        s.append("<rect x='1' y='1' width='158' height='102' rx='8' fill='#eef6fb'/>")
        s.append("<line x1='80' y1='2' x2='80' y2='102' stroke='#c0392b' stroke-width='3'/>")
        s.append("<circle cx='80' cy='52' r='20' fill='none' stroke='#3b78c4' stroke-width='2'/>")
        s.append("<path d='M150 34 L132 34 L132 70 L150 70' fill='none' stroke='#c0392b' stroke-width='3'/>")
        for y in range(40, 70, 8):
            s.append("<line x1='134' y1='%d' x2='150' y2='%d' stroke='#9fb3c8' stroke-width='1'/>" % (y, y))
        s.append("<ellipse cx='36' cy='76' rx='9' ry='4' fill='%s'/>" % INK)
        s.append("<path d='M14 20 L36 66 L52 66' fill='none' stroke='#8a5a2b' stroke-width='4' stroke-linecap='round'/>")
        lab = "a hockey rink with a net, a stick and a puck"
    else:
        raise ValueError(name)
    if name != "calendar":
        s.append(frame(W, H))
    return svg_wrap(W, H, "".join(s), lab)


def coin_svg():
    s = []
    for i, (word, mark) in enumerate([("heads", "H"), ("tails", "T")]):
        cx = 46 + i * 92
        s.append("<circle cx='%d' cy='42' r='36' fill='#e9c46a' stroke='%s' stroke-width='2'/>" % (cx, INK))
        s.append("<circle cx='%d' cy='42' r='29' fill='none' stroke='%s' stroke-width='1'/>" % (cx, INK))
        s.append(text(cx, 52, mark, 28, bold=True))
        s.append(text(cx, 98, word, 16, bold=True))
    return svg_wrap(184, 106, "".join(s), "the two sides of a loonie: heads and tails")


def mitts_svg(counts, rnd, label="mitts"):
    items = bag_items(counts, rnd)
    s = []
    for i, c in enumerate(items):
        x = 6 + i * 38
        s.append("<path d='M%d 60 L%d 22 Q%d 6 %d 10 Q%d 6 %d 22 L%d 60 Z' fill='%s' stroke='%s' stroke-width='1.5'/>"
                 % (x, x, x, x + 15, x + 30, x + 30, x + 30, COL[c][1], INK))
        s.append("<path d='M%d 36 Q%d 30 %d 22 Q%d 18 %d 28 L%d 44' fill='%s' stroke='%s' stroke-width='1.5'/>"
                 % (x, x - 8, x - 4, x + 2, x + 2, x + 2, COL[c][1], INK))
        s.append("<rect x='%d' y='60' width='30' height='8' fill='#ffffff' stroke='%s' stroke-width='1.2'/>" % (x, INK))
        s.append(text(x + 16, 44, COL[c][0], 15, bold=True))
    W = 6 + len(items) * 38
    lines = key_lines(colours_in([c for c, _ in counts]))
    s.append(text(W / 2, 92, "     ".join(lines), 15))
    return svg_wrap(int(max(W + 2, tw("     ".join(lines), 15) + 8)), 100, "".join(s), label)


# ------------------------------------------------------------ set 1: everyday events
def set_everyday(rnd):
    its = []
    S = lambda n: fig(scene_svg(n))
    its.append(mcq(S("winter") + "A snowy winter day in Ottawa. Which is impossible?", "The snowman talks to you.",
                   ["You go skating.", "More snow falls.", "You see a cardinal."],
                   "A snowman cannot talk. That can never happen, so it is impossible. "
                   "The other things might happen, so they are possible."))
    its.append(mcq(S("winter") + "A snowy winter day in Ottawa. Which is possible?", "You build a snow fort.",
                   ["The snow turns hot.", "A moose drives a bus.", "The snowman walks home."],
                   "You might build a snow fort, or you might not. So it is possible. The other things can never happen."))
    its.append(mcq(S("lake") + "A hot summer day at the lake. Which is impossible?", "The lake freezes today.",
                   ["You see a loon.", "You go for a swim.", "You go in a canoe."],
                   "Water does not freeze on a hot summer day. So it is impossible. "
                   "Seeing a loon is possible: loons live on many Ontario lakes."))
    its.append(mcq(S("lake") + "A hot summer day at the lake. Which is possible?", "You see a loon.",
                   ["It snows on the lake.", "The canoe flies away.", "The lake turns into milk."],
                   "Loons live on many lakes. You might see one, or you might not. So it is possible."))
    its.append(mcq(S("night") + "It is midnight in Toronto. Which is certain?", "It is dark outside.",
                   ["You hear an owl.", "It rains.", "The sun is shining."],
                   "At midnight the sky in Toronto is always dark. That is certain. "
                   "An owl or rain might happen, so they are only possible."))
    its.append(mcq(S("night") + "Which is impossible?", "A cow jumps over the Moon.",
                   ["You see the Moon.", "You hear a dog bark.", "You read a bedtime story."],
                   "The Moon is very, very far away. A cow cannot jump that high, so it is impossible."))
    its.append(mcq(S("calendar") + "Today is Monday. Which is certain?", "Tomorrow is Tuesday.",
                   ["Tomorrow is sunny.", "Tomorrow there is gym.", "Tomorrow is Friday."],
                   "Tuesday always comes after Monday, so it is certain. A sunny day or gym class is only possible."))
    its.append(mcq(S("calendar") + "Today is Monday. Which is impossible?", "Tomorrow is Saturday.",
                   ["Tomorrow is Tuesday.", "Tomorrow is rainy.", "Tomorrow is a snow day."],
                   "The day after Monday is always Tuesday. So tomorrow being Saturday is impossible. "
                   "Tomorrow being Tuesday is certain."))
    its.append(mcq(S("cake") + "Ava is 7 today. Which is certain?", "Next year Ava will be 8.",
                   ["Ava gets a puppy.", "It rains at the party.", "Next year Ava will be 6."],
                   "Every year you get 1 year older. 7 + 1 = 8, so it is certain. You cannot get younger, so 6 is impossible."))
    its.append(mcq(S("cake") + "Ava is 7 today. Which is possible?", "Ava gets a new book.",
                   ["Ava turns 70 today.", "Ava gets younger.", "The cake sings a song."],
                   "Ava might get a book as a gift, or she might not. So it is possible. The other things can never happen."))
    its.append(mcq(S("egg") + "Lucas lets go of an egg. Which is certain?", "The egg falls down.",
                   ["The egg flies up.", "The egg turns into a chick.", "The egg floats in the air."],
                   "When you let go of something, it always falls down. So it is certain."))
    its.append(mcq(S("popsicle") + "A popsicle sits in the hot sun. Which is certain?", "It melts.",
                   ["It gets colder.", "It gets bigger.", "A bee lands on it."],
                   "The hot sun always melts ice. So it is certain. A bee landing on it is only possible."))
    its.append(mcq(S("hockey") + "Jayden’s team plays hockey today. Which is possible?", "Jayden scores a goal.",
                   ["Both teams win.", "The puck turns into a pizza.", "The ice turns into sand."],
                   "Jayden might score, or he might not. So it is possible. Both teams cannot win, so that is impossible."))
    its.append(mcq(S("hockey") + "Which is impossible?", "The puck melts into water.",
                   ["Jayden’s team wins.", "The game ends in a tie.", "Someone falls on the ice."],
                   "A puck is made of rubber. It cannot melt into water, so it is impossible. "
                   "Winning, a tie and falling are all possible."))
    its.append(mcq(S("school") + "It is a school day. Which is possible?", "You go out for recess.",
                   ["A beaver teaches math.", "The school floats away.", "You turn into a fish."],
                   "You might go out for recess. On a very rainy day, you might not. So it is possible."))
    its.append(mcq(S("rain") + "Dark clouds fill the sky. Which is possible?", "It rains today.",
                   ["It rains maple syrup.", "Rain falls up.", "The clouds turn into sheep."],
                   "Dark clouds often bring rain, but not every time. So rain is possible, not certain."))
    its.append(mcq(S("rain") + "Owen says, “Rain tomorrow is certain.” Which is better?", "Rain tomorrow is possible.",
                   ["Rain tomorrow is certain.", "Rain tomorrow is impossible.", "Rain will fall up tomorrow."],
                   "No one can be sure about rain tomorrow. It might rain, or it might not. So say possible, not certain."))
    its.append(mcq(S("winter") + "Mei says, “A snow day this winter is impossible.” Which is better?",
                   "A snow day is possible.",
                   ["A snow day is impossible.", "A snow day is certain.", "Snow will fall in July."],
                   "Ottawa gets big snowstorms. A snow day might happen, or it might not. "
                   "So it is possible, not impossible."))
    its.append(mcq("Maya rides the school bus every day. She says, “The bus will be on time tomorrow. It is certain.” "
                   "Which is better?", "It is possible.",
                   ["It is certain.", "It is impossible.", "The bus will fly."],
                   "The bus is on time most days, but snow or traffic can make it late. "
                   "So it is possible, not certain."))
    its.append(mcq("Which event is certain?", "A week has 7 days.",
                   ["It snows on Monday.", "You lose a tooth today.", "A week has 9 days."],
                   "Every week has 7 days, so it is certain. A week with 9 days is impossible."))
    assert len(its) == 20
    return {"title": "Everyday events: impossible, possible or certain?", "items": its}


# ------------------------------------------------------------ set 2: bags and spinners
def set_bags_spinners(rnd):
    its = []
    B = lambda counts: fig(bag_svg(counts, rnd))
    F = lambda sec: fig(spinner_svg(sec))
    pick = "Picking {}"
    land = "Landing on {}"
    c = {"red": 6}
    its.append(st_q(B(list(c.items())) + "You pick one counter without looking. Which is true?", c, "red", "blue",
                    "Every counter is red. You will pick red for sure, so it is certain. There is no blue, so blue is impossible.",
                    pick))
    c = {"red": 4, "blue": 3}
    its.append(st_q(B(list(c.items())) + "Which is true?", c, "blue", "red",
                    "There are blue counters, so you might pick blue. There are red counters too, so you might not. "
                    "Blue is possible.", pick))
    c = {"yellow": 5, "green": 2}
    its.append(st_q(B(list(c.items())) + "Which is true?", c, "red", "yellow",
                    "There are no red counters in the bag. You can never pick red, so it is impossible.", pick))
    sec = eq("blue", "blue", "blue", "blue")
    its.append(st_q(F(sec) + "Which is true?", amounts(sec), "blue", "red",
                    "Every section is blue. The arrow must land on blue, so it is certain.", land))
    sec = eq("red", "blue", "yellow", "green")
    its.append(st_q(F(sec) + "Which is true?", amounts(sec), "purple", "red",
                    "There is no purple section. The arrow can never land on purple, so it is impossible.", land))
    sec = eq("red", "red", "red", "blue")
    its.append(st_q(F(sec) + "There is only 1 blue section. Which is true?", amounts(sec), "blue", "red",
                    "There is 1 blue section, so the arrow might land on blue. Only 1 section does not make it impossible. "
                    "Blue is possible.", land))
    its.append(mcq(B([("red", 3), ("blue", 2), ("yellow", 1)]) + "Which colour can you never pick?", "green",
                   ["yellow", "blue", "red"],
                   "The bag has red, blue and yellow. There is no green, so green is impossible. "
                   "There is only 1 yellow, but yellow is still possible."))
    sec = eq("yellow", "yellow", "yellow", "yellow", "yellow", "yellow")
    its.append(mcq(F(sec) + "Which is certain?", "landing on yellow",
                   ["landing on red", "landing on blue", "landing on green"],
                   "Every section is yellow. The arrow must land on yellow, so it is certain."))
    its.append(abcd_q(fig(spinners_abcd([eq("red", "red", "red", "blue"), eq("red", "blue", "yellow", "green"),
                                         eq("red", "red", "red", "red"), eq("blue", "yellow", "blue", "yellow")])) +
                      "On which spinner is landing on red certain?", "Spinner", 2,
                      "Certain means it must happen. Only Spinner C is all red. On A, red is possible, "
                      "but not certain, because there is a blue section."))
    its.append(abcd_q(fig(bags_abcd([[("blue", 3), ("red", 3)], [("blue", 1), ("red", 5)],
                                     [("blue", 6)], [("red", 4), ("yellow", 2)]], rnd)) +
                      "From which bag is picking blue impossible?", "Bag", 3,
                      "Bag D has no blue counters, so blue is impossible. "
                      "Bag B has only 1 blue counter, but blue is still possible there."))
    its.append(abcd_q(fig(spinners_abcd([eq("red", "red", "red", "red"), eq("blue", "green", "blue", "green"),
                                         eq("blue", "blue", "blue", "blue"), eq("red", "blue", "red", "blue")])) +
                      "On which spinner is red possible, but not certain?", "Spinner", 3,
                      "Spinner D has red and blue sections. The arrow might land on red, or it might not. "
                      "On A, red is certain. On B and C, red is impossible."))
    its.append(abcd_q(fig(bags_abcd([[("yellow", 5), ("red", 1)], [("yellow", 6)], [("green", 3), ("yellow", 3)],
                                     [("green", 6)]], rnd)) +
                      "From which bag is picking yellow certain?", "Bag", 1,
                      "Bag B has only yellow counters, so yellow is certain. "
                      "Bag A has 1 red counter too, so yellow is possible there, not certain."))
    its.append(mcq("Mei’s bag has 4 red counters and 2 blue counters. She wants picking red to be certain. "
                   "What should she do?", "Take out the 2 blue counters.",
                   ["Take out the 4 red counters.", "Add 2 more red counters.", "Take out 1 blue counter."],
                   "Certain means every counter must be red. If the 2 blue counters come out, only red is left. "
                   "Adding red counters does not make red certain."))
    its.append(mcq("Arjun’s bag has 3 blue counters and 5 red counters. He wants picking blue to be impossible. "
                   "What should he do?", "Take out the 3 blue counters.",
                   ["Take out 1 blue counter.", "Add 5 more red counters.", "Take out the 5 red counters."],
                   "Impossible means it can never happen. With no blue counters left, blue can never be picked."))
    its.append(mcq(fig(cube_faces_svg()) + "Priya rolls a number cube. Which number is impossible to roll?", "7",
                   ["6", "1", "3"],
                   "The cube has the numbers 1 to 6. There is no 7, so rolling a 7 is impossible. "
                   "6 is not hard to roll: every number has the same chance."))
    its.append(mcq(fig(cube_faces_svg()) + "Priya rolls a number cube. Which is certain?", "rolling a number from 1 to 6",
                   ["rolling a 6", "rolling a 1", "rolling a 0"],
                   "Every face shows a number from 1 to 6. You must roll one of them, so it is certain. "
                   "Rolling a 6 is only possible."))
    c = {"blue": 5}
    its.append(st_q(fig(mitts_svg(list(c.items()), rnd, "5 blue mitts")) +
                    "Leah grabs one mitt from the box in the dark. Which is true?", c, "blue", "red",
                    "All the mitts are blue. Leah will get a blue mitt for sure, so it is certain.", "a {} mitt"))
    c = {"red": 3, "green": 3}
    its.append(st_q(fig(mitts_svg(list(c.items()), rnd, "3 red mitts and 3 green mitts")) +
                    "Leah grabs one mitt in the dark. Which is true?", c, "green", "red",
                    "There are green mitts and red mitts. She might get green, or she might not. So green is possible.",
                    "a {} mitt"))
    its.append(mcq(F(eq("1", "2", "3", "4")) + "Which is impossible?", "landing on 5",
                   ["landing on 4", "landing on 1", "landing on 2"],
                   "The spinner has only 1, 2, 3 and 4. There is no 5, so landing on 5 is impossible."))
    its.append(mcq("A bag has 10 counters. Picking red is certain. How many red counters are in the bag?", "10",
                   ["9", "1", "5"],
                   "Certain means every counter is red: all 10. With 9 red and 1 other counter, red is only possible."))
    assert len(its) == 20
    return {"title": "Bags and spinners: what can you get?", "items": its}


# ------------------------------------------------------------ set 3: which is more likely?
def set_more_likely(rnd):
    its = []
    B = lambda counts: fig(bag_svg(counts, rnd))
    F = lambda sec: fig(spinner_svg(sec))
    G = lambda bags: fig(bags_abcd(bags, rnd))
    SAME = "same chance"
    its.append(mcq(B([("red", 6), ("blue", 2)]) + "Which colour are you more likely to pick?", "red",
                   ["blue", SAME, "green"],
                   "There are 6 red counters and only 2 blue. More counters means more likely. So red is more likely."))
    its.append(mcq(B([("yellow", 1), ("green", 7)]) + "Which colour are you less likely to pick?", "yellow",
                   ["green", SAME, "both are certain"],
                   "There is only 1 yellow counter and 7 green. Fewer counters means less likely. So yellow is less likely."))
    its.append(mcq(F(eq("red", "red", "blue", "red")) + "Which colour is the arrow more likely to land on?", "red",
                   ["blue", SAME, "yellow"],
                   "3 of the 4 equal sections are red and only 1 is blue. Red is more likely."))
    its.append(mcq(F(eq("red", "blue", "red", "blue")) + "Which colour is the arrow more likely to land on?", SAME,
                   ["red", "blue", "red is certain"],
                   "There are 2 red and 2 blue sections, all the same size. Red and blue have the same chance."))
    sec = [("red", 3), ("blue", 1), ("green", 1), ("blue", 1)]
    assert amounts(sec) == {"red": 3, "blue": 2, "green": 1}
    its.append(mcq(F(sec) + "Kai says blue is more likely, because blue has 2 sections. Which is more likely, red or blue?",
                   "red", ["blue", SAME, "green"],
                   "Do not just count sections. Look at their size. The red section is half of the spinner. "
                   "The 2 blue sections are small. So red is more likely."))
    its.append(mcq(B([("green", 7), ("yellow", 2)]) + "Zoe says yellow is more likely, because yellow is her favourite colour. "
                   "Which colour is more likely?", "green", ["yellow", SAME, "red"],
                   "Your favourite colour does not change the chance. There are 7 green and 2 yellow counters, "
                   "so green is more likely."))
    its.append(mcq(B([("red", 3), ("blue", 3), ("yellow", 2)]) + "Which two colours have the same chance?",
                   "red and blue", ["red and yellow", "blue and yellow", "all three"],
                   "Count each colour: red 3, blue 3, yellow 2. Red and blue have the same number, so they have the same chance."))
    its.append(mcq(B([("yellow", 5), ("red", 2), ("green", 1)]) + "Put the colours in order from most likely to least likely.",
                   "yellow, red, green", ["green, red, yellow", "red, yellow, green", "yellow, green, red"],
                   "Count each colour: yellow 5, red 2, green 1. The most counters is most likely: yellow, red, green."))
    its.append(abcd_q(G([[("red", 1), ("blue", 5)], [("red", 3), ("blue", 3)], [("red", 5), ("blue", 1)],
                         [("red", 2), ("blue", 4)]]) +
                      "From which bag is picking red most likely?", "Bag", 2,
                      "Each bag has 6 counters. Bag C has the most red counters (5), so red is most likely there."))
    its.append(abcd_q(fig(spinners_abcd([eq("blue", "blue", "red", "blue"), eq("blue", "red", "blue", "red"),
                                         eq("red", "red", "red", "blue"), eq("blue", "blue", "blue", "blue")])) +
                      "On which spinner is blue less likely than red?", "Spinner", 2,
                      "On Spinner C, only 1 of the 4 sections is blue and 3 are red. So blue is less likely than red there."))
    assert 2 + 6 == 8 and 8 > 6
    its.append(mcq(B([("red", 6), ("green", 2)]) + "Kai puts 6 more green counters into the bag. "
                   "Which colour is now more likely?", "green", ["red", SAME, "green is impossible"],
                   "Green: 2 + 6 = 8 counters. Red: 6 counters. 8 is more than 6, so green is now more likely."))
    assert 5 - 2 == 3
    its.append(mcq(B([("red", 2), ("blue", 5)]) + "How many red counters must Zoe add to give red and blue the same chance?",
                   "3", ["5", "7", "1"],
                   "Same chance means the same number of each. Blue has 5. Red has 2. 5 − 2 = 3, so add 3 red counters."))
    its.append(mcq("It is January in Winnipeg. Which is more likely tomorrow?", "a snowy day",
                   ["a hot beach day", SAME, "neither can happen"],
                   "Winnipeg is very cold in January, and it often snows. A hot beach day in January is impossible."))
    its.append(mcq("It is a school day. Which is least likely?", "A moose walks into class.",
                   ["You read a book.", "You eat lunch.", "You go out for recess."],
                   "Reading, lunch and recess happen on most school days. A moose in class almost never happens, "
                   "so it is least likely."))
    assert 15 > 12
    its.append(mcq("Liam’s class has 15 girls and 12 boys. The teacher picks one name from a toque. "
                   "Which is more likely?", "a girl’s name", ["a boy’s name", SAME, "a girl’s name is certain"],
                   "There are 15 girls and 12 boys. 15 is more than 12, so a girl’s name is more likely. "
                   "It is not certain, because there are boys’ names too."))
    assert 14 + 5 + 1 == 20
    its.append(mcq("A prize box has 20 prizes: 14 pencils, 5 stickers and 1 toy car. Olivia picks one without looking. "
                   "Which is she least likely to get?", "the toy car", ["a pencil", "a sticker", SAME],
                   "There is only 1 toy car, so it is least likely. There are 14 pencils, so a pencil is most likely."))
    assert 9 > 3
    its.append(mcq("A box has 9 grape popsicles and 3 cherry popsicles. Owen takes one without looking. "
                   "Which is he more likely to get?", "grape", ["cherry", SAME, "orange"],
                   "There are 9 grape and 3 cherry popsicles. 9 is more than 3, so grape is more likely. "
                   "There is no orange, so orange is impossible."))
    its.append(mcq(B([("red", 4), ("blue", 4)]) + "Mateo picked red last time. He puts it back. He says red is more likely now. "
                   "Which is right?", SAME, ["red", "blue", "red is certain"],
                   "Mateo put the counter back, so there are still 4 red and 4 blue counters. "
                   "Red and blue have the same chance."))
    its.append(abcd_q(fig(spinners_abcd([eq("red", "blue", "blue", "blue"), eq("blue", "blue", "blue", "blue"),
                                         eq("red", "blue", "red", "blue"), eq("red", "red", "red", "blue")])) +
                      "Ethan wants red to be more likely than blue. Which spinner should he use?", "Spinner", 3,
                      "Spinner D has 3 red sections and 1 blue section. Red is more likely there. "
                      "On C, red and blue have the same chance."))
    assert 3 > 1 and not 4 > 6
    its.append(mcq("Bag A has 3 red and 1 blue counter. Bag B has 4 red and 6 blue counters. "
                   "In which bag is red more likely than blue?", "Bag A", ["Bag B", "both bags", "neither bag"],
                   "Compare red with blue in each bag. Bag A: 3 red, 1 blue, so red is more likely. "
                   "Bag B has more red counters, but even more blue: 4 red, 6 blue."))
    assert len(its) == 20
    return {"title": "Which is more likely?", "items": its}


# ------------------------------------------------------------ set 4: complementary events
def set_complement(rnd):
    its = []
    B = lambda counts: fig(bag_svg(counts, rnd))
    F = lambda sec: fig(spinner_svg(sec))
    its.append(mcq(fig(scene_svg("rain")) + "What is the opposite of “It will rain today”?", "It will not rain today.",
                   ["It will rain tomorrow.", "It will snow today.", "It will rain a lot today."],
                   "The opposite says it does not happen: “It will not rain today.” One of the two must happen."))
    its.append(mcq(fig(coin_svg()) + "Hana tosses a loonie. What is the opposite of “it lands on heads”?",
                   "it lands on tails", ["it lands on heads", "it lands on a 2", "it lands on heads and tails"],
                   "A coin has only 2 sides. If it does not land on heads, it lands on tails."))
    its.append(mcq(B([("red", 4), ("blue", 4)]) + "What is the opposite of “picking red”?", "picking blue",
                   ["picking red", "picking yellow", "picking 2 counters"],
                   "The bag has only red and blue. Not red means blue here."))
    its.append(mcq(B([("red", 3), ("blue", 2), ("yellow", 2)]) + "What is the opposite of “picking red”?",
                   "picking blue or yellow", ["picking blue", "picking yellow", "picking red or blue"],
                   "Not red means every colour that is not red: blue or yellow. It is not just one of them."))
    its.append(mcq(F(eq("red", "blue", "yellow", "blue")) + "The arrow lands on red, or it does not. Which is certain?",
                   "It lands on red or not red.", ["It lands on red.", "It lands on blue.", "It lands on yellow."],
                   "An event and its opposite cover everything. The arrow must land on red or on a colour that is not red."))
    its.append(pair_q(B([("green", 6)]) + "Which is true?", "Green", "Not green", "certain", "impossible",
                      [("certain", "certain"), ("possible", "possible"), ("certain", "possible")],
                      "Every counter is green, so green is certain. There is no counter that is not green, "
                      "so not green is impossible."))
    its.append(pair_q(B([("red", 5), ("blue", 1)]) + "Which is true?", "Red", "Not red", "possible", "possible",
                      [("possible", "impossible"), ("certain", "impossible"), ("impossible", "possible")],
                      "There is 1 blue counter, so not red might happen. That makes red possible, not certain. "
                      "Not red is possible too, even with only 1 blue counter."))
    its.append(pair_q(B([("yellow", 4), ("blue", 3)]) + "Which is true?", "Red", "Not red", "impossible", "certain",
                      [("impossible", "impossible"), ("possible", "possible"), ("impossible", "possible")],
                      "There are no red counters, so red is impossible. Every counter is not red, so not red is certain."))
    its.append(pair_q(fig(scene_svg("rain")) + "Dark clouds fill the sky. Which is true?", "Rain today", "No rain today",
                      "possible", "possible",
                      [("certain", "impossible"), ("possible", "impossible"), ("impossible", "certain")],
                      "Dark clouds often bring rain, but not every time. Rain might happen, and no rain might happen. "
                      "Both are possible."))
    its.append(pair_q(fig(scene_svg("calendar")) + "Today is Monday. Which is true?", "“Tomorrow is Tuesday”",
                      "“Tomorrow is not Tuesday”", "certain", "impossible",
                      [("possible", "possible"), ("certain", "possible"), ("impossible", "certain")],
                      "Tuesday always comes after Monday, so it is certain. Then tomorrow not being Tuesday is impossible."))
    its.append(mcq("In Owen’s bag, picking red is certain. Which is true?", "Not red is impossible.",
                   ["Not red is possible.", "Not red is certain.", "Red is impossible."],
                   "Certain means every counter is red. Then there is no counter that is not red, so not red is impossible."))
    its.append(mcq("In Ava’s bag, picking blue is impossible. Which is true?", "Not blue is certain.",
                   ["Not blue is impossible.", "Not blue is possible.", "Blue is certain."],
                   "Impossible means there are no blue counters. Every counter is not blue, so not blue is certain."))
    its.append(mcq("Rain tomorrow is possible. Which is true?", "No rain is possible too.",
                   ["No rain is impossible.", "No rain is certain.", "Rain is certain."],
                   "Possible means it might rain, or it might not. So no rain might happen too: it is also possible."))
    its.append(mcq(F(eq("red", "red", "blue", "red")) + "Which is more likely?", "red",
                   ["not red", "same chance", "not red is impossible"],
                   "Red: 3 of the 4 equal sections. Not red: only 1 section. So red is more likely."))
    assert 3 + 3 > 2
    its.append(mcq(B([("red", 2), ("blue", 3), ("yellow", 3)]) + "Which is more likely: red or not red?", "not red",
                   ["red", "same chance", "red is certain"],
                   "Not red means blue or yellow: 3 + 3 = 6 counters. Red has only 2. 6 is more than 2, so not red is more likely."))
    assert 2 + 2 == 4
    its.append(mcq(B([("red", 4), ("blue", 2), ("green", 2)]) + "Which is more likely: red or not red?", "same chance",
                   ["red", "not red", "not red is impossible"],
                   "Red: 4 counters. Not red: blue and green, 2 + 2 = 4 counters. 4 and 4 are the same, so they have the same chance."))
    assert 12 - 5 == 7
    its.append(mcq("A bag has 12 counters. 5 of them are red. How many counters are not red?", "7",
                   ["17", "5", "12"],
                   "Not red means all the other counters: 12 − 5 = 7."))
    its.append(mcq(fig(cube_faces_svg()) + "Nathan rolls a number cube. Which is more likely: a 6 or not a 6?", "not a 6",
                   ["a 6", "same chance", "a 6 is impossible"],
                   "Not a 6 means 1, 2, 3, 4 or 5: that is 5 faces. A 6 is only 1 face. So not a 6 is more likely."))
    its.append(abcd_q(fig(spinners_abcd([eq("red", "blue", "blue", "blue"), eq("red", "red", "red", "red"),
                                         eq("blue", "yellow", "blue", "yellow"), eq("red", "yellow", "red", "yellow")])) +
                      "On which spinner is “not red” certain?", "Spinner", 2,
                      "Spinner C has no red sections. Every section is not red, so not red is certain. "
                      "On B, not red is impossible."))
    assert 25 - 9 == 16
    its.append(mcq("Liam’s class has 25 students. 9 students walk to school. The rest do not walk. "
                   "How many students do not walk to school?", "16", ["34", "24", "9"],
                   "Do not walk means all the other students: 25 − 9 = 16."))
    assert len(its) == 20
    return {"title": "It will rain or it will not rain: opposite events", "items": its}


# ------------------------------------------------------------ set 5: predictions, decisions and word problems
def set_predictions(rnd):
    its = []
    maya = [9, 7, 4]
    assert sum(maya) == 20
    tf = fig(tally_svg("Maya’s 20 spins", "Colour", ["Red", "Blue", "Yellow"], maya, label="tally chart: Maya’s spins"))
    its.append(mcq(tf + "Which colour came up most often?", "red", ["yellow", "blue", "all the same"],
                   "Red: 1 group of 5 and 4 more = 9. Blue: 7. Yellow: 4. Red has the most tally marks."))
    its.append(mcq(tf + "How many times did Maya spin altogether?", "20 times", ["3 times", "9 times", "16 times"],
                   "Add the tallies: 9 + 7 + 4 = 20."))
    assert 9 - 4 == 5
    its.append(mcq(tf + "How many more times did red come up than yellow?", "5 times", ["13 times", "4 times", "9 times"],
                   "Red 9, yellow 4. How many more means subtract: 9 − 4 = 5."))
    its.append(mcq(fig(spinner_svg(eq("red", "blue"))) + "Lucas spins 20 times. Which result would be most surprising?",
                   "red 20, blue 0", ["red 10, blue 10", "red 11, blue 9", "red 8, blue 12"],
                   "Half the spinner is red and half is blue, so you expect about 10 of each. "
                   "Red every single time is possible, but it would be very surprising."))
    its.append(mcq(fig(spinner_svg(eq("blue", "blue", "red", "blue"))) + "Benjamin spins 20 times. Which prediction is best?",
                   "blue 15, red 5", ["blue 5, red 15", "blue 10, red 10", "blue 20, red 0"],
                   "3 of the 4 equal sections are blue, so blue should come up much more often than red. "
                   "Blue 20, red 0 is not a good guess, because red is possible."))
    its.append(mcq(fig(bag_svg([("green", 9), ("yellow", 1)], rnd)) +
                   "Amira picks a counter and puts it back. She does this 10 times. Which prediction is best?",
                   "green most times", ["yellow most times", "the same for each", "green every time for sure"],
                   "There are 9 green and 1 yellow counter, so green is much more likely. "
                   "Yellow is possible, so green every time is not certain."))
    its.append(mcq("Benjamin picks a counter and puts it back, 20 times. He gets red 17 times and blue 3 times. "
                   "Which bag did he most likely use?", "8 red, 2 blue",
                   ["2 red, 8 blue", "5 red, 5 blue", "10 red, 0 blue"],
                   "Red came up much more often, so the bag likely has many more red counters. "
                   "It cannot be 10 red and 0 blue: then blue would be impossible, but he picked blue 3 times."))
    av = [14, 6]
    tg = fig(tally_svg("Ava’s 20 spins", "Colour", ["Green", "Purple"], av, label="tally chart: Ava’s spins"))
    its.append(mcq(tg + "Ava’s spinner has 4 equal sections. Which spinner did she most likely use?",
                   "3 green, 1 purple", ["1 green, 3 purple", "2 green, 2 purple", "4 purple"],
                   "Green came up 14 times and purple 6 times. Green probably covers more of the spinner. "
                   "With 4 purple sections, green would be impossible."))
    its.append(mcq(fig(coin_svg()) + "Arjun tosses a loonie 4 times. He gets heads every time. What about the next toss?",
                   "same chance", ["tails is certain", "heads is certain", "heads is impossible"],
                   "A coin does not remember what happened before. Heads and tails still have the same chance."))
    its.append(mcq("Kai wins a prize if he picks red. Bag A has 3 red and 5 blue counters. Bag B has 5 red and 3 blue counters. "
                   "Which bag should he choose?", "Bag B", ["Bag A", "Either bag", "Neither bag"],
                   "Both bags have 8 counters. Bag B has 5 red and Bag A has only 3 red. Red is more likely in Bag B."))
    its.append(mcq("Zoe gets a point when the spinner lands on red. Jayden gets a point when it lands on blue. "
                   "Each spinner has 4 equal sections. Which spinner is fair?", "2 red and 2 blue sections",
                   ["3 red and 1 blue section", "1 red and 3 blue sections", "4 red sections"],
                   "A game is fair when both players have the same chance. 2 red and 2 blue equal sections "
                   "give red and blue the same chance."))
    its.append(mcq("It is January in Winnipeg. Snow is possible tomorrow. What should Nathan do?",
                   "Bring his boots and mitts.", ["Wear shorts and sandals.", "Stay home all week.", "Bring a beach towel."],
                   "Snow might happen, so it is smart to be ready. Boots and mitts keep him warm and dry if it snows."))
    its.append(mcq("Rain is possible on the day of the class picnic. What is a good plan?",
                   "Bring rain jackets, just in case.", ["Cancel, because rain is certain.", "Bring nothing, because rain is impossible.",
                                                         "Bring snow shovels."],
                   "Possible means it might rain, or it might not. So keep the picnic, but bring rain jackets just in case."))
    assert 10 > 1
    its.append(mcq("At the winter carnival, there are 100 raffle tickets. Ava buys 1 ticket. Ethan buys 10 tickets. "
                   "Who is more likely to win?", "Ethan", ["Ava", "same chance", "Ethan will win for sure"],
                   "Ethan has 10 tickets and Ava has 1. More tickets means more likely to win. "
                   "Ethan is not sure to win: there are 100 tickets."))
    assert 15 + 5 == 20
    its.append(mcq("A box has 20 granola bars: 15 chocolate chip and 5 oatmeal. Leah takes one without looking. "
                   "Which is true?", "Oatmeal is possible.",
                   ["Oatmeal is impossible.", "Oatmeal is certain.", "Chocolate chip is impossible."],
                   "There are 5 oatmeal bars, so Leah might get one. Oatmeal is possible. "
                   "It is less likely than chocolate chip, but it is not impossible."))
    its.append(mcq("Each of the 24 students in Sofia’s class puts their name in a toque. The teacher picks one name. "
                   "Which is certain?", "The name is a student in the class.",
                   ["Sofia’s name is picked.", "A boy’s name is picked.", "The teacher’s name is picked."],
                   "Every name in the toque belongs to a student in the class, so that is certain. "
                   "The teacher did not put in her name, so that is impossible."))
    assert 12 - 3 == 9
    its.append(mcq("Owen rolls a number cube 12 times. He gets a 6 three times. How many times did he not get a 6?",
                   "9 times", ["15 times", "3 times", "6 times"],
                   "Not a 6 means all the other rolls: 12 − 3 = 9."))
    assert 20 - 8 - 5 == 7
    its.append(mcq("Chloe spins 20 times. She gets red 8 times, blue 5 times and yellow the rest of the time. "
                   "How many times did she get yellow?", "7 times", ["13 times", "3 times", "33 times"],
                   "Step 1: red and blue: 8 + 5 = 13. Step 2: 20 − 13 = 7 times yellow."))
    assert 38 + 12 == 50
    its.append(mcq("Liam’s class spins a spinner 50 times. They get blue 38 times and yellow 12 times. "
                   "What is the best prediction for the next spin?", "Blue is more likely.",
                   ["Yellow is more likely.", "Blue is certain.", "Yellow is impossible."],
                   "Blue came up much more often, so blue probably covers more of the spinner. "
                   "Blue is more likely, but not certain: yellow came up 12 times."))
    assert 50 + 50 == 100
    its.append(mcq("A bag has 1 red and 1 blue counter. The class picks a counter and puts it back, 100 times. "
                   "Which result is the best prediction?", "about 50 red, 50 blue",
                   ["100 red, 0 blue", "about 90 red, 10 blue", "1 red, 1 blue"],
                   "Red and blue have the same chance, so about half of the 100 picks should be red: about 50. "
                   "The other half, about 50, should be blue."))
    assert len(its) == 20
    return {"title": "Predictions, decisions and word problems", "items": its}


# ------------------------------------------------------------ lesson
def ex(title, q, s, a):
    return ("<div class='sn-ex'><span class='sn-ex-t'>%s</span><p class='sn-ex-q'>%s</p>"
            "<p class='sn-ex-s'>%s</p><p class='sn-ex-a'>Answer: %s</p></div>" % (title, q, s, a))


def table(head, rows, cls="sn-table"):
    h = "".join("<th>%s</th>" % x for x in head)
    b = "".join("<tr>" + "".join("<td>%s</td>" % c for c in r) + "</tr>" for r in rows)
    return "<div class='sn-tw'><table class='%s'><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>" % (cls, h, b)


def scale3_svg():
    W, H = 420, 70
    x0, x1, y = 60, 360, 40
    s = ["<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='3'/>" % (x0, y, x1, y, GREEN)]
    s.append("<rect x='%d' y='%d' width='%d' height='10' fill='%s'/>" % (x0 + 8, y - 5, x1 - x0 - 16, FILL))
    for f, w in ((0, "impossible"), (0.5, "possible"), (1, "certain")):
        x = x0 + f * (x1 - x0)
        if f in (0, 1):
            s.append("<line x1='%.1f' y1='%d' x2='%.1f' y2='%d' stroke='%s' stroke-width='3'/>" % (x, y - 10, x, y + 10, GREEN))
        s.append(text(x, y - 18, w, 16, bold=True))
    s.append(text(x0, y + 26, "never", 14))
    s.append(text((x0 + x1) / 2, y + 26, "might happen", 14))
    s.append(text(x1, y + 26, "for sure", 14))
    return svg_wrap(W, H + 6, "".join(s), "impossible, possible and certain on a line")


def body_html(rnd):
    return (
        "<h2>Three probability words</h2>"
        "<p>Some things will happen for sure. Some things can never happen. Some things might happen.</p>"
        "<ul><li><b>Impossible</b>: it can never happen.</li>"
        "<li><b>Possible</b>: it might happen, or it might not.</li>"
        "<li><b>Certain</b>: it will happen for sure.</li></ul>"
        "<figure class='sn-fig'>" + scale3_svg() +
        "<figcaption>Impossible at one end, certain at the other. Possible is in between.</figcaption></figure>" +
        table(["Word", "Example"], [
            ["impossible", "A moose drives the school bus."],
            ["possible", "It snows in Ottawa tomorrow."],
            ["certain", "Today is Monday, so tomorrow is Tuesday."],
        ]) +
        "<h2>Bags and spinners</h2>"
        "<p>Look at what is in the bag. If <b>every</b> counter is red, red is certain. "
        "If there is <b>no</b> red counter, red is impossible. If there is some red and some other colour, red is possible.</p>"
        "<figure class='sn-fig'>" + bag_svg([("red", 5), ("blue", 1)], rnd, "bag: 5 red counters and 1 blue counter") +
        "<figcaption>5 red counters and 1 blue counter.</figcaption></figure>" +
        ex("Example", "Is picking blue possible or impossible?",
           "There is 1 blue counter, so you might pick it. Only 1 does not make it impossible.", "possible") +
        "<h2>Which is more likely?</h2>"
        "<p>Count how many of each colour there are. More counters means <b>more likely</b>. "
        "Fewer counters means <b>less likely</b>. The same number means the <b>same chance</b>. "
        "On a spinner, look at how big each part is.</p>"
        "<figure class='sn-fig'>" + spinner_svg(eq("red", "red", "blue", "red"), "spinner: 3 red sections and 1 blue section") +
        "<figcaption>3 red sections and 1 blue section, all the same size.</figcaption></figure>" +
        ex("Example", "Which colour is the arrow more likely to land on?",
           "Red has 3 sections. Blue has 1 section. 3 is more than 1.", "red") +
        "<h2>Opposite events: rain or no rain</h2>"
        "<p>Every event has an opposite. “It will rain” and “It will not rain” are opposites. "
        "One of the two must happen.</p>" +
        table(["If an event is …", "then its opposite is …"], [
            ["certain", "impossible"],
            ["impossible", "certain"],
            ["possible", "possible"],
        ]) +
        "<h2>Predictions and decisions</h2>"
        "<p>Use the chance to make a good guess. If most counters are green, predict green most of the time. "
        "If rain is possible, bring a rain jacket, just in case.</p>" +
        ex("Example", "Kai wins if he picks red. Bag A: 3 red, 5 blue. Bag B: 5 red, 3 blue. Which bag should he choose?",
           "Bag B has more red counters, so red is more likely there.", "Bag B") +
        "<h2>Common mistakes</h2>" +
        table(["Mistake", "What to do instead"], [
            ["Saying certain when it is only possible", "Certain means for sure, every time. If it might not happen, it is possible"],
            ["Saying impossible when there is only 1", "If it can happen even once, it is possible, not impossible"],
            ["Not counting how many of each", "Count each colour. More counters means more likely"],
            ["Counting sections, not their size", "Look at how much of the spinner each colour covers"],
            ["Choosing your favourite colour", "Your favourite colour does not change the chance"],
            ["Thinking not red is just one colour", "Not red means every colour that is not red"],
        ])
    )


FAQ = [
    {"q": "What do Grade 2 students learn about probability in Ontario?",
     "a": "In the Ontario Mathematics Curriculum (2020), expectation D2.1, Grade 2 students use the words impossible, possible and certain to describe events and their opposites, such as rain and no rain. They use these words to make predictions and simple decisions."},
    {"q": "What is the difference between possible and certain?",
     "a": "Possible means it might happen, or it might not, like rain tomorrow. Certain means it will happen for sure, like Tuesday coming after Monday."},
    {"q": "How can I practise probability with my child at home?",
     "a": "Put coloured counters, blocks or socks in a bag and ask, “Which colour is more likely?” before picking. Talk about everyday events too, such as a snow day or rain at recess, using impossible, possible and certain."},
    {"q": "Do Grade 2 students write a provincial math test in Ontario?",
     "a": "No. In Ontario, students write the EQAO provincial assessments in Grade 3 and Grade 6. Grade 2 probability builds the words students use again in Grade 3."},
]


def balance(sets, rnd):
    """Fixed questions keep their order. The rest are moved so every position is right 5 times in each set."""
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
    rnd = random.Random(42811)
    sets = [set_everyday(rnd), set_bags_spinners(rnd), set_more_likely(rnd), set_complement(rnd), set_predictions(rnd)]
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
        "country": "ca-on", "subject": "math", "grade": "grade-2", "slug": "probability", "sort": 11,
        "updated": UPDATED, "pdf_url": "",
        "title": "Probability: Impossible, Possible or Certain",
        "seo_title": "Grade 2 Probability Worksheets: Impossible, Possible, Certain (Free, with Answer Key)",
        "short_title": "Probability",
        "domain": "Data",
        "standard_code": "Grade 2: D2.1",
        "standard_url": "https://www.dcp.edu.gov.on.ca/en/curriculum/elementary-mathematics",
        "standard_text": "Use mathematical language, including the terms “impossible”, “possible”, and “certain”, to describe the likelihood of complementary events happening, and use that likelihood to make predictions and informed decisions",
        "meta_desc": "Free Grade 2 math worksheets on probability: describe everyday events as impossible, possible or certain, look at bags and spinners, decide which is more likely, think about opposite events (rain or no rain) and make predictions. 100 questions with an answer key, following the Ontario curriculum (D2.1).",
        "key_big": "Impossible: it can never happen. Possible: it might happen. Certain: it will happen for sure.",
        "key_sub": "Count how many of each colour to see which is more likely. An event and its opposite (rain and no rain): if one is certain, the other is impossible.",
        "body_html": body_html(rnd), "faq": FAQ, "sets": sets,
    }


def mark_large(u, pattern):
    """Tag pictures that must print larger (A to D panels, tally charts, number cube faces, mitts) so labels stay readable."""
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
        mark_large(u, "(spinners A to D|bags A to D|tally chart|the six faces|[0-9] [a-z ]*mitts)")
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
