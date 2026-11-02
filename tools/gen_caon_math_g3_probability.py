# -*- coding: utf-8 -*-
"""
Canada (Ontario) Grade 3 Math: Probability (Ontario Mathematics Curriculum 2020: Grade 3, D2.1)
  python3 tools/gen_ca_math_g3_probability.py
Everyday events, spinners, bags of counters, complementary events (red or not red), and predictions and
decisions from experiments. The five words: impossible, unlikely, equally likely, likely, certain.
Word questions show 4 of the 5 words in scale order (one word that is not the answer is left out).
Wrong answers come from real student mistakes: likely confused with certain, unlikely confused with impossible,
counting sections instead of looking at their size, judging by a favourite colour, taking the complement as
just one other colour, and "it is due" thinking after a run of heads.
Every picture shows the colour as a letter too (R = red ...), so it still works when printed in black and white.
HTML attributes use single quotes (no backslashes in the JSON). Canadian English.
"""
import json, re, math, os, random

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "ca-on", "math", "grade-3")
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



# ------------------------------------------------------------ set 1: everyday events
def set_everyday(rnd):
    its = []
    its.append(word_q("Next July 1 will be Canada Day. How likely is this?", "certain",
                      "Canada Day is on July 1 every year. It must happen, so it is certain."))
    its.append(word_q("Owen is 8 years old. On his next birthday, he will turn 9. How likely is this?", "certain",
                      "Everyone gets one year older on their birthday. 8 + 1 = 9, so it is certain."))
    its.append(word_q("Tomorrow is Friday. The day after tomorrow will be Saturday. How likely is this?", "certain",
                      "The days of the week always come in the same order. Saturday always comes after Friday, so it is certain."))
    its.append(word_q("Mei lets go of a hockey puck. It will fall down. How likely is this?", "certain",
                      "When you let go of a puck, it always falls. It must happen, so it is certain."))
    its.append(word_q("A moose will fly over the school like a bird. How likely is this?", "impossible",
                      "Moose cannot fly. This can never happen, so it is impossible."))
    its.append(word_q("Liam is 8 years old. Next year he will be 7 years old. How likely is this?", "impossible",
                      "You cannot get younger. Next year Liam will be 9, so being 7 is impossible."))
    its.append(word_q("A beaver will drive the school bus tomorrow. How likely is this?", "impossible",
                      "A beaver cannot drive a bus. This can never happen, so it is impossible."))
    its.append(mcq("Which event is impossible?", "Next week will have 9 days",
                   ["It will rain on Saturday", "Ava will lose a tooth this year", "Nathan will see a Canada goose today"],
                   "Every week has 7 days, so a week with 9 days can never happen. The other events could happen."))
    its.append(word_q("There will be snow on the ground in Ottawa on January 15. How likely is this?", "likely",
                      "Ottawa usually has snow on the ground in the middle of January. But a warm spell could melt it, "
                      "so it is likely, not certain.", keep=("certain",)))
    its.append(word_q("A July afternoon in Toronto will be warm. How likely is this?", "likely",
                      "July is summer in Toronto, so most afternoons are warm. A few days can be cool and rainy, "
                      "so it is likely, not certain.", keep=("certain",)))
    its.append(word_q("The next vehicle that drives past the school will have 4 wheels. How likely is this?", "likely",
                      "Most vehicles on the road are cars with 4 wheels. But the next one could be a motorcycle or a truck, "
                      "so it is likely, not certain."))
    its.append(word_q("Students will go outside for recess on a sunny day in June. How likely is this?", "likely",
                      "On a sunny June day, students almost always go out for recess. Something could still change the plan, "
                      "so it is likely, not certain.", keep=("certain",)))
    its.append(word_q("Emma will find a $20 bill on the sidewalk on the way to school. How likely is this?", "unlikely",
                      "It could happen, but it almost never does. So it is unlikely. It is not impossible: people do drop money.",
                      keep=("impossible",)))
    its.append(word_q("A black bear will walk into the classroom today. How likely is this?", "unlikely",
                      "Bears live in the forest. One could wander into a school, but it hardly ever happens. "
                      "So it is unlikely, not impossible.", keep=("impossible",)))
    its.append(word_q("It will rain on every single day of July in Winnipeg. How likely is this?", "unlikely",
                      "Winnipeg has many sunny days in July. Rain on all 31 days could happen, but it is unlikely.",
                      keep=("impossible",)))
    its.append(word_q("Jayden’s team will score 20 goals in one hockey game. How likely is this?", "unlikely",
                      "Hockey teams usually score a few goals in a game. 20 goals is possible, but it is unlikely."))
    its.append(word_q("Hana tosses a coin. It will land on heads. How likely is this?", "equally likely",
                      "A coin has 2 sides: heads and tails. Heads is as likely to happen as not to happen, "
                      "so it is equally likely."))
    its.append(word_q("Mateo’s friend hides a toonie in one of her two closed hands. Mateo picks a hand. "
                      "He will pick the hand with the toonie. How likely is this?", "equally likely",
                      "There are 2 hands and the toonie is in 1 of them. Picking the toonie hand and picking the empty hand "
                      "have the same chance, so it is equally likely."))
    its.append(word_q("The teacher flips a coin to choose gym class or art first. Gym class will be first. How likely is this?",
                      "equally likely",
                      "The coin has 2 sides, one for gym and one for art. Gym first and art first have the same chance, "
                      "so it is equally likely."))
    its.append(word_q("Only 3 of the 24 students will be picked to read the morning announcements. Chloe says, "
                      "“It is impossible that I will be picked.” Which word should she use instead?", "unlikely",
                      "3 of the 24 students will be picked, so Chloe could be one of them. It is possible, but not very likely. "
                      "The right word is unlikely, not impossible.", keep=("impossible",)))
    assert len(its) == 20
    return {"title": "Everyday events: from impossible to certain", "items": its}


# ------------------------------------------------------------ set 2: spinners
def set_spinners(rnd):
    its = []
    F = lambda sec: fig(spinner_svg(sec))
    S = lambda spins: fig(spinners_abcd(spins))
    its.append(mcq(F(eq("red", "red", "blue", "red")) + "The spinner has 4 equal sections. Which colour is the arrow most likely to land on?",
                   "red", ["blue", "equally likely", "green"],
                   "3 of the 4 equal sections are red and only 1 is blue, so red is most likely. "
                   "(There is no green, so green is impossible.)"))
    its.append(mcq(F(eq("yellow", "yellow", "green", "yellow", "yellow", "yellow")) +
                   "The spinner has 6 equal sections. Which colour is the arrow least likely to land on?",
                   "green", ["yellow", "equally likely", "always green"],
                   "Only 1 of the 6 equal sections is green. 5 are yellow. Green has the smallest part, so it is least likely."))
    its.append(word_q(F(eq("red", "red", "red", "red")) + "Landing on red is …", "certain",
                      "Every section is red. The arrow must land on red, so it is certain."))
    sec = eq("red", "blue", "blue", "blue", "blue", "blue")
    assert chance_word(amounts(sec)["red"], 6) == "unlikely"
    its.append(word_q(F(sec) + "Landing on red is …", "unlikely",
                      "Only 1 of the 6 equal sections is red. It can happen, but not often, so it is unlikely. "
                      "It is not impossible, because there is a red section.", keep=("impossible",)))
    its.append(word_q(F(eq("red", "blue", "yellow", "blue", "red", "yellow")) + "Landing on green is …", "impossible",
                      "There is no green section on this spinner. The arrow can never land on green, so it is impossible."))
    sec = eq("green", "green", "purple", "green", "green", "green")
    assert chance_word(amounts(sec)["green"], 6) == "likely"
    its.append(word_q(F(sec) + "Landing on green is …", "likely",
                      "5 of the 6 equal sections are green, so green is likely. "
                      "It is not certain, because there is 1 purple section.", keep=("certain",)))
    sec = eq("red", "blue", "red", "blue")
    assert chance_word(amounts(sec)["red"], 4) == "equally likely"
    its.append(word_q(F(sec) + "Landing on red is …", "equally likely",
                      "2 of the 4 equal sections are red and 2 are not. Red covers half of the spinner, "
                      "so landing on red and not landing on red are equally likely."))
    sec = [("blue", 3), ("red", 1)]
    assert chance_word(amounts(sec)["blue"], 4) == "likely"
    its.append(word_q(F(sec) + "Landing on blue is …", "likely",
                      "The blue part covers 3 quarters of the spinner. The red part is only 1 quarter. "
                      "So blue is likely, but not certain.", keep=("certain",)))
    sec = [("red", 3), ("blue", 1), ("green", 1), ("blue", 1)]
    assert amounts(sec) == {"red": 3, "blue": 2, "green": 1}
    its.append(mcq(F(sec) + "Which colour is the arrow most likely to land on?", "red",
                   ["blue", "green", "all equally likely"],
                   "Do not just count sections. Look at their size. The red part is half of the spinner. "
                   "The two blue sections are small: together they are less than half."))
    sec = [("yellow", 6), ("blue", 1), ("red", 2), ("blue", 1), ("red", 1), ("blue", 1)]
    assert amounts(sec) == {"yellow": 6, "blue": 3, "red": 3}
    its.append(mcq(F(sec) + "Kai says blue is most likely, because blue has the most sections. Which colour is most likely?",
                   "yellow", ["blue", "red", "all equally likely"],
                   "Kai counted sections, not their size. The one yellow section is half of the whole spinner. "
                   "Blue and red each cover only a quarter, so yellow is most likely."))
    its.append(mcq(F(eq("red", "blue", "yellow", "red")) + "Which colour can the arrow never land on?",
                   "green", ["yellow", "blue", "red"],
                   "The spinner has red, blue and yellow sections. There is no green, so green is impossible. "
                   "Yellow has only 1 section, so it is unlikely, not impossible."))
    its.append(mcq(F([("red", 1), ("blue", 1)]) + "Which sentence is true?", "Red and blue are equally likely",
                   ["Red is more likely than blue", "Landing on red is certain", "Landing on blue is impossible"],
                   "Half of the spinner is red and half is blue. The parts are the same size, so they are equally likely."))
    sec = eq("red", "blue", "yellow", "red", "blue", "yellow")
    assert len(set(amounts(sec).values())) == 1
    its.append(mcq(F(sec) + "Which colours are equally likely?", "all three colours",
                   ["only red and blue", "only red", "none of them"],
                   "Each colour has 2 of the 6 equal sections. They all cover the same amount, so all three are equally likely."))
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
    its.append(abcd_q(S([eq("blue", "blue", "blue", "red"), eq("blue", "blue", "blue", "blue"), [("blue", 3), ("yellow", 1)],
                         eq("blue", "yellow", "red", "green")]) +
                      "On which spinner is landing on blue certain?", "Spinner", 1,
                      "Certain means it must happen. Only Spinner B is all blue. "
                      "On A and C, blue is likely, but not certain, because there is another colour too."))
    its.append(mcq("Ethan colours a spinner with 4 equal sections. He wants landing on red to be unlikely, but not impossible. "
                   "How many sections should he colour red?", "1 section",
                   ["0 sections", "3 sections", "4 sections"],
                   "1 red section out of 4 makes red unlikely. 0 red sections would make red impossible. "
                   "3 would make it likely, and 4 would make it certain."))
    assert 4 + 4 == 8
    its.append(mcq("Sofia’s spinner has 8 equal sections. She colours 4 sections red and the rest blue. "
                   "Which sentence is true?", "Red and blue are equally likely",
                   ["Red is more likely", "Blue is more likely", "Blue is impossible"],
                   "8 − 4 = 4 sections are blue. 4 red and 4 blue sections of the same size cover the same amount, "
                   "so red and blue are equally likely."))
    sec = eq("green", "green", "yellow", "green", "green", "green", "yellow", "green")
    assert amounts(sec) == {"green": 6, "yellow": 2}
    its.append(mcq(F(sec) + "Zoe says the arrow will probably land on yellow, because yellow is her favourite colour. "
                   "Which colour is the arrow more likely to land on?", "green",
                   ["yellow", "equally likely", "always yellow"],
                   "Your favourite colour does not change the chance. 6 of the 8 equal sections are green and 2 are yellow, "
                   "so green is more likely."))
    assert len(its) == 20
    return {"title": "Spinners: look at the size of each part", "items": its}


# ------------------------------------------------------------ set 3: bags, cards and equally likely
def set_bags(rnd):
    its = []
    B = lambda counts, lab="bag of counters": fig(bag_svg(counts, rnd, lab))
    G = lambda bags: fig(bags_abcd(bags, rnd))
    its.append(mcq(B([("red", 6), ("blue", 2)]) + "Amira picks one counter from the bag without looking. "
                   "Which colour is she most likely to pick?", "red",
                   ["blue", "equally likely", "yellow"],
                   "There are 6 red counters and only 2 blue counters. More red counters means red is more likely."))
    its.append(mcq(B([("yellow", 7), ("green", 1)]) + "Noah picks one counter without looking. Which colour is he least likely to pick?",
                   "green", ["yellow", "equally likely", "always green"],
                   "There is only 1 green counter and 7 yellow counters, so green is least likely."))
    its.append(word_q(B([("blue", 8)]) + "Picking a blue counter from this bag is …", "certain",
                      "Every counter in the bag is blue, so you must pick blue. It is certain."))
    its.append(word_q(B([("red", 5), ("yellow", 3)]) + "Picking a green counter from this bag is …", "impossible",
                      "There are only red and yellow counters. There is no green counter, so it is impossible."))
    assert chance_word(7, 8) == "likely" and chance_word(1, 10) == "unlikely" and chance_word(4, 8) == "equally likely"
    its.append(word_q(B([("red", 7), ("blue", 1)]) + "Picking a red counter from this bag is …", "likely",
                      "7 of the 8 counters are red, so red is likely. It is not certain, because there is 1 blue counter.",
                      keep=("certain",)))
    its.append(word_q(B([("red", 1), ("blue", 9)]) + "Picking a red counter from this bag is …", "unlikely",
                      "Only 1 of the 10 counters is red. It can happen, but not often, so it is unlikely, not impossible.",
                      keep=("impossible",)))
    its.append(word_q(B([("red", 4), ("blue", 4)]) + "Picking a red counter from this bag is …", "equally likely",
                      "4 of the 8 counters are red and 4 are not. Picking red and not picking red have the same chance, "
                      "so it is equally likely."))
    its.append(mcq(B([("red", 3), ("blue", 3), ("yellow", 2)]) + "Which two colours are equally likely to be picked?",
                   "red and blue", ["red and yellow", "blue and yellow", "all three colours"],
                   "There are 3 red, 3 blue and 2 yellow counters. Red and blue have the same number, so they are equally likely."))
    its.append(mcq(B([("yellow", 5), ("red", 2), ("green", 1)]) + "Put the colours in order from most likely to least likely.",
                   "yellow, red, green", ["green, red, yellow", "red, yellow, green", "yellow, green, red"],
                   "Count each colour: yellow 5, red 2, green 1. The most counters is most likely: yellow, red, green."))
    its.append(word_q(B([("red", 3), ("blue", 5)]) + "Mei takes all the blue counters out of the bag. "
                      "Now picking a red counter is …", "certain",
                      "After the blue counters come out, only the 3 red counters are left. You must pick red, so it is certain.",
                      keep=("likely",)))
    assert 2 + 6 > 6
    its.append(mcq(B([("red", 6), ("green", 2)]) + "Kai puts 6 more green counters into the bag. "
                   "Which colour is now more likely to be picked?", "green",
                   ["red", "equally likely", "green is impossible"],
                   "Green: 2 + 6 = 8 counters. Red: 6 counters. 8 is more than 6, so green is now more likely."))
    assert 2 + 3 == 5
    its.append(mcq(B([("red", 2), ("blue", 5)]) + "How many red counters must Zoe add to make red and blue equally likely?",
                   "3", ["5", "7", "1"],
                   "Red and blue are equally likely when there are the same number of each. Blue has 5. "
                   "Red has 2, so add 5 − 2 = 3 red counters."))
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
    its.append(abcd_q(G([[("red", 4), ("blue", 2)], [("red", 5), ("blue", 1)], [("red", 3), ("blue", 3)], [("red", 6)]]) +
                      "From which bag are red and blue equally likely?", "Bag", 2,
                      "Bag C has 3 red and 3 blue counters. The same number of each colour means they are equally likely."))
    its.append(mcq("Leah has 10 hockey cards face down: 5 goalie cards and 5 player cards. She turns over one card. "
                   "Which sentence is true?", "A goalie card and a player card are equally likely",
                   ["A goalie card is more likely", "A goalie card is certain", "A player card is impossible"],
                   "There are 5 goalie cards and 5 player cards. The same number of each means they are equally likely."))
    its.append(mcq("Amira’s bag has 3 red counters and 2 blue counters. She wants picking a blue counter to be impossible. "
                   "What should she do?", "Take out the 2 blue counters",
                   ["Take out the 3 red counters", "Add 2 more red counters", "Take out 1 blue counter"],
                   "Impossible means it can never happen. If there are no blue counters left, blue can never be picked. "
                   "Adding red counters only makes blue unlikely."))
    its.append(mcq("A bag has 10 counters. Picking a red counter is certain. How many red counters are in the bag?",
                   "10", ["9", "5", "1"],
                   "Certain means it must happen, so every counter must be red: all 10. "
                   "With 9 red and 1 other counter, red is likely, not certain."))
    its.append(mcq("At the school fun fair, a prize box has 20 prizes: 15 pencils, 4 sticker sheets and 1 toy car. "
                   "Olivia picks one prize without looking. Which prize is she least likely to get?", "the toy car",
                   ["a pencil", "a sticker sheet", "they are all equally likely"],
                   "There is only 1 toy car out of 20 prizes, so it is least likely. "
                   "15 of the 20 prizes are pencils, so a pencil is most likely."))
    assert len(its) == 20
    return {"title": "Bags and cards: equally likely or not?", "items": its}


# ------------------------------------------------------------ set 4: complementary events (red or not red)
def set_complement(rnd):
    its = []
    F = lambda sec: fig(spinner_svg(sec))
    B = lambda counts: fig(bag_svg(counts, rnd))
    sec = eq("red", "blue", "blue", "blue")
    assert chance_word(3, 4) == "likely"
    its.append(word_q(F(sec) + "Landing on red is unlikely. Landing on a colour that is not red is …", "likely",
                      "Not red means blue here. 3 of the 4 equal sections are not red, so not red is likely. "
                      "When red is unlikely, not red is likely."))
    its.append(word_q(B([("red", 7), ("blue", 1)]) + "Picking a red counter is likely. Picking a counter that is not red is …",
                      "unlikely",
                      "Only 1 of the 8 counters is not red. It can happen, so it is unlikely, not impossible.",
                      keep=("impossible",)))
    its.append(word_q(F(eq("red", "red", "blue", "blue")) + "Landing on a colour that is not blue is …", "equally likely",
                      "Not blue means red here. Red covers 2 of the 4 equal sections: half of the spinner. "
                      "So not blue and blue are equally likely."))
    its.append(word_q(B([("green", 6)]) + "Picking a counter that is not green is …", "impossible",
                      "Every counter is green. There is no counter that is not green, so it is impossible."))
    its.append(word_q(B([("blue", 5), ("yellow", 3)]) + "Picking a counter that is not red is …", "certain",
                      "There are no red counters in the bag. Every counter is not red, so picking a counter that is not red is certain.",
                      keep=("likely",)))
    its.append(mcq("Landing on red is likely. What can you say about not landing on red?", "It is unlikely",
                   ["It is also likely", "It is certain", "It is impossible"],
                   "Red and not red cover the whole spinner together. If red covers the bigger part, "
                   "not red covers the smaller part, so it is unlikely."))
    its.append(word_q("Picking a purple marble from a bag is impossible. Picking a marble that is not purple is …", "certain",
                      "There are no purple marbles, so every marble is not purple. You must pick one that is not purple. "
                      "It is certain."))
    its.append(word_q("Rolling a 6 on a number cube is unlikely. Rolling a number that is not 6 is …", "likely",
                      "Not 6 means 1, 2, 3, 4 or 5: 5 of the 6 faces. So it is likely. It is not certain, "
                      "because you could roll a 6.", keep=("certain",)))
    its.append(mcq("What is the complement of “the coin lands on heads”?", "the coin lands on tails",
                   ["the coin lands on heads again", "the coin lands on heads or tails", "the coin lands on a number"],
                   "The complement is everything else that could happen. A coin has only heads and tails, "
                   "so the complement of heads is tails."))
    its.append(mcq(F(eq("red", "blue", "yellow", "blue")) + "What is the complement of “landing on red”?",
                   "landing on blue or yellow", ["landing on blue", "landing on yellow", "landing on red or blue"],
                   "The complement is every outcome that is not red. On this spinner that is blue or yellow, "
                   "not just one of them."))
    sec = eq("red", "blue", "yellow", "green")
    assert chance_word(3, 4) == "likely"
    its.append(word_q(F(sec) + "Landing on a colour that is not green is …", "likely",
                      "Red, blue and yellow are not green: 3 of the 4 equal sections. So it is likely. "
                      "It is not certain, because there is a green section.", keep=("certain",)))
    assert len([n for n in range(1, 7) if n % 2 == 0]) == 3
    its.append(word_q(fig(cube_faces_svg()) + "Owen rolls a number cube. Rolling an even number is …", "equally likely",
                      "Even numbers: 2, 4, 6 (3 faces). Not even: 1, 3, 5 (3 faces). "
                      "3 and 3 are the same, so even and not even are equally likely."))
    assert chance_word(5, 6) == "likely"
    its.append(mcq(fig(cube_faces_svg()) + "Priya rolls a number cube. Which is the complement of “rolling a 1”?",
                   "rolling 2, 3, 4, 5 or 6", ["rolling a 6", "rolling a 2", "rolling 1, 2, 3, 4, 5 or 6"],
                   "The complement is every other outcome: 2, 3, 4, 5 or 6. Rolling a 1 is unlikely, "
                   "so its complement is likely."))
    sec = [("blue", 1), ("red", 6), ("yellow", 1)]
    assert chance_word(2, 8) == "unlikely"
    its.append(word_q(F(sec) + "Landing on a colour that is not red is …", "unlikely",
                      "Not red means blue or yellow. Those two small parts together are only a quarter of the spinner. "
                      "So not red is unlikely, but not impossible.", keep=("impossible",)))
    A = eq("red", "blue", "yellow", "green")
    Bs = [("red", 2), ("blue", 1), ("yellow", 1)]
    C = eq("red", "red", "red", "blue")
    D = eq("red", "blue", "yellow", "red", "green", "blue")
    assert [amounts(s)["red"] * 2 == sum(u for _, u in s) for s in (A, Bs, C, D)] == [False, True, False, False]
    its.append(abcd_q(fig(spinners_abcd([A, Bs, C, D])) +
                      "On which spinner are landing on red and landing on not red equally likely?", "Spinner", 1,
                      "On Spinner B, red covers half of the spinner and not red covers the other half. "
                      "So red and not red are equally likely there."))
    its.append(abcd_q(fig(bags_abcd([[("blue", 1), ("red", 5)], [("red", 3), ("yellow", 3)], [("blue", 6)],
                                     [("blue", 3), ("red", 3)]], rnd)) +
                      "From which bag is picking a counter that is not blue certain?", "Bag", 1,
                      "Bag B has no blue counters, so every counter is not blue. That is certain. "
                      "In Bag A, not blue is likely. In Bag C, it is impossible. In Bag D, it is equally likely."))
    its.append(mcq("In Owen’s bag, picking a red counter is certain. What about picking a counter that is not red?",
                   "It is impossible", ["It is unlikely", "It is likely", "It is certain"],
                   "Certain means every counter is red. Then there is no counter that is not red, so it is impossible."))
    its.append(word_q("The weather forecast says rain in Halifax tomorrow is likely. "
                      "“It will not rain in Halifax tomorrow” is …", "unlikely",
                      "Rain and no rain are complements. If rain is likely, no rain is unlikely. "
                      "It is not impossible: forecasts can be wrong.", keep=("impossible",)))
    its.append(mcq("Olivia says, “Landing on red is unlikely, so landing on not red is impossible.” Is she right?",
                   "No, not red is likely", ["Yes, she is right", "No, not red is certain", "No, not red is also unlikely"],
                   "Red is unlikely, but it can happen. So not red does not always happen: it is likely, not certain or impossible."))
    its.append(mcq(B([("red", 2), ("blue", 4), ("yellow", 2)]) + "Which is more likely: picking blue or picking not blue?",
                   "They are equally likely", ["Blue is more likely", "Not blue is more likely", "Not blue is impossible"],
                   "Blue: 4 counters. Not blue: red and yellow, 2 + 2 = 4 counters. 4 and 4 are the same, "
                   "so they are equally likely."))
    assert len(its) == 20
    return {"title": "Red or not red: complementary events", "items": its}


# ------------------------------------------------------------ set 5: predictions, decisions and word problems
def set_predictions(rnd):
    its = []
    maya = [9, 7, 4]
    assert sum(maya) == 20
    tf = fig(tally_svg("Maya’s 20 spins", "Colour", ["Red", "Blue", "Yellow"], maya, label="tally chart: Maya's spins"))
    its.append(mcq(tf + "Which colour came up most often?", "red", ["yellow", "blue", "they all came up the same"],
                   "Red: 1 group of 5 and 4 more = 9. Blue: 7. Yellow: 4. Red has the most tally marks."))
    its.append(mcq(tf + "How many times did Maya spin altogether?", "20 times", ["3 times", "9 times", "16 times"],
                   "Add the tallies: 9 + 7 + 4 = 20."))
    its.append(mcq(tf + "How many more times did red come up than yellow?", "5 times", ["13 times", "2 times", "4 times"],
                   "Red 9, yellow 4. How many more means subtract: 9 − 4 = 5."))
    its.append(mcq(fig(spinner_svg(eq("red", "blue"))) + "Lucas spins this spinner 20 times. Which result would be most surprising?",
                   "red 20, blue 0", ["red 10, blue 10", "red 11, blue 9", "red 8, blue 12"],
                   "Half the spinner is red and half is blue, so you expect about 10 of each. Results near 10 are normal. "
                   "Red every single time is possible, but very unlikely."))
    sec = eq("blue", "blue", "red", "blue")
    its.append(mcq(fig(spinner_svg(sec)) + "Benjamin spins this spinner 20 times. Which prediction is best?",
                   "blue 15, red 5", ["blue 5, red 15", "blue 10, red 10", "blue 20, red 0"],
                   "3 of the 4 equal sections are blue, so blue should come up about 3 times as often as red. "
                   "Blue 15 and red 5 fits best. The results can change a little each time."))
    assert 40 // 4 == 10
    its.append(mcq(fig(spinner_svg(eq("red", "blue", "blue", "blue"))) +
                   "Hana spins this spinner 40 times. About how many times should she predict red?",
                   "about 10 times", ["about 20 times", "about 30 times", "about 4 times"],
                   "Red is 1 of 4 equal sections, so about 1 spin in every 4 is red. 40 ÷ 4 = 10. "
                   "30 is the prediction for blue, not red."))
    roll = [4, 6, 5, 3, 7, 5]
    assert sum(roll) == 30 and max(roll) == roll[4]
    tb = fig(table_svg("Nathan’s 30 rolls", ["Number", "1", "2", "3", "4", "5", "6"], [["Times"] + roll],
                       label="table: Nathan's number cube rolls"))
    its.append(mcq(tb + "Nathan rolled a number cube 30 times. Which number did he roll most often?", "5", ["6", "4", "2"],
                   "Find the biggest number in the Times row: 7. That is under the number 5. "
                   "(6 is the biggest number on the cube, not the most rolled.)"))
    its.append(mcq(tb + "Nathan says 5 is the easiest number to roll, because it came up most. Is he right?",
                   "No, each number is equally likely",
                   ["Yes, 5 will come up most every time", "No, 6 is the easiest to roll", "No, 4 is the easiest to roll"],
                   "Each face of a number cube has the same chance. Results vary: next time a different number may come up most."))
    its.append(mcq("Benjamin picks a counter from a bag, looks at it and puts it back. He does this 20 times. "
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
    its.append(mcq("Arjun tosses a coin 4 times and gets heads every time. What about the next toss?",
                   "Heads and tails are still equally likely",
                   ["Tails is now certain", "Heads is now certain", "Heads is now impossible"],
                   "A coin does not remember what happened before. Every toss, heads and tails are equally likely."))
    its.append(mcq("Kai wins a prize if he picks a red counter. Bag A has 3 red and 5 blue counters. "
                   "Bag B has 5 red and 3 blue counters. Which bag should he choose?", "Bag B",
                   ["Bag A", "Either bag, they are the same", "Neither bag, red is impossible"],
                   "Both bags have 8 counters. Bag B has 5 red, Bag A has only 3. Red is likely in Bag B, "
                   "so Bag B is the better choice."))
    its.append(mcq("Zoe and Jayden play a game. Zoe gets a point when the spinner lands on red. "
                   "Jayden gets a point when it lands on blue. Which spinner makes the game fair?",
                   "2 red and 2 blue sections",
                   ["3 red and 1 blue section", "1 red and 3 blue sections", "4 red sections"],
                   "A game is fair when both players are equally likely to win. With 2 equal red and 2 equal blue sections, "
                   "red and blue are equally likely."))
    its.append(mcq("Liam’s class spins a spinner 50 times. They get blue 38 times and yellow 12 times. "
                   "What is the best prediction for the next spin?", "Blue is more likely",
                   ["Yellow is more likely, because it is due", "Blue is certain", "They are equally likely"],
                   "Blue came up much more often, so blue probably covers more of the spinner. "
                   "Blue is more likely, but not certain. Yellow is never “due”."))
    its.append(word_q("At the school winter carnival, 100 raffle tickets are sold. Ava buys 1 ticket. Ava winning the raffle is …",
                      "unlikely",
                      "Ava has only 1 of the 100 tickets. She could win, but it is unlikely.", keep=("impossible",)))
    assert chance_word(95, 100) == "likely"
    its.append(word_q("Ethan’s family buys 95 of the 100 raffle tickets. Ethan’s family winning the raffle is …", "likely",
                      "95 of the 100 tickets are theirs, so it is likely. It is not certain, because 5 tickets belong to other people.",
                      keep=("certain",)))
    assert chance_word(15, 20) == "likely"
    its.append(word_q("A box has 20 granola bars: 15 chocolate chip and 5 oatmeal. Leah takes one without looking. "
                      "Getting an oatmeal bar is …", "unlikely",
                      "Only 5 of the 20 bars are oatmeal, and 15 are chocolate chip. Oatmeal can happen, but it is unlikely.",
                      keep=("impossible",)))
    its.append(word_q("Sofia’s class has 24 students. Each student puts their name in a toque, and the teacher picks one. "
                      "Picking the name of a student in Sofia’s class is …", "certain",
                      "Every name in the toque belongs to a student in the class, so it is certain.", keep=("likely",)))
    assert 12 - 3 == 9
    its.append(mcq("Owen rolls a number cube 12 times. He gets a 6 three times. How many times did he not get a 6?",
                   "9 times", ["15 times", "3 times", "6 times"],
                   "Not a 6 means all the other rolls: 12 − 3 = 9."))
    assert 20 - 8 - 5 == 7
    its.append(mcq("Chloe spins a spinner 20 times. She gets red 8 times, blue 5 times and yellow the rest of the time. "
                   "How many times did she get yellow?", "7 times", ["13 times", "3 times", "33 times"],
                   "Step 1: red and blue: 8 + 5 = 13. Step 2: 20 − 13 = 7 times yellow."))
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


def body_html(rnd):
    return (
        "<h2>The five probability words</h2>"
        "<p>Probability tells us how likely something is to happen. "
        "<b>Impossible</b> means it can never happen. <b>Certain</b> means it must happen. "
        "<b>Unlikely</b> means it could happen, but probably will not. <b>Likely</b> means it will probably happen. "
        "<b>Equally likely</b> means it is just as likely to happen as not to happen.</p>"
        "<figure class='sn-fig'>" + scale_svg() +
        "<figcaption>From impossible to certain. Equally likely is in the middle.</figcaption></figure>" +
        table(["Word", "Meaning", "Example"], [
            ["impossible", "can never happen", "A moose will fly over the school."],
            ["unlikely", "could happen, but probably will not", "A black bear will walk into the classroom."],
            ["equally likely", "same chance to happen or not", "A tossed coin will land on heads."],
            ["likely", "will probably happen", "There will be snow in Ottawa in January."],
            ["certain", "must happen", "Next July 1 will be Canada Day."],
        ]) +
        "<h2>Spinners: look at the size of each part</h2>"
        "<p>A spinner is more likely to land on a colour that covers <b>more</b> of it. "
        "Compare the size of the parts, not just the number of sections.</p>"
        "<figure class='sn-fig'>" + spinner_svg([("red", 3), ("blue", 1), ("green", 1), ("blue", 1)],
                                                  "spinner: red half, 2 small blue sections, 1 small green section") +
        "<figcaption>Blue has 2 sections, but red covers half of the spinner.</figcaption></figure>" +
        ex("Example", "Which colour is the arrow most likely to land on?",
           "Red is one big section: half of the spinner. The two blue sections together are less than half.", "red") +
        "<h2>Bags of counters</h2>"
        "<p>When you pick without looking, the colour with <b>more</b> counters is more likely. "
        "The same number of each colour means they are equally likely.</p>"
        "<figure class='sn-fig'>" + bag_svg([("red", 5), ("blue", 1)], rnd, "bag: 5 red counters and 1 blue counter") +
        "<figcaption>5 red counters and 1 blue counter.</figcaption></figure>" +
        ex("Example", "Is picking a blue counter unlikely or impossible?",
           "There is 1 blue counter, so it could happen. It is not impossible.", "unlikely") +
        "<h2>Red or not red: complementary events</h2>"
        "<p>The <b>complement</b> of an event is everything else that could happen. "
        "The complement of “landing on red” is “landing on not red”. One of the two always happens.</p>"
        "<figure class='sn-fig'>" + spinner_svg(eq("red", "blue", "blue", "yellow"),
                                                  "spinner: 1 red, 2 blue and 1 yellow section") +
        "<figcaption>Red is 1 of 4 equal sections. Not red (blue or yellow) is 3 of 4.</figcaption></figure>" +
        table(["If red is …", "then not red is …"], [
            ["impossible", "certain"],
            ["unlikely", "likely"],
            ["equally likely", "equally likely"],
            ["likely", "unlikely"],
            ["certain", "impossible"],
        ]) +
        "<h2>Predictions and decisions</h2>"
        "<p>Use the chance to predict. A number cube has 6 faces, and each face is equally likely. "
        "If red is 1 of 4 equal sections, predict red about 1 time in every 4 spins. "
        "Real results <b>vary</b> a little each time.</p>"
        "<figure class='sn-fig'>" + cube_faces_svg() +
        "<figcaption>The 6 faces of a number cube. A 6 is just as likely as a 1.</figcaption></figure>" +
        ex("Example", "Kai wins if he picks red. Bag A: 3 red, 5 blue. Bag B: 5 red, 3 blue. Which bag should he choose?",
           "Red is unlikely in Bag A and likely in Bag B.", "Bag B") +
        "<h2>Common mistakes</h2>" +
        table(["Mistake", "What to do instead"], [
            ["Saying certain when it is only likely", "Certain means it must happen every time. If it could fail, it is likely"],
            ["Saying impossible when it is only unlikely", "If it could happen even once, it is not impossible"],
            ["Counting sections, not their size", "Compare how much of the spinner each colour covers"],
            ["Choosing your favourite colour", "Look at how much of the spinner or bag is that colour"],
            ["Thinking the complement is just one other colour", "Not red means every colour that is not red"],
            ["Thinking tails is due after many heads", "A coin does not remember: heads and tails stay equally likely"],
        ])
    )


FAQ = [
    {"q": "What do Grade 3 students learn about probability in Ontario?",
     "a": "In the Ontario Mathematics Curriculum (2020), expectation D2.1, Grade 3 students use the words impossible, unlikely, equally likely, likely and certain to describe events and their complements, such as red and not red. They use these words to make predictions and informed decisions."},
    {"q": "What is a complementary event?",
     "a": "The complement of an event is everything else that could happen. The complement of landing on red is landing on not red, so if red is likely, not red is unlikely."},
    {"q": "What is the difference between unlikely and impossible?",
     "a": "Unlikely means it could happen, but probably will not, like picking the one blue counter from a bag of ten. Impossible means it can never happen, like rolling a 7 on a number cube with the numbers 1 to 6."},
    {"q": "Is probability on the Grade 3 EQAO math assessment?",
     "a": "The Grade 3 EQAO math assessment is based on the Ontario curriculum, which includes data and probability. Practising the probability words with spinners, bags and number cubes is useful preparation."},
]


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


def gen_unit():
    rnd = random.Random(33817)
    sets = [set_everyday(rnd), set_spinners(rnd), set_bags(rnd), set_complement(rnd), set_predictions(rnd)]
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
        "country": "ca-on", "subject": "math", "grade": "grade-3", "slug": "probability", "sort": 17,
        "updated": UPDATED, "pdf_url": "",
        "title": "Probability: Impossible, Unlikely, Equally Likely, Likely or Certain",
        "seo_title": "Grade 3 Probability Worksheets: Likely, Unlikely, Certain (Free, with Answer Key)",
        "short_title": "Probability",
        "domain": "Data",
        "standard_code": "Grade 3: D2.1",
        "standard_url": "https://www.dcp.edu.gov.on.ca/en/curriculum/elementary-mathematics",
        "standard_text": "Use mathematical language, including the terms “impossible”, “unlikely”, “equally likely”, “likely”, and “certain”, to describe the likelihood of complementary events happening, and use that likelihood to make predictions and informed decisions",
        "meta_desc": "Free Grade 3 math worksheets on probability: describe events as impossible, unlikely, equally likely, likely or certain, compare spinners and bags of counters, work with complementary events (red or not red) and make predictions from experiments. 100 questions with an answer key, following the Ontario curriculum (D2.1). Helpful EQAO practice.",
        "key_big": "The bigger the part of the spinner or bag, the more likely the outcome.",
        "key_sub": "Use the words impossible, unlikely, equally likely, likely and certain. An event and its complement (red and not red) cover everything: if red is likely, not red is unlikely.",
        "body_html": body_html(rnd), "faq": FAQ, "sets": sets,
    }


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
