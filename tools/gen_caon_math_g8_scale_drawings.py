# -*- coding: utf-8 -*-
"""
Ontario Grade 8 Math: Scale Drawings (Ontario Curriculum 2020, Grade 8: E1.3)
  python3 tools/gen_caon_math_g8_scale_drawings.py
Read scales (1 cm : 2 m, 1:500, scale bars), find actual lengths from a drawing, find drawing lengths
from actual lengths and redraw at a new scale, find areas from scale drawings (area scales by the
square of the length factor), then map, floor-plan and model word problems in Canadian contexts.
Wrong answers come from real mistakes: dividing instead of multiplying, adding the scale, reading
1:500 as 500 m, cm/m/km slips, scaling an area by the length factor, and perimeter for area.
Every answer is checked with fractions.Fraction (never float).
Canadian English, metric units, SI number spacing (no-break space). HTML attributes use single quotes.
"""
import json, os, random, re
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "ca-on", "math", "grade-8")
SLUG = "scale-drawings"
UPDATED = "2026-11-02"
NBSP = " "
FILL = "#4fae74"
PALE = "#dff0e5"
LINE = "#2b2b2b"
THIN = "#9a9a9a"
RED = "#d6453b"
BLUE = "#2f6fc0"
FONT = "Arial, Helvetica, sans-serif"
CANT = "You can’t tell"
SQ = "²"


# ------------------------------------------------------------ numbers
def num(x):
    """Exact decimal text: F(9, 2) -> '4.5', 2500 -> '2500', 18000 -> '18 000' (no-break space)."""
    x = F(x)
    assert x >= 0, x
    d, k = x.denominator, 0
    while (10 ** k) % d:
        k += 1
        assert k < 8, x
    v = x.numerator * (10 ** k // d)
    i, r = divmod(v, 10 ** k)
    s = str(i) if i < 10000 else "{:,}".format(i).replace(",", NBSP)
    if r:
        s += "." + str(r).zfill(k).rstrip("0")
    return s


def L(x, u):
    return "%s %s" % (num(x), u)


def A(x, u):
    return "%s %s%s" % (num(x), u, SQ)


def R(a, b):
    return "%s:%s" % (num(a), num(b))


def fr(a, b):
    return "<span class='fr'><span class='fn'>%s</span><span class='fd'>%s</span></span>" % (a, b)


def plain(s):
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", s)).strip()


FRX = re.compile(r"^<span class='fr'><span class='fn'>(\d+)</span><span class='fd'>(\d+)</span></span>$")
RAT = re.compile(r"^(\d[\d" + NBSP + r"]*(?:\.\d+)?):(\d[\d" + NBSP + r"]*(?:\.\d+)?)$")
NUM = re.compile(r"^(\$)?(\d[\d" + NBSP + r"]*(?:\.\d+)?)( .+)?$")
UNIT = {"mm": F(1, 10), "cm": F(1), "m": F(100), "km": F(100000),
        "mm²": F(1, 100), "cm²": F(1), "m²": F(10000), "km²": F(10 ** 10)}


def val(c):
    """(number, unit) of a choice, or None when it is not a single number."""
    m = FRX.match(c)
    if m:
        return (F(int(m.group(1)), int(m.group(2))), "")
    m = RAT.match(c)
    if m:
        return (F(m.group(1).replace(NBSP, "")) / F(m.group(2).replace(NBSP, "")), "ratio")
    m = NUM.match(c)
    if not m:
        return None
    v = F(m.group(2).replace(NBSP, ""))
    u = (m.group(3) or "").strip()
    if m.group(1):
        return None if u else (v, "$")
    return (v, u)


def norm(c):
    """Value in base units, so that 300 m and 0.3 km count as the same value."""
    v = val(c)
    if v is None:
        return None
    if v[1] in UNIT:
        return (v[0] * UNIT[v[1]], "area" if SQ in v[1] else "len")
    return v


def mcq(q, right, wrong, e, value=None):
    """Correct answer first + 3 wrong; balance() moves it. No two choices equal in value.
    value: the exact answer (number before its unit), checked against the correct choice."""
    right = str(right)
    wrong = [str(x) for x in wrong]
    assert len(wrong) == 3, (q, wrong)
    ch = [right] + wrong
    assert len(set(plain(x) for x in ch)) == 4, (q, ch)
    if value is not None:
        v = val(right)
        assert v is not None and v[0] == F(value), (q, right, value)
    known = [n for n in (norm(x) for x in ch) if n is not None]
    assert len(set(known)) == len(known), (q, ch)
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


def table(head, rows):
    h = "".join("<th>%s</th>" % x for x in head)
    b = "".join("<tr>" + "".join("<td>%s</td>" % c for c in r) + "</tr>" for r in rows)
    return "<div class='sn-tw'><table class='sn-table'><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>" % (h, b)


def ex(title, q, s, a):
    return ("<div class='sn-ex'><span class='sn-ex-t'>%s</span><p class='sn-ex-q'>%s</p>"
            "<p class='sn-ex-s'>%s</p><p class='sn-ex-a'>Answer: %s</p></div>" % (title, q, s, a))


# ------------------------------------------------------------ svg helpers
def fig(svg):
    return "<div class='qfig'>" + svg + "</div>"


def svg_wrap(w, h, body, label):
    w, h = int(round(w)), int(round(h))
    return ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 %d %d' width='%d' height='%d' "
            "role='img' aria-label='%s'><g font-family='%s'>%s</g></svg>" % (w, h, w, h, label, FONT, body))


def text(x, y, t, fs=16, anchor="middle", col=LINE, weight=700):
    return ("<text x='%.1f' y='%.1f' font-size='%d' font-weight='%d' fill='%s' text-anchor='%s'>%s</text>"
            % (x, y, fs, weight, col, anchor, t))


def tw(t, fs):
    """Rough width of bold Arial text."""
    return len(plain(t)) * fs * 0.62


def scale_bar_svg(cm, amt, unit, parts):
    """Scale bar: `parts` alternating blocks; the whole bar is `cm` cm on the drawing and stands for `amt` `unit`.
    The picture is not to real size, so the length of the bar is written under it."""
    lab = [num(F(amt * i, parts)) for i in range(parts + 1)]
    Lx = 6 + tw("0", 14) / 2
    seg = max(44.0 * cm / parts, max(tw(t, 14) for t in lab) + 10)
    bw = seg * parts
    s = []
    for i in range(parts):
        s.append("<rect x='%.1f' y='30' width='%.1f' height='14' fill='%s' stroke='%s' stroke-width='1.6'/>"
                 % (Lx + i * seg, seg, LINE if i % 2 == 0 else "#ffffff", LINE))
    for i in range(parts + 1):
        s.append(text(Lx + i * seg, 22, lab[i], 14, weight=400))
    s.append(text(Lx + bw + 8, 42, unit, 15, "start"))
    s.append("<line x1='%.1f' y1='58' x2='%.1f' y2='58' stroke='%s' stroke-width='1.6'/>" % (Lx, Lx + bw, BLUE))
    for x in (Lx, Lx + bw):
        s.append("<line x1='%.1f' y1='52' x2='%.1f' y2='64' stroke='%s' stroke-width='1.6'/>" % (x, x, BLUE))
    s.append(text(Lx + bw / 2, 80, "%s cm" % num(cm), 14, col=BLUE))
    W = max(Lx + bw + 8 + tw(unit, 15) + 4, Lx + bw + tw(lab[-1], 14) / 2 + 4)
    return svg_wrap(W, 88, "".join(s), "scale bar: %s cm stands for %s %s" % (num(cm), num(amt), unit))


def rect_svg(w, h, name="", PX=26):
    """A rectangle drawn in proportion (w × h cm), sides labelled in cm, a name inside."""
    x0, y0 = 6, 6
    bw, bh = float(w * PX), float(h * PX)
    s = ["<rect x='%d' y='%d' width='%.1f' height='%.1f' fill='%s' stroke='%s' stroke-width='2.5'/>"
         % (x0, y0, bw, bh, PALE, LINE)]
    if name:
        assert tw(name, 14) < bw - 6, name
        s.append(text(x0 + bw / 2, y0 + bh / 2 + 5, name, 14, weight=400))
    lw = "%s cm" % num(w)
    lh = "%s cm" % num(h)
    s.append(text(x0 + bw / 2, y0 + bh + 20, lw, 15, col=BLUE))
    s.append(text(x0 + bw + 6, y0 + bh / 2 + 5, lh, 15, "start", col=BLUE))
    W = x0 + bw + 6 + tw(lh, 15) + 4
    H = y0 + bh + 26
    return svg_wrap(W, H, "".join(s), "scale drawing: rectangle %s cm by %s cm" % (num(w), num(h)))


def grid_plan_svg(cols, rows, cells):
    """A grid of 1 cm squares; `cells` (col, row) are the shaded room."""
    sq = 24
    W, H = cols * sq + 8, rows * sq + 8
    s = []
    for (c, r) in cells:
        s.append("<rect x='%d' y='%d' width='%d' height='%d' fill='%s'/>" % (4 + c * sq, 4 + r * sq, sq, sq, FILL))
    for i in range(cols + 1):
        s.append("<line x1='%d' y1='4' x2='%d' y2='%d' stroke='%s' stroke-width='1.2'/>" % (4 + i * sq, 4 + i * sq, 4 + rows * sq, THIN))
    for j in range(rows + 1):
        s.append("<line x1='4' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='1.2'/>" % (4 + j * sq, 4 + cols * sq, 4 + j * sq, THIN))
    # outline of the room
    cs = set(cells)
    for (c, r) in cells:
        x, y = 4 + c * sq, 4 + r * sq
        for (dc, dr, x1, y1, x2, y2) in ((0, -1, x, y, x + sq, y), (0, 1, x, y + sq, x + sq, y + sq),
                                         (-1, 0, x, y, x, y + sq), (1, 0, x + sq, y, x + sq, y + sq)):
            if (c + dc, r + dr) not in cs:
                s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='3' stroke-linecap='square'/>"
                         % (x1, y1, x2, y2, LINE))
    return svg_wrap(W, H, "".join(s), "floor plan on a grid of 1 cm squares: %d squares shaded" % len(cells))


def area_svg():
    """1 cm by 1 cm on the drawing stands for 2 m by 2 m = 4 m² in real life."""
    a = 46
    s = []
    x0, y0 = 46, 30
    s.append("<rect x='%d' y='%d' width='%d' height='%d' fill='%s' stroke='%s' stroke-width='2.5'/>" % (x0, y0, a, a, PALE, LINE))
    s.append(text(x0 + a / 2, y0 - 8, "1 cm", 14, col=BLUE))
    s.append(text(x0 - 6, y0 + a / 2 + 5, "1 cm", 14, "end", col=BLUE))
    s.append(text(x0 + a / 2, y0 + a + 22, "drawing", 14, weight=400))
    s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='2.5'/>" % (x0 + a + 14, y0 + a / 2 + 23, x0 + a + 52, y0 + a / 2 + 23, LINE))
    s.append("<polygon points='%d,%d %d,%d %d,%d' fill='%s'/>" % (x0 + a + 60, y0 + a / 2 + 23, x0 + a + 50, y0 + a / 2 + 17, x0 + a + 50, y0 + a / 2 + 29, LINE))
    x1 = x0 + a + 112
    for i in range(2):
        for j in range(2):
            s.append("<rect x='%d' y='%d' width='%d' height='%d' fill='%s' stroke='%s' stroke-width='1.6'/>"
                     % (x1 + i * a, y0 + j * a, a, a, FILL if (i + j) % 2 == 0 else PALE, LINE))
            s.append(text(x1 + i * a + a / 2, y0 + j * a + a / 2 + 5, "1 m%s" % SQ, 14, weight=400))
    s.append("<rect x='%d' y='%d' width='%d' height='%d' fill='none' stroke='%s' stroke-width='2.5'/>" % (x1, y0, 2 * a, 2 * a, LINE))
    s.append(text(x1 + a, y0 - 8, "2 m", 14, col=BLUE))
    s.append(text(x1 - 6, y0 + a + 5, "2 m", 14, "end", col=BLUE))
    s.append(text(x1 + a, y0 + 2 * a + 22, "real life", 14, weight=400))
    return svg_wrap(x1 + 2 * a + 8, y0 + 2 * a + 30, "".join(s), "area: 1 cm by 1 cm on the drawing stands for 2 m by 2 m, or 4 square metres")


# ============================================================ set 1: reading scales
def set_read():
    its = []
    its.append(mcq("A scale drawing uses the scale 1 cm : 2 m. What does 3 cm on the drawing stand for?",
                   L(6, "m"), [L(F(3, 2), "m"), L(5, "m"), L(6, "cm")],
                   "Each 1 cm stands for 2 m, so 3 cm stands for 3 × 2 = <b>6 m</b>. "
                   "1.5 m divides, 5 m adds, and 6 cm forgets that the real lengths are in metres.", value=6))
    its.append(mcq("A plan uses the scale 1 cm : 5 m. What does 4 cm on the plan stand for?",
                   L(20, "m"), [L(F(4, 5), "m"), L(9, "m"), L(20, "cm")],
                   "4 × 5 = <b>20 m</b>. 0.8 m divides 4 by 5, 9 m adds 4 + 5, and 20 cm uses the wrong unit.", value=20))
    its.append(mcq("A map uses the scale 1 cm : 10 km. What does 7 cm on the map stand for?",
                   L(70, "km"), [L(17, "km"), L(F(7, 10), "km"), L(70, "m")],
                   "7 × 10 = <b>70 km</b>. 17 km adds, 0.7 km divides, and 70 m uses metres instead of kilometres.", value=70))
    its.append(mcq(fig(scale_bar_svg(4, 40, "m", 4)) + "Each block of this scale bar is 1 cm long. What scale does it show?",
                   "1 cm : 10 m", ["1 cm : 40 m", "1 cm : 4 m", "4 cm : 10 m"],
                   "The whole bar is 4 cm for 40 m. Each 1 cm block is 40 ÷ 4 = 10 m, so the scale is <b>1 cm : 10 m</b>. "
                   "1 cm : 40 m reads the whole bar as 1 cm, and 1 cm : 4 m divides the wrong way."))
    its.append(mcq("What does the scale 1:500 mean on a plan?",
                   "1 cm on the plan is 500 cm in real life",
                   ["1 cm on the plan is 500 m in real life", "500 cm on the plan is 1 cm in real life",
                    "The plan is 500 times as big as the real thing"],
                   "A ratio scale has the <b>same unit</b> on both sides: 1 cm stands for 500 cm (= 5 m). "
                   "The first number is the drawing, so the plan is smaller than the real thing."))
    its.append(mcq("Write the scale 1 cm : 2 m as a ratio with no units.",
                   R(1, 200), [R(1, 2), R(1, 20), R(1, 2000)],
                   "Change both parts to the same unit: 2 m = 200 cm. So 1 cm : 200 cm = <b>1:200</b>. "
                   "1:2 forgets to change the metres into centimetres."))
    its.append(mcq("Write the map scale 1 cm : 5 km as a ratio with no units.",
                   R(1, 500000), [R(1, 5000), R(1, 50000), R(1, 5)],
                   "1 km = 1000 m = 100" + NBSP + "000 cm, so 5 km = 500" + NBSP + "000 cm. The ratio is <b>1:500" + NBSP + "000</b>. "
                   "1:5000 changes km to m only."))
    its.append(mcq("A plan has the scale 1:500. Complete: 1 cm on the plan stands for ? in real life.",
                   L(5, "m"), [L(500, "m"), L(50, "m"), L(F(1, 2), "m")],
                   "1 cm stands for 500 cm. 500 cm ÷ 100 = <b>5 m</b>. 500 m keeps the 500 but switches the unit to metres.", value=5))
    its.append(mcq("A plan has the scale 1:250. Complete: 1 cm on the plan stands for ? in real life.",
                   L(F(5, 2), "m"), [L(250, "m"), L(25, "m"), L(F(1, 4), "m")],
                   "1 cm stands for 250 cm = 250 ÷ 100 = <b>2.5 m</b>. 250 m reads the ratio as metres, "
                   "and 25 m divides by 10 instead of 100.", value=F(5, 2)))
    its.append(mcq("A town map has the scale 1:20" + NBSP + "000. Complete: 1 cm on the map stands for ? in real life.",
                   L(200, "m"), [L(20, "m"), L(2000, "m"), L(20000, "m")],
                   "1 cm stands for 20" + NBSP + "000 cm. 20" + NBSP + "000 ÷ 100 = <b>200 m</b>. "
                   "20 m divides by 1000, and 2000 m divides by 10.", value=200))
    its.append(mcq("A road map has the scale 1:100" + NBSP + "000. Complete: 1 cm on the map stands for ? in real life.",
                   L(1, "km"), [L(100, "km"), L(10, "km"), L(100, "m")],
                   "100" + NBSP + "000 cm = 1000 m = <b>1 km</b>. 100 km reads the ratio as kilometres, "
                   "and 100 m divides by 1000 instead of 100.", value=1))
    its.append(mcq("Which scale makes a drawing that is <b>larger</b> than the real object?",
                   R(5, 1), [R(1, 5), R(1, 50), R(1, 500)],
                   "The first number is the drawing. In <b>5:1</b>, 5 cm on the drawing stands for 1 cm in real life, "
                   "so the drawing is an enlargement. 1:5, 1:50 and 1:500 all make the drawing smaller."))
    its.append(mcq("Ethan draws the same garden at four different scales. Which scale gives the <b>largest</b> drawing?",
                   R(1, 50), [R(1, 100), R(1, 200), R(1, 500)],
                   "At 1:50, 1 cm stands for only 50 cm, so you need more centimetres for the garden. "
                   "<b>1:50</b> is the largest drawing. 1:500 has the biggest number but makes the smallest drawing."))
    its.append(mcq("A model car is built at a scale of 1:24. How many times as long as the model is the real car?",
                   "24", [fr(1, 24), "2.4", "240"],
                   "1:24 means 1 cm on the model stands for 24 cm on the car. The real car is <b>24</b> times as long. "
                   + fr(1, 24) + " is how long the model is compared with the car.", value=24))
    its.append(mcq("A plan uses the scale 2 cm : 5 m. What does 1 cm on the plan stand for?",
                   L(F(5, 2), "m"), [L(10, "m"), L(5, "m"), L(3, "m")],
                   "2 cm stands for 5 m, so 1 cm stands for half of it: 5 ÷ 2 = <b>2.5 m</b>. "
                   "10 m multiplies by 2, and 3 m subtracts 5 − 2.", value=F(5, 2)))
    its.append(mcq("A plan uses the scale 4 cm : 1 m. Write it as a ratio in the form 1:n.",
                   R(1, 25), [R(4, 1), R(1, 4), R(1, 250)],
                   "1 m = 100 cm, so 4 cm : 100 cm. Divide both parts by 4: <b>1:25</b>. "
                   "4:1 forgets to change 1 m into 100 cm."))
    its.append(mcq(fig(scale_bar_svg(3, 150, "m", 3)) + "This scale bar is 3 cm long. Which ratio does it show?",
                   R(1, 5000), [R(1, 50), R(1, 500), R(1, 150)],
                   "3 cm stands for 150 m, so 1 cm stands for 50 m = 5000 cm. The ratio is <b>1:5000</b>. "
                   "1:50 forgets to change metres into centimetres, and 1:150 reads the whole bar as 1 cm."))
    its.append(mcq(fig(scale_bar_svg(2, 10, "km", 4)) + "This scale bar is 2 cm long. What does 1 cm on the map stand for?",
                   L(5, "km"), [L(10, "km"), L(F(5, 2), "km"), L(20, "km")],
                   "2 cm stands for 10 km, so 1 cm stands for 10 ÷ 2 = <b>5 km</b>. 2.5 km is one block, "
                   "but each block is only 0.5 cm. 20 km multiplies by 2.", value=5))
    its.append(mcq("A floor plan has the scale 1:50. Which statement is true?",
                   "2 cm on the plan stands for 1 m",
                   ["1 cm on the plan stands for 50 m", "1 m on the plan stands for 50 cm", "50 cm on the plan stands for 1 cm"],
                   "1 cm stands for 50 cm, so 2 cm stands for 100 cm = <b>1 m</b>. "
                   "50 m reads the ratio as metres, and the other two put the real length first."))
    its.append(mcq("Map A has the scale 1:50" + NBSP + "000. Map B has the scale 1 cm : 2 km. Which map shows the same lake larger?",
                   "Map A", ["Map B", "They are the same size", CANT],
                   "Map A: 1 cm stands for 50" + NBSP + "000 cm = 0.5 km. Map B: 1 cm stands for 2 km. "
                   "On Map A each centimetre covers less ground, so the lake is drawn larger: <b>Map A</b>."))
    assert len(its) == 20, len(its)
    return {"title": "Reading scales: 1 cm : 2 m, 1:500 and scale bars", "items": its}


# ============================================================ set 2: actual lengths from a drawing
def set_actual():
    its = []
    its.append(mcq(fig(rect_svg(6, 4, "patio")) + "The scale is 1 cm : 2 m. How long is the longer side of the real patio?",
                   L(12, "m"), [L(3, "m"), L(8, "m"), L(12, "cm")],
                   "The longer side is 6 cm on the drawing. 6 × 2 = <b>12 m</b>. 3 m divides, 8 m adds, and 12 cm uses the wrong unit.",
                   value=6 * 2))
    its.append(mcq(fig(rect_svg(5, 2, "pool")) + "The scale is 1 cm : 3 m. How wide is the real pool (the shorter side)?",
                   L(6, "m"), [L(15, "m"), L(5, "m"), L(6, "cm")],
                   "The shorter side is 2 cm. 2 × 3 = <b>6 m</b>. 15 m is the longer side (5 × 3), and 5 m adds 2 + 3.",
                   value=2 * 3))
    its.append(mcq("A floor plan has the scale 1:200. A wall is 6 cm long on the plan. How long is the real wall?",
                   L(12, "m"), [L(1200, "m"), L(120, "m"), L(F(6, 5), "m")],
                   "6 × 200 = 1200 cm. 1200 cm ÷ 100 = <b>12 m</b>. 1200 m forgets to change centimetres into metres.",
                   value=F(6 * 200, 100)))
    its.append(mcq("A plan of a house has the scale 1:50. A door is 4 cm tall on the plan. How tall is the real door?",
                   L(2, "m"), [L(200, "m"), L(20, "m"), L(F(8, 100), "m")],
                   "4 × 50 = 200 cm = <b>2 m</b>. 200 m keeps 200 but changes the unit, and 0.08 m divides 4 by 50.",
                   value=F(4 * 50, 100)))
    its.append(mcq("A hiking map has the scale 1:50" + NBSP + "000. Two campsites are 6 cm apart on the map. How far apart are they really?",
                   L(3, "km"), [L(300, "km"), L(30, "km"), L(F(3, 10), "km")],
                   "6 × 50" + NBSP + "000 = 300" + NBSP + "000 cm. 300" + NBSP + "000 cm = 3000 m = <b>3 km</b>. "
                   "300 km changes cm straight to km without dividing by 100" + NBSP + "000.",
                   value=F(6 * 50000, 100000)))
    its.append(mcq("A road map has the scale 1:250" + NBSP + "000. Two towns are 4 cm apart on the map. How far apart are they really?",
                   L(10, "km"), [L(100, "km"), L(1, "km"), L(1000, "km")],
                   "4 × 250" + NBSP + "000 = 1" + NBSP + "000" + NBSP + "000 cm = 10" + NBSP + "000 m = <b>10 km</b>. "
                   "100 km and 1 km each slip by a factor of 10 when changing units.",
                   value=F(4 * 250000, 100000)))
    its.append(mcq(fig(scale_bar_svg(4, 40, "km", 4)) + "Two towns are 3.5 cm apart on this map. How far apart are they really?",
                   L(35, "km"), [L(140, "km"), L(30, "km"), L(350, "km")],
                   "The bar shows 4 cm for 40 km, so 1 cm stands for 10 km. 3.5 × 10 = <b>35 km</b>. "
                   "140 km multiplies 3.5 by the whole bar (40 km), and 30 km drops the half centimetre.",
                   value=F(7, 2) * 10))
    its.append(mcq(fig(grid_plan_svg(6, 4, [(c, r) for c in range(6) for r in range(4)])) +
                   "Each square on this plan is 1 cm. The scale is 1 cm : 1.5 m. How long is the real room (the longer side)?",
                   L(9, "m"), [L(F(15, 2), "m"), L(4, "m"), L(6, "m")],
                   "The longer side is 6 squares = 6 cm. 6 × 1.5 = <b>9 m</b>. 7.5 m adds 6 + 1.5, "
                   "4 m divides 6 by 1.5, and 6 m forgets the scale.", value=6 * F(3, 2)))
    its.append(mcq("Aiden builds a model car at a scale of 1:24. The model is 18 cm long. How long is the real car?",
                   L(F(432, 100), "m"), [L(F(3, 4), "m"), L(F(432, 10), "m"), L(42, "cm")],
                   "18 × 24 = 432 cm = <b>4.32 m</b>, a normal car length. 0.75 m divides 18 by 24, "
                   "43.2 m divides by 10 instead of 100, and 42 cm adds 18 + 24.", value=F(18 * 24, 100)))
    its.append(mcq("A model train is built at a scale of 1:87. The model locomotive is 20 cm long. How long is the real locomotive?",
                   L(F(174, 10), "m"), [L(174, "m"), L(F(174, 100), "m"), L(107, "cm")],
                   "20 × 87 = 1740 cm. 1740 ÷ 100 = <b>17.4 m</b>. 174 m divides by 10 instead of 100, "
                   "and 107 cm adds 20 + 87.", value=F(20 * 87, 100)))
    its.append(mcq("A plan uses the scale 2 cm : 5 m. A pool is 10 cm long on the plan. How long is the real pool?",
                   L(25, "m"), [L(50, "m"), L(4, "m"), L(20, "m")],
                   "10 cm is 5 groups of 2 cm, so the pool is 5 × 5 = <b>25 m</b>. 50 m treats the scale as 1 cm : 5 m, "
                   "4 m divides 10 by 2.5, and 20 m multiplies 10 by 2.", value=F(10, 2) * 5))
    its.append(mcq("A bedroom plan uses the scale 1 cm : 0.5 m. The bed is 4 cm long on the plan. How long is the real bed?",
                   L(2, "m"), [L(8, "m"), L(F(9, 2), "m"), L(F(1, 5), "m")],
                   "4 × 0.5 = <b>2 m</b>. 8 m divides 4 by 0.5, and 4.5 m adds 4 + 0.5.", value=4 * F(1, 2)))
    its.append(mcq("A plan uses the scale 3 cm : 1 m. A desk is 4.5 cm long on the plan. How long is the real desk?",
                   L(F(3, 2), "m"), [L(F(27, 2), "m"), L(F(11, 2), "m"), L(15, "m")],
                   "Every 3 cm stands for 1 m, so 4.5 ÷ 3 = <b>1.5 m</b>. 13.5 m multiplies by 3, "
                   "5.5 m adds 4.5 + 1, and 15 m moves the decimal point.", value=F(9, 2) / 3))
    its.append(mcq("A science book shows an ant at a scale of 5:1. The drawing is 4 cm long. How long is the real ant?",
                   L(8, "mm"), [L(20, "cm"), L(9, "cm"), L(F(8, 10), "mm")],
                   "5:1 is an enlargement: the drawing is 5 times as long as the ant. 4 ÷ 5 = 0.8 cm = <b>8 mm</b>. "
                   "20 cm multiplies, and 0.8 mm keeps the number but uses the wrong unit.", value=8))
    its.append(mcq("A diagram shows a ladybug at a scale of 10:1. The drawing is 50 mm long. How long is the real ladybug?",
                   L(5, "mm"), [L(500, "mm"), L(40, "mm"), L(F(1, 2), "mm")],
                   "The drawing is 10 times as long as the ladybug. 50 ÷ 10 = <b>5 mm</b>. "
                   "500 mm multiplies, 40 mm subtracts 10, and 0.5 mm divides by 100.", value=F(50, 10)))
    its.append(mcq("A city map has the scale 1:20" + NBSP + "000. Two schools are 7.5 cm apart on the map. How far apart are they really?",
                   L(F(3, 2), "km"), [L(15, "km"), L(F(3, 20), "km"), L(150, "km")],
                   "7.5 × 20" + NBSP + "000 = 150" + NBSP + "000 cm = 1500 m = <b>1.5 km</b>. "
                   "15 km and 0.15 km each slip by a factor of 10, and 150 km changes cm straight to km.",
                   value=F(15, 2) * 20000 / 100000))
    its.append(mcq(fig(rect_svg(5, 4, "classroom")) + "The scale is 1:100. What is the perimeter of the real classroom?",
                   L(18, "m"), [L(9, "m"), L(20, "m"), L(1800, "m")],
                   "Real sides: 5 × 100 = 500 cm = 5 m and 4 × 100 = 400 cm = 4 m. Perimeter: 2 × (5 + 4) = <b>18 m</b>. "
                   "9 m adds only two sides, 20 m is the area number, and 1800 m forgets to change the units.",
                   value=2 * (5 + 4)))
    its.append(mcq("A map has the scale 1 cm : 25 km. Toronto and Ottawa are about 14 cm apart on the map. About how far apart are they?",
                   L(350, "km"), [L(39, "km"), L(140, "km"), L(3500, "km")],
                   "14 × 25 = <b>350 km</b>, close to the straight-line distance between the two cities. "
                   "39 km adds 14 + 25, and 140 km multiplies by 10.", value=14 * 25))
    its.append(mcq(fig(scale_bar_svg(4, 100, "m", 4)) + "A trail on this park map is 6 cm long. How long is the real trail?",
                   L(150, "m"), [L(600, "m"), L(24, "m"), L(F(3, 2), "m")],
                   "The bar shows 4 cm for 100 m, so 1 cm stands for 25 m. 6 × 25 = <b>150 m</b>. "
                   "600 m multiplies 6 by the whole bar, and 24 m multiplies 6 by 4.", value=6 * 25))
    its.append(mcq("A plan of a school has the scale 1:50. A hallway is 16 cm long and 3 cm wide on the plan. "
                   "How much longer than wide is the real hallway?",
                   L(F(13, 2), "m"), [L(13, "m"), L(8, "m"), L(65, "m")],
                   "On the plan the difference is 16 − 3 = 13 cm. 13 × 50 = 650 cm = <b>6.5 m</b>. "
                   "8 m is only the real length (16 × 50 cm), and 65 m divides by 10 instead of 100.",
                   value=F((16 - 3) * 50, 100)))
    assert len(its) == 20, len(its)
    return {"title": "Actual lengths from scale drawings", "items": its}


# ============================================================ set 3: drawing lengths from actual lengths
def set_drawing():
    its = []
    its.append(mcq("A plan uses the scale 1 cm : 2 m. A real wall is 10 m long. How long is it on the plan?",
                   L(5, "cm"), [L(20, "cm"), L(12, "cm"), L(8, "cm")],
                   "Each 2 m becomes 1 cm, so divide: 10 ÷ 2 = <b>5 cm</b>. 20 cm multiplies, 12 cm adds, and 8 cm subtracts.",
                   value=F(10, 2)))
    its.append(mcq("A plan uses the scale 1 cm : 5 m. A real fence is 35 m long. How long is it on the plan?",
                   L(7, "cm"), [L(175, "cm"), L(40, "cm"), L(30, "cm")],
                   "35 ÷ 5 = <b>7 cm</b>. 175 cm multiplies instead of dividing, 40 cm adds, and 30 cm subtracts.", value=F(35, 5)))
    its.append(mcq("A plan has the scale 1:100. A real room is 6 m long. How long is it on the plan?",
                   L(6, "cm"), [L(600, "cm"), L(60, "cm"), L(F(6, 10), "cm")],
                   "6 m = 600 cm. 600 ÷ 100 = <b>6 cm</b>. 600 cm is the real length, and 60 cm divides by 10.", value=F(600, 100)))
    its.append(mcq("A plan has the scale 1:50. A real table is 3 m long. How long is it on the plan?",
                   L(6, "cm"), [L(150, "cm"), L(F(6, 10), "cm"), L(60, "cm")],
                   "3 m = 300 cm. 300 ÷ 50 = <b>6 cm</b>. 150 cm multiplies 3 by 50, and 0.6 cm and 60 cm slip by a factor of 10.",
                   value=F(300, 50)))
    its.append(mcq("A plan has the scale 1:200. A real driveway is 15 m long. How long is it on the plan?",
                   L(F(15, 2), "cm"), [L(3000, "cm"), L(75, "cm"), L(F(3, 4), "cm")],
                   "15 m = 1500 cm. 1500 ÷ 200 = <b>7.5 cm</b>. 3000 cm multiplies 15 by 200, "
                   "and 75 cm and 0.75 cm slip by a factor of 10.", value=F(1500, 200)))
    its.append(mcq("A site plan has the scale 1:500. A real parking lot is 40 m long. How long is it on the plan?",
                   L(8, "cm"), [L(20000, "cm"), L(80, "cm"), L(F(4, 5), "cm")],
                   "40 m = 4000 cm. 4000 ÷ 500 = <b>8 cm</b>. 20" + NBSP + "000 cm multiplies 40 by 500.", value=F(4000, 500)))
    its.append(mcq("A road map has the scale 1:100" + NBSP + "000. Two towns are 12 km apart. How far apart are they on the map?",
                   L(12, "cm"), [L(F(6, 5), "cm"), L(120, "cm"), L(F(12, 100), "cm")],
                   "12 km = 1" + NBSP + "200" + NBSP + "000 cm. 1" + NBSP + "200" + NBSP + "000 ÷ 100" + NBSP + "000 = <b>12 cm</b>. "
                   "Another way: 1 cm stands for 1 km, so 12 km is 12 cm.", value=F(1200000, 100000)))
    its.append(mcq("A hiking map has the scale 1:50" + NBSP + "000. A trail is 4 km long. How long is it on the map?",
                   L(8, "cm"), [L(F(4, 5), "cm"), L(80, "cm"), L(F(25, 2), "cm")],
                   "4 km = 400" + NBSP + "000 cm. 400" + NBSP + "000 ÷ 50" + NBSP + "000 = <b>8 cm</b>. "
                   "12.5 cm divides the wrong way (50" + NBSP + "000 ÷ 4000 m).", value=F(400000, 50000)))
    its.append(mcq("A plan uses the scale 2 cm : 1 m. A real bookshelf is 3.5 m wide. How wide is it on the plan?",
                   L(7, "cm"), [L(F(7, 4), "cm"), L(F(11, 2), "cm"), L(70, "cm")],
                   "Each metre becomes 2 cm: 3.5 × 2 = <b>7 cm</b>. 1.75 cm divides by 2, and 5.5 cm adds 3.5 + 2.",
                   value=F(7, 2) * 2))
    its.append(mcq("A diagram shows a seed at a scale of 20:1. The real seed is 3 mm long. How long is it in the diagram?",
                   L(60, "mm"), [L(F(3, 20), "mm"), L(23, "mm"), L(6, "mm")],
                   "20:1 is an enlargement: the drawing is 20 times as long. 3 × 20 = <b>60 mm</b> (6 cm). "
                   "0.15 mm divides, 23 mm adds, and 6 mm slips by a factor of 10.", value=3 * 20))
    its.append(mcq("A plan uses the scale 1 cm : 4 m. A soccer field is 100 m long. How long is it on the plan?",
                   L(25, "cm"), [L(400, "cm"), L(F(5, 2), "cm"), L(96, "cm")],
                   "100 ÷ 4 = <b>25 cm</b>. 400 cm multiplies, 2.5 cm divides by 40, and 96 cm subtracts.", value=F(100, 4)))
    its.append(mcq("Leah draws a garden that is 12 m by 8 m at a scale of 1:200. What size is her drawing?",
                   "6 cm by 4 cm", ["60 cm by 40 cm", "0.6 cm by 0.4 cm", "24 cm by 16 cm"],
                   "12 m = 1200 cm and 8 m = 800 cm. 1200 ÷ 200 = 6 and 800 ÷ 200 = 4: <b>6 cm by 4 cm</b>. "
                   "24 cm by 16 cm multiplies by 2, and the other two slip by a factor of 10."))
    its.append(mcq("Ava wants to draw a 30 m by 18 m schoolyard as large as possible on a sheet 21.6 cm by 27.9 cm. "
                   "Which scale should she use?",
                   R(1, 200), [R(1, 50), R(1, 100), R(1, 500)],
                   "At 1:100 the drawing is 30 cm by 18 cm, too long for the sheet. At <b>1:200</b> it is 15 cm by 9 cm and fits. "
                   "1:500 (6 cm by 3.6 cm) fits too, but it is smaller. 1:50 is far too big (60 cm)."))
    its.append(mcq("A wall is 8 cm long on a 1:100 plan. Hana redraws the plan at 1:50. How long is the wall on the new plan?",
                   L(16, "cm"), [L(4, "cm"), L(8, "cm"), L(400, "cm")],
                   "Real wall: 8 × 100 = 800 cm. At 1:50: 800 ÷ 50 = <b>16 cm</b>. 1:50 is a larger scale, so the wall gets longer. "
                   "4 cm halves it instead.", value=F(8 * 100, 50)))
    its.append(mcq("A line is 9 cm long on a 1:200 drawing. Noah redraws it at 1:300. How long is the new line?",
                   L(6, "cm"), [L(F(27, 2), "cm"), L(3, "cm"), L(9, "cm")],
                   "Real length: 9 × 200 = 1800 cm. At 1:300: 1800 ÷ 300 = <b>6 cm</b>. "
                   "13.5 cm makes the drawing bigger, but 1:300 is a smaller scale than 1:200.", value=F(9 * 200, 300)))
    its.append(mcq("A path is 6 cm long on a plan with the scale 1 cm : 5 m. How long is it on a new plan with the scale 1 cm : 2 m?",
                   L(15, "cm"), [L(F(12, 5), "cm"), L(6, "cm"), L(12, "cm")],
                   "Real path: 6 × 5 = 30 m. New plan: 30 ÷ 2 = <b>15 cm</b>. 2.4 cm multiplies 6 by 2 and divides by 5, "
                   "which is backwards, and 12 cm multiplies 6 by 2.", value=F(6 * 5, 2)))
    its.append(mcq("The CN Tower is 553 m tall. Olivia builds a model at a scale of 1:500. How tall is the model?",
                   L(F(1106, 10), "cm"), [L(F(1106, 1000), "cm"), L(1106, "cm"), L(F(1106, 100), "cm")],
                   "553 m = 55" + NBSP + "300 cm. 55" + NBSP + "300 ÷ 500 = <b>110.6 cm</b>, a little over 1 m. "
                   "The other answers put the decimal point in the wrong place.", value=F(55300, 500)))
    its.append(mcq("A floor plan uses the scale 1 cm : 0.5 m. A real room is 4.5 m long. How long is it on the plan?",
                   L(9, "cm"), [L(F(9, 4), "cm"), L(5, "cm"), L(4, "cm")],
                   "Each 0.5 m becomes 1 cm. 4.5 ÷ 0.5 = <b>9 cm</b>. 2.25 cm multiplies by 0.5, 5 cm adds, and 4 cm subtracts.",
                   value=F(9, 2) / F(1, 2)))
    its.append(mcq("A map uses the scale 1 cm : 25 km. Two cities are 180 km apart. How far apart are they on the map?",
                   L(F(36, 5), "cm"), [L(4500, "cm"), L(F(18, 25), "cm"), L(72, "cm")],
                   "180 ÷ 25 = <b>7.2 cm</b>. 4500 cm multiplies, and 0.72 cm and 72 cm slip by a factor of 10.", value=F(180, 25)))
    its.append(mcq("A hockey rink is about 61 m long. Mateo draws it at a scale of 1:500. How long is his drawing?",
                   L(F(122, 10), "cm"), [L(30500, "cm"), L(F(122, 100), "cm"), L(122, "cm")],
                   "61 m = 6100 cm. 6100 ÷ 500 = <b>12.2 cm</b>. 30" + NBSP + "500 cm multiplies by 500, "
                   "and 1.22 cm and 122 cm slip by a factor of 10.", value=F(6100, 500)))
    assert len(its) == 20, len(its)
    return {"title": "Drawing lengths from actual lengths, and changing the scale", "items": its}


# ============================================================ set 4: areas
def set_area():
    its = []
    its.append(mcq(fig(rect_svg(4, 3, "deck")) + "The scale is 1 cm : 3 m. What is the area of the real deck?",
                   A(108, "m"), [A(36, "m"), A(12, "m"), A(42, "m")],
                   "Change each length first: 4 × 3 = 12 m and 3 × 3 = 9 m. Area: 12 × 9 = <b>108 m²</b>. "
                   "36 m² multiplies the drawing area (12) by 3 only once, and 42 is the real perimeter.", value=12 * 9))
    its.append(mcq(fig(rect_svg(5, 2, "garden")) + "The scale is 1 cm : 3 m. What is the area of the real garden?",
                   A(90, "m"), [A(30, "m"), A(10, "m"), A(42, "m")],
                   "Real sides: 5 × 3 = 15 m and 2 × 3 = 6 m. Area: 15 × 6 = <b>90 m²</b>. "
                   "30 m² multiplies 10 cm² by 3 instead of 3 × 3 = 9, and 42 is the real perimeter.", value=15 * 6))
    its.append(mcq("A plan has the scale 1:100. A square on the plan is 1 cm by 1 cm. What real area does it stand for?",
                   A(1, "m"), [A(100, "cm"), A(100, "m"), A(10, "m")],
                   "1 cm stands for 100 cm = 1 m, so the square stands for 1 m by 1 m = <b>1 m²</b>. "
                   "100 cm² scales the area by 100 instead of 100 × 100 = 10" + NBSP + "000.", value=1))
    its.append(mcq("Every length in a drawing is made 3 times as long. How many times as large is the area?",
                   "9", ["3", "6", "27"],
                   "Length and width are both 3 times as long, so the area is 3 × 3 = <b>9</b> times as large. "
                   "3 forgets that both sides change, and 27 is 3 × 3 × 3 (that is for volume).", value=9))
    its.append(mcq("A plan uses the scale 1 cm : 2 m. What real area does 1 cm² on the plan stand for?",
                   A(4, "m"), [A(2, "m"), A(8, "m"), A(1, "m")],
                   "1 cm by 1 cm stands for 2 m by 2 m = <b>4 m²</b>. 2 m² scales the area like a length, "
                   "and 8 m² is 2 × 2 × 2.", value=4))
    its.append(mcq("A plan uses the scale 1 cm : 5 m. A lawn covers 6 cm² on the plan. What is the real area of the lawn?",
                   A(150, "m"), [A(30, "m"), A(11, "m"), A(6, "m")],
                   "Each 1 cm² stands for 5 × 5 = 25 m². 6 × 25 = <b>150 m²</b>. 30 m² multiplies by 5 only once, "
                   "and 11 adds 6 + 5.", value=6 * 25))
    its.append(mcq(fig(grid_plan_svg(4, 3, [(c, r) for c in range(4) for r in range(3)])) +
                   "Each square on this plan is 1 cm. The scale is 1 cm : 1.5 m. What is the area of the real room?",
                   A(27, "m"), [A(18, "m"), A(12, "m"), A(21, "m")],
                   "Real sides: 4 × 1.5 = 6 m and 3 × 1.5 = 4.5 m. Area: 6 × 4.5 = <b>27 m²</b>. "
                   "18 m² multiplies 12 squares by 1.5 only once, and 21 is the real perimeter.", value=6 * F(9, 2)))
    lcells = [(c, r) for c in range(4) for r in range(2)] + [(0, 2), (1, 2)]
    its.append(mcq(fig(grid_plan_svg(4, 3, lcells)) +
                   "Each square on this L-shaped plan is 1 cm. The scale is 1 cm : 2 m. What is the area of the real room?",
                   A(40, "m"), [A(20, "m"), A(10, "m"), A(100, "m")],
                   "The room covers %d squares = %d cm². Each 1 cm² stands for 2 × 2 = 4 m². "
                   "10 × 4 = <b>40 m²</b>. 20 m² multiplies by 2 only once." % (len(lcells), len(lcells)), value=len(lcells) * 4))
    its.append(mcq("A map has the scale 1:100" + NBSP + "000. A lake covers 3 cm² on the map. What is the real area of the lake?",
                   A(3, "km"), [A(300, "km"), A(30, "km"), A(F(3, 10), "km")],
                   "1 cm stands for 100" + NBSP + "000 cm = 1 km, so 1 cm² stands for 1 km × 1 km = 1 km². "
                   "3 cm² stands for <b>3 km²</b>.", value=3))
    its.append(mcq("A map has the scale 1:50" + NBSP + "000. A park covers 8 cm² on the map. What is the real area of the park?",
                   A(2, "km"), [A(4, "km"), A(F(1, 4), "km"), A(64, "km")],
                   "1 cm stands for 0.5 km, so 1 cm² stands for 0.5 × 0.5 = 0.25 km². 8 × 0.25 = <b>2 km²</b>. "
                   "4 km² multiplies 8 by 0.5 only once, and 0.25 km² is just one square centimetre.", value=8 * F(1, 4)))
    its.append(mcq("A patio has an area of 24 m². How much area does it cover on a plan with the scale 1 cm : 2 m?",
                   A(6, "cm"), [A(12, "cm"), A(48, "cm"), A(96, "cm")],
                   "Each 1 cm² stands for 2 × 2 = 4 m². 24 ÷ 4 = <b>6 cm²</b>. 12 cm² divides by 2 only once, "
                   "and 48 and 96 multiply instead of dividing.", value=F(24, 4)))
    its.append(mcq("A plan has the scale 1:50. A room covers 40 cm² on the plan. What is the real area of the room?",
                   A(10, "m"), [A(F(1, 5), "m"), A(2000, "m"), A(40, "m")],
                   "1 cm² stands for 50 × 50 = 2500 cm². 40 × 2500 = 100" + NBSP + "000 cm² = <b>10 m²</b> "
                   "(1 m² = 10" + NBSP + "000 cm²). 0.2 m² multiplies by 50 only once.", value=F(40 * 2500, 10000)))
    its.append(mcq("The same garden is drawn at 1:100 and at 1:200. How does its area on the 1:200 drawing compare with its area on the 1:100 drawing?",
                   fr(1, 4) + " as large", [fr(1, 2) + " as large", "2 times as large", "4 times as large"],
                   "At 1:200 every length is half as long as at 1:100. The area is " + fr(1, 2) + " × " + fr(1, 2) + " = <b>"
                   + fr(1, 4) + " as large</b>. " + fr(1, 2) + " scales the area like a length."))
    its.append(mcq("A photo 10 cm by 15 cm is enlarged so that every length is twice as long. What is the area of the new photo?",
                   A(600, "cm"), [A(300, "cm"), A(150, "cm"), A(2400, "cm")],
                   "New photo: 20 cm by 30 cm = <b>600 cm²</b>, which is 2 × 2 = 4 times the old 150 cm². "
                   "300 cm² only doubles the area.", value=20 * 30))
    its.append(mcq("Drawing B of a room has 4 times the area of drawing A. How many times as long is each side in drawing B?",
                   "2", ["4", "16", fr(1, 4)],
                   "Area grows by the square of the length factor. 2 × 2 = 4, so each side is <b>2</b> times as long. "
                   "4 would make the area 16 times as large.", value=2))
    its.append(mcq("A rectangular lot is 20 m by 15 m. What area does it cover on a 1:500 plan?",
                   A(12, "cm"), [A(F(3, 5), "cm"), A(60, "cm"), A(F(6, 5), "cm")],
                   "20 m = 2000 cm and 15 m = 1500 cm. On the plan: 2000 ÷ 500 = 4 cm and 1500 ÷ 500 = 3 cm. "
                   "Area: 4 × 3 = <b>12 cm²</b>. 0.6 divides 300 m² by 500 only once.", value=4 * 3))
    its.append(mcq(fig(rect_svg(6, 4, "shed floor")) + "The scale is 1:50. What is the area of the real shed floor?",
                   A(6, "m"), [A(F(12, 100), "m"), A(1200, "m"), A(24, "m")],
                   "Real sides: 6 × 50 = 300 cm = 3 m and 4 × 50 = 200 cm = 2 m. Area: 3 × 2 = <b>6 m²</b>. "
                   "0.12 m² multiplies 24 cm² by 50 only once.", value=3 * 2))
    its.append(mcq("A rug is 2 m by 3 m. Kai draws it on a plan with the scale 1 cm : 0.5 m. What area does the rug cover on the plan?",
                   A(24, "cm"), [A(12, "cm"), A(3, "cm"), A(F(3, 2), "cm")],
                   "On the plan: 2 ÷ 0.5 = 4 cm and 3 ÷ 0.5 = 6 cm. Area: 4 × 6 = <b>24 cm²</b>. "
                   "12 cm² divides the 6 m² by 0.5 only once, and 1.5 cm² multiplies by 0.5 × 0.5.", value=4 * 6))
    its.append(mcq("A plan uses the scale 1 cm : 10 m. A field covers 5 cm² on the plan. What is the real area of the field?",
                   A(500, "m"), [A(50, "m"), A(5, "m"), A(25, "m")],
                   "Each 1 cm² stands for 10 × 10 = 100 m². 5 × 100 = <b>500 m²</b>. 50 m² multiplies by 10 only once.",
                   value=5 * 100))
    its.append(mcq("A rectangular room has an area of 72 m², and its long side is 12 m. How wide is the room on a 1:200 plan?",
                   L(3, "cm"), [L(6, "cm"), L(F(36, 100), "cm"), L(36, "cm")],
                   "Real width: 72 ÷ 12 = 6 m = 600 cm. On the plan: 600 ÷ 200 = <b>3 cm</b>. 6 cm is the long side on the plan "
                   "(1200 ÷ 200), and 0.36 cm divides the area by 200.", value=F(600, 200)))
    assert len(its) == 20, len(its)
    return {"title": "Areas from scale drawings: area scales by the square", "items": its}


# ============================================================ set 5: word problems
def set_problems():
    its = []
    its.append(mcq("Zoe’s family plans a canoe trip in Algonquin Park. On a 1:50" + NBSP + "000 map, the route is 9 cm long. "
                   "They paddle at about 3 km/h. About how long will the trip take?",
                   "1.5 h", ["15 h", "3 h", "4.5 h"],
                   "Real route: 9 × 50" + NBSP + "000 = 450" + NBSP + "000 cm = 4.5 km. Time: 4.5 ÷ 3 = <b>1.5 h</b>. "
                   "15 h comes from 45 km (a units slip), and 4.5 is the distance, not the time.", value=F(9 * 50000, 100000) / 3))
    its.append(mcq("A bedroom is 8 cm by 7 cm on a plan with the scale 1 cm : 0.5 m. Carpet costs $30 per square metre. "
                   "What does carpet for the whole floor cost?",
                   "$420", ["$840", "$1680", "$450"],
                   "Real room: 4 m by 3.5 m = 14 m². 14 × $30 = <b>$420</b>. $840 scales the 56 cm² by 0.5 only once, "
                   "$1680 forgets the scale, and $450 uses the perimeter (15 m).", value=14 * 30))
    its.append(mcq("A Toronto street map uses the scale 1 cm : 250 m. Arjun’s school and the library are 12 cm apart on the map. "
                   "How far apart are they really?",
                   L(3, "km"), [L(30, "km"), L(300, "m"), L(3000, "km")],
                   "12 × 250 = 3000 m = <b>3 km</b>. 300 m drops a zero, and 30 km adds one.", value=F(12 * 250, 1000)))
    its.append(mcq("A real canoe is 5 m long. Owen builds a model at a scale of 1:20. How long is the model?",
                   L(25, "cm"), [L(100, "cm"), L(F(5, 2), "cm"), L(F(1, 4), "cm")],
                   "5 m = 500 cm. 500 ÷ 20 = <b>25 cm</b>. 100 cm multiplies 5 by 20, "
                   "and 2.5 cm divides by 200.", value=F(500, 20)))
    its.append(mcq("Emma draws her vegetable garden as a 6 cm by 4 cm rectangle with the scale 1 cm : 0.5 m. "
                   "Fencing costs $12 per metre. What does a fence all the way around cost?",
                   "$120", ["$240", "$72", "$288"],
                   "Real garden: 3 m by 2 m. Perimeter: 2 × (3 + 2) = 10 m. 10 × $12 = <b>$120</b>. "
                   "$240 uses the 20 cm perimeter on the drawing, $72 uses the 6 m² area, and $288 uses 24 cm².", value=10 * 12))
    its.append(mcq("An elevation drawing of a wall has the scale 1:50. The wall is 8 cm by 5 cm on the drawing. "
                   "What is the real area of the wall to be painted?",
                   A(10, "m"), [A(F(1, 5), "m"), A(2000, "m"), A(26, "m")],
                   "Real wall: 8 × 50 = 400 cm = 4 m and 5 × 50 = 250 cm = 2.5 m. Area: 4 × 2.5 = <b>10 m²</b>. "
                   "0.2 m² multiplies 40 cm² by 50 only once, and 26 is a perimeter in centimetres.", value=4 * F(5, 2)))
    its.append(mcq("Two towns are 6 cm apart on a 1:100" + NBSP + "000 map. How far apart are they on a 1:250" + NBSP + "000 map?",
                   L(F(12, 5), "cm"), [L(15, "cm"), L(6, "cm"), L(F(18, 5), "cm")],
                   "Real distance: 6 × 100" + NBSP + "000 cm = 6 km. On the new map: 600" + NBSP + "000 ÷ 250" + NBSP + "000 = <b>2.4 cm</b>. "
                   "15 cm makes the distance bigger, but 1:250" + NBSP + "000 is a smaller scale.", value=F(600000, 250000)))
    its.append(mcq("Hana draws a 60 m by 26 m hockey rink at the scale 1 cm : 2 m on a sheet 21.6 cm by 27.9 cm. "
                   "Will the drawing fit?",
                   "No: it would be 30 cm long", ["Yes: it would be 15 cm long", "Yes: it would be 6 cm long", "No: it would be 120 cm long"],
                   "60 ÷ 2 = 30 cm, which is longer than 27.9 cm, so <b>no</b>. 120 cm multiplies by 2, "
                   "15 cm divides 60 by 4, and 6 cm divides 60 by 10."))
    its.append(mcq("A cottage plan has the scale 1:100. The living room is 5.5 cm by 4 cm on the plan. What is its real area?",
                   A(22, "m"), [A(F(22, 100), "m"), A(2200, "m"), A(19, "m")],
                   "Real room: 5.5 m by 4 m. Area: 5.5 × 4 = <b>22 m²</b>. 0.22 m² multiplies 22 cm² by 100 only once, "
                   "and 19 is the real perimeter.", value=F(11, 2) * 4))
    its.append(mcq(fig(scale_bar_svg(4, 2, "km", 4)) + "Jayden’s hike is 7 cm long on this trail map. How long is the real hike?",
                   L(F(7, 2), "km"), [L(14, "km"), L(F(7, 4), "km"), L(F(7, 20), "km")],
                   "The bar shows 4 cm for 2 km, so 1 cm stands for 0.5 km. 7 × 0.5 = <b>3.5 km</b>. "
                   "14 km multiplies 7 by the whole bar, and 1.75 km divides 7 by 4.", value=7 * F(1, 2)))
    its.append(mcq("A building lot is 6 cm by 9 cm on a 1:500 plan. What is the real area of the lot?",
                   A(1350, "m"), [A(27000, "m"), A(270, "m"), A(150, "m")],
                   "Real lot: 6 × 5 m = 30 m and 9 × 5 m = 45 m. Area: 30 × 45 = <b>1350 m²</b>. "
                   "27" + NBSP + "000 m² multiplies 54 cm² by 500 and keeps the wrong unit, and 150 is the real perimeter.",
                   value=30 * 45))
    its.append(mcq("A classroom is 9 m long. On Benjamin’s plan it is 18 cm long. What scale did he use?",
                   R(1, 50), [R(1, 2), R(2, 1), R(1, 500)],
                   "Use the same unit: 9 m = 900 cm. 18 : 900 = 1 : 50, so the scale is <b>1:50</b>. "
                   "1:2 and 2:1 compare 18 and 9 without changing the units."))
    its.append(mcq("Two towns 24 km apart are 8 cm apart on a map. What is the scale of the map?",
                   R(1, 300000), [R(1, 3), R(1, 3000), R(1, 30000)],
                   "8 cm stands for 24 km, so 1 cm stands for 3 km = 300" + NBSP + "000 cm. The scale is <b>1:300" + NBSP + "000</b>. "
                   "1:3 forgets to change km into cm."))
    its.append(mcq("Priya’s model of her school has the scale 1:200. The gym floor is 15 cm by 10 cm on the model. "
                   "What is the area of the real gym floor?",
                   A(600, "m"), [A(3, "m"), A(30000, "m"), A(100, "m")],
                   "Real gym: 15 × 200 = 3000 cm = 30 m and 10 × 200 = 2000 cm = 20 m. Area: 30 × 20 = <b>600 m²</b>. "
                   "3 m² multiplies 150 cm² by 200 only once, and 100 is the real perimeter.", value=30 * 20))
    its.append(mcq("A city park plan has the scale 1:1000. A soccer field is 10 cm by 6.5 cm on the plan. "
                   "What is the area of the real field?",
                   A(6500, "m"), [A(65, "m"), A(65000, "m"), A(330, "m")],
                   "1 cm stands for 1000 cm = 10 m. Real field: 100 m by 65 m. Area: 100 × 65 = <b>6500 m²</b>. "
                   "65 m² treats each 1 cm² as 1 m², 65" + NBSP + "000 m² multiplies 65 by 1000, and 330 is the real perimeter.", value=100 * 65))
    its.append(mcq("Maya enlarges a 4 cm by 6 cm photo of a loon so that the 4 cm side becomes 12 cm. How long is the other side now?",
                   L(18, "cm"), [L(14, "cm"), L(54, "cm"), L(12, "cm")],
                   "4 cm became 12 cm, so the scale factor is 12 ÷ 4 = 3. 6 × 3 = <b>18 cm</b>. "
                   "14 cm adds 8 to both sides, and 54 cm multiplies by 9, the area factor.", value=6 * 3))
    its.append(mcq("On a 1:5" + NBSP + "000" + NBSP + "000 map, Toronto and Montréal are about 10 cm apart. About how far apart are they in a straight line?",
                   L(500, "km"), [L(50, "km"), L(5000, "km"), L(F(1, 2), "km")],
                   "10 × 5" + NBSP + "000" + NBSP + "000 = 50" + NBSP + "000" + NBSP + "000 cm = 500" + NBSP + "000 m = <b>500 km</b>. "
                   "50 km and 5000 km slip by a factor of 10.", value=F(10 * 5000000, 100000)))
    its.append(mcq("A kitchen is 6 cm by 5 cm on a plan with the scale 1 cm : 0.5 m. Each floor tile is 0.5 m by 0.5 m. "
                   "How many tiles cover the floor?",
                   "30", ["15", "8", "60"],
                   "Real kitchen: 3 m by 2.5 m, so 6 tiles by 5 tiles = <b>30</b> tiles. Each 1 cm square on the plan is one tile. "
                   "15 multiplies 30 cm² by 0.5, and 8 rounds up the 7.5 m² area.", value=30))
    its.append(mcq("A sugar shack has a floor area of 48 m². How much area does the floor cover on a 1:400 plan?",
                   A(3, "cm"), [A(12, "cm"), A(F(12, 100), "cm"), A(192, "cm")],
                   "1 cm stands for 400 cm = 4 m, so 1 cm² stands for 4 × 4 = 16 m². 48 ÷ 16 = <b>3 cm²</b>. "
                   "12 cm² divides by 4 only once, and 192 multiplies instead of dividing.", value=F(48, 16)))
    its.append(mcq("Amira’s map has the scale 1:25" + NBSP + "000 and Lucas’s map has the scale 1:50" + NBSP + "000. "
                   "A lake covers 3 cm² on Lucas’s map. How much area does it cover on Amira’s map?",
                   A(12, "cm"), [A(6, "cm"), A(F(3, 2), "cm"), A(F(3, 4), "cm")],
                   "Amira’s map is twice as large in every length, so areas are 2 × 2 = 4 times as large: 3 × 4 = <b>12 cm²</b>. "
                   "6 cm² doubles the area only once, and 1.5 cm² and 0.75 cm² make it smaller.", value=12))
    assert len(its) == 20, len(its)
    return {"title": "Word problems: maps, floor plans and models", "items": its}


# ============================================================ lesson
def body_html():
    f_bar = scale_bar_svg(4, 20, "m", 4)
    f_rect = rect_svg(4, 3, "patio")
    f_area = area_svg()
    return (
        "<h2>What a scale means</h2>"
        "<p>A <b>scale drawing</b> has the same shape as the real object, but every length is multiplied by the same number. "
        "The <b>scale</b> tells you how a length on the drawing compares with the real length. The drawing always comes first.</p>"
        "<p>A scale can have units, like <b>1 cm : 5 m</b>, or no units, like <b>1:500</b>. With no units, both parts use the "
        "same unit: 1 cm stands for 500 cm, which is 5 m.</p>"
        "<figure class='sn-fig'>" + f_bar +
        "<figcaption>A scale bar. The bar is 4 cm long and stands for 20 m, so 1 cm stands for 5 m. "
        "The scale is 1 cm : 5 m, or 1:500.</figcaption></figure>"
        + ex("Change to a ratio", "Write 1 cm : 2 m as a ratio with no units.",
             "Use one unit: 2 m = 200 cm. So 1 cm : 200 cm.", "1:200")
        + "<h2>Actual lengths and drawing lengths</h2>"
        "<p>Drawing to real: <b>multiply</b> by the scale. Real to drawing: <b>divide</b>. Then check the units: "
        "1 m = 100 cm and 1 km = 100" + NBSP + "000 cm.</p>"
        "<figure class='sn-fig'>" + f_rect +
        "<figcaption>At 1 cm : 2 m, the 4 cm side stands for 4 × 2 = 8 m, and the 3 cm side stands for 3 × 2 = 6 m.</figcaption></figure>"
        + ex("Drawing to real", "A map has the scale 1:50" + NBSP + "000. Two lakes are 4 cm apart on the map. How far apart are they?",
             "4 × 50" + NBSP + "000 = 200" + NBSP + "000 cm = 2000 m.", "2 km")
        + ex("Real to drawing", "A room is 6 m long. How long is it on a 1:50 plan?",
             "6 m = 600 cm. 600 ÷ 50 = 12.", "12 cm")
        + "<p>To <b>redraw at a new scale</b>, find the real length first, then use the new scale. "
        "6 cm at 1:100 is 600 cm in real life; at 1:200 it becomes 600 ÷ 200 = 3 cm.</p>"
        + "<h2>Area scales by the square</h2>"
        "<p>When every length is multiplied by k, the area is multiplied by <b>k × k</b>. "
        "So change the lengths first, then find the area.</p>"
        "<figure class='sn-fig'>" + f_area +
        "<figcaption>At 1 cm : 2 m, 1 cm² on the drawing stands for 2 m × 2 m = 4 m², not 2 m².</figcaption></figure>"
        + ex("Area", "A deck is 4 cm by 3 cm on a plan with the scale 1 cm : 2 m. What is its real area?",
             "Real sides: 8 m and 6 m. Area: 8 × 6 = 48 m². (The drawing area 12 cm² × 4 = 48 also works.)", "48 m²")
        + "<h2>Common mistakes</h2>"
        + table(["Mistake", "What to do instead"], [
            ["1:500, so 1 cm is 500 m", "Both parts use the same unit: 1 cm is 500 cm = 5 m"],
            ["Scale 1 cm : 2 m, wall 10 m, so draw 20 cm", "Real to drawing means divide: 10 ÷ 2 = 5 cm"],
            ["6 × 50" + NBSP + "000 = 300" + NBSP + "000, so 300 km", "300" + NBSP + "000 cm = 3000 m = 3 km"],
            ["Drawing area 12 cm² at 1 cm : 2 m is 24 m²", "Area grows by 2 × 2 = 4: 12 × 4 = 48 m²"],
            ["1:500 has a bigger number, so it is a bigger drawing", "1:50 makes a larger drawing than 1:500"],
        ])
    )


FAQ = [
    {"q": "What do Grade 8 students learn about scale drawings in Ontario?",
     "a": "In the Ontario Grade 8 math curriculum, students use scale drawings to calculate actual lengths and areas, and they redraw scale drawings at different ratios. Maps, floor plans and models are the usual contexts."},
    {"q": "How do you find the actual length from a scale drawing?",
     "a": "Multiply the length on the drawing by the scale, then change the units. At 1:200, a 6 cm wall is 6 × 200 = 1200 cm, which is 12 m."},
    {"q": "Why does the area not scale by the same number as the lengths?",
     "a": "Area uses two lengths, and both are multiplied by the scale. At 1 cm : 2 m, each 1 cm² stands for 2 m × 2 m = 4 m², so areas grow 4 times as fast as the scale number."},
    {"q": "How do you write 1 cm : 2 m as a ratio scale?",
     "a": "Change both parts to the same unit and drop the units: 2 m = 200 cm, so 1 cm : 2 m is the ratio 1:200."},
]


def mark_large(u, pattern):
    """Tag wide pictures so they print larger and stay readable."""
    rx = re.compile(r"<svg (?=[^>]*aria-label='" + pattern + ")")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u


def gen():
    rnd = random.Random(48815)
    sets = [set_read(), set_actual(), set_drawing(), set_area(), set_problems()]
    seen = set()
    for s in sets:
        assert len(s["items"]) == 20, (s["title"], len(s["items"]))
        for it in s["items"]:
            assert len(set(it["c"])) == 4, it
            assert it["q"].count("<svg") <= 1, it["q"]
            k = plain(it["q"]) + "|" + "|".join(sorted(it["c"]))
            assert k not in seen, it["q"]
            seen.add(k)
    balance(sets, rnd)
    for s in sets:
        assert sorted(it["a"] for it in s["items"]) == sorted([0, 1, 2, 3] * 5)
    u = {
        "country": "ca-on", "subject": "math", "grade": "grade-8", "slug": SLUG, "sort": 15,
        "updated": UPDATED, "pdf_url": "",
        "title": "Scale Drawings: Actual Lengths, Areas, Maps and Floor Plans",
        "seo_title": "Grade 8 Scale Drawings Worksheets (Ontario Math): Free with Answer Key",
        "short_title": "Scale drawings",
        "domain": "Spatial Sense",
        "standard_code": "Grade 8: E1.3",
        "standard_url": "https://www.dcp.edu.gov.on.ca/en/curriculum/elementary-mathematics",
        "standard_text": "Use scale drawings to calculate actual lengths and areas, and reproduce scale drawings at different ratios",
        "meta_desc": "Free Grade 8 scale drawing worksheets for the Ontario curriculum: read scales like 1 cm : 2 m and 1:500, find actual and drawing lengths, redraw at a new scale, and find real areas from maps and floor plans. 100 math questions with an answer key.",
        "key_big": "Drawing to real: multiply by the scale. Real to drawing: divide. Area grows by the scale squared.",
        "key_sub": "1:500 means 1 cm stands for 500 cm = 5 m. At 1 cm : 2 m, 1 cm² stands for 2 × 2 = 4 m², not 2 m².",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }
    return mark_large(u, "(scale bar)")


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
