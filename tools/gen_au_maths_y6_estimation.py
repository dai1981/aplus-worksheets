# -*- coding: utf-8 -*-
"""
Australia Year 6 Maths: Estimation and Financial Problems
(Australian Curriculum v9.0, AC9M6N08)
  python3 tools/gen_au_maths_y6_estimation.py
Decimals are worked with Decimal (ROUND_HALF_UP), money with whole cents, so every answer is exact.
Writing money: under $1 as 75c, from $1 as $3.45; rounded estimates as whole dollars ($20).
Every answer is checked in code. HTML attributes use single quotes (no backslashes in the JSON).
"""
import json, os, random, re
from decimal import Decimal as D, ROUND_HALF_UP, ROUND_FLOOR
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "au", "maths", "year-6")
UPDATED = "2026-11-02"
GREEN = "#006633"
RED = "#c0392b"
INK = "#2b2b2b"
GREY = "#6b6259"
TAG = "#fff4d6"
TAGEDGE = "#b8860b"
FONT = "Arial, Helvetica, sans-serif"
NB = " "
MINUS = "−"
GIRLS = ["Charlotte", "Isla", "Mia", "Amelia", "Ava", "Harper", "Chloe", "Ruby", "Mei", "Zara", "Matilda", "Sienna", "Grace"]
BOYS = ["Oliver", "Jack", "Noah", "William", "Leo", "Lachlan", "Liam", "Aarav", "Kai", "Cooper", "Ethan"]


# ------------------------------------------------------------ numbers and money
def nf(n):
    """4536 -> '4536', 37080 -> '37 080' (no-break space from 5 digits)."""
    assert n >= 0, n
    s = str(n)
    if len(s) < 5:
        return s
    out = []
    while s:
        out.insert(0, s[-3:])
        s = s[:-3]
    return NB.join(out)


def ds(x):
    """Decimal -> plain text, keeping the places it has ('10.0' stays '10.0')."""
    s = format(x, "f")
    if "." in s:
        a, b = s.split(".")
        return nf(int(a)) + "." + b
    return nf(int(s))


def r_to(x, places):
    """round half up to a number of decimal places (0 = whole number)"""
    return D(x).quantize(D(1).scaleb(-places), rounding=ROUND_HALF_UP)


def fl_to(x, places):
    return D(x).quantize(D(1).scaleb(-places), rounding=ROUND_FLOOR)


def aud(c):
    """cents -> '75c' or '$3.45'"""
    assert c > 0 and c == int(c), c
    c = int(c)
    return "%dc" % c if c < 100 else "$%s.%02d" % (nf(c // 100), c % 100)


def dol(c):
    """whole dollars: 1400 -> '$14'"""
    assert c % 100 == 0 and c > 0, c
    return "$" + nf(int(c) // 100)


def money(c):
    return dol(c) if c % 100 == 0 else aud(c)


NUM = re.compile(r"^(?:about )?(\$)?(\d+(?:\.\d+)?)(c|%)?(?: (.+))?$")


def val(s):
    """Value of a number or money text: (unit, Decimal). Money is in cents. None for words."""
    s = re.sub(r"<[^>]+>", "", s).replace(NB, "")
    m = NUM.match(s)
    if not m:
        return None
    x = D(m.group(2))
    if m.group(1):
        return ("$", x * 100, m.group(4) or "")
    if m.group(3) == "c":
        return ("$", x, m.group(4) or "")
    return (m.group(3) or "", x, m.group(4) or "")


def cap(s):
    return s[0].upper() + s[1:]


# ------------------------------------------------------------ helpers
def mcq(q, correct, cands, e):
    """correct is a string; cands are strings (None skipped). Wrong choices equal in value to the answer
    or to another choice are dropped. The first 3 left are used."""
    seen_t, seen_v = {correct}, {val(correct)} - {None}
    pick = []
    for x in cands:
        if x is None:
            continue
        v = val(x)
        if x in seen_t or (v is not None and v in seen_v):
            continue
        seen_t.add(x)
        if v is not None:
            seen_v.add(v)
        pick.append(x)
        if len(pick) == 3:
            break
    assert len(pick) == 3, (q, correct, cands)
    return {"q": q, "c": [correct] + pick, "a": 0, "e": e}


def balance(sets, rnd):
    """Each position (A to D) is the right answer 5 times in every set."""
    for s in sets:
        targets = [0, 1, 2, 3] * 5
        rnd.shuffle(targets)
        for it, t in zip(s["items"], targets):
            c = it["c"]
            right = c[it["a"]]
            wrong = [x for i, x in enumerate(c) if i != it["a"]]
            rnd.shuffle(wrong)
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


def text(x, y, t, fs=16, anchor="middle", col=INK, wt=700):
    return ("<text x='%.1f' y='%.1f' font-size='%d' font-weight='%d' fill='%s' text-anchor='%s'>%s</text>"
            % (x, y, fs, wt, col, anchor, t))


def table(head, rows):
    h = "".join("<th>%s</th>" % x for x in head)
    b = "".join("<tr>" + "".join("<td>%s</td>" % c for c in r) + "</tr>" for r in rows)
    return "<div class='sn-tw'><table class='sn-table'><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>" % (h, b)


def ex(title, q, s, a):
    return ("<div class='sn-ex'><span class='sn-ex-t'>%s</span><p class='sn-ex-q'>%s</p>"
            "<p class='sn-ex-s'>%s</p><p class='sn-ex-a'>Answer: %s</p></div>" % (title, q, s, a))


def mark_large(u, pattern):
    rx = re.compile(r"<svg (?=[^>]*aria-label='" + pattern + ")")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u


# ------------------------------------------------------------ pictures
def number_line_svg(lo, hi, n, places):
    """Decimal number line from lo to hi with 10 equal steps; labels at both ends and halfway; red dot on n.
    places = decimal places of lo and hi (0 for whole numbers)."""
    lo, hi, n = D(lo), D(hi), D(n)
    L, R, Y = 52, 388, 52
    W, H = 440, 96
    span = hi - lo
    mid = lo + span / 2
    step = span / 10

    def X(v):
        return L + float((v - lo) / span) * (R - L)

    s = ["<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='2'/>" % (L - 10, Y, R + 10, Y, INK)]
    for i in range(11):
        v = lo + step * i
        big = i in (0, 5, 10)
        s.append("<line x1='%.1f' y1='%d' x2='%.1f' y2='%d' stroke='%s' stroke-width='%d'/>"
                 % (X(v), Y - (11 if big else 6), X(v), Y + (11 if big else 6), INK, 2 if big else 1))
        if big:
            lab = ds(r_to(v, places + (1 if i == 5 else 0)))
            s.append(text(X(v), Y + 32, lab, 15, col=GREY if i == 5 else GREEN))
    s.append("<circle cx='%.1f' cy='%d' r='7' fill='%s'/>" % (X(n), Y, RED))
    tx = min(max(X(n), 40), W - 40)
    s.append(text(tx, Y - 18, ds(n), 16, col=RED, wt=800))
    return svg_wrap(W, H, "".join(s), "number line from %s to %s" % (ds(lo), ds(hi)))


def tags_svg(items):
    """Price tags in one row: items = [(name, cents), ...]"""
    tw, th, gap, pad = 112, 66, 10, 4
    W = pad * 2 + len(items) * tw + (len(items) - 1) * gap
    H = th + pad * 2
    s = []
    for i, (name, p) in enumerate(items):
        x = pad + i * (tw + gap)
        s.append("<rect x='%d' y='%d' width='%d' height='%d' rx='8' fill='%s' stroke='%s' stroke-width='2'/>"
                 % (x, pad, tw, th, TAG, TAGEDGE))
        s.append("<circle cx='%d' cy='%d' r='4' fill='#fff' stroke='%s' stroke-width='1.5'/>" % (x + 12, pad + 12, TAGEDGE))
        s.append(text(x + tw / 2, pad + 26, name, 15, col=GREY))
        s.append(text(x + tw / 2, pad + 54, aud(p), 20))
    return svg_wrap(W, H, "".join(s), "price tags: " + ", ".join("%s %s" % (n, aud(p)) for n, p in items))


# ============================================================ set 1: round decimals
def q_round(x, places, unit="", line=False):
    """Round x to a whole number (places 0) or to one decimal place (places 1)."""
    x = D(x)
    r = r_to(x, places)
    lo = fl_to(x, places)
    step = D(1).scaleb(-places)
    hi = lo + step
    look = "tenths" if places == 0 else "hundredths"
    d = int(x.scaleb(places + 1)) % 10
    u = (" " + unit) if unit else ""
    f = lambda v: ds(v) + u
    cands = [lo if r == hi else hi]                               # rounded the wrong way
    cands.append(r_to(x, places + 1))                             # rounded to the wrong place (one more place)
    if places == 1:
        cands.append(r_to(x, 0))                                  # rounded to a whole number
    else:
        cands.append(r_to(x, -1))                                 # rounded to the nearest ten
    dbl = r_to(r_to(x, places + 1), places)                       # rounded twice: 15.49 -> 15.5 -> 16
    if dbl != r:
        cands.insert(0, dbl)
    if places == 1 and r == hi and int(hi.scaleb(1)) % 10 == 0:   # 9.96 -> 9.10 (did not regroup)
        cands.insert(0, D(str(int(lo)) + ".10"))
    if places == 0 and r == hi:
        cands.append(x + 1)                                       # added 1 but kept the decimals: 4.62 -> 5.62
    cands += [r + step, r - step, x]
    cands = [c for c in cands if c != r and (c > 0 or (c == 0 and x < 1))]
    e = ("%s is between %s and %s. Look only at the %s digit: %d. It is %s, so round %s to <b>%s</b>."
         % (f(x), f(lo), f(hi), look, d, "5 or more" if d >= 5 else "4 or less", "up" if r == hi else "down", f(r)))
    if dbl != r:
        e += " Do not round twice (%s → %s → %s)." % (ds(x), ds(r_to(x, places + 1)), ds(dbl))
    if places == 1 and r == hi and int(hi.scaleb(1)) % 10 == 0:
        e += " One more tenth than %s is %s (10 tenths make 1 whole)." % (ds(lo), ds(hi))
    what = "a whole number" if places == 0 else "one decimal place"
    if unit:
        q = "Round %s to the nearest %s." % (f(x), {"kg": "kilogram", "m": "metre", "L": "litre"}[unit]) \
            if places == 0 else "Round %s to one decimal place." % f(x)
    else:
        q = "Round %s to %s." % (ds(x), what)
    if line:
        q = fig(number_line_svg(lo, hi, x, places)) + q
    return mcq(q, f(r), [f(c) for c in cands], e)


def set_round():
    its = []
    for x, u, ln in [("4.62", "", True), ("7.38", "", False), ("12.5", "", True), ("15.49", "", True),
                     ("39.6", "", False), ("0.83", "", False), ("6.507", "", False), ("23.09", "", False),
                     ("48.45", "kg", False), ("2.7", "L", False)]:
        its.append(q_round(x, 0, u, ln))
    for x, u, ln in [("3.46", "", True), ("8.72", "", False), ("5.35", "", False), ("2.049", "", True),
                     ("9.96", "", True), ("14.682", "", False), ("0.374", "", False), ("6.95", "", False),
                     ("11.14", "m", False), ("3.351", "kg", False)]:
        its.append(q_round(x, 1, u, ln))
    return {"title": "Round decimals", "items": its}


# ============================================================ set 2: estimate with decimals
def est_sum(nums, ops):
    """nums: Decimal texts; ops: '+'/'-' between them. Round each to a whole number."""
    xs = [D(n) for n in nums]
    rs = [r_to(x, 0) for x in xs]
    fs = [fl_to(x, 0) for x in xs]

    def calc(v):
        t = v[0]
        for o, y in zip(ops, v[1:]):
            t = t + y if o == "+" else t - y
        return t

    est, exact, down = calc(rs), calc(xs), calc(fs)
    assert est != exact and est > 0
    sym = lambda o: "+" if o == "+" else MINUS
    expr = ds(xs[0]) + "".join(" %s %s" % (sym(o), ds(y)) for o, y in zip(ops, xs[1:]))
    rexpr = ds(rs[0]) + "".join(" %s %s" % (sym(o), ds(y)) for o, y in zip(ops, rs[1:]))
    e = "Round each number to the nearest whole number: %s = <b>%s</b>. (The exact answer is %s.)" % (
        rexpr, ds(est), ds(exact.normalize()))
    q = "Estimate %s by rounding each number to the nearest whole number." % expr
    return mcq(q, ds(est), [ds(down), ds(exact.normalize()), ds(est * 10), ds(est + 1), ds(est - 1)], e)


def est_prod(a, b):
    xa, xb = D(a), D(b)
    ra, rb = r_to(xa, 0), r_to(xb, 0)
    est, exact = ra * rb, xa * xb
    down = fl_to(xa, 0) * fl_to(xb, 0)
    up = (fl_to(xa, 0) + (xa != fl_to(xa, 0))) * (fl_to(xb, 0) + (xb != fl_to(xb, 0)))
    exact = exact.normalize()
    assert est != exact
    e = "%s rounds to %s%s. %s × %s = <b>%s</b>. (The exact answer is %s.)" % (
        a, ds(ra), "" if xb == rb else " and %s rounds to %s" % (b, ds(rb)), ds(ra), ds(rb), ds(est), ds(exact))
    q = "Estimate %s × %s by rounding to whole numbers." % (a, b)
    return mcq(q, ds(est), [ds(down), ds(est * 10), ds(exact), ds(up)], e)


def est_div(a, k, c):
    """a ÷ k, with c a compatible number near a"""
    xa = D(a)
    est = D(c) / k
    assert est == int(est) and abs(D(c) - xa) < 1
    trunc = int(xa) // k
    e = "%s is close to %d, and %d ÷ %d = %d exactly. So %s ÷ %d is about <b>%s</b>. (The exact answer is %s.)" % (
        a, c, c, k, int(est), a, k, ds(est), ds(r_to(xa / k, 2)) if xa / k != r_to(xa / k, 2) else ds(xa / k))
    if xa / k != r_to(xa / k, 2):
        e = e.replace("(The exact answer is", "(The exact answer is about")
    q = "Use a compatible number to estimate %s ÷ %d." % (a, k)
    return mcq(q, ds(est), [ds(D(trunc)), ds(est * 10), ds(est / 10), ds(est + 1)], e)


def set_est():
    its = []
    for nums, ops in [(["4.8", "7.3"], "+"), (["12.65", "6.4"], "+"), (["15.62", "8.9"], "-"),
                      (["23.4", "9.75"], "-"), (["3.71", "5.48", "8.2"], "++"), (["31.18", "17.6"], "+")]:
        its.append(est_sum(nums, ops))
    for a, b in [("6.8", "4"), ("7.2", "8"), ("9.85", "6"), ("3.9", "5.1"), ("4.6", "2.3"), ("12.4", "3.8")]:
        its.append(est_prod(a, b))
    for a, k, c in [("23.7", 6, 24), ("41.6", 7, 42), ("63.5", 8, 64)]:
        its.append(est_div(a, k, c))
    # friendly decimals
    for a, b, f, fb, est, wr, how in [
        ("0.48", "62", "0.5", "60", 30, [300, 3, 12], "0.48 is close to 0.5, which is one half. Half of 60 is"),
        ("0.26", "81", "0.25", "80", 20, [40, 200, 2], "0.26 is close to 0.25, which is one quarter. A quarter of 80 is"),
        ("0.49", "398", "0.5", "400", 200, [2000, 20, 100], "0.49 is close to 0.5. Half of 400 is"),
        ("0.11", "59", "0.1", "60", 6, [60, D("0.6"), 12], "0.11 is close to 0.1, which is one tenth. One tenth of 60 is"),
        ("0.24", "159", "0.25", "160", 40, [80, 400, 4], "0.24 is close to 0.25. A quarter of 160 is"),
    ]:
        assert D(f) * D(fb) == est
        exact = D(a) * D(b)
        assert abs(exact - est) / est < D("0.1")
        e = "%s <b>%d</b>. (The exact answer is %s.)" % (how, est, ds(exact))
        its.append(mcq("Estimate %s × %s." % (a, b), ds(D(est)), [ds(D(x)) for x in wr], e))
    return {"title": "Estimate with decimals", "items": its}


# ============================================================ set 3: estimate percentages
def set_pct(P):
    its = []

    def add(q, right, cands, e, fmt=dol):
        its.append(mcq(q, fmt(right) if not isinstance(right, str) else right,
                       [fmt(x) if not isinstance(x, str) else x for x in cands], e))

    def chk(pct, amount, friendly, est, fp=None):
        assert F(fp or pct, 100) * friendly == est, (pct, friendly, est)
        exact = F(pct, 100) * amount
        assert abs(exact - est) / est < F(1, 8), (pct, amount, exact, est)

    chk(25, 79, 80, 20)
    add("Estimate 25% of $79.", 2000, [4000, 5400, 2500],
        "$79 is close to $80. 25% is one quarter: $80 ÷ 4 = <b>$20</b>. (The exact answer is $19.75.)")
    chk(50, 198, 200, 100)
    add("Estimate 50% of 198.", "100", ["50", "20", "148"],
        "198 is close to 200. 50% is one half: 200 ÷ 2 = <b>100</b>. (The exact answer is 99.)")
    chk(10, 61, 60, 6)
    add("Estimate 10% of $61.", 600, [6000, 60, 5100],
        "$61 is close to $60. 10% is one tenth: $60 ÷ 10 = <b>$6</b>. (The exact answer is $6.10.)", fmt=money)
    chk(9, 412, 400, 40, 10)
    add("Estimate 9% of 412 by using 10% of 400.", "40", ["400", "4", "46"],
        "9% is close to 10%, and 412 is close to 400. 10% of 400 = 400 ÷ 10 = <b>40</b>. "
        "(The exact answer is 37.08. 9% does not mean divide by 9.)")
    chk(75, 41, 40, 30)
    add("Estimate 75% of $41.", 3000, [1000, 2000, 300],
        "$41 is close to $40. 25% of $40 is $10, so 75% is 3 × $10 = <b>$30</b>. (The exact answer is $30.75.)")
    chk(20, 148, 150, 30)
    add("Estimate 20% of $148.", 3000, [750, 1500, 12800],
        "$148 is close to $150. 10% of $150 is $15, so 20% is 2 × $15 = <b>$30</b>. (The exact answer is $29.60.)",
        fmt=money)
    chk(49, 803, 800, 400, 50)
    add("Estimate 49% of 803.", "400", ["4000", "40", "16"],
        "49% is close to 50%, and 803 is close to 800. Half of 800 is <b>400</b>. (The exact answer is 393.47.)")
    chk(1, 2995, 3000, 30)
    add("Estimate 1% of $2995.", 3000, [30000, 300, 299500],
        "$2995 is close to $3000. 1% is one hundredth: $3000 ÷ 100 = <b>$30</b>. (The exact answer is $29.95.)")
    chk(5, 199, 200, 10)
    add("Estimate 5% of $199.", 1000, [4000, 2000, 100],
        "$199 is close to $200. 10% of $200 is $20, so 5% is half of that: <b>$10</b>. "
        "(The exact answer is $9.95. 5% does not mean divide by 5.)", fmt=money)
    chk(24, 121, 120, 30, 25)
    add("Estimate 24% of 121 kg.", "30 kg", ["60 kg", "97 kg", "5 kg"],
        "24% is close to 25%, and 121 kg is close to 120 kg. 120 kg ÷ 4 = <b>30 kg</b>. (The exact answer is 29.04 kg.)")
    # discounts and groups
    chk(30, F(5995, 100), 60, 18)
    add("A jacket costs $59.95. It is 30% off. About how much do you save?", 1800, [3000, 4200, 200],
        "$59.95 is close to $60. 10% of $60 is $6, so 30% is 3 × $6 = <b>$18</b>. "
        "(The exact saving is $17.99. $42 would be the sale price, not the saving.)")
    chk(25, 119, 120, 30)
    add("Runners cost $119. They are 25% off. About how much is the sale price?", 9000, [3000, 9400, 15000],
        "$119 is close to $120. 25% of $120 is $30, so the sale price is about $120 " + MINUS + " $30 = <b>$90</b>. "
        "(The exact sale price is $89.25.)")
    chk(40, F(4995, 100), 50, 20)
    add("A video game costs $49.95. It is 40% off. About how much is the sale price?", 3000, [2000, 1000, 7000],
        "$49.95 is close to $50. 40% of $50 is $20, so the sale price is about $50 " + MINUS + " $20 = <b>$30</b>. "
        "(The exact sale price is $29.97.)")
    chk(15, 81, 80, 12)
    add("A wetsuit costs $81. It is 15% off. About how much do you save?",
        1200, [1500, 6600, 500],
        "$81 is close to $80. 10% of $80 is $8 and 5% is $4, so 15% is $8 + $4 = <b>$12</b>. (The exact saving is $12.15.)")
    chk(52, 297, 300, 150, 50)
    add("A school has 297 students. 52% of them walk to school. About how many students walk?",
        "150", ["52", "245", "6"],
        "52% is close to 50%, and 297 is close to 300. Half of 300 is <b>150</b>. (The exact answer is about 154.)")
    chk(24, 403, 400, 100, 25)
    add("At a school of 403 students, 24% play footy. About how many students play footy?",
        "100", ["200", "24", "379"],
        "24% is close to 25%, and 403 is close to 400. A quarter of 400 is <b>100</b>. (The exact answer is about 97.)")
    assert abs(F(33, 100) * 612 - 200) < 5
    add("At the swimming carnival, 33% of the 612 students swim in a race. About how many students is that?",
        "200", ["300", "33", "579"],
        "33% is about one third. 612 is close to 600, and one third of 600 is <b>200</b>. (The exact answer is about 202.)")
    chk(5, 495, 500, 25)
    name, she, her = P.next()
    add("%s has $495 in a bank account. The bank pays 5%% interest a year. About how much interest does %s earn "
        "in one year?" % (name, she), 2500, [10000, 250, 25000],
        "$495 is close to $500. 10% of $500 is $50, so 5% is half of that: <b>$25</b>. (The exact interest is $24.75.)",
        fmt=money)
    add("Which is more: 48% of $62 or 26% of $79?", "48% of $62 (about $30)",
        ["26% of $79 (about $40)", "26% of $79 (about $20)", "They are about the same"],
        "48% of $62 is about half of $60 = $30. 26% of $79 is about a quarter of $80 = $20. "
        "So <b>48% of $62</b> is more. (Exact: $29.76 and $20.54.)")
    assert abs(F(19, 41) - F(1, 2)) < F(1, 20)
    name, she, her = P.next()
    add("%s scores 19 out of 41 on a quiz. About what percentage is that?" % name,
        "50%", ["19%", "41%", "25%"],
        "19 out of 41 is close to 20 out of 40, which is one half. One half = <b>50%</b>. (The exact answer is about 46%.)")
    return {"title": "Estimate percentages", "items": its}


# ============================================================ set 4: is it reasonable?
def set_reasonable(P):
    its = []
    # where does the decimal point go?
    for a, op, b, ests in [("3.8", "×", "6.2", "4 × 6 = 24"), ("4.5", "×", "7.3", "5 × 7 = 35"),
                           ("0.6", "×", "48.5", "0.6 × 50 = 30"),
                           ("12.4", "×", "2.6", "12 × 3 = 36"), ("56.7", "÷", "7", "56 ÷ 7 = 8")]:
        exact = D(a) * D(b) if op == "×" else D(a) / D(b)
        exact = exact.normalize()
        digits = format(exact, "f").replace(".", "").lstrip("0")
        right = ds(exact)
        others = [ds((exact * D(10) ** k).normalize()) for k in (-1, 1, 2)]
        e = "Estimate: %s. Only <b>%s</b> is close to that." % (ests, right)
        q = ("A calculator gives the digits %s for %s %s %s, but the decimal point is missing. "
             "Use an estimate to choose the answer." % (digits, a, op, b))
        its.append(mcq(q, right, others, e))

    # yes or no
    def yes_no(expr, said, ok, est, big, why, extra=""):
        name, she, her = P.next()
        right = ("Yes, it is close to %s" if ok else "No, it should be about %s") % est
        other = ("No, it should be about %s" if ok else "Yes, it is close to %s") % est
        traps = ["Yes, it is close to %s" % big, "No, it should be about %s" % big]
        e = "Estimate: %s. %s is %s, so it is <b>%s</b>. %s" % (
            why, said, "close to %s" % est if ok else "not close to %s" % est,
            "reasonable" if ok else "not reasonable", extra)
        q = "%s works out %s and gets %s. Use an estimate to check. Is the answer reasonable?" % (name, expr, said)
        its.append(mcq(q, right, [other] + traps, e.strip()))

    assert D("4.9") * D("6.1") == D("29.89")
    yes_no("4.9 × 6.1", "298.9", False, "30", "300", "5 × 6 = 30", "The exact answer is 29.89; the point is in the wrong place.")
    assert D("7.85") + D("3.4") == D("11.25")
    yes_no("7.85 + 3.4", "8.19", False, "11", "1", "8 + 3 = 11",
           "The exact answer is 11.25. Line up the decimal points: 3.4 is 3 ones and 4 tenths, not 34 hundredths.")
    assert D("12.6") - D("4.85") == D("7.75")
    yes_no("12.6 " + MINUS + " 4.85", "7.75", True, "8", "80", "13 " + MINUS + " 5 = 8")
    assert D("8.2") * D("3.9") == D("31.98")
    yes_no("8.2 × 3.9", "31.98", True, "32", "320", "8 × 4 = 32")
    assert D("45.6") / 8 == D("5.7")
    yes_no("45.6 ÷ 8", "57", False, "6", "60", "48 ÷ 8 = 6", "The exact answer is 5.7.")
    assert F(25, 100) * F(8200, 100) == F(2050, 100)
    yes_no("25% of $82", "$41", False, "$20", "$40", "a quarter of $80 is $20",
           "$41 is half of $82, which is 50%. The exact answer is $20.50.")
    assert F(10, 100) * F(6750, 100) == F(675, 100)
    yes_no("10% of $67.50", "$6.75", True, "$7", "$70", "one tenth of $70 is $7")
    assert 6 * 1495 == 8970
    yes_no("6 × $14.95", "$89.70", True, "$90", "$9", "6 × $15 = $90")

    # best estimate
    def best(expr, exact, cands, how):
        exact = D(exact)
        ex_txt = ds(exact.normalize()) if exact == r_to(exact, 2) else "about " + ds(r_to(exact, 2))
        b = min(cands, key=lambda x: abs(D(x) - exact))
        for x in cands:
            if x != b:
                assert abs(D(x) - exact) > abs(D(b) - exact)
        e = "%s = <b>%s</b>. The exact answer is %s, so this estimate is the closest." % (how, b, ex_txt)
        its.append(mcq("Which estimate is closest to the exact answer of %s?" % expr, b,
                       [x for x in cands if x != b], e))

    best("19.6 × 4.95", D("19.6") * D("4.95"), ["100", "76", "80", "1000"], "20 × 5")
    best("38.7 + 21.45 + 9.8", D("38.7") + D("21.45") + D("9.8"), ["70", "68", "60", "700"], "39 + 21 + 10")
    best("81.3 ÷ 9.2", D("81.3") / D("9.2"), ["9", "8", "10", "90"], "81 ÷ 9")
    best("0.52 × 297", D("0.52") * D("297"), ["150", "1500", "15", "200"], "half of 300")

    # units
    name, she, her = P.next()
    assert D("2.4") + D("0.85") == D("3.25")
    its.append(mcq("%s adds 2.4 m and 85 cm and gets 87.4 m. Is the answer reasonable?" % name,
                   "No, it should be about 3 m",
                   ["Yes, it is close to 87 m", "No, it should be about 87 cm", "Yes, the digits add up correctly"],
                   "The units are different. 85 cm is less than 1 m (0.85 m). 2.4 m + 0.85 m is about 2 m + 1 m = 3 m, "
                   "so 87.4 m is <b>not reasonable</b>. The exact answer is 3.25 m."))
    assert 1850 / 150 > 12 and 1850 / 150 < 13
    its.append(mcq("A bag of apples has a mass of 1.85 kg. Each apple is about 150 g. About how many apples are in the bag?",
                   "about 12", ["about 1", "about 120", "about 185"],
                   "Use the same units: 1.85 kg = 1850 g. 1800 g ÷ 150 g = <b>12</b>. "
                   "(Dividing 1.85 by 150 mixes kilograms and grams.)"))
    name, she, her = P.next()
    its.append(mcq("A recipe needs 750 mL of milk. %s has a 2 L bottle that is about one quarter full. "
                   "Does %s have enough milk?" % (name, she),
                   "No, the bottle has about 500 mL",
                   ["Yes, the bottle has about 2 L", "Yes, the bottle has about 750 mL", "No, the bottle has about 0.5 mL"],
                   "2 L = 2000 mL. One quarter of 2000 mL is 500 mL, and 500 mL is less than 750 mL, so <b>no</b>."))
    return {"title": "Is it reasonable?", "items": its}


# ============================================================ set 5: budgets and best buys
def set_words(P):
    its = []

    def add(q, right, cands, e, fmt=money):
        its.append(mcq(q, fmt(right) if not isinstance(right, str) else right,
                       [fmt(x) if not isinstance(x, str) else x for x in cands], e))

    assert 450 * 100 // 500 == 90
    add("A 500 g bag of muesli costs $4.50. What is the price per 100 g?", 90, [900, 45, 225],
        "500 g is 5 lots of 100 g. $4.50 ÷ 5 = <b>90c</b> per 100 g.", fmt=aud)
    assert 580 * 100 // 2000 == 29
    add("A 2 kg bag of rice costs $5.80. What is the price per 100 g?", 29, [290, 58, 580],
        "2 kg = 2000 g, which is 20 lots of 100 g. $5.80 ÷ 20 = <b>29c</b> per 100 g. "
        "($2.90 is the price per kilogram.)", fmt=aud)
    assert F(600, 750) * 100 == 80 and F(750, 1000) * 100 == 75
    its.append(mcq(fig(tags_svg([("750 g", 600), ("1 kg", 750)])) +
                   "Two packets of the same pasta are on sale. Which is the better buy?",
                   "the 1 kg packet: 75c per 100 g",
                   ["the 750 g packet: it costs less", "the 750 g packet: 80c per 100 g", "the 1 kg packet: $7.50 per 100 g"],
                   "Compare the price of 100 g. 750 g: $6.00 ÷ 7.5 = 80c. 1 kg = 1000 g: $7.50 ÷ 10 = 75c. "
                   "<b>The 1 kg packet</b> is the better buy."))
    assert F(620, 10) == 62 and F(180, 2) == 90
    its.append(mcq("A 1 kg tub of yoghurt costs $6.20. A 200 g pot costs $1.80. Which is the better buy?",
                   "the 1 kg tub: 62c per 100 g",
                   ["the 200 g pot: it costs less", "the 200 g pot: 90c per 100 g", "the 1 kg tub: $6.20 per 100 g"],
                   "Use the same unit. 1 kg = 1000 g, so the tub is $6.20 ÷ 10 = 62c per 100 g. "
                   "The pot is $1.80 ÷ 2 = 90c per 100 g. <b>The 1 kg tub</b> is the better buy."))
    up = {n: F(c * 100, g) for n, c, g in [("300 g", 390, 300), ("500 g", 550, 500), ("750 g", 840, 750)]}
    assert min(up, key=up.get) == "500 g" and up["300 g"] == 130 and up["500 g"] == 110 and up["750 g"] == 112
    its.append(mcq(fig(tags_svg([("300 g", 390), ("500 g", 550), ("750 g", 840)])) +
                   "Three boxes of the same cereal. Which box is the best buy?",
                   "the 500 g box", ["the 300 g box", "the 750 g box", "They all cost the same per 100 g"],
                   "Price per 100 g: 300 g: $3.90 ÷ 3 = $1.30. 500 g: $5.50 ÷ 5 = $1.10. 750 g: $8.40 ÷ 7.5 = $1.12. "
                   "<b>The 500 g box</b> is the cheapest per 100 g. The biggest box is not always the best buy."))
    # saving
    name, she, her = P.next()
    assert 15 * 1850 < 28900 <= 16 * 1850
    its.append(mcq("%s wants a bike that costs $289. %s saves $18.50 every week. How many weeks does %s need to save?"
                   % (name, cap(she), she), "16 weeks", ["15 weeks", "14 weeks", "156 weeks"],
                   "Estimate: $300 ÷ $20 = 15, so about 15 weeks. Check: 15 × $18.50 = $277.50, which is not enough. "
                   "16 × $18.50 = $296, so %s needs <b>16 weeks</b>." % she))
    name, she, her = P.next()
    assert 12 * 1500 < 24900 - 6500 <= 13 * 1500
    its.append(mcq("%s has $65. %s wants a bike that costs $249 and saves $15 a week. How many more weeks does %s "
                   "need to save?" % (name, cap(she), she), "13 weeks", ["12 weeks", "17 weeks", "21 weeks"],
                   "%s still needs $249 " % cap(she) + MINUS + " $65 = $184. $184 ÷ $15 is about 12.3. After 12 weeks "
                   "%s has saved $180, which is not enough, so %s needs <b>13 weeks</b>." % (she, she)))
    # budget
    assert 6 * 1495 + 4 * 380 == 10490 and 12000 - 10490 < 2500
    its.append(mcq("Year 6 has $120 for a class party. They buy 6 pizzas at $14.95 each and 4 bottles of juice at "
                   "$3.80 each. Estimate. Is there enough money left for a $25 cake?",
                   "No, only about $14 is left",
                   ["Yes, about $30 is left", "No, only about $24 is left", "Yes, about $106 is left"],
                   "Pizzas: 6 × $15 = $90. Juice: 4 × $4 = $16. $90 + $16 = $106. $120 " + MINUS + " $106 = $14, "
                   "which is less than $25, so <b>no</b>. (Exactly $15.10 is left.)"))
    assert 7900 * 3 // 4 == 5925 and 5925 < 6500
    its.append(mcq("Store A sells a skateboard for $79 with 25% off. Store B sells it for $65. Estimate. "
                   "Which store is cheaper?", "Store A, about $60",
                   ["Store B, $65", "Store A, about $54", "Store A, about $20"],
                   "25% of $80 is $20, so Store A charges about $80 " + MINUS + " $20 = $60. $60 is less than $65, so "
                   "<b>Store A</b> is cheaper. (The exact price is $59.25. $79 " + MINUS + " $25 = $54 treats 25% as $25.)"))
    assert 1499 * 12 == 17988
    add("A streaming service costs $14.99 a month. About how much does it cost for a year?", 18000,
        [15000, 180000, 12000],
        "$14.99 rounds to $15, and a year has 12 months. 12 × $15 = <b>$180</b>. (The exact cost is $179.88.)")
    assert D("7.8") * D("2.9") == D("22.62")
    its.append(mcq("A car uses 7.8 L of petrol for every 100 km. About how much petrol does it use on a 290 km trip?",
                   "24 L", ["240 L", "2.4 L", "37 L"],
                   "290 km is about 3 lots of 100 km, and 7.8 L is about 8 L. 3 × 8 L = <b>24 L</b>. "
                   "(The exact amount is 22.62 L. 290 ÷ 7.8 ≈ 37 mixes up the units.)"))
    assert 189 * 42 == 7938
    add("Petrol costs $1.89 per litre. Dad puts 42 L in the car. About how much does he pay?", 8000,
        [4000, 80000, 800],
        "$1.89 is about $2, and 42 L is about 40 L. 40 × $2 = <b>$80</b>. (The exact cost is $79.38.)")
    name, she, her = P.next()
    assert 3 * 1295 == 3885
    its.append(mcq("%s buys 3 beach towels at $12.95 each. The receipt says $388.50. Is that reasonable?" % name,
                   "No, it should be about $39",
                   ["Yes, it is close to $390", "No, it should be about $3.90", "Yes, it is close to $39"],
                   "$12.95 is about $13. 3 × $13 = $39, so $388.50 is <b>not reasonable</b>. The exact total is $38.85; "
                   "the point is in the wrong place."))
    name, she, her = P.next()
    assert F(25, 100) * 58 == F(29, 2)
    add("%s gets $58 for %s birthday and saves 25%% of it. About how much does %s save?" % (name, her, she), 1500,
        [2900, 3300, 2500],
        "$58 is close to $60. 25% is one quarter: $60 ÷ 4 = <b>$15</b>. (The exact amount is $14.50.)")
    assert 34900 * 80 // 100 == 27920
    add("A bike costs $349. It is 20% off. About how much is the sale price?", 28000, [7000, 32900, 42000],
        "$349 is close to $350. 10% of $350 is $35, so 20% is $70. $350 " + MINUS + " $70 = <b>$280</b>. "
        "(The exact sale price is $279.20.)")
    ps = [2345, 1890, 3160, 1285, 970]
    assert sum(ps) == 9650 and sum((p + 50) // 100 for p in ps) == 97
    add("Mum’s shopping costs $23.45, $18.90, $31.60, $12.85 and $9.70. Round each price to the nearest dollar. "
        "About how much is the total?", 9700, [9300, 9800, 97000],
        "$23 + $19 + $32 + $13 + $10 = <b>$97</b>. (The exact total is $96.50.)")
    assert 148 * 295 == 43660
    add("Year 6 sells 148 ice blocks at $2.95 each at the school fete. About how much money do they raise?", 45000,
        [30000, 4500, 450000],
        "148 is about 150 and $2.95 is about $3. 150 × $3 = <b>$450</b>. (The exact amount is $436.60.)")
    name, she, her = P.next()
    assert 2 * 3 * 2850 == 17100
    add("Kayak hire costs $28.50 per kayak for each hour. %s’s family hires 2 kayaks for 3 hours. "
        "About how much do they pay?" % name, 18000, [9000, 6000, 180000],
        "$28.50 is about $30. 2 kayaks for 3 hours is 2 × 3 = 6 kayak-hours. 6 × $30 = <b>$180</b>. "
        "(The exact cost is $171.)")
    assert F(38500, 5) == 7700
    add("Year 6 camp costs $385. Families can pay in 5 equal payments. About how much is each payment?", 8000,
        [800, 80000, 200000],
        "$385 is close to $400. $400 ÷ 5 = <b>$80</b>. (The exact payment is $77.)")
    assert 12 * 35 == 420 and 4 * 99 == 396
    its.append(mcq("Phone plan A costs $35 a month. Plan B costs $99 for 3 months. Which is cheaper for a whole year, "
                   "and by how much?", "Plan B, by $24", ["Plan A, by $64", "Plan B, by $6", "Plan A, by $24"],
                   "Plan A: 12 × $35 = $420. Plan B: a year is 4 lots of 3 months, so 4 × $99 = $396. "
                   "$420 " + MINUS + " $396 = $24, so <b>Plan B is cheaper by $24</b>."))
    return {"title": "Budgets and best buys", "items": its}


# ============================================================ lesson
def body_html():
    return (
        "<h2>Round first, then estimate</h2>"
        "<p>An estimate is a quick answer that is close to the exact answer. Round the numbers to friendly numbers, "
        "then work it out in your head. To round a decimal, look only at the digit just after the place you round to. "
        "5 or more rounds up; 4 or less rounds down.</p>"
        "<figure class='sn-fig'>" + number_line_svg("4", "5", "4.62", 0) +
        "<figcaption>4.62 is past the halfway point, 4.5, so it rounds up to 5. "
        "To one decimal place it rounds to 4.6.</figcaption></figure>"
        + ex("Estimate with decimals", "Estimate 6.8 × 4.1.",
             "6.8 rounds to 7 and 4.1 rounds to 4. 7 × 4 = 28. (The exact answer is 27.88.)", "about 28")
        + "<h2>Estimating percentages</h2>"
        "<p>Change the percentage into a friendly fraction, and round the amount so it is easy to divide.</p>"
        + table(["Percentage", "Fraction", "How to find it", "Example"], [
            ["50%", "one half", "divide by 2", "50% of $198 ≈ $200 ÷ 2 = $100"],
            ["25%", "one quarter", "divide by 4", "25% of $79 ≈ $80 ÷ 4 = $20"],
            ["10%", "one tenth", "divide by 10", "10% of $61 ≈ $60 ÷ 10 = $6"],
            ["20%", "two tenths", "find 10%, then double", "20% of $148 ≈ 2 × $15 = $30"],
            ["5%", "half of 10%", "find 10%, then halve", "5% of $199 ≈ $20 ÷ 2 = $10"],
        ]) +
        ex("A sale", "A $59.95 jacket is 30% off. About how much is the sale price?",
           "$59.95 is about $60. 10% of $60 is $6, so 30% is $18. $60 " + MINUS + " $18 = $42.", "about $42")
        + "<h2>Best buys and budgets</h2>"
        "<p>To find the best buy, compare the price of the same amount, such as 100 g or 1 kg. "
        "Australian supermarkets show this unit price on the shelf label.</p>"
        "<figure class='sn-fig'>" + tags_svg([("400 g", 320), ("1 kg", 700)]) +
        "<figcaption>400 g: $3.20 ÷ 4 = 80c per 100 g. 1 kg: $7.00 ÷ 10 = 70c per 100 g. "
        "The 1 kg bag is the better buy.</figcaption></figure>"
        + ex("Is it reasonable?", "Kai works out 5.1 × 3.9 and gets 198.9.",
             "Estimate: 5 × 4 = 20. 198.9 is about 10 times too big, so it is not reasonable. "
             "The exact answer is 19.89.", "not reasonable")
        + "<h2>Common mistakes</h2>"
        + table(["Mistake", "What to do instead"], [
            ["Rounding the wrong place: 15.49 → 15.5 → 16", "Look only at the tenths digit: 15.49 rounds to 15"],
            ["Writing 9.96 to one decimal place as 9.10", "10 tenths make 1 whole: 9.96 rounds to 10.0"],
            ["Estimating too far away: 6.8 × 4.1 ≈ 6 × 4 = 24", "Round to the nearest whole number: 7 × 4 = 28"],
            ["25% of $79 ≈ $79 " + MINUS + " $25 = $54", "25% is one quarter: $80 ÷ 4 = $20"],
            ["Ignoring units: comparing $7.50 for 1 kg with $6.00 for 750 g by price only",
             "Change to the same unit and compare the price per 100 g"],
        ])
    )


FAQ = [
    {"q": "What does Year 6 learn about estimation in the Australian Curriculum?",
     "a": "Year 6 students approximate answers to problems with decimals, fractions and percentages, including money "
          "problems, using estimation strategies that suit the problem (AC9M6N08)."},
    {"q": "How do you estimate a percentage of an amount?",
     "a": "Round the amount to a friendly number and use a benchmark percentage: 50% is half, 25% is a quarter and 10% "
          "is a tenth. For 25% of $79, use $80 ÷ 4 = $20."},
    {"q": "How do you find the best buy using the unit price?",
     "a": "Work out the price of the same amount for each item, such as the price per 100 g, and choose the lowest. "
          "Australian supermarkets show this unit price on the shelf label."},
    {"q": "How can my child check if a decimal answer is reasonable?",
     "a": "Round each number to the nearest whole number and work out an estimate in your head. If 4.9 × 6.1 gives "
          "298.9 but 5 × 6 = 30, the decimal point is in the wrong place."},
]


def gen():
    rnd = random.Random(6808)
    P = People(rnd)
    sets = [set_round(), set_est(), set_pct(P), set_reasonable(P), set_words(P)]
    balance(sets, rnd)
    seen = set()
    for s in sets:
        assert len(s["items"]) == 20, (s["title"], len(s["items"]))
        assert sorted(it["a"] for it in s["items"]) == sorted([0, 1, 2, 3] * 5)
        for it in s["items"]:
            assert len(set(it["c"])) == 4, it
            vv = [val(c) for c in it["c"] if val(c) is not None]
            assert len(set(vv)) == len(vv), it["c"]
            assert it["q"] not in seen, it["q"]
            seen.add(it["q"])
            for x in [it["q"], it["e"]] + it["c"]:
                assert "\\" not in x and '"' not in x, x
    u = {
        "country": "au", "subject": "maths", "grade": "year-6", "slug": "estimation-and-financial-problems", "sort": 8,
        "updated": UPDATED, "pdf_url": "",
        "title": "Year 6 Estimation and Financial Problems",
        "seo_title": "Year 6 Estimation and Financial Maths Worksheets: Free with Answer Key (Australian Curriculum)",
        "short_title": "Estimation and Financial Problems",
        "domain": "Number",
        "standard_code": "AC9M6N08",
        "standard_url": "https://v9.australiancurriculum.edu.au/f-10-curriculum/learning-areas/mathematics",
        "standard_text": "Approximate numerical solutions to problems involving rational numbers and percentages, including financial contexts, using appropriate estimation strategies",
        "meta_desc": "Free Year 6 maths worksheets on estimation and financial problems, aligned to the Australian Curriculum (AC9M6N08): round decimals, estimate with decimals, estimate percentages and discounts, check if answers are reasonable, and solve budget, saving and best-buy problems with unit prices. 100 questions with an answer key.",
        "key_big": "Round to friendly numbers, then calculate: 25% of $79 is about 25% of $80 = $20.",
        "key_sub": "To find the best buy, compare the price of the same amount, such as the price per 100 g. Always check an exact answer against your estimate.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }
    return mark_large(u, "(number line|price tags)")


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
