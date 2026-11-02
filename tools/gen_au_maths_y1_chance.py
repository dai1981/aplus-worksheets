# -*- coding: utf-8 -*-
"""
AU Year 1 Maths: Chance (AC9M1P01, Australian Curriculum v9.0)
  python3 tools/gen_au_maths_y1_chance.py
Everyday events, spinners, bags of counters, "which is more likely?", coins, dice and short stories.
Only the everyday words of Year 1: will happen, might happen, won't happen (and "more likely").
Wrong answers come from real mistakes: "will" for something that only might happen, "won't" when there is
only a little of a colour, ignoring what is in the bag, choosing a favourite colour, thinking 6 is hard to roll.
Every picture shows the colour as a letter too (R = red ...), so it still works in black and white.
Year 1: very short sentences for 6-7 year olds, a picture in almost every question.
HTML attributes use single quotes (no backslashes in the JSON). Australian English.
"""
import json, math, os, random, re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "au", "maths", "year-1")
UPDATED = "2026-11-02"
GREEN = "#006633"
FILL = "#cfe6d6"
FILL2 = "#e6f2ea"
INK = "#2b2b2b"
FONT = "Arial, Helvetica, sans-serif"

COL = {
    "red": ("R", "#f28b82"),
    "blue": ("B", "#8ab4f8"),
    "yellow": ("Y", "#fde293"),
    "green": ("G", "#81c995"),
    "purple": ("P", "#c58af9"),
}
MODS = ["will", "might", "won’t"]


# ------------------------------------------------------------ helpers
def mcq(q, correct, cands, e):
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


def abcd_q(q, kind, ai, e):
    return {"q": q, "c": ["%s %s" % (kind, L) for L in "ABCD"], "a": ai, "e": e, "_fix": True}


def modal(counts, target):
    n = counts.get(target, 0)
    tot = sum(counts.values())
    return "will" if n == tot else ("won’t" if n == 0 else "might")


def say(m, verb, thing, who="You"):
    return "%s %s %s %s." % (who, m, verb, thing)


def st_q(q, counts, target, verb, other, e, who="You"):
    """Which sentence is true? Correct: the right word for target.
    Wrong: the other two words for target, and a wrong word for another thing."""
    m = modal(counts, target)
    mo = modal(counts, other)
    wrong_o = "will" if mo != "will" else "won’t"
    correct = say(m, verb, target, who)
    cands = [say(x, verb, target, who) for x in MODS if x != m] + [say(wrong_o, verb, other, who)]
    return mcq(q, correct, cands, e)


def fig(svg):
    return "<div class='qfig'>" + svg + "</div>"


def svg_wrap(w, h, body, label):
    return ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 %d %d' width='%d' height='%d' "
            "role='img' aria-label='%s'><g font-family='%s'>%s</g></svg>" % (w, h, w, h, label, FONT, body))


def tw(t, fs, bold=False):
    return len(str(t)) * fs * (0.62 if bold else 0.58)


def text(x, y, t, fs=14, anchor="middle", bold=False, col=INK):
    return ("<text x='%.1f' y='%.1f' font-size='%d'%s fill='%s' text-anchor='%s'>%s</text>"
            % (x, y, fs, " font-weight='700'" if bold else "", col, anchor, t))


def eq(*labels):
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


def key_lines(cols):
    return ["%s = %s" % (COL[c][0], c) for c in cols]


# ------------------------------------------------------------ spinner
def spinner_body(cx, cy, R, sectors, fs):
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


def spinner_svg(sectors, label="spinner"):
    R, pad = 62, 6
    cx, cy = pad + R, pad + R
    s = spinner_body(cx, cy, R, sectors, 18)
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
        s.append(text(W / 2, H + 14, "     ".join(key_lines(cols)), 14))
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
    rows = (len(items) + cols - 1) // cols
    bw = cols * gap + 16
    bh = rows * gap + 16
    top = y + 14
    s = []
    s.append("<path d='M%.1f %.1f L%.1f %.1f L%.1f %.1f L%.1f %.1f Z' fill='#f4efe4' stroke='%s' stroke-width='1.5'/>"
             % (x + bw / 2 - 14, y, x + bw / 2 + 14, y, x + bw / 2 + 22, top, x + bw / 2 - 22, top, INK))
    s.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='3'/>"
             % (x + bw / 2 - 16, y + 5, x + bw / 2 + 16, y + 5, INK))
    s.append("<rect x='%.1f' y='%.1f' width='%d' height='%d' rx='16' fill='#f4efe4' stroke='%s' stroke-width='2'/>"
             % (x, top, bw, bh, INK))
    for i, c in enumerate(items):
        rr, cc = divmod(i, cols)
        n_row = min(cols, len(items) - rr * cols)
        off = (cols - n_row) * gap / 2
        px = x + 8 + off + cc * gap + gap / 2
        py = top + 8 + rr * gap + gap / 2
        s.append("<circle cx='%.1f' cy='%.1f' r='%d' fill='%s' stroke='%s' stroke-width='1.2'/>" % (px, py, r, COL[c][1], INK))
        s.append(text(px, py + fs * 0.35, COL[c][0], fs, bold=True))
    return s, bw, 14 + bh


def bag_svg(counts, rnd, label="bag of counters"):
    items = bag_items(counts, rnd)
    cols = 4 if len(items) > 4 else len(items)
    if len(items) in (5, 6):
        cols = 3
    s, bw, bh = bag_body(4, 4, items, cols, 14, 34, 15)
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
    s.append(text(W / 2, H + 14, "     ".join(key_lines(colours_in(allc))), 14))
    H += 22
    return svg_wrap(W, H, "".join(s), label)


# ------------------------------------------------------------ everyday pictures
SKY = "#dff0fb"


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


def scene_svg(name):
    W, H = 160, 104
    s = []
    lab = name
    if name == "beach":
        s.append("<rect x='1' y='1' width='158' height='102' rx='8' fill='%s'/>" % SKY)
        s.append(sun(128, 26, 13))
        s.append("<rect x='1' y='54' width='158' height='20' fill='#8ab4f8'/>")
        s.append("<path d='M1 74 L159 74 L159 95 Q159 103 151 103 L9 103 Q1 103 1 95 Z' fill='#f4e2b0'/>")
        s.append("<line x1='48' y1='40' x2='48' y2='92' stroke='%s' stroke-width='2.5'/>" % INK)
        s.append("<path d='M18 44 Q48 14 78 44 Z' fill='#f28b82' stroke='%s' stroke-width='1.5'/>" % INK)
        s.append("<path d='M96 92 L104 80 L112 92 Z' fill='#e9c46a' stroke='%s' stroke-width='1.2'/>" % INK)
        lab = "a sunny beach in summer"
    elif name == "night":
        s.append("<rect x='1' y='1' width='158' height='102' rx='8' fill='#2f3e66'/>")
        s.append("<circle cx='42' cy='34' r='18' fill='#fde293'/>")
        s.append("<circle cx='51' cy='28' r='16' fill='#2f3e66'/>")
        for (x, y) in [(90, 20), (120, 36), (140, 16), (100, 52), (70, 62), (132, 64), (20, 70)]:
            s.append("<circle cx='%d' cy='%d' r='2.5' fill='#ffffff'/>" % (x, y))
        s.append("<path d='M1 84 L159 84 L159 95 Q159 103 151 103 L9 103 Q1 103 1 95 Z' fill='#2e5b3a'/>")
        lab = "the Moon and stars at night"
    elif name == "sunset":
        s.append("<rect x='1' y='1' width='158' height='102' rx='8' fill='#fbd7a5'/>")
        s.append("<circle cx='80' cy='66' r='24' fill='#f9a03f' stroke='#d9822b' stroke-width='2'/>")
        s.append("<path d='M1 66 L159 66 L159 95 Q159 103 151 103 L9 103 Q1 103 1 95 Z' fill='#8ab4f8'/>")
        s.append("<line x1='1' y1='66' x2='159' y2='66' stroke='%s' stroke-width='1.5'/>" % INK)
        lab = "the sun going down in the evening"
    elif name == "rain":
        s.append("<rect x='1' y='1' width='158' height='102' rx='8' fill='#e3e7ec'/>")
        s.append(cloud(80, 34, 1.3, "#c4ccd6"))
        for k in range(7):
            x = 40 + k * 13
            s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='#3b78c4' stroke-width='2.5' stroke-linecap='round'/>"
                     % (x, 66 + (k % 2) * 8, x - 4, 78 + (k % 2) * 8))
        lab = "dark rain clouds"
    elif name == "school":
        s.append("<rect x='1' y='1' width='158' height='102' rx='8' fill='%s'/>" % SKY)
        s.append("<rect x='30' y='42' width='100' height='54' fill='#f4e2b0' stroke='%s' stroke-width='2'/>" % INK)
        s.append("<path d='M24 42 L80 16 L136 42 Z' fill='#c0392b' stroke='%s' stroke-width='2'/>" % INK)
        s.append("<rect x='70' y='68' width='20' height='28' fill='#8a5a2b' stroke='%s' stroke-width='1.5'/>" % INK)
        for x in (40, 104):
            s.append("<rect x='%d' y='54' width='16' height='14' fill='#8ab4f8' stroke='%s' stroke-width='1.5'/>" % (x, INK))
        s.append(text(80, 38, "SCHOOL", 14, bold=True, col="#ffffff"))
        s.append("<line x1='142' y1='96' x2='142' y2='30' stroke='%s' stroke-width='2'/>" % INK)
        s.append("<rect x='142' y='30' width='12' height='9' fill='#81c995' stroke='%s' stroke-width='1'/>" % INK)
        lab = "a school"
    elif name == "cake":
        s.append("<rect x='1' y='1' width='158' height='102' rx='8' fill='#fdf1f4'/>")
        s.append("<rect x='38' y='56' width='84' height='38' rx='4' fill='#f7c6d0' stroke='%s' stroke-width='2'/>" % INK)
        s.append("<path d='M38 66 Q50 74 62 66 Q74 74 86 66 Q98 74 110 66 Q116 72 122 66' fill='none' stroke='#ffffff' stroke-width='4'/>")
        for k in range(6):
            x = 50 + k * 12
            s.append("<rect x='%d' y='38' width='5' height='18' fill='#8ab4f8' stroke='%s' stroke-width='1'/>" % (x - 2, INK))
            s.append("<path d='M%.1f 36 Q%.1f 28 %.1f 24 Q%.1f 28 %.1f 36 Z' fill='#f9a03f'/>" % (x - 3, x - 3, x + 0.5, x + 4, x + 4))
        s.append("<line x1='28' y1='94' x2='132' y2='94' stroke='%s' stroke-width='2.5'/>" % INK)
        lab = "a birthday cake with 6 candles"
    elif name == "park":
        s.append("<rect x='1' y='1' width='158' height='102' rx='8' fill='%s'/>" % SKY)
        s.append("<path d='M1 78 L159 78 L159 95 Q159 103 151 103 L9 103 Q1 103 1 95 Z' fill='#81c995'/>")
        s.append("<rect x='44' y='48' width='12' height='34' fill='#8a5a2b' stroke='%s' stroke-width='1.5'/>" % INK)
        s.append("<circle cx='50' cy='36' r='26' fill='#4f9d69' stroke='%s' stroke-width='1.5'/>" % INK)
        s.append("<ellipse cx='112' cy='70' rx='14' ry='9' fill='#c98a3d' stroke='%s' stroke-width='1.5'/>" % INK)
        s.append("<circle cx='124' cy='62' r='7' fill='#ffffff' stroke='%s' stroke-width='1.5'/>" % INK)
        s.append("<circle cx='126' cy='61' r='1.5' fill='%s'/>" % INK)
        s.append("<path d='M130 62 L140 64 L130 66 Z' fill='%s'/>" % INK)
        s.append("<line x1='108' y1='79' x2='108' y2='86' stroke='%s' stroke-width='1.5'/>" % INK)
        s.append("<line x1='116' y1='79' x2='116' y2='86' stroke='%s' stroke-width='1.5'/>" % INK)
        lab = "a park with a tree and a bird"
    elif name == "footy":
        s.append("<rect x='1' y='1' width='158' height='102' rx='8' fill='%s'/>" % SKY)
        s.append("<path d='M1 80 L159 80 L159 95 Q159 103 151 103 L9 103 Q1 103 1 95 Z' fill='#81c995'/>")
        for x, top in ((108, 38), (122, 14), (136, 14), (150, 38)):
            s.append("<line x1='%d' y1='%d' x2='%d' y2='80' stroke='%s' stroke-width='3'/>" % (x, top, x, INK))
        s.append("<ellipse cx='58' cy='56' rx='34' ry='21' fill='#c0392b' stroke='%s' stroke-width='2'/>" % INK)
        s.append("<line x1='46' y1='42' x2='70' y2='42' stroke='#ffffff' stroke-width='2.5'/>")
        for x in (50, 56, 62, 68):
            s.append("<line x1='%d' y1='38' x2='%d' y2='46' stroke='#ffffff' stroke-width='2'/>" % (x, x))
        lab = "a footy and goal posts"
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
    elif name == "icypole":
        s.append("<rect x='1' y='1' width='158' height='102' rx='8' fill='%s'/>" % SKY)
        s.append(sun(124, 30, 15))
        s.append("<rect x='46' y='18' width='30' height='52' rx='12' fill='#f9a03f' stroke='%s' stroke-width='2'/>" % INK)
        s.append("<rect x='57' y='70' width='8' height='24' rx='3' fill='#e9c46a' stroke='%s' stroke-width='1.5'/>" % INK)
        lab = "an icy pole in the hot sun"
    elif name == "race":
        s.append("<rect x='1' y='1' width='158' height='102' rx='8' fill='#f0b48a'/>")
        for k in range(7):
            y = 4 + k * 16
            s.append("<line x1='4' y1='%d' x2='156' y2='%d' stroke='#ffffff' stroke-width='2'/>" % (y, y))
        for k in range(6):
            s.append(text(16, 17 + k * 16, str(k + 1), 14, bold=True))
        s.append("<line x1='134' y1='4' x2='134' y2='100' stroke='%s' stroke-width='3'/>" % INK)
        lab = "a running track with 6 lanes"
    else:
        raise ValueError(name)
    if name != "calendar":
        s.append(frame(W, H))
    return svg_wrap(W, H, "".join(s), lab)


# ------------------------------------------------------------ coins, dice, hat, icy poles, socks
PIPS = {1: [(1, 1)], 2: [(0, 0), (2, 2)], 3: [(0, 0), (1, 1), (2, 2)], 4: [(0, 0), (2, 0), (0, 2), (2, 2)],
        5: [(0, 0), (2, 0), (1, 1), (0, 2), (2, 2)], 6: [(0, 0), (2, 0), (0, 1), (2, 1), (0, 2), (2, 2)]}


def die(x, y, n, sz=46):
    s = ["<rect x='%d' y='%d' width='%d' height='%d' rx='8' fill='#ffffff' stroke='%s' stroke-width='2'/>" % (x, y, sz, sz, INK)]
    st = sz / 4
    for (px, py) in PIPS[n]:
        s.append("<circle cx='%.1f' cy='%.1f' r='%.1f' fill='%s'/>" % (x + st + px * st, y + st + py * st, sz / 10, INK))
    return "".join(s)


def dice_faces_svg(label="the six faces of a dice"):
    sz, gap = 46, 12
    s = []
    for i in range(6):
        x = 4 + i * (sz + gap)
        s.append(die(x, 4, i + 1, sz))
        s.append(text(x + sz / 2, 4 + sz + 20, str(i + 1), 15, bold=True))
    return svg_wrap(4 + 6 * sz + 5 * gap + 4, 4 + sz + 28, "".join(s), label)


def one_die_svg(n):
    return svg_wrap(70, 70, die(6, 6, n, 58), "a dice showing %d" % n)


def coin_svg():
    s = []
    for i, (word, mark) in enumerate([("heads", "H"), ("tails", "T")]):
        cx = 46 + i * 92
        s.append("<circle cx='%d' cy='42' r='36' fill='#e9c46a' stroke='%s' stroke-width='2'/>" % (cx, INK))
        s.append("<circle cx='%d' cy='42' r='29' fill='none' stroke='%s' stroke-width='1'/>" % (cx, INK))
        s.append(text(cx, 52, mark, 28, bold=True))
        s.append(text(cx, 98, word, 16, bold=True))
    return svg_wrap(184, 106, "".join(s), "the two sides of a coin: heads and tails")


def hat_svg(names):
    s = ["<rect x='30' y='8' width='120' height='16' rx='3' fill='#4a4a4a' stroke='%s' stroke-width='2'/>" % INK,
         "<path d='M38 24 L142 24 L134 96 L46 96 Z' fill='#5c5c5c' stroke='%s' stroke-width='2'/>" % INK,
         "<rect x='46' y='70' width='88' height='8' fill='#c0392b'/>"]
    pos = [(64, 42), (116, 42), (64, 60), (116, 60)]
    for (x, y), nm in zip(pos, names):
        s.append("<rect x='%d' y='%d' width='48' height='18' fill='#ffffff' stroke='%s' stroke-width='1'/>" % (x - 24, y - 13, INK))
        s.append(text(x, y + 1, nm, 14, bold=True))
    return svg_wrap(180, 104, "".join(s), "a hat with name cards: " + ", ".join(names))


def icypoles_svg(counts, rnd):
    items = bag_items(counts, rnd)
    s = []
    for i, c in enumerate(items):
        x = 6 + i * 34
        s.append("<rect x='%d' y='6' width='26' height='52' rx='10' fill='%s' stroke='%s' stroke-width='1.5'/>" % (x, COL[c][1], INK))
        s.append("<rect x='%d' y='58' width='8' height='18' rx='3' fill='#e9c46a' stroke='%s' stroke-width='1.2'/>" % (x + 9, INK))
        s.append(text(x + 13, 38, COL[c][0], 15, bold=True))
    W = 6 + len(items) * 34
    lines = key_lines(colours_in([c for c, _ in counts]))
    s.append(text(W / 2, 98, "     ".join(lines), 15))
    return svg_wrap(int(max(W + 2, tw("     ".join(lines), 15) + 8)), 106, "".join(s), "icy poles")


def socks_svg(counts, rnd):
    items = bag_items(counts, rnd)
    s = []
    for i, c in enumerate(items):
        x = 6 + i * 40
        s.append("<path d='M%d 6 H%d V44 H%d Q%d 44 %d 52 Q%d 60 %d 60 H%d Q%d 60 %d 54 Z' fill='%s' stroke='%s' stroke-width='1.5'/>"
                 % (x, x + 18, x + 28, x + 36, x + 36, x + 36, x + 28, x + 6, x, x, COL[c][1], INK))
        s.append("<line x1='%d' y1='14' x2='%d' y2='14' stroke='%s' stroke-width='1'/>" % (x, x + 18, INK))
        s.append(text(x + 9, 36, COL[c][0], 15, bold=True))
    W = 6 + len(items) * 40
    lines = key_lines(colours_in([c for c, _ in counts]))
    s.append(text(W / 2, 94, "     ".join(lines), 15))
    return svg_wrap(int(max(W + 4, tw("     ".join(lines), 15) + 8)), 102, "".join(s), "socks")


# ------------------------------------------------------------ set 1: everyday events
def set_everyday(rnd):
    its = []
    S = lambda n: fig(scene_svg(n))
    its.append(mcq(S("beach") + "A hot summer day at the beach. What won’t happen?", "It will snow.",
                   ["You might see a crab.", "You might swim.", "There will be sand."],
                   "Summer at the beach is warm. Snow never falls on a hot summer beach. So it won’t happen."))
    its.append(mcq(S("beach") + "A hot summer day at the beach. What might happen?", "You might see a dolphin.",
                   ["The sea will turn to milk.", "It will snow on the sand.", "The sand will turn blue."],
                   "Dolphins live in the sea. You see one on some days, but not every day. So it might happen. "
                   "The other things won’t happen."))
    its.append(mcq(S("night") + "It is night. What will happen?", "It will be dark.",
                   ["The sun will shine all night.", "You might hear a frog.", "It might rain."],
                   "Every night the sky is dark. It will happen. A frog or rain might happen, but not for sure."))
    its.append(mcq(S("night") + "It is night. What won’t happen?", "The sun will shine.",
                   ["You might see the Moon.", "You might hear a possum.", "Mum might read a story."],
                   "The sun does not shine at night. That won’t happen. The other things might happen."))
    its.append(mcq(S("sunset") + "Which one will happen?", "The sun will set tonight.",
                   ["It will snow in class.", "Your dog will talk.", "You will see a whale."],
                   "The sun sets every evening, so it will happen. You might see a whale, but not for sure. "
                   "Snow in class and a talking dog won’t happen."))
    its.append(mcq(S("rain") + "Dark clouds fill the sky. What might happen?", "It might rain.",
                   ["It will rain lollies.", "The sky will fall down.", "The clouds will turn into cats."],
                   "Dark clouds often bring rain, but not always. So it might rain. The other things won’t happen."))
    its.append(mcq(S("school") + "It is a school day. What will happen?", "The bell will ring.",
                   ["A cow will be your teacher.", "You might get a sticker.", "You might play cricket."],
                   "The school bell rings every school day, so it will happen. A sticker or cricket might happen."))
    its.append(mcq(S("school") + "It is a school day. What won’t happen?", "A fish will teach the class.",
                   ["You might read a book.", "You might paint.", "You might eat an apple."],
                   "A fish can’t teach. That won’t happen. Reading, painting and eating an apple might happen."))
    its.append(mcq(S("cake") + "Mia is 6 today. What will happen?", "Next year Mia will be 7.",
                   ["Next year Mia will be 3.", "Mia might get a present.", "It might rain at the party."],
                   "Every year you get 1 year older. 6 + 1 = 7, so it will happen. You can’t get younger, so 3 won’t happen."))
    its.append(mcq(S("cake") + "Mia is 6 today. What might happen?", "Mia might get a puppy.",
                   ["Mia will be 100 tomorrow.", "Mia will get younger.", "Next year Mia will be 7."],
                   "A puppy is a gift Mia might get, or might not. So it might happen. "
                   "Being 7 next year will happen. The other two won’t happen."))
    its.append(mcq(S("park") + "At the park. What might happen?", "You might see a kookaburra.",
                   ["A tree will walk away.", "The grass will be pink.", "You will see a dinosaur."],
                   "Kookaburras live in many Australian parks. You might see one, or you might not. "
                   "The other things won’t happen."))
    its.append(mcq(S("park") + "At the park. What won’t happen?", "The tree will fly away.",
                   ["A bird might sing.", "You might go on the swings.", "You might see a dog."],
                   "A tree can’t fly. That won’t happen. The other things might happen."))
    its.append(mcq(S("rain") + "Isla says, “It will rain tomorrow.” Which is better?", "It might rain tomorrow.",
                   ["It will rain tomorrow.", "It won’t rain tomorrow.", "It will rain lollies tomorrow."],
                   "We can’t be sure about rain tomorrow. It may rain, or it may not. So say “might”, not “will”."))
    its.append(mcq(S("beach") + "Leo says, “It might snow at the beach in summer.” Which is better?",
                   "It won’t snow at the beach in summer.",
                   ["It will snow at the beach in summer.", "It might snow at the beach in summer.",
                    "The sea will freeze in summer."],
                   "A summer beach is hot. Snow can’t fall there. So it won’t happen. “Might” is not right."))
    its.append(mcq(S("sunset") + "Jack says, “The sun might set tonight.” Which is better?", "The sun will set tonight.",
                   ["The sun might set tonight.", "The sun won’t set tonight.", "The sun will set at lunch time."],
                   "The sun sets every evening. We are sure, so say “will”, not “might”."))
    its.append(mcq(S("footy") + "Our footy team plays today. Which is right?", "Our team might win.",
                   ["Our team will win.", "Our team won’t win.", "Both teams will win."],
                   "A team can win or lose. We can’t be sure, so our team might win. Both teams can’t win."))
    its.append(mcq(S("calendar") + "Today is Monday. Which is right?", "Tomorrow will be Tuesday.",
                   ["Tomorrow might be Tuesday.", "Tomorrow won’t be Tuesday.", "Tomorrow will be Friday."],
                   "Tuesday always comes after Monday. We are sure, so say “will”."))
    its.append(mcq(S("night") + "Which is right?", "A cow won’t jump over the Moon.",
                   ["A cow will jump over the Moon.", "A cow might jump over the Moon.", "The Moon will fall down."],
                   "The Moon is very, very far away. A cow can’t jump that high. So it won’t happen."))
    its.append(mcq(S("egg") + "Ruby drops an egg on the floor. What will happen?", "The egg will break.",
                   ["The egg will bounce up.", "The egg will turn into a chick.", "The egg will fly away."],
                   "An egg shell is thin. When it hits the hard floor, it breaks. So it will happen."))
    its.append(mcq(S("icypole") + "An icy pole is left in the hot sun. What will happen?", "It will melt.",
                   ["It will get bigger.", "It will get colder.", "It will turn into a lolly."],
                   "The hot sun melts ice. So the icy pole will melt. It won’t get bigger or colder."))
    assert len(its) == 20
    return {"title": "Will happen, might happen or won’t happen?", "items": its}


# ------------------------------------------------------------ set 2: spinners
def set_spinners(rnd):
    its = []
    F = lambda sec: fig(spinner_svg(sec))

    def sp(sec, target, other, e, q="You spin it. Which is right?"):
        return st_q(F(sec) + q, amounts(sec), target, "get", other, e)

    its.append(sp(eq("red", "red", "red", "red"), "red", "blue",
                  "All the parts are red. The arrow must land on red. So you will get red."))
    its.append(sp(eq("red", "blue"), "red", "yellow",
                  "Half is red and half is blue. The arrow can land on either one. So you might get red."))
    its.append(sp(eq("red", "blue", "yellow"), "green", "red",
                  "There is no green part. The arrow can’t land on green. So you won’t get green."))
    its.append(sp(eq("blue", "blue", "red", "blue"), "blue", "green",
                  "Most parts are blue. But there is 1 red part, so the arrow could land on red. "
                  "So you might get blue. It is not “will”."))
    its.append(sp(eq("yellow", "yellow", "yellow", "yellow", "yellow", "yellow"), "yellow", "blue",
                  "Every part is yellow. You will get yellow. There is no blue."))
    its.append(sp(eq("red", "green", "green", "green"), "red", "purple",
                  "Only 1 part is red. But it is there, so the arrow can land on it. You might get red. "
                  "It is not “won’t”."))
    its.append(sp(eq(1, 2, 3, 4), "5", "1",
                  "The numbers are 1, 2, 3 and 4. There is no 5. So you won’t get 5."))
    its.append(sp(eq(1, 2, 3, 4), "4", "6",
                  "4 is on the spinner, so you might get it. A big number is not harder to get."))
    its.append(sp(eq(2, 2, 2, 2), "2", "1",
                  "Every part has a 2. The arrow must land on 2. So you will get 2."))
    its.append(mcq(F(eq("green", "green", "green")) + "Which colour will you get?", "green",
                   ["red", "blue", "yellow"],
                   "Every part is green. So you will get green."))
    its.append(mcq(F(eq("red", "blue", "yellow")) + "Which colour won’t you get?", "green",
                   ["red", "blue", "yellow"],
                   "The spinner has red, blue and yellow. There is no green. So you won’t get green."))
    its.append(mcq(F(eq("green", "purple", "yellow", "purple")) + "Which colour won’t you get?", "red",
                   ["green", "purple", "yellow"],
                   "Look at the spinner. It has green, purple and yellow. There is no red."))
    its.append(mcq(F(eq(1, 2, 3, 4, 5, 6)) + "Which number won’t you get?", "7",
                   ["1", "6", "3"],
                   "The numbers go from 1 to 6. There is no 7. So you won’t get 7."))
    S = lambda spins: fig(spinners_abcd(spins))
    its.append(abcd_q(S([eq("red", "blue"), eq("red", "red", "red", "red"), eq("blue", "yellow", "blue"),
                         eq("red", "red", "blue", "red")]) + "Which spinner will land on red?", "Spinner", 1,
                      "Spinner B is all red. It must land on red. Spinner D is mostly red, "
                      "but it has a blue part. So D might land on red."))
    its.append(abcd_q(S([eq("red", "blue", "red", "blue"), eq("red", "yellow", "yellow", "yellow"),
                         eq("red", "red", "red", "red"), eq("blue", "green", "yellow", "green")]) +
                      "Which spinner won’t land on red?", "Spinner", 3,
                      "Spinner D has no red part. So it won’t land on red. Spinner B has 1 red part, so it might."))
    its.append(abcd_q(S([eq("blue", "blue", "blue", "blue"), eq("red", "red", "red", "red"),
                         eq("yellow", "green", "yellow", "green"), eq("red", "blue", "red", "blue")]) +
                      "Which spinner might land on red?", "Spinner", 3,
                      "Spinner D has red parts and blue parts. It might land on red, or it might land on blue. "
                      "B will land on red. A and C won’t."))
    its.append(mcq(F(eq("blue", "red", "blue", "red")) + "Leo says, “I will get blue.” Is he right?",
                   "No. He might get blue.",
                   ["Yes. He will get blue.", "No. He won’t get blue.", "Yes. Blue is his favourite."],
                   "Half the spinner is red. The arrow might land on red. So Leo might get blue. "
                   "His favourite colour does not change the spinner."))
    its.append(mcq(F(eq("red", "red", "yellow", "red")) + "Amelia says, “I won’t get yellow. It is too small.” Is she right?",
                   "No. She might get yellow.",
                   ["Yes. She won’t get yellow.", "No. She will get yellow.", "Yes. Red always wins."],
                   "There is 1 yellow part. The arrow can land on it. So she might get yellow. It is not “won’t”."))
    its.append(sp(eq("red", "blue", "yellow", "green"), "yellow", "purple",
                  "There is 1 yellow part out of 4. The arrow can land on it, or on another colour. So you might get yellow."))
    its.append(sp(eq("purple", "purple", "purple", "purple"), "green", "purple",
                  "Every part is purple. There is no green. So you won’t get green."))
    assert len(its) == 20
    return {"title": "Spinners: can you get red?", "items": its}


# ------------------------------------------------------------ set 3: bags of counters
def set_bags(rnd):
    its = []
    B = lambda counts: fig(bag_svg(counts, rnd))

    def bq(counts, target, other, e, q="You pick one without looking. Which is right?"):
        return st_q(B(counts) + q, dict(counts), target, "pick", other, e)

    its.append(bq([("red", 5)], "red", "blue", "Every counter is red. You will pick red."))
    its.append(bq([("red", 3), ("blue", 3)], "blue", "yellow",
                  "There are red and blue counters. You could pick either one. So you might pick blue."))
    its.append(bq([("red", 4), ("yellow", 2)], "green", "red",
                  "Look in the bag. There are red and yellow counters. There is no green. So you won’t pick green."))
    its.append(bq([("blue", 5), ("red", 1)], "red", "green",
                  "There is only 1 red counter. But it is in the bag, so you could pick it. You might pick red."))
    its.append(bq([("green", 7), ("red", 1)], "green", "yellow",
                  "Most counters are green. But there is 1 red counter. So you might pick green. It is not “will”."))
    its.append(bq([("yellow", 4), ("purple", 2)], "yellow", "blue",
                  "There are yellow and purple counters. You could pick a purple one. So you might pick yellow."))
    its.append(mcq(B([("yellow", 6)]) + "Which colour will you pick?", "yellow", ["red", "blue", "green"],
                   "Every counter is yellow. So you will pick yellow."))
    its.append(mcq(B([("red", 2), ("blue", 2), ("yellow", 2)]) + "Which colour won’t you pick?", "green",
                   ["red", "blue", "yellow"],
                   "The bag has red, blue and yellow counters. There is no green. So you won’t pick green."))
    its.append(mcq(B([("green", 3), ("purple", 2), ("blue", 1)]) + "Which colour won’t you pick?", "red",
                   ["green", "purple", "blue"],
                   "The bag has green, purple and blue. There is no red. So you won’t pick red. "
                   "There is 1 blue, so you might pick blue."))
    its.append(mcq(B([("red", 3), ("blue", 3)]) + "Mia wants a green counter. Can she get one?", "No. There is no green.",
                   ["Yes. She might get green.", "Yes. She will get green.", "Yes, if she shuts her eyes."],
                   "Look in the bag first. There are only red and blue counters. No green means she won’t get green."))
    its.append(mcq(B([("red", 1), ("blue", 5)]) + "Kai wants a red counter. Can he get one?", "Yes. He might get red.",
                   ["No. There is no red.", "Yes. He will get red.", "No. He won’t get red."],
                   "There is 1 red counter in the bag. Kai could pick it. So he might get red."))
    its.append(st_q(B([("red", 3), ("blue", 3)]) + "Ava takes out all the blue counters. Then she picks one. Which is right?",
                    {"red": 3}, "red", "pick", "blue",
                    "After the blue counters come out, only red counters are left. So she will pick red.", who="She"))
    its.append(st_q(B([("red", 4)]) + "Noah puts 2 green counters in the bag. Then he picks one. Which is right?",
                    {"red": 4, "green": 2}, "green", "pick", "blue",
                    "Now the bag has red and green counters. So he might pick green. Before, green was “won’t”.", who="He"))
    G = lambda bags: fig(bags_abcd(bags, rnd))
    its.append(abcd_q(G([[("red", 3), ("blue", 3)], [("blue", 6)], [("red", 5), ("yellow", 1)], [("red", 6)]]) +
                      "Which bag will give you red?", "Bag", 3,
                      "Bag D has only red counters. You will pick red. Bag C has a yellow counter, so red might happen there."))
    its.append(abcd_q(G([[("red", 4), ("blue", 2)], [("yellow", 3), ("green", 3)], [("blue", 6)], [("blue", 1), ("red", 5)]]) +
                      "Which bag won’t give you blue?", "Bag", 1,
                      "Bag B has yellow and green counters. There is no blue. So it won’t give you blue."))
    its.append(abcd_q(G([[("red", 6)], [("yellow", 2), ("red", 4)], [("blue", 6)], [("green", 3), ("blue", 3)]]) +
                      "Which bag might give you yellow?", "Bag", 1,
                      "Only bag B has yellow counters, and it has red ones too. So you might pick yellow from bag B."))
    its.append(mcq(B([("red", 2), ("blue", 4)]) + "Grace says, “I will pick red. Red is my favourite.” Is she right?",
                   "No. She might pick red.",
                   ["Yes. She will pick red.", "No. She won’t pick red.", "Yes. Red is her favourite."],
                   "The bag has blue counters too. Her favourite colour does not change what she picks. "
                   "So she might pick red."))
    its.append(bq([("red", 2), ("yellow", 2), ("blue", 2)], "yellow", "green",
                  "There are 2 yellow counters. You could pick one, or a red or blue one. So you might pick yellow."))
    its.append(mcq(B([("red", 6)]) + "Isla picks 2 counters. What will happen?", "She will get 2 red ones.",
                   ["She might get a blue one.", "She will get 1 red, 1 blue.", "She won’t get red."],
                   "Every counter is red. Any 2 counters she picks will be red."))
    its.append(mcq(B([("blue", 2), ("green", 2)]) + "Cooper wants a yellow counter. What can he do?",
                   "Put a yellow one in the bag.",
                   ["Pick again and again.", "Shake the bag.", "Pick very fast."],
                   "There is no yellow in the bag, so he won’t get yellow. Picking again or shaking does not help. "
                   "He must put a yellow counter in."))
    assert len(its) == 20
    return {"title": "Bags of counters: what could you pick?", "items": its}


# ------------------------------------------------------------ set 4: which is more likely?
def more_q(pic, counts, q, ask_less, extra, e):
    """Choices: the two colours, 'the same', and an extra (a colour that is not there)."""
    (a, na), (b, nb) = counts
    if na == nb:
        corr = "the same"
    else:
        big, small = (a, b) if na > nb else (b, a)
        corr = small if ask_less else big
    return mcq(pic + q, corr, [a, b, "the same", extra], e)


def set_more(rnd):
    its = []
    F = lambda sec: fig(spinner_svg(sec))
    B = lambda counts: fig(bag_svg(counts, rnd))
    Q = "Which colour are you more likely to get?"
    its.append(more_q(F(eq("red", "red", "blue", "red")), [("red", 3), ("blue", 1)], Q, False, "green",
                      "3 parts are red. Only 1 part is blue. More red means red is more likely."))
    its.append(more_q(F(eq("green", "yellow", "yellow", "yellow")), [("green", 1), ("yellow", 3)], Q, False, "red",
                      "3 parts are yellow and 1 part is green. Yellow covers more, so yellow is more likely."))
    its.append(more_q(F(eq("red", "blue", "red", "blue")), [("red", 2), ("blue", 2)], Q, False, "yellow",
                      "2 parts are red and 2 parts are blue. The parts are the same size. So they are the same."))
    its.append(more_q(B([("blue", 6), ("red", 2)]), [("blue", 6), ("red", 2)], "Which colour are you more likely to pick?",
                      False, "yellow", "There are 6 blue counters and 2 red counters. More blue means blue is more likely."))
    its.append(more_q(B([("yellow", 2), ("green", 6)]), [("yellow", 2), ("green", 6)],
                      "Which colour are you less likely to pick?", True, "red",
                      "There are only 2 yellow counters and 6 green ones. Fewer yellow means yellow is less likely."))
    its.append(more_q(B([("red", 3), ("blue", 3)]), [("red", 3), ("blue", 3)], "Which colour are you more likely to pick?",
                      False, "green", "3 red and 3 blue. The same number, so they are the same."))
    its.append(more_q(F(eq("green", "green", "green", "purple", "green", "green")), [("green", 5), ("purple", 1)],
                      "Which colour are you less likely to get?", True, "blue",
                      "Only 1 part is purple. 5 parts are green. So purple is less likely."))
    its.append(mcq(F(eq(1, 1, 2, 1)) + "Which number are you more likely to get?", "1", ["2", "the same", "3"],
                   "3 parts have a 1. Only 1 part has a 2. So 1 is more likely."))
    its.append(mcq(F(eq(1, 2, 3, 4)) + "Which is more likely, 1 or 4?", "the same", ["4", "1", "5"],
                   "1 and 4 each have 1 part. The parts are the same size. So they are the same. "
                   "A bigger number is not harder to get."))
    its.append(mcq(B([("red", 4), ("blue", 2), ("yellow", 1)]) + "Which colour are you most likely to pick?", "red",
                   ["blue", "yellow", "the same"],
                   "Count each colour: red 4, blue 2, yellow 1. Red has the most, so red is most likely."))
    its.append(mcq(B([("red", 4), ("blue", 2), ("yellow", 1)]) + "Which colour are you least likely to pick?", "yellow",
                   ["red", "blue", "the same"],
                   "Count each colour: red 4, blue 2, yellow 1. Yellow has the fewest, so yellow is least likely."))
    its.append(mcq(F(eq("purple", "green", "green", "green")) + "Harper loves purple. Which colour is she more likely to get?",
                   "green", ["purple", "the same", "red"],
                   "3 parts are green and only 1 is purple. Her favourite colour does not change the spinner. Green is more likely."))
    its.append(mcq(B([("red", 5), ("blue", 1)]) + "Jack wants blue. What is more likely?", "He gets red.",
                   ["He gets blue.", "Both are the same.", "He gets green."],
                   "Look in the bag: 5 red and 1 blue. Wanting blue does not help. Red is more likely."))
    S = lambda spins: fig(spinners_abcd(spins))
    its.append(abcd_q(S([eq("red", "blue", "blue", "blue"), eq("red", "blue", "red", "blue"),
                         eq("red", "red", "blue", "red"), eq("blue", "blue", "blue", "blue")]) +
                      "Which spinner is best for getting red?", "Spinner", 2,
                      "Spinner C has 3 red parts out of 4. That is the most red. Spinner D has no red at all."))
    its.append(abcd_q(S([eq("yellow", "yellow", "red", "yellow"), eq("yellow", "red", "yellow", "red"),
                         eq("yellow", "red", "red", "red"), eq("yellow", "yellow", "yellow", "yellow")]) +
                      "Which spinner is worst for getting yellow?", "Spinner", 2,
                      "Spinner C has only 1 yellow part. The others have more yellow. So C is worst for yellow."))
    G = lambda bags: fig(bags_abcd(bags, rnd))
    its.append(abcd_q(G([[("blue", 2), ("red", 4)], [("blue", 1), ("red", 5)], [("blue", 5), ("red", 1)], [("blue", 3), ("red", 3)]]) +
                      "Which bag is best for picking blue?", "Bag", 2,
                      "Each bag has 6 counters. Bag C has 5 blue counters. That is the most blue."))
    its.append(abcd_q(G([[("red", 4), ("blue", 2)], [("red", 3), ("blue", 3)], [("red", 1), ("blue", 5)], [("red", 6)]]) +
                      "In which bag are red and blue the same?", "Bag", 1,
                      "Bag B has 3 red and 3 blue. The same number of each, so they are the same."))
    its.append(mcq(B([("red", 2), ("blue", 2)]) + "Ethan puts 3 more red counters in. Which colour is more likely now?",
                   "red", ["blue", "the same", "green"],
                   "Red: 2 + 3 = 5. Blue: 2. 5 is more than 2, so red is now more likely."))
    its.append(mcq(fig(scene_svg("beach")) + "Summer at the beach. Which is more likely?", "a hot day",
                   ["a snowy day", "a frosty day", "the same"],
                   "Summer days at the beach are usually hot. Snow and frost won’t happen there in summer."))
    its.append(mcq(fig(scene_svg("rain")) + "The sky is full of dark clouds. Which is more likely?", "rain",
                   ["a sunny sky", "snow on the beach", "the same"],
                   "Dark clouds often bring rain. So rain is more likely."))
    assert len(its) == 20
    return {"title": "Which is more likely?", "items": its}


# ------------------------------------------------------------ set 5: coins, dice and stories
def set_coins_dice(rnd):
    its = []
    C = fig(coin_svg())
    D = fig(dice_faces_svg())
    its.append(st_q(C + "You toss a coin. Which is right?", {"heads": 1, "tails": 1}, "heads", "get", "6",
                    "A coin can land on heads or tails. So you might get heads."))
    its.append(mcq(C + "You toss a coin. What can you get?", "heads or tails",
                   ["only heads", "only tails", "1, 2 or 3"],
                   "A coin has 2 sides: heads and tails. It can land on either side."))
    its.append(mcq(D + "You roll a dice. Which number won’t you get?", "7", ["1", "6", "3"],
                   "A dice has 1 to 6 dots. There is no 7. So you won’t get 7."))
    its.append(st_q(D + "You roll a dice. Which is right?", {str(k): 1 for k in range(1, 7)}, "6", "get", "0",
                    "6 is on the dice. It might come up, or another number might. So you might get 6."))
    its.append(mcq(D + "You roll a dice. What will happen?", "You will get 1, 2, 3, 4, 5 or 6.",
                   ["You will get 6.", "You might get 8.", "You won’t get 1."],
                   "Every face has 1, 2, 3, 4, 5 or 6 dots. One of them must come up. So that will happen."))
    its.append(st_q(D + "You roll a dice. Which is right?", {str(k): 1 for k in range(1, 7)}, "9", "get", "4",
                    "The dice only goes up to 6. There is no 9. So you won’t get 9."))
    its.append(mcq(D + "Noah says, “6 is hard to get. It is a big number.” Is he right?",
                   "No. 6 and 1 have the same chance.",
                   ["Yes. 6 is harder to get.", "No. 6 is easier to get.", "Yes. You won’t get 6."],
                   "Each number is on 1 face. So every number has the same chance. Big numbers are not harder."))
    its.append(mcq(C + "Which is right?", "Heads and tails have the same chance.",
                   ["Heads is more likely.", "Tails is more likely.", "You won’t get tails."],
                   "A coin has 1 heads side and 1 tails side. So heads and tails have the same chance."))
    its.append(mcq(C + "Kai gets heads 3 times. He tosses again. Which is right?",
                   "He might get heads or tails.",
                   ["He will get tails.", "He will get heads.", "He won’t get heads."],
                   "A coin does not remember. Each toss, heads and tails have the same chance. So he might get either one."))
    its.append(mcq(C + "Harper says, “I will get heads. Heads is lucky.” Is she right?",
                   "No. She might get heads.",
                   ["Yes. She will get heads.", "No. She won’t get heads.", "Yes. Heads is lucky."],
                   "No side is lucky. The coin might land on heads or tails. So she might get heads."))
    its.append(mcq(C + "The umpire tosses a coin before the footy. Our captain calls heads. Which is right?",
                   "Our captain might win the toss.",
                   ["Our captain will win the toss.", "Our captain won’t win the toss.", "Both captains will win."],
                   "The coin might land on heads, or on tails. So our captain might win. Both can’t win."))
    its.append(mcq(fig(one_die_svg(6)) + "Leo needs a 6 to start the game. He rolls a dice. Which is right?",
                   "Leo might get a 6.",
                   ["Leo will get a 6.", "Leo won’t get a 6.", "Leo might get a 10."],
                   "6 is on the dice, so he might get it. He might get another number too. There is no 10."))
    its.append(st_q(fig(bag_svg([("red", 6), ("yellow", 1)], rnd, "lucky dip bag of balls")) +
                    "At the school fete lucky dip, the yellow ball wins a big prize. Ava picks one ball. Which is right?",
                    {"red": 6, "yellow": 1}, "yellow", "pick", "blue",
                    "There is 1 yellow ball. Ava could pick it, but there are lots of red ones too. So she might pick yellow.",
                    who="Ava"))
    its.append(mcq(fig(hat_svg(["Mia", "Leo", "Kai", "Ava"])) + "The teacher picks one name from the hat. Which is right?",
                   "Leo might be picked.",
                   ["Leo will be picked.", "Leo won’t be picked.", "Ruby might be picked."],
                   "Leo’s name is in the hat with 3 other names. So Leo might be picked. "
                   "Ruby’s name is not in the hat, so she won’t be picked."))
    its.append(mcq(fig(hat_svg(["Mia", "Leo", "Kai", "Ava"])) + "Ruby’s name is not in the hat. Which is right?",
                   "Ruby won’t be picked.",
                   ["Ruby might be picked.", "Ruby will be picked.", "Mia won’t be picked."],
                   "Only names in the hat can be picked. Ruby’s name is not there. So she won’t be picked."))
    its.append(mcq(fig(icypoles_svg([("red", 4), ("yellow", 2)], rnd)) +
                   "The canteen has 4 red and 2 yellow icy poles. Chloe takes one without looking. Which is more likely?",
                   "a red one", ["a yellow one", "the same", "a green one"],
                   "There are 4 red and 2 yellow. More red means red is more likely. There are no green ones."))
    its.append(mcq(fig(socks_svg([("red", 3), ("blue", 3)], rnd)) +
                   "Ruby picks a sock in the dark. Which is right?", "She might get a red sock.",
                   ["She will get a red sock.", "She won’t get a red sock.", "She will get a green sock."],
                   "There are red socks and blue socks. In the dark she could get either one. So she might get red."))
    its.append(mcq(fig(scene_svg("race")) + "6 children run a race. Jack is one of them. Which is right?",
                   "Jack might win.",
                   ["Jack will win.", "Jack won’t win.", "All 6 will win."],
                   "Any of the 6 children could win. We can’t be sure it is Jack. So Jack might win."))
    its.append(mcq(fig(scene_svg("rain")) + "It is a cold winter day in Hobart. The sky is grey. Which is right?",
                   "It might rain today.",
                   ["It will rain today.", "It won’t rain today.", "It will be a hot summer day."],
                   "Grey clouds can bring rain, but not always. So it might rain. It is winter, so it won’t be a summer day."))
    its.append(mcq(fig(icypoles_svg([("yellow", 3)], rnd)) +
                   "The canteen has only yellow icy poles left. Liam takes one. Which is right?",
                   "He will get a yellow one.",
                   ["He might get a red one.", "He won’t get a yellow one.", "He might get a blue one."],
                   "Every icy pole left is yellow. So he will get a yellow one."))
    assert len(its) == 20
    return {"title": "Coins, dice and chance stories", "items": its}


# ------------------------------------------------------------ lesson
def ex(title, q, s, a):
    return ("<div class='sn-ex'><span class='sn-ex-t'>%s</span><p class='sn-ex-q'>%s</p>"
            "<p class='sn-ex-s'>%s</p><p class='sn-ex-a'>Answer: %s</p></div>" % (title, q, s, a))


def table(head, rows, cls="sn-table"):
    h = "".join("<th>%s</th>" % x for x in head)
    b = "".join("<tr>" + "".join("<td>%s</td>" % c for c in r) + "</tr>" for r in rows)
    return "<div class='sn-tw'><table class='%s'><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>" % (cls, h, b)


def body_html(rnd):
    return (
        "<h2>Three chance words</h2>"
        "<p>Some things we are sure about. Some things we are not sure about. We use three phrases.</p>" +
        table(["Words", "Meaning", "Example"], [
            ["<b>will happen</b>", "We are sure it happens.", "The sun will set tonight."],
            ["<b>might happen</b>", "It can happen, but we are not sure.", "It might rain tomorrow."],
            ["<b>won’t happen</b>", "It can’t happen.", "It won’t snow at the beach in summer."],
        ]) +
        "<figure class='sn-fig'>" + scene_svg("sunset") +
        "<figcaption>The sun sets every evening. It will happen.</figcaption></figure>" +
        ex("Will, might or won’t?", "Our team plays footy today. Will we win?",
           "A team can win or lose. We are not sure.", "Our team might win.") +
        "<h2>Spinners</h2>"
        "<p>Look at the colours on the spinner. If <b>all</b> the parts are red, you <b>will</b> get red. "
        "If <b>some</b> parts are red, you <b>might</b> get red. If <b>no</b> parts are red, you <b>won’t</b> get red.</p>"
        "<figure class='sn-fig'>" + spinner_svg(eq("red", "red", "blue", "red"), "spinner: 3 red parts and 1 blue part") +
        "<figcaption>3 red parts and 1 blue part. You might get red. You might get blue. You won’t get green.</figcaption></figure>" +
        ex("Example", "Will you get red?", "Most parts are red, but there is a blue part.", "No. You might get red.") +
        "<h2>Bags of counters</h2>"
        "<p>Look in the bag <b>before</b> you answer. You can only pick a colour that is in the bag. "
        "The colour with <b>more</b> counters is <b>more likely</b>.</p>"
        "<figure class='sn-fig'>" + bag_svg([("red", 5), ("blue", 1)], rnd, "bag: 5 red counters and 1 blue counter") +
        "<figcaption>5 red counters and 1 blue counter. Red is more likely. You might still pick blue.</figcaption></figure>" +
        ex("Example", "Can you pick blue?", "There is 1 blue counter. It is in the bag.", "Yes. You might pick blue.") +
        "<h2>Coins and dice</h2>"
        "<p>A coin can land on <b>heads</b> or <b>tails</b>. A dice can show 1, 2, 3, 4, 5 or 6. "
        "Every number has the same chance. You won’t roll a 7.</p>"
        "<figure class='sn-fig'>" + dice_faces_svg() +
        "<figcaption>The 6 faces of a dice. A 6 is just as likely as a 1.</figcaption></figure>"
        "<h2>Common mistakes</h2>" +
        table(["Mistake", "What to do instead"], [
            ["Saying “will” when it only might happen", "Use “will” only when you are sure"],
            ["Saying “won’t” when there is only a little of a colour", "If it is there at all, it might happen"],
            ["Not looking in the bag", "Check which colours are in the bag first"],
            ["Choosing your favourite colour", "Count the parts or counters of each colour"],
            ["Thinking 6 is harder to roll than 1", "Every number on a dice has the same chance"],
        ])
    )


FAQ = [
    {"q": "What do Year 1 students learn about chance in Australia?",
     "a": "The Australian Curriculum (AC9M1P01) asks Year 1 students to talk about familiar events and say whether they will happen, won’t happen or might happen. For example, the sun will set tonight, but it won’t snow at the beach in summer."},
    {"q": "What is the difference between “will happen” and “might happen”?",
     "a": "“Will happen” means we are sure, like Tuesday coming after Monday. “Might happen” means it can happen but we are not sure, like rain tomorrow."},
    {"q": "How can I teach chance to a 6-year-old at home?",
     "a": "Use a bag of coloured blocks or a homemade spinner. Ask “Will you get red, might you get red, or won’t you get red?” and then try it to see."},
    {"q": "Why does my child say a colour won’t come up when it is on the spinner?",
     "a": "Many children think a small part can never be landed on. Spin a few times together and show that if a colour is there at all, it might happen."},
]


def balance(sets, rnd):
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


def mark_large(u, pattern):
    rx = re.compile(r"<svg (?=[^>]*aria-label='(?:" + pattern + ")')")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u


def gen_unit():
    rnd = random.Random(1813)
    sets = [set_everyday(rnd), set_spinners(rnd), set_bags(rnd), set_more(rnd), set_coins_dice(rnd)]
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
    u = {
        "country": "au", "subject": "maths", "grade": "year-1", "slug": "chance", "sort": 13,
        "updated": UPDATED, "pdf_url": "",
        "title": "Chance: Will Happen, Might Happen or Won’t Happen",
        "seo_title": "Year 1 Chance Worksheets: Will, Might or Won’t Happen (Free, with Answer Key)",
        "short_title": "Chance",
        "domain": "Probability",
        "standard_code": "AC9M1P01",
        "standard_url": "https://v9.australiancurriculum.edu.au/f-10-curriculum/learning-areas/mathematics",
        "standard_text": "Identify outcomes of familiar events involving chance and describe them using everyday language, such as “will happen”, “won’t happen” or “might happen”",
        "meta_desc": "Free Year 1 maths worksheets on chance for the Australian Curriculum: say if everyday events will happen, might happen or won’t happen, find what you can get on a spinner or from a bag of counters, choose which colour is more likely, and toss coins and roll dice. 100 questions with an answer key.",
        "key_big": "Will happen means we are sure. Might happen means it can happen, but we are not sure. Won’t happen means it can’t happen.",
        "key_sub": "If all the parts of a spinner are red, you will get red. If some are red, you might get red. If none are red, you won’t get red. Always look at what is in the bag first.",
        "body_html": body_html(rnd), "faq": FAQ, "sets": sets,
    }
    return mark_large(u, "spinners A to D|bags A to D|the six faces of a dice|socks|icy poles")


if __name__ == "__main__":
    u = gen_unit()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
