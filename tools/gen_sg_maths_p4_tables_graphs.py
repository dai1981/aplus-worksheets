# -*- coding: utf-8 -*-
"""
Singapore Primary 4 Maths: Tables, line graphs and pie charts
(MOE 2021 Primary Mathematics Syllabus, Standard, Primary 4: Statistics —
 completing a table from given data; reading and interpreting data from tables, line graphs and pie charts)
  python3 tools/gen_sg_maths_p4_tables_graphs.py
Tables with totals and missing values, line graphs (scale, values between gridlines), trends and changes,
simple pie charts (halves, quarters, eighths) and word problems with bar models.
Numbers: 4-digit numbers have no separator (2400); 5 or more digits use a no-break space. Never commas.
Wrong answers come from real mistakes: misreading the scale (counting each gridline gap as 1), reading the wrong
row or column, adding when the question asks for a difference, subtracting without renaming, taking the highest
point for the greatest increase, and thinking a bigger slice means a bigger number when the totals differ.
Every figure is drawn exactly from its data. HTML attributes use single quotes (no backslashes in the JSON).
"""
import json, re, math, os, random
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "sg", "maths", "primary-4")
UPDATED = "2026-11-03"
GREEN = "#006633"
LINE1 = "#2e8b57"
LINE2 = "#c0392b"
RED = "#c0392b"
INK = "#2b2b2b"
GRID = "#d5ddd8"
GRID2 = "#9fb0a5"
FILL = "#cfe6d6"
FILL2 = "#e6f2ea"
FONT = "Arial, Helvetica, sans-serif"
PALETTE = ["#8fc9a3", "#f2d16b", "#9cbfe8", "#f0a58f", "#c9bde6", "#d7dcd9"]
NB = " "
MINUS = "−"


# ------------------------------------------------------------ helpers
def fr(a, b):
    return "<span class='fr'><span class='fn'>%s</span><span class='fd'>%s</span></span>" % (a, b)


def frs(x):
    x = F(x)
    if x.denominator == 1:
        return str(x.numerator)
    return fr(x.numerator, x.denominator)


def n(x):
    """MOE style: 2400, 10 000 (no-break spaces, never commas)."""
    s = str(abs(int(x)))
    if len(s) > 4:
        g = []
        while s:
            g.insert(0, s[-3:])
            s = s[:-3]
        s = NB.join(g)
    return (MINUS if x < 0 else "") + s


def num(x):
    x = F(x)
    if x.denominator == 1:
        return n(x.numerator)
    d = x * 100
    assert d.denominator == 1, x
    v = int(d)
    return "%s.%02d" % (n(v // 100), v % 100)


def money(x):
    return "$" + num(x)


def unit(v, one, many):
    return "%s %s" % (num(v), one if F(v) == 1 else many)


def plain(s):
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", s)).strip()


def mcq(q, right, wrongs, e):
    """right + 3 wrongs (already formatted). balance() moves the answer."""
    ch = [right]
    for w in wrongs:
        if plain(w) not in {plain(c) for c in ch}:
            ch.append(w)
        if len(ch) == 4:
            break
    assert len(ch) == 4, (q, right, wrongs)
    return {"q": q, "c": ch, "a": 0, "e": e}


def mcqv(q, right, wrongs, f, e, allow_zero=False):
    """Choices given as values: equal values are dropped (no two choices equal in value)."""
    seen = [F(right)]
    pick = []
    for w in wrongs:
        w = F(w)
        if w in seen or (w <= 0 and not allow_zero):
            continue
        seen.append(w)
        pick.append(w)
        if len(pick) == 3:
            break
    assert len(pick) == 3, (q, right, wrongs)
    return mcq(q, f(right), [f(w) for w in pick], e)


def fig(svg):
    return "<div class='qfig'>" + svg + "</div>"


def svg_wrap(x0, y0, w, h, body, label):
    return ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='%d %d %d %d' width='%d' height='%d' "
            "role='img' aria-label='%s'><g font-family='%s'>%s</g></svg>" % (x0, y0, w, h, w, h, label, FONT, body))


def tw(t, fs, bold=False):
    """Approximate text width in px (Arial)."""
    return len(str(t)) * fs * (0.62 if bold else 0.58)


def text(x, y, t, fs=14, anchor="middle", bold=False, col=INK, extra=""):
    return ("<text x='%.1f' y='%.1f' font-size='%d'%s fill='%s' text-anchor='%s'%s>%s</text>"
            % (x, y, fs, " font-weight='700'" if bold else "", col, anchor, extra, t))


STU = lambda v: unit(v, "student", "students")


# ------------------------------------------------------------ tables (SVG)
def table_svg(title, head, rows, label=None):
    """Data table drawn as SVG. A cell '?' is a red question mark. A row starting with 'Total' is bold."""
    fs, rh = 15, 28
    ncol = len(head)
    cols = []
    for k in range(ncol):
        cells = [head[k]] + [str(r[k]) for r in rows]
        cols.append(int(max(max(tw(plain(c), fs, True) for c in cells) + 22, 58 if k else 70)))
    top = 30
    tot = sum(cols)
    W = int(max(tot + 8, tw(title, 16, True) + 16))
    x0 = (W - tot) / 2.0
    s = [text(W / 2.0, 19, title, 16, bold=True)]
    allrows = [head] + rows
    for r, row in enumerate(allrows):
        y = top + r * rh
        hd = r == 0
        totrow = str(row[0]) == "Total"
        x = x0
        for k, cw in enumerate(cols):
            s.append("<rect x='%.1f' y='%d' width='%d' height='%d' fill='%s' stroke='%s' stroke-width='1.5'/>"
                     % (x, y, cw, rh, FILL2 if hd or k == 0 or totrow else "#ffffff", GREEN))
            c = str(row[k])
            if c == "?":
                s.append(text(x + cw / 2.0, y + 20, "?", 17, bold=True, col=RED))
            elif k == 0:
                s.append(text(x + 10, y + 19, c, fs, anchor="start", bold=hd or totrow))
            else:
                s.append(text(x + cw / 2.0, y + 19, c, fs, bold=hd or totrow))
            x += cw
    H = top + len(allrows) * rh + 4
    return svg_wrap(0, 0, W, H, "".join(s), label or "table: " + title.lower())


# ------------------------------------------------------------ pie charts
class Pie:
    """cats with parts out of n equal slices (n = parts total). Drawn from 12 o’clock, clockwise."""
    def __init__(self, title, cats, parts, ticks=True):
        self.title, self.cats, self.parts = title, cats, parts
        self.n = sum(parts)
        self.ticks = ticks
        self.fills = PALETTE[:len(cats)]
        assert len(set(cats)) == len(cats)

    def frac(self, *names):
        return F(sum(self.parts[self.cats.index(c)] for c in names), self.n)

    def p(self, c):
        return self.parts[self.cats.index(c)]


def pie_parts(p, R=58, fs=14):
    s = []
    a0 = 0.0
    pt = lambda a, r: (r * math.sin(math.radians(a)), -r * math.cos(math.radians(a)))
    boxes = []
    for i, (c, k) in enumerate(zip(p.cats, p.parts)):
        a1 = a0 + 360.0 * k / p.n
        x1, y1 = pt(a0, R)
        x2, y2 = pt(a1, R)
        large = 1 if a1 - a0 > 180 else 0
        s.append("<path d='M0 0 L%.2f %.2f A%d %d 0 %d 1 %.2f %.2f Z' fill='%s'/>"
                 % (x1, y1, R, R, large, x2, y2, p.fills[i]))
        am = (a0 + a1) / 2
        sn, cs = math.sin(math.radians(am)), math.cos(math.radians(am))
        rl = R + 7 + 5 * abs(cs)
        lx, ly = sn * rl, -cs * rl + 5
        lab = c
        w = tw(lab, fs)
        if sn > 0.3:
            anc, bx = "start", lx
        elif sn < -0.3:
            anc, bx = "end", lx - w
        else:
            anc, bx = "middle", lx - w / 2
        boxes.append((bx, ly - 11, bx + w, ly + 3, lab))
        s.append(text(lx, ly, lab, fs, anchor=anc))
        a0 = a1
    if p.ticks:
        for k in range(p.n):
            x, y = pt(360.0 * k / p.n, R)
            s.append("<line x1='0' y1='0' x2='%.2f' y2='%.2f' stroke='%s' stroke-opacity='0.45' stroke-width='0.9' "
                     "stroke-dasharray='3 2'/>" % (x, y, INK))
    a0 = 0.0
    for k in p.parts:
        x, y = pt(a0, R)
        s.append("<line x1='0' y1='0' x2='%.2f' y2='%.2f' stroke='%s' stroke-width='1.6'/>" % (x, y, INK))
        a0 += 360.0 * k / p.n
    s.append("<circle cx='0' cy='0' r='%d' fill='none' stroke='%s' stroke-width='1.8'/>" % (R, INK))
    for i in range(len(boxes)):
        for j in range(i + 1, len(boxes)):
            a, b = boxes[i], boxes[j]
            assert a[2] + 3 < b[0] or b[2] + 3 < a[0] or a[3] + 1 < b[1] or b[3] + 1 < a[1], (p.title, a, b)
    xs = [b[0] for b in boxes] + [-R - 2]
    xe = [b[2] for b in boxes] + [R + 2]
    ys = [b[1] for b in boxes] + [-R - 2]
    ye = [b[3] for b in boxes] + [R + 2]
    ty = min(ys) - 10
    s.append(text(0, ty, p.title, 15, bold=True))
    tww = tw(p.title, 15, True)
    bbox = (min(min(xs), -tww / 2), ty - 14, max(max(xe), tww / 2), max(ye))
    return "".join(s), bbox


def pie_svg(*pies):
    parts = [pie_parts(p) for p in pies]
    x = 0.0
    top = min(b[1] for _, b in parts)
    bot = max(b[3] for _, b in parts)
    body = []
    for el, b in parts:
        dx = x - b[0]
        body.append("<g transform='translate(%.1f 0)'>%s</g>" % (dx, el))
        x += (b[2] - b[0]) + 30
    W = x - 30
    lab = ("pie charts: " if len(pies) > 1 else "pie chart: ") + " and ".join(p.title.lower() for p in pies)
    return svg_wrap(-6, int(math.floor(top)) - 4, int(math.ceil(W)) + 12, int(math.ceil(bot - top)) + 10, "".join(body), lab)


# ------------------------------------------------------------ line graphs
class LG:
    def __init__(self, title, xl, xt, yt, series, ymin, ymax, lstep, gstep, names=None, f=num):
        self.title, self.xl, self.xt, self.yt = title, xl, xt, yt
        self.series, self.ymin, self.ymax, self.lstep, self.gstep = series, ymin, ymax, lstep, gstep
        self.names, self.f = names, f
        for v in series:
            assert len(v) == len(xl)
            assert all(ymin <= x <= ymax for x in v)
            # every point sits on a gridline or halfway between two gridlines
            assert all(F(x - ymin, gstep).denominator in (1, 2) for x in v), v
        assert (ymax - ymin) % gstep == 0 and lstep % gstep == 0 and ymin % lstep == 0

    def v(self, x):
        return self.f(x)

    def at(self, label, si=0):
        return self.series[si][self.xl.index(label)]

    def svg(self):
        fs = 14
        nt = (self.ymax - self.ymin) // self.gstep
        gy = max(9, min(20, int(round(150.0 / nt))))
        ph = nt * gy
        ylabs = [num(v) for v in range(self.ymin, self.ymax + 1, self.lstep)]
        slot = max(46, max(tw(c, fs) for c in self.xl) + 10)
        x0 = 24 + max(tw(c, fs) for c in ylabs) + 8
        nx = len(self.xl)
        pw = slot * (nx - 1)
        y0 = 34 + (22 if self.names else 0)
        yb = y0 + ph
        W = x0 + pw + tw(self.xl[-1], fs) / 2 + 8
        W = max(W, tw(self.title, 16, True) + 16)
        s = [text(W / 2, 18, self.title, 16, bold=True)]
        Y = lambda v: yb - (v - self.ymin) / float(self.gstep) * gy
        for k in range(nt + 1):
            v = self.ymin + k * self.gstep
            major = v % self.lstep == 0
            s.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='%s'/>"
                     % (x0, Y(v), x0 + pw, Y(v), GRID2 if major else GRID, "1" if major else "0.8"))
            if major:
                s.append(text(x0 - 5, Y(v) + 5, num(v), fs, anchor="end"))
        for i, c in enumerate(self.xl):
            x = x0 + slot * i
            s.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='1'/>" % (x, y0, x, yb, GRID2))
            s.append(text(x, yb + 18, c, fs))
        s.append("<path d='M%.1f %d V%.1f H%.1f' fill='none' stroke='%s' stroke-width='2'/>" % (x0, y0 - 6, yb, x0 + pw + 4, INK))
        for si, vals in enumerate(self.series):
            col = LINE1 if si == 0 else LINE2
            dash = "" if si == 0 else " stroke-dasharray='7 4'"
            pts = [(x0 + slot * i, Y(v)) for i, v in enumerate(vals)]
            s.append("<polyline points='%s' fill='none' stroke='%s' stroke-width='2.5'%s/>"
                     % (" ".join("%.1f,%.1f" % p for p in pts), col, dash))
            for p in pts:
                if si == 0:
                    s.append("<circle cx='%.1f' cy='%.1f' r='3.8' fill='%s'/>" % (p[0], p[1], GREEN))
                else:
                    s.append("<rect x='%.1f' y='%.1f' width='7' height='7' fill='%s'/>" % (p[0] - 3.5, p[1] - 3.5, LINE2))
        if self.names:
            ws = [tw(nm, fs) for nm in self.names]
            tot = sum(ws) + 2 * 34 + 24
            x = (W - tot) / 2
            for si, nm in enumerate(self.names):
                col = LINE1 if si == 0 else LINE2
                dash = "" if si == 0 else " stroke-dasharray='7 4'"
                s.append("<line x1='%.1f' y1='38' x2='%.1f' y2='38' stroke='%s' stroke-width='2.5'%s/>" % (x, x + 26, col, dash))
                s.append(text(x + 32, 43, nm, fs, anchor="start"))
                x += 34 + ws[si] + 24
        s.append(text(x0 + pw / 2, yb + 38, self.xt, fs, bold=True))
        mid = y0 + ph / 2
        s.append(text(13, mid, self.yt, fs, bold=True, extra=" transform='rotate(-90 13 %.1f)'" % mid))
        assert tw(self.yt, fs, True) < ph + 30, (self.yt, ph)
        H = yb + 44
        return svg_wrap(0, 0, int(math.ceil(W)), int(H), "".join(s), "line graph: " + self.title.lower())


# ------------------------------------------------------------ bar models
SEGFILL = {"u": FILL, "o": "#e3e3e3", "w": "#ffffff"}


def model_svg(rows, top=None, under=(), right=None, BW=300, label="bar model"):
    """Bar model drawn to scale.
    rows: [(name, [(value, text, style)])], style u (unit, green), o (other, grey), w (white).
    top: (v0, v1, text) bracket over row 0; under: [(row, v0, v1, text)] brackets under a row;
    right: text for a bracket on the right joining all rows. Text '?' is drawn in red."""
    names = [nm for nm, _ in rows]
    nw = max([tw(nm, 15) for nm in names] + [0])
    x0 = 8 + (nw + 10 if nw else 0)
    maxv = max(sum(v for v, _, _ in segs) for _, segs in rows)
    sc = BW / float(maxv)
    bh = 32
    out = []
    y = 38 if top else 8
    ys = []
    for i in range(len(rows)):
        ys.append(y)
        y += bh + (38 if any(u[0] == i for u in under) else 16)
    Hh = y - 16 + 8 if not any(u[0] == len(rows) - 1 for u in under) else y - 38 + 44
    col = lambda t: RED if t == "?" else INK
    for i, (nm, segs) in enumerate(rows):
        ry = ys[i]
        if nm:
            out.append(text(8, ry + 22, nm, 15, anchor="start", bold=True))
        x = x0
        for v, t, st in segs:
            w = v * sc
            out.append("<rect x='%.1f' y='%d' width='%.1f' height='%d' fill='%s' stroke='%s' stroke-width='2'/>"
                       % (x, ry, w, bh, SEGFILL[st], GREEN))
            if t:
                assert tw(t, 15) + 4 <= w, (t, w)
                out.append(text(x + w / 2, ry + 22, t, 15, bold=True, col=col(t)))
            x += w
    if top:
        v0, v1, t = top
        a, b = x0 + v0 * sc, x0 + v1 * sc
        ry = ys[0]
        out.append("<path d='M%.1f %d V%d H%.1f V%d' fill='none' stroke='%s' stroke-width='2'/>" % (a, ry - 4, ry - 11, b, ry - 4, INK))
        out.append(text((a + b) / 2, ry - 16, t, 16, bold=True, col=col(t)))
    for r, v0, v1, t in under:
        a, b = x0 + v0 * sc, x0 + v1 * sc
        yb = ys[r] + bh
        out.append("<path d='M%.1f %d V%d H%.1f V%d' fill='none' stroke='%s' stroke-width='2'/>"
                   % (a, yb + 4, yb + 11, b, yb + 4, RED if t == "?" else INK))
        out.append(text((a + b) / 2, yb + 30, t, 16, bold=True, col=col(t)))
    W = x0 + BW + 8
    if right:
        xr = x0 + BW + 8
        y0, y1 = ys[0], ys[-1] + bh
        out.append("<path d='M%.1f %d H%.1f V%d H%.1f' fill='none' stroke='%s' stroke-width='2'/>" % (xr, y0, xr + 8, y1, xr, INK))
        out.append(text(xr + 14, (y0 + y1) / 2 + 6, right, 16, anchor="start", bold=True, col=col(right)))
        W = xr + 14 + tw(right, 16, True) + 8
    return svg_wrap(0, 0, int(math.ceil(W)), int(Hh), "".join(out), label)


U = lambda k: [(1, "", "u")] * k


# ------------------------------------------------------------ set 1: tables
def set_tables():
    its = []
    # Table A: favourite hawker food
    foods = ["Chicken rice", "Prata", "Laksa", "Nasi lemak"]
    boys = [8, 5, 2, 4]
    girls = [6, 7, 4, 3]
    tots = [b + g for b, g in zip(boys, girls)]
    B, G = sum(boys), sum(girls)
    rows = [[f, b, g, t] for f, b, g, t in zip(foods, boys, girls, tots)] + [["Total", B, G, B + G]]
    f = fig(table_svg("Favourite hawker food of 4E", ["Food", "Boys", "Girls", "Total"], rows))
    i = foods.index("Prata")
    its.append(mcqv(f + "How many girls chose prata?", girls[i], [boys[i], tots[i], girls[i + 1]], STU,
                    "Go across the Prata row to the Girls column: %d. (%d is in the Boys column.)" % (girls[i], boys[i])))
    i = 0
    its.append(mcqv(f + "How many students chose chicken rice altogether?", tots[i], [boys[i], girls[i], boys[i] - girls[i]], STU,
                    "“Altogether” means boys and girls: %d + %d = %d. It is in the Total column." % (boys[i], girls[i], tots[i])))
    its.append(mcqv(f + "How many students are there in 4E?", B + G, [G, B, tots[0]], STU,
                    "Look at the bottom right of the table: %d boys + %d girls = %d students." % (B, G, B + G)))
    gmin = girls.index(min(girls))
    assert girls.count(min(girls)) == 1 and foods[gmin] == "Nasi lemak"
    assert tots.index(min(tots)) == 2 and tots.count(min(tots)) == 1
    its.append(mcq(f + "Which food did the fewest girls choose?", "Nasi lemak", ["Laksa", "Prata", "Chicken rice"],
                   "Read down the Girls column: %s. The fewest is %d, nasi lemak. (Laksa has the fewest students in the Total column.)"
                   % (", ".join(str(g) for g in girls), min(girls))))
    i = foods.index("Prata")
    its.append(mcqv(f + "How many more girls than boys chose prata?", girls[i] - boys[i], [tots[i], girls[i], boys[i]], STU,
                    "Prata: %d girls and %d boys. “How many more” means subtract: %d − %d = %d." % (girls[i], boys[i], girls[i], boys[i], girls[i] - boys[i])))

    # Table B: library books with missing values
    fic = [36, 48, 55]
    non = [18, 35, 37]
    tb = [a + b for a, b in zip(fic, non)]
    assert tb == [54, 83, 92]
    rows = [["Monday", fic[0], non[0], tb[0]], ["Tuesday", fic[1], "?", tb[1]], ["Wednesday", "?", non[2], tb[2]]]
    f = fig(table_svg("Books borrowed from the library", ["Day", "Fiction", "Non-fiction", "Total"], rows))
    its.append(mcqv(f + "What is the missing number of non-fiction books on Tuesday?", non[1], [tb[1] + fic[1], 45, fic[1]],
                    lambda v: unit(v, "book", "books"),
                    "Total − fiction = non-fiction: %d − %d = %d. Rename 1 ten as 10 ones: 13 − 8 = 5, 7 − 4 = 3. "
                    "(45 comes from 8 − 3 instead of renaming.)" % (tb[1], fic[1], non[1])))
    its.append(mcqv(f + "What is the missing number of fiction books on Wednesday?", fic[2], [tb[2] + non[2], 65, non[2]],
                    lambda v: unit(v, "book", "books"),
                    "%d − %d = %d. Rename 1 ten as 10 ones: 12 − 7 = 5, 8 − 3 = 5. Check: %d + %d = %d. (65 comes from 7 − 2 instead of renaming.)"
                    % (tb[2], non[2], fic[2], fic[2], non[2], tb[2])))
    assert sum(fic) == 139 and sum(non) == 90 and sum(tb) == 229
    its.append(mcqv(f + "How many fiction books were borrowed on the three days altogether?", sum(fic),
                    [fic[0] + fic[1], sum(tb), sum(non)], lambda v: unit(v, "book", "books"),
                    "First find Wednesday: %d − %d = %d. Then add the Fiction column: %d + %d + %d = %d."
                    % (tb[2], non[2], fic[2], fic[0], fic[1], fic[2], sum(fic))))

    # Table C: CCA
    ccas = ["Choir", "Football", "Art Club", "Chess"]
    cv = [28, 35, 19, 24]
    rows = [[c, v] for c, v in zip(ccas[:3], cv[:3])] + [["Chess", "?"], ["Total", sum(cv)]]
    f = fig(table_svg("P4 students in each CCA", ["CCA", "Students"], rows))
    s3 = sum(cv[:3])
    its.append(mcqv(f + "How many students are in Chess?", cv[3], [s3, sum(cv) + s3, cv[3] + 10], STU,
                    "Add the known rows: %d + %d + %d = %d. Then total − %d: %d − %d = %d."
                    % (cv[0], cv[1], cv[2], s3, s3, sum(cv), s3, cv[3])))
    its.append(mcq(f + "Which CCA has the most P4 students?", "Football", ["Choir", "Chess", "Art Club"],
                   "Compare the numbers: Choir %d, Football %d, Art Club %d, Chess %d. Football has the most."
                   % tuple(cv)))

    # Completing a table from raw data
    raw = ["milk", "juice", "milk", "water", "soya milk", "milk", "juice", "milk", "water", "milk", "juice", "milk"]
    cnt = {k: raw.count(k) for k in ["milk", "juice", "water", "soya milk"]}
    assert cnt == {"milk": 6, "juice": 3, "water": 2, "soya milk": 1}
    q0 = ("Mei Ling asked 12 friends for their favourite drink. These are the answers:<br>"
          "<b>%s</b><br>She puts the results in a table. " % ", ".join(raw))
    its.append(mcqv(q0 + "What number goes in the Milk row?", 6, [5, 7, 3], lambda v: unit(v, "friend", "friends"),
                    "Count “milk” one by one and tick each one: 6. Check the table: 6 + 3 + 2 + 1 = 12 friends."))
    its.append(mcqv(q0 + "What number goes in the Juice row?", 3, [2, 4, 6], lambda v: unit(v, "friend", "friends"),
                    "Count “juice”: 3. Water has 2, soya milk has 1 and milk has 6. 6 + 3 + 2 + 1 = 12."))
    walk, bus, total = 12, 9, 36
    car = total - walk - bus
    rows = [["Walk", walk], ["School bus", bus], ["Car", "?"], ["Total", total]]
    f = fig(table_svg("How 4A students go to school", ["Way", "Students"], rows))
    its.append(mcqv(f + "There are 36 students in 4A. 12 walk, 9 take the school bus and the rest come by car. "
                    "What number goes in the Car row?", car, [walk + bus, total + walk + bus, total - walk], STU,
                    "Walk and bus: %d + %d = %d. The rest: %d − %d = %d come by car." % (walk, bus, walk + bus, total, walk + bus, car)))

    # Table D: Sports Day
    houses = ["Red", "Blue", "Green", "Yellow"]
    run = [45, 38, 39, 50]
    rel = [30, 36, 42, 25]
    ht = [a + b for a, b in zip(run, rel)]
    assert ht == [75, 74, 81, 75]
    rows = [["Red", run[0], rel[0], ht[0]], ["Blue", run[1], "?", ht[1]], ["Green", "?", rel[2], ht[2]],
            ["Yellow", run[3], rel[3], ht[3]]]
    f = fig(table_svg("Sports Day points", ["House", "Races", "Relay", "Total"], rows))
    its.append(mcqv(f + "How many points did Blue House score in the relay?", rel[1], [ht[1] + run[1], 44, run[1]],
                    lambda v: unit(v, "point", "points"),
                    "%d − %d = %d. Rename 1 ten as 10 ones: 14 − 8 = 6, 6 − 3 = 3. (44 comes from 8 − 4 instead of renaming.)"
                    % (ht[1], run[1], rel[1])))
    its.append(mcq(f + "Which house scored the most points altogether?", "Green", ["Red", "Yellow", "Blue"],
                   "Use the Total column: Red %d, Blue %d, Green %d, Yellow %d. Green has the most." % tuple(ht)))
    assert run.index(max(run)) == 3
    its.append(mcq(f + "Which house scored the most points in the races?", "Yellow", ["Red", "Green", "Blue"],
                   "Green’s races: %d − %d = %d. Races column: Red %d, Blue %d, Green %d, Yellow %d. Yellow has the most. "
                   "(Green has the most in the Total column, not the Races column.)"
                   % (ht[2], rel[2], run[2], run[0], run[1], run[2], run[3])))

    # Table E: fun fair visitors
    ad = [125, 240, 316]
    ch = [208, 375, 434]
    ft = [a + b for a, b in zip(ad, ch)]
    assert ft == [333, 615, 750]
    rows = [["Friday", ad[0], ch[0], ft[0]], ["Saturday", ad[1], ch[1], ft[1]], ["Sunday", ad[2], "?", ft[2]]]
    f = fig(table_svg("Visitors to the school fun fair", ["Day", "Adults", "Children", "Total"], rows))
    V = lambda v: unit(v, "child", "children")
    its.append(mcqv(f + "How many children went to the fun fair on Sunday?", ch[2], [ft[2] + ad[2], 446, ad[2]], V,
                    "%d − %d = %d. Rename 1 ten as 10 ones: 10 − 6 = 4, 4 − 1 = 3, 7 − 3 = 4. "
                    "(446 comes from 6 − 0 instead of renaming.)" % (ft[2], ad[2], ch[2])))
    assert sum(ch) == 1017
    its.append(mcqv(f + "How many children went on the three days altogether?", sum(ch), [ch[0] + ch[1], sum(ft), sum(ad)], V,
                    "Sunday: %d − %d = %d. Children column: %d + %d + %d = %d. (%d adds the Total column.)"
                    % (ft[2], ad[2], ch[2], ch[0], ch[1], ch[2], sum(ch), sum(ft))))
    its.append(mcqv(f + "How many more children than adults went on Friday?", ch[0] - ad[0], [123, ft[0], ad[0]],
                    lambda v: unit(v, "visitor", "visitors"),
                    "Friday: %d children and %d adults. %d − %d = %d. Rename 1 hundred as 10 tens. "
                    "(123 comes from taking the smaller digit from the bigger one.)" % (ch[0], ad[0], ch[0], ad[0], ch[0] - ad[0])))
    days = ["Monday", "Tuesday", "Wednesday", "Thursday"]
    ov = [240, 185, 310, 265]
    rows = [[d, v] for d, v in zip(days[:3], ov[:3])] + [["Thursday", "?"], ["Total", sum(ov)]]
    assert sum(ov) == 1000
    f = fig(table_svg("Mandarin oranges sold at a stall", ["Day", "Oranges"], rows))
    its.append(mcqv(f + "How many mandarin oranges were sold on Thursday?", ov[3], [sum(ov[:3]), sum(ov) + sum(ov[:3]), 375],
                    lambda v: unit(v, "orange", "oranges"),
                    "Monday to Wednesday: %d + %d + %d = %d. Thursday: 1000 − %d = %d. "
                    "(375 comes from renaming each 0 as 10 without taking 1 from the next place. 1000 is 9 hundreds, 9 tens and 10 ones.)" % (ov[0], ov[1], ov[2], sum(ov[:3]), sum(ov[:3]), ov[3])))
    return {"title": "Complete and read tables", "items": its}


# ------------------------------------------------------------ line graphs (data)
DAYS5 = ["Mon", "Tue", "Wed", "Thu", "Fri"]
DAYN = {"Mon": "Monday", "Tue": "Tuesday", "Wed": "Wednesday", "Thu": "Thursday", "Fri": "Friday",
        "Sat": "Saturday", "Sun": "Sunday"}
MON = {"Jan": "January", "Feb": "February", "Mar": "March", "Apr": "April", "May": "May", "Jun": "June"}
VIS = lambda v: unit(v, "visitor", "visitors")
DEG = lambda v: num(v) + " °C"
CM = lambda v: num(v) + " cm"
LIT = lambda v: num(v) + " ℓ"
CUP = lambda v: unit(v, "cup", "cups")
ORA = lambda v: unit(v, "orange", "oranges")
BOOK = lambda v: unit(v, "book", "books")

LIB = LG("Visitors to the school library", DAYS5, "Day", "Visitors", [[40, 55, 30, 70, 65]], 0, 80, 20, 10, f=VIS)
ROOM = LG("Temperature in a classroom", ["8 am", "9 am", "10 am", "11 am", "12 noon", "1 pm", "2 pm"], "Time",
          "Temperature (°C)", [[26, 27, 29, 30, 32, 31, 31]], 24, 34, 2, 1, f=DEG)
SUN = LG("Height of a sunflower", ["1", "2", "3", "4", "5", "6"], "Week", "Height (cm)",
         [[10, 20, 35, 55, 70, 85]], 0, 100, 20, 10, f=CM)
ORANGES = LG("Mandarin oranges sold at a stall", ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat"], "Day", "Oranges sold",
             [[150, 225, 300, 350, 450, 400]], 0, 500, 100, 50, f=ORA)
SAVE = LG("Wei Ming’s savings", ["Jan", "Feb", "Mar", "Apr", "May", "Jun"], "Month", "Savings ($)",
          [[5, 15, 20, 30, 35, 50]], 0, 60, 10, 5, f=money)
PAIL = LG("Water in a pail", ["0", "2", "4", "6", "8", "10"], "Minutes", "Water (ℓ)",
          [[0, 3, 6, 9, 12, 15]], 0, 16, 4, 2, f=LIT)
TEA = LG("Cups of bubble tea sold", ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"], "Day", "Cups sold",
         [[40, 50, 50, 70, 60, 100, 110]], 0, 120, 20, 10, f=CUP)
OUT_T = LG("Temperature outside the school", ["7 am", "9 am", "11 am", "1 pm", "3 pm", "5 pm", "7 pm"], "Time",
           "Temperature (°C)", [[25, 27, 30, 32, 31, 28, 27]], 24, 34, 2, 1, f=DEG)
PLANTS = LG("Heights of two plants", ["1", "2", "3", "4", "5", "6"], "Week", "Height (cm)",
            [[4, 6, 9, 12, 14, 16], [2, 5, 9, 11, 15, 18]], 0, 20, 5, 1, names=["Plant A", "Plant B"], f=CM)
TANK = LG("Water in a tank", ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat"], "Day", "Water (ℓ)",
          [[900, 800, 650, 650, 400, 300]], 0, 1000, 200, 100, f=LIT)
READ = LG("Books read by 4C", ["Jan", "Feb", "Mar", "Apr", "May", "Jun"], "Month", "Books read",
          [[12, 16, 20, 26, 30, 22]], 0, 40, 10, 2, f=BOOK)


def changes(T, si=0):
    v = T.series[si]
    return [v[k + 1] - v[k] for k in range(len(v) - 1)]


# ------------------------------------------------------------ set 2: read line graphs
def set_read():
    its = []
    T = LIB
    f = fig(T.svg())
    its.append(mcqv(f + "How many visitors were there on Monday?", 40, [4, 50, 30], T.v,
                    "Go up from Mon to the point, then across to the scale. The point is on the line for 40. "
                    "(4 counts the gaps, but each gap is 10.)"))
    its.append(mcqv(f + "The labels on the scale go up in 20s. How many visitors does each gap between two gridlines stand for?",
                    10, [20, 1, 5], T.v,
                    "There is one gridline between 0 and 20, so 20 is split into 2 gaps. 20 ÷ 2 = 10 visitors for each gap."))
    its.append(mcqv(f + "How many visitors were there on Tuesday?", 55, [50, 60, 45], T.v,
                    "The point for Tue is halfway between the gridlines for 50 and 60. Halfway between 50 and 60 is 55."))
    its.append(mcq(f + "On which day were there 30 visitors?", "Wednesday", ["Monday", "Thursday", "Friday"],
                   "Find 30 on the scale and go across to the line, then down: Wed. (Monday had 40.)"))
    its.append(mcq(f + "On which day were there the most visitors?", "Thursday", ["Friday", "Tuesday", "Monday"],
                   "The highest point is above Thu: 70 visitors. Friday had 65, a little less."))
    T = ROOM
    f = fig(T.svg())
    its.append(mcqv(f + "What was the temperature at 10 am?", 29, [28, 30, 5], T.v,
                    "The scale starts at 24, not 0. Each gap is 1 °C. The point at 10 am is 1 gap above 28: 29 °C. "
                    "(5 counts the gaps from the bottom but forgets that the scale starts at 24.)"))
    its.append(mcqv(f + "What was the highest temperature?", 32, [31, 34, 30], T.v,
                    "The highest point is at 12 noon, on the line for 32: 32 °C. (34 is the top of the scale, not a reading.)"))
    its.append(mcq(f + "At what time was the temperature 30 °C?", "11 am", ["10 am", "12 noon", "1 pm"],
                   "Find 30 on the scale, go across to the line, then down: 11 am."))
    its.append(mcqv(f + "What was the temperature at 8 am?", 26, [24, 2, 27], T.v,
                    "The point at 8 am is on the line labelled 26: 26 °C. (24 is where the scale starts.)"))
    T = SUN
    f = fig(T.svg())
    its.append(mcqv(f + "How tall was the sunflower in week 3?", 35, [30, 40, 45], T.v,
                    "The labels go up in 20s, so each gap is 10 cm. Week 3 is halfway between 30 and 40: 35 cm."))
    its.append(mcq(f + "In which week was the sunflower 55 cm tall?", "Week 4", ["Week 5", "Week 3", "Week 6"],
                   "55 is halfway between 50 and 60. Go across to the line, then down: week 4."))
    its.append(mcqv(f + "How tall was the sunflower in week 6?", 85, [80, 90, 100], T.v,
                    "The point for week 6 is halfway between 80 and 90: 85 cm."))
    T = ORANGES
    f = fig(T.svg())
    its.append(mcqv(f + "How many mandarin oranges were sold on Monday?", 150, [3, 100, 200], T.v,
                    "Each gap is 100 ÷ 2 = 50. The point for Mon is 1 gap above 100: 150 oranges. (3 counts the gaps, not their value.)"))
    its.append(mcqv(f + "How many mandarin oranges were sold on Tuesday?", 225, [250, 200, 275], T.v,
                    "The point is halfway between the gridlines for 200 and 250. Halfway between 200 and 250 is 225."))
    its.append(mcq(f + "On which day were 350 oranges sold?", "Thursday", ["Wednesday", "Friday", "Saturday"],
                   "350 is the gridline halfway between 300 and 400. Go across to the line, then down: Thu."))
    its.append(mcqv(f + "How many oranges does each gap between two gridlines stand for?", 50, [100, 10, 25], T.v,
                    "The labels go up in 100s and there are 2 gaps between labels: 100 ÷ 2 = 50."))
    T = SAVE
    f = fig(T.svg())
    its.append(mcqv(f + "How much had Wei Ming saved by April?", 30, [3, 25, 35], T.v,
                    "Go up from Apr to the point, then across: it is on the line for 30. He had saved $30."))
    its.append(mcq(f + "In which month did Wei Ming have $35?", "May", ["April", "June", "March"],
                   "Each gap is $5. $35 is halfway between 30 and 40. Go across to the line, then down: May."))
    T = PAIL
    f = fig(T.svg())
    its.append(mcqv(f + "How much water was in the pail after 6 minutes?", 9, [8, 10, 6], T.v,
                    "The labels go up in 4s and each gap is 2 ℓ. At 6 minutes the point is halfway between 8 and 10: 9 ℓ."))
    its.append(mcqv(f + "After how many minutes was there 15 ℓ of water in the pail?", 10, [8, 15, 6],
                    lambda v: num(v) + " min",
                    "15 is halfway between 14 and 16. Go across to the line, then down: 10 minutes."))
    return {"title": "Read line graphs: scales and values", "items": its}


# ------------------------------------------------------------ set 3: trends and changes
def pair(T, k, full=True):
    a, b = T.xl[k], T.xl[k + 1]
    if full:
        a, b = DAYN.get(a, MON.get(a, a)), DAYN.get(b, MON.get(b, b))
    return "%s and %s" % (a, b)


def tpair(T, k):
    return "%s to %s" % (T.xl[k], T.xl[k + 1])


def set_trends():
    its = []
    T = TEA
    ch = changes(T)
    f = fig(T.svg())
    mo, th = T.at("Mon"), T.at("Thu")
    its.append(mcqv(f + "How many more cups were sold on Thursday than on Monday?", th - mo, [th + mo, th, 3], T.v,
                    "Thursday: %d cups. Monday: %d cups. %d − %d = %d cups." % (th, mo, th, mo, th - mo)))
    assert ch.count(0) == 1 and ch.index(0) == 1
    its.append(mcq(f + "Between which two days did the number of cups sold stay the same?", pair(T, 1),
                   [pair(T, 0), pair(T, 3), pair(T, 5)],
                   "The line is flat from Tue to Wed: 50 cups on both days."))
    dn = [k for k, c in enumerate(ch) if c < 0]
    assert dn == [3]
    its.append(mcq(f + "Between which two days did the number of cups sold go down?", pair(T, 3),
                   [pair(T, 1), pair(T, 4), pair(T, 0)],
                   "The line goes down only from Thu (70) to Fri (60)."))
    k = ch.index(max(ch))
    assert ch.count(max(ch)) == 1 and k == 4
    its.append(mcq(f + "Between which two days was the greatest increase?", pair(T, 4), [pair(T, 5), pair(T, 2), pair(T, 0)],
                   "Look for the steepest part going up. Fri to Sat: 60 to 100, up 40 cups. "
                   "Sunday has the highest point, but Sat to Sun is only up 10."))
    its.append(mcqv(f + "By how much did the sales increase from Friday to Saturday?", 40, [100, 160, 4], T.v,
                    "Saturday: 100. Friday: 60. 100 − 60 = 40 cups. (4 counts the gaps, but each gap is 10.)"))

    T = OUT_T
    ch = changes(T)
    f = fig(T.svg())
    its.append(mcq(f + "How did the temperature change from 7 am to 1 pm?", "It increased",
                   ["It decreased", "It stayed the same", "It increased, then decreased"],
                   "From 7 am to 1 pm the line goes up all the time: 25, 27, 30, 32 °C. It increased."))
    its.append(mcqv(f + "By how much did the temperature fall from 1 pm to 7 pm?", 5, [27, 3, 32], T.v,
                    "1 pm: 32 °C. 7 pm: 27 °C. 32 − 27 = 5 °C. (27 °C is the reading at 7 pm, not the fall.)"))
    k = ch.index(min(ch))
    assert ch.count(min(ch)) == 1 and k == 4
    its.append(mcq(f + "In which 2 hours did the temperature fall the most?", tpair(T, 4), [tpair(T, 5), tpair(T, 3), tpair(T, 2)],
                   "Falls: 1 pm to 3 pm: 1 °C; 3 pm to 5 pm: 3 °C; 5 pm to 7 pm: 1 °C. The steepest fall is 3 pm to 5 pm."))
    its.append(mcqv(f + "By how much did the temperature rise from 7 am to 1 pm?", 7, [32, 25, 3], T.v,
                    "1 pm: 32 °C. 7 am: 25 °C. 32 − 25 = 7 °C. The scale starts at 24, so read the labels, not the gaps from the bottom."))

    T = PLANTS
    A, Bv = T.series
    f = fig(T.svg())
    same = [i for i in range(6) if A[i] == Bv[i]]
    assert same == [2]
    its.append(mcq(f + "In which week were both plants the same height?", "Week 3", ["Week 6", "Week 1", "Week 4"],
                   "The two lines meet at week 3: both plants were 9 cm tall."))
    its.append(mcqv(f + "How much taller was Plant B than Plant A in week 6?", Bv[5] - A[5], [Bv[5], A[5], Bv[5] + A[5]], T.v,
                    "Week 6: Plant B %d cm, Plant A %d cm. %d − %d = %d cm." % (Bv[5], A[5], Bv[5], A[5], Bv[5] - A[5])))
    ga, gb = A[5] - A[0], Bv[5] - Bv[0]
    assert (ga, gb) == (12, 16)
    its.append(mcq(f + "Which plant grew more from week 1 to week 6?", "Plant B", ["Plant A", "They grew the same", "You cannot tell"],
                   "Plant A: %d − %d = %d cm. Plant B: %d − %d = %d cm. Plant B grew more, even though it was shorter in week 1."
                   % (A[5], A[0], ga, Bv[5], Bv[0], gb)))
    assert A[3] > Bv[3]
    its.append(mcq(f + "Which plant was taller in week 4?", "Plant A", ["Plant B", "They were the same", "You cannot tell"],
                   "Week 4: Plant A (solid line) %d cm, Plant B (dashed line) %d cm. Plant A was taller by 1 cm." % (A[3], Bv[3])))

    T = TANK
    ch = changes(T)
    f = fig(T.svg())
    its.append(mcq(f + "How did the amount of water in the tank change from Monday to Saturday?", "It decreased",
                   ["It increased", "It stayed the same", "It increased, then decreased"],
                   "The line goes down from 900 ℓ to 300 ℓ (it is flat for one day). Overall, it decreased."))
    assert ch.index(0) == 2 and ch.count(0) == 1
    its.append(mcq(f + "Between which two days did the amount of water not change?", pair(T, 2), [pair(T, 1), pair(T, 3), pair(T, 4)],
                   "The line is flat from Wed to Thu: 650 ℓ on both days."))
    its.append(mcqv(f + "How much water was used from Monday to Saturday?", 600, [300, 1200, 6], T.v,
                    "Monday: 900 ℓ. Saturday: 300 ℓ. 900 − 300 = 600 ℓ were used. (300 ℓ is what is left.)"))
    k = ch.index(min(ch))
    assert ch.count(min(ch)) == 1 and k == 3
    its.append(mcq(f + "Between which two days was the most water used?", pair(T, 3), [pair(T, 4), pair(T, 1), pair(T, 0)],
                   "The steepest fall is Thu to Fri: 650 − 400 = 250 ℓ. Saturday has the lowest point, but Fri to Sat is only 100 ℓ."))

    T = READ
    ch = changes(T)
    f = fig(T.svg())
    assert [k for k, c in enumerate(ch) if c < 0] == [4]
    its.append(mcq(f + "Between which two months did the number of books read go down?", pair(T, 4),
                   [pair(T, 3), pair(T, 0), pair(T, 2)],
                   "The line goes down only from May (30) to Jun (22)."))
    its.append(mcqv(f + "By how much did the number of books increase from January to May?", 18, [30, 42, 12], T.v,
                    "Each gap is 2 books. January: 12. May: 30. 30 − 12 = 18 books."))
    its.append(mcq(f + "Which sentence describes the graph?", "It rose every month until May, then fell",
                   ["It rose every month from January to June", "It fell every month until May, then rose",
                    "It stayed the same from January to May"],
                   "12, 16, 20, 26, 30: up every month until May. Then it fell to 22 in June."))
    return {"title": "Trends and changes in line graphs", "items": its}


# ------------------------------------------------------------ set 4: pie charts
def frac_wrongs(p, nn, k, neg=False):
    """Typical mistakes: complement, 1 out of the number of groups, part to rest, one slice too many or few."""
    right = F(nn - p, nn) if neg else F(p, nn)
    c = [F(p, nn) if neg else F(nn - p, nn), F(1, k), F(p, nn - p) if not neg else F(nn - p, p), F(p + 1, nn), F(p - 1, nn),
         F(1, nn), F(1, 2)]
    return right, [x for x in c if 0 < x < 1]


def frac_ex(p, nn, names, neg=False):
    nm = " and ".join(names)
    s = "The circle is split into %d equal parts. %s %s %d of them" % (nn, nm, "has" if len(names) == 1 else "have", p)
    if neg:
        s += ", so %d − %d = %d parts are not %s: %s" % (nn, p, nn - p, nm.lower(), fr(nn - p, nn))
        v = F(nn - p, nn)
    else:
        s += ": %s" % fr(p, nn)
        v = F(p, nn)
    if v.denominator != nn:
        s += " = %s in simplest form" % frs(v)
    return s + "."


FRUIT = Pie("Favourite fruit", ["Mango", "Watermelon", "Durian", "Rambutan"], [4, 2, 1, 1])
TRAVEL = Pie("How 4D students go to school", ["Walk", "School bus", "Car"], [4, 3, 1])
CCA = Pie("Favourite CCA", ["Choir", "Football", "Art"], [2, 1, 1])
POCKET = Pie("How Ali used $32", ["Food", "Bus fare", "Savings", "Books"], [4, 2, 1, 1])
COLOUR = Pie("Favourite colour of 16 students", ["Blue", "Red", "Green"], [2, 5, 1])


def set_pie():
    its = []

    def fq(pie, names, q, neg=False):
        p = sum(pie.p(c) for c in names)
        right, wr = frac_wrongs(p, pie.n, len(pie.cats), neg)
        its.append(mcqv(fig(pie_svg(pie)) + q, right, wr, frs, frac_ex(p, pie.n, names, neg)))

    def which(pie, c, q):
        p = pie.p(c)
        others = [x for x in pie.cats if x != c]
        assert all(pie.p(x) != p for x in others)
        its.append(mcq(fig(pie_svg(pie)) + q, c, others + [x for x in ["Bicycle", "Papaya"] if x not in pie.cats],
                       "The circle is split into %d equal parts. %s has %d of them: %s%s."
                       % (pie.n, c, p, fr(p, pie.n), "" if F(p, pie.n).denominator == pie.n else " = " + frs(F(p, pie.n)))))

    fq(FRUIT, ["Mango"], "What fraction of the students chose mango?")
    which(FRUIT, "Watermelon", "Which fruit was chosen by a quarter of the students?")
    fq(FRUIT, ["Durian"], "What fraction of the students chose durian?")
    fq(FRUIT, ["Watermelon"], "What fraction of the students did not choose watermelon?", neg=True)
    fq(TRAVEL, ["School bus"], "What fraction of the students take the school bus?")
    which(TRAVEL, "Walk", "Which way of going to school is used by half of the students?")
    fq(TRAVEL, ["School bus", "Car"], "What fraction of the students take the school bus or come by car?")
    fq(CCA, ["Choir"], "What fraction of the students chose Choir?")

    F40 = Pie("Favourite fruit of 40 students", FRUIT.cats, FRUIT.parts)
    f = fig(pie_svg(F40))
    its.append(mcqv(f + "How many students chose mango?", 20, [4, 10, 36], STU,
                    "Mango is half of the pie chart. Half of 40 = 40 ÷ 2 = 20 students. (4 is the number of parts, not students.)"))
    its.append(mcqv(f + "How many students chose durian?", 5, [1, 8, 10], STU,
                    "Durian is 1 of the 8 equal parts: %s of 40 = 40 ÷ 8 = 5 students." % fr(1, 8)))
    its.append(mcqv(f + "How many students chose watermelon?", 10, [2, 20, 5], STU,
                    "Watermelon is 2 of the 8 parts = %s. %s of 40 = 40 ÷ 4 = 10 students." % (frs(F(1, 4)), frs(F(1, 4)))))
    T24 = Pie("How 24 students go to school", TRAVEL.cats, TRAVEL.parts)
    f = fig(pie_svg(T24))
    its.append(mcqv(f + "How many students take the school bus?", 9, [3, 8, 15], STU,
                    "School bus is %s of the pie chart. 24 ÷ 8 = 3 students in each part. 3 parts: 3 × 3 = 9 students." % fr(3, 8)))
    its.append(mcqv(f + "How many students walk to school?", 12, [4, 6, 20], STU,
                    "Walk is half of the pie chart. Half of 24 = 12 students."))
    its.append(mcqv(f + "How many more students walk than come by car?", 9, [3, 15, 12], STU,
                    "Each part is 24 ÷ 8 = 3 students. Walk: 4 × 3 = 12. Car: 1 × 3 = 3. 12 − 3 = 9 students. "
                    "(3 is the difference in parts, not students.)"))
    f = fig(pie_svg(POCKET))
    its.append(mcqv(f + "How much did Ali spend on food?", 16, [4, 8, 28], money,
                    "Food is half of the pie chart. Half of $32 = $16."))
    its.append(mcqv(f + "How much did Ali spend on bus fare?", 8, [2, 16, 4], money,
                    "Bus fare is 2 of the 8 parts = %s. %s of $32 = $32 ÷ 4 = $8." % (frs(F(1, 4)), frs(F(1, 4)))))
    f = fig(pie_svg(CCA))
    its.append(mcqv(f + "6 students chose Football. How many students were asked altogether?", 24, [10, 12, 18], STU,
                    "Football is a quarter of the pie chart. If %s is 6 students, the whole is 4 × 6 = 24 students. "
                    "(12 doubles 6, but Football is a quarter, not a half.)" % frs(F(1, 4))))
    f = fig(pie_svg(FRUIT))
    its.append(mcqv(f + "3 students chose rambutan. How many students were asked altogether?", 24, [11, 6, 12], STU,
                    "Rambutan is %s of the pie chart. If 1 part is 3 students, 8 parts are 8 × 3 = 24 students." % fr(1, 8)))
    pr = ["Durian and Rambutan", "Mango and Durian", "Watermelon and Durian", "Mango and Watermelon"]
    assert FRUIT.frac("Durian", "Rambutan") == F(1, 4)
    its.append(mcq(f + "Which two fruits together make a quarter of the pie chart?", pr[0], pr[1:],
                   "A quarter of 8 parts is 2 parts. Durian (1 part) and rambutan (1 part) make 2 parts: %s = %s."
                   % (fr(2, 8), frs(F(1, 4)))))
    f = fig(pie_svg(COLOUR))
    its.append(mcqv(f + "How many students chose red?", 10, [5, 2, 6], STU,
                    "Red is %s of the pie chart. 16 ÷ 8 = 2 students in each part. 5 parts: 5 × 2 = 10 students. "
                    "(5 is the number of parts.)" % fr(5, 8)))
    return {"title": "Read pie charts: halves, quarters and eighths", "items": its}


# ------------------------------------------------------------ set 5: word problems
def set_words():
    its = []
    a4 = Pie("4A: 24 students", ["Football", "Swimming", "Badminton"], [4, 2, 2])
    b4 = Pie("4B: 40 students", ["Football", "Swimming", "Badminton"], [3, 3, 2])
    fa, fb = a4.frac("Football") * 24, b4.frac("Football") * 40
    assert (fa, fb) == (12, 15)
    f = fig(pie_svg(a4, b4))
    its.append(mcq(f + "Which class has more students who chose football?", "4B", ["4A", "Both the same", "You cannot tell"],
                   "4A: %s of 24 = 12 students. 4B: %s of 40 = 40 ÷ 8 × 3 = 15 students. 4B has more, even though its "
                   "football slice is smaller, because 4B has more students." % (frs(F(1, 2)), fr(3, 8))))
    its.append(mcqv(f + "How many students chose football in 4A and 4B altogether?", fa + fb, [64, 12, 15], STU,
                    "4A: 12. 4B: 15. 12 + 15 = 27 students."))
    ba = Pie("Block A: 80 homes", ["Recycle", "Do not recycle"], [4, 4])
    bb = Pie("Block B: 120 homes", ["Recycle", "Do not recycle"], [3, 5])
    ra, rb = ba.frac("Recycle") * 80, bb.frac("Recycle") * 120
    assert (ra, rb) == (40, 45)
    its.append(mcq(fig(pie_svg(ba, bb)) + "Siti says, “More homes recycle in Block A, because its Recycle slice is bigger.” "
                   "Is she right?", "No: 40 in A, 45 in B",
                   ["Yes: 40 in A, 45 in B", "Yes: the slice is bigger", "No: 45 in A, 40 in B"],
                   "Block A: %s of 80 = 40 homes. Block B: %s of 120 = 120 ÷ 8 × 3 = 45 homes. The slice shows the fraction, "
                   "not the number of homes." % (frs(F(1, 2)), fr(3, 8))))
    m = model_svg([("4A", U(3)), ("4C", U(1))], right="168", under=[(0, 0, 3, "?")],
                  label="bar model: 4A is 3 units, 4C is 1 unit, 168 cans altogether")
    its.append(mcqv(fig(m) + "Mrs Ng is completing a table of cans collected for recycling. 4A collected 3 times as many cans "
                    "as 4C. Together they collected 168 cans. How many cans did 4A collect?", 126, [42, 56, 84],
                    lambda v: unit(v, "can", "cans"),
                    "4 units = 168, so 1 unit = 168 ÷ 4 = 42. 4A has 3 units: 3 × 42 = 126 cans. "
                    "(56 uses 3 units instead of 4 units for the total.)"))
    m = model_svg([("Chicken rice", U(3)), ("Prata", U(1))], under=[(0, 1, 3, "12")],
                  label="bar model: chicken rice is 3 units, prata is 1 unit, the difference is 12")
    its.append(mcqv(fig(m) + "In a pie chart of favourite hawker food, chicken rice is %s and prata is %s of the circle. "
                    "12 more students chose chicken rice than prata. How many students were in the survey?" % (fr(3, 8), fr(1, 8)),
                    48, [24, 96, 20], STU,
                    "The circle has 8 units. Chicken rice is 3 units and prata is 1 unit. 2 units = 12, so 1 unit = 6. "
                    "The whole survey is 8 units: 8 × 6 = 48 students."))
    f = fig(SAVE.svg())
    its.append(mcqv(f + "Wei Ming wants to buy a watch that costs $65. He uses his savings in June. How much more money does he need?", 15,
                    [50, 115, 30], money,
                    "June: $50. $65 − $50 = $15. (30 uses May’s savings, $35.)"))
    f = fig(SUN.svg())
    its.append(mcqv(f + "The sunflower keeps growing by the same amount each week as from week 5 to week 6. How tall will it be "
                    "in week 8?", 115, [100, 170, 95], CM,
                    "Week 5: 70 cm. Week 6: 85 cm. It grows 15 cm a week. Week 7: 100 cm. Week 8: 115 cm."))
    rows = [["Adult", "$8", 45], ["Child", "$5", 60]]
    f = fig(table_svg("Tickets sold for the school concert", ["Ticket", "Price", "Number sold"], rows))
    its.append(mcqv(f + "How much money was collected from child tickets?", 300, [65, 225, 480], money,
                    "Child row: 60 tickets at $5 each. 60 × $5 = $300. (480 uses the adult price.)"))
    its.append(mcqv(f + "How much money was collected altogether?", 660, [105, 300, 1365], money,
                    "Adult: 45 × $8 = $360. Child: 60 × $5 = $300. $360 + $300 = $660. (105 is the number of tickets.)"))
    m = model_svg([("Boys", U(1)), ("Girls", U(1) + [(14 / 23.0, "14", "o")])], right="60", under=[(0, 0, 1, "?")],
                  label="bar model: boys 1 unit, girls 1 unit and 14, 60 altogether")
    its.append(mcqv(fig(m) + "Mrs Lim is making a table of the boys and girls in the Choir. There are 60 students in the Choir. "
                    "There are 14 more girls than boys. How many boys are there?", 23, [37, 30, 46],
                    lambda v: unit(v, "boy", "boys"),
                    "Take away the extra 14 girls: 60 − 14 = 46. Now 2 units = 46, so 1 unit = 23. There are 23 boys "
                    "(and 23 + 14 = 37 girls)."))
    lim = Pie("How Mrs Lim spent $2400", ["Food", "Transport", "Bills", "Savings"], [3, 1, 2, 2])
    f = fig(pie_svg(lim))
    its.append(mcqv(f + "How much did Mrs Lim spend on food?", 900, [300, 1500, 800], money,
                    "$2400 ÷ 8 = $300 for each part. Food has 3 parts: 3 × $300 = $900. (800 divides by 3, not 8.)"))
    its.append(mcqv(f + "How much more did Mrs Lim spend on food than on transport?", 600, [1200, 300, 1500], money,
                    "Each part is $300. Food: $900. Transport: $300. $900 − $300 = $600. (1500 is the money not spent on food.)"))
    f = fig(TEA.svg())
    its.append(mcqv(f + "Each cup of bubble tea costs $3. How much money did the stall collect on Saturday?", 300,
                    [103, 330, 210], money,
                    "Saturday: 100 cups. 100 × $3 = $300. (330 uses Sunday’s 110 cups.)"))
    f = fig(PLANTS.svg())
    its.append(mcq(f + "After week 6, Plant B grows 3 cm every week. In which week will it be 27 cm tall?", "Week 9",
                   ["Week 8", "Week 10", "Week 7"],
                   "Week 6: 18 cm. Week 7: 21 cm. Week 8: 24 cm. Week 9: 27 cm."))
    boys = [18, 20, 19]
    girls = [22, 19, 20]
    BT, GT = sum(boys), sum(girls)
    assert (BT, GT) == (57, 61)
    rows = [["4A", boys[0], "?"], ["4B", boys[1], girls[1]], ["4C", "?", girls[2]], ["Total", BT, GT]]
    f = fig(table_svg("P4 students in each class", ["Class", "Boys", "Girls"], rows))
    its.append(mcqv(f + "How many girls are there in 4A?", girls[0], [girls[1] + girls[2], GT + girls[1] + girls[2], GT - boys[0]],
                    lambda v: unit(v, "girl", "girls"),
                    "Girls in 4B and 4C: %d + %d = %d. 4A: %d − %d = %d girls. (43 takes away 4A’s boys instead.)"
                    % (girls[1], girls[2], girls[1] + girls[2], GT, girls[1] + girls[2], girls[0])))
    cls = [b + g for b, g in zip(boys, girls)]
    assert cls == [40, 39, 39]
    its.append(mcq(f + "Which class has the most students?", "4A", ["4B", "4C", "All the same"],
                   "4A girls: %d. 4C boys: %d − %d − %d = %d. 4A: 18 + 22 = 40. 4B: 20 + 19 = 39. 4C: 19 + 20 = 39. 4A has the most."
                   % (girls[0], BT, boys[0], boys[1], boys[2])))
    cc = Pie("Favourite club", ["Chess", "Art", "Robotics"], [4, 3, 1])
    its.append(mcqv(fig(pie_svg(cc)) + "6 students chose Robotics. How many students chose Art?", 18, [24, 48, 3], STU,
                    "Robotics is 1 of the 8 equal parts, so 1 part = 6 students. Art has 3 parts: 3 × 6 = 18 students. "
                    "(48 is everyone in the survey.)"))
    m = model_svg([("Mon", U(1)), ("Sat", U(3))], under=[(0, 0, 1, "?"), (1, 1, 3, "60")],
                  label="bar model: Monday 1 unit, Saturday 3 units, the difference is 60")
    its.append(mcqv(fig(m) + "A bubble tea stall sold 3 times as many cups on Saturday as on Monday. It sold 60 more cups on "
                    "Saturday than on Monday. How many cups did it sell on Monday?", 30, [20, 90, 15], CUP,
                    "Saturday has 2 more units than Monday. 2 units = 60, so 1 unit = 30 cups on Monday. "
                    "(20 takes 60 as 3 units.)"))
    its.append(mcq("Which graph is best to show how the height of a plant changes over 6 weeks?", "Line graph",
                   ["Pie chart", "Picture graph", "Table of names"],
                   "The height changes over time. A line graph joins the readings so you can see it rise."))
    its.append(mcqv("Pie charts for School A (400 students) and School B (600 students) both show a quarter of the students "
                    "walking to school. How many more students walk in School B than in School A?", 50, [0, 200, 250], STU,
                    "School A: %s of 400 = 100. School B: %s of 600 = 150. 150 − 100 = 50. The same slice does not mean "
                    "the same number when the totals are different." % (frs(F(1, 4)), frs(F(1, 4))), allow_zero=True))
    return {"title": "Word problems with tables, line graphs and pie charts", "items": its}


# ------------------------------------------------------------ lesson
def ex(title, q, s, a):
    return ("<div class='sn-ex'><span class='sn-ex-t'>%s</span><p class='sn-ex-q'>%s</p>"
            "<p class='sn-ex-s'>%s</p><p class='sn-ex-a'>Answer: %s</p></div>" % (title, q, s, a))


def table(head, rows, cls="sn-table"):
    h = "".join("<th>%s</th>" % x for x in head)
    b = "".join("<tr>" + "".join("<td>%s</td>" % c for c in r) + "</tr>" for r in rows)
    return "<div class='sn-tw'><table class='%s'><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>" % (cls, h, b)


def body_html():
    lg = LG("Visitors to the school canteen stall", ["Mon", "Tue", "Wed", "Thu", "Fri"], "Day", "Visitors",
            [[30, 45, 45, 70, 55]], 0, 80, 20, 10, f=VIS)
    pie = Pie("Favourite drink of 32 students", ["Milk", "Juice", "Water"], [4, 3, 1])
    m = model_svg([("Milk", U(4)), ("Juice", U(3))], under=[(0, 3, 4, "4")],
                  label="bar model: milk 4 units, juice 3 units, the difference is 4")
    return (
        "<h2>Tables: read across a row and down a column</h2>"
        "<p>A table puts data in rows and columns. Put one finger on the row and one on the column. "
        "The answer is where they meet. The Total row or column adds up the others.</p>" +
        table(["Food", "Boys", "Girls", "Total"], [["Chicken rice", "8", "6", "14"], ["Prata", "5", "?", "12"],
                                                   ["Total", "13", "13", "26"]]) +
        ex("Example 1", "Find the missing number of girls who chose prata.",
           "Total − boys = girls: 12 − 5 = 7. Check the Girls column: 6 + 7 = 13.", "7 girls") +
        "<h2>Line graphs: check the scale first</h2>"
        "<p>A line graph shows how something changes. Before you read a point, ask: <b>what is each gap between two "
        "gridlines worth?</b> Go up from the bottom to the point, then across to the scale. "
        "A point halfway between two gridlines is halfway between their values.</p>"
        "<figure class='sn-fig'>" + lg.svg() +
        "<figcaption>The labels go up in 20s and each gap is 10. Tuesday is halfway between 40 and 50, so 45 visitors.</figcaption></figure>" +
        ex("Example 2", "By how much did the number of visitors increase from Wednesday to Thursday?",
           "Thursday: 70. Wednesday: 45. 70 − 45 = 25. This is the steepest part going up, so it is the greatest increase.",
           "25 visitors") +
        "<p><b>Trends:</b> a line going up shows an increase, a line going down shows a decrease, and a flat line shows no change. "
        "The steepest part shows the greatest change. The highest point is not always the greatest increase.</p>"
        "<h2>Pie charts: parts of a whole</h2>"
        "<p>A pie chart is a circle that stands for the whole group. Each slice is a fraction of the whole: half, a quarter "
        "or an eighth. Count the equal parts, then find that fraction of the total.</p>"
        "<figure class='sn-fig'>" + pie_svg(pie) +
        "<figcaption>The circle has 8 equal parts. Milk is 4 parts, so half of the 32 students chose milk: 16 students.</figcaption></figure>" +
        ex("Example 3", "How many students chose juice?", "32 ÷ 8 = 4 students in each part. Juice has 3 parts: 3 × 4 = 12.",
           "12 students") +
        "<p>Use a bar model when the question gives a difference. Milk is 4 units and juice is 3 units. "
        "If 4 more students chose milk than juice, then 1 unit = 4 students.</p>"
        "<figure class='sn-fig'>" + m +
        "<figcaption>Milk is 1 unit more than juice. 1 unit = 4, so the whole circle is 8 units = 32 students.</figcaption></figure>"
        "<h2>Comparing two pie charts</h2>"
        "<p>A bigger slice means a bigger <b>fraction</b>. It is only a bigger number if both pie charts show the same total. "
        "Half of 24 is 12, but %s of 40 is 15.</p>" % fr(3, 8) +
        "<h2>Common mistakes</h2>" +
        table(["Mistake", "What to do instead"], [
            ["Counting each gap on a line graph as 1", "Work out the scale: labels 0, 20, 40 with 2 gaps means 10 each"],
            ["Reading the wrong row or column of a table", "Put one finger on the row and one on the column"],
            ["Taking the highest point as the greatest increase", "Look for the steepest part of the line"],
            ["Giving the number of parts instead of students", "Divide the total by the number of parts first"],
            ["Saying a bigger slice always means more people", "Work out the numbers when the totals are different"],
        ])
    )


FAQ = [
    {"q": "What is taught in P4 tables, line graphs and pie charts?",
     "a": "In Primary 4, students complete tables from given data and read and interpret tables, line graphs and pie charts. They find totals and missing values, read scales, describe changes, and work out fractions of a whole from simple pie charts."},
    {"q": "How do I help my child read a line graph?",
     "a": "Ask your child to find out what each gap between two gridlines is worth before reading any point. Then go up from the bottom axis to the point and across to the scale."},
    {"q": "What is the most common mistake with pie charts?",
     "a": "The most common mistake is thinking a bigger slice always means more people. A slice only shows a fraction, so compare the numbers when two pie charts have different totals."},
    {"q": "Is this topic in the MOE syllabus?",
     "a": "Yes. Tables, line graphs and pie charts are part of the Statistics strand in the MOE 2021 Primary 4 Mathematics syllabus. Students build on this in later years, up to the PSLE in Primary 6."},
]


def balance(sets, rnd):
    """Spread the correct answers evenly: 5 at each of the 4 positions in every set."""
    for s in sets:
        items = s["items"]
        targets = [i for i in range(4) for _ in range(5)]
        rnd.shuffle(targets)
        for it, t in zip(items, targets):
            corr = it["c"][it["a"]]
            wrong = [c for k, c in enumerate(it["c"]) if k != it["a"]]
            rnd.shuffle(wrong)
            wrong.insert(t, corr)
            it["c"] = wrong
            it["a"] = t
        final = [sum(1 for it in items if it["a"] == i) for i in range(4)]
        assert final == [5, 5, 5, 5], (s["title"], final)


def gen_unit():
    rnd = random.Random(64817)
    sets = [set_tables(), set_read(), set_trends(), set_pie(), set_words()]
    balance(sets, rnd)
    seen = set()
    for s in sets:
        assert len(s["items"]) == 20, (s["title"], len(s["items"]))
        for it in s["items"]:
            assert len({plain(c) for c in it["c"]}) == 4, it
            assert it["e"], it
            assert it["q"].count("<svg") <= 1, it["q"]
            k = it["q"] + "|" + "|".join(sorted(it["c"]))
            assert k not in seen, it["q"]
            seen.add(k)
    meta = ("Free P4 maths worksheets: complete tables, read line graph scales and trends, and read pie charts. "
            "100 questions with answers, MOE syllabus.")
    assert len(meta) <= 160, len(meta)
    return {
        "country": "sg", "subject": "maths", "grade": "primary-4", "slug": "tables-line-graphs-and-pie-charts", "sort": 17,
        "updated": UPDATED, "pdf_url": "",
        "title": "Primary 4 Tables, Line Graphs and Pie Charts",
        "seo_title": "P4 Tables, Line Graphs and Pie Charts Worksheets: Free Primary 4 Maths with Answers (MOE Syllabus)",
        "short_title": "Tables, line graphs and pie charts",
        "domain": "Statistics",
        "standard_code": "Primary 4: Statistics",
        "standard_url": "https://www.moe.gov.sg/primary/curriculum/syllabus",
        "standard_text": "Completing a table from given data; reading and interpreting data from tables, line graphs and pie charts",
        "meta_desc": meta,
        "key_big": "Check the scale or the equal parts first, then read the value.",
        "key_sub": "A pie chart of 32 students has 8 equal parts, so each part is 32 ÷ 8 = 4 students, and 3 parts are 12 students.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }


def mark_large(u, pattern):
    """Tag pictures that must print larger (tables, charts, graphs, bar models) so their labels stay readable."""
    rx = re.compile(r"<svg (?=[^>]*aria-label='" + pattern + ")")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u


if __name__ == "__main__":
    u = gen_unit()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    mark_large(u, "(pie chart|line graph|table|bar model)")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
