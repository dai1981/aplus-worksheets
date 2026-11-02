# -*- coding: utf-8 -*-
"""
Canada (British Columbia) Grade 1 Math: Likelihood
(BC Mathematics Curriculum, Grade 1 Content: likelihood of familiar life events, using comparative language)
  python3 tools/gen_cabc_math_g1_likelihood.py
Everyday events (always, sometimes, never), spinners and bags (which colour is more likely?),
comparing two everyday BC events (more likely, less likely, equally likely), predictions and word problems.
Wrong answers come from real mistakes: mixing up more likely and less likely, "never" for a small part,
"always" for something that only happens a lot, choosing a favourite colour, ignoring what is in the bag,
thinking a big number is harder to roll, thinking a coin "remembers".
Every picture shows the colour as a letter too (R = red ...), so it still works in black and white.
Grade 1: very short sentences for 6-7 year olds, a picture in every question.
HTML attributes use single quotes (no backslashes in the JSON). Canadian English.
"""
import json, math, os, random, re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "ca-bc", "math", "grade-1")
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


WA = "always: it happens every time"
WS = "sometimes: it may happen"
WN = "never: it can’t happen"
WREASON = {"always": WA, "sometimes": WS, "never": WN}
EQ = "equally likely"
CT = "you can’t tell"
SAME = "They are equally likely."


def cap(s):
    return s[0].upper() + s[1:]


def word_q(q, w, fourth, e):
    """Which word fits? The three words with a meaning, plus one real wrong reason."""
    return mcq(q, WREASON[w], [x for k, x in WREASON.items() if k != w] + [fourth], e)


def cmp_q(q, x, y, rel, fourth, e):
    """Two events x and y. rel: 'more' (x is more likely), 'less' (y is more likely) or 'equal'."""
    mx = "%s is more likely." % cap(x)
    my = "%s is more likely." % cap(y)
    corr = {"more": mx, "less": my, "equal": SAME}[rel]
    return mcq(q, corr, [mx, my, SAME, fourth], e)


def col_rel_q(q, counts, a, b, fourth, e):
    """Compare colour a with colour b: more / less / equally likely (checked from the counts)."""
    na, nb = counts.get(a, 0), counts.get(b, 0)
    s_more = "%s is more likely than %s." % (cap(a), b)
    s_less = "%s is less likely than %s." % (cap(a), b)
    s_eq = "%s and %s are equally likely." % (cap(a), b)
    corr = s_more if na > nb else (s_less if na < nb else s_eq)
    return mcq(q, corr, [s_more, s_less, s_eq, fourth], e)


def which_q(q, counts, a, b, ask, fourth, e):
    """'a or b: which is more/less likely?' Answer checked from the counts."""
    na, nb = counts[a], counts[b]
    if na == nb:
        corr = EQ
    elif ask == "more":
        corr = a if na > nb else b
    else:
        corr = a if na < nb else b
    return mcq(q, corr, [a, b, EQ, fourth], e)

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


def scene_parts(name, day="Monday"):
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
    elif name == "ferry":
        s.append("<rect x='1' y='1' width='158' height='102' rx='8' fill='%s'/>" % SKY)
        s.append(cloud(36, 22, 0.7))
        s.append("<rect x='94' y='26' width='12' height='16' fill='#3b78c4' stroke='%s' stroke-width='1.5'/>" % INK)
        s.append("<rect x='48' y='42' width='68' height='16' fill='#ffffff' stroke='%s' stroke-width='1.5'/>" % INK)
        for x in (54, 68, 82, 96):
            s.append("<rect x='%d' y='46' width='10' height='7' fill='#8ab4f8' stroke='%s' stroke-width='1'/>" % (x, INK))
        s.append("<path d='M26 58 L136 58 L126 76 L36 76 Z' fill='#ffffff' stroke='%s' stroke-width='2'/>" % INK)
        s.append("<rect x='33' y='64' width='96' height='4' fill='#3b78c4'/>")
        s.append("<path d='%s' fill='#5b8fd1'/>" % (GROUND % (72, 72)))
        for (x, y) in [(18, 84), (60, 92), (110, 86), (140, 96)]:
            s.append("<path d='M%d %d q5 -4 10 0 q5 4 10 0' fill='none' stroke='#ffffff' stroke-width='1.5'/>" % (x, y))
        lab = "a ferry boat on the sea"
    elif name == "orca":
        s.append("<rect x='1' y='1' width='158' height='102' rx='8' fill='%s'/>" % SKY)
        s.append("<ellipse cx='80' cy='64' rx='44' ry='16' fill='%s'/>" % INK)
        s.append("<polygon points='70,52 80,20 90,52' fill='%s'/>" % INK)
        s.append("<ellipse cx='108' cy='55' rx='7' ry='3' fill='#ffffff'/>")
        s.append("<path d='%s' fill='#3b6fa8'/>" % (GROUND % (62, 62)))
        for (x, y) in [(14, 74), (50, 86), (100, 78), (130, 92)]:
            s.append("<path d='M%d %d q5 -4 10 0 q5 4 10 0' fill='none' stroke='#ffffff' stroke-width='1.5'/>" % (x, y))
        lab = "an orca in the sea"
    elif name == "gull":
        s.append("<rect x='1' y='1' width='158' height='102' rx='8' fill='%s'/>" % SKY)
        s.append("<path d='%s' fill='#5b8fd1'/>" % (GROUND % (68, 68)))
        s.append("<rect x='70' y='56' width='16' height='46' fill='#8a5a2b' stroke='%s' stroke-width='1.5'/>" % INK)
        s.append("<path d='M58 42 L46 36 L50 46 Z' fill='#9aa3ab' stroke='%s' stroke-width='1.2'/>" % INK)
        s.append("<ellipse cx='76' cy='46' rx='20' ry='10' fill='#ffffff' stroke='%s' stroke-width='1.5'/>" % INK)
        s.append("<path d='M62 44 Q76 34 90 44 Q76 52 62 44 Z' fill='#9aa3ab' stroke='%s' stroke-width='1.2'/>" % INK)
        s.append("<circle cx='96' cy='34' r='9' fill='#ffffff' stroke='%s' stroke-width='1.5'/>" % INK)
        s.append("<path d='M104 32 L114 35 L104 38 Z' fill='#f6c445' stroke='%s' stroke-width='1'/>" % INK)
        s.append("<circle cx='98' cy='32' r='1.6' fill='%s'/>" % INK)
        for (x, y) in [(16, 82), (110, 80), (128, 94)]:
            s.append("<path d='M%d %d q5 -4 10 0 q5 4 10 0' fill='none' stroke='#ffffff' stroke-width='1.5'/>" % (x, y))
        lab = "a seagull on a post by the sea"
    elif name == "salmon":
        s.append("<rect x='1' y='1' width='158' height='102' rx='8' fill='#81c995'/>")
        s.append("<rect x='1' y='30' width='158' height='46' fill='#5b8fd1'/>")
        for (x, y) in [(40, 46), (92, 62), (126, 42)]:
            s.append("<polygon points='%d,%d %d,%d %d,%d' fill='#c0392b' stroke='%s' stroke-width='1.2'/>"
                     % (x + 14, y, x + 24, y - 7, x + 24, y + 7, INK))
            s.append("<ellipse cx='%d' cy='%d' rx='16' ry='7' fill='#d9534f' stroke='%s' stroke-width='1.2'/>" % (x, y, INK))
            s.append("<circle cx='%d' cy='%d' r='1.6' fill='%s'/>" % (x - 9, y - 2, INK))
        for x in (20, 140):
            s.append("<polygon points='%d,98 %d,80 %d,98' fill='#2e5b3a'/>" % (x - 9, x, x + 9))
        s.append("<polygon points='12,24 20,6 28,24' fill='#2e5b3a'/>")
        lab = "red salmon swimming in a river"
    elif name == "mountain":
        s.append("<rect x='1' y='1' width='158' height='102' rx='8' fill='%s'/>" % SKY)
        s.append("<polygon points='8,90 64,20 120,90' fill='#7a8a99' stroke='%s' stroke-width='1.5'/>" % INK)
        s.append("<polygon points='64,20 52,35 59,32 64,38 70,32 76,35' fill='#ffffff'/>")
        s.append("<polygon points='76,90 118,36 158,90' fill='#9aa3ab' stroke='%s' stroke-width='1.5'/>" % INK)
        s.append("<polygon points='118,36 108,49 114,46 118,51 123,46 128,49' fill='#ffffff'/>")
        s.append("<path d='%s' fill='#ffffff'/>" % (GROUND % (84, 84)))
        s.append("<line x1='1' y1='84' x2='159' y2='84' stroke='#7a8a99' stroke-width='1.5'/>")
        for x in (22, 140):
            s.append("<polygon points='%d,98 %d,74 %d,98' fill='#2e5b3a'/>" % (x - 9, x, x + 9))
        for (x, y) in [(20, 16), (100, 14), (146, 22), (40, 50)]:
            s.append("<circle cx='%d' cy='%d' r='3' fill='#ffffff' stroke='#7a8a99' stroke-width='0.8'/>" % (x, y))
        lab = "snowy mountains in winter"
    else:
        raise ValueError(name)
    if name != "calendar":
        s.append(frame(W, H))
    return "".join(s), lab


def scene_svg(name, day="Monday"):
    body, lab = scene_parts(name, day)
    return svg_wrap(160, 104, body, lab)


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


# ------------------------------------------------------------ two pictures side by side
def compare_svg(a, cap_a, b, cap_b):
    ba, _ = scene_parts(a)
    bb, _ = scene_parts(b)
    gap = 20
    for c in (cap_a, cap_b):
        assert tw(c, 15, True) <= 156, c
    s = [ba, "<g transform='translate(%d,0)'>%s</g>" % (160 + gap, bb),
         text(80, 124, cap_a, 15, bold=True), text(160 + gap + 80, 124, cap_b, 15, bold=True)]
    return svg_wrap(340, 132, "".join(s), "two pictures: %s, and %s" % (cap_a, cap_b))


# ------------------------------------------------------------ set 1: everyday events
def set_everyday(rnd):
    its = []
    S = lambda n, **k: fig(scene_svg(n, **k))
    its.append(word_q(S("sunrise") + "The sun comes up in the morning. Which word fits?", "always",
                      "sometimes: clouds can hide it",
                      "The sun comes up every morning. Clouds can hide it, but it still comes up. So the word is always."))
    its.append(word_q(S("bus") + "A dog drives the school bus. Which word fits?", "never",
                      "sometimes: dogs can ride a bus",
                      "A dog can’t drive. It can’t happen. So the word is never."))
    its.append(word_q(S("rain") + "It is a November day in Vancouver. It rains. Which word fits?", "sometimes",
                      "always: it rains a lot then",
                      "Vancouver gets lots of rain in November. But some days are dry. So rain on a day is sometimes, not always."))
    its.append(word_q(S("beach") + "It snows at the beach on a hot July day. Which word fits?", "never",
                      "sometimes: it snows in winter",
                      "A July day at the beach is hot. Snow can’t fall then. So the word is never."))
    its.append(word_q(S("calendar", day="Monday") + "Tuesday comes after Monday. Which word fits?", "always",
                      "sometimes: today is not Tuesday",
                      "Tuesday comes after Monday every week. So the word is always."))
    its.append(word_q(S("cake") + "On her birthday, Zara gets 1 year older. Which word fits?", "always",
                      "sometimes: only if there is a cake",
                      "Every birthday, you get 1 year older. Cake or no cake. So the word is always."))
    its.append(word_q(S("hockey") + "Our hockey team plays a game. We win. Which word fits?", "sometimes",
                      "always: we try very hard",
                      "A team can win or lose. Trying hard does not make it sure. So the word is sometimes."))
    its.append(word_q(S("popsicle") + "A popsicle sits in the hot sun. It melts. Which word fits?", "always",
                      "never: popsicles are cold",
                      "The hot sun melts ice every time. So the word is always."))
    its.append(word_q(S("night") + "The sun shines in the night sky. Which word fits?", "never",
                      "sometimes: the Moon is bright",
                      "The sun does not shine at night. The bright light is the Moon. So the word is never."))
    its.append(word_q(S("salmon") + "It is fall at a BC river. You see a salmon jump. Which word fits?", "sometimes",
                      "always: there are lots of salmon",
                      "You may see a salmon jump, or you may not. So the word is sometimes."))
    its.append(mcq(S("park") + "You visit Stanley Park. Which will never happen?", "A tree walks away.",
                   ["You see a squirrel.", "A dog barks.", "You see a bald eagle."],
                   "A tree can’t walk. That is never. The other things can happen sometimes."))
    its.append(mcq(S("school") + "It is a school day. Which will never happen?", "A fish teaches the class.",
                   ["You read a book.", "You play at recess.", "You paint a picture."],
                   "A fish can’t teach. That is never. Reading, recess and painting can happen."))
    its.append(mcq(S("ferry") + "You ride BC Ferries. Which will always happen?", "The ferry floats on water.",
                   ["You see an orca.", "You eat a snack.", "The ferry flies in the sky."],
                   "A ferry floats on water every trip. That is always. You see an orca only sometimes."))
    its.append(mcq(S("ferry") + "You ride BC Ferries. Which can happen sometimes?", "You see an orca.",
                   ["The ferry flies in the sky.", "The sea turns pink.", "A fish drives the ferry."],
                   "Orcas swim near the ferry on some trips. So that is sometimes. The other things never happen."))
    its.append(mcq(S("snow") + "It is a snow day. Which can happen sometimes?", "You build a snowman.",
                   ["It is a hot beach day.", "The snow is pink.", "A moose drives a car."],
                   "You may build a snowman, or you may not. So that is sometimes. The other things never happen."))
    its.append(mcq(S("night") + "It is night. Which will always happen?", "The sky is dark.",
                   ["You hear an owl.", "You see a shooting star.", "The sun shines."],
                   "The sky is dark every night. That is always. An owl or a shooting star is only sometimes."))
    its.append(mcq(S("rain") + "Owen says, “It always rains in Vancouver.” Is he right?", "No. It rains sometimes.",
                   ["Yes. It always rains.", "No. It never rains.", "Yes. It rained today."],
                   "Vancouver has lots of rain. But it also has dry, sunny days. So it rains sometimes, not always."))
    its.append(mcq(S("beach") + "Nadia says, “It sometimes snows at the beach in July.” Is she right?",
                   "No. It never happens.",
                   ["Yes. It sometimes snows.", "No. It always snows.", "Yes. Nadia likes snow."],
                   "July at the beach is hot. Snow can’t fall there. So it never happens."))
    its.append(mcq(S("sunrise") + "Kai says, “The sun comes up sometimes.” Is he right?", "No. It always comes up.",
                   ["Yes. It comes up sometimes.", "No. It never comes up.", "Yes. It is cloudy today."],
                   "The sun comes up every morning, even on cloudy days. So it always comes up."))
    its.append(mcq(S("hockey") + "Leah says, “Our team will always win.” Is she right?", "No. We win sometimes.",
                   ["Yes. We always win.", "No. We never win.", "Yes. We won last time."],
                   "A team can win or lose. Winning last time does not make it sure. So we win sometimes."))
    assert len(its) == 20
    return {"title": "Everyday events: always, sometimes or never?", "items": its}


# ------------------------------------------------------------ set 2: spinners and bags
def set_colours(rnd):
    its = []
    F = lambda sec: fig(spinner_svg(sec))
    B = lambda counts: fig(bag_svg(counts, rnd))
    sec = eq("red", "red", "blue", "red")
    its.append(which_q(F(sec) + "Red or blue: which is more likely?", amounts(sec), "red", "blue", "more", "green",
                       "3 parts are red. Only 1 part is blue. Red has more parts, so red is more likely."))
    sec = eq("green", "yellow", "yellow", "yellow")
    its.append(which_q(F(sec) + "Green or yellow: which is less likely?", amounts(sec), "green", "yellow", "less", CT,
                       "Only 1 part is green. 3 parts are yellow. Green has fewer parts, so green is less likely."))
    sec = eq("red", "blue", "red", "blue")
    its.append(which_q(F(sec) + "Red or blue: which is more likely?", amounts(sec), "red", "blue", "more", CT,
                       "2 parts are red and 2 parts are blue. The parts are the same size. So they are equally likely."))
    c = [("blue", 5), ("red", 1)]
    its.append(which_q(B(c) + "You pick one without looking. Blue or red: which is more likely?", dict(c), "blue", "red",
                       "more", "yellow",
                       "There are 5 blue counters and 1 red counter. More blue, so blue is more likely."))
    c = [("yellow", 2), ("green", 6)]
    its.append(which_q(B(c) + "You pick one without looking. Yellow or green: which is less likely?", dict(c),
                       "yellow", "green", "less", CT,
                       "There are 2 yellow and 6 green. Yellow has fewer, so yellow is less likely."))
    c = [("red", 3), ("blue", 3)]
    its.append(which_q(B(c) + "You pick one without looking. Red or blue: which is less likely?", dict(c),
                       "red", "blue", "less", CT,
                       "3 red and 3 blue. The same number, so they are equally likely. Neither one is less likely."))
    sec = eq("green", "green", "green", "purple", "green", "green")
    its.append(which_q(F(sec) + "Green or purple: which is less likely?", amounts(sec), "green", "purple", "less", CT,
                       "5 parts are green. Only 1 part is purple. Purple has fewer parts, so purple is less likely."))
    sec = eq("red", "blue", "blue", "blue")
    its.append(col_rel_q(F(sec) + "You spin once. Which is right?", amounts(sec), "red", "blue", "You will never get red.",
                         "1 part is red and 3 parts are blue. Red has fewer parts. So red is less likely than blue. "
                         "Red is there, so you can still get it."))
    c = [("yellow", 4), ("purple", 2)]
    its.append(col_rel_q(B(c) + "You pick one without looking. Which is right?", dict(c), "yellow", "purple",
                         "You will always get yellow.",
                         "There are 4 yellow and 2 purple. Yellow has more. So yellow is more likely than purple."))
    sec = eq("red", "blue", "blue", "red")
    its.append(col_rel_q(F(sec) + "You spin once. Which is right?", amounts(sec), "blue", "red", "You will always get blue.",
                         "2 parts are blue and 2 parts are red. Same number, same size. So they are equally likely."))
    its.append(mcq(F(eq("red", "red", "red", "red")) + "You spin once. Which is right?", "You will always get red.",
                   ["You will sometimes get red.", "You will never get red.", "Blue is more likely than red."],
                   "Every part is red. The arrow must land on red. So you will always get red."))
    its.append(mcq(B([("red", 2), ("blue", 2), ("yellow", 2)]) + "Which colour will you never get?", "green",
                   ["red", "blue", "yellow"],
                   "The bag has red, blue and yellow. There is no green. So you will never get green."))
    its.append(mcq(B([("red", 4), ("blue", 2), ("yellow", 1)]) + "Which colour is most likely?", "red",
                   ["blue", "yellow", "green"],
                   "Count each colour: red 4, blue 2, yellow 1. Red has the most. So red is most likely."))
    its.append(mcq(B([("red", 1), ("blue", 4), ("yellow", 2)]) + "Which colour is least likely?", "red",
                   ["blue", "yellow", EQ],
                   "Count each colour: red 1, blue 4, yellow 2. Red has the fewest. So red is least likely."))
    S = lambda spins: fig(spinners_abcd(spins))
    its.append(abcd_q(S([eq("red", "blue", "blue", "blue"), eq("red", "blue", "red", "blue"),
                         eq("red", "red", "blue", "red"), eq("blue", "blue", "blue", "blue")]) +
                      "On which spinner is red more likely than blue?", "Spinner", 2,
                      "Spinner C has 3 red parts and 1 blue part. More red, so red is more likely. "
                      "On A, red is less likely. On B, they are equally likely."))
    its.append(abcd_q(S([eq("red", "red", "red", "red"), eq("red", "yellow", "yellow", "yellow"),
                         eq("blue", "blue", "red", "blue"), eq("red", "blue", "red", "blue")]) +
                      "On which spinner are red and blue equally likely?", "Spinner", 3,
                      "Spinner D has 2 red parts and 2 blue parts. The same, so they are equally likely."))
    G = lambda bags: fig(bags_abcd(bags, rnd))
    its.append(abcd_q(G([[("blue", 6)], [("blue", 3), ("red", 3)], [("blue", 1), ("red", 5)], [("blue", 5), ("red", 1)]]) +
                      "In which bag is blue less likely than red?", "Bag", 2,
                      "Bag C has 1 blue and 5 red. Fewer blue, so blue is less likely than red. "
                      "Bag D has more blue, so blue is more likely there."))
    its.append(abcd_q(G([[("red", 3), ("blue", 3)], [("blue", 6)], [("red", 5), ("yellow", 1)], [("red", 6)]]) +
                      "In which bag will you always get red?", "Bag", 3,
                      "Bag D has only red counters. So you will always get red. Bag C has a yellow one too."))
    its.append(mcq(F(eq("blue", "red", "red", "red")) + "Liam says, “Blue is more likely. It is my favourite.” Is he right?",
                   "No. Red is more likely.",
                   ["Yes. Blue is more likely.", "No. They are equally likely.", "Yes. Blue is his favourite."],
                   "3 parts are red and only 1 is blue. A favourite colour does not change the spinner. "
                   "Red is more likely."))
    its.append(mcq(F(eq("red", "red", "yellow", "red")) + "Ava says, “I will never get yellow. The part is small.” Is she right?",
                   "No. Yellow is less likely.",
                   ["Yes. Yellow will never come.", "No. Yellow is more likely.", "No. Yellow will always come."],
                   "There is 1 yellow part. The arrow can land on it. So yellow is less likely, but not never."))
    assert len(its) == 20
    return {"title": "Spinners and bags: which colour is more likely?", "items": its}


# ------------------------------------------------------------ set 3: compare two events
def set_compare(rnd):
    its = []
    C = lambda a, ca, b, cb: fig(compare_svg(a, ca, b, cb))
    its.append(cmp_q(C("rain", "rain in November", "snow", "snow in July") + "Think about Vancouver. Which is right?",
                     "rain in November", "snow in July", "more", "Rain in November never happens.",
                     "Vancouver gets lots of rain in November. Snow in July does not happen there. "
                     "So rain in November is more likely."))
    its.append(cmp_q(C("beach", "a sunny day", "snow", "a snowstorm") + "It is July in Kelowna. Which is right?",
                     "a sunny day", "a snowstorm", "more", "A sunny day never happens.",
                     "Kelowna is hot and sunny in July. A snowstorm does not happen then. So a sunny day is more likely."))
    its.append(mcq(C("mountain", "snow", "beach", "a hot beach day") + "It is January in Whistler. Which is less likely?",
                   "a hot beach day", ["snow", EQ, CT],
                   "Whistler is cold and snowy in January. A hot beach day does not happen then. "
                   "So a hot beach day is less likely."))
    its.append(mcq(fig(coin_svg()) + "You toss a coin. Heads or tails: which is more likely?", EQ,
                   ["heads", "tails", CT],
                   "A coin has 2 sides. Each side has the same chance. So they are equally likely."))
    its.append(cmp_q(C("gull", "a seagull", "orca", "an orca") + "You ride BC Ferries. Which is right?",
                     "seeing a seagull", "seeing an orca", "more", "Seeing an orca never happens.",
                     "Seagulls fly near the ferry on most trips. Orcas swim by only sometimes. "
                     "So seeing a seagull is more likely."))
    its.append(mcq(fig(cube_faces_svg()) + "You roll a number cube. 6 or 1: which is more likely?", EQ,
                   ["6", "1", CT],
                   "6 and 1 are each on 1 face. So they are equally likely. A big number is not harder to roll."))
    its.append(mcq(C("night", "stars", "sunrise", "the sun") + "It is a clear night. Which will you more likely see?",
                   "stars", ["the sun", EQ, CT],
                   "On a clear night, you can see stars. The sun does not shine at night. So stars are more likely."))
    its.append(cmp_q(C("snow", "snow", "beach", "a hot beach day") + "It is January in Prince George. Which is right?",
                     "snow on the ground", "a hot beach day", "more", "Snow on the ground never happens.",
                     "Prince George is very cold in January. Snow is on the ground most days. "
                     "So snow is more likely than a hot beach day."))
    its.append(mcq(C("rain", "rain", "beach", "a sunny day") + "Dark clouds fill the sky. Which is more likely?",
                   "rain", ["a sunny day", EQ, CT],
                   "Dark clouds often bring rain. So rain is more likely than a sunny day."))
    its.append(mcq(fig(scene_svg("popsicle")) + "A popsicle sits in the hot sun. Which is more likely?",
                   "It melts.", ["It gets colder.", SAME, "You can’t tell."],
                   "The hot sun warms the popsicle. Ice melts when it gets warm. So melting is more likely."))
    its.append(mcq(fig(hat_svg(["Mei", "Liam", "Owen", "Zara"])) +
                   "The teacher picks one name. Mei or Liam: which is more likely?", EQ, ["Mei", "Liam", CT],
                   "Each name is in the hat 1 time. So Mei and Liam are equally likely."))
    its.append(mcq(fig(scene_svg("school")) + "It is a school day. Which is more likely?", "You read a book.",
                   ["You ride an elephant.", SAME, "You can’t tell."],
                   "You read books at school a lot. You never ride an elephant there. So reading a book is more likely."))
    its.append(mcq(C("snow", "snow in July", "rain", "rain in November") + "Think about Vancouver. Which is right?",
                   "Snow in July is less likely.",
                   ["Snow in July is more likely.", SAME, "Snow in July always happens."],
                   "Snow does not fall in Vancouver in July. Rain in November happens a lot. "
                   "So snow in July is less likely."))
    its.append(mcq(C("beach", "the beach", "snow", "a snowman") + "It is a hot July day. Which is less likely?",
                   "building a snowman", ["going to the beach", EQ, CT],
                   "There is no snow on a hot July day. So building a snowman is less likely than going to the beach."))
    its.append(mcq(fig(cube_faces_svg()) + "Ryan rolls a number cube. A 3 or a 7: which is more likely?", "a 3",
                   ["a 7", EQ, CT],
                   "3 is on the cube. 7 is not, so you can never roll 7. So a 3 is more likely."))
    its.append(mcq(fig(scene_svg("salmon")) + "It is fall at a BC river. Which will you more likely see?", "a salmon",
                   ["a shark", EQ, CT],
                   "In fall, salmon swim up BC rivers. Sharks do not live in rivers. So a salmon is more likely."))
    its.append(mcq(fig(cube_faces_svg()) + "Ryan says, “6 is less likely than 1. It is a big number.” Is he right?",
                   "No. They are equally likely.",
                   ["Yes. 6 is less likely.", "No. 6 is more likely.", "Yes. Big numbers are hard."],
                   "6 is on 1 face, just like 1. So they are equally likely. Big numbers are not harder to roll."))
    its.append(mcq(C("gull", "a seagull", "orca", "an orca") +
                   "Wei rides BC Ferries. He says, “An orca is more likely than a seagull.” Is he right?",
                   "No. A seagull is more likely.",
                   ["Yes. An orca is more likely.", "No. They are equally likely.", "Yes. Orcas are big."],
                   "Seagulls are near the ferry on most trips. Orcas come by only sometimes. "
                   "So a seagull is more likely. Being big does not make it more likely."))
    its.append(mcq(fig(coin_svg()) + "Chloe says, “Tails is more likely than heads.” Is she right?",
                   "No. They are equally likely.",
                   ["Yes. Tails is more likely.", "No. Heads is more likely.", "Yes. Tails is her favourite."],
                   "A coin has 2 sides with the same chance. So heads and tails are equally likely."))
    its.append(mcq(fig(scene_svg("rain")) + "It is November in Vancouver. Which is most likely?", "a rainy day",
                   ["a hot beach day", "a snowstorm", CT],
                   "November in Vancouver is cool and very rainy. Hot beach days and snowstorms are rare then. "
                   "So a rainy day is most likely."))
    assert len(its) == 20
    return {"title": "Compare two events: more, less or equally likely?", "items": its}


# ------------------------------------------------------------ set 4: predictions
def set_predict(rnd):
    its = []
    F = lambda sec: fig(spinner_svg(sec))
    B = lambda counts: fig(bag_svg(counts, rnd))
    its.append(mcq(F(eq("red", "red", "blue", "red")) + "Kai spins 10 times. What will he probably see?",
                   "more red than blue", ["more blue than red", "red and blue the same", "no red at all"],
                   "3 parts are red and 1 is blue. Red is more likely. So he will probably see more red than blue."))
    its.append(mcq(fig(coin_svg()) + "Mei tosses a coin 10 times. What will probably happen?",
                   "some heads and some tails", ["heads 10 times", "tails 10 times", "a 3 every time"],
                   "Heads and tails are equally likely. So she will probably get some of each. A coin has no 3."))
    c = [("blue", 6), ("red", 2)]
    its.append(which_q(B(c) + "Which colour will you probably pick?", dict(c), "blue", "red", "more", "yellow",
                       "There are 6 blue and 2 red. Blue is more likely. So you will probably pick blue."))
    its.append(mcq(B([("red", 2), ("blue", 2)]) + "Mateo puts in 3 more red. Which is more likely now?", "red",
                   ["blue", EQ, "green"],
                   "Red: 2 + 3 = 5. Blue: 2. 5 is more than 2. So red is more likely now."))
    its.append(mcq(B([("red", 3), ("blue", 4)]) + "Hana takes out 2 blue. Which is more likely now?", "red",
                   ["blue", EQ, CT],
                   "Blue: 4 − 2 = 2. Red: 3. 3 is more than 2. So red is more likely now."))
    S = lambda spins: fig(spinners_abcd(spins))
    its.append(abcd_q(S([eq("blue", "blue", "blue", "blue"), eq("red", "blue", "red", "blue"),
                         eq("red", "red", "blue", "red"), eq("red", "blue", "blue", "blue")]) +
                      "Kai spins 10 times. He gets red 8 times and blue 2 times. Which spinner did he probably use?",
                      "Spinner", 2,
                      "He got a lot more red. Spinner C has 3 red parts and 1 blue part. Red is more likely there."))
    its.append(abcd_q(S([eq("red", "red", "red", "red"), eq("red", "blue", "red", "blue"),
                         eq("blue", "blue", "red", "blue"), eq("red", "red", "blue", "red")]) +
                      "Sofia spins 10 times. She gets red 5 times and blue 5 times. Which spinner did she probably use?",
                      "Spinner", 1,
                      "She got red and blue the same. On spinner B, red and blue are equally likely."))
    G = lambda bags: fig(bags_abcd(bags, rnd))
    its.append(abcd_q(G([[("green", 1), ("red", 5)], [("green", 3), ("red", 3)], [("green", 5), ("red", 1)], [("red", 6)]]) +
                      "You want green. Which bag is best?", "Bag", 2,
                      "Each bag has 6 counters. Bag C has 5 green. So green is most likely in bag C."))
    its.append(abcd_q(G([[("yellow", 2), ("blue", 4)], [("yellow", 6)], [("yellow", 3), ("blue", 3)], [("blue", 6)]]) +
                      "Which bag will never give you yellow?", "Bag", 3,
                      "Bag D has only blue counters. There is no yellow. So you will never get yellow from bag D."))
    its.append(mcq(F(eq(1, 1, 2, 1)) + "Which number will you probably get?", "1", ["2", EQ, "3"],
                   "3 parts have a 1. Only 1 part has a 2. So 1 is more likely."))
    its.append(mcq(fig(cube_faces_svg()) + "Ji-woo rolls a number cube 12 times. Will she roll a 7?",
                   "No. 7 is not on it.", ["Yes. 7 is likely.", "Yes, if she rolls a lot.", "Yes. 7 is lucky."],
                   "The faces show 1 to 6. There is no 7. So she will never roll a 7, even if she rolls a lot."))
    its.append(mcq(fig(scene_svg("beach")) + "It is July in Kelowna. What weather will probably come?",
                   "hot and sunny", ["cold and snowy", "icy and freezing", CT],
                   "Summer in Kelowna is hot and sunny. Snow and ice are not likely in July."))
    its.append(mcq(fig(scene_svg("snow")) + "It is January in Prince George. What will you probably wear outside?",
                   "a warm coat and mitts", ["a swimsuit", "shorts and sandals", "only a sun hat"],
                   "Prince George is very cold in January. Snow is likely. So you will probably wear a warm coat and mitts."))
    its.append(mcq(fig(scene_svg("rain")) + "It is November in Vancouver. What should Noah bring to school?",
                   "an umbrella", ["a beach ball", "a swimsuit", "only sunscreen"],
                   "Rain is very likely in Vancouver in November. So an umbrella is the best thing to bring."))
    its.append(mcq(fig(scene_svg("mountain")) + "Kai goes to Whistler for Spring Break in March. What will he probably do?",
                   "ski on the snow", ["swim in a lake", "pick apples", "go to the beach"],
                   "In March there is still lots of snow on the mountains at Whistler. So skiing is most likely."))
    its.append(mcq(fig(scene_svg("salmon")) + "It is fall. Olivia visits a BC river. What will she probably see?",
                   "salmon swimming", ["a snowman", "an orca", "a penguin"],
                   "In fall, salmon swim up many BC rivers. Orcas live in the sea, not rivers. So salmon are most likely."))
    its.append(mcq(fig(scene_svg("rain")) + "Dark clouds fill the sky. Should Lucas take his umbrella?",
                   "Yes. Rain is likely.",
                   ["No. Rain will never come.", "No. It is not raining yet.", "Yes. Rain will always come."],
                   "Dark clouds often bring rain. So rain is likely. It is not sure, so “always” is the wrong reason."))
    its.append(mcq(F(eq("purple", "green", "green", "green")) + "Hana loves purple. Which colour will she probably get?",
                   "green", ["purple", EQ, "red"],
                   "3 parts are green and only 1 is purple. Her favourite colour does not change the spinner. "
                   "Green is more likely."))
    its.append(mcq(B([("red", 5), ("blue", 1)]) + "Jasleen wants blue. What will probably happen?", "She picks red.",
                   ["She picks blue.", "Both are equally likely.", "She picks green."],
                   "Look in the bag: 5 red and 1 blue. Wanting blue does not help. Red is more likely."))
    its.append(mcq(fig(scene_svg("bus")) + "The school bus comes every school day. Tomorrow is Tuesday. What will probably happen?",
                   "The bus will come.", ["The bus will never come.", "A dog will drive it.", "It will come at midnight."],
                   "Tuesday is a school day. The bus comes every school day. So the bus will come."))
    assert len(its) == 20
    return {"title": "Predictions: what will probably happen?", "items": its}


# ------------------------------------------------------------ set 5: word problems
def set_stories(rnd):
    its = []
    Cn = fig(coin_svg())
    D = fig(cube_faces_svg())
    its.append(mcq(Cn + "Before a soccer game, the referee tosses a coin. Our captain calls heads. Which is right?",
                   "Heads and tails are equally likely.",
                   ["Heads is more likely.", "Tails is more likely.", "Heads will always come."],
                   "A coin can land on heads or tails. Each side has the same chance. So they are equally likely."))
    its.append(mcq(Cn + "Mei gets heads 3 times. She tosses again. Which is right?",
                   "Heads and tails are still equally likely.",
                   ["Tails is more likely now.", "Heads is more likely now.", "Tails will never come."],
                   "A coin does not remember. Each toss, heads and tails have the same chance."))
    H4 = fig(hat_svg(["Mei", "Liam", "Owen", "Zara"]))
    its.append(mcq(H4 + "The teacher picks one name from the hat. Which is right?",
                   "Each name is equally likely.",
                   ["Liam is more likely than Mei.", "Owen will always be picked.", "Zara will never be picked."],
                   "Each name is in the hat 1 time. So every name has the same chance."))
    its.append(mcq(H4 + "Nadia’s name is not in the hat. Which is right?",
                   "Nadia will never be picked.",
                   ["Nadia is more likely than Mei.", "Nadia will always be picked.", "Nadia is equally likely."],
                   "Only names in the hat can be picked. Nadia’s name is not there. So she will never be picked."))
    its.append(mcq(fig(hat_svg(["Owen"])) + "Only Owen’s name is in the hat. The teacher picks one. Which is right?",
                   "Owen will always be picked.",
                   ["Owen will sometimes be picked.", "Owen will never be picked.", "Zara is more likely."],
                   "There is only one name in the hat. It must be Owen. So Owen will always be picked."))
    its.append(mcq(fig(popsicles_svg([("red", 4), ("yellow", 2)], rnd)) +
                   "Emma takes a popsicle without looking. Which is she more likely to get?",
                   "a red one", ["a yellow one", EQ, "a green one"],
                   "There are 4 red and 2 yellow. More red, so a red one is more likely. There are no green ones."))
    its.append(mcq(fig(popsicles_svg([("yellow", 3)], rnd)) +
                   "Only yellow popsicles are left. Liam takes one. Which is right?",
                   "He will always get yellow.",
                   ["He will sometimes get yellow.", "He will never get yellow.", "Red is more likely."],
                   "Every popsicle left is yellow. So he will always get yellow."))
    c = [("blue", 5), ("red", 1)]
    its.append(col_rel_q(fig(mitts_svg(c, rnd)) +
                         "Sofia picks a mitt from the lost and found without looking. Which is right?",
                         dict(c), "red", "blue", "She will never get red.",
                         "There are 5 blue mitts and 1 red mitt. Fewer red, so red is less likely than blue. "
                         "Red is there, so she can still get it."))
    c = [("red", 3), ("blue", 3)]
    its.append(col_rel_q(fig(mitts_svg(c, rnd)) + "Owen picks a mitt from the bin without looking. Which is right?",
                         dict(c), "red", "blue", "He will always get red.",
                         "There are 3 red mitts and 3 blue mitts. The same number, so they are equally likely."))
    its.append(mcq(fig(scene_svg("race")) + "Our school does the Terry Fox Run in September. Which weather is least likely?",
                   "a snowstorm", ["a sunny day", "a cloudy day", "a rainy day"],
                   "September can be sunny, cloudy or rainy. A snowstorm is very rare then. So it is least likely."))
    c = [("red", 6), ("yellow", 1)]
    its.append(col_rel_q(fig(bag_svg(c, rnd, "prize bag of balls")) +
                         "At the fall fair, the yellow ball wins a prize. Ava picks one ball. Which is right?",
                         dict(c), "yellow", "red", "She will never get yellow.",
                         "There is 1 yellow ball and 6 red balls. Fewer yellow, so yellow is less likely than red."))
    G = lambda bags: fig(bags_abcd(bags, rnd))
    its.append(abcd_q(G([[("blue", 6)], [("red", 2), ("blue", 4)], [("red", 4), ("blue", 2)], [("red", 1), ("blue", 5)]]) +
                      "Arjun wins if he picks red. Which bag should he pick from?", "Bag", 2,
                      "Bag C has 4 red counters. That is the most red, so red is most likely there. "
                      "In bag A, he will never get red."))
    S = lambda spins: fig(spinners_abcd(spins))
    its.append(abcd_q(S([eq("blue", "blue", "blue", "blue"), eq("blue", "red", "blue", "red"),
                         eq("red", "red", "red", "red"), eq("blue", "yellow", "yellow", "yellow")]) +
                      "Simran wins if she lands on blue. Which spinner should she use?", "Spinner", 0,
                      "Spinner A is all blue. She will always get blue. On spinner C, she will never get blue."))
    its.append(mcq(fig(bag_svg([("blue", 2), ("green", 2)], rnd)) + "Harjot needs a yellow counter for a game. What can he do?",
                   "Put a yellow one in the bag.",
                   ["Pick again and again.", "Pick with his eyes shut.", "Shake the bag hard."],
                   "There is no yellow in the bag, so he will never get one. Picking again does not help. "
                   "He must put a yellow counter in."))
    its.append(mcq(fig(scene_svg("orca")) + "Owen goes whale watching near Victoria. Which is right?",
                   "He may see an orca, or may not.",
                   ["He will always see an orca.", "He will never see an orca.", "Orcas live in lakes."],
                   "Orcas swim in the sea near Victoria. Some trips see them, some do not. So he may see one."))
    its.append(mcq(fig(scene_svg("calendar", day="July 1")) + "It is Canada Day. Which will always happen?",
                   "Tomorrow will be July 2.",
                   ["There will be fireworks.", "It will rain.", "It will snow."],
                   "July 2 always comes after July 1. Fireworks and rain happen only sometimes."))
    its.append(mcq(fig(scene_svg("hockey")) + "Our team won 3 games in a row. Which is right about the next game?",
                   "We may win or lose.", ["We will always win now.", "We will never win.", "We will win 3 more."],
                   "Winning before does not make the next game sure. We may win or lose."))
    its.append(mcq(fig(scene_svg("race")) + "On Sports Day, 6 children run a race. Ethan is one of them. Which is right?",
                   "Ethan may win, or may not.",
                   ["Ethan will always win.", "Ethan will never win.", "All 6 children will win."],
                   "Any of the 6 children could win. We can’t be sure it is Ethan. So he may win, or may not."))
    its.append(mcq(D + "Ryan needs an 8 to win the game. He rolls a number cube. Which is right?",
                   "He will never get an 8.",
                   ["An 8 is more likely.", "An 8 is equally likely.", "He will always get an 8."],
                   "The faces show 1 to 6. There is no 8. So he will never get an 8."))
    its.append(mcq(fig(scene_svg("popsicle")) + "Kai leaves his popsicle in the sun on a hot day in Kelowna. Which is right?",
                   "Melting is more likely than freezing.",
                   ["Freezing is more likely than melting.", "They are equally likely.", "It will never melt."],
                   "The hot sun warms the popsicle. Warm ice melts. So melting is more likely."))
    assert len(its) == 20
    return {"title": "Word problems: which is more likely?", "items": its}


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
        "<h2>Always, sometimes, never</h2>"
        "<p>Some things happen every time. Some things may happen. Some things can’t happen. We use three words.</p>" +
        table(["Word", "Meaning", "Example"], [
            ["<b>always</b>", "It happens every time.", "The sun comes up in the morning."],
            ["<b>sometimes</b>", "It may happen, or not.", "It rains in Vancouver."],
            ["<b>never</b>", "It can’t happen.", "A dog drives the school bus."],
        ]) +
        "<figure class='sn-fig'>" + scene_svg("sunrise") +
        "<figcaption>The sun comes up every morning. That is always.</figcaption></figure>" +
        ex("Example", "Our hockey team plays today. Will we win?",
           "A team can win or lose. We are not sure.", "We win sometimes.") +
        "<h2>More likely, less likely, equally likely</h2>"
        "<p>Count the parts on a spinner. The colour with <b>more</b> parts is <b>more likely</b>. "
        "The colour with <b>fewer</b> parts is <b>less likely</b>. "
        "If the colours have the <b>same</b> number of parts, they are <b>equally likely</b>.</p>"
        "<figure class='sn-fig'>" + spinner_svg(eq("red", "red", "blue", "red"), "spinner: 3 red parts and 1 blue part") +
        "<figcaption>3 red parts and 1 blue part. Red is more likely. Blue is less likely.</figcaption></figure>" +
        ex("Example", "Is blue more likely or less likely than red?", "Blue has 1 part. Red has 3 parts. 1 is fewer than 3.",
           "Blue is less likely than red.") +
        "<p>A bag of counters works the same way. Look in the bag first. Count each colour.</p>"
        "<figure class='sn-fig'>" + bag_svg([("red", 3), ("blue", 3)], rnd, "bag: 3 red counters and 3 blue counters") +
        "<figcaption>3 red counters and 3 blue counters.</figcaption></figure>" +
        ex("Example", "Which colour is more likely?", "3 red and 3 blue. The numbers are the same.",
           "They are equally likely.") +
        "<h2>Comparing two events</h2>"
        "<p>Think about what usually happens. The thing that happens more often is more likely.</p>"
        "<figure class='sn-fig'>" + compare_svg("rain", "rain in November", "snow", "snow in July").replace("<svg ", "<svg data-pf='lg' ", 1) +
        "<figcaption>In Vancouver, rain in November is more likely than snow in July.</figcaption></figure>" +
        ex("Example", "You ride BC Ferries. Which is more likely: a seagull or an orca?",
           "Seagulls are near the ferry on most trips. Orcas come by only sometimes.", "a seagull") +
        "<h2>Common mistakes</h2>" +
        table(["Mistake", "What to do instead"], [
            ["Mixing up more likely and less likely", "More parts or counters means more likely. Fewer means less likely"],
            ["Saying “never” when there is only a little of a colour", "If it is there at all, it can happen"],
            ["Saying “always” when it only happens a lot", "Always means every time, with no other way"],
            ["Choosing your favourite colour", "Count the parts or counters of each colour"],
            ["Thinking 6 is harder to roll than 1", "Every number on a number cube is equally likely"],
        ])
    )


FAQ = [
    {"q": "What do Grade 1 students learn about likelihood in BC?",
     "a": "In the BC Mathematics Curriculum, Grade 1 students describe the likelihood of familiar life events using comparative language. They say whether something is more likely, less likely or equally likely, and use words like always, sometimes and never."},
    {"q": "What does equally likely mean?",
     "a": "Equally likely means two things have the same chance. When you toss a coin, heads and tails are equally likely."},
    {"q": "How can I practise likelihood with my child at home?",
     "a": "Put 5 red blocks and 1 blue block in a bag and ask “Which colour is more likely?” Pick without looking a few times to check, then change the blocks and try again."},
    {"q": "Why does my child mix up more likely and less likely?",
     "a": "Many children pick the colour they see least, or their favourite colour. Count the parts or counters together first: the colour with more is more likely, and the colour with fewer is less likely."},
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
    rnd = random.Random(51810)
    sets = [set_everyday(rnd), set_colours(rnd), set_compare(rnd), set_predict(rnd), set_stories(rnd)]
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
        "country": "ca-bc", "subject": "math", "grade": "grade-1", "slug": "likelihood", "sort": 10,
        "updated": UPDATED, "pdf_url": "",
        "title": "Likelihood: More Likely, Less Likely or Equally Likely",
        "seo_title": "Grade 1 Math Likelihood Worksheets for the BC Curriculum (Free, with Answer Key)",
        "short_title": "Likelihood",
        "domain": "Data and probability",
        "standard_code": "Grade 1: Data and probability",
        "standard_url": "https://curriculum.gov.bc.ca/curriculum/mathematics/1/core",
        "standard_text": "Likelihood of familiar life events, using comparative language",
        "meta_desc": "Free Grade 1 math worksheets on likelihood for the BC curriculum: use always, sometimes and never for everyday events, find which colour is more likely on a spinner or in a bag, compare two events as more likely, less likely or equally likely, and make predictions. 100 questions with an answer key.",
        "key_big": "More chances means more likely. Fewer chances means less likely. The same chances means equally likely.",
        "key_sub": "Always means it happens every time. Sometimes means it may happen. Never means it can’t happen. Count the parts or counters of each colour before you decide.",
        "body_html": body_html(rnd), "faq": FAQ, "sets": sets,
    }
    return mark_large(u, "spinners A to D|bags A to D|the six faces of a number cube|mitts|popsicles|two pictures: [^']*")


if __name__ == "__main__":
    u = gen_unit()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
