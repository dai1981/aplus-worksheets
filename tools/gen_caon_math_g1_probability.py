# -*- coding: utf-8 -*-
"""
Canada (Ontario) Grade 1 Math: Probability (Ontario Mathematics Curriculum 2020: Grade 1, D2.1)
  python3 tools/gen_caon_math_g1_probability.py
Everyday events, spinners, bags of counters, predictions (which colour will you probably pick?) and word problems.
Only the three Grade 1 words: impossible, possible, certain.
Wrong answers come from real mistakes: "certain" for something that only happens a lot (possible vs certain),
"impossible" when there is only a little of a colour, "impossible" because it is not happening right now,
ignoring what is in the bag, choosing a favourite colour, thinking a big number is hard to roll.
Every picture shows the colour as a letter too (R = red ...), so it still works when printed in black and white.
Grade 1: very short sentences for 6-7 year olds, a picture in every question.
HTML attributes use single quotes (no backslashes in the JSON). Canadian English.
"""
import json, math, os, random, re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "ca-on", "math", "grade-1")
UPDATED = "2026-11-02"
GREEN = "#006633"
FILL = "#cfe6d6"
INK = "#2b2b2b"
FONT = "Arial, Helvetica, sans-serif"

COL = {
    "red": ("R", "#f28b82"),
    "blue": ("B", "#8ab4f8"),
    "yellow": ("Y", "#fde293"),
    "green": ("G", "#81c995"),
    "purple": ("P", "#c58af9"),
}
WORDS = ["impossible", "possible", "certain"]


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


def word_of(counts, target):
    n = counts.get(target, 0)
    tot = sum(counts.values())
    return "certain" if n == tot else ("impossible" if n == 0 else "possible")


# the most common wrong word for each right word
MISTAKE = {"impossible": "possible", "possible": "certain", "certain": "impossible"}


def cap(s):
    return s[0].upper() + s[1:]


def say(thing, w):
    return "%s is %s." % (cap(str(thing)), w)


def st_q(q, counts, target, other, e):
    """Which is right? Correct: the right word for target.
    Wrong: the other two words for target, and a wrong word for another thing."""
    w = word_of(counts, target)
    wo = word_of(counts, other)
    correct = say(target, w)
    cands = [say(target, x) for x in WORDS if x != w] + [say(other, MISTAKE[wo])]
    return mcq(q, correct, cands, e)


WC = "certain: it must happen"
WP = "possible: it may happen"
WI = "impossible: it can’t happen"
WREASON = {"certain": WC, "possible": WP, "impossible": WI}


def word_q(q, w, fourth, e):
    """Which word fits? The three words with a reason, plus one real wrong reason."""
    return mcq(q, WREASON[w], [x for k, x in WREASON.items() if k != w] + [fourth], e)


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


GROUND = "M1 %d L159 %d L159 95 Q159 103 151 103 L9 103 Q1 103 1 95 Z"


def scene_svg(name, day="Monday"):
    W, H = 160, 104
    s = []
    if name == "beach":
        s.append("<rect x='1' y='1' width='158' height='102' rx='8' fill='%s'/>" % SKY)
        s.append(sun(128, 26, 13))
        s.append("<rect x='1' y='54' width='158' height='20' fill='#8ab4f8'/>")
        s.append("<path d='%s' fill='#f4e2b0'/>" % (GROUND % (74, 74)))
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
        s.append("<path d='%s' fill='#2e5b3a'/>" % (GROUND % (84, 84)))
        lab = "the Moon and stars at night"
    elif name == "sunrise":
        s.append("<rect x='1' y='1' width='158' height='102' rx='8' fill='#fbd7a5'/>")
        s.append("<circle cx='80' cy='70' r='24' fill='#f9a03f' stroke='#d9822b' stroke-width='2'/>")
        for a in (-150, -120, -90, -60, -30):
            r = math.radians(a)
            s.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='#d9822b' stroke-width='2.5'/>"
                     % (80 + 30 * math.cos(r), 70 + 30 * math.sin(r), 80 + 40 * math.cos(r), 70 + 40 * math.sin(r)))
        s.append("<path d='%s' fill='#81c995'/>" % (GROUND % (70, 70)))
        s.append("<line x1='1' y1='70' x2='159' y2='70' stroke='%s' stroke-width='1.5'/>" % INK)
        lab = "the sun coming up in the morning"
    elif name == "rain":
        s.append("<rect x='1' y='1' width='158' height='102' rx='8' fill='#e3e7ec'/>")
        s.append(cloud(80, 34, 1.3, "#c4ccd6"))
        for k in range(7):
            x = 40 + k * 13
            s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='#3b78c4' stroke-width='2.5' stroke-linecap='round'/>"
                     % (x, 66 + (k % 2) * 8, x - 4, 78 + (k % 2) * 8))
        lab = "dark rain clouds"
    elif name == "snow":
        s.append("<rect x='1' y='1' width='158' height='102' rx='8' fill='#c9d6e3'/>")
        s.append("<path d='%s' fill='#ffffff'/>" % (GROUND % (76, 76)))
        s.append("<line x1='1' y1='76' x2='159' y2='76' stroke='#7a8a99' stroke-width='1.5'/>")
        s.append("<circle cx='112' cy='72' r='16' fill='#ffffff' stroke='%s' stroke-width='1.5'/>" % INK)
        s.append("<circle cx='112' cy='46' r='11' fill='#ffffff' stroke='%s' stroke-width='1.5'/>" % INK)
        s.append("<circle cx='108' cy='44' r='1.6' fill='%s'/>" % INK)
        s.append("<circle cx='116' cy='44' r='1.6' fill='%s'/>" % INK)
        s.append("<path d='M112 48 L120 50 L112 51 Z' fill='#f9a03f'/>")
        s.append("<rect x='103' y='54' width='18' height='4' fill='#f28b82'/>")
        for (x, y) in [(20, 16), (44, 30), (70, 14), (30, 52), (60, 44), (88, 26), (140, 18), (146, 44), (84, 58), (16, 36)]:
            s.append("<circle cx='%d' cy='%d' r='3' fill='#ffffff' stroke='#7a8a99' stroke-width='0.8'/>" % (x, y))
        lab = "a snowy winter day with a snowman"
    elif name == "school":
        s.append("<rect x='1' y='1' width='158' height='102' rx='8' fill='%s'/>" % SKY)
        s.append("<rect x='30' y='42' width='100' height='54' fill='#f4e2b0' stroke='%s' stroke-width='2'/>" % INK)
        s.append("<path d='M24 42 L80 16 L136 42 Z' fill='#c0392b' stroke='%s' stroke-width='2'/>" % INK)
        s.append("<rect x='70' y='68' width='20' height='28' fill='#8a5a2b' stroke='%s' stroke-width='1.5'/>" % INK)
        for x in (40, 104):
            s.append("<rect x='%d' y='54' width='16' height='14' fill='#8ab4f8' stroke='%s' stroke-width='1.5'/>" % (x, INK))
        s.append(text(80, 38, "SCHOOL", 14, bold=True, col="#ffffff"))
        lab = "a school"
    elif name == "bus":
        s.append("<rect x='1' y='1' width='158' height='102' rx='8' fill='%s'/>" % SKY)
        s.append("<rect x='1' y='84' width='158' height='18' fill='#9aa3ab'/>")
        s.append("<rect x='16' y='30' width='128' height='50' rx='6' fill='#f6c445' stroke='%s' stroke-width='2'/>" % INK)
        for x in (24, 48, 72, 96):
            s.append("<rect x='%d' y='38' width='18' height='16' fill='#dff0fb' stroke='%s' stroke-width='1.5'/>" % (x, INK))
        s.append("<rect x='120' y='38' width='18' height='34' fill='#dff0fb' stroke='%s' stroke-width='1.5'/>" % INK)
        s.append(text(64, 72, "SCHOOL BUS", 14, bold=True))
        for x in (40, 118):
            s.append("<circle cx='%d' cy='82' r='9' fill='%s'/>" % (x, INK))
            s.append("<circle cx='%d' cy='82' r='3.5' fill='#cccccc'/>" % x)
        lab = "a yellow school bus"
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
        s.append("<path d='%s' fill='#81c995'/>" % (GROUND % (78, 78)))
        s.append("<rect x='44' y='48' width='12' height='34' fill='#8a5a2b' stroke='%s' stroke-width='1.5'/>" % INK)
        s.append("<circle cx='50' cy='36' r='26' fill='#4f9d69' stroke='%s' stroke-width='1.5'/>" % INK)
        s.append("<ellipse cx='112' cy='70' rx='14' ry='9' fill='#c98a3d' stroke='%s' stroke-width='1.5'/>" % INK)
        s.append("<circle cx='124' cy='62' r='7' fill='#ffffff' stroke='%s' stroke-width='1.5'/>" % INK)
        s.append("<circle cx='126' cy='61' r='1.5' fill='%s'/>" % INK)
        s.append("<path d='M130 62 L140 64 L130 66 Z' fill='%s'/>" % INK)
        s.append("<line x1='108' y1='79' x2='108' y2='86' stroke='%s' stroke-width='1.5'/>" % INK)
        s.append("<line x1='116' y1='79' x2='116' y2='86' stroke='%s' stroke-width='1.5'/>" % INK)
        lab = "a park with a tree and a bird"
    elif name == "hockey":
        s.append("<rect x='1' y='1' width='158' height='102' rx='8' fill='#eaf4fb'/>")
        s.append("<rect x='98' y='50' width='44' height='30' fill='#ffffff'/>")
        for k in range(1, 6):
            s.append("<line x1='%d' y1='50' x2='%d' y2='80' stroke='#9aa3ab' stroke-width='1'/>" % (98 + k * 7.3, 98 + k * 7.3))
        for y in (60, 70):
            s.append("<line x1='98' y1='%d' x2='142' y2='%d' stroke='#9aa3ab' stroke-width='1'/>" % (y, y))
        s.append("<path d='M98 80 L98 50 L142 50 L142 80' fill='none' stroke='#c0392b' stroke-width='3.5'/>")
        s.append("<line x1='30' y1='16' x2='54' y2='76' stroke='#8a5a2b' stroke-width='5' stroke-linecap='round'/>")
        s.append("<path d='M52 74 L76 80 L74 86 L50 80 Z' fill='#8a5a2b' stroke='%s' stroke-width='1.5'/>" % INK)
        s.append("<ellipse cx='84' cy='88' rx='9' ry='4' fill='%s'/>" % INK)
        lab = "a hockey stick, a puck and a net"
    elif name == "calendar":
        fs = 22 if len(day) <= 7 else 18
        s.append("<rect x='30' y='8' width='100' height='90' rx='6' fill='#ffffff' stroke='%s' stroke-width='2'/>" % INK)
        s.append("<rect x='30' y='8' width='100' height='28' rx='6' fill='#f28b82' stroke='%s' stroke-width='2'/>" % INK)
        s.append(text(80, 28, "Today", 16, bold=True))
        s.append(text(80, 74, day, fs, bold=True))
        s.append("<rect x='52' y='3' width='6' height='12' rx='2' fill='%s'/>" % INK)
        s.append("<rect x='102' y='3' width='6' height='12' rx='2' fill='%s'/>" % INK)
        lab = "a calendar page: today is " + day
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


# ------------------------------------------------------------ coins, number cube, hat, popsicles, mitts
PIPS = {1: [(1, 1)], 2: [(0, 0), (2, 2)], 3: [(0, 0), (1, 1), (2, 2)], 4: [(0, 0), (2, 0), (0, 2), (2, 2)],
        5: [(0, 0), (2, 0), (1, 1), (0, 2), (2, 2)], 6: [(0, 0), (2, 0), (0, 1), (2, 1), (0, 2), (2, 2)]}


def die(x, y, n, sz=46):
    s = ["<rect x='%d' y='%d' width='%d' height='%d' rx='8' fill='#ffffff' stroke='%s' stroke-width='2'/>" % (x, y, sz, sz, INK)]
    st = sz / 4
    for (px, py) in PIPS[n]:
        s.append("<circle cx='%.1f' cy='%.1f' r='%.1f' fill='%s'/>" % (x + st + px * st, y + st + py * st, sz / 10, INK))
    return "".join(s)


def cube_faces_svg(label="the six faces of a number cube"):
    sz, gap = 46, 12
    s = []
    for i in range(6):
        x = 4 + i * (sz + gap)
        s.append(die(x, 4, i + 1, sz))
        s.append(text(x + sz / 2, 4 + sz + 20, str(i + 1), 15, bold=True))
    return svg_wrap(4 + 6 * sz + 5 * gap + 4, 4 + sz + 28, "".join(s), label)


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
         "<rect x='46' y='80' width='88' height='8' fill='#c0392b'/>"]
    pos = [(64, 44), (116, 44), (64, 66), (116, 66)] if len(names) > 1 else [(90, 54)]
    for (x, y), nm in zip(pos, names):
        s.append("<rect x='%d' y='%d' width='48' height='19' fill='#ffffff' stroke='%s' stroke-width='1'/>" % (x - 24, y - 14, INK))
        s.append(text(x, y + 1, nm, 14, bold=True))
    return svg_wrap(180, 104, "".join(s), "a hat with name cards: " + ", ".join(names))


def popsicles_svg(counts, rnd):
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
    return svg_wrap(int(max(W + 2, tw("     ".join(lines), 15) + 8)), 106, "".join(s), "popsicles")


def mitts_svg(counts, rnd):
    items = bag_items(counts, rnd)
    s = []
    for i, c in enumerate(items):
        x = 6 + i * 42
        s.append("<path d='M%d 62 L%d 26 Q%d 6 %d 6 Q%d 6 %d 26 L%d 62 Z' fill='%s' stroke='%s' stroke-width='1.5'/>"
                 % (x + 4, x + 4, x + 4, x + 17, x + 30, x + 30, x + 30, COL[c][1], INK))
        s.append("<path d='M%d 40 Q%d 30 %d 22 Q%d 18 %d 24 Q%d 30 %d 46' fill='%s' stroke='%s' stroke-width='1.5'/>"
                 % (x + 30, x + 34, x + 35, x + 39, x + 40, x + 39, x + 30, COL[c][1], INK))
        s.append("<rect x='%d' y='62' width='26' height='10' fill='#ffffff' stroke='%s' stroke-width='1.5'/>" % (x + 4, INK))
        s.append(text(x + 17, 42, COL[c][0], 15, bold=True))
    W = 6 + len(items) * 42
    lines = key_lines(colours_in([c for c, _ in counts]))
    s.append(text(W / 2, 96, "     ".join(lines), 15))
    return svg_wrap(int(max(W + 4, tw("     ".join(lines), 15) + 8)), 104, "".join(s), "mitts")


# ------------------------------------------------------------ set 1: everyday events
def set_everyday(rnd):
    its = []
    S = lambda n, **k: fig(scene_svg(n, **k))
    its.append(word_q(S("sunrise") + "The sun will come up tomorrow. Which word fits?", "certain",
                      "possible: it comes up a lot",
                      "The sun comes up every morning. It must happen. So it is certain."))
    its.append(word_q(S("bus") + "A dog will drive the school bus. Which word fits?", "impossible",
                      "possible: a dog can ride a bus",
                      "A dog can’t drive. It can never happen. So it is impossible."))
    its.append(word_q(S("snow") + "It is January in Ottawa. It will snow today. Which word fits?", "possible",
                      "certain: it snows a lot in winter",
                      "It snows a lot in Ottawa in January. But some days it does not snow. So it is possible, not certain."))
    its.append(word_q(S("beach") + "It is a hot July day at the beach. It will snow. Which word fits?", "impossible",
                      "possible: it snows in winter",
                      "July at the beach is hot. Snow can’t fall on a hot summer day. So it is impossible."))
    its.append(word_q(S("rain") + "Dark clouds are in the sky. It will rain. Which word fits?", "possible",
                      "certain: the clouds are dark",
                      "Dark clouds often bring rain, but not always. So rain is possible, not certain."))
    its.append(word_q(S("calendar", day="Monday") + "Today is Monday. Tomorrow will be Tuesday. Which word fits?", "certain",
                      "impossible: it is not Tuesday now",
                      "Tuesday always comes after Monday. It must happen. So it is certain."))
    its.append(word_q(S("cake") + "Maya is 6 today. Next year she will be 7. Which word fits?", "certain",
                      "impossible: she is 6 now",
                      "Every year you get 1 year older. 6 + 1 = 7. So it is certain."))
    its.append(word_q(S("hockey") + "Our hockey team plays today. We will win. Which word fits?", "possible",
                      "certain: we want to win",
                      "A team can win or lose. Wanting to win does not make it sure. So it is possible."))
    its.append(mcq(S("park") + "At the park. Which is impossible?", "A tree will walk away.",
                   ["A bird will sing.", "You will see a dog.", "You will go on the swings."],
                   "A tree can’t walk. That is impossible. The other things are possible."))
    its.append(mcq(S("park") + "At the park. Which is possible?", "You will see a Canada goose.",
                   ["A tree will fly away.", "The grass will turn pink.", "A dog will read a book."],
                   "Canada geese live in many parks. You may see one, or not. So it is possible. "
                   "The other things are impossible."))
    its.append(mcq(S("school") + "It is a school day. Which is impossible?", "A fish will teach the class.",
                   ["You will read a book.", "You will play at recess.", "You will paint a picture."],
                   "A fish can’t teach. That is impossible. Reading, recess and painting are possible."))
    its.append(mcq(S("school") + "It is a school day. Which is possible?", "You will have gym class.",
                   ["A cow will be your teacher.", "The school will fly away.", "Your desk will talk."],
                   "Some days you have gym, some days you don’t. So it is possible. The others are impossible."))
    its.append(mcq(S("night") + "It is night. Which is certain?", "The sky will be dark.",
                   ["You will hear an owl.", "You will see a shooting star.", "The sun will shine."],
                   "The sky is dark every night. So that is certain. An owl or a shooting star is only possible."))
    its.append(mcq(S("night") + "It is night. Which is impossible?", "The sun will shine.",
                   ["You will see stars.", "Dad will read a story.", "You will hear a dog."],
                   "The sun does not shine at night. That is impossible. The other things are possible."))
    its.append(mcq(S("egg") + "Leah drops an egg. Which is certain?", "The egg will fall down.",
                   ["Mom will see it.", "The egg will fly up.", "The egg will turn into a chick."],
                   "When you let go, things always fall down. So it is certain. Mom seeing it is only possible."))
    its.append(mcq(S("popsicle") + "A popsicle sits in the hot sun. Which is certain?", "It will melt.",
                   ["A bee will land on it.", "It will get colder.", "It will turn into a toy."],
                   "The hot sun always melts ice. So it is certain. A bee is only possible."))
    its.append(mcq(S("snow") + "It is a snow day. Which is possible?", "You will build a snowman.",
                   ["It will be a hot day.", "The snow will be pink.", "A moose will drive a car."],
                   "You may build a snowman, or you may not. So it is possible. The other things are impossible."))
    its.append(mcq(S("rain") + "Owen says, “Rain tomorrow is certain.” Is he right?", "No. It is possible.",
                   ["Yes. It is certain.", "No. It is impossible.", "Yes. The clouds are dark."],
                   "We can’t be sure it will rain tomorrow. It may rain, or not. So rain is possible, not certain."))
    its.append(mcq(S("beach") + "Zoe says, “Snow at the beach in July is possible.” Is she right?", "No. It is impossible.",
                   ["Yes. It is possible.", "No. It is certain.", "Yes. Zoe likes snow."],
                   "July at the beach is hot. Snow can’t fall there. So it is impossible."))
    its.append(mcq(S("sunrise") + "Kai says, “The sun coming up tomorrow is possible.” Is he right?", "No. It is certain.",
                   ["Yes. It is possible.", "No. It is impossible.", "Yes. It came up today."],
                   "The sun comes up every morning. We are sure. So it is certain, not just possible."))
    assert len(its) == 20
    return {"title": "Everyday events: impossible, possible or certain?", "items": its}


# ------------------------------------------------------------ set 2: spinners
def set_spinners(rnd):
    its = []
    F = lambda sec: fig(spinner_svg(sec))

    def sp(sec, target, other, e, q="You spin once. Which is right?"):
        return st_q(F(sec) + q, amounts(sec), target, other, e)

    its.append(sp(eq("red", "red", "red", "red"), "red", "blue",
                  "All the parts are red. The arrow must land on red. So red is certain."))
    its.append(sp(eq("red", "blue"), "red", "yellow",
                  "Half is red and half is blue. The arrow can land on either one. So red is possible."))
    its.append(sp(eq("red", "blue", "yellow"), "green", "red",
                  "There is no green part. The arrow can’t land on green. So green is impossible."))
    its.append(sp(eq("blue", "blue", "red", "blue"), "blue", "green",
                  "Most parts are blue. But there is 1 red part. The arrow could land on red. "
                  "So blue is possible, not certain."))
    its.append(sp(eq("yellow", "yellow", "yellow", "yellow", "yellow", "yellow"), "yellow", "blue",
                  "Every part is yellow. So yellow is certain. There is no blue."))
    its.append(sp(eq("red", "green", "green", "green"), "red", "purple",
                  "Only 1 part is red. But it is there, so the arrow can land on it. Red is possible, not impossible."))
    its.append(sp(eq(1, 2, 3, 4), "5", "1",
                  "The numbers are 1, 2, 3 and 4. There is no 5. So 5 is impossible."))
    its.append(sp(eq(1, 2, 3, 4), "4", "6",
                  "4 is on the spinner, so 4 is possible. A big number is not harder to get."))
    its.append(sp(eq(2, 2, 2, 2), "2", "1",
                  "Every part has a 2. The arrow must land on 2. So 2 is certain."))
    its.append(mcq(F(eq("green", "green", "green")) + "Which colour is certain?", "green",
                   ["red", "blue", "yellow"],
                   "Every part is green. So green is certain."))
    its.append(mcq(F(eq("red", "blue", "yellow")) + "Which colour is impossible?", "green",
                   ["red", "blue", "yellow"],
                   "The spinner has red, blue and yellow. There is no green. So green is impossible."))
    its.append(mcq(F(eq("green", "purple", "yellow", "purple")) + "Which colour is impossible?", "red",
                   ["green", "purple", "yellow"],
                   "The spinner has green, purple and yellow. There is no red. So red is impossible."))
    its.append(mcq(F(eq(1, 2, 3, 4, 5, 6)) + "Which number is impossible?", "7",
                   ["1", "6", "3"],
                   "The numbers go from 1 to 6. There is no 7. So 7 is impossible."))
    S = lambda spins: fig(spinners_abcd(spins))
    its.append(abcd_q(S([eq("red", "blue"), eq("red", "red", "red", "red"), eq("blue", "yellow", "blue"),
                         eq("red", "red", "blue", "red")]) + "On which spinner is red certain?", "Spinner", 1,
                      "Spinner B is all red. It must land on red. Spinner D has a blue part, "
                      "so red is only possible there."))
    its.append(abcd_q(S([eq("red", "blue", "red", "blue"), eq("red", "yellow", "yellow", "yellow"),
                         eq("red", "red", "red", "red"), eq("blue", "green", "yellow", "green")]) +
                      "On which spinner is red impossible?", "Spinner", 3,
                      "Spinner D has no red part. So red is impossible. Spinner B has 1 red part, so red is possible."))
    its.append(abcd_q(S([eq("blue", "blue", "blue", "blue"), eq("red", "red", "red", "red"),
                         eq("yellow", "green", "yellow", "green"), eq("red", "blue", "red", "blue")]) +
                      "On which spinner is red possible, but not certain?", "Spinner", 3,
                      "Spinner D has red parts and blue parts. Red may come, or blue may come. "
                      "On B red is certain. On A and C red is impossible."))
    its.append(mcq(F(eq("blue", "red", "blue", "red")) + "Liam says, “Blue is certain.” Is he right?",
                   "No. Blue is possible.",
                   ["Yes. Blue is certain.", "No. Blue is impossible.", "Yes. Blue is his favourite."],
                   "Half the spinner is red. The arrow may land on red. So blue is possible, not certain. "
                   "His favourite colour does not change the spinner."))
    its.append(mcq(F(eq("red", "red", "yellow", "red")) + "Ava says, “Yellow is impossible. The part is small.” Is she right?",
                   "No. Yellow is possible.",
                   ["Yes. Yellow is impossible.", "No. Yellow is certain.", "Yes. Red always wins."],
                   "There is 1 yellow part. The arrow can land on it. So yellow is possible, not impossible."))
    its.append(sp(eq("red", "blue", "yellow", "green"), "yellow", "purple",
                  "There is 1 yellow part out of 4. The arrow can land on it, or on another colour. So yellow is possible."))
    its.append(sp(eq("purple", "purple", "purple", "purple"), "green", "purple",
                  "Every part is purple. There is no green. So green is impossible."))
    assert len(its) == 20
    return {"title": "Spinners: can you land on red?", "items": its}


# ------------------------------------------------------------ set 3: bags of counters
def set_bags(rnd):
    its = []
    B = lambda counts: fig(bag_svg(counts, rnd))

    def bq(counts, target, other, e, q="You pick one without looking. Which is right?"):
        return st_q(B(counts) + q, dict(counts), target, other, e)

    its.append(bq([("red", 5)], "red", "blue", "Every counter is red. So red is certain."))
    its.append(bq([("red", 3), ("blue", 3)], "blue", "yellow",
                  "There are red and blue counters. You could pick either one. So blue is possible."))
    its.append(bq([("red", 4), ("yellow", 2)], "green", "red",
                  "Look in the bag. There are red and yellow counters. There is no green. So green is impossible."))
    its.append(bq([("blue", 5), ("red", 1)], "red", "green",
                  "There is only 1 red counter. But it is in the bag, so you could pick it. Red is possible."))
    its.append(bq([("green", 7), ("red", 1)], "green", "yellow",
                  "Most counters are green. But there is 1 red counter. So green is possible, not certain."))
    its.append(bq([("yellow", 4), ("purple", 2)], "yellow", "blue",
                  "There are yellow and purple counters. You could pick a purple one. So yellow is possible."))
    its.append(mcq(B([("yellow", 6)]) + "Which colour is certain?", "yellow", ["red", "blue", "green"],
                   "Every counter is yellow. So yellow is certain."))
    its.append(mcq(B([("red", 2), ("blue", 2), ("yellow", 2)]) + "Which colour is impossible?", "green",
                   ["red", "blue", "yellow"],
                   "The bag has red, blue and yellow counters. There is no green. So green is impossible."))
    its.append(mcq(B([("green", 3), ("purple", 2), ("blue", 1)]) + "Which colour is impossible?", "red",
                   ["green", "purple", "blue"],
                   "The bag has green, purple and blue. There is no red. So red is impossible. "
                   "There is 1 blue, so blue is possible."))
    its.append(mcq(B([("red", 3), ("blue", 3)]) + "Maya wants a green counter. Can she get one?", "No. There is no green.",
                   ["Yes. Green is possible.", "Yes. Green is certain.", "Yes, if she shuts her eyes."],
                   "Look in the bag first. There are only red and blue counters. Green is impossible."))
    its.append(mcq(B([("red", 1), ("blue", 5)]) + "Kai wants a red counter. Can he get one?", "Yes. Red is possible.",
                   ["No. There is no red.", "Yes. Red is certain.", "No. Red is impossible."],
                   "There is 1 red counter in the bag. Kai could pick it. So red is possible."))
    its.append(st_q(B([("red", 3), ("blue", 3)]) + "Ava takes out all the blue counters. Then she picks one. Which is right?",
                    {"red": 3}, "red", "blue",
                    "After the blue counters come out, only red counters are left. So red is certain."))
    its.append(st_q(B([("red", 4)]) + "Noah puts 2 green counters in the bag. Then he picks one. Which is right?",
                    {"red": 4, "green": 2}, "green", "blue",
                    "Now the bag has red and green counters. So green is possible. Before, green was impossible."))
    G = lambda bags: fig(bags_abcd(bags, rnd))
    its.append(abcd_q(G([[("red", 3), ("blue", 3)], [("blue", 6)], [("red", 5), ("yellow", 1)], [("red", 6)]]) +
                      "In which bag is red certain?", "Bag", 3,
                      "Bag D has only red counters. So red is certain. Bag C has a yellow counter, so red is only possible there."))
    its.append(abcd_q(G([[("red", 4), ("blue", 2)], [("yellow", 3), ("green", 3)], [("blue", 6)], [("blue", 1), ("red", 5)]]) +
                      "In which bag is blue impossible?", "Bag", 1,
                      "Bag B has yellow and green counters. There is no blue. So blue is impossible."))
    its.append(abcd_q(G([[("red", 6)], [("yellow", 2), ("red", 4)], [("blue", 6)], [("green", 3), ("blue", 3)]]) +
                      "In which bag is yellow possible?", "Bag", 1,
                      "Only bag B has yellow counters, and it has red ones too. So yellow is possible in bag B."))
    its.append(mcq(B([("red", 2), ("blue", 4)]) + "Chloe says, “Red is certain. Red is my favourite.” Is she right?",
                   "No. Red is possible.",
                   ["Yes. Red is certain.", "No. Red is impossible.", "Yes. Red is her favourite."],
                   "The bag has blue counters too. Her favourite colour does not change what she picks. "
                   "So red is possible, not certain."))
    its.append(bq([("red", 2), ("yellow", 2), ("blue", 2)], "yellow", "green",
                  "There are 2 yellow counters. You could pick one, or a red or blue one. So yellow is possible."))
    its.append(mcq(B([("red", 6)]) + "Leah picks 2 counters. What is certain?", "She gets 2 red ones.",
                   ["She gets 1 red, 1 blue.", "She gets 2 blue ones.", "She gets no red."],
                   "Every counter is red. Any 2 counters she picks will be red. So 2 red ones is certain."))
    its.append(mcq(B([("blue", 2), ("green", 2)]) + "Ethan wants a yellow counter. What can he do?",
                   "Put a yellow one in the bag.",
                   ["Pick again and again.", "Shake the bag.", "Pick very fast."],
                   "There is no yellow in the bag, so yellow is impossible. Picking again or shaking does not help. "
                   "He must put a yellow counter in."))
    assert len(its) == 20
    return {"title": "Bags of counters: can you pick red?", "items": its}


# ------------------------------------------------------------ set 4: predictions
SAME = "the same for both"


def prob_q(pic, counts, q, extra, e):
    """Choices: the two colours, 'the same for both', and a colour that is not there."""
    (a, na), (b, nb) = counts
    corr = SAME if na == nb else (a if na > nb else b)
    return mcq(pic + q, corr, [a, b, SAME, extra], e)


def set_predict(rnd):
    its = []
    F = lambda sec: fig(spinner_svg(sec))
    B = lambda counts: fig(bag_svg(counts, rnd))
    QS = "Which colour will you probably get?"
    QB = "Which colour will you probably pick?"
    its.append(prob_q(F(eq("red", "red", "blue", "red")), [("red", 3), ("blue", 1)], QS, "green",
                      "3 parts are red. Only 1 part is blue. More red, so you will probably get red."))
    its.append(prob_q(F(eq("green", "yellow", "yellow", "yellow")), [("green", 1), ("yellow", 3)], QS, "red",
                      "3 parts are yellow and 1 part is green. Yellow covers more, so you will probably get yellow."))
    its.append(prob_q(F(eq("red", "blue", "red", "blue")), [("red", 2), ("blue", 2)], QS, "yellow",
                      "2 parts are red and 2 parts are blue. The parts are the same size. So it is the same for both."))
    its.append(prob_q(B([("blue", 6), ("red", 2)]), [("blue", 6), ("red", 2)], QB, "yellow",
                      "There are 6 blue counters and 2 red counters. More blue, so you will probably pick blue."))
    its.append(prob_q(B([("yellow", 2), ("green", 6)]), [("yellow", 2), ("green", 6)], QB, "red",
                      "There are 6 green counters and only 2 yellow. More green, so you will probably pick green."))
    its.append(prob_q(B([("red", 3), ("blue", 3)]), [("red", 3), ("blue", 3)], QB, "green",
                      "3 red and 3 blue. The same number, so it is the same for both."))
    its.append(prob_q(F(eq("green", "green", "green", "purple", "green", "green")), [("green", 5), ("purple", 1)], QS, "blue",
                      "5 parts are green. Only 1 part is purple. So you will probably get green."))
    its.append(mcq(F(eq(1, 1, 2, 1)) + "Which number will you probably get?", "1", ["2", SAME, "3"],
                   "3 parts have a 1. Only 1 part has a 2. So you will probably get 1."))
    its.append(mcq(F(eq(1, 2, 3, 4)) + "Which will you probably get, 1 or 4?", SAME, ["4", "1", "5"],
                   "1 and 4 each have 1 part. The parts are the same size. So it is the same for both. "
                   "A bigger number is not harder to get."))
    its.append(mcq(B([("red", 4), ("blue", 2), ("yellow", 1)]) + QB, "red",
                   ["blue", "yellow", "green"],
                   "Count each colour: red 4, blue 2, yellow 1. Red has the most, so you will probably pick red."))
    its.append(mcq(F(eq("purple", "green", "green", "green")) + "Hana loves purple. Which colour will she probably get?",
                   "green", ["purple", SAME, "red"],
                   "3 parts are green and only 1 is purple. Her favourite colour does not change the spinner. "
                   "She will probably get green."))
    its.append(mcq(B([("red", 5), ("blue", 1)]) + "Jayden wants blue. What will probably happen?", "He picks red.",
                   ["He picks blue.", "Both are the same.", "He picks green."],
                   "Look in the bag: 5 red and 1 blue. Wanting blue does not help. He will probably pick red."))
    S = lambda spins: fig(spinners_abcd(spins))
    its.append(abcd_q(S([eq("red", "blue", "blue", "blue"), eq("red", "blue", "red", "blue"),
                         eq("red", "red", "blue", "red"), eq("blue", "blue", "blue", "blue")]) +
                      "You want red. Which spinner is best?", "Spinner", 2,
                      "Spinner C has 3 red parts out of 4. That is the most red. On spinner D, red is impossible."))
    its.append(abcd_q(S([eq("yellow", "yellow", "red", "yellow"), eq("yellow", "red", "yellow", "red"),
                         eq("yellow", "red", "red", "red"), eq("yellow", "yellow", "yellow", "yellow")]) +
                      "On which spinner is yellow hardest to get?", "Spinner", 2,
                      "Spinner C has only 1 yellow part. The others have more yellow. So yellow is hardest to get on C."))
    G = lambda bags: fig(bags_abcd(bags, rnd))
    its.append(abcd_q(G([[("blue", 2), ("red", 4)], [("blue", 1), ("red", 5)], [("blue", 5), ("red", 1)], [("blue", 3), ("red", 3)]]) +
                      "You want blue. Which bag is best?", "Bag", 2,
                      "Each bag has 6 counters. Bag C has 5 blue counters. That is the most blue."))
    its.append(abcd_q(G([[("red", 4), ("blue", 2)], [("red", 3), ("blue", 3)], [("red", 1), ("blue", 5)], [("red", 6)]]) +
                      "In which bag are red and blue the same?", "Bag", 1,
                      "Bag B has 3 red and 3 blue. The same number of each, so it is the same for both."))
    its.append(mcq(B([("red", 2), ("blue", 2)]) + "Mateo puts in 3 more red. Which colour will he probably pick now?",
                   "red", ["blue", SAME, "green"],
                   "Red: 2 + 3 = 5. Blue: 2. 5 is more than 2, so he will probably pick red."))
    its.append(mcq(F(eq("red", "red", "blue", "red")) + "Kai spins 10 times. What will he probably see?",
                   "more red than blue", ["more blue than red", "red and blue the same", "no red at all"],
                   "3 parts are red and 1 is blue. Red comes up more often. So he will probably see more red than blue."))
    its.append(mcq(fig(scene_svg("snow")) + "It is January in Winnipeg. What will the weather probably be?",
                   "cold and snowy", ["hot and sunny", "a beach day", "warm and rainy"],
                   "Winnipeg is very cold in January. Snow is common. So cold and snowy is the best guess."))
    its.append(mcq(fig(scene_svg("rain")) + "Dark clouds fill the sky. Should Noah take his umbrella?",
                   "Yes. Rain is possible.",
                   ["No. Rain is impossible.", "No. It is not raining yet.", "Yes. Rain is certain."],
                   "Dark clouds often bring rain, so rain is possible. Taking an umbrella is a good idea. "
                   "Rain is not certain, so “certain” is the wrong reason."))
    assert len(its) == 20
    return {"title": "Predictions: which colour will you probably get?", "items": its}


# ------------------------------------------------------------ set 5: word problems
def set_stories(rnd):
    its = []
    C = fig(coin_svg())
    D = fig(cube_faces_svg())
    its.append(mcq(C + "You toss a coin. Which is right?", "Heads is possible.",
                   ["Heads is certain.", "Heads is impossible.", "Tails is impossible."],
                   "A coin can land on heads or tails. So heads is possible."))
    its.append(mcq(C + "You toss a coin. What can you get?", "heads or tails",
                   ["only heads", "only tails", "1, 2 or 3"],
                   "A coin has 2 sides: heads and tails. It can land on either side."))
    its.append(mcq(D + "You roll a number cube. Which number is impossible?", "7", ["1", "6", "3"],
                   "A number cube has 1 to 6 dots. There is no 7. So 7 is impossible."))
    its.append(st_q(D + "You roll a number cube. Which is right?", {str(k): 1 for k in range(1, 7)}, "6", "0",
                    "6 is on the cube. It may come up, or another number may. So 6 is possible."))
    its.append(mcq(D + "You roll a number cube. What is certain?", "You get 1, 2, 3, 4, 5 or 6.",
                   ["You get 6.", "You get 1.", "You get 8."],
                   "Every face has 1, 2, 3, 4, 5 or 6 dots. One of them must come up. So that is certain."))
    its.append(mcq(D + "Nathan says, “6 is impossible. It is a big number.” Is he right?",
                   "No. 6 is possible.",
                   ["Yes. 6 is impossible.", "No. 6 is certain.", "Yes. Big numbers are hard."],
                   "6 is on 1 face, just like 1. So 6 is possible. Big numbers are not harder to roll."))
    its.append(mcq(C + "Mei gets heads 3 times. She tosses again. Which is right?",
                   "Heads and tails are possible.",
                   ["Tails is certain.", "Heads is certain.", "Heads is impossible."],
                   "A coin does not remember. Each toss, heads or tails can come up. So both are possible."))
    its.append(mcq(C + "Before a soccer game, the referee tosses a coin. Our captain calls heads. Which is right?",
                   "Winning the toss is possible.",
                   ["Winning the toss is certain.", "Winning the toss is impossible.", "Both teams will win."],
                   "The coin may land on heads, or on tails. So winning is possible. Both teams can’t win."))
    H4 = fig(hat_svg(["Maya", "Liam", "Owen", "Zoe"]))
    its.append(mcq(H4 + "The teacher picks one name from the hat. Which is right?",
                   "Liam is possible.",
                   ["Liam is certain.", "Liam is impossible.", "Chloe is possible."],
                   "Liam’s name is in the hat with 3 other names. So Liam is possible. "
                   "Chloe’s name is not in the hat, so Chloe is impossible."))
    its.append(mcq(H4 + "Chloe’s name is not in the hat. Which is right?",
                   "Chloe is impossible.",
                   ["Chloe is possible.", "Chloe is certain.", "Maya is impossible."],
                   "Only names in the hat can be picked. Chloe’s name is not there. So Chloe is impossible."))
    its.append(mcq(fig(hat_svg(["Owen"])) + "Only Owen’s name is in the hat. The teacher picks one. Which is right?",
                   "Owen is certain.",
                   ["Owen is possible.", "Owen is impossible.", "Zoe is possible."],
                   "There is only one name in the hat. It must be Owen. So Owen is certain."))
    its.append(mcq(fig(popsicles_svg([("red", 4), ("yellow", 2)], rnd)) +
                   "There are 4 red and 2 yellow popsicles. Emma takes one without looking. Which will she probably get?",
                   "a red one", ["a yellow one", SAME, "a green one"],
                   "There are 4 red and 2 yellow. More red, so she will probably get a red one. There are no green ones."))
    its.append(mcq(fig(popsicles_svg([("yellow", 3)], rnd)) +
                   "Only yellow popsicles are left. Liam takes one. Which is right?",
                   "Yellow is certain.",
                   ["Yellow is possible.", "Yellow is impossible.", "Red is possible."],
                   "Every popsicle left is yellow. So yellow is certain. Red is impossible."))
    its.append(mcq(fig(mitts_svg([("red", 3), ("blue", 3)], rnd)) +
                   "Sofia picks a mitt from the bin without looking. Which is right?", "Red is possible.",
                   ["Red is certain.", "Red is impossible.", "Green is possible."],
                   "There are red mitts and blue mitts. She could get either one. So red is possible. Green is impossible."))
    its.append(mcq(fig(scene_svg("race")) + "6 children run a race on Sports Day. Ethan is one of them. Which is right?",
                   "Ethan winning is possible.",
                   ["Ethan winning is certain.", "Ethan winning is impossible.", "All 6 winning is possible."],
                   "Any of the 6 children could win. We can’t be sure it is Ethan. So Ethan winning is possible."))
    its.append(st_q(fig(bag_svg([("red", 6), ("yellow", 1)], rnd, "prize bag of balls")) +
                    "At the fall fair, the yellow ball wins a prize. Ava picks one ball without looking. Which is right?",
                    {"red": 6, "yellow": 1}, "yellow", "blue",
                    "There is 1 yellow ball. Ava could pick it, but there are lots of red ones too. So yellow is possible."))
    G = lambda bags: fig(bags_abcd(bags, rnd))
    its.append(abcd_q(G([[("blue", 6)], [("red", 2), ("blue", 4)], [("red", 4), ("blue", 2)], [("red", 1), ("blue", 5)]]) +
                      "Arjun wins if he picks red. Which bag should he pick from?", "Bag", 2,
                      "Bag C has 4 red counters. That is the most red. In bag A, red is impossible."))
    S = lambda spins: fig(spinners_abcd(spins))
    its.append(abcd_q(S([eq("blue", "blue", "blue", "blue"), eq("blue", "red", "blue", "red"),
                         eq("red", "red", "red", "red"), eq("blue", "yellow", "yellow", "yellow")]) +
                      "Priya wins if she lands on blue. Which spinner should she use?", "Spinner", 0,
                      "Spinner A is all blue. Blue is certain, so she will win. On spinner C, blue is impossible."))
    its.append(mcq(fig(bag_svg([("blue", 2), ("green", 2)], rnd)) + "Benjamin needs a yellow counter for a game. What can he do?",
                   "Put a yellow one in the bag.",
                   ["Pick again and again.", "Pick with his eyes shut.", "Wish for yellow."],
                   "There is no yellow in the bag, so yellow is impossible. Picking again does not help. "
                   "He must put a yellow counter in."))
    its.append(mcq(fig(scene_svg("calendar", day="July 1")) + "It is Canada Day. Which is certain?",
                   "Tomorrow will be July 2.",
                   ["There will be fireworks.", "It will rain.", "Today will be Christmas."],
                   "July 2 always comes after July 1. So it is certain. Fireworks and rain are only possible. "
                   "Christmas is in December, so that is impossible."))
    assert len(its) == 20
    return {"title": "Word problems: predict and decide", "items": its}


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
        "<h2>Three probability words</h2>"
        "<p>Some things we are sure about. Some things we are not sure about. We use three words.</p>" +
        table(["Word", "Meaning", "Example"], [
            ["<b>certain</b>", "It must happen.", "The sun will come up tomorrow."],
            ["<b>possible</b>", "It may happen, but we are not sure.", "It will snow today."],
            ["<b>impossible</b>", "It can never happen.", "A dog will drive the school bus."],
        ]) +
        "<figure class='sn-fig'>" + scene_svg("sunrise") +
        "<figcaption>The sun comes up every morning. It is certain.</figcaption></figure>" +
        ex("Example", "Our hockey team plays today. Will we win?",
           "A team can win or lose. We are not sure.", "Winning is possible.") +
        "<h2>Spinners</h2>"
        "<p>Look at the colours on the spinner. If <b>all</b> the parts are red, red is <b>certain</b>. "
        "If <b>some</b> parts are red, red is <b>possible</b>. If <b>no</b> parts are red, red is <b>impossible</b>.</p>"
        "<figure class='sn-fig'>" + spinner_svg(eq("red", "red", "blue", "red"), "spinner: 3 red parts and 1 blue part") +
        "<figcaption>3 red parts and 1 blue part. Red is possible. Blue is possible. Green is impossible.</figcaption></figure>" +
        ex("Example", "Is red certain on this spinner?", "Most parts are red, but there is a blue part.",
           "No. Red is possible, not certain.") +
        "<h2>Bags of counters</h2>"
        "<p>Look in the bag <b>before</b> you answer. You can only pick a colour that is in the bag.</p>"
        "<figure class='sn-fig'>" + bag_svg([("red", 5), ("blue", 1)], rnd, "bag: 5 red counters and 1 blue counter") +
        "<figcaption>5 red counters and 1 blue counter.</figcaption></figure>" +
        ex("Example", "Can you pick blue?", "There is 1 blue counter. It is in the bag.", "Yes. Blue is possible.") +
        "<h2>Making predictions</h2>"
        "<p>When there is <b>more</b> of a colour, you will <b>probably</b> get that colour. "
        "If there is the same amount of each colour, it is the same for both.</p>" +
        ex("Example", "The bag has 5 red counters and 1 blue counter. Which colour will you probably pick?",
           "There are more red counters than blue counters.", "red") +
        "<h2>Common mistakes</h2>" +
        table(["Mistake", "What to do instead"], [
            ["Saying “certain” when it only happens a lot", "Certain means it must happen every time"],
            ["Saying “impossible” when there is only a little of a colour", "If it is there at all, it is possible"],
            ["Not looking in the bag", "Check which colours are in the bag first"],
            ["Choosing your favourite colour", "Count the parts or counters of each colour"],
            ["Thinking 6 is harder to roll than 1", "Every number on a number cube has the same chance"],
        ])
    )


FAQ = [
    {"q": "What do Grade 1 students learn about probability in Ontario?",
     "a": "In the Ontario Mathematics Curriculum (2020), expectation D2.1, Grade 1 students use the words impossible, possible and certain to describe events. They use these words to make predictions and simple decisions, such as which colour they will probably pick."},
    {"q": "What is the difference between possible and certain?",
     "a": "Certain means it must happen every time, like Tuesday coming after Monday. Possible means it may happen but we are not sure, like snow on a January day."},
    {"q": "How can I teach probability to a 6-year-old at home?",
     "a": "Put some coloured blocks in a bag and ask “Is red impossible, possible or certain?” Then pick without looking to check, and change the blocks to try again."},
    {"q": "Why does my child say a colour is impossible when it is on the spinner?",
     "a": "Many children think a small part can never be landed on. Spin a few times together and show that if a colour is there at all, it is possible."},
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
    rnd = random.Random(41810)
    sets = [set_everyday(rnd), set_spinners(rnd), set_bags(rnd), set_predict(rnd), set_stories(rnd)]
    balance(sets, rnd)
    seen = set()
    for s in sets:
        assert len(s["items"]) == 20, (s["title"], len(s["items"]))
        for it in s["items"]:
            assert len(set(it["c"])) == 4, it
            assert it["e"], it
            assert it["q"].count("<svg") == 1, it["q"]
            k = it["q"] + "|" + "|".join(sorted(it["c"]))
            assert k not in seen, it["q"]
            seen.add(k)
    u = {
        "country": "ca-on", "subject": "math", "grade": "grade-1", "slug": "probability", "sort": 10,
        "updated": UPDATED, "pdf_url": "",
        "title": "Probability: Impossible, Possible or Certain",
        "seo_title": "Grade 1 Probability Worksheets: Impossible, Possible or Certain (Free, with Answer Key)",
        "short_title": "Probability",
        "domain": "Data",
        "standard_code": "Grade 1: D2.1",
        "standard_url": "https://www.dcp.edu.gov.on.ca/en/curriculum/elementary-mathematics",
        "standard_text": "Use mathematical language, including the terms “impossible”, “possible”, and “certain”, to describe the likelihood of events happening, and use that likelihood to make predictions and informed decisions",
        "meta_desc": "Free Grade 1 math worksheets on probability for the Ontario curriculum: say if everyday events are impossible, possible or certain, find what you can land on with a spinner or pick from a bag of counters, predict which colour you will probably get, and solve short word problems. 100 questions with an answer key.",
        "key_big": "Certain means it must happen. Possible means it may happen. Impossible means it can never happen.",
        "key_sub": "If all the counters are red, red is certain. If some are red, red is possible. If none are red, red is impossible. The colour with more counters is the one you will probably pick.",
        "body_html": body_html(rnd), "faq": FAQ, "sets": sets,
    }
    return mark_large(u, "spinners A to D|bags A to D|the six faces of a number cube|mitts|popsicles")


if __name__ == "__main__":
    u = gen_unit()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
