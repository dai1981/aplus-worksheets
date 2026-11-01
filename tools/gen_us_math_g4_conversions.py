# -*- coding: utf-8 -*-
"""
US Grade 4 Math: Measurement Conversions (4.MD.A.1-2)
  python tools/gen_us_math_g4_conversions.py
HTML attributes use single quotes (no backslashes in the JSON).
Grade 4 style: numbers 1,000 and above are written with commas.
"""
import json, os, random, re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "us", "math", "grade-4")
UPDATED = "2026-11-02"
GREEN = "#006633"
FILL = "#cfe6d6"
FILL2 = "#eef6f0"
RED = "#c0392b"
INK = "#2b2b2b"
FONT = "Arial, Helvetica, sans-serif"
GIRLS = ["Maya", "Ava", "Mia", "Zoe", "Lily", "Emma", "Nora", "Ruby", "Sofia", "Grace"]
BOYS = ["Leo", "Noah", "Eli", "Sam", "Ben", "Omar", "Kai", "Jack", "Luis", "Owen"]


# ------------------------------------------------------------ helpers
def f(n):
    """Grade 4 style: 4536 -> 4,536."""
    return "{:,}".format(n)


def mcq(q, correct, cands, e, rnd):
    """4 choices: correct + 3 unique distractors (no zero or negative numbers)."""
    correct = str(correct)
    seen = {correct}
    pick = []
    for c in cands:
        c = str(c)
        lead = c.split(" ")[0].lstrip("$")
        if c in seen or not c or lead.startswith("-") or lead == "0":
            continue
        seen.add(c)
        pick.append(c)
        if len(pick) == 3:
            break
    assert len(pick) == 3, (q, correct, cands)
    ch = pick + [correct]
    rnd.shuffle(ch)
    return {"q": q, "c": ch, "a": ch.index(correct), "e": e}


class People:
    def __init__(self, rnd):
        self.pool = [(n, "she", "her") for n in GIRLS] + [(n, "he", "his") for n in BOYS]
        rnd.shuffle(self.pool)
        self.i = 0

    def next(self):
        p = self.pool[self.i % len(self.pool)]
        self.i += 1
        return p


def cap(s):
    return s[0].upper() + s[1:]


def fig(svg):
    return "<div class='qfig'>" + svg + "</div>"


def svg_wrap(w, h, body, label):
    return ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 %d %d' width='%d' height='%d' "
            "role='img' aria-label='%s'><g font-family='%s'>%s</g></svg>" % (w, h, w, h, label, FONT, body))


def text(x, y, t, fs=17, anchor="middle", bold=True, col=INK):
    return ("<text x='%.1f' y='%.1f' font-size='%d'%s fill='%s' text-anchor='%s'>%s</text>"
            % (x, y, fs, " font-weight='700'" if bold else "", col, anchor, t))


def frac(a, b):
    return "<span class='fr'><span class='fn'>%d</span><span class='fd'>%d</span></span>" % (a, b)


# ------------------------------------------------------------ units
# key: (abbreviation, singular, plural)
U = {
    "km": ("km", "kilometer", "kilometers"), "m": ("m", "meter", "meters"), "cm": ("cm", "centimeter", "centimeters"),
    "kg": ("kg", "kilogram", "kilograms"), "g": ("g", "gram", "grams"),
    "L": ("L", "liter", "liters"), "mL": ("mL", "milliliter", "milliliters"),
    "lb": ("lb", "pound", "pounds"), "oz": ("oz", "ounce", "ounces"),
    "yd": ("yd", "yard", "yards"), "ft": ("ft", "foot", "feet"), "in": ("in", "inch", "inches"),
    "hr": ("hr", "hour", "hours"), "min": ("min", "minute", "minutes"), "sec": ("sec", "second", "seconds"),
    "day": (None, "day", "days"), "wk": (None, "week", "weeks"),
}

# (big, small, how many small in 1 big, typical wrong factors)
FACTS = {
    "km": ("km", "m", 1000, [100, 10, 60]),
    "m": ("m", "cm", 100, [1000, 10, 12]),
    "kg": ("kg", "g", 1000, [100, 10, 16]),
    "L": ("L", "mL", 1000, [100, 10, 60]),
    "lb": ("lb", "oz", 16, [12, 10, 100]),
    "ft": ("ft", "in", 12, [10, 16, 3]),
    "yd": ("yd", "ft", 3, [12, 10, 36]),
    "hr": ("hr", "min", 60, [100, 24, 10]),
    "min": ("min", "sec", 60, [100, 10, 24]),
    "day": ("day", "hr", 24, [12, 60, 7]),
    "wk": ("wk", "day", 7, [5, 10, 24]),
}
WHY = {
    "km": "Kilo means 1,000, so 1 km = 1,000 m.",
    "m": "Centi means one hundredth, so 1 m = 100 cm.",
    "kg": "Kilo means 1,000, so 1 kg = 1,000 g.",
    "L": "Milli means one thousandth, so 1 L = 1,000 mL.",
    "lb": "1 lb = 16 oz (not 10 or 12).",
    "ft": "1 ft = 12 in. A 12-inch ruler is exactly 1 foot long.",
    "yd": "1 yd = 3 ft. A yardstick is as long as 3 rulers.",
    "hr": "1 hr = 60 min (not 100), so 1 hour is 60 times as long as 1 minute.",
    "min": "1 min = 60 sec (not 100).",
    "day": "1 day = 24 hr.",
    "wk": "1 week = 7 days.",
}


def word(u, n):
    a, s, p = U[u]
    return s if n == 1 else p


def m(n, u):
    """'5 kg', '3 days', '1 week'. Abbreviations have no plural."""
    a, s, p = U[u]
    if a is None:
        return "%s %s" % (f(n), s if n == 1 else p)
    return "%s %s" % (f(n), a)


def mw(n, u):
    """Measurement with the full word: '1 foot', '3 feet'."""
    return "%s %s" % (f(n), word(u, n))


def fact(key):
    b, s, k, _ = FACTS[key]
    return "%s = %s" % (m(1, b), m(k, s))


# ------------------------------------------------------------ figure: two-column table
def conv_table(b, s, rows, miss=None):
    """Two-column conversion table. rows = [(big, small)]; miss = (row, col) shown as a red ?."""
    CW, HH, RH = 136, 34, 32
    W = CW * 2 + 4
    H = HH + RH * len(rows) + 4
    o = []
    o.append("<rect x='2' y='2' width='%d' height='%d' fill='%s'/>" % (CW * 2, HH, GREEN))
    for c, u in enumerate([b, s]):
        o.append(text(2 + CW * c + CW / 2, 2 + HH / 2 + 6, cap(U[u][2]), 16, col="#ffffff"))
    for r, row in enumerate(rows):
        y = 2 + HH + RH * r
        o.append("<rect x='2' y='%d' width='%d' height='%d' fill='%s'/>" % (y, CW * 2, RH, FILL2 if r % 2 else "#ffffff"))
        for c, v in enumerate(row):
            cx = 2 + CW * c + CW / 2
            if miss == (r, c):
                o.append("<rect x='%.1f' y='%d' width='60' height='24' rx='4' fill='none' stroke='%s' stroke-width='2' "
                         "stroke-dasharray='5 3'/>" % (cx - 30, y + 4, RED))
                o.append(text(cx, y + RH / 2 + 6, "?", 18, col=RED))
            else:
                o.append(text(cx, y + RH / 2 + 6, f(v), 17))
    for r in range(len(rows)):
        y = 2 + HH + RH * (r + 1)
        o.append("<line x1='2' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='1'/>" % (y, 2 + CW * 2, y, "#b9d6c2"))
    o.append("<line x1='%d' y1='2' x2='%d' y2='%d' stroke='%s' stroke-width='2'/>" % (2 + CW, 2 + CW, H - 2, GREEN))
    o.append("<rect x='2' y='2' width='%d' height='%d' fill='none' stroke='%s' stroke-width='2.5'/>" % (CW * 2, H - 4, GREEN))
    lab = "conversion table: %s and %s" % (U[b][2], U[s][2])
    return svg_wrap(W, H, "".join(o), lab)


# ------------------------------------------------------------ set 1: relative sizes
def set_sizes(rnd):
    its = []
    asks = {
        "km": "How many meters are in 1 kilometer?",
        "m": "How many centimeters are in 1 meter?",
        "kg": "How many grams are in 1 kilogram?",
        "L": "How many milliliters are in 1 liter?",
        "lb": "How many ounces are in 1 pound?",
        "ft": "How many inches are in 1 foot?",
        "yd": "How many feet are in 1 yard?",
        "hr": "1 hour is how many times as long as 1 minute?",
        "min": "How many seconds are in 1 minute?",
    }
    for key, q in asks.items():
        b, s, k, wr = FACTS[key]
        if key == "hr":
            right, wrong = "%d times" % k, ["%d times" % w for w in wr]
        else:
            right, wrong = mw(k, s), [mw(w, s) for w in wr]
        its.append(mcq(q, right, wrong, WHY[key], rnd))
    bench = [
        ("A classroom door is about how tall?", "about 2 m", ["about 2 cm", "about 2 km", "about 20 m"],
         "A door is a little taller than a grown-up, about 2 meters. 2 cm is shorter than your finger, and 2 km is a long walk."),
        ("What is the mass of a paper clip?", "about 1 g", ["about 1 kg", "about 100 g", "about 10 kg"],
         "A paper clip is very light. Its mass is about 1 gram. 1 kilogram is about the mass of a pineapple."),
        ("What is the mass of a pineapple?", "about 1 kg", ["about 1 g", "about 100 kg", "about 10 g"],
         "A pineapple has a mass of about 1 kilogram (1,000 g). 1 g is the mass of a paper clip."),
        ("How much water does a small water bottle hold?", "about 500 mL", ["about 500 L", "about 5 mL", "about 50 L"],
         "A small water bottle holds about 500 milliliters, which is half of 1 liter. 5 mL is just one spoonful."),
        ("You walk for about 15 minutes. About how far do you go?", "about 1 km", ["about 1 m", "about 1 cm", "about 100 km"],
         "In 15 minutes you can walk about 1 kilometer (1,000 m). 1 m is just one big step."),
        ("What is the weight of a loaf of bread?", "about 1 lb", ["about 1 oz", "about 16 lb", "about 100 lb"],
         "A loaf of bread weighs about 1 pound (16 ounces). 1 ounce is about the weight of a slice of bread."),
        ("How long does it take to brush your teeth?", "about 2 minutes", ["about 2 seconds", "about 2 hours", "about 20 hours"],
         "Brushing your teeth takes about 2 minutes. 2 seconds is far too short, and 2 hours is far too long."),
    ]
    for q, r, w, e in bench:
        its.append(mcq(q, r, w, e, rnd))
    orders = [
        ("Which list goes from the shortest unit of time to the longest?", "sec, min, hr",
         ["hr, min, sec", "min, sec, hr", "sec, hr, min"], "1 min = 60 sec and 1 hr = 60 min, so second < minute < hour."),
        ("Which list goes from the shortest unit of length to the longest?", "in, ft, yd",
         ["yd, ft, in", "ft, in, yd", "in, yd, ft"], "1 ft = 12 in and 1 yd = 3 ft, so inch < foot < yard."),
        ("Which list goes from the shortest unit of length to the longest?", "cm, m, km",
         ["km, m, cm", "m, cm, km", "cm, km, m"], "1 m = 100 cm and 1 km = 1,000 m, so centimeter < meter < kilometer."),
    ]
    for q, r, w, e in orders:
        its.append(mcq(q, r, w, e, rnd))
    its.append(mcq("Which is true?", "1 lb > 1 oz", ["1 in > 1 ft", "1 g > 1 kg", "1 mL > 1 L"],
                   "1 pound = 16 ounces, so a pound is heavier than an ounce. The others are backward: 1 ft = 12 in, "
                   "1 kg = 1,000 g, and 1 L = 1,000 mL.", rnd))
    rnd.shuffle(its)
    return {"title": "How big is each unit?", "items": its}


# ------------------------------------------------------------ set 2: bigger unit -> smaller unit
def conv_cands(n, key):
    b, s, k, wr = FACTS[key]
    return [n * wr[0], n * wr[1], n + k, n * wr[2]]


def conv_e(n, key):
    b, s, k, _ = FACTS[key]
    return ("%s. %s are bigger than %s, so you need more %s: multiply. %s × %s = %s, so %s = %s."
            % (fact(key), cap(word(b, 2)), word(s, 2), word(s, 2), f(n), f(k), f(n * k), m(n, b), m(n * k, s)))


def conv_item(n, key, rnd, words):
    b, s, k, _ = FACTS[key]
    if words:
        q = "How many %s are in %s?" % (word(s, 2), mw(n, b))
        fm = lambda v: mw(v, s)
    else:
        q = "Convert. <b>%s = ☐ %s</b>" % (m(n, b), U[s][0] or word(s, 2))
        fm = lambda v: m(v, s)
    return mcq(q, fm(n * k), [fm(v) for v in conv_cands(n, key)], conv_e(n, key), rnd)


def set_convert(rnd):
    keys = ["km", "m", "kg", "L", "lb", "ft", "yd", "hr", "min", "wk"]
    small_n = {"km": (2, 9), "m": (2, 9), "kg": (2, 9), "L": (2, 9), "lb": (2, 6), "ft": (2, 9), "yd": (4, 9),
               "hr": (2, 9), "min": (2, 9), "wk": (2, 9)}
    big_n = {"km": (11, 25), "m": (12, 45), "kg": (11, 30), "L": (11, 20), "lb": (7, 12), "ft": (11, 25), "yd": (12, 40),
             "hr": (10, 12), "min": (10, 15), "day": (3, 7)}
    easy, hard = [], []
    for i, key in enumerate(keys):
        n = rnd.randint(*small_n[key])
        easy.append(conv_item(n, key, rnd, i % 2 == 1))
    for i, key in enumerate(["km", "m", "kg", "L", "lb", "ft", "yd", "hr", "min", "day"]):
        n = rnd.randint(*big_n[key])
        hard.append(conv_item(n, key, rnd, i % 2 == 0))
    rnd.shuffle(easy)
    rnd.shuffle(hard)
    return {"title": "Change to a smaller unit", "items": easy + hard}


# ------------------------------------------------------------ set 3: two-column tables
def table_rows(rnd, k, lo=1):
    xs = sorted(rnd.sample(range(lo, lo + 8), 4))
    return [(x, x * k) for x in xs]


def set_tables(rnd):
    its = []
    keys = ["kg", "ft", "hr", "L", "lb", "km", "yd", "min", "m", "wk", "day", "lb"]
    for i, key in enumerate(keys):
        b, s, k, wr = FACTS[key]
        rows = table_rows(rnd, k, lo=1 if i < 6 else 2)
        r = 3 if i % 3 != 2 else rnd.randint(1, 2)
        left = i in (8, 10)
        L, R = rows[r]
        if left:
            miss = (r, 0)
            ans = L
            wrong = [R - k, R * k, L * 10, L + 1]
            e = ("Each row follows the rule %s. Go backward: how many %s make %s? %s ÷ %s = %s. Check: %s × %s = %s."
                 % (fact(key), word(b, 2), m(R, s), f(R), f(k), f(L), f(L), f(k), f(R)))
            q = "What number goes in the ? box?"
        else:
            miss = (r, 1)
            ans = R
            prev = rows[r - 1][1]
            wrong = [L * w for w in wr[:2]] + [prev + k, L + k]
            e = ("%s, so every number on the right is the left number × %s. %s × %s = %s."
                 % (fact(key), f(k), f(L), f(k), f(R)))
            q = "What number goes in the ? box?"
        its.append(mcq(fig(conv_table(b, s, rows, miss)) + q, f(ans), [f(v) for v in wrong], e, rnd))
    # which rule?
    for key in ["kg", "lb", "min", "yd"]:
        b, s, k, wr = FACTS[key]
        rows = table_rows(rnd, k)
        right = "× %s" % f(k)
        wrong = ["× %s" % f(wr[0]), "+ %s" % f(k), "÷ %s" % f(k)]
        a0, c0 = rows[1]
        e = ("%s. Each left number times %s gives the right number, for example %s × %s = %s. "
             "Adding %s does not work: %s + %s = %s, not %s."
             % (fact(key), f(k), f(a0), f(k), f(c0), f(k), f(a0), f(k), f(a0 + k), f(c0)))
        its.append(mcq(fig(conv_table(b, s, rows)) + "Which rule changes the left column into the right column?",
                       right, wrong, e, rnd))
    # which row belongs?
    for key in ["ft", "hr", "m", "L"]:
        b, s, k, wr = FACTS[key]
        rows = table_rows(rnd, k)
        used = {a for a, _ in rows}
        n = max(used) + rnd.randint(1, 3)
        right = "%s = %s" % (m(n, b), m(n * k, s))
        wrong = ["%s = %s" % (m(n, b), m(n * wr[0], s)),
                 "%s = %s" % (m(n, b), m(n + k, s)),
                 "%s = %s" % (m(n * k, b), m(n, s))]
        e = ("%s, so the right number is always the left number × %s. %s × %s = %s, so %s fits."
             % (fact(key), f(k), f(n), f(k), f(n * k), right))
        its.append(mcq(fig(conv_table(b, s, rows)) + "Which row could be added to this table?", right, wrong, e, rnd))
    rnd.shuffle(its)
    return {"title": "Two-column conversion tables", "items": its}


# ------------------------------------------------------------ set 4: mixed units and comparing
def set_mixed(rnd):
    its = []
    mixed = [(2, "ft", 5), (3, "hr", 20), (4, "kg", 250), (4, "m", 8), (2, "lb", 7),
             (5, "km", 300), (2, "L", 750), (4, "min", 15), (3, "yd", 2), (2, "kg", 50)]
    for a, key, c in mixed:
        b, s, k, wr = FACTS[key]
        ans = a * k + c
        wrong = [int("%d%d" % (a, c)), a * k, a * wr[0] + c, a + k + c]
        q = "Convert. <b>%s %s = ☐ %s</b>" % (m(a, b), m(c, s), U[s][0])
        e = ("Change the %s first: %s × %s = %s. Then add the leftover %s: %s + %s = %s."
             % (word(b, 2), f(a), f(k), m(a * k, s), word(s, 2), f(a * k), f(c), m(ans, s)))
        its.append(mcq(q, m(ans, s), [m(v, s) for v in wrong], e, rnd))
    rnd.shuffle(its)
    big = [
        ("Which is the longest?", ["5 ft", "58 in", "55 in", "1 yd 1 ft"], [60, 58, 55, 48], "in", max,
         "5 ft = 60 in and 1 yd 1 ft = 3 ft + 1 ft = 48 in"),
        ("Which is the heaviest?", ["2 kg", "1,950 g", "2 kg 75 g", "2,070 g"], [2000, 1950, 2075, 2070], "g", max,
         "2 kg = 2,000 g and 2 kg 75 g = 2,075 g"),
        ("Which is the longest amount of time?", ["2 hr", "100 min", "1 hr 50 min", "130 min"], [120, 100, 110, 130],
         "min", max, "2 hr = 120 min (not 200) and 1 hr 50 min = 110 min"),
        ("Which is the shortest?", ["4 m", "350 cm", "3 m 60 cm", "410 cm"], [400, 350, 360, 410], "cm", min,
         "4 m = 400 cm and 3 m 60 cm = 360 cm"),
        ("Which holds the most?", ["1 L", "900 mL", "1 L 50 mL", "1,100 mL"], [1000, 900, 1050, 1100], "mL", max,
         "1 L = 1,000 mL and 1 L 50 mL = 1,050 mL"),
        ("Which is the lightest?", ["2 lb", "30 oz", "1 lb 15 oz", "34 oz"], [32, 30, 31, 34], "oz", min,
         "2 lb = 32 oz (not 20) and 1 lb 15 oz = 31 oz"),
    ]
    cmp = []
    for q, ch, vals, u, fn, how in big:
        i = vals.index(fn(vals))
        order = sorted(range(4), key=lambda j: vals[j], reverse=(fn is max))
        e = ("Change everything to %s: %s. In order: %s. So the answer is %s."
             % (word(u, 2), how, ", ".join(m(vals[j], u) for j in order), ch[i]))
        cmp.append(mcq(q, ch[i], [c for j, c in enumerate(ch) if j != i], e, rnd))
    true = [
        ("3 hr < 200 min", ["3 hr = 300 min", "2 hr > 150 min", "1 hr = 100 min"],
         "1 hr = 60 min, so 3 hr = 180 min, and 180 < 200. 2 hr = 120 min, which is less than 150 min."),
        ("4 ft = 48 in", ["4 ft = 40 in", "4 ft < 40 in", "5 ft = 15 in"],
         "1 ft = 12 in, so 4 ft = 4 × 12 = 48 in. 5 ft = 60 in (15 is the number of feet in 5 yards)."),
        ("2 km > 1,900 m", ["2 km = 200 m", "2 km < 1,900 m", "3 km = 300 m"],
         "1 km = 1,000 m, so 2 km = 2,000 m, and 2,000 > 1,900. 3 km = 3,000 m, not 300 m."),
        ("3 lb = 48 oz", ["3 lb = 36 oz", "2 lb < 30 oz", "3 lb < 40 oz"],
         "1 lb = 16 oz, so 3 lb = 3 × 16 = 48 oz. 2 lb = 32 oz, which is more than 30 oz."),
    ]
    for r, w, e in true:
        cmp.append(mcq("Which is true?", r, w, e, rnd))
    rnd.shuffle(cmp)
    return {"title": "Mixed units and comparing", "items": its + cmp}


# ------------------------------------------------------------ set 5: word problems
def money(c):
    """cents -> '$1.25'"""
    return "$%s.%02d" % (f(c // 100), c % 100)


def set_story(rnd):
    P = People(rnd)
    its = []

    def add(q, r, w, e):
        its.append(mcq(q, r, w, e, rnd))

    n, he, his = P.next()
    add("%s has a rope that is 3 m long. %s cuts off 85 cm. How long is the rope now?" % (n, cap(he)),
        "215 cm", ["385 cm", "2,915 cm", "225 cm"],
        "Use the same unit: 3 m = 300 cm. The rope gets shorter, so subtract: 300 − 85 = 215 cm.")
    add("A pitcher holds 3 L of lemonade. How many 500 mL bottles can be filled from the pitcher?",
        "6 bottles", ["3 bottles", "60 bottles", "1,500 bottles"],
        "3 L = 3,000 mL. How many groups of 500 mL are in 3,000 mL? 3,000 ÷ 500 = 6 bottles.")
    add("A movie starts at 6:45 p.m. It is 1 hr 50 min long. What time does it end?",
        "8:35 p.m.", ["7:35 p.m.", "8:45 p.m.", "8:35 a.m."],
        "Add 1 hour: 7:45 p.m. Add 50 minutes: 15 minutes gets to 8:00, then 35 more minutes is 8:35 p.m.")
    n, he, his = P.next()
    add("%s's soccer practice starts at 3:40 p.m. and ends at 5:15 p.m. How long is practice?" % n,
        "1 hr 35 min", ["2 hr 25 min", "1 hr 75 min", "2 hr 35 min"],
        "From 3:40 to 4:40 is 1 hour. From 4:40 to 5:00 is 20 minutes, and 5:00 to 5:15 is 15 minutes. "
        "1 hr + 20 min + 15 min = 1 hr 35 min.")
    n, he, his = P.next()
    add("%s reads for %s hour on Monday and %s hour on Tuesday. How many minutes does %s read in all?"
        % (n, frac(1, 2), frac(1, 4), he),
        "45 minutes", ["75 minutes", "15 minutes", "30 minutes"],
        "1 hour = 60 minutes. Half of 60 is 30, and one fourth of 60 is 15. In all: 30 + 15 = 45 minutes.")
    n, he, his = P.next()
    add("%s has $5.00. %s buys a juice for $1.35 and a muffin for $2.40. How much change does %s get?" % (n, cap(he), he),
        money(125), [money(375), money(875), money(275)],
        "Step 1: the cost: $1.35 + $2.40 = $3.75. Step 2: the change: $5.00 − $3.75 = $1.25.")
    n, he, his = P.next()
    add("Pencils cost 45 cents each. %s buys 6 pencils. How much does %s pay?" % (n, he),
        money(270), [money(2700), money(240), money(51)],
        "6 × 45 cents = 270 cents. 100 cents = $1, so 270 cents = $2.70.")
    add("Four friends share the cost of an $18.00 pizza equally. How much does each friend pay?",
        money(450), [money(420), money(7200), money(1400)],
        "Share equally, so divide: $18.00 ÷ 4. 18 ÷ 4 = 4 with 2 dollars left over. 2 dollars = 200 cents, and "
        "200 ÷ 4 = 50 cents. Each friend pays $4.50 (not $4.20).")
    add("A bag has 2 kg of flour. A baker uses 750 g. How many grams of flour are left?",
        "1,250 g", ["748 g", "2,750 g", "1,350 g"],
        "Use the same unit: 2 kg = 2,000 g. Then subtract: 2,000 − 750 = 1,250 g.")
    add("A bag holds 8 apples. Each apple has a mass of 150 g. What is the mass of all the apples?",
        "1 kg 200 g", ["12 kg", "1 kg 20 g", "1,200 kg"],
        "8 × 150 = 1,200 g. 1,000 g = 1 kg, so 1,200 g = 1 kg 200 g.")
    n, he, his = P.next()
    add("%s has a board that is 6 feet long. %s cuts it into pieces that are 8 inches long. How many pieces does %s get?"
        % (n, cap(he), he),
        "9 pieces", ["12 pieces", "48 pieces", "7 pieces"],
        "6 ft = 6 × 12 = 72 in. How many 8-inch pieces are in 72 inches? 72 ÷ 8 = 9 pieces.")
    n, he, his = P.next()
    add("%s needs 5 yards of ribbon. %s has 12 feet of ribbon. How many more feet does %s need?" % (n, cap(he), he),
        "3 ft", ["7 ft", "48 ft", "27 ft"],
        "5 yd = 5 × 3 = 15 ft. Find the missing part: 15 − 12 = 3 ft.")
    n, he, his = P.next()
    add("%s runs 3 km and then walks 450 m. How many meters does %s go in all?" % (n, he),
        "3,450 m", ["453 m", "750 m", "3,045 m"],
        "3 km = 3,000 m. Add: 3,000 + 450 = 3,450 m.")
    add("A relay race is 2 km long. Four runners each run the same distance. How many meters does each runner run?",
        "500 m", ["50 m", "8,000 m", "2,000 m"],
        "2 km = 2,000 m. Share it equally: 2,000 ÷ 4 = 500 m.")
    n, he, his = P.next()
    add("%s drinks 3 glasses of milk every day. Each glass holds 250 mL. How much milk does %s drink in 1 week?" % (n, he),
        "5,250 mL", ["750 mL", "1,750 mL", "5,250 L"],
        "One day: 3 × 250 = 750 mL. 1 week = 7 days, so 7 × 750 = 5,250 mL.")
    n, he, his = P.next()
    add("A recipe needs 1 pound of cheese. %s has 10 ounces. How many more ounces does %s need?" % (n, he),
        "6 oz", ["2 oz", "90 oz", "9 oz"],
        "1 lb = 16 oz. Find the missing part: 16 − 10 = 6 oz.")
    n, he, his = P.next()
    add("A song is 3 minutes 25 seconds long. %s plays it 2 times. How many seconds is that?" % n,
        "410 seconds", ["650 seconds", "360 seconds", "205 seconds"],
        "3 min = 3 × 60 = 180 sec, so the song is 180 + 25 = 205 seconds. 2 times: 2 × 205 = 410 seconds.")
    add("A family drives for 3 hours on Saturday and 2 %s hours on Sunday. How many minutes do they drive in all?" % frac(1, 2),
        "330 minutes", ["550 minutes", "300 minutes", "530 minutes"],
        "Saturday: 3 × 60 = 180 min. Sunday: 2 × 60 = 120 min, plus %s hour = 30 min, so 150 min. "
        "In all: 180 + 150 = 330 minutes." % frac(1, 2))
    add("A bean plant grows for 3 weeks and 4 days. How many days is that?",
        "25 days", ["34 days", "21 days", "19 days"],
        "1 week = 7 days, so 3 weeks = 21 days. Add the leftover 4 days: 21 + 4 = 25 days.")
    n, he, his = P.next()
    add("A 2 L bottle of water costs $1.80. A 500 mL bottle costs $0.65. %s needs 2 L of water. "
        "How much does %s save by buying the 2 L bottle instead of 500 mL bottles?" % (n, he),
        money(80), [money(115), money(260), money(440)],
        "2 L = 2,000 mL, and 2,000 ÷ 500 = 4 small bottles. 4 × $0.65 = $2.60. Savings: $2.60 − $1.80 = $0.80.")
    assert len(its) == 20, len(its)
    rnd.shuffle(its)
    return {"title": "Word problems with measurements and money", "items": its}


# ------------------------------------------------------------ lesson
def ex(title, q, s, a):
    return ("<div class='sn-ex'><span class='sn-ex-t'>%s</span><p class='sn-ex-q'>%s</p>"
            "<p class='sn-ex-s'>%s</p><p class='sn-ex-a'>Answer: %s</p></div>" % (title, q, s, a))


def table(head, rows, cls="sn-table"):
    h = "".join("<th>%s</th>" % x for x in head)
    b = "".join("<tr>" + "".join("<td>%s</td>" % c for c in r) + "</tr>" for r in rows)
    return "<div class='sn-tw'><table class='%s'><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>" % (cls, h, b)


def body_html():
    return (
        "<h2>Bigger unit to smaller unit: multiply</h2>"
        "<p>A foot is longer than an inch, so it takes <b>more</b> inches to cover the same length. "
        "To change a bigger unit into a smaller unit, <b>multiply</b> by how many small units are in 1 big unit.</p>" +
        ex("Feet to inches", "3 ft = ☐ in", "1 ft = 12 in. Multiply: 3 × 12 = 36.", "36 in") +
        "<h2>Conversion facts to know</h2>" +
        table(["Measure", "Facts"], [
            ["Metric length", "1 km = 1,000 m &nbsp; 1 m = 100 cm"],
            ["Metric mass", "1 kg = 1,000 g"],
            ["Metric liquid volume", "1 L = 1,000 mL"],
            ["Customary length", "1 yd = 3 ft &nbsp; 1 ft = 12 in"],
            ["Customary weight", "1 lb = 16 oz"],
            ["Time", "1 hr = 60 min &nbsp; 1 min = 60 sec &nbsp; 1 day = 24 hr &nbsp; 1 week = 7 days"],
        ]) +
        "<h2>Make a two-column table</h2>"
        "<p>Write the big unit on the left and the small unit on the right. Every row uses the same rule: "
        "left number × 1,000 = right number.</p>"
        "<figure class='sn-fig'>" + conv_table("kg", "g", [(1, 1000), (2, 2000), (3, 3000), (4, 4000)]) +
        "<figcaption>1 kg = 1,000 g, so 2 kg = 2,000 g, 3 kg = 3,000 g and 4 kg = 4,000 g.</figcaption></figure>"
        "<h2>Mixed units</h2>"
        "<p>Change the big unit first, then <b>add the leftover</b> small units.</p>" +
        ex("Hours and minutes", "2 hr 15 min = ☐ min", "2 × 60 = 120 min. Add the leftover 15 min: 120 + 15 = 135.",
           "135 min") +
        "<p>To compare two measurements, change both to the same unit. 5 ft = 60 in, so 5 ft is longer than 58 in.</p>"
        "<h2>Common mistakes</h2>" +
        table(["Mistake", "What to do instead"], [
            ["Using 100 for every unit (1 hr = 100 min)", "1 hr = 60 min, 1 lb = 16 oz, 1 ft = 12 in"],
            ["Dividing to get the smaller unit (6 ft = 2 in)", "Bigger unit to smaller unit: multiply (6 ft = 72 in)"],
            ["Forgetting the leftover (2 ft 5 in = 24 in)", "Add the leftover inches: 24 + 5 = 29 in"],
            ["Writing the digits together (4 m 8 cm = 48 cm)", "4 m = 400 cm, so 4 m 8 cm = 408 cm"],
            ["Comparing only the numbers (58 in > 5 ft)", "Use one unit first: 5 ft = 60 in, and 60 > 58"],
        ])
    )


FAQ = [
    {"q": "How do you convert larger units to smaller units in 4th grade?",
     "a": "Multiply by the number of small units in 1 large unit. For example, 1 ft = 12 in, so 4 ft = 4 × 12 = 48 in."},
    {"q": "What measurement conversions should a 4th grader know?",
     "a": "1 km = 1,000 m, 1 m = 100 cm, 1 kg = 1,000 g, 1 L = 1,000 mL, 1 lb = 16 oz, 1 yd = 3 ft, 1 ft = 12 in, "
          "1 hr = 60 min and 1 min = 60 sec."},
    {"q": "What is a two-column conversion table?",
     "a": "It lists a measurement in a big unit on the left and the same measurement in a small unit on the right, "
          "such as 1 ft | 12 in, 2 ft | 24 in, 3 ft | 36 in. Every row follows the same multiplication rule."},
    {"q": "What does 4.MD.A.1 mean?",
     "a": "It is the Common Core Grade 4 standard for knowing the relative sizes of units and writing a measurement "
          "in a smaller unit, such as 3 hr = 180 min. 4.MD.A.2 uses these conversions in word problems about distance, "
          "time, volume, mass and money."},
]


def balance(sets, rnd):
    """Spread the correct answers evenly over the 4 positions in every set."""
    for s in sets:
        targets = [0, 1, 2, 3] * 5
        rnd.shuffle(targets)
        for it, t in zip(s["items"], targets):
            c = it["c"]
            c[it["a"]], c[t] = c[t], c[it["a"]]
            it["a"] = t


def gen_conversions():
    rnd = random.Random(112)
    sets = [set_sizes(rnd), set_convert(rnd), set_tables(rnd), set_mixed(rnd), set_story(rnd)]
    balance(sets, rnd)
    seen = set()
    for s in sets:
        assert len(s["items"]) == 20, (s["title"], len(s["items"]))
        for it in s["items"]:
            assert len(set(it["c"])) == 4, it
            k = it["q"] + "|" + "|".join(sorted(it["c"]))
            assert k not in seen, it["q"]
            seen.add(k)
    return {
        "country": "us", "subject": "math", "grade": "grade-4", "slug": "measurement-conversions", "sort": 12,
        "updated": UPDATED, "pdf_url": "",
        "title": "Measurement Conversions",
        "seo_title": "Grade 4 Measurement Conversion Worksheets: Metric, Customary and Time Units with Tables",
        "short_title": "Measurement conversions",
        "domain": "Measurement and Data",
        "standard_code": "4.MD.A.1–2",
        "standard_url": "https://www.thecorestandards.org/Math/Content/4/MD/A/",
        "standard_text": "Know relative sizes of measurement units within one system of units including km, m, cm; kg, g; lb, oz; l, ml; hr, min, sec. Within a single system of measurement, express measurements in a larger unit in terms of a smaller unit. Record measurement equivalents in a two-column table. Use the four operations to solve word problems involving distances, intervals of time, liquid volumes, masses of objects, and money, including problems involving simple fractions or decimals, and problems that require expressing measurements given in a larger unit in terms of a smaller unit.",
        "meta_desc": "Free Grade 4 measurement conversion worksheets: km, m, cm, kg, g, L, mL, lb, oz, ft, in, yd, hours, minutes and seconds. Two-column tables, mixed units, comparing and word problems with money. 100 practice questions with step-by-step answers.",
        "key_big": "To change a bigger unit into a smaller unit, multiply.",
        "key_sub": "There are more of the small units. 1 ft = 12 in, so 3 ft = 3 × 12 = 36 in. For mixed units, add the leftover: 2 hr 15 min = 120 + 15 = 135 min.",
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
    u = gen_conversions()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        mark_large(u, "conversion table")
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
