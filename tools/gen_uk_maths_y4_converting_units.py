# -*- coding: utf-8 -*-
"""
UK Year 4 Maths: Converting Units (National Curriculum in England, Year 4: Measurement)
  python tools/gen_uk_maths_y4_converting_units.py
HTML attributes use single quotes (no backslashes in the JSON).
British English, metric units only, numbers 1,000 and above with commas.
Every correct answer is checked in code: each measurement string is parsed back to a base unit.
"""
import json, math, os, random, re
from fractions import Fraction as Fr

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "uk", "maths", "year-4")
UPDATED = "2026-11-02"
GREEN = "#006633"
FILL = "#cfe6d6"
FILL2 = "#eef6f0"
RED = "#c0392b"
INK = "#2b2b2b"
WATER = "#9fd3f2"
WATER_LINE = "#2a7fb8"
WOOD = "#f6e7b8"
FONT = "Arial, Helvetica, sans-serif"
GIRLS = ["Amelia", "Isla", "Freya", "Poppy", "Ava", "Aisha", "Lily", "Zara", "Grace", "Ruby", "Maya", "Evie"]
BOYS = ["Oliver", "Harry", "Mohammed", "Jack", "Arjun", "Noah", "George", "Leo", "Alfie", "Kai", "Ethan", "Charlie"]


# ------------------------------------------------------------ units and checking
# unit: (family, size in the base unit, singular word, plural word)
UNIT = {
    "mm": ("L", 1, "millimetre", "millimetres"), "cm": ("L", 10, "centimetre", "centimetres"),
    "m": ("L", 1000, "metre", "metres"), "km": ("L", 1000000, "kilometre", "kilometres"),
    "g": ("M", 1, "gram", "grams"), "kg": ("M", 1000, "kilogram", "kilograms"),
    "ml": ("C", 1, "millilitre", "millilitres"), "l": ("C", 1000, "litre", "litres"),
    "second": ("T", 1, "second", "seconds"), "minute": ("T", 60, "minute", "minutes"),
    "hour": ("T", 3600, "hour", "hours"), "day": ("T", 86400, "day", "days"),
    "week": ("T", 604800, "week", "weeks"),
    "month": ("Y", 1, "month", "months"), "year": ("Y", 12, "year", "years"),
}
TIME = {"second", "minute", "hour", "day", "week", "month", "year"}
ALIAS = {}
for _k, (_fam, _sz, _s, _p) in UNIT.items():
    ALIAS[_k] = _k
    if _k in TIME:
        ALIAS[_s] = _k
        ALIAS[_p] = _k
TOK = re.compile(r"([\d,]+(?:\.\d+)?)\s*(" + "|".join(sorted(ALIAS, key=len, reverse=True)) + r")(?![a-z])")


def parse(s):
    """'2 kg 30 g' -> ('M', 2030). Returns None if the string is not a plain measurement."""
    s = re.sub(r"^about ", "", s.strip())
    pos, fam, tot = 0, None, Fr(0)
    for mt in TOK.finditer(s):
        if s[pos:mt.start()].strip():
            return None
        u = ALIAS[mt.group(2)]
        fu, sz = UNIT[u][0], UNIT[u][1]
        if fam and fu != fam:
            return None
        fam = fu
        tot += Fr(mt.group(1).replace(",", "")) * sz
        pos = mt.end()
    if fam is None or s[pos:].strip():
        return None
    return fam, tot


def truth(st):
    """'3 km > 2,900 m' -> True/False (chains like a < b < c allowed)."""
    parts = re.split(r" (<|>|=) ", st)
    vals = [parse(p) for p in parts[0::2]]
    assert all(vals) and len({v[0] for v in vals}) == 1, st
    ok = True
    for i, op in enumerate(parts[1::2]):
        a, b = vals[i][1], vals[i + 1][1]
        ok = ok and {"<": a < b, ">": a > b, "=": a == b}[op]
    return ok


def fmt(x):
    """Fraction/int -> '4,536' or '2.5'."""
    x = Fr(x)
    if x.denominator == 1:
        return "{:,}".format(x.numerator)
    s = "%.3f" % float(x)
    s = s.rstrip("0").rstrip(".")
    a, _, b = s.partition(".")
    return "{:,}".format(int(a)) + "." + b


def m(n, u):
    """'4,000 m', '3 hours', '1 minute'."""
    if u in TIME:
        return "%s %s" % (fmt(n), UNIT[u][2] if Fr(n) == 1 else UNIT[u][3])
    return "%s %s" % (fmt(n), u)


def mix(a, ua, b, ub):
    """'2 kg 30 g', '1 hour 45 minutes'."""
    return m(a, ua) + " " + m(b, ub)


def word(u, n=2):
    return UNIT[u][2] if n == 1 else UNIT[u][3]


# ------------------------------------------------------------ helpers
def mcq(q, correct, cands, e, rnd, want=None):
    """4 choices: correct + 3 unique distractors. If the choices are measurements, their values must differ.
    want = (family, value in base unit) checks the correct answer."""
    correct = str(correct)
    if want is not None:
        assert parse(correct) == (want[0], Fr(want[1])), (q, correct, want, parse(correct))
    seen = {correct}
    vals = set()
    pc = parse(correct)
    if pc:
        vals.add(pc[1])
    pick = []
    for c in cands:
        c = str(c)
        lead = c.split(" ")[0].lstrip("£")
        if c in seen or not c or lead.startswith("-") or lead in ("0", "0p"):
            continue
        pv = parse(c)
        if pc and pv and pv[0] == pc[0]:
            if pv[1] in vals:
                continue
            vals.add(pv[1])
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


def marks(k):
    return "%d mark%s" % (k, "" if k == 1 else "s")


# ------------------------------------------------------------ conversion facts
FACT = {  # (big, small): how many small in 1 big
    ("cm", "mm"): 10, ("m", "cm"): 100, ("km", "m"): 1000, ("kg", "g"): 1000, ("l", "ml"): 1000,
    ("minute", "second"): 60, ("hour", "minute"): 60, ("day", "hour"): 24, ("week", "day"): 7,
    ("year", "month"): 12,
}


def fact(b, s):
    return "%s = %s" % (m(1, b), m(FACT[(b, s)], s))


def conv_e(n, uf, ut):
    """Explanation for n uf -> ut (one step)."""
    if (uf, ut) in FACT:
        k = FACT[(uf, ut)]
        return ("%s. %s are bigger than %s, so you need more %s: multiply. %s × %s = %s, so %s = %s."
                % (fact(uf, ut), cap(word(uf)), word(ut), word(ut), fmt(n), fmt(k), fmt(n * k), m(n, uf), m(n * k, ut)))
    k = FACT[(ut, uf)]
    r = Fr(n) / k
    return ("%s. %s are bigger than %s, so you need fewer %s: divide. %s ÷ %s = %s, so %s = %s."
            % (fact(ut, uf), cap(word(ut)), word(uf), word(ut), fmt(n), fmt(k), fmt(r), m(n, uf), m(r, ut)))


def conv(n, uf, ut, wrong, rnd, q=None, e=None):
    """Convert n uf into ut. wrong = numbers in ut from real mistakes."""
    fam = UNIT[uf][0]
    r = Fr(n) * UNIT[uf][1] / UNIT[ut][1]
    if q is None:
        q = "Convert. <b>%s = ☐ %s</b>" % (m(n, uf), ut if ut not in TIME else word(ut))
    return mcq(q, m(r, ut), [m(w, ut) for w in wrong], e or conv_e(n, uf, ut), rnd,
               want=(fam, Fr(n) * UNIT[uf][1]))


# ------------------------------------------------------------ figures
def ruler_svg(s_mm, e_mm, ncm=9):
    """Ruler from 0 to ncm cm with mm marks and a pencil from s_mm to e_mm (exact)."""
    PX = 38.0
    X0, YR, RH = 18, 40, 50
    W = int(X0 * 2 + PX * ncm + 26)
    H = YR + RH + 4
    X = lambda mm: X0 + PX * mm / 10.0
    o = []
    # pencil
    a, b = X(s_mm), X(e_mm)
    tip = min(22, (b - a) * 0.3)
    o.append("<rect x='%.1f' y='12' width='%.1f' height='20' fill='#f4c542' stroke='%s' stroke-width='1.5'/>"
             % (a, b - a - tip, INK))
    o.append("<rect x='%.1f' y='12' width='8' height='20' fill='#e98aa0' stroke='%s' stroke-width='1.5'/>" % (a, INK))
    o.append("<path d='M%.1f 12 L%.1f 22 L%.1f 32 Z' fill='%s' stroke='%s' stroke-width='1.5' stroke-linejoin='round'/>"
             % (b - tip, b, b - tip, WOOD, INK))
    o.append("<path d='M%.1f 19.5 L%.1f 22 L%.1f 24.5 Z' fill='%s'/>" % (b - tip * 0.25, b, b - tip * 0.25, INK))
    # dashed guides to the ruler
    for x in (a, b):
        o.append("<line x1='%.1f' y1='32' x2='%.1f' y2='%d' stroke='%s' stroke-width='1.2' stroke-dasharray='3 2'/>"
                 % (x, x, YR, RED))
    # ruler
    o.append("<rect x='4' y='%d' width='%d' height='%d' rx='3' fill='%s' stroke='%s' stroke-width='2'/>"
             % (YR, W - 8, RH, WOOD, INK))
    small, big = [], []
    for i in range(ncm * 10 + 1):
        x = X(i)
        ln = 18 if i % 10 == 0 else (12 if i % 5 == 0 else 7)
        (big if i % 10 == 0 else small).append("M%.1f %dL%.1f %d" % (x, YR, x, YR + ln))
    o.append("<path d='%s' stroke='%s' stroke-width='1'/>" % ("".join(small), INK))
    o.append("<path d='%s' stroke='%s' stroke-width='2'/>" % ("".join(big), INK))
    for c in range(ncm + 1):
        o.append(text(X(c * 10), YR + 38, str(c), 15))
    o.append(text(X(ncm * 10) + 12, YR + 38, "cm", 15, anchor="start", bold=False))
    return svg_wrap(W, H, "".join(o), "ruler with a pencil from %d mm to %d mm" % (s_mm, e_mm))


def dial_svg(v, mx, lab, tick, unit, div=1, size=200):
    """Round scale, values in grams. Labels every `lab` g shown as val/div. Needle exactly at v."""
    c = size / 2.0
    R = c - 6
    def pt(val, r):
        a = math.radians(-135 + 270.0 * val / mx)
        return c + r * math.sin(a), c - r * math.cos(a)
    s = ["<circle cx='%.1f' cy='%.1f' r='%.1f' fill='#fff' stroke='%s' stroke-width='6'/>" % (c, c, R, GREEN)]
    small, big = [], []
    for i in range(mx // tick + 1):
        val = i * tick
        major = val % lab == 0
        x1, y1 = pt(val, R - (17 if major else 10))
        x2, y2 = pt(val, R - 4)
        (big if major else small).append("M%.1f %.1fL%.1f %.1f" % (x1, y1, x2, y2))
    s.append("<path d='%s' stroke='%s' stroke-width='1.6'/>" % ("".join(small), INK))
    s.append("<path d='%s' stroke='%s' stroke-width='3'/>" % ("".join(big), INK))
    nx, ny = pt(v, R - 9)
    s.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='3.5' stroke-linecap='round'/>"
             % (c, c, nx, ny, RED))
    s.append("<g font-size='%d' font-weight='700' fill='%s' text-anchor='middle' stroke='#fff' stroke-width='4' "
             "paint-order='stroke'>" % (15 if mx // div >= 1000 else 17, INK))
    for val in range(0, mx + 1, lab):
        x, y = pt(val, R - 36)
        s.append("<text x='%.1f' y='%.1f'>%s</text>" % (x, y + 6, fmt(Fr(val, div))))
    s.append("</g>")
    s.append("<circle cx='%.1f' cy='%.1f' r='7' fill='%s'/>" % (c, c, RED))
    s.append("<text x='%.1f' y='%.1f' font-size='22' font-weight='800' fill='%s' text-anchor='middle'>%s</text>"
             % (c, c + 62, GREEN, unit))
    return svg_wrap(size, size, "".join(s), "weighing scale with the needle at %s g" % fmt(v))


def jug_svg(v, mx, lab, step, size=200):
    """Measuring jug in ml: a line every `step` ml, a label every `lab` ml. Water exactly at v."""
    x0, x1 = 92, 168
    yb, yt = 186, 34
    def Y(val):
        return yb - (yb - yt) * float(val) / mx
    s = []
    s.append("<path d='M%d %d C%d %d %d %d %d %d' fill='none' stroke='%s' stroke-width='6'/>"
             % (x1, 50, x1 + 28, 50, x1 + 28, 124, x1, 124, INK))
    s.append("<rect x='%d' y='%.1f' width='%d' height='%.1f' fill='%s'/>" % (x0, Y(v), x1 - x0, yb - Y(v), WATER))
    s.append("<line x1='%d' y1='%.1f' x2='%d' y2='%.1f' stroke='%s' stroke-width='2.5'/>" % (x0, Y(v), x1, Y(v), WATER_LINE))
    s.append("<path d='M%d %d L%d %d L%d %d Q%d %d %d %d L%d %d Q%d %d %d %d L%d %d' fill='none' stroke='%s' "
             "stroke-width='4' stroke-linejoin='round'/>"
             % (x0 - 8, 14, x0, 22, x0, yb - 4, x0, yb, x0 + 6, yb, x1 - 6, yb, x1, yb, x1, yb - 4, x1, 16, INK))
    s.append("<g font-size='15' font-weight='700' fill='%s' text-anchor='end'>" % INK)
    for val in range(step, mx + 1, step):
        major = val % lab == 0
        s.append("<line x1='%d' y1='%.1f' x2='%d' y2='%.1f' stroke='%s' stroke-width='%s'/>"
                 % (x0, Y(val), x0 + (22 if major else 12), Y(val), INK, "2.6" if major else "1.6"))
        if major:
            s.append("<text x='%d' y='%.1f'>%s</text>" % (x0 - 7, Y(val) + 5, fmt(val)))
    s.append("</g>")
    s.append(text(x0 - 7, 198, "ml", 15, anchor="end", col=GREEN))
    return svg_wrap(size, size + 6, "".join(s), "measuring jug with water at %s ml" % fmt(v))


def ladder_svg(units, factors, label):
    """Boxes big -> small with × above and ÷ below the arrows."""
    BW, GAP, BH = 64, 86, 44
    W = 8 + len(units) * BW + (len(units) - 1) * GAP + 8
    H = 120
    o = []
    for i, u in enumerate(units):
        x = 8 + i * (BW + GAP)
        o.append("<rect x='%d' y='38' width='%d' height='%d' rx='8' fill='%s' stroke='%s' stroke-width='2.5'/>"
                 % (x, BW, BH, FILL, GREEN))
        o.append(text(x + BW / 2, 38 + BH / 2 + 7, u, 20))
        if i < len(units) - 1:
            a, b = x + BW + 6, x + BW + GAP - 6
            o.append("<path d='M%d 48 L%d 48 M%d 42 L%d 48 L%d 54' fill='none' stroke='%s' stroke-width='2.5'/>"
                     % (a, b, b - 7, b, b - 7, GREEN))
            o.append(text((a + b) / 2, 34, "× " + factors[i], 16, col=GREEN))
            o.append("<path d='M%d 72 L%d 72 M%d 66 L%d 72 L%d 78' fill='none' stroke='%s' stroke-width='2.5'/>"
                     % (b, a, a + 7, a, a + 7, RED))
            o.append(text((a + b) / 2, 100, "÷ " + factors[i], 16, col=RED))
    return svg_wrap(W, H, "".join(o), label)


# ------------------------------------------------------------ set 1: length
def set_length(rnd):
    its = []
    L = lambda v: ("L", v)
    its.append(mcq("How many millimetres are in 1 centimetre?", "10 mm", ["100 mm", "1,000 mm", "1 mm"],
                   "Look at a ruler: there are 10 small marks in each centimetre. 1 cm = 10 mm.", rnd, want=L(10)))
    its.append(mcq("How many centimetres are in 1 metre?", "100 cm", ["10 cm", "1,000 cm", "60 cm"],
                   "Centi means one hundredth, so 1 m = 100 cm. A metre stick has 100 cm marked on it.", rnd, want=L(1000)))
    its.append(mcq("How many metres are in 1 kilometre?", "1,000 m", ["100 m", "10 m", "10,000 m"],
                   "Kilo means 1,000, so 1 km = 1,000 m (not 100 m).", rnd, want=L(1000000)))
    its.append(mcq("About how thick is a £1 coin?", "about 3 mm", ["about 3 cm", "about 3 m", "about 30 cm"],
                   "A £1 coin is very thin, about 3 millimetres. 3 cm is even more than the width of the whole coin.", rnd))
    its.append(mcq("About how tall is a classroom door?", "about 2 m", ["about 2 cm", "about 2 km", "about 20 m"],
                   "A door is a little taller than a grown-up, about 2 metres. 2 cm is shorter than your finger.", rnd))
    its.append(mcq("Pupils walk for about 15 minutes. About how far do they go?", "about 1 km",
                   ["about 1 m", "about 1 cm", "about 100 km"],
                   "In 15 minutes you can walk about 1 kilometre (1,000 m). 1 m is just one big step.", rnd))
    # single-unit conversions
    its.append(conv(6, "cm", "mm", [600, 6000, 16], rnd))
    its.append(conv(7, "m", "cm", [70, 7000, 107], rnd))
    its.append(conv(4, "km", "m", [400, 40, 1004], rnd))
    its.append(conv(90, "mm", "cm", [900, 90, Fr(9, 10)], rnd))
    its.append(conv(800, "cm", "m", [80, 80000, Fr(8, 10)], rnd))
    its.append(conv(9000, "m", "km", [90, 900, 9000], rnd))
    its.append(conv(12, "km", "m", [1200, 120, 1012], rnd))
    # rulers
    for s_mm, e_mm, form in [(0, 64, "mm"), (0, 57, "cm mm"), (10, 83, "mm")]:
        ln = e_mm - s_mm
        q = fig(ruler_svg(s_mm, e_mm))
        if form == "mm":
            q += "How long is the pencil in millimetres?"
            right = m(ln, "mm")
            if s_mm:
                wrong = [m(e_mm, "mm"), m(ln - 10, "mm"), m(ln * 10, "mm")]
                e = ("The pencil starts at 1 cm, not at 0. It ends at %d cm %d mm = %d mm. "
                     "Take away the start: %d − 10 = %d mm." % (e_mm // 10, e_mm % 10, e_mm, e_mm, ln))
            else:
                wrong = [m(ln * 10, "mm"), m(int("%d0%d" % (ln // 10, ln % 10)), "mm"), m(ln - ln % 10, "mm")]
                e = ("The pencil ends %d small marks after %d cm, so it is %d cm %d mm long. "
                     "1 cm = 10 mm, so %d × 10 = %d, and %d + %d = %d mm."
                     % (ln % 10, ln // 10, ln // 10, ln % 10, ln // 10, ln - ln % 10, ln - ln % 10, ln % 10, ln))
        else:
            q += "How long is the pencil?"
            right = mix(ln // 10, "cm", ln % 10, "mm")
            wrong = [m(ln, "cm"), mix(ln % 10, "cm", ln // 10, "mm"), mix(ln // 10 + 1, "cm", ln % 10, "mm")]
            e = ("The pencil reaches %d whole centimetres and then %d small marks. Each small mark is 1 mm, "
                 "so it is %d cm %d mm long (%d mm)." % (ln // 10, ln % 10, ln // 10, ln % 10, ln))
        its.append(mcq(q, right, wrong, e, rnd, want=L(ln)))
    # mixed units
    its.append(mcq("Convert. <b>3 m 5 cm = ☐ cm</b>", "305 cm", ["35 cm", "350 cm", "3,005 cm"],
                   "3 m = 300 cm. Add the 5 cm: 300 + 5 = 305 cm. Writing 35 cm forgets that 3 m is 300 cm.",
                   rnd, want=L(3050)))
    its.append(mcq("Convert. <b>2 km 30 m = ☐ m</b>", "2,030 m", ["230 m", "2,300 m", "32 m"],
                   "2 km = 2,000 m. Add the 30 m: 2,000 + 30 = 2,030 m. The 3 goes in the tens place, not the hundreds.",
                   rnd, want=L(2030000)))
    its.append(mcq("Which is the same as <b>450 cm</b>?", "4 m 50 cm", ["45 m", "4 m 5 cm", "40 m 50 cm"],
                   "100 cm = 1 m, so 400 cm = 4 m. 450 cm = 4 m and 50 cm left over.", rnd, want=L(4500)))
    its.append(mcq("Which is the same as <b>5,600 m</b>?", "5 km 600 m", ["56 km", "5 km 60 m", "560 km"],
                   "1,000 m = 1 km, so 5,000 m = 5 km. 5,600 m = 5 km and 600 m left over.", rnd, want=L(5600000)))
    assert len(its) == 20, len(its)
    return {"title": "Length: mm, cm, m and km", "items": its}


# ------------------------------------------------------------ set 2: mass and capacity
def dial_e(v, lab, tick, unit, div):
    sp = lab // tick
    base = v - v % lab
    k = (v - base) // tick
    if div == 1:
        s = ("The numbers go up by %s g. There are %d spaces between numbers, so each mark is %s ÷ %d = %s g. "
             % (fmt(lab), sp, fmt(lab), sp, fmt(tick)))
        return s + "The needle is %s past %s g: %s + %s = %s g." % (marks(k), fmt(base), fmt(base), fmt(k * tick), fmt(v))
    s = ("Each kilogram is split into %d equal spaces, so each mark is 1,000 ÷ %d = %s g. " % (sp, sp, fmt(tick)))
    return s + ("The needle is %s past %s kg: %s + %s = %s g, which is %s."
                % (marks(k), fmt(base // 1000), fmt(base), fmt(k * tick), fmt(v), mix(v // 1000, "kg", v % 1000, "g")))


def jug_e(v, lab, step):
    sp = lab // step
    base = v - v % lab
    k = (v - base) // step
    s = ("The numbers go up by %s ml. There are %d spaces between numbers, so each line is %s ÷ %d = %s ml. "
         % (fmt(lab), sp, fmt(lab), sp, fmt(step)))
    return s + "The water is %d line%s above %s ml: %s + %s = %s ml." % (
        k, "" if k == 1 else "s", fmt(base), fmt(base), fmt(k * step), fmt(v))


def set_mass_cap(rnd):
    its = []
    its.append(mcq("How many grams are in 1 kilogram?", "1,000 g", ["100 g", "10 g", "10,000 g"],
                   "Kilo means 1,000, so 1 kg = 1,000 g.", rnd, want=("M", 1000)))
    its.append(mcq("How many millilitres are in 1 litre?", "1,000 ml", ["100 ml", "10 ml", "10,000 ml"],
                   "Milli means one thousandth, so 1 l = 1,000 ml.", rnd, want=("C", 1000)))
    its.append(mcq("About what is the mass of a bag of sugar?", "about 1 kg", ["about 1 g", "about 100 kg", "about 10 g"],
                   "A bag of sugar is about 1 kilogram (1,000 g). 1 g is about the mass of a paper clip.", rnd))
    its.append(mcq("About how much does a teaspoon hold?", "about 5 ml", ["about 5 l", "about 50 l", "about 500 ml"],
                   "A teaspoon holds about 5 millilitres. 500 ml is about a big bottle of water.", rnd))
    its.append(mcq("About how much does a can of fizzy drink hold?", "about 330 ml",
                   ["about 330 l", "about 33 ml", "about 3 l"],
                   "A can of drink holds about 330 millilitres, which is about one third of a litre.", rnd))
    its.append(conv(5, "kg", "g", [500, 50, 1005], rnd))
    its.append(conv(6, "l", "ml", [600, 60, 1006], rnd))
    its.append(conv(3000, "g", "kg", [30, 300, 3000], rnd))
    its.append(conv(7000, "ml", "l", [70, 700, 7000], rnd))
    its.append(mcq("Convert. <b>2 kg 300 g = ☐ g</b>", "2,300 g", ["230 g", "2,030 g", "302 g"],
                   "2 kg = 2,000 g. Add the 300 g: 2,000 + 300 = 2,300 g.", rnd, want=("M", 2300)))
    its.append(mcq("Convert. <b>2 kg 30 g = ☐ g</b>", "2,030 g", ["230 g", "2,300 g", "32 g"],
                   "2 kg = 2,000 g. Add the 30 g: 2,000 + 30 = 2,030 g. Writing 230 g forgets that 2 kg is 2,000 g.",
                   rnd, want=("M", 2030)))
    its.append(mcq("Convert. <b>1 l 750 ml = ☐ ml</b>", "1,750 ml", ["175 ml", "850 ml", "1,075 ml"],
                   "1 l = 1,000 ml. Add the 750 ml: 1,000 + 750 = 1,750 ml. 850 ml would mean 1 l = 100 ml, which is wrong.",
                   rnd, want=("C", 1750)))
    its.append(mcq("Which is the same as <b>3,450 g</b>?", "3 kg 450 g", ["34 kg 50 g", "3 kg 45 g", "345 kg"],
                   "1,000 g = 1 kg, so 3,000 g = 3 kg. 3,450 g = 3 kg and 450 g left over.", rnd, want=("M", 3450)))
    its.append(mcq("Which is the same as <b>4,080 ml</b>?", "4 l 80 ml", ["4 l 800 ml", "40 l 80 ml", "408 l"],
                   "4,000 ml = 4 l. 4,080 ml = 4 l and 80 ml left over (not 800 ml: the 8 is in the tens place).",
                   rnd, want=("C", 4080)))
    # scales
    for v, mx, lab, tick, div, ask in [(650, 1000, 200, 50, 1, "g"), (2400, 5000, 1000, 200, 1000, "g"),
                                       (1700, 3000, 1000, 100, 1000, "kgg")]:
        base = v - v % lab
        k = (v - base) // tick
        unit = "g" if div == 1 else "kg"
        q = fig(dial_svg(v, mx, lab, tick, unit, div))
        if ask == "g" and div == 1:
            q += "The scale shows the mass of a bag of apples. What is the mass?"
            right = m(v, "g")
            wrong = [m(base + k * 10, "g"), m(v + tick, "g"), m(v, "kg"), m(base + k, "g")]
        elif ask == "g":
            q += "The scale shows the mass of a bag of potatoes. What is the mass in grams?"
            right = m(v, "g")
            wrong = [m(base + k * 100, "g"), m(base + k * 10, "g"), m(v // 10, "g")]
        else:
            q += "The scale shows the mass of a parcel. What is the mass?"
            right = mix(v // 1000, "kg", v % 1000, "g")
            wrong = [mix(v // 1000, "kg", (v % 1000) // 10, "g"), m(v // 100, "kg"),
                     mix(v // 1000, "kg", v % 1000 - tick, "g")]
        its.append(mcq(q, right, wrong, dial_e(v, lab, tick, unit, div), rnd, want=("M", v)))
    # jugs
    for v, mx, lab, step, ask in [(700, 1000, 200, 100, "ml"), (400, 1000, 250, 50, "ml"), (1300, 2000, 500, 100, "lml")]:
        base = v - v % lab
        k = (v - base) // step
        q = fig(jug_svg(v, mx, lab, step))
        if ask == "ml":
            q += "How much water is in the jug?"
            right = m(v, "ml")
            wrong = [m(base + k * 50, "ml") if step != 50 else m(base + k * 10, "ml"),
                     m(base + lab, "ml"), m(v, "l"), m(v + step, "ml")]
        else:
            q += "How much water is in the jug? Give your answer in litres and millilitres."
            right = mix(v // 1000, "l", v % 1000, "ml")
            wrong = [mix(v // 1000, "l", (v % 1000) // 10, "ml"), m(v // 100, "l"),
                     mix(v // 1000, "l", base % 1000 + k * 50, "ml")]
        e = jug_e(v, lab, step)
        if ask != "ml":
            e += " 1,000 ml = 1 l, so %s ml = %s." % (fmt(v), right)
        its.append(mcq(q, right, wrong, e, rnd, want=("C", v)))
    assert len(its) == 20, len(its)
    return {"title": "Mass and capacity: g, kg, ml and l", "items": its}


# ------------------------------------------------------------ set 3: time
def set_time(rnd):
    its = []
    T = lambda v: ("T", v)
    its.append(conv(3, "hour", "minute", [300, 63, 30], rnd,
                    e="1 hour = 60 minutes (not 100). Multiply: 3 × 60 = 180, so 3 hours = 180 minutes."))
    its.append(conv(4, "minute", "second", [400, 64, 40], rnd,
                    e="1 minute = 60 seconds. Multiply: 4 × 60 = 240, so 4 minutes = 240 seconds."))
    its.append(conv(9, "minute", "second", [900, 69, 90], rnd,
                    e="1 minute = 60 seconds. Multiply: 9 × 60 = 540, so 9 minutes = 540 seconds."))
    its.append(conv(300, "second", "minute", [3, 30, 18000], rnd,
                    e="1 minute = 60 seconds. Seconds to minutes: divide. 300 ÷ 60 = 5, because 5 × 60 = 300."))
    its.append(mcq("Convert. <b>240 minutes = ☐ hours</b>", "4 hours", ["2 hours 40 minutes", "24 hours", "14,400 hours"],
                   "1 hour = 60 minutes. Minutes to hours: divide. 240 ÷ 60 = 4, because 4 × 60 = 240. "
                   "2 hours 40 minutes would mean 1 hour = 100 minutes.", rnd, want=T(14400)))
    its.append(conv(3, "year", "month", [30, 15, 156], rnd,
                    e="1 year = 12 months. Multiply: 3 × 12 = 36, so 3 years = 36 months."))
    its.append(conv(60, "month", "year", [6, 720, 12], rnd,
                    e="1 year = 12 months. Months to years: divide. 60 ÷ 12 = 5, because 5 × 12 = 60."))
    its.append(conv(5, "week", "day", [50, 12, 30], rnd,
                    e="1 week = 7 days. Multiply: 5 × 7 = 35, so 5 weeks = 35 days."))
    its.append(conv(28, "day", "week", [196, 21, 7], rnd,
                    e="1 week = 7 days. Days to weeks: divide. 28 ÷ 7 = 4, so 28 days = 4 weeks."))
    its.append(conv(2, "day", "hour", [24, 200, 26], rnd,
                    e="1 day = 24 hours. Multiply: 2 × 24 = 48, so 2 days = 48 hours."))
    its.append(mcq("How many days are in 1 year (not a leap year)?", "365 days", ["366 days", "360 days", "52 days"],
                   "A year has 365 days. A leap year has one extra day, 29 February, so it has 366 days. "
                   "52 is the number of weeks in a year.", rnd, want=T(365 * 86400)))
    its.append(mcq("About how many weeks are in 1 year?", "52 weeks", ["12 weeks", "365 weeks", "48 weeks"],
                   "A year has 365 days. 365 ÷ 7 is 52 with 1 day left over, so a year is about 52 weeks. "
                   "12 is the number of months.", rnd, want=T(52 * 604800)))
    for (a, ua, b, ub), wrong, e in [
        ((2, "hour", 15, "minute"), [215, 17, 120],
         "2 hours = 2 × 60 = 120 minutes. Add the 15 minutes: 120 + 15 = 135 minutes."),
        ((1, "hour", 40, "minute"), [140, 41, 160],
         "1 hour = 60 minutes. Add the 40 minutes: 60 + 40 = 100 minutes. 140 would mean 1 hour = 100 minutes."),
        ((3, "minute", 20, "second"), [320, 23, 180],
         "3 minutes = 3 × 60 = 180 seconds. Add the 20 seconds: 180 + 20 = 200 seconds."),
        ((2, "year", 5, "month"), [25, 7, 24],
         "2 years = 2 × 12 = 24 months. Add the 5 months: 24 + 5 = 29 months."),
        ((3, "week", 2, "day"), [32, 5, 21],
         "3 weeks = 3 × 7 = 21 days. Add the 2 days: 21 + 2 = 23 days."),
    ]:
        k = FACT[(ua, ub)]
        tot = a * k + b
        q = "Convert. <b>%s = ☐ %s</b>" % (mix(a, ua, b, ub), word(ub))
        its.append(mcq(q, m(tot, ub), [m(w, ub) for w in wrong], e, rnd, want=(UNIT[ub][0], tot * UNIT[ub][1])))
    its.append(mcq("Which is the same as <b>150 minutes</b>?", "2 hours 30 minutes",
                   ["1 hour 50 minutes", "15 hours", "2 hours 50 minutes"],
                   "120 minutes = 2 hours. 150 − 120 = 30, so 150 minutes = 2 hours 30 minutes. "
                   "1 hour 50 minutes would mean 1 hour = 100 minutes.", rnd, want=T(9000)))
    its.append(mcq("Which is the same as <b>100 seconds</b>?", "1 minute 40 seconds",
                   ["1 minute", "10 minutes", "1 hour 40 minutes"],
                   "1 minute = 60 seconds (not 100). 100 − 60 = 40, so 100 seconds = 1 minute 40 seconds.",
                   rnd, want=T(100)))
    its.append(mcq("Which is the same as <b>30 months</b>?", "2 years 6 months",
                   ["3 years", "3 years 6 months", "2 years 10 months"],
                   "1 year = 12 months, so 2 years = 24 months. 30 − 24 = 6, so 30 months = 2 years 6 months. "
                   "3 years would mean 1 year = 10 months.", rnd, want=("Y", 30)))
    assert len(its) == 20, len(its)
    return {"title": "Time: seconds to years", "items": its}


# ------------------------------------------------------------ set 4: fractions, decimals, comparing
def set_compare(rnd):
    its = []
    its.append(mcq("How many metres are in %s km?" % frac(1, 2), "500 m", ["50 m", "250 m", "2,000 m"],
                   "1 km = 1,000 m. Half of 1,000 is 500, so %s km = 500 m. 50 m would mean 1 km = 100 m." % frac(1, 2),
                   rnd, want=("L", 500000)))
    its.append(mcq("How many grams are in %s kg?" % frac(1, 4), "250 g", ["25 g", "400 g", "4,000 g"],
                   "1 kg = 1,000 g. To find a quarter, divide by 4: 1,000 ÷ 4 = 250 g.", rnd, want=("M", 250)))
    its.append(mcq("How many millilitres are in %s l?" % frac(3, 4), "750 ml", ["75 ml", "250 ml", "300 ml"],
                   "1 l = 1,000 ml. One quarter is 1,000 ÷ 4 = 250 ml, so three quarters is 3 × 250 = 750 ml.",
                   rnd, want=("C", 750)))
    its.append(mcq("Convert. <b>1.5 l = ☐ ml</b>", "1,500 ml", ["150 ml", "1,050 ml", "1,005 ml"],
                   "1 l = 1,000 ml, and 0.5 l is half a litre = 500 ml. 1,000 + 500 = 1,500 ml. (Or 1.5 × 1,000 = 1,500.)",
                   rnd, want=("C", 1500)))
    its.append(mcq("Convert. <b>2.5 km = ☐ m</b>", "2,500 m", ["250 m", "2,050 m", "25,000 m"],
                   "2 km = 2,000 m, and 0.5 km is half a kilometre = 500 m. 2,000 + 500 = 2,500 m.",
                   rnd, want=("L", 2500000)))
    its.append(mcq("Convert. <b>4.2 kg = ☐ g</b>", "4,200 g", ["420 g", "4,020 g", "4,002 g"],
                   "4 kg = 4,000 g. 0.2 kg is 2 tenths of 1,000 g = 200 g. 4,000 + 200 = 4,200 g.",
                   rnd, want=("M", 4200)))
    its.append(mcq("How many minutes are in %s hour?" % frac(1, 2), "30 minutes", ["50 minutes", "15 minutes", "120 minutes"],
                   "1 hour = 60 minutes. Half of 60 is 30. 50 would mean 1 hour = 100 minutes.", rnd, want=("T", 1800)))
    its.append(mcq("How many minutes are in %s hour?" % frac(3, 4), "45 minutes", ["75 minutes", "15 minutes", "30 minutes"],
                   "A quarter of 60 is 60 ÷ 4 = 15, so three quarters is 3 × 15 = 45 minutes.", rnd, want=("T", 2700)))
    # which is the most / least?
    cmp = [
        ("Which is the longest?", ["1,200 m", "1 km 50 m", "1 km 250 m", "1,025 m"], max, "m"),
        ("Which is the heaviest?", ["2 kg", "1,950 g", "2 kg 75 g", "2,070 g"], max, "g"),
        ("Which holds the most?", ["1 l", "900 ml", "1 l 50 ml", "1,100 ml"], max, "ml"),
        ("Which is the shortest?", ["5 cm", "48 mm", "4 cm 5 mm", "52 mm"], min, "mm"),
        ("Which is the longest time?", ["2 hours", "100 minutes", "1 hour 50 minutes", "130 minutes"], max, "minute"),
        ("Which is the shortest time?", ["1 minute", "75 seconds", "1 minute 5 seconds", "58 seconds"], min, "second"),
    ]
    for q, ch, fn, u in cmp:
        vals = [parse(c)[1] / UNIT[u][1] for c in ch]
        assert len(set(vals)) == 4
        i = vals.index(fn(vals))
        order = sorted(range(4), key=lambda j: vals[j], reverse=(fn is max))
        conv_ = ["%s = %s" % (ch[j], m(vals[j], u)) for j in range(4) if ch[j] != m(vals[j], u)]
        e = ("Change them all to %s: %s. In order: %s. So the answer is %s."
             % (word(u), ", ".join(conv_), ", ".join(m(vals[j], u) for j in order), ch[i]))
        its.append(mcq(q, ch[i], [c for j, c in enumerate(ch) if j != i], e, rnd))
    # which is true?
    for sts, e in [
        (["3 km > 2,900 m", "3 km = 300 m", "2 km < 1,950 m", "4 km = 400 m"],
         "1 km = 1,000 m, so 3 km = 3,000 m, and 3,000 > 2,900. 2 km = 2,000 m, which is more than 1,950 m."),
        (["2 hours = 120 minutes", "2 hours = 200 minutes", "3 hours < 150 minutes", "1 hour 30 minutes = 130 minutes"],
         "1 hour = 60 minutes, so 2 hours = 120 minutes. 3 hours = 180 minutes, and 1 hour 30 minutes = 90 minutes."),
        (["5 kg 60 g = 5,060 g", "5 kg 60 g = 560 g", "4 kg > 4,100 g", "6 kg = 600 g"],
         "5 kg = 5,000 g, so 5 kg 60 g = 5,000 + 60 = 5,060 g. 4 kg = 4,000 g, which is less than 4,100 g."),
    ]:
        tv = [truth(s) for s in sts]
        assert tv == [True, False, False, False], sts
        its.append(mcq("Which is true?", sts[0], sts[1:], e, rnd))
    for q, sts, e in [
        ("Which list goes from the lightest to the heaviest?",
         ["1 kg 50 g < 1 kg 400 g < 1,500 g", "1,500 g < 1 kg 400 g < 1 kg 50 g",
          "1 kg 400 g < 1 kg 50 g < 1,500 g", "1 kg 50 g < 1,500 g < 1 kg 400 g"],
         "Change them all to grams: 1 kg 50 g = 1,050 g and 1 kg 400 g = 1,400 g. 1,050 < 1,400 < 1,500."),
        ("Which list goes from the shortest to the longest?",
         ["2 m 5 cm < 2 m 30 cm < 250 cm", "250 cm < 2 m 30 cm < 2 m 5 cm",
          "2 m 30 cm < 2 m 5 cm < 250 cm", "2 m 5 cm < 250 cm < 2 m 30 cm"],
         "Change them all to centimetres: 2 m 5 cm = 205 cm and 2 m 30 cm = 230 cm. 205 < 230 < 250."),
    ]:
        tv = [truth(s) for s in sts]
        assert tv == [True, False, False, False], sts
        its.append(mcq(q, sts[0], sts[1:], e, rnd))
    its.append(mcq("Find the missing number. <b>1 km = 750 m + ☐ m</b>", "250 m", ["25 m", "350 m", "1,750 m"],
                   "1 km = 1,000 m. 1,000 − 750 = 250, so 750 m + 250 m = 1 km. 25 m would mean 1 km = 100 m.",
                   rnd, want=("L", 250000)))
    assert len(its) == 20, len(its)
    return {"title": "Fractions, decimals and comparing", "items": its}


# ------------------------------------------------------------ set 5: word problems
def set_story(rnd):
    P = People(rnd)
    its = []

    def add(q, r, w, e, want=None):
        its.append(mcq(q, r, w, e, rnd, want=want))

    n, he, his = P.next()
    d = 1200 * 2
    add("%s walks 1 km 200 m to school in the morning. %s walks the same way home after school. "
        "How far does %s walk altogether?" % (n, cap(he), he),
        m(d, "m"), ["1,200 m", "600 m", "1,400 m"],
        "1 km 200 m = 1,000 + 200 = 1,200 m. There and back is 2 lots: 1,200 + 1,200 = 2,400 m.", ("L", d * 1000))
    n, he, his = P.next()
    add("%s is baking a cake. The recipe needs 350 g of flour. %s has a 1 kg bag of flour. "
        "How much flour is left after baking?" % (n, cap(he)),
        m(1000 - 350, "g"), ["750 g", "1,350 g", "550 g"],
        "1 kg = 1,000 g. Subtract: 1,000 − 350 = 650 g. Take care when you exchange: the answer is not 750 g.",
        ("M", 650))
    add("A film is 130 minutes long. How long is it in hours and minutes?",
        "2 hours 10 minutes", ["1 hour 30 minutes", "13 hours", "2 hours 30 minutes"],
        "1 hour = 60 minutes, so 2 hours = 120 minutes. 130 − 120 = 10, so it is 2 hours 10 minutes. "
        "1 hour 30 minutes would mean 1 hour = 100 minutes.", ("T", 130 * 60))
    n, he, his = P.next()
    add("%s swims 50 lengths of a 25 m pool in a sponsored swim. How far does %s swim?" % (n, he),
        mix(1, "km", 250, "m"), ["12 km 50 m", "125 m", "1 km 25 m"],
        "50 × 25 = 1,250 m. 1,000 m = 1 km, so 1,250 m = 1 km 250 m.", ("L", 1250000))
    n, he, his = P.next()
    add("%s's sponsor gives 50p for every 100 m %s swims. %s swims 1 km. How much money does the sponsor give?"
        % (n, he, cap(he)),
        "£5.00", ["50p", "£50.00", "£500.00"],
        "1 km = 1,000 m. 1,000 ÷ 100 = 10 lots of 100 m. 10 × 50p = 500p. 100p = £1, so 500p = £5.00. 50p would mean 1 km = 100 m.")
    add("A sponsored walk is 5 km long. It has 4 equal stages. How long is each stage in metres?",
        m(5000 // 4, "m"), ["125 m", "20,000 m", "1,025 m"],
        "5 km = 5,000 m. Share it into 4 equal parts: 5,000 ÷ 4 = 1,250 m.", ("L", 1250000))
    add("A bottle holds 2 litres of squash. Six cups of 250 ml are poured from it. How much squash is left?",
        m(2000 - 6 * 250, "ml"), ["1,500 ml", "1,750 ml", "250 ml"],
        "6 × 250 = 1,500 ml poured. 2 litres = 2,000 ml. 2,000 − 1,500 = 500 ml left.", ("C", 500))
    n, he, his = P.next()
    add("%s is 8 years 7 months old. How old is %s in months?" % (n, he),
        m(8 * 12 + 7, "month"), ["87 months", "96 months", "15 months"],
        "1 year = 12 months, so 8 years = 8 × 12 = 96 months. Add the 7 months: 96 + 7 = 103 months.",
        ("Y", 103))
    add("The summer holiday is 6 weeks long. How many days is that?",
        m(42, "day"), ["36 days", "60 days", "13 days"],
        "1 week = 7 days. 6 × 7 = 42 days.", ("T", 42 * 86400))
    n, he, his = P.next()
    add("In PE, %s holds a plank for 2 minutes 15 seconds. How many seconds is that?" % n,
        m(135, "second"), ["215 seconds", "75 seconds", "120 seconds"],
        "2 minutes = 2 × 60 = 120 seconds. Add 15: 120 + 15 = 135 seconds.", ("T", 135))
    add("In the Multiplication Tables Check there are 25 questions. Pupils get 6 seconds for each one. "
        "How long is that altogether?",
        "2 minutes 30 seconds", ["1 minute 50 seconds", "15 minutes", "2 minutes 50 seconds"],
        "25 × 6 = 150 seconds. 120 seconds = 2 minutes, and 150 − 120 = 30, so it is 2 minutes 30 seconds.",
        ("T", 150))
    add("A football match has two halves of 45 minutes and a 15-minute break at half-time. "
        "How long is that altogether?",
        "1 hour 45 minutes", ["1 hour 5 minutes", "1 hour 30 minutes", "2 hours"],
        "45 + 45 + 15 = 105 minutes. 60 minutes = 1 hour, and 105 − 60 = 45, so it is 1 hour 45 minutes.",
        ("T", 105 * 60))
    add("On a school trip, the coach journey to the zoo takes 2 hours 20 minutes. The journey home takes "
        "155 minutes. How much longer is the journey home?",
        m(155 - 140, "minute"), ["65 minutes", "135 minutes", "25 minutes"],
        "2 hours 20 minutes = 120 + 20 = 140 minutes. 155 − 140 = 15 minutes longer. "
        "65 would mean 1 hour = 100 minutes.", ("T", 15 * 60))
    n, he, his = P.next()
    add("%s's school bag with books in it weighs 3 kg 200 g. The books weigh 1 kg 750 g. "
        "How much does the empty bag weigh?" % n,
        m(3200 - 1750, "g"), ["1,550 g", "4,950 g", "2,450 g"],
        "Change to grams: 3,200 g − 1,750 g = 1,450 g. (1,550 g comes from taking 200 from 750 by mistake.)",
        ("M", 1450))
    add("How many 250 g bags of sweets weigh the same as 2 kg?",
        "8 bags", ["80 bags", "4 bags", "500 bags"],
        "2 kg = 2,000 g. 4 bags of 250 g make 1,000 g, so 2,000 g is 8 bags. Check: 8 × 250 = 2,000.")
    n, he, his = P.next()
    n2, he2, his2 = P.next()
    add("%s cycles 2.5 km. %s cycles 2,300 m. Who cycles further, and by how much?" % (n, n2),
        "%s, by 200 m" % n, ["%s, by 250 m" % n2, "%s, by 2,050 m" % n2, "%s, by 20 m" % n],
        "2.5 km = 2,500 m. 2,500 > 2,300, so %s cycles further. 2,500 − 2,300 = 200 m." % n)
    n, he, his = P.next()
    add("%s has 3 m of ribbon. %s cuts it into pieces 25 cm long. How many pieces does %s get?" % (n, cap(he), he),
        "12 pieces", ["120 pieces", "75 pieces", "4 pieces"],
        "3 m = 300 cm. 300 ÷ 25 = 12, because 4 pieces make 1 m and 3 × 4 = 12.")
    add("A running track is 400 m long. How many laps make 2 km?",
        "5 laps", ["50 laps", "20 laps", "4 laps"],
        "2 km = 2,000 m. 2,000 ÷ 400 = 5 laps. Check: 5 × 400 = 2,000 m.")
    n, he, his = P.next()
    add("%s wants to drink 1.5 litres of water today. So far %s has drunk 4 glasses of 300 ml. "
        "How much more does %s need to drink?" % (n, he, he),
        m(1500 - 1200, "ml"), ["1,200 ml", "2,700 ml", "150 ml"],
        "4 × 300 = 1,200 ml so far. 1.5 litres = 1,500 ml. 1,500 − 1,200 = 300 ml more.", ("C", 300))
    add("A bag of potatoes weighs 2.5 kg. Dad buys 3 bags. How much do they weigh altogether?",
        mix(7, "kg", 500, "g"), ["7 kg 50 g", "75 kg", "6 kg 500 g"],
        "2.5 kg = 2,500 g. 3 × 2,500 = 7,500 g = 7 kg 500 g.", ("M", 7500))
    assert len(its) == 20, len(its)
    return {"title": "Word problems: converting units", "items": its}


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
        "<p>A kilometre is much longer than a metre, so you need <b>more</b> metres to make the same distance. "
        "To change a bigger unit into a smaller unit, <b>multiply</b>. "
        "To change a smaller unit into a bigger unit, <b>divide</b>.</p>"
        "<figure class='sn-fig'>" + ladder_svg(["km", "m", "cm", "mm"], ["1,000", "100", "10"],
                                                "length units: km to m to cm to mm") +
        "<figcaption>Going to a smaller unit: multiply. Going to a bigger unit: divide.</figcaption></figure>" +
        ex("Kilometres to metres", "3 km = ☐ m", "1 km = 1,000 m. Multiply: 3 × 1,000 = 3,000.", "3,000 m") +
        ex("Millilitres to litres", "6,000 ml = ☐ l", "1 l = 1,000 ml. Divide: 6,000 ÷ 1,000 = 6.", "6 l") +
        "<h2>Facts to know</h2>" +
        table(["Measure", "Facts"], [
            ["Length", "1 cm = 10 mm &nbsp; 1 m = 100 cm &nbsp; 1 km = 1,000 m"],
            ["Mass", "1 kg = 1,000 g"],
            ["Capacity", "1 l = 1,000 ml"],
            ["Time", "1 minute = 60 seconds &nbsp; 1 hour = 60 minutes &nbsp; 1 day = 24 hours"],
            ["Longer times", "1 week = 7 days &nbsp; 1 year = 12 months &nbsp; 1 year = 365 days (366 in a leap year)"],
        ]) +
        "<h2>Two units together</h2>"
        "<p>Change the bigger unit first, then add what is left over. Watch the place value.</p>" +
        ex("Kilograms and grams", "2 kg 30 g = ☐ g", "2 kg = 2,000 g. Add 30: 2,000 + 30 = 2,030.", "2,030 g") +
        ex("Hours and minutes", "150 minutes = ☐ hours ☐ minutes",
           "2 hours = 120 minutes. 150 − 120 = 30 minutes left over.", "2 hours 30 minutes") +
        "<h2>Read the scale, then convert</h2>"
        "<figure class='sn-fig'>" + jug_svg(1300, 2000, 500, 100) +
        "<figcaption>Each line is 100 ml. The water is 3 lines above 1,000 ml: 1,300 ml = 1 l 300 ml.</figcaption></figure>"
        "<h2>Halves and decimals</h2>"
        "<p>%s km = 500 m, %s kg = 250 g and 1.5 l = 1,500 ml. To compare, change both to the same unit: "
        "1,200 m is longer than 1 km 50 m, because 1 km 50 m = 1,050 m.</p>" % (frac(1, 2), frac(1, 4)) +
        "<h2>Common mistakes</h2>" +
        table(["Mistake", "What to do instead"], [
            ["1 hour = 100 minutes", "1 hour = 60 minutes and 1 minute = 60 seconds"],
            ["1 km = 100 m, or 1 m = 1,000 cm", "1 km = 1,000 m and 1 m = 100 cm"],
            ["2 kg 30 g = 230 g", "2 kg = 2,000 g, so 2 kg 30 g = 2,030 g"],
            ["Multiplying to get a bigger unit (8,000 m = 8,000,000 km)", "Smaller unit to bigger unit: divide (8,000 m = 8 km)"],
            ["Comparing only the numbers (1,200 m &lt; 1 km 50 m)", "Use one unit first: 1 km 50 m = 1,050 m, and 1,200 &gt; 1,050"],
        ])
    )


FAQ = [
    {"q": "What units do Year 4 children need to convert?",
     "a": "The National Curriculum asks Year 4 pupils to convert between units such as kilometres and metres, metres and "
          "centimetres, kilograms and grams, litres and millilitres, and hours and minutes, minutes and seconds, "
          "years and months, and weeks and days."},
    {"q": "How do you convert kilometres to metres?",
     "a": "Multiply by 1,000, because 1 km = 1,000 m. For example, 3 km = 3 × 1,000 = 3,000 m. "
          "To go back from metres to kilometres, divide by 1,000."},
    {"q": "Why is 1 hour not 100 minutes?",
     "a": "Time does not use tens like metric units: 1 hour = 60 minutes and 1 minute = 60 seconds. "
          "So 150 minutes is 2 hours 30 minutes, not 1 hour 50 minutes."},
    {"q": "What is an easy way to remember metric conversions?",
     "a": "Kilo means 1,000 (1 km = 1,000 m, 1 kg = 1,000 g), centi means a hundredth (1 m = 100 cm) and milli means a "
          "thousandth (1 l = 1,000 ml, 1 m = 1,000 mm). A ruler shows that 1 cm = 10 mm."},
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


def gen_unit():
    rnd = random.Random(4411)
    sets = [set_length(rnd), set_mass_cap(rnd), set_time(rnd), set_compare(rnd), set_story(rnd)]
    balance(sets, rnd)
    seen = set()
    for s in sets:
        assert len(s["items"]) == 20, (s["title"], len(s["items"]))
        pos = [0, 0, 0, 0]
        for it in s["items"]:
            assert len(set(it["c"])) == 4, it
            pos[it["a"]] += 1
            k = it["q"] + "|" + "|".join(sorted(it["c"]))
            assert k not in seen, it["q"]
            seen.add(k)
            assert it["q"].count("<svg") <= 1
        assert pos == [5, 5, 5, 5], (s["title"], pos)
    return {
        "country": "uk", "subject": "maths", "grade": "year-4", "slug": "converting-units", "sort": 11,
        "updated": UPDATED, "pdf_url": "",
        "title": "Converting Units",
        "seo_title": "Year 4 Converting Units Worksheets: Length, Mass, Capacity and Time (Free, with Answers)",
        "short_title": "Converting units",
        "domain": "Measurement",
        "standard_code": "Year 4: Measurement",
        "standard_url": "https://www.gov.uk/government/publications/national-curriculum-in-england-mathematics-programmes-of-study",
        "standard_text": "Convert between different units of measure [for example, kilometre to metre; hour to minute]; solve problems involving converting from hours to minutes; minutes to seconds; years to months; weeks to days.",
        "meta_desc": "Free Year 4 maths worksheets on converting units: mm, cm, m and km, g and kg, ml and l, and seconds, minutes, hours, days, weeks, months and years. Scales, jugs, comparing and word problems. 100 questions with an answer key, matched to the National Curriculum.",
        "key_big": "Bigger unit to smaller unit: multiply. Smaller unit to bigger unit: divide.",
        "key_sub": "1 km = 1,000 m, 1 m = 100 cm, 1 kg = 1,000 g, 1 l = 1,000 ml, but 1 hour = 60 minutes (not 100). So 3 km = 3,000 m and 180 minutes = 3 hours.",
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
    u = gen_unit()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        mark_large(u, "ruler")
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
