# -*- coding: utf-8 -*-
"""
Australia Year 4 Maths: Chance (Australian Curriculum v9.0: AC9M4P01, AC9M4P02)
  python3 tools/gen_au_maths_y4_chance.py
Chance words and ordering everyday events from impossible to certain, possible outcomes of chance experiments
(coins, dice, spinners, bags of counters, number cards), ordering outcomes by likelihood, independent events
(a coin has no memory; picking with and without putting back) and repeated experiments with tallies and tables.
Wrong answers come from real student mistakes: the gambler's fallacy ("tails is due"), counting pieces of a spinner
instead of their size, "likely" confused with "certain", "unlikely" confused with "impossible", judging by where a
section is or by the size of a number, and expecting the same results every time.
Every picture shows the colour as a letter too (R = red ...), so it still works when printed in black and white.
HTML attributes use single quotes (no backslashes in the JSON). Australian English.
"""
import json, re, math, os, random

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "au", "maths", "year-4")
UPDATED = "2026-11-02"
GREEN = "#006633"
FILL = "#cfe6d6"
FILL2 = "#e6f2ea"
INK = "#2b2b2b"
FONT = "Arial, Helvetica, sans-serif"

# colour name -> (letter, fill)
COL = {
    "red": ("R", "#f28b82"),
    "blue": ("B", "#8ab4f8"),
    "yellow": ("Y", "#fde293"),
    "green": ("G", "#81c995"),
    "purple": ("P", "#c58af9"),
}
WORDS = ["certain", "likely", "unlikely", "impossible"]


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


def word_q(q, word, e):
    """The four chance words, always in the same order: certain, likely, unlikely, impossible."""
    return mcq_fixed(q, WORDS, WORDS.index(word), e)


def abcd_q(q, kind, ai, e):
    return mcq_fixed(q, ["%s %s" % (kind, L) for L in "ABCD"], ai, e)


def chance_word(k, n):
    assert 0 <= k <= n and 2 * k != n
    if k == 0:
        return "impossible"
    if k == n:
        return "certain"
    return "likely" if 2 * k > n else "unlikely"


def fig(svg):
    return "<div class='qfig'>" + svg + "</div>"


def svg_wrap(w, h, body, label):
    return ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 %d %d' width='%d' height='%d' "
            "role='img' aria-label='%s'><g font-family='%s'>%s</g></svg>" % (w, h, w, h, label, FONT, body))


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
    s.append(text(W / 2, H + 14, "     ".join(key_lines(colours_in(allc))), 14))
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


# ------------------------------------------------------------ lesson pictures
def scale_svg():
    W, H = 490, 92
    x0, x1, y = 50, 440, 46
    s = ["<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='3'/>" % (x0, y, x1, y, GREEN)]
    marks = [(0, "impossible", -1), (0.25, "unlikely", 1), (0.5, "equally likely", -1), (0.75, "likely", 1), (1, "certain", -1)]
    for f, w, side in marks:
        x = x0 + f * (x1 - x0)
        s.append("<line x1='%.1f' y1='%d' x2='%.1f' y2='%d' stroke='%s' stroke-width='2'/>" % (x, y - 8, x, y + 8, GREEN))
        s.append(text(x, y - 16 if side < 0 else y + 29, w, 15, bold=True))
    return svg_wrap(W, H, "".join(s), "chance scale from impossible to certain")


def dice_faces_svg():
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
    return svg_wrap(4 + 6 * sz + 5 * gap + 4, 4 + sz + 28, "".join(s), "the six faces of a dice")



def scale_points_svg(points, label="chance scale with points A to D"):
    """points = {letter: position 0..1} placed on an impossible-to-certain line."""
    W, H = 500, 100
    x0, x1, y = 60, 440, 62
    s = ["<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='3'/>" % (x0, y, x1, y, GREEN)]
    for f, w in [(0, "impossible"), (0.5, "even chance"), (1, "certain")]:
        x = x0 + f * (x1 - x0)
        s.append("<line x1='%.1f' y1='%d' x2='%.1f' y2='%d' stroke='%s' stroke-width='2'/>" % (x, y - 7, x, y + 7, GREEN))
        s.append(text(x, y + 30, w, 15))
    xs = []
    for L in "ABCD":
        f = points[L]
        x = x0 + f * (x1 - x0)
        xs.append(x)
        s.append("<line x1='%.1f' y1='%d' x2='%.1f' y2='%d' stroke='%s' stroke-width='2'/>" % (x, 33, x, y - 3, INK))
        s.append("<polygon points='%.1f,%d %.1f,%d %.1f,%d' fill='%s'/>" % (x, y - 2, x - 5, y - 11, x + 5, y - 11, INK))
        s.append("<circle cx='%.1f' cy='20' r='13' fill='#ffffff' stroke='%s' stroke-width='2'/>" % (x, INK))
        s.append(text(x, 25, L, 15, bold=True))
    xs.sort()
    assert all(b - a >= 34 for a, b in zip(xs, xs[1:])), points
    return svg_wrap(W, H, "".join(s), label)


# ------------------------------------------------------------ set 1: chance words and ordering events
def set_words(rnd):
    its = []
    its.append(word_q("The month after March will be April. This is …", "certain",
                      "The months always come in the same order. April always comes after March, so it is certain."))
    its.append(word_q("Next year will have 13 months. This is …", "impossible",
                      "Every year has 12 months. A year can never have 13 months, so it is impossible."))
    its.append(word_q("It will be cold at night in Canberra in July. This is …", "likely",
                      "July is winter in Australia, and Canberra nights in winter are usually very cold, often below 0 °C. "
                      "A mild night could happen, so it is likely, not certain."))
    its.append(word_q("A platypus will walk across the school playground today. This is …", "unlikely",
                      "Platypuses live in creeks and rivers and are hardly ever seen. It is not impossible, "
                      "but it almost never happens, so it is unlikely."))
    its.append(word_q("If today is Saturday, tomorrow will be Sunday. This is …", "certain",
                      "Sunday always comes after Saturday, so it is certain."))
    its.append(word_q("Cooper will grow 2 metres taller this week. This is …", "impossible",
                      "Children grow a few centimetres a year, not 2 metres in a week. It can never happen, so it is impossible."))
    its.append(word_q("Christmas Day in Brisbane will be warm. This is …", "likely",
                      "Christmas is in summer in Australia, and Brisbane summers are warm. A cooler, rainy day is possible, "
                      "so it is likely, not certain."))
    its.append(word_q("A kookaburra will land on Mia’s desk during maths. This is …", "unlikely",
                      "A kookaburra could fly into a classroom, but it hardly ever happens. So it is unlikely, not impossible."))
    its.append(word_q("Isla throws a ball up into the air. It will come back down. This is …", "certain",
                      "A ball thrown up always falls back down. It must happen, so it is certain."))
    its.append(word_q("Lachlan buys 1 ticket in a raffle. 200 tickets are sold. Lachlan will win. This is …", "unlikely",
                      "Lachlan has only 1 of the 200 tickets. He could win, but it is unlikely."))
    its.append(word_q("A goldfish will climb a tree. This is …", "impossible",
                      "A goldfish lives in water and cannot climb. It can never happen, so it is impossible."))
    its.append(word_q("Dark clouds cover the sky. Jack says, “It is certain to rain today.” Which word is better?", "likely",
                      "Dark clouds mean rain will probably come, but the clouds might blow away. "
                      "It could still not rain, so it is likely, not certain."))
    its.append(mcq("Which event is impossible?", "Walking from Perth to Sydney in one hour",
                   ["It will rain in Darwin in the wet season", "Liam will kick a goal at footy on Saturday",
                    "The school canteen will sell a pie today"],
                   "Perth and Sydney are more than 3000 km apart. Nobody can walk that far in one hour, so it is impossible. "
                   "The other events could happen."))
    its.append(mcq("Which event is more likely?", "rain in Darwin in January",
                   ["rain in Darwin in July", "They are equally likely", "Both are impossible"],
                   "January is in Darwin’s wet season, when it rains most days. July is in the dry season, when it hardly rains. "
                   "So rain in January is more likely."))
    its.append(mcq("Put these events in order from impossible to certain.<br>"
                   "P: The sun will rise tomorrow.<br>Q: A dog will read a book.<br>"
                   "R: Ava will eat lunch at school today.<br>S: A koala will visit your classroom.",
                   "Q, S, R, P", ["P, R, S, Q", "Q, R, S, P", "S, Q, R, P"],
                   "Q is impossible, S is unlikely, R is likely and P is certain. So the order is Q, S, R, P. "
                   "Unlikely comes before likely."))
    its.append(mcq("Which list goes from least likely to most likely?",
                   "impossible, unlikely, likely, certain",
                   ["certain, likely, unlikely, impossible", "unlikely, impossible, likely, certain",
                    "impossible, likely, unlikely, certain"],
                   "Impossible means it never happens and certain means it always happens. "
                   "Unlikely (not often) comes before likely (most of the time)."))
    L1 = {"A": 0.15, "B": 1.0, "C": 0.5, "D": 0.0}
    L2 = {"A": 1.0, "B": 0.85, "C": 0.15, "D": 0.5}
    P1 = fig(scale_points_svg(L1))
    P2 = fig(scale_points_svg(L2))
    its.append(abcd_q(P1 + "Which point shows the chance of rolling a 7 on a normal dice?", "Point", 3,
                      "A dice shows 1 to 6, so a 7 is impossible. Point D is at impossible. Point A is unlikely, not impossible."))
    its.append(abcd_q(P1 + "Which point shows the chance of a coin landing on heads?", "Point", 2,
                      "A coin has 2 sides, heads and tails, so heads is an even chance. Point C is at even chance."))
    its.append(abcd_q(P2 + "A bag has 9 red counters and 1 blue counter. Which point best shows the chance of picking red?",
                      "Point", 1,
                      "9 of the 10 counters are red, so red is likely, close to certain. Point B. "
                      "It is not certain (point A), because there is 1 blue counter."))
    its.append(abcd_q(P2 + "Which point shows the chance that the sun will set tonight?", "Point", 0,
                      "The sun sets every evening. It must happen, so it is certain: point A."))
    assert len(its) == 20
    return {"title": "Chance words: from impossible to certain", "items": its}


# ------------------------------------------------------------ set 2: possible outcomes
def set_outcomes(rnd):
    its = []
    its.append(mcq("Oliver tosses a coin. Which list shows all the possible outcomes?", "heads, tails",
                   ["heads", "tails", "heads, heads, tails"],
                   "A coin can land on heads or on tails. List each outcome once: heads, tails."))
    its.append(mcq("Charlotte rolls a dice. Which list shows all the possible outcomes?", "1, 2, 3, 4, 5, 6",
                   ["1, 2, 3, 4, 5", "0, 1, 2, 3, 4, 5, 6", "2, 4, 6"],
                   "A dice has 6 faces with 1 to 6 dots. Any face can land on top. There is no 0."))
    sec = eq("red", "blue", "red", "yellow", "red", "blue")
    assert len(amounts(sec)) == 3
    its.append(mcq(fig(spinner_svg(sec)) + "This spinner has 6 sections. How many different outcomes (colours) are there?",
                   "3", ["6", "2", "4"],
                   "Count the different colours, not the sections: red, blue and yellow. That is 3 outcomes."))
    its.append(mcq(fig(bag_svg([("red", 5), ("green", 3)], rnd)) + "Ruby picks one counter without looking. "
                   "Which list shows all the possible outcomes?", "red, green",
                   ["red", "red, green, blue", "5, 3"],
                   "The counter can be red or green. Green is possible, even though there are fewer green counters. "
                   "There is no blue."))
    its.append(mcq("Number cards 1 to 8 are face down. Aarav picks one card. How many possible outcomes are there?",
                   "8", ["9", "7", "1"],
                   "Any card from 1 to 8 can be picked: 1, 2, 3, 4, 5, 6, 7, 8. That is 8 outcomes."))
    its.append(mcq(fig(spinner_svg(eq(1, 2, 3, 4, 5))) + "Leo spins this spinner. Which outcome is impossible?",
                   "landing on 6", ["landing on 1", "landing on 5", "landing on 3"],
                   "The spinner has the numbers 1 to 5. There is no 6, so landing on 6 is impossible."))
    its.append(word_q("Rolling a number from 1 to 6 on a dice is …", "certain",
                      "Every roll gives 1, 2, 3, 4, 5 or 6. It must happen, so it is certain."))
    its.append(word_q(fig(bag_svg([("blue", 4), ("green", 4)], rnd)) + "Picking a yellow counter from this bag is …", "impossible",
                      "The bag has only blue and green counters. There is no yellow, so it is impossible."))
    its.append(word_q(fig(spinner_svg([("green", 3), ("purple", 1)])) + "Landing on purple is …", "unlikely",
                      "Purple is only a quarter of the spinner. It can happen, but not often, so it is unlikely."))
    assert chance_word(4, 6) == "likely"
    its.append(word_q("Rolling a number greater than 2 on a dice is …", "likely",
                      "Greater than 2: 3, 4, 5, 6. That is 4 of the 6 faces, so it is likely. "
                      "It is not certain, because 1 or 2 could come up."))
    its.append(mcq("Sienna rolls a dice. Which list shows all the even outcomes?", "2, 4, 6",
                   ["2, 4", "1, 3, 5", "2, 4, 6, 8"],
                   "The even numbers on a dice are 2, 4 and 6. 1, 3 and 5 are odd, and there is no 8 on a dice."))
    assert [n for n in range(1, 7) if n % 2 == 1 and n > 2] == [3, 5]
    its.append(mcq("Zara rolls a dice. Which list shows all the odd outcomes greater than 2?", "3, 5",
                   ["3, 4, 5, 6", "1, 3, 5", "5"],
                   "Odd numbers on a dice: 1, 3, 5. Greater than 2 leaves 3 and 5."))
    word = "KANGAROO"
    assert len(word) == 8 and len(set(word)) == 6
    its.append(mcq("The letters of KANGAROO are written on 8 cards, one letter on each card. Mei picks one card. "
                   "How many different letters could she get?", "6", ["8", "7", "5"],
                   "The letters are K, A, N, G, A, R, O, O. A and O appear twice, but each is one outcome. "
                   "The different letters are K, A, N, G, R, O: 6 outcomes."))
    its.append(mcq(fig(spinner_svg([("red", 2), ("blue", 1), ("yellow", 1)])) +
                   "Which list shows all the possible outcomes of this spinner?", "red, blue, yellow",
                   ["red, red, blue, yellow", "red, blue", "red"],
                   "Red is bigger, but it is still one outcome. Blue and yellow are possible too. "
                   "The size of a part changes the chance, not the list of outcomes."))
    its.append(mcq("Which experiment has exactly 3 possible outcomes?", "spinning a red, blue and green spinner",
                   ["tossing a coin", "rolling a dice", "picking a day of the week"],
                   "The spinner can land on red, blue or green: 3 outcomes. A coin has 2, a dice has 6 and the days of the week are 7."))
    its.append(mcq("Ethan rolls a dice and tosses a coin. Which is a possible outcome?", "5 and heads",
                   ["7 and tails", "heads and tails", "0 and heads"],
                   "The dice gives a number from 1 to 6 and the coin gives heads or tails. 5 and heads can happen. "
                   "A coin cannot show heads and tails at once."))
    its.append(mcq("Mia picks a counter from a bag. The only possible outcomes are red and blue. Which bag could it be?",
                   "6 red and 2 blue", ["6 red", "2 blue", "6 red, 2 blue and 1 green"],
                   "The bag must have red and blue counters, and no other colour. Only 6 red and 2 blue works."))
    its.append(word_q("All 10 counters in a bag are green. Picking a green counter is …", "certain",
                      "Every counter is green, so you must pick green. It is certain."))
    its.append(mcq("You toss a 10c coin and a 20c coin. H means heads and T means tails. "
                   "Which list shows all the possible outcomes? (10c coin first)", "HH, HT, TH, TT",
                   ["HH, HT, TT", "HH, TT", "HT, TH"],
                   "Each coin can be H or T. HT (10c heads, 20c tails) and TH (10c tails, 20c heads) are different. "
                   "So there are 4 outcomes: HH, HT, TH, TT."))
    assert [n for n in range(1, 13) if n % 5 == 0] == [5, 10]
    its.append(mcq("Number cards 1 to 12 are face down. Kai picks one. Which outcomes are multiples of 5?", "5, 10",
                   ["5, 10, 15", "5", "10"],
                   "The multiples of 5 are 5, 10, 15 … Only 5 and 10 are on the cards. There is no 15 card."))
    assert len(its) == 20
    return {"title": "Possible outcomes: coins, dice, spinners and counters", "items": its}


# ------------------------------------------------------------ set 3: ordering outcomes by likelihood
def set_order(rnd):
    its = []
    its.append(mcq(fig(bag_svg([("red", 6), ("blue", 3), ("yellow", 1)], rnd)) +
                   "Put the colours in order from most likely to least likely.", "red, blue, yellow",
                   ["yellow, blue, red", "blue, red, yellow", "red, yellow, blue"],
                   "Count each colour: red 6, blue 3, yellow 1. The most counters is most likely: red, blue, yellow."))
    sec = eq("red", "blue", "red", "green", "red", "blue")
    assert amounts(sec) == {"red": 3, "blue": 2, "green": 1}
    its.append(mcq(fig(spinner_svg(sec)) + "Put the colours in order from least likely to most likely.", "green, blue, red",
                   ["red, blue, green", "green, red, blue", "blue, green, red"],
                   "Count the equal sections: green 1, blue 2, red 3. Least likely first: green, blue, red."))
    sec = [("red", 1), ("blue", 4), ("red", 1), ("yellow", 2)]
    assert amounts(sec) == {"red": 2, "blue": 4, "yellow": 2}
    its.append(mcq(fig(spinner_svg(sec)) + "Which colour is the arrow most likely to land on?", "blue",
                   ["red", "yellow", "They are all equally likely"],
                   "Look at the size of each part, not the number of pieces. Blue is half of the spinner. "
                   "Red has 2 pieces, but they are small: together a quarter."))
    its.append(mcq(fig(spinner_svg(sec)) + "Which two colours are equally likely?", "red and yellow",
                   ["red and blue", "blue and yellow", "all three colours"],
                   "Red is 2 small pieces that make a quarter. Yellow is one piece that is also a quarter. "
                   "Same size means equally likely."))
    sec = [("yellow", 5), ("green", 2), ("purple", 1)]
    its.append(mcq(fig(spinner_svg(sec)) + "Put the colours in order from most likely to least likely.", "yellow, green, purple",
                   ["purple, green, yellow", "green, yellow, purple", "yellow, purple, green"],
                   "Yellow covers the biggest part, then green, then purple. So yellow, green, purple."))
    assert len([n for n in range(1, 7) if n < 5]) == 4
    its.append(mcq("Aarav rolls a dice. Which is most likely?", "rolling a number less than 5",
                   ["rolling a 6", "rolling an even number", "rolling a 1 or a 2"],
                   "Count the faces. Less than 5: 1, 2, 3, 4 (4 faces). Even: 2, 4, 6 (3 faces). 1 or 2: 2 faces. A 6: 1 face. "
                   "4 faces is the most."))
    its.append(mcq("Grace rolls a dice. Put these in order from least likely to most likely.<br>"
                   "A: rolling a 6<br>B: rolling an odd number<br>C: rolling a number less than 6",
                   "A, B, C", ["C, B, A", "B, A, C", "A, C, B"],
                   "A: 1 face (6). B: 3 faces (1, 3, 5). C: 5 faces (1, 2, 3, 4, 5). Fewest faces first: A, B, C."))
    assert len([n for n in range(1, 11) if n % 2 == 0]) == 5 and len([n for n in range(1, 11) if n > 8]) == 2
    its.append(mcq("Number cards 1 to 10 are face down. Harper picks one. Which is most likely?", "an even number",
                   ["a number greater than 8", "the number 10", "a number greater than 10"],
                   "Even: 2, 4, 6, 8, 10 (5 cards). Greater than 8: 9, 10 (2 cards). The 10: 1 card. "
                   "Greater than 10: no cards, so impossible."))
    S = lambda spins: fig(spinners_abcd(spins))
    D = eq("red", "blue", "red", "blue", "red", "blue", "blue", "blue")
    assert amounts(D)["red"] == 3
    its.append(abcd_q(S([eq("red", "blue"), [("red", 1), ("blue", 3)], [("red", 3), ("blue", 1)], D]) +
                      "On which spinner is landing on red most likely?", "Spinner", 2,
                      "Compare how much of each spinner is red. C is three quarters red. A is half. "
                      "D has 3 red pieces, but they are small: less than half of the spinner."))
    its.append(abcd_q(S([[("blue", 1), ("yellow", 1)], [("blue", 1), ("yellow", 7)], [("blue", 1), ("yellow", 3)],
                         eq("blue", "yellow", "blue", "yellow", "blue", "yellow")]) +
                      "On which spinner is landing on blue least likely?", "Spinner", 1,
                      "Blue is only one small eighth of spinner B. On C blue is a quarter, and on A and D blue is half."))
    G = lambda bags: fig(bags_abcd(bags, rnd))
    its.append(abcd_q(G([[("green", 2), ("red", 4)], [("green", 3), ("red", 3)], [("green", 5), ("red", 1)],
                         [("green", 1), ("red", 5)]]) +
                      "From which bag is picking a green counter most likely?", "Bag", 2,
                      "Each bag has 6 counters. Bag C has the most green counters (5), so green is most likely there."))
    its.append(abcd_q(G([[("red", 6)], [("red", 1), ("blue", 5)], [("blue", 6)], [("red", 3), ("blue", 3)]]) +
                      "From which bag is picking red least likely, but still possible?", "Bag", 1,
                      "Bag B has only 1 red counter out of 6, so red is unlikely there. "
                      "Bag C has no red at all, so red is impossible, not just least likely."))
    its.append(mcq("Bag A has 3 red and 1 blue counter. Bag B has 3 red and 5 blue counters. "
                   "Noah wants a red counter. Which bag should he pick from?", "Bag A",
                   ["Bag B", "Both bags give the same chance", "Neither bag has red"],
                   "Both bags have 3 red counters. But in Bag A almost all the counters are red, "
                   "and in Bag B most are blue. Compare red with the other counters too."))
    its.append(mcq("Bag A has 2 red and 2 blue counters. Bag B has 6 red and 6 blue counters. "
                   "Which bag gives a better chance of red?", "Both bags give the same chance",
                   ["Bag B", "Bag A", "Neither bag has red"],
                   "In both bags half the counters are red. Bag B has more red counters, but it also has more blue ones. "
                   "So the chance is the same."))
    sec = [("3", 4), ("1", 2), ("2", 1), ("4", 1)]
    assert amounts(sec) == {"3": 4, "1": 2, "2": 1, "4": 1}
    its.append(mcq(fig(spinner_svg(sec)) + "Put 1, 2 and 3 in order from most likely to least likely.", "3, 1, 2",
                   ["1, 2, 3", "3, 2, 1", "2, 1, 3"],
                   "3 covers half the spinner, 1 covers a quarter and 2 covers an eighth. So 3, 1, 2. "
                   "The size of the number does not matter, only the size of its part."))
    its.append(mcq(fig(spinner_svg([("yellow", 1), ("green", 3)])) +
                   "Harper says yellow is more likely because it is at the top of the spinner. Which colour is more likely?",
                   "green", ["yellow", "They are equally likely", "You can’t tell"],
                   "Where a part is does not matter. Green covers three quarters of the spinner and yellow only a quarter, "
                   "so green is more likely."))
    its.append(mcq("A bag has 4 red, 4 blue and 2 yellow counters. Which sentence is true?", "Red and blue are equally likely",
                   ["Red is more likely than blue", "Yellow is impossible", "Yellow is most likely"],
                   "Red and blue have 4 counters each, so they are equally likely. Yellow has 2: it is least likely, but possible."))
    its.append(mcq("The canteen has a box of icy poles: 8 lemon, 15 orange and 2 lime. Cooper takes one without looking. "
                   "Put the flavours in order from least likely to most likely.", "lime, lemon, orange",
                   ["orange, lemon, lime", "lemon, lime, orange", "lime, orange, lemon"],
                   "Count each flavour: lime 2, lemon 8, orange 15. Least likely first: lime, lemon, orange."))
    its.append(mcq("Chloe colours a spinner with 6 equal sections. She wants blue to be less likely than red, "
                   "but more likely than green. Which colouring works?", "3 red, 2 blue, 1 green",
                   ["2 red, 3 blue, 1 green", "1 red, 2 blue, 3 green", "2 red, 2 blue, 2 green"],
                   "Blue must have fewer sections than red and more than green. 3 red, 2 blue, 1 green: 3 &gt; 2 &gt; 1."))
    its.append(mcq("At the athletics carnival, a lucky dip has 20 prizes: 12 pencils, 6 stickers and 2 medals. "
                   "Which sentence is true?", "A pencil is most likely and a medal is least likely",
                   ["A medal is most likely", "All the prizes are equally likely", "Getting a medal is impossible"],
                   "12 pencils is the most, so a pencil is most likely. 2 medals is the fewest, so a medal is least likely, "
                   "but still possible."))
    order = [0, 1, 4, 2, 3, 5, 6, 7, 8, 9, 10, 11, 15, 16, 12, 13, 14, 17, 18, 19]
    return {"title": "Ordering outcomes from most likely to least likely", "items": [its[i] for i in order]}


# ------------------------------------------------------------ set 4: independent events
def set_independent(rnd):
    its = []
    its.append(mcq("Isla tosses a coin and gets heads. Which list shows the possible outcomes of her next toss?",
                   "heads or tails", ["tails only", "heads only", "neither heads nor tails"],
                   "A coin does not change after a toss. The next toss can still be heads or tails."))
    its.append(mcq("A coin lands on heads 4 times in a row. On the next toss, tails is …", "just as likely as heads",
                   ["more likely than heads", "certain", "impossible"],
                   "A coin has no memory. Every toss, heads and tails are equally likely. Tails is not “due”."))
    its.append(mcq("Noah rolls a dice and gets a 6. Is a 6 on his next roll less likely now?",
                   "No, a 6 is just as likely as before",
                   ["Yes, you can’t roll a 6 twice in a row", "Yes, a 6 is now impossible", "No, a 6 is now more likely"],
                   "The dice does not remember the last roll. A 6 is still 1 of the 6 faces, the same as before."))
    its.append(mcq("Ava rolls a dice 5 times and gets 1, 3, 2, 5, 4. She has not rolled a 6 yet. "
                   "Rolling a 6 on her next roll is …", "unlikely, the same as on every roll",
                   ["certain, because a 6 is due", "likely, because a 6 is due", "impossible"],
                   "Earlier rolls do not change the next one. A 6 is 1 of 6 faces on every roll, so it is unlikely. "
                   "A 6 is never “due”."))
    its.append(mcq(fig(spinner_svg(eq("red", "blue"))) + "Kai spins red 3 times in a row. What about the next spin?",
                   "Red and blue are still equally likely",
                   ["Blue is now certain", "Blue is now more likely", "Red is now impossible"],
                   "The spinner is still half red and half blue. Past spins do not change it."))
    its.append(mcq("Grace rolls a 5 on a dice. Then she tosses a coin. Does the 5 change the chance of heads?",
                   "No, heads and tails are still equally likely",
                   ["Yes, heads is now more likely", "Yes, tails is now more likely", "Yes, heads is now impossible"],
                   "The dice and the coin do not affect each other. These are independent events."))
    its.append(mcq("Which two events do NOT affect each other?", "rolling a dice and tossing a coin",
                   ["it rains all morning and the oval is wet at lunch",
                    "eating a big lunch and feeling less hungry",
                    "practising times tables and getting faster at them"],
                   "The dice cannot change the coin, and the coin cannot change the dice. "
                   "In the other pairs, the first event changes the second."))
    its.append(mcq("Which two events DO affect each other?", "it rains all morning and the oval is wet at lunch",
                   ["Mia tosses heads, then Jack tosses heads", "a spinner lands on red, then a dice shows 4",
                    "rolling a 6, then tossing tails"],
                   "Rain makes the oval wet, so the first event changes the chance of the second. "
                   "Coins, dice and spinners do not affect each other."))
    bag = fig(bag_svg([("red", 2), ("blue", 2)], rnd))
    its.append(mcq(bag + "Jack picks a red counter and puts it back. Then he picks again. Which is true?",
                   "Red and blue are still equally likely",
                   ["Blue is now more likely", "Red is now more likely", "Red is now impossible"],
                   "He put the counter back, so the bag still has 2 red and 2 blue. Nothing has changed."))
    its.append(mcq(bag + "Jack picks a red counter and does NOT put it back. Which colour is now more likely?", "blue",
                   ["red", "They are still equally likely", "You can’t tell"],
                   "Now the bag has 1 red and 2 blue. Blue has more counters, so blue is more likely. "
                   "Keeping the counter changes the chance."))
    bag2 = fig(bag_svg([("red", 1), ("green", 4)], rnd))
    its.append(word_q(bag2 + "Sienna picks the red counter and keeps it. Now picking red is …", "impossible",
                      "There was only 1 red counter, and Sienna kept it. No red is left, so it is impossible."))
    its.append(word_q(bag2 + "Sienna picks the red counter and puts it back. Now picking red is …", "unlikely",
                      "The red counter is back in the bag: 1 red and 4 green, the same as before. Red is unlikely."))
    its.append(mcq("In which experiment does the first pick change the chance of the second pick?",
                   "picking a lolly from a bag, eating it, then picking again",
                   ["tossing a coin twice", "rolling a dice twice",
                    "picking a counter, putting it back, then picking again"],
                   "Once a lolly is eaten, the bag has one less lolly, so the chances change. "
                   "Coins and dice do not change, and a counter that is put back leaves the bag the same."))
    its.append(mcq("Liam has 5 number cards: 1, 2, 3, 4, 5. He picks the 3 and keeps it. "
                   "Which number is now impossible to pick?", "3", ["1", "5", "none of them"],
                   "The 3 card is no longer in the pile, so 3 is impossible. 1, 2, 4 and 5 can still be picked."))
    its.append(mcq("Mei says, “It rained yesterday, so I am less likely to roll a 6 today.” Is she right?",
                   "No, the rain does not change the dice",
                   ["Yes, a 6 is less likely", "Yes, a 6 is impossible on rainy days", "No, a 6 is now more likely"],
                   "The weather and a dice do not affect each other. A 6 is the same chance every day."))
    its.append(word_q("Kai’s class puts 26 names in a hat. The teacher picks Kai’s name and puts it back. "
                      "Picking Kai’s name again on the next pick is …", "unlikely",
                      "His name went back in, so it is still 1 of 26 names. It could be picked again, but it is unlikely."))
    its.append(mcq("At a sausage sizzle raffle, Oliver has only 1 ticket. His ticket is drawn first and is not put back. "
                   "Can he win the second prize?", "No, his only ticket has been drawn",
                   ["Yes, it is likely", "Yes, it is certain", "Yes, the same chance as before"],
                   "The second prize is drawn from the tickets that are left. Oliver has no tickets left in, "
                   "so winning the second prize is impossible."))
    its.append(mcq("Jack’s footy team has won the coin toss 5 weeks in a row. Next week the captain calls heads again. "
                   "Which is true?", "Winning and losing the toss are equally likely",
                   ["They will surely lose this time", "They will surely win again", "Winning the toss is impossible"],
                   "Each toss is new. The coin does not know about the last 5 weeks, so it is still an even chance."))
    its.append(mcq("Ruby spins a red and blue spinner and a spinner with 4 equal sections numbered 1 to 4. "
                   "The colour spinner lands on red. Which number is most likely on the number spinner?",
                   "All four numbers are equally likely", ["1", "4", "2"],
                   "The colour spinner does not affect the number spinner. The 4 equal sections make each number equally likely."))
    its.append(mcq("A bag has 3 red and 3 blue counters. Kai takes out 2 blue counters and keeps them. Which is now true?",
                   "Red is more likely than blue",
                   ["Red and blue are still equally likely", "Blue is more likely than red", "Blue is impossible"],
                   "Now the bag has 3 red and 1 blue. Red has more counters, so red is more likely. "
                   "Blue is still possible, because 1 blue counter is left."))
    assert len(its) == 20
    return {"title": "Independent events: does one result change the next?", "items": its}


# ------------------------------------------------------------ set 5: repeated experiments and word problems
def set_experiments(rnd):
    its = []
    mia = [14, 10, 6]
    assert sum(mia) == 30
    tf = fig(tally_svg("Mia’s 30 spins", "Colour", ["Red", "Blue", "Yellow"], mia, label="tally chart: spins by Mia"))
    its.append(mcq(tf + "Which colour came up most often?", "red", ["yellow", "blue", "They all came up the same"],
                   "Red: 2 groups of 5 and 4 more = 14. Blue: 10. Yellow: 6. Red has the most tally marks."))
    its.append(mcq(tf + "How many times did Mia spin altogether?", "30 times", ["3 times", "24 times", "14 times"],
                   "Add the tallies: 14 + 10 + 6 = 30."))
    its.append(mcq(tf + "How many more times did red come up than yellow?", "8 times", ["20 times", "4 times", "6 times"],
                   "Red 14, yellow 6. How many more means subtract: 14 − 6 = 8."))
    its.append(mcq(tf + "Mia’s spinner has 6 equal sections. Which spinner did she most likely use?",
                   "3 red, 2 blue, 1 yellow",
                   ["1 red, 2 blue, 3 yellow", "2 red, 2 blue, 2 yellow", "3 red, 3 blue, 0 yellow"],
                   "Red came up most, then blue, then yellow, so red should have the most sections and yellow the fewest. "
                   "It cannot have 0 yellow, because yellow came up 6 times."))
    roll = [9, 11, 8, 10, 12, 10]
    assert sum(roll) == 60 and roll.index(max(roll)) == 4
    assert roll[1] + roll[3] + roll[5] == 31 and roll[0] + roll[2] + roll[4] == 29
    tb = fig(table_svg("Cooper’s 60 dice rolls", ["Number", "1", "2", "3", "4", "5", "6"], [["Times"] + [str(v) for v in roll]],
                       label="table: dice rolls by Cooper"))
    its.append(mcq(tb + "Which number did Cooper roll most often?", "5", ["6", "3", "2"],
                   "The biggest number in the Times row is 12, under the number 5. "
                   "(6 is the biggest number on the dice, not the one rolled most.)"))
    its.append(mcq(tb + "Cooper says 5 is the easiest number to roll, because it came up most. Is he right?",
                   "No, each number is equally likely",
                   ["Yes, 5 will come up most every time", "No, 6 is the easiest to roll", "No, 3 is the easiest to roll"],
                   "Each face of a dice has the same chance. Results vary: next time a different number may come up most."))
    its.append(mcq(tb + "How many times did Cooper roll an even number?", "31 times", ["30 times", "29 times", "3 times"],
                   "Even numbers: 2, 4 and 6. Add their results: 11 + 10 + 10 = 31. (29 is the odd numbers.)"))
    its.append(mcq("Charlotte tosses a coin 20 times and gets 12 heads and 8 tails. She tosses it 20 more times. What will happen?",
                   "The results will probably be a little different",
                   ["She will get 12 heads again", "She will get 12 tails and 8 heads", "She will get exactly 10 heads"],
                   "Chance results vary each time. She might get 9 heads, or 11, or 12. We cannot know for sure."))
    its.append(mcq(fig(spinner_svg(eq("red", "blue"))) + "Jack spins this spinner 40 times. Which result would be most surprising?",
                   "red 40, blue 0", ["red 20, blue 20", "red 22, blue 18", "red 17, blue 23"],
                   "Half the spinner is red and half is blue, so you expect about 20 of each. Results near 20 are normal. "
                   "Red every single time is possible, but very unlikely."))
    its.append(mcq(fig(spinner_svg([("blue", 3), ("red", 1)])) + "William spins this spinner 40 times. Which result is most likely?",
                   "blue 30, red 10", ["blue 10, red 30", "blue 20, red 20", "blue 40, red 0"],
                   "Blue is three quarters of the spinner, so blue should come up about 3 times as often as red. "
                   "Blue 30 and red 10 fits best."))
    its.append(mcq("Matilda picks a counter from a bag, writes the colour and puts it back. She does this 20 times. "
                   "She gets red 15 times and green 5 times. Which bag did she most likely use?", "6 red, 2 green",
                   ["2 red, 6 green", "4 red, 4 green", "8 red, 0 green"],
                   "Red came up about 3 times as often as green, so the bag probably has many more red counters. "
                   "It cannot be 8 red and 0 green, because she picked green 5 times."))
    ava = [9, 11]
    tg = fig(tally_svg("Ava’s 20 coin tosses", "Outcome", ["Heads", "Tails"], ava, label="tally chart: coin tosses by Ava"))
    its.append(mcq(tg + "Ava says tails is more likely, because it came up more. Is she right?",
                   "No, heads and tails are equally likely",
                   ["Yes, tails is more likely", "No, heads is more likely", "Yes, tails will win next time too"],
                   "9 and 11 are close. A coin has an even chance of heads or tails; results just vary a little each time."))
    heads = [13, 8, 11]
    assert sum(heads) == 32 and 60 - 32 == 28
    its.append(mcq("Three groups in Year 4 each toss a coin 20 times. They get 13, 8 and 11 heads. "
                   "How many heads did the class get altogether?", "32", ["60", "28", "30"],
                   "Add the heads: 13 + 8 + 11 = 32. (60 is all the tosses, and 30 is half of them.)"))
    its.append(mcq("Three groups toss a coin 20 times each: 60 tosses. They get 32 heads altogether. "
                   "How many tails did they get?", "28", ["32", "30", "92"],
                   "Every toss is heads or tails: 60 − 32 = 28 tails."))
    its.append(mcq("Ethan wants to find out if a spinner is fair. Which gives a better idea?", "100 spins",
                   ["5 spins", "Both are just as good", "Neither tells you anything"],
                   "With only a few spins, luck can change the results a lot. Many spins give a much better idea."))
    rb = [22, 18]
    tr = fig(tally_svg("Ruby’s 40 spins", "Colour", ["Green", "Purple"], rb, label="tally chart: spins by Ruby"))
    its.append(mcq(tr + "Ruby’s spinner is half green and half purple. Are her results surprising?",
                   "No, they are close to half each",
                   ["Yes, the spinner must be broken", "Yes, they should be exactly 20 and 20", "Yes, green must be more likely"],
                   "With a half-and-half spinner you expect about 20 of each, but rarely exactly 20. 22 and 18 are close."))
    assert 24 - 4 == 20
    its.append(mcq("Liam rolls a dice 24 times. He gets a 6 four times. How many rolls were not a 6?", "20",
                   ["28", "4", "24"],
                   "Not a 6 means all the other rolls: 24 − 4 = 20."))
    assert 20 - 7 - 6 == 7
    its.append(mcq("Zara spins a spinner 20 times. She gets red 7 times, blue 6 times and yellow the rest. "
                   "How many times did she get yellow?", "7 times", ["13 times", "33 times", "14 times"],
                   "Step 1: red and blue: 7 + 6 = 13. Step 2: 20 − 13 = 7 times yellow."))
    its.append(word_q("A raffle at the school fete sells 150 tickets. Matilda buys 3 of them. Matilda winning is …", "unlikely",
                      "Matilda has only 3 of the 150 tickets. She could win, but it is unlikely."))
    its.append(word_q("Kai rolls a dice 12 times and never gets a 6. Getting a 6 on his next roll is …", "unlikely",
                      "The dice has no memory. A 6 is 1 of the 6 faces, the same as every roll, so it is unlikely. "
                      "It is not likely or certain just because it has not come up."))
    assert len(its) == 20
    return {"title": "Repeated experiments, tallies and word problems", "items": its}


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
        "<h2>Chance words: from impossible to certain</h2>"
        "<p>Chance is how likely something is to happen. <b>Impossible</b> means it can never happen. "
        "<b>Certain</b> means it must happen. <b>Unlikely</b> means it could happen, but probably will not. "
        "<b>Likely</b> means it will probably happen. Put events on a line from impossible to certain to order them.</p>"
        "<figure class='sn-fig'>" + scale_svg() +
        "<figcaption>From impossible to certain. Even chance (equally likely) is in the middle.</figcaption></figure>" +
        ex("Example", "Order these from least likely to most likely: a dog will read a book; the sun will rise tomorrow; "
           "a koala will visit your classroom.",
           "A dog reading is impossible. A koala visiting is unlikely. The sun rising is certain.",
           "dog, koala, sun") +
        "<h2>Possible outcomes</h2>"
        "<p>An <b>outcome</b> is something that can happen in a chance experiment. A coin has 2 outcomes: heads or tails. "
        "A dice has 6: 1, 2, 3, 4, 5 or 6. List each outcome once.</p>"
        "<figure class='sn-fig'>" + dice_faces_svg() +
        "<figcaption>The 6 outcomes of a dice. Each face is equally likely.</figcaption></figure>"
        "<h2>Order outcomes by how likely they are</h2>"
        "<p>On a spinner, the colour that covers the <b>biggest part</b> is most likely. Look at the size of each part, "
        "not the number of pieces. In a bag, the colour with the <b>most counters</b> is most likely.</p>"
        "<figure class='sn-fig'>" + spinner_svg([("yellow", 5), ("green", 2), ("purple", 1)],
                                                  "spinner: yellow 5 eighths, green 2 eighths, purple 1 eighth") +
        "<figcaption>Yellow covers the most, then green, then purple.</figcaption></figure>" +
        ex("Example", "Order the colours from most likely to least likely.",
           "Compare the parts: yellow is biggest, purple is smallest.", "yellow, green, purple") +
        "<h2>Independent events: a coin has no memory</h2>"
        "<p>Two events are <b>independent</b> when one does not change the chance of the other. "
        "Tossing a coin and rolling a dice are independent. A coin also does not remember earlier tosses: "
        "after 4 heads, tails is still an even chance.</p>" +
        table(["What happens", "Does the chance change?"], [
            ["Toss a coin, then toss it again", "No. Heads and tails stay equally likely."],
            ["Roll a dice, then toss a coin", "No. The dice cannot change the coin."],
            ["Pick a counter and put it back", "No. The bag is the same as before."],
            ["Pick a counter and keep it", "Yes. The bag now has one less counter."],
        ]) +
        "<h2>Repeated experiments</h2>"
        "<p>Do an experiment many times and keep a tally. The results <b>vary</b>: if you do it again, "
        "you will probably get different numbers. More tries give a better idea of the real chances.</p>"
        "<figure class='sn-fig'>" + tally_svg("20 coin tosses", "Outcome", ["Heads", "Tails"], [11, 9],
                                              label="tally chart: 20 coin tosses") +
        "<figcaption>11 heads and 9 tails. Close to half each, but not exactly. That is normal.</figcaption></figure>"
        "<h2>Common mistakes</h2>" +
        table(["Mistake", "What to do instead"], [
            ["“5 heads in a row, so tails is due.”", "A coin has no memory. Heads and tails stay equally likely."],
            ["Counting pieces of a spinner, not their size", "Compare how much of the spinner each colour covers."],
            ["Saying certain when it is only likely", "Certain means it must happen. If it might not, say likely."],
            ["Saying impossible when it is only unlikely", "If it could happen even once, it is not impossible."],
            ["Expecting the same results every time", "Results vary each time you repeat an experiment."],
        ])
    )


FAQ = [
    {"q": "What do Year 4 students learn about chance in the Australian Curriculum?",
     "a": "In Year 4 (AC9M4P01 and AC9M4P02) students describe possible outcomes, order events and outcomes from least to most likely, identify independent events, and run repeated chance experiments to see how results vary."},
    {"q": "What is the difference between likely and certain?",
     "a": "Certain means it must happen, like rolling a number from 1 to 6 on a dice. Likely means it will probably happen but might not, like picking red from a bag of 9 red and 1 blue counter."},
    {"q": "What are independent events in Year 4 maths?",
     "a": "Independent events do not change each other’s chances. Tossing a coin and rolling a dice are independent, and so is picking a counter if you put it back before the next pick."},
    {"q": "If a coin lands on heads 5 times in a row, is tails more likely next?",
     "a": "No. A coin has no memory, so heads and tails are still equally likely on the next toss. Thinking tails is “due” is a common mistake called the gambler’s fallacy."},
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
    rnd = random.Random(4820)
    sets = [set_words(rnd), set_outcomes(rnd), set_order(rnd), set_independent(rnd), set_experiments(rnd)]
    balance(sets, rnd)
    seen = set()
    for s in sets:
        assert len(s["items"]) == 20, (s["title"], len(s["items"]))
        for it in s["items"]:
            assert len(set(it["c"])) == 4, it
            assert it["e"], it
            assert it["q"].count("<svg") <= 1, it["q"]
            k = re.sub(r"<[^>]+>", "", it["q"]) + "|" + "|".join(sorted(it["c"]))
            assert k not in seen, it["q"]
            seen.add(k)
    return {
        "country": "au", "subject": "maths", "grade": "year-4", "slug": "chance", "sort": 20,
        "updated": UPDATED, "pdf_url": "",
        "title": "Chance: Ordering Events, Outcomes and Independent Events",
        "seo_title": "Year 4 Chance Worksheets: Likely, Unlikely, Outcomes and Experiments (Free, with Answers)",
        "short_title": "Chance",
        "domain": "Probability",
        "standard_code": "AC9M4P01",
        "standard_url": "https://v9.australiancurriculum.edu.au/f-10-curriculum/learning-areas/mathematics",
        "standard_text": "Describe possible everyday events and the possible outcomes of chance experiments and order outcomes or events based on their likelihood of occurring; identify events where the chance of one occurring will not be affected by the occurrence of the other",
        "meta_desc": "Free Year 4 maths worksheets on chance: order events from impossible to certain, list the outcomes of coins, dice, spinners and bags of counters, order outcomes by likelihood, spot independent events and read the results of repeated chance experiments. 100 questions with an answer key, aligned to the Australian Curriculum (AC9M4P01, AC9M4P02).",
        "key_big": "The outcome that covers the biggest part of the spinner or bag is the most likely.",
        "key_sub": "Order events from impossible to certain. A coin or dice has no memory: after 4 heads, tails is still an even chance. Likely is not certain, and results vary each time you repeat an experiment.",
        "body_html": body_html(rnd), "faq": FAQ, "sets": sets,
    }


def mark_large(u, pattern):
    """Tag pictures that must print larger (A to D panels, chance scales, tables, tally charts)."""
    rx = re.compile(r"<svg (?=[^>]*aria-label='" + pattern + ")")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u


if __name__ == "__main__":
    u = gen_unit()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    mark_large(u, "(spinners A to D|bags A to D|chance scale with points|tally chart|table)")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
