# -*- coding: utf-8 -*-
"""
UK Year 6 Maths: Pie charts and line graphs (National Curriculum: Year 6 Statistics)
  python3 tools/gen_uk_maths_y6_pie_line.py
HTML attributes use single quotes (no backslashes in the JSON).
Pie charts are drawn exactly from the data (sector angle = share of 360°).
"""
import json, re, math, os, random
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "uk", "maths", "year-6")
UPDATED = "2026-11-02"
GREEN = "#006633"
LINE1 = "#2e8b57"
LINE2 = "#c0392b"
INK = "#2b2b2b"
GRID = "#d5ddd8"
GRID2 = "#9fb0a5"
FONT = "Arial, Helvetica, sans-serif"
PALETTE = ["#8fc9a3", "#f2d16b", "#9cbfe8", "#f0a58f", "#c9bde6", "#d7dcd9"]
COLOURS = {"Red": "#e5786e", "Blue": "#86aee6", "Green": "#86c98f", "Yellow": "#f3dc6e", "Purple": "#b79fdc"}
MINUS = "−"


# ------------------------------------------------------------ helpers
def fr(a, b):
    return "<span class='fr'><span class='fn'>%s</span><span class='fd'>%s</span></span>" % (a, b)


def frs(x):
    x = F(x)
    if x.denominator == 1:
        return str(x.numerator)
    return fr(x.numerator, x.denominator)


def num(x):
    x = F(x)
    if x.denominator == 1:
        v = x.numerator
        s = "{:,}".format(abs(v))
        return (MINUS if v < 0 else "") + s
    d = F(x) * 10
    if d.denominator == 1:
        return "%s%d.%d" % (MINUS if x < 0 else "", abs(int(d)) // 10, abs(int(d)) % 10)
    d = F(x) * 100
    assert d.denominator == 1, x
    v = abs(int(d))
    return "%s%d.%02d" % (MINUS if x < 0 else "", v // 100, v % 100)


def pct(x):
    return num(x) + "%"


def deg(x):
    return num(x) + "°"


def pounds(x):
    return "£" + num(x)


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


# ------------------------------------------------------------ pie charts
class Pie:
    """cats with parts out of n equal slices (n = parts total). Drawn from 12 o'clock, clockwise."""
    def __init__(self, title, cats, parts, ticks=True, labels=None, fills=None):
        self.title, self.cats, self.parts = title, cats, parts
        self.n = sum(parts)
        self.ticks = ticks
        self.labels = labels or cats
        self.fills = fills or ([COLOURS[c] for c in cats] if all(c in COLOURS for c in cats)
                               else PALETTE[:len(cats)])
        assert len(set(cats)) == len(cats)

    def frac(self, *names):
        return F(sum(self.parts[self.cats.index(c)] for c in names), self.n)

    def angle(self, c):
        return self.frac(c) * 360

    def parts_of(self, c):
        return self.parts[self.cats.index(c)]


def pie_parts(p, R=58, fs=14):
    """Return (svg elements, bbox) for a pie centred at (0, 0) with its title above."""
    s = []
    a0 = 0.0
    pt = lambda a, r: (r * math.sin(math.radians(a)), -r * math.cos(math.radians(a)))
    boxes = []
    for i, (c, k) in enumerate(zip(p.cats, p.parts)):
        a1 = a0 + 360.0 * k / p.n
        x1, y1 = pt(a0, R)
        x2, y2 = pt(a1, R)
        large = 1 if a1 - a0 > 180 else 0
        if k == p.n:
            s.append("<circle cx='0' cy='0' r='%d' fill='%s'/>" % (R, p.fills[i]))
        else:
            s.append("<path d='M0 0 L%.2f %.2f A%d %d 0 %d 1 %.2f %.2f Z' fill='%s'/>"
                     % (x1, y1, R, R, large, x2, y2, p.fills[i]))
        am = (a0 + a1) / 2
        sn, cs = math.sin(math.radians(am)), math.cos(math.radians(am))
        rl = R + 7 + 5 * abs(cs)
        lx, ly = sn * rl, -cs * rl + 5
        lab = p.labels[i]
        w = tw(plain(lab), fs)
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
    if len(p.parts) > 1:
        for k in p.parts:
            x, y = pt(a0, R)
            s.append("<line x1='0' y1='0' x2='%.2f' y2='%.2f' stroke='%s' stroke-width='1.6'/>" % (x, y, INK))
            a0 += 360.0 * k / p.n
    s.append("<circle cx='0' cy='0' r='%d' fill='none' stroke='%s' stroke-width='1.8'/>" % (R, INK))
    # labels must not overlap each other
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


def pie_svg(*pies, label=None):
    """One or more pie charts side by side in one SVG."""
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
    lab = label or ("pie charts: " if len(pies) > 1 else "pie chart: ") + " and ".join(p.title.lower() for p in pies)
    return svg_wrap(-6, int(math.floor(top)) - 4, int(math.ceil(W)) + 12, int(math.ceil(bot - top)) + 10, "".join(body), lab)


# ------------------------------------------------------------ line graphs
class LG:
    def __init__(self, title, xl, xt, yt, series, ymin, ymax, lstep, gstep, dots=True, names=None, u=("", "")):
        self.title, self.xl, self.xt, self.yt = title, xl, xt, yt
        self.series, self.ymin, self.ymax, self.lstep, self.gstep = series, ymin, ymax, lstep, gstep
        self.dots, self.names, self.u = dots, names, u
        for v in series:
            assert len(v) == len(xl)
            assert all(ymin <= x <= ymax for x in v)
        assert (ymax - ymin) % gstep == 0 and lstep % gstep == 0 and ymin % lstep == 0

    def v(self, x):
        return "%s%s" % (num(x), self.u[0])

    def svg(self):
        fs = 14
        nt = (self.ymax - self.ymin) // self.gstep
        gy = max(9, min(20, int(round(150.0 / nt))))
        ph = nt * gy
        ylabs = [num(v) for v in range(self.ymin, self.ymax + 1, self.lstep)]
        slot = max(44, max(tw(c, fs) for c in self.xl) + 8)
        x0 = 24 + max(tw(c, fs) for c in ylabs) + 8
        n = len(self.xl)
        pw = slot * (n - 1)
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
        if self.ymin < 0:
            s.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='1.5'/>" % (x0, Y(0), x0 + pw, Y(0), INK))
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
            if self.dots:
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


# ------------------------------------------------------------ set 1: pie charts as fractions
def frac_wrongs(p, n, k, neg=False):
    """Typical mistakes: complement, 1 out of the number of groups, one slice too many/few, slices as denominator."""
    right = F(n - p, n) if neg else F(p, n)
    c = [F(p, n) if neg else F(n - p, n), F(1, k), F(p + 1, n), F(p - 1, n), F(1, p) if p > 1 else F(1, n + 1),
         F(p, n + 2), F(1, n)]
    return right, [x for x in c if 0 < x < 1]


def frac_ex(p, n, names, neg=False):
    nm = " and ".join(names)
    s = "The circle is split into %d equal parts. %s %s %s of them" % (n, nm, "has" if len(names) == 1 else "have", p)
    if neg:
        s += ", so %d − %d = %d parts are not %s: %s" % (n, p, n - p, nm, fr(n - p, n))
        v = F(n - p, n)
    else:
        s += ": %s" % fr(p, n)
        v = F(p, n)
    if v.denominator != n:
        s += " = %s" % frs(v)
    return s + "."


def set_fractions():
    its = []
    sport = Pie("Favourite sport", ["Football", "Netball", "Swimming", "Cricket"], [4, 2, 1, 1])
    colour = Pie("Favourite colour", ["Red", "Blue", "Green", "Yellow", "Purple"], [3, 2, 1, 1, 1])
    travel = Pie("How we travel to school", ["Walk", "Car", "Bus"], [3, 2, 1])
    pets = Pie("Pets", ["Dog", "Cat", "Fish", "Rabbit"], [6, 3, 2, 1])
    fruit = Pie("Favourite fruit", ["Apple", "Banana", "Grapes", "Pear"], [1, 2, 4, 1])
    dinner = Pie("School dinners", ["Pasta", "Curry", "Pizza", "Roast"], [4, 3, 2, 1])
    season = Pie("Favourite season", ["Summer", "Spring", "Autumn", "Winter"], [5, 3, 2, 2])
    subject = Pie("Favourite subject", ["Maths", "Science", "PE", "Art"], [2, 3, 1, 2])

    def fq(pie, names, q, neg=False):
        p = sum(pie.parts_of(c) for c in names)
        right, wr = frac_wrongs(p, pie.n, len(pie.cats), neg)
        its.append(mcqv(fig(pie_svg(pie)) + q, right, wr, frs, frac_ex(p, pie.n, names, neg)))

    def which(pie, c, q):
        p = pie.parts_of(c)
        others = [x for x in pie.cats if x != c]
        others.sort(key=lambda x: abs(pie.parts_of(x) - p))
        assert all(pie.parts_of(x) != p for x in others)
        its.append(mcq(fig(pie_svg(pie)) + q, c, others,
                       "The circle is split into %d equal parts. %s has %d of them: %s%s."
                       % (pie.n, c, p, fr(p, pie.n), "" if F(p, pie.n).denominator == pie.n else " = " + frs(F(p, pie.n)))))

    fq(sport, ["Football"], "What fraction of the pupils chose football?")
    which(sport, "Netball", "Which sport was chosen by a quarter of the pupils?")
    which(colour, "Blue", "Which colour was chosen by a quarter of the pupils?")
    fq(colour, ["Red"], "What fraction of the pupils chose red?")
    fq(travel, ["Walk"], "What fraction of the pupils walk to school?")
    fq(travel, ["Car"], "What fraction of the pupils come by car?")
    pairs = ["Car and Bus", "Walk and Bus", "Walk and Car", "Bus only"]
    its.append(mcq(fig(pie_svg(travel)) + "Which ways of travelling make half of the pie chart together?", pairs[0], pairs[1:],
                   "Half of 6 parts is 3 parts. Car has 2 parts and Bus has 1 part: 2 + 1 = 3, so Car and Bus make %s = %s."
                   % (fr(3, 6), frs(F(1, 2)))))
    fq(pets, ["Cat"], "What fraction of the pupils have a cat?")
    which(pets, "Fish", "Which pet is %s of the pie chart?" % frs(F(1, 6)))
    fq(colour, ["Blue"], "What fraction of the pupils did not choose blue?", neg=True)
    fq(fruit, ["Apple", "Pear"], "What fraction of the pupils chose an apple or a pear?")
    which(fruit, "Grapes", "Which fruit was chosen by half of the pupils?")
    fq(dinner, ["Pasta"], "What fraction of the pupils chose pasta?")
    fq(pets, ["Dog", "Cat"], "What fraction of the pupils have a dog or a cat?")
    fq(dinner, ["Curry", "Pizza"], "What fraction of the pupils chose curry or pizza?")
    fq(season, ["Spring"], "What fraction of the pupils chose spring?")
    which(season, "Summer", "Which season was chosen by %s of the pupils?" % frs(F(5, 12)))
    which(subject, "Science", "Which subject was chosen by %s of the pupils?" % frs(F(3, 8)))
    fq(subject, ["Maths", "Art"], "What fraction of the pupils chose maths or art?")
    fq(subject, ["Science"], "What fraction of the pupils did not choose science?", neg=True)
    return {"title": "Read pie charts as fractions", "items": its}


# ------------------------------------------------------------ set 2: amounts and percentages
def set_amounts():
    its = []
    P = lambda v: unit(v, "pupil", "pupils")
    travel = Pie("How 40 pupils travel to school", ["Walk", "Car", "Bus", "Bike"], [4, 2, 1, 1])
    f = fig(pie_svg(travel))
    its.append(mcqv(f + "How many pupils come by car?", 10, [4, 25, 20, 30], P,
                    "Car is 2 of the 8 equal parts: %s = %s of the pie. %s of 40 = 40 ÷ 4 = 10 pupils."
                    % (fr(2, 8), frs(F(1, 4)), frs(F(1, 4)))))
    its.append(mcqv(f + "How many pupils walk to school?", 20, [4, 50, 10, 36], P,
                    "Walk is half of the pie. Half of 40 = 40 ÷ 2 = 20 pupils."))
    its.append(mcqv(f + "How many pupils cycle to school?", 5, [8, 10, 35, 1], P,
                    "Bike is 1 of the 8 equal parts: %s of 40 = 40 ÷ 8 = 5 pupils." % fr(1, 8)))
    crisps = Pie("Favourite ice lolly", ["Lemon", "Orange", "Cola", "Cherry"], [4, 3, 2, 1],
                 ticks=False, labels=["Lemon 40%", "Orange 30%", "Cola 20%", "Cherry 10%"])
    f = fig(pie_svg(crisps))
    its.append(mcqv(f + "200 pupils chose their favourite ice lolly. How many chose orange?", 60, [30, 140, 80, 600], P,
                    "10% of 200 = 200 ÷ 10 = 20. So 30% = 3 × 20 = 60 pupils. (30% is not 30 pupils: there are 200 pupils, not 100.)"))
    its.append(mcqv(f + "200 pupils chose their favourite ice lolly. How many more chose lemon than cherry?", 60,
                    [30, 100, 20, 80], P,
                    "10% of 200 = 20. Lemon: 40% = 80. Cherry: 10% = 20. 80 − 20 = 60 pupils. "
                    "(Or: 40% − 10% = 30%, and 30% of 200 = 60.)"))
    hol = Pie("Holidays of 50 families", ["Spain", "France", "UK", "Italy"], [4, 3, 2, 1])
    f = fig(pie_svg(hol))
    its.append(mcqv(f + "What percentage of the families went to France?", 30, [3, 33, 40, 15], pct,
                    "The circle is split into 10 equal parts, so each part is 10%. France has 3 parts: 3 × 10% = 30%."))
    its.append(mcqv(f + "How many of the 50 families went to Spain?", 20, [40, 4, 10, 25],
                    lambda v: unit(v, "family", "families"),
                    "Spain has 4 of the 10 parts: %s = 40%%. 10%% of 50 = 5, so 40%% = 4 × 5 = 20 families." % fr(4, 10)))
    fruit = Pie("Favourite fruit of 60 pupils", ["Apple", "Banana", "Grapes"], [2, 1, 3])
    its.append(mcqv(fig(pie_svg(fruit)) + "How many pupils chose apples?", 20, [3, 30, 40, 2], P,
                    "Apple is 2 of the 6 equal parts: %s = %s. %s of 60 = 60 ÷ 3 = 20 pupils." % (fr(2, 6), frs(F(1, 3)), frs(F(1, 3)))))
    swim = Pie("Favourite sport", ["Swimming", "Football", "Tennis", "Dance"], [2, 3, 2, 1],
               ticks=True)
    its.append(mcqv(fig(pie_svg(swim)) + "12 pupils chose swimming. How many pupils were asked altogether?", 48, [3, 16, 24, 36], P,
                    "Swimming is 2 of the 8 parts = %s of the pie. If %s is 12 pupils, the whole is 4 × 12 = 48 pupils."
                    % (frs(F(1, 4)), frs(F(1, 4)))))
    rugby = Pie("Favourite sport", ["Rugby", "Football", "Netball", "Hockey"], [1, 4, 3, 2], ticks=False,
                labels=["Rugby 10%", "Football 40%", "Netball 30%", "Hockey 20%"])
    its.append(mcqv(fig(pie_svg(rugby)) + "9 pupils chose rugby. How many pupils were asked altogether?", 90, [19, 900, 10, F(9, 10)], P,
                    "10% is 9 pupils. 100% is 10 times as many: 10 × 9 = 90 pupils."))
    drinks = Pie("Favourite hot drink of 300 adults", ["Tea", "Coffee", "Hot chocolate"], [1, 2, 1], ticks=False,
                 labels=["Tea 25%", "Coffee 50%", "Hot chocolate 25%"])
    its.append(mcqv(fig(pie_svg(drinks)) + "How many adults chose tea?", 75, [25, 225, 150, 100],
                    lambda v: unit(v, "adult", "adults"),
                    "25%% = %s. %s of 300 = 300 ÷ 4 = 75 adults." % (frs(F(1, 4)), frs(F(1, 4)))))
    lunch = Pie("Lunch of 64 pupils", ["School dinner", "Packed lunch", "Home"], [4, 3, 1])
    f = fig(pie_svg(lunch))
    its.append(mcqv(f + "How many pupils have a packed lunch?", 24, [3, 8, 40, 32], P,
                    "Packed lunch is 3 of the 8 equal parts: %s. 64 ÷ 8 = 8, so %s = 3 × 8 = 24 pupils." % (fr(3, 8), fr(3, 8))))
    its.append(mcqv(f + "How many pupils go home for lunch?", 8, [1, 56, 16, 24], P,
                    "Home is 1 of the 8 equal parts: %s of 64 = 64 ÷ 8 = 8 pupils." % fr(1, 8)))
    juice = Pie("Favourite drink of 80 pupils", ["Juice", "Milk", "Water"], [9, 6, 5], ticks=False,
                labels=["Juice 45%", "Milk 30%", "Water 25%"])
    f = fig(pie_svg(juice))
    its.append(mcqv(f + "How many pupils chose juice?", 36, [45, 44, 40, 9], P,
                    "10% of 80 = 8, and 5% of 80 = 4. 45% = 40% + 5% = 4 × 8 + 4 = 32 + 4 = 36 pupils."))
    its.append(mcqv(f + "How many pupils chose milk?", 24, [30, 56, 20, 3], P,
                    "10% of 80 = 8. 30% = 3 × 8 = 24 pupils."))
    cars = Pie("Colours of 100 cars", ["Black", "Silver", "White", "Red"], [3, 4, 2, 1])
    f = fig(pie_svg(cars))
    its.append(mcqv(f + "How many of the cars are silver?", 40, [4, 25, 60, 30], lambda v: unit(v, "car", "cars"),
                    "Each of the 10 equal parts is 10%. Silver has 4 parts = 40%. 40% of 100 = 40 cars."))
    its.append(mcqv(f + "What percentage of the cars are not black?", 70, [30, 7, 60, 75], pct,
                    "Black is 3 of the 10 parts = 30%. Not black: 100% − 30% = 70%."))
    sport = Pie("Favourite sport of 120 pupils", ["Football", "Netball", "Swimming", "Dance"], [4, 3, 2, 3])
    its.append(mcqv(fig(pie_svg(sport)) + "How many pupils chose swimming?", 20, [2, 30, 100, 12], P,
                    "The circle has 12 equal parts. Swimming has 2: %s = %s. 120 ÷ 6 = 20 pupils." % (fr(2, 12), frs(F(1, 6)))))
    maths = Pie("Favourite subject of 30 pupils in 6B", ["Maths", "English", "Science", "Art"], [4, 3, 2, 1], ticks=False,
                labels=["Maths 40%", "English 30%", "Science 20%", "Art 10%"])
    its.append(mcqv(fig(pie_svg(maths)) + "How many pupils in 6B chose maths?", 12, [40, 18, 4, 10], P,
                    "10% of 30 = 3. 40% = 4 × 3 = 12 pupils."))
    its.append(mcqv("24 pupils chose their favourite lesson. 6 pupils chose art. What fraction of the pie chart is art?",
                    F(1, 4), [F(1, 6), F(3, 4), F(1, 3)], frs,
                    "Art is 6 out of all 24 pupils (not out of the other 18): %s. Divide both numbers by 6: %s." % (fr(6, 24), frs(F(1, 4)))))
    return {"title": "Pie charts: find amounts and percentages", "items": its}


# ------------------------------------------------------------ set 3: angles
def set_angles():
    its = []
    D = deg
    P = lambda v: unit(v, "pupil", "pupils")
    its.append(mcqv("All the angles in a pie chart add up to …", 360, [100, 180, 90], D,
                    "A pie chart is a whole circle, and the angles at the centre of a circle add up to 360°. (100 is for percentages.)"))
    its.append(mcqv("A pie chart shows 20 pupils. How many degrees stand for each pupil?", 18, [20, 5, 340], D,
                    "The whole circle is 360°. 360 ÷ 20 = 18°, so each pupil is 18°. (100 ÷ 20 = 5 uses 100, not 360.)"))
    its.append(mcqv("A pie chart shows 60 people. How many degrees stand for each person?", 6, [60, 300, F(18, 5)], D,
                    "360 ÷ 60 = 6, so each person is 6°."))
    its.append(mcqv("60 people were asked. 15 chose swimming. What angle should the swimming sector be?", 90, [15, 25, 4], D,
                    "Each person is 360 ÷ 60 = 6°. 15 × 6 = 90°. (Or: 15 out of 60 is %s, and %s of 360° = 90°.)"
                    % (frs(F(1, 4)), frs(F(1, 4)))))
    its.append(mcqv("24 pupils were asked. 8 chose cricket. What angle should the cricket sector be?", 120, [8, 33, 15], D,
                    "Each pupil is 360 ÷ 24 = 15°. 8 × 15 = 120°. (Or: 8 out of 24 is %s, and %s of 360° = 120°.)"
                    % (frs(F(1, 3)), frs(F(1, 3)))))
    its.append(mcqv("30 pupils were asked. 9 chose art. What angle should the art sector be?", 108, [9, 30, 12], D,
                    "Each pupil is 360 ÷ 30 = 12°. 9 × 12 = 108°."))
    its.append(mcqv("A sector of a pie chart has an angle of 90°. What fraction of the pie chart is it?", F(1, 4),
                    [F(9, 10), F(1, 3), F(3, 4)], frs,
                    "Compare with the whole circle: %s = %s. (%s uses 100, not 360.)" % (fr(90, 360), frs(F(1, 4)), fr(90, 100))))
    its.append(mcqv("A sector of a pie chart has an angle of 120°. What fraction of the pie chart is it?", F(1, 3),
                    [F(1, 4), F(2, 3), F(6, 5)], frs,
                    "%s = %s. Three sectors of 120° make 360°." % (fr(120, 360), frs(F(1, 3)))))
    its.append(mcqv("A sector of a pie chart has an angle of 45°. What percentage of the pie chart is it?", F(25, 2),
                    [45, 8, 12], pct,
                    "%s = %s. %s = 100%% ÷ 8 = 12.5%%." % (fr(45, 360), frs(F(1, 8)), frs(F(1, 8)))))
    its.append(mcqv("A sector is %s of a pie chart. What is its angle?" % frs(F(1, 6)), 60, [6, 30, 300], D,
                    "360 ÷ 6 = 60°."))
    its.append(mcqv("A sector is 25% of a pie chart. What is its angle?", 90, [25, 270, 50], D,
                    "25%% = %s. 360 ÷ 4 = 90°." % frs(F(1, 4))))
    pet = Pie("Pets", ["Dog", "Cat", "Fish", "Other"], [7, 9, 4, 4], ticks=False,
              labels=["Dog 105°", "Cat 135°", "Fish 60°", "Other ?"])
    its.append(mcqv(fig(pie_svg(pet)) + "What is the angle of the Other sector?", 60, [300, 120, 165], D,
                    "The angles add up to 360°. 105 + 135 + 60 = 300. 360 − 300 = 60°."))
    sp = Pie("Sports club", ["Football", "Tennis", "Swimming", "Hockey"], [10, 7, 4, 3], ticks=False,
             labels=["Football 150°", "Tennis 105°", "Swimming ?", "Hockey 45°"])
    its.append(mcqv(fig(pie_svg(sp)) + "What is the angle of the Swimming sector?", 60, [300, 105, 150, 15], D,
                    "150 + 105 + 45 = 300. The angles add up to 360°, so 360 − 300 = 60°."))
    fb = Pie("Favourite sport of 36 pupils", ["Football", "Netball", "Rugby"], [10, 9, 5], ticks=False,
             labels=["Football 150°", "Netball 135°", "Rugby 75°"])
    its.append(mcqv(fig(pie_svg(fb)) + "How many pupils chose football?", 15, [150, 10, 21], P,
                    "Each pupil is 360 ÷ 36 = 10°. 150 ÷ 10 = 15 pupils."))
    its.append(mcqv("45 pupils were asked. 18 chose football. What angle should the football sector be?", 144, [18, 40, 8], D,
                    "Each pupil is 360 ÷ 45 = 8°. 18 × 8 = 144°."))
    its.append(mcqv("In a pie chart each pupil is 12°. The netball sector is 84°. How many pupils chose netball?", 7,
                    [72, 96, 84], P, "84 ÷ 12 = 7 pupils. Check: 7 × 12 = 84°."))
    its.append(mcqv("In a pie chart, a sector of 72° stands for 10 people. How many people does the whole pie chart show?", 50,
                    [82, 36, 720], lambda v: unit(v, "person", "people"),
                    "72° × 5 = 360°, so the whole pie chart is 5 times as big as the sector: 5 × 10 = 50 people."))
    tr = Pie("How 90 pupils travel to school", ["Bus", "Walk", "Car"], [3, 4, 2], ticks=False,
             labels=["Bus 120°", "Walk 160°", "Car 80°"])
    its.append(mcqv(fig(pie_svg(tr)) + "How many more pupils walk than come by car?", 20, [80, 40, 30], P,
                    "Each pupil is 360 ÷ 90 = 4°. Walk: 160 ÷ 4 = 40. Car: 80 ÷ 4 = 20. 40 − 20 = 20 pupils."))
    its.append(mcqv("40 pupils were asked about pets: cat 10, dog 14, fish 6, other 10. What angle should the dog sector be?",
                    126, [14, 35, 140], D, "Each pupil is 360 ÷ 40 = 9°. 14 × 9 = 126°."))
    walk = Pie("How 18 pupils travel to school", ["Walk", "Car", "Bus"], [7, 6, 5], ticks=False,
               labels=["Walk 140°", "Car 120°", "Bus 100°"])
    its.append(mcqv(fig(pie_svg(walk)) + "How many pupils walk?", 7, [140, 14, 11], P,
                    "Each pupil is 360 ÷ 18 = 20°. 140 ÷ 20 = 7 pupils."))
    return {"title": "Angles in pie charts", "items": its}


# ------------------------------------------------------------ set 4: line graphs
def times(h0, step, n):
    out = []
    for k in range(n):
        m = h0 * 60 + k * step
        out.append("%02d:%02d" % (m // 60, m % 60))
    return out


C = (" °C", " °C")
CM = (" cm", " cm")
KM = (" km", " km")
TEMP = LG("Temperature on a winter day", times(6, 120, 7), "Time", "Temperature (°C)",
          [[-3, -2, 2, 5, 6, 4, 1]], -4, 8, 2, 1, u=C)
PLANT = LG("Height of a bean plant", [str(w) for w in range(7)], "Week", "Height (cm)",
           [[2, 4, 8, 14, 18, 22, 24]], 0, 30, 10, 2, u=CM)
BIKE = LG("Kai’s bike ride", times(9, 20, 7), "Time", "Distance (km)",
          [[0, 6, 12, 12, 20, 26, 30]], 0, 30, 10, 2, u=KM)
CITY = LG("Average temperature", ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul"], "Month", "Temperature (°C)",
          [[4, 6, 8, 12, 14, 18, 20], [4, 4, 6, 8, 10, 14, 16]], 0, 20, 10, 2, names=["London", "Edinburgh"], u=C)
KETTLE = LG("Water cooling after boiling", [str(m) for m in range(0, 35, 5)], "Minutes", "Temperature (°C)",
            [[100, 80, 65, 55, 50, 45, 40]], 0, 100, 20, 10, u=C)
MILES = LG("Miles and kilometres", [str(m) for m in range(0, 60, 10)], "Miles", "Kilometres",
           [[0, 16, 32, 48, 64, 80]], 0, 80, 16, 8, dots=False, u=KM)


def set_line():
    its = []
    T, V = TEMP, TEMP.series[0]
    f = fig(T.svg())
    its.append(mcqv(f + "What was the temperature at 10:00?", 2, [-2, 1, 3, 4], T.v,
                    "Go up from 10:00 to the point, then across. Each small square is 1 °C. The point is 2 squares above 0, so 2 °C.",
                    allow_zero=True))
    its.append(mcqv(f + "What was the lowest temperature?", -3, [3, -2, -4, 1], T.v,
                    "The lowest point is at 06:00. It is 3 squares below 0, so −3 °C.", allow_zero=True))
    its.append(mcqv(f + "How much warmer was it at 14:00 than at 06:00?", 9, [3, 6, 4], T.v,
                    "14:00: 6 °C. 06:00: −3 °C. From −3 up to 0 is 3, and from 0 up to 6 is 6: 3 + 6 = 9 °C."))
    labs = ["%s to %s" % (T.xl[k], T.xl[k + 1]) for k in range(6)]
    ups = [V[k + 1] - V[k] for k in range(6)]
    k = ups.index(max(ups))
    assert ups.count(max(ups)) == 1 and k == 1
    its.append(mcq(f + "Between which two times did the temperature rise the most?", labs[1], [labs[2], labs[3], labs[0]],
                   "Look for the steepest part going up. From 08:00 to 10:00 it rose from −2 °C to 2 °C: 4 °C. "
                   "From 10:00 to 12:00 it rose only 3 °C."))
    its.append(mcq(f + "At what time was the temperature 5 °C?", "12:00", ["14:00", "16:00", "10:00"],
                   "Find 5 on the scale and go across to the line. The point at 5 °C is above 12:00."))
    T, V = PLANT, PLANT.series[0]
    f = fig(T.svg())
    its.append(mcqv(f + "How tall was the bean plant in week 3?", 14, [12, 16, 7, 13], T.v,
                    "The numbers go up in 10s, but each small square is 2 cm. Week 3 is 2 squares above 10: 10 + 2 + 2 = 14 cm. "
                    "(7 counts the squares as 1 cm each.)"))
    its.append(mcqv(f + "How much did the plant grow from week 2 to week 5?", 14, [22, 30, 12, 8], T.v,
                    "Week 2: 8 cm. Week 5: 22 cm. 22 − 8 = 14 cm. (22 cm is the height, not the growth.)"))
    wl = ["Week %d to week %d" % (k, k + 1) for k in range(6)]
    ups = [V[k + 1] - V[k] for k in range(6)]
    assert ups.index(max(ups)) == 2 and ups.count(max(ups)) == 1
    its.append(mcq(f + "Between which two weeks did the plant grow the most?", wl[2], [wl[5], wl[3], wl[1]],
                   "The steepest part of the line is from week 2 (8 cm) to week 3 (14 cm): 6 cm. "
                   "The highest point (week 6) is the tallest, not the fastest growth."))
    its.append(mcq(f + "In which week did the plant first reach 18 cm?", "Week 4", ["Week 5", "Week 3", "Week 6"],
                   "Find 18 cm on the scale (4 small squares above 10) and go across to the line, then down: week 4."))
    T, V = BIKE, BIKE.series[0]
    f = fig(T.svg())
    its.append(mcqv(f + "How far had Kai cycled by 10:20?", 20, [26, 10, 12, 4], T.v,
                    "Go up from 10:20 to the point. It is on the line for 20, so 20 km."))
    bl = ["%s to %s" % (T.xl[k], T.xl[k + 1]) for k in range(6)]
    its.append(mcq(f + "Kai stopped for a rest. When was he resting?", bl[2], [bl[1], bl[3], bl[5]],
                   "When Kai stops, the distance does not change, so the line is flat. From 09:40 to 10:00 it stays at 12 km."))
    ups = [V[k + 1] - V[k] for k in range(6)]
    assert ups.index(max(ups)) == 3 and ups.count(max(ups)) == 1
    its.append(mcq(f + "When was Kai cycling fastest?", bl[3], [bl[5], bl[0], bl[2]],
                   "Fastest means the most distance in the same time: the steepest part. From 10:00 to 10:20 he went "
                   "20 − 12 = 8 km. In every other 20 minutes he went 6 km or less."))
    its.append(mcqv(f + "How far did Kai cycle between 09:20 and 10:40?", 20, [26, 32, 6, 14], T.v,
                    "09:20: 6 km. 10:40: 26 km. 26 − 6 = 20 km."))
    T = CITY
    f = fig(T.svg())
    its.append(mcqv(f + "How much warmer was London than Edinburgh in April?", 4, [12, 8, 20, 2], T.v,
                    "April: London 12 °C, Edinburgh 8 °C. 12 − 8 = 4 °C."))
    its.append(mcq(f + "In which month was the temperature the same in both cities?", "January", ["July", "February", "June"],
                   "The two lines meet at January: both are 4 °C."))
    its.append(mcqv(f + "By how much did Edinburgh’s temperature rise from February to June?", 10, [14, 12, 18, 4], T.v,
                    "Use the dashed line (Edinburgh). February: 4 °C. June: 14 °C. 14 − 4 = 10 °C. "
                    "(12 °C uses the London line.)"))
    T = KETTLE
    f = fig(T.svg())
    its.append(mcqv(f + "What was the temperature of the water after 10 minutes?", 65, [60, 70, 75], T.v,
                    "The labels go up in 20s, so each square is 10 °C. At 10 minutes the point is halfway between 60 and 70: 65 °C."))
    its.append(mcqv(f + "How much did the water cool in the first 5 minutes?", 20, [80, 180, 10, 15], T.v,
                    "0 minutes: 100 °C. 5 minutes: 80 °C. 100 − 80 = 20 °C. After that it cools more slowly."))
    T = MILES
    f = fig(T.svg())
    its.append(mcqv(f + "Use the graph to change 25 miles into kilometres.", 40, [25, 50, 32, 48], T.v,
                    "25 miles is halfway between 20 and 30. Go up to the line and across: 40 km. "
                    "(The labels go up in 16s and each square is 8 km.)"))
    its.append(mcqv(f + "Use the graph to change 64 km into miles.", 40, [64, 50, 30, 102],
                    lambda v: unit(v, "mile", "miles"),
                    "Find 64 on the kilometres scale, go across to the line, then down: 40 miles."))
    return {"title": "Read and interpret line graphs", "items": its}


# ------------------------------------------------------------ set 5: compare and solve
def set_problems():
    its = []
    P = lambda v: unit(v, "pupil", "pupils")
    a6 = Pie("6A: 24 pupils", ["Football", "Netball", "Tennis"], [4, 1, 1])
    b6 = Pie("6B: 60 pupils", ["Football", "Netball", "Tennis"], [1, 1, 1])
    f = fig(pie_svg(a6, b6))
    its.append(mcq(f + "Which class has more pupils who chose football?", "6B", ["6A", "Both the same", "You cannot tell"],
                   "6A: %s of 24 = 16 pupils. 6B: %s of 60 = 20 pupils. 6B has more, even though its sector is smaller, "
                   "because 6B has more pupils." % (frs(F(2, 3)), frs(F(1, 3)))))
    its.append(mcqv(f + "How many more pupils chose netball in 6B than in 6A?", 16, [4, 20, 56, 24], P,
                    "6A netball: %s of 24 = 4. 6B netball: %s of 60 = 20. 20 − 4 = 16 pupils." % (frs(F(1, 6)), frs(F(1, 3)))))
    sa = Pie("School A: 120 pupils", ["Walk", "Car", "Bus"], [1, 2, 1])
    sb = Pie("School B: 300 pupils", ["Walk", "Car", "Bus"], [1, 3, 2])
    f = fig(pie_svg(sa, sb))
    its.append(mcq(f + "Mohammed says, “More pupils walk at School A, because its Walk sector is bigger.” Is he right?",
                   "No: 30 at A, 50 at B", ["Yes: 50 at A, 30 at B", "Yes: the sector is bigger", "No: 50 at A, 30 at B"],
                   "School A: %s of 120 = 30. School B: %s of 300 = 50. The sector size only shows the fraction, "
                   "not the number of pupils." % (frs(F(1, 4)), frs(F(1, 6)))))
    money = Pie("How Ruby spent £32", ["Books", "Cinema", "Sweets"], [3, 4, 1])
    f = fig(pie_svg(money))
    its.append(mcqv(f + "Ruby spent £32. How much did she spend on books?", 12, [3, 20, 4, 8], pounds,
                    "£32 ÷ 8 = £4 for each of the 8 parts. Books has 3 parts: 3 × £4 = £12."))
    its.append(mcqv(f + "How much did Ruby spend on books and sweets together?", 16, [12, 20, 4], pounds,
                    "Books and sweets have 3 + 1 = 4 of the 8 parts: half of £32 = £16."))
    its.append(mcq("Which graph is best to show how the temperature changes during a day?", "Line graph",
                   ["Pie chart", "Pictogram", "Venn diagram"],
                   "Temperature changes over time. A line graph joins the readings so you can see it rise and fall."))
    its.append(mcq("Which graph is best to show what fraction of a class chose each school dinner?", "Pie chart",
                   ["Line graph", "Tally chart", "Carroll diagram"],
                   "A pie chart shows how a whole is split into parts, so you can see each fraction."))
    its.append(mcq("Which sentence about a pie chart is true?", "The angles add up to 360°",
                   ["The angles add up to 100°", "A bigger sector always means more people", "Each sector is 1 person"],
                   "A pie chart is a circle, so the angles add up to 360°. A bigger sector is a bigger fraction, but only more "
                   "people if the totals are the same."))
    sales = LG("Drinks sold at the café", ["Jan", "Feb", "Mar", "Apr", "May", "Jun"], "Month", "Drinks sold",
               [[120, 110, 90, 60, 40, 20], [20, 30, 60, 80, 110, 140]], 0, 160, 40, 20,
               names=["Hot chocolate", "Ice cream"])
    f = fig(sales.svg())
    its.append(mcq(f + "In which month did the café first sell more ice creams than hot chocolates?", "April",
                   ["March", "May", "June"],
                   "In March hot chocolate was 90 and ice cream 60, so hot chocolate was still more. In April ice cream was 80 and hot chocolate 60, "
                   "so April is the first month."))
    its.append(mcqv(f + "How many more ice creams than hot chocolates were sold in June?", 120, [140, 160, 20, 100],
                    lambda v: unit(v, "drink", "drinks"),
                    "Each square is 20. June: ice cream 140, hot chocolate 20. 140 − 20 = 120."))
    zoo = Pie("360 visitors: favourite animal", ["Penguins", "Lions", "Monkeys", "Giraffes"], [3, 4, 3, 2], ticks=False,
              labels=["Penguins 90°", "Lions 120°", "Monkeys 90°", "Giraffes 60°"])
    its.append(mcqv(fig(pie_svg(zoo)) + "How many visitors chose giraffes?", 60, [6, 300, 30, 10],
                    lambda v: unit(v, "visitor", "visitors"),
                    "360 visitors and 360°, so each visitor is 1°. The giraffes sector is 60°, so 60 visitors."))
    bus = Pie("How pupils travel to school", ["Bus", "Car", "Walk"], [5, 3, 4], ticks=False,
              labels=["Bus 150°", "Car 90°", "Walk 120°"])
    its.append(mcqv(fig(pie_svg(bus)) + "30 pupils walk. How many pupils are in the survey altogether?", 90,
                    [120, 360, 60, 40], P,
                    "Walk is 120°, which is %s of 360°. If %s is 30 pupils, the whole is 3 × 30 = 90 pupils."
                    % (frs(F(1, 3)), frs(F(1, 3)))))
    pets = Pie("Pupils in Isla’s class", ["No pets", "Dog", "Cat", "Other"], [5, 7, 6, 2], ticks=False,
               labels=["No pets 25%", "Dog 35%", "Cat 30%", "Other 10%"])
    its.append(mcqv(fig(pie_svg(pets)) + "7 pupils have no pets. How many pupils are in Isla’s class?", 28,
                    [32, 175, 21, 7], P, "25%% = %s. If %s is 7 pupils, the whole class is 4 × 7 = 28 pupils."
                    % (frs(F(1, 4)), frs(F(1, 4)))))
    y5 = Pie("Year 5: 80 pupils", ["Art", "Music", "PE"], [1, 1, 2], ticks=False, labels=["Art 25%", "Music 25%", "PE 50%"])
    y6 = Pie("Year 6: 60 pupils", ["Art", "Music", "PE"], [3, 3, 4], ticks=False, labels=["Art 30%", "Music 30%", "PE 40%"])
    f = fig(pie_svg(y5, y6))
    its.append(mcq(f + "Which year group has more pupils who chose art?", "Year 5", ["Year 6", "Both the same", "You cannot tell"],
                   "Year 5: 25% of 80 = 20 pupils. Year 6: 30% of 60 = 18 pupils. Year 6 has the bigger percentage, "
                   "but Year 5 has more pupils."))
    its.append(mcqv(f + "How many pupils chose PE altogether in Year 5 and Year 6?", 64, [90, 40, 24, 140], P,
                    "Year 5: 50% of 80 = 40. Year 6: 40% of 60 = 24. 40 + 24 = 64 pupils. (90 adds the percentages.)"))
    its.append(mcqv(fig(PLANT.svg()) + "After week 6, the plant keeps growing at the same rate as from week 5 to week 6. "
                    "How tall will it be in week 8?", 28, [26, 32, 30, 24], PLANT.v,
                    "Week 5: 22 cm. Week 6: 24 cm. It grows 2 cm a week. Week 7: 26 cm. Week 8: 28 cm."))
    its.append(mcqv("1,200 people voted. In the pie chart, the Yes sector is %s of the circle. How many people voted Yes?"
                    % frs(F(3, 8)), 450, [400, 750, 150, 375], lambda v: unit(v, "person", "people"),
                    "1,200 ÷ 8 = 150, so %s is 150 people. %s = 3 × 150 = 450 people." % (fr(1, 8), fr(3, 8))))
    its.append(mcqv("Pie chart A shows 40 pupils and pie chart B shows 100 pupils. Both have a Walk sector of 90°. "
                    "How many more pupils walk in B than in A?", 15, [0, 60, 25, 10], P,
                    "90° is %s of a pie chart. A: %s of 40 = 10. B: %s of 100 = 25. 25 − 10 = 15 pupils. "
                    "The same angle does not mean the same number." % (frs(F(1, 4)), frs(F(1, 4)), frs(F(1, 4))),
                    allow_zero=True))
    euro = LG("Pounds and euros", [str(m) for m in range(0, 60, 10)], "Pounds (£)", "Euros (€)",
              [[0, 12, 24, 36, 48, 60]], 0, 60, 12, 6, dots=False)
    its.append(mcq(fig(euro.svg()) + "Grace changes £35 into euros before her holiday. How many euros does she get?", "€42",
                   ["€35", "€40", "€45"],
                   "£35 is halfway between £30 and £40. Go up to the line and across: halfway between €36 and €48 is €42. "
                   "(Each square is €6.)"))
    day = Pie("Harry’s school day (24 hours)", ["Sleep", "School", "Play", "Other"], [5, 3, 2, 2], ticks=False,
              labels=["Sleep 150°", "School 90°", "Play 60°", "Other 60°"])
    its.append(mcqv(fig(pie_svg(day)) + "How many more hours does Harry spend sleeping than at school?", 4,
                    [60, 10, 16, 6], lambda v: unit(v, "hour", "hours"),
                    "24 hours = 360°, so 1 hour = 360 ÷ 24 = 15°. Sleep: 150 ÷ 15 = 10 hours. School: 90 ÷ 15 = 6 hours. "
                    "10 − 6 = 4 hours."))
    return {"title": "Compare pie charts and solve problems", "items": its}


# ------------------------------------------------------------ lesson
def ex(title, q, s, a):
    return ("<div class='sn-ex'><span class='sn-ex-t'>%s</span><p class='sn-ex-q'>%s</p>"
            "<p class='sn-ex-s'>%s</p><p class='sn-ex-a'>Answer: %s</p></div>" % (title, q, s, a))


def table(head, rows, cls="sn-table"):
    h = "".join("<th>%s</th>" % x for x in head)
    b = "".join("<tr>" + "".join("<td>%s</td>" % c for c in r) + "</tr>" for r in rows)
    return "<div class='sn-tw'><table class='%s'><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>" % (cls, h, b)


def body_html():
    sport = Pie("Favourite sport of 40 pupils", ["Football", "Netball", "Swimming", "Cricket"], [4, 2, 1, 1])
    temp = LG("Temperature on a spring day", times(8, 120, 6), "Time", "Temperature (°C)",
              [[4, 7, 12, 14, 11, 8]], 0, 16, 4, 1, u=C)
    return (
        "<h2>A pie chart shows parts of a whole</h2>"
        "<p>A pie chart is a circle split into <b>sectors</b>. The whole circle is everyone in the survey. "
        "Each sector shows a <b>fraction</b> of the total, not a number of people.</p>"
        "<figure class='sn-fig'>" + pie_svg(sport) +
        "<figcaption>The circle is split into 8 equal parts. Football has 4 of them, so half of the pupils chose football.</figcaption></figure>" +
        ex("Example 1", "How many of the 40 pupils chose netball?",
           "Netball is 2 of the 8 parts = %s. %s of 40 = 40 ÷ 4 = 10." % (frs(F(1, 4)), frs(F(1, 4))), "10 pupils") +
        "<h2>Angles in a pie chart</h2>"
        "<p>The angles at the centre add up to <b>360°</b>. To draw a pie chart, find how many degrees each person is worth: "
        "360 ÷ total.</p>" +
        table(["Sport", "Pupils", "Angle (9° each)"], [["Football", "20", "20 × 9 = 180°"], ["Netball", "10", "10 × 9 = 90°"],
                                                       ["Swimming", "5", "5 × 9 = 45°"], ["Cricket", "5", "5 × 9 = 45°"],
                                                       ["Total", "40", "360°"]]) +
        ex("Example 2", "60 people were asked. 15 chose tennis. What angle is the tennis sector?",
           "360 ÷ 60 = 6° for each person. 15 × 6 = 90°.", "90°") +
        "<p>To go back from an angle to people, divide: a sector of 120° with 6° for each person is 120 ÷ 6 = 20 people.</p>"
        "<h2>Read a line graph</h2>"
        "<p>A line graph shows how something changes over time. First check the <b>scale</b>: what is each small square worth? "
        "Go up from the bottom axis to the line, then across to the scale. A steeper line means a faster change. "
        "A flat line means no change.</p>"
        "<figure class='sn-fig'>" + temp.svg() +
        "<figcaption>The labels go up in 4s and each small square is 1 °C. At 12:00 it was 12 °C, the fastest rise was "
        "from 10:00 to 12:00 (5 °C).</figcaption></figure>" +
        ex("Example 3", "How much did the temperature fall from 14:00 to 18:00?", "14:00: 14 °C. 18:00: 8 °C. 14 − 8 = 6.", "6 °C") +
        "<h2>Comparing two pie charts</h2>"
        "<p>A bigger sector is a bigger <b>fraction</b>. It is only more people if both pie charts show the same total. "
        "Always work out the numbers: %s of 24 = 8, but %s of 60 = 15.</p>" % (frs(F(1, 3)), frs(F(1, 4))) +
        "<h2>Common mistakes</h2>" +
        table(["Mistake", "What to do instead"], [
            ["Reading a sector as a number of people", "Find the fraction, then the fraction of the total"],
            ["Using 100 instead of 360 for angles", "Angles add up to 360°; percentages add up to 100%"],
            ["Saying a bigger sector always means more people", "Check the totals of both pie charts"],
            ["Counting each small square on a line graph as 1", "Work out the scale: labels 0, 10, 20 with 5 squares means 2 each"],
            ["Choosing the highest point for the fastest change", "Fastest change is the steepest part of the line"],
        ])
    )


FAQ = [
    {"q": "How do you work out the angles for a pie chart?",
     "a": "Divide 360 by the total to find the angle for one item, then multiply by each amount. For 60 people, each person is 360 ÷ 60 = 6°, so 15 people get 15 × 6 = 90°."},
    {"q": "How do you read a pie chart in Year 6?",
     "a": "Work out what fraction or percentage of the circle the sector is, then find that fraction of the total. If a quarter of 40 pupils chose swimming, 40 ÷ 4 = 10 pupils chose swimming."},
    {"q": "What is a line graph used for?",
     "a": "A line graph shows how something changes over time, such as temperature, height or distance. A steeper line shows a faster change, and a flat line shows no change."},
    {"q": "Are pie charts and line graphs in the Year 6 SATs?",
     "a": "Yes, statistics questions can appear in the KS2 SATs reasoning papers. Pupils may be asked to read values, find fractions or angles of a pie chart, or compare and calculate from a line graph."},
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
    rnd = random.Random(6619)
    sets = [set_fractions(), set_amounts(), set_angles(), set_line(), set_problems()]
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
    return {
        "country": "uk", "subject": "maths", "grade": "year-6", "slug": "pie-charts-and-line-graphs", "sort": 19,
        "updated": UPDATED, "pdf_url": "",
        "title": "Pie Charts and Line Graphs",
        "seo_title": "Year 6 Pie Charts and Line Graphs Worksheets: Fractions, Angles and Reading Scales (Free, with Answers)",
        "short_title": "Pie charts and line graphs",
        "domain": "Statistics",
        "standard_code": "Year 6: Statistics",
        "standard_url": "https://www.gov.uk/government/publications/national-curriculum-in-england-mathematics-programmes-of-study",
        "standard_text": "Interpret and construct pie charts and line graphs and use these to solve problems.",
        "meta_desc": "Free Year 6 maths worksheets on pie charts and line graphs: read sectors as fractions and percentages, work out angles out of 360°, read line graph scales and compare two pie charts. 100 SATs-style questions with an answer key, following the National Curriculum.",
        "key_big": "A pie chart shows fractions of a whole. The whole circle is 360°.",
        "key_sub": "Find the fraction, then the fraction of the total. Each person is 360 ÷ total degrees. On a line graph, check what each small square is worth, and look for the steepest part for the fastest change.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }


def mark_large(u, pattern):
    """Tag pictures that must print larger (charts and graphs) so their labels stay readable."""
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
        mark_large(u, "(pie chart|line graph)")
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
