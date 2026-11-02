# -*- coding: utf-8 -*-
"""
UK Year 4 Maths: Mental multiplication and division (National Curriculum in England)
  python3 tools/gen_uk_maths_y4_mental_mult_div.py
Every answer is checked in code. HTML attributes use single quotes (no backslashes in the JSON).
"""
import json, os, random, re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "uk", "maths", "year-4")
UPDATED = "2026-11-02"
GREEN = "#006633"
BLUE = "#2f6fb0"
FILL = "#cfe6d6"
GREY = "#8a8a8a"
RED = "#c0392b"
INK = "#2b2b2b"
FONT = "Arial, Helvetica, sans-serif"
GIRLS = ["Amelia", "Isla", "Freya", "Poppy", "Ava", "Aisha", "Lily", "Zara", "Grace", "Ruby", "Maya", "Evie"]
BOYS = ["Oliver", "Harry", "Mohammed", "Jack", "Arjun", "Noah", "George", "Leo", "Alfie", "Kai", "Ethan", "Charlie"]


# ------------------------------------------------------------ numbers
def n(x):
    """1,000 and above get a comma."""
    return "{:,}".format(x)


def money(p):
    """Pence below £1, pounds and pence from £1."""
    return "%dp" % p if p < 100 else "£%d.%02d" % divmod(p, 100)


def factors(x):
    return [d for d in range(1, x + 1) if x % d == 0]


def pairs(x):
    return [(d, x // d) for d in factors(x) if d * d <= x]


# ------------------------------------------------------------ helpers
def mcq(q, correct, cands, e):
    """4 choices: correct + the first 3 unique distractors. Positions are set later by balance()."""
    correct = str(correct)
    seen = {correct}
    pick = []
    for c in cands:
        c = str(c)
        if c in seen or not c or c.startswith("-"):
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


def mark_large(u, pattern):
    """Tag pictures that must print larger (wide charts) so every digit can be read."""
    rx = re.compile(r"<svg (?=[^>]*aria-label='(?:" + pattern + "))")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u


# ------------------------------------------------------------ pictures
def array_svg(rows, cols, s=22):
    r = 7
    body = "".join("<circle cx='%d' cy='%d' r='%d' fill='%s'/>" % (6 + c * s + s // 2, 6 + j * s + s // 2, r, GREEN)
                   for j in range(rows) for c in range(cols))
    return svg_wrap(cols * s + 12, rows * s + 12, body, "array of counters in %d rows of %d" % (rows, cols))


COLS = ["Th", "H", "T", "O"]


def pv_svg(a, b, op):
    """Place value chart: a on the top row, b below it. Arrows show every digit moving one column
    (left for × 10, right for ÷ 10)."""
    cw, x0, hh, rh = 50, 6, 30, 52
    W = x0 + 4 * cw + 74
    H = hh + 2 * rh + 6
    shift = -1 if op == "× 10" else 1
    out = ["<rect x='%d' y='%d' width='%d' height='%d' fill='%s'/>" % (x0, 4, 4 * cw, hh, FILL)]
    for i in range(5):
        out.append("<line x1='%d' y1='4' x2='%d' y2='%d' stroke='%s' stroke-width='1.5'/>"
                   % (x0 + i * cw, x0 + i * cw, 4 + hh + 2 * rh, GREEN))
    for y in (4, 4 + hh, 4 + hh + rh, 4 + hh + 2 * rh):
        out.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='1.5'/>" % (x0, y, x0 + 4 * cw, y, GREEN))
    for i, h in enumerate(COLS):
        out.append(text(x0 + i * cw + cw / 2, 4 + 21, h, 16, GREEN))

    def digits(v):
        s = str(v)
        return {4 - len(s) + k: d for k, d in enumerate(s)}

    da, db = digits(a), digits(b)
    y1, y2 = 4 + hh + 34, 4 + hh + rh + 34
    for i, d in da.items():
        out.append(text(x0 + i * cw + cw / 2, y1, d, 22))
    for i, d in db.items():
        out.append(text(x0 + i * cw + cw / 2, y2, d, 22, BLUE))
    for i in da:
        j = i + shift
        if j in db:
            xa, xb = x0 + i * cw + cw / 2, x0 + j * cw + cw / 2
            xs, xe = xa + shift * 8, xb - shift * 8
            out.append("<line x1='%.1f' y1='%d' x2='%.1f' y2='%d' stroke='%s' stroke-width='2' marker-end='url(#ah)'/>"
                       % (xs, y1 + 6, xe, y2 - 20, RED))
    defs = ("<defs><marker id='ah' viewBox='0 0 10 10' refX='8' refY='5' markerWidth='6' markerHeight='6' orient='auto'>"
            "<path d='M0 0 L10 5 L0 10 z' fill='%s'/></marker></defs>" % RED)
    out.append(text(x0 + 4 * cw + 37, 4 + hh + rh + 6, op, 18, RED))
    return svg_wrap(W, H, defs + "".join(out), "place value chart: %d %s = %d" % (a, op, b))


# ------------------------------------------------------------ set 1: × 0, × 1, ÷ 1
def set_zero_one(P):
    its = []
    for q, v in [("8 × 1", 8), ("1 × 6", 6), ("1 × 12", 12), ("157 × 1", 157)]:
        its.append(mcq("What is %s?" % q, v, [1, v + 1, 0],
                       "Multiplying by 1 keeps the number the same. %s = <b>%d</b>. (One lot of %d is %d.)" % (q, v, v, v)))
    for q, v in [("7 × 0", 7), ("0 × 9", 9), ("11 × 0", 11), ("0 × 245", 245)]:
        assert eval(q.replace("×", "*")) == 0
        its.append(mcq("What is %s?" % q, 0, [v, 1, n(v * 10)],
                       "Multiplying by 0 always gives 0. %s means %s, so there is nothing at all. "
                       "Writing a 0 on the end is the rule for × 10, not × 0."
                       % (q, "%d lots of 0" % v if q.endswith("0") else "0 lots of %d" % v)))
    for v in [8, 12, 60, 314]:
        its.append(mcq("What is %d ÷ 1?" % v, v, [1, 0, v - 1],
                       "Dividing by 1 keeps the number the same. Share %d into 1 group and all %d are in that group. "
                       "%d ÷ 1 = <b>%d</b>." % (v, v, v, v)))
    its.append(mcq("Find the missing number: <b>?</b> × 9 = 9", 1, [0, 9, 10],
                   "Only 1 keeps the number the same: 1 × 9 = 9. 0 × 9 = 0 and 9 × 9 = 81."))
    its.append(mcq("Find the missing number: 12 × <b>?</b> = 0", 0, [1, 12, 10],
                   "A product is 0 only when you multiply by 0: 12 × 0 = 0. 12 × 1 = 12."))
    its.append(mcq("Find the missing number: 25 ÷ <b>?</b> = 25", 1, [0, 25, 5],
                   "Dividing by 1 keeps the number the same: 25 ÷ 1 = 25. 25 ÷ 25 = 1 and 25 ÷ 5 = 5."))
    its.append(mcq("Which calculation is correct?", "6 × 0 = 0", ["6 × 0 = 6", "6 ÷ 1 = 1", "6 × 1 = 7"],
                   "Times 0 gives 0, so 6 × 0 = 0 is correct. 6 × 0 is not 6, 6 ÷ 1 is 6 (not 1), and 6 × 1 is 6 (not 7)."))
    its.append(mcq("Which calculation is correct?", "9 ÷ 1 = 9", ["9 ÷ 1 = 1", "9 × 0 = 9", "0 × 9 = 90"],
                   "Dividing by 1 keeps the number: 9 ÷ 1 = 9. Anything times 0 is 0, in either order."))
    its.append(mcq("What is 6 × 8 × 0?", 0, [48, 14, 480],
                   "6 × 8 = 48, then 48 × 0 = <b>0</b>. If one of the numbers is 0, the answer is always 0."))
    its.append(mcq("What is 1 × 7 × 1?", 7, [1, 9, 0],
                   "1 × 7 = 7, then 7 × 1 = <b>7</b>. Multiplying by 1 never changes the number. (9 comes from adding.)"))
    its.append(mcq("Which calculation has a <b>different</b> answer from the others?", "5 × 0",
                   ["5 × 1", "1 × 5", "5 ÷ 1"],
                   "5 × 1, 1 × 5 and 5 ÷ 1 all equal 5. <b>5 × 0</b> = 0."))
    assert len(its) == 20, len(its)
    return {"title": "Multiply by 0 and 1, divide by 1", "items": its}


# ------------------------------------------------------------ set 2: place value and derived facts
def set_place_value(P):
    its = []
    its.append(mcq(fig(pv_svg(36, 360, "× 10")) + "What is 36 × 10?", "360", [n(3600), 46, 306],
                   "× 10 moves every digit one place to the left: 3 tens become 3 hundreds and 6 ones become 6 tens. "
                   "A 0 holds the ones place. 36 × 10 = <b>360</b>."))
    for q, v, cands, e in [
            ("100 × 8", 800, [80, n(8000), 108], "× 100 moves the digit two places to the left: 8 ones become 8 hundreds. 100 × 8 = <b>800</b>."),
            ("45 × 100", 4500, [450, n(45000), 145], "× 100 moves both digits two places to the left: 45 × 100 = <b>4,500</b>. 450 is only × 10."),
            ("10 × 70", 700, [70, n(7000), 80], "70 is 7 tens. 10 × 7 tens = 70 tens = <b>700</b>.")]:
        assert eval(q.replace("×", "*")) == v
        its.append(mcq("What is %s?" % q, n(v), cands, e))
    its.append(mcq(fig(pv_svg(420, 42, "÷ 10")) + "What is 420 ÷ 10?", 42, [n(4200), 410, 402],
                   "÷ 10 moves every digit one place to the right: 4 hundreds become 4 tens and 2 tens become 2 ones. "
                   "420 ÷ 10 = <b>42</b>."))
    its.append(mcq("What is 3,500 ÷ 100?", 35, [350, n(3400), 305],
                   "÷ 100 moves every digit two places to the right: 3,500 ÷ 100 = <b>35</b>. 350 is only ÷ 10."))
    # derived multiplication facts
    for fact, q, v, cands in [
            ("6 × 7 = 42", "60 × 7", 420, [42, n(4200), 402]),
            ("8 × 3 = 24", "8 × 300", 2400, [240, n(24000), 24]),
            ("9 × 4 = 36", "9 × 40", 360, [36, n(3600), 49]),
            ("12 × 5 = 60", "12 × 50", 600, [60, n(6000), 62])]:
        a, b = [int(x) for x in q.split(" × ")]
        assert a * b == v
        big = a if a >= 10 and a % 10 == 0 else b
        small_f = fact.split(" = ")[0]
        if big % 100 == 0:
            why = "%d is %d hundreds, so the answer is %s hundreds" % (big, big // 100, fact.split(" = ")[1])
        else:
            why = "%d is %d tens, so the answer is %s tens" % (big, big // 10, fact.split(" = ")[1])
        its.append(mcq("You know that %s. What is %s?" % (fact, q), n(v), cands,
                       "Use the fact %s. %s: %s = <b>%s</b>." % (small_f, why, q, n(v))))
    its.append(mcq("What is 70 × 8?", 560, [56, n(5600), 78],
                   "7 × 8 = 56. 70 is 7 tens, so 70 × 8 = 56 tens = <b>560</b>. (78 comes from adding.)"))
    # derived division facts
    for fact, q, v, cands, e in [
            ("42 ÷ 7 = 6", "420 ÷ 7", 60, [6, 600, 70], "420 is 42 tens. 42 tens ÷ 7 = 6 tens = <b>60</b>. Check: 60 × 7 = 420."),
            (None, "360 ÷ 9", 40, [4, 400, 351], "Use 36 ÷ 9 = 4. 360 is 36 tens, so 360 ÷ 9 = 4 tens = <b>40</b>. Check: 40 × 9 = 360."),
            (None, "480 ÷ 6", 80, [8, 800, 474], "Use 48 ÷ 6 = 8. 480 is 48 tens, so 480 ÷ 6 = 8 tens = <b>80</b>. Check: 80 × 6 = 480."),
            ("27 ÷ 9 = 3", "2,700 ÷ 9", 300, [30, n(3000), 3], "2,700 is 27 hundreds. 27 hundreds ÷ 9 = 3 hundreds = <b>300</b>. Check: 300 × 9 = 2,700.")]:
        a, b = [int(x.replace(",", "")) for x in q.split(" ÷ ")]
        assert a == v * b
        lead = "You know that %s. What is %s?" % (fact, q) if fact else "What is %s?" % q
        its.append(mcq(lead, v, cands, e))
    # missing numbers
    its.append(mcq("Find the missing number: <b>?</b> × 8 = 560", 70, [7, 700, 552],
                   "7 × 8 = 56, and 560 is 56 tens. So the missing number is 7 tens = <b>70</b>. Check: 70 × 8 = 560."))
    its.append(mcq("Find the missing number: 30 × <b>?</b> = 270", 9, [90, 900, 240],
                   "30 is 3 tens and 270 is 27 tens. 3 × 9 = 27, so the missing number is <b>9</b>. Check: 30 × 9 = 270."))
    its.append(mcq("Find the missing number: 400 ÷ <b>?</b> = 80", 5, [50, 8, 320],
                   "8 × 5 = 40, so 80 × 5 = 400. The missing number is <b>5</b>. Check: 400 ÷ 5 = 80."))
    its.append(mcq("Which fact helps you work out 50 × 9?", "5 × 9 = 45", ["50 + 9 = 59", "5 × 10 = 50", "9 × 10 = 90"],
                   "50 is 5 tens. Use <b>5 × 9 = 45</b>: 5 tens × 9 = 45 tens, so 50 × 9 = 450."))
    its.append(mcq("Which fact helps you work out 630 ÷ 7?", "63 ÷ 7 = 9", ["630 − 7 = 623", "70 × 7 = 490", "6 × 7 = 42"],
                   "630 is 63 tens. Use <b>63 ÷ 7 = 9</b>: 63 tens ÷ 7 = 9 tens, so 630 ÷ 7 = 90."))
    assert len(its) == 20, len(its)
    return {"title": "Use place value: × 10, × 100 and derived facts", "items": its}


# ------------------------------------------------------------ set 3: three numbers and order
def three_cands(a, b, c):
    return [a + b + c, b * c, a * b, a * b + c, a + b * c]


def set_three(P):
    its = []
    for a, b, c in [(2, 7, 5), (5, 6, 2), (2, 9, 5), (4, 9, 5), (2, 6, 7), (4, 5, 6)]:
        p = a * b * c
        if 10 in (a * c,):
            e = "Change the order to make 10 first: %d × %d = 10. Then 10 × %d = <b>%d</b>." % (a, c, b, p)
        elif a * b == 10:
            e = "Multiply %d × %d = 10 first. Then 10 × %d = <b>%d</b>." % (a, b, c, p)
        elif a * c == 20:
            e = "Change the order to make 20 first: %d × %d = 20. Then 20 × %d = <b>%d</b>. Remember to use all three numbers." % (a, c, b, p)
        elif a * b == 12:
            e = "%d × %d = 12. Then 12 × %d = <b>%d</b>. Remember to use all three numbers." % (a, b, c, p)
        else:
            e = ("%d × %d = %d. Then %d × %d = <b>%d</b>. Or %d × %d = %d first, then %d × %d = %d. "
                 "Remember to use all three numbers." % (a, b, a * b, a * b, c, p, a, c, a * c, a * c, b, p))
        its.append(mcq("What is %d × %d × %d?" % (a, b, c), p, three_cands(a, b, c), e))
    # best pair first
    for a, b, c, tgt in [(2, 13, 5, 10), (5, 8, 2, 10), (4, 7, 5, 20), (5, 3, 4, 20)]:
        x, y = (a, c)
        assert x * y == tgt and a * b * c == tgt * b
        other = [("%d × %d" % (a, b)), ("%d × %d" % (b, c)), ("%d + %d" % (a, c))]
        its.append(mcq("To work out %d × %d × %d in your head, which should you do first?" % (a, b, c),
                       "%d × %d" % (a, c), other,
                       "%d × %d = %d, a round number. Then %d × %d = <b>%d</b> is easy. You may multiply the numbers in any order."
                       % (a, c, tgt, tgt, b, tgt * b)))
    # commutativity: missing numbers
    for q, ans, cands, e in [
            ("9 × <b>?</b> = 4 × 9", 4, [9, 36, 5], "The same two numbers in a different order give the same answer: 9 × 4 = 4 × 9 = 36."),
            ("7 × 12 = 12 × <b>?</b>", 7, [12, 84, 19], "Swap the order: 7 × 12 = 12 × 7 = 84."),
            ("<b>?</b> × 6 = 6 × 11", 11, [6, 66, 5], "Swap the order: 11 × 6 = 6 × 11 = 66."),
            ("8 × 3 × 5 = 5 × 3 × <b>?</b>", 8, [3, 15, 120], "Both sides must use the same three numbers: 8, 3 and 5. Both equal 120.")]:
        its.append(mcq("Find the missing number: " + q, ans, cands, e))
    # regrouping: missing numbers
    for q, ans, cands, e in [
            ("3 × 4 × 5 = 12 × <b>?</b>", 5, [20, 60, 4], "3 × 4 = 12, and the 5 is still to be multiplied: 12 × 5 = 60."),
            ("4 × 5 × 7 = <b>?</b> × 7", 20, [9, 35, 140], "4 × 5 = 20, so 4 × 5 × 7 = 20 × 7 = 140. (9 comes from adding 4 + 5.)"),
            ("6 × 2 × 5 = 6 × <b>?</b>", 10, [7, 12, 60], "2 × 5 = 10, so 6 × 2 × 5 = 6 × 10 = 60. (7 comes from adding 2 + 5.)")]:
        its.append(mcq("Find the missing number: " + q, ans, cands, e))
    its.append(mcq("Which has the same answer as 4 × 3 × 5?", "20 × 3", ["4 + 3 + 5", "12 + 5", "4 × 8"],
                   "4 × 5 = 20, so 4 × 3 × 5 = <b>20 × 3</b> = 60. 12 + 5 forgets to multiply by 5, and 4 × 8 adds 3 + 5."))
    its.append(mcq("Which has the same answer as 7 × 6 × 2?", "7 × 12", ["7 × 8", "42 + 2", "13 × 2"],
                   "6 × 2 = 12, so 7 × 6 × 2 = <b>7 × 12</b> = 84. 7 × 8 adds 6 + 2, and 13 × 2 adds 7 + 6."))
    its.append(mcq("Which is true?", "9 × 4 = 4 × 9", ["9 − 4 = 4 − 9", "12 ÷ 4 = 4 ÷ 12", "9 × 4 = 9 + 4"],
                   "You can swap the numbers in a multiplication: 9 × 4 = 4 × 9 = 36. This does not work for − or ÷."))
    assert len(its) == 20, len(its)
    return {"title": "Multiply three numbers and change the order", "items": its}


# ------------------------------------------------------------ set 4: factor pairs
def set_factor_pairs(P):
    its = []
    for r, c in [(3, 8), (4, 9), (2, 9), (5, 6)]:
        t = r * c
        its.append(mcq(fig(array_svg(r, c)) + "%d counters are in %d equal rows. Find the missing factor: %d × <b>?</b> = %d"
                       % (t, r, r, t), c, [t - r, c + 1, c - 1, t + r],
                       "Count the counters in one row: <b>%d</b>. %d × %d = %d, so %d and %d are a factor pair of %d."
                       % (c, r, c, t, r, c, t)))
    for t, (a, b), wrong in [(36, (4, 9), [(16, 20), (4, 8), (6, 7)]), (40, (5, 8), [(20, 20), (5, 7), (6, 7)]),
                             (56, (7, 8), [(50, 6), (6, 9), (7, 9)])]:
        assert a * b == t and all(x * y != t for x, y in wrong) and sum(wrong[0]) == t
        its.append(mcq("Which is a factor pair of %d?" % t, "%d and %d" % (a, b), ["%d and %d" % w for w in wrong],
                       "%d × %d = <b>%d</b>. %d + %d also makes %d, but a factor pair must <b>multiply</b> to make %d."
                       % (a, b, t, wrong[0][0], wrong[0][1], t, t)))
    for t, bad, good in [(24, (6, 3), [(1, 24), (2, 12), (3, 8)]), (36, (8, 4), [(2, 18), (3, 12), (4, 9)]),
                         (48, (6, 9), [(6, 8), (4, 12), (3, 16)])]:
        assert bad[0] * bad[1] != t and all(x * y == t for x, y in good)
        its.append(mcq("Which is <b>not</b> a factor pair of %d?" % t, "%d and %d" % bad, ["%d and %d" % g for g in good],
                       "%d × %d = %d, not %d. The others are factor pairs: %s."
                       % (bad[0], bad[1], bad[0] * bad[1], t, ", ".join("%d × %d = %d" % (x, y, t) for x, y in good))))
    for t, shown, miss, near in [(24, [(1, 24), (2, 12), (4, 6)], (3, 8), (3, 7)),
                                 (30, [(1, 30), (2, 15), (5, 6)], (3, 10), (3, 9)),
                                 (36, [(1, 36), (2, 18), (3, 12), (6, 6)], (4, 9), (4, 8))]:
        assert sorted(shown + [miss]) == pairs(t) and near[0] * near[1] != t
        nm, he, his = P.next()
        rev = [(b, a) for a, b in shown if a != b]
        its.append(mcq("%s lists the factor pairs of %d: %s. Which pair did %s miss?"
                       % (nm, t, ", ".join("%d × %d" % p for p in shown), he),
                       "%d × %d" % miss, ["%d × %d" % rev[-1], "%d × %d" % near, "%d × %d" % rev[-2]],
                       "Test 1, 2, 3, 4 … in order. %d × %d = %d is missing. Swapping a pair (like %d × %d) does not make a new pair."
                       % (miss[0], miss[1], t, rev[-1][0], rev[-1][1])))
    for t in [18, 16]:
        k = len(pairs(t))
        sq = pairs(t)[-1][0] == pairs(t)[-1][1]
        its.append(mcq("How many factor pairs does %d have?" % t, k, [k - 1, len(factors(t)), k + 1],
                       "%s. That is <b>%d</b> pairs.%s" % (", ".join("%d × %d" % p for p in pairs(t)), k,
                                                         " Count 4 × 4 only once." if sq else " 1 × %d counts too." % t)))
    # factor pairs in mental calculations
    for q, split, step, v, cands in [
            ("12 × 5", "12 = 6 × 2", "6 × 2 × 5 = 6 × 10", 60, [30, 17, 600]),
            ("14 × 5", "14 = 7 × 2", "7 × 2 × 5 = 7 × 10", 70, [35, 19, 700]),
            ("15 × 6", "6 = 2 × 3", "15 × 2 × 3 = 30 × 3", 90, [45, 30, 21]),
            ("25 × 8", "8 = 4 × 2", "25 × 4 × 2 = 100 × 2", 200, [100, 33, n(2000)])]:
        a, b = [int(x) for x in q.split(" × ")]
        assert a * b == v
        its.append(mcq("Use the factor pair %s. What is %s?" % (split, q), n(v), cands,
                       "%s = %s = <b>%s</b>. Remember to use every factor." % (q, step, n(v))))
    its.append(mcq("Which calculation helps you work out 16 × 5?", "8 × 2 × 5", ["1 × 6 × 5", "8 × 8 × 5", "16 + 5"],
                   "8 × 2 = 16, so 16 × 5 = <b>8 × 2 × 5</b> = 8 × 10 = 80. Splitting 16 into its digits does not work: 1 × 6 = 6, not 16. "
                   "And 8 × 8 = 64, not 16."))
    assert len(its) == 20, len(its)
    return {"title": "Factor pairs in mental calculations", "items": its}


# ------------------------------------------------------------ set 5: word problems
def set_words(P):
    its = []

    def add(q, right, wrong, e):
        its.append(mcq(q, right, wrong, e))

    add("A box holds 10 packs of biscuits. Each pack has 8 biscuits. How many biscuits are in 3 boxes?",
        n(240), [80, 21, n(2400)],
        "3 × 10 × 8. Do 3 × 8 = 24 first, then 24 × 10 = <b>240</b> biscuits. 80 is only one box.")
    add("The school hall has 3 rows of 4 tables. Each table has 5 chairs. How many chairs are there?",
        60, [12, 20, 15],
        "3 × 4 = 12 tables. 12 × 5 = <b>60</b> chairs. 12 is the number of tables, not chairs.")
    nm, he, his = P.next()
    add("A pencil costs 30p. %s buys 8 pencils. How much does %s spend?" % (nm, he),
        money(240), ["24p", "£24.00", "38p"],
        "3 × 8 = 24, so 30p × 8 = 24 tens of pence = 240p = <b>£2.40</b>.")
    nm, he, his = P.next()
    add("In a game, every red card scores 0 points. %s picks 9 red cards. How many points does %s score?" % (nm, he),
        "0 points", ["9 points", "1 point", "90 points"],
        "9 × 0 = <b>0</b>. Nine lots of nothing is still nothing.")
    add("There are 28 pupils in Year 4. Each pupil gets 1 carton of milk. How many cartons are needed?",
        "28 cartons", ["1 carton", "29 cartons", "0 cartons"],
        "28 × 1 = <b>28</b> cartons. Multiplying by 1 keeps the number the same.")
    add("The school orders 7 boxes of pencils. Each box has 30 pencils. How many pencils is that?",
        210, [21, n(2100), 37],
        "7 × 3 = 21, so 7 × 30 = 21 tens = <b>210</b> pencils.")
    add("240 pupils go on a school trip. Each coach takes 40 pupils. How many coaches are needed?",
        "6 coaches", ["60 coaches", "200 coaches", "4 coaches"],
        "24 ÷ 4 = 6, so 240 ÷ 40 = <b>6</b> coaches. Check: 6 × 40 = 240.")
    add("A garden has 5 flower beds. Each bed has 4 rows of 6 plants. How many plants are there?",
        120, [24, 15, n(1200)],
        "4 × 6 = 24 plants in one bed. 24 × 5 = <b>120</b>. Or 4 × 5 = 20 first, then 20 × 6 = 120.")
    nm, he, his = P.next()
    add("%s puts 24 chairs in equal rows with none left over. Which number of rows will <b>not</b> work?" % nm,
        "5 rows", ["3 rows", "4 rows", "6 rows"],
        "5 is not a factor of 24: 5 × 4 = 20 and 5 × 5 = 25. The others work: 3 × 8, 4 × 6 and 6 × 4 all make 24.")
    nm, he, his = P.next()
    add("%s puts 36 cupcakes on a tray in equal rows. Which could the tray show?" % nm,
        "4 rows of 9", ["5 rows of 7", "6 rows of 7", "4 rows of 8"],
        "4 × 9 = <b>36</b>, a factor pair of 36. 5 × 7 = 35, 6 × 7 = 42 and 4 × 8 = 32.")
    add("Raffle tickets cost 5p each. 4 children each buy 7 tickets. How much do they spend altogether?",
        money(140), ["35p", "28p", "16p"],
        "4 × 7 × 5. Do 4 × 5 = 20 first, then 20 × 7 = 140p = <b>£1.40</b>. 28p forgets the cost of each ticket.")
    a1, a2 = P.next()[0], P.next()[0]
    add("%s has 7 bags of 9 sweets. %s has 9 bags of 7 sweets. Who has more sweets?" % (a1, a2),
        "Same: 63 each", [a1, a2, "Same: 16 each"],
        "7 × 9 = 63 and 9 × 7 = 63. Swapping the order does not change the answer. (16 comes from adding.)")
    add("A PE teacher puts 350 cones into 7 equal stacks. How many cones are in each stack?",
        50, [5, 500, 343],
        "35 ÷ 7 = 5, so 350 ÷ 7 = 5 tens = <b>50</b> cones. Check: 50 × 7 = 350.")
    nm, he, his = P.next()
    add("One lap of the field is 400 m. %s runs 3 laps. How far does %s run?" % (nm, he),
        "1,200 m", ["120 m", "12,000 m", "403 m"],
        "4 × 3 = 12, so 400 × 3 = 12 hundreds = <b>1,200 m</b>.")
    add("A tray holds 15 eggs. How many eggs are on 4 trays?",
        60, [30, 19, 600],
        "4 = 2 × 2, so 15 × 4 = 15 × 2 × 2 = 30 × 2 = <b>60</b> eggs. 30 is only 2 trays.")
    nm, he, his = P.next()
    add("%s saves 20p every day for 9 days. How much does %s save?" % (nm, he),
        money(180), ["18p", "£18.00", "29p"],
        "2 × 9 = 18, so 20p × 9 = 18 tens of pence = 180p = <b>£1.80</b>.")
    add("A packet of biscuits costs 25p. How much do 4 packets cost?",
        money(100), ["29p", "50p", "£10.00"],
        "25 × 4 = 25 × 2 × 2 = 50 × 2 = 100p = <b>£1.00</b>. 50p is only 2 packets.")
    add("A car park has 8 rows. Each row has 30 spaces. How many spaces are there?",
        240, [24, n(2400), 38],
        "8 × 3 = 24, so 8 × 30 = 24 tens = <b>240</b> spaces.")
    add("6 bags of crisps cost £3.60 altogether. Each bag costs the same. How much is one bag?",
        "60p", ["6p", "£6.00", "£3.54"],
        "£3.60 = 360p. 36 ÷ 6 = 6, so 360 ÷ 6 = 6 tens = <b>60p</b>. Check: 60p × 6 = 360p = £3.60.")
    nm, he, his = P.next()
    add("%s buys 2 packs of pens every week for 5 weeks. Each pack has 6 pens. How many pens does %s buy?" % (nm, he),
        60, [13, 12, 30],
        "2 × 6 × 5. Do 2 × 5 = 10 first, then 10 × 6 = <b>60</b> pens. 12 is only one week.")
    assert len(its) == 20, len(its)
    # money checks
    assert money(240) == "£2.40" and money(140) == "£1.40" and money(180) == "£1.80" and money(100) == "£1.00"
    return {"title": "Word problems: mental strategies", "items": its}


# ------------------------------------------------------------ lesson
def table(head, rows):
    h = "".join("<th>%s</th>" % x for x in head)
    b = "".join("<tr>" + "".join("<td>%s</td>" % c for c in r) + "</tr>" for r in rows)
    return "<div class='sn-tw'><table class='sn-table'><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>" % (h, b)


def ex(title, q, s, a):
    return ("<div class='sn-ex'><span class='sn-ex-t'>%s</span><p class='sn-ex-q'>%s</p>"
            "<p class='sn-ex-s'>%s</p><p class='sn-ex-a'>Answer: %s</p></div>" % (title, q, s, a))


def body_html():
    return (
        "<h2>Use facts you already know</h2>"
        "<p>You do not need a written method for every calculation. Use your times tables, place value and a few simple rules "
        "to work out harder facts in your head.</p>"
        "<h2>Multiply by 0 and 1, divide by 1</h2>" +
        table(["Rule", "Example", "Why"], [
            ["A number × 1 = the same number", "8 × 1 = 8", "One lot of 8 is 8"],
            ["A number × 0 = 0", "7 × 0 = 0", "Seven lots of nothing is nothing"],
            ["A number ÷ 1 = the same number", "9 ÷ 1 = 9", "Put all 9 in one group"],
        ]) +
        "<h2>Use place value: derived facts</h2>"
        "<p>× 10 moves every digit one place to the left. So if you know 6 × 7 = 42, you also know 60 × 7 = 420.</p>"
        "<figure class='sn-fig'>" + pv_svg(42, 420, "× 10") +
        "<figcaption>42 × 10 = 420. The 4 tens become 4 hundreds, the 2 ones become 2 tens, and a 0 holds the ones place."
        "</figcaption></figure>" +
        ex("Example", "Work out 60 × 7 and 420 ÷ 7.",
           "6 × 7 = 42. 60 is 6 tens, so 60 × 7 = 42 tens = 420. Use the inverse: 420 ÷ 7 = 6 tens = 60.", "420 and 60") +
        "<h2>Multiply three numbers</h2>"
        "<p>You can multiply in <b>any order</b>. Look for a pair that makes 10 or 20 first.</p>" +
        ex("Example", "Work out 2 × 7 × 5.", "Swap the order: 2 × 5 = 10. Then 10 × 7 = 70.", "70") +
        "<h2>Factor pairs</h2>"
        "<p>A <b>factor pair</b> is two numbers that multiply to make a number. 3 × 8 = 24, so 3 and 8 are a factor pair of 24. "
        "The factor pairs of 24 are 1 × 24, 2 × 12, 3 × 8 and 4 × 6.</p>"
        "<figure class='sn-fig'>" + array_svg(3, 8) +
        "<figcaption>24 counters in 3 rows of 8. 3 × 8 = 24.</figcaption></figure>" +
        ex("Example", "Work out 15 × 6 using a factor pair.", "6 = 2 × 3. So 15 × 6 = 15 × 2 × 3 = 30 × 3 = 90.", "90") +
        "<h2>Common mistakes</h2>" +
        table(["Mistake", "What to do instead"], [
            ["7 × 0 = 7", "Anything × 0 is 0"],
            ["8 ÷ 1 = 1", "Dividing by 1 keeps the number: 8 ÷ 1 = 8"],
            ["60 × 7 = 42 or 4,200", "60 is 6 tens, so the answer is 42 tens = 420"],
            ["2 × 7 × 5 = 35", "Use all three numbers: 2 × 5 = 10, then 10 × 7 = 70"],
            ["Missing a factor pair of 24", "Test 1, 2, 3, 4 … in order until the pairs meet"],
            ["Saying 8 + 16 = 24, so 8 and 16 are a factor pair", "A factor pair must multiply: 8 × 3 = 24"],
        ])
    )


FAQ = [
    {"q": "What are mental multiplication and division strategies in Year 4?",
     "a": "Pupils use times tables, place value and simple rules to calculate in their heads. For example, 6 × 7 = 42 tells you that 60 × 7 = 420, and 2 × 9 × 5 is easier as 2 × 5 = 10, then 10 × 9 = 90."},
    {"q": "What times tables should a Year 4 child know?",
     "a": "By the end of Year 4, the National Curriculum expects children to recall all multiplication and division facts up to 12 × 12."},
    {"q": "What is the Multiplication Tables Check?",
     "a": "It is a short online check taken in June of Year 4 in England. Children answer 25 times tables questions up to 12 × 12, with 6 seconds for each one."},
    {"q": "What is a factor pair?",
     "a": "Two numbers that multiply to make a given number. The factor pairs of 12 are 1 × 12, 2 × 6 and 3 × 4."},
]


def gen():
    rnd = random.Random(4406)
    P = People(rnd)
    sets = [set_zero_one(P), set_place_value(P), set_three(P), set_factor_pairs(P), set_words(P)]
    balance(sets, rnd)
    seen = set()
    for s in sets:
        assert len(s["items"]) == 20, (s["title"], len(s["items"]))
        assert sorted(it["a"] for it in s["items"]) == sorted([0, 1, 2, 3] * 5)
        for it in s["items"]:
            assert len(set(it["c"])) == 4, it
            k = it["q"] + "|" + "|".join(sorted(it["c"]))
            assert k not in seen, it["q"]
            seen.add(k)
    u = {
        "country": "uk", "subject": "maths", "grade": "year-4", "slug": "mental-multiplication-and-division", "sort": 6,
        "updated": UPDATED, "pdf_url": "",
        "title": "Mental Multiplication and Division",
        "seo_title": "Year 4 Mental Multiplication and Division Worksheets: × 0, × 1, Derived Facts and Factor Pairs",
        "short_title": "Mental multiplication and division",
        "domain": "Multiplication and division",
        "standard_code": "Year 4: Multiplication and division",
        "standard_url": "https://www.gov.uk/government/publications/national-curriculum-in-england-mathematics-programmes-of-study",
        "standard_text": "Use place value, known and derived facts to multiply and divide mentally, including: multiplying by 0 and 1; dividing by 1; multiplying together three numbers; recognise and use factor pairs and commutativity in mental calculations.",
        "meta_desc": "Free Year 4 maths worksheets on mental multiplication and division: multiplying by 0 and 1, dividing by 1, derived facts like 60 × 7, multiplying three numbers and factor pairs. 100 questions with an answer key, matched to the National Curriculum.",
        "key_big": "Use a fact you know to work out one you don’t: 6 × 7 = 42, so 60 × 7 = 420.",
        "key_sub": "Any number × 0 is 0. Any number × 1 or ÷ 1 stays the same. Multiply three numbers in any order, and use factor pairs to split a hard calculation.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }
    return mark_large(u, "place value chart")


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, "mental-multiplication-and-division.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(u, f, ensure_ascii=False, indent=1)
    print("wrote", path)
