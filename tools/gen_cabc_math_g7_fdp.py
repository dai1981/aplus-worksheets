# -*- coding: utf-8 -*-
"""
British Columbia Grade 7 Math: Fractions, decimals and percents
(BC Mathematics Curriculum, Grade 7, Number — relationships between decimals, fractions, ratios, and percents)
  python3 tools/gen_cabc_math_g7_fdp.py
Fraction <-> decimal including repeating decimals (1/3 = 0.333… = 0.3 with a bar), decimal <-> percent
(including 12.5% and percents over 100%), fraction <-> percent, comparing and ordering mixed forms,
word problems (test scores, a team's win record).
Every answer is checked with fractions.Fraction / decimal.Decimal (never float); repeating decimals are built
from real long division.
Canadian English, metric units. HTML attributes use single quotes (no backslashes in the JSON).
"""
import json, os, random, re
from decimal import Decimal as Dm
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "ca-bc", "math", "grade-7")
UPDATED = "2026-11-02"
FILL = "#4fae74"
LINE = "#2b2b2b"
THIN = "#8a8a8a"
RED = "#d6453b"
BLUE = "#2f6fb5"
FONT = "Arial, Helvetica, sans-serif"
GIRLS = ["Olivia", "Ava", "Chloe", "Simran", "Jasleen", "Mei", "Hana", "Sofia", "Emma", "Leah", "Zara", "Nadia"]
BOYS = ["Liam", "Ethan", "Noah", "Arjun", "Harjot", "Wei", "Mateo", "Lucas", "Kai", "Owen", "Ryan"]


# ------------------------------------------------------------ helpers
def fr(a, b):
    return "<span class='fr'><span class='fn'>%s</span><span class='fd'>%s</span></span>" % (a, b)


def mixed(w, a, b):
    return "%d %s" % (w, fr(a, b))


def bar(s):
    """Digits under a repeat bar."""
    return "<span style='text-decoration:overline;text-decoration-thickness:0.09em'>%s</span>" % s


def period(v):
    """(whole, non-repeating digits, repeating digits) of a positive Fraction, from long division."""
    v = F(v)
    whole, r = divmod(v.numerator, v.denominator)
    d = v.denominator
    digits, seen = [], {}
    while r and r not in seen:
        seen[r] = len(digits)
        r *= 10
        digits.append(str(r // d))
        r %= d
    if not r:
        return whole, "".join(digits), ""
    k = seen[r]
    return whole, "".join(digits[:k]), "".join(digits[k:])


def check_period(v, whole, a, b):
    """Rebuild the value from its digits: whole + 0.a(bbb…)."""
    x = F(whole) + (F(int(a), 10 ** len(a)) if a else 0)
    if b:
        x += F(int(b), (10 ** len(b) - 1) * 10 ** len(a))
    assert x == F(v), (v, whole, a, b)


def dots(v, times=3):
    """Repeating decimal written with dots: 1/6 -> 0.1666…, 5/11 -> 0.454545…"""
    w, a, b = period(v)
    check_period(v, w, a, b)
    assert b, v
    return "%d.%s%s…" % (w, a, b * times)


def bart(v):
    """Repeating decimal written with a bar: 1/6 -> 0.1(6 with a bar)."""
    w, a, b = period(v)
    check_period(v, w, a, b)
    assert b, v
    return "%d.%s%s" % (w, a, bar(b))


def dec(v):
    """Exact decimal text of a Fraction with a terminating decimal."""
    v = F(v)
    d = Dm(v.numerator) / Dm(v.denominator)
    assert F(d) == v, v
    return format(d.normalize(), "f")


def pct(v):
    """Percent text of a Fraction whose percent terminates: 1/8 -> 12.5%."""
    return dec(F(v) * 100) + "%"


def D(s):
    return F(Dm(s))


FRX = re.compile(r"^(?:(\d+) )?<span class='fr'><span class='fn'>(\d+)</span><span class='fd'>(\d+)</span></span>( .+)?$")
NUM = re.compile(r"^(\$)?(\d*\.?\d+)(¢|%)?( .+)?$")


def val(c):
    """Value of a choice (Fraction) with its unit; 20% counts as 0.2 so 20% and 0.2 are equal.
    None for choices that are not a single terminating number (repeating decimals are checked where they are built)."""
    m = FRX.match(c)
    if m:
        return (int(m.group(1) or 0) + F(int(m.group(2)), int(m.group(3))), (m.group(4) or "").strip())
    m = NUM.match(c)
    if not m:
        return None
    v = F(Dm(m.group(2)))
    if m.group(1):
        return (v, "$")
    if m.group(3) == "¢":
        return (v / 100, "$")
    if m.group(3) == "%":
        v = v / 100
    return (v, (m.group(4) or "").strip())


def mcq(q, correct, wrong, e, same_ok=False, value=None):
    """4 choices: correct first + 3 wrong. Positions are set by balance(). No two choices may have the same value
    (same_ok=True only for 'which is NOT equal' and statement choices). value: the exact answer to check."""
    correct = str(correct)
    wrong = [str(x) for x in wrong]
    assert len(wrong) == 3, (q, wrong)
    ch = [correct] + wrong
    assert len(set(re.sub(r"<[^>]+>", "", x) for x in ch)) == 4, (q, ch)
    if value is not None:
        assert val(correct)[0] == F(value), (q, correct, value)
    if not same_ok:
        vs = [val(x) for x in ch]
        known = [v for v in vs if v is not None]
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


def text(x, y, t, fs=16, anchor="middle", col=LINE, weight=700):
    return ("<text x='%.1f' y='%.1f' font-size='%d' font-weight='%d' fill='%s' text-anchor='%s'>%s</text>"
            % (x, y, fs, weight, col, anchor, t))


def table(head, rows):
    h = "".join("<th>%s</th>" % x for x in head)
    b = "".join("<tr>" + "".join("<td>%s</td>" % c for c in r) + "</tr>" for r in rows)
    return "<div class='sn-tw'><table class='sn-table'><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>" % (h, b)


def ex(title, q, s, a):
    return ("<div class='sn-ex'><span class='sn-ex-t'>%s</span><p class='sn-ex-q'>%s</p>"
            "<p class='sn-ex-s'>%s</p><p class='sn-ex-a'>Answer: %s</p></div>" % (title, q, s, a))


# ------------------------------------------------------------ pictures
def bar_svg(n, k, W=264, H=38):
    """One fraction bar of n equal parts, first k shaded."""
    s = []
    for i in range(n):
        s.append("<rect x='%.1f' y='4' width='%.2f' height='%d' fill='%s' stroke='%s' stroke-width='2.5'/>"
                 % (4 + i * W / float(n), W / float(n), H, FILL if i < k else "#fff", LINE))
    return svg_wrap(W + 8, H + 8, "".join(s), "fraction bar of %d equal parts with %d shaded" % (n, k))


def grids_svg(ks, cell=15):
    """Hundred grids side by side (each grid is one whole); ks[i] squares shaded in grid i,
    full columns first, then from the top of the next column."""
    pad, gap = 4, 18
    side = 10 * cell
    s = []
    for g, k in enumerate(ks):
        ox = pad + g * (side + gap)
        for c in range(10):
            for r in range(10):
                if c * 10 + r < k:
                    s.append("<rect x='%d' y='%d' width='%d' height='%d' fill='%s'/>"
                             % (ox + c * cell, pad + r * cell, cell, cell, FILL))
        for i in range(1, 10):
            s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='1.1'/>"
                     % (ox + i * cell, pad, ox + i * cell, pad + side, THIN))
            s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='1.1'/>"
                     % (ox, pad + i * cell, ox + side, pad + i * cell, THIN))
        s.append("<rect x='%d' y='%d' width='%d' height='%d' fill='none' stroke='%s' stroke-width='2.5'/>"
                 % (ox, pad, side, side, LINE))
    w = 2 * pad + len(ks) * side + (len(ks) - 1) * gap
    lab = ("hundred grid with %d of 100 squares shaded" % ks[0] if len(ks) == 1 else
           "%d hundred grids, each one whole, with %s squares shaded" % (len(ks), " and ".join(str(k) for k in ks)))
    return svg_wrap(w, side + 2 * pad, "".join(s), lab)


def rdiv(a, b, places, hide=False):
    """Short division of a ÷ b to `places` decimal places, drawn from the real working, then '…' because the
    remainder never reaches 0. Remainders are carried as small red digits. hide=True draws the answer digits
    after the point as empty boxes."""
    w = str(a)
    cells = list(w) + ["."] + ["0"] * places
    q, carry, rem = [], {}, 0
    for i, ch in enumerate(cells):
        if ch == ".":
            q.append(".")
            continue
        cur = rem * 10 + int(ch)
        q.append(str(cur // b))
        rem = cur % b
        nxt = i + 1 if i + 1 < len(cells) and cells[i + 1] != "." else i + 2
        if rem and nxt < len(cells):
            carry[nxt] = str(rem)
    assert rem != 0, (a, b)
    # the digits drawn are the true decimal of a/b cut off after `places` places
    assert F(Dm("".join(q))) == F(int(F(a, b) * 10 ** places), 10 ** places), (q, a, b)
    lead = 0
    while lead < len(w) - 1 and q[lead] == "0":
        lead += 1
    CW, DW = 30, 14
    xs, x = [], 62
    for ch in cells:
        xs.append(x)
        x += DW if ch == "." else CW
    W = x + 34
    ytop, ybar, ydig = 34, 46, 78
    o = []
    for i, ch in enumerate(cells):
        cx = xs[i] + (DW if ch == "." else CW) / 2.0
        if ch == ".":
            o.append("<circle cx='%.1f' cy='%d' r='3.5' fill='%s'/>" % (cx, ydig - 2, LINE))
            o.append("<circle cx='%.1f' cy='%d' r='3.5' fill='%s'/>" % (cx, ytop - 2, LINE))
            continue
        o.append(text(cx + 3, ydig, ch, 26))
        if i in carry:
            o.append(text(xs[i] + 5, ydig - 14, carry[i], 15, col=RED))
        if i < lead:
            continue
        if hide and i > len(w):
            o.append("<rect x='%.1f' y='%d' width='20' height='24' fill='#fff' stroke='%s' stroke-width='1.8' rx='3'/>"
                     % (cx - 10, ytop - 22, LINE))
        else:
            o.append(text(cx + 3, ytop, q[i], 26))
    o.append(text(x + 14, ytop, "…", 26))
    o.append(text(x + 14, ydig, "…", 26))
    o.append("<line x1='54' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='2.5'/>" % (ybar, W - 6, ybar, LINE))
    o.append("<path d='M 54 %d Q 62 %d 54 %d' fill='none' stroke='%s' stroke-width='2.5'/>" % (ybar, ybar + 22, ybar + 44, LINE))
    o.append(text(30, ydig, str(b), 26))
    return svg_wrap(W, ybar + 50, "".join(o), "short division of %s by %d that keeps going" % ("".join(cells), b))


def line_svg(parts, dot, labels, W=400, what="0 to 1"):
    """Number line with `parts` equal spaces, red dot at tick `dot`. labels: {tick: text}."""
    L, R, Y = 30, W - 30, 30

    def X(i):
        return L + (R - L) * i / float(parts)
    s = ["<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='2.5'/>" % (L, Y, R, Y, LINE)]
    for i in range(parts + 1):
        big = i in labels
        s.append("<line x1='%.1f' y1='%d' x2='%.1f' y2='%d' stroke='%s' stroke-width='%s'/>"
                 % (X(i), Y - (13 if big else 9), X(i), Y + (13 if big else 9), LINE, "2.5" if big else "1.8"))
    for i, t in labels.items():
        s.append(text(X(i), Y + 36, t, 17))
    s.append("<circle cx='%.1f' cy='%d' r='8' fill='%s'/>" % (X(dot), Y, RED))
    return svg_wrap(W, Y + 46, "".join(s), "number line from %s split into %d equal parts" % (what, parts))


# ============================================================ set 1: fractions and decimals, repeating decimals
def set_fraction_decimal():
    its = []

    def f2d(v, right, wrong, e, q=None, fg=""):
        if "…" in right:
            assert right == dots(v), (v, right)
        else:
            assert D(right) == F(v), (v, right)
        its.append(mcq(fg + (q or "Write %s as a decimal." % fr(v.numerator, v.denominator)), right, wrong, e))

    f2d(F(1, 4), "0.25", ["0.14", "0.4", "4"],
        "%s = %s (multiply the top and bottom by 25) = <b>0.25</b>. 0.4 uses the denominator as tenths, "
        "and 4 is 4 ÷ 1, the wrong way round." % (fr(1, 4), fr(25, 100)))
    f2d(F(3, 5), "0.6", ["0.35", "0.53", "1.6"],
        "%s = %s (multiply the top and bottom by 2) = <b>0.6</b>. 0.35 just writes the digits 3 and 5 after the point."
        % (fr(3, 5), fr(6, 10)))
    f2d(F(1, 8), "0.125", ["0.8", "0.18", "0.12"],
        "1 ÷ 8: write 1 as 1.000. 10 ÷ 8 = 1 R 2, 20 ÷ 8 = 2 R 4, 40 ÷ 8 = 5. So %s = <b>0.125</b>. "
        "0.8 uses the denominator as the decimal, and 0.12 stops before the remainder is 0." % fr(1, 8))
    f2d(F(7, 20), "0.35", ["0.7", "0.72", "3.5"],
        "20 × 5 = 100, so multiply the top by 5 too: %s = %s = <b>0.35</b>. 0.7 would be %s, 0.72 just writes the digits, and 3.5 is 7 ÷ 2, which drops the 0 in 20."
        % (fr(7, 20), fr(35, 100), fr(7, 10)))
    f2d(F(9, 25), "0.36", ["0.925", "0.09", "0.34"],
        "25 × 4 = 100, so %s = %s = <b>0.36</b>. 0.09 forgets to multiply the top by 4, and 0.34 adds 9 + 25."
        % (fr(9, 25), fr(36, 100)))
    f2d(F(1, 3), dots(F(1, 3)), ["0.3", "0.13", "0.33"],
        "1 ÷ 3 = 0.333… The remainder is always 1, so the 3s never stop. It is written <b>0.333…</b> or %s "
        "(a bar over the digit that repeats). 0.33 stops too early, so it is a little less than %s." % (bart(F(1, 3)), fr(1, 3)))
    f2d(F(2, 3), dots(F(2, 3)), ["0.23", "0.6", "1.5"],
        "2 ÷ 3: 20 ÷ 3 = 6 R 2, and the remainder 2 comes back every time. So %s = <b>0.666…</b> = %s. "
        "1.5 is 3 ÷ 2, the wrong way round." % (fr(2, 3), bart(F(2, 3))))
    f2d(F(4, 9), dots(F(4, 9)), ["0.49", "0.4", "2.25"],
        "40 ÷ 9 = 4 R 4, and the remainder 4 comes back every time. So %s = <b>0.444…</b> = %s. "
        "2.25 is 9 ÷ 4, the wrong way round." % (fr(4, 9), bart(F(4, 9))))
    f2d(F(1, 6), dots(F(1, 6)), ["0.16", "0.161616…", "0.6"],
        "10 ÷ 6 = 1 R 4, then 40 ÷ 6 = 6 R 4, and the remainder 4 keeps coming back. Only the 6 repeats: "
        "%s = <b>0.1666…</b> = %s. 0.161616… repeats the 1 as well, but the 1 appears only once." % (fr(1, 6), bart(F(1, 6))),
        q="The division shows 1 ÷ 6. The remainder keeps coming back. What is %s as a decimal?" % fr(1, 6),
        fg=fig(rdiv(1, 6, 4, hide=True)))
    f2d(F(5, 11), dots(F(5, 11)), ["0.511", "2.2", "0.4545"],
        "50 ÷ 11 = 4 R 6, 60 ÷ 11 = 5 R 5, then 50 ÷ 11 again. The two digits 4 and 5 repeat: %s = <b>0.454545…</b> = %s. "
        "0.4545 stops, and 2.2 is 11 ÷ 5." % (fr(5, 11), bart(F(5, 11))),
        q="The division shows 5 ÷ 11. What is %s as a decimal?" % fr(5, 11), fg=fig(rdiv(5, 11, 4, hide=True)))
    f2d(F(7, 12), dots(F(7, 12)), ["0.712", "0.583", "0.585858…"],
        "70 ÷ 12 = 5 R 10, 100 ÷ 12 = 8 R 4, 40 ÷ 12 = 3 R 4, and the remainder 4 keeps coming back. "
        "So %s = <b>0.58333…</b> = %s. Only the 3 repeats. 0.583 stops too early." % (fr(7, 12), bart(F(7, 12))))
    f2d(F(23, 6), dots(F(23, 6)), ["3.56", "3.8", "0.8333…"],
        "The 3 wholes stay. %s = 5 ÷ 6 = 0.8333…, so %s = <b>3.8333…</b> = %s. 0.8333… forgets the 3 wholes."
        % (fr(5, 6), mixed(3, 5, 6), bart(F(23, 6))), q="Write %s as a decimal." % mixed(3, 5, 6))
    its.append(mcq("In the repeating decimal 0.4%s, which digits repeat?" % bar("3"),
                   "Only the 3", ["The 4 and the 3", "Only the 4", "No digits repeat"],
                   "The bar is only over the 3, so 0.4%s = <b>0.4333…</b>, and the 4 is written once. "
                   "0.%s would be 0.434343…" % (bar("3"), bar("43")), same_ok=True))
    its.append(mcq("Which fraction is a <b>repeating</b> decimal?", fr(2, 9), [fr(3, 8), fr(7, 20), fr(4, 5)],
                   "%s = 2 ÷ 9 = 0.222… The 2s never stop. The others end: %s = 0.375, %s = 0.35 and %s = 0.8. "
                   "In simplest form, a fraction ends as a decimal only when the denominator has no prime factors except 2 and 5."
                   % (fr(2, 9), fr(3, 8), fr(7, 20), fr(4, 5))))
    assert period(F(2, 9))[2] and not any(period(v)[2] for v in (F(3, 8), F(7, 20), F(4, 5)))
    its.append(mcq("Which fraction is a <b>terminating</b> decimal (it ends)?", fr(3, 16), [fr(1, 3), fr(5, 6), fr(4, 7)],
                   "16 = 2 × 2 × 2 × 2, so %s ends: 3 ÷ 16 = <b>0.1875</b>. %s, %s and %s have a factor of 3 or 7 in the denominator, "
                   "so they repeat." % (fr(3, 16), fr(1, 3), fr(5, 6), fr(4, 7))))
    assert not period(F(3, 16))[2] and all(period(v)[2] for v in (F(1, 3), F(5, 6), F(4, 7)))

    def d2f(stem, right, wrong, e, v):
        its.append(mcq("Write <b>%s</b> as a fraction in simplest form." % stem, right, wrong, e, value=v))

    assert D("0.45") == F(9, 20)
    d2f("0.45", fr(9, 20), [fr(45, 10), fr(4, 5), fr(1, 45)],
        "0.45 = 45 hundredths = %s. Divide the top and bottom by 5: <b>%s</b>. %s would be 4.5."
        % (fr(45, 100), fr(9, 20), fr(45, 10)), F(9, 20))
    assert D("0.125") == F(1, 8)
    d2f("0.125", fr(1, 8), [fr(125, 100), fr(1, 125), fr(1, 12)],
        "0.125 has three decimal places, so it is %s. Divide the top and bottom by 125: <b>%s</b>. "
        "%s would be 1.25." % (fr(125, 1000), fr(1, 8), fr(125, 100)), F(1, 8))
    assert bart(F(1, 9)) == "0." + bar("1")
    its.append(mcq("Which fraction is equal to 0.%s?" % bar("1"), fr(1, 9), [fr(1, 10), fr(1, 11), fr(11, 100)],
                   "1 ÷ 9 = 0.111… = 0.%s, so the answer is <b>%s</b>. %s is 0.1, which stops, and %s = 0.090909…"
                   % (bar("1"), fr(1, 9), fr(1, 10), fr(1, 11)), value=F(1, 9)))
    assert bart(F(2, 3)) == "0." + bar("6")
    its.append(mcq("Which fraction is equal to 0.%s?" % bar("6"), fr(2, 3), [fr(6, 10), fr(1, 6), fr(6, 100)],
                   "2 ÷ 3 = 0.666… = 0.%s, so the answer is <b>%s</b>. %s = 0.6 ends after one 6. %s = 0.1666…"
                   % (bar("6"), fr(2, 3), fr(6, 10), fr(1, 6)), value=F(2, 3)))
    assert bart(F(5, 11)) == "0." + bar("45")
    its.append(mcq("Which fraction is equal to 0.%s? Divide to check." % bar("45"), fr(5, 11), [fr(9, 20), fr(4, 9), fr(1, 45)],
                   "5 ÷ 11 = 0.454545… = 0.%s, so the answer is <b>%s</b>. %s = 0.45 stops, and %s = 0.444…"
                   % (bar("45"), fr(5, 11), fr(9, 20), fr(4, 9)), value=F(5, 11)))
    # easy terminating first, then repeating, then decimals to fractions
    order = [0, 1, 2, 3, 4, 15, 16, 5, 6, 7, 13, 14, 12, 8, 10, 9, 17, 18, 11, 19]
    its = [its[i] for i in order]
    assert len(its) == 20 and len(set(order)) == 20
    return {"title": "Fractions and decimals, including repeating decimals", "items": its}


# ============================================================ set 2: decimals and percents
def set_decimal_percent():
    its = []
    for d_, wrong, e in [
        ("0.4", ["4%", "0.4%", "400%"],
         "Multiply by 100: 0.4 × 100 = 40, so 0.4 = <b>40%</b>. 4% would be 0.04."),
        ("0.07", ["70%", "0.07%", "0.7%"],
         "0.07 × 100 = 7, so 0.07 = <b>7%</b>. 70% would be 0.7."),
        ("0.125", ["125%", "1.25%", "0.125%"],
         "0.125 × 100 = 12.5, so 0.125 = <b>12.5%</b>. A percent can have a decimal in it. 125% would be 1.25."),
        ("0.875", ["875%", "8.75%", "0.875%"],
         "0.875 × 100 = 87.5, so 0.875 = <b>87.5%</b>. Move the decimal point 2 places to the right."),
        ("0.035", ["35%", "0.35%", "350%"],
         "0.035 × 100 = 3.5, so 0.035 = <b>3.5%</b>. 35% would be 0.35."),
        ("1.5", ["15%", "1.5%", "105%"],
         "1.5 × 100 = 150, so 1.5 = <b>150%</b>. More than 1 whole is more than 100%. 105% would be 1.05."),
        ("2.3", ["23%", "2.3%", "203%"],
         "2.3 × 100 = 230, so 2.3 = <b>230%</b>. 203% would be 2.03."),
        ("1", ["1%", "10%", "0.1%"],
         "1 × 100 = 100, so 1 = <b>100%</b>, one whole. 1% would be 0.01."),
    ]:
        right = pct(D(d_))
        its.append(mcq("Write <b>%s</b> as a percent." % d_, right, wrong, e))
    for p_, wrong, e in [
        ("36%", ["3.6", "0.036", "36"],
         "Divide by 100: 36 ÷ 100 = <b>0.36</b>. Move the decimal point 2 places to the left."),
        ("5%", ["0.5", "5", "0.005"],
         "5% = 5 hundredths. Hundredths are the second place after the point: <b>0.05</b>. 0.5 is 50%."),
        ("12.5%", ["1.25", "0.0125", "12.5"],
         "12.5 ÷ 100 = <b>0.125</b>. 1.25 moves the point only one place, and 1.25 is 125%."),
        ("140%", ["0.14", "14", "0.4"],
         "140 ÷ 100 = <b>1.4</b>. 140% is more than 100%, so the decimal must be more than 1. 0.14 is only 14%."),
        ("250%", ["0.25", "25", "0.025"],
         "250 ÷ 100 = <b>2.5</b>. 250% is 2 wholes and a half. 0.25 is only 25%."),
        ("0.5%", ["0.5", "0.05", "5"],
         "0.5 ÷ 100 = <b>0.005</b>. 0.5% is half of 1%, and 1% = 0.01. 0.5 would be 50%."),
    ]:
        right = dec(F(Dm(p_.rstrip("%"))) / 100)
        its.append(mcq("Write <b>%s</b> as a decimal." % p_, right, wrong, e))
    its.append(mcq(fig(grids_svg([100, 35])) + "Each hundred grid is one whole. What percent is shaded?",
                   "135%", ["35%", "13.5%", "65%"],
                   "One whole grid is 100%, and 35 squares of the next grid is 35%. 100% + 35% = <b>135%</b> = 1.35. "
                   "35% forgets the full grid, and 65% counts the white squares."))
    its.append(mcq(fig(grids_svg([8])) + "Which shows the shaded part as a decimal and a percent?",
                   "0.08 and 8%", ["0.8 and 80%", "0.8 and 8%", "0.08 and 80%"],
                   "8 of 100 squares = 8 hundredths = <b>0.08</b> = <b>8%</b>. 0.8 would be 80 squares.", same_ok=True))
    its.append(mcq("Which decimal is <b>more than 100%</b>?", "1.05", ["0.99", "0.105", "0.5"],
                   "100% = 1. Only <b>1.05</b> is more than 1: 1.05 = 105%. 0.99 = 99%, 0.105 = 10.5% and 0.5 = 50%."))
    its.append(mcq("Which is <b>not</b> equal to 1.2?", "12%", ["120%", "1.20", fr(6, 5)],
                   "1.2 = 1.20 = 120%% = %s. <b>12%%</b> is 0.12, only one tenth as much." % fr(6, 5), same_ok=True))
    its.append(mcq("Write <b>3.75</b> as a percent.", "375%", ["37.5%", "3.75%", "0.375%"],
                   "3.75 × 100 = 375, so 3.75 = <b>375%</b>. 37.5% moves the point only one place."))
    its.append(mcq("Write <b>0.%s</b> as a percent." % bar("3"), "33.3…%", ["3.3%", "0.33%", "333%"],
                   "0.%s = 0.333… Multiply by 100: <b>33.3…%%</b>, also written 33%s%%. "
                   "The 3s after the point keep going." % (bar("3"), fr(1, 3))))
    # easy -> hard
    order = [0, 1, 8, 9, 15, 7, 5, 6, 11, 12, 2, 10, 3, 4, 13, 14, 16, 17, 18, 19]
    its = [its[i] for i in order]
    assert len(its) == 20 and len(set(order)) == 20
    return {"title": "Decimals and percents, including 12.5% and over 100%", "items": its}


# ============================================================ set 3: fractions and percents
def set_fraction_percent():
    its = []

    def f2p(v, wrong, e, q=None, fg=""):
        right = pct(v)
        its.append(mcq(fg + (q or "Write %s as a percent." % fr(v.numerator, v.denominator)), right, wrong, e))

    f2p(F(1, 4), ["14%", "4%", "40%"],
        "%s = %s = <b>25%%</b>. 14%% just writes the digits, and 40%% uses the denominator as tenths." % (fr(1, 4), fr(25, 100)))
    f2p(F(3, 5), ["35%", "30%", "53%"],
        "%s = %s = <b>60%%</b>. 35%% just writes the digits 3 and 5." % (fr(3, 5), fr(60, 100)))
    f2p(F(7, 10), ["7%", "0.7%", "30%"],
        "%s = %s = <b>70%%</b>. 7%% would be %s, and 30%% is the part that is left." % (fr(7, 10), fr(70, 100), fr(7, 100)))
    f2p(F(9, 20), ["9%", "55%", "0.45%"],
        "20 × 5 = 100, so %s = %s = <b>45%%</b>. 55%% is the other part, %s." % (fr(9, 20), fr(45, 100), fr(11, 20)))
    f2p(F(1, 8), ["8%", "18%", "80%"],
        "%s = 1 ÷ 8 = 0.125 = <b>12.5%%</b>. 80%% comes from the mistake %s = 0.8." % (fr(1, 8), fr(1, 8)))
    f2p(F(5, 8), ["58%", "5.8%", "6.25%"],
        "%s = 5 ÷ 8 = 0.625. Multiply by 100: <b>62.5%%</b>. 58%% just writes the digits, and 6.25%% moves the point only one place."
        % fr(5, 8))
    its.append(mcq("Write %s as a percent." % fr(1, 3), "33.3…%", ["3%", "13%", "30%"],
                   "%s = 1 ÷ 3 = 0.333… Multiply by 100: <b>33.3…%%</b>, also written 33%s%%. "
                   "30%% would be %s." % (fr(1, 3), fr(1, 3), fr(3, 10))))
    assert dots(F(1, 3)) == "0.333…"
    its.append(mcq("Write %s as a percent." % fr(2, 3), "66.6…%", ["23%", "66%", "150%"],
                   "%s = 2 ÷ 3 = 0.666… Multiply by 100: <b>66.6…%%</b>, also written 66%s%%. "
                   "66%% stops too early, and 150%% is %s." % (fr(2, 3), fr(2, 3), fr(3, 2))))
    assert dots(F(2, 3)) == "0.666…"
    f2p(F(5, 4), ["54%", "1.25%", "80%"],
        "%s = 5 ÷ 4 = 1.25 = <b>125%%</b>. The fraction is more than 1, so the percent is more than 100%%. 80%% is %s."
        % (fr(5, 4), fr(4, 5)))
    its.append(mcq("Write %s as a percent." % mixed(1, 3, 5), "160%", ["135%", "60%", "16%"],
                   "1 whole = 100%% and %s = 60%%. 100%% + 60%% = <b>160%%</b>. 60%% forgets the whole, "
                   "and 135%% just writes the digits." % fr(3, 5)))
    assert pct(F(8, 5)) == "160%"

    def p2f(p_, right, wrong, e, v):
        assert F(Dm(p_.rstrip("%"))) / 100 == v
        its.append(mcq("Write <b>%s</b> as a fraction in simplest form." % p_, right, wrong, e, value=v))

    p2f("40%", fr(2, 5), [fr(1, 40), fr(4, 100), fr(4, 5)],
        "40%% = %s. Divide the top and bottom by 20: <b>%s</b>. %s is 4%%, not 40%%." % (fr(40, 100), fr(2, 5), fr(4, 100)), F(2, 5))
    p2f("15%", fr(3, 20), [fr(1, 15), fr(3, 2), fr(3, 10)],
        "15%% = %s. Divide the top and bottom by 5: <b>%s</b>. %s would be 150%%." % (fr(15, 100), fr(3, 20), fr(3, 2)), F(3, 20))
    p2f("12.5%", fr(1, 8), [fr(1, 12), fr(125, 100), fr(1, 125)],
        "12.5%% = 0.125 = %s. Divide the top and bottom by 125: <b>%s</b>. %s is 125%%." % (fr(125, 1000), fr(1, 8), fr(125, 100)),
        F(1, 8))
    p2f("175%", mixed(1, 3, 4), [fr(3, 4), mixed(1, 7, 10), fr(1, 75)],
        "175%% = 100%% + 75%% = 1 + %s = <b>%s</b>. %s forgets the whole, and %s is 170%%."
        % (fr(3, 4), mixed(1, 3, 4), fr(3, 4), mixed(1, 7, 10)), F(7, 4))
    p2f("0.5%", fr(1, 200), [fr(1, 2), fr(1, 5), fr(1, 50)],
        "0.5%% = %s. Multiply the top and bottom by 2 to get rid of the decimal: <b>%s</b>. %s is 50%%, not 0.5%%."
        % (fr("0.5", 100), fr(1, 200), fr(1, 2)), F(1, 200))
    its.append(mcq("Which fraction is equal to 85%?", fr(17, 20), [fr(8, 5), fr(1, 85), fr(3, 20)],
                   "85%% = %s. Divide the top and bottom by 5: <b>%s</b>. %s is 15%%, the part that is left."
                   % (fr(85, 100), fr(17, 20), fr(3, 20)), value=F(17, 20)))
    its.append(mcq("Which is <b>not</b> equal to 75%?", fr(7, 5), [fr(3, 4), "0.75", fr(75, 100)],
                   "75%% = %s = %s = 0.75. <b>%s</b> just writes the digits 7 and 5; it is 140%%."
                   % (fr(75, 100), fr(3, 4), fr(7, 5)), same_ok=True))
    its.append(mcq("Which fraction is equal to %s%%?" % mixed(33, 1, 3), fr(1, 3), [fr(1, 33), fr(3, 10), fr(33, 10)],
                   "%s%% = 33.3…%% = 0.333… = <b>%s</b>. %s is 30%%, and %s is 330%%."
                   % (mixed(33, 1, 3), fr(1, 3), fr(3, 10), fr(33, 10)), value=F(1, 3)))
    f2p(F(3, 8), ["3.8%", "30%", "62.5%"],
        "3 of 8 equal parts are shaded: %s = 3 ÷ 8 = 0.375 = <b>37.5%%</b>. 62.5%% is the white part." % fr(3, 8),
        q="What percent of the bar is shaded?", fg=fig(bar_svg(8, 3)))
    its.append(mcq(fig(line_svg(8, 5, {0: "0%", 4: "100%", 8: "200%"}, what="0% to 200%")) +
                   "The line from 0% to 200% is split into 8 equal parts. What percent is at the red dot?",
                   "125%", ["5%", "50%", "62.5%"],
                   "100%% is 4 parts, so each part is 25%%. The dot is 5 parts along: 5 × 25%% = <b>125%%</b> = %s. "
                   "62.5%% treats the whole line as 100%%." % mixed(1, 1, 4), value=F(5, 4)))
    order = [0, 1, 2, 3, 10, 11, 4, 5, 18, 12, 6, 7, 17, 15, 8, 9, 13, 19, 14, 16]
    its = [its[i] for i in order]
    assert len(its) == 20 and len(set(order)) == 20
    return {"title": "Fractions and percents", "items": its}


# ============================================================ set 4: compare and order
def cmp_item(x, xv, y, yv, e):
    lt, gt, eq = "%s &lt; %s" % (x, y), "%s &gt; %s" % (x, y), "%s = %s" % (x, y)
    right = lt if xv < yv else gt if xv > yv else eq
    wrong = [c for c in (lt, gt, eq) if c != right] + ["You can’t tell"]
    return mcq("Compare <b>%s</b> and <b>%s</b>." % (x, y), right, wrong, e, same_ok=True)


def set_compare():
    its = []
    its.append(cmp_item("0.4", D("0.4"), "4%", F(4, 100),
                        "4% = 0.04. 0.40 &gt; 0.04, so <b>0.4 &gt; 4%</b>. 0.4 is 40%, not 4%."))
    its.append(cmp_item(fr(1, 8), F(1, 8), "0.8", D("0.8"),
                        "%s = 1 ÷ 8 = 0.125. 0.125 &lt; 0.800, so <b>%s &lt; 0.8</b>." % (fr(1, 8), fr(1, 8))))
    its.append(cmp_item(fr(3, 5), F(3, 5), "0.35", D("0.35"),
                        "%s = %s = 0.6 = 0.60. 0.60 &gt; 0.35, so <b>%s &gt; 0.35</b>." % (fr(3, 5), fr(6, 10), fr(3, 5))))
    its.append(cmp_item("12.5%", F(1, 8), fr(1, 8), F(1, 8),
                        "12.5%% = 0.125, and %s = 1 ÷ 8 = 0.125. So <b>12.5%% = %s</b>." % (fr(1, 8), fr(1, 8))))
    its.append(cmp_item("150%", F(3, 2), "1.05", D("1.05"),
                        "150% = 1.50. 1.50 &gt; 1.05, so <b>150% &gt; 1.05</b>. 1.05 is only 105%."))
    its.append(cmp_item("0." + bar("3"), F(1, 3), "0.33", D("0.33"),
                        "0.%s = 0.333… and 0.33 = 0.330. The third place is 3 &gt; 0, so <b>0.%s &gt; 0.33</b>."
                        % (bar("3"), bar("3"))))
    its.append(cmp_item(fr(2, 3), F(2, 3), "0.67", D("0.67"),
                        "%s = 2 ÷ 3 = 0.666… and 0.67 = 0.670. Compare the hundredths: 6 &lt; 7. "
                        "So <b>%s &lt; 0.67</b>." % (fr(2, 3), fr(2, 3))))
    its.append(cmp_item(fr(5, 6), F(5, 6), "0.83", D("0.83"),
                        "%s = 5 ÷ 6 = 0.8333… and 0.83 = 0.830. The third place is 3 &gt; 0, so <b>%s &gt; 0.83</b>."
                        % (fr(5, 6), fr(5, 6))))
    its.append(cmp_item(fr(3, 7), F(3, 7), "0.43", D("0.43"),
                        "%s = 3 ÷ 7 = 0.4285… and 0.43 = 0.4300. Compare the hundredths: 2 &lt; 3. "
                        "So <b>%s &lt; 0.43</b>." % (fr(3, 7), fr(3, 7))))
    assert dots(F(3, 7), 1).startswith("0.4285")
    a_, b_ = "0.4" + bar("5"), "0." + bar("45")
    assert bart(F(41, 90)) == a_ and bart(F(5, 11)) == b_
    its.append(cmp_item(a_, F(41, 90), b_, F(5, 11),
                        "Write out the digits: %s = 0.4555… and %s = 0.4545… The third place is 5 &gt; 4, so <b>%s &gt; %s</b>."
                        % (a_, b_, a_, b_)))

    def order_q(q, vals, asc, wrongs, e):
        s = sorted(vals, key=lambda t: t[1], reverse=not asc)
        assert len(set(v for _, v in vals)) == len(vals)
        right = ", ".join(h for h, _ in s)
        for w in wrongs:
            assert sorted(w) == sorted(h for h, _ in vals)
        return mcq(q, right, [", ".join(w) for w in wrongs], e, same_ok=True)

    its.append(order_q("Order from <b>least to greatest</b>:<br><b>0.3, %s, 0.33, 30.5%%</b>" % fr(1, 3),
                       [("0.3", D("0.3")), (fr(1, 3), F(1, 3)), ("0.33", D("0.33")), ("30.5%", D("0.305"))], True,
                       [["0.3", "0.33", fr(1, 3), "30.5%"], ["30.5%", "0.3", "0.33", fr(1, 3)], ["0.3", fr(1, 3), "0.33", "30.5%"]],
                       "As decimals with 3 places: 0.300, %s = 0.333…, 0.330, 30.5%% = 0.305. "
                       "So <b>0.3, 30.5%%, 0.33, %s</b>." % (fr(1, 3), fr(1, 3))))
    its.append(order_q("Order from <b>greatest to least</b>:<br><b>1.2, 115%%, %s, 1.02</b>" % mixed(1, 1, 4),
                       [("1.2", D("1.2")), ("115%", D("1.15")), (mixed(1, 1, 4), F(5, 4)), ("1.02", D("1.02"))], False,
                       [["1.2", mixed(1, 1, 4), "115%", "1.02"], ["115%", mixed(1, 1, 4), "1.2", "1.02"],
                        [mixed(1, 1, 4), "1.2", "1.02", "115%"]],
                       "As decimals: 1.20, 115%% = 1.15, %s = 1.25, 1.02. Greatest first: <b>%s, 1.2, 115%%, 1.02</b>."
                       % (mixed(1, 1, 4), mixed(1, 1, 4))))
    six = "0." + bar("6")
    its.append(order_q("Order from <b>least to greatest</b>:<br><b>%s, 0.6, 62%%, %s</b>" % (fr(5, 8), six),
                       [(fr(5, 8), F(5, 8)), ("0.6", D("0.6")), ("62%", D("0.62")), (six, F(2, 3))], True,
                       [[six, "0.6", "62%", fr(5, 8)], ["0.6", fr(5, 8), "62%", six], ["0.6", "62%", six, fr(5, 8)]],
                       "As decimals: %s = 0.625, 0.600, 62%% = 0.620, %s = 0.666… "
                       "So <b>0.6, 62%%, %s, %s</b>." % (fr(5, 8), six, fr(5, 8), six)))
    its.append(order_q("Which list is in order from <b>least to greatest</b>?",
                       [(fr(2, 5), F(2, 5)), ("0.45", D("0.45")), (fr(4, 9), F(4, 9)), ("46%", D("0.46"))], True,
                       [[fr(2, 5), "0.45", fr(4, 9), "46%"], [fr(4, 9), fr(2, 5), "0.45", "46%"], ["46%", "0.45", fr(4, 9), fr(2, 5)]],
                       "As decimals: %s = 0.400, %s = 0.444…, 0.450, 46%% = 0.460. "
                       "So <b>%s, %s, 0.45, 46%%</b>." % (fr(2, 5), fr(4, 9), fr(2, 5), fr(4, 9))))
    eight = "0." + bar("8")
    assert bart(F(8, 9)) == eight
    its.append(mcq("Which is the <b>greatest</b>?", eight, [fr(7, 8), "0.85", "86%"],
                   "As decimals: %s = 0.888…, %s = 0.875, 0.850, 86%% = 0.860. The greatest is <b>%s</b>."
                   % (eight, fr(7, 8), eight)))
    assert F(1, 12) < D("0.085") < D("0.09") < D("0.1")
    its.append(mcq("Which is the <b>least</b>?", fr(1, 12), ["0.09", "8.5%", "0.1"],
                   "As decimals: %s = 1 ÷ 12 = 0.0833…, 0.090, 8.5%% = 0.085, 0.100. The least is <b>%s</b>."
                   % (fr(1, 12), fr(1, 12))))
    assert D("0.4") < F(4, 9) < D("0.5") and not D("0.4") < F(3, 8) < D("0.5")
    its.append(mcq("Which number is between 0.4 and 0.5?", fr(4, 9), ["0.04", fr(3, 8), "51%"],
                   "%s = 4 ÷ 9 = 0.444…, which is between 0.4 and 0.5. 0.04 is far less, %s = 0.375 and 51%% = 0.51."
                   % (fr(4, 9), fr(3, 8))))
    its.append(mcq(fig(line_svg(6, 5, {0: "0", 6: "1"})) +
                   "The line from 0 to 1 is split into 6 equal parts. What decimal is at the red dot?",
                   dots(F(5, 6)), ["0.5", "0.56", "0.83"],
                   "Each part is %s. The dot is 5 parts along: %s = 5 ÷ 6 = <b>0.8333…</b> = %s. "
                   "0.5 counts the parts as tenths, and 0.83 is close but stops; the 3s keep going." % (fr(1, 6), fr(5, 6), bart(F(5, 6)))))
    one6 = "1." + bar("6")
    assert bart(F(5, 3)) == one6
    its.append(mcq("Which is the <b>greatest</b>?", one6, ["1.66", mixed(1, 5, 8), "160.5%"],
                   "As decimals: %s = 1.666…, 1.660, %s = 1.625, 160.5%% = 1.605. The greatest is <b>%s</b>. "
                   "1.66 stops, so it is a little less than 1.666…" % (one6, mixed(1, 5, 8), one6)))
    its.append(mcq("Which statement is <b>true</b>?", "0.%s = %s" % (bar("3"), fr(1, 3)),
                   ["0.33 = %s" % fr(1, 3), "%s = 0.8" % fr(1, 8), "0.4 = 4%"],
                   "%s = 1 ÷ 3 = 0.333… = <b>0.%s</b>. The others are common mistakes: 0.33 stops too early, "
                   "%s = 0.125, and 0.4 = 40%%." % (fr(1, 3), bar("3"), fr(1, 8)), same_ok=True))
    order = [0, 1, 2, 3, 4, 5, 6, 7, 8, 14, 15, 16, 10, 13, 11, 12, 17, 9, 18, 19]
    its = [its[i] for i in order]
    assert len(its) == 20 and len(set(order)) == 20
    return {"title": "Compare and order fractions, decimals and percents", "items": its}


# ============================================================ set 5: word problems
def set_problems(P):
    its = []
    n, he, his = P.next()
    its.append(mcq("%s scores 42 out of 50 on a science test. What percent does %s score?" % (n, he),
                   "84%", ["42%", "16%", "8.4%"],
                   "%s = %s (multiply the top and bottom by 2) = <b>84%%</b>. 16%% is the part %s got wrong."
                   % (fr(42, 50), fr(84, 100), he)))
    assert F(42, 50) == F(84, 100)
    its.append(mcq("A Surrey soccer team has 9 wins and 3 losses, with no ties. What percent of its games did it win?",
                   "75%", ["25%", "93%", "300%"],
                   "It played 9 + 3 = 12 games. %s = %s = <b>75%%</b>. 300%% divides 9 by 3, the losses, "
                   "instead of by all 12 games." % (fr(9, 12), fr(3, 4))))
    its.append(mcq("A Kamloops lacrosse team won 15 of its 24 games. What percent of its games did it win?",
                   pct(F(15, 24)), ["15%", "37.5%", "160%"],
                   "%s = %s (divide by 3) = 5 ÷ 8 = 0.625 = <b>62.5%%</b>. 37.5%% is the games it did not win, "
                   "and 160%% is 24 ÷ 15, the wrong way round." % (fr(15, 24), fr(5, 8))))
    assert int(F(2, 3) * 1000 + F(1, 2)) == 667
    its.append(mcq("A hockey team in Prince George won %s of its games. Win records are often written as a decimal "
                   "to 3 places. What is its win record?" % fr(2, 3), "0.667", ["0.666", "0.23", "1.5"],
                   "%s = 2 ÷ 3 = 0.6666… The 4th place is 6, so round up: <b>0.667</b>. "
                   "0.666 cuts the digits off without rounding." % fr(2, 3)))
    a, ah, _ = P.next()
    b, bh, _ = P.next()
    its.append(mcq("On a math test, %s scores 17 out of 20. %s gets 0.84 of the marks on the same test. Who has the higher score?" % (a, b),
                   a, [b, "They are the same", "You can’t tell"],
                   "%s = %s = 85%% = 0.85. 0.85 &gt; 0.84, so <b>%s</b> has the higher score." % (fr(17, 20), fr(85, 100), a)))
    n, he, his = P.next()
    its.append(mcq("%s gets 7 out of 8 questions right on a quiz. What percent is that?" % n,
                   pct(F(7, 8)), ["78%", "8.75%", "12.5%"],
                   "%s = 7 ÷ 8 = 0.875 = <b>87.5%%</b>. 12.5%% is the part %s got wrong, and 78%% just writes the digits."
                   % (fr(7, 8), he)))
    its.append(mcq("In a Grade 7 class of 30 students, 12 take the bus to school. What percent take the bus?",
                   "40%", ["12%", "60%", "2.5%"],
                   "%s = %s (divide by 3) = <b>40%%</b>. 60%% is the students who do not take the bus, "
                   "and 2.5%% comes from 30 ÷ 12." % (fr(12, 30), fr(4, 10))))
    its.append(mcq("A school raised 1.25 times as much in this year’s Terry Fox Run as last year. "
                   "What percent of last year’s amount is that?", "125%", ["25%", "12.5%", "1.25%"],
                   "1.25 × 100 = 125, so it is <b>125%</b> of last year’s amount. More than last year means more than 100%. "
                   "25% is only the extra part."))
    n, he, his = P.next()
    its.append(mcq("%s pours 2 L of water equally into 3 bottles for a hike near Whistler. How much water is in each bottle?" % n,
                   dots(F(2, 3)) + " L", ["1.5 L", "0.23 L", "0.6 L"],
                   "2 ÷ 3 = %s L = <b>0.666… L</b> = %s L, a little less than 0.7 L. 1.5 L is 3 ÷ 2, the wrong way round."
                   % (fr(2, 3), bart(F(2, 3)))))
    n, he, his = P.next()
    its.append(mcq("A quiz has 30 questions. %s gets 0.%s of them right. How many questions does %s get right?"
                   % (n, bar("6"), he), "20", ["18", "6", "10"],
                   "0.%s = %s. %s of 30 = 30 ÷ 3 × 2 = <b>20</b>. 18 uses 0.6 instead of 0.666…, and 10 is the number %s gets wrong."
                   % (bar("6"), fr(2, 3), fr(2, 3), he)))
    assert F(2, 3) * 30 == 20
    a, _, _ = P.next()
    b, _, _ = P.next()
    c, _, _ = P.next()
    vals = sorted([(a, D("0.82")), (b, F(4, 5)), (c, D("0.83"))], key=lambda t: -t[1])
    right = ", ".join(x for x, _ in vals)
    its.append(mcq("On a reading test, %s gets 0.82 of the marks, %s gets %s and %s gets 83%%. "
                   "Order them from <b>highest to lowest</b> score." % (a, b, fr(4, 5), c),
                   right, [", ".join([b, c, a]), ", ".join([a, c, b]), ", ".join([b, a, c])],
                   "As decimals: 0.82, %s = 0.80, 83%% = 0.83. Highest first: <b>%s</b>." % (fr(4, 5), right), same_ok=True))
    assert right == ", ".join([c, a, b])
    assert F(5, 8) > D("0.61") > D("0.6")
    its.append(mcq("Three soccer teams compare win records. The Kelowna team won %s of its games, the Nanaimo team won 0.6, "
                   "and the Burnaby team won 61%%. Which team has the best record?" % fr(5, 8),
                   "Kelowna", ["Nanaimo", "Burnaby", "They are all the same"],
                   "As decimals: %s = 0.625, 0.600 and 61%% = 0.610. 0.625 is the greatest, so <b>Kelowna</b> has the best record."
                   % fr(5, 8)))
    its.append(mcq("One November, it rained on 18 of the 30 days in Vancouver. On what percent of the days did it rain?",
                   "60%", ["18%", "40%", "1.8%"],
                   "%s = %s (divide by 3) = <b>60%%</b>. 40%% is the days with no rain." % (fr(18, 30), fr(6, 10))))
    its.append(mcq("A bike shop in Victoria sells a bike for 140% of what the shop paid for it. "
                   "Write 140% as a decimal.", "1.4", ["0.14", "14", "0.4"],
                   "140 ÷ 100 = <b>1.4</b>. The shop sells the bike for 1.4 times what it paid. 0.14 is only 14%."))
    n, he, his = P.next()
    its.append(mcq("%s gets 1 of the 8 questions wrong on a quiz. What percent of the questions does %s get wrong?" % (n, he),
                   pct(F(1, 8)), ["8%", "18%", "87.5%"],
                   "%s = 1 ÷ 8 = 0.125 = <b>12.5%%</b>. 87.5%% is the part %s got right." % (fr(1, 8), he)))
    its.append(mcq("A lacrosse team won 60% of its 25 games. How many games did it win?",
                   "15", ["10", "60", "35"],
                   "60%% = %s. %s of 25 = 25 ÷ 5 × 3 = <b>15</b> games. 10 is the games it did not win, "
                   "and 35 is 60 − 25." % (fr(3, 5), fr(3, 5))))
    assert F(60, 100) * 25 == 15
    its.append(mcq("On a snowy day, %s of the runs at a ski hill on Grouse Mountain are open. What decimal is that?" % fr(5, 6),
                   dots(F(5, 6)), ["0.56", "0.6", "1.2"],
                   "5 ÷ 6: 50 ÷ 6 = 8 R 2, then 20 ÷ 6 = 3 R 2 again and again. So %s = <b>0.8333…</b> = %s. "
                   "1.2 is 6 ÷ 5, the wrong way round." % (fr(5, 6), bart(F(5, 6)))))
    a, ah, _ = P.next()
    b, bh, _ = P.next()
    assert D("0.67") > F(2, 3)
    its.append(mcq("%s scores %s of the marks on a test. %s scores 67%%. Who has the higher score?" % (a, fr(2, 3), b),
                   b, [a, "They are the same", "You can’t tell"],
                   "%s = 0.666… = 66.6…%%, and 67%% = 0.67. 0.670 &gt; 0.666…, so <b>%s</b> has the higher score, "
                   "but only just." % (fr(2, 3), b)))
    its.append(mcq("A class collects 150% of its goal of 200 cans for the food bank. How many cans does it collect?",
                   "300", ["150", "350", "30"],
                   "150% = 1.5. 1.5 × 200 = <b>300</b> cans. 350 adds 150 + 200, and 150 is only the percent."))
    assert D("1.5") * 200 == 300
    its.append(mcq("After 12 games, a hockey team has 7 wins, 3 losses and 2 ties. What percent of its games did it lose?",
                   "25%", ["3%", "30%", "75%"],
                   "%s = %s = <b>25%%</b>. 30%% uses 7 + 3 = 10 games instead of all 12, and 75%% is the games it did not lose."
                   % (fr(3, 12), fr(1, 4))))
    order = [0, 6, 12, 1, 5, 4, 7, 13, 2, 14, 8, 9, 16, 10, 11, 17, 3, 15, 18, 19]
    its = [its[i] for i in order]
    assert len(its) == 20 and len(set(order)) == 20
    return {"title": "Word problems: test scores and win records", "items": its}


# ============================================================ lesson
def body_html():
    f_div = rdiv(1, 3, 4)
    f_grids = grids_svg([100, 35])
    f_bar = bar_svg(8, 1)
    return (
        "<h2>One amount, three ways</h2>"
        "<p>A fraction, a decimal and a percent can name the same amount. A fraction is a division: "
        + fr(3, 4) + " means 3 ÷ 4 = 0.75. Percent means <b>out of 100</b>: 0.75 = 75%.</p>"
        "<figure class='sn-fig'>" + f_bar +
        "<figcaption>1 of 8 equal parts: " + fr(1, 8) + " = 1 ÷ 8 = 0.125 = 12.5%.</figcaption></figure>"
        + "<h2>Fractions to decimals</h2>"
        "<p>Divide the numerator by the denominator. If the remainder becomes 0, the decimal <b>terminates</b> (ends). "
        "If a remainder comes back, the digits repeat for ever. That is a <b>repeating decimal</b>.</p>"
        "<figure class='sn-fig'>" + f_div +
        "<figcaption>1 ÷ 3: the remainder is always 1, so the 3s never stop. " + fr(1, 3) + " = 0.333… = 0."
        + bar("3") + ".</figcaption></figure>"
        "<p>Write a repeating decimal with dots (0.333…) or with a <b>bar</b> over the digits that repeat. "
        "Put the bar only over the repeating part: " + fr(1, 6) + " = 0.1666… = 0.1" + bar("6") + ", and "
        + fr(5, 11) + " = 0.4545… = 0." + bar("45") + ".</p>"
        + ex("Example", "Write " + fr(7, 20) + " as a decimal.",
             "20 × 5 = 100, so multiply the top by 5 too: " + fr(7, 20) + " = " + fr(35, 100) + ".", "0.35")
        + ex("Repeating", "Write " + fr(2, 3) + " as a decimal.",
             "20 ÷ 3 = 6 R 2. The remainder 2 comes back every time, so the 6s never stop.", "0.666… = 0." + bar("6"))
        + "<h2>Decimals and percents</h2>"
        "<p>To change a decimal to a percent, multiply by 100 (move the point 2 places right). "
        "To change a percent to a decimal, divide by 100 (move the point 2 places left). "
        "A percent can have a decimal in it, like 12.5%, and it can be more than 100%.</p>"
        "<figure class='sn-fig'>" + f_grids +
        "<figcaption>Each grid is one whole. 1 whole and 35 hundredths: 1.35 = 135%.</figcaption></figure>"
        + table(["Fraction", "Decimal", "Percent"], [
            [fr(1, 2), "0.5", "50%"],
            [fr(1, 4), "0.25", "25%"],
            [fr(1, 8), "0.125", "12.5%"],
            [fr(1, 5), "0.2", "20%"],
            [fr(1, 3), "0.333… = 0." + bar("3"), "33.3…%"],
            [fr(2, 3), "0.666… = 0." + bar("6"), "66.6…%"],
            [mixed(1, 1, 2), "1.5", "150%"],
        ])
        + "<h2>Comparing and ordering</h2>"
        "<p>Change everything into decimals and write them with the same number of places. "
        "For a repeating decimal, write out enough digits to see the difference.</p>"
        + ex("Example", "Order 0.3, " + fr(1, 3) + ", 0.33 and 30.5% from least to greatest.",
             "0.300, " + fr(1, 3) + " = 0.333…, 0.330 and 30.5% = 0.305. Compare place by place.",
             "0.3, 30.5%, 0.33, " + fr(1, 3))
        + ex("Win record", "A team won 15 of its 24 games. What percent did it win?",
             fr(15, 24) + " = " + fr(5, 8) + " = 5 ÷ 8 = 0.625. Multiply by 100.", "62.5%")
        + "<h2>Common mistakes</h2>"
        + table(["Mistake", "What to do instead"], [
            ["0.4 = 4%", "0.4 = 0.40 = 40 hundredths = 40%"],
            [fr(1, 8) + " = 0.8", "Divide: 1 ÷ 8 = 0.125"],
            [fr(3, 5) + " = 0.35", "Divide: " + fr(3, 5) + " = " + fr(6, 10) + " = 0.6"],
            [fr(1, 3) + " = 0.33", "0.33 stops too early. " + fr(1, 3) + " = 0.333… = 0." + bar("3")],
            [fr(1, 6) + " = 0." + bar("16"), "Only the 6 repeats: 0.1666… = 0.1" + bar("6")],
            ["140% = 0.14", "Divide by 100: 140% = 1.4 (more than 100% is more than 1)"],
        ])
    )


FAQ = [
    {"q": "What do Grade 7 students learn about fractions, decimals and percents in BC?",
     "a": "The BC Grade 7 math curriculum covers the relationships between decimals, fractions, ratios and percents. Students change between the forms, including repeating decimals such as 1/3 = 0.333… and percents such as 12.5% and 150%, and use them to compare amounts and solve problems."},
    {"q": "What is a repeating decimal and how do you write it?",
     "a": "A repeating decimal has digits that repeat for ever, such as 2/3 = 0.666… You can write it with dots or with a bar over only the digits that repeat, so 1/6 = 0.1666… has the bar over the 6 alone."},
    {"q": "How do you change a fraction to a percent?",
     "a": "Divide the numerator by the denominator, then multiply by 100. For example, 3/8 = 3 ÷ 8 = 0.375, and 0.375 × 100 = 37.5%."},
    {"q": "Are fractions, decimals and percents on the Grade 7 FSA?",
     "a": "The Grade 7 Foundation Skills Assessment (FSA) checks numeracy based on the BC curriculum, so working easily with fractions, decimals and percents is useful practice for it."},
]


def mark_large(u, pattern):
    """Tag pictures that must print larger (hundred grids, number lines, fraction bars, short division)."""
    rx = re.compile(r"<svg (?=[^>]*aria-label='" + pattern + ")")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u


def gen():
    rnd = random.Random(37806)
    P = People(rnd)
    sets = [set_fraction_decimal(), set_decimal_percent(), set_fraction_percent(), set_compare(), set_problems(P)]
    balance(sets, rnd)
    seen = set()
    for s in sets:
        assert len(s["items"]) == 20, (s["title"], len(s["items"]))
        assert sorted(it["a"] for it in s["items"]) == sorted([0, 1, 2, 3] * 5)
        for it in s["items"]:
            assert len(set(it["c"])) == 4, it
            assert it["q"].count("<svg") <= 1
            k = re.sub(r"<[^>]+>", "", it["q"]) + "|" + "|".join(sorted(it["c"]))
            assert k not in seen, it["q"]
            seen.add(k)
    u = {
        "country": "ca-bc", "subject": "math", "grade": "grade-7", "slug": "fractions-decimals-and-percents", "sort": 6,
        "updated": UPDATED, "pdf_url": "",
        "title": "Grade 7 Fractions, Decimals and Percents",
        "seo_title": "Grade 7 Fractions, Decimals and Percents Worksheets: Free Math Practice with Answer Key (BC Curriculum)",
        "short_title": "Fractions, decimals and percents",
        "domain": "Number",
        "standard_code": "Grade 7: Number",
        "standard_url": "https://curriculum.gov.bc.ca/curriculum/mathematics/7/core",
        "standard_text": "Relationships between decimals, fractions, ratios, and percents",
        "meta_desc": "Free Grade 7 math worksheets on fractions, decimals and percents for the BC curriculum: repeating decimals like 1/3 = 0.333…, percents like 12.5% and 150%, comparing and ordering mixed forms, and word problems with test scores and win records. 100 questions with an answer key, good FSA numeracy practice.",
        "key_big": "A fraction is a division: 1/8 = 1 ÷ 8 = 0.125 = 12.5%. If a remainder comes back, the decimal repeats: 1/3 = 0.333…",
        "key_sub": "Multiply a decimal by 100 to get a percent: 0.4 = 40%, not 4%, and 1.5 = 150%. Put the repeat bar only over the digits that repeat: 1/6 = 0.1666…",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }
    return mark_large(u, "(hundred grid|[0-9]+ hundred grids|number line|fraction bar|short division)")


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
