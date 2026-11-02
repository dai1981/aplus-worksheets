# -*- coding: utf-8 -*-
"""
Singapore Primary 1 Maths: Picture Graphs (MOE 2021 Primary Mathematics Syllabus, Standard – Statistics)
  python3 tools/gen_sg_maths_p1_picture_graphs.py
Reading and interpreting picture graphs where 1 picture stands for 1: counting the pictures in a row or
column, most and fewest, how many more and how many fewer, totals, and word problems with Singapore
contexts (favourite fruits, pets, the canteen, the library, Chinese New Year red packets, Sports Day).
Wrong answers come from real student mistakes: miscounting by one, reading the row or column next door,
adding when the question asks “how many more”, giving the number of rows as the total, leaving out a row,
and comparing how long a row looks instead of counting when the pictures are not the same size.
Every value is checked in code. Singapore style: British spelling, Singapore names. HTML attributes use
single quotes (no backslashes in the JSON).
"""
import json, math, os, random, re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "sg", "maths", "primary-1")
UPDATED = "2026-11-03"
LINE = "#1f4e79"
SYM = "#2f6fb5"
FILL = "#cfe0f1"
PFILL = "#eef4fa"
RED = "#c0392b"
INK = "#2b2b2b"
GRID = "#c4d0dc"
FONT = "Arial, Helvetica, sans-serif"


# ------------------------------------------------------------ helpers
def mcq(q, correct, cands, e):
    """4 choices: correct + 3 unique distractors from real mistakes (no zero or negative numbers).
    Positions are balanced later for the whole set."""
    correct = str(correct)
    seen = {correct}
    pick = []
    for c in cands:
        if c is None:
            continue
        c = str(c)
        lead = c.split(" ")[0]
        if c in seen or not c or lead.startswith("-") or lead.startswith("−") or lead == "0":
            continue
        seen.add(c)
        pick.append(c)
        if len(pick) == 3:
            break
    assert len(pick) == 3, (q[-90:], correct, cands)
    return {"q": q, "c": pick + [correct], "a": 3, "e": e}


def fig(svg):
    return "<div class='qfig'>" + svg + "</div>"


def svg_wrap(w, h, body, label):
    w, h = int(math.ceil(w)), int(math.ceil(h))
    return ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 %d %d' width='%d' height='%d' "
            "role='img' aria-label='%s'><g font-family='%s'>%s</g></svg>" % (w, h, w, h, label, FONT, body))


def tw(t, fs, bold=False):
    """Approximate text width in px (Arial)."""
    return len(str(t)) * fs * (0.62 if bold else 0.58)


def text(x, y, t, fs=14, anchor="middle", bold=False, col=INK, extra=""):
    return ("<text x='%.1f' y='%.1f' font-size='%d'%s fill='%s' text-anchor='%s'%s>%s</text>"
            % (x, y, fs, " font-weight='700'" if bold else "", col, anchor, extra, t))


def fmt(v, unit):
    """unit = (singular, plural)."""
    return "%d %s" % (v, unit[0] if v == 1 else unit[1])


def fl(vals, unit):
    return [fmt(v, unit) for v in vals]


CH = ("child", "children")
PET = ("pet", "pets")
DAY = ("day", "days")
BOOK = ("book", "books")
STK = ("sticker", "stickers")
RP = ("red packet", "red packets")
FR = ("fruit", "fruits")
BAG = ("beanbag", "beanbags")
SHELL = ("shell", "shells")
STAR = ("star", "stars")
FISH = ("fish", "fish")
VOTE = ("vote", "votes")


# ------------------------------------------------------------ pictures (all the same size: about 18 px)
def star_pts(cx, cy, R=9.5, r=4.0):
    pts = []
    for i in range(10):
        ang = -math.pi / 2 + i * math.pi / 5
        rad = R if i % 2 == 0 else r
        pts.append((cx + rad * math.cos(ang), cy + rad * math.sin(ang)))
    return pts


def symbol(kind, cx, cy, k=1.0):
    """k scales the picture (used only for the 'different sizes' trap)."""
    if kind == "face":
        r = 8.5 * k
        return ("<circle cx='%.1f' cy='%.1f' r='%.1f' fill='%s'/>"
                "<circle cx='%.1f' cy='%.1f' r='%.1f' fill='#ffffff'/><circle cx='%.1f' cy='%.1f' r='%.1f' fill='#ffffff'/>"
                "<path d='M %.1f %.1f Q %.1f %.1f %.1f %.1f' fill='none' stroke='#ffffff' stroke-width='%.1f' stroke-linecap='round'/>"
                % (cx, cy, r, SYM, cx - 3 * k, cy - 2.2 * k, 1.3 * k, cx + 3 * k, cy - 2.2 * k, 1.3 * k,
                   cx - 4 * k, cy + 2.2 * k, cx, cy + 6.2 * k, cx + 4 * k, cy + 2.2 * k, 1.4 * k))
    if kind == "apple":
        r = 8 * k
        return ("<circle cx='%.1f' cy='%.1f' r='%.1f' fill='%s'/>"
                "<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='%.1f' stroke-linecap='round'/>"
                "<ellipse cx='%.1f' cy='%.1f' rx='%.1f' ry='%.1f' fill='#4c9a5b'/>"
                % (cx, cy + 1 * k, r, RED, cx, cy - 6 * k, cx + 1 * k, cy - 9.5 * k, INK, 1.4 * k,
                   cx + 4 * k, cy - 8 * k, 3 * k, 1.6 * k))
    if kind == "square":
        h = 7.5 * k
        return "<rect x='%.1f' y='%.1f' width='%.1f' height='%.1f' rx='2' fill='%s'/>" % (cx - h, cy - h, 2 * h, 2 * h, SYM)
    if kind == "circle":
        return "<circle cx='%.1f' cy='%.1f' r='%.1f' fill='%s'/>" % (cx, cy, 8.5 * k, SYM)
    if kind == "fish":
        return ("<ellipse cx='%.1f' cy='%.1f' rx='%.1f' ry='%.1f' fill='%s'/>"
                "<polygon points='%.1f,%.1f %.1f,%.1f %.1f,%.1f' fill='%s'/>"
                "<circle cx='%.1f' cy='%.1f' r='%.1f' fill='#ffffff'/>"
                % (cx - 1.5 * k, cy, 6.5 * k, 5 * k, SYM, cx + 3.5 * k, cy, cx + 9 * k, cy - 5 * k, cx + 9 * k, cy + 5 * k, SYM,
                   cx - 4.5 * k, cy - 1.2 * k, 1.2 * k))
    # star
    return "<polygon points='%s' fill='%s'/>" % (" ".join("%.1f,%.1f" % (x, y) for x, y in
                                                         star_pts(cx, cy, 9.5 * k, 4.0 * k)), SYM)


def key_parts(sym, unit, W, ky, fs=15):
    """Key: <picture> stands for 1 child."""
    keytxt = "stands for " + fmt(1, unit)
    kw = tw("Key:", fs, True) + 32 + tw(keytxt, fs)
    x = (W - kw) / 2
    s = [text(x, ky, "Key:", fs, anchor="start", bold=True)]
    x += tw("Key:", fs, True) + 16
    s.append(symbol(sym, x, ky - 5))
    s.append(text(x + 14, ky, keytxt, fs, anchor="start"))
    return "".join(s), kw


def key_w(unit, fs=15):
    return tw("Key:", fs, True) + 32 + tw("stands for " + fmt(1, unit), fs)


def pic_svg(title, cats, vals, sym, unit, minsym=5):
    """Horizontal picture graph: one row for each group, 1 picture = 1."""
    fs, rh, gap = 15, 26, 23
    lw = int(max(tw(c, fs) for c in cats) + 22)
    m = max(max(vals), minsym)
    W = int(max(lw + 12 + m * gap + 14, tw(title, 16, True) + 16, key_w(unit) + 16))
    top = 28
    s = [text(W / 2, 19, title, 16, bold=True)]
    H_tab = len(cats) * rh
    s.append("<rect x='4' y='%d' width='%d' height='%d' fill='none' stroke='%s' stroke-width='1.5'/>" % (top, W - 8, H_tab, LINE))
    s.append("<rect x='5' y='%d' width='%d' height='%d' fill='%s'/>" % (top + 1, lw - 6, H_tab - 2, PFILL))
    s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='1.5'/>" % (lw, top, lw, top + H_tab, LINE))
    for i, (c, v) in enumerate(zip(cats, vals)):
        y = top + i * rh
        if i:
            s.append("<line x1='4' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='1'/>" % (y, W - 4, y, GRID))
        s.append(text(lw - 8, y + 18, c, fs, anchor="end"))
        for j in range(v):
            s.append(symbol(sym, lw + 12 + j * gap + 9, y + rh / 2))
    ky = top + H_tab + 22
    s.append(key_parts(sym, unit, W, ky)[0])
    return svg_wrap(W, ky + 8, "".join(s), "picture graph: " + title.lower())


def vpic_svg(title, cats, vals, sym, unit, minsym=5):
    """Vertical picture graph: one column for each group, pictures stacked from the bottom."""
    fs, gap = 15, 22
    cw = int(max(max(tw(c, fs) for c in cats) + 14, 46))
    m = max(max(vals), minsym)
    tot = cw * len(cats)
    W = int(max(tot + 12, tw(title, 16, True) + 16, key_w(unit) + 16))
    x0 = (W - tot) / 2
    top = 30
    ch = m * gap + 10
    base = top + ch
    s = [text(W / 2, 19, title, 16, bold=True)]
    s.append("<rect x='%.1f' y='%d' width='%d' height='%d' fill='none' stroke='%s' stroke-width='1.5'/>" % (x0, top, tot, ch + 26, LINE))
    s.append("<rect x='%.1f' y='%d' width='%d' height='24' fill='%s'/>" % (x0 + 1, base + 1, tot - 2, PFILL))
    s.append("<line x1='%.1f' y1='%d' x2='%.1f' y2='%d' stroke='%s' stroke-width='1.5'/>" % (x0, base, x0 + tot, base, LINE))
    for i, (c, v) in enumerate(zip(cats, vals)):
        x = x0 + i * cw
        if i:
            s.append("<line x1='%.1f' y1='%d' x2='%.1f' y2='%d' stroke='%s' stroke-width='1'/>" % (x, top, x, base + 26, GRID))
        s.append(text(x + cw / 2, base + 18, c, fs))
        for j in range(v):
            s.append(symbol(sym, x + cw / 2, base - 5 - gap / 2 - j * gap + 1))
    ky = base + 26 + 22
    s.append(key_parts(sym, unit, W, ky)[0])
    return svg_wrap(W, ky + 8, "".join(s), "picture graph: " + title.lower())


def uneven_svg(title, cats, vals, sym):
    """Two rows that do not line up: big pictures far apart and small pictures close together."""
    lw = int(max(tw(c, 15) for c in cats) + 22)
    big, small = vals
    W = int(max(lw + 12 + big * 50 + 6, lw + 12 + small * 18 + 6, tw(title, 16, True) + 16))
    s = [text(W / 2, 19, title, 16, bold=True)]
    s.append(text(lw - 8, 51, cats[0], 15, anchor="end"))
    s.append(text(lw - 8, 87, cats[1], 15, anchor="end"))
    for j in range(big):
        s.append(symbol(sym, lw + 22 + j * 50, 46, 1.35))
    for j in range(small):
        s.append(symbol(sym, lw + 14 + j * 18, 82, 0.7))
    s.append("<line x1='%d' y1='28' x2='%d' y2='100' stroke='%s' stroke-width='1.5'/>" % (lw, lw, LINE))
    return svg_wrap(W, 106, "".join(s), "picture graph with pictures of different sizes")


def row_svg(n, sym, label):
    """One row of pictures to count."""
    gap = 24
    W = n * gap + 16
    s = ["<rect x='1' y='1' width='%d' height='32' rx='4' fill='#ffffff' stroke='%s' stroke-width='1.5'/>" % (W - 2, GRID)]
    for j in range(n):
        s.append(symbol(sym, 8 + gap / 2 + j * gap, 17))
    return svg_wrap(W, 34, "".join(s), label)


# ------------------------------------------------------------ question builders
def ask_count(P, q, v, near, unit, extra=""):
    """near = the value of the row next door (reading the wrong row)."""
    return mcq(P + q, fmt(v, unit), fl([v - 1, v + 1, near, v + 2], unit),
               "Each picture stands for 1. Touch each picture once and count: %s. So %s.%s"
               % (", ".join(str(k) for k in range(1, v + 1)), fmt(v, unit), extra))


def ask_more(P, q, a, b, an, bn, wrong_row, unit, fewer=False):
    """a > b. wrong_row = the difference with the wrong row."""
    d = a - b
    assert d > 0 and wrong_row != d
    word = "fewer" if fewer else "more"
    return mcq(P + q, fmt(d, unit), fl([a + b, wrong_row, a, d + 1], unit),
               "%s: %d. %s: %d. How many %s means take away: %d − %d = %d. (%d adds them.)"
               % (an, a, bn, b, word, a, b, d, a + b))


# ------------------------------------------------------------ set 1: count the pictures
def set_count(rnd):
    its = []
    fc, fv = ["Banana", "Mango", "Durian", "Rambutan"], [5, 7, 3, 6]
    G1 = fig(pic_svg("Our favourite fruits", fc, fv, "face", CH))
    its.append(ask_count(G1, "How many children chose mango?", 7, 5, CH, " (5 is the Banana row above.)"))
    its.append(ask_count(G1, "How many children chose durian?", 3, 7, CH, " (7 is the Mango row above.)"))
    its.append(ask_count(G1, "How many children chose rambutan?", 6, 3, CH, " (3 is the Durian row above.)"))
    its.append(ask_count(G1, "How many children chose banana?", 5, 7, CH, " (7 is the Mango row below.)"))
    its.append(mcq(G1 + "Which fruit has 6 pictures?", "Rambutan", ["Mango", "Banana", "Durian"],
                   "Count each row: banana 5, mango 7, durian 3, rambutan 6. Rambutan has 6 pictures."))
    its.append(mcq(G1 + "What does each picture stand for?", "1 child", ["2 children", "1 fruit", "5 children"],
                   "Look at the key. One picture stands for 1 child."))
    pc, pv = ["Cat", "Dog", "Fish", "Hamster"], [4, 6, 8, 2]
    G2 = fig(vpic_svg("Pets in our class", pc, pv, "circle", PET))
    its.append(ask_count(G2, "How many cats are there?", 4, 6, ("cat", "cats"), " (6 is the Dog column next to it.)"))
    its.append(ask_count(G2, "How many fish are there?", 8, 6, FISH, " (6 is the Dog column next to it.)"))
    its.append(ask_count(G2, "How many hamsters are there?", 2, 8, ("hamster", "hamsters"), " (8 is the Fish column next to it.)"))
    its.append(mcq(G2 + "Which pet has 6 pictures?", "Dog", ["Fish", "Cat", "Hamster"],
                   "Count each column: cat 4, dog 6, fish 8, hamster 2. Dog has 6 pictures."))
    its.append(mcq(G2 + "Which pet has 2 pictures?", "Hamster", ["Cat", "Dog", "Fish"],
                   "The Hamster column has only 2 pictures. So there are 2 hamsters."))
    sc, sv = ["Bus", "Car", "MRT", "Walk"], [9, 4, 6, 3]
    G3 = fig(pic_svg("How we go to school", sc, sv, "face", CH))
    its.append(ask_count(G3, "How many children go by bus?", 9, 4, CH, " (4 is the Car row below.)"))
    its.append(ask_count(G3, "How many children take the MRT?", 6, 4, CH, " (4 is the Car row above.)"))
    its.append(ask_count(G3, "How many children walk to school?", 3, 6, CH, " (6 is the MRT row above.)"))
    its.append(mcq(G3 + "Which row has 4 pictures?", "Car", ["Bus", "MRT", "Walk"],
                   "Count each row: bus 9, car 4, MRT 6, walk 3. The Car row has 4 pictures."))
    its.append(mcq(G3 + "Wei Ming counts the Bus row and gets 10. What went wrong?", "He counted one twice",
                   ["He missed one", "He is right", "He read the Car row"],
                   "The Bus row has 9 pictures. 10 is 1 too many, so he counted one picture twice. "
                   "Touch each picture only once."))
    wc, wv = ["Sunny", "Rainy", "Cloudy"], [8, 10, 5]
    G4 = fig(vpic_svg("Weather in May", wc, wv, "square", DAY))
    its.append(ask_count(G4, "How many days were rainy?", 10, 8, DAY, " (8 is the Sunny column.)"))
    its.append(ask_count(G4, "How many days were sunny?", 8, 10, DAY, " (10 is the Rainy column.)"))
    its.append(mcq(G4 + "Which weather has 5 pictures?", "Cloudy", ["Sunny", "Rainy", "None of them"],
                   "Count each column: sunny 8, rainy 10, cloudy 5. Cloudy has 5 pictures."))
    R = fig(row_svg(8, "star", "a row of stars"))
    its.append(mcq(R + "Siti draws 1 star for each friend. How many friends?", fmt(8, ("friend", "friends")),
                   fl([7, 9, 1], ("friend", "friends")),
                   "1 star stands for 1 friend. Count the stars: 1, 2, 3, 4, 5, 6, 7, 8. So 8 friends."))
    assert len(its) == 20
    return {"title": "Count the pictures", "items": its}


# ------------------------------------------------------------ set 2: most and fewest
def set_most(rnd):
    its = []
    fc, fv = ["Chicken rice", "Noodles", "Prata", "Fried rice"], [8, 5, 9, 6]
    G5 = fig(pic_svg("Favourite canteen food", fc, fv, "face", CH))
    its.append(mcq(G5 + "Which food did the most children choose?", "Prata", ["Chicken rice", "Fried rice", "Noodles"],
                   "The pictures line up, so the longest row has the most. Prata has 9. Chicken rice has only 8."))
    its.append(mcq(G5 + "Which food did the fewest children choose?", "Noodles", ["Fried rice", "Prata", "Chicken rice"],
                   "The shortest row has the fewest. Noodles has 5 pictures."))
    its.append(mcq(G5 + "Fried rice or noodles: which did more children choose?", "Fried rice",
                   ["Noodles", "They are the same", "You cannot tell"],
                   "Fried rice has 6 pictures and noodles has 5. 6 is more than 5. So more children chose fried rice."))
    its.append(mcq(G5 + "Which food has 1 more picture than chicken rice?", "Prata", ["Fried rice", "Noodles", "Chicken rice"],
                   "Chicken rice has 8. 8 + 1 = 9. Prata has 9."))
    its.append(mcq(G5 + "Put the foods in order, from most to fewest.", "Prata, Chicken rice, Fried rice, Noodles",
                   ["Noodles, Fried rice, Chicken rice, Prata", "Chicken rice, Noodles, Prata, Fried rice",
                    "Prata, Fried rice, Chicken rice, Noodles"],
                   "Prata 9, chicken rice 8, fried rice 6, noodles 5. Most to fewest: 9, 8, 6, 5."))
    tc, tv = ["Ball", "Car", "Doll", "Robot"], [3, 7, 5, 4]
    G6 = fig(vpic_svg("Toys in the box", tc, tv, "square", ("toy", "toys")))
    its.append(mcq(G6 + "Which toy is there the most of?", "Car", ["Doll", "Robot", "Ball"],
                   "The tallest column has the most. Car has 7 pictures."))
    its.append(mcq(G6 + "Which toy is there the fewest of?", "Ball", ["Robot", "Doll", "Car"],
                   "The shortest column has the fewest. Ball has 3 pictures."))
    its.append(mcq(G6 + "Which toy has 1 fewer than the dolls?", "Robot", ["Ball", "Car", "Doll"],
                   "Doll has 5. 5 − 1 = 4. Robot has 4 pictures."))
    its.append(mcq(G6 + "Put the toys in order, from fewest to most.", "Ball, Robot, Doll, Car",
                   ["Car, Doll, Robot, Ball", "Ball, Car, Doll, Robot", "Robot, Ball, Doll, Car"],
                   "Ball 3, robot 4, doll 5, car 7. Fewest to most: 3, 4, 5, 7."))
    U1 = fig(uneven_svg("Favourite colour", ["Red", "Blue"], [5, 7], "circle"))
    its.append(mcq(U1 + "Which colour got more votes?", "Blue", ["Red", "They are the same", "You cannot tell"],
                   "Count, do not look at the length. Red has 5 pictures. Blue has 7. "
                   "The Red row looks longer only because its pictures are big and far apart."))
    its.append(mcq(U1 + "Ali says, “Red got more votes.” Is he right?", "No. Blue has 7.",
                   ["Yes. Red is longer.", "No. They are the same.", "Yes. Red has 7."],
                   "Red has 5 and Blue has 7. Ali looked at the length of the row. "
                   "The pictures are not the same size, so we must count."))
    U2 = fig(uneven_svg("Birds in the park", ["Mynah", "Sparrow"], [6, 8], "star"))
    its.append(mcq(U2 + "Which bird did the children see more of?", "Sparrow",
                   ["Mynah", "They are the same", "You cannot tell"],
                   "Count each row. Mynah has 6 pictures. Sparrow has 8. 8 is more than 6. "
                   "The Mynah row is longer, but its pictures are bigger."))
    kc, kv = ["Siti", "Ali", "Mei Ling", "Raju"], [6, 9, 4, 7]
    G7 = fig(pic_svg("Stickers we have", kc, kv, "star", STK))
    its.append(mcq(G7 + "Who has the most stickers?", "Ali", ["Raju", "Siti", "Mei Ling"],
                   "The longest row has the most. Ali has 9 stickers."))
    its.append(mcq(G7 + "Who has the fewest stickers?", "Mei Ling", ["Siti", "Raju", "Ali"],
                   "The shortest row has the fewest. Mei Ling has 4 stickers."))
    its.append(mcq(G7 + "Who has fewer stickers than Siti?", "Mei Ling", ["Raju", "Ali", "Siti"],
                   "Siti has 6. Only Mei Ling has fewer: 4. Raju (7) and Ali (9) have more."))
    its.append(mcq(G7 + "Who has more than Siti but fewer than Ali?", "Raju", ["Mei Ling", "Ali", "Siti"],
                   "Siti has 6 and Ali has 9. Raju has 7. 7 is more than 6 and fewer than 9."))
    dc, dv = ["Water", "Milk", "Juice", "Soya milk"], [6, 4, 6, 3]
    G8 = fig(pic_svg("Drinks at recess", dc, dv, "face", CH))
    its.append(mcq(G8 + "Which two drinks have the same number?", "Water and juice",
                   ["Water and milk", "Milk and soya milk", "Juice and milk"],
                   "Count each row: water 6, milk 4, juice 6, soya milk 3. Water and juice both have 6."))
    its.append(mcq(G8 + "Which drink did the fewest children choose?", "Soya milk", ["Milk", "Water", "Juice"],
                   "The shortest row has the fewest. Soya milk has 3 pictures."))
    its.append(mcq(G8 + "Which drinks did the most children choose?", "Water and juice",
                   ["Water only", "Juice only", "Milk and juice"],
                   "Water has 6 and juice has 6. They are the same, and no row has more. So both have the most."))
    its.append(mcq("When does the longest row show the most?", "When pictures are the same size",
                   ["Always", "When it has a title", "When it is at the top"],
                   "If the pictures are the same size and line up, the longest row has the most. "
                   "If they are not the same size, count the pictures."))
    assert len(its) == 20
    return {"title": "Most and fewest", "items": its}


# ------------------------------------------------------------ set 3: how many more, how many fewer
def set_more(rnd):
    its = []
    zc, zv = ["Orangutan", "Elephant", "Tiger", "Otter"], [9, 6, 4, 7]
    G9 = fig(pic_svg("Favourite zoo animals", zc, zv, "face", CH))
    its.append(ask_more(G9, "How many more children chose the orangutan than the tiger?", 9, 4, "Orangutan", "Tiger",
                        3, CH))
    its.append(ask_more(G9, "How many more children chose the otter than the elephant?", 7, 6, "Otter", "Elephant",
                        3, CH))
    its.append(ask_more(G9, "How many fewer children chose the tiger than the otter?", 7, 4, "Otter", "Tiger",
                        2, CH, fewer=True))
    its.append(ask_more(G9, "How many more children chose the orangutan than the elephant?", 9, 6, "Orangutan",
                        "Elephant", 2, CH))
    its.append(mcq(G9 + "Which animal got 2 fewer than the orangutan?", "Otter", ["Elephant", "Tiger", "Orangutan"],
                   "Orangutan has 9. 9 − 2 = 7. Otter has 7 pictures."))
    its.append(mcq(G9 + "Which animal got 2 more than the tiger?", "Elephant", ["Otter", "Orangutan", "Tiger"],
                   "Tiger has 4. 4 + 2 = 6. Elephant has 6 pictures."))
    its.append(mcq(G9 + "Kumar says orangutan has 13 more than tiger. What went wrong?", "He added 9 and 4",
                   ["He took away", "He is right", "He counted twice"],
                   "Orangutan 9, tiger 4. 9 + 4 = 13, so he added. How many more means take away: 9 − 4 = 5."))
    bc, bv = ["Hui Min", "Jun Jie", "Priya", "Hafiz"], [7, 4, 10, 5]
    G10 = fig(vpic_svg("Books we read", bc, bv, "square", BOOK))
    its.append(ask_more(G10, "How many more books did Priya read than Jun Jie?", 10, 4, "Priya", "Jun Jie", 3, BOOK))
    its.append(ask_more(G10, "How many more books did Hui Min read than Hafiz?", 7, 5, "Hui Min", "Hafiz", 3, BOOK))
    its.append(ask_more(G10, "How many fewer books did Jun Jie read than Hafiz?", 5, 4, "Hafiz", "Jun Jie", 3, BOOK,
                        fewer=True))
    its.append(mcq(G10 + "Jun Jie wants as many books as Hui Min. How many more must he read?", fmt(3, BOOK),
                   fl([11, 6, 7], BOOK),
                   "Hui Min 7, Jun Jie 4. Count on from 4: 5, 6, 7. That is 3 more. 7 − 4 = 3. (11 adds them.)"))
    its.append(mcq(G10 + "Who read 3 more books than Jun Jie?", "Hui Min", ["Hafiz", "Priya", "Jun Jie"],
                   "Jun Jie read 4. 4 + 3 = 7. Hui Min read 7."))
    U3 = fig(uneven_svg("Things in the sky", ["Kites", "Balloons"], [4, 7], "circle"))
    its.append(mcq(U3 + "How many more balloons than kites are there?", fmt(3, ("balloon", "balloons")),
                   fl([11, 4, 7], ("balloon", "balloons")),
                   "Count, do not look at the length. Kites 4, balloons 7. 7 − 4 = 3. (11 adds them.)"))
    rc, rv = ["Wei Ming", "Xin Yi", "Zhi Hao", "Mei Ling"], [8, 10, 6, 9]
    G12 = fig(pic_svg("Red packets we got", rc, rv, "square", RP))
    its.append(ask_more(G12, "How many more red packets did Xin Yi get than Zhi Hao?", 10, 6, "Xin Yi", "Zhi Hao",
                        1, RP))
    its.append(ask_more(G12, "How many fewer red packets did Zhi Hao get than Wei Ming?", 8, 6, "Wei Ming", "Zhi Hao",
                        3, RP, fewer=True))
    its.append(ask_more(G12, "How many more red packets did Mei Ling get than Wei Ming?", 9, 8, "Mei Ling", "Wei Ming",
                        3, RP))
    its.append(mcq(G12 + "Who got 2 more red packets than Zhi Hao?", "Wei Ming", ["Mei Ling", "Xin Yi", "Zhi Hao"],
                   "Zhi Hao got 6. 6 + 2 = 8. Wei Ming got 8."))
    its.append(mcq(G12 + "Who got 1 fewer red packet than Xin Yi?", "Mei Ling", ["Wei Ming", "Zhi Hao", "Xin Yi"],
                   "Xin Yi got 10. 10 − 1 = 9. Mei Ling got 9."))
    G13 = fig(pic_svg("Shells we found", ["Ryan", "Sarah"], [9, 6], "star", SHELL))
    its.append(ask_more(G13, "How many more shells did Ryan find than Sarah?", 9, 6, "Ryan", "Sarah", 6, SHELL))
    its.append(mcq(G13 + "Who found fewer shells? How many fewer?", "Sarah, 3 fewer",
                   ["Ryan, 3 fewer", "Sarah, 15 fewer", "Sarah, 6 fewer"],
                   "Ryan 9, Sarah 6. Sarah has the shorter row. 9 − 6 = 3, so Sarah found 3 fewer."))
    assert len(its) == 20
    return {"title": "How many more? How many fewer?", "items": its}


# ------------------------------------------------------------ set 4: totals
def set_total(rnd):
    its = []
    fc, fv = ["Apple", "Pear", "Orange", "Banana"], [6, 4, 8, 5]
    G14 = fig(pic_svg("Fruits in the basket", fc, fv, "apple", FR))
    its.append(mcq(G14 + "How many fruits are there in all?", fmt(23, FR), fl([22, 4, 24], FR),
                   "Add every row: 6 + 4 + 8 + 5 = 23. (4 is the number of rows, not fruits.)"))
    its.append(mcq(G14 + "How many apples and oranges are there altogether?", fmt(14, FR), fl([2, 10, 13], FR),
                   "Apples 6, oranges 8. Altogether means add: 6 + 8 = 14. (2 takes away. 10 adds the Pear row.)"))
    its.append(mcq(G14 + "How many fruits are <b>not</b> oranges?", fmt(15, FR), fl([23, 8, 10], FR),
                   "Add the other rows: 6 + 4 + 5 = 15. (23 is all the fruits. 10 forgets the Banana row.)"))
    its.append(mcq(G14 + "How many pears and bananas are there altogether?", fmt(9, FR), fl([1, 12, 8], FR),
                   "Pears 4, bananas 5. 4 + 5 = 9. (1 takes away. 12 adds the Orange row instead.)"))
    its.append(mcq(G14 + "Mum puts in 2 more apples. How many fruits are there now?", fmt(25, FR), fl([23, 8, 21], FR),
                   "There are 23 fruits. 2 more: 23 + 2 = 25. (8 is the new Apple row only. 21 takes away.)"))
    lc, lv = ["Monday", "Tuesday", "Wednesday", "Thursday"], [8, 5, 10, 7]
    G15 = fig(pic_svg("Children at the library", lc, lv, "face", CH))
    its.append(mcq(G15 + "How many children came on the four days?", fmt(30, CH), fl([29, 4, 31], CH),
                   "Add every row: 8 + 5 + 10 + 7 = 30. (4 is the number of days.)"))
    its.append(mcq(G15 + "How many children came on Monday and Tuesday?", fmt(13, CH), fl([3, 18, 12], CH),
                   "Monday 8, Tuesday 5. 8 + 5 = 13. (3 takes away. 18 adds Wednesday instead of Tuesday.)"))
    its.append(mcq(G15 + "How many children came on Wednesday and Thursday?", fmt(17, CH), fl([3, 15, 16], CH),
                   "Wednesday 10, Thursday 7. 10 + 7 = 17. (3 takes away. 15 adds Monday instead of Wednesday.)"))
    its.append(mcq(G15 + "How many children did <b>not</b> come on Wednesday?", fmt(20, CH), fl([30, 10, 13], CH),
                   "Add the other days: 8 + 5 + 7 = 20. Or 30 − 10 = 20. (13 forgets Thursday.)"))
    its.append(mcq(G15 + "The library wants 40 children. How many more must come?", fmt(10, CH), fl([70, 30, 11], CH),
                   "30 children came. Count on from 30 to 40: that is 10. 40 − 30 = 10. (70 adds 40 + 30.)"))
    tc, tv = ["Red", "Blue", "Green", "Yellow"], [6, 9, 4, 7]
    G16 = fig(vpic_svg("Beanbags on Sports Day", tc, tv, "circle", BAG))
    its.append(mcq(G16 + "How many beanbags are there in all?", fmt(26, BAG), fl([25, 4, 27], BAG),
                   "Add every column: 6 + 9 + 4 + 7 = 26. (4 is the number of teams.)"))
    its.append(mcq(G16 + "How many beanbags did Red and Blue get altogether?", fmt(15, BAG), fl([3, 10, 16], BAG),
                   "Red 6, Blue 9. 6 + 9 = 15. (3 takes away. 10 adds Green instead of Blue.)"))
    its.append(mcq(G16 + "How many beanbags did Green and Yellow get altogether?", fmt(11, BAG), fl([3, 13, 10], BAG),
                   "Green 4, Yellow 7. 4 + 7 = 11. (3 takes away. 13 adds Red instead of Green.)"))
    its.append(mcq(G16 + "How many beanbags are <b>not</b> Blue?", fmt(17, BAG), fl([26, 9, 10], BAG),
                   "Add the other teams: 6 + 4 + 7 = 17. (26 is all of them. 10 forgets Yellow.)"))
    pairs = {("Red", "Green"): 10, ("Blue", "Green"): 13, ("Red", "Yellow"): 13, ("Yellow", "Green"): 11}
    for (a, b), v in pairs.items():
        assert tv[tc.index(a)] + tv[tc.index(b)] == v
    its.append(mcq(G16 + "Which two teams have 10 beanbags altogether?", "Red and Green",
                   ["Blue and Green", "Red and Yellow", "Yellow and Green"],
                   "Red 6 + Green 4 = 10. (Blue and Green make 13. Red and Yellow make 13. Yellow and Green make 11.)"))
    kc, kv = ["Ethan", "Chloe", "Ryan"], [12, 9, 11]
    G17 = fig(pic_svg("Stars on the chart", kc, kv, "star", STAR))
    its.append(mcq(G17 + "How many stars are there in all?", fmt(32, STAR), fl([31, 3, 21], STAR),
                   "Add every row: 12 + 9 + 11 = 32. (3 is the number of children. 21 forgets Ryan.)"))
    its.append(mcq(G17 + "How many stars do Ethan and Ryan have altogether?", fmt(23, STAR), fl([1, 21, 22], STAR),
                   "Ethan 12, Ryan 11. Add tens, then ones: 10 + 10 = 20 and 2 + 1 = 3. 20 + 3 = 23. "
                   "(1 takes away. 21 adds Chloe instead of Ryan.)"))
    its.append(mcq(G17 + "The children want 40 stars in all. How many more do they need?", fmt(8, STAR),
                   fl([72, 32, 7], STAR),
                   "They have 32. Count on from 32 to 40: 33, 34, 35, 36, 37, 38, 39, 40. That is 8. "
                   "(72 adds 40 + 32.)"))
    its.append(mcq(G17 + "Chloe gets 3 more stars. How many stars are there in all now?", fmt(35, STAR),
                   fl([12, 32, 29], STAR),
                   "There are 32 stars. 3 more: 32 + 3 = 35. (12 is Chloe’s new row only. 29 takes away.)"))
    assert sum(kv) + 3 == 35
    its.append(mcq("A picture graph has rows of 10, 10 and 5 pictures. How many pictures in all?",
                   "25 pictures", ["15 pictures", "3 pictures", "20 pictures"],
                   "Count on by tens, then ones: 10, 20, then 21, 22, 23, 24, 25. (15 adds only one 10. "
                   "20 forgets the 5.)"))
    assert len(its) == 20
    return {"title": "Find the total", "items": its}


# ------------------------------------------------------------ set 5: word problems
def set_words(rnd):
    its = []
    fc, fv = ["Durian", "Mango", "Watermelon", "Banana"], [4, 9, 6, 7]
    G19 = fig(pic_svg("Favourite fruits of Class 1A", fc, fv, "face", CH))
    its.append(mcq(G19 + "Each child chose one fruit. How many children are in Class 1A?", fmt(26, CH),
                   fl([25, 4, 27], CH),
                   "Add every row: 4 + 9 + 6 + 7 = 26. Each child chose once, so there are 26 children. "
                   "(4 is the number of fruits.)"))
    its.append(mcq(G19 + "Which sentence is true?", "Mango is the favourite.",
                   ["Durian is the favourite.", "Banana has 2 more than mango.", "Watermelon has the fewest."],
                   "Mango has the longest row (9), so it is the favourite. Durian has the fewest (4). "
                   "Mango has 2 more than banana, not the other way."))
    its.append(mcq(G19 + "3 more children chose durian. How many chose durian now?", fmt(7, CH), fl([4, 1, 12], CH),
                   "Durian had 4. 3 more: 4 + 3 = 7. (1 takes away. 12 adds 3 to the Mango row.)"))
    its.append(mcq(G19 + "Mrs Lim buys 1 fruit for each child who chose mango or banana. How many fruits?",
                   fmt(16, FR), fl([2, 15, 13], FR),
                   "Mango 9, banana 7. 9 + 7 = 16 fruits. (2 takes away. 15 adds watermelon instead of banana.)"))
    its.append(mcq(G19 + "Which fruit did 2 more children choose than durian?", "Watermelon", ["Mango", "Banana", "Durian"],
                   "Durian has 4. 4 + 2 = 6. Watermelon has 6."))
    pc, pv = ["Cat", "Dog", "Fish", "Bird", "Rabbit"], [5, 7, 8, 3, 2]
    G20 = fig(vpic_svg("Pets of Primary 1 children", pc, pv, "circle", PET))
    its.append(mcq(G20 + "How many pets are there in all?", fmt(25, PET), fl([24, 5, 26], PET),
                   "Add every column: 5 + 7 + 8 + 3 + 2 = 25. (5 is the number of kinds of pets.)"))
    its.append(mcq(G20 + "Jun Jie says, “There are more dogs than fish.” Is he right?", "No. Fish has 8.",
                   ["Yes. Dog has 7.", "No. They are the same.", "Yes. Dog has 8."],
                   "Dog has 7 and fish has 8. 8 is more than 7, so there are more fish. Jun Jie is not right."))
    its.append(mcq(G20 + "How many cats, dogs and rabbits are there altogether?", fmt(14, PET), fl([12, 25, 15], PET),
                   "Cats 5, dogs 7, rabbits 2. 5 + 7 + 2 = 14. (12 forgets the rabbits. 25 is all the pets.)"))
    its.append(mcq(G20 + "How many more fish than birds are there?", fmt(5, PET), fl([11, 1, 8], PET),
                   "Fish 8, birds 3. 8 − 3 = 5. (11 adds them. 1 compares fish with dogs.)"))
    its.append(mcq(G20 + "2 children get a new hamster each. How many pets are there now?", fmt(27, PET),
                   fl([25, 2, 23], PET),
                   "There are 25 pets. 2 more: 25 + 2 = 27. (23 takes away.)"))
    vc, vv = ["Zoo", "Sentosa", "Gardens by the Bay", "East Coast Park"], [7, 5, 9, 4]
    G21 = fig(pic_svg("Places we visited in June", vc, vv, "face", CH))
    its.append(mcq(G21 + "Which place did the most children visit?", "Gardens by the Bay",
                   ["Zoo", "Sentosa", "East Coast Park"],
                   "The longest row has the most. Gardens by the Bay has 9 pictures."))
    its.append(mcq(G21 + "How many children visited the Zoo or Sentosa?", fmt(12, CH), fl([2, 16, 11], CH),
                   "Zoo 7, Sentosa 5. 7 + 5 = 12. (2 takes away. 16 adds Gardens by the Bay instead of Sentosa.)"))
    its.append(mcq(G21 + "How many more children visited the Zoo than East Coast Park?", fmt(3, CH),
                   fl([11, 2, 7], CH),
                   "Zoo 7, East Coast Park 4. 7 − 4 = 3. (11 adds them. 2 compares the Zoo with Sentosa.)"))
    its.append(mcq(G21 + "Kavya went to Sentosa. She adds 1 picture. How many are in the Sentosa row now?",
                   fmt(6, ("picture", "pictures")), fl([5, 4, 10], ("picture", "pictures")),
                   "The Sentosa row has 5. 1 more: 5 + 1 = 6. (4 takes away. 10 adds 1 to the Gardens by the Bay row.)"))
    G23 = fig(vpic_svg("Pets at the pet shop", ["Hamster", "Rabbit"], [9, 4], "circle", PET, minsym=9))
    its.append(mcq(G23 + "The shop sells 3 hamsters. How many hamsters are left?", fmt(6, ("hamster", "hamsters")),
                   fl([12, 5, 3], ("hamster", "hamsters")),
                   "There are 9 hamsters. 3 are sold: 9 − 3 = 6 left. (12 adds. 3 is the number sold. 5 is 9 − 4, the rabbits.)"))
    its.append(mcq(G23 + "How many more hamsters than rabbits are there?", fmt(5, ("hamster", "hamsters")),
                   fl([13, 9, 4], ("hamster", "hamsters")),
                   "Hamsters 9, rabbits 4. 9 − 4 = 5. (13 adds them.)"))
    R = fig(row_svg(6, "fish", "a row of fish"))
    its.append(mcq(R + "Ahmad has these fish. Ali has 3 more. How many fish does Ali have?", fmt(9, FISH),
                   fl([3, 6, 10], FISH),
                   "Ahmad has 6 fish. Ali has 3 more: 6 + 3 = 9. (3 takes away. 6 is Ahmad’s fish.)"))
    R2 = fig(row_svg(8, "apple", "a row of apples"))
    its.append(mcq(R2 + "Farah draws 1 apple for each friend who likes apples. How many friends like apples?",
                   fmt(8, ("friend", "friends")), fl([7, 9, 1], ("friend", "friends")),
                   "1 picture stands for 1 friend. Count the apples: 1, 2, 3, 4, 5, 6, 7, 8. So 8 friends."))
    its.append(mcq("Mei Ling wants to find her friends’ favourite fruit. What should she ask?",
                   "What is your favourite fruit?",
                   ["Do you like apples?", "How many fruits are there?", "What fruit is red?"],
                   "She must ask each friend for their favourite fruit. "
                   "“Do you like apples?” only tells her about apples."))
    its.append(mcq(G21 + "What can you tell from this graph?", "East Coast Park got the fewest.",
                   ["The Zoo is the most fun.", "Everyone went to Sentosa.", "Sentosa is far away."],
                   "A picture graph shows how many children went to each place. East Coast Park has the shortest row (4). "
                   "It does not tell us what is fun or far."))
    assert len(its) == 20
    return {"title": "Word problems: fruits, pets and more", "items": its}


# ------------------------------------------------------------ lesson
def ex(title, q, s, a):
    return ("<div class='sn-ex'><span class='sn-ex-t'>%s</span><p class='sn-ex-q'>%s</p>"
            "<p class='sn-ex-s'>%s</p><p class='sn-ex-a'>Answer: %s</p></div>" % (title, q, s, a))


def table(head, rows, cls="sn-table"):
    h = "".join("<th>%s</th>" % x for x in head)
    b = "".join("<tr>" + "".join("<td>%s</td>" % c for c in r) + "</tr>" for r in rows)
    return "<div class='sn-tw'><table class='%s'><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>" % (cls, h, b)


def body_html():
    fc, fv = ["Apple", "Banana", "Mango", "Durian"], [6, 4, 7, 3]
    pc, pv = ["Cat", "Dog", "Fish"], [5, 3, 6]
    return (
        "<h2>What is a picture graph?</h2>"
        "<p>A <b>picture graph</b> uses pictures to show how many. "
        "Here, <b>1 picture stands for 1</b>. "
        "The <b>key</b> tells you what one picture stands for. "
        "All the pictures are the same size and they line up.</p>"
        "<figure class='sn-fig'>" + pic_svg("Our favourite fruits", fc, fv, "face", CH) +
        "<figcaption>Each picture stands for 1 child. The Banana row has 4 pictures, so 4 children chose banana."
        "</figcaption></figure>" +
        ex("Example 1", "How many children chose mango?",
           "Put your finger on the word Mango. Touch each picture once: 1, 2, 3, 4, 5, 6, 7.", "7 children") +
        "<p>Some picture graphs go up in columns. Read them in the same way.</p>"
        "<figure class='sn-fig'>" + vpic_svg("Pets in our class", pc, pv, "circle", PET) +
        "<figcaption>The Fish column has 6 pictures, so there are 6 fish.</figcaption></figure>"
        "<h2>Most and fewest</h2>"
        "<p>The longest row has the <b>most</b>. The shortest row has the <b>fewest</b>. "
        "This works only when the pictures are the same size. If they are not, count.</p>"
        "<h2>How many more? How many fewer?</h2>"
        "<p>Take the smaller number away from the bigger number.</p>" +
        ex("Example 2", "How many more children chose apple than durian?",
           "Apple 6. Durian 3. 6 − 3 = 3.", "3 more children") +
        "<h2>How many in all?</h2>"
        "<p>Add the numbers in every row.</p>" +
        ex("Example 3", "How many children chose a fruit?", "6 + 4 + 7 + 3 = 20.", "20 children") +
        "<h2>Common mistakes</h2>"
        "<figure class='sn-fig'>" + uneven_svg("Favourite colour", ["Red", "Blue"], [5, 7], "circle") +
        "<figcaption>The Red row looks longer, but Blue has more: 7 is more than 5. Count, do not look at the length."
        "</figcaption></figure>" +
        table(["Mistake", "What to do"], [
            ["Counting a picture twice, or missing one", "Touch each picture once as you count"],
            ["Reading the row above or below", "Put your finger on the label and follow the row"],
            ["Looking at the length when pictures are not the same size", "Count the pictures"],
            ["Adding when the question says how many more", "How many more means take away"],
            ["Giving the number of rows as the total", "Add the pictures in every row"],
        ])
    )


FAQ = [
    {"q": "What do P1 students learn about picture graphs?",
     "a": "In Primary 1, students read picture graphs where one picture stands for one. They count the pictures, find the most and the fewest, and work out how many more, how many fewer and how many in all."},
    {"q": "How do I help my child read a picture graph?",
     "a": "Ask your child to read the title and the key first. Then point to a label and touch each picture in that row once as you count together."},
    {"q": "What is the most common mistake with picture graphs?",
     "a": "The most common mistake is miscounting a row or reading the row next door. Another is judging by how long a row looks when the pictures are not the same size."},
    {"q": "Are picture graphs in the MOE Primary 1 syllabus?",
     "a": "Yes. Reading and interpreting data from picture graphs is part of Statistics in the MOE 2021 Primary 1 Mathematics syllabus. In Primary 2, picture graphs use scales, such as 1 picture for 2."},
]


# ------------------------------------------------------------ assemble
def balance(sets, rnd):
    """Move the answers so every position is right 5 times in each set."""
    for s in sets:
        targets = [p for p in range(4) for _ in range(5)]
        rnd.shuffle(targets)
        for it, t in zip(s["items"], targets):
            corr = it["c"][it["a"]]
            wrong = [c for k, c in enumerate(it["c"]) if k != it["a"]]
            rnd.shuffle(wrong)
            wrong.insert(t, corr)
            it["c"] = wrong
            it["a"] = t
        final = [sum(1 for it in s["items"] if it["a"] == i) for i in range(4)]
        assert final == [5, 5, 5, 5], (s["title"], final)


def mark_large(u, pattern):
    """Tag pictures that must print larger (graphs, rows of pictures) so their labels stay readable."""
    rx = re.compile(r"<svg (?=[^>]*aria-label='" + pattern + ")")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u


def gen_unit():
    rnd = random.Random(61811)
    sets = [set_count(rnd), set_most(rnd), set_more(rnd), set_total(rnd), set_words(rnd)]
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
        "country": "sg", "subject": "maths", "grade": "primary-1", "slug": "picture-graphs", "sort": 11,
        "updated": UPDATED, "pdf_url": "",
        "title": "Primary 1 Picture Graphs",
        "seo_title": "P1 Picture Graphs Worksheets: Free Primary 1 Maths with Answers (MOE Syllabus)",
        "short_title": "Picture Graphs",
        "domain": "Statistics",
        "standard_code": "Primary 1: Statistics",
        "standard_url": "https://www.moe.gov.sg/primary/curriculum/syllabus",
        "standard_text": "Reading and interpreting data from picture graphs",
        "meta_desc": "Free P1 maths: read picture graphs, count pictures, find the most and fewest, how many more "
                     "and how many in all. 100 questions with answers.",
        "key_big": "One picture stands for 1. Count the pictures in a row.",
        "key_sub": "Apple has 6 pictures and durian has 3, so 6 − 3 = 3 more children chose apple.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }
    assert len(u["meta_desc"]) <= 160, len(u["meta_desc"])
    return u


if __name__ == "__main__":
    u = gen_unit()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    mark_large(u, "(picture graph|a row of)")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
