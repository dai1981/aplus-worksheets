# -*- coding: utf-8 -*-
"""
Australia Year 5 Maths: Number Sentences with Multiplication and Division
(Australian Curriculum v9.0, AC9M5A02, with AC9M5A01 inverse operations and fact families)
  python3 tools/gen_au_maths_y5_number_sentences.py
Fact families, unknowns in multiplication and division (? × 8 = 56, 96 ÷ ? = 8, ? ÷ 4 = 12),
properties (commutative, associative, distributive), the equals sign as a balance (3 × 8 = 4 × ?)
and word problems written as number sentences.
Wrong choices come from real mistakes: using the same operation instead of the inverse
(? × 8 = 56 -> 448, ? ÷ 4 = 12 -> 3), subtracting or adding the two numbers, copying a number,
a times-table slip, dropping or adding a zero, distributive slips (7 × 16 = 70 + 6),
reading = as “the answer is” (3 × 8 = 4 × ? -> 24) and adding instead of multiplying on a balance
(3 + 8 = 4 + 7). Every answer is checked in code. HTML attributes use single quotes. Australian English.
"""
import json, os, random, re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "au", "maths", "year-5")
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


# ------------------------------------------------------------ helpers
def mcq(q, correct, wrongs, e):
    correct = n(correct) if isinstance(correct, int) else correct
    ch = [correct]
    for w in wrongs:
        if isinstance(w, int):
            assert w > 0, (q, w)
            w = n(w)
        if w not in ch:
            ch.append(w)
    assert len(ch) == 4, (q, ch)
    return {"q": q, "c": ch, "a": 0, "e": e}


def balance(sets, rnd):
    """Spread the correct answers evenly over the 4 positions in every set."""
    for s in sets:
        targets = [0, 1, 2, 3] * 5
        rnd.shuffle(targets)
        for it, t in zip(s["items"], targets):
            c = it["c"]
            wrong = [x for i, x in enumerate(c) if i != it["a"]]
            rnd.shuffle(wrong)
            it["c"] = wrong[:t] + [c[it["a"]]] + wrong[t:]
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
    w, h = int(w), int(h)
    return ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 %d %d' width='%d' height='%d' "
            "role='img' aria-label='%s'><g font-family='%s'>%s</g></svg>" % (w, h, w, h, label, FONT, body))


def tw(t, fs):
    return len(str(t)) * fs * 0.6


def text(x, y, t, fs=18, col=INK, anchor="middle"):
    return ("<text x='%.1f' y='%.1f' font-size='%d' font-weight='700' fill='%s' text-anchor='%s'>%s</text>"
            % (x, y, fs, col, anchor, t))


def triangle_svg(top, left, right):
    """Fact family triangle: the product at the top, the two factors at the bottom. None = '?'."""
    pts = [(90, 26, top), (28, 122, left), (152, 122, right)]
    s = ["<path d='M90 26 L28 122 L152 122 Z' fill='%s' stroke='%s' stroke-width='3' stroke-linejoin='round'/>" % (FILL, GREEN)]
    for x, y, v in pts:
        s.append("<circle cx='%d' cy='%d' r='23' fill='#fff' stroke='%s' stroke-width='2.5'/>" % (x, y, GREEN))
        s.append(text(x, y + 7, "?" if v is None else v, 20, RED if v is None else INK))
    s.append(text(90, 100, "× ÷", 18, GREEN))
    lab = "fact family triangle: %s at the top, %s and %s at the bottom" % tuple("?" if v is None else v for v in (top, left, right))
    return svg_wrap(180, 150, "".join(s), lab)


def bar_svg(k, part, total):
    """Bar model: k equal parts, each labelled part, with total above. '?' is drawn in red."""
    cw = 46 if k <= 5 else 40
    x0, y = 8, 40
    s = []
    for i in range(k):
        s.append("<rect x='%d' y='%d' width='%d' height='36' fill='%s' stroke='%s' stroke-width='2.5'/>"
                 % (x0 + i * cw, y, cw, FILL, GREEN))
        s.append(text(x0 + i * cw + cw / 2, y + 25, part, 18, RED if part == "?" else INK))
    x1 = x0 + k * cw
    s.append("<path d='M%d %d v-8 H%d v8' fill='none' stroke='%s' stroke-width='2'/>" % (x0, y - 4, x1, INK))
    s.append(text((x0 + x1) / 2, y - 18, total, 18, RED if total == "?" else INK))
    return svg_wrap(x1 + 8, y + 44, "".join(s), "bar model: %d equal parts of %s make %s" % (k, part, total))


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


def array_svg(rows, cols, s=20):
    body = "".join("<circle cx='%d' cy='%d' r='7' fill='%s'/>" % (6 + c * s + s // 2, 6 + j * s + s // 2, GREEN)
                   for j in range(rows) for c in range(cols))
    return svg_wrap(cols * s + 12, rows * s + 12, body, "array of counters in %d rows of %d" % (rows, cols))


def mark_large(u, pattern):
    rx = re.compile(r"<svg (?=[^>]*aria-label='(?:" + pattern + "))")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u


# ============================================================ set 1: fact families
def set_families():
    its = []
    # use a known multiplication fact to divide
    for a, b in [(8, 12), (9, 7), (6, 11), (12, 4)]:
        p = a * b
        e = ("Division undoes multiplication. %s, so %s. Not %s: that multiplies again instead of using the inverse."
             % (plain(a, "×", b, "=", p), plain(p, "÷", a, "=", "<b>%d</b>" % b), n(p * a)))
        its.append(mcq("You know %s. What is %s?" % (plain(a, "×", b, "=", p), plain(p, "÷", a)),
                       b, [a, p - a, p * a], e))
    # which division fact belongs
    for a, b in [(6, 7), (9, 8), (7, 12), (11, 6)]:
        p = a * b
        e = ("A fact family uses the same three numbers. In a division fact, the biggest number (%d) is divided: "
             "%s and %s." % (p, plain(p, "÷", a, "=", b), plain(p, "÷", b, "=", a)))
        its.append(mcq("%s. Which division fact is in the same fact family?" % plain(a, "×", b, "=", p),
                       plain(p, "÷", a, "=", b),
                       [plain(a, "÷", p, "=", b), plain(b, "÷", a, "=", p), plain(p, "−", a, "=", p - a)], e))
    # which multiplication fact belongs
    for p, a, b in [(108, 9, 12), (56, 7, 8), (66, 6, 11), (45, 5, 9)]:
        assert a * b == p
        e = ("Multiplication is the inverse of division. %s, so %s. "
             "%s is true, but it uses %d × %d, not the two smaller numbers."
             % (plain(p, "÷", a, "=", b), plain(b, "×", a, "=", p), plain(p, "×", a, "=", p * a), p, a))
        its.append(mcq("Which number sentence is in the same fact family as %s?" % plain(p, "÷", a, "=", b),
                       plain(b, "×", a, "=", p),
                       [plain(p, "×", a, "=", p * a), plain(p, "×", b, "=", p * b), plain(p, "−", a, "=", p - a)], e))
    # fact family triangles
    tri = [
        (None, 6, 8, 48, [14, 42, 56],
         "The top number is the product: 6 × 8 = <b>48</b>. Not 14: that adds 6 and 8."),
        (63, 7, None, 9, [56, 441, 70],
         "7 × ? = 63. Use the inverse: 63 ÷ 7 = <b>9</b>. Check: 7 × 9 = 63. Not 56: that subtracts 7 from 63."),
        (60, None, 5, 12, [55, 300, 65],
         "? × 5 = 60. Use the inverse: 60 ÷ 5 = <b>12</b>. Check: 12 × 5 = 60. Not 300: that multiplies instead of dividing."),
        (None, 11, 4, 44, [15, 40, 48],
         "The top number is the product: 11 × 4 = <b>44</b>. Not 15: that adds 11 and 4."),
    ]
    for top, l, r, ans, wr, e in tri:
        vals = [top or ans, l or ans, r or ans]
        assert vals[1] * vals[2] == vals[0]
        its.append(mcq("The three numbers in this triangle make a fact family. What is the missing number?"
                       + fig(triangle_svg(top, l, r)), ans, wr, e))
    # which is NOT in the family
    notin = [
        (7, 8, 56, plain(8, "÷", 56, "=", 7), "the big number must be divided: 56 ÷ 8 = 7"),
        (6, 9, 54, plain(54, "×", 6, "=", 9), "54 × 6 is not 9. The fact is 54 ÷ 6 = 9"),
        (4, 12, 48, plain(12, "÷", 4, "=", 48), "12 ÷ 4 is 3, not 48. The fact is 48 ÷ 4 = 12"),
        (3, 11, 33, plain(11, "÷", 3, "=", 33), "the big number must be divided: 33 ÷ 3 = 11"),
    ]
    for i, (a, b, p, bad, why) in enumerate(notin):
        fam = [plain(a, "×", b, "=", p), plain(b, "×", a, "=", p), plain(p, "÷", a, "=", b), plain(p, "÷", b, "=", a)]
        good = [fam[j] for j in range(4) if j != i]
        e = "The fact family of %d, %d and %d is %s. <b>%s</b> is not in it: %s." % (a, b, p, ", ".join(fam), bad, why)
        its.append(mcq("Which number sentence is <b>not</b> in the fact family of %d, %d and %d?" % (a, b, p), bad, good, e))
    assert len(its) == 20
    return {"title": "Fact families", "items": its}


# ============================================================ set 2: unknowns in multiplication
def mult_e(eq, a, p, ans, wrong, why):
    return ("%s. Use the inverse: ? = %s = <b>%s</b>. Check: %s. Not %s: %s."
            % (eq, plain(p, "÷", a), n(ans), plain(ans, "×", a, "=", p), n(wrong), why))


def set_mult():
    its = []
    for a, p in [(8, 56), (6, 48), (12, 84), (7, 63), (11, 66)]:
        ans = p // a
        assert ans * a == p and ans != a
        e = mult_e(sent("?", "×", a, "=", p), a, p, ans, p * a, "that multiplies instead of dividing")
        its.append(mcq("%s<br>What is the missing number?" % sent("?", "×", a, "=", p), ans, [p - a, p * a, a], e))
    for a, p in [(9, 108), (4, 44), (12, 96), (6, 72)]:
        ans = p // a
        assert ans * a == p and ans != a
        e = mult_e(sent(a, "×", "?", "=", p), a, p, ans, p - a, "that subtracts instead of dividing")
        its.append(mcq("%s<br>What is the missing number?" % sent(a, "×", "?", "=", p), ans, [p - a, p * a, a], e))
    for p, left, a in [(72, True, 9), (60, False, 5), (77, False, 7)]:
        ans = p // a
        assert ans * a == p
        eq = sent(p, "=", "?", "×", a) if left else sent(p, "=", a, "×", "?")
        e = ("The = sign can come first. It means both sides are the same. " +
             mult_e(eq, a, p, ans, p * a, "that multiplies instead of dividing"))
        its.append(mcq("%s<br>What is the missing number?" % eq, ans, [p - a, p * a, a], e))
    tens = [
        (sent(6, "×", "?", "=", 240), 6, 240, 40, [4, 400, 234], "6 × 4 = 24, so 6 × 40 = 240", "6 × 4 = 24, not 240, so a zero is missing"),
        (sent("?", "×", 30, "=", 210), 30, 210, 7, [70, 180, 6300], "3 × 7 = 21, so 30 × 7 = 210", "70 × 30 = 2100, one zero too many"),
        (sent(50, "×", "?", "=", 400), 50, 400, 8, [80, 350, 20000], "5 × 8 = 40, so 50 × 8 = 400", "80 × 50 = 4000, one zero too many"),
        (sent("?", "×", 4, "=", 280), 4, 280, 70, [7, 700, 276], "7 × 4 = 28, so 70 × 4 = 280", "7 × 4 = 28, not 280, so a zero is missing"),
    ]
    for eq, a, p, ans, wr, fact, why in tens:
        assert ans * a == p
        e = "Use a times table fact: %s. Check: %s. Not %s: %s." % (fact, plain(ans, "×", a, "=", p), n(wr[0]), why)
        its.append(mcq("%s<br>What is the missing number?" % eq, ans, wr, e))
    for k, p in [(5, 35), (4, 36), (6, 42), (3, 24)]:
        ans = p // k
        assert ans * k == p and ans != k
        e = ("%d equal parts make %d, so %s. Use the inverse: ? = %s = <b>%d</b>. Not %d: that subtracts instead of dividing."
             % (k, p, sent(k, "×", "?", "=", p), plain(p, "÷", k), ans, p - k))
        its.append(mcq("The bar model shows %d equal parts that make %d. What number goes in each part?" % (k, p)
                       + fig(bar_svg(k, "?", str(p))), ans, [p - k, p * k, k], e))
    assert len(its) == 20
    return {"title": "Unknowns in multiplication", "items": its}


# ============================================================ set 3: unknowns in division
def div_wrongs(a, q):
    """? ÷ a = q: dividing again, adding, subtracting, then a times-table slip."""
    c = []
    if q % a == 0:
        c.append(q // a)
    c += [q + a]
    if q - a > 0:
        c.append(q - a)
    c.append(a * (q + 1))
    return c[:3]


def dividend_item(a, q, left=False):
    ans = a * q
    assert ans // a == q
    eq = sent(q, "=", "?", "÷", a) if left else sent("?", "÷", a, "=", q)
    wr = div_wrongs(a, q)
    first = ("that divides again (%s), the same operation, not the inverse" % plain(q, "÷", a)) if q % a == 0 \
        else "that adds the two numbers"
    e = ("%s%s. The unknown is the number you start with. Use the inverse: ? = %s = <b>%s</b>. Check: %s. Not %s: %s."
         % ("The = sign can come first. " if left else "", eq, plain(q, "×", a), n(ans), plain(ans, "÷", a, "=", q), n(wr[0]), first))
    return mcq("%s<br>What is the missing number?" % eq, ans, wr, e)


def divisor_item(p, q, left=False):
    ans = p // q
    assert ans * q == p
    eq = sent(q, "=", p, "÷", "?") if left else sent(p, "÷", "?", "=", q)
    e = ("%s%s. Ask: %d shared into how many groups gives %d in each? ? = %s = <b>%d</b>. Check: %s. "
         "Not %s: multiplying %d by %d does not undo this."
         % ("The = sign can come first. " if left else "", eq, p, q, plain(p, "÷", q), ans, plain(p, "÷", ans, "=", q),
            n(p * q), p, q))
    return mcq("%s<br>What is the missing number?" % eq, ans, [p * q, p - q, p + q], e)


def set_div():
    its = []
    for a, q in [(4, 12), (6, 9), (7, 11), (3, 12), (5, 10)]:
        its.append(dividend_item(a, q))
    for p, q in [(96, 8), (63, 9), (132, 11), (72, 8), (66, 6)]:
        its.append(divisor_item(p, q))
    its.append(dividend_item(5, 7, left=True))
    its.append(divisor_item(48, 6, left=True))
    its.append(dividend_item(4, 11, left=True))
    for k, part in [(3, 15), (5, 13), (4, 24)]:
        tot = k * part
        wr = div_wrongs(k, part)
        e = ("The bar shows %s. Put the %d parts together: ? = %s = <b>%d</b>. Not %s."
             % (sent("?", "÷", k, "=", part), k, plain(part, "×", k), tot,
                ("%d: that divides %d by %d instead of multiplying" % (wr[0], part, k)) if part % k == 0
                else "%d: that adds %d and %d" % (wr[0], part, k)))
        its.append(mcq("The bar model shows %s. There are %d equal parts of %d. What is the total?"
                       % (sent("?", "÷", k, "=", part), k, part) + fig(bar_svg(k, str(part), "?")), tot, wr, e))
    big = [
        (sent("?", "÷", 5, "=", 20), 100, [4, 25, 15], "? = 20 × 5 = <b>100</b>. Check: 100 ÷ 5 = 20. Not 4: that divides 20 by 5 again"),
        (sent(360, "÷", "?", "=", 9), 40, [4, 3240, 351],
         "36 ÷ 9 = 4, so 360 ÷ 9 = <b>40</b>. Check: 360 ÷ 40 = 9. Not 4: a zero is missing"),
        (sent("?", "÷", 10, "=", 45), 450, [55, 35, 4500],
         "? = 45 × 10 = <b>450</b>. Check: 450 ÷ 10 = 45. Not 4500: × 10 adds one zero, not two"),
        (sent(240, "÷", "?", "=", 6), 40, [4, 1440, 234],
         "24 ÷ 6 = 4, so 240 ÷ 6 = <b>40</b>. Check: 240 ÷ 40 = 6. Not 1440: that multiplies 240 by 6"),
    ]
    assert 100 // 5 == 20 and 360 // 40 == 9 and 450 // 10 == 45 and 240 // 40 == 6
    for eq, ans, wr, e in big:
        its.append(mcq("%s<br>What is the missing number?" % eq, ans, wr, e + "."))
    assert len(its) == 20
    return {"title": "Unknowns in division", "items": its}


# ============================================================ set 4: properties and balance
def set_props():
    its = []
    # commutative
    e = "You can multiply in any order: 7 × 9 = 9 × 7. So ? = <b>7</b>. Not 63: both sides must be equal, so ? is not the answer to 7 × 9."
    its.append(mcq(sent(7, "×", 9, "=", 9, "×", "?") + "<br>What is the missing number?", 7, [63, 9, 567], e))
    e = "Turn-around facts: 12 × 5 = 5 × 12. So ? = <b>5</b>. Not 60: = means “the same as”, not “the answer is”."
    its.append(mcq(sent(12, "×", 5, "=", "?", "×", 12) + "<br>What is the missing number?", 5, [60, 12, 17], e))
    e = ("Multiplication can be done in any order, so 5 × 9 = 9 × 5 is <b>true</b>. Division cannot: 20 ÷ 4 = 5 but 4 ÷ 20 is less than 1. "
         "7 × 3 = 21, not 10. 6 × 4 = 24, not 144.")
    its.append(mcq("Which number sentence is true?", "5 × 9 = 9 × 5", ["20 ÷ 4 = 4 ÷ 20", "7 × 3 = 7 + 3", "6 × 4 = 24 × 6"], e))
    # associative
    assert 5 * 17 * 2 == 170 and 4 * 13 * 25 == 1300 and 2 * 36 * 5 == 36 * 10
    e = "Multiply 5 × 2 first: 5 × 2 = 10. Then 10 × 17 = <b>170</b>. Not 85: that forgets the × 2."
    its.append(mcq("Work out " + sent(5, "×", 17, "×", 2) + ". Hint: multiply the 5 and the 2 first.", 170, [85, 1700, 24], e))
    e = "Multiply 4 × 25 first: 4 × 25 = 100. Then 100 × 13 = <b>1300</b>. Not 325: that forgets the × 4."
    its.append(mcq("Work out " + sent(4, "×", 13, "×", 25) + ". Hint: multiply the 4 and the 25 first.", 1300, [325, 13000, 42], e))
    e = "2 × 5 = 10, so 2 × 36 × 5 = 36 × 10. ? = <b>10</b>. Not 7: you multiply 2 and 5, you do not add them."
    its.append(mcq(sent(2, "×", 36, "×", 5, "=", 36, "×", "?") + "<br>What is the missing number?", 10, [7, 72, 360], e))
    # distributive
    assert 6 * 14 == 60 + 24 and 7 * 16 == 70 + 42 and 8 * 23 == 160 + 24 and 5 * 17 == 50 + 35
    e = "Split 14 into 10 + 4. 6 × 14 = 6 × 10 + 6 × 4, so ? = <b>4</b>. Not 14: only the 4 ones are left after the 10."
    its.append(mcq(sent(6, "×", 14, "=", 6, "×", 10, "+", 6, "×", "?") + "<br>What is the missing number?", 4, [14, 24, 10], e))
    e = "Split 16 into 10 + 6. 7 × 16 = 7 × 10 + 7 × 6 = 70 + 42, so ? = <b>42</b>. Not 6: the 6 must be multiplied by 7 too."
    its.append(mcq(sent(7, "×", 16, "=", 70, "+", "?") + "<br>What is the missing number?", 42, [6, 16, 112], e))
    e = "Split 23 into 20 + 3. 8 × 23 = 8 × 20 + 8 × 3, so ? = <b>3</b>. Not 24: that is 8 × 3, but ? is the number that 8 multiplies."
    its.append(mcq(sent(8, "×", 23, "=", 8, "×", 20, "+", 8, "×", "?") + "<br>What is the missing number?", 3, [23, 24, 20], e))
    e = "Split 17 into 10 + 7. 5 × 17 = 5 × 10 + 5 × 7 = 50 + 35, so ? = <b>35</b>. Not 7: the 7 must be multiplied by 5 too."
    its.append(mcq(sent(5, "×", 17, "=", 5, "×", 10, "+", "?") + "<br>What is the missing number?", 35, [7, 17, 85], e))
    assert 6 * 18 == 108 and 3 * 26 == 78 and 9 * 19 == 180 - 9
    e = "6 × 18 = 6 × 10 + 6 × 8 = 60 + 48 = <b>108</b>. Not 68: that is 60 + 8, which forgets to multiply the 8 by 6."
    its.append(mcq("Split 18 into 10 + 8 to work out " + sent(6, "×", 18) + ".", 108, [68, 54, 114], e))
    e = "3 × 26 = 3 × 20 + 3 × 6 = 60 + 18 = <b>78</b>. Not 66: that is 60 + 6, which forgets to multiply the 6 by 3."
    its.append(mcq("Split 26 into 20 + 6 to work out " + sent(3, "×", 26) + ".", 78, [66, 24, 81], e))
    e = ("19 is 1 less than 20. 9 × 19 = 9 × 20 − 9 × 1 = 180 − 9, so ? = <b>9</b>. "
         "Not 1: take away one group of 9, not just 1. 9 × 19 = 171.")
    its.append(mcq(sent(9, "×", 19, "=", 9, "×", 20, "−", "?") + "<br>What is the missing number?", 9, [1, 19, 180], e))
    # balance
    pans = [(3, 8, 4, True), (2, 12, 8, True), (6, 6, 9, True), (5, 8, 10, False), (4, 9, 12, False)]
    for a, b, c, pic in pans:
        p = a * b
        ans = p // c
        add = a + b - c
        assert ans * c == p and add > 0 and add != ans
        e = ("= means both sides have the same value. The left side is %s, so %s. Use the inverse: ? = %s = <b>%d</b>. "
             "Not %d: that is the value of the left side, not the missing number."
             % (plain(a, "×", b, "=", p), sent(c, "×", "?", "=", p), plain(p, "÷", c), ans, p))
        q = sent(a, "×", b, "=", c, "×", "?")
        if pic:
            q = "The pans balance, so " + q + ". What is the missing number?" + fig(pan_svg(plain(a, "×", b), plain(c, "×", "?")))
        else:
            q += "<br>What is the missing number?"
        its.append(mcq(q, ans, [p, add, p * c], e))
    assert 36 // 4 == 18 // 2
    e = ("36 ÷ 4 = 9, so ? ÷ 2 = 9. Use the inverse: ? = 9 × 2 = <b>18</b>. "
         "Not 9: that is the value of the left side. Not 34: the two sides are divisions, not subtractions.")
    its.append(mcq(sent(36, "÷", 4, "=", "?", "÷", 2) + "<br>What is the missing number?", 18, [9, 34, 72], e))
    assert 5 * 6 == 10 * 3 and 5 * 6 != 30 * 2 and 5 * 6 != 4 * 7 and 5 * 6 != 15 * 3
    e = ("Work out both sides. 5 × 6 = 30 and 10 × 3 = 30, so <b>5 × 6 = 10 × 3</b> is true. "
         "30 × 2 = 60, 4 × 7 = 28 and 15 × 3 = 45.")
    its.append(mcq("Work out both sides. Which number sentence is true?", "5 × 6 = 10 × 3", ["5 × 6 = 30 × 2", "5 × 6 = 4 × 7", "5 × 6 = 15 × 3"], e))
    assert len(its) == 20
    return {"title": "Properties and the equals sign", "items": its}


# ============================================================ set 5: word problems
def set_words(P):
    its = []

    def solve(q, sentence, ans, wr, fmt, e):
        f = (lambda v: "$" + n(v)) if fmt == "$" else (lambda v: n(v))
        its.append(mcq(q, f(ans), [f(w) for w in wr], "Number sentence: %s. %s" % (sentence, e)))

    # 1 match
    nm, he, his = P.next()
    e = ("72 sausages are shared equally into 9 groups, so divide: <b>72 ÷ 9 = ?</b> (? = 8). "
         "9 ÷ 72 is the wrong way round: the total comes first.")
    its.append(mcq("%s puts 72 sausages onto 9 trays for the sausage sizzle, with the same number on each tray. "
                   "Which number sentence shows how many sausages go on each tray?" % nm,
                   sent(72, "÷", 9, "=", "?"), [sent(72, "×", 9, "=", "?"), sent(9, "÷", 72, "=", "?"), sent(72, "−", 9, "=", "?")], e))
    # 2 solve
    nm, he, his = P.next()
    assert 54 // 6 == 9
    solve("%s buys 6 packets of stickers. Each packet has the same number of stickers. %s gets 54 stickers altogether. "
          "How many stickers are in each packet?" % (nm, cap(he)), sent(6, "×", "?", "=", 54), 9, [48, 324, 60], "",
          "Use the inverse: ? = 54 ÷ 6 = <b>9</b>. Check: 6 × 9 = 54. Not 48: that subtracts 6 from 54.")
    # 3 match
    nm, he, his = P.next()
    e = ("You do not know how many pencils there are in total, so the total is ?: <b>? ÷ 6 = 9</b>. Then ? = 9 × 6 = 54 pencils.")
    its.append(mcq("A teacher shares some pencils equally among 6 tables. Each table gets 9 pencils. "
                   "Which number sentence matches the story?",
                   sent("?", "÷", 6, "=", 9), [sent(9, "÷", 6, "=", "?"), sent(6, "÷", 9, "=", "?"), sent("?", "−", 6, "=", 9)], e))
    # 4 solve
    assert 96 // 12 == 8
    solve("Eggs come in boxes of 12. The school canteen uses 96 eggs in a week. How many boxes of eggs is that?",
          sent("?", "×", 12, "=", 96), 8, [84, 108, 1152], "",
          "Use the inverse: ? = 96 ÷ 12 = <b>8</b> boxes. Check: 8 × 12 = 96. Not 1152: that multiplies instead of dividing.")
    # 5 match
    nm, he, his = P.next()
    e = ("%s has ? packs of 8 cards and 64 cards in total: <b>? × 8 = 64</b>. Then ? = 64 ÷ 8 = 8 packs." % nm)
    its.append(mcq("%s has some packs of footy cards. Each pack has 8 cards. %s has 64 cards altogether. "
                   "Which number sentence shows the number of packs?" % (nm, cap(he)),
                   sent("?", "×", 8, "=", 64), [sent(64, "×", 8, "=", "?"), sent("?", "+", 8, "=", 64), sent(8, "÷", 64, "=", "?")], e))
    # 6 solve
    nm, he, his = P.next()
    assert 84 // 7 == 12
    solve("%s shares 84 koala stickers equally among some friends. Each friend gets 7 stickers. How many friends are there?" % nm,
          sent(84, "÷", "?", "=", 7), 12, [77, 91, 588], "",
          "? = 84 ÷ 7 = <b>12</b> friends. Check: 84 ÷ 12 = 7. Not 77: that subtracts 7 from 84.")
    # 7 solve money
    assert 108 // 9 == 12
    solve("Tickets to the aquarium cost $9 each. A group pays $108. How many tickets do they buy?",
          sent(9, "×", "?", "=", 108), 12, [99, 117, 972], "",
          "Use the inverse: ? = 108 ÷ 9 = <b>12</b> tickets. Check: 9 × 12 = 108. Not 972: that multiplies instead of dividing.")
    # 8 match
    nm, he, his = P.next()
    e = ("Each day is the same distance, ?, and 5 days make 35 km: <b>5 × ? = 35</b>. Then ? = 35 ÷ 5 = 7 km. "
         "? ÷ 5 = 35 would mean 35 km each day.")
    its.append(mcq("%s runs the same distance every day for 5 days to train for the cross-country. %s runs 35 km in total. "
                   "Which number sentence shows how far %s runs each day?" % (nm, cap(he), he),
                   sent(5, "×", "?", "=", 35), [sent(35, "×", 5, "=", "?"), sent(5, "+", "?", "=", 35), sent("?", "÷", 5, "=", 35)], e))
    # 9 solve dividend unknown
    assert 8 * 7 == 56
    solve("At the athletics carnival, the Year 5 students are split into 8 teams of 7. How many Year 5 students are there?",
          sent("?", "÷", 8, "=", 7), 56, [15, 1, 64], "",
          "Use the inverse: ? = 7 × 8 = <b>56</b> students. Check: 56 ÷ 8 = 7. Not 15: that adds 8 and 7.")
    # 10 solve money
    nm, he, his = P.next()
    assert 72 // 6 == 12
    solve("%s saves the same amount of money each week. After 6 weeks %s has saved $72. How much does %s save each week?" % (nm, he, he),
          sent(6, "×", "?", "=", 72), 12, [66, 78, 432], "$",
          "Use the inverse: ? = 72 ÷ 6 = <b>$12</b>. Check: 6 × $12 = $72. Not $66: that subtracts 6 from 72.")
    # 11 match balance
    nm, he, his = P.next()
    e = ("Both ways use the same number of desks, so the two sides are equal: <b>4 × 7 = 2 × ?</b>. "
         "Then 28 = 2 × ?, so ? = 14 desks in each long row.")
    its.append(mcq("%s’s classroom has 4 rows of 7 desks. The class moves the same desks into 2 long rows of equal length. "
                   "Which number sentence matches?" % nm,
                   sent(4, "×", 7, "=", 2, "×", "?"), [sent(4, "+", 7, "=", 2, "+", "?"), sent(4, "×", 7, "=", 28, "×", 2),
                                                   sent(4, "×", 2, "=", 7, "×", "?")], e))
    # 12 solve swimming carnival
    assert 120 // 8 == 15
    solve("At the swimming carnival, 120 students swim in heats of 8. How many heats are there?",
          sent(120, "÷", 8, "=", "?"), 15, [112, 960, 16], "",
          "120 = 80 + 40, so 120 ÷ 8 = 10 + 5 = <b>15</b> heats. Check: 15 × 8 = 120. Not 112: that subtracts 8 from 120.")
    # 13 match check
    nm, he, his = P.next()
    e = ("Check a division with the inverse, multiplication: 12 × 7 = 84, so <b>12 × 7 = 84</b> shows 84 ÷ 7 = 12 is right. "
         "84 × 7 = 588 is true, but it does not check the division.")
    its.append(mcq("%s works out that 84 ÷ 7 = 12. Which number sentence can %s use to check %s answer?" % (nm, he, his),
                   "12 × 7 = 84", ["84 × 7 = 588", "84 − 7 = 77", "12 + 7 = 19"], e))
    # 14 solve balance story
    (n1, h1, s1), (n2, h2, s2) = P.next(), P.next()
    assert 4 * 6 == 3 * 8
    solve("%s has 4 bags with 6 marbles in each. %s has 3 bags with the same number in each, and the same number of marbles "
          "as %s altogether. How many marbles are in each of %s’s bags?" % (n1, n2, n1, n2),
          sent(4, "×", 6, "=", 3, "×", "?"), 8, [24, 7, 72], "",
          "4 × 6 = 24, so 3 × ? = 24. ? = 24 ÷ 3 = <b>8</b>. Not 24: that is the total, not the number in each bag.")
    # 15 solve distributive
    assert 6 * 15 == 90
    solve("The school buys 6 boxes of tennis balls. Each box has 15 balls. How many balls is that?",
          sent(6, "×", 15, "=", "?"), 90, [65, 36, 96], "",
          "Split 15 into 10 + 5: 6 × 10 + 6 × 5 = 60 + 30 = <b>90</b>. Not 65: that is 60 + 5, which forgets to multiply the 5 by 6.")
    # 16 match equals as answer
    nm, he, his = P.next()
    e = ("= means both sides are the same. 6 × 7 is 42, but 42 + 3 is 45, so “6 × 7 = 42 + 3” is <b>not true</b>. "
         "%s should write two number sentences: 6 × 7 = 42 and 42 + 3 = 45." % nm)
    its.append(mcq("%s works out 6 × 7 and then adds 3. %s writes: 6 × 7 = 42 + 3 = 45. What is wrong?" % (nm, cap(he)),
                   "6 × 7 is not equal to 42 + 3",
                   ["6 × 7 is not 42", "Nothing is wrong", "It should be 42 − 3"], e))
    # 17 solve fact family
    nm, he, his = P.next()
    assert 9 * 8 == 72
    solve("%s knows that 9 × 8 = 72. On a school excursion, 72 students are put into 8 equal groups. How many students are in each group?" % nm,
          sent(72, "÷", 8, "=", "?"), 9, [8, 64, 576], "",
          "It is in the same fact family as 9 × 8 = 72, so 72 ÷ 8 = <b>9</b>. Not 64: that subtracts 8 from 72.")
    # 18 solve two-digit
    assert 4 * 48 == 192
    solve("4 buses each carry 48 students to the museum. How many students is that altogether?",
          sent(4, "×", 48, "=", "?"), 192, [168, 52, 196], "",
          "4 × 40 + 4 × 8 = 160 + 32 = <b>192</b>. Not 168: that is 160 + 8, which forgets to multiply the 8 by 4.")
    # 19 match division divisor unknown
    nm, he, his = P.next()
    e = ("The total ($96) and the price of each netball are known, but the number of netballs is not. 96 ÷ ? = 8 means "
         "“$96 shared into how many groups of $8?”: <b>96 ÷ ? = 8</b>. Then ? = 12 netballs.")
    its.append(mcq("A netball club spends $96 on new netballs. Each netball costs $8. Which number sentence shows how many netballs they buy?",
                   sent(96, "÷", "?", "=", 8), [sent(96, "×", 8, "=", "?"), sent(8, "÷", 96, "=", "?"), sent("?", "÷", 8, "=", 96)], e))
    # 20 solve two steps with tens
    assert 3 * 40 == 120 and 120 // 4 == 30
    solve("A carton holds 40 packets of muesli bars. The school canteen orders 3 cartons. How many packets is that?",
          sent(3, "×", 40, "=", "?"), 120, [12, 1200, 43], "",
          "3 × 4 = 12, so 3 × 40 = <b>120</b> packets. Not 12: a zero is missing. Not 1200: one zero too many.")
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
        "<h2>Multiplication and division are inverses</h2>"
        "<p>Division undoes multiplication, and multiplication undoes division. "
        "So three numbers like 6, 7 and 42 make a <b>fact family</b> of four facts.</p>"
        "<figure class='sn-fig'>" + array_svg(6, 7) +
        "<figcaption>6 rows of 7 counters: 6 × 7 = 42, 7 × 6 = 42, 42 ÷ 6 = 7 and 42 ÷ 7 = 6.</figcaption></figure>" +
        table(["Multiplication", "Division"], [["6 × 7 = 42", "42 ÷ 6 = 7"], ["7 × 6 = 42", "42 ÷ 7 = 6"]]) +
        "<p>In a division fact the biggest number, the total, always comes first.</p>"
        "<h2>Find the unknown: use the inverse</h2>"
        "<p>A number sentence can have a missing number, shown as ? or a box. Use the inverse operation to find it, "
        "then put it back in to check.</p>"
        "<figure class='sn-fig'>" + bar_svg(5, "?", "35") +
        "<figcaption>5 equal parts make 35: 5 × ? = 35, so ? = 35 ÷ 5 = 7.</figcaption></figure>" +
        table(["Number sentence", "Do this", "Answer"], [
            [sent("?", "×", 8, "=", 56), "56 ÷ 8", "7"],
            [sent(9, "×", "?", "=", 108), "108 ÷ 9", "12"],
            [sent("?", "÷", 4, "=", 12), "12 × 4", "48"],
            [sent(96, "÷", "?", "=", 8), "96 ÷ 8", "12"],
        ]) +
        ex("Example", sent("?", "÷", 4, "=", 12),
           "The unknown is the total you start with. Undo ÷ 4 by multiplying: 12 × 4 = 48. Check: 48 ÷ 4 = 12.", "48") +
        "<h2>Use the properties</h2>" +
        table(["Property", "What it says", "Example"], [
            ["Commutative (turn-around)", "You can multiply in any order", "8 × 7 = 7 × 8"],
            ["Associative", "With three numbers, you can multiply any pair first", "5 × 17 × 2 = 10 × 17 = 170"],
            ["Distributive", "Split a number, multiply each part, then add", "6 × 14 = 6 × 10 + 6 × 4 = 60 + 24 = 84"],
        ]) +
        "<p>Division is <b>not</b> commutative: 20 ÷ 4 = 5, but 4 ÷ 20 is less than 1.</p>" +
        ex("Example", "7 × 16 = 70 + " + Q,
           "Split 16 into 10 + 6. 7 × 10 = 70 and 7 × 6 = 42, so ? = 42. Check: 70 + 42 = 112 = 7 × 16.", "42") +
        "<h2>The equals sign means “the same as”</h2>"
        "<p>= does not mean “the answer is”. It means both sides have the same value, like a balance.</p>"
        "<figure class='sn-fig'>" + pan_svg("3 × 8", "4 × ?") +
        "<figcaption>The pans balance: 3 × 8 = 4 × ?. The left side is 24, so 4 × ? = 24 and ? = 6.</figcaption></figure>" +
        ex("Example", sent(3, "×", 8, "=", 4, "×", "?"),
           "Work out the side you know: 3 × 8 = 24. So 4 × ? = 24. Use the inverse: ? = 24 ÷ 4 = 6.", "6") +
        "<h2>Common mistakes</h2>" +
        table(["Mistake", "What to do instead"], [
            ["? × 8 = 56, so ? = 448 (56 × 8)", "Use the inverse: 56 ÷ 8 = 7"],
            ["? ÷ 4 = 12, so ? = 3 (12 ÷ 4)", "Undo ÷ 4 by multiplying: 12 × 4 = 48"],
            ["7 × 16 = 70 + 6", "Multiply both parts: 70 + 42 = 112"],
            ["3 × 8 = 4 × ?, so ? = 24", "24 is the left side. 4 × ? = 24, so ? = 6"],
            ["3 × 8 = 4 × ?, so ? = 7 (because 3 + 8 = 4 + 7)", "The sides are multiplications, not additions: ? = 6"],
            ["6 × 7 = 42 + 3 = 45", "Write two number sentences: 6 × 7 = 42, then 42 + 3 = 45"],
        ])
    )


FAQ = [
    {"q": "What is a number sentence in Year 5 maths?",
     "a": "A number sentence uses numbers, operation signs and an equals sign, like 6 × 7 = 42. In Year 5 (AC9M5A02), students find unknown values in number sentences such as ? × 8 = 56 or 96 ÷ ? = 8."},
    {"q": "How do you find the missing number in a division number sentence?",
     "a": "Use the inverse. For ? ÷ 4 = 12, multiply: 12 × 4 = 48. For 96 ÷ ? = 8, divide: 96 ÷ 8 = 12. Then put the answer back in to check."},
    {"q": "What is a multiplication and division fact family?",
     "a": "Three numbers that make two multiplication facts and two division facts, such as 6 × 7 = 42, 7 × 6 = 42, 42 ÷ 6 = 7 and 42 ÷ 7 = 6. The Australian Curriculum calls this using multiplication and division as inverse operations (AC9M5A01)."},
    {"q": "Are missing number questions on the Year 5 NAPLAN numeracy test?",
     "a": "NAPLAN numeracy is based on the Australian Curriculum, so Year 5 students can meet number sentences with unknown values. Practising inverse operations and the equals sign as a balance helps students prepare."},
]


def gen_unit():
    rnd = random.Random(5809)
    P = People(rnd)
    sets = [set_families(), set_mult(), set_div(), set_props(), set_words(P)]
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
        "country": "au", "subject": "maths", "grade": "year-5", "slug": "number-sentences-multiplication-and-division", "sort": 9,
        "updated": UPDATED, "pdf_url": "",
        "title": "Year 5 Number Sentences: Multiplication and Division",
        "seo_title": "Year 5 Multiplication and Division Number Sentences Worksheets: Free Maths with Answer Key (Australian Curriculum)",
        "short_title": "Number Sentences: × and ÷",
        "domain": "Algebra",
        "standard_code": "AC9M5A02",
        "standard_url": "https://v9.australiancurriculum.edu.au/f-10-curriculum/learning-areas/mathematics",
        "standard_text": "Find unknown values in numerical equations involving multiplication and division using the properties of numbers and operations",
        "meta_desc": "Free Year 5 maths worksheets on multiplication and division number sentences, aligned to the Australian Curriculum (AC9M5A02, AC9M5A01): fact families, missing numbers like ? × 8 = 56 and 96 ÷ ? = 8, properties, the equals sign and word problems. 100 questions with an answer key, great for NAPLAN practice.",
        "key_big": "To find a missing number, use the inverse: division undoes multiplication, and multiplication undoes division.",
        "key_sub": "? × 8 = 56, so ? = 56 ÷ 8 = 7. ? ÷ 4 = 12, so ? = 12 × 4 = 48. The = sign means “the same as”: 3 × 8 = 4 × 6.",
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
