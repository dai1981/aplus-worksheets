# -*- coding: utf-8 -*-
"""
US Grade 6 Math: Converting Units with Ratios (6.RP.A.3d)
  python3 tools/gen_us_math_g6_unit_conversions.py
Grade 6 treats a conversion fact as a RATIO (1 ft : 12 in) and uses ratio reasoning:
ratio tables, double number lines, multiplying by a conversion fraction so the units cancel,
converting between systems with a given rate (1 in = 2.54 cm, 1 kg is about 2.2 lb),
and converting BOTH parts of a rate (60 mi per hr = 1 mi per min).
Every answer is computed or checked in code with fractions.Fraction / Decimal, and no wrong
choice may have the same value as the right answer (or as another choice).
Questions are written in plain text ('3 1/2 ft'); fractions become <span class='fr'> at the end.
HTML attributes use single quotes (no backslashes in the JSON). Numbers 1,000 and above have commas.
"""
import json, os, random, re
from decimal import Decimal as Dm
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "us", "math", "grade-6")
UPDATED = "2026-11-02"
GREEN = "#006633"
FILL2 = "#eef6f0"
RED = "#c0392b"
INK = "#2b2b2b"
GRAY = "#5a5a5a"
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
    "lb": ("wt", 16, "pound", "pounds", "lb"),
    "oz": ("wt", 1, "ounce", "ounces", "oz"),
    "gal": ("ccap", 16, "gallon", "gallons", "gal"),
    "qt": ("ccap", 4, "quart", "quarts", "qt"),
    "pt": ("ccap", 2, "pint", "pints", "pt"),
    "cup": ("ccap", 1, "cup", "cups", None),
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


def conv(x, a, b):
    """Exact value of x a in unit b."""
    assert U[a][0] == U[b][0], (a, b)
    return F(x) * U[a][1] / U[b][1]


# ------------------------------------------------------------ numbers
def N(x):
    """Exact decimal text, commas from 1,000: 3500 -> '3,500', 0.050 -> '0.05'."""
    if isinstance(x, F):
        d = x.denominator
        while d % 2 == 0:
            d //= 2
        while d % 5 == 0:
            d //= 5
        assert d == 1, ("not a finite decimal", x)
        x = Dm(x.numerator) / Dm(x.denominator)
    x = Dm(x)
    return format(x.normalize(), ",f")


def fr(x):
    """Fraction as a whole or mixed number: 5/2 -> '2 1/2', 3/4 -> '3/4', 6 -> '6'."""
    x = F(x)
    w, r = divmod(x.numerator, x.denominator)
    if r == 0:
        return N(w)
    if w == 0:
        return "%d/%d" % (r, x.denominator)
    return "%s %d/%d" % (N(w), r, x.denominator)


def money(x):
    return "$%s" % format(Dm(x.numerator) / Dm(x.denominator) if isinstance(x, F) else Dm(x), ",.2f")


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


def short(u):
    return U[u][4] or name(u)


def fact(big, small):
    return "%s = %s" % (q(1, big), q(ratio(big, small), small))


def rat(big, small):
    return "%s : %s" % (q(1, big), q(ratio(big, small), small))


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
    """'2 ft 6 in' -> ('clen', 30). Unknown words (laps, bows) count as their own unit.
    Plain numbers -> ('', n). 'about 11 lb', '$0.30 per oz', rates -> compared by their text pattern."""
    s = s.strip()
    m = re.fullmatch(r"about (.+)", s)
    if m:
        v = value(m.group(1))
        return ("about",) + v if v else None
    m = re.fullmatch(r"\$([\d,]+\.\d\d)(?: per (\w+))?", s)
    if m:
        return ("$", m.group(2) or "", F(Dm(m.group(1).replace(",", ""))))
    m = re.fullmatch(r"(" + NUM + r") (\w+) per (\w+)", s)
    if m:
        return ("rate", m.group(2), m.group(3), parse_num(m.group(1)))
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


def same(a, b):
    """Two measurements are equal (checked with exact values)."""
    va, vb = value(a), value(b)
    assert va and vb and va[0] == vb[0], (a, b)
    return va[1] == vb[1]


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


def text(x, y, t, fs=17, anchor="middle", col=INK, bold=True):
    return ("<text x='%.1f' y='%.1f' font-size='%d'%s fill='%s' text-anchor='%s'>%s</text>"
            % (x, y, fs, " font-weight='700'" if bold else "", col, anchor, t))


def frac(a, b):
    return "<span class='fr'><span class='fn'>%d</span><span class='fd'>%d</span></span>" % (a, b)


def UF(top, bot):
    """A conversion fraction with units, e.g. 1 yd over 3 ft."""
    return "<span class='fr'><span class='fn'>%s</span><span class='fd'>%s</span></span>" % (top, bot)


FR = re.compile(r"(?<![\d/])(\d+)/(\d+)(?![\d/])")


def H(s):
    """Plain '2 1/2' -> HTML stacked fraction."""
    return FR.sub(lambda m: frac(int(m.group(1)), int(m.group(2))), s)


def tw(s, fs):
    """Rough text width of a bold label in viewBox units."""
    return sum(0.33 if ch in ",." else 0.6 for ch in s) * fs


# ------------------------------------------------------------ figure: ratio table
def ratio_table(top, bot, tv, bv, miss):
    """Horizontal ratio table. top/bot = unit keys (row labels). tv/bv = values as text.
    miss = (row, col) of the red ? box. Every column is checked to be the same ratio."""
    assert len(tv) == len(bv)
    r0 = None
    for c, (a, b) in enumerate(zip(tv, bv)):
        if (0, c) == miss or (1, c) == miss:
            continue
        rr = parse_num(b) / parse_num(a)
        assert r0 is None or rr == r0, (tv, bv)
        r0 = rr
    labels = [cap(name(top)), cap(name(bot))]
    LW = int(max(tw(l, 16) for l in labels)) + 22
    CW = int(max(max(tw(v, 18) for v in tv + bv) + 22, 62))
    RH = 40
    n = len(tv)
    W = 4 + LW + CW * n
    Ht = 4 + RH * 2
    o = []
    for r, (lab, vals) in enumerate([(labels[0], tv), (labels[1], bv)]):
        y = 2 + RH * r
        o.append("<rect x='2' y='%d' width='%d' height='%d' fill='%s'/>" % (y, LW, RH, GREEN))
        o.append(text(2 + LW / 2.0, y + RH / 2.0 + 5.5, lab, 16, col="#ffffff"))
        o.append("<rect x='%d' y='%d' width='%d' height='%d' fill='%s'/>" % (2 + LW, y, CW * n, RH, "#ffffff" if r == 0 else FILL2))
        for c, v in enumerate(vals):
            cx = 2 + LW + CW * c + CW / 2.0
            cy = y + RH / 2.0
            if (r, c) == miss:
                o.append("<rect x='%.1f' y='%.1f' width='40' height='28' rx='4' fill='none' stroke='%s' stroke-width='2' "
                         "stroke-dasharray='5 3'/>" % (cx - 20, cy - 14, RED))
                o.append(text(cx, cy + 6.5, "?", 18, col=RED))
            else:
                o.append(text(cx, cy + 6.5, v, 18))
    for c in range(1, n):
        x = 2 + LW + CW * c
        o.append("<line x1='%d' y1='2' x2='%d' y2='%d' stroke='#b9d6c2' stroke-width='1.5'/>" % (x, x, Ht - 2))
    o.append("<line x1='2' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='2'/>" % (2 + RH, W - 2, 2 + RH, GREEN))
    o.append("<rect x='2' y='2' width='%d' height='%d' fill='none' stroke='%s' stroke-width='2.5'/>" % (W - 4, Ht - 4, GREEN))
    return svg_wrap(W, Ht, "".join(o), "ratio table: %s and %s" % (name(top), name(bot)))


# ------------------------------------------------------------ figure: double number line
def dnl(top, bot, tv, bv, miss, labels=None):
    """Double number line. Ticks are placed by the TOP value (drawn to scale).
    miss = (row, index) of the red ? box. Every pair is checked to be the same ratio."""
    assert len(tv) == len(bv)
    pos = [parse_num(v) for v in tv]
    r0 = None
    for i, (a, b) in enumerate(zip(tv, bv)):
        if (0, i) == miss or (1, i) == miss or parse_num(a) == 0:
            continue
        rr = parse_num(b) / parse_num(a)
        assert r0 is None or rr == r0, (tv, bv)
        r0 = rr
    labels = labels or [cap(name(top)), cap(name(bot))]
    LW = int(max(tw(l, 16) for l in labels)) + 14
    gap = max(max(tw(v, 17) for v in tv + bv) + 16, 56)
    steps = [pos[i + 1] - pos[i] for i in range(len(pos) - 1)]
    unit = min(steps)
    span = float((pos[-1] - pos[0]) / unit) * gap
    x0 = LW + 22
    W = int(x0 + span + 30)
    Y1, Y2 = 42, 92
    Ht = 128
    o = []
    o.append(text(LW, Y1 + 6, labels[0], 16, "end", GREEN))
    o.append(text(LW, Y2 + 6, labels[1], 16, "end", GREEN))
    for y in (Y1, Y2):
        o.append("<line x1='%.1f' y1='%d' x2='%.1f' y2='%d' stroke='%s' stroke-width='2.2'/>" % (x0 - 8, y, W - 10, y, INK))
        o.append("<path d='M%d %d l-9 -5 v10 z' fill='%s'/>" % (W - 4, y, INK))
    for i, p in enumerate(pos):
        x = x0 + float((p - pos[0]) / unit) * gap
        for r, (y, v) in enumerate([(Y1, tv[i]), (Y2, bv[i])]):
            o.append("<line x1='%.1f' y1='%d' x2='%.1f' y2='%d' stroke='%s' stroke-width='2'/>" % (x, y - 8, x, y + 8, INK))
            ty = y - 14 if r == 0 else y + 28
            if (r, i) == miss:
                o.append("<rect x='%.1f' y='%.1f' width='36' height='24' rx='4' fill='none' stroke='%s' stroke-width='2' "
                         "stroke-dasharray='5 3'/>" % (x - 18, ty - 18, RED))
                o.append(text(x, ty, "?", 17, col=RED))
            else:
                o.append(text(x, ty, v, 17))
    return svg_wrap(W, Ht, "".join(o), "double number line: %s and %s" % (labels[0].lower(), labels[1].lower()))


# ------------------------------------------------------------ explanations
def ratio_e(x, a, b, style="frac", note=""):
    """Explain x a -> b with the ratio 1 big : k small."""
    x = F(x)
    ans = conv(x, a, b)
    f = (lambda v: fr(v)) if style == "frac" else (lambda v: N(v))
    if U[a][1] > U[b][1]:
        k = ratio(a, b)
        s = ("The ratio is %s. %s are smaller, so you need <b>more</b> of them: multiply by %s. "
             "%s × %s = %s, so %s = <b>%s</b>." % (rat(a, b), cap(name(b)), N(k), f(x), N(k), f(ans),
                                                  q(x, a, style), q(ans, b, style)))
    else:
        k = ratio(b, a)
        s = ("The ratio is %s. %s are bigger, so you need <b>fewer</b> of them: divide by %s. "
             "%s ÷ %s = %s, so %s = <b>%s</b>." % (rat(b, a), cap(name(b)), N(k), f(x), N(k), f(ans),
                                                  q(x, a, style), q(ans, b, style)))
    return s + (" " + note if note else "")


def conv_q(x, a, b, style="frac"):
    return "Convert. <b>%s = ☐ %s</b>" % (q(x, a, style), short(b))


def conv_item(x, a, b, wrong, note="", style="frac"):
    x = F(x)
    ans = conv(x, a, b)
    return mcq(conv_q(x, a, b, style), q(ans, b, style), wrong, ratio_e(x, a, b, style, note))


# ------------------------------------------------------------ set 1: the conversion ratio
def set_ratio(rnd):
    P = People(rnd)
    its = []
    its.append(mcq("1 foot is the same length as 12 inches. Which ratio shows this?", "1 ft : 12 in",
                   ["12 ft : 1 in", "1 ft : 10 in", "1 ft : 36 in"],
                   "Write the units in the same order as the words: 1 foot to 12 inches is <b>1 ft : 12 in</b>. "
                   "(12 ft : 1 in turns it around, and 36 is the number of inches in a yard.)"))
    its.append(mcq("Which ratio is correct for yards and feet?", "1 yd : 3 ft",
                   ["3 yd : 1 ft", "1 yd : 12 ft", "1 yd : 36 ft"],
                   "1 yard = 3 feet, so the ratio is <b>1 yd : 3 ft</b>. (12 is inches in a foot, and 36 is inches in a yard, not feet.)"))
    its.append(mcq("Which ratio is correct for gallons and quarts?", "1 gal : 4 qt",
                   ["1 gal : 2 qt", "4 gal : 1 qt", "1 gal : 8 qt"],
                   "1 gallon = 4 quarts, so the ratio is <b>1 gal : 4 qt</b>. (2 is pints in a quart, and 8 is pints in a gallon.)"))
    its.append(mcq("Which ratio is correct for kilometers and meters?", "1 km : 1,000 m",
                   ["1 km : 100 m", "1,000 km : 1 m", "1 km : 10 m"],
                   "Kilo means 1,000, so 1 km = 1,000 m and the ratio is <b>1 km : 1,000 m</b>. "
                   "(1 m = 100 cm, but 1 km is 1,000 m, not 100 m.)"))
    its.append(conv_item(5, "yd", "ft", ["60 ft", "1 2/3 ft", "8 ft"],
                         "(60 ft uses 12, the inches in a foot. 1 2/3 ft divides instead of multiplying, and 8 ft adds 3.)"))
    its.append(conv_item(7, "lb", "oz", ["84 oz", "70 oz", "23 oz"],
                         "(84 oz uses 12 and 70 oz uses 10. 23 oz adds 16 instead of multiplying.)"))
    its.append(conv_item(6, "qt", "pt", ["3 pt", "24 pt", "8 pt"],
                         "(3 pt divides instead of multiplying, 24 pt uses 4, the quarts in a gallon, and 8 pt adds 2.)"))
    its.append(conv_item(4, "km", "m", ["400 m", "40,000 m", "0.004 m"],
                         "(400 m uses 1 km = 100 m, and 0.004 m divides instead of multiplying.)", "dec"))
    its.append(mcq("To change 60 in to feet, what do you do?", "Divide by 12",
                   ["Multiply by 12", "Divide by 3", "Divide by 36"],
                   "The ratio is 1 ft : 12 in. A foot is bigger than an inch, so there will be fewer feet: "
                   "<b>divide by 12</b>. 60 ÷ 12 = 5, so 60 in = 5 ft. (Dividing by 3 or 36 would give yards.)"))
    its.append(mcq("To change 9 gal to quarts, what do you do?", "Multiply by 4",
                   ["Divide by 4", "Multiply by 2", "Multiply by 8"],
                   "The ratio is 1 gal : 4 qt. A quart is smaller than a gallon, so there will be more quarts: "
                   "<b>multiply by 4</b>. 9 × 4 = 36, so 9 gal = 36 qt. (1 qt = 2 pt and 1 gal = 8 pt, so 2 and 8 are for pints.)"))
    its.append(conv_item(48, "oz", "lb", ["768 lb", "4 lb", "4.8 lb"],
                         "(768 lb multiplies instead of dividing, 4 lb uses 12, and 4.8 lb uses 10.)"))
    its.append(conv_item(20, "qt", "gal", ["80 gal", "10 gal", "2 gal"],
                         "(80 gal multiplies instead of dividing, 10 gal uses 2, and 2 gal uses 10.)"))
    its.append(conv_item(3500, "g", "kg", ["35 kg", "3,500,000 kg", "0.35 kg"],
                         "(35 kg divides by 100, 0.35 kg divides by 10,000, and 3,500,000 kg multiplies instead of dividing.)", "dec"))
    its.append(conv_item(180, "min", "hr", ["1.8 hr", "18 hr", "10,800 hr"],
                         "(1.8 hr uses 100 minutes in an hour, 18 hr divides by 10, and 10,800 hr multiplies instead of dividing.)"))
    its.append(conv_item(72, "in", "yd", ["6 yd", "24 yd", "2,592 yd"],
                         "(6 is the number of feet, not yards. 24 yd divides by 3, the feet in a yard, and 2,592 yd multiplies instead of dividing.)"))
    its.append(mcq("Which ratio is equivalent to 1 ft : 12 in?", "5 ft : 60 in",
                   ["5 ft : 16 in", "5 ft : 50 in", "60 ft : 5 in"],
                   "Multiply both parts of 1 ft : 12 in by 5: <b>5 ft : 60 in</b>. "
                   "(5 ft : 16 in adds 4 to both parts. Adding does not keep the ratio the same.)"))
    its.append(mcq("To change 9 ft to yards, you multiply 9 ft by a fraction equal to 1. Which fraction?",
                   UF("1 yd", "3 ft"), [UF("3 ft", "1 yd"), UF("1 yd", "12 ft"), UF("12 in", "1 ft")],
                   "Put feet on the bottom so the feet cancel and yards are left: 9 ft × (1 yd over 3 ft) = 9 ÷ 3 yd = 3 yd. "
                   "The answer is <b>1 yd over 3 ft</b>. (With 3 ft over 1 yd, the feet do not cancel.)"))
    its.append(mcq("To change 5 gal to quarts, you multiply 5 gal by a fraction equal to 1. Which fraction?",
                   UF("4 qt", "1 gal"), [UF("1 gal", "4 qt"), UF("2 qt", "1 gal"), UF("8 qt", "1 gal")],
                   "Put gallons on the bottom so the gallons cancel and quarts are left: 5 gal × (4 qt over 1 gal) = 5 × 4 qt = 20 qt. "
                   "The answer is <b>4 qt over 1 gal</b>. (1 gal = 4 qt, not 2 or 8.)"))
    its.append(conv_item(2, "mi", "ft", ["2,640 ft", "3,520 ft", "10,000 ft"],
                         "(2,640 ft divides instead of multiplying, 3,520 is the number of yards in 2 miles, "
                         "and 10,000 ft uses 1 mi = 5,000 ft.)"))
    n, he, his = P.next()
    its.append(mcq("%s says 8 pt = 16 qt. What mistake did %s make?" % (n, he),
                   "%s multiplied instead of dividing." % cap(he),
                   ["%s used 1 qt = 4 pt." % cap(he), "%s divided instead of multiplying." % cap(he), "%s made no mistake." % cap(he)],
                   "The ratio is 1 qt : 2 pt. A quart is bigger than a pint, so there are <b>fewer</b> quarts: 8 ÷ 2 = 4, "
                   "so 8 pt = 4 qt. %s multiplied 8 × 2 = 16. <b>%s multiplied instead of dividing.</b>" % (n, cap(he))))
    assert len(its) == 20
    order = [0, 1, 2, 3, 4, 8, 5, 6, 9, 7, 10, 11, 12, 13, 15, 14, 18, 16, 17, 19]
    assert sorted(order) == list(range(20))
    return {"title": "The conversion ratio: multiply or divide?", "items": [its[i] for i in order]}


# ------------------------------------------------------------ set 2: ratio tables and double number lines
def set_tables():
    its = []

    def tbl(top, bot, tv, bv, miss, right, wrong, e):
        mv = (tv if miss[0] == 0 else bv)[miss[1]]
        # the missing value must fit the ratio of the other columns
        other = [(parse_num(a), parse_num(b)) for i, (a, b) in enumerate(zip(tv, bv)) if i != miss[1]]
        k = other[0][1] / other[0][0]
        want = parse_num(tv[miss[1]]) * k if miss[0] == 1 else parse_num(bv[miss[1]]) / k
        assert parse_num(right) == want and parse_num(mv) == want, (right, want)
        its.append(mcq(fig(ratio_table(top, bot, tv, bv, miss)) + "What number goes in the ? box?", right, wrong, e))

    def line(top, bot, tv, bv, miss, right, wrong, e, labels=None):
        mv = (tv if miss[0] == 0 else bv)[miss[1]]
        other = [(parse_num(a), parse_num(b)) for i, (a, b) in enumerate(zip(tv, bv)) if i != miss[1] and parse_num(a)]
        k = other[0][1] / other[0][0]
        want = parse_num(tv[miss[1]]) * k if miss[0] == 1 else parse_num(bv[miss[1]]) / k
        assert parse_num(right) == want and parse_num(mv) == want, (right, want)
        its.append(mcq(fig(dnl(top, bot, tv, bv, miss, labels)) + "What number goes in the ? box?", right, wrong, e))

    tbl("ft", "in", ["1", "2", "3", "5"], ["12", "24", "36", "60"], (1, 3), "60", ["48", "50", "17"],
        "1 ft : 12 in, so each bottom number is 12 × the top number. 5 × 12 = <b>60</b>. "
        "(48 is the next number in the pattern, but the table jumps from 3 to 5, not to 4.)")
    line("yd", "ft", ["0", "1", "2", "3", "4"], ["0", "3", "6", "9", "12"], (1, 4), "12", ["48", "7", "144"],
         "1 yd : 3 ft. Each step on the top line adds 1 yard, and each step on the bottom line adds 3 feet. "
         "4 × 3 = <b>12</b>. (48 uses 12, 144 uses 36, the inches in a yard, and 7 adds 3 to 4.)")
    tbl("gal", "qt", ["1", "3", "6", "9"], ["4", "12", "24", "36"], (0, 3), "9", ["144", "18", "12"],
        "1 gal : 4 qt, so each top number is the bottom number ÷ 4. 36 ÷ 4 = <b>9</b>. "
        "(144 multiplies instead of dividing, 18 uses 2 quarts in a gallon, and 12 divides by 3.)")
    line("m", "cm", ["0", "1", "2", "3", "4"], ["0", "100", "200", "300", "400"], (1, 3), "300", ["30", "3,000", "103"],
         "1 m : 100 cm, so 3 m = 3 × 100 = <b>300</b> cm. (30 uses 10 cm in a meter, 3,000 uses 1,000, "
         "and 103 adds instead of multiplying.)")
    tbl("lb", "oz", ["1", "2", "5", "8"], ["16", "32", "80", "128"], (0, 3), "8", ["6", "2,048", "12.8"],
        "1 lb : 16 oz, so each top number is the bottom number ÷ 16. 128 ÷ 16 = <b>8</b>. "
        "(6 is the next counting number, 2,048 multiplies, and 12.8 divides by 10.)")
    line("ft", "in", ["0", "2", "4", "6", "8"], ["0", "24", "48", "72", "96"], (1, 3), "72", ["60", "50", "18"],
         "Each tick is 2 ft = 24 in. 6 ft = 6 × 12 = <b>72</b> in. (60 uses 10 inches in a foot, "
         "50 adds 2 to 48 as on the top line, and 18 uses 3.)")
    tbl("hr", "min", ["1", "2", "4", "5"], ["60", "120", "240", "300"], (0, 3), "5", ["3", "30", "18,000"],
        "1 hr : 60 min, so each top number is the bottom number ÷ 60. 300 ÷ 60 = <b>5</b>. "
        "(3 uses 100 minutes in an hour, 30 divides by 10, and 18,000 multiplies.)")
    line("qt", "cup", ["0", "1", "2", "3", "4"], ["0", "4", "8", "12", "16"], (0, 3), "3", ["6", "48", "12"],
         "1 qt : 4 cups, so 12 cups ÷ 4 = <b>3</b> quarts. It lines up with 12 on the cups line. "
         "(6 uses 2 cups in a quart, 48 multiplies instead of dividing, and 12 is the number of cups, not quarts.)")
    tbl("km", "m", ["0.5", "1", "2", "3.5"], ["500", "1,000", "2,000", "3,500"], (1, 3), "3,500", ["350", "35,000", "3,000"],
        "1 km : 1,000 m, so 3.5 km = 3.5 × 1,000 = <b>3,500</b> m. (350 uses 100 and 35,000 uses 10,000. "
        "3,000 forgets the 0.5 km.)")
    tbl("kg", "g", ["1", "2", "4.5", "6"], ["1,000", "2,000", "4,500", "6,000"], (0, 2), "4.5", ["45", "0.45", "4,500,000"],
        "1 kg : 1,000 g, so 4,500 g ÷ 1,000 = <b>4.5</b> kg. (45 divides by 100, 0.45 divides by 10,000, "
        "and 4,500,000 multiplies.)")
    line("L", "mL", ["0", "0.5", "1", "1.5", "2"], ["0", "500", "1,000", "1,500", "2,000"], (1, 3), "1,500",
         ["150", "15,000", "1,050"],
         "1 L : 1,000 mL, so 1.5 L = 1.5 × 1,000 = <b>1,500</b> mL. The ? is halfway between 1,000 and 2,000. "
         "(150 uses 100, 15,000 uses 10,000, and 1,050 reads 1.5 L as 1 L 50 mL.)")
    line("hr", "min", ["0", "0.5", "1", "1.5", "2", "2.5"], ["0", "30", "60", "90", "120", "150"], (1, 5), "150",
         ["250", "170", "125"],
         "1 hr : 60 min, so 2.5 hr = 2.5 × 60 = <b>150</b> min. Each tick adds 30 minutes: 120 + 30 = 150. "
         "(250 uses 100 minutes in an hour, 125 uses 50, and 170 reads 2.5 hr as 2 hr 50 min.)")
    tbl("ft", "in", ["3", "6", "10"], ["36", "72", "120"], (1, 2), "120", ["108", "100", "30"],
        "First find the unit rate: 36 ÷ 3 = 12 inches for each foot. 10 × 12 = <b>120</b>. "
        "(108 adds 36 again, but the top went up by 4, not 3. 100 uses 10, and 30 uses 3.)")
    tbl("pt", "qt", ["4", "10", "16"], ["2", "5", "8"], (1, 2), "8", ["11", "32", "4"],
        "Each quart is 2 pints, so each bottom number is the top number ÷ 2. 16 ÷ 2 = <b>8</b>. "
        "(11 adds 6 because the top went up by 6, but adding does not keep the ratio. 32 multiplies, and 4 divides by 4.)")
    tbl("yd", "in", ["2", "5", "8"], ["72", "180", "288"], (0, 2), "8", ["24", "96", "10,368"],
        "Unit rate: 72 ÷ 2 = 36 inches in each yard. 288 ÷ 36 = <b>8</b>. "
        "(24 divides by 12, which gives feet, and 96 divides by 3.)")
    tbl("cm", "m", ["50", "125", "300"], ["0.5", "1.25", "3"], (1, 2), "3", ["30", "0.3", "30,000"],
        "1 m : 100 cm, so each bottom number is the top number ÷ 100. 300 ÷ 100 = <b>3</b>. "
        "(30 divides by 10, 0.3 divides by 1,000, and 30,000 multiplies.)")
    line("in", "cm", ["0", "1", "2", "3", "4"], ["0", "2.54", "5.08", "7.62", "10.16"], (1, 3), "7.62",
         ["7.08", "15.24", "1.18"],
         "1 in = 2.54 cm, so each tick adds 2.54 cm. 3 × 2.54 = <b>7.62</b>. "
         "(7.08 adds 2 instead of 2.54, 15.24 multiplies 5.08 by 3, and 1.18 divides 3 by 2.54.)")
    line("lb", "oz", ["0", "0.5", "1", "1.5", "2"], ["0", "8", "16", "24", "32"], (1, 3), "24", ["21", "15", "12"],
         "1 lb : 16 oz, so 1.5 lb = 1.5 × 16 = <b>24</b> oz (16 + 8). "
         "(21 reads 1.5 lb as 1 lb 5 oz, 15 uses 10, and 12 uses 8 ounces for each pound.)")
    tbl("oz", "lb", ["32", "56", "72"], ["2", "3.5", "4.5"], (1, 2), "4.5", ["6", "1,152", "7.2"],
        "1 lb : 16 oz, so each bottom number is the top number ÷ 16. 72 ÷ 16 = <b>4.5</b>. "
        "(6 divides by 12, 7.2 divides by 10, and 1,152 multiplies.)")
    # read the unit rate from a table
    its.append(mcq(fig(ratio_table("gal", "qt", ["3", "5", "8"], ["12", "20", "32"], None)) +
                   "The table shows gallons and quarts. How many quarts are in 1 gallon?", "4", ["9", "2", "12"],
                   "Divide any bottom number by its top number: 12 ÷ 3 = 4, 20 ÷ 5 = 4, 32 ÷ 8 = 4. "
                   "So 1 gal = <b>4</b> qt. (9 subtracts 12 − 3. Ratios compare by dividing, not subtracting. 2 is the pints in a quart, and 12 qt is 3 gallons.)"))
    assert len(its) == 20
    order = [0, 1, 2, 3, 5, 4, 7, 6, 8, 9, 10, 11, 19, 12, 13, 15, 14, 17, 18, 16]
    assert sorted(order) == list(range(20))
    return {"title": "Ratio tables and double number lines", "items": [its[i] for i in order]}


# ------------------------------------------------------------ set 3: fractions, decimals and mixed units
def set_mixed():
    its = []

    def add(qs, right, wrong, e, check=None, same_ok=False):
        if check:
            assert same(check, right), (check, right)
            for w in wrong:
                if not same_ok and value(w) and value(w)[0] == value(check)[0]:
                    assert not same(check, w), (check, w)
        its.append(mcq(qs, right, wrong, e, same_ok))

    add(conv_q(F(5, 2), "gal", "qt", "dec"), "10 qt", ["8 qt", "5 qt", "13 qt"],
        "The ratio is 1 gal : 4 qt, so multiply: 2.5 × 4 = <b>10 qt</b>. "
        "(8 qt forgets the 0.5 gal, 5 qt uses 2, and 13 qt reads 2.5 gal as 2 gal 5 qt.)", "2.5 gal")
    add(conv_q(42, "in", "ft"), "3 1/2 ft", ["3.6 ft", "4.2 ft", "504 ft"],
        "The ratio is 1 ft : 12 in, so divide: 42 ÷ 12 = 3 R6. 6 inches is 6/12 = 1/2 foot, so 42 in = <b>3 1/2 ft</b>. "
        "(3.6 ft is a mistake for 3 ft 6 in, 4.2 ft divides by 10, and 504 ft multiplies.)", "42 in")
    add(conv_q(F(3, 4), "lb", "oz"), "12 oz", ["7.5 oz", "21 1/3 oz", "4 oz"],
        "The ratio is 1 lb : 16 oz, so multiply: 3/4 × 16 = 48/4 = <b>12 oz</b>. "
        "(7.5 oz uses 10, 21 1/3 oz divides 16 by 3/4, and 4 oz is only 1/4 lb.)", "3/4 lb")
    add(conv_q(F(5, 4), "hr", "min", "dec"), "75 min", ["125 min", "85 min", "15 min"],
        "The ratio is 1 hr : 60 min, so multiply: 1.25 × 60 = <b>75 min</b>. "
        "(125 min uses 100 minutes in an hour, 85 min reads 1.25 hr as 1 hr 25 min, and 15 min forgets the whole hour.)", "1.25 hr")
    add("Convert. <b>2 ft 8 in = ☐ in</b>", "32 in", ["28 in", "10 in", "24 in"],
        "2 ft = 2 × 12 = 24 in. Add the 8 inches: 24 + 8 = <b>32 in</b>. "
        "(28 in uses 10 inches in a foot, 10 in adds 2 + 8, and 24 in forgets the 8 inches.)", "2 ft 8 in")
    add("Convert. <b>30 oz = ☐ lb ☐ oz</b>", "1 lb 14 oz", ["3 lb", "1.14 lb", "2 lb 6 oz"],
        "1 lb : 16 oz. 30 ÷ 16 = 1 R14: 1 whole pound and 14 ounces left over, so 30 oz = <b>1 lb 14 oz</b>. "
        "(3 lb divides by 10, 1.14 lb writes the remainder as a decimal, and 2 lb 6 oz uses 12.)", "30 oz")
    add(conv_q(F(3, 2), "mi", "ft"), "7,920 ft", ["5,280 ft", "2,640 ft", "7,500 ft"],
        "The ratio is 1 mi : 5,280 ft. 1 mi = 5,280 ft and 1/2 mi = 2,640 ft, so 1 1/2 mi = 5,280 + 2,640 = <b>7,920 ft</b>. "
        "(5,280 ft forgets the 1/2 mi, 2,640 ft is only the 1/2 mi, and 7,500 ft uses 1 mi = 5,000 ft.)", "1 1/2 mi")
    add(conv_q(F(3, 4), "L", "mL", "dec"), "750 mL", ["75 mL", "7.5 mL", "7,500 mL"],
        "The ratio is 1 L : 1,000 mL, so multiply: 0.75 × 1,000 = <b>750 mL</b>. "
        "(75 mL multiplies by 100, 7.5 mL by 10, and 7,500 mL by 10,000.)", "0.75 L")
    add(conv_q(F(9, 4), "ft", "in"), "27 in", ["24 in", "28 in", "22 1/2 in"],
        "The ratio is 1 ft : 12 in. 2 × 12 = 24, and 1/4 of 12 = 3, so 2 1/4 ft = 24 + 3 = <b>27 in</b>. "
        "(24 in forgets the 1/4 ft, 28 in uses 1/4 ft = 4 in, and 22 1/2 in uses 10.)", "2 1/4 ft")
    add(conv_q(5, "qt", "gal"), "1 1/4 gal", ["1.1 gal", "20 gal", "2 1/2 gal"],
        "The ratio is 1 gal : 4 qt, so divide: 5 ÷ 4 = 1 R1. The extra quart is 1/4 gal, so 5 qt = <b>1 1/4 gal</b>. "
        "(1.1 gal writes the remainder as a decimal, 20 gal multiplies, and 2 1/2 gal uses 2.)", "5 qt")
    add(conv_q(F(16, 5), "km", "m", "dec"), "3,200 m", ["320 m", "32,000 m", "0.0032 m"],
        "The ratio is 1 km : 1,000 m, so multiply: 3.2 × 1,000 = <b>3,200 m</b>. "
        "(320 m uses 100, 32,000 m uses 10,000, and 0.0032 m divides instead of multiplying.)", "3.2 km")
    add(conv_q(F(5, 2), "lb", "oz", "dec"), "40 oz", ["37 oz", "25 oz", "32 oz"],
        "The ratio is 1 lb : 16 oz, so multiply: 2.5 × 16 = <b>40 oz</b>. "
        "(37 oz reads 2.5 lb as 2 lb 5 oz, 25 oz uses 10, and 32 oz forgets the 0.5 lb.)", "2.5 lb")
    add(conv_q(10, "cup", "qt"), "2 1/2 qt", ["5 qt", "40 qt", "2.2 qt"],
        "The ratio is 1 qt : 4 cups, so divide: 10 ÷ 4 = 2 R2. 2 cups is 2/4 = 1/2 qt, so 10 cups = <b>2 1/2 qt</b>. "
        "(5 qt uses 2 cups in a quart, 40 qt multiplies, and 2.2 qt writes the remainder as a decimal.)", "10 cups")
    add(conv_q(F(7, 4), "hr", "min"), "105 min", ["175 min", "60 min", "75 min"],
        "The ratio is 1 hr : 60 min. 1 hr = 60 min and 3/4 of 60 = 45 min, so 1 3/4 hr = 60 + 45 = <b>105 min</b>. "
        "(175 min uses 100 minutes in an hour, 60 min forgets the 3/4 hr, and 75 min uses 1/4 hr instead of 3/4 hr.)", "1 3/4 hr")
    add(conv_q(27, "in", "yd"), "3/4 yd", ["2 1/4 yd", "9 yd", "0.27 yd"],
        "The ratio is 1 yd : 36 in, so divide: 27/36 = <b>3/4 yd</b>. "
        "(2 1/4 divides by 12, which gives feet. 9 yd divides by 3, and 0.27 yd divides by 100.)", "27 in")
    add("Convert. <b>4 ft 9 in = ☐ ft</b>", "4 3/4 ft", ["4.9 ft", "57 ft", "4 1/4 ft"],
        "1 ft : 12 in, so 9 in = 9/12 = 3/4 ft. 4 ft 9 in = <b>4 3/4 ft</b>. "
        "(4.9 ft treats 9 inches as 9 tenths of a foot, 57 is the number of inches, and 4 1/4 uses 9/36, a part of a yard.)", "4 ft 9 in")
    add(conv_q(3750, "mL", "L", "dec"), "3.75 L", ["37.5 L", "0.375 L", "3,750,000 L"],
        "The ratio is 1 L : 1,000 mL, so divide: 3,750 ÷ 1,000 = <b>3.75 L</b>. "
        "(37.5 L divides by 100, 0.375 L divides by 10,000, and 3,750,000 L multiplies.)", "3,750 mL")
    add("Convert. <b>1 gal 3 qt = ☐ cups</b>", "28 cups", ["7 cups", "14 cups", "19 cups"],
        "1 gal = 4 qt, so 1 gal 3 qt = 7 qt. The ratio is 1 qt : 4 cups, so 7 × 4 = <b>28 cups</b>. "
        "(7 is the number of quarts, 14 is the number of pints, and 19 adds 16 cups + 3.)", "1 gal 3 qt")
    add("Which is the same length as 5 1/2 yd?", "16 1/2 ft", ["15 1/2 ft", "66 ft", "1 5/6 ft"],
        "The ratio is 1 yd : 3 ft, so multiply: 5 × 3 = 15 and 1/2 × 3 = 1 1/2. 15 + 1 1/2 = <b>16 1/2 ft</b>. "
        "(15 1/2 ft forgets to multiply the 1/2 by 3, 66 ft uses 12, and 1 5/6 ft divides.)", "5 1/2 yd")
    target = "2.25 hr"
    ch = ["2 hr 25 min", "135 min", "2 hr 15 min", "2 1/4 hr"]
    assert not same(target, ch[0]) and all(same(target, c) for c in ch[1:])
    add("Which is NOT equal to 2.25 hr?", ch[0], ch[1:],
        "0.25 hr = 1/4 hr = 1/4 of 60 = 15 min. So 2.25 hr = 2 1/4 hr = 2 hr 15 min = 135 min. "
        "<b>2 hr 25 min</b> reads the .25 as 25 minutes, but an hour has 60 minutes, not 100.", same_ok=True)
    assert len(its) == 20
    order = [0, 4, 7, 2, 1, 10, 11, 3, 5, 9, 8, 12, 16, 6, 13, 17, 14, 15, 18, 19]
    assert sorted(order) == list(range(20))
    return {"title": "Fractions, decimals and mixed units", "items": [its[i] for i in order]}


# ------------------------------------------------------------ set 4: between systems, and rates
def set_rates():
    its = []
    D = Dm

    def add(qs, right, wrong, e):
        its.append(mcq(qs, right, wrong, e))

    # 1 in = 2.54 cm (exact)
    assert D("10") * D("2.54") == D("25.4") and round(D(10) / D("2.54"), 2) == D("3.94")
    add("Use 1 in = 2.54 cm. Convert. <b>10 in = ☐ cm</b>", "25.4 cm", ["3.94 cm", "254 cm", "12.54 cm"],
        "The ratio is 1 in : 2.54 cm. A centimeter is smaller, so multiply: 10 × 2.54 = <b>25.4 cm</b>. "
        "(3.94 divides instead of multiplying, 254 moves the point too far, and 12.54 adds 10 + 2.54.)")
    assert D(12) * D("2.54") == D("30.48") and round(D(12) / D("2.54"), 2) == D("4.72")
    add("Use 1 in = 2.54 cm. A ruler is 12 in long. How long is it in centimeters?", "30.48 cm",
        ["4.72 cm", "14.54 cm", "304.8 cm"],
        "Multiply by the ratio 2.54 cm for each inch: 12 × 2.54 = <b>30.48 cm</b>. "
        "(4.72 divides instead of multiplying, 14.54 adds 12 + 2.54, and 304.8 puts the point in the wrong place.)")
    assert D(127) / D("2.54") == 50 and D(127) * D("2.54") == D("322.58") and D(127) - D("2.54") == D("124.46")
    add("Use 1 in = 2.54 cm. Convert. <b>127 cm = ☐ in</b>", "50 in", ["322.58 in", "124.46 in", "5 in"],
        "An inch is bigger than a centimeter, so there will be fewer inches: divide. 127 ÷ 2.54 = <b>50 in</b>. "
        "(322.58 multiplies instead of dividing, 124.46 subtracts, and 5 divides by 25.4.)")
    # 1 kg is about 2.2 lb
    assert D(5) * D("2.2") == 11 and round(D(5) / D("2.2"), 1) == D("2.3")
    add("Use 1 kg ≈ 2.2 lb. A bag of rice is 5 kg. About how many pounds is it?", "about 11 lb",
        ["about 2.3 lb", "about 7.2 lb", "about 110 lb"],
        "A pound is smaller than a kilogram, so there are more pounds: multiply. 5 × 2.2 = 11, so 5 kg is <b>about 11 lb</b>. "
        "(2.3 divides, 7.2 adds 5 + 2.2, and 110 moves the point.)")
    assert D(44) / D("2.2") == 20 and D(44) * D("2.2") == D("96.8") and D(44) - D("2.2") == D("41.8")
    add("Use 1 kg ≈ 2.2 lb. A dog weighs 44 lb. About how many kilograms is that?", "about 20 kg",
        ["about 96.8 kg", "about 41.8 kg", "about 2 kg"],
        "A kilogram is bigger than a pound, so there are fewer kilograms: divide. 44 ÷ 2.2 = 20, so 44 lb is <b>about 20 kg</b>. "
        "(96.8 multiplies, 41.8 subtracts, and 2 divides 44 by 22.)")
    # 1 mi is about 1.6 km
    assert D(5) * D("1.6") == 8 and D(5) / D("1.6") == D("3.125")
    add("Use 1 mi ≈ 1.6 km. About how many kilometers is 5 mi?", "about 8 km", ["about 3.1 km", "about 6.6 km", "about 80 km"],
        "A kilometer is shorter than a mile, so there are more kilometers: 5 × 1.6 = <b>about 8 km</b>. "
        "(3.1 divides, 6.6 adds 5 + 1.6, and 80 moves the point.)")
    assert D(10) / D("1.6") == D("6.25") and D(10) - D("1.6") == D("8.4")
    add("Use 1 mi ≈ 1.6 km. A race is 10 km long. About how many miles is that?", "about 6.25 mi",
        ["about 16 mi", "about 8.4 mi", "about 62.5 mi"],
        "A mile is longer than a kilometer, so there are fewer miles: divide. 10 ÷ 1.6 = 6.25, so the race is "
        "<b>about 6.25 mi</b>. (16 multiplies, 8.4 subtracts, and 62.5 puts the point in the wrong place.)")
    # 1 gal is about 3.8 L
    assert D(5) * D("3.8") == 19 and round(D(5) / D("3.8"), 1) == D("1.3")
    add("Use 1 gal ≈ 3.8 L. A fish tank holds 5 gal. About how many liters is that?", "about 19 L",
        ["about 1.3 L", "about 8.8 L", "about 190 L"],
        "A liter is smaller than a gallon, so multiply: 5 × 3.8 = <b>about 19 L</b>. "
        "(1.3 divides, 8.8 adds 5 + 3.8, and 190 moves the point.)")
    add("To change 8 in to centimeters, you multiply 8 in by a fraction. Which fraction?",
        UF("2.54 cm", "1 in"), [UF("1 in", "2.54 cm"), UF("1 cm", "2.54 in"), UF("12 in", "1 ft")],
        "Put inches on the bottom so the inches cancel and centimeters are left: 8 in × (2.54 cm over 1 in) = "
        "8 × 2.54 cm = 20.32 cm. The answer is <b>2.54 cm over 1 in</b>.")
    # rates: convert both parts
    add("60 miles per hour is the same speed as how many miles per minute?", "1 mi per min",
        ["60 mi per min", "3,600 mi per min", "6 mi per min"],
        "1 hr = 60 min, so 60 miles in 60 minutes is 60 ÷ 60 = <b>1 mile per minute</b>. "
        "(60 mi per min forgets to change the hour, 3,600 multiplies instead of dividing, and 6 divides by 10.)")
    assert F(3) * 4 == 12
    add("A faucet fills 3 gal per minute. How many quarts per minute is that?", "12 qt per min",
        ["3/4 qt per min", "6 qt per min", "180 qt per min"],
        "Change only the gallons: 1 gal : 4 qt, so 3 × 4 = <b>12 qt per minute</b>. The time stays “per minute.” "
        "(3/4 divides, 6 uses 2, and 180 multiplies by 60, but the time does not change.)")
    assert D(120) / 60 == 2
    add("A hose sprays 120 L per hour. How many liters per minute is that?", "2 L per min",
        ["7,200 L per min", "12 L per min", "1.2 L per min"],
        "Change only the time: 1 hr = 60 min, so 120 ÷ 60 = <b>2 L per minute</b>. "
        "(7,200 multiplies, 12 divides by 10, and 1.2 uses 100 minutes in an hour.)")
    assert D("4.80") / 16 == D("0.30")
    add("Cheese costs $4.80 per pound. What is the price per ounce?", "$0.30 per oz",
        ["$76.80 per oz", "$0.40 per oz", "$0.48 per oz"],
        "1 lb = 16 oz, so the price of 1 ounce is $4.80 ÷ 16 = <b>$0.30</b>. "
        "($76.80 multiplies, $0.40 uses 12 ounces in a pound, and $0.48 uses 10.)")
    add("Juice costs $2 per quart. At this rate, what is the price per gallon?", "$8.00 per gal",
        ["$0.50 per gal", "$4.00 per gal", "$16.00 per gal"],
        "1 gal = 4 qt, so a gallon costs 4 × $2 = <b>$8.00</b>. "
        "($0.50 divides, $4.00 uses 2 quarts in a gallon, and $16.00 uses 8, the pints in a gallon.)")
    assert 30 * 60 == 1800
    add("A cheetah can run 30 m per second. How many meters per minute is that?", "1,800 m per min",
        ["30 m per min", "0.5 m per min", "180 m per min"],
        "1 min = 60 sec, so in 1 minute it runs 30 × 60 = <b>1,800 m</b>. "
        "(30 forgets to change the time, 0.5 divides, and 180 multiplies by 6.)")
    assert F(48, 16) == 3
    add("A pump moves 48 cups of water per minute. How many gallons per minute is that?", "3 gal per min",
        ["12 gal per min", "6 gal per min", "768 gal per min"],
        "1 gal = 16 cups, so 48 ÷ 16 = <b>3 gal per minute</b>. "
        "(12 gives quarts, 6 uses 8, the pints in a gallon, and 768 multiplies.)")
    assert D("1.60") * D("0.5") == D("0.80")
    add("Rice costs $1.60 per kilogram. What do 500 g of rice cost?", "$0.80",
        ["$800.00", "$8.00", "$3.20"],
        "1 kg = 1,000 g, so 500 g = 0.5 kg. 0.5 × $1.60 = <b>$0.80</b>. "
        "($800.00 forgets to convert, $8.00 uses 100 g in a kilogram, and $3.20 doubles instead of halving.)")
    assert 90 * 1000 / 60 == 1500
    add("A train travels 90 km per hour. How many meters per minute is that?", "1,500 m per min",
        ["90,000 m per min", "1.5 m per min", "5,400,000 m per min"],
        "Change both parts. Distance: 90 km = 90,000 m. Time: 1 hr = 60 min. 90,000 ÷ 60 = <b>1,500 m per minute</b>. "
        "(90,000 changes only the distance, 1.5 changes only the time, and 5,400,000 multiplies by 60 instead of dividing.)")
    assert F(5 * 3600, 1000) == 18
    add("A bike goes 5 m per second. How many kilometers per hour is that?", "18 km per hr",
        ["18,000 km per hr", "0.3 km per hr", "300 km per hr"],
        "Change both parts. In 1 hour (3,600 sec) it goes 5 × 3,600 = 18,000 m. 18,000 m = 18 km, so <b>18 km per hour</b>. "
        "(18,000 forgets to change meters to kilometers, and 0.3 and 300 multiply by 60 only once.)")
    assert F(30 * 5280, 3600) == 44
    add("A car goes 30 miles per hour. How many feet per second is that?", "44 ft per sec",
        ["158,400 ft per sec", "2,640 ft per sec", "0.5 ft per sec"],
        "Change both parts. In 1 hour it goes 30 × 5,280 = 158,400 ft. 1 hr = 3,600 sec, so 158,400 ÷ 3,600 = "
        "<b>44 ft per second</b>. (158,400 changes only the distance, 2,640 divides by 60 only once, and 0.5 changes only the time.)")
    assert len(its) == 20
    order = [0, 3, 5, 7, 9, 1, 4, 6, 2, 8, 10, 11, 13, 12, 14, 15, 16, 17, 18, 19]
    assert sorted(order) == list(range(20))
    return {"title": "Between systems and converting rates", "items": [its[i] for i in order]}


# ------------------------------------------------------------ set 5: multi-step word problems
def set_story(rnd):
    P = People(rnd)
    P.i = 5
    its = []

    def add(qs, r, w, e):
        its.append(mcq(qs, r, w, e))

    n, he, his = P.next()
    assert F(6 * 400, 1000) == F(12, 5)
    add("A track is 400 m around. %s runs 6 laps. How many kilometers does %s run?" % (n, he),
        "2.4 km", ["24 km", "0.24 km", "2,400 km"],
        "Step 1: 6 × 400 = 2,400 m. Step 2: 1 km : 1,000 m, so 2,400 ÷ 1,000 = <b>2.4 km</b>. "
        "(2,400 km forgets to convert, 24 km uses 100 m in a kilometer, and 0.24 km uses 10,000.)")
    n, he, his = P.next()
    assert 4 * 750 == 3000
    add("A water bottle holds 750 mL. %s drinks 4 bottles a day. How many liters is that?" % n,
        "3 L", ["30 L", "0.3 L", "3,000 L"],
        "Step 1: 4 × 750 = 3,000 mL. Step 2: 1 L : 1,000 mL, so 3,000 ÷ 1,000 = <b>3 L</b>. (3,000 L forgets to convert, 30 L divides by 100, and 0.3 L divides by 10,000.)")
    assert 3 * 12 == 36 and 36 // 3 == 12
    add("A garden needs 3 sides of fence. Each side is 12 ft long. The fence is sold by the yard. How many yards are needed?",
        "12 yd", ["36 yd", "108 yd", "3 yd"],
        "Step 1: 3 × 12 = 36 ft. Step 2: 1 yd : 3 ft, so 36 ÷ 3 = <b>12 yd</b>. "
        "(36 yd forgets to convert, 108 multiplies, and 3 yd divides by 12.)")
    assert F(5, 2) * 16 == 40
    add("A cooler holds 2.5 gal of lemonade. How many 1-cup servings is that?",
        "40 servings", ["10 servings", "20 servings", "25 servings"],
        "1 gal = 16 cups, so 2.5 × 16 = <b>40 servings</b>. "
        "(10 counts quarts, 20 counts pints, and 25 uses 10 cups in a gallon.)")
    n, he, his = P.next()
    assert 16 // 4 * 3 == 12 and F(12, 4) == 3
    add("A soup recipe for 4 people uses 3 cups of broth. %s makes soup for 16 people. How many quarts of broth does %s need?" % (n, he),
        "3 qt", ["12 qt", "6 qt", "48 qt"],
        "Step 1: 16 people is 4 times as many, so 4 × 3 = 12 cups. Step 2: 1 qt : 4 cups, so 12 ÷ 4 = <b>3 qt</b>. "
        "(12 qt forgets to convert, 6 qt uses 2 cups in a quart, and 48 qt multiplies.)")
    n, he, his = P.next()
    assert 5 * 36 // 9 == 20
    add("%s has 5 yd of ribbon. Each bow uses 9 in. How many bows can %s make?" % (n, he),
        "20 bows", ["6 bows", "1 bow", "45 bows"],
        "Step 1: 1 yd : 36 in, so 5 yd = 5 × 36 = 180 in. Step 2: 180 ÷ 9 = <b>20 bows</b>. "
        "(6 bows uses 12 inches in a yard, 1 bow divides 15 ft by 9 without changing to inches, and 45 multiplies 5 × 9.)")
    n, he, his = P.next()
    assert 6 + 6 == 12
    add("Punch is made with 1 1/2 qt of juice and 3 pt of sparkling water. How many cups of punch is that?",
        "12 cups", ["4 1/2 cups", "9 cups", "18 cups"],
        "Change to cups. 1 qt = 4 cups, so 1 1/2 qt = 6 cups. 1 pt = 2 cups, so 3 pt = 6 cups. 6 + 6 = <b>12 cups</b>. "
        "(4 1/2 adds without converting, 9 uses 2 cups in a quart, and 18 uses 4 cups in a pint.)")
    n, he, his = P.next()
    assert F(18, 4) == F(9, 2)
    add("Each room needs 3 qt of paint. %s paints 6 rooms. How many gallons of paint does %s use?" % (n, he),
        "4 1/2 gal", ["18 gal", "9 gal", "4.2 gal"],
        "Step 1: 6 × 3 = 18 qt. Step 2: 1 gal : 4 qt, so 18 ÷ 4 = 4 R2 = <b>4 1/2 gal</b>. "
        "(18 gal forgets to convert, 9 gal uses 2, and 4.2 writes the remainder 2 as a decimal.)")
    n, he, his = P.next()
    assert F(24, 16) * F("2.40") == F("3.60")
    add("Grapes cost $2.40 per pound. %s buys 24 oz of grapes. How much does %s pay?" % (n, he),
        "$3.60", ["$57.60", "$5.76", "$4.80"],
        "Step 1: 1 lb : 16 oz, so 24 oz = 24 ÷ 16 = 1.5 lb. Step 2: 1.5 × $2.40 = <b>$3.60</b>. "
        "($57.60 forgets to convert, $5.76 uses 24 oz = 2.4 lb, and $4.80 uses 12 ounces in a pound.)")
    assert F(5000, 400) == F(25, 2)
    add("A race is 5 km long. A track is 400 m around. How many laps of the track is the race?",
        "12 1/2 laps", ["1 1/4 laps", "80 laps", "125 laps"],
        "Step 1: 5 km = 5 × 1,000 = 5,000 m. Step 2: 5,000 ÷ 400 = <b>12 1/2 laps</b>. "
        "(1 1/4 uses 100 m in a kilometer, 80 divides 400 by 5, and 125 uses 10,000 m.)")
    n, he, his = P.next()
    assert F(7, 2) * 3 - 8 == F(5, 2)
    add("%s has 3 1/2 yd of rope. %s cuts off 4 pieces that are each 2 ft long. How many feet of rope are left?" % (n, cap(he)),
        "2 1/2 ft", ["1 ft", "34 ft", "10 1/2 ft"],
        "Step 1: 1 yd : 3 ft, so 3 1/2 yd = 10 1/2 ft. Step 2: 4 × 2 = 8 ft cut off. Step 3: 10 1/2 − 8 = <b>2 1/2 ft</b>. "
        "(1 ft forgets the 1/2 yd, 34 ft uses 12, and 10 1/2 ft forgets to subtract.)")
    n, he, his = P.next()
    assert F(4, F(3, 4)) == F(16, 3)
    add("A pancake recipe uses 3/4 cup of milk for each batch. %s has 1 qt of milk. How many full batches can %s make?" % (n, he),
        "5 batches", ["6 batches", "1 batch", "3 batches"],
        "Step 1: 1 qt = 4 cups. Step 2: 4 ÷ 3/4 = 4 × 4/3 = 16/3 = 5 1/3, so <b>5 full batches</b>. "
        "(6 rounds up, but there is not enough milk for a 6th batch. 1 batch forgets to change quarts to cups, "
        "and 3 multiplies 4 × 3/4.)")
    assert 2000 // 250 == 8
    add("A 2 L jug of juice is poured into glasses that hold 250 mL each. How many glasses can be filled?",
        "8 glasses", ["4 glasses", "125 glasses", "500 glasses"],
        "Step 1: 1 L : 1,000 mL, so 2 L = 2,000 mL. Step 2: 2,000 ÷ 250 = <b>8 glasses</b>. "
        "(4 uses only 1 L, 125 divides 250 by 2, and 500 multiplies.)")
    n, he, his = P.next()
    assert F(4 * 5280, 4) == 5280
    add("%s walks 4 miles per hour. How many feet does %s walk in 15 minutes?" % (n, he),
        "5,280 ft", ["21,120 ft", "1,320 ft", "316,800 ft"],
        "Step 1: 15 min = 1/4 hr, so %s walks 4 × 1/4 = 1 mi. Step 2: 1 mi = <b>5,280 ft</b>. "
        "(21,120 ft is a whole hour, 1,320 ft is only 1/4 mi, and 316,800 ft multiplies by 15 instead of taking 1/4.)" % he)
    assert F(180, 3) * F(40, 60) == 40
    add("A car travels 180 miles in 3 hours. At the same rate, how far does it go in 40 minutes?",
        "40 mi", ["24 mi", "2,400 mi", "1 1/2 mi"],
        "Step 1: unit rate: 180 ÷ 3 = 60 mi per hour = 1 mi per minute. Step 2: 40 × 1 = <b>40 mi</b>. "
        "(24 uses 40 min = 0.4 hr, 2,400 multiplies 60 × 40, and 1 1/2 divides 60 by 40.)")
    n, he, his = P.next()
    assert 6 * 75 == 450 and F(450, 100) * 6 == 27 and F(75, 100) * 6 == F(9, 2)
    add("Fabric costs $6 per meter. %s needs 6 pieces that are each 75 cm long. How much does the fabric cost?" % n,
        "$27.00", ["$2,700.00", "$270.00", "$4.50"],
        "Step 1: 6 × 75 = 450 cm. Step 2: 1 m : 100 cm, so 450 cm = 4.5 m. Step 3: 4.5 × $6 = <b>$27.00</b>. "
        "($2,700 forgets to convert, $270 uses 10 cm in a meter, and $4.50 is the cost of only 1 piece.)")
    assert 9000 // 15 == 600 and 600 // 60 == 10
    add("A pool holds 9,000 gal. A hose fills it at 15 gal per minute. How many hours does it take to fill?",
        "10 hr", ["600 hr", "6 hr", "135,000 hr"],
        "Step 1: 9,000 ÷ 15 = 600 min. Step 2: 1 hr : 60 min, so 600 ÷ 60 = <b>10 hr</b>. "
        "(600 forgets to change minutes to hours, 6 uses 100 minutes in an hour, and 135,000 multiplies.)")
    assert (F(15, 2) + 3) == F(21, 2) and F(15, 2) + 48 == F(111, 2)
    add("A puppy weighed 7 lb 8 oz. It gained 6 oz a week for 8 weeks. How much does it weigh now, in pounds?",
        "10 1/2 lb", ["10.8 lb", "13 1/2 lb", "55 1/2 lb"],
        "Step 1: 8 × 6 = 48 oz gained. 48 ÷ 16 = 3 lb. Step 2: 7 lb 8 oz = 7 1/2 lb, and 7 1/2 + 3 = <b>10 1/2 lb</b>. "
        "(10.8 lb is a mistake for 10 lb 8 oz, 13 1/2 lb uses 8 oz in a pound, and 55 1/2 adds 48 oz as pounds.)")
    n, he, his = P.next()
    assert F(5, 2) * 1000 / 500 * 7 == 35
    add("%s drinks 2 1/2 L of water every day from 500 mL bottles. How many bottles does %s drink in a week?" % (n, he),
        "35 bottles", ["5 bottles", "3 1/2 bottles", "17 1/2 bottles"],
        "Step 1: 2 1/2 L = 2,500 mL, and 2,500 ÷ 500 = 5 bottles a day. Step 2: 7 × 5 = <b>35 bottles</b>. "
        "(5 is only one day, 3 1/2 uses 1 L = 100 mL, and 17 1/2 multiplies 2 1/2 × 7 without converting.)")
    n, he, his = P.next()
    assert F(5280, 4) / 120 == 11
    add("%s runs 1/4 mi in 2 minutes. What is %s speed in feet per second?" % (n, his),
        "11 ft per sec", ["22 ft per sec", "660 ft per sec", "1,320 ft per sec"],
        "Change both parts. Distance: 1/4 mi = 5,280 ÷ 4 = 1,320 ft. Time: 2 min = 120 sec. "
        "1,320 ÷ 120 = <b>11 ft per second</b>. (22 divides by 60 and forgets that it took 2 minutes, "
        "660 is feet per minute, and 1,320 is the whole distance, not the speed.)")
    assert len(its) == 20, len(its)
    order = [0, 1, 2, 3, 4, 5, 6, 7, 12, 8, 9, 10, 11, 13, 14, 15, 16, 17, 18, 19]
    assert sorted(order) == list(range(20))
    return {"title": "Multi-step word problems", "items": [its[i] for i in order]}


# ------------------------------------------------------------ lesson
def ex(title, qs, s, a):
    return ("<div class='sn-ex'><span class='sn-ex-t'>%s</span><p class='sn-ex-q'>%s</p>"
            "<p class='sn-ex-s'>%s</p><p class='sn-ex-a'>Answer: %s</p></div>" % (title, qs, s, a))


def table(head, rows):
    h = "".join("<th>%s</th>" % x for x in head)
    b = "".join("<tr>" + "".join("<td>%s</td>" % c for c in r) + "</tr>" for r in rows)
    return "<div class='sn-tw'><table class='sn-table'><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>" % (h, b)


def body_html():
    t1 = ratio_table("ft", "in", ["1", "2", "3", "4", "5"], ["12", "24", "36", "48", "60"], None)
    d1 = dnl("gal", "qt", ["0", "1", "2", "3", "4"], ["0", "4", "8", "12", "16"], None)
    return H(
        "<h2>The big idea</h2>"
        "<p>Every conversion fact is a <b>ratio</b>. 1 ft = 12 in means the ratio of feet to inches is <b>1 : 12</b>. "
        "Equivalent ratios give every other conversion: 2 : 24, 3 : 36, 5 : 60.</p>"
        "<figure class='sn-fig'>" + t1 +
        "<figcaption>A ratio table for 1 ft : 12 in. Each inches number is 12 × the feet number.</figcaption></figure>"
        "<h2>Multiply or divide?</h2>"
        "<p>To a <b>smaller</b> unit, you need <b>more</b> of them: multiply. "
        "To a <b>bigger</b> unit, you need <b>fewer</b> of them: divide.</p>" +
        ex("Both ways", "5 yd = ☐ ft &nbsp; and &nbsp; 48 oz = ☐ lb",
           "1 yd : 3 ft, so 5 × 3 = 15. 1 lb : 16 oz, so 48 ÷ 16 = 3.", "15 ft and 3 lb") +
        "<figure class='sn-fig'>" + d1 +
        "<figcaption>A double number line for 1 gal : 4 qt. 3 gal lines up with 12 qt.</figcaption></figure>"
        "<h2>Let the units cancel</h2>"
        "<p>Multiply by a fraction equal to 1, like " + UF("1 yd", "3 ft") + ". Put the unit you want to remove on the bottom.</p>" +
        ex("Feet to yards", "9 ft = ☐ yd",
           "9 ft × " + UF("1 yd", "3 ft") + " = 9 ÷ 3 yd. The feet cancel.", "3 yd") +
        "<h2>Between systems</h2>"
        "<p>Use the rate you are given, such as 1 in = 2.54 cm or 1 kg ≈ 2.2 lb (about).</p>" +
        ex("Inches to centimeters", "Use 1 in = 2.54 cm. 10 in = ☐ cm",
           "A centimeter is smaller, so multiply: 10 × 2.54 = 25.4.", "25.4 cm") +
        "<h2>Converting a rate</h2>"
        "<p>A rate has two units. Change one part or both, one at a time.</p>" +
        ex("Miles per hour", "60 mi per hr = ☐ mi per min",
           "1 hr = 60 min, so 60 miles in 60 minutes is 60 ÷ 60 = 1 mile each minute.", "1 mi per min") +
        ex("Price per ounce", "$4.80 per lb = ☐ per oz",
           "1 lb = 16 oz, so 1 ounce costs $4.80 ÷ 16 = $0.30.", "$0.30 per oz") +
        "<h2>Common mistakes</h2>" +
        table(["Mistake", "What to do instead"], [
            ["Multiplying to get a bigger unit (6 ft = 18 yd)", "Bigger unit, fewer of them: 6 ft ÷ 3 = 2 yd"],
            ["Using the wrong fact (1 yd = 12 in)", "1 yd = 3 ft = 36 in. 1 ft = 12 in"],
            ["Mixing up capacity (1 gal = 2 qt)", "1 gal = 4 qt, 1 qt = 2 pt, 1 pt = 2 cups"],
            ["Using 100 for kilo (1 km = 100 m)", "Kilo means 1,000: 1 km = 1,000 m, 1 kg = 1,000 g"],
            ["Adding to both parts of a ratio (1 : 12 → 5 : 16)", "Multiply both parts: 1 : 12 → 5 : 60"],
            ["Changing only one part of a rate", "90 km per hr: change km to m AND hours to minutes"],
        ])
    )


FAQ = [
    {"q": "How do you use ratios to convert units in 6th grade?",
     "a": "Write the conversion fact as a ratio, such as 1 ft : 12 in, then find an equivalent ratio with a ratio table, "
          "a double number line or multiplication: 5 ft : 60 in."},
    {"q": "How do you know whether to multiply or divide when converting units?",
     "a": "To a smaller unit, multiply, because you need more of them (5 yd = 15 ft). To a bigger unit, divide, "
          "because you need fewer of them (48 oz = 3 lb)."},
    {"q": "How do you convert 60 miles per hour to miles per minute?",
     "a": "An hour has 60 minutes, so divide both numbers by 60: 60 miles per hour = 1 mile per minute."},
    {"q": "What does 6.RP.A.3d mean?",
     "a": "It is the Common Core Grade 6 standard for using ratio reasoning to convert measurement units, "
          "including converting rates and handling units correctly when you multiply or divide."},
]


def gen():
    rnd = random.Random(620)
    sets = [set_ratio(rnd), set_tables(), set_mixed(), set_rates(), set_story(rnd)]
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
        "country": "us", "subject": "math", "grade": "grade-6", "slug": "converting-units-with-ratios", "sort": 20,
        "updated": UPDATED, "pdf_url": "",
        "title": "Converting Units with Ratios",
        "seo_title": "Grade 6 Converting Units with Ratios Worksheets: Ratio Tables, Double Number Lines, Rates",
        "short_title": "Converting units with ratios",
        "domain": "Ratios and Proportional Relationships",
        "standard_code": "6.RP.A.3d",
        "standard_url": "https://www.thecorestandards.org/Math/Content/6/RP/A/3/",
        "standard_text": "Use ratio reasoning to convert measurement units; manipulate and transform units appropriately when multiplying or dividing quantities.",
        "meta_desc": "Free Grade 6 worksheets on converting units with ratios: use 1 ft : 12 in style conversion ratios, ratio tables and double number lines, fractions and decimals of units, inches to centimeters with 1 in = 2.54 cm, and converting rates like 60 miles per hour = 1 mile per minute. 100 practice questions with an answer key and step-by-step explanations.",
        "key_big": "A conversion fact is a ratio. Use equivalent ratios to convert.",
        "key_sub": "1 ft : 12 in, so 5 ft : 60 in. To a smaller unit, multiply (5 yd = 15 ft). To a bigger unit, divide (48 oz = 3 lb). For a rate, convert both parts: 60 mi per hr = 1 mi per min.",
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
        mark_large(u, "(ratio table|double number line)")
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
