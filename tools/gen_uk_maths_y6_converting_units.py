# -*- coding: utf-8 -*-
"""
UK Year 6 Maths: Converting Units (National Curriculum in England, Year 6: Measurement)
  python tools/gen_uk_maths_y6_converting_units.py
HTML attributes use single quotes (no backslashes in the JSON).
British English, metric units, miles and kilometres (5 miles ≈ 8 km), decimals up to 3 places.
Every correct answer is checked in code: each measurement string is parsed back to a base unit.
Miles are stored as exactly 8/5 km (the Year 6 rule), so "about" answers can be checked too.
"""
import json, math, os, random, re
from fractions import Fraction as Fr

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "uk", "maths", "year-6")
UPDATED = "2026-11-02"
GREEN = "#006633"
FILL = "#cfe6d6"
FILL2 = "#eef6f0"
RED = "#c0392b"
INK = "#2b2b2b"
GRID = "#c9ddd0"
WATER = "#9fd3f2"
WATER_LINE = "#2a7fb8"
FONT = "Arial, Helvetica, sans-serif"
GIRLS = ["Amelia", "Isla", "Freya", "Poppy", "Ava", "Aisha", "Lily", "Zara", "Grace", "Ruby", "Maya", "Evie"]
BOYS = ["Oliver", "Harry", "Mohammed", "Jack", "Arjun", "Noah", "George", "Leo", "Alfie", "Kai", "Ethan", "Charlie"]


# ------------------------------------------------------------ units and checking
# unit: (family, size in the base unit, singular word, plural word)
UNIT = {
    "mm": ("L", 1, "millimetre", "millimetres"), "cm": ("L", 10, "centimetre", "centimetres"),
    "m": ("L", 1000, "metre", "metres"), "km": ("L", 1000000, "kilometre", "kilometres"),
    "mile": ("L", 1600000, "mile", "miles"),  # 5 miles ≈ 8 km
    "g": ("M", 1, "gram", "grams"), "kg": ("M", 1000, "kilogram", "kilograms"),
    "ml": ("C", 1, "millilitre", "millilitres"), "l": ("C", 1000, "litre", "litres"),
    "second": ("T", 1, "second", "seconds"), "minute": ("T", 60, "minute", "minutes"),
    "hour": ("T", 3600, "hour", "hours"), "day": ("T", 86400, "day", "days"),
    "week": ("T", 604800, "week", "weeks"),
}
WORDU = {"second", "minute", "hour", "day", "week", "mile"}
ALIAS = {}
for _k, (_fam, _sz, _s, _p) in UNIT.items():
    ALIAS[_k] = _k
    if _k in WORDU:
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
    """Fraction/int -> '4,536' or '2.375' (exact, at most 3 decimal places)."""
    x = Fr(x)
    assert (x * 1000).denominator == 1, x
    if x.denominator == 1:
        return "{:,}".format(x.numerator)
    s = "%.3f" % float(x)
    s = s.rstrip("0").rstrip(".")
    a, _, b = s.partition(".")
    return "{:,}".format(int(a)) + "." + b


def m(n, u):
    """'4,000 m', '3 hours', '1 minute', '40 miles'."""
    if u in WORDU:
        return "%s %s" % (fmt(n), UNIT[u][2] if Fr(n) == 1 else UNIT[u][3])
    return "%s %s" % (fmt(n), u)


def mix(a, ua, b, ub):
    return m(a, ua) + " " + m(b, ub)


def word(u, n=2):
    return UNIT[u][2] if n == 1 else UNIT[u][3]


def D(s):
    return Fr(s)


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


def tw(s, fs):
    return sum(0.33 if ch in ",." else 0.6 for ch in s) * fs


# ------------------------------------------------------------ conversion explanations
def k_between(uf, ut):
    return Fr(UNIT[uf][1], UNIT[ut][1])


def places(k):
    return {10: "1 place", 100: "2 places", 1000: "3 places"}.get(k)


def conv_e(n, uf, ut):
    """Explanation for n uf -> ut (one step, metric or time)."""
    k = k_between(uf, ut)
    r = Fr(n) * k
    if k > 1:
        k = int(k)
        s = "%s. %s are bigger than %s, so multiply by %s: %s × %s = %s." % (
            "%s = %s" % (m(1, uf), m(k, ut)), cap(word(uf)), word(ut), fmt(k), fmt(n), fmt(k), fmt(r))
        if places(k):
            s += " The digits move %s to the left." % places(k)
    else:
        k = int(1 / k)
        s = "%s. %s are smaller than %s, so divide by %s: %s ÷ %s = %s." % (
            "%s = %s" % (m(1, ut), m(k, uf)), cap(word(uf)), word(ut), fmt(k), fmt(n), fmt(k), fmt(r))
        if places(k):
            s += " The digits move %s to the right." % places(k)
    return s + " So %s = %s." % (m(n, uf), m(r, ut))


def conv(n, uf, ut, wrong, rnd, q=None, e=None, extra=""):
    """Convert n uf into ut. wrong = numbers in ut from real mistakes."""
    n = Fr(n)
    fam = UNIT[uf][0]
    r = n * k_between(uf, ut)
    if q is None:
        q = "Convert. <b>%s = ☐ %s</b>" % (m(n, uf), ut if ut not in WORDU else word(ut))
    return mcq(q, m(r, ut), [m(Fr(w), ut) for w in wrong], (e or conv_e(n, uf, ut)) + extra, rnd,
               want=(fam, n * UNIT[uf][1]))


# ------------------------------------------------------------ figures
def ruler_svg(s_mm, e_mm, ncm=9):
    """Ruler from 0 to ncm cm with mm marks and a pencil from s_mm to e_mm (exact)."""
    PX = 38.0
    X0, YR, RH = 18, 40, 50
    W = int(X0 * 2 + PX * ncm + 26)
    H = YR + RH + 4
    X = lambda mm: X0 + PX * mm / 10.0
    o = []
    a, b = X(s_mm), X(e_mm)
    tip = min(22, (b - a) * 0.3)
    o.append("<rect x='%.1f' y='12' width='%.1f' height='20' fill='#f4c542' stroke='%s' stroke-width='1.5'/>"
             % (a, b - a - tip, INK))
    o.append("<rect x='%.1f' y='12' width='8' height='20' fill='#e98aa0' stroke='%s' stroke-width='1.5'/>" % (a, INK))
    o.append("<path d='M%.1f 12 L%.1f 22 L%.1f 32 Z' fill='#f6e7b8' stroke='%s' stroke-width='1.5' stroke-linejoin='round'/>"
             % (b - tip, b, b - tip, INK))
    o.append("<path d='M%.1f 19.5 L%.1f 22 L%.1f 24.5 Z' fill='%s'/>" % (b - tip * 0.25, b, b - tip * 0.25, INK))
    for x in (a, b):
        o.append("<line x1='%.1f' y1='32' x2='%.1f' y2='%d' stroke='%s' stroke-width='1.2' stroke-dasharray='3 2'/>"
                 % (x, x, YR, RED))
    o.append("<rect x='4' y='%d' width='%d' height='%d' rx='3' fill='#f6e7b8' stroke='%s' stroke-width='2'/>"
             % (YR, W - 8, RH, INK))
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


def graph_svg(from_miles=None, from_km=None):
    """Conversion graph: miles 0-50 (x) against km 0-80 (y), straight line through (5, 8).
    Grid every 5 miles and every 8 km, so each reading is exact. Red dashed guide from the given value."""
    L, T, PW, PH = 50, 30, 300, 160
    W, Hh = L + PW + 18, T + PH + 50
    X = lambda mi: L + PW * float(mi) / 50
    Y = lambda km: T + PH - PH * float(km) / 80
    o = []
    o.append("<rect x='%d' y='%d' width='%d' height='%d' fill='#fff'/>" % (L, T, PW, PH))
    g = []
    for i in range(1, 11):
        g.append("M%.1f %dL%.1f %d" % (X(5 * i), T, X(5 * i), T + PH))
        g.append("M%d %.1fL%d %.1f" % (L, Y(8 * i), L + PW, Y(8 * i)))
    o.append("<path d='%s' stroke='%s' stroke-width='1.2'/>" % ("".join(g), GRID))
    o.append("<path d='M%d %dL%d %dL%d %d' fill='none' stroke='%s' stroke-width='2.2'/>"
             % (L, T, L, T + PH, L + PW, T + PH, INK))
    for mi in range(0, 51, 10):
        o.append(text(X(mi), T + PH + 20, str(mi), 14))
    for km in range(0, 81, 16):
        o.append(text(L - 7, Y(km) + 5, str(km), 14, anchor="end"))
    o.append(text(L + PW / 2.0, T + PH + 42, "miles", 15, col=GREEN))
    o.append(text(L - 7, T - 12, "km", 15, anchor="end", col=GREEN))
    o.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='3'/>"
             % (X(0), Y(0), X(50), Y(80), GREEN))
    if from_miles is not None or from_km is not None:
        mi = Fr(from_miles) if from_miles is not None else Fr(from_km) * 5 / 8
        km = mi * 8 / 5
        assert (mi % 5 == 0) and (km % 8 == 0)
        dash = "stroke='%s' stroke-width='2' stroke-dasharray='5 3' fill='none'" % RED
        if from_miles is not None:
            o.append("<path d='M%.1f %.1fL%.1f %.1fL%.1f %.1f' %s/>" % (X(mi), Y(0), X(mi), Y(km), L, Y(km), dash))
        else:
            o.append("<path d='M%.1f %.1fL%.1f %.1fL%.1f %.1f' %s/>" % (L, Y(km), X(mi), Y(km), X(mi), Y(0), dash))
        o.append("<circle cx='%.1f' cy='%.1f' r='4.5' fill='%s'/>" % (X(mi), Y(km), RED))
    lab = "conversion graph for miles and kilometres"
    return svg_wrap(W, Hh, "".join(o), lab)


def dnl_svg(top, bot, miss, labels):
    """Double number line, ticks drawn to scale by the top value. miss = (row, index) of the red ? box."""
    r0 = None
    for i, (a, b) in enumerate(zip(top, bot)):
        if (0, i) == miss or (1, i) == miss or a == 0:
            continue
        rr = Fr(b) / Fr(a)
        assert r0 is None or rr == r0
        r0 = rr
    LW = int(max(tw(l, 16) for l in labels)) + 14
    gap = 64
    unit = min(top[i + 1] - top[i] for i in range(len(top) - 1))
    x0 = LW + 22
    W = int(x0 + (top[-1] - top[0]) / unit * gap + 30)
    Y1, Y2, Ht = 42, 92, 128
    o = [text(LW, Y1 + 6, labels[0], 16, "end", col=GREEN), text(LW, Y2 + 6, labels[1], 16, "end", col=GREEN)]
    for y in (Y1, Y2):
        o.append("<line x1='%.1f' y1='%d' x2='%.1f' y2='%d' stroke='%s' stroke-width='2.2'/>" % (x0 - 8, y, W - 10, y, INK))
        o.append("<path d='M%d %d l-9 -5 v10 z' fill='%s'/>" % (W - 4, y, INK))
    for i, p in enumerate(top):
        x = x0 + float((p - top[0]) / unit) * gap
        for r, (y, v) in enumerate([(Y1, top[i]), (Y2, bot[i])]):
            o.append("<line x1='%.1f' y1='%d' x2='%.1f' y2='%d' stroke='%s' stroke-width='2'/>" % (x, y - 8, x, y + 8, INK))
            ty = y - 14 if r == 0 else y + 28
            if (r, i) == miss:
                o.append("<rect x='%.1f' y='%.1f' width='36' height='24' rx='4' fill='none' stroke='%s' stroke-width='2' "
                         "stroke-dasharray='5 3'/>" % (x - 18, ty - 18, RED))
                o.append(text(x, ty, "?", 17, col=RED))
            else:
                o.append(text(x, ty, fmt(v), 17))
    return svg_wrap(W, Ht, "".join(o), "double number line: %s and %s" % (labels[0], labels[1]))


# ------------------------------------------------------------ set 1: length with decimals
def set_length(rnd):
    its = []
    L = lambda v: ("L", v)
    its.append(conv(45, "mm", "cm", [450, D("0.45"), D("0.045")], rnd))
    its.append(conv(D("3.6"), "m", "cm", [36, 3600, 306], rnd))
    its.append(conv(D("2.4"), "km", "m", [240, 24000, 2004], rnd))
    its.append(conv(850, "m", "km", [D("8.5"), D("0.085"), 850000], rnd))
    its.append(conv(D("0.6"), "cm", "mm", [60, D("0.06"), 600], rnd))
    its.append(conv(D("1.75"), "m", "mm", [175, 17500, D("1.75")], rnd,
                    e="1 m = 1,000 mm. Metres are bigger than millimetres, so multiply by 1,000: "
                      "1.75 × 1,000 = 1,750. The digits move 3 places to the left. So 1.75 m = 1,750 mm.",
                    extra=" (1.75 × 100 = 175 would give centimetres, not millimetres.)"))
    its.append(conv(45, "mm", "m", [D("4.5"), D("0.45"), 45], rnd,
                    e="1 m = 1,000 mm. Millimetres are smaller than metres, so divide by 1,000: 45 ÷ 1,000 = 0.045. "
                      "The digits move 3 places to the right, so you need a 0 in the tenths place. So 45 mm = 0.045 m."))
    its.append(conv(D("3.125"), "km", "m", [D("312.5"), 31250, D("3.125")], rnd))
    its.append(conv(65, "m", "km", [D("0.65"), D("6.5"), 65000], rnd,
                    extra=" Check: 0.65 km would be 650 m."))
    its.append(conv(7, "cm", "m", [D("0.7"), D("0.007"), 700], rnd))
    q = fig(ruler_svg(0, 83)) + "How long is the pencil in metres?"
    its.append(mcq(q, "0.083 m", ["0.83 m", "8.3 m", "83 m"],
                   "The pencil ends 3 small marks after 8 cm, so it is 8 cm 3 mm = 83 mm. "
                   "1 m = 1,000 mm, so divide by 1,000: 83 ÷ 1,000 = 0.083 m.", rnd, want=L(83)))
    its.append(conv(4050, "m", "km", [D("4.5"), D("40.5"), D("4.005")], rnd,
                    extra=" The 0 in 4,050 keeps its place: 4.05, not 4.5."))
    its.append(conv(D("1.08"), "m", "cm", [180, D("10.8"), 1080], rnd))
    its.append(mcq("Convert. <b>2 km 75 m = ☐ km</b>", "2.075 km", ["2.75 km", "20.75 km", "2.705 km"],
                   "75 m = 75 ÷ 1,000 = 0.075 km, because 1 km = 1,000 m. So 2 km 75 m = 2 + 0.075 = 2.075 km. "
                   "2.75 km would be 2 km 750 m.", rnd, want=L(2075000)))
    its.append(mcq("Which is the same as <b>0.305 km</b>?", "305 m", ["3,050 m", "30.5 m", "35 m"],
                   "Multiply by 1,000: 0.305 × 1,000 = 305 m. The 0 holds the tenths place, so it is not 35 m.",
                   rnd, want=L(305000)))
    its.append(mcq("Which is the same as <b>6.04 m</b>?", "6 m 4 cm", ["6 m 40 cm", "6 m 4 mm", "64 cm"],
                   "6.04 m = 6 m and 0.04 m. 0.04 m = 0.04 × 100 = 4 cm. So 6.04 m = 6 m 4 cm. "
                   "6 m 40 cm would be 6.4 m.", rnd, want=L(6040)))
    ch = ["0.5 km", "450 m", "5,200 cm", "0.48 km"]
    vals = [parse(c)[1] / 1000 for c in ch]
    assert vals == [500, 450, 52, 480]
    its.append(mcq("Which is the longest?", "0.5 km", ch[1:],
                   "Change them all to metres: 0.5 km = 500 m, 5,200 cm = 52 m and 0.48 km = 480 m. "
                   "500 m is the longest. 5,200 cm has the biggest number, but centimetres are small.", rnd))
    ch = ["6.5 cm", "0.07 m", "68 mm", "0.6 m"]
    vals = [parse(c)[1] for c in ch]
    assert vals == [65, 70, 68, 600]
    its.append(mcq("Which is the shortest?", "6.5 cm", ch[1:],
                   "Change them all to millimetres: 6.5 cm = 65 mm, 0.07 m = 70 mm and 0.6 m = 600 mm. "
                   "65 mm is the shortest.", rnd))
    sts = ["1.2 km = 1,200 m", "0.3 m = 3 cm", "45 mm = 0.45 m", "2.5 m = 250 mm"]
    assert [truth(s) for s in sts] == [True, False, False, False]
    its.append(mcq("Which is true?", sts[0], sts[1:],
                   "1.2 × 1,000 = 1,200, so 1.2 km = 1,200 m. The others are wrong: 0.3 m = 30 cm, "
                   "45 mm = 0.045 m and 2.5 m = 2,500 mm.", rnd))
    its.append(mcq("Find the missing number. <b>1 km − 375 m = ☐ km</b>", "0.625 km",
                   ["0.725 km", "0.375 km", "625 km"],
                   "1 km = 1,000 m. 1,000 − 375 = 625 m. 625 ÷ 1,000 = 0.625 km. "
                   "Take care when you exchange: 1,000 − 375 is 625, not 725.", rnd, want=L(625000)))
    assert len(its) == 20, len(its)
    return {"title": "Length: mm, cm, m and km with decimals", "items": its}


# ------------------------------------------------------------ set 2: mass and capacity
def set_mass_cap(rnd):
    its = []
    its.append(conv(D("1.25"), "l", "ml", [125, 12500, 1025], rnd,
                    extra=" (125 ml would be 0.125 l.)"))
    its.append(conv(750, "g", "kg", [D("7.5"), D("0.075"), 750000], rnd))
    its.append(conv(D("2.375"), "kg", "g", [D("237.5"), 23750, D("2.375")], rnd))
    its.append(conv(D("0.5"), "l", "ml", [50, 5, 5000], rnd))
    its.append(conv(330, "ml", "l", [D("3.3"), D("0.033"), 330000], rnd))
    its.append(conv(45, "g", "kg", [D("0.45"), D("4.5"), 45000], rnd))
    its.append(conv(D("4.08"), "kg", "g", [4800, 408, 4008], rnd))
    its.append(conv(D("0.2"), "l", "ml", [20, 2, 2000], rnd))
    its.append(conv(2600, "ml", "l", [26, D("0.26"), D("2.06")], rnd))
    its.append(mcq("Convert. <b>3 kg 50 g = ☐ kg</b>", "3.05 kg", ["3.5 kg", "3.005 kg", "30.5 kg"],
                   "50 g = 50 ÷ 1,000 = 0.05 kg. So 3 kg 50 g = 3.05 kg. 3.5 kg would be 3 kg 500 g.",
                   rnd, want=("M", 3050)))
    its.append(mcq("Work out <b>1.5 kg + 700 g</b>. Give your answer in kilograms.", "2.2 kg",
                   ["701.5 kg", "8.5 kg", "1.57 kg"],
                   "Use one unit first: 700 g = 0.7 kg. Then 1.5 + 0.7 = 2.2 kg. "
                   "701.5 kg adds the numbers without converting.", rnd, want=("M", 2200)))
    ch = ["1.2 kg", "1,050 g", "0.95 kg", "1 kg 150 g"]
    assert [parse(c)[1] for c in ch] == [1200, 1050, 950, 1150]
    its.append(mcq("Which is the heaviest?", "1.2 kg", ch[1:],
                   "Change them all to grams: 1.2 kg = 1,200 g, 0.95 kg = 950 g, 1 kg 150 g = 1,150 g. "
                   "1,200 g is the heaviest.", rnd))
    sts = ["0.25 l < 400 ml < 0.5 l", "0.5 l < 400 ml < 0.25 l", "400 ml < 0.25 l < 0.5 l", "0.25 l < 0.5 l < 400 ml"]
    assert [truth(s) for s in sts] == [True, False, False, False]
    its.append(mcq("Which list goes from the smallest to the largest capacity?", sts[0], sts[1:],
                   "Change them all to millilitres: 0.25 l = 250 ml and 0.5 l = 500 ml. 250 &lt; 400 &lt; 500.", rnd))
    sts = ["0.6 kg = 600 g", "0.6 kg = 60 g", "1.05 l = 1,500 ml", "3 kg > 3,100 g"]
    assert [truth(s) for s in sts] == [True, False, False, False]
    its.append(mcq("Which is true?", sts[0], sts[1:],
                   "0.6 × 1,000 = 600, so 0.6 kg = 600 g. The others are wrong: 1.05 l = 1,050 ml, "
                   "and 3 kg = 3,000 g, which is less than 3,100 g.", rnd))
    # scales in kilograms
    q = fig(dial_svg(1400, 3000, 1000, 200, "kg", 1000)) + "The scale shows the mass of a bag of flour. What is the mass in kilograms?"
    its.append(mcq(q, "1.4 kg", ["1.2 kg", "1.04 kg", "14 kg"],
                   "Each kilogram is split into 5 equal spaces, so each mark is 1 ÷ 5 = 0.2 kg (200 g). "
                   "The needle is 2 marks past 1 kg: 1 + 0.4 = 1.4 kg. (1.2 kg counts each mark as 0.1 kg.)",
                   rnd, want=("M", 1400)))
    q = fig(dial_svg(2750, 4000, 1000, 250, "kg", 1000)) + "The scale shows the mass of a parcel. What is the mass in kilograms?"
    its.append(mcq(q, "2.75 kg", ["2.3 kg", "2.075 kg", "27.5 kg"],
                   "Each kilogram is split into 4 equal spaces, so each mark is 1 ÷ 4 = 0.25 kg (250 g). "
                   "The needle is 3 marks past 2 kg: 2 + 0.75 = 2.75 kg. (2.3 kg counts each mark as 0.1 kg.)",
                   rnd, want=("M", 2750)))
    q = fig(dial_svg(600, 1000, 200, 50, "g")) + "The scale shows the mass of some apples. What is the mass in kilograms?"
    its.append(mcq(q, "0.6 kg", ["6 kg", "0.06 kg", "600 kg"],
                   "The needle points to 600 g. 1 kg = 1,000 g, so divide by 1,000: 600 ÷ 1,000 = 0.6 kg.",
                   rnd, want=("M", 600)))
    # jugs
    q = fig(jug_svg(1300, 2000, 500, 100)) + "How much water is in the jug? Give your answer in litres."
    its.append(mcq(q, "1.3 l", ["1.03 l", "13 l", "1.15 l"],
                   "The numbers go up by 500 ml and there are 5 spaces, so each line is 100 ml. "
                   "The water is 3 lines above 1,000 ml: 1,300 ml. 1,300 ÷ 1,000 = 1.3 l.", rnd, want=("C", 1300)))
    q = fig(jug_svg(650, 1000, 250, 50)) + "How much water is in the jug? Give your answer in litres."
    its.append(mcq(q, "0.65 l", ["0.53 l", "6.5 l", "0.065 l"],
                   "The numbers go up by 250 ml and there are 5 spaces, so each line is 50 ml. "
                   "The water is 3 lines above 500 ml: 500 + 150 = 650 ml. 650 ÷ 1,000 = 0.65 l. "
                   "(0.53 l counts each line as 10 ml.)", rnd, want=("C", 650)))
    q = fig(jug_svg(1600, 2000, 500, 100)) + "How much more water is needed to fill the jug to 2 litres?"
    its.append(mcq(q, "400 ml", ["600 ml", "1,600 ml", "40 ml"],
                   "Each line is 100 ml. The water is at 1,600 ml. 2 litres = 2,000 ml. 2,000 − 1,600 = 400 ml more.",
                   rnd, want=("C", 400)))
    assert len(its) == 20, len(its)
    return {"title": "Mass and capacity: g, kg, ml and l", "items": its}


# ------------------------------------------------------------ set 3: time
def set_time(rnd):
    its = []
    T = lambda v: ("T", v)
    its.append(mcq("Which is the same as <b>2.5 hours</b>?", "2 hours 30 minutes",
                   ["2 hours 50 minutes", "2 hours 5 minutes", "25 minutes"],
                   "0.5 hours is half an hour, and half of 60 minutes is 30 minutes. So 2.5 hours = 2 hours 30 minutes. "
                   "2 hours 50 minutes treats an hour as 100 minutes.", rnd, want=T(9000)))
    its.append(conv(D("1.5"), "hour", "minute", [150, 105, 65], rnd,
                    e="1 hour = 60 minutes. Multiply: 1.5 × 60 = 90, so 1.5 hours = 90 minutes (60 + 30)."))
    its.append(conv(D("0.25"), "hour", "minute", [25, D("2.5"), 4], rnd,
                    e="0.25 is one quarter. A quarter of 60 minutes is 60 ÷ 4 = 15 minutes. (0.25 × 60 = 15.)"))
    its.append(conv(D("2.5"), "minute", "second", [250, 205, 120], rnd,
                    e="1 minute = 60 seconds. Multiply: 2.5 × 60 = 150, so 2.5 minutes = 150 seconds (120 + 30)."))
    its.append(conv(1, "hour", "second", [6000, 360, 120], rnd,
                    e="1 hour = 60 minutes and 1 minute = 60 seconds. 60 × 60 = 3,600, so 1 hour = 3,600 seconds."))
    its.append(conv(D("0.2"), "hour", "minute", [20, 2, 120], rnd,
                    e="0.2 is two tenths. One tenth of 60 minutes is 60 ÷ 10 = 6 minutes, so two tenths is 2 × 6 = 12 minutes, not 20."))
    its.append(conv(4, "day", "hour", [40, 28, 48], rnd,
                    e="1 day = 24 hours. Multiply: 4 × 24 = 96, so 4 days = 96 hours."))
    its.append(conv(72, "hour", "day", [D("7.2"), 6, 1728], rnd,
                    e="1 day = 24 hours. Hours to days: divide. 72 ÷ 24 = 3, so 72 hours = 3 days. "
                      "Do not divide by 10 (that gives 7.2)."))
    its.append(conv(14, "week", "day", [140, 21, 2], rnd,
                    e="1 week = 7 days. Multiply: 14 × 7 = 98, so 14 weeks = 98 days."))
    its.append(conv(63, "day", "week", [D("6.3"), 441, 7], rnd,
                    e="1 week = 7 days. Days to weeks: divide. 63 ÷ 7 = 9, so 63 days = 9 weeks."))
    its.append(conv(1, "week", "hour", [140, 31, 120], rnd,
                    e="1 week = 7 days and 1 day = 24 hours. 7 × 24 = 168, so 1 week = 168 hours."))
    its.append(conv(D("1.5"), "day", "hour", [15, 29, 150], rnd,
                    e="1 day = 24 hours, and half a day is 12 hours. 24 + 12 = 36, so 1.5 days = 36 hours."))
    its.append(mcq("Convert. <b>3 hours 20 minutes = ☐ minutes</b>", "200 minutes",
                   ["320 minutes", "23 minutes", "180 minutes"],
                   "3 hours = 3 × 60 = 180 minutes. Add the 20 minutes: 180 + 20 = 200 minutes.", rnd, want=T(12000)))
    its.append(mcq("Which is the same as <b>210 seconds</b>?", "3 minutes 30 seconds",
                   ["2 minutes 10 seconds", "3 minutes 50 seconds", "21 minutes"],
                   "180 seconds = 3 minutes. 210 − 180 = 30, so 210 seconds = 3 minutes 30 seconds. "
                   "(210 ÷ 60 = 3.5, but 0.5 minutes is 30 seconds, not 50.)", rnd, want=T(210)))
    its.append(mcq("Which is the same as <b>3.75 hours</b>?", "3 hours 45 minutes",
                   ["3 hours 75 minutes", "3 hours 7 minutes", "375 minutes"],
                   "0.75 hours is three quarters of an hour: 0.75 × 60 = 45 minutes. "
                   "So 3.75 hours = 3 hours 45 minutes.", rnd, want=T(13500)))
    its.append(mcq("Convert. <b>135 minutes = ☐ hours</b>", "2.25 hours", ["1.35 hours", "2.15 hours", "13.5 hours"],
                   "135 minutes = 120 + 15 minutes = 2 hours 15 minutes. 15 minutes is a quarter of an hour, "
                   "0.25 hours. So 135 minutes = 2.25 hours, not 2.15 hours.", rnd, want=T(8100)))
    its.append(mcq("Which is the same as <b>45 days</b>?", "6 weeks 3 days",
                   ["6.3 weeks", "4 weeks 5 days", "6 weeks 5 days"],
                   "6 × 7 = 42 days. 45 − 42 = 3 days left over, so 45 days = 6 weeks 3 days. "
                   "The remainder is days, so it is not 6.3 weeks.", rnd, want=T(45 * 86400)))
    ch = ["78 minutes", "1.2 hours", "1 hour 15 minutes", "4,200 seconds"]
    assert [parse(c)[1] / 60 for c in ch] == [78, 72, 75, 70]
    its.append(mcq("Which is the longest time?", ch[0], ch[1:],
                   "Change them all to minutes: 1.2 hours = 1.2 × 60 = 72 minutes (not 1 hour 20 minutes), "
                   "1 hour 15 minutes = 75 minutes and 4,200 seconds = 4,200 ÷ 60 = 70 minutes. "
                   "78 minutes is the longest.", rnd))
    sts = ["0.75 hours = 45 minutes", "0.75 hours = 75 minutes", "1.5 hours = 150 minutes",
           "2.4 hours = 2 hours 40 minutes"]
    assert [truth(s) for s in sts] == [True, False, False, False]
    its.append(mcq("Which is true?", sts[0], sts[1:],
                   "0.75 × 60 = 45, so 0.75 hours = 45 minutes. 1.5 hours = 90 minutes, and "
                   "2.4 hours = 2 hours 24 minutes (0.4 × 60 = 24).", rnd))
    its.append(mcq("Find the missing number. <b>2.5 minutes − 45 seconds = ☐ seconds</b>", "105 seconds",
                   ["205 seconds", "195 seconds", "120 seconds"],
                   "2.5 minutes = 2.5 × 60 = 150 seconds. 150 − 45 = 105 seconds. "
                   "205 seconds comes from treating 2.5 minutes as 250 seconds.", rnd, want=T(105)))
    assert len(its) == 20, len(its)
    return {"title": "Time: decimals of hours, minutes and days", "items": its}


# ------------------------------------------------------------ set 4: miles and kilometres
def km_of(mi):
    return Fr(mi) * 8 / 5


def mi_of(km):
    return Fr(km) * 5 / 8


def ab(n, u):
    return "about " + m(n, u)


def set_miles(rnd):
    its = []
    L = lambda v: ("L", v)
    RULE = "5 miles is approximately 8 km. "
    its.append(mcq("Approximately how many kilometres are the same as <b>5 miles</b>?", ab(8, "km"),
                   [ab(5, "km"), ab(3, "km"), ab(13, "km")],
                   "This is the fact to learn: 5 miles is approximately 8 km. A mile is longer than a kilometre.",
                   rnd, want=L(8000000)))
    its.append(mcq("Approximately how many miles are the same as <b>8 km</b>?", ab(5, "mile"),
                   [ab(8, "mile"), ab(13, "mile"), ab(D("12.8"), "mile")],
                   RULE + "So 8 km is about 5 miles. There are fewer miles because a mile is longer.",
                   rnd, want=L(8000000)))
    its.append(mcq("Approximately how many kilometres are the same as <b>10 miles</b>?", ab(16, "km"),
                   [ab(18, "km"), ab(D("6.25"), "km"), ab(10, "km")],
                   RULE + "10 miles is 2 lots of 5 miles, so it is about 2 × 8 = 16 km.", rnd, want=L(16000000)))
    its.append(mcq("Approximately how many kilometres are the same as <b>40 miles</b>?", ab(64, "km"),
                   [ab(25, "km"), ab(48, "km"), ab(45, "km")],
                   RULE + "40 ÷ 5 = 8 lots, so 8 × 8 = 64 km. (25 km comes from going the wrong way.)",
                   rnd, want=L(64000000)))
    its.append(mcq("Approximately how many miles are the same as <b>24 km</b>?", ab(15, "mile"),
                   [ab(D("38.4"), "mile"), ab(21, "mile"), ab(3, "mile")],
                   RULE + "24 ÷ 8 = 3 lots, so 3 × 5 = 15 miles. (3 miles forgets to multiply by 5.)",
                   rnd, want=L(24000000)))
    its.append(mcq("Approximately how many kilometres are the same as <b>25 miles</b>?", ab(40, "km"),
                   [ab(33, "km"), ab(5, "km"), ab(30, "km")],
                   RULE + "25 ÷ 5 = 5 lots, so 5 × 8 = 40 km.", rnd, want=L(40000000)))
    its.append(mcq("Approximately how many miles are the same as <b>100 km</b>?", ab(D("62.5"), "mile"),
                   [ab(160, "mile"), ab(108, "mile"), ab(D("12.5"), "mile")],
                   RULE + "100 ÷ 8 = 12.5 lots, so 12.5 × 5 = 62.5 miles. Kilometres to miles: the number gets smaller.",
                   rnd, want=L(100000000)))
    its.append(mcq("Approximately how many kilometres are the same as <b>120 miles</b>?", ab(192, "km"),
                   [ab(75, "km"), ab(128, "km"), ab(960, "km")],
                   RULE + "120 ÷ 5 = 24 lots, so 24 × 8 = 192 km. (960 km multiplies by 8 but forgets to divide by 5.)",
                   rnd, want=L(192000000)))
    its.append(mcq("Approximately how many kilometres are the same as <b>2.5 miles</b>?", ab(4, "km"),
                   [ab(D("2.5"), "km"), ab(D("5.5"), "km"), ab(20, "km")],
                   RULE + "2.5 miles is half of 5 miles, so it is about half of 8 km = 4 km.", rnd, want=L(4000000)))
    its.append(mcq("Which fact says the same as <b>5 miles ≈ 8 km</b>?", "1 mile ≈ 1.6 km",
                   ["1 km ≈ 1.6 miles", "1 mile ≈ 0.625 km", "1 mile ≈ 3 km"],
                   "Divide both sides by 5: 5 ÷ 5 = 1 mile and 8 ÷ 5 = 1.6 km. A mile is longer than a kilometre, "
                   "so 1 mile is more than 1 km.", rnd))
    its.append(mcq("Approximately how many miles are the same as <b>1.6 km</b>?", ab(1, "mile"),
                   [ab(D("1.6"), "mile"), ab(D("2.56"), "mile"), ab(16, "mile")],
                   "1 mile ≈ 1.6 km (8 ÷ 5 = 1.6). So 1.6 km is about 1 mile.", rnd, want=L(1600000)))
    # conversion graph
    G = "Use the conversion graph. "
    for mi, wrong, e in [
        (30, [60, 30, 50], "Up from 30 miles to the line, then across: 48 km. On the km axis each square is 8 km "
                           "(the labels go up in 16s), so 6 squares is 48 km, not 60 km."),
        (45, [90, 45, 64], "Up from 45 miles (halfway between 40 and 50) to the line, then across: 72 km "
                           "(halfway between 64 and 80). Each square on the km axis is 8 km."),
    ]:
        q = fig(graph_svg(from_miles=mi)) + G + "Approximately how many kilometres are the same as %s?" % m(mi, "mile")
        its.append(mcq(q, ab(km_of(mi), "km"), [ab(w, "km") for w in wrong], e, rnd, want=L(km_of(mi) * 1000000)))
    for km, wrong, e in [
        (56, [70, 56, 30], "Across from 56 km to the line, then down: 35 miles (halfway between 30 and 40). "
                           "Each square on the miles axis is 5 miles, so 7 squares is 35 miles, not 70."),
        (40, [50, 40, 20], "Across from 40 km to the line, then down: 25 miles (halfway between 20 and 30). "
                           "Each square on the miles axis is 5 miles."),
    ]:
        q = fig(graph_svg(from_km=km)) + G + "Approximately how many miles are the same as %s?" % m(km, "km")
        its.append(mcq(q, ab(mi_of(km), "mile"), [ab(w, "mile") for w in wrong], e, rnd, want=L(km * 1000000)))
    q = (fig(dnl_svg([0, 5, 10, 15, 20], [0, 8, 16, 24, 32], (1, 3), ["miles", "km"])) +
         "The double number line uses 5 miles ≈ 8 km. What is the missing number?")
    its.append(mcq(q, ab(24, "km"), [ab(21, "km"), ab(30, "km"), ab(15, "km")],
                   "Each step on the top line is 5 miles, and each step on the bottom line is 8 km. "
                   "16 + 8 = 24, so 15 miles ≈ 24 km. (21 km adds 5 instead of 8.)", rnd, want=L(24000000)))
    sts = ["20 km < 15 miles < 30 km", "15 miles < 20 km < 30 km", "20 km < 30 km < 15 miles", "30 km < 20 km < 15 miles"]
    assert [truth(s) for s in sts] == [True, False, False, False]
    its.append(mcq("Which list goes from the shortest to the longest distance?", sts[0], sts[1:],
                   "Change 15 miles to km: 15 ÷ 5 = 3 lots, 3 × 8 = 24 km. So 20 km &lt; 24 km &lt; 30 km.", rnd))
    its.append(mcq("A road sign says <b>London 80 miles</b>. Approximately how far is that in kilometres?",
                   ab(128, "km"), [ab(50, "km"), ab(88, "km"), ab(640, "km")],
                   RULE + "80 ÷ 5 = 16 lots, so 16 × 8 = 128 km.", rnd, want=L(128000000)))
    P = People(rnd)
    n1, he1, _ = P.next()
    n2, he2, _ = P.next()
    its.append(mcq("%s cycles 30 miles. %s cycles 45 km. Who cycles further, and by about how much?" % (n1, n2),
                   "%s, by about 3 km" % n1,
                   ["%s, by about 15 km" % n2, "%s, by about 15 miles" % n2, "%s, by about 18 km" % n1],
                   "Use one unit. 30 miles: 30 ÷ 5 = 6 lots, 6 × 8 = 48 km. 48 km &gt; 45 km, so %s cycles further, "
                   "by 48 − 45 = 3 km. 45 is the bigger number, but miles are longer than kilometres." % n1, rnd))
    its.append(mcq("A marathon is about 42 km. Approximately how many miles is that, to the nearest mile?",
                   "about 26 miles", ["about 67 miles", "about 34 miles", "about 37 miles"],
                   "Kilometres to miles: divide by 8, then multiply by 5. 42 ÷ 8 = 5.25 and 5.25 × 5 = 26.25, "
                   "so about 26 miles. (67 miles goes the wrong way: 42 × 1.6.)", rnd))
    assert len(its) == 20, len(its)
    return {"title": "Miles and kilometres", "items": its}


# ------------------------------------------------------------ set 5: word problems
def set_story(rnd):
    P = People(rnd)
    its = []

    def add(q, r, w, e, want=None):
        its.append(mcq(q, r, w, e, rnd, want=want))

    n, he, his = P.next()
    add("%s makes pancakes. One batch needs 0.3 kg of flour. %s makes 3 batches from a 1.5 kg bag. "
        "How many grams of flour are left?" % (n, cap(he)),
        "600 g", ["1,200 g", "60 g", "1,410 g"],
        "3 × 0.3 = 0.9 kg used. 1.5 − 0.9 = 0.6 kg left. 0.6 × 1,000 = 600 g. "
        "(1,200 g only takes away one batch.)", ("M", 600))
    add("A recipe for 4 people uses 250 ml of milk. How many litres of milk are needed for 10 people?",
        "0.625 l", ["6.25 l", "2.5 l", "1 l"],
        "250 ÷ 4 = 62.5 ml for each person. 10 × 62.5 = 625 ml. 625 ÷ 1,000 = 0.625 l. "
        "(2.5 l uses 250 ml for each person.)", ("C", 625))
    n, he, his = P.next()
    add("A biscuit recipe uses 125 g of butter to make 12 biscuits. %s wants to make 36 biscuits. "
        "How many kilograms of butter does %s need?" % (n, he),
        "0.375 kg", ["3.75 kg", "0.125 kg", "4.5 kg"],
        "36 biscuits is 3 times 12, so 3 × 125 = 375 g. 375 ÷ 1,000 = 0.375 kg.", ("M", 375))
    add("A 2 litre carton of juice is poured into 8 glasses of 0.18 l. How many millilitres are left in the carton?",
        "560 ml", ["1,440 ml", "1,820 ml", "56 ml"],
        "8 × 0.18 = 1.44 l poured. 2 − 1.44 = 0.56 l left. 0.56 × 1,000 = 560 ml.", ("C", 560))
    n, he, his = P.next()
    add("%s posts three parcels: 1.25 kg, 750 g and 2.4 kg. What is their total mass in kilograms?" % n,
        "4.4 kg", ["753.65 kg", "11.15 kg", "3.725 kg"],
        "Change 750 g to kilograms first: 750 ÷ 1,000 = 0.75 kg. 1.25 + 0.75 + 2.4 = 4.4 kg.", ("M", 4400))
    n, he, his = P.next()
    add("%s drinks 0.35 l of milk every day for 2 weeks. How much milk is that altogether?" % n,
        "4.9 l", ["0.7 l", "2.45 l", "49 l"],
        "2 weeks = 14 days. 14 × 0.35 = 4.9 l. (2.45 l is only 1 week.)", ("C", 4900))
    add("Four pupils do a standing long jump. Oliver jumps 1.6 m, Ava jumps 155 cm, Leo jumps 1,580 mm "
        "and Isla jumps 1.06 m. Who jumps the furthest?",
        "Oliver", ["Ava", "Leo", "Isla"],
        "Change them all to centimetres: 1.6 m = 160 cm, 1,580 mm = 158 cm and 1.06 m = 106 cm. "
        "160 cm is the furthest, so Oliver jumps the furthest.")
    n, he, his = P.next()
    add("%s swims 1.2 km in a 25 m pool. How many lengths does %s swim?" % (n, he),
        "48 lengths", ["4.8 lengths", "480 lengths", "30 lengths"],
        "1.2 km = 1,200 m. 1,200 ÷ 25 = 48 lengths. Check: 48 × 25 = 1,200.")
    add("A school 5 km fun run goes round a 400 m track. How many laps is that?",
        "12.5 laps", ["125 laps", "1.25 laps", "12 laps"],
        "5 km = 5,000 m. 5,000 ÷ 400 = 12.5 laps. Check: 12 × 400 = 4,800 m and half a lap is 200 m more.")
    add("A 1.5 km relay race is split into 4 equal legs. How long is each leg in metres?",
        "375 m", ["37.5 m", "6,000 m", "0.375 m"],
        "1.5 km = 1,500 m. 1,500 ÷ 4 = 375 m. (0.375 m is the answer in kilometres written with the wrong unit.)",
        ("L", 375000))
    n, he, his = P.next()
    add("%s runs 4 laps of the playground. Each lap takes 1 minute 45 seconds. How long does %s run for?" % (n, he),
        "7 minutes", ["5 minutes 80 seconds", "6 minutes", "7 minutes 45 seconds"],
        "1 minute 45 seconds = 105 seconds. 4 × 105 = 420 seconds. 420 ÷ 60 = 7 minutes. "
        "(5 minutes 80 seconds works out 4 × 1.45 as if a minute had 100 seconds.)", ("T", 420))
    add("A film starts at 6:45 pm. It lasts 2.25 hours. What time does it finish?",
        "9:00 pm", ["9:10 pm", "8:45 pm", "9:30 pm"],
        "2.25 hours = 2 hours 15 minutes (0.25 × 60 = 15). 6:45 pm + 2 hours = 8:45 pm, "
        "and 15 more minutes is 9:00 pm. (9:10 pm uses 25 minutes.)")
    n, he, his = P.next()
    add("%s practises the piano for 25 minutes every day for 3 weeks. How long is that altogether?" % n,
        "8 hours 45 minutes", ["5 hours 25 minutes", "1 hour 15 minutes", "6 hours 15 minutes"],
        "3 weeks = 21 days. 21 × 25 = 525 minutes. 8 × 60 = 480, and 525 − 480 = 45, "
        "so it is 8 hours 45 minutes, not 5 hours 25 minutes.", ("T", 525 * 60))
    add("A sponsored walk is 12 km. The class walks 2.75 km before lunch and 3,600 m after lunch. "
        "How much further do they still have to walk?",
        "5.65 km", ["8.89 km", "6.35 km", "6.65 km"],
        "3,600 m = 3.6 km. 2.75 + 3.6 = 6.35 km walked. 12 − 6.35 = 5.65 km to go. "
        "(8.89 km treats 3,600 m as 0.36 km.)", ("L", 5650000))
    n, he, his = P.next()
    add("%s has 4.5 m of ribbon. %s cuts it into pieces 15 cm long. How many pieces does %s get?"
        % (n, cap(he), he),
        "30 pieces", ["3 pieces", "300 pieces", "60 pieces"],
        "4.5 m = 450 cm. 450 ÷ 15 = 30 pieces. (3 pieces divides 45 by 15 without converting.)")
    n, he, his = P.next()
    add("%s's family drives 45 miles to a theme park, then 32 km to a hotel. Approximately how far do they drive "
        "altogether in kilometres?" % n,
        "about 104 km", ["about 77 km", "about 72 km", "about 60 km"],
        "45 miles: 45 ÷ 5 = 9 lots, 9 × 8 = 72 km. 72 + 32 = 104 km. (77 km adds miles and kilometres "
        "as if they were the same.)", ("L", 104000000))
    n, he, his = P.next()
    add("A sign says <b>Bristol 40 miles</b>. %s's family then drives 24 km towards Bristol. "
        "Approximately how many miles do they still have to go?" % n,
        "about 25 miles", ["about 16 miles", "about 15 miles", "about 40 miles"],
        "24 km: 24 ÷ 8 = 3 lots, 3 × 5 = 15 miles. 40 − 15 = 25 miles to go. "
        "(16 miles takes away 24 without converting.)", ("L", 40000000))
    n, he, his = P.next()
    add("%s's family drives 150 miles to the coast. They stop for lunch after 80 km. "
        "Approximately how many more miles do they have to drive?" % n,
        "about 100 miles", ["about 70 miles", "about 22 miles", "about 50 miles"],
        "80 km: 80 ÷ 8 = 10 lots, 10 × 5 = 50 miles. 150 − 50 = 100 miles. "
        "(22 miles changes 80 km the wrong way, into 128.)", ("L", 160000000))
    add("A 60-mile charity cycle ride is split into 4 equal stages. Approximately how long is each stage in kilometres?",
        "about 24 km", ["about 15 km", "about 96 km", "about 37.5 km"],
        "60 ÷ 4 = 15 miles in each stage. 15 ÷ 5 = 3 lots, 3 × 8 = 24 km. "
        "(96 km is the whole ride, not one stage.)", ("L", 24000000))
    add("Put these distances in order from shortest to longest: 3 miles, 4.5 km, 4,900 m.",
        "4.5 km, 3 miles, 4,900 m", ["3 miles, 4.5 km, 4,900 m", "4,900 m, 4.5 km, 3 miles", "4.5 km, 4,900 m, 3 miles"],
        "Change them all to metres. 3 miles ≈ 3 × 1.6 = 4.8 km = 4,800 m, and 4.5 km = 4,500 m. "
        "4,500 &lt; 4,800 &lt; 4,900.")
    assert truth("4.5 km < 3 miles < 4,900 m") and not truth("3 miles < 4.5 km")
    assert len(its) == 20, len(its)
    return {"title": "Word problems: recipes, journeys and races", "items": its}


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
        "<h2>Multiply or divide?</h2>"
        "<p>To change a bigger unit into a smaller unit, <b>multiply</b>: you need more of the small units. "
        "To change a smaller unit into a bigger unit, <b>divide</b>. "
        "Multiplying by 1,000 moves every digit 3 places to the left. Dividing by 1,000 moves every digit 3 places to the right.</p>"
        "<figure class='sn-fig'>" + ladder_svg(["km", "m", "cm", "mm"], ["1,000", "100", "10"],
                                                "length units: km to m to cm to mm") +
        "<figcaption>Going to a smaller unit: multiply. Going to a bigger unit: divide.</figcaption></figure>" +
        ex("Kilograms to grams", "2.375 kg = ☐ g", "1 kg = 1,000 g. Multiply: 2.375 × 1,000 = 2,375.", "2,375 g") +
        ex("Millimetres to metres", "45 mm = ☐ m",
           "1 m = 1,000 mm. Divide: 45 ÷ 1,000 = 0.045. Use 0 as a place holder in the tenths.", "0.045 m") +
        "<h2>Facts to know</h2>" +
        table(["Measure", "Facts"], [
            ["Length", "1 cm = 10 mm &nbsp; 1 m = 100 cm = 1,000 mm &nbsp; 1 km = 1,000 m"],
            ["Mass", "1 kg = 1,000 g"],
            ["Capacity", "1 l = 1,000 ml"],
            ["Time", "1 minute = 60 seconds &nbsp; 1 hour = 60 minutes &nbsp; 1 day = 24 hours &nbsp; 1 week = 7 days"],
            ["Miles", "5 miles ≈ 8 km (so 1 mile ≈ 1.6 km)"],
        ]) +
        "<h2>Time is not decimal</h2>"
        "<p>An hour has 60 minutes, not 100. Multiply the decimal part by 60.</p>" +
        ex("Hours and minutes", "2.5 hours = ☐ hours ☐ minutes",
           "0.5 × 60 = 30 minutes.", "2 hours 30 minutes (not 2 hours 50 minutes)") +
        ex("Seconds to minutes", "210 seconds = ☐ minutes ☐ seconds",
           "3 × 60 = 180. 210 − 180 = 30 seconds left over.", "3 minutes 30 seconds") +
        "<h2>Miles and kilometres</h2>"
        "<p>A mile is longer than a kilometre. Use <b>5 miles ≈ 8 km</b> like a ratio: find how many lots of 5 miles "
        "(or 8 km) there are, then multiply.</p>"
        "<figure class='sn-fig'>" + graph_svg(from_miles=20) +
        "<figcaption>Go up from 20 miles to the line, then across: about 32 km. Each square is 5 miles across and 8 km up.</figcaption></figure>" +
        ex("Miles to kilometres", "40 miles ≈ ☐ km", "40 ÷ 5 = 8 lots. 8 × 8 = 64.", "about 64 km") +
        ex("Kilometres to miles", "24 km ≈ ☐ miles", "24 ÷ 8 = 3 lots. 3 × 5 = 15.", "about 15 miles") +
        "<h2>Read the scale, then convert</h2>"
        "<figure class='sn-fig'>" + jug_svg(1300, 2000, 500, 100) +
        "<figcaption>Each line is 100 ml. The water is at 1,300 ml, which is 1.3 l.</figcaption></figure>"
        "<h2>Common mistakes</h2>" +
        table(["Mistake", "What to do instead"], [
            ["2.5 hours = 2 hours 50 minutes", "0.5 hours = half of 60 minutes = 30 minutes"],
            ["45 mm = 4.5 m or 45 m", "1 m = 1,000 mm, so 45 mm = 45 ÷ 1,000 = 0.045 m"],
            ["1.25 l = 125 ml", "Multiply by 1,000, not 100: 1.25 l = 1,250 ml"],
            ["Multiplying to get a bigger unit (750 g = 750,000 kg)", "Smaller unit to bigger unit: divide (750 g = 0.75 kg)"],
            ["8 miles ≈ 5 km (the wrong way round)", "A mile is longer, so 5 miles ≈ 8 km"],
            ["Comparing only the numbers (5,200 cm &gt; 0.5 km)", "Use one unit first: 5,200 cm = 52 m and 0.5 km = 500 m"],
        ])
    )


FAQ = [
    {"q": "What unit conversions do Year 6 pupils need to know?",
     "a": "Year 6 pupils convert between mm, cm, m and km, g and kg, ml and l, and units of time, using decimals up to "
          "three decimal places. They also convert between miles and kilometres."},
    {"q": "How do you convert miles to kilometres in Year 6?",
     "a": "Use 5 miles ≈ 8 km. Find how many lots of 5 miles there are and multiply by 8: 40 miles is 8 lots, so about 64 km."},
    {"q": "Why is 2.5 hours not 2 hours 50 minutes?",
     "a": "An hour has 60 minutes, not 100. 0.5 hours is half an hour, which is 30 minutes, so 2.5 hours = 2 hours 30 minutes."},
    {"q": "Are converting units questions in the Year 6 SATs?",
     "a": "Yes. Converting units can come up in the reasoning papers, often in word problems with money, recipes, "
          "distances or time, and pupils may need to read scales or conversion graphs."},
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
    rnd = random.Random(6614)
    sets = [set_length(rnd), set_mass_cap(rnd), set_time(rnd), set_miles(rnd), set_story(rnd)]
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
        "country": "uk", "subject": "maths", "grade": "year-6", "slug": "converting-units", "sort": 14,
        "updated": UPDATED, "pdf_url": "",
        "title": "Converting Units",
        "seo_title": "Year 6 Converting Units Worksheets: Decimals, Time, Miles and Kilometres (Free, with Answers)",
        "short_title": "Converting units",
        "domain": "Measurement",
        "standard_code": "Year 6: Measurement",
        "standard_url": "https://www.gov.uk/government/publications/national-curriculum-in-england-mathematics-programmes-of-study",
        "standard_text": "Solve problems involving the calculation and conversion of units of measure, using decimal notation up to three decimal places where appropriate; use, read, write and convert between standard units, converting measurements of length, mass, volume and time from a smaller unit of measure to a larger unit, and vice versa, using decimal notation to up to three decimal places; convert between miles and kilometres.",
        "meta_desc": "Free Year 6 maths worksheets on converting units: length, mass and capacity with decimals to three places, time, and miles and kilometres (5 miles ≈ 8 km). Scales, conversion graphs and SATs-style word problems. 100 questions with an answer key, matched to the National Curriculum.",
        "key_big": "Bigger unit to smaller unit: multiply. Smaller unit to bigger unit: divide.",
        "key_sub": "× or ÷ 1,000 moves the digits 3 places: 2.375 kg = 2,375 g and 45 mm = 0.045 m. Time uses 60, so 2.5 hours = 2 hours 30 minutes. And 5 miles ≈ 8 km.",
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
        mark_large(u, "(ruler|conversion graph|double number line)")
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
