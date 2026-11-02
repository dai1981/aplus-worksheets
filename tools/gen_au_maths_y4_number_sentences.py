# -*- coding: utf-8 -*-
"""
Australia Year 4 Maths: Number Sentences with Addition and Subtraction
(Australian Curriculum v9.0, AC9M4A01)
  python3 tools/gen_au_maths_y4_number_sentences.py
Fact families and the inverse, unknowns in addition and subtraction (? + 245 = 600, 700 − ? = 325,
? − 148 = 375), properties (commutative and associative; subtraction is not commutative),
the equals sign as a balance (45 + 38 = 40 + ?) and word problems written as number sentences.
Wrong choices come from real mistakes: adding when the inverse is needed, subtracting the smaller
digit from the larger in each column (600 − 245 -> 445), forgetting to carry (45 + 38 -> 73),
regrouping slips, reading = as “the answer is” (45 + 38 = 40 + 83), adjusting the wrong way on
a balance (45 + 38 = 40 + 33) and treating subtraction as if order does not matter.
Every answer is checked in code. HTML attributes use single quotes. Australian English.
"""
import json, os, random, re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "au", "maths", "year-4")
UPDATED = "2026-11-02"
GREEN = "#006633"
FILL = "#cfe6d6"
GREY = "#e4e4e4"
INK = "#2b2b2b"
RED = "#c0392b"
FONT = "Arial, Helvetica, sans-serif"
GIRLS = ["Charlotte", "Isla", "Mia", "Amelia", "Ava", "Harper", "Chloe", "Ruby", "Mei", "Zara", "Matilda", "Sienna", "Grace"]
BOYS = ["Oliver", "Jack", "Noah", "William", "Leo", "Lachlan", "Liam", "Aarav", "Kai", "Cooper", "Ethan"]
Q = "<b>?</b>"
NB = " "


# ------------------------------------------------------------ numbers
def n(x):
    """Australian style: 4 digits no separator, 5 or more digits grouped with a no-break space."""
    s = str(x)
    if abs(x) < 10000:
        return s
    out = ""
    while len(s) > 3:
        out = NB + s[-3:] + out
        s = s[:-3]
    return s + out


def sent(*parts):
    """A number sentence: numbers are formatted, '?' becomes a bold question mark."""
    return " ".join(Q if p == "?" else (n(p) if isinstance(p, int) else p) for p in parts)


def plain(*parts):
    return " ".join(n(p) if isinstance(p, int) else p for p in parts)


def val(expr):
    return eval(expr.replace("−", "-").replace(NB, ""), {"__builtins__": {}})


def holds(eq, ans=None):
    """'? + 245 = 600' is true with ? = ans (real minus sign allowed)."""
    s = eq.replace(Q, "?")
    if ans is not None:
        s = s.replace("?", str(ans))
    vals = [val(p.strip()) for p in s.split("=")]
    return all(v == vals[0] for v in vals)


def sfl(a, b):
    """Smaller digit from larger digit in each column: 600 − 245 -> 445 (a typical mistake)."""
    da, db = str(a), str(b).rjust(len(str(a)), "0")
    return int("".join(str(abs(int(x) - int(y))) for x, y in zip(da, db)))


def nocarry(a, b):
    """Add column by column and drop every carried ten: 45 + 38 -> 73."""
    out, p = 0, 1
    while a or b:
        out += ((a % 10 + b % 10) % 10) * p
        a, b, p = a // 10, b // 10, p * 10
    return out


# ------------------------------------------------------------ helpers
def mcq(q, correct, cands, e):
    """4 choices: correct + the first 3 unique distractors. Positions are set later by balance()."""
    correct = n(correct) if isinstance(correct, int) else str(correct)
    seen = {correct}
    pick = []
    for c in cands:
        if isinstance(c, int):
            if c <= 0:
                continue
            c = n(c)
        c = str(c)
        if c in seen or not c or c.startswith("-") or c.startswith("−") or c.startswith("0"):
            continue
        seen.add(c)
        pick.append(c)
        if len(pick) == 3:
            break
    assert len(pick) == 3, (q, correct, cands)
    return {"q": q, "c": [correct] + pick, "a": 0, "e": e}


def balance(sets, rnd):
    """Spread the correct answers evenly over the 4 positions in every set."""
    for s in sets:
        targets = [0, 1, 2, 3] * 5
        rnd.shuffle(targets)
        for it, t in zip(s["items"], targets):
            c = it["c"]
            right = c[it["a"]]
            wrong = [x for i, x in enumerate(c) if i != it["a"]]
            rnd.shuffle(wrong)
            it["c"] = wrong[:t] + [right] + wrong[t:]
            it["a"] = t


class People:
    def __init__(self, rnd):
        self.pool = [(x, "she", "her") for x in GIRLS] + [(x, "he", "his") for x in BOYS]
        rnd.shuffle(self.pool)
        self.i = 0

    def next(self):
        p = self.pool[self.i % len(self.pool)]
        self.i += 1
        return p


def cap(s):
    return s[0].upper() + s[1:]


# ------------------------------------------------------------ pictures
def fig(svg):
    return "<div class='qfig'>" + svg + "</div>"


def svg_wrap(w, h, body, label):
    w, h = int(round(w)), int(round(h))
    return ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 %d %d' width='%d' height='%d' "
            "role='img' aria-label='%s'><g font-family='%s'>%s</g></svg>" % (w, h, w, h, label, FONT, body))


def tw(t, fs):
    return len(str(t)) * fs * 0.6


def text(x, y, t, fs=18, col=INK, anchor="middle"):
    return ("<text x='%.1f' y='%.1f' font-size='%d' font-weight='700' fill='%s' text-anchor='%s'>%s</text>"
            % (x, y, fs, col, anchor, t))


def bar_svg(whole, p1, p2):
    """Part-part-whole bar model: the whole bar on top, the two parts below, drawn to scale.
    Values are numbers or None for '?'."""
    vals = [whole, p1, p2]
    known = [v for v in vals if v is not None]
    if None in vals:
        miss = vals.index(None)
        full = [whole, p1, p2]
        full[miss] = (p1 + p2) if miss == 0 else (whole - (p2 if miss == 1 else p1))
    else:
        full = vals
    assert full[1] + full[2] == full[0] and len(known) >= 2
    W = 280
    x0, h = 8, 36
    w1 = round(W * full[1] / full[0])
    w1 = min(max(w1, 70), W - 70)
    s = []
    rows = [(8, [(x0, W, whole, FILL)]), (8 + h + 10, [(x0, w1, p1, "#fff"), (x0 + w1, W - w1, p2, "#fff")])]
    for y, cells in rows:
        for x, w, v, f in cells:
            s.append("<rect x='%d' y='%d' width='%d' height='%d' fill='%s' stroke='%s' stroke-width='2.5'/>"
                     % (x, y, w, h, f, GREEN))
            s.append(text(x + w / 2, y + 25, "?" if v is None else n(v), 18, RED if v is None else INK))
    lab = "bar model: whole %s, parts %s and %s" % tuple("?" if v is None else n(v) for v in vals)
    return svg_wrap(W + 16, 8 + 2 * h + 10 + 8, "".join(s), lab)


def pan_svg(left, right):
    """A level pan balance with a number sentence part on each pan (plain text, '?' allowed)."""
    def box_w(t):
        return max(90, int(tw(t, 18) + 24))
    wl, wr = box_w(left), box_w(right)
    cl = 8 + wl / 2
    cr = cl + wl / 2 + 40 + wr / 2
    mid = (cl + cr) / 2
    top, ih = 8, 36
    py = top + ih
    s = []
    for t, c, w in ((left, cl, wl), (right, cr, wr)):
        s.append("<rect x='%.1f' y='%d' width='%d' height='%d' rx='6' fill='%s' stroke='%s' stroke-width='2'/>"
                 % (c - w / 2, top, w, ih, GREY, INK))
        if "?" in t:
            a, b = t.split("?")
            full = tw(t, 18)
            x = c - full / 2
            s.append("<text x='%.1f' y='%d' font-size='18' font-weight='700' fill='%s'>%s<tspan fill='%s'>?</tspan>%s</text>"
                     % (x, top + 25, INK, a, RED, b))
        else:
            s.append(text(c, top + 25, t))
        s.append("<rect x='%.1f' y='%d' width='%d' height='6' fill='%s'/>" % (c - w / 2, py, w, INK))
        s.append("<rect x='%.1f' y='%d' width='4' height='18' fill='%s'/>" % (c - 2, py + 6, INK))
    by = py + 24
    s.append("<rect x='%.1f' y='%d' width='%.1f' height='6' fill='%s'/>" % (cl - 2, by, cr - cl + 4, INK))
    s.append("<path d='M%.1f %d L%.1f %d L%.1f %d Z' fill='%s'/>" % (mid, by + 6, mid - 22, by + 40, mid + 22, by + 40, GREEN))
    s.append("<rect x='%.1f' y='%d' width='80' height='5' fill='%s'/>" % (mid - 40, by + 40, INK))
    return svg_wrap(cr + wr / 2 + 8, by + 47, "".join(s), "pan balance: %s on the left and %s on the right" % (left, right))


def mark_large(u, pattern):
    rx = re.compile(r"<svg (?=[^>]*aria-label='(?:" + pattern + "))")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u


# ------------------------------------------------------------ distractor lists
def sub_cands(big, small, ans):
    """Answer is big − small. Mistakes: adding instead, smaller-from-larger, regrouping slips."""
    return [big + small, sfl(big, small), ans + 100, ans - 100, ans + 10, ans - 10]


def add_cands(a, b, ans):
    """Answer is a + b. Mistakes: subtracting instead, forgetting to carry, carry slips."""
    return [abs(a - b), nocarry(a, b), ans - 10, ans + 10, ans - 100, ans + 100]


WHAT = "<br>What is the missing number?"


# ============================================================ set 1: fact families and the inverse
def set_families():
    its = []
    # use a known addition fact to subtract
    for a, b in [(36, 47), (125, 75), (248, 352), (163, 237)]:
        s = a + b
        e = ("Subtraction undoes addition. %s, so %s. Not %s: that adds again instead of using the inverse."
             % (plain(a, "+", b, "=", s), plain(s, "−", a, "=", "<b>%s</b>" % n(b)), n(s + a)))
        its.append(mcq("You know %s. What is %s?" % (plain(a, "+", b, "=", s), plain(s, "−", a)),
                       b, [s + a, a, b + 10, b - 10], e))
    # which subtraction fact belongs
    for a, b in [(45, 38), (160, 240), (275, 325), (318, 482)]:
        s = a + b
        good = plain(s, "−", a, "=", b)
        e = ("A fact family uses the same three numbers. In a subtraction fact, the whole (%s) comes first: "
             "%s and %s." % (n(s), plain(s, "−", a, "=", b), plain(s, "−", b, "=", a)))
        its.append(mcq("%s. Which subtraction fact is in the same fact family?" % plain(a, "+", b, "=", s), good,
                       [plain(a, "−", s, "=", b), plain(b, "−", a, "=", s), plain(s, "+", a, "=", s + a)], e))
    # which addition fact belongs
    for s, a in [(500, 180), (83, 29), (720, 450), (1000, 365)]:
        b = s - a
        e = ("Addition is the inverse of subtraction. %s, so %s. %s is true, but it does not use %s, %s and %s."
             % (plain(s, "−", a, "=", b), plain(b, "+", a, "=", s), plain(s, "+", a, "=", s + a), n(s), n(a), n(b)))
        its.append(mcq("Which number sentence is in the same fact family as %s?" % plain(s, "−", a, "=", b),
                       plain(b, "+", a, "=", s),
                       [plain(s, "+", a, "=", s + a), plain(a, "+", s, "=", b), plain(s, "+", b, "=", s + b)], e))
    # bar models
    bars = [
        (None, 45, 38, 83, [73, 713, 7],
         "The whole is the two parts added: 45 + 38 = <b>83</b>. Not 73: that forgets to carry the ten from 5 + 8 = 13."),
        (600, 245, None, 355, [845, 445, 365],
         "245 + ? = 600. Use the inverse: 600 − 245 = <b>355</b>. Check: 245 + 355 = 600. "
         "Not 845: that adds instead of subtracting."),
        (420, None, 160, 260, [580, 340, 360],
         "? + 160 = 420. Use the inverse: 420 − 160 = <b>260</b>. Check: 260 + 160 = 420. "
         "Not 580: that adds instead of subtracting. Not 340: that takes the smaller digit from the larger in each column."),
        (None, 256, 168, 424, [88, 314, 324],
         "The whole is the two parts added: 256 + 168 = <b>424</b>. Not 88: that subtracts. "
         "Not 314: that forgets to carry both tens."),
    ]
    for wh, p1, p2, ans, wr, e in bars:
        vals = [wh or ans, p1 or ans, p2 or ans]
        assert vals[1] + vals[2] == vals[0]
        assert nocarry(45, 38) == 73 and sfl(600, 245) == 445 and sfl(420, 160) == 340 and nocarry(256, 168) == 314
        its.append(mcq("What is the missing number in the bar model?" + fig(bar_svg(wh, p1, p2)), ans, wr, e))
    # which is NOT in the family
    notin = [
        (54, 29, plain(29, "−", 83, "=", 54), "the whole must come first: 83 − 29 = 54"),
        (150, 270, plain(270, "−", 150, "=", 420), "270 − 150 is 120, not 420. The fact is 420 − 150 = 270"),
        (308, 192, plain(500, "+", 192, "=", 308), "500 + 192 is 692, not 308. The fact is 500 − 192 = 308"),
        (65, 135, plain(65, "−", 135, "=", 200), "65 − 135 is not 200. The fact is 200 − 135 = 65"),
    ]
    for i, (a, b, bad, why) in enumerate(notin):
        s = a + b
        fam = [plain(a, "+", b, "=", s), plain(b, "+", a, "=", s), plain(s, "−", a, "=", b), plain(s, "−", b, "=", a)]
        assert not holds(bad)
        good = [fam[j] for j in range(4) if j != i]
        assert all(holds(g) for g in good)
        e = "The fact family of %s, %s and %s is %s. <b>%s</b> is not in it: %s." % (n(a), n(b), n(s), ", ".join(fam), bad, why)
        its.append(mcq("Which number sentence is <b>not</b> in the fact family of %s, %s and %s?" % (n(a), n(b), n(s)), bad, good, e))
    assert len(its) == 20
    return {"title": "Fact families and the inverse", "items": its}


# ============================================================ set 2: unknowns
def set_unknowns():
    its = []

    def add(eq, ans, cands, e):
        assert holds(eq, ans), eq
        its.append(mcq(eq + WHAT, ans, cands, e))

    # ? + a = s and a + ? = s
    for a, s, left in [(245, 600, True), (178, 500, True), (367, 800, True), (456, 1000, True), (1250, 3000, True),
                       (380, 920, False), (256, 700, False), (195, 610, False), (2400, 5000, False)]:
        ans = s - a
        eq = sent("?", "+", a, "=", s) if left else sent(a, "+", "?", "=", s)
        e = ("%s. Use the inverse: ? = %s = <b>%s</b>. Check: %s. Not %s: that adds instead of subtracting."
             % (eq, plain(s, "−", a), n(ans), plain(*(([ans, "+", a] if left else [a, "+", ans]) + ["=", s])), n(s + a)))
        add(eq, ans, sub_cands(s, a, ans), e)
    # a − ? = r
    for a, r in [(700, 325), (543, 218), (900, 456), (812, 375), (4000, 1650)]:
        ans = a - r
        eq = sent(a, "−", "?", "=", r)
        e = ("%s. Ask: %s take away what leaves %s? ? = %s = <b>%s</b>. Check: %s. Not %s: that adds the two numbers."
             % (eq, n(a), n(r), plain(a, "−", r), n(ans), plain(a, "−", ans, "=", r), n(a + r)))
        add(eq, ans, sub_cands(a, r, ans), e)
    # ? − a = r
    for a, r in [(148, 375), (265, 438), (390, 245), (1200, 2600)]:
        ans = r + a
        eq = sent("?", "−", a, "=", r)
        e = ("%s. The unknown is the number you start with. Undo − %s by adding: ? = %s = <b>%s</b>. Check: %s. "
             "Not %s: that subtracts again instead of using the inverse."
             % (eq, n(a), plain(r, "+", a), n(ans), plain(ans, "−", a, "=", r), n(abs(r - a))))
        add(eq, ans, add_cands(r, a, ans), e)
    # = sign first
    eq = sent(850, "=", "?", "+", 375)
    add(eq, 475, sub_cands(850, 375, 475),
        "The = sign can come first. It means both sides are the same. ? + 375 = 850, so ? = 850 − 375 = <b>475</b>. "
        "Check: 475 + 375 = 850. Not 1225: that adds instead of subtracting.")
    eq = sent(460, "=", 900, "−", "?")
    add(eq, 440, sub_cands(900, 460, 440),
        "The = sign can come first. 900 − ? = 460, so ? = 900 − 460 = <b>440</b>. Check: 900 − 440 = 460. "
        "Not 1360: that adds the two numbers.")
    assert len(its) == 20
    return {"title": "Unknowns in addition and subtraction", "items": its}


# ============================================================ set 3: properties
def set_props(P):
    its = []

    def add(q, ans, cands, e, eq=None):
        if eq is not None:
            assert holds(eq, ans), eq
        its.append(mcq(q, ans, cands, e))

    # commutative
    eq = sent(245, "+", 38, "=", 38, "+", "?")
    add(eq + WHAT, 245, [283, 38, 207],
        "You can add in any order: 245 + 38 = 38 + 245. So ? = <b>245</b>. Not 283: = means “the same as”, "
        "so ? is not the answer to 245 + 38.", eq)
    eq = sent(167, "+", 59, "=", "?", "+", 167)
    add(eq + WHAT, 59, [226, 167, 108],
        "Turn-around facts: 167 + 59 = 59 + 167. So ? = <b>59</b>. Not 226: that is the total of the left side.", eq)
    add("Which number sentence is true?", "64 + 29 = 29 + 64",
        ["64 − 29 = 29 − 64", "64 + 29 = 64 − 29", "64 − 29 = 29 + 64"],
        "You can add in any order, so <b>64 + 29 = 29 + 64</b> is true. You cannot subtract in any order: "
        "64 − 29 = 35, but 29 − 64 does not give 35.")
    add("Which number sentence is <b>not</b> true?", "50 − 20 = 20 − 50",
        ["50 + 20 = 20 + 50", "50 − 20 = 30", "30 + 20 = 50"],
        "Subtraction does not work in any order. 50 − 20 = 30, but 20 − 50 is not 30. "
        "So <b>50 − 20 = 20 − 50</b> is not true.")
    add("Which number sentence has the same total as 36 + 47?", "47 + 36",
        ["47 − 36", "36 − 47", "36 + 74"],
        "Changing the order of two numbers you add does not change the total: 36 + 47 = <b>47 + 36</b> = 83. "
        "36 + 74 uses a different number (74, not 47).")
    nm, he, his = P.next()
    add("%s says 85 − 40 = 40 − 85, because you can add in any order. What is wrong?" % nm,
        "Subtraction cannot be done in any order",
        ["Addition cannot be done in any order", "85 − 40 is not 45", "Nothing is wrong"],
        "The turn-around rule works for addition only. 85 − 40 = 45, but 40 − 85 is not 45. "
        "<b>Subtraction cannot be done in any order.</b>")
    # associative: friendly pairs
    for a, b, c, pair, wr, e in [
        (46, 27, 54, "46 and 54", [100, 117, 73],
         "46 + 54 = 100. Then 100 + 27 = <b>127</b>. Not 100: that forgets the 27. Not 73: that forgets the 54."),
        (38, 75, 25, "75 and 25", [100, 128, 113],
         "75 + 25 = 100. Then 100 + 38 = <b>138</b>. Not 100: that forgets the 38. Not 113: that forgets the 25."),
        (125, 68, 75, "125 and 75", [200, 258, 193],
         "125 + 75 = 200. Then 200 + 68 = <b>268</b>. Not 200: that forgets the 68. Not 193: that forgets the 75."),
        (19, 36, 81, "19 and 81", [100, 126, 55],
         "19 + 81 = 100. Then 100 + 36 = <b>136</b>. Not 100: that forgets the 36. Not 55: that forgets the 81."),
    ]:
        ans = a + b + c
        add("Work out %s. Hint: add %s first." % (sent(a, "+", b, "+", c), pair), ans, wr, e)
    eq = sent(24, "+", 58, "+", 6, "=", 30, "+", "?")
    add(eq + WHAT, 58, [88, 64, 52],
        "You can add three numbers in any order. 24 + 6 = 30, so 24 + 58 + 6 = 30 + 58. ? = <b>58</b>. "
        "Not 88: that is the total, not the missing number.", eq)
    eq = sent(37, "+", 45, "+", 13, "=", 50, "+", "?")
    add(eq + WHAT, 45, [95, 32, 58],
        "37 + 13 = 50, so 37 + 45 + 13 = 50 + 45. ? = <b>45</b>. Not 95: that is the total. "
        "Not 32: the 13 is already in the 50.", eq)
    add("Subtract from left to right. Which number sentence is true?", "100 − 30 − 20 = 50",
        ["100 − 30 − 20 = 90", "100 − 30 − 20 = 70", "100 − 30 = 30 − 100"],
        "Subtract from left to right: 100 − 30 = 70, then 70 − 20 = 50. So <b>100 − 30 − 20 = 50</b>. "
        "Not 90: that works out 30 − 20 first. Subtraction cannot be grouped in any order. Not 70: that forgets the − 20.")
    # partitioning and compensation
    eq = sent(245, "+", 38, "=", 245, "+", 30, "+", "?")
    add(eq + WHAT, 8, [38, 275, 30],
        "Split 38 into 30 + 8. So 245 + 38 = 245 + 30 + 8 and ? = <b>8</b>. Not 38: the 30 has already been added.", eq)
    eq = sent(198, "+", 245, "=", 200, "+", "?")
    add(eq + WHAT, 243, [247, 443, 45],
        "198 is 2 less than 200. Move 2 from 245 to 198: 198 + 245 = 200 + 243. ? = <b>243</b>. "
        "Not 247: if one number goes up by 2, the other must go down by 2. Not 443: that is the total.", eq)
    eq = sent(399, "+", 126, "=", 400, "+", "?")
    add(eq + WHAT, 125, [127, 525, 26],
        "399 + 1 = 400, so take 1 from 126: 399 + 126 = 400 + 125. ? = <b>125</b>. "
        "Not 127: the other number must go down, not up. Not 525: that is the total.", eq)
    add("Work out " + sent(523, "−", 198) + ". Hint: take away 200, then add 2 back.", 325, [321, 323, 721],
        "523 − 200 = 323. You took away 2 too many, so add 2 back: 323 + 2 = <b>325</b>. "
        "Not 321: that takes away the extra 2 instead of adding it back.")
    add("Work out " + sent(640, "−", 299) + ". Hint: take away 300, then add 1 back.", 341, [339, 340, 939],
        "640 − 300 = 340. You took away 1 too many, so add 1 back: 340 + 1 = <b>341</b>. "
        "Not 339: that takes away the extra 1 instead of adding it back.")
    add("Work out " + sent(250, "+", 175, "+", 50) + ". Hint: add 250 and 50 first.", 475, [300, 425, 465],
        "250 + 50 = 300. Then 300 + 175 = <b>475</b>. Not 300: that forgets the 175. Not 425: that forgets the 50.")
    add("Work out " + sent(1350, "+", 480, "+", 650) + ". Hint: add 1350 and 650 first.", 2480, [2000, 1830, 2130],
        "1350 + 650 = 2000. Then 2000 + 480 = <b>2480</b>. Not 2000: that forgets the 480. Not 1830: that forgets the 650.")
    assert 250 + 175 + 50 == 475 and 1350 + 480 + 650 == 2480 and 2480 - 350 == 2130
    assert len(its) == 20
    return {"title": "Properties of addition and subtraction", "items": its}


# ============================================================ set 4: the equals sign as a balance
def set_equals(P):
    its = []

    def add(q, ans, cands, e, eq=None):
        if eq is not None:
            assert holds(eq, ans), eq
        its.append(mcq(q, ans, cands, e))

    # a + b = c + ?
    for a, b, c, pic in [(45, 38, 40, True), (27, 56, 30, True), (68, 25, 70, False), (134, 58, 130, False), (246, 97, 250, False)]:
        S = a + b
        ans = S - c
        d = a - c
        wrong_way = b - d
        eq = sent(a, "+", b, "=", c, "+", "?")
        how = ("%s is %d %s than %s, so ? must be %d %s than %s" %
               (n(c), abs(d), "less" if d > 0 else "more", n(a), abs(d), "more" if d > 0 else "less", n(b)))
        e = ("= means both sides have the same value. The left side is %s. So %s and ? = <b>%s</b>. "
             "Or: %s. Not %s: that is the value of the left side, not the missing number. Not %s: that changes %s the wrong way."
             % (plain(a, "+", b, "=", S), plain(c, "+", "?", "=", S), n(ans), how, n(S), n(wrong_way), n(b)))
        q = ("The pans balance, so " + eq + ". What is the missing number?" + fig(pan_svg(plain(a, "+", b), plain(c, "+", "?")))) \
            if pic else eq + WHAT
        add(q, ans, [S, wrong_way, S + c], e, eq)
    # a − b = c − ?
    for a, b, c, pic in [(72, 28, 74, True), (85, 39, 86, True), (63, 27, 60, False), (500, 198, 502, False), (91, 46, 95, False)]:
        D = a - b
        ans = c - D
        wrong_way = b - (c - a)
        eq = sent(a, "−", b, "=", c, "−", "?")
        e = ("Work out the side you know: %s. So %s, and ? = %s = <b>%s</b>. "
             "Both numbers move the same way to keep the same difference. Not %s: that is the value of the left side. "
             "Not %s: that moves %s the wrong way."
             % (plain(a, "−", b, "=", D), plain(c, "−", "?", "=", D), plain(c, "−", D), n(ans), n(D), n(wrong_way), n(b)))
        q = ("The pans balance, so " + eq + ". What is the missing number?" + fig(pan_svg(plain(a, "−", b), plain(c, "−", "?")))) \
            if pic else eq + WHAT
        add(q, ans, [D, wrong_way, c + D], e, eq)
    # mixed
    eq = sent(300, "+", 250, "=", 600, "−", "?")
    add(eq + WHAT, 50, [550, 1150, 350],
        "300 + 250 = 550. So 600 − ? = 550, and ? = 600 − 550 = <b>50</b>. Not 550: that is the value of the left side.", eq)
    eq = sent(64, "+", 36, "=", 150, "−", "?")
    add(eq + WHAT, 50, [100, 250, 114],
        "64 + 36 = 100. So 150 − ? = 100, and ? = 150 − 100 = <b>50</b>. Not 100: that is the value of the left side.", eq)
    eq = sent(90, "−", 25, "=", 40, "+", "?")
    add(eq + WHAT, 25, [65, 105, 15],
        "90 − 25 = 65. So 40 + ? = 65, and ? = 65 − 40 = <b>25</b>. Not 65: that is the value of the left side.", eq)
    eq = sent(58, "+", "?", "=", 60, "+", 37)
    add(eq + WHAT, 39, [97, 155, 35],
        "60 + 37 = 97. So 58 + ? = 97, and ? = 97 − 58 = <b>39</b>. Or: 58 is 2 less than 60, so ? is 2 more than 37. "
        "Not 35: that changes 37 the wrong way.", eq)
    eq = sent(1250, "+", 380, "=", 1300, "+", "?")
    add(eq + WHAT, 330, [1630, 430, 2930],
        "1300 is 50 more than 1250, so ? is 50 less than 380: ? = <b>330</b>. Check: 1250 + 380 = 1630 and 1300 + 330 = 1630. "
        "Not 1630: that is the value of the left side.", eq)
    # true sentences
    for right, wrongs, e in [
        ("45 + 38 = 40 + 43", ["45 + 38 = 40 + 83", "45 + 38 = 40 + 33", "45 + 38 = 50 + 43"],
         "Work out both sides. 45 + 38 = 83 and 40 + 43 = 83, so <b>45 + 38 = 40 + 43</b> is true. "
         "40 + 83 = 123, 40 + 33 = 73 and 50 + 43 = 93."),
        ("70 − 26 = 74 − 30", ["70 − 26 = 66 − 30", "70 − 26 = 44 − 30", "70 − 26 = 74 − 22"],
         "Work out both sides. 70 − 26 = 44 and 74 − 30 = 44, so <b>70 − 26 = 74 − 30</b> is true. "
         "66 − 30 = 36, 44 − 30 = 14 and 74 − 22 = 52."),
        ("150 + 80 = 300 − 70", ["150 + 80 = 300 + 70", "150 + 80 = 230 + 70", "150 + 80 = 200 − 70"],
         "Work out both sides. 150 + 80 = 230 and 300 − 70 = 230, so <b>150 + 80 = 300 − 70</b> is true. "
         "300 + 70 = 370, 230 + 70 = 300 and 200 − 70 = 130."),
    ]:
        assert holds(right) and not any(holds(w) for w in wrongs)
        add("Work out both sides. Which number sentence starting with %s is true?" % right.split(" = ")[0], right, wrongs, e)
    nm, he, his = P.next()
    add("%s adds 45 and 38, then adds 9. %s writes: 45 + 38 = 83 + 9 = 92. What is wrong?" % (nm, cap(he)),
        "45 + 38 is not equal to 83 + 9",
        ["45 + 38 is not 83", "Nothing is wrong", "83 + 9 is not 92"],
        "= means both sides are the same. 45 + 38 is 83, but 83 + 9 is 92, so “45 + 38 = 83 + 9” is <b>not true</b>. "
        "%s should write two number sentences: 45 + 38 = 83 and 83 + 9 = 92." % nm)
    add("What does the = sign mean in 50 + 30 = 60 + 20?", "Both sides have the same value",
        ["The answer comes next", "Add all the numbers together", "The left side is bigger"],
        "= means “is the same as”. 50 + 30 = 80 and 60 + 20 = 80, so <b>both sides have the same value</b>. "
        "It does not just mean “the answer comes next”.")
    assert len(its) == 20
    return {"title": "The equals sign as a balance", "items": its}


# ============================================================ set 5: word problems
def set_words(P):
    its = []

    def match(q, right, wrongs, e, ans):
        if ans is not None or re.fullmatch(r"[0-9 +−=]+", right):
            assert holds(right, ans), right
        its.append(mcq(q, right, wrongs, e))

    def solve(q, sentence, ans, cands, e, money=False):
        assert holds(sentence, ans), sentence
        f = (lambda v: "$" + n(v)) if money else (lambda v: n(v))
        cs = [f(c) for c in cands if c > 0]
        its.append(mcq(q, f(ans), cs, "Number sentence: %s. %s" % (sentence, e)))

    # 1
    nm, he, his = P.next()
    match("%s has 245 footy cards. %s gets some more and now has 600. Which number sentence shows how many more "
          "cards %s got?" % (nm, cap(he), he),
          sent(245, "+", "?", "=", 600), [sent(245, "+", 600, "=", "?"), sent(600, "+", "?", "=", 245), sent("?", "−", 245, "=", 600)],
          "%s starts with 245, adds an unknown number and ends with 600: <b>245 + ? = 600</b>. Then ? = 600 − 245 = 355." % nm, 355)
    # 2
    nm, he, his = P.next()
    solve("%s’s book has 450 pages. %s has read 178 pages. How many pages are left to read?" % (nm, cap(he)),
          sent(178, "+", "?", "=", 450), 272, sub_cands(450, 178, 272),
          "Use the inverse: ? = 450 − 178 = <b>272</b> pages. Check: 178 + 272 = 450. Not 628: that adds instead of subtracting.")
    # 3
    solve("The school canteen had 700 icy poles. After a hot week, 325 are left. How many icy poles were sold?",
          sent(700, "−", "?", "=", 325), 375, sub_cands(700, 325, 375),
          "? = 700 − 325 = <b>375</b> icy poles. Check: 700 − 375 = 325. Not 1025: that adds the two numbers.")
    # 4
    nm, he, his = P.next()
    match("%s spends $148 at the shops and has $375 left. Which number sentence shows how much money %s had at the start?" % (nm, he),
          sent("?", "−", 148, "=", 375), [sent(375, "−", 148, "=", "?"), sent(148, "−", "?", "=", 375), sent("?", "+", 375, "=", 148)],
          "You do not know the starting amount, so it is ?. Take away $148 and $375 is left: <b>? − 148 = 375</b>. "
          "Then ? = 375 + 148 = $523.", 523)
    # 5
    nm, he, his = P.next()
    solve("%s buys a scooter for $148 and has $375 left. How much money did %s have at the start?" % (nm, he),
          sent("?", "−", 148, "=", 375), 523, add_cands(375, 148, 523),
          "Undo − 148 by adding: ? = 375 + 148 = <b>$523</b>. Check: $523 − $148 = $375. "
          "Not $227: that subtracts instead of adding.", money=True)
    # 6
    nm, he, his = P.next()
    match("Two classes collect cans for recycling. Class 4A collects 45 cans on Monday and 38 on Tuesday. "
          "Class 4B collects 40 cans on Monday and the same total as 4A. Which number sentence shows 4B’s Tuesday cans?",
          sent(45, "+", 38, "=", 40, "+", "?"), [sent(45, "+", 38, "=", "?"), sent(45, "+", 40, "=", 38, "+", "?"),
                                              sent(40, "+", 38, "=", 45, "+", "?")],
          "The two totals are the same, so the two sides are equal: <b>45 + 38 = 40 + ?</b>. 45 + 38 = 83, so ? = 43 cans.", 43)
    # 7
    nm, he, his = P.next()
    match("%s works out 523 − 168 = 355. Which number sentence can %s use to check %s answer?" % (nm, he, his),
          "355 + 168 = 523", ["523 + 168 = 691", "355 − 168 = 187", "523 + 355 = 878"],
          "Check a subtraction with the inverse, addition: 355 + 168 = 523, so <b>355 + 168 = 523</b> shows the answer is right. "
          "523 + 168 = 691 is true, but it does not check the subtraction.", None)
    # 8
    nm, he, his = P.next()
    solve("%s’s family drives 640 km over two days of the holidays. They drive 285 km on the first day. "
          "How far do they drive on the second day?" % nm,
          sent(285, "+", "?", "=", 640), 355, sub_cands(640, 285, 355),
          "? = 640 − 285 = <b>355</b> km. Check: 285 + 355 = 640. Not 445: that takes the smaller digit from the larger "
          "in each column instead of regrouping.")
    # 9
    match("A rainwater tank holds 900 L. After watering the garden, 456 L is left. "
          "Which number sentence shows how much water was used?",
          sent(900, "−", "?", "=", 456), [sent(900, "+", 456, "=", "?"), sent("?", "−", 900, "=", 456), sent(456, "−", 900, "=", "?")],
          "Start with 900 L, take away an unknown amount, and 456 L is left: <b>900 − ? = 456</b>. Then ? = 900 − 456 = 444 L.", 444)
    # 10
    solve("A rainwater tank holds 900 L. After watering the garden, 456 L is left. How much water was used?",
          sent(900, "−", "?", "=", 456), 444, sub_cands(900, 456, 444),
          "? = 900 − 456 = <b>444</b> L. Check: 900 − 444 = 456. Not 1356: that adds the two numbers.")
    # 11
    solve("At the athletics carnival, Red House has 1250 points and Blue House has 1750 points. "
          "How many more points does Red House need to equal Blue House?",
          sent(1250, "+", "?", "=", 1750), 500, sub_cands(1750, 1250, 500),
          "? = 1750 − 1250 = <b>500</b> points. Check: 1250 + 500 = 1750. Not 3000: that adds the two scores.")
    # 12
    nm, he, his = P.next()
    match("%s has to work out 38 + 245. %s starts with 245 and adds 38. Which number sentence shows why that works?" % (nm, cap(he)),
          "38 + 245 = 245 + 38", ["38 − 245 = 245 − 38", "38 + 245 = 245 − 38", "38 + 245 = 283 + 38"],
          "You can add two numbers in any order and get the same total: <b>38 + 245 = 245 + 38</b>.", None)
    # 13
    solve("At the sausage sizzle, the Year 4 stall sells 46 sausages before school, 27 at recess and 54 at lunch. "
          "How many sausages do they sell altogether?",
          sent(46, "+", 27, "+", 54, "=", "?"), 127, [100, 117, 73],
          "Add 46 + 54 first to make 100. Then 100 + 27 = <b>127</b> sausages. Not 100: that forgets the 27.")
    # 14
    nm, he, his = P.next()
    match("%s has 45 shells and finds 38 more at the beach. Then %s gives away 20. %s writes: 45 + 38 = 83 − 20 = 63. "
          "What is wrong?" % (nm, he, cap(he)),
          "45 + 38 is not equal to 83 − 20", ["45 + 38 is not 83", "83 − 20 is not 63", "Nothing is wrong"],
          "= means both sides are the same. 45 + 38 = 83, but 83 − 20 = 63, so “45 + 38 = 83 − 20” is <b>not true</b>. "
          "Write two number sentences: 45 + 38 = 83, then 83 − 20 = 63.", None)
    # 15
    nm, he, his = P.next()
    solve("%s is 10 and %s mum is 38. In 5 years, %s mum will be 43. The difference in their ages stays "
          "the same. How old will %s be then?" % (nm, his, his, nm),
          sent(38, "−", 10, "=", 43, "−", "?"), 15, [28, 33, 5],
          "38 − 10 = 28, so 43 − ? = 28 and ? = <b>15</b>. Both ages go up by 5, so the difference stays 28. "
          "Not 28: that is the difference, not %s’s age. Not 33: that takes 10 from 43." % nm)
    # 16
    nm, he, his = P.next()
    solve("%s has saved $265. The bike %s wants costs $430. How much more money does %s need?" % (nm, he, he),
          sent(265, "+", "?", "=", 430), 165, sub_cands(430, 265, 165),
          "? = 430 − 265 = <b>$165</b>. Check: $265 + $165 = $430. Not $695: that adds instead of subtracting.", money=True)
    # 17
    match("There are some people at the beach. Then 128 more arrive, and now there are 365 people. "
          "Which number sentence matches the story?",
          sent("?", "+", 128, "=", 365), [sent(365, "+", 128, "=", "?"), sent(128, "−", "?", "=", 365), sent("?", "−", 128, "=", 365)],
          "You do not know how many were there first, so that is ?. Add 128 to get 365: <b>? + 128 = 365</b>. "
          "Then ? = 365 − 128 = 237.", 237)
    # 18
    solve("There are some people at the beach. Then 128 more arrive, and now there are 365 people. "
          "How many people were at the beach at first?",
          sent("?", "+", 128, "=", 365), 237, sub_cands(365, 128, 237),
          "Use the inverse: ? = 365 − 128 = <b>237</b> people. Check: 237 + 128 = 365. Not 493: that adds instead of subtracting.")
    # 19
    nm, he, his = P.next()
    solve("%s knows that 356 + 244 = 600. A school has 600 students, and 356 of them are at the swimming carnival. "
          "How many students are not at the carnival?" % nm,
          sent(600, "−", 356, "=", "?"), 244, [956, 356, 354],
          "356 + 244 = 600 is in the same fact family as 600 − 356 = 244, so <b>244</b> students. "
          "Not 956: that adds instead of subtracting.")
    # 20
    solve("A cricket club sells 2600 tickets in December. By the end of January it has sold 4350 tickets in total. "
          "How many tickets did it sell in January?",
          sent(2600, "+", "?", "=", 4350), 1750, sub_cands(4350, 2600, 1750),
          "? = 4350 − 2600 = <b>1750</b> tickets. Check: 2600 + 1750 = 4350. Not 6950: that adds the two numbers.")
    assert len(its) == 20
    return {"title": "Word problems", "items": its}


# ============================================================ lesson
def ex(title, q, s, a):
    return ("<div class='sn-ex'><span class='sn-ex-t'>%s</span><p class='sn-ex-q'>%s</p>"
            "<p class='sn-ex-s'>%s</p><p class='sn-ex-a'>Answer: %s</p></div>" % (title, q, s, a))


def table(head, rows):
    h = "".join("<th>%s</th>" % x for x in head)
    b = "".join("<tr>" + "".join("<td>%s</td>" % c for c in r) + "</tr>" for r in rows)
    return "<div class='sn-tw'><table class='sn-table'><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>" % (h, b)


def body_html():
    return (
        "<h2>Addition and subtraction are inverses</h2>"
        "<p>Subtraction undoes addition, and addition undoes subtraction. "
        "So three numbers like 245, 355 and 600 make a <b>fact family</b> of four facts.</p>"
        "<figure class='sn-fig'>" + bar_svg(600, 245, 355) +
        "<figcaption>The two parts, 245 and 355, make the whole, 600.</figcaption></figure>" +
        table(["Addition", "Subtraction"], [["245 + 355 = 600", "600 − 245 = 355"], ["355 + 245 = 600", "600 − 355 = 245"]]) +
        "<p>In a subtraction fact the whole, the biggest number, always comes first.</p>"
        "<h2>Find the unknown: use the inverse</h2>"
        "<p>A number sentence can have a missing number, shown as ? or a box. Use the inverse operation to find it, "
        "then put it back in to check.</p>" +
        table(["Number sentence", "Do this", "Answer"], [
            [sent("?", "+", 245, "=", 600), "600 − 245", "355"],
            [sent(700, "−", "?", "=", 325), "700 − 325", "375"],
            [sent("?", "−", 148, "=", 375), "375 + 148", "523"],
        ]) +
        ex("Example", sent("?", "−", 148, "=", 375),
           "The unknown is the number you start with. Undo − 148 by adding: 375 + 148 = 523. Check: 523 − 148 = 375.", "523") +
        "<h2>Use the properties</h2>" +
        table(["Property", "What it says", "Example"], [
            ["Commutative (turn-around)", "You can add two numbers in any order", "38 + 245 = 245 + 38"],
            ["Associative", "With three numbers, you can add any pair first", "46 + 27 + 54 = 100 + 27 = 127"],
        ]) +
        "<p>Subtraction is <b>not</b> commutative: 50 − 20 = 30, but 20 − 50 is not 30. "
        "With more than one subtraction, work from left to right.</p>" +
        ex("Example", sent(198, "+", 245, "=", 200, "+", "?"),
           "198 + 2 = 200, so take 2 from 245. 198 + 245 = 200 + 243.", "243") +
        "<h2>The equals sign means “the same as”</h2>"
        "<p>= does not mean “the answer is”. It means both sides have the same value, like a balance.</p>"
        "<figure class='sn-fig'>" + pan_svg("45 + 38", "40 + ?") +
        "<figcaption>The pans balance: 45 + 38 = 40 + ?. The left side is 83, so 40 + ? = 83 and ? = 43.</figcaption></figure>" +
        ex("Example", sent(45, "+", 38, "=", 40, "+", "?"),
           "40 is 5 less than 45, so ? must be 5 more than 38: ? = 43. Check: 40 + 43 = 83 = 45 + 38.", "43") +
        ex("Example", sent(72, "−", 28, "=", 74, "−", "?"),
           "72 − 28 = 44. So 74 − ? = 44, and ? = 30. Both numbers went up by 2, so the difference stays the same.", "30") +
        "<h2>Common mistakes</h2>" +
        table(["Mistake", "What to do instead"], [
            ["? + 245 = 600, so ? = 845 (600 + 245)", "Use the inverse: 600 − 245 = 355"],
            ["? − 148 = 375, so ? = 227 (375 − 148)", "Undo − 148 by adding: 375 + 148 = 523"],
            ["600 − 245 = 445 (smaller digit from larger)", "Regroup: 600 − 245 = 355"],
            ["45 + 38 = 40 + ?, so ? = 83", "83 is the left side. 40 + ? = 83, so ? = 43"],
            ["45 + 38 = 40 + ?, so ? = 33", "40 is less than 45, so ? is more than 38: ? = 43"],
            ["45 + 38 = 83 + 9 = 92", "Write two number sentences: 45 + 38 = 83, then 83 + 9 = 92"],
            ["50 − 20 = 20 − 50", "Only addition can be done in any order"],
        ])
    )


FAQ = [
    {"q": "What is a number sentence in Year 4 maths?",
     "a": "A number sentence uses numbers, operation signs and an equals sign, like 245 + 355 = 600. In Year 4 (AC9M4A01), students find unknown values in number sentences such as ? + 245 = 600 or 700 − ? = 325."},
    {"q": "How do you find the missing number in a subtraction number sentence?",
     "a": "Use the inverse. For ? − 148 = 375, add: 375 + 148 = 523. For 700 − ? = 325, subtract: 700 − 325 = 375. Then put the answer back in to check."},
    {"q": "What does the equals sign mean in Year 4?",
     "a": "The equals sign means “is the same as”, not “the answer is”. In 45 + 38 = 40 + ?, both sides must have the same value, so ? = 43, not 83."},
    {"q": "What are the commutative and associative properties of addition?",
     "a": "Commutative means you can add two numbers in any order (38 + 245 = 245 + 38). Associative means you can add three numbers in any pairs (46 + 27 + 54 = 100 + 27). Subtraction does not have these properties."},
]


def gen_unit():
    rnd = random.Random(4811)
    P = People(rnd)
    sets = [set_families(), set_unknowns(), set_props(P), set_equals(P), set_words(P)]
    balance(sets, rnd)
    seen = set()
    for s in sets:
        assert len(s["items"]) == 20, (s["title"], len(s["items"]))
        assert sorted(it["a"] for it in s["items"]) == sorted([0, 1, 2, 3] * 5), s["title"]
        for it in s["items"]:
            assert len(set(it["c"])) == 4, it
            assert it["q"].count("<svg") <= 1
            assert it["q"] not in seen, it["q"]
            seen.add(it["q"])
    return {
        "country": "au", "subject": "maths", "grade": "year-4", "slug": "number-sentences-addition-and-subtraction", "sort": 11,
        "updated": UPDATED, "pdf_url": "",
        "title": "Year 4 Number Sentences: Addition and Subtraction",
        "seo_title": "Year 4 Addition and Subtraction Number Sentences Worksheets: Free Maths with Answer Key (Australian Curriculum)",
        "short_title": "Number Sentences: + and −",
        "domain": "Algebra",
        "standard_code": "AC9M4A01",
        "standard_url": "https://v9.australiancurriculum.edu.au/f-10-curriculum/learning-areas/mathematics",
        "standard_text": "Find unknown values in numerical equations involving addition and subtraction, using the properties of numbers and operations",
        "meta_desc": "Free Year 4 maths worksheets on addition and subtraction number sentences, aligned to the Australian Curriculum (AC9M4A01): fact families, missing numbers like ? + 245 = 600 and 700 − ? = 325, properties, the equals sign as a balance and word problems. 100 questions with an answer key.",
        "key_big": "To find a missing number, use the inverse: subtraction undoes addition, and addition undoes subtraction.",
        "key_sub": "? + 245 = 600, so ? = 600 − 245 = 355. ? − 148 = 375, so ? = 375 + 148 = 523. The = sign means “the same as”: 45 + 38 = 40 + 43.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }


if __name__ == "__main__":
    u = gen_unit()
    mark_large(u, "bar model|pan balance")
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(u, f, ensure_ascii=False, indent=1)
    print("wrote", path)
