# -*- coding: utf-8 -*-
"""
Canada (British Columbia) Grade 3 Math: Likelihood of simulated events
(BC Mathematics Curriculum, Grade 3, Data and probability: likelihood of simulated events, using comparative language)
  python3 tools/gen_cabc_math_g3_likelihood.py
Likelihood words (impossible, unlikely, equally likely, likely, certain; more likely / less likely), spinners and bags
(the size of each part), tally results from coin and spinner simulations, predictions compared with results, and fair games.
Word questions show 4 of the 5 words in scale order (one word that is not the answer is left out).
Wrong answers come from real student mistakes: counting sections instead of their size, likely confused with certain,
unlikely confused with impossible, expecting results to match a prediction exactly, favourite colours and "it is due" thinking.
Every picture shows the colour as a letter too (R = red ...), so it still works when printed in black and white.
HTML attributes use single quotes (no backslashes in the JSON). Canadian English.
"""
import json, re, math, os, random

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "ca-bc", "math", "grade-3")
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
WORDS5 = ["impossible", "unlikely", "equally likely", "likely", "certain"]


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


def word_q(q, word, e, keep=()):
    """4 of the 5 probability words in scale order. Which word is left out is chosen in balance()."""
    assert word in WORDS5 and word not in keep
    return {"q": q, "e": e, "_word": word, "_keep": tuple(keep)}


def abcd_q(q, kind, ai, e):
    return mcq_fixed(q, ["%s %s" % (kind, L) for L in "ABCD"], ai, e)


def chance_word(k, n):
    """Word for an event that happens in k of n equal parts (compared with its complement)."""
    assert 0 <= k <= n
    if k == 0:
        return "impossible"
    if k == n:
        return "certain"
    if 2 * k == n:
        return "equally likely"
    return "likely" if 2 * k > n else "unlikely"


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


# ------------------------------------------------------------ set 1: likelihood words
def set_words(rnd):
    its = []
    its.append(word_q("Today is Tuesday. Tomorrow will be Wednesday. How likely is this?", "certain",
                      "The days of the week always come in the same order. Wednesday always comes after Tuesday, so it is certain."))
    its.append(word_q("Jasleen is 8 years old. On her next birthday, she will turn 9. How likely is this?", "certain",
                      "Everyone gets one year older on their birthday. 8 + 1 = 9, so it is certain."))
    its.append(word_q("Simran lets go of a soccer ball. It will fall to the ground. How likely is this?", "certain",
                      "A ball you let go of always falls. It must happen, so it is certain."))
    its.append(word_q("An orca will walk down the street in Victoria. How likely is this?", "impossible",
                      "Orcas live in the ocean and cannot walk. This can never happen, so it is impossible."))
    its.append(word_q("Next month will have 40 days. How likely is this?", "impossible",
                      "A month has 28, 29, 30 or 31 days. It can never have 40 days, so it is impossible."))
    its.append(word_q(fig(cube_faces_svg()) + "Owen rolls a number cube. He will roll a 7. How likely is this?", "impossible",
                      "The faces show 1, 2, 3, 4, 5 and 6. There is no 7, so rolling a 7 is impossible."))
    its.append(word_q("It will rain at least once in Vancouver in November. How likely is this?", "likely",
                      "Vancouver gets a lot of rain in November, so it is likely. We cannot be sure, "
                      "so it is likely, not certain.", keep=("certain",)))
    its.append(word_q("There will be snow on the ski hills at Whistler in January. How likely is this?", "likely",
                      "Whistler’s ski hills almost always have snow in January. But we cannot be sure, "
                      "so it is likely, not certain.", keep=("certain",)))
    its.append(word_q("The next car that drives past the school will have 4 wheels. How likely is this?", "likely",
                      "Most vehicles on the road have 4 wheels. But the next one could be a motorcycle or a big truck, "
                      "so it is likely, not certain."))
    its.append(word_q("Emma will find a $20 bill on the sidewalk on the way to school. How likely is this?", "unlikely",
                      "It could happen, but it almost never does. So it is unlikely. It is not impossible: people do drop money.",
                      keep=("impossible",)))
    its.append(word_q("A black bear will walk onto the school field in Kamloops today. How likely is this?", "unlikely",
                      "Bears do live near Kamloops, so it could happen. But it hardly ever does. "
                      "So it is unlikely, not impossible.", keep=("impossible",)))
    its.append(word_q("Lucas’s hockey team will score 20 goals in one game. How likely is this?", "unlikely",
                      "Hockey teams usually score only a few goals in a game. 20 goals could happen, but it is unlikely."))
    its.append(word_q("Hana tosses a coin. It will land on heads. How likely is this?", "equally likely",
                      "A coin has 2 sides: heads and tails. Heads and tails have the same chance, so it is equally likely."))
    its.append(word_q("Mateo hides a loonie in one of his two closed hands. Sofia picks a hand. "
                      "She will pick the hand with the loonie. How likely is this?", "equally likely",
                      "There are 2 hands and the loonie is in 1 of them. The loonie hand and the empty hand "
                      "have the same chance, so it is equally likely."))
    its.append(word_q("Kai says, “It is certain that it will rain in Vancouver tomorrow, because it rains there a lot.” "
                      "Which word should he use instead?", "likely",
                      "Rain in Vancouver happens often, but some days are dry. It could fail to happen, "
                      "so it is likely, not certain.", keep=("certain",)))
    its.append(word_q("Zara’s bag has 9 green counters and 1 yellow counter. She says, “Picking the yellow counter is impossible.” "
                      "Which word should she use instead?", "unlikely",
                      "There is 1 yellow counter, so it could be picked. It is possible, but not very likely. "
                      "The right word is unlikely, not impossible.", keep=("impossible",)))
    its.append(mcq("Which is more likely in Vancouver?", "rain in November",
                   ["snow in July", "they are equally likely", "both are impossible"],
                   "November is a very rainy month in Vancouver. July is summer, and snow then is almost impossible. "
                   "So rain in November is more likely."))
    its.append(mcq("Which event is certain?", "Next Saturday will come after Friday",
                   ["It will be sunny in Kelowna tomorrow", "Ryan will see an eagle today", "Ava will win the class draw"],
                   "Saturday always comes after Friday, so it must happen. The other events might happen, or might not."))
    its.append(mcq("Leah tosses a coin. Compare landing on heads and landing on tails.",
                   "they are equally likely", ["heads is more likely", "tails is more likely", "heads is certain"],
                   "A coin has one heads side and one tails side. They have the same chance, so they are equally likely."))
    its.append(mcq(fig(cube_faces_svg()) + "Which is less likely: rolling a number from 1 to 6, or rolling a 6?",
                   "rolling a 6", ["rolling a number from 1 to 6", "they are equally likely", "both are impossible"],
                   "Every roll is a number from 1 to 6, so that is certain. A 6 is only 1 of the 6 faces, "
                   "so rolling a 6 is less likely."))
    assert len(its) == 20
    return {"title": "Likelihood words: impossible, unlikely, likely, certain", "items": its}


# ------------------------------------------------------------ set 2: spinners and bags
def set_parts(rnd):
    its = []
    F = lambda sec: fig(spinner_svg(sec))
    B = lambda counts: fig(bag_svg(counts, rnd))
    S = lambda spins: fig(spinners_abcd(spins))
    G = lambda bags: fig(bags_abcd(bags, rnd))
    its.append(mcq(F(eq("blue", "blue", "green", "blue")) + "The spinner has 4 equal sections. "
                   "Which colour is the arrow most likely to land on?",
                   "blue", ["green", "equally likely", "red"],
                   "3 of the 4 equal sections are blue and only 1 is green, so blue is most likely."))
    sec = [("red", 1), ("yellow", 3)]
    its.append(mcq(F(sec) + "Landing on yellow is ___ than landing on red.", "more likely",
                   ["less likely", "equally likely", "certain"],
                   "Yellow covers 3 quarters of the spinner. Red covers only 1 quarter. "
                   "Yellow has the bigger part, so it is more likely."))
    sec = [("green", 2), ("blue", 1), ("red", 1)]
    assert amounts(sec) == {"green": 2, "blue": 1, "red": 1}
    its.append(mcq(F(sec) + "Which two colours are equally likely?", "blue and red",
                   ["green and blue", "green and red", "all three colours"],
                   "Green covers half of the spinner. Blue and red each cover a quarter. "
                   "Blue and red have parts of the same size, so they are equally likely."))
    sec = [("red", 6), ("blue", 1), ("green", 3), ("blue", 1), ("blue", 1)]
    assert amounts(sec) == {"red": 6, "blue": 3, "green": 3}
    its.append(mcq(F(sec) + "Ryan says blue is most likely, because blue has the most sections. "
                   "Which colour is most likely?", "red",
                   ["blue", "green", "all equally likely"],
                   "Ryan counted sections, not their size. The one red section is half of the spinner. "
                   "The 3 small blue sections together make only a quarter. Red is most likely."))
    its.append(word_q(F(eq("green", "green", "green", "green", "green", "green")) + "Landing on green is …", "certain",
                      "Every section is green. The arrow must land on green, so it is certain."))
    sec = eq("yellow", "yellow", "yellow", "purple", "yellow", "yellow", "yellow", "yellow")
    assert chance_word(amounts(sec)["yellow"], 8) == "likely"
    its.append(word_q(F(sec) + "Landing on yellow is …", "likely",
                      "7 of the 8 equal sections are yellow, so yellow is likely. "
                      "It is not certain, because there is 1 purple section.", keep=("certain",)))
    its.append(word_q(B([("red", 5), ("blue", 3)]) + "Picking a green counter from this bag is …", "impossible",
                      "There are only red and blue counters. There is no green counter, so it is impossible."))
    assert chance_word(1, 10) == "unlikely"
    its.append(word_q(B([("yellow", 1), ("green", 9)]) + "Picking a yellow counter from this bag is …", "unlikely",
                      "Only 1 of the 10 counters is yellow. It can happen, but not often, so it is unlikely, not impossible.",
                      keep=("impossible",)))
    its.append(mcq(B([("red", 4), ("blue", 4)]) + "Compare picking red and picking blue.", "they are equally likely",
                   ["red is more likely", "blue is more likely", "red is certain"],
                   "There are 4 red and 4 blue counters. The same number of each means they are equally likely."))
    its.append(mcq(B([("blue", 2), ("red", 6)]) + "Picking a blue counter is ___ than picking a red counter.", "less likely",
                   ["more likely", "equally likely", "impossible"],
                   "There are only 2 blue counters and 6 red counters. Fewer counters means less likely. "
                   "It is not impossible, because there are blue counters in the bag."))
    its.append(mcq(B([("green", 4), ("yellow", 3), ("red", 1)]) + "Put the colours in order from most likely to least likely.",
                   "green, yellow, red", ["red, yellow, green", "yellow, green, red", "green, red, yellow"],
                   "Count each colour: green 4, yellow 3, red 1. The most counters is most likely: green, yellow, red."))
    A = [("blue", 1), ("red", 1), ("blue", 1), ("red", 1), ("blue", 1), ("red", 3)]
    assert amounts(A)["blue"] == 3 and sum(u for _, u in A) == 8
    its.append(abcd_q(S([A, eq("blue", "red", "red", "red"), eq("blue", "red", "blue", "red"), [("blue", 3), ("red", 1)]]) +
                      "On which spinner is landing on blue most likely?", "Spinner", 3,
                      "Compare how much of each spinner is blue. D is three quarters blue. "
                      "A has 3 blue sections, but they are small: together they are less than half of the spinner."))
    its.append(abcd_q(S([eq("yellow", "green", "green", "green"), eq("red", "green", "blue", "green"),
                         eq("yellow", "yellow", "yellow", "yellow"), eq("yellow", "red", "yellow", "red")]) +
                      "On which spinner is landing on yellow impossible?", "Spinner", 1,
                      "Spinner B has no yellow section, so yellow is impossible there. "
                      "Spinner A has 1 yellow section: yellow is unlikely there, but not impossible."))
    its.append(abcd_q(G([[("red", 5), ("blue", 1)], [("red", 3), ("yellow", 3)], [("red", 6)], [("blue", 6)]]) +
                      "From which bag is picking a red counter certain?", "Bag", 2,
                      "Bag C has only red counters, so red is certain. "
                      "Bag A is likely to give red, but not certain, because it has 1 blue counter."))
    its.append(abcd_q(G([[("blue", 3), ("green", 3)], [("blue", 4), ("green", 2)], [("blue", 1), ("green", 5)], [("green", 6)]]) +
                      "From which bag are blue and green equally likely?", "Bag", 0,
                      "Bag A has 3 blue and 3 green counters. The same number of each colour means they are equally likely."))
    its.append(mcq("Noah colours a spinner with 4 equal sections. He wants red to be likely, but not certain. "
                   "How many sections should he colour red?", "3 sections",
                   ["4 sections", "1 section", "2 sections"],
                   "3 red sections out of 4 makes red likely. 4 red sections would make red certain. "
                   "2 would make red equally likely, and 1 would make it unlikely."))
    its.append(mcq("Leah’s spinner has 6 equal sections: 3 blue and 3 yellow. Which sentence is true?",
                   "Blue and yellow are equally likely",
                   ["Blue is more likely", "Yellow is less likely", "Landing on blue is certain"],
                   "3 blue and 3 yellow sections of the same size cover the same amount, so blue and yellow are equally likely."))
    sec = eq("red", "blue", "blue", "blue", "red", "blue", "blue", "blue")
    assert amounts(sec) == {"red": 2, "blue": 6}
    its.append(mcq(F(sec) + "Sofia thinks the arrow will land on red, because red is her favourite colour. "
                   "Which colour is the arrow more likely to land on?", "blue",
                   ["red", "equally likely", "always red"],
                   "A favourite colour does not change the chance. 6 of the 8 equal sections are blue and only 2 are red, "
                   "so blue is more likely."))
    assert 2 + 4 > 5
    its.append(mcq(B([("red", 5), ("yellow", 2)]) + "Arjun puts 4 more yellow counters into the bag. "
                   "Which colour is now more likely to be picked?", "yellow",
                   ["red", "equally likely", "yellow is impossible"],
                   "Yellow: 2 + 4 = 6 counters. Red: 5 counters. 6 is more than 5, so yellow is now more likely."))
    assert 3 + 4 == 7
    its.append(mcq(B([("red", 3), ("blue", 7)]) + "How many red counters must Chloe add to make red and blue equally likely?",
                   "4", ["7", "10", "3"],
                   "Red and blue are equally likely when there are the same number of each. Blue has 7. "
                   "Red has 3, so add 7 − 3 = 4 red counters."))
    assert len(its) == 20
    return {"title": "Spinners and bags: the size of each part", "items": its}


# ------------------------------------------------------------ set 3: experiments with tally results
def set_tally(rnd):
    its = []
    T = lambda title, head, cats, vals, lab: fig(tally_svg(title, head, cats, vals, label="tally chart: " + lab))
    j = [11, 9]
    assert sum(j) == 20
    tj = T("Jasleen’s 20 coin tosses", "Side", ["Heads", "Tails"], j, "Jasleen's coin tosses")
    its.append(mcq(tj + "How many times did the coin land on heads?", "11 times", ["10 times", "9 times", "3 times"],
                   "Count the tally marks: 2 groups of 5 is 10, and 1 more makes 11."))
    its.append(mcq(tj + "Heads came up 2 more times than tails. Is heads more likely on a coin?",
                   "No, heads and tails are equally likely", ["Yes, heads is more likely", "Yes, heads is certain",
                                                              "No, tails is more likely"],
                   "A coin has one heads side and one tails side, so they are equally likely. "
                   "Results are a little different each time, so 11 and 9 is a normal result."))
    w = [13, 7, 4]
    assert sum(w) == 24
    tw_ = T("Wei’s 24 spins", "Colour", ["Red", "Blue", "Yellow"], w, "Wei's spins")
    its.append(mcq(tw_ + "Which colour came up least often?", "yellow", ["red", "blue", "they all came up the same"],
                   "Red: 13. Blue: 7. Yellow: 4. Yellow has the fewest tally marks."))
    its.append(mcq(tw_ + "How many more times did red come up than blue?", "6 times", ["20 times", "7 times", "9 times"],
                   "Red 13, blue 7. How many more means subtract: 13 − 7 = 6."))
    its.append(mcq(tw_ + "How many spins were not red?", "11 spins", ["13 spins", "24 spins", "7 spins"],
                   "Not red means blue or yellow: 7 + 4 = 11. You can also do 24 − 13 = 11."))
    its.append(mcq(tw_ + "From these results, which colour probably covers the biggest part of Wei’s spinner?", "red",
                   ["yellow", "blue", "all the parts are the same size"],
                   "Red came up far more often than the other colours. The colour with the biggest part comes up most often, "
                   "so red probably covers the biggest part."))
    roll = [3, 2, 4, 3, 2, 4]
    assert sum(roll) == 18
    tb = fig(table_svg("Kai’s 18 rolls", ["Number", "1", "2", "3", "4", "5", "6"], [["Times"] + [str(r) for r in roll]],
                       label="table: Kai's number cube rolls"))
    its.append(mcq(tb + "Kai rolled a number cube 18 times. How many times did he roll a 3?", "4 times",
                   ["3 times", "18 times", "2 times"],
                   "Find 3 in the Number row. The number under it in the Times row is 4."))
    assert roll[4] + roll[5] == 6
    its.append(mcq(tb + "How many times did Kai roll a number greater than 4?", "6 times",
                   ["9 times", "4 times", "18 times"],
                   "Greater than 4 means 5 or 6 (not 4 itself). 5 came up 2 times and 6 came up 4 times: 2 + 4 = 6."))
    g = [12, 8]
    tg = T("Penalty kick simulation", "Toss", ["Heads: goal", "Tails: miss"], g, "penalty kick simulation")
    its.append(mcq(tg + "Mr. Singh’s class simulates soccer penalty kicks with a coin. Heads means a goal and tails means a miss. "
                   "How many goals did the simulation show?", "12 goals", ["8 goals", "20 goals", "2 goals"],
                   "Heads stands for a goal. Heads has 2 groups of 5 and 2 more: 12 goals."))
    its.append(mcq(tg + "How many kicks did the class simulate altogether?", "20 kicks", ["12 kicks", "4 kicks", "2 kicks"],
                   "Each toss is one kick. Add the tallies: 12 + 8 = 20."))
    its.append(mcq(tg + "In this simulation, what does landing on tails stand for?", "a missed kick",
                   ["a goal", "a tie game", "a new player"],
                   "In a simulation, each outcome stands for something real. Here, tails stands for a miss."))
    a = [7, 7, 6]
    assert sum(a) == 20
    ta = T("Ava’s 20 spins", "Colour", ["Red", "Blue", "Green"], a, "Ava's spins")
    its.append(mcq(ta + "Which two colours came up the same number of times?", "red and blue",
                   ["blue and green", "red and green", "none of them"],
                   "Red: 7. Blue: 7. Green: 6. Red and blue both came up 7 times."))
    o = [15, 10]
    to = T("Owen’s 25 picks", "Colour", ["Green", "Purple"], o, "Owen's picks")
    its.append(mcq(to + "Owen picks a counter, writes the colour and puts it back. How many more times did he get green than purple?",
                   "5 times", ["25 times", "10 times", "15 times"],
                   "Green 15, purple 10. 15 − 10 = 5."))
    its.append(mcq(to + "What do the results tell you about Owen’s bag?", "It probably has more green counters",
                   ["It must have only green counters", "It has more purple counters", "It has no purple counters"],
                   "Green came up more often, so there are probably more green counters. "
                   "It cannot be only green, because purple came up 10 times."))
    its.append(mcq("Lucas spins a spinner 20 times. Yellow never comes up. Is landing on yellow impossible?",
                   "Not sure: yellow may just be unlikely",
                   ["Yes, it must be impossible", "No, yellow is likely", "No, yellow is certain"],
                   "If the spinner has a small yellow part, yellow is unlikely and might not come up in 20 spins. "
                   "Look at the spinner: it is impossible only if there is no yellow at all."))
    its.append(mcq("Hana picks a counter 10 times and puts it back each time. She gets red all 10 times. "
                   "Is picking red certain?", "Not sure: red may just be likely",
                   ["Yes, red must be certain", "No, red is impossible", "No, red is unlikely"],
                   "If the bag has many red counters and 1 blue, red is likely and could come up 10 times in a row. "
                   "Red is certain only if every counter is red."))
    m = 30 - 18
    assert m == 12
    its.append(mcq("Mei spins a red and blue spinner 30 times. She gets red 18 times. How many times did she get blue?",
                   "12 times", ["48 times", "18 times", "30 times"],
                   "Every spin is red or blue. 30 − 18 = 12 times blue."))
    assert 20 - 9 - 6 == 5
    its.append(mcq("Nadia uses a spinner to simulate the weather in Nanaimo. In 20 tries she gets "
                   "rain 9 times, cloud 6 times and sun the rest of the time. How many times did she get sun?",
                   "5 times", ["15 times", "11 times", "35 times"],
                   "Step 1: rain and cloud: 9 + 6 = 15. Step 2: 20 − 15 = 5 times sun."))
    its.append(mcq("Ethan tosses a coin 10 times: H, T, T, H, T, H, H, H, T, H. How many times did he get heads?",
                   "6 times", ["4 times", "10 times", "5 times"],
                   "Count each H: there are 6. There are 4 T’s, and 6 + 4 = 10 tosses."))
    tt = T("Chloe’s 16 spins", "Colour", ["Red", "Blue"], [9, 7], "Chloe's spins")
    its.append(mcq(tt + "Chloe spins 4 more times and gets blue every time. Which colour has more tallies now?",
                   "blue", ["red", "they are the same", "you cannot tell"],
                   "Blue: 7 + 4 = 11. Red stays at 9. 11 is more than 9, so blue has more tallies now."))
    assert len(its) == 20
    return {"title": "Experiments: read the tally results", "items": its}


# ------------------------------------------------------------ set 4: compare predictions with results
def set_predict(rnd):
    its = []
    F = lambda sec: fig(spinner_svg(sec))
    assert 20 // 2 == 10
    its.append(mcq(F(eq("red", "blue")) + "Jasleen spins this spinner 20 times. About how many times should she predict red?",
                   "about 10 times", ["about 20 times", "about 2 times", "about 5 times"],
                   "Red is half of the spinner, so about half of the spins should be red. Half of 20 is 10."))
    assert 20 * 3 // 4 == 15
    its.append(mcq(F(eq("blue", "blue", "red", "blue")) + "Harjot spins this spinner 20 times. Which prediction is best?",
                   "blue 15, red 5", ["blue 5, red 15", "blue 10, red 10", "blue 20, red 0"],
                   "3 of the 4 equal sections are blue, so blue should come up about 3 times as often as red. "
                   "Blue 15 and red 5 fits best."))
    assert 40 // 4 == 10
    its.append(mcq(F(eq("red", "blue", "yellow", "green")) + "Olivia spins this spinner 40 times. "
                   "About how many times should she predict red?", "about 10 times",
                   ["about 40 times", "about 4 times", "about 20 times"],
                   "Red is 1 of 4 equal sections, so about 1 spin in every 4 is red. 40 ÷ 4 = 10."))
    sec = [("red", 2), ("blue", 1), ("yellow", 1)]
    its.append(mcq(F(sec) + "Ji-woo spins this spinner 20 times. About how many times should she predict red?",
                   "about 10 times", ["about 7 times", "about 5 times", "about 20 times"],
                   "Red covers half of the spinner, so predict red about half the time: 10 of 20. "
                   "About 7 comes from thinking the 3 sections are the same size, but they are not."))
    pt = fig(table_svg("Prediction and results", ["", "Red", "Blue"], [["Predicted", "15", "5"], ["Result", "13", "7"]],
                       label="table: predicted and real results"))
    its.append(mcq(pt + "Owen predicted his 20 spins. How many more times did blue come up than he predicted?",
                   "2 more times", ["12 more times", "7 more times", "5 more times"],
                   "Blue: predicted 5, result 7. 7 − 5 = 2 more times."))
    its.append(mcq(pt + "Which colour came up less often than Owen predicted?", "red",
                   ["blue", "both colours", "neither colour"],
                   "Red: predicted 15, result 13. 13 is less than 15. Blue came up more often than predicted."))
    its.append(mcq(pt + "Was Owen’s prediction a good one?", "Yes, the results were close to it",
                   ["No, the results must match exactly", "No, blue should never come up", "Yes, the results matched exactly"],
                   "A prediction tells you about how many, not exactly how many. 13 and 7 are close to 15 and 5, "
                   "so it was a good prediction."))
    its.append(mcq(F(eq("red", "blue")) + "Lucas spins this spinner 20 times. Which result would be most surprising?",
                   "red 20, blue 0", ["red 10, blue 10", "red 11, blue 9", "red 8, blue 12"],
                   "Half the spinner is red and half is blue, so you expect about 10 of each. Results near 10 are normal. "
                   "Red every single time is possible, but very unlikely."))
    tg = fig(tally_svg("Mei’s 20 spins", "Colour", ["Green", "Purple"], [15, 5], label="tally chart: Mei's spins"))
    its.append(mcq(tg + "Mei’s spinner has 4 equal sections. Which spinner did she most likely use?",
                   "3 green and 1 purple section",
                   ["1 green and 3 purple sections", "2 green and 2 purple sections", "4 green sections"],
                   "Green came up about 3 times as often as purple, so green probably covers 3 of the 4 sections. "
                   "With 4 green sections, purple would be impossible, but it came up 5 times."))
    its.append(mcq("Mei and Wei spin the same spinner 20 times each. Mei gets red 9 times and Wei gets red 12 times. "
                   "Which sentence is true?", "Results can be different each time",
                   ["Wei’s spinner must be broken", "Mei made a mistake", "Red is certain for Wei"],
                   "Spins happen by chance, so two experiments with the same spinner can give different results."))
    its.append(mcq("Ji-woo predicts 10 heads in 20 coin tosses. She gets 12 heads. Was her prediction wrong?",
                   "No, results are often a little different", ["Yes, it was wrong", "Yes, she should predict 20 heads",
                                                               "No, she got exactly 10"],
                   "10 heads out of 20 is the best prediction. 12 is close to 10. Real results often differ a little."))
    its.append(mcq(F(eq("blue", "blue", "red", "blue")) + "Hana predicts that every spin will be blue. Is she right?",
                   "No, blue is likely, but red can still come up",
                   ["Yes, blue is certain", "No, red is more likely", "No, blue is impossible"],
                   "3 of the 4 equal sections are blue, so blue is likely. Red is 1 section, so red will come up sometimes. "
                   "Likely is not the same as certain."))
    its.append(mcq("Arjun tosses a coin 5 times and gets heads every time. What about the next toss?",
                   "Heads and tails are still equally likely",
                   ["Tails is now certain", "Heads is now certain", "Heads is now impossible"],
                   "A coin does not remember what happened before. Every toss, heads and tails are equally likely."))
    assert 16 * 6 // 8 == 12
    its.append(mcq(fig(bag_svg([("red", 6), ("blue", 2)], rnd)) + "Nadia picks a counter and puts it back, 16 times. "
                   "Which prediction is best?", "red 12, blue 4",
                   ["red 4, blue 12", "red 8, blue 8", "red 16, blue 0"],
                   "6 of the 8 counters are red: 3 times as many red as blue. Red 12 and blue 4 fits best. "
                   "Red 16 and blue 0 would mean blue is impossible, but there are blue counters."))
    roll = [5, 4, 6, 3, 7, 5]
    assert sum(roll) == 30 and max(roll) == roll[4]
    tb = fig(table_svg("Zara’s 30 rolls", ["Number", "1", "2", "3", "4", "5", "6"], [["Times"] + [str(r) for r in roll]],
                       label="table: Zara's number cube rolls"))
    its.append(mcq(tb + "Zara predicted each number about 5 times. Which number came up the most?", "5",
                   ["6", "1", "4"],
                   "Find the biggest number in the Times row: 7. It is under the number 5. "
                   "(6 is the biggest number on the cube, not the one rolled most.)"))
    its.append(mcq(tb + "Zara says 5 will always come up most, because it did this time. Is she right?",
                   "No, each number is equally likely",
                   ["Yes, 5 is more likely", "No, 6 is more likely", "No, 4 is more likely"],
                   "Each face of a number cube has the same chance. Next time, a different number may come up most."))
    S = [eq("green", "purple", "purple", "purple"), eq("green", "green", "green", "purple"),
         eq("green", "purple", "green", "purple"), eq("purple", "purple", "purple", "purple")]
    its.append(abcd_q(fig(spinners_abcd(S)) + "Leah spins one of these spinners 40 times: green 21, purple 19. "
                      "Which spinner did she most likely use?", "Spinner", 2,
                      "Green and purple came up about the same number of times. Spinner C is half green and half purple. "
                      "Spinner D could never give green."))
    its.append(abcd_q(fig(spinners_abcd(S)) + "Ryan spins one of these spinners 40 times: green 9, purple 31. "
                      "Which spinner did he most likely use?", "Spinner", 0,
                      "Purple came up about 3 times as often as green. Spinner A is 3 quarters purple and 1 quarter green. "
                      "Spinner D could not give any green."))
    assert 12 // 3 == 4
    its.append(mcq("The class uses a spinner to simulate the weather in Prince George. 1 of 3 equal sections means snow. "
                   "In 12 spins, about how many times should they predict snow?", "about 4 times",
                   ["about 3 times", "about 12 times", "about 9 times"],
                   "Snow is 1 of 3 equal sections, so about 1 spin in every 3. 12 ÷ 3 = 4. "
                   "9 is the prediction for no snow."))
    its.append(mcq("Kai predicted red about 10 times in 40 spins. He got red 11 times. What should he do?",
                   "Keep his prediction: 11 is close to 10",
                   ["Say red is now more likely", "Say red is now certain", "Change the spinner"],
                   "Results vary a little each time. 11 is very close to 10, so the prediction was good."))
    assert len(its) == 20
    return {"title": "Compare predictions with results", "items": its}


# ------------------------------------------------------------ set 5: fair games
def set_fair(rnd):
    its = []
    F = lambda sec: fig(spinner_svg(sec))
    its.append(mcq("What makes a game fair?", "Each player is equally likely to win",
                   ["One player is more likely to win", "The winner is certain", "The best player always wins"],
                   "A game of chance is fair when every player has the same chance to win."))
    its.append(mcq("Before a soccer game in Surrey, the referee tosses a coin to choose which team kicks off. Is this fair?",
                   "Yes, heads and tails are equally likely",
                   ["No, heads is more likely", "No, tails is more likely", "Yes, because heads is certain"],
                   "A coin has one heads side and one tails side, so each team has the same chance."))
    sec = eq("red", "red", "red", "blue")
    its.append(mcq(F(sec) + "Zara gets a point for red. Owen gets a point for blue. Is the game fair?",
                   "No, Zara is more likely to win",
                   ["Yes, it is fair", "No, Owen is more likely to win", "No, Zara is certain to win"],
                   "3 of the 4 equal sections are red and only 1 is blue. Red is more likely, so Zara has the better chance. "
                   "She is not certain to win: blue can still come up."))
    sec = [("red", 3), ("blue", 1)]
    its.append(mcq(F(sec) + "Emma says this game is fair, because the spinner has 2 sections: red for her and blue for Liam. "
                   "Is she right?", "No, the red part is bigger",
                   ["Yes, 2 sections means fair", "No, the blue part is bigger", "Yes, both colours are certain"],
                   "Look at the size of each part, not the number of sections. Red covers 3 quarters of the spinner, "
                   "so Emma is more likely to win."))
    S = [eq("red", "red", "red", "blue"), [("red", 1), ("blue", 3)], eq("red", "blue", "red", "blue"), [("red", 3), ("blue", 1)]]
    its.append(abcd_q(fig(spinners_abcd(S)) + "Red is for Sofia and blue is for Noah. Which spinner makes the game fair?",
                      "Spinner", 2,
                      "On Spinner C, red and blue each cover half, so they are equally likely. "
                      "On B and D, one colour has a bigger part."))
    its.append(mcq(fig(cube_faces_svg()) + "Kai gets a point for an even number (2, 4, 6). Leah gets a point for an odd number "
                   "(1, 3, 5). Is the game fair?", "Yes, each has 3 numbers",
                   ["No, Kai has the bigger numbers", "No, Leah is more likely to win", "No, 6 is more likely"],
                   "Kai has 3 faces and Leah has 3 faces. Every face is equally likely, so the game is fair."))
    its.append(mcq(fig(cube_faces_svg()) + "Arjun gets a point for 1 or 2. Simran gets a point for 3, 4, 5 or 6. Who is more likely to win?",
                   "Simran", ["Arjun", "they are equally likely", "neither player"],
                   "Simran has 4 faces and Arjun has only 2. More faces means more likely, so Simran is more likely to win."))
    its.append(mcq(fig(cube_faces_svg()) + "Harjot gets a point for a 6. Jasleen gets a point for a 1. Is the game fair?",
                   "Yes, a 6 and a 1 are equally likely",
                   ["No, 6 is more likely", "No, 1 is more likely", "No, both are impossible"],
                   "Each face of the cube has the same chance. A 6 is not harder to roll than a 1."))
    its.append(mcq(fig(cube_faces_svg()) + "Arjun gets a point for 1 or 2. Simran gets a point for 3, 4, 5 or 6. "
                   "Which change makes the game fair?", "Arjun also gets 3",
                   ["Arjun also gets 3 and 4", "Simran also gets 2", "Arjun gets 6 instead of 2"],
                   "Fair means each player has 3 of the 6 faces. Give 3 to Arjun: Arjun 1, 2, 3 and Simran 4, 5, 6."))
    assert 3 + 2 == 5
    its.append(mcq(fig(bag_svg([("red", 5), ("blue", 3)], rnd)) + "Mateo wins with red and Chloe wins with blue. "
                   "How many blue counters should they add to make the game fair?", "2",
                   ["5", "8", "3"],
                   "Fair means the same number of red and blue counters. Red has 5 and blue has 3, so add 5 − 3 = 2 blue."))
    its.append(mcq("Ryan writes the names of 4 friends on cards for a draw. He writes his own name on 2 cards. Is the draw fair?",
                   "No, Ryan is more likely to be picked",
                   ["Yes, it is fair", "No, Ryan is less likely to be picked", "No, Ryan is certain to be picked"],
                   "Ryan’s name is on 2 cards and each friend is on only 1. More cards means more likely, so the draw is not fair."))
    its.append(mcq("The teacher puts 24 names in a toque, one card for each student, and picks one to feed the class fish. "
                   "Is this fair?", "Yes, each name is equally likely",
                   ["No, the first name is more likely", "No, some names are impossible to pick", "Yes, every student is certain to be picked"],
                   "Each student has exactly 1 card, so every student has the same chance."))
    its.append(word_q("At the school fun fair, 50 raffle tickets are sold. Liam buys 1 ticket. Liam winning the raffle is …",
                      "unlikely", "Liam has only 1 of the 50 tickets. He could win, but it is unlikely.", keep=("impossible",)))
    its.append(mcq("Nadia’s grandma buys 40 of the 50 raffle tickets. Who is more likely to win: Nadia’s grandma or Liam with 1 ticket?",
                   "Nadia’s grandma", ["Liam", "they are equally likely", "neither can win"],
                   "40 tickets is far more than 1 ticket. More tickets means more likely to win, but it is still not certain."))
    its.append(mcq("Wei wins a prize for picking a green counter. Bag A has 3 green and 5 yellow. Bag B has 5 green and 3 yellow. "
                   "Which bag should he choose?", "Bag B", ["Bag A", "either bag, they are the same", "neither bag"],
                   "Both bags have 8 counters. Bag B has 5 green and Bag A has only 3, so green is more likely in Bag B."))
    its.append(mcq("The class simulates a salmon swimming up the Fraser River with a spinner: 3 equal sections say “gets past” "
                   "and 1 says “stopped”. Which is more likely in the simulation?", "the salmon gets past",
                   ["the salmon is stopped", "they are equally likely", "the salmon is certain to get past"],
                   "3 of the 4 equal sections say gets past, so that is more likely. It is not certain, because 1 section says stopped."))
    its.append(mcq("Ava and Olivia play rock, paper, scissors. Ava says she always wins because she is lucky. "
                   "Which is true?", "Each player is equally likely to win",
                   ["Ava is certain to win", "Olivia can never win", "Ava is more likely, because she is lucky"],
                   "When both players choose by chance, each one is equally likely to win a round. Luck does not change the chance."))
    assert 10 + 10 == 20
    its.append(mcq("Mei and Ji-woo test a game 20 times to see if it is fair. Which result shows a fair game best?",
                   "Mei 11 wins, Ji-woo 9 wins",
                   ["Mei 18 wins, Ji-woo 2 wins", "Mei 20 wins, Ji-woo 0 wins", "Mei 3 wins, Ji-woo 17 wins"],
                   "In a fair game, each player should win about half the time: about 10 each. 11 and 9 is closest."))
    sec = eq("red", "blue", "yellow")
    its.append(mcq(F(sec) + "Three friends play. Owen has red, Leah has blue and Kai has yellow. Is the game fair?",
                   "Yes, the 3 parts are the same size",
                   ["No, red is first", "No, Kai is more likely to win", "No, there are too many players"],
                   "The 3 sections are equal, so each friend has the same chance to win. The game is fair."))
    sec = [("red", 2), ("blue", 1), ("yellow", 1)]
    its.append(mcq(F(sec) + "Owen has red, Leah has blue and Kai has yellow. Who is most likely to win?",
                   "Owen", ["Leah", "Kai", "they are equally likely"],
                   "Red covers half of the spinner. Blue and yellow each cover only a quarter. "
                   "Owen’s colour has the biggest part, so he is most likely to win."))
    assert len(its) == 20
    return {"title": "Fair games and word problems", "items": its}


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
        "<h2>Words for how likely something is</h2>"
        "<p>Likelihood tells us how likely something is to happen. "
        "<b>Impossible</b> means it can never happen. <b>Certain</b> means it must happen. "
        "<b>Unlikely</b> means it could happen, but probably will not. <b>Likely</b> means it will probably happen. "
        "<b>Equally likely</b> means two things have the same chance.</p>"
        "<figure class='sn-fig'>" + scale_svg() +
        "<figcaption>From impossible to certain. Equally likely is in the middle.</figcaption></figure>" +
        table(["Word", "Meaning", "Example"], [
            ["impossible", "can never happen", "An orca will walk down the street."],
            ["unlikely", "could happen, but probably will not", "A black bear will walk onto the school field."],
            ["equally likely", "the same chance", "A tossed coin lands on heads or on tails."],
            ["likely", "will probably happen", "It will rain in Vancouver in November."],
            ["certain", "must happen", "Wednesday will come after Tuesday."],
        ]) +
        "<p>To compare two events, say which one is <b>more likely</b> or <b>less likely</b>, "
        "or say they are <b>equally likely</b>.</p>"
        "<h2>Spinners and bags: look at the size of each part</h2>"
        "<p>A spinner is more likely to land on a colour that covers <b>more</b> of it. "
        "Compare the size of the parts, not just the number of sections. "
        "In a bag, the colour with <b>more</b> counters is more likely.</p>"
        "<figure class='sn-fig'>" + spinner_svg([("red", 6), ("blue", 1), ("green", 3), ("blue", 1), ("blue", 1)],
                                                  "spinner: red half, green quarter, 3 small blue sections") +
        "<figcaption>Blue has 3 sections, but red covers half of the spinner.</figcaption></figure>" +
        ex("Example", "Which colour is the arrow most likely to land on?",
           "Red is one big section: half of the spinner. The 3 small blue sections together are only a quarter.", "red") +
        "<h2>Simulations and tally results</h2>"
        "<p>A <b>simulation</b> uses a coin, spinner, bag or number cube to act out a real event. "
        "For example, heads can stand for a goal and tails for a miss. Record each result with a tally mark.</p>"
        "<figure class='sn-fig'>" + tally_svg("Wei’s 24 spins", "Colour", ["Red", "Blue", "Yellow"], [13, 7, 4],
                                                "tally chart: Wei's spins") +
        "<figcaption>Each group of 5 has 4 marks and 1 mark across them.</figcaption></figure>" +
        ex("Example", "How many spins were not red?", "Not red means blue or yellow: 7 + 4 = 11.", "11 spins") +
        "<h2>Compare predictions with results</h2>"
        "<p>Predict first. If red is 1 of 4 equal sections, predict red about 1 time in every 4 spins. "
        "Then compare. Results <b>vary</b>, so they are usually close to the prediction, not exactly the same.</p>" +
        ex("Example", "Red is half of a spinner. Kai spins 20 times and gets red 9 times. Was the prediction of about 10 good?",
           "Half of 20 is 10. 9 is close to 10.", "yes, the result is close") +
        "<h2>Fair games</h2>"
        "<p>A game is <b>fair</b> when every player is equally likely to win. "
        "A spinner with 2 red and 2 blue equal sections is fair for a red player and a blue player. "
        "A number cube game is fair when each player has the same number of faces.</p>"
        "<figure class='sn-fig'>" + cube_faces_svg() +
        "<figcaption>Even (2, 4, 6) and odd (1, 3, 5): 3 faces each, so the game is fair.</figcaption></figure>" +
        "<h2>Common mistakes</h2>" +
        table(["Mistake", "What to do instead"], [
            ["Counting sections, not their size", "Compare how much of the spinner each colour covers"],
            ["Saying certain when it is only likely", "Certain means it must happen every time. If it could fail, it is likely"],
            ["Saying impossible when it is only unlikely", "If it could happen even once, it is not impossible"],
            ["Expecting results to match the prediction exactly", "Results vary: close to the prediction is normal"],
            ["Thinking tails is due after many heads", "A coin does not remember: heads and tails stay equally likely"],
        ])
    )


FAQ = [
    {"q": "What do Grade 3 students learn about probability in BC?",
     "a": "In the Data and probability area of the BC Grade 3 math curriculum, students describe the likelihood of simulated events with comparative language: more likely, less likely, equally likely, impossible and certain. They use spinners, coins, bags and number cubes."},
    {"q": "What is a simulated event?",
     "a": "A simulated event uses a coin, spinner, bag or number cube to act out something real. For example, a class can toss a coin many times, with heads for a goal and tails for a miss, and record the results with tallies."},
    {"q": "What is the difference between likely and certain?",
     "a": "Certain means it must happen every time, like Wednesday coming after Tuesday. Likely means it will probably happen but could fail, like landing on blue when 3 of 4 equal sections are blue."},
    {"q": "How can my child tell if a game is fair?",
     "a": "A game of chance is fair when every player is equally likely to win. Check that each player has parts of the same size on the spinner, or the same number of counters or number cube faces."},
]


def gen_unit():
    rnd = random.Random(53811)
    sets = [set_words(rnd), set_parts(rnd), set_tally(rnd), set_predict(rnd), set_fair(rnd)]
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
        "country": "ca-bc", "subject": "math", "grade": "grade-3", "slug": "likelihood-of-simulated-events", "sort": 11,
        "updated": UPDATED, "pdf_url": "",
        "title": "Likelihood of Simulated Events: More Likely, Less Likely or Equally Likely",
        "seo_title": "Grade 3 Math Likelihood and Probability Worksheets (BC Curriculum, Free, Answer Key)",
        "short_title": "Likelihood of simulated events",
        "domain": "Data and probability",
        "standard_code": "Grade 3: Data and probability",
        "standard_url": "https://curriculum.gov.bc.ca/curriculum/mathematics/3/core",
        "standard_text": "Likelihood of simulated events, using comparative language",
        "meta_desc": "Free Grade 3 math worksheets on likelihood for the BC curriculum: impossible, unlikely, equally likely, likely and certain, more likely and less likely with spinners and bags, tally results from coin and spinner simulations, predictions compared with results, and fair games. 100 questions with an answer key.",
        "key_big": "The bigger the part of the spinner or bag, the more likely the outcome.",
        "key_sub": "Compare the size of each part, not the number of sections. Likely is not certain, and unlikely is not impossible. Real results are close to the prediction, not exactly the same.",
        "body_html": body_html(rnd), "faq": FAQ, "sets": sets,
    }

def assign_words(items, cnt, rnd):
    """Pick which of the 5 words to leave out of each word question, so no answer position is used more than 5 times."""
    opts = []
    for it in items:
        o = []
        for om in WORDS5:
            if om == it["_word"] or om in it["_keep"]:
                continue
            ch = [w for w in WORDS5 if w != om]
            o.append((ch.index(it["_word"]), ch))
        rnd.shuffle(o)
        o.sort(key=lambda t: cnt[t[0]])
        opts.append(o)
    order = sorted(range(len(items)), key=lambda i: len({p for p, _ in opts[i]}))
    pick = {}

    def dfs(k):
        if k == len(order):
            return True
        i = order[k]
        for p, ch in sorted(opts[i], key=lambda t: cnt[t[0]]):
            if cnt[p] < 5:
                cnt[p] += 1
                pick[i] = (p, ch)
                if dfs(k + 1):
                    return True
                cnt[p] -= 1
        return False

    assert dfs(0), "cannot balance word questions"
    for i, it in enumerate(items):
        p, ch = pick[i]
        it["c"], it["a"] = ch, p
        del it["_word"], it["_keep"]


def balance(sets, rnd):
    """Fixed questions keep their order. The rest are moved so every position is right 5 times in each set."""
    for s in sets:
        cnt, free, words = [0] * 4, [], []
        for it in s["items"]:
            if "_word" in it:
                words.append(it)
            elif it.pop("_fix", False):
                cnt[it["a"]] += 1
            else:
                free.append(it)
        assign_words(words, cnt, rnd)
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
    """Tag pictures that must print larger (A to D panels, tables, tally charts, number cube faces) so their labels stay readable."""
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
        mark_large(u, "(spinners A to D|bags A to D|tally chart|table|the six faces)")
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
