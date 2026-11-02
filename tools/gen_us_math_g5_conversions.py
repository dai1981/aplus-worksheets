# -*- coding: utf-8 -*-
"""
US Grade 5 Math: Measurement Conversions (5.MD.A.1)
  python3 tools/gen_us_math_g5_conversions.py
Grade 5 adds converting a SMALLER unit into a LARGER unit, with decimals and fractions:
250 cm = 2.5 m, 5 cm = 0.05 m, 30 in = 2 1/2 ft, 90 min = 1 1/2 hr.
Every measurement is checked in code with fractions.Fraction: each right answer is computed,
and no wrong choice may have the same value as the right answer (or as another choice).
Questions are written in plain text ('2 1/2 ft'); fractions become <span class='fr'> at the end.
HTML attributes use single quotes (no backslashes in the JSON).
Grade 5 style: numbers 1,000 and above are written with commas.
"""
import json, os, random, re
from decimal import Decimal as Dm
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "us", "math", "grade-5")
UPDATED = "2026-11-02"
GREEN = "#006633"
FILL2 = "#eef6f0"
RED = "#c0392b"
INK = "#2b2b2b"
FONT = "Arial, Helvetica, sans-serif"
GIRLS = ["Maya", "Ava", "Mia", "Zoe", "Lily", "Emma", "Nora", "Ruby", "Sofia", "Grace"]
BOYS = ["Leo", "Noah", "Eli", "Sam", "Ben", "Omar", "Kai", "Jack", "Luis", "Owen"]


# ------------------------------------------------------------ units
# key: (dimension, size in the base unit, singular word, plural word, abbreviation or None)
U = {
    "km": ("mlen", 1000000, "kilometer", "kilometers", "km"),
    "m": ("mlen", 1000, "meter", "meters", "m"),
    "cm": ("mlen", 10, "centimeter", "centimeters", "cm"),
    "mm": ("mlen", 1, "millimeter", "millimeters", "mm"),
    "kg": ("mass", 1000, "kilogram", "kilograms", "kg"),
    "g": ("mass", 1, "gram", "grams", "g"),
    "L": ("mcap", 1000, "liter", "liters", "L"),
    "mL": ("mcap", 1, "milliliter", "milliliters", "mL"),
    "mi": ("clen", 63360, "mile", "miles", "mi"),
    "yd": ("clen", 36, "yard", "yards", "yd"),
    "ft": ("clen", 12, "foot", "feet", "ft"),
    "in": ("clen", 1, "inch", "inches", "in"),
    "ton": ("wt", 32000, "ton", "tons", None),
    "lb": ("wt", 16, "pound", "pounds", "lb"),
    "oz": ("wt", 1, "ounce", "ounces", "oz"),
    "gal": ("ccap", 16, "gallon", "gallons", "gal"),
    "qt": ("ccap", 4, "quart", "quarts", "qt"),
    "pt": ("ccap", 2, "pint", "pints", "pt"),
    "cup": ("ccap", 1, "cup", "cups", None),
    "week": ("time", 604800, "week", "weeks", None),
    "day": ("time", 86400, "day", "days", None),
    "hr": ("time", 3600, "hour", "hours", "hr"),
    "min": ("time", 60, "minute", "minutes", "min"),
    "sec": ("time", 1, "second", "seconds", "sec"),
}
WORD2KEY = {}
for _k, (_d, _s, _sg, _pl, _ab) in U.items():
    for _w in (_k, _sg, _pl, _ab):
        if _w:
            WORD2KEY[_w] = _k


def ratio(big, small):
    r = F(U[big][1], U[small][1])
    assert r.denominator == 1 and r > 1, (big, small)
    return int(r)


# ------------------------------------------------------------ numbers
def N(x):
    """Exact decimal text, commas from 1,000: 3500 -> '3,500', 0.050 -> '0.05'."""
    x = Dm(x) if not isinstance(x, F) else Dm(x.numerator) / Dm(x.denominator)
    s = format(x.normalize(), ",f")
    return s


def fr(x):
    """Fraction as a whole or mixed number: 5/2 -> '2 1/2', 3/4 -> '3/4', 6 -> '6'."""
    x = F(x)
    w, r = divmod(x.numerator, x.denominator)
    if r == 0:
        return N(w)
    if w == 0:
        return "%d/%d" % (r, x.denominator)
    return "%s %d/%d" % (N(w), r, x.denominator)


def q(x, u, style="frac"):
    """'2 1/2 ft', '0.75 kg', '3 cups', '1 cup', '1/2 cup'. Abbreviations have no plural."""
    x = F(x) if not isinstance(x, str) else x
    num = x if isinstance(x, str) else (fr(x) if style == "frac" else N(x))
    d, s, sg, pl, ab = U[u]
    if ab:
        return "%s %s" % (num, ab)
    val = x if not isinstance(x, str) else parse_num(x)
    return "%s %s" % (num, sg if val <= 1 else pl)


def name(u, n=2):
    return U[u][2] if n == 1 else U[u][3]


def cap(s):
    return s[0].upper() + s[1:]


def fact(big, small):
    return "%s = %s" % (q(1, big), q(ratio(big, small), small))


NUM = r"(?:\d[\d,]*(?:\.\d+)?(?: \d+/\d+)?|\d+/\d+)"
PAIR = re.compile(r"(" + NUM + r") ([A-Za-z]+)")


def parse_num(s):
    s = s.replace(",", "")
    if "/" in s:
        parts = s.split(" ")
        w = F(parts[0]) if len(parts) == 2 else F(0)
        return w + F(parts[-1])
    return F(Dm(s))


def value(s):
    """'2 ft 6 in' -> ('clen', 30). Unknown words (pieces, bottles) count as their own unit.
    Plain numbers -> ('', n). Anything else (statements, lists) -> None."""
    s = s.strip()
    if re.fullmatch(NUM, s):
        return ("", parse_num(s))
    pairs = PAIR.findall(s)
    if not pairs or " ".join("%s %s" % p for p in pairs) != s:
        return None
    dims = set()
    tot = F(0)
    for n, w in pairs:
        k = WORD2KEY.get(w)
        if k is None:
            dims.add(w)
            tot += parse_num(n)
        else:
            dims.add(U[k][0])
            tot += parse_num(n) * U[k][1]
    if len(dims) != 1:
        return None
    return (dims.pop(), tot)


def side(s):
    v = value(s)
    assert v and v[0], s
    return v


def is_true(stmt):
    """'2 1/2 ft = 30 in' -> True. Checked with exact values."""
    m = re.fullmatch(r"(.+) ([=<>]) (.+)", stmt)
    a, op, b = side(m.group(1)), m.group(2), side(m.group(3))
    assert a[0] == b[0], stmt
    return {"=": a[1] == b[1], "<": a[1] < b[1], ">": a[1] > b[1]}[op]


# ------------------------------------------------------------ helpers
def mcq(qs, correct, cands, e, same_ok=False):
    """4 choices: correct + exactly 3 distractors. No two choices may have the same value
    (same_ok only for 'Which is NOT equal to ...?', where three choices are equal on purpose)."""
    ch = [correct] + list(cands)
    assert len(ch) == 4 and len(set(ch)) == 4, (qs, ch)
    if not same_ok:
        vals = [value(c) for c in ch]
        known = [v for v in vals if v is not None]
        assert len(set(known)) == len(known), (qs, ch)
    for c in ch:
        assert not c.startswith("0 ") and not c.startswith("-"), (qs, c)
    return {"q": qs, "c": ch, "a": 0, "e": e}


def balance(sets, rnd):
    """Spread the correct answers evenly over the 4 positions in every set (5 each)."""
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
        self.pool = [(n, "she", "her") for n in GIRLS] + [(n, "he", "his") for n in BOYS]
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


def text(x, y, t, fs=17, anchor="middle", col=INK):
    return ("<text x='%.1f' y='%.1f' font-size='%d' font-weight='700' fill='%s' text-anchor='%s'>%s</text>"
            % (x, y, fs, col, anchor, t))


def frac(a, b):
    return "<span class='fr'><span class='fn'>%d</span><span class='fd'>%d</span></span>" % (a, b)


FR = re.compile(r"(?<![\d/])(\d+)/(\d+)(?![\d/])")


def H(s):
    """Plain '2 1/2' -> HTML stacked fraction."""
    return FR.sub(lambda m: frac(int(m.group(1)), int(m.group(2))), s)


# ------------------------------------------------------------ figure: two-column table
def svg_num(cx, cy, x, fs=18, col=INK):
    """A number in a table cell, centered on (cx, cy). Fractions are drawn stacked."""
    if isinstance(x, Dm):
        return text(cx, cy + fs * 0.35, N(x), fs, col=col)
    x = F(x)
    w, r = divmod(x.numerator, x.denominator)
    if r == 0:
        return text(cx, cy + fs * 0.35, N(x), fs, col=col)
    d = x.denominator
    ffs = 16
    fw = 13 if max(r, d) < 10 else 22          # width of the fraction part
    ws = N(w) if w else ""
    ww = len(ws) * fs * 0.56 + (4 if ws else 0)
    left = cx - (ww + fw) / 2.0
    o = []
    if ws:
        o.append(text(left, cy + fs * 0.35, ws, fs, "start", col))
    fx = left + ww + fw / 2.0
    o.append(text(fx, cy - 3, str(r), ffs, col=col))
    o.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='1.6'/>"
             % (fx - fw / 2.0 - 1, cy + 1, fx + fw / 2.0 + 1, cy + 1, col))
    o.append(text(fx, cy + 17, str(d), ffs, col=col))
    return "".join(o)


def conv_table(small, big, rows, miss):
    """Two-column table: the smaller unit on the left, the larger unit on the right.
    rows = [(small value, big value)]; miss = row whose right cell is a red ?."""
    for a, b in rows:
        assert F(a) * U[small][1] == F(b) * U[big][1], (a, b)
    has_fr = any(isinstance(b, F) and b.denominator != 1 for a, b in rows)
    CW, HH = 132, 34
    RH = 46 if has_fr else 32
    W = CW * 2 + 4
    H = HH + RH * len(rows) + 4
    o = ["<rect x='2' y='2' width='%d' height='%d' fill='%s'/>" % (CW * 2, HH, GREEN)]
    for c, u in enumerate([small, big]):
        o.append(text(2 + CW * c + CW / 2.0, 2 + HH / 2.0 + 6, cap(U[u][3]), 16, col="#ffffff"))
    for r, row in enumerate(rows):
        y = 2 + HH + RH * r
        cy = y + RH / 2.0
        o.append("<rect x='2' y='%d' width='%d' height='%d' fill='%s'/>" % (y, CW * 2, RH, FILL2 if r % 2 else "#ffffff"))
        for c, v in enumerate(row):
            cx = 2 + CW * c + CW / 2.0
            if c == 1 and r == miss:
                o.append("<rect x='%.1f' y='%.1f' width='60' height='26' rx='4' fill='none' stroke='%s' stroke-width='2' "
                         "stroke-dasharray='5 3'/>" % (cx - 30, cy - 13, RED))
                o.append(text(cx, cy + 6.5, "?", 18, col=RED))
            else:
                o.append(svg_num(cx, cy, v))
    for r in range(len(rows) - 1):
        y = 2 + HH + RH * (r + 1)
        o.append("<line x1='2' y1='%d' x2='%d' y2='%d' stroke='#b9d6c2' stroke-width='1'/>" % (y, 2 + CW * 2, y))
    o.append("<line x1='%d' y1='2' x2='%d' y2='%d' stroke='%s' stroke-width='2'/>" % (2 + CW, 2 + CW, H - 2, GREEN))
    o.append("<rect x='2' y='2' width='%d' height='%d' fill='none' stroke='%s' stroke-width='2.5'/>" % (CW * 2, H - 4, GREEN))
    return svg_wrap(W, H, "".join(o), "conversion table: %s and %s" % (U[small][3], U[big][3]))


# ------------------------------------------------------------ explanations
def places_word(k):
    return "%d place%s" % (k, "" if k == 1 else "s")


def metric_e(x, a, b):
    """Explain a metric conversion (powers of 10)."""
    x = Dm(x)
    if U[a][1] > U[b][1]:
        k = ratio(a, b)
        p = len(str(k)) - 1
        ans = x * k
        return ("%s. %s are bigger than %s, so there will be <b>more</b> %s: multiply by %s. "
                "The point moves %s right: %s × %s = %s, so %s = <b>%s</b>."
                % (fact(a, b), cap(name(a)), name(b), name(b), N(k), places_word(p), N(x), N(k), N(ans),
                   q(x, a, "dec"), q(ans, b, "dec")))
    k = ratio(b, a)
    p = len(str(k)) - 1
    ans = x / k
    return ("%s. %s are bigger than %s, so there will be <b>fewer</b> of them: divide by %s. "
            "The point moves %s left: %s ÷ %s = %s, so %s = <b>%s</b>."
            % (fact(b, a), cap(name(b)), name(a), N(k), places_word(p), N(x), N(k), N(ans),
               q(x, a, "dec"), q(ans, b, "dec")))


def up_e(x, a, b, extra=""):
    """Smaller unit -> larger unit with a fraction: 30 in -> 2 1/2 ft."""
    k = ratio(b, a)
    x = F(x)
    ans = x / k
    w, r = divmod(int(x), k)
    s = "%s. %s are bigger, so divide: %s ÷ %s" % (fact(b, a), cap(name(b)), N(x), N(k))
    if r == 0:
        s += " = %s, so %s = <b>%s</b>." % (N(w), q(x, a), q(ans, b))
    else:
        part = F(r, k)
        red = "" if part.denominator == k else " = %s" % fr(part)
        if w:
            s += " = %s R%d. The %s %s left over %s %d/%d of %s%s, so %s = <b>%s</b>." % (
                N(w), r, N(r), name(a, r), "is" if r == 1 else "are", r, k, ("a " + name(b, 1)) if b != "hr" else "an hour", red, q(x, a), q(ans, b))
        else:
            s += ". %s is %d/%d of %s%s, so %s = <b>%s</b>." % (
                q(x, a), r, k, ("a " + name(b, 1)) if b != "hr" else "an hour", red, q(x, a), q(ans, b))
    return s + (" " + extra if extra else "")


def down_e(x, a, b, extra=""):
    """Larger unit -> smaller unit with a fraction: 3 1/2 ft -> 42 in."""
    k = ratio(a, b)
    x = F(x)
    ans = x * k
    w = int(x)
    part = x - w
    s = "%s. %s are smaller, so multiply: " % (fact(a, b), cap(name(b)))
    if part == 0:
        s += "%s × %s = %s, so %s = <b>%s</b>." % (N(w), N(k), N(ans), q(x, a), q(ans, b))
    elif w == 0 and part.numerator == 1:
        s += "%s of %s = %s ÷ %d = %s, so %s = <b>%s</b>." % (
            fr(part), N(k), N(k), part.denominator, N(ans), q(x, a), q(ans, b))
    elif w == 0:
        s += "%s of %s = %s ÷ %d × %d = %s, so %s = <b>%s</b>." % (
            fr(part), N(k), N(k), part.denominator, part.numerator, N(ans), q(x, a), q(ans, b))
    else:
        s += "%s × %s = %s, and %s of %s = %s. %s + %s = %s, so %s = <b>%s</b>." % (
            N(w), N(k), N(w * k), fr(part), N(k), N(part * k), N(w * k), N(part * k), N(ans), q(x, a), q(ans, b))
    return s + (" " + extra if extra else "")


# ------------------------------------------------------------ set 1: metric
def metric_item(x, a, b, wrong=None):
    x = Dm(x)
    if U[a][1] > U[b][1]:
        k = ratio(a, b)
        ans = x * k
        cands = [x / k, ans / 10, ans * 10]          # divided instead; one place too few / too many
    else:
        k = ratio(b, a)
        ans = x / k
        cands = [x * k, ans * 10, ans / 10]          # multiplied instead; one place too few / too many
    cands = wrong or cands
    qs = "Convert. <b>%s = ☐ %s</b>" % (q(x, a, "dec"), b)
    return mcq(qs, q(ans, b, "dec"), [q(v, b, "dec") for v in cands], metric_e(x, a, b))


def set_metric():
    down = [("3.5", "km", "m"), ("4.2", "m", "cm"), ("0.6", "kg", "g"), ("1.25", "L", "mL"),
            ("0.8", "cm", "mm"), ("2.75", "m", "mm"), ("0.4", "m", "cm")]
    up = [("250", "cm", "m"), ("5", "cm", "m"), ("750", "g", "kg"), ("3200", "m", "km"),
          ("600", "mL", "L"), ("45", "mm", "cm"), ("80", "g", "kg"), ("1500", "mL", "L"), ("350", "mm", "m")]
    its = [metric_item(*t) for t in down[:4]] + [metric_item(*t) for t in up[:4]]
    its += [metric_item(*t) for t in down[4:]] + [metric_item(*t) for t in up[4:]]
    its.append(mcq("To change 2,400 g to kilograms, what do you do?", "Divide by 1,000",
                   ["Multiply by 1,000", "Divide by 100", "Multiply by 100"],
                   "1 kg = 1,000 g. A kilogram is bigger than a gram, so there will be fewer kilograms: "
                   "<b>divide by 1,000</b>. 2,400 ÷ 1,000 = 2.4, so 2,400 g = 2.4 kg."))
    its.append(mcq("You change 6.8 m to centimeters. How does the decimal point move?", "2 places right",
                   ["2 places left", "3 places right", "1 place right"],
                   "1 m = 100 cm, so multiply by 100. 100 has 2 zeros, and multiplying makes the number bigger, "
                   "so the point moves <b>2 places right</b>: 6.8 m = 680 cm."))
    rows = [(50, Dm("0.5")), (100, Dm("1")), (150, Dm("1.5")), (275, Dm("2.75"))]
    its.append(table_item("cm", "m", rows, 3, "dec",
                          ["27.5", "0.275", "27,500"],
                          "1 m = 100 cm, so every number on the right is the left number ÷ 100. "
                          "275 ÷ 100 = <b>2.75</b> (the point moves 2 places left)."))
    rows = [(250, Dm("0.25")), (500, Dm("0.5")), (1000, Dm("1")), (1750, Dm("1.75"))]
    its.append(table_item("g", "kg", rows, 3, "dec",
                          ["17.5", "0.175", "1,750,000"],
                          "1 kg = 1,000 g, so every number on the right is the left number ÷ 1,000. "
                          "1,750 ÷ 1,000 = <b>1.75</b> (the point moves 3 places left)."))
    # easy -> hard: decimals to a smaller unit, then to a larger unit, then the harder ones
    order = [0, 1, 2, 3, 4, 5, 6, 7, 16, 18, 8, 9, 10, 17, 11, 12, 13, 14, 15, 19]
    its = [its[i] for i in order]
    assert len(its) == 20
    return {"title": "Metric units: multiply or divide by 10, 100, 1,000", "items": its}


def table_item(small, big, rows, miss, style, wrong, e):
    ans = rows[miss][1]
    right = N(ans) if style == "dec" else fr(ans)
    return mcq(fig(conv_table(small, big, rows, miss)) + "What number goes in the ? box?", right, wrong, e)


# ------------------------------------------------------------ set 2: customary length and weight
def conv_q(x, a, b):
    return "Convert. <b>%s = ☐ %s</b>" % (q(x, a), U[b][4] or name(b))


def set_customary():
    its = []

    def down(x, a, b, wrong, note=""):
        x = F(x)
        its.append(mcq(conv_q(x, a, b), q(x * ratio(a, b), b), wrong, down_e(x, a, b, note)))

    def up(x, a, b, wrong, note=""):
        x = F(x)
        its.append(mcq(conv_q(x, a, b), q(x / ratio(b, a), b), wrong, up_e(x, a, b, note)))

    down(4, "yd", "ft", ["48 ft", "1 1/3 ft", "7 ft"], "(48 uses 12, the inches in a foot.)")
    up(9, "ft", "yd", ["27 yd", "3/4 yd", "6 yd"], "(27 multiplies instead of dividing.)")
    down(F(7, 2), "ft", "in", ["35 in", "38 in", "36 in"],
         "(36 in forgets the half foot, and 35 in uses 10 instead of 12.)")
    down(2, "mi", "ft", ["5,282 ft", "3,520 ft", "2,640 ft"],
         "(2,640 divides instead of multiplying, and 3,520 is the number of yards in 2 miles.)")
    up(30, "in", "ft", ["3 ft", "2.6 ft", "360 ft"],
       "(3 ft divides by 10. 2.6 ft is a mistake for 2 ft 6 in: 6 inches is half a foot, not 0.6 of a foot.)")
    up(40, "oz", "lb", ["4 lb", "2.8 lb", "640 lb"],
       "(4 lb divides by 10. 2.8 lb is a mistake for 2 lb 8 oz: 8 oz is half a pound, not 0.8 of a pound.)")
    up(8, "oz", "lb", ["0.8 lb", "2 lb", "128 lb"],
       "(2 lb divides 16 by 8, the wrong way round.)")
    up(18, "in", "ft", ["1.8 ft", "216 ft", "6 ft"],
       "(6 ft divides by 3, the feet in a yard.)")
    down(F(11, 4), "lb", "oz", ["32 oz", "35 oz", "27.5 oz"],
         "(32 oz forgets the 3/4 pound, and 27.5 oz uses 10 instead of 16.)")
    up(4000, "lb", "ton", ["4 tons", "250 tons", "8,000,000 tons"],
       "(4 tons divides by 1,000, and 250 tons divides by 16, the ounces in a pound.)")
    down(F(3, 2), "ton", "lb", ["1,500 lb", "2,500 lb", "24 lb"],
         "(1,500 lb uses 1,000 instead of 2,000, and 24 lb uses 16, the ounces in a pound.)")
    its.append(mcq(conv_q(2640, "ft", "mi"), "1/2 mi", ["2 mi", "880 mi", "2.64 mi"],
                   "1 mi = 5,280 ft. Miles are bigger, so divide: 2,640 ÷ 5,280. 2,640 is half of 5,280, "
                   "so 2,640 ft = <b>1/2 mi</b>. (2 mi divides 5,280 by 2,640, the wrong way round. 2.64 mi divides by 1,000.)"))
    down(F(1, 4), "mi", "ft", ["21,120 ft", "440 ft", "2,640 ft"],
         "(21,120 multiplies by 4 instead of finding one fourth, and 2,640 ft is half a mile.)")
    down(F(10, 3), "yd", "ft", ["9 1/3 ft", "40 ft", "9 ft"],
         "(9 1/3 ft forgets to multiply the 1/3 by 3.)")
    up(75, "in", "ft", ["7.5 ft", "6.3 ft", "6 1/3 ft"],
       "(7.5 ft divides by 10. 6.3 ft and 6 1/3 ft both treat the 3 leftover inches as 3 tenths or 1 third of a foot.)")
    # mixed units
    its.append(mcq("Convert. <b>4 ft 9 in = ☐ in</b>", "57 in", ["49 in", "48 in", "13 in"],
                   "1 ft = 12 in, so 4 ft = 4 × 12 = 48 in. Add the leftover inches: 48 + 9 = <b>57 in</b>. "
                   "(49 in uses 10 instead of 12, and 48 in forgets the 9 inches.)"))
    its.append(mcq("Convert. <b>6 lb 5 oz = ☐ oz</b>", "101 oz", ["65 oz", "96 oz", "77 oz"],
                   "1 lb = 16 oz, so 6 lb = 6 × 16 = 96 oz. Add the leftover ounces: 96 + 5 = <b>101 oz</b>. "
                   "(65 oz writes the digits side by side, and 77 oz uses 12 instead of 16.)"))
    its.append(mcq("Convert. <b>1 yd 2 ft = ☐ in</b>", "60 in", ["36 in", "38 in", "5 in"],
                   "1 yd = 3 ft, so 1 yd 2 ft = 3 + 2 = 5 ft. 1 ft = 12 in, so 5 ft = 5 × 12 = <b>60 in</b>. "
                   "(36 in forgets the 2 feet, and 38 in adds 2 inches instead of 2 feet.)"))
    its.append(mcq("Convert. <b>42 in = ☐ ft ☐ in</b>", "3 ft 6 in", ["4 ft 2 in", "3.6 ft", "6 ft 3 in"],
                   "1 ft = 12 in. 42 ÷ 12 = 3 R6: 3 whole feet and 6 inches left over, so 42 in = <b>3 ft 6 in</b>. "
                   "Check: 36 + 6 = 42. (4 ft 2 in divides by 10.)"))
    its.append(mcq("Convert. <b>52 oz = ☐ lb ☐ oz</b>", "3 lb 4 oz", ["5 lb 2 oz", "3.4 lb", "4 lb 4 oz"],
                   "1 lb = 16 oz. 52 ÷ 16 = 3 R4: 3 whole pounds and 4 ounces left over, so 52 oz = <b>3 lb 4 oz</b>. "
                   "Check: 48 + 4 = 52. (5 lb 2 oz divides by 10, and 4 lb 4 oz uses 12 instead of 16.)"))
    assert len(its) == 20
    # easy -> hard: whole-number facts, fractions, then mixed units
    order = [0, 1, 2, 3, 4, 5, 15, 6, 7, 8, 16, 9, 10, 17, 18, 11, 12, 13, 19, 14]
    its = [its[i] for i in order]
    return {"title": "Customary length and weight: fractions and mixed units", "items": its}


# ------------------------------------------------------------ set 3: capacity and time
def set_capacity_time():
    its = []

    def down(x, a, b, wrong, note=""):
        x = F(x)
        its.append(mcq(conv_q(x, a, b), q(x * ratio(a, b), b), wrong, down_e(x, a, b, note)))

    def up(x, a, b, wrong, note=""):
        x = F(x)
        its.append(mcq(conv_q(x, a, b), q(x / ratio(b, a), b), wrong, up_e(x, a, b, note)))

    down(3, "qt", "pt", ["12 pt", "1 1/2 pt", "5 pt"],
         "(12 pt uses 4, the quarts in a gallon, and 1 1/2 pt divides instead of multiplying.)")
    up(6, "cup", "pt", ["12 pt", "1 1/2 pt", "4 pt"],
       "(12 pt multiplies instead of dividing, and 1 1/2 pt divides by 4, the cups in a quart.)")
    up(12, "qt", "gal", ["48 gal", "6 gal", "1 1/2 gal"],
       "(48 gal multiplies instead of dividing, and 6 gal divides by 2, the pints in a quart.)")
    down(2, "gal", "qt", ["1/2 qt", "4 qt", "16 qt"],
         "(4 qt multiplies by 2 instead of 4, and 16 is the number of pints in 2 gallons.)")
    up(5, "pt", "qt", ["10 qt", "1 1/4 qt", "2 1/4 qt"],
       "(1 1/4 qt divides by 4, and 2 1/4 qt treats the leftover pint as 1/4 quart.)")
    up(10, "qt", "gal", ["40 gal", "2.2 gal", "5 gal"],
       "(2.2 gal is a mistake for 2 gal 2 qt: 2 quarts is half a gallon, not 0.2 of a gallon.)")
    its.append(mcq("Convert. <b>1/2 gal = ☐ cups</b>", "8 cups", ["2 cups", "4 cups", "32 cups"],
                   "1 gal = 4 qt and 1 qt = 4 cups, so 1 gal = 16 cups. Half of 16 is <b>8 cups</b>. "
                   "(2 cups is the number of quarts in 1/2 gallon, and 32 cups doubles instead of halving.)"))
    its.append(mcq("Convert. <b>3 gal 2 qt = ☐ qt</b>", "14 qt", ["32 qt", "12 qt", "8 qt"],
                   "1 gal = 4 qt, so 3 gal = 3 × 4 = 12 qt. Add the leftover quarts: 12 + 2 = <b>14 qt</b>. "
                   "(32 qt writes the digits side by side, and 8 qt uses 2 instead of 4.)"))
    up(3, "cup", "qt", ["12 qt", "1 1/2 qt", "6 qt"],
       "(12 qt multiplies instead of dividing, and 1 1/2 qt divides by 2, the cups in a pint.)")
    # time
    up(90, "min", "hr", ["9 hr", "0.9 hr", "1.3 hr"],
       "(9 hr divides by 10 and 0.9 hr divides by 100. 1.3 hr is a mistake for 1 hr 30 min.)")
    its.append(mcq("Which is the same as 1.5 hours?", "1 hr 30 min", ["1 hr 50 min", "1 hr 5 min", "150 min"],
                   "1.5 hours is 1 hour and half an hour. Half of 60 minutes is 30 minutes, so 1.5 hr = <b>1 hr 30 min</b> "
                   "= 90 min. The .5 means one half, not 50 minutes: an hour has 60 minutes, not 100."))
    up(45, "min", "hr", ["0.45 hr", "4 1/2 hr", "2,700 hr"],
       "(0.45 hr divides by 100, and 2,700 hr multiplies instead of dividing.)")
    up(150, "sec", "min", ["1.5 min", "2.3 min", "9,000 min"],
       "(1.5 min divides by 100. 2.3 min is a mistake for 2 min 30 sec.)")
    down(F(9, 4), "hr", "min", ["225 min", "124 min", "120 min"],
         "(225 min uses 100 instead of 60, and 120 min forgets the 1/4 hour.)")
    its.append(mcq("Convert. <b>0.25 hr = ☐ min</b>", "15 min", ["25 min", "2.5 min", "240 min"],
                   "0.25 = 1/4. 1 hr = 60 min, and 1/4 of 60 = 60 ÷ 4 = <b>15 min</b>. "
                   "(25 min reads the decimal as minutes, and 240 min divides 60 by 0.25.)"))
    up(36, "hr", "day", ["3 days", "1.2 days", "864 days"],
       "(3 days divides by 12. 1.2 days is a mistake for 1 day 12 hours.)")
    its.append(mcq("Convert. <b>200 min = ☐ hr ☐ min</b>", "3 hr 20 min", ["2 hr", "3.2 hr", "20 hr"],
                   "1 hr = 60 min. 200 ÷ 60 = 3 R20: 3 whole hours and 20 minutes left over, so 200 min = <b>3 hr 20 min</b>. "
                   "Check: 180 + 20 = 200. (2 hr uses 100 minutes in an hour.)"))
    its.append(mcq("Which is the same as 3 1/4 hours?", "3 hr 15 min", ["3 hr 25 min", "3 hr 4 min", "325 min"],
                   "1/4 of an hour is 60 ÷ 4 = 15 minutes, so 3 1/4 hr = <b>3 hr 15 min</b> = 195 min. "
                   "(3 hr 25 min reads 1/4 as 0.25, and 3 hr 4 min uses the 4 from the fraction.)"))
    rows = [(2, F(1, 2)), (6, F(3, 2)), (10, F(5, 2))]
    its.append(table_item("qt", "gal", rows, 2, "frac", ["40", "5", "2.2"],
                          "1 gal = 4 qt, so every number on the right is the left number ÷ 4. "
                          "10 ÷ 4 = 2 R2, and 2 quarts is 2/4 = 1/2 gallon, so the answer is <b>2 1/2</b>. "
                          "(5 divides by 2, and 2.2 is a mistake for 2 gal 2 qt.)"))
    rows = [(30, F(1, 2)), (90, F(3, 2)), (105, F(7, 4))]
    its.append(table_item("min", "hr", rows, 2, "frac", ["1.05", "10 1/2", "6,300"],
                          "1 hr = 60 min, so every number on the right is the left number ÷ 60. "
                          "105 ÷ 60 = 1 R45, and 45 minutes is 45/60 = 3/4 of an hour, so the answer is <b>1 3/4</b>. "
                          "(1.05 divides by 100, 10 1/2 divides by 10, and 6,300 multiplies instead of dividing.)"))
    assert len(its) == 20
    # easy -> hard: capacity, then time, tables and mixed units mixed in
    order = [0, 1, 3, 2, 6, 7, 4, 5, 18, 8, 9, 10, 11, 14, 12, 13, 19, 15, 16, 17]
    its = [its[i] for i in order]
    return {"title": "Capacity and time: cups, pints, quarts, gallons, hours", "items": its}


# ------------------------------------------------------------ set 4: compare and order
def set_compare():
    its = []

    def which(qs, ch, fn, how):
        vals = [side(c)[1] for c in ch]
        assert len(set(vals)) == 4, ch
        best = fn(range(4), key=lambda j: vals[j])
        u = how[0]
        conv = how[1]
        order = sorted(range(4), key=lambda j: vals[j], reverse=(fn is max))
        unit_vals = [q(vals[j] / U[u][1], u, "dec") for j in order]
        e = ("Change everything to %s: %s. In order: %s. So the answer is <b>%s</b>."
             % (name(u), conv, ", ".join(unit_vals), ch[best]))
        its.append(mcq(qs, ch[best], [c for j, c in enumerate(ch) if j != best], e))

    which("Which is the longest?", ["1.2 m", "98 cm", "1,150 mm", "1 m 25 cm"], max,
          ("cm", "1.2 m = 120 cm, 1,150 mm = 115 cm and 1 m 25 cm = 125 cm"))
    which("Which is the heaviest?", ["0.8 kg", "750 g", "0.09 kg", "820 g"], max,
          ("g", "0.8 kg = 800 g and 0.09 kg = 90 g (not 900 g)"))
    which("Which holds the least?", ["0.5 L", "450 mL", "0.05 L", "120 mL"], min,
          ("mL", "0.5 L = 500 mL and 0.05 L = 50 mL"))
    which("Which is the lightest?", ["1.05 kg", "1,100 g", "1.5 kg", "1,010 g"], min,
          ("g", "1.05 kg = 1,050 g and 1.5 kg = 1,500 g"))
    which("Which is the longest?", ["2 1/2 ft", "28 in", "1 yd", "2 ft 8 in"], max,
          ("in", "2 1/2 ft = 24 + 6 = 30 in, 1 yd = 36 in and 2 ft 8 in = 24 + 8 = 32 in"))
    which("Which is the heaviest?", ["2 1/4 lb", "35 oz", "2 lb 5 oz", "34 oz"], max,
          ("oz", "2 1/4 lb = 32 + 4 = 36 oz and 2 lb 5 oz = 32 + 5 = 37 oz"))
    which("Which holds the most?", ["3 qt", "5 pt", "1 gal", "14 cups"], max,
          ("cup", "3 qt = 12 cups, 5 pt = 10 cups and 1 gal = 16 cups"))
    which("Which is the longest amount of time?", ["1 1/2 hr", "100 min", "1 hr 35 min", "1 3/4 hr"], max,
          ("min", "1 1/2 hr = 90 min, 1 hr 35 min = 95 min and 1 3/4 hr = 60 + 45 = 105 min"))
    which("Which is the shortest distance?", ["1/2 mi", "2,500 ft", "900 yd", "3,000 ft"], min,
          ("ft", "1/2 mi = 5,280 ÷ 2 = 2,640 ft and 900 yd = 900 × 3 = 2,700 ft"))

    def order(qs, items, rev, how):
        vals = [side(c)[1] for c in items]
        assert len(set(vals)) == 3
        srt = sorted(items, key=lambda c: side(c)[1], reverse=rev)
        right = ", ".join(srt)
        perms = [srt[::-1], [srt[1], srt[0], srt[2]], [srt[0], srt[2], srt[1]]]
        wrong = [", ".join(p) for p in perms]
        e = "Change them to the same unit: %s. So the order is <b>%s</b>." % (how, right)
        its.append(mcq(qs, right, wrong, e))

    order("Which list goes from least to greatest?", ["0.5 m", "6 cm", "8 mm"], False,
          "0.5 m = 500 mm and 6 cm = 60 mm, and 8 &lt; 60 &lt; 500. The biggest number is not always the longest length")
    order("Which list goes from least to greatest?", ["16 in", "1 1/4 ft", "1 ft 1 in"], False,
          "1 1/4 ft = 12 + 3 = 15 in and 1 ft 1 in = 12 + 1 = 13 in, and 13 &lt; 15 &lt; 16")
    order("Which list goes from greatest to least?", ["110 min", "1 3/4 hr", "2 hr"], True,
          "2 hr = 120 min and 1 3/4 hr = 60 + 45 = 105 min, and 120 &gt; 110 &gt; 105")

    def true_one(right, wrong, e):
        assert is_true(right), right
        for w in wrong:
            assert not is_true(w), w
        its.append(mcq("Which is true?", right, wrong, e))

    true_one("7 cm = 0.07 m", ["7 cm = 0.7 m", "7 mm = 0.07 m", "70 cm = 7 m"],
             "1 m = 100 cm, so 7 cm = 7 ÷ 100 = <b>0.07 m</b>. 7 mm is only 0.007 m, and 70 cm = 0.7 m.")
    true_one("2 1/2 ft = 30 in", ["2 1/2 ft = 25 in", "2 1/2 ft = 2 ft 5 in", "30 in = 3 ft"],
             "2 ft = 24 in, and 1/2 ft = 6 in, so <b>2 1/2 ft = 30 in</b>. Half a foot is 6 inches, not 5, "
             "and 30 in is not 3 ft because 1 ft = 12 in, not 10.")
    true_one("2.5 hr = 150 min", ["2.5 hr = 250 min", "2.5 hr = 2 hr 50 min", "150 min = 1.5 hr"],
             "2.5 hr = 2 hours and half an hour = 120 + 30 = <b>150 min</b>. The .5 is one half of 60 minutes, "
             "which is 30 minutes, not 50.")
    true_one("3 pt > 1 qt", ["3 pt < 1 qt", "3 pt = 1 1/2 gal", "6 cups > 2 qt"],
             "1 qt = 2 pt, so 3 pt is more than 1 qt: <b>3 pt &gt; 1 qt</b>. 3 pt is only 3/8 gal, "
             "and 2 qt = 8 cups, which is more than 6 cups.")
    true_one("0.6 kg < 650 g", ["0.6 kg > 650 g", "0.6 kg = 60 g", "650 g = 6.5 kg"],
             "0.6 kg = 0.6 × 1,000 = 600 g, and 600 g &lt; 650 g, so <b>0.6 kg &lt; 650 g</b>. "
             "650 g = 0.65 kg, not 6.5 kg.")
    true_one("3/4 lb = 12 oz", ["3/4 lb = 7.5 oz", "3/4 lb = 75 oz", "12 oz > 1 lb"],
             "1 lb = 16 oz. 1/4 of 16 is 4, so 3/4 of 16 is 3 × 4 = 12. <b>3/4 lb = 12 oz</b>, "
             "which is less than 1 lb.")
    # Which is NOT equal: three choices are equal on purpose; check that exactly one is different
    for target, ch, e in [
        ("2 qt", ["6 cups", "1/2 gal", "4 pt", "8 cups"],
         "1 qt = 2 pt = 4 cups, so 2 qt = 4 pt = 8 cups. 1 gal = 4 qt, so 1/2 gal = 2 qt too. "
         "<b>6 cups</b> is only 1 1/2 qt."),
        ("1.5 m", ["1 m 5 cm", "150 cm", "1,500 mm", "1 m 50 cm"],
         "1.5 m = 150 cm = 1,500 mm = 1 m 50 cm. <b>1 m 5 cm</b> is only 105 cm: the .5 means 50 cm, not 5 cm."),
    ]:
        t = side(target)
        assert side(ch[0]) != t and all(side(c) == t for c in ch[1:]), ch
        its.append(mcq("Which is NOT equal to %s?" % target, ch[0], ch[1:], e, same_ok=True))
    assert len(its) == 20
    order_ = [0, 1, 2, 3, 12, 13, 9, 4, 5, 14, 6, 7, 15, 16, 10, 17, 18, 11, 8, 19]
    its = [its[i] for i in order_]
    return {"title": "Compare and order measurements", "items": its}


# ------------------------------------------------------------ set 5: multi-step word problems
def set_story(rnd):
    P = People(rnd)
    its = []

    def add(qs, r, w, e):
        its.append(mcq(qs, r, w, e))

    n, he, his = P.next()
    add("%s has a ribbon 2 m long. %s cuts it into pieces that are 25 cm long. How many pieces does %s get?" % (n, cap(he), he),
        "8 pieces", ["80 pieces", "50 pieces", "4 pieces"],
        "Use the same unit: 2 m = 200 cm. 200 ÷ 25 = <b>8 pieces</b>. (80 uses 1 m = 1,000 cm, 50 multiplies 2 × 25, "
        "and 4 uses only 1 m.)")
    add("A store sells rice in 750 g bags. What is the total mass of 6 bags in kilograms?",
        "4.5 kg", ["45 kg", "0.45 kg", "4,500 kg"],
        "Step 1: 6 × 750 = 4,500 g. Step 2: 1 kg = 1,000 g, so divide: 4,500 ÷ 1,000 = <b>4.5 kg</b>. "
        "(4,500 kg forgets to convert.)")
    n, he, his = P.next()
    add("A track is 400 m around. %s runs 12 laps. How many kilometers does %s run?" % (n, he),
        "4.8 km", ["48 km", "0.48 km", "4,800 km"],
        "Step 1: 12 × 400 = 4,800 m. Step 2: 1 km = 1,000 m, so 4,800 ÷ 1,000 = <b>4.8 km</b>.")
    add("A snail moves 5 cm each minute. How many meters does it move in 1 hour?",
        "3 m", ["30 m", "0.3 m", "300 m"],
        "Step 1: 1 hr = 60 min, so 60 × 5 = 300 cm. Step 2: 1 m = 100 cm, so 300 ÷ 100 = <b>3 m</b>. "
        "(300 m forgets to convert.)")
    add("A cooler holds 3 gal of water. How many 1-pint bottles can be filled from it?",
        "24 bottles", ["6 bottles", "12 bottles", "48 bottles"],
        "1 gal = 4 qt and 1 qt = 2 pt, so 1 gal = 8 pt. 3 × 8 = <b>24 bottles</b>. "
        "(12 counts quarts, and 48 counts cups.)")
    n, he, his = P.next()
    add("A recipe uses 3/4 cup of milk. %s makes 4 batches. How many pints of milk does %s need?" % (n, he),
        "1 1/2 pt", ["6 pt", "3 pt", "3/4 pt"],
        "Step 1: 4 × 3/4 = 12/4 = 3 cups. Step 2: 2 cups = 1 pt, so 3 ÷ 2 = <b>1 1/2 pt</b>. "
        "(3 pt forgets to convert, and 6 pt multiplies by 2 instead of dividing.)")
    add("Lemonade is made with 10 qt of water and 6 pt of juice. How many gallons of lemonade is that?",
        "3 1/4 gal", ["4 gal", "13 gal", "2 1/2 gal"],
        "Step 1: 6 pt = 6 ÷ 2 = 3 qt, so the total is 10 + 3 = 13 qt. Step 2: 4 qt = 1 gal, so 13 ÷ 4 = 3 R1 = "
        "<b>3 1/4 gal</b>. (4 gal adds 10 + 6 without changing pints to quarts, and 13 gal forgets to change quarts to gallons.)")
    n, he, his = P.next()
    add("%s has a 5 m rope. %s cuts off 3 pieces that are each 85 cm long. How many meters of rope are left?" % (n, cap(he)),
        "2.45 m", ["4.15 m", "2.55 m", "4.745 m"],
        "Step 1: 3 × 85 = 255 cm = 2.55 m cut off. Step 2: 5 − 2.55 = <b>2.45 m</b>. "
        "(2.55 m is the part cut off, 4.15 m subtracts only one piece, and 4.745 m treats 255 cm as 0.255 m.)")
    n, he, his = P.next()
    add("%s has a 1.5 L bottle of water. %s drinks 350 mL in the morning and 0.4 L in the afternoon. "
        "How many milliliters are left?" % (n, cap(he)),
        "750 mL", ["1,146 mL", "1,100 mL", "1,150 mL"],
        "Use mL: 1.5 L = 1,500 mL and 0.4 L = 400 mL. 350 + 400 = 750 mL, and 1,500 − 750 = <b>750 mL</b>. "
        "(1,146 mL treats 0.4 L as 4 mL.)")
    n, he, his = P.next()
    add("A movie is 2 1/4 hours long. %s has watched 85 minutes. How many minutes are left?" % n,
        "50 min", ["60 min", "140 min", "35 min"],
        "Step 1: 2 1/4 hr = 120 + 15 = 135 min. Step 2: 135 − 85 = <b>50 min</b>. "
        "(60 min reads 2 1/4 hr as 2 hr 25 min, and 35 min forgets the 1/4 hour.)")
    add("A puppy weighed 3 lb when it was born. Now it weighs 10 lb 8 oz. How many ounces has it gained?",
        "120 oz", ["78 oz", "112 oz", "168 oz"],
        "Step 1: 10 lb 8 oz − 3 lb = 7 lb 8 oz. Step 2: 7 × 16 = 112, and 112 + 8 = <b>120 oz</b>. "
        "(78 oz uses 10 ounces in a pound, and 168 oz is the puppy's weight now.)")
    add("A shelf is 3 ft long. Each book on it is 1 1/2 in thick. How many books fit on the shelf?",
        "24 books", ["2 books", "54 books", "20 books"],
        "Step 1: 3 ft = 3 × 12 = 36 in. Step 2: 36 ÷ 1 1/2 = <b>24 books</b> (2 books fill 3 inches, and 36 ÷ 3 × 2 = 24). "
        "(2 books forgets to change feet to inches, and 20 uses 10 inches in a foot.)")
    add("A baker has 3 bags of flour. Each bag holds 2.5 kg. A loaf of bread uses 500 g. How many loaves can the baker make?",
        "15 loaves", ["5 loaves", "150 loaves", "1 1/2 loaves"],
        "Step 1: 3 × 2.5 = 7.5 kg = 7,500 g. Step 2: 7,500 ÷ 500 = <b>15 loaves</b>. "
        "(5 loaves uses only 1 bag, and 150 loaves changes 7.5 kg to 75,000 g instead of 7,500 g, and 1 1/2 loaves changes 2.5 kg to 250 g.)")
    add("Punch is made with 1 qt of orange juice, 3 pt of apple juice and 6 cups of ginger ale. How many cups of punch is that?",
        "16 cups", ["10 cups", "14 cups", "22 cups"],
        "Change to cups: 1 qt = 4 cups and 3 pt = 3 × 2 = 6 cups. 4 + 6 + 6 = <b>16 cups</b>, which is exactly 1 gal. "
        "(10 adds the numbers without converting.)")
    n, he, his = P.next()
    add("%s practices soccer for 1 hr 45 min, 4 days a week. How long does %s practice each week?" % (n, he),
        "7 hr", ["5.8 hr", "6 hr 20 min", "4 hr 45 min"],
        "Step 1: 1 hr 45 min = 105 min, and 4 × 105 = 420 min. Step 2: 420 ÷ 60 = <b>7 hr</b>. "
        "(5.8 hr multiplies 1.45 × 4, as if an hour had 100 minutes, and 4 hr 45 min multiplies only the hours.)")
    add("A truck can carry 2 tons. Each crate weighs 250 lb. How many crates can the truck carry?",
        "16 crates", ["8 crates", "160 crates", "500 crates"],
        "Step 1: 1 ton = 2,000 lb, so 2 tons = 4,000 lb. Step 2: 4,000 ÷ 250 = <b>16 crates</b>. "
        "(8 crates uses only 1 ton, 160 crates divides by 25 instead of 250, and 500 crates multiplies 2 × 250.)")
    n, he, his = P.next()
    add("%s walks 1/4 mi to school and 1/4 mi back home, 5 days a week. How many feet does %s walk in a week?" % (n, he),
        "13,200 ft", ["6,600 ft", "1,320 ft", "2,640 ft"],
        "Step 1: 1/4 mi = 5,280 ÷ 4 = 1,320 ft. Step 2: each day 2 × 1,320 = 2,640 ft. Step 3: 5 × 2,640 = <b>13,200 ft</b>. "
        "(6,600 ft counts only the walk to school.)")
    n, he, his = P.next()
    add("A backpack can hold 5 kg. %s puts in 3 books of 650 g each and a laptop of 1.8 kg. "
        "How many more kilograms can the backpack hold?" % n,
        "1.25 kg", ["3.75 kg", "2.55 kg", "12.5 kg"],
        "Step 1: 3 × 650 = 1,950 g = 1.95 kg. Step 2: 1.95 + 1.8 = 3.75 kg in the bag. Step 3: 5 − 3.75 = <b>1.25 kg</b>. "
        "(3.75 kg is what is already in the bag, and 2.55 kg counts only one book.)")
    n, he, his = P.next()
    add("%s practices piano for 3/4 hr on Monday, 50 min on Tuesday and 1 1/4 hr on Wednesday. "
        "How many minutes is that in all?" % n,
        "170 min", ["250 min", "110 min", "95 min"],
        "Change to minutes: 3/4 hr = 45 min and 1 1/4 hr = 60 + 15 = 75 min. 45 + 50 + 75 = <b>170 min</b> "
        "(2 hr 50 min). (250 min uses 100 minutes in an hour, and 110 min forgets the 1 in 1 1/4 hr.)")
    n, he, his = P.next()
    add("%s has 4 yd of ribbon. Each bow uses 2 ft 6 in. How many whole bows can %s make?" % (n, he),
        "4 bows", ["5 bows", "6 bows", "1 bow"],
        "Use inches: 4 yd = 4 × 36 = 144 in and 2 ft 6 in = 30 in. 144 ÷ 30 = 4 R24, so <b>4 bows</b>, with 24 in left over. "
        "(5 rounds up, but there is not enough ribbon for a 5th bow. 6 ignores the 6 inches: 12 ft ÷ 2 ft.)")
    assert len(its) == 20, len(its)
    return {"title": "Multi-step word problems", "items": its}


# ------------------------------------------------------------ lesson
def ex(title, qs, s, a):
    return ("<div class='sn-ex'><span class='sn-ex-t'>%s</span><p class='sn-ex-q'>%s</p>"
            "<p class='sn-ex-s'>%s</p><p class='sn-ex-a'>Answer: %s</p></div>" % (title, qs, s, a))


def table(head, rows):
    h = "".join("<th>%s</th>" % x for x in head)
    b = "".join("<tr>" + "".join("<td>%s</td>" % c for c in r) + "</tr>" for r in rows)
    return "<div class='sn-tw'><table class='sn-table'><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>" % (h, b)


def body_html():
    tbl = conv_table("cm", "m", [(25, Dm("0.25")), (50, Dm("0.5")), (100, Dm("1")), (250, Dm("2.5"))], None)
    return H(
        "<h2>The big idea</h2>"
        "<p>To change to a <b>bigger</b> unit, <b>divide</b>: you need fewer of the big units. "
        "To change to a <b>smaller</b> unit, <b>multiply</b>: you need more of the small units.</p>" +
        ex("Two ways", "3 m = ☐ cm &nbsp; and &nbsp; 250 cm = ☐ m",
           "1 m = 100 cm. To centimeters (smaller): 3 × 100 = 300. To meters (bigger): 250 ÷ 100 = 2.5.",
           "300 cm and 2.5 m") +
        "<h2>Metric units: powers of 10</h2>"
        "<p>Metric units go up by 10, 100 or 1,000, so you only move the decimal point.</p>" +
        table(["Fact", "To the smaller unit", "To the bigger unit"], [
            ["1 km = 1,000 m", "× 1,000: point 3 places right", "÷ 1,000: point 3 places left"],
            ["1 m = 100 cm", "× 100: point 2 places right", "÷ 100: point 2 places left"],
            ["1 cm = 10 mm", "× 10: point 1 place right", "÷ 10: point 1 place left"],
            ["1 kg = 1,000 g", "0.75 kg = 750 g", "750 g = 0.75 kg"],
            ["1 L = 1,000 mL", "1.2 L = 1,200 mL", "600 mL = 0.6 L"],
        ]) +
        "<figure class='sn-fig'>" + tbl +
        "<figcaption>Centimeters to meters: divide by 100. 5 cm is 0.05 m, not 0.5 m.</figcaption></figure>"
        "<h2>Customary units and time</h2>"
        "<p>These do not go up by 10, so learn each number.</p>" +
        table(["Measure", "Facts"], [
            ["Length", "1 ft = 12 in &nbsp; 1 yd = 3 ft = 36 in &nbsp; 1 mi = 5,280 ft"],
            ["Weight", "1 lb = 16 oz &nbsp; 1 ton = 2,000 lb"],
            ["Capacity", "1 pt = 2 cups &nbsp; 1 qt = 2 pt &nbsp; 1 gal = 4 qt"],
            ["Time", "1 min = 60 sec &nbsp; 1 hr = 60 min &nbsp; 1 day = 24 hr &nbsp; 1 week = 7 days"],
        ]) +
        "<h2>Fractions, decimals and mixed units</h2>"
        "<p>When the division has a remainder, write the leftover as a fraction of the big unit, "
        "or keep it as a mixed unit.</p>" +
        ex("Inches to feet", "30 in = ☐ ft",
           "30 ÷ 12 = 2 R6. 6 inches is 6/12 = 1/2 of a foot.", "2 1/2 ft, or 2 ft 6 in") +
        ex("Minutes to hours", "90 min = ☐ hr",
           "90 ÷ 60 = 1 R30. 30 minutes is 30/60 = 1/2 of an hour.", "1 1/2 hr = 1.5 hr = 1 hr 30 min") +
        "<h2>Multi-step problems</h2>"
        "<p>First change all the measurements to <b>one unit</b>. Then solve. Change the answer to the unit the question asks for.</p>" +
        ex("Example", "5 bags of apples weigh 900 g each. What is the total mass in kilograms?",
           "Step 1: 5 × 900 = 4,500 g. Step 2: 4,500 ÷ 1,000 = 4.5.", "4.5 kg") +
        "<h2>Common mistakes</h2>" +
        table(["Mistake", "What to do instead"], [
            ["Multiplying to get a bigger unit (250 cm = 25,000 m)", "To a bigger unit, divide: 250 ÷ 100 = 2.5 m"],
            ["Moving the point the wrong number of places (5 cm = 0.5 m)", "÷ 100 moves it 2 places: 5 cm = 0.05 m"],
            ["Using 10 or 100 for customary units (30 in = 3 ft)", "1 ft = 12 in, so 30 in = 2 1/2 ft"],
            ["Writing a mixed unit as a decimal (90 min = 1.3 hr)", "1 hr 30 min = 1 1/2 hr = 1.5 hr"],
            ["Mixing up pints and quarts (3 qt = 12 pt)", "1 qt = 2 pt, so 3 qt = 6 pt. 4 qt = 1 gal"],
        ])
    )


FAQ = [
    {"q": "How do you convert smaller units to larger units in 5th grade?",
     "a": "Divide by the number of small units in 1 large unit. For example, 1 m = 100 cm, so 250 cm = 250 ÷ 100 = 2.5 m."},
    {"q": "How do you convert 5 cm to meters?",
     "a": "Divide by 100, which moves the decimal point 2 places to the left: 5 cm = 0.05 m. A common mistake is 0.5 m, which moves it only 1 place."},
    {"q": "How many cups, pints and quarts are in a gallon?",
     "a": "1 gallon = 4 quarts = 8 pints = 16 cups, because 1 quart = 2 pints and 1 pint = 2 cups."},
    {"q": "What does 5.MD.A.1 mean?",
     "a": "It is the Common Core Grade 5 standard for converting between bigger and smaller units in the same measurement system, "
          "such as 5 cm = 0.05 m, and using these conversions to solve multi-step real-world problems."},
]


def gen():
    rnd = random.Random(514)
    sets = [set_metric(), set_customary(), set_capacity_time(), set_compare(), set_story(rnd)]
    balance(sets, rnd)
    seen = set()
    for s in sets:
        assert len(s["items"]) == 20, (s["title"], len(s["items"]))
        assert sorted(it["a"] for it in s["items"]) == sorted([0, 1, 2, 3] * 5)
        for it in s["items"]:
            assert len(set(it["c"])) == 4, it
            k = re.sub(r"<[^>]+>", "", it["q"]) + "|" + "|".join(sorted(it["c"]))
            assert k not in seen, it["q"]
            seen.add(k)
            it["q"] = H(it["q"])
            it["c"] = [H(c) for c in it["c"]]
            it["e"] = H(it["e"])
    return {
        "country": "us", "subject": "math", "grade": "grade-5", "slug": "measurement-conversions", "sort": 14,
        "updated": UPDATED, "pdf_url": "",
        "title": "Measurement Conversions",
        "seo_title": "Grade 5 Measurement Conversion Worksheets: Convert to Larger Units with Decimals and Fractions, Multi-Step Problems",
        "short_title": "Measurement conversions",
        "domain": "Measurement and Data",
        "standard_code": "5.MD.A.1",
        "standard_url": "https://www.thecorestandards.org/Math/Content/5/MD/A/1/",
        "standard_text": "Convert among different-sized standard measurement units within a given measurement system (e.g., convert 5 cm to 0.05 m), and use these conversions in solving multi-step, real world problems.",
        "meta_desc": "Free Grade 5 measurement conversion worksheets: convert both ways between km, m, cm, mm, kg, g, L, mL, miles, yards, feet, inches, pounds, ounces, tons, cups, pints, quarts, gallons and time, with decimals (5 cm = 0.05 m) and fractions (30 in = 2½ ft). Compare measurements and solve multi-step word problems. 100 practice questions with step-by-step answers.",
        "key_big": "To a bigger unit, divide. To a smaller unit, multiply.",
        "key_sub": "1 m = 100 cm, so 250 cm = 250 ÷ 100 = 2.5 m and 5 cm = 0.05 m. A leftover becomes a fraction: 30 in = 2 ft 6 in = 2½ ft, and 90 min = 1½ hr = 1 hr 30 min (not 1 hr 50 min).",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }


def mark_large(u, pattern):
    """Tag pictures that must print larger so their labels stay readable."""
    rx = re.compile(r"<svg (?=[^>]*aria-label='" + pattern + ")")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        mark_large(u, "conversion table")
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
