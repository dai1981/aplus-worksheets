# -*- coding: utf-8 -*-
"""
British Columbia Grade 2 Math: Likelihood (BC Mathematics Curriculum, Data and probability)
  python3 tools/gen_cabc_math_g2_likelihood.py
Likelihood of familiar life events in BC with the words impossible, unlikely, likely and certain;
bags and spinners; comparing two events (more likely, less likely, equally likely); predictions from
a few trials; and word problems.
Wrong answers come from real student mistakes: likely confused with certain (it happens a lot, so it is
certain), unlikely confused with impossible ("only 1, so impossible"), ignoring how many of each colour,
counting sections instead of looking at their size, choosing a favourite colour, "tails is due" thinking,
and treating a few trials as proof.
Every picture shows the colour as a letter too (R = red ...), so it still works when printed in black and white.
Grade 2: short sentences for 7-8 year olds, a picture in many questions, numbers to 100.
HTML attributes use single quotes (no backslashes in the JSON). Canadian English.
"""
import json, re, math, os, random

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "ca-bc", "math", "grade-2")
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
    # recess games on a spinner (letter + soft fill, like the colours)
    "soccer": ("S", "#cfe6d6"),
    "tag": ("T", "#ffffff"),
}

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





WORDS4 = ["impossible", "unlikely", "likely", "certain"]
CMP = ["more likely", "less likely", "equally likely"]


def word4(counts, target):
    """impossible / unlikely / likely / certain for picking target from counts (dict colour -> number).
    Only clear cases are used: at most a third (unlikely) or at least two thirds (likely)."""
    n = counts.get(target, 0)
    tot = sum(counts.values())
    if n == 0:
        return "impossible"
    if n == tot:
        return "certain"
    assert 3 * n <= tot or 3 * n >= 2 * tot, (counts, target)
    return "unlikely" if 3 * n <= tot else "likely"


def cmp_word(a, b):
    return "more likely" if a > b else ("less likely" if a < b else "equally likely")


def cap(s):
    return s[0].upper() + s[1:]


def word_q(q, correct, e, extra=None):
    """Choices are the four likelihood words."""
    assert correct in WORDS4
    return mcq(q, correct, [w for w in WORDS4 if w != correct], e)


def st_q(q, counts, target, other, e, noun="{}"):
    """Which sentence is true? Correct: the right word for target. Wrong: two other words for target
    (the closest mistakes first) and a wrong word for another colour."""
    w = word4(counts, target)
    wo = word4(counts, other)
    near = {"impossible": ["unlikely", "likely"], "unlikely": ["impossible", "likely"],
            "likely": ["certain", "unlikely"], "certain": ["likely", "unlikely"]}[w]
    bad_o = {"impossible": "unlikely", "unlikely": "impossible", "likely": "certain", "certain": "likely"}[wo]
    n = lambda c: cap(noun.format(c))
    correct = "%s is %s." % (n(target), w)
    cands = ["%s is %s." % (n(target), x) for x in near] + ["%s is %s." % (n(other), bad_o)]
    return mcq(q, correct, cands, e)


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
    elif name == "ferry":
        s.append("<rect x='1' y='1' width='158' height='102' rx='8' fill='%s'/>" % SKY)
        s.append(ground("#5b8fd6", 70))
        s.append("<path d='M8 70 L40 44 L64 58 L84 40 L120 70 Z' fill='#4f7d5c' stroke='%s' stroke-width='1.2'/>" % INK)
        s.append("<path d='M30 72 L134 72 L126 88 L38 88 Z' fill='#ffffff' stroke='%s' stroke-width='2'/>" % INK)
        s.append("<rect x='34' y='78' width='96' height='4' fill='#3b78c4'/>")
        s.append("<rect x='50' y='58' width='62' height='14' fill='#ffffff' stroke='%s' stroke-width='1.5'/>" % INK)
        for x in range(56, 106, 12):
            s.append("<rect x='%d' y='62' width='7' height='6' fill='#8ab4f8' stroke='%s' stroke-width='0.8'/>" % (x, INK))
        s.append("<rect x='76' y='48' width='10' height='10' fill='#c0392b' stroke='%s' stroke-width='1.2'/>" % INK)
        s.append("<path d='M120 24 q5 -5 10 0 q5 -5 10 0' fill='none' stroke='%s' stroke-width='1.8'/>" % INK)
        lab = "a ferry on the ocean"
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


# ------------------------------------------------------------ results of a few trials
COIN = {"H": "#e9c46a", "T": "#e9c46a"}


def trial_row_svg(results, label, key=True):
    """A row of results, in order: colour names (counters) or H/T (coin tosses). Numbered 1, 2, 3 ..."""
    gap, r = 34, 14
    s = []
    for i, c in enumerate(results):
        cx = 6 + gap / 2 + i * gap
        if c in COL:
            fill, t = COL[c][1], COL[c][0]
        else:
            fill, t = COIN[c], c
        s.append("<circle cx='%.1f' cy='22' r='%d' fill='%s' stroke='%s' stroke-width='1.4'/>" % (cx, r, fill, INK))
        s.append(text(cx, 27, t, 14, bold=True))
        s.append(text(cx, 56, str(i + 1), 14, col="#555555"))
    W = int(12 + gap * len(results))
    H = 62
    if key:
        cols = colours_in(results)
        line = "  ".join(key_lines(cols)) if cols else "H = heads  T = tails"
        s.append(text(W / 2, H + 18, line, 15))
        W = int(max(W, tw(line, 15) + 12))
        H += 26
    return svg_wrap(W, H, "".join(s), label)


# ------------------------------------------------------------ set 1: everyday events in BC
def set_everyday(rnd):
    its = []
    S = lambda n: fig(scene_svg(n))
    its.append(word_q(S("lake") + "A sunny July day in Kelowna. July in Kelowna is hot and dry. "
                      "Which word fits “It rains today”?", "unlikely",
                      "Rain on a hot, dry July day is not likely, but it can happen. So it is unlikely. "
                      "It is not impossible: Kelowna does get some rain in summer."))
    its.append(mcq(S("lake") + "A hot summer day at a lake in the Okanagan. Which is impossible?", "The lake freezes today.",
                   ["You go for a swim.", "You see a boat.", "You eat ice cream."],
                   "Water does not freeze on a hot summer day. It can never happen, so it is impossible."))
    its.append(mcq(S("lake") + "A hot summer day at the lake. Which is likely?", "Kids swim in the lake.",
                   ["It snows on the lake.", "An orca swims in the lake.", "The lake turns into juice."],
                   "On a hot day, many kids swim. That will probably happen, so it is likely. "
                   "Orcas live in the ocean, not in lakes."))
    its.append(mcq(S("night") + "It is midnight in Kamloops. Which is certain?", "It is dark outside.",
                   ["You hear an owl.", "It rains.", "The sun is shining."],
                   "At midnight the sky is always dark. That is certain. An owl or rain might happen, but not for sure."))
    its.append(mcq(S("calendar") + "Today is Monday. Which is certain?", "Tomorrow is Tuesday.",
                   ["Tomorrow is sunny.", "Tomorrow is Friday.", "Tomorrow is a snow day."],
                   "Tuesday always comes after Monday, so it is certain. A sunny day is only likely or unlikely."))
    its.append(word_q(S("calendar") + "Today is Monday. Which word fits “Tomorrow is Saturday”?", "impossible",
                      "The day after Monday is always Tuesday. Tomorrow can never be Saturday, so it is impossible."))
    its.append(mcq(S("cake") + "Chloe is 7 today. Which is certain?", "Next year Chloe will be 8.",
                   ["Chloe gets a puppy.", "It rains at the party.", "Next year Chloe will be 6."],
                   "Every year you get 1 year older. 7 + 1 = 8, so it is certain. You cannot get younger."))
    its.append(word_q(S("egg") + "Lucas lets go of an egg. Which word fits “The egg falls down”?", "certain",
                      "When you let go of something, it always falls down. It is not just likely. It is certain."))
    its.append(word_q(S("popsicle") + "Leah leaves a popsicle in the hot sun for an hour. Which word fits “It melts”?",
                      "certain",
                      "The hot sun always melts a popsicle. It will happen for sure, so it is certain, not just likely."))
    its.append(mcq(S("hockey") + "Harjot’s team plays a hockey game. Which is impossible?", "Both teams win the game.",
                   ["Harjot scores a goal.", "The game ends in a tie.", "Someone falls on the ice."],
                   "Only one team can win a game. Both teams winning can never happen, so it is impossible."))
    its.append(mcq(S("school") + "It is a school day in Surrey. Which is likely?", "You read a book at school.",
                   ["There is a fire drill today.", "The school floats away.", "A bear teaches math."],
                   "Students read on most school days, so it is likely. A fire drill happens only a few times a year, "
                   "so it is unlikely."))
    its.append(mcq(S("school") + "It is a school day. Which is unlikely?", "A deer walks into your class.",
                   ["You eat lunch.", "You see your teacher.", "The school turns into a cake."],
                   "A deer in class could happen, but it almost never does. So it is unlikely. "
                   "A school turning into a cake can never happen: that is impossible, not unlikely."))
    its.append(mcq(S("winter") + "It is a snowy winter day at Whistler. Which is likely?", "People go skiing.",
                   ["People swim in the lake.", "It is 30\u00a0°C outside.", "The snow turns hot."],
                   "Many people ski at Whistler on a snowy winter day, so it is likely. "
                   "Swimming in an icy lake is unlikely."))
    its.append(mcq(S("winter") + "A snowy day in Prince George. Which is impossible?", "The snowman talks to you.",
                   ["You build a snow fort.", "More snow falls.", "You see a bald eagle."],
                   "A snowman cannot talk. That can never happen, so it is impossible. "
                   "The other things might happen."))
    its.append(word_q(S("rain") + "It is November in Vancouver. It rains on many days. "
                      "Owen says rain tomorrow is certain. Which word is better?", "likely",
                      "It rains on many November days in Vancouver, so rain is likely. "
                      "But some days are dry. It is not for sure, so it is not certain."))
    its.append(mcq(S("ferry") + "Wei rides a ferry to Vancouver Island. Which is unlikely?", "He sees an orca.",
                   ["He sees the ocean.", "He sees a seagull.", "The ferry flies in the sky."],
                   "Orcas live near Vancouver Island, but you do not see one on most trips. So it is unlikely. "
                   "Seeing the ocean is certain, and a flying ferry is impossible."))
    its.append(mcq(S("ferry") + "Wei rides a ferry. Which is impossible?", "The ferry drives on the highway.",
                   ["He sees an orca.", "He eats a snack.", "It rains on the trip."],
                   "A ferry is a boat. It can never drive on a highway, so it is impossible. "
                   "Seeing an orca is unlikely, but it can happen."))
    its.append(mcq("Which event is certain?", "A week has 7 days.",
                   ["It rains on Monday.", "You lose a tooth today.", "A week has 9 days."],
                   "Every week has 7 days, so it is certain. A week with 9 days is impossible."))
    its.append(word_q("Ava takes the SkyTrain every day. She says, “The train will be on time tomorrow. It is certain.” "
                      "Which word is better?", "likely",
                      "The SkyTrain is on time most days, so it is likely. Sometimes it is late, so it is not certain."))
    its.append(mcq("It is December in Prince George. Which is likely?", "It snows this week.",
                   ["You swim in an outdoor lake.", "It is a hot beach day.", "December has 40 days."],
                   "Prince George is cold and snowy in December, so snow this week is likely. "
                   "December has 31 days, so 40 days is impossible."))
    assert len(its) == 20
    return {"title": "Everyday events in BC: impossible, unlikely, likely or certain?", "items": its}


# ------------------------------------------------------------ set 2: bags and spinners
def set_bags_spinners(rnd):
    its = []
    B = lambda counts: fig(bag_svg(counts, rnd))
    F = lambda sec: fig(spinner_svg(sec))
    pick = "Picking {}"

    def wb(counts, target, q, e):
        return word_q(B(list(counts.items())) + q, word4(counts, target), e)

    def ws(sec, target, q, e):
        return word_q(F(sec) + q, word4(amounts(sec), target), e)

    its.append(wb({"red": 6}, "red", "You pick one counter without looking. Which word fits picking red?",
                  "Every counter is red. You will pick red for sure, so it is certain."))
    its.append(wb({"red": 5, "blue": 1}, "blue", "Which word fits picking blue?",
                  "There is only 1 blue counter and 5 red. Blue can happen, but probably not. So it is unlikely. "
                  "Only 1 does not make it impossible."))
    its.append(wb({"red": 5, "blue": 1}, "red", "Which word fits picking red?",
                  "Most counters are red, so red is likely. There is 1 blue counter, so red is not certain."))
    its.append(wb({"yellow": 5, "green": 2}, "red", "Which word fits picking red?",
                  "There are no red counters in the bag. You can never pick red, so it is impossible."))
    its.append(ws(eq("blue", "blue", "blue", "blue"), "blue", "Which word fits landing on blue?",
                  "Every section is blue. The arrow must land on blue, so it is certain."))
    sec = eq("red", "red", "red", "blue")
    its.append(ws(sec, "red", "Which word fits landing on red?",
                  "3 of the 4 equal sections are red, so red is likely. There is a blue section too, so red is not certain."))
    its.append(ws(sec, "blue", "Which word fits landing on blue?",
                  "Only 1 of the 4 equal sections is blue. Blue can happen, but probably not. So it is unlikely."))
    its.append(ws(eq("red", "blue", "yellow", "green"), "purple", "Which word fits landing on purple?",
                  "There is no purple section. The arrow can never land on purple, so it is impossible."))
    c = {"green": 1, "yellow": 7}
    its.append(st_q(B(list(c.items())) + "Which is true?", c, "green", "yellow",
                    "There is only 1 green counter and 7 yellow. Green can happen, but probably not. So green is unlikely.",
                    pick))
    c = {"red": 2, "blue": 6}
    its.append(st_q(B(list(c.items())) + "Which is true?", c, "blue", "red",
                    "6 of the 8 counters are blue, so blue is likely. There are red counters too, so blue is not certain.",
                    pick))
    its.append(abcd_q(fig(spinners_abcd([eq("red", "red", "red", "blue"), eq("red", "blue", "yellow", "green"),
                                         eq("red", "red", "red", "red"), eq("blue", "yellow", "blue", "yellow")])) +
                      "On which spinner is landing on red certain?", "Spinner", 2,
                      "Certain means it must happen. Only Spinner C is all red. On A, red is likely, "
                      "but not certain, because there is a blue section."))
    its.append(abcd_q(fig(bags_abcd([[("blue", 5), ("red", 1)], [("blue", 1), ("red", 5)],
                                     [("blue", 6)], [("red", 6)]], rnd)) +
                      "From which bag is picking blue unlikely?", "Bag", 1,
                      "Bag B has only 1 blue counter and 5 red. Blue can happen, but probably not. "
                      "In Bag D, blue is impossible, not unlikely."))
    its.append(abcd_q(fig(spinners_abcd([eq("red", "red", "red", "red"), eq("blue", "blue", "blue", "red"),
                                         eq("blue", "green", "blue", "green"), eq("red", "red", "red", "blue")])) +
                      "On which spinner is red likely, but not certain?", "Spinner", 3,
                      "Spinner D has 3 red sections and 1 blue. Red is likely, but blue can happen too. "
                      "On A, red is certain. On B, red is unlikely."))
    its.append(abcd_q(fig(bags_abcd([[("green", 6)], [("yellow", 1), ("green", 5)], [("yellow", 5), ("green", 1)],
                                     [("yellow", 6)]], rnd)) +
                      "From which bag is picking yellow impossible?", "Bag", 0,
                      "Bag A has no yellow counters, so yellow is impossible. "
                      "Bag B has only 1 yellow counter, so yellow is unlikely there, not impossible."))
    its.append(mcq("Mei’s bag has 4 red counters and 2 blue counters. Red is likely. She wants picking red to be certain. "
                   "What should she do?", "Take out the 2 blue counters.",
                   ["Add 2 more red counters.", "Take out the 4 red counters.", "Take out 1 blue counter."],
                   "Certain means every counter must be red. If the 2 blue counters come out, only red is left. "
                   "Adding red counters makes red more likely, but not certain."))
    its.append(mcq("Arjun’s bag has 1 blue counter and 5 red counters. Blue is unlikely. He wants picking blue to be impossible. "
                   "What should he do?", "Take out the 1 blue counter.",
                   ["Add 5 more red counters.", "Add 1 more blue counter.", "Take out the 5 red counters."],
                   "Impossible means it can never happen. With no blue counter left, blue can never be picked. "
                   "More red counters make blue less likely, but still not impossible."))
    its.append(word_q(fig(cube_faces_svg()) + "Simran rolls a number cube. Which word fits rolling a 7?", "impossible",
                      "The cube has the numbers 1 to 6. There is no 7, so rolling a 7 is impossible."))
    its.append(word_q(fig(cube_faces_svg()) + "Simran rolls a number cube. Which word fits rolling a 6?", "unlikely",
                      "Only 1 of the 6 faces shows a 6. A 6 can happen, but probably not. So it is unlikely, not impossible."))
    c = {"blue": 4, "red": 1}
    its.append(word_q(fig(mitts_svg(list(c.items()), rnd, "4 blue mitts and 1 red mitt")) +
                      "Kai grabs one mitt from the box in the dark. Which word fits getting a blue mitt?", word4(c, "blue"),
                      "4 of the 5 mitts are blue, so blue is likely. There is 1 red mitt, so blue is not certain."))
    its.append(mcq("A bag has 10 counters. Picking red is certain. How many red counters are in the bag?", "10",
                   ["9", "1", "5"],
                   "Certain means every counter is red: all 10. With 9 red and 1 other counter, red is only likely."))
    assert len(its) == 20
    return {"title": "Bags and spinners: which word fits?", "items": its}


# ------------------------------------------------------------ set 3: compare two events
def set_compare(rnd):
    its = []
    B = lambda counts: fig(bag_svg(counts, rnd))
    F = lambda sec: fig(spinner_svg(sec))
    G = lambda bags: fig(bags_abcd(bags, rnd))
    EQ = "equally likely"

    def cq(pic, q, a, b, fourth, e):
        return mcq(pic + q, cmp_word(a, b), [x for x in CMP if x != cmp_word(a, b)] + [fourth], e)

    its.append(cq(B([("red", 6), ("blue", 2)]), "Compare picking red with picking blue. Picking red is …", 6, 2, "certain",
                  "There are 6 red counters and only 2 blue. More counters means more likely."))
    its.append(cq(B([("yellow", 1), ("green", 7)]), "Compare picking yellow with picking green. Picking yellow is …", 1, 7,
                  "impossible",
                  "There is only 1 yellow counter and 7 green. Fewer counters means less likely. "
                  "It is not impossible: there is 1 yellow."))
    its.append(cq(F(eq("red", "blue", "red", "blue")), "Compare landing on red with landing on blue. Landing on red is …",
                  2, 2, "certain",
                  "There are 2 red and 2 blue sections, all the same size. Red and blue are equally likely."))
    sec = [("red", 3), ("blue", 1), ("green", 1), ("blue", 1)]
    assert amounts(sec) == {"red": 3, "blue": 2, "green": 1}
    its.append(mcq(F(sec) + "Kai says blue is more likely, because blue has 2 sections. Which is more likely, red or blue?",
                   "red", ["blue", EQ, "green"],
                   "Do not just count sections. Look at their size. The red section is half of the spinner. "
                   "The 2 blue sections are small. So red is more likely."))
    its.append(mcq(B([("green", 7), ("yellow", 2)]) + "Zara says yellow is more likely, because yellow is her favourite colour. "
                   "Which colour is more likely?", "green", ["yellow", EQ, "red"],
                   "Your favourite colour does not change the chance. There are 7 green and 2 yellow counters, "
                   "so green is more likely."))
    its.append(mcq(B([("red", 3), ("blue", 3), ("yellow", 2)]) + "Which two colours are equally likely?",
                   "red and blue", ["red and yellow", "blue and yellow", "all three"],
                   "Count each colour: red 3, blue 3, yellow 2. Red and blue have the same number, so they are equally likely."))
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
                      "On Spinner C, only 1 of the 4 sections is blue and 3 are red. So blue is less likely than red there. "
                      "On B, they are equally likely."))
    assert 2 + 6 == 8 and 8 > 6
    its.append(mcq(B([("red", 6), ("green", 2)]) + "Liam puts 6 more green counters into the bag. "
                   "Which colour is now more likely?", "green", ["red", EQ, "green is impossible"],
                   "Green: 2 + 6 = 8 counters. Red: 6 counters. 8 is more than 6, so green is now more likely."))
    assert 5 - 2 == 3
    its.append(mcq(B([("red", 2), ("blue", 5)]) + "How many red counters must Nadia add to make red and blue equally likely?",
                   "3", ["5", "7", "1"],
                   "Equally likely means the same number of each. Blue has 5. Red has 2. 5 − 2 = 3, so add 3 red counters."))
    its.append(mcq(fig(scene_svg("rain")) + "It is November in Vancouver. Which is more likely tomorrow?", "a rainy day",
                   ["a hot beach day", EQ, "a snowy day"],
                   "Vancouver gets a lot of rain in November and not much snow. So a rainy day is more likely. "
                   "A hot beach day in November is very unlikely."))
    its.append(mcq("Which is more likely?", "snow at Whistler in January",
                   ["snow in Vancouver in July", EQ, "both are impossible"],
                   "Whistler is in the mountains, and January is winter, so snow is very likely. "
                   "Snow in Vancouver in July almost never happens."))
    its.append(mcq("It is a school day. Which is least likely?", "A bald eagle flies into class.",
                   ["You read a book.", "You eat lunch.", "You go out for recess."],
                   "Reading, lunch and recess happen on most school days. An eagle in class almost never happens, "
                   "so it is least likely."))
    assert 15 > 12
    its.append(mcq("Ethan’s class has 15 girls and 12 boys. The teacher picks one name from a toque. "
                   "Which is more likely?", "a girl’s name", ["a boy’s name", EQ, "a girl’s name is certain"],
                   "There are 15 girls and 12 boys. 15 is more than 12, so a girl’s name is more likely. "
                   "It is not certain, because there are boys’ names too."))
    assert 14 + 5 + 1 == 20
    its.append(mcq("A prize box has 20 prizes: 14 pencils, 5 stickers and 1 toy car. Olivia picks one without looking. "
                   "Which is she least likely to get?", "the toy car", ["a pencil", "a sticker", EQ],
                   "There is only 1 toy car, so it is least likely. There are 14 pencils, so a pencil is most likely."))
    assert 9 > 3
    its.append(mcq("A box has 9 grape popsicles and 3 cherry popsicles. Owen takes one without looking. "
                   "Which is he more likely to get?", "grape", ["cherry", EQ, "orange"],
                   "There are 9 grape and 3 cherry popsicles. 9 is more than 3, so grape is more likely. "
                   "There is no orange, so orange is impossible."))
    its.append(mcq(B([("red", 4), ("blue", 4)]) + "Mateo picked red last time. He put it back. He says red is more likely now. "
                   "Which is right?", "Red and blue are equally likely.",
                   ["Red is more likely.", "Blue is more likely.", "Red is certain."],
                   "Mateo put the counter back, so there are still 4 red and 4 blue counters. "
                   "Red and blue are equally likely."))
    its.append(abcd_q(fig(spinners_abcd([eq("red", "blue", "blue", "blue"), eq("blue", "blue", "blue", "blue"),
                                         eq("red", "blue", "red", "blue"), eq("red", "red", "red", "blue")])) +
                      "Noah wants red to be more likely than blue. Which spinner should he use?", "Spinner", 3,
                      "Spinner D has 3 red sections and 1 blue section. Red is more likely there. "
                      "On C, red and blue are equally likely."))
    assert 3 > 1 and not 4 > 6
    its.append(mcq("Bag A has 3 red and 1 blue counter. Bag B has 4 red and 6 blue counters. "
                   "In which bag is red more likely than blue?", "Bag A", ["Bag B", "both bags", "neither bag"],
                   "Compare red with blue in each bag. Bag A: 3 red, 1 blue, so red is more likely. "
                   "Bag B has more red counters, but even more blue: 4 red, 6 blue."))
    assert len(its) == 20
    return {"title": "Compare two events: more, less or equally likely", "items": its}


# ------------------------------------------------------------ set 4: predictions from a few trials
def set_trials(rnd):
    its = []
    hana = ["red", "red", "blue", "red", "red", "red", "red", "blue", "red", "red"]
    assert hana.count("red") == 8 and hana.count("blue") == 2
    R = fig(trial_row_svg(hana, "results of 10 picks: 8 red and 2 blue"))
    intro = "Hana picks a counter from a bag and puts it back. She does this 10 times. "
    its.append(mcq(R + intro + "Which colour did she get more often?", "red", ["blue", "equally often", "green"],
                   "Count each colour: red 8 times, blue 2 times. 8 is more than 2, so red came up more often."))
    its.append(mcq(R + intro + "How many times did she get blue?", "2 times", ["8 times", "10 times", "12 times"],
                   "Count the B circles: picks 3 and 8. That is 2 times. 8 is the number of reds."))
    its.append(mcq(R + intro + "Which bag did she most likely use?", "7 red, 3 blue",
                   ["3 red, 7 blue", "0 red, 10 blue", "10 red, 0 blue"],
                   "Red came up much more often, so the bag likely has more red counters. "
                   "It cannot be 10 red and 0 blue: then blue would be impossible, but she picked blue."))
    its.append(mcq(R + intro + "What is the best prediction for her next pick?", "Red is likely.",
                   ["Red is certain.", "Blue is impossible.", "Blue is likely."],
                   "Red came up 8 of 10 times, so red is likely. Blue came up 2 times, so blue is not impossible, "
                   "and red is not certain."))
    ow = [9, 3]
    tf = fig(tally_svg("Owen’s 12 spins", "Colour", ["Red", "Yellow"], ow, label="tally chart: Owen’s spins"))
    its.append(mcq(tf + "Owen’s spinner has 4 equal sections. Which spinner did he most likely use?",
                   "3 red, 1 yellow", ["1 red, 3 yellow", "2 red, 2 yellow", "4 red"],
                   "Red came up 9 times and yellow 3 times. Red probably covers more of the spinner. "
                   "With 4 red sections, yellow would be impossible."))
    assert sum(ow) == 12
    its.append(mcq(tf + "How many times did Owen spin altogether?", "12 times", ["9 times", "6 times", "2 times"],
                   "Add the tallies: red 5 + 4 = 9, yellow 3. 9 + 3 = 12."))
    its.append(mcq(tf + "What is the best prediction for Owen’s next spin?", "Red is likely.",
                   ["Red is certain.", "Yellow is impossible.", "Yellow is likely."],
                   "Red came up most of the time, so red is likely. Yellow came up 3 times, so it is not impossible."))
    its.append(mcq(fig(coin_svg()) + "Arjun tosses a loonie 4 times. He gets heads every time. What about the next toss?",
                   "Heads and tails are equally likely.", ["Tails is certain.", "Heads is certain.", "Heads is impossible."],
                   "A coin does not remember what happened before. Heads and tails are still equally likely."))
    its.append(mcq(fig(spinner_svg(eq("red", "red", "red", "blue"))) +
                   "Kai spins 5 times. He never gets blue. Is landing on blue impossible?", "No, it is unlikely.",
                   ["Yes, it is impossible.", "No, it is certain.", "No, it is likely."],
                   "The spinner has a blue section, so blue can happen. 1 of 4 sections is blue, so it is unlikely. "
                   "A few spins cannot show that it is impossible."))
    its.append(mcq(fig(spinner_svg(eq("red", "blue"))) + "Lucas spins 10 times. Which result would be most surprising?",
                   "red 10, blue 0", ["red 5, blue 5", "red 6, blue 4", "red 4, blue 6"],
                   "Half the spinner is red and half is blue, so you expect about 5 of each. "
                   "Red every single time can happen, but it is very unlikely."))
    assert 8 * 3 // 4 == 6
    its.append(mcq(fig(spinner_svg(eq("blue", "blue", "red", "blue"))) + "Ryan spins 8 times. Which prediction is best?",
                   "blue 6, red 2", ["blue 2, red 6", "blue 4, red 4", "blue 8, red 0"],
                   "3 of the 4 equal sections are blue, so blue should come up much more often than red. "
                   "Blue 8, red 0 is not a good guess, because red can happen."))
    its.append(mcq(fig(bag_svg([("green", 9), ("yellow", 1)], rnd)) +
                   "Sofia picks a counter and puts it back. She does this 10 times. Which prediction is best?",
                   "green most times", ["yellow most times", "the same for each", "green every time for sure"],
                   "There are 9 green and 1 yellow counter, so green is much more likely. "
                   "Yellow can happen, so green every time is not certain."))
    jas = ["blue"] * 6
    its.append(mcq(fig(trial_row_svg(jas, "results of 6 picks: all blue")) +
                   "Jasleen picks from a bag 6 times and puts the counter back each time. She gets blue every time. "
                   "What is the best thing to say about the bag?", "It likely has mostly blue.",
                   ["It has only blue for sure.", "It has no blue.", "It has mostly red."],
                   "Blue every time tells us blue is likely. But 6 picks cannot show that every counter is blue. "
                   "There might be another colour she did not pick yet."))
    av = [7, 3]
    tg = fig(tally_svg("Ava’s 10 picks", "Colour", ["Green", "Purple"], av, label="tally chart: Ava’s picks"))
    its.append(word_q(tg + "Ava picks from a bag of green and purple counters. She puts each one back. "
                      "Which word best fits picking purple next?", "unlikely",
                      "Purple came up only 3 times out of 10. It can happen, so it is not impossible. "
                      "But it is less likely than green, so unlikely fits best."))
    assert 38 + 12 == 50
    its.append(mcq("Liam’s class spins a spinner 50 times. They get blue 38 times and yellow 12 times. "
                   "What is the best prediction for the next spin?", "Blue is more likely.",
                   ["Yellow is more likely.", "Blue is certain.", "Yellow is impossible."],
                   "Blue came up much more often, so blue probably covers more of the spinner. "
                   "Blue is more likely, but not certain: yellow came up 12 times."))
    assert 12 - 3 == 9
    its.append(mcq(fig(cube_faces_svg()) + "Owen rolls a number cube 12 times. He gets a 6 three times. "
                   "How many times did he not get a 6?", "9 times", ["15 times", "3 times", "6 times"],
                   "Not a 6 means all the other rolls: 12 − 3 = 9."))
    assert 10 - 5 - 3 == 2
    its.append(mcq("Chloe spins 10 times. She gets red 5 times, blue 3 times and yellow the rest of the time. "
                   "How many times did she get yellow?", "2 times", ["8 times", "18 times", "3 times"],
                   "Step 1: red and blue: 5 + 3 = 8. Step 2: 10 − 8 = 2 times yellow."))
    its.append(mcq("A bag has 1 red and 1 blue counter. Mei picks a counter and puts it back, 20 times. "
                   "Which result is the best prediction?", "about 10 red, 10 blue",
                   ["20 red, 0 blue", "about 18 red, 2 blue", "1 red, 1 blue"],
                   "Red and blue are equally likely, so about half of the 20 picks should be red: about 10. "
                   "The other half, about 10, should be blue."))
    toss = ["H", "T", "T", "H", "T", "T"]
    its.append(mcq(fig(trial_row_svg(toss, "results of 6 toonie tosses: H T T H T T")) +
                   "Noah tosses a toonie 6 times. He gets tails 4 times. Which is true about the next toss?",
                   "Heads and tails are equally likely.",
                   ["Tails is certain.", "Heads is impossible.", "Tails is more likely."],
                   "A toonie has 2 sides, and each side has the same chance every time. "
                   "A few tosses do not change that."))
    its.append(word_q("Hana got red 8 times out of 10. She says, “Red is certain next time.” Which word is better?", "likely",
                      "Red came up most of the time, so red is likely. Blue came up too, so red is not certain."))
    assert len(its) == 20
    return {"title": "Predictions from a few trials", "items": its}


# ------------------------------------------------------------ set 5: word problems
def set_word(rnd):
    its = []
    EQ = "equally likely"
    assert 10 > 1
    its.append(mcq("At the school fun fair, there are 100 raffle tickets. Ava buys 1 ticket. Ethan buys 10 tickets. "
                   "Who is more likely to win?", "Ethan", ["Ava", EQ, "Ethan will win for sure"],
                   "Ethan has 10 tickets and Ava has 1. More tickets means more likely to win. "
                   "Ethan is not sure to win: there are 100 tickets."))
    assert 15 + 5 == 20 and 3 * 5 <= 20
    its.append(mcq("A box has 20 granola bars: 15 chocolate chip and 5 oatmeal. Leah takes one without looking. "
                   "Which is true?", "Oatmeal is unlikely.",
                   ["Oatmeal is impossible.", "Oatmeal is likely.", "Oatmeal is certain."],
                   "Only 5 of the 20 bars are oatmeal. Leah might get one, but probably not. "
                   "So oatmeal is unlikely, not impossible."))
    its.append(mcq("Each of the 24 students in Sofia’s class puts their name in a toque. The teacher picks one name. "
                   "Which is certain?", "The name is a student in the class.",
                   ["Sofia’s name is picked.", "A boy’s name is picked.", "The teacher’s name is picked."],
                   "Every name in the toque belongs to a student in the class, so that is certain. "
                   "The teacher did not put in her name, so that is impossible."))
    its.append(mcq("Zara gets a point when the spinner lands on red. Lucas gets a point when it lands on blue. "
                   "Each spinner has 4 equal sections. Which spinner is fair?", "2 red and 2 blue sections",
                   ["3 red and 1 blue section", "1 red and 3 blue sections", "4 red sections"],
                   "A game is fair when both players are equally likely to win. 2 red and 2 blue equal sections "
                   "make red and blue equally likely."))
    its.append(mcq("Kai wins a prize if he picks red. Bag A has 3 red and 5 blue counters. Bag B has 5 red and 3 blue counters. "
                   "Which bag should he choose?", "Bag B", ["Bag A", "Either bag", "Neither bag"],
                   "Both bags have 8 counters. Bag B has 5 red and Bag A has only 3 red. Red is more likely in Bag B."))
    its.append(mcq("Rain is likely on the day of the class picnic in Stanley Park. What is a good plan?",
                   "Bring rain jackets.", ["Cancel, because rain is certain.", "Bring nothing, because rain is impossible.",
                                           "Bring snow shovels."],
                   "Likely means it will probably rain, but not for sure. So keep the picnic, and bring rain jackets."))
    its.append(mcq(fig(scene_svg("ferry")) + "On the ferry, Wei looks for orcas. Seeing an orca is unlikely. Which is true?",
                   "He might see one.", ["He will see one for sure.", "He can never see one.", "He will see 100 orcas."],
                   "Unlikely means it can happen, but probably will not. So he might see one. "
                   "Unlikely is not the same as impossible."))
    assert 8 + 2 == 10 and 3 * 8 >= 2 * 10
    its.append(word_q("Lucas has 8 white socks and 2 black socks in a drawer. He grabs one sock in the dark. "
                      "Which word fits getting a white sock?", "likely",
                      "8 of the 10 socks are white, so white is likely. There are 2 black socks, so white is not certain."))
    assert 25 + 5 == 30
    its.append(mcq("Ryan has 30 stickers in a bag: 25 orca stickers and 5 eagle stickers. He picks one without looking. "
                   "Which is true?", "An orca sticker is likely.",
                   ["An orca sticker is certain.", "An eagle sticker is likely.", "An eagle sticker is impossible."],
                   "25 of the 30 stickers are orcas, so an orca is likely. There are 5 eagles, so an orca is not certain "
                   "and an eagle is not impossible."))
    assert 20 - 6 == 14
    its.append(mcq("A bag has 20 counters. 6 of them are red. How many counters are not red?", "14",
                   ["26", "6", "20"],
                   "Not red means all the other counters: 20 − 6 = 14."))
    its.append(mcq("Arjun puts 10 blue counters in a bag. He wants red and blue to be equally likely. "
                   "How many red counters should he add?", "10", ["20", "5", "11"],
                   "Equally likely means the same number of each colour. Blue has 10, so add 10 red."))
    assert 3 + 6 == 9 and 9 > 3
    its.append(mcq("A bag has 3 red and 3 blue counters. Nadia adds 6 more red counters. Which is true now?",
                   "Red is more likely.", ["Red is certain.", "Red and blue are equally likely.", "Blue is more likely."],
                   "Red: 3 + 6 = 9 counters. Blue: 3 counters. 9 is more than 3, so red is more likely. "
                   "There is still blue, so red is not certain."))
    sec = eq("soccer", "soccer", "soccer", "tag")
    its.append(word_q(fig(spinner_svg(sec, "spinner: 3 soccer sections and 1 tag section")) +
                      "Mr. Kim’s class spins to pick a recess game. Which word fits playing tag?",
                      word4(amounts(sec), "tag"),
                      "Only 1 of the 4 equal sections is tag. Tag can happen, but probably not. So it is unlikely."))
    its.append(mcq("On the day of the Terry Fox Run, rain is unlikely. What does unlikely mean?",
                   "It might rain, but probably not.",
                   ["It will rain for sure.", "It can never rain.", "It will probably rain."],
                   "Unlikely means it can happen, but it probably will not. It is not the same as impossible."))
    its.append(mcq("The weather report says rain in Victoria is likely tomorrow. Jasleen says, “So it will rain for sure.” "
                   "Is she right?", "No. Likely is not certain.",
                   ["Yes. Likely means certain.", "No. Rain is impossible.", "No. Rain is unlikely."],
                   "Likely means it will probably rain. It might stay dry. Only certain means for sure."))
    assert 40 > 10 and 40 + 10 == 50
    its.append(mcq("A jar has 40 green marbles and 10 yellow marbles. Ji-woo picks one without looking. "
                   "Which is more likely?", "green", ["yellow", EQ, "blue"],
                   "There are 40 green and 10 yellow marbles. 40 is more than 10, so green is more likely. "
                   "There are no blue marbles, so blue is impossible."))
    assert 30 - 14 == 16
    its.append(mcq(fig(coin_svg()) + "Emma’s class tosses a loonie 30 times. They get heads 14 times. "
                   "How many times did they get tails?", "16 times", ["44 times", "14 times", "30 times"],
                   "A loonie lands on heads or tails. Tails is all the other tosses: 30 − 14 = 16."))
    its.append(mcq(fig(cube_faces_svg()) + "Zara wins if she rolls 1, 2, 3, 4 or 5. Harjot wins if he rolls a 6. "
                   "Is the game fair?", "No. Zara is more likely to win.",
                   ["Yes. It is fair.", "No. Harjot is more likely to win.", "No. Zara will win for sure."],
                   "Zara wins on 5 faces. Harjot wins on only 1 face. They are not equally likely to win, so it is not fair. "
                   "Zara is not sure to win: a 6 can happen."))
    its.append(mcq("A bag has 50 counters. Picking red is impossible. How many red counters are in the bag?", "0",
                   ["1", "50", "25"],
                   "Impossible means it can never happen. So there are no red counters: 0. With 1 red, red is unlikely."))
    its.append(mcq("Owen picks a name from a toque with 30 names. His own name is on 1 paper. "
                   "Which word fits picking his own name?", "unlikely",
                   ["impossible", "likely", "certain"],
                   "His name is only 1 of 30, so it can happen, but probably not. It is unlikely, not impossible."))
    assert len(its) == 20
    return {"title": "Word problems: likelihood in BC life", "items": its}


# ------------------------------------------------------------ lesson
def ex(title, q, s, a):
    return ("<div class='sn-ex'><span class='sn-ex-t'>%s</span><p class='sn-ex-q'>%s</p>"
            "<p class='sn-ex-s'>%s</p><p class='sn-ex-a'>Answer: %s</p></div>" % (title, q, s, a))


def table(head, rows, cls="sn-table"):
    h = "".join("<th>%s</th>" % x for x in head)
    b = "".join("<tr>" + "".join("<td>%s</td>" % c for c in r) + "</tr>" for r in rows)
    return "<div class='sn-tw'><table class='%s'><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>" % (cls, h, b)


def scale4_svg():
    W, H = 470, 76
    x0, x1, y = 60, 410, 40
    s = ["<rect x='%d' y='%d' width='%d' height='10' fill='%s'/>" % (x0, y - 5, x1 - x0, FILL)]
    s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='3'/>" % (x0, y, x1, y, GREEN))
    for f, w, sub in ((0, "impossible", "never"), (1 / 3, "unlikely", "probably not"),
                      (2 / 3, "likely", "probably"), (1, "certain", "for sure")):
        x = x0 + f * (x1 - x0)
        s.append("<line x1='%.1f' y1='%d' x2='%.1f' y2='%d' stroke='%s' stroke-width='3'/>" % (x, y - 10, x, y + 10, GREEN))
        s.append(text(x, y - 18, w, 16, bold=True))
        s.append(text(x, y + 28, sub, 14))
    return svg_wrap(W, H, "".join(s), "impossible, unlikely, likely and certain on a line")


def body_html(rnd):
    return (
        "<h2>Four likelihood words</h2>"
        "<p>Likelihood tells how sure we are that something will happen. Use these words, from never to for sure:</p>"
        "<ul><li><b>Impossible</b>: it can never happen.</li>"
        "<li><b>Unlikely</b>: it can happen, but probably will not.</li>"
        "<li><b>Likely</b>: it will probably happen, but not for sure.</li>"
        "<li><b>Certain</b>: it will happen for sure.</li></ul>"
        "<figure class='sn-fig'>" + scale4_svg() +
        "<figcaption>Impossible at one end, certain at the other. Unlikely and likely are in between.</figcaption></figure>" +
        table(["Word", "Example in BC"], [
            ["impossible", "A ferry drives on the highway."],
            ["unlikely", "You see an orca from the ferry."],
            ["likely", "It rains in Vancouver on a November day."],
            ["certain", "Today is Monday, so tomorrow is Tuesday."],
        ]) +
        "<h2>Bags and spinners</h2>"
        "<p>Look at what is in the bag. <b>All</b> red: red is certain. <b>Most</b> red: red is likely. "
        "<b>Only a few</b> red: red is unlikely. <b>No</b> red: red is impossible.</p>"
        "<figure class='sn-fig'>" + bag_svg([("red", 5), ("blue", 1)], rnd, "bag: 5 red counters and 1 blue counter") +
        "<figcaption>5 red counters and 1 blue counter.</figcaption></figure>" +
        ex("Example", "Which word fits picking red? Which word fits picking blue?",
           "Most counters are red, so red is likely. There is 1 blue, so red is not certain. "
           "Blue can happen, but probably not.", "red is likely, blue is unlikely") +
        "<h2>More likely, less likely, equally likely</h2>"
        "<p>To compare two events, count how many of each. More counters means <b>more likely</b>. "
        "Fewer counters means <b>less likely</b>. The same number means <b>equally likely</b>. "
        "On a spinner, look at how big each part is.</p>"
        "<figure class='sn-fig'>" + spinner_svg(eq("red", "blue", "red", "blue"), "spinner: 2 red sections and 2 blue sections") +
        "<figcaption>2 red sections and 2 blue sections, all the same size.</figcaption></figure>" +
        ex("Example", "Compare landing on red with landing on blue.",
           "Red has 2 sections. Blue has 2 sections. They are the same size.", "equally likely") +
        "<h2>Predictions from a few trials</h2>"
        "<p>Try it a few times and look at the results. What comes up most often is likely to come up again. "
        "A few tries cannot show that something is impossible or certain.</p>"
        "<figure class='sn-fig'>" + trial_row_svg(["red", "red", "blue", "red", "red", "red", "red", "blue", "red", "red"],
                                                  "10 picks: 8 red and 2 blue") +
        "<figcaption>Hana’s 10 picks. She put the counter back each time.</figcaption></figure>" +
        ex("Example", "What is the best prediction for Hana’s next pick?",
           "Red came up 8 times and blue 2 times. Red is likely. Blue came up too, so red is not certain.",
           "Red is likely.") +
        "<h2>Common mistakes</h2>" +
        table(["Mistake", "What to do instead"], [
            ["Saying certain when it is only likely", "Certain means for sure, every time. If it might not happen, say likely"],
            ["Saying impossible when it is only unlikely", "If it can happen even once, it is unlikely, not impossible"],
            ["Not counting how many of each", "Count each colour. More counters means more likely"],
            ["Counting sections, not their size", "Look at how much of the spinner each colour covers"],
            ["Choosing your favourite colour", "Your favourite colour does not change the chance"],
            ["Thinking a coin is “due” for tails", "Heads and tails are equally likely on every toss"],
        ])
    )


FAQ = [
    {"q": "What do Grade 2 students learn about likelihood in BC math?",
     "a": "In the BC curriculum (Data and probability), Grade 2 students describe the likelihood of familiar life events with words like impossible, unlikely, likely and certain. They also compare two events as more likely, less likely or equally likely."},
    {"q": "What is the difference between likely and certain?",
     "a": "Likely means it will probably happen, but it might not, like rain on a November day in Vancouver. Certain means it will happen for sure, like Tuesday coming after Monday."},
    {"q": "What is the difference between unlikely and impossible?",
     "a": "Unlikely means it can happen, but probably will not, like seeing an orca from a ferry. Impossible means it can never happen, like a ferry driving on the highway."},
    {"q": "How can I practise likelihood with my child at home?",
     "a": "Put coloured blocks or socks in a bag and ask, “Which colour is more likely?” before picking. Talk about everyday events too, such as rain at recess or a snow day, using impossible, unlikely, likely and certain."},
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
    rnd = random.Random(52811)
    sets = [set_everyday(rnd), set_bags_spinners(rnd), set_compare(rnd), set_trials(rnd), set_word(rnd)]
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
        "country": "ca-bc", "subject": "math", "grade": "grade-2", "slug": "likelihood", "sort": 11,
        "updated": UPDATED, "pdf_url": "",
        "title": "Likelihood: Impossible, Unlikely, Likely or Certain",
        "seo_title": "Grade 2 Likelihood Worksheets: Impossible, Unlikely, Likely, Certain (Free Math, Answer Key, BC Curriculum)",
        "short_title": "Likelihood",
        "domain": "Data and probability",
        "standard_code": "Grade 2: Data and probability",
        "standard_url": "https://curriculum.gov.bc.ca/curriculum/mathematics/2/core",
        "standard_text": "Likelihood of familiar life events, using comparative language",
        "meta_desc": "Free Grade 2 math worksheets on likelihood: describe familiar events in BC as impossible, unlikely, likely or certain, use bags and spinners, compare events as more, less or equally likely, and make predictions from a few trials. 100 questions with an answer key, matched to the BC curriculum.",
        "key_big": "Impossible: never. Unlikely: probably not. Likely: probably. Certain: for sure.",
        "key_sub": "Likely is not certain: if it might not happen, say likely. To compare two events, count each colour: more, less or equally likely.",
        "body_html": body_html(rnd), "faq": FAQ, "sets": sets,
    }


def mark_large(u, pattern):
    """Tag pictures that must print larger (A to D panels, tally charts, number cube faces, mitts, rows of results)."""
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
        mark_large(u, "(spinners A to D|bags A to D|tally chart|the six faces|[0-9] [a-z ]*mitts? and|results of)")
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
