# -*- coding: utf-8 -*-
"""
British Columbia Grade 2 Math: Pictographs (BC Mathematics Curriculum, Data and probability)
  python3 tools/gen_cabc_math_g2_pictographs.py
Pictographs with one-to-one correspondence (1 picture = 1): reading rows, making a pictograph from a tally,
most / fewest / how many more, totals, and asking questions and drawing conclusions in BC contexts.
Wrong answers come from real student mistakes: miscounting by one, reading the wrong row, counting a tally
group of 5 as 4, adding when the question asks “how many more”, counting rows instead of pictures,
and judging rows by length when the pictures are not the same size.
HTML attributes use single quotes (no backslashes in the JSON). Canadian English.
"""
import json, re, math, os, random

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "ca-bc", "math", "grade-2")
UPDATED = "2026-11-02"
GREEN = "#006633"
FILL2 = "#e6f2ea"
RED = "#c0392b"
INK = "#2b2b2b"
GRID = "#c9d3cc"
MUTE = "#555555"
FONT = "Arial, Helvetica, sans-serif"


# ------------------------------------------------------------ helpers
def mcq(q, correct, cands, e):
    """4 choices: correct + 3 unique distractors from real mistakes. Positions are balanced later."""
    correct = str(correct)
    seen = {correct}
    pick = []
    for c in cands:
        c = str(c)
        lead = c.split(" ")[0]
        if c in seen or not c or lead.startswith("-") or lead.startswith("−") or lead == "0":
            continue
        seen.add(c)
        pick.append(c)
        if len(pick) == 3:
            break
    assert len(pick) == 3, (q, correct, cands)
    return {"q": q, "c": pick + [correct], "a": 3, "e": e}


def mcq_fixed(q, choices, ai, e):
    """Choices keep their order (A, B, C, D). The answer position is not moved later."""
    assert len(set(choices)) == 4 and 0 <= ai < 4
    return {"q": q, "c": list(choices), "a": ai, "e": e, "_fix": True}


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


STU = ("student", "students")
B = ("bird", "birds")
D = ("day", "days")
SAL = ("salmon", "salmon")
PET = ("pet", "pets")
BK = ("book", "books")
CAN = ("can", "cans")
VOTE = ("vote", "votes")
LAP = ("lap", "laps")


# ------------------------------------------------------------ symbols
def star_pts(cx, cy, R=9.5, r=4.0):
    pts = []
    for i in range(10):
        ang = -math.pi / 2 + i * math.pi / 5
        rad = R if i % 2 == 0 else r
        pts.append((cx + rad * math.cos(ang), cy + rad * math.sin(ang)))
    return pts


def symbol(kind, cx, cy, col=GREEN):
    if kind == "circle":
        return "<circle cx='%.1f' cy='%.1f' r='8.5' fill='%s'/>" % (cx, cy, col)
    if kind == "square":
        return "<rect x='%.1f' y='%.1f' width='15' height='15' rx='2' fill='%s'/>" % (cx - 7.5, cy - 7.5, col)
    return "<polygon points='%s' fill='%s'/>" % (" ".join("%.1f,%.1f" % p for p in star_pts(cx, cy)), col)


def source_line(y, src):
    return text(8, y, src, 14, anchor="start", col=MUTE, extra=" font-style='italic'")


# ------------------------------------------------------------ tally marks
def tally_marks(x, cy, v):
    """Groups of five: four upright lines and the fifth line across."""
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


def tally_only_svg(v):
    W = max(tally_width(v) + 30, 80)
    return svg_wrap(W, 34, "<rect x='1' y='1' width='%d' height='32' rx='4' fill='#ffffff' stroke='%s' stroke-width='1.5'/>"
                    % (W - 2, GRID) + tally_marks(15, 17, v), "tally marks")


def tally_text(v):
    g, r = v // 5, v % 5
    if g and r:
        return "%s of 5 and %d more. Count %s, then %s. So it is %d." % (
            "1 group" if g == 1 else "%d groups" % g, r, ", ".join(str(5 * k) for k in range(1, g + 1)),
            ", ".join(str(5 * g + k) for k in range(1, r + 1)), v)
    if g:
        return "%s of 5. Count %s. So it is %d." % ("1 group" if g == 1 else "%d groups" % g,
                                                   ", ".join(str(5 * k) for k in range(1, g + 1)), v)
    return "%d single marks. So it is %d." % (r, v)


def group4(v):
    """The mistake of counting each group of 5 as 4."""
    return (v // 5) * 4 + v % 5


def tally_svg(title, head, cats, vals, label):
    """One-column tally table."""
    fs, rh = 15, 30
    c1 = int(max(max(tw(c, fs) for c in cats), tw(head, fs, True)) + 20)
    c2 = int(max(max(tally_width(v) for v in vals) + 26, tw("Tally", fs, True) + 20, 70))
    tot = c1 + c2
    W = int(max(tot + 8, tw(title, 16, True) + 16))
    x0 = (W - tot) / 2
    top = 30
    s = [text(W / 2, 20, title, 16, bold=True)]
    rows = [head] + cats
    for r, c in enumerate(rows):
        y = top + r * rh
        hd = r == 0
        s.append("<rect x='%.1f' y='%d' width='%d' height='%d' fill='%s' stroke='%s' stroke-width='1.5'/>" % (x0, y, c1, rh, FILL2, GREEN))
        s.append("<rect x='%.1f' y='%d' width='%d' height='%d' fill='%s' stroke='%s' stroke-width='1.5'/>"
                 % (x0 + c1, y, c2, rh, FILL2 if hd else "#ffffff", GREEN))
        s.append(text(x0 + 10, y + 20, c, fs, anchor="start", bold=hd))
        if hd:
            s.append(text(x0 + c1 + c2 / 2, y + 20, "Tally", fs, bold=True))
        else:
            s.append(tally_marks(x0 + c1 + 14, y + rh / 2, vals[r - 1]))
    H = top + len(rows) * rh + 6
    return svg_wrap(W, H, "".join(s), label)


# ------------------------------------------------------------ pictograph (one symbol for each)
def key_parts(sym, unit, W, ky, fs=15):
    keytxt = "= " + fmt(1, unit)
    kw = tw("Key:", fs, True) + 32 + tw(keytxt, fs)
    x = (W - kw) / 2
    s = [text(x, ky, "Key:", fs, anchor="start", bold=True)]
    x += tw("Key:", fs, True) + 16
    s.append(symbol(sym, x, ky - 5))
    s.append(text(x + 14, ky, keytxt, fs, anchor="start"))
    return "".join(s), kw


def pic_svg(title, cats, vals, sym, unit, source=None, minsym=4):
    fs, rh, gap = 15, 26, 23
    lw = max(tw(c, fs) for c in cats) + 22
    m = max(max(vals), minsym)
    kw = tw("Key:", 15, True) + 32 + tw("= " + fmt(1, unit), 15)
    W = int(max(lw + 12 + m * gap + 14, tw(title, 16, True) + 16, kw + 16, tw(source, 14) + 16 if source else 0))
    top = 28
    s = [text(W / 2, 19, title, 16, bold=True)]
    H_tab = len(cats) * rh
    s.append("<rect x='4' y='%d' width='%d' height='%d' fill='none' stroke='%s' stroke-width='1.5'/>" % (top, W - 8, H_tab, GREEN))
    s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='1.5'/>" % (lw, top, lw, top + H_tab, GREEN))
    for i, (c, v) in enumerate(zip(cats, vals)):
        y = top + i * rh
        if i:
            s.append("<line x1='4' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='1'/>" % (y, W - 4, y, GRID))
        s.append(text(lw - 8, y + 18, c, fs, anchor="end"))
        for j in range(v):
            s.append(symbol(sym, lw + 12 + j * gap + 9, y + rh / 2))
    ky = top + H_tab + 22
    s.append(key_parts(sym, unit, W, ky)[0])
    H = ky + 8
    if source:
        s.append(source_line(ky + 24, source))
        H = ky + 30
    return svg_wrap(W, H, "".join(s), "pictograph: " + title.lower())


def tally_pic_svg(title, head, cats, tallies, pics, sym, unit, label):
    """Table: category | tally | pictograph row made from the tally."""
    fs, rh, gap = 15, 30, 21
    c1 = int(max(max(tw(c, fs) for c in cats), tw(head, fs, True)) + 20)
    c2 = int(max(max(tally_width(v) for v in tallies) + 26, tw("Tally", fs, True) + 20))
    c3 = int(max(max(pics) * gap + 16, tw("Pictograph", fs, True) + 20))
    tot = c1 + c2 + c3
    kw = tw("Key:", 15, True) + 32 + tw("= " + fmt(1, unit), 15)
    W = int(max(tot + 8, tw(title, 16, True) + 16, kw + 16))
    x0 = (W - tot) / 2
    top = 30
    s = [text(W / 2, 20, title, 16, bold=True)]
    rows = [head] + cats
    for r, c in enumerate(rows):
        y = top + r * rh
        hd = r == 0
        x = x0
        for k, cw in enumerate((c1, c2, c3)):
            s.append("<rect x='%.1f' y='%d' width='%d' height='%d' fill='%s' stroke='%s' stroke-width='1.5'/>"
                     % (x, y, cw, rh, FILL2 if hd or k == 0 else "#ffffff", GREEN))
            x += cw
        s.append(text(x0 + 10, y + 20, c, fs, anchor="start", bold=hd))
        if hd:
            s.append(text(x0 + c1 + c2 / 2, y + 20, "Tally", fs, bold=True))
            s.append(text(x0 + c1 + c2 + c3 / 2, y + 20, "Pictograph", fs, bold=True))
        else:
            s.append(tally_marks(x0 + c1 + 14, y + rh / 2, tallies[r - 1]))
            for j in range(pics[r - 1]):
                s.append(symbol(sym, x0 + c1 + c2 + 8 + j * gap + 9, y + rh / 2))
    ky = top + len(rows) * rh + 22
    s.append(key_parts(sym, unit, W, ky)[0])
    return svg_wrap(W, ky + 8, "".join(s), label)


def rows_panel_svg(v, word, rows, sym, label):
    """A tally at the top and four pictograph rows A to D (one picture)."""
    gap = 22
    m = max(rows)
    lw = 40
    W = int(max(lw + 10 + m * gap + 10, tally_width(v) + tw(word + ":", 15, True) + 60))
    s = []
    tx = 10 + tw(word + ":", 15, True) + 14
    s.append(text(10, 24, word + ":", 15, anchor="start", bold=True))
    s.append("<rect x='%.1f' y='6' width='%d' height='28' rx='4' fill='#ffffff' stroke='%s' stroke-width='1.5'/>"
             % (tx - 2, tally_width(v) + 24, GRID))
    s.append(tally_marks(tx + 10, 20, v))
    top = 46
    rh = 28
    for i, n in enumerate(rows):
        y = top + i * rh
        s.append("<line x1='4' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='1'/>" % (y, W - 4, y, GRID))
        s.append(text(18, y + 20, "ABCD"[i], 17, bold=True))
        for j in range(n):
            s.append(symbol(sym, lw + 10 + j * gap + 9, y + rh / 2))
    s.append("<line x1='4' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='1'/>" % (top + 4 * rh, W - 4, top + 4 * rh, GRID))
    s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='1.5'/>" % (lw - 4, top, lw - 4, top + 4 * rh, GREEN))
    return svg_wrap(W, top + 4 * rh + 6, "".join(s), label)


def uneven_svg():
    """Two rows that do not line up: 5 big, spread-out symbols and 7 small, close ones."""
    s = [text(170, 19, "Favourite sport", 16, bold=True)]
    lw = 84
    s.append(text(lw - 8, 50, "Soccer", 15, anchor="end"))
    s.append(text(lw - 8, 86, "Hockey", 15, anchor="end"))
    for j in range(5):
        s.append("<circle cx='%.1f' cy='45' r='12' fill='%s'/>" % (lw + 18 + j * 54, GREEN))
    for j in range(7):
        s.append("<circle cx='%.1f' cy='81' r='6' fill='%s'/>" % (lw + 12 + j * 18, GREEN))
    s.append("<line x1='%d' y1='28' x2='%d' y2='100' stroke='%s' stroke-width='1.5'/>" % (lw, lw, GREEN))
    return svg_wrap(340, 106, "".join(s), "pictograph with rows that do not line up")


# ------------------------------------------------------------ data used in more than one set
AN_C, AN_V = ["Orca", "Bald eagle", "Salmon", "Black bear"], [6, 4, 7, 5]
WE_C, WE_V = ["Rain", "Cloudy", "Sunny", "Snow"], [7, 4, 2, 1]
BI_C, BI_V = ["Chickadee", "Steller’s jay", "Junco", "Robin"], [8, 3, 6, 5]
FR_C, FR_V = ["Apples", "Cherries", "Blueberries", "Peaches"], [9, 5, 10, 4]


# ------------------------------------------------------------ set 1: read a pictograph
def set_read(rnd):
    its = []
    P1 = fig(pic_svg("Favourite BC animal", AN_C, AN_V, "star", STU, source="Source: Grade 2 class vote"))
    its.append(mcq(P1 + "How many students chose the orca?", fmt(6, STU), fl([5, 7, 4], STU),
                   "Each star = 1 student. Touch each star in the Orca row and count: 1, 2, 3, 4, 5, 6. "
                   "So 6 students. (4 is the Bald eagle row.)"))
    its.append(mcq(P1 + "How many students chose the salmon?", fmt(7, STU), fl([6, 8, 5], STU),
                   "Count the stars in the Salmon row, one at a time: 7 stars. So 7 students. "
                   "(5 is the Black bear row.)"))
    its.append(mcq(P1 + "How many students chose the bald eagle?", fmt(4, STU), fl([3, 5, 6], STU),
                   "The Bald eagle row has 4 stars. Each star = 1 student, so 4 students. "
                   "(6 is the Orca row above it.)"))
    its.append(mcq(P1 + "Which row shows 5 students?", "Black bear", ["Orca", "Salmon", "Bald eagle"],
                   "Count each row: orca 6, bald eagle 4, salmon 7, black bear 5. Black bear has 5 stars."))
    its.append(mcq(P1 + "What does each star stand for?", "1 student", ["2 students", "1 animal", "5 students"],
                   "Look at the key: one star = 1 student. Each student who voted got one star."))
    P2 = fig(pic_svg("Weather in Vancouver", WE_C, WE_V, "square", D, source="Source: our class weather chart"))
    its.append(mcq(P2 + "How many days were rainy?", fmt(7, D), fl([6, 8, 4], D),
                   "Each square = 1 day. Count the squares in the Rain row: 7. So 7 rainy days. "
                   "(4 is the Cloudy row.)"))
    its.append(mcq(P2 + "How many days were sunny?", fmt(2, D), fl([1, 3, 4], D),
                   "The Sunny row has 2 squares, so 2 days were sunny. (4 is the Cloudy row above it.)"))
    its.append(mcq(P2 + "Which weather happened on 4 days?", "Cloudy", ["Rain", "Sunny", "Snow"],
                   "Count each row: rain 7, cloudy 4, sunny 2, snow 1. Cloudy has 4 squares."))
    its.append(mcq(P2 + "How many days had snow?", fmt(1, D), fl([2, 4, 7], D),
                   "The Snow row has only 1 square, so it snowed on 1 day. (2 is the Sunny row.)"))
    P3 = fig(pic_svg("Birds at our feeder", BI_C, BI_V, "circle", B, source="Source: our class bird count"))
    its.append(mcq(P3 + "How many juncos came to the feeder?", fmt(6, B), fl([5, 7, 3], B),
                   "Each circle = 1 bird. Count the Junco row: 6 circles. So 6 juncos. "
                   "(3 is the Steller’s jay row above it.)"))
    its.append(mcq(P3 + "How many Steller’s jays came to the feeder?", fmt(3, B), fl([2, 4, 8], B),
                   "The Steller’s jay row has 3 circles, so 3 Steller’s jays came. (8 is the Chickadee row.)"))
    its.append(mcq(P3 + "Which bird came 8 times?", "Chickadee", ["Junco", "Robin", "Steller’s jay"],
                   "Count each row: chickadee 8, Steller’s jay 3, junco 6, robin 5. The Chickadee row has 8 circles."))
    its.append(mcq(P3 + "How many robins came to the feeder?", fmt(5, B), fl([4, 6, 3], B),
                   "Count the circles in the Robin row: 5. (6 is the Junco row above it.)"))
    P4 = fig(pic_svg("Fruit we like", FR_C, FR_V, "square", STU, source="Source: Grade 2 class vote"))
    its.append(mcq(P4 + "How many students chose blueberries?", fmt(10, STU), fl([9, 11, 5], STU),
                   "Each square = 1 student. Count the Blueberries row: 10 squares. So 10 students. "
                   "(5 is the Cherries row above it.)"))
    its.append(mcq(P4 + "How many students chose apples?", fmt(9, STU), fl([8, 10, 5], STU),
                   "The Apples row has 9 squares, so 9 students chose apples. (5 is the Cherries row.)"))
    its.append(mcq(P4 + "Which fruit has 4 squares?", "Peaches", ["Cherries", "Apples", "Blueberries"],
                   "Count each row: apples 9, cherries 5, blueberries 10, peaches 4. Peaches has 4 squares."))
    its.append(mcq(P4 + "Which fruit has 1 more square than apples?", "Blueberries", ["Cherries", "Peaches", "Apples"],
                   "Apples has 9 squares. 9 + 1 = 10. Blueberries has 10 squares."))
    its.append(mcq("A pictograph has 6 stars in the Soccer row. Each star = 1 student. How many students chose soccer?",
                   fmt(6, STU), fl([1, 7, 5], STU),
                   "One star stands for one student. 6 stars means 6 students."))
    its.append(mcq(P1 + "Which animal has 1 fewer star than the salmon?", "Orca", ["Bald eagle", "Black bear", "Salmon"],
                   "The salmon has 7 stars. 7 − 1 = 6. The Orca row has 6 stars."))
    its.append(mcq(P3 + "Leah counts the Junco row and gets 7. What went wrong?", "She counted a circle twice",
                   ["She read the Robin row", "She is right", "She missed a circle"],
                   "The Junco row has 6 circles. 7 is 1 too many, so she counted one circle twice. "
                   "Touch each circle once as you count."))
    assert len(its) == 20
    return {"title": "Read a pictograph (1 picture = 1)", "items": its}


# ------------------------------------------------------------ set 2: make a pictograph from a tally
def tally_q(T, cat, v, other, unit_word, sym_word):
    pics = "%d %s" % (v, sym_word if v == 1 else sym_word + "s")
    cands = ["%d %ss" % (x, sym_word) for x in (group4(v), v + 1, v - 1, other) if x != v]
    return mcq(T + "How many %ss go in the %s row?" % (sym_word, cat), pics, cands,
               "Read the tally: %s Each %s = 1 %s, so draw %s." % (tally_text(v), sym_word, unit_word, pics))


def set_make(rnd):
    its = []
    sc, sv = ["Walk", "Bus", "Car", "Bike"], [8, 6, 5, 3]
    T1 = fig(tally_svg("How we get to school", "Way", sc, sv, "tally table: how we get to school"))
    its.append(tally_q(T1, "Walk", 8, 6, "student", "circle"))
    its.append(tally_q(T1, "Bus", 6, 8, "student", "circle"))
    its.append(tally_q(T1, "Car", 5, 3, "student", "circle"))
    its.append(tally_q(T1, "Bike", 3, 5, "student", "circle"))
    fc, fv = ["Aquarium", "Science centre", "Farm", "Stanley Park"], [9, 7, 4, 10]
    T2 = fig(tally_svg("Field trip vote", "Place", fc, fv, "tally table: field trip vote"))
    its.append(tally_q(T2, "Aquarium", 9, 7, "student", "star"))
    its.append(tally_q(T2, "Stanley Park", 10, 4, "student", "star"))
    its.append(tally_q(T2, "Science centre", 7, 9, "student", "star"))
    # A to D rows (one picture). The wrong rows come from counting a group of 5 as 4 and miscounting.
    for v, word, rows, ai in [(7, "Rainy days", [6, 7, 8, 5], 1), (9, "Robins", [8, 10, 5, 9], 3),
                              (6, "Hockey", [6, 5, 7, 2], 0)]:
        assert rows[ai] == v and len(set(rows)) == 4
        R = fig(rows_panel_svg(v, word, rows, "circle", "tally and pictograph rows a to d"))
        its.append(mcq_fixed(R + "Each circle = 1. Which row matches the tally?", ["Row A", "Row B", "Row C", "Row D"], ai,
                             "Read the tally: %s Row %s has %d circles. (Counting the group of 5 as 4 gives %d.)"
                             % (tally_text(v), "ABCD"[ai], v, group4(v))))
    # tally and pictograph side by side, one row wrong
    W = [("Favourite snack", "Snack", ["Apples", "Crackers", "Cheese", "Carrots"], [7, 5, 9, 3], 2, 8, "circle",
          "The Cheese tally is 1 group of 5 and 4 more: 9. The Cheese row has only 8 circles. "
          "The group of 5 was counted as 4."),
         ("Our pets", "Pet", ["Dog", "Cat", "Fish", "Hamster"], [6, 10, 4, 2], 2, 5, "square",
          "The Fish tally has 4 marks, but the Fish row has 5 squares. One extra square was drawn."),
         ("Favourite colour", "Colour", ["Red", "Blue", "Green", "Purple"], [5, 8, 6, 3], 0, 4, "star",
          "The Red tally is 1 group of 5: 5. The Red row has only 4 stars. The group of 5 was counted as 4.")]
    for title, head, cats, tal, bad, bv, sym, why in W:
        pics = list(tal)
        pics[bad] = bv
        unit = PET if head == "Pet" else STU
        F = fig(tally_pic_svg(title, head, cats, tal, pics, sym, unit, "tally and pictograph: " + title.lower()))
        its.append(mcq(F + "Which row of the pictograph does not match the tally?", cats[bad],
                       [c for k, c in enumerate(cats) if k != bad],
                       "Check every row: count the tally, then count the pictures. " + why))
    its.append(mcq("The tally for Soccer shows 2 groups of 5 and 3 more. Each ball = 1 student. "
                   "How many balls go in the Soccer row?", "13 balls", ["11 balls", "5 balls", "10 balls"],
                   "Count by 5s for the groups: 5, 10. Then 11, 12, 13. Draw 13 balls. "
                   "(11 counts each group as 4. 5 adds 2 + 3.)"))
    its.append(mcq("Every picture in a pictograph should …", "be the same size and line up",
                   ["be bigger for big numbers", "be a different colour", "stand for 5 things"],
                   "In a Grade 2 pictograph, 1 picture = 1. All pictures are the same size and line up, "
                   "so you can compare the rows."))
    its.append(mcq("Why does a pictograph need a key?", "It tells what 1 picture means",
                   ["It makes the graph pretty", "It gives the title", "It counts the rows"],
                   "The key shows one picture and what it stands for, such as “= 1 student.”"))
    its.append(mcq("Ji-woo’s tally says 12 students chose hockey. Each star = 1 student. How many stars go in the Hockey row?",
                   "12 stars", ["4 stars", "10 stars", "11 stars"],
                   "1 star for each student: 12 students need 12 stars. "
                   "(4 stars draws one star for each group of 5 and one for each extra mark.)"))
    its.append(mcq(fig(tally_only_svg(11)) + "Each picture = 1. How many pictures show this tally?", "11 pictures",
                   ["9 pictures", "10 pictures", "3 pictures"],
                   "Read the tally: " + tally_text(11) + " Draw 11 pictures. (9 counts each group as 4. 3 adds 2 + 1.)"))
    its.append(mcq(fig(tally_only_svg(14)) + "Each picture = 1. How many pictures show this tally?", "14 pictures",
                   ["12 pictures", "13 pictures", "6 pictures"],
                   "Read the tally: " + tally_text(14) + " Draw 14 pictures. (12 counts each group as 4. 6 adds 2 + 4.)"))
    its.append(mcq("A pictograph row has 6 squares. What should the tally for this row show?",
                   "1 group of 5 and 1 more", ["6 groups of 5", "1 group of 5", "1 group of 5 and 6 more"],
                   "6 = 5 + 1. Make one group of 5 (the fifth mark goes across), then 1 more mark."))
    assert len(its) == 20
    return {"title": "Make a pictograph from a tally", "items": its}


# ------------------------------------------------------------ set 3: most, fewest, how many more
def set_compare(rnd):
    its = []
    sc, sv = ["Soccer", "Hockey", "Lacrosse", "Swimming"], [8, 6, 4, 9]
    P1 = fig(pic_svg("Favourite sport", sc, sv, "star", STU, source="Source: Grade 2 class vote"))
    its.append(mcq(P1 + "Which sport did the most students choose?", "Swimming", ["Soccer", "Hockey", "Lacrosse"],
                   "The stars line up, so the longest row has the most. Swimming has 9 stars."))
    its.append(mcq(P1 + "Which sport did the fewest students choose?", "Lacrosse", ["Hockey", "Swimming", "Soccer"],
                   "The shortest row has the fewest. Lacrosse has 4 stars."))
    its.append(mcq(P1 + "How many more students chose swimming than lacrosse?", fmt(5, STU), fl([13, 9, 4], STU),
                   "Swimming 9, lacrosse 4. How many more means take away: 9 − 4 = 5. (13 adds them.)"))
    its.append(mcq(P1 + "How many more students chose soccer than hockey?", fmt(2, STU), fl([14, 1, 4], STU),
                   "Soccer 8, hockey 6. 8 − 6 = 2. (14 adds them. 4 compares soccer with lacrosse, the wrong row.)"))
    its.append(mcq(P1 + "How many fewer students chose lacrosse than soccer?", fmt(4, STU), fl([12, 3, 8], STU),
                   "Soccer 8, lacrosse 4. How many fewer means take away: 8 − 4 = 4. (12 adds them.)"))
    dc, dv = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"], [3, 7, 10, 5, 6]
    P2 = fig(pic_svg("Salmon we saw in the creek", dc, dv, "circle", SAL, source="Source: our class field trip notes"))
    its.append(mcq(P2 + "On which day did the class see the most salmon?", "Wednesday", ["Tuesday", "Friday", "Monday"],
                   "The longest row has the most. Wednesday has 10 circles."))
    its.append(mcq(P2 + "On which day did the class see the fewest salmon?", "Monday", ["Thursday", "Wednesday", "Friday"],
                   "The shortest row has the fewest. Monday has 3 circles."))
    its.append(mcq(P2 + "How many more salmon did they see on Wednesday than on Thursday?", fmt(5, SAL), fl([15, 3, 10], SAL),
                   "Wednesday 10, Thursday 5. 10 − 5 = 5. (15 adds them. 3 compares Wednesday with Tuesday, the wrong row.)"))
    its.append(mcq(P2 + "How many more salmon did they see on Tuesday than on Monday?", fmt(4, SAL), fl([10, 3, 7], SAL),
                   "Tuesday 7, Monday 3. 7 − 3 = 4. (10 adds them.)"))
    its.append(mcq(P2 + "On which day did they see 1 more salmon than on Thursday?", "Friday", ["Tuesday", "Monday", "Wednesday"],
                   "Thursday has 5 circles. 5 + 1 = 6. Friday has 6 circles."))
    U = fig(uneven_svg())
    its.append(mcq(U + "Which sport got more votes?", "Hockey", ["Soccer", "They are the same", "You cannot tell"],
                   "Count, do not look at the length. Soccer has 5 circles and hockey has 7. "
                   "The Soccer row looks longer only because its circles are big and far apart."))
    its.append(mcq(U + "How many more votes did hockey get than soccer?", fmt(2, VOTE), fl([12, 5, 7], VOTE),
                   "Hockey 7, soccer 5. 7 − 5 = 2. (12 adds them.)"))
    ac, av = ["Skiing", "Swimming", "Camping", "Biking"], [7, 5, 7, 3]
    P3 = fig(pic_svg("Favourite Spring Break activity", ac, av, "square", STU, source="Source: Grade 2 class vote"))
    its.append(mcq(P3 + "Which two activities got the same number of votes?", "Skiing and camping",
                   ["Skiing and swimming", "Swimming and biking", "Camping and biking"],
                   "Count each row: skiing 7, swimming 5, camping 7, biking 3. Skiing and camping both have 7."))
    its.append(mcq(P3 + "Which activity did the fewest students choose?", "Biking", ["Swimming", "Camping", "Skiing"],
                   "The shortest row has the fewest. Biking has 3 squares."))
    its.append(mcq(P3 + "How many more students chose skiing than biking?", fmt(4, STU), fl([10, 2, 7], STU),
                   "Skiing 7, biking 3. 7 − 3 = 4. (10 adds them. 2 compares swimming with biking, the wrong row.)"))
    its.append(mcq(P3 + "How many more students need to choose biking so it ties with swimming?", fmt(2, STU),
                   fl([8, 3, 5], STU),
                   "Swimming has 5. Biking has 3. 3 + 2 = 5, so 2 more students. (8 adds 5 + 3.)"))
    its.append(mcq("In a pictograph, the Orca row has 9 stars and the Black bear row has 6 stars. Which is true?",
                   "Orca has 3 more", ["Black bear has 3 more", "Orca has 15 more", "They are the same"],
                   "9 − 6 = 3. Orca has the longer row, so orca has 3 more. (15 adds them.)"))
    its.append(mcq(P1 + "Which sport got 2 fewer votes than soccer?", "Hockey", ["Lacrosse", "Swimming", "Soccer"],
                   "Soccer has 8. 8 − 2 = 6. Hockey has 6 stars."))
    its.append(mcq(P2 + "On which days did they see more than 5 salmon?", "Tuesday, Wednesday, Friday",
                   ["Wednesday only", "Tuesday to Friday", "Monday and Thursday"],
                   "More than 5 means 6 or more. Tuesday 7, Wednesday 10 and Friday 6. "
                   "Thursday has exactly 5, which is not more than 5, so it is not “Tuesday to Friday.”"))
    its.append(mcq(P1 + "Put the sports in order from most to fewest.", "Swimming, Soccer, Hockey, Lacrosse",
                   ["Lacrosse, Hockey, Soccer, Swimming", "Soccer, Hockey, Lacrosse, Swimming", "Swimming, Hockey, Soccer, Lacrosse"],
                   "Swimming 9, soccer 8, hockey 6, lacrosse 4. Most to fewest: 9, 8, 6, 4."))
    assert len(its) == 20
    return {"title": "Most, fewest and how many more", "items": its}


# ------------------------------------------------------------ set 4: find the total
def set_total(rnd):
    its = []
    pc, pv = ["Dog", "Cat", "Fish", "Rabbit"], [9, 6, 4, 2]
    P1 = fig(pic_svg("Our pets", pc, pv, "circle", PET, source="Source: Grade 2 class survey"))
    its.append(mcq(P1 + "How many pets does the pictograph show in all?", fmt(21, PET), fl([20, 4, 22], PET),
                   "Add every row: 9 + 6 + 4 + 2 = 21. (4 is the number of rows, not pets.)"))
    its.append(mcq(P1 + "How many dogs and cats are there altogether?", fmt(15, PET), fl([3, 14, 13], PET),
                   "Dogs 9, cats 6. Altogether means add: 9 + 6 = 15. (3 takes away. 13 adds the Fish row by mistake.)"))
    its.append(mcq(P1 + "How many pets are <b>not</b> dogs?", fmt(12, PET), fl([21, 9, 10], PET),
                   "Add the other rows: 6 + 4 + 2 = 12. (21 is all the pets. 10 forgets the Rabbit row.)"))
    its.append(mcq(P1 + "How many fish and rabbits are there altogether?", fmt(6, PET), fl([2, 10, 7], PET),
                   "Fish 4, rabbits 2. 4 + 2 = 6. (2 takes away. 10 uses the Cat row instead of the Rabbit row.)"))
    wc, wv = ["Rain", "Cloudy", "Sunny", "Fog"], [12, 9, 6, 3]
    P2 = fig(pic_svg("Weather in November", wc, wv, "square", D, source="Source: our class weather chart"))
    its.append(mcq(P2 + "How many days does the pictograph show in all?", fmt(30, D), fl([29, 31, 4], D),
                   "Add every row: 12 + 9 + 6 + 3 = 30. November has 30 days, so this checks out."))
    its.append(mcq(P2 + "How many days had rain or fog?", fmt(15, D), fl([9, 21, 14], D),
                   "Rain 12, fog 3. 12 + 3 = 15. (9 takes away. 21 adds the Cloudy row instead of the Fog row.)"))
    its.append(mcq(P2 + "How many days did <b>not</b> have rain?", fmt(18, D), fl([30, 12, 15], D),
                   "Add the other rows: 9 + 6 + 3 = 18. Or 30 − 12 = 18. (12 is the rainy days.)"))
    its.append(mcq(P2 + "How many days were rainy or cloudy?", fmt(21, D), fl([3, 18, 20], D),
                   "Rain 12, cloudy 9. 12 + 9 = 21. (3 takes away. 18 adds the Sunny row instead of the Cloudy row.)"))
    bc, bv = ["Simran", "Arjun", "Chloe", "Noah"], [8, 5, 11, 7]
    P3 = fig(pic_svg("Books we read in October", bc, bv, "square", BK, source="Source: our reading logs"))
    its.append(mcq(P3 + "How many books did the four friends read in all?", fmt(31, BK), fl([30, 4, 11], BK),
                   "Add every row: 8 + 5 + 11 + 7 = 31. (4 is the number of friends. 11 is only Chloe.)"))
    its.append(mcq(P3 + "How many books did Simran and Chloe read together?", fmt(19, BK), fl([3, 13, 18], BK),
                   "Simran 8, Chloe 11. 8 + 11 = 19. (3 takes away. 13 adds Arjun’s row instead of Chloe’s.)"))
    its.append(mcq(P3 + "How many books did Arjun and Noah read together?", fmt(12, BK), fl([2, 13, 11], BK),
                   "Arjun 5, Noah 7. 5 + 7 = 12. (2 takes away. 13 adds Simran’s row instead of Noah’s.)"))
    its.append(mcq(P3 + "The four friends want to read 40 books. How many more books do they need?", fmt(9, BK),
                   fl([71, 10, 11], BK),
                   "They read 31. Count up from 31 to 40: 9. So 40 − 31 = 9 more books. (71 adds 40 + 31.)"))
    cc, cv = ["Week 1", "Week 2", "Week 3"], [8, 11, 9]
    P4 = fig(pic_svg("Cans for the food bank", cc, cv, "circle", CAN, source="Source: Grade 2 food drive"))
    its.append(mcq(P4 + "How many cans did the class collect in all?", fmt(28, CAN), fl([27, 3, 11], CAN),
                   "Add every row: 8 + 11 + 9 = 28. (3 is the number of weeks. 11 is only week 2.)"))
    its.append(mcq(P4 + "How many cans did they collect in week 1 and week 2?", fmt(19, CAN), fl([3, 17, 20], CAN),
                   "Week 1: 8. Week 2: 11. 8 + 11 = 19. (17 adds week 3 instead of week 2.)"))
    its.append(mcq(P4 + "The class wants 40 cans. How many more cans do they need?", fmt(12, CAN), fl([68, 2, 11], CAN),
                   "They have 28. Count up: 28 to 30 is 2, then 30 to 40 is 10. 2 + 10 = 12 cans. "
                   "(68 adds. 2 stops counting at 30.)"))
    its.append(mcq(P1 + "How many cats and rabbits are there altogether?", fmt(8, PET), fl([4, 10, 7], PET),
                   "Cats 6, rabbits 2. 6 + 2 = 8. (4 takes away. 10 adds the Fish row instead of the Rabbit row.)"))
    its.append(mcq(P1 + "3 more students say they have a fish. How many pets will the pictograph show now?",
                   fmt(24, PET), fl([21, 7, 25], PET),
                   "There are 21 pets now. 3 more: 21 + 3 = 24. (7 is the new Fish row only.)"))
    its.append(mcq("Kai’s pictograph has 3 rows. They have 10, 10 and 6 stars. How many stars are there in all?",
                   "26 stars", ["16 stars", "3 stars", "25 stars"],
                   "Count by 10s, then on: 10, 20, then 21, 22, 23, 24, 25, 26. So 26 stars. (16 adds only one 10.)"))
    its.append(mcq("A pictograph has 14 stars in the Hockey row and 23 stars in the Soccer row. How many stars altogether?",
                   "37 stars", ["9 stars", "36 stars", "47 stars"],
                   "Add tens, then ones: 10 + 20 = 30 and 4 + 3 = 7. 30 + 7 = 37. (9 takes away. 47 adds one ten too many.)"))
    its.append(mcq("There are 25 students in the class. The class pictograph has 22 pictures. "
                   "Each picture = 1 student. How many students have not voted yet?", fmt(3, STU), fl([47, 2, 4], STU),
                   "25 − 22 = 3. Count up from 22: 23, 24, 25. That is 3. (47 adds 25 + 22.)"))
    assert len(its) == 20
    return {"title": "Find the total", "items": its}


# ------------------------------------------------------------ set 5: questions and conclusions
def set_words(rnd):
    its = []
    tc, tv = ["Walk", "Bus", "Car", "Bike"], [9, 4, 7, 3]
    TR = fig(pic_svg("How we get to school", tc, tv, "circle", STU, source="Source: survey in Ms. Gill’s class"))
    its.append(mcq(TR + "What question did the class ask?", "How do you get to school?",
                   ["How far is the school?", "What is your favourite car?", "How many buses are there?"],
                   "The rows are ways to get to school: walk, bus, car and bike. Each student answered "
                   "“How do you get to school?”"))
    its.append(mcq(TR + "Which sentence is true?", "More students walk than come by car.",
                   ["Bike has the most students.", "Bus has 4 more than car.", "Everyone walks to school."],
                   "Walk 9 and car 7: 9 is more than 7, so this is true. Walk has the most, not bike. "
                   "Car has 3 more than bus (7 − 4), not the other way."))
    its.append(mcq(TR + "Arjun says, “Most students in BC walk to school.” Is he right?",
                   "No. The data is from one class.", ["Yes. Walk has the longest row.", "Yes. 9 students walk.",
                                                      "No. Bus has the longest row."],
                   "The source says the data is from Ms. Gill’s class. It tells us about this class only, "
                   "not every student in BC."))
    its.append(mcq(TR + "The class did this survey in June. Why might fewer students bike in January?",
                   "It is cold, wet and dark.", ["The bus is yellow.", "The graph has a title.", "Bikes have 2 wheels."],
                   "In January it is cold and rainy, and it gets dark early, so fewer students bike. "
                   "When we explain data, we think about when it was collected."))
    its.append(mcq(TR + "3 students who come by car start to walk. How many students will walk?", fmt(12, STU),
                   fl([6, 4, 16], STU),
                   "9 students walk now. 3 more will walk: 9 + 3 = 12. (6 takes away. 4 is how many will still come by car. "
                   "16 adds all 7 car students.)"))
    its.append(mcq(TR + "How many students answered the survey?", fmt(23, STU), fl([22, 4, 9], STU),
                   "Each student gave one answer. Add every row: 9 + 4 + 7 + 3 = 23. (4 is the number of rows.)"))
    fc, fv = ["Sack race", "Tug-of-war", "Relay race", "Obstacle course"], [6, 10, 5, 8]
    FD = fig(pic_svg("Sports Day vote", fc, fv, "star", STU, source="Source: Grade 2 class vote"))
    its.append(mcq(FD + "The class can do one activity. Which one will make the most students happy?", "Tug-of-war",
                   ["Obstacle course", "Sack race", "Relay race"],
                   "Tug-of-war has the longest row: 10 students. More students chose it than any other activity."))
    its.append(mcq(FD + "How many students did <b>not</b> choose tug-of-war?", fmt(19, STU), fl([10, 29, 13], STU),
                   "Add the other rows: 6 + 5 + 8 = 19. (29 is everyone. 13 forgets the Sack race row.)"))
    its.append(mcq(FD + "3 more students vote for the obstacle course. Which activity has the most votes now?",
                   "Obstacle course", ["Tug-of-war", "Sack race", "Relay race"],
                   "Obstacle course now has 8 + 3 = 11 votes. 11 is more than 10 (tug-of-war)."))
    its.append(mcq(FD + "Leah says, “Relay race got half as many votes as tug-of-war.” Is she right?",
                   "Yes. 5 is half of 10.", ["No. 5 is not half of 10.", "No. Relay race has more.", "Yes. 6 is half of 10."],
                   "Relay race 5, tug-of-war 10. 5 + 5 = 10, so 5 is half of 10. She is right."))
    its.append(mcq("Mei wants to find out the favourite fruit of her class. Which question should she ask?",
                   "What is your favourite fruit?", ["Do you like apples?", "How many fruits are there?",
                                                     "What fruit is red?"],
                   "Her question must ask each student for their favourite fruit. "
                   "“Do you like apples?” only tells her about apples."))
    its.append(mcq("Ethan wants to know which birds visit the school feeder. What is the best way to collect the data?",
                   "Watch the feeder and tally", ["Ask friends their favourite bird", "Count the trees",
                                                   "Read a book about birds"],
                   "He can find out by watching. He makes one tally mark for each bird he sees at the feeder. "
                   "A favourite bird is not the same as a bird that comes to the feeder."))
    its.append(mcq("Nadia asks her class, “Have you seen an orca?” Which rows should her pictograph have?",
                   "Yes and No", ["Orca and Salmon", "Boys and Girls", "Big and Small"],
                   "Each student can only answer yes or no, so her pictograph needs a Yes row and a No row."))
    its.append(mcq("Lucas asked 24 students. His pictograph has 22 stars. Each star = 1 student. What went wrong?",
                   "He missed 2 students", ["He drew 2 too many", "He is right", "He asked 2 too many"],
                   "24 students need 24 stars. 24 − 22 = 2, so 2 stars are missing. Check each tally mark again."))
    its.append(mcq("A class will make a pictograph of favourite snacks. What must it have?", "A title, labels and a key",
                   ["Only pictures", "Big and small pictures", "A different picture for each child"],
                   "A title tells what the graph is about, the labels name the rows, and the key tells what 1 picture means."))
    its.append(mcq("At the Terry Fox Run, Owen ran 6 laps, Zara ran 9 laps and Ryan ran 4 laps. "
                   "How many more laps did Zara run than Ryan?", fmt(5, LAP), fl([13, 3, 2], LAP),
                   "Zara 9, Ryan 4. 9 − 4 = 5. (13 adds them. 3 compares Zara with Owen, the wrong person.)"))
    its.append(mcq("For the food bank, Hana’s school collected 18 cans in week 1, 24 cans in week 2 and 31 cans in "
                   "week 3. How many cans did they collect?", fmt(73, CAN), fl([42, 55, 49], CAN),
                   "Add all three weeks. 18 + 24 = 42. Then 42 + 31 = 73 cans. "
                   "(42, 55 and 49 add only two of the weeks.)"))
    its.append(mcq("The school wanted 90 cans. They collected 73 cans. How many more cans do they need?",
                   fmt(17, CAN), fl([23, 163, 7], CAN),
                   "90 − 73: count up from 73 to 80 (7), then 80 to 90 (10). 7 + 10 = 17 cans. "
                   "(23 takes 0 from 3 the wrong way. 7 stops counting at 80.)"))
    its.append(mcq("18 students voted for a field trip. 9 chose the aquarium and 5 chose the science centre. "
                   "The rest chose Stanley Park. How many chose Stanley Park?", fmt(4, STU), fl([14, 13, 9], STU),
                   "9 + 5 = 14 students chose the other places. 18 − 14 = 4 chose Stanley Park. "
                   "(14 stops after adding. 13 only takes away 5.)"))
    its.append(mcq(FD + "What can you tell from this pictograph?", "Relay race got the fewest votes.",
                   ["Relay race is boring.", "Everyone likes tug-of-war.", "The sack race is the fastest."],
                   "A pictograph shows how many chose each activity. The Relay race row is the shortest. "
                   "It does not tell us why, or what is boring or fast."))
    assert len(its) == 20
    return {"title": "Questions and conclusions: word problems", "items": its}


# ------------------------------------------------------------ lesson
def ex(title, q, s, a):
    return ("<div class='sn-ex'><span class='sn-ex-t'>%s</span><p class='sn-ex-q'>%s</p>"
            "<p class='sn-ex-s'>%s</p><p class='sn-ex-a'>Answer: %s</p></div>" % (title, q, s, a))


def table(head, rows, cls="sn-table"):
    h = "".join("<th>%s</th>" % x for x in head)
    b = "".join("<tr>" + "".join("<td>%s</td>" % c for c in r) + "</tr>" for r in rows)
    return "<div class='sn-tw'><table class='%s'><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>" % (cls, h, b)


def body_html():
    sp = ["Soccer", "Hockey", "Lacrosse", "Skiing"]
    spv = [7, 4, 6, 3]
    return (
        "<h2>One picture for each</h2>"
        "<p>A <b>pictograph</b> uses pictures to show data. In Grade 2, <b>1 picture = 1</b>. "
        "One star can stand for one student, one day or one bird. "
        "The <b>key</b> tells you what one picture means. "
        "The pictures are all the same size and line up, so the rows are easy to compare.</p>"
        "<figure class='sn-fig'>" + pic_svg("Favourite sport", sp, spv, "star", STU, source="Source: Grade 2 class vote") +
        "<figcaption>Each star = 1 student. The Hockey row has 4 stars, so 4 students chose hockey.</figcaption></figure>" +
        ex("Example", "How many students chose lacrosse?", "Touch each star in the Lacrosse row once: 1, 2, 3, 4, 5, 6.",
           "6 students") +
        "<h2>Make a pictograph from a tally</h2>"
        "<p>Read each tally first. A group of 5 has four lines and one line across. "
        "Then draw one picture for each tally mark, in the same row.</p>"
        "<figure class='sn-fig'>" + tally_pic_svg("How we get to school", "Way", ["Walk", "Bus", "Car"], [8, 5, 3],
                                                  [8, 5, 3], "circle", STU, "tally and pictograph: how we get to school") +
        "<figcaption>Walk: 1 group of 5 and 3 more is 8, so draw 8 circles.</figcaption></figure>"
        "<h2>Most, fewest and how many more</h2>"
        "<p>The longest row has the <b>most</b>. The shortest row has the <b>fewest</b>. "
        "To find <b>how many more</b>, take the smaller number away from the bigger number.</p>" +
        ex("Example", "In the sport pictograph, how many more students chose soccer than skiing?",
           "Soccer 7, skiing 3. 7 − 3 = 4.", "4 more students") +
        "<h2>Find the total</h2>"
        "<p>To find how many in all, add the numbers in every row. "
        "To find how many did <b>not</b> choose something, add all the other rows.</p>" +
        ex("Example", "How many students voted in the sport pictograph?", "7 + 4 + 6 + 3 = 20.", "20 students") +
        "<h2>Ask a question, then explain</h2>"
        "<p>Start with a question, such as “What is your favourite sport?” Collect the answers with tally marks, "
        "make the pictograph, and then say what it tells you. "
        "A pictograph of one class tells you about that class, not about every student in BC.</p>"
        "<h2>Common mistakes</h2>" +
        table(["Mistake", "What to do instead"], [
            ["Counting one picture twice or skipping one", "Touch each picture once as you count"],
            ["Reading the row above or below", "Put your finger on the label and follow the row"],
            ["Counting a group of 5 tally marks as 4", "The line across is the 5th mark"],
            ["Adding when the question says how many more", "How many more means take away"],
            ["Looking at how long a row is when pictures are different sizes", "Count the pictures"],
            ["Giving the number of rows as the total", "Add the pictures in every row"],
        ])
    )


FAQ = [
    {"q": "What do Grade 2 students learn about pictographs in BC math?",
     "a": "In the BC curriculum, Grade 2 students show data in concrete graphs and pictographs using one-to-one correspondence, so each picture stands for one thing. They read the graph, compare rows, find totals and explain what the data tells them."},
    {"q": "What does one-to-one correspondence mean in a pictograph?",
     "a": "It means one picture stands for one thing, such as one star for one student. To read the graph, count the pictures in a row."},
    {"q": "How do you make a pictograph from a tally chart?",
     "a": "Count each tally (a group of 5 has a line across), then draw one picture for each mark in that row. Make all the pictures the same size, line them up, and add a title and a key."},
    {"q": "How can I practise pictographs with my child at home?",
     "a": "Ask family members a question, such as their favourite fruit, and tally the answers. Then draw one sticker or picture for each answer and ask which has the most and how many more."},
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
    rnd = random.Random(52810)
    sets = [set_read(rnd), set_make(rnd), set_compare(rnd), set_total(rnd), set_words(rnd)]
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
        "country": "ca-bc", "subject": "math", "grade": "grade-2", "slug": "pictographs", "sort": 10,
        "updated": UPDATED, "pdf_url": "",
        "title": "Pictographs: Read, Make from a Tally, Compare and Find the Total",
        "seo_title": "Grade 2 Pictographs Worksheets: Free Math Practice with Answer Key (BC Curriculum)",
        "short_title": "Pictographs",
        "domain": "Data and probability",
        "standard_code": "Grade 2: Data and probability",
        "standard_url": "https://curriculum.gov.bc.ca/curriculum/mathematics/2/core",
        "standard_text": "Pictorial representation of concrete graphs, using one-to-one correspondence",
        "meta_desc": "Free Grade 2 math worksheets on pictographs where 1 picture = 1: read rows, make a pictograph from a tally, find the most, the fewest and how many more, add totals and draw conclusions. 100 questions with an answer key, matched to the BC curriculum.",
        "key_big": "One picture stands for one. Count the pictures in a row to read it.",
        "key_sub": "Touch each picture once and follow the right row. A tally group of 5 is 5, not 4. How many more means take away; how many in all means add every row.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }


def mark_large(u, pattern):
    """Tag pictures that must print larger (graphs, tables, A to D rows) so their labels stay readable."""
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
        mark_large(u, "(pictograph|tally table|tally and pictograph|rows that)")
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
