# -*- coding: utf-8 -*-
"""
Singapore Primary 3 Maths: Money (MOE 2021 Primary Mathematics Syllabus, Standard:
Primary 3 Money, adding and subtracting money in decimal notation)
  python3 tools/gen_sg_maths_p3_money.py
All amounts are whole numbers of cents (int), so every total, change and typical mistake is exact.
Singapore money: coins 5¢, 10¢, 20¢, 50¢, $1 (no 1¢), notes $2, $5, $10, $50, $100. Every amount is a
multiple of 5¢. Answers are written in decimal notation ($6.25); amounts under $1 as 45¢.
Coin, note, number line and price tag drawing adapted from gen_cabc_math_g3_money.py; bar models from
gen_sg_maths_p4_add_sub_decimals.py. HTML attributes use single quotes (no backslashes in the JSON).
"""
import json, os, random, re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "sg", "maths", "primary-3")
UPDATED = "2026-11-03"
GREEN = "#006633"
INK = "#2b2b2b"
RED = "#c0392b"
HEADFILL = "#cfe6d6"
PARTFILL = "#fde3c8"
ORANGE = "#b35900"
NB = " "
FONT = "Arial, Helvetica, sans-serif"
GIRLS = ["Siti", "Nurul", "Farah", "Mei Ling", "Hui Min", "Xin Yi", "Priya", "Devi", "Kavya", "Chloe", "Sarah"]
BOYS = ["Ali", "Ahmad", "Hafiz", "Wei Ming", "Jun Jie", "Zhi Hao", "Raju", "Kumar", "Arjun", "Ethan", "Ryan"]

# ------------------------------------------------------------ money facts
ORDER = ["N100", "N50", "N10", "N5", "N2", "C100", "C50", "C20", "C10", "C5"]     # biggest value first
VAL = {"N100": 10000, "N50": 5000, "N10": 1000, "N5": 500, "N2": 200,
       "C100": 100, "C50": 50, "C20": 20, "C10": 10, "C5": 5}
ONE = {"N100": "$100 note", "N50": "$50 note", "N10": "$10 note", "N5": "$5 note", "N2": "$2 note",
       "C100": "$1 coin", "C50": "50¢ coin", "C20": "20¢ coin", "C10": "10¢ coin", "C5": "5¢ coin"}
COIN = {"C5": 17, "C10": 18, "C20": 20, "C50": 22, "C100": 24}        # radius, in the order of the real sizes
COINFILL, COINEDGE = "#e4e6e9", "#6f767d"
NOTE = {"N2": ("#e3d4ef", "#5b2d8a"), "N5": ("#d3ecd2", "#2f7a2a"), "N10": ("#f6d0cf", "#a32020"),
        "N50": ("#cfe0f3", "#1f5f99"), "N100": ("#f8dfc0", "#a3560f")}
NOTE_W, NOTE_H = 80, 42


def lab(v):
    return "$%d" % (v // 100) if v >= 100 else "%d¢" % v


def f(c):
    """answer format: 45 -> '45¢', 625 -> '$6.25', 600 -> '$6.00'"""
    assert c > 0, c
    return "%d¢" % c if c < 100 else "$%d.%02d" % (c // 100, c % 100)


def d(c):
    """always dollars with 2 places: 45 -> '$0.45'"""
    return "$%d.%02d" % (c // 100, c % 100)


def dl(c):
    """dollars only, for whole dollar amounts in sentences: 1000 -> '$10'"""
    assert c % 100 == 0
    return "$%d" % (c // 100)


def short(c):
    """number line label: $4, $3.45, 45¢"""
    if c < 100:
        return "%d¢" % c
    return dl(c) if c % 100 == 0 else d(c)


def mval(s):
    s = re.sub(r"<[^>]+>", "", s)
    m = re.match(r"^\$(\d+)\.(\d\d)$", s) or re.match(r"^\$(\d+)()$", s)
    if m:
        return int(m.group(1)) * 100 + int(m.group(2) or 0)
    m = re.match(r"^(\d+)¢$", s)
    return int(m.group(1)) if m else None


def cap(s):
    return s[0].upper() + s[1:]


def total(toks):
    return sum(VAL[t] for t in toks)


def digs(n, k):
    return [(n // 10 ** i) % 10 for i in range(k)]


def from_digs(ds):
    return sum(x * 10 ** i for i, x in enumerate(ds))


# ------------------------------------------------------------ typical mistakes (cents in, (value, why) out)
def add_mistakes(a, b):
    da, ca, db, cb = a // 100, a % 100, b // 100, b % 100
    s = a + b
    out = []
    if ca + cb >= 100:
        out.append(("$%d.%d" % (da + db, ca + cb), "%%s writes %d¢ after the point instead of renaming 100¢ as $1" % (ca + cb)))
        out.append((s - 100, "%s forgets the $1 from renaming 100¢"))
    if ca % 10 + cb % 10 >= 10:
        out.append((s - 10, "%s loses the 10¢ from 5¢ + 5¢"))
    out.append((abs(a - b), "%s subtracts instead of adding"))
    if ca + cb < 100:
        out.append((s + 100, "%s adds an extra $1, but the cents make less than 100¢"))
    out.append((s + 10, None))
    return out


def sub_mistakes(a, b):
    da, ca, db, cb = a // 100, a % 100, b // 100, b % 100
    r = a - b
    out = []
    if ca == 0 and cb:
        out.append(((da - db) * 100 + cb, "%%s takes $%d from $%d and just brings down the %d¢" % (db, da, cb)))
    if ca < cb:
        out.append((r + 100, "%s renames $1 as 100¢ but does not take the $1 away from the dollars"))
    k = len(str(a))
    sb = from_digs([abs(x - y) for x, y in zip(digs(a, k), digs(b, k))])
    if sb != r:
        out.append((sb, "%s takes the smaller digit from the bigger one in each place"))
    if ca % 10 < cb % 10 and ca >= cb:
        out.append((r + 10, "%s forgets to take away the 10¢ that was renamed"))
    out.append((a + b, "%s adds instead of subtracting"))
    out.append((r - 100, None))
    out.append((r + 10, None))
    return out


def change_mistakes(paid, price):
    r = paid - price
    out = []
    if price % 100:
        out.append(((paid // 100 - price // 100) * 100 + price % 100,
                     "%%s takes $%d from $%d and just brings down the %d¢" % (price // 100, paid // 100, price % 100)))
        out.append((r + 100, "%s forgets the $1 used up to make the cents"))
    out.append((price, "%s is the price, not the change"))
    if price % 10:
        out.append((r + 10, "%%s counts on %d¢ to the next dollar wrongly (it is %d¢)" % (100 - price % 100 + 10, 100 - price % 100)))
    out.append((paid + price, "%s adds instead of subtracting"))
    out.append((r - 100, None))
    return out


# ------------------------------------------------------------ explanations
def add_expl(nums):
    cs = [n % 100 for n in nums]
    ds = [n // 100 for n in nums]
    C, D = sum(cs), sum(ds)
    T = sum(nums)
    ce = " + ".join("%d¢" % c for c in cs if c)
    de = " + ".join("$%d" % x for x in ds if x)
    parts = []
    if len([c for c in cs if c]) > 1:
        parts.append("Add the cents: %s = %d¢." % (ce, C))
    if C >= 100:
        parts.append("Rename 100¢ as $1, so %d¢ = %s." % (C, d(C)))
        dd = [x for x in ds if x] + [C // 100]
        parts.append("Add the dollars: %s = $%d." % (" + ".join("$%d" % x for x in dd), D + C // 100))
    elif len([x for x in ds if x]) > 1:
        parts.append("Add the dollars: %s = $%d." % (de, D))
    parts.append("Answer: <b>%s</b>." % f(T))
    return " ".join(parts)


def sub_expl(a, b, check=True):
    da, ca, db, cb = a // 100, a % 100, b // 100, b % 100
    r = a - b
    parts = []
    if ca >= cb:
        if cb:
            parts.append("Subtract the cents: %d¢ − %d¢ = %d¢." % (ca, cb, ca - cb))
        if db:
            parts.append("Subtract the dollars: $%d − $%d = $%d." % (da, db, da - db))
    else:
        if ca == 0:
            parts.append("Write %s as %s. There are no cents to take %d¢ from." % (f(a) if a % 100 else dl(a), d(a), cb))
        else:
            parts.append("%d¢ − %d¢: there are not enough cents." % (ca, cb))
        if da == 1 and ca:
            parts.append("Write %s as %d¢. %d¢ − %d¢ = %d¢." % (d(a), a, a, cb, a - cb))
        else:
            parts.append("Rename $1 as 100¢: %s = $%d and %d¢. %d¢ − %d¢ = %d¢." % (d(a), da - 1, ca + 100, ca + 100, cb, ca + 100 - cb))
        if db:
            parts.append("Dollars: $%d − $%d = $%d." % (da - 1, db, da - 1 - db))
    parts.append("Answer: <b>%s</b>." % f(r))
    if check:
        parts.append("Check: %s + %s = %s." % (f(r), f(b), d(a)))
    return " ".join(parts)


# ------------------------------------------------------------ helpers
def mcq(q, correct, cands, e, notes=2):
    """4 choices: correct + the first 3 usable distractors (never equal in value). cands: [(value, why)] or values.
    The reasons of the chosen distractors (up to `notes`) are added to the explanation."""
    correct = f(correct) if isinstance(correct, int) else str(correct)
    seen_t, seen_v = {correct}, {mval(correct)} - {None}
    pick, why = [], []
    for c in cands:
        w = None
        if isinstance(c, tuple):
            c, w = c
        if c is None:
            continue
        if isinstance(c, int):
            if c <= 0:
                continue
            c = f(c)
        v = mval(c)
        if c in seen_t or (v is not None and v in seen_v):
            continue
        seen_t.add(c)
        if v is not None:
            seen_v.add(v)
        pick.append(c)
        if w and len(why) < notes:
            why.append(cap(w % c if "%s" in w else w) + ".")
        if len(pick) == 3:
            break
    assert len(pick) == 3, (q, correct, cands)
    return {"q": q, "c": [correct] + pick, "a": 0, "e": (e + " " + " ".join(why)).strip()}


def balance(sets, rnd):
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


def text(x, y, t, fs=16, anchor="middle", col=INK, weight=700):
    return ("<text x='%.1f' y='%.1f' font-size='%d' font-weight='%d' fill='%s' text-anchor='%s'>%s</text>"
            % (x, y, fs, weight, col, anchor, t))


def table(head, rows):
    h = "".join("<th>%s</th>" % x for x in head)
    b = "".join("<tr>" + "".join("<td>%s</td>" % c for c in r) + "</tr>" for r in rows)
    return "<div class='sn-tw'><table class='sn-table'><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>" % (h, b)


def ex(title, q, s, a):
    return ("<div class='sn-ex'><span class='sn-ex-t'>%s</span><p class='sn-ex-q'>%s</p>"
            "<p class='sn-ex-s'>%s</p><p class='sn-ex-a'>Answer: %s</p></div>" % (title, q, s, a))


def tw(s, fs):
    """Rough text width of bold Arial."""
    w = 0
    for ch in s:
        if ch in ".,: " + NB:
            w += 0.3
        elif ch in "l1i":
            w += 0.45
        elif ch in "m×÷?$¢":
            w += 0.75
        else:
            w += 0.6
    return w * fs


# ------------------------------------------------------------ pictures: coins and notes
def tok_size(t):
    if t.startswith("N"):
        return NOTE_W, NOTE_H
    return 2 * COIN[t], 2 * COIN[t]


def draw_tok(t, cx, cy):
    if t.startswith("N"):
        fill, edge = NOTE[t]
        x, y = cx - NOTE_W / 2, cy - NOTE_H / 2
        return ("<rect x='%.1f' y='%.1f' width='%d' height='%d' rx='4' fill='%s' stroke='%s' stroke-width='2'/>"
                "<rect x='%.1f' y='%.1f' width='%d' height='%d' rx='2' fill='none' stroke='%s' stroke-width='1'/>"
                % (x, y, NOTE_W, NOTE_H, fill, edge, x + 5, y + 5, NOTE_W - 10, NOTE_H - 10, edge)
                + text(cx, cy + 7, lab(VAL[t]), 20, col=edge))
    r = COIN[t]
    fs = 15 if t != "C100" else 16
    return ("<circle cx='%.1f' cy='%.1f' r='%d' fill='%s' stroke='%s' stroke-width='2'/>" % (cx, cy, r, COINFILL, COINEDGE)
            + "<circle cx='%.1f' cy='%.1f' r='%d' fill='none' stroke='%s' stroke-width='1'/>" % (cx, cy, r - 3, COINEDGE)
            + text(cx, cy + fs * 0.36, lab(VAL[t]), fs))


def money_svg(toks, per_row=6, gap=8, pad=6, label=None, under=None):
    nrow = -(-len(toks) // per_row)
    per = -(-len(toks) // nrow)
    rows = [toks[i:i + per] for i in range(0, len(toks), per)]
    lab_h = 22 if under else 0
    widths = []
    for r in rows:
        ws = [max(tok_size(t)[0], 64 if under else 0) for t in r]
        widths.append(sum(ws) + gap * (len(r) - 1))
    heights = [max(tok_size(t)[1] for t in r) + lab_h for r in rows]
    W = max(widths) + 2 * pad
    H = sum(heights) + gap * (len(rows) - 1) + 2 * pad
    s, y, k = [], pad, 0
    for r, rh in zip(rows, heights):
        x = pad
        hh = rh - lab_h
        for t in r:
            w = max(tok_size(t)[0], 64 if under else 0)
            s.append(draw_tok(t, x + w / 2, y + hh / 2))
            if under:
                s.append(text(x + w / 2, y + hh + 18, under[k], 15, col=GREEN))
            x += w + gap
            k += 1
        y += rh + gap
    return svg_wrap(W, H, "".join(s), label or ("money: " + ", ".join(ONE[t] for t in toks)))


# ------------------------------------------------------------ pictures: columns ($, dollars, point, cents)
def column_svg(nums, op, answer=None, fs=28):
    rows = list(nums) + ([answer] if answer else [])
    I = max(len(str(n // 100)) for n in rows)
    cw = fs * 0.64
    kw = cw * 0.55
    sign_x = 10 + cw / 2
    dollar_x = sign_x + cw * 1.15
    x = dollar_x + cw * 0.6
    xs = {}
    for p in range(I - 1, -1, -1):
        xs[p] = x + cw / 2
        x += cw
    xs["pt"] = x + kw / 2
    x += kw
    xs[-1] = x + cw / 2
    xs[-2] = x + cw * 1.5
    x += 2 * cw
    W = int(x + 10)
    s = []

    def ch(c, cx, y, color):
        s.append("<text x='%.1f' y='%d' font-size='%d' font-weight='700' fill='%s' text-anchor='middle' "
                 "font-family='monospace'>%s</text>" % (cx, y, fs, color, c))

    def put(n, y, color):
        dol_s = str(n // 100)
        lead = I - len(dol_s)
        ch("$", dollar_x, y, color)
        for i, c in enumerate(reversed(dol_s)):
            ch(c, xs[i], y, color)
        ch(".", xs["pt"], y, color)
        cs = "%02d" % (n % 100)
        ch(cs[0], xs[-1], y, color)
        ch(cs[1], xs[-2], y, color)

    ys = [8 + fs + int(i * fs * 1.15) for i in range(len(nums))]
    for n, y in zip(nums, ys):
        put(n, y, INK)
    s.append("<text x='%.1f' y='%d' font-size='%d' font-weight='700' fill='%s' text-anchor='middle'>%s</text>"
             % (sign_x, ys[-1], fs, GREEN, "+" if op == "+" else "−"))
    ly = ys[-1] + 13
    s.append("<line x1='%.1f' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='3'/>" % (sign_x - cw * 0.4, ly, W - 8, ly, INK))
    H = ly + 10
    if answer:
        put(answer, ly + fs + 6, GREEN)
        H = ly + fs + 14
    label = "%s written in columns" % (" plus " if op == "+" else " minus ").join(d(n) for n in nums)
    return svg_wrap(W, H, "".join(s), label)


# ------------------------------------------------------------ pictures: counting on for change
def change_pts(price, paid):
    """price -> next 10¢ -> next dollar -> next $10 (for $50) -> money paid"""
    pts, s = [price], price
    if s % 10:
        s += 10 - s % 10
        pts.append(s)
    if s % 100 and s < paid:
        s += 100 - s % 100
        pts.append(s)
    if paid >= 5000 and s % 1000 and s + 1000 - s % 1000 < paid:
        s += 1000 - s % 1000
        pts.append(s)
    if s < paid:
        pts.append(paid)
    assert pts[-1] == paid and all(a < b for a, b in zip(pts, pts[1:]))
    return pts


def count_on(price, paid):
    pts = change_pts(price, paid)
    steps = ["%s + %s = %s" % (short(a), short(b - a), short(b)) for a, b in zip(pts, pts[1:])]
    jumps = [b - a for a, b in zip(pts, pts[1:])]
    assert sum(jumps) == paid - price
    tail = "" if len(jumps) == 1 else " Add the jumps: %s = %s." % (" + ".join(short(j) for j in jumps), f(paid - price))
    return "Count on from %s to %s: %s.%s" % (d(price), dl(paid), ", ".join(steps), tail)


def change_line(price, paid, show=True):
    pts = change_pts(price, paid)
    seg = [110, 120, 130, 140][:len(pts) - 1]
    x0, y0 = 36, 70
    xs = [x0]
    for dd in seg:
        xs.append(xs[-1] + dd)
    W = xs[-1] + 40
    H = 104
    b = ["<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='2'/>" % (x0 - 20, y0, xs[-1] + 20, y0, INK)]
    for x, p in zip(xs, pts):
        b.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='2'/>" % (x, y0 - 7, x, y0 + 7, INK))
        b.append(text(x, y0 + 27, short(p), 16))
    for i in range(len(pts) - 1):
        a, c = xs[i], xs[i + 1]
        m = (a + c) / 2
        b.append("<path d='M%d %d Q%.1f %d %d %d' fill='none' stroke='%s' stroke-width='2'/>" % (a, y0 - 8, m, y0 - 50, c, y0 - 8, GREEN))
        b.append(text(m, y0 - 34, ("+" + short(pts[i + 1] - pts[i])) if show else "+ ?", 16, col=GREEN))
    return svg_wrap(W, H, "".join(b), "counting on from %s to %s" % (d(price), dl(paid)))


# ------------------------------------------------------------ pictures: price tags
def tags_svg(items, kind):
    gap, pad, h = 8, 6, 62
    ws = [int(max(tw(n, 15) + 18, 78)) for n, p in items]
    W = sum(ws) + gap * (len(ws) - 1) + 2 * pad
    H = h + 2 * pad
    b, x = [], pad
    for (n, p), w in zip(items, ws):
        b.append("<rect x='%d' y='%d' width='%d' height='%d' rx='6' fill='#ffffff' stroke='%s' stroke-width='2'/>" % (x, pad, w, h, INK))
        b.append(text(x + w / 2, pad + 24, n, 15))
        b.append(text(x + w / 2, pad + 50, f(p), 18, col=GREEN))
        x += w + gap
    return svg_wrap(W, H, "".join(b), kind + ": " + ", ".join("%s %s" % (n, f(p)) for n, p in items))


# ------------------------------------------------------------ pictures: bar models
def brace(x1, x2, y, up, lab_, col=INK):
    dd = 7 if up else -7
    o = ["<path d='M%.1f %.1f L%.1f %.1f L%.1f %.1f L%.1f %.1f' fill='none' stroke='%s' stroke-width='2'/>"
         % (x1, y + dd, x1, y, x2, y, x2, y + dd, col)]
    o.append(text((x1 + x2) / 2.0, y - 7 if up else y + 20, lab_, 16, col=col))
    return "".join(o)


def bar_parts(parts, total_lab, BW=500):
    """One bar split into parts drawn to scale. parts = [(cents, label)]. Bracket below with total_lab."""
    X0, TOP, BH = 10, 8, 40
    tot = sum(v for v, _ in parts)
    W = X0 * 2 + BW
    H = TOP + BH + 36
    o, x = [], float(X0)
    fills = [HEADFILL, PARTFILL, "#fff"]
    for i, (v, lb) in enumerate(parts):
        w = float(v) / tot * BW
        assert tw(lb, 16) <= w - 6, (lb, w)
        o.append("<rect x='%.1f' y='%d' width='%.1f' height='%d' fill='%s' stroke='%s' stroke-width='2'/>"
                 % (x, TOP, w, BH, fills[i % 3], GREEN))
        o.append(text(x + w / 2.0, TOP + BH / 2.0 + 6, lb, 16, col=RED if lb == "?" else INK))
        x += w
    o.append(brace(X0, X0 + BW, TOP + BH + 10, False, total_lab, col=RED if total_lab == "?" else INK))
    return svg_wrap(W, H, "".join(o), "bar model: parts %s, whole %s" % (", ".join(l for _, l in parts), total_lab))


def bar_compare(rows, diff_lab, BW=420):
    """Comparison model. rows = [(name, cents, label)], the first bar is the longer one."""
    (n1, v1, l1), (n2, v2, l2) = rows
    assert v1 > v2
    LW = int(max(tw(n1, 16), tw(n2, 16))) + 16
    X0, TOP, BH, GAP = 6, 8, 38, 16
    x0 = X0 + LW
    W = x0 + BW + 10
    H = TOP + 2 * BH + GAP + 8
    w2 = float(v2) / v1 * BW
    o = []
    for i, (nm, w, lb, fill) in enumerate([(n1, BW, l1, HEADFILL), (n2, w2, l2, PARTFILL)]):
        y = TOP + i * (BH + GAP)
        assert tw(lb, 16) <= w - 6, (lb, w)
        o.append(text(x0 - 10, y + BH / 2.0 + 6, nm, 16, anchor="end"))
        o.append("<rect x='%d' y='%d' width='%.1f' height='%d' fill='%s' stroke='%s' stroke-width='2'/>"
                 % (x0, y, w, BH, fill, GREEN))
        o.append(text(x0 + w / 2.0, y + BH / 2.0 + 6, lb, 16, col=RED if lb == "?" else INK))
    y = TOP + BH + GAP
    dw = BW - w2
    assert tw(diff_lab, 16) <= dw - 6, (diff_lab, dw)
    o.append("<rect x='%.1f' y='%d' width='%.1f' height='%d' fill='none' stroke='%s' stroke-width='2' "
             "stroke-dasharray='6 4'/>" % (x0 + w2, y, dw, BH, ORANGE))
    o.append(text(x0 + w2 + dw / 2.0, y + BH / 2.0 + 6, diff_lab, 16, col=RED if diff_lab == "?" else ORANGE))
    lb = "bar model comparing %s (%s) and %s (%s), difference %s" % (n1, l1, n2, l2, diff_lab)
    return svg_wrap(int(W), H, "".join(o), lb)


# ============================================================ random amounts
def amount(rnd, lo, hi):
    """dollars lo..hi, cents a multiple of 5 (not 0)"""
    return rnd.randint(lo, hi) * 100 + 5 * rnd.randint(1, 19)


def add_kind(a, b):
    ca, cb = a % 100, b % 100
    if ca + cb >= 100:
        return "dollar"
    return "unit" if ca % 10 + cb % 10 >= 10 else "none"


def sub_kind(a, b):
    ca, cb = a % 100, b % 100
    if ca < cb:
        return "dollar"
    return "unit" if ca % 10 < cb % 10 else "none"


def pick_add(rnd, seen, kind, lo, hi):
    for _ in range(5000):
        a, b = amount(rnd, lo, hi), amount(rnd, lo, hi)
        key = ("+",) + tuple(sorted([a, b]))
        if key in seen or a == b or add_kind(a, b) != kind or (a + b) % 100 == 0:
            continue
        seen.add(key)
        return a, b
    raise RuntimeError(kind)


def pick_sub(rnd, seen, kind, lo, hi, whole=False):
    for _ in range(5000):
        a, b = amount(rnd, lo, hi), amount(rnd, 1, hi - 1)
        if whole:
            a = a // 100 * 100
        key = ("-", a, b)
        if key in seen or a - b < 50 or sub_kind(a, b) != kind or a == 2 * b or (a - b) % 100 == 0:
            continue
        seen.add(key)
        return a, b
    raise RuntimeError(kind)


def item_add(nums, col):
    T = sum(nums)
    if col:
        q = fig(column_svg(nums, "+")) + "Add."
    else:
        q = "What is %s?" % " + ".join(d(n) for n in nums)
    cands = add_mistakes(*nums) if len(nums) == 2 else []
    return mcq(q, T, cands, add_expl(nums))


def item_sub(a, b, col):
    if col:
        q = fig(column_svg([a, b], "-")) + "Subtract."
    else:
        q = "What is %s − %s?" % (dl(a) if a % 100 == 0 else d(a), d(b))
    return mcq(q, a - b, sub_mistakes(a, b), sub_expl(a, b))


# ============================================================ set 1: add money
def set_add(P, rnd, seen):
    its = []
    its.append(mcq("$3.45 is 3 dollars and how many cents?", "45¢", ["34¢", "54¢", "5¢"],
                   "The 2 digits after the decimal point are the cents. $3.45 = 3 dollars and <b>45 cents</b>."))
    its.append(mcq("How do you write 6 dollars and 5 cents in decimal notation?", 605, [650, 6500, 65],
                   "Cents always take 2 places after the point. 5 cents is written 05, so the answer is <b>$6.05</b>. "
                   "$6.50 is 6 dollars and 50 cents."))
    its.append(mcq("Write 280¢ in dollars and cents.", 280, [2800, 28, 208],
                   "100¢ = $1, so 200¢ = $2. 280¢ = $2 and 80¢ = <b>$2.80</b>. $28.00 is ten times too much."))
    its.append(mcq("How many 20¢ coins make $1?", "5 coins", ["10 coins", "20 coins", "4 coins"],
                   "$1 = 100¢. Count in 20s: 20¢, 40¢, 60¢, 80¢, 100¢. That is <b>5 coins</b>. "
                   "10 coins of 10¢ make $1, not 10 coins of 20¢."))
    t1 = ["N5", "N2", "C50", "C20", "C20", "C5"]
    assert total(t1) == 795
    its.append(mcq(fig(money_svg(t1)) + "How much money is there?", 795,
                   [(790, "%s leaves out the 5¢ coin"), (775, "%s counts only one 20¢ coin"), (700, "%s counts only the notes")],
                   "Notes: $5 + $2 = $7. Coins: 50¢, 70¢, 90¢, 95¢. $7 and 95¢ is <b>$7.95</b>."))
    t2 = ["N10", "C100", "C100", "C50", "C50", "C20", "C10"]
    assert total(t2) == 1330
    its.append(mcq(fig(money_svg(t2, per_row=7)) + "How much money is there?", 1330,
                   [(1230, "%s forgets to rename 100¢ as $1"), (1320, "%s leaves out the 10¢ coin"),
                    (1132, "%s counts the $1 coins as 1¢ each")],
                   "Dollars: $10, $11, $12. Cents: 50¢, 100¢, 120¢, 130¢. 130¢ = $1.30. $12 + $1.30 = <b>$13.30</b>."))
    # the key example of the unit
    a, b = 345, 280
    assert a + b == 625
    seen.add(("+", 280, 345))
    n, he, his = P.next()
    its.append(mcq("%s says $3.45 + $2.80 = $5.125. What is the correct answer?" % n, 625,
                   [("$5.125", None), (525, "%s forgets the $1 from renaming 100¢"), (535, "%s subtracts the cents: 80¢ − 45¢ = 35¢")],
                   "Add the cents: 45¢ + 80¢ = 125¢. Rename 100¢ as $1, so 125¢ = $1.25. "
                   "Add the dollars: $3 + $2 + $1 = $6. Answer: <b>$6.25</b>. "
                   "$5.125 writes 125¢ after the point, but money has only 2 places for cents."))
    plan = [("none", 1, 5), ("none", 2, 7), ("unit", 1, 6), ("dollar", 1, 5), ("dollar", 2, 8),
            ("unit", 2, 9), ("dollar", 3, 9), ("dollar", 4, 15), ("dollar", 10, 30), ("none", 10, 40)]
    for i, (k, lo, hi) in enumerate(plan):
        a, b = pick_add(rnd, seen, k, lo, hi)
        its.append(item_add([a, b], i % 2 == 0))
    # whole dollars + dollars and cents
    assert 400 + 235 == 635
    its.append(mcq("What is $4 + $2.35?", 635, [(239, "%s adds $4 as if it were 4¢"), (275, "%s adds 40¢ instead of $4"),
                                               (435, "%s leaves out the $2")],
                   "$4 has no cents. Add the dollars: $4 + $2 = $6. The cents stay 35¢. Answer: <b>$6.35</b>."))
    # dollars and cents + cents
    assert 265 + 85 == 350
    its.append(mcq("What is $2.65 + 85¢?", 350, [("$2.150", "%s writes 150¢ after the point instead of renaming 100¢ as $1"),
                                                (250, "%s forgets the $1 from renaming 100¢"), (8765, "%s reads 85¢ as $85")],
                   "Add the cents: 65¢ + 85¢ = 150¢. Rename 100¢ as $1, so 150¢ = $1.50. "
                   "Add the dollars: $2 + $1 = $3. Answer: <b>$3.50</b>."))
    # three amounts
    nums = [120, 235, 50]
    assert sum(nums) == 405
    its.append(mcq("What is $1.20 + $2.35 + 50¢?", 405, [(355, "%s leaves out the 50¢"), (395, "%s adds 40¢ instead of 50¢"),
                                                       (305, "%s forgets the $1 from renaming 100¢")],
                   add_expl(nums)))
    assert len(its) == 20, len(its)
    return {"title": "Add money in decimal notation", "items": its}


# ============================================================ set 2: subtract money
def set_sub(P, rnd, seen):
    its = []
    its.append(mcq("To find $5.20 − $2.75, you rename $1 as 100¢. What is $5.20 after renaming?", "$4 and 120¢",
                   ["$5 and 120¢", "$4 and 30¢", "$4 and 20¢"],
                   "Take $1 from the $5 and change it into 100¢. 100¢ + 20¢ = 120¢. So $5.20 = <b>$4 and 120¢</b>. "
                   "$5 and 120¢ forgets to take the $1 away. $4 and 30¢ renames $1 as 10¢, but $1 = 100¢."))
    n, he, his = P.next()
    assert 520 - 275 == 245
    its.append(mcq("%s says $5.20 − $2.75 = $3.55. What is the correct answer?" % n, 245,
                   [(355, "%s takes the smaller digit from the bigger one in each place"),
                    (345, "%s renames $1 as 100¢ but does not take the $1 away"), (795, "%s adds instead of subtracting")],
                   "20¢ − 75¢: there are not enough cents. Rename $1 as 100¢: $5.20 = $4 and 120¢. "
                   "120¢ − 75¢ = 45¢. Dollars: $4 − $2 = $2. Answer: <b>$2.45</b>. Check: $2.45 + $2.75 = $5.20.", notes=1))
    n, he, his = P.next()
    assert 840 - 365 == 475
    its.append(mcq("%s found $8.40 − $3.65 = $4.75. Which addition checks %s answer?" % (n, his),
                   "$4.75 + $3.65 = $8.40", ["$8.40 + $3.65 = $12.05", "$4.75 + $8.40 = $13.15", "$4.75 − $3.65 = $1.10"],
                   "Addition undoes subtraction. Add the answer to the amount taken away: $4.75 + $3.65 = $8.40. "
                   "You get back the starting amount, so %s answer is right." % his))
    seen.update({("-", 520, 275), ("-", 840, 365)})
    plan = [("none", 2, 6, False), ("none", 3, 9, False), ("unit", 3, 8, False), ("none", 4, 9, False),
            ("dollar", 3, 7, False), ("unit", 4, 9, False), ("dollar", 4, 9, False), ("dollar", 5, 9, False),
            ("none", 10, 30, False), ("dollar", 6, 9, False), ("dollar", 10, 20, False), ("unit", 10, 40, False),
            ("dollar", 20, 60, False), ("dollar", 5, 9, True), ("dollar", 10, 20, True), ("dollar", 20, 40, True)]
    for i, (k, lo, hi, whole) in enumerate(plan):
        a, b = pick_sub(rnd, seen, k, lo, hi, whole)
        its.append(item_sub(a, b, i % 2 == 0))
    assert 410 - 65 == 345
    its.append(mcq("What is $4.10 − 65¢?", 345, [(445, "%s renames $1 as 100¢ but does not take the $1 away"),
                                                 (355, "%s takes the smaller digit from the bigger one"),
                                                 (475, "%s adds instead of subtracting")],
                   "10¢ − 65¢: there are not enough cents. Rename $1 as 100¢: $4.10 = $3 and 110¢. "
                   "110¢ − 65¢ = 45¢. The dollars stay $3. Answer: <b>$3.45</b>. Check: $3.45 + 65¢ = $4.10.", notes=1))
    assert len(its) == 20, len(its)
    return {"title": "Subtract money with renaming", "items": its}


# ============================================================ set 3: change from $10 or $50
def note_word(paid):
    return {1000: "a $10 note", 5000: "a $50 note"}[paid]


def set_change(P, rnd):
    its = []
    jobs = [(1000, 435, "a pencil case", True), (1000, 790, "a storybook", False), (1000, 380, "a plate of chicken rice", False),
            (1000, 185, "a bottle of glue", False), (1000, 265, "a file", True), (1000, 420, "a kaya toast set", False),
            (1000, 340, "a cup of bubble tea", False), (1000, 725, "a box of colour pencils", True), (1000, 655, "a lunch box", False),
            (5000, 3290, "a pair of school shoes", True), (5000, 2745, "a school bag", False), (5000, 1285, "a water bottle", False),
            (5000, 1850, "a box of mandarin oranges", False), (5000, 2495, "a football", True), (5000, 1630, "a jigsaw puzzle", False),
            (5000, 2175, "a dictionary", False), (5000, 3960, "a badminton racket", False)]
    for paid, pr, thing, line in jobs:
        nm, he, his = P.next()
        r = paid - pr
        q = "%s buys %s for %s. %s pays with %s. How much change does %s get?" % (nm, thing, d(pr), cap(he), note_word(paid), he)
        if line:
            q = fig(change_line(pr, paid, show=False)) + q + " Count on along the number line."
        e = "%s The change is <b>%s</b>. Check: %s + %s = %s." % (count_on(pr, paid), f(r), d(pr), f(r), dl(paid))
        its.append(mcq(q, r, change_mistakes(paid, pr), e))
    # which money is the change
    assert 200 + 100 + 20 == 320
    nm, he, his = P.next()
    its.append(mcq("%s’s change is $3.20. Which of these makes $3.20?" % nm,
                   "a $2 note, a $1 coin and a 20¢ coin",
                   ["a $2 note and a 20¢ coin", "a $2 note, a $1 coin and two 20¢ coins", "three $1 coins and a 10¢ coin"],
                   "$2 + $1 = $3. $3 + 20¢ = <b>$3.20</b>. A $2 note and a 20¢ coin is only $2.20. "
                   "Two 20¢ coins make 40¢, so that one is $3.40."))
    # check the change in a picture
    tk = ["N5", "N2", "C100", "C10", "C5"]
    assert total(tk) == 815 and 1000 - 85 == 915
    nm, he, his = P.next()
    its.append(mcq(fig(money_svg(tk)) + "%s buys a ruler for 85¢ and pays with a $10 note. %s gets this change. Is it correct?"
                   % (nm, cap(he)),
                   "No. It is $1 too little.", ["Yes. It is correct.", "No. It is $1 too much.", "No. It is 10¢ too little."],
                   "The change should be $10.00 − 85¢ = $9.15 (85¢ + 15¢ = $1, $1 + $9 = $10). "
                   "The picture shows $5 + $2 + $1 + 10¢ + 5¢ = $8.15. $8.15 is <b>$1 too little</b>."))
    # find the price from the change
    assert 1000 - 355 == 645
    nm, he, his = P.next()
    its.append(mcq("%s pays for a book with a $10 note. %s gets $3.55 change. What is the price of the book?" % (nm, cap(he)),
                   645, [(355, "%s is the change, not the price"), (755, "%s takes $3 from $10 and just brings down the 55¢"),
                         (1355, "%s adds instead of subtracting")],
                   "Price + change = $10, so price = $10.00 − $3.55. Count on from $3.55: $3.55 + 45¢ = $4, $4 + $6 = $10. "
                   "45¢ + $6 = <b>$6.45</b>. Check: $6.45 + $3.55 = $10.", notes=1))
    assert len(its) == 20, len(its)
    return {"title": "Change from $10 or $50", "items": its}


# ============================================================ set 4: compare prices and budgets
CANTEEN = [("chicken rice", 250), ("mee goreng", 220), ("fishball noodles", 195), ("nasi lemak", 245), ("soya bean drink", 80)]
BOOKSHOP = [("storybook", 835), ("colour pencils", 465), ("file", 235), ("notebook", 175), ("ruler", 85), ("eraser", 60)]


def set_compare(P, rnd):
    its = []
    cv = dict(CANTEEN)
    bv = dict(BOOKSHOP)
    canteen = tags_svg(CANTEEN, "price list at the school canteen")
    shop = tags_svg(BOOKSHOP, "price list at the bookshop")
    its.append(mcq("Which price is the greatest?", "$4.50", ["$4.05", "$4.45", "$4.15"],
                   "All 4 prices have $4. Compare the cents: 50¢ is more than 45¢, 15¢ and 5¢. So <b>$4.50</b> is the greatest. "
                   "$4.05 has only 5¢: the 0 means no tens of cents."))
    its.append(mcq("Which is more: $3.05 or 350¢?", "350¢ is more.", ["$3.05 is more.", "They are equal.", "You cannot compare them."],
                   "Write 350¢ in dollars: 350¢ = $3.50. $3.50 is more than $3.05, so <b>350¢ is more</b>."))
    its.append(mcq("Put the prices in order, from the cheapest to the most expensive: $5.60, $5.06, $6.05, $5.65",
                   "$5.06, $5.60, $5.65, $6.05", ["$5.60, $5.06, $5.65, $6.05", "$6.05, $5.65, $5.60, $5.06", "$5.06, $5.65, $5.60, $6.05"],
                   "Compare the dollars first: $6.05 is the most. The others have $5, so compare the cents: 6¢ &lt; 60¢ &lt; 65¢. "
                   "Order: <b>$5.06, $5.60, $5.65, $6.05</b>. $5.06 has 6¢, not 60¢."))
    its.append(mcq(fig(canteen) + "Which food at the canteen is the cheapest?", "fishball noodles",
                   ["mee goreng", "nasi lemak", "chicken rice"],
                   "Fishball noodles cost $1.95, which is less than $2. The other food costs more than $2. "
                   "So <b>fishball noodles</b> are the cheapest."))
    its.append(mcq(fig(canteen) + "Which food costs more than $2 but less than $2.40?", "mee goreng",
                   ["nasi lemak", "fishball noodles", "chicken rice"],
                   "Mee goreng costs $2.20: more than $2 and less than $2.40. Nasi lemak costs $2.45, which is more than $2.40. "
                   "Fishball noodles cost $1.95, less than $2."))
    a, b = cv["chicken rice"], cv["fishball noodles"]
    its.append(mcq(fig(canteen) + "How much more does chicken rice cost than fishball noodles?", a - b,
                   sub_mistakes(a, b), sub_expl(a, b)))
    nm, he, his = P.next()
    spent = cv["chicken rice"] + cv["soya bean drink"]
    assert spent == 330 and 500 - spent == 170
    its.append(mcq(fig(canteen) + "%s has $5. %s buys chicken rice and a soya bean drink. How much money does %s have left?"
                   % (nm, cap(he), he), 170,
                   [(230, "%s takes $3 from $5 and just brings down the 30¢"), (270, "%s forgets the $1 used up to make the cents"),
                    (330, "%s is the money spent, not the money left")],
                   "Money spent: $2.50 + 80¢ = $3.30. Money left: $5.00 − $3.30. Count on: $3.30 + 70¢ = $4, $4 + $1 = $5. "
                   "Answer: <b>$1.70</b>."))
    nm, he, his = P.next()
    s5 = bv["colour pencils"] + bv["eraser"]
    assert s5 == 525
    its.append(mcq(fig(shop) + "%s has $5. Can %s buy colour pencils and an eraser?" % (nm, he),
                   "No. %s needs 25¢ more." % cap(he),
                   ["Yes. %s has 35¢ left." % cap(he), "Yes. %s has 25¢ left." % cap(he), "No. %s needs 60¢ more." % cap(he)],
                   "Total: $4.65 + 60¢ = $5.25. $5.25 is more than $5. $5.25 − $5.00 = 25¢, so <b>%s needs 25¢ more</b>. "
                   "“35¢ left” forgets the eraser: $5.00 − $4.65 = 35¢." % he))
    nm, he, his = P.next()
    s6 = bv["storybook"] + bv["ruler"]
    assert s6 == 920 and 1000 - s6 == 80
    its.append(mcq(fig(shop) + "%s has $10. Can %s buy the storybook and a ruler?" % (nm, he),
                   "Yes. %s has 80¢ left." % cap(he),
                   ["No. %s needs 80¢ more." % cap(he), "Yes. %s has $1.65 left." % cap(he), "Yes. %s has 90¢ left." % cap(he)],
                   "Total: $8.35 + 85¢ = 120¢ + $8 = $9.20. $9.20 is less than $10. $10.00 − $9.20 = 80¢, so <b>yes, with 80¢ left</b>. "
                   "$1.65 left forgets the ruler."))
    nm, he, his = P.next()
    its.append(mcq(fig(shop) + "%s has $5. Which pair of items can %s NOT buy with $5?" % (nm, he),
                   "colour pencils and ruler",
                   ["file and notebook", "notebook and eraser", "file and ruler"],
                   "Colour pencils and ruler: $4.65 + 85¢ = <b>$5.50</b>, more than $5. "
                   "File and notebook: $4.10. Notebook and eraser: $2.35. File and ruler: $3.20. These are all less than $5."))
    nm, he, his = P.next()
    its.append(mcq(fig(shop) + "%s has $4.30. What is the most expensive item %s can buy?" % (nm, he),
                   "file", ["colour pencils", "notebook", "storybook"],
                   "Colour pencils cost $4.65, which is more than $4.30. The storybook costs even more. "
                   "The file ($2.35) costs more than the notebook ($1.75), so the answer is the <b>file</b>."))
    nm, he, his = P.next()
    a, b = 835, 680
    assert a - b == 155
    its.append(mcq(fig(bar_compare([("storybook", a, "$8.35"), (nm, b, "$6.80")], "?")) +
                   "The storybook costs $8.35. %s has $6.80. How much more money does %s need?" % (nm, he),
                   a - b, sub_mistakes(a, b), sub_expl(a, b)))
    nm, he, his = P.next()
    a, b = 905, 740
    assert a - b == 165
    its.append(mcq("A football costs $9.05. %s has $7.40. How much more money does %s need to buy it?" % (nm, he),
                   a - b, sub_mistakes(a, b), sub_expl(a, b)))
    nm, he, his = P.next()
    its.append(mcq("%s can spend $20 on Children’s Day gifts for %s friends. %s has spent $13.65. How much more can %s spend?"
                   % (nm, his, cap(he), he), 635, change_mistakes(2000, 1365),
                   count_on(1365, 2000) + " %s can spend <b>$6.35</b> more." % cap(he)))
    nm, he, his = P.next()
    a, b = 310, 285
    its.append(mcq("A file costs $2.85 at Shop A and $3.10 at Shop B. How much does %s save by buying it at Shop A?" % nm,
                   a - b, sub_mistakes(a, b), sub_expl(a, b)))
    a, b = 120, 95
    its.append(mcq("A bottle of water costs $1.20 at the canteen and 95¢ at a supermarket. How much cheaper is it at the supermarket?",
                   a - b, sub_mistakes(a, b), sub_expl(a, b)))
    nm, he, his = P.next()
    its.append(mcq("%s gets $3 a day for recess. Today %s spends $2.35. How much does %s save today?" % (nm, he, he),
                   65, change_mistakes(300, 235),
                   count_on(235, 300) + " %s saves <b>65¢</b>." % cap(he)))
    nm, he, his = P.next()
    tot = 3490 + 1255
    assert tot == 4745 and 5000 - tot == 255
    its.append(mcq("%s has $50. A school bag costs $34.90 and a pencil case costs $12.55. Can %s buy both?" % (nm, he),
                   "Yes. %s has $2.55 left." % cap(he),
                   ["No. %s needs $2.55 more." % cap(he), "Yes. %s has $15.10 left." % cap(he), "Yes. %s has $3.55 left." % cap(he)],
                   "Total: $34.90 + $12.55. Cents: 90¢ + 55¢ = 145¢ = $1.45. Dollars: $34 + $12 + $1 = $47. Total $47.45, less than $50. "
                   "$50.00 − $47.45 = <b>$2.55</b> left. $15.10 left forgets the pencil case. "
                   "$3.55 left forgets the $1 from renaming 145¢."))
    a, b = 835, 790
    assert a - b == 45
    its.append(mcq("A storybook costs $8.35 at one shop and $7.90 at another shop. Which price is cheaper, and by how much?",
                   "$7.90, by 45¢", ["$8.35, by 45¢", "$7.90, by $1.45", "$7.90, by $1.65"],
                   "$7 is less than $8, so <b>$7.90</b> is cheaper. Count on from $7.90: $7.90 + 10¢ = $8, $8 + 35¢ = $8.35. "
                   "10¢ + 35¢ = <b>45¢</b>. $1.45 forgets to take away the $1 used for renaming. "
                   "$1.65 takes the smaller digit from the bigger one."))
    tk = ["C100", "C100", "C20", "C20", "C20"]
    assert total(tk) == 260 and 260 - cv["chicken rice"] == 10
    nm, he, his = P.next()
    its.append(mcq(fig(money_svg(tk)) + "%s has these coins. Chicken rice costs $2.50. Does %s have enough money?" % (nm, he),
                   "Yes. 10¢ is left.", ["No. %s needs 20¢ more." % cap(he), "No. %s needs 50¢ more." % cap(he), "Yes. 60¢ is left."],
                   "$1 + $1 = $2. Three 20¢ coins: 20¢, 40¢, 60¢. %s has $2.60. $2.60 − $2.50 = <b>10¢ left</b>. "
                   "“20¢ more” counts each 20¢ coin as 10¢. “50¢ more” counts only the $1 coins." % cap(he)))
    assert len(its) == 20, len(its)
    return {"title": "Compare prices and budgets", "items": its}


# ============================================================ set 5: word problems with bar models
def set_words(P, rnd):
    its = []

    def add(q, right, cands, e, model=None, notes=2):
        its.append(mcq((fig(model) if model else "") + q, right, cands, e, notes))

    # 1 canteen, total
    n, he, his = P.next()
    a, b = 250, 90
    add("At recess, %s buys a bowl of noodles for $2.50 and a drink for 90¢. How much does %s spend?" % (n, he),
        a + b, add_mistakes(a, b), "Spend in all means add. " + add_expl([a, b]),
        model=bar_parts([(a, "$2.50"), (b, "90¢")], "?"))
    # 2 canteen, money left
    n, he, his = P.next()
    add("%s brings $5 to school. %s spends $2.85 at the canteen. How much money does %s have left?" % (n, cap(he), he),
        215, change_mistakes(500, 285), count_on(285, 500) + " %s has <b>$2.15</b> left. Check: $2.85 + $2.15 = $5." % cap(he))
    # 3 bookshop, total
    n, he, his = P.next()
    a, b = 895, 160
    add("At the bookshop, %s buys a storybook for $8.95 and a pen for $1.60. How much does %s pay altogether?" % (n, he),
        a + b, add_mistakes(a, b), "Altogether means add. " + add_expl([a, b]))
    # 4 bookshop, two steps, change from $50
    n, he, his = P.next()
    sp = 2460 + 975
    assert sp == 3435 and 5000 - sp == 1565
    add("%s buys a dictionary for $24.60 and a storybook for $9.75. %s pays with a $50 note. How much change does %s get?"
        % (n, cap(he), he), 1565,
        [(3435, "%s is the money spent, not the change"), (1665, "%s forgets the $1 from renaming 135¢ when adding"),
         (1635, "%s takes $34 from $50 and just brings down the 35¢")],
        "Step 1, total cost: $24.60 + $9.75 = $34.35. Step 2, change: $50.00 − $34.35. "
        + count_on(3435, 5000) + " Change: <b>$15.65</b>.",
        model=bar_parts([(2460, "$24.60"), (975, "$9.75"), (1565, "?")], "$50"))
    # 5 hawker centre, total
    n, he, his = P.next()
    a, b = 450, 580
    add("At the hawker centre, %s’s family buys a plate of chicken rice for $4.50 and a bowl of laksa for $5.80. "
        "How much do they pay?" % n, a + b, add_mistakes(a, b), add_expl([a, b]))
    # 6 hawker, two plates
    a = 450
    add("Mr Tan buys 2 plates of char kway teow at the hawker centre. Each plate costs $4.50. How much does he pay?",
        900, [("$8.100", "%s writes 100¢ after the point instead of renaming it as $1"),
              (800, "%s forgets the $1 from renaming 100¢"), (450, "%s is the price of 1 plate only")],
        "$4.50 + $4.50. Cents: 50¢ + 50¢ = 100¢ = $1. Dollars: $4 + $4 + $1 = $9. Answer: <b>$9.00</b>.",
        model=bar_parts([(450, "$4.50"), (450, "$4.50")], "?"))
    # 7 comparison: more than
    n1, _, _ = P.next()
    n2, h2, _ = P.next()
    a, b = 1240, 385
    assert a + b == 1625
    add("%s has $12.40. %s has $3.85 more than %s. How much money does %s have?" % (n1, n2, n1, n2),
        a + b, add_mistakes(a, b), "%s’s bar is %s’s bar and $3.85 more, so add. " % (n2, n1) + add_expl([a, b]),
        model=bar_compare([(n2, a + b, "?"), (n1, a, "$12.40")], "$3.85"))
    # 8 comparison: less than
    a, b = 1425, 680
    assert a - b == 745
    add("A book costs $14.25. A comic costs $6.80 less than the book. How much does the comic cost?",
        a - b, sub_mistakes(a, b), "Less than means subtract. " + sub_expl(a, b),
        model=bar_compare([("book", a, "$14.25"), ("comic", a - b, "?")], "$6.80"))
    # 9 two steps: less than, then altogether
    n1, _, _ = P.next()
    n2, _, _ = P.next()
    p2 = 1850 - 475
    assert p2 == 1375 and 1850 + p2 == 3225
    add("%s saves $18.50. %s saves $4.75 less than %s. How much do they save altogether?" % (n1, n2, n1),
        3225, [(1375, "%%s is only what %s saves" % n2), (2325, "%s adds $4.75 instead of taking it away"),
               (3125, "%s forgets the $1 from renaming 125¢")],
        "Step 1, %s: $18.50 − $4.75 = $13.75. Step 2, altogether: $18.50 + $13.75. Cents: 50¢ + 75¢ = 125¢ = $1.25. "
        "Dollars: $18 + $13 + $1 = $32. Answer: <b>$32.25</b>." % n2,
        model=bar_compare([(n1, 1850, "$18.50"), (n2, p2, "?")], "$4.75"))
    # 10 how much more is needed
    n, he, his = P.next()
    add("%s wants a bicycle helmet that costs $40. %s has $23.60. How much more money does %s need?" % (n, cap(he), he),
        1640, change_mistakes(4000, 2360), count_on(2360, 4000) + " %s needs <b>$16.40</b> more." % cap(he),
        model=bar_compare([("helmet", 4000, "$40"), (n, 2360, "$23.60")], "?"))
    # 11 Children's Day party
    a, b = 3650, 2875
    add("For Children’s Day, Mrs Lim’s class has $36.50 for a party. They spend $28.75 on food. How much money is left?",
        a - b, sub_mistakes(a, b), sub_expl(a, b))
    # 12 National Day, two steps
    sp = 1290 + 845
    assert sp == 2135 and 5000 - sp == 2865
    add("For National Day, Mdm Wong buys flags for $12.90 and balloons for $8.45. She pays with a $50 note. "
        "How much change does she get?", 2865,
        [(2135, "%s is the money spent, not the change"), (2935, "%s takes $21 from $50 and just brings down the 35¢"),
         (2965, "%s forgets the $1 used up to make the cents")],
        "Step 1, money spent: $12.90 + $8.45 = $21.35. Step 2, change: $50.00 − $21.35. " + count_on(sp, 5000)
        + " Change: <b>$28.65</b>.",
        model=bar_parts([(1290, "$12.90"), (845, "$8.45"), (2865, "?")], "$50"))
    # 13 zoo snacks
    n, he, his = P.next()
    a, b = 1570, 685
    add("At the Singapore Zoo, %s’s family spends $15.70 on snacks and $6.85 on drinks. How much do they spend in all?" % n,
        a + b, add_mistakes(a, b), add_expl([a, b]))
    # 14 unknown whole
    n, he, his = P.next()
    a, b = 360, 515
    assert a + b == 875
    add("%s buys a cup of bubble tea for $3.60. Then %s has $5.15 left. How much money did %s have at first?" % (n, he, he),
        a + b, [(155, "%s subtracts, but the money at first is the whole"), (515, "%s is the money left, not the money at first"),
                (975, "%s adds an extra $1")],
        "The money at first is the whole: money spent + money left. " + add_expl([a, b]),
        model=bar_parts([(a, "$3.60"), (b, "$5.15")], "?"))
    # 15 red packets, two steps
    n, he, his = P.next()
    got = 2000 + 800
    assert 2800 - 1235 == 1565
    add("At Chinese New Year, %s gets $20 in one red packet and $8 in another. %s spends $12.35 on a toy. "
        "How much money does %s have left?" % (n, cap(he), he), 1565,
        [(765, "%s takes the toy money from $20 only"), (1635, "%s takes $12 from $28 and just brings down the 35¢"),
         (1665, "%s forgets the $1 used up to make the cents")],
        "Step 1: $20 + $8 = $28. Step 2: $28.00 − $12.35. " + count_on(1235, 2800) + " %s has <b>$15.65</b> left." % cap(he))
    # 16 canteen, how much more
    n, he, his = P.next()
    a, b = 235, 180
    add("%s spends $1.80 at the canteen on Monday and $2.35 on Tuesday. How much more does %s spend on Tuesday?" % (n, he),
        a - b, sub_mistakes(a, b), sub_expl(a, b))
    # 17 bookshop, enough?
    n, he, his = P.next()
    assert 695 + 280 == 975 and 1000 - 975 == 25
    add("%s has $10. At the bookshop, %s wants a storybook for $6.95 and a bookmark for $2.80. Does %s have enough money?"
        % (n, he, he), "Yes. %s has 25¢ left." % cap(he),
        ["No. %s needs 25¢ more." % cap(he), "Yes. %s has $3.05 left." % cap(he), "Yes. %s has $1.25 left." % cap(he)],
        "Total: $6.95 + $2.80. Cents: 95¢ + 80¢ = 175¢ = $1.75. Dollars: $6 + $2 + $1 = $9. Total $9.75, less than $10. "
        "$10.00 − $9.75 = <b>25¢ left</b>. $3.05 left forgets the bookmark. $1.25 left forgets the $1 from renaming 175¢.")
    # 18 hawker, change
    sp = 340 + 150
    assert sp == 490 and 1000 - sp == 510
    add("At the hawker centre, Mr Rahman buys 2 pieces of prata for $3.40 and a cup of teh for $1.50. "
        "He pays with a $10 note. How much change does he get?", 510,
        [(490, "%s is the money spent, not the change"), (690, "%s takes $4 from $10 and just brings down the 90¢"),
         (610, "%s forgets the $1 used up to make the cents")],
        "Step 1, money spent: $3.40 + $1.50 = $4.90. Step 2, change: " + count_on(490, 1000) + " Change: <b>$5.10</b>.")
    # 19 part-whole, find a part
    n1, _, _ = P.next()
    n2, _, _ = P.next()
    add("%s and %s have $25 altogether. %s has $13.45. How much money does %s have?" % (n1, n2, n1, n2),
        1155, change_mistakes(2500, 1345), count_on(1345, 2500) + " %s has <b>$11.55</b>." % n2,
        model=bar_parts([(1345, "$13.45"), (1155, "?")], "$25"))
    # 20 three parts, money left
    n, he, his = P.next()
    sp = 1275 + 960
    assert sp == 2235 and 3000 - sp == 765
    add("%s has $30. In one week, %s spends $12.75 at the bookshop and $9.60 at the canteen. How much money does %s have left?"
        % (n, he, he), 765,
        [(2235, "%s is the money spent, not the money left"), (865, "%s forgets the $1 from renaming 135¢ when adding"),
         (835, "%s takes $22 from $30 and just brings down the 35¢")],
        "Step 1, money spent: $12.75 + $9.60 = $22.35. Step 2, money left: $30.00 − $22.35. " + count_on(sp, 3000)
        + " %s has <b>$7.65</b> left." % cap(he),
        model=bar_parts([(1275, "$12.75"), (960, "$9.60"), (765, "?")], "$30"))
    assert len(its) == 20, len(its)
    return {"title": "Word problems: canteen, bookshop and hawker centre", "items": its}


# ============================================================ lesson
def body_html():
    coins = ["C5", "C10", "C20", "C50", "C100"]
    notes = ["N2", "N5", "N10", "N50", "N100"]
    assert 345 + 280 == 625 and 520 - 275 == 245 and 1000 - 345 == 655
    return (
        "<h2>Dollars and cents</h2>"
        "<p>$1 = 100¢. In decimal notation, the dollars come before the point and the cents after it. "
        "The cents always take 2 places: 3 dollars 45 cents is $3.45, and 6 dollars 5 cents is $6.05.</p>"
        "<figure class='sn-fig'>" + money_svg(coins, per_row=5, label="Singapore coins: 5¢, 10¢, 20¢, 50¢ and $1") +
        "<figcaption>Coins: 5¢, 10¢, 20¢, 50¢ and $1.</figcaption></figure>"
        "<figure class='sn-fig'>" + money_svg(notes, per_row=5, label="Singapore notes: $2, $5, $10, $50 and $100") +
        "<figcaption>Notes: $2, $5, $10, $50 and $100.</figcaption></figure>"
        "<h2>Add money</h2>"
        "<p>Add the cents first, then the dollars. If the cents make 100¢ or more, rename 100¢ as $1.</p>"
        "<figure class='sn-fig'>" + column_svg([345, 280], "+", answer=625, fs=34) +
        "<figcaption>$3.45 + $2.80: 45¢ + 80¢ = 125¢. Rename 100¢ as $1: 125¢ = $1.25. "
        "$3 + $2 + $1 = $6. Answer: $6.25.</figcaption></figure>"
        "<h2>Subtract money</h2>"
        "<p>Subtract the cents first. If there are not enough cents, rename $1 as 100¢.</p>"
        + ex("Example 1", "What is $5.20 − $2.75?",
             "20¢ − 75¢: not enough cents. Rename $1 as 100¢: $5.20 = $4 and 120¢. "
             "120¢ − 75¢ = 45¢. $4 − $2 = $2. Check: $2.45 + $2.75 = $5.20.", "$2.45") +
        "<h2>Change: count on from the price</h2>"
        "<p>Change = money paid − price. An easy way is to count on: from the price to the next 10¢, "
        "then to the next dollar, then to the money paid. Add the jumps.</p>"
        "<figure class='sn-fig'>" + change_line(345, 1000) +
        "<figcaption>Change from $10 for $3.45: 5¢ + 50¢ + $6 = $6.55.</figcaption></figure>"
        "<h2>Compare prices</h2>"
        "<p>Compare the dollars first. If the dollars are the same, compare the cents: $4.50 is more than $4.05. "
        "To find how much more or how much cheaper, subtract.</p>"
        "<h2>Word problems: draw a bar model</h2>"
        "<p>Draw the whole and the parts. Put a ? on the amount you need to find.</p>"
        "<figure class='sn-fig'>" + bar_parts([(2460, "$24.60"), (975, "$9.75"), (1565, "?")], "$50") +
        "<figcaption>A dictionary costs $24.60 and a storybook costs $9.75. Pay with $50. "
        "Spent: $24.60 + $9.75 = $34.35. Change: $50.00 − $34.35 = $15.65.</figcaption></figure>"
        "<h2>Common mistakes</h2>" +
        table(["Mistake", "What to do instead"], [
            ["$3.45 + $2.80 = $5.125", "125¢ = $1.25. Rename 100¢ as $1: $6.25"],
            ["$3.45 + $2.80 = $5.25", "Do not forget the $1 from renaming 100¢"],
            ["$5.20 − $2.75 = $3.55", "Rename $1 as 100¢: 120¢ − 75¢ = 45¢, so $2.45"],
            ["$10 − $3.45 = $7.45", "Write $10 as $10.00, then rename: $6.55"],
            ["Giving the price as the change", "Change = money paid − price"],
        ])
    )


FAQ = [
    {"q": "What is taught in P3 money?",
     "a": "In Primary 3, students add and subtract money in decimal notation, such as $3.45 + $2.80 and $10 − $3.45. "
          "They find change, compare prices and solve word problems with bar models."},
    {"q": "How do I explain adding money to my child?",
     "a": "Add the cents first, then the dollars. If the cents make 100¢ or more, rename 100¢ as $1: "
          "$3.45 + $2.80 is 125¢ and $5, so the total is $6.25."},
    {"q": "What is the most common mistake with money?",
     "a": "The most common mistake is writing $3.45 + $2.80 = $5.125 instead of renaming 125¢ as $1.25. "
          "Another is giving the price instead of the change in a word problem."},
    {"q": "Is this in the MOE syllabus?",
     "a": "Yes. Adding and subtracting money in decimal notation is part of the Primary 3 Money topic in the "
          "MOE 2021 Primary Mathematics Syllabus (Standard Mathematics)."},
]


def mark_large(u, pattern):
    rx = re.compile(r"<svg (?=[^>]*aria-label='(?:" + pattern + "))")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u


def verify(sets):
    """Recompute every 'What is a ± b?' answer and every column picture from its text."""
    n = 0
    for s in sets:
        for it in s["items"]:
            right = mval(it["c"][it["a"]])
            m = re.search(r"What is (\$[\d.]+(?:¢)?|\d+¢) ([+−]) (\$[\d.]+|\d+¢)\?$", it["q"])
            if m:
                a, op, b = mval(m.group(1)), m.group(2), mval(m.group(3))
                assert right == (a + b if op == "+" else a - b), it["q"]
                n += 1
            m = re.search(r"aria-label='(\$[\d.]+) (plus|minus) (\$[\d.]+) written in columns", it["q"])
            if m:
                a, op, b = mval(m.group(1)), m.group(2), mval(m.group(3))
                assert right == (a + b if op == "plus" else a - b), it["q"]
                n += 1
            m = re.search(r"aria-label='counting on from (\$[\d.]+) to (\$\d+)'", it["q"])
            if m:
                assert right == mval(m.group(2)) - mval(m.group(1)), it["q"]
                n += 1
    return n


def gen():
    rnd = random.Random(63807)
    P = People(rnd)
    seen = set()
    sets = [set_add(P, rnd, seen), set_sub(P, rnd, seen), set_change(P, rnd), set_compare(P, rnd), set_words(P, rnd)]
    balance(sets, rnd)
    nv = verify(sets)
    assert nv >= 30, nv
    keys = set()
    for s in sets:
        assert len(s["items"]) == 20, (s["title"], len(s["items"]))
        assert sorted(it["a"] for it in s["items"]) == sorted([0, 1, 2, 3] * 5)
        for it in s["items"]:
            assert len(set(it["c"])) == 4, it
            vv = [mval(c) for c in it["c"] if mval(c) is not None]
            assert len(set(vv)) == len(vv), it["c"]
            assert it["q"].count("<svg") <= 1, it["q"]
            assert it["q"] not in keys, it["q"]
            keys.add(it["q"])
            for x in [it["q"], it["e"]] + it["c"]:
                assert "\\" not in x and '"' not in x, x
    u = {
        "country": "sg", "subject": "maths", "grade": "primary-3", "slug": "money", "sort": 7,
        "updated": UPDATED, "pdf_url": "",
        "title": "Primary 3 Money: Adding and Subtracting Money",
        "seo_title": "P3 Money Worksheets: Free Primary 3 Maths with Answers (MOE Syllabus)",
        "short_title": "Money",
        "domain": "Number and Algebra",
        "standard_code": "Primary 3: Money",
        "standard_url": "https://www.moe.gov.sg/primary/curriculum/syllabus",
        "standard_text": "Adding and subtracting money in decimal notation",
        "meta_desc": "Free P3 maths: add and subtract money in decimal notation, find change from $10 or $50, "
                     "compare prices and solve word problems. 100 questions with answers.",
        "key_big": "Add or subtract the cents first. 100¢ = $1, so rename when you need to.",
        "key_sub": "$3.45 + $2.80: 45¢ + 80¢ = 125¢ = $1.25, and $3 + $2 + $1.25 = $6.25.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }
    return mark_large(u, "bar model|counting on|price list|money:")


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
