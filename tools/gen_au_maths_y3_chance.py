# -*- coding: utf-8 -*-
"""
Australia Year 3 Maths: Chance (Australian Curriculum v9.0: AC9M3P01, AC9M3P02)
  python3 tools/gen_au_maths_y3_chance.py
Everyday events, spinners, bags of counters, possible outcomes (dice, coins, number cards)
and repeated chance experiments with tally charts and tables.
Only the words certain, likely, unlikely, impossible (and "equally likely").
Wrong answers come from real student mistakes: unlikely confused with impossible, judging by a favourite
colour, thinking a bigger number on a dice is harder to roll, counting sections instead of looking at their
size, expecting the same results every time, and "it is due" thinking after a run of heads.
Every picture shows the colour as a letter too (R = red ...), so it still works when printed in black and white.
HTML attributes use single quotes (no backslashes in the JSON). Australian English.
"""
import json, re, math, os, random

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "au", "maths", "year-3")
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


# ------------------------------------------------------------ set 1: everyday events
def set_everyday(rnd):
    its = []
    its.append(word_q("The sun will rise tomorrow morning. This is …", "certain",
                      "The sun rises every morning. It always happens, so it is certain."))
    its.append(word_q("It will snow in Darwin this summer. This is …", "impossible",
                      "Darwin is in the hot tropical north. Summer there is hot and wet, and snow does not fall in Darwin, so it is impossible."))
    its.append(word_q("After Wednesday, the next day will be Thursday. This is …", "certain",
                      "The days of the week always come in the same order. Thursday always comes after Wednesday, so it is certain."))
    its.append(word_q("A kangaroo will fly over the school like a bird. This is …", "impossible",
                      "Kangaroos hop, but they cannot fly. This can never happen, so it is impossible."))
    its.append(word_q("Oliver is 8. Next year he will be 9. This is …", "certain",
                      "Everyone is one year older each year. 8 + 1 = 9, so it is certain."))
    its.append(word_q("Tomorrow will have 30 hours. This is …", "impossible",
                      "Every day has 24 hours. A day can never have 30 hours, so it is impossible."))
    its.append(word_q("It will be cold on a winter morning in Canberra. This is …", "likely",
                      "Canberra winter mornings are usually very cold, often below 0 °C. Most of the time this happens, "
                      "but a mild morning is possible, so it is likely, not certain."))
    its.append(word_q("Mia will find a $50 note on the way to school. This is …", "unlikely",
                      "It could happen, but it almost never does. So it is unlikely. It is not impossible: notes do get dropped."))
    its.append(word_q("It will be warm on a January day at the beach in Sydney. This is …", "likely",
                      "January is summer in Australia, so most days are warm. A few days can be cool or rainy, "
                      "so it is likely, not certain."))
    its.append(word_q("A koala will walk into the classroom today. This is …", "unlikely",
                      "Koalas live in trees in the bush. One could wander into a school, but it hardly ever happens. "
                      "So it is unlikely, not impossible."))
    its.append(word_q("If Isla drops a tennis ball, it will fall down. This is …", "certain",
                      "When you let go of a ball, it always falls to the ground. It must happen, so it is certain."))
    its.append(word_q("It will rain every day in January in Perth. This is …", "unlikely",
                      "January is summer in Perth. Most January days are dry and sunny, so rain on every single day is unlikely."))
    its.append(word_q("Leo is 8. Next year he will be 3 years old. This is …", "impossible",
                      "You cannot get younger. Next year Leo will be 9, so being 3 is impossible."))
    its.append(word_q("The next vehicle that drives past the school will have 4 wheels. This is …", "likely",
                      "Most vehicles on the road are cars with 4 wheels. But the next one could be a motorbike or a truck, "
                      "so it is likely, not certain."))
    its.append(word_q("Ruby will drink some water at school today. This is …", "likely",
                      "Most students drink water during a school day. Ruby could forget, so it is likely, not certain."))
    its.append(word_q("Jack will roll a 6 on a dice five times in a row. This is …", "unlikely",
                      "Rolling a 6 once is unlikely (1 out of 6 faces). Five 6s in a row is even harder. "
                      "It could happen, so it is unlikely, not impossible."))
    its.append(mcq("Which event is certain?", "Friday will come after Thursday",
                   ["It will rain tomorrow", "Ava will win her race at the athletics carnival", "Kai will have pasta for dinner"],
                   "Friday always comes after Thursday, so it is certain. Rain, winning a race and pasta for dinner "
                   "might happen, but they might not."))
    its.append(mcq("Which event is impossible?", "A cat will fly to the Moon",
                   ["Grace will lose a tooth this year", "Lachlan will see a bird today", "It will be sunny on Saturday"],
                   "A cat cannot fly, and it cannot get to the Moon, so this can never happen. "
                   "The other events could happen."))
    its.append(mcq("Which event is unlikely?", "A snake will be found in the school library",
                   ["The sun will set tonight", "A fish will ride a bike", "Students will eat lunch at school today"],
                   "A snake in the library could happen, but it is rare, so it is unlikely. "
                   "The sun setting is certain, a fish riding a bike is impossible, and students eating lunch is likely."))
    its.append(word_q("Only 2 of the 20 students will be picked for the netball team. Chloe says, “It is impossible that I will be picked.” "
                      "Which word should she use instead?", "unlikely",
                      "2 of the 20 students will be picked, so Chloe could be one of them. "
                      "It is possible, but not very likely. The right word is unlikely, not impossible."))
    assert len(its) == 20
    return {"title": "Everyday events: certain, likely, unlikely or impossible?", "items": its}


# ------------------------------------------------------------ set 2: spinners
def set_spinners(rnd):
    its = []
    F = lambda sec: fig(spinner_svg(sec))
    its.append(mcq(F(eq("red", "red", "blue", "red")) + "The spinner has 4 equal sections. Which colour is the arrow most likely to land on?",
                   "red", ["blue", "red and blue are equally likely", "green"],
                   "3 of the 4 equal sections are red and only 1 is blue, so red is most likely. "
                   "(There is no green, so green is impossible.)"))
    its.append(mcq(F(eq("yellow", "yellow", "green", "yellow", "yellow", "yellow")) +
                   "The spinner has 6 equal sections. Which colour is the arrow least likely to land on?",
                   "green", ["yellow", "both colours are equally likely", "it always lands on green"],
                   "Only 1 of the 6 equal sections is green. 5 are yellow. Green has the smallest part, so it is least likely."))
    its.append(word_q(F(eq("red", "red", "red", "red")) + "Landing on red is …", "certain",
                      "Every section is red. The arrow must land on red, so it is certain."))
    sec = eq("red", "blue", "blue", "blue", "blue", "blue")
    assert chance_word(amounts(sec)["red"], 6) == "unlikely"
    its.append(word_q(F(sec) + "Landing on red is …", "unlikely",
                      "Only 1 of the 6 equal sections is red. It can happen, but not often, so it is unlikely. "
                      "It is not impossible, because there is a red section."))
    its.append(word_q(F(eq("red", "blue", "yellow", "blue", "red", "yellow")) + "Landing on green is …", "impossible",
                      "There is no green section on this spinner. The arrow can never land on green, so it is impossible."))
    sec = eq("green", "green", "purple", "green", "green", "green")
    assert chance_word(amounts(sec)["green"], 6) == "likely"
    its.append(word_q(F(sec) + "Landing on green is …", "likely",
                      "5 of the 6 equal sections are green, so green is likely. "
                      "It is not certain, because there is 1 purple section."))
    its.append(mcq(F(eq("red", "blue", "yellow", "red")) + "Which colour can the arrow never land on?",
                   "green", ["red", "blue", "yellow"],
                   "The spinner has red, blue and yellow sections only. There is no green, so landing on green is impossible."))
    sec = [("blue", 4), ("red", 1), ("yellow", 1), ("red", 1), ("yellow", 1)]
    am = amounts(sec)
    assert am["blue"] == 4 and am["red"] == 2 and am["yellow"] == 2
    its.append(mcq(F(sec) + "Which colour is the arrow most likely to land on?",
                   "blue", ["red", "yellow", "all three colours are equally likely"],
                   "Look at the size of each part, not the number of sections. Blue is one big section: half of the spinner. "
                   "Red is 2 small sections (a quarter) and yellow is 2 small sections (a quarter). So blue is most likely."))
    its.append(mcq(F([("yellow", 2), ("red", 1), ("green", 1)]) + "Which two colours are equally likely?",
                   "red and green", ["yellow and red", "yellow and green", "all three colours"],
                   "Red and green are each a quarter of the spinner. Parts of the same size are equally likely. "
                   "Yellow is half of the spinner, so it is more likely than red or green."))
    its.append(word_q(F([("green", 3), ("yellow", 1)]) + "Landing on yellow is …", "unlikely",
                      "Yellow is only a quarter of the spinner and green is three quarters. "
                      "Yellow can happen, but it is unlikely."))
    its.append(mcq(F(eq(*range(1, 9))) + "The spinner has 8 equal sections. Which number is the arrow most likely to land on?",
                   "all the numbers are equally likely", ["8", "1", "4"],
                   "All 8 sections are the same size, so each number has the same chance. "
                   "A bigger number is not harder or easier to get."))
    its.append(word_q(F([("1", 4), ("2", 2), ("3", 1), ("4", 1)]) + "Landing on a number less than 5 is …", "certain",
                      "The numbers on the spinner are 1, 2, 3 and 4. They are all less than 5, so it is certain."))
    its.append(word_q(F(eq(*range(1, 7))) + "Landing on 7 is …", "impossible",
                      "The numbers go from 1 to 6. There is no 7 on the spinner, so it is impossible."))
    S = lambda spins: fig(spinners_abcd(spins))
    its.append(abcd_q(S([eq("blue", "red", "blue", "red"), eq("blue", "blue", "blue", "blue"),
                         eq("blue", "blue", "blue", "yellow"), eq("red", "yellow", "green", "red")]) +
                      "Which spinner is certain to land on blue?", "Spinner", 1,
                      "Spinner B is all blue, so it must land on blue. Spinner C is likely to land on blue, "
                      "but it could land on yellow, so it is not certain."))
    its.append(abcd_q(S([eq("red", "blue", "blue", "blue"), eq("red", "red", "blue", "yellow"),
                         eq("red", "red", "red", "red"), eq("blue", "yellow", "green", "yellow")]) +
                      "On which spinner is landing on red impossible?", "Spinner", 3,
                      "Spinner D has no red section, so red is impossible there. "
                      "Spinner A has 1 red section: red is unlikely there, but not impossible."))
    D = [("red", 1), ("blue", 1), ("red", 1), ("blue", 1), ("red", 1), ("blue", 3)]
    assert amounts(D)["red"] == 3 and sum(u for _, u in D) == 8
    its.append(abcd_q(S([eq("red", "blue", "blue", "blue"), eq("red", "blue", "red", "blue"), [("red", 3), ("blue", 1)], D]) +
                      "On which spinner is landing on red most likely?", "Spinner", 2,
                      "Compare how much of each spinner is red. C is three quarters red. "
                      "D has 3 red sections, but they are small: together they are less than half of the spinner."))
    its.append(abcd_q(S([[("red", 1), ("blue", 1)], eq("red", "red", "red", "blue"), [("red", 2), ("blue", 1), ("yellow", 1)],
                         eq("red", "blue", "blue", "red", "blue", "blue")]) +
                      "On which spinner are red and blue equally likely?", "Spinner", 0,
                      "Spinner A is half red and half blue, so red and blue are equally likely. "
                      "In C, red and blue each have 1 section, but the red section is bigger, so red is more likely there."))
    its.append(mcq("Ethan colours a spinner with 4 equal sections. He wants landing on red to be unlikely, but not impossible. "
                   "How many sections should he colour red?", "1 section",
                   ["0 sections", "3 sections", "4 sections"],
                   "1 red section out of 4 makes red unlikely. 0 red sections would make red impossible. "
                   "3 would make it likely, and 4 would make it certain."))
    sec = eq("green", "green", "yellow", "green", "green", "green", "yellow", "green")
    assert amounts(sec) == {"green": 6, "yellow": 2}
    its.append(mcq(F(sec) + "Sienna says the arrow will probably land on yellow, because yellow is her favourite colour. "
                   "Which colour is the arrow more likely to land on?", "green",
                   ["yellow", "both colours are equally likely", "it is certain to land on yellow"],
                   "Your favourite colour does not change the chance. 6 of the 8 equal sections are green and 2 are yellow, "
                   "so green is more likely."))
    sec = eq("red", "blue", "red", "yellow", "red", "blue")
    assert amounts(sec) == {"red": 3, "blue": 2, "yellow": 1}
    its.append(mcq(F(sec) + "Put the colours in order from most likely to least likely.", "red, blue, yellow",
                   ["yellow, blue, red", "blue, red, yellow", "red, yellow, blue"],
                   "Count the equal sections: red 3, blue 2, yellow 1. The most sections is most likely, "
                   "so the order is red, blue, yellow."))
    assert len(its) == 20
    return {"title": "Spinners: which colour is most likely?", "items": its}


# ------------------------------------------------------------ set 3: bags of counters
def set_bags(rnd):
    its = []
    B = lambda counts, lab="bag of counters": fig(bag_svg(counts, rnd, lab))
    its.append(mcq(B([("red", 6), ("blue", 2)]) + "Zara picks one counter from the bag without looking. "
                   "Which colour is she most likely to pick?", "red",
                   ["blue", "red and blue are equally likely", "yellow"],
                   "There are 6 red counters and only 2 blue counters. More red counters means red is more likely."))
    its.append(mcq(B([("yellow", 7), ("green", 1)]) + "Noah picks one counter without looking. Which colour is he least likely to pick?",
                   "green", ["yellow", "both colours are equally likely", "he will always pick green"],
                   "There is only 1 green counter and 7 yellow counters, so green is least likely."))
    its.append(word_q(B([("blue", 8)]) + "Picking a blue counter from this bag is …", "certain",
                      "Every counter in the bag is blue, so you must pick blue. It is certain."))
    its.append(word_q(B([("red", 5), ("yellow", 3)]) + "Picking a green counter from this bag is …", "impossible",
                      "There are only red and yellow counters. There is no green counter, so it is impossible."))
    assert chance_word(7, 8) == "likely" and chance_word(1, 10) == "unlikely"
    its.append(word_q(B([("red", 7), ("blue", 1)]) + "Picking a red counter from this bag is …", "likely",
                      "7 of the 8 counters are red, so red is likely. It is not certain, because there is 1 blue counter."))
    its.append(word_q(B([("red", 1), ("blue", 9)]) + "Picking a red counter from this bag is …", "unlikely",
                      "Only 1 of the 10 counters is red. It can happen, but not often, so it is unlikely, not impossible."))
    its.append(mcq(B([("red", 4), ("blue", 3), ("yellow", 1)]) + "Which colour is impossible to pick from this bag?",
                   "green", ["yellow", "blue", "red"],
                   "The bag has red, blue and yellow counters. There is no green, so green is impossible. "
                   "There is 1 yellow counter, so yellow is unlikely, not impossible."))
    its.append(mcq(B([("red", 4), ("blue", 4)]) + "Which sentence is true?", "Red and blue are equally likely",
                   ["Red is more likely than blue", "Picking blue is certain", "Picking red is impossible"],
                   "There are 4 red and 4 blue counters. The same number of each colour means they are equally likely."))
    its.append(word_q(B([("green", 9), ("purple", 1)], "bag of marbles") + "This bag has 9 green marbles and 1 purple marble. "
                      "Harper picks one marble without looking. Picking the purple marble is …", "unlikely",
                      "Only 1 of the 10 marbles is purple. It can happen, but it is unlikely."))
    its.append(mcq(B([("red", 3), ("blue", 3), ("yellow", 2)]) + "Which two colours are equally likely to be picked?",
                   "red and blue", ["red and yellow", "blue and yellow", "all three colours"],
                   "There are 3 red, 3 blue and 2 yellow counters. Red and blue have the same number, so they are equally likely."))
    its.append(mcq(B([("yellow", 5), ("red", 2), ("green", 1)]) + "Put the colours in order from most likely to least likely.",
                   "yellow, red, green", ["green, red, yellow", "red, yellow, green", "yellow, green, red"],
                   "Count each colour: yellow 5, red 2, green 1. The most counters is most likely: yellow, red, green."))
    its.append(word_q(B([("red", 3), ("blue", 5)]) + "Mei takes all the blue counters out of the bag. "
                      "Now picking a red counter is …", "certain",
                      "After the blue counters come out, only the 3 red counters are left. You must pick red, so it is certain."))
    assert 2 + 6 > 6
    its.append(mcq(B([("red", 6), ("green", 2)]) + "Kai puts 6 more green counters into the bag. "
                   "Which colour is now more likely to be picked?", "green",
                   ["red", "they are equally likely", "green is impossible"],
                   "Green: 2 + 6 = 8 counters. Red: 6 counters. 8 is more than 6, so green is now more likely."))
    G = lambda bags: fig(bags_abcd(bags, rnd))
    its.append(abcd_q(G([[("red", 3), ("blue", 3)], [("red", 5), ("blue", 1)], [("yellow", 4), ("blue", 2)], [("red", 6)]]) +
                      "Which bag makes picking a red counter certain?", "Bag", 3,
                      "Bag D has only red counters, so red is certain. "
                      "Bag B is likely to give red, but not certain, because it has 1 blue counter."))
    its.append(abcd_q(G([[("red", 4), ("blue", 2)], [("yellow", 1), ("red", 5)], [("yellow", 3), ("blue", 3)], [("yellow", 6)]]) +
                      "From which bag is picking a yellow counter impossible?", "Bag", 0,
                      "Bag A has no yellow counters, so yellow is impossible. "
                      "Bag B has 1 yellow counter, so yellow is unlikely there, not impossible."))
    its.append(abcd_q(G([[("blue", 1), ("red", 5)], [("blue", 5), ("red", 1)], [("blue", 3), ("red", 3)], [("blue", 2), ("red", 4)]]) +
                      "From which bag is picking a blue counter most likely?", "Bag", 1,
                      "Each bag has 6 counters. Bag B has the most blue counters (5), so blue is most likely there."))
    its.append(abcd_q(G([[("red", 6)], [("red", 4), ("blue", 2)], [("red", 1), ("blue", 5)], [("blue", 6)]]) +
                      "From which bag is picking a red counter unlikely (but not impossible)?", "Bag", 2,
                      "Bag C has only 1 red counter out of 6, so red is unlikely. "
                      "Bag D has no red, so red is impossible there. A is certain and B is likely."))
    its.append(mcq("Ruby’s bag has 3 red counters and 2 blue counters. She wants picking a blue counter to be impossible. "
                   "What should she do?", "Take out the 2 blue counters",
                   ["Take out the 3 red counters", "Add 2 more red counters", "Take out 1 blue counter"],
                   "Impossible means it can never happen. If there are no blue counters left, blue can never be picked. "
                   "Adding red counters only makes blue unlikely."))
    its.append(mcq("A bag has 10 counters. Picking a red counter is certain. How many red counters are in the bag?",
                   "10", ["9", "5", "1"],
                   "Certain means it must happen, so every counter must be red: all 10. "
                   "With 9 red and 1 other counter, red is likely, not certain."))
    its.append(mcq("At the school fete lucky dip there are 20 prizes: 15 lolly bags, 4 pencils and 1 toy car. "
                   "Grace picks one prize without looking. Which prize is she most likely to get?", "a lolly bag",
                   ["the toy car", "a pencil", "they are all equally likely"],
                   "15 of the 20 prizes are lolly bags. That is more than all the others, so a lolly bag is most likely. "
                   "There is only 1 toy car, so it is unlikely."))
    assert len(its) == 20
    return {"title": "Bags of counters: what could you pick?", "items": its}


# ------------------------------------------------------------ set 4: possible outcomes
def set_outcomes(rnd):
    its = []
    its.append(mcq("Isla tosses a coin. What are the possible outcomes?", "heads or tails",
                   ["heads only", "tails only", "1, 2, 3, 4, 5 or 6"],
                   "A coin has two sides: heads and tails. It can land on either one, so the outcomes are heads or tails."))
    its.append(mcq("Oliver rolls a dice. What are all the possible outcomes?", "1, 2, 3, 4, 5, 6",
                   ["1, 2, 3, 4, 5", "0, 1, 2, 3, 4, 5, 6", "6 only"],
                   "A dice has 6 faces with 1 to 6 dots. Any face can land on top: 1, 2, 3, 4, 5 or 6. There is no 0."))
    its.append(mcq("How many different outcomes are there when you roll a dice?", "6", ["5", "7", "12"],
                   "The outcomes are 1, 2, 3, 4, 5 and 6. That is 6 outcomes."))
    its.append(mcq("Which number is impossible to roll on a dice?", "7", ["1", "3", "6"],
                   "A dice shows 1 to 6. There is no 7, so rolling a 7 is impossible."))
    its.append(word_q("Rolling a number less than 7 on a dice is …", "certain",
                      "Every number on a dice (1, 2, 3, 4, 5, 6) is less than 7. It must happen, so it is certain."))
    its.append(word_q("Rolling a number greater than 6 on a dice is …", "impossible",
                      "The biggest number on a dice is 6. You can never roll more than 6, so it is impossible."))
    assert chance_word(1, 6) == "unlikely" and chance_word(5, 6) == "likely"
    its.append(word_q("Rolling a 6 on a dice is …", "unlikely",
                      "Only 1 of the 6 faces shows 6. It can happen, but it is unlikely."))
    its.append(word_q("Rolling a number greater than 1 on a dice is …", "likely",
                      "5 of the 6 faces are greater than 1 (2, 3, 4, 5, 6). Only the 1 is not. So it is likely."))
    its.append(mcq("Noah thinks a 6 is harder to roll than a 1, because 6 is a bigger number. Is he right?",
                   "No, 1 and 6 are equally likely", ["Yes, 6 is less likely", "No, 6 is more likely", "Yes, 6 is impossible"],
                   "Each face of a dice has the same chance. The size of the number does not matter. "
                   "1 and 6 are each 1 face out of 6, so they are equally likely."))
    its.append(mcq("Charlotte tosses a coin. Getting heads is …", "as likely as tails",
                   ["more likely than tails", "certain", "impossible"],
                   "A coin has one heads side and one tails side, so heads and tails are equally likely."))
    sec = eq("red", "red", "blue", "green")
    assert len(amounts(sec)) == 3
    its.append(mcq(fig(spinner_svg(sec)) + "How many different outcomes (colours) can this spinner land on?", "3",
                   ["4", "2", "1"],
                   "The spinner has 4 sections, but two of them are red. The different colours are red, blue and green: "
                   "3 outcomes. (Counting sections gives 4.)"))
    its.append(mcq("Matilda has number cards from 1 to 10. She turns them face down and picks one. "
                   "Which number is impossible to pick?", "11", ["1", "5", "10"],
                   "The cards go from 1 to 10. There is no 11 card, so 11 is impossible."))
    its.append(word_q("Number cards 1 to 10 are face down. Picking a number less than 11 is …", "certain",
                      "Every card from 1 to 10 is less than 11. It must happen, so it is certain."))
    assert chance_word(8, 10) == "likely"
    its.append(word_q("Number cards 1 to 10 are face down. Picking a number greater than 2 is …", "likely",
                      "8 of the 10 cards are greater than 2 (3 to 10). Only 1 and 2 are not. So it is likely."))
    its.append(word_q("Number cards 1 to 10 are face down. Picking the 10 is …", "unlikely",
                      "There is only 1 card with 10 on it, out of 10 cards. It can happen, but it is unlikely."))
    assert {2, 4, 6} and len([n for n in range(1, 7) if n % 2 == 0]) == 3
    its.append(mcq("Rolling an even number on a dice is …", "as likely as rolling an odd number",
                   ["more likely than rolling an odd number", "less likely than rolling an odd number", "impossible"],
                   "Even numbers: 2, 4, 6 (3 faces). Odd numbers: 1, 3, 5 (3 faces). 3 and 3 are the same, so they are equally likely."))
    its.append(mcq("Aarav rolls a dice. Which is most likely?", "rolling a number less than 5",
                   ["rolling a 6", "rolling a 1 or a 2", "rolling a 7"],
                   "Less than 5: 1, 2, 3, 4 (4 faces). A 6 is 1 face, a 1 or a 2 is 2 faces, and 7 is impossible. "
                   "4 faces is the most, so a number less than 5 is most likely."))
    its.append(mcq(fig(spinner_svg(eq(1, 2, 3, 4))) + "Leo spins this spinner. Which outcome is impossible?", "landing on 5",
                   ["landing on 1", "landing on 4", "landing on 2"],
                   "The spinner has 1, 2, 3 and 4. There is no 5, so landing on 5 is impossible."))
    its.append(mcq("Which is certain when you toss a coin?", "It lands on heads or tails",
                   ["It lands on heads", "It lands on tails", "It lands on the number 6"],
                   "Heads alone or tails alone might not happen. But the coin must land on heads or tails, so that is certain."))
    assert chance_word(2, 6) == "unlikely"
    its.append(word_q("Rolling a 3 or a 4 on a dice is …", "unlikely",
                      "Only 2 of the 6 faces (3 and 4) work. 4 faces do not. It can happen, but it is unlikely."))
    assert len(its) == 20
    return {"title": "Dice, coins and number cards: possible outcomes", "items": its}


# ------------------------------------------------------------ set 5: experiments and word problems
def set_experiments(rnd):
    its = []
    mia = [9, 7, 4]
    assert sum(mia) == 20
    tf = fig(tally_svg("Mia’s 20 spins", "Colour", ["Red", "Blue", "Yellow"], mia, label="tally chart: Mia's spins"))
    its.append(mcq(tf + "Which colour came up most often?", "red", ["yellow", "blue", "they all came up the same"],
                   "Red: 1 group of 5 and 4 more = 9. Blue: 7. Yellow: 4. Red has the most tally marks."))
    its.append(mcq(tf + "How many times did Mia spin altogether?", "20 times", ["3 times", "9 times", "16 times"],
                   "Add the tallies: 9 + 7 + 4 = 20."))
    its.append(mcq(tf + "How many more times did red come up than yellow?", "5 times", ["13 times", "2 times", "4 times"],
                   "Red 9, yellow 4. How many more means subtract: 9 − 4 = 5."))
    its.append(mcq(fig(spinner_svg(eq("red", "blue"))) + "Jack spins this spinner 20 times. Which result would be most surprising?",
                   "red 20, blue 0", ["red 10, blue 10", "red 11, blue 9", "red 8, blue 12"],
                   "Half the spinner is red and half is blue, so you expect about 10 of each. Results near 10 are normal. "
                   "Red every single time is possible, but very unlikely."))
    sec = eq("blue", "blue", "red", "blue")
    its.append(mcq(fig(spinner_svg(sec)) + "William spins this spinner 20 times. Which result is most likely?",
                   "blue 15, red 5", ["blue 5, red 15", "blue 10, red 10", "blue 20, red 0"],
                   "3 of the 4 equal sections are blue, so blue should come up about 3 times as often as red. "
                   "Blue 15 and red 5 fits best. The results can change a little each time."))
    its.append(mcq("Charlotte tosses a coin 10 times and gets 6 heads and 4 tails. She tosses it 10 more times. What will happen?",
                   "The results may be different this time",
                   ["She will get 6 heads again", "She will get 6 tails and 4 heads", "She cannot get heads again"],
                   "Chance results change each time. She might get 6 heads again, or 5, or 3. We cannot know for sure."))
    roll = [4, 6, 5, 3, 7, 5]
    assert sum(roll) == 30 and max(roll) == roll[4]
    tb = fig(table_svg("Oliver’s 30 dice rolls", ["Number", "1", "2", "3", "4", "5", "6"], [["Times"] + roll],
                       label="table: Oliver's dice rolls"))
    its.append(mcq(tb + "Which number did Oliver roll most often?", "5", ["6", "4", "2"],
                   "Find the biggest number in the Times row: 7. That is under the number 5. "
                   "(6 is the biggest number on the dice, not the most rolled.)"))
    its.append(mcq(tb + "Oliver says 5 is the easiest number to roll, because it came up most. Is he right?",
                   "No, each number is equally likely",
                   ["Yes, 5 will come up most every time", "No, 6 is the easiest to roll", "No, 4 is the easiest to roll"],
                   "Each face of a dice has the same chance. Results vary: next time a different number may come up most."))
    its.append(mcq("Cooper picks a counter from a bag, looks at it and puts it back. He does this 20 times. "
                   "He gets red 17 times and blue 3 times. Which bag did he most likely use?", "8 red, 2 blue",
                   ["2 red, 8 blue", "5 red, 5 blue", "10 red, 0 blue"],
                   "Red came up much more often than blue, so the bag probably has many more red counters. "
                   "It cannot be 10 red and 0 blue, because then blue would be impossible, and he picked blue 3 times."))
    av = [14, 6]
    tg = fig(tally_svg("Ava’s 20 spins", "Colour", ["Green", "Purple"], av, label="tally chart: Ava's spins"))
    its.append(mcq(tg + "Ava’s spinner has 4 equal sections. Which spinner did she most likely use?",
                   "3 green and 1 purple section",
                   ["1 green and 3 purple sections", "2 green and 2 purple sections", "4 purple sections"],
                   "Green came up 14 times and purple 6 times. Green came up much more often, so green probably covers "
                   "more of the spinner. With 4 purple sections, green would be impossible."))
    its.append(mcq("Isla tosses a coin 4 times and gets heads every time. What about the next toss?",
                   "Heads and tails are still equally likely",
                   ["Tails is now certain", "Heads is now certain", "Heads is now impossible"],
                   "A coin does not remember what happened before. Every toss, heads and tails are equally likely."))
    its.append(word_q("At the school fete, 100 raffle tickets are sold. Ava buys 1 ticket. Ava winning the raffle is …", "unlikely",
                      "Ava has only 1 of the 100 tickets. She could win, but it is unlikely."))
    assert chance_word(95, 100) == "likely"
    its.append(word_q("Ethan’s family buys 95 of the 100 raffle tickets. Ethan’s family winning the raffle is …", "likely",
                      "95 of the 100 tickets are theirs, so it is likely. It is not certain, because 5 tickets belong to other people."))
    assert chance_word(3, 10) == "unlikely"
    its.append(word_q("Matilda has 10 animal cards face down: 7 kangaroo cards and 3 koala cards. "
                      "She turns over one card. Getting a koala card is …", "unlikely",
                      "Only 3 of the 10 cards are koalas, and 7 are kangaroos. A koala can happen, but it is unlikely."))
    its.append(word_q("Kai’s class has 26 students. Each student puts their name in a hat, and the teacher picks one. "
                      "Picking the name of a student in Kai’s class is …", "certain",
                      "Every name in the hat belongs to a student in the class, so it is certain."))
    its.append(word_q("Kai’s class of 26 students puts their names in a hat. The teacher picks one name. Picking Kai’s name is …", "unlikely",
                      "Kai’s name is only 1 of the 26 names. It could be picked, but it is unlikely."))
    assert chance_word(18, 20) == "likely"
    its.append(word_q("The school canteen has 20 icy poles in a box: 18 orange and 2 lemon. "
                      "Liam takes one without looking. Getting an orange icy pole is …", "likely",
                      "18 of the 20 icy poles are orange, so orange is likely. It is not certain, because there are 2 lemon ones."))
    assert 12 - 3 == 9
    its.append(mcq("Zara rolls a dice 12 times. She gets a 6 three times. How many times did she not get a 6?",
                   "9 times", ["15 times", "3 times", "6 times"],
                   "Not a 6 means all the other rolls: 12 − 3 = 9."))
    its.append(mcq("Year 3 tossed a coin 50 times. They got 27 heads and 23 tails. Which sentence is true?",
                   "Heads and tails came up about the same",
                   ["Heads is more likely than tails", "Tails is impossible", "Heads is certain"],
                   "27 and 23 are close. Heads and tails are equally likely, and results vary a little each time."))
    assert 20 - 8 - 5 == 7
    its.append(mcq("Chloe spins a spinner 20 times. She gets red 8 times, blue 5 times and yellow the rest of the time. "
                   "How many times did she get yellow?", "7 times", ["13 times", "3 times", "33 times"],
                   "Step 1: red and blue: 8 + 5 = 13. Step 2: 20 − 13 = 7 times yellow."))
    assert len(its) == 20
    return {"title": "Chance experiments and word problems", "items": its}


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
        "<h2>The chance words</h2>"
        "<p>Chance is how likely something is to happen. We use four words. "
        "<b>Impossible</b> means it can never happen. <b>Certain</b> means it must happen. "
        "In between are <b>unlikely</b> (it could happen, but not often) and <b>likely</b> (it will probably happen).</p>"
        "<figure class='sn-fig'>" + scale_svg() +
        "<figcaption>From impossible to certain. Equally likely is in the middle: the same chance either way.</figcaption></figure>" +
        table(["Word", "Meaning", "Example"], [
            ["certain", "must happen", "The sun will rise tomorrow."],
            ["likely", "will probably happen", "It will be warm on a summer day in Sydney."],
            ["unlikely", "could happen, but probably will not", "A koala will walk into the classroom."],
            ["impossible", "can never happen", "It will snow in Darwin in summer."],
        ]) +
        "<h2>Spinners: look at the size of each part</h2>"
        "<p>A spinner is more likely to land on a colour that covers <b>more</b> of it. "
        "Compare the size of the parts, not just the number of sections.</p>"
        "<figure class='sn-fig'>" + spinner_svg(eq("red", "red", "blue", "red"), "spinner: 3 red sections and 1 blue section") +
        "<figcaption>3 of the 4 equal sections are red. Red is likely and blue is unlikely. Green is impossible.</figcaption></figure>" +
        ex("Example", "Which colour is the arrow most likely to land on?", "Red covers 3 sections. Blue covers 1 section.", "red") +
        "<h2>Bags of counters</h2>"
        "<p>When you pick without looking, the colour with <b>more</b> counters is more likely. "
        "If every counter is one colour, that colour is certain. If a colour is not in the bag, it is impossible.</p>"
        "<figure class='sn-fig'>" + bag_svg([("red", 5), ("blue", 1)], rnd, "bag: 5 red counters and 1 blue counter") +
        "<figcaption>5 red counters and 1 blue counter.</figcaption></figure>" +
        ex("Example", "Is picking a blue counter unlikely or impossible?",
           "There is 1 blue counter, so it could happen. It is not impossible.", "unlikely") +
        "<h2>Possible outcomes</h2>"
        "<p>An <b>outcome</b> is something that can happen. A coin has 2 outcomes: heads or tails. "
        "A dice has 6 outcomes: 1, 2, 3, 4, 5 or 6. Each face has the same chance, so all 6 numbers are equally likely.</p>"
        "<figure class='sn-fig'>" + dice_faces_svg() +
        "<figcaption>The 6 faces of a dice. A 6 is just as likely as a 1.</figcaption></figure>" +
        ex("Example", "Is rolling a 7 on a dice unlikely or impossible?", "A dice only shows 1 to 6.", "impossible") +
        "<h2>Chance experiments</h2>"
        "<p>Do the same thing many times and keep a tally. The results <b>vary</b>: "
        "if you do it again, you will probably get different numbers. A big part of a spinner usually comes up more often.</p>"
        "<figure class='sn-fig'>" + tally_svg("20 coin tosses", "Outcome", ["Heads", "Tails"], [11, 9], label="tally chart: 20 coin tosses") +
        "<figcaption>11 heads and 9 tails. Next time it might be 8 heads and 12 tails. That is normal.</figcaption></figure>" +
        "<h2>Common mistakes</h2>" +
        table(["Mistake", "What to do instead"], [
            ["Saying impossible when it is only unlikely", "If it could happen even once, it is not impossible"],
            ["Choosing your favourite colour", "Look at how much of the spinner or bag is that colour"],
            ["Thinking a 6 is harder to roll than a 1", "Every number on a dice is equally likely"],
            ["Counting sections, not their size", "Compare how much of the spinner each colour covers"],
            ["Expecting the same results every time", "Results change each time you repeat an experiment"],
            ["Thinking tails is due after many heads", "A coin does not remember: heads and tails stay equally likely"],
        ])
    )


FAQ = [
    {"q": "What do Year 3 students learn about chance?",
     "a": "In the Australian Curriculum (AC9M3P01 and AC9M3P02), Year 3 students describe events as certain, likely, unlikely or impossible and explain why. They also list possible outcomes, run simple chance experiments and see that results vary."},
    {"q": "What is the difference between unlikely and impossible?",
     "a": "Unlikely means it could happen, but probably will not, like picking the one blue counter from a bag of ten. Impossible means it can never happen, like rolling a 7 on a dice."},
    {"q": "How do you know which colour a spinner is most likely to land on?",
     "a": "Look at how much of the spinner each colour covers. The colour with the biggest part is most likely, even if another colour has more small sections."},
    {"q": "Why do the results change when you repeat a chance experiment?",
     "a": "Each spin, roll or toss is up to chance, so the results are a little different every time. Over many tries, the results usually match the chances, such as about half heads with a coin."},
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
    rnd = random.Random(3814)
    sets = [set_everyday(rnd), set_spinners(rnd), set_bags(rnd), set_outcomes(rnd), set_experiments(rnd)]
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
        "country": "au", "subject": "maths", "grade": "year-3", "slug": "chance", "sort": 14,
        "updated": UPDATED, "pdf_url": "",
        "title": "Chance: Certain, Likely, Unlikely or Impossible",
        "seo_title": "Year 3 Chance Worksheets: Certain, Likely, Unlikely, Impossible (Free, with Answers)",
        "short_title": "Chance",
        "domain": "Probability",
        "standard_code": "AC9M3P01",
        "standard_url": "https://v9.australiancurriculum.edu.au/f-10-curriculum/learning-areas/mathematics",
        "standard_text": "Identify practical activities and everyday events involving chance; describe possible outcomes and events as ‘likely’ or ‘unlikely’ and identify some events as ‘certain’ or ‘impossible’ explaining reasoning",
        "meta_desc": "Free Year 3 maths worksheets on chance: describe everyday events as certain, likely, unlikely or impossible, compare colours on spinners and in bags of counters, list the outcomes of a dice or coin, and read the results of chance experiments. 100 questions with an answer key, aligned to the Australian Curriculum (AC9M3P01, AC9M3P02). Useful NAPLAN numeracy practice.",
        "key_big": "Impossible means it can never happen. Unlikely means it could happen, but probably will not.",
        "key_sub": "Certain means it must happen. On a spinner or in a bag, the colour that covers more is more likely. Every number on a dice is equally likely, and results change each time you repeat an experiment.",
        "body_html": body_html(rnd), "faq": FAQ, "sets": sets,
    }


def mark_large(u, pattern):
    """Tag pictures that must print larger (A to D panels, tables, tally charts) so their labels stay readable."""
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
        mark_large(u, "(spinners A to D|bags A to D|tally chart|table)")
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
