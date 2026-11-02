# -*- coding: utf-8 -*-
"""
Singapore Primary 5 Maths: Decimals and measurement (MOE 2021 Primary Mathematics Syllabus, Standard)
  python3 tools/gen_sg_maths_p5_decimals.py
× and ÷ decimals by 10, 100, 1000 and their multiples (0.45 × 30, 8.4 ÷ 20), converting km, m, cm, kg, g,
ℓ and ml in decimal form (2.35 km = 2350 m, 450 g = 0.45 kg), compound units to decimals (3 ℓ 40 ml = 3.04 ℓ),
then word problems with bar models in Singapore contexts.
Every answer is computed with decimal.Decimal. Every measurement choice is parsed back to a base unit
(cm, g, ml) and checked: the correct one must equal the true value, and no two choices may be equal.
Wrong answers are real student mistakes: moving the digits the wrong way or the wrong number of places,
“just add a zero”, 3 ℓ 40 ml = 3.4 ℓ, 1 m = 10 cm, 1 km = 100 m, dropping a place-holding zero,
forgetting the × 10 / ÷ 10 step with multiples, and adding numbers with different units.
Singapore style: British spelling, ℓ and ml, $ and ¢. 4-digit numbers have no separator (2350);
5 or more digits use a no-break space (12 500). HTML attributes use single quotes (no backslashes in the JSON).
"""
import json, math, os, random, re
from decimal import Decimal as Dm

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "sg", "maths", "primary-5")
UPDATED = "2026-11-03"
GREEN = "#006633"
HEADFILL = "#cfe6d6"
PARTFILL = "#fde3c8"
ORANGE = "#b35900"
INK = "#2b2b2b"
RED = "#c0392b"
GHOST = "#9a9a9a"
THIN = "#8a8a8a"
WATER = "#9fd3f2"
WATER_LINE = "#2a7fb8"
FONT = "Arial, Helvetica, sans-serif"
NB = " "
PLACE = {3: "thousands", 2: "hundreds", 1: "tens", 0: "ones", -1: "tenths", -2: "hundredths", -3: "thousandths"}

# unit: (family, size in the base unit)  base units: cm, g, ml
UNIT = {"km": ("L", 100000), "m": ("L", 100), "cm": ("L", 1),
        "kg": ("M", 1000), "g": ("M", 1), "ℓ": ("C", 1000), "ml": ("C", 1)}
WORD = {"km": "kilometres", "m": "metres", "cm": "centimetres", "kg": "kilograms", "g": "grams",
        "ℓ": "litres", "ml": "millilitres"}
FACTOR = {("km", "m"): 1000, ("m", "cm"): 100, ("kg", "g"): 1000, ("ℓ", "ml"): 1000}


# ------------------------------------------------------------ numbers
def N(x):
    """Exact decimal text, Singapore style: 4536, 12 350 (no-break space), 0.045."""
    d = Dm(str(x).replace(NB, "").replace(" ", "")).normalize()
    s = format(d, "f")
    w, _, f = s.partition(".")
    if len(w) >= 5:
        g = []
        while w:
            g.insert(0, w[-3:])
            w = w[:-3]
        w = NB.join(g)
    return w + ("." + f if f else "")


def M(x):
    """Money: $135, $4.50."""
    d = Dm(x)
    if d == d.to_integral_value():
        return "$" + N(d)
    q = format(d.quantize(Dm("0.01")), "f")
    assert Dm(q) == d, x
    w, _, f = q.partition(".")
    return "$" + N(w) + "." + f


def U(n, u):
    return N(n) + " " + u


def P10(k):
    return N(10 ** k)


def calc(x, op, k):
    x = Dm(str(x))
    return x * 10 ** k if op == "×" else x / 10 ** k


def places(x):
    s = str(x)
    return len(s.split(".")[1]) if "." in s else 0


TOK = re.compile(r"([\d" + NB + r"]*\.?\d+) (km|kg|ml|cm|m|g|ℓ)(?![a-zA-Z])")
NUM = re.compile(r"^(\$)?([\d" + NB + r"]*\.?\d+)$")


def parse(c):
    """'3 ℓ 40 ml' -> ('C', 3040); '0.45' -> ('', 0.45); '$4.50' -> ('$', 4.50); otherwise None."""
    c = c.strip()
    m = NUM.match(c)
    if m:
        return ("$" if m.group(1) else "", Dm(m.group(2).replace(NB, "")))
    pos, fam, tot = 0, None, Dm(0)
    for t in TOK.finditer(c):
        if c[pos:t.start()].strip():
            return None
        f, sz = UNIT[t.group(2)]
        if fam and f != fam:
            return None
        fam = f
        tot += Dm(t.group(1).replace(NB, "")) * sz
        pos = t.end()
    if fam is None or c[pos:].strip():
        return None
    return (fam, tot)


def mcq(q, correct, wrong, e, want=None, same_ok=False):
    """4 choices: correct first + 3 wrong. No two choices may have the same value (in the same family).
    want = (family, value in base unit) or a plain number: checks the correct answer."""
    correct = str(correct)
    wrong = [str(x) for x in wrong]
    assert len(wrong) == 3, (q, wrong)
    ch = [correct] + wrong
    assert len(set(ch)) == 4, (q, ch)
    if want is not None:
        w = want if isinstance(want, tuple) else ("", Dm(str(want)))
        assert parse(correct) == (w[0], Dm(w[1])), (q, correct, want, parse(correct))
    if not same_ok:
        vs = [parse(x) for x in ch]
        assert all(v is not None for v in vs), (q, ch)
        assert len({v[0] for v in vs}) == 1, (q, ch)
        assert len({v[1] for v in vs}) == 4, (q, ch)
        assert all(v[1] > 0 for v in vs), (q, ch)
    return {"q": q, "c": ch, "a": 0, "e": e}


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


def cap(s):
    return s[0].upper() + s[1:]


def fig(svg):
    return "<div class='qfig'>" + svg + "</div>"


def svg_wrap(w, h, body, label, font=FONT):
    return ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 %d %d' width='%d' height='%d' "
            "role='img' aria-label='%s'><g font-family='%s'>%s</g></svg>" % (w, h, w, h, label, font, body))


def text(x, y, t, fs=16, anchor="middle", col=INK, weight=700):
    return ("<text x='%.1f' y='%.1f' font-size='%d' font-weight='%d' fill='%s' text-anchor='%s'>%s</text>"
            % (x, y, fs, weight, col, anchor, t))


def tw(s, fs):
    """Rough text width of bold Arial."""
    w = 0
    for ch in s:
        if ch in ".,: " + NB:
            w += 0.3
        elif ch in "ℓl1i":
            w += 0.45
        elif ch in "m×÷?":
            w += 0.85
        else:
            w += 0.6
    return w * fs


def table(head, rows):
    h = "".join("<th>%s</th>" % x for x in head)
    b = "".join("<tr>" + "".join("<td>%s</td>" % c for c in r) + "</tr>" for r in rows)
    return "<div class='sn-tw'><table class='sn-table'><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>" % (h, b)


def ex(title, q, s, a):
    return ("<div class='sn-ex'><span class='sn-ex-t'>%s</span><p class='sn-ex-q'>%s</p>"
            "<p class='sn-ex-s'>%s</p><p class='sn-ex-a'>Answer: %s</p></div>" % (title, q, s, a))


# ------------------------------------------------------------ figure: place value chart with arrows
def split_digits(s):
    w, _, f = s.replace(NB, "").partition(".")
    d = {}
    for j, ch in enumerate(w):
        d[len(w) - 1 - j] = ch
    for j, ch in enumerate(f):
        d[-(j + 1)] = ch
    return d


def pv_move(x, op, k, hi=None, show_answer=True, CW=106):
    """Two-row place value chart: x on top, x op 10^k below, red arrows from each digit to its new place.
    Zeros that only hold an empty place are grey. hi: place of a digit of x; that digit is red in the answer row."""
    r = N(calc(x, op, k))
    top, bot = split_digits(N(x)), split_digits(r)
    shift = k if op == "×" else -k
    moved = {p + shift for p in top}
    hi_place = None if hi is None else hi + shift
    cols = list(range(max(max(top), max(bot)), min(min(top), min(bot), -1) - 1, -1))
    assert all(p in PLACE for p in cols), (x, op, k)
    PW = 16
    HEAD, ROW, BAND, LW = 30, 44, 46, 76
    x0, y0 = 4, 4
    gw = len(cols) * CW + PW
    W = 2 * x0 + LW + gw
    yt = y0 + HEAD
    yb = yt + ROW + BAND
    gy = yb + ROW
    H = gy + y0
    xs, xx = {}, x0 + LW
    for p in cols:
        xs[p] = xx
        xx += CW + (PW if p == 0 else 0)
    cx = {p: xs[p] + CW / 2.0 for p in cols}
    o = ["<rect x='%d' y='%d' width='%d' height='%d' fill='#fff' stroke='%s' stroke-width='2'/>"
         % (x0 + LW, y0, gw, gy - y0, GREEN),
         "<rect x='%d' y='%d' width='%d' height='%d' fill='%s'/>" % (x0 + LW, y0, gw, HEAD, HEADFILL)]
    for p in cols:
        if p != cols[0]:
            o.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='1'/>"
                     % (xs[p], y0, xs[p], gy, GREEN))
        o.append(text(cx[p], y0 + 21, cap(PLACE[p]), 14, col=GREEN))
    o.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='1'/>"
             % (xs[0] + CW + PW, y0, xs[0] + CW + PW, gy, GREEN))
    for yy in (yt, yt + ROW, yb):
        o.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='%d'/>"
                 % (x0 + LW, yy, x0 + LW + gw, yy, GREEN, 2 if yy == yt else 1))
    for p, ch in top.items():
        o.append(text(cx[p], yt + 32, ch, 28, weight=800))
    if show_answer:
        for p, ch in bot.items():
            col = INK if p in moved else GHOST
            if hi_place == p:
                col = RED
            o.append(text(cx[p], yb + 32, ch, 28, col=col, weight=800))
    ptx = xs[0] + CW + PW / 2.0
    if "." in N(x):
        o.append("<circle cx='%.1f' cy='%d' r='4.5' fill='%s'/>" % (ptx, yt + 31, INK))
    if show_answer and "." in r:
        o.append("<circle cx='%.1f' cy='%d' r='4.5' fill='%s'/>" % (ptx, yb + 31, INK))
    y1, y2 = yt + ROW + 5, yb - 5
    for p in top:
        if p + shift not in bot:
            continue
        xa, xb = cx[p], cx[p + shift]
        L = math.hypot(xb - xa, y2 - y1)
        ux, uy = (xb - xa) / L, (y2 - y1) / L
        hx, hy = xb - ux * 11, y2 - uy * 11
        o.append("<line x1='%.1f' y1='%d' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='2.5'/>" % (xa, y1, hx, hy, RED))
        o.append("<polygon points='%.1f,%.1f %.1f,%.1f %.1f,%.1f' fill='%s'/>"
                 % (xb, y2, hx - uy * 5.5, hy + ux * 5.5, hx + uy * 5.5, hy - ux * 5.5, RED))
    o.append(text(x0 + LW - 10, yt + ROW + BAND / 2.0 + 6, "%s %s" % (op, P10(k)), 17, anchor="end", col=GREEN))
    lab = "place value chart: %s %s %s, every digit moves %d place%s to the %s" % (
        N(x), "times" if op == "×" else "divided by", P10(k), k, "" if k == 1 else "s", "left" if op == "×" else "right")
    if show_answer:
        lab += ", giving %s" % r
    return svg_wrap(W, H, "".join(o), lab)


# ------------------------------------------------------------ figure: two steps (× 3 then × 10)
def steps_svg(start, ops, hide_last=True):
    """Boxes joined by arrows: start -> op1 -> v1 -> op2 -> v2. ops = [('×', 3), ('×', 10)].
    The values are computed here; the last box shows ? when hide_last."""
    vals = [Dm(start)]
    for op, n in ops:
        vals.append(vals[-1] * n if op == "×" else vals[-1] / n)
    labs = [N(v) for v in vals]
    if hide_last:
        labs[-1] = "?"
    FS, BH, GAP, PAD = 22, 46, 84, 6
    bws = [max(56, int(tw(t, FS) + 26)) for t in labs]
    W = PAD * 2 + sum(bws) + GAP * len(ops)
    H = 34 + BH + PAD
    o, x = [], PAD
    for i, t in enumerate(labs):
        last = i == len(labs) - 1
        o.append("<rect x='%d' y='34' width='%d' height='%d' rx='8' fill='%s' stroke='%s' stroke-width='2.5'/>"
                 % (x, bws[i], BH, PARTFILL if last else HEADFILL, ORANGE if last else GREEN))
        o.append(text(x + bws[i] / 2.0, 34 + BH / 2.0 + 8, t, FS, col=RED if (last and hide_last) else INK, weight=800))
        x += bws[i]
        if i < len(ops):
            a, b = x + 6, x + GAP - 6
            y = 34 + BH / 2.0
            o.append("<path d='M%d %.1f L%d %.1f M%d %.1f L%d %.1f L%d %.1f' fill='none' stroke='%s' stroke-width='2.5'/>"
                     % (a, y, b, y, b - 8, y - 6, b, y, b - 8, y + 6, GREEN))
            o.append(text((a + b) / 2.0, 24, "%s %s" % (ops[i][0], N(ops[i][1])), 17, col=GREEN))
            x += GAP
    lab = "steps: " + ", then ".join("%s %s" % (op, N(n)) for op, n in ops) + ", starting from %s" % N(start)
    return svg_wrap(W, H, "".join(o), lab)


# ------------------------------------------------------------ figure: weighing scale in kg
def dial_svg(v, mx, lab, tick, size=200):
    """Round scale in kg from 0 to mx: a tick every `tick` kg, a label every `lab` kg. Needle exactly at v."""
    v, mx, lab, tick = Dm(v), Dm(mx), Dm(lab), Dm(tick)
    c = size / 2.0
    R = c - 6

    def pt(val, r):
        a = math.radians(-135 + 270.0 * float(val / mx))
        return c + r * math.sin(a), c - r * math.cos(a)
    s = ["<circle cx='%.1f' cy='%.1f' r='%.1f' fill='#fff' stroke='%s' stroke-width='6'/>" % (c, c, R, GREEN)]
    small, big = [], []
    n = int(mx / tick)
    for i in range(n + 1):
        val = tick * i
        major = (val / lab) == (val / lab).to_integral_value()
        x1, y1 = pt(val, R - (17 if major else 10))
        x2, y2 = pt(val, R - 4)
        (big if major else small).append("M%.1f %.1fL%.1f %.1f" % (x1, y1, x2, y2))
    s.append("<path d='%s' stroke='%s' stroke-width='1.6'/>" % ("".join(small), INK))
    s.append("<path d='%s' stroke='%s' stroke-width='3'/>" % ("".join(big), INK))
    nx, ny = pt(v, R - 9)
    s.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='3.5' stroke-linecap='round'/>"
             % (c, c, nx, ny, RED))
    s.append("<g font-size='17' font-weight='700' fill='%s' text-anchor='middle' stroke='#fff' stroke-width='4' "
             "paint-order='stroke'>" % INK)
    for i in range(int(mx / lab) + 1):
        x, y = pt(lab * i, R - 36)
        s.append("<text x='%.1f' y='%.1f'>%s</text>" % (x, y + 6, N(lab * i)))
    s.append("</g>")
    s.append("<circle cx='%.1f' cy='%.1f' r='7' fill='%s'/>" % (c, c, RED))
    s.append(text(c, c + 62, "kg", 22, col=GREEN, weight=800))
    return svg_wrap(size, size, "".join(s), "weighing scale in kg with the needle at %s kg" % N(v))


# ------------------------------------------------------------ figure: measuring jug in ml
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
            s.append("<text x='%d' y='%.1f'>%s</text>" % (x0 - 7, Y(val) + 5, N(val)))
    s.append("</g>")
    s.append(text(x0 - 7, 202, "ml", 15, anchor="end", col=GREEN))
    return svg_wrap(size, size + 6, "".join(s), "measuring jug with water at %s ml" % N(v))


# ------------------------------------------------------------ figure: number line in one unit
def nline_svg(a, b, minor, unit, point, show_point_label=False, labels=None):
    """Number line from a to b (whole numbers of `unit`), a tick every `minor`. Whole units labelled.
    A red arrow marks `point`."""
    a, b, minor, point = Dm(a), Dm(b), Dm(minor), Dm(point)
    assert a <= point <= b
    L, R = 34, 34
    PX = Dm(560) / (b - a)
    W = int(L + PX * (b - a) + R)
    AY = 46
    H = AY + 40
    X = lambda v: L + float((Dm(v) - a) * PX)
    o = ["<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='2.5'/>" % (L - 12, AY, W - R + 12, AY, INK)]
    n = int((b - a) / minor)
    for i in range(n + 1):
        v = a + minor * i
        big = v == v.to_integral_value() if labels is None else v in [Dm(t) for t in labels]
        x = X(v)
        o.append("<line x1='%.1f' y1='%d' x2='%.1f' y2='%d' stroke='%s' stroke-width='%s'/>"
                 % (x, AY - (11 if big else 7), x, AY + (11 if big else 7), INK if big else THIN, "2.5" if big else "1.5"))
        if big:
            o.append(text(x, AY + 32, "%s %s" % (N(v), unit), 16))
    xp = X(point)
    o.append("<path d='M%.1f %d L%.1f %d' stroke='%s' stroke-width='3'/>" % (xp, 6, xp, AY - 12, RED))
    o.append("<polygon points='%.1f,%d %.1f,%d %.1f,%d' fill='%s'/>" % (xp, AY - 3, xp - 6, AY - 14, xp + 6, AY - 14, RED))
    o.append("<circle cx='%.1f' cy='%d' r='5' fill='%s'/>" % (xp, AY, RED))
    if show_point_label:
        o.append(text(xp + 8, 20, "%s %s" % (N(point), unit), 15, anchor="start", col=RED))
    lab = "number line from %s %s to %s %s with a tick every %s %s, an arrow at %s %s" % (
        N(a), unit, N(b), unit, N(minor), unit, N(point), unit)
    return svg_wrap(W, H, "".join(o), lab)


# ------------------------------------------------------------ figures: bar models
def brace(x1, x2, y, up, lab, col=INK):
    """Bracket from x1 to x2 at y; ticks point to the bar (down if up=True). Label beyond it."""
    d = 7 if up else -7
    o = ["<path d='M%.1f %.1f L%.1f %.1f L%.1f %.1f L%.1f %.1f' fill='none' stroke='%s' stroke-width='2'/>"
         % (x1, y + d, x1, y, x2, y, x2, y + d, col)]
    o.append(text((x1 + x2) / 2.0, y - 7 if up else y + 20, lab, 16, col=col))
    return "".join(o)


def bar_units(n, total_lab, unit_lab, note, BW=560):
    """One bar of n equal units. Bracket above with total_lab; the first unit is shaded with unit_lab inside.
    A note (e.g. '20 units = 2.4 ℓ') is written under the bar."""
    X0, TOP, BH = 10, 34, 38
    uw = BW / float(n)
    assert tw(unit_lab, 16) <= uw - 4, (unit_lab, uw)
    W = X0 * 2 + BW
    H = TOP + BH + 34
    o = [brace(X0, X0 + BW, 22, True, total_lab)]
    o.append("<rect x='%.1f' y='%d' width='%.1f' height='%d' fill='%s'/>" % (X0, TOP, uw, BH, PARTFILL))
    o.append("<rect x='%d' y='%d' width='%d' height='%d' fill='none' stroke='%s' stroke-width='2'/>"
             % (X0, TOP, BW, BH, GREEN))
    for i in range(1, n):
        o.append("<line x1='%.1f' y1='%d' x2='%.1f' y2='%d' stroke='%s' stroke-width='1.5'/>"
                 % (X0 + uw * i, TOP, X0 + uw * i, TOP + BH, GREEN))
    o.append(text(X0 + uw / 2.0, TOP + BH / 2.0 + 6, unit_lab, 16, col=RED if unit_lab == "?" else INK))
    o.append(text(X0, TOP + BH + 24, note, 16, anchor="start", col=GREEN))
    return svg_wrap(W, H, "".join(o), "bar model: %d equal units, total %s, 1 unit %s" % (n, total_lab, unit_lab))


def bar_parts(parts, total_lab, BW=560):
    """One bar split into parts drawn to scale. parts = [(value, label inside)]. Bracket below with total_lab."""
    X0, TOP, BH = 10, 8, 40
    tot = sum(Dm(v) for v, _ in parts)
    W = X0 * 2 + BW
    H = TOP + BH + 36
    o, x = [], float(X0)
    fills = [HEADFILL, PARTFILL, "#fff"]
    for i, (v, lab) in enumerate(parts):
        w = float(Dm(v) / tot) * BW
        assert tw(lab, 16) <= w - 6, (lab, w)
        o.append("<rect x='%.1f' y='%d' width='%.1f' height='%d' fill='%s' stroke='%s' stroke-width='2'/>"
                 % (x, TOP, w, BH, fills[i % 3], GREEN))
        o.append(text(x + w / 2.0, TOP + BH / 2.0 + 6, lab, 16, col=RED if lab == "?" else INK))
        x += w
    o.append(brace(X0, X0 + BW, TOP + BH + 10, False, total_lab, col=RED if total_lab == "?" else INK))
    return svg_wrap(W, H, "".join(o), "bar model: parts %s, whole %s" % (", ".join(l for _, l in parts), total_lab))


def bar_compare(rows, diff_lab, BW=440):
    """Comparison model. rows = [(name, value, label inside)], the first bar is the longer one.
    The shorter bar has a dashed part up to the longer one, with diff_lab inside it."""
    (n1, v1, l1), (n2, v2, l2) = rows
    v1, v2 = Dm(v1), Dm(v2)
    assert v1 > v2
    LW = int(max(tw(n1, 16), tw(n2, 16))) + 16
    X0, TOP, BH, GAP = 6, 8, 38, 16
    x0 = X0 + LW
    W = x0 + BW + 10
    H = TOP + 2 * BH + GAP + 8
    w2 = float(v2 / v1) * BW
    o = []
    for i, (nm, w, lab, fill) in enumerate([(n1, BW, l1, HEADFILL), (n2, w2, l2, PARTFILL)]):
        y = TOP + i * (BH + GAP)
        assert tw(lab, 16) <= w - 6, (lab, w)
        o.append(text(x0 - 10, y + BH / 2.0 + 6, nm, 16, anchor="end"))
        o.append("<rect x='%d' y='%d' width='%.1f' height='%d' fill='%s' stroke='%s' stroke-width='2'/>"
                 % (x0, y, w, BH, fill, GREEN))
        o.append(text(x0 + w / 2.0, y + BH / 2.0 + 6, lab, 16, col=RED if lab == "?" else INK))
    y = TOP + BH + GAP
    dw = BW - w2
    assert tw(diff_lab, 16) <= dw - 6, (diff_lab, dw)
    o.append("<rect x='%.1f' y='%d' width='%.1f' height='%d' fill='none' stroke='%s' stroke-width='2' "
             "stroke-dasharray='6 4'/>" % (x0 + w2, y, dw, BH, ORANGE))
    o.append(text(x0 + w2 + dw / 2.0, y + BH / 2.0 + 6, diff_lab, 16, col=RED if diff_lab == "?" else ORANGE))
    lab = "bar model comparing %s (%s) and %s (%s), difference %s" % (n1, l1, n2, l2, diff_lab)
    return svg_wrap(int(W), H, "".join(o), lab)


# ------------------------------------------------------------ explanations
def moves(k):
    return "1 place" if k == 1 else "%d places" % k


def p10_e(x, op, k, note=""):
    r = calc(x, op, k)
    e = ("%s %s %s: every digit moves <b>%s to the %s</b>. The decimal point stays still."
         % (N(x), op, P10(k), moves(k), "left" if op == "×" else "right"))
    if op == "×" and len(N(x).partition(".")[2]) < k:
        e += " Write 0 in the empty places up to the ones."
    elif op == "÷" and r < 1:
        e += " Write 0 in the empty places, starting with the ones."
    e += " %s %s %s = <b>%s</b>." % (N(x), op, P10(k), N(r))
    if note:
        e += " " + note
    return e


def p10(x, op, k, wrong, note=""):
    return mcq("%s %s %s = ?" % (N(x), op, P10(k)), N(calc(x, op, k)), wrong, p10_e(x, op, k, note),
               want=calc(x, op, k))


def split_mult(m):
    """30 -> (3, 10); 400 -> (4, 100); 2000 -> (2, 1000)."""
    k = 0
    while m % 10 == 0:
        m //= 10
        k += 1
    assert 1 < m < 10 and k >= 1
    return m, 10 ** k


def mult_e(x, op, m, note=""):
    """0.45 × 30 = 0.45 × 3 × 10 = 1.35 × 10 = 13.5."""
    a, p = split_mult(m)
    x = Dm(x)
    mid = x * a if op == "×" else x / a
    r = mid * p if op == "×" else mid / p
    e = ("%s is %d %s %s. So %s %s %s = %s %s %d %s %s. First %s %s %d = %s. Then %s %s %s = <b>%s</b>."
         % (N(m), a, "×", N(p), N(x), op, N(m), N(x), op, a, op, N(p),
            N(x), op, a, N(mid), N(mid), op, N(p), N(r)))
    if note:
        e += " " + note
    return e


def mult(x, op, m, wrong, note=""):
    r = Dm(x) * m if op == "×" else Dm(x) / m
    return mcq("%s %s %s = ?" % (N(x), op, N(m)), N(r), wrong, mult_e(x, op, m, note), want=r)


def conv_r(n, uf, ut):
    n = Dm(str(n))
    if (uf, ut) in FACTOR:
        return n * FACTOR[(uf, ut)]
    return n / FACTOR[(ut, uf)]


def conv_e(n, uf, ut, note=""):
    r = conv_r(n, uf, ut)
    if (uf, ut) in FACTOR:
        k = FACTOR[(uf, ut)]
        e = ("1 %s = %s %s. To change %s to %s, multiply by %s: %s × %s = %s. The digits move %s to the left."
             % (uf, N(k), ut, uf, ut, N(k), N(n), N(k), N(r), moves(len(str(k)) - 1)))
    else:
        k = FACTOR[(ut, uf)]
        e = ("1 %s = %s %s. To change %s to %s, divide by %s: %s ÷ %s = %s. The digits move %s to the right."
             % (ut, N(k), uf, uf, ut, N(k), N(n), N(k), N(r), moves(len(str(k)) - 1)))
    e += " So %s = <b>%s</b>." % (U(n, uf), U(r, ut))
    if note:
        e += " " + note
    return e


def conv(n, uf, ut, wrong, note="", q=None):
    """Convert n uf into ut. wrong = numbers in ut from real mistakes."""
    r = conv_r(n, uf, ut)
    if q is None:
        q = "%s = ? %s" % (U(n, uf), ut)
    fam, sz = UNIT[uf]
    return mcq(q, U(r, ut), [U(w, ut) for w in wrong], conv_e(n, uf, ut, note), want=(fam, Dm(str(n)) * sz))


def big_small(big):
    return {"km": "m", "m": "cm", "kg": "g", "ℓ": "ml"}[big]


def to_dec_e(a, b, big, note=""):
    """3 ℓ 40 ml -> 3.04 ℓ."""
    sm = big_small(big)
    k = FACTOR[(big, sm)]
    f = Dm(b) / k
    e = ("1 %s = %s %s, so %s = %s ÷ %s %s = %s %s. %s = %s %s + %s %s = <b>%s</b>."
         % (big, N(k), sm, U(b, sm), N(b), N(k), big, N(f), big, U(a, big) + " " + U(b, sm),
            N(a), big, N(f), big, U(Dm(a) + f, big)))
    if note:
        e += " " + note
    return e


def to_dec(a, b, big, wrong, note=""):
    sm = big_small(big)
    k = FACTOR[(big, sm)]
    r = Dm(a) + Dm(b) / k
    fam, sz = UNIT[big]
    return mcq("%s %s = ? %s" % (U(a, big), U(b, sm), big), U(r, big), wrong, to_dec_e(a, b, big, note),
               want=(fam, r * sz))


def from_dec_e(x, big, note=""):
    """2.6 ℓ -> 2 ℓ 600 ml."""
    sm = big_small(big)
    k = FACTOR[(big, sm)]
    x = Dm(x)
    w = int(x)
    f = x - w
    e = ("%s = %s %s + %s %s. 1 %s = %s %s, so %s %s = %s × %s %s = %s %s. %s = <b>%s %s</b>."
         % (U(x, big), N(w), big, N(f), big, big, N(k), sm, N(f), big, N(f), N(k), sm, N(f * k), sm,
            U(x, big), U(w, big), U(f * k, sm)))
    if note:
        e += " " + note
    return e


def from_dec(x, big, wrong, note=""):
    sm = big_small(big)
    k = FACTOR[(big, sm)]
    x = Dm(x)
    w = int(x)
    fam, sz = UNIT[big]
    return mcq("%s = ? %s ? %s" % (U(x, big), big, sm), "%s %s" % (U(w, big), U((x - w) * k, sm)), wrong,
               from_dec_e(x, big, note), want=(fam, x * sz))


# ============================================================ set 1: × and ÷ by 10, 100, 1000
def set_p10():
    its = []
    its.append(mcq(fig(pv_move("5.8", "×", 1, show_answer=False)) + "The chart shows 5.8 × 10. What is the answer?",
                   "58", ["5.80", "0.58", "580"],
                   p10_e("5.8", "×", 1, "5.80 is wrong: a zero at the end of a decimal does not change its value."),
                   want=58))
    its.append(mcq(fig(pv_move("9.4", "÷", 1, show_answer=False)) + "The chart shows 9.4 ÷ 10. What is the answer?",
                   "0.94", ["94", "0.094", "9.04"],
                   p10_e("9.4", "÷", 1, "94 moves the digits the wrong way: dividing by 10 makes the number smaller."),
                   want="0.94"))
    its.append(p10("0.67", "×", 2, ["0.6700", "6.7", "670"], "0.6700 only adds zeros, so it is still 0.67."))
    its.append(p10("35.2", "÷", 2, ["3520", "3.52", "0.0352"], "3520 moves the digits the wrong way."))
    assert calc("3.14", "×", 1) == Dm("31.4")
    its.append(mcq(fig(pv_move("3.14", "×", 1)) + "Which calculation does the chart show?",
                   "3.14 × 10", ["3.14 ÷ 10", "3.14 × 100", "3.14 ÷ 100"],
                   "Every digit moved <b>1 place to the left</b>, so the number was multiplied by 10. "
                   "<b>3.14 × 10</b> = 31.4.", same_ok=True))
    assert calc("52.6", "÷", 2) == Dm("0.526")
    its.append(mcq(fig(pv_move("52.6", "÷", 2)) + "Which calculation does the chart show?",
                   "52.6 ÷ 100", ["52.6 × 100", "52.6 ÷ 10", "52.6 ÷ 1000"],
                   "Every digit moved <b>2 places to the right</b>, so the number was divided by 100. "
                   "<b>52.6 ÷ 100</b> = 0.526.", same_ok=True))
    its.append(p10("0.3", "÷", 1, ["3", "0.003", "0.30"], "0.30 only adds a zero, so it is still 0.3."))
    its.append(p10("4.08", "×", 2, ["48", "40.8", "4080"], "Keep the 0 that holds the tens place: 408, not 48."))
    its.append(p10("2.5", "×", 3, ["250", "25" + NB + "000", "2.5000"], "250 moves the digits only 2 places."))
    its.append(p10("76", "÷", 3, ["0.76", "7.6", "76" + NB + "000"], "0.76 moves the digits only 2 places."))
    assert calc("0.059", "×", 2) == Dm("5.9")
    its.append(mcq(fig(pv_move("0.059", "×", 2, hi=-3)) +
                   "The chart shows 0.059 × 100 = 5.9. What is the value of the red digit in the answer?",
                   "9 tenths", ["9 thousandths", "9 hundredths", "9 ones"],
                   "The 9 was in the thousandths place. Every digit moved 2 places to the left, so the 9 is now in the "
                   "<b>tenths</b> place. Its value is <b>9 tenths</b> = 0.9.", same_ok=True))
    assert calc("6.43", "÷", 1) == Dm("0.643")
    its.append(mcq(fig(pv_move("6.43", "÷", 1, hi=-2)) +
                   "The chart shows 6.43 ÷ 10 = 0.643. What is the value of the red digit in the answer?",
                   "3 thousandths", ["3 hundredths", "3 tenths", "3 ones"],
                   "The 3 was in the hundredths place. Every digit moved 1 place to the right, so the 3 is now in the "
                   "<b>thousandths</b> place. Its value is <b>3 thousandths</b> = 0.003.", same_ok=True))
    its.append(p10("13.07", "×", 1, ["13.070", "1307", "130.07"],
                   "130.07 only multiplies the whole-number part. Every digit must move, including the 7."))
    its.append(p10("980", "÷", 2, ["98", "0.98", "98" + NB + "000"],
                   "98 moves the digits only 1 place. The last 0 is not needed after the point: 9.80 = 9.8."))
    assert calc("0.72", "÷", 3) == Dm("0.00072")
    its.append(mcq("In <b>0.72 ÷ 1000</b>, how do the digits move?", "3 places to the right",
                   ["3 places to the left", "2 places to the right", "1 place to the right"],
                   "1000 has 3 zeros, so every digit moves <b>3 places</b>. Dividing makes the number smaller, so they "
                   "move to the <b>right</b>.", same_ok=True))
    its.append(p10("0.009", "×", 3, ["0.9", "90", "9000"], "0.9 moves the digit only 2 places."))
    assert Dm("0.8") * 100 == 80
    its.append(mcq("0.8 × ? = 80", "100", ["10", "1000", "79.2"],
                   "The 8 moves from the tenths to the tens: that is 2 places to the left, so the missing number is "
                   "<b>100</b>. 79.2 is 80 − 0.8, which is subtraction, not multiplication.", want=100))
    assert Dm("4.5") / 1000 == Dm("0.0045")
    its.append(mcq("4.5 ÷ ? = 0.0045", "1000", ["100", "10", "10" + NB + "000"],
                   "The 4 moves from the ones to the thousandths: 3 places to the right. So the missing number is "
                   "<b>1000</b>.", want=1000))
    assert Dm("0.062") * 1000 == 62
    its.append(mcq("? × 1000 = 62", "0.062", ["0.62", "62" + NB + "000", "6.2"],
                   "Use the inverse: 62 ÷ 1000 = <b>0.062</b>. Check: 0.062 × 1000 = 62. "
                   "62" + NB + "000 multiplies instead of dividing.", want="0.062"))
    its.append(p10("72.5", "×", 3, ["7250", "725" + NB + "000", "72.5000"],
                   "7250 moves the digits only 2 places. 72" + NB + "500 has 5 digits, so it is written with a space."))
    order = [0, 1, 2, 3, 4, 5, 6, 7, 14, 8, 9, 10, 11, 12, 13, 15, 16, 17, 18, 19]
    return {"title": "× and ÷ by 10, 100 and 1000", "items": [its[i] for i in order]}


# ============================================================ set 2: × and ÷ by multiples of 10, 100, 1000
def set_mult():
    its = []
    assert Dm("0.45") * 30 == Dm("13.5")
    its.append(mcq(fig(steps_svg("0.45", [("×", 3), ("×", 10)])) +
                   "The steps show 0.45 × 30. What is 0.45 × 30?", "13.5", ["1.35", "135", "0.135"],
                   mult_e("0.45", "×", 30, "1.35 forgets the × 10 step."), want="13.5"))
    assert Dm("8.4") / 20 == Dm("0.42")
    its.append(mcq(fig(steps_svg("8.4", [("÷", 2), ("÷", 10)])) +
                   "The steps show 8.4 ÷ 20. What is 8.4 ÷ 20?", "0.42", ["4.2", "0.042", "168"],
                   mult_e("8.4", "÷", 20, "4.2 forgets the ÷ 10 step. 168 multiplies instead of dividing."),
                   want="0.42"))
    its.append(mult("0.3", "×", 20, ["0.6", "60", "20.3"], "0.6 forgets the × 10 step. 20.3 adds instead of multiplying."))
    its.append(mult("2.4", "×", 30, ["7.2", "720", "60.12"],
                    "60.12 writes 2 × 30 = 60 and 0.4 × 30 = 12 side by side instead of adding: 60 + 12 = 72."))
    its.append(mult("6.3", "÷", 30, ["2.1", "0.021", "189"], "2.1 forgets the ÷ 10 step."))
    its.append(mult("4.8", "÷", 40, ["1.2", "0.012", "192"], "1.2 forgets the ÷ 10 step. 192 multiplies."))
    its.append(mult("0.6", "×", 400, ["24", "2400", "2.4"], "24 multiplies by 40 instead of 400."))
    its.append(mult("1.25", "×", 40, ["5", "500", "0.5"], "5 forgets the × 10 step."))
    its.append(mult("0.08", "×", 50, ["0.4", "40", "0.04"], "0.4 forgets the × 10 step."))
    its.append(mult("5.6", "÷", 70, ["0.8", "0.008", "392"], "0.8 forgets the ÷ 10 step."))
    its.append(mult("36", "÷", 400, ["0.9", "9", "0.009"], "0.9 divides by 40 instead of 400. 9 forgets the ÷ 100 step."))
    its.append(mult("3.2", "×", 2000, ["640", "64" + NB + "000", "6.4"],
                    "640 multiplies by 200 instead of 2000. 6.4 forgets the × 1000 step."))
    its.append(mult("0.123", "×", 300, ["3.69", "369", "0.369"], "0.369 forgets the × 100 step."))
    its.append(mult("2.7", "÷", 900, ["0.03", "0.0003", "0.3"], "0.3 forgets the ÷ 100 step."))
    assert Dm("7.2") / 800 == Dm("0.009")
    its.append(mcq(fig(steps_svg("7.2", [("÷", 8), ("÷", 100)])) +
                   "The steps show 7.2 ÷ 800. What is 7.2 ÷ 800?", "0.009", ["0.09", "0.9", "0.0009"],
                   mult_e("7.2", "÷", 800, "0.09 moves the digit only 1 place in the ÷ 100 step."), want="0.009"))
    assert Dm("0.7") * 60 == Dm("0.7") * 6 * 10 == 42
    its.append(mcq("Which gives the same answer as <b>0.7 × 60</b>?", "0.7 × 6 × 10",
                   ["0.7 × 6 + 10", "0.7 × 6 ÷ 10", "0.7 × 600"],
                   "60 = 6 × 10, so 0.7 × 60 = <b>0.7 × 6 × 10</b> = 4.2 × 10 = 42.", same_ok=True))
    assert Dm("0.7") * 30 == 21
    its.append(mcq("0.7 × ? = 21", "30", ["3", "300", "20.3"],
                   "0.7 × 3 = 2.1, and 2.1 × 10 = 21. So 0.7 × 30 = 21. The missing number is <b>30</b>. "
                   "20.3 is 21 − 0.7, which is subtraction.", want=30))
    assert Dm("2.4") / 40 == Dm("0.06")
    its.append(mcq("? ÷ 40 = 0.06", "2.4", ["0.24", "24", "0.0015"],
                   "Use the inverse: 0.06 × 40 = 0.06 × 4 × 10 = 0.24 × 10 = <b>2.4</b>. Check: 2.4 ÷ 40 = 0.06. "
                   "0.0015 divides instead of multiplying.", want="2.4"))
    assert Dm("0.25") * 80 == 20
    its.append(mcq("Jun Jie says 0.25 × 80 = 2. What is the correct answer?", "20", ["2", "200", "80.25"],
                   mult_e("0.25", "×", 80, "Jun Jie forgot the × 10 step."), want=20))
    assert Dm("9.6") / 30 == Dm("0.32")
    its.append(mcq("Mei Ling says 9.6 ÷ 30 = 3.2. What is the correct answer?", "0.32", ["3.2", "0.032", "288"],
                   mult_e("9.6", "÷", 30, "Mei Ling forgot the ÷ 10 step. Check: 0.32 × 30 = 9.6."), want="0.32"))
    order = [0, 1, 2, 3, 4, 5, 8, 7, 6, 9, 10, 15, 11, 12, 13, 14, 16, 17, 18, 19]
    return {"title": "× and ÷ by multiples of 10, 100 and 1000", "items": [its[i] for i in order]}


# ============================================================ set 3: converting units in decimal form
def set_convert():
    its = []
    its.append(conv("2.35", "km", "m", ["235", "23" + NB + "500", "0.00235"],
                    "235 m uses 1 km = 100 m, which is wrong."))
    its.append(conv("4.5", "m", "cm", ["45", "4500", "0.045"], "45 cm uses 1 m = 10 cm, which is wrong."))
    its.append(conv("450", "g", "kg", ["4.5", "0.045", "45"], "4.5 kg divides by 100 instead of 1000."))
    its.append(conv("1.2", "ℓ", "ml", ["120", "12", "12" + NB + "000"], "120 ml multiplies by 100 instead of 1000."))
    its.append(conv("750", "ml", "ℓ", ["7.5", "0.075", "75"], "750 ml is less than 1 ℓ, so the answer must be less than 1."))
    its.append(conv("86", "cm", "m", ["8.6", "0.086", "8600"],
                    "8.6 m uses 1 m = 10 cm. 8600 m moves the digits the wrong way."))
    its.append(conv("0.6", "km", "m", ["60", "6", "6000"], "60 m multiplies by 100 instead of 1000."))
    its.append(conv("3.08", "kg", "g", ["308", "3800", "30" + NB + "800"],
                    "3800 g drops the 0 that holds the tenths place: 3.08 is not 3.8."))
    its.append(conv("2050", "m", "km", ["2.5", "20.5", "205"],
                    "2.5 km drops the 0 that holds the tenths place: 2.5 km is 2500 m."))
    its.append(conv("5", "cm", "m", ["0.5", "0.005", "500"], "0.5 m uses 1 m = 10 cm: 0.5 m is 50 cm."))
    its.append(conv("0.025", "ℓ", "ml", ["2.5", "250", "0.25"], "250 ml reads 0.025 as 0.25."))
    its.append(conv("40", "g", "kg", ["0.4", "0.004", "4"], "0.4 kg divides by 100 instead of 1000: 0.4 kg is 400 g."))
    its.append(conv("0.75", "m", "cm", ["7.5", "750", "0.0075"], "7.5 cm uses 1 m = 10 cm."))
    its.append(conv("12500", "ml", "ℓ", ["125", "1.25", "1250"], "125 ℓ divides by 100 instead of 1000."))
    assert conv_r("1.4", "kg", "g") == 1400
    its.append(mcq(fig(dial_svg("1.4", "2", "0.5", "0.1")) + "What is the mass shown on the scale, in grams?",
                   "1400 g", ["140 g", "14" + NB + "000 g", "1040 g"],
                   "The needle is 4 small marks past 1 kg. Each small mark is 0.1 kg, so the mass is 1.4 kg. "
                   + conv_e("1.4", "kg", "g", "1040 g is 1 kg 40 g, not 1 kg 400 g."), want=("M", 1400)))
    assert conv_r("600", "ml", "ℓ") == Dm("0.6")
    its.append(mcq(fig(jug_svg(600, 1000, 200, 100)) + "How much water is in the jug, in litres?",
                   "0.6 ℓ", ["6 ℓ", "0.06 ℓ", "60 ℓ"],
                   "The water is at 600 ml. " + conv_e("600", "ml", "ℓ", "6 ℓ divides by 100 instead of 1000."),
                   want=("C", 600)))
    assert conv_r("2.4", "km", "m") == 2400
    its.append(mcq(fig(nline_svg(0, 3, "0.1", "km", "2.4")) +
                   "Each small mark is 0.1 km. How far from 0 is the arrow, in metres?",
                   "2400 m", ["240 m", "24" + NB + "000 m", "2040 m"],
                   "The arrow is 4 small marks past 2 km, so it is at 2.4 km. "
                   + conv_e("2.4", "km", "m", "2040 m is 2 km 40 m, not 2 km 400 m."), want=("L", 240000)))
    its.append(mcq("Which mass is equal to <b>0.8 kg</b>?", "800 g", ["80 g", "8 g", "8000 g"],
                   conv_e("0.8", "kg", "g", "80 g multiplies by 100 instead of 1000."), want=("M", 800)))
    its.append(mcq("Which length is equal to <b>307 cm</b>?", "3.07 m", ["3.7 m", "30.7 m", "0.307 m"],
                   conv_e("307", "cm", "m", "3.7 m drops the 0 that holds the tenths place: 3.7 m is 370 cm."),
                   want=("L", 307)))
    its.append(mcq("Which mass is the <b>heaviest</b>?", "0.9 kg", ["850 g", "0.09 kg", "899 g"],
                   "Change them all to grams: 0.9 kg = 900 g and 0.09 kg = 90 g. "
                   "900 g is more than 899 g, 850 g and 90 g, so <b>0.9 kg</b> is the heaviest.",
                   want=("M", 900)))
    order = [0, 1, 2, 3, 4, 6, 9, 11, 5, 12, 17, 14, 15, 7, 8, 10, 13, 16, 18, 19]
    return {"title": "Converting units in decimal form", "items": [its[i] for i in order]}


# ============================================================ set 4: compound units and decimals
def set_compound():
    its = []
    its.append(to_dec(3, 40, "ℓ", ["3.4 ℓ", "3.004 ℓ", "3040 ℓ"],
                      "3.4 ℓ is a common mistake: 0.4 ℓ is 400 ml, not 40 ml."))
    its.append(to_dec(2, 35, "m", ["2.035 m", "23.5 m", "235 m"],
                      "2.035 m uses 1 m = 1000 cm, which is wrong."))
    its.append(to_dec(5, 600, "kg", ["5.06 kg", "5.006 kg", "56 kg"], "5.06 kg is 5 kg 60 g."))
    its.append(to_dec(4, 250, "km", ["4.025 km", "42.5 km", "4250 km"], "4.025 km is 4 km 25 m."))
    its.append(to_dec(1, 5, "kg", ["1.5 kg", "1.05 kg", "1005 kg"],
                      "1.5 kg is 1 kg 500 g, and 1.05 kg is 1 kg 50 g. 5 g is 5 thousandths of a kilogram."))
    its.append(to_dec(7, 8, "m", ["7.8 m", "7.008 m", "78 m"], "7.8 m is 7 m 80 cm."))
    its.append(from_dec("2.6", "ℓ", ["2 ℓ 60 ml", "2 ℓ 6 ml", "26 ℓ"],
                        "2 ℓ 6 ml is a common mistake: the 6 is 6 tenths of a litre, which is 600 ml."))
    its.append(from_dec("1.8", "km", ["1 km 80 m", "1 km 8 m", "18 km"], "1 km 80 m uses 1 km = 100 m."))
    its.append(from_dec("3.45", "kg", ["3 kg 45 g", "345 g", "3450 kg"],
                        "3 kg 45 g treats the digits after the point as grams: 0.45 kg is 450 g, not 45 g."))
    its.append(from_dec("5.07", "m", ["5 m 70 cm", "50 m 7 cm", "507 m"], "5 m 70 cm is 5.7 m, not 5.07 m."))
    its.append(to_dec(6, 5, "ℓ", ["6.5 ℓ", "6.05 ℓ", "65 ℓ"],
                      "6.05 ℓ is 6 ℓ 50 ml. Two zeros hold the tenths and hundredths places."))
    its.append(to_dec(9, 75, "kg", ["9.75 kg", "97.5 kg", "9075 kg"], "9.75 kg is 9 kg 750 g."))
    assert 3 * 100 + 6 == 306
    its.append(mcq("3 m 6 cm = ? cm", "306 cm", ["360 cm", "36 cm", "3006 cm"],
                   "1 m = 100 cm, so 3 m = 300 cm. 300 cm + 6 cm = <b>306 cm</b>. "
                   "360 cm is 3 m 60 cm. 36 cm uses 1 m = 10 cm.", want=("L", 306)))
    assert 2 * 1000 + 40 == 2040
    its.append(mcq("2 km 40 m = ? m", "2040 m", ["2400 m", "240 m", "2004 m"],
                   "1 km = 1000 m, so 2 km = 2000 m. 2000 m + 40 m = <b>2040 m</b>. "
                   "2400 m is 2 km 400 m. 240 m uses 1 km = 100 m.", want=("L", 204000)))
    its.append(mcq(fig(nline_svg(2, 3, "0.1", "m", "2.7")) +
                   "Each small mark is 10 cm. What length does the arrow show, in metres?",
                   "2.7 m", ["2.07 m", "2.007 m", "27 m"],
                   "The arrow is 7 small marks past 2 m, so it shows 2 m 70 cm. "
                   + to_dec_e(2, 70, "m", "2.07 m is 2 m 7 cm."), want=("L", 270)))
    its.append(mcq(fig(dial_svg("2.3", "4", "1", "0.1")) +
                   "Each small mark is 0.1 kg. What mass does the scale show?",
                   "2 kg 300 g", ["2 kg 30 g", "2 kg 3 g", "230 g"],
                   "The needle is 3 small marks past 2 kg, so it shows 2.3 kg. "
                   + from_dec_e("2.3", "kg", "2 kg 30 g is 2.03 kg."), want=("M", 2300)))
    its.append(mcq("Which mass is equal to <b>4.06 kg</b>?", "4 kg 60 g", ["4 kg 600 g", "4 kg 6 g", "406 g"],
                   from_dec_e("4.06", "kg", "4 kg 600 g is 4.6 kg. 406 g multiplies by 100 instead of 1000."),
                   want=("M", 4060)))
    its.append(mcq("Which is the <b>longest</b>?", "255 cm", ["2.5 m", "2 m 45 cm", "2.05 m"],
                   "Change them all to centimetres: 2.5 m = 250 cm, 2 m 45 cm = 245 cm, 2.05 m = 205 cm. "
                   "So <b>255 cm</b> is the longest.", want=("L", 255)))
    its.append(mcq("Siti says 6 m 5 cm = 6.5 m. What is the correct answer?", "6.05 m", ["6.5 m", "6.005 m", "65 m"],
                   to_dec_e(6, 5, "m", "6.5 m is 6 m 50 cm, so Siti is wrong."), want=("L", 605)))
    assert Dm("1.2") + Dm("0.35") == Dm("1.55")
    its.append(mcq("1.2 kg + 350 g = ? kg", "1.55 kg", ["4.7 kg", "351.2 kg", "15.5 kg"],
                   "Change 350 g to kilograms first: 350 ÷ 1000 = 0.35 kg. 1.2 kg + 0.35 kg = <b>1.55 kg</b>. "
                   "4.7 kg uses 1 kg = 100 g. 351.2 kg adds numbers with different units. 15.5 kg puts the point in the wrong place.", want=("M", 1550)))
    order = [0, 1, 2, 3, 5, 4, 10, 11, 6, 7, 8, 9, 12, 13, 14, 15, 16, 18, 17, 19]
    return {"title": "Compound units and decimals", "items": [its[i] for i in order]}


# ============================================================ set 5: word problems with bar models
def set_problems():
    its = []
    # 0
    T = Dm("2.5") * 10
    assert T == 25
    its.append(mcq("A packet of rice has a mass of 2.5 kg. Mrs Lim buys 10 packets for a food donation drive. "
                   "What is the total mass of the rice?", U(T, "kg"), ["250 kg", "12.5 kg", "2.50 kg"],
                   "2.5 × 10: every digit moves 1 place to the left. 2.5 × 10 = <b>25 kg</b>. "
                   "12.5 kg adds 10 instead of multiplying. 2.50 kg only adds a zero.", want=("M", 25000)))
    # 1
    its.append(mcq("Wei Ming’s school is 1.35 km from his HDB flat. How far is that in metres?",
                   "1350 m", ["135 m", "13" + NB + "500 m", "1035 m"],
                   conv_e("1.35", "km", "m", "1035 m is 1 km 35 m."), want=("L", 135000)))
    # 2
    T = Dm("0.4") * 8
    assert T == Dm("3.2")
    its.append(mcq("One lap of the school field is 400 m. Hafiz runs 8 laps on Sports Day. How far does he run, in kilometres?",
                   "3.2 km", ["32 km", "0.32 km", "3200 km"],
                   "400 m × 8 = 3200 m. 3200 ÷ 1000 = <b>3.2 km</b>. 32 km divides by 100 instead of 1000.",
                   want=("L", 320000)))
    # 3
    T = Dm("4.50") * 30
    assert T == 135
    its.append(mcq("A plate of chicken rice at a hawker centre costs $4.50. Mr Tan buys 30 plates for a staff lunch. "
                   "How much does he pay?", M(T), ["$13.50", "$1350", "$120"],
                   "30 = 3 × 10. $4.50 × 3 = $13.50. Then $13.50 × 10 = <b>$135</b>. "
                   "$13.50 forgets the × 10 step. $120 multiplies only the $4.",
                   want=("$", 135)))
    # 4  bar model: 20 equal units
    T = Dm("2.4") / 20
    assert T == Dm("0.12") and T * 1000 == 120
    its.append(mcq(fig(bar_units(20, "2.4 ℓ", "?", "20 units = 2.4 ℓ")) +
                   "A jug holds 2.4 ℓ of lime juice. It is poured equally into 20 cups for a class party. "
                   "How much juice is in each cup, in millilitres?", "120 ml", ["12 ml", "1200 ml", "0.12 ml"],
                   "20 units = 2.4 ℓ, so 1 unit = 2.4 ℓ ÷ 20 = 0.12 ℓ. 0.12 × 1000 = <b>120 ml</b>. "
                   "0.12 ml forgets to change litres to millilitres. 1200 ml divides by 2 instead of 20.",
                   want=("C", 120)))
    # 5
    T = Dm("18.5") / 100
    assert T == Dm("0.185")
    its.append(mcq("A stack of 100 exercise books has a mass of 18.5 kg. What is the mass of 1 exercise book, in grams?",
                   "185 g", ["18.5 g", "1850 g", "0.185 g"],
                   "18.5 ÷ 100 = 0.185 kg. 0.185 × 1000 = <b>185 g</b>. 0.185 g forgets to change kg to g. "
                   "1850 g divides by 10 instead of 100.", want=("M", 185)))
    # 6  bar model comparison
    T = Dm("2.45") - Dm("0.8")
    assert T == Dm("1.65")
    its.append(mcq(fig(bar_compare([("Red", 245, "2.45 m"), ("Blue", 165, "?")], "80 cm")) +
                   "A red ribbon is 2.45 m long. A blue ribbon is 80 cm shorter. How long is the blue ribbon, in metres?",
                   "1.65 m", ["2.37 m", "3.25 m", "165 m"],
                   "80 cm = 0.8 m. 2.45 m − 0.8 m = <b>1.65 m</b>. 2.37 m uses 80 cm = 0.08 m. "
                   "3.25 m adds instead of subtracting.", want=("L", 165)))
    # 7
    T = Dm("0.35") * 40
    assert T == 14
    its.append(mcq("A jar of kaya has a mass of 0.35 kg. The school canteen buys 40 jars. What is the total mass?",
                   "14 kg", ["1.4 kg", "140 kg", "12 kg"],
                   mult_e("0.35", "×", 40, "The total mass is 14 kg. 12 kg uses 0.3 instead of 0.35."),
                   want=("M", 14000)))
    # 8  bar model: 10 units
    T = Dm("1.75") * 10
    assert T == Dm("17.5")
    its.append(mcq(fig(bar_units(10, "?", "1.75", "1 unit = 1 kg 750 g = 1.75 kg")) +
                   "Each durian has a mass of 1 kg 750 g. Mr Rahman buys 10 durians of the same mass. "
                   "What is the total mass, in kilograms?", "17.5 kg", ["10.75 kg", "175 kg", "1.75 kg"],
                   "1 kg 750 g = 1.75 kg. 10 units = 1.75 kg × 10 = <b>17.5 kg</b>. "
                   "10.75 kg uses 1 kg 750 g = 1.075 kg. 1.75 kg is the mass of one durian.", want=("M", 17500)))
    # 9  bar model: two parts
    T = Dm("2.4") + Dm("0.65")
    assert T == Dm("3.05")
    its.append(mcq(fig(bar_parts([(2400, "2.4 km"), (650, "650 m")], "?")) +
                   "Ali cycles 2.4 km at East Coast Park. Then he cycles another 650 m. How far does he cycle in all, in kilometres?",
                   "3.05 km", ["8.9 km", "652.4 km", "3.5 km"],
                   "650 m = 0.65 km. 2.4 km + 0.65 km = <b>3.05 km</b>. 3.5 km drops the 0 in the tenths place. "
                   "8.9 km uses 650 m = 6.5 km. 652.4 km adds numbers with different units.", want=("L", 305000)))
    # 10
    T = Dm("0.6") * 30
    assert T == 18
    its.append(mcq("A tap lets out 0.6 ℓ of water every minute. How much water does it let out in 30 minutes?",
                   "18 ℓ", ["1.8 ℓ", "180 ℓ", "30.6 ℓ"],
                   mult_e("0.6", "×", 30, "It lets out 18 ℓ. 30.6 ℓ adds instead of multiplying."), want=("C", 18000)))
    # 11
    T = Dm(72) / 800
    assert T == Dm("0.09")
    its.append(mcq("Mrs Ng pays $72 for 800 red packets for Chinese New Year at his office. All the red packets cost the same. "
                   "How much does 1 red packet cost?", M(T), ["$0.90", "$0.72", "$9"],
                   mult_e("72", "÷", 800, "So 1 red packet costs <b>$0.09</b> (9¢). $0.90 divides by 80 instead of 800. "
                          "$0.72 divides by 100 only.").replace("<b>0.09</b>", "0.09"), want=("$", "0.09")))
    # 12  bar model comparison
    T = 1250 - 950
    assert T == 300
    its.append(mcq(fig(bar_compare([("Xin Yi", 1250, "1.25 ℓ"), ("Zhi Hao", 950, "950 ml")], "?")) +
                   "Xin Yi drinks 1.25 ℓ of water in a day. Zhi Hao drinks 950 ml. How much more water does Xin Yi drink, "
                   "in millilitres?", "300 ml", ["825 ml", "0.3 ml", "948.75 ml"],
                   "1.25 ℓ = 1250 ml. 1250 ml − 950 ml = <b>300 ml</b>. 825 ml uses 1.25 ℓ = 125 ml. "
                   "948.75 ml subtracts numbers with different units.", want=("C", 300)))
    # 13
    T = Dm("5.6") / 70
    assert T == Dm("0.08")
    its.append(mcq("A rope 5.6 m long is cut into 70 equal pieces for a CCA craft session. How long is each piece, in centimetres?",
                   "8 cm", ["80 cm", "0.8 cm", "0.08 cm"],
                   mult_e("5.6", "÷", 70, "Each piece is 0.08 m. 0.08 × 100 = <b>8 cm</b>. "
                          "80 cm forgets the ÷ 10 step. 0.08 cm forgets to change m to cm.").replace("<b>0.08</b>", "0.08"),
                   want=("L", 8)))
    # 14  bar model: used and left
    used = 20 * 12
    left = Dm(3) - Dm(used) / 100
    assert used == 240 and left == Dm("0.6")
    its.append(mcq(fig(bar_parts([(240, "used: 20 × 12 cm"), (60, "?")], "3 m")) +
                   "Chloe has a ribbon 3 m long. She cuts 20 pieces, each 12 cm long, to make bookmarks. "
                   "How much ribbon is left, in metres?", "0.6 m", ["2.4 m", "2.88 m", "0.06 m"],
                   "Used: 20 × 12 cm = 240 cm = 2.4 m. Left: 3 m − 2.4 m = <b>0.6 m</b>. "
                   "2.4 m is the ribbon used, not left. 2.88 m takes away only 1 piece (12 cm). 0.06 m is 6 cm.",
                   want=("L", 60)))
    # 15
    T = Dm("0.45") * 1000
    assert T == 450
    its.append(mcq("For a recycling drive, 1000 students each bring 0.45 kg of old newspapers. What is the total mass?",
                   "450 kg", ["45 kg", "4500 kg", "1000.45 kg"],
                   "0.45 × 1000: every digit moves 3 places to the left. 0.45 × 1000 = <b>450 kg</b>. "
                   "45 kg moves the digits only 2 places. 1000.45 kg adds.", want=("M", 450000)))
    # 16
    T = Dm("0.75") * 2 * 20
    assert T == 30
    its.append(mcq("Raju walks 0.75 km from his flat to the MRT station every morning, and walks back home in the evening. "
                   "How far does he walk on these trips in 20 days?", "30 km", ["15 km", "3 km", "300 km"],
                   "Each day: 0.75 km × 2 = 1.5 km. In 20 days: 1.5 × 20 = 1.5 × 2 × 10 = 3 × 10 = <b>30 km</b>. "
                   "15 km forgets the walk back.", want=("L", 3000000)))
    # 17  two steps, mixed units
    T = Dm("1.5") * 3 + Dm("0.33") * 4
    assert T == Dm("5.82")
    its.append(mcq("For a picnic at the Botanic Gardens, Ethan buys 3 bottles of water of 1.5 ℓ each and 4 cans of juice "
                   "of 330 ml each. How much drink does he buy in all, in litres?", "5.82 ℓ",
                   ["17.7 ℓ", "4.83 ℓ", "1324.5 ℓ"],
                   "Water: 1.5 ℓ × 3 = 4.5 ℓ. Juice: 330 ml × 4 = 1320 ml = 1.32 ℓ. Total: 4.5 ℓ + 1.32 ℓ = <b>5.82 ℓ</b>. "
                   "17.7 ℓ uses 1 ℓ = 100 ml. 4.83 ℓ adds just one can.", want=("C", 5820)))
    # 18 bar model: units, missing unit value
    T = Dm("8.4") / 30
    assert T == Dm("0.28") and T * 1000 == 280
    its.append(mcq("Mdm Wong packs 8.4 kg of rambutans equally into 30 bags. What is the mass of each bag, in grams?",
                   "280 g", ["28 g", "2800 g", "0.28 g"],
                   mult_e("8.4", "÷", 30, "Each bag is 0.28 kg. 0.28 × 1000 = <b>280 g</b>. "
                          "2800 g forgets the ÷ 10 step. 0.28 g forgets to change kg to g.").replace("<b>0.28</b>", "0.28"), want=("M", 280)))
    # 19  bar model, two steps
    tot = Dm("1.5")
    drunk = Dm("0.35")
    T = tot - drunk
    assert T == Dm("1.15")
    its.append(mcq(fig(bar_parts([(1150, "?"), (350, "350 ml")], "1.5 ℓ")) +
                   "Priya has a 1.5 ℓ bottle of soya bean milk. She pours out 350 ml for her brother. "
                   "How much soya bean milk is left, in litres?", "1.15 ℓ", ["1.85 ℓ", "1.465 ℓ", "1150 ℓ"],
                   "350 ml = 0.35 ℓ. 1.5 ℓ − 0.35 ℓ = <b>1.15 ℓ</b>. 1.85 ℓ adds instead of subtracting. "
                   "1.465 ℓ uses 350 ml = 0.035 ℓ. 1150 ℓ forgets to change 1150 ml back to litres.", want=("C", 1150)))
    order = [0, 1, 2, 3, 5, 15, 4, 7, 10, 13, 8, 9, 6, 11, 12, 18, 14, 16, 17, 19]
    return {"title": "Word problems with bar models", "items": [its[i] for i in order]}


# ============================================================ lesson
def body_html():
    f1 = pv_move("2.35", "×", 3)
    f2 = steps_svg("0.45", [("×", 3), ("×", 10)], hide_last=False)
    f3 = nline_svg(3, "3.1", "0.01", "ℓ", "3.04", show_point_label=True, labels=["3", "3.1"])
    f4 = bar_parts([(1150, "?"), (350, "350 ml")], "1.5 ℓ")
    return (
        "<h2>Move the digits, not the decimal point</h2>"
        "<p>When you multiply by 10, 100 or 1000, every digit moves 1, 2 or 3 places to the <b>left</b>. "
        "When you divide, every digit moves to the <b>right</b>. The number of zeros tells you how many places.</p>"
        "<figure class='sn-fig'>" + f1 +
        "<figcaption>2.35 × 1000: every digit moves 3 places to the left. Write 0 in the empty ones place. "
        "2.35 × 1000 = 2350.</figcaption></figure>"
        "<h2>× and ÷ by multiples of 10, 100 and 1000</h2>"
        "<p>Split the multiple: 30 = 3 × 10, 400 = 4 × 100. Multiply or divide by the single digit first, "
        "then by 10, 100 or 1000.</p>"
        "<figure class='sn-fig'>" + f2 +
        "<figcaption>0.45 × 30 = 0.45 × 3 × 10 = 1.35 × 10 = 13.5.</figcaption></figure>"
        + ex("Example 1", "8.4 ÷ 20", "20 = 2 × 10. 8.4 ÷ 2 = 4.2. Then 4.2 ÷ 10 = 0.42.", "0.42")
        + "<h2>Converting units</h2>"
        "<p>Learn the four facts. To change a big unit to a small unit, multiply. "
        "To change a small unit to a big unit, divide.</p>"
        + table(["Fact", "Big → small (×)", "Small → big (÷)"], [
            ["1 km = 1000 m", "2.35 km = 2350 m", "450 m = 0.45 km"],
            ["1 m = 100 cm", "1.6 m = 160 cm", "85 cm = 0.85 m"],
            ["1 kg = 1000 g", "0.3 kg = 300 g", "450 g = 0.45 kg"],
            ["1 ℓ = 1000 ml", "1.25 ℓ = 1250 ml", "60 ml = 0.06 ℓ"],
        ])
        + "<h2>Compound units as decimals</h2>"
        "<p>Change the small unit to a decimal of the big unit, then add the whole number.</p>"
        "<figure class='sn-fig'>" + f3 +
        "<figcaption>Each small mark is 10 ml (0.01 ℓ). 3 ℓ 40 ml is 4 marks past 3 ℓ: 40 ml = 40 ÷ 1000 ℓ = 0.04 ℓ, "
        "so 3 ℓ 40 ml = 3.04 ℓ, not 3.4 ℓ.</figcaption></figure>"
        + ex("Example 2", "Write 5.07 m in m and cm.", "5.07 m = 5 m + 0.07 m. 0.07 × 100 = 7, so 0.07 m = 7 cm.",
             "5 m 7 cm")
        + "<h2>Word problems: use the same unit</h2>"
        "<p>Draw a bar model. Change all the measurements to the same unit before you add or subtract.</p>"
        "<figure class='sn-fig'>" + f4 +
        "<figcaption>Priya has 1.5 ℓ of soya bean milk and pours out 350 ml. 350 ml = 0.35 ℓ. "
        "1.5 ℓ − 0.35 ℓ = 1.15 ℓ is left.</figcaption></figure>"
        + "<h2>Common mistakes</h2>"
        + table(["Mistake", "What to do instead"], [
            ["3.5 ÷ 100 = 350 (moving the digits the wrong way)", "Dividing makes it smaller: 0.035"],
            ["0.67 × 10 = 0.670 (“just add a zero”)", "Move every digit 1 place to the left: 6.7"],
            ["0.45 × 30 = 1.35 (forgetting the × 10)", "× 3, then × 10: 13.5"],
            ["3 ℓ 40 ml = 3.4 ℓ", "40 ml = 0.04 ℓ, so 3.04 ℓ"],
            ["4.5 m = 45 cm (1 m = 10 cm)", "1 m = 100 cm, so 450 cm"],
            ["2.4 km + 650 m = 652.4 km", "Same unit first: 2.4 km + 0.65 km = 3.05 km"],
        ])
    )


FAQ = [
    {"q": "What is taught in P5 decimals?",
     "a": "In Primary 5, students multiply and divide decimals (up to 3 decimal places) by 10, 100, 1000 and their multiples, such as 0.45 × 30 and 8.4 ÷ 20. They also convert measurements between units in decimal form, such as 2.35 km = 2350 m and 3 ℓ 40 ml = 3.04 ℓ."},
    {"q": "How do I explain multiplying a decimal by 30 to my child?",
     "a": "Split 30 into 3 × 10: multiply by 3 first, then by 10. For 0.45 × 30, 0.45 × 3 = 1.35 and 1.35 × 10 = 13.5."},
    {"q": "Why is 3 ℓ 40 ml equal to 3.04 ℓ and not 3.4 ℓ?",
     "a": "1 ℓ = 1000 ml, so 40 ml = 40 ÷ 1000 ℓ = 0.04 ℓ, and 3 ℓ 40 ml = 3.04 ℓ. 3.4 ℓ would be 3 ℓ 400 ml."},
    {"q": "Is this in the MOE syllabus?",
     "a": "Yes. Multiplying and dividing decimals by 10, 100, 1000 and their multiples, and converting measurements in decimal form, are part of the Primary 5 Decimals topic in the MOE 2021 Primary Mathematics Syllabus. These skills are used again in Primary 6 and the PSLE."},
]


def mark_large(u, pattern):
    """Tag place value charts, step diagrams, number lines and bar models so they print larger."""
    rx = re.compile(r"<svg (?=[^>]*aria-label='(?:" + pattern + "))")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u


def check_answers(sets):
    """Re-check every 'a × b = ?' / 'a ÷ b = ?' and 'What is a op b?' question with Decimal."""
    num = r"([\d. ]+)"
    rxs = [re.compile(r"^" + num + r" ([×÷]) " + num + r" = \?$"), re.compile(r"What is " + num + r" ([×÷]) " + num + r"\?$")]
    n = 0
    for s in sets:
        for it in s["items"]:
            for rx in rxs:
                m = rx.search(it["q"])
                if m:
                    a, op, b = Dm(m.group(1).replace(NB, "")), m.group(2), Dm(m.group(3).replace(NB, ""))
                    r = a * b if op == "×" else a / b
                    assert parse(it["c"][it["a"]])[1] == r, it["q"]
                    n += 1
                    break
            for c in it["c"]:
                v = parse(c)
                if v and v[0] == "$":
                    assert v[1] == v[1].quantize(Dm("0.01")), (it["q"], c)
    return n


def gen():
    rnd = random.Random(65807)
    sets = [set_p10(), set_mult(), set_convert(), set_compound(), set_problems()]
    assert check_answers(sets) >= 25
    balance(sets, rnd)
    seen = set()
    for s in sets:
        assert len(s["items"]) == 20, (s["title"], len(s["items"]))
        assert sorted(it["a"] for it in s["items"]) == sorted([0, 1, 2, 3] * 5)
        for it in s["items"]:
            assert len(set(it["c"])) == 4, it
            assert it["q"].count("<svg") <= 1
            k = re.sub(r"<[^>]+>", "", it["q"])
            assert k not in seen, it["q"]
            seen.add(k)
            for x in [it["q"], it["e"]] + it["c"]:
                assert "\\" not in x and '"' not in x, x
    u = {
        "country": "sg", "subject": "maths", "grade": "primary-5", "slug": "decimals-and-measurement",
        "sort": 7, "updated": UPDATED, "pdf_url": "",
        "title": "Primary 5 Decimals and Measurement",
        "seo_title": "P5 Decimals and Measurement Worksheets: Free Primary 5 Maths with Answers (MOE Syllabus)",
        "short_title": "Decimals and Measurement",
        "domain": "Number and Algebra",
        "standard_code": "Primary 5: Decimals",
        "standard_url": "https://www.moe.gov.sg/primary/curriculum/syllabus",
        "standard_text": "Multiplying and dividing decimals (up to 3 decimal places) by 10, 100, 1000 and their multiples; "
                         "converting measurements between units in decimal form",
        "meta_desc": "Free P5 maths practice: × and ÷ decimals by 10, 100, 1000 and multiples, and converting "
                     "km, m, kg, ℓ and ml as decimals. 100 questions with answers.",
        "key_big": "× 10, 100, 1000 moves every digit 1, 2, 3 places left; ÷ moves them right.",
        "key_sub": "0.45 × 30 = 0.45 × 3 × 10 = 13.5, and 3 ℓ 40 ml = 3.04 ℓ (40 ml = 0.04 ℓ).",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }
    assert len(u["meta_desc"]) <= 160, len(u["meta_desc"])
    return mark_large(u, "place value chart|steps|number line|bar model")


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
