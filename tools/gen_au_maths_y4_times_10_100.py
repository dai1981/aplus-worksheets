# -*- coding: utf-8 -*-
"""
Australia Year 4 Maths: Multiplying and dividing by 10 and 100 (Australian Curriculum v9.0, AC9M4N05)
  python3 tools/gen_au_maths_y4_times_10_100.py
× 10 and × 100 on a place value chart (digits move left), ÷ 10 and ÷ 100 of whole numbers ending in zeros
(digits move right), multiples of 10 and 100 (30 × 4 = 120, 600 ÷ 3 = 200), missing numbers, then word
problems in Australian contexts (boxes of 100, $10 notes, 1000 m in a km, 100c in $1).
Every answer and every wrong answer is computed here (wrong answers = real student mistakes:
the zero in the wrong place, moving the wrong way, dropping or adding a zero).
HTML attributes use single quotes (no backslashes in the JSON). Australian English.
Numbers of 5 or more digits use a no-break space between groups of three (12 340); 4-digit numbers
have no separator (4536).
"""
import json, os, random, re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "au", "maths", "year-4")
UPDATED = "2026-11-02"
GREEN = "#006633"
FILL = "#cfe6d6"
RED = "#c0392b"
BLUE = "#2f6fb0"
INK = "#2b2b2b"
FONT = "Arial, Helvetica, sans-serif"
NB = " "
GIRLS = ["Charlotte", "Isla", "Mia", "Amelia", "Ava", "Harper", "Chloe", "Ruby", "Mei", "Zara", "Matilda", "Sienna", "Grace"]
BOYS = ["Oliver", "Jack", "Noah", "William", "Leo", "Lachlan", "Liam", "Aarav", "Kai", "Cooper", "Ethan"]
PLACE = ["ones", "tens", "hundreds", "thousands", "ten thousands"]
COLS = ["TTh", "Th", "H", "T", "O"]


# ------------------------------------------------------------ helpers
def f(n):
    """4536 -> 4536, 12350 -> 12 350 (no-break space)."""
    s = str(abs(n))
    if len(s) >= 5:
        g = []
        while s:
            g.insert(0, s[-3:])
            s = s[:-3]
        s = NB.join(g)
    return ("−" if n < 0 else "") + s


def mcq(q, correct, cands, e):
    """4 choices: correct + the first 3 unique distractors (no zero, negative or fractional numbers)."""
    correct = str(correct)
    seen = {correct}
    pick = []
    for c in cands:
        if isinstance(c, (int, float)) and (c <= 0 or c != int(c)):
            continue
        c = str(c)
        if c in seen or not c:
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
            wrong = [x for i, x in enumerate(c) if i != it["a"]]
            rnd.shuffle(wrong)
            right = c[it["a"]]
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


def fig(svg):
    return "<div class='qfig'>" + svg + "</div>"


def svg_wrap(w, h, body, label):
    return ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 %d %d' width='%d' height='%d' "
            "role='img' aria-label='%s'><g font-family='%s'>%s</g></svg>" % (w, h, w, h, label, FONT, body))


def text(x, y, t, fs=18, col=INK, anchor="middle", weight="700"):
    return ("<text x='%.1f' y='%.1f' font-size='%d' font-weight='%s' fill='%s' text-anchor='%s'>%s</text>"
            % (x, y, fs, weight, col, anchor, t))


def unit(k, i):
    """3 hundreds, 1 hundred."""
    w = PLACE[i]
    if k == 1:
        w = w[:-1]
    return "%d %s" % (k, w)


def digits(n):
    return [int(c) for c in reversed(str(n))]          # ones first


def mark_large(u, pattern):
    """Tag place value charts so they print large enough to read."""
    rx = re.compile(r"<svg (?=[^>]*aria-label='(?:" + pattern + "))")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u


# ------------------------------------------------------------ place value chart
def pv_svg(a, b, op, show_b=True, hide_op=False):
    """Place value chart (TTh Th H T O). a on the top row, b below it. Red arrows show each digit of a
    moving to its new column (left for ×, right for ÷). show_b=False leaves the bottom row empty.
    Zeros that hold empty places in the answer are drawn green."""
    shift = {"× 10": 1, "× 100": 2, "÷ 10": -1, "÷ 100": -2}[op]
    cw, x0, y0, hh, rh = 54, 4, 4, 30, 54
    nc = len(COLS)
    W = x0 + nc * cw + 84
    H = y0 + hh + 2 * rh + 4
    out = ["<rect x='%d' y='%d' width='%d' height='%d' fill='%s'/>" % (x0, y0, nc * cw, hh, FILL)]
    for i in range(nc + 1):
        out.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='1.5'/>"
                   % (x0 + i * cw, y0, x0 + i * cw, y0 + hh + 2 * rh, GREEN))
    for y in (y0, y0 + hh, y0 + hh + rh, y0 + hh + 2 * rh):
        out.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='1.5'/>" % (x0, y, x0 + nc * cw, y, GREEN))
    for i, h in enumerate(COLS):
        out.append(text(x0 + i * cw + cw / 2, y0 + 21, h, 16, GREEN))

    def cx(place):                              # place 0 = ones (right-hand column)
        return x0 + (nc - 1 - place) * cw + cw / 2

    da = digits(a)
    assert len(da) <= nc and len(digits(b)) <= nc
    y1, y2 = y0 + hh + 35, y0 + hh + rh + 35
    for p, d in enumerate(da):
        out.append(text(cx(p), y1, d, 24))
    if show_b:
        db = digits(b)
        moved = {p + shift for p in range(len(da))}
        for p, d in enumerate(db):
            col = BLUE if p in moved else GREEN
            out.append(text(cx(p), y2, d, 24, col))
    for p, d in enumerate(da):
        q = p + shift
        if 0 <= q < len(digits(b)):
            xa, xb = cx(p), cx(q)
            dx = 1 if xb > xa else -1
            out.append("<line x1='%.1f' y1='%d' x2='%.1f' y2='%d' stroke='%s' stroke-width='2' marker-end='url(#ah)'/>"
                       % (xa + dx * 7, y1 + 6, xb - dx * 7, y2 - 22, RED))
    defs = ("<defs><marker id='ah' viewBox='0 0 10 10' refX='8' refY='5' markerWidth='6' markerHeight='6' orient='auto'>"
            "<path d='M0 0 L10 5 L0 10 z' fill='%s'/></marker></defs>" % RED)
    out.append(text(x0 + nc * cw + 42, y0 + hh + rh + 7, "?" if hide_op else op, 20, RED))
    lab = "place value chart: %d %s = %s" % (a, "?" if hide_op else op, b if show_b else "?")
    return svg_wrap(W, H, defs + "".join(out), lab)


# ------------------------------------------------------------ explanations
def move_text(a, k, left=True):
    """'the 3 tens become 3 hundreds and the 6 ones become 6 tens' for the non-zero digits of a."""
    da = digits(a)
    parts = []
    for p in range(len(da) - 1, -1, -1):
        if da[p]:
            q = p + k if left else p - k
            parts.append("the %s become%s %s" % (unit(da[p], p), "s" if da[p] == 1 else "", unit(da[p], q)))
    if len(parts) > 2:
        parts = parts[:1]
    return " and ".join(parts)


def fill_text(k):
    return {1: "A 0 holds the ones place", 2: "Zeros hold the tens and ones places"}[k]


def ins_zero(a, z=1):
    """Zero written in the wrong place: 36 -> 306, 124 -> 1024."""
    s = str(a)
    return int(s[0] + "0" * z + s[1:])


def no_zeros(a):
    """Every zero crossed out: 3050 -> 35."""
    return int(str(a).replace("0", ""))


# ------------------------------------------------------------ set 1: × 10 and × 100
def times_item(a, k, chart):
    m = 10 ** k
    ans = a * m
    op = "× %d" % m
    if k == 1:
        wrong = [a * 100, ins_zero(a), a + 10, a * 1000]
    else:
        wrong = [a * 10, a * 1000, a + 100, ins_zero(a, 2), ins_zero(a)]
    e = ("%s moves every digit %d place%s to the left: %s. %s. %s %s = <b>%s</b>."
         % (op, k, "" if k == 1 else "s", move_text(a, k), fill_text(k), f(a), op, f(ans)))
    if k == 2:
        e += " (%s × 10 = %s moves the digits only 1 place.)" % (f(a), f(a * 10))
    q = (fig(pv_svg(a, ans, op, show_b=False)) + "Use the place value chart. " if chart else "") + "What is %s %s?" % (f(a), op)
    return mcq(q, f(ans), [f(w) for w in wrong], e)


def set_times():
    its = []
    for a, k, chart in [(36, 1, True), (58, 1, False), (124, 1, True), (9, 2, False), (46, 2, True),
                        (305, 1, False), (73, 2, False), (460, 1, False), (208, 2, True), (890, 1, False),
                        (2047, 1, False), (350, 2, False), (125, 2, False)]:
        its.append(times_item(a, k, chart))
    MOVES = ["1 place to the left", "1 place to the right", "2 places to the left", "2 places to the right"]
    its.insert(2, mcq("When you multiply a number by 10, every digit moves …", MOVES[0], MOVES[1:],
                      "× 10 makes every digit 10 times bigger, so each digit moves <b>1 place to the left</b>. "
                      "Example: 24 × 10 = 240."))
    its.insert(6, mcq("When you multiply a number by 100, every digit moves …", MOVES[2], [MOVES[0], MOVES[3], MOVES[1]],
                      "× 100 is × 10 and then × 10 again, so each digit moves <b>2 places to the left</b>. "
                      "Example: 24 × 100 = 2400."))
    its.append(mcq("In 47 × 10, the 4 tens become 4 …", "hundreds", ["thousands", "tens", "ones"],
                   "× 10 moves every digit 1 place to the left. The 4 tens move into the <b>hundreds</b> place: 47 × 10 = 470."))
    its.append(mcq("In 63 × 100, the 3 ones become 3 …", "hundreds", ["tens", "thousands", "ones"],
                   "× 100 moves every digit 2 places to the left: ones → tens → <b>hundreds</b>. 63 × 100 = 6300."))
    assert 52 * 100 == 5200 and 805 * 10 == 8050
    OPS = ["× 10", "× 100", "× 1000", "÷ 100"]
    its.append(mcq(fig(pv_svg(52, 5200, "× 100", hide_op=True))
                   + "52 has changed to 5200. What was 52 multiplied by?", "× 100", ["× 10", "× 1000", "÷ 100"],
                   "The 5 tens became 5 thousands: every digit moved <b>2 places</b> to the left. That is <b>× 100</b>. "
                   "Count the new zeros: 52 → 5200 has 2 more zeros."))
    its.append(mcq(fig(pv_svg(805, 8050, "× 10", hide_op=True))
                   + "805 has changed to 8050. What was 805 multiplied by?", "× 10", ["× 100", "× 1000", "÷ 10"],
                   "The 8 hundreds became 8 thousands: every digit moved <b>1 place</b> to the left. That is <b>× 10</b>. "
                   "The 0 inside 805 moves too, so the answer is 8050, not 8500."))
    its.append(mcq("Which number is 10 times as large as 380?", f(3800), [f(38), f(38000), f(390)],
                   "10 times as large means × 10. Every digit moves 1 place to the left: 380 × 10 = <b>3800</b>. "
                   "(390 is only 10 more.)"))
    assert len(its) == 20, len(its)
    return {"title": "× 10 and × 100 on a place value chart", "items": its}


# ------------------------------------------------------------ set 2: ÷ 10 and ÷ 100
def div_item(a, k, chart):
    m = 10 ** k
    assert a % m == 0
    ans = a // m
    op = "÷ %d" % m
    if k == 1:
        wrong = [a * 10, no_zeros(a), a // 100 if a % 100 == 0 else a - 10, a - 10]
    else:
        wrong = [a // 10, a * 100, no_zeros(a), a // 1000 if a % 1000 == 0 else a - 100, a - 100]
    e = ("%s moves every digit %d place%s to the right: %s. %s %s = <b>%s</b>."
         % (op, k, "" if k == 1 else "s", move_text(a, k, left=False), f(a), op, f(ans)))
    if no_zeros(a) != ans:
        e += " Only %s zero%s from the end drop%s off; any other zeros still hold places." % ("one" if k == 1 else "two", "" if k == 1 else "s", "s" if k == 1 else "")
    q = (fig(pv_svg(a, ans, op, show_b=False)) + "Use the place value chart. " if chart else "") + "What is %s %s?" % (f(a), op)
    return mcq(q, f(ans), [f(w) for w in wrong], e)


def set_divide(P):
    its = []
    for a, k, chart in [(600, 1, False), (4500, 1, True), (800, 2, False), (3600, 1, False), (4700, 2, True),
                        (900, 1, False), (6000, 2, False), (2080, 1, True), (9300, 2, False), (40500, 1, False),
                        (2400, 2, True), (5010, 1, False), (12000, 2, False), (12300, 1, False), (30500, 2, False),
                        (50000, 2, False)]:
        its.append(div_item(a, k, chart))
    MOVES = ["2 places to the right", "1 place to the right", "2 places to the left", "1 place to the left"]
    its.insert(4, mcq("When you divide a number by 100, every digit moves …", MOVES[0], MOVES[1:],
                      "÷ 100 makes every digit 100 times smaller, so each digit moves <b>2 places to the right</b>. "
                      "Example: 2400 ÷ 100 = 24."))
    its.insert(9, mcq("In 4300 ÷ 100, the 4 thousands become 4 …", "tens", ["hundreds", "ones", "ten thousands"],
                      "÷ 100 moves every digit 2 places to the right: thousands → hundreds → <b>tens</b>. 4300 ÷ 100 = 43."))
    its.append(mcq("Which number sentence is true?", "800 ÷ 10 = 80",
                   ["800 ÷ 10 = 8", "800 ÷ 100 = 80", "80 ÷ 10 = 800"],
                   "÷ 10 moves every digit 1 place to the right, so 800 ÷ 10 = <b>80</b>. 800 ÷ 100 = 8, and 80 ÷ 10 = 8."))
    n, he, his = P.next()
    assert 3050 // 10 == 305
    its.append(mcq("%s says 3050 ÷ 10 = 35 because “you take off the zeros”. What is 3050 ÷ 10?" % n,
                   "305", ["35", f(30500), "350"],
                   "÷ 10 moves every digit 1 place to the right: the 3 thousands become 3 hundreds and the 5 tens become 5 ones. "
                   "The 0 in the hundreds place moves to the tens place and must stay. 3050 ÷ 10 = <b>305</b>."))
    assert len(its) == 20, len(its)
    return {"title": "÷ 10 and ÷ 100 of numbers ending in zeros", "items": its}


# ------------------------------------------------------------ set 3: multiples of 10 and 100
def mult_item(a, b):
    """a or b is a multiple of 10 or 100; the other is a one-digit number (or 40 × 20)."""
    ans = a * b
    big, small = (a, b) if a % 10 == 0 and (b % 10 or a >= b) else (b, a)
    z = len(str(big)) - len(str(big).rstrip("0"))
    t = big // 10 ** z
    zw = PLACE[z]
    if small % 10 == 0:                          # tens × tens
        s2 = small // 10
        fact = t * s2
        wrong = [ans // 10, ans * 10, t * 10 + small, a + b]
        e = ("Use %d × %d = %d. %s tens × %s tens = %d hundreds, so put back two zeros: %d × %d = <b>%s</b>."
             % (t, s2, fact, t, s2, fact, a, b, f(ans)))
        return mcq("What is %d × %d?" % (a, b), f(ans), [f(w) for w in wrong], e)
    fact = t * small
    wrong = [ans // 10, ans * 10, fact if z > 1 else a + b, a + b, ans * 100]
    e = "%s is %s. %d × %d = %d, so %s × %d = %d %s = <b>%s</b>." % (
        f(big), unit(t, z), t, small, fact, f(big), small, fact, zw, f(ans))
    if fact % 10 == 0:
        e += " The 0 in %d is part of the fact, so keep it as well." % fact
    return mcq("What is %d × %d?" % (a, b), f(ans), [f(w) for w in wrong], e)


def div_mult_item(a, d):
    ans = a // d
    assert ans * d == a
    z = len(str(ans)) - len(str(ans).rstrip("0"))
    chunk = a // 10 ** z                          # 600 -> 6 hundreds, 400 ÷ 8 -> 40 tens
    zw = PLACE[z]
    wrong = [ans // 10, ans * 10, ans // 10 ** z, a - d]
    e = ("%s is %d %s. %d ÷ %d = %d, so %s ÷ %d = %d %s = <b>%s</b>. Check: %s × %d = %s."
         % (f(a), chunk, zw, chunk, d, chunk // d, f(a), d, chunk // d, zw if chunk // d != 1 else zw[:-1], f(ans),
            f(ans), d, f(a)))
    return mcq("What is %s ÷ %d?" % (f(a), d), f(ans), [f(w) for w in wrong], e)


def set_multiples():
    its = []
    for a, b in [(30, 4), (4, 70), (60, 5), (200, 7), (6, 300)]:
        its.append(mult_item(a, b))
    for a, d in [(120, 4), (600, 3), (350, 5)]:
        its.append(div_mult_item(a, d))
    its.append(mcq("Which fact helps you work out 70 × 6?", "7 × 6 = 42",
                   ["70 + 6 = 76", "7 × 10 = 70", "6 × 10 = 60"],
                   "70 is 7 tens. Use <b>7 × 6 = 42</b>: 7 tens × 6 = 42 tens, so 70 × 6 = 420."))
    for a, b in [(50, 8), (500, 6), (800, 4), (40, 9), (700, 8), (40, 20)]:
        its.append(mult_item(a, b))
    its.append(mcq("Which fact helps you work out 3600 ÷ 9?", "36 ÷ 9 = 4",
                   ["3600 − 9 = 3591", "9 × 10 = 90", "6 ÷ 3 = 2"],
                   "3600 is 36 hundreds. Use <b>36 ÷ 9 = 4</b>: 36 hundreds ÷ 9 = 4 hundreds, so 3600 ÷ 9 = 400."))
    for a, d in [(2400, 6), (400, 8), (4500, 9), (3000, 5)]:
        its.append(div_mult_item(a, d))
    assert len(its) == 20, len(its)
    return {"title": "Multiples of 10 and 100: 30 × 4 and 600 ÷ 3", "items": its}


# ------------------------------------------------------------ set 4: missing numbers
def set_missing():
    its = []

    def add(q, ans, wrong, e, check):
        assert check, q
        its.append(mcq("Find the missing number: " + q if B in q else q, f(ans) if isinstance(ans, int) else ans,
                       [f(w) if isinstance(w, int) else w for w in wrong], e))

    B = "<b>?</b>"
    add("%s × 10 = 380" % B, 38, [3800, 370, 390],
        "Work backwards: 380 ÷ 10 = <b>38</b>. Check: 38 × 10 = 380.", 38 * 10 == 380)
    add("%s × 100 = 4500" % B, 45, [450, 450000, 4400],
        "Work backwards: 4500 ÷ 100 moves the digits 2 places to the right, so the missing number is <b>45</b>. "
        "450 × 100 would be 45 000.", 45 * 100 == 4500)
    add("72 × %s = 7200" % B, 100, [10, 1000, 7128],
        "The 7 tens became 7 thousands, so the digits moved 2 places to the left. That is × <b>100</b>.", 72 * 100 == 7200)
    add("640 = 64 × %s" % B, 10, [100, 1000, 576],
        "The digits moved 1 place to the left, so 64 × <b>10</b> = 640. (576 is 640 − 64: that is subtracting, not multiplying.)",
        64 * 10 == 640)
    add("%s ÷ 10 = 60" % B, 600, [6, 6000, 70],
        "Work backwards with the inverse: 60 × 10 = <b>600</b>. Check: 600 ÷ 10 = 60.", 600 // 10 == 60)
    add("%s ÷ 100 = 23" % B, 2300, [230, 23000, 123],
        "Work backwards with the inverse: 23 × 100 = <b>2300</b>. Check: 2300 ÷ 100 = 23.", 2300 // 100 == 23)
    add("8000 ÷ %s = 80" % B, 100, [10, 1000, 7920],
        "The 8 thousands became 8 tens: the digits moved 2 places to the right. That is ÷ <b>100</b>.", 8000 // 100 == 80)
    add("950 ÷ %s = 95" % B, 10, [100, 1000, 855],
        "The digits moved 1 place to the right: 950 ÷ <b>10</b> = 95. (855 is 950 − 95: that is subtracting.)", 950 // 10 == 95)
    add("How many tens are in 450?", 45, [5, 450, 4500],
        "450 = 45 × 10, so there are <b>45</b> tens in 450. The 5 is only the tens digit; the 4 hundreds are 40 more tens.",
        450 // 10 == 45)
    add("How many hundreds are in 3200?", 32, [2, 320, 3],
        "3200 = 32 × 100, so there are <b>32</b> hundreds. The 2 is only the hundreds digit; the 3 thousands are 30 more hundreds.",
        3200 // 100 == 32)
    add("%s × 4 = 240" % B, 60, [6, 600, 236],
        "Use 6 × 4 = 24. 240 is 24 tens, so the missing number is 6 tens = <b>60</b>. Check: 60 × 4 = 240.", 60 * 4 == 240)
    add("7 × %s = 350" % B, 50, [5, 500, 343],
        "Use 7 × 5 = 35. 350 is 35 tens, so the missing number is 5 tens = <b>50</b>. Check: 7 × 50 = 350.", 7 * 50 == 350)
    add("%s × 3 = 1800" % B, 600, [60, 6000, 1797],
        "Use 6 × 3 = 18. 1800 is 18 hundreds, so the missing number is 6 hundreds = <b>600</b>. Check: 600 × 3 = 1800.",
        600 * 3 == 1800)
    add("400 × %s = 2800" % B, 7, [70, 700, 2400],
        "400 is 4 hundreds and 2800 is 28 hundreds. 4 × 7 = 28, so the missing number is <b>7</b>. Check: 400 × 7 = 2800.",
        400 * 7 == 2800)
    add("360 ÷ %s = 90" % B, 4, [40, 400, 270],
        "Think 9 tens × ? = 36 tens. 9 × 4 = 36, so the missing number is <b>4</b>. Check: 360 ÷ 4 = 90. "
        "(270 is 360 − 90: that is subtracting.)", 360 // 4 == 90)
    add("%s ÷ 5 = 30" % B, 150, [6, 15, 35],
        "Use the inverse: 30 × 5 = 3 tens × 5 = 15 tens = <b>150</b>. Check: 150 ÷ 5 = 30. "
        "(6 is 30 ÷ 5, the wrong operation.)", 150 // 5 == 30)
    add("56 × 100 = 560 × %s" % B, 10, [100, 1, 1000],
        "56 × 100 = 5600. 560 is already 56 × 10, so it needs one more × <b>10</b>: 560 × 10 = 5600.",
        56 * 100 == 560 * 10)
    add("4800 ÷ 100 = 480 ÷ %s" % B, 10, [100, 1, 1000],
        "4800 ÷ 100 = 48. 480 ÷ <b>10</b> = 48 too. Both sides equal 48.", 4800 // 100 == 480 // 10 == 48)
    add("Which of these is correct?", "45 × 100 = 4500",
        ["45 × 10 = 4500", "450 ÷ 10 = 4500", "4500 ÷ 100 = 450"],
        "× 100 moves the digits 2 places to the left: <b>45 × 100 = 4500</b>. 45 × 10 = 450, 450 ÷ 10 = 45 and "
        "4500 ÷ 100 = 45.", 45 * 100 == 4500 and 45 * 10 != 4500 and 450 // 10 != 4500 and 4500 // 100 != 450)
    add("Which is equal to 2700?", "27 × 100", ["27 × 10", "270 × 100", "2700 ÷ 10"],
        "27 hundreds = 2700, so <b>27 × 100</b> = 2700. 27 × 10 = 270, 270 × 100 = 27 000 and 2700 ÷ 10 = 270.",
        27 * 100 == 2700 and 27 * 10 != 2700 and 270 * 100 != 2700 and 2700 // 10 != 2700)
    assert len(its) == 20, len(its)
    order = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 18, 19, 16, 17, 10, 11, 12, 13, 14, 15]
    its = [its[i] for i in order]
    return {"title": "Missing numbers: ? × 100 = 4500", "items": its}


# ------------------------------------------------------------ set 5: word problems
def set_words(P):
    its = []

    def add(q, right, wrong, e):
        its.append(mcq(q, right, wrong, e))

    def nm():
        return P.next()

    assert 24 * 100 == 2400
    add("Pencils come in boxes of 100. The school office orders 24 boxes. How many pencils is that?",
        "2400 pencils", ["240 pencils", f(24000) + " pencils", "124 pencils"],
        "24 boxes × 100 pencils. × 100 moves the digits 2 places to the left: 24 × 100 = <b>2400</b> pencils.")
    assert 28 * 10 == 280
    add("Each of the 28 students in Year 4 brings a $10 note for the school excursion. How much money is that?",
        "$280", ["$28", "$2800", "$38"],
        "28 students × $10. × 10 moves the digits 1 place to the left: 28 × 10 = <b>$280</b>.")
    assert 450 // 10 == 45
    n, he, his = nm()
    add("%s has saved $450, all in $10 notes. How many $10 notes does %s have?" % (n, he),
        "45 notes", ["450 notes", "4500 notes", "440 notes"],
        "How many tens are in 450? 450 ÷ 10 = <b>45</b> notes. Check: 45 × $10 = $450.")
    assert 3600 // 100 == 36
    add("The P&amp;C raised $3600 at the school fete. The treasurer counts it all in $100 notes. How many notes is that?",
        "36 notes", ["360 notes", "3500 notes", f(360000) + " notes"],
        "3600 ÷ 100 moves the digits 2 places to the right: <b>36</b> notes. Check: 36 × $100 = $3600.")
    assert 2 * 1000 == 2000
    add("1 km = 1000 m. The school cross-country course is 2 km long. How many metres is that?",
        "2000 m", ["200 m", f(20000) + " m", "1002 m"],
        "Each kilometre is 1000 m, so 2 km = 2 × 1000 m = <b>2000 m</b>.")
    assert 5000 // 1000 == 5
    add("A fun run in Perth is 5000 m long. How many kilometres is that?",
        "5 km", ["50 km", "500 km", "5000 km"],
        "1000 m = 1 km. 5000 m is 5 thousands of metres, so it is <b>5 km</b>. (5000 km would take days to drive!)")
    assert 8 * 100 == 800
    add("$1 = 100c. How many cents are in $8?",
        "800c", ["80c", "8000c", "108c"],
        "Each dollar is 100c, so $8 = 8 × 100c = <b>800c</b>.")
    n, he, his = nm()
    assert 40 * 10 == 400
    add("%s empties %s money box. It has 40 coins, and every coin is 10c. How much money is that?" % (n, his),
        "$4", ["$40", "40c", "$400"],
        "40 × 10c = 400c. 100c = $1, so 400c = <b>$4</b>. (40c is only 4 coins.)")
    assert 18 * 10 == 180
    add("1 cm = 10 mm. A new pencil is 18 cm long. How long is it in millimetres?",
        "180 mm", ["1800 mm", "28 mm", "108 mm"],
        "Each centimetre is 10 mm, so 18 cm = 18 × 10 mm = <b>180 mm</b>.")
    assert 9 * 100 == 900
    add("1 m = 100 cm. The classroom is 9 m long. How long is it in centimetres?",
        "900 cm", ["90 cm", "9000 cm", "109 cm"],
        "Each metre is 100 cm, so 9 m = 9 × 100 cm = <b>900 cm</b>.")
    assert 30 * 8 == 240
    add("At the school sausage sizzle, each class gets 30 sausages. There are 8 classes. How many sausages are needed?",
        "240 sausages", ["24 sausages", "2400 sausages", "38 sausages"],
        "8 × 3 = 24, so 30 × 8 = 24 tens = <b>240</b> sausages.")
    assert 600 // 3 == 200
    add("A footy club has 600 raffle tickets. Three teams share them equally to sell. How many tickets does each team get?",
        "200 tickets", ["20 tickets", "2000 tickets", "597 tickets"],
        "600 is 6 hundreds. 6 ÷ 3 = 2, so 600 ÷ 3 = 2 hundreds = <b>200</b> tickets. Check: 200 × 3 = 600.")
    assert 480 // 10 == 48
    add("A bakery puts 480 bread rolls into bags of 10. How many bags does it fill?",
        "48 bags", ["4800 bags", "470 bags", "490 bags"],
        "480 ÷ 10 moves the digits 1 place to the right: <b>48</b> bags. Check: 48 × 10 = 480.")
    assert 1500 // 100 == 15
    add("Tea bags come in boxes of 100. The school canteen uses 1500 tea bags in a term. How many boxes is that?",
        "15 boxes", ["150 boxes", "1400 boxes", f(150000) + " boxes"],
        "1500 ÷ 100 moves the digits 2 places to the right: <b>15</b> boxes. Check: 15 × 100 = 1500.")
    assert 6 * 20 == 120
    add("A wildlife park orders 6 bags of kangaroo food. Each bag holds 20 kg. How many kilograms is that?",
        "120 kg", ["12 kg", "1200 kg", "26 kg"],
        "6 × 2 = 12, so 6 × 20 = 12 tens = <b>120 kg</b>.")
    n, he, his = nm()
    assert 400 * 5 == 2000
    add("One lap of the school oval is 400 m. %s runs 5 laps at the athletics carnival. How far does %s run?" % (n, he),
        "2000 m", ["200 m", f(20000) + " m", "405 m"],
        "4 × 5 = 20, so 400 × 5 = 20 hundreds = <b>2000 m</b>. That is 2 km. The 0 in 20 is part of the fact, so keep it.")
    assert 900 * 3 == 2700
    add("A water truck carries 900 L to a farm each day. How much water does it carry in 3 days?",
        "2700 L", ["270 L", f(27000) + " L", "903 L"],
        "9 × 3 = 27, so 900 × 3 = 27 hundreds = <b>2700 L</b>.")
    assert 4 * 100 + 6 * 10 == 460
    add("The school orders 4 boxes of 100 pencils and 6 packs of 10 pencils. How many pencils is that altogether?",
        "460 pencils", ["4600 pencils", "1000 pencils", "406 pencils"],
        "Boxes: 4 × 100 = 400. Packs: 6 × 10 = 60. Total: 400 + 60 = <b>460</b> pencils. "
        "(1000 treats the packs as 100s; 406 forgets that each pack has 10.)")
    n, he, his = nm()
    assert 10 * 20 - 150 == 50
    add("%s puts $10 into %s savings every week for 20 weeks. Then %s spends $150 on a new bike helmet and lights. "
        "How much does %s have left?" % (n, his, he, he),
        "$50", ["$200", "$350", "$1850"],
        "Step 1: 20 × $10 = $200. Step 2: $200 − $150 = <b>$50</b>. ($200 is only step 1; $350 adds instead of subtracting; $1850 comes from 20 × $10 = $2000, one zero too many.)")
    (n1, he1, _), (n2, _, _) = nm(), nm()
    assert 3 * 1000 - 2800 == 200
    add("%s rides 3 km to netball training. %s rides 2800 m to footy training. How much further does %s ride?" % (n1, n2, n1),
        "200 m", ["2797 m", "20 m", "5800 m"],
        "Change km to m first: 3 km = 3 × 1000 m = 3000 m. Then 3000 − 2800 = <b>200 m</b>. "
        "(2797 comes from 2800 − 3 without changing the units.)")
    assert len(its) == 20, len(its)
    return {"title": "Word problems: boxes of 100, $10 notes and 1000 m in a km", "items": its}


# ------------------------------------------------------------ lesson
def table(head, rows):
    h = "".join("<th>%s</th>" % x for x in head)
    b = "".join("<tr>" + "".join("<td>%s</td>" % c for c in r) + "</tr>" for r in rows)
    return "<div class='sn-tw'><table class='sn-table'><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>" % (h, b)


def ex(title, q, s, a):
    return ("<div class='sn-ex'><span class='sn-ex-t'>%s</span><p class='sn-ex-q'>%s</p>"
            "<p class='sn-ex-s'>%s</p><p class='sn-ex-a'>Answer: %s</p></div>" % (title, q, s, a))


def body_html():
    assert 47 * 100 == 4700 and 3050 // 10 == 305 and 60 * 7 == 420 and 2400 // 6 == 400 and 3600 // 100 == 36
    return (
        "<h2>Each place is worth 10 times the place to its right</h2>"
        "<p>When you multiply by 10, every digit becomes 10 times bigger, so it moves <b>1 place to the left</b>. "
        "When you multiply by 100, every digit moves <b>2 places to the left</b>. A 0 holds each empty place.</p>"
        "<figure class='sn-fig'>" + pv_svg(47, 4700, "× 100") +
        "<figcaption>47 × 100 = 4700. The 4 tens become 4 thousands and the 7 ones become 7 hundreds. "
        "The green zeros hold the tens and ones places.</figcaption></figure>"
        "<h2>Dividing by 10 and 100</h2>"
        "<p>Dividing is the inverse. ÷ 10 moves every digit <b>1 place to the right</b>; ÷ 100 moves every digit "
        "<b>2 places to the right</b>. Zeros drop off only from the end: one for ÷ 10, two for ÷ 100. Zeros in the middle stay.</p>"
        "<figure class='sn-fig'>" + pv_svg(3050, 305, "÷ 10") +
        "<figcaption>3050 ÷ 10 = 305. The 0 in the middle moves too and still holds the tens place.</figcaption></figure>"
        "<h2>Multiples of 10 and 100</h2>"
        "<p>Use a fact you know, then think about place value. 60 is 6 tens, so 60 × 7 is 6 × 7 = 42 tens = <b>420</b>.</p>" +
        ex("Multiply", "300 × 4 = ?", "300 is 3 hundreds. 3 × 4 = 12, so 300 × 4 = 12 hundreds.", "1200") +
        ex("Divide", "2400 ÷ 6 = ?", "2400 is 24 hundreds. 24 ÷ 6 = 4, so 2400 ÷ 6 = 4 hundreds. Check: 400 × 6 = 2400.", "400") +
        ex("Missing number", "? × 100 = 3600", "Work backwards with the inverse: 3600 ÷ 100 = 36.", "36") +
        "<h2>Common mistakes</h2>" +
        table(["Mistake", "What to do instead"], [
            ["Writing the 0 in the wrong place (36 × 10 = 306)", "Move every digit 1 place left; the 0 goes in the ones place: 360"],
            ["Moving the wrong way (450 ÷ 10 = 4500)", "÷ makes a number smaller: digits move right, 450 ÷ 10 = 45"],
            ["Taking off every zero (3050 ÷ 10 = 35)", "Only the end zero goes; the middle 0 still holds a place: 305"],
            ["Dropping the zero from the fact (50 × 8 = 40)", "5 × 8 = 40, so 50 × 8 = 40 tens = 400"],
            ["× 100 with only one zero (46 × 100 = 460)", "× 100 moves digits 2 places: 4600"],
        ])
    )


FAQ = [
    {"q": "How do you multiply by 10 and 100 in Year 4?",
     "a": "Every digit moves to a bigger place: 1 place to the left for × 10 and 2 places for × 100, with zeros holding the empty places. For example, 47 × 100 = 4700."},
    {"q": "Why is “just add a zero” not a good rule?",
     "a": "It does not explain what happens and can put the zero in the wrong place, such as 36 × 10 = 306. It also breaks later with decimals: 0.4 × 10 is 4, not 0.40. Moving digits on a place value chart always works."},
    {"q": "What does AC9M4N05 mean in the Australian Curriculum?",
     "a": "It is the Year 4 maths content description for multiplying and dividing natural numbers by multiples and powers of 10 without a calculator, using place value. For example, 30 × 4 = 120 and 600 ÷ 3 = 200."},
    {"q": "How can my child work out 30 × 4 in their head?",
     "a": "Use the fact 3 × 4 = 12. 30 is 3 tens, so 30 × 4 is 12 tens, which is 120."},
]


def gen():
    rnd = random.Random(4806)
    P = People(rnd)
    sets = [set_times(), set_divide(P), set_multiples(), set_missing(), set_words(P)]
    balance(sets, rnd)
    seen = set()
    for s in sets:
        assert len(s["items"]) == 20, (s["title"], len(s["items"]))
        assert sorted(it["a"] for it in s["items"]) == sorted([0, 1, 2, 3] * 5)
        for it in s["items"]:
            assert len(set(it["c"])) == 4, it
            assert it["q"].count("<svg") <= 1, it["q"]
            k = re.sub(r"<[^>]+>", "", it["q"])
            assert k not in seen, it["q"]
            seen.add(k)
    u = {
        "country": "au", "subject": "maths", "grade": "year-4", "slug": "multiplying-and-dividing-by-10-and-100",
        "sort": 6, "updated": UPDATED, "pdf_url": "",
        "title": "Multiplying and Dividing by 10 and 100: Place Value, Multiples of 10 and Missing Numbers",
        "seo_title": "Year 4 Multiplying and Dividing by 10 and 100 Worksheets: Free Maths with Answer Key (Australian Curriculum)",
        "short_title": "× and ÷ by 10 and 100",
        "domain": "Number",
        "standard_code": "AC9M4N05",
        "standard_url": "https://v9.australiancurriculum.edu.au/f-10-curriculum/learning-areas/mathematics",
        "standard_text": "Solve problems involving multiplying or dividing natural numbers by multiples and powers of 10 without a calculator, using the multiplicative relationship between the place value of digits",
        "meta_desc": "Free Year 4 maths worksheets on multiplying and dividing by 10 and 100, aligned to the Australian Curriculum (AC9M4N05): moving digits on a place value chart, multiples of 10 and 100 like 30 × 4 and 600 ÷ 3, missing numbers and word problems with $10 notes and kilometres. 100 questions with an answer key.",
        "key_big": "× 10 moves every digit 1 place to the left; × 100 moves it 2 places. ÷ 10 and ÷ 100 move the digits right.",
        "key_sub": "47 × 100 = 4700 and 3050 ÷ 10 = 305: zeros hold the empty places. For multiples of 10, use a fact: 3 × 4 = 12, so 30 × 4 = 12 tens = 120.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }
    return mark_large(u, "place value chart")


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
