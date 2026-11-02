# -*- coding: utf-8 -*-
"""
Canada (Ontario) Grade 4 Math: Probability (Ontario Mathematics Curriculum 2020: Grade 4, D2.1)
  python3 tools/gen_caon_math_g4_probability.py
The five likelihood words, the probability line from 0 to 1 (0 impossible, 0.5 equally likely, 1 certain, tenths),
spinners, bags of counters and number cubes, comparing likelihood, and predictions and fair games.
Wrong answers come from real student mistakes: likely confused with certain, unlikely confused with impossible,
counting sections instead of looking at their size, more red counters taken as more likely without looking at the
whole bag, counting tick marks instead of steps on the line, reading the other colour's chance, and "it is due" thinking.
Every picture shows the colour as a letter too (R = red ...), so it still works when printed in black and white.
HTML attributes use single quotes (no backslashes in the JSON). Canadian English.
"""
import json, re, math, os, random

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "ca-on", "math", "grade-4")
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


# ------------------------------------------------------------ probability line
def pline_svg(marks=(), five=False, label="probability line"):
    """Probability line from 0 to 1 with tenth ticks. marks: [(value in tenths 0..10, letter or '')] arrows above.
    Numbers 0, 0.5, 1 under the line; words impossible / equally likely / certain (all five words if five=True)."""
    W, x0, L = 460, 50, 360
    top = 40 if any(l for _, l in marks) else 24
    ly = top + (14 if marks else 0)

    def X(t):
        return x0 + L * t / 10.0

    s = ["<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='3'/>" % (x0, ly, x0 + L, ly, INK)]
    for k in range(11):
        h = 10 if k in (0, 5, 10) else 6
        s.append("<line x1='%.1f' y1='%d' x2='%.1f' y2='%d' stroke='%s' stroke-width='2'/>" % (X(k), ly - h, X(k), ly + h, INK))
    for k, t in ((0, "0"), (5, "0.5"), (10, "1")):
        s.append(text(X(k), ly + 28, t, 15, bold=True))
    wl = [(0, "impossible"), (5, "equally likely"), (10, "certain")]
    if five:
        wl += [(2.5, "unlikely"), (7.5, "likely")]
    for k, t in wl:
        s.append(text(X(k), ly + 48, t, 14, col=GREEN))
    xs = sorted(X(v) for v, _ in marks)
    assert all(b - a >= 30 for a, b in zip(xs, xs[1:])), marks
    for v, lab in marks:
        x = X(v)
        s.append("<line x1='%.1f' y1='%d' x2='%.1f' y2='%d' stroke='%s' stroke-width='3'/>" % (x, ly - 30, x, ly - 13, GREEN))
        s.append("<polygon points='%.1f,%d %.1f,%d %.1f,%d' fill='%s'/>" % (x - 6, ly - 15, x + 6, ly - 15, x, ly - 4, GREEN))
        if lab:
            s.append(text(x, ly - 35, lab, 17, bold=True, col=GREEN))
    return svg_wrap(W, ly + 56, "".join(s), label)


def PL(v, lab="probability line"):
    return fig(pline_svg([(v, "")], label=lab))


# ------------------------------------------------------------ set 1: likelihood words
def set_words(rnd):
    its = []
    its.append(word_q("Ava rolls a number cube with the numbers 1 to 6. She will roll a 7. How likely is this?", "impossible",
                      "The cube only has the numbers 1 to 6. There is no 7, so rolling a 7 can never happen. It is impossible."))
    its.append(word_q("Kai draws a triangle. It will have 4 sides. How likely is this?", "impossible",
                      "Every triangle has exactly 3 sides. A triangle with 4 sides can never happen, so it is impossible."))
    its.append(word_q("Next month will have 45 days. How likely is this?", "impossible",
                      "Every month has 28 to 31 days. A month with 45 days can never happen, so it is impossible."))
    its.append(word_q("The sun will rise tomorrow morning. How likely is this?", "certain",
                      "The sun rises every morning. It must happen, so it is certain."))
    its.append(word_q("Thanksgiving in Canada will be in October next year. How likely is this?", "certain",
                      "Canadian Thanksgiving is always on the second Monday of October. It must happen, so it is certain."))
    its.append(word_q("Arjun has 4 quarters in his pocket and no other coins. He takes out one coin without looking. "
                      "It will be a quarter. How likely is this?", "certain",
                      "Every coin in his pocket is a quarter, so he must take out a quarter. It is certain."))
    its.append(word_q("On a cold, snowy day in January, Liam will wear mitts to walk to school. How likely is this?", "likely",
                      "Most children wear mitts on a cold, snowy day. But Liam could forget them, "
                      "so it is likely, not certain.", keep=("certain",)))
    its.append(word_q("A pumpkin bought at a farm market in October will be orange. How likely is this?", "likely",
                      "Most pumpkins are orange, but some are white or green. So it is likely, not certain.", keep=("certain",)))
    assert 22 + 3 == 25
    its.append(word_q("In Priya’s class, 22 students like soccer and 3 do not. The teacher picks one student without looking. "
                      "The student will like soccer. How likely is this?", "likely",
                      "22 of the 25 students like soccer. That is most of the class, so it is likely. "
                      "It is not certain, because 3 students do not like soccer."))
    its.append(word_q("Noah will find a toonie on the sidewalk on the way to school. How likely is this?", "unlikely",
                      "It could happen, but it almost never does. So it is unlikely. It is not impossible: people do drop coins.",
                      keep=("impossible",)))
    its.append(word_q("There are 30 names in a hat. Chloe’s name is one of them. The teacher picks one name. "
                      "It will be Chloe’s name. How likely is this?", "unlikely",
                      "Chloe’s name is only 1 of the 30 names. It could be picked, but probably will not be. "
                      "So it is unlikely, not impossible.", keep=("impossible",)))
    its.append(word_q("A moose will walk down a busy street in downtown Toronto today. How likely is this?", "unlikely",
                      "Moose live in forests, far from big city streets. It has happened, but very rarely. "
                      "So it is unlikely, not impossible.", keep=("impossible",)))
    its.append(word_q("Hana tosses a coin. It will land on heads. How likely is this?", "equally likely",
                      "A coin has 2 sides: heads and tails. Heads is just as likely to happen as not to happen, "
                      "so it is equally likely."))
    its.append(word_q("Ethan has 2 cards face down: one red card and one black card. He picks one. "
                      "It will be the red card. How likely is this?", "equally likely",
                      "There is 1 red card and 1 black card. Picking red and picking black have the same chance, "
                      "so it is equally likely."))
    assert [n for n in range(1, 7) if n % 2 == 0] == [2, 4, 6]
    its.append(word_q("Owen rolls a number cube with the numbers 1 to 6. He will roll an even number. How likely is this?",
                      "equally likely",
                      "Even numbers: 2, 4 and 6 (3 faces). Not even: 1, 3 and 5 (3 faces). "
                      "3 and 3 are the same, so it is equally likely."))
    its.append(mcq("Which event is certain?", "A week will have 7 days",
                   ["It will rain tomorrow", "Ava will get a puppy", "The bus will be late"],
                   "Every week has 7 days, so it must happen. The other events might happen or might not."))
    its.append(mcq("Which event is impossible?", "Rolling a 0 on a number cube",
                   ["Rolling a 6 on a number cube", "A coin landing on tails", "Snow in Ottawa in March"],
                   "A number cube has the numbers 1 to 6. There is no 0, so rolling a 0 can never happen. "
                   "The other events can happen."))
    its.append(word_q("Jayden’s hockey team won its last 5 games. Jayden says, “It is certain that we will win the next game.” "
                      "Which word should he use instead?", "likely",
                      "A good team will probably win, but it could still lose. If something could fail to happen, "
                      "it is not certain. The better word is likely.", keep=("certain",)))
    its.append(word_q("Leah buys 1 of the 200 tickets for the school raffle. She says, “It is impossible that I will win.” "
                      "Which word should she use instead?", "unlikely",
                      "Leah has a ticket, so she could win. 1 of 200 is a very small chance, so the right word is unlikely, "
                      "not impossible."))
    its.append(word_q("Which word means “it could happen, but it probably will not”?", "unlikely",
                      "Unlikely means it can happen, but probably will not. Impossible means it can never happen."))
    assert len(its) == 20
    return {"title": "Likelihood words: impossible to certain", "items": its}


# ------------------------------------------------------------ set 2: the probability line
def set_line(rnd):
    its = []
    its.append(mcq("On a probability line from 0 to 1, where does an impossible event go?", "at 0",
                   ["at 1", "at 0.5", "near 0, not at 0"],
                   "Impossible is the lowest chance there is, so it goes at the very start: 0. "
                   "Near 0 (but not at 0) is for unlikely events."))
    its.append(mcq("On a probability line from 0 to 1, where does a certain event go?", "at 1",
                   ["at 0", "at 0.5", "near 1, not at 1"],
                   "Certain is the highest chance there is, so it goes at the very end: 1. "
                   "Near 1 (but not at 1) is for likely events."))
    its.append(mcq("On a probability line from 0 to 1, where does an equally likely event go?", "at 0.5",
                   ["at 0", "at 1", "at 2"],
                   "Equally likely is halfway between impossible (0) and certain (1). Halfway is 0.5. "
                   "2 is not on the line at all."))
    its.append(mcq("On a probability line from 0 to 1, where does an unlikely event go?", "between 0 and 0.5",
                   ["at 0", "between 0.5 and 1", "at 1"],
                   "Unlikely means it could happen, but probably will not. That is more than impossible (0) "
                   "but less than equally likely (0.5)."))
    its.append(word_q(PL(9, "probability line arrow at 0.9") + "Which word best describes the chance shown by the arrow?",
                      "likely",
                      "The arrow is at 0.9. That is close to 1, but not at 1. So it is likely, not certain.",
                      keep=("certain",)))
    its.append(word_q(PL(2, "probability line arrow at 0.2") + "Which word best describes the chance shown by the arrow?",
                      "unlikely",
                      "The arrow is at 0.2. That is between 0 and 0.5, closer to 0. So it is unlikely. "
                      "It is not impossible, because it is not at 0.", keep=("impossible",)))
    its.append(word_q(PL(10, "probability line arrow at 1") + "Which word describes the chance shown by the arrow?", "certain",
                      "The arrow is at 1, the very end of the line. That means certain."))
    its.append(word_q(PL(5, "probability line arrow at 0.5") + "Which word describes the chance shown by the arrow?",
                      "equally likely",
                      "The arrow is at 0.5, exactly halfway between 0 and 1. That means equally likely."))
    its.append(word_q(PL(0, "probability line arrow at 0") + "Which word describes the chance shown by the arrow?", "impossible",
                      "The arrow is at 0, the very start of the line. That means impossible."))
    M1 = [(0, "A"), (2, "B"), (5, "C"), (9, "D")]
    L1 = lambda: fig(pline_svg(M1, label="probability line with points A B C D"))
    its.append(abcd_q(L1() + "Which letter shows the chance of rolling a 7 on a number cube with the numbers 1 to 6?",
                      "Point", 0,
                      "There is no 7 on the cube, so it is impossible. Impossible goes at 0: point A."))
    its.append(abcd_q(L1() + "Which letter shows the chance of a coin landing on heads?", "Point", 2,
                      "Heads and tails are equally likely, so the chance is halfway: 0.5. That is point C."))
    its.append(abcd_q(L1() + "Which letter best shows the chance of snow on the ground in Winnipeg on January 15?",
                      "Point", 3,
                      "Winnipeg almost always has snow on the ground in January. It is very likely, but not certain, "
                      "so it goes near 1: point D."))
    assert 1 + 4 == 5 and 1 * 10 // 5 == 2
    its.append(abcd_q(L1() + "A bag has 1 blue counter and 4 red counters. Which letter shows the chance of picking "
                      "the blue counter?", "Point", 1,
                      "1 of the 5 counters is blue. That could happen, but probably will not: unlikely. "
                      "It goes between 0 and 0.5, near 0: point B."))
    M2 = [(1, "A"), (3, "B"), (7, "C"), (10, "D")]
    L2 = lambda: fig(pline_svg(M2, label="probability line with points A B C D"))
    assert 7 + 3 == 10
    its.append(abcd_q(L2() + "A spinner has 10 equal sections: 7 green and 3 yellow. "
                      "Which letter shows the chance of landing on green?", "Point", 2,
                      "7 of the 10 equal sections are green: 7 tenths = 0.7. That is point C."))
    its.append(abcd_q(L2() + "A spinner has 10 equal sections: 7 green and 3 yellow. "
                      "Which letter shows the chance of landing on yellow?", "Point", 1,
                      "3 of the 10 equal sections are yellow: 3 tenths = 0.3. That is point B. "
                      "Point C (0.7) is for green."))
    its.append(abcd_q(L2() + "A spinner has 10 equal sections: 7 green and 3 yellow. "
                      "Which letter shows the chance of landing on green or yellow?", "Point", 3,
                      "Every section is green or yellow, so the arrow must land on one of them. That is certain: 1, point D."))
    its.append(mcq(PL(6, "probability line arrow at 0.6") + "The line is split into tenths. What number does the arrow show?",
                   "0.6", ["0.4", "6", "0.7"],
                   "Each small step is 0.1. Count the steps from 0: 6 steps, so 0.6. "
                   "0.4 counts back from 1. 0.7 counts the tick marks instead of the steps."))
    assert 4 + 6 == 10
    its.append(mcq("A bag has 10 counters: 4 red and 6 blue. Where on the probability line does picking a red counter go?",
                   "at 0.4", ["at 0.6", "at 4", "at 1"],
                   "4 of the 10 counters are red: 4 tenths = 0.4. 0.6 is the chance of blue. "
                   "4 is not on a line that goes from 0 to 1."))
    its.append(mcq("The weather forecast says rain is likely on Saturday. Kai puts “rain on Saturday” at 1 on the probability line. "
                   "Where should it go?", "between 0.5 and 1", ["at 1", "at 0", "between 0 and 0.5"],
                   "Likely means it will probably happen, but it is not sure. 1 is only for certain events. "
                   "Likely goes between 0.5 and 1."))
    its.append(mcq("A bag has 10 counters: 1 blue and 9 red. Mei puts “picking the blue counter” at 0, "
                   "because it probably will not happen. Where should it go?", "at 0.1", ["at 0", "at 0.9", "at 1"],
                   "There is 1 blue counter, so it can happen: it is not impossible. 1 of 10 = 1 tenth = 0.1. "
                   "0.9 is the chance of red."))
    assert len(its) == 20
    return {"title": "The probability line from 0 to 1", "items": its}


# ------------------------------------------------------------ set 3: spinners and bags
def set_spin_bag(rnd):
    its = []
    F = lambda sec, lab="spinner": fig(spinner_svg(sec, lab))
    B = lambda counts, lab="bag of counters": fig(bag_svg(counts, rnd, lab))
    its.append(mcq(F(eq("red", "red", "blue", "red")) + "The spinner has 4 equal sections. "
                   "Which colour is the arrow most likely to land on?", "red",
                   ["blue", "green", "red and blue tie"],
                   "3 of the 4 equal sections are red and only 1 is blue, so red is most likely. "
                   "There is no green, so green is impossible."))
    sec = eq(*(["green"] * 4 + ["yellow"] + ["green"] * 5))
    assert amounts(sec) == {"green": 9, "yellow": 1} and chance_word(9, 10) == "likely"
    its.append(word_q(F(sec) + "The spinner has 10 equal sections. Landing on green is …", "likely",
                      "9 of the 10 equal sections are green, so green is likely. "
                      "It is not certain, because 1 section is yellow.", keep=("certain",)))
    its.append(word_q(F(eq("blue", "blue", "blue", "blue", "blue", "blue")) + "Landing on blue is …", "certain",
                      "Every section is blue. The arrow must land on blue, so it is certain."))
    its.append(word_q(F(eq("red", "yellow", "blue", "yellow", "red", "blue")) + "Landing on purple is …", "impossible",
                      "There is no purple section on this spinner. The arrow can never land on purple, so it is impossible."))
    sec = eq("red", "yellow", "red", "yellow", "red", "yellow")
    assert chance_word(3, 6) == "equally likely"
    its.append(word_q(F(sec) + "Landing on red is …", "equally likely",
                      "3 of the 6 equal sections are red and 3 are not. Red covers half of the spinner, "
                      "so landing on red is equally likely."))
    sec = [("red", 1), ("blue", 1), ("red", 1), ("blue", 1), ("yellow", 4)]
    assert amounts(sec) == {"red": 2, "blue": 2, "yellow": 4}
    its.append(mcq(F(sec) + "Which colour is the arrow most likely to land on?", "yellow",
                   ["red", "blue", "all are equally likely"],
                   "Do not just count sections. Look at their size. The one yellow section is half of the spinner. "
                   "Red and blue each cover only a quarter."))
    sec = [("red", 6), ("blue", 1), ("green", 1)]
    assert amounts(sec)["red"] * 4 == 3 * 8
    its.append(word_q(F(sec) + "This spinner has 3 sections. Landing on red is …", "likely",
                      "Red is only 1 of the 3 sections, but it is a big one: it covers 3 quarters of the spinner. "
                      "So red is likely, not unlikely. It is not certain, because of the blue and green parts.",
                      keep=("certain", "unlikely")))
    its.append(mcq(B([("red", 6), ("blue", 2)]) + "Amira picks one counter from the bag without looking. "
                   "Which colour is she most likely to pick?", "red",
                   ["blue", "yellow", "red and blue tie"],
                   "There are 6 red counters and only 2 blue counters. More red counters means red is more likely."))
    assert chance_word(1, 10) == "unlikely"
    its.append(word_q(B([("red", 1), ("blue", 9)]) + "Picking a red counter from this bag is …", "unlikely",
                      "Only 1 of the 10 counters is red. It can happen, but not often, so it is unlikely, not impossible.",
                      keep=("impossible",)))
    its.append(word_q(B([("yellow", 5), ("green", 5)]) + "Picking a yellow counter from this bag is …", "equally likely",
                      "5 of the 10 counters are yellow and 5 are not. Yellow and not yellow have the same chance, "
                      "so it is equally likely."))
    its.append(mcq(B([("red", 3), ("blue", 4), ("yellow", 1)]) + "Which colour is least likely to be picked?", "yellow",
                   ["red", "blue", "all are the same"],
                   "Count each colour: red 3, blue 4, yellow 1. Yellow has the fewest counters, so it is least likely."))
    its.append(mcq(B([("red", 2), ("blue", 5), ("green", 3)]) + "Put the colours in order from most likely to least likely.",
                   "blue, green, red", ["red, green, blue", "green, blue, red", "blue, red, green"],
                   "Count each colour: blue 5, green 3, red 2. The most counters is most likely: blue, green, red."))
    its.append(mcq(B([("red", 3), ("blue", 5)]) + "Where on the probability line does picking a red counter go?",
                   "between 0 and 0.5", ["between 0.5 and 1", "at 0.5", "at 0"],
                   "3 of the 8 counters are red. Half of 8 is 4, and 3 is less than 4. "
                   "So red is unlikely: between 0 and 0.5."))
    sec = eq("red", "blue", "blue", "red", "blue", "red", "blue", "blue", "red", "blue")
    assert amounts(sec) == {"red": 4, "blue": 6}
    its.append(mcq(F(sec) + "The spinner has 10 equal sections. What number on the probability line shows landing on red?",
                   "0.4", ["0.6", "4", "0.5"],
                   "4 of the 10 equal sections are red: 4 tenths = 0.4. 0.6 is the chance of blue. "
                   "The line only goes from 0 to 1, so 4 is not on it."))
    assert len([n for n in range(1, 7) if n < 3]) == 2
    its.append(word_q(fig(cube_faces_svg()) + "Owen rolls a number cube. Rolling a number less than 3 is …", "unlikely",
                      "Less than 3 means 1 or 2: only 2 of the 6 faces. The other 4 faces are not less than 3. "
                      "So it is unlikely, not impossible.", keep=("impossible",)))
    its.append(word_q(fig(cube_faces_svg()) + "Owen rolls a number cube. Rolling a number greater than 0 is …", "certain",
                      "Every face shows 1, 2, 3, 4, 5 or 6. All of them are greater than 0, so it is certain."))
    its.append(mcq("A spinner has 5 equal sections: 4 blue and 1 red. Aiden says landing on red is impossible, "
                   "because there is only one red section. Is he right?", "No, red is unlikely",
                   ["Yes, red is impossible", "No, red is likely", "No, red is certain"],
                   "There is a red section, so the arrow can land on it. It is not impossible. "
                   "1 of 5 sections is a small part, so red is unlikely."))
    its.append(mcq("Maya colours a spinner with 6 equal sections. She wants landing on blue to be certain. "
                   "How many sections should she colour blue?", "6", ["5", "3", "1"],
                   "Certain means it must happen, so every section must be blue: all 6. "
                   "With 5 blue sections, blue is only likely."))
    its.append(mcq("A bag has 4 red and 4 blue counters. Which change makes picking red likely, but not certain?",
                   "Add 3 red counters", ["Add 3 blue counters", "Take out 2 red counters", "Take out all 4 blue counters"],
                   "With 3 more red, there are 7 red and 4 blue: red is likely. "
                   "Taking out all the blue counters makes red certain, not just likely."))
    sec = eq("red", "blue", "red", "yellow", "red", "blue", "red", "yellow")
    assert amounts(sec) == {"red": 4, "blue": 2, "yellow": 2}
    its.append(mcq(F(sec) + "The spinner has 8 equal sections. Which two colours are equally likely?", "blue and yellow",
                   ["red and blue", "red and yellow", "all three colours"],
                   "Red has 4 sections, blue has 2 and yellow has 2. Blue and yellow cover the same amount, "
                   "so they are equally likely."))
    assert len(its) == 20
    return {"title": "Spinners and bags: look at the size of each part", "items": its}


# ------------------------------------------------------------ set 4: compare likelihood
def set_compare(rnd):
    its = []
    S = lambda spins: fig(spinners_abcd(spins))
    G = lambda bags: fig(bags_abcd(bags, rnd))
    D = [("red", 1), ("blue", 2), ("red", 1), ("blue", 2), ("red", 1), ("blue", 1)]
    assert amounts(D) == {"red": 3, "blue": 5}
    its.append(abcd_q(S([eq("red", "blue", "blue", "blue"), eq("red", "blue", "red", "blue"), [("red", 3), ("blue", 1)], D]) +
                      "On which spinner is landing on red most likely?", "Spinner", 2,
                      "Compare how much of each spinner is red. C is three quarters red. "
                      "D has 3 red sections, but they are small: together they are less than half of the spinner."))
    its.append(abcd_q(G([[("blue", 3), ("red", 3)], [("blue", 5), ("red", 1)], [("blue", 1), ("red", 5)], [("blue", 2), ("yellow", 4)]]) +
                      "From which bag is picking a blue counter least likely?", "Bag", 2,
                      "Each bag has 6 counters. Bag C has only 1 blue counter, the fewest, so blue is least likely there."))
    its.append(abcd_q(S([eq("red", "red", "red", "blue"), [("red", 2), ("blue", 1), ("yellow", 1)],
                         eq("red", "red", "blue", "yellow"), eq("red", "yellow", "blue", "yellow")]) +
                      "On which spinner are red and blue equally likely?", "Spinner", 3,
                      "On Spinner D, red and blue each cover 1 of the 4 equal sections, so they are equally likely. "
                      "On B, red and blue each have 1 section, but the red section is bigger."))
    its.append(abcd_q(G([[("red", 6)], [("red", 5), ("blue", 1)], [("red", 3), ("yellow", 3)], [("blue", 6)]]) +
                      "From which bag is picking a red counter certain?", "Bag", 0,
                      "Bag A has only red counters, so red is certain. "
                      "Bag B is likely to give red, but not certain, because it has 1 blue counter."))
    its.append(abcd_q(G([[("red", 6)], [("yellow", 1), ("red", 5)], [("yellow", 3), ("red", 3)], [("yellow", 5), ("red", 1)]]) +
                      "From which bag is picking a yellow counter unlikely, but not impossible?", "Bag", 1,
                      "Bag B has 1 yellow counter out of 6: it can happen, but probably will not. "
                      "Bag A has no yellow, so yellow is impossible there, not unlikely."))
    its.append(mcq("Bag A has 7 red and 3 blue counters. Bag B has 4 red and 6 blue counters. "
                   "From which bag is picking red more likely?", "Bag A",
                   ["Bag B", "both the same", "neither bag"],
                   "Both bags have 10 counters. Bag A has 7 red, Bag B has only 4. So red is more likely from Bag A."))
    its.append(mcq("Bag A has 5 red and 5 blue counters. Bag B has 2 red and 8 blue counters. Which sentence is true?",
                   "Red is more likely from Bag A",
                   ["Red is more likely from Bag B", "Red is equally likely from both", "Red is impossible from Bag B"],
                   "Both bags have 10 counters. Bag A has 5 red (equally likely). Bag B has only 2 red (unlikely). "
                   "So red is more likely from Bag A."))
    assert 3 * 8 == 6 * 4
    its.append(mcq("Bag A has 3 red and 1 blue counter. Bag B has 6 red and 2 blue counters. Which sentence is true?",
                   "Red is equally likely from both",
                   ["Red is more likely from Bag B", "Red is more likely from Bag A", "Red is certain from Bag B"],
                   "Bag B is just Bag A doubled: 3 red for every 1 blue. In both bags, 3 of every 4 counters are red. "
                   "More red counters does not mean more likely when there are also more blue counters."))
    assert 2 * 10 == 5 * 4
    its.append(mcq("Bag A has 2 green and 2 yellow counters. Bag B has 5 green and 5 yellow counters. "
                   "Which sentence is true?", "Green is equally likely from both",
                   ["Green is more likely from Bag B", "Green is more likely from Bag A", "Green is impossible from Bag A"],
                   "In both bags, half the counters are green. So picking green is equally likely from both bags. "
                   "Bag B has more green counters, but it also has more yellow ones."))
    assert 8 * 4 < 20 * 3
    its.append(mcq("Kai says picking red is more likely from Bag B (8 red, 12 blue) than from Bag A (3 red, 1 blue), "
                   "because Bag B has more red counters. Is he right?", "No, red is more likely from Bag A",
                   ["Yes, Bag B has more red", "No, they are equally likely", "No, red is impossible from Bag B"],
                   "Look at the whole bag. In Bag A, 3 of 4 counters are red: likely. In Bag B, 8 of 20 are red: "
                   "less than half, so unlikely. Red is more likely from Bag A."))
    its.append(mcq("Which order goes from least likely to most likely?<br>P: rolling a 7 on a number cube (1 to 6)<br>"
                   "Q: a coin landing on heads<br>R: rolling a number less than 6 on a number cube",
                   "P, Q, R", ["R, Q, P", "Q, P, R", "P, R, Q"],
                   "P is impossible (0). Q is equally likely (0.5). R: 1, 2, 3, 4 or 5 is 5 of the 6 faces, so it is likely. "
                   "Least to most likely: P, Q, R."))
    its.append(mcq("Event P is at 0.3 on the probability line. Event Q is at 0.8. Which sentence is true?",
                   "Q is more likely than P",
                   ["P is more likely than Q", "P and Q are equally likely", "Q is certain"],
                   "The closer to 1, the more likely. 0.8 is closer to 1 than 0.3, so Q is more likely. "
                   "Q is not certain, because it is not at 1."))
    its.append(mcq("Which is more likely when you roll a number cube: rolling an even number or rolling a 6?",
                   "an even number", ["a 6", "they are equally likely", "you cannot tell"],
                   "Even numbers are 2, 4 and 6: 3 faces. A 6 is only 1 face. 3 faces give a bigger chance, "
                   "so an even number is more likely."))
    its.append(mcq("Which is more likely: a coin landing on heads, or a number cube landing on 1?", "the coin landing on heads",
                   ["the cube landing on 1", "they are equally likely", "you cannot tell"],
                   "Heads is 1 of 2 sides: equally likely (0.5). A 1 is only 1 of 6 faces: unlikely. "
                   "So heads is more likely."))
    its.append(mcq("A spinner has 4 equal sections and 1 is red. A bag has 2 red and 2 blue counters. "
                   "Which is more likely: landing on red or picking a red counter?", "picking a red counter",
                   ["landing on red", "they are equally likely", "you cannot tell"],
                   "Spinner: 1 of 4 sections is red, so red is unlikely. Bag: 2 of 4 counters are red, so red is "
                   "equally likely. Picking a red counter is more likely."))
    its.append(mcq("A bag has 4 red and 4 blue counters. Compared with picking blue, picking red is …", "equally likely",
                   ["more likely", "less likely", "certain"],
                   "There are 4 red and 4 blue counters: the same number. So red and blue are equally likely."))
    sec = [("red", 4), ("blue", 1), ("blue", 1), ("blue", 1), ("blue", 1)]
    assert amounts(sec) == {"red": 4, "blue": 4}
    its.append(mcq(fig(spinner_svg(sec)) + "Compared with landing on red, landing on blue is …", "equally likely",
                   ["more likely", "less likely", "impossible"],
                   "Blue has 4 sections, but they are small. Together they cover half of the spinner. "
                   "The red section covers the other half. So blue and red are equally likely."))
    its.append(mcq("Which event is least likely?", "rolling a 1 on a number cube",
                   ["a coin landing on tails", "picking red: 3 red, 1 blue", "picking red: 2 red, 2 blue"],
                   "Rolling a 1 is 1 of 6 faces: unlikely. Tails is equally likely. 3 red and 1 blue gives a likely red. "
                   "2 red and 2 blue gives an equally likely red. So rolling a 1 is least likely."))
    its.append(mcq("Spinner A has 10 equal sections and 3 are red. Spinner B has 10 equal sections and 6 are red. "
                   "Which sentence is true?", "Red is more likely on Spinner B",
                   ["Red is more likely on Spinner A", "Red is equally likely on both", "Red is certain on Spinner B"],
                   "Spinner A: red is 0.3 on the probability line. Spinner B: red is 0.6. 0.6 is closer to 1, "
                   "so red is more likely on Spinner B."))
    its.append(mcq("Which is more likely: picking red from a bag with only red counters, or landing on red on a spinner "
                   "that is half red?", "picking red from the bag",
                   ["landing on red on the spinner", "they are equally likely", "you cannot tell"],
                   "A bag with only red counters makes red certain (1). A half red spinner makes red equally likely (0.5). "
                   "Certain is more likely than equally likely."))
    assert len(its) == 20
    return {"title": "Compare likelihood: more, less or equally likely", "items": its}


# ------------------------------------------------------------ set 5: predictions and fair games
def set_predict(rnd):
    its = []
    assert 40 // 4 == 10
    its.append(mcq(fig(spinner_svg(eq("red", "blue", "blue", "blue"))) +
                   "Hana spins this spinner 40 times. About how many times should she predict red?",
                   "about 10 times", ["about 30 times", "about 20 times", "about 4 times"],
                   "Red is 1 of 4 equal sections, so about 1 spin in every 4 is red. 40 ÷ 4 = 10. "
                   "30 is the prediction for blue, not red."))
    its.append(mcq(fig(spinner_svg(eq("red", "blue"))) + "Lucas spins this spinner 20 times. Which result would be most surprising?",
                   "red 20, blue 0", ["red 10, blue 10", "red 11, blue 9", "red 8, blue 12"],
                   "Half the spinner is red and half is blue, so you expect about 10 of each. Results near 10 are normal. "
                   "Red every single time is possible, but very unlikely."))
    its.append(mcq(fig(bag_svg([("red", 3), ("blue", 1)], rnd)) +
                   "Benjamin picks a counter, looks at it and puts it back. He does this 20 times. Which prediction is best?",
                   "red 15, blue 5", ["red 5, blue 15", "red 10, blue 10", "red 20, blue 0"],
                   "3 of the 4 counters are red, so red should come up about 3 times as often as blue. "
                   "Red 15 and blue 5 fits best. Red 20 is unlikely, because blue can be picked too."))
    maya = [16, 9, 5]
    assert sum(maya) == 30
    tf = lambda: fig(tally_svg("Maya’s 30 spins", "Colour", ["Red", "Blue", "Yellow"], maya, label="tally chart: Maya’s spins"))
    its.append(mcq(tf() + "Maya spins a spinner 30 times. Which colour will most likely come up on the next spin?", "red",
                   ["yellow, because it is due", "blue", "all are equally likely"],
                   "Red came up most often (16 times), so red probably covers the biggest part of the spinner. "
                   "Yellow is never “due”: the spinner does not remember."))
    its.append(mcq(tf() + "How many more times did red come up than yellow?", "11 times",
                   ["21 times", "5 times", "7 times"],
                   "Red 16, yellow 5. How many more means subtract: 16 − 5 = 11."))
    assert 16 - 5 == 11
    its.append(mcq("Arjun tosses a coin 5 times and gets tails every time. What about the next toss?",
                   "Heads and tails are still equally likely",
                   ["Heads is now certain", "Tails is now certain", "Tails is now impossible"],
                   "A coin does not remember what happened before. Every toss, heads and tails are equally likely."))
    its.append(mcq("A game is fair when …", "each player has the same chance to win",
                   ["the best player wins", "each player gets a turn", "the game is short"],
                   "Fair means equally likely to win. Taking turns is nice, but a game can still be unfair "
                   "if one player has a bigger chance."))
    its.append(abcd_q(fig(spinners_abcd([eq("red", "red", "red", "blue"), [("red", 1), ("blue", 1)], [("red", 1), ("blue", 2)],
                                         eq("red", "blue", "blue", "blue")])) +
                      "Zoe gets a point when the spinner lands on red. Jayden gets a point when it lands on blue. "
                      "Which spinner makes the game fair?", "Spinner", 1,
                      "On Spinner B, red and blue each cover half, so both players are equally likely to get a point. "
                      "On C, the blue part is bigger, so Jayden would have a better chance."))
    assert len([1, 2]) * 2 == len([3, 4, 5, 6])
    its.append(mcq("Arjun and Ava roll a number cube. Arjun wins on 1 or 2. Ava wins on 3, 4, 5 or 6. Is the game fair?",
                   "No, Ava is more likely to win",
                   ["Yes, it is fair", "No, Arjun is more likely to win", "No, Ava is certain to win"],
                   "Arjun wins on 2 faces and Ava wins on 4 faces. Ava has more ways to win, so the game is not fair. "
                   "Ava is not certain to win, because a 1 or 2 can be rolled."))
    its.append(mcq("Nathan wins if a number cube shows an even number. Leah wins if it shows an odd number. "
                   "Is the game fair?", "Yes, both have 3 numbers",
                   ["No, Nathan is more likely to win", "No, Leah is more likely to win", "No, nobody can win"],
                   "Even: 2, 4, 6. Odd: 1, 3, 5. Each player has 3 of the 6 faces, so they are equally likely to win. "
                   "The game is fair."))
    assert 5 == 3 + 2
    its.append(mcq("A bag has 5 red and 3 blue counters. Owen wins on red and Emma wins on blue. "
                   "How can they make the game fair?", "Add 2 blue counters",
                   ["Add 2 red counters", "Take out 3 blue counters", "Add 5 blue counters"],
                   "Fair means the same number of red and blue counters. 3 + 2 = 5 blue, the same as 5 red. "
                   "Adding 5 blue would give 8 blue: then Emma has the better chance."))
    its.append(mcq("Kai wins a prize if he picks a green counter. Bag A has 2 green and 6 yellow counters. "
                   "Bag B has 6 green and 2 yellow counters. Which bag should he choose?", "Bag B",
                   ["Bag A", "either bag, they are the same", "neither bag, green is impossible"],
                   "Both bags have 8 counters. Bag B has 6 green, Bag A has only 2. Green is likely from Bag B, "
                   "so Bag B is the better choice."))
    its.append(mcq("The forecast for Algonquin Park gives the chance of rain as 0.8 on Saturday and 0.1 on Sunday. "
                   "Sofia’s family wants a dry day for their canoe trip. Which day should they choose?", "Sunday",
                   ["Saturday", "either day, they are the same", "neither day, rain is certain"],
                   "0.1 is close to 0, so rain on Sunday is unlikely. 0.8 is close to 1, so rain on Saturday is likely. "
                   "Sunday is the better choice."))
    its.append(word_q("At the school fun fair, 200 raffle tickets are sold. Ethan buys 2 tickets. "
                      "Ethan winning the raffle is …", "unlikely",
                      "Ethan has only 2 of the 200 tickets. He could win, but it is unlikely.", keep=("impossible",)))
    assert 60 // 6 == 10
    its.append(mcq("Priya rolls a number cube 60 times. About how many times should she predict a 6?", "about 10 times",
                   ["about 6 times", "about 30 times", "about 50 times"],
                   "Each of the 6 faces is equally likely, so about 1 roll in every 6 is a 6. 60 ÷ 6 = 10. "
                   "About 50 is the prediction for not getting a 6."))
    its.append(mcq("Benjamin picks a counter from a bag, looks at it and puts it back. He does this 20 times. "
                   "He gets red 4 times and blue 16 times. Which bag did he most likely use?", "2 red, 8 blue",
                   ["8 red, 2 blue", "5 red, 5 blue", "0 red, 10 blue"],
                   "Blue came up much more often than red, so the bag probably has many more blue counters. "
                   "It cannot be 0 red, because then red would be impossible, and he picked red 4 times."))
    its.append(mcq("Mei tosses a coin 10 times. She gets 6 heads and 4 tails. Which sentence is true?",
                   "This is normal: results vary", ["The coin must be unfair", "Heads is now certain", "Tails is due next"],
                   "Heads and tails are equally likely, so you expect about 5 of each. Real results vary a little: "
                   "6 and 4 is close to 5 and 5."))
    its.append(mcq("Liam wins if the spinner lands on red. Spinner A is half red. Spinner B has 4 equal sections, "
                   "and 1 is red. Which spinner should he choose?", "Spinner A",
                   ["Spinner B", "either spinner, they are the same", "neither, red is impossible"],
                   "On Spinner A, red is equally likely (0.5). On Spinner B, red is only 1 of 4 sections: unlikely. "
                   "Spinner A gives Liam the better chance."))
    assert 100 // 10 * 7 == 70
    its.append(mcq("Chloe’s spinner has 10 equal sections: 7 green and 3 yellow. She spins it 100 times. "
                   "About how many times should she predict green?", "about 70 times",
                   ["about 30 times", "about 7 times", "about 100 times"],
                   "Green is 7 of every 10 sections, so predict about 7 green in every 10 spins. "
                   "100 spins is 10 groups of 10: 10 × 7 = 70. 30 is the prediction for yellow."))
    assert 9 + 3 == 12
    its.append(mcq("A box has 12 granola bars: 9 chocolate chip and 3 oatmeal. Leah takes one without looking. "
                   "Where on the probability line does “getting chocolate chip” go?", "between 0.5 and 1",
                   ["at 1", "between 0 and 0.5", "at 0.5"],
                   "9 of the 12 bars are chocolate chip. Half of 12 is 6, and 9 is more than 6, so it is likely. "
                   "It is not certain (1), because there are oatmeal bars too."))
    assert len(its) == 20
    return {"title": "Predictions and fair games", "items": its}


# ------------------------------------------------------------ lesson
def body_html(rnd):
    return (
        "<h2>The five probability words</h2>"
        "<p>Probability tells us how likely something is to happen. "
        "<b>Impossible</b> means it can never happen. <b>Certain</b> means it must happen. "
        "<b>Unlikely</b> means it could happen, but probably will not. <b>Likely</b> means it will probably happen. "
        "<b>Equally likely</b> means it is just as likely to happen as not to happen.</p>" +
        table(["Word", "Meaning", "Example"], [
            ["impossible", "can never happen", "rolling a 7 on a number cube (1 to 6)"],
            ["unlikely", "could happen, but probably will not", "finding a toonie on the sidewalk"],
            ["equally likely", "same chance to happen or not", "a coin landing on heads"],
            ["likely", "will probably happen", "snow on the ground in Winnipeg in January"],
            ["certain", "must happen", "Thanksgiving in October"],
        ]) +
        "<h2>The probability line</h2>"
        "<p>A probability line goes from <b>0</b> to <b>1</b>. Impossible events go at 0. Certain events go at 1. "
        "Equally likely events go halfway, at 0.5. Unlikely events go between 0 and 0.5. "
        "Likely events go between 0.5 and 1.</p>"
        "<figure class='sn-fig'>" + pline_svg([(2, "A"), (5, "B"), (9, "C")], five=True,
                                               label="probability line from 0 to 1 with the five words") +
        "<figcaption>A: unlikely. B: equally likely. C: likely.</figcaption></figure>" +
        ex("Example", "A spinner has 10 equal sections. 7 are green. Where does landing on green go on the line?",
           "7 of 10 equal sections is 7 tenths. Count 7 steps from 0.", "0.7, between 0.5 and 1 (likely)") +
        "<h2>Spinners and bags: look at the size of each part</h2>"
        "<p>A spinner is more likely to land on a colour that covers <b>more</b> of it. "
        "Compare the size of the parts, not just the number of sections. In a bag, the colour with more counters is more likely.</p>"
        "<figure class='sn-fig'>" + spinner_svg([("yellow", 4), ("red", 1), ("blue", 1), ("red", 1), ("blue", 1)],
                                                  "spinner: yellow half, 2 small red and 2 small blue sections") +
        "<figcaption>Red and blue have 2 sections each, but yellow covers half of the spinner.</figcaption></figure>" +
        ex("Example", "Which colour is the arrow most likely to land on?",
           "Yellow is one big section: half of the spinner. Red covers a quarter, and so does blue.", "yellow") +
        "<h2>Compare likelihood</h2>"
        "<p>To compare two events, look at the part of the whole for each one. "
        "The event closer to 1 on the probability line is more likely.</p>" +
        ex("Example", "Bag A has 3 red and 1 blue counter. Bag B has 3 red and 7 blue counters. Where is red more likely?",
           "Bag A: 3 of 4 are red, more than half. Bag B: 3 of 10 are red, less than half.", "Bag A") +
        "<h2>Predictions and fair games</h2>"
        "<p>Use the chance to predict. If red is 1 of 4 equal sections, predict red about 1 time in every 4 spins. "
        "Real results <b>vary</b> a little each time. A game is <b>fair</b> when every player has the same chance to win.</p>"
        "<figure class='sn-fig'>" + cube_faces_svg() +
        "<figcaption>The 6 faces of a number cube. Each face is equally likely.</figcaption></figure>" +
        ex("Example", "Nathan wins on an even number. Leah wins on an odd number. Is the game fair?",
           "Even: 2, 4, 6. Odd: 1, 3, 5. Each player has 3 of the 6 faces.", "Yes, it is fair") +
        "<h2>Common mistakes</h2>" +
        table(["Mistake", "What to do instead"], [
            ["Saying certain when it is only likely", "Certain means it must happen. If it could fail, it is likely (between 0.5 and 1)"],
            ["Saying impossible when it is only unlikely", "If it could happen even once, it is not impossible and does not go at 0"],
            ["Counting sections, not their size", "Compare how much of the spinner each colour covers"],
            ["Thinking more red counters always means more likely", "Look at the whole bag: 3 of 4 is more likely than 8 of 20"],
            ["Thinking a colour is “due” after it has not come up", "A spinner or coin does not remember: the chance stays the same"],
        ])
    )


FAQ = [
    {"q": "What do Grade 4 students learn about probability in Ontario?",
     "a": "In the Ontario Mathematics Curriculum (2020), expectation D2.1, Grade 4 students use the words impossible, unlikely, equally likely, likely and certain, place events on a probability line from 0 to 1, and use the likelihood to make predictions and decisions."},
    {"q": "What is a probability line?",
     "a": "A probability line is a number line from 0 to 1. Impossible events go at 0, certain events go at 1 and equally likely events go halfway, at 0.5."},
    {"q": "What is the difference between likely and certain?",
     "a": "Likely means it will probably happen, but it might not, like picking red from a bag with 9 red counters and 1 blue. Certain means it must happen, like picking red from a bag with only red counters."},
    {"q": "How do you know if a game is fair?",
     "a": "A game is fair when every player has the same chance to win. For example, one player wins on an even number and the other on an odd number: each has 3 of the 6 faces of a number cube."},
]


def gen_unit():
    rnd = random.Random(44812)
    sets = [set_words(rnd), set_line(rnd), set_spin_bag(rnd), set_compare(rnd), set_predict(rnd)]
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
        "country": "ca-on", "subject": "math", "grade": "grade-4", "slug": "probability", "sort": 12,
        "updated": UPDATED, "pdf_url": "",
        "title": "Probability: Likelihood Words and the Probability Line",
        "seo_title": "Grade 4 Probability Worksheets: Probability Line and Likelihood (Free, with Answer Key)",
        "short_title": "Probability",
        "domain": "Data",
        "standard_code": "Grade 4: D2.1",
        "standard_url": "https://www.dcp.edu.gov.on.ca/en/curriculum/elementary-mathematics",
        "standard_text": "Use mathematical language, including the terms “impossible”, “unlikely”, “equally likely”, “likely”, and “certain”, to describe the likelihood of events happening, represent this likelihood on a probability line, and use it to make predictions and informed decisions",
        "meta_desc": "Free Grade 4 math worksheets on probability: describe events as impossible, unlikely, equally likely, likely or certain, place them on a probability line from 0 to 1, compare spinners and bags of counters, make predictions and decide if a game is fair. 100 questions with an answer key, following the Ontario curriculum (D2.1).",
        "key_big": "Impossible is 0, certain is 1, and equally likely is halfway at 0.5.",
        "key_sub": "Likely events go between 0.5 and 1, unlikely events between 0 and 0.5. Look at the size of each part of a spinner or bag, not just the number of sections.",
        "body_html": body_html(rnd), "faq": FAQ, "sets": sets,
    }


# ------------------------------------------------------------ lesson
def ex(title, q, s, a):
    return ("<div class='sn-ex'><span class='sn-ex-t'>%s</span><p class='sn-ex-q'>%s</p>"
            "<p class='sn-ex-s'>%s</p><p class='sn-ex-a'>Answer: %s</p></div>" % (title, q, s, a))


def table(head, rows, cls="sn-table"):
    h = "".join("<th>%s</th>" % x for x in head)
    b = "".join("<tr>" + "".join("<td>%s</td>" % c for c in r) + "</tr>" for r in rows)
    return "<div class='sn-tw'><table class='%s'><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>" % (cls, h, b)


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
    mark_large(u, "(spinners A to D|bags A to D|tally chart|the six faces|probability line)")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
