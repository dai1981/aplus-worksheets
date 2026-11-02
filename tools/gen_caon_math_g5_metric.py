# -*- coding: utf-8 -*-
"""
CA-ON Grade 5 Math: Metric Conversions (Ontario Curriculum 2020, Spatial Sense E2.2, with E2.1 choosing units)
  python3 tools/gen_caon_math_g5_metric.py
Use the metric prefixes to change larger units into smaller units: km to m, m to cm, cm to mm, kg to g and
L to mL, with whole numbers, two units (4 m 35 cm) and decimals to hundredths (2.5 m = 250 cm); read a ruler,
scale and jug; choose and compare units; Canadian word problems (Terry Fox Run, maple syrup, canoe portage).
Every measurement answer is parsed back to a base unit (mm, g, mL) and checked in code.
Wrong answers come from real mistakes: multiplying by 100 (or 10) instead of 1000, moving the digits the wrong
way, 2.5 m = 205 cm, 2 kg 80 g = 2800 g, adding the two numbers without converting.
Canadian English and Ontario number style (4 digits plain, 5 or more digits with a no-break space).
HTML attributes use single quotes (no backslashes in the JSON).
"""
import json, math, os, random, re
from fractions import Fraction as Fr

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "ca-on", "math", "grade-5")
UPDATED = "2026-11-02"
GREEN = "#006633"
FILL = "#cfe6d6"
RED = "#c0392b"
INK = "#2b2b2b"
WATER = "#9fd3f2"
WATER_LINE = "#2a7fb8"
WOOD = "#f6e7b8"
FONT = "Arial, Helvetica, sans-serif"
NBSP = " "


# ------------------------------------------------------------ units and checking
# unit: (family, size in the base unit mm / g / mL, word)
UNIT = {"mm": ("L", 1, "millimetres"), "cm": ("L", 10, "centimetres"), "m": ("L", 1000, "metres"),
        "km": ("L", 1000000, "kilometres"),
        "g": ("M", 1, "grams"), "kg": ("M", 1000, "kilograms"), "t": ("M", 1000000, "tonnes"),
        "mL": ("C", 1, "millilitres"), "L": ("C", 1000, "litres")}
TOK = re.compile(r"(\d[\d" + NBSP + r"]*(?:\.\d+)?)\s*(" + "|".join(sorted(UNIT, key=len, reverse=True)) +
                 r")(?![a-zA-Z])")


def parse(s):
    """'2 kg 40 g' -> ('M', 2040). None if the string is not a plain measurement."""
    s = s.strip()
    pos, fam, tot = 0, None, Fr(0)
    for mt in TOK.finditer(s):
        if s[pos:mt.start()].strip():
            return None
        fu, sz = UNIT[mt.group(2)][:2]
        if fam and fu != fam:
            return None
        fam = fu
        tot += Fr(mt.group(1).replace(NBSP, "")) * sz
        pos = mt.end()
    if fam is None or s[pos:].strip():
        return None
    return fam, tot


def truth(st):
    """'0.4 L < 450 mL' -> True/False (chains allowed)."""
    parts = re.split(r" (<|>|=) ", st)
    vals = [parse(p) for p in parts[0::2]]
    assert all(vals) and len({v[0] for v in vals}) == 1, st
    ok = True
    for i, op in enumerate(parts[1::2]):
        a, b = vals[i][1], vals[i + 1][1]
        ok = ok and {"<": a < b, ">": a > b, "=": a == b}[op]
    return ok


def c(n):
    """Ontario style: 4 digits plain (2400), 5 or more digits grouped with a no-break space (12 000)."""
    n = int(n)
    if n < 10000:
        return str(n)
    return "{:,}".format(n).replace(",", NBSP)


def fmt(x):
    """Fraction/int -> '2400', '12 000' or '0.75' (exact, at most 3 decimal places)."""
    x = Fr(x)
    assert (x * 1000).denominator == 1, x
    if x.denominator == 1:
        return c(x.numerator)
    s = ("%.3f" % float(x)).rstrip("0")
    a, _, b = s.partition(".")
    return c(int(a)) + "." + b


def m(n, u):
    return "%s %s" % (fmt(n), u)


def two(v, big, small):
    """v in base units -> '2 kg 40 g' (no zero parts)."""
    B, S = UNIT[big][1], UNIT[small][1]
    a, r = divmod(Fr(v), B)
    r = r / S
    assert r.denominator == 1
    if r == 0:
        return m(a, big)
    if a == 0:
        return m(r, small)
    return "%s %s" % (m(a, big), m(r, small))


def kgg(v):
    return two(v, "kg", "g")


def lml(v):
    return two(v, "L", "mL")


def mcm(v):
    return two(v, "m", "cm")


def cmmm(v):
    return two(v, "cm", "mm")


# ------------------------------------------------------------ helpers
def mcq(q, correct, cands, e, rnd, want=None):
    """4 choices: correct + 3 unique distractors. Measurement choices must all differ in value.
    want = (family, value in base unit) checks the correct answer."""
    correct = str(correct)
    if want is not None:
        assert parse(correct) == (want[0], Fr(want[1])), (q, correct, want, parse(correct))
    seen = {correct}
    pc = parse(correct)
    vals = {pc[1]} if pc else set()
    pick = []
    for x in cands:
        x = str(x)
        lead = x.split(" ")[0]
        if x in seen or not x or lead.startswith("-") or lead == "0":
            continue
        pv = parse(x)
        if pc and pv and pv[0] == pc[0]:
            if pv[1] in vals:
                continue
            vals.add(pv[1])
        seen.add(x)
        pick.append(x)
        if len(pick) == 3:
            break
    assert len(pick) == 3, (q, correct, cands)
    ch = pick + [correct]
    rnd.shuffle(ch)
    return {"q": q, "c": ch, "a": ch.index(correct), "e": e}


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


def marks(k, w="mark"):
    return "%d %s%s" % (k, w, "" if k == 1 else "s")


# ------------------------------------------------------------ figures
def draw_object(kind, a, b):
    """An object lying exactly from x=a to x=b, between y=12 and y=32."""
    o = []
    if kind in ("pencil", "crayon"):
        body = "#f4c542" if kind == "pencil" else "#3a6fb0"
        tipc = WOOD if kind == "pencil" else body
        tip = min(22, (b - a) * 0.3)
        o.append("<rect x='%.1f' y='12' width='%.1f' height='20' fill='%s' stroke='%s' stroke-width='1.5'/>"
                 % (a, b - a - tip, body, INK))
        if kind == "pencil":
            o.append("<rect x='%.1f' y='12' width='8' height='20' fill='#e98aa0' stroke='%s' stroke-width='1.5'/>" % (a, INK))
        else:
            o.append("<rect x='%.1f' y='12' width='%.1f' height='20' fill='#fff' stroke='%s' stroke-width='1.5'/>"
                     % (a + (b - a - tip) * 0.25, (b - a - tip) * 0.4, INK))
        o.append("<path d='M%.1f 12 L%.1f 22 L%.1f 32 Z' fill='%s' stroke='%s' stroke-width='1.5' stroke-linejoin='round'/>"
                 % (b - tip, b, b - tip, tipc, INK))
        if kind == "pencil":
            o.append("<path d='M%.1f 19.5 L%.1f 22 L%.1f 24.5 Z' fill='%s'/>" % (b - tip * 0.25, b, b - tip * 0.25, INK))
    elif kind == "eraser":
        o.append("<rect x='%.1f' y='12' width='%.1f' height='20' rx='4' fill='#f7b7c5' stroke='%s' stroke-width='1.5'/>"
                 % (a, b - a, INK))
        o.append("<rect x='%.1f' y='12' width='%.1f' height='20' fill='#5dade2' stroke='%s' stroke-width='1.5'/>"
                 % (a + (b - a) * 0.45, (b - a) * 0.4, INK))
    else:  # ribbon
        o.append("<rect x='%.1f' y='15' width='%.1f' height='14' fill='%s' stroke='%s' stroke-width='1.5'/>"
                 % (a, b - a, RED, INK))
    return "".join(o)


NAMES = {"pencil": "pencil", "crayon": "crayon", "eraser": "eraser", "ribbon": "piece of ribbon"}


def ruler_svg(s_mm, e_mm, kind="pencil", ncm=None):
    """Ruler from 0 to ncm cm with mm marks and an object from s_mm to e_mm (exact)."""
    if ncm is None:
        ncm = max(8, -(-e_mm // 10) + 1)
    PX = 38.0
    X0, YR, RH = 18, 40, 50
    W = int(X0 * 2 + PX * ncm + 26)
    H = YR + RH + 4
    X = lambda mm: X0 + PX * mm / 10.0
    a, b = X(s_mm), X(e_mm)
    o = [draw_object(kind, a, b)]
    for x in (a, b):
        o.append("<line x1='%.1f' y1='32' x2='%.1f' y2='%d' stroke='%s' stroke-width='1.2' stroke-dasharray='3 2'/>"
                 % (x, x, YR, RED))
    o.append("<rect x='4' y='%d' width='%d' height='%d' rx='3' fill='%s' stroke='%s' stroke-width='2'/>"
             % (YR, W - 8, RH, WOOD, INK))
    small, big = [], []
    for i in range(ncm * 10 + 1):
        x = X(i)
        ln = 18 if i % 10 == 0 else (12 if i % 5 == 0 else 7)
        (big if i % 10 == 0 else small).append("M%.1f %dL%.1f %d" % (x, YR, x, YR + ln))
    o.append("<path d='%s' stroke='%s' stroke-width='1'/>" % ("".join(small), INK))
    o.append("<path d='%s' stroke='%s' stroke-width='2'/>" % ("".join(big), INK))
    for cc in range(ncm + 1):
        o.append(text(X(cc * 10), YR + 38, str(cc), 15))
    o.append(text(X(ncm * 10) + 12, YR + 38, "cm", 15, anchor="start", bold=False))
    return svg_wrap(W, H, "".join(o), "ruler with %s %s from %d mm to %d mm"
                    % ("an" if kind == "eraser" else "a", NAMES[kind], s_mm, e_mm))


def dial_svg(v, mx, lab, tick, div=1, size=200):
    """Round scale, values in grams. Labels every `lab` g shown as val/div (g or kg). Needle exactly at v."""
    unit = "g" if div == 1 else "kg"
    cx = cy = size / 2.0
    R = size / 2.0 - 6

    def pt(val, r):
        ang = math.radians(-135 + 270.0 * val / mx)
        return cx + r * math.sin(ang), cy - r * math.cos(ang)
    s = ["<circle cx='%.1f' cy='%.1f' r='%.1f' fill='#fff' stroke='%s' stroke-width='6'/>" % (cx, cy, R, GREEN)]
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
             % (cx, cy, nx, ny, RED))
    s.append("<g font-size='%d' font-weight='700' fill='%s' text-anchor='middle' stroke='#fff' stroke-width='4' "
             "paint-order='stroke'>" % (15 if mx // div >= 1000 else 17, INK))
    for val in range(0, mx + 1, lab):
        x, y = pt(val, R - 36)
        s.append("<text x='%.1f' y='%.1f'>%s</text>" % (x, y + 6, fmt(Fr(val, div))))
    s.append("</g>")
    s.append("<circle cx='%.1f' cy='%.1f' r='7' fill='%s'/>" % (cx, cy, RED))
    s.append("<text x='%.1f' y='%.1f' font-size='22' font-weight='800' fill='%s' text-anchor='middle'>%s</text>"
             % (cx, cy + 62, GREEN, unit))
    return svg_wrap(size, size, "".join(s), "weighing scale in %s with the needle at %s" % (unit, kgg(v)))


def jug_svg(v, mx, lab, step, div=1, size=200):
    """Measuring jug, values in mL: a line every `step` mL, a label every `lab` mL shown as val/div (mL or L).
    Water exactly at v."""
    unit = "mL" if div == 1 else "L"
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
            s.append("<text x='%d' y='%.1f'>%s</text>" % (x0 - 7, Y(val) + 5, fmt(Fr(val, div))))
    s.append("</g>")
    s.append(text(x0 - 7, 202, unit, 15, anchor="end", col=GREEN))
    return svg_wrap(size, size + 8, "".join(s), "measuring jug in %s with water at %s" % (unit, lml(v)))

# ------------------------------------------------------------ conversions
def k_between(uf, ut):
    return Fr(UNIT[uf][1], UNIT[ut][1])


PLACES = {10: "1 place", 100: "2 places", 1000: "3 places"}


def conv_e(n, uf, ut):
    """Explanation for n uf -> ut (one step)."""
    k = k_between(uf, ut)
    r = Fr(n) * k
    if k > 1:
        k = int(k)
        s = "1 %s = %s %s. %s are bigger than %s, so multiply by %s: %s × %s = %s." % (
            uf, fmt(k), ut, cap(UNIT[uf][2]), UNIT[ut][2], fmt(k), fmt(n), fmt(k), fmt(r))
        if k in PLACES:
            s += " The digits move %s to the left." % PLACES[k]
    else:
        k = int(1 / k)
        s = "1 %s = %s %s. %s are smaller than %s, so divide by %s: %s ÷ %s = %s." % (
            ut, fmt(k), uf, cap(UNIT[uf][2]), UNIT[ut][2], fmt(k), fmt(n), fmt(k), fmt(r))
        if k in PLACES:
            s += " The digits move %s to the right." % PLACES[k]
    return s + " So %s = %s." % (m(n, uf), m(r, ut))


def conv(n, uf, ut, wrong, rnd, q=None, e=None, extra=""):
    """Convert n uf into ut. wrong = numbers in ut from real mistakes."""
    n = Fr(n)
    fam = UNIT[uf][0]
    r = n * k_between(uf, ut)
    if q is None:
        q = "Convert. <b>%s = ☐ %s</b>" % (m(n, uf), ut)
    return mcq(q, m(r, ut), [m(Fr(w), ut) for w in wrong], (e or conv_e(n, uf, ut)) + extra, rnd,
               want=(fam, n * UNIT[uf][1]))


def D(s):
    return Fr(s)


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

# ------------------------------------------------------------ lesson
def ex(title, q, s, a):
    return ("<div class='sn-ex'><span class='sn-ex-t'>%s</span><p class='sn-ex-q'>%s</p>"
            "<p class='sn-ex-s'>%s</p><p class='sn-ex-a'>Answer: %s</p></div>" % (title, q, s, a))


def table(head, rows, cls="sn-table"):
    h = "".join("<th>%s</th>" % x for x in head)
    b = "".join("<tr>" + "".join("<td>%s</td>" % x for x in r) + "</tr>" for r in rows)
    return "<div class='sn-tw'><table class='%s'><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>" % (cls, h, b)

def balance(sets, rnd):
    """Spread the correct answers evenly over the 4 positions in every set."""
    for s in sets:
        targets = [0, 1, 2, 3] * 5
        rnd.shuffle(targets)
        for it, t in zip(s["items"], targets):
            ch = it["c"]
            ch[it["a"]], ch[t] = ch[t], ch[it["a"]]
            it["a"] = t


def mark_large(u, pattern):
    """Tag pictures that must print larger so their labels stay readable."""
    rx = re.compile(r"<svg (?=[^>]*aria-label='" + pattern + ")")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u



# ------------------------------------------------------------ grade 5 helpers
def stmt(q, correct, wrong, e, rnd):
    """Choices are statements like '1 m = 100 cm'; the correct one must be true and the others false."""
    assert truth(correct), correct
    for w in wrong:
        assert not truth(w), w
    return mcq(q, correct, wrong, e, rnd)


def count_q(q, ans, word, wrong, e, rnd):
    """Answer is a whole count (bottles, pieces ...). wrong = numbers from real mistakes."""
    def w(n):
        n = Fr(n)
        return "%s %s" % (fmt(n), word if n != 1 else word.rstrip("s"))
    return mcq(q, w(ans), [w(x) for x in wrong], e, rnd)


# ------------------------------------------------------------ set 1: length
def set_length(rnd):
    its = []
    its.append(stmt("Which is true?", "1 km = 1000 m", ["1 km = 100 m", "1 km = 10 m", "1 m = 1000 km"],
                    "<b>Kilo</b> means 1000, so 1 kilometre = 1000 metres. A kilometre is about a 15-minute walk.",
                    rnd))
    its.append(stmt("Which is true?", "1 m = 100 cm", ["1 m = 10 cm", "1 m = 1000 cm", "1 cm = 100 m"],
                    "<b>Centi</b> means one hundredth, so 100 centimetres make 1 metre. "
                    "(1000 is the number of millimetres in a metre.)", rnd))
    its.append(stmt("Which is true?", "1 cm = 10 mm", ["1 cm = 100 mm", "1 cm = 1000 mm", "1 mm = 10 cm"],
                    "<b>Milli</b> means one thousandth. 1 cm has 10 small marks on a ruler, and each one is 1 mm. "
                    "So 1 cm = 10 mm.", rnd))
    its.append(conv(3, "km", "m", [300, 30, 30000], rnd,
                    extra=" (300 m multiplies by 100, but 1 km is 1000 m.)"))
    its.append(conv(7, "m", "cm", [70, 7000, D("0.07")], rnd,
                    extra=" (0.07 cm divides when it should multiply.)"))
    its.append(conv(9, "cm", "mm", [900, 9000, D("0.9")], rnd,
                    extra=" (900 mm multiplies by 100, but 1 cm is only 10 mm.)"))
    its.append(conv(12, "km", "m", [1200, 120000, 120], rnd,
                    extra=" (1200 m multiplies by 100 instead of 1000.)"))
    its.append(conv(25, "m", "cm", [250, 25000, D("0.25")], rnd))
    its.append(conv(40, "cm", "mm", [4000, 4, 40000], rnd,
                    extra=" (4 mm divides when it should multiply.)"))
    q = fig(ruler_svg(0, 60, "crayon", 7)) + "The crayon is 6 cm long. How long is it in millimetres?"
    its.append(mcq(q, "60 mm", ["6 mm", "600 mm", "0.6 mm"],
                   "Each centimetre has 10 small marks, and each small mark is 1 mm. "
                   "6 × 10 = 60, so 6 cm = 60 mm. (600 mm multiplies by 100.)", rnd, want=("L", 60)))
    q = fig(ruler_svg(0, 47, "eraser", 6)) + "How long is the eraser in millimetres?"
    its.append(mcq(q, "47 mm", ["4.7 mm", "407 mm", "470 mm"],
                   "The eraser ends 7 small marks after 4 cm. 4 cm = 40 mm, and 40 + 7 = 47 mm. "
                   "(4.7 is the length in centimetres, not millimetres.)", rnd, want=("L", 47)))
    its.append(conv(20, "km", "m", [2000, 200000, 200], rnd,
                    extra=" (2000 m uses × 100. Check: 20 km is 20 groups of 1000 m.)"))
    its.append(conv(3, "m", "mm", [300, 30, 30000], rnd,
                    extra=" (300 is the number of centimetres in 3 m, not millimetres.)"))
    its.append(mcq("Convert. <b>4 m 35 cm = ☐ cm</b>", "435 cm", ["4035 cm", "4350 cm", "75 cm"],
                   "4 m = 4 × 100 = 400 cm. 400 + 35 = 435 cm. "
                   "(75 cm uses 4 m = 40 cm, and 4035 cm uses 4 m = 4000 cm.)", rnd, want=("L", 4350)))
    its.append(mcq("Convert. <b>6 m 8 cm = ☐ cm</b>", "608 cm", ["68 cm", "680 cm", "6008 cm"],
                   "6 m = 600 cm. 600 + 8 = 608 cm. The 0 holds the tens place. "
                   "(680 cm would be 6 m 80 cm.)", rnd, want=("L", 6080)))
    its.append(mcq("Convert. <b>9 cm 4 mm = ☐ mm</b>", "94 mm", ["904 mm", "940 mm", "13 mm"],
                   "9 cm = 9 × 10 = 90 mm. 90 + 4 = 94 mm. (13 mm just adds 9 + 4.)", rnd, want=("L", 94)))
    its.append(mcq("Convert. <b>2 km 300 m = ☐ m</b>", "2300 m", ["302 m", "2030 m", "500 m"],
                   "2 km = 2 × 1000 = 2000 m. 2000 + 300 = 2300 m. "
                   "(500 m uses 2 km = 200 m, and 302 m forgets to convert the kilometres.)",
                   rnd, want=("L", 2300000)))
    its.append(mcq("Convert. <b>5 km 45 m = ☐ m</b>", "5045 m", ["5450 m", "545 m", "5405 m"],
                   "5 km = 5000 m. 5000 + 45 = 5045 m. The 0 keeps the hundreds place empty. "
                   "(5450 m would be 5 km 450 m.)", rnd, want=("L", 5045000)))
    its.append(mcq("Convert. <b>1 km 5 m = ☐ m</b>", "1005 m", ["1500 m", "105 m", "1050 m"],
                   "1 km = 1000 m. 1000 + 5 = 1005 m. (1500 m would be 1 km 500 m, and 1050 m would be "
                   "1 km 50 m.)", rnd, want=("L", 1005000)))
    its.append(mcq("Which is the same as <b>3500 m</b>?", "3 km 500 m", ["35 km", "3 km 50 m", "350 km"],
                   "1 km = 1000 m, so 3000 m = 3 km. 3500 m = 3000 m + 500 m = 3 km 500 m. "
                   "(3 km 50 m is only 3050 m.)", rnd, want=("L", 3500000)))
    assert len(its) == 20, len(its)
    return {"title": "Length: km to m, m to cm and cm to mm", "items": its}


# ------------------------------------------------------------ set 2: mass and capacity
def set_mass_cap(rnd):
    its = []
    its.append(stmt("Which is true?", "1 kg = 1000 g", ["1 kg = 100 g", "1 kg = 10 g", "1 g = 1000 kg"],
                    "<b>Kilo</b> means 1000, so 1 kilogram = 1000 grams. A 1 kg bag of flour is as heavy as "
                    "1000 paper clips.", rnd))
    its.append(stmt("Which is true?", "1 L = 1000 mL", ["1 L = 100 mL", "1 L = 10 mL", "1 mL = 1000 L"],
                    "<b>Milli</b> means one thousandth, so 1000 millilitres make 1 litre. "
                    "Four 250 mL glasses fill a 1 L jug.", rnd))
    its.append(conv(4, "kg", "g", [400, 40000, 40], rnd,
                    extra=" (400 g multiplies by 100, but 1 kg is 1000 g.)"))
    its.append(conv(6, "L", "mL", [600, 60, 60000], rnd,
                    extra=" (600 mL uses × 100. A litre has 1000 millilitres.)"))
    its.append(conv(9, "kg", "g", [900, 90000, 90], rnd))
    its.append(conv(2, "L", "mL", [200, 20, 20000], rnd))
    its.append(conv(15, "kg", "g", [1500, 150000, 150], rnd,
                    extra=" (1500 g multiplies by 100 instead of 1000.)"))
    its.append(conv(10, "L", "mL", [1000, 100000, 100], rnd,
                    extra=" Multiplying by 1000 puts 3 zeros after 10."))
    its.append(mcq("Convert. <b>3 kg 250 g = ☐ g</b>", "3250 g", ["253 g", "550 g", "3025 g"],
                   "3 kg = 3 × 1000 = 3000 g. 3000 + 250 = 3250 g. "
                   "(550 g uses 3 kg = 300 g, and 253 g adds 3 + 250.)", rnd, want=("M", 3250)))
    its.append(mcq("Convert. <b>1 L 500 mL = ☐ mL</b>", "1500 mL", ["501 mL", "600 mL", "1005 mL"],
                   "1 L = 1000 mL. 1000 + 500 = 1500 mL. (600 mL uses 1 L = 100 mL, and 1005 mL would be 1 L 5 mL.)", rnd, want=("C", 1500)))
    its.append(mcq("Convert. <b>2 kg 80 g = ☐ g</b>", "2080 g", ["2800 g", "280 g", "82 g"],
                   "2 kg = 2000 g. 2000 + 80 = 2080 g. The 0 holds the hundreds place. "
                   "(2800 g would be 2 kg 800 g.)", rnd, want=("M", 2080)))
    its.append(mcq("Convert. <b>4 L 5 mL = ☐ mL</b>", "4005 mL", ["4500 mL", "405 mL", "4050 mL"],
                   "4 L = 4000 mL. 4000 + 5 = 4005 mL. "
                   "(4500 mL would be 4 L 500 mL, and 4050 mL would be 4 L 50 mL.)", rnd, want=("C", 4005)))
    q = fig(dial_svg(2000, 4000, 1000, 500, 1000)) + \
        "The scale shows the mass of a bag of apples in kilograms. What is the mass in grams?"
    its.append(mcq(q, "2000 g", ["200 g", "20 g", "20" + NBSP + "000 g"],
                   "The needle points to 2 kg. 1 kg = 1000 g, so 2 × 1000 = 2000 g. "
                   "(200 g uses × 100.)", rnd, want=("M", 2000)))
    q = fig(dial_svg(3500, 4000, 1000, 500, 1000)) + \
        "The scale shows the mass of a pumpkin. What is the mass in grams?"
    its.append(mcq(q, "3500 g", ["350 g", "3050 g", "35" + NBSP + "000 g"],
                   "Each kilogram is split into 2 equal spaces, so each mark is half a kilogram, 500 g. "
                   "The needle is 1 mark past 3 kg: 3000 + 500 = 3500 g. (3050 g reads the half mark as 50 g.)",
                   rnd, want=("M", 3500)))
    q = fig(jug_svg(2000, 3000, 1000, 500, 1000)) + \
        "The jug is marked in litres. How much water is in it, in millilitres?"
    its.append(mcq(q, "2000 mL", ["200 mL", "20 mL", "20" + NBSP + "000 mL"],
                   "The water is at 2 L. 1 L = 1000 mL, so 2 × 1000 = 2000 mL. (200 mL uses × 100.)",
                   rnd, want=("C", 2000)))
    q = fig(jug_svg(1500, 2000, 1000, 250, 1000)) + \
        "The jug is marked in litres. How much water is in it, in millilitres?"
    its.append(mcq(q, "1500 mL", ["1200 mL", "150 mL", "1050 mL"],
                   "Each litre is split into 4 equal spaces, so each line is 1000 ÷ 4 = 250 mL. "
                   "The water is 2 lines above 1 L: 1000 + 250 + 250 = 1500 mL. "
                   "(1200 mL counts each line as 100 mL.)", rnd, want=("C", 1500)))
    its.append(mcq("Find the missing number. <b>7000 g = ☐ kg</b>", "7 kg", ["70 kg", "700 kg", "7000 kg"],
                   "1 kg = 1000 g, so count the thousands: 7000 g is 7 groups of 1000 g, which is 7 kg. "
                   "(70 kg uses 1 kg = 100 g.)", rnd, want=("M", 7000)))
    its.append(mcq("Find the missing number. <b>8000 mL = ☐ L</b>", "8 L", ["80 L", "800 L", "8000 L"],
                   "1 L = 1000 mL. 8000 mL is 8 groups of 1000 mL, which is 8 L. "
                   "(8000 L forgets to change the unit.)", rnd, want=("C", 8000)))
    its.append(mcq("Convert. <b>5 L 750 mL = ☐ mL</b>", "5750 mL", ["5075 mL", "575 mL", "755 mL"],
                   "5 L = 5000 mL. 5000 + 750 = 5750 mL. (755 mL adds 5 + 750, and 575 mL uses 5 L = 500 mL.)",
                   rnd, want=("C", 5750)))
    its.append(mcq("Convert. <b>12 kg 400 g = ☐ g</b>", "12" + NBSP + "400 g",
                   ["1600 g", "12" + NBSP + "040 g", "412 g"],
                   "12 kg = 12 × 1000 = 12" + NBSP + "000 g. 12" + NBSP + "000 + 400 = 12" + NBSP + "400 g. "
                   "(1600 g uses 12 kg = 1200 g, 412 g adds 12 + 400, and 12" + NBSP + "040 g would be 12 kg 40 g.)",
                   rnd, want=("M", 12400)))
    assert len(its) == 20, len(its)
    return {"title": "Mass and capacity: kg to g and L to mL", "items": its}


# ------------------------------------------------------------ set 3: decimals
def set_decimals(rnd):
    its = []
    its.append(conv(D("2.5"), "m", "cm", [25, 205, 2500], rnd,
                    extra=" (205 cm reads 2.5 m as 2 m 5 cm, but 0.5 m is half a metre, 50 cm.)"))
    its.append(conv(D("1.5"), "km", "m", [150, 1005, 15000], rnd,
                    extra=" (150 m multiplies by 100, and 1005 m reads 1.5 km as 1 km 5 m.)"))
    its.append(conv(D("3.5"), "kg", "g", [350, 3005, 35000], rnd,
                    extra=" (0.5 kg is half a kilogram, 500 g, so it is not 3005 g.)"))
    its.append(conv(D("0.5"), "L", "mL", [50, 5, 5000], rnd,
                    extra=" Half a litre is 500 mL."))
    its.append(conv(D("4.5"), "cm", "mm", [450, 405, D("0.45")], rnd,
                    extra=" (0.45 mm moves the digits the wrong way.)"))
    its.append(conv(D("1.25"), "m", "cm", [D("12.5"), 1025, 1250], rnd,
                    extra=" (12.5 cm multiplies by 10, and 1250 cm multiplies by 1000.)"))
    its.append(conv(D("2.75"), "L", "mL", [275, 2075, 27500], rnd,
                    extra=" (275 mL multiplies by 100, but 1 L is 1000 mL.)"))
    its.append(conv(D("0.75"), "kg", "g", [75, 7500, D("7.5")], rnd,
                    extra=" (75 g uses × 100. A quarter of a kilogram is 250 g, so 0.75 kg is 3 × 250 = 750 g.)"))
    its.append(conv(D("6.4"), "km", "m", [640, 6004, 64000], rnd))
    its.append(conv(D("0.3"), "m", "cm", [3, 300, D("0.03")], rnd,
                    extra=" (3 cm multiplies by 10, and 0.03 cm moves the digits the wrong way.)"))
    its.append(conv(D("7.2"), "cm", "mm", [720, 702, D("0.72")], rnd))
    its.append(conv(D("0.25"), "L", "mL", [25, 2500, D("2.5")], rnd,
                    extra=" Check: 0.25 L is a quarter of a litre, and 1000 ÷ 4 = 250."))
    its.append(conv(D("1.05"), "m", "cm", [150, D("10.5"), 1050], rnd,
                    extra=" (150 cm would be 1.5 m. The 0 in 1.05 means 0 tenths.)"))
    its.append(conv(D("4.08"), "kg", "g", [4800, 408, 40800], rnd,
                    extra=" (4800 g would be 4.8 kg. Keep the 0 in its place.)"))
    its.append(conv(D("9.6"), "L", "mL", [960, 9006, 96000], rnd))
    its.append(conv(D("3.02"), "km", "m", [3200, 302, 30200], rnd,
                    extra=" (3200 m would be 3.2 km.)"))
    its.append(mcq("Which is the same as <b>2.4 m</b>?", "240 cm", ["24 cm", "2 m 4 cm", "2400 cm"],
                   "1 m = 100 cm, so 2.4 × 100 = 240 cm. (2 m 4 cm is 204 cm. The 4 in 2.4 is 4 tenths of a "
                   "metre, which is 40 cm.)", rnd, want=("L", 2400)))
    its.append(mcq("Which is the same as <b>1.6 kg</b>?", "1 kg 600 g", ["1 kg 6 g", "1 kg 60 g", "16 kg"],
                   "0.6 kg = 0.6 × 1000 = 600 g. So 1.6 kg = 1 kg 600 g = 1600 g. "
                   "(1 kg 6 g reads the decimal digit as grams.)", rnd, want=("M", 1600)))
    q = fig(jug_svg(2500, 3000, 1000, 500, 1000)) + \
        "The jug is marked in litres. How much juice is in it, in millilitres?"
    its.append(mcq(q, "2500 mL", ["250 mL", "2005 mL", "25" + NBSP + "000 mL"],
                   "Each line is half a litre. The juice is 1 line above 2 L, so it is 2.5 L. "
                   "2.5 × 1000 = 2500 mL. (250 mL multiplies by 100.)", rnd, want=("C", 2500)))
    its.append(conv(D("3.25"), "km", "m", [325, 3025, 32500], rnd,
                    extra=" (3025 m would be 3 km 25 m, which is 3.025 km.)"))
    assert len(its) == 20, len(its)
    return {"title": "Decimal measurements: 2.5 m = 250 cm", "items": its}


# ------------------------------------------------------------ set 4: choose the unit and compare
def set_choose(rnd):
    its = []
    for obj, ans, wr, e in [
        ("the length of a pencil", "centimetres (cm)", ["kilometres (km)", "litres (L)", "kilograms (kg)"],
         "A pencil is about 15 cm long, so centimetres fit. Litres measure capacity and kilograms measure mass."),
        ("the distance from Toronto to Ottawa", "kilometres (km)", ["centimetres (cm)", "millimetres (mm)",
                                                                    "grams (g)"],
         "Toronto to Ottawa is a long drive, so kilometres fit. Centimetres and millimetres are far too small."),
        ("the mass of a full backpack", "kilograms (kg)", ["grams (g)", "millilitres (mL)", "metres (m)"],
         "A full backpack is heavy, so kilograms fit. Grams are for light things like a pencil."),
        ("the mass of a paper clip", "grams (g)", ["kilograms (kg)", "litres (L)", "centimetres (cm)"],
         "A paper clip is very light, about 1 g, so grams fit."),
        ("how much water a bathtub holds", "litres (L)", ["millilitres (mL)", "grams (g)", "metres (m)"],
         "A bathtub holds a lot of water, so litres fit. Millilitres are for small amounts, like a spoonful."),
        ("how much medicine fits in a spoon", "millilitres (mL)", ["litres (L)", "kilograms (kg)",
                                                                   "kilometres (km)"],
         "A spoon holds only a small amount, about 5 mL, so millilitres fit."),
    ]:
        its.append(mcq("Which unit is best for measuring <b>%s</b>?" % obj, ans, wr, e, rnd))
    for obj, ans, wr, e in [
        ("the length of a canoe", "5 m", ["5 km", "5 cm", "50 m"],
         "A canoe is about as long as 3 adults lying end to end, so about 5 m. 50 m is half a soccer field."),
        ("the mass of a hockey puck", "170 g", ["170 kg", "17 kg", "1700 kg"],
         "A hockey puck fits in your hand and is light, so grams fit. 17 kg is about the mass of a small dog."),
        ("how much a juice box holds", "200 mL", ["200 L", "20 L", "2 L"],
         "A juice box holds much less than a litre, so 200 mL fits. 2 L is a big carton."),
        ("the height of a classroom door", "2 m", ["2 cm", "2 km", "20 m"],
         "A door is a little taller than an adult, so about 2 m. 20 m is about as tall as a 6-storey building."),
    ]:
        its.append(mcq("Which is the most sensible measurement for <b>%s</b>?" % obj, ans, wr, e, rnd))
    its.append(mcq("A metre is ☐ times as long as a centimetre. What number goes in the box?", "100",
                   ["10", "1000", "0.01"],
                   "100 cm = 1 m, so a metre is 100 times as long as a centimetre. "
                   "(10 is for centimetres and millimetres. 0.01 compares the other way.)", rnd))
    its.append(mcq("A kilometre is ☐ times as long as a metre. What number goes in the box?", "1000",
                   ["100", "10", "10" + NBSP + "000"],
                   "<b>Kilo</b> means 1000. 1000 m = 1 km, so a kilometre is 1000 times as long as a metre. (100 is for metres and centimetres.)", rnd))
    q = fig(ladder_svg(["km", "m", "cm", "mm"], ["1000", "?", "10"], "length units: km to m to cm to mm")) + \
        "The chart shows how to change between length units. What number goes where the <b>?</b> is?"
    its.append(mcq(q, "100", ["10", "1000", "0.01"],
                   "The ? is between metres and centimetres. 1 m = 100 cm, so you multiply by 100 to go from "
                   "m to cm, and divide by 100 to go back.", rnd))
    its.append(mcq("Which is the <b>longest</b>?", "3 km", ["2900 m", "2950 m", "2 km 990 m"],
                   "Change them all to metres: 3 km = 3000 m and 2 km 990 m = 2990 m. 3000 m is the longest. "
                   "(2900 has the biggest number, but metres are a smaller unit.)", rnd, want=("L", 3000000)))
    its.append(mcq("Which is the <b>heaviest</b>?", "4 kg", ["3900 g", "3 kg 950 g", "3999 g"],
                   "Change them all to grams: 4 kg = 4000 g and 3 kg 950 g = 3950 g. 4000 g is the heaviest.",
                   rnd, want=("M", 4000)))
    its.append(mcq("Which is the <b>shortest</b>?", "85 mm", ["9 cm", "10 cm", "1 m"],
                   "Change them all to millimetres: 9 cm = 90 mm, 10 cm = 100 mm and 1 m = 1000 mm. "
                   "85 mm is the shortest. (85 is the biggest number, but millimetres are the smallest unit.)",
                   rnd, want=("L", 85)))
    its.append(mcq("Which holds the <b>least</b>?", "750 mL", ["1 L", "1 L 50 mL", "2 L"],
                   "1 L = 1000 mL, so 750 mL is less than 1 L. The other amounts are all 1000 mL or more. "
                   "(750 is a big number, but millilitres are a small unit.)", rnd, want=("C", 750)))
    its.append(stmt("Which is true?", "2.5 kg = 2500 g", ["2.5 kg = 250 g", "2.5 kg = 25 g", "2.5 kg = 2005 g"],
                    "1 kg = 1000 g, so 2.5 × 1000 = 2500 g. (250 g multiplies by 100, and 2005 g reads "
                    "0.5 kg as 5 g.)", rnd))
    its.append(mcq("Convert. <b>1 km = ☐ cm</b>", "100" + NBSP + "000 cm", ["1000 cm", "10" + NBSP + "000 cm", "100 cm"],
                   "Do it in two steps. 1 km = 1000 m, and each metre is 100 cm. 1000 × 100 = 100" + NBSP +
                   "000 cm. (1000 cm stops after the first step.)", rnd, want=("L", 1000000)))
    its.append(mcq("Kai says <b>6 m = 60 cm</b>. What mistake did he make?",
                   "He multiplied by 10 instead of 100.",
                   ["He multiplied by 1000 instead of 100.", "He divided instead of multiplying.",
                    "He made no mistake."],
                   "1 m = 100 cm, so 6 m = 6 × 100 = 600 cm. Kai used 10, which is the number of millimetres "
                   "in a centimetre.", rnd))
    assert len(its) == 20, len(its)
    return {"title": "Choose the unit and compare", "items": its}


# ------------------------------------------------------------ set 5: word problems
def set_story(rnd):
    its = []

    def add(q, correct, wrong, e, want=None):
        its.append(mcq(q, correct, wrong, e, rnd, want=want))

    add("Olivia’s school runs the Terry Fox Run. The route is 5 km long. How many metres is that?",
        "5000 m", ["500 m", "50" + NBSP + "000 m", "50 m"],
        "1 km = 1000 m, so 5 × 1000 = 5000 m. (500 m multiplies by 100.)", ("L", 5000000))
    add("Maya’s backpack has a mass of 4 kg. Her lunch has a mass of 600 g. What is the total mass in grams?",
        "4600 g", ["604 g", "1000 g", "4060 g"],
        "Change to one unit first: 4 kg = 4000 g. 4000 + 600 = 4600 g. "
        "(604 g adds 4 + 600 without converting, and 1000 g uses 4 kg = 400 g.)", ("M", 4600))
    assert 2000 // 250 == 8
    its.append(count_q("A 2 L carton of milk is poured into glasses that hold 250 mL each. "
                       "How many glasses can be filled?", 8, "glasses", [80, 500, Fr(125)],
                       "2 L = 2000 mL. 2000 ÷ 250 = 8 glasses. Check: 4 glasses make 1 L. "
                       "(500 multiplies 2 × 250, and 125 divides 250 by 2.)", rnd))
    assert 200 // 20 == 10
    its.append(count_q("Emma has 2 m of ribbon. She cuts it into pieces that are 20 cm long. "
                       "How many pieces does she get?", 10, "pieces", [1, 100, 40],
                       "2 m = 200 cm. 200 ÷ 20 = 10 pieces. (1 piece uses 2 m = 20 cm, and 40 multiplies 2 × 20.)",
                       rnd))
    add("A portage on a canoe trip is 1.2 km long. How many metres is the portage?",
        "1200 m", ["120 m", "1002 m", "12" + NBSP + "000 m"],
        "1 km = 1000 m, so 1.2 × 1000 = 1200 m. (120 m multiplies by 100, and 1002 m reads 1.2 km as 1 km 2 m.)",
        ("L", 1200000))
    assert 5000 // 250 == 20
    its.append(count_q("A sugar shack has 5 L of maple syrup. It fills bottles that hold 250 mL each. "
                       "How many bottles can it fill?", 20, "bottles", [2, 1250, 4],
                       "5 L = 5000 mL. 5000 ÷ 250 = 20 bottles. Check: 4 bottles make 1 L, and 5 × 4 = 20. "
                       "(2 bottles uses 5 L = 500 mL, and 4 is the number of bottles in just 1 L.)", rnd))
    add("A newborn moose calf has a mass of about 15 kg. About how many grams is that?",
        "15" + NBSP + "000 g", ["1500 g", "150" + NBSP + "000 g", "150 g"],
        "1 kg = 1000 g, so 15 × 1000 = 15" + NBSP + "000 g. (1500 g multiplies by 100.)", ("M", 15000))
    add("Four friends each bring a 750 mL water bottle on a field trip. How many litres of water is that altogether?",
        "3 L", ["30 L", "3000 L", "0.3 L"],
        "4 × 750 = 3000 mL. 1 L = 1000 mL, so 3000 mL = 3 L. (3000 L forgets to change the unit, "
        "and 30 L uses 1 L = 100 mL.)", ("C", 3000))
    add("Zoe is 1.35 m tall. How tall is she in centimetres?",
        "135 cm", ["13.5 cm", "1035 cm", "1350 cm"],
        "1 m = 100 cm, so 1.35 × 100 = 135 cm. (13.5 cm multiplies by 10, and 1350 cm by 1000.)", ("L", 1350))
    add("A pumpkin from a farm stand has a mass of 4.25 kg. What is its mass in grams?",
        "4250 g", ["425 g", "4025 g", "42" + NBSP + "500 g"],
        "1 kg = 1000 g, so 4.25 × 1000 = 4250 g. (425 g multiplies by 100, and 4025 g reads 0.25 kg as 25 g.)",
        ("M", 4250))
    add("Noah’s hockey stick is 1.5 m long. His little sister’s stick is 95 cm long. How much longer is Noah’s stick, "
        "in centimetres?",
        "55 cm", ["93.5 cm", "10 cm", "80 cm"],
        "1.5 m = 150 cm. 150 − 95 = 55 cm. (93.5 cm takes 1.5 from 95 without converting, 80 cm uses 1.5 m = 15 cm, "
        "and 10 cm uses 1.5 m = 105 cm.)", ("L", 550))
    add("After a snowstorm in Ottawa, there is 0.4 m of snow on the ground. How deep is the snow in centimetres?",
        "40 cm", ["4 cm", "400 cm", "0.04 cm"],
        "1 m = 100 cm, so 0.4 × 100 = 40 cm. (4 cm multiplies by 10, 400 cm by 1000, and 0.04 cm divides.)",
        ("L", 400))
    add("Arjun runs 3 laps of a 400 m track. Then he runs 2 km more. How many metres does he run in all?",
        "3200 m", ["1400 m", "1202 m", "1220 m"],
        "3 × 400 = 1200 m. 2 km = 2000 m. 1200 + 2000 = 3200 m. "
        "(1400 m uses 2 km = 200 m, 1220 m uses 2 km = 20 m, and 1202 m forgets to convert the 2 km.)", ("L", 3200000))
    add("A bag has 2 kg of flour. Liam uses 750 g to make bread. How much flour is left, in grams?",
        "1250 g", ["748 g", "1350 g", "2750 g"],
        "2 kg = 2000 g. 2000 − 750 = 1250 g. (748 g takes 2 from 750 without converting, "
        "1350 g is a regrouping mistake, and 2750 g adds instead of subtracting.)", ("M", 1250))
    assert 1000 // 25 == 40
    its.append(count_q("Kai swims 1 km in a pool that is 25 m long. How many lengths of the pool does he swim?",
                       40, "lengths", [4, 400, 25],
                       "1 km = 1000 m. 1000 ÷ 25 = 40 lengths. Check: 40 × 25 = 1000. "
                       "(4 lengths uses 1 km = 100 m, and 400 lengths uses 1 km = 10" + NBSP + "000 m.)", rnd))
    add("A bucket for maple sap holds 8 L. It has 3500 mL of sap in it now. How many more millilitres will fill it?",
        "4500 mL", ["3492 mL", "11" + NBSP + "500 mL", "5500 mL"],
        "8 L = 8000 mL. 8000 − 3500 = 4500 mL. (3492 mL takes 8 from 3500 without converting, "
        "and 11" + NBSP + "500 mL adds instead of subtracting.)", ("C", 4500))
    add("The CN Tower in Toronto is 553 m tall. How tall is it in centimetres?",
        "55" + NBSP + "300 cm", ["5530 cm", "553" + NBSP + "000 cm", "5.53 cm"],
        "1 m = 100 cm, so 553 × 100 = 55" + NBSP + "300 cm. (5530 cm multiplies by 10, 553" + NBSP +
        "000 cm by 1000, and 5.53 cm divides by 100.)", ("L", 553000))
    add("A 1 kg bag of trail mix is shared equally into 8 small bags for a hike. How many grams go in each bag?",
        "125 g", ["12.5 g", "8000 g", "992 g"],
        "1 kg = 1000 g. 1000 ÷ 8 = 125 g. Check: 8 × 125 = 1000. "
        "(12.5 g uses 1 kg = 100 g, 8000 g multiplies, and 992 g takes away 8.)", ("M", 125))
    add("A cross-country ski trail is 3 km 250 m long. Hana skis the trail twice. How many metres does she ski?",
        "6500 m", ["6050 m", "650 m", "3250 m"],
        "3 km 250 m = 3000 + 250 = 3250 m. 2 × 3250 = 6500 m. (6050 m uses 3 km 250 m = 3025 m, "
        "and 3250 m is only one time around.)", ("L", 6500000))
    add("For Thanksgiving, Ava’s family buys a 7.5 kg turkey and 2 kg 400 g of potatoes. "
        "What is the total mass in grams?",
        "9900 g", ["3150 g", "9504 g", "7740 g"],
        "7.5 kg = 7500 g and 2 kg 400 g = 2400 g. 7500 + 2400 = 9900 g. "
        "(3150 g uses 7.5 kg = 750 g, and 9504 g uses 2 kg 400 g = 2004 g.)", ("M", 9900))
    assert len(its) == 20, len(its)
    return {"title": "Word problems: Terry Fox Run, maple syrup and canoe trips", "items": its}


# ------------------------------------------------------------ lesson
def body_html():
    return (
        "<h2>Big unit to small unit: multiply</h2>"
        "<p>Metric units are built on 10s. Each prefix tells you the size: <b>kilo</b> means 1000, "
        "<b>centi</b> means one hundredth and <b>milli</b> means one thousandth. "
        "To change a bigger unit into a smaller unit, <b>multiply</b>. You need more of the small units.</p>"
        "<figure class='sn-fig'>" + ladder_svg(["km", "m", "cm", "mm"], ["1000", "100", "10"],
                                                "length units: km to m to cm to mm") +
        "<figcaption>Going to a smaller unit: multiply. Going to a bigger unit: divide.</figcaption></figure>" +
        table(["Measure", "Facts to know"], [
            ["Length", "1 km = 1000 m &nbsp; 1 m = 100 cm &nbsp; 1 cm = 10 mm &nbsp; 1 m = 1000 mm"],
            ["Mass", "1 kg = 1000 g"],
            ["Capacity", "1 L = 1000 mL"],
        ]) +
        "<figure class='sn-fig'>" + ruler_svg(0, 47, "eraser", 6) +
        "<figcaption>Each centimetre has 10 small marks. The eraser is 4 cm 7 mm = 47 mm long.</figcaption>"
        "</figure>" +
        ex("Example 1: kilometres to metres", "3 km = ☐ m", "1 km = 1000 m. Multiply: 3 × 1000 = 3000.", "3000 m") +
        ex("Example 2: two units", "2 kg 80 g = ☐ g", "2 kg = 2000 g. Then 2000 + 80 = 2080.", "2080 g (not 2800 g)") +
        "<h2>Decimals: move the digits to the left</h2>"
        "<p>Multiplying by 10 moves every digit 1 place to the left. Multiplying by 100 moves it 2 places, "
        "and multiplying by 1000 moves it 3 places.</p>" +
        ex("Example 3: a decimal in metres", "2.5 m = ☐ cm", "1 m = 100 cm. Multiply: 2.5 × 100 = 250.",
           "250 cm (not 25 cm or 205 cm)") +
        ex("Example 4: a decimal in litres", "0.75 L = ☐ mL", "1 L = 1000 mL. Multiply: 0.75 × 1000 = 750.",
           "750 mL") +
        "<figure class='sn-fig'>" + jug_svg(1500, 2000, 1000, 250, 1000) +
        "<figcaption>Each line is 250 mL. The water is at 1.5 L, which is 1500 mL.</figcaption></figure>"
        "<h2>Choose the unit</h2>"
        "<p>Pick the unit that gives an easy number. Use mm or cm for small lengths, m for rooms and rinks, "
        "and km for trips. Use g for light things and kg for heavy things. Use mL for a spoon or a cup and "
        "L for a bathtub.</p>"
        "<h2>Common mistakes</h2>" +
        table(["Mistake", "What to do instead"], [
            ["3 km = 300 m (multiplying by 100)", "1 km = 1000 m, so 3 km = 3000 m"],
            ["7 m = 0.07 cm (moving the digits the wrong way)",
             "Bigger unit to smaller unit: multiply. 7 m = 700 cm"],
            ["2.5 m = 205 cm", "0.5 m is half a metre, 50 cm. So 2.5 m = 250 cm"],
            ["2 kg 80 g = 2800 g", "2000 + 80 = 2080 g. Keep the 0 in the hundreds place"],
        ])
    )


FAQ = [
    {"q": "What metric conversions do Grade 5 students learn in the Ontario math curriculum?",
     "a": "Grade 5 students use the metric prefixes to change larger units into smaller ones: km to m, m to cm, "
          "cm to mm, kg to g and L to mL, including decimals such as 2.5 m = 250 cm."},
    {"q": "How do you convert kilometres to metres?",
     "a": "Multiply by 1000, because 1 km = 1000 m. So 3 km = 3000 m and 1.5 km = 1500 m."},
    {"q": "Why do I multiply when I change metres to centimetres?",
     "a": "A centimetre is smaller than a metre, so you need more of them: 100 cm fit in every metre. "
          "Bigger unit to smaller unit always means multiply."},
    {"q": "What is the most common mistake with metric conversions?",
     "a": "Using the wrong number, such as multiplying by 100 for km to m or kg to g when the answer needs × 1000. "
          "Learning the prefixes kilo (1000), centi (one hundredth) and milli (one thousandth) helps."},
]


def gen_unit():
    rnd = random.Random(45819)
    sets = [set_length(rnd), set_mass_cap(rnd), set_decimals(rnd), set_choose(rnd), set_story(rnd)]
    balance(sets, rnd)
    seen = set()
    for s in sets:
        assert len(s["items"]) == 20, (s["title"], len(s["items"]))
        pos = [0, 0, 0, 0]
        for it in s["items"]:
            assert len(set(it["c"])) == 4, it
            assert it["e"], it
            pos[it["a"]] += 1
            k = it["q"] + "|" + "|".join(sorted(it["c"]))
            assert k not in seen, it["q"]
            seen.add(k)
            assert it["q"].count("<svg") <= 1
            assert "," not in "".join(re.findall(r"\d,\d", it["q"] + it["e"] + "".join(it["c"])))
        assert pos == [5, 5, 5, 5], (s["title"], pos)
    return {
        "country": "ca-on", "subject": "math", "grade": "grade-5", "slug": "metric-conversions", "sort": 19,
        "updated": UPDATED, "pdf_url": "",
        "title": "Metric Conversions: km to m, m to cm, cm to mm, kg to g and L to mL",
        "seo_title": "Grade 5 Metric Conversions Worksheets: km, m, cm, mm, kg, g, L, mL (Free Math, Answer Key)",
        "short_title": "Metric Conversions",
        "domain": "Spatial Sense",
        "standard_code": "Grade 5: E2.2",
        "standard_url": "https://www.dcp.edu.gov.on.ca/en/curriculum/elementary-mathematics",
        "standard_text": "Use the metric prefixes to convert larger units to smaller units for length, mass, and "
                         "capacity, and describe the base-ten relationships among metric units",
        "meta_desc": "Free Grade 5 math worksheets on metric conversions for the Ontario curriculum: km to m, m to cm, "
                     "cm to mm, kg to g and L to mL, decimals like 2.5 m = 250 cm, choosing the unit, and Terry Fox "
                     "Run and maple syrup word problems. 100 questions with an answer key.",
        "key_big": "Bigger unit to smaller unit: multiply.",
        "key_sub": "1 km = 1000 m, 1 m = 100 cm, 1 cm = 10 mm, 1 kg = 1000 g and 1 L = 1000 mL. "
                   "So 2.5 m = 2.5 × 100 = 250 cm.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }


if __name__ == "__main__":
    u = gen_unit()
    mark_large(u, "(ruler|length units)")
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
