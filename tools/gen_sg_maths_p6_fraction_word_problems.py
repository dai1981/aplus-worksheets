# -*- coding: utf-8 -*-
"""
Singapore Primary 6 Maths: Fraction Word Problems (MOE 2021 Primary Mathematics Syllabus, Standard)
  python3 tools/gen_sg_maths_p6_fraction_word_problems.py
Fraction of a quantity, fraction of a remainder, comparing parts, finding the whole from a part,
and PSLE-style before-and-after / multi-step problems with the model method (units).
Every answer is checked with fractions.Fraction; no two choices are equal in value.
HTML attributes use single quotes (no backslashes in the JSON). Singapore English.
"""
import json, os, random, re
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "sg", "maths", "primary-6")
UPDATED = "2026-11-03"
DARK = "#4fae74"      # the part asked for
LIGHT = "#d7ecdf"     # other known parts
LINE = "#2b2b2b"
FONT = "Arial, Helvetica, sans-serif"
NB = "\u00a0"
MEASURE = {"m", "kg", "ℓ", "g", "cm", "ml", "min", "km", "m²"}


# ------------------------------------------------------------ helpers
def num(n):
    """Whole number: 4 digits as they are, 5 or more digits grouped with a no-break space."""
    s = str(int(n))
    if len(s) <= 4:
        return s
    out = ""
    while len(s) > 3:
        out = NB + s[-3:] + out
        s = s[:-3]
    return s + out


def dec(v):
    """A Fraction as a whole number or a terminating decimal, else None."""
    v = F(v)
    if v.denominator == 1:
        return num(v.numerator)
    for k in range(1, 4):
        if (v * 10 ** k).denominator == 1:
            q, r = divmod(int(v * 10 ** k), 10 ** k)
            return "%s.%0*d" % (num(q), k, r)
    return None


def money(v):
    v = F(v)
    if v.denominator == 1:
        return "$" + num(v.numerator)
    if (v * 100).denominator != 1:
        return None
    c = int(v * 100)
    return "$%s.%02d" % (num(c // 100), c % 100)


def amt(v, u):
    """An amount with its unit: u is '$', '' or a unit/noun written after the number."""
    if u == "$":
        return money(v)
    if u not in MEASURE and F(v).denominator != 1:
        return None                     # counted things are whole numbers
    d = dec(v)
    if d is None:
        return None
    return d + ((" " + u) if u else "")


def lml(ml):
    """Millilitres as ℓ and ml."""
    l, m = divmod(int(ml), 1000)
    if l and m:
        return "%d ℓ %d ml" % (l, m)
    if l:
        return "%d ℓ" % l
    return "%d ml" % m


def fr(a, b):
    return "<span class='fr'><span class='fn'>%d</span><span class='fd'>%d</span></span>" % (a, b)


def frv(v):
    v = F(v)
    return fr(v.numerator, v.denominator)


def show(v):
    v = F(v)
    q, r = divmod(v.numerator, v.denominator)
    if r == 0:
        return num(q)
    if q == 0:
        return fr(r, v.denominator)
    return "%s %s" % (num(q), fr(r, v.denominator))


def A(v, u):
    return (amt(v, u), F(v))


def FV(v):
    return (show(v), F(v))


def mcq(q, correct, cands, e):
    """correct and cands are (html, value). Skips empty, repeated, zero or negative candidates."""
    assert correct[0], (q, correct)
    ch, vals = [correct[0]], [correct[1]]
    for h, v in cands:
        if not h or h in ch or (v is not None and (v in vals or v <= 0)):
            continue
        ch.append(h)
        vals.append(v)
        if len(ch) == 4:
            break
    assert len(ch) == 4, (q, correct, cands)
    return {"q": q, "c": ch, "a": 0, "e": e}


def balance(sets, rnd):
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


def fig(svg):
    return "<div class='qfig'>" + svg + "</div>"


def table(head, rows):
    h = "".join("<th>%s</th>" % x for x in head)
    b = "".join("<tr>" + "".join("<td>%s</td>" % c for c in r) + "</tr>" for r in rows)
    return "<div class='sn-tw'><table class='sn-table'><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>" % (h, b)


def ex(title, q, s, a):
    return ("<div class='sn-ex'><span class='sn-ex-t'>%s</span><p class='sn-ex-q'>%s</p>"
            "<p class='sn-ex-s'>%s</p><p class='sn-ex-a'>Answer: %s</p></div>" % (title, q, s, a))


def mark_large(u, pattern):
    rx = re.compile(r"<svg (?=[^>]*aria-label='" + pattern + ")")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u


# ------------------------------------------------------------ bar models
def tw(t, fs):
    return len(re.sub(r"&[a-z]+;", "x", t)) * fs * 0.6


def bars(rows, uw, aria):
    """Bar model. rows: dicts with
       name  (optional label on the left),
       segs  [(width in units, fill, number of equal cells, text inside)],
       above / below  [(from unit, to unit, label)] brackets."""
    FS = 15
    names = [r.get("name", "") for r in rows]
    namew = max(tw(n, FS) for n in names) + 10 if any(names) else 0
    x0 = namew + 4
    s = []
    lo, hi = 0.0, 0.0
    y = 4
    for r in rows:
        if r.get("above"):
            y += 30
        top, bot = y, y + 30
        x = x0
        for w, fill, cells, lab in r["segs"]:
            sw = w * uw
            cw = sw / float(cells)
            for i in range(cells):
                s.append("<rect x='%.1f' y='%d' width='%.1f' height='30' fill='%s' stroke='%s' stroke-width='1.5'/>"
                         % (x + i * cw, top, cw, fill, LINE))
            s.append("<rect x='%.1f' y='%d' width='%.1f' height='30' fill='none' stroke='%s' stroke-width='2.5'/>"
                     % (x, top, sw, LINE))
            if lab:
                s.append("<text x='%.1f' y='%d' font-size='%d' font-weight='700' fill='%s' text-anchor='middle'>%s</text>"
                         % (x + sw / 2, top + 21, FS, "#fff" if fill == DARK else LINE, lab))
            x += sw
        hi = max(hi, x)
        if r.get("name"):
            s.append("<text x='%.1f' y='%d' font-size='%d' font-weight='700' fill='%s' text-anchor='end'>%s</text>"
                     % (x0 - 8, top + 21, FS, LINE, r["name"]))
        for u0, u1, lab in r.get("above", []):
            xa, xb = x0 + u0 * uw, x0 + u1 * uw
            ly = top - 8
            s.append("<path d='M%.1f %d V%d H%.1f V%d' fill='none' stroke='%s' stroke-width='2'/>"
                     % (xa + 3, ly + 5, ly, xb - 3, ly + 5, LINE))
            s.append("<text x='%.1f' y='%d' font-size='%d' font-weight='700' fill='%s' text-anchor='middle'>%s</text>"
                     % ((xa + xb) / 2, ly - 6, FS, LINE, lab))
            lo = min(lo, (xa + xb) / 2 - tw(lab, FS) / 2)
            hi = max(hi, (xa + xb) / 2 + tw(lab, FS) / 2)
        y = bot
        if r.get("below"):
            for u0, u1, lab in r["below"]:
                xa, xb = x0 + u0 * uw, x0 + u1 * uw
                ly = bot + 9
                s.append("<path d='M%.1f %d V%d H%.1f V%d' fill='none' stroke='%s' stroke-width='2'/>"
                         % (xa + 3, ly - 5, ly, xb - 3, ly - 5, LINE))
                s.append("<text x='%.1f' y='%d' font-size='%d' font-weight='700' fill='%s' text-anchor='middle'>%s</text>"
                         % ((xa + xb) / 2, ly + 19, FS, LINE, lab))
                lo = min(lo, (xa + xb) / 2 - tw(lab, FS) / 2)
                hi = max(hi, (xa + xb) / 2 + tw(lab, FS) / 2)
            y += 34
        y += 12
    H = y - 12 + 4
    left = min(0.0, lo - 4)
    W = int(hi - left + 6)
    return ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='%d 0 %d %d' width='%d' height='%d' role='img' "
            "aria-label='bar model: %s'><g font-family='%s'>%s</g></svg>"
            % (int(left), W, H, W, H, aria, FONT, "".join(s)))


def one_bar(b, a, top_lab, bot_lab, shade_lab="", uw=None, known_shaded=True):
    """A whole bar of b units; the first a units dark. top_lab over the whole; bot_lab under the dark
    (or under the white part when known_shaded is False)."""
    uw = uw or max(28, 300 // b)
    segs = [(a, DARK, a, shade_lab), (b - a, "#fff", b - a, "")]
    below = [(0, a, bot_lab)] if known_shaded else [(a, b, bot_lab)]
    return bars([{"segs": segs, "above": [(0, b, top_lab)], "below": below}], uw,
                "a whole of %d equal units with %d units shaded" % (b, a))


def rem_bar(p, r, top_lab, l1, l2, ask):
    """Fraction of a remainder: first part p of the whole, then r of the remainder.
    The whole is drawn as p.denominator big units; the remainder is cut into r.denominator equal cells."""
    b, a = p.denominator, p.numerator
    d, c = r.denominator, r.numerator
    total = b * d                       # in small units
    w1 = a * d
    wr = (b - a) * d
    w2 = (b - a) * c
    uw = 300.0 / total
    segs = [(w1, LIGHT, a, ""),
            (w2, DARK if ask == "second" else LIGHT, c, ""),
            (wr - w2, DARK if ask == "left" else "#fff", d - c, "")]
    below = [(0, w1, l1), (w1, w1 + w2, l2)]
    if ask == "left":
        below.append((w1 + w2, total, "?"))
    return bars([{"segs": segs, "above": [(0, total, top_lab)], "below": below}], uw,
                "a whole split into %d units; %d units for the first part; the remainder split into %d equal parts"
                % (b, a, d))


# ============================================================ set 1: fraction of a quantity
def of_wrongs(a, b, q, u, order):
    out = []
    for k in order:
        if k == "one":
            v = F(q, b)
        elif k == "rest":
            v = F(q * (b - a), b)
        elif k == "times":
            v = F(a * q)
        elif k == "swap":
            v = F(q, a) * b if a > 1 else None
        if v is not None:
            out.append(A(v, u))
    return out


def of_e(a, b, q, u):
    one = F(q, b)
    return ("%d units = %s. 1 unit = %s ÷ %d = %s. %d units = %d × %s = <b>%s</b>."
            % (b, amt(q, u), amt(q, u), b, amt(one, u), a, a, amt(one, u), amt(one * a, u)))


def set_quantity():
    its = []
    # A) with a bar model
    for a, b, q, u in [(3, 5, 40, "$"), (3, 4, 36, "kg"), (2, 3, 27, "ℓ"), (5, 8, 56, "m"), (4, 7, 63, "$")]:
        qq = (fig(one_bar(b, a, amt(q, u), "?")) + "The model shows %s split into %d equal units. Find %s of %s."
              % (amt(q, u), b, fr(a, b), amt(q, u)))
        its.append(mcq(qq, A(F(a * q, b), u), of_wrongs(a, b, q, u, ["one", "rest", "times", "swap"]), of_e(a, b, q, u)))
    # B) calculate
    for a, b, q, u, form in [(5, 6, 72, "$", "of"), (3, 8, 96, "kg", "of"), (4, 9, 54, "m", "of"),
                             (7, 10, 250, "g", "of"), (2, 7, 84, "cm", "of"), (5, 12, 96, "", "x"),
                             (3, 5, 85, "", "x")]:
        if form == "of":
            qq = "Find %s of %s." % (fr(a, b), amt(q, u))
            e = of_e(a, b, q, u)
        else:
            qq = "Find the value of %s × %d." % (fr(a, b), q)
            e = "%s × %d means %s of %d. " % (fr(a, b), q, fr(a, b), q) + of_e(a, b, q, u)
        its.append(mcq(qq, A(F(a * q, b), u), of_wrongs(a, b, q, u, ["one", "times", "rest", "swap"]), e))
    # C) money in cents and unit conversion
    its.append(mcq("Find %s of $6." % fr(3, 4), A(F(9, 2), "$"),
                   [A(F(3, 2), "$"), A(18, "$"), A(8, "$"), A(2, "$")], of_e(3, 4, 6, "$")))
    its.append(mcq("Find %s of 1 h. Give your answer in minutes." % fr(2, 5), A(24, "min"),
                   [A(12, "min"), A(36, "min"), A(40, "min"), A(150, "min")],
                   "1 h = 60 min. 1 unit = 60 min ÷ 5 = 12 min. 2 units = 2 × 12 min = <b>24 min</b>. "
                   "(1 h is 60 min, not 100 min.)"))
    its.append(mcq("Find %s of 1 kg. Give your answer in grams." % fr(3, 8), A(375, "g"),
                   [A(125, "g"), A(625, "g"), A(3000, "g")],
                   "1 kg = 1000 g. 1 unit = 1000 g ÷ 8 = 125 g. 3 units = 3 × 125 g = <b>375 g</b>."))
    its.append(mcq("Find %s of 3 ℓ. Give your answer in millilitres." % fr(5, 6), A(2500, "ml"),
                   [A(500, "ml"), A(3600, "ml"), A(15000, "ml")],
                   "3 ℓ = 3000 ml. 1 unit = 3000 ml ÷ 6 = 500 ml. 5 units = 5 × 500 ml = <b>2500 ml</b>."))
    its.append(mcq("Find %s of 2 m 50 cm. Give your answer in centimetres." % fr(3, 5), A(150, "cm"),
                   [A(120, "cm"), A(50, "cm"), A(100, "cm"), A(750, "cm")],
                   "2 m 50 cm = 250 cm. 1 unit = 250 cm ÷ 5 = 50 cm. 3 units = 3 × 50 cm = <b>150 cm</b>. "
                   "(Do not leave out the 50 cm.)"))
    # D) short word problems
    its.append(mcq("There are 48 students in the school hall. %s of them are girls. How many boys are there?" % fr(5, 8),
                   A(18, "boys"), [A(30, "boys"), A(6, "boys"), A(40, "boys")],
                   "The girls are 5 units out of 8, so the boys are 3 units. 1 unit = 48 ÷ 8 = 6. "
                   "Boys: 3 × 6 = <b>18</b>. (30 is the number of girls.)"))
    its.append(mcq("A tank can hold 60 ℓ of water. It is %s full. How much more water is needed to fill it?" % fr(3, 4),
                   A(15, "ℓ"), [A(45, "ℓ"), A(20, "ℓ"), A(80, "ℓ")],
                   "The tank is 3 units full out of 4, so 1 unit is still empty. 1 unit = 60 ℓ ÷ 4 = <b>15 ℓ</b>. "
                   "(45 ℓ is the water already in the tank.)"))
    its.append(mcq("Mrs Lim baked 72 pineapple tarts for Chinese New Year. She gave away %s of them. "
                   "How many tarts did she have left?" % fr(7, 9),
                   A(16, "tarts"), [A(56, "tarts"), A(8, "tarts"), A(63, "tarts")],
                   "She gave away 7 units out of 9, so 2 units are left. 1 unit = 72 ÷ 9 = 8. "
                   "Left: 2 × 8 = <b>16</b> tarts."))
    assert len(its) == 20, len(its)
    return {"title": "Fraction of a quantity", "items": its}


# ============================================================ set 2: fraction of a remainder
def rem_amounts(W, p, r):
    first = W * p
    rem = W - first
    second = rem * r
    return first, rem, second, rem - second


def rem_item(text, W, p, r, ask, u, l1, l2, figure, n1, n2):
    first, rem, second, left = rem_amounts(W, p, r)
    e = ("%s: %s of %s = %s. Remainder: %s − %s = %s. %s: %s of %s = %s."
         % (cap(n1), frv(p), amt(W, u), amt(first, u), amt(W, u), amt(first, u), amt(rem, u),
            cap(n2), frv(r), amt(rem, u), amt(second, u)))
    if ask == "second":
        right = second
        wr = [W * r, first, left, rem, rem / r.denominator, W * p * r]
        e = e[:-len(amt(second, u)) - 1] + "<b>%s</b>. (Take %s of the remainder, not of %s.)" % (
            amt(second, u), frv(r), amt(W, u))
    elif ask == "left":
        right = left
        wr = [W - first - W * r, second, first + second, rem, W * (1 - r)]
        e += " %s: %s − %s = <b>%s</b>." % ("Girls" if n2 == "boys" else "Left", amt(rem, u), amt(second, u),
                                           amt(left, u))
    else:
        right = first + second
        wr = [first + W * r, second, left, first, W * r]
        e += " Altogether: %s + %s = <b>%s</b>." % (amt(first, u), amt(second, u), amt(right, u))
    q = text
    if figure:
        q = fig(rem_bar(p, r, amt(W, u), l1, l2, ask)) + q
    return mcq(q, A(right, u), [A(v, u) for v in wr], e)


def rem_frac(text, p, r, ask, n2):
    rem = 1 - p
    second = rem * r
    left = rem - second
    e = "Remainder: 1 − %s = %s. %s: %s of %s = %s × %s = %s." % (
        frv(p), frv(rem), cap(n2), frv(r), frv(rem), frv(r), frv(rem), frv(second))
    if ask == "fsecond":
        right = second
        wr = [r, p * r, 1 - p - r, left, p + r]
    elif ask == "fleft":
        right = left
        wr = [1 - p - r, 1 - r, p * r, second, p + r]
        e += " Left: %s − %s = %s." % (frv(rem), frv(second), frv(left))
    else:
        right = p + second
        wr = [p + r, second, left, p * r]
        e += " Altogether: %s + %s = %s." % (frv(p), frv(second), frv(right))
    e = e[:-len(frv(right)) - 1] + "<b>%s</b>." % frv(right)
    wr = [w for w in wr if 0 < w < 1]
    return mcq(text, FV(right), [FV(w) for w in wr], e)


def cap(s):
    return s[0].upper() + s[1:]


def set_remainder():
    its = []
    T = [
        ("Siti had $60. She spent %s of her money on a book and %s of the remainder on lunch. "
         "How much did she spend on lunch?", 60, F(1, 3), F(1, 4), "second", "$", "book", "?", "book", "lunch"),
        ("Mr Tan had 120 mandarin oranges. He gave %s of them to his neighbours and %s of the remainder to his relatives. "
         "How many mandarin oranges did he have left?", 120, F(1, 4), F(2, 3), "left", "", "neighbours", "relatives",
         "neighbours", "relatives"),
        ("Mdm Wong had a roll of ribbon 72 m long. She used %s of it to wrap gift boxes and %s of the remainder to make "
         "bows. How many metres of ribbon did she use to make bows?", 72, F(5, 8), F(1, 3), "second", "m", "gift boxes", "?",
         "gift boxes", "bows"),
        ("Wei Ming had 84 stickers. He gave %s of them to his sister and %s of the remainder to his friends. "
         "How many stickers did he give to his friends?", 84, F(2, 7), F(3, 5), "second", "", "sister", "?",
         "sister", "friends"),
        ("A tank had 96 ℓ of water. %s of the water was used to wash a car and %s of the remainder was used to water "
         "the plants. How much water was left in the tank?", 96, F(3, 8), F(2, 5), "left", "ℓ", "car", "plants",
         "car", "plants"),
        ("Priya had $90. She spent %s of it on a pair of shoes and %s of the remainder on a bag. "
         "How much did she spend altogether?", 90, F(2, 5), F(1, 3), "spent", "$", "shoes", "bag", "shoes", "bag"),
        ("There were 450 people at a National Day concert. %s of them were adults and %s of the remainder were boys. "
         "The rest were girls. How many girls were there?", 450, F(2, 5), F(1, 3), "left", "", "adults", "boys",
         "adults", "boys"),
        ("Mrs Ng baked 144 curry puffs. She sold %s of them in the morning and %s of the remainder in the afternoon. "
         "How many curry puffs did she sell in the afternoon?", 144, F(5, 12), F(3, 7), "second", "", "morning", "?",
         "morning", "afternoon"),
        ("Jun Jie had $150 in his savings. He used %s of it to buy a birthday present for his mother and %s of the "
         "remainder to buy books. How much money did he have left?", 150, F(1, 5), F(3, 8), "left", "$", "", "", "present",
         "books"),
        ("A drinks stall sold 240 drinks on Saturday. %s of them were bubble tea and %s of the remainder were kopi. "
         "How many cups of kopi were sold?", 240, F(3, 8), F(1, 5), "second", "", "", "", "bubble tea", "kopi"),
        ("Hafiz had $45. He spent %s of it on a T-shirt and %s of the remainder on lunch at a hawker centre. "
         "How much did he spend on lunch?", 45, F(1, 3), F(1, 4), "second", "$", "", "", "T-shirt", "lunch"),
        ("Chloe had 150 beads. She used %s of them to make a necklace and %s of the remainder to make a bracelet. "
         "How many beads did she use altogether?", 150, F(3, 5), F(2, 3), "spent", "", "", "", "necklace", "bracelet"),
        ("Ethan had $80. He topped up his EZ-Link card with %s of it and spent %s of the remainder on books. "
         "How much money did he have left?", 80, F(1, 4), F(3, 5), "left", "$", "", "", "EZ-Link card", "books"),
    ]
    for i, (text, W, p, r, ask, u, l1, l2, n1, n2) in enumerate(T):
        its.append(rem_item(text % (frv(p), frv(r)), W, p, r, ask, u, l1, l2, i < 8, n1, n2))
    # time and volume with unit changes
    its.append(mcq("Xin Yi had 3 h of free time on Saturday. She spent %s of the time reading and %s of the remaining "
                   "time at the swimming pool. How much free time did she have left? Give your answer in minutes."
                   % (fr(1, 4), fr(2, 3)),
                   A(45, "min"), [A(15, "min"), A(90, "min"), A(135, "min"), A(120, "min")],
                   "3 h = 180 min. Reading: %s of 180 min = 45 min. Remainder: 180 − 45 = 135 min. Swimming: %s of "
                   "135 min = 90 min. Left: 135 − 90 = <b>45 min</b>." % (fr(1, 4), fr(2, 3))))
    its.append(mcq("Devi had 1 ℓ 500 ml of orange juice. She poured %s of it into a glass and %s of the remainder into a "
                   "bottle. How much juice was left? Give your answer in millilitres." % (fr(1, 5), fr(2, 5)),
                   A(720, "ml"), [A(600, "ml"), A(780, "ml"), A(480, "ml"), A(1200, "ml")],
                   "1 ℓ 500 ml = 1500 ml. Glass: %s of 1500 ml = 300 ml. Remainder: 1500 − 300 = 1200 ml. Bottle: %s "
                   "of 1200 ml = 480 ml. Left: 1200 − 480 = <b>720 ml</b>." % (fr(1, 5), fr(2, 5))))
    # what fraction of the whole
    F4 = [
        ("Nurul spent %s of her money on a dress and %s of the remainder on a bag. "
         "What fraction of her money did she spend on the bag?", F(1, 4), F(1, 3), "fsecond", "bag"),
        ("Arjun spent %s of his money on a game and %s of the remainder on a book. "
         "What fraction of his money did he have left?", F(2, 5), F(1, 2), "fleft", "book"),
        ("Sarah used %s of a packet of flour to make bread and %s of the remainder to make a cake. "
         "What fraction of the packet of flour did she use for the cake?", F(1, 3), F(3, 4), "fsecond", "cake"),
        ("A water tank was full. %s of the water was used on Monday and %s of the remainder was used on Tuesday. "
         "What fraction of the water was left?", F(3, 5), F(1, 4), "fleft", "Tuesday"),
        ("Ryan spent %s of his money at a hawker centre and %s of the remainder at a bookshop. "
         "What fraction of his money did he spend altogether?", F(1, 6), F(3, 5), "fspent", "bookshop"),
    ]
    for text, p, r, ask, n2 in F4:
        its.append(rem_frac(text % (frv(p), frv(r)), p, r, ask, n2))
    assert len(its) == 20, len(its)
    return {"title": "Fraction of a remainder", "items": its}


# ============================================================ set 3: comparing parts
def set_compare():
    its = []
    # A) two fractions of the same whole
    S = [
        ("Mr Rahman had 48 m of rope. He used %s of it to tie up a tent and %s of it to make a fence for a garden "
         "bed. How much more rope did he use for the tent than for the fence?", 48, F(3, 8), F(1, 4), "m"),
        ("There are 40 students in a P6 class. %s of them take the bus to school and %s of them walk. "
         "How many more students take the bus than walk?", 40, F(3, 5), F(1, 4), "students"),
        ("Mrs Ng had $120. She spent %s of it on groceries and %s of it on a gift. "
         "How much more did she spend on groceries than on the gift?", 120, F(5, 12), F(1, 4), "$"),
        ("A hawker stall sold 360 plates of food in a day. %s of them were chicken rice and %s of them were laksa. "
         "How many more plates of chicken rice than laksa were sold?", 360, F(4, 9), F(1, 6), "plates"),
        ("Sarah had $30 of pocket money. She saved %s of it and spent %s of it on snacks. "
         "How much more did she save than spend on snacks?", 30, F(2, 5), F(1, 4), "$"),
        ("A school garden has an area of 90 m². %s of it is grass and %s of it is flower beds. "
         "How much greater is the area of grass than the area of flower beds?", 90, F(2, 5), F(1, 3), "m²"),
    ]
    for text, W, p1, p2, u in S:
        a1, a2 = W * p1, W * p2
        e = ("%s of %s = %s. %s of %s = %s. Difference: %s − %s = <b>%s</b>. "
             "(You can also subtract first: %s − %s = %s, and %s of %s = %s.)"
             % (frv(p1), amt(W, u), amt(a1, u), frv(p2), amt(W, u), amt(a2, u), amt(a1, u), amt(a2, u),
                amt(a1 - a2, u), frv(p1), frv(p2), frv(p1 - p2), frv(p1 - p2), amt(W, u), amt(a1 - a2, u)))
        uu = "" if u in ("students", "plates") else u
        d = p1 - p2
        fake = ((frv(d) + " " + uu) if uu and uu != "$" else ("$" + frv(d) if uu == "$" else frv(d)), d)
        its.append(mcq(text % (frv(p1), frv(p2)), A(a1 - a2, u),
                       [A(a1, u), A(a1 + a2, u), A(a2, u), fake, A(W - a1 - a2, u)], e))
    its.append(mcq("Mei Ling ate %s of a cake and her brother ate %s of the same cake. How much more of the cake did "
                   "Mei Ling eat than her brother?" % (fr(3, 8), fr(1, 6)),
                   FV(F(5, 24)), [R(2, 8), R(2, 24), FV(F(13, 24)), R(2, 2)],
                   "Use a common denominator: %s = %s and %s = %s. %s − %s = <b>%s</b>. "
                   "(Rename both fractions before you subtract.)"
                   % (fr(3, 8), fr(9, 24), fr(1, 6), fr(4, 24), fr(9, 24), fr(4, 24), fr(5, 24))))
    # B) one quantity is a fraction of another (two bars)
    def two(n1, a, n2, b, lab_rows, uw=34):
        r1 = {"name": n1, "segs": [(a, LIGHT, a, "")]}
        r2 = {"name": n2, "segs": [(b, LIGHT, b, "")]}
        for row, key, u0, u1, t in lab_rows:
            (r1 if row == 1 else r2).setdefault(key, []).append((u0, u1, t))
        return bars([r1, r2], uw, "%s has %d units and %s has %d units" % (n1, a, n2, b))

    q = (fig(two("Ali", 2, "Mei Ling", 5, [(1, "above", 0, 2, "?"), (2, "below", 2, 5, "$45")])) +
         "Ali’s savings are %s of Mei Ling’s savings. Mei Ling has $45 more than Ali. How much money does Ali have?"
         % fr(2, 5))
    its.append(mcq(q, A(30, "$"), [A(15, "$"), A(75, "$"), A(18, "$"), A(105, "$")],
                   "Ali has 2 units and Mei Ling has 5 units. The difference is 5 − 2 = 3 units. 3 units = $45, "
                   "1 unit = $15. Ali: 2 × $15 = <b>$30</b>. (Do not stop at 1 unit.)"))
    q = ("Wei Ming has %s as many stamps as Jun Jie. Jun Jie has 18 more stamps than Wei Ming. "
         "How many stamps do they have altogether?" % fr(3, 4))
    its.append(mcq(q, A(126, "stamps"), [A(54, "stamps"), A(72, "stamps"), A(42, "stamps")],
                   "Wei Ming has 3 units and Jun Jie has 4 units. The difference is 1 unit = 18. "
                   "Altogether: 3 + 4 = 7 units = 7 × 18 = <b>126</b> stamps."))
    q = (fig(two("Box A", 5, "Box B", 8, [(2, "below", 0, 8, "39 kg altogether")], uw=30)) +
         "The mass of Box A is %s of the mass of Box B. The total mass of the two boxes is 39 kg. "
         "What is the mass of Box A?" % fr(5, 8))
    its.append(mcq(q, A(15, "kg"), [A(3, "kg"), A(24, "kg"), A(9, "kg")],
                   "Box A has 5 units and Box B has 8 units: 13 units altogether. 13 units = 39 kg, "
                   "1 unit = 3 kg. Box A: 5 × 3 kg = <b>15 kg</b>."))
    q = (fig(two("Tank A", 4, "Tank B", 7, [(2, "below", 4, 7, "27 ℓ"), (2, "above", 0, 7, "?")])) +
         "The volume of water in Tank A is %s of the volume of water in Tank B. Tank B has 27 ℓ more water than "
         "Tank A. How much water is in Tank B?" % fr(4, 7))
    its.append(mcq(q, A(63, "ℓ"), [A(36, "ℓ"), A(9, "ℓ"), A(99, "ℓ")],
                   "Tank A has 4 units and Tank B has 7 units. The difference is 3 units = 27 ℓ, so 1 unit = 9 ℓ. "
                   "Tank B: 7 × 9 ℓ = <b>63 ℓ</b>."))
    q = (fig(two("Farah", 2, "Hafiz", 3, [(2, "below", 0, 3, "$90 altogether")], uw=44)) +
         "Farah saved %s as much as her brother Hafiz. Together they saved $90. "
         "How much more did Hafiz save than Farah?" % fr(2, 3))
    its.append(mcq(q, A(18, "$"), [A(36, "$"), A(54, "$"), A(30, "$")],
                   "Farah has 2 units and Hafiz has 3 units: 5 units altogether. 5 units = $90, 1 unit = $18. "
                   "Hafiz saved 1 unit more: <b>$18</b>."))
    q = ("A ribbon was cut into two pieces. The shorter piece is %s as long as the longer piece. The difference in "
         "their lengths is 24 cm. How long was the ribbon before it was cut?" % fr(3, 5))
    its.append(mcq(q, A(96, "cm"), [A(36, "cm"), A(60, "cm"), A(40, "cm")],
                   "Shorter piece: 3 units. Longer piece: 5 units. The difference is 2 units = 24 cm, so 1 unit = 12 cm. "
                   "The ribbon: 8 units = 8 × 12 cm = <b>96 cm</b>."))
    q = ("There are %s as many boys as girls in a school choir. There are 63 pupils in the choir. "
         "How many girls are there?" % fr(3, 4))
    its.append(mcq(q, A(36, "girls"), [A(27, "girls"), A(9, "girls"), A(84, "girls")],
                   "Boys: 3 units. Girls: 4 units. 7 units = 63, 1 unit = 9. Girls: 4 × 9 = <b>36</b>. "
                   "(63 is all the pupils, not the boys.)"))
    # C) comparing a part with a fraction of the remainder
    q = (fig(rem_bar(F(1, 3), F(1, 4), "$72", "game", "book", "")) +
         "Ali had $72. He spent %s of it on a game and %s of the remainder on a book. "
         "How much more did he spend on the game than on the book?" % (fr(1, 3), fr(1, 4)))
    its.append(mcq(q, A(12, "$"), [A(6, "$"), A(36, "$"), A(24, "$"), A(48, "$")],
                   "Game: %s of $72 = $24. Remainder: $72 − $24 = $48. Book: %s of $48 = $12. "
                   "Difference: $24 − $12 = <b>$12</b>. (%s of $72 = $18 is wrong: the book is %s of the remainder.)"
                   % (fr(1, 3), fr(1, 4), fr(1, 4), fr(1, 4))))
    q = ("Devi had 120 beads. She used %s of them for a bracelet and %s of the remainder for a key chain. "
         "How many more beads did she use for the bracelet than for the key chain?" % (fr(3, 8), fr(2, 5)))
    its.append(mcq(q, A(15, "beads"), [A(75, "beads"), A(30, "beads"), A(45, "beads")],
                   "Bracelet: %s of 120 = 45. Remainder: 120 − 45 = 75. Key chain: %s of 75 = 30. "
                   "Difference: 45 − 30 = <b>15</b> beads." % (fr(3, 8), fr(2, 5))))
    q = ("Mrs Lim had 2 kg of flour. She used %s of it to make bread and %s of the remainder to make a cake. "
         "How much more flour did she use for the cake than for the bread? Give your answer in grams."
         % (fr(1, 4), fr(4, 5)))
    its.append(mcq(q, A(700, "g"), [A(1100, "g"), A(1200, "g"), A(500, "g"), A(1700, "g")],
                   "2 kg = 2000 g. Bread: %s of 2000 g = 500 g. Remainder: 1500 g. Cake: %s of 1500 g = 1200 g. "
                   "Difference: 1200 − 500 = <b>700 g</b>." % (fr(1, 4), fr(4, 5))))
    q = ("Jun Jie spent %s of his money on food and %s of the remainder on a book. How much more did he spend on the "
         "book than on food? Give your answer as a fraction of his money." % (fr(1, 6), fr(1, 2)))
    its.append(mcq(q, FV(F(1, 4)), [FV(F(1, 3)), FV(F(7, 12)), FV(F(5, 12))],
                   "Book: %s of %s = %s. Food: %s = %s. Difference: %s − %s = %s = <b>%s</b>. "
                   "(%s − %s = %s is wrong: the two fractions are of different wholes.)"
                   % (fr(1, 2), fr(5, 6), fr(5, 12), fr(1, 6), fr(2, 12), fr(5, 12), fr(2, 12), fr(3, 12), fr(1, 4),
                      fr(1, 2), fr(1, 6), fr(1, 3))))
    q = ("Kavya ate %s of a pizza. Then Ryan ate %s of what was left. Who ate more pizza?" % (fr(1, 4), fr(1, 3)))
    its.append(mcq(q, ("They ate the same amount.", None), [("Kavya", None), ("Ryan", None), ("You cannot tell.", None)],
                   "%s was left after Kavya ate. Ryan ate %s of %s = %s. Both ate %s of the pizza, so "
                   "<b>they ate the same amount</b>." % (fr(3, 4), fr(1, 3), fr(3, 4), fr(1, 4), fr(1, 4))))
    q = ("Ahmad cycled a 36 km route. He cycled %s of it before lunch and %s of the remaining distance after lunch. "
         "How much farther did he cycle after lunch than before lunch?" % (fr(1, 3), fr(3, 4)))
    its.append(mcq(q, A(6, "km"), [A(15, "km"), A(30, "km"), A(18, "km")],
                   "Before lunch: %s of 36 km = 12 km. Remaining: 24 km. After lunch: %s of 24 km = 18 km. "
                   "Difference: 18 − 12 = <b>6 km</b>." % (fr(1, 3), fr(3, 4))))
    assert len(its) == 20, len(its)
    return {"title": "Comparing parts: how much more?", "items": its}


def R(n, d):
    return (fr(n, d), F(n, d))


# ============================================================ set 4: finding the whole from a part
def set_whole():
    its = []
    # A) a/b of the whole is N
    P = [
        ("%s of the students in a P6 class wear spectacles. 12 students wear spectacles. "
         "How many students are there in the class?", 2, 7, 12, "students", ["one", "times", "rest"]),
        ("%s of a sum of money is $36. What is the whole sum of money?", 3, 5, 36, "$", ["one", "times", "rest"]),
        ("Mr Kumar has read %s of a book. He has read 150 pages. How many pages are there in the book?",
         5, 8, 150, "pages", ["one", "rest", "times"]),
        ("A tank is %s full. It has 24 ℓ of water in it. What is the capacity of the tank?",
         3, 8, 24, "ℓ", ["one", "times", "rest", "of"]),
        ("%s of the pupils in the canteen bought chicken rice. 36 pupils bought chicken rice. "
         "How many pupils were in the canteen?", 4, 9, 36, "pupils", ["one", "rest", "times", "of"]),
        ("Siti saved %s of her pocket money. She saved $42. How much pocket money did she have?",
         7, 10, 42, "$", ["one", "rest", "of", "times"]),
    ]
    for text, a, b, N, u, order in P:
        one = F(N, a)
        whole = one * b
        wr = []
        for k in order:
            wr.append(A({"one": one, "times": N * b, "rest": one * (b - a), "of": F(N * a, b)}[k], u))
        e = ("%d units = %s. 1 unit = %s ÷ %d = %s. The whole is %d units: %d × %s = <b>%s</b>."
             % (a, amt(N, u), amt(N, u), a, amt(one, u), b, b, amt(one, u), amt(whole, u)))
        its.append(mcq(text % fr(a, b), A(whole, u), wr, e))
    # B) after using a/b, L is left
    L = [
        ("Hui Min spent %s of her money and had $24 left. How much money did she have at first?", 3, 5, 24, "$"),
        ("Arjun gave away %s of his marbles and had 28 marbles left. How many marbles did he have at first?",
         5, 9, 28, "marbles"),
        ("After %s of the water in a tank was used, 45 ℓ of water was left. How much water was in the tank at first?",
         3, 8, 45, "ℓ"),
        ("A fruit seller sold %s of his durians and had 40 durians left. How many durians did he have at first?",
         7, 12, 40, "durians"),
        ("Ryan used %s of the value on his EZ-Link card and $5.40 was left. How much was on the card at first?",
         2, 3, F(27, 5), "$"),
    ]
    for text, a, b, Lf, u in L:
        k = b - a
        one = F(Lf) / k
        whole = one * b
        wr = [A(F(Lf) / a * b, u), A(one, u), A(one * a, u), A(F(Lf) * k, u), A(F(Lf) * b, u)]
        if k == 1:
            mid = "1 unit = %s." % amt(Lf, u)
        else:
            mid = "%d units = %s, 1 unit = %s." % (k, amt(Lf, u), amt(one, u))
        e = ("%s was used, so %d − %d = %d %s left. %s At first: %d units = %d × %s = <b>%s</b>. "
             "(%s is the part left, not the part used.)"
             % (fr(a, b), b, a, k, "unit is" if k == 1 else "units are", mid, b, b, amt(one, u), amt(whole, u),
                amt(Lf, u)))
        its.append(mcq(text % fr(a, b), A(whole, u), wr, e))
    # C) read the model
    M = [(8, 3, 27, True), (5, 3, 51, True), (7, 3, 32, False), (9, 2, 49, False)]
    for b, a, N, sh in M:
        known = a if sh else b - a
        one = F(N, known)
        whole = one * b
        if sh:
            q = (fig(one_bar(b, a, "?", str(N))) + "In the model, %d of the %d equal units have a value of %d. "
                 "What is the value of the whole bar?" % (a, b, N))
        else:
            q = (fig(one_bar(b, a, "?", str(N), known_shaded=False)) + "In the model, the %d white units have a value of %d. "
                 "What is the value of the whole bar?" % (b - a, N))
        wr = [A(one, ""), A(N * b, ""), A(one * (b - known), ""), A(N + one, "")]
        e = ("%d units = %d. 1 unit = %d ÷ %d = %s. The whole bar is %d units: %d × %s = <b>%s</b>."
             % (known, N, N, known, dec(one), b, b, dec(one), dec(whole)))
        its.append(mcq(q, A(whole, ""), wr, e))
    # D) whole from a part of a remainder
    its.append(mcq("Siti spent %s of her money on a book and %s of the remainder on lunch. She spent $10 on lunch. "
                   "How much money did she have at first?" % (fr(1, 3), fr(1, 4)),
                   A(60, "$"), [A(40, "$"), A(120, "$"), A(30, "$")],
                   "Lunch = %s of the remainder, so the remainder = 4 × $10 = $40. The remainder is %s of her money: "
                   "2 units = $40, 1 unit = $20. At first: 3 × $20 = <b>$60</b>." % (fr(1, 4), fr(2, 3))))
    its.append(mcq("Mr Tan gave %s of his mandarin oranges to his neighbours and %s of the remainder to his relatives. "
                   "He had 30 mandarin oranges left. How many did he have at first?" % (fr(1, 4), fr(2, 3)),
                   A(120, ""), [A(360, ""), A(90, ""), A(40, "")],
                   "He had %s of the remainder left, so the remainder = 3 × 30 = 90. The remainder is %s of all: "
                   "3 units = 90, 1 unit = 30. At first: 4 × 30 = <b>120</b>. (1 − %s − %s = %s is wrong: "
                   "the fractions are of different wholes.)" % (fr(1, 3), fr(3, 4), fr(1, 4), fr(2, 3), fr(1, 12))))
    its.append(mcq("Nurul spent %s of her money on a bag and %s of the remainder on shoes. She had $45 left. "
                   "How much money did she have at first?" % (fr(2, 5), fr(1, 2)),
                   A(150, "$"), [A(450, "$"), A(90, "$"), A(75, "$")],
                   "She had %s of the remainder left, so the remainder = 2 × $45 = $90. The remainder is %s of her "
                   "money: 3 units = $90, 1 unit = $30. At first: 5 × $30 = <b>$150</b>." % (fr(1, 2), fr(3, 5))))
    its.append(mcq("A tank was full of water. %s of the water was used in the morning and %s of the remaining water was "
                   "used in the afternoon. 36 ℓ of water was left. How much water was in the tank at first?"
                   % (fr(1, 4), fr(1, 3)),
                   A(72, "ℓ"), [A(48, "ℓ"), A(54, "ℓ"), A(144, "ℓ")],
                   "%s of the remaining water was left, so the remaining water = 36 ℓ ÷ 2 × 3 = 54 ℓ. "
                   "It is %s of the full tank: 3 units = 54 ℓ, 1 unit = 18 ℓ. At first: 4 × 18 ℓ = <b>72 ℓ</b>."
                   % (fr(2, 3), fr(3, 4))))
    its.append(mcq("Ethan spent %s of his savings on a watch and %s of the remainder on a bag. He spent $60 on the bag. "
                   "How much were his savings at first?" % (fr(3, 8), fr(2, 5)),
                   A(240, "$"), [A(150, "$"), A(160, "$"), A(96, "$")],
                   "The bag = %s of the remainder, so the remainder = $60 ÷ 2 × 5 = $150. The remainder is %s of his "
                   "savings: 5 units = $150, 1 unit = $30. At first: 8 × $30 = <b>$240</b>." % (fr(2, 5), fr(5, 8))))
    assert len(its) == 20, len(its)
    return {"title": "Finding the whole from a part", "items": its}


# ============================================================ set 5: PSLE-style problems
def set_psle():
    its = []

    def add(q, right, wrongs, e, u):
        its.append(mcq(q, A(right, u), [A(w, u) for w in wrongs], e))

    # equal fractions
    W, H = 45, 40
    assert F(2, 3) * W == F(3, 4) * H and W + H == 85
    add("%s of Wei Ming’s marbles is equal to %s of Hafiz’s marbles. They have 85 marbles altogether. "
        "How many marbles does Wei Ming have?" % (fr(2, 3), fr(3, 4)), 45, [40, 34, 5],
        "Make the numerators the same: %s = %s and %s = %s. So Wei Ming has 9 units and Hafiz has 8 units. "
        "17 units = 85, 1 unit = 5. Wei Ming: 9 × 5 = <b>45</b> marbles." % (fr(2, 3), fr(6, 9), fr(3, 4), fr(6, 8)),
        "marbles")
    B, G = 130, 156
    assert F(3, 5) * B == F(1, 2) * G and G - B == 26
    add("In a school hall, %s of the boys is equal to %s of the girls. There are 26 more girls than boys. "
        "How many girls are there?" % (fr(3, 5), fr(1, 2)), 156, [130, 26, 286],
        "Make the numerators the same: %s = %s and %s = %s. Boys: 5 units. Girls: 6 units. "
        "The difference is 1 unit = 26. Girls: 6 × 26 = <b>156</b>." % (fr(3, 5), fr(3, 5), fr(1, 2), fr(3, 6)), "girls")
    a_, b_ = 24, 45
    assert F(3, 4) * a_ == F(2, 5) * b_ and b_ - a_ == 21
    add("%s of the mass of Box A is equal to %s of the mass of Box B. Box B is 21 kg heavier than Box A. "
        "What is the total mass of the two boxes?" % (fr(3, 4), fr(2, 5)), 69, [24, 45, 189],
        "Make the numerators the same: %s = %s and %s = %s. Box A: 8 units. Box B: 15 units. "
        "The difference is 7 units = 21 kg, so 1 unit = 3 kg. Total: 23 units = 23 × 3 kg = <b>69 kg</b>. "
        "(Do not use the denominators 4 and 5 as the units.)" % (fr(3, 4), fr(6, 8), fr(2, 5), fr(6, 15)), "kg")
    # transfers (total unchanged)
    q = (fig(bars([{"name": "Jun Jie", "segs": [(3, LIGHT, 3, "")]},
                   {"name": "Zhi Hao", "segs": [(4, LIGHT, 4, ""), (1, DARK, 1, "")], "below": [(4, 5, "12")]}], 40,
                  "Jun Jie has 3 units and Zhi Hao has 5 units")) +
         "Jun Jie had %s as many stickers as Zhi Hao. After Zhi Hao gave Jun Jie 12 stickers, they had the same number "
         "of stickers. How many stickers did they have altogether?" % fr(3, 5))
    assert 36 + 12 == 60 - 12
    add(q, 96, [48, 60, 36],
        "Jun Jie: 3 units. Zhi Hao: 5 units. To have the same number, each needs 4 units, so Zhi Hao gave 1 unit. "
        "1 unit = 12. Altogether: 8 units = 8 × 12 = <b>96</b> stickers.", "stickers")
    assert 80 + 30 == 140 - 30 and F(80, 140) == F(4, 7)
    add("Priya had %s as much money as her sister Devi. After Devi gave Priya $30, they had the same amount of money. "
        "How much money did Priya have at first?" % fr(4, 7), 80, [40, 140, 110],
        "Priya: 4 units. Devi: 7 units. The difference is 3 units. After Devi gives $30, the difference is 0, so "
        "3 units = 2 × $30 = $60. 1 unit = $20. Priya at first: 4 × $20 = <b>$80</b>.", "$")
    assert F(15, 40) == F(3, 8) and F(15 + 20, 40) == F(7, 8)
    add("Raju had %s as many cards as Arjun. After Raju bought 20 more cards, he had %s as many cards as Arjun. "
        "How many cards does Arjun have?" % (fr(3, 8), fr(7, 8)), 40, [15, 35, 5],
        "Arjun’s cards do not change: 8 units. Raju went from 3 units to 7 units, so 4 units = 20 and 1 unit = 5. "
        "Arjun: 8 × 5 = <b>40</b> cards.", "cards")
    # tank before and after
    add("A tank was %s full of water. After 18 ℓ of water was poured in, it was %s full. "
        "What is the capacity of the tank?" % (fr(2, 5), fr(4, 5)), 45, [F(45, 2), 90, 30],
        "The water went up from %s to %s, which is %s of the tank. 2 units = 18 ℓ, 1 unit = 9 ℓ. "
        "Capacity: 5 units = <b>45 ℓ</b>." % (fr(2, 5), fr(4, 5), fr(2, 5)), "ℓ")
    assert F(18 + 12, 48 + 12) == F(1, 2)
    add("A box had some red beads and blue beads. %s of the beads were red. After Siti put in 12 more red beads, "
        "%s of the beads were red. How many beads were in the box at first?" % (fr(3, 8), fr(1, 2)), 48, [60, 32, 24],
        "At first: red 3 units, blue 5 units. The blue beads do not change. After: red = blue = 5 units. "
        "The red beads went up by 2 units = 12, so 1 unit = 6. At first: 8 units = <b>48</b> beads.", "beads")
    # remainder with a difference
    q = (fig(rem_bar(F(1, 4), F(2, 3), "?", "watch", "shoes", "")) +
         "Mr Kumar spent %s of his money on a watch and %s of the remainder on a pair of shoes. The shoes cost $36 more "
         "than the watch. How much money did he have at first?" % (fr(1, 4), fr(2, 3)))
    add(q, 144, [72, 108, 36],
        "Watch: 1 unit out of 4. The remainder is 3 units; the shoes are %s of it = 2 units. "
        "The shoes cost 1 unit more than the watch: 1 unit = $36. At first: 4 × $36 = <b>$144</b>." % fr(2, 3), "$")
    W = 360
    assert W * F(5, 8) - W * F(3, 8) * F(1, 3) == 180
    add("Mr Rahman spent %s of his money on a bicycle and %s of the remainder on a helmet. The bicycle cost $180 more "
        "than the helmet. How much did the helmet cost?" % (fr(5, 8), fr(1, 3)), 45, [225, 360, 135],
        "Bicycle: 5 units out of 8. Remainder: 3 units; helmet: %s of 3 units = 1 unit. The difference is "
        "5 − 1 = 4 units = $180, so 1 unit = $45. The helmet cost <b>$45</b>." % fr(1, 3), "$")
    assert 120 * F(1, 4) == 30 and 90 * F(2, 3) == 60
    add("Kavya read %s of a storybook on Monday and %s of the remaining pages on Tuesday. She read 30 more pages on "
        "Tuesday than on Monday. How many pages did she read on Tuesday?" % (fr(1, 4), fr(2, 3)), 60, [120, 30, 80],
        "Monday: 1 unit out of 4. Remainder: 3 units; Tuesday: %s of 3 units = 2 units. The difference is 1 unit = 30 "
        "pages. Tuesday: 2 × 30 = <b>60</b> pages." % fr(2, 3), "pages")
    # boys and girls
    assert 200 * F(3, 5) * F(1, 4) + 200 * F(2, 5) * F(1, 2) == 70
    add("%s of the pupils in a school are girls. %s of the girls and %s of the boys wear spectacles. 70 pupils wear "
        "spectacles. How many girls are there in the school?" % (fr(3, 5), fr(1, 4), fr(1, 2)), 120, [80, 200, 30],
        "Girls with spectacles: %s × %s = %s. Boys with spectacles: %s × %s = %s = %s. Together: %s of the pupils = 70, "
        "so %s = 10 and all the pupils = 200. Girls: %s of 200 = <b>120</b>."
        % (fr(1, 4), fr(3, 5), fr(3, 20), fr(1, 2), fr(2, 5), fr(1, 5), fr(4, 20), fr(7, 20), fr(1, 20), fr(3, 5)),
        "girls")
    # working back from what is left
    assert 72 * F(2, 3) * F(3, 4) == 36
    add("Xin Yi gave %s of her stickers to her brother and %s of the remainder to her sister. She had 36 stickers left. "
        "How many stickers did she give to her sister?" % (fr(1, 3), fr(1, 4)), 12, [72, 24, 9],
        "36 stickers are %s of the remainder, so the remainder = 36 ÷ 3 × 4 = 48. Sister: %s of 48 = <b>12</b>."
        % (fr(3, 4), fr(1, 4)), "stickers")
    assert 30 * F(3, 5) * F(1, 4) == F(9, 2)
    add("Chloe spent %s of her money on pens and %s of the remainder on files. She had $4.50 left. "
        "How much did she spend on pens?" % (fr(2, 5), fr(3, 4)), 12, [30, F(27, 2), 18],
        "$4.50 is %s of the remainder, so the remainder = 4 × $4.50 = $18. The remainder is %s of her money: "
        "3 units = $18, 1 unit = $6. Pens: 2 units = <b>$12</b>." % (fr(1, 4), fr(3, 5)), "$")
    assert 300 * F(3, 5) * F(2, 3) == 120
    add("At a CCA fair, %s of the students signed up for sports and %s of the rest signed up for uniformed groups. "
        "The other 120 students signed up for clubs. How many students signed up for uniformed groups?"
        % (fr(2, 5), fr(1, 3)), 60, [300, 100, 180],
        "The 120 students are %s of the rest, so the rest = 120 ÷ 2 × 3 = 180. Uniformed groups: %s of 180 = <b>60</b>."
        % (fr(2, 3), fr(1, 3)), "students")
    assert 40 * F(3, 5) * F(1, 2) == 12
    add("Mr Tan drove from his home to Changi Airport. He stopped for breakfast after driving %s of the distance. "
        "After breakfast, he drove %s of the remaining distance and then had 12 km left to drive. "
        "How far was his home from the airport?" % (fr(2, 5), fr(1, 2)), 40, [120, 24, 20],
        "12 km is %s of the remaining distance, so the remaining distance = 24 km. It is %s of the whole: "
        "3 units = 24 km, 1 unit = 8 km. Whole: 5 units = <b>40 km</b>." % (fr(1, 2), fr(3, 5)), "km")
    assert 3500 * F(5, 7) * F(1, 2) == 1250
    its.append(mcq("Mrs Lim poured %s of a bottle of milk into a jug and %s of the rest into cups. 1 ℓ 250 ml of milk "
                   "was left in the bottle. How much milk was in the bottle at first?" % (fr(2, 7), fr(1, 2)),
                   (lml(3500), F(3500)), [(lml(2500), F(2500)), (lml(1750), F(1750)), (lml(1000), F(1000))],
                   "1 ℓ 250 ml = 1250 ml. It is %s of the rest, so the rest = 2 × 1250 ml = 2500 ml. The rest is %s "
                   "of the milk: 5 units = 2500 ml, 1 unit = 500 ml. At first: 7 × 500 ml = 3500 ml = <b>3 ℓ 500 ml</b>."
                   % (fr(1, 2), fr(5, 7))))
    # same amounts at first
    q = (fig(bars([{"name": "Hafiz", "segs": [(1, LIGHT, 1, ""), (3, "#fff", 3, "")], "below": [(0, 1, "spent")]},
                   {"name": "Ryan", "segs": [(3, LIGHT, 3, ""), (1, "#fff", 1, "")], "below": [(0, 3, "$42")]}], 56,
                  "Hafiz and Ryan each have 4 units at first")) +
         "Hafiz and Ryan had the same amount of money. Hafiz spent %s of his money and Ryan spent $42. Then Hafiz had "
         "3 times as much money as Ryan. How much money did each boy have at first?" % fr(1, 4))
    assert 56 * F(3, 4) == 3 * (56 - 42)
    add(q, 56, [42, 14, 168],
        "Each boy had 4 units. Hafiz has 3 units left, so Ryan has 1 unit left (3 times as much). "
        "Ryan spent 3 units = $42, so 1 unit = $14. At first: 4 × $14 = <b>$56</b> each.", "$")
    assert 15 + 6 == 25 - 4
    add("In a club, the number of boys was %s of the number of girls. Then 6 more boys joined and 4 girls left. "
        "After that, there were as many boys as girls. How many members were in the club at first?" % fr(3, 5),
        40, [24, 15, 25],
        "Boys: 3 units. Girls: 5 units. After: 3 units + 6 = 5 units − 4, so 2 units = 6 + 4 = 10 and 1 unit = 5. "
        "At first: 8 units = <b>40</b> members.", "members")
    assert ((42 - 21 - 3) - 9 - 3) == 6
    add("Sarah gave %s of her sweets and 3 more to Ethan. Then she gave %s of the remaining sweets and 3 more to Chloe. "
        "She had 6 sweets left. How many sweets did she have at first?" % (fr(1, 2), fr(1, 2)), 42, [24, 18, 33],
        "Work backwards. Before the last 3: 6 + 3 = 9, which is half, so before Chloe: 18. Before the 3 for Ethan: "
        "18 + 3 = 21, which is half, so at first: 42. She had <b>42</b> sweets.", "sweets")
    assert len(its) == 20, len(its)
    return {"title": "PSLE-style multi-step and before-and-after problems", "items": its}


# ============================================================ lesson
def body_html():
    f1 = ("<figure class='sn-fig'>" + one_bar(5, 3, "$40", "?") +
          "<figcaption>" + fr(3, 5) + " of $40: 5 units = $40, 1 unit = $8, 3 units = $24.</figcaption></figure>")
    f2 = ("<figure class='sn-fig'>" + rem_bar(F(1, 3), F(1, 4), "$60", "book", "lunch", "left") +
          "<figcaption>Spent " + fr(1, 3) + " on a book, then " + fr(1, 4) + " of the remainder on lunch. "
          "The remainder ($40) is cut into 4 equal parts.</figcaption></figure>")
    f3 = ("<figure class='sn-fig'>" + one_bar(7, 2, "?", "12") +
          "<figcaption>" + fr(2, 7) + " of the class is 12: 2 units = 12, 1 unit = 6, 7 units = 42.</figcaption></figure>")
    return (
        "<h2>The big idea</h2>"
        "<p>Every fraction is a fraction <b>of something</b>. Before you calculate, ask: “a fraction of what?” "
        "Draw a bar model and work with <b>units</b>: find 1 unit first, then the number of units you need.</p>"
        "<h2>Fraction of a quantity</h2>"
        "<p>Divide by the denominator to find 1 unit. Multiply by the numerator.</p>"
        + f1 +
        "<h2>Fraction of a remainder</h2>"
        "<p>When a question says “of the remainder” or “of the rest”, find the remainder first. "
        "Then take the fraction of the remainder, not of the whole.</p>"
        + f2
        + ex("Example", "Siti had $60. She spent " + fr(1, 3) + " of it on a book and " + fr(1, 4)
             + " of the remainder on lunch. How much did she have left?",
             "Book: " + fr(1, 3) + " of $60 = $20. Remainder: $60 − $20 = $40. Lunch: " + fr(1, 4)
             + " of $40 = $10. Left: $40 − $10 = $30.", "$30")
        + "<h2>Finding the whole from a part</h2>"
        "<p>If you know the value of some units, find 1 unit, then multiply by the total number of units.</p>"
        + f3
        + ex("Example", "Hui Min spent " + fr(3, 5) + " of her money and had $24 left. How much did she have at first?",
             "She has 5 − 3 = 2 units left. 2 units = $24, so 1 unit = $12. At first: 5 units = 5 × $12.", "$60")
        + "<h2>Before-and-after problems</h2>"
        "<p>Look for the quantity that <b>does not change</b> (the total, the difference or one person’s amount) "
        "and use the same units for it before and after.</p>"
        + ex("Example", "Jun Jie had " + fr(3, 5) + " as many stickers as Zhi Hao. After Zhi Hao gave Jun Jie 12 stickers, "
             "they had the same number. How many stickers did they have altogether?",
             "Jun Jie: 3 units. Zhi Hao: 5 units. To be equal, both need 4 units, so Zhi Hao gave 1 unit. "
             "1 unit = 12, and 8 units = 96.", "96 stickers")
        + "<h2>Common mistakes</h2>"
        + table(["Mistake", "What to do instead"], [
            ["Taking " + fr(1, 4) + " of the whole ($60) when the question says " + fr(1, 4) + " of the remainder",
             "Find the remainder first ($40), then " + fr(1, 4) + " of $40 = $10"],
            ["Adding fractions of different wholes: " + fr(1, 3) + " + " + fr(1, 4) + " = " + fr(7, 12) + " spent",
             "Change the second fraction into a fraction of the whole: " + fr(1, 4) + " × " + fr(2, 3) + " = "
             + fr(1, 6) + ", so " + fr(1, 3) + " + " + fr(1, 6) + " = " + fr(1, 2) + " spent"],
            ["Finding one unit only and stopping (2 units = 12, so the answer is 6)",
             "Read the question again: multiply 1 unit by the number of units asked for"],
            ["Using the part used when the question gives the part left",
             "If " + fr(3, 5) + " is spent and $24 is left, then $24 is 2 units, not 3 units"],
        ])
    )


FAQ = [
    {"q": "What fraction word problems come out in the PSLE?",
     "a": "The PSLE often has fraction of a remainder, finding the whole from a part, comparing two people and "
          "before-and-after problems. Many of them are multi-step questions in Paper 2, so students should show their working."},
    {"q": "How do I teach fraction word problems with the model method?",
     "a": "Draw a bar for the whole and cut it into equal units using the denominator. Label what you know and put “?” "
          "for the unknown, then find 1 unit first."},
    {"q": "What is the most common mistake in fraction of a remainder questions?",
     "a": "Taking the fraction of the whole instead of the remainder. If Siti spent 1/3 of $60 and then 1/4 of the "
          "remainder, the second part is 1/4 of $40, not 1/4 of $60."},
    {"q": "Are fraction word problems in the MOE Primary 6 syllabus?",
     "a": "Yes. The MOE 2021 Primary Mathematics Syllabus includes solving word problems involving the four operations "
          "on fractions, and Primary 6 students use them in multi-step problems."},
]


def gen():
    rnd = random.Random(66802)
    sets = [set_quantity(), set_remainder(), set_compare(), set_whole(), set_psle()]
    balance(sets, rnd)
    seen = set()
    for s in sets:
        assert len(s["items"]) == 20, (s["title"], len(s["items"]))
        cnt = [0, 0, 0, 0]
        for it in s["items"]:
            assert len(set(it["c"])) == 4, it
            cnt[it["a"]] += 1
            assert it["q"] not in seen, it["q"]
            seen.add(it["q"])
        assert cnt == [5, 5, 5, 5], (s["title"], cnt)
    return {
        "country": "sg", "subject": "maths", "grade": "primary-6", "slug": "fraction-word-problems", "sort": 2,
        "updated": UPDATED, "pdf_url": "",
        "title": "Primary 6 Fraction Word Problems",
        "seo_title": "P6 Fraction Word Problems Worksheets: Free Primary 6 Maths with Answers (MOE Syllabus, PSLE Practice)",
        "short_title": "Fraction word problems",
        "domain": "Number and Algebra",
        "standard_code": "Primary 6: Fractions",
        "standard_url": "https://www.moe.gov.sg/primary/curriculum/syllabus",
        "standard_text": "Solving word problems involving the four operations on fractions",
        "meta_desc": "Free P6 fraction word problems for the PSLE: fraction of a remainder, finding the whole, before-and-after "
                     "and the model method. 100 questions with answers.",
        "key_big": "Always ask “a fraction of what?” Find the remainder first, then take the fraction of the remainder.",
        "key_sub": "Spent 1/3 of $60, then 1/4 of the rest: the rest is $40, so 1/4 of $40 = $10 (not 1/4 of $60).",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    mark_large(u, "bar model")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
